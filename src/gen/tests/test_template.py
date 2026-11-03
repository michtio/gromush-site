"""Unit tests for the template engine. Run: python3 -I -m unittest discover -s src/gen/tests"""
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from gen.template import AttrDict, Environment, Markup, TemplateError, wrap  # noqa: E402


TMP = tempfile.TemporaryDirectory()


def tearDownModule():
    TMP.cleanup()


def env_with(files, globals=None):
    root = Path(tempfile.mkdtemp(dir=TMP.name))
    for name, text in files.items():
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    return Environment(root, globals or {})


def render(source, **ctx):
    return Environment(".", {}).from_string(source).render(ctx)


class Escaping(unittest.TestCase):
    def test_double_braces_escape(self):
        self.assertEqual(render("{{ x }}", x='<a href="y">&\'</a>'), "&lt;a href=&quot;y&quot;&gt;&amp;&#x27;&lt;/a&gt;")

    def test_triple_braces_raw(self):
        self.assertEqual(render("{{{ x }}}", x="<b>vet</b>"), "<b>vet</b>")

    def test_markup_not_escaped(self):
        self.assertEqual(render("{{ x }}", x=Markup("<img>")), "<img>")

    def test_none_renders_empty(self):
        self.assertEqual(render("[{{ x }}]", x=None), "[]")

    def test_attribute_access_on_data(self):
        self.assertEqual(render("{{ site.email }}", site=wrap({"email": "info@gromush.be"})), "info@gromush.be")

    def test_undefined_name_is_an_error_with_line(self):
        with self.assertRaisesRegex(TemplateError, r":2: NameError"):
            render("ok\n{{ nope }}")


class Control(unittest.TestCase):
    def test_if_elif_else(self):
        tpl = "{% if n == 1 %}een{% elif n == 2 %}twee{% else %}veel{% endif %}"
        self.assertEqual([render(tpl, n=i) for i in (1, 2, 3)], ["een", "twee", "veel"])

    def test_for_with_loop_and_else(self):
        tpl = "{% for x in xs %}{{ loop.index }}{{ x }}{% if not loop.last %},{% endif %}{% else %}leeg{% endfor %}"
        self.assertEqual(render(tpl, xs=["a", "b"]), "1a,2b")
        self.assertEqual(render(tpl, xs=[]), "leeg")

    def test_for_unpacking(self):
        self.assertEqual(render("{% for k, v in d.items() %}{{ k }}={{ v }};{% endfor %}", d={"a": 1, "b": 2}), "a=1;b=2;")

    def test_set(self):
        self.assertEqual(render("{% set y = x * 2 %}{{ y }}", x=4), "8")

    def test_newline_after_tag_is_trimmed(self):
        self.assertEqual(render("{% if True %}\nja\n{% endif %}\n"), "ja\n")

    def test_comments_vanish(self):
        self.assertEqual(render("a{# nota #}b"), "ab")

    def test_unclosed_block_is_an_error(self):
        with self.assertRaises(TemplateError):
            render("{% if x %}open")

    def test_unknown_tag_is_an_error(self):
        with self.assertRaises(TemplateError):
            render("{% macro x %}")


class IncludeExtends(unittest.TestCase):
    def test_include_with_sees_globals_and_with_only(self):
        env = env_with({"p.html": "{{ site }}:{{ label }}", "leak.html": "{{ item }}"}, {"site": "GroMush"})
        out = env.from_string('{% for item in [1] %}{% include "p.html" with {"label": item} %}{% endfor %}').render()
        self.assertEqual(out, "GroMush:1")
        with self.assertRaisesRegex(TemplateError, "NameError"):
            env.from_string('{% for item in [1] %}{% include "leak.html" %}{% endfor %}').render()

    def test_include_without_with(self):
        env = env_with({"p.html": "[{{ site }}]"}, {"site": "GroMush"})
        self.assertEqual(env.from_string('{% include "p.html" %}').render(), "[GroMush]")

    def test_include_missing_template(self):
        with self.assertRaisesRegex(TemplateError, "not found"):
            env_with({}).from_string('{% include "nope.html" %}').render()

    def test_extends_and_blocks(self):
        env = env_with({
            "base.html": "<title>{% block title %}Standaard{% endblock %}</title><main>{% block main %}{% endblock %}</main>",
            "page.html": '{% extends "base.html" %}\n{% block main %}Hallo {{ name }}{% endblock %}',
        })
        self.assertEqual(env.get("page.html").render({"name": "Anthony"}), "<title>Standaard</title><main>Hallo Anthony</main>")

    def test_two_level_extends(self):
        env = env_with({
            "base.html": "[{% block a %}base-a{% endblock %}|{% block b %}base-b{% endblock %}]",
            "mid.html": '{% extends "base.html" %}{% block a %}mid-a{% endblock %}{% block b %}mid-b{% endblock %}',
            "leaf.html": '{% extends "mid.html" %}{% block b %}leaf-b{% endblock %}',
        })
        self.assertEqual(env.get("leaf.html").render(), "[mid-a|leaf-b]")

    def test_extends_must_come_first(self):
        env = env_with({"base.html": "x"})
        with self.assertRaises(TemplateError):
            env.from_string('tekst {% extends "base.html" %}')


class Data(unittest.TestCase):
    def test_attrdict_missing_key_message(self):
        with self.assertRaisesRegex(AttributeError, "no key 'x'"):
            AttrDict(a=1).x


class OptionalValues(unittest.TestCase):
    def test_opt_reads_include_values_with_default(self):
        env = env_with({"p.html": '{{ opt("kind", "primary") }}|{{ opt("cls") }}'})
        page = env.from_string('{% include "p.html" with {"kind": "second"} %}/{% include "p.html" %}')
        self.assertEqual(page.render({}), "second|/primary|")


if __name__ == "__main__":
    unittest.main()
