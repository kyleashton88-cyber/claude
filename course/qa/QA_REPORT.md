# GridBot Blueprint expansion plan: consolidated QA report (BP-01 to BP-11)

Prepared 16 Nov 2026, about 9:00am WITA (12:00pm AEDT). Read-only. This merges six specialist reports in `/workspace/bp-qa/`:

| Ref | Report | Topic | Source SHA |
|---|---|---|---|
| [01] | 01-script-pacing.md, YouTube Producer | script and pacing | 962465c |
| [02] | 02-image-sync.md, Creative Studio | image fit and sync | 962465c |
| [03] | 03-facts.md, Crypto Research | facts | **5d59cf0, stale** |
| [04] | 04-tax-austrac.md, Tax Accounting | tax and AUSTRAC | plan docs |
| [05] | 05-brand-consistency.md, External Comms | brand and consistency | **5d59cf0, stale** |
| [06] | 06-scoring.md, Grok Bot | scoring and FLAGs | 962465c |

Findings from [03] and [05] were re-checked at the live head 962465c. These four don't reproduce, so they're treated as closed or regression checks:
- the Market Pros line
- disclaimer variant B
- the BP-03 "inventory" line
- the live `walk()` shots

Details are in FIXES.md (SHA note and conflicts C1–C11). Fix numbers below (#) refer to FIXES.md; S-numbers refer to FLAGS_FOR_STEWART.md.

## Scores

Scores are out of 10 for the plan as written, if built as specified. "Prior" is the scored average of the current films and scripts.

The columns are:
- Clar: first-timer clarity
- Acc: accuracy
- Pace: pacing and length
- Vis: visual fit and sync
- Brand: brand and compliance
- Out: delivers the series outcome

Adjusted from [06] using the other reports:
- **Brand:** −1 in every lesson. Disclaimer drift, `#1E5EFF` in every JSON prompt and fence remnants are all live at head [05]. BP-07 is not penalised for Market Pros, which is stale.
- **Visual fit:** −1 for BP-01 (still 003 slogan, unnamed map, 012) [02]; BP-02 (recap 019, map 013) [02]; BP-11 (4:00 capstone hold) [02].
- **Accuracy:** −1 for BP-07 ("grids" = gaps) [03] M2, and BP-11 (isolated margin ≠ "inventory"; liquidation is intraday) [01], [03].
- **Pacing:** +1 for BP-02 and BP-03. [01] measured the real baseline, so the under-run risk I raised is smaller (C11).
- **Clarity:** −1 for BP-11 (wrong margin term) [01].

| Lesson | Clar | Acc | Pace | Vis | Brand | Out | **Avg** | [06] avg | Prior | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| BP-01 Introduction | 8 | 6 | 6 | 6 | 6 | 9 | **6.8** | 7.2 | 4.5 | **Fix, then build.** Pair swap, core teaching and map remake |
| BP-02 What you are going to need | 8 | 5 | 6 | 6 | 6 | 8 | **6.5** | 6.7 | 4.0 | **Fix, then build.** Journal currency and tax columns |
| BP-03 What is a grid bot | 8 | 7 | 6 | 7 | 6 | 8 | **7.0** | 7.0 | 4.5 | **Build with should-fixes** (after the series blockers) |
| BP-04 Market regimes | 7 | 5 | 6 | 7 | 7 | 8 | **6.7** | 6.8 | 4.0 | **Fix, then build.** Regime glossary and touches chip |
| BP-05 Choosing grid spacing and range | 8 | 7 | 5 | 6 | 7 | 8 | **6.8** | 6.8 | 4.0 | **Build with should-fixes.** Watch the 12:00 budget |
| BP-06 Entry and exit rules | 7 | 8 | 7 | 8 | 7 | 9 | **7.7** | 7.8 | 4.0 | **Fix, then build.** Downside stop and loss card |
| BP-07 Spot paper trading | 8 | 5 | 8 | 8 | 7 | 9 | **7.5** | 7.5 | 4.0 | **Fix, then build.** "Grids" fact; needs decision S16 |
| BP-08 Managing and monitoring | 8 | 5 | 7 | 6 | 7 | 9 | **7.0** | 7.2 | 3.5 | **Fix, then build.** Week card, result-row remakes and tax note; needs decision S17 |
| BP-09 Common mistakes | 8 | 7 | 6 | 8 | 7 | 9 | **7.5** | 7.7 | 3.5 | **Build with should-fixes** |
| BP-10 Scaling up on spot | 7 | 5 | 6 | 7 | 7 | 9 | **6.8** | 7.0 | 3.0 | **Fix, then build.** A$12,500, correlation rule, still 011; needs decision S19 |
| BP-11 Advanced: liquidation scenarios | 7 | 6 | 7 | 6 | 7 | 9 | **7.0** | 7.7 | 3.5 | **Fix, then build.** Margin wording; one-currency capstone |
| **Series** | | | | | | | **7.1** | 7.3 | ≈3.8 | **Plan approved in principle.** 29 blocking fixes, then build BP-01 first and re-score the film |

No lesson reaches 8+ until the series blockers are done: one source, the clip caps, the gate, palette, disclaimer and the 20 s cut lists. Every lesson is a large step up on the prior set (≈3.8 → 7.1).

## Series-wide issues (apply to every lesson)

| Category | Issue | Source | Fix |
|---|---|---|---|
| Pacing | All 11 currently speak 1,000–1,181 words (6.3–7.4 min). Each needs +739 to +920 words for 12:00. The curriculum's additions totals are wrong in 6 lessons. | [01], [06] | #3 |
| Pacing / tooling | `studio.py` clip caps (4 sentences / 80 words; 3 / 48) will silently delete the new teaching. | [01] | #2 |
| Flow | Unmatched stills are stacked before the Recap; BP-01 replays its Hook. | [01], [05] F7 | #1, S3 |
| Accuracy | The stop rule only covers the upside exit, and its "does not come back" wording conflicts with the two-close rule. The daily close is described as 11am AEDT all year. | [01], [03] M4/M10, [06] | #11, #13, S5 |
| Visual sync | About 100 of 121 segments hold one visual for more than 20 s; about 150 of 164 KEEP stills have no clock anchor. | [02] | #12 |
| Brand | Two disclaimer texts at head; `#1E5EFF` in every JSON prompt; amber, mint and blue in 40+ KEEP stills and `studio.py`; fence and "rail" leftovers; BP-05 and BP-11 idents don't match their titles. | [02], [05], [06] | #6, #7, #9, #10 |
| Outcome | The series promise says "grow the money"; "earn" and "grid income" wording; 4 existing lines contradict the planned outcome. | [03] M11, [04] #15, [05] F14/F15, [01] | #16, S2, S7a/S16/S17/S19 |
| Compliance | Passing: no URL, path or hash spoken; no return claim spoken; Australian spelling clean; no Market Pros at head. | [01], [05], [06] | #8 (regression grep) |
| Tax / AUSTRAC | PASS WITH FIXES: 15 issues (2 high, 7 medium, 6 low). The high ones are the journal's A$ values and coin-quoted swaps. | [04] | #30, #31, #55a |

## Per-lesson key issues

### BP-01 · Introduction: 6.8, fix then build
- **Accuracy:**
  - The EXAMPLE pair arithmetic is correct [01][02][03], but that pair never completed on daily closes [06]. Swap it to 26,730→27,630 (C1, #20).
  - "Low/High" are intraday extremes on a closes chart [03] m1 (#25).
  - Only 3 one-rung pairs completed on closes [06] (#27).
- **Script / pacing:** never teaches the buy→sell pair mechanism or the fall case; second Hook block; definitions arrive late [01] (#21, S8a–f).
- **Visuals:**
  - still 003 slogan; still 012 wording [02] (#22, #24)
  - the course map is rushed and unnamed again, the repeated v3–v8 failure [02][06] (#23)
  - mint and blue still 007 [02]
  - CURRICULUM omits V07 [02]
- **Brand:** fence chapter and analogy still live at head [05] F8 (#9).

### BP-02 · What you are going to need: 6.5, fix then build
- **Accuracy:** the V04 journal row says "BTC/AUD" with a US$ band [06] (#29).
- **Tax:** the journal lacks the A$ value and other ATO fields [04] #1 (#30).
- **AUSTRAC:** VASP wording and the register check; registration is not an endorsement [04] #4/#5/#11, [03] m5 (#31).
- **Script:** never mentions an exchange account, fees or a journal; chapter "Seven lines"; 7 definitions in one shot [01] (#34, S10).
- **Visuals:** recap 019 and map 013 need a remake; Teach 1 has 100 s with no visual [02] (#32, #33).
- **Brand:** fence prompt for the paper beat [05] F9 (#9).

### BP-03 · What is a grid bot: 7.0, build with should-fixes
- **Accuracy:**
  - "number of grids" definition [03] M3 (#36)
  - starting inventory needs coin [03] m6 (#36)
  - the old wrong-side inventory line is **gone at head** [03] B1, so closed
- **Script:** passive "a sell can be written" hides the bot; five labels named two ways; "inventory" undefined [01] (S11).
- **Visuals:** V02 currency mix; V02/V03 overlap [06]; don't remake 009/011/014 [02] (#37, #37a).

### BP-04 · Market regimes: 6.7, fix then build
- **Accuracy:**
  - "4 touches each side" isn't supported: 4/3 within one gap [06] (#39)
  - crash −48% (low) vs −37% (closes) [01][03] (C6, #40)
  - trend start 28k vs 33,086 [03] m8 (#41)
- **Clarity / brand:** three "trend" definitions [01]; "range" regime collides with the grid range [05] F12; "break" overlaps the stop [06] (C7, #38, S20).
- **Visuals:** check the KEEP-still "weave" wording; prompt copy-paste [05] F13 (#42).

### BP-05 · Choosing grid spacing and range: 6.8, build with should-fixes
- **Accuracy:**
  - A$2,000 ÷ 20 orders vs 19 gaps [06] (#43)
  - span 9.5% vs 9.94% [03] m4 (#45)
  - the 006 maths is already correct [02] (C8)
- **Script:** "spacing" never defined; "Say the example fee" ambiguity; recount out of order; 150-word padding [01] (#44, S13).
- **Pacing:** 6.5 min now, +4:45 planned, minus about 0:40 of padding cuts, gives about 10:40–11:15. That is at risk of missing 12:00 [01][06] (#3).

### BP-06 · Entry and exit rules: 7.7, fix then build
- **Accuracy:**
  - the A$248.68 loss is correct [03]
  - label 85 as an EXAMPLE exit and show the fee lines [03] m7 (#47)
  - the only stop taught is the upside one [01] (#47)
- **Clarity:** price stop-loss vs the close rule; "take-profit" clashes with "no profit target" [06], [05] F15 (#48).
- **Visuals:** 013/015 "Sizing is Lesson 10" [02] (#49, S14).

### BP-07 · Spot paper trading: 7.5, fix then build
- **Accuracy:** "seven was the line count" is wrong: forms count gaps [03] M2 (C5, #50, S15).
- **Outcome:** "pressing it is not the lesson, even on paper" blocks the paper run (outcome line 2) [01] (S16, #51).
- **Realism:** "9 pairs in 2 weeks" vs 3 in the real window [06] (#52).
- **Brand:** Market Pros is **gone at head** [05] F2, so it's a regression check only (#8).

### BP-08 · Managing and monitoring: 7.0, fix then build
- **Accuracy:** the week card's A$1.80/pair and −A$24 don't come from any course bot. The correct figures are A$3.60 and −A$30 [03] M8/M9, [06] (#54).
- **Outcome:** the "no result row / wipe off the profit figure" lines are outcome line 3 [01] (S17). Stills 012/015/009 need a remake; 015 is missing from the remake list [02][06] (#55).
- **Tax:** coin-quoted fills are disposals; 4-beat records note; "grid income" rename; business-vs-investor caution [04] #2/#7/#8/#9 (#55, #55a).

### BP-09 · Common mistakes: 7.5, build with should-fixes
- **Script:** only page-hygiene mistakes; the "blank stop" line said 3 times; the stop described as a date, not a condition [01] (#55c, S18).
- **Accuracy:** "left in days" was really about 3 weeks; re-centre vs chasing needs a clear line [06]. The 7.46% figure is correct [03].
- **Visuals:** the 005 wick note is stale [02] (C8).

### BP-10 · Scaling up on spot: 6.8, fix then build
- **Accuracy:**
  - A$12,500, not A$12,440; the +25% step also breaks the 20% cap [03] M7, [06] (C2, #56)
  - the correlation-bucket rule is undefined; V05's three bots (≈A$747) exceed the 6% cap [06], [03] m10 (#57)
  - 57–73k is quoted on a closes line [01] (#59)
- **Outcome:** "the page does not tell you how much money to assign" is outcome line 4 [01] (S19). Still 011, the 001 hook and the 015 recap conflict [02] (#58).
- **Pacing:** +7:30 of additions (not 7:00) on 7.0 min; cut the 188-word repeat to stay ≤ 14:30 [06][01].

### BP-11 · Advanced: liquidation scenarios: 7.0, fix then build
- **Accuracy:**
  - isolated margin explained as "inventory" (wrong) [01] (#61)
  - liquidation is intraday: use the 13 Mar low card (4,107, −48%) [03] M6 (#62)
  - the `walk()` 2020 shots are **not live at head** [03] B3 (#14)
- **Brand:** "isolated fence" recap; box/bucket drift [01][05] F10 (#9, #61, S21).
- **Visuals / outcome:** capstone V03 holds 4:00 and needs 12+ changes; the capstone mixes US$ and A$ examples; 11:30–12:00 has no visual [02][06] (#63).
- **Brand:** the ident says "Liquidation, as a public path", not the title (#7).

## Counts
- **Fixes:** 29 blocking (12 series-wide, 17 lesson-level). By owner: **Cursor 26, Creative Studio 8, Grok Bot 8** (an item with two owners counts for each).
- **Decisions for Stewart:** 55 (11 series-wide, 44 lesson-level). These include the 4 outcome-contradicting lines (S7a, S16, S17, S19).
