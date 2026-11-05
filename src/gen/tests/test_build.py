"""Unit tests for the generator: base-path helpers, data rules, flags, routes, a full build.
Run: python3 -I -m unittest discover -s src/gen/tests"""
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from gen import build as b  # noqa: E402
from gen.template import wrap  # noqa: E402

SITE = wrap({"origin": "https://michtio.github.io", "strings": {"skip_link": "Ga naar inhoud"}})
IMAGES = wrap([
    {"id": "logo", "source": "src/static/img/logo-gromush.png", "width": 264, "height": 132, "alt": "GroMush"},
    {"id": "nog-geen-alt", "source": "src/static/img/x.png", "width": 1, "height": 1, "alt": None},
    {"id": "pijplijn", "source": ".impeccable/x.webp", "width": 1, "height": 1, "alt": "x"},
])


class Urls(unittest.TestCase):
    def test_url_under_subpath(self):
        h = b.make_helpers(SITE, "/gromush-site/", IMAGES)
        self.assertEqual(h["url"]("/"), "/gromush-site/")
        self.assertEqual(h["url"]("/zwammen/gele-oesterzwam/"), "/gromush-site/zwammen/gele-oesterzwam/")
        self.assertEqual(h["url"]("/proefbox/?soort=blauwe#formulier"), "/gromush-site/proefbox/?soort=blauwe#formulier")

    def test_url_at_domain_root(self):
        h = b.make_helpers(SITE, "/", IMAGES)
        self.assertEqual(h["url"]("/"), "/")
        self.assertEqual(h["url"]("/zwammen/"), "/zwammen/")

    def test_base_is_normalized(self):
        for given in ("gromush-site", "/gromush-site", "gromush-site/", "/gromush-site/"):
            self.assertEqual(b.normalize_base(given), "/gromush-site/")
        self.assertEqual(b.normalize_base("/"), "/")

    def test_url_rejects_relative_and_protocol_relative(self):
        h = b.make_helpers(SITE, "/", IMAGES)
        for bad in ("zwammen/", "//cdn.example/x", "https://x.be/"):
            with self.assertRaises(ValueError):
                h["url"](bad)

    def test_abs_url_both_bases(self):
        self.assertEqual(b.make_helpers(SITE, "/gromush-site/", IMAGES)["abs_url"]("/zwammen/"),
                         "https://michtio.github.io/gromush-site/zwammen/")
        self.assertEqual(b.make_helpers(SITE, "/", IMAGES)["abs_url"]("/zwammen/"), "https://michtio.github.io/zwammen/")

    def test_t_and_missing_string(self):
        h = b.make_helpers(SITE, "/", IMAGES)
        self.assertEqual(h["t"]("skip_link"), "Ga naar inhoud")
        with self.assertRaises(KeyError):
            h["t"]("bestaat-niet")

    def test_picture_uses_rendered_files(self):  # S3: real picture(), the details are in test_picture.py
        h = b.make_helpers(SITE, "/gromush-site/", IMAGES)
        out = h["picture"]("logo")
        self.assertTrue(out.startswith("<picture>"))
        self.assertIn('src="/gromush-site/img/r/logo-264.png"', out)
        self.assertIn('alt="GroMush"', out)
        self.assertIn('width="264" height="132"', out)
        with self.assertRaises(ValueError):
            h["picture"]("nog-geen-alt")
        with self.assertRaises(ValueError):
            h["picture"]("pijplijn")  # not rendered
        with self.assertRaises(KeyError):
            h["picture"]("bestaat-niet")


class DataRules(unittest.TestCase):
    def test_real_data_loads_and_validates(self):
        data = b.load_data()
        self.assertEqual(data.site.name, "GroMush")
        self.assertEqual(len(data.varieties), 6)

    def test_in_range_filters_and_orders(self):
        vs = wrap([{"slug": "b", "in_range": True, "nav_order": 2}, {"slug": "grijze", "in_range": False, "nav_order": 1},
                   {"slug": "a", "in_range": True, "nav_order": 1}])
        self.assertEqual([v.slug for v in b.in_range(vs)], ["a", "b"])

    def test_brand_hits(self):
        self.assertEqual(b.brand_hits("GroMush, info@gromush.be, instagram.com/gromush.be"), [])
        self.assertEqual(b.brand_hits("Gromush GRO MUSH GroMUSH GROmush"), ["Gromush", "GRO MUSH", "GroMUSH", "GROmush"])


class FullBuild(unittest.TestCase):
    """Builds into a temp dir from a temp copy of the data, so the real data and docs/ stay untouched."""

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

    def run_build(self, base="/gromush-site/"):
        b.build(base=base, out=self.out, data_dir=self.data)
        return (self.out / "index.html").read_text(encoding="utf-8")

    def test_writes_shell_files(self):
        html = self.run_build()
        for rel in (".nojekyll", "404.html", "index.html", "css/site.css", "img/logo-gromush.png"):
            self.assertTrue((self.out / rel).is_file(), rel)
        self.assertIn('class="skip" href="#inhoud"', html)
        self.assertIn('<html lang="nl-BE">', html)

    def test_no_off_base_links_at_either_base(self):
        sub = self.run_build("/gromush-site/")
        self.assertIn('href="/gromush-site/css/site.css"', sub)
        self.assertNotIn('href="/css', sub)
        root = self.run_build("/")
        self.assertNotIn("/gromush-site/", root)
        self.assertIn('href="/css/site.css"', root)
        self.assertIn('<link rel="canonical" href="https://michtio.github.io/">', root)

    def test_taste_words_change_once_shows_on_page(self):  # AC6 at S1 scope
        self.edit("varieties", lambda vs: vs[0].update(taste_words=["Proefwoord", "twee", "drie"]))
        self.assertIn("Proefwoord · twee · drie", self.run_build())

    def test_out_of_range_variety_disappears(self):  # R17 at S1 scope
        self.edit("varieties", lambda vs: [v.update(in_range=False) for v in vs if v["key"] == "grijze"])
        self.assertNotIn("Grijze oesterzwam", self.run_build())

    def test_phone_flag(self):  # AC5
        self.assertIn('href="tel:', self.run_build())
        self.edit("flags", lambda f: f.update(phone_published=False))
        html = self.run_build()
        self.assertNotIn("tel:", html)
        self.assertNotIn("wa.me", html)

    def test_nav_from_data(self):  # S4: R5, R6, AD19
        html = self.run_build()
        header = html.split('<header class="site-header"', 1)[1].split("</header>", 1)[0]
        for label in ("Zwammen", "Voor wie", "Ons verhaal", "Inspiratie", "Contact", "Alle zwammen",
                      "Thuis &amp; MushLove", "Over Anthony", "Leveringsregio", "Italiaanse oesterzwam"):
            self.assertIn(f">{label}</a>", header)
        self.assertIn('<a class="btn-cta" href="/gromush-site/proefbox/">Gratis ProefBox</a>', header)
        self.assertEqual(header.count('class="nav-item'), 5)
        self.assertEqual(header.count('class="sub-toggle"'), 3)
        self.assertIn('href="/gromush-site/zwammen/grijze-oesterzwam/"', header)
        self.edit("varieties", lambda vs: [v.update(in_range=False) for v in vs if v["key"] == "grijze"])
        self.assertNotIn("grijze-oesterzwam", self.run_build())  # header and footer follow the range (R17)

    def test_nav_rules(self):  # R5, R6
        self.edit("nav", lambda n: n["main"].extend([{"label": f"X{i}", "path": "/x/"} for i in range(2)]))
        with self.assertRaisesRegex(b.BuildError, "R6"):
            self.run_build()
        shutil.copy(b.DATA / "nav.json", self.data / "nav.json")
        self.edit("nav", lambda n: n["cta"].update(label="Gratis ChefBox"))
        with self.assertRaisesRegex(b.BuildError, "R5"):
            self.run_build()

    def test_footer_r9(self):  # R9 from site.json, towns.json and nav.json
        html = self.run_build()
        footer = html.split('<footer class="footer">', 1)[1].split("</footer>", 1)[0]
        for needle in ('href="mailto:info@gromush.be"', 'href="tel:+32499242359"', 'href="https://wa.me/32499242359"',
                       "Westkapelle", 'href="https://www.instagram.com/gromush.be/"',
                       'href="https://www.facebook.com/profile.php?id=61590322125848"',
                       'href="/gromush-site/privacy/"', 'href="/gromush-site/cookies/"', 'href="/gromush-site/voorwaarden/"',
                       'href="/gromush-site/leveringsregio/blankenberge/"', 'href="/gromush-site/ons-verhaal/adopteer/"'):
            self.assertIn(needle, footer)
        self.assertNotIn("61594707453474", footer)  # the MushLove page belongs on Thuis (S14), not the footer

    def test_promo_never_on_proefbox_or_contact(self):  # R35 template condition (AD15)
        tpl = self.tmp / "templates"
        shutil.copytree(b.TEMPLATES, tpl)
        page = ('{% extends "layouts/base.html" %}{% block title %}{{ page.path }} · GroMush{% endblock %}'
                '{% block description %}Testpagina {{ page.path }}.{% endblock %}{% block main %}<p>x</p>{% endblock %}')
        for slug in ("proefbox", "contact", "inspiratie"):
            (tpl / "pages" / slug).mkdir()
            (tpl / "pages" / slug / "index.html").write_text(page)
        b.build(base="/gromush-site/", out=self.out, data_dir=self.data, templates=tpl)
        read = lambda rel: (self.out / rel).read_text(encoding="utf-8")
        self.assertIn('<dialog class="promo" id="promo"', read("index.html"))
        self.assertIn('<dialog class="promo" id="promo"', read("inspiratie/index.html"))
        self.assertIn('data-never-on="/gromush-site/proefbox/ /gromush-site/voor-wie/thuis/ /gromush-site/contact/ /gromush-site/voor-wie/grootkeukens/ /gromush-site/voor-wie/speciaalzaken/ /gromush-site/privacy/ /gromush-site/cookies/ /gromush-site/voorwaarden/"', read("index.html"))
        for rel in ("proefbox/index.html", "contact/index.html"):
            self.assertNotIn('id="promo"', read(rel), rel)
            self.assertIn("/js/site.js", read(rel))
        self.assertNotRegex(read("index.html").split('id="promo"', 1)[1].split("</dialog>", 1)[0], "(?i)chef ?box")

    def test_flags_must_be_booleans(self):
        self.edit("flags", lambda f: f.update(startup_phase="ja"))
        with self.assertRaisesRegex(b.BuildError, "startup_phase"):
            self.run_build()

    def test_wrong_brand_spelling_in_data_fails(self):  # R1
        self.edit("site", lambda s: s.update(baseline="Gromush kweekt."))
        with self.assertRaisesRegex(b.BuildError, "R1"):
            self.run_build()

    def test_three_taste_words_required(self):  # R4
        self.edit("varieties", lambda vs: vs[0].update(taste_words=["een", "twee"]))
        with self.assertRaisesRegex(b.BuildError, "three taste words"):
            self.run_build()

    def test_refuses_foreign_out_dir(self):
        self.out.mkdir()
        (self.out / "iets.html").write_text("niet van ons")
        with self.assertRaisesRegex(b.BuildError, "refusing"):
            self.run_build()

    def test_routes_follow_url_scheme(self):
        paths = {path for _, _, path in b.routes()}
        self.assertIn("/", paths)
        self.assertIn("/404.html", paths)
        self.assertIn("/_dev/componenten/", paths)
        for p in paths - {"/404.html"}:
            if p.startswith(b.DEV_PREFIX):  # only the explicit /_dev/ segment may break the slug rule
                p = "/" + p[len(b.DEV_PREFIX):]
            self.assertRegex(p, b.PAGE_PATH)

    def test_underscore_only_allowed_as_dev_prefix(self):
        tmp = Path(tempfile.mkdtemp())
        try:
            (tmp / "pages" / "_geheim").mkdir(parents=True)
            (tmp / "pages" / "_geheim" / "index.html").write_text("x")
            with self.assertRaisesRegex(b.BuildError, "URL scheme"):
                b.routes(tmp)
            shutil.rmtree(tmp / "pages" / "_geheim")
            (tmp / "pages" / "_dev" / "Fout").mkdir(parents=True)
            (tmp / "pages" / "_dev" / "Fout" / "index.html").write_text("x")
            with self.assertRaisesRegex(b.BuildError, "URL scheme"):
                b.routes(tmp)
        finally:
            shutil.rmtree(tmp)

    def test_dev_page_is_noindex(self):
        b.build(base="/gromush-site/", out=self.out, data_dir=self.data)
        html = (self.out / "_dev" / "componenten" / "index.html").read_text(encoding="utf-8")
        self.assertIn('<meta name="robots" content="noindex', html)


if __name__ == "__main__":
    unittest.main()
