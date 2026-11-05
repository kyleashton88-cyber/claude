# STYLE V3: GBB (Grid Bot Builder look), set by Stewart 5 Nov 2026
Refs: /workspace/course-images/style-ref-gbb-v1/ (10 files; QG0H and F0Y7 are the same page, "Spot vs Futures").

## Frame and safe area
Generate at 1536x1024. Video masters are 16:9 at 1920x1080 (settled), so the headline, every label and all key content stay inside the centre 1536x864 safe area. Keep about 80px at the top and bottom as background only. Video stills are a hero visual with a few labels, not a full infographic page.

## Style block: Elite (TEAL)
```
STYLE (GBB v3, Elite TEAL): Premium course still, 1536x1024. SAFE AREA: keep the headline, every label and all key content inside the centre 1536x864 band; the top ~80px and bottom ~80px are background only. Near-black navy background (#05080F to #0B1424) with depth: faint grid, soft bokeh, glowing TEAL (#14E0C8 / #0FB5A5) neon accent light. Frosted glass cards with glowing teal borders. Detailed candlestick charts with labelled dashed BUY/SELL grid lines and buy/sell fill markers. Circled teal line icons, numbered step flows, formula boxes with worked examples, comparison tables. 3D BTC, ETH and USDT coins; glossy G-badge robot mascot with visor-bar eyes only. Bold condensed all-caps headline in crisp white with ONE keyword in teal, plus a few short crisp labels. Rich and layered, never flat or minimal. Education only: every price or level is labelled EXAMPLE; no profit, return, win-rate or income claims; no exchange names or logos; no people.
```
## Style block: Blueprint / OCO (navy/cyan-blue)
```
STYLE (GBB v3, Blueprint/OCO CYAN): same as above, but the accent is electric cyan-blue (#00D4FF / #1E7BFF) on navy (#050A18 to #0A1630), as in the refs. Glass cards with glowing cyan borders, and the headline keyword in cyan. Same safe-area, text and compliance rules.
```
## Negative block
```
NEGATIVE: no flat or minimal look, no off-white paper cards, no paragraphs or garbled/misspelt text, no exchange names, logos or real app UI, no people or photos, no face-like shapes other than the G-badge robot (visor-bar eyes, no smile arcs), no money piles, rockets, trophies or profit arrows, no unlabelled prices or levels, no "award-winning", nothing important in the top or bottom 80px. Elite: no blue-dominant palette. Blueprint/OCO: no teal-dominant palette.
```
## Anchors to attach in ChatGPT web
- **Elite teal:** 01M6MSHVNG1R56TMTX6163QTJT.png (03 "What is Grid Trading": chart with BUY/SELL grid, mascot, step flow) and 01M6MSHVNHDS25DF52A243CTZG.png (04 "How does a grid bot work": numbered steps, glass cards). Add the line "recolour every blue accent to TEAL".
- **Blueprint/OCO cyan:** 01M6MSHVNHDS25DF52A243CTZG.png (04) and 01M6MSJZM9PRAVHGK3607P817A.png (09 "Mathematics": formula boxes, worked examples).
- Do not use the presenter-photo pages (Y99N, PW54) as anchors, because they would pull a real face in. Do not use the cover (K1HT): the mascot has smiling arc eyes and the price axis has no EXAMPLE label.
- The refs are portrait 2:3 (1024x1536). The prompt has to state landscape 1536x1024 and the safe area.
- Anchor-match line (first line of every paste): "Match the attached reference images' style exactly (...) Landscape 1536x1024 with all text and key content inside the centre 1536x864 safe area. New subject below."

## QA rubric
HARD FAIL (any one = reject):
1. Any headline, label or key content outside the centre 1536x864 safe area.
2. Flat or minimal: no glow, no glass cards, no depth, or a sparse single-object look.
3. Wrong variant colour (Elite not teal-led; Blueprint/OCO not navy/cyan).
4. A price, level or number shown without EXAMPLE.
5. A profit, return, win-rate or income claim, "award-winning", or money/rocket/trophy imagery.
6. Exchange name, logo or real-app UI lookalike.
7. People, or any face-like shape other than the visor-eyed G-badge robot.
8. Garbled, misspelt or paragraph-length text.
9. Wrong size (not 1536x1024) or the shot's teaching meaning is missing.
Score 1-5 (pass needs 4+ average, no hard fail): headline crispness and accent keyword; chart/icon detail; glass and glow depth; label economy (a headline plus 2-4 labels); anchor match.

## Compliance concerns in the refs themselves (do not copy)
- Profit/return language: 03 "capturing profits from every completed cycle", "many small wins compound into significant returns"; 02 Introduction "consistent returns"; 04 "Profit collected", "Compound effect"; 05 "Potentially higher returns", "Profit potential"; 06 "Profit in sideways markets", "Compounding small wins"; 07 "maximise profits", "Profit per Cycle ~1%-2%"; 08 "compounding small profits"; 09 "Expected Daily Return $40", "Expected Monthly Return $1,200", "Future Capital ~ $1,644"; cover "Proven Strategy", "Consistent Returns", "Grow your portfolio".
- Prices and levels without an EXAMPLE label: cover price axis 22,000-36,000; 07 "Example Grid Setup (BTC/USDT)" 60,000-70,000 / $10,000 (labelled only as a title, not on each level); 09 Range $70,000-$60,000, $1,000 etc. under "Example:" headers but not per value. The BUY/SELL 1-3 grid lines on 03, 04, 08, 09 and the cover carry no prices but also no EXAMPLE label.
- The cover mascot has smiling arc eyes (the rule is visor-bar eyes only). There are target/bullseye icons on 02, 03, 06 and 07.
- Real presenter photo (Stewart) on 02 and 06. 08 recommends specific settings ("1%-2% of your portfolio"), which reads as advice.
- No exchange logos seen. The coins (BTC, ETH, USDT) are allowed.

## Files
- v3 prompts: batch-web/v3/{batch-01..24, el-05-r2-batch-A, el-05-r2-batch-B}.json + .txt (133 items; the old prompt is kept as prompt_v2; originals untouched). Generator: batch-web/v3/build_v3.py.
- OCO: /workspace/oco-upload/IMAGE_BRIEF.md and IMAGE_QA_CHECKLIST.md updated (.bak = previous).


## Hard rules for every still (Creative Studio v3b, 5 Nov 2026)
- No text beyond the named headline and labels. No branding, no byline (no "BY STEWART CROWN"), no course headers, no logos, no extra sub-labels, no sentences.
- Charts go sideways or are left out. No rising charts or arrows, and no $ axes or $ text.
- Coins are BTC, ETH and USDT only, at most 3 per vault. No gold coins. Rims are plain, with no text. Never duplicate a coin type where the beat says single, lone or independent.
- The background is one seamless pass. No paper blocks. Nothing in the top 80px or the bottom 80px.
- Elite: teal glass cards and glow only, never flat navy or matte grey. Blueprint and OCO: the same glass and glow in cyan.
- The robot, when it appears, matches the passed el-06 shot 28: visor-bar eyes, no smile.
- A toggle is OFF (knob left, track unlit) unless the label says otherwise.
- The picture must match its labels.
- Passed anchors to attach instead of the book pages: el-06 shots 28, 31, 32, 34, 38 and 39, and el-07 shot 14.

## No degradation (Stewart, 5 Nov 2026)
Image quality must not degrade at any stage: no compression artifacts, no loss of detail, no colour shift, no softening of labels or text; full resolution preserved from generation through to the final 1080p video frame.

- HARD FAIL (degradation): compression artifacts, lost detail, colour shift, soft labels/text, or below full resolution at any stage.
