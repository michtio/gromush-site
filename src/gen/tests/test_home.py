"""S9 homepage (/): the radial opening's network (src/gen/hyphae.py) and the delivery map (src/gen/levering.py) are the
approved artwork, the scenes come in R11's order, every variety text comes from data (R4) and the medallions link by
plain name with their own "Vraag aan" action (R10a). Run: python3 -I -m unittest discover -s src/gen/tests"""
import hashlib
import json
import re
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from gen import build as b  # noqa: E402
from gen import hyphae, levering  # noqa: E402
from gen.template import TemplateError  # noqa: E402

# sha256 of the approved artwork: final.html's <!-- RING:START/END --> block (round 4, approved 2026-11-04) and its
# delivery map (variant 1). A change here means the drawing changed: re-run tools/ring_obstacles.py, tools/ringprobes.sh
# and the visual comparison, and have it approved, before updating the hash.
RING_SHA = "7ef8ec82548765d8c0be8b00f4707225c3c3b86391e6e34a96503fa4a1b8a3d9"
MAP_SHA = "76b3a8c4b2fbb62a02ec44ed6e4c0d2fb022ae2bf71835d482933c0479377dfe"
SIX = {"gele": "Gele oesterzwam", "roze": "Roze oesterzwam", "witte": "Witte oesterzwam",
       "blauwe": "Blauwe oesterzwam", "italiaanse": "Italiaanse oesterzwam", "grijze": "Grijze oesterzwam"}
SCENES = ["opening", "levering", "assortiment", "kweek", "tafels", "kweker", "proefbox"]  # R11


def sha(text):
    return hashlib.sha256(text.encode()).hexdigest()


class Generators(unittest.TestCase):
    def test_ring_is_the_approved_network(self):  # AD13, R10
        self.assertEqual(sha(hyphae.ring_svg(frozenset(SIX))), RING_SHA)

    def test_ring_without_a_variety_drops_its_main(self):  # R4, R17
        block = hyphae.ring_svg(frozenset(set(SIX) - {"grijze"}))
        self.assertNotIn('data-v="grijze"', block)
        self.assertEqual(len(re.findall(r'class="m" data-v=', block)), 2 * 5)

    def test_medallion_places_and_name_guard(self):  # R10: three per side
        meds = hyphae.medallions(SIX)
        self.assertEqual([m["key"] for m in meds], ["grijze", "witte", "roze", "gele", "blauwe", "italiaanse"])
        self.assertEqual(sum(float(m["x"][:-1]) < 50 for m in meds), 3)
        with self.assertRaises(ValueError):  # a renamed variety no longer fits its measured curved label
            hyphae.medallions({**SIX, "gele": "Citroengele oesterzwam"})
        with self.assertRaises(ValueError):
            hyphae.medallions({**SIX, "nieuw": "Nieuwe oesterzwam"})

    def test_map_is_the_approved_map(self):
        stops = ((625, 280, True), (569, 133, False), (850, 293, False), (561, 550, False), (403, 737, False), (144, 275, False))
        self.assertEqual(sha(levering.map_svg(stops)), MAP_SHA)
        self.assertEqual(levering.van_style(), "--vx:61.99%;--vy:28.70%")

    def test_route_check(self):
        self.assertEqual(levering.route_check([("Damme", 561, 550), ("Elders", 500, 500)]), ["Elders"])


class Homepage(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        shutil.copytree(b.DATA, self.tmp / "data")

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def edit(self, name, fn):
        path = self.tmp / "data" / f"{name}.json"
        value = json.loads(path.read_text(encoding="utf-8"))
        fn(value)
        path.write_text(json.dumps(value, ensure_ascii=False), encoding="utf-8")

    def render(self):
        b.build(base="/gromush-site/", out=self.tmp / "out", data_dir=self.tmp / "data")
        html = (self.tmp / "out/index.html").read_text(encoding="utf-8")
        return html[html.index("<main"):html.index("</main>")]

    def test_scenes_in_story_order(self):  # R11
        self.assertEqual(re.findall(r'data-scene="([a-z-]+)"', self.render()), SCENES)

    def test_medallions_link_by_plain_name_with_their_own_action(self):  # R10a, AC10b, AD10
        main = self.render()
        meds = re.findall(r'<a class="med-link" href="([^"]+)" data-variety="([a-z]+)">.*?<span class="sr-only">([^<]+)</span></a>\s*'
                          r'<a class="pill pill-link[^"]*" href="([^"]+)"', main, re.S)
        self.assertEqual(len(meds), 6)
        names = {v["key"]: v for v in json.loads((self.tmp / "data/varieties.json").read_text(encoding="utf-8"))}
        for href, key, label, pill in meds:
            self.assertEqual(label, names[key]["name"])
            self.assertEqual(href, f"/gromush-site/zwammen/{names[key]['slug']}/")
            self.assertEqual(pill, f"/gromush-site/proefbox/?soort={names[key]['slug']}#formulier")

    def test_variety_copy_from_data(self):  # R4, AC6
        self.edit("varieties", lambda vs: vs[0].update(taste_words=["Proefwoord", "twee", "drie"]))
        main = self.render()
        self.assertEqual(main.count("Proefwoord · twee · drie"), 2)  # the opening list and the flip card

    def test_out_of_range_variety_leaves_every_scene(self):  # R4, R17
        self.edit("varieties", lambda vs: [v.update(in_range=False) for v in vs if v["key"] == "grijze"])
        main = self.render()
        for needle in ('data-variety="grijze"', 'data-v="grijze"', 'data-card="grijze"', "Grijze oesterzwam", "grijze-oesterzwam"):
            self.assertNotIn(needle, main)

    def test_outdoor_note_is_a_plan(self):  # R23, AC22
        main = self.render()
        self.assertIn("gepland voor 2027", main)
        for word in ("januari", "voorjaar", "2028", "oogst verwacht"):
            self.assertNotIn(word, main)

    def test_grower_photo_is_the_approved_krat(self):  # R44: AI-styled, approved by Michael 2026-11-05
        self.assertIn("anthony-krat", self.render())

    def test_town_off_the_route_fails_the_build(self):
        self.edit("towns", lambda t: t["towns"][0]["map"].update(x=100, y=700))
        with self.assertRaisesRegex((b.BuildError, TemplateError), "not on the drawn delivery route"):
            self.render()


if __name__ == "__main__":
    unittest.main()
