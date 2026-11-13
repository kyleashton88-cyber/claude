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

Presets: `house`, `light`, `contrast`, `thumbnail`.

```bash
python3 -m illustration_engine render "fence analogy, practice inside" --preset contrast --out fence.png
python3 -m illustration_engine render "mascot pointing" --preset house --out mascot.png
```

A JSON or YAML spec works as the prompt too:

```bash
python3 -m illustration_engine render '{"type":"checklist","headline":"ON PAPER","labels":["RANGE","LEVELS","STOP"]}' --preset house --out list.png
```

`--llm` asks a chat model for that JSON only, then draws locally. It needs `ILLUSTRATION_LLM_API_KEY` or `OPENAI_API_KEY`. It does not request pixels. Without a key, the flag stops and the rule parser remains the default.

## A lesson

```bash
python3 -m illustration_engine batch examples/lesson-demo.yaml --preset house --out /tmp/demo-range
python3 -m illustration_engine batch ../../IMAGE_REQUESTS.json --lesson bp-01-introduction --preset house --out test-outputs/batch/bp-01-introduction
```

File names follow the lesson list (`001.png`, …). Each folder gets `MANIFEST.json` (spec, checksum, preset), `ALT.txt`, `QA.md`, and `BEGINNER.md`.

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
- Headline in bold type. One word is cyan.
- Two to five labels, each at most three words, with a leader or an arrow.
- EXAMPLE on any plate that shows a figure.
- The mascot, when it appears, has a visor of two straight bars and no mouth.

## QA

A render fails closed when a label leaves the frame, sits in the outer margin, is under the preset's minimum size, fails the contrast floor, or the PNG is blank. Re-check a folder with:

```bash
python3 -m illustration_engine qa test-outputs/batch/bp-01-introduction
```

Then read `BEGINNER.md`. The human question is: with the sound off, is this one idea, in plain words?
