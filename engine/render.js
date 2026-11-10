// node render.js <epdir>  -> <epdir>/video.mp4
const {chromium}=require('playwright');const {spawn}=require('child_process');const fs=require('fs');const path=require('path');
(async()=>{const ep=path.resolve(process.argv[2]);const DUR=JSON.parse(fs.readFileSync(ep+'/timing.json')).end,FPS=30,N=Math.round(DUR*FPS);
const ff=spawn('ffmpeg',['-y','-v','error','-f','image2pipe','-framerate','30','-c:v','mjpeg','-i','-','-c:v','libx264','-preset','veryfast','-crf','17','-pix_fmt','yuv420p','-r','30',ep+'/video_tmp.mp4'],{stdio:['pipe','inherit','inherit']});
const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920},deviceScaleFactor:1});
const errs=[];p.on('pageerror',e=>errs.push(e.message));p.on('console',m=>{if(m.type()==='error')errs.push(m.text())});
await p.goto('file://'+ep+'/build.html');await p.evaluate(()=>document.fonts.ready);
for(let i=0;i<N;i++){await p.evaluate(t=>window.render(t),i/FPS);const buf=await p.screenshot({type:'jpeg',quality:92});if(!ff.stdin.write(buf))await new Promise(r=>ff.stdin.once('drain',r));}
ff.stdin.end();await new Promise(r=>ff.on('close',c=>{r()}));await b.close();fs.renameSync(ep+'/video_tmp.mp4',ep+'/video.mp4');console.log('ok',DUR,[...new Set(errs)].slice(0,5).join(' | '))})();
