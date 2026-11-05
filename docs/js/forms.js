/* GroMush request forms (S5; plan AD7, AD9, AD10; PRD R33, R38). Loaded only on pages with a form
   (partials/form.html). Progressive: without this script the form posts natively to its mailto: action with
   enctype="text/plain", and the browser checks the required fields.
   1. Validation: inline, per field. A field is checked when it loses focus with a value, and again on every change
      once it is invalid; submit checks every field and moves focus to the first invalid one. Invalid fields get
      aria-invalid="true" and their message (#err-<name>) in aria-describedby.
   2. Pre-selection (AD10): ?soort=<variety key or slug> ticks that variety (?soort=blauwe or
      ?soort=blauwe-oesterzwam); ?<name>=<value> picks an option in a select marked data-prefill="<name>"
      (contact: ?reden=); a radio group marked data-prefill picks the option whose text matches (?gemeente=brugge).
   2b. Progress (S13): a fieldset holding [data-progress] shows "{n} van {total}" answered fields (hidden without JS).
   2a. Modes (S6, PRD R42): a form with data-mode-field="<select name>" switches mode with that select; the chosen
      option's data-mode ("afhalen") is the mode. Elements with data-mode-only="<mode>" show only in that mode,
      data-mode-not="<mode>" hide in it, data-optional-in="<mode>" makes a required field optional in it (in the
      form and its hand-off note). Hidden fields are skipped by validation and left out of the mail. The submit
      text (data-text-<mode>), a status announcement (data-mode-<mode>-announce) and one extra mail line
      (data-mode-<mode>-mail-label / -mail) follow the mode. data-subject-field="<select name>" adds the chosen
      option's text to the mail subject. Without JS every mode element shows (the order fields are optional).
   3. Hand-off (AD7, AD9): submitRequest(form, data) builds one mailto: to the form's recipient with the form's
      subject and a "Label: value" line per field (RFC 6068: percent-encoded UTF-8, CRLF line breaks), keeps the
      body under MAX_BODY characters by shortening the message with a note, and opens it. A form service can
      replace this one function later. The page then shows the hand-off note: the request only arrives once the
      visitor sends that mail; it never says the request was received.
   Test seam: GroMushForms.navigate(url) does the navigation; tools/func.js replaces it to read the URL. */
(function () {
  'use strict';
  var MAX_BODY = 1800; /* characters of the decoded body; some mail clients cut long mailto: URLs (AD7) */
  var CRLF = '\r\n';
  var api = window.GroMushForms = window.GroMushForms || {};
  api.navigate = api.navigate || function (url) { window.location.href = url; };

  /* ---------- 3. hand-off ---------- */
  function mailtoUrl(recipient, subject, body) {
    return 'mailto:' + recipient + '?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
  }

  /* data: {recipient, subject, lines: [{label, value, block}], truncatedNote}. A "block" value (the message) goes
     on its own lines under its label and is the one that is shortened when the body is too long. */
  function buildBody(data) {
    var head = [], blocks = [];
    data.lines.forEach(function (l) {
      if (l.block) blocks.push(l); else head.push(l.label + ': ' + l.value);
    });
    var fixed = head.join(CRLF);
    var truncated = false;
    var parts = blocks.map(function (b) { return b.label + ':' + CRLF + b.value.replace(/\r?\n/g, CRLF); });
    var body = [fixed].concat(parts).join(CRLF + CRLF);
    if (body.length > MAX_BODY && blocks.length) {
      truncated = true;
      var last = blocks[blocks.length - 1];
      var others = [fixed].concat(parts.slice(0, -1)).join(CRLF + CRLF);
      var prefix = last.label + ':' + CRLF;
      var suffix = '…' + CRLF + CRLF + data.truncatedNote;
      var room = Math.max(0, MAX_BODY - others.length - (CRLF + CRLF).length - prefix.length - suffix.length);
      /* never cut an emoji in half: a lone surrogate makes encodeURIComponent throw */
      var text = last.value.replace(/\r?\n/g, CRLF).slice(0, room).replace(/[\uD800-\uDBFF]$/, '').replace(/\s+$/, '');
      body = others + CRLF + CRLF + prefix + text + suffix;
    }
    return {body: body, truncated: truncated};
  }

  function submitRequest(form, data) {
    var built = buildBody(data);
    var url = mailtoUrl(data.recipient, data.subject, built.body);
    api.navigate(url);
    return {url: url, truncated: built.truncated};
  }
  api.submitRequest = submitRequest;
  api.buildBody = buildBody;

  /* ---------- 1. validation ---------- */
  var EMAIL = /^[^\s@]+@[^\s@.]+(\.[^\s@.]+)+$/;
  function check(input) {
    var value = input.value.trim();
    if (input.type === 'tel') {
      var digits = value.replace(/\D/g, '');
      return value === '' ? !input.required : (/^[+()\d\s./-]+$/.test(value) && digits.length >= 8 && digits.length <= 15);
    }
    if (value === '') return !input.required;
    if (input.type === 'email') return value.length <= 254 && EMAIL.test(value) && !/^\.|\.\.|\.@/.test(value);
    return true;
  }
  function describe(input, errId, on) {
    var ids = (input.getAttribute('aria-describedby') || '').split(/\s+/).filter(function (x) { return x && x !== errId; });
    if (on) ids.push(errId);
    if (ids.length) input.setAttribute('aria-describedby', ids.join(' ')); else input.removeAttribute('aria-describedby');
  }
  function validate(input) {
    var errId = 'err-' + input.name;
    var err = document.getElementById(errId);
    var wrap = input.closest('.field');
    var ok = check(input);
    if (ok) input.removeAttribute('aria-invalid'); else input.setAttribute('aria-invalid', 'true');
    describe(input, errId, !ok);
    if (err) err.textContent = ok ? '' : (input.getAttribute('data-error') || '');
    if (wrap) wrap.classList.toggle('invalid', !ok);
    return ok;
  }

  function inactive(el) { return el.disabled || !!el.closest('[hidden]'); }
  function clearField(input) {
    input.removeAttribute('aria-invalid');
    describe(input, 'err-' + input.name, false);
    var err = document.getElementById('err-' + input.name);
    if (err) err.textContent = '';
    var wrap = input.closest('.field');
    if (wrap) wrap.classList.remove('invalid');
  }

  function collect(form) {
    var empty = form.getAttribute('data-empty') || '';
    var wraps = Array.prototype.filter.call(form.querySelectorAll('[data-field]'), function (w) { return !inactive(w); });
    return wraps.map(function (wrap) {
      var name = wrap.getAttribute('data-field');
      var label = wrap.getAttribute('data-label');
      var value, block = false;
      if (wrap.tagName === 'FIELDSET') {
        value = Array.prototype.filter.call(wrap.querySelectorAll('input[type=checkbox], input[type=radio]'), function (c) { return c.checked; })
          .map(function (c) { return c.value; }).join(', ');
      } else {
        var input = form.elements[name];
        value = input.value.trim();
        /* a select's mail value is the visible option text (the contact reason key reads as its label) */
        if (input.tagName === 'SELECT' && value !== '') value = input.options[input.selectedIndex].textContent.trim();
        block = input.tagName === 'TEXTAREA' && value !== '';
      }
      return {label: label, value: value || empty, block: block};
    });
  }

  /* ---------- per form ---------- */
  document.querySelectorAll('form[data-form]').forEach(function (form) {
    var key = form.getAttribute('data-form');
    var note = document.querySelector('[data-handoff="' + key + '"]');
    var controls = Array.prototype.filter.call(form.querySelectorAll('input, select, textarea'), function (el) {
      return el.type !== 'checkbox' && el.type !== 'radio';
    });
    form.noValidate = true;

    controls.forEach(function (input) {
      input.addEventListener('blur', function () {
        if (input.value.trim() !== '' || input.getAttribute('aria-invalid') === 'true') validate(input);
      });
      ['input', 'change'].forEach(function (type) {
        input.addEventListener(type, function () { if (input.getAttribute('aria-invalid') === 'true') validate(input); });
      });
    });

    /* 2. pre-selection from the query string (AD10) */
    var params;
    try { params = new URLSearchParams(window.location.search); } catch (e) { params = null; }
    if (params) {
      form.querySelectorAll('[data-prefill]').forEach(function (el) {
        var value = params.get(el.getAttribute('data-prefill'));
        if (!value) return;
        if (el.tagName === 'SELECT') {
          if (Array.prototype.some.call(el.options, function (o) { return o.value === value && value !== ''; })) el.value = value;
        } else {
          var safe = value.toLowerCase().replace(/[^a-z0-9-]/g, '');
          var box = safe && el.querySelector('input[type=checkbox][data-key="' + safe + '"], input[type=checkbox][data-slug="' + safe + '"]');
          /* a radio group (S13): the option whose text reads as the value (?gemeente=knokke-heist) */
          if (!box && safe) box = Array.prototype.filter.call(el.querySelectorAll('input[type=radio]'), function (r) {
            return r.value.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '') === safe;
          })[0];
          if (box) box.checked = true;
        }
      });
    }

    /* 2b. progress (S13): a group with [data-progress="{n} van {total} …"] counts its answered fields */
    form.querySelectorAll('[data-progress]').forEach(function (p) {
      var group = p.closest('fieldset');
      var wraps = group ? group.querySelectorAll('[data-field]') : [];
      function answered(w) {
        if (w.tagName === 'FIELDSET') return !!w.querySelector('input:checked');
        var c = form.elements[w.getAttribute('data-field')];
        return !!c && c.value.trim() !== '';
      }
      function update() {
        var n = Array.prototype.filter.call(wraps, answered).length;
        p.textContent = p.getAttribute('data-progress').replace('{n}', n).replace('{total}', wraps.length);
        p.classList.toggle('is-complete', n === wraps.length);
      }
      if (!wraps.length) return;
      group.addEventListener('change', update);
      group.addEventListener('input', update);
      update();
      p.hidden = false;
    });

    /* 2a. modes (R42): the mode follows the chosen option of data-mode-field */
    var modeField = form.getAttribute('data-mode-field');
    var modeSelect = modeField ? form.elements[modeField] : null;
    var live = form.querySelector('[data-mode-live]');
    var submitBtn = form.querySelector('[type=submit]');
    var mode = '';
    function currentMode() {
      var opt = modeSelect && modeSelect.options[modeSelect.selectedIndex];
      return (opt && opt.getAttribute('data-mode')) || '';
    }
    function applyMode(announce) {
      var next = currentMode();
      var changed = next !== mode;
      mode = next;
      var scopes = [form].concat(note ? [note] : []);
      scopes.forEach(function (scope) {
        scope.querySelectorAll('[data-mode-only], [data-mode-not]').forEach(function (el) {
          var only = el.getAttribute('data-mode-only');
          var not = el.getAttribute('data-mode-not');
          el.hidden = only !== null ? only !== mode : not === mode;
          if (el.hidden) el.querySelectorAll('input, select, textarea').forEach(function (c) { if (c.type !== 'checkbox') clearField(c); });
        });
      });
      form.querySelectorAll('[data-optional-in]').forEach(function (wrap) {
        var optional = wrap.getAttribute('data-optional-in') === mode;
        var input = form.elements[wrap.getAttribute('data-field')];
        if (input) {
          input.required = !optional;
          if (input.getAttribute('aria-invalid') === 'true') validate(input);
        }
        wrap.querySelectorAll('[data-mark=required]').forEach(function (m) { m.hidden = optional; });
        wrap.querySelectorAll('[data-mark=optional]').forEach(function (m) { m.hidden = !optional; });
      });
      if (submitBtn) submitBtn.textContent = (mode && submitBtn.getAttribute('data-text-' + mode)) || submitBtn.getAttribute('data-text-default') || submitBtn.textContent;
      if (announce && changed && live) live.textContent = (mode && form.getAttribute('data-mode-' + mode + '-announce')) || '';
      form.setAttribute('data-mode-ready', mode || 'none');
    }
    if (modeSelect) {
      applyMode(false);
      modeSelect.addEventListener('change', function () { applyMode(true); });
    }

    function subject() {
      var base = form.getAttribute('data-subject');
      var field = form.getAttribute('data-subject-field');
      var sel = field ? form.elements[field] : null;
      var opt = sel && sel.value && sel.options[sel.selectedIndex];
      return opt ? base + ': ' + opt.textContent.trim() : base;
    }
    function lines() {
      var out = collect(form);
      var label = mode && form.getAttribute('data-mode-' + mode + '-mail-label');
      var text = mode && form.getAttribute('data-mode-' + mode + '-mail');
      if (label && text) out.push({label: label, value: text, block: false});
      return out;
    }

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      controls.forEach(function (input) {
        if (input.tagName === 'INPUT') input.value = input.value.replace(/\s+/g, ' ').trim();
      });
      var firstInvalid = null;
      controls.forEach(function (input) {
        if (inactive(input)) return;
        if (!validate(input) && !firstInvalid) firstInvalid = input;
      });
      if (firstInvalid) { firstInvalid.focus(); return; }
      var result = submitRequest(form, {
        recipient: form.getAttribute('data-recipient'),
        subject: subject(),
        lines: lines(),
        truncatedNote: form.getAttribute('data-truncated') || ''
      });
      if (!note) return;
      var reopen = note.querySelector('.form-handoff-reopen');
      if (reopen) reopen.href = result.url;
      var trunc = note.querySelector('.form-handoff-trunc');
      if (trunc) trunc.hidden = !result.truncated;
      form.hidden = true;
      note.hidden = false;
      var title = note.querySelector('.form-handoff-title');
      if (title) title.focus();
    });

    if (note) {
      var edit = note.querySelector('.form-handoff-edit');
      if (edit) edit.addEventListener('click', function () {
        note.hidden = true;
        form.hidden = false;
        var submit = form.querySelector('[type=submit]');
        if (submit) submit.focus();
      });
    }
  });
})();
