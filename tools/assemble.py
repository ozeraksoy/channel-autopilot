#!/usr/bin/env python3
"""Assemble an episode from clips, footage and images:  python3 tools/assemble.py <channel_dir> <ep>
Cuts every shot to the time its narration needs, fits it to the frame, joins them, burns word-timed captions,
and writes <episode>/video.mp4 (engine/mix.py then adds the sound). Refuses generated clips that were not approved."""
import sys, os, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import jload, duration
from clips import ctx, spans, path
FPS = 30

def run(cmd): subprocess.run(['ffmpeg', '-y', '-v', 'error'] + cmd, check=True)

def ass_time(t): h = int(t // 3600); m = int(t % 3600 // 60); return f'{h}:{m:02d}:{t % 60:05.2f}'

def captions(T, size, theme, out, n=5):
    W, H = size; col = lambda h: '&H00' + h[5:7] + h[3:5] + h[1:3] + '&'
    hi = col((theme.get('colors') or {}).get('accent', '#FFD23F')); font = theme.get('captionFont', 'Arial'); fs = int(H * (0.055 if W > H else 0.045))
    head = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, OutlineColour, BackColour, Bold, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV
Style: C,{font},{fs},&H00FFFFFF,&H002E1A1F,&H00000000,-1,1,{max(3, fs//12)},0,2,{int(W*0.08)},{int(W*0.08)},{int(H*(0.09 if W > H else 0.30))}

[Events]
Format: Layer, Start, End, Style, Text
"""
    chunks = []; cur = None; ws = T['words']
    for i, w in enumerate(ws):
        prev = ws[i - 1] if i else None
        if not cur or cur[0]['s'] != w['s'] or len(cur) >= n or prev['w'][-1:] in '.!?:' or w['t0'] - prev['t1'] > 0.4: cur = []; chunks.append(cur)
        cur.append(w)
    lines = []
    for ci, c in enumerate(chunks):
        end = min(chunks[ci + 1][0]['t0'], c[-1]['t1'] + 0.45) if ci + 1 < len(chunks) else c[-1]['t1'] + 0.6
        for k, w in enumerate(c):
            a = w['t0']; b = c[k + 1]['t0'] if k + 1 < len(c) else end
            txt = ' '.join(('{\\c' + hi + '}' + x['w'].upper() + '{\\c&HFFFFFF&}') if j == k else x['w'].upper() for j, x in enumerate(c))
            lines.append(f'Dialogue: 0,{ass_time(a)},{ass_time(b)},C,{txt}')
    open(out, 'w', encoding='utf-8').write(head + '\n'.join(lines) + '\n')

def main():
    chan, ep = sys.argv[1], sys.argv[2]; d, S, T, size = ctx(chan, ep); W, H = size
    fit = f'scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},setsar=1,fps={FPS}'; parts = []
    bad = [s['id'] for s, a, b in spans(S, T) if s['source'] == 'generate' and not s.get('approved')]
    if bad: sys.exit('Not assembling: generated clips without approval: ' + ', '.join(bad) + '\nReview them first (tools/clips.py review, then approve or reject).')
    os.makedirs(os.path.join(d, 'clips'), exist_ok=True)
    for s, a, b in spans(S, T):
        need = round((b - a) * FPS) / FPS; src = path(d, s); out = os.path.join(d, 'clips', f"_n_{s['id']}.mp4")
        if not os.path.exists(src): sys.exit(f"missing file for shot {s['id']}: {src}")
        enc = ['-an', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '17', '-pix_fmt', 'yuv420p', '-t', f'{need:.3f}', out]
        if s['source'] == 'image':
            fr = int(need * FPS) + 2; mv = s.get('move', 'in')
            z = {'in': "min(1+0.10*on/%d,1.10)" % fr, 'out': "max(1.10-0.10*on/%d,1)" % fr, 'none': '1'}[mv]
            run(['-loop', '1', '-i', src, '-vf', f"scale={W*2}:{H*2}:force_original_aspect_ratio=increase,crop={W*2}:{H*2},zoompan=z='{z}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={fr}:s={W}x{H}:fps={FPS},setsar=1"] + enc)
        else:
            off = float(s.get('start', 0)); have = duration(src) - off
            if have >= need: vf = fit
            elif need / have <= 1.35: vf = f'setpts={need/have:.4f}*PTS,' + fit           # gentle slow-down
            else: vf = fit + f',tpad=stop_mode=clone:stop_duration={need-have+0.2:.2f}'     # hold the last frame
            run(['-ss', f'{off:.3f}', '-i', src, '-vf', vf] + enc)
        parts.append(out)
    lst = os.path.join(d, 'clips', '_list.txt'); open(lst, 'w').write(''.join(f"file '{os.path.abspath(p)}'\n" for p in parts))
    raw = os.path.join(d, 'video_raw.mp4'); run(['-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy', raw])
    final = os.path.join(d, 'video.mp4')
    if S.get('captions', True):
        ass = os.path.join(d, 'captions.ass'); captions(T, size, jload(os.path.join(chan, 'theme.json'), {}), ass, S.get('captionWords', 5))
        esc = os.path.abspath(ass).replace('\\', '/').replace(':', '\\:').replace("'", "\\'")
        run(['-i', raw, '-vf', f"ass='{esc}'", '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '17', '-pix_fmt', 'yuv420p', '-an', final]); os.remove(raw)
    else: os.replace(raw, final)
    for p in parts: os.remove(p)
    os.remove(lst); print('assembled', final, f'{duration(final):.2f}s', f'{W}x{H}')

if __name__ == '__main__':
    main()
