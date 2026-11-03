"""Unit tests for tools/lint_content.py: the seeded fixtures, flags and the false-positive guards.

Run: python3 -I -m unittest discover -s tools/tests
"""
import io
import os
import sys
import unittest
from contextlib import redirect_stdout

TOOLS = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, TOOLS)
import lint_content  # noqa: E402

FIXTURES = os.path.join(TOOLS, "tests", "fixtures")
FLAGS_OFF = {"certified_organic": False, "startup_phase": True, "show_future_species": True, "phone_published": True}


def page(body, head=""):
    return f"<!DOCTYPE html><html><head><title>GroMush</title>{head}</head><body>{body}</body></html>"


class LintTestCase(unittest.TestCase):
    """Shared helpers: lint one document with the committed rules."""

    @classmethod
    def setUpClass(cls):
        cls.cfg, cls.rules, _ = lint_content.load_config(lint_content.DEFAULT_RULES, lint_content.DEFAULT_FLAGS)

    def hits(self, html, path="/", **flags):
        f = dict(FLAGS_OFF, **flags)
        return [h[1]["id"] for h in lint_content.lint_html(html, path, self.rules, f, self.cfg)]


class TestFixtures(LintTestCase):
    def test_fixture_folder_has_exactly_the_nine_seeded_hits(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            code = lint_content.main([FIXTURES, "--flags", os.path.join(TOOLS, "..", "src", "data", "flags.json")])
        lines = buf.getvalue().strip().splitlines()
        self.assertEqual(code, 1)
        self.assertEqual(lines[-1], "9 hits")
        ids = sorted(line.split("[")[1].split("]")[0] for line in lines[:-1])
        self.assertEqual(ids, sorted(["R1-brand", "R2-organic", "R2a-health", "R2a-medical", "R3-price",
                                      "R5-chefbox-free", "R21-speciaalzaken", "R23-ours", "R23-timing"]))

    def test_page_path(self):
        self.assertEqual(lint_content.page_path("docs", "docs/index.html"), "/")
        self.assertEqual(lint_content.page_path("docs", "docs/voor-wie/chefs/index.html"), "/voor-wie/chefs/")
        self.assertEqual(lint_content.page_path("docs", "docs/404.html"), "/404.html")


class TestR1Brand(LintTestCase):
    def test_variants_hit(self):
        for bad in ("Gromush", "GROMUSH", "GRO MUSH", "GroMUSH", "Gro-Mush", "gromush"):
            self.assertEqual(self.hits(page(f"<p>{bad} kweekt</p>")), ["R1-brand"], bad)

    def test_brand_domain_and_handle_pass(self):
        self.assertEqual(self.hits(page("<p>GroMush · info@gromush.be · gromush.be</p>")), [])

    def test_ignores_script_style_comments_and_other_attributes(self):
        html = page('<!-- Gromush --><script>var a="Gromush"</script><style>p{content:"Gromush"}</style>'
                    '<p class="Gromush" data-x="Gromush" id="Gromush"><a href="/Gromush/">GroMush</a></p>')
        self.assertEqual(self.hits(html), [])

    def test_reads_alt_title_aria_label_meta_and_title(self):
        for html in (page('<img alt="Gromush">'), page('<a title="Gromush">x</a>'), page('<a aria-label="Gromush">x</a>'),
                     page("", '<meta name="description" content="Gromush">'), page("", '<meta property="og:title" content="Gromush">'),
                     "<html><head><title>Gromush</title></head><body></body></html>"):
            self.assertEqual(self.hits(html), ["R1-brand"], html)

    def test_inline_elements_join(self):
        self.assertEqual(self.hits(page("<p><strong>Gro</strong>Mush</p>")), [])
        self.assertEqual(self.hits(page("<p><strong>Gro</strong>mush</p>")), ["R1-brand"])


class TestR2Organic(LintTestCase):
    def test_terms_hit_when_flag_off(self):
        for bad in ("biologisch", "biologische teelt", "bio", "bio-oesterzwam", "ecologisch", "gecertificeerd", "100% biologisch", "eco-teelt"):
            self.assertEqual(self.hits(page(f"<p>Onze {bad} zwammen.</p>")), ["R2-organic"], bad)

    def test_words_containing_bio_pass(self):
        self.assertEqual(self.hits(page("<p>De biografie, biodiversiteit en het ecosysteem.</p>")), [])

    def test_flag_on_allows_terms(self):
        self.assertEqual(self.hits(page("<p>Onze biologische zwammen.</p>"), certified_organic=True), [])


class TestR2aHealth(LintTestCase):
    def test_superfood_on_professional_pages(self):
        for path in ("/voor-wie/chefs/", "/voor-wie/grootkeukens/", "/voor-wie/speciaalzaken/", "/zwammen/gele-oesterzwam/", "/leveringsregio/brugge/", "/"):
            self.assertEqual(self.hits(page("<p>Een gezonde superfood.</p>"), path), ["R2a-health"], path)

    def test_health_allowed_on_consumer_pages(self):
        for path in ("/voor-wie/thuis/", "/inspiratie/", "/ons-verhaal/"):
            self.assertEqual(self.hits(page("<p>Een gezonde superfood.</p>"), path), [], path)

    def test_medical_claims_hit_everywhere(self):
        for path in ("/voor-wie/thuis/", "/inspiratie/", "/voor-wie/chefs/"):
            self.assertIn("R2a-medical", self.hits(page("<p>Oesterzwammen voorkomen kanker.</p>"), path), path)
        self.assertEqual(self.hits(page("<p>Een geneeskrachtige zwam.</p>"), "/inspiratie/"), ["R2a-medical"])

    def test_ordinary_verbs_pass(self):
        self.assertEqual(self.hits(page("<p>Behandel ze voorzichtig. Wij voorkomen dat de hoedjes breken.</p>"), "/inspiratie/"), [])


class TestR3Price(LintTestCase):
    def test_prices_hit(self):
        for bad in ("€ 12", "12 euro", "12 EUR", "12,-", "vanaf 5 kg", "-20%", "20% korting", "met korting", "prijs: 12"):
            self.assertEqual(self.hits(page(f"<p>Nu {bad}.</p>")), ["R3-price"], bad)

    def test_non_prices_pass(self):
        self.assertEqual(self.hits(page("<p>100% natuurlijk. Vanaf de kwekerij. Europese teelt.</p>")), [])

    def test_phone_links_only_when_phone_unpublished(self):
        html = page('<a href="tel:+32499242359">Bel</a><a href="https://wa.me/32499242359">WhatsApp</a>')
        self.assertEqual(self.hits(html), [])
        self.assertEqual(self.hits(html, phone_published=False), ["R3-phone", "R3-phone"])


class TestR5(LintTestCase):
    def test_chefbox_near_free_offer(self):
        self.assertEqual(self.hits(page("<p>Vraag je gratis ChefBox aan.</p>")), ["R5-chefbox-free"])
        self.assertEqual(self.hits(page("<p>Een Chef Box om te proeven.</p>")), ["R5-chefbox-free"])

    def test_chefbox_elsewhere_passes(self):
        self.assertEqual(self.hits(page("<p>De ChefBox is ons abonnement. Vraag een gratis ProefBox aan.</p>")), [])

    def test_link_to_proefbox_labelled_chefbox(self):
        self.assertEqual(self.hits(page('<a href="/gromush-site/proefbox/">ChefBox</a>')), ["R5-chefbox-link"])

    def test_proefbox_spelling(self):
        self.assertEqual(self.hits(page("<p>Gratis Proefbox</p>")), ["R5-name"])
        self.assertEqual(self.hits(page('<p><a href="/gromush-site/proefbox/">Gratis ProefBox</a></p>')), [])


class TestR21(LintTestCase):
    def test_gratis_in_main_hits_on_speciaalzaken_only(self):
        html = page("<main><p>Een gratis proeflevering.</p></main>")
        self.assertEqual(self.hits(html, "/voor-wie/speciaalzaken/"), ["R21-speciaalzaken"])
        self.assertEqual(self.hits(html, "/voor-wie/chefs/"), [])

    def test_header_cta_outside_main_passes(self):
        html = page('<header><a href="/gromush-site/proefbox/">Gratis ProefBox</a></header><main><p>Intake.</p></main>')
        self.assertEqual(self.hits(html, "/voor-wie/speciaalzaken/"), [])


class TestR23(LintTestCase):
    def test_allowed_plan_line_passes(self):
        self.assertEqual(self.hits(page("<main><h1>Buitenkweek op boomstammen, gepland voor 2027</h1></main>"), "/ons-verhaal/buitenkweek/"), [])
        self.assertEqual(self.hits(page("<p>Een voedselbos is een bos dat voedsel geeft.</p>")), [])

    def test_existing_forest_and_offers_hit(self):
        self.assertEqual(self.hits(page("<p>Welkom in ons voedselbos.</p>")), ["R23-ours"])
        self.assertEqual(self.hits(page("<p>Word mede-eigenaar.</p>")), ["R23-ours"])
        self.assertEqual(self.hits(page("<p>Adopteer een boomstam.</p>")), ["R23-offer"])
        self.assertEqual(self.hits(page("<p>Bezoek het voedselbos.</p>")), ["R23-offer"])

    def test_timing_near_outdoor_terms(self):
        self.assertEqual(self.hits(page("<p>De buitenkweek start in januari 2027.</p>")), ["R23-timing"])
        self.assertEqual(self.hits(page("<p>Buitenkweek: voorjaar 2027.</p>")), ["R23-timing"])
        self.assertEqual(self.hits(page("<p>Levering op maandag. Opgericht in 2025.</p>")), [])

    def test_any_timing_in_main_of_buitenkweek_page(self):
        self.assertEqual(self.hits(page("<main><p>Start in maart.</p></main>"), "/ons-verhaal/buitenkweek/"), ["R23-timing"])

    def test_bucket_adoption_passes(self):
        self.assertEqual(self.hits(page("<p>Adopteer een emmer en volg de groei.</p>")), [])


if __name__ == "__main__":
    unittest.main()
