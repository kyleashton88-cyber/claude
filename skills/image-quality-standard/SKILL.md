---
name: image-quality-standard
description: The single pass bar for course stills and illustration-engine plates. Use before accepting any image, after a render, or when a review says the pictures look unfinished.
---

# Image quality standard

This replaces the four disagreeing checks:

- `.cursor/skills/illustration-qa` (script and render checklist; deprecated as a score)
- `.cursor/skills/beat-illustration-prompts` (prompt writing; deprecated as a score)
- `skills/illustration-engine` technical preflight (fonts, margins, blank PNG; not appeal)
- Creative Studio image-style-qa (a box skill, not in the repo; mirrored in `rubric.json`)

Lesson images are still made in ChatGPT. This standard does not change that path and does not call an image API.

## Pass bar

Score each category from 1 to 5. A plate passes only when every category is at least 4 and there is no hard fail.

1. Beginner clarity. One idea, readable with the sound off.
2. Composition and hierarchy. One subject, a headline, quiet space. A glowing rectangle is not a composition.
3. Craft and polish. Line weight, glass, and depth that can sit beside the reference stills.
4. Brand fidelity. Navy ground, cyan `#00D4FF`, white type, one cyan keyword. Mint is sell. Amber is warning, stop, or liquidation. Electric blue is buy or the current price.
5. Text legibility. Words stay separate. Bold headlines. Labels are sentence case and large enough.
6. Character consistency. A character is the approved sheet in `skills/illustration-engine/illustration_engine/assets/character/poses/`, in the locked box. No sheet means no character. A generated robot is a hard fail.
7. Accuracy of labels and numbers. The words and figures match the lesson. Example figures are stamped EXAMPLE.

Hard fails, any one of which fails the plate: a misspelling, off-brand colours, a muddy or illegible label, a cramped margin, a wrong number, an inconsistent mascot.

## What code can measure

`python3 skills/image-quality-standard/check.py <png-or-folder>`

It reports contrast, margins, fill, legibility inputs, palette distance, and SVG spelling when the SVG sits beside the PNG. It does not award category scores. Every category above is marked `human_required`. There is no OCR binary on the render box, so spelling from pixels stays a human check; the checker lists the SVG words for that review.

## References

`references/good/` holds ChatGPT lesson stills copied from `course/images/bp-01-introduction/`. `references/bad/` holds engine plates that scored as amateur: a generated mascot and milk-halo frames. See `references/INDEX.md`.

## Scores

Human scores for the current engine gallery live in `test-outputs/SCORES.md`. A technical preflight that says zero failures is not a pass.
