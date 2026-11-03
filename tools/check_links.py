"""Link and base-path checker for the built site (plan AD4, AD16).

usage: python3 -I tools/check_links.py <dir> --base /gromush-site/ [--origin URL] [--images] [--same-chrome]

Checks every href, src, srcset, action, poster and formaction in the .html files under <dir>, the
absolute URLs in og:/twitter: meta tags, and every url() in the .css files:

- internal paths must start with --base, else "off-base" (relative paths in HTML are off-base too:
  everything goes through url(); fragment-only "#x" and query-only "?x" links are same-page);
- an internal path must resolve to a file under <dir> ("/x/" -> x/index.html; a folder linked
  without its trailing slash is broken, plan AD5), and a "#fragment" must exist as an id on the
  target page ("#" and "#top" are always fine);
- absolute URLs on the site's own origin (--origin, default from src/data/site.json) are internal;
- other hosts must be on the allowlist (mailto:, tel:, data:, wa.me, instagram.com, facebook.com),
  else "external-not-allowed".
- url() in CSS may be relative (resolved against the CSS file); absolute ones must carry the base.

--images       every <img> has width, height, alt (may be empty) and srcset; an <img> inside a
               <picture> whose <source> has a srcset counts as having one, and .svg images need
               none. Images marked flagged in src/data/images.json are listed as warnings (R44).
--pending FILE paths from sitemap.md that are not built yet (one site path per line, "/zwammen/", "#" comments;
               tools/pending_pages.txt, each removed by the slice that builds it). A link to a missing page on
               that list counts as "pending", not "broken", and is reported separately; a listed page that
               exists is a warning (take it off the list).
--same-chrome  the site header (first <header> directly under <body>) and footer (last <footer>
               directly under <body>) are identical on every page, after removing aria-current
               (the current-page marker). Forward pages (meta refresh) are skipped.

Prints one line per problem, then "N broken, M off-base" (plus the other counts when not zero, and
"P pending" with --pending: the number of distinct unbuilt pages that are linked).
Exit 0 when everything is clean, 1 otherwise, 2 on a usage error. Python 3 stdlib only.
"""
import argparse
import collections
import json
import os
import re
import sys
from html.parser import HTMLParser
from urllib.parse import unquote, urlsplit

HERE = os.path.dirname(os.path.abspath(__file__))
SITE_JSON = os.path.join(HERE, "..", "src", "data", "site.json")
IMAGES_JSON = os.path.join(HERE, "..", "src", "data", "images.json")
ALLOWED_SCHEMES = {"mailto", "tel", "data"}
ALLOWED_HOSTS = ("wa.me", "instagram.com", "facebook.com", "gegevensbeschermingsautoriteit.be")
URL_ATTRS = {"href", "src", "action", "poster", "formaction", "data"}
SRCSET_ATTRS = {"srcset", "imagesrcset"}
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}
CSS_URL = re.compile(r"url\(\s*(['\"]?)(.*?)\1\s*\)", re.I)


def srcset_urls(value):
    """Splits a srcset into its URLs ("a.jpg 400w, b.jpg 800w" -> [a.jpg, b.jpg])."""
    return [c.strip().split()[0] for c in re.split(r",\s+|,(?=\S+\s+\d)", value.strip()) if c.strip()]


class Page(HTMLParser):
    """Collects URLs, ids, images and the raw header/footer of one HTML document."""

    def __init__(self, raw):
        super().__init__(convert_charrefs=True)
        self.raw = raw
        self.line_starts = [0] + [m.end() for m in re.finditer(r"\n", raw)]
        self.urls, self.ids, self.images = [], set(), []
        self.refresh = False
        self.stack, self.picture_srcset = [], None
        self.header = self.footer = None
        self._open = {}

    def pos_offset(self):
        line, col = self.getpos()
        return self.line_starts[line - 1] + col

    def handle_starttag(self, tag, attrs):
        a = {k: (v if v is not None else "") for k, v in attrs}
        line = self.getpos()[0]
        for k in ("id", "name"):
            if a.get(k) and (k == "id" or tag == "a"):
                self.ids.add(a[k])
        for k, v in a.items():
            if k in URL_ATTRS and (k != "data" or tag == "object"):
                self.urls.append((k, v, line))
            elif k in SRCSET_ATTRS:
                for u in srcset_urls(v):
                    self.urls.append((k, u, line))
        if tag == "meta":
            key = (a.get("property") or a.get("name") or "").lower()
            if key.startswith(("og:", "twitter:")) and re.match(r"^https?://", a.get("content", "")):
                self.urls.append(("content", a["content"], line))
            if a.get("http-equiv", "").lower() == "refresh":
                self.refresh = True
        if tag == "picture":
            self.picture_srcset = False
        elif tag == "source" and self.picture_srcset is not None and a.get("srcset"):
            self.picture_srcset = True
        elif tag == "img":
            self.images.append((a, line, bool(self.picture_srcset)))
        parent = self.stack[-1] if self.stack else None
        if tag in ("header", "footer") and parent == "body":
            self._open[tag] = self.pos_offset()
        if tag not in VOID:
            self.stack.append(tag)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID and self.stack and self.stack[-1] == tag:
            self.stack.pop()

    def handle_endtag(self, tag):
        if tag == "picture":
            self.picture_srcset = None
        if tag in self._open and len(self.stack) >= 2 and self.stack[-1] == tag and self.stack[-2] == "body":
            start, end = self._open.pop(tag), self.raw.index(">", self.pos_offset()) + 1
            span = self.raw[start:end]
            if tag == "header" and self.header is None:
                self.header = span
            elif tag == "footer":
                self.footer = span
        if tag in self.stack:
            while self.stack and self.stack.pop() != tag:
                pass


class Checker:
    """Resolves URLs against the site folder and the base path."""

    def __init__(self, root, base, origin, pending=()):
        self.root, self.base = os.path.abspath(root), "/" + base.strip("/") + "/" if base.strip("/") else "/"
        self.origin = urlsplit(origin).netloc.lower() if origin else ""
        self.pages, self.problems = {}, []
        self.pending, self.pending_linked = set(pending), set()

    def page(self, path):
        if path not in self.pages:
            with open(path, encoding="utf-8") as f:
                raw = f.read()
            p = Page(raw)
            p.feed(raw)
            p.close()
            self.pages[path] = p
        return self.pages[path]

    def report(self, kind, file, line, attr, url, why):
        self.problems.append((kind, os.path.relpath(file), line, attr, url, why))

    def check_internal(self, file, line, attr, path, fragment, url):
        if not path.startswith(self.base):
            self.report("off-base", file, line, attr, url, f"does not start with {self.base}")
            return
        rel = unquote(path[len(self.base):])
        target = os.path.join(self.root, *[p for p in rel.split("/") if p])
        if path.endswith("/"):
            target = os.path.join(target, "index.html")
        elif os.path.isdir(target):
            self.report("broken", file, line, attr, url, "folder linked without its trailing slash")
            return
        site_path = "/" + rel.lstrip("/")
        if site_path in self.pending and path.endswith("/") and (not os.path.isfile(target) or is_placeholder(target)):
            self.pending_linked.add(site_path)  # unbuilt, or only its "in opbouw" placeholder (src/data/wip.json)
            return
        if not os.path.isfile(target):
            if site_path in self.pending and path.endswith("/"):
                self.pending_linked.add(site_path)
                return
            self.report("broken", file, line, attr, url, f"no file {os.path.relpath(target)}")
            return
        self.check_fragment(file, line, attr, target, fragment, url)

    def check_fragment(self, file, line, attr, target, fragment, url):
        frag = unquote(fragment or "")
        if frag in ("", "top") or not target.endswith(".html"):
            return
        if frag not in self.page(target).ids:
            self.report("broken", file, line, attr, url, f"no id #{frag} on {os.path.relpath(target)}")

    def check_url(self, file, line, attr, url, css=False):
        u = url.strip()
        if not u:
            self.report("broken", file, line, attr, url, "empty URL")
            return
        if u.startswith("#"):
            self.check_fragment(file, line, attr, file, u[1:], url)
            return
        if u.startswith("?"):
            return
        scheme = re.match(r"^([a-zA-Z][a-zA-Z0-9+.-]*):", u)
        if scheme or u.startswith("//"):
            s = scheme.group(1).lower() if scheme else "https"
            if s in ALLOWED_SCHEMES:
                return
            if s not in ("http", "https"):
                self.report("broken", file, line, attr, url, f"{s}: URL")
                return
            parts = urlsplit(u if scheme else "https:" + u)
            host = parts.netloc.lower()
            if host == self.origin:
                self.check_internal(file, line, attr, parts.path or "/", parts.fragment, url)
            elif not any(host == h or host.endswith("." + h) for h in ALLOWED_HOSTS):
                self.report("external-not-allowed", file, line, attr, url, f"host {host} is not on the allowlist")
            return
        parts = urlsplit(u)
        if u.startswith("/"):
            self.check_internal(file, line, attr, parts.path, parts.fragment, url)
        elif css:
            target = os.path.normpath(os.path.join(os.path.dirname(file), unquote(parts.path)))
            if not os.path.isfile(target):
                self.report("broken", file, line, attr, url, f"no file {os.path.relpath(target)}")
        else:
            self.report("off-base", file, line, attr, url, "relative path; internal URLs go through url() and carry the base")

    def check_css(self, file):
        with open(file, encoding="utf-8") as f:
            css = re.sub(r"/\*.*?\*/", lambda m: "\n" * m.group(0).count("\n"), f.read(), flags=re.S)
        for m in CSS_URL.finditer(css):
            self.check_url(file, css.count("\n", 0, m.start()) + 1, "url()", m.group(2), css=True)

    def check_images(self, file, flagged):
        for a, line, picture_srcset in self.page(file).images:
            src = a.get("src", "")
            missing = [k for k in ("width", "height", "alt") if k not in a]
            if "srcset" not in a and not picture_srcset and not src.lower().split("?")[0].endswith(".svg"):
                missing.append("srcset")
            if missing:
                self.report("image", file, line, "img", src, "missing " + ", ".join(missing))
            names = [os.path.basename(urlsplit(u).path) for u in [src] + srcset_urls(a.get("srcset", ""))]
            for fid in flagged:
                if any(n == fid or n.startswith((fid + "-", fid + ".")) for n in names):
                    print(f"warning: {os.path.relpath(file)}:{line}: flagged image '{fid}' (R44, images.json)")
                    break

    def check_chrome(self, files):
        groups = collections.defaultdict(list)
        for f in files:
            p = self.page(f)
            if p.refresh:
                continue
            for part, raw in (("header", p.header), ("footer", p.footer)):
                if raw is None:
                    self.report("chrome", f, 1, part, "", f"no site {part} directly under <body>")
                    continue
                norm = re.sub(r'\s+aria-current\s*=\s*("[^"]*"|\'[^\']*\'|\S+)', "", raw)
                norm = re.sub(r"\s+(/?>)", r"\1", re.sub(r">\s+<", "><", re.sub(r"\s+", " ", norm))).strip()
                groups[part].append((norm, f))
        for part, items in groups.items():
            ref, count = collections.Counter(n for n, _ in items).most_common(1)[0]
            for norm, f in items:
                if norm != ref:
                    i = next((k for k, (x, y) in enumerate(zip(norm, ref)) if x != y), min(len(norm), len(ref)))
                    self.report("chrome", f, 1, part, "", f"differs from {count} other page(s) near: {norm[max(0, i - 40):i + 40]!r}")


def is_placeholder(path):
    """True for an "in opbouw" placeholder page rendered from src/data/wip.json (layouts/wip.html)."""
    with open(path, encoding="utf-8") as fh:
        return 'class="wrap wip"' in fh.read()


def read_pending(path):
    """Site paths from a pending list: one per line, '#' starts a comment, blank lines ignored."""
    with open(path, encoding="utf-8") as f:
        lines = [ln.split("#", 1)[0].strip() for ln in f]
    return [ln if ln.endswith("/") else ln + "/" for ln in lines if ln]


def main(argv):
    ap = argparse.ArgumentParser(description="Check links and base paths in the built site.")
    ap.add_argument("dir")
    ap.add_argument("--base", required=True)
    ap.add_argument("--origin", default=None)
    ap.add_argument("--images", action="store_true")
    ap.add_argument("--same-chrome", action="store_true")
    ap.add_argument("--pending", default=None, help="file with sitemap paths that are not built yet")
    args = ap.parse_args(argv)
    if not os.path.isdir(args.dir):
        print(f"not a folder: {args.dir}", file=sys.stderr)
        return 2
    origin = args.origin
    if origin is None and os.path.isfile(SITE_JSON):
        with open(SITE_JSON, encoding="utf-8") as f:
            origin = json.load(f).get("origin", "")
    pending = read_pending(args.pending) if args.pending else []
    c = Checker(args.dir, args.base, origin, pending)
    html, css = [], []
    for d, dirs, files in os.walk(args.dir):
        dirs.sort()
        for name in sorted(files):
            (html if name.endswith(".html") else css if name.endswith(".css") else []).append(os.path.join(d, name))
    flagged = []
    if args.images and os.path.isfile(IMAGES_JSON):
        with open(IMAGES_JSON, encoding="utf-8") as f:
            flagged = [i["id"] for i in json.load(f).get("images", []) if i.get("flagged")]
    for f in html:
        for attr, url, line in c.page(f).urls:
            c.check_url(f, line, attr, url)
        if args.images:
            c.check_images(f, flagged)
    for f in css:
        c.check_css(f)
    if args.same_chrome:
        c.check_chrome(html)
    for kind, file, line, attr, url, why in c.problems:
        print(f'{file}:{line}: {kind} {attr} "{url}": {why}')
    for p in pending:
        built = os.path.join(c.root, *[x for x in p.split("/") if x], "index.html")
        if os.path.isfile(built) and not is_placeholder(built):
            print(f"warning: {p} is built; remove it from {args.pending}")
    n = collections.Counter(p[0] for p in c.problems)
    summary = f'{n["broken"]} broken, {n["off-base"]} off-base'
    for kind, label in (("external-not-allowed", "external-not-allowed"), ("image", "image problems"), ("chrome", "chrome differences")):
        if n[kind] or (kind == "image" and args.images) or (kind == "chrome" and args.same_chrome):
            summary += f", {n[kind]} {label}"
    if args.pending:
        summary += f", {len(c.pending_linked)} pending"
    print(summary)
    return 1 if c.problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
