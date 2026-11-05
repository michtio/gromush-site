"""Hyphae network of the homepage's radial opening (plan AD13, PRD R10, R10a, R12; slice S9).

Ported from the approved round-4 prototype generator (.impeccable/tools/radiaal/gen.py, approved by Michael
on 2026-11-04). The build calls ring_svg() and medallions(); the generated paths go into the page fully grown, so
no-JS and reduced motion show the complete network (R12) and js/home.js only animates them. With all six varieties
in the range the output is byte-identical to the approved artwork (tests pin its hash).

Obstacles: src/gen/hyphae_obs/obs-<width>.json, measured in ring-svg units (viewBox 1320x780) from the opening's
layout by .impeccable/tools/radiaal/measure.js (title, intro, slip with tape and note, curved-label glyphs, pills,
discs). They depend on the layout and on each variety's name (one glyph box per letter): after a change to either,
re-measure them (see measure.js) and check the collision probes, or the network may cross a label.

A variety taken out of the range (in_range false) loses its medallion and its main; the network is then regenerated
without them (deterministic, but no longer the approved drawing: re-run the probes).

Original notes (unchanged growth model):
Growth model
- Six mains (class m, data-v) run in smooth curves from the title block to each medallion's
  ring; a thicker underlay (class mb) tapers their first half.
- The web: strands fork off existing strands at 14-37 deg, from a point jittered along the
  parent, preferring fork points near the medallions and the mains. Their heading drifts
  slowly (low-frequency, capped turn per step, so long gentle arcs and no zig-zag) and is pulled
  gently outward, away from the title block, each strand with its own lean; the pull ramps in
  over the first FLOW_IN units so a fresh fork opens away from its parent before it bends.
  An obstacle ahead is skirted gradually (look-ahead), so strands curve round the medallions
  into the paper behind them. No two forks leave within ORIGIN_R of each other at an opening
  angle under SIB (that stacking made feather-like tufts in round 2); a strand that draws
  alongside another (within ALONG units, under PAR) bends towards it and stops against it.
  A strand that meets another at a wide angle always fuses (anastomosis, no hatching); a
  shallow meeting fuses after FUSE_AFTER units and otherwise grows on over it. A strand also
  ends at an obstacle or, more readily the further it is from the medallions and the nearer the
  paper's edge, dies, so the mesh thins outward. Nothing grows in the bands above the title or
  below the slip. Round 4 (softening): see softness.py for the measures (turn, flow, cross).
- Timing: every strand starts at the network distance where its parent passes the fork
  (data-a) and ends at data-a + its length (data-b). Mains and the longer strands (class s)
  are drawn with a dash; the fine web (classes f1-f3, 0.3-0.65) is merged per stroke class
  and start bucket into a few path elements that fade in (data-f), which keeps the markup small.
- Path data: integer relative cubics with smooth `s` continuations (Catmull-Rom is C1, so the
  reflected control point is exact up to rounding); every emitted curve is re-checked against
  the bare obstacles and shortened if it would touch one.
"""
import functools, glob, json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OBS_DIR = os.path.join(HERE, 'hyphae_obs')
VW, VH = 1320, 780
FRAME = 6
PAD_CORE, PAD_GLYPH, PAD_PILL, PAD_DISC = 12, 6, 6, 7
BANDS = {'s': (1100, 1279), 'l': (1280, 1920)}
# arrival angle on the ring (deg, screen coords), side of the block, height on it (share)
MAIN = {
    'grijze': (12, 'l', .34), 'roze': (0, 'l', .5), 'blauwe': (24, 'l', .72),
    'witte': (168, 'r', .34), 'gele': (180, 'r', .5), 'italiaanse': (156, 'r', .72),
}
STRANDS = {'s': 1100, 'l': 1180}  # web strands per network (ink at or above r2's, see softness.py)
FORK = (.25, .65)      # fork angle off the parent (rad), either side
WANT = (110, 380)      # intended strand length before it dies, fuses or meets an obstacle
DRIFT = (.95, .012, .05)  # heading drift: memory, noise per 4-unit step, cap (rad per step)
FLOW = .07             # pull per step towards the outward direction (away from the title block)
FLOW_IN = 30           # run over which that pull ramps in
LEAN = math.radians(15)  # per-strand offset of that outward direction
STEER, LOOK = .08, 16   # obstacle look-ahead: max turn per step, distance
WIDE = math.radians(40)  # a strand meeting another at more than this always fuses (no hatching)
FUSE_AFTER = 30        # a shallow meeting fuses only after this run (before it, it crosses over)
FUSE_P = 1.0           # chance such a meeting after FUSE_AFTER fuses rather than crossing over
SIB = math.radians(28)  # min opening-angle gap between fork origins closer than ORIGIN_R
ORIGIN_R = 16
PAR = math.radians(15)  # "alongside" = within ALONG units at a heading gap under this
ALONG = 7               # see PAR
STOP_ALONG = 5          # a strand this close alongside another stops (contact), 0 = off
EV_S, EV_F = 22, 26      # spline knot spacing for strands and fine web
FADE_BUCKET = 40       # network-distance bucket for merged fine strands
TM = {}                # tuft metrics per band, filled by build()


def union(rects):
    return [min(r[0] for r in rects), min(r[1] for r in rects), max(r[2] for r in rects), max(r[3] for r in rects)]


def pad(r, p):
    return [r[0] - p, r[1] - p, r[2] + p, r[3] + p]


def angdiff(a, b):
    return (a - b + math.pi) % (2 * math.pi) - math.pi


def length(pts):
    return sum(math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1))


# ---------- curves ----------
def R(p):
    return (int(round(p[0])), int(round(p[1])))


def spline(pts, every):
    """Catmull-Rom through points ~`every` units apart, as rounded segments; returns the exact
    rendered cubics [(p0, c1, c2, p1)] and the path data (c, then s continuations)."""
    keep, run = [pts[0]], 0.0
    for i in range(1, len(pts)):
        run += math.dist(pts[i - 1], pts[i])
        if run >= every:
            keep.append(pts[i]); run = 0.0
    if keep[-1] != pts[-1]:
        if math.dist(keep[-1], pts[-1]) < every * .4 and len(keep) > 2:
            keep[-1] = pts[-1]
        else:
            keep.append(pts[-1])
    if len(keep) == 2:
        keep = [keep[0], ((keep[0][0] + keep[1][0]) / 2, (keep[0][1] + keep[1][1]) / 2), keep[1]]
    cur = R(keep[0])
    d, cubics, prev_c2 = 'M%d %d' % cur, [], None
    for i in range(len(keep) - 1):
        p0 = keep[i - 1] if i else keep[i]
        p1, p2 = keep[i], keep[i + 1]
        p3 = keep[i + 2] if i + 2 < len(keep) else p2
        c2 = R((p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6))
        e = R(p2)
        if prev_c2 is None:
            c1 = R((p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6))
            nums, cmd = [c1[0] - cur[0], c1[1] - cur[1], c2[0] - cur[0], c2[1] - cur[1], e[0] - cur[0], e[1] - cur[1]], 'c'
        else:
            c1 = (2 * cur[0] - prev_c2[0], 2 * cur[1] - prev_c2[1])
            nums, cmd = [c2[0] - cur[0], c2[1] - cur[1], e[0] - cur[0], e[1] - cur[1]], 's'
        seg = ''
        for n in nums:
            seg += ('%d' % n) if (n < 0 or not seg) else (' %d' % n)
        d += cmd + seg
        cubics.append((cur, c1, c2, e))
        prev_c2, cur = c2, e
    return cubics, d


def bez(c, t):
    (p0, c1, c2, p1), u = c, 1 - t
    return (u*u*u*p0[0] + 3*u*u*t*c1[0] + 3*u*t*t*c2[0] + t*t*t*p1[0],
            u*u*u*p0[1] + 3*u*u*t*c1[1] + 3*u*t*t*c2[1] + t*t*t*p1[1])


def tuft_metrics(strands):
    """Tuft measures over the web strands (mains excluded).
    pairs: strand pairs whose origins lie within 12 units and whose opening headings (over the
      first ~16 units) differ by less than 12 deg: near-parallel siblings from one point.
    par: share of web length (sampled every 4 units, first 8 units after each fork skipped) that
      runs within 6 units of another web strand at a heading difference under 12 deg.
    ink: total web length (density reference)."""
    web = [h['pts'] for h in strands if h['cls'] != 'm']
    heads = []
    for pts in web:
        k = min(len(pts) - 1, 4)
        heads.append((pts[0], math.atan2(pts[k][1] - pts[0][1], pts[k][0] - pts[0][0])))
    og = {}
    for i, (o, a) in enumerate(heads):
        og.setdefault((int(o[0] // 12), int(o[1] // 12)), []).append(i)
    pairs = 0
    for i, (o, a) in enumerate(heads):
        gx, gy = int(o[0] // 12), int(o[1] // 12)
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                for j in og.get((gx + dx, gy + dy), ()):
                    if j > i and math.dist(o, heads[j][0]) < 12 and abs(angdiff(a, heads[j][1])) < math.radians(12):
                        pairs += 1
    samp, g = [], {}
    for si, pts in enumerate(web):
        run = 0.0
        for j in range(1, len(pts) - 1):
            run += math.dist(pts[j - 1], pts[j])
            if run < 8 or j % 1:
                continue
            a = math.atan2(pts[j + 1][1] - pts[j - 1][1], pts[j + 1][0] - pts[j - 1][0])
            samp.append((si, pts[j], a))
            g.setdefault((int(pts[j][0] // 6), int(pts[j][1] // 6)), []).append(len(samp) - 1)
    hit = 0
    for (si, p, a) in samp:
        gx, gy = int(p[0] // 6), int(p[1] // 6)
        found = False
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                for k in g.get((gx + dx, gy + dy), ()):
                    sj, q, b = samp[k]
                    if sj != si and math.dist(p, q) < 6 and abs(angdiff(a, b)) < math.radians(12) \
                            and abs(angdiff(a + math.pi, b)) > 0:
                        found = True
                        break
                if found:
                    break
            if found:
                break
        hit += found
    ink = sum(length(p) for p in web)
    return {'pairs': pairs, 'par': round(hit / max(1, len(samp)), 3), 'ink': round(ink), 'web': len(web)}


def build(band, obs, seed):
    rng = random.Random(seed)
    TM.pop(band, None)
    core = {k: union([o['core'][k] for o in obs]) for k in obs[0]['core']}
    core_rects = [pad(r, PAD_CORE) for r in core.values()]
    meds = {}
    for k, m0 in obs[0]['meds'].items():
        glyphs = [pad(union([o['meds'][k]['glyphs'][i] for o in obs]), PAD_GLYPH) for i in range(len(m0['glyphs']))]
        meds[k] = {'c': m0['c'], 'r': max(o['meds'][k]['r'] for o in obs), 'glyphs': glyphs,
                   'pill': pad(union([o['meds'][k]['pill'] for o in obs]), PAD_PILL)}
    rects = core_rects + [g for m in meds.values() for g in m['glyphs']] + [m['pill'] for m in meds.values()]
    names = list(meds.keys())
    discs = [(meds[k]['c'][0], meds[k]['c'][1], meds[k]['r'] + PAD_DISC) for k in names]
    cx0, cx1 = min(r[0] for r in core_rects), max(r[2] for r in core_rects)
    cy0, cy1 = min(r[1] for r in core_rects), max(r[3] for r in core_rects)
    CX, CY = (cx0 + cx1) / 2, (cy0 + cy1) / 2

    def free(x, y, skip=None):
        if x < FRAME or y < FRAME or x > VW - FRAME or y > VH - FRAME:
            return False
        # no strands in the bands straight above the title or below the slip
        if cx0 < x < cx1 and (y < cy0 or y > cy1):
            return False
        for r in rects:
            if r[0] < x < r[2] and r[1] < y < r[3]:
                return False
        for i, (cx, cy, rr) in enumerate(discs):
            if i == skip:
                rr -= PAD_DISC - 2
            if (x - cx) ** 2 + (y - cy) ** 2 < rr * rr:
                return False
        return True

    def seg_free(a, b, skip=None):
        n = max(1, int(math.dist(a, b) / 1.5))
        return all(free(a[0] + (b[0] - a[0]) * i / n, a[1] + (b[1] - a[1]) * i / n, skip) for i in range(n + 1))

    def side_x(y, side):
        xs = [r[0] if side == 'l' else r[2] for r in core_rects if r[1] <= y <= r[3]]
        return (min(xs) - 2) if side == 'l' else (max(xs) + 2)

    def density(p):
        """1 on a ring, falling off with distance from the nearest medallion."""
        d = min(math.dist(p, m['c']) - m['r'] for m in meds.values())
        f = 1.0
        if p[1] < cy0 or p[1] > cy1:
            # above the title and below the slip the web thins out softly, so strands
            # die away before the open band instead of stopping on a line
            f = min(1.0, max(0.0, max(cx0 - p[0], p[0] - cx1) / 150)) ** 1.5
        return math.exp(-max(0.0, d) / 130) * f

    strands = []          # {pts, a, cls, v?}
    grid = {}             # spatial hash of strand points, for fusing

    def index(si, pts):
        for j, p in enumerate(pts):
            grid.setdefault((int(p[0] // 6), int(p[1] // 6)), []).append((si, j, p))

    def near(p, own, parent):
        gx, gy = int(p[0] // 6), int(p[1] // 6)
        best = None
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                for (si, j, q) in grid.get((gx + dx, gy + dy), ()):
                    if si in (own, parent):
                        continue
                    dd = math.dist(p, q)
                    if dd < 3.5 and (best is None or dd < best[0]):
                        best = (dd, q, si, j)
        return best

    # ---------- mains ----------
    for k, (deg, side, fy) in MAIN.items():
        if k not in meds:
            continue
        m, di = meds[k], names.index(k)
        y0 = core['h1'][1] + (core['slip'][3] - core['h1'][1]) * fy
        S = (side_x(y0, side), y0)
        th = math.radians(deg)
        T = (m['c'][0] + (m['r'] + 3) * math.cos(th), m['c'][1] + (m['r'] + 3) * math.sin(th))
        best, tries = None, 0
        while tries < 1500 and (best is None or tries < 160):
            tries += 1
            pts, om = [S], 0.0
            ang = math.atan2(T[1] - S[1], T[0] - S[0]) + rng.uniform(-.5, .5)
            ok = False
            for _ in range(300):
                P = pts[-1]
                if math.dist(P, T) < 8:
                    ok = seg_free(P, T, di)
                    pts.append(T)
                    break
                want = math.atan2(T[1] - P[1], T[0] - P[0])
                om = om * .85 + rng.uniform(-.025, .025)
                ang += om + max(-.12, min(.12, angdiff(want, ang) * .12))
                q = (P[0] + 4 * math.cos(ang), P[1] + 4 * math.sin(ang))
                if not seg_free(P, q, di):
                    break
                pts.append(q)
            if ok:
                score = abs(length(pts) / math.dist(S, T) - 1.08)
                if best is None or score < best[0]:
                    best = (score, pts)
        if best is None:
            raise ValueError('hyphae: no main for %s in band %s' % (k, band))
        strands.append({'pts': best[1], 'a': 0.0, 'cls': 'm', 'v': k, 'skip': di})
        index(len(strands) - 1, best[1])

    # ---------- the web ----------
    cands = {'l': [], 'r': []}   # fork candidates per side: (weight, strand, point index, run)

    def add_cands(si):
        pts, run = strands[si]['pts'], 0.0
        main = strands[si]['cls'] == 'm'
        for j in range(1, len(pts) - 1):
            run += math.dist(pts[j - 1], pts[j])
            if j % 2:
                continue
            w = density(pts[j]) * (1.4 if main else 1.0) + .04
            cands['l' if pts[j][0] < CX else 'r'].append((w, si, j, run))

    for si in range(len(strands)):
        add_cands(si)

    def heading(pts, j):
        a, b = pts[max(0, j - 1)], pts[min(len(pts) - 1, j + 1)]
        return math.atan2(b[1] - a[1], b[0] - a[0])

    def alongside(p, a, own, parent, r):
        """Nearest point of another strand within r that runs within PAR_DEG of heading a
        (either direction), as (distance, point) or None."""
        gx, gy, best = int(p[0] // 6), int(p[1] // 6), None
        span = int(r // 6) + 1
        for dx in range(-span, span + 1):
            for dy in range(-span, span + 1):
                for (si, j, q) in grid.get((gx + dx, gy + dy), ()):
                    if si in (own, parent):
                        continue
                    dd = math.dist(p, q)
                    if dd < r and (best is None or dd < best[0]):
                        b = heading(strands[si]['pts'], j)
                        if min(abs(angdiff(a, b)), abs(angdiff(a + math.pi, b))) < PAR:
                            best = (dd, q)
        return best

    origins = {}          # fork origins (point, opening heading), for sibling separation

    def crowded(P, a):
        gx, gy = int(P[0] // ORIGIN_R), int(P[1] // ORIGIN_R)
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                for (q, b) in origins.get((gx + dx, gy + dy), ()):
                    if math.dist(P, q) < ORIGIN_R and abs(angdiff(a, b)) < SIB:
                        return True
        return False

    made, attempts = 0, 0
    while made < STRANDS[band] and attempts < STRANDS[band] * 14:
        attempts += 1
        # alternate sides so both halves of the ring carry the same web
        pool = cands['l' if attempts % 2 else 'r']
        w, si, j, run = rng.choices(pool, weights=[c[0] for c in pool])[0]
        par = strands[si]
        pts = par['pts']
        # origin jittered along the parent, between its sample points
        t = rng.random()
        P = (pts[j][0] + (pts[j + 1][0] - pts[j][0]) * t, pts[j][1] + (pts[j + 1][1] - pts[j][1]) * t)
        run += math.dist(pts[j], P)
        h = heading(pts, j)
        ang = h + rng.choice((-1, 1)) * rng.uniform(*FORK)
        # sibling separation: no second strand leaving the same spot at nearly the same angle
        if crowded(P, ang):
            continue
        want = rng.uniform(*WANT)
        out, run2, fused, met = [P], 0.0, False, set()
        mem, noise, cap = DRIFT
        om = rng.uniform(-cap, cap) * .5
        own = len(strands)
        pulled = False
        # each strand leans its own way off the radial direction, so neighbours do not
        # converge onto one heading and bundle
        lean = rng.uniform(-LEAN, LEAN)
        while run2 < want:
            Q = out[-1]
            # slow, low-frequency heading drift: long gentle arcs, no zig-zag
            om = max(-cap, min(cap, om * mem + rng.uniform(-noise, noise)))
            ang += om
            # a slight outward flow, away from the title block
            # (ramped in, so a fresh fork first opens away from its parent instead of being bent
            # straight back alongside it)
            ang += angdiff(math.atan2(Q[1] - CY, Q[0] - CX) + lean, ang) * FLOW * min(1.0, run2 / FLOW_IN)
            # a strand running alongside another bends into it (anastomosis)
            pulled = False
            if run2 > 12:
                side = alongside(Q, ang, own, si, ALONG)
                if side and STOP_ALONG and side[0] < STOP_ALONG:
                    break
                if side:
                    to = math.atan2(side[1][1] - Q[1], side[1][0] - Q[0])
                    ang += max(-.07, min(.07, angdiff(to, ang) * .25))
                    pulled = True
            if run2 > 6:
                # look ahead: an obstacle ahead is skirted, so the strand bends gradually round a
                # medallion into the paper behind it instead of kinking or stopping short
                A = (Q[0] + LOOK * math.cos(ang), Q[1] + LOOK * math.sin(ang))
                if not seg_free(Q, A):
                    fl = [seg_free(Q, (Q[0] + LOOK * math.cos(ang + sg * .5), Q[1] + LOOK * math.sin(ang + sg * .5))) for sg in (-1, 1)]
                    if fl[0] != fl[1]:
                        ang += STEER * (1 if fl[1] else -1)
            step = 4.0
            nxt = None
            for dv in (0, .06, -.06, .12, -.12):
                a2 = ang + dv
                c = (Q[0] + step * math.cos(a2), Q[1] + step * math.sin(a2))
                if seg_free(Q, c):
                    nxt, ang = c, a2
                    break
            if nxt is None:
                break
            out.append(nxt)
            run2 += step
            # thin toward the edges: a strand far from the medallions ends sooner
            edge = min(nxt[0], nxt[1], VW - nxt[0], VH - nxt[1]) - FRAME
            if rng.random() < .004 + .04 * (1 - density(nxt)) ** 2 + max(0.0, 1 - edge / 40) * .1:
                break
            if run2 > 16:
                hit = near(nxt, own, si)
                # a strand that drew alongside always fuses; one that crosses another strand
                # fuses now and then and otherwise grows on over it (once per strand met)
                if hit and hit[2] not in met:
                    met.add(hit[2])
                    hb = heading(strands[hit[2]]['pts'], hit[3])
                    wide = abs(math.sin(angdiff(hb, ang))) > math.sin(WIDE)
                    if pulled or wide or (run2 > FUSE_AFTER and rng.random() < FUSE_P):
                        out.append(hit[1]); fused = True
                        break
        L = length(out)
        if L < 18:
            continue
        if L > 110 and rng.random() < .3:
            cls = 's'
        else:
            cls = rng.choices(('f3', 'f2', 'f1'), weights=(.25, .35, .4))[0]
        k = min(len(out) - 1, 4)
        a0 = math.atan2(out[k][1] - out[0][1], out[k][0] - out[0][0])
        origins.setdefault((int(P[0] // ORIGIN_R), int(P[1] // ORIGIN_R)), []).append((P, a0))
        strands.append({'pts': out, 'a': par['a'] + run, 'cls': cls, 'fused': fused})
        index(own, out)
        add_cands(own)
        made += 1

    # ---------- emit, re-checking the rendered curves against the bare obstacles ----------
    hard_rects = [pad(r, 1 - PAD_CORE) for r in core_rects] + \
        [pad(g, 1 - PAD_GLYPH) for m in meds.values() for g in m['glyphs']] + [pad(m['pill'], 1 - PAD_PILL) for m in meds.values()]
    hard_discs = [(cx, cy, rr - PAD_DISC + 1) for (cx, cy, rr) in discs]

    def clear(cubics):
        for c in cubics:
            for i in range(1, 13):
                x, y = bez(c, i / 12)
                if any(r[0] < x < r[2] and r[1] < y < r[3] for r in hard_rects):
                    return False
                if any((x - cx) ** 2 + (y - cy) ** 2 < rr * rr for (cx, cy, rr) in hard_discs):
                    return False
        return True

    EVERY = {'m': 12, 's': EV_S, 'f3': EV_F, 'f2': EV_F, 'f1': EV_F}
    out = []
    for h in strands:
        pts = h['pts']
        while True:
            cubics, d = spline(pts, EVERY[h['cls']])
            if clear(cubics):
                break
            if h['cls'] == 'm':
                raise ValueError('hyphae: main %s touches an obstacle' % h['v'])
            pts = pts[:-3]
            if len(pts) < 5:
                d = None
                break
        if d:
            out.append({'d': d, 'a': h['a'], 'b': h['a'] + length(pts), 'cls': h['cls'], 'v': h.get('v'),
                        'half': spline(pts[:len(pts) // 2 + 1], 12)[1] if h['cls'] == 'm' else None,
                        'hb': h['a'] + length(pts[:len(pts) // 2 + 1])})
    TM[band] = tuft_metrics(strands)
    return out


def load_obs(keys):
    """Measured obstacles per width, restricted to the medallions in keys (variety keys in the range)."""
    files = {int(re.search(r'obs-(\d+)', f).group(1)): f for f in glob.glob(os.path.join(OBS_DIR, 'obs-*.json'))}
    out = {}
    for w, f in sorted(files.items()):
        with open(f, encoding='utf-8') as fh:
            o = json.load(fh)
        o['meds'] = {k: v for k, v in o['meds'].items() if k in keys}
        out[w] = o
    return out


def medallions(names):
    """Layout of the medallions for the template: [{key, x, y}] in reading order (top row, middle, bottom; left
    before right), x/y as percentages of the ring stage. names: {variety key: canonical name}. Raises ValueError
    for a variety with no measured place, or one whose name no longer matches its measured curved label."""
    obs = load_obs(set(names))
    o = obs[max(obs)]
    unknown = sorted(set(names) - set(o['meds']))
    if unknown:
        raise ValueError('hyphae: no medallion place measured for %s (src/gen/hyphae_obs)' % ', '.join(unknown))
    for k, name in names.items():
        n = len(o['meds'][k]['glyphs'])
        if n != len(name):
            raise ValueError('hyphae: %s is now %r (%d letters) but its curved label was measured with %d; '
                             're-measure src/gen/hyphae_obs (measure.js) and re-run the probes' % (k, name, len(name), n))
    out = [{'key': k, 'x': '%.3f%%' % (m['c'][0] / VW * 100), 'y': '%.3f%%' % (m['c'][1] / VH * 100)}
           for k, m in o['meds'].items()]
    return sorted(out, key=lambda m: (float(m['y'][:-1]), float(m['x'][:-1])))


@functools.lru_cache(maxsize=4)
def ring_svg(keys):
    """The baked networks (inner SVG of .ring-svg): a blur filter, then group "s" (1100-1279 px) and "l" (1280 px
    up), each with the mains, longer strands, merged fine web and the feathered knock-out plates. keys: a frozenset
    of the variety keys in the range."""
    obs_all = load_obs(set(keys))
    out = ['    <defs><filter id="ring-ko-blur" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="11"/></filter></defs>']
    for band, (lo, hi) in BANDS.items():
        obs = [o for w, o in sorted(obs_all.items()) if lo <= w <= hi]
        items = build(band, obs, 20261104 + (band == 'l'))
        core = {k: union([o['core'][k] for o in obs]) for k in obs[0]['core']}
        out.append('    <g class="ring-hy ring-hy--%s">' % band)
        for h in items:
            if h['cls'] == 'm':
                out.append('      <path class="mb" pathLength="1" data-a="0" data-b="%d" d="%s"/>' % (math.ceil(h['hb']), h['half']))
        fine = {}
        for h in items:
            if h['cls'] in ('m', 's'):
                v = ' data-v="%s"' % h['v'] if h['v'] else ''
                out.append('      <path class="%s"%s pathLength="1" data-a="%d" data-b="%d" d="%s"/>' % (
                    h['cls'], v, round(h['a']), math.ceil(h['b']), h['d']))
            else:
                fine.setdefault((h['cls'], int(h['a'] // FADE_BUCKET)), []).append(h['d'])
        for (cls, bucket), ds in sorted(fine.items(), key=lambda kv: kv[0][1]):
            out.append('      <path class="%s" data-f="%d" d="%s"/>' % (cls, bucket * FADE_BUCKET, ''.join(ds)))
        # knock-out: feathered straw plates over the mains' first steps
        for k in ('h1', 'intro', 'slip'):
            r = core[k]
            out.append('      <rect class="ring-ko" filter="url(#ring-ko-blur)" x="%d" y="%d" width="%d" height="%d" rx="22"/>' % (
                round(r[0] - 2), round(r[1] - 2), round(r[2] - r[0] + 4), round(r[3] - r[1] + 4)))
        out.append('    </g>')
    return '\n'.join(out)


def main():
    """python3 -I src/gen/hyphae.py [page.html]: print size and tuft metrics; with a page, compare its baked
    <!-- RING:START/END --> block (e.g. the prototype final.html) with the generated one."""
    import sys
    block = ring_svg(frozenset(MAIN))
    print('inline svg bytes', len(block.encode()), 'tufts', TM)
    if len(sys.argv) > 1:
        with open(sys.argv[1], encoding='utf-8') as fh:
            m = re.search(r'<!-- RING:START -->\n(.*?)\n<!-- RING:END -->', fh.read(), re.S)
        print('same as baked:', bool(m) and m.group(1) == block)


if __name__ == '__main__':
    main()
