# python3 mix.py <epdir> <sfxdir> [followWord] -> <epdir>/final.mp4 (needs video.mp4); SFX list from ep.json "sfx": [[seg:word(:n), name, vol], ...] + standard scene sfx
import json,subprocess,re,sys,os
ep,SD=sys.argv[1],sys.argv[2];d=json.load(open(f'{ep}/timing.json'));OFF=d['off'];W=d['words'];END=d['end'];EP=json.load(open(f'{ep}/ep.json'))
FW=sys.argv[3] if len(sys.argv)>3 else EP.get('cta',{}).get('followWord','follow')
n=lambda w:re.sub(r'[.,!?¿¡:;"\'“”‘’…()\-]','',w.lower())
def AT(k):
  if isinstance(k,(int,float)):return k
  p=k.split(':');s,w=p[0],p[1];i=int(p[2]) if len(p)>2 else 0
  m=[x for x in W if x['s']==s and n(x['w'])==n(w)]
  return m[i]['t0'] if len(m)>i else OFF[s]
LONG=EP.get('format')=='long' or EP.get('mode')=='clips'
if LONG:  # long form: a soft whoosh at every scene change and a pop on chapter cards; everything else comes from ep.json "sfx"
  std=[['whoosh',OFF[sc['segs'][0]]-0.25,.35] for sc in EP.get('scenes',[])[1:] if sc.get('segs')]+[['pop',OFF[c['at']]-float(EP.get('pause',{}).get(c['at'],0))+0.15,.5] for c in EP.get('chapters',[]) if c.get('at') in OFF]
else:
  std=[['pop',0.3,.6],['pop',AT(EP['hook'].get('chipAt',0.9)),.5],['pop',AT(EP['hook'].get('bigAt',1.5)),.6],['boom',OFF['s2']-0.05,.9],['whoosh',OFF['s3']-0.2,.6],['pop',OFF['s3']+0.1,.4],
   ['whoosh',OFF['s4']-0.2,.6],['whoosh',OFF['s5']-0.2,.6],['pop',OFF['s5'],.5],['whoosh',OFF['s6']-0.2,.5],['whoosh',OFF['s7']-0.2,.6],['pop',AT('s7:'+FW),.5],['ding',AT('s7:'+FW),.5]]
  std+= [['text',AT(b['at']),.7] for b in EP['chat']['bubbles']]
SFX=std+[[a[1],AT(a[0]),a[2]] for a in EP.get('sfx',[])]
ins=[];fl=[];k=0
for s,o in OFF.items():
  ins+=['-i',f'{ep}/vo/{s}.mp3'];fl.append(f'[{k}:a]aresample=48000,pan=stereo|c0=c0|c1=c0,adelay={int(o*1000)}:all=1[a{k}]');k+=1
for f,t,v in SFX:
  if not os.path.exists(f'{SD}/{f}.mp3'):print('missing sfx',f);continue
  ins+=['-i',f'{SD}/{f}.mp3'];fl.append(f'[{k}:a]aresample=48000,aformat=channel_layouts=stereo,volume={v*0.55},adelay={int(max(0,t)*1000)}:all=1[a{k}]');k+=1
MU=f"{SD}/{EP.get('music','bed')}.mp3"
if os.path.exists(MU):
  ins+=['-stream_loop','-1','-i',MU];fl.append(f'[{k}:a]aresample=48000,aformat=channel_layouts=stereo,volume={float(EP.get('musicVol',0.08 if LONG else 0.12))},afade=t=in:d=0.4,atrim=0:{END},afade=t=out:st={END-1.6}:d=1.6[a{k}]');k+=1
else: print('no music bed (',MU,') - mixing without music')
fl.append(''.join(f'[a{i}]' for i in range(k))+f'amix=inputs={k}:normalize=0:duration=longest:dropout_transition=0,atrim=0:{END}[mix]')
subprocess.run(['ffmpeg','-y','-v','error',*ins,'-filter_complex',';'.join(fl),'-map','[mix]','-c:a','pcm_f32le',f'{ep}/mix.wav'],check=True)
I=float(re.findall(r'I:\s+(-?[\d.]+) LUFS',subprocess.run(['ffmpeg','-hide_banner','-i',f'{ep}/mix.wav','-af','ebur128','-f','null','-'],capture_output=True,text=True).stderr)[-1])
g=float(os.environ.get('TARGET_LUFS','-17.4'))-I
subprocess.run(['ffmpeg','-y','-v','error','-i',f'{ep}/video.mp4','-i',f'{ep}/mix.wav','-af',f'volume={g:.2f}dB,alimiter=limit=0.89:level=false','-map','0:v','-map','1:a','-c:v','copy','-c:a','aac','-b:a','256k','-ar','48000','-shortest',f'{ep}/final.mp4'],check=True)
print('mixed',ep,'I',I,'gain',round(g,2))
