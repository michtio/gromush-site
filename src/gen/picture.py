"""Responsive images for the GroMush build (plan AD12, PRD R37).

tools/images.py renders every source in src/data/images.json into src/static/img/r/<id>-<width>.<ext>:
avif + webp at each width, plus a jpeg fallback (png when the source has transparency, e.g. cut-outs) at two
widths only (the smallest and the largest up to 800 px, fallback_widths()): every current browser takes avif or
webp, so the fallback only has to be good enough, and capping it keeps docs/ small (S4 follow-up).
picture() turns one images.json entry into <picture> with avif and webp <source>s and the fallback <img>,
with width, height, loading, decoding and the Dutch alt from images.json. It fails the build when the
image is unknown, has no alt yet, or its rendered files are missing.
"""
from pathlib import Path

from .template import Markup, escape

WIDTHS = (400, 800, 1200, 1600)
RENDER_DIR = "img/r"          # under src/static (rendered files, committed) and so under docs/
FALLBACKS = ("jpg", "png")    # jpeg for photos, png for images with transparency
MODERN = (("avif", "image/avif"), ("webp", "image/webp"))


class PictureError(ValueError):
    pass


def widths_for(source_width):
    """Rendered widths for a source: the standard widths up to the source width (never upscaled),
    plus the source width itself when it is clearly larger than the last standard one (>15 %)."""
    out = [w for w in WIDTHS if w <= source_width]
    if not out:
        return [source_width]
    if source_width > out[-1] * 1.15 and source_width < WIDTHS[-1]:
        out.append(source_width)
    return out


FALLBACK_CAP = 800


def fallback_widths(widths):
    """Widths that also get the jpeg/png fallback: the smallest and the largest up to FALLBACK_CAP."""
    capped = [w for w in widths if w <= FALLBACK_CAP]
    return sorted({widths[0], capped[-1] if capped else widths[0]})


def height_for(img, width):
    return round(img.height * width / img.width)


def rendered_name(image_id, width, ext):
    return f"{image_id}-{width}.{ext}"


def _srcset(url, image_id, widths, ext):
    return ", ".join(f"{url('/' + RENDER_DIR + '/' + rendered_name(image_id, w, ext))} {w}w" for w in widths)


def render(img, *, url, static_dir, cls="", sizes=None, loading=None, decorative=False):
    """One images.json entry -> <picture> markup.

    cls         class on the <img> (the <picture> is display:contents, so CSS targets the img)
    sizes       the sizes attribute (default 100vw, or the width itself for a single rendering)
    loading     'lazy' or 'eager'; default from images.json ("eager": true), else lazy
    decorative  alt="" whatever the register says (e.g. a town photo beside the town's name)
    """
    if decorative:
        alt = ""
    elif img.get("alt") is None:
        raise PictureError(f"image {img.id!r} has no alt text yet in images.json (R37)")
    else:
        alt = img.alt
    widths = widths_for(img.width)
    static_dir = Path(static_dir)

    fb_widths = fallback_widths(widths)

    def present(ext, ws=widths):
        return all((static_dir / RENDER_DIR / rendered_name(img.id, w, ext)).is_file() for w in ws)

    fallback = next((ext for ext in FALLBACKS if present(ext, fb_widths)), None)
    if fallback is None:
        raise PictureError(f"image {img.id!r} is not rendered yet ({RENDER_DIR}/{img.id}-*.jpg|png missing): "
                           f"run python3 -I tools/images.py")
    modern = [(ext, mime) for ext, mime in MODERN if present(ext)]
    if not modern:
        raise PictureError(f"image {img.id!r} has no avif or webp rendering: run python3 -I tools/images.py")
    if loading is None:
        loading = "eager" if img.get("eager") else "lazy"
    if loading not in ("lazy", "eager"):
        raise PictureError(f"loading must be 'lazy' or 'eager', got {loading!r}")
    if not sizes:  # w descriptors need sizes; one rendering is shown at its own width at most
        sizes = "100vw" if len(widths) > 1 else f"{widths[0]}px"
    size_attr = f' sizes="{escape(sizes)}"'
    sources = "".join(f'<source type="{mime}" srcset="{escape(_srcset(url, img.id, widths, ext))}"{size_attr}>'
                      for ext, mime in modern)
    largest = widths[-1]
    src_w = fb_widths[-1]
    attrs = []
    if cls:
        attrs.append(f'class="{escape(cls)}"')
    attrs += [f'src="{escape(url("/" + RENDER_DIR + "/" + rendered_name(img.id, src_w, fallback)))}"',
              f'srcset="{escape(_srcset(url, img.id, fb_widths, fallback))}"']
    attrs.append(size_attr.strip())
    attrs += [f'alt="{escape(alt)}"', f'width="{largest}"', f'height="{height_for(img, largest)}"',
              f'loading="{loading}"', 'decoding="async"']
    if loading == "eager":
        attrs.append('fetchpriority="high"')
    return Markup(f"<picture>{sources}<img {' '.join(attrs)}></picture>")
