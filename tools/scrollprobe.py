"""Scroll-sampling probe for scroll-driven sections (pinned hero, delivery van).

usage: python3 -I tools/scrollprobe.py <url> <width> <height> '<js returning JSON>' [y1,y2,...]
Loads the page (use the local server URL so rAF runs), scrolls to each y, waits 1.6s, and
prints the expression's value. Example expression:
  JSON.stringify({top:Math.round(document.querySelector('.net').getBoundingClientRect().top)})
"""
import os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cdp import launch, viewport, to_url, evaluate, stop  # noqa: E402

url, w, h, expr = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
ys = [int(y) for y in (sys.argv[5] if len(sys.argv) > 5 else "0,300,600,900,1200,1500").split(",")]
proc, ws = launch()
try:
    viewport(ws, w, h)
    ws.send("Page.navigate", {"url": to_url(url)}); time.sleep(3)
    evaluate(ws, "document.documentElement.style.scrollBehavior='auto'")
    for y in ys:
        evaluate(ws, f"scrollTo(0,{y})"); time.sleep(1.6)
        print(y, evaluate(ws, expr))
finally:
    stop(proc)
