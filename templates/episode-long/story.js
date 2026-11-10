// Long-form story: one object per scene id listed in ep.json → "scenes".
// Each scene: bg (css), html (1920x1080 stage, keep y<900 clear of the caption line), init(), render(t, lt, p)
//   t = absolute time · lt = seconds since this scene started · p = 0..1 progress through the scene
// Blocks: bullets()/bulletsRender(), bigText()/linesRender(), counter(), kevSVG()/kv(), T('c3','word'), AT('c3:word'), pop(), seg(), sty().
const heart=(w,c='#FF5A5F',id='')=>`<svg ${id?`id="${id}"`:''} viewBox="0 0 100 90" width="${w}" style="overflow:visible"><path d="M50,84 C10,54 0,34 0,22 C0,6 14,0 26,0 C38,0 46,8 50,16 C54,8 62,0 74,0 C86,0 100,6 100,22 C100,34 90,54 50,84z" fill="${c}" stroke="${INK}" stroke-width="7"/></svg>`;
const octo=(w,id)=>`<svg id="${id}" viewBox="0 0 460 560" width="${w}" style="overflow:visible">
 ${[0,1,2,3,4,5].map(i=>`<path d="M${90+i*56},330 q${i%2?30:-30},110 ${i%2?-10:10},200" fill="none" stroke="${INK}" stroke-width="46" stroke-linecap="round"/><path d="M${90+i*56},330 q${i%2?30:-30},110 ${i%2?-10:10},200" fill="none" stroke="#B26BFF" stroke-width="32" stroke-linecap="round"/>`).join('')}
 <ellipse cx="230" cy="210" rx="190" ry="180" fill="#B26BFF" stroke="${INK}" stroke-width="8"/>
 <circle cx="165" cy="200" r="30" fill="#fff" stroke="${INK}" stroke-width="6"/><circle cx="295" cy="200" r="30" fill="#fff" stroke="${INK}" stroke-width="6"/><circle cx="170" cy="204" r="13" fill="${INK}"/><circle cx="300" cy="204" r="13" fill="${INK}"/></svg>`;
const beat=(t,k=0)=>1+0.14*Math.max(0,Math.sin(t*9+k));
const STORY={scenes:{
 intro:{bg:'linear-gradient(#BFE9FF,#7CC4F5)',
  html:`<div class="abs" style="left:0;top:820px;width:1920px;height:260px;background:#2E6FA8;border-top:8px solid ${INK}"></div>
   <div class="abs" id="i_octo" style="left:1180px;top:210px">${octo(440,'i_o')}</div>
   ${[0,1,2].map(i=>`<div class="abs i_h" style="left:${1240+i*110}px;top:${470+(i==1?36:0)}px">${heart(84)}</div>`).join('')}
   <div class="abs" id="i_kev" style="left:170px;top:420px;width:230px"></div>
   ${bigText('i_q',[["THREE HEARTS.","w",120],["ONE KEEPS STOPPING.","cor",96]],{top:150})}
   <div class="abs cen" id="i_why" style="top:420px"><span class="chip" style="font-size:64px;background:#fff">...so it walks?!</span></div>`,
  init(){$('i_kev').innerHTML=kevSVG('kI',CH());sty('i_q',{left:'0',right:'700px'});sty('i_why',{right:'700px'})},
  render(t){const st=T('c1','stops'),th=T('c1','three'),wk=T('c2','reason');
   kv('kI',{mouth:t>=st?'o':'smile',brows:t>=st?'sad':null,look:1,bob:Math.sin(t*4)*3});
   linesRender('i_q',t,['c1:three','c1:stops']);
   document.querySelectorAll('.i_h').forEach((e,i)=>{const dead=i===2&&t>=st;sty(e,{opacity:t>=th+i*0.15?1:0,filter:dead?'grayscale(1)':'none',transform:`scale(${pop(t,th+i*0.15)*(dead?0.9:beat(t,i))})`})});
   sty('i_octo',{transform:`translateY(${Math.sin(t*2)*12}px)`});sty('i_why',{opacity:t>=wk?1:0,transform:`scale(${pop(t,wk)}) rotate(-3deg)`})}},
 plumbing:{bg:'var(--cream)',
  html:`<div class="abs card" style="left:1040px;top:170px;width:760px;height:700px;background:#DDF3FF"></div>
   <div class="abs" style="left:1210px;top:230px">${octo(420,'p_o')}</div>
   <div class="abs p_g" style="left:1130px;top:560px">${heart(90,'#FFD23F')}</div><div class="abs p_g" style="left:1620px;top:560px">${heart(90,'#FFD23F')}</div>
   <div class="abs" id="p_big" style="left:1345px;top:470px">${heart(150)}</div>
   <div class="abs T" style="left:140px;top:170px;font-size:84px">How the blood moves</div>
   ${bullets('p_b',[{text:'Two <b>gill hearts</b> push blood through the gills',at:'c3:two'},{text:'Blood picks up <b>oxygen</b> there',at:'c3:oxygen.'},{text:'One <b>big heart</b> sends it to the whole body',at:'c4:third'}],{left:140,top:320,width:840})}`,
  render(t){bulletsRender('p_b',t);const g=T('c3','two'),b=T('c4','third');
   document.querySelectorAll('.p_g').forEach((e,i)=>sty(e,{opacity:t>=g?1:0,transform:`scale(${pop(t,g+i*0.2)*beat(t,i)})`}));
   sty('p_big',{opacity:t>=b?1:0,transform:`scale(${pop(t,b)*beat(t,2)})`})}},
 catch:{bg:'linear-gradient(#9AD6FF,#2E6FA8)',
  html:`<div class="abs" id="c_octo" style="left:200px;top:260px">${octo(400,'c_o')}</div>
   <div class="abs" id="c_big" style="left:330px;top:500px">${heart(140)}</div>
   <div class="abs card" style="left:1080px;top:200px;width:700px;height:330px;text-align:center;padding-top:30px"><div class="B" style="font-size:44px">Big heart while swimming</div><div class="T" id="c_num" style="font-size:170px;line-height:1.1"></div></div>
   <div class="abs cen" id="c_walk" style="top:610px;left:900px"><span class="chip" style="font-size:60px;background:var(--teal);color:#fff">Walking = all three working</span></div>`,
  render(t){const sw=T('c5','swims'),pa=T('c5','pauses'),wa=T('c6','crawling');const swim=t>=sw&&t<wa;
   sty('c_octo',{transform:`translate(${swim?seg(t,sw,wa)*260:260-seg(t,wa,wa+1)*260}px,${Math.sin(t*(swim?7:2))*14}px)`});
   const stopped=t>=pa&&t<wa;sty('c_big',{filter:stopped?'grayscale(1)':'none',transform:`translate(${swim?seg(t,sw,wa)*260:260-seg(t,wa,wa+1)*260}px,0) scale(${stopped?0.9:beat(t)})`});
   $('c_num').textContent=t<pa?'60 bpm':stopped?'0 bpm':'60 bpm';$('c_num').style.color=stopped?'var(--cor)':'var(--ink)';
   sty('c_walk',{opacity:t>=wa?1:0,transform:`scale(${pop(t,wa)})`})}},
 outro:{bg:'radial-gradient(circle at 50% 40%,#FFE680,#FFD23F 62%,#F5B800)',
  html:`<div class="abs" id="o_kev" style="left:330px;top:540px;width:230px"></div>
   ${bigText('o_q',[["WHICH ANIMAL","w",120],["SHOULD WE OPEN UP NEXT?","cor",96]],{top:200})}
   <div class="abs" id="o_f" style="left:1040px;top:560px"><span class="chip" style="font-size:64px;background:var(--cor);color:#fff" id="o_ft"></span></div>`,
  init(){$('o_kev').innerHTML=kevSVG('kO',CH());$('o_ft').textContent=((TH.labels&&TH.labels.follow)||'FOLLOW')+' '+TH.handle},
  render(t){linesRender('o_q',t,['c7:which','c7:open']);const f=T('c7',(TH.cta&&TH.cta.followWord)||'follow');
   kv('kO',{eyes:'happy',armR:t>=f?-150+Math.sin(t*12)*14:0,bob:Math.sin(t*5)*5});sty('o_f',{opacity:t>=f?1:0,transform:`scale(${pop(t,f)})`})}}
}};
