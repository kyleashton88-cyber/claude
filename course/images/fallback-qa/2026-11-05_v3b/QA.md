# QA — 2026-11-05_v3b (33 awaiting_qa stills, PR #6, branch cursor/course-video-qa-fix-7f90)
Rubric: /workspace/course-images/STYLE_V3_GBB.md. Visual review on safe-area overlays (red lines y=80 / y=944).

## Automated checks
- image_qa.py: 33 checked, 0 flagged. All 1536x1024, unique md5. Every manifest prompt matches its batch prompt.
- Top/bottom 80px bands: the 20 new stills are flat background. Redos el-05-29 and el-06-14 have content in the bands (see below).

| Still | Result | Reason | Fix |
|---|---|---|---|
| el-05-18 | FAIL | Steep rising candlestick uptrend behind the hero reads as gains; chart runs into the top band | Swap for a neutral, sideways, dim chart kept inside the safe area |
| el-05-19 | FAIL | The separate coin is a second ETH, so the contrast is muddled; faint vertical seam at mid-frame; garbled micro-text on the gold coin rim | Use one distinct teal/neutral coin, a single seamless background, and a plain coin rim |
| el-05-20 | FAIL | Flat navy look, no glow or depth, not teal-led | Re-render on a dark teal-glow scene with a glass card rim light |
| el-05-21 | FAIL | Rising arrow on the NOTE card (gain imagery) | Replace with a flat note/pencil icon |
| el-05-22 | FAIL | Minimal: one dashed box on an empty grid, no hero | Add a glass cap card hero holding CAP = 10% (EXAMPLE) |
| el-05-29 | FAIL | Branding header (GRID BOT BUILDER / VOLUME 1) crosses y=80, and BY STEWART CROWN sits in the bottom band; extra text | Remove header and footer; keep only the headline and 3 labels inside the safe area |
| el-05-40 | FAIL | Off-white torn-paper block clashes with the style and reads unfinished | Replace with a dark glass "clean page" card |
| el-05-48 | FAIL | No glass frame around the group; garbled micro-text on coin rims | Put the grouped coins in a glass card and use plain coin faces |
| el-06-13 | FAIL | Flat: bare chart, no glass or depth | Put the chart on a glass card with rim light and a depth glow |
| el-06-14 | FAIL | Headline top sits in the top 80px band; flat; rising chart | Move the headline down, use a glass card, use a sideways chart |
| el-06-15 | FAIL | Flat; steep breakout uptrend reads as gains | Use a glass card and a neutral range chart that touches the line |
| el-06-16 | FAIL | Flat, uptrend, and price never touches the line (bell above, dot below) | Put the touch exactly on the line with the bell at the touch; add a glass card |
| el-06-26 | FAIL | Flat matte grey, not teal; robot is not the G-badge mascot | Re-render to match el-06-28 (glass, teal, G-badge robot) |
| el-06-28 | PASS | Wireframe switch, G-badge visor mascot, labels crisp | — |
| el-06-29 | FAIL | Toggle reads ON (teal fill, knob right) against the OFF message | Knob left, track unlit/grey |
| el-06-30 | FAIL | Darker rectangle seam behind the hero; mascot eyes read as smiling arcs; toggle reads ON | Use a seamless background, straight visor eyes, and the toggle set to OFF |
| el-06-31 | PASS | Clean 3-step glass cards; correct labels | — |
| el-06-32 | PASS | Correct, with glow trail; crisp | — |
| el-06-33 | FAIL | Extra sub-labels (SYSTEM HALT / SIGNAL TRIGGER / EXECUTION PLAN); bell clapper reads as a smile | Remove sub-labels; use a plain bell clapper |
| el-06-34 | PASS | Struck middle line plus corrected teal line; correct labels | — |
| el-06-35 | FAIL | Extra GRID BOT ELITE logo top right; labels float off the card, away from their lines | Remove logo; anchor OLD RULE and CORRECTED to their lines |
| el-06-36 | FAIL | OLD RULE label sits on the top line, not the struck line | Re-anchor OLD RULE to the red struck line |
| el-06-37 | FAIL | Extra header text (GRID BOT ELITE COURSE / VOLUME 1 / LESSON 01) | Remove the header line |
| el-06-38 | PASS | Correct layout; labels crisp (grain is a stylistic sparkle, not artifacting) | — |
| el-06-39 | PASS | Two-panel as prompted (empty left card is intended) | — |
| el-06-53 | FAIL | Clear darker inner rectangle seam around the hero; rising chart behind | Use a full-bleed seamless background and a neutral or no chart |
| el-07-14 | PASS | Falling chart to LIQUIDATION LEVEL (EXAMPLE); warning icon; POSITION CLOSED | — |
| el-07-15 | FAIL | Sentence paragraphs (garbled; "profits"), fake app-UI panels, header/footer branding | Strip to the hero chart and the 2 labels only |
| el-07-16 | FAIL | $ axis values, garbled text (CAGEED, $80UE), extra grid labels | Remove axes and grid labels; keep LIQUIDATION LEVEL (EXAMPLE) and POSITION CLOSED |
| el-07-17 | FAIL | Garbled / $ text on the vault back screens ($635M) | Make the vault interiors plain glass, with no screens |
| el-07-18 | FAIL | No wall icon between the vaults (they touch, with no gap); right coins are G-badges, not cyan USDT | Add a gap and a wall icon; use cyan USDT coins on the right |
| el-07-19 | FAIL | Extra branding line and BY STEWART CROWN; duplicate SEPARATE RISK under ISOLATED plus a CROSS label | Remove extra text; labels ISOLATED and SEPARATE RISK once each |
| el-07-20 | FAIL | Coins carry $-like glyphs and number more than 3 per vault; the centre icon is a shield, not a wall | 3 plain USDT coins per vault (teal / cyan); brick-wall icon |

## Totals
33 checked — 7 PASS, 26 FAIL.
Redos: 0/13 pass. New: 7/20 pass.
Main fail causes: flat or not teal (7), extra, sentence or garbled text (9), rising or gain imagery (6), seams (3), $ glyphs (3), meaning mismatch (5), safe area (2).
