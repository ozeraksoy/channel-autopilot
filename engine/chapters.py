# python3 engine/chapters.py <episode_dir>  -> YouTube chapter timestamps for the description (long-form episodes)
import json,sys
ep=sys.argv[1];T=json.load(open(f'{ep}/timing.json'));E=json.load(open(f'{ep}/ep.json'))
f=lambda t:f'{int(t//60)}:{int(t%60):02d}'
print('0:00 Intro')
for c in E.get('chapters',[]):
  if c['at'] in T['off']: print(f(max(0,T['off'][c['at']]-float(E.get('pause',{}).get(c['at'],0)))),c['title'])
