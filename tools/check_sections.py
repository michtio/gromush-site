"""Section structure check on built pages (plan S11 AC16; also S12 AC18, S13 AC19). Python 3 stdlib only.

  python3 -I tools/check_sections.py <file.html>... --order hero,intro,smaak      sections appear in exactly this order
  python3 -I tools/check_sections.py <file.html>... --before startup,helper       section a comes before section b
  python3 -I tools/check_sections.py <file.html>... --primary-action /proefbox/   that link is inside hero and slot
        [--in hero,slot]                                                          (sections to search; default hero,slot)
        [--template product]                                                      only pages of that template

Conventions (for page builders):
  - A section is any element with data-section="<id>"; ids are read in document order (nested ones count too).
  - A page opts in by carrying data-template="<name>" on an element (product pages: data-template="product").
    Files without any data-template are skipped (listed on stderr), so a shell glob such as
    docs/zwammen/*/index.html leaves out the /zwammen/ overview and forward pages. --template narrows to one name.
  - --order: the page's data-section ids must equal the list, in that order, nothing more or less.
  - --before a,b: both present and the first a comes before the first b.
  - --primary-action PATH: every searched section holds an <a href> whose path (query and fragment dropped)
    ends with PATH, so the base path (/gromush-site/) does not matter: /proefbox/ matches
    /gromush-site/proefbox/?type=x#formulier.
Several checks may be combined. Prints one line per problem, then "N ok" (N checked pages) when there are none,
else "N problems"; exit 1 on any problem or when no page was checked.
"""
import argparse
import sys
from html.parser import HTMLParser
from urllib.parse import urlsplit

VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}


class Sections(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.templates, self.order, self.links = [], [], {}
        self._stack = []  # (tag, section id or None)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get("data-template"):
            self.templates.append(a["data-template"])
        sid = a.get("data-section")
        if sid:
            self.order.append(sid)
            self.links.setdefault(sid, [])
        if tag == "a" and a.get("href"):
            for _, open_id in self._stack:
                if open_id:
                    self.links[open_id].append(a["href"])
        if tag not in VOID:
            self._stack.append((tag, sid))

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID and self._stack:
            self._stack.pop()

    def handle_endtag(self, tag):
        for i in range(len(self._stack) - 1, -1, -1):
            if self._stack[i][0] == tag:
                del self._stack[i:]
                break


def ids(value):
    return [x.strip() for x in value.split(",") if x.strip()]


def check(path, args):
    parser = Sections()
    with open(path, encoding="utf-8") as fh:
        parser.feed(fh.read())
    if not parser.templates or (args.template and args.template not in parser.templates):
        return None
    problems = []
    if args.order:
        want = ids(args.order)
        if parser.order != want:
            problems.append(f"{path}: order {','.join(parser.order) or '(none)'} is not {','.join(want)}")
    if args.before:
        first, second = ids(args.before)[:2]
        if first not in parser.order or second not in parser.order:
            problems.append(f"{path}: --before needs both {first} and {second}")
        elif parser.order.index(first) > parser.order.index(second):
            problems.append(f"{path}: {first} comes after {second}")
    if args.primary_action:
        target = args.primary_action.rstrip("/") + "/" if not args.primary_action.endswith("/") else args.primary_action
        for sid in ids(args.within):
            hrefs = parser.links.get(sid)
            if hrefs is None:
                problems.append(f"{path}: no data-section {sid!r}")
            elif not any(urlsplit(h).path.endswith(target) for h in hrefs):
                problems.append(f"{path}: no link to {args.primary_action} in {sid}")
    return problems


def main(argv=None):
    ap = argparse.ArgumentParser(description="Check data-section order and primary actions on built pages.")
    ap.add_argument("files", nargs="+")
    ap.add_argument("--order")
    ap.add_argument("--before")
    ap.add_argument("--primary-action")
    ap.add_argument("--in", dest="within", default="hero,slot")
    ap.add_argument("--template")
    args = ap.parse_args(argv)
    if not (args.order or args.before or args.primary_action):
        ap.error("give --order, --before and/or --primary-action")
    checked, problems = 0, []
    for path in args.files:
        result = check(path, args)
        if result is None:
            print(f"skipped (no matching data-template): {path}", file=sys.stderr)
            continue
        checked += 1
        problems += result
    for p in problems:
        print(p)
    if problems:
        print(f"{len(problems)} problems")
        return 1
    if not checked:
        print("0 pages checked")
        return 1
    print(f"{checked} ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
