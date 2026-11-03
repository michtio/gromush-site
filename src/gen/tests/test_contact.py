"""Unit tests for the /contact/ page (S6; PRD R9, R32, R33, R34, R42; plan AD7, AD10): the reason selector, the
home-cook pick-up mode and the contact details, rendered from forms.json, site.json and towns.json.
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

R32 = ["Chef / restaurant", "Grootkeuken", "Speciaalzaak", "Bestelling thuis (afhalen)", "Adoptie emmer",
       "Interesse buitenkweek", "School of vereniging", "Samenwerking", "Andere"]


class ContactPage(unittest.TestCase):
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
        return (self.out / "contact" / "index.html").read_text(encoding="utf-8")

    def test_reasons_match_r32(self):  # R32: the reasons, in order, after the empty default
        html = self.page()
        select = re.search(r'<select id="f-reden" name="reden" required[^>]*>(.*?)</select>', html, re.S).group(1)
        labels = re.findall(r'<option value="([^"]*)"[^>]*>([^<]*)</option>', select)
        self.assertEqual(labels[0][0], "")
        self.assertEqual([label for _, label in labels[1:]], R32)
        self.assertIn('<option value="grootkeuken">Grootkeuken</option>', select)  # AC31: ?reden=grootkeuken
        self.assertIn('<option value="bestelling-thuis" data-mode="afhalen">', select)

    def test_native_mailto_action(self):  # R33, AC28a
        form = re.search(r'<form [^>]*data-form="contact"[^>]*>', self.page()).group(0)
        self.assertIn('action="mailto:info@gromush.be?subject=Contactaanvraag"', form)
        self.assertIn('method="post"', form)
        self.assertIn('enctype="text/plain"', form)
        self.assertIn('data-mode-afhalen-mail="Anthony bevestigt', form)

    def test_pickup_mode_r42(self):  # R42, AC38: confirm, harvest days, payment; no address, schedule or price
        html = self.page()
        note = re.search(r'<div class="mode-note[^>]*>(.*?)</div>', html, re.S).group(1)
        for text in ("Anthony bevestigt je bestelling, het afhaalmoment en de plaats persoonlijk",
                     "oogstdagen wisselen", "overschrijving", "cash"):
            self.assertIn(text, note)
        handoff = re.search(r'<p class="form-handoff-mode"[^>]*>(.*?)</p>', html).group(1)
        self.assertIn("Anthony bevestigt", handoff)
        self.assertIn("persoonlijk", handoff)
        main = re.search(r"<main.*?</main>", html, re.S).group(0)
        self.assertNotIn("€", main)
        self.assertNotRegex(note + handoff, r"\b\d{4}\b|straat|laan|Westkapelle")

    def test_mode_fields_never_required_without_js(self):  # AD10: no-JS shows every field; order fields optional
        html = self.page()
        for name in ("soorten", "hoeveelheid"):
            block = re.search(rf'data-field="{name}"[^>]*data-mode-only="afhalen".*?(</fieldset>|</div>)', html, re.S)
            self.assertIsNotNone(block, name)
            self.assertNotIn(" required", block.group(0))
        self.assertIn('data-slug="blauwe-oesterzwam"', html)  # ?soort=<slug> from the product pages

    def test_details_card_r9(self):  # R9: email, phone as call link, WhatsApp, Westkapelle without street address
        html = self.page()
        self.assertIn('href="mailto:info@gromush.be"', html)
        self.assertIn('href="tel:+32499242359"', html)
        self.assertIn('href="https://wa.me/32499242359"', html)
        self.assertIn("Westkapelle (Knokke-Heist)", html)
        self.assertIn('href="/gromush-site/privacy/"', html)  # R34
        for slug in ("knokke-heist", "damme", "sluis", "brugge", "blankenberge"):
            self.assertIn(f'href="/gromush-site/leveringsregio/{slug}/"', html)

    def test_phone_flag_hides_phone(self):  # AC5 on the contact page
        self.edit("flags", lambda f: f.update(phone_published=False))
        html = self.page()
        self.assertNotIn('href="tel:', html)
        self.assertNotIn("wa.me", html)


if __name__ == "__main__":
    unittest.main()
