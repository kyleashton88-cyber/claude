# OCO re-render image brief (DRAFT, internal, Creative Studio for Stewart)
Scope: the 90 flagged OCO videos (Module 4 onward, each under 10:00), listed in RERENDER_FLAGS.md, with durations in OCO_VIDEO_LIST.md. Target: curriculum standard, a 15–20 min YouTube-tutorial format with a branded intro and outro and music. **Do NOT start re-renders until Stewart says go.**
Prompt file: IMAGE_REQUESTS.json from render agent bc-e6e311bd (PR #6) is **not in /workspace yet** (checked with rg, 5 Nov 09:18 WITA). SERIES_FLOW.md is **also pending** (not found). This brief has not been checked against either one.

## 1. Palette: CONFLICT, Stewart to decide
- Current rule (RERENDER_FLAGS, Stewart voice note, 5 Nov): **navy/cyan**. Background navy #0A1630, primary cyan #00D4FF, text white, muted slate #8CA0C0.
- Earlier rule: the course uses **OCO mint/teal**. (No hex values for it were found in the workspace.)
- **Resolved 5 Nov (GBB v3 standard):** OCO and Blueprint use the navy/cyan-blue variant as in the Grid Bot Builder refs; teal is Elite-only. See /workspace/course-images/STYLE_V3_GBB.md. Prompts must state hex values. Don't mix the two palettes inside one video.

## 2. One real illustration per beat
- Every script beat gets its own illustration that shows that beat's specific concept. No reused frames, no generic "crypto background", no stock-style filler, and no repeated image with only the text changed.
- Each prompt names the concept, the diagram elements and the composition, and leaves empty space for code-overlaid text.
- Generate a new image for each beat. Every beat gets a unique image ID (`m{mod}-l{lesson}-b{beat}`).

## 3. Tooling and look (GBB v3, 5 Nov)
- **ChatGPT image only** (ChatGPT web or gpt-image). Attach anchors: /workspace/course-images/style-ref-gbb-v1/01M6MSHVNHDS25DF52A243CTZG.png and /workspace/course-images/style-ref-gbb-v1/01M6MSJZM9PRAVHGK3607P817A.png.
- Premium near-black navy with neon cyan glow and depth, glass cards with glowing borders, detailed candlestick charts with labelled dashed BUY/SELL lines, circled line icons, numbered steps, formula boxes, 3D BTC/ETH/USDT coins, G-badge robot (visor-bar eyes only). Flat/minimal = fail.
- **Text allowed now:** one bold condensed all-caps headline with one cyan keyword, plus a few short crisp labels. No paragraphs.
- **No people or faces** (mascot only; no other face-like shapes).
- Generate 1536x1024; masters are 16:9 1920x1080, so all text and key content must sit inside the centre 1536x864 safe area (~80px clear top and bottom).

## 4. Compliance (education only)
- No profit, return, win-rate, income, "passive income" or prediction claims, and no hockey-stick or upward-arrow money imagery. Coins are allowed as concept objects.
- Every number or level is labelled **(Example)**.
- No exchange or protocol-front-end names, logos, or UI lookalikes. Show wallets, dashboards and charts as generic.
- Never write "award-winning". Footer on level frames: "Education only. Not financial advice."

## 5. Prompt template
```
Match the attached reference images' style exactly (navy/cyan). Landscape 1536x1024; all text and key content inside the centre 1536x864 safe area, top and bottom ~80px background only.
STYLE: <Blueprint/OCO cyan block from STYLE_V3_GBB.md>
NEGATIVE: <negative block from STYLE_V3_GBB.md>
SHOT: Headline: <ALL CAPS, one "KEYWORD" in cyan>. Hero visual: <beat concept, elements, explicit positions>. Labels: <2-4 short labels; any price/level ends with (EXAMPLE)>. Hero visual with a few labels, not a full infographic page.
```
Lesson from X P15 (5 Nov): spell out the spatial relationships ("centred", "beside, with a gap", "not touching the edge"), because the model will otherwise place elements loosely.

## 6. Series continuity (all 90 must play as one series)
To be reconciled with SERIES_FLOW.md once it lands.
- **Recurring motifs:** the same visual vocabulary for recurring concepts in every lesson, e.g. wallet = rounded cyan card, pool = two-tone vessel, range = cyan rectangle, risk = slate hatched zone. Keep one motif sheet and reuse its wording in every prompt.
- **Titles and lower thirds:** a single template, overlaid in code: title in Bold white with a cyan underline, lower third on a navy bar with a cyan left rule, same font, sizes and position, and the "Module X · Lesson Y" label in the same spot.
- **Palette:** the hex values from §1 locked across all lessons, with no per-lesson drift.
- **Illustration style:** GBB v3 premium glass/neon look, same glow strength, corner radius and detail level; 3D coins and mascot allowed; no photoreal people.
- **Pacing per beat:** about 20–45 s per illustration, a new image at each beat change, and no still held longer than about 60 s. Lesson length 15–20 min means roughly 25–45 beats.
- **Intro and outro:** the same branded intro (sting, music bed, duration) and the same outro (recap card, next-lesson card, disclaimer) on every video. Module intros use the same template with only the module title changed.


## No degradation (Stewart, 5 Nov 2026)
Image quality must not degrade at any stage: no compression artifacts, no loss of detail, no colour shift, no softening of labels or text; full resolution preserved from generation through to the final 1080p video frame.
