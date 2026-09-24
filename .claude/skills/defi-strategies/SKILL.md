---
name: defi-strategies
description: Explain, choose, model and plan DeFi strategies (stablecoin lending, staking/LSTs, collateral borrowing, AMM and concentrated LP, stable LP, vaults, incentive farming, airdrops, leveraged loops, delta-neutral funding carry, LP hedges, treasury management) — where each one's return comes from, the maths, execution steps, kill rules and how it loses. Use when the user asks which DeFi strategy to use, how a strategy makes money, whether a yield is worth it, how to size or exit a position, or wants DeFi strategy course content.
---

# DeFi Strategies

The full playbook is `programs/defi-program/03-defi-strategy-mastery.md`
(16 strategies across 5 levels, execution system, progression path, quiz).
Read the relevant strategy card from it before answering.

## Workflow

1. **Regime first.** Classify the market (sideways, uptrend, downtrend or high
   volatility) and use the Part 2 selector to shortlist strategies.
2. **Name the profit engine.** Which of the 5 sources pays: fees, interest,
   security rewards, carry or incentives. If it's only price going up, say so:
   that's a directional bet, not a strategy.
3. **Run the numbers** with `scripts/defi_calc.py` using live rates the user
   provides or that you cite from a source:
   - `il --ratio 2` · `lp-breakeven --ratio 1.5 --days 90 --fee-apr 12`
   - `cl --low 2700 --high 3300`
   - `health --qty 10 --price 3000 --lt 0.8 --debt 12000`
   - `loop --ltv 0.7 --loops 3 --collateral-apy 3.5 --borrow-apy 2.5`
   - `carry --rate-8h 0.01 --short-lev 2`
   - `supply --borrow-apy 8 --utilisation 0.8` · `apy --apr 10 --position 5000 --gas 2`
   - `airdrop --probability 0.3 --value 1500 --costs 200`
4. **Compare to a benchmark** (holding the assets, or plain stablecoin
   lending). The strategy has to beat it after costs by enough to pay for the extra risk.
5. **Protocol check** with `defi-due-diligence` before any capital moves.
6. **Write the plan:** size (within the Part 4 caps), exact kill rules,
   monitoring cadence, journal row.

## Guardrails
- Educational only. Never promise or project guaranteed profits. Present
  returns as "if these rates hold" with the risks that produce them.
- Always state how the strategy loses money alongside how it earns.
- Value incentive tokens at a realistic sale price, not the headline APY.
- Beginners start at Level 1. Don't recommend leverage or carry until the
  user shows they understand liquidation, funding and margin.
- Never ask for seed phrases, private keys or API secrets.
