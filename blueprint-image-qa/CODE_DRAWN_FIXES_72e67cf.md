# Code-drawn stills @ 72e67cf: remaining fixes

Scored against skills/image-quality-standard (f688829). A frame passes when every category scores at least 4 and there is no hard fail.
Scope: the 17 frames that failed at d7125bc and were redrawn in 72e67cf. The other 8 are byte-identical to d7125bc (blobs checked) and still pass.
Result: **13 of 25 code-drawn frames pass** (5 of the 17 redrawn). Coordinates are at 1920x1080; thumbnails are 1280x720.
Every figure was re-checked against course/data/public-prices/btc-usd-windows.json @72e67cf, and none is wrong.

Newly passing: bp-01 title-card, end-card and thumbnail; bp-02 seven-lines and title-card.

## Embedded analogy panels
1. **bp-01 a-ladder** (frame crop; the ladder still itself passes). This has hard fails.
   - The headline "A LADDER = YOUR STEPS" is not half-cut; it is cropped out completely. The panel (x~96-935, y~232-700) starts at the second rung.
   - Both tags are cut by the panel edges: "ng = one price step" (x~96-330, y~262-305) and "Gap = distan / between ste" (x~750-935, y~322-400).
   - Fix: fit the whole 1536x1024 still into the panel (contain, not cover), so the headline and both tags are fully inside with at least 24px clearance.
   - The 7 level connectors (x~700-935) stop before the rungs (which end at x~680), and the 28,531 connector runs into the Gap tag. End the connectors at the panel edge and keep them clear of the tags. The still has 5 rungs and the chart has 7 levels, so don't imply a one-to-one match.
2. **bp-01 the-fence** (frame crop; the fence still itself passes).
   - The deep zoom on two plank textures loses the posts and the headline "A FENCE = YOUR RANGE", so it no longer reads as a fence.
   - The zoom also makes the wood grain soft and gives the zig-zag stair-stepped edges, and the zig-zag is cut off at both panel edges.
   - Fix: fit the whole still (contain). Keep the new connectors ending on the rails at their fitted positions. Keep any still tags at 28px or larger at 1080p, or drop them.
3. **bp-02 hook.** This has hard fails.
   - The EXAMPLE pill's right end (x~1807, y~232-265) touches the card border (x~1808). Move it in by at least 24px.
   - The "Band" leader runs from the tag (x~130-225, y~450-490) across the notebook and through the highlighted GAPS item. Route it from the BAND item, or drop it.
   - *Embedded old analogy-list only:* its four call-out tags are ~17-19px. That hard fail clears only with a passing list remake.

## bp-02 text frame
4. **the-three-words.**
   - The Range row's icon is the EX stamp (x~130-170, y~262-292); use a two-line range icon instead.
   - Align the right-side pictures in one column at a fixed x (say 1500-1760), at the same size. The stop octagon at x~1285 crowds the end of the sentence (x~1240) and duplicates the left icon.
   - Or drop the right-side pictures and narrow the cards so they aren't 35% empty.

## bp-03 order tickets
5. **hook and limit-orders-wait.**
   - Two identical "BUY 27,630" tickets sit side by side at the start (x~150-300 and 337-484, y~455-492). Show one waiting order, or put tickets at a few of the real 27,630 crossings. In limit-orders-wait the picture should show crossings, because the caption claims "crossed 10 times. That is not a receipt".
   - The "16 Oct 28,519" tag box (x~1255-1505, y~425-465) is oversized, with its ~22px text crammed left and its edge ~15px from the end dot. Fit the box to the text, use ~28px type as before, and leave at least 24px to the dot.
6. **buys-and-sells.**
   - The ticket column (x~425-597) hides the price path: the path goes behind "sell 30,331" and "sell 29,431" (y~305-405), and the July drop (x~565-590) runs behind "sell 28,531" and "middle 27,630".
   - Move the ticket column into empty space (for example x~1000-1170, where the path sits low) or drop it; the right axis already carries the same seven labels.

## Cards and thumbnails
7. **"BUY 27,630" chip below the band.**
   - It appears on the bp-02 end-card (x~1535-1610, y~968-992, ~14px text), the bp-03 title-card (x~1003-1135, y~778-806) and the bp-03 thumbnail (x~845-995, y~512-545 at 1280x720).
   - It sits under the 24,930 label, outside the band, with no 27,630 line, so it reads as a buy at the bottom.
   - Fix: draw the 27,630 line in the card and sit the chip on it with ~24px+ type, or drop the chip.
8. **bp-03 end-card.** The three columns Range / Trend / Break (x~1145-1720, y~320-760) are empty placeholders. Draw a mini path in each: sideways in a band, rising, and breaking out of the band.
9. **bp-02 thumbnail.** This has a hard fail: the "Example on every figure" row ends at x~1233, past the card border at x~1230. Widen the card or shorten the row to "EXAMPLE on figures", keeping at least 16px inside the border.
