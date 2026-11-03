/* 44x44 target sweep (R38, WCAG 2.2 AA plus the site's 44 px bar). Run via check.py:
   python3 -I tools/check.py <url> 390 "$(cat tools/sweep.js)"   -> {"n":0,...}
   Lists visible interactive elements whose effective hit area is under 44x44. Hit areas extended upward
   only can read as false positives; verify those by hand. Copy of .impeccable/tools/sweep.js. */
document.fonts.ready.then(async()=>{document.documentElement.style.scrollBehavior='auto';
const els=[...document.querySelectorAll('a[href],button,input:not([type=hidden]),select,textarea,summary,[tabindex="0"]')];
const out=[];
for(const e of els){let t=e;
 if(e.tagName==='INPUT'){const l=e.closest('label')||(e.id&&document.querySelector('label[for="'+e.id+'"]'));if(l&&['checkbox','radio'].includes(e.type))t=l;}
 const cs=getComputedStyle(t);if(cs.display==='none'||cs.visibility==='hidden'||!t.getClientRects().length)continue;
 if(t.closest('[hidden],[aria-hidden=true]'))continue;
 t.scrollIntoView({block:'center',inline:'center'});await new Promise(r=>setTimeout(r,16));
 const r=t.getBoundingClientRect();if(r.width>=44&&r.height>=44)continue;
 const x=r.left+r.width/2,y=r.top+r.height/2;const hit=(px,py)=>{const q=document.elementFromPoint(px,py);return q&&(q===t||t.contains(q)||q.contains(t)&&false)};
 // 44x44 hit area centred on the element (::before extensions count as the element)
 if(hit(x,y-21.5)&&hit(x,y+21.5)&&hit(x-21.5,y)&&hit(x+21.5,y))continue;
 out.push(t.tagName+'.'+String(t.className).split(' ')[0]+' "'+(t.textContent||'').trim().slice(0,18)+'" '+Math.round(r.width)+'x'+Math.round(r.height));}
scrollTo(0,0);return JSON.stringify({n:out.length,first:out.slice(0,6)})})
