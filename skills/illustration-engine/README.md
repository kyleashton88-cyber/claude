# Illustration engine

In-house diagrams for course lessons. A sentence or a YAML spec becomes an SVG, then a PNG. Nothing here calls an image API, and nothing here writes into `course/`.

The live stills path is unchanged. Use this engine when you want a plate drawn in the repo.

## Layout

| Path | What it is |
|---|---|
| `SKILL.md` | How to invoke the engine |
| `illustration_engine/` | The package: parser, presets, drawers, QA, batch |
| `illustration_engine/types/` | One drawer per visual type |
| `illustration_engine/assets/fonts/` | Inter, under the SIL Open Font License |
| `examples/lesson-demo.yaml` | A three-slot lesson file |
| `tests/` | Parser, theme contrast, and render checks |
| `test-outputs/` | Generated plates, a lesson batch, comparisons, a contact sheet |

## Visual types

Candle anatomy, candle series, candle pattern, grid ladder, liquidation, price range, flowchart, comparison, steps, fence, ladder, buckets, checklist, mascot scene, title card, lesson cover, section divider.

## Presets

`house` (navy and cyan, 1536×1024), `light`, `contrast`, `thumbnail`, and `elite` (teal, provisional until Stewart confirms it). Sizes scale from 1280×720. Supported still sizes are 1536×1024, 1280×720, and 1920×1080. Headlines are Roboto Condensed Bold. Labels are Inter Bold.

## Commands

From this directory, after `pip install -r requirements.txt`:

```bash
python3 -m illustration_engine render "grid ladder, range 90-110, 10 grids, price 100, label buy and sell" --preset house --out x.png
python3 -m illustration_engine batch examples/lesson-demo.yaml --preset house --out /tmp/demo
python3 -m illustration_engine gallery --out test-outputs
python3 -m illustration_engine types
```
