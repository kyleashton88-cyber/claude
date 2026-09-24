---
name: visual-storyboard
description: Storyboard a course video scene by scene - choose what is on screen for every beat, where to cut away to a flow, diagram, real screen or worked number, and how to pace visual change. Use after the teach plan and before writing narration, or when a video feels static, slide-heavy or hard to follow.
---

# Visual Storyboard and Cutaways

A storyboard decides what the viewer **sees** for every sentence. Write it before the
narration. The rule of thumb: if the voice describes something that moves, happens in
order, or appears on a screen, the picture should show that thing, not a bullet about it.

## The cutaway grammar

A cutaway is a planned switch from the "teacher" view (title, statement, bullets) to
something concrete, then back. Use the right one for the job:

| When the voice is... | Cut away to | Scene type |
|---|---|---|
| Explaining how something works, in steps or between parties | Animated flow, nodes lighting up as they're named | `flow` |
| Telling them to click, type or read something in an app | The real screen, step by step, with a highlight box and push-in | `cutaway` |
| Pointing at a chart, diagram or annotated screenshot | The image, with callouts and a zoom to the key area | `image` |
| Contrasting right and wrong, before and after, A vs B | Two columns revealed item by item | `compare` |
| Quoting a number that should land | The number counting up | `stats` |
| Busting a myth | The myth struck through, then the truth | `strike` |
| Doing arithmetic | Numbered steps with the result popping in | `steps` |
| Asking a question | Question, thinking timer, answer | `quiz` |

Full field reference: `.claude/skills/lesson-script-writing/references/scene-reference.md`.

## Pacing rules

- A visual change at least every 8 to 20 seconds. Item reveals count as change; a static slide over 20 seconds doesn't.
- Never more than two text slides (`bullets`, `statement`, `steps`, `pillars`) in a row.
- In lessons of 5 minutes or more: at least one `flow` and at least one `cutaway` or annotated `image`.
- Visual scenes should be at least 40% of the scenes.
- The first 20 seconds: a hook, not an agenda.
- A cutaway is followed by a short "what just happened" line back on the teacher view, so the viewer re-orients.

## Storyboard table

Write it like this (in the teach-plan note or a scratch file) and agree it before scripting:

| # | Beat | Chapter | Scene | On screen | Voice (gist) | Secs |
|---|---|---|---|---|---|---|
| 1 | Hook | Intro | title | 3.2 · LTV, LT & HF | Three numbers decide tool or trap | 8 |
| 2 | Hook | Why it matters | statement | "A lending protocol never calls you." | No margin call, penalty sale | 15 |
| 3 | See it | How it works | flow | Wallet → Pool → Oracle → Liquidator | What happens behind a loan | 25 |
| 4 | Understand | The four numbers | bullets | LTV, Max LTV, LT, HF | Define each, one at a time | 40 |
| 5 | Do it | Do it | cutaway | App position panel: HF box, liquidation price box | Where to read these in the app | 30 |
| 6 | Worked | Worked example | steps | $50k × 0.8 ÷ $20k = 2.0 | Arithmetic, step by step | 30 |
| 7 | Check | Quiz | quiz | HF question | Pause, answer | 15 |

Then count: visual share, longest text run, seconds between changes. Fix before scripting.

## Choosing and making visuals

1. **Reuse first:** 56 images already exist in `programs/defi-program/assets/` (diagrams, charts, module banners). Check them before making new ones.
2. **Flows:** design with `animated-flows`. Keep them to 3 to 6 nodes.
3. **Screens:** capture with `screen-demo-cutaways`. Never draw a fake app UI.
4. **Charts and diagrams:** add to `export/build_images.js` (same brand, same palette) or render Mermaid via `export/render_mermaid.js`.
5. **Vertical cuts (9:16 shorts):** flows switch to a column layout automatically; keep node labels to three words.

## Brand and legibility

- Palette and fonts come from `export/build_images.js` (`C`, Inter, JetBrains Mono). Don't introduce new colours.
- Orange (`tone: bad`) is for danger, loss and wrong beliefs only. Aqua is for correct and safe.
- On-screen text: 3 to 7 words per line, never full sentences over 12 words.
- Minimum on-screen font size is 26 px at 1080p. Captions sit at the bottom 200 px: keep key content above them.
