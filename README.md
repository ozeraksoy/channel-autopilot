# Channel Autopilot

A skill set for [Claude Code](https://claude.com/claude-code) that starts and runs a social video channel with you:
it interviews you, designs the look and an optional main character, produces animated shorts, publishes them, studies
the numbers every day, talks to your audience — and uses what it learns to make the next episodes better.

It grew out of running a real channel (2D animated shorts about funny sayings from around the world) and packages the
rules and tools that came out of that.

## What you get
| Skill | What it does |
|---|---|
| `channel-setup` | Guided interview: shorts/long/mixed, platforms, niche (or help finding one), audience, tone, structure, schedule, voice and tools, publishing, goals |
| `channel-design` | Colour theme, design line, labels, brand badge and a recurring main character — with previews before you commit |
| `episode-production` | Shorts: topic → fact check → script → voice-over → animation → control frames → final video and texts |
| `long-form-production` | Long videos: research → outline you approve → script → 16:9 animation, your footage, or clips from your own video model → your viewing |
| `publishing` | Uploads and schedules on YouTube, TikTok, Instagram, Facebook through your signed-in browser, or prepares a ready-to-post pack |
| `analytics-loop` | Logs views/likes/comments/followers daily, explains why episodes over- or under-perform, sets the next experiment |
| `engagement` | Pinned question, replies in your channel's voice, viewer requests into the plan, "it's live!" follow-ups |
| `daily-run` | The whole routine in order, with a short report |
| `channel-edit` | Change anything later: niche, look, voice, schedule, permissions, goals |

## What it can produce
- **Vertical animated shorts** (1080×1920, ~30–60 s) with word-timed captions.
- **Long-form animated videos** (1920×1080) with chapters, a progress bar and explainer building blocks.
- **Videos from clips**, short or long: your own footage and images, and/or clips from a video model **you** connect
  (your model, your account, your key — none is bundled). Shots are cut to the narration, captioned and mixed.

## No AI slop
The kit refuses to be a content mill. [`QUALITY.md`](QUALITY.md) is binding for every channel: each episode needs a real
reason to exist, checked facts, visuals that mean something and no padding. Generated clips must be individually reviewed
before they can be used, long videos need your approval of the outline and your viewing of the final cut, and an episode
that fails the check is fixed or dropped — a missed day is better than a bad video.

## Quick start
```bash
git clone https://github.com/ozeraksoy/channel-autopilot.git
cd channel-autopilot
npm install && npx playwright install chromium     # rendering
pip install -r requirements.txt                    # images + free voices
claude                                             # open Claude Code in this folder
```
Then just say: **"I want to start a new channel."**
Claude checks your machine, asks its questions, and takes it from there. You also need `ffmpeg` installed
(`python3 tools/check_setup.py` tells you what is missing and how to get it).

## Keys and costs
No keys are included and none are required.
- **Voice**: free Microsoft Edge voices work out of the box (`edge-tts`). For the most natural, expressive narration you
  can add your own [ElevenLabs](https://elevenlabs.io) key: copy `.env.example` to `.env` and paste the key there.
  You can also record your own voice.
- **Sound**: a free synthesised effects pack is built in; ElevenLabs can generate richer effects with the same key.
- `.env` is git-ignored. Never commit keys.

## Publishing
With a browser-automation tool connected to your signed-in browser (for example the Claude in Chrome extension), Claude
can upload and schedule for you — only within the permission you give it during setup. Without one, it writes an upload
pack per episode (file, titles, captions, tags, cover, time) and you post it.

## How your data is kept
Each channel is a folder in `channels/<slug>/`: `CHANNEL.md` (the guide and current status), `channel.json`, `theme.json`,
`voices.json`, `plan.csv`, `episodes.csv`, `performance.csv`, `followers.csv`, `insights.md`, `requests.csv`, and
`episodes/`. Plain files, so every session picks up exactly where the last one stopped and you can read everything yourself.
Videos and audio are git-ignored because they are large; back them up separately.

## Try the engine without a channel
```bash
python3 tools/new_channel.py demo
python3 tools/new_episode.py channels/demo ep001
python3 tools/sfx.py basic channels/demo
python3 tools/tts.py channels/demo ep001            # free voice
tools/produce.sh channels/demo ep001 check          # control frames → channels/demo/episodes/ep001/sheet.jpg
tools/produce.sh channels/demo ep001 render         # → final.mp4
python3 tools/new_episode.py channels/demo lf001 long   # 16:9 long-form starter (then tts + produce as above)
node engine/preview.js channels/demo/theme.json theme_preview.png
```
`examples/funny-slangs-ep28/` is a real episode's source (script, episode data, story animation).

## Honest limits
- Platforms change their screens; publishing steps may need a nudge (Claude records what it learns in your channel guide).
- The animation style is one specific look (thick outlines, flat colours). Other styles mean extending the engine.
- Long animated videos take real scene-by-scene work; the kit makes that work structured, not instant.
- The clips route is only as good as the footage or the model you connect, which is why every clip is reviewed.
- Good numbers are not guaranteed. The kit makes you consistent and makes you learn from data; the ideas still matter.

## Türkçe özet
Bu repo, Claude Code ile sıfırdan bir video kanalı kurup yürütmek için hazır bir skill setidir. Klasörü indirip içinde
Claude Code'u açın ve "yeni bir kanal kurmak istiyorum" yazın: sorularla kanalınızı tanımlar (shorts/uzun, platformlar,
niş, ton, takvim, ses ve araçlar), tema ve ana karakter tasarlar, bölümleri üretir, yayınlar, her gün veriyi analiz eder
ve izleyiciyle ilgilenir. Shorts'un yanında uzun (yatay) videolar da üretir: kendi animasyon tarzımızla, kendi
çekimlerinizle ya da sizin bağladığınız bir video modelinin klipleriyle. Tek şart: asla "AI slop" üretilmez
(`QUALITY.md`); kalite kontrolünden geçmeyen bölüm yayınlanmaz. Anahtar gerekmez; isterseniz kendi ElevenLabs anahtarınızı `.env` dosyasına eklersiniz.

## Licence
MIT (see `LICENSE`). Bundled fonts are under the SIL Open Font License.
