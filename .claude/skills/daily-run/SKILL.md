---
name: daily-run
description: Run a channel's whole daily routine in the right order — status check, production if the buffer is low, publishing/scheduling, data collection and analysis, engagement, and a short report. Use when the owner says "daily run", "run the channel", "do today's work", "continue", "where are we", or starts a session on an existing channel without a specific request.
---

# Daily run

One pass through the routine for one channel. If several channels exist, ask which, or do them one after another.

1. **Load state** — read `channels/<slug>/CHANNEL.md` completely, then `insights.md` (takeaways, next experiment) and the
   tail of `plan.csv`. Say in two lines where things stand.
2. **Publishing check** — is today's episode scheduled/published on every platform? Is the rolling window full (platforms
   with short scheduling horizons need topping up daily)? Fix gaps with `publishing`.
3. **Buffer check** — count produced-but-unpublished episodes. If fewer than the buffer in `CHANNEL.md` (default: 7 days
   ahead), produce the next batch with `episode-production` (shorts) or continue the current long video with
   `long-form-production`. A thin buffer is never a reason to publish something that fails `QUALITY.md`; report the gap instead.
4. **Data** — after posting time, run `analytics-loop`: log numbers, explain, update takeaways and the experiment.
5. **Audience** — run `engagement`.
6. **Write down and report** — update "Status" in `CHANNEL.md`; give the owner a short report: what was done, the standout
   number and its meaning, what is needed from them (approvals, a missing key, a phone verification…).

Stop and ask instead of guessing when something public would happen outside the standing permission, when a fact cannot
be verified, or when a platform shows a consent, security or payment screen.

## Running it unattended
The routine can be started on a schedule with Claude Code's non-interactive mode, for example a daily job that runs
`claude -p "Run the daily-run skill for channels/<slug>"` in this folder. Unattended runs must stay inside the standing
permission and leave everything else as a question in the report. Set this up only if the owner asks for it.

## Editing
The order, the buffer size and what the report contains can be changed per channel in `CHANNEL.md` (use `channel-edit`).
