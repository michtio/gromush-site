"""Unit tests for picture(): rendered widths, srcset, width/height, alt, loading, missing files (S3, R37).
Run: python3 -I -m unittest discover -s src/gen/tests"""
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from gen import build as b  # noqa: E402
from gen import picture as pic  # noqa: E402
from gen.template import TemplateError, wrap  # noqa: E402

SITE = wrap({"origin": "https://michtio.github.io", "strings": {}})


def url(path):
    return "/gromush-site" + path


class Widths(unittest.TestCase):
    def test_standard_widths_never_upscaled(self):
        self.assertEqual(pic.widths_for(800), [400, 800])
        self.assertEqual(pic.widths_for(1600), [400, 800, 1200, 1600])
        self.assertEqual(pic.widths_for(2400), [400, 800, 1200, 1600])
        self.assertEqual(pic.widths_for(264), [264])

    def test_source_width_added_when_clearly_larger(self):
        self.assertEqual(pic.widths_for(1189), [400, 800, 1189])
        self.assertEqual(pic.widths_for(1280), [400, 800, 1200])  # within 15 % of 1200


class FallbackWidths(unittest.TestCase):
    def test_smallest_and_largest_up_to_800(self):
        self.assertEqual(pic.fallback_widths([400, 800, 1200, 1600]), [400, 800])
        self.assertEqual(pic.fallback_widths([400, 800, 1189]), [400, 800])
        self.assertEqual(pic.fallback_widths([400, 800]), [400, 800])
        self.assertEqual(pic.fallback_widths([400, 700]), [400, 700])
        self.assertEqual(pic.fallback_widths([264]), [264])


class ExpectedFiles(unittest.TestCase):
    def test_images_py_expects_capped_fallbacks(self):
        sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "tools"))
        import images  # tools/images.py
        names = images.expected_names([{"id": "foto", "width": 1600}])
        self.assertIn("foto-1600.avif", names)
        self.assertIn("foto-1200.webp", names)
        self.assertIn("foto-800.jpg", names)
        self.assertIn("foto-400.png", names)
        self.assertNotIn("foto-1200.jpg", names)
        self.assertNotIn("foto-1600.png", names)


class Render(unittest.TestCase):
    def setUp(self):
        self.static = Path(tempfile.mkdtemp())
        self.r = self.static / pic.RENDER_DIR
        self.r.mkdir(parents=True)
        for w in (400, 800, 1200):
            for ext in ("avif", "webp") + (("jpg",) if w <= 800 else ()):
                (self.r / f"foto-{w}.{ext}").write_bytes(b"x")
        for ext in ("avif", "webp", "png"):
            (self.r / f"knip-400.{ext}").write_bytes(b"x")
        self.images = wrap([
            {"id": "foto", "width": 1280, "height": 960, "alt": "Geroosterde oesterzwam"},
            {"id": "knip", "width": 400, "height": 266, "alt": ""},
            {"id": "zonder-alt", "width": 400, "height": 300, "alt": None},
            {"id": "niet-gerenderd", "width": 800, "height": 600, "alt": "x"},
        ])
        self.by = {i.id: i for i in self.images}

    def tearDown(self):
        shutil.rmtree(self.static)

    def render(self, image_id, **kw):
        return pic.render(self.by[image_id], url=url, static_dir=self.static, **kw)

    def test_sources_srcset_widths_and_fallback(self):
        out = self.render("foto", sizes="50vw", cls="foto")
        self.assertTrue(out.startswith("<picture>") and out.endswith("</picture>"))
        for ext, mime in (("avif", "image/avif"), ("webp", "image/webp")):
            self.assertIn(f'<source type="{mime}" srcset="/gromush-site/img/r/foto-400.{ext} 400w, '
                          f'/gromush-site/img/r/foto-800.{ext} 800w, /gromush-site/img/r/foto-1200.{ext} 1200w" '
                          f'sizes="50vw">', out)
        self.assertIn('class="foto" src="/gromush-site/img/r/foto-800.jpg"', out)
        # the jpeg fallback stops at 800 px (fallback_widths); avif and webp keep every width
        self.assertIn('srcset="/gromush-site/img/r/foto-400.jpg 400w, /gromush-site/img/r/foto-800.jpg 800w"', out)
        self.assertNotIn("foto-1200.jpg", out)

    def test_width_height_from_largest_rendering(self):
        self.assertIn('width="1200" height="900"', self.render("foto"))

    def test_alt_lazy_and_decoding(self):
        out = self.render("foto")
        self.assertIn('alt="Geroosterde oesterzwam"', out)
        self.assertIn('loading="lazy" decoding="async"', out)
        self.assertNotIn("fetchpriority", out)
        self.assertIn('sizes="100vw"', out)  # default when there are several widths

    def test_eager_flag_and_override(self):
        self.by["foto"]["eager"] = True
        out = self.render("foto")
        self.assertIn('loading="eager"', out)
        self.assertIn('fetchpriority="high"', out)
        self.assertIn('loading="lazy"', self.render("foto", loading="lazy"))

    def test_png_fallback_for_transparency(self):
        out = self.render("knip")
        self.assertIn('src="/gromush-site/img/r/knip-400.png"', out)
        self.assertIn('sizes="400px"', out)  # one width: sizes is that width
        self.assertIn('alt=""', out)

    def test_alt_required(self):
        with self.assertRaisesRegex(pic.PictureError, "no alt text"):
            self.render("zonder-alt")

    def test_decorative_overrides_alt(self):
        self.by["zonder-alt"]["id"] = "knip"
        self.by["zonder-alt"]["width"], self.by["zonder-alt"]["height"] = 400, 266
        self.assertIn('alt=""', self.render("zonder-alt", decorative=True))

    def test_missing_rendering_fails(self):
        with self.assertRaisesRegex(pic.PictureError, "tools/images.py"):
            self.render("niet-gerenderd")

    def test_missing_image_fails_the_build(self):
        tmp = Path(tempfile.mkdtemp())
        try:
            (tmp / "templates" / "pages").mkdir(parents=True)
            (tmp / "templates" / "pages" / "index.html").write_text('{{ picture("bestaat-niet") }}')
            with self.assertRaises((KeyError, TemplateError)):
                b.build(base="/", out=tmp / "docs", templates=tmp / "templates", static=self.static)
            (tmp / "templates" / "pages" / "index.html").write_text('{{ picture("dish-curry") }}')
            with self.assertRaisesRegex(TemplateError, "not rendered yet"):
                b.build(base="/", out=tmp / "docs2", templates=tmp / "templates", static=self.static)
        finally:
            shutil.rmtree(tmp)

    def test_real_register_is_rendered(self):
        """Every image in images.json has its files in src/static (run tools/images.py if this fails)."""
        data = b.load_data()
        h = b.make_helpers(data.site, "/", data.images.images)
        for img in data.images.images:
            out = h["picture"](img.id, decorative=img.alt is None)
            self.assertIn('<source type="image/avif"', out, img.id)
            self.assertIn('<source type="image/webp"', out, img.id)


if __name__ == "__main__":
    unittest.main()
