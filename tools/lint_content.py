"""Content lint for the built site (plan AD16): PRD rules R1, R2, R2a, R3, R5, R21, R23.

usage: python3 -I tools/lint_content.py <dir-or-file>... [--root DIR] [--rules tools/lint_rules.json] [--flags src/data/flags.json]

Reads every .html file under the given folders, extracts the text a visitor can read (visible
text, alt/title/aria-label/placeholder, button values, meta description and Open Graph content;
never script, style or comments) and applies the rules in lint_rules.json, which document every
reading taken. Prints one line per hit, then "N hits". Exit 0 when there are none, 1 otherwise,
2 on a usage error. Page paths (for page-specific rules) are relative to --root, which defaults
to each folder given (so lint `docs`, or pass --root docs when linting one sub-folder or file).
Python 3 stdlib only.
"""
import fnmatch
import json
import os
import re
import sys
from html.parser import HTMLParser

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_RULES = os.path.join(HERE, "lint_rules.json")
DEFAULT_FLAGS = os.path.join(HERE, "..", "src", "data", "flags.json")

# Elements that do not break a run of text. Everything else starts a new unit.
INLINE = {"a", "abbr", "b", "bdi", "bdo", "br", "cite", "code", "data", "del", "dfn", "em", "i", "img",
          "ins", "kbd", "label", "mark", "picture", "q", "s", "samp", "small", "source", "span", "strong",
          "sub", "sup", "time", "u", "var", "wbr", "tspan", "textpath", "svg", "use", "path", "g"}
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}
SKIP = {"script", "style"}
BUTTON_INPUTS = {"submit", "button", "reset"}
SENTENCE_SPLIT = re.compile(r"(?<=[.!?…])\s+|\s*[·|]\s*")
WB_BEFORE, WB_AFTER = r"(?<![\w])", r"(?![\w])"


class Unit:
    """A run of text that reads as one piece: a block's inline text, or one attribute value."""

    def __init__(self, main, kind="text"):
        self.main, self.kind, self.parts = main, kind, []  # parts: (offset, line, text)

    def add(self, text, line):
        offset = sum(len(p[2]) for p in self.parts)
        self.parts.append((offset, line, text))

    @property
    def text(self):
        return "".join(p[2] for p in self.parts)

    def line_at(self, offset):
        line, start, text = self.parts[0][1], 0, self.parts[0][2]
        for o, ln, t in self.parts:
            if o <= offset:
                line, start, text = ln, o, t
        return line + text[: max(0, offset - start)].count("\n")


class Extractor(HTMLParser):
    """Collects text units, link texts and href values from one HTML document."""

    def __init__(self, text_attributes, meta_content):
        super().__init__(convert_charrefs=True)
        self.text_attributes, self.meta_content = set(text_attributes), meta_content
        self.units, self.links, self.hrefs = [], [], []
        self.skip = self.main = 0
        self.cur = None
        self.link = None  # [href, text, line, aria-label]

    def flush(self):
        if self.cur is not None and self.cur.text.strip():
            self.units.append(self.cur)
        self.cur = None

    def attr_unit(self, value, line):
        if value and value.strip():
            u = Unit(self.main > 0, "attr")
            u.add(value, line)
            self.units.append(u)

    def handle_starttag(self, tag, attrs):
        a = {k: (v or "") for k, v in attrs}
        line = self.getpos()[0]
        if tag in SKIP:
            self.skip += 1
            return
        if tag not in INLINE:
            self.flush()
        if tag == "main":
            self.main += 1
        for name in ("alt", "title", "aria-label", "placeholder"):
            if name in self.text_attributes and name in a:
                self.attr_unit(a[name], line)
        if "value" in self.text_attributes and tag == "input" and a.get("type", "").lower() in BUTTON_INPUTS:
            self.attr_unit(a.get("value"), line)
        if tag == "meta" and "content" in a:
            key = (a.get("name") or a.get("property") or "").lower()
            if key and any(fnmatch.fnmatch(key, p) for p in self.meta_content):
                self.attr_unit(a["content"], line)
        if "href" in a:
            self.hrefs.append((a["href"], line))
        if tag == "a":
            self.link = [a.get("href", ""), "", line, a.get("aria-label", "")]
        if tag == "br" and self.cur is not None:
            self.cur.add(" ", line)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        if tag in SKIP:
            self.skip = max(0, self.skip - 1)
            return
        if tag == "a" and self.link is not None:
            self.links.append(tuple(self.link))
            self.link = None
        if tag not in INLINE:
            self.flush()
        if tag == "main":
            self.main = max(0, self.main - 1)

    def handle_data(self, data):
        if self.skip:
            return
        if self.cur is None:
            self.cur = Unit(self.main > 0)
        self.cur.add(data, self.getpos()[0])
        if self.link is not None:
            self.link[1] += data

    def close(self):
        super().close()
        self.flush()


def term_regex(terms):
    return WB_BEFORE + "(?:" + "|".join(terms) + ")" + WB_AFTER


def compile_rules(cfg):
    """Turns the JSON rules into dicts with compiled patterns."""
    out = []
    for r in cfg["rules"]:
        r = dict(r)
        src = r.get("pattern") or term_regex(r["terms"])
        r["_re"] = re.compile(src, re.I)
        if "near" in r:
            near = r["near"]
            r["_near"] = re.compile(near if isinstance(near, str) else term_regex(near), re.I)
        if "href_pattern" in r:
            r["_href"] = re.compile(r["href_pattern"], re.I)
        r["_strip"] = [re.compile(re.escape(s).replace(r"\ ", r"\s+"), re.I) for s in r.get("strip", [])]
        if "except_paths_from" in r:
            r["except_paths"] = cfg[r["except_paths_from"]]
        out.append(r)
    return out


def page_path(root, file):
    """docs/voor-wie/chefs/index.html -> /voor-wie/chefs/ ; docs/404.html -> /404.html"""
    rel = os.path.relpath(file, root).replace(os.sep, "/")
    if rel == ".":
        rel = os.path.basename(file)
    if rel == "index.html":
        return "/"
    if rel.endswith("/index.html"):
        return "/" + rel[: -len("index.html")]
    return "/" + rel


def applies(rule, path, flags):
    if rule.get("unless_flag") and flags.get(rule["unless_flag"]) is True:
        return False
    if rule.get("when_flag_false") and flags.get(rule["when_flag_false"]) is not False:
        return False
    if "paths" in rule and path not in rule["paths"]:
        return False
    if "except_paths" in rule and path in rule["except_paths"]:
        return False
    return True


def blank(text, patterns):
    """Replaces allowed phrases with spaces, keeping offsets."""
    for p in patterns:
        text = p.sub(lambda m: " " * len(m.group(0)), text)
    return text


def first_match(rule, text):
    allow = set(rule.get("allow", []))
    for m in rule["_re"].finditer(text):
        if m.group(0) not in allow:
            return m
    return None


def lint_html(html, path, rules, flags, cfg):
    """Returns [(line, rule, matched text, context)] for one document at site path `path`."""
    ex = Extractor(cfg.get("text_attributes", ["alt", "title", "aria-label"]), cfg.get("meta_content", []))
    ex.feed(html)
    ex.close()
    hits = []
    active = [r for r in rules if applies(r, path, flags)]
    for r in active:
        target = r.get("target", "text")
        if target == "href":
            for href, line in ex.hrefs:
                m = r["_re"].search(href.strip())
                if m:
                    hits.append((line, r, m.group(0), href))
        elif target == "link_text":
            for href, text, line, label in ex.links:
                if r["_href"].search(href):
                    m = first_match(r, text + " " + label)
                    if m:
                        hits.append((line, r, m.group(0), " ".join((text + " " + label).split())))
    text_rules = [r for r in active if r.get("target", "text") == "text"]
    for u in ex.units:
        full = u.text
        pos = 0
        for piece in SENTENCE_SPLIT.split(full):
            start = full.find(piece, pos)
            pos = start + len(piece)
            if not piece.strip():
                continue
            for r in text_rules:
                if r.get("region") == "main" and not u.main:
                    continue
                s = blank(piece, r["_strip"])
                m = first_match(r, s)
                if not m:
                    continue
                if "_near" in r:
                    page_wide = path in r.get("near_or_paths", []) and u.main
                    if not page_wide and not r["_near"].search(s):
                        continue
                hits.append((u.line_at(start + m.start()), r, m.group(0), " ".join(piece.split())))
    hits.sort(key=lambda h: h[0])
    return hits


def html_files(target, root=None):
    """Lists (site root, file) for every .html file under target."""
    if os.path.isfile(target):
        return [(root or os.path.dirname(target), target)]
    out = []
    for d, dirs, files in os.walk(target):
        dirs.sort()
        out += [(root or target, os.path.join(d, f)) for f in sorted(files) if f.endswith(".html")]
    return out


def load_config(rules_path, flags_path):
    with open(rules_path, encoding="utf-8") as f:
        cfg = json.load(f)
    with open(flags_path, encoding="utf-8") as f:
        flags = json.load(f)
    return cfg, compile_rules(cfg), flags


def main(argv):
    args, rules_path, flags_path, root = [], DEFAULT_RULES, DEFAULT_FLAGS, None
    it = iter(argv)
    for a in it:
        if a == "--rules":
            rules_path = next(it)
        elif a == "--flags":
            flags_path = next(it)
        elif a == "--root":
            root = next(it)
        else:
            args.append(a)
    if not args:
        print(__doc__.strip().splitlines()[2].strip(), file=sys.stderr)
        return 2
    cfg, rules, flags = load_config(rules_path, flags_path)
    total = 0
    for target in args:
        if not os.path.exists(target):
            print(f"not found: {target}", file=sys.stderr)
            return 2
        for site_root, file in html_files(target, root):
            with open(file, encoding="utf-8") as f:
                html = f.read()
            for line, r, match, ctx in lint_html(html, page_path(site_root, file), rules, flags, cfg):
                total += 1
                ctx = ctx if len(ctx) <= 110 else ctx[:107] + "..."
                print(f'{file}:{line}: {r["req"]} {r["ac"]} [{r["id"]}] "{match.strip()}" in "{ctx}"')
    print(f"{total} hits")
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
