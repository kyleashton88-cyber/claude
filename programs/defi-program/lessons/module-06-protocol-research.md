# Module 6 — Protocol Research

![Module 6 — Protocol Research](../assets/modules/module-06.png)

*Outcome: complete a full due-diligence file on a real protocol.*
*Stage 3 · Analyst. Source: ATLAS "DeFi & On-Chain" ch. 24–26, 41. Educational content only. Not financial advice.*

![The 6-step research loop](../assets/diagrams/research-loop.png)

---

## Lesson 6.1 — Protocol due diligence *(ch. 24)*

### Objective
Run the 6-step research loop on a protocol and reach a written verdict.

### Explanation
1. **Mechanism:** what the contracts do; users, assets, incentives.
2. **Cash flow:** real fees and interest vs emissions.
3. **Dependencies:** oracles, bridges, admin keys, stablecoins, other protocols.
4. **Solvency:** collateral quality, liquidation design, bad-debt paths.
5. **Evidence:** explorers, audits, governance, independent data.
6. **Exit:** exact unwind, gas, slippage, approvals to revoke.

Log it in the **DeFi Protocol Due Diligence Tracker** (Notion) and tick a box
only when the step is **evidenced**, not assumed.

### Worked example (template verdict)
*"Protocol Y (lending, Arbitrum). Risk: Medium. Fees are real (borrow demand
$2M/yr), but one collateral uses a thin-market oracle and upgrades have a
24h timelock. Verdict: supply stablecoins only, cap at 10% of the DeFi book,
alert on queued upgrades."*

### Checklist
- [ ] All six steps written with sources
- [ ] Risk rating = worst material risk, not an average
- [ ] Verdict states size, conditions and exit

### Quiz
<details><summary>1. Why is the rating the worst risk, not the average?</summary>One failure point is enough to lose the position.</details>
<details><summary>2. Which step prevents getting stuck?</summary>Step 6: Exit.</details>
<details><summary>3. When do you tick a tracker box?</summary>Only when there's evidence for it.</details>

---

## Lesson 6.2 — Tokenomics: supply, unlocks, FDV, value capture *(ch. 25)*

### Objective
Read a token's supply schedule and judge whether protocol success reaches the token.

### Explanation
- **Circulating supply:** tokens tradable now. **Max/total supply:** all that will exist.
- **Market cap** = price × circulating. **FDV** (fully diluted valuation) = price × max supply.
- **Unlocks/vesting:** team and investor tokens released on a schedule; new supply that may be sold.
- **Emissions:** ongoing new tokens (rewards).
- **Value capture:** does protocol revenue actually reach token holders (fee share, buybacks), and how is it enforced?

### Worked example
Price $2, circulating 100M, max 1B: market cap **$200M**, FDV **$2B**.
Next month 50M unlock: circulating supply rises **50%**. Unless demand grows
to match, that's heavy selling pressure. A low market cap with a huge FDV is a warning.

### Checklist
- [ ] Market cap vs FDV compared
- [ ] Next 12 months of unlocks listed
- [ ] Value-capture mechanism identified (or "none")

### Quiz
<details><summary>1. Price $5, circulating 20M, max 100M. FDV?</summary>$500M.</details>
<details><summary>2. Why do unlocks matter?</summary>They add supply that recipients may sell.</details>
<details><summary>3. What is value capture?</summary>An enforceable way protocol success benefits the token.</details>

---

## Lesson 6.3 — Governance & DAOs *(ch. 26)*

### Objective
Read how a protocol is controlled and spot governance risk before it hits your position.

### Explanation
- **Governance tokens** vote on parameters, upgrades and treasury.
- **Proposal lifecycle:** forum discussion → vote → timelock → execution.
- **Delegation** lets holders assign votes to representatives.
- **Risks:** low turnout, concentrated voting power, borrowed votes, rushed proposals, weak timelocks.

### Worked example
A proposal to raise a collateral's LTV passes with 8% turnout, 70% of it from
three wallets. Lenders now carry more bad-debt risk, decided by a few voters.
**Track governance for markets you're in.** It changes your risk without you doing anything.

### Checklist
- [ ] Governance forum/alerts followed for protocols I use
- [ ] Voting concentration checked
- [ ] Timelock length known

### Quiz
<details><summary>1. What's a governance attack?</summary>Using concentrated or borrowed voting power to pass harmful changes.</details>
<details><summary>2. Why follow governance as a user?</summary>Parameter changes alter your risk.</details>
<details><summary>3. Order of the proposal lifecycle?</summary>Discussion → vote → timelock → execution.</details>

---

## Lesson 6.4 — The on-chain research workflow *(ch. 41)*

### Objective
Turn research into a written thesis with invalidation and monitoring.

### Explanation
**Question first** → primary sources (docs, contracts, governance) → economic
reality (fees vs incentives) → cross-check with independent data → **thesis**:
what must be true, what would prove it wrong, what to monitor.

### Worked example (thesis template)
*"Thesis: stablecoin lending on Protocol Z earns ~5% from real borrow demand.
Must be true: utilisation 60–85%, oracle unchanged, no new risky collateral.
Invalidation: utilisation > 95% for 48h, a governance change adding thin
collateral, or an incident. Monitor: weekly utilisation, governance feed."*

### Checklist
- [ ] Research question written first
- [ ] Thesis, invalidation and monitoring written
- [ ] Evidence from at least two independent sources

### Quiz
<details><summary>1. Why start with a question?</summary>To avoid hunting for data that confirms what you already believe.</details>
<details><summary>2. What makes a thesis useful?</summary>A clear invalidation you'll act on.</details>
<details><summary>3. What should monitoring track?</summary>Only the metrics that would change the thesis.</details>

---

### Module 6 practical: analyst capstone part 1
Complete a full due-diligence file on one real protocol using lessons 6.1–6.4
and the Notion tracker. (Submitted with Module 7 as the **analyst capstone**.)
