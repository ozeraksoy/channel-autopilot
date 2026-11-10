#!/usr/bin/env python3
"""Clips for episodes made from generated video, your own footage, or still images (ep.json "mode": "clips").

  python3 tools/clips.py plan     <channel_dir> <ep>     # show every shot with the seconds it has to fill
  python3 tools/clips.py generate <channel_dir> <ep>     # run YOUR video model for shots with "source": "generate"
  python3 tools/clips.py review   <channel_dir> <ep>     # contact sheet clips/review.jpg — LOOK at it
  python3 tools/clips.py approve  <channel_dir> <ep> sh01 sh04 | all
  python3 tools/clips.py reject   <channel_dir> <ep> sh03 "hands melt at 2s"   # deletes the clip so it is regenerated

Shots live in <episode>/shots.json:
  {"captions": true,
   "shots": [{"id": "sh01", "from": "c1",        "source": "generate", "prompt": "…", "approved": false},
             {"id": "sh02", "from": "c2:whales", "source": "file",  "file": "footage/dive.mp4", "start": 12.5},
             {"id": "sh03", "from": "c3",        "source": "image", "file": "images/map.png", "move": "in"}]}
A shot starts when its trigger is spoken ("c2" = start of segment c2, "c2:word" = that word) and runs until the next shot.

The video model is whatever the owner connects in channels/<slug>/channel.json:
  "production": {"video_provider": {"command": "python3 /path/to/my_model.py --prompt {prompt} --seconds {seconds} --width {width} --height {height} --out {out}"}}
The command must write an mp4 to {out}. Optional placeholders: {image} (a reference image from the shot), {id}.
Nothing generated is used until it has been reviewed and approved — tools/assemble.py refuses unapproved clips.
"""
import sys, os, json, subprocess, shlex
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import jload, jdump, duration, load_env

def ctx(chan, ep):
    d = os.path.join(chan, 'episodes', ep); S = jload(os.path.join(d, 'shots.json')); T = jload(os.path.join(d, 'timing.json'))
    if not S: sys.exit(f'no shots.json in {d}')
    if not T: sys.exit('run engine/timing.py first (voice-over must exist): tools/produce.sh <channel> <ep> check')
    E = jload(os.path.join(d, 'ep.json'), {}); size = S.get('size') or ([1920, 1080] if E.get('format') == 'long' else [1080, 1920])
    return d, S, T, size

def at(T, k):
    if isinstance(k, (int, float)): return float(k)
    import re
    n = lambda w: re.sub(r'[.,!?¿¡:;"\'“”‘’…()\-]', '', w.lower()); p = k.split(':')
    if len(p) == 1: return max(0.0, T['off'][p[0]] - 0.15)
    m = [x for x in T['words'] if x['s'] == p[0] and n(x['w']) == n(p[1])]; i = int(p[2]) if len(p) > 2 else 0
    if len(m) <= i: sys.exit(f'shot trigger {k}: word not found in narration')
    return m[i]['t0']

def spans(S, T):
    st = [at(T, s['from']) for s in S['shots']]; st[0] = 0.0
    if st != sorted(st): sys.exit('shots.json: shots must be in time order')
    return [(s, a, (st[i + 1] if i + 1 < len(st) else T['end'])) for i, (s, a) in enumerate(zip(S['shots'], st))]

def path(d, s):
    return os.path.join(d, 'clips', s['id'] + '.mp4') if s['source'] == 'generate' else os.path.join(d, s['file'])

def plan(chan, ep):
    d, S, T, size = ctx(chan, ep)
    for s, a, b in spans(S, T):
        p = path(d, s); have = os.path.exists(p)
        print(f"{s['id']:6} {a:7.2f}–{b:7.2f}  needs {b-a:5.2f}s  {s['source']:8} {'ok' if have else 'MISSING':8} {'approved' if s.get('approved') else ('' if s['source']!='generate' else 'NOT APPROVED')}  {s.get('prompt', s.get('file', ''))[:70]}")
    print(f'frame size {size[0]}x{size[1]}, total {T["end"]}s')

def generate(chan, ep):
    d, S, T, size = ctx(chan, ep); load_env()
    prov = (jload(os.path.join(chan, 'channel.json'), {}).get('production') or {}).get('video_provider') or {}
    cmd = prov.get('command')
    if not cmd: sys.exit('No video model connected. Add production.video_provider.command to channel.json (see this file\'s header), '
                         'or use your own footage/images ("source": "file" / "image"), or the animation engine instead.')
    os.makedirs(os.path.join(d, 'clips'), exist_ok=True); made = 0
    for s, a, b in spans(S, T):
        if s['source'] != 'generate': continue
        out = path(d, s)
        if os.path.exists(out): continue
        secs = round(b - a + 0.3, 2)
        full = cmd.format(prompt=shlex.quote(s['prompt']), out=shlex.quote(out), seconds=secs, width=size[0], height=size[1],
                          image=shlex.quote(os.path.join(d, s['image'])) if s.get('image') else "''", id=s['id'])
        print('generating', s['id'], f'({secs}s)'); r = subprocess.run(full, shell=True)
        if r.returncode != 0 or not os.path.exists(out): print('  FAILED', s['id']); continue
        s['approved'] = False; made += 1
    jdump(S, os.path.join(d, 'shots.json')); print(f'{made} clip(s) generated. Next: clips.py review, look at clips/review.jpg, then approve or reject each.')

def review(chan, ep):
    from PIL import Image, ImageDraw
    d, S, T, size = ctx(chan, ep); rows = []; tw = 320; th = int(tw * size[1] / size[0])
    for s, a, b in spans(S, T):
        p = path(d, s)
        if not os.path.exists(p): print(s['id'], 'missing'); continue
        if s['source'] == 'image': ims = [Image.open(p).convert('RGB').resize((tw, th))]; note = 'image'
        else:
            dur = duration(p); off = float(s.get('start', 0)); ims = []
            for f in (0.08, 0.36, 0.64, 0.92):
                t = off + min(dur - off - 0.05, (b - a)) * f; tmp = os.path.join(d, 'clips', '_r.jpg'); os.makedirs(os.path.dirname(tmp), exist_ok=True)
                subprocess.run(['ffmpeg', '-y', '-v', 'error', '-ss', f'{max(0,t):.2f}', '-i', p, '-frames:v', '1', '-vf', f'scale={tw}:{th}:force_original_aspect_ratio=increase,crop={tw}:{th}', tmp], check=True)
                ims.append(Image.open(tmp).convert('RGB').copy()); os.remove(tmp)
            have = dur - off; note = f'{have:.1f}s for {b-a:.1f}s' + ('  TOO SHORT (will be slowed/held)' if have < (b - a) * 0.98 else '')
        row = Image.new('RGB', (tw * 4, th + 26), 'white')
        for i, im in enumerate(ims): row.paste(im, (i * tw, 26))
        ImageDraw.Draw(row).text((6, 6), f"{s['id']}  {s['source']}  {'APPROVED' if s.get('approved') else 'not approved'}  {note}  {s.get('prompt', s.get('file',''))[:60]}", fill='black')
        rows.append(row); print(s['id'], note)
    if not rows: sys.exit('nothing to review')
    sheet = Image.new('RGB', (tw * 4, sum(r.height for r in rows)), 'white'); y = 0
    for r in rows: sheet.paste(r, (0, y)); y += r.height
    out = os.path.join(d, 'clips', 'review.jpg'); os.makedirs(os.path.dirname(out), exist_ok=True); sheet.save(out, quality=82); print('review sheet:', out)

def mark(chan, ep, ids, ok, why=''):
    d, S, T, size = ctx(chan, ep)
    for s in S['shots']:
        if 'all' in ids or s['id'] in ids:
            if ok:
                if not os.path.exists(path(d, s)): print(s['id'], 'has no file, skipped'); continue
                s['approved'] = True
            else:
                s['approved'] = False; s['rejected'] = why
                if s['source'] == 'generate' and os.path.exists(path(d, s)): os.remove(path(d, s))
            print(s['id'], 'approved' if ok else 'rejected: ' + why)
    jdump(S, os.path.join(d, 'shots.json'))

if __name__ == '__main__':
    a = sys.argv
    if len(a) < 4: sys.exit(__doc__)
    c = a[1]
    if c == 'plan': plan(a[2], a[3])
    elif c == 'generate': generate(a[2], a[3])
    elif c == 'review': review(a[2], a[3])
    elif c == 'approve' and len(a) > 4: mark(a[2], a[3], a[4:], True)
    elif c == 'reject' and len(a) > 4: mark(a[2], a[3], [a[4]], False, ' '.join(a[5:]))
    else: sys.exit(__doc__)
