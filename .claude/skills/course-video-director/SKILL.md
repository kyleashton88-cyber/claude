---
name: course-video-director
description: Produce a high-end course lesson video end to end, from lesson text to a rendered, checked MP4 with flows, screen cutaways, worked examples, practice and a recap. Use when the user asks to make, upgrade, rewrite or render a lesson video, bring a lesson "up to gold standard", or batch-produce course videos for the On-Chain Operator Program or Grid Bot Blueprint. Chains instructional-design, lesson-script-writing, visual-storyboard, animated-flows, screen-demo-cutaways, practice-and-assessment and video-qa-review.
---

# Course Video Director

The lead skill for course video. It runs the other video skills in order and
owns the finished result. The bar is `programs/defi-program/video-scripts/gold/lesson-03-2.json`
(rendered as `video/lesson-03-2.mp4`). Every lesson should reach or beat it.

## Why this exists

Most of the generated scripts in `video-scripts/lessons/` are slide decks read
aloud. The linter shows it: most lessons have no visual scene at all (no flow, image,
cutaway or comparison), and many have no hook or recap. A premium lesson *shows*
things happening. It moves between explanation, a diagram of the mechanism, the real
screen, a worked number and a check for understanding.

## The pipeline

| Step | Skill | Output |
|---|---|---|
| 1. Teach plan | `instructional-design` | Objective, misconceptions, the understand → see it → do it → check → teach it back arc |
| 2. Storyboard | `visual-storyboard` | Scene list: what's on screen for every 8 to 20 seconds, where the cutaways go |
| 3. Flows | `animated-flows` | `flow` scenes for every mechanism (transaction, swap, liquidation, bridge, bot loop) |
| 4. Screen demos | `screen-demo-cutaways` | Captured screenshots + `cutaway` scenes for every "do it" moment |
| 5. Script | `lesson-script-writing` | Gold-format JSON with voice (`vo`) and on-screen text (`cap`) |
| 6. Practice | `practice-and-assessment` | Quiz scenes, worked-example fading, the "your turn" task, worksheet link |
| 7. QA | `video-qa-review` | Lint clean, test render checked, compliance and facts checked |
| 8. Render | this skill | `video/<id>.mp4` + thumbnail, captions, chapters |

Do steps 1 and 2 before writing any narration. Narration written first becomes a
slideshow; narration written to a storyboard follows the pictures.

## Working files

- Lesson source: `programs/defi-program/lessons/module-NN-*.md` (and `03-defi-strategy-mastery.md` for 8.3)
- Baseline script (generated): `video-scripts/lessons/lesson-NN-M.json`
- Upgraded script (hand-finished): `video-scripts/gold/lesson-NN-M.json` (the generator skips any lesson with a gold script)
- Demo specs: `programs/defi-program/demos/<id>.json` → screenshots in `assets/demos/<id>/`
- Scene reference: `.claude/skills/lesson-script-writing/references/scene-reference.md`

## Commands (from `programs/defi-program/export`)

```bash
npm install                                               # once
python3 lint_video_script.py ../video-scripts/gold/lesson-03-2.json   # lint one script
python3 lint_video_script.py --all --summary              # lint every script
node capture_demo.js ../demos/<id>.json                   # capture a screen demo
SCENES=4-6 node build_video.js lesson-03-2                # test-render scenes 4 to 6 only
node build_video.js lesson-03-2                           # full render
```

Rendering needs Kokoro TTS (`pip install kokoro soundfile`), ffmpeg via
`imageio-ffmpeg`, and Chromium (set `CHROMIUM_PATH` if it isn't at the default path).

## Definition of done (every lesson)

1. Opens with a hook that names the problem or the cost of getting it wrong, within 20 seconds.
2. States one measurable objective ("By the end you'll be able to...").
3. Every mechanism is shown as a `flow` or diagram, not only described.
4. Every "do it" step is shown on a real screen (`cutaway`), with a highlight box on where to click.
5. At least one worked example with real numbers, then a faded one the viewer finishes.
6. Visual change at least every 20 seconds; no more than two text slides in a row.
7. Two or three quiz questions, spaced through the lesson, plus a final check.
8. Recap in three lines, and "Next up" pointing to the next lesson.
9. `lint_video_script.py` shows 0 errors and no structure warnings.
10. A test render of the new scenes has been looked at frame by frame (see `video-qa-review`).
11. Under 25 minutes. Split into Part 1 and Part 2 if longer.

## Batch mode

For a whole module, run steps 1 and 2 for every lesson first, so the flows and demos
can be shared (one captured demo often serves three lessons). Then script, lint and
render. Keep a checklist in `10-video-production-plan.md` (the "Rendered" column).

## Guardrails

- Educational only. No income or return promises, no "guaranteed", no pressure. The linter enforces the obvious cases; judgement covers the rest.
- Screen demos use testnets, practice mode or tiny amounts, and never show a seed phrase, private key, full balance or personal address. Blur them.
- Protocol facts (rates, parameters, UI labels) go stale. Put a "last checked" date in the script's `use` field and re-check before rendering.
