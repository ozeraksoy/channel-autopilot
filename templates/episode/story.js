// The story scene (segment s4) is the heart of an episode: the visual joke lives here.
// Everything is positioned on a 1080x1920 stage. Keep the bottom ~600px clear of important art
// (captions sit at y=1330 and platform buttons cover the bottom and right edge).
// Helpers available: kevSVG(idPrefix, opts) / kv(idPrefix, pose) for characters, T('s4','word') for the time a word
// is spoken, pop(t,t0) for a bouncy appear, seg(t,a,b) for 0..1 progress, sty(id,{css}) to style an element, INK colour.
const heartSVG=(w,c='#FF5A5F')=>`<svg viewBox="0 0 100 90" width="${w}" style="overflow:visible"><path d="M50,84 C10,54 0,34 0,22 C0,6 14,0 26,0 C38,0 46,8 50,16 C54,8 62,0 74,0 C86,0 100,6 100,22 C100,34 90,54 50,84z" fill="${c}" stroke="${INK}" stroke-width="7"/></svg>`;
const STORY={
 html:`<div class="abs" style="inset:0;background:linear-gradient(#BFE9FF,#7CC4F5)"></div>
  <div class="abs" style="left:0;top:1160px;width:1080px;height:760px;background:#2E6FA8;border-top:8px solid ${INK}"></div>
  <div class="abs" id="Dkev" style="left:90px;top:640px;width:260px"></div>
  <div class="abs" id="Dkh" style="left:170px;top:880px">${heartSVG(90)}</div>
  <div class="abs" id="Docto" style="left:520px;top:520px;width:460px"><svg viewBox="0 0 460 560" width="460" style="overflow:visible">
    ${[0,1,2,3,4,5].map(i=>`<path d="M${90+i*56},330 q${i%2?30:-30},110 ${i%2?-10:10},200" fill="none" stroke="${INK}" stroke-width="46" stroke-linecap="round"/><path d="M${90+i*56},330 q${i%2?30:-30},110 ${i%2?-10:10},200" fill="none" stroke="#B26BFF" stroke-width="32" stroke-linecap="round"/>`).join('')}
    <ellipse cx="230" cy="210" rx="190" ry="180" fill="#B26BFF" stroke="${INK}" stroke-width="8"/>
    <circle cx="165" cy="200" r="30" fill="#fff" stroke="${INK}" stroke-width="6"/><circle cx="295" cy="200" r="30" fill="#fff" stroke="${INK}" stroke-width="6"/><circle cx="170" cy="204" r="13" fill="${INK}"/><circle cx="300" cy="204" r="13" fill="${INK}"/>
    <path id="Dom" d="M195,270 q35,30 70,0" fill="none" stroke="${INK}" stroke-width="8" stroke-linecap="round"/></svg></div>
  ${[0,1,2].map(i=>`<div class="abs Dh" style="left:${600+i*110}px;top:${760+(i==1?40:0)}px">${heartSVG(84)}</div>`).join('')}
  <div class="abs L" id="Dstop" style="left:560px;top:420px;font-size:90px;color:#FF5A5F;-webkit-text-stroke:8px ${INK};paint-order:stroke fill">...STOP</div>`,
 hookArt:`<div style="display:flex;justify-content:center;gap:16px">${heartSVG(120)}${heartSVG(120,'#FFD23F')}${heartSVG(120)}</div>`,
 literalArt:`<div style="display:flex;justify-content:center;gap:30px;padding-top:120px">${heartSVG(170)}${heartSVG(170)}${heartSVG(170)}</div>`,
 meaningArt:`<div style="display:flex;justify-content:center;padding-top:150px"><div class="L" style="font-size:200px;color:#fff;-webkit-text-stroke:10px ${INK};paint-order:stroke fill">😮‍💨</div></div>`,
 sticker:heartSVG(180),
 init(){$('Dkev').innerHTML=kevSVG('kD',typeof CH==='function'?CH():{})},
 render(t){
  const doc=T('s4','doctor'),nor=T('s4','normal'),oct=T('s4','octopus'),two=T('s4','two'),thi=T('s4','third'),swi=T('s4','swims'),stop=T('s4','stops');
  kv('kD',{mouth:t>=oct?'o':'smile',eyes:t<oct?'happy':'n',look:t>=oct?1:0,bob:Math.sin(t*4)*3});
  sty('Dkh',{opacity:t>=doc?1:0,transform:`scale(${pop(t,doc)*(1+0.12*Math.max(0,Math.sin(t*9)))})`});
  sty('Docto',{opacity:t>=oct?1:0,transform:`translateY(${(1-pop(t,oct,.5))*700+Math.sin(t*2)*14}px)`});
  const at=[two,two+0.25,thi];
  document.querySelectorAll('.Dh').forEach((e,i)=>{const beating=!(i===2&&t>=stop);
   sty(e,{opacity:t>=at[i]?1:0,filter:beating?'none':'grayscale(1)',transform:`scale(${pop(t,at[i])*(beating?1+0.14*Math.max(0,Math.sin(t*9+i)):0.9)})`})});
  sty('Dstop',{opacity:t>=stop?1:0,transform:`scale(${pop(t,stop)}) rotate(-6deg)`});
 }
};
