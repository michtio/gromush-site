"""Unit tests for S11 product pages (products/zwam.html): R14 order, R16 actions, R17 removal, R4 cross-sell, R40.
Run: python3 -I -m unittest discover -s src/gen/tests"""
import json
import re
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from gen import build as b  # noqa: E402

ORDER = ["hero", "intro", "smaak", "tijdlijn", "kweker", "keuken", "voor-wie", "product", "bewaren", "andere", "slot"]


class ProductPages(unittest.TestCase):
    """Builds into a temp dir from a temp copy of the data."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.data = self.tmp / "data"
        shutil.copytree(b.DATA, self.data)
        self.out = self.tmp / "docs"

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def edit(self, fn):
        path = self.data / "varieties.json"
        value = json.loads(path.read_text(encoding="utf-8"))
        fn(value)
        path.write_text(json.dumps(value, ensure_ascii=False), encoding="utf-8")

    def page(self, slug):
        return (self.out / "zwammen" / slug / "index.html").read_text(encoding="utf-8")

    def build(self):
        b.build(base="/gromush-site/", out=self.out, data_dir=self.data)

    def test_one_page_per_variety_in_r14_order(self):  # R14, AC16
        self.build()
        for v in json.loads((self.data / "varieties.json").read_text(encoding="utf-8")):
            html = self.page(v["slug"])
            self.assertEqual(re.findall(r'data-section="([^"]+)"', html), ORDER, v["slug"])
            self.assertIn('data-template="product"', html)

    def test_order_and_request_links(self):  # R16, AC17
        self.build()
        html = self.page("blauwe-oesterzwam")
        self.assertIn('href="/gromush-site/contact/?reden=bestelling-thuis&amp;soort=blauwe-oesterzwam#formulier"', html)
        self.assertIn('href="/gromush-site/proefbox/?soort=blauwe#formulier"', html)

    def test_cross_sell_uses_canonical_words_and_skips_self(self):  # R4, AC6
        self.edit(lambda vs: vs[0].update(taste_words=["Proefwoord", "twee", "drie"]))
        self.build()
        self.assertIn("Proefwoord · twee · drie", self.page("roze-oesterzwam"))
        self.assertNotIn('href="/gromush-site/zwammen/roze-oesterzwam/"', self.page("roze-oesterzwam").split('data-section="andere"')[1].split('data-section="slot"')[0])

    def test_removed_variety_gets_forward_page_and_leaves_cross_sells(self):  # R17, AC14
        self.edit(lambda vs: [v.update(in_range=False) for v in vs if v["key"] == "grijze"])
        self.build()
        self.assertIn('http-equiv="refresh"', self.page("grijze-oesterzwam"))
        for slug in ("gele-oesterzwam", "blauwe-oesterzwam"):
            self.assertNotIn("Grijze oesterzwam", self.page(slug))

    def test_product_jsonld_without_price(self):  # R40, AD18
        self.build()
        html = self.page("gele-oesterzwam")
        self.assertIn('"@type": "Product"', html)
        self.assertNotIn("offers", html)
        self.assertNotIn("€", html)

    def test_missing_optional_copy_hides_block(self):  # R3
        self.edit(lambda vs: [v["page"].pop("quote", None) for v in vs])
        self.build()
        self.assertNotIn("zw-quote", self.page("gele-oesterzwam"))

    def test_missing_page_copy_fails_clearly(self):
        self.edit(lambda vs: vs[0]["page"].pop("intro_title"))
        with self.assertRaisesRegex(b.BuildError, "gele-oesterzwam page misses intro_title"):
            self.build()


if __name__ == "__main__":
    unittest.main()
