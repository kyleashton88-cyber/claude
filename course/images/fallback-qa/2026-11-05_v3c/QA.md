# QA — 2026-11-05_v3c (PR #6 @ bbb531b, course/images/FALLBACK_MANIFEST.json)
53 awaiting_qa stills downloaded. **33 are byte-identical to the v3b files**, so their v3b verdicts carry over (they were not re-rendered).
20 stills are new or changed and were reviewed this round: the redos el-05-41, 45, 47 and el-06-20 to 25 and 27, plus the new stills el-07-21 to 28, 30 and 31.

## Automated checks
- image_qa.py: 53 checked, 0 flagged. All 1536x1024, no duplicate md5s, and every prompt matches batch-web/v3.
- The top and bottom 80px bands hold content on el-07-21, el-07-22, el-07-26 and el-07-28 (the headline or the CHECK LOCAL RULES line crosses y=80 or y=944).

## Reviewed this round (20)
| Still | Result | Reason | Fix |
|---|---|---|---|
| el-05-41 | FAIL | Off-white torn-paper scrap is the main element; muted, not teal-led | Make it a dark frosted-glass "scrap" card with a teal rim |
| el-05-45 | FAIL | The "single" coin is a second ETH, which muddles the meaning; garbled micro-text on the BTC rim | Make the single coin a plain USDT; use clean coin rims |
| el-05-47 | FAIL | Minimal: left half empty; smeared orange strike under the headline; dull teal | Add a struck-out target card on the left; use a clean single strike line |
| el-06-20 | FAIL | Minimal/flat: small bell and card on bare navy | Make the card a glass hero with depth, glow and bokeh |
| el-06-21 | PASS | Glass card, glow, labels crisp | — |
| el-06-22 | FAIL | Flat navy, no glow or depth | Add teal glow, glass reflections and bokeh |
| el-06-23 | PASS | Wireframe bell and glass card; crisp | — |
| el-06-24 | PASS | Glass card, teal link, labels crisp | — |
| el-06-25 | FAIL | Flat matte grey, not teal; plain "G" on the chest, not the G-badge | Re-render in el-06-28's style |
| el-06-27 | FAIL | Flat matte grey, not teal; off-model mascot | Re-render in el-06-28's style |
| el-07-21 | FAIL | Headline crosses y=80; small headline; large empty left half | Move the headline below y=80, scale it up, centre the hero |
| el-07-22 | FAIL | Headline crosses y=80; ISOLATED / SEPARATE RISK printed twice | Move the headline down; label each vault once |
| el-07-23 | PASS | Two regions with fences; labels inside the safe area | — |
| el-07-24 | PASS | Glow link between the regions; crisp | — |
| el-07-25 | FAIL | Off-style desk props (mug, book, pen); dim scene | Remove the props; use a grid and bokeh background |
| el-07-26 | FAIL | Headline crosses y=80; CHECK LOCAL RULES on y=944 | Pull both inside the safe area |
| el-07-27 | PASS | Glass twin regions; teal glow | — |
| el-07-28 | FAIL | Headline crosses y=80; CHECK LOCAL RULES crosses y=944 | Pull both inside the safe area |
| el-07-30 | FAIL | Flat/minimal: 4 empty boxes; YOUR LIMIT floats away from the picked box | Add glass depth and glow; put the label under the ticked box |
| el-07-31 | PASS | Glass stack, ticked box, label matches | — |

Round: 7 PASS / 13 FAIL.

## Carried over unchanged from v3b (33, identical files)
PASS (7): el-06-28, el-06-31, el-06-32, el-06-34, el-06-38, el-06-39, el-07-14.
FAIL (26): el-05-18, 19, 20, 21, 22, 29, 40, 48; el-06-13, 14, 15, 16, 26, 29, 30, 33, 35, 36, 37, 53; el-07-15, 16, 17, 18, 19, 20. The fixes in v3b/QA.md still apply; none of these was re-rendered.

## Top fail causes this round
flat, minimal or not teal (8) · outside the safe area (4) · label or meaning mismatch / duplicate labels (4) · off-style props or paper (2) · garbled micro-text (1)

## Running total, el-05 to el-11 (out of 133; latest verdict per still)
Sources: QA-2026-11-05-a.md (all 18 later re-QA'd in v3a, so v3a supersedes), v3a/QA.md, v3b/QA.md, el-05-11 r2 ChatGPT pass, and v3c.
**20 / 133 passed:**
el-05-11, el-05-30, el-05-31;
el-06-11, el-06-17, el-06-18, el-06-21, el-06-23, el-06-24, el-06-28, el-06-31, el-06-32, el-06-34, el-06-38, el-06-39;
el-07-14, el-07-23, el-07-24, el-07-27, el-07-31.
