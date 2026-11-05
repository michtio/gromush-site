/* Recipe dialog check for /inspiratie/ (S18; PRD R26, AC24). Run via check.py at 390 and 1440:
   python3 -I tools/check.py <url>/inspiratie/ 390 "$(cat tools/dialog.js)"   -> open focus-inside esc-closed focus-returned
   For every recipe card: its trigger is a <button> (recipes.js replaced the no-JS link); activating it opens a modal
   <dialog> labelled by the recipe title, with focus inside; Escape (a keydown on the focused element, bubbling to the
   dialog's listener in recipes.js) closes it and focus returns to the card's button. Also: the dialog holds the
   ingredients, steps, servings and a link to a variety page or /zwammen/ (R26), and it fits the viewport with its
   own scroll (near-fullscreen below 600 px). Prints the four tokens when every card passes, else a JSON list of failures.
   Synthetic events: button.click() stands in for Enter/Space on a <button>. */
(async () => {
  const errs = [];
  const wait = (ms) => new Promise((r) => setTimeout(r, ms || 60));
  await document.fonts.ready; await wait(200);
  const cards = [...document.querySelectorAll('.rc-card')];
  if (!cards.length) return JSON.stringify(['no recipe cards']);
  const book = document.querySelector('[data-recipe-book]');
  if (!book || !book.hidden) errs.push('recipe book not hidden with JS');
  for (const card of cards) {
    const btn = card.querySelector('.rc-open');
    const label = (btn && btn.textContent.trim().slice(0, 30)) || '?';
    if (!btn || btn.tagName !== 'BUTTON') { errs.push('trigger is not a button: ' + label); continue; }
    btn.focus(); btn.click(); await wait();
    const dlg = document.querySelector('dialog.rc-dialog[open]');
    if (!dlg) { errs.push('no open dialog: ' + label); continue; }
    if (!dlg.matches(':modal')) errs.push('dialog not modal: ' + label);
    const title = document.getElementById(dlg.getAttribute('aria-labelledby') || '');
    if (!title || !dlg.contains(title) || title.textContent.trim() !== btn.textContent.trim()) errs.push('dialog label is not the recipe title: ' + label);
    if (!dlg.contains(document.activeElement)) errs.push('focus not inside: ' + label);
    if (!dlg.querySelector('.rc-ingredients li') || !dlg.querySelector('.rc-steps li')) errs.push('no ingredients or steps: ' + label);
    if (!/Voor/.test(dlg.querySelector('.rc-facts')?.textContent || '')) errs.push('no servings: ' + label);
    if (!dlg.querySelector('.rc-facts a[href*="/zwammen/"]')) errs.push('no variety link: ' + label);
    const r = dlg.getBoundingClientRect();
    if (r.top < 0 || r.bottom > innerHeight + 1 || r.left < 0 || r.right > innerWidth + 1) errs.push('dialog outside the viewport: ' + label);
    if (innerWidth < 600 && (r.width < innerWidth - 24 || r.height < innerHeight * 0.85)) errs.push('dialog not near-fullscreen at ' + innerWidth + ': ' + label + ' ' + Math.round(r.width) + 'x' + Math.round(r.height));
    if (dlg.scrollHeight > dlg.clientHeight + 1 && getComputedStyle(dlg).overflowY === 'visible') errs.push('dialog content overflows without scroll: ' + label);
    (document.activeElement || dlg).dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape', bubbles: true, cancelable: true }));
    await wait();
    if (dlg.open) { errs.push('Escape did not close: ' + label); dlg.close(); await wait(); }
    if (document.activeElement !== btn) errs.push('focus did not return to the card: ' + label);
  }
  return errs.length ? JSON.stringify(errs) : 'open focus-inside esc-closed focus-returned';
})()
