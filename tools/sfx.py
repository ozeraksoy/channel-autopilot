#!/usr/bin/env python3
"""Sound effects for a channel.

  python3 tools/sfx.py basic <channel_dir>             # free: synthesise the standard pack (pop, whoosh, boom, ding, text, bonk, tada, sad, bed music)
  python3 tools/sfx.py generate <channel_dir> fx.json  # ElevenLabs sound generation, needs ELEVENLABS_API_KEY
                                                       # fx.json: {"name": ["short concrete prompt", seconds], ...}
Files land in <channel_dir>/sfx/<name>.mp3. Existing files are kept.
"""
import sys, os, json, subprocess, urllib.request, wave, struct, math, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import secret, jload
SR = 44100

def write(path, samples):
    peak = max(1e-9, max(abs(s) for s in samples)); wav = path[:-4] + '.wav'
    with wave.open(wav, 'w') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes(b''.join(struct.pack('<h', int(32000 * 0.9 * s / peak)) for s in samples))
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', wav, '-b:a', '192k', path], check=True); os.remove(wav)

def tone(f0, f1, dur, decay, shape='sin', vol=1.0):
    out = []; ph = 0.0
    for i in range(int(SR * dur)):
        t = i / SR; f = f0 + (f1 - f0) * (t / dur); ph += 2 * math.pi * f / SR
        v = math.sin(ph) if shape == 'sin' else (1 if math.sin(ph) > 0 else -1) * 0.5
        out.append(vol * v * math.exp(-t * decay) * min(1, t * 400))
    return out

def noise(dur, shape):
    out = []; y = 0.0
    for i in range(int(SR * dur)):
        t = i / SR; x = random.uniform(-1, 1); a = shape(t / dur); y += (x - y) * (0.05 + 0.5 * a); out.append(y * a)
    return out

def add(a, b, off=0.0):
    o = int(off * SR); a = a + [0.0] * max(0, o + len(b) - len(a))
    for i, v in enumerate(b): a[o + i] += v
    return a

def pluck(freq, dur=0.45):
    return [((math.sin(2*math.pi*freq*i/SR) + 0.4*math.sin(4*math.pi*freq*i/SR) + 0.2*math.sin(6*math.pi*freq*i/SR)) * math.exp(-i/SR*7) * min(1, i/60)) for i in range(int(SR*dur))]

def bed(bpm=118, bars=8):
    beat = 60 / bpm; N = {'C': 261.63, 'D': 293.66, 'E': 329.63, 'F': 349.23, 'G': 392.0, 'A': 440.0, 'B': 493.88}
    prog = [('C', 'E', 'G'), ('A', 'C', 'E'), ('F', 'A', 'C'), ('G', 'B', 'D')]; out = [0.0] * int(SR * beat * 4 * bars)
    for bar in range(bars):
        ch = prog[bar % 4]
        for b in range(8):
            t = (bar * 4 + b / 2) * beat; n = ch[[0, 2, 1, 2, 0, 2, 1, 2][b]]
            out = add(out, [v * (0.9 if b % 2 == 0 else 0.6) for v in pluck(N[n] * (0.5 if b % 4 == 0 else 1))], t)
            if b % 2 == 1: out = add(out, [v * 0.12 for v in noise(0.04, lambda x: 1 - x)], t)
    return out[:int(SR * beat * 4 * bars)]

def basic(chan):
    d = os.path.join(chan, 'sfx'); os.makedirs(d, exist_ok=True); random.seed(7)
    pack = {
        'pop': lambda: tone(420, 900, 0.12, 28),
        'whoosh': lambda: noise(0.45, lambda x: math.sin(math.pi * x) ** 2),
        'boom': lambda: add(tone(110, 38, 0.9, 5), [v * 0.5 for v in noise(0.25, lambda x: (1 - x) ** 3)]),
        'ding': lambda: add(tone(1318, 1318, 0.9, 5), tone(1976, 1976, 0.9, 7, vol=0.5)),
        'text': lambda: add(tone(880, 880, 0.08, 30), tone(1174, 1174, 0.12, 25), 0.07),
        'bonk': lambda: add(tone(240, 120, 0.25, 16, 'sq'), tone(90, 60, 0.3, 12)),
        'tada': lambda: add(add(tone(523, 523, 0.5, 5), tone(659, 659, 0.5, 5), 0.12), tone(784, 784, 0.9, 3.5), 0.24),
        'sad': lambda: add(add(tone(392, 370, 0.4, 3), tone(349, 330, 0.4, 3), 0.38), tone(311, 262, 0.9, 2.5), 0.76),
        'bed': bed,
    }
    for n, f in pack.items():
        p = os.path.join(d, n + '.mp3')
        if os.path.exists(p): continue
        write(p, f()); print('made', p)

def generate(chan, fx):
    key = secret('ELEVENLABS_API_KEY'); d = os.path.join(chan, 'sfx'); os.makedirs(d, exist_ok=True)
    for n, (prompt, secs) in jload(fx).items():
        p = os.path.join(d, n + '.mp3')
        if os.path.exists(p): continue
        r = urllib.request.Request('https://api.elevenlabs.io/v1/sound-generation?output_format=mp3_44100_192',
            data=json.dumps({'text': prompt, 'duration_seconds': secs, 'prompt_influence': 0.5}).encode(), headers={'xi-api-key': key, 'Content-Type': 'application/json'})
        open(p, 'wb').write(urllib.request.urlopen(r, timeout=120).read()); print('made', p)

if __name__ == '__main__':
    if len(sys.argv) >= 3 and sys.argv[1] == 'basic': basic(sys.argv[2])
    elif len(sys.argv) >= 4 and sys.argv[1] == 'generate': generate(sys.argv[2], sys.argv[3])
    else: sys.exit(__doc__)
