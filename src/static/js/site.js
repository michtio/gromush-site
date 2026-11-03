/* GroMush site script (S4), loaded on every page. Progressive: without it the navigation is plain links (the hubs
   and the footer reach every page), dropdowns open on hover or keyboard focus in CSS, and the promo never opens.
   1. Mobile menu: the 44px button opens the panel; Escape closes it and returns focus to the button.
   2. Dropdowns: disclosure buttons (aria-expanded) beside the hub links; click, Enter or Space toggles, mouse hover
      opens on wide screens, Escape closes and returns focus to the button, focus or a click outside closes.
   3. Header scroll state (straw ground with an ink rule once the page scrolls); a header taller than a quarter
      of the viewport stops being sticky, and the menu panel fits the space under the header.
   4. ProefBox promo (PRD R35, plan AD15): sessionStorage key "gromush-promo" ({views, state}); shown at most once
      per session, from the second page view, after data-delay seconds or data-scroll of the page; never on the
      paths in data-never-on; closes with its button, Escape (native <dialog>) or a click outside the paper. */
(function () {
  'use strict';
  var header = document.querySelector('.site-header');
  var nav = document.getElementById('main-nav');
  var menuBtn = document.querySelector('.menu-btn');
  var wide = window.matchMedia('(min-width: 900px)');
  var hover = window.matchMedia('(hover: hover)');

  /* ---------- 1. mobile menu ---------- */
  function menuOpen() { return !!(nav && nav.classList.contains('open')); }
  function setMenu(open, focusButton) {
    if (!nav || !menuBtn) return;
    nav.classList.toggle('open', open);
    if (header) header.classList.toggle('is-open', open);
    menuBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
    menuBtn.setAttribute('aria-label', menuBtn.getAttribute(open ? 'data-label-close' : 'data-label-open'));
    if (!open) closeAll();
    if (!open && focusButton) menuBtn.focus();
  }
  if (nav && menuBtn) {
    menuBtn.addEventListener('click', function () { setMenu(!menuOpen()); fitHeader(); });
    nav.addEventListener('click', function (e) { if (e.target.closest('a')) setMenu(false); });
    wide.addEventListener('change', function () { setMenu(false); });
  }

  /* ---------- 2. dropdowns ---------- */
  var toggles = Array.prototype.slice.call(document.querySelectorAll('.sub-toggle'));
  var hoverTimer = null;
  function isOpen(t) { return t.getAttribute('aria-expanded') === 'true'; }
  function setSub(t, open) { t.setAttribute('aria-expanded', open ? 'true' : 'false'); }
  function closeAll(except) { toggles.forEach(function (t) { if (t !== except) setSub(t, false); }); }
  toggles.forEach(function (t) {
    var item = t.closest('.has-sub');
    t.hidden = false;
    t.addEventListener('click', function () {
      var open = !isOpen(t);
      closeAll(t);
      setSub(t, open);
    });
    item.addEventListener('focusout', function (e) {
      if (e.relatedTarget && !item.contains(e.relatedTarget)) setSub(t, false);
    });
    item.addEventListener('pointerenter', function (e) {
      if (e.pointerType !== 'mouse' || !wide.matches || !hover.matches) return;
      clearTimeout(hoverTimer);
      closeAll(t);
      setSub(t, true);
    });
    item.addEventListener('pointerleave', function (e) {
      if (e.pointerType !== 'mouse' || !wide.matches || !hover.matches) return;
      clearTimeout(hoverTimer);
      hoverTimer = setTimeout(function () { if (!item.contains(document.activeElement)) setSub(t, false); }, 250);
    });
  });
  document.addEventListener('click', function (e) {
    if (!e.target.closest('.has-sub')) closeAll();
    if (menuOpen() && header && !header.contains(e.target)) setMenu(false);
  });
  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    var open = toggles.filter(isOpen)[0];
    if (open) {
      var inside = open.closest('.has-sub').contains(document.activeElement);
      setSub(open, false);
      if (inside || !document.activeElement || document.activeElement === document.body) open.focus();
      return;
    }
    if (menuOpen()) setMenu(false, true);
  });

  /* ---------- 3. header scroll state and size ---------- */
  function onScrollHeader() { if (header) header.classList.toggle('is-scrolled', window.scrollY > 8); }
  window.addEventListener('scroll', onScrollHeader, { passive: true });
  onScrollHeader();
  // with large text on a small screen the header can fill much of the viewport: then it scrolls away (reflow,
  // R38), and the open menu panel is capped to the space under the header so its last links stay reachable
  function fitHeader() {
    if (!header) return;
    header.classList.toggle('is-static', header.offsetHeight > window.innerHeight / 4);
    if (nav && menuBtn && !wide.matches) {
      nav.style.maxHeight = Math.max(160, window.innerHeight - Math.max(0, header.getBoundingClientRect().bottom)) + 'px';
    } else if (nav) nav.style.maxHeight = '';
  }
  window.addEventListener('resize', fitHeader);
  fitHeader();

  /* ---------- 4. ProefBox promo ---------- */
  var KEY = 'gromush-promo';
  var promo = document.getElementById('promo');
  var state;
  try {
    state = JSON.parse(window.sessionStorage.getItem(KEY) || 'null') || { views: 0, state: '' };
    state.views += 1;
    window.sessionStorage.setItem(KEY, JSON.stringify(state));
  } catch (err) {
    return; // no sessionStorage: "once per session" cannot be kept, so the promo stays closed
  }
  function save() { try { window.sessionStorage.setItem(KEY, JSON.stringify(state)); } catch (err) { /* ignore */ } }
  if (!promo || typeof promo.showModal !== 'function' || state.state || state.views < 2) return;
  var neverOn = (promo.getAttribute('data-never-on') || '').split(' ');
  if (neverOn.indexOf(window.location.pathname) !== -1) return;

  var delay = parseFloat(promo.getAttribute('data-delay')) || 8;
  var share = parseFloat(promo.getAttribute('data-scroll')) || 0.4;
  var timer = setTimeout(trigger, delay * 1000);
  function onScroll() {
    var range = document.documentElement.scrollHeight - window.innerHeight;
    if (range > 0 && window.scrollY / range >= share) trigger();
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  function busy() {
    var a = document.activeElement;
    return menuOpen() || toggles.some(isOpen) || document.querySelector('dialog[open]') ||
      (a && /^(INPUT|TEXTAREA|SELECT)$/.test(a.tagName));
  }
  function trigger() {
    clearTimeout(timer);
    if (busy()) { timer = setTimeout(trigger, 3000); return; } // never interrupt a menu, a dialog or typing
    window.removeEventListener('scroll', onScroll);
    state.state = 'shown';
    save();
    promo.showModal();
  }
  promo.addEventListener('close', function () { state.state = 'dismissed'; save(); });
  promo.addEventListener('click', function (e) {
    if (e.target === promo || e.target.closest('.promo-close')) promo.close(); // the button, the backdrop, the margin around the paper
  });
})();
