# Module 2 — Trading On-Chain

![Module 2 — Trading On-Chain](../assets/modules/module-02.png)

*Outcome: execute a swap or LP position deliberately, understanding price impact, fees, impermanent loss and MEV.*
*Source: ATLAS "DeFi & On-Chain" ch. 6–9, 35. Educational content only. Not financial advice. Figures illustrative.*

Lesson 2.2 (AMM mathematics) is in `../02-sample-lesson-amm-math.md`.

---

## Lesson 2.0 — Mastery Starter

*New to this topic? Start here. It takes about 10 minutes and gets you from zero to ready for this module.*

### The 60-second version
A swap on a DEX trades against a pool of tokens priced by a formula. Providing liquidity to that pool earns fees but changes what you hold. This module teaches you to trade and provide liquidity knowing the real cost.

### Words you'll need
| Term | Meaning |
|---|---|
| DEX | a decentralised exchange you use from your wallet |
| Liquidity pool | a pot of two tokens traders swap against |
| Price impact | how much your trade moves the price |
| Slippage | the worst price you'll accept |
| Impermanent loss | how far an LP lags simply holding |

### Before you start
- [ ] Modules 0–1
- [ ] A little ETH for gas and some USDC on a low-fee network

### Your first safe step
Quote a $20 swap on one DEX and on an aggregator; compare what you'd actually receive after gas. Don't execute yet.

### The mastery ladder
| Level | You can… |
|---|---|
| **Beginner** | Makes small swaps with deliberate slippage and protected routing |
| **Practitioner** | Calculates fee APR and IL, and tracks LP vs holding |
| **Master** | Uses limit/TWAP/intent orders and runs LPs with written rules |

### You've mastered this module when…
…you can predict a swap's cost and an LP position's result against holding, before you enter.

---

## Lesson 2.1 — DEXs, aggregators & routing *(ch. 6)*

### Objective
Choose where to swap by comparing the **net amount received**, not the quoted price.

### Explanation
- **AMM DEX**: you trade against a liquidity pool priced by a formula (Lesson 2.2).
- **On-chain order book**: orders matched by price and time, fully or partly on-chain.
- **Aggregator**: searches many pools and venues and may split your order across routes.
- **Price impact**: how much *your* trade moves the price. It grows with size relative to pool depth.
- **Slippage tolerance**: the worst price you'll accept before the transaction reverts.
- **Routing**: multi-hop routes (A → B → C) can give a better price but touch more contracts.

**What you actually get = quoted output − price impact − pool fees − gas.**

### Worked example
Selling **20 ETH**:
| Route | Output | Gas | Net |
|---|---|---|---|
| Single pool direct | 59,100 USDC | $8 | **59,092** |
| Aggregator (split across 3 pools) | 59,420 USDC | $20 | **59,400** |

The aggregator wins by ~$308. Now selling **0.5 ETH**: the aggregator quotes $3
better but costs $12 more in gas, so the direct pool wins. **Big trades
benefit from routing. Small trades mostly lose to gas.**

### Checklist
- [ ] Compare net output after gas, not headline price
- [ ] Price impact shown and acceptable for the size
- [ ] Route uses reputable pools and tokens you've verified
- [ ] Slippage set on purpose (see 2.5)

### Quiz
<details><summary>1. Why can an aggregator give a better price?</summary>It can split an order across pools, so each pool's price moves less.</details>
<details><summary>2. When does the best quote lose?</summary>When the extra gas costs more than the price improvement, which is common for small trades.</details>
<details><summary>3. What drives price impact?</summary>Trade size relative to pool liquidity.</details>

---

## Lesson 2.3 — Providing liquidity *(ch. 8)*

### Objective
Estimate an LP position's fee income from real pool data.

### Explanation
When you LP you deposit both tokens and receive a share of the pool (a token,
or an NFT for concentrated positions). You earn your share of swap fees. In
return, **your token mix changes as traders move the price**: you become
the counterparty to every trade.

**Fee APR estimate:**
`fee APR ≈ (daily volume × fee tier × your pool share × 365) ÷ your deposit`
For a full-range pool your share = deposit ÷ pool TVL, so this simplifies to
`daily volume × fee tier × 365 ÷ TVL`.

Use a **30-day average volume**, not today's. Volume spikes on volatile days,
which are also the days you take the most impermanent loss.

### Worked example
Pool TVL **$10M**, 30-day average daily volume **$2M**, fee tier **0.3%**:
- Daily pool fees = 2,000,000 × 0.003 = **$6,000**
- Your $10,000 = 0.1% share → **$6/day** → ~**21.9% fee APR** (before impermanent loss and gas)

If volume halves, your fee APR halves. If a lot more TVL joins the pool, your share shrinks.

### Checklist
- [ ] Fee APR calculated from 30-day volume
- [ ] I'm OK holding 100% of either token
- [ ] Entry prices recorded for the "vs hold" benchmark
- [ ] Exit rule written (volume drops, trend starts, fees stop covering IL)

### Quiz
<details><summary>1. Pool TVL $5M, daily volume $1M, 0.05% fee. Full-range fee APR?</summary>1,000,000 × 0.0005 × 365 ÷ 5,000,000 = 3.65%.</details>
<details><summary>2. Why use 30-day volume?</summary>Single-day spikes overstate fee income, and they happen on the days you take the most impermanent loss.</details>
<details><summary>3. What happens to your share if TVL doubles?</summary>It halves, and so do your fees, at the same volume.</details>

---

## Lesson 2.4 — Impermanent loss & true LP P&L *(ch. 9)*

### Objective
Calculate an LP position's full P&L and judge it against simply holding.

### Explanation
**Impermanent loss (IL)** is how much the LP position lags *simply holding the
same starting tokens* when their relative price changes:
`IL = 2√r ÷ (1 + r) − 1` (r = new price ÷ entry price). It's "impermanent" only
if price returns. Withdraw after the move and it's permanent.

**Full LP P&L = LP value + fees + incentives − gas**, compared to **hold value**.

### Worked example

![Impermanent loss vs holding](../assets/charts/impermanent-loss.png)

Deposit **1 ETH + 3,000 USDC** at ETH = $3,000 (total $6,000). ETH rises to **$4,000**.
- Pool rebalances you to √(3,000 ÷ 4,000) = **0.866 ETH** and √(3,000 × 4,000) = **3,464 USDC**
- LP value = 0.866 × 4,000 + 3,464 = **$6,928**
- Hold value = 4,000 + 3,000 = **$7,000** → IL = −$72 (**−1.03%**)
- Fees earned $150, gas $20 → LP total **$7,058**

| Compared with | Result |
|---|---|
| Starting $6,000 | +$1,058 (mostly from ETH going up, not from LPing) |
| Holding | **+$58**, the actual value added by LPing |

A master judges the LP on the **+$58**, not the +$1,058.

Calculator: `defi_calc.py il --ratio 1.3333` · `defi_calc.py lp-breakeven --ratio 1.5 --days 90 --fee-apr 12`

### Checklist
- [ ] P&L tracked against hold, weekly
- [ ] IL, fees, incentives and gas recorded separately
- [ ] Exit if fees consistently fail to cover IL

### Quiz
<details><summary>1. ETH doubles. IL on a 50/50 pool?</summary>About −5.7% vs holding.</details>
<details><summary>2. Your LP is up 20% since deposit. Did LPing work?</summary>Unknown until you compare with holding. The 20% could be all price.</details>
<details><summary>3. When does IL become permanent?</summary>When you withdraw while the price ratio is different from entry.</details>

---

## Lesson 2.5 — MEV and protecting your trades *(ch. 35)*

### Objective
Set slippage and routing so your trades aren't easy targets.

### Explanation
**MEV** (maximal extractable value) is profit taken by whoever orders
transactions in a block. Some is harmless (arbitrage realigning prices). The
kind that hurts you:
- **Sandwich attack**: a bot sees your pending swap, buys just before you
  (pushing the price up), lets your trade execute at the worse price, then
  sells just after. Your slippage tolerance is its profit ceiling.

**Defences:**
- Tight but realistic slippage (e.g. 0.1–0.5% for liquid majors, more only when you understand why)
- MEV-protected / private transaction routing (many wallets and aggregators offer this)
- Split large trades. Avoid thin pools
- Don't broadcast huge swaps in illiquid pairs

### Worked example
Swapping **$20,000**:
| Slippage tolerance | Max a sandwich can take (before its own costs) |
|---|---|
| 3% | up to ~$600 |
| 0.5% | up to ~$100 |
| Private / protected route | Transaction isn't visible in the public mempool, so it can't be sandwiched from there |

Too tight a tolerance (e.g. 0.05% on a volatile pair) just makes the transaction
fail, and failed transactions still cost gas (Lesson 1.2).

### Checklist
- [ ] Slippage set for this pair and size, never left at a high default
- [ ] Protected routing on for larger swaps
- [ ] Large orders split or routed through deep liquidity

### Quiz
<details><summary>1. What limits how much a sandwich bot can take?</summary>Your slippage tolerance (and the pool's depth).</details>
<details><summary>2. Why not set slippage near zero?</summary>Normal price movement makes the transaction revert, and you still pay gas.</details>
<details><summary>3. Name two MEV defences.</summary>Any two: tight slippage, private/protected routing, splitting trades, using deep pools.</details>

---

## Lesson 2.6 — Advanced execution: limit, TWAP and intent-based orders *(new)*

### Objective
Use order types that give you better prices and protection than a plain swap.

### Explanation
- **On-chain limit orders:** you sign an order off-chain ("sell 1 ETH at 3,300 or better"); it fills only if the price is reached. Usually gasless until filled.
- **TWAP orders:** split a large trade into equal slices over time to reduce price impact.
- **Intent-based / RFQ trading:** you state what you want ("100,000 USDC → ETH, at least X"); competing **solvers** or market makers fill it, often with MEV protection and no failed-transaction gas.
- **Trade-offs:** limit orders may never fill; TWAP takes time and the price can move away; intents rely on the protocol's solver design.

### Worked example
Buying $50,000 of ETH in a pool where a single $50,000 trade has ~1.5% price impact
(~$750). A TWAP of 10 × $5,000 over an hour has far less impact per slice, as long
as the price doesn't trend against you during the hour. An intent-based order may
beat both by sourcing liquidity from several venues at once. Compare the quotes.

### Checklist
- [ ] I compare a plain swap, a TWAP and an intent quote for large trades
- [ ] Limit orders have an expiry I've chosen
- [ ] I know which order types include MEV protection

### Quiz
<details><summary>1. Why split a large trade into a TWAP?</summary>Smaller slices cause less price impact each.</details>
<details><summary>2. What's the risk of a limit order?</summary>It may never fill.</details>
<details><summary>3. Who fills an intent-based order?</summary>Competing solvers or market makers.</details>

---

## Lesson 2.7 — Advanced AMM design and LVR *(expert)*

### Objective
Know the major AMM designs and measure an LP's real cost with loss-versus-rebalancing (LVR).

### Explanation
- **Constant product (x·y=k):** works for any pair; spreads liquidity across all prices.
- **StableSwap:** for assets that should trade near 1:1 (stablecoins, LST/ETH). Blends constant-sum (flat, low slippage near the peg) with constant-product (safety away from it), tuned by an **amplification** parameter.
- **Weighted pools:** more than two tokens or uneven weights (e.g. 80/20), with invariant ∏ xᵢ^wᵢ = k. An 80/20 pool has less impermanent loss on the 80% token.
- **Concentrated liquidity:** positions in price ranges ("ticks"); the pool tracks √price internally.
- **Hooks and dynamic fees:** newer designs (e.g. Uniswap v4, 2025) let pools run custom code at swap time: dynamic fees, limit orders, oracles. Each hook is extra contract risk.
- **LVR (loss-versus-rebalancing):** pool prices only update when arbitrageurs trade against LPs after prices move elsewhere. LVR measures what LPs lose to that arbitrage, versus a portfolio that rebalances at market prices. For a full-range constant-product pool, **LVR ≈ σ²/8 of pool value per year** (σ = annual volatility). **Fees must beat LVR**, not just impermanent loss.

![Loss-versus-rebalancing vs volatility](../assets/charts/lvr.png)

### Worked example
An ETH/USDC full-range pool with ETH volatility **80%/yr**:
`defi_calc.py lvr --vol 80 --fee-apr 12` → LVR ≈ **8.0%/yr**. With 12% fee APR, LPs keep
≈ **+4%/yr** before gas. If volatility rises to 110%, LVR ≈ 15%/yr, and the same fees now lose money.
Higher-volatility pairs need much higher fee tiers.

### Checklist
- [ ] I choose pool type by pair: StableSwap for pegged pairs, weighted/CL otherwise
- [ ] I compare fee APR with LVR, not just IL
- [ ] Hook contracts reviewed like any other contract

### Quiz
<details><summary>1. Why do stable pairs use StableSwap curves?</summary>They give very low slippage near the peg, where these pairs trade.</details>
<details><summary>2. What does LVR measure?</summary>What LPs lose to arbitrageurs because pool prices lag the market.</details>
<details><summary>3. Volatility 60%/yr: approximate LVR for a full-range pool?</summary>0.6²/8 = 4.5% of pool value per year.</details>

---

## Lesson 2.8 — The MEV supply chain *(expert)*

### Objective
Understand who sees, orders and profits from your transactions, and how to get some of that value back.

### Explanation
The path of an Ethereum transaction today:
1. **You / your wallet** send it, either to the **public mempool** or to a **private RPC** (e.g. an MEV-protection endpoint).
2. **Searchers** scan for opportunities (arbitrage, liquidations, backruns, sandwiches) and submit **bundles**.
3. **Builders** assemble the most profitable blocks from transactions and bundles.
4. **Relays** pass blocks to **proposers** (validators), who pick the highest-paying block (**proposer-builder separation**, via MEV-Boost).
- **Order-flow auctions / MEV rebates:** some private RPCs and wallets let searchers bid to backrun your transaction and **refund you part** of the value.
- **Intent systems** (Lesson 2.6) move competition to solvers, often with built-in protection.
- L2s usually have a **single sequencer** ordering transactions, which changes MEV dynamics (e.g. first-come-first-served or priority-fee ordering).

![The MEV supply chain](../assets/diagrams/mev-supply-chain.png)

### Worked example
A $100,000 swap sent publicly with 1% slippage could leak up to ~$1,000 to a sandwich.
Sent through a protected RPC with rebates: no sandwich, and if the trade creates a
backrun opportunity (e.g. arbitrage between pools), you may receive a share of it back.
Same trade, very different outcome, decided by where you send it.

### Checklist
- [ ] Large trades go through a protected RPC, an intent system or an aggregator with MEV protection
- [ ] I know whether my wallet's RPC offers rebates
- [ ] I understand my L2's sequencer ordering rules

### Quiz
<details><summary>1. What do builders do?</summary>Assemble blocks from transactions and searcher bundles to maximise value.</details>
<details><summary>2. What is an MEV rebate?</summary>A refund of part of the value searchers extract from backrunning your transaction.</details>
<details><summary>3. Who orders transactions on most L2s today?</summary>A sequencer, often a single operator.</details>

---

### Module 2 practical
1. Quote the same swap on a single DEX and an aggregator. Record the net output after gas for a small and a large size.
2. Pick a real pool and calculate its full-range fee APR from 30-day volume and TVL.
3. Model an LP entry with `defi_calc.py`: IL at ±25% and ±50%, and the fee APR needed to break even over 90 days.
4. Turn on protected routing in your wallet or aggregator and set a default slippage you can justify.
