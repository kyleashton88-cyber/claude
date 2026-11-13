---
name: scene-planner
description: Turn a lesson script or lesson.yaml into a shot list where the picture changes at least every 8 seconds. Use when planning a Blueprint, Elite, Market Check, explainer, interview, or Short, before frames are drawn.
---

# Scene planner

Read a lesson and write `shotlist.yaml` plus `shotlist.md`. Each shot is one idea. No shot is longer than 8 seconds. Word timings set the duration when a beat has `words`. Otherwise the planner estimates 2.4 words per second and splits the line.

## Visuals

The picture is one of:

| Words in the beat | Visual | Illustration-engine type |
|---|---|---|
| candle | candle chart | `candle_series` |
| grid, ladder, orders | grid ladder | `grid_ladder` |
| liquidation | liquidation warning | `liquidation` |
| analogy, fence, beginner, diagram | beginner diagram | `analogy_fence` |
| mascot, robot | mascot scene | `mascot_scene` |
| title, cover, intro | branded scene | `title_card` |

If none of those match, the shot is a motion graphic, a lower third, or kinetic type. A beat that runs past 8 seconds is split, and the later slices change treatment so the picture does not repeat.

Labels are at most four, and at most three words each. Every shot has alt text.

## Run

```bash
cd skills/video-production/scene-planner
python3 cli.py plan samples/lesson.yaml --out out-dir
```

Accepts lesson YAML, a gold script with `scenes`, or the demo script shape with `shots`.

## Do not

- Draw the frames here. The illustration engine and the motion-graphics skill do that.
- Write the shot list into `course/`.
- Call an image API.
