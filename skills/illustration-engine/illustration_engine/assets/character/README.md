# Character sheet slot

The engine does not draw a mascot. A generated robot made of rectangles and circles was rejected as kindergarten work. A professional character is drawn once, outside this engine, in ChatGPT through Creative Studio, and dropped here as locked poses.

Until those files exist, mascot plates render the diagram only and mark `character: withheld`. They do not invent a stand-in.

## Files

Put one PNG per pose in `poses/`. The name is the pose, lowercase:

- `explain.png`
- `point.png`
- `warn.png`
- `think.png`
- `thumbs.png`
- `turnaround.png` (front, three-quarter, and side on one sheet; not placed on a lesson plate)

## Locked tokens

Every lesson plate uses the same placement. Do not crop or recolour per lesson.

- Height is 520px on a 1536-wide frame, and scales with `canvas width / 1536`.
- The figure sits on the bottom-left of the content area, 24px in from the left padding.
- The pose file's aspect ratio is kept.
- Palette in the drawing itself: body off-white, visor near-black, one cyan visor light, rim `#B8FFFF`. No mouth. No second character.
- The same file is used every time that pose is requested. The engine does not redraw it.

## Who draws it

Creative Studio, from the live ChatGPT account. Not Flux, not an image API, not this SVG renderer. Stewart approves the sheet before any pose file is committed.
