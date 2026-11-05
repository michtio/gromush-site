"""Real keyboard walk (S9, AC11): presses Tab from the top of the page and records which [data-scene] each focus
lands in, so the scenes reached by keyboard and their order can be read off.

usage: python3 -I tools/tabwalk.py <url> <width> [max_tabs=400]
Prints the scenes in the order focus first entered them, the number of Tab presses spent in each, and "tab ok"
when every visible [data-scene] was reached and never revisited out of order (exit 0), else "tab FAIL: ..." (exit 1).
"""
import json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cdp import launch, viewport, to_url, evaluate, stop  # noqa: E402

SCENES = """JSON.stringify([...document.querySelectorAll('main [data-scene]')].filter(s=>{let e=s;while(e&&e!==document.body){if(getComputedStyle(e).display==='none')return false;e=e.parentElement}return true}).map(s=>s.dataset.scene))"""
WHERE = """(()=>{const a=document.activeElement;const s=a&&a.closest('[data-scene]');return JSON.stringify([s?s.dataset.scene:(a&&a.closest('footer')?'#footer':a&&a.closest('header')?'#header':a?a.tagName:'-'),!!(a&&a.closest('footer'))])})()"""


def main(argv):
    url, w = argv[0], int(argv[1])
    limit = int(argv[2]) if len(argv) > 2 else 400
    proc, ws = launch()
    try:
        viewport(ws, w)
        ws.send("Page.navigate", {"url": to_url(url)}); time.sleep(3)
        want = json.loads(evaluate(ws, SCENES))
        seen, counts = [], {}
        for _ in range(limit):
            for t in ("keyDown", "keyUp"):
                ws.send("Input.dispatchKeyEvent", {"type": t, "key": "Tab", "code": "Tab", "windowsVirtualKeyCode": 9})
            time.sleep(0.03)
            scene, in_footer = json.loads(evaluate(ws, WHERE))
            if in_footer:
                break
            if not scene.startswith('#') and scene in want:
                counts[scene] = counts.get(scene, 0) + 1
                if not seen or seen[-1] != scene:
                    seen.append(scene)
    finally:
        stop(proc)
    print(w, 'scenes in DOM:', want)
    print(w, 'focus order:  ', seen, counts)
    fails = []
    if [s for s in seen] != [s for s in want if s in seen]:
        fails.append('out of order or revisited')
    missing = [s for s in want if s not in seen]
    if missing:
        fails.append('never reached: ' + ', '.join(missing))
    print('tab ok' if not fails else 'tab FAIL: ' + '; '.join(fails))
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
