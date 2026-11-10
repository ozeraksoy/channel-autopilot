# The quality standard: no AI slop, ever

This kit uses AI to make videos. It must never be used to make *slop*: content produced because it is cheap to produce,
that gives the viewer nothing. This standard applies to every channel, every format, every episode. It outranks
schedules, streaks and volume targets: **a missed day is better than a bad episode.**

## What slop is
- Narration that says nothing: generic statements, padding, filler transitions, "in today's fast-paced world".
- Facts nobody checked, invented statistics, fake quotes, confident nonsense.
- Visuals that are unrelated to what is being said (random stock-like b-roll), or generated footage with visible
  defects: melting hands and faces, gibberish text, objects morphing, physics that breaks.
- Length for its own sake: a ten-minute video with two minutes of substance.
- The same template with the nouns swapped, published in bulk. Recycled or lightly reworded content from other creators.
- Clickbait that the video does not pay off. Fake urgency. Engagement bait with no real question.
- Imitating a real person's voice or face, or presenting generated imagery as real footage.

## What every episode must have
1. **A reason to exist** — one sentence: what does the viewer know, feel or laugh at afterwards that they did not before?
   If that sentence is weak, do not make the episode.
2. **Something of our own** — an angle, a joke, an example, a way of showing it. Not a summary of the top search results.
3. **Verified substance** — every factual claim checked against a reliable source, sources kept in the episode folder.
4. **Visuals that carry meaning** — every shot shows what the narration is about, or makes the joke. No filler shots.
5. **Earned length** — cut until removing anything more would hurt. Long-form must hold a specialist's respect and a
   beginner's attention for its whole duration.
6. **Craft** — clean audio, readable text, no visual defects, a hook that the video actually pays off.
7. **Honesty** — AI voice or imagery is disclosed where platforms offer the label; nothing generated is passed off as real.

## How it is enforced
- **Before producing**: write the reason-to-exist sentence in the episode's `quality.md`. No sentence, no production.
- **Before rendering**: look at the control frames / clip review sheet. Generated clips cannot be assembled until each
  one has been looked at and approved (`tools/clips.py`); defective ones are rejected and regenerated or replaced.
- **Before publishing**: complete `quality.md` (template in `templates/quality.md`). Any "no" means the episode is fixed
  or dropped — not published. Tell the owner plainly when an episode was dropped and why.
- **Long-form**: the owner approves the outline before scripting and watches the final video before it is scheduled.
  This approval cannot be replaced by a standing permission.
- **Volume**: never increase the publishing cadence beyond what can be researched, reviewed and watched properly.
- **After publishing**: comments like "AI garbage", "this is wrong", or steep early drop-off are treated as quality
  findings in `insights.md`, not as noise.

If the owner asks for something that would be slop (mass-produce 50 videos, skip checks, copy a competitor), say so,
explain what it would cost the channel, and offer the version that meets this standard.
