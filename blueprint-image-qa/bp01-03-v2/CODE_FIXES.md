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

## Re-check at PR #17 head e0b84d5 (14 Nov)

e0b84d5 applies CF-1..CF-5. I re-scored the 25 committed PNGs under `blueprint-smoke/code-drawn/bp-0{1,2,3}-*/` (rows now say source `code-drawn@e0b84d5`, scored_blob = the committed blob). A scratch `studio.py --frames` export at e0b84d5 is pixel-identical for all 19 charts and 3 thumbnails. The 6 title and end cards differ only inside the mascot box, because the mascot is gated on the pass list, which the scratch export didn't have. So the committed PNGs are current.

| Fix | Status at e0b84d5 |
|---|---|
| CF-1 Exact disclaimer | Done. All 25 footers read exactly "Education only. Not financial advice." `FOOT`, the definition, `disclaimer_on_screen`, the YAML writer, `build_numbers.py`, `numbers/bp-0{1,2,3}*.yaml`, the 3 captions VTTs and `pack/paint.py` are all changed. Blueprint code and yaml have no "Educational content only" left. It still appears in two committed smoke outputs, `blueprint-smoke/bp-01-introduction.yaml` and `blueprint-smoke/bp-01-wrong-number.yaml` (old `smoke.py` outputs that no frame reads; regenerate them or delete them on the next smoke run). It also appears outside the Blueprint course: `.claude/skills/video-qa-review/SKILL.md`, `skills/video-production/lib/brand.py` DISCLAIMER, `skills/production-pipeline/.../build.py` and `programs/defi-program/*`. |
| CF-2 Walk charts | Done. The axis reads 30,331 / 29,431 / ... with commas. The unwalked path is drawn at alpha 150, width 2, so the whole path is visible (bp-01 walk-the-summer, bp-02 copy-the-path, bp-03 where-the-path-stood). |
| CF-3 28px tickets | Done (bp-03 hook, limit-orders-wait): tickets use font(28) on 42px tags. |
| CF-4 "a filled order" | Done. The subtitle reads "A buy order waits at 27,630. A cross is not a filled order." and the caption reads "Daily closes crossed 27,630 10 times. A cross is not a filled order." |
| CF-5 Break leaves the band | Done. In the bp-03 end-card Break panel, the path ends about 80px above the top line. |
| CF-6 Fence relabel | **Not applied.** studio.py L1226-1229 and L1272-1273 are still tuned to the old 1280x720 still. The new 1536x1024 still has now passed (see below). |
| CF-7 (new) 10 crosses, 5 marks | **Needed.** See below. |

### CF-6: exact change for the new fence still (not applied)

The new still: `course/images/blueprint-analogies/analogy-fence.png`, blob a8b3633d, from gen/blueprint-analogies/analogy-fence/web1.png. In the 840x472 panel, `_contain` scales it by 0.4609 with ox = 66 and oy = 0, so screen = (96 + 66 + 0.4609·x, 230 + 0.4609·y). The baked tags in the source are: top (1022,203)-(1461,282); bottom-left (93,750)-(729,833); bottom-right (892,750)-(1463,833). The rail centres are at y = 413 (top) and y = 611 (bottom). The baked lettering is about 35px cap height. That is about 16px in the panel, below the 28px floor, so the cover tags stay. In `course/blueprint-rebuild/studio.py` at e0b84d5:

```diff
@@ -1225,6 +1225,6 @@ def _retouch_analogy(...)
     if kind == "fence":
-        _cover_label(draw, (710, 308, 900, 350), ["Top rail", "= top price"], bounds)
-        _cover_label(draw, (184, 574, 432, 620), ["Bottom rail", "= bottom price"], bounds)
-        # One line, same height as the baked tag, so it stays under the post.
-        _cover_label(draw, (620, 578, 900, 626), ["Bounces between"], bounds)
+        # Tuned to the 1536x1024 fence still (contain scale 0.461, x offset 66).
+        _cover_label(draw, (625, 316, 843, 368), ["Top rail = top price"], bounds)
+        _cover_label(draw, (197, 568, 506, 622), ["Bottom rail", "= bottom price"], bounds)
+        _cover_label(draw, (565, 568, 844, 622), ["Price bounces between"], bounds)
         return
@@ -1272,2 +1272,2 @@ def paint_analogy(...)
-            rail_top = int(264 * src_h / 720)
-            rail_bot = int(408 * src_h / 720)
+            rail_top = int(413 * src_h / 1024)
+            rail_bot = int(611 * src_h / 1024)
```

The boxes are padded 8px past each baked tag's glow. "Price bounces between" now matches the still's own words. Each cover stays inside the panel bounds: right edges 915 / 424 / 922, all ≤ 924. To verify, I rendered a scratch export with the new still: `cf6_the-fence_preview.png`. No baked tag shows through, and the rail connectors land on the rails. Then commit the new still on d1f6 together with this change and re-render `code-drawn/bp-01-introduction/chart/range-2023/the-fence` (that row is scored against the old still for now).

Does the still teach on its own without the code labels? Yes. At full size the three baked tags are legible, spelled right and arrowed to the right parts. The code labels are needed only because the masters show the still at about 46%.

### CF-7: limit-orders-wait shows 5 marks next to "10 times" (not applied)

The caption and VO say the close crossed 27,630 ten times. That's right: 5 down-crosses (17 Aug, 30 Aug, 2/5/9 Oct) and 5 up-crosses (29 Aug, 1/4/6/16 Oct) in btc-usd-windows.json range_2023. The frame marks only the 5 down-crosses. Stage 2 noted this, but no fix was written for it. Exact change, in `course/blueprint-rebuild/studio.py` at e0b84d5, after L828 (the October dots loop):

```diff
@@ -826,6 +826,14 @@
         for index in october:
             cx = x_of(index)
             draw.ellipse((cx - 5, y_line - 5, cx + 5, y_line + 5), fill=WHITE, outline=CYAN)
+        if chapter == "Limit orders wait":
+            # The caption says 10 crosses: mark the 5 up-crosses too, as rings.
+            ups = [index for index in range(1, n) if closes[index - 1] < 27630 < closes[index]]
+            for index in ups:
+                cx = x_of(index)
+                draw.ellipse((cx - 7, y_line - 7, cx + 7, y_line + 7), outline=WHITE, width=3)
+            key = f"{len(downs) + len(ups)} crosses: {len(downs)} down, {len(ups)} up (rings)"
+            draw_ticket(key, plot[0] + 16, plot[3] - 16 - ticket_h, None)
         if october:
```

The Hook frame is unchanged, because it makes no count claim. Scratch render: `cf7_limit-orders-wait_preview.png`. It shows 5 marks plus 5 rings and the key "10 crosses: 5 down, 5 up (rings)" bottom-left in empty plot space. The full patch for both fixes is in `cf6_cf7.diff`. After applying it, re-export with `studio.py --frames` and commit the 2 PNGs.
