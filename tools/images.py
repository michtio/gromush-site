"""Render the image register into responsive files (plan AD12, PRD R37). Python stdlib only.

usage: python3 -I tools/images.py [--force] [--prune] [id ...]

Reads src/data/images.json and writes src/static/img/r/<id>-<width>.{avif,webp} at the widths of
src/gen/picture.py (400/800/1200/1600, never upscaled) and <id>-<width>.{jpg|png} at the two fallback widths
(picture.fallback_widths: the smallest and the largest up to 800 px). Images with transparency (cut-outs, logo)
get a png fallback instead of jpeg. Files in img/r/ that the register no longer produces are listed as stale;
--prune deletes them. Files newer than their source are skipped unless --force. The build copies
src/static into docs/, and picture() refuses an image whose files are missing.

Host tools: sips (macOS, decodes the source and writes jpeg/png), cwebp (webp), avifenc (avif). A missing
tool is reported up front; the run continues without that format and exits 1, so nothing is half-silent.
"""
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from gen.picture import RENDER_DIR, fallback_widths, rendered_name, widths_for  # noqa: E402

REGISTER = ROOT / "src" / "data" / "images.json"
OUT = ROOT / "src" / "static" / RENDER_DIR
TOOLS = {"sips": "decode + jpeg/png", "cwebp": "webp", "avifenc": "avif"}
WEBP_Q, AVIF_Q, JPEG_Q = "80", "60", "70"
TOOLS_FOR = {"webp": "cwebp", "avif": "avifenc"}


def run(*cmd):
    r = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"{cmd[0]} failed: {r.stdout.strip()[-400:]}")
    return r.stdout


def has_alpha(path):
    return "hasAlpha: yes" in run("sips", "-g", "hasAlpha", str(path))


def fresh(target, source):
    return target.is_file() and target.stat().st_mtime >= source.stat().st_mtime


def render_one(img, tools, force, tmp):
    source = ROOT / img["source"]
    if not source.is_file():
        raise RuntimeError(f"{img['id']}: source not found: {img['source']}")
    actual = run("sips", "-g", "pixelWidth", "-g", "pixelHeight", str(source))
    w = int(actual.split("pixelWidth:")[1].split()[0])
    h = int(actual.split("pixelHeight:")[1].split()[0])
    if (w, h) != (img["width"], img["height"]):
        raise RuntimeError(f"{img['id']}: images.json says {img['width']}x{img['height']}, the file is {w}x{h}")
    fallback = "png" if has_alpha(source) else "jpg"
    written = 0
    widths = widths_for(w)
    for width in widths:
        exts = ("avif", "webp", fallback) if width in fallback_widths(widths) else ("avif", "webp")
        targets = {ext: OUT / rendered_name(img["id"], width, ext) for ext in exts}
        wanted = {ext: t for ext, t in targets.items()
                  if (force or not fresh(t, source)) and (ext in ("jpg", "png") or TOOLS_FOR[ext] in tools)}
        if not wanted:
            continue
        png = Path(tmp) / f"{img['id']}-{width}.png"
        run("sips", "-s", "format", "png", "--resampleWidth", str(width), str(source), "--out", str(png))
        for ext, target in wanted.items():
            if ext == "png":
                shutil.copyfile(png, target)
            elif ext == "jpg":
                run("sips", "-s", "format", "jpeg", "-s", "formatOptions", JPEG_Q, str(png), "--out", str(target))
            elif ext == "webp":
                run("cwebp", "-quiet", "-q", WEBP_Q, "-m", "6", "-metadata", "none", str(png), "-o", str(target))
            elif ext == "avif":
                run("avifenc", "-q", AVIF_Q, "-s", "6", str(png), str(target))
            written += 1
    return written



def expected_names(images):
    """Every file name the register produces: avif + webp at each width, jpg and png at the fallback widths
    (both extensions, since which one a source gets depends on its transparency)."""
    names = set()
    for i in images:
        widths = widths_for(i["width"])
        for w in widths:
            names |= {rendered_name(i["id"], w, ext) for ext in ("avif", "webp")}
        for w in fallback_widths(widths):
            names |= {rendered_name(i["id"], w, ext) for ext in ("jpg", "png")}
    return names


def main(argv=None):
    args = sys.argv[1:] if argv is None else argv
    force = "--force" in args
    prune = "--prune" in args
    only = [a for a in args if not a.startswith("--")]
    tools = {t for t in TOOLS if shutil.which(t)}
    missing = [t for t in TOOLS if t not in tools]
    if "sips" not in tools:
        print("images: sips not found (macOS only); cannot decode sources. Nothing rendered.", file=sys.stderr)
        return 1
    for t in missing:
        print(f"images: {t} not found, skipping {TOOLS[t]} (brew install {'webp' if t == 'cwebp' else 'libavif'})",
              file=sys.stderr)
    images = json.loads(REGISTER.read_text(encoding="utf-8"))["images"]
    unknown = set(only) - {i["id"] for i in images}
    if unknown:
        print(f"images: unknown id(s): {', '.join(sorted(unknown))}", file=sys.stderr)
        return 1
    OUT.mkdir(parents=True, exist_ok=True)
    total, failed = 0, []
    with tempfile.TemporaryDirectory() as tmp:
        for img in images:
            if only and img["id"] not in only:
                continue
            try:
                total += render_one(img, tools, force, tmp)
            except RuntimeError as exc:
                failed.append(str(exc))
    expected = expected_names(images)
    stale = sorted(p.name for p in OUT.iterdir() if p.is_file() and p.name not in expected)
    print(f"images: {total} files written to {OUT.relative_to(ROOT)}")
    for name in stale:
        if prune:
            (OUT / name).unlink()
            print(f"images: removed stale file {RENDER_DIR}/{name}")
        else:
            print(f"images: warning: stale file {RENDER_DIR}/{name} (not produced by images.json; --prune removes it)",
                  file=sys.stderr)
    for msg in failed:
        print(f"images: error: {msg}", file=sys.stderr)
    return 1 if failed or missing else 0


if __name__ == "__main__":
    sys.exit(main())
