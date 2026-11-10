# python3 engine/build.py <episode_dir> [theme.json]  -> <episode_dir>/build.html
import json,sys,shutil,os
ep=sys.argv[1];E=os.path.dirname(os.path.abspath(__file__))
theme='{}'
cands=[sys.argv[2]] if len(sys.argv)>2 else [f'{ep}/theme.json',os.path.join(ep,'..','..','theme.json'),os.path.join(ep,'..','theme.json')]
for c in cands:
  if os.path.exists(c): theme=json.dumps(json.load(open(c)),ensure_ascii=False);break
h=open(f'{E}/engine.html').read().replace('__TIMING__',open(f'{ep}/timing.json').read()).replace('__EP__',open(f'{ep}/ep.json').read()).replace('__THEME__',theme).replace('__STORY__','story.js')
for f in ['flags.js','characters.js']: shutil.copy(f'{E}/{f}',f'{ep}/{f}')
if not os.path.exists(f'{ep}/fonts'): shutil.copytree(f'{E}/fonts',f'{ep}/fonts')
open(f'{ep}/build.html','w').write(h)
print('built',ep)
