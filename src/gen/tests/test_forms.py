"""Unit tests for the form engine (S5; PRD R31, R33, R34; plan AD7, AD10): the mailto() helper and the
/proefbox/ page rendered from forms.json. Run: python3 -I -m unittest discover -s src/gen/tests"""
import json
import re
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from gen import build as b  # noqa: E402
from gen.template import wrap  # noqa: E402


class Mailto(unittest.TestCase):
    def test_subject_is_percent_encoded(self):  # RFC 6068: spaces %20, & %26, non-ASCII as UTF-8
        h = b.make_helpers(wrap({"origin": "https://x.be", "form_recipient": "info@gromush.be", "strings": {}}), "/", [])
        self.assertEqual(h["mailto"]("ProefBox-aanvraag"), "mailto:info@gromush.be?subject=ProefBox-aanvraag")
        self.assertEqual(h["mailto"]("Café & co"), "mailto:info@gromush.be?subject=Caf%C3%A9%20%26%20co")


class ProefBoxPage(unittest.TestCase):
    """Builds from a temp copy of the data into a temp dir; the real data and docs/ stay untouched."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.data = self.tmp / "data"
        shutil.copytree(b.DATA, self.data)
        self.out = self.tmp / "docs"

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def edit(self, name, fn):
        path = self.data / f"{name}.json"
        value = json.loads(path.read_text(encoding="utf-8"))
        fn(value)
        path.write_text(json.dumps(value, ensure_ascii=False), encoding="utf-8")

    def page(self):
        b.build(base="/gromush-site/", out=self.out, data_dir=self.data)
        return (self.out / "proefbox" / "index.html").read_text(encoding="utf-8")

    def test_native_mailto_action(self):  # AC28a
        form = re.search(r"<form [^>]*>", self.page()).group(0)
        self.assertIn('action="mailto:info@gromush.be?subject=ProefBox-aanvraag"', form)
        self.assertIn('method="post"', form)
        self.assertIn('enctype="text/plain"', form)

    def test_r31_fields(self):  # R31: name, business, type, email, town, optional phone, varieties, message
        html = self.page()
        for name in ("naam", "zaak", "type", "email", "gemeente", "bericht"):
            self.assertIn(f'name="{name}"', html)
        self.assertRegex(html, r'<input id="f-tel" name="tel" type="tel"(?![^>]*required)[^>]*>')
        self.assertIn('<fieldset class="soorten', html)
        self.assertIn("<legend>Welke soorten wil je proeven?</legend>", html)
        self.assertIn("gratis", html)
        self.assertIn("professionele klanten in onze leveringsregio", html)

    def test_options_from_data(self):  # towns and in-range varieties come from data (R17, AD2)
        self.edit("varieties", lambda vs: [v.update(in_range=False) for v in vs if v["key"] == "grijze"])
        html = self.page()
        self.assertNotIn("Grijze oesterzwam", html)
        self.assertIn('data-key="blauwe"', html)
        for town in ("Knokke-Heist", "Damme", "Sluis", "Brugge", "Blankenberge"):
            self.assertIn(f'<option value="{town}">', html)

    def test_privacy_line_and_no_claims(self):  # R34, AC29, AC32
        html = self.page()
        self.assertIn('href="/gromush-site/privacy/"', html)
        self.assertNotRegex(html.lower(), r"is ontvangen|is verstuurd|captcha")
        self.assertIn('href="mailto:info@gromush.be"', html)

    def test_phone_flag_hides_phone(self):  # AC5 on the form page
        self.edit("flags", lambda f: f.update(phone_published=False))
        html = self.page()
        self.assertNotIn('href="tel:', html)
        self.assertNotIn("wa.me", html)


if __name__ == "__main__":
    unittest.main()
