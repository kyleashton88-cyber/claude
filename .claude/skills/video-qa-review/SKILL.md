---
name: video-qa-review
description: Quality-check a course video script and render before it ships - lint the script, test-render and inspect frames, check sync, legibility, audio, facts, numbers and compliance. Use before rendering or publishing any lesson, VSL or module video, after upgrading scripts, or when asked to review, audit or QA course videos.
---

# Video QA Review

Three passes: the script (automatic lint), the pictures (test render, look at frames),
and the substance (facts, numbers, compliance). Fix, then render the full video.

## Pass 1: lint the script

```bash
cd programs/defi-program/export
python3 lint_video_script.py ../video-scripts/gold/lesson-NN-M.json
python3 lint_video_script.py --all --summary     # whole course overview
```

**Errors (must fix):** unknown scene types, missing fields, missing asset files, flow
edges to unknown nodes, quizzes without an "The answer..." sentence, over the length cap,
and compliance hits (guaranteed or risk-free claims, periodic return promises, asking for
keys or seed phrases).

**Warnings (fix for gold):** too many text slides, text-slide runs, no visuals, no worked
example or demo, no quiz, no hook or recap chapter, long sentences, abbreviations the
voice will mispronounce, flows over 6 nodes, cutaway shots with no highlight box.

## Pass 2: test render and look

Render only the new or changed scenes, then view frames:

```bash
SCENES=5-7 node build_video.js lesson-NN-M          # writes video/lesson-NN-M-test.mp4
ffmpeg -ss 12 -i ../video/lesson-NN-M-test.mp4 -frames:v 1 /tmp/f12.jpg   # grab a frame
```

(`ffmpeg` is available as `python3 -c "import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())"`.)
Look at the frames yourself (Read the JPGs). Check:

- Nothing overlaps: captions (bottom), step captions, callouts, flow labels.
- All text is readable at phone size: nothing under 26 px, no more than about 7 words per line.
- Flows: every node and arrow is visible in the last frame; arrows aren't hidden under nodes.
- Cutaways: the highlight box sits on the right element; private details are blurred.
- Items light up while they're being spoken (scrub a few seconds around each reveal).
- Delete the `-test.mp4` afterwards; it isn't a deliverable.

## Pass 3: substance

- **Facts:** protocol parameters, fees, rates and UI labels are checked against the official docs or app, with the date in `use` ("facts last checked: YYYY-MM-DD").
- **Numbers:** every worked example and quiz answer recalculated with `defi_calc.py` or `grid_calc.py`.
- **Teaching:** the video meets the definition of done in `course-video-director` (hook, objective, flow, cutaway, worked example, spaced quizzes, your turn, recap).
- **Compliance:** "Educational content only, not financial advice" disclaimer is on screen (the renderer adds it to every frame). No income claims, testimonials or implied results. Risks stated alongside rewards. No pressure or fake urgency.
- **Accessibility:** captions file written (`video/captions/<id>.vtt`), chapter list written, colour is never the only signal (bad items also get ✕).

## After the full render

```bash
ffprobe -v error -show_entries format=duration -of csv=p=0 ../video/lesson-NN-M.mp4
ffmpeg -i ../video/lesson-NN-M.mp4 -af ebur128 -f null - 2>&1 | grep -A3 Summary   # integrated loudness near -16 LUFS
```

Then tick the lesson in the "Rendered" column of `10-video-production-plan.md`.

## Report format

Give the owner a short list: what was fixed, anything that needs their decision (a fact
you couldn't verify, a UI that needs a logged-in screenshot), and the file names ready to upload.
