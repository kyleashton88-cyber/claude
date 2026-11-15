# Self-check — Arty trade plan v2

Run date: 15 November 2026. PDF: `clients/arty/Arty_Trade_Plan_v2.pdf`, 15 A4 pages.
Builder: `python3 clients/arty/build/build.py` (asserts, charts, print, text audit, page images).

## 1. Layout

Every page was rendered to PNG at 150 dpi and read back.

| Page | What was checked | Result |
| --- | --- | --- |
| 1 | Cover type, chart, contents 2–15, yellow rule, full disclaimer | Fits. Nothing clipped. |
| 2 | Percent table, glossary, disclaimer box, footer | Last glossary line and both disclaimers visible. |
| 3 | Six rules, watchlist, DOGE note, ticker steps | Ends cleanly above the footer. |
| 4 | Ladder chart, four-rung table | Chart title, USDT axis, legend, and example caption all on the page. |
| 5 | Sizing chart and worked table | 4.00 and 2.40 labels sit clear of the axis. 750.00 halt bar is labelled. |
| 6 | Leverage chart, formulas, 5× gate | Dashed-line note is in the axis label, not across a bar. Last gate line is above the footer. |
| 7 | Range steps and candle diagram | Swing, ATR buffer, and example badge readable. |
| 8 | Fee chart and worked grid table | Shaded fail region, 0.876% marker, and 0.0946 USDT row all visible. |
| 9 | Price chart and full-scale strip | Grid lines, middle third, launch dot, and 2,015 / 2,415 / 3,585 / 3,985 marks do not cover the axis numbers. |
| 10 | Gate drawing and checks 1–22 | All 22 lines are on the page. Footer clear. |
| 11 | Close decision picture and the numbered rules | Last sentence (“Do not widen, shift, or top up.”) is above the footer. |
| 12 | Daily check and journal fields | Full field list, including fees, funding, and the exit types. |
| 13 | Weekly card | Tick column and initials line present. |
| 14 | Roadmap and deposit steps | Week blocks and the 5,000.00 worked case both on the page. |
| 15 | Sign-off, screen list, disclaimer | Signature lines and the full disclaimer visible. |

No orphan heading, no chart cut by a page edge, no 16th page. The first cover pass left a large empty navy field; a contents list and a taller example chart now fill it. That second cover was re-rendered and read.

## 2. Arithmetic

`build/plan_math.py` asserts these identities, and the PDF text contains the displayed figures.

Starter account 500.00 USDT:

- Margin at 10% = 50.00. Planned stop = 50.00 × 0.08 = 4.00 (0.80% of 500.00). The +4.8% close = 2.40 (0.48%).
- 1% cap = 5.00. A supposed 70.00 minimum × 0.08 = 5.60, which fails the cap.
- Week −3% = 15.00. Window −6% = 30.00. Soft halt −10% = 50.00. Hard halt −15% = 75.00.
- Three stops = 12.00, inside 15.00. Four planned stops = 16.00, over 15.00.

Deposit case, trading result unchanged, equity 500.00 + 4,500.00 = 5,000.00:

- Week 150.00. Window 300.00. Soft halt 500.00. Hard halt 750.00.
- Phase-in margin 5% = 250.00, planned stop 20.00 (0.40%). Later margin 10% = 500.00, planned stop 40.00 (0.80%).
- The +4.8% close on a 500.00 margin is 24.00.

Leverage, maintenance assumption 0.50%, fictional price 3,000:

- Distance = 1/leverage − 0.50%. 3× = 32.833…% (written 32.83%). 5× = 19.50%.
- Long liquidation = price × (1 − 1/leverage + 0.005). 3× = 2,015.00. 5× = 2,415.00.
- Short liquidation = price × (1 + 1/leverage − 0.005). 3× = 3,985.00. 5× = 3,585.00.
- Full-position move for an 8% margin loss = 8% ÷ leverage. 3× = 2.666…% (written 2.67%), 80 USDT. 5× = 1.60%, 48 USDT.

Example range, not a quote:

- Bounds 3,000 × (1 ± 0.055) = 2,835 and 3,165. Span 330. Twelve intervals, step 27.50.
- Worst gross step = 27.50 / 3,137.50 = 0.876494…% (written 0.876%).
- Planning round trip = 2 × 0.05% + 0.02% = 0.120%. Net = 0.756%.
- One order = 50 × 3 / 12 = 12.50. Gross 0.1096 USDT. Costs 0.0150 USDT. Left 0.0946 USDT.
- Buffer prices 2,835 × 0.97 = 2,749.95 and 3,165 × 1.03 = 3,259.95. Both 3× and 5× liquidation prices sit outside them on this example.
- Middle third 2,945 to 3,055. Outer 10% at 2,868 and 3,132.
- Example daily ATR 60 is 2.00% of 3,000. 4 × ATR = 8.00%, so the ETH floor of 11% binds. 8 × ATR = 16.00%, so 11% is under the maximum. Swings 2,865 and 3,135 plus or minus 30 land on 2,835 and 3,165.

## 3. Task coverage

| Required rule | Where it is explicit |
| --- | --- |
| Pre-launch checklist | Page 10, checks 1–22, and the gate drawing |
| Range qualification | Page 7, steps 1–7, plus checks 10–14 |
| Take-profit, stop, manual close | Pages 2, 5, 6, and 11. Manual close with a negative result counts as a stop. |
| Range-break handling | Page 11: 4H close outside, two wicks, outer 10% with 2× volume |
| Time-based exit | Page 11: 7 days with fewer than 3 round trips, 14 days absolute |
| Stop versus grid and liquidation at 3× and 5× | Pages 6 and 9 |
| Position size, 500 example, minimums, fees, funding | Pages 5, 8, and 11 |
| Risk per bot and the 1% ceiling | Page 5 |
| Drawdown ladder and circuit breakers | Page 4 |
| Grid range, spacing, ATR, fee, amount left after costs | Pages 7 and 8 |
| When to pause or stop | Page 11, including volatility, news, funding, and exchange trouble |
| Journal fields | Page 12 |
| Daily, weekly, and end-of-month review | Pages 12, 13, and 14 |
| Futures risks, including cross margin and liquidation | Pages 2, 6, and 11 |
| Week-4 deposit | Page 14, seven steps, worked at 5,000.00 only if the screen matches |
| Ticker check, including DOGE rather than DODG | Page 3 |

## 4. Wording scan

PDF text search after the final build:

| Phrase | Hits |
| --- | --- |
| Market Pros | 0 |
| passive income | 0 |
| will make | 0 |
| 10% weekly | 0 |
| target | 0 |
| growth | 0 |
| profit | 0 |
| guarantee | 3, each inside “not a guarantee of any result” in the disclaimer (cover, page 2, sign-off) |

The remaining “10%” hits are the margin cap and the soft-halt line, not a weekly result. “Per week” appears once, as “one process note per week.”

## 5. Disclaimer

Present in full on the cover, in the box on page 2, and in the box on page 15. The footer on pages 2–15 repeats: educational information only, not financial advice, total loss, examples are not indicative of future results, the reader decides, Pionex is not affiliated, verify current settings.

No external illustration was required. Nothing was listed in an image-request file.
