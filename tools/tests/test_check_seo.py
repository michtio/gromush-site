"""Tests for tools/check_seo.py on a fresh build in a temp dir, then with seeded faults.
Run: python3 -I -m unittest discover -s tools/tests"""
import re
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "src"))

import check_seo  # noqa: E402
from gen import build as b  # noqa: E402

ORIGIN = "https://michtio.github.io"


class CheckSeo(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = Path(tempfile.mkdtemp())
        cls.clean = cls.tmp / "clean"
        b.build(base="/gromush-site/", out=cls.clean)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp)

    def setUp(self):
        self.out = self.tmp / "case"
        shutil.copytree(self.clean, self.out)

    def tearDown(self):
        shutil.rmtree(self.out)

    def check(self):
        return "\n".join(check_seo.check(self.out, "/gromush-site/", ORIGIN))

    def edit(self, rel, fn):
        path = self.out / rel
        path.write_text(fn(path.read_text(encoding="utf-8")), encoding="utf-8")

    def test_clean_build_has_no_problems(self):
        self.assertEqual(self.check(), "")

    def test_wrong_base_is_reported(self):
        self.assertIn("canonical", "\n".join(check_seo.check(self.out, "/", ORIGIN)))

    def test_seeded_faults(self):
        self.edit("index.html", lambda h: re.sub(r"<title>.*?</title>", "<title>Thuis</title>", h, count=1))
        self.edit("index.html", lambda h: h.replace('"@type": "LocalBusiness",', '"@type": "LocalBusiness", "offers": {"price": 1},', 1))
        self.edit("404.html", lambda h: h.replace('<meta name="robots" content="noindex">', "", 1))
        self.edit("sitemap.xml", lambda h: h.replace("</urlset>", f"<url><loc>{ORIGIN}/gromush-site/_dev/componenten/</loc></url>\n</urlset>"))
        out = self.check()
        self.assertIn("/: title does not name GroMush (R1)", out)
        self.assertIn("/: og:title", out)
        self.assertIn("'offers' is not allowed", out)
        self.assertIn("'price' is not allowed", out)
        self.assertIn("/404.html: must be noindex", out)
        self.assertIn("_dev/componenten/ is not an indexable page", out)

    def test_duplicate_description_and_missing_sitemap_entry(self):
        desc = re.search(r'<meta name="description" content="([^"]*)"', (self.out / "index.html").read_text()).group(1)
        self.edit("_dev/componenten/index.html",
                  lambda h: re.sub(r'<meta name="description" content="[^"]*"', f'<meta name="description" content="{desc}"', h, count=1))
        self.edit("sitemap.xml", lambda h: h.replace(f"<url><loc>{ORIGIN}/gromush-site/</loc></url>\n", ""))
        out = self.check()
        self.assertIn("/: same description as /_dev/componenten/ (R40)", out)
        self.assertIn(f"sitemap.xml: misses {ORIGIN}/gromush-site/", out)

    def test_forward_page_rules(self):
        (self.out / "zwammen" / "weg").mkdir(parents=True)
        page = (self.out / "404.html").read_text(encoding="utf-8")
        page = page.replace("<title>", '<meta http-equiv="refresh" content="0; url=/gromush-site/elders/"><title>Weg · ', 1)
        page = re.sub(r'<meta name="description" content="', '<meta name="description" content="Weg. ', page, count=1)
        (self.out / "zwammen" / "weg" / "index.html").write_text(page, encoding="utf-8")
        self.assertIn("/zwammen/weg/: refresh target '/gromush-site/elders/' and canonical None disagree", self.check())


if __name__ == "__main__":
    unittest.main()
