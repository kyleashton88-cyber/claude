# Fallback QA: Elite v3 stills, 2026-11-05 (v3a)
Source: kyleashton88-cyber/claude PR #6, branch cursor/course-video-qa-fix-7f90, course/images/fallback/<lesson>/<shot>.png (28 awaiting_qa items in FALLBACK_MANIFEST.json).
Rubric: /workspace/course-images/STYLE_V3_GBB.md (hard fails plus no-degradation rule). QA'd by viewing every still at full res with the 80px / 944px safe-area lines drawn on.

## Automated checks
- image_qa.py (--size 1536x1024): 28 files, 0 flagged (size, duplicate, brand colour and dark background all OK). See image_qa_report.md.
- All 28 are 1536x1024 RGB PNG, and all md5 hashes are different.
- Safe area: on all 28, rows 0-79 and 944-1023 are one flat colour, (5,8,15). No text or content sits outside the 1536x864 band.
- Prompt match: the manifest prompt for every item is identical to the `prompt` field in its source batch (el-05-r2-batch-A/B.json, batch-01/02.json).
- Recurring defect: a visible darker rectangle or band inside the safe area ("panel seam"), which makes the hero look pasted in and not one continuous background. I count it as a degradation fail (lost depth or detail, colour step).

## Results
| Still | Result | Reason | Fix |
|---|---|---|---|
| el-05-18 | FAIL | Sparse single-card look with no grid or bokeh (minimal). Headline is centred, but the brief asks for top-left. | Regenerate with the full v3 prompt and stress "faint grid, soft bokeh, depth, headline top-left". Attach both teal anchors. |
| el-05-19 | FAIL | Panel seam: a darker inner rectangle is visible around the content (about x 140-1330). | Regenerate with "one continuous background, no inner panel or vignette box". |
| el-05-20 | FAIL | Garbled chart text ("TERY 1", unreadable axis ticks), soft or blurry chart, panel band seam. The coins carry G logos, but the shot needs BTC/ETH-style coins. | Regenerate. Drop axis numbers ("chart with no axis numbers, one label MOVE TOGETHER?"), use 3D BTC and ETH coins, keep the background continuous. |
| el-05-21 | FAIL | Panel seam (darker rectangle behind the content). | Regenerate with "continuous background, no inner box". Composition and text are otherwise fine. |
| el-05-22 | FAIL | The literal placeholder text "SHORT LABEL" appears. There is an unrequested BUY/SELL grid chart with mascot, and a horizontal band seam. | Regenerate. Replace "short label card" in the prompt with a named label (e.g. "label card reading CAP"), then remove the chart and mascot. |
| el-05-29 | FAIL | Step 3 shows $-dollar coins, which is money imagery, and the brief asks for grouped BTC/ETH coins. | Regenerate step 3 with "3D BTC and ETH coins, no $ symbols". |
| el-05-30 | PASS | Rich glass cards, budget bar, single coin and grouped coins. Labels are correct and crisp. Teal-led and inside the safe area. | — |
| el-05-31 | PASS | BTC and ETH sit in a glass frame. "RESTATE THE GROUP" has the teal keyword, and SAME GROUP is crisp and inside the safe area. | — |
| el-05-40 | FAIL | The headline has a stray trailing comma ("CLEAN PAGE,"). A sentence label reads "A fresh start ensures optimal performance and clarity", which is a paragraph and reads like a performance claim. Band seam. | Regenerate with the exact headline "SECOND PASS, CLEAN PAGE", the clean card showing only a grouped-coin frame plus a NOTE tag, and the instruction "no sentences". |
| el-05-41 | FAIL | Unrequested text "ELITE COURSE / SYSTEM ARCHITECTURE", a pile of six or more mixed coins (one with a $ mark), and a scrap card that is not faded or tilted. | Regenerate with a faded, tilted scrap card and a clean card holding just two grouped BTC/ETH coins. Specify "no other text, no $". |
| el-05-45 | FAIL | Gold coin stack (money-pile imagery), a sentence label ("Operates independently."), and a band seam. | Regenerate with two grouped BTC/ETH coins and one lone coin with a small NOTE tag. Specify "no coin stacks, no sentences". |
| el-05-47 | FAIL | Panel seam (darker box around the content, about x 100-1430). Content and labels are otherwise correct. | Regenerate with a continuous background. |
| el-05-48 | FAIL | Coin stacks (money pile) and a rising 3-bar chart that reads as growth or profit, where the brief asks for a budget bar. | Regenerate with "horizontal budget bar (as shot 30), one lone coin, two grouped coins, no stacks, no rising bars". |
| el-06-11 | PASS | Pause and shutter cards with a teal chart behind them. The headline has teal keywords, everything is crisp and inside the safe area, and it is on brief. | — |
| el-06-13 | FAIL | "ALERT LEVEL (EXAMPLE)" is printed twice (duplicate label), and the bell sits slightly above the touch point. | Regenerate with "ALERT LEVEL (EXAMPLE) label once, at the left end of the line; bell exactly on the candle touch". |
| el-06-14 | FAIL | A horizontal band seam (about y 200-820) breaks the background. Content is otherwise on brief. | Regenerate with a continuous background. |
| el-06-15 | FAIL | The candles are red and white, so the key element is not teal-led and the "rest dimmed" treatment is lost. | Regenerate with "teal candles only, everything except the alert line and bell dimmed". |
| el-06-16 | FAIL | Panel seam (darker rectangle about x 210-1350). | Regenerate with a continuous background. |
| el-06-17 | PASS | Detailed teal chart with the labelled EXAMPLE line and the bell at the touch. Crisp, deep, and inside the safe area. | — |
| el-06-18 | PASS | Empty glass card on the left and the hero chart on the right, as briefed. Labels are correct and teal-led (a few red candles are acceptable). | — |
| el-06-20 | FAIL | Minimal: plain black background with no grid, bokeh or depth. The stray comma in "ALERT," is minor. | Regenerate with "faint grid, soft bokeh, teal glow depth" and the card text "IF HIT: PAUSE THE BOT". |
| el-06-21 | FAIL | Horizontal band seam (about y 165-860). | Regenerate with a continuous background. |
| el-06-22 | FAIL | Band seam, plus a background that resembles a real trading-app dashboard UI. | Regenerate with "no app UI, dim teal chart or grid only". |
| el-06-23 | FAIL | A smudged, garbled text fragment sits in the bottom-left of the rule card (about x 930, y 660). | Regenerate, or clean that area. Card text: "IF HIT: PAUSE THE BOT" only. |
| el-06-24 | FAIL | Horizontal band seam (about y 240-780). | Regenerate with a continuous background. |
| el-06-25 | FAIL | The mascot has smiling arc eyes and a smile mouth (only visor-bar eyes are allowed), and there is a band seam. | Regenerate with "G-badge robot with straight visor-bar eyes, no smile, no mouth" and a continuous background. |
| el-06-26 | FAIL | Mascot with smiling arc eyes and a smile mouth. The toggle reads as ON (knob right, teal fill). | Regenerate with visor-bar eyes and a toggle clearly in the OFF state (knob left, dim track, OFF label next to it). |
| el-06-27 | FAIL | Horizontal band seam (about y 220-815). The toggle state is ambiguous (glowing knob in the centre). | Regenerate with a continuous background and the toggle clearly set to OFF. |

## Totals
28 checked: 5 PASS (el-05-30, el-05-31, el-06-11, el-06-17, el-06-18), 23 FAIL.
Fail causes: panel/band seam 14, money/coin imagery 5, garbled/placeholder/extra text 6, mascot face 2, minimal 2, not teal-led 1, duplicate label 1 (several stills have more than one cause).
No exchange logos, no people, no profit claims beyond the el-05-40 "optimal performance" line, and no unlabelled prices were found.
