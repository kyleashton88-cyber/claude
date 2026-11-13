---
name: motion-graphics
description: Code-drawn motion graphics for trading-education videos. Use when a lesson needs animated candlesticks, a grid-bot ladder with orders filling, a price range, a liquidation-line warning, labelled arrows, lower-thirds, kinetic text, number counters, a simple vector figure, or a Ken Burns / parallax move on a still that already exists. Do not use an AI image model here. Stills only come from files already in the repo, or from ChatGPT through Creative Studio on the stills path.
---

# Motion graphics

Draw teaching frames at 1920×1080 and encode them with ffmpeg. Every shape is a vector drawing command rasterized once, at final size. Nothing is upscaled.

This is the same rule as the lesson renderer: native frames, H.264, no second scale. Pillow is the drawing library because it is already the house tool and it does not need a browser or LaTeX. Remotion and Manim are not required.

## When to use

- A sentence is about a process (orders filling, a buffer shrinking) and a still would freeze it.
- You need a reusable component rather than a one-off plate.
- You want to push in on a diagram that already exists, without redrawing it and without an image model.

## When not to use

- A brand-new still illustration. That stays on the ChatGPT / Creative Studio path. This skill will not call an image model.
- A photograph of a person. The figure here is a geometric diagram, not a likeness.

## Inputs

A sequence JSON:

| Field | Meaning |
|---|---|
| `fps` | 30. |
| `width`, `height` | Must be 1920 and 1080. Other sizes are refused. |
| `shots[].kind` | `title`, `candles`, `ladder`, `risk`, or `still`. |
| `shots[].seconds` | Duration of that shot. |
| `shots[].title`, `caption` | Top line and the lower bar. |
| `shots[].lower_third` | `{kicker, line}`. Slides in from the left. |
| `shots[].image` | For `still` only. A path, absolute or relative to the repo root. |
| `shots[].fills` | The counter the still shot counts up to. |

`python3 cli.py spec` prints the built-in 29 second reel.

## Outputs

- H.264, yuv420p, BT.709, no audio, CRF 18 by default, `+faststart`.
- One PNG from `cli.py frame` when you only need a still of the animation.

## Components

| Kind | What moves |
|---|---|
| `title` | Kinetic lines, a rule, a lower-third. |
| `candles` | Candles draw on left to right. Green close above open, orange below. |
| `ladder` | Buy chips below the price, sell chips above. A cross marks the chip filled. |
| `risk` | A shaded range, a dashed liquidation line, a buffer counter, a warning pill when the gap gets small. |
| `still` | Ken Burns on an existing plate, a faster nearer crop (parallax), a callout, a counter, a geometric figure. |

The still crop stays in the top 85.5% of `liquidity-ladder.png`, so the footer wordmark never enters the frame. The crop is always larger than the destination, then scaled down.

## Run

```bash
cd skills/video-production/motion-graphics
python3 cli.py render --out test-outputs/grid-sequence.mp4
python3 cli.py render --spec my-sequence.json --out out.mp4
python3 cli.py frame --at 14 --out frame.png
```

## Settings

- `--crf` default 18. Use 16 for an intermediate you will grade later.
- `--preset` default `medium`.
- Prices and candles are illustrative and seeded. They are not a market feed and they are not a forecast.

## Failure modes

| What you see | Why | What to do |
|---|---|---|
| `Ken Burns would upscale` | The crop is smaller than 1920×1080. | Use a larger still, or a wider crop. Do not turn the check off. |
| `still not found` | `image` does not exist at that path or under the repo root. | Fix the path. Do not generate a replacement raster. |
| `unknown shot kind` | The kind is not one of the five. | Add a component in `motion/components.py` and register it in `DRAW`. |
| `sequences are drawn at 1920×1080` | Width or height was changed. | Keep the sequence at final size. |
| ffmpeg pipe error | ffmpeg missing, or the disk filled. | `ffmpeg` must be on `PATH`. Read the stderr tail the CLI raises. |
| Text from a plate is sliced | The detail crop is tighter than the line. | Anchor `detail_crop` to the top-left, or widen it. Do not scale the plate up to hide the cut. |

## Test

```bash
python3 -m unittest tests/test_motion.py
```

Committed sample: `test-outputs/grid-sequence.mp4` (29s, 1080p, H.264).
