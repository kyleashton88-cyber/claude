# Revisions, 23 November

Proposed scripts only. BP-01 and BP-02 were not edited. Nothing here was rendered.

Reviews applied: numbers review 71 (mean 8.4, FIX items 1–9) and legal review 70. The quiz recount used `course/data/public-prices/btc-usd-windows.json`, window `range_2023`, 90 daily closes from 19 July 2023 to 16 October 2023.

Spoken words below are the words after `## Spoken script`.

| Lesson | Spoken words | Minutes at 165 wpm |
| --- | ---: | ---: |
| BP-03 | 2042 | 12.4 |
| BP-04 | 1851 | 11.2 |
| BP-05 | 1795 | 10.9 |
| BP-06 | 1749 | 10.6 |
| BP-07 | 1764 | 10.7 |
| BP-08 | 1740 | 10.5 |
| BP-09 | 1798 | 10.9 |
| BP-10 | 1773 | 10.7 |
| BP-11 | 2204 | 13.4 |

## Numbers

1. BP-03 and BP-05 now use the published rungs 28,531 and 29,431. BP-05 walks those rungs directly. 28,530 is named only as the unrounded step that is not published. The 901 gap sits between 27,630 and 28,531. Locked ladder: 24,930, 25,830, 26,730, 27,630, 28,531, 29,431, 30,331.
2. The day line in every lesson is the approved BP-01 S5 line. See Legal C1.
3. The locked fee on 0.01 coin at 26,730 and 27,630 is 0.2673 + 0.2763 = 0.5436, about US$0.54. What is left of the 9 dollars is about US$8.46. On a whole coin the two fees are 54.36. BP-03, BP-05 and BP-08 no longer teach about 55 dollars or about 55 cents as the fee. BP-05 shows 55.26 only as the rejected mid-price shortcut. The thin-gap test is 40 against about 54, which still fails. 9 is still wider than 0.54, and 900 is still wider than 54.36.
4. BP-03 no longer says three buys were still waiting at the end of the window. Under the taught book, buys wait below the middle. The three completed pairs are 26,730 with 27,630, then 25,830 with 26,730, then 26,730 with 27,630 again. Zero parcels are still waiting.
5. BP-04 and BP-09 now say eight closes near the top and five near the bottom. Recounted from the course file: close at least about 29,431 on 19, 20, 21, 22 and 23 July, 1 August, and 8 and 9 August (eight). Close at most about 25,830 on 1, 4, 5, 6 and 11 September (five). 10 September (25,832.23) and 12 September (25,833.34) stay just outside. The self-check, the paper reminder, the recap, and BP-09 use eight and five.
6. BP-04 March 2020 now uses about 7,911 on 11 March and about 4,971 on 12 March. The drop is 2,940, about 37 percent. The old about 8,000, about 5,000 and about 3,000 are gone.
7. BP-05 says 900 divided by 27,630 is about 0.033, which is about 3.3 percent, still much wider than 0.2 percent.
8. BP-07 no longer says "On most forms, grids means gaps." It says check the help page, then enter six if that word means gaps. Six gaps, not seven, stays.
9. The intra-day correction is only in `BP-11-ALT-long-warning.md`. A forced close can fire during the day on the live price. The 13 March low, 4,107, is 3,804 under 7,911, about 48 percent, against about 37 percent close to close. No liquidation price and no multiple are invented. The main BP-11 script does not teach that mechanism.

## Legal

C1. Every lesson, including the ALT file, uses this day line: "This lesson uses the end of each UTC day, the world's standard clock, which is 11am Sydney time in daylight saving, 10am otherwise."

C2. In every lesson the full disclaimer is the paragraph immediately after the title, before any teaching. The canonical sentences are unchanged. The next sentences name the prices as public historical daily prices, marked Example, say the range uses the high and the low of that window, and say inside or outside uses the daily close.

C3, the cheap optional. Range edges are window highs and lows, not extreme closes. BP-11 states the summer edges as the 11 September 2023 low and the 23 July 2023 high. BP-10 states that 56,555 and 72,715 are the high and the low of that window.

BP-03. Published rungs, as in numbers item 1. Size is one sentence of arithmetic: 600 dollars across 6 orders is 100 dollars each, not a size for an account, and size stays off the page until the finish rule exists. Tax reminder: a swap is treated like a sale, so a fill can belong in the journal. General information, not tax advice. The API secret reminder is included: it can place trades and sometimes move money out, so withdrawal permissions stay off.

BP-04. Eight and five, and the March figures, as in numbers items 5 and 6. The contract exclusion now says that other kind of trading can be a financial product, it is higher risk, and this course does not teach it or recommend it.

BP-05. Day line, disclaimer, fee, ladder and 3.3 percent, as above. 27,630 is the middle and the worked pair's sell. 26,730 is the buy.

BP-06. Day line and disclaimer only. The figures were already accepted.

BP-07. Disclaimer before the real-account confirm sentence. After the contract and multiple definition: a contract or a multiple can be a financial product, it is higher risk, this course does not teach it or recommend it, and a prefilled contract setting or multiple is cleared or the form is left. Numbers item 8 is applied.

BP-08. Realised means a finished pair, both the buy and the later sell, and it is not money you made. Unrealised means coin still held, priced at the latest close, and it is not a tax figure. The tax reminder is included. The fourth row may stay blank. The fee is about US$0.54 on 0.01 coin, or 54.36 on a whole coin at the taught prices.

BP-09. Eight and five, with the same rule as BP-04. Four and three is named only as a wrong page.

BP-10. A multiple means borrowed size, can be a financial product, is higher risk, and is not taught or recommended. Scaling is a second written spot page, not a multiple. The "because you are ready" reason is removed. The page-two paragraph is marked as hindsight after 24 June 2024, and it says you would not have known that on the first day. The arithmetic is unchanged: width 16,160, about 2,693, six times 2,693 is 16,158, about three times the summer width, and six times 900 fits page one only.

BP-11, the major cut. The lesson to record no longer teaches margin, contracts, liquidation, or isolated versus cross. One short exclusion says we don't cover these, they are financial products with higher risk, and a spot holding is not closed for you by a drop in the coin's price. The rest of the lesson is a spot-page recap: edges, ladder, pair, fee, three completed pairs, eight and five, the stop, paper, and the journal. The longer mechanism, including the 48 percent intra-day correction, is only in `BP-11-ALT-long-warning.md`, marked NEEDS STEWART + COUNSEL. "Then you choose" is removed from that file.

Pass lists for BP-03, BP-04, BP-05 and BP-11 were updated where the on-screen card changed. Every pass list remains draft, pass false, needs_score true, with no scores.
