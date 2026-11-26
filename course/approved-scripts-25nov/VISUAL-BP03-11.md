# Visual-readiness check: Blueprint BP-03 to BP-11 (script stage)

Creative Studio, read-only. Scored **25 Nov 2026, 8:53am AEDT** (Australia/Sydney, UTC+11). No renders were started or requested, and no images were generated.

**Scope:** signed spoken scripts and visual plans at repo head `e37bbc1` (box copy: `/workspace/bp-qa/readiness/_src/course/proposed-scripts-23nov/`). Packet: `/workspace/bp-qa/readiness/PACKET.md`. This is a script-stage check of whether each lesson is render-ready under the current visual rules. There are no films for these signed scripts.

**Rules applied:** nothing static longer than 8 s (holds of 20 s or more are a fail); the concept must be shown within about 2 s of being spoken; show the idea, do not only print the sentence; EXAMPLE badge on any figure or chart; navy/cyan/white palette only; on-screen text at least 28 px; margins at least 45 px; official Grid Bot Builder end-card lockup (hex G, GRID BOT in white, BUILDER in blue); exchange-neutral; beginner lens (each lesson assumes only the prior lessons). Images must come from ChatGPT web, with Cursor/Claude as a fallback only after QA. Ken Burns or a caption change does not count as a visual change.

**Runtime basis:** official spoken word counts from the readiness scan (whitespace tokens). Pace is 163 words/min, the measured af_heart 1.0 pace from the BP-01 and BP-02 films. 150 words/min is shown as a slower bound. “Minimum beats” is the sum, over each spoken paragraph, of `ceil(duration / 8 s)`. That is the fewest distinct pictures that keep any one paragraph from holding longer than 8 s. A new concept still has to appear within about 2 s of being spoken, so some long paragraphs will need more than this floor.

## Orchestrator claims — verified or corrected

| Claim | Verdict |
|---|---|
| None of the 48 planned cards exist | **CONFIRMED.** `BP-03`–`BP-11` PASS-LISTs name 48 paths `proposed/bp-XX/0N.png` (7+6+6+4+5+5+5+5+5). All rows are `status: draft`, `pass: false`, `scores: null`. None of those files exists in the e37bbc1 extract, and a box-wide search found no `proposed/bp-03`…`bp-11` PNGs. |
| `course/images/FALLBACK_MANIFEST.json` still marks old stills as passed, although we failed them on 14 Nov | **CONFIRMED for BP-04–11; only partly true for BP-03.** The e37bbc1 manifest lists **180** unique stills for BP-03–11 and marks **every one** `status: pass`, with 5 Nov qa_reason lines. Creative Studio’s 14 Nov rescore of the old-script stills is: **BP-04–11, 0 pass / 161 fail of 161** (`/workspace/blueprint-beginner/bp04-11-qa/REPORT.md`; same result recorded in `course/blueprint-rebuild/BP04-11_IMAGE_MANIFEST.json`). **BP-03 was not a blanket fail:** the 14 Nov v2 report (`blueprint-image-qa/bp01-03-v2/REPORT.md`) left lesson stills at **18 pass / 1 fail of 19** after remake rounds, with `010.png` still failing; the manifest still marks all 19, including `010.png`, as pass. Those 18 passes are for the *old* 1,229-word script “What is a grid bot” and do not match the signed lesson, so they must not be reused. There is no numbered 14 Nov report sitting in `/workspace/bp-qa/` itself; the reports live in the bp04-11 / bp01-03 QA work and are cited from the readiness notes and the image manifest. |
| BP-04, BP-10 and BP-11 need 2020 and 2024 charts | **OVER-SIMPLIFIED. Corrected below.** Not all three lessons need both charts. BP-04 needs the **March 2020** crash/candle *and* the later path from **23 October 2023 (33,086) to 14 March 2024 (71,397)** — that 2024 close is the end of the 2023–24 trend, not the later 2024 second range. BP-10 needs the **second_range_2024** window (27 March–24 June 2024, 56,555–72,715) plus the summer page; it does not use a 2020 chart. BP-11 recaps the same 2024 second-range edges (width 16,160) and needs that 2024 picture (or a card of those edges); its spoken script has **no 2020** material. All three also still use the shared summer 2023 range (24,930–30,331). The current builder defaults every signed paragraph to the summer chart. |
| BP-06 has only 4 cards for ~11 min | **CONFIRMED.** The PASS-LIST and the header both list **4** cards. Spoken length is 1,744 words: **10.7 min at 163 wpm**, 11.6 min at 150 wpm. That is the thinnest plan in the set. Four cards cannot cover a 10–12 minute lesson under the 8 s rule. |

Two smaller plan mismatches, not in the claims: the BP-04 *header* lists **7** on-screen visuals (it adds a separate “candle card for 13 March 2020”) while the PASS-LIST has **6**, folding those figures into the March 2020 card. The BP-03 self-check card says “three questions” but the spoken self-check asks **four**. The BP-08 plan has a “stop card: two questions” that conflicts with the lesson’s three-question rule.

## Set result

**All nine lessons are NOT READY.** 0 of 48 planned cards exist. 0 of them have been scored. The old stills are the wrong scripts, and for BP-04–11 they already failed QA. A paragraph-stack render would produce 16–20 holds of 20 s or more in every lesson (automatic fails) and 19–23 holds over 8 s. Each lesson needs a voice-tied shot list and new stills, drawn to the rules above, from ChatGPT web (Cursor/Claude only as a QA’d fallback).

| Lesson | Title | Words | Min @163 / @150 | Planned cards present | Old stills (manifest / 14 Nov QA) | Paras | Holds >8 s / ≥20 s | Max hold | Min beats (≤8 s) | Verdict |
|---|---|---:|---|---:|---|---:|---|---:|---:|---|
| BP-03 | How a grid bot works, order by order | 2,181 | 13.4 / 14.5 | 0 / 7 | 19, all manifest-pass; 18 pass / 1 fail on 14 Nov, old script | 24 | 23 / 20 | 86.5 s | 112 | **NOT READY** |
| BP-04 | Market regimes | 1,845 | 11.3 / 12.3 | 0 / 6 | 20, all manifest-pass; 0/20 on 14 Nov | 20 | 19 / 17 | 58.2 s | 94 | **NOT READY** |
| BP-05 | Choosing grid spacing and range | 1,658 | 10.2 / 11.1 | 0 / 6 | 19, all manifest-pass; 0/19 on 14 Nov | 20 | 19 / 15 | 71.0 s | 87 | **NOT READY** |
| BP-06 | Entry and exit rules | 1,744 | 10.7 / 11.6 | 0 / 4 | 20, all manifest-pass; 0/20 on 14 Nov | 23 | 21 / 16 | 55.6 s | 92 | **NOT READY** |
| BP-07 | Spot paper trading | 1,727 | 10.6 / 11.5 | 0 / 5 | 20, all manifest-pass; 0/20 on 14 Nov | 23 | 22 / 15 | 43.8 s | 90 | **NOT READY** |
| BP-08 | Managing and monitoring | 1,805 | 11.1 / 12.0 | 0 / 5 | 20, all manifest-pass; 0/20 on 14 Nov | 23 | 22 / 19 | 55.2 s | 94 | **NOT READY** |
| BP-09 | Common mistakes | 1,696 | 10.4 / 11.3 | 0 / 5 | 21, all manifest-pass; 0/21 on 14 Nov | 23 | 21 / 17 | 60.7 s | 89 | **NOT READY** |
| BP-10 | Scaling up on spot | 1,721 | 10.5 / 11.5 | 0 / 5 | 21, all manifest-pass; 0/21 on 14 Nov | 22 | 21 / 16 | 53.4 s | 91 | **NOT READY** |
| BP-11 | Optional close: the spot page, and what this course does not cover | 1,992 | 12.2 / 13.3 | 0 / 5 | 20, all manifest-pass; 0/20 on 14 Nov | 24 | 22 / 19 | 54.1 s | 103 | **NOT READY** |
| **Total** | | **16,369** | **~101 / ~110 min** | **0 / 48** | **180 unique, all still manifest-pass** | **202** | **190 / 154** | **86.5 s** | **852** | **9 / 9 NOT READY** |

Old stills are not in the e37bbc1 extract (`/workspace/bp-qa/readiness/_src/course/images/` holds only the manifest). Copies of the scored files are on the box at `/workspace/blueprint-beginner/bp04-11-qa/src/` (161) and `/workspace/blueprint-beginner/bp01-03-qa/src/bp-03-what-is-a-grid-bot/` (19). Do not use them for these signed scripts.

The 48 planned cards are the hero teaching pictures (ladders, worked sums, safety lists). They are necessary and all missing, but they are not a sufficient still count. **At least 852 distinct visual beats** are needed so no paragraph holds longer than 8 s. A runtime-only floor (`ceil(seconds / 8)`) is 759. Official end-card lockups, title/disclaimer frames, and fill-in variants of the hero cards are part of that beat count, not extras on top of a 48-card plan.

---

## BP-03 — NOT READY

How a grid bot works, order by order. 2,181 words (PASS-LIST header still says 2,178; the scan and this report use 2,181), 13.4 min at 163 wpm.

**Planned cards (0 of 7 present):** `proposed/bp-03/01.png`–`07.png` — ladder (24,930…30,331, 901 gap between 27,630 and 28,531, every figure Example); cross-versus-fill two-column; worked arithmetic (0.01 coin, buy 26,730, sell 27,630, gross 9, fee 0.2673+0.2763=0.5436); inventory (more coin after the buy, more cash after the sell, neither called a result); two-parcel card; leave card (23 October 2023 close 33,086 above 30,331); self-check.

**Old stills:** 19 under `course/images/bp-03-what-is-a-grid-bot/`. Manifest: 19 pass (5 Nov). 14 Nov v2: 18 pass / 1 fail after remakes (`010.png` still fail). All are the old “What is a grid bot” script, including a title card that still uses that name. Not usable.

**Needs to be render-ready:**
- All 7 planned cards, redrawn for the signed script. Fix the self-check to **four** spoken questions, with answers held until spoken.
- A voice-tied shot list of **at least 112** stills/variants so none of the 24 paragraphs holds >8 s (20 of those paragraphs would already be ≥20 s fails on a one-stack render; longest 86.5 s). Show each new idea (limit vs market, gap arithmetic, middle split vs lesson 1, cross vs fill, inventory, two parcels, leave date) within about 2 s of the line.
- Shared summer 2023 range chart (24,930–30,331, seven lines, six gaps). No 2020 or 2024 window is spoken here.
- Official end-card lockup naming the next lesson (Market regimes). Title, disclaimer (“Education only. Not financial advice.”), EXAMPLE on every figure, navy/cyan/white, type ≥28 px, margins ≥45 px, no exchange marks.
- Beginner: do not preview a “finish rule” as if it had already been taught in BP-06; if the script keeps that wording, the picture should not assume the later lesson.

## BP-04 — NOT READY

Market regimes. 1,845 words, 11.3 min at 163 wpm.

**Planned cards (0 of 6 present):** three-shape card (range, trend, break, no forecast arrow); range card with “within one gap” strips; count card (eight near the top, five near the bottom, “not four and four”); later-path card (33,086 on 23 Oct 2023 to 71,397 on 14 Mar 2024); March 2020 card (11 Mar ~7,911, 12 Mar ~4,971, ~37 percent, 13 Mar high 5,838 / low 4,107 / close 5,564, width 1,731, close higher); label card (shape name plus dates, or “not sorted”).

**Old stills:** 20, all manifest-pass; **0/20** on 14 Nov. Not usable.

**Needs to be render-ready:**
- All 6 planned cards. Resolve the header’s seventh item (a separate 13 March 2020 candle card) by merging it into the March 2020 card or splitting it clearly in the PASS-LIST.
- Voice-tied shot list of **at least 94** beats (20 paragraphs; 17 would hold ≥20 s; max 58.2 s).
- Chart variants: summer 2023 range; **crash_2020** (11–13 March 2020, including the 13 March candle); **later path / breakout** from 23 October 2023 to 14 March 2024 (33,086 → 71,397). The builder must not park these beats on the summer chart.
- Official end-card lockup; EXAMPLE on every figure; beginner: the candle is spoken after some 2020 figures — the candle picture should arrive with the definition, not as an unexplained wick before that line.

## BP-05 — NOT READY

Choosing grid spacing and range. 1,658 words, 10.2 min at 163 wpm.

**Planned cards (0 of 6 present):** ladder (seven lines, six gaps, about 900, 30,331 / 24,930); cost card (0.2673+0.2763=0.5436, about 54 cents on 0.01 coin and US$54.36 on a whole coin, mid-price shortcut of about 55 crossed out); miss card (round top 30,000 vs real top 30,331, 331 above); equal-dollar ladder 100, 125, 150, 175, 200; equal-percent ladder 100, 118.9, 141.4, 168.2, 200; self-check with answers hidden until spoken.

**Old stills:** 19, all manifest-pass; **0/19** on 14 Nov. Not usable.

**Needs to be render-ready:**
- All 6 planned cards, including the two 100→200 ladders (no extra market window required).
- Voice-tied shot list of **at least 87** beats (20 paragraphs; 15 would hold ≥20 s; max 71.0 s). The fee-sum paragraph is the longest and must fill in line by line, not sit on one still for 71 s.
- Shared summer 2023 range only. Official end-card lockup; EXAMPLE on every teaching figure.

## BP-06 — NOT READY

Entry and exit rules. 1,744 words, 10.7 min at 163 wpm (11.6 at 150). **Four planned cards for a ~11 minute lesson.**

**Planned cards (0 of 4 present):** two-column Finish / Before / Size-blank (23 Oct 2023 close 33,086; 7 Oct 2023 close 27,969); leave card (2,755 and 3,571 above 30,331, 7 Oct 2,362 under the top and 339 over the middle, next close still outside); inside card (27,969 between 24,930 and 30,331, a little above 27,630); self-check with the size line empty on purpose.

**Old stills:** 20, all manifest-pass; **0/20** on 14 Nov. Not usable.

**Needs to be render-ready:**
- All 4 planned hero cards, plus many fill-in / highlight variants. Four cards are not enough.
- Voice-tied shot list of **at least 92** beats (23 paragraphs; 16 would hold ≥20 s; max 55.6 s).
- Shared summer 2023 range for the worked dates. The line that “2023 to March 2024 already shows the leave” can use the BP-04 later-path picture if it is shown as a recap, not as a new 2024 second range. No 2020 chart is required.
- Official end-card lockup; EXAMPLE on every figure. If the script keeps “ceiling” unexplained, do not put an undefined “ceiling” label on the card.

## BP-07 — NOT READY

Spot paper trading. 1,727 words, 10.6 min at 163 wpm.

**Planned cards (0 of 5 present):** page card (pair bitcoin, top 30,331, bottom 24,930, gaps six, two sentences, Example, **no logo and no balance**); count card (seven lines vs six gaps, “enter six”); cleared-size card (filled-in size crossed out, “the page did not write this”); spot card (coin you hold vs a contract marked “not this lesson”); self-check ending “nothing is sent”.

**Old stills:** 20, all manifest-pass; **0/20** on 14 Nov. Not usable.

**Needs to be render-ready:**
- All 5 planned cards. The mock form must stay exchange-neutral and show no balance.
- Voice-tied shot list of **at least 90** beats (23 paragraphs; 15 would hold ≥20 s; max 43.8 s). Walk the wrong form and the right form as pictures, not as a paragraph of text.
- Shared summer 2023 figures only. Official end-card lockup; EXAMPLE on page figures.

## BP-08 — NOT READY

Managing and monitoring. 1,805 words, 11.1 min at 163 wpm.

**Planned cards (0 of 5 present):** three-question card for 7 Oct 2023 (inside, 339 above 27,630, stop not met); three-question card for 23 Oct 2023 (outside, 33,086 is 2,755 above 30,331, the finish sentence holds); fourth-row “review record, not a target”; stop card currently labelled “two questions, then you close the page”; a line that this course does not run an alert service.

**Old stills:** 20, all manifest-pass; **0/20** on 14 Nov. Not usable.

**Needs to be render-ready:**
- All 5 planned cards. Rework the “two questions” stop card so it does not contradict the three-question rule (for example: on an outside day, “which side” no longer matters, then you close the page).
- Voice-tied shot list of **at least 94** beats (23 paragraphs; 19 would hold ≥20 s; max 55.2 s).
- Shared summer 2023 range and the two worked dates. Official end-card lockup; EXAMPLE on every figure.

## BP-09 — NOT READY

Common mistakes. 1,696 words, 10.4 min at 163 wpm.

**Planned cards (0 of 5 present):** blank-stop card (empty finish column and the sentence that belongs there, dated 23 Oct 2023); tight-range / miss card (round box 30,000, real top 30,331, 331 above); count card (seven marks, six gaps, “seven” crossed out as a gap count); three-pass card (stop, then top, then six gaps; no grade); corrected page (range, six gaps of about 900, stop rule).

**Old stills:** 21, all manifest-pass; **0/21** on 14 Nov. Not usable.

**Needs to be render-ready:**
- All 5 planned cards, shown as pages being fixed, not as slogans.
- Voice-tied shot list of **at least 89** beats (23 paragraphs; 17 would hold ≥20 s; max 60.7 s).
- Shared summer 2023 range only. Official end-card lockup; EXAMPLE on every figure.

## BP-10 — NOT READY

Scaling up on spot. 1,721 words, 10.5 min at 163 wpm.

**Planned cards (0 of 5 present):** two-page card (page one 24,930–30,331, stop 23 Oct 2023; page two 56,555–72,715, 27 Mar–24 Jun 2024); width card (page-two width beside summer 5,401, “do not copy 900”); one-change card (range changes, pair stays bitcoin, spot stays coins you hold); crossed-out “scaling by adding a multiple”; two buckets, each with its own stop line.

**Old stills:** 21, all manifest-pass; **0/21** on 14 Nov. Not usable.

**Needs to be render-ready:**
- All 5 planned cards.
- Voice-tied shot list of **at least 91** beats (22 paragraphs; 16 would hold ≥20 s; max 53.4 s). The page-two paragraph (53.4 s) has to *show* the 2024 window filling in, not hold a summer chart.
- Chart variants: summer 2023 page one, and **second_range_2024** (27 March–24 June 2024, 56,555–72,715, width 16,160). No 2020 chart. The builder must not title this window “19 July 2023 to 16 October 2023”.
- Official end-card lockup; EXAMPLE on both pages’ figures.

## BP-11 — NOT READY

Optional close: the spot page, and what this course does not cover. 1,992 words, 12.2 min at 163 wpm.

**Planned cards (0 of 5 present):** opening card (signed title beside a completed summer spot page; no definitions of margin, liquidation, isolated, or cross); ladder (same seven Example levels, 901 gap labelled); pair card (buy 26,730, sell 27,630, gross 9, fee 0.5436, about 54 cents, about 8 dollars 46 left); stop card (23 Oct 2023 close 33,086, 2,755 above 30,331, next close still outside); skip card (“Skipped on purpose. The spot page stands.”).

**Old stills:** 20 under the old slug `bp-11-advanced-liquidation`, all manifest-pass; **0/20** on 14 Nov. Those stills are the old liquidation lesson. Not usable, and they must not be shown as if this optional-close script teaches liquidation mechanics.

**Needs to be render-ready:**
- All 5 planned cards. The skip / “does not cover” card must not define margin, liquidation, isolated or cross.
- Voice-tied shot list of **at least 103** beats (24 paragraphs; 19 would hold ≥20 s; max 54.1 s). The recap that names the 2024 second-range edges (56,555 and 72,715, width 16,160) needs that **second_range_2024** picture, or a clearly Example-marked card of those edges — not a 2020 chart, and not a silent summer chart while 2024 numbers are spoken.
- Chart variants: summer 2023 ladder and stop, plus the 2024 second-range recap from BP-10.
- Official end-card lockup (course close / what to bring). The BP-11-ALT long warning is still LAWYER and is not part of this lesson’s visuals.
- Title on the opening card must be the signed title, not “Advanced: liquidation”.

---

## What “render-ready” still requires, for every lesson

1. A voice-tied beat list (concept on screen within ~2 s; no static hold >8 s; a 20 s hold is a fail).
2. New stills for those beats, including fill-in variants of the planned hero cards, title and disclaimer frames, and an **official end-card lockup**. Source: ChatGPT web; Cursor/Claude only as a QA’d fallback. Do not reuse the 14 Nov old-script stills, and do not treat a FALLBACK_MANIFEST `pass` as a current pass.
3. The chart windows actually spoken: summer 2023 on all nine lessons; crash_2020 and the Oct 2023–Mar 2024 later path on BP-04; second_range_2024 on BP-10 and as a recap on BP-11.
4. QA at the same bar used for BP-01/02 stills: show-not-print, EXAMPLE on figures, navy/cyan/white, type ≥28 px, margins ≥45 px, exchange-neutral, beginner lens.

## Totals to commission

| Item | Count |
|---|---:|
| Planned hero cards, all missing, all still required | **48** |
| Minimum voice-tied stills / variants so no paragraph holds >8 s @ 163 wpm | **852** |
| Runtime-only floor (`ceil(seconds / 8)`), for reference | 759 |
| Official end-card lockups (one per lesson; part of the 852, not extra) | 9 |
| Old stills in the manifest, all still marked pass, not reusable | 180 (19 + 161) |
| Lessons render-ready | **0 / 9** |

**Commission against the 852-beat floor, not against the 48-card lists.** The 48 are the pictures that must exist inside that beat list. Concept-within-2 s will add more beats in the long teaching paragraphs. Nothing in this report was generated, committed, or sent.
