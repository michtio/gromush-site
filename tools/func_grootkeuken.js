/* Scripted check of the Grootkeukens needs form and its helper (S13; PRD R19, R20, R33, R34, AC19, AC20, AC28-AC32).
   python3 -I tools/check.py "<url>/voor-wie/grootkeukens/?gemeente=brugge" 390 "$(cat tools/func_grootkeuken.js)"
   -> ok   (or a JSON list of failures)
   Navigation is intercepted through the test seam of js/forms.js (GroMushForms.navigate), as in tools/func.js.
   Steps: 1. structure: the helper is the first fieldset of the form, holds the four questions, the start-up statement
   (when present) comes before it, ?gemeente=brugge picks the town, the progress line counts it, the primary actions
   reach the form, the contact link pre-selects Grootkeuken (AC31), privacy line, no captcha, no kg/price on the page;
   2. empty submit: focus on the first invalid field, nothing opened (AC30); 3. a valid request: subject names the
   form, the body holds the four helper answers and every other field as "Label: value" (AC20, AC28); the hand-off
   note shows the address and phone/WhatsApp and claims nothing was received (AC29). */
(async()=>{
const w=t=>new Promise(r=>setTimeout(r,t));const $=s=>document.querySelector(s);const fails=[];
const ok=(c,m)=>{if(!c)fails.push(m)};
const urls=[];const startHref=location.href;
if(!window.GroMushForms||!GroMushForms.submitRequest){return JSON.stringify(['forms.js not loaded'])}
GroMushForms.navigate=u=>urls.push(u);
const form=$('form[data-form=grootkeuken]');if(!form)return JSON.stringify(['no grootkeuken form']);
const btn=form.querySelector('[type=submit]');const note=$('[data-handoff=grootkeuken]');
const set=(sel,v)=>{const e=$(sel);e.value=v;e.dispatchEvent(new Event('input',{bubbles:true}));e.dispatchEvent(new Event('change',{bubbles:true}))};
const pick=(name,value)=>{const r=[...form.querySelectorAll('input[name="'+name+'"]')].find(i=>i.value===value);if(!r){fails.push('no option '+name+'='+value);return}r.click()};
const errs=()=>[...form.querySelectorAll('.err')].filter(e=>e.textContent.trim()).map(e=>e.id);
const parse=u=>{const q={};u.slice(u.indexOf('?')+1).split('&').forEach(p=>{const i=p.indexOf('=');q[p.slice(0,i)]=decodeURIComponent(p.slice(i+1))});return q};
const main=document.querySelector('main');
// 1. structure
ok(form.getAttribute('action').startsWith('mailto:info@gromush.be?subject=')&&form.getAttribute('enctype')==='text/plain'&&form.getAttribute('method')==='post','native mailto action/enctype/method');
const helper=form.querySelector('[data-section=helper]');
ok(helper&&helper.tagName==='FIELDSET','helper is not a fieldset');
ok(helper&&form.querySelector('fieldset')===helper,'helper is not the first fieldset of the form');
const q4=helper?[...helper.querySelectorAll('[data-field]')].map(e=>e.getAttribute('data-field')):[];
ok(JSON.stringify(q4)==='["maaltijden","frequentie","soorten","gemeente"]','helper questions: '+JSON.stringify(q4));
const st=$('[data-section=startup]');
if(st){ok(st.compareDocumentPosition(helper)&Node.DOCUMENT_POSITION_FOLLOWING,'start-up statement not above the helper');
  ok(/opstartfase/.test(st.textContent)&&/niet garanderen/.test(st.textContent),'start-up statement text')}
ok([...form.querySelectorAll('input[name=gemeente]')].find(i=>i.value==='Brugge')?.checked,'?gemeente=brugge did not pick Brugge');
const prog=form.querySelector('[data-progress]');
ok(prog&&!prog.hidden&&prog.textContent.trim()==='1 van 4 vragen beantwoord','progress: '+(prog&&prog.textContent));
['hero','slot'].forEach(s=>ok([...document.querySelectorAll('[data-section='+s+'] a[data-primary-action]')].some(a=>a.textContent.trim()==='Bespreek jouw behoefte'&&new URL(a.href).pathname.endsWith('/voor-wie/grootkeukens/')&&new URL(a.href).hash==='#behoefte'),'primary action missing in '+s));
ok(document.getElementById('behoefte')&&document.getElementById('behoefte').contains(form),'#behoefte does not hold the form');
const contactLinks=[...main.querySelectorAll('a[href*="/contact/"]')];
ok(contactLinks.length&&contactLinks.every(a=>new URL(a.href).searchParams.get('reden')==='grootkeuken'),'a contact link without ?reden=grootkeuken');
ok(form.querySelector('.form-privacy a[href$="/privacy/"]'),'no privacy line');
ok(!/captcha|puzzel/i.test(main.innerHTML)&&!main.querySelector('iframe'),'captcha/puzzle/iframe on the page');
ok(!/kg|kilo|€/i.test(main.textContent),'kg/kilo/€ in the page text');
ok(/info@gromush\.be/.test(main.textContent)&&main.querySelector('a[href^="tel:"]')&&main.querySelector('a[href^="https://wa.me/"]'),'address/phone/WhatsApp not next to the form');
// 2. empty submit (AC30)
btn.click();await w(60);
ok(urls.length===0,'empty submit opened a mailto');
ok(document.activeElement.id==='f-naam','empty submit: focus on '+document.activeElement.id);
ok(JSON.stringify(errs())==='["err-naam","err-organisatie","err-email"]','empty submit errors: '+errs());
ok($('#f-email').getAttribute('aria-invalid')==='true'&&($('#f-email').getAttribute('aria-describedby')||'').includes('err-email'),'email not flagged with aria');
// 3. valid request
pick('maaltijden','1.000 tot 5.000');pick('frequentie','2 tot 3 keer per week');
$('#chk-gele').click();$('#chk-blauwe').click();
await w(20);
ok(prog.textContent.trim()==='4 van 4 vragen beantwoord','progress after answers: '+prog.textContent);
set('#f-naam','Sofie Peeters');set('#f-organisatie','WZC De Duinen');set('#f-type','Woonzorgcentrum');set('#f-functie','Keukenchef');
set('#f-email','sofie@deduinen.be');set('#f-tel','050 12 34 56');set('#f-leverfrequentie','Wekelijks');set('#f-bericht','Wij koken twee warme maaltijden per dag.');
btn.click();await w(80);
ok(urls.length===1,'valid submit: '+urls.length+' mailto URLs '+errs());
const u=urls[0]||'';const q=parse(u);const body=q.body||'';
ok(u.startsWith('mailto:info@gromush.be?'),'URL does not start mailto:info@gromush.be?');
ok(q.subject==='Behoefte grootkeuken','subject: '+q.subject);
['Maaltijden per dag: 1.000 tot 5.000','Paddenstoelen op het menu: 2 tot 3 keer per week','Soorten: Gele oesterzwam, Blauwe oesterzwam','Leveringsgemeente: Brugge',
 'Naam: Sofie Peeters','Organisatie: WZC De Duinen','Type keuken: Woonzorgcentrum','Functie: Keukenchef','E-mail: sofie@deduinen.be','Telefoon: 050 12 34 56','Leverfrequentie: Wekelijks','Bericht:\r\nWij koken twee warme maaltijden per dag.']
 .forEach(s=>ok(body.includes(s),'body misses '+JSON.stringify(s)));
ok(!/kg|kilo|€/i.test(body),'kg/price in the mail body');
ok(form.hidden&&!note.hidden&&document.activeElement===note.querySelector('.form-handoff-title'),'hand-off note not shown/focused');
ok(/verstuur/i.test(note.textContent)&&note.querySelector('a[href="mailto:info@gromush.be"]')&&note.querySelector('a[href^="tel:"]')&&note.querySelector('a[href^="https://wa.me/"]'),'note lacks send-to-finish or the alternatives');
ok(!/is ontvangen|is verstuurd|bedankt/i.test(note.textContent),'note claims the request arrived');
// back to the form: answers kept
note.querySelector('.form-handoff-edit').click();await w(40);
ok(!form.hidden&&note.hidden&&[...form.querySelectorAll('input[name=maaltijden]')].find(i=>i.checked)?.value==='1.000 tot 5.000','edit: form or answers not back');
ok(location.href===startHref,'page navigated');
return fails.length?JSON.stringify(fails):'ok'})()
