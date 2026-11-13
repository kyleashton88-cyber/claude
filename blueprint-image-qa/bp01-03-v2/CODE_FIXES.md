# BP-01..03 code-drawn frames: code fixes needed

These frames are drawn by the repo's code, so they can't be remade on ChatGPT. Line numbers are for `course/blueprint-rebuild/studio.py` at d1f6 `fbb3f9c`. The full patch is in `code_fix.diff`, next to this file.

How I checked: I re-rendered the 25 frames with `studio.py --frames` at fbb3f9c, applied CF-1..CF-5 to a scratch copy, and rendered again. Every listed problem cleared and no new ones appeared. Nothing was pushed or committed to code.

Stale committed PNGs: `blueprint-smoke/code-drawn/*.png` on d1f6 were rendered at 61c4f97. For 22 of the 25 frames they differ from what fbb3f9c draws: 61c4f97 changed the grid colour, the axis label size and the walk-chart number format. The 3 thumbnails are byte-identical. After the fixes, re-export with `studio.py --frames` and commit those PNGs.

| Fix | Frames | Exact change |
|---|---|---|
| CF-1 Exact disclaimer | all 25 (every footer, plus the disclaimer definition and numbers files) | studio.py L63 `FOOT = "Educational content only. Not financial advice."` -> `FOOT = "Education only. Not financial advice."`; L1899 `"definition": ...`, L1926 `"disclaimer_on_screen": ...` and L1939 (the YAML writer) get the same string; regenerate `course/blueprint-rebuild/numbers/bp-0{1,2,3}*.yaml`. Also `skills/video-production/templates/pack/paint.py` L95 (same string, thumbnail template). |
| CF-2 Walk-chart figures | bp-01 walk-the-summer, bp-02 copy-the-path, bp-03 where-the-path-stood | L737 `color, width, label = MUTED, 2, str(rounded)` -> `color, width, label = MUTED, 2, f"{rounded:,}"` so the axis reads 30,331 like the tag and every other frame. L690 `_stroke(base, rest, (0, 212, 255, 89), 1)` -> `_stroke(base, rest, (0, 212, 255, 150), 2)` so the unwalked path is visible and the still doesn't read as an empty chart. |
| CF-3 Ticket size | bp-03 hook, bp-03 limit-orders-wait | L795 `face_t = font(22)` -> `font(28)`; L798 `ticket_h = 36` -> `42`; L811 `face = font(22)` -> `font(28)` (28px minimum at 1080p). |
| CF-4 Plain words | bp-03 limit-orders-wait | L516 `"A limit order waits at 27,630. A cross is not a receipt."` -> `"A buy order waits at 27,630. A cross is not a filled order."`; `course/blueprint-rework/lesson_scripts.py` L380 caption `"Daily closes crossed 27,630 10 times. That is not a receipt."` -> `"Daily closes crossed 27,630 10 times. A cross is not a filled order."` (10 checked against btc-usd-windows.json range_2023: 5 down-crosses, 5 up-crosses). The spoken VO on L378 also says "receipt"; that's narration, so I left it alone. |
| CF-5 Break leaves the band | bp-03 end-card | L932 (regimes panel, Break branch) `top = py0 + 16` -> `top = py0 + 90`, so the path breaks through the top line and finishes about 80px above it, instead of ending about 10px above. |
| CF-6 (after the fence remake lands) | bp-01 the-fence (and its embedded panel) | `_retouch_analogy` L1226-1229 cover boxes are pixel-tuned to the old 1280x720 fence still. Once the 1536x1024 remake replaces `analogy-fence.png`, re-measure them or delete the fence branch if the new tags read at 28px or more in the 840x472 panel. |

After CF-1, the only frames still failing are those listed for CF-2..CF-5 (6 frames). The other 19 then meet the standard.
