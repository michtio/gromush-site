/* Homepage radial opening (S9, AC10a): every visible hypha against every medallion part (curved-label glyphs, pill,
   disc). Prints {paths, hits:{glyph,pill,disc}, ex:[first hits]}. From .impeccable/tools/radiaal/ringnet.js; run by tools/ringprobes.sh. */
document.fonts.ready.then(()=>new Promise(r=>setTimeout(r,300))).then(()=>{
const svg=document.querySelector('.ring-svg');const m=svg.getScreenCTM();
const meds=[...document.querySelectorAll('.ring .med')].map(md=>{const d=md.querySelector('.med-disc').getBoundingClientRect();
 const t=md.querySelector('.med-label text'),M=t.getScreenCTM(),g=[];
 for(let i=0;i<t.getNumberOfChars();i++){const x=t.getExtentOfChar(i);if(!x.width)continue;
  const ps=[[x.x,x.y],[x.x+x.width,x.y],[x.x,x.y+x.height],[x.x+x.width,x.y+x.height]].map(([u,v])=>{const p=svg.createSVGPoint();p.x=u;p.y=v;return p.matrixTransform(M)});
  g.push({x:Math.min(...ps.map(p=>p.x)),y:Math.min(...ps.map(p=>p.y)),right:Math.max(...ps.map(p=>p.x)),bottom:Math.max(...ps.map(p=>p.y))})}
 return {id:md.dataset.variety,cx:d.left+d.width/2,cy:d.top+d.height/2,r:d.width/2,pill:md.querySelector('.pill').getBoundingClientRect(),g}});
const inR=(x,y,b)=>x>b.x&&x<b.right&&y>b.y&&y<b.bottom;
const hits={glyph:0,pill:0,disc:0},ex=[];let n=0;
(()=>{const ns='http://www.w3.org/2000/svg',g=document.createElementNS(ns,'g');svg.appendChild(g);const out=[];document.querySelectorAll('.ring-svg path').forEach(p=>{const b=p.getBoundingClientRect();if(!b.width&&!b.height)return;out.push(p);if(p.dataset.f!==undefined){out.pop();p.getAttribute('d').split('M').filter(Boolean).forEach(sd=>{const q=document.createElementNS(ns,'path');q.setAttribute('d','M'+sd);q.setAttribute('class',p.getAttribute('class'));g.appendChild(q);out.push(q)})}});window.__ringG=g;return out})().forEach(p=>{n++;const L=p.getTotalLength();const seen=new Set();
 for(let s=0;s<=L;s+=3){const q=p.getPointAtLength(s);const sp=svg.createSVGPoint();sp.x=q.x;sp.y=q.y;const r=sp.matrixTransform(m);
  meds.forEach(md=>{let k=null;if((r.x-md.cx)**2+(r.y-md.cy)**2<md.r*md.r)k='disc';else if(inR(r.x,r.y,md.pill))k='pill';else if(md.g.some(b=>inR(r.x,r.y,b)))k='glyph';
   if(k&&!seen.has(md.id+k)){seen.add(md.id+k);hits[k]++;if(ex.length<6)ex.push(md.id+':'+k+' '+(p.dataset.v||p.getAttribute('class')))}})}});
window.__ringG&&window.__ringG.remove();return JSON.stringify({paths:n,hits,ex})})
