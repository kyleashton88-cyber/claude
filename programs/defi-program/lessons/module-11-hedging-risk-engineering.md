# Module 11 — Hedging & Risk Engineering

![Module 11 — Hedging & Risk Engineering](../assets/modules/module-11.png)

*Outcome: hedge the risks you don't want, stress-test the portfolio, and have an incident plan ready.*
*Stage 4 · Strategist. Prerequisites: Modules 1–10. Educational content only. Not financial advice. Figures are illustrative.*

---

## Lesson 11.1 — Hedging price exposure with perps and options

### Objective
Reduce price exposure deliberately, and know what each hedge costs.

### Explanation
- **Perp hedge:** short a perpetual future against spot you hold. Cheap to open;
  pays or earns funding; needs margin; the hedge ratio is your choice.
- **Protective put:** buy the right to sell at a strike. Costs a premium, and your loss is capped below the strike.
- **Collar:** buy a put and sell a call to pay for it. Cheaper protection in exchange for capped upside.
- A hedge **costs** something (premium, funding, capped upside). Hedge the risk you can't afford, not every risk.

### Worked example
You hold **10 ETH at $3,000** ($30,000).
- **50% perp hedge** (short 5 ETH): ETH falls 30% → spot −$9,000, short +$4,500 → **−$4,500** (−15%) instead of −30%.
- **Protective put:** buy a 30-day $2,700 put for 2% ($60/ETH). Worst case per ETH = $300 drop to the strike + $60 premium = **$360 (12%)**, however far ETH falls in that month.

### Checklist
- [ ] Hedge target stated (which risk, how much)
- [ ] Cost computed (premium, funding, capped upside)
- [ ] Margin buffer for perp hedges set

### Quiz
<details><summary>1. What does a protective put cap?</summary>Your loss below the strike, for the option's term, at the cost of the premium.</details>
<details><summary>2. What does a collar trade away?</summary>Upside above the call strike, to pay for the put.</details>
<details><summary>3. 20 ETH, 25% perp hedge, ETH −40%. Net loss if ETH was $3,000?</summary>Spot −$24,000, short +$6,000 → −$18,000.</details>

---

## Lesson 11.2 — Depeg, protocol and smart-contract cover

### Objective
Evaluate on-chain cover products as insurance: what they pay, when, and what they don't.

### Explanation
Cover protocols sell protection against defined events (a protocol hack, a
depeg beyond a threshold). Read: **what's covered** (exact wording), **exclusions**,
**claim process** (who decides, how long), **payout asset**, and the cover
provider's **own** solvency and contract risk.

### Worked example
Cover $50,000 in a lending protocol at 2.5%/yr = **$1,250/yr**. If your
risk-adjusted yield there is 4.5%, cover takes more than half of it. Worth it
for a large, concentrated position; often not for a small, diversified one.

### Checklist
- [ ] Cover wording and exclusions read
- [ ] Claim process and payout asset understood
- [ ] Cost compared with the yield it protects

### Quiz
<details><summary>1. Name two things to check in cover terms.</summary>Any two: covered events, exclusions, claim process, payout asset, provider solvency.</details>
<details><summary>2. Cover costs 3%/yr on a 5% yield. Net?</summary>About 2%.</details>
<details><summary>3. Does cover remove all risk?</summary>No. The cover provider has its own claim, solvency and contract risks.</details>

---

## Lesson 11.3 — Liquidation protection: buffers, alerts and automated deleveraging

### Objective
Make liquidation practically impossible with buffers, alerts and pre-computed repayment.

### Explanation
Three layers: **buffer** (HF ≥ 2–2.5 at entry) → **alerts** (HF 2.0 and 1.7,
Module 14.1) → **action** (repay, add collateral, or automated deleveraging tools
that repay debt when HF crosses a trigger; these add their own contract and permission risk).
**Pre-compute** the repayment needed to restore your target HF:
`debt to keep = collateral value × LT ÷ target HF`.

### Worked example
10 ETH falls to $2,400 → collateral $24,000, LT 0.8, debt $12,000 → **HF 1.6**.
To restore HF 2.5: debt must be 24,000 × 0.8 ÷ 2.5 = $7,680 → **repay $4,320** from the reserve.

### Checklist
- [ ] Alerts at HF 2.0 and 1.7
- [ ] Repayment to restore target HF pre-computed
- [ ] Reserve covers that repayment

### Quiz
<details><summary>1. Collateral $40,000, LT 0.8, target HF 2. Max debt?</summary>$16,000.</details>
<details><summary>2. What do automated deleveraging tools add?</summary>Their own contract and permission risk.</details>
<details><summary>3. Why pre-compute the repayment?</summary>So you act immediately, not while calculating under stress.</details>

---

## Lesson 11.4 — Stress-testing a portfolio

### Objective
Run standard shock scenarios on your book and fix what fails before markets test it.

### Explanation
Scenarios every operator runs: **crypto −50% in a day** · **a stablecoin depegs 10%**
· **borrow rates spike to 20%** · **your largest protocol is hacked** · **your main L2 halts for 48h**.
For each: loss, liquidations, liquidity, and whether the payout policy survives.

### Worked example — $200,000 book
Holdings: ETH spot $60k · LST collateral $60k with $12k debt · stable lending $50k
($25k each in two protocols) · ETH/USDC LP $20k · PT stable $10k.

| Scenario | Impact | Passes? |
|---|---|---|
| ETH −50% | Spot −$30k; collateral −$30k (HF 4.0 → 2.0, no liquidation); LP $20k → $14.1k (−$5.9k) → **−$65.9k (−32.9%)** | Survives, but the payout must fall |
| One stablecoin −10% | −$2.5k on $25k | Yes |
| Borrow rate 20% | Interest on $12k rises from ~$600 to $2,400/yr | Yes: covered by reserve |
| One lending protocol hacked (total loss) | −$25k (−12.5%) | Survives; cap was 12.5% |
| L2 halted 48h | Positions frozen; the reserve on another chain covers needs | Yes, *if* the reserve isn't on the same L2 |

### Checklist
- [ ] Five scenarios run on the current book
- [ ] Every "fail" has a fix (smaller cap, bigger buffer, move the reserve)
- [ ] Re-run quarterly and after big changes

### Quiz
<details><summary>1. Why did the collateral position survive −50%?</summary>It started at HF 4.0; halving the price took it to 2.0.</details>
<details><summary>2. What does the L2-halt scenario test?</summary>Whether your liquidity depends on a single chain.</details>
<details><summary>3. What's the output of a stress test?</summary>Fixes: smaller caps, bigger buffers, better-placed reserves.</details>

---

## Lesson 11.5 — Incident response: the first 60 minutes

### Objective
Know exactly what to do when a protocol you use is exploited, a stablecoin depegs, or your wallet is compromised.

### Explanation — the 60-minute playbook
**0–5 min: Verify.** Official channels only (bookmarked X/Discord/status page,
security firms). Don't click links in DMs, and don't sign anything "to protect funds".
**5–20 min: Contain.**
- *Protocol exploit:* withdraw if still possible and safe; revoke approvals to affected contracts.
- *Depeg:* follow your written peg rule (e.g. exit below 0.99 for X hours); don't panic-sell far below it on a thin book.
- *Wallet compromise:* move remaining assets to a **fresh** wallet (new seed, clean device); revoke approvals; assume the old seed is burned.

**20–60 min: Stabilise.** Check HFs across all positions (prices may be
moving), top up from the reserve, and journal every action with timestamps.
**After: Review.** What was the signal, what worked, and what changes in the caps and the register?

### Worked example
A lending protocol you use announces a paused market after an exploit. You
verify on its bookmarked status page, see withdrawals still work on unaffected
markets, withdraw your USDC, revoke the pool approval, check your other HFs,
and journal it. Total time: 25 minutes. Loss: none. Because the steps were written in advance.

### Checklist
- [ ] Incident playbook printed/saved offline
- [ ] Official channels bookmarked for every protocol I use
- [ ] A clean "fresh wallet" procedure written

### Quiz
<details><summary>1. First thing to do in an incident?</summary>Verify through official, bookmarked channels.</details>
<details><summary>2. Someone offers a link to "rescue your funds". What do you do?</summary>Ignore it. It's a common scam during incidents.</details>
<details><summary>3. Wallet compromised: can you keep using the seed?</summary>No. Move to a fresh wallet with a new seed; the old one is burned.</details>

---

### Module 11 practical
1. Price one hedge (perp and put) for your largest price exposure.
2. Run the five stress scenarios on your book and write the fixes.
3. Write and save your incident playbook, with bookmarks.
