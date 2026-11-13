# Code-drawn stills @ 0eb1dc6: remaining fixes

Standard: skills/image-quality-standard (f688829). A frame passes when every category scores at least 4 and there is no hard fail.
**19 of 25 code-drawn frames pass.** The 11 earlier passes not touched in 0eb1dc6 are byte-identical (git blob at 0eb1dc6 = scored_blob). Of the 14 changed frames, 8 pass: bp-01 a-ladder, the-fence, title-card, end-card; bp-02 title-card, end-card; bp-03 title-card, end-card.
Figures re-verified against course/data/public-prices/btc-usd-windows.json @0eb1dc6; none is wrong. Coordinates are at 1920x1080; thumbnails are 1280x720.
Mascot: every card uses the approved cut-out (course/images/mascot/blueprint-mascot.png, blob 5d421ae). On the navy ground there is no dark halo; only the thin cyan rim shows. The halo would only show on a light area, and no card puts it on one.
This supersedes the e3d737e fix list.

## Fixed since e3d737e (now passing)
- bp-01 a-ladder: the full still and headline are fitted; the connectors are gone; the tags are code tags at ~28px; the chip says "Not to scale: the chart has 7 levels" (fix option i).
- bp-01 the-fence: the tags are code tags at ~28px; the connectors run from the rails to 30,331 / 24,930.
- bp-02 end-card: the chip is clear of the July drop.
- bp-03 end-card: Trend has pullbacks; Break has a band with the path leaving through the top.

## Still failing
1. **bp-02 hook: illegible-label hard fail.** It now embeds the passing analogy-list (blob 91c8667), but the still is shrunk ~0.55x. Its four tags ("Pair: what you trade", "Range: top and bottom price", "Gaps: step size", "Stop: when you quit", x~200-400, y~375-640) render at ~17-18px.
   - Fix: re-set those four tags as code tags of at least 28px over the panel, as on a-ladder and the-fence, or enlarge the panel.
2. **bp-03 limit-orders-wait** (clarity 3, composition 3). The caption is fixed and the 10 crossings are verified.
   - (a) The first ticket (x~505-640, y~425-465) covers the 17 Aug drop. Lift it ~40px or shift it left, so the path visibly meets 27,630.
   - (b) The second ticket's leader ends on the 29 Aug peak, which is an up-close. Point it at the 30 Aug down-crossing (one day right, x~+16px).
   - (c) The three stacked October tickets (x~1110-1245, y~340-465) use elbow leaders that run just under the 27,630 line (y~520-532) and end below the level (x~1295/1338/1408). They tangle and read as extra lines.
     - Use straight diagonal leaders from each ticket to the exact crossing point ON the 27,630 line (2 Oct, 5 Oct, 9 Oct), with no horizontal runs.
     - Or replace the three tickets with one ticket, "3 more in October", plus three dots on the line.
   - (d) Keep the stack at least 40px from the "16 Oct 28,519" tag.
3. **bp-03 hook** (composition 3). It has the same ticket faults as limit-orders-wait: (a) the first ticket covers the drop; (b) the second ticket points at the 29 Aug peak; (c) the third ticket's elbow leader runs ~17px under the 27,630 line to x~1278. Apply the same fix.
4. **bp-03 thumbnail** (composition 3).
   - (a) The moved "BUY 27,630" chip (x~1035-1220, y~330-368) now covers the October path: the peaks and the final up-move run behind it. Its right end also overhangs the chart area. Put the chip on the empty left end of the line (before the July drop; the line is clear there at y~345), or above the band with a short leader.
   - (b) The mascot problem in item 5.
5. **bp-01 thumbnail and bp-02 thumbnail** (composition 3, and bp-03 thumbnail too). The mascot added at x~630-730, y~500-650 is only ~150px tall on a 720px frame. It is wedged between the headline, the footer and the card. At thumbnail display size (~250-320px wide) it is ~30px tall, so it reads as a speck and a second subject.
   - Fix (pick one):
     - Drop the mascot from the thumbnails, since the cards already carry it.
     - Make it a real subject: at least ~45% of frame height (~330px), standing in the left-centre gap with the headline shortened or set above it. Keep at least 45px from every edge and from the footer.

## Not failing, worth a look
- bp-01 a-ladder: the "Not to scale" chip is ~12px under the panel edge. Give it ~24px.
- bp-01 the-fence: the "Top rail = top price" tag covers the top of the right post.
- bp-02 end-card: the chip's left end overhangs the chart's left edge slightly.
