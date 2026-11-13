---
name: quality-gate
description: Pass or fail a finished lesson master before anyone reviews it. Use when a Blueprint, Elite, Market Check, explainer, interview, or Short master needs a single gate for length, loudness, frozen frames, captions, brands, gaps, format, and the disclaimer. Use this instead of the old 15-minute check.
---

# Quality gate

One pass/fail for a master. The report is `report.json` and `report.md`. A failure exits 1. The tool does not publish, upload, or email.

## What it replaces

`course/skills/motion_picture/qa.py` still prints loudness and fails a master under 15 minutes. `course/blueprint-rework/render_motion.py` still exits when a render is under 15 minutes. Those files stay. This gate is the one to run.

The approved Blueprint lesson BP-01 is 6:15. That length is inside the Blueprint window (4–10 minutes). The old 15-minute floor rejects it. Do not put that floor back.

## Formats

| Format | Length | Frame | Longest still picture |
|---|---|---|---|
| `blueprint` | 4–10 min | 1920×1080 | 8 s |
| `elite` | 8–20 min | 1920×1080 | 8 s |
| `market-check` | 2–8 min | 1920×1080 | 8 s |
| `explainer` | 3–8 min | 1920×1080 | 8 s |
| `interview` | 8–25 min | 1920×1080 | 12 s |
| `short` | 5 s to just under 60 s | 1080×1920 | 5 s |

`python3 cli.py formats` prints the table.

## Checks

Every check is pass or fail. A missing measurement is a fail.

| Check | Fail when |
|---|---|
| Length | Outside the format window. |
| Loudness | Integrated loudness is outside −14 LUFS ± 1. |
| True peak | Above −1 dBTP, or the meter did not return a peak. |
| Frozen | Near-identical frames last longer than the format limit. |
| Black | A near-black run lasts longer than 0.5 s. Navy `#00081B` is not black. |
| Silence | Silence lasts 2 s or more. |
| Resolution, fps, codec | Not the profile frame, not 30 fps, not H.264 yuv420p, or not AAC. |
| Captions | No caption file, a line over 42 characters, more than 2 lines, or faster than 20 characters per second. |
| Text recognition | `tesseract` is missing or a frame fails to read. Brand and margin checks fail with it. They are not skipped. |
| Brands | An exchange or banned brand name is in the captions, the transcript, or the picture. |
| Safe margins | A recognised word sits in the outer 4% of the frame. |
| Disclaimer | Neither the captions, the transcript, nor the picture contains an education line that says not financial advice. |

## Run

```bash
cd skills/video-production/quality-gate
python3 cli.py check master.mp4 --format blueprint --captions master.vtt --out report-dir
```

`--transcript` is optional and is included in the disclaimer and brand scans.

## Do not

- Publish, upload, or email.
- Write the report into `course/`.
- Call a paid voice, image, or avatar API.
