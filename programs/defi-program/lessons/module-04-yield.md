# Module 4 — Yield

![Module 4 — Yield](../assets/modules/module-04.png)

*Outcome: split any APY into organic vs subsidised, and name the risk being paid for.*
*Stage 2 · Practitioner. Source: ATLAS "DeFi & On-Chain" ch. 14–18, 37. Educational content only. Not financial advice. Figures are illustrative.*

![Where DeFi returns come from](../assets/diagrams/profit-sources.png)

---

## Lesson 4.1 — Yield farming: base yield vs emissions *(ch. 14)*

### Objective
Split a farm's APY into what's earned from real activity and what's paid in newly minted tokens.

### Explanation
- **Base yield:** trading fees or borrower interest. Paid by real users.
- **Emissions / incentives:** new tokens the protocol prints to attract deposits. The reward token often falls while emissions continue.
- **Mercenary liquidity:** capital that leaves when incentives end, often taking the base yield with it.

### Worked example
A farm shows **60% APY**: 5% fees + 55% in reward tokens. If the reward token
falls 50% on average while you harvest, the emissions are worth ~27.5%, so the
real return is ~**32.5%**, before impermanent loss and gas. Remove emissions
entirely and you're left with 5%. **Would you take the risk for 5%?** That's the real question.

### Checklist
- [ ] APY split into base vs incentives
- [ ] Reward token valued at a realistic, falling price
- [ ] Harvest-and-sell schedule set

### Quiz
<details><summary>1. What's the test for a farm?</summary>Does the base yield alone justify the risk?</details>
<details><summary>2. Why do emissions APYs fall?</summary>More capital shares the rewards, and the reward token's price often declines.</details>
<details><summary>3. What is mercenary liquidity?</summary>Capital that moves on as soon as incentives end.</details>

---

## Lesson 4.2 — Native staking *(ch. 15)*

### Objective
Understand what staking pays for, and its lock-up and validator risks.

### Explanation
Proof-of-stake networks pay **stakers** to secure the chain. You either run a
validator or **delegate** to one. Rewards come from issuance and fees. Risks:
**slashing** (penalties for validator misbehaviour on some networks),
**unbonding periods** (waiting time to withdraw) and validator downtime.

### Worked example
Staking yields a few percent a year in the staked asset (e.g. ~3%, illustrative).
Your dollar return is still dominated by the asset's price: +3% staking on an
asset that falls 30% is still a large loss. **Stake what you'd hold anyway.**

### Checklist
- [ ] Validator/provider chosen on uptime, fee, concentration and record
- [ ] Unbonding period known
- [ ] Only "hold-anyway" capital staked

### Quiz
<details><summary>1. What do staking rewards pay for?</summary>Securing the network.</details>
<details><summary>2. What is unbonding?</summary>A waiting period before unstaked assets become transferable.</details>
<details><summary>3. Does staking protect against price falls?</summary>No. It adds a small yield; price moves dominate.</details>

---

## Lesson 4.3 — Liquid staking (LSTs) *(ch. 16)*

### Objective
Use liquid staking tokens knowing how they accrue value and how they can depeg.

### Explanation
A **liquid staking token (LST)** represents staked assets plus rewards, and can
be traded or used as collateral. Value accrues by **rebasing** (your balance
grows) or an **exchange rate** that rises (each token is worth more of the
underlying). In stress, an LST can trade at a **discount** to what it redeems for.

### Worked example
An exchange-rate LST goes from 1.000 to 1.030 of the underlying over a year: **3%**.
In a panic it trades at 0.98 on the market. Holders who can wait for redemption
(queue) recover 1.03; holders forced to sell take the 2% discount.
**Never borrow so close to the limit that an LST discount liquidates you.**

### Checklist
- [ ] Accrual method known (rebase vs exchange rate)
- [ ] Redemption path and queue length known
- [ ] Discount alert set if used as collateral

### Quiz
<details><summary>1. Two ways LSTs pass on rewards?</summary>Rebasing balances, or a rising exchange rate.</details>
<details><summary>2. What is an LST discount?</summary>Its market price falling below its redemption value.</details>
<details><summary>3. Who is hurt most by a discount?</summary>Forced sellers and leveraged holders who get liquidated.</details>

---

## Lesson 4.4 — Restaking & shared security *(ch. 17)*

### Objective
Map the extra risk layers restaking adds before accepting its extra yield.

### Explanation
Restaking reuses staked assets to secure additional services, for extra
rewards and often points. Each service adds its own **slashing conditions**,
and **operators** (who run the services) add operational risk. One collateral
base securing many services creates **correlated failure**. Full strategy
treatment: Lesson 10.6.

### Worked example
Stack for one position: ETH → staked → LST → liquid restaking token →
restaking protocol → 4 services. That's **6 layers**, each able to fail. The extra
yield must pay for all of them. Plan with points valued at zero.

### Checklist
- [ ] Every layer of the stack written down
- [ ] Slashing conditions of each service read
- [ ] Sized in the speculative bucket

### Quiz
<details><summary>1. What does restaking add?</summary>Extra rewards in exchange for extra slashing and operator risk.</details>
<details><summary>2. Why is correlated failure a concern?</summary>One collateral base secures many services; a failure can hit them all.</details>
<details><summary>3. How should points be valued when planning?</summary>At zero.</details>

---

## Lesson 4.5 — Vaults & yield optimisers *(ch. 18)*

### Objective
Decide when a vault's fees are worth paying compared with doing it yourself.

### Explanation
A **vault** pools deposits and runs a strategy (often harvesting and
reinvesting rewards). You get **shares**. Costs: **performance fee** (a share of
profits), **management fee** (a share of assets per year), sometimes
**withdrawal fees**. Risks: the vault's code plus **every protocol it uses**.

### Worked example
Gross 10%, 20% performance fee, 0.5% management → **7.5%** net.
DIY instead, compounding weekly at $2 gas:
- $5,000 position: gas = $104/yr = **2.08%** drag → the vault probably wins.
- $500,000 position: gas = **0.02%** drag, while the vault's fees cost 2.5 points → DIY probably wins.

### Checklist
- [ ] Net APY after all vault fees computed
- [ ] Compared with DIY gas drag at my size
- [ ] Every underlying protocol reviewed

### Quiz
<details><summary>1. Gross 12%, 10% performance fee, 1% management. Net?</summary>12 × 0.9 − 1 = 9.8%.</details>
<details><summary>2. Why do vaults suit small positions?</summary>They spread gas costs across all depositors.</details>
<details><summary>3. What risk does a vault add?</summary>Its own code and strategy, on top of every protocol it deposits into.</details>

---

## Lesson 4.6 — Airdrops & points: opportunity cost *(ch. 37)*

### Objective
Price airdrop and points farming as a bet, including its costs.

### Explanation
Protocols reward early users with tokens (**airdrops**), often tracked by
**points** first. Eligibility rules, snapshots and **sybil filters** (removing
people who split into many wallets) decide who gets what. Nothing is promised.
Fake claim sites are one of the most common scams (Lesson 1.6).

### Worked example
`defi_calc.py airdrop --probability 0.3 --value 1500 --costs 200` → EV **$250**.
If the same $10,000 could earn 5% ($500/yr) risk-light elsewhere, the farm must
beat that plus its extra risk, or it's the worse choice.

### Checklist
- [ ] Only actions I'd take anyway, or a capped speculative budget
- [ ] Opportunity cost compared
- [ ] Claims only from verified official links

### Quiz
<details><summary>1. Are points a promise of tokens?</summary>No.</details>
<details><summary>2. What's a sybil filter?</summary>Rules that exclude wallets believed to belong to the same person farming many times.</details>
<details><summary>3. What's the airdrop EV formula?</summary>Probability × value − costs.</details>

---

### Module 4 practical
1. Decompose three real APYs into base vs incentive.
2. Compare one vault's net APY with DIY at your position size.
3. Write the risk stack for one staking or restaking position.
