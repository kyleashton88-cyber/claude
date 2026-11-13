---
name: beat-illustration-prompts
description: Write a ChatGPT image prompt for one tutorial beat so the still shows the exact concept being taught. Use when a lesson needs images, when IMAGE_REQUESTS.json is incomplete, when a beat would reuse a still, or when a picture is thin, stock-like, or a grey placeholder.
---

# Beat-to-illustration prompts

Deprecated as an image-quality rubric. Prompt writing stays here. Whether a still is good enough to ship is `skills/image-quality-standard/` (pass bar 4 in every category, no hard fail). Lesson stills are still made in ChatGPT. This skill does not switch that path.

Every beat gets its own still. Code may add captions, lower thirds, the disclaimer line, and a slow zoom. Code does not draw the diagram, the chart, the checklist, or the character for a live lesson.

## When to write one

- A beat has no image.
- A beat would reuse another beat's file.
- The current still could be swapped to a different sentence and still "fit".
- The still is a blank page, a grey bar, or a generic document.

## The prompt

Use `course/tools/prompt_writer.py` (`write_prompt`) so the palette and the bans stay stable. A hand prompt must still contain all of these:

1. Lesson title, beat number, and role, so two similar beats cannot collapse.
2. A layout: one diagram, a before/after pair, three steps, an annotated chart, or a generic unbranded form.
3. The exact shapes that teach the sentence (nineteen gaps, a health bar, a stop under the band). Not "a worksheet about the topic".
4. At most four short labels, spelled as they should appear. Stamp Example on any chart.
5. The style lock: navy `#050A12` to `#0A1628`, cyan `#00D4FF`, electric blue `#1E5EFF`, off-white panels, empty bottom fifth.
6. Bans: coins, profit, trophies, logos, logins, seed phrases, real exchange screens, a chart that only rises.

Elite stays teal. Do not put an Elite lesson in this navy-and-cyan request file.

## Where it goes

Append the prompt to `IMAGE_REQUESTS.json` with `out_path` set to `course/images/<lesson>/<beat>.png`. Do not generate the PNG in the lesson-writing step. The orchestrator generates it with ChatGPT and commits the file. After the files exist, `course/render/render_tutorial.py` can render. It refuses a lesson that is missing a still, rather than reusing one.
