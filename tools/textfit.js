/* Text fit at the current viewport (written for 200 % text at 320 px, PRD R38 / WCAG 1.4.4 and 1.4.10).
   Evaluate in the page (tools/fullshot.py runs it before capturing; tools/check.py accepts it as an expression).
   Returns {n, problems:[...]} where each problem is one of:
     "offscreen <el> <word>"   a word runs past the left or right edge of the viewport (html clips overflow-x,
                               so scrollWidth alone cannot see it)
     "clipped <el> <word>"     a word is cut off by an ancestor with overflow hidden/clip (a line clamp is not counted)
     "broken <el> <word>"      a word is split over two lines without a hyphen (overflow-wrap broke it);
                               breaks at '-', '/', '@' or '.' and automatic hyphenation (hyphens:auto) are allowed;
                               a break counts as hyphenation when the word fits its block with overflow-wrap off;
                               e-mail addresses and URLs may break anywhere
     "hscroll <scrollWidth>"   the page scrolls horizontally
   Words inside a horizontal scroll container are not checked against the viewport edges.
   Text that is not rendered (display:none, visibility:hidden, zero-size, aria-hidden, .sr-only) is skipped. */
(() => {
  const W = document.documentElement.clientWidth, out = [];
  const name = el => el.tagName.toLowerCase() + (typeof el.className === 'string' && el.className.trim()
    ? '.' + el.className.trim().split(/\s+/).slice(0, 2).join('.') : '');
  if (document.documentElement.scrollWidth > W) out.push('hscroll ' + document.documentElement.scrollWidth);
  /* the nearest ancestor that clips (overflow hidden/clip), and whether a horizontal scroll container holds the text:
     a row of cards that scrolls sideways inside its own frame keeps its content reachable, so its words are not
     checked against the viewport edges */
  const frame = el => {
    let clip = null, scrolls = false;
    for (let e = el; e && e !== document.body && e !== document.documentElement; e = e.parentElement) {
      const cs = getComputedStyle(e);
      if (/auto|scroll/.test(cs.overflowX)) { scrolls = true; break; }
      /* a line clamp (-webkit-line-clamp) is a deliberate teaser cut, not a clip: the page must carry the full text elsewhere */
      if (!clip && /hidden|clip/.test(cs.overflowX + cs.overflowY) && (cs.webkitLineClamp || 'none') === 'none') clip = e;
    }
    return { clip, scrolls };
  };
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  const range = document.createRange(), probe = document.createRange();
  /* words split under hyphens:auto, checked together at the end (one relayout instead of two per word) */
  const hyphenated = [];
  const blockOf = el => {
    let block = el;
    while (block.parentElement && getComputedStyle(block).display.startsWith('inline')) block = block.parentElement;
    return block;
  };
  /* the box of one character: its last client rect (a range that starts at a soft wrap can also report an empty
     box at the end of the previous line) */
  const charBox = (node, i) => {
    probe.setStart(node, i); probe.setEnd(node, i + 1);
    const rs = [...probe.getClientRects()].filter(r => r.width > 0);
    return rs.length ? rs[rs.length - 1] : null;
  };
  /* first and last character on different lines: their tops differ by more than half a line (a tilted note moves
     the tops of one line by a pixel or two) */
  const split = (node, start, len) => {
    const a = charBox(node, start), b = charBox(node, start + len - 1);
    return !!(a && b) && Math.abs(a.top - b.top) > Math.max(a.height, b.height) / 2;
  };
  /* an e-mail address, URL or phone number may break anywhere (it has no syllables, and a hyphen would change it) */
  const address = (text, i) => {
    const a = text.lastIndexOf(' ', i) + 1, b = text.indexOf(' ', i);
    return /@|:\/\/|^www\.|^\+?\d[\d ]{6,}/.test(text.slice(a, b < 0 ? undefined : b));
  };
  const seen = new Set();
  let node;
  while ((node = walker.nextNode())) {
    const el = node.parentElement;
    if (!el || !node.textContent.trim()) continue;
    if (el.closest('script,style,noscript,template,[aria-hidden="true"],.sr-only,.visually-hidden,[hidden]')) continue;
    const cs = getComputedStyle(el);
    if (cs.visibility !== 'visible' || !el.getClientRects().length) continue;
    const { clip, scrolls } = frame(el), cr = clip && clip.getBoundingClientRect();
    const re = /[^\s\-‐-—\/@.]+/g;
    let m;
    while ((m = re.exec(node.textContent))) {
      range.setStart(node, m.index); range.setEnd(node, m.index + m[0].length);
      const rects = [...range.getClientRects()].filter(r => r.width > 0 && r.height > 0);
      if (!rects.length) continue;
      const key = (kind) => { const k = kind + ' ' + name(el) + ' ' + m[0]; if (!seen.has(k)) { seen.add(k); out.push(k); } };
      if (!scrolls && rects.some(r => r.right > W + 1 || r.left < -1)) key('offscreen');
      else if (cr && cr.width > 0 && rects.some(r => r.right > cr.right + 1 || r.left < cr.left - 1 || r.bottom > cr.bottom + 1 || r.top < cr.top - 1)) key('clipped');
      if (m[0].length > 1 && !address(node.textContent, m.index) && split(node, m.index, m[0].length)) {
        /* under hyphens:auto the break is fine when hyphenation alone makes the word fit: with overflow-wrap and
           word-break switched off the word then still stays inside its block. If it runs out, the break was
           overflow-wrap's, inside the word without a hyphen. */
        if (cs.hyphens !== 'auto') key('broken');
        else hyphenated.push({ node, start: m.index, len: m[0].length, block: blockOf(el), label: 'broken ' + name(el) + ' ' + m[0] });
      }
    }
  }
  /* under hyphens:auto a split is fine when hyphenation alone makes the word fit: with overflow-wrap and word-break
     switched off everywhere, the word still stays inside its block. If it runs out, the split was overflow-wrap's,
     inside the word without a hyphen. */
  if (hyphenated.length) {
    const off = document.createElement('style');
    off.textContent = '*{overflow-wrap:normal!important;word-break:normal!important}';
    document.head.append(off);
    for (const w of hyphenated) {
      const bs = getComputedStyle(w.block), br = w.block.getBoundingClientRect();
      const right = br.right - parseFloat(bs.paddingRight) - parseFloat(bs.borderRightWidth);
      probe.setStart(w.node, w.start); probe.setEnd(w.node, w.start + w.len);
      if (![...probe.getClientRects()].every(r => r.right <= right + 1) && !seen.has(w.label)) { seen.add(w.label); out.push(w.label); }
    }
    off.remove();
  }
  return { n: out.length, problems: out };
})()
