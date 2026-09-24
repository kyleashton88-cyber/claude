---
name: lesson-script-writing
description: Write or rewrite a course lesson video script in the gold-standard JSON format - narration written for the ear, on-screen text, chapters, and scene fields synced to the storyboard. Use when turning a lesson or storyboard into a video script, upgrading a generated script in video-scripts/lessons to gold, or fixing narration that sounds robotic, rushed or like it's reading slides.
---

# Lesson Script Writing

Input: the teach plan (`instructional-design`) and storyboard (`visual-storyboard`).
Output: `programs/defi-program/video-scripts/gold/lesson-NN-M.json`.
Field reference for every scene type: `references/scene-reference.md`.
Model to copy: `video-scripts/gold/lesson-03-2.json`.

## Writing for the ear

- Sentences of 8 to 20 words. One idea per sentence. The linter flags anything over 32.
- Say the thing on screen as it appears: "First, L.T.V." while "LTV" is revealed. This is what drives the sync.
- Signpost: "Here's the problem.", "Now watch what happens when the price drops.", "Your turn."
- Numbers the way people say them: "fifty thousand dollars", "point eight", "two percent". Put the digits in `cap` and on screen.
- Spell abbreviations for the voice (L.T.V., E.T.H., M.E.V.) and give the normal form in `cap`. Words people say as words (DeFi, DAO, NFT) stay as they are.
- Use "you". Contractions. No filler ("basically", "essentially", "in this video we will").
- Explain the why before the how. Every rule gets a one-line reason.
- End every section with a one-line takeaway before cutting away.

## Voice over a cutaway

Screen demos need different narration: say where to look, then what it means.
"On the right of your position panel, find the number labelled Health factor. [[pause 1]]
That's the one number to watch." One action per sentence, and one shot per action,
so the highlight box and the voice move together.

## Voice over a flow

Name each node in the order it appears, and say what moves between them:
"Your wallet sends the signed transaction to a node. The node shares it with the mempool.
A validator picks it up..." Nodes light up and tokens travel on those words.

## Structure (a typical 6 to 12 minute lesson)

1. `title` (Intro)
2. `statement` or `strike` hook (Why it matters)
3. `pillars` objectives ("By the end of this lesson you'll be able to")
4. Concept: `bullets` / `compare` (1 to 3 scenes), with a `quiz` after the first big idea
5. Mechanism: `flow` (How it works)
6. Do it: `cutaway` (1 to 2 scenes), then a one-line `statement` to re-orient
7. Worked example: `steps` with `result`, then a faded example as a `quiz`
8. Pitfalls: `compare` or `bullets` with `check: false`
9. `quiz` final check
10. Your turn: `statement` with the 5 to 20 minute action and worksheet
11. Recap: `bullets` (3 items), then `cta` or `statement` "Next up: Lesson N.M"

## Upgrading a generated script to gold

1. Read the lesson file and the generated script side by side.
2. Keep what's correct; replace read-out bullet walls with the storyboard's visuals.
3. Move quizzes into the body (after each section), keep 2 to 3.
4. Add the hook, the flow, the cutaway, the faded example and "Your turn".
5. Set `"gold": true`, a strong `thumbnail.title` (2 to 4 words, the outcome or the danger), and "facts last checked: YYYY-MM-DD" in `use`.
6. Save to `video-scripts/gold/` with the same `id`. Run `python3 export/lint_video_script.py` on it.

## Length

Estimate 150 words per minute of `vo`. Target 5 to 12 minutes for most lessons, up to
25 for deep expert lessons. Over 25: split into Part 1 and Part 2 with ids
`lesson-NN-M-p1` and `lesson-NN-M-p2`.

## Compliance language

Education, not advice. Say "can", "historically", "in this example"; never "will earn",
"guaranteed", "risk-free", "safe" as an absolute. Risk is mentioned in the same breath as
reward. Keys and seed phrases are only ever mentioned as things never to share.
