---
name: publishing
description: Upload and schedule finished episodes on YouTube, TikTok, Instagram and Facebook, or prepare a ready-to-post pack when Claude cannot operate the browser. Use when the owner says publish, upload, schedule, post, "put it on YouTube/TikTok/Instagram", asks what is scheduled, or after episode-production finishes a batch.
---

# Publishing

Publishing is public and hard to undo, so the order is: check permission → prepare → confirm → act → verify → record.

## Permission
Read `CHANNEL.md` for a standing permission (written during setup). If the routine you are about to run is not covered
by it word for word, show the owner what will be posted (episode, platform, date/time, title/caption) and wait for a yes.
Platform consent or terms screens, account settings, and anything asking for a password are always the owner's to handle.

## Two ways to publish (from `channel.json` → `publishing.method`)
**A. Browser automation** — when the session has browser tools connected to the owner's signed-in browser (for example the
Claude in Chrome extension). Check which account is active on each site before posting; brand accounts and personal
accounts are easy to mix up. Follow `references/platforms.md` for each platform's steps and quirks, and record new quirks
in `CHANNEL.md` → Lessons.

**B. Upload pack** — when there are no browser tools, or the owner prefers to post themselves. For each episode write
`episodes/<ep>/UPLOAD.md` with: file path, per-platform title/description/caption/tags ready to copy, the cover frame
(export it as `cover.jpg` with ffmpeg at the timestamp), the scheduled date/time, and the switches to set (not made for
kids, AI label on, language). Tell the owner where the packs are and what to do, in order.

## Schedule
One episode per slot from `channel.json` → `cadence`, in the channel's timezone. Scheduling ahead beats posting live.
Each platform limits how far ahead and how many per day you can schedule; when a limit blocks you, record what is left in
"Status" so the next session continues instead of starting over.

## After every action
- Verify in the platform's own list of scheduled/published posts (date, time, account) — not just the success pop-up.
- Update `plan.csv` (status per platform) and `episodes.csv` (`publish_date`) and "Status" in `CHANNEL.md`.
- Once an episode is live, the `analytics-loop` and `engagement` skills take over.

## Editing
Changing a posting time, platform list or the publishing method: use `channel-edit`, then reschedule only the posts that
are affected; never delete and re-upload a published post just to change text that can be edited in place.
