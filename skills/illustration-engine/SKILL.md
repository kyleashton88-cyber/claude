---
name: illustration-engine
description: Draw course diagrams in-house as SVG and PNG. Use when a lesson needs a candle, a grid ladder, a range, a liquidation line, a beginner analogy, a mascot scene, or a title card, and the plate should be rendered from code rather than sent to an image tool. Does not replace the live stills path and does not write course image files.
---

# Illustration engine

Draw one idea per plate. Navy and cyan on the house preset, a short headline, two to five plain labels, and an EXAMPLE stamp whenever a figure appears. Text is SVG text in Inter (SIL Open Font License). The PNG is produced by resvg when that binary is on PATH, otherwise by CairoSVG.

Do not write into `course/`. The engine refuses any output path that contains a `course` segment. Do not publish the plates and do not send mail.

## One plate

```bash
cd skills/illustration-engine
python3 -m illustration_engine render "grid ladder, range 90-110, 10 grids, price 100, label buy and sell" --preset house --out x.png
```

Presets: `house` (1536×1024), `light`, `contrast`, `thumbnail`, and `elite`. `elite` repeats the house geometry in teal. It is provisional until Stewart confirms it.

Supported still sizes, scaled from a 1280×720 baseline: 1536×1024, 1280×720, and 1920×1080.

```bash
python3 -m illustration_engine render "grid ladder, range 90-110, 10 grids, price 100, label buy and sell" --preset house --size 1920x1080 --out wide.png
python3 -m illustration_engine render "grid ladder, range 90-110, 10 grids, price 100, label buy and sell" --preset elite --out elite.png
```

```bash
python3 -m illustration_engine render "fence analogy, practice inside" --preset contrast --out fence.png
python3 -m illustration_engine render "mascot pointing" --preset house --out mascot.png
```

A JSON or YAML spec works as the prompt too:

```bash
python3 -m illustration_engine render '{"type":"checklist","headline":"ON PAPER","labels":["RANGE","LEVELS","STOP"]}' --preset house --out list.png
```

`--llm` asks a chat model for that JSON only, then draws locally. It stays off unless `ILLUSTRATION_LLM_ENABLE=1`, `ILLUSTRATION_LLM_API_KEY`, `ILLUSTRATION_LLM_BASE_URL`, and `ILLUSTRATION_LLM_HOSTS` are set. `OPENAI_API_KEY` is not read.

`--fallback` draws candles, grid ladders, liquidation, ranges, and beginner diagrams. Mascot, cover, and branded plates need the flag left off.

`--allow-generic` rewrites an exchange or brand name to the word exchange and prints that. Without the flag the name is refused and nothing is drawn.

## A lesson

```bash
python3 -m illustration_engine batch examples/lesson-demo.yaml --preset house --out /tmp/demo-range
python3 -m illustration_engine batch ../../IMAGE_REQUESTS.json --lesson bp-01-introduction --preset house --out test-outputs/batch/bp-01-introduction
```

File names follow the lesson list (`001.png`, …). Each folder gets `MANIFEST.json` (spec, checksum, preset), `ALT.txt`, `QA.md`, and `BEGINNER.md`.

The side-by-side plates in `test-outputs/compare/` use the stills already in the lesson folder. Creative Studio measured those as fallback plates. A closer set of reference stills can replace them later. The engine does not write into `course/`. A router may copy an approved fallback plate into `course/images/_fallback_quarantine/`.

## Python

```python
from illustration_engine import parse, render_prompt, set_default

set_default("house")
spec = parse("price range, support and resistance, sideways")
render_prompt("liquidation, entry 100, liquidation 80, leverage 5, price 90", "liq.png", preset="house")
```

## What a plate contains

- One visual type. The list is `python3 -m illustration_engine types`.
- House frame 1536×1024, with the top and bottom 80px kept clear of labels.
- Headline in Roboto Condensed Bold (`font-weight: 700` on the face and the text). One word is cyan. A short headline is 89px at 1536 wide, which is a 63px cap.
- Two to five labels, sentence case, 34px at 1536 wide. Each is at most three words, with a leader or an arrow.
- EXAMPLE on any plate that shows a figure.
- The mascot, when it appears, has one visor bar and no mouth. There is no celebrating pose.

## QA

A render fails closed when a label leaves the frame, sits in the outer margin, is under the preset's minimum size, fails the contrast floor, or the PNG is blank. It also fails when the painted headline stem is under 10px at a 55px cap (that is a Regular face, not Bold) or when the lit ink covers less than 30% or more than 55% of the frame. Re-check a folder with:

```bash
python3 -m illustration_engine qa test-outputs/batch/bp-01-introduction
```

Then read `BEGINNER.md`. The human question is: with the sound off, is this one idea, in plain words?
