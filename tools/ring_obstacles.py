"""Homepage radial opening (S9, plan AD13): are the built page's obstacles still the ones the hyphae were grown around?

usage: python3 -I tools/ring_obstacles.py <url> [tolerance=2]
Measures the opening at every width of src/gen/hyphae_obs (tools/ringmeasure.js: title, intro, slip, tape, note,
curved-label glyphs, pills, discs, in ring-svg units) and compares each box with the stored file. Prints the largest
deviation per width and "obstacles ok" (exit 0) when every box is within the tolerance (ring-svg units; the network
keeps 6 to 12 units of padding). A larger deviation means the layout changed since the network was generated:
re-measure (write the new JSON files), rebuild, and re-run tools/ringprobes.sh.
Env: WRITE=1 writes the measured files into src/gen/hyphae_obs instead of comparing.
"""
import json, os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from cdp import launch, viewport, to_url, evaluate, stop  # noqa: E402

OBS = os.path.join(HERE, '..', 'src', 'gen', 'hyphae_obs')


def boxes(o):
    out = {('core', k): v for k, v in o['core'].items()}
    for k, m in o['meds'].items():
        out[(k, 'c')] = m['c'] + [m['r']]
        out[(k, 'pill')] = m['pill']
        for i, g in enumerate(m['glyphs']):
            out[(k, 'g%d' % i)] = g
    return out


def main(argv):
    url, tol = argv[0], float(argv[1]) if len(argv) > 1 else 2.0
    js = open(os.path.join(HERE, 'ringmeasure.js'), encoding='utf-8').read()
    widths = sorted(int(f[4:-5]) for f in os.listdir(OBS) if f.startswith('obs-') and f.endswith('.json'))
    bad = 0
    for w in widths:
        proc, ws = launch()
        try:
            viewport(ws, w)
            ws.send("Page.navigate", {"url": to_url(url)}); time.sleep(3)
            got = json.loads(evaluate(ws, js))
        finally:
            stop(proc)
        path = os.path.join(OBS, 'obs-%d.json' % w)
        if os.environ.get('WRITE'):
            with open(path, 'w', encoding='utf-8') as f:
                f.write(json.dumps(got, separators=(',', ':')))
            print(w, 'written'); continue
        want = boxes(json.load(open(path, encoding='utf-8')))
        have = boxes(got)
        missing = sorted(set(want) ^ set(have))
        dev, where = 0.0, None
        for k in set(want) & set(have):
            d = max(abs(a - b) for a, b in zip(want[k], have[k]))
            if d > dev:
                dev, where = d, k
        ok = not missing and dev <= tol
        bad += not ok
        print(w, 'max deviation %.1f' % dev, where or '', ('missing ' + str(missing[:4])) if missing else '', 'ok' if ok else 'FAIL')
    if not os.environ.get('WRITE'):
        print('obstacles ok' if not bad else 'obstacles FAIL: %d width(s)' % bad)
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
