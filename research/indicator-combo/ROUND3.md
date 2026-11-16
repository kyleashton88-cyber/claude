# Round 3 holdout

Education only. Not financial advice. Past performance is not a reliable indicator of future results.

Leverage can liquidate a position before a stop fills. Isolated margin does not limit losses to the posted margin if a gap goes through the liquidation price in the same move; in this model a gap through liquidation wipes the posted margin.

Variants logged: 634. Selection did not use 16 May 2026 onward.

## Locked from the walk-forward

- Arithmetic: range `atr3`, gate `hyst_age`, exit `time36`, levels 8, stop 4.0%, min step 0.01. Selection-fold win rate 74.0% on n=1126, mean return -0.05%.
- Geometric: range `atr3`, gate `hyst_liq`, exit `time36`, levels 6, stop 4.0%, min step 0.01. Selection-fold win rate 71.4% on n=1104, mean return -0.08%.

## Out of sample

Win rate is per deployment, after fees and recorded funding. The interval is a 95% Wilson interval. n below 20 is not a result.

| Mode | Coin | TF | Lev | Win rate | 95% CI | n | Mean return | Max DD | Stops | Liq |
|---|---|---|---|---|---|---|---|---|---|---|
| Arithmetic | BTC | 1h | 1x | — not meaningful | — | 0 | — | — | 0 | 0 |
| Arithmetic | BTC | 1h | 2x | — not meaningful | — | 0 | — | — | 0 | 0 |
| Arithmetic | BTC | 1h | 3x | — not meaningful | — | 0 | — | — | 0 | 0 |
| Arithmetic | BTC | 1h | 5x | — not meaningful | — | 0 | — | — | 0 | 0 |
| Arithmetic | BTC | 4h | 1x | 100.0% not meaningful | 43.8–100.0% | 3 | 0.21% | 1.5% | 0 | 0 |
| Arithmetic | BTC | 4h | 2x | 100.0% not meaningful | 43.8–100.0% | 3 | 0.42% | 2.9% | 0 | 0 |
| Arithmetic | BTC | 4h | 3x | 100.0% not meaningful | 43.8–100.0% | 3 | 0.64% | 4.4% | 0 | 0 |
| Arithmetic | BTC | 4h | 5x | 100.0% not meaningful | 43.8–100.0% | 3 | 1.06% | 7.3% | 0 | 0 |
| Arithmetic | ETH | 1h | 1x | — not meaningful | — | 0 | — | — | 0 | 0 |
| Arithmetic | ETH | 1h | 2x | — not meaningful | — | 0 | — | — | 0 | 0 |
| Arithmetic | ETH | 1h | 3x | — not meaningful | — | 0 | — | — | 0 | 0 |
| Arithmetic | ETH | 1h | 5x | — not meaningful | — | 0 | — | — | 0 | 0 |
| Arithmetic | ETH | 4h | 1x | 64.7% not meaningful | 41.3–82.7% | 17 | -0.34% | 6.0% | 1 | 0 |
| Arithmetic | ETH | 4h | 2x | 64.7% not meaningful | 41.3–82.7% | 17 | -0.67% | 11.9% | 1 | 0 |
| Arithmetic | ETH | 4h | 3x | 64.7% not meaningful | 41.3–82.7% | 17 | -1.01% | 17.8% | 1 | 0 |
| Arithmetic | ETH | 4h | 5x | 64.7% not meaningful | 41.3–82.7% | 17 | -1.68% | 29.5% | 1 | 0 |
| Arithmetic | SOL | 1h | 1x | 83.3% not meaningful | 55.2–95.3% | 12 | 0.18% | 0.9% | 0 | 0 |
| Arithmetic | SOL | 1h | 2x | 83.3% not meaningful | 55.2–95.3% | 12 | 0.36% | 1.8% | 0 | 0 |
| Arithmetic | SOL | 1h | 3x | 83.3% not meaningful | 55.2–95.3% | 12 | 0.54% | 2.8% | 0 | 0 |
| Arithmetic | SOL | 1h | 5x | 83.3% not meaningful | 55.2–95.3% | 12 | 0.90% | 4.6% | 0 | 0 |
| Arithmetic | SOL | 4h | 1x | 67.6% | 50.8–80.9% | 34 | -0.01% | 5.3% | 1 | 0 |
| Arithmetic | SOL | 4h | 2x | 67.6% | 50.8–80.9% | 34 | -0.03% | 10.1% | 1 | 0 |
| Arithmetic | SOL | 4h | 3x | 67.6% | 50.8–80.9% | 34 | -0.04% | 14.5% | 1 | 0 |
| Arithmetic | SOL | 4h | 5x | 67.6% | 50.8–80.9% | 34 | -0.07% | 22.2% | 1 | 0 |
| Arithmetic | ZEC | 1h | 1x | 76.3% | 65.6–84.5% | 76 | -0.06% | 17.5% | 5 | 0 |
| Arithmetic | ZEC | 1h | 2x | 76.3% | 65.6–84.5% | 76 | -0.12% | 32.2% | 5 | 0 |
| Arithmetic | ZEC | 1h | 3x | 76.3% | 65.6–84.5% | 76 | -0.18% | 44.7% | 5 | 0 |
| Arithmetic | ZEC | 1h | 5x | 76.3% | 65.6–84.5% | 76 | -0.29% | 64.9% | 5 | 0 |
| Arithmetic | ZEC | 4h | 1x | 64.7% | 47.9–78.5% | 34 | -0.61% | 25.9% | 6 | 0 |
| Arithmetic | ZEC | 4h | 2x | 64.7% | 47.9–78.5% | 34 | -1.21% | 49.9% | 6 | 0 |
| Arithmetic | ZEC | 4h | 3x | 64.7% | 47.9–78.5% | 34 | -1.82% | 72.2% | 6 | 0 |
| Arithmetic | ZEC | 4h | 5x | 64.7% | 47.9–78.5% | 34 | -3.03% | 112.2% | 6 | 0 |
| Geometric | BTC | 1h | 1x | 88.9% not meaningful | 56.5–98.0% | 9 | 0.53% | 1.9% | 0 | 0 |
| Geometric | BTC | 1h | 2x | 88.9% not meaningful | 56.5–98.0% | 9 | 1.07% | 3.6% | 0 | 0 |
| Geometric | BTC | 1h | 3x | 88.9% not meaningful | 56.5–98.0% | 9 | 1.60% | 5.2% | 0 | 0 |
| Geometric | BTC | 1h | 5x | 88.9% not meaningful | 56.5–98.0% | 9 | 2.67% | 7.8% | 0 | 0 |
| Geometric | BTC | 4h | 1x | 62.1% | 44.0–77.3% | 29 | -0.24% | 13.3% | 2 | 0 |
| Geometric | BTC | 4h | 2x | 62.1% | 44.0–77.3% | 29 | -0.47% | 26.6% | 2 | 0 |
| Geometric | BTC | 4h | 3x | 62.1% | 44.0–77.3% | 29 | -0.71% | 39.8% | 2 | 0 |
| Geometric | BTC | 4h | 5x | 62.1% | 44.0–77.3% | 29 | -1.18% | 66.2% | 2 | 0 |
| Geometric | ETH | 1h | 1x | 71.9% | 54.6–84.4% | 32 | -0.10% | 9.0% | 1 | 0 |
| Geometric | ETH | 1h | 2x | 71.9% | 54.6–84.4% | 32 | -0.19% | 17.9% | 1 | 0 |
| Geometric | ETH | 1h | 3x | 71.9% | 54.6–84.4% | 32 | -0.29% | 26.7% | 1 | 0 |
| Geometric | ETH | 1h | 5x | 71.9% | 54.6–84.4% | 32 | -0.48% | 44.1% | 1 | 0 |
| Geometric | ETH | 4h | 1x | 66.7% | 48.8–80.8% | 30 | -0.69% | 20.9% | 5 | 0 |
| Geometric | ETH | 4h | 2x | 66.7% | 48.8–80.8% | 30 | -1.39% | 41.7% | 5 | 0 |
| Geometric | ETH | 4h | 3x | 66.7% | 48.8–80.8% | 30 | -2.08% | 62.5% | 5 | 0 |
| Geometric | ETH | 4h | 5x | 66.7% | 48.8–80.8% | 30 | -2.83% | 84.9% | 5 | 0 |
| Geometric | SOL | 1h | 1x | 57.8% | 45.6–69.1% | 64 | -0.26% | 22.2% | 3 | 0 |
| Geometric | SOL | 1h | 2x | 57.8% | 45.6–69.1% | 64 | -0.52% | 42.2% | 3 | 0 |
| Geometric | SOL | 1h | 3x | 57.8% | 45.6–69.1% | 64 | -0.77% | 60.4% | 3 | 0 |
| Geometric | SOL | 1h | 5x | 57.1% | 44.9–68.6% | 63 | -1.33% | 93.5% | 3 | 0 |
| Geometric | SOL | 4h | 1x | 61.9% | 40.9–79.2% | 21 | -0.45% | 15.0% | 5 | 0 |
| Geometric | SOL | 4h | 2x | 61.9% | 40.9–79.2% | 21 | -0.91% | 29.5% | 5 | 0 |
| Geometric | SOL | 4h | 3x | 61.9% | 40.9–79.2% | 21 | -1.36% | 43.7% | 5 | 0 |
| Geometric | SOL | 4h | 5x | 61.9% | 40.9–79.2% | 21 | -2.26% | 71.1% | 5 | 0 |
| Geometric | ZEC | 1h | 1x | 75.0% | 57.9–86.7% | 32 | -0.13% | 10.4% | 2 | 0 |
| Geometric | ZEC | 1h | 2x | 75.0% | 57.9–86.7% | 32 | -0.25% | 19.7% | 2 | 0 |
| Geometric | ZEC | 1h | 3x | 75.0% | 57.9–86.7% | 32 | -0.38% | 28.1% | 2 | 0 |
| Geometric | ZEC | 1h | 5x | 75.9% | 57.9–87.8% | 29 | -0.61% | 42.8% | 2 | 0 |
| Geometric | ZEC | 4h | 1x | 36.4% not meaningful | 15.2–64.6% | 11 | -1.49% | 22.6% | 6 | 0 |
| Geometric | ZEC | 4h | 2x | 36.4% not meaningful | 15.2–64.6% | 11 | -2.97% | 42.4% | 6 | 0 |
| Geometric | ZEC | 4h | 3x | 36.4% not meaningful | 15.2–64.6% | 11 | -4.46% | 59.9% | 6 | 0 |
| Geometric | ZEC | 4h | 5x | 40.0% not meaningful | 16.8–68.7% | 10 | -9.13% | 93.6% | 6 | 0 |

## Max safe leverage

Rule, applied after the fact to this holdout and not used to pick settings. A leverage is safe for a mode and coin only when both 1h and 4h have at least 20 deployments, zero liquidations, and path drawdown on the fixed 10,000 margin at or under 35%. A cell that did not trade is not evidence of safety.

- Arithmetic BTC: none. 1h did not trade.
- Arithmetic ETH: none. 1h did not trade.
- Arithmetic SOL: none. 1h has 12 deployments.
- Arithmetic ZEC: 1x. 2x draws down 49.9% on 4h.
- Geometric BTC: none. 1h has 9 deployments.
- Geometric ETH: 1x. 2x draws down 41.7% on 4h.
- Geometric SOL: 1x. 2x on 1h is above the 35% drawdown line once the 1x drawdown of 22% is scaled by the leverage.
- Geometric ZEC: none. 4h has 11 deployments.

## Scaling

Hypothetical. A 10,000 account posts 15% of equity as isolated margin per deployment at the locked leverage rule's returns from the 1x holdout path. This is not a forecast.

Terminal on the recorded path: 7726. Bootstrap median 7515, 5th percentile 7228, ruin rate 0.0% of 2,000 redraws. Ruin means equity at or under 2,000.

OKX public funding history used where the file has prints, from about 10 Aug 2026. Earlier bars, including most of the in-sample window and the first part of the out-of-sample window, are charged zero. Binance futures funding was blocked from this environment.
DefiLlama stablecoins.llama.fi total circulating USD, 14-day change, lagged one day. History covers the in-sample window.

## Indicator changes, holdout, not used to select

Each row is the best walk-forward variant of that gate, then run once at 1x on 4h for BTC, ETH, SOL and ZEC. The lock stayed with the walk-forward winner. These out-of-sample numbers were not used to change it.

The original screener gate (score at least 60 and a neutral reading) is `score60`. Smoothed ADX hysteresis is `hyst`. Variance ratio below 0.90 is `hyst_vr`. Daily ADX agreement is `hyst_daily`. Range age 6 to 48 bars is `hyst_age`. A positive lagged 14-day stablecoin-supply change is `hyst_stable`. Score at least 55 with no hard neutral requirement is `score55`. Hysteresis plus the 2,000,000 USDT per hour floor is `hyst_liq`.

| Mode | Gate | Walk-forward win | Walk-forward n | 4h holdout win | Holdout n | Holdout mean return |
|---|---|---|---|---|---|---|
| Arithmetic | hyst | 72.4% | 3011 | 65.7% | 175 | -0.42% |
| Arithmetic | hyst_age | 72.9% | 2203 | 66.7% | 129 | -0.23% |
| Arithmetic | hyst_daily | 73.2% | 1796 | 65.3% | 75 | -0.17% |
| Arithmetic | hyst_liq | 72.8% | 1766 | 62.9% | 132 | -0.35% |
| Arithmetic | hyst_vr | 71.6% | 2369 | 64.1% | 128 | -0.57% |
| Arithmetic | score55 | 72.5% | 1612 | 73.3% | 105 | -0.28% |
| Arithmetic | score60 | 71.8% | 1385 | 60.4% | 96 | -0.29% |
| Geometric | hyst | 72.5% | 3067 | 68.3% | 186 | -0.42% |
| Geometric | hyst_age | 72.0% | 2228 | 68.9% | 135 | -0.22% |
| Geometric | hyst_daily | 73.1% | 1831 | 67.1% | 79 | -0.21% |
| Geometric | hyst_liq | 72.6% | 1805 | 67.6% | 142 | -0.33% |
| Geometric | hyst_vr | 71.9% | 2423 | 65.2% | 132 | -0.58% |
| Geometric | score55 | 72.5% | 2763 | 70.7% | 198 | -0.22% |
| Geometric | score60 | 72.5% | 1415 | 64.7% | 102 | -0.26% |

`hyst_stable` did not clear the selection-fold return floor, so it has no row here. None of these pooled 4h holdouts reach 75%. The refined lock, which raised the minimum step to 2%, trades less than these coarse rows and is the table above this section.

## Ceiling

634 variants were scored on the selection folds. The best eligible walk-forward win rate was about 75% in sample and about 64% to 73% when the same families were looked at on the 4h holdout. No cell with at least 20 deployments is at or above 75% on both timeframes, and the cells that do print 75% or more are either under 20 deployments or have a 95% interval that includes values below 75%. Arithmetic ZEC 1h is 76.3% (interval 66% to 84%, n=76) and the mean return is still negative. The gate stays closed. The PDF was not built.

## What blocks the gate

Every cell except Arithmetic ZEC on 1h at 1x, 2x, 3x and 5x, and Geometric ZEC on 1h at 1x and 5x. Those exceptions still sit next to a negative mean return, and the other 58 cells fail on sample size or on the win rate. `pdf_gate.py` exits 2.
