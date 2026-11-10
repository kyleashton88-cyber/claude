# Market Check scores before and after review A and C

Provisional only. The hard drop in `select.py` is the reading this unmerged PR uses so it can be reviewed. It is not a production change, and it is not a decision to drop rather than penalise.

`compare_scores.py` produced the tables below. HISTORICAL rows use the saved screen output in the review bundle (24 Oct `selection-2026-10-24`, and the 1 Nov screen under `2026-11-01-am/screen`). LIVE is a fresh universe pull. No candle file was invented.

## Width unit, checked against the TRX example

`win()` sets width to `(p95(close) - p5(close)) / midpoint` of those two percentiles. That is a fraction of price. `scores.csv` rounds it to 3 decimals.

The 24 Oct saved row for TRX is width30 `0.024` and width180 `0.104`, which is 2.4% and 10.4%. The 1 Nov review describes that break as "2.4% over 30 days, ~9–10% over 90/180", and its factor table repeats width30 `0.024` and width180 `0.104`. The bundle has no TRX candle file, so this check is that saved row. Every coin that does have candles recomputes to the same rounded widths, and the same A/C decision, as the csv. So "about 6%" is the constant `0.06` in the units `select.py` already uses, and "under a third of its 180-day width" is `width30 < width180 / 3` in those same fractions.

The 1 Nov saved TRX row is width30 `0.026`, width180 `0.105`. Both cuts still fire.

## What the two rules do in code

**A.** `is_squeeze` is true when `width30 < SQUEEZE_WIDTH30_MIN` or `width30 < width180 / SQUEEZE_WIDTH180_RATIO`, with `SQUEEZE_WIDTH30_MIN = 0.06` and `SQUEEZE_WIDTH180_RATIO = 3`. Both comparisons are strict. A true result skips that coin in `scores.csv` and in the top 5. Candle data is still kept, and the hardcoded BTC/ETH/SOL/XRP block in `levels.json` is unchanged, so a major can disappear from the ranked list and still receive example levels.

**C.** `mid30` is the 30-day `win()` score (`m[0]`, the `mid30` column). `long180` is the `win()` score on the full fetched history (`L[0]`, the `long180` column), which is up to 180 daily bars. They are scores, not prices. The old blend is `0.5*mid30 + 0.4*long180 + 10*liq`. When `drift30 > 0.8` and `adx14 > 40` and `long180 > mid30 + 15`, the `0.4` becomes `0` and the `0.5` and the liquidity term stay as they are. The remaining weights are not renormalized.

That zero-weight reading is the one that matches the 8 Nov check. On the review's own factors (XLM drift30 0.97, ADX14 46.9, long180 53.5, mid30 29.3; DOGE 0.92 / 47.9 / 16.5 / 29.4; SHIB 0.95 / 54.2 / 28.3 / 18.7), shared liquidity gives XLM `0.5*29.3 + 10*liq` and leaves DOGE and SHIB on the old blend. XLM lands below both. Moving the discarded `0.4` onto the mid weight (`0.9*mid30 + 10*liq`) leaves XLM above both, so that reading does not "exclude XLM and keep DOGE and SHIB". The same order shows up on the 1 Nov saved screen with real volumes: XLM 43.9 → 22.6, DOGE stays 29.9, SHIB stays 28.4.

## Open choices for Stewart, before any merge

1. **Drop vs penalise.** The review says "drop or heavily penalise" and does not choose. This PR hard-drops. The penalty variant below is comparison-only and is not what `select.py` runs.
2. **Exactly 6%, and exactly one third.** The review says "about 6%" and "under a third". The constants are exactly `0.06` and `/ 3`.

## Penalty variant used for the comparison

Heavy penalty here means: multiply the composite `0.5*mid30 + 0.4*long180 + 10*liq` by **0.5** when the squeeze rule fires, keep the row, and leave every other published score unchanged. C is off for this variant. A second check, same formula, used 0.75 and 0.8 on the two saved screens only.

On all three runs below, 0.5× produced the same top 5 as deleting the squeezed rows. It still left the coin on the board (TRX fell to the low 20s). 0.75× put 24 Oct WLD back into the top 5 (KAS, ICP, AVAX, WLD, XLM). 0.8× did that as well, and put 1 Nov ASTER back into the top 5 (BNB, POL, ASTER, XLM, ONDO). So 0.5 is heavy enough, on these samples, to match a drop's top 5; a milder cut is not.

## Picks, short version

`select.py` publishes `head(5)` as its picks. That is a different list from the edition's DOGE/XLM/SHIB rotation.

| Run | Top 5 before | Top 5 after A hard-drop + C |
| --- | --- | --- |
| HISTORICAL 24 Oct | WLD, ASTER, KAS, PEPE, DOT | KAS, ICP, AVAX, XLM, HBAR |
| HISTORICAL 1 Nov | ASTER, ARB, BNB, POL, BTC | BNB, POL, ONDO, PEPE, WLD |
| LIVE 8 Nov 2026, fetch 06:36:47–06:36:53 UTC | ASTER, ENA, BTC, ARB, BCH | PEPE, XRP, LTC, AVAX, DOGE |

A alone (no C) on 1 Nov would have been BNB, POL, XLM, ONDO, PEPE. C is what takes XLM back out. On the live pull, A alone would have been PEPE, XRP, XLM, ONDO, LTC, and C again takes XLM out (37.4 → 17.5), below DOGE (30.3) and SHIB (29.8).

24 Oct XLM does not trip C: ADX14 is 38.4, which is not above 40. The review locates that failure on the following week's factors.

Coins whose published score is unchanged are every row with flag `—`. Their new score is the saved score, not a recompute.

Candle files agree with the rounded csv on every A/C yes/no we could recompute. Two 1 Nov guard hits sit on the rounded `+15` gap and have no candle file: LTC (long180 33.8 vs mid30 18.7, gap 0.1 on the rounded scores) and HBAR (29.5 vs 14.1, gap 0.4). Treat those two as unconfirmed. XRP's guard hit is confirmed from candles on both saved screens. 24 Oct ETH also meets C on the raw candles; A removes it first, so the ranked table shows the drop.

1 Nov ASTER's raw width30 is 0.0604. The strict 6% floor keeps it. The one-third ratio drops it (`0.0604 < 0.2114/3`).

LIVE TRX width30 displays as 0.059 (about 5.9%) and width180 as 0.111. Only the 6% floor fires; 5.9% is not under a third of 11.1%. A 5% floor would keep this later TRX. The forming 8 Nov UTC daily is included, because that is what `select.py` fetches.

## Recommendation for A (a recommendation, not a decision)

Use an absolute floor near 6% as the squeeze rule that matches the cited TRX case, and hold the one-third ratio out of any hard drop.

On the two saved screens, width30 under 5% or under 6% drops TRX and leaves XLM, DOGE, and SHIB in place. The 6% floor also drops 24 Oct BTC (width30 0.052). The 5% floor leaves that BTC row. The 7% floor also drops ASTER (24 Oct 0.065, 1 Nov raw 0.0604). The live TRX row, about 5.9%, shows why "about 6%" still needs a human pick: 5% keeps it, 6% and 7% drop it.

The one-third ratio does catch historical TRX, and it also catches a different population. On 24 Oct it removes 15 of 30 coins, including four of the five screen picks (WLD 19.7% over 30 days, ASTER, PEPE, DOT). On 1 Nov it removes 9 of 30, including ASTER and BTC at 9.7% over 30 days. Those 30-day ranges are not the 2.4% coil the review described. `width180/2` is wider still (23–24 coins, and it takes DOGE). `width180/4` is the nearby ratio that still drops historical TRX and, on 24 Oct, only WLD, BTC, NEAR, and TRX, leaving ASTER, KAS, PEPE, and DOT in the top 5. That is a sensitivity result, not a proposed constant.

Between drop and penalty: a 0.5× composite multiplier matched the hard drop's top 5 on these three runs and still showed the squeezed names further down the table. 0.75× no longer matched. Until Stewart chooses, the hard drop should stay in this unmerged PR only.

Change B (re-weight 180-day crossings, cap the ADX bonus) is not in this diff.

## Deployment

This repository did not contain the screen. The 24 Oct and 1 Nov copies in the bundle are the same file (md5 `5913d036858608ef03bd8877be274e6d`). Nothing here publishes to the machine that writes editions. Merging is deliberately not done. After Stewart confirms the reading, that machine's copy of `select.py` has to be replaced with this one; this PR does not know that path and does not update it.

## HISTORICAL — 24 Oct 2026 saved screen

Baseline ranks and scores are the saved `scores.csv` (already sorted). A+C uses those published factor columns. A squeezed coin is removed. A guard hit recomputes `0.5*mid30 + 10*liq` from the published (rounded) factors and rounds to 0.1. Every other coin keeps its published score exactly.

Top 5 before: WLD, ASTER, KAS, PEPE, DOT

Top 5 after A hard-drop + C: KAS, ICP, AVAX, XLM, HBAR

| old_rank | coin | old_score | new_rank | new_score | flag | width30 | width180 | drift30 | adx14 | mid30 | long180 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | WLD | 62.6 | — | — | A drop (width30<width180/3) | 0.197 | 0.823 | 0.24 | 17.9 | 79.7 | 35.4 |
| 2 | ASTER | 54.0 | — | — | A drop (width30<width180/3) | 0.065 | 0.211 | 0.98 | 27.6 | 44.8 | 59.4 |
| 3 | KAS | 52.5 | 1 | 52.5 | — | 0.268 | 0.487 | 0.57 | 25.9 | 56.8 | 42.8 |
| 4 | PEPE | 51.6 | — | — | A drop (width30<width180/3) | 0.160 | 0.525 | 0.17 | 27.3 | 56.9 | 36.1 |
| 5 | DOT | 50.6 | — | — | A drop (width30<width180/3) | 0.144 | 0.522 | 0.89 | 20.2 | 56.5 | 35.5 |
| 6 | BTC | 50.0 | — | — | A drop (both cuts) | 0.052 | 0.321 | 0.78 | 23.5 | 42.2 | 47.1 |
| 7 | ICP | 49.1 | 2 | 49.1 | — | 0.238 | 0.456 | 0.70 | 21.9 | 47.2 | 44.6 |
| 8 | AVAX | 49.0 | 3 | 49.0 | — | 0.218 | 0.539 | 0.78 | 24.3 | 51.7 | 37.0 |
| 9 | NEAR | 48.7 | — | — | A drop (width30<width180/3) | 0.155 | 1.092 | 0.56 | 13.2 | 72.0 | 9.8 |
| 10 | AAVE | 46.9 | — | — | A drop (width30<width180/3) | 0.216 | 0.841 | 0.37 | 26.8 | 55.6 | 27.1 |
| 11 | XLM | 45.5 | 4 | 45.5 | — | 0.255 | 0.391 | 0.99 | 38.4 | 30.0 | 56.2 |
| 12 | TRX | 44.6 | — | — | A drop (both cuts) | 0.024 | 0.104 | 1.00 | 15.9 | 30.5 | 52.2 |
| 13 | HBAR | 44.2 | 5 | 44.2 | — | 0.282 | 0.394 | 0.73 | 23.4 | 44.2 | 35.6 |
| 14 | ARB | 40.9 | — | — | A drop (width30<width180/3) | 0.263 | 0.938 | 1.11 | 40.9 | 37.6 | 34.9 |
| 15 | ENA | 39.8 | 6 | 39.8 | — | 0.350 | 1.020 | 0.97 | 17.7 | 37.6 | 30.6 |
| 16 | SUI | 39.6 | 7 | 39.6 | — | 0.225 | 0.539 | 1.01 | 32.7 | 32.1 | 37.7 |
| 17 | SHIB | 39.4 | 8 | 39.4 | — | 0.177 | 0.393 | 1.09 | 45.9 | 34.0 | 36.4 |
| 18 | ADA | 38.6 | 9 | 38.6 | — | 0.220 | 0.520 | 0.95 | 32.5 | 33.0 | 34.2 |
| 19 | XRP | 37.4 | 13 | 21.0 | C weight 0 | 0.163 | 0.379 | 1.25 | 40.4 | 23.8 | 41.1 |
| 20 | BNB | 35.5 | — | — | A drop (width30<width180/3) | 0.085 | 0.310 | 0.68 | 33.7 | 21.6 | 39.5 |
| 21 | ONDO | 34.7 | 10 | 34.7 | — | 0.249 | 0.464 | 1.17 | 41.3 | 29.0 | 30.7 |
| 22 | LINK | 34.0 | — | — | A drop (width30<width180/3) | 0.198 | 0.610 | 0.89 | 39.4 | 29.0 | 27.9 |
| 23 | ETC | 31.7 | 15 | 16.0 | C weight 0 | 0.202 | 0.379 | 1.07 | 70.0 | 16.8 | 39.3 |
| 24 | LTC | 30.8 | 14 | 17.2 | C weight 0 | 0.216 | 0.475 | 1.16 | 52.9 | 17.6 | 34.2 |
| 25 | ETH | 29.1 | — | — | A drop (width30<width180/3) | 0.126 | 0.495 | 1.00 | 44.5 | 12.2 | 32.8 |
| 26 | DOGE | 28.8 | 11 | 28.8 | — | 0.206 | 0.445 | 1.18 | 47.9 | 17.0 | 29.3 |
| 27 | SOL | 27.8 | — | — | A drop (width30<width180/3) | 0.166 | 0.543 | 1.09 | 39.7 | 14.8 | 27.6 |
| 28 | QNT | 27.4 | 12 | 27.4 | — | 0.515 | 1.231 | 0.70 | 26.5 | 25.1 | 17.7 |
| 29 | BCH | 25.7 | — | — | A drop (width30<width180/3) | 0.214 | 0.771 | 1.03 | 48.7 | 17.5 | 22.0 |
| 30 | UNI | 23.3 | — | — | A drop (width30<width180/3) | 0.323 | 1.106 | 1.03 | 61.0 | 15.3 | 18.2 |

### A only: hard drop vs 0.5× score penalty

The penalty is not in `select.py`. It multiplies the rebuilt composite (`0.5*mid30 + 0.4*long180 + 10*liq`) by 0.5 when the provisional squeeze rule fires, and leaves every other published score unchanged. C is off.

- A-only hard drop top 5: KAS, ICP, AVAX, XLM, HBAR
- A-only 0.5× penalty top 5 (multiplier 0.5, C off): KAS, ICP, AVAX, XLM, HBAR
- A hard-drop + C top 5: KAS, ICP, AVAX, XLM, HBAR
- TRX: old rank 12 score 44.6; A-only drop rank —; A-only 0.5× rank 23 score 22.3; A+C rank — score —
- XLM: old rank 11 score 45.5; A-only drop rank 4; A-only 0.5× rank 4 score 45.5; A+C rank 4 score 45.5
- DOGE: old rank 26 score 28.8; A-only drop rank 14; A-only 0.5× rank 15 score 28.8; A+C rank 11 score 28.8
- SHIB: old rank 17 score 39.4; A-only drop rank 8; A-only 0.5× rank 8 score 39.4; A+C rank 8 score 39.4
- BTC: old rank 6 score 50.0; A-only drop rank —; A-only 0.5× rank 20 score 25.0; A+C rank — score —
- ETH: old rank 25 score 29.1; A-only drop rank —; A-only 0.5× rank 27 score 14.6; A+C rank — score —
- SOL: old rank 27 score 27.8; A-only drop rank —; A-only 0.5× rank 28 score 13.9; A+C rank — score —
- XRP: old rank 19 score 37.4; A-only drop rank 10; A-only 0.5× rank 10 score 37.4; A+C rank 13 score 21.0
- WLD: old rank 1 score 62.6; A-only drop rank —; A-only 0.5× rank 13 score 31.3; A+C rank — score —
- ASTER: old rank 2 score 54.0; A-only drop rank —; A-only 0.5× rank 17 score 27.0; A+C rank — score —
- PEPE: old rank 4 score 51.6; A-only drop rank —; A-only 0.5× rank 18 score 25.8; A+C rank — score —
- DOT: old rank 5 score 50.6; A-only drop rank —; A-only 0.5× rank 19 score 25.3; A+C rank — score —
- KAS: old rank 3 score 52.5; A-only drop rank 1; A-only 0.5× rank 1 score 52.5; A+C rank 1 score 52.5
- LTC: old rank 24 score 30.8; A-only drop rank 13; A-only 0.5× rank 14 score 30.8; A+C rank 14 score 17.2
- HBAR: old rank 13 score 44.2; A-only drop rank 5; A-only 0.5× rank 5 score 44.2; A+C rank 5 score 44.2

### Squeeze-rule sensitivity

Counts use the rounded factor columns. `n` is how many of the 30 scored coins the rule removes. `top5` is who would lead if those coins were deleted and everyone else kept their published score.

| rule | n | top5 | TRX | XLM | DOGE | SHIB | BTC | ASTER | dropped |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| absolute only 5% | 1 | WLD, ASTER, KAS, PEPE, DOT | drop | keep | keep | keep | keep | keep | TRX |
| absolute only 6% | 2 | WLD, ASTER, KAS, PEPE, DOT | drop | keep | keep | keep | drop | keep | BTC, TRX |
| absolute only 7% | 3 | WLD, KAS, PEPE, DOT, ICP | drop | keep | keep | keep | drop | drop | ASTER, BTC, TRX |
| ratio only width180/2 | 24 | KAS, ICP, XLM, HBAR, ONDO | drop | keep | drop | drop | drop | drop | WLD, ASTER, PEPE, DOT, BTC, AVAX, NEAR, AAVE, TRX, ARB, ENA, SUI, SHIB, ADA, XRP, BNB, LINK, LTC, ETH, DOGE, SOL, QNT, BCH, UNI |
| ratio only width180/3 | 15 | KAS, ICP, AVAX, XLM, HBAR | drop | keep | keep | keep | drop | drop | WLD, ASTER, PEPE, DOT, BTC, NEAR, AAVE, TRX, ARB, BNB, LINK, ETH, SOL, BCH, UNI |
| ratio only width180/4 | 4 | ASTER, KAS, PEPE, DOT, ICP | drop | keep | keep | keep | drop | keep | WLD, BTC, NEAR, TRX |
| OR 5% or width180/2 | 24 | KAS, ICP, XLM, HBAR, ONDO | drop | keep | drop | drop | drop | drop | WLD, ASTER, PEPE, DOT, BTC, AVAX, NEAR, AAVE, TRX, ARB, ENA, SUI, SHIB, ADA, XRP, BNB, LINK, LTC, ETH, DOGE, SOL, QNT, BCH, UNI |
| OR 5% or width180/3 | 15 | KAS, ICP, AVAX, XLM, HBAR | drop | keep | keep | keep | drop | drop | WLD, ASTER, PEPE, DOT, BTC, NEAR, AAVE, TRX, ARB, BNB, LINK, ETH, SOL, BCH, UNI |
| OR 5% or width180/4 | 4 | ASTER, KAS, PEPE, DOT, ICP | drop | keep | keep | keep | drop | keep | WLD, BTC, NEAR, TRX |
| OR 6% or width180/2 | 24 | KAS, ICP, XLM, HBAR, ONDO | drop | keep | drop | drop | drop | drop | WLD, ASTER, PEPE, DOT, BTC, AVAX, NEAR, AAVE, TRX, ARB, ENA, SUI, SHIB, ADA, XRP, BNB, LINK, LTC, ETH, DOGE, SOL, QNT, BCH, UNI |
| OR 6% or width180/3 | 15 | KAS, ICP, AVAX, XLM, HBAR | drop | keep | keep | keep | drop | drop | WLD, ASTER, PEPE, DOT, BTC, NEAR, AAVE, TRX, ARB, BNB, LINK, ETH, SOL, BCH, UNI |
| OR 6% or width180/4 | 4 | ASTER, KAS, PEPE, DOT, ICP | drop | keep | keep | keep | drop | keep | WLD, BTC, NEAR, TRX |
| OR 7% or width180/2 | 24 | KAS, ICP, XLM, HBAR, ONDO | drop | keep | drop | drop | drop | drop | WLD, ASTER, PEPE, DOT, BTC, AVAX, NEAR, AAVE, TRX, ARB, ENA, SUI, SHIB, ADA, XRP, BNB, LINK, LTC, ETH, DOGE, SOL, QNT, BCH, UNI |
| OR 7% or width180/3 | 15 | KAS, ICP, AVAX, XLM, HBAR | drop | keep | keep | keep | drop | drop | WLD, ASTER, PEPE, DOT, BTC, NEAR, AAVE, TRX, ARB, BNB, LINK, ETH, SOL, BCH, UNI |
| OR 7% or width180/4 | 5 | KAS, PEPE, DOT, ICP, AVAX | drop | keep | keep | keep | drop | drop | WLD, ASTER, BTC, NEAR, TRX |

### Candle recompute vs rounded factors

Raw `win()` on the saved candle files, checked against the rounded columns. No A/C decision changed.

| coin | same | raw_w30 | csv_w30 | raw_w180 | csv_w180 | raw_A | csv_A | raw_C | csv_C |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ASTER | yes | 0.0653 | 0.065 | 0.2114 | 0.211 | drop | drop | 0.4 | 0.4 |
| BTC | yes | 0.0524 | 0.052 | 0.3210 | 0.321 | drop | drop | 0.4 | 0.4 |
| DOT | yes | 0.1439 | 0.144 | 0.5221 | 0.522 | drop | drop | 0.4 | 0.4 |
| ETH | yes | 0.1256 | 0.126 | 0.4953 | 0.495 | drop | drop | zero | zero |
| KAS | yes | 0.2677 | 0.268 | 0.4866 | 0.487 | keep | keep | 0.4 | 0.4 |
| PEPE | yes | 0.1597 | 0.160 | 0.5246 | 0.525 | drop | drop | 0.4 | 0.4 |
| SOL | yes | 0.1661 | 0.166 | 0.5434 | 0.543 | drop | drop | 0.4 | 0.4 |
| WLD | yes | 0.1972 | 0.197 | 0.8226 | 0.823 | drop | drop | 0.4 | 0.4 |
| XLM | yes | 0.2551 | 0.255 | 0.3910 | 0.391 | keep | keep | 0.4 | 0.4 |
| XRP | yes | 0.1630 | 0.163 | 0.3792 | 0.379 | keep | keep | zero | zero |

## HISTORICAL — 1 Nov 2026 saved screen

Baseline ranks and scores are the saved `scores.csv` (already sorted). A+C uses those published factor columns. A squeezed coin is removed. A guard hit recomputes `0.5*mid30 + 10*liq` from the published (rounded) factors and rounds to 0.1. Every other coin keeps its published score exactly.

Top 5 before: ASTER, ARB, BNB, POL, BTC

Top 5 after A hard-drop + C: BNB, POL, ONDO, PEPE, WLD

| old_rank | coin | old_score | new_rank | new_score | flag | width30 | width180 | drift30 | adx14 | mid30 | long180 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | ASTER | 56.2 | — | — | A drop (width30<width180/3) | 0.060 | 0.211 | 0.54 | 38.3 | 51.2 | 56.6 |
| 2 | ARB | 50.7 | — | — | A drop (width30<width180/3) | 0.215 | 0.938 | 0.82 | 31.2 | 58.0 | 34.4 |
| 3 | BNB | 48.4 | 1 | 48.4 | — | 0.112 | 0.310 | 0.79 | 39.7 | 44.9 | 42.7 |
| 4 | POL | 46.2 | 2 | 46.2 | — | 0.203 | 0.429 | 0.74 | 59.8 | 42.1 | 43.8 |
| 5 | BTC | 44.8 | — | — | A drop (width30<width180/3) | 0.097 | 0.321 | 0.88 | 38.8 | 32.9 | 45.9 |
| 6 | NEAR | 44.6 | — | — | A drop (width30<width180/3) | 0.198 | 1.053 | 0.26 | 21.2 | 60.7 | 13.9 |
| 7 | ENA | 44.2 | — | — | A drop (width30<width180/3) | 0.245 | 1.020 | 0.83 | 21.6 | 44.6 | 33.7 |
| 8 | XLM | 43.9 | 18 | 22.6 | C weight 0 | 0.245 | 0.391 | 0.97 | 46.9 | 29.5 | 53.4 |
| 9 | ONDO | 42.7 | 3 | 42.7 | — | 0.202 | 0.448 | 0.90 | 43.3 | 38.1 | 39.0 |
| 10 | PEPE | 42.6 | 4 | 42.6 | — | 0.247 | 0.558 | 0.72 | 37.2 | 47.0 | 26.0 |
| 11 | WLD | 42.3 | 5 | 42.3 | — | 0.372 | 0.774 | 0.86 | 31.5 | 39.7 | 36.2 |
| 12 | ETC | 41.2 | 6 | 41.2 | — | 0.219 | 0.379 | 0.98 | 63.2 | 46.4 | 26.6 |
| 13 | LINK | 41.2 | 7 | 41.2 | — | 0.206 | 0.610 | 0.75 | 48.0 | 42.0 | 29.2 |
| 14 | BCH | 40.3 | — | — | A drop (width30<width180/3) | 0.164 | 0.745 | 0.57 | 38.9 | 44.7 | 24.7 |
| 15 | ICP | 40.1 | 8 | 40.1 | — | 0.305 | 0.456 | 0.85 | 38.4 | 30.5 | 43.6 |
| 16 | ETH | 39.8 | 9 | 39.8 | — | 0.182 | 0.495 | 0.92 | 54.1 | 36.3 | 30.0 |
| 17 | DOT | 39.2 | 10 | 39.2 | — | 0.260 | 0.522 | 0.72 | 29.6 | 41.8 | 26.2 |
| 18 | SUI | 38.0 | 11 | 38.0 | — | 0.281 | 0.539 | 0.83 | 44.7 | 31.3 | 35.2 |
| 19 | TRX | 37.8 | — | — | A drop (both cuts) | 0.026 | 0.105 | 3.50 | 25.9 | 33.7 | 30.2 |
| 20 | XRP | 33.1 | 20 | 17.4 | C weight 0 | 0.180 | 0.379 | 0.94 | 44.5 | 17.1 | 39.2 |
| 21 | AVAX | 32.5 | 12 | 32.5 | — | 0.260 | 0.539 | 0.86 | 41.4 | 22.5 | 32.3 |
| 22 | AAVE | 31.6 | 13 | 31.6 | — | 0.318 | 0.841 | 0.93 | 53.4 | 26.8 | 24.5 |
| 23 | LTC | 31.1 | 19 | 17.6 | C weight 0 | 0.225 | 0.475 | 0.98 | 63.9 | 18.7 | 33.8 |
| 24 | SOL | 30.9 | 14 | 30.9 | — | 0.228 | 0.543 | 0.93 | 56.0 | 20.2 | 28.8 |
| 25 | DOGE | 29.9 | 15 | 29.9 | — | 0.220 | 0.443 | 0.91 | 47.9 | 29.4 | 16.7 |
| 26 | ADA | 28.9 | 16 | 28.9 | — | 0.305 | 0.520 | 0.74 | 40.2 | 22.9 | 23.3 |
| 27 | SHIB | 28.4 | 17 | 28.4 | — | 0.209 | 0.393 | 0.94 | 54.2 | 18.7 | 28.5 |
| 28 | QNT | 28.0 | — | — | A drop (width30<width180/3) | 0.353 | 1.231 | 0.61 | 36.6 | 25.5 | 18.7 |
| 29 | UNI | 26.6 | — | — | A drop (width30<width180/3) | 0.273 | 1.106 | 0.84 | 59.5 | 22.4 | 16.9 |
| 30 | HBAR | 26.5 | 21 | 14.7 | C weight 0 | 0.342 | 0.394 | 1.01 | 59.5 | 14.1 | 29.5 |

### A only: hard drop vs 0.5× score penalty

The penalty is not in `select.py`. It multiplies the rebuilt composite (`0.5*mid30 + 0.4*long180 + 10*liq`) by 0.5 when the provisional squeeze rule fires, and leaves every other published score unchanged. C is off.

- A-only hard drop top 5: BNB, POL, XLM, ONDO, PEPE
- A-only 0.5× penalty top 5 (multiplier 0.5, C off): BNB, POL, XLM, ONDO, PEPE
- A hard-drop + C top 5: BNB, POL, ONDO, PEPE, WLD
- TRX: old rank 19 score 37.8; A-only drop rank —; A-only 0.5× rank 28 score 18.9; A+C rank — score —
- XLM: old rank 8 score 43.9; A-only drop rank 3; A-only 0.5× rank 3 score 43.9; A+C rank 18 score 22.6
- DOGE: old rank 25 score 29.9; A-only drop rank 18; A-only 0.5× rank 18 score 29.9; A+C rank 15 score 29.9
- SHIB: old rank 27 score 28.4; A-only drop rank 20; A-only 0.5× rank 20 score 28.4; A+C rank 17 score 28.4
- BTC: old rank 5 score 44.8; A-only drop rank —; A-only 0.5× rank 24 score 22.4; A+C rank — score —
- ETH: old rank 16 score 39.8; A-only drop rank 10; A-only 0.5× rank 10 score 39.8; A+C rank 9 score 39.8
- SOL: old rank 24 score 30.9; A-only drop rank 17; A-only 0.5× rank 17 score 30.9; A+C rank 14 score 30.9
- XRP: old rank 20 score 33.1; A-only drop rank 13; A-only 0.5× rank 13 score 33.1; A+C rank 20 score 17.4
- WLD: old rank 11 score 42.3; A-only drop rank 6; A-only 0.5× rank 6 score 42.3; A+C rank 5 score 42.3
- ASTER: old rank 1 score 56.2; A-only drop rank —; A-only 0.5× rank 21 score 28.1; A+C rank — score —
- PEPE: old rank 10 score 42.6; A-only drop rank 5; A-only 0.5× rank 5 score 42.6; A+C rank 4 score 42.6
- DOT: old rank 17 score 39.2; A-only drop rank 11; A-only 0.5× rank 11 score 39.2; A+C rank 10 score 39.2
- LTC: old rank 23 score 31.1; A-only drop rank 16; A-only 0.5× rank 16 score 31.1; A+C rank 19 score 17.6
- HBAR: old rank 30 score 26.5; A-only drop rank 21; A-only 0.5× rank 22 score 26.5; A+C rank 21 score 14.7

### Squeeze-rule sensitivity

Counts use the rounded factor columns. `n` is how many of the 30 scored coins the rule removes. `top5` is who would lead if those coins were deleted and everyone else kept their published score.

| rule | n | top5 | TRX | XLM | DOGE | SHIB | BTC | ASTER | dropped |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| absolute only 5% | 1 | ASTER, ARB, BNB, POL, BTC | drop | keep | keep | keep | keep | keep | TRX |
| absolute only 6% | 1 | ASTER, ARB, BNB, POL, BTC | drop | keep | keep | keep | keep | keep | TRX |
| absolute only 7% | 2 | ARB, BNB, POL, BTC, NEAR | drop | keep | keep | keep | keep | drop | ASTER, TRX |
| ratio only width180/2 | 23 | XLM, ETC, ICP, SUI, ADA | drop | keep | drop | keep | drop | drop | ASTER, ARB, BNB, POL, BTC, NEAR, ENA, ONDO, PEPE, WLD, LINK, BCH, ETH, DOT, TRX, XRP, AVAX, AAVE, LTC, SOL, DOGE, QNT, UNI |
| ratio only width180/3 | 9 | BNB, POL, XLM, ONDO, PEPE | drop | keep | keep | keep | drop | drop | ASTER, ARB, BTC, NEAR, ENA, BCH, TRX, QNT, UNI |
| ratio only width180/4 | 6 | ASTER, BNB, POL, BTC, XLM | drop | keep | keep | keep | keep | keep | ARB, NEAR, ENA, BCH, TRX, UNI |
| OR 5% or width180/2 | 23 | XLM, ETC, ICP, SUI, ADA | drop | keep | drop | keep | drop | drop | ASTER, ARB, BNB, POL, BTC, NEAR, ENA, ONDO, PEPE, WLD, LINK, BCH, ETH, DOT, TRX, XRP, AVAX, AAVE, LTC, SOL, DOGE, QNT, UNI |
| OR 5% or width180/3 | 9 | BNB, POL, XLM, ONDO, PEPE | drop | keep | keep | keep | drop | drop | ASTER, ARB, BTC, NEAR, ENA, BCH, TRX, QNT, UNI |
| OR 5% or width180/4 | 6 | ASTER, BNB, POL, BTC, XLM | drop | keep | keep | keep | keep | keep | ARB, NEAR, ENA, BCH, TRX, UNI |
| OR 6% or width180/2 | 23 | XLM, ETC, ICP, SUI, ADA | drop | keep | drop | keep | drop | drop | ASTER, ARB, BNB, POL, BTC, NEAR, ENA, ONDO, PEPE, WLD, LINK, BCH, ETH, DOT, TRX, XRP, AVAX, AAVE, LTC, SOL, DOGE, QNT, UNI |
| OR 6% or width180/3 | 9 | BNB, POL, XLM, ONDO, PEPE | drop | keep | keep | keep | drop | drop | ASTER, ARB, BTC, NEAR, ENA, BCH, TRX, QNT, UNI |
| OR 6% or width180/4 | 6 | ASTER, BNB, POL, BTC, XLM | drop | keep | keep | keep | keep | keep | ARB, NEAR, ENA, BCH, TRX, UNI |
| OR 7% or width180/2 | 23 | XLM, ETC, ICP, SUI, ADA | drop | keep | drop | keep | drop | drop | ASTER, ARB, BNB, POL, BTC, NEAR, ENA, ONDO, PEPE, WLD, LINK, BCH, ETH, DOT, TRX, XRP, AVAX, AAVE, LTC, SOL, DOGE, QNT, UNI |
| OR 7% or width180/3 | 9 | BNB, POL, XLM, ONDO, PEPE | drop | keep | keep | keep | drop | drop | ASTER, ARB, BTC, NEAR, ENA, BCH, TRX, QNT, UNI |
| OR 7% or width180/4 | 7 | BNB, POL, BTC, XLM, ONDO | drop | keep | keep | keep | keep | drop | ASTER, ARB, NEAR, ENA, BCH, TRX, UNI |

### Candle recompute vs rounded factors

Raw `win()` on the saved candle files, checked against the rounded columns. No A/C decision changed.

| coin | same | raw_w30 | csv_w30 | raw_w180 | csv_w180 | raw_A | csv_A | raw_C | csv_C |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ARB | yes | 0.2152 | 0.215 | 0.9384 | 0.938 | drop | drop | 0.4 | 0.4 |
| ASTER | yes | 0.0604 | 0.060 | 0.2114 | 0.211 | drop | drop | 0.4 | 0.4 |
| BNB | yes | 0.1118 | 0.112 | 0.3098 | 0.310 | keep | keep | 0.4 | 0.4 |
| BTC | yes | 0.0971 | 0.097 | 0.3210 | 0.321 | drop | drop | 0.4 | 0.4 |
| ETH | yes | 0.1818 | 0.182 | 0.4953 | 0.495 | keep | keep | 0.4 | 0.4 |
| POL | yes | 0.2032 | 0.203 | 0.4295 | 0.429 | keep | keep | 0.4 | 0.4 |
| SOL | yes | 0.2278 | 0.228 | 0.5434 | 0.543 | keep | keep | 0.4 | 0.4 |
| XRP | yes | 0.1803 | 0.180 | 0.3792 | 0.379 | keep | keep | zero | zero |

## LIVE

Fetched 2026-11-08 06:36:47 UTC through 2026-11-08 06:36:53 UTC.
Same universe rules as `select.py` (CoinGecko top, non-stable, Bybit USDT spot and Pionex USDT spot, cap 30). Daily candles are Pionex public 1D klines, limit 180. Factors below are raw `win()` values, rounded only for display; the drop and the guard use the raw values. Scores are rounded to 0.1 the way `select.py` writes `scores.csv`.

Top 5 before: ASTER, ENA, BTC, ARB, BCH

Top 5 after A hard-drop + C: PEPE, XRP, LTC, AVAX, DOGE

| old_rank | coin | old_score | new_rank | new_score | flag | width30 | width180 | drift30 | adx14 | mid30 | long180 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | ASTER | 49.3 | — | — | A drop (both cuts) | 0.049 | 0.211 | 0.97 | 49.3 | 38.7 | 55.7 |
| 2 | ENA | 43.7 | — | — | A drop (width30<width180/3) | 0.308 | 1.020 | 1.15 | 30.8 | 40.6 | 38.0 |
| 3 | BTC | 43.3 | — | — | A drop (width30<width180/3) | 0.096 | 0.321 | 0.93 | 27.6 | 29.2 | 46.8 |
| 4 | ARB | 43.0 | — | — | A drop (width30<width180/3) | 0.230 | 0.938 | 0.53 | 21.2 | 42.1 | 34.9 |
| 5 | BCH | 42.3 | — | — | A drop (width30<width180/3) | 0.130 | 0.581 | 0.93 | 29.0 | 49.0 | 24.2 |
| 6 | UNI | 41.4 | — | — | A drop (width30<width180/3) | 0.106 | 1.106 | 0.68 | 39.0 | 49.9 | 20.1 |
| 7 | TRX | 40.7 | — | — | A drop (width30<0.06) | 0.059 | 0.111 | 0.53 | 19.2 | 33.0 | 39.3 |
| 8 | BNB | 39.7 | — | — | A drop (width30<width180/3) | 0.080 | 0.310 | 0.90 | 33.7 | 25.2 | 46.0 |
| 9 | POL | 39.5 | — | — | A drop (width30<width180/3) | 0.141 | 0.429 | 0.87 | 39.8 | 25.8 | 47.6 |
| 10 | ETH | 38.7 | — | — | A drop (width30<width180/3) | 0.112 | 0.495 | 1.03 | 28.4 | 27.9 | 37.8 |
| 11 | PEPE | 38.6 | 1 | 38.6 | — | 0.230 | 0.616 | 0.82 | 46.9 | 41.6 | 23.8 |
| 12 | XRP | 38.0 | 2 | 38.0 | — | 0.168 | 0.379 | 1.11 | 30.8 | 29.8 | 35.2 |
| 13 | XLM | 37.4 | 15 | 17.5 | C weight 0 | 0.242 | 0.391 | 1.11 | 48.2 | 19.2 | 49.8 |
| 14 | ONDO | 35.2 | 16 | 16.7 | C weight 0 | 0.280 | 0.448 | 1.15 | 42.0 | 17.9 | 46.3 |
| 15 | LINK | 34.0 | — | — | A drop (width30<width180/3) | 0.190 | 0.610 | 1.01 | 30.7 | 21.9 | 37.1 |
| 16 | LTC | 33.5 | 3 | 33.5 | — | 0.187 | 0.475 | 1.10 | 48.7 | 25.2 | 32.0 |
| 17 | QNT | 32.2 | — | — | A drop (width30<width180/3) | 0.245 | 1.231 | 0.87 | 25.8 | 31.5 | 22.1 |
| 18 | AVAX | 31.9 | 4 | 31.9 | — | 0.227 | 0.539 | 1.05 | 35.1 | 21.3 | 33.1 |
| 19 | DOGE | 30.3 | 5 | 30.3 | — | 0.176 | 0.386 | 1.07 | 44.3 | 24.5 | 24.2 |
| 20 | SHIB | 29.8 | 6 | 29.8 | — | 0.168 | 0.335 | 1.17 | 51.6 | 24.1 | 25.7 |
| 21 | ICP | 29.8 | 7 | 29.8 | — | 0.257 | 0.428 | 1.01 | 44.7 | 19.3 | 32.2 |
| 22 | SOL | 29.4 | 8 | 29.4 | — | 0.193 | 0.543 | 1.10 | 47.0 | 16.2 | 30.9 |
| 23 | AAVE | 28.7 | — | — | A drop (width30<width180/3) | 0.261 | 0.841 | 1.00 | 43.8 | 19.1 | 27.5 |
| 24 | ETC | 28.6 | 9 | 28.6 | — | 0.183 | 0.346 | 1.11 | 57.2 | 25.0 | 22.1 |
| 25 | NEAR | 27.2 | 10 | 27.2 | — | 0.350 | 1.039 | 1.01 | 29.0 | 20.5 | 21.4 |
| 26 | WLD | 26.0 | 17 | 11.0 | C weight 0 | 0.525 | 0.739 | 0.94 | 47.9 | 6.1 | 37.3 |
| 27 | SUI | 25.9 | 11 | 25.9 | — | 0.237 | 0.526 | 1.14 | 50.2 | 18.9 | 20.8 |
| 28 | ADA | 24.4 | 12 | 24.4 | — | 0.292 | 0.485 | 1.12 | 63.9 | 17.2 | 19.5 |
| 29 | HBAR | 24.3 | 13 | 24.3 | — | 0.288 | 0.394 | 1.14 | 54.0 | 17.4 | 20.5 |
| 30 | DOT | 23.8 | 14 | 23.8 | — | 0.301 | 0.484 | 1.12 | 42.8 | 16.6 | 19.4 |

### A only on this live pull: hard drop vs 0.5× penalty

- A-only hard drop top 5: PEPE, XRP, XLM, ONDO, LTC
- A-only 0.5× penalty top 5 (multiplier 0.5, C off): PEPE, XRP, XLM, ONDO, LTC
- A hard-drop + C top 5: PEPE, XRP, LTC, AVAX, DOGE
- TRX: old rank 7 score 40.7; A-only drop rank —; A-only 0.5× rank 24 score 20.3; A+C rank — score —
- XLM: old rank 13 score 37.4; A-only drop rank 3; A-only 0.5× rank 3 score 37.4; A+C rank 15 score 17.5
- DOGE: old rank 19 score 30.3; A-only drop rank 7; A-only 0.5× rank 7 score 30.3; A+C rank 5 score 30.3
- SHIB: old rank 20 score 29.8; A-only drop rank 8; A-only 0.5× rank 8 score 29.8; A+C rank 6 score 29.8
- BTC: old rank 3 score 43.3; A-only drop rank —; A-only 0.5× rank 20 score 21.6; A+C rank — score —
- ETH: old rank 10 score 38.7; A-only drop rank —; A-only 0.5× rank 27 score 19.4; A+C rank — score —
- SOL: old rank 22 score 29.4; A-only drop rank 10; A-only 0.5× rank 10 score 29.4; A+C rank 8 score 29.4
- XRP: old rank 12 score 38.0; A-only drop rank 2; A-only 0.5× rank 2 score 38.0; A+C rank 2 score 38.0
- WLD: old rank 26 score 26.0; A-only drop rank 13; A-only 0.5× rank 13 score 26.0; A+C rank 17 score 11.0
- ASTER: old rank 1 score 49.3; A-only drop rank —; A-only 0.5× rank 15 score 24.7; A+C rank — score —
- PEPE: old rank 11 score 38.6; A-only drop rank 1; A-only 0.5× rank 1 score 38.6; A+C rank 1 score 38.6
- DOT: old rank 30 score 23.8; A-only drop rank 17; A-only 0.5× rank 18 score 23.8; A+C rank 14 score 23.8
- LTC: old rank 16 score 33.5; A-only drop rank 5; A-only 0.5× rank 5 score 33.5; A+C rank 3 score 33.5
- HBAR: old rank 29 score 24.3; A-only drop rank 16; A-only 0.5× rank 17 score 24.3; A+C rank 13 score 24.3
