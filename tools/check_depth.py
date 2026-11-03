"""Click-depth check for PRD R7 / AC9: every sitemap page is reachable within N clicks of the homepage.

usage: python3 -I tools/check_depth.py <dir> --base /gromush-site/ [--sitemap PATH] [--max 2]

Reads the page paths from the "Page tree" code block of specs/2026-10-19-gromush-site/sitemap.md (the
legal line included), then crawls the built HTML under <dir> breadth-first from the homepage, following
every <a href> that resolves to an internal page (base path stripped, query and fragment dropped). A page
that is linked but not built yet (a pending page, see tools/pending_pages.txt) counts as found at that
depth; it cannot be crawled further, so links that will live on it are not credited.

Prints one line per sitemap page deeper than --max or not found, then
"N of M sitemap pages within K clicks (B built, P pending)". Exit 0 when all are within reach, else 1.
Python 3 stdlib only.
"""
import argparse
import os
import re
import sys
from collections import deque
from html.parser import HTMLParser
from urllib.parse import urlsplit

HERE = os.path.dirname(os.path.abspath(__file__))
SITEMAP = os.path.join(HERE, "..", "specs", "2026-10-19-gromush-site", "sitemap.md")


def sitemap_paths(path=SITEMAP):
    """Page paths from the sitemap's "Page tree" block, in order, with the trailing slash of plan AD5."""
    with open(path, encoding="utf-8") as f:
        text = f.read()
    block = text.split("## Page tree", 1)[1].split("```")[1]
    out = []
    for line in block.splitlines():
        for m in re.finditer(r"(?<![\w/])(/[a-z0-9-]*(?:/[a-z0-9-]+)*)", line):
            p = m.group(1) if m.group(1).endswith("/") else m.group(1) + "/"
            if p not in out:
                out.append(p)
    return out


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.hrefs = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            href = dict(attrs).get("href")
            if href:
                self.hrefs.append(href)


def page_links(file, base):
    """Internal page paths ('/x/') linked from one HTML file."""
    p = Links()
    with open(file, encoding="utf-8") as f:
        p.feed(f.read())
    out = []
    for href in p.hrefs:
        parts = urlsplit(href)
        if parts.scheme or parts.netloc or not parts.path.startswith(base):
            continue
        path = "/" + parts.path[len(base):]
        if path.endswith("/"):
            out.append(path)
    return out


def crawl(root, base, max_depth):
    """Breadth-first click depths from '/' over the built pages; returns {path: depth}."""
    def file_for(path):
        return os.path.join(root, *[x for x in path.split("/") if x], "index.html")

    depth = {"/": 0}
    queue = deque(["/"])
    while queue:
        path = queue.popleft()
        if depth[path] >= max_depth or not os.path.isfile(file_for(path)):
            continue
        for link in page_links(file_for(path), base):
            if link not in depth:
                depth[link] = depth[path] + 1
                queue.append(link)
    return depth, file_for


def main(argv):
    ap = argparse.ArgumentParser(description="Click depth of every sitemap page from the homepage (R7, AC9).")
    ap.add_argument("dir")
    ap.add_argument("--base", required=True)
    ap.add_argument("--sitemap", default=SITEMAP)
    ap.add_argument("--max", type=int, default=2)
    args = ap.parse_args(argv)
    base = "/" + args.base.strip("/") + "/" if args.base.strip("/") else "/"
    if not os.path.isfile(os.path.join(args.dir, "index.html")):
        print(f"no homepage: {os.path.join(args.dir, 'index.html')}", file=sys.stderr)
        return 2
    wanted = sitemap_paths(args.sitemap)
    depth, file_for = crawl(args.dir, base, args.max)
    ok = built = pending = 0
    for path in wanted:
        d = depth.get(path)
        if d is None:
            print(f"{path}: not reachable within {args.max} clicks")
            continue
        ok += 1
        if os.path.isfile(file_for(path)):
            built += 1
        else:
            pending += 1
    print(f"{ok} of {len(wanted)} sitemap pages within {args.max} clicks ({built} built, {pending} pending)")
    return 0 if ok == len(wanted) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
