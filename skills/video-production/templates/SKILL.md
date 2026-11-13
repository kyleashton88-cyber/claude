---
name: video-templates
description: Format templates and distribution pieces for Stewart Crown's education videos. Use for a Blueprint lesson, Elite lesson, Market Check, explainer, interview, or Short, and for a 1280×720 thumbnail, a 9:16 cut under 60 seconds, YouTube chapters, or an end card with a next-lesson slot.
---

# Templates

Six lesson files in `formats/`, in the same shape as a lesson.yaml. Each one has a spoken disclaimer, an on-screen disclaimer, chapters, and a next lesson. Numbers in the samples are marked EXAMPLE.

| File | Format |
|---|---|
| `formats/blueprint-lesson.yaml` | Blueprint, 4–10 min, 16:9 |
| `formats/elite-lesson.yaml` | Elite, 8–20 min, 16:9 |
| `formats/market-check.yaml` | Market Check, 60–90 s, 16:9 |
| `formats/explainer.yaml` | Explainer, 3–8 min, 16:9 |
| `formats/interview.yaml` | Interview, 8–25 min, 16:9 |
| `formats/short.yaml` | Short, under 60 s, 9:16 |

## Thumbnail

1280×720. Cyan `#00D4FF`, text `#F4F8FC`, background `#00081B` to `#000F2A` to `#000B21`. Headline is Roboto Condensed Bold. Labels are Inter Bold.

```bash
cd skills/video-production/templates
python3 cli.py thumbnail --title "A grid in one picture" --label "Four facts" --out thumb.png
```

`--engine auto` calls the illustration engine (`python -m illustration_engine render`, preset `thumbnail`, 1280×720) when that package is installed. It does not pass `--llm`. When the engine is absent, the Pillow fallback draws the still. `--engine pil` forces the fallback. `--engine illustration` fails if the engine is missing.

## Short

A 9:16 cut from chapter markers, with captions, under 60 seconds. A longer chapter is trimmed to 59 seconds and the report says so. The reframe scales to 1080×1920. That scale is only for this distribution cut.

```bash
python3 cli.py short --master lesson.mp4 --chapters chapters.txt --vtt lesson.vtt --chapter "The idea" --out short.mp4
```

## Chapters and the end card

```bash
python3 cli.py chapters --lesson formats/blueprint-lesson.yaml --out description.txt
python3 cli.py endcard --title "A grid in one picture" --next "Where the range sits" --out end.png
```

The description starts with the education line. The first chapter is `0:00`. The end card is 1920×1080, held for the last 20 seconds, with the next-lesson title on the left and the right side left clear for the YouTube end screen.

## Do not

- Publish, upload, or schedule the short.
- Write into `course/`.
- Call an external image API, HeyGen, or a paid voice.
