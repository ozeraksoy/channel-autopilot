// node shots.js <epdir> [t1 t2 ...] -> <epdir>/sheet.jpg  (control frames; long episodes: two per segment, max 48)
const {chromium}=require('playwright');const fs=require('fs');const path=require('path');const {execSync}=require('child_process');
(async()=>{const ep=path.resolve(process.argv[2]);const T=JSON.parse(fs.readFileSync(ep+'/timing.json'));const o=T.off;
const EPJ=JSON.parse(fs.readFileSync(ep+'/ep.json'));const LONG=EPJ.format==='long';const VP=LONG?{width:1920,height:1080}:{width:1080,height:1920};
const auto=()=>{const segs=T.order||Object.keys(o);let a=[];for(const s of segs){const e=(T.segend&&T.segend[s])||o[s]+2;a.push(o[s]+Math.min(0.9,(e-o[s])*0.3),o[s]+(e-o[s])*0.8)}const max=48;if(a.length>max){const st=a.length/max;a=Array.from({length:max},(_,i)=>a[Math.floor(i*st)])}return a.map(x=>Math.round(x*10)/10)};
const ts=process.argv.length>3?process.argv.slice(3).map(Number):LONG?auto():[o.s1+2.5,o.s2-0.4,o.s2+0.9,o.s3+1.5,o.s4-0.4,o.s4+2,o.s4+(o.s5-o.s4)*0.3,o.s4+(o.s5-o.s4)*0.5,o.s4+(o.s5-o.s4)*0.7,o.s5-0.5,o.s5+1.5,o.s6-0.5,o.s7-0.5,o.s7+1.5,T.end-1.3,o.s6+1.5].map(x=>Math.round(x*10)/10);
const b=await chromium.launch();const p=await b.newPage({viewport:VP});const errs=[];p.on('pageerror',e=>errs.push(e.message));p.on('console',m=>{if(m.type()==='error')errs.push(m.text())});
await p.goto('file://'+ep+'/build.html');await p.evaluate(()=>document.fonts.ready);fs.mkdirSync(ep+'/chk',{recursive:true});
for(const t of ts){await p.evaluate(t=>{for(let x=0;x<=t;x+=0.5)window.render(x);window.render(t)},t);await p.screenshot({path:`${ep}/chk/${t}.jpg`,type:'jpeg',quality:70});}
await b.close();
execSync('python3 '+__dirname+'/sheet.py '+ep+' '+ts.join(' '));console.log('times',ts.join(','),'errs',[...new Set(errs)].join(' | '))})();
