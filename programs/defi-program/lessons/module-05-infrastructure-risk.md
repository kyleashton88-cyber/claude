# Module 5 — Infrastructure Risk

![Module 5 — Infrastructure Risk](../assets/modules/module-05.png)

*Outcome: map every bridge, oracle, L2 and contract a position depends on.*
*Stage 2 · Practitioner. Source: ATLAS "DeFi & On-Chain" ch. 19–23. Educational content only. Not financial advice.*

**Why this module matters:** most of DeFi's largest losses came from the
plumbing (bridges, oracles, admin keys, contract bugs), not from price moves.

---

## Lesson 5.1 — Bridges and trust assumptions *(ch. 19)*

### Objective
Choose bridge routes by their trust model, and size bridge exposure accordingly.

### Explanation
Bridges move value between chains:
- **Canonical bridges:** the chain's official route (e.g. a rollup's native bridge). Usually the strongest security, sometimes slower.
- **Lock-and-mint:** assets locked on chain A, a wrapped copy minted on chain B. The wrapped copy is only as good as the lock.
- **Liquidity networks:** market makers pay you out on the other side. Fast; you rely on their contracts and liquidity.
- **Trust model:** who can approve a transfer: a multisig of a few keys, a validator set, a light client, or fraud/validity proofs? Fewer, weaker signers = more risk.

Bridges hold large pools of value, which makes them prime targets.

### Worked example
Moving $50,000 to a Layer 2: use the canonical route for the bulk (even if
slower), a reputable fast bridge for a small, time-sensitive amount, and send a
test first. Never leave large balances as a **wrapped** asset from a weak bridge.

### Checklist
- [ ] Trust model of every bridge I use written down
- [ ] Canonical route preferred for size
- [ ] Wrapped-asset exposure capped

### Quiz
<details><summary>1. What backs a lock-and-mint wrapped token?</summary>The locked assets on the source chain, and the bridge's security.</details>
<details><summary>2. Why are bridges frequent hack targets?</summary>They concentrate large amounts of value behind complex, cross-chain logic.</details>
<details><summary>3. Fast bridge or canonical for $50k?</summary>Canonical for the bulk; fast only for small, urgent amounts.</details>

---

## Lesson 5.2 — Layer 2s, sequencers & withdrawal paths *(ch. 20)*

### Objective
Understand how your L2 settles, who orders your transactions, and how you'd exit.

### Explanation
- **Rollups** execute transactions off Ethereum and post data or proofs back to it.
- **Optimistic rollups** assume transactions are valid unless challenged. Native withdrawals to Ethereum wait out a **challenge window** (about 7 days on major optimistic rollups).
- **ZK rollups** post validity proofs, so native withdrawals can be faster.
- **Sequencer:** the operator that orders transactions. Often a single operator today; if it goes down, the chain may pause.
- **Escape hatches:** most rollups let you force a withdrawal via Ethereum if the sequencer censors you. Know if yours does.

### Worked example
You hold $20,000 on an optimistic rollup and need it on Ethereum. Native bridge:
safest, ~7 days. Fast bridge: minutes, for a fee, relying on its liquidity.
**Plan your liquidity ladder (Module 12.4) around the slow path.**

### Checklist
- [ ] Rollup type and withdrawal time known for each L2 I use
- [ ] Sequencer setup and escape hatch known
- [ ] Liquidity plan assumes the slow path

### Quiz
<details><summary>1. Why do optimistic rollup withdrawals take ~7 days?</summary>The challenge window lets anyone dispute an invalid state before it's final.</details>
<details><summary>2. What happens if a single sequencer goes down?</summary>The L2 may pause transactions until it recovers.</details>
<details><summary>3. What's an escape hatch?</summary>A way to force a transaction or withdrawal via the base chain if the sequencer censors you.</details>

---

## Lesson 5.3 — Oracles, TWAPs & manipulation *(ch. 21)*

### Objective
Know which price feed secures each position, and how it can fail.

### Explanation
Smart contracts can't see market prices; **oracles** bring them in. Lending
markets liquidate based on the oracle price, not the price you see on screen.
- **Push oracles:** a network updates prices on a schedule or when price moves past a **deviation threshold**.
- **Pull oracles:** prices are fetched and verified when a transaction needs them.
- **TWAP** (time-weighted average price) smooths manipulation, but **lags** fast moves.
- **Failures:** stale prices in outages, manipulation of thin markets, misconfigured feeds.

### Worked example
Your collateral is priced by a 30-minute TWAP. The market drops 10% in 5
minutes. Your screen shows −10%; the oracle shows maybe −2%. You feel liquidated
and aren't yet, **but you also can't rely on the lag**: it catches up.
Conversely, a thinly traded collateral token can be pushed up and borrowed against by an attacker.

### Checklist
- [ ] Oracle type and source known for each collateral
- [ ] Thin-market collateral avoided or capped
- [ ] Buffers sized for oracle catch-up

### Quiz
<details><summary>1. Which price triggers a DeFi liquidation?</summary>The oracle price used by the protocol.</details>
<details><summary>2. What's the trade-off of a TWAP?</summary>Harder to manipulate, but it lags fast moves.</details>
<details><summary>3. Why is thin-market collateral dangerous for lenders?</summary>Its price can be manipulated to borrow more than it's really worth.</details>

---

## Lesson 5.4 — Smart contracts: state, proxies, admin keys *(ch. 22)*

### Objective
Read who controls a contract and whether its code can change after you deposit.

### Explanation
- **State:** what a contract stores (balances, parameters). **Functions** change it; **events** log what happened.
- **Verified source:** the code published on the explorer matches what's deployed. That's good, not proof of safety.
- **Proxy / upgradeable contracts:** the address you use stays the same, but the logic behind it can be swapped. Whoever controls upgrades controls your funds' rules.
- **Admin keys and roles:** owners, guardians, multisigs; can they pause, upgrade or move funds?
- **Timelocks:** a delay between an approved change and it taking effect. Your window to exit.

### Worked example
On a block explorer, the vault you use shows "Proxy", with the upgrade admin a
**3-of-5 multisig** behind a **48-hour timelock**. That means no instant rug by
one key, and 48 hours to exit if a change you don't like is queued.
A 1-of-1 admin with no timelock is a red flag.

### Checklist
- [ ] Proxy or not, and who can upgrade
- [ ] Admin roles and multisig threshold known
- [ ] Timelock length known; alert on queued changes for large positions

### Quiz
<details><summary>1. Does verified source code mean safe?</summary>No. It means the published code matches the deployed code.</details>
<details><summary>2. Why does a timelock matter to users?</summary>It gives time to see and exit before a change takes effect.</details>
<details><summary>3. Red flag in admin setup?</summary>A single key that can upgrade or move funds instantly.</details>

---

## Lesson 5.5 — Smart-contract risk & what audits don't prove *(ch. 23)*

### Objective
Weigh contract risk honestly, and read an audit for what it actually covers.

### Explanation
- **Common failure types:** logic bugs, **reentrancy** (a contract is called back before it updates its state), broken access control, and **economic exploits** (correct code, exploitable incentives or oracles).
- **Audits** review specific code at a specific time. Check the **scope** (which contracts), **date** (before later changes?), **severity of findings** and whether they were **fixed**.
- **Bug bounties** pay hackers to report instead of exploit. A large, active bounty is a good sign.
- **Time and value at risk:** code that has safely held large value for years has survived more real attacks.

### Worked example
Protocol X: two audits, but the latest upgrade (last month) isn't in either
scope; bounty $50k; TVL $400M. The newest code is unaudited and the bounty is
small relative to the value. Size down, or wait.

### Checklist
- [ ] Audit scope matches deployed code; date after last upgrade
- [ ] Critical/high findings resolved
- [ ] Bug bounty size relative to TVL checked

### Quiz
<details><summary>1. What does an audit not prove?</summary>That the code (or later changes, or economic design) is safe.</details>
<details><summary>2. What is reentrancy?</summary>A contract being called back before it finishes updating its state, letting an attacker repeat actions.</details>
<details><summary>3. Why check audit dates?</summary>Code changed after the audit wasn't reviewed.</details>

---

### Module 5 practical
Pick one position you hold or plan. Draw its dependency map: chain, bridge,
oracle, contracts, admin/timelock, audits. Mark each link Low/Medium/High risk.
