"""SEO check on a built site (plan S8; PRD R1, R8, R17, R40, AD17, AD18). Python 3 stdlib only.

  python3 -I tools/check_seo.py docs --base /gromush-site/ [--origin https://michtio.github.io]

Per page (every *.html under the folder; docs/x/index.html is /x/, docs/404.html is the 404 page):
  - a title naming GroMush and a meta description; both unique across all pages (R1, R40)
  - indexable pages: at least one <h1>, its text on no other indexable page (AC26: town pages each their own)
  - indexable pages (no robots noindex): canonical = origin + base + path with a trailing slash (AD4, AD5);
    og:title, og:description and og:url equal to title, description and canonical; og:type; og:image an
    absolute URL to a file in the folder, with og:image:alt
  - the 404 page and /_dev/ pages are noindex; a page with a meta refresh is noindex and its canonical is the
    refresh target (AD17 forward page)
  - every application/ld+json block parses, uses only Organization, LocalBusiness, Product, Recipe at the top
    (LocalBusiness only on /, Recipe only on /inspiratie/, Product only on /zwammen/<slug>/), and has no
    offers, price or streetAddress anywhere (AD18, R3, R40)
Site-wide: sitemap.xml (sitemaps.org 0.9) lists exactly the canonicals of the indexable pages; robots.txt names
the sitemap's absolute URL.

Prints one line per problem and "N problems"; exit 1 when N > 0.
"""
import argparse
import json
import re
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
SITEMAP_NS = "http://www.sitemaps.org/schemas/sitemap/0.9"
TOP_TYPES = {"Organization", "LocalBusiness", "Product", "Recipe"}
FORBIDDEN = ("offers", "price", "streetaddress")
PRODUCT_PATH = re.compile(r"^/zwammen/[a-z0-9-]+/$")


class Head(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title, self.meta, self.og, self.canonicals, self.jsonld = None, {}, {}, [], []
        self.h1s, self._h1 = [], None  # S19: the text of every <h1> (AC26)
        self._in_title = self._in_ld = False
        self._buf = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "h1":
            self._h1 = []
        if tag == "title":
            self._in_title, self._buf = True, []
        elif tag == "meta":
            if a.get("name"):
                self.meta[a["name"].lower()] = a.get("content") or ""
            if a.get("http-equiv", "").lower() == "refresh":
                self.meta["refresh"] = a.get("content") or ""
            if (a.get("property") or "").startswith("og:"):
                self.og.setdefault(a["property"], a.get("content") or "")
        elif tag == "link" and "canonical" in (a.get("rel") or "").split():
            self.canonicals.append(a.get("href") or "")
        elif tag == "script" and (a.get("type") or "").lower() == "application/ld+json":
            self._in_ld, self._buf = True, []

    def handle_data(self, data):
        if self._in_title or self._in_ld:
            self._buf.append(data)
        if self._h1 is not None:
            self._h1.append(data)

    def handle_endtag(self, tag):
        if tag == "h1" and self._h1 is not None:
            self.h1s.append(" ".join("".join(self._h1).split()))
            self._h1 = None
        if tag == "title" and self._in_title:
            self.title, self._in_title = " ".join("".join(self._buf).split()), False
        elif tag == "script" and self._in_ld:
            self.jsonld.append("".join(self._buf))
            self._in_ld = False


def page_path(rel):
    rel = rel.as_posix()
    if rel == "404.html":
        return "/404.html"
    if rel == "index.html":
        return "/"
    if rel.endswith("/index.html"):
        return "/" + rel[: -len("index.html")]
    return "/" + rel  # a loose .html file: reported, the URL scheme has none


def forbidden_keys(value, found):
    if isinstance(value, dict):
        for k, v in value.items():
            if any(bad in k.lower() for bad in FORBIDDEN):
                found.append(k)
            forbidden_keys(v, found)
    elif isinstance(value, list):
        for v in value:
            forbidden_keys(v, found)
    return found


def check_jsonld(path, blocks, problems):
    types = []
    for i, text in enumerate(blocks, 1):
        where = f"{path}: JSON-LD block {i}"
        try:
            obj = json.loads(text)
        except json.JSONDecodeError as exc:
            problems.append(f"{where} does not parse: {exc}")
            continue
        items = obj.get("@graph", [obj]) if isinstance(obj, dict) else obj
        for item in items if isinstance(items, list) else [items]:
            kind = item.get("@type") if isinstance(item, dict) else None
            types.append(kind)
            if kind not in TOP_TYPES:
                problems.append(f"{where}: type {kind!r} is not one of {', '.join(sorted(TOP_TYPES))} (AD18)")
            if kind == "Recipe":  # S18: a Recipe needs a name and image, ingredients and steps (schema.org/Recipe)
                for key in ("name", "image", "recipeIngredient", "recipeInstructions"):
                    if not item.get(key):
                        problems.append(f"{where}: Recipe has no {key}")
        if isinstance(obj, dict) and obj.get("@context") not in ("https://schema.org", "http://schema.org"):
            problems.append(f"{where}: @context is not schema.org")
        for key in forbidden_keys(obj, []):
            problems.append(f"{where}: {key!r} is not allowed (R3, R40: no offers, price or street address)")
    if "LocalBusiness" in types and path != "/":
        problems.append(f"{path}: LocalBusiness only on the homepage (AD18)")
    if "Recipe" in types and path != "/inspiratie/":
        problems.append(f"{path}: Recipe only on /inspiratie/ (AD18)")
    if "Product" in types and not PRODUCT_PATH.match(path):
        problems.append(f"{path}: Product only on /zwammen/<slug>/ (AD18)")
    return types


def check(folder, base, origin):
    folder = Path(folder)
    base = "/" + base.strip("/") + "/" if base.strip("/") else "/"
    prefix = origin.rstrip("/") + base[:-1]
    problems, seen_title, seen_desc, seen_h1, indexable = [], {}, {}, {}, set()
    pages = sorted(folder.rglob("*.html"))
    if not pages:
        return [f"{folder}: no html files"]
    for file in pages:
        path = page_path(file.relative_to(folder))
        h = Head()
        h.feed(file.read_text(encoding="utf-8"))
        title, desc = h.title or "", h.meta.get("description", "").strip()
        noindex = "noindex" in h.meta.get("robots", "").lower()
        if not title:
            problems.append(f"{path}: no <title>")
        elif "GroMush" not in title:
            problems.append(f"{path}: title does not name GroMush (R1): {title!r}")
        if not desc:
            problems.append(f"{path}: no meta description")
        for value, seen, what in ((title, seen_title, "title"), (desc, seen_desc, "description")):
            if value and value in seen:
                problems.append(f"{path}: same {what} as {seen[value]} (R40)")
            elif value:
                seen[value] = path
        if len(h.canonicals) > 1:
            problems.append(f"{path}: {len(h.canonicals)} canonical links")
        canonical = h.canonicals[0] if h.canonicals else None
        if (path == "/404.html" or path.startswith("/_dev/")) and not noindex:
            problems.append(f"{path}: must be noindex")
        if "refresh" in h.meta:
            target = h.meta["refresh"].split("url=", 1)[-1].strip() if "url=" in h.meta["refresh"] else ""
            if not noindex:
                problems.append(f"{path}: a forward page (meta refresh) must be noindex (AD17)")
            if not target.startswith(base) or canonical != origin.rstrip("/") + target:
                problems.append(f"{path}: refresh target {target!r} and canonical {canonical!r} disagree (AD17)")
        types = check_jsonld(path, h.jsonld, problems)
        if noindex or path == "/404.html" or path.startswith("/_dev/"):
            continue
        indexable.add(prefix + path)
        if not re.fullmatch(r"/(?:[a-z0-9]+(?:-[a-z0-9]+)*/)*", path):
            problems.append(f"{path}: not a lowercase path with a trailing slash (R8, AD5)")
        if canonical != prefix + path:
            problems.append(f"{path}: canonical {canonical!r}, expected {prefix + path!r}")
        expect = {"og:title": title, "og:description": desc, "og:url": prefix + path}
        for prop, want in expect.items():
            if h.og.get(prop) != want:
                problems.append(f"{path}: {prop} {h.og.get(prop)!r} does not match {want!r}")
        if not h.og.get("og:type"):
            problems.append(f"{path}: no og:type")
        image = h.og.get("og:image", "")
        if not image.startswith(prefix + "/"):
            problems.append(f"{path}: og:image {image!r} is not an absolute URL under {prefix}/")
        elif not (folder / image[len(prefix) + 1:]).is_file():
            problems.append(f"{path}: og:image {image!r} has no file in {folder}")
        if not h.og.get("og:image:alt"):
            problems.append(f"{path}: no og:image:alt")
        if "Organization" not in types:
            problems.append(f"{path}: no Organization JSON-LD (AD18)")
        h1s = {h for h in h.h1s if h}  # the homepage carries one heading in two layouts (radial and list)
        if not h1s:
            problems.append(f"{path}: no <h1> (AC26)")
        for text in sorted(h1s):
            if text in seen_h1:
                problems.append(f"{path}: same h1 as {seen_h1[text]}: {text!r} (AC26)")
            else:
                seen_h1[text] = path
    problems += check_sitemap(folder, prefix, indexable)
    return problems


def check_sitemap(folder, prefix, indexable):
    problems = []
    try:
        root = ET.parse(folder / "sitemap.xml").getroot()
    except (OSError, ET.ParseError) as exc:
        return [f"sitemap.xml: {exc}"]
    if root.tag != f"{{{SITEMAP_NS}}}urlset":
        problems.append(f"sitemap.xml: root is {root.tag}, expected urlset in {SITEMAP_NS}")
    locs = [(el.text or "").strip() for el in root.iter(f"{{{SITEMAP_NS}}}loc")]
    for loc in sorted({x for x in locs if locs.count(x) > 1}):
        problems.append(f"sitemap.xml: {loc} listed twice")
    for loc in sorted(set(locs) - indexable):
        problems.append(f"sitemap.xml: {loc} is not an indexable page")
    for loc in sorted(indexable - set(locs)):
        problems.append(f"sitemap.xml: misses {loc}")
    try:
        robots = (folder / "robots.txt").read_text(encoding="utf-8")
    except OSError as exc:
        return problems + [f"robots.txt: {exc}"]
    if f"Sitemap: {prefix}/sitemap.xml" not in robots.splitlines():
        problems.append(f"robots.txt: no 'Sitemap: {prefix}/sitemap.xml' line")
    if not re.search(r"(?im)^user-agent:\s*\*", robots):
        problems.append("robots.txt: no 'User-agent: *' group")
    return problems


def main(argv=None):
    parser = argparse.ArgumentParser(description="SEO check on a built site (S8, R40).")
    parser.add_argument("folder")
    parser.add_argument("--base", required=True, help="URL base path, e.g. /gromush-site/ or /")
    parser.add_argument("--origin", help="default: origin in src/data/site.json")
    args = parser.parse_args(argv)
    origin = args.origin or json.loads((ROOT / "src" / "data" / "site.json").read_text(encoding="utf-8"))["origin"]
    if urlsplit(origin).scheme != "https":
        print(f"origin {origin!r} must be https", file=sys.stderr)
        return 2
    problems = check(args.folder, args.base, origin)
    for p in problems:
        print(p)
    print(f"{len(problems)} problems")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
