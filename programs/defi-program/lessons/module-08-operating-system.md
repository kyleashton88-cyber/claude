# Module 8 — The DeFi Operating System

![Module 8 — The DeFi Operating System](../assets/modules/module-08.png)

*Outcome: a written portfolio plan with risk buckets, limits and an emergency plan.*
*Stage 4 · Strategist. Source: ATLAS "DeFi & On-Chain" ch. 38–40, 42. Lesson 8.3 (the 25-strategy library) is in `03-defi-strategy-mastery.md`. Educational content only. Not financial advice. Figures are illustrative.*

---

## Lesson 8.1 — DeFi portfolio construction *(ch. 38)*

### Objective
Split capital into risk buckets with caps, so no single failure can sink the portfolio.

### Explanation
- **Buckets:** liquidity reserve · core (simple, durable) · productive (LP, vaults, carry) · speculative (new, points, experiments).
- **Concentration caps:** per protocol, per chain, per stablecoin issuer, per bridge.
- **Genuine diversification:** two front ends on the same protocol, or two stablecoins with the same backing, are one risk, not two.
- **Rebalancing rules:** thresholds that trigger moving money between buckets.

### Worked example — a $100,000 DeFi book (illustrative)
| Bucket | Share | Example holdings | Cap per protocol |
|---|---|---|---|
| Reserve | 15% | Stablecoins split across 2 issuers, instant access | n/a |
| Core | 45% | Blue-chip stable lending (2 protocols), ETH staking | 20% |
| Productive | 30% | Wide concentrated LP, a vault, a PT | 10% |
| Speculative | ≤10% | Points, new protocols | 5% |

Rebalance when any bucket drifts more than 5 points from target, or after any incident.

### Checklist
- [ ] Buckets and targets written
- [ ] Caps per protocol, chain, issuer, bridge written
- [ ] Rebalancing rule written

### Quiz
<details><summary>1. Two stablecoins backed by the same collateral: diversified?</summary>No. They share one failure point.</details>
<details><summary>2. Why keep a reserve bucket?</summary>To defend debt, meet needs and redeploy without forced selling.</details>
<details><summary>3. When should you rebalance?</summary>When buckets drift past the threshold, or after an incident.</details>

---

## Lesson 8.2 — The DeFi risk framework *(ch. 39)*

### Objective
Keep a risk register that scores every position's risks and names the response.

### Explanation
The eight risk surfaces: **smart-contract · economic · oracle · liquidity ·
governance · bridge/chain · counterparty · user-operation.**
Score each for **likelihood (1–5) × impact (1–5)**. Anything ≥ 15 needs a
mitigation or an exit; anything ≥ 20 shouldn't be held.

### Worked example — one register row
| Position | Risk | L | I | Score | Response |
|---|---|---|---|---|---|
| USDC lending, Protocol Y | Oracle on one collateral is thin | 3 | 4 | 12 | Cap 10%, alert on governance changes |
| LST loop | Rate spike above break-even | 3 | 3 | 9 | Alert at 4.5% borrow; unwind rule |
| Bridged stablecoin on new L2 | Bridge exploit | 2 | 5 | 10 | Canonical bridge; cap 5% |
| New farm | Contract bug (unaudited upgrade) | 4 | 5 | **20** | **Don't hold** |

### Checklist
- [ ] Register covers every position and all eight surfaces
- [ ] Scores ≥ 15 have a mitigation or exit
- [ ] Reviewed monthly and after incidents

### Quiz
<details><summary>1. How is a risk scored?</summary>Likelihood × impact, each 1–5.</details>
<details><summary>2. What's a user-operation risk?</summary>Your own mistakes: wrong network, bad signature, lost keys.</details>
<details><summary>3. Score 20. Action?</summary>Don't hold it.</details>

---

## Lesson 8.3 — Strategy library

The full strategy library (25 strategies in 6 levels, each with its profit
engine, maths, execution, kill rules and failure modes) is **Lesson 8.3:
DeFi Strategy Mastery** (`03-defi-strategy-mastery.md`).

---

## Lesson 8.4 — The operating playbook: deploy, monitor, respond, review *(ch. 42)*

### Objective
Run every position through the same four-phase routine.

### Explanation
1. **Deploy:** due diligence done · before-signing checklist · test amount · journal row (protocol, chain, contracts, amount, entry, thesis, kill rules, approvals).
2. **Monitor:** daily HF/pegs/ranges/incidents; weekly P&L vs benchmark, harvest, revoke; monthly register review.
3. **Respond:** pre-written actions for each trigger (see Module 11.5 for incidents).
4. **Review:** net return after all costs vs benchmark; simplify anything you can't explain in one sentence.

### Worked example — a journal row
| Field | Entry |
|---|---|
| Position | USDC supply, Protocol Y, Arbitrum |
| Amount / date | $10,000 · 2026-09-01 |
| Thesis | ~5% from real borrow demand |
| Kill rules | Utilisation > 95% for 48h; oracle or collateral change; any incident |
| Approvals | USDC → Protocol Y pool, limited to $10,000 |
| Weekly | Interest earned, utilisation, governance notes |

### Checklist
- [ ] Journal row for every position
- [ ] Daily / weekly / monthly routine in the calendar
- [ ] Response actions written per trigger

### Quiz
<details><summary>1. The four phases?</summary>Deploy, monitor, respond, review.</details>
<details><summary>2. What goes in a journal row?</summary>Position, amount, date, thesis, kill rules, approvals and ongoing results.</details>
<details><summary>3. What to do with a strategy you can't explain simply?</summary>Simplify it or exit.</details>

---

### Module 8 practical
Write your portfolio plan: buckets and caps (8.1), risk register (8.2), your
chosen strategies from 8.3 with kill rules, and your operating calendar (8.4).
