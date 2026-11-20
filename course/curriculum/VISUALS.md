# GridBot Blueprint: visuals production list (BP-01 to BP-11)

Version 1 · 16 Nov 2026 (WITA)

This list goes with `CURRICULUM.md`. Under Stewart's scope rule, **existing passed stills are KEEP**, and the only new visuals listed are the ones the added sections need.

## How to read this

- **Types**
  - **STILL**: an illustration or diagram made by Cursor image agent **bc-6781931a**. Creative Studio scores every still before use.
  - **MOTION**: an animated chart or diagram coded in the video pipeline (`course/blueprint-rebuild/studio.py`, following the `paint_leave` pattern).
  - **SCREEN**: a demo-screen capture through `capture_demo.js`, then `skills/video-production/screen-demo-kit` (blur, then `cli.py qa` must PASS). Counted as MOTION.
  - **CARD**: a code-drawn text or number card in `studio.py`. Counted as MOTION. Use it for sums, rules, titles, disclaimer and outro.
- **KEEP**: the still is on Creative Studio's v2 PASS list (14 Nov), in `blueprint-image-qa/bp01-03-v2/` and `bp04-11/` on `cursor/blueprint-beginner-images` at 116f86b, held locally.
  - Before a render, `image_gate.py` must confirm the blob at the path equals the scored blob.
  - KEEP stills are still subject to the colour decision (CURRICULUM §5.4).
- **RETIRE**: remove from the lesson.
- **REMAKE**: a known FAIL, or the text must change.

### [BRAND-STD]: applies to every visual below

- **Colours.** Navy background (#050A18 to #0A1630), cyan accent (#00D4FF), white text.
  - No teal (Elite style #14E0C8 must not appear).
  - Mint, amber and blue are not used in new visuals until Stewart decides.
  - Interim coding: buys are solid cyan, sells are outlined white, the stop is a white dashed line with a warning-triangle icon in cyan, and the "filled" state is a bright cyan glow.
- **Titles fully in frame,** with no slide-off animation.
- **All text inside the 5% safe margin:**
  - frames (1920×1080): 96 px left/right, 54 px top/bottom
  - stills (1536×1024): 77 px left/right, 51 px top/bottom, inside the STYLE_V3 centre band
- **Branding:** GridBot Builder wordmark and visor mascot only. No other brand, no exchange names or logos, no people.
- **Figures:** every one carries an **EXAMPLE** pill.
- **Footer:** "Education only. Not financial advice."
- **Text size:** labels at least 28 px at 1080p. Arrow tips must touch their targets (the most common past FAIL).
- **Charts:** line charts use **daily closes only**. Highs, lows and wicks appear only on candle cards.

### QA line (every visual)

`QA: [ ] accurate  [ ] on brand  [ ] unique  [ ] a first-timer gets the point in 3 s`

---

## BP-01 · Introduction (target 12:30)

**KEEP**
- Lesson stills, PASS: 001, 002, 003, 004, 005, 006, 007 (re-scored PASS 15 Nov), 008, 009, 010, 011, 012 (text change, see REMAKE), 014, 016, 017, 018.
- Code-drawn, PASS: range-2023 hook, a-ladder, the-range, the-levels, walk-the-summer, breakout-2023 the-stop, title-card, end-card, thumbnail.
- Motion: `paint_leave` (climb to all cash, fall to all coin), candle card (19 Jul 2023), course map (`paint_course_map`).
- Shared: wordmark, mascot, `analogy-ladder.png`, `analogy-list.png`.

**RETIRE:** `analogy-fence.png`, the "The fence" chart (range-2023 the-fence), and 015 ("paper or demo is a fence around practice"). The fence analogy is banned.

**REMAKE:**
- 012: headline becomes "NO PROMISE OF RESULTS".
- Course map: name every lesson through to "Scaling up" and "Your complete plan".

**NEW**

**BP01-V01** · STILL · Teach 1 "Cash and coin" · 1:20–2:50
- **Shows:** two glass cards joined by two arrows. The left card is a dollar note icon labelled "Cash". The right card is a plain coin outline (no logo) labelled "Coin". The top arrow, cash to coin, is labelled "Buy order". The bottom arrow, coin to cash, is labelled "Sell order". A small lock on the sell arrow reads "needs coin first".
- **Teaches:** a buy swaps cash for coin and a sell swaps coin for cash, so selling needs coin.
- **On-screen text:** headline "BUY = CASH → COIN"; labels "Cash", "Coin", "Buy order", "Sell order", "Needs coin first".
- **Data:** none.
- **Brand:** [BRAND-STD]. Unique to BP-01.
- **Reuse:** none.
- QA: [ ] accurate [ ] on brand [ ] unique [ ] 3 s

**BP01-V02** · STILL · Teach 1 "What an exchange is" · 1:20–2:50
- **Shows:** a generic phone or laptop outline with a two-sided swap screen (A$ and a coin outline), no logo. The mascot points at it.
- **Teaches:** an exchange is the app where you swap dollars for crypto and back.
- **On-screen text:** "EXCHANGE = WHERE YOU SWAP"; labels "Australian dollars", "Crypto".
- **Data:** none.
- **Brand:** [BRAND-STD]. Must not resemble any real exchange UI.
- **Reuse:** none.
- QA: [ ] accurate [ ] on brand [ ] unique [ ] 3 s

**BP01-V03** · MOTION · Teach 2 "Bot vs you" · 3:40–4:20
- **Shows:** a split card. Left, "YOU": choose band, choose gaps, choose money, write stop, act on stop (cyan ticks appear one by one). Right, "THE BOT": place orders, after a fill place the opposite order one rung away. A small ladder animates one fill and the refill.
- **Teaches:** what is automatic and what is your job.
- **On-screen text:** "YOU" / "THE BOT" plus the five and two rows above.
- **Data:** none.
- **Brand:** [BRAND-STD]. Code-drawn in `studio.py`.
- **Reuse:** extends the a-ladder chart style.
- QA: [ ] accurate [ ] on brand [ ] unique [ ] 3 s

**BP01-V04** · MOTION · Teach 3 "Why a grid earns" · 4:20–5:50
- **Shows:** a ladder of seven lines on the summer chart. Price dips to 27,630: the buy line glows (filled), and a "C" tag appears. Price bounces up to 28,531: the sell line glows, and a "$" tag appears. A bracket labelled "one completed pair" joins them. Then a faster loop shows three more bounces, with a pair counter incrementing. Then price drops out of the bottom, the counter stops, and "C C C" piles up (the catch).
- **Teaches:** each bounce inside the band completes a small buy-then-sell pair; it only works while price keeps bouncing.
- **On-screen text:** "ONE BOUNCE = ONE PAIR"; "Buy 27,630", "Sell 28,531", "Pairs: 1, 2, 3, 4", "Leaves the band: pairs stop".
- **Data:** EXAMPLE levels 27,630 / 28,531 from LEVELS. The loop is illustrative and labelled "Illustration, not the real order of fills".
- **Brand:** [BRAND-STD]. Market-stall analogy in the voice only. **No "BUY LOW SELL HIGH" headline** (that failed QA as a slogan).
- **Reuse:** `paint_leave` key ($ / C / glow).
- QA: [ ] accurate [ ] on brand [ ] unique [ ] 3 s

**BP01-V05** · CARD · Worked example "One pair, after fees" · 5:50–7:00
- **Shows:** a sum card.
  - Buy 0.01 BTC at 27,630 = US$276.30
  - Sell 0.01 BTC at 28,531 = US$285.31
  - Gross US$9.01
  - Fees 0.1% + 0.1% = US$0.56
  - **Net ≈ US$8.45**
  - Footnote: "Only if price comes back up. Not a forecast."
- **Teaches:** fees come off every pair, and the result depends on price returning.
- **On-screen text:** as above; title "ONE PAIR, AFTER FEES".
- **Data:** EXAMPLE, BTC/USD public daily data; fee 0.1% is an EXAMPLE rate.
- **Brand:** [BRAND-STD]
- **Reuse:** none.
- QA: [ ] accurate [ ] on brand [ ] unique [ ] 3 s

**BP01-V06** · MOTION · Teach "The stop, plainly" · 8:30–9:50
- **Shows:** the breakout-2023 close line. The 23 Oct close crosses above the top line and is tagged "Close 1 outside". The 24 Oct close is still above, tagged "Close 2 still outside → stop". Then a three-step strip appears: "1 · Stop the bot (cancels waiting orders)", "2 · Follow your written rule: keep coin or swap to cash", "3 · Who: bot's stop setting, or you by hand". A small "11am AEDT = daily close" chip.
- **Teaches:** when the stop triggers, what you do, and who does it.
- **On-screen text:** as above.
- **Data:** EXAMPLE, 23 Oct 2023 close 33,086 and 24 Oct close 33,902, both above the 30,331 top line. Values sit on the chart, not in the voice.
- **Brand:** [BRAND-STD]. White dashed stop, no amber (pending decision).
- **Reuse:** extends the PASS chart breakout-2023 the-stop.
- QA: [ ] accurate [ ] on brand [ ] unique [ ] 3 s

**BP01-V07** · STILL · What you do next "L-plates" · 10:30–11:30 (replaces 015)
- **Shows:** a learner-driver "L" plate (Australian yellow-and-black recoloured to navy and cyan, an outline-only "L") on a glass card, next to a small paper notebook with a ladder sketch stamped EXAMPLE.
- **Teaches:** practise on paper or demo first, like L-plates.
- **On-screen text:** "PRACTISE FIRST"; labels "Paper or demo", "No real money".
- **Data:** none.
- **Brand:** [BRAND-STD]. The plate must not be real yellow (palette).
- **Reuse:** none.
- QA: [ ] accurate [ ] on brand [ ] unique [ ] 3 s

---

## BP-02 · What you are going to need (target 12:00)

**KEEP**
- Lesson stills, PASS: 001, 002, 003, 004, 005, 006, 007, 008, 009, 010, 011, 013, 015, 016–018 (practice; use only if timing needs them), 019, 020.
- Code-drawn, PASS: hook, seven-lines, the-three-words, no-secrets, copy-the-path, title-card, end-card, thumbnail.

**REMAKE:**
- 021 outro (known FAIL, arrow 17 px short): becomes a code-drawn end card.
- 012 ("form only copies it", flagged cryptic) and 014 ("Empty pair", flagged confusing): RETIRE them and replace with BP02-V05.

**NEW**

**BP02-V01** · SCREEN · Teach 2 "Exchange account in Australia" · 3:00–4:30
- **Shows:** a demo or fake exchange sign-up flow, four steps highlighted in turn: ID check, AUSTRAC registration check (generic "Registered with AUSTRAC" text on an info card, not a real site), AUD deposit, 2FA set-up. All names, balances and codes blurred by the screen-demo kit.
- **Teaches:** the account steps, and safety before money.
- **On-screen text:** step chips "1 ID check", "2 Check AUSTRAC registration", "3 Deposit A$", "4 Turn on 2FA".
- **Data:** none.
- **Brand:** [BRAND-STD] chips over a blurred screen. `screen-demo-kit qa` PASS required. No exchange name or logo visible.
- **Reuse:** none.
- QA: [ ] accurate [ ] on brand [ ] unique [ ] 3 s

**BP02-V02** · STILL · Teach 3 "Reading a pair" · 4:30–5:30
- **Shows:** a large "BTC / AUD" label split into two glass tiles. The left tile is labelled "Base: what you buy"; the right is labelled "Quote: what you pay with". A smaller "BTC / USDT" row below, labelled "USDT = a stablecoin, near US$1".
- **Teaches:** base, quote and stablecoin.
- **On-screen text:** as above.
- **Data:** EXAMPLE pair names only.
- **Brand:** [BRAND-STD]
- **Reuse:** extends the 006 idea (keep 006 for the definition beat).
- QA: [ ] accurate [ ] on brand [ ] unique [ ] 3 s

**BP02-V03** · CARD · Teach 4 "Fees: the round trip" · 5:30–6:45
- **Shows:** maker vs taker defined in two rows. Then the sum: A$100 buy × 0.1% = A$0.10; A$100 sell × 0.1% ≈ A$0.10; **round trip ≈ A$0.20 (0.2%)**. Callout: "Any gap under 0.2% loses before price moves → Lesson 5".
- **Teaches:** every pair pays two fees.
- **On-screen text:** as above.
- **Data:** EXAMPLE fee 0.1%, order A$100.
- **Brand:** [BRAND-STD]
- **Reuse:** none.
- QA: [ ] accurate [ ] on brand [ ] unique [ ] 3 s

**BP02-V04** · STILL · Teach 5 "Your trading journal" · 6:45–8:00
- **Shows:** a clean journal page on a glass card with column headers: Date · Pair · Band · Gaps · Money in bot · Stop rule · Fills · Pairs · Fees · Result · Rules followed? One example row is filled and stamped EXAMPLE.
- **Teaches:** what you record. The journal is used in Lessons 8 and 10.
- **On-screen text:** headline "YOUR JOURNAL" plus the column names.
- **Data:** EXAMPLE row (BTC/AUD, band 24,930–30,331, 6 gaps).
- **Brand:** [BRAND-STD]. Unique; it becomes the course's journal reference image.
- **Reuse:** none.
- QA: [ ] accurate [ ] on brand [ ] unique [ ] 3 s

**BP02-V05** · CARD · Replaces 012/014 "Page first, screen later" · 9:45–10:30
- **Shows:** a left-to-right arrow from "Your page (written first)" to "The screen (copy the page)". Pair row filled with "BTC/AUD, EXAMPLE".
- **Teaches:** the page is the plan and the screen only copies it.
- **On-screen text:** as above.
- **Data:** EXAMPLE.
- **Brand:** [BRAND-STD]
- **Reuse:** checklist analogy style (`analogy-list.png`).
- QA: [ ] accurate [ ] on brand [ ] unique [ ] 3 s

---

## BP-03 · What is a grid bot (target 12:00)

**KEEP**
- Lesson stills, PASS: 001–019, except for these changes:
  - 011: REPLACE the chain and circle icons if still present.
  - 014: REPLACE the cryptic icon string ("One-breath definition").
  - 009: REPLACE the looping arrows / small text.
  - Each needs a re-score after the fix.
- Code-drawn, PASS: hook, limit-orders-wait, buys-and-sells, where-the-path-stood, title-card, end-card, thumbnail.

**NEW**

**BP03-V01** · MOTION · Teach 2 "The grid cycle" · 3:00–5:00
- **Shows:** a seven-line ladder (summer levels). Pass 1, slow:
  - price steps down through 27,630: the buy glows and a new **sell** appears at 28,531, with the label "bot places the opposite order one rung up"
  - price steps up through 28,531: the sell glows and a new **buy** appears at 27,630
  - pair counter = 1
  Pass 2 runs with the counts. Pass 3 replays on the real summer close path.
- **Teaches:** fill, then the opposite order is placed. This is the whole job of the bot.
- **On-screen text:** "BUY FILLS → SELL PLACED ABOVE", "SELL FILLS → BUY PLACED BELOW", "Completed pairs: n".
- **Data:** EXAMPLE, LEVELS; summer 2023 closes.
- **Brand:** [BRAND-STD]
- **Reuse:** extends the limit-orders-wait chart.
- QA: [ ] accurate [ ] on brand [ ] unique [ ] 3 s

**BP03-V02** · SCREEN · Teach 3 "Settings a bot asks for" · 5:00–6:30
- **Shows:** a generic grid-bot settings form (demo or fake) with fields highlighted in turn: Upper price, Lower price, Number of grids, Amount, then a computed "Per order". Spacing mode shown with the chip "Arithmetic / Geometric: Lesson 5".
- **Teaches:** the settings are the plan page in form fields.
- **On-screen text:** field chips as above.
- **Data:** EXAMPLE values: Upper 30,331, Lower 24,930, Grids 6, Amount A$600, Per order A$100.
- **Brand:** [BRAND-STD]. Screen-demo kit PASS. No logo.
- **Reuse:** none.
- QA: [ ] accurate [ ] on brand [ ] unique [ ] 3 s

**BP03-V03** · CARD · Teach 3 "Order size" · 5:45–6:30
- **Shows:** "A$600 ÷ 6 orders = A$100 per order".
- **Teaches:** how the amount is split across orders.
- **On-screen text:** as above.
- **Data:** EXAMPLE.
- **Brand:** [BRAND-STD]
- **Reuse:** none.
- QA: [ ] accurate [ ] on brand [ ] unique [ ] 3 s

**BP03-V04** · MOTION · Worked example "Inventory moves" · 6:30–7:45
- **Shows:** a two-bar meter (Coin / Cash) beside a short path: two steps down (coin bar grows twice), one step up (cash bar grows once). An end label reads "One parcel still waiting to sell".
- **Teaches:** inventory shifts as price moves.
- **On-screen text:** "COIN" / "CASH", "after each fill".
- **Data:** EXAMPLE, A$100 parcels.
- **Brand:** [BRAND-STD]. The bars are cyan and white, not mint.
- **Reuse:** none.
- QA: [ ] accurate [ ] on brand [ ] unique [ ] 3 s

**BP03-V05** · STILL · Common mistake "A fill is a swap, not a win" · 8:45–9:45
- **Shows:** one glass card with a cash icon ⇄ coin icon swap arrow. The label "A fill swaps cash and coin" sits beside a small question mark over a future price path, labelled "Ahead or behind depends on where price goes next".
- **Teaches:** fills are not profits until a pair completes and price cooperates.
- **On-screen text:** "A FILL IS A SWAP" plus the labels above.
- **Data:** none.
- **Brand:** [BRAND-STD]
- **Reuse:** none.
- QA: [ ] accurate [ ] on brand [ ] unique [ ] 3 s

---

## BP-04 · Market regimes (target 12:00)

**KEEP**
- Lesson stills, PASS: 001, 004, 005, 006, 007, 008, 009, 010, 011, 012, 013, 014, 015, 019.
- **Code-drawn NEEDED** (not generated): 002 disclaimer card, 003 title card, 020 end card.

**NEW**

**BP04-V01** · MOTION · Teach 2 "How to sort" · 2:50–4:20
- **Shows:** a 90-day close chart drawn left to right. Touches at the top and bottom get cyan dots and a counter. A higher-highs test draws peak-to-peak and trough-to-trough lines. The result chip reads "RANGE: 4 touches each side, no new highs".
- **Teaches:** a repeatable sort with one reason.
- **On-screen text:** "COUNT TOUCHES", "HIGHER HIGHS?", "Label + 1 reason".
- **Data:** EXAMPLE, range_2023 closes.
- **Brand:** [BRAND-STD]
- **Reuse:** none.
- QA: [ ] accurate [ ] on brand [ ] unique [ ] 3 s

**BP04-V02** · MOTION · Teach 3 "What the grid does in each regime" · 4:20–6:00
- **Shows:** a three-panel strip, each with the same ladder:
  - Range: pairs counter climbs
  - Trend up: price exits the top, "all cash" $ tags
  - Break down: price exits the bottom, "all coin" C tags, then the stop line
- **Teaches:** the outcome of a grid per regime.
- **On-screen text:** "RANGE → pairs", "TREND → left behind", "BREAK → stop".
- **Data:** EXAMPLE, illustrative paths labelled "Illustration".
- **Brand:** [BRAND-STD]
- **Reuse:** `paint_leave` key.
- QA: [ ] accurate [ ] on brand [ ] unique [ ] 3 s

**BP04-V03** · CARD · Teach 4 "Volatility vs gap" · 6:00–7:00
- **Shows:** a histogram of daily close-to-close moves in summer 2023, with a cyan line at "one gap ≈ 900". Label: "83 of 89 days moved less than one gap".
- **Teaches:** compare the usual daily move to your gap size.
- **On-screen text:** as above.
- **Data:** EXAMPLE, computed from range_2023 closes (83/89 < 900; the verifier must re-check).
- **Brand:** [BRAND-STD]
- **Reuse:** none.
- QA: [ ] accurate [ ] on brand [ ] unique [ ] 3 s

**BP04-V04** · MOTION · Worked sort "Three real windows" · 7:00–8:15
- **Shows:** three close-only charts in sequence, each with a label chip:
  - Summer 2023: RANGE
  - Oct 2023 to Mar 2024: TREND (about 28k to about 71k on the axis)
  - Feb to Mar 2020: BREAK (11 Mar close 7,911 to 12 Mar close 4,971, ≈ −37%)
- **Teaches:** sorting real history.
- **On-screen text:** window dates plus labels.
- **Data:** EXAMPLE, closes from `btc-usd-windows.json`. No lows on these line charts.
- **Brand:** [BRAND-STD]
- **Reuse:** chart style from the PASS code-drawn charts.
- QA: [ ] accurate [ ] on brand [ ] unique [ ] 3 s

**BP04-V05** · STILL · "Regimes change" · 9:00–9:45
- **Shows:** a weekly calendar strip with a cyan "re-sort" tick each week. Week 5's tick turns from "RANGE" to "TREND", with an arrow to "Stop or re-plan".
- **Teaches:** re-sort on a schedule.
- **On-screen text:** "RE-SORT WEEKLY".
- **Data:** none.
- **Brand:** [BRAND-STD]
- **Reuse:** none.
- QA: [ ] accurate [ ] on brand [ ] unique [ ] 3 s

---

## BP-05 · Choosing grid spacing and range (target 12:00)

**KEEP**
- Lesson stills, PASS: 001, 004, 005, 007, 008, 009, 010, 011 (pair with a candle card, see V04), 012, 013, 014, 015, 018.
- 006: KEEP the image, but **fix the maths** in the narration and caption per 51d8fcd.
- **REMAKE:** 019 outro (known FAIL): becomes a code-drawn end card.
- **Code-drawn NEEDED:** 002, 003.

**NEW**

**BP05-V01** · MOTION · Teach 2 "Arithmetic vs geometric" · 2:40–3:40
- **Shows:** two ladders side by side on a A$100–A$200 band.
  - Left (arithmetic): 100/125/150/175/200, labelled "same dollars".
  - Right (geometric): 100/118.9/141.4/168.2/200, labelled "same percent".
  - Gap labels animate in.
- **Teaches:** two ways to space lines.
- **On-screen text:** "ARITHMETIC = SAME $", "GEOMETRIC = SAME %".
- **Data:** EXAMPLE.
- **Brand:** [BRAND-STD]
- **Reuse:** a-ladder style.
- QA: [ ] accurate [ ] on brand [ ] unique [ ] 3 s

**BP05-V02** · CARD · Teach 3 "Net per pair: pass and fail" · 3:40–5:00
- **Shows:** two rows.
  - "0.5% gap on A$100: +A$0.50 − A$0.20 fees = **+A$0.30** ✓ passes"
  - "0.15% gap: +A$0.15 − A$0.20 = **−A$0.05** ✗ fails"
- **Teaches:** the cost check.
- **On-screen text:** as above.
- **Data:** EXAMPLE fee 0.1% per side.
- **Brand:** [BRAND-STD]. The ✗ is white, not amber.
- **Reuse:** links to BP02-V03.
- QA: [ ] accurate [ ] on brand [ ] unique [ ] 3 s

**BP05-V03** · MOTION · Teach 4 "More grids vs fewer grids" · 5:00–6:15
- **Shows:** the same price path over two ladders. Ladder A (many lines) shows frequent small glows and "many small pairs". Ladder B (few lines) shows rare large glows and "few bigger pairs". Both carry the fee chip.
- **Teaches:** the trade-off.
- **On-screen text:** as above.
- **Data:** EXAMPLE, illustrative path.
- **Brand:** [BRAND-STD]
- **Reuse:** none.
- QA: [ ] accurate [ ] on brand [ ] unique [ ] 3 s

**BP05-V04** · CARD · Teach 5 "Room for real highs and lows" · 6:15–7:15
- **Shows:** a candle strip from the summer window with the band drawn on it. Wicks outside a too-tight band are tagged "real low", "real high". The band then widens to contain them.
- **Teaches:** the band must hold the real highs and lows, not only the closes.
- **On-screen text:** "LEAVE ROOM FOR THE WICKS".
- **Data:** EXAMPLE, range_2023 high/low data (24,930 / 30,331).
- **Brand:** [BRAND-STD]. Candle chart only (fixes the high/low-over-line failures).
- **Reuse:** candle-card style from BP-01.
- QA: [ ] accurate [ ] on brand [ ] unique [ ] 3 s

**BP05-V05** · CARD · "Order size and minimum" · 7:15–8:00
- **Shows:** "A$2,000 ÷ 20 orders = A$100 per order", then "Exchange minimum: A$10 ✓".
- **Teaches:** each order must meet the minimum.
- **On-screen text:** as above.
- **Data:** EXAMPLE.
- **Brand:** [BRAND-STD]
- **Reuse:** none.
- QA: [ ] accurate [ ] on brand [ ] unique [ ] 3 s

---

## BP-06 · Entry and exit rules (target 12:30)

**KEEP**
- Lesson stills, PASS: 001, 004, 005, 006, 007, 008, 009, 010, 011, 012, 013 (text change: "Sizing is Lesson 10"), 014, 015, 019.
- **REMAKE:** 016, 018, 020 (known FAILs, arrow tips). 020 becomes a code-drawn end card.
- **Code-drawn NEEDED:** 002, 003.

**NEW**

**BP06-V01** · MOTION · Teach 2 "Trigger plus confirmation" · 2:40–4:00
- **Shows:** a reuse of the BP01-V06 chart with only the trigger part: "Close 1 outside" on 23 Oct, then "Close 2 still outside" on 24 Oct, with a "= confirmed" chip.
- **Teaches:** the finish sentence needs a confirmation.
- **On-screen text:** as above.
- **Data:** EXAMPLE, 23 and 24 Oct 2023 closes.
- **Brand:** [BRAND-STD]
- **Reuse:** BP01-V06 code path; recolour or crop so the frame is not identical (uniqueness).
- QA: [ ] accurate [ ] on brand [ ] unique [ ] 3 s

**BP06-V02** · STILL · Teach 3 "Three stop actions" · 4:00–5:30
- **Shows:** three glass cards in a row:
  - "Stop + keep coin"
  - "Stop + swap to cash"
  - "Bot's automatic stop setting"
  Each carries a tiny icon and a "who" tag: You / You / Bot.
- **Teaches:** the choices, and who acts.
- **On-screen text:** as above, plus the headline "WHAT YOU DO AT THE STOP".
- **Data:** none.
- **Brand:** [BRAND-STD]
- **Reuse:** none.
- QA: [ ] accurate [ ] on brand [ ] unique [ ] 3 s

**BP06-V03** · MOTION · Teach 4 "Up break vs down break" · 5:30–6:30
- **Shows:** split screen. Left: price exits the top, all sells filled, "$ $ $ all cash", "Upper exit rule". Right: price exits the bottom, all buys filled, "C C C all coin", "Stop-loss rule".
- **Teaches:** what you hold after each break.
- **On-screen text:** as above.
- **Data:** illustration.
- **Brand:** [BRAND-STD]
- **Reuse:** `paint_leave`.
- QA: [ ] accurate [ ] on brand [ ] unique [ ] 3 s

**BP06-V04** · CARD · Worked example "Loss at stop" · 6:30–8:00
- **Shows:** a sum card that builds line by line:
  - Bot A$2,000 · start 100 · band 90–110 · 10 gaps of 2
  - Start: 10 coins (A$1,000) + A$1,000 cash in 5 buys of A$200
  - All buys fill: +10.65 coins → ≈ 20.65 coins
  - Stop sells at 85: ≈ A$1,755
  - Fees ≈ A$4
  - **Loss at stop ≈ A$249 (≈ 12% of the bot)**
- **Teaches:** you know your loss before starting.
- **On-screen text:** as above; title "KNOW YOUR LOSS FIRST".
- **Data:** EXAMPLE, A$; fee 0.1%.
- **Brand:** [BRAND-STD]
- **Reuse:** reused as the input in BP10-V02.
- QA: [ ] accurate [ ] on brand [ ] unique [ ] 3 s

**BP06-V05** · STILL · Teach 5 "Start near the middle" · 8:00–8:45
- **Shows:** a band with a cyan "Start here" marker at mid-band (good, ✓). A faded marker at the top edge reads "starting at the edge = all cash fast".
- **Teaches:** start near the middle of the band.
- **On-screen text:** "START NEAR THE MIDDLE".
- **Data:** none.
- **Brand:** [BRAND-STD]
- **Reuse:** none.
- QA: [ ] accurate [ ] on brand [ ] unique [ ] 3 s

---

## BP-07 · Spot paper trading (target 12:30)

**KEEP**
- Lesson stills, PASS: 001, 004, 005, 006, 007, 008, 009, 010, 011, 012, 013, 014, 015, 019.
- **REMAKE:** 003 and 020 (known FAILs). Both become code-drawn cards.
- **Code-drawn NEEDED:** 002.

**NEW**

**BP07-V01** · SCREEN · Teach 1 "Form to page" · 2:00–4:30
- **Shows:** a demo grid-bot form captured with `capture_demo.js` and blurred with screen-demo-kit. Each field is highlighted in turn with a cyan connector line to the matching row of the plan page shown on the right: Pair, Upper, Lower, Grids (chip: "lines or gaps? check the preview count"), Amount, Stop/exit fields. Defaults get a "DEFAULT, not your choice" tag. The walk ends with a cursor hovering, not clicking, over the confirm control and a "STOP HERE" chip.
- **Teaches:** the form copies the page; stop before confirm.
- **On-screen text:** field chips, "Form calls it… / Your page calls it…".
- **Data:** EXAMPLE values from the plan page.
- **Brand:** [BRAND-STD]. `screen-demo-kit qa` PASS. No exchange name or logo; balances blurred.
- **Reuse:** none (the first course use of the kit).
- QA: [ ] accurate [ ] on brand [ ] unique [ ] 3 s

**BP07-V02** · STILL · Teach 2 "What to record on paper" · 4:30–6:00
- **Shows:** the BP-02 journal page (V04 style) with only the paper-run columns highlighted: Fills, Pairs, Fees, Touches, Breaks, Rules followed.
- **Teaches:** the paper run produces evidence.
- **On-screen text:** "RECORD EVERY CHECK".
- **Data:** EXAMPLE.
- **Brand:** [BRAND-STD]
- **Reuse:** a variant of BP02-V04 (a new still, so it stays unique).
- QA: [ ] accurate [ ] on brand [ ] unique [ ] 3 s

**BP07-V03** · STILL · Teach 3 "Paper vs real" · 6:00–6:45
- **Shows:** two columns, "Paper" vs "Real". Rows: fills are perfect vs fills can slip (slippage); no fees felt vs real fees; calm vs nervous.
- **Teaches:** paper is easier than real.
- **On-screen text:** as above.
- **Data:** none.
- **Brand:** [BRAND-STD]. L-plates icon small in the corner.
- **Reuse:** BP01-V07 icon.
- QA: [ ] accurate [ ] on brand [ ] unique [ ] 3 s

**BP07-V04** · CARD · Worked example "Two-week paper journal" · 6:45–8:00
- **Shows:** a filled journal of 14 rows, summarised: Pairs 9 · Touches 1 · Stop triggered 0 · Rules followed 9/9 · Fees recorded ✓.
- **Teaches:** what a complete paper record looks like.
- **On-screen text:** as above.
- **Data:** EXAMPLE.
- **Brand:** [BRAND-STD]
- **Reuse:** none.
- QA: [ ] accurate [ ] on brand [ ] unique [ ] 3 s

**BP07-V05** · CARD · Teach 4 "Graduation rule" · 8:00–9:00
- **Shows:** a rules card titled "EXAMPLE GRADUATION RULE": at least 14 days · every check on schedule · journal complete · no rule broken → start real money at the **smallest** size your sizing rule allows. A small first-rung highlight of the scaling ladder (preview of BP10-V06).
- **Teaches:** the gate from paper to real.
- **On-screen text:** as above.
- **Data:** EXAMPLE rule.
- **Brand:** [BRAND-STD]
- **Reuse:** ladder motif.
- QA: [ ] accurate [ ] on brand [ ] unique [ ] 3 s

---

## BP-08 · Managing and monitoring (target 12:30)

**KEEP**
- Lesson stills, PASS: 001, 004, 005, 006, 007, 008, 009 (text adjust: no ranking or leverage control; results are reviewed in the journal), 010, 011, 012 (**REMAKE**: "no result row" becomes "result row is a review record, not a target"), 013, 014, 015 (**REMAKE**: the recap "NO RESULT" chip), 019.
- **Code-drawn NEEDED:** 002, 003, 020. These replace the "MANAGINGMONITORING" and wrong-disclaimer FAILs.

**NEW**

**BP08-V01** · STILL · Teach 2 "Weekly journal entry" · 3:45–5:15
- **Shows:** one journal row enlarged: Week · Fills · Pairs · Fees · Realised · Unrealised · Total · Rules followed Y/N.
- **Teaches:** the weekly record.
- **On-screen text:** column names; headline "ONE ROW A WEEK".
- **Data:** EXAMPLE.
- **Brand:** [BRAND-STD]
- **Reuse:** BP02-V04 family.
- QA: [ ] accurate [ ] on brand [ ] unique [ ] 3 s

**BP08-V02** · MOTION · Worked example "Grid income is not the whole result" · 5:15–6:30
- **Shows:** two buckets fill and empty. The "Realised (pairs)" bucket gets +A$10.80. The "Unrealised (coin held)" bucket gets −A$24 as price slides 100 → 97. They merge into "Week total ≈ −A$13".
- **Teaches:** realised vs unrealised.
- **On-screen text:** as above.
- **Data:** EXAMPLE: 6 pairs × A$1.80; 100 → 97.
- **Brand:** [BRAND-STD]. Buckets analogy.
- **Reuse:** bucket style from BP-10 005.
- QA: [ ] accurate [ ] on brand [ ] unique [ ] 3 s

**BP08-V03** · MOTION · Teach 3 "Drawdown" · 6:30–7:45
- **Shows:** an account-value line rises to a peak marker (A$2,050), dips to A$1,950, and a bracket labels "Drawdown = (2,050 − 1,950) ÷ 2,050 ≈ 4.9%".
- **Teaches:** drawdown is measured from the highest point.
- **On-screen text:** as above; title "DRAWDOWN".
- **Data:** EXAMPLE.
- **Brand:** [BRAND-STD]
- **Reuse:** none.
- QA: [ ] accurate [ ] on brand [ ] unique [ ] 3 s

**BP08-V04** · STILL · Teach 4 "Adjust or stop" · 7:45–8:45
- **Shows:** a decision fork after the three rows. "All three OK → do nothing". "Band touched / regime changed → follow written re-centre or stop rule". "Rule broken → stop and review".
- **Teaches:** only written moves.
- **On-screen text:** as above.
- **Data:** none.
- **Brand:** [BRAND-STD]
- **Reuse:** none.
- QA: [ ] accurate [ ] on brand [ ] unique [ ] 3 s

**BP08-V05** · CARD · "Records for tax (Australia)" · 9:30–10:00
- **Shows:** a card reading "Each sell or swap can be a CGT event · Keep dated records · General information: check ATO guidance or a registered tax agent".
- **Teaches:** the journal doubles as a record.
- **On-screen text:** as above.
- **Data:** none.
- **Brand:** [BRAND-STD]. No logos (ATO named in text only).
- **Reuse:** none.
- QA: [ ] accurate [ ] on brand [ ] unique [ ] 3 s

---

## BP-09 · Common mistakes (target 12:00)

**KEEP**
- Lesson stills, PASS: 001, 004, 005, 006, 007, 008, 009, 010, 011, 012, 013, 014, 015, 020. The wick note on 005 is stale. Wick talk stays on candle cards only.
- **Code-drawn NEEDED:** 002, 003 (replace the disclaimer-chip and empty-title FAILs).

**NEW**

**BP09-V01** · MOTION · Case 1 "Grid in a trend" · 3:30–4:30
- **Shows:** the Oct 2023 to Mar 2024 close line rises through a ladder drawn in October. Sells glow, then "all cash" while price keeps climbing; caption "left behind".
- **Teaches:** grids don't suit trends.
- **On-screen text:** "GRID IN A TREND".
- **Data:** EXAMPLE, breakout_2023 closes (about 28k to about 71k on the axis).
- **Brand:** [BRAND-STD]
- **Reuse:** chart code.
- QA: [ ] accurate [ ] on brand [ ] unique [ ] 3 s

**BP09-V02** · CARD · Case 2 "Gaps under fees" · 4:30–5:15
- **Shows:** a reprise of BP05-V02's fail row, inside a "MISTAKE" frame with the rule reference "Lesson 5: cost check".
- **Teaches:** the fee check.
- **On-screen text:** as above.
- **Data:** EXAMPLE.
- **Brand:** [BRAND-STD]
- **Reuse:** BP05-V02 code (new framing keeps it unique).
- QA: [ ] accurate [ ] on brand [ ] unique [ ] 3 s

**BP09-V03** · CARD · Case 3 "Oversizing" · 5:15–6:30
- **Shows:** two bars against a A$10,000 account: "A$2,000 bot → loss at stop ≈ A$249 (2.5%)" vs "A$6,000 bot → ≈ A$750 (7.5%)".
- **Teaches:** size drives the damage.
- **On-screen text:** as above, plus "Rule: Lesson 10 caps".
- **Data:** EXAMPLE (scaled from BP06-V04).
- **Brand:** [BRAND-STD]
- **Reuse:** none.
- QA: [ ] accurate [ ] on brand [ ] unique [ ] 3 s

**BP09-V04** · MOTION · Case 4 "Revenge adding / chasing the band" · 6:30–7:45
- **Shows:** the band breaks down and the stop triggers. A new lower band is drawn with a doubled money chip, and it breaks again. The loss counter steps twice. The rule chip reads "Add only after a passed review (Lesson 10)".
- **Teaches:** don't add to win back losses.
- **On-screen text:** as above.
- **Data:** illustration with EXAMPLE amounts.
- **Brand:** [BRAND-STD]
- **Reuse:** none.
- QA: [ ] accurate [ ] on brand [ ] unique [ ] 3 s

**BP09-V05** · STILL · "Correlation" · 7:45–8:30
- **Shows:** two coin outlines labelled "BTC bot" and "ETH bot" with their price lines moving almost together, poured into **one** bucket labelled "Counts as one risk".
- **Teaches:** correlated bots share risk.
- **On-screen text:** "MOVE TOGETHER = ONE RISK".
- **Data:** illustration.
- **Brand:** [BRAND-STD]. Generic coin outlines, no logos (letters only).
- **Reuse:** bucket analogy.
- QA: [ ] accurate [ ] on brand [ ] unique [ ] 3 s

---

## BP-10 · Scaling up on spot (target 14:00)

**KEEP**
- Lesson stills, PASS: 001, 004, 005, 006, 007, 008, 009, 010, 012, 013, 014, 015, 020.
- 011 ("The page does not tell you how much money to assign"): **RETIRE**, replaced by BP10-V02.
- **Code-drawn NEEDED:** 002, 003, 021.

**NEW**

**BP10-V01** · CARD · Hook "What scaling means here" · 0:40–1:30
- **Shows:** a definition card: "SCALING = growing the money given to bots, step by step, under written rules. Never a promise of results."
- **Teaches:** the definition.
- **On-screen text:** as above.
- **Data:** none.
- **Brand:** [BRAND-STD]
- **Reuse:** none.
- QA: [ ] accurate [ ] on brand [ ] unique [ ] 3 s

**BP10-V02** · CARD · Teach 1 "Two sizing caps" · 1:30–3:30
- **Shows:** a rules card titled "EXAMPLE SIZING RULES (A$10,000 account)":
  1. One bot ≤ 20% of the account = A$2,000
  2. Loss at stop ≤ 2.5% of the account = A$250
  The check row reads "BP-06 bot: A$2,000, loss ≈ A$249 ✓ fits".
- **Teaches:** sizing from caps, not feelings.
- **On-screen text:** as above.
- **Data:** EXAMPLE.
- **Brand:** [BRAND-STD]
- **Reuse:** BP06-V04 output.
- QA: [ ] accurate [ ] on brand [ ] unique [ ] 3 s

**BP10-V03** · STILL · Teach 2 "The review gate" · 3:30–5:00
- **Shows:** a gate graphic with six cyan check rows: 30 days or 20 pairs · every weekly check done · rules followed every time · journal complete · regime still fits · no drawdown limit hit. The gate opens only when all six are ticked.
- **Teaches:** add money only after a passed review.
- **On-screen text:** "REVIEW GATE" plus the six rows.
- **Data:** EXAMPLE rule.
- **Brand:** [BRAND-STD]. Unique illustration for BP-10.
- **Reuse:** none.
- QA: [ ] accurate [ ] on brand [ ] unique [ ] 3 s

**BP10-V04** · CARD · Worked example "A scale step that fails the cap" · 5:00–6:30
- **Shows:** a step card:
  - +25% → A$2,500 bot
  - Loss at stop ≈ A$311 = **3.1% ✗** (cap 2.5%)
  - Option A: wait until the account ≈ A$12,440
  - Option B: re-plan the band and stop, re-test on paper
  - Footer: "The rule decides, not the feeling."
- **Teaches:** each step is checked against the caps.
- **On-screen text:** as above.
- **Data:** EXAMPLE: 249 × 1.25 ≈ 311; 311 ÷ 0.025 ≈ 12,440.
- **Brand:** [BRAND-STD]
- **Reuse:** none.
- QA: [ ] accurate [ ] on brand [ ] unique [ ] 3 s

**BP10-V05** · MOTION · Teach 3 "Many bots, one risk cap" · 6:30–8:00
- **Shows:** a row of buckets (Bot 1 BTC, Bot 2 ETH, Bot 3 other) fill with their loss-at-stop amounts. BTC and ETH merge (correlated). A total gauge fills toward "6% cap = A$600"; two independent A$2,000 bots read "≈ A$498 used".
- **Teaches:** total open risk, with correlated bots counted together.
- **On-screen text:** "TOTAL RISK ≤ 6%".
- **Data:** EXAMPLE.
- **Brand:** [BRAND-STD]
- **Reuse:** extends BP-10 005 buckets (KEEP still used first).
- QA: [ ] accurate [ ] on brand [ ] unique [ ] 3 s

**BP10-V06** · MOTION · Teach 4 "Drawdown limits and scale-down" · 8:00–9:30
- **Shows:** an account line from a A$10,600 peak down to A$9,540. At −10% a chip fires: "HALVE every bot". The line continues to −15%: "STOP all bots → paper until review". A side list of other triggers: regime change · two band breaks in a month · any rule broken · journal behind.
- **Teaches:** when to scale down, by rule.
- **On-screen text:** as above.
- **Data:** EXAMPLE: (10,600 − 9,540) ÷ 10,600 = 10%.
- **Brand:** [BRAND-STD]. No amber.
- **Reuse:** BP08-V03 code.
- QA: [ ] accurate [ ] on brand [ ] unique [ ] 3 s

**BP10-V07** · MOTION · "The scaling ladder" · 9:30–10:30
- **Shows:** a vertical ladder (the course's core analogy) with rungs: Paper → Small real bot → Review passed → +1 step → Second bot (uncorrelated) → … Each rung up requires a gate icon. Down arrows at the side are labelled "drawdown limit / trigger → step down".
- **Teaches:** scaling is a ladder you climb by reviews and step down by rules.
- **On-screen text:** rung labels.
- **Data:** none.
- **Brand:** [BRAND-STD]. Reuses the ladder analogy art style (`analogy-ladder.png` look) as a new motion piece.
- **Reuse:** ladder analogy.
- QA: [ ] accurate [ ] on brand [ ] unique [ ] 3 s

---

## BP-11 · Advanced: liquidation scenarios + capstone (target 13:00)

**KEEP**
- Lesson stills, PASS: 001, 004, 005, 006, 007 (narration: "bucket", not fence), 008, 009, 010, 011, 012, 013, 014, 015 (**REMAKE** text: recap says "isolated bucket", not "isolated fence"), 019.
- **Code-drawn NEEDED:** 002, 003 (replace the "LIQUIDATION SCENES" FAIL), 020 (becomes the series end card).

**NEW**

**BP11-V01** · CARD · Worked path "The 2020 drop, closes only" · 4:15–5:00
- **Shows:** a close-only line for Feb to Mar 2020 with two tags: "11 Mar close 7,911" and "12 Mar close 4,971", plus a bracket "≈ −37% in one day". Two outcome chips: "Spot: still held, worth less" / "Contract: can be closed by the venue".
- **Teaches:** spot vs contract on the same drop.
- **On-screen text:** as above.
- **Data:** EXAMPLE, crash_2020 closes. No 13 Mar low on this line chart.
- **Brand:** [BRAND-STD]
- **Reuse:** chart code.
- QA: [ ] accurate [ ] on brand [ ] unique [ ] 3 s

**BP11-V02** · STILL · Teach 3 "Why we scale on spot only" · 5:00–6:00
- **Shows:** two buckets. The spot bucket has a "loss at stop known" tag. The leveraged bucket has a crack and the tag "forced close before your stop". The caption reads "Scaling rules need a loss you control".
- **Teaches:** leverage breaks the sizing caps.
- **On-screen text:** as above.
- **Data:** none (no multiple shown).
- **Brand:** [BRAND-STD]
- **Reuse:** bucket analogy.
- QA: [ ] accurate [ ] on brand [ ] unique [ ] 3 s

**BP11-V03** · MOTION · Capstone "Your complete plan" · 6:30–10:30
- **Shows:** the one-page plan card (checklist analogy) filling row by row, each row tagged with its lesson:
  - Regime (L4)
  - Range and gaps vs fees (L5)
  - Entry, stop trigger, stop action, loss at stop (L6)
  - Paper run and graduation (L7)
  - Weekly check and journal (L8)
  - Mistakes audit (L9)
  - Sizing caps, review gate, step, total risk, drawdown limits (L10)
  A mini-visual from that lesson flashes beside each row.
- **Teaches:** the whole course as one plan.
- **On-screen text:** "YOUR COMPLETE PLAN" plus the row labels.
- **Data:** EXAMPLE A$10,000 plan values from the BP-06 and BP-10 cards.
- **Brand:** [BRAND-STD]. This is BP-11's unique illustration.
- **Reuse:** thumbnails of the earlier new visuals (allowed inside a recap montage; each is labelled).
- QA: [ ] accurate [ ] on brand [ ] unique [ ] 3 s

**BP11-V04** · CARD · "Explain it back" · 10:30–11:30
- **Shows:** five question cards in turn, with a pause chip "Say it aloud":
  1. Why can a grid earn?
  2. When does it stop?
  3. What do you do at the stop?
  4. How big can a bot be?
  5. When do you add or cut money?
- **Teaches:** the series outcome check.
- **On-screen text:** as above.
- **Data:** none.
- **Brand:** [BRAND-STD]
- **Reuse:** none.
- QA: [ ] accurate [ ] on brand [ ] unique [ ] 3 s

**BP11-V05** · CARD · Series end card · 12:00–13:00
- **Shows:** wordmark, mascot, "Blueprint complete". The checklist reads: paper until your graduation rule passes · weekly check · journal · scale only by written rules. Disclaimer footer.
- **Teaches:** the close and the next actions.
- **On-screen text:** as above.
- **Data:** none.
- **Brand:** [BRAND-STD]
- **Reuse:** end-card template (`paint_outro`) without a "NEXT" lesson.
- QA: [ ] accurate [ ] on brand [ ] unique [ ] 3 s

---

## Totals

| Lesson | KEEP stills (PASS) | New STILL | New MOTION / CARD / SCREEN | Remakes / code-drawn cards needed |
|---|---|---|---|---|
| BP-01 | 16 + 9 code-drawn | 3 | 4 | 012 text, course map; retire fence + 015 |
| BP-02 | 18 + 8 code-drawn | 2 | 3 | 021; retire 012, 014 |
| BP-03 | 19 + 7 code-drawn | 1 | 4 | 009, 011 and 014 are already plain. Do not remake them again. |
| BP-04 | 14 | 1 | 4 | 002, 003, 020 |
| BP-05 | 14, including 006 | 0 | 5 | 002, 003, 019. 006 maths is already correct. |
| BP-06 | 14 | 2 | 3 | 002, 003, 016, 018, 020 |
| BP-07 | 14 | 2 | 3 | 002, 003, 020 |
| BP-08 | 13 (+012 remake) | 2 | 3 | 002, 003, 020 |
| BP-09 | 14 | 1 | 4 | 002, 003 |
| BP-10 | 13 (011 retired) | 1 | 6 | 002, 003, 021 |
| BP-11 | 13 (+015 remake) | 1 | 4 | 002, 003, 020 |
| **Total** | **161 KEEP + 24 code-drawn** | **16 new stills (bc-6781931a)** | **43 new code-drawn / screen** | about 30 cards or remakes |

Every lesson gets at least one new unique illustration (S9). Creative Studio scores all 16 new stills and any remake. Cursor bc-6781931a makes the stills; Cursor PR #17 codes the MOTION, CARD and SCREEN items in `studio.py`.
