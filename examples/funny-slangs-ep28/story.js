const trainSVG=w=>`<svg viewBox="-110 -80 220 120" width="${w}" style="overflow:visible"><rect x="-100" y="-30" width="70" height="44" rx="8" fill="#23C9B6" stroke="${INK}" stroke-width="6"/><rect x="-20" y="-40" width="110" height="54" rx="10" fill="#FF5A5F" stroke="${INK}" stroke-width="6"/><rect x="40" y="-70" width="44" height="34" rx="6" fill="#FF5A5F" stroke="${INK}" stroke-width="6"/><rect x="-6" y="-66" width="18" height="28" fill="${INK}"/><rect x="48" y="-62" width="28" height="18" rx="3" fill="#BDE6FF" stroke="${INK}" stroke-width="4"/><circle cx="-80" cy="22" r="13" fill="${INK}"/><circle cx="-48" cy="22" r="13" fill="${INK}"/><circle cx="0" cy="22" r="15" fill="${INK}"/><circle cx="64" cy="22" r="15" fill="${INK}"/><path d="M90,10 l18,10 l-18,4z" fill="#FFD23F" stroke="${INK}" stroke-width="4"/></svg>`;
const STORY={
 html:`<div class="abs" style="inset:0;background:#E9E3D6"></div>
  <div class="abs" style="left:0;top:1160px;width:1080px;height:760px;background:#A0714F;border-top:8px solid ${INK}"></div>
  <div class="abs" style="left:50px;top:270px;width:640px;height:330px;background:#2F5D50;border:14px solid #8B5A2B;border-radius:8px;box-shadow:0 0 0 6px ${INK}"><div id="Dform" style="position:absolute;inset:16px 24px;font-family:'Comic Sans MS',N;font-weight:700;font-size:46px;line-height:72px;color:#F4F4EC"></div></div>
  <div class="abs" id="Dprof" style="left:740px;top:640px;width:290px"></div>
  <div class="abs" id="Dkev" style="left:120px;top:700px;width:260px"></div>
  <div class="abs" style="left:70px;top:990px;width:380px;height:40px;background:#C98B5A;border:8px solid ${INK};border-radius:8px"></div>
  <div class="abs" style="left:90px;top:1030px;width:340px;height:130px;background:#B5742A;border:8px solid ${INK};border-top:none"></div>
  <div class="abs" id="Dcloud" style="left:360px;top:380px;width:430px;height:260px"><svg viewBox="0 0 430 260" width="430" style="position:absolute;inset:0;overflow:visible"><path d="M60,200 q-60,-10 -40,-70 q-20,-70 60,-80 q20,-50 90,-30 q50,-40 110,0 q70,-20 90,40 q60,20 30,90 q20,60 -60,60 q-30,30 -100,10 q-60,30 -110,0 q-60,10 -70,-20z" fill="#fff" stroke="${INK}" stroke-width="8"/><circle cx="20" cy="250" r="16" fill="#fff" stroke="${INK}" stroke-width="6"/><circle cx="-10" cy="290" r="10" fill="#fff" stroke="${INK}" stroke-width="5"/></svg>
   <div id="Dempty" class="L" style="position:absolute;left:0;right:0;top:80px;text-align:center;font-size:60px;color:#9AA6B8">*empty*</div>
   <div id="Dsign" style="position:absolute;left:70px;top:70px;width:290px;background:#1F4E9C;border:7px solid ${INK};border-radius:10px;font-family:L;font-size:50px;color:#fff;text-align:center;padding:10px 0">🚉 BAHNHOF</div></div>
  <div class="abs" id="Dtrain" style="left:0;top:740px">${trainSVG(170)}</div>
  <div class="abs" id="Dsmoke"></div>
  <div class="abs L" id="Dchoo" style="left:40px;top:600px;font-size:80px;color:#FF5A5F;-webkit-text-stroke:6px ${INK};paint-order:stroke fill">CHOO CHOO!</div>`,
 literalArt:`<div style="display:flex;justify-content:center;padding-top:110px"><div style="position:relative;width:460px;height:300px"><div style="position:absolute;left:30px;top:0;width:400px;background:#1F4E9C;border:9px solid ${INK};border-radius:14px;font-family:L;font-size:66px;color:#fff;text-align:center;padding:16px 0">🚉 BAHNHOF</div><div id="Ct" style="position:absolute;left:0;top:170px">${trainSVG(260)}</div></div></div>`,
 meaningArt:`<div style="display:flex;justify-content:center;padding-top:200px"><div id="Eq" class="L" style="font-size:230px;color:#FF5A5F;-webkit-text-stroke:10px ${INK};paint-order:stroke fill">???</div></div>`,
 sticker:trainSVG(200),
 init(){$('Dkev').innerHTML=kevSVG('kD',{shirt:'#FFCE00'});$('Dprof').innerHTML=kevSVG('pD',{shirt:'#7A6A58',hair:'#E6E6E6',skin:'#F2C9A0'});
  $('Dsmoke').innerHTML=[...Array(4)].map(()=>`<div class="abs Ds" style="width:50px;height:50px;border-radius:50%;background:#fff;border:5px solid ${INK}"></div>`).join('')},
 literal(t,at){sty('Ct',{transform:`translateX(${Math.sin(t*2)*60+60}px) translateY(${-Math.abs(Math.sin(t*16))*4}px)`})},
 meaning(t,at){sty('Eq',{transform:`rotate(${Math.sin(t*5)*6}deg) scale(${1+Math.sin(t*8)*0.04})`})},
 render(t){
  const pr=T('s4','professor'),qu=T('s4','quantum'),ei=T('s4','eigenvalues'),th=T('s4','thermodynamics'),br=T('s4','brain'),em=T('s4','empty'),on=T('s4','only'),stn=T('s4','station'),ti=T('s4','tiny'),ch=T('s4','choo'),ri=T('s4','right');
  const F=[[qu,'Ψ = ∮ ε·dΣ²'],[ei,'λ(Ĥ) − ∂Ω/∂t = 0'],[th,'ΔS ≥ ħ / 2kT']];
  $('Dform').innerHTML=F.filter(f=>t>=f[0]).map(f=>`<div>${f[1]}</div>`).join('');
  const talk=t>=pr&&t<br;
  kv('pD',{mouth:talk?(Math.sin(t*18)>0?'o':'smile'):'smile',armR:talk?-110+Math.sin(t*6)*20:0,look:-1});
  sty('Dprof',{transform:'scaleX(-1)'});
  const lost=t>=br;
  kv('kD',{mouth:t>=ti?'o':(lost?'flat':'smile'),eyes:'n',brows:lost&&t<stn?'sad':null,look:t<br?-1:0,tilt:t>=ti?Math.sin(t*6)*5:0});
  sty('Dcloud',{opacity:t>=br?1:0,transform:`scale(${pop(t,br)})`,transformOrigin:'10% 100%'});
  sty('Dempty',{opacity:t>=em&&t<stn?1:0});
  sty('Dsign',{opacity:t>=stn?1:0,transform:`scale(${pop(t,stn)})`});
  const tp=clamp(seg(t,ti,ri+0.8));
  sty('Dtrain',{opacity:t>=ti&&tp<1?1:0,transform:`translate(${-60+tp*520}px,${-Math.abs(Math.sin(t*14))*6}px)`});
  document.querySelectorAll('.Ds').forEach((e,i)=>{const k=((t-ti)*1.5+i/4)%1;const x=-60+tp*520+130-k*60;sty(e,{opacity:t>=ti&&tp<1?1-k:0,left:x+'px',top:(730-k*120)+'px',transform:`scale(${0.5+k})`})});
  sty('Dchoo',{opacity:t>=ch&&tp<1?1:0,transform:`scale(${pop(t,ch)}) rotate(-6deg)`});
 }
};
