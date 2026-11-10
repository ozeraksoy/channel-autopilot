# Engine reference (vertical animated shorts)

Pipeline: `script.json` → `tools/tts.py` (audio + character timing in `vo/`) → `engine/timing.py` (word times →
`timing.json`) → `engine/build.py` (merges `engine.html` + `ep.json` + `theme.json` + `story.js` → `build.html`) →
`engine/shots.js` (control frames) → `engine/render.js` (frames → `video.mp4`) → `engine/mix.py` (voice + sfx + music →
`final.mp4`). `tools/produce.sh` runs these for you.

The page exposes one pure function, `window.render(t)`: given a time in seconds it sets the state of everything on screen.
Because it is pure, any frame can be rendered in any order — that is what makes control frames and re-renders reliable.

## Scenes and segments
A hook (s1) · B reveal (s2) · C unpack (s3) · D story (s4, yours) · E takeaway (s5) · F chat example (s6) · G call to action (s7).
Stage is 1080×1920. Top badges sit at y≈118; captions at y=1330 (3-word chunks, spoken word highlighted). Keep important
art between y≈250 and y≈1250 and away from the right edge (platform buttons).

## ep.json
```
{"badge": "ANIMALS",                    // top-right label; or use "country": "GERMANY", "flag": "DE" for a flag badge (codes in engine/flags.js)
 "kevin": {"shirt": "#FFCE00"},          // per-episode overrides of the main character (merged over theme.character)
 "hook":   {"chip": "ANIMAL FACT", "chipAt": "s1:octopus", "big": "WAIT...", "bigAt": "s1:wild",
            "kevAt": "s1:hiding", "kev": {"mouth": "o", "brows": "sad"}, "bg": "<css background, optional>"},
 "reveal": {"chip": "THE FACT", "lines": [["THREE", "w", 230], ["HEARTS!", "yel", 210]], "pron": "optional pronunciation", "bg": "<css, optional>"},
 "literal":{"chip": "REALLY", "lines": [[["THREE","yel",170]], [["SEPARATE","w",130]], [["HEARTS","cor",170]]]},   // rows of [text, colour, size]; words pop in as they are spoken in s3
 "meaning":{"chip": "SO...", "lines": [["SWIMMING","w",130], …], "at": ["s5:swimming", …], "artAt": "s5:crawl."},
 "chat":   {"name": "Maya", "bubbles": [{"side": "L", "text": "…", "at": "s6:ran"}, {"side": "R", "text": "…", "at": "s6:today."}]},
 "cta":    {"lines": [["WHICH ANIMAL","w",110], …], "dropWord": "comments", "followWord": "follow"},   // words optional; default from theme
 "sfx":    [["s4:doctor.", "ding", 0.5], …],   // [trigger, file name in channels/<slug>/sfx (without .mp3), volume]
 "music":  "bed",                              // optional, file in sfx/
 "cover":  "s4:third"}                         // note for the cover frame
```
Colours: `w` white, `yel` accent, `cor` accent2, `teal` accent3, `tom` tomato red. Sizes are px; long words need smaller sizes.
Triggers: `"s4:word"` = the moment that word is spoken in segment s4 (punctuation and case ignored); `"s4:word:1"` = its
second occurrence; a plain number = seconds. A trigger word that is not in the narration prints `missing s4 word` and falls
back to the segment start — fix these, they make animation fire at the wrong time.
In left (grey) chat bubbles highlight with a dark colour such as `#E8590C`; the accent yellow is unreadable there.

## story.js
Defines `const STORY = {…}`:
- `html` — markup for scene D (absolutely positioned elements; class `abs`, class `L` for the display font).
  For small labels inside art use `style="font-family:L"` instead of `class="L"` (the class adds a thick outline).
- `hookArt`, `literalArt`, `meaningArt`, `sticker` — optional art for scenes A (when there is no flag), C, E and the chat sticker.
- `init()` — runs once; insert characters here: `$('Dkev').innerHTML = kevSVG('kD', CH())` (`CH(overrides)` = theme character).
- `render(t)` — called every frame while s4 is on screen. Also optional `hook(t)`, `literal(t, at)`, `meaning(t, at)`, `chat(t)`.
- `noCap(t)` — optional; return true to hide captions at time t.

Helpers: `T('s4','word', n=0)` word time · `OFF.s4` segment start · `SEND('s4')` segment end · `pop(t, t0, d=.35)` bouncy
0→1 · `seg(t, a, b)` linear 0→1 · `oc`, `ob`, `io` easings · `clamp` · `sty(idOrEl, {css})` · `$('id')` · `INK` ·
`kevSVG(prefix, opts)` draws a character (opts: shirt, hair, skin, pants, hairStyle, accessory, hat, hold) and
`kv(prefix, pose)` poses it each frame: `mouth` smile|frown|flat|o · `eyes` n|happy · `brows` angry|sad · `tears` 0..1 ·
`walk` phase · `armL`/`armR` degrees · `bob` px · `tilt` degrees · `look` −1..1.
Several characters can share a scene: give each its own prefix and colours.

Rules of thumb: derive every time from `T(...)`; repeated words need an index; measure positions with
`getBoundingClientRect()` when zooming to something; add space between inline words with margins; keep every moment alive
with small motion (bob, blink, drift) but one main action at a time.

## Languages and fonts
Bundled fonts cover Latin (incl. Turkish, Polish…), Cyrillic, Devanagari and Arabic; CJK falls back to system Noto fonts
if installed. For another script add a woff2 to `engine/fonts/` and an `@font-face` with its `unicode-range` in
`engine/engine.html`. Flags are SVG in `engine/flags.js`; add missing ones there.

## Sound
`engine/mix.py` adds standard scene sounds if present in `sfx/` (`pop`, `whoosh`, `boom`, `ding`, `text`), your `ep.json`
effects, and the music bed at low volume, then normalises loudness (`TARGET_LUFS` env var overrides −17.4).
