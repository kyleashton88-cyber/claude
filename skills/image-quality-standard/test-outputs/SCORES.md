# Scores against the image quality standard

Scored by eye on the gallery rendered after the fallback-gate rebuild. The pass bar is 4 in every category and no hard fail. These plates do not pass.

A character cell is n/a when the plate is not a character plate. A mascot plate with no approved sheet scores 1. That is not a pass.

| Type | Clarity | Composition | Craft | Brand | Legibility | Character | Accuracy | Hard fail | Pass |
|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| Mascot scene | 3 | 3 | 2 | 3 | 4 | 1 | 4 | no approved character | no |
| Lesson cover | 3 | 3 | 2 | 3 | 4 | n/a | 4 | none | no |
| Grid ladder | 4 | 3 | 3 | 4 | 4 | n/a | 4 | none | no |
| Candle anatomy | 4 | 3 | 3 | 3 | 4 | n/a | 4 | none | no |
| Three-step | 3 | 3 | 3 | 3 | 4 | n/a | 4 | none | no |
| Checklist / flowchart | 3 | 3 | 2 | 3 | 4 | n/a | 4 | none | no |
| Warning / liquidation | 3 | 3 | 3 | 4 | 4 | n/a | 4 | none | no |
| Analogy scenes | 3 | 3 | 2 | 3 | 4 | n/a | 4 | none | no |
| Elite | 4 | 3 | 3 | 3 | 4 | n/a | 4 | none | no |

The technical preflight can still say pass. That only means the font, the frame, and the margins held. It is not this score.

## Why nothing ships

The mascot plate has no figure. The old rectangle robot was removed, and no Creative Studio sheet has been dropped into `assets/character/poses/`. A missing character is not a professional character.

The diagrams are clearer than the milk-halo pass: the ladder sits on the grid, the step cards have a small mark, the rim is thinner. They are still code drawings. Labels are still one word. The rotated EXAMPLE watermark is still on the ladder. Craft stays at 2 or 3.

## Automated check

`python3 skills/image-quality-standard/check.py <png>` reports margins, fill, palette, and the SVG words. It leaves every category as `human_required` and does not set `pass`.
