/* Keyboard and disclosure check of the site header (S4; R6, R38). Run via check.py at 1440 and at 390:
   python3 -I tools/check.py <url> 390 "$(cat tools/nav-a11y.js)"   -> ok
   - no positive tabindex anywhere (so Tab follows DOM order); every nav link, disclosure button, dropdown link and
     the CTA is focusable and visible when reached (focus() lands on it while it is rendered and not inert);
   - each disclosure button: aria-expanded false and its list hidden; activating it sets true and shows the list;
     Escape from inside the list closes it and returns focus to the button; activating again closes it;
   - below 900 px: the menu button comes before the nav in DOM order (Tab goes from the button into the panel),
     opens the panel (aria-expanded, label), its targets are at least 44 px, and Escape closes it and returns
     focus to the button.
   Synthetic events: element.click() stands in for Enter/Space on a <button>, and an Escape keydown on the focused
   element bubbles to the document listener of site.js. Prints "ok" or a JSON list of failures. */
(async () => {
  const errs = [];
  const wait = (ms) => new Promise((r) => setTimeout(r, ms || 30));
  const vis = (e) => !!e && e.getClientRects().length > 0 && getComputedStyle(e).visibility !== 'hidden' && !e.closest('[inert]');
  const name = (e) => (e.getAttribute('aria-label') || e.textContent || '').trim().slice(0, 30);
  const reach = (e) => { e.focus(); if (document.activeElement !== e || !vis(e)) errs.push('not reachable: ' + name(e)); };
  const esc = () => (document.activeElement || document.body).dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape', bubbles: true }));
  await document.fonts.ready; await wait(200);
  const nav = document.getElementById('main-nav');
  const btn = document.querySelector('.menu-btn');
  const wide = innerWidth >= 900;
  if (!nav) return JSON.stringify(['no #main-nav']);
  if (document.querySelector('[tabindex]:not([tabindex="0"]):not([tabindex="-1"])')) errs.push('positive tabindex present');
  if (!wide) {
    if (!vis(btn)) return JSON.stringify(['menu button not visible']);
    if (!(btn.compareDocumentPosition(nav) & Node.DOCUMENT_POSITION_FOLLOWING)) errs.push('menu button is not before the nav');
    if (btn.getAttribute('aria-expanded') !== 'false' || vis(nav)) errs.push('menu not closed at load');
    const closedLabel = btn.getAttribute('aria-label');
    btn.focus(); btn.click(); await wait();
    if (btn.getAttribute('aria-expanded') !== 'true' || !vis(nav)) errs.push('menu does not open');
    if (btn.getAttribute('aria-label') === closedLabel) errs.push('menu button label does not change');
  } else if (btn && vis(btn)) errs.push('menu button visible on a wide screen');
  const toggles = [...nav.querySelectorAll('.sub-toggle')];
  if (toggles.length !== 3) errs.push('expected 3 dropdowns, got ' + toggles.length);
  nav.querySelectorAll('.nav-link').forEach(reach);
  for (const t of toggles) {
    const sub = document.getElementById(t.getAttribute('aria-controls'));
    if (!sub) { errs.push('no list for ' + name(t)); continue; }
    reach(t);
    if (t.getAttribute('aria-expanded') !== 'false' || vis(sub)) errs.push('open at load: ' + name(t));
    t.click(); await wait();
    if (t.getAttribute('aria-expanded') !== 'true' || !vis(sub)) errs.push('does not open: ' + name(t));
    const links = [...sub.querySelectorAll('a')];
    if (!links.length) errs.push('empty dropdown: ' + name(t));
    links.forEach(reach);
    if (!wide) links.concat([t]).forEach((e) => { const r = e.getBoundingClientRect(); if (r.height < 44 || r.width < 44) errs.push('target under 44px: ' + name(e)); });
    esc(); await wait();
    if (t.getAttribute('aria-expanded') !== 'false' || vis(sub)) errs.push('Escape does not close: ' + name(t));
    if (document.activeElement !== t) errs.push('Escape does not return focus to: ' + name(t));
    t.click(); await wait(); t.click(); await wait();
    if (t.getAttribute('aria-expanded') !== 'false' || vis(sub)) errs.push('second activation does not close: ' + name(t));
  }
  const cta = document.querySelector('.site-header .btn-cta');
  if (!cta) errs.push('no CTA'); else reach(cta);
  if (!wide) {
    nav.querySelector('.nav-link').focus();
    esc(); await wait();
    if (btn.getAttribute('aria-expanded') !== 'false' || vis(nav)) errs.push('Escape does not close the menu');
    if (document.activeElement !== btn) errs.push('Escape does not return focus to the menu button');
  }
  return errs.length ? JSON.stringify(errs) : 'ok';
})()
