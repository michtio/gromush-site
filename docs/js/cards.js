/* Variety flip cards (S3; final.html "flip cards"). Progressive: without this script both faces show and the
   request link works (CSS, html:not(.js)). With it, the "Draai om" button under each card turns the card; the face
   that is turned away is inert and aria-hidden, and the request link on the back is only reachable when it shows.
   Reduced motion turns the flip into a cross-fade in CSS; nothing here depends on motion. */
(function () {
  document.querySelectorAll('.tc[data-card]').forEach(function (card) {
    var name = (card.getAttribute('data-name') || '').toLowerCase();
    var flip = card.parentElement.querySelector(':scope > .tc-flip');
    var front = card.querySelector('.tc-front');
    var back = card.querySelector('.tc-back');
    if (!flip || !front || !back) return;
    var labelOn = flip.textContent.trim();
    var labelOff = flip.getAttribute('data-flip-back') || labelOn;
    function setInert(el, on) {
      if (on) el.setAttribute('inert', ''); else el.removeAttribute('inert');
      el.setAttribute('aria-hidden', on ? 'true' : 'false');
    }
    function apply(on) {
      card.classList.toggle('is-flipped', on);
      flip.textContent = on ? labelOff : labelOn;
      var sr = document.createElement('span');
      sr.className = 'sr-only';
      sr.textContent = ': ' + name;
      flip.appendChild(sr);
      setInert(front, on);
      setInert(back, !on);
    }
    flip.hidden = false;
    apply(false);
    flip.addEventListener('click', function () { apply(!card.classList.contains('is-flipped')); });
  });
})();
