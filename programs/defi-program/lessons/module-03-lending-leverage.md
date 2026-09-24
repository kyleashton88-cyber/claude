# Module 3 — Lending & Leverage

![Module 3 — Lending & Leverage](../assets/modules/module-03.png)

*Outcome: borrow against collateral with a buffer and a written defence plan.*
*Stage 2 · Practitioner. Source: ATLAS "DeFi & On-Chain" ch. 10–13. Educational content only. Not financial advice. Figures are illustrative.*

---

## Lesson 3.0 — Mastery Starter

*New to this topic? Start here. It takes about 10 minutes and gets you from zero to ready for this module.*

### The 60-second version
Lending markets let you earn interest by lending, or borrow against what you own without selling it. Borrowing comes with one hard rule: if your collateral falls too far, it's sold automatically, at a penalty.

### Words you'll need
| Term | Meaning |
|---|---|
| Collateral | what you lock up to borrow |
| LTV | debt ÷ collateral value |
| Health factor | your safety margin; below 1 means liquidation |
| Liquidation | forced sale of collateral to repay debt |
| Utilisation | how much of a pool is borrowed |

### Before you start
- [ ] Modules 0–2
- [ ] Comfort using a DEX on a low-fee network

### Your first safe step
Supply $20 of USDC to a blue-chip lending market, read its utilisation, then withdraw it. No borrowing yet.

### The mastery ladder
| Level | You can… |
|---|---|
| **Beginner** | Supplies stablecoins and reads utilisation and rates |
| **Practitioner** | Borrows with HF ≥ 2 and a written defence ladder |
| **Master** | Runs correlated loops and perps with computed liquidation prices and break-even rates |

### You've mastered this module when…
…you can open, monitor and unwind a borrow without ever approaching liquidation.

---

## Lesson 3.1 — How lending markets work *(ch. 10)*

### Objective
Explain where lending yields come from and why rates jump when a market is nearly fully borrowed.

### Explanation
A DeFi **money market** is a pool: lenders **supply** assets, borrowers
**borrow** them against collateral, and a smart contract sets the rates.
- **Utilisation** = borrowed ÷ supplied. It drives the rates.
- **Interest-rate curve:** most markets use a "kinked" curve. Rates rise gently
  up to an **optimal utilisation** (e.g. 80%), then steeply above it, to pull in
  lenders and push out borrowers.
- **Supply APY ≈ borrow APY × utilisation × (1 − reserve factor).** The reserve
  factor is the protocol's cut.
- **Receipt tokens:** when you supply, you get a token representing your
  deposit plus interest.

### Worked example (illustrative curve: 4% at 80% optimal, +60% slope above)
| Utilisation | Borrow APY | Supply APY (10% reserve factor) |
|---|---|---|
| 50% | 2.5% | 1.1% |
| 70% | 3.5% | 2.2% |
| 80% | 4.0% | 2.9% |
| 90% | 34.0% | 27.5% |
| 95% | 49.0% | 41.9% |

Near 100% utilisation, rates spike **and lenders may not be able to withdraw**,
because the money is lent out. A sudden high supply APY is often a warning, not a gift.

### Checklist
- [ ] I check utilisation before supplying
- [ ] I know the market's optimal-utilisation kink
- [ ] I treat a sudden rate spike as a liquidity warning

### Quiz
<details><summary>1. What sets the rates in a money market?</summary>Mainly utilisation, through the protocol's interest-rate curve.</details>
<details><summary>2. Why does the curve kink?</summary>To make borrowing expensive and supplying attractive when liquidity runs low, restoring withdrawal capacity.</details>
<details><summary>3. Utilisation is 99%. Risk for lenders?</summary>Withdrawals may be blocked until borrowers repay or new supply arrives.</details>

---

## Lesson 3.2 — LTV, liquidation threshold & health factor *(ch. 11)*

### Objective
Calculate your LTV, health factor and liquidation price before you borrow.

### Explanation
- **LTV (loan-to-value)** = debt ÷ collateral value.
- **Max LTV:** the most you can borrow against an asset.
- **Liquidation threshold (LT):** the LTV at which your position can be liquidated. It's higher than max LTV.
- **Health factor (HF)** = (collateral value × LT) ÷ debt. **Below 1.0 = liquidatable.**
- **Liquidation price** = debt ÷ (collateral quantity × LT).

![The liquidation cascade](../assets/diagrams/liquidation-cascade.png)

### Worked example
10 ETH at $3,000 ($30,000), LT 0.80, borrow $12,000:
- LTV **40%** · HF **2.0** · liquidation at **$1,500** (−50%)
- `defi_calc.py health --qty 10 --price 3000 --lt 0.8 --debt 12000`
- Max debt for HF 2.0 = $12,000; for HF 1.5 = $16,000.

### Checklist
- [ ] HF and liquidation price calculated before borrowing
- [ ] HF ≥ 2 for volatile collateral
- [ ] Alerts set (Module 14.1)

### Quiz
<details><summary>1. Collateral $50,000, LT 0.8, debt $20,000. HF?</summary>2.0.</details>
<details><summary>2. Why keep HF well above 1?</summary>Collateral prices can fall fast; the buffer is your time to react.</details>
<details><summary>3. Max LTV vs liquidation threshold?</summary>Max LTV caps new borrowing; the liquidation threshold is where liquidation becomes possible.</details>

---

## Lesson 3.3 — Liquidations and cascades *(ch. 12)*

### Objective
Know exactly what a liquidation costs you, and how to avoid ever reaching one.

### Explanation
When HF drops below 1, a **liquidator** (usually a bot) repays part of your debt
(up to the **close factor**, often 50%) and takes that value of your
collateral **plus a bonus** (the liquidation penalty, often 5–10%).
Liquidations sell collateral into a falling market, which can push prices
lower and trigger more liquidations: a **cascade**.

### Worked example
Your position from 3.2. ETH falls to **$1,490**, HF just under 1:
- A liquidator repays **$6,000** (50% close factor) and seizes $6,000 × 1.05 = **$6,300** of ETH ≈ **4.228 ETH**.
- The **$300** bonus is a pure loss to you, on top of having sold ETH near the low.

**Defence ladder:** HF 2.0 → alert; HF 1.7 → repay from reserve or add
collateral; HF 1.5 → sell part of the collateral yourself. Never wait for 1.1.

### Checklist
- [ ] Defence ladder written with exact HF levels
- [ ] Reserve set aside to repay (Module 12.4)
- [ ] Oracle for my collateral known (Module 5.3)

### Quiz
<details><summary>1. What does a liquidator receive?</summary>Collateral equal to the debt repaid plus a bonus (penalty).</details>
<details><summary>2. Why is self-deleveraging better than being liquidated?</summary>You avoid the penalty and choose the size and timing.</details>
<details><summary>3. How do cascades form?</summary>Liquidations sell collateral, pushing prices down, which pushes more positions below HF 1.</details>

---

## Lesson 3.4 — Borrowing strategies & looping *(ch. 13)*

### Objective
Use borrowing deliberately, and know when looping adds return and when it just adds risk.

### Explanation
- **Liquidity without selling:** borrow stablecoins against assets you want to keep (Module 12.3 turns this into a credit policy).
- **Looping:** deposit → borrow → re-deposit → repeat, to multiply exposure. After n loops at LTV L: leverage = `(1 − L^(n+1)) ÷ (1 − L)`.
- **Net APY on equity** = collateral yield × leverage − borrow rate × (leverage − 1).
- **Correlated loops** (an LST against its underlying, or stablecoin against stablecoin) are far safer than volatile-against-stable loops.

![Leveraged loop: the spread is everything](../assets/charts/loop-spread.png)

### Worked example
LTV 0.7, 3 loops, 3.5% collateral yield, 2.5% borrow:
`defi_calc.py loop --ltv 0.7 --loops 3 --collateral-apy 3.5 --borrow-apy 2.5`
→ **2.53×** leverage, **5.03%** net on equity. The return is wiped out if borrow rises to **5.78%**.
Section 3.1 showed borrow rates can jump from 4% to 34% in hours. That's the risk.

### Checklist
- [ ] Repayment source named before borrowing
- [ ] Loops only on correlated pairs, below max leverage
- [ ] Break-even borrow rate known and alerted

### Quiz
<details><summary>1. Max leverage at LTV 0.75?</summary>4×.</details>
<details><summary>2. What single number decides whether a loop is worth it?</summary>The spread between collateral yield and borrow rate.</details>
<details><summary>3. Why prefer correlated loops?</summary>Collateral and debt move together, so price moves barely change HF.</details>

---

## Lesson 3.5 — Perpetual futures and margin on-chain *(new)*

### Objective
Understand perp positions well enough to use them for hedging (Module 11) and carry (10.3), and to see why high leverage fails.

### Explanation
- A **perpetual future (perp)** tracks an asset's price with no expiry. You post **margin** and choose **leverage**.
- **Isolated margin:** only the margin in that position is at risk. **Cross margin:** your whole account backs every position (one bad trade can drain the rest).
- **Mark price** (used for liquidation) vs **index price** (spot reference). **Funding** is paid between longs and shorts, usually every hour or 8 hours.
- **Liquidation** happens when your margin falls to the **maintenance margin**. Roughly, a long is liquidated after a fall of `1 ÷ leverage − maintenance margin`.

### Worked example
Long ETH from $3,000 at **5×**, 0.5% maintenance margin:
`defi_calc.py perp --entry 3000 --leverage 5 --mmr 0.5` → liquidation ≈ **$2,415 (−19.5%)**.
The same short at **20×** is liquidated at ≈ **$3,135 (+4.5%)**, a move ETH can make in an hour.
Leverage doesn't just magnify gains: it shrinks how wrong you're allowed to be.

### Checklist
- [ ] Isolated margin by default
- [ ] Liquidation price computed before opening
- [ ] Leverage ≤ 2–3× for anything but a hedge I fully understand
- [ ] Funding cost checked for how long I'll hold

### Quiz
<details><summary>1. Isolated vs cross margin?</summary>Isolated risks only that position's margin; cross puts the whole account behind every position.</details>
<details><summary>2. Roughly how far can a 10× long fall before liquidation (0.5% maintenance)?</summary>About 9.5%.</details>
<details><summary>3. Which price triggers liquidation?</summary>The mark price.</details>

---

## Lesson 3.6 — Lending design deep dive: e-mode, caps, auctions, soft liquidation, bad debt *(expert)*

### Objective
Read a lending protocol's risk parameters like a risk manager.

### Explanation
- **Efficiency mode (e-mode):** higher LTVs for **correlated** assets (e.g. an LST against ETH, or stablecoin against stablecoin). Great for correlated loops; dangerous if the correlation breaks (a depeg).
- **Isolation mode / isolated markets:** newer or riskier collateral can only back limited borrowing, so its failure can't infect the whole pool.
- **Supply and borrow caps:** limits on how much of an asset can be deposited or borrowed, protecting against manipulation and illiquid collateral.
- **Liquidation mechanisms:** a **fixed bonus** (liquidators get e.g. 5% extra) vs **Dutch auctions** (the price falls until someone buys, a better price discovery in calm markets but vulnerable if keepers fail) vs **soft liquidation** (collateral is converted gradually across price bands as the price falls, and can convert back if the price recovers; losses come from the conversions rather than one penalty).
- **Bad debt:** when collateral is worth less than the debt it backs. Who pays: a reserve or insurance fund, a staking "safety module", or **lenders pro rata** (socialised).
- **Risk curators / risk managers** set these parameters; governance approves them.

![The liquidation cascade](../assets/diagrams/liquidation-cascade.png)

### Worked example
An LST loop in e-mode at 90% LTV looks safe because LST and ETH move together.
If the LST trades at a 6% discount on the oracle during a panic, the "correlated"
position can be liquidated even though ETH's price didn't move. Check what
oracle prices the LST (market price vs exchange rate) before trusting e-mode.

### Checklist
- [ ] For each market: LTV, liquidation threshold, bonus/mechanism, caps, oracle
- [ ] I know who absorbs bad debt in each protocol I lend to
- [ ] E-mode positions have a depeg scenario in my stress test

### Quiz
<details><summary>1. What is e-mode for?</summary>Higher LTVs on correlated assets.</details>
<details><summary>2. How does soft liquidation differ from a fixed-bonus liquidation?</summary>Collateral is converted gradually across price bands (and can convert back) instead of being seized in one go with a penalty.</details>
<details><summary>3. Who can end up paying for bad debt?</summary>Protocol reserves, a safety module, or lenders pro rata.</details>

---

## Lesson 3.7 — CDP stablecoins: minting your own dollars *(expert)*

### Objective
Mint stablecoins against your own collateral (as your own bank would), and manage the position safely.

### Explanation
- A **CDP** (collateralised debt position) lets you lock collateral and **mint** a stablecoin against it. You owe the stablecoin back, plus a **stability fee** (interest).
- **Minimum collateral ratio** (e.g. 150%): below it, the position is liquidated.
- The stablecoin holds its peg through over-collateralisation, liquidations, interest rates and often a **peg stability module (PSM)** that swaps it 1:1 (minus a small fee) with other stablecoins.
- Compared with borrowing from a lending pool: you create new money rather than borrow someone's deposit; rates are set by governance, not utilisation.
- **Uses:** liquidity without selling (Module 12.3), funding a liquidity ladder, or a yield-covered credit line (strategy #25).

### Worked example
10 ETH at $3,000 ($30,000) with a 150% minimum ratio: you could mint up to $20,000.
Mint **$10,000** instead:
`defi_calc.py cdp --qty 10 --price 3000 --mint 10000 --fee 6`
→ ratio **300%**, liquidation at **$1,500 (−50%)**, stability fee **$600/yr**.
Operators treat the maximum as a cliff, not a target.

### Checklist
- [ ] Collateral ratio target (e.g. ≥ 250%) and action levels written
- [ ] Stability fee vs alternatives (lending-pool borrow rates) compared
- [ ] Peg mechanism (PSM, rates) understood, and my exit if the stablecoin depegs

### Quiz
<details><summary>1. What do you owe on a CDP?</summary>The minted stablecoin plus the accrued stability fee.</details>
<details><summary>2. Collateral $40,000, 150% minimum ratio. Maximum mint?</summary>About $26,667.</details>
<details><summary>3. What does a PSM do?</summary>Swaps the stablecoin 1:1 (minus a fee) with other stablecoins, supporting the peg.</details>

---

### Module 3 practical
1. Pick a real lending market: record utilisation, supply and borrow APY, and the kink.
2. Model a borrow with `defi_calc.py health`; write your defence ladder.
3. Model one loop with `defi_calc.py loop` and write its break-even borrow rate.
