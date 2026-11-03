"""Minimal template engine for the GroMush static build (plan AD3). Python stdlib only.

Syntax:
  {{ expr }}            escaped output (Markup values pass through unescaped)
  {{{ expr }}}          raw output
  {# comment #}
  {% if expr %} {% elif expr %} {% else %} {% endif %}
  {% for x in expr %} / {% for k, v in expr %} ... {% else %} ... {% endfor %}   (loop.index, loop.first, loop.last)
  {% set name = expr %}
  {% include "partials/x.html" %} / {% include "partials/x.html" with {"key": expr} %}
  {% extends "layouts/base.html" %} with {% block name %} ... {% endblock %}
  opt("name", default)  the value of `name` if it is set (e.g. passed by `include ... with`), else default

Expressions are Python expressions evaluated against the context; dict keys read as attributes
(`site.email`). Templates are trusted repo files. An include sees the globals plus its `with`
dict only, never the caller's loop variables, so partials stay self-contained.
A newline directly after a {% %} tag is dropped (like Jinja's trim_blocks).
"""
import builtins
import html
import re
from pathlib import Path

TOKEN = re.compile(r"({{{.*?}}}|{{.*?}}|{%.*?%}\n?|{#.*?#}\n?)", re.S)
SAFE_BUILTINS = {n: getattr(builtins, n) for n in ("len", "range", "enumerate", "zip", "sorted", "min", "max",
                                                   "str", "int", "list", "dict", "any", "all", "round", "abs")}


class TemplateError(Exception):
    pass


class Markup(str):
    """A string that is already safe HTML; {{ }} does not escape it."""


class AttrDict(dict):
    """A dict whose keys also read as attributes; missing keys raise a clear error."""

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(f"no key {name!r} (keys: {', '.join(sorted(self))})") from None


def wrap(value):
    """Turn loaded JSON (dicts, lists) into AttrDicts recursively."""
    if isinstance(value, dict):
        return AttrDict({k: wrap(v) for k, v in value.items()})
    if isinstance(value, list):
        return [wrap(v) for v in value]
    return value


def escape(value):
    if value is None:
        return ""
    if isinstance(value, Markup):
        return str(value)
    return html.escape(str(value), quote=True)


class Node:
    def __init__(self, kind, line, **kw):
        self.kind, self.line = kind, line
        self.__dict__.update(kw)


class Template:
    def __init__(self, source, name="<string>", env=None):
        self.name, self.env = name, env
        self.parent = None  # extends target
        self.blocks = {}
        self.body = self._parse(source)

    # ---------- parsing ----------
    def _parse(self, source):
        root, stack, line = [], [], 1
        current = root

        def push(node, body_attr="body"):
            nonlocal current
            current.append(node)
            stack.append((node, current))
            current = getattr(node, body_attr)

        for part in TOKEN.split(source):
            if not part:
                continue
            here = line
            line += part.count("\n")
            if not TOKEN.fullmatch(part):
                current.append(Node("text", here, text=part))
            elif part.startswith("{#"):
                continue
            elif part.startswith("{{{"):
                current.append(Node("var", here, expr=self._compile(part[3:-3], here), raw=True))
            elif part.startswith("{{"):
                current.append(Node("var", here, expr=self._compile(part[2:-2], here), raw=False))
            elif part.startswith("{%"):
                tag = part.rstrip("\n")[2:-2].strip()
                word, _, rest = tag.partition(" ")
                rest = rest.strip()
                if word == "if":
                    push(Node("if", here, branches=[(self._compile(rest, here), [])], other=None, body=None))
                    current = stack[-1][0].branches[0][1]
                elif word in ("elif", "else") and stack and stack[-1][0].kind == "if":
                    node = stack[-1][0]
                    if word == "elif":
                        node.branches.append((self._compile(rest, here), []))
                        current = node.branches[-1][1]
                    else:
                        node.other = []
                        current = node.other
                elif word == "else" and stack and stack[-1][0].kind == "for":
                    stack[-1][0].other = []
                    current = stack[-1][0].other
                elif word == "for":
                    m = re.fullmatch(r"([\w\s,]+?)\s+in\s+(.+)", rest, re.S)
                    if not m:
                        raise self._error(here, f"bad for tag: {tag!r}")
                    names = [n.strip() for n in m.group(1).split(",")]
                    push(Node("for", here, names=names, iterable=self._compile(m.group(2), here), body=[], other=None))
                elif word == "block":
                    node = Node("block", here, name=rest, body=[])
                    if rest in self.blocks:
                        raise self._error(here, f"block {rest!r} defined twice")
                    self.blocks[rest] = node
                    push(node)
                elif word in ("endif", "endfor", "endblock"):
                    want = word[3:]
                    if not stack or stack[-1][0].kind != want:
                        raise self._error(here, f"unexpected {{% {word} %}}")
                    current = stack.pop()[1]
                elif word == "set":
                    name, eq, expr = rest.partition("=")
                    if not eq or not name.strip().isidentifier():
                        raise self._error(here, f"bad set tag: {tag!r}")
                    current.append(Node("set", here, name=name.strip(), expr=self._compile(expr, here)))
                elif word == "include":
                    m = re.fullmatch(r'"([^"]+)"(?:\s+with\s+(.+))?', rest, re.S)
                    if not m:
                        raise self._error(here, f"bad include tag: {tag!r}")
                    data = self._compile(m.group(2), here) if m.group(2) else None
                    current.append(Node("include", here, template=m.group(1), data=data))
                elif word == "extends":
                    m = re.fullmatch(r'"([^"]+)"', rest)
                    if not m or self.parent or stack or any(n.kind != "text" or n.text.strip() for n in root):
                        raise self._error(here, "extends must be the first tag, used once")
                    self.parent = m.group(1)
                else:
                    raise self._error(here, f"unknown tag: {tag!r}")
        if stack:
            raise self._error(stack[-1][0].line, f"unclosed {{% {stack[-1][0].kind} %}}")
        return root

    def _compile(self, expr, line):
        try:
            return compile(expr.strip(), f"{self.name}:{line}", "eval")
        except SyntaxError as exc:
            raise self._error(line, f"bad expression {expr.strip()!r}: {exc.msg}") from None

    def _error(self, line, msg):
        return TemplateError(f"{self.name}:{line}: {msg}")

    # ---------- rendering ----------
    def render(self, context=None, blocks=None):
        ctx = dict(self.env.globals if self.env else {})
        ctx.update(context or {})
        ctx["opt"] = lambda name, default=None: ctx.get(name, default)  # optional include values
        overrides = dict(self.blocks)
        overrides.update(blocks or {})
        if self.parent:
            return self.env.get(self.parent).render(context=ctx, blocks=overrides)
        out = []
        self._run(self.body, ctx, out, overrides)
        return "".join(out)

    def _eval(self, code, ctx, line):
        try:
            return eval(code, {**ctx, "__builtins__": SAFE_BUILTINS})
        except Exception as exc:
            raise self._error(line, f"{type(exc).__name__}: {exc}") from None

    def _run(self, nodes, ctx, out, blocks):
        for n in nodes:
            if n.kind == "text":
                out.append(n.text)
            elif n.kind == "var":
                value = self._eval(n.expr, ctx, n.line)
                out.append("" if value is None else str(value)) if n.raw else out.append(escape(value))
            elif n.kind == "if":
                for cond, body in n.branches:
                    if self._eval(cond, ctx, n.line):
                        self._run(body, ctx, out, blocks)
                        break
                else:
                    if n.other is not None:
                        self._run(n.other, ctx, out, blocks)
            elif n.kind == "for":
                items = list(self._eval(n.iterable, ctx, n.line) or [])
                for i, item in enumerate(items):
                    inner = dict(ctx)
                    if len(n.names) == 1:
                        inner[n.names[0]] = item
                    else:
                        inner.update(zip(n.names, item))
                    inner["loop"] = AttrDict(index=i + 1, index0=i, first=i == 0, last=i == len(items) - 1, length=len(items))
                    self._run(n.body, inner, out, blocks)
                if not items and n.other is not None:
                    self._run(n.other, ctx, out, blocks)
            elif n.kind == "set":
                ctx[n.name] = self._eval(n.expr, ctx, n.line)
            elif n.kind == "block":
                block = blocks.get(n.name, n)
                self._run(block.body, ctx, out, blocks)
            elif n.kind == "include":
                data = self._eval(n.data, ctx, n.line) if n.data else {}
                if not isinstance(data, dict):
                    raise self._error(n.line, "include ... with needs a dict")
                out.append(self.env.get(n.template).render(context=data))


class Environment:
    """Loads templates from one root directory and holds the globals every template sees."""

    def __init__(self, root, globals=None):
        self.root = Path(root)
        self.globals = dict(globals or {})
        self._cache = {}

    def get(self, name):
        if name not in self._cache:
            path = self.root / name
            if not path.is_file():
                raise TemplateError(f"template not found: {name}")
            self._cache[name] = Template(path.read_text(encoding="utf-8"), name, self)
        return self._cache[name]

    def from_string(self, source, name="<string>"):
        return Template(source, name, self)
