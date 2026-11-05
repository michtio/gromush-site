"""No-JS check: loads a page with script execution disabled and reports what a visitor still gets.

usage: python3 -I tools/nojs.py <url-or-html> <width> <out.png>

Generalised from .impeccable/tools/nojs.py (which read final.html's own ids). Prints a JSON report
and a verdict line, and saves a screenshot of the first 900 px:
  jsClass      the <html> class (must not contain "js": the inline script did not run)
  header/main/footer  visible (display not none, height > 0)
  nav          the site navigation is visible, or the menu toggle is (null when the page has no nav yet)
  sections     every direct child section of <main> has height (a reveal-on-scroll left hidden fails)
  forms        per form: visible, method, action, enctype, visible field count
  imgsBroken   images that failed to load
  sw           document scrollWidth (must equal the width)
  ring         homepage radial opening (S9, AC13): {paths, drawn} of the visible hyphae network, where drawn counts
               paths fully drawn (visible, opacity > 0, no dash offset); null on pages without it. Fails unless
               drawn == paths. Only measurable from 1100 px (below, the opening shows its list instead).
  recipes      /inspiratie/ (S18, AD14): {articles, readable}: recipe articles in the page and how many are visible
               with a title, ingredients and steps; null on pages without them. Fails unless readable == articles.
Verdict "nojs ok", or "nojs FAIL: ..." with exit 1.
"""
import base64
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cdp import launch, viewport, evaluate, to_url, stop  # noqa: E402

# Synchronous on purpose: with page scripts disabled, timers and promise callbacks never run.
# Lazy images load eagerly when scripting is disabled (HTML spec), so the Python side just waits.
PROBE = """(()=>{
const vis=e=>{if(!e)return null;const r=e.getBoundingClientRect();const cs=getComputedStyle(e);return cs.display!=='none'&&cs.visibility!=='hidden'&&r.height>0&&parseFloat(cs.opacity)>0};
const q=s=>document.querySelector(s);
const nav=q('body > header nav, .site-header nav, nav[aria-label]');const toggle=q('.menu-btn, [aria-controls][aria-expanded]');
const main=q('main');
return JSON.stringify({jsClass:document.documentElement.className,header:vis(q('body > header')),main:vis(main),footer:vis(q('body > footer')),
nav:nav?(vis(nav)||vis(toggle)):null,
sections:main?[...main.querySelectorAll(':scope > section, :scope > * > section')].map(s=>vis(s)&&s.getBoundingClientRect().height>40).every(Boolean):null,
forms:[...document.forms].map(f=>({id:f.id||null,visible:vis(f),method:f.getAttribute('method'),action:f.getAttribute('action'),enctype:f.getAttribute('enctype'),
 fields:[...f.querySelectorAll('input:not([type=hidden]),select,textarea')].filter(vis).length})),
imgsBroken:[...document.images].filter(i=>i.complete&&!i.naturalWidth).map(i=>i.currentSrc||i.src),
sw:document.documentElement.scrollWidth,
recipes:(()=>{const a=[...document.querySelectorAll('article.rc-article')];if(!a.length)return null;
 return {articles:a.length,readable:a.filter(x=>vis(x)&&vis(x.querySelector('h3'))&&x.querySelectorAll('.rc-ingredients li').length&&x.querySelectorAll('.rc-steps li').length).length}})(),
ring:(()=>{const g=[...document.querySelectorAll('.ring-svg .ring-hy')].find(x=>getComputedStyle(x).display!=='none');if(!g)return null;
 const ps=[...g.querySelectorAll('path')];const drawn=ps.filter(p=>{const cs=getComputedStyle(p);return cs.visibility!=='hidden'&&parseFloat(cs.opacity)>0&&(parseFloat(cs.strokeDashoffset)||0)===0}).length;
 return {paths:ps.length,drawn}})()})})()"""


def main(argv):
    if len(argv) < 3:
        print(__doc__.strip().splitlines()[2].strip(), file=sys.stderr)
        return 2
    target, width, out = argv[0], int(argv[1]), argv[2]
    proc, ws = launch()
    try:
        viewport(ws, width)
        ws.send("Emulation.setScriptExecutionDisabled", {"value": True})
        ws.send("Page.navigate", {"url": to_url(target)})
        time.sleep(3.0)
        # Runtime.evaluate still runs while page scripts are disabled (synchronous code only).
        r = json.loads(evaluate(ws, PROBE))
        shot = ws.send("Page.captureScreenshot", {"format": "png", "clip": {"x": 0, "y": 0, "width": width, "height": 900, "scale": 1}})
        with open(out, "wb") as f:
            f.write(base64.b64decode(shot["data"]))
    finally:
        stop(proc)
    print(width, json.dumps(r, ensure_ascii=False))
    fails = []
    if "js" in r["jsClass"].split():
        fails.append("page scripts ran")
    for k in ("header", "main", "footer"):
        if r[k] is not True:
            fails.append(f"{k} not visible")
    if r["nav"] is False:
        fails.append("nav not visible")
    if r["sections"] is False:
        fails.append("a section is hidden or empty")
    fails += [f"form {f['id'] or '?'} not visible" for f in r["forms"] if not f["visible"]]
    if r["imgsBroken"]:
        fails.append(f"{len(r['imgsBroken'])} broken image(s)")
    if r.get("recipes") and r["recipes"]["readable"] != r["recipes"]["articles"]:
        fails.append(f"recipes not readable ({r['recipes']['readable']} of {r['recipes']['articles']})")
    if r.get("ring") and r["ring"]["drawn"] != r["ring"]["paths"]:
        fails.append(f"hyphae network not fully drawn ({r['ring']['drawn']} of {r['ring']['paths']} paths)")
    if r["sw"] > width:
        fails.append(f"scrollWidth {r['sw']} > {width}")
    print("nojs ok" if not fails else "nojs FAIL: " + "; ".join(fails))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
