# DeFi Program — Offer & Curriculum (DRAFT for approval)

Status: **draft, nothing created on Whop yet.** Items marked **DECIDE** need
your call before phase 3 (Whop setup).

## Decisions so far (2026-09-24)
| Item | Decision |
|---|---|
| Name | **On-Chain Operator Program** |
| Format | **Two tiers:** self-paced course + a higher tier with live sessions |
| Sales path | **Application → call → checkout** |
| Audience | **Everyone at once:** GBB customers, Elite Intel members and cold ad traffic from launch |
| Price | **Course $15,000 one-time** · live tier priced higher (TBD) |
| Refund policy | Open |
| Starter tier / GBB pricing conflict | Open |
| 9-module structure | Assumed OK unless you say otherwise |

**What $15,000 changes (recommendations, your call):**
- It becomes the top of the ladder (above Grid Bot Elite at $2,497), so it
  needs a **high-ticket sales path**: cold traffic → application → call →
  checkout, not straight-to-checkout ads. `gbb-new-lead` scoring (capital
  20k+ = 4) becomes the qualifier.
- Buyers at this price expect access to you: the live tier (calls, reviews,
  capstone feedback) carries most of the value. The course alone is hard to
  justify at $15k.
- High-ticket crypto education attracts consumer-protection scrutiny. Keep
  every page and call script free of income/return claims, and put terms,
  refund policy and "educational, not financial advice" at checkout.

Built from: Notion → ATLAS → *DeFi & On-Chain (Complete Module)* (42 chapters,
16 strategy frameworks, 20 on-chain metrics) and the existing Grid Bot Builder
offer stack.

---

## Phase 1 — Offer

### Positioning
Grid Bot Builder automates trading **on exchanges**. The DeFi program teaches
people to operate **on-chain** safely: research a protocol, size a position,
know the exit. Your module already has a strong line to lead with:

> **"If you can't explain the unwind, you don't understand the position yet."**

**Promise (skills, not returns):** *Research any DeFi protocol with a 6-step
risk loop, understand exactly where yield comes from, and never sign a
transaction you can't unwind.*

### Working name — DECIDE
| Option | Why |
|---|---|
| **DeFi Operator Blueprint** (recommended) | Matches "Grid Bot Building Blueprint" on Whop; "operator" = process, not hype |
| Risk-First DeFi | States the differentiator |
| On-Chain Operator Program | Neutral, broader |

### Who it's for — DECIDE
| Audience | Fit | How they arrive |
|---|---|---|
| **GBB customers** (recommended primary) | Already trust you, already think in systems/risk | Cross-sell email ~14 days after GBB onboarding |
| Elite Intel Community members | Warm, recurring, already reading intel briefs | In-community offer + LAUNCH-style code |
| Cold ad traffic | Largest pool, needs most education | Separate ad campaign → lead skill with `defi-lead` tag |

Recommendation: launch to GBB customers + Elite Intel members first (warm,
lower CAC, real feedback), open to cold traffic once conversion is proven.

### Format — DECIDE
- **Core (recommended):** self-paced Whop course (9 modules below) + worksheets
  (the two Notion trackers as templates) + quizzes + capstone.
- **Optional higher tier:** Core + live monthly DeFi Q&A / portfolio review.
  Your Calendly already has `vip-defi-consult` and `defi` links — are those
  for this program? (The GBB skills are told never to use them, so they're
  free for DeFi.)

### Pricing — DECIDE (proposal only)
Mirror GBB's one-time + 3-pay pattern, priced **below** GBB so it works as
a cross-sell rather than competing with it:

| Plan | Proposal | Reasoning |
|---|---|---|
| One-time | $497 | Half of GBB; education product, not software |
| 3-pay | 3 × $197 ($591) | ~19% payment-plan premium, in line with GBB's 20% (3 × $399 vs $997) |
| GBB customer price | $397 or bundle | Rewards the cross-sell |
| Higher tier (if live calls) | $997 | Only if you'll run the calls |

Refund policy — DECIDE: GBB has 30-day money-back on the software. For a
course, suggest **14 days, if under 30% of lessons completed**.

> Still open from before: `gbb ad performance` mentions a "Grid Bot Starter"
> (A$47–97) and GBB at A$497. Other skills say $997, no Starter. Which is
> current? It affects where DeFi sits in the ladder.

### Ladder after launch
```
Elite Intel Community ($67/mo) ──► Grid Bot Builder ($997) ──► Grid Bot Elite ($2,497)
            │                               │
            └──────────► On-Chain Operator Program ($15,000) ◄──┘
                         Module 9 cross-sells back into GBB
```

---

## Phase 2 — Curriculum

**Change from the skill's default:** I split "Research" (12 chapters) into
two modules, so it's **9 modules** instead of 8 and every module is 3–8
lessons. All 42 chapters are used exactly once.

Every lesson follows one template: **Objective → Explanation → Worked example
→ Checklist → 3 quiz questions.** A full sample lesson is in
`02-sample-lesson-amm-math.md`.

### Module 1 — Foundations & Safety *(6 lessons)*
Outcome: set up and use a wallet safely; know what can go irreversibly wrong.
| # | Lesson | ATLAS ch. |
|---|---|---|
| 1.1 | What DeFi is — and the risk-first mindset | 1 |
| 1.2 | How a transaction actually happens (gas, nonce, finality) | 2 |
| 1.3 | Wallets, keys, hardware & multisig | 3 |
| 1.4 | Tokens, approvals & allowances | 4 |
| 1.5 | Stablecoins and how they break | 5 |
| 1.6 | Scam defence: phishing, drainers, address poisoning | 36 |
Assets: before-signing checklist (ch. 42) introduced here and reused in every module.

### Module 2 — Trading On-Chain *(5 lessons)*
Outcome: execute a swap deliberately, understanding price impact and MEV.
| 2.1 | DEXs, aggregators & routing | 6 |
| 2.2 | AMM mathematics (x·y=k) — *sample lesson* | 7 |
| 2.3 | Providing liquidity | 8 |
| 2.4 | Impermanent loss & true LP P&L | 9 |
| 2.5 | MEV and how to protect your trades | 35 |
Assets: AMM flow diagram, 100 ETH / 300k USDC worked example, LP-vs-hold benchmark.

### Module 3 — Lending & Leverage *(4 lessons)*
Outcome: borrow against collateral with a buffer and a written defence plan.
| 3.1 | How lending markets work (utilisation, rate curves) | 10 |
| 3.2 | LTV, liquidation threshold & health factor | 11 |
| 3.3 | Liquidations and cascades | 12 |
| 3.4 | Borrowing strategies & looping | 13 |
Assets: liquidation feedback-loop diagram, Aave health-factor primary source.

### Module 4 — Yield *(6 lessons)*
Outcome: split any APY into organic vs subsidised, and name the risk being paid for.
| 4.1 | Yield farming: base yield vs emissions | 14 |
| 4.2 | Native staking | 15 |
| 4.3 | Liquid staking (LSTs) | 16 |
| 4.4 | Restaking & shared security | 17 |
| 4.5 | Vaults & yield optimisers | 18 |
| 4.6 | Airdrops & points — opportunity cost | 37 |

### Module 5 — Infrastructure Risk *(5 lessons)*
Outcome: map every bridge, oracle, L2 and contract a position depends on.
| 5.1 | Bridges and trust assumptions | 19 |
| 5.2 | Layer 2s, sequencers & withdrawal paths | 20 |
| 5.3 | Oracles, TWAPs & manipulation | 21 |
| 5.4 | Smart contracts: state, proxies, admin keys | 22 |
| 5.5 | Smart-contract risk & what audits don't prove | 23 |

### Module 6 — Protocol Research *(4 lessons)*
Outcome: complete a full due-diligence file on a real protocol.
| 6.1 | Protocol due diligence | 24 |
| 6.2 | Tokenomics: supply, unlocks, FDV, value capture | 25 |
| 6.3 | Governance & DAOs | 26 |
| 6.4 | The on-chain research workflow | 41 |
Assets: **DeFi Protocol Due Diligence Tracker** (Notion) + `defi-due-diligence` 6-step loop.

### Module 7 — On-Chain Analytics *(8 lessons)*
Outcome: read on-chain data without over-interpreting it.
| 7.1 | On-chain data foundations (address ≠ person) | 27 |
| 7.2 | Block explorer mastery | 28 |
| 7.3 | Exchange flows | 29 |
| 7.4 | Whale & entity analysis | 30 |
| 7.5 | Holder & supply metrics (MVRV, SOPR, HODL waves) | 31 |
| 7.6 | Network activity | 32 |
| 7.7 | DEX & liquidity analytics | 33 |
| 7.8 | Derivatives on-chain (perps, funding, OI) | 34 |
Assets: 20-metric directory as a downloadable reference card.

### Module 8 — The DeFi Operating System *(4 lessons)*
Outcome: a written portfolio plan with risk buckets, limits and an emergency plan.
| 8.1 | DeFi portfolio construction | 38 |
| 8.2 | The DeFi risk framework | 39 |
| 8.3 | Strategy library (16 frameworks, Core → Advanced), full content in `03-defi-strategy-mastery.md` | 40 |
| 8.4 | The operating playbook: deploy, monitor, respond, review | 42 |

### Module 9 — DeFi vs Grid Bots *(3 lessons, new content)*
Outcome: choose the right tool for the market — and the natural bridge into GBB.
| 9.1 | LP position vs grid bot: same idea (sell high/buy low inside a range), different risks | new |
| 9.2 | When a CEX grid beats on-chain LP, and when it doesn't (fees, custody, IL vs inventory risk, regime) | new |
| 9.3 | Building a combined system: grid bots for range markets, DeFi for yield/collateral | new |
Cross-sell: GBB checkout link for non-customers; Elite Intel invite for everyone.

### Capstone
Pick one real protocol → complete the due-diligence file (Module 6) → write a
position plan with sizing, monitoring triggers and exact unwind (Module 8).
Submitted via Whop; optional review on the higher tier.

### Totals
9 modules · 45 lessons (42 ATLAS + 3 new) · 135 quiz questions · 2 worksheets · 1 capstone.

---

## What I need from you to move to Phase 3 (Whop setup)
1. Name
2. Primary audience (warm-first recommended?)
3. Format: core only, or core + live tier (and are `vip-defi-consult` / `defi` Calendly links for this?)
4. Prices + refund policy
5. Starter tier: does it exist?
6. 9-module structure OK?
