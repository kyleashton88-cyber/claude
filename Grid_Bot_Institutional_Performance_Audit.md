# Institutional Performance Audit — Spot Neutral Grid Program

**Source:** `Grid_Bot_Tracker_Excel_1.xlsx` (Setup · Bot Log · Weekly Review)
**Venue:** Pionex (workbook subtitle says "Bybit" — see Data Integrity)
**Audit window:** 2026-09-20 → 2026-10-21 (32 calendar days) · **Starting capital:** 1,000 USDT
**Prepared:** 2026-10-22

> **Scope note — read first.** The journal contains *realized, closed-bot results only* (entry/exit dates, grid range, grid count, investment, final value). It contains **no price series, no fill-level data, no fee line items, no open-bot marks and no intraday timestamps.** Every metric below is labelled **[Measured]** (computed from the journal), **[Derived]** (model-based, assumptions stated) or **[Not computable]** (data absent). Nothing marked Measured has been estimated, and I have not invented ATR, slippage, or Buy-and-Hold figures.

---

## Section I — Executive Summary

### Overall Rating: **6.5 / 10** — *Promising edge, unproven robustness* (provisional)

| Component | Weight | Score | Rationale |
|---|---|---|---|
| Realized return | 25% | 9.0 | +32.3% in 32 days; 33 of 34 bots profitable |
| Risk-adjusted quality | 25% | 5.0 | Ratios are mathematically excellent but **statistically meaningless** (n = 32 days, realized-only, zero MTM drawdown observable) |
| Capital efficiency | 15% | 7.0 | ~80% average deployment; but capital is concentrated in the *lowest-yielding* pairs (TRX, INJ) |
| Grid robustness / boundary risk | 20% | 5.0 | No out-of-range event recorded; single-name concentration (NEAR = 43% of profit) |
| Data integrity | 15% | 5.5 | Example row in totals, orphan rows, concurrency inconsistency, no fee data |
| **Weighted total** | | **6.5** | Rating is *capped by evidence quality*, not by performance |

### High-Level Performance Snapshot

| Metric | Value | Basis |
|---|---|---|
| Total realized profit (in-window, 34 bots) | **+322.94 USDT** | [Measured] ties to Weekly Review |
| Total return on 1,000 USDT | **+32.29%** (≈ +32.3% before 6.2 USDT withdrawal) | [Measured] |
| Closing balance (sheet) | 1,316.74 USDT (after 6.2 withdrawn) | [Measured] |
| Average weekly return | 5.79% (range 4.67% – 7.71%, 5 weeks) | [Measured] |
| Win rate (per bot) | **97.1%** (33 W / 1 L) | [Measured] |
| Profit Factor | **73.6** (327.39 gross wins / 4.45 gross loss) | [Measured] |
| Avg win / avg loss | +9.92 / −4.45 → 2.2 : 1 payoff | [Measured] |
| Expectancy per bot | +9.50 USDT (+3.38% mean, +1.81% median ROI) | [Measured] |
| Maximum drawdown (realized equity) | **0.00%** | [Measured] — **not** a true MDD (no MTM) |
| Sharpe (daily, ann. √365) | 12.6 | [Derived] — not decision-grade |
| Sortino / Calmar | Undefined (no negative day / zero MDD) | [Not computable] |
| Annualized ROI (simple) | ≈ 368% | [Derived] — do not extrapolate |
| CAGR (compounded) | ≈ 2,334% | [Derived] — arithmetic artefact of a 32-day window; **disregard** |
| Grid profit vs. asset appreciation | Cannot be split | [Not computable] — no price data |
| Fee impact | Not recorded | [Not computable]; modelled below |

> ### 🏆 Golden Win
> Weekly returns are unusually stable (4.7% – 7.7%) and the loss distribution is truncated: the single losing bot (ADA, −3.27%) cost 4.45 USDT, i.e. **1.4% of total profit**.

> ### 🚨 Critical Alerts
> 1. **Deployed notional peaks at 3,874 USDT (≈ 2.9× equity) on 2026-10-20.** Either the account uses leverage/margin, bots were run sequentially intra-day (dates have no time component), or investment figures are mis-logged. This must be resolved before any risk figure can be trusted. *(Upper bound — see Section II.)*
> 2. **Zero observable drawdown is a measurement artefact**, not evidence of low risk. Open positions and inventory marks are absent.
> 3. **Profit concentration:** NEAR/USDT = 42.6% of profit; the 7 bots ≥ 900 USDT = 48.1% of profit; the top 3 days = 41.5%.

### Core Strategy Verdict
The program harvests mean reversion in mid-cap altcoin ranges with short holding periods (mean 1.2 days) and has produced a strong, steady realized yield with a very high hit rate. However, the sample covers one month, contains no recorded range break, and omits mark-to-market and fee data — so the observed Sharpe and zero drawdown reflect *harvest-then-exit discipline in a cooperative tape* rather than demonstrated tail resilience. **Viable and worth scaling cautiously; not yet underwritten for larger capital.**

---

## Section II — Grid Microstructure & Operational Audit

### Grid Parameter Review [Measured]

| Parameter | Observed |
|---|---|
| Mode | 100% Neutral (spot-style, two-sided) |
| Grid count | 20 – 181 (median 40) |
| Range width (upper/lower − 1) | 4.8% (WTI) → 188.7% (牛来); median 20.4% |
| Geometric step per grid (derived from range ÷ grids) | mean **0.50%**, min 0.18%, max 1.26% |
| Order distribution | Spacing type not logged; geometric step shown for comparability |
| Holding period | mean 1.18 d, median 1 d; **12 of 34 bots (35%) opened and closed same-day** |
| Bot size | 17 bots < 150 USDT; 9 bots 150–500; 8 bots ≥ 500 (incl. 7 ≥ 900) |

**Grid spacing vs. ATR / volatility regime — [Not computable].** No price history is in the journal. Using step size as a proxy, bots with steps ≤ 0.25% (ADA 0.22%, TRX 0.18%, WTI 0.24%) sit at a fee-fragile spacing (see below). The ratchet in the NEAR lower bound across successive deployments (4.33 → 4.22 → 4.25 → 4.12 → 3.90 between 10/07 and 10/20) is consistent with a downward-drifting or expanding-volatility tape that you were re-centering manually.

### Fee & Execution Drag Analysis

The journal records **Profit as `Final − Investment`**, i.e. already *net of whatever the venue charged*. Gross-vs-net therefore cannot be separated from the data. A model:

> **[Derived — assumption to verify]** Maker/taker on Pionex grid fills ≈ **0.05% per fill** → ≈ **0.10% round-trip** per completed grid cycle.

| Geometric step | Round-trip fee as % of gross cell margin | Net cell margin |
|---|---|---|
| 0.18% (TRX, 9/29) | **≈ 56%** | 0.08% |
| 0.22% (ADA) | **≈ 45%** | 0.12% |
| 0.50% (portfolio mean) | ≈ 20% | 0.40% |
| 0.88% (NEAR typical) | ≈ 11% | 0.78% |

**Finding:** The only losing bot (ADA, 181 grids on a 50% range) is also the tightest-spaced bot in the sample. That is the signature of **fee-dominated spacing** compounded by inventory carry in a trending leg. Rule of thumb: step ≥ 3× round-trip cost (≥ 0.30%).
**Slippage drag:** [Not computable] — recommend logging fill-vs-limit and maker/taker split.

### Inventory Management & Capital Efficiency

| Metric | Value | Basis |
|---|---|---|
| Average deployed notional (calendar-day, inclusive of start/end dates) | ≈ 921 USDT | [Derived], upper bound |
| Average utilization vs. equity | ≈ 80% | [Derived] |
| Zero-deployment days | 3 of 32 (9/24, 9/25, 10/14) | [Measured] |
| **Peak deployed notional** | **3,874 USDT on 10/20 (≈ 2.9× equity)**; 2,577 on 10/10 (≈ 2.2×) | [Derived] — date resolution only |
| Return per unit capital, by pair (cumulative profit ÷ cumulative investment) | HYPE 6.5% · WLFI 10.0% · RENDER 4.0% · NEAR 3.6% · FRAX 3.9% · **INJ 0.84% · TRX 0.28% · COPPER 0.34% · WTI 0.45%** | [Measured] |

**Inventory skew:** Neutral-mode grids start ≈ 50/50 base/quote and become **long-heavy as price falls** (each fill buys the dip). Asymmetric risk is therefore always to the downside: a neutral spot grid is short volatility on the lower tail and long-inventory at the boundary. No bot was reported out-of-range, but all positions were closed within ≤ 7 days — i.e. *the journal shows that risk was avoided by early exit, not that it was absent.*

**Capital-allocation misalignment:** TRX (1,222 USDT deployed → 3.46 profit) and INJ (1,998 → 16.84) absorbed ~27% of all capital-dollars for ~6% of profit, while HYPE/WLFI/RENDER produced 4–10% per deployment on much smaller tickets. Larger tickets are earning **lower** yield per dollar (≥ 500 USDT bucket: 2.1%; 150–500 bucket: 4.8%), which is an efficiency leak.

---

## Section III — Risk & Stress-Testing Assessment

### Boundary Risk Analysis
- **Recorded range breaks: none** [Measured as absent from journal]. Closed-bot data cannot show whether any bot sat below its lower bound for a period before being stopped.
- **[Derived] Value at lower bound.** Model: arithmetic grid, started at range midpoint, half in base asset, equal USDT per buy level, price pinned at the lower bound:

| Bot | Range | Bot size | Modelled loss at lower bound |
|---|---|---|---|
| NEAR (10/10) | 4.22 – 6.15 | 978.61 | **−136.7 USDT (−14.0%)** |
| NEAR (10/20) | 3.90 – 6.07 | 921.42 | **−151.9 USDT (−16.5%)** |
| FRAX (10/10) | 0.2716 – 0.345 | 999.80 | −89.9 USDT (−9.0%) |
| TRX | 0.322 – 0.349 | 1,073.29 | −32.1 USDT (−3.0%) |
| INJ | 8.212 – 8.876 | 998.87 | −28.9 USDT (−2.9%) |

Wide-range bots (NEAR) carry a *deep* inventory tail but earn the most per cycle; narrow-range bots (TRX, INJ) have shallow tails but also minimal yield. A single NEAR lower-bound event would erase **~3 weeks of the program's average profit**.

### Volatility & Regime Sensitivity
| Regime proxy | Observation |
|---|---|
| Wide range / 30–45 grids (NEAR, HYPE) | Highest yield per cycle (NEAR bots 1.6–6.1% ROI, 1–3 d holds) — **high-vol harvesting** |
| Tight range / low vol (TRX, INJ, WTI, COPPER, SOL) | ROI 0.1–1.1%; WTI 7-day hold earned 0.45% — **low-vol consolidation yields poorly relative to capital tied up** |
| Trend-expansion exposure | Only ADA (−3.27%) shows a trend-leg loss |
Regime classification against ATR/ADX is [Not computable] without price data.

### Worst-Case Scenario Assessment [Derived, indicative]
Stack of bots concurrently open on 10/20 (NEAR 955, INJ 999, INJ 999, NEAR 921 — treat as an *upper bound* because of date resolution):

| Shock | Approx. portfolio loss | % of ~1,300 equity |
|---|---|---|
| Alt basket −10% (avg delta ≈ 0.5–0.6 on 3,874 notional) | ≈ −190 to −230 USDT | ≈ −15% to −18% |
| NEAR to lower bound, INJ to lower bound | ≈ −340 USDT | ≈ **−26%** |
| Flash crash −30% through all lower bounds (delta ≈ 0.8): 1.0× notional → 2.9× notional | ≈ −310 → −930 USDT | **−24% → −72%** |

> ### ⚠ Risk Callout
> If the 2.9× peak notional reflects real leverage/margin, a −35% simultaneous move on that stack is a **capital-impairment event**. If it reflects sequential same-day cycling, the tail is roughly one-third of that. *The journal cannot distinguish the two — resolve this first.*

### Divergence / Impermanent Loss vs. Buy-and-Hold
[Not computable] — requires entry/exit prices. Required fields: `entry price`, `exit price`, `open-bot unrealized value`. For reference, a neutral grid underperforms Buy-and-Hold whenever price trends beyond the range one-way; it outperforms in sideways/mean-reverting tape. Given 97% win rate over a 32-day window, the strategy mostly sampled the second regime.

---

## Section IV — Data Visualizations

### 1. Equity Curve & Drawdown (realized, USDT; base 1,000, pre-withdrawal)
Buy-and-Hold benchmark: **not available** (no price data) — flat USDT-cash line (1,000) shown as the only benchmark.

```
Equity (USDT)     1,000 ──────────────────────────────────────── (USDT cash benchmark)
09-21  1036  ▇▇▇▇▇▇
09-23  1068  ▇▇▇▇▇▇▇▇▇▇▇
09-26  1077  ▇▇▇▇▇▇▇▇▇▇▇▇
09-28  1100  ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇
09-29  1121  ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇
10-02  1130  ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇
10-04  1136  ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇
10-08  1144  ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇
10-10  1182  ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇
10-13  1244  ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇
10-18  1265  ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇
10-20  1300  ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇
10-21  1323  ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇

Realized drawdown   0% ──────────────────────────────────────── (no down day)
                    ▲ 10/05: ADA −4.45 (netted against +4.47 same-day wins)
Flat days (no closed bot): 14 of 32 — the curve is a staircase, not a continuous mark.
```

### 2. Range Map — NEAR/USDT deployments (the program's largest profit source)
Price axis in USDT, `[` lower bound, `]` upper bound, bars scaled 3.6 → 6.4.

```
price  3.6   4.0   4.4   4.8   5.2   5.6   6.0   6.4
        |     |     |     |     |     |     |     |
09-23   ·   [━━━━━━━━━━━━━━━━━━━━━━]                      3.795–5.000  36 grids  +11.5%
10-07   ·     ·   [━━━━━━━━━━━━]                           4.330–5.630  30 grids  + 1.8%
10-10   ·     ·  [━━━━━━━━━━━━━━━━━━━━━━]                  4.220–6.150  30 grids  + 6.0%
10-16   ·     ·  [━━━━━━━━━━━━━━━━━━━━━━━]                 4.246–6.200  40 grids  + 4.3%
10-19   ·     [━━━━━━━━━━━━━━━━━━━━━━━]                    4.116–6.110  45 grids  + 1.6%
10-20   ·  [━━━━━━━━━━━━━━━━━━━━━━━━━━]                    3.900–6.066  42 grids  + 2.5%
        lower-bound trend:  4.33 → 4.22 → 4.25 → 4.12 → 3.90   (−10% in 13 days)
```
*Trigger price and per-level fill density are not in the journal. Proxy for density — cycle yield per grid count — is tabulated below.*

| Pair | Bots | Capital deployed | Profit | Yield on deployed | Profit per grid-level (avg) |
|---|---|---|---|---|---|
| NEAR | 6 | 3,838 | +137.51 | 3.58% | 0.62 |
| HYPE | 4 | 946 | +61.51 | 6.50% | 0.38 |
| FRAX | 1 | 1,000 | +38.76 | 3.88% | 0.86 |
| 牛来 | 3 | 635 | +21.24 | 3.34% | 0.05 |
| WLFI | 1 | 200 | +19.93 | 9.97% | 0.40 |
| INJ | 2 | 1,998 | +16.84 | 0.84% | 0.37 |
| RENDER | 4 | 350 | +13.97 | 3.99% | 0.07 |
| TRX | 3 | 1,222 | +3.46 | 0.28% | 0.04 |
| ADA | 1 | 136 | **−4.45** | −3.27% | −0.02 |

### 3. Daily PnL Distribution (realized, by bot end date; 1 block ≈ 1.5 USDT)
```
09-21 +36.1 ████████████████████████
09-23 +31.6 █████████████████████
09-26  +9.4 ██████
09-28 +23.2 ███████████████
09-29 +21.0 ██████████████
09-30  +1.1 █
10-02  +7.4 █████
10-04  +6.1 ████
10-08  +7.6 █████
10-10 +38.8 ██████████████████████████
10-12  +2.7 ██
10-13 +59.2 ███████████████████████████████████████   ← best day
10-18 +21.1 ██████████████
10-19  +2.3 ██
10-20 +32.0 █████████████████████
10-21 +23.3 ████████████████
(+ 16 flat days omitted)
```
Weekly PnL (USDT): `W1 +77.1 ███████████████ · W2 +52.8 ██████████ · W3 +52.5 ██████████ · W4 +61.9 ████████████ · W5 +78.7 ███████████████`

---

## Section V — Strategic Optimization & Recommendations

1. **Volatility-adjusted spacing (ATR integration).** Set `step = max(0.30%, 0.15 × ATR(14, 1h)/price)`; reject any configuration with step < 3× round-trip fees. This would have screened the only losing bot (ADA, 0.22%) and the TRX/COPPER/SOL bots whose yield on deployed capital is < 1.2%.
2. **Dynamic re-centering triggers.** The NEAR lower bound was already ratcheted down ~10% in 13 days; formalize it: re-center when price is within 10% of either bound *or* inventory skew > 70% to base; cap re-centers at 2/day to avoid chasing.
3. **Hard stop + trailing harvest.** (a) Stop-and-liquidate if price closes below lower bound −3% or bot mark-to-market ≤ −5% of ticket; (b) harvest when cumulative bot ROI ≥ 2× its rolling median (≈ 3.5%) or after 3 days, whichever first. Your own data shows holds ≤ 3 days produce nearly all profit.
4. **Perp delta-hedge for wide-range tickets.** For bots ≥ 500 USDT with ranges ≥ 30% (NEAR, FRAX), open a short perp equal to `0.5 × notional` at start and scale to track inventory delta; this converts the −14% to −16% lower-bound tail into funding/basis cost (est. 2–5 bps/day) while preserving grid harvest.
5. **Capital reallocation and portfolio caps.** Cap any single pair at 25% of equity and total deployed notional at ≤ 1.0× equity (or ≤ 1.5× if leverage is deliberate and documented). Rotate tickets from TRX/INJ (0.3–0.8% yield) to HYPE/RENDER/WLFI-class volatility; tickets of 150–500 USDT produced the best yield per dollar (4.8%).

---

## Appendix A — Data-Integrity Findings (fix before the next audit)

| # | Finding | Impact |
|---|---|---|
| 1 | **Row 1 is labelled `EXAMPLE ROW: overwrite`** (HYPE, +7.55) yet is included in Weekly Review totals | Total profit overstated by 2.3%; excluding it gives **315.39 USDT (+31.5%)** |
| 2 | Row 4 contains an orphan `FRAX/USDT` label with no data | Harmless to totals; cleanup |
| 3 | Bots 24–26 (BTR ×2, WTI) end 9/14–9/18, **before** the 9/20 tracking start (13.12 USDT) | Correctly excluded from Weekly Review (336.06 raw → 322.94 reported) |
| 4 | Bots 24–37 are logged out of chronological order | Reduces auditability |
| 5 | Workbook subtitle says **Bybit**; Setup says **Pionex**; Focus pair blank | Fee model depends on venue |
| 6 | **Peak concurrent investment (3,874) ≈ 2.9× equity** | Unresolved leverage / sequencing ambiguity |
| 7 | Dates have no time component; 12 bots show `Days Running = 0` | Intraday ROI/annualization impossible |
| 8 | Planned withdrawal 20%; actual **6.2 USDT = 8.0% of Week-1 profit**, none since | Compounding is stronger than plan |
| 9 | Status is Closed for all bots — no open-position marks | True MDD / unrealized loss invisible |
| 10 | Weekly Review shows 52 rows; only 5 weeks populated (forward weeks show 0% return) | Do not average them in |

## Appendix B — Fields to Add for a True 10/10 Audit
`Start time / End time (UTC)` · `Entry price` · `Exit price` · `Spacing type (Arithmetic/Geometric)` · `Fees paid` · `Maker/taker split` · `Grid profit vs. position PnL (Pionex shows both)` · `Max unrealized drawdown per bot` · `Leverage (if any)` · `Open-bot snapshots at each weekly review` · `Stop reason (target / manual / out-of-range)`.

## Appendix C — Methodology
- Daily returns: realized profit attributed to bot **end date**, divided by running balance at the start of that day, 32 calendar days incl. zero-profit days.
- Sharpe = mean/σ × √365 (rf = 0); Sortino and Calmar undefined (no negative day, zero MDD).
- Geometric step = (Upper/Lower)^(1/Grids) − 1.
- Concurrency = sum of investments for all bots whose [start, end] date range contains the day (inclusive; upper bound).
- Lower-bound loss model: arithmetic grid starting at mid-range, 50% base / 50% quote, equal USDT per buy level, price pinned at the lower bound, fees ignored.
- Fee model (0.05% per fill) is an **assumption to verify** against the venue's current schedule.
- The 32-day sample (34 trades) is too small for inferential claims; treat ratios as descriptive only.
