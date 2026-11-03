"""S10 range overview (/zwammen/): one card per variety in the range, each linking to its product page (R13);
a variety taken out of the range drops out of the overview (R17, AC14).
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


class Overview(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        shutil.copytree(b.DATA, self.tmp / "data")

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def render(self):
        b.build(base="/gromush-site/", out=self.tmp / "out", data_dir=self.tmp / "data")
        html = (self.tmp / "out/zwammen/index.html").read_text(encoding="utf-8")
        return html[html.index("<main"):html.index("</main>")]

    def varieties(self):
        return json.loads((self.tmp / "data/varieties.json").read_text(encoding="utf-8"))

    def test_one_card_per_variety_in_range_with_product_link(self):  # R4, R13
        main = self.render()
        in_range = sorted((v for v in self.varieties() if v["in_range"]), key=lambda v: v["nav_order"])
        self.assertEqual(re.findall(r'data-card="([a-z]+)"', main), [v["key"] for v in in_range])
        links = re.findall(r'class="tc-more link-action" href="([^"]+)"', main)
        self.assertEqual(links, [f"/gromush-site/zwammen/{v['slug']}/" for v in in_range])
        for v in in_range:
            self.assertIn(f"<h3>{v['name']}</h3>", main)
            self.assertIn(" · ".join(v["taste_words"]), main)

    def test_removed_variety_is_not_listed(self):  # R17, AC14
        vs = self.varieties()
        for v in vs:
            if v["key"] == "grijze":
                v["in_range"] = False
        (self.tmp / "data/varieties.json").write_text(json.dumps(vs, ensure_ascii=False), encoding="utf-8")
        main = self.render()
        self.assertNotIn('data-card="grijze"', main)
        self.assertNotIn("Grijze oesterzwam", main)
        self.assertNotIn("/zwammen/grijze-oesterzwam/", main)
        self.assertEqual(len(re.findall(r'data-card="', main)), sum(1 for v in vs if v["in_range"]))


if __name__ == "__main__":
    unittest.main()
