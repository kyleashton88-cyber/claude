---
name: defi-due-diligence
description: Research a DeFi protocol or position with the ATLAS 6-step risk loop (Mechanism → Cash Flow → Dependencies → Solvency → Evidence → Exit), produce a risk rating and verdict, and log it to the Notion "DeFi Protocol Due Diligence Tracker". Use when the user asks whether a protocol, pool, vault, LST, bridge or yield strategy is safe, wants a DeFi lesson example, or needs a pre-transaction checklist.
---

# DeFi Due Diligence

Source: Notion → ATLAS → *DeFi & On-Chain (Complete Module)*. Operating
principle: **risk first**. Educational research only — never financial advice,
never a return forecast.

## The 6-step research loop

For each step, write findings and cite the source (docs, explorer link,
audit, governance post, data dashboard). Mark anything unverified as such.

1. **Mechanism** — what the protocol does at contract level: users, assets,
   state changes, incentives.
2. **Cash Flow** — split yield into real activity (trading fees, borrower
   interest, service fees) vs token emissions / temporary incentives.
3. **Dependencies** — map oracles, bridges, admin keys/multisigs, validators,
   stablecoins, governance, sequencers, third-party contracts.
4. **Solvency** — collateral quality, liquidation mechanics, liquidity depth,
   bad-debt pathways, concentration.
5. **Evidence** — verify claims via explorers, docs, audits (scope, date,
   unresolved findings), bug bounty, governance forums, independent data.
6. **Exit** — exact unwind path, gas needed, slippage limits, approvals to
   revoke, emergency triggers.

## Risk surfaces to score

Smart-contract · Economic · Oracle · Liquidity · Governance · Bridge/chain ·
Counterparty · User-operation. For each: Low / Medium / High + one-line reason.
Overall **Risk Rating** = the highest material surface, not an average.

## Output format

```
Protocol: <name>   Chain: <chain>   TVL: <$, source, date>
Risk Rating: Low | Medium | High
Verdict: <one sentence>

1. Mechanism — ...
2. Cash Flow — organic: ...  subsidised: ...
3. Dependencies — ...
4. Solvency — ...
5. Evidence — ... (links)
6. Exit — ...

Risk surfaces: table
Monitoring triggers: health factor / depeg / utilisation / governance / incident alerts
```

## Log to Notion (on user confirmation)

Database: **DeFi Protocol Due Diligence Tracker** (Worksheets section).
Properties: `Protocol` (title), `Chain`, `TVL` ($), `Risk Rating`
(Low/Medium/High), `Verdict`, and checkboxes `Mechanism Understood`,
`Dependency Map Complete`, `Contracts Verified`, `Audit Reviewed`,
`Exit Path Defined`. Tick a box only if that step was actually evidenced.

## Before-signing checklist (every transaction)

- [ ] Chain confirmed correct
- [ ] Contract address verified through an authoritative source
- [ ] Token and amount double-checked
- [ ] Spender/allowance reviewed (prefer limited approvals)
- [ ] Slippage set deliberately
- [ ] Gas/fee estimate reviewed
- [ ] Intended outcome stated in one sentence before signing
- [ ] Small test transaction for unfamiliar routes/bridges

## Guardrails

- Never ask for seed phrases, private keys or wallet secrets.
- Never present headline APY without its risk source.
- If the unwind can't be explained, the verdict is "do not deploy yet".
