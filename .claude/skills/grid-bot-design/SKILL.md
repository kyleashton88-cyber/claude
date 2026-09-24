---
name: grid-bot-design
description: Design, sanity-check and document a grid bot configuration (spot or futures) using the ATLAS Grid Bot Builder method — regime, range, spacing, fee-adjusted economics, risk and invalidation — and log it to the Notion "Grid Bot Pre-Launch Checklist". Use when the user or a Grid Bot Builder customer asks to set up, review, troubleshoot or explain a grid bot, or when writing Grid Bot Builder course/support content.
---

# Grid Bot Design

Source: Notion → ATLAS → *Grid Bot Builder (Complete Module)*. Educational
modelling only — not an order ticket, not a return forecast. Live tick size,
min order size, fees, spread, funding and liquidation rules must be checked on
the exchange.

## The four questions (answer before any numbers)

1. **Regime** — is price rotating, or is the range likely to break?
   Excellent: sideways/consolidation, liquid, moderate volatility.
   Conditional: slow trend, orderly pullbacks. Poor: breakout, parabolic,
   flash crash, major news (FOMC/CPI/jobs), thin liquidity.
2. **Range** — where it begins, ends and **invalidates** (support/resistance +
   recent volatility, with room for normal wicks).
3. **Economics** — is spacing large enough after fees and slippage?
4. **Risk** — what happens if price leaves the range and doesn't return?

## Math

Run `scripts/grid_calc.py` for the numbers:

```
python3 .claude/skills/grid-bot-design/scripts/grid_calc.py \
  --lower 58000 --upper 72000 --grids 20 --capital 5000 \
  --mode geometric --fee 0.1 --slippage 0.05
```

It prints the levels, capital per grid, gross step %, net step % after
round-trip costs and flags a grid whose net step is ≤ 0 or thin.

Formulas: width = upper − lower · arithmetic spacing = width ÷ grids ·
geometric ratio = (upper/lower)^(1/grids) · capital per grid = capital ÷ grids
· gross step % = spacing ÷ buy price × 100 · net step % = gross − 2×fee −
slippage (− funding for futures).

## Spot vs futures
Default to **spot** for beginners (no leverage liquidation, no funding).
Futures only when the user can state liquidation price, margin behaviour,
funding cost and directional exposure.

## Risk tier
Green: spot, liquid pair, no leverage, wide invalidation. Blue: structured
market, planned exit. Amber: futures, mild leverage, event risk. Red: high
leverage, thin liquidity, news, poor liquidation buffer.

## Pre-launch gate (all must be true)
- [ ] Regime classified
- [ ] Range boundaries justified
- [ ] Grid count + spacing mode chosen
- [ ] Fees/funding modelled against gross step
- [ ] Coin score reviewed (liquidity, volume, volatility, spread, funding, correlation)
- [ ] Risk % per bot and portfolio defined
- [ ] Invalidation written down
- [ ] Monitoring cadence + alerts set

On confirmation, add a row to Notion **Grid Bot Pre-Launch Checklist**:
`Deployment` (title), `Pair`, `Range Low`, `Range High`, `Grid Count`,
`Spacing Mode` (Arithmetic/Geometric), `Status` (Draft/Ready/Launched/Paused/
Closed) and the checkboxes `Regime Classified`, `Fees Modeled`,
`Coin Score Reviewed`, `Risk % Defined`, `Invalidation Defined`.

## Troubleshooting order
Separate realised grid profit from unrealised inventory P&L first, then:
no trades → spacing/range/orders live · tiny profits → spacing vs fees ·
price out of range → rebuild/pause/exit per plan · funding eating profit →
spot alternative · liquidation close → reduce leverage · idle capital → density.

## Guardrails
Never ask for or handle exchange API keys (customers connect them inside the
Grid Bot Builder tool). No profit promises. Change one variable at a time when
optimising.
