/* GroMush homepage (S9; plan AD13; PRD R10, R10a, R11, R12). Vanilla JS, no library: requestAnimationFrame and
   IntersectionObserver only. Ported from final.html (radial opening round 4, delivery variant 1).
   Progressive: the page is complete without this script. The network (src/gen/hyphae.py) and the delivery route are
   in the markup fully drawn; this script only animates them, and never with prefers-reduced-motion (R12, AC12).
   1. Radial opening (68.75em, 1100 px at the default text size, and up; larger text gets the list): the mains and longer strands carry pathLength="1" and the network distance at
      which they start (data-a) and end (data-b), measured from the title block; the fine web is merged into a few
      paths that fade in from their bucket's distance (data-f). One distance D sweeps the network outward: on load it
      carries the six mains from the title to their medallions, each medallion resolving as its main arrives (AC10),
      and scroll grows the web beyond while the opening holds (pinned). Keyboard focus anywhere in the opening
      completes the drawing at once. Hover or focus on a medallion gives its main branch the variety colour.
   2. Delivery: the route with the van, driven by scroll (a sticky map; the stops appear as the van reaches them).
      A stage taller than the viewport cannot pin and falls back to the static map and register. */
(function () {
  'use strict';
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)');
  var header = document.querySelector('.site-header');

  /* ---------- 1. radial opening ---------- */
  function initRing() {
    var ringPin = document.querySelector('.ring-pin');
    var ring = ringPin && ringPin.querySelector('.ring');
    if (!ring) return;
    var rootEl = document.documentElement;
    var bandMq = window.matchMedia('(min-width: 80em)'); /* 1280 px at 16 px; em, like the CSS */
    var band = null, paths = [], fades = [], mains = {}, dMax = 1, dIntro = 0;
    var meds = [].slice.call(ring.querySelectorAll('.med'));

    /* the visible network (one per width band) */
    function collect() {
      var b = bandMq.matches ? 'l' : 's';
      if (b === band) return false;
      band = b;
      var g = ring.querySelector('.ring-hy--' + band);
      if (!g) return false;
      paths = [].slice.call(g.querySelectorAll('path[data-b]')).map(function (p) {
        return {el: p, a: +p.getAttribute('data-a'), b: +p.getAttribute('data-b'), last: -1};
      });
      fades = [].slice.call(g.querySelectorAll('path[data-f]')).map(function (p) {
        return {el: p, a: +p.getAttribute('data-f'), last: -1};
      });
      mains = {};
      [].slice.call(g.querySelectorAll('path[data-v]')).forEach(function (p) {
        mains[p.getAttribute('data-v')] = {el: p, a: +p.getAttribute('data-a'), b: +p.getAttribute('data-b')};
      });
      dMax = paths.reduce(function (m, p) { return Math.max(m, p.b); }, 1);
      dMax = fades.reduce(function (m, p) { return Math.max(m, p.a + 60); }, dMax);
      dIntro = Object.keys(mains).reduce(function (m, k) { return Math.max(m, mains[k].b); }, 0);
      return true;
    }
    collect();

    /* a medallion resolves (opacity and a slight scale) over the last stretch of its own main */
    function resolveMeds(D) {
      meds.forEach(function (li) {
        var m = mains[li.getAttribute('data-variety')];
        var t = m ? Math.min(1, Math.max(0, (D - m.a - (m.b - m.a) * 0.55) / ((m.b - m.a) * 0.45))) : 1;
        var e = 1 - Math.pow(1 - t, 3);
        li.style.setProperty('--o', (0.3 + 0.7 * e).toFixed(3));
        li.style.setProperty('--s', (0.95 + 0.05 * e).toFixed(4));
      });
    }
    function apply(D) {
      var i, p, t;
      for (i = 0; i < paths.length; i++) {
        p = paths[i]; t = (D - p.a) / (p.b - p.a);
        t = t < 0 ? 0 : t > 1 ? 1 : t;
        if (t !== p.last) {
          /* hidden until it starts, so no round cap dots the origin */
          p.el.style.strokeDashoffset = 1 - t;
          p.el.style.visibility = t > 0 ? 'visible' : '';
          p.last = t;
        }
      }
      for (i = 0; i < fades.length; i++) {
        p = fades[i]; t = (D - p.a) / 60;
        t = t < 0 ? 0 : t > 1 ? 1 : Math.round(t * 50) / 50;
        if (t !== p.last) { p.el.style.opacity = t; p.last = t; }
      }
      resolveMeds(D);
    }
    function setStatic() {
      rootEl.classList.remove('ring-grow');
      paths.forEach(function (p) { p.el.style.strokeDashoffset = ''; p.el.style.visibility = ''; p.last = -1; });
      fades.forEach(function (p) { p.el.style.opacity = ''; p.last = -1; });
      meds.forEach(function (li) { li.style.removeProperty('--o'); li.style.removeProperty('--s'); });
    }

    var cur = 0, target = 0, raf = null, start = null, active = false, done = false, runway = 1;
    var INTRO = 1500;
    function layout(on) {
      ringPin.classList.toggle('is-pinned', on);
      if (!on) { ringPin.style.height = ''; ring.style.top = ''; return; }
      var hdr = header ? header.offsetHeight : 0;
      runway = Math.round(window.innerHeight * 0.9);
      ring.style.top = Math.min(hdr, window.innerHeight - ring.offsetHeight) + 'px';
      ringPin.style.height = (ring.offsetHeight + runway) + 'px';
    }
    function scrollShare() {
      var s0 = ringPin.offsetTop - (parseFloat(ring.style.top) || 0);
      return Math.min(1, Math.max(0, (window.scrollY - s0) / runway));
    }
    function frame(ts) {
      if (start === null) start = ts;
      var ti = Math.min(1, (ts - start) / INTRO);
      var intro = dIntro * (1 - Math.pow(2, -9 * ti));
      var s = scrollShare();
      /* scroll carries D from where the intro ends to the far tips; the full drawing holds for the last fifth */
      var fromScroll = s > 0 ? dIntro + (dMax - dIntro) * Math.min(1, s / 0.8) : 0;
      target = done ? dMax : Math.max(intro, fromScroll);
      cur += (target - cur) * 0.12;
      if (Math.abs(target - cur) < 0.3) cur = target;
      apply(cur);
      if (ti >= 1 && cur === target) { raf = null; return; }
      raf = requestAnimationFrame(frame);
    }
    function kick() { if (!raf && active) raf = requestAnimationFrame(frame); }
    function reveal() {
      if (!active || done) return;
      done = true; cur = target = dMax; apply(dMax);
    }
    var wide = window.matchMedia('(min-width: 68.75em)'); /* 1100 px at 16 px */
    function setup() {
      var on = wide.matches && !reduce.matches;
      if (on && !active) {
        active = true; done = false;
        rootEl.classList.add('ring-grow');
        layout(true);
        cur = target = 0; start = null;
        apply(0);
        kick();
        if (ring.contains(document.activeElement)) reveal();
      } else if (!on && active) {
        active = false;
        layout(false);
        if (raf) { cancelAnimationFrame(raf); raf = null; }
        setStatic();
      } else if (!on) {
        setStatic();
      }
    }
    if (wide.addEventListener) { wide.addEventListener('change', setup); reduce.addEventListener('change', setup); }
    window.addEventListener('scroll', kick, {passive: true});
    window.addEventListener('resize', function () {
      if (collect()) { if (active) apply(done ? dMax : cur); else setStatic(); }
      if (active) { layout(true); kick(); }
    });
    ring.addEventListener('focusin', reveal);
    setup();

    /* hover / focus: the medallion's own main branch takes its colour (--branch, from varieties.json) */
    meds.forEach(function (li) {
      var id = li.getAttribute('data-variety');
      var col = getComputedStyle(li).getPropertyValue('--branch').trim();
      function main() { return ring.querySelector('.ring-hy--' + band + ' path[data-v="' + id + '"]'); }
      function on() { var p = main(); if (p && col) { p.style.stroke = col; p.style.strokeWidth = '3'; } }
      function off() { var p = main(); if (p) { p.style.stroke = ''; p.style.strokeWidth = ''; } }
      li.addEventListener('mouseenter', on);
      li.addEventListener('mouseleave', off);
      li.addEventListener('focusin', on);
      li.addEventListener('focusout', off);
    });
  }

  /* ---------- 2. delivery: the route with the van, driven by scroll ---------- */
  function initDelivery() {
    var root = document.querySelector('.lv1[data-start]');
    if (!root) return;
    var track = root.querySelector('.lv1-track'), stage = root.querySelector('.lv1-stage'),
        map = root.querySelector('.lv1-map'), canvas = root.querySelector('.lv1-canvas'),
        route = root.querySelector('.lv1-route'), van = root.querySelector('.lv1-van');
    if (!track || !stage || !map || !canvas || !route || !van || !route.getTotalLength) return;
    /* the compass rose turns once and settles on north as the map comes into view */
    if (!reduce.matches && 'IntersectionObserver' in window) {
      root.classList.add('is-rose-armed');
      var rio = new IntersectionObserver(function (es) {
        es.forEach(function (e) { if (e.isIntersecting) { root.classList.add('is-rose-in'); rio.disconnect(); } });
      }, {threshold: .25});
      rio.observe(canvas);
    }
    var stops = [].slice.call(root.querySelectorAll('.lv1-stop[data-x]'));
    var more = root.querySelector('.lv1-stop--more');
    var logs = [].slice.call(root.querySelectorAll('.lv1-log li'));
    /* sample the route once; the scroll loop only reads this table */
    var L = route.getTotalLength(), N = 900, px = new Float32Array(N + 1), py = new Float32Array(N + 1), i;
    for (i = 0; i <= N; i++) { var pt = route.getPointAtLength(L * i / N); px[i] = pt.x; py[i] = pt.y; }
    stops.forEach(function (s) {
      var x = +s.getAttribute('data-x'), y = +s.getAttribute('data-y'), best = 0, bd = 1e12;
      for (var k = 0; k <= N; k++) { var d = (px[k] - x) * (px[k] - x) + (py[k] - y) * (py[k] - y); if (d < bd) { bd = d; best = k; } }
      s._len = L * best / N;
    });
    stops.sort(function (a, b) { return a._len - b._len; });
    var marks = stops.map(function (s) { return s._len; });
    marks[0] = +root.getAttribute('data-start') || 0; marks[marks.length - 1] = L; /* start just outside the farm's medallion */
    var legs = marks.length - 1, D0 = .35, DR = 1, DW = .6, DE = .9, T = D0 + legs * DR + (legs - 1) * DW + DE, TILT = 10;
    var third = Math.max(1, Math.round(legs / 3)); /* the three log blocks follow the route in thirds */
    function lenAt(p) {
      var t = p * T;
      if (t <= D0) return marks[0];
      t -= D0;
      for (var j = 0; j < legs; j++) {
        if (t < DR) { var e = -(Math.cos(Math.PI * t / DR) - 1) / 2; return marks[j] + (marks[j + 1] - marks[j]) * e; }
        t -= DR;
        if (j < legs - 1) { if (t < DW) return marks[j + 1]; t -= DW; }
      }
      return L;
    }
    var live = false, top = 0, range = 1, scale = 1, wheelR = 8, cur = 0, target = 0, face = 1, ang = 0, raf = 0, wanted = {f: 1, a: 0};
    function clear() {
      van.style.transform = ''; van.style.removeProperty('--w'); van.style.removeProperty('--fs');
      route.style.strokeDasharray = ''; route.style.strokeDashoffset = '';
      stops.forEach(function (s) { s.classList.add('is-on'); });
      if (more) more.classList.add('is-on');
      logs.forEach(function (l) { l.classList.add('is-on'); l.classList.remove('is-cur'); });
    }
    function prog() { return Math.min(1, Math.max(0, (window.scrollY - top) / range)); }
    function dirAt(len) {
      var k = Math.round(len / L * N), j = Math.max(0, k - 5), dx, dy;
      if (k < 5) { dx = px[k + 6] - px[k]; dy = py[k + 6] - py[k]; } else { dx = px[k] - px[j]; dy = py[k] - py[j]; }
      var f = dx < 0 ? -1 : 1, a = (f > 0 ? Math.atan2(dy, dx) : Math.atan2(-dy, -dx)) * 57.2958;
      return {f: f, a: Math.max(-TILT, Math.min(TILT, a))};
    }
    function render() {
      var len = lenAt(cur), k = len / L * N, k0 = Math.floor(k), k1 = Math.min(N, k0 + 1), t = k - k0;
      var x = px[k0] + (px[k1] - px[k0]) * t, y = py[k0] + (py[k1] - py[k0]) * t;
      wanted = dirAt(len);
      face += (wanted.f - face) * .2; if (Math.abs(wanted.f - face) < .02) face = wanted.f;
      ang += (wanted.a - ang) * .14; if (Math.abs(wanted.a - ang) < .1) ang = wanted.a;
      van.style.transform = 'translate(' + (x * scale).toFixed(1) + 'px,' + (y * scale).toFixed(1) + 'px) translate(-50%,-88%) rotate(' + ang.toFixed(2) + 'deg) scaleX(' + face.toFixed(3) + ')';
      van.style.setProperty('--w', (len * scale / wheelR * 57.2958).toFixed(1) + 'deg');
      van.style.setProperty('--fs', face < 0 ? '-1' : '1');
      route.style.strokeDashoffset = (L - len).toFixed(1);
      for (var s = 0; s < stops.length; s++) {
        var on = len >= stops[s]._len - 1;
        if (on !== stops[s].classList.contains('is-on')) stops[s].classList.toggle('is-on', on);
      }
      if (more) more.classList.toggle('is-on', cur >= (T - DE * .75) / T);
      var m1 = marks[Math.min(legs, third)], m2 = marks[Math.min(legs, 2 * third)];
      var cur3 = len < m1 - 1 ? 0 : (len < m2 - 1 ? 1 : 2);
      logs.forEach(function (l, n) { l.classList.toggle('is-on', n <= cur3); l.classList.toggle('is-cur', n === cur3); });
    }
    function measure() {
      if (reduce.matches) { root.classList.remove('is-live'); live = false; clear(); return; }
      root.classList.add('is-live');
      /* a stage taller than the viewport cannot pin: fall back to the static map and register */
      if (map.offsetHeight > stage.clientHeight + 1) { root.classList.remove('is-live'); live = false; clear(); return; }
      live = true;
      top = track.getBoundingClientRect().top + window.scrollY;
      range = Math.max(1, track.offsetHeight - stage.offsetHeight);
      scale = canvas.clientWidth / 1000;
      wheelR = van.offsetWidth * 15 / 220;
      route.style.strokeDasharray = L + ' ' + L;
      target = cur = prog();
      var f = dirAt(lenAt(cur)); face = f.f; ang = f.a;
      render();
    }
    function frame() {
      raf = 0;
      cur += (target - cur) * .16; if (Math.abs(target - cur) < .0004) cur = target;
      render();
      if (cur !== target || face !== wanted.f || ang !== wanted.a) raf = requestAnimationFrame(frame);
    }
    window.addEventListener('scroll', function () {
      if (!live) return;
      target = prog();
      if (!raf) raf = requestAnimationFrame(frame);
    }, {passive: true});
    var rt = 0;
    window.addEventListener('resize', function () { clearTimeout(rt); rt = setTimeout(measure, 150); });
    if (reduce.addEventListener) reduce.addEventListener('change', measure);
    /* keyboard users reach every stop, whatever the scroll position */
    root.addEventListener('focusin', function () { root.classList.add('lv1-all'); });
    measure();
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(measure);
    window.addEventListener('load', measure);
  }

  initRing();
  initDelivery();
})();
