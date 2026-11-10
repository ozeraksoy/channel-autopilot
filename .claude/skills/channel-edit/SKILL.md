---
name: channel-edit
description: Change anything about an existing channel after setup — niche or promise, format, platforms, schedule, episode structure, theme or character, voices and tools, API keys, publishing method, permissions, goals, guardrails, the plan, or the rules in CHANNEL.md. Use whenever the owner says change, edit, update, switch, rename, "from now on", "stop doing", "add a platform", or is unhappy with how something is set up.
---

# Editing a channel

Everything decided during setup can be changed. The job here is to change it in every place it lives, so later sessions
do not find two versions of the truth.

1. Read `CHANNEL.md` and `channel.json`, show the current value of what the owner wants to change, and confirm the new one.
   If the request is vague ("make it better"), ask what bothers them, or offer the relevant options from
   `channel-setup/references/interview.md`.
2. Apply the change where it lives:

| Change | Files | Then |
|---|---|---|
| Name, niche, promise, audience, tone, guardrails | `channel.json`, `CHANNEL.md` §1 | Review `plan.csv` for topics that no longer fit |
| Format, length, beats, recurring elements, CTA question | `channel.json`, `CHANNEL.md` §2, theme `labels`/`cta` | Applies to unproduced episodes |
| Colours, labels, badge, main character | `theme.json` via the `channel-design` skill | Preview before saving |
| How long videos are made, connected video model | `channel.json` → production (`long_style`, `video_provider`), `.env` for its key | Test one shot with `tools/clips.py` |
| Narrator or native voices, voice provider | `voices.json`, `channel.json` → production | Test one segment with `tools/tts.py … --only s1` |
| API keys | `.env` (the owner edits it; never show contents) | `python3 tools/check_setup.py` |
| Platforms, handles, posting time, cadence | `channel.json`, `CHANNEL.md` §4 | Reschedule affected posts with `publishing` |
| Publishing method or what Claude may do unasked | `channel.json`, standing permission text in `CHANNEL.md` | Read the new permission back to the owner |
| Goals, what to track, report rhythm | `channel.json`, `CHANNEL.md` Rule 2 notes | Next `analytics-loop` run uses it |
| Topics and order | `plan.csv` | Never move episodes already scheduled or promised to a viewer without telling the owner |
| Working rules, lessons | `CHANNEL.md` | — |

3. Record the change with its date in `CHANNEL.md` (a short "Changes" list under Status). If episodes are already
   published and the change could affect performance (look, voice, structure, schedule), also note it in `insights.md` as
   an experiment so the analysis can compare before and after.
4. `QUALITY.md` is not editable per channel: guardrails can be made stricter in `CHANNEL.md`, never looser.
5. Do not rewrite history: published episodes, logged numbers and past analysis stay as they are.
