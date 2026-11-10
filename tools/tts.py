#!/usr/bin/env python3
"""Voice-over for one or more episodes, with word timing the render engine needs.

  python3 tools/tts.py <channel_dir> <ep_id> [<ep_id> ...] [--provider elevenlabs|edge|manual] [--only s1,s4]

Reads  <channel_dir>/episodes/<ep_id>/script.json : [[segment_id, voice_key, text, lang], ...]
       <channel_dir>/voices.json                   : {"provider": "...", "<voice_key>": {"elevenlabs": "<voice id>", "edge": "<voice name>"}}
Writes <episode>/vo/<segment_id>.mp3 and .json ({"text","lang","provider","align":{characters, character_start_times_seconds, character_end_times_seconds}})

Providers
  elevenlabs  best quality, emotion tags ([excited] ...), needs ELEVENLABS_API_KEY in .env
  edge        free Microsoft Edge neural voices via the `edge-tts` package (pip install edge-tts), no key
  manual      you (or any other tool) put <segment_id>.mp3 into vo/ yourself; timing is estimated from audio length
"""
import sys, os, json, base64, re, argparse, asyncio, urllib.request
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import secret, jload, jdump, duration, strip_tags

NORM = re.compile(r"[\W_]+", re.UNICODE)
norm = lambda s: NORM.sub('', s.lower())

def align_from_words(text, words, total):
    """Build per-character timing from word boundaries [(word, start, end), ...].
    Unmatched tokens are interpolated, so the result always covers the whole text."""
    toks = [(m.group(0), m.start()) for m in re.finditer(r'\S+', text)]
    times = [None] * len(toks); wi = 0
    for i, (tok, _) in enumerate(toks):
        rest = norm(tok); st = en = None
        while wi < len(words) and rest:
            w = norm(words[wi][0])
            if not w: wi += 1; continue
            if rest.startswith(w) or w.startswith(rest) or w in rest:
                st = words[wi][1] if st is None else st; en = words[wi][2]
                rest = rest[rest.find(w) + len(w):] if w in rest else ''
                wi += 1
            else:
                break
        if st is not None: times[i] = [st, en]
    # interpolate gaps by character length
    known = [i for i, t in enumerate(times) if t]
    if not known:
        tot = sum(len(t) for t, _ in toks) or 1; pos = 0.05; span = max(0.1, total - 0.15)
        for i, (tok, _) in enumerate(toks):
            d = span * len(tok) / tot; times[i] = [pos, pos + d * 0.92]; pos += d
    else:
        bounds = [(-1, 0.0)] + [(i, times[i][1]) for i in known] + [(len(toks), total)]
        for (a, ta), (b, tb) in zip(bounds, bounds[1:]):
            gap = [j for j in range(a + 1, b) if not times[j]]
            if not gap: continue
            lo = ta; hi = times[b][0] if b < len(toks) else tb
            tot = sum(len(toks[j][0]) for j in gap) or 1; pos = lo
            for j in gap:
                d = max(0.0, hi - lo) * len(toks[j][0]) / tot; times[j] = [pos, pos + d * 0.92]; pos += d
    chars, st, en = [], [], []
    last = 0.0
    for i, ch in enumerate(text):
        tk = next((k for k, (tok, p) in enumerate(toks) if p <= i < p + len(tok)), None)
        if tk is None:
            chars.append(ch); st.append(round(last, 3)); en.append(round(last, 3)); continue
        tok, p = toks[tk]; a, b = times[tk]; n = len(tok)
        s = a + (b - a) * (i - p) / n; e = a + (b - a) * (i - p + 1) / n
        chars.append(ch); st.append(round(s, 3)); en.append(round(e, 3)); last = e
    return {'characters': chars, 'character_start_times_seconds': st, 'character_end_times_seconds': en}

def eleven(text, voice, out, stability):
    H = {'xi-api-key': secret('ELEVENLABS_API_KEY'), 'Content-Type': 'application/json'}
    def post(body):
        u = f'https://api.elevenlabs.io/v1/text-to-speech/{voice}/with-timestamps?output_format=mp3_44100_192'
        return json.load(urllib.request.urlopen(urllib.request.Request(u, data=json.dumps(body).encode(), headers=H), timeout=180))
    try:
        r = post({'text': text, 'model_id': 'eleven_v3', 'voice_settings': {'stability': stability}}); used = text; model = 'eleven_v3'
    except Exception as e:
        print('  eleven_v3 failed, retrying with eleven_multilingual_v2:', type(e).__name__)
        used = strip_tags(text)
        r = post({'text': used, 'model_id': 'eleven_multilingual_v2', 'voice_settings': {'stability': 0.3, 'similarity_boost': 0.8, 'style': 0.7}}); model = 'eleven_multilingual_v2'
    open(out, 'wb').write(base64.b64decode(r['audio_base64']))
    return used, r['alignment'], model

def edge(text, voice, out):
    try:
        import edge_tts
    except ImportError:
        sys.exit('The free "edge" provider needs the edge-tts package:  pip install edge-tts')
    used = strip_tags(text)
    async def run():
        try: c = edge_tts.Communicate(used, voice, boundary='WordBoundary')
        except TypeError: c = edge_tts.Communicate(used, voice)
        words = []
        with open(out, 'wb') as f:
            async for ch in c.stream():
                if ch['type'] == 'audio': f.write(ch['data'])
                elif ch['type'] == 'WordBoundary':
                    s = ch['offset'] / 1e7; words.append((ch['text'], s, s + ch['duration'] / 1e7))
        return words
    words = asyncio.run(run())
    return used, align_from_words(used, words, duration(out)), 'edge-tts'

def manual(text, out):
    if not os.path.exists(out):
        sys.exit(f'manual provider: record or export the audio for this segment to {out} first')
    used = strip_tags(text)
    return used, align_from_words(used, [], duration(out)), 'manual (estimated timing)'

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('channel'); ap.add_argument('eps', nargs='+')
    ap.add_argument('--provider'); ap.add_argument('--only', help='comma separated segment ids'); a = ap.parse_args()
    V = jload(os.path.join(a.channel, 'voices.json'), {})
    prov = a.provider or V.get('provider') or 'edge'
    only = set(a.only.split(',')) if a.only else None
    for ep in a.eps:
        d = os.path.join(a.channel, 'episodes', ep); os.makedirs(os.path.join(d, 'vo'), exist_ok=True)
        for sid, who, text, lang in jload(os.path.join(d, 'script.json')):
            if only and sid not in only: continue
            out = os.path.join(d, 'vo', f'{sid}.mp3')
            v = (V.get(who) or {}).get(prov)
            if prov != 'manual' and not v:
                sys.exit(f'voices.json has no "{prov}" voice for "{who}". Add it (see the episode-production skill, "Voices").')
            if prov == 'elevenlabs': used, al, model = eleven(text, v, out, 0.0 if who == 'narr' else 0.5)
            elif prov == 'edge': used, al, model = edge(text, v, out)
            else: used, al, model = manual(text, out)
            jdump({'text': used, 'lang': lang, 'provider': model, 'align': al}, os.path.join(d, 'vo', f'{sid}.json'))
            print(ep, sid, model, round(al['character_end_times_seconds'][-1], 2), 's')

if __name__ == '__main__':
    main()
