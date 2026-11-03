"""Unit tests for S8: page metadata, Open Graph, JSON-LD (AD18), sitemap, robots, forward pages (AD17).
Run: python3 -I -m unittest discover -s src/gen/tests"""
import json
import re
import shutil
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from gen import build as b  # noqa: E402
from gen import seo  # noqa: E402
from gen.template import wrap  # noqa: E402

ORIGIN = "https://michtio.github.io/gromush-site"
abs_url = lambda path: ORIGIN + path  # noqa: E731


def head(title="Over · GroMush", desc="Een pagina.", extra=""):
    return (f'<html><head><title>{title}</title>\n<meta name="description" content="{desc}">\n{extra}'
            f'<link rel="canonical" href="{ORIGIN}/x/">\n</head><body></body></html>')


class PageMeta(unittest.TestCase):
    def test_reads_and_unescapes(self):
        meta = seo.page_meta(head("Zwammen &amp; meer · GroMush", "Proef &quot;vers&quot;."))
        self.assertEqual(meta["title"], "Zwammen & meer · GroMush")
        self.assertEqual(meta["description"], 'Proef "vers".')
        self.assertEqual(meta["canonical"], ORIGIN + "/x/")
        self.assertFalse(meta["noindex"])
        self.assertTrue(seo.page_meta(head(extra='<meta name="robots" content="noindex, nofollow">'))["noindex"])

    def test_indexable(self):
        meta = {"noindex": False}
        self.assertTrue(seo.is_indexable("/zwammen/", meta))
        self.assertFalse(seo.is_indexable("/404.html", meta))
        self.assertFalse(seo.is_indexable("/_dev/componenten/", meta))
        self.assertFalse(seo.is_indexable("/zwammen/", {"noindex": True}))

    def test_check_pages(self):
        ok = {"title": "A · GroMush", "description": "a", "noindex": False}
        self.assertEqual(seo.check_pages([("a", "/a/", ok), ("b", "/b/", {**ok, "title": "B · GroMush", "description": "b"})]), [])
        problems = "\n".join(seo.check_pages([
            ("a", "/a/", ok),
            ("dubbel", "/b/", {**ok, "description": "anders"}),
            ("leeg", "/c/", {**ok, "title": "", "description": ""}),
            ("merkloos", "/d/", {**ok, "title": "Zonder merk", "description": "d"}),
            ("404", "/404.html", {**ok, "title": "Weg · GroMush", "description": "weg"}),
        ]))
        self.assertIn("dubbel: same title as a", problems)
        self.assertIn("leeg: no title", problems)
        self.assertIn("leeg: no description", problems)
        self.assertIn("merkloos: the title must name GroMush (R1)", problems)
        self.assertIn("/404.html must be noindex", problems)


class OpenGraph(unittest.TestCase):
    SITE = wrap({"name": "GroMush", "lang": "nl-BE"})

    def test_adds_tags_from_title_description_canonical(self):
        page = head("Zwammen &amp; meer · GroMush")
        out = seo.add_open_graph(page, seo.page_meta(page), self.SITE, '<meta property="og:image" content="x">\n')
        self.assertIn('<meta property="og:title" content="Zwammen &amp; meer · GroMush">', out)
        self.assertIn('<meta property="og:url" content="%s/x/">' % ORIGIN, out)
        self.assertIn('<meta property="og:locale" content="nl_BE">', out)
        self.assertIn('<meta property="og:type" content="website">', out)
        self.assertEqual(out.count('property="og:image"'), 1)
        self.assertLess(out.index("og:title"), out.index("</head>"))

    def test_page_own_og_image_wins(self):
        page = head(extra='<meta property="og:image" content="eigen">\n')
        out = seo.add_open_graph(page, seo.page_meta(page), self.SITE, '<meta property="og:image" content="standaard">\n')
        self.assertNotIn("standaard", out)
        self.assertEqual(out.count('property="og:image"'), 1)

    def test_og_image_tags_from_register(self):
        img = wrap({"id": "dish-geroosterd", "width": 1280, "height": 960, "alt": "Geroosterde oesterzwam"})
        tags = seo.og_image_tags(img, abs_url, b.STATIC)
        self.assertIn(f'content="{ORIGIN}/img/r/dish-geroosterd-800.jpg"', tags)
        self.assertIn('og:image:width" content="800"', tags)
        self.assertIn('og:image:height" content="600"', tags)
        self.assertIn('og:image:alt" content="Geroosterde oesterzwam"', tags)
        with self.assertRaises(seo.SeoError):
            seo.og_image_tags(wrap({**img, "alt": None}), abs_url, b.STATIC)


class JsonLd(unittest.TestCase):
    def setUp(self):
        self.data = b.load_data()
        self.helpers = b.seo_helpers(self.data, abs_url, b.STATIC)

    @staticmethod
    def objects(markup):
        return [json.loads(m) for m in re.findall(r'<script type="application/ld\+json">\n(.*?)\n</script>', markup, re.S)]

    def test_organization_everywhere_local_business_only_home(self):
        home = self.objects(self.helpers["jsonld_site"]("/"))
        other = self.objects(self.helpers["jsonld_site"]("/zwammen/"))
        self.assertEqual([o["@type"] for o in home], ["Organization", "LocalBusiness"])
        self.assertEqual([o["@type"] for o in other], ["Organization"])
        biz = home[1]
        self.assertEqual(biz["address"], {"@type": "PostalAddress", "addressLocality": self.data.site.locality,
                                          "addressCountry": "BE"})
        self.assertEqual(seo.find_forbidden(home), [])

    def test_phone_only_when_published(self):
        self.assertIn("telephone", self.objects(self.helpers["jsonld_site"]("/"))[0])
        self.data.flags["phone_published"] = False
        helpers = b.seo_helpers(self.data, abs_url, b.STATIC)
        for obj in self.objects(helpers["jsonld_site"]("/")):
            self.assertNotIn("telephone", obj)

    def test_product_without_offers(self):
        v = self.data.varieties[0]
        (obj,) = self.objects(self.helpers["jsonld_product"](v))
        self.assertEqual(obj["@type"], "Product")
        self.assertEqual(obj["name"], v.name)
        self.assertEqual(obj["url"], f"{ORIGIN}/zwammen/{v.slug}/")
        self.assertEqual(seo.find_forbidden(obj), [])

    def test_recipe_only_known_fields(self):
        r = wrap({"id": "x", "title": "Test", "servings": "2 personen", "image": "dish-curry",
                  "ingredients": ["oesterzwammen"], "steps": ["Bak ze."]})
        (obj,) = self.objects(self.helpers["jsonld_recipe"](r))
        self.assertEqual(obj["recipeIngredient"], ["oesterzwammen"])
        self.assertEqual(obj["recipeInstructions"], [{"@type": "HowToStep", "text": "Bak ze."}])
        (bare,) = self.objects(self.helpers["jsonld_recipe"](wrap({"title": "Kaal", "ingredients": [], "steps": []})))
        self.assertNotIn("recipeIngredient", bare)
        self.assertNotIn("image", bare)

    def test_forbidden_keys_refused(self):
        self.assertEqual(seo.find_forbidden({"a": [{"offers": {"price": 1}}], "address": {"streetAddress": "x"}}),
                         ["offers", "price", "streetAddress"])
        with self.assertRaises(seo.SeoError):
            seo._script({"@type": "Product", "offers": {}})

    def test_script_cannot_close_early(self):
        self.assertNotIn("</b>", seo._script({"name": "a</b>"}))


class SitemapRobots(unittest.TestCase):
    def test_sitemap_xml(self):
        xml = seo.sitemap_xml([ORIGIN + "/", ORIGIN + "/a/?x=1&y=2"])
        root = ET.fromstring(xml.encode("utf-8"))
        self.assertEqual(root.tag, "{http://www.sitemaps.org/schemas/sitemap/0.9}urlset")
        self.assertEqual([e.text for e in root.iter("{http://www.sitemaps.org/schemas/sitemap/0.9}loc")],
                         [ORIGIN + "/", ORIGIN + "/a/?x=1&y=2"])
        self.assertIn("&amp;", xml)

    def test_robots(self):
        self.assertEqual(seo.robots_txt(ORIGIN + "/sitemap.xml"),
                         f"User-agent: *\nAllow: /\n\nSitemap: {ORIGIN}/sitemap.xml\n")


class SeoBuild(unittest.TestCase):
    """Full builds into a temp dir from temp copies of the data and templates."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.data = self.tmp / "data"
        self.tpl = self.tmp / "templates"
        shutil.copytree(b.DATA, self.data)
        shutil.copytree(b.TEMPLATES, self.tpl)
        self.out = self.tmp / "docs"

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def build(self, base="/gromush-site/"):
        b.build(base=base, out=self.out, data_dir=self.data, templates=self.tpl)

    def read(self, rel):
        return (self.out / rel).read_text(encoding="utf-8")

    def remove_grijze(self):
        path = self.data / "varieties.json"
        vs = json.loads(path.read_text(encoding="utf-8"))
        for v in vs:
            if v["key"] == "grijze":
                v["in_range"] = False
        path.write_text(json.dumps(vs, ensure_ascii=False), encoding="utf-8")

    def add_page(self, slug, title, desc):
        (self.tpl / "pages" / slug).mkdir(parents=True, exist_ok=True)
        (self.tpl / "pages" / slug / "index.html").write_text(
            '{% extends "layouts/base.html" %}' f"{{% block title %}}{title}{{% endblock %}}"
            f"{{% block description %}}{desc}{{% endblock %}}{{% block main %}}<p>x</p>{{% endblock %}}", encoding="utf-8")

    def sitemap(self):
        root = ET.fromstring(self.read("sitemap.xml").encode("utf-8"))
        return [e.text for e in root.iter("{http://www.sitemaps.org/schemas/sitemap/0.9}loc")]

    def test_sitemap_lists_indexable_pages_only(self):
        self.build()
        locs = self.sitemap()
        self.assertIn(ORIGIN + "/", locs)
        self.assertFalse([u for u in locs if "_dev" in u or "404" in u])
        self.assertEqual(locs, sorted(locs))
        self.assertIn(f"Sitemap: {ORIGIN}/sitemap.xml", self.read("robots.txt"))

    def test_domain_root_base(self):
        self.build("/")
        self.assertIn("<loc>https://michtio.github.io/</loc>", self.read("sitemap.xml"))
        self.assertIn("Sitemap: https://michtio.github.io/sitemap.xml", self.read("robots.txt"))
        self.assertIn('<meta property="og:url" content="https://michtio.github.io/">', self.read("index.html"))

    def test_open_graph_on_indexable_not_on_noindex(self):
        self.build()
        self.assertIn('property="og:title"', self.read("index.html"))
        self.assertNotIn('property="og:', self.read("404.html"))
        self.assertNotIn('rel="canonical"', self.read("404.html"))
        self.assertNotIn('property="og:', self.read("_dev/componenten/index.html"))

    def test_forward_page_for_removed_variety(self):  # AC14, AC15, AD17
        self.remove_grijze()
        self.build()
        page = self.read("zwammen/grijze-oesterzwam/index.html")
        self.assertIn('<meta name="robots" content="noindex">', page)
        self.assertIn('<meta http-equiv="refresh" content="0; url=/gromush-site/zwammen/">', page)
        self.assertIn(f'<link rel="canonical" href="{ORIGIN}/zwammen/">', page)
        self.assertIn('href="/gromush-site/zwammen/"', page)
        self.assertNotIn('property="og:', page)
        self.assertFalse([u for u in self.sitemap() if "grijze" in u])
        others = [p for p in self.out.rglob("*.html") if "grijze-oesterzwam" not in p.as_posix()]
        self.assertFalse([p for p in others if "Grijze oesterzwam" in p.read_text(encoding="utf-8")])

    def test_no_forward_page_while_in_range(self):
        self.build()
        page = self.read("zwammen/grijze-oesterzwam/index.html")  # S11: the product page, not a forward page
        self.assertNotIn('http-equiv="refresh"', page)
        self.assertNotIn('content="noindex"', page)
        self.assertIn('"@type": "Product"', page)

    def test_forward_page_cannot_collide_with_a_template(self):
        self.remove_grijze()
        self.add_page("zwammen/grijze-oesterzwam", "Grijs · GroMush", "Grijs.")
        with self.assertRaisesRegex(b.BuildError, "out of the range"):
            self.build()

    def test_duplicate_title_fails_and_writes_nothing(self):
        self.add_page("een", "Zelfde · GroMush", "Eén.")
        self.add_page("twee", "Zelfde · GroMush", "Twee.")
        with self.assertRaisesRegex(b.BuildError, "same title"):
            self.build()
        self.assertFalse((self.out / "een").exists())

    def test_missing_description_fails(self):
        self.add_page("leeg", "Leeg · GroMush", "")
        with self.assertRaisesRegex(b.BuildError, "no description"):
            self.build()

    def test_title_without_brand_fails(self):  # R1
        self.add_page("merk", "Zonder merk", "Merk.")
        with self.assertRaisesRegex(b.BuildError, "R1"):
            self.build()


if __name__ == "__main__":
    unittest.main()
