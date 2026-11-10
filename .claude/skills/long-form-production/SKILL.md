---
name: long-form-production
description: Produce long-form (horizontal, multi-minute) videos for a channel — research, outline, script, then visuals either with the 16:9 animation engine, with clips from the owner's own connected video model, with the owner's footage and images, or a mix. Use when the owner asks for a long video, a YouTube video that is not a Short, an explainer, documentary or essay, a "long version" of a short, wants to connect or use their own video/AI model for visuals, or when channel.json says the format is long or mixed.
---

# Long-form production

A long video asks for minutes of someone's attention, so the bar is higher than for a short and the process is slower on
purpose. Read `QUALITY.md` first — it decides what may be published — then the channel's `CHANNEL.md` and `insights.md`.

Two approvals belong to the owner and cannot be skipped or covered by a standing permission: **the outline** (step 3) and
**the finished video** (step 8).

## 1. Is there a video here?
Write the reason-to-exist sentence into `quality.md` (created with the episode folder). Then test the idea: is there enough
real substance for the planned length, a question that pulls the viewer through, and something we add that the first page of
search results does not? If the honest answer is "this is a 60-second idea", make a short instead and say so.

## 2. Research
Search, read primary sources where they exist, and keep `episodes/<ep>/sources.md`: each claim you intend to make, the
source, and a link. Note disagreements between sources instead of picking the convenient one. Numbers need a date and a
source. If something cannot be verified, it does not go in.

## 3. Outline → owner approval
Propose: working title, the promise, the opening 15 seconds, 3–6 chapters (each with its one point, its evidence, and what
will be *seen*), the ending, and target length. Show it to the owner and wait for a yes or changes. Record the approval in `quality.md`.

## 4. Script — `script.json`
Segments `c1, c2, …` in order: `[[id, voice_key, text, lang], …]`. One idea per segment, 1–3 sentences, written for the ear.
- Open on the most interesting thing, not on context. State the question the video answers within 15 seconds.
- Each chapter ends by raising what the next one answers. Use concrete examples and numbers over adjectives.
- No filler: delete greetings, recaps of what was just said, and every sentence that only sounds informative.
- Aim for ~140–160 spoken words per minute; length follows content, never the other way round.

## 5. Choose how it is shown (`channel.json` → `production.long_style`, or per episode)
| Route | When | How |
|---|---|---|
| **animation** | Explainers, stories, anything our characters can act out | 16:9 engine: `python3 tools/new_episode.py <channel> <ep> long`, then `ep.json` (scenes, chapters) + `story.js`. See `../episode-production/references/engine.md` → "Long-form engine". |
| **clips** | The owner has a video model, real footage, screen recordings, photos, archive material | `python3 tools/new_episode.py <channel> <ep> clips`, then `shots.json`. See "Clips route" below. |
| **mixed** | Mostly footage with animated explanations | Render animated parts as their own long-engine episode, then use the resulting mp4 as `"source": "file"` shots in a clips episode. |

Do not default to generated footage because it is easy. Use it where it shows something that cannot be shown better with
animation, real footage or a diagram.

## 6. Voice — `python3 tools/tts.py <channel> <ep>` (same providers as shorts), then `tools/produce.sh <channel> <ep> check`
For animation this renders control frames (two per segment) into `sheet.jpg`; for clips it prints the shot plan and builds
the review sheet. Look at the result and fix before going on — the same technical and quality checks as for shorts, plus:
does every scene change at least every 8–10 seconds, and is there always something on screen that carries the point?

### Animation route notes
Plan 2–4 scenes per minute. Each scene is its own object in `story.js` with `html`, `init()`, `render(t, lt, p)`. Use the
building blocks (`bullets`, `bigText`, `counter`, characters) for structure and spend the effort on custom drawings that
explain. Chapter cards come from `ep.json` → `chapters` plus a `pause` before the chapter's first segment; the progress
bar and chapter label are automatic. `python3 engine/chapters.py <episode_dir>` prints YouTube chapter timestamps.

### Clips route
1. Write `shots.json`: one shot per visual beat, each starting at a narration trigger (`"c4"` or `"c4:word"`).
   `python3 tools/clips.py plan <channel> <ep>` shows how many seconds each shot must fill.
2. Sources: `"file"` (owner's footage, `start` offset in seconds), `"image"` (slow zoom `in`/`out`/`none`), `"generate"`.
3. **Connecting the owner's video model**: ask what they have (a local model, or a hosted service with their own account).
   Put a command in `channel.json` → `production.video_provider.command` that takes `{prompt} {seconds} {width} {height} {out}`
   (optionally `{image}`) and writes an mp4 — usually a small wrapper script the owner already has or that you write for
   their model's documented API. `examples/dummy_video_model.py` shows the contract. API keys for it go in `.env`, never in
   the command or the repo. Test with one shot before generating a whole episode; generation can cost real money — tell
   the owner roughly how many clips and seconds a video needs before starting.
4. `python3 tools/clips.py generate <channel> <ep>` → `review` → **open `clips/review.jpg` and judge every clip**:
   does it show what the narration says? Any melting hands/faces, garbled text, morphing, impossible motion, wrong
   subject? Approve only clean ones (`clips.py approve … sh01 sh04`); reject the rest with the reason
   (`clips.py reject … sh03 "text on the sign is gibberish"`), improve the prompt, regenerate — or replace the shot with
   footage, an image or animation. Three failed attempts on a shot means the shot idea is wrong; change it.
   The assembler refuses clips that were not approved.
5. Prompts: describe what is seen (subject, action, place, light, camera), ask for no on-screen text, keep one action per
   clip, and keep recurring subjects consistent by repeating their description or using a reference image. Never prompt
   for real people's likeness or other creators' characters.

## 7. Render — `tools/produce.sh <channel> <ep> render` → `final.mp4`
Animation: roughly two minutes of rendering per minute of video. Then watch for sound: narration clear over music
(`"musicVol"` in `ep.json`), effects not startling.

## 8. Quality check and owner viewing
Fill in `quality.md` honestly. Any "no" → fix or drop. Then give the owner the file and ask them to watch it fully before
it is scheduled; their notes are edits, not suggestions. Only then hand over to `publishing` with: title options,
description with chapter timestamps and sources, tags, and a thumbnail concept (a thumbnail frame can be exported from
the engine with `node engine/shots.js <episode_dir> <time>`).

## 9. Records
`episodes.csv` row (use `category` and an `experiment` tag), `plan.csv`, "Status" in `CHANNEL.md`. Long videos get their
own retention review in `analytics-loop`: where do people leave, and what was on screen at that moment?

## Turning a short into a long video (or the reverse)
A long version is not the short stretched out: it needs the outline step and new substance (origin, examples, why it
exists, what people get wrong). A short cut from a long video should be its single best moment, re-edited to open on the hook.

## Editing
The default route, target length, chapter style and the connected video model are in `channel.json`/`CHANNEL.md`; change
them with `channel-edit`. To fix a published long video, never re-upload silently: correct in the description/pinned
comment, or replace only with the owner's decision.
