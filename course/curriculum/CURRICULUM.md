# GridBot Blueprint: curriculum (expand the existing 11 lessons)

Version 1 · 16 Nov 2026 (WITA) · For Stewart's review · Education only

**Scope (Stewart, 16 Nov, 8:10am WITA):** expand the current 11 lessons. Do not redesign them. Lesson list, order, titles, scripts and passed visuals stay as the base. Each lesson gets ADD and ADJUST items to reach 10–15 minutes of beginner teaching. The one reorder idea is marked **OPTIONAL**.

Companion files:
- `BASELINE.md`: what worked, what kept failing, where the tools live, and the team QA plan.
- `VISUALS.md`: KEEP stills and the new visuals for each lesson.

---

## 0. Standard checklist (every lesson must pass all of these)

| # | Check | How it is checked | Tool or owner |
|---|---|---|---|
| S1 | Titles fully in frame, none sliding off | Frame samples at every chapter title, plus intro and outro | Completeness verifier |
| S2 | Captions and all on-screen text inside the **5%** safe margin (96 px left/right, 54 px top/bottom at 1920×1080) | OCR margin check at 5%. Today's gate only checks 4% (see BASELINE). | Quality gate + verifier |
| S3 | Audio −14 LUFS ±1, true peak ≤ −1 dBTP, no silence ≥ 2 s | `ebur128` + `silencedetect` | `lib/mix.py` + quality gate |
| S4 | Chart and number accuracy, every figure marked EXAMPLE | Re-compute every worked number and check dates against `btc-usd-windows.json` | Accuracy verifier + Crypto Research |
| S5 | **Navy and cyan only, NO teal mixing.** Every current use of teal, amber or mint is flagged for Stewart's decision (§5.4). | Palette check on frames and stills | Creative Studio (a lint is proposed) |
| S6 | Length **10:00–15:00** (target 12–13 min) | Probe the master | Quality gate (profile change proposed) |
| S7 | Branded intro and outro (wordmark, visor mascot, lesson number and title; NEXT card) | Frame check | `studio.py` `paint_brand` / `paint_outro` |
| S8 | Background music bed under the voice, ducked 20 dB | Listen + no silence at −50 dB | `lib/mix.py` |
| S9 | At least **one unique illustration per lesson** that appears in no other lesson | Hash-uniqueness across `course/images` | Creative Studio |
| S10 | **Screen-demo kit** used for any exchange or bot walkthrough (blur, then the QA pass) | `screen-demo-kit cli.py qa` on every screen frame | `skills/video-production/screen-demo-kit` |
| S11 | **One builder** (`course/blueprint-rebuild/studio.py`) and **one loudness standard** (`skills/video-production/lib/mix.py`) for all 11 lessons | Build log names `studio.py`; gate report shows −14 | Cursor + verifier |
| S12 | The existing quality gate passes: `skills/video-production/quality-gate`, format `blueprint`, plus `image_gate.py` on current PASS blobs | `report.md`: every check PASS | Quality gate |

Production rule (unchanged): render one lesson at a time. If anything is flagged, stop, fix and re-render before starting the next lesson. Each lesson gets verified images and script, a render, the audio check, the accuracy verifier, and a **fresh blind first-timer watch**.

---

## 1. Course promise and learner profile

**Course promise (said in BP-01 and repeated in every recap):**

> "By the end of this series you will understand exactly what a grid bot does, why it can earn on bounces, and where it loses. You will know how to plan one, test it on paper, run it, check it, and grow the money you give to bots step by step under written risk rules. This is education, not a promise of results."

**Series learning outcome (master criterion; Stewart, 16 Nov, 8:06am WITA):**

> By the end of BP-11 the viewer has a complete understanding of grid bots and can scale a trading account with one. "Scale" is taught as education only. It means growing the capital allocated to bots step by step under written risk rules:
> - sizing each bot
> - adding capital only after a rule-based review
> - running more than one bot without doubling the same risk
> - drawdown limits
> - knowing when to scale down
> - journaling and review
>
> It never promises returns.

**Learner profile:** an Australian adult who has never heard of a grid bot.

- Assume no knowledge of crypto, exchanges, wallets, orders, candles, charts, fees, stablecoins, margin or tax records.
- They may never have bought a coin.
- They learn by seeing one picture and one worked example at a time.
- They need to be told *why*, *when* and *exactly what they do*, and whether the bot does it or they do.
- They give up when a word appears before it is explained, or when the lesson jumps around.

## 2. Learning path (one line)

**BP-01** what a grid is and why it earns → **BP-02** what you need (account, pair, fees, journal, safety) → **BP-03** how the bot places and refills orders → **BP-04** when a grid fits (regimes) → **BP-05** setting range and spacing that beat fees → **BP-06** written entry, exit and stop, with the loss known in advance → **BP-07** a paper run on a demo screen → **BP-08** weekly checks and the journal → **BP-09** the mistakes that break plans → **BP-10** scaling capital under written rules → **BP-11** opt-in leverage and liquidation, then the **capstone: your complete plan and scaling rules**.

## 3. Analogy set (one set, used the same way everywhere)

| Idea | Analogy | Where it is taught | Notes |
|---|---|---|---|
| Grid levels, range, gaps | **Ladder.** Rungs are levels, the top and bottom rungs are the range, the space between rungs is a gap. "The rungs wait; they don't chase you." | BP-01, reused in 03, 05 | KEEP (`analogy-ladder.png` PASS). Range is now the top and bottom rungs, **replacing the fence**. |
| Why a grid earns | **Market stall.** A stallholder buys stock a little cheaper and sells it a little dearer, many times, and pays a stall fee on every sale. | BP-01, reused in 05, 08 | NEW. The headline never says "buy low, sell high" as a slogan (that still failed QA). |
| Paper and demo practice | **L-plates.** A learner driver practises with L-plates before driving alone. | BP-01, 07 | NEW. **Replaces the fence** for "paper or demo" (BP-01 015). |
| The plan page | **Checklist.** Tick every row before you start. | BP-02, 06, 07, 11 capstone | KEEP (`analogy-list.png` PASS) |
| Separate money per bot; isolated vs cross margin | **Buckets.** Each bot has its own bucket, and a leak stays in that bucket. | BP-10, 11 | KEEP (BP-10 005, BP-11 007/008) |

**Retired:** the fence analogy, everywhere: `analogy-fence.png`, BP-01 "The fence" chapter, BP-01 015, and the BP-11 recap "isolated fence". It is not to be reused.

---

## 4. First-time learner review rubric (every rendered video is judged against this)

The reviewer watches the lesson as someone who has never seen a grid bot. **Master criterion M0 is scored first.** A lesson fails if M0 or any B item fails.

| # | Criterion | PASS when |
|---|---|---|
| **M0** | **Moves the viewer toward the series outcome** (complete understanding plus the ability to scale under written risk rules; education only) | The lesson states its piece of that outcome in the hook and the recap, as given in its "Moves toward the outcome" line below. The reviewer can say what new capability they gained and how it feeds scaling. |
| B1 | Teaches **why** | Every rule comes with the reason for it (for example, why a stop exists, or why gaps must beat fees) |
| B2 | Teaches **when** | Triggers are concrete (for example, "a daily close outside the band, and the next daily close still outside") |
| B3 | Teaches **what you do**, and **bot vs you** | Each action names who does it: the bot automatically, or you by hand |
| B4 | **Terms grounded before use** | No term is spoken or shown before its plain-English definition and lower third |
| B5 | **A single clear structure** | Hook → teach → worked example → common mistake → what you do next → recap. No repeated block, no second hook, no course admin in the middle. |
| B6 | **No undefined jargon** on screen or in voice | Includes captions, chapter titles and still labels |
| B7 | **Explain-back test** | After one watch, the reviewer can explain the lesson's one-line objective and answer the 3 self-check questions |
| B8 | Worked example | At least one, with numbers marked EXAMPLE and fees included where money changes hands; arithmetic shown on screen, not only spoken |
| B9 | Visual clarity | Each visual makes its point in 3 seconds. No cryptic icons or titles. No high, low or wick talk over a close-only line. |
| B10 | Pacing | No spoken list longer than 3 numbers, no repeated sentences, no dead holds. The picture changes at least every 8 s. |
| B11 | Compliance | GridBot Builder only, education-only disclaimer, no profit claims, no exchange names |
| S1–S12 | Standard checklist (§0) | All PASS |

Reviewers' comments about the voice are non-blocking (standing rule).

---

## 5. Course-wide rules

1. **Brand:** GridBot Builder only. Never Market Pros, no ABN, no entity name, no personal names on screen.
   - Flag: the current wordmark and narration say "**Grid Bot Builder**" (with spaces). Stewart to confirm the spelling, then apply it to every lesson.
2. **Education only:** no profit claims, win rates or income promises.
   - Every number is labelled EXAMPLE.
   - Worked "earnings" are shown with fees and alongside the losing case.
   - Standard disclaimer, spoken and on screen (keep the current Australian wording): "Education only. Not financial advice. This is general information and doesn't consider your objectives, financial situation or needs. Crypto is high risk; you could lose all the money you put in. Past performance is not a reliable indicator of future results."
3. **Narration:** Kokoro af_heart at speed 1.0 (`studio.py` hard stop).
   - Do not read raw URLs, file paths or long hashes aloud.
   - Prices of five or more digits are not spoken (keep `_speak_round`). Check the grammar of every swap.
4. **Colour: navy and cyan, no teal mixing.** Stewart's decision is needed on these current uses:
   - AMBER `(255,176,32)`: stop chapter idea text, the 30,331 highlight, the leave-band dot and "all cash/all coin" labels, the "No profit promises" X, stop-sign icons (BP-02), the crystal-ball X (BP-03).
   - MINT `#4FD1A5`: sell lines, the cash/coin key, end-card ticks, BP-03 rungs. Mint reads as **teal** on navy.
   - BLUE `#1E7BFF`: buy lines.
   - The still style (`STYLE_V3_GBB.md`) allows mint for sells and amber for warnings. The Elite TEAL style must never be used for Blueprint.
   - Recommended: navy + cyan + white only. Buys are solid cyan, sells are outlined white, the stop is a white dashed line with a warning icon. Recolouring would touch most passed stills, so decide before more renders.
5. **Australian context:**
   - Account examples in A$. Price data is public BTC/USD daily closes (Yahoo source), labelled.
   - The daily close is cut at 00:00 UTC, which is **11:00am AEDT** (10:00am AEST).
   - Exchanges are described generically. Australian exchanges must be registered with AUSTRAC; name the regulator only, never an exchange.
   - Selling or swapping crypto can be a CGT event, so keep records. This is general information; check ATO guidance or a registered tax agent.
   - Scam warnings point to Moneysmart.
6. **Analogy set:** §3 only. No fence.
7. **One builder, one loudness standard, one gate** (S11, S12).
8. **Format:** 1920×1080, 30 fps, H.264/AAC. Sidecar captions at most 42 characters and 18 characters per second.

---

## 6. Lessons

Every lesson uses the same skeleton (B5):

1. Open and disclaimer (KEEP, about 0:40)
2. Hook
3. Teach
4. Worked example
5. Common mistake
6. What you do next
7. Recap and outro (KEEP pattern, about 1:00)

Minute estimates use about 160 words per minute at Kokoro 1.0 (measured on BP-01 v8).

---

### BP-01 · Introduction

- **Current:** film **7:19** (438.8 s, v8 962465c). Spoken plan: 23 shots, plus 18 appended JSON beats.
- **Target runtime: 12:30**
- **Moves toward the outcome:** the viewer learns the core mechanism (why a grid earns on bounces, and what happens when price leaves). They see the whole series path ending in scaling under written rules.
- **Objectives** (after this lesson the viewer can):
  1. Explain a grid as buy orders below and sell orders above inside a band, and why each completed buy-then-sell pair earns the gap minus fees.
  2. Say what happens when price leaves through the top (mostly cash) or bottom (mostly coin).
  3. State a stop rule: when it triggers, what they do, and whether the bot or they do it.
- **Prerequisites:** none.
- **New terms** (defined before use, each with a lower third):

| Term | Plain-English definition |
|---|---|
| crypto | digital money such as bitcoin |
| exchange | the website or app where you swap Australian dollars for crypto and back |
| cash | money you can spend; here, dollars or a dollar-pegged coin |
| coin | the crypto |
| order | an instruction to buy or sell |
| buy order | swap cash for coin |
| sell order | swap coin for cash; you need coin first |
| limit order | waits at a price you choose |
| fill | the order's trade happens at its line |
| band / range | the top and bottom you choose |
| level / line / rung | a price where an order waits |
| gap | the space between two lines |
| daily close | the last price of the day, cut at 11am AEDT |
| fee | what the exchange charges on each trade |
| stop | a written rule for what you do if price leaves the band and does not come back |
| bot | software that places and refills the orders for you |

- **Worked example (EXAMPLE, BTC/USD summer 2023):**
  - Band 24,930 to 30,331, six gaps of about 900.
  - One pair: buy 0.01 BTC at 27,630 (US$276.30), then sell it at 28,531 (US$285.31), so US$9.01 gross.
  - Fees of 0.1% each side come to US$0.56, so **about US$8.45 net** for that one pair.
  - It only happens if price comes back up through 28,531. If price leaves through the bottom, you hold coin bought above the market.
  - The summer window had 28 daily-close crossings of the seven lines (EXAMPLE; closes only; the verifier must re-check the count).
- **Segment outline (12:30):**

| Time | Segment | Status |
|---|---|---|
| 0:00–0:40 | Open, disclaimer, risk lines | KEEP |
| 0:40–1:20 | **Hook:** price often bounces sideways; a grid is a ladder of waiting orders built for that. Series promise, ending in scaling under written rules. | KEEP + ADD promise |
| 1:20–2:50 | **Teach 1, the basics:** crypto, exchange, cash vs coin, buy = cash→coin, sell = coin→cash, so selling needs coin first and a grid starts part cash, part coin. Limit order, "rungs wait". | ADD grounding (fix #9) + KEEP limit-order lines |
| 2:50–4:20 | **Teach 2, the ladder on the real path:** range = top and bottom rungs, levels, about 900 gap maths, seven lines, buys below and sells above. Bot vs you: you choose the band, gaps and money; the bot places each order and, after a fill, places the opposite order one rung away. | KEEP (ladder, range, levels) + ADD bot vs you |
| 4:20–5:50 | **Teach 3, why a grid earns:** one buy-low/sell-high pair on a bounce, many small pairs, fees on every fill; the catch is that it only works while price keeps bouncing inside. | **ADD** (fix #9) |
| 5:50–7:00 | **Worked example on real data:** 19 Jul candle card, whole summer window inside the band, the pair maths on screen | KEEP candle + whole window; ADD pair card |
| 7:00–8:30 | **When price leaves the band:** climb → all cash, fall → all coin ($/C key) | KEEP motion |
| 8:30–9:50 | **The stop, plainly:** trigger (EXAMPLE rule: a daily close outside the band, and the next daily close still outside); action (stop the bot, which cancels the waiting orders, then follow the rule written in advance: keep the coin or swap back to cash); who does it (some bots have an automatic stop setting at a price; otherwise you do it by hand, and you write which). Real case: 23 Oct close above the top, 24 Oct still above, so the example is finished. | KEEP 23 Oct + **ADD** trigger, action, bot vs you (fix #9) |
| 9:50–10:30 | **Common mistake:** thinking the bot predicts price, or starting without a written stop | ADD (merges old "No result number") |
| 10:30–11:30 | **What you do next:** L-plates (paper or demo first); bring a notebook; course map naming each lesson through to scaling | ADJUST (fence → L-plates; map updated) |
| 11:30–12:30 | Recap (three parts + why it earns + stop action), outro card | KEEP |

- **New visuals:** BP01-V01 to V07 (VISUALS.md). V07 is the L-plates still that replaces 015.
- **Self-check:**
  1. Why does a grid start with some coin as well as cash?
  2. In the EXAMPLE pair, why is the net about US$8.45 and not US$9.01?
  3. Price closes above your top line and the next day's close is still above it. What do you do, and does the bot do it or do you?
- **What changes vs the current script:**
  - REMOVE the duplicate second "Hook" block (v8 4:21–5:13: Hook, three parts, buys and sells, no order is sent, map). Fold its content into one flow.
  - REPLACE the fence (2:39 chapter and 015) with ladder rungs and L-plates.
  - REWORD "No result number" to "No promise of results". The lesson now shows the mechanics of one pair with fees.
  - REWORD "Leave every figure marked EXAMPLE" to "Numbers marked EXAMPLE are teaching numbers, not advice".
  - ADD the series promise, basics, bot vs you, why it earns, the stop action and the common mistake.
- **Additions summary:** promise +0:20, basics +1:00, bot vs you +0:30, why it earns +1:30, pair card +0:30, stop action +1:00, common mistake +0:40, minus the duplicate block −1:00. Net **about +5:10, from 7:19 to about 12:30**.
- **Script brief:**
  - One flow, no second hook.
  - Define every term in the table at its first use, with a lower third.
  - Keep every verified number (24,930 / 30,331 / about 900 / 19 Jul candle / 23 Oct 33,086).
  - Speak "the top line" and "about 900 dollars", never five-digit prices.
  - The pair maths goes on a card; say only "about eight dollars fifty after fees, for one small pair".
  - The stop rule is said as three plain sentences: when, what, who.
  - No fence anywhere; use ladder, market stall and L-plates only.
  - End on the promise and "Next: what you're going to need".

---

### BP-02 · What you are going to need

- **Current:** film **7:23** (older render 8c65710). Plan: 16 shots, about 860 words; 21 JSON beats.
- **Target runtime: 12:00**
- **Moves toward the outcome:** the viewer sets up the account, fee knowledge, security and **trading journal** that every later review and scaling decision relies on.
- **Objectives:**
  1. List the seven setup items and why each matters.
  2. Read a pair name (base/quote) and find an exchange's maker and taker fee.
  3. Set up a one-page plan and a journal, with secrets kept off both.
- **Prerequisites:** BP-01.
- **New terms:**

| Term | Plain-English definition |
|---|---|
| account verification (ID check) | the exchange confirms who you are before you can deposit |
| AUSTRAC registration | Australian exchanges must be registered with AUSTRAC; check before signing up |
| two-factor authentication (2FA) | a second code, as well as your password, to log in |
| pair, base, quote | BTC/AUD: you buy the base (BTC) with the quote (AUD) |
| stablecoin | a coin designed to stay near one US dollar |
| maker / taker fee | the fee for an order that waits (maker) versus one that fills straight away (taker) |
| round-trip cost | the fee to buy plus the fee to sell |
| trading journal | a dated record of every bot: plan, changes, fills, fees, result and whether you followed the rules |

- **Worked example (EXAMPLE):**
  - BTC/AUD, maker fee 0.1%. A A$100 buy costs A$0.10 in fees, and the sell costs about A$0.10, so the round trip costs about A$0.20.
  - So any gap smaller than 0.2% loses money before price does anything (this sets up BP-05).
- **Segment outline (12:00):**

| Time | Segment | Status |
|---|---|---|
| 0:00–0:40 | Open, disclaimer | KEEP |
| 0:40–1:20 | Hook: you need a page before a screen, and this page grows into your scaling journal | KEEP + ADD tie |
| 1:20–3:00 | Teach 1: the seven items (notebook, the three words, pair, paper/demo, no secrets, written stop, EXAMPLE) with **why** for each | KEEP + ADD whys |
| 3:00–4:30 | Teach 2: the exchange account in Australia (ID check, AUSTRAC check, AUD deposit, 2FA, where the demo or paper mode usually is). Screen-demo kit only. | **ADD** |
| 4:30–5:30 | Teach 3: pair names, base/quote, stablecoin; BTC/AUD vs BTC/USDT | ADJUST (expand 006) |
| 5:30–6:45 | Teach 4: fees (maker/taker, round-trip cost); worked A$100 example on a card | **ADD** |
| 6:45–8:00 | Teach 5: the trading journal template (columns defined) | **ADD** |
| 8:00–9:00 | Worked check: fill the page for the summer EXAMPLE (pair, band, gaps, stop, EXAMPLE) | KEEP (copy-the-path + worked check) |
| 9:00–9:45 | No secrets: seed phrase, private key, API secret (plain glosses); scam warning (Moneysmart) | KEEP + ADD scam line |
| 9:45–10:30 | Common mistake: opening the screen before the page; profit target or leverage written on the page | KEEP (011/015) |
| 10:30–11:00 | What you do next: complete the page and journal header today | KEEP (020) |
| 11:00–12:00 | Recap, outro | KEEP pattern; **FIX** triple-repeated recap lines |

- **New visuals:** BP02-V01 to V05.
- **Self-check:**
  1. In BTC/AUD, which is the base and which is the quote?
  2. With 0.1% fees each side, what does a round trip cost on A$100?
  3. Name three things that must never go on your page or into a chat.
- **What changes:**
  - ADD exchange basics (Australia), fees, and the journal.
  - FIX the recap and objective stacks that repeat each line two or three times.
  - Define range, levels and stop **before** any numbers.
  - Cut the second recitation of July to October dates (BP-02 watch, item 2).
  - REPLACE the cryptic "Your page comes first / form only copies it" and "Empty Pair" stills.
  - FIX the 021 outro (known FAIL) as a code-drawn card.
- **Additions summary:** account +1:30, pair expansion +0:30, fees +1:15, journal +1:15, whys +0:30, scam line +0:15. Net **about +5:00 after trimming repeats, from 7:23 to about 12:00**.
- **Script brief:**
  - Each of the seven items gets "what it is" and then "why you need it".
  - The account section is generic: no exchange names or logos; any screen goes through the screen-demo kit with balances blurred.
  - The fee maths goes on a card.
  - Introduce the journal as "the record you'll use in Lesson 8 and Lesson 10 to decide whether you're allowed to add money".

---

### BP-03 · What is a grid bot

- **Current:** film **6:30** (older render da9d22b). Plan: 18 shots, about 940 words; 19 JSON beats.
- **Target runtime: 12:00**
- **Moves toward the outcome:** the viewer understands exactly what the bot does on every fill and what settings it needs. That understanding comes before anyone can size or scale one.
- **Objectives:**
  1. Describe the full grid cycle: a fill, then the opposite order placed one rung away.
  2. Name the settings a grid bot asks for (upper, lower, number of grids, amount) and work out the order size.
  3. Explain how inventory (coin vs cash) shifts as price moves.
- **Prerequisites:** BP-01, BP-02.
- **New terms:**

| Term | Plain-English definition |
|---|---|
| market order | buys or sells straight away at the current price; already in the plan, keep it |
| grid cycle | buy fills, the bot places a sell one rung up; sell fills, the bot places a buy one rung down |
| completed pair | one buy and its matching sell both filled |
| number of grids | how many lines or gaps you set |
| order size | your amount divided by the number of orders |
| inventory | how much coin vs cash you hold right now |
| upper / lower / side | already in the script, keep |

- **Worked example (EXAMPLE):**
  - A$600 spread over 6 waiting orders is A$100 per order.
  - On the summer path, the price steps down two rungs (two buys fill: hold more coin), then up one rung (one sell fills: one completed pair).
  - Inventory afterwards: one extra coin parcel still held, waiting for its sell.
- **Segment outline (12:00):**

| Time | Segment | Status |
|---|---|---|
| 0:00–0:40 | Open, disclaimer | KEEP |
| 0:40–1:30 | Hook: not a machine that predicts; waiting orders inside a band you chose | KEEP |
| 1:30–3:00 | Teach 1: five labels (upper, lower, levels, side, stop), each defined before use. Limit vs market. | KEEP + define "rung" first |
| 3:00–5:00 | Teach 2: **the grid cycle in motion**: step down, buy fills, sell placed above; step up, sell fills, buy placed below; count completed pairs | KEEP 006/007 + **ADD motion** |
| 5:00–6:30 | Teach 3: the settings a bot asks for (upper, lower, number of grids, amount, order size); arithmetic vs geometric named only ("Lesson 5 explains this") | **ADD** |
| 6:30–7:45 | Worked example: inventory on a short path (coin vs cash after each fill) | ADJUST (expand 008) |
| 7:45–8:45 | Bot vs you: the bot keeps orders in the market; you choose settings, act on the stop and review | KEEP 009/018 + ADD |
| 8:45–9:45 | Common mistake: "the bot earns while price chops" said as a promise. Instead: a fill only swaps cash and coin, and whether you end up ahead depends on where price goes next. | ADJUST (012 + plain rewording) |
| 9:45–10:45 | What you do next: label a band with the five words and the settings on paper | KEEP 015 |
| 10:45–12:00 | Recap, outro | KEEP |

- **New visuals:** BP03-V01 to V05.
- **Self-check:**
  1. A buy at one rung fills. What order does the bot place next, and where?
  2. A$600 over 6 orders: what is the order size?
  3. After price falls through three buy lines, do you hold more coin or more cash?
- **What changes:**
  - ADD the cycle motion, the settings and order-size maths, and bot vs you.
  - Define "rung" before 1:29 (BP-03 watch).
  - Define coin vs cash before 2:57.
  - Explain the stop before "write the stop".
  - REWORD "A result would require a future that this page does not have" to plain wording.
  - REPLACE the chain and circle icons, small Inventory text and looping arrows (watch item 5).
  - Five-digit prices are never spoken.
- **Additions summary:** cycle motion +1:30, settings +1:30, inventory +0:45, bot vs you +0:45, rewording +0:15. Net **about +5:30, from 6:30 to about 12:00**.
- **Script brief:**
  - Slow down around numbers.
  - Show the cycle three times: once slow, once with counts, once on the real summer path.
  - Every setting the bot asks for is named and defined, with a card showing "amount ÷ orders = order size".

---

### BP-04 · Market regimes

- **Current:** not rendered. Plan: 16 shots, about 850 words, **est. 6:00–7:00**; 20 JSON beats.
- **Target runtime: 12:00**
- **Moves toward the outcome:** regime is the first gate in every plan and every scaling review. You only add capital to a bot whose regime still fits.
- **Objectives:**
  1. Sort a 90-day chart into range, trend or break, with one written reason.
  2. Say what a grid does in each regime (bounces earn; trends leave you all cash or all coin; breaks hit the stop).
  3. Re-sort on a schedule and spot a regime change.
- **Prerequisites:** BP-01 to 03.
- **New terms:**

| Term | Plain-English definition |
|---|---|
| regime | the shape the market is in right now: range, trend or break |
| trend | higher highs and higher lows, or lower highs and lower lows |
| break | leaves the band and does not come back |
| volatility | how big the usual daily move is |
| touch | price comes close to the top or bottom and turns back |

- **Worked example (EXAMPLE, three real windows):**
  - **Range:** summer 2023. 83 of 89 daily close-to-close moves were smaller than one 900 gap.
  - **Trend:** Oct 2023 to Mar 2024, from about 28 thousand to about 71 thousand, closes only.
  - **Break:** 11 to 12 Mar 2020, close to close about −37% (closes 7,911 to 4,971).
- **Segment outline (12:00):**

| Time | Segment | Status |
|---|---|---|
| 0:00–0:40 | Open, disclaimer | KEEP |
| 0:40–1:20 | Hook: the same ladder is a different idea in a different regime | KEEP |
| 1:20–2:50 | Teach 1: three shapes defined (range, trend, break) | KEEP 004/006/007/008 |
| 2:50–4:20 | Teach 2: **how to sort, step by step**: 90 days of daily closes; count touches; higher-highs test; one label plus one reason | **ADD** |
| 4:20–6:00 | Teach 3: **what the grid does in each regime** (three-panel motion with the $/C key) | **ADD** |
| 6:00–7:00 | Teach 4: volatility vs gap size, in plain words | **ADD** |
| 7:00–8:15 | Worked sort: the three real windows | ADJUST (009 + real data) |
| 8:15–9:00 | News days and thin markets | KEEP 012 |
| 9:00–9:45 | Regimes change: re-sort weekly; this feeds the Lesson 8 check and Lesson 10 reviews | **ADD** |
| 9:45–10:30 | Common mistake: grid first, regime second; fitting a grid to a trend | KEEP 013 |
| 10:30–11:00 | What you do next: sort one chart on paper with one reason | KEEP 015 |
| 11:00–12:00 | Recap, outro | KEEP |

- **New visuals:** BP04-V01 to V05.
- **Self-check:**
  1. What two things would make you call a chart a trend?
  2. In a strong uptrend, why does a grid end up mostly cash?
  3. How often do you re-sort, and why?
- **What changes:**
  - ADD how-to-sort, regime outcomes, volatility and re-sort.
  - FIX "about about" (#11).
  - FIX the low spoken over the crash line chart: use closes (about −37%) or a 13 Mar 2020 candle card.
  - "Range weaves" becomes "A range bounces".
  - Add a numbers YAML for the builder.
- **Additions summary:** sort how-to +1:30, regime outcomes +1:40, volatility +1:00, re-sort +0:45. **About +5:00, from about 7:00 to about 12:00.**
- **Script brief:** define each shape with a picture before using the word. Use only closes on line charts. Each regime ends with "so the grid…" and "so you…".

---

### BP-05 · Choosing grid spacing and range

- **Current:** not rendered. Plan: 15 shots, about 790 words, **est. 5:30–6:30**; 19 JSON beats.
- **Target runtime: 12:00**
- **Moves toward the outcome:** spacing that clears fees and a range that fits the regime are what make a bot worth sizing at all. You never scale a bot whose gaps lose to fees.
- **Objectives:**
  1. Count gaps vs lines and work out the span.
  2. Check that each gap beats the round-trip fee.
  3. Choose arithmetic or geometric spacing and an order size that meets the exchange minimum.
- **Prerequisites:** BP-01 to 04.
- **New terms:**

| Term | Plain-English definition |
|---|---|
| span | bottom to top, as a percent |
| step | one gap as a percent |
| arithmetic spacing | every gap is the same dollar amount |
| geometric spacing | every gap is the same percent |
| net per pair | gap minus round-trip fee |
| minimum order size | the smallest order the exchange accepts |

- **Worked examples (EXAMPLE):**
  - 20 lines make 19 gaps; 19 × 0.5% ≈ 9.5% span. The 006 maths on the still is already correct. Do not remake it for arithmetic.
  - A$100 order, 0.5% gap: about A$0.50 gross, minus about A$0.20 round-trip fee, is about A$0.30 net per pair.
  - A 0.15% gap: about A$0.15 gross minus A$0.20 is **−A$0.05**, so it fails the cost check.
  - Band A$100 to A$200 with 4 gaps:
    - arithmetic: 100 / 125 / 150 / 175 / 200
    - geometric: 100 / 118.9 / 141.4 / 168.2 / 200
- **Segment outline (12:00):**

| Time | Segment | Status |
|---|---|---|
| 0:00–0:40 | Open, disclaimer | KEEP |
| 0:40–1:20 | Hook: a band that's too tight breaks on an ordinary bounce | KEEP |
| 1:20–2:40 | Teach 1: lines vs gaps; span maths on a card | KEEP 004/005 |
| 2:40–3:40 | Teach 2: arithmetic vs geometric | **ADD** |
| 3:40–5:00 | Teach 3: the fee check, net per pair (pass and fail cases) | KEEP 008/009 + **ADD** worked maths |
| 5:00–6:15 | Teach 4: the trade-off. More grids: smaller gaps, more fills, each smaller. Fewer grids: bigger gaps, rarer fills. | **ADD** motion |
| 6:15–7:15 | Teach 5: setting the range from the regime chart (room for the real highs and lows, shown on a candle card) | ADJUST (011) |
| 7:15–8:00 | Order size and exchange minimum | **ADD** |
| 8:00–9:00 | Worked recount from a wrong page | KEEP 010 |
| 9:00–9:45 | Common mistake: changing step and range in one edit | KEEP 012 |
| 9:45–10:45 | What you do next: write percent, gaps, orders and the cost check on the page | KEEP 013/014 |
| 10:45–12:00 | Recap, outro | KEEP 015 pattern |

- **New visuals:** BP05-V01 to V05.
- **Self-check:**
  1. How many gaps do 12 lines make?
  2. With a 0.2% round-trip fee, does a 0.15% gap pass?
  3. Which spacing keeps every gap the same percent?
- **What changes:**
  - ADD geometric vs arithmetic, the net-per-pair maths, the trade-off and order minimums.
  - FIX the garbled line (#10). The 006 maths is already correct on the still.
  - Move all high, low and wick talk onto candle cards (#5, #11, #13, #16).
  - Fix the 019 outro (known FAIL) as a code-drawn card.
- **Additions summary:** geometric +1:00, fee maths +0:45, trade-off +1:15, range-from-regime +0:30, order minimum +0:45, other trims +0:30. **About +6:00, from about 6:00 to about 12:00.**
- **Script brief:** every percent is shown as a card with the sum. Never "more lines = better". End with the cost-check sentence the learner writes.

---

### BP-06 · Entry and exit rules

- **Current:** not rendered. Plan: 16 shots, about 840 words, **est. 6:00–7:00**; 20 JSON beats.
- **Target runtime: 12:30**
- **Moves toward the outcome:** the viewer knows the **maximum loss at the stop before starting**. That number is the base of every sizing and scaling rule in BP-10.
- **Objectives:**
  1. Write a finish (stop) sentence first, then a start sentence.
  2. Choose the stop action for an upside vs a downside break.
  3. Work out the loss at the stop in dollars before starting.
- **Prerequisites:** BP-01 to 05.
- **New terms:**

| Term | Plain-English definition |
|---|---|
| invalidation | already in the script, keep |
| stop-loss price | the price where you or the bot close everything |
| take-profit / upper exit | an optional rule for leaving through the top |
| loss at stop | what the bot would be down if the stop triggers |
| confirmation | the next daily close is still outside |

- **Worked example (EXAMPLE, A$):**
  - Bot A$2,000, started at price 100, band 90 to 110, 10 gaps of 2.
  - Holds A$1,000 of coin (10 coins) and A$1,000 cash split into 5 buys of A$200.
  - The stop sells everything at 85, after a close below 90 is confirmed by the next close.
  - All buys fill on the way down: about 20.65 coins worth A$1,755 at 85.
  - With fees of about A$4: **loss at stop about A$249**, about 12% of the bot.
- **Segment outline (12:30):**

| Time | Segment | Status |
|---|---|---|
| 0:00–0:40 | Open, disclaimer | KEEP |
| 0:40–1:20 | Hook: an entry without an exit is a page that can't finish | KEEP |
| 1:20–2:40 | Teach 1: two columns; finish first | KEEP 004/005 |
| 2:40–4:00 | Teach 2: the finish sentence: trigger plus confirmation (summer: 23 Oct close above, 24 Oct still above) | KEEP 006 + ADD confirmation |
| 4:00–5:30 | Teach 3: **stop actions**: stop and keep coin; stop and swap to cash; the bot's automatic stop-loss or upper-exit settings (bot vs you) | **ADD** |
| 5:30–6:30 | Teach 4: upside vs downside break (all cash vs all coin) and what each means for you | **ADD** (links BP-01 motion) |
| 6:30–8:00 | Worked example: **loss at stop in A$** on a card | **ADD** |
| 8:00–8:45 | Teach 5: the start sentence (regime, fee check, start near the middle of the band, not the edge) | KEEP 007 + ADD |
| 8:45–9:30 | Hope is not a rule; invalidation | KEEP 009/010 |
| 9:30–10:15 | Common mistake: "I'll know" stops; moving the stop after it triggers | KEEP 011 + ADD |
| 10:15–11:15 | What you do next: write both sentences plus the loss at stop | KEEP 014, ADJUST |
| 11:15–12:30 | Recap, outro | KEEP |

- **New visuals:** BP06-V01 to V05.
- **Self-check:**
  1. What confirms a break in the EXAMPLE rule?
  2. Price leaves through the bottom. What are you holding, and what does your rule say to do?
  3. Why work out the loss at stop **before** starting?
- **What changes:**
  - ADD stop actions, upside vs downside, the A$ loss-at-stop and start-near-middle.
  - ADJUST "Size is not this lesson" to "Sizing is Lesson 10; here you only measure the loss at stop".
  - FIX "summer high" spoken over a line chart (#5).
  - Trim the repeated 23 Oct and 7 Oct dates.
  - Fix stills 016, 018 and 020 (known FAILs, arrow tips).
- **Additions summary:** confirmation +0:30, stop actions +1:30, up vs down +1:00, loss card +1:30, start-near-middle +0:30, common mistake +0:15. **About +5:30, from about 7:00 to about 12:30.**
- **Script brief:** finish first, always. The loss-at-stop card shows each line of the sum. Say plainly: "This number is what you are risking; Lesson 10 uses it to decide how big a bot may be."

---

### BP-07 · Spot paper trading

- **Current:** not rendered. Plan: 16 shots, about 810 words, **est. 6:00–7:00**; 20 JSON beats.
- **Target runtime: 12:30**
- **Moves toward the outcome:** paper is step one of the scaling ladder. The viewer learns the evidence a paper run must produce before any real money, and the graduation rule.
- **Objectives:**
  1. Map every field of a grid bot form to the plan page (on a demo screen captured through the screen-demo kit).
  2. Run and record a paper grid for a set period.
  3. Apply a written graduation rule before using real money.
- **Prerequisites:** BP-01 to 06.
- **New terms:**

| Term | Plain-English definition |
|---|---|
| paper / demo trading | practice with pretend money; L-plates |
| default | a value the form filled in for you |
| slippage | the fill price differs from the line |
| graduation rule | the written test for moving from paper to a small real bot |
| spot vs contract | already in the script, keep |

- **Worked example (EXAMPLE):**
  - Paper run: 2 weeks, summer-style band.
  - Journal shows 9 completed pairs, 1 band touch, stop never triggered, rules followed 9/9, fees recorded.
  - Graduation rule (EXAMPLE): at least 14 days, every check done on schedule, journal complete, no rule broken. Then start real money at the **smallest** size your sizing rule allows.
- **Segment outline (12:30):**

| Time | Segment | Status |
|---|---|---|
| 0:00–0:40 | Open, disclaimer | KEEP |
| 0:40–1:20 | Hook: walk a demo screen, stop before confirm; L-plates | KEEP + ADD analogy |
| 1:20–2:00 | Not affiliated; spot not contract; no keys | KEEP 004/006/007 |
| 2:00–4:30 | Teach 1: **screen-demo walkthrough**: pair, upper, lower, number of grids (gaps vs lines), amount, stop and exit fields, each matched to the page; defaults flagged | KEEP 008–011 + **ADD** screen demo |
| 4:30–6:00 | Teach 2: **running the paper grid**: what to record each check (fills, completed pairs, fees, touches, breaks) | **ADD** |
| 6:00–6:45 | Teach 3: paper vs real (fills, slippage, emotions) | **ADD** |
| 6:45–8:00 | Worked example: a two-week paper journal | **ADD** |
| 8:00–9:00 | Teach 4: the graduation rule, the first rung of the scaling ladder | **ADD** |
| 9:00–9:45 | Common mistake: accepting defaults; skipping paper because "it's only small" | KEEP 012 + ADD |
| 9:45–10:30 | If the screen differs, translate or stop | KEEP 019 |
| 10:30–11:15 | What you do next: set up the paper grid, stop before confirm on any real screen | KEEP 014 |
| 11:15–12:30 | Recap, outro | KEEP |

- **New visuals:** BP07-V01 to V05.
- **Self-check:**
  1. The form shows "Grids: 20". Is that lines or gaps, and how do you check?
  2. Name three things you record at every paper check.
  3. What must be true before you move from paper to real money?
- **What changes:**
  - ADD the screen-demo walkthrough (first use of the kit in the course), the paper-run record, paper vs real, the worked journal and the graduation rule.
  - Fix 003 and 020 (known FAILs).
- **Additions summary:** screen demo +1:30, paper run +1:30, paper vs real +0:45, worked journal +1:15, graduation +1:00. **About +6:00, from about 6:30 to about 12:30.**
- **Script brief:**
  - The screen is a fake or demo screen captured with `capture_demo.js`, then blurred and passed with `screen-demo-kit` (no balances, keys or account numbers).
  - No exchange name or logo.
  - Every field is said as "the form calls it X; your page calls it Y".

---

### BP-08 · Managing and monitoring

- **Current:** not rendered. Plan: 17 shots, about 850 words, **est. 6:00–7:00**; 20 JSON beats.
- **Target runtime: 12:30**
- **Moves toward the outcome:** the weekly check and the journal produce the evidence that decides every "add, hold or cut" scaling step. Drawdown is introduced here.
- **Objectives:**
  1. Run the three-row check (inside, side, sentence) on a chosen schedule.
  2. Record a weekly journal entry, separating grid income from the change in coin value.
  3. Measure drawdown, and know when to adjust vs stop.
- **Prerequisites:** BP-01 to 07.
- **New terms:**

| Term | Plain-English definition |
|---|---|
| cadence | already in the script, keep |
| alert | already in the script, keep |
| realised | money locked in by completed pairs |
| unrealised | the value change of coin you still hold, not yet sold |
| drawdown | how far the total has fallen from its highest point, as a percent |
| re-centre | stop and rebuild the band around a new range, only by written rule |
| record keeping (tax) | keep dated records of every sell or swap; it can be a CGT event; general information only |

- **Worked example (EXAMPLE, A$):**
  - Week: 14 fills, 6 completed pairs at about A$1.80 net each, so **A$10.80 realised**.
  - Price slipped from 100 to 97, so the coin held is **down about A$24 unrealised**.
  - Week total **about −A$13**. "Grid income is not the whole result."
  - Drawdown: peak A$2,050 to now A$1,950 is about 4.9%.
- **Segment outline (12:30):**

| Time | Segment | Status |
|---|---|---|
| 0:00–0:40 | Open, disclaimer | KEEP |
| 0:40–1:20 | Hook: monitoring is a short list you finish, not a vigil | KEEP |
| 1:20–3:00 | Teach 1: three rows (inside, side, sentence), each defined | KEEP 004–007 |
| 3:00–3:45 | Cadence and alerts | KEEP 008/011 |
| 3:45–5:15 | Teach 2: **the weekly journal entry**: realised vs unrealised, fees, rules followed Y/N | **ADD** (replaces "no result row") |
| 5:15–6:30 | Worked example: the A$ week on a card (grid income vs total) | **ADD** |
| 6:30–7:45 | Teach 3: drawdown, defined and measured | **ADD** |
| 7:45–8:45 | Teach 4: adjust vs stop; re-centre only by written rule | **ADD** |
| 8:45–9:30 | Worked check on a path that starts inside and ends outside | KEEP 010 |
| 9:30–10:00 | Australian records note (CGT event, keep records, ATO or tax agent) | **ADD** |
| 10:00–10:45 | Common mistake: hovering; changing the plan mid-check; counting only grid income | KEEP 012/013, ADJUST |
| 10:45–11:15 | What you do next: build the card plus a journal row and run it once | KEEP 014 |
| 11:15–12:30 | Recap, outro | KEEP |

- **New visuals:** BP08-V01 to V05.
- **Self-check:**
  1. Why can a week with six completed pairs still be a loss?
  2. Peak A$2,050, now A$1,950: what is the drawdown?
  3. After the three rows, what are the only two things you do?
- **What changes:**
  - **REVERSE "no result row"**: a result row is now a *review record* (realised, unrealised, fees, rules followed), never a target. Flag for Stewart.
  - ADD the journal, drawdown, adjust vs stop and the tax-records note.
  - FIX "the middle line, the middle line" (#5, #20) and the lower-case sentence start (#10).
  - Remake the title and disclaimer cards as code-drawn ("MANAGINGMONITORING" fail).
- **Additions summary:** journal +1:30, worked week +1:15, drawdown +1:15, adjust vs stop +1:00, tax note +0:30. **About +5:30, from about 7:00 to about 12:30.**
- **Script brief:** realised vs unrealised is shown as two buckets of the same total. Drawdown has its formula on a card. Say: "Lesson 10 uses this number to decide when you must scale down."

---

### BP-09 · Common mistakes

- **Current:** not rendered. Plan: 17 shots, about 840 words, **est. 6:00–7:00**; 21 JSON beats.
- **Target runtime: 12:00**
- **Moves toward the outcome:** the viewer can recognise the plan and scaling mistakes that wipe out accounts (oversizing, revenge adding, correlated bots) before learning the scaling rules.
- **Objectives:**
  1. Audit a page for the six existing mistakes.
  2. Recognise four scaling mistakes in worked case studies.
  3. Fix one miss at a time.
- **Prerequisites:** BP-01 to 08.
- **New terms:**

| Term | Plain-English definition |
|---|---|
| oversizing | one bot holding too much of the account |
| revenge adding | putting more money in to win back a loss |
| correlation | two coins that tend to move together, like BTC and ETH |
| chasing the band | moving the band down again and again after breaks |

- **Worked case studies (EXAMPLE):**
  1. **Grid in a trend:** Oct 2023 to Mar 2024. The band is left in days; mostly cash, watching price rise.
  2. **Gaps under fees:** 0.15% gap, −A$0.05 per pair.
  3. **Oversizing:** 60% of a A$10,000 account in one bot; loss at stop about A$750 (7.5% of the account) instead of about A$249.
  4. **Revenge adding / chasing:** after the stop, money is doubled into a lower band; the loss repeats.
- **Segment outline (12:00):**

| Time | Segment | Status |
|---|---|---|
| 0:00–0:40 | Open, disclaimer | KEEP |
| 0:40–1:20 | Hook: mistakes are pages, not personalities | KEEP |
| 1:20–3:30 | Teach 1: the six existing misses (blank stop, tight band, ending early, lines vs gaps, default size, result language), one picture each | KEEP 004–009 |
| 3:30–4:30 | Case 1: grid in a trend (real window, closes only) | **ADD** |
| 4:30–5:15 | Case 2: gaps under fees | **ADD** |
| 5:15–6:30 | Case 3: oversizing (A$ card) | **ADD** |
| 6:30–7:45 | Case 4: revenge adding / chasing the band | **ADD** |
| 7:45–8:30 | Correlation: BTC and ETH bots are not two separate risks | **ADD** (bridge to BP-10) |
| 8:30–9:30 | Worked audit of a sample page | KEEP 010 |
| 9:30–10:00 | One fix at a time; the audit is not a grade | KEEP 011/012 |
| 10:00–10:45 | What you do next: audit your own page | KEEP 014 |
| 10:45–12:00 | Recap, outro | KEEP |

- **New visuals:** BP09-V01 to V05.
- **Self-check:**
  1. Why is a grid in a strong trend a mistake?
  2. 60% of the account in one bot: what happens to the loss at stop?
  3. Why don't a BTC bot and an ETH bot halve your risk?
- **What changes:**
  - ADD four scaling case studies and correlation.
  - Replace "wick" on the line-chart caption and lower third (#12).
  - Remake the disclaimer chips, empty title card and illegible labels (known FAILs) as code-drawn cards.
- **Additions summary:** 4 cases +4:00, correlation +0:45, trims −0:15. **About +5:00, from about 7:00 to about 12:00.**
- **Script brief:** each case follows the same four lines: what they did, what happened (EXAMPLE), which rule would have stopped it, and the lesson that teaches that rule. No blame language.

---

### BP-10 · Scaling up on spot  (core of the series outcome)

- **Current:** not rendered. Plan: 17 shots, about 940 words, **est. 6:30–7:30**; 21 JSON beats.
- **Target runtime: 14:00**
- **Moves toward the outcome:** this **is** the outcome's core. The viewer learns the written rules to grow, or shrink, capital allocated to bots step by step.
- **Objectives:**
  1. Size a bot with two written caps (share of account, and loss at stop as a share of account).
  2. Add capital only after a rule-based review, one step at a time, and check that the step still fits the caps.
  3. Run more than one bot under a total risk cap, counting correlated bots together.
  4. Apply drawdown limits and scale-down triggers.
  5. Keep the journal that proves each step.
- **Prerequisites:** BP-01 to 09, especially BP-06 (loss at stop) and BP-08 (journal, drawdown).
- **New terms:**

| Term | Plain-English definition |
|---|---|
| scaling | growing the money given to bots step by step under written rules; never a promise of results |
| allocation | the money assigned to one bot |
| position sizing | deciding the allocation from written caps |
| risk per bot | loss at stop ÷ account |
| total open risk | all bots' losses at stop added together |
| review gate | the written test that must pass before adding money |
| scale step | the fixed amount you may add after one passed review |
| scale down | cut allocation by rule |
| buckets | separate money per bot (keep) |

- **Worked example (EXAMPLE rule set, A$10,000 account; teaching numbers, not advice):**
  1. **Size caps:** each bot at most 20% of the account (A$2,000), **and** loss at stop at most 2.5% of the account (A$250). The BP-06 bot (A$2,000, loss at stop about A$249) fits.
  2. **Review gate (to add):** at least 30 days or 20 completed pairs; every weekly check done; rules followed every time; journal complete; regime still fits; no drawdown limit hit.
  3. **Scale step:** +25% of that bot (A$500), then re-check the caps. At A$2,500 the loss at stop becomes about A$311, which is **3.1%**: **it fails**. The step only fits once the account has grown to about A$12,440, or the band and stop are re-planned and re-tested on paper. *The rule decides, not the feeling.*
  4. **Multiple bots:** total open risk at most 6% of the account (A$600). Correlated bots (BTC and ETH) count as one bucket for the cap. Two independent A$2,000 bots use about A$498 of the A$600.
  5. **Drawdown limits:** account down 10% from its peak (A$10,600 to A$9,540) means halve every allocation. Down 15% means stop all bots and go back to paper until a full review passes.
  6. **Scale-down triggers:** regime turns to trend or break; two band breaks in a month; any rule broken; the journal falls behind.
  7. **Journal:** every step is logged (date, bot, old to new allocation, which review passed, caps checked).
- **Segment outline (14:00):**

| Time | Segment | Status |
|---|---|---|
| 0:00–0:40 | Open, disclaimer | KEEP |
| 0:40–1:30 | Hook: scaling means more written pages and bigger buckets, earned by reviews, not a bigger number from a feeling. Define scaling plus the no-promise line. | KEEP 001 + ADD definition |
| 1:30–3:30 | Teach 1: **sizing caps** (share of account plus loss-at-stop share), worked on the BP-06 bot | **ADD** |
| 3:30–5:00 | Teach 2: **the review gate** (journal evidence, regime, rules followed). Same size is allowed (keep 006). | **ADD** + KEEP 006 |
| 5:00–6:30 | Worked example: **the scale step that fails the cap**, and the two lawful options | **ADD** |
| 6:30–8:00 | Teach 3: **multiple bots**: second page repeats the gates (keep 004), buckets (keep 005), correlation (keep 013), total open-risk cap | KEEP + **ADD** cap |
| 8:00–9:30 | Teach 4: **drawdown limits** and **scale-down triggers** | **ADD** |
| 9:30–10:30 | **The scaling ladder** (motion): paper → small real bot → review → +1 step → second bot → … with the down arrows | **ADD** |
| 10:30–11:15 | Spot only; one change at a time | KEEP 007/010 |
| 11:15–12:00 | Common mistake: doubling because the first page felt fine; adding after a loss | KEEP 012 + ADD |
| 12:00–12:45 | What you do next: write your own caps, review gate, step size, drawdown limits and journal columns, all marked EXAMPLE until reviewed | ADJUST 014 |
| 12:45–14:00 | Recap, outro | KEEP pattern |

- **New visuals:** BP10-V01 to V07.
- **Self-check:**
  1. With a 2.5% loss-at-stop cap on A$10,000, can a bot with a A$311 loss at stop run?
  2. Name four things the review gate checks before you add money.
  3. The account falls 15% from its peak. What does the EXAMPLE rule say to do?
- **What changes:**
  - **REVERSE** "The page does not tell you how much money to assign" and "size not filled by the course". The lesson now teaches a *method* for sizing with EXAMPLE caps, not a recommended amount. Flag for Stewart's yes.
  - ADD sizing, the review gate, the failing scale-step example, the total risk cap, drawdown limits, scale-down triggers, the ladder and journal logging.
  - FIX the 2024 low and high spoken over a close-only line (#5, #10, #13). Trim the BP-10 #16 number run.
  - Remake title and disclaimer cards as code-drawn.
- **Additions summary:** definition +0:30, sizing +2:00, review gate +1:00, worked fail +1:30, risk cap +0:45, drawdown and triggers +1:30, ladder +1:00, trims −0:45. **About +7:00, from about 7:00 to about 14:00.**
- **Script brief:**
  - Every rule is said as "EXAMPLE rule" and shown on a rules card.
  - Every sum is on screen.
  - Say "This is a method for deciding, not advice on how much to put in."
  - Use buckets for multiple bots.
  - End by previewing the capstone in Lesson 11.

---

### BP-11 · Advanced: liquidation scenarios  (final lesson + capstone)

- **Current:** not rendered. Plan: 17 shots, about 910 words, **est. 6:00–7:00**; 20 JSON beats.
- **Target runtime: 13:00**
- **Moves toward the outcome:** the viewer sees why leverage breaks the scaling rules (opt-in part). Then the **capstone** delivers the series outcome explicitly: the complete grid bot plan plus written scaling rules, explained back.
- **Objectives:**
  1. *(opt-in)* Explain liquidation, and isolated vs cross margin, without using a multiple, loss first.
  2. Explain why the course scales on spot only.
  3. **Series outcome:** lay out a complete grid bot plan (regime, range, gaps vs fees, entry/exit/stop action, loss at stop, paper and graduation, weekly check, journal) and the written scaling rules (caps, review gate, step, multiple bots, drawdown limits, scale-down). Explain each in plain English.
- **Prerequisites:** BP-01 to 10.
- **New terms:**

| Term | Plain-English definition |
|---|---|
| liquidation, margin, isolated, cross, funding | keep the existing definitions; isolated = one bucket, cross = buckets joined (no fence) |
| capstone | your whole plan on one page |

- **Worked example (EXAMPLE):**
  - The crash: 11 Mar 2020 close 7,911 to 12 Mar close 4,971, about −37% close to close.
  - A spot holding is still held (down in value). A contract can be closed by the venue.
  - Capstone: the A$10,000 EXAMPLE plan card from BP-01 to 10, filled in row by row.
- **Segment outline (13:00):**

| Time | Segment | Status |
|---|---|---|
| 0:00–0:40 | Open, disclaimer | KEEP |
| 0:40–1:20 | Hook: opt-in, losing path first. "If you skip the opt-in part, jump to the chapter 'Your complete plan'." | KEEP + ADD chapter pointer |
| 1:20–3:00 | Teach 1: what liquidation means; spot is complete without it | KEEP 004/005/006 |
| 3:00–4:15 | Teach 2: isolated vs cross as **buckets**; funding; no multiple | KEEP 007–010, ADJUST wording |
| 4:15–5:00 | Worked path: the 2020 drop with **closes** (about −37%) | ADJUST (fix #5/#12/#16) |
| 5:00–6:00 | Teach 3: **why the course scales on spot only**: leverage turns the loss at stop into a forced close and breaks the caps | **ADD** |
| 6:00–6:30 | Two flags; not a venue guide; skipped on purpose | KEEP 012/013/019 |
| 6:30–10:30 | **Capstone, "Your complete plan":** walk the one-page plan, one row per lesson (BP-01 to 10), on the EXAMPLE card; then the scaling rules card | **ADD** |
| 10:30–11:30 | **Series outcome explain-back:** five questions the viewer answers aloud (why it earns, when it stops, what you do, how big, when you add or cut) | **ADD** |
| 11:30–12:00 | What you do next: keep paper until your graduation rule passes; review weekly; scale only by your written rules | **ADD** |
| 12:00–13:00 | Course recap and final outro (no "next lesson"; series end card) | ADJUST 020 |

- **New visuals:** BP11-V01 to V05.
- **Self-check (series):**
  1. In one sentence, why can a grid earn, and when does it lose?
  2. What are your two sizing caps, and what has to pass before you add money?
  3. At what drawdown do you halve allocations, and when do you stop all bots?
- **What changes:**
  - ADD the spot-only rationale, the 4-minute capstone, the series explain-back and the series end card.
  - REPLACE "isolated fence" with buckets.
  - FIX the 13 Mar low spoken over the line chart: switch to closes, about −37%.
  - FIX the lower-case sentence start (#10).
  - Remake the "LIQUIDATION SCENES" title as code-drawn.
- **Additions summary:** spot-only +1:00, capstone +4:00, explain-back +1:00, next steps +0:30, minus about 0:30 trimmed. **About +6:00, from about 7:00 to about 13:00.**
- **Script brief:** keep the opt-in part tight and loss-first. The capstone is a calm walk-through of the plan card, one row at a time, each row naming its lesson. The last spoken line is the series outcome plus the disclaimer.

**OPTIONAL reorder (flagged, not recommended now):** the series ends on an opt-in leverage topic, which weakens the final-lesson outcome. The plan above fixes this with the capstone, without moving anything. If Stewart prefers, swap BP-10 and BP-11 so scaling plus the capstone is the last lesson. That would change the "NEXT" cards on BP-09 to 11 and the course map in BP-01.

---

## 7. Runtime summary

| Lesson | Current | Added | Target |
|---|---|---|---|
| BP-01 Introduction | 7:19 (film) | +5:10 | **12:30** |
| BP-02 What you are going to need | 7:23 (film, old) | +5:00 (after trims) | **12:00** |
| BP-03 What is a grid bot | 6:30 (film, old) | +5:30 | **12:00** |
| BP-04 Market regimes | est. 6:00–7:00 | +5:00 | **12:00** |
| BP-05 Choosing grid spacing and range | est. 5:30–6:30 | +6:00 | **12:00** |
| BP-06 Entry and exit rules | est. 6:00–7:00 | +5:30 | **12:30** |
| BP-07 Spot paper trading | est. 6:00–7:00 | +6:00 | **12:30** |
| BP-08 Managing and monitoring | est. 6:00–7:00 | +5:30 | **12:30** |
| BP-09 Common mistakes | est. 6:00–7:00 | +5:00 | **12:00** |
| BP-10 Scaling up on spot | est. 6:30–7:30 | +7:00 | **14:00** |
| BP-11 Advanced: liquidation + capstone | est. 6:00–7:00 | +6:00 | **13:00** |

All targets sit inside 10–15 minutes, with at least 1 minute of headroom each side. The first real render of each lesson will be measured, and any lesson under 10:00 or over 15:00 is fixed before moving on.

## 8. Decisions needed from Stewart

1. **Colour:** strict navy, cyan and white (recolour amber, mint and blue), or keep one warning colour. Mint reads as teal.
2. **Brand spelling:** "GridBot Builder" (rule) vs "Grid Bot Builder" (current wordmark and voice).
3. **BP-08 and BP-10 reversals:** a result row as a review record, and EXAMPLE sizing caps. These replace the current "no result row" and "page does not tell you how much money to assign".
4. **Optional:** swap BP-10 and BP-11.
5. **Tool changes:**
   - gate profile 600–900 s
   - 5% margin
   - palette lint
   - screen-demo kit wired into `studio.py`
   - numbers YAML for BP-04 to 11
   - one script source per lesson in `studio.py`
