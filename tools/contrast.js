/* Contrast scan (WCAG 2.2 AA 1.4.3). Run via check.py:
   python3 -I tools/check.py <url> 1440 "$(cat tools/contrast.js)"   -> lines marked FAIL are failures
   Gives wrong readings on color-mix() backgrounds; compute those by hand. Copy of .impeccable/tools/contrast.js. */
document.fonts.ready.then(()=>{
function rgb(s){const m=s.match(/[\d.]+/g);return m?m.map(Number):[0,0,0,0];}
function lum(c){const a=c.slice(0,3).map(v=>{v/=255;return v<=.03928?v/12.92:Math.pow((v+.055)/1.055,2.4)});return .2126*a[0]+.7152*a[1]+.0722*a[2];}
function blend(fg,bg){const a=fg[3]===undefined?1:fg[3];return [0,1,2].map(i=>fg[i]*a+bg[i]*(1-a));}
function bgOf(el){let stack=[];let e=el;while(e){const cs=getComputedStyle(e);const c=rgb(cs.backgroundColor);if(c.length<4)c[3]=1;if(c[3]>0)stack.push(c);if(c[3]>=1)break;e=e.parentElement;}let b=[255,255,255];for(let i=stack.length-1;i>=0;i--)b=blend(stack[i],b);return b;}
function opac(el){let o=1;let e=el;while(e){o*=parseFloat(getComputedStyle(e).opacity);e=e.parentElement;}return o;}
const out={};
document.querySelectorAll('body *').forEach(el=>{
 if(el.closest('svg,.sr-only,[hidden]'))return;
 const t=[...el.childNodes].filter(n=>n.nodeType===3&&n.textContent.trim()).map(n=>n.textContent.trim()).join(' ');
 if(!t)return;const r=el.getBoundingClientRect();if(!r.width)return;
 const cs=getComputedStyle(el);let fg=rgb(cs.color);if(fg.length<4)fg[3]=1;
 const bg=bgOf(el);fg=[...fg.slice(0,3),fg[3]*opac(el)];const f=blend(fg,bg);
 const L1=lum(f),L2=lum(bg);const cr=(Math.max(L1,L2)+.05)/(Math.min(L1,L2)+.05);
 const fs=parseFloat(cs.fontSize),fw=parseInt(cs.fontWeight);const large=fs>=24||(fs>=18.66&&fw>=700);
 const key=f.map(Math.round).join(',')+' on '+bg.map(Math.round).join(',')+(large?' L':'');
 if(!out[key])out[key]={cr:+cr.toFixed(2),need:large?3:4.5,n:0,ex:(el.className||el.tagName)+': '+t.slice(0,40)};
 out[key].n++;
});
return Object.entries(out).sort((a,b)=>a[1].cr-b[1].cr).map(([k,v])=>`${v.cr}${v.cr<v.need?' FAIL':''} [${k}] x${v.n} ${v.ex}`);
})
