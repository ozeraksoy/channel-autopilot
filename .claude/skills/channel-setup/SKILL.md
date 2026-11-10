---
name: channel-setup
description: Start a new social video channel from zero with a guided interview, or finish a half-done setup. Use whenever the owner says they want to start/create/launch a channel or a series (YouTube, Shorts, TikTok, Reels, Facebook), asks "what channel should I make", wants help finding a niche, or when the repo has no channels/<slug>/ folder yet. Also use for the first run after cloning this kit.
---

# Channel setup

The goal is a channel folder that contains everything a later session needs to produce, publish and improve episodes
without asking the owner again. Ask, do not assume: a wrong guess here is copied into every episode.

Speak the owner's language. Ask in small rounds (2–4 questions at a time, multiple choice where a choice exists — use the
question tool if the session has one), and say what you will do with each answer. Offer a recommendation when the owner is
unsure, with the reason. People may answer "you decide": then decide, say what you chose, and move on.

## Flow

1. **Check the machine** — `python3 tools/check_setup.py`. If required items are missing, help install them now (the hints
   are printed). Production needs Python 3, ffmpeg, Node 18+ and Playwright with Chromium.
2. **Interview** — work through `references/interview.md` in order. It covers: format (shorts / long / mixed), platforms,
   niche (or help finding one → `references/niche-finding.md`), audience and language, tone, episode structure, cadence,
   voice and tools (including API keys), publishing method, goals, and guardrails.
3. **Scaffold** — `python3 tools/new_channel.py <slug>` then fill `channel.json`, `voices.json` and `CHANNEL.md`
   (replace `{{NAME}}`, complete sections 1–4 from the answers; keep Rule 1 and Rule 2 as they are).
4. **Look and character** — hand over to the `channel-design` skill (theme, design line, optional main character). Skip only
   if the owner explicitly wants defaults.
5. **First plan** — propose the first 10–15 episode ideas as a table (topic, why it should work, category, hook type).
   Verify each fact/idiom/claim against a reliable source before listing it. After the owner agrees, write them to `plan.csv`
   with dates that match the cadence. Put variety in on purpose (different categories and hook types): the first weeks are
   also the first experiment, and `analytics-loop` needs something to compare.
6. **Accounts** — the owner creates the accounts and signs in themselves (never create accounts or type passwords for them).
   Record handles in `channel.json`. Suggest bio text and cross-links; help make a logo/banner if they want.
7. **Sound pack** — `python3 tools/sfx.py basic channels/<slug>` (free, always works). With an ElevenLabs key the owner can
   later add richer effects and music (see `episode-production`).
8. **Read back** — summarise the whole setup in a short list, ask for corrections, fix them, then write "Status: setup
   complete on <date>, next: produce the first batch" into `CHANNEL.md`.
9. **Offer the next step** — produce the first batch now (`episode-production`), and explain the daily routine (`daily-run`).

## Keys and tools (part of the interview)
Explain the options plainly and let the owner choose; nothing here is mandatory:
- **Voice**: ElevenLabs (most natural, emotion tags, paid, needs their own API key) · Edge voices (free, no key,
  `pip install edge-tts`, good quality, less expressive) · their own recorded voice (`manual`).
- If they choose a service that needs a key: tell them to create `.env` from `.env.example` and paste the key **into the file
  themselves** — not into the chat. Then confirm with `python3 tools/check_setup.py`. If they paste a key into the chat anyway,
  do not repeat it; write it to `.env` and suggest they rotate it later.
- **Publishing**: with a browser-automation tool connected to their signed-in browser (for example the Claude in Chrome
  extension), Claude can upload and schedule; without one, Claude prepares an upload pack and the owner posts it
  (see `publishing`). Both work; record the choice.

## What the kit can and cannot produce (say this honestly during the interview)
- Included and tested: **vertical animated shorts** (1080×1920, 30–60 s) in a 2D sticker style with word-timed captions,
  made by the engine in `engine/`.
- Long-form or live-action channels: the kit still does planning, scripts, titles/descriptions, publishing, analytics and
  engagement, but the video itself must come from the owner's footage/editor, or the engine has to be extended first
  (say so; do not promise finished long videos).

## Editing later
Any answer can be changed afterwards with the `channel-edit` skill. When re-running setup on an existing channel, read
`channel.json` and `CHANNEL.md` first, show the current values, and only ask about what the owner wants to change.
