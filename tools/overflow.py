"""Horizontal overflow check at the five reference widths (R38, AC35).

usage: python3 -I tools/overflow.py <url-or-html> [widths=320,390,768,1024,1440]

Loads the page in headless Chrome at each width (reduced motion forced, lazy images loaded,
web fonts ready) and compares the document's scrollWidth with the viewport width. Prints
"320 ok 390 ok 768 ok 1024 ok 1440 ok" when nothing overflows; a failing width prints as
"390 FAIL(+24)" followed by the widest offending elements. Exit 0 when all widths pass, else 1.
Honours FONT_SIZE=32 (200 % text) via cdp.py.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cdp import launch, navigate, viewport, evaluate, stop  # noqa: E402

WIDTHS = [320, 390, 768, 1024, 1440]

PROBE = """(async()=>{document.documentElement.style.scrollBehavior='auto';
for(const i of document.images){i.loading='eager'}
const h=document.documentElement.scrollHeight;for(let y=0;y<h;y+=800){scrollTo(0,y);await new Promise(r=>setTimeout(r,30))}
scrollTo(0,0);await document.fonts.ready;
const vw=document.documentElement.clientWidth,sw=Math.max(document.documentElement.scrollWidth,document.body?document.body.scrollWidth:0);
const clipped=e=>{for(let p=e.parentElement;p&&p!==document.body;p=p.parentElement){const o=getComputedStyle(p).overflowX;if(o!=='visible')return true}return false};
const off=[...document.querySelectorAll('body *')].map(e=>[e,e.getBoundingClientRect()]).filter(([e,r])=>r.width&&(r.right>vw+0.5||r.left<-0.5)&&!clipped(e))
 .sort((a,b)=>b[1].right-a[1].right).slice(0,4).map(([e,r])=>e.tagName.toLowerCase()+(e.id?'#'+e.id:'')+(typeof e.className==='string'&&e.className?'.'+e.className.trim().split(/\\s+/)[0]:'')+'['+Math.round(r.left)+'..'+Math.round(r.right)+']');
return JSON.stringify({vw,sw,off})})()"""


def main(argv):
    if not argv:
        print(__doc__.strip().splitlines()[2].strip(), file=sys.stderr)
        return 2
    import json
    target = argv[0]
    widths = [int(w) for w in argv[1].split(",")] if len(argv) > 1 else WIDTHS
    proc, ws = launch(reduced_motion=True)
    out, details, ok = [], [], True
    try:
        for w in widths:
            viewport(ws, w)
            navigate(ws, target)
            r = json.loads(evaluate(ws, PROBE))
            if r["sw"] > r["vw"]:
                ok = False
                out.append(f"{w} FAIL(+{r['sw'] - r['vw']})")
                details.append(f"  {w}: scrollWidth {r['sw']} > {r['vw']}: " + (", ".join(r["off"]) or "no single element found"))
            else:
                out.append(f"{w} ok")
    finally:
        stop(proc)
    print(" ".join(out))
    for d in details:
        print(d)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
