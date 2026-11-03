"""Load a page in headless Chrome, report runtime JS errors, then evaluate expressions.

usage: python3 -I tools/check.py <html-or-url> <width> '<js expression>' [...]
Expressions may return promises (awaited). Wrap layout-dependent checks in
document.fonts.ready.then(()=>...). Use FONT_SIZE=32 for a real 200% default font size.
Motion is not reduced here (use fullshot.py for reduced-motion captures).
"""
import os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cdp import WS, CHROME, launch, viewport, to_url, evaluate, stop  # noqa: E402,F401


def main():
    target, width, exprs = sys.argv[1], int(sys.argv[2]), sys.argv[3:]
    proc, ws = launch()
    try:
        viewport(ws, width)
        ws.send("Page.addScriptToEvaluateOnNewDocument", {"source": "window.__errs=[];addEventListener('error',e=>__errs.push(e.message+' @'+e.lineno));"})
        ws.send("Page.navigate", {"url": to_url(target)})
        time.sleep(3)
        print("errors:", evaluate(ws, "JSON.stringify(window.__errs)"))
        for e in exprs:
            print(e[:70], "=>", evaluate(ws, e))
    finally:
        stop(proc)


if __name__ == "__main__":
    main()
