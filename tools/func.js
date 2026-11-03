/* Scripted check of the ProefBox form and its mailto hand-off (S5; PRD AC28, AC29, AC30; plan AD7, AD9).
   python3 -I tools/check.py <url>/proefbox/ 390 "$(cat tools/func.js)"   -> ok   (or a JSON list of failures)
   Navigation is intercepted through the test seam of js/forms.js: GroMushForms.navigate(url) is replaced by a
   recorder, so the mailto: URL that submitRequest() would open is read instead of handed to the OS.
   Steps: empty submit (focus on the first invalid field, aria-invalid + aria-describedby, nothing opened); a request
   without an email address (AC30); a valid request (subject names the ProefBox, the body holds every filled field
   as "Label: value" with RFC 6068 encoding, AC28); the hand-off note (address and phone, focus, no "received"
   claim, AC29); "Pas je aanvraag aan" back to the form; a long message shortened with the note. */
(async()=>{
const w=t=>new Promise(r=>setTimeout(r,t));const $=s=>document.querySelector(s);const fails=[];
const ok=(c,m)=>{if(!c)fails.push(m)};
const urls=[];const startHref=location.href;
if(!window.GroMushForms||!GroMushForms.submitRequest){return JSON.stringify(['forms.js not loaded'])}
GroMushForms.navigate=u=>urls.push(u);
const form=$('form[data-form=proefbox]');const btn=form.querySelector('[type=submit]');
const set=(sel,v)=>{const e=$(sel);e.value=v;e.dispatchEvent(new Event('input',{bubbles:true}));e.dispatchEvent(new Event('change',{bubbles:true}))};
const errs=()=>[...form.querySelectorAll('.err')].filter(e=>e.textContent.trim()).map(e=>e.id);
// native no-JS path stays on the element (AC28a)
ok(form.getAttribute('action').startsWith('mailto:info@gromush.be?subject=')&&form.getAttribute('enctype')==='text/plain'&&form.getAttribute('method')==='post','native mailto action/enctype/method');
// 1. empty submit
btn.click();await w(60);
ok(urls.length===0,'empty submit opened a mailto');
ok(document.activeElement&&document.activeElement.id==='f-naam','empty submit: focus not on #f-naam but '+(document.activeElement&&document.activeElement.id));
ok(JSON.stringify(errs())===JSON.stringify(['err-naam','err-zaak','err-type','err-email','err-gemeente']),'empty submit errors: '+errs());
ok($('#f-naam').getAttribute('aria-invalid')==='true'&&($('#f-naam').getAttribute('aria-describedby')||'').split(' ').includes('err-naam'),'aria-invalid/aria-describedby on #f-naam');
ok(location.href===startHref,'page navigated');
// 2. AC30: everything but the email address
set('#f-naam','Jan Peeters');set('#f-zaak','Bistro De Zwam & Co');set('#f-type','Grootkeuken');set('#f-gemeente','Damme');
set('#f-email','jan@');btn.click();await w(60);
ok(urls.length===0,'invalid email opened a mailto');
ok(document.activeElement.id==='f-email'&&JSON.stringify(errs())==='["err-email"]','AC30: focus/flag on email: '+document.activeElement.id+' '+errs());
set('#f-email','');btn.click();await w(60);
ok(urls.length===0&&document.activeElement.id==='f-email','AC30: empty email');
// 3. AC28: a valid request
set('#f-email','jan@voorbeeld.be');set('#f-tel','0499 12 34 56');
$('#chk-gele').click();form.querySelector('input[value="Verras me"]').click();
const msg='Graag een box voor vrijdag.\nKan dat? 100% zeker & #1 = top';
set('#f-bericht',msg);
ok(!$('#f-email').hasAttribute('aria-invalid'),'email still invalid after fix');
btn.click();await w(80);
ok(urls.length===1,'valid submit: '+urls.length+' mailto URLs');
const u=urls[0]||'';
ok(u.startsWith('mailto:info@gromush.be?'),'URL does not start mailto:info@gromush.be?');
const q={};u.slice(u.indexOf('?')+1).split('&').forEach(p=>{const i=p.indexOf('=');q[p.slice(0,i)]=decodeURIComponent(p.slice(i+1))});
ok(/ProefBox/.test(q.subject||''),'subject: '+q.subject);
const body=q.body||'';
['Naam: Jan Peeters','Zaak: Bistro De Zwam & Co','Type zaak: Grootkeuken','E-mail: jan@voorbeeld.be','Leveringsgemeente: Damme','Telefoon: 0499 12 34 56','Soorten: Gele oesterzwam, Verras me','Bericht:\r\nGraag een box voor vrijdag.\r\nKan dat? 100% zeker & #1 = top']
 .forEach(s=>ok(body.includes(s),'body misses '+JSON.stringify(s)));
ok(!/[ +#]/.test(u.slice(u.indexOf('?')))&&u.includes('%0D%0A')&&u.includes('%26')&&u.includes('%23'),'RFC 6068 encoding (spaces, &, #, CRLF)');
// AC29: the hand-off note
const note=$('[data-handoff=proefbox]');
ok(form.hidden&&!note.hidden,'form not replaced by the note');
ok(document.activeElement===note.querySelector('.form-handoff-title'),'focus not on the note title');
const nt=note.textContent;
ok(/verstuur/i.test(nt)&&nt.includes('info@gromush.be')&&nt.includes('0499 24 23 59'),'note lacks send-to-finish, address or phone');
ok(note.querySelector('a[href="mailto:info@gromush.be"]')&&note.querySelector('a[href^="tel:"]')&&note.querySelector('a[href^="https://wa.me/"]'),'note links (mail, tel, WhatsApp)');
ok(!/is ontvangen|is verstuurd|bedankt/i.test(nt),'note claims the request arrived');
ok(note.querySelector('.form-handoff-reopen').getAttribute('href')===u,'reopen link is not the mailto URL');
ok(note.querySelector('.form-handoff-trunc').hidden,'truncation note shown for a short message');
ok(location.href===startHref,'page navigated after submit');
// 4. back to the form, then a long message
note.querySelector('.form-handoff-edit').click();await w(40);
ok(!form.hidden&&note.hidden&&document.activeElement===btn,'edit: form back with focus on submit');
set('#f-bericht','Lang bericht. '.repeat(150));btn.click();await w(80);
const u2=urls[1]||'';const b2=decodeURIComponent((u2.split('&body=')[1])||'');
ok(urls.length===2&&b2.length<=1800,'long body length '+b2.length);
ok(b2.includes('Naam: Jan Peeters')&&b2.includes('[Bericht ingekort'),'long body lost fields or the note');
ok(!note.querySelector('.form-handoff-trunc').hidden,'truncation note not shown on the page');
return fails.length?JSON.stringify(fails):'ok'})()
