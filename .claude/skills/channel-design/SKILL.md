---
name: channel-design
description: Create or change a channel's visual identity — colour theme, design line, on-screen labels, brand badge, and an optional recurring main character — and show previews before anything is produced. Use when the owner asks for a theme, style, look, logo-ish badge, colours, mascot or main character, wants to see options, or says the videos should look different. Also the design step of channel-setup.
---

# Channel design

The look lives in `channels/<slug>/theme.json` and is applied to every episode by the engine, so changing it later is
cheap — but people recognise a channel by its look, so settle it before the first episode and change it rarely.

## What can be designed
`theme.json` fields (all optional; defaults in `templates/channel/theme.json`):
- `brand` — two-part badge text shown top-left (`a` in ink, `b` in the second accent), e.g. `{"a":"SPACE","b":"BITES"}`.
- `handle` — shown on the follow button in the last beat.
- `colors` — `ink` (outlines/text), `accent` (highlight, spoken-word colour), `accent2`, `accent3`, `paper` (light background).
- `labels` — the chips that name the beats: `unpack` (default LITERALLY), `takeaway` (MEANING), `comments`, `follow`, `sayIt`.
  Rename them to fit the niche and write them in the content language.
- `cta` — `followWord` and `dropWord`: the words in the last narration line that trigger the follow button and the
  comments arrow. They must appear in every episode's s7 line, in the content language (e.g. "follow", "takip").
- `character` — the recurring main character: `name`, `shirt`, `hair`, `skin`, `pants` (hex colours),
  `hairStyle` (short · long · bun · curly · bald), `accessory` (none · glasses · cap · beanie · bow · headphones).

The design line that stays fixed across themes: thick ink outlines, flat colours, "sticker" drop shadows, big rounded
display type (Lilita One) with Nunito for body text, word-by-word captions. That consistency is part of the brand.

## Process
1. Ask what the channel should feel like (3 adjectives), colours they love or hate, and whether a character should carry
   the stories. A character helps: a face people recognise, someone for the joke to happen to.
2. Make **three distinct directions** — not three shades of one idea. Write each as a small theme file in a scratch folder.
   Choose accents with strong contrast against the ink colour and against white caption text; check that `accent` is
   readable as highlighted caption text on both light and dark scenes.
3. Render each: `node engine/preview.js <theme.json> <out.png>` and **look at the images yourself** before showing them
   (legibility, clashes, character charm). Show the owner the three previews side by side.
4. Iterate on the chosen one until the owner says yes, then save it as `channels/<slug>/theme.json` and keep the final
   preview as `channels/<slug>/brand/theme_preview.png`.
5. Character: give them a name and two lines of personality in `CHANNEL.md` (what they want, how they react when things go
   wrong). Scripts use this; a character with no personality is just a drawing.
6. Offer profile picture / banner ideas. If you make them, save to `brand/` and tell the owner the exact pixel sizes each
   platform expects (look these up; they change).

## Going beyond the presets
New hairstyles or accessories are small SVG snippets in `engine/characters.js` (`HAIRS`, `ACC`; drawn around a head centred
at 0,0 with radius 98). Per-episode costumes go through `kevSVG(id, {hat: '<svg…>', shirt: …})` in a story. If the owner
wants a completely different character (an animal, a robot), add a new drawing function next to `kevSVG` with the same pose
controls and render a preview before using it.

## Editing later
Read the current `theme.json`, change only what was asked, re-render the preview, show before/after, then save. Note the
change and its date in `CHANNEL.md` (section 3) and, if episodes are already published, in `insights.md` as an experiment —
a new look changes the numbers, and the analysis should know when it happened.
