"""Delivery map of the homepage (slice S9, delivery variant 1 "route met bestelwagen"; plan S9 layers).

Ported from the prototype builder (.impeccable/tools/levering/build_levering.py + v1chunk.py, variant 1) so the
build draws the approved map: real geography in a 1000x820 viewBox (40 units per km, coast along the top), seeded
engraving (waves, dunes, polder ditches), roads, the compass rose, the route and the electric van. With the towns of
src/data/towns.json the output is identical to the approved final.html map (tests pin its hash).

The route is fixed artwork drawn through the delivery towns in one order; route_check() fails the build when a
town's map point (towns.json "map") is no longer on it, so moving a town means redrawing ROUTE.
"""
import functools
import math
import random

# ---------------------------------------------------------------- geography
COAST = "M0 377C50 330 100 290 144 262C280 200 430 160 569 120C650 96 720 70 780 48C820 36 860 28 889 24C930 18 970 13 1000 10"
VAART = "M410 742C470 670 520 600 566 556C650 470 760 380 846 300"
BOUDEWIJN = "M398 730C385 600 352 400 333 204"
ROUTE = "M625 280C640 230 575 190 569 133C640 120 870 180 850 293C760 330 660 470 561 550C540 640 410 640 403 737C300 760 130 470 144 275"
ROUTE_SEGS = [((625, 280), (640, 230), (575, 190), (569, 133)), ((569, 133), (640, 120), (870, 180), (850, 293)),
              ((850, 293), (760, 330), (660, 470), (561, 550)), ((561, 550), (540, 640), (410, 640), (403, 737)),
              ((403, 737), (300, 760), (130, 470), (144, 275))]
COAST_SEGS = [((0, 377), (50, 330), (100, 290), (144, 262)), ((144, 262), (280, 200), (430, 160), (569, 120)),
              ((569, 120), (650, 96), (720, 70), (780, 48)), ((780, 48), (820, 36), (860, 28), (889, 24)),
              ((889, 24), (930, 18), (970, 13), (1000, 10))]
V1_START = 46  # route units: the van waits just outside the Westkapelle medallion (js/home.js reads data-start)
MAP_W, MAP_H = 1000, 820


def pct(x, y):
    """CSS position of a map point: '--x:62.50%;--y:34.15%'."""
    return f"--x:{x / 10:.2f}%;--y:{y / 8.2:.2f}%"


def bez(seg, t):
    (x0, y0), (x1, y1), (x2, y2), (x3, y3) = seg
    u = 1 - t
    return (u**3*x0 + 3*u*u*t*x1 + 3*u*t*t*x2 + t**3*x3, u**3*y0 + 3*u*u*t*y1 + 3*u*t*t*y2 + t**3*y3)


def polyline(segs, n=60):
    pts = []
    for s in segs:
        for i in range(n):
            pts.append(bez(s, i / n))
    pts.append(segs[-1][3])
    return pts


def resample(pts, step):
    out, acc = [pts[0]], 0.0
    for a, b in zip(pts, pts[1:]):
        d = math.dist(a, b)
        while acc + d >= step:
            t = (step - acc) / d
            a = (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)
            out.append(a)
            d = math.dist(a, b)
            acc = 0.0
        acc += d
    return out


def point_along(segs, length):
    pts = polyline(segs, 200)
    acc = 0.0
    for a, b in zip(pts, pts[1:]):
        d = math.dist(a, b)
        if acc + d >= length:
            t = (length - acc) / d
            return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)
        acc += d
    return pts[-1]


COAST_LINE = resample(polyline(COAST_SEGS), 4)


def coast_y(x):
    best = min(COAST_LINE, key=lambda p: abs(p[0] - x))
    return best[1]


def coast_xy(y):
    best = min(COAST_LINE, key=lambda p: abs(p[1] - y))
    return best[0]


def waves(step=12, seed=7):
    """fine engraved wave lines in the sea."""
    rnd = random.Random(seed)
    out = []
    y = 10
    while y < 368:
        x_end = coast_xy(y) - 12
        x = 6 + rnd.random() * 20
        if x_end - x > 24:
            d = f"M{x:.0f} {y:.1f}"
            amp = rnd.uniform(1.1, 1.9)
            seg = rnd.uniform(13, 18)
            k = 0
            while x + seg < x_end:
                d += f"q{seg/2:.1f} {(-amp if k % 2 == 0 else amp):.1f} {seg:.1f} 0"
                x += seg
                k += 1
            out.append(f'<path d="{d}"/>')
        y += step + rnd.uniform(-1.5, 1.5)
    return "".join(out)


def dunes(seed=9):
    """a scalloped dune band and marram ticks just inland of the coast."""
    rnd = random.Random(seed)
    pts = resample(polyline(COAST_SEGS), 15)
    bumps, ticks = [], []
    for a, b in zip(pts, pts[1:]):
        dx, dy = b[0] - a[0], b[1] - a[1]
        ln = math.hypot(dx, dy) or 1
        nx, ny = -dy / ln, dx / ln
        if ny < 0:
            nx, ny = -nx, -ny
        off = 7 + rnd.uniform(-1, 1.5)
        ax, ay = a[0] + nx * off, a[1] + ny * off
        bx, by = b[0] + nx * off, b[1] + ny * off
        h = rnd.uniform(3.5, 6.5)
        cx, cy = (ax + bx) / 2 - nx * h, (ay + by) / 2 - ny * h
        bumps.append(f"M{ax:.1f} {ay:.1f}Q{cx:.1f} {cy:.1f} {bx:.1f} {by:.1f}")
        if rnd.random() < .55:
            tx, ty = (ax + bx) / 2 + nx * rnd.uniform(9, 15), (ay + by) / 2 + ny * rnd.uniform(9, 15)
            ticks.append(f"M{tx:.1f} {ty:.1f}l{-2 + rnd.uniform(-1, 1):.1f} {-5:.1f}M{tx+3:.1f} {ty:.1f}l{1 + rnd.uniform(-1, 1):.1f} {-5.5:.1f}")
    beach = " ".join(f"{'M' if i == 0 else 'L'}{p[0]-0:.1f} {p[1]-4.5:.1f}" for i, p in enumerate(resample(polyline(COAST_SEGS), 12)))
    return "".join(bumps), "".join(ticks), beach


def polder(n=120, seed=13):
    rnd = random.Random(seed)
    out, tries = [], 0
    while len(out) < n and tries < 6000:
        tries += 1
        x, y = rnd.uniform(15, 985), rnd.uniform(40, 812)
        if y < coast_y(x) + 34:
            continue
        ln = rnd.uniform(24, 60)
        a = rnd.choice([-0.42, -0.36, 1.15, 1.2, 0.05, -0.4])
        out.append(f'<path d="M{x:.0f} {y:.0f}l{math.cos(a)*ln:.0f} {math.sin(a)*ln:.0f}"/>')
    return "".join(out)


def rose():
    """antique compass rose, engraved: rings, fine rays, an eight-point star, N."""
    rays = "".join(
        f'<path d="M{math.sin(math.radians(a))*10:.1f} {-math.cos(math.radians(a))*10:.1f}L{math.sin(math.radians(a))*40:.1f} {-math.cos(math.radians(a))*40:.1f}"/>'
        for a in range(0, 360, 360 // 32))
    star = []
    for i, a in enumerate(range(0, 360, 45)):
        long = i % 2 == 0
        r, w = (38, 7) if long else (24, 5)
        ra = math.radians(a)
        tip = (math.sin(ra) * r, -math.cos(ra) * r)
        l = (math.sin(ra - math.pi / 2) * w, -math.cos(ra - math.pi / 2) * w)
        rr = (math.sin(ra + math.pi / 2) * w, -math.cos(ra + math.pi / 2) * w)
        star.append(f'<path class="r-dark" d="M0 0L{l[0]:.1f} {l[1]:.1f}L{tip[0]:.1f} {tip[1]:.1f}Z"/>'
                    f'<path class="r-light" d="M0 0L{rr[0]:.1f} {rr[1]:.1f}L{tip[0]:.1f} {tip[1]:.1f}Z"/>')
    star = star[1::2] + star[0::2]  # long points drawn on top
    ticks = "".join(
        f'<path d="M{math.sin(math.radians(a))*43:.1f} {-math.cos(math.radians(a))*43:.1f}L{math.sin(math.radians(a))*(47 if a % 90 == 0 else 45):.1f} {-math.cos(math.radians(a))*(47 if a % 90 == 0 else 45):.1f}"/>'
        for a in range(0, 360, 10))
    return (f'<g class="lv1-rose-in"><circle class="r-ring" r="47"/><circle class="r-ring r-thin" r="43"/><circle class="r-ring r-thin" r="28"/>'
            f'<g class="r-rays">{rays}</g><g class="r-ticks">{ticks}</g>{"".join(star)}<circle class="r-hub" r="3"/>'
            f'<text class="r-n" y="-53">N</text></g>')


# ---------------------------------------------------------------- the van (side view, faces right)
BODY = ("M14 96C11 80 11 46 14 32C16 22 24 16.5 38 16L150 14.5C164 14.5 172 18 178 26"
        "C186 38 194 51 199 61C204 69 206 77 206 86L206 92C206 96 203 98 199 98L18 98.5C16 98.5 14.5 97.5 14 96Z")


def van_svg(pid):
    def wheel(cx):
        return (f'<g class="v-wheel"><circle class="v-tyre" cx="{cx}" cy="98" r="15"/>'
                f'<circle class="v-hub" cx="{cx}" cy="98" r="8"/>'
                f'<path class="v-spoke" d="M{cx} 91V105M{cx-6.1} 94.5L{cx+6.1} 101.5M{cx-6.1} 101.5L{cx+6.1} 94.5"/></g>')
    return f'''<svg class="lv-van-svg" viewBox="0 0 220 116" aria-hidden="true" focusable="false">
<defs><clipPath id="{pid}-vc"><path d="{BODY}"/></clipPath></defs>
<path class="v-cream" d="{BODY}"/>
<path class="v-low" clip-path="url(#{pid}-vc)" d="M0 60C70 61.5 140 58.5 168 60C184 61 194 68 210 77V116H0Z"/>
<path class="v-belt" d="M13 60C70 61.5 140 58.5 168 60C182 61 193 67.5 205 75"/>
<path class="v-glass" d="M24 24C22 32 22 44 24.5 51.5L168 52.5L168.5 23.5C120 23 70 23.2 24 24Z"/>
<g class="v-crates"><rect x="28" y="41.5" width="13" height="10" rx="1"/><rect x="42" y="41.5" width="13" height="10" rx="1"/>
<circle class="m-gele" cx="32" cy="40" r="3"/><circle class="m-roze" cx="37.5" cy="39.4" r="3"/><circle class="m-blauwe" cx="46" cy="40" r="3"/><circle class="m-witte" cx="51.5" cy="39.4" r="3"/></g>
<path class="v-pillar" d="M62 23.5V52.5M108 23.3V52.5M142 23.3V52.5"/>
<path class="v-glass" d="M173 23C181 31 189 43 195.5 56L173 55Z"/>
<path class="v-seam" d="M108 58V90M146 56V90M100 66h5"/>
<path class="v-bar-ink" d="M185 66.5C193 67 200 69 204.5 71.5"/><path class="v-bar" d="M185 66.5C193 67 200 69 204.5 71.5"/>
<path class="v-tail" d="M13.5 63V75"/>
<path class="v-line" d="{BODY}"/>
<path class="v-arch" d="M23 98.5A19 19 0 0 1 61 98.5Z"/>
<path class="v-arch" d="M157 98.5A19 19 0 0 1 195 98.5Z"/>
{wheel(42)}{wheel(176)}
<g class="v-word"><text class="v-text" x="109" y="83">GroMush</text></g>
</svg>'''




@functools.lru_cache(maxsize=1)
def van_start():
    """(x, y) of the parked van, in map units."""
    return point_along(ROUTE_SEGS, V1_START)


def van_style():
    x, y = van_start()
    return f"--vx:{x / 10:.2f}%;--vy:{y / 8.2:.2f}%"


def route_check(points, tolerance=2.0):
    """Names of the map points [(name, x, y)] that are not on the drawn route (within tolerance map units)."""
    line = polyline(ROUTE_SEGS, 120)
    return [n for n, x, y in points if min(math.dist((x, y), p) for p in line) > tolerance]


def route_pos(x, y):
    """Share of the route (0..1) at the point nearest to (x, y): orders the stops as the van meets them."""
    line = polyline(ROUTE_SEGS, 120)
    best = min(range(len(line)), key=lambda i: math.dist((x, y), line[i]))
    return best / (len(line) - 1)


@functools.lru_cache(maxsize=4)
def map_svg(stops):
    """The map (svg.lv1-svg). stops: tuple of (x, y, home) map points; home draws the ringed start dot."""
    dots = []
    for x, y, home in stops:
        if home:
            dots.append(f'<circle class="lv1-ring" cx="{x}" cy="{y}" r="19"/><circle class="lv1-home" cx="{x}" cy="{y}" r="10"/>')
        else:
            dots.append(f'<circle class="lv1-dot" cx="{x}" cy="{y}" r="8.5"/>')
    bumps, ticks, beach = dunes()
    leopold = "M447 160C500 230 540 300 575 400C600 470 612 520 640 600C670 690 700 760 730 820"
    schipdonk = "M459 156C512 226 552 296 587 396C612 466 624 516 652 596C682 686 712 756 742 820"
    zwin = "M776 50C772 66 786 78 782 94C779 108 794 118 806 132C818 146 812 162 826 178"
    zwin_creeks = "M782 94C792 90 800 96 808 92M806 132C796 136 790 146 780 148M789 74C798 70 806 76 816 70"
    return f'''<svg class="lv1-svg" viewBox="0 0 1000 820" aria-hidden="true" focusable="false">
            <g class="lv1-waves">{waves()}</g>
            <g class="lv1-polder">{polder()}</g>
            <path class="lv1-beach" d="{beach}"/>
            <path class="lv1-coast" d="{COAST}"/>
            <path class="lv1-dune" d="{bumps}"/><path class="lv1-grass" d="{ticks}"/>
            <path class="lv1-wb" d="{zwin}"/><path class="lv1-ww" d="{zwin}"/><path class="lv1-creek" d="{zwin_creeks}"/>
            <path class="lv1-cb" d="{leopold}"/><path class="lv1-cb" d="{schipdonk}"/>
            <path class="lv1-wb" d="{VAART}"/><path class="lv1-ww" d="{VAART}"/>
            <path class="lv1-cb" d="{BOUDEWIJN}"/>
            <g class="lv1-roads">
              <path class="r-main" d="M150 268C280 215 430 170 565 135"/><path class="r-main-in" d="M150 268C280 215 430 170 565 135"/>
              <path class="r-main" d="M405 735C450 600 560 420 625 282C610 220 590 170 570 135"/><path class="r-main-in" d="M405 735C450 600 560 420 625 282C610 220 590 170 570 135"/>
              <path class="r-minor" d="M400 737C320 600 220 420 146 278"/>
              <path class="r-minor" d="M626 282C700 285 780 300 848 294"/>
              <path class="r-minor" d="M563 548C640 520 720 470 790 520C830 548 870 600 920 640"/>
              <path class="r-minor" d="M565 135C640 115 720 90 790 62"/>
            </g>
            <g class="lv1-rose" transform="translate(292 58) scale(.8)"><g class="lv1-rose-turn">{rose()}</g></g>
            <text class="lv1-zee" x="592" y="96" transform="rotate(-17 592 96)">Noordzee</text>
            <path class="lv1-road" d="{ROUTE}"/>
            <path class="lv1-route" d="{ROUTE}"/>
            {"".join(dots)}
          </svg>'''
