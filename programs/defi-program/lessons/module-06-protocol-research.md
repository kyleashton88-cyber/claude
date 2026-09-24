# Module 6 — Protocol Research

![Module 6 — Protocol Research](../assets/modules/module-06.png)

*Outcome: complete a full due-diligence file on a real protocol.*
*Stage 3 · Analyst. Source: ATLAS "DeFi & On-Chain" ch. 24–26, 41. Educational content only. Not financial advice.*

![The 6-step research loop](../assets/diagrams/research-loop.png)

---

## Lesson 6.0 — Mastery Starter

*New to this topic? Start here. It takes about 10 minutes and gets you from zero to ready for this module.*

### The 60-second version
Before trusting a protocol with money, a professional researches it the same way every time: what it does, where its money comes from, what it depends on, whether it's solvent, what the evidence says, and how to get out.

### Words you'll need
| Term | Meaning |
|---|---|
| Due diligence | structured research before investing |
| TVL | total value deposited in a protocol |
| FDV | token price × maximum supply |
| Governance | how holders vote on changes |
| Thesis | what must be true for the position to work |

### Before you start
- [ ] Modules 0–5

### Your first safe step
Pick a protocol you've heard of and write one sentence for each of the six research steps, even if it's "don't know yet".

### The mastery ladder
| Level | You can… |
|---|---|
| **Beginner** | Completes the six-step loop with sources |
| **Practitioner** | Reads tokenomics and governance and writes a thesis with invalidation |
| **Master** | Spots failure patterns early and writes verdicts others can act on |

### You've mastered this module when…
…your due-diligence file ends in a verdict with size, conditions and an exit.

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

## Lesson 6.5 — Case studies: how DeFi failures happened *(new)*

### Objective
Learn the patterns behind major failures so you recognise them early.

### Explanation — seven failures, seven patterns
| Case | What broke | Pattern | Warning signs |
|---|---|---|---|
| **Black Thursday, March 2020** (Maker) | ETH crashed; congested network and failing keeper bots let some collateral auctions clear at 0 DAI bids (~$8M lost) | Liquidation mechanism failure under stress | Auctions relying on keepers during congestion; no minimum bid |
| **TerraUSD (UST), May 2022** | Algorithmic stablecoin lost its peg and collapsed | Reflexive design: confidence was the collateral | Yield (~20%) far above any real cash flow; peg defended by a sister token |
| **Ronin bridge, March 2022** (~$600M) | Attackers got 5 of 9 validator keys | Weak bridge trust model | Small signer set; keys concentrated |
| **Mango Markets, Oct 2022** (~$110M) | Collateral price pumped on thin markets, then borrowed against | Oracle manipulation | Thin-market collateral valued at spot |
| **FTX, Nov 2022** | Exchange used customer funds | Custodial (CeFi) counterparty failure | Opaque reserves; "not your keys" |
| **Euler Finance, March 2023** (~$197M, later largely returned) | Logic flaw in a lending function | Contract bug missed by audits | Complex new function added after earlier audits |
| **Curve pools, July 2023** | Reentrancy guard broken by a compiler bug | Toolchain risk | Rare. Shows audited code can fail from below |

Figures are approximate, from public reporting.

### Worked example
Using the table: a new stablecoin offers 18% "sustainable" yield, backed by its own
governance token. That's the UST pattern: reflexive collateral and yield with no
matching cash flow. Rating: High. Verdict: don't hold.

### Checklist
- [ ] For every position, I've asked which failure pattern it resembles
- [ ] My register (8.2) includes these seven patterns

### Quiz
<details><summary>1. What pattern did Mango Markets show?</summary>Oracle manipulation of thin-market collateral.</details>
<details><summary>2. What did FTX show DeFi users?</summary>Custodial counterparty risk: "not your keys, not your coins".</details>
<details><summary>3. UST's main warning sign?</summary>High yield with no matching real cash flow, backed by a reflexive sister token.</details>

---

## Lesson 6.6 — Vote-escrow tokenomics, bribes and governance markets *(expert)*

### Objective
Understand vote-escrow ("ve") systems and bribe markets, a major source of DeFi yield and power.

### Explanation
- **Vote-escrow:** you lock a governance token for a period (often up to 4 years) and get **ve-tokens** with voting power that decays as the unlock approaches. Longer lock = more power.
- **Gauges:** ve-holders vote on which pools receive the protocol's token **emissions**. Emissions attract liquidity, so votes are valuable.
- **Bribes / voting incentives:** protocols that want liquidity pay ve-holders to vote for their pool. Voters earn this as yield (plus a share of fees in some designs).
- **Liquid lockers / meta-governance:** protocols that lock on your behalf and give you a tradable token. It's liquid, but it can trade at a discount, and it adds a layer of risk.
- **Risks:** long locks (you can't sell), the token's price over the lock, emissions diluting holders, and governance capture.

### Worked example
$10,000 of a ve-token earning ~15% APR in bribes ≈ **$1,500/yr**, paid in various tokens.
But the underlying is locked for 4 years: if the token falls 60%, the position is worth
$4,000 plus the bribes collected. A liquid-locker version lets you exit, but it traded at a
20% discount during the last sell-off. Price the lock, not just the APR.

### Checklist
- [ ] Lock length and decay understood
- [ ] Bribe income valued at a realistic sale price
- [ ] Liquid-locker discount history checked before using one

### Quiz
<details><summary>1. What do ve-holders vote on?</summary>Which pools receive emissions (gauge weights) and other governance decisions.</details>
<details><summary>2. Why do protocols pay bribes?</summary>Votes direct emissions to their pools, attracting liquidity.</details>
<details><summary>3. Main cost of a 4-year lock?</summary>You can't sell during the lock, whatever the token's price does.</details>

---

## Lesson 6.7 — Valuing DeFi protocols: fees, revenue, earnings and multiples *(expert)*

### Objective
Compare protocols on their economics, not their narratives.

### Explanation
- **Fees:** everything users pay. **Revenue:** the part that goes to the protocol or token holders (the rest goes to LPs/lenders). **Earnings:** revenue minus token incentives paid out.
- **Multiples:** price-to-fees (P/F), price-to-sales (P/S, on revenue), price-to-earnings (P/E). Use **FDV** as well as market cap, since unlocks will arrive (6.2).
- **Quality checks:** is revenue growing without rising incentives? Is it concentrated in one pool or chain? Does it survive a bear market? Does the token actually receive it (value capture)?
- Multiples compare protocols; they don't set a "right" price.

### Worked example
FDV **$2B**, annual revenue **$100M**, token incentives **$60M** → earnings **$40M**.
P/S (FDV) = **20×**; P/E (FDV) = **50×**. A rival with the same revenue but no incentives
has earnings of $100M: at the same FDV its P/E is 20×. Same revenue, very different economics.

### Checklist
- [ ] Fees, revenue and earnings separated, with sources
- [ ] Multiples on FDV and market cap
- [ ] Revenue quality and value capture assessed

### Quiz
<details><summary>1. Revenue vs earnings?</summary>Earnings are revenue minus token incentives (and other costs).</details>
<details><summary>2. Why use FDV in multiples?</summary>Future unlocks will add supply; FDV shows the fully diluted price.</details>
<details><summary>3. FDV $600M, earnings $20M. P/E?</summary>30×.</details>

---

### Module 6 practical: analyst capstone part 1
Complete a full due-diligence file on one real protocol using lessons 6.1–6.4
and the Notion tracker. (Submitted with Module 7 as the **analyst capstone**.)
