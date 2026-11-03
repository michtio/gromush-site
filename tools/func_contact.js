/* Scripted check of the contact form: reason selector, pre-selection and the home-cook pick-up mode (S6; PRD R32,
   R33, R42, AC31, AC38; plan AD7, AD10). Run it on the order link that product pages use:
   python3 -I tools/check.py "<url>/contact/?reden=bestelling-thuis&soort=blauwe-oesterzwam" 390 "$(cat tools/func_contact.js)"
   -> ok   (or a JSON list of failures)
   Navigation is intercepted through the test seam of js/forms.js (GroMushForms.navigate), as in tools/func.js.
   Steps: 1. pre-selection (reason, variety by slug), pick-up copy shown, no address or price on the page;
   2. an order request: subject names the form and the reason, the body lists the fields and says Anthony confirms
   the pick-up personally, the hand-off note says it too, neither holds an address or a price (AC38);
   3. back to the form, reason Grootkeuken: the order fields fold away, the message is required again, the mail has no
   pick-up line; 4. empty submit focuses the reason selector and opens nothing; 5. the reasons match R32. */
(async()=>{
const w=t=>new Promise(r=>setTimeout(r,t));const $=s=>document.querySelector(s);const fails=[];
const ok=(c,m)=>{if(!c)fails.push(m)};
const urls=[];const startHref=location.href;
if(!window.GroMushForms||!GroMushForms.submitRequest){return JSON.stringify(['forms.js not loaded'])}
GroMushForms.navigate=u=>urls.push(u);
const form=$('form[data-form=contact]');const btn=form.querySelector('[type=submit]');const note=$('[data-handoff=contact]');
const set=(sel,v)=>{const e=$(sel);e.value=v;e.dispatchEvent(new Event('input',{bubbles:true}));e.dispatchEvent(new Event('change',{bubbles:true}))};
const shown=e=>!!e&&!e.closest('[hidden]')&&getComputedStyle(e).display!=='none'&&e.getBoundingClientRect().height>0;
const errs=()=>[...form.querySelectorAll('.err')].filter(e=>e.textContent.trim()).map(e=>e.id);
const parse=u=>{const q={};u.slice(u.indexOf('?')+1).split('&').forEach(p=>{const i=p.indexOf('=');q[p.slice(0,i)]=decodeURIComponent(p.slice(i+1))});return q};
const ADDRESS=/€|\bEUR\b|prijs|\b\d{4}\b|straat|laan|\bweg\b|Westkapelle/i;  // a price, a postcode, a street, the locality
const R32=['Chef / restaurant','Grootkeuken','Speciaalzaak','Bestelling thuis (afhalen)','Adoptie emmer','Interesse buitenkweek','School of vereniging','Samenwerking','Andere'];
// native no-JS path (AC28a)
ok(form.getAttribute('action').startsWith('mailto:info@gromush.be?subject=')&&form.getAttribute('enctype')==='text/plain'&&form.getAttribute('method')==='post','native mailto action/enctype/method');
// 1. pre-selection from ?reden=bestelling-thuis&soort=blauwe-oesterzwam (AD10)
ok($('#f-reden').value==='bestelling-thuis','reden not pre-selected: '+$('#f-reden').value);
ok($('#chk-blauwe').checked,'?soort=blauwe-oesterzwam did not tick the blue oyster');
const mn=$('.mode-note');
ok(shown(mn),'pick-up copy not shown');
ok(/Anthony bevestigt/.test(mn.textContent)&&/persoonlijk/.test(mn.textContent)&&/oogstdagen wisselen/i.test(mn.textContent)&&/overschrijving/.test(mn.textContent)&&/cash/.test(mn.textContent),'pick-up copy misses confirm/harvest/payment');
ok(!ADDRESS.test(mn.textContent),'pick-up copy holds an address or price: '+mn.textContent);
ok(!/€/.test(document.querySelector('main').textContent),'a € on the page');
ok(shown($('#f-soorten'))&&shown($('#f-hoeveelheid')),'order fields not shown');
ok(!shown($('#f-organisatie'))&&!shown($('#f-onderwerp')),'business fields shown in pick-up mode');
ok(btn.textContent.trim()==='Vraag mijn bestelling aan','submit text: '+btn.textContent.trim());
ok(!$('#f-bericht').required,'message required in pick-up mode');
ok(($('#f-hoeveelheid').getAttribute('aria-describedby')||'').includes('hint-hoeveelheid'),'quantity hint not described');
// 2. an order request (AC38)
set('#f-naam','Els Claeys');set('#f-email','els@voorbeeld.be');set('#f-tel','0470 11 22 33');set('#f-hoeveelheid','500 g');
$('#chk-roze').click();
btn.click();await w(80);
ok(urls.length===1,'order submit: '+urls.length+' mailto URLs '+errs());
const u=urls[0]||'';const q=parse(u);const body=q.body||'';
ok(u.startsWith('mailto:info@gromush.be?'),'URL does not start mailto:info@gromush.be?');
ok(q.subject==='Contactaanvraag: Bestelling thuis (afhalen)','subject: '+q.subject);
['Reden: Bestelling thuis (afhalen)','Naam: Els Claeys','E-mail: els@voorbeeld.be','Telefoon: 0470 11 22 33','Soorten: Roze oesterzwam, Blauwe oesterzwam','Hoeveelheid: 500 g','Bericht: niet ingevuld','Afhalen: Anthony bevestigt de bestelling, het afhaalmoment en de plaats persoonlijk.']
 .forEach(s=>ok(body.includes(s),'order body misses '+JSON.stringify(s)));
ok(!/Organisatie:|Onderwerp:/.test(body),'order body holds folded business fields');
ok(!ADDRESS.test(body.replace(/0470 11 22 33/,'')),'order body holds an address or price');
ok(form.hidden&&!note.hidden&&document.activeElement===note.querySelector('.form-handoff-title'),'hand-off note not shown/focused');
const hm=note.querySelector('.form-handoff-mode');
ok(shown(hm)&&/Anthony bevestigt/.test(hm.textContent)&&/persoonlijk/.test(hm.textContent),'hand-off note does not say Anthony confirms the pick-up personally');
ok(!ADDRESS.test(hm.textContent),'hand-off pick-up line holds an address or price');
ok(/verstuur/i.test(note.textContent)&&note.querySelector('a[href="mailto:info@gromush.be"]')&&note.querySelector('a[href^="tel:"]')&&note.querySelector('a[href^="https://wa.me/"]'),'note lacks send-to-finish or the alternatives');
ok(!/is ontvangen|is verstuurd|bedankt/i.test(note.textContent),'note claims the request arrived');
// 3. back to the form, another reason
note.querySelector('.form-handoff-edit').click();await w(40);
ok(!form.hidden&&note.hidden,'edit: form not back');
set('#f-reden','grootkeuken');await w(40);
ok(!shown($('.mode-note'))&&!shown($('#f-soorten'))&&!shown($('#f-hoeveelheid')),'order fields still shown for Grootkeuken');
ok(shown($('#f-organisatie'))&&shown($('#f-onderwerp')),'business fields hidden for Grootkeuken');
ok($('#f-bericht').required&&btn.textContent.trim()==='Verstuur mijn bericht','message not required again / submit text '+btn.textContent.trim());
btn.click();await w(60);
ok(urls.length===1&&document.activeElement.id==='f-bericht'&&JSON.stringify(errs())==='["err-bericht"]','empty message not flagged: '+errs());
set('#f-organisatie','WZC De Duinen');set('#f-onderwerp','Wekelijkse levering');set('#f-bericht','Wij koken 300 maaltijden per dag.');
btn.click();await w(80);
const q2=parse(urls[1]||'');const b2=q2.body||'';
ok(q2.subject==='Contactaanvraag: Grootkeuken','subject 2: '+q2.subject);
['Reden: Grootkeuken','Organisatie: WZC De Duinen','Onderwerp: Wekelijkse levering','Bericht:\r\nWij koken 300 maaltijden per dag.'].forEach(s=>ok(b2.includes(s),'body 2 misses '+JSON.stringify(s)));
ok(!/Afhalen:|Soorten:|Hoeveelheid:/.test(b2),'body 2 holds pick-up lines');
ok(!shown(note.querySelector('.form-handoff-mode')),'pick-up line in the hand-off note for Grootkeuken');
// 4. empty submit
note.querySelector('.form-handoff-edit').click();await w(40);
['#f-naam','#f-email','#f-tel','#f-organisatie','#f-onderwerp','#f-bericht'].forEach(s=>set(s,''));set('#f-reden','');
btn.click();await w(60);
ok(urls.length===2,'empty submit opened a mailto');
ok(document.activeElement.id==='f-reden','empty submit: focus on '+document.activeElement.id);
ok(JSON.stringify(errs())==='["err-reden","err-naam","err-email","err-bericht"]','empty submit errors: '+errs());
ok(location.href===startHref,'page navigated');
// 5. R32: the reasons, in order
const reasons=[...$('#f-reden').options].filter(o=>o.value).map(o=>o.textContent.trim());
ok(JSON.stringify(reasons)===JSON.stringify(R32),'reasons: '+JSON.stringify(reasons));
return fails.length?JSON.stringify(fails):'ok'})()
