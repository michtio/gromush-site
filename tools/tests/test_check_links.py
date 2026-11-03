"""Unit tests for tools/check_links.py on the fixtures and on throwaway folders.

Run: python3 -I -m unittest discover -s tools/tests
"""
import io
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stdout

TOOLS = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, TOOLS)
import check_links  # noqa: E402

FIXTURES = os.path.join(TOOLS, "tests", "fixtures")
PAGE = "<!DOCTYPE html><html><head><title>x</title></head><body>{}</body></html>"


def run(argv):
    buf = io.StringIO()
    with redirect_stdout(buf):
        code = check_links.main(argv)
    return code, buf.getvalue().strip().splitlines()


class TestCheckLinks(unittest.TestCase):
    def site(self, files):
        d = tempfile.mkdtemp()
        for rel, body in files.items():
            path = os.path.join(d, rel)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                f.write(body)
        return d

    def test_fixtures_report_the_three_seeds(self):
        code, lines = run([FIXTURES, "--base", "/gromush-site/", "--origin", "https://michtio.github.io"])
        self.assertEqual(code, 1)
        self.assertEqual(lines[-1], "1 broken, 2 off-base")
        self.assertEqual(len(lines), 4)
        self.assertTrue(all("links/index.html" in line for line in lines[:-1]))

    def test_srcset_split(self):
        self.assertEqual(check_links.srcset_urls("a.jpg 400w, b.jpg 800w"), ["a.jpg", "b.jpg"])
        self.assertEqual(check_links.srcset_urls("a.jpg"), ["a.jpg"])

    def test_root_base_and_fragments(self):
        d = self.site({"index.html": PAGE.format('<a href="/x/#a">x</a><a href="#nope">n</a>'),
                       "x/index.html": PAGE.format('<p id="a">a</p><a href="/x">no slash</a>')})
        code, lines = run([d, "--base", "/", "--origin", "https://example.org"])
        self.assertEqual(lines[-1], "2 broken, 0 off-base")
        self.assertTrue(any("#nope" in line for line in lines))
        self.assertTrue(any("trailing slash" in line for line in lines))

    def test_external_hosts_and_own_origin(self):
        d = self.site({"index.html": PAGE.format(
            '<a href="https://www.instagram.com/x/">i</a><a href="https://cdn.example.com/x.js">c</a>'
            '<a href="https://michtio.github.io/gromush-site/">own</a><a href="https://michtio.github.io/elders/">off</a>')})
        code, lines = run([d, "--base", "/gromush-site/", "--origin", "https://michtio.github.io"])
        self.assertEqual(lines[-1], "0 broken, 1 off-base, 1 external-not-allowed")

    def test_css_urls(self):
        d = self.site({"index.html": PAGE.format(""), "css/site.css": "a{background:url(../img/x.png)} b{background:url('/img/y.png')}",
                       "img/x.png": ""})
        code, lines = run([d, "--base", "/gromush-site/", "--origin", "https://example.org"])
        self.assertEqual(lines[-1], "0 broken, 1 off-base")

    def test_images_flag(self):
        d = self.site({"index.html": PAGE.format(
            '<img src="/a.png" alt="" width="1" height="1" srcset="/a.png 1x">'
            '<img src="/a.png" alt="x">'
            '<picture><source srcset="/a.png 1x" type="image/webp"><img src="/a.png" alt="" width="1" height="1"></picture>'
            '<img src="/i.svg" alt="" width="1" height="1">'), "a.png": "", "i.svg": ""})
        code, lines = run([d, "--base", "/", "--origin", "https://example.org", "--images"])
        self.assertEqual(lines[-1], "0 broken, 0 off-base, 1 image problems")
        self.assertIn("missing width, height, srcset", lines[0])

    def test_same_chrome(self):
        chrome = '<header class="site-header"><a href="/" {}>Home</a></header><main>{}</main><footer><p>f</p></footer>'
        d = self.site({"index.html": PAGE.format(chrome.format('aria-current="page"', "a")),
                       "b/index.html": PAGE.format(chrome.format("", "b")),
                       "c/index.html": PAGE.format(chrome.format("", "c").replace("<p>f</p>", "<p>g</p>")),
                       "old/index.html": '<html><head><meta http-equiv="refresh" content="0; url=/"></head><body><a href="/">x</a></body></html>'})
        code, lines = run([d, "--base", "/", "--origin", "https://example.org", "--same-chrome"])
        self.assertEqual(lines[-1], "0 broken, 0 off-base, 1 chrome differences")
        self.assertIn("c/index.html", lines[0])

    def test_pending_pages_counted_apart_from_broken(self):
        d = self.site({"index.html": PAGE.format('<a href="/later/">l</a><a href="/later/#x">l</a><a href="/weg/">w</a>'
                                                 '<a href="/nu/">n</a>'),
                       "nu/index.html": PAGE.format(""),
                       "pending.txt": "# comment\n/later/\n/nu\n"})
        code, lines = run([d, "--base", "/", "--origin", "https://example.org", "--pending", os.path.join(d, "pending.txt")])
        self.assertEqual(code, 1)
        self.assertEqual(lines[-1], "1 broken, 0 off-base, 1 pending")
        self.assertTrue(any("/weg/" in line for line in lines))
        self.assertTrue(any(line.startswith("warning: /nu/ is built") for line in lines))

    def test_pending_only_is_clean(self):
        d = self.site({"index.html": PAGE.format('<a href="/later/">l</a>'), "p.txt": "/later/\n"})
        code, lines = run([d, "--base", "/", "--origin", "https://example.org", "--pending", os.path.join(d, "p.txt")])
        self.assertEqual((code, lines[-1]), (0, "0 broken, 0 off-base, 1 pending"))


if __name__ == "__main__":
    unittest.main()
