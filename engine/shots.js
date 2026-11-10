// node shots.js <epdir> -> <epdir>/sheet.jpg (16 frames spread over scenes)
const {chromium}=require('playwright');const fs=require('fs');const path=require('path');const {execSync}=require('child_process');
(async()=>{const ep=path.resolve(process.argv[2]);const T=JSON.parse(fs.readFileSync(ep+'/timing.json'));const o=T.off;
const ts=process.argv.length>3?process.argv.slice(3).map(Number):[o.s1+2.5,o.s2-0.4,o.s2+0.9,o.s3+1.5,o.s4-0.4,o.s4+2,o.s4+(o.s5-o.s4)*0.3,o.s4+(o.s5-o.s4)*0.5,o.s4+(o.s5-o.s4)*0.7,o.s5-0.5,o.s5+1.5,o.s6-0.5,o.s7-0.5,o.s7+1.5,T.end-1.3,o.s6+1.5].map(x=>Math.round(x*10)/10);
const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});const errs=[];p.on('pageerror',e=>errs.push(e.message));p.on('console',m=>{if(m.type()==='error')errs.push(m.text())});
await p.goto('file://'+ep+'/build.html');await p.evaluate(()=>document.fonts.ready);fs.mkdirSync(ep+'/chk',{recursive:true});
for(const t of ts){await p.evaluate(t=>{for(let x=0;x<=t;x+=0.5)window.render(x);window.render(t)},t);await p.screenshot({path:`${ep}/chk/${t}.jpg`,type:'jpeg',quality:70});}
await b.close();
execSync('python3 '+__dirname+'/sheet.py '+ep+' '+ts.join(' '));console.log('times',ts.join(','),'errs',[...new Set(errs)].join(' | '))})();
