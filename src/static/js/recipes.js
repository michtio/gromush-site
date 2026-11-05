/* Recipe dialogs for /inspiratie/ (S18; PRD R26, AC24; plan AD14). Vanilla, no dependencies.
   The page ships every recipe as a full <article> in .rc-book, and every card's title as a link to that article,
   so without this script the recipes read in place. This script:
   - moves each article into its own native <dialog> (showModal: focus moves inside, the rest of the page is inert),
     with a close button first and aria-labelledby on the recipe title;
   - turns each card's link into a <button> that opens its dialog, and hides the now empty .rc-book;
   - closes on the close button, Escape and a click on the backdrop, and returns focus to the card's button;
   - opens the dialog named in the URL hash on load (#recept-<id>, e.g. a link from another page).
   Docs: https://html.spec.whatwg.org/multipage/interactive-elements.html#the-dialog-element,
   https://developer.mozilla.org/en-US/docs/Web/API/HTMLDialogElement/showModal */
(() => {
  const book = document.querySelector('[data-recipe-book]');
  if (!book || typeof HTMLDialogElement !== 'function') return; // no dialog support: the articles stay in place
  const main = document.querySelector('main') || document.body;
  const closeLabel = book.getAttribute('data-close-label') || 'Sluiten';
  const dialogs = new Map(); // article id -> {dialog, opener}

  const closeIcon = '<svg width="16" height="16" viewBox="0 0 16 16" aria-hidden="true" focusable="false"><path d="M2 2l12 12M14 2L2 14" stroke="currentColor" stroke-width="2" stroke-linecap="round" fill="none"/></svg>';

  book.querySelectorAll('article.rc-article[id]').forEach((article) => {
    const id = article.id;
    const dialog = document.createElement('dialog');
    dialog.className = 'rc-dialog';
    dialog.id = id + '-dialoog';
    const title = article.getAttribute('aria-labelledby');
    if (title) dialog.setAttribute('aria-labelledby', title);
    const sheet = document.createElement('div');
    sheet.className = 'rc-sheet';
    const close = document.createElement('button');
    close.type = 'button';
    close.className = 'rc-close';
    close.setAttribute('aria-label', closeLabel);
    close.innerHTML = closeIcon;
    close.addEventListener('click', () => dialog.close());
    const bar = document.createElement('div'); // sticky strip: the close button stays in reach while the recipe scrolls
    bar.className = 'rc-bar';
    bar.append(close);
    article.removeAttribute('id'); // the dialog carries the anchor's meaning now; keep ids unique
    article.setAttribute('data-recipe-id', id);
    sheet.append(bar, article);
    dialog.append(sheet);
    main.append(dialog);
    const entry = { dialog, opener: null };
    dialogs.set(id, entry);

    // Escape: handled here as well as natively, so the close (and the focus return below) never depends on the
    // browser's close-request handling; preventDefault stops a second, native cancel.
    dialog.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') { e.preventDefault(); dialog.close(); }
    });
    // a click on the backdrop lands on the <dialog> itself; the sheet fills the whole dialog box
    dialog.addEventListener('click', (e) => { if (e.target === dialog) dialog.close(); });
    dialog.addEventListener('close', () => {
      if (location.hash === '#' + id) history.replaceState(null, '', location.pathname + location.search);
      if (entry.opener && entry.opener.isConnected) entry.opener.focus();
    });
  });

  const open = (id, opener) => {
    const entry = dialogs.get(id);
    if (!entry || entry.dialog.open) return;
    entry.opener = opener || entry.opener;
    entry.dialog.showModal();
    entry.dialog.scrollTop = 0;
  };

  document.querySelectorAll('a.rc-open[data-recipe]').forEach((link) => {
    const id = link.getAttribute('data-recipe');
    if (!dialogs.has(id)) return;
    const button = document.createElement('button');
    button.type = 'button';
    button.className = link.className;
    button.setAttribute('data-recipe', id);
    button.setAttribute('aria-haspopup', 'dialog');
    button.textContent = link.textContent;
    link.replaceWith(button);
    dialogs.get(id).opener = button;
    button.addEventListener('click', () => open(id, button));
  });

  book.hidden = true;
  document.documentElement.classList.add('rc-ready');

  const fromHash = () => {
    const id = decodeURIComponent(location.hash.slice(1));
    if (dialogs.has(id)) open(id);
  };
  addEventListener('hashchange', fromHash);
  fromHash();
})();
