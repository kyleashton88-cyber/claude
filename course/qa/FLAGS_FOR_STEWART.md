# Decisions only Stewart can make: GridBot Blueprint expansion

Prepared 16 Nov 2026, about 9:00am WITA (12:00pm AEDT). Deduplicated from [01] YouTube Producer (61 FLAGs), [02] Creative Studio, [03] Crypto Research, [04] Tax Accounting, [05] External Comms and [06] Grok Bot (F0–F31). The "Old" wording is what is spoken or shown at the live head 962465c.

**Already decided, so not listed:**
- GridBot Builder spelling
- strict navy/cyan/white, with blue, amber and mint recoloured
- the fence retired
- titles and order unchanged

(BP-05 and BP-11's spoken idents, which differ from their titles, are aligned to the unchanged titles as a fix, not a flag. See FIXES #7.)

## Series-wide

| ID | Decision | Old | Proposed |
|---|---|---|---|
| S1 | **Disclaimer wording** (one text, all 11) | Two variants. Spoken in `studio.py`: "Education only. Not financial advice. This is general information and doesn't consider your objectives, financial situation or needs. Crypto is high risk. You could lose all the money you put in." JSON / `legal()`: "Education only, not financial advice. Crypto carries a risk of total loss. This is general information. It doesn't consider your objectives, financial situation or needs. The prices are public historical daily closes, marked Example…" | **External Comms' canonical block, verbatim:** "Education only. Not financial advice. This is general information and doesn't consider your objectives, financial situation or needs. Crypto is high risk; you could lose all the money you put in. Past performance is not a reliable indicator of future results." Optional add-ons, each its own sentence: "The prices are public historical daily closes, marked Example. No order is sent from this lesson." · BP-11 only: "Leverage magnifies losses. A leveraged position can be liquidated, and you can lose all the money you commit." · "This lesson is not affiliated with, endorsed by or sponsored by any exchange." · BP-02 and BP-08 tax segments (Tax): "This is general information, not tax advice. How tax applies depends on your circumstances. Check ATO guidance or speak to a registered tax agent." *(The alternative is the brief's "Educational content only, not financial advice…", per [01] F-ALL-1.)* |
| S2 | **Series promise** | "…grow the money you give to bots only under written risk rules" / "why a grid earns" | External Comms' wording: "By the end of this series you will understand what a grid bot does, when it can capture bounces, and where it loses. You will know how to plan one, test it on paper, run it, check it, and change the capital you give to bots only under written risk rules. This is education, not a promise of results." "Why it earns" becomes "how a grid can capture bounces". |
| S3 | **Shot order inside every lesson** | 10–14 stills appended as one block before the Recap (BP-01 replays "Hook" after the worked check) | Re-chapter so each still plays inside its own teaching section, in hook → teach → example → mistake → next → recap order. Words kept; order changes. |
| S4 | Fence leftovers in script lines | "Move the rail up to the top line" / "Rails come from…" (17 uses) | "Move the top line up to the real high" / "The top and bottom lines come from…" |
| S5 | **Stop rule wording** (BP-01, 02, 06, 08, 09, 10) | "if the daily close leaves the top line and does not come back, the idea is finished" | "if a daily close is outside the band, through the top or the bottom, and the next daily close is still outside, the idea is finished. Then you stop the bot, which cancels the waiting orders, and do what you wrote: keep the coin or swap to cash." |
| S6 | Cut padded repeat blocks (BP-05 to 10) and the repeated workbook lines | 150–190-word chart shots re-reading the lesson; "On the diagram for this beat, look for…", "The shapes are the lesson", "Say the opening line once more…" | Keep the first few sentences of each block; use the freed time for new teaching; keep one short cue per beat. |
| S7 | **Outro wording** (all 11) | "Bring your notes: the top and bottom of the band, the gaps between the lines, and your stop rule. **Leave every figure marked Example.** No order is sent between lessons." | "Bring your notes: your band, your gaps and your stop rule. Keep the word Example on every practice figure. Next lesson you will [one sentence naming the next skill]." |
| S7a | **Outcome-contradicting line 1 of 4** (BP-01 to 10 outros; BP-01 "Paper first"; BP-02/06/07) | "No order is sent between lessons." / "You still do not send an order in this course." | "No real order is sent in this lesson. Paper practice comes in Lesson 7, and real money only after your written graduation rule." |
| S7b | Brief vs measured wording: "5x" | "A multiple, like 5x" (BP-07, 10, 11) | "A multiple, such as five times" |
| S7c | Builder caps (tool change) | `clip_vo` 4 sentences / 80 words; `key_stops` 3 / 48 | Lift the caps, or write the additions as more, shorter shots. Either works; lifting them is a tool change. |
| S7d | Captions | Sidecar VTT (not burned in) | Burn the captions in so they stay inside the 5% margin, or keep VTT with positioning cues. |

## BP-01 · Introduction

| ID | Old | Proposed |
|---|---|---|
| S8 | Still 012 "NO PROFIT PROMISES"; shot "No result number": "There is no result number in this lesson. A result number would pretend the example already happened. The example is a drawing of a mechanism." | Still "NO PROMISE OF RESULTS"; "There is no promise of results in this lesson. Numbers marked Example are teaching numbers, not advice." |
| S8a | "The fence": "A fence has a top rail and a bottom rail. Inside them, the price can wander. On the chart those rails are 24930 and 30331." | "The top rung and the bottom rung are your range. Inside them, the price can move up and down. On the chart they are the top line and the bottom line." |
| S8b | "Paper first": "A paper or demo account is a fence around practice… You still do not send an order in this course." | "Paper or demo trading is like driving with L-plates: you practise with pretend money before anything is real. Lesson 7 shows you how." |
| S8c | Stop shot opener (verbatim repeat): "A stop is a rule you write down before you start…" | "Here is that stop rule on the real path." |
| S8d | "The levels are limit orders that wait on the rungs." | "The levels are the prices on the rungs where limit orders wait." |
| S8e | Card "Stop = when you quit." | "The stop is your written rule for when you stop the bot." |
| S8f | Map: "…Next is a checklist. Then the definition. Then calm or trending markets…" | Name every lesson: "…Then exactly what a grid bot does, order by order… Then scaling up under written rules. Then an opt-in lesson on liquidation and your complete plan." |
| S9 | Worked check "Low 24,930 / High 30,331" (intraday extremes on a closes chart) | "Bottom line / top line", with the figures on the card only. |
| S9a | (New example, not an existing line) EXAMPLE pair 27,630→28,531, which never completed on closes | Use 26,730→27,630 (filled 17 Aug → 29 Aug), net ≈ US$8.46, "about eight and a half dollars". Or keep the old pair labelled "illustration". |

## BP-02 · What you are going to need

| ID | Old | Proposed |
|---|---|---|
| S10 | Chapter "Seven lines" | "Seven items" |
| S10a | "…the three words, range, levels and stop, which come next…" | "…the three words from lesson one, range, levels and stop…" |
| S10b | Objective: "…seven-item checklist on paper. An order is an instruction to buy or sell." | Drop the second sentence (the definition moves to BP-01). |
| S10c | Recap: "Say the hook in one line, name the diagram you drew…" | "Recap: your page has seven items, each with a written fact, every figure marked Example, and no secrets on it." |
| S10d | "Empty pair": "The page shows one blank row, labelled Pair…" | "Write the pair first. For this course it is bitcoin priced in US dollars. Every other row depends on it." |

## BP-03 · What is a grid bot

| ID | Old | Proposed |
|---|---|---|
| S11 | "…and a sell can be written one rung higher." | "…and the bot places a sell one rung higher." |
| S11a | "Point and say the five: Top, Bottom, Levels, What you hold, and Stop." | "Point and say the five: upper, lower, levels, side, and stop." (matching the earlier shot) |
| S11b | "It is not a signal, not a fund, and not a person watching the market for you." | "It is not a tip telling you when to buy, not a fund that manages money for you, and not a person watching the market for you." |

## BP-04 · Market regimes

| ID | Old | Proposed |
|---|---|---|
| S12 | "From the close two days earlier, about 8 thousand, down to the low on this candle, is about 48 percent." | "From the close on 11 March, about 7,900, to the close on 12 March, about 5,000, the price fell about 37 percent in one day." (Keep −48% only on a labelled intraday-low card.) |
| S20 | Three trend definitions, including "A trend on this page is a path that leaves and keeps making ground in one direction." Bare "range" for the regime. | One definition: "A trend is a path that keeps moving one way over weeks." "A break is a sudden big move out of the band in a day or two." "Range regime / ranging market" for the regime. |
| S20a | "A trend means drawing what you'd end up holding." | "…a climb fills every sell and leaves you all cash, and a fall fills every buy and leaves you all coin." |
| S20b | Objective "You will call 12 to 13 March 2020 a break" vs the 11–12 Mar maths | One window, "11 to 12 March 2020", on every line. |

## BP-05 · Choosing grid spacing and range

| ID | Old | Proposed |
|---|---|---|
| S13 | "Say the example fee for one buy plus one sell is two tenths of one percent." | "Suppose the example fee is one tenth of one percent on the buy and the same on the sell. That round trip is two tenths of one percent." |
| S13a | "A round box would have missed days that went outside it." | "A band drawn at tidy round numbers would have missed days that went outside it." |
| S13b | "Halving the step doubles the gaps, not the lines. Five gaps become ten gaps, which is eleven lines." | "…For example, a band with five gaps has six lines. Halve the step and it has ten gaps, which is eleven lines." |
| S13c | Wrong-page recount plays before the 19-gaps teaching | Move it after, and drop "Now a second, made-up example…". |

## BP-06 · Entry and exit rules

| ID | Old | Proposed |
|---|---|---|
| S14 | "Size is not this lesson. A size written here would pretend the rules are done." Stills 013/015 "no size" | "Sizing is Lesson 10. Here you only measure the loss at stop." |
| S14a | "The finish rule is the stop rule from lesson 1: the condition that ends the idea." | "The finish rule is your exit rule, the stop rule from lesson 1… The before sentence is your entry rule." |
| S14b | Recap: "The finish rule names 23 October 2023." | "In the example, the finish rule was met on 23 October 2023." |

## BP-07 · Spot paper trading

| ID | Old | Proposed |
|---|---|---|
| S16 | **Outcome-contradicting line 2 of 4:** "The walk ends before any confirm control… Pressing it is not the lesson, even on paper, because the habit is the point." | "On a paper or demo account, pressing start uses pretend money, and that is the practice. On a real account, you stop before confirm until your graduation rule passes." |
| S15 | "The form says seven and your page says six gaps. Seven was the line count, and six is the gap count." | "On most forms, 'grids' means gaps. Your page has six gaps, which is seven lines, so you enter six. Check your exchange's help page." |
| S16a | "A venue is an app or a website…" (twice) | "exchange" throughout; say it once. |

## BP-08 · Managing and monitoring (reversal)

| ID | Old | Proposed |
|---|---|---|
| S17 | **Outcome-contradicting line 3 of 4 (BP-08 reversal):** "If you add a profit figure to either card, wipe it off." / "do not open a fourth row for a result" / "The common miss is to add a result row…" / "no result row". Stills 009/012/015. | "The fourth row is a review record, not a target: realised, unrealised, fees, and whether you followed the rules." Common miss: "counting only completed-pair results". |
| S17a | "grid income" | "completed-pair result", plus "Your journal's realised number is not your tax figure." |
| S17b | "A cadence is a day you choose to reread the same three rows. Cadence means the day you come back." | "A cadence is the day you choose to come back and reread the same three rows." |

## BP-09 · Common mistakes

| ID | Old | Proposed |
|---|---|---|
| S18 | "Without a written rule for 23 October…" / "First write the stop rule for 23 October 2023…" | "Without a written rule for a close outside the band…" / "First write the stop rule: a daily close outside the band, and the next close still outside. In the example, that happened on 23 October 2023." |
| S18a | "Write the next title so the ending cannot pretend." | "Write the next lesson's title at the bottom of your page, so you know the course is not finished." |
| S18b | "A leverage multiple is a times-number. Cross it out." | "Leverage means trading with borrowed money, and the multiple, such as five times, says how much is borrowed. Cross it out." |

## BP-10 · Scaling up on spot (reversal)

| ID | Old | Proposed |
|---|---|---|
| S19 | **Outcome-contradicting line 4 of 4 (BP-10 reversal):** "The page does not tell you how much money to assign… The lesson will not fill it." / "size not filled by the course" / "Size is still not a target." Still 011 "NO MONEY AMOUNT ON THIS PAGE"; 015 "no money amount" | "This lesson teaches a method for deciding size with Example caps. It is not advice on how much to put in." / "size set by your written caps" / "Size comes from your caps, never from a target." Remove 011; rework 001 and 015. |
| S19a | "Scaling by adding leverage is a different course of risk, and this page crosses that out." (twice) | Once: "Scaling by adding leverage is a different kind of risk, and this course crosses it out." |
| S19b | "a band from about 57 thousand to about 73 thousand" over a close-only line | "from about 58 to about 72 thousand" on closes, or a candle card for the extremes. |

## BP-11 · Advanced: liquidation scenarios

| ID | Old | Proposed |
|---|---|---|
| S21 | Recap: "opt-in, loss first, isolated fence, cross can pull…" | "Recap: opt-in, loss first, isolated is one bucket, cross joins the buckets…" |
| S21a | "Isolated margin… means the venue looks at the inventory assigned to that position." | "…means the exchange looks only at the margin you assigned to that position." |
| S21b | "isolated as one box" / "a loss stays in that box" | "bucket" throughout. |
| S21c | "11 March closed at 7911 and 12 March closed at 4971." | "about 7,900… about 5,000" (exact figures on the card). |

**Count: 55 decisions** (11 series-wide, 44 lesson-level). The 4 outcome-contradicting lines are S7a, S16, S17 and S19.

**Recommended order of decision:**
1. S1, S2, S7, S7a, S16, S17, S19. These unblock the planned BP-07, BP-08 and BP-10 content.
2. S3, S5, S7c, S7d. These are structure and tooling.
3. Everything else as a batch.
