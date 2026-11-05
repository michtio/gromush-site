"""AC9 (PRD R7): every sitemap page is reachable within two clicks of the homepage.

usage: python3 -I tools/crawl.py <dir> --base /gromush-site/ [--sitemap PATH] [--max 2]

A thin alias of tools/check_depth.py (the crawl, the sitemap parsing and the counting live there; plan S21 names
this script in its gate). Prints one line per sitemap page deeper than --max or not found, then
"N/M within K clicks". Exit 0 when all are within reach, else 1. Python 3 stdlib only.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from check_depth import parse, report  # noqa: E402


def main(argv):
    args, base = parse(argv, "AC9: sitemap pages within K clicks of the homepage (alias of check_depth.py).")
    if not os.path.isfile(os.path.join(args.dir, "index.html")):
        print(f"no homepage: {os.path.join(args.dir, 'index.html')}", file=sys.stderr)
        return 2
    missing, ok, total, _built, _pending = report(args.dir, base, args.sitemap, args.max)
    for path in missing:
        print(f"{path}: not reachable within {args.max} clicks")
    print(f"{ok}/{total} within {args.max} clicks")
    return 0 if ok == total else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
