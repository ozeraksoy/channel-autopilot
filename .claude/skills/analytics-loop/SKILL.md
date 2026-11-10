---
name: analytics-loop
description: Collect performance numbers for every published episode, log them, work out why the best and weakest episodes performed the way they did, and turn that into takeaways and the next experiment. Use daily after posting time, whenever the owner asks how the channel/videos are doing, about views, likes, comments, followers, growth or "what works", wants a weekly report, or before planning the next batch.
---

# Analytics loop

The channel improves only if each batch is shaped by what earlier episodes showed. This skill is that feedback loop:
**measure → explain → decide → test**. Do it every day; skipped days are lost evidence, because platforms mostly show
current totals and the history has to be kept by us.

## 1. Measure
For every published episode and every platform, get: views, likes, comments, shares, average percentage viewed (or
average watch time) if shown, and followers gained from that video if shown. Also the account's total followers.
- With browser tools: read them from YouTube Studio (Content and Analytics), TikTok Studio (Posts, Analytics), Meta
  Business Suite (Content, Insights).
- Without: ask the owner to paste numbers or export CSVs from those pages, and parse them.
Log each one:
```
python3 tools/perf.py add channels/<slug> --ep ep012 --platform youtube --views 1367 --likes 25 --comments 4 --shares 2 --avg-view-pct 71 --followers-gained 4
python3 tools/perf.py followers channels/<slug> --platform youtube --total 132
```
The CSVs are append-only: never rewrite old rows. If a number cannot be read today, skip it and note that; do not estimate.

## 2. Explain
Run `python3 tools/perf.py report channels/<slug>`. It ranks episodes, computes engagement rate, compares groups by every
attribute column in `episodes.csv` (category, hook_type, experiment…), shows follower growth, and marks episodes that are
too young to judge (under 48 hours). Then do the part a script cannot: look at the best and the weakest mature episodes
side by side and ask what differs —
- the hook sentence and first frame (retention in the first seconds),
- topic/category and how familiar it is to the audience,
- the visual joke: is there one, how early does it land,
- cover and title, length, day and time posted,
- which platform it did well on (the same video can win on one and die on another),
- what commenters actually said (questions, corrections, "do my country" — see `engagement`).
Read the comments on outliers; they often state the reason outright.

Honesty rules: say what the numbers show and label everything else **hypothesis**. Two or three episodes are an anecdote.
A difference inside normal day-to-day variation is not a finding. Views alone are not the goal if `channel.json` says the
goal is followers or comments — rank by the goal metric too.

## 3. Decide — update `channels/<slug>/insights.md`
- **Analysis log**: 3–6 lines for today (date, best/weakest, the likely why, evidence).
- **Current takeaways**: what the data supports now, each with its evidence and confidence; delete lines newer data contradicts.
- **Next experiment**: exactly one deliberate change for the next batch (e.g. "question hooks instead of statement hooks"),
  the metric that will judge it, and when. One change at a time, otherwise nobody can tell what caused the difference.
`episode-production` reads these before every batch.

## 4. Report
- Daily: 2–3 lines to the owner — the standout number and what we are doing about it. Skip if nothing changed.
- Weekly (or when asked): top 3 and bottom 3 with reasons, follower change per platform, result of the last experiment,
  the next one, and any suggestion to reorder `plan.csv` (move up topics similar to what works; drop what repeatedly fails).
  If a pattern holds for two weeks, propose making it part of the channel's rules in `CHANNEL.md`.

## Editing
What to track, the 48-hour threshold (`--min-hours`), the goal metric and the report rhythm live in `channel.json` and
`CHANNEL.md`; change them with `channel-edit`. New attribute to compare (say `cover_style`)? Add a column to `episodes.csv`
and fill it for past episodes — the report picks it up automatically.
