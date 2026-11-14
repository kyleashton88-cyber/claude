# Code-drawn stills @ d7125bc: remaining fixes

> **Superseded** by `CODE_DRAWN_FIXES_72e67cf.md` (rescore of the 17 frames redrawn at 72e67cf). Kept for history.

Scored against skills/image-quality-standard (f688829). Pass = every category at least 4 and no hard fail.
Result: **8 of 25 pass.** Coordinates are at 1920x1080 (thumbnails are 1280x720; their coordinates are scaled the same way).
Figures re-verified against course/data/public-prices/btc-usd-windows.json @d7125bc; no wrong numbers anywhere.

Passing: bp-01 hook, the-range, the-levels, walk-the-summer, the-stop; bp-02 no-secrets, copy-the-path; bp-03 where-the-path-stood.

## Ladder, fence and list panels (old stills cropped to 16:9)
1. **bp-01 a-ladder.**
   - Frame fault (a): the 7 level connectors end at the panel edge (x~935) and never reach the rungs. The ladder has ~6 rungs at other heights.
   - Fix (a): draw 7 rungs at exactly the 7 level heights, or end each connector on a rung.
   - Frame fault (b): the top 30,331 connector (y~294) runs into the panel headline "A LADDER = YOUR STEPS" (x~575-925).
   - Fix (b): move the headline or start the connectors below it.
   - *From the old still only:* brown wood is off-brand (the hard fail) and the tags are ~19px. Both clear once the remade ladder is in.
2. **bp-01 the-fence.**
   - Frame fault: the band connectors (y~296 and y~670) stop at the panel edge and miss the rails (y~403 and y~497).
   - Fix: end them on the rails, or scale the fence so its rails sit at the band heights.
   - *From the old still only:* the tags "Top rail = top price", "Bottom rail = bottom price" and "Price bounces between" are ~17-19px. That is the illegible-label hard fail; it needs the remade fence with tags of 28px or more.
3. **bp-02 hook.**
   - Frame faults: the list panel and the range chart are unrelated side by side, and the chart doesn't show the idea "Write the page before any screen".
   - Fix: drop the chart for a single page or list visual, or link one list item ("Band") to the band on the chart.
   - *From the old still only:* the tags are ~17-19px (the hard fail) and there is no headline. The remade list clears this.

## bp-02 text frames
4. **seven-lines.**
   - Row 7's icon ("The word Example on every figure", x~128, y~730) is an amber octagon. Amber is for warnings and stops only, so make it cyan.
   - Replace the ~30px ambiguous glyphs (row 5 looks like a TV or robot) with clear icons of at least 40px: notebook, ladder, coin, paper, lock, stop sign, EXAMPLE stamp.
5. **the-three-words.**
   - The EXAMPLE pill (x~1640-1850, y~197-240) sits on the Range card's top border (y~200). Move it above the stack, or inside the card's top-right with at least 24px clearance.
   - Fill the empty right halves of the cards with small pictures: two lines for Range, a ladder for Levels, a stop for Stop. Alternatively, narrow the cards.

## bp-03 order tickets
6. **hook and limit-orders-wait.**
   - The price spike at x~760-780 runs through the end of the "order waits" label (x~630-785, y~490-520), which is the hard fail. Move the label left of the first ticket or above the line.
   - Put content in each ticket, such as "BUY 27,630", not just a clock icon.
   - Space the two tickets at x~1270-1385 apart or merge them. Move the last ticket (x~1505-1565) clear of the "16 Oct 28,519" tag and dot.
   - hook only: draw the 27,630 line so the tickets sit on a level.
   - limit-orders-wait only: the caption says "27630". Write "27,630".
7. **buys-and-sells.**
   - The price path crosses the 30,331 and 29,431 tickets (x~160-222, y~315-405). Move the ticket column right of the path start, or draw the tickets with a solid fill above the line.
   - Give the tickets text ("sell 30,331" and so on) or drop them; the right-hand labels already carry the meaning.

## Title cards, end cards and thumbnails (all 9 fail)
8. **All cards.**
   - The hero graphic is a crude straight-line sawtooth.
   - Replace it with the real range_2023 path, or a proper lesson visual, at the same size.
   - Stamp EXAMPLE on any card that shows 30,331 or 24,930, or drop the figures.
9. **bp-02 title-card and thumbnail.** The graphic is labelled "Seven lines" but shows a zig-zag in a band. Show the seven-line page or list instead.
10. **bp-03 title-card, end-card and thumbnail.** The empty "order waits" ticket sits on the zig-zag. Give it content and move it off the line.
11. **End cards (all three).**
   - The graphic under "Up next: Lesson N" is THIS lesson's motif:
     - bp-01 shows "The band" for Lesson 2.
     - bp-02 shows "Seven lines" for Lesson 3.
     - bp-03 shows "order waits" for Lesson 4.
   - Use the next lesson's motif.
   - Drop the duplicate "Up next: Lesson N" line, since the left already says NEXT / Lesson N.
   - Fill or tighten the empty lower right card area (y~720-820).
12. **Thumbnails.**
   - bp-01's headline "Introduction" is all cyan. Use white with one cyan keyword, as bp-02 and bp-03 do, and a more telling title (for example "Blueprint: your first range").
   - Add a series or lesson cue ("Blueprint · Lesson 0N") to all three.
