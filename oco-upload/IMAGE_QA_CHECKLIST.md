# OCO re-render image QA checklist (DRAFT)
Run this per image and per lesson. Mark each item PASS/FIX and log it against the image ID.

## Per image: technical
- [ ] Opens, not blank or corrupted; 1536x1024
- [ ] **HARD FAIL** if any headline, label or key content is outside the centre 1536x864 safe area (top/bottom 80px must be background only)
- [ ] Navy/cyan GBB v3 variant (no teal-dominant Elite look); matches anchors CTZG / 817A
- [ ] **HARD FAIL** if flat or minimal (needs glow, glass cards, depth, detailed chart/icons)
- [ ] Contrast of overlaid text 4.5:1 or better; at least 60 px safe margin clear of text
- [ ] Made with ChatGPT image; prompt logged with the image ID

## Per image: content
- [ ] Shows this beat's concept specifically; not a duplicate or near-duplicate of another beat (perceptual-hash check across the lesson and series)
- [ ] Spatial instructions followed (centred, contained, gap, overshoot); elements don't sit on box edges unless the prompt asks for it
- [ ] Text crisp and correctly spelt; one headline + a few labels only, no paragraphs
- [ ] No people or faces; only the G-badge robot with visor-bar eyes; no other face-like shapes (HARD FAIL)
- [ ] No exchange or protocol names, logos or UI lookalikes
- [ ] No profit, win-rate or income claims or imagery (money piles, rocket, hockey stick)
- [ ] **HARD FAIL** if any price/level in the art or overlay lacks EXAMPLE. Every level or number says "(Example)"; footer "Education only. Not financial advice." where levels appear; no "award-winning"

## Series continuity (per lesson, then across the series)
- [ ] Recurring motifs drawn as on the motif sheet (wallet, pool, range, risk etc.)
- [ ] Title and lower-third template identical (font, size, position, cyan rule)
- [ ] Palette identical to the previous and next lessons
- [ ] Illustration style consistent (GBB v3 glass/neon, glow strength, detail level)
- [ ] Pacing: about 20–45 s per beat, no still longer than about 60 s, runtime 15–20 min
- [ ] Same branded intro and outro (sting, music, recap and next-lesson cards, disclaimer); module intros on the shared template
- [ ] Checked against SERIES_FLOW.md (PENDING: file not in workspace yet)

## Sign-off
- [ ] Spot-check 3 frames per lesson side by side with the previous lesson
- [ ] Open issues logged; nothing published until Stewart gives a direct yes


## Hard fail: degradation
- [ ] HARD FAIL if: Image quality must not degrade at any stage: no compression artifacts, no loss of detail, no colour shift, no softening of labels or text; full resolution preserved from generation through to the final 1080p video frame.
