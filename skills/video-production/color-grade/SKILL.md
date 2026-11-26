---
name: color-grade
description: Professional ffmpeg color grade for teaching video. Use when a clip needs a house look, a procedural .cube LUT, auto white balance, exposure normalisation, contrast and saturation, skin-tone protection, broadcast-safe legal range, matching one clip to another, or waveform and vectorscope stills. Use this instead of a copyrighted LUT pack.
---

# Color grade

An ffmpeg grade with house looks stored as procedural `.cube` files. The LUTs are generated in this folder. They are not converted from anyone else's pack.

## When to use

- A camera shot needs to sit next to another shot from the same lesson.
- You want the clean educational look, the warmer talking-head look, or the cooler data look.
- You need a before/after and a scope to show the grade did what it claims.

## When not to use

- Designed motion graphics that are already in the house palette. Run the LUT and the legal-range stage, and leave exposure at 0. Auto exposure targets mid grey and will lift a navy field.
- A creative grade that needs a human to pull a key. This is a one-pass technical grade.

## Looks

| Name | What it does |
|---|---|
| `clean-educational` | Slight contrast, a little saturation, neutral. |
| `warm-talking-head` | Warm highlights, softer saturation, strong skin protection. |
| `cool-data` | Cooler shadows, lower saturation, a bit more contrast. |

Each look is a 33-point 3D LUT. Inside the LUT, in this order: contrast about mid grey, saturation that keeps luma, a warmth offset, a shadow/highlight split, then skin-tone protection. Skin protection keeps the graded luma and pulls chroma back toward the original when the input sits in a skin hue (about 8–52 degrees, moderate saturation, mid value). A soft shoulder leaves headroom. The legal-range step is separate, so the cube stays full-range and portable.

## Inputs

- A video ffmpeg can decode. The ungraded demo card is full-range BT.709.
- Optional `--match other.mp4`. Gains and exposure are taken from that clip instead of gray-world / mid-grey.

## Outputs

- Graded H.264, CRF 18, yuv420p, `color_range=tv`, BT.709.
- A JSON report: RGB gains, exposure in stops, and signalstats min/max.
- From `demo`: before/after split-screen movies, waveform and vectorscope PNGs, and a cool/bright card matched to the clean grade.

## The filter, in order

1. `colorchannelmixer` — gray-world white balance, green-referenced, gains clipped so a graphic is not yanked off its palette.
2. `exposure` — stops to bring mean luma near 0.42. Clipped to ±1.5.
3. `lut3d` — the house look, tetrahedral interpolation.
4. `scale=in_range=full:out_range=tv`, then `lutyuv` hard-clips luma to 16–235 and chroma to 16–240, then the frame is tagged tv. A 4:2:0 encode can reconstruct a few codes outside that. That is the subsampling, not the limiter missing.
5. `format=yuv420p`.

## Run

```bash
cd skills/video-production/color-grade
python3 cli.py luts --out luts
python3 cli.py grade --in clip.mp4 --look clean-educational --out graded.mp4
python3 cli.py grade --in clip.mp4 --look warm-talking-head --match reference.mp4 --out matched.mp4
python3 cli.py demo --out test-outputs
```

## Settings

- LUT size default 33 (`cli.py luts --size 17` for a smaller file).
- White-balance gains are clipped to 0.82–1.22 before the green reference.
- Exposure target luma is 0.42. Pass a designed graphic with gains `1,1,1` and exposure `0` (the end-to-end demo does this) and you still get the LUT and legal range.

## Failure modes

| What you see | Why | What to do |
|---|---|---|
| `unknown look` | The name is not one of the three. | Use the table above, or add a spec in `grade/lut.py` and regenerate. |
| `lut3d` cannot open the file | The `.cube` was not generated, or the path contains a colon or a space. | Run `cli.py luts`. Keep the path simple. |
| YMIN below 16 or YMAX above 235 | The legal stage was skipped, or the encode was tagged full range after a limited scale. | Keep `legal=True` and `-color_range tv`. Check `signal_range` in the report. |
| Skin goes green or magenta | Protection strength is low for that look, or the swatch is outside the hue window. | Raise `skin` on that look and regenerate the cube. The warm look is tested to move a mid skin hue by less than 8 degrees. |
| Auto exposure lifts a title card | The card is supposed to be dark. | Do not use auto exposure on designed frames. |
| `no frames decoded` | The file has no video, or ffmpeg cannot read it. | Probe the file. |
| Match makes a clip worse | The reference itself is off. | Grade the reference first, then match to that. |

## Test

```bash
python3 -m unittest tests/test_grade.py
python3 cli.py demo --out test-outputs
```

Committed samples live in `test-outputs/`: `ungraded.mp4`, one graded file and one split per look, `matched-to-clean.mp4`, and the scope PNGs. `grade-report.json` holds the measured gains and the legal-range numbers.
