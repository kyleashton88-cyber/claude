# Grid Bot win-rate and growth optimisation: walk-forward study (10 Nov 2026)

Prepared for Stewart. This is historical simulation for research only. It is not a forecast and not financial advice. Nothing was changed in TradingView, in any live alert or in any account, and nothing was published. The live files (`grid-bot-improved-merged-deploy*.pine`, `grid-screener*.pine`) are untouched.

## 1. The answer first

- **Target (win rate above 75% AND capital growth of at least 60%), out of sample, on BTC, ETH and SOL with one set of settings: NOT met.** No settings met it, robust or not. I tested about 31,000 grid configurations on 1h and 18,000 on 4h, plus 10,000 Cipher B configurations. Even when I picked results **with hindsight** from the untouched last 30%, none reached 60% on all three coins. The best all-three result with a win rate of 75% or more was about +25–26% (1h and 4h), and that comes from cherry-picking.
- **A win rate above 75% is easy to get. Growth is the hard part.** The win rate goes up almost automatically with more grid lines (a smaller target) and a wider stop. 98% of the one-step variations around the recommended settings (and all 40 random two-step ones) still win more than 75% of trades out of sample. But the average loss is about **7–15× the average win**, so the high win rate tells you almost nothing about profit.
- **Recommended trade-off, v3 (4h chart, new "Auto" mode).** Out of sample (15 Nov 2025 → 10 Nov 2026, about 12 months), it won **97–100%** of trades with growth of **+5.0% BTC, +9.2% ETH and +17.0% SOL** and max drawdown of **≤4.7%** (122 trades in total). In sample (Aug 2023 → Nov 2025) it won 94–97% with growth of +9.9% to +13.2% and max drawdown up to 13.6%. **It lost −7.2% on ZEC out of sample**, and ZEC is the coin the live alert was set up on.
- **Baseline (live v2 settings, 1h).** It wins 59–69% of trades, with growth from **−2.9% to −13.9% out of sample** and a profit factor of 0.67–0.86. It loses money after 0.1% fees plus slippage on every coin tested. At the script's own 0.055% fee it is still negative on BTC, SOL and ZEC.
- **Cipher B (VuManChu reference strategy, which reverses on every WaveTrend cross).** It wins 27–35% of trades and loses 59–100% of capital on BTC, ETH and SOL, at both 1h and 4h. ZEC 4h out of sample was the only gain (+160%), with a 54% drawdown, a one-coin fluke. None of the 10,000 dot + ATR TP/SL variants had a robust in-sample edge.

## 2. What each indicator signals and what counts as a "win"

| Script | What it does | Unit counted as a trade / "win" |
|---|---|---|
| `grid-bot-improved-merged-deploy(-weekday).pine` (live **Grid Bot v2**) | Builds a frozen geometric grid (Donchian 100, 10 lines) only when the market is ranging (ADX < 22 and BB width < 8%). It buys a level crossed downward below the midline and sells at the next level up, with shorts mirrored above the midline. Hard stop at the range edge ±1 ATR; close-all on a range break or at the opposite edge. Spike filter, circuit breaker (4 losses or 10% drawdown pauses for 24 bars) and a 20% hard max-drawdown halt. | **One grid leg** (entry at level i, exit at level i±1, a stop or a close-all). Win = the leg's net P&L after fees is above 0. This is what TradingView's "Percent profitable" shows. |
| `…-weekday` variant | Same strategy. The Sat/Sun (Sydney) gate only blocks **alerts**, not strategy trades. | Same. Note: a person following the alerts also misses weekend **exit** alerts. |
| `grid-screener*.pine` (1h and 4h-data variants) | A 0–100 "grid-fit" ranking of 36 coins (ADX, BB width, ATR%, midline crosses, range containment). It is descriptive and places no trades. | No win rate exists. It isn't a trading signal, so it wasn't optimised. |
| `market-cipher/refs/vumanchu-cipher-b*.pine` (public community imitation, not official Market Cipher) | WaveTrend wt1/wt2. Buy dot = cross up with wt2 ≤ −53; sell dot = cross down with wt2 ≥ +53. The reference strategy goes long when wt1 > wt2 and short when wt1 < wt2. | One position from entry to exit or reversal. |

No recorded live win rate exists. Memory, transcripts and the Alert Log hold only test rows (the PIPELINE-REPORT says 0 real TradingView alerts). So the baseline below is measured here.

## 3. Method

- **Data:** Binance public spot klines (`data-api.binance.vision`), BTCUSDT, ETHUSDT, SOLUSDT and ZECUSDT, 1h and 4h, from 1 Aug 2023 to 10 Nov 2026 UTC (28,729 1h bars and 7,183 4h bars per coin). The live scripts point at Bybit perps, so funding isn't modelled.
- **Engine:** a bar-by-bar Python/numba port of the v2 script (`grid_sim.py`) that follows TradingView's broker emulator:
  - signals on bar close, with market orders filled at the **next bar's open**;
  - `strategy.exit` limit and stop orders rest from the bar after they are placed, with gaps filled at the open;
  - the intrabar path follows TradingView's rule (open → nearer extreme → other extreme);
  - per-level legs, `maxOpen`, cooldown, spike filter, circuit breaker and the 20% hard-drawdown halt are all modelled;
  - Pine-style RMA/EMA/ATR/DMI.
- **Costs:** a **0.10% fee per side** plus **0.03% slippage** on market and stop fills (limit take-profits get no slippage, as in TradingView). Cost sensitivity was also run at 0.055%/0.01%, 0.10%/0.10% and 0.15%/0.10%.
- **Sizing:** $10,000 start, % of equity per leg and compounding. Total exposure is never above 100% of equity (qty% × maxOpen ≤ 100, so no leverage).
- **Walk-forward:**
  - the first 70% of bars is in sample (IS, 1 Aug 2023 → 15 Nov 2025);
  - the last 30% is out of sample (OOS, 15/16 Nov 2025 → 10 Nov 2026), untouched during selection;
  - selection was on **IS only**, requiring at least 30 IS trades per coin and scoring on the **worst** coin of BTC/ETH/SOL (one setting for all three);
  - candidates were then checked OOS, on ZEC as an extra coin, against 40 random two-parameter neighbours, one parameter at a time, and across cost levels.
- **Search space:** mode (Neutral/Long/Short/new Auto), range method (Donchian/ATR/Percentile), lookback 50–300, grid lines 4–20, min step 0.4–2%, stop 0.5–8 ATR, ADX/BBW regime on/off and thresholds, qty 5–50%, max open 2–10, edge TP, cooldown 0–24, spike filter, circuit breaker, hard-drawdown 20/30/off, weekday-only entries, 4h EMA200 side filter, and chart EMA 100/200.

## 4. Baseline: live v2 settings (0.10% fee + 0.03% slippage)

IS = 1 Aug 2023 → 15 Nov 2025 and OOS = 15 Nov 2025 → 10 Nov 2026, each with a fresh $10,000. Growth is total over the window, not annualised. Avg win/loss $ is per leg; % move is the price move on that leg.

#### Baseline (live v2 settings) 1h

| Symbol | Window | Trades | Win % | Growth % | Max DD % | Profit factor | Avg win $ | Avg loss $ | Expectancy $/trade | Avg win % move | Avg loss % move |
|---|---|---|---|---|---|---|---|---|---|---|---|
| BTC | IS | 472 | 61.4 | -9.7 | 10.4 | 0.66 | 4.97 | -12.07 | -1.60 | +1.17 | -2.42 |
| BTC | OOS | 227 | 67.0 | -2.9 | 3.7 | 0.80 | 4.86 | -12.32 | -0.81 | +1.10 | -2.37 |
| ETH | IS | 663 | 68.3 | -1.6 | 4.7 | 1.06 | 7.13 | -14.52 | +0.27 | +1.54 | -2.74 |
| ETH | OOS | 245 | 69.0 | -2.8 | 4.2 | 0.86 | 5.77 | -14.90 | -0.64 | +1.30 | -2.90 |
| SOL | IS | 893 | 60.5 | -15.8 | 16.5 | 0.80 | 8.45 | -16.24 | -1.31 | +1.96 | -3.34 |
| SOL | OOS | 354 | 65.8 | -5.0 | 7.6 | 0.83 | 6.65 | -15.43 | -0.90 | +1.45 | -2.95 |
| ZEC | IS | 841 | 65.0 | -8.4 | 11.7 | 0.92 | 9.21 | -18.60 | -0.52 | +2.05 | -3.65 |
| ZEC | OOS | 354 | 58.8 | -13.9 | 14.3 | 0.67 | 11.37 | -24.17 | -3.28 | +2.55 | -4.85 |

#### Baseline (live v2 settings) 1h @script costs 0.055%

| Symbol | Window | Trades | Win % | Growth % | Max DD % | Profit factor | Avg win $ | Avg loss $ | Expectancy $/trade | Avg win % move | Avg loss % move |
|---|---|---|---|---|---|---|---|---|---|---|---|
| BTC | FULL | 699 | 63.2 | -8.3 | 9.9 | 0.78 | 5.23 | -11.53 | -0.93 | +1.18 | -2.34 |
| ETH | FULL | 909 | 68.5 | +1.6 | 6.6 | 1.10 | 7.31 | -14.47 | +0.46 | +1.50 | -2.72 |
| SOL | FULL | 1247 | 62.0 | -13.1 | 13.4 | 0.87 | 8.22 | -15.50 | -0.79 | +1.84 | -3.18 |
| ZEC | FULL | 1195 | 63.2 | -14.6 | 17.3 | 0.88 | 10.30 | -20.15 | -0.91 | +2.21 | -3.99 |

#### Baseline (live v2 settings) 4h

| Symbol | Window | Trades | Win % | Growth % | Max DD % | Profit factor | Avg win $ | Avg loss $ | Expectancy $/trade | Avg win % move | Avg loss % move |
|---|---|---|---|---|---|---|---|---|---|---|---|
| BTC | IS | 191 | 52.9 | -7.9 | 8.3 | 0.59 | 9.90 | -18.83 | -3.64 | +2.21 | -3.72 |
| BTC | OOS | 91 | 72.5 | -0.4 | 2.6 | 1.02 | 8.08 | -20.96 | +0.10 | +1.74 | -3.94 |
| ETH | IS | 146 | 65.8 | -0.4 | 3.0 | 1.09 | 14.38 | -25.40 | +0.75 | +3.06 | -4.75 |
| ETH | OOS | 68 | 66.2 | +0.4 | 1.5 | 1.15 | 12.61 | -21.45 | +1.09 | +2.65 | -4.00 |
| SOL | IS | 102 | 53.9 | -7.3 | 7.3 | 0.59 | 17.80 | -35.34 | -6.69 | +3.91 | -6.80 |
| SOL | OOS | 83 | 66.3 | +0.4 | 2.7 | 1.12 | 13.49 | -23.62 | +0.97 | +2.82 | -4.39 |
| ZEC | IS | 108 | 63.0 | -5.1 | 9.0 | 0.71 | 16.28 | -39.17 | -4.26 | +3.43 | -7.04 |
| ZEC | OOS | 12 | 75.0 | +0.2 | 1.0 | 1.21 | 15.94 | -39.57 | +2.06 | +3.33 | -7.50 |


## 5. Recommended v3: in sample vs out of sample, per coin

ZEC wasn't used in selection; it's shown as an independent check.

#### Recommended v3 (4h, Auto)

| Symbol | Window | Trades | Win % | Growth % | Max DD % | Profit factor | Avg win $ | Avg loss $ | Expectancy $/trade | Avg win % move | Avg loss % move |
|---|---|---|---|---|---|---|---|---|---|---|---|
| BTC | IS | 64 | 96.9 | +9.9 | 7.7 | 3.58 | 23.71 | -204.99 | +16.56 | +2.43 | -16.74 |
| BTC | OOS | 21 | 100.0 | +5.0 | 2.4 | ∞ (no losses) | 25.03 | 0.00 | +25.03 | +2.63 | +0.00 |
| ETH | IS | 116 | 95.7 | +13.2 | 13.6 | 1.87 | 28.08 | -333.01 | +12.51 | +2.70 | -21.57 |
| ETH | OOS | 38 | 97.4 | +9.2 | 4.7 | 5.66 | 31.50 | -205.93 | +25.25 | +3.21 | -18.49 |
| SOL | IS | 109 | 93.6 | +11.0 | 12.4 | 1.48 | 37.07 | -365.57 | +11.21 | +3.51 | -26.70 |
| SOL | OOS | 63 | 100.0 | +17.0 | 4.0 | ∞ (no losses) | 28.03 | 0.00 | +28.03 | +2.78 | +0.00 |
| ZEC | IS | 85 | 91.8 | +2.8 | 13.4 | 1.19 | 28.77 | -268.41 | +4.29 | +3.10 | -23.30 |
| ZEC | OOS | 32 | 90.6 | -7.2 | 16.9 | 0.60 | 35.19 | -570.32 | -21.57 | +4.00 | -41.31 |


#### For comparison: highest-growth candidate with a 75%+ win rate (1h, fragile, not recommended)

| Symbol | Window | Trades | Win % | Growth % | Max DD % | Profit factor | Avg win $ | Avg loss $ | Expectancy $/trade | Avg win % move | Avg loss % move |
|---|---|---|---|---|---|---|---|---|---|---|---|
| BTC | IS | 284 | 91.9 | +35.8 | 13.4 | 1.78 | 37.27 | -237.02 | +15.06 | +1.65 | -8.56 |
| BTC | OOS | 66 | 92.4 | +14.1 | 10.0 | 2.60 | 41.35 | -193.94 | +23.53 | +2.06 | -7.93 |
| ETH | IS | 181 | 91.7 | +11.4 | 20.0 | 1.21 | 52.95 | -483.17 | +8.52 | +2.49 | -16.27 |
| ETH | OOS | 93 | 92.5 | +16.9 | 13.9 | 2.04 | 43.11 | -259.89 | +20.30 | +2.18 | -10.77 |
| SOL | IS | 51 | 94.1 | +11.2 | 21.6 | 1.42 | 87.46 | -985.90 | +24.32 | +3.84 | -35.73 |
| SOL | OOS | 92 | 91.3 | +11.1 | 13.9 | 1.39 | 55.07 | -415.31 | +14.17 | +2.79 | -15.68 |
| ZEC | IS | 56 | 78.6 | -18.5 | 20.1 | 0.51 | 40.74 | -294.30 | -31.05 | +2.28 | -12.40 |
| ZEC | OOS | 13 | 53.8 | -16.0 | 20.1 | 0.32 | 105.48 | -386.16 | -121.43 | +5.78 | -16.34 |


#### Cipher B reference strategy (WT cross, stop and reverse, 100% equity)

##### Cipher B ref strategy (WT cross SAR) 1h

| Symbol | Window | Trades | Win % | Growth % | Max DD % | Profit factor | Avg win $ | Avg loss $ | Expectancy $/trade | Avg win % move | Avg loss % move |
|---|---|---|---|---|---|---|---|---|---|---|---|
| BTC | IS | 3931 | 27.0 | -100.0 | 100.0 | 0.54 | 7.03 | -4.81 | -1.61 | +1.18 | -0.52 |
| BTC | OOS | 1736 | 26.6 | -98.7 | 98.9 | 0.78 | 36.57 | -17.04 | -2.80 | +1.11 | -0.46 |
| ETH | IS | 3903 | 29.8 | -100.0 | 100.0 | 0.57 | 7.35 | -5.46 | -1.64 | +1.53 | -0.75 |
| ETH | OOS | 1718 | 27.3 | -98.6 | 98.9 | 0.74 | 36.58 | -18.47 | -3.44 | +1.48 | -0.61 |
| SOL | IS | 3967 | 31.5 | -100.0 | 100.0 | 0.77 | 16.16 | -9.68 | -1.54 | +2.05 | -1.09 |
| SOL | OOS | 1738 | 28.5 | -98.8 | 99.1 | 0.89 | 65.63 | -29.25 | -2.23 | +1.64 | -0.71 |
| ZEC | IS | 4127 | 30.3 | -100.0 | 100.0 | 0.54 | 6.71 | -5.39 | -1.72 | +2.41 | -1.23 |
| ZEC | OOS | 1692 | 34.1 | -98.9 | 99.3 | 0.71 | 33.40 | -24.21 | -4.57 | +2.77 | -1.47 |



##### Cipher B ref strategy (WT cross SAR) 4h

| Symbol | Window | Trades | Win % | Growth % | Max DD % | Profit factor | Avg win $ | Avg loss $ | Expectancy $/trade | Avg win % move | Avg loss % move |
|---|---|---|---|---|---|---|---|---|---|---|---|
| BTC | IS | 987 | 32.5 | -90.3 | 90.7 | 0.87 | 92.58 | -51.48 | -4.63 | +2.19 | -1.07 |
| BTC | OOS | 403 | 32.5 | -64.4 | 67.9 | 0.82 | 132.62 | -78.16 | -9.65 | +2.20 | -1.10 |
| ETH | IS | 963 | 34.3 | -94.2 | 94.4 | 0.83 | 86.97 | -54.50 | -6.02 | +2.87 | -1.57 |
| ETH | OOS | 415 | 31.6 | -58.7 | 68.0 | 0.92 | 222.48 | -111.91 | -6.36 | +2.97 | -1.33 |
| SOL | IS | 990 | 35.5 | -96.7 | 97.1 | 0.90 | 149.16 | -91.20 | -5.98 | +3.95 | -2.26 |
| SOL | OOS | 407 | 31.7 | -86.3 | 86.3 | 0.67 | 110.55 | -76.77 | -17.40 | +3.08 | -1.77 |
| ZEC | IS | 992 | 32.6 | -93.9 | 98.7 | 0.76 | 69.76 | -44.48 | -7.28 | +5.19 | -2.38 |
| ZEC | OOS | 403 | 35.0 | +160.5 | 54.5 | 1.13 | 1615.10 | -767.55 | +66.09 | +6.91 | -2.74 |
## 6. Baseline vs recommended settings (inputs)

| Input | Baseline (live v2) | Recommended v3 | Why |
|---|---|---|---|
| Chart timeframe | 1h | **4h** | 4h beat 1h on robustness: fewer, larger grid steps cover the 0.2%+ round-trip cost. |
| Grid mode | Neutral | **Auto** (new) | Neutral was the worst mode on every coin. Auto opens long legs only when close > EMA100 **and** the 4h close > 4h EMA200, short legs only when both are below, and no new legs in between. |
| HTF side filter | n/a | **On (4h EMA200)** | It improved the median result in both timeframes. |
| Range method / lookback | Donchian / 100 | **Percentile 95/5 / 200** | Longer lookbacks (200–300) were consistently better. |
| Grid lines / spacing | 10 / Geometric | **14** / Geometric | More lines raise the win rate. Below 10 lines the edge disappears. |
| Min step % | 0.6 | **1.0** | Keeps each step well above costs. |
| Trend EMA | 200 | **100** | |
| ADX/BBW regime filter | On (22 / 8%) | **Off** | Turning it on with Auto cut out the profitable trend-aligned periods (OOS worst coin −14.8%). |
| Equity % per leg / max open | 5% / 6 | **10% / 6** (max 60% of equity deployed) | 5% halves both return and drawdown; 15% gives about 1.5× the return with a 20% in-sample drawdown. |
| Range-break stop | 1.0 ATR | **5.0 ATR** | This is what lifts the win rate, and it is also why the average loss is large (see the warning below). |
| Spike filter | On | **Off** | On, it cut the OOS worst coin from +5.0% to −1.1%. |
| Circuit breaker / hard DD | 4 losses or 10% DD / 20% | unchanged | Results are the same with both off, so the halt doesn't prop up the numbers. |
| Cooldown | 12 | 12 | |
| Weekday-only entries | n/a | **Off** (input added) | Mon–Fri-only entries hurt in sample (−16% worst coin). Weekend alerts stay gated as before. |
| Commission in `strategy()` | 0.055% | **0.10%** | Matches the cost assumption tested here. |

## 7. Robustness of the recommendation (4h, Auto)

- **Costs:** worst-coin OOS growth was +5.3% at 0.055%/0.01%, +4.9% at 0.10%/0.10% and +4.7% at 0.15%/0.10%. In sample it was +10.7%, +9.4% and +8.7%. Costs are not what drives the result.
- **Neighbourhood:**
  - Of 40 random two-parameter neighbours, 60% stay positive in sample and 62% stay positive out of sample (median OOS worst coin +4.3%), and **100% keep a win rate of 75% or more**.
  - One-step changes: 71% stay positive OOS and 98% keep 75%+ wins.
  - Sensitive parameters: the range lookback (300 holds up; 50–150 turn negative), the stop distance (any value other than 5 ATR is weaker in sample), the spike filter, and the regime filter. Insensitive: ADX/BBW thresholds (unused), min step 0.4–1.5, max open ≥ 3, and the circuit breaker on/off.
  - **This is a narrow peak in a mostly negative landscape, not a broad plateau.** In the 4h search only about 4% of all configurations had a 75%+ win rate, positive growth and a drawdown under 20% in sample (about 1% on 1h).
- **Scaling to chase 60%:**
  - Growth scales roughly with size. At 15% per leg (90% max deployed), OOS reached +7.6% / +26.4% (worst/best coin) with an in-sample drawdown of 20.1%, which trips the hard stop.
  - Getting to +60% on the worst coin would take roughly 10× the current exposure, which means leverage, with drawdowns far beyond 20%. I don't recommend it.
- **Why high win rates aren't profit:**
  - In sample, v3's average winning leg is +2.4% to +3.5% of the leg's notional, and its average losing leg is −17% to −27%. In dollars that's about $24–37 per win against $205–366 per loss.
  - One range break that stops out several legs can erase 10–15 wins.
  - The OOS window had **no losing leg on BTC or SOL**. That's a favourable year for this rule, not evidence that losses are gone.

## 8. Best trade-offs, as asked

| Trade-off | Settings | OOS result (BTC / ETH / SOL) | Verdict |
|---|---|---|---|
| **Highest win rate with 60%+ growth** | None robust. With hindsight, 13 configs reached 60%+ on **one** coin (all SOL), e.g. 1h Neutral, 20 lines, 8 ATR stop, 25% per leg: SOL OOS +110%. | All 13 lost money in sample on at least one of BTC/ETH/SOL (11 of the 13 on SOL itself, down to −89%). | Curve-fit and unusable. |
| **Highest growth with 75%+ win rate (IS-selected)** | 1h, Auto, ATR-range 50 × 6, 8 lines, min step 0.8, 8 ATR stop, 20% × 3 legs, no edge TP (`params_1h_4194.json`) | 92.4% / 92.5% / 91.3% wins; **+14.1% / +16.9% / +11.1%**; max DD 10.0 / 13.9 / 13.9% | **Fragile.** In sample it only survives because the 20% hard-drawdown halt stops it; with the halt off, the in-sample worst coin is −54%. ZEC OOS −16%. Not recommended. |
| **Recommended balance** | 4h v3 (above) | 100% / 97.4% / 100% wins; **+5.0% / +9.2% / +17.0%**; max DD 2.4 / 4.7 / 4.0% | It's the most stable of the candidates, but well short of 60%. |

## 9. Cipher B (VuManChu WaveTrend) results

- **Reference strategy, which reverses on every WT cross at 100% equity:** win rates of 26–35%. On BTC, ETH and SOL it loses 59–100% at both 1h and 4h: the many small losses plus 0.2% round-trip costs on about 1,700 trades a year at 1h wipe it out. ZEC 4h OOS was the only exception (+160%, with a 54% drawdown).
- **Dot-only variants** (buy/sell dots at ±30 to ±70, ATR TP 0.5–4 and SL 1–6, max-hold, EMA200 / 4h EMA200 / ADX filters, long/short/both, weekday filter; 6,000 configs at 1h and 4,000 at 4h):
  - none met 75% + 60% in or out of sample;
  - high win rates (80–95%) appear only with TP ≤ 1 ATR and SL ≥ 3–6 ATR, with in-sample growth in single digits and negative OOS growth on at least one coin.
  - Full results: `cipher_1h.csv`, `cipher_4h.csv`.

## 10. Caveats

1. **Model parity isn't verified in TradingView.** I wasn't allowed to touch TradingView, so the Python model hasn't been reconciled with the Strategy Tester. Before relying on any number:
   - load `grid-bot-improved-v3.pine` on a 4h BINANCE:BTCUSDT chart (spot, the same data used here) with the default inputs;
   - compare the trade count, win rate and net profit with the tables above. Small differences are expected from the Percentile-interpolation method, EMA seeding and the intrabar fill rules.
2. The v3 file is written in Pine **v5** as requested (the live files are v6). I haven't compiled it. I kept the changes to the v6 logic minimal and avoided v6-only syntax, but it needs a first compile check in the Pine editor.
3. **Data:** Binance spot data, not Bybit perps, so there's no funding cost. Funding of about 0.01% per 8h on open legs would cut growth, more so on 4h, where legs are held longer.
4. **Regime dependence:** in sample was mostly a BTC/SOL uptrend and out of sample mostly a downtrend for BTC. Auto mode switches sides, but only about 12 months of OOS data exist, and the OOS window had unusually few range breaks for this rule.
5. **ZEC**, the coin the live alert was set up on, is negative OOS for v3 (−7.2%, 16.9% drawdown) and for the baseline (−13.9%). I wouldn't run either on ZEC without more evidence.
6. Out-of-sample trade counts per coin are 21 (BTC), 38 (ETH) and 63 (SOL), 122 in total. BTC alone is under 30, so a 100% BTC win rate rests on a small sample.
7. The weekday variant gates all alerts on Sat/Sun Sydney time, **including exits**. Anyone following alerts by hand would hold weekend legs without exit notices. The backtest assumes the strategy itself exits.
8. Win rate isn't a quality measure for this kind of strategy, and nothing here should be presented to members as a win-rate claim. That matches the education-only guardrails.

## 11. Files

All in `/workspace/tradingview/` unless noted:
- `grid-bot-improved-v3.pine`: the new strategy (Pine v5) with the recommended defaults, Auto mode, an HTF side filter, a weekday-only entry option and the `src:"gridv3"` payload tag. The live v2 files are unchanged.
- `optimisation-2026-11-10/REPORT.md`: this report.
- `optimisation-2026-11-10/`:
  - `fetch.py` and `data/*.csv`: OHLCV;
  - `ind.py`, `grid_sim.py` (v2/v3 engine) and `cipher_sim.py`;
  - `baseline.py`, `search.py`, `oos.py`, `oos_all.py` (hindsight diagnostic), `robust.py`, `plateau.py`, `final.py` and `cipher_search.py`;
  - results: `baseline.csv`, `search_*_IS_*.csv`, `oos_*.csv`, `oos_all_*.csv`, `robust_*.csv` / `.txt`, `final_results.csv`, `params_*.json` (exact inputs), `tables.md`, `cipher_*.csv`.
