# Channel Autopilot

This folder is a kit for starting and running social video channels (YouTube, TikTok, Instagram, Facebook) with Claude Code:
onboarding interview → look and main character → episode production → publishing → daily data analysis → audience engagement.

## How to work here
- Talk to the owner in the language they write in. Episode content is written in the channel's `content_language`.
- Each channel lives in `channels/<slug>/`. Its `CHANNEL.md` is the single source of truth: read it fully at the start of every
  session and continue from "Status". Write down what you did before you stop — the next session only knows what is in the files.
- No channel yet, or the owner wants a new one → use the `channel-setup` skill. Do not start producing before setup is done.
- Skills (in `.claude/skills/`): `channel-setup`, `channel-design`, `episode-production`, `publishing`, `analytics-loop`,
  `long-form-production`, `engagement`, `daily-run`, `channel-edit`.
- Tools (in `tools/`): `check_setup.py`, `new_channel.py`, `new_episode.py`, `tts.py`, `sfx.py`, `produce.sh`,
  `clips.py`, `assemble.py`, `perf.py`.
  Prefer them over rewriting the same logic.

## Rules that always hold
- **No AI slop, ever** — read `QUALITY.md`. Every episode needs a real reason to exist, verified substance, visuals that
  carry meaning and earned length. A missed day is better than a bad episode; an episode that fails the quality check is
  fixed or dropped, never published. This outranks schedules and volume.
- **Secrets**: API keys live only in `.env` (git-ignored). Never print, echo, log, commit or paste a key, and never read `.env`
  aloud. Tools read keys themselves; to check whether a key exists run `python3 tools/check_setup.py`.
- **Publishing is the owner's call**: scheduling or posting publicly, changing account settings, and accepting platform
  terms/consent screens need the owner's yes — unless `CHANNEL.md` records a standing permission for that exact routine.
  Never enter passwords or create accounts; ask the owner to sign in.
- **Honesty with the audience**: content made with AI voice or imagery is labelled as such where the platform offers the switch.
  Verify facts with a reliable source before they go into a script. No reposting other people's videos, no copyrighted
  music or characters.
- **Quality bar** (Rule 1 in every `CHANNEL.md`): would someone stop scrolling for this, and then follow? If not, fix it first.
- **Data over opinion** (Rule 2): log numbers daily, explain them, change one thing at a time.
