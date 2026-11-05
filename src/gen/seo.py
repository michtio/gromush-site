"""SEO for the GroMush build (plan S8: AD4, AD5, AD17, AD18; PRD R1, R8, R17, R40).

- Page metadata: every page declares {% block title %} and {% block description %} (README-build.md). After
  rendering, page_meta() reads them back from the HTML and check_pages() fails the build when one is missing,
  does not name GroMush (R1), or is shared by two pages (R40).
- Open Graph: add_open_graph() writes og:* tags into the head of every indexable page, taken from the same
  title, description and canonical, so they can never disagree. A page may set its own og:image (og_image()
  helper in {% block head %}); the default comes from site.json seo.og_image.
- Structured data (AD18), from data only: jsonld_site() puts Organization on every indexable page and
  LocalBusiness (addressLocality only, never a street address) on the homepage; jsonld_product() (no offers,
  no price) and jsonld_recipe() are template helpers for the product and inspiration pages.
- sitemap_xml() and robots_txt(): the sitemap lists every indexable page (not noindex, not 404, not /_dev/).

Docs: https://www.sitemaps.org/protocol.html, https://developers.google.com/search/docs/crawling-indexing/robots/create-robots-txt,
https://ogp.me/, https://schema.org/Organization, https://schema.org/LocalBusiness, https://schema.org/Product,
https://schema.org/Recipe, https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls
"""
import html
import json
import re
from xml.sax.saxutils import escape as xml_escape

from .picture import RENDER_DIR, fallback_widths, height_for, rendered_name, widths_for
from .template import Markup, escape

BRAND = "GroMush"
SCHEMA = "https://schema.org"
TITLE = re.compile(r"<title>(.*?)</title>", re.S)
DESCRIPTION = re.compile(r'<meta name="description" content="([^"]*)"\s*/?>')
NOINDEX = re.compile(r'<meta name="robots" content="[^"]*\bnoindex\b')
CANONICAL = re.compile(r'<link rel="canonical" href="([^"]*)"')
OG_TAG = re.compile(r'<meta property="(og:[a-z:_]+)"')
FORBIDDEN_KEYS = ("offers", "price", "streetaddress")  # R3, R40: no price, no street address in JSON-LD


class SeoError(ValueError):
    pass


# ---------- page metadata ----------
def page_meta(page_html):
    """Title, description (unescaped text), noindex and canonical as the rendered page declares them."""
    title = TITLE.search(page_html)
    desc = DESCRIPTION.search(page_html)
    canonical = CANONICAL.search(page_html)
    return {
        "title": html.unescape(" ".join(title.group(1).split())) if title else "",
        "description": html.unescape(" ".join(desc.group(1).split())) if desc else "",
        "noindex": bool(NOINDEX.search(page_html)),
        "canonical": canonical.group(1) if canonical else None,
    }


def is_indexable(page_path, meta):
    """In the sitemap and with Open Graph: not noindex, not the 404 page, not a /_dev/ page."""
    return not meta["noindex"] and page_path != "/404.html" and not page_path.startswith("/_dev/")


def check_pages(pages):
    """pages: [(template name, page path, meta)]. Problems: missing or brandless title or description (R1, R40),
    a title or description shared by two pages (R40), an indexable /_dev/ or 404 page."""
    problems = []
    seen = {"title": {}, "description": {}}
    for name, path, meta in pages:
        for key in ("title", "description"):
            value = meta[key]
            if not value:
                problems.append(f"{name}: no {key}; declare {{% block {key} %}} (R40)")
                continue
            if value in seen[key]:
                problems.append(f"{name}: same {key} as {seen[key][value]}: {value!r} (R40: unique)")
            else:
                seen[key][value] = name
        if meta["title"] and BRAND not in meta["title"]:
            problems.append(f"{name}: the title must name {BRAND} (R1): {meta['title']!r}")
        if (path == "/404.html" or path.startswith("/_dev/")) and not meta["noindex"]:
            problems.append(f"{name}: {path} must be noindex")
    return problems


# ---------- Open Graph ----------
def fallback_image(img, static_dir):
    """(width, ext, root-relative path) of an images.json entry's largest jpeg/png rendering: the file every
    crawler and link preview can read."""
    width = fallback_widths(widths_for(img.width))[-1]
    for ext in ("jpg", "png"):
        name = rendered_name(img.id, width, ext)
        if (static_dir / RENDER_DIR / name).is_file():
            return width, ext, f"/{RENDER_DIR}/{name}"
    raise SeoError(f"image {img.id!r}: no {width} px jpg or png rendered yet (tools/images.py)")


def og_image_tags(img, abs_url, static_dir):
    """og:image with type, width, height and alt for an images.json entry (ogp.me structured image properties)."""
    if not img.get("alt"):
        raise SeoError(f"image {img.id!r} has no alt text for og:image:alt (R37)")
    width, ext, path = fallback_image(img, static_dir)
    src = abs_url(path)
    return Markup(
        f'<meta property="og:image" content="{escape(src)}">\n'
        f'<meta property="og:image:type" content="image/{"png" if ext == "png" else "jpeg"}">\n'
        f'<meta property="og:image:width" content="{width}">\n'
        f'<meta property="og:image:height" content="{height_for(img, width)}">\n'
        f'<meta property="og:image:alt" content="{escape(img.alt)}">\n')


def add_open_graph(page_html, meta, site, default_image):
    """Insert the og:* tags an indexable page does not set itself, right before </head>."""
    present = set(OG_TAG.findall(page_html))
    if not meta["canonical"]:
        raise SeoError("an indexable page needs a canonical link")
    tags = [("og:type", "website"), ("og:site_name", site.name), ("og:locale", site.lang.replace("-", "_")),
            ("og:title", meta["title"]), ("og:description", meta["description"]), ("og:url", meta["canonical"])]
    out = "".join(f'<meta property="{p}" content="{escape(v)}">\n' for p, v in tags if p not in present)
    if "og:image" not in present:
        out += default_image
    if "</head>" not in page_html:
        raise SeoError("page has no </head>")
    return page_html.replace("</head>", out + "</head>", 1)


# ---------- structured data (AD18) ----------
def _script(obj):
    text = json.dumps(obj, ensure_ascii=False, indent=1)
    forbidden = find_forbidden(obj)
    if forbidden:
        raise SeoError(f"JSON-LD must not carry {', '.join(forbidden)} (R3, R40)")
    return Markup('<script type="application/ld+json">\n' + text.replace("</", "<\\/") + "\n</script>\n")


def find_forbidden(value, found=None):
    """Keys anywhere in a JSON-LD value that hold a price, an offer or a street address."""
    found = [] if found is None else found
    if isinstance(value, dict):
        for k, v in value.items():
            if any(bad in k.lower() for bad in FORBIDDEN_KEYS):
                found.append(k)
            find_forbidden(v, found)
    elif isinstance(value, list):
        for v in value:
            find_forbidden(v, found)
    return found


def make_jsonld(site, flags, towns, abs_url, image_url):
    """Template helpers. image_url(id) is the absolute URL of an images.json entry's largest fallback."""
    org_id = abs_url("/") + "#organisatie"

    def organization():
        org = {"@type": "Organization", "@id": org_id, "name": site.name, "url": abs_url("/"),
               "logo": image_url("logo"), "email": site.email}
        if flags.phone_published:
            org["telephone"] = site.phone.tel
        org["sameAs"] = [site.socials.instagram.url, site.socials.facebook.url]
        return org

    def jsonld_site(page_path):
        """Organization on every page; LocalBusiness with addressLocality only on the homepage (AD18)."""
        out = _script({"@context": SCHEMA, **organization()})
        if page_path == "/":
            biz = {"@context": SCHEMA, "@type": "LocalBusiness", "@id": abs_url("/") + "#kwekerij",
                   "name": site.name, "url": abs_url("/"), "image": image_url(site.seo.og_image),
                   "logo": image_url("logo"), "email": site.email,
                   "address": {"@type": "PostalAddress", "addressLocality": site.locality, "addressCountry": "BE"},
                   "areaServed": [t.name for t in sorted(towns, key=lambda t: t.nav_order)],
                   "parentOrganization": {"@id": org_id}}
            if flags.phone_published:
                biz["telephone"] = site.phone.tel
            out = Markup(out + _script(biz))
        return out

    def jsonld_product(v):
        """Product for a variety page: name, Latin name, taste sentence, photo, brand. Never offers or price."""
        return _script({"@context": SCHEMA, "@type": "Product", "name": v.name, "alternateName": v.latin,
                        "description": v.taste_sentence, "image": image_url(v.photo),
                        "url": abs_url(f"/zwammen/{v.slug}/"), "brand": {"@id": org_id}})

    def jsonld_recipe(r):
        """Recipe from recipes.json; only the fields the recipe actually has."""
        obj = {"@context": SCHEMA, "@type": "Recipe", "name": r.title, "author": {"@id": org_id}}
        if r.get("id"):
            obj["url"] = abs_url("/inspiratie/") + "#recept-" + r.id
        if r.get("intro"):
            obj["description"] = r.intro
        if r.get("image"):
            obj["image"] = image_url(r.image)
        if r.get("servings"):
            obj["recipeYield"] = r.servings
        if r.get("ingredients"):
            obj["recipeIngredient"] = list(r.ingredients)
        if r.get("steps"):
            # a step is a string or {title?, text} (S18)
            obj["recipeInstructions"] = [
                {"@type": "HowToStep", **({"name": s.title} if s.get("title") else {}), "text": s.text}
                if isinstance(s, dict) else {"@type": "HowToStep", "text": s} for s in r.steps]
        return _script(obj)

    return {"jsonld_site": jsonld_site, "jsonld_product": jsonld_product, "jsonld_recipe": jsonld_recipe}


# ---------- sitemap and robots ----------
def sitemap_xml(urls):
    """sitemaps.org 0.9 urlset with <loc> only: no lastmod (a build date is not a content change)."""
    rows = "".join(f"<url><loc>{xml_escape(u)}</loc></url>\n" for u in urls)
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + rows + "</urlset>\n")


def robots_txt(sitemap_url):
    """Allow everything (noindex pages must stay crawlable for their noindex to be seen); name the sitemap."""
    return f"User-agent: *\nAllow: /\n\nSitemap: {sitemap_url}\n"
