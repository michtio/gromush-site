/* Homepage radial opening (S9, AC10a): every visible hypha against the title block (h1, intro, slip with tape and
   note), and the title block against every medallion part. Prints a list of hits ([] = clear). From .impeccable/tools/radiaal/ringlabel.js. */
document.fonts.ready.then(()=>new Promise(r=>setTimeout(r,300))).then(()=>{
const svg=document.querySelector('.ring-svg');const m=svg.getScreenCTM();
const core=[['h1','.ring-core h1'],['intro','.ring-core .support'],['slip','.ring-core .slip'],['tape-l','.ring-core .tape--l'],['tape-r','.ring-core .tape--r'],['note','.ring-core .slip-note']].map(([n,s])=>({n,r:document.querySelector(s).getBoundingClientRect()}));
const parts=[...document.querySelectorAll('.ring .med')].flatMap(md=>[{n:md.dataset.variety+':disc',r:md.querySelector('.med-disc').getBoundingClientRect()},{n:md.dataset.variety+':pill',r:md.querySelector('.pill').getBoundingClientRect()},{n:md.dataset.variety+':label',r:md.querySelector('.med-label text').getBoundingClientRect()}]);
const ov=(a,b)=>a.x<b.right&&a.right>b.x&&a.y<b.bottom&&a.bottom>b.y;const out=[];
core.forEach(c=>parts.forEach(p=>{if(ov(c.r,p.r))out.push(c.n+' x '+p.n)}));
(()=>{const ns='http://www.w3.org/2000/svg',g=document.createElementNS(ns,'g');svg.appendChild(g);const out=[];document.querySelectorAll('.ring-svg path').forEach(p=>{const b=p.getBoundingClientRect();if(!b.width&&!b.height)return;out.push(p);if(p.dataset.f!==undefined){out.pop();p.getAttribute('d').split('M').filter(Boolean).forEach(sd=>{const q=document.createElementNS(ns,'path');q.setAttribute('d','M'+sd);q.setAttribute('class',p.getAttribute('class'));g.appendChild(q);out.push(q)})}});window.__ringG=g;return out})().forEach(p=>{const L=p.getTotalLength();
 for(let s=0;s<=L;s+=3){const q=p.getPointAtLength(s);const sp=svg.createSVGPoint();sp.x=q.x;sp.y=q.y;const r=sp.matrixTransform(m);
  const c=core.find(c=>r.x>c.r.x&&r.x<c.r.right&&r.y>c.r.y&&r.y<c.r.bottom);if(c){out.push('line x '+c.n+' ('+(p.dataset.v||p.getAttribute('class'))+')');break}}});
window.__ringG&&window.__ringG.remove();return JSON.stringify(out)})
