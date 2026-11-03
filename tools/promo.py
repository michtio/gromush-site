"""ProefBox promo flow over several page views in one browser session (S4; PRD R35, AC33, plan AD15).

usage: python3 -I tools/promo.py <site-url> [--close button|escape|backdrop] [--width 1440] [-v]
  <site-url>  the served site root, e.g. http://127.0.0.1:8766/gromush-site

One headless Chrome, one tab, so sessionStorage carries over between the views (tools/promo.js probes):
  page 1  /                     wait past the delay (data-delay + 1 s) and scroll to the end: no promo
  page 2  /_dev/componenten/    scroll to 45 % (the scroll trigger): the promo shows as a modal with focus in it;
          then close it with a real click on its button, a real Escape key, or a real click outside the paper
          (--close, default button): closed, focus back on the element that had it before (the header CTA,
          focused by the script before scrolling), state "dismissed"
  page 3  /                     wait past the delay and scroll to the end: no promo
Prints "<page1> <page2> <page3>", where page1 is "none" or "shown", page2 "shown" or "none" (plus
"-not-dismissed" when the close failed), page3 "dismissed-none" or "dismissed-shown". The pass line is
"none shown dismissed-none"; exit 0 only then. -v prints each probe to stderr. Python 3 stdlib only.
"""
import argparse
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cdp import launch, viewport, evaluate, navigate, stop  # noqa: E402

PROBE = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "promo.js"), encoding="utf-8").read()


def probe(ws, verbose, label):
    r = json.loads(evaluate(ws, PROBE))
    if verbose:
        print(label, json.dumps(r), file=sys.stderr)
    return r


def click(ws, x, y):
    for t in ("mousePressed", "mouseReleased"):
        ws.send("Input.dispatchMouseEvent", {"type": t, "x": x, "y": y, "button": "left", "clickCount": 1})


def scroll_to(ws, share):
    evaluate(ws, f"window.scrollTo(0, (document.documentElement.scrollHeight - innerHeight) * {share})")
    time.sleep(0.8)


def main(argv):
    ap = argparse.ArgumentParser(description="ProefBox promo flow over three page views (R35).")
    ap.add_argument("site")
    ap.add_argument("--close", choices=("button", "escape", "backdrop"), default="button")
    ap.add_argument("--width", type=int, default=1440)
    ap.add_argument("-v", action="store_true")
    args = ap.parse_args(argv)
    site = args.site.rstrip("/")
    proc, ws = launch()
    out = []
    try:
        viewport(ws, args.width)
        # page 1: never on the first page view
        navigate(ws, site + "/")
        delay = float(evaluate(ws, "(document.getElementById('promo')||{dataset:{}}).dataset.delay || 8"))
        time.sleep(delay + 1)
        scroll_to(ws, 1)
        out.append("shown" if probe(ws, args.v, "page1")["open"] else "none")
        # page 2: the scroll trigger, then the dismissal
        navigate(ws, site + "/_dev/componenten/")
        evaluate(ws, "document.querySelector('.site-header .btn-cta').focus()")  # focus before the promo opens
        scroll_to(ws, 0.45)
        r = probe(ws, args.v, "page2-open")
        token = "shown" if r["open"] and r["focusIn"] else "none"
        if r["open"]:
            if args.close == "button":
                click(ws, *r["close"])
            elif args.close == "escape":
                for t in ("keyDown", "keyUp"):
                    ws.send("Input.dispatchKeyEvent", {"type": t, "key": "Escape", "code": "Escape", "windowsVirtualKeyCode": 27})
            else:
                left, top = r["box"][0], r["box"][1]
                click(ws, max(2, left / 2), max(2, top / 2))  # on the backdrop, outside the paper
            time.sleep(0.5)
            r = probe(ws, args.v, "page2-closed")
            focus_back = evaluate(ws, "document.activeElement === document.querySelector('.site-header .btn-cta')")
            if r["open"] or (r["store"] or {}).get("state") != "dismissed" or not focus_back:
                token += "-not-dismissed"
        out.append(token)
        # page 3: dismissed, so never again this session
        navigate(ws, site + "/")
        time.sleep(delay + 1)
        scroll_to(ws, 1)
        r = probe(ws, args.v, "page3")
        out.append(("dismissed-" if (r["store"] or {}).get("state") == "dismissed" else "state-") +
                   ("shown" if r["open"] else "none"))
    finally:
        stop(proc)
    line = " ".join(out)
    print(line)
    return 0 if line == "none shown dismissed-none" else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
