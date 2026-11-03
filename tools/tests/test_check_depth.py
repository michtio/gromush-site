"""Unit tests for tools/check_depth.py (R7, AC9): sitemap parsing and click depth over built and pending pages.

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
import check_depth  # noqa: E402

PAGE = "<!DOCTYPE html><html><body>{}</body></html>"
SITEMAP = """# x

## Page tree

```
/                     Home
├── /a                A
│   └── /a/b          B
└── legal: /c
```
"""


def run(argv):
    buf = io.StringIO()
    with redirect_stdout(buf):
        code = check_depth.main(argv)
    return code, buf.getvalue().strip().splitlines()


class TestCheckDepth(unittest.TestCase):
    def site(self, files):
        d = tempfile.mkdtemp()
        for rel, body in files.items():
            path = os.path.join(d, rel)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                f.write(body)
        return d

    def test_real_sitemap_has_29_pages(self):
        paths = check_depth.sitemap_paths()
        self.assertEqual(len(paths), 29)
        self.assertEqual(paths[0], "/")
        self.assertIn("/voorwaarden/", paths)
        self.assertIn("/leveringsregio/blankenberge/", paths)

    def test_depth_built_and_pending(self):
        d = self.site({"sitemap.md": SITEMAP,
                       "index.html": PAGE.format('<a href="/s/a/">a</a><a href="/s/c/#x">c</a><a href="https://x.org/s/a/b/">x</a>'),
                       "a/index.html": PAGE.format('<a href="/s/a/b/">b</a>')})
        code, lines = run([d, "--base", "/s/", "--sitemap", os.path.join(d, "sitemap.md")])
        self.assertEqual((code, lines[-1]), (0, "4 of 4 sitemap pages within 2 clicks (2 built, 2 pending)"))

    def test_too_deep_and_unbuilt_parent_fail(self):
        d = self.site({"sitemap.md": SITEMAP,
                       "index.html": PAGE.format('<a href="/s/a/">a</a><a href="/s/c/">c</a>'),
                       "a/index.html": PAGE.format('<a href="/s/z/">z</a>'),
                       "z/index.html": PAGE.format('<a href="/s/a/b/">b</a>')})
        code, lines = run([d, "--base", "/s/", "--sitemap", os.path.join(d, "sitemap.md")])
        self.assertEqual(code, 1)
        self.assertIn("/a/b/: not reachable within 2 clicks", lines)


if __name__ == "__main__":
    unittest.main()
