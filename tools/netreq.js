/* Request hosts and cookies (R41, AC37). Run via check.py after the page has loaded:
   python3 -I tools/check.py <url> 390 "$(cat tools/netreq.js)"
   -> {"hosts":["127.0.0.1:8770"],"thirdParty":[],"cookie":"","storage":[...]}
   hosts: every host the page fetched from (navigation and resource timing: CSS, JS, fonts, images,
   fetch/XHR); thirdParty: hosts other than the page's own; cookie: document.cookie (must be "").
   storage lists sessionStorage/localStorage keys for information (the promo uses sessionStorage, AD15). */
new Promise(r=>setTimeout(r,500)).then(()=>{
const own=location.host;
const urls=[location.href,...performance.getEntriesByType('resource').map(e=>e.name)];
const hosts=[...new Set(urls.filter(u=>/^https?:/.test(u)).map(u=>new URL(u).host))].sort();
let storage=[];try{storage=[...Object.keys(sessionStorage).map(k=>'session:'+k),...Object.keys(localStorage).map(k=>'local:'+k)]}catch(e){}
return JSON.stringify({hosts,thirdParty:hosts.filter(h=>h!==own),cookie:document.cookie,storage});})
