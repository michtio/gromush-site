"""Full-page and sliced screenshots via CDP, with reduced motion forced and lazy images loaded.

usage: python3 -I tools/fullshot.py <html-or-url> <out-prefix> [widths=1440,390]
writes <prefix>-<w>.png (full page, max 16000px tall) and <prefix>-<w>-sNN.png slices
(1400px tall at desktop, 1600px on phones); prints unloaded image count and scrollWidth.

env:
  PRE_JS='<js>'      run before capturing (e.g. click "Kook je thuis?" to show Particulier mode)
  SHOT_SEL='<css>'   capture only that element as <prefix>-<w>-el.png (skips the full page)
  FONT_SIZE=32       real browser default font size (200% text)
  MOTION=1           do not force reduced motion
"""
import base64, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cdp import WS, CHROME, launch, viewport, to_url, evaluate, stop  # noqa: E402,F401

JS_LOAD = """(async()=>{document.documentElement.style.scrollBehavior='auto';
for(const i of document.images){i.loading='eager'}
const h=document.documentElement.scrollHeight;for(let y=0;y<h;y+=600){scrollTo(0,y);await new Promise(r=>setTimeout(r,60))}
scrollTo(0,0);await document.fonts.ready;
await Promise.all([...document.images].map(i=>i.complete?0:new Promise(r=>{i.onload=i.onerror=r;setTimeout(r,4000)})));
return [...document.images].filter(i=>!i.naturalWidth).length})()"""


def shot(ws, path, clip):
    r = ws.send("Page.captureScreenshot", {"format": "png", "captureBeyondViewport": True, "clip": {**clip, "scale": 1}})
    with open(path, "wb") as f:
        f.write(base64.b64decode(r["data"]))


def main():
    target, prefix = sys.argv[1], sys.argv[2]
    widths = [int(w) for w in (sys.argv[3] if len(sys.argv) > 3 else "1440,390").split(",")]
    proc, ws = launch(reduced_motion=not os.environ.get("MOTION"))
    try:
        for w in widths:
            viewport(ws, w)
            ws.send("Page.navigate", {"url": to_url(target)})
            time.sleep(3.0)
            unloaded = evaluate(ws, JS_LOAD)
            time.sleep(1.0)
            if os.environ.get("PRE_JS"):
                evaluate(ws, os.environ["PRE_JS"]); time.sleep(1.2)
            if os.environ.get("SHOT_SEL"):
                x, y, ew, eh = evaluate(ws, "(()=>{const r=document.querySelector(%r).getBoundingClientRect();return [r.left+scrollX,r.top+scrollY,r.width,r.height]})()" % os.environ["SHOT_SEL"])
                out = f"{prefix}-{w}-el.png"
                shot(ws, out, {"x": max(0, x - 16), "y": max(0, y - 16), "width": min(w, ew + 32), "height": min(eh + 32, 6000)})
                print(out); continue
            h = min(int(ws.send("Page.getLayoutMetrics")["cssContentSize"]["height"]), 16000)
            shot(ws, f"{prefix}-{w}.png", {"x": 0, "y": 0, "width": w, "height": h})
            sl = 1400 if w > 600 else 1600
            for i, y in enumerate(range(0, h, sl)):
                shot(ws, f"{prefix}-{w}-s{i+1:02d}.png", {"x": 0, "y": y, "width": w, "height": min(sl, h - y)})
            print(f"{prefix}-{w}.png unloaded_imgs={unloaded} height={h} scrollWidth={evaluate(ws, 'document.documentElement.scrollWidth')}")
    finally:
        stop(proc)


if __name__ == "__main__":
    main()
