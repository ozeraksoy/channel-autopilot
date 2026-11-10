import json,subprocess,sys,os
ep=sys.argv[1];order=['s1','s2','s3','s4','s5','s6','s7']
o=0.3;OFF={};words=[]
for s in order:
  d=json.load(open(f'{ep}/vo/{s}.json'));a=d['align']
  OFF[s]=round(o,3);cur='';ws=0;last=0;sw=[]
  for c,a0,a1 in zip(a['characters'],a['character_start_times_seconds'],a['character_end_times_seconds']):
    if c==' ' or c=='\n':
      if cur and not cur.startswith('[') and not cur.endswith(']'): sw.append({'s':s,'w':cur,'t0':round(o+ws,3),'t1':round(o+last,3)})
      cur='';continue
    if not cur: ws=a0
    cur+=c;last=a1
  if cur and not cur.startswith('['): sw.append({'s':s,'w':cur,'t0':round(o+ws,3),'t1':round(o+last,3)})
  if s=='s2' and len(sw)==1 and ' ' not in d['text'].strip('[] '):  # CJK etc: single token
    pass
  words+=sw
  dur=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f'{ep}/vo/{s}.mp3']))
  o=max(sw[-1]['t1'] if sw else o+dur, o+0.1)+0.35
end=round(words[-1]['t1']+1.2,2)
json.dump({'off':OFF,'words':words,'end':end},open(f'{ep}/timing.json','w'),ensure_ascii=False)
print(ep,'end',end,OFF)
