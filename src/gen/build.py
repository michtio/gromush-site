"""GroMush static build: src/data/*.json + src/templates/** -> docs/ (plan AD1-AD5).

Run from the repo root: python3 -I build.py [--base /gromush-site/] [--out docs]
"""
import argparse
import json
import re
import shutil
import sys
from pathlib import Path
from urllib.parse import quote

from . import hyphae, levering, seo
from .picture import render as render_picture
from .template import AttrDict, Environment, Markup, TemplateError, escape, wrap

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "src" / "data"
TEMPLATES = ROOT / "src" / "templates"
STATIC = ROOT / "src" / "static"

# R1: any spelling of the brand other than "GroMush" (lowercase "gromush" is the domain and handle)
BRAND = re.compile(r"(?i)\bgro[\s_-]?mush")
PAGE_PATH = re.compile(r"^/(?:[a-z0-9]+(?:-[a-z0-9]+)*/)*$")  # R8 + AD5: lowercase slugs, trailing slash
DEV_PREFIX = "/_dev/"  # internal reference pages (components page): noindex, never in nav or sitemap
DATA_FILES = ("site", "flags", "varieties", "towns", "audiences", "recipes", "future_species", "forms", "images", "nav", "wip")
NAV_MAX_ITEMS = 6                      # R6: at most six items plus the ProefBox CTA
NAV_CTA_LABEL = "Gratis ProefBox"      # R5: the header CTA, word for word
CHEFBOX = re.compile(r"(?i)chef[\s_-]*box")  # R5/AC7: never labels the free offer


class BuildError(Exception):
    pass


# ---------- data ----------
def load_data(data_dir=DATA):
    data = AttrDict()
    for name in DATA_FILES:
        path = Path(data_dir) / f"{name}.json"
        try:
            data[name] = wrap(json.loads(path.read_text(encoding="utf-8")))
        except FileNotFoundError:
            raise BuildError(f"missing data file: {path}") from None
        except json.JSONDecodeError as exc:
            raise BuildError(f"{path.name}: invalid JSON: {exc}") from None
    validate(data)
    return data


def brand_hits(text):
    return [m.group(0) for m in BRAND.finditer(text) if m.group(0) not in ("GroMush", "gromush")]


def _strings(value):
    if isinstance(value, dict):
        for v in value.values():
            yield from _strings(v)
    elif isinstance(value, list):
        for v in value:
            yield from _strings(v)
    elif isinstance(value, str):
        yield value


def validate(data):
    problems = []
    for name in DATA_FILES:
        for s in _strings(data[name]):
            for hit in brand_hits(s):
                problems.append(f"{name}.json: brand written as {hit!r} (R1: always 'GroMush')")
    for key, value in data.flags.items():
        if not isinstance(value, bool):
            problems.append(f"flags.json: {key} must be true or false")
    for key in ("certified_organic", "startup_phase", "show_future_species", "phone_published"):
        if key not in data.flags:
            problems.append(f"flags.json: missing {key}")
    seen = set()
    for v in data.varieties:
        for key in ("key", "slug", "name", "latin", "taste_words", "taste_sentence", "in_range", "nav_order"):
            if key not in v:
                problems.append(f"varieties.json: {v.get('slug', '?')} misses {key}")
        if len(v.get("taste_words", [])) != 3:
            problems.append(f"varieties.json: {v.get('slug')} needs exactly three taste words (R4)")
        if not PAGE_PATH.match(f"/{v.get('slug', '')}/"):
            problems.append(f"varieties.json: slug {v.get('slug')!r} is not a lowercase slug (R8)")
        if v.get("slug") in seen:
            problems.append(f"varieties.json: duplicate slug {v.get('slug')}")
        seen.add(v.get("slug"))
    for t in data.towns.towns:
        if not PAGE_PATH.match(f"/{t.slug}/"):
            problems.append(f"towns.json: slug {t.slug!r} is not a lowercase slug (R8)")
    problems += validate_nav(data.nav)
    if "promo" in data.site and CHEFBOX.search(" ".join(_strings(data.site.promo))):
        problems.append("site.json: the ProefBox promo must not say ChefBox (R5)")
    base = data.site.base
    if not (base.startswith("/") and base.endswith("/")):
        problems.append("site.json: base must start and end with '/'")
    if problems:
        raise BuildError("data problems:\n  " + "\n  ".join(problems))


def validate_nav(nav):
    """R5, R6, R8 on nav.json: item count, CTA label and path, URL shape, no ChefBox label."""
    problems = []
    items = nav.get("main", [])
    if not 1 <= len(items) <= NAV_MAX_ITEMS:
        problems.append(f"nav.json: {len(items)} items; the primary navigation holds 1 to {NAV_MAX_ITEMS} (R6)")
    cta = nav.get("cta") or {}
    if cta.get("label") != NAV_CTA_LABEL or cta.get("path") != "/proefbox/":
        problems.append(f"nav.json: the CTA must be {NAV_CTA_LABEL!r} to /proefbox/ (R5, R6)")
    links = list(items) + [cta]
    for item in items:
        links += item.get("children", [])
    for col in nav.get("footer", []):
        links += [col] + list(col.get("links", []))
    for link in links:
        if "from" in link:
            if link["from"] not in ("varieties", "towns"):
                problems.append(f"nav.json: unknown list {link['from']!r} (varieties or towns)")
            continue
        label = link.get("label", link.get("title", ""))
        if CHEFBOX.search(label):
            problems.append(f"nav.json: {label!r}: ChefBox never labels a navigation link (R5)")
        if "path" in link and not PAGE_PATH.match(link["path"]):
            problems.append(f"nav.json: path {link['path']!r} breaks the URL scheme (R8, AD5)")
    return problems


def resolve_nav(nav, varieties, towns):
    """nav.json with every {"from": ...} expanded into links: varieties in range in nav order, towns in nav order."""
    def expand(links):
        out = []
        for link in links:
            if link.get("from") == "varieties":
                out += [AttrDict(label=v.name, path=f"/zwammen/{v.slug}/") for v in varieties]
            elif link.get("from") == "towns":
                out += [AttrDict(label=t.name, path=f"/leveringsregio/{t.slug}/")
                        for t in sorted(towns, key=lambda t: t.nav_order)]
            else:
                out.append(link)
        return out

    items = [AttrDict({**item, "children": expand(item.get("children", []))}) for item in nav["main"]]
    footer = [AttrDict({**col, "links": expand(col.get("links", []))}) for col in nav.get("footer", [])]
    return AttrDict(label=nav.label, main=items, cta=nav.cta, footer=footer)  # "main", not "items" (dict.items)


def in_range(varieties):
    """Varieties currently sold, in navigation order (R13, R17)."""
    return sorted((v for v in varieties if v.in_range), key=lambda v: v.nav_order)


# ---------- helpers ----------
def normalize_base(base):
    base = "/" + base.strip("/") + "/" if base.strip("/") else "/"
    return base


def make_helpers(site, base, images, static=STATIC):
    base = normalize_base(base)
    origin = site.origin.rstrip("/")
    by_id = {img.id: img for img in images}

    def url(path):
        """Internal path -> path under the base (AD4). '/zwammen/' -> '/gromush-site/zwammen/'."""
        if not isinstance(path, str) or not path.startswith("/") or path.startswith("//"):
            raise ValueError(f"url() needs a root-relative path like '/zwammen/', got {path!r}")
        return base[:-1] + path

    def abs_url(path):
        """Absolute URL for canonical, Open Graph and sitemap."""
        return origin + url(path)

    def t(key):
        """Shared interface string from site.json 'strings'."""
        if key not in site.strings:
            raise KeyError(f"no string {key!r} in site.json strings")
        return site.strings[key]

    def picture(image_id, cls="", sizes=None, loading=None, decorative=False):
        """<picture> with avif/webp sources and a jpeg/png fallback for an images.json entry (S3, R37)."""
        img = by_id.get(image_id)
        if img is None:
            raise KeyError(f"no image {image_id!r} in images.json")
        return render_picture(img, url=url, static_dir=static, cls=cls, sizes=sizes, loading=loading,
                              decorative=decorative)

    def mailto(subject):
        """Native form action of AD7 (no-JS path): 'mailto:<form_recipient>?subject=<percent-encoded>' (RFC 6068)."""
        return f"mailto:{site.form_recipient}?subject={quote(subject, safe='')}"

    return {"url": url, "abs_url": abs_url, "t": t, "picture": picture, "mailto": mailto}


# ---------- routes ----------
def routes(templates=TEMPLATES):
    """(template name, output file relative to out, page path) for every page template.
    pages/index.html -> /, pages/x/index.html and pages/x.html -> /x/, pages/404.html -> 404.html."""
    out = []
    for path in sorted((Path(templates) / "pages").rglob("*.html")):
        rel = path.relative_to(Path(templates) / "pages").as_posix()
        if rel == "404.html":
            out.append((f"pages/{rel}", "404.html", "/404.html"))
            continue
        stem = rel[: -len("index.html")] if rel.endswith("index.html") else rel[: -len(".html")] + "/"
        page_path = "/" + stem
        checked = "/" + page_path[len(DEV_PREFIX):] if page_path.startswith(DEV_PREFIX) else page_path
        if not PAGE_PATH.match(checked):
            raise BuildError(f"page path {page_path!r} breaks the URL scheme (R8, AD5)")
        out.append((f"pages/{rel}", page_path.lstrip("/") + "index.html", page_path))
    return out


# ---------- build ----------
def check_out_dir(out):
    if out.exists() and any(out.iterdir()) and not (out / ".nojekyll").exists():
        raise BuildError(f"{out} exists, is not empty and has no .nojekyll: not a build output, refusing to write")


def seo_helpers(data, abs_url, static):
    """S8 template globals: og_image('id') for a page's own og:image, jsonld_site/product/recipe (AD18)."""
    by_id = {img.id: img for img in data.images.images}

    def image(image_id):
        if image_id not in by_id:
            raise KeyError(f"no image {image_id!r} in images.json")
        return by_id[image_id]

    def image_url(image_id):
        return abs_url(seo.fallback_image(image(image_id), Path(static))[2])

    return {"og_image": lambda image_id: seo.og_image_tags(image(image_id), abs_url, Path(static)),
            **seo.make_jsonld(data.site, data.flags, data.towns.towns, abs_url, image_url)}


PRODUCT_TEMPLATE = "products/zwam.html"  # S11: one template (R14), rendered per variety; not under pages/, so not routed
PRODUCT_COPY = ("plural", "hero_title", "intro_title", "intro_text", "appearance", "timeline", "uses", "who_title", "who",
                "kitchen_image")  # varieties.json "page": the fields every product page needs (optional ones hide a block)


def product_pages(env, varieties, targets):
    """S11, R14: /zwammen/<slug>/ from products/zwam.html for every variety in the range (never for one out of
    it: that path is its forward page, R17). A page template at the same path is an error."""
    out = []
    for v in varieties:
        path = f"/zwammen/{v.slug}/"
        target = path.lstrip("/") + "index.html"
        if target in targets:
            raise BuildError(f"{path}: rendered by {PRODUCT_TEMPLATE} and by a page template")
        missing = [k for k in PRODUCT_COPY if k not in v.get("page", {})]
        if missing or len(v.get("page", {}).get("timeline", [])) != 4:
            raise BuildError(f"varieties.json: {v.slug} page misses {', '.join(missing) or 'four timeline steps'} (S11)")
        html = env.get(PRODUCT_TEMPLATE).render(
            {"page": AttrDict(path=path, template=PRODUCT_TEMPLATE, dev=False), "variety": v})
        out.append((f"{PRODUCT_TEMPLATE} ({v.slug})", target, path, html))
    return out


TOWN_TEMPLATE = "towns/gemeente.html"  # S19: one template (template H), rendered per delivery town; not under pages/
TOWN_COPY = ("title", "description", "image", "subtitle", "tagline", "intro", "region", "audiences", "route", "delivery",
             "proefbox")  # towns.json "page": the fields every town page needs


def town_pages(env, towns, targets):
    """S19, R28: /leveringsregio/<slug>/ from towns/gemeente.html for every delivery town in towns.json.
    A page template at the same path is an error."""
    out = []
    for t in sorted(towns, key=lambda t: t.nav_order):
        path = f"/leveringsregio/{t.slug}/"
        target = path.lstrip("/") + "index.html"
        if target in targets:
            raise BuildError(f"{path}: rendered by {TOWN_TEMPLATE} and by a page template")
        missing = [k for k in TOWN_COPY if k not in t.get("page", {})]
        if missing:
            raise BuildError(f"towns.json: {t.slug} page misses {', '.join(missing)} (S19)")
        html = env.get(TOWN_TEMPLATE).render(
            {"page": AttrDict(path=path, template=TOWN_TEMPLATE, dev=False), "town": t})
        out.append((f"{TOWN_TEMPLATE} ({t.slug})", target, path, html))
    return out


def forward_pages(env, all_varieties, targets):
    """AD17, R17: /zwammen/<slug>/ for every variety out of the range: noindex, refresh and canonical to /zwammen/."""
    out = []
    for v in all_varieties:
        if v.in_range:
            continue
        path = f"/zwammen/{v.slug}/"
        target = path.lstrip("/") + "index.html"
        if target in targets:
            raise BuildError(f"{path}: {v.slug} is out of the range (in_range false) but a page template renders it")
        html = env.get("layouts/forward.html").render(
            {"page": AttrDict(path=path, template="layouts/forward.html", dev=False), "variety": v})
        out.append((f"layouts/forward.html ({v.slug})", target, path, html))
    return out


def wip_pages(env, wip, targets):
    """'In opbouw' placeholders (src/data/wip.json) for sitemap pages no template renders yet: noindex, no canonical."""
    out = []
    for item in wip.pages:
        target = item.path.lstrip("/") + "index.html"
        if target in targets:
            continue
        html = env.get("layouts/wip.html").render(
            {"page": AttrDict(path=item.path, template="layouts/wip.html", dev=False), "wip": item})
        out.append((f"layouts/wip.html ({item.path})", target, item.path, html))
    return out


def write_pages(rendered, out, site, abs_url, og_default):
    """R1 and R40 checks on every rendered page, Open Graph on indexable ones, then write the pages,
    sitemap.xml and robots.txt (S8). Nothing is written when a check fails."""
    checked, problems = [], []
    for name, target, page_path, html in rendered:
        hits = brand_hits(html)
        if hits:
            raise BuildError(f"{name}: brand written as {hits[0]!r} (R1)")
        meta = seo.page_meta(html)
        checked.append((name, page_path, meta))
    problems += seo.check_pages(checked)
    if problems:
        raise BuildError("page metadata problems:\n  " + "\n  ".join(problems))
    written, sitemap = [], []
    for (name, target, page_path, html), (_, _, meta) in zip(rendered, checked):
        if seo.is_indexable(page_path, meta):
            if meta["canonical"] != abs_url(page_path):
                raise BuildError(f"{name}: canonical {meta['canonical']} is not {abs_url(page_path)} (R40)")
            html = seo.add_open_graph(html, meta, site, og_default)
            sitemap.append(abs_url(page_path))
        dest = out / target
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(html, encoding="utf-8")
        written.append(dest)
    for rel, text in (("sitemap.xml", seo.sitemap_xml(sorted(sitemap))), ("robots.txt", seo.robots_txt(abs_url("/sitemap.xml")))):
        (out / rel).write_text(text, encoding="utf-8")
        written.append(out / rel)
    return written


def home_helpers(varieties, towns_data):
    """S9 template globals for the homepage (plan AD13, S9): the radial opening's baked hyphae network and medallion
    places (src/gen/hyphae.py), and the delivery map with the van (src/gen/levering.py). Computed only when a template
    calls them; a town off the drawn route fails the build."""
    names = {v.key: v.name for v in varieties}
    by_key = {v.key: v for v in varieties}

    def hyphae_ring():
        return Markup(hyphae.ring_svg(frozenset(names)))

    def hyphae_medallions():
        return [AttrDict(m, variety=by_key[m["key"]]) for m in hyphae.medallions(names)]

    def levering_points():
        origin = towns_data.map.origin
        return [(origin.name, origin.x, origin.y, True)] + [(t.name, t.map.x, t.map.y, False) for t in towns_data.towns]

    def levering_map():
        points = levering_points()
        off = levering.route_check([(n, x, y) for n, x, y, _ in points])
        if off:
            raise BuildError(f"towns.json: {', '.join(off)} not on the drawn delivery route (src/gen/levering.py ROUTE)")
        return Markup(levering.map_svg(tuple((x, y, home) for _, x, y, home in points)))

    return {"hyphae_ring": hyphae_ring, "hyphae_medallions": hyphae_medallions, "levering_map": levering_map,
            "levering_van": lambda: Markup(levering.van_svg("lv1")), "levering_pos": levering.pct,
            "levering_van_style": levering.van_style, "levering_start": levering.V1_START,
            "levering_route_order": lambda towns: sorted(towns, key=lambda t: levering.route_pos(t.map.x, t.map.y))}


def build(base=None, out=ROOT / "docs", data_dir=DATA, templates=TEMPLATES, static=STATIC):
    out = Path(out)
    data = load_data(data_dir)
    base = normalize_base(base if base is not None else data.site.base)
    check_out_dir(out)
    helpers = make_helpers(data.site, base, data.images.images, static)
    varieties = in_range(data.varieties)
    env = Environment(templates, {
        **helpers, "site": data.site, "flags": data.flags, "data": data,
        "varieties": varieties, "base": base, "nav": resolve_nav(data.nav, varieties, data.towns.towns),
        **seo_helpers(data, helpers["abs_url"], static),
        **home_helpers(varieties, data.towns),
    })
    rendered = []
    for name, target, page_path in routes(templates):
        html = env.get(name).render({"page": AttrDict(path=page_path, template=name, dev=page_path.startswith(DEV_PREFIX))})
        rendered.append((name, target, page_path, html))
    if (Path(templates) / PRODUCT_TEMPLATE).is_file():
        rendered += product_pages(env, varieties, {target for _, target, _, _ in rendered})
    if (Path(templates) / TOWN_TEMPLATE).is_file():
        rendered += town_pages(env, data.towns.towns, {target for _, target, _, _ in rendered})
    rendered += forward_pages(env, data.varieties, {target for _, target, _, _ in rendered})
    rendered += wip_pages(env, data.wip, {target for _, target, _, _ in rendered})
    written = write_pages(rendered, out, data.site, helpers["abs_url"], env.globals["og_image"](data.site.seo.og_image))
    for src in sorted(p for p in Path(static).rglob("*") if p.is_file() and p.name != ".DS_Store"):
        dest = out / src.relative_to(static)
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)
        written.append(dest)
    (out / ".nojekyll").write_text("", encoding="utf-8")
    written.append(out / ".nojekyll")
    stale = sorted(p for p in out.rglob("*") if p.is_file() and p not in set(written) and p.name != ".DS_Store")
    return written, stale, base


def main(argv=None):
    parser = argparse.ArgumentParser(description="Build the GroMush site into docs/.")
    parser.add_argument("--base", help="URL base path, e.g. /gromush-site/ (GitHub Pages) or / (domain root)")
    parser.add_argument("--out", default=str(ROOT / "docs"), help="output directory (default: docs)")
    args = parser.parse_args(argv)
    try:
        written, stale, base = build(base=args.base, out=Path(args.out))
    except (BuildError, TemplateError, KeyError, ValueError) as exc:
        print(f"build failed: {exc}", file=sys.stderr)
        return 1
    pages = sum(1 for p in written if p.suffix == ".html")
    print(f"{pages} pages written to {args.out} (base {base})")
    for p in stale:
        print(f"warning: stale file not produced by this build: {p}", file=sys.stderr)
    return 0
