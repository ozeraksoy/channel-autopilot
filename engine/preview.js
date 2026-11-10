// node engine/preview.js <theme.json> <out.png>
// Renders a one-page style sheet (badge, palette, caption sample, main character in several moods)
// so the channel owner can SEE a theme / character before any episode is produced.
const {chromium}=require('playwright');const fs=require('fs');const path=require('path');
(async()=>{const themePath=path.resolve(process.argv[2]);const out=path.resolve(process.argv[3]||'theme_preview.png');
const TH=JSON.parse(fs.readFileSync(themePath,'utf8'));const E=__dirname;const c=Object.assign({ink:'#1F1A2E',accent:'#FFD23F',accent2:'#FF5A5F',accent3:'#23C9B6',paper:'#FFF6E0'},TH.colors||{});
const moods=[['happy',{eyes:'happy',armR:-150}],['neutral',{}],['shocked',{mouth:'o',brows:'sad'}],['angry',{mouth:'frown',brows:'angry'}],['sad',{mouth:'frown',brows:'sad',tears:0.3}]];
const html=`<!doctype html><meta charset="utf-8"><style>
@font-face{font-family:L;src:url(file://${E}/fonts/lilita-latin.woff2);unicode-range:U+0000-00FF}
@font-face{font-family:L;src:url(file://${E}/fonts/lilita-ext.woff2);unicode-range:U+0100-024F}
@font-face{font-family:N;font-weight:900;src:url(file://${E}/fonts/nunito-latin.woff2);unicode-range:U+0000-00FF}
@font-face{font-family:N;font-weight:900;src:url(file://${E}/fonts/nunito-ext.woff2);unicode-range:U+0100-024F}
*{margin:0;box-sizing:border-box}body{width:1600px;height:1000px;background:${c.paper};font-family:N;font-weight:900;color:${c.ink};position:relative;overflow:hidden}
.b{position:absolute;font-family:L;font-size:46px;background:#fff;border:6px solid ${c.ink};border-radius:50px;padding:8px 30px 4px;box-shadow:0 7px 0 ${c.ink}}
.b b{color:${c.accent2};font-weight:400}.sw{display:inline-block;width:150px;height:110px;border:6px solid ${c.ink};border-radius:20px;margin-right:16px;box-shadow:0 7px 0 ${c.ink};vertical-align:top;font-size:19px;line-height:1.1;padding:58px 0 0 10px}
.L{font-family:L;color:#fff;-webkit-text-stroke:12px ${c.ink};paint-order:stroke fill;text-transform:uppercase}
.k{position:absolute;top:470px;width:210px;text-align:center;font-size:26px}</style>
<div class="b" style="left:60px;top:50px">${(TH.brand&&TH.brand.a)||''} <b>${(TH.brand&&TH.brand.b)||''}</b></div>
<div class="b" style="left:60px;top:150px;background:${c.accent2};color:#fff">${((TH.labels&&TH.labels.follow)||'FOLLOW')+' '+(TH.handle||'')}</div>
<div style="position:absolute;left:60px;top:270px">${Object.entries(c).map(([k,v])=>`<span class="sw" style="background:${v};color:${k==='ink'?'#fff':c.ink}">${k}<br>${v}</span>`).join('')}</div>
<div style="position:absolute;left:940px;top:60px;width:600px;text-align:center;background:linear-gradient(#8FD3FF,#D8F1FF);border:6px solid ${c.ink};border-radius:30px;padding:40px 10px 30px">
 <div class="L" style="font-size:84px;line-height:1.05"><span>CAPTION </span><span style="color:${c.accent}">SAMPLE</span></div>
 <div class="b" style="position:static;display:inline-block;margin-top:26px;background:${c.accent}">${(TH.labels&&TH.labels.unpack)||'LITERALLY'}</div>
 <div class="b" style="position:static;display:inline-block;margin-top:26px;background:${c.accent3};color:#fff">${(TH.labels&&TH.labels.takeaway)||'MEANING'}</div></div>
${moods.map(([n],i)=>`<div class="k" style="left:${70+i*300}px"><div id="k${i}"></div>${n}</div>`).join('')}
<div style="position:absolute;left:60px;bottom:26px;font-size:26px">Main character: ${(TH.character&&TH.character.name)||'(unnamed)'} · hair: ${(TH.character&&TH.character.hairStyle)||'short'} · accessory: ${(TH.character&&TH.character.accessory)||'none'}</div>
<script>${fs.readFileSync(E+'/characters.js','utf8')}
const CH=${JSON.stringify(TH.character||{})};const M=${JSON.stringify(moods)};
M.forEach(([n,o],i)=>{document.getElementById('k'+i).innerHTML=kevSVG('p'+i,CH);kv('p'+i,o)});</script>`;
const tmp=out+'.html';fs.writeFileSync(tmp,html);const b=await chromium.launch();const p=await b.newPage({viewport:{width:1600,height:1000}});const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.goto('file://'+tmp);await p.evaluate(()=>document.fonts.ready);await p.screenshot({path:out});await b.close();fs.unlinkSync(tmp);console.log('preview',out,errs.join(' | '))})();
