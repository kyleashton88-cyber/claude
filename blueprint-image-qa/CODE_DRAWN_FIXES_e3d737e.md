# Code-drawn stills @ e3d737e: remaining fixes

Standard: skills/image-quality-standard (f688829). A frame passes when every category scores at least 4 and there is no hard fail.
**17 of 25 code-drawn frames pass.** The 13 earlier passes are byte-identical (blob at e3d737e = scored blob); 4 of the 12 redrawn frames now pass: bp-02 the-three-words and thumbnail, bp-03 buys-and-sells and title-card.
Figures re-verified against course/data/public-prices/btc-usd-windows.json @e3d737e; none is wrong. Coordinates are at 1920x1080; thumbnails are 1280x720.
This supersedes the 72e67cf fix list.

## Embedded analogy panels
1. **bp-01 a-ladder: accuracy fail (check a) and an illegible-label hard fail.**
   - The connectors send the whole ladder's top and bottom (y~294 / y~669) to 30,331 / 24,930. Inside that span the still says "Rung = one price step", so a beginner matches rungs to levels and counts 5 rungs against 7 levels.
   - Fix (pick one):
     - (i) Overlay a code label "Not to scale: the chart has 7 levels" and drop the band connectors.
     - (ii) Draw 7 code rungs over the still at the 7 level heights.
     - (iii) Use a 7-rung ladder still.
   - The tags (~19-20px at 1080p, x~190-395 and x~675-835) are too small. Re-set them as code tags of at least 28px, or enlarge the panel.
2. **bp-01 the-fence: illegible-label hard fail only.** The still's three tags render at ~18px because the still is shrunk ~0.55x. Re-set them as code tags of at least 28px over the still, or drop them; the lower third already explains the rails. The rail-to-band connectors are correct.
3. **bp-02 hook: hard fail only from the embedded old analogy-list** (tags ~17-19px). It clears with a passing list remake, or with code tags of at least 28px over the panel.

## bp-03 order tickets
4. **hook and limit-orders-wait.**
   - Each "BUY 27,630" ticket (x~503-638, 698-833, 1215-1350; y~486-519) covers the crossing it marks. Lift each ticket ~40px above the line with a short leader to the crossing point, so the path visibly meets 27,630.
   - limit-orders-wait only: two of the three tickets sit on upward crossings (29 Aug, 1 Oct). A buy limit at 27,630 waits for price to fall to it, so mark downward crossings only (17 Aug, 30 Aug, 2 Oct, 5 Oct, 9 Oct), or relabel the tickets "27,630 crossed".
   - limit-orders-wait only: say what "crossed" means. Write "Daily closes crossed 27,630 10 times. That is not a receipt." (By intraday range it was touched on 12 days.)

## Cards
5. **bp-02 end-card:** the "BUY 27,630" chip (x~1160-1345, y~508-548) covers the July drop at x~1335-1345. Move it ~40px left, or place it after the drop.
6. **bp-03 thumbnail:** the chip (x~860-1045, y~325-370 at 1280x720) covers the July drop at x~955-965. Move it to x~1060+ or before the drop.
7. **bp-03 end-card** (x~1145-1720, y~310-765):
   - Trend is a single straight line; give it a rising path with pullbacks.
   - Break needs a band (two lines) with the path leaving through the top. Keep amber only if it's labelled stop.
   - Match the Range column's line weight and scale across all three columns.
