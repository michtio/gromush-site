/* Structural accessibility checks (PRD R38, AC35), an axe-like pass without npm. Evaluate in the page:
   python3 -I tools/check.py <url> 390 "$(cat tools/a11y.js)"
   -> {"n":0,"problems":[]}
   Checks: <html lang> and a <title>; every <img> has an alt attribute and every svg[role=img] a name; every form
   control has a label (label[for], a wrapping label, aria-label, aria-labelledby or title); one <main>, one banner
   header and one contentinfo footer at the top level, and several <nav>s carry distinct names; exactly one <h1>;
   heading levels never skip down (h2 -> h4), counted apart inside each <dialog>; every link and button has an
   accessible name (checked where exposed: rendered and outside aria-hidden); aria-labelledby/-describedby/-controls/-owns/-activedescendant/-errormessage and label[for]
   point at existing ids; no duplicate ids; nothing focusable inside aria-hidden="true"; no positive tabindex.
   It complements contrast.js, sweep.js (44 px targets), nav-a11y.js and tabwalk.py; it does not replace a
   screen-reader pass. */
(() => {
  const out = [];
  const add = s => { if (!out.includes(s)) out.push(s); };
  const desc = el => el.tagName.toLowerCase() + (el.id ? '#' + el.id : '') +
    (typeof el.className === 'string' && el.className.trim() ? '.' + el.className.trim().split(/\s+/).slice(0, 2).join('.') : '');
  const byId = id => document.getElementById(id);
  /* rendered for assistive technology: not display:none / visibility:hidden, not inside aria-hidden="true" */
  const shown = el => (el.checkVisibility ? el.checkVisibility({ visibilityProperty: true }) : el.getClientRects().length > 0);
  const exposed = el => shown(el) && !el.closest('[aria-hidden="true"]');
  /* accessible name, close to the accname rules for the cases this site uses */
  const textOf = el => {
    if (el.nodeType === 3) return el.textContent;
    if (el.nodeType !== 1) return '';
    if (el.getAttribute('aria-hidden') === 'true' || el.hidden) return '';
    if (el.tagName === 'IMG') return el.getAttribute('alt') || '';
    if (el.tagName === 'svg' || el.tagName === 'SVG') {
      const t = el.querySelector('title');
      return el.getAttribute('aria-label') || (t ? t.textContent : '');
    }
    if (el.getAttribute('aria-label')) return el.getAttribute('aria-label');
    return [...el.childNodes].map(textOf).join(' ');
  };
  const nameOf = el => {
    const lb = el.getAttribute('aria-labelledby');
    if (lb) return lb.split(/\s+/).map(id => byId(id) ? byId(id).textContent : '').join(' ').trim();
    if (el.getAttribute('aria-label')) return el.getAttribute('aria-label').trim();
    if (/^(INPUT|SELECT|TEXTAREA)$/.test(el.tagName)) {
      const labels = el.labels ? [...el.labels] : [];
      const t = labels.map(textOf).join(' ').trim();
      if (t) return t;
      if (el.type === 'submit' || el.type === 'button') return (el.value || '').trim();
      return (el.getAttribute('title') || '').trim();
    }
    return (textOf(el).replace(/\s+/g, ' ').trim() || el.getAttribute('title') || '').trim();
  };

  /* document */
  if (!document.documentElement.lang) add('html has no lang');
  if (!document.title.trim()) add('empty <title>');

  /* duplicate ids */
  const seen = {};
  for (const el of document.querySelectorAll('[id]')) seen[el.id] = (seen[el.id] || 0) + 1;
  for (const [id, n] of Object.entries(seen)) if (n > 1) add('duplicate id #' + id + ' (' + n + 'x)');

  /* id references */
  for (const attr of ['aria-labelledby', 'aria-describedby', 'aria-controls', 'aria-owns', 'aria-activedescendant', 'aria-errormessage']) {
    for (const el of document.querySelectorAll('[' + attr + ']')) {
      for (const id of el.getAttribute(attr).split(/\s+/).filter(Boolean)) if (!byId(id)) add(attr + ' on ' + desc(el) + ' points at missing #' + id);
    }
  }
  for (const l of document.querySelectorAll('label[for]')) if (!byId(l.htmlFor)) add('label[for] points at missing #' + l.htmlFor);

  /* images */
  for (const img of document.querySelectorAll('img')) if (!img.hasAttribute('alt')) add('img without alt: ' + (img.getAttribute('src') || '').split('/').pop());
  for (const svg of document.querySelectorAll('svg[role="img"]')) if (!nameOf(svg) && !textOf(svg).trim()) add('svg[role=img] without a name: ' + desc(svg));
  for (const el of document.querySelectorAll('[role="img"]:not(svg)')) if (!nameOf(el)) add('role=img without a name: ' + desc(el));

  /* form controls */
  for (const c of document.querySelectorAll('input:not([type=hidden]):not([type=submit]):not([type=button]):not([type=reset]),select,textarea')) {
    if (!nameOf(c)) add('form control without a label: ' + desc(c) + (c.name ? '[name=' + c.name + ']' : ''));
  }
  for (const fs of document.querySelectorAll('fieldset')) if (!fs.querySelector(':scope > legend') && !nameOf(fs)) add('fieldset without legend: ' + desc(fs));

  /* landmarks */
  const top = sel => [...document.querySelectorAll(sel)].filter(el => !el.parentElement.closest('article,aside,main,nav,section,dialog'));
  const mains = document.querySelectorAll('main,[role=main]');
  if (mains.length !== 1) add(mains.length + ' main landmarks');
  if (top('header,[role=banner]').length !== 1) add(top('header,[role=banner]').length + ' banner headers');
  if (top('footer,[role=contentinfo]').length !== 1) add(top('footer,[role=contentinfo]').length + ' contentinfo footers');
  const navs = [...document.querySelectorAll('nav,[role=navigation]')];
  if (navs.length > 1) {
    const names = navs.map(nameOf);
    navs.forEach((n, i) => {
      const own = n.getAttribute('aria-label') || n.getAttribute('aria-labelledby');
      if (!own) add('nav without a name among ' + navs.length + ': ' + desc(n));
      else if (names.indexOf(names[i]) !== i) add('two navs named "' + names[i] + '"');
    });
  }
  for (const el of document.querySelectorAll('body *')) {
    if (!el.closest('header,nav,main,footer,aside,dialog,[role=banner],[role=navigation],[role=main],[role=contentinfo],[role=complementary],[role=region],section[aria-label],section[aria-labelledby]') &&
        el.matches('a,button,input,select,textarea,h1,h2,h3,h4,h5,h6,p,img') && el.getClientRects().length &&
        !el.matches('a.skip')) { /* the skip link sits before the landmarks on purpose (axe exempts it too) */
      add('content outside landmarks: ' + desc(el)); break;
    }
  }

  /* headings */
  /* one h1 as rendered: the homepage has a desktop and a phone hero, one of them display:none */
  const h1s = [...document.querySelectorAll('h1')].filter(h => !h.closest('dialog') && shown(h));
  if (h1s.length !== 1) add(h1s.length + ' h1 elements');
  const outline = scope => {
    let prev = 0;
    for (const h of scope.querySelectorAll('h1,h2,h3,h4,h5,h6')) {
      if (!h.closest('dialog') && !exposed(h)) continue;
      const inDialog = h.closest('dialog');
      if ((scope.tagName === 'DIALOG') !== !!inDialog || (inDialog && inDialog !== scope)) continue;
      const level = +h.tagName[1];
      if (prev && level > prev + 1) add('heading skips h' + prev + ' -> h' + level + ': "' + h.textContent.trim().slice(0, 40) + '"' + (inDialog ? ' (in ' + desc(inDialog) + ')' : ''));
      prev = level;
    }
  };
  outline(document.body);
  document.querySelectorAll('dialog').forEach(outline);
  for (const h of document.querySelectorAll('h1,h2,h3,h4,h5,h6')) if (!textOf(h).trim()) add('empty heading: ' + desc(h));

  /* links and buttons */
  for (const a of document.querySelectorAll('a[href]')) if (exposed(a) && !nameOf(a)) add('link without a name: ' + desc(a) + ' -> ' + a.getAttribute('href'));
  for (const b of document.querySelectorAll('button,[role=button]')) if (exposed(b) && !nameOf(b)) add('button without a name: ' + desc(b));

  /* focus */
  for (const el of document.querySelectorAll('[aria-hidden="true"] a[href],[aria-hidden="true"] button,[aria-hidden="true"] input,[aria-hidden="true"] select,[aria-hidden="true"] textarea,[aria-hidden="true"] [tabindex]:not([tabindex="-1"])')) {
    if (shown(el) && el.tabIndex >= 0) add('focusable inside aria-hidden: ' + desc(el));
  }
  for (const el of document.querySelectorAll('[tabindex]')) if (el.tabIndex > 0) add('positive tabindex: ' + desc(el));

  return { n: out.length, problems: out };
})()
