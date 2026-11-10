# python3 engine/timing.py <episode_dir> -> timing.json  (segment start offsets + every spoken word with start/end time)
# Segment order comes from script.json (any ids); falls back to s1..s7.
import json,subprocess,sys,os
ep=sys.argv[1]
order=[r[0] for r in json.load(open(f'{ep}/script.json'))] if os.path.exists(f'{ep}/script.json') else ['s1','s2','s3','s4','s5','s6','s7']
EP=json.load(open(f'{ep}/ep.json')) if os.path.exists(f'{ep}/ep.json') else {}
GAP=float(EP.get('gap',0.35)); PAUSE=EP.get('pause',{})   # "pause": {"c7": 1.2} adds silence BEFORE a segment (e.g. chapter cards)
o=0.3;OFF={};words=[];segend={}
for s in order:
  d=json.load(open(f'{ep}/vo/{s}.json'));a=d['align']
  o+=float(PAUSE.get(s,0));OFF[s]=round(o,3);cur='';ws=0;last=0;sw=[]
  for c,a0,a1 in zip(a['characters'],a['character_start_times_seconds'],a['character_end_times_seconds']):
    if c==' ' or c=='\n':
      if cur and not cur.startswith('[') and not cur.endswith(']'): sw.append({'s':s,'w':cur,'t0':round(o+ws,3),'t1':round(o+last,3)})
      cur='';continue
    if not cur: ws=a0
    cur+=c;last=a1
  if cur and not cur.startswith('['): sw.append({'s':s,'w':cur,'t0':round(o+ws,3),'t1':round(o+last,3)})
  words+=sw
  dur=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f'{ep}/vo/{s}.mp3']))
  e=max(sw[-1]['t1'] if sw else o+dur, o+0.1);segend[s]=round(e,3);o=e+GAP
end=round(words[-1]['t1']+float(EP.get('tail',1.2)),2)
json.dump({'off':OFF,'segend':segend,'order':order,'words':words,'end':end},open(f'{ep}/timing.json','w'),ensure_ascii=False)
print(ep,'end',end,OFF if len(OFF)<=8 else f'{len(OFF)} segments')
