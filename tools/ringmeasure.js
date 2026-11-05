/* Homepage radial opening (S9): obstacles in ring-svg units (viewBox 1320x780), the input of src/gen/hyphae.py
   (src/gen/hyphae_obs/obs-<width>.json). Copied from .impeccable/tools/radiaal/measure.js; run by tools/ring_obstacles.py. */
document.fonts.ready.then(()=>new Promise(r=>setTimeout(r,300))).then(()=>{
const svg=document.querySelector('.ring-svg');const inv=svg.getScreenCTM().inverse();
const P=(x,y)=>{const p=svg.createSVGPoint();p.x=x;p.y=y;const q=p.matrixTransform(inv);return [q.x,q.y]};
const R=r=>{const a=P(r.left,r.top),b=P(r.right,r.bottom);return [a[0],a[1],b[0],b[1]].map(v=>Math.round(v*10)/10)};
const core={};
[['h1','.ring-core h1'],['intro','.ring-core .support'],['slip','.ring-core .slip'],['tapel','.ring-core .tape--l'],['taper','.ring-core .tape--r'],['note','.ring-core .slip-note']].forEach(([k,s])=>core[k]=R(document.querySelector(s).getBoundingClientRect()));
const meds={};
document.querySelectorAll('.ring .med').forEach(m=>{const d=m.querySelector('.med-disc').getBoundingClientRect();
 const c=P(d.left+d.width/2,d.top+d.height/2),e=P(d.right,d.top+d.height/2);
 const t=m.querySelector('.med-label text'),M=t.getScreenCTM();const g=[];
 for(let i=0;i<t.getNumberOfChars();i++){const x=t.getExtentOfChar(i);if(!x.width)continue;
  const pts=[[x.x,x.y],[x.x+x.width,x.y],[x.x,x.y+x.height],[x.x+x.width,x.y+x.height]].map(([u,v])=>{const p=svg.createSVGPoint();p.x=u;p.y=v;const s=p.matrixTransform(M);return P(s.x,s.y)});
  const xs=pts.map(p=>p[0]),ys=pts.map(p=>p[1]);g.push([Math.min(...xs),Math.min(...ys),Math.max(...xs),Math.max(...ys)].map(v=>Math.round(v*10)/10))}
 meds[m.dataset.variety]={c:c.map(v=>Math.round(v*10)/10),r:Math.round((e[0]-c[0])*10)/10,pill:R(m.querySelector('.pill').getBoundingClientRect()),glyphs:g}});
return JSON.stringify({w:innerWidth,core,meds})})
