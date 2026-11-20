# GridBot Blueprint expansion: consolidated fix list

Prepared 16 Nov 2026, about 9:00am WITA (12:00pm AEDT). Read-only consolidation; nothing changed in the repo and nothing sent.

**Sources:** [01] YouTube Producer (script and pacing) · [02] Creative Studio (image fit and sync) · [03] Crypto Research (facts) · [04] Tax Accounting (tax and AUSTRAC) · [05] External Comms (brand and consistency) · [06] Grok Bot (scoring and FLAGs).

**Severity:**
- **blocking:** must be done before that lesson renders. A series row blocks every lesson.
- **should:** fix in the same script pass.
- **nice:** optional polish.

**Owners:**
- **Cursor:** bc-f8dcc94a. Scripts, `studio.py`, gate and tooling, code-drawn cards. New and remade stills come from image agent bc-6781931a.
- **Creative Studio:** scores and re-scores stills, palette and image fit.
- **Grok Bot:** curriculum, word budgets and verification.

Items that need Stewart's yes first carry **[FLAG Sx]**, which points to FLAGS_FOR_STEWART.md.

## Source SHA note (affects several findings)
Reports [03] and [05] read the **stale local ref 5d59cf0** (13 Nov). Reports [01], [02] and [06] read the live head **962465c** (15 Nov). I re-checked the stale-only findings at 962465c:

| Finding | At 962465c | Resolution |
|---|---|---|
| [05] F2: "Market Pros" in the BP-07 legal line | **Not present** | Closed. Keep a regression grep (fix 8). |
| [05] variant B disclaimer "Educational content only… Trading involves risk" | **Not present.** `studio.py` now speaks the Australian block plus three risk lines. JSON and `lesson_scripts.legal()` carry a second text ("Crypto carries a risk of total loss… doesn't consider your objectives, financial situation or needs…"). | Drift is real but down to two variants. Fix 6. |
| [03] B1: BP-03 "one side can be left holding inventory" (wrong side) | **Removed** | Closed. Re-check after the rewrite. |
| [03] B2, B3, M1: `walk()` speaks the summer rungs over the 2020, 2023 rally and 2024 windows | `walk()` is **still defined** with hard-coded rungs, but **no builder calls it**, so nothing is spoken | Not live. Delete or fix the dead code (fix 14) so it can't come back. |
| [05] fence in BP-01 and the BP-11 recap; electric blue `#1E5EFF` in prompts | **Still present.** BP-01 JSON beat 15 and the "The fence" shot; BP-11 recap "isolated fence"; 19–20 `#1E5EFF` hits per JSON file | Valid. Fixes 9 and 10. |

## Conflicts between reports, and how they're resolved

| # | Topic | Reports | Resolution |
|---|---|---|---|
| C1 | BP-01 EXAMPLE pair (buy 27,630, sell 28,531, net US$8.45) | [01], [02] and [03]: the arithmetic is correct. [06]: the pair **never completed on daily closes** in the window. Price fell through 28,531 on 17 Aug, and no close came back above it (the 16 Oct close was 28,519.47). | **Both are true.** The maths is right, but presenting it on the real path implies something that didn't happen. **Use 26,730→27,630:** buy filled on the 17 Aug close, sell filled on the 29 Aug close. Numbers: 0.01 BTC, US$267.30 → US$276.30, gross US$9.00, fees US$0.27 + US$0.28 = US$0.54, **net ≈ US$8.46**. Speak "about eight and a half dollars", which also fixes [03] m3's rounding note. If Stewart wants to keep the original pair, label it "illustration, not a fill that happened". Fix 20. |
| C2 | BP-10: account size at which the +25% step fits | [01] and the plan: A$12,440. [03] and [06]: A$12,500. | **A$12,500.** The 20% size cap binds first (2,500 ÷ 0.20). Also, the +25% step breaks the 20% cap at A$10,000 (it would be 25%), not only the 2.5% loss cap. Fix 56. |
| C3 | Narration rate | The brief said about 150 wpm. [01] and [06] measured BP-01 v8 at 161.5 wpm overall (202 continuous speech). [02] used 150 for still timing. | **Use 160 wpm** for budgets. Re-measure on the first render. |
| C4 | Disclaimer wording | [01] F-ALL-1 offers the brief's "Educational content only…" as an option. [05] says the canonical block is the CURRICULUM §5.2 Australian wording. [04] says keep it, plus a "not tax advice" line in the tax segments. | **Stewart decides (S1).** Recommendation: [05]'s canonical block verbatim, with the tax add-on in BP-02 and BP-08 only. |
| C5 | "Number of grids" | Plan: "lines or gaps". BP-07 script: "seven was the line count". [03]: on common forms it means **gaps** (spread = (upper − lower) ÷ grids). | **[03] is right:** grids = gaps, lines = grids + 1, and tell learners to check their exchange's help page. Fixes 31 and 47. |
| C6 | Crash figure | BP-04 and BP-11 scripts: close to the 13 Mar low, −48%. Plan: closes, −37%. [03] M6: liquidation happens intraday, so −37% understates it. | **−37% (11→12 Mar closes)** on every line chart. **−48% only on a labelled 13 Mar candle card** ("intraday low"), used in BP-11 to explain forced closes. Fixes 40 and 62. |
| C7 | Trend vs break vs range | Plan: trend = higher highs and higher lows. Script: three different definitions ([01]). [05]: "range" collides with the grid range. [06]: "break" equals BP-01's stop definition. | One glossary: **trend** = a path that keeps moving one way over weeks; **break** = a sudden big move out of the band in a day or two (Mar 2020); **range regime / ranging market** in BP-04, never a bare "range". Script lines change, so this is **FLAG S20**. Fix 38. |
| C8 | Remake notes that are already done | VISUALS: fix BP-05 006 maths; remake BP-03 009/011/014; fix the BP-09 005 wick caption. [02]: all of these are already correct or clean at 962465c. | **Don't remake.** Drop those notes from VISUALS (fix 18). |
| C9 | Recolour count | [06] (from Creative Studio's notes): 18 amber, 6 mint. [02] (pixel scan): 3 mint, 32 amber, 11 blue. | **Use [02]'s list.** Fix 10. |
| C10 | KEEP still count | VISUALS totals: 161. [02]: 164. | Count 164. Fix 18. |
| C11 | BP-04 to 11 baseline runtime | [06] warned the 6–7 min estimates might be inflated. [01] ran `studio.plan()`: 1,000–1,126 spoken words now (6.3–7.0 min). | **[01]'s measured baseline stands.** The real risk is the `studio.py` clip caps (fix 2) and the padding cuts, not the baseline. |

## Fix list

### Series-wide (block every lesson)

| # | Severity | Exact fix | Owner | Source |
|---|---|---|---|---|
| 1 | blocking | **One script source per lesson**, with stills re-chaptered so each plays inside its teaching section in B5 order (hook → teach → worked example → common mistake → next → recap). This ends the appended still block before the recap, including BP-01's second "Hook". [FLAG S3] | Cursor | [01] F-ALL-8, [05] F7, [06] |
| 2 | blocking | **Lift or work around the `studio.py` caps**, which silently cut added teaching: `clip_vo(vo, 4, 80)` on stack, analogy and worked shots; 80 words on still lines; `key_stops` 3 sentences / 48 words on runs of 6+ chart shots. Either write new teaching as more shots of ≤4 sentences and ≤80 words, or change the caps (a tool change). | Cursor | [01] |
| 3 | blocking | **Word-count gate before render**, at 160 wpm. Target 1,920–2,240 words (12–14 min); floor 1,600; ceiling 2,400. BP-10 ≤ about 2,300. Correct the curriculum's "Additions summary" totals: BP-01 +4:30 (not +5:10); BP-03 +4:45 (not +5:30); BP-05 +4:45 (not +6:00); BP-06 +5:15 (not +5:30); BP-09 +4:30 (not +5:00); BP-10 +7:30 (not +7:00). Words to add per lesson are in [01]'s table (+739 to +920 for 12:00). | Grok Bot (budgets), Cursor (gate) | [01], [06] |
| 4 | blocking | **Gate and tool changes:** `blueprint` length profile 600–900 s; 5% safe-margin OCR; palette lint (navy, cyan and white only; fail on amber, mint, teal, blue `#1E7BFF`/`#1E5EFF`, green, orange, yellow); screen-demo kit `cli.py qa` wired into `studio.py` for every `kind: screen` shot (BP-02, 03, 07). | Cursor | BASELINE, [02], [05], [06] |
| 5 | blocking | **Captions:** decide how the 5% caption margin is guaranteed. Sidecar VTT isn't burned in. Either burn in captions, or set the VTT `line`/`position` cues inside 5% and test in the target player. | Cursor | [02], [06] |
| 6 | blocking | **One disclaimer text**, spoken and shown in full in every lesson, with no mid-sentence caption crop. Replace the second variant in JSON and `lesson_scripts.legal()`. Add-on lines only as separate sentences, used the same way every time. [FLAG S1] | Cursor | [05] F1, [01] F-ALL-1 |
| 7 | blocking | **Brand:** "GridBot Builder" on the wordmark, open card, captions and ident; course title "GridBot Blueprint". The spoken ident must say the **exact lesson title**. Two don't today: BP-05 says "Spacing and range" (title "Choosing grid spacing and range"), and BP-11 says "Liquidation, as a public path" (title "Advanced: liquidation scenarios"). Remake the wordmark crop and any still that bakes in "GRID BOT BUILDER". | Cursor, Creative Studio | [05] F3, [06] (ident check 962465c) |
| 8 | blocking | **Compliance grep before every render:** no "Market Pros", ABN, entity or personal names, no exchange names, no URL/path/hash spoken, no "DeFi" in the legal text, and no "we run/operate the bot" lines (the BP-07/08 rule). | Cursor | [05] F2/F16, Stewart's rule |
| 9 | blocking | **Scrub the fence** (decided). Retire `analogy-fence.png`, the `range-2023/the-fence` chart, BP-01 still 015 and the "The fence" shot. Also the BP-02 prompt "fence around a generic form labelled Paper", the BP-11 007 prompt and the 015 recap "isolated fence", and every "rail/rails" (17 uses: BP-01 18; BP-05 11, 12, 15, 27; BP-09 12, 17; BP-10 10). Use ladder rungs, L-plates and buckets. [FLAG S4 for the replacement lines] | Cursor, Creative Studio | [01] F-ALL-4, [02], [05] F8–F10 |
| 10 | blocking | **Recolour** (decided) to navy, cyan and white. **Mint:** BP-01 007; BP-03 008, 010. **Amber:** BP-01 004, 008, 009, 012; BP-02 006, 007, 009, 011, 015, 017; BP-03 001, 004, 010, 012, 013, 015, 018; BP-04 019; BP-05 001, 007, 008, 009, 012, 018 (plus the 011 down-candles); BP-06 001, 009, 011, 015; BP-07 007, 012, 013, 015. **Blue:** BP-01 007; BP-02 001, 011, 018; BP-03 008, 010, 016, 017; BP-05 004, 018; BP-06 004. Also the `studio.py` AMBER/MINT/BLUE constants, the dark-green chip, the leave-motion $/C key and amber chapter-title frames. Strip `#1E5EFF` from every JSON prompt. Buys solid cyan, sells outlined white, stop white dashed with a cyan warning icon. Creative Studio re-scores every recoloured still. | Creative Studio (re-score), Cursor (studio and prompts), bc-6781931a (stills) | [02], [05] F4/F5, [06] |
| 11 | blocking | **Stop rule, one version:** "a daily close outside the band, through the top **or the bottom**, and the next daily close still outside", then the action (stop the bot, which cancels the waiting orders; keep the coin or swap to cash, as written in advance) and who does it. Explain that a bot's automatic stop-loss is a **price** trigger that can fire intraday, unlike the close rule. Applies to BP-01, 02, 06, 08, 09 and 10. [FLAG S5] | Cursor, Grok Bot | [01] F-ALL-7, [03] M4, [06] |
| 12 | blocking | **20-second visual-change plan:** give every KEEP still a segment id. Write a cut list for every segment over 20 s (about 100 of 121). Each CARD/MOTION brief must state its change cadence (row by row, tick by tick). Use script-beat anchors, not clock times, because runtimes will move. | Grok Bot (anchors), Creative Studio (cut list check) | [02], [06] |
| 13 | should | **Daily-close definition:** "cut at 00:00 UTC: 11:00am AEDT in daylight saving, 10:00am AEST otherwise". Note that the July–Sep 2023 house window closes were 10:00am AEST. Fix the BP-01 term table and the V06 chip "11am AEDT". | Cursor, Grok Bot | [03] M10, [06] |
| 14 | should | Delete the unused `walk()` generator in `lesson_scripts.py` (hard-coded 27,630 / about 900 rungs), or make it derive rungs, middle and gap from each window. | Cursor | [03] B2/B3/M1 |
| 15 | should | **Lock the glossary** across all 11 ([05] §4): band = grid range (synonym introduced once in BP-01); exchange (not venue or app); bucket (not box); stop (finish rule and exit introduced once as synonyms); level = a price, not an order. | Cursor, Grok Bot | [01] issue 5, [05] F12 |
| 16 | should | **Outcome wording, no growth claim:** reword the series promise and the BP-01/recap line "grow the money you give to bots" and "why a grid earns". [FLAG S2] | Grok Bot | [03] M11/m9, [04] #15, [05] F14/F15 |
| 17 | should | Cut the repeated JSON workbook scaffolding ("On the diagram for this beat, look for…", "The shapes are the lesson", "Say the opening line once more…"), keeping one short cue per beat. Cut the 150–190-word padded repeat blocks in BP-05 to 10, and sentences repeated 2–3 times in 10 of 11 lessons. [FLAG S6] | Cursor | [01], [05] F6 |
| 18 | nice | VISUALS.md hygiene: add BP01-V07 to the CURRICULUM BP-01 list; drop the stale remake notes (BP-03 009/011/014, BP-05 006 maths, BP-09 005 wick); KEEP total 164; fix the CURRICULUM cross-refs ("fix #9" should be #1/#2/#3); S6 target 12–14 min, not 12–13. | Grok Bot | [02], [06] |
| 19 | nice | Every "Next" outro adds one sentence naming the next lesson's skill (today BP-03 to 10 share an identical outro). [FLAG S7] | Cursor | [01] |

### BP-01 · Introduction

| # | Severity | Exact fix | Owner | Source |
|---|---|---|---|---|
| 20 | blocking | Swap the EXAMPLE pair to **26,730 → 27,630** (fills on the 17 Aug and 29 Aug closes): gross US$9.00, fees US$0.54, net ≈ US$8.46, spoken "about eight and a half dollars". Update BP01-V04, V05 and self-check Q2. (C1) | Grok Bot, Cursor | [06], [01]/[02]/[03] |
| 21 | blocking | Add the missing core teaching per [01] §7 (about 900 words): basics (crypto, exchange, order, buy/sell as swaps, bot); why a grid **can** earn (market stall plus pair card with fees and the losing case); bot vs you; stop, plainly; the **downside walk** (fall → all coin, value keeps dropping until the stop acts); common mistake; L-plates. | Cursor | [01], CURRICULUM |
| 22 | blocking | Remake still 012: "NO PROFIT PROMISES" becomes "NO PROMISE OF RESULTS". Recolour the amber X. [FLAG S8] | bc-6781931a, Creative Studio | [02], VISUALS |
| 23 | should | Remake the course map (still 010 / `paint_course_map`) with **every lesson named** through "Scaling up" and "Your complete plan". Give it its own slot with pauses, not a 60 s block shared with L-plates and the notebook. This is the repeated v3–v8 "map rushed" failure. | Cursor, bc-6781931a | [02], [06] |
| 24 | should | Still 003: relabel "Sell higher / Buy lower" to "Sell orders above / Buy orders below"; recolour the green dots. Its headline "INTRODUCTION TO GRID BOTS" differs from the title "Introduction": use the code-drawn title card on screen, or retitle the still. | bc-6781931a, Creative Studio | [02], [06] |
| 25 | should | The worked check and the speech say "Low 24,930 / High 30,331". Those are intraday extremes (11 Sep low; 23 Jul high) on a close-only chart. Say "bottom line / top line"; keep the figures on the card. [FLAG S9] | Cursor | [03] m1, [06] |
| 26 | should | The "leave the band" segment (7:00–8:30, 90 s) ran about 13 s in v8. Either give it real content (the downside walk, fix 21) with a cut list, or shrink it. | Grok Bot | [02], [06] |
| 27 | should | BP01-V04: draw the "Pairs 1, 2, 3, 4" illustrative loop on a blank ladder, not the real summer chart. On closes the summer window completed only **3** one-rung pairs, and 3 parcels were still held at the end. Qualify "many small pairs". | Cursor | [06] |
| 28 | nice | Candle card: the data has no open price. Keep "a simple candle showing high, low and close", or derive the open from the prior close and label it. | Cursor | [06], earlier watches P11 |

### BP-02 · What you are going to need

| # | Severity | Exact fix | Owner | Source |
|---|---|---|---|---|
| 29 | blocking | BP02-V04 journal row: "BTC/AUD, band 24,930–30,331" uses US$ prices. Make it BTC/USD (the course's data), or convert with a labelled rate and date. | bc-6781931a, Creative Studio | [06], [03] (no AUD/USD rate anywhere) |
| 30 | blocking (before render) | Journal tax columns: for every buy, sell or swap, record date and time, amount, **A$ value at the time**, fee, exchange or wallet, and purpose. Export exchange history regularly (the ATO suggests at least every 3 months). Record wallet **addresses**, but keep keys off the page. | Cursor, bc-6781931a | [04] #1, #14 |
| 31 | should | AUSTRAC lines: "Crypto exchanges offering services in Australia must be registered with AUSTRAC (as a virtual asset service provider). You can search AUSTRAC's public register by legal name or ABN. Registration is not an endorsement and doesn't mean your money is protected." Show the check generically with the screen-demo kit. ID check: "under Australia's anti-money-laundering law… only upload ID inside the exchange's own app". Optional: ASIC licensing of exchanges starts 9 Apr 2027. | Cursor | [04] #4, #5, #11, #12; [03] m5; [06] |
| 32 | should | Recap still 019 ("SAY THREE THINGS") doesn't recap the new content. Remake it to cover page, account, pair, fees, journal and no secrets. Still 013 "YOU ARE AT THE START" needs named steps or should be dropped. | bc-6781931a, Creative Studio | [02] |
| 33 | should | Teach 1 (1:20–3:00, 100 s) has no visual plan: assign 004/005/007/009 with cuts under 20 s. | Grok Bot | [02] |
| 34 | should | Script fixes: chapter "Seven lines" → "Seven items"; "three words… which come next" → "from lesson one"; move the order definition to BP-01; cut the duplicate EXAMPLE sentence; replace the "Empty pair" lines. [FLAG S10] | Cursor | [01] F-02-1…6 |
| 35 | nice | Fee wording: "a gap smaller than the 0.2% round trip loses money before price moves" (a gap exactly equal to it only breaks even). | Grok Bot | [06] |

### BP-03 · What is a grid bot

| # | Severity | Exact fix | Owner | Source |
|---|---|---|---|---|
| 36 | should | "Number of grids" glossary: "on most grid forms, the number of **gaps**; price lines = grids + 1; check your exchange's help page" (C5). Add that the 3 sell orders need coin bought at the start (about A$300), so a mid-band start is about half coin and half cash. | Grok Bot, Cursor | [03] M3, m6 |
| 37 | should | BP03-V02 mixes a US$ band (30,331 / 24,930) with "Amount A$600": make the currency consistent. Sequence V02 (5:00–5:45) then V03 (5:45–6:30). Pass 3 "on the real path" must show the honest close-based count. Bot vs you: "the **bot** places a sell one rung higher". Define "inventory" when first spoken. [FLAG S11] | Cursor | [06], [02], [01] F-03-2 |
| 37a | nice | Don't remake 009/011/014: they're already plain at 962465c (C8). Recolour 008/010 only. | Creative Studio | [02] |

### BP-04 · Market regimes

| # | Severity | Exact fix | Owner | Source |
|---|---|---|---|---|
| 38 | blocking | One set of regime definitions (C7). Say "range regime" or "ranging market" in BP-04, never a bare "range". [FLAG S20] | Grok Bot, Cursor | [01] F-04-2, [05] F12, [06] |
| 39 | blocking | BP04-V01 chip "4 touches each side" isn't supported. Define a touch threshold and recompute from closes: within one gap (900), 4 top and 3 bottom; within half a gap, 2 top and 1 bottom. | Cursor (Crypto Research to verify) | [06] |
| 40 | should | Crash: −37% on closes (11→12 Mar) on the line chart; −48% only on a labelled candle card (C6). Use one window throughout: the objectives today say "12 March" and "12 to 13 March". [FLAG S12] | Cursor | [01] F-04-1, [03] M5/m2 |
| 41 | should | Trend start: pick one figure (about 28 thousand on 1 Oct, or 33,086 on 23 Oct) and use it everywhere. Teach what the grid **does** in a trend (F-04-3). Use "volatility", which is planned but never spoken. | Cursor | [03] m8, [01] |
| 42 | should | Check the KEEP stills' on-image "weave" wording (001/004/008/011) against "A range bounces". Fix the JSON prompt copy-paste that drops the 19-gap picture into regime beats. | Creative Studio, Cursor | [05] F13, [06] |

### BP-05 · Choosing grid spacing and range

| # | Severity | Exact fix | Owner | Source |
|---|---|---|---|---|
| 43 | should | "A$2,000 ÷ 20 orders" conflicts with "20 lines = 19 gaps" and BP-03's rule (orders = lines − 1). Use 21 lines / 20 orders, or A$1,900 ÷ 19. Label the exchange minimum as EXAMPLE. Don't state a real minimum unless it comes from a named venue's help page, which the no-exchange-names rule rules out. | Grok Bot | [06], [03] unverified #1 |
| 44 | should | Define "spacing" (the lesson title) and "round trip" at first mention. Move the wrong-page recount after the 19-gaps teaching. Cut the 150-word padding. [FLAG S13] | Cursor | [01] F-05-1…6 |
| 45 | nice | Span: say which mode. Arithmetic (0.5% of the lower price) gives 9.5%; geometric gives 9.94%. Add "per 1 BTC, round trip" to the 55-dollar fee line. | Grok Bot | [03] m4, m11 |
| 46 | nice | No new still in BP-05. S9 is met by the KEEP stills, but add a unique hero illustration if Stewart means a new one. Drop "fix the 006 maths" (already correct, C8). | Grok Bot, bc-6781931a | [02], [06] |

### BP-06 · Entry and exit rules

| # | Severity | Exact fix | Owner | Source |
|---|---|---|---|---|
| 47 | blocking | Teach the downside stop, stop actions and loss at stop (today the only stop taught is the upside exit). Loss card: label 85 as "EXAMPLE exit price (the real exit is at or after the second close and can be worse)". Show fee lines A$1.00 + A$1.00 + A$1.76 = A$3.76; loss ≈ A$249 (12.4%). | Cursor | [01], [03] m7 |
| 48 | should | "Stop-loss price" (a bot's price trigger) vs the EXAMPLE two-close rule: teach both and say which one the plan uses. Rename "take-profit" to "upper exit", which avoids clashing with BP-02's "no profit target on the page". | Grok Bot | [06], [05] F15 |
| 49 | should | Stills 013 and 015 become "Sizing is Lesson 10" / "Amount: set in Lesson 10". Cut the 180-word and 65-word repeats. Recap "met on 23 October" (not "names 23 October"). [FLAG S14] | bc-6781931a, Cursor | [02], [01] F-06-1…4 |

### BP-07 · Spot paper trading

| # | Severity | Exact fix | Owner | Source |
|---|---|---|---|---|
| 50 | blocking | Fix the wrong form fact: "Form says 7 grids… seven was the line count" becomes "On most forms, 'grids' means gaps. Your page has 6 gaps (7 lines), so you enter 6. Check your exchange's help page." [FLAG S15] | Cursor | [03] M2 |
| 51 | blocking | Actually teach paper trading: define it; run it; what to record; paper vs real; the graduation rule. This needs the S16 decision on "pressing it is not the lesson, even on paper". | Cursor | [01], CURRICULUM |
| 52 | should | Worked journal: "9 completed pairs in 2 weeks" is far above the course's own real window (3 on closes in 90 days). Use a smaller, labelled EXAMPLE, and say real counts vary. "Rules followed 9/9" becomes "9 of 9 checks done on schedule". | Grok Bot | [06] |
| 53 | should | "venue" → "exchange"; "5x" → "five times" (TTS). Cut the 165-word repeat. [FLAG S16] | Cursor | [01] F-07-2…4, F-ALL-5 |

### BP-08 · Managing and monitoring

| # | Severity | Exact fix | Owner | Source |
|---|---|---|---|---|
| 54 | blocking | Week card numbers don't come from any course bot. On the BP-06 bot: about A$3.60 net per pair (6 pairs = A$21.58), and −A$30 unrealised on 10 coins (100→97). The week is about −A$8. Or state the order size, gap and coins that give A$1.80 and −A$24. Make drawdown per bot here and per account in BP-10 explicit. | Grok Bot (Crypto Research to verify) | [03] M8/M9, [06] |
| 55 | blocking (with S17) | Remake stills 012 ("DO NOT ADD A RESULT ROW") and **015** (recap chip "No result row"; missing from the VISUALS remake list), and adjust 009 ("Not a result chart"), to "a result row is a review record, not a target". Rename "grid income" to "completed-pair result" (or "realised result"), and add "your journal's realised number is not your tax figure". | bc-6781931a, Creative Studio, Cursor | [02], [06], [04] #7, [05] F15 |
| 55a | blocking (before render) | Tax records note in four beats: (1) disposals can be CGT events, including every fill on a coin-quoted pair (e.g. BTC/USDT, where buys are swaps too); (2) keep A$-valued records of every transaction for 5 years; (3) exchanges report data to the ATO, so records should match; (4) "General information, not tax advice; check ATO guidance or a registered tax agent." Add a neutral investor-vs-business caution here or in BP-10. | Cursor | [04] #2, #6, #8, #9 |
| 55b | should | "We do not operate an alert service" moves after the Alerts shot. Merge the cadence definitions. Cut the 164-word repeat. Explain "below the middle = more coin, above = more cash". [FLAG S17] | Cursor | [01] F-08-2…4 |

### BP-09 · Common mistakes

| # | Severity | Exact fix | Owner | Source |
|---|---|---|---|---|
| 55c | should | Draw a clear line between "re-centre by written rule" (BP-08) and "chasing the band" (BP-09). For the trend case, the band "left in days" was really about 3 weeks (1→23 Oct). Stop "rule for 23 October" becomes a condition (F-ALL-6). Cut the 152-word repeat and the third "blank stop" line. [FLAG S18] | Grok Bot, Cursor | [06], [01] F-09-1…4 |

### BP-10 · Scaling up on spot

| # | Severity | Exact fix | Owner | Source |
|---|---|---|---|---|
| 56 | blocking | Scale-step card: "+25% → A$2,500 = 25% of the account (cap 20%) ✗, and loss at stop ≈ A$311 = 3.1% (cap 2.5%) ✗. Fits only once the account is ≥ **A$12,500**, or after a re-plan and paper re-test." Better teaching: start the example bot below its cap (e.g. A$1,600) so one step can pass and the next fails. (C2) | Grok Bot, Cursor | [03] M7, [06] |
| 57 | blocking | Define the correlation rule exactly: "Bots on coins that move together count as **one bot** for both caps: their combined allocation ≤ 20% and combined loss at stop ≤ 2.5%; all bots together ≤ 6% total open risk." Note that most coins move with BTC. BP10-V05's three full-size bots (≈ A$747 > A$600) must be shown as a **fail**. | Grok Bot | [06], [03] m10 |
| 58 | blocking (with S19) | Remove still 011 ("NO MONEY AMOUNT ON THIS PAGE") and its beat from the script. Rework the 001 hook ("A SECOND PAGE, NOT A BIGGER NUMBER") or move it after V01. Update the "no money amount" recap. | Cursor, Creative Studio | [02], [01] F-10-1 |
| 59 | should | 2024 band spoken as about 57–73 thousand over a close-only line: use closes (about 58 to about 72 thousand) or a candle card. Say the leverage line once. Cut the 188-word repeat. [FLAG S19] | Cursor | [01] F-10-2…4 |
| 60 | nice | Review gate: change "30 days **or** 20 completed pairs" to "**and**", so 20 quick pairs in a few days can't open the gate. | Grok Bot | [06] |

### BP-11 · Advanced: liquidation scenarios (plus capstone)

| # | Severity | Exact fix | Owner | Source |
|---|---|---|---|---|
| 61 | blocking | Fix the accuracy line: isolated margin is "the exchange looks only at the **margin** you assigned to that position" (not the "inventory"). Buckets throughout (not box or fence). | Cursor | [01] F-11-3/F-11-4, [05] F10 |
| 62 | should | Show that liquidation triggers **intraday** on the live (mark) price, not at the daily close. Use the 13 Mar candle card (low 4,107, −48% from the 11 Mar close) next to the −37% closes line (C6). Note that spot bought with borrowed margin can also be liquidated. | Cursor | [03] M6, BP-11 note |
| 63 | should | Capstone: use **one** coherent EXAMPLE (one currency and one bot) across all rows, not BTC/US$ from BP-01–05 mixed with the A$ price-100 bot and the A$10,000 account. V03 needs a visible change at least every 20 s (12+ changes over 4:00). V04 cuts per question. 11:30–12:00 needs a visual. | Grok Bot, Cursor | [06], [02] |
| 64 | should | Speak "about 7,900 / about 5,000" (exact figures on the card). "venue" → "exchange". [FLAG S21] | Cursor | [01] F-11-2, F-11-5 |
| 65 | nice | One-line plain definition of "funding". Optional: "derivatives and margin may be taxed differently; ask a tax agent". | Cursor | [06], [04] missing #10 |

## Blocking count by owner (an item with two owners counts for each)

| Owner | Blocking items |
|---|---|
| **Cursor** (incl. bc-6781931a image work) | 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 20, 21, 22, 29, 30, 38, 39, 47, 50, 51, 55, 55a, 56, 58, 61 → **26** |
| **Creative Studio** | 7, 9, 10, 12, 22, 29, 55, 58 → **8** |
| **Grok Bot** | 3, 11, 12, 20, 38, 54, 56, 57 → **8** |
| **Unique blocking items** | **29** (12 series-wide, 17 lesson-specific) |
