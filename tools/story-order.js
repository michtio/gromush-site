/* Homepage story order (S9, PRD R11, AC11), via tools/check.py: the visible scenes ([data-scene] in <main>, not
   display:none at this width) in DOM order, each with its number of keyboard-focusable elements (visible, not inert,
   no negative tabindex), and the positive tabindex count (must be 0, so Tab follows the DOM, which is story order).
   Prints {"order":[...], "focusable":{scene:n}, "positiveTabindex":0}. Expected order at every width:
   opening, levering, assortiment, kweek, tafels, kweker, proefbox (R11; the opening holds both drawings). */
document.fonts.ready.then(()=>{
const vis=e=>{const cs=getComputedStyle(e);if(cs.display==='none'||cs.visibility==='hidden')return false;const r=e.getBoundingClientRect();return r.width>0&&r.height>0};
const scenes=[...document.querySelectorAll('main [data-scene]')].filter(s=>{let e=s;while(e&&e!==document.body){if(getComputedStyle(e).display==='none')return false;e=e.parentElement}return true});
const sel='a[href],button:not([disabled]),input:not([disabled]):not([type=hidden]),select:not([disabled]),textarea:not([disabled]),[tabindex]';
const focusable={};
scenes.forEach(s=>{focusable[s.dataset.scene]=[...s.querySelectorAll(sel)].filter(e=>e.tabIndex>=0&&!e.closest('[inert]')&&vis(e)).length});
return JSON.stringify({order:scenes.map(s=>s.dataset.scene),focusable,positiveTabindex:[...document.querySelectorAll('[tabindex]')].filter(e=>e.tabIndex>0).length})})
