---
name: episode-production
description: Produce short-form episodes (vertical shorts/reels) for an existing channel — pick topics from the plan, verify facts, write the script, generate voice-over, animate the story scene, check frames, render and mix the final video, and write titles/descriptions/captions. Use whenever the owner asks to make, produce, render or script an episode or a batch, says "next episodes" or "today's production", or wants an existing episode fixed or re-rendered. For long horizontal videos use long-form-production.
---

# Episode production

**Quality first**: `QUALITY.md` (top of the kit) is the standard — no AI slop, ever. Each episode folder gets a `quality.md`;
write its reason-to-exist sentence before producing and complete the check before handing over to publishing. An episode
that fails is fixed or dropped, and the owner is told. Never lower the bar to keep a schedule.

Read `channels/<slug>/CHANNEL.md` (all of it) and `insights.md` → "Current takeaways" and "Next experiment" before writing
anything. Episodes are supposed to get better because of what earlier ones taught us; a batch that ignores the takeaways
wastes the data. In the batch notes, say which takeaway you applied and the **one** thing you changed on purpose.

Work in batches of up to 4 episodes; finish and save one stage for all of them before starting the next, so an interrupted
session loses little.

## 1. Choose and verify
- Take the next unproduced rows from `plan.csv`. Viewer requests recorded in `requests.csv` go first (see `engagement`).
- Verify every claim (fact, idiom, spelling, meaning, pronunciation) with at least one reliable source via web search.
  If it cannot be verified, replace the topic and say so in the notes. Wrong facts cost trust and get called out in comments.
- Respect the channel's guardrails.

## 2. Script — `episodes/<ep>/script.json`
Format: `[[segment, voice_key, text, lang], …]` with segments `s1…s7` (the engine's seven beats):
s1 hook · s2 reveal · s3 unpack · s4 story · s5 takeaway · s6 everyday example · s7 call to action.
Read `references/script-craft.md` for what makes each beat work. The essentials:
- The first two seconds decide everything: open on tension or a strange image, not on a greeting.
- s4 carries the visual joke. Write it as things that can be *seen* happening to the character, in short sentences.
- s7 must contain the channel's `followWord` and `dropWord` (from `theme.json` → `cta`) and give a reason to come back.
- Total 30–50 s unless `channel.json` says otherwise (roughly 85–130 spoken words in English).
- With ElevenLabs v3 voices, emotion tags like `[excited]`, `[laughing]`, `[sighs]` at the start of a line add life; other
  providers ignore them automatically.

## 3. Voice — `python3 tools/tts.py channels/<slug> <ep> [<ep> …]`
Provider and voices come from `voices.json`. `narr` is the narrator; add more keys (e.g. `"de"`) for native-language lines.
- **edge** (free): voice names like `en-US-GuyNeural`; list them with `edge-tts --list-voices`.
- **elevenlabs**: voice ids from the owner's ElevenLabs account; the key is read from `.env` by the tool.
- **manual**: the owner records `vo/s1.mp3 … s7.mp3`; run the tool with `--provider manual` to estimate timing.
Listen-check is not possible for you, so check durations printed by the tool: a segment far shorter or longer than expected
usually means a mispronounced or skipped line — regenerate that segment with `--only s4`.
If the network is down, do the animation work first and come back.

## 4. Episode data and story — `ep.json`, `story.js`
Start from `python3 tools/new_episode.py channels/<slug> <ep>` (a complete working starter; add `clips` as a third argument for a
short made from generated clips, footage or images instead of animation — see `long-form-production` → "Clips route", it works the same at 1080×1920) and read
`references/engine.md` for every field and helper. `ep.json` holds the on-screen text and when each piece appears
(triggers refer to spoken words: `"s4:word"`); `story.js` draws and animates the s4 scene, which is where the effort goes.
Animation times come from spoken words (`T('s4','word')`), never fixed seconds, so re-recording audio does not break them.

## 5. Check before rendering — `tools/produce.sh channels/<slug> <ep> check`
This writes `sheet.jpg`, a grid of control frames. **Open it and look.** Fix and re-run until it is clean:
- technical: overlapping text, things off-screen, empty scenes, art colliding with captions (y≈1330) or the top badges,
  missing-word errors printed by the script (a trigger word that is not in the narration);
- quality (Rule 1): is the hook frame intriguing on its own? Is the joke visible without sound? Is every scene alive
  (something moving or changing), or is the character just standing there?

## 6. Render — `tools/produce.sh channels/<slug> <ep> render` → `final.mp4`
About 1–2 minutes per episode. Sound effects named in `ep.json` → `sfx` must exist in `channels/<slug>/sfx/`
(`python3 tools/sfx.py basic …` for the free pack; `tools/sfx.py generate … fx.json` for ElevenLabs effects). Loudness is
normalised to −17.4 LUFS. If the file is larger than the upload path allows (browser upload tools often cap at 10 MB),
re-encode a copy: `ffmpeg -i final.mp4 -c:v libx264 -preset veryfast -crf 23 -c:a copy final_upload.mp4`.

## 7. Texts and records
- `episodes/<ep>/texts.json`: `title`, `description`, `caption` (short, for TikTok/Instagram), `tags`, `cover` (which frame and why).
  Titles promise the payoff without giving it away; descriptions end with the question that invites comments.
- Append a row to `episodes.csv` (topic, title, category, hook_type, hook_text, duration, experiment). The analysis
  compares episodes by these columns, so fill them consistently.
- Mark the rows in `plan.csv` as produced and update "Status" in `CHANNEL.md`.
- Complete `quality.md`. Only episodes with verdict PUBLISH go on.
- Hand over to `publishing`.

## Fixing an existing episode
Change only what is needed: text → `ep.json`; narration → edit `script.json`, regenerate just that segment
(`tts.py … --only s3`); animation → `story.js`. Then check and render again. Never overwrite a published file silently —
keep the old one with a suffix and note why it changed.

## Editing how production works
Production defaults (length, beats, voice provider, batch size) live in `channel.json`, `voices.json` and `CHANNEL.md`
section 2. Change them through `channel-edit` so the reason and date are recorded.
