/* ProefBox promo probe (S4; R35, AD15), evaluated by tools/promo.py after each step of its multi-page run.
   Returns JSON: open (the dialog is showing as a modal), present (the page has the dialog), store (the
   sessionStorage "gromush-promo" value), focusIn (focus is inside the dialog), active (tag.class of the focused
   element), box (the paper's rectangle, for clicking outside it), close (the close button's centre). */
(() => {
  const d = document.getElementById('promo');
  const paper = d && d.querySelector('.promo-paper');
  const btn = d && d.querySelector('.promo-close');
  const r = paper ? paper.getBoundingClientRect() : null;
  const c = btn ? btn.getBoundingClientRect() : null;
  const a = document.activeElement;
  let store = null;
  try { store = JSON.parse(sessionStorage.getItem('gromush-promo')); } catch (e) { store = 'unavailable'; }
  return JSON.stringify({
    present: !!d, open: !!(d && d.open && d.matches(':modal')), store,
    focusIn: !!(d && d.contains(a)), active: a ? a.tagName + '.' + String(a.className).split(' ')[0] : null,
    box: r && [r.left, r.top, r.right, r.bottom], close: c && [c.left + c.width / 2, c.top + c.height / 2],
  });
})()
