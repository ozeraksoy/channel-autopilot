# Interview question bank

Ask in this order; skip what the owner already told you. Options in brackets. After each round, note the answer in your
working notes so nothing is asked twice.

## Round 1 — format and platforms
1. Which format? [Shorts only · Long videos only · Mixed] — recommend Shorts for a new channel: faster feedback, cheaper to produce.
2. Which platforms? [YouTube only · YouTube + TikTok + Instagram · + Facebook · other mix] — the same vertical short works on all four.
2b. If long or mixed: how should long videos be made? [Animated in our style (16:9 engine) · From my own footage/photos ·
   With clips from a video model I have access to · A mix] — if a video model: which one, local or hosted, and can it be
   called from a script? (Connected later in `channel.json` → `production.video_provider`; their key goes in `.env`.)
   How long should a typical video be, and how many per week or month is realistic *with* the owner watching each one?
3. Do the accounts already exist? Which handles? (If not, pick a name later in this interview and the owner creates them.)

## Round 2 — niche
4. Do you already have a niche/topic? [Yes: tell me · I have a few ideas · No, help me find one]
   - "Help me" or "a few ideas" → follow `niche-finding.md`, come back with 3 candidates and a recommendation.
5. In one sentence, what does a viewer get from every episode? (the promise — e.g. "one weird saying from another country, explained with a joke")
6. Who is it for? Country/region, language, age range, what they already like.
7. Which language is the content in? Does the owner want a different language for working with Claude?

## Round 3 — voice of the channel
8. Tone? [Funny · Curious/educational · Calm · Dramatic · Mix: describe]
9. Channels or videos you love and want to be compared with? What exactly do you like about them? (Use as reference, never copy.)
10. Anything the channel must never do? (topics, swearing, politics, religion, brand-unsafe humour…) → guardrails.
11. Channel name: do you have one? If not, propose 5–8, check they are short, pronounceable, and that the handle looks
    free on the chosen platforms (search; the owner confirms availability when creating accounts).

## Round 4 — episode shape
12. Episode length? [~30 s · 30–50 s · up to 60 s] (long form: target minutes)
13. Is there a recurring structure? Propose one that fits the niche. The engine's default is 7 beats:
    hook → reveal → unpack → story (the visual joke) → takeaway → everyday example → call to action.
    Rename the beats to fit (see the labels in `theme.json`), or drop the example beat for niches where it makes no sense.
14. Should there be a recurring main character? [Yes, design one with me · Yes, use the default · No character]
15. Should viewers be invited to request topics in comments? (Recommended: it feeds the plan and the engagement loop.)

## Round 5 — schedule
16. How many episodes per week? [7 · 5 · 3 · other] — and at what local time? Which timezone?
17. How much of your own time per week can go into this? (decides how much Claude does unattended vs. asks)

## Round 6 — production tools
18. Narrator voice: [ElevenLabs (your key) · free Edge voices · my own voice] — then pick the actual voice together
    (male/female, age, energy, accent). For foreign-language lines, pick a native voice per language as they come up.
19. Sound effects and music: [free basic pack · ElevenLabs-generated (same key) · my own files]
20. Any other paid tools you already have and want used? (analytics tools, stock libraries…) Record them; never assume.

## Round 7 — publishing and permissions
21. How should publishing work? [Claude uploads and schedules in my signed-in browser · Claude prepares everything, I post]
22. What may Claude do without asking each time? [Nothing public without my yes · Schedule episodes I approved as a batch ·
    Schedule everything that passes the quality check · Also reply to comments]. Write the exact standing permission into
    `CHANNEL.md` — later sessions act only on what is written there.
23. AI disclosure: the kit turns on the platform's "AI-generated/altered content" label when AI voice or imagery is used. Confirm.

## Round 7b — quality
23b. Explain the no-slop standard (`QUALITY.md`) in two sentences and get agreement: an episode that fails the quality
    check is fixed or dropped, even if that means a missed day; long videos need the owner's outline approval and viewing.
    Ask: what would make *you* embarrassed to have on your channel? Add the answers to the guardrails.

## Round 8 — goals and measurement
24. What is the main goal? [Followers · Views · Comments/community · Selling something later · Just learning]
25. A number for 90 days from now? (It is fine to say "no idea"; then set one after two weeks of data.)
26. How do you want to hear about progress? [Short daily note · Weekly report · Only when something needs me]

## After the interview
Read everything back as a compact summary, get a yes, then scaffold.
