// Shared character rig & animation helpers
const INK='#1F1A2E';
const clamp=(x,a=0,b=1)=>Math.max(a,Math.min(b,x));
const seg=(t,a,b)=>clamp((t-a)/(b-a));
const oc=x=>1-Math.pow(1-x,3), io=x=>x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2;
const ob=x=>{const c1=1.9,c3=c1+1;return x<=0?0:1+c3*Math.pow(x-1,3)+c1*Math.pow(x-1,2)};
const pop=(t,t0,d=.35)=>ob(seg(t,t0,t0+d));
const $=id=>document.getElementById(id);
function sty(id,o){const e=typeof id==='string'?$(id):id;if(!e)return;for(const k in o)e.style[k]=o[k]}

// Kevin: p = id prefix. opts: shirt, hair
// Accessory presets drawn in head coordinates (head centre = 0,0, radius 98). Use via character.accessory in theme.json.
const ACC={none:'',
 glasses:`<g fill="none" stroke="${INK}" stroke-width="7"><circle cx="-36" cy="0" r="30"/><circle cx="36" cy="0" r="30"/><path d="M-6,0 h12 M-66,-4 L-96,-12 M66,-4 L96,-12"/></g>`,
 cap:`<path d="M-100,-40 C-96,-128 96,-128 100,-40z" fill="#FF5A5F" stroke="${INK}" stroke-width="8"/><path d="M40,-46 q80,-6 96,26 q-50,-14 -96,-8z" fill="#FF5A5F" stroke="${INK}" stroke-width="7"/>`,
 beanie:`<path d="M-100,-36 C-100,-150 100,-150 100,-36z" fill="#3B82F6" stroke="${INK}" stroke-width="8"/><rect x="-104" y="-56" width="208" height="34" rx="14" fill="#fff" stroke="${INK}" stroke-width="7"/><circle cy="-128" r="18" fill="#fff" stroke="${INK}" stroke-width="6"/>`,
 bow:`<g transform="translate(60,-96)"><path d="M0,0 L-44,-26 L-44,26z M0,0 L44,-26 L44,26z" fill="#FF5A5F" stroke="${INK}" stroke-width="7" stroke-linejoin="round"/><circle r="12" fill="#FF5A5F" stroke="${INK}" stroke-width="6"/></g>`,
 headphones:`<path d="M-104,6 C-110,-150 110,-150 104,6" fill="none" stroke="${INK}" stroke-width="16"/><rect x="-128" y="-22" width="36" height="66" rx="14" fill="#FFD23F" stroke="${INK}" stroke-width="7"/><rect x="92" y="-22" width="36" height="66" rx="14" fill="#FFD23F" stroke="${INK}" stroke-width="7"/>`};
// HAIR presets (head coordinates).
const HAIRS={short:h=>`<path d="M-96,-20 C-100,-90 -40,-118 10,-110 C60,-118 104,-80 96,-24 C80,-60 60,-70 30,-66 C10,-90 -30,-80 -40,-60 C-60,-70 -86,-50 -96,-20z" fill="${h}" stroke="${INK}" stroke-width="7"/>`,
 long:h=>`<path d="M-100,90 C-124,-40 -80,-124 0,-118 C80,-124 124,-40 100,90 C92,40 96,-10 80,-40 C40,-74 -40,-74 -80,-40 C-96,-10 -92,40 -100,90z" fill="${h}" stroke="${INK}" stroke-width="7"/>`,
 bun:h=>`<circle cy="-118" r="34" fill="${h}" stroke="${INK}" stroke-width="7"/><path d="M-96,-20 C-100,-90 -40,-112 0,-108 C40,-112 100,-90 96,-20 C70,-66 -70,-66 -96,-20z" fill="${h}" stroke="${INK}" stroke-width="7"/>`,
 curly:h=>[[-80,-50],[-52,-88],[-12,-104],[30,-100],[66,-78],[88,-44]].map(([x,y])=>`<circle cx="${x}" cy="${y}" r="34" fill="${h}" stroke="${INK}" stroke-width="7"/>`).join(''),
 bald:h=>''};
function kevSVG(p,o={}){const shirt=o.shirt||'#23C9B6', hair=o.hair||'#7A4A2A', skin=o.skin||'#FFD3A8', pants=o.pants||'#3D5A99';
 const hairS=(HAIRS[o.hairStyle||'short']||HAIRS.short)(hair); const acc=(o.hat||'')+(ACC[o.accessory||'none']||'');
 return `<svg viewBox="0 0 300 520" width="100%" style="overflow:visible"><g id="${p}all">
  <g id="${p}legL" transform="translate(115,360)"><rect x="-22" y="0" width="44" height="130" rx="18" fill="${pants}" stroke="${INK}" stroke-width="7"/><ellipse cx="-6" cy="132" rx="34" ry="18" fill="${INK}"/></g>
  <g id="${p}legR" transform="translate(185,360)"><rect x="-22" y="0" width="44" height="130" rx="18" fill="${pants}" stroke="${INK}" stroke-width="7"/><ellipse cx="6" cy="132" rx="34" ry="18" fill="${INK}"/></g>
  <g id="${p}armL" transform="translate(78,235)"><rect x="-20" y="-6" width="40" height="125" rx="20" fill="${shirt}" stroke="${INK}" stroke-width="7"/><circle cy="128" r="22" fill="${skin}" stroke="${INK}" stroke-width="6"/></g>
  <rect x="70" y="210" width="160" height="175" rx="50" fill="${shirt}" stroke="${INK}" stroke-width="8"/>
  <path d="M120,215 q30,30 60,0" fill="none" stroke="${INK}" stroke-width="6"/>
  <g id="${p}armR" transform="translate(222,235)"><rect x="-20" y="-6" width="40" height="125" rx="20" fill="${shirt}" stroke="${INK}" stroke-width="7"/><g id="${p}hold" transform="translate(0,140)">${o.hold||''}</g><circle cy="128" r="22" fill="${skin}" stroke="${INK}" stroke-width="6"/></g>
  <g id="${p}head" transform="translate(150,120)">
   ${o.hairStyle==='long'?hairS:''}<circle r="98" fill="${skin}" stroke="${INK}" stroke-width="8"/>
   <circle cx="-98" cy="10" r="18" fill="${skin}" stroke="${INK}" stroke-width="6"/><circle cx="98" cy="10" r="18" fill="${skin}" stroke="${INK}" stroke-width="6"/>
   ${o.hairStyle==='long'?`<path d="M-90,-40 C-60,-84 60,-84 90,-40 C60,-62 -60,-62 -90,-40z" fill="${hair}" stroke="${INK}" stroke-width="7"/>`:hairS}
   <g id="${p}eyesN"><circle cx="-36" cy="0" r="20" fill="#fff" stroke="${INK}" stroke-width="5"/><circle cx="36" cy="0" r="20" fill="#fff" stroke="${INK}" stroke-width="5"/><circle class="${p}pp" cx="-34" cy="2" r="9" fill="${INK}"/><circle class="${p}pp" cx="38" cy="2" r="9" fill="${INK}"/></g>
   <g id="${p}eyesH" style="display:none"><path d="M-54,4 q18,-20 36,0 M18,4 q18,-20 36,0" fill="none" stroke="${INK}" stroke-width="7" stroke-linecap="round"/></g>
   <g id="${p}brows" style="display:none"><path d="M-56,-30 L-18,-22 M56,-30 L18,-22" stroke="${INK}" stroke-width="7" stroke-linecap="round"/></g>
   <g id="${p}sadbrows" style="display:none"><path d="M-56,-24 L-18,-34 M56,-24 L18,-34" stroke="${INK}" stroke-width="7" stroke-linecap="round"/></g>
   <path d="M-8,28 q8,14 18,0" fill="none" stroke="${INK}" stroke-width="5" stroke-linecap="round"/>
   <path id="${p}mS" d="M-30,52 q30,26 60,0" fill="none" stroke="${INK}" stroke-width="7" stroke-linecap="round"/>
   <path id="${p}mF" style="display:none" d="M-26,66 q26,-22 52,0" fill="none" stroke="${INK}" stroke-width="7" stroke-linecap="round"/>
   <path id="${p}mB" style="display:none" d="M-26,58 L26,58" fill="none" stroke="${INK}" stroke-width="7" stroke-linecap="round"/>
   <ellipse id="${p}mO" cx="0" cy="58" rx="16" ry="20" fill="#7A2130" stroke="${INK}" stroke-width="6" style="display:none"/>
   <g id="${p}tears" style="display:none"><path class="${p}tr" d="M-40,20 q-6,14 0,22 q6,-8 0,-22z" fill="#5FB8FF" stroke="${INK}" stroke-width="3"/><path class="${p}tr" d="M40,20 q-6,14 0,22 q6,-8 0,-22z" fill="#5FB8FF" stroke="${INK}" stroke-width="3"/></g>
   <g id="${p}hat">${acc}</g>
  </g></g></svg>`}
// kv(p,{mouth:'smile'|'frown'|'flat'|'o', eyes:'n'|'happy', brows:'angry'|'sad'|null, tears:t, walk:phase, armR, armL, bob, tilt, look})
function kv(p,o){const m=o.mouth||'smile';[['mS','smile'],['mF','frown'],['mB','flat'],['mO','o']].forEach(([id,k])=>{const e=$(p+id);if(e)e.style.display=m===k?'block':'none'});
 $(p+'eyesN').style.display=o.eyes==='happy'?'none':'block';$(p+'eyesH').style.display=o.eyes==='happy'?'block':'none';
 $(p+'brows').style.display=o.brows==='angry'?'block':'none';$(p+'sadbrows').style.display=o.brows==='sad'?'block':'none';
 const tr=$(p+'tears');tr.style.display=o.tears!==undefined&&o.tears!==null?'block':'none';
 if(o.tears!=null)tr.setAttribute('transform',`translate(0,${(o.tears*60)%60})`);
 const a=o.walk!==undefined?Math.sin(o.walk)*18:0;
 $(p+'legL').setAttribute('transform',`translate(115,360) rotate(${a})`);$(p+'legR').setAttribute('transform',`translate(185,360) rotate(${-a})`);
 $(p+'armL').setAttribute('transform',`translate(78,235) rotate(${-a*.8+(o.armL||0)})`);$(p+'armR').setAttribute('transform',`translate(222,235) rotate(${(o.armR||0)+a*.8})`);
 $(p+'head').setAttribute('transform',`translate(150,${120+(o.bob||0)}) rotate(${o.tilt||0})`);
 if(o.look!==undefined)document.querySelectorAll('.'+p+'pp').forEach((c,i)=>c.setAttribute('cx',(i?38:-34)+o.look*8));}

function flagSVG(code,w){return `<svg viewBox="0 0 30 20" preserveAspectRatio="none" width="${w}" height="${w*2/3}">${F[code]}</svg>`}
function bigArrow(fill){return `<svg viewBox="0 0 240 230" width="100%"><path d="M80,0 h80 v110 h70 L120,225 L10,110 h70z" fill="${fill}" stroke="${INK}" stroke-width="9" stroke-linejoin="round"/></svg>`}
