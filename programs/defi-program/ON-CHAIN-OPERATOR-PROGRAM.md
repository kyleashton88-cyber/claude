# On-Chain Operator Program — Master File

![On-Chain Operator Program](assets/brand/logo-horizontal-light.png)

*Generated 2026-09-24 from `programs/defi-program/`. Don't edit this file directly: edit the source files and run `python3 programs/defi-program/build_master.py`.*

## Contents
0. Brand & logo (see `06-whop-store-listing.md`)
1. Build status
2. Offer, decisions & curriculum
3. Whop setup
4. Whop store listing
5. Funnel changes
6. Course content (finished lessons)
7. Skills archive
8. Build prompt (hand this to Claude Code)

---

# 1. Build status


**Everything in one file:** `ON-CHAIN-OPERATOR-PROGRAM.md`, also as `On-Chain-Operator-Program.docx` (Word) and `On-Chain-Operator-Program.pdf`.
Rebuild: `python3 programs/defi-program/build_master.py`, then `cd programs/defi-program/export && npm install && npm run build`.
**To finish the build with AI:** paste `BUILD-PROMPT.md` into Claude Code.

| File | Phase | Status |
|---|---|---|
| `01-offer-and-curriculum.md` | 1–2 Offer + curriculum | Decisions locked; curriculum expanded to 6 stages · 15 modules · 76 lessons |
| `02-sample-lesson-amm-math.md` | Lesson 2.2 | Written |
| `03-defi-strategy-mastery.md` | Lesson 8.3 (strategy library) | Written |
| `04-funnel-changes.md` | 4 Funnel wiring | Draft, not applied to Zapier |
| `05-whop-setup.md` | 3 Whop setup | Decisions locked; waiting on Whop reconnect + product ID |
| `06-whop-store-listing.md` | Store product listing: copy + image upload map | Ready to paste (3 placeholders) |
| `assets/` | 50 images: logo system (8), store icon + banner + 7 gallery (9), 15 module banners, 13 diagrams, 5 charts | Rendered by `export/build_images.js` |
| `lessons/module-01-foundations-safety.md` | Module 1 (6) | Written |
| `lessons/module-02-trading-on-chain.md` | Module 2 (4 + sample 2.2) | Written |
| `lessons/module-09-defi-vs-grid-bots.md` | Module 9 (3) | Written |
| `lessons/module-10-advanced-yield-engineering.md` | Module 10 (6) | Written |
| `lessons/module-12-own-bank.md` | Module 12 (6) | Written |
| `lessons/module-13-income-engine.md` | Module 13 (5) | Written |


Lessons written: 32 of 76 (Modules 1, 2, 9, 10, 12, 13 + lesson 8.3).
Still to write (44): Module 0 · Modules 3–7 · lessons 8.1, 8.2, 8.4 · Module 11 · Module 14.
Phase 3: blocked until Whop is reconnected in Zapier and the product is created in the Whop dashboard (see `05-whop-setup.md`).

---

# 2. Offer, decisions & curriculum

![On-Chain Operator Program](assets/store/banner-1920x1080.png)

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
| Structure | **15 modules, 76 lessons, 6 stages: zero to operator** (expanded 2026-09-24) |

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
*Superseded: see "Decisions so far" at the top. Kept for the record.*
| Option | Why |
|---|---|
| **DeFi Operator Blueprint** (recommended) | Matches "Grid Bot Building Blueprint" on Whop; "operator" = process, not hype |
| Risk-First DeFi | States the differentiator |
| On-Chain Operator Program | Neutral, broader |

### Who it's for — DECIDE
*Superseded: see "Decisions so far" at the top. Kept for the record.*
| Audience | Fit | How they arrive |
|---|---|---|
| **GBB customers** (recommended primary) | Already trust you, already think in systems/risk | Cross-sell email ~14 days after GBB onboarding |
| Elite Intel Community members | Warm, recurring, already reading intel briefs | In-community offer + LAUNCH-style code |
| Cold ad traffic | Largest pool, needs most education | Separate ad campaign → lead skill with `defi-lead` tag |

Recommendation: launch to GBB customers + Elite Intel members first (warm,
lower CAC, real feedback), open to cold traffic once conversion is proven.

### Format — DECIDE
*Superseded: see "Decisions so far" at the top. Kept for the record.*
- **Core (recommended):** self-paced Whop course (15 modules below) + worksheets
  (the two Notion trackers as templates) + quizzes + capstone.
- **Optional higher tier:** Core + live monthly DeFi Q&A / portfolio review.
  Your Calendly already has `vip-defi-consult` and `defi` links — are those
  for this program? (The GBB skills are told never to use them, so they're
  free for DeFi.)

### Pricing — DECIDE (proposal only)
*Superseded: see "Decisions so far" at the top. Kept for the record.*
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
![Product ladder](assets/diagrams/product-ladder.png)

---

## Phase 2 — Curriculum: zero to mastery

![Path to mastery](assets/diagrams/path-to-mastery.png)

**Expanded 2026-09-24:** the program now takes someone who knows nothing all
the way to operating as their own bank. That's **15 modules and 76 lessons in
6 stages**. Modules 1–9 keep their numbers. Module 0 and Modules 10–14 are new.
All 42 ATLAS chapters are still used exactly once; the new modules are
original content.

Every lesson follows one template: **Objective → Explanation → Worked example
→ Checklist → 3 quiz questions**, with at least one diagram or chart. A full
sample lesson is in `02-sample-lesson-amm-math.md`.

| Stage | Modules | You can… |
|---|---|---|
| **0 · Zero** | 0 | Buy crypto, set up a wallet and send a first transaction safely |
| **1 · Foundations** | 1–2 | Protect a wallet, read a transaction, swap and LP deliberately |
| **2 · Practitioner** | 3–5 | Borrow, earn yield and map infrastructure risk |
| **3 · Analyst** | 6–7 | Research any protocol and read on-chain data |
| **4 · Strategist** | 8–11 | Run the 25-strategy library, engineer fixed and hedged yield, stress-test a portfolio |
| **5 · Operator** | 12–14 | Run your own on-chain bank: balance sheet, credit line, income engine, automation |

---

## Stage 0 · Zero

### Module 0 — Crypto From Zero *(5 lessons, new)*
Outcome: go from never having owned crypto to a funded, secured wallet and a first on-chain transaction.

| # | Lesson | Source |
|---|---|---|
| 0.1 | Money, ledgers and why blockchains exist | new |
| 0.2 | Buying your first crypto: exchanges, KYC, fees, withdrawals | new |
| 0.3 | Exchange account vs self-custody wallet: who holds the keys | new |
| 0.4 | Your first wallet and first transaction (small test amount) | new |
| 0.5 | The language of DeFi: a working glossary and mental models | new |

---

## Stage 1 · Foundations

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

| # | Lesson | ATLAS ch. |
|---|---|---|
| 2.1 | DEXs, aggregators & routing | 6 |
| 2.2 | AMM mathematics (x·y=k) — *sample lesson* | 7 |
| 2.3 | Providing liquidity | 8 |
| 2.4 | Impermanent loss & true LP P&L | 9 |
| 2.5 | MEV and how to protect your trades | 35 |

Assets: AMM flow diagram, 100 ETH / 300k USDC worked example, LP-vs-hold benchmark.

---

## Stage 2 · Practitioner

### Module 3 — Lending & Leverage *(4 lessons)*
Outcome: borrow against collateral with a buffer and a written defence plan.

| # | Lesson | ATLAS ch. |
|---|---|---|
| 3.1 | How lending markets work (utilisation, rate curves) | 10 |
| 3.2 | LTV, liquidation threshold & health factor | 11 |
| 3.3 | Liquidations and cascades | 12 |
| 3.4 | Borrowing strategies & looping | 13 |

Assets: liquidation feedback-loop diagram, Aave health-factor primary source.

### Module 4 — Yield *(6 lessons)*
Outcome: split any APY into organic vs subsidised, and name the risk being paid for.

| # | Lesson | ATLAS ch. |
|---|---|---|
| 4.1 | Yield farming: base yield vs emissions | 14 |
| 4.2 | Native staking | 15 |
| 4.3 | Liquid staking (LSTs) | 16 |
| 4.4 | Restaking & shared security | 17 |
| 4.5 | Vaults & yield optimisers | 18 |
| 4.6 | Airdrops & points — opportunity cost | 37 |

### Module 5 — Infrastructure Risk *(5 lessons)*
Outcome: map every bridge, oracle, L2 and contract a position depends on.

| # | Lesson | ATLAS ch. |
|---|---|---|
| 5.1 | Bridges and trust assumptions | 19 |
| 5.2 | Layer 2s, sequencers & withdrawal paths | 20 |
| 5.3 | Oracles, TWAPs & manipulation | 21 |
| 5.4 | Smart contracts: state, proxies, admin keys | 22 |
| 5.5 | Smart-contract risk & what audits don't prove | 23 |

---

## Stage 3 · Analyst

### Module 6 — Protocol Research *(4 lessons)*
Outcome: complete a full due-diligence file on a real protocol.

| # | Lesson | ATLAS ch. |
|---|---|---|
| 6.1 | Protocol due diligence | 24 |
| 6.2 | Tokenomics: supply, unlocks, FDV, value capture | 25 |
| 6.3 | Governance & DAOs | 26 |
| 6.4 | The on-chain research workflow | 41 |

Assets: **DeFi Protocol Due Diligence Tracker** (Notion) + `defi-due-diligence` 6-step loop.

![The 6-step research loop](assets/diagrams/research-loop.png)

### Module 7 — On-Chain Analytics *(8 lessons)*
Outcome: read on-chain data without over-interpreting it.

| # | Lesson | ATLAS ch. |
|---|---|---|
| 7.1 | On-chain data foundations (address ≠ person) | 27 |
| 7.2 | Block explorer mastery | 28 |
| 7.3 | Exchange flows | 29 |
| 7.4 | Whale & entity analysis | 30 |
| 7.5 | Holder & supply metrics (MVRV, SOPR, HODL waves) | 31 |
| 7.6 | Network activity | 32 |
| 7.7 | DEX & liquidity analytics | 33 |
| 7.8 | Derivatives on-chain (perps, funding, OI) | 34 |

Assets: 20-metric directory as a downloadable reference card.

---

## Stage 4 · Strategist

### Module 8 — The DeFi Operating System *(4 lessons)*
Outcome: a written portfolio plan with risk buckets, limits and an emergency plan.

| # | Lesson | ATLAS ch. |
|---|---|---|
| 8.1 | DeFi portfolio construction | 38 |
| 8.2 | The DeFi risk framework | 39 |
| 8.3 | Strategy library (25 strategies in 6 levels, Core → Professional), full content in `03-defi-strategy-mastery.md` | 40 |
| 8.4 | The operating playbook: deploy, monitor, respond, review | 42 |

### Module 9 — DeFi vs Grid Bots *(3 lessons, new content)*
Outcome: choose the right tool for the market — and the natural bridge into GBB.

| # | Lesson | ATLAS ch. |
|---|---|---|
| 9.1 | LP position vs grid bot: same idea (sell high/buy low inside a range), different risks | new |
| 9.2 | When a CEX grid beats on-chain LP, and when it doesn't (fees, custody, IL vs inventory risk, regime) | new |
| 9.3 | Building a combined system: grid bots for range markets, DeFi for yield/collateral | new |

Cross-sell: GBB checkout link for non-customers; Elite Intel invite for everyone.

### Module 10 — Advanced Yield Engineering *(6 lessons, new)*
Outcome: build fixed, hedged and structured yield, and know exactly what each one is short.

| # | Lesson | Source |
|---|---|---|
| 10.1 | Fixed-rate yield: principal and yield tokens (PT/YT) | new |
| 10.2 | Cash-and-carry basis trades | new |
| 10.3 | Delta-neutral funding carry, done properly | new |
| 10.4 | Options income: covered calls, cash-secured puts, options vaults | new |
| 10.5 | Active concentrated-liquidity management | new |
| 10.6 | Restaking and points: pricing speculative yield | new |

### Module 11 — Hedging & Risk Engineering *(5 lessons, new)*
Outcome: hedge the risks you don't want, stress-test the portfolio, and have an incident plan ready.

| # | Lesson | Source |
|---|---|---|
| 11.1 | Hedging price exposure with perps and options | new |
| 11.2 | Depeg, protocol and smart-contract cover | new |
| 11.3 | Liquidation protection: buffers, alerts and automated deleveraging | new |
| 11.4 | Stress-testing a portfolio: −50% days, depegs, rate spikes | new |
| 11.5 | Incident response: what to do in the first 60 minutes | new |

---

## Stage 5 · Operator — operate as your own bank

![Operate as your own bank](assets/diagrams/own-bank.png)

### Module 12 — Operate as Your Own Bank *(6 lessons, new)*
Outcome: run your crypto like a bank runs its book: a balance sheet, custody policy, a credit line, a liquidity ladder and records.

| # | Lesson | Source |
|---|---|---|
| 12.1 | Your balance sheet: assets, liabilities, equity | new |
| 12.2 | Custody architecture: vault, multisig and spending policies | new |
| 12.3 | The credit line: borrowing against your assets like a bank client | new |
| 12.4 | Treasury and the liquidity ladder | new |
| 12.5 | Being the lender: supplying, curating and pricing credit risk | new |
| 12.6 | Books, records and succession: if you're gone, can your family recover it? | new |

### Module 13 — The Income Engine *(5 lessons, new)*
Outcome: design an income portfolio, measure expected income after expected losses, and set a payout you can sustain.

| # | Lesson | Source |
|---|---|---|
| 13.1 | Income sources ranked by durability | new |
| 13.2 | Risk-adjusted yield: subtracting expected losses | new |
| 13.3 | Building the income portfolio | new |
| 13.4 | The payout policy: how much you can take out | new |
| 13.5 | Scaling, compounding and the annual review | new |

### Module 14 — Automation & Mastery *(4 lessons, new)*
Outcome: monitor and automate safely, run multisig operations, and complete the operator capstone.

| # | Lesson | Source |
|---|---|---|
| 14.1 | Monitoring: dashboards, alerts and on-chain watchers | new |
| 14.2 | Automation: keepers, bots and agents without handing over the keys | new |
| 14.3 | Operating procedures: multisig signing, change control, reviews | new |
| 14.4 | Operator capstone and certification | new |

---

### Capstones
- **Analyst capstone (after Module 7):** a complete due-diligence file on one real protocol.
- **Operator capstone (Module 14):** a full personal "bank": balance sheet, custody
  policy, credit-line policy, income portfolio with risk-adjusted expected income,
  payout policy, stress test and incident plan. Reviewed on the Live tier.

### Totals
15 modules · 76 lessons (42 ATLAS + 34 new) · 228 quiz questions · 25 strategy playbooks · 2 capstones · strategy calculator with 15 commands.

---

## Still open
1. Live-tier price
2. Refund policy
3. Grid Bot Builder customer pricing (if any)
4. Does the "Grid Bot Starter" tier exist?

---

# 3. Whop setup

## Decisions locked (2026-09-24)
| Item | Decision |
|---|---|
| Name | On-Chain Operator Program |
| Tier 1 — Course (self-paced, 15 modules, 76 lessons, worksheets, 2 capstones) | **$15,000 one-time** (no payment plan) |
| Tier 2 — Live (course + live sessions) | **Priced above $15,000 — number TBD** |
| Audience | Everyone at launch (GBB customers, Elite Intel members, cold ads) |
| Sales path | **Application → call → checkout** (no straight-to-checkout ads) |
| Call link | `vip-defi-consult` Calendly (verify the exact URL is live) |

Still open: Tier 2 price · refund policy · GBB-customer price (if any) ·
the Starter tier / GBB price conflict.

## Blockers found
1. **Whop is not connected in Zapier** (0 connected accounts on WhopCLIAPI).
   Reconnect it in Zapier before any Whop step below. The existing `gbb-*`
   skills also need it to run.
2. **Zapier can't create Whop products.** It can create *plans*, checkout
   sessions, leads, promo codes and invoices. The product itself must be
   created in the Whop dashboard.

## Step 1 — You, in the Whop dashboard
1. Create a product named **On-Chain Operator Program**. Keep it **hidden /
   unlisted** until launch. Upload the icon, banner and gallery images and
   paste the copy from `06-whop-store-listing.md`.
2. Add a course experience and create the 9 module sections (titles in
   `01-offer-and-curriculum.md`).
3. Add terms of sale: refund policy (once decided) and "Educational content
   only. Not financial advice. No results are guaranteed."
4. Send me the product ID (starts with `prod_`).

## Step 2 — Me, via Zapier (after you confirm)
| Action | Zapier tool | Values |
|---|---|---|
| Course plan | `whop_create_plan` | product = your `prod_` ID, one-time, $15,000, hidden until launch |
| Live-tier plan | `whop_create_plan` | once the price is set |
| Checkout links per campaign | `whop_create_checkout_session` | metadata `utm_campaign`, `utm_adset`, `utm_creative` so ad reports attribute sales |
| Applications | `whop_create_lead` | one lead per application, product-specific |

Nothing gets created until you've seen the exact values and said yes.

## Step 3 — Upload content
Written and ready to paste in (32 of 76 lessons): Modules 1, 2, 9, 10, 12
and 13, plus lesson 8.3 (`lessons/`, `02-…`, `03-…`). Still to write:
Module 0, Modules 3–7, lessons 8.1/8.2/8.4, Modules 11 and 14.

## Step 4 — High-ticket sales path
![High-ticket sales path](assets/diagrams/sales-funnel.png)

Suggested qualification (adjust as you like): lead score ≥ 6 (capital 20k+ /
major exchange / some experience) **and** completed application.

---

# 4. Whop store listing

![On-Chain Operator Program](assets/store/banner-1920x1080.png)

Everything needed to add the program to your Whop store as a new product:
logo, images, copy and upload order. **Nothing is published.** You create the
product in the Whop dashboard (Zapier can't create products), paste this in,
and keep it hidden until launch.

> Check Whop's current image size limits in the dashboard when you upload.
> These files are produced at standard sizes (1024×1024 square, 1920×1080
> 16:9) and can be re-exported at any size with `npm run images`.

---

## 1. The logo

![Brand guide](assets/brand/brand-guide.png)

The mark is **two interlocked chain rings inside a hexagonal block**, with
nodes on its corners: a chain (on-chain), a block, and a network. The rings
link, like the two halves of the program: DeFi strategy and running your own bank.

| File | Use |
|---|---|
| `assets/brand/logo-icon-1024.png` | **Whop product icon**, social avatars (stacked lockup on navy) |
| `assets/brand/logo-mark-dark-1024.png` | App icon / square badge without text |
| `assets/brand/logo-mark-transparent-dark-1024.png` | Mark over dark backgrounds (transparent PNG) |
| `assets/brand/logo-mark-transparent-light-1024.png` | Mark over light backgrounds (transparent PNG) |
| `assets/brand/logo-horizontal-dark.png` | Headers, email banners on dark |
| `assets/brand/logo-horizontal-light.png` | Documents, invoices, light pages |
| `assets/brand/favicon-256.png` | Favicon / tiny sizes (no corner nodes) |
| `assets/brand/brand-guide.png` | Colours, type and usage rules |

Rules: keep clear space of one ring's width around the mark; never recolour
the rings, stretch the mark or put the light version on a dark background.

---

## 2. Images: upload map

| Whop slot | File | Size |
|---|---|---|
| Product icon / logo | `assets/store/icon-1024.png` (same as `brand/logo-icon-1024.png`) | 1024×1024 |
| Cover / hero banner | `assets/store/banner-1920x1080.png` | 1920×1080 |
| Gallery 1 | `assets/store/gallery-01-path-to-mastery.png` | 1920×1080 |
| Gallery 2 | `assets/store/gallery-02-curriculum.png` | 1920×1080 |
| Gallery 3 | `assets/store/gallery-03-own-bank.png` | 1920×1080 |
| Gallery 4 | `assets/store/gallery-04-strategy-levels.png` | 1920×1080 |
| Gallery 5 | `assets/store/gallery-05-research-loop.png` | 1920×1080 |
| Gallery 6 | `assets/store/gallery-06-grid-vs-lp.png` | 1920×1080 |
| Gallery 7 | `assets/store/gallery-07-whats-included.png` | 1920×1080 |
| Course module headers | `assets/modules/module-00.png` … `module-14.png` | 1600×500 @2x |
| In-lesson diagrams & charts | `assets/diagrams/*.png`, `assets/charts/*.png` | 1800 wide @2x |

![Icon](assets/store/icon-1024.png)

![Path to mastery](assets/store/gallery-01-path-to-mastery.png)
![Curriculum](assets/store/gallery-02-curriculum.png)
![Own bank](assets/store/gallery-03-own-bank.png)
![Strategy levels](assets/store/gallery-04-strategy-levels.png)
![Research loop](assets/store/gallery-05-research-loop.png)
![Grid vs LP](assets/store/gallery-06-grid-vs-lp.png)
![What's included](assets/store/gallery-07-whats-included.png)

---

## 3. Listing copy

**Product name:** On-Chain Operator Program

**Tagline (short):** From zero to your own on-chain bank.

**Short description (≈150 characters):**
DeFi from first principles to professional strategies. Build a risk-adjusted
income engine and run your capital like a bank. 15 modules · 76 lessons.

**Headline:** From zero to your own on-chain bank.

**Full description:**

> Most people enter DeFi through a number: an APY. Operators start with a
> different question: *what am I being paid to risk, and how do I get out?*
>
> The On-Chain Operator Program takes you from never having owned crypto to
> running your capital the way a bank runs its book: a balance sheet, a custody
> policy, a credit line, a liquidity ladder, and an income engine with a
> payout you can sustain.
>
> Six stages, 15 modules and 76 lessons: wallets and safety, trading and
> liquidity, lending and yield, protocol research and on-chain analytics, 25
> strategy playbooks up to fixed-rate, basis, options and hedged yield, and
> finally operating your own on-chain bank. Every strategy is taught with its
> maths, its kill rules and exactly how it loses money.

**What you'll learn**
- Stage 0–1: buy, store and move crypto safely; read any transaction; swap and provide liquidity deliberately
- Stage 2–3: lending, health factors and liquidations; yield, staking and restaking; a 6-step research loop for any protocol; on-chain analytics
- Stage 4: 25 strategy playbooks in 6 levels, including fixed-rate yield (PT/YT), cash-and-carry basis, delta-neutral funding carry, covered calls and cash-secured puts, hedging and stress testing
- Stage 5: operate as your own bank. Balance sheet, multisig custody, a credit line against your assets, a liquidity ladder, lending-desk decisions, books and succession, and an income engine that pays out less than it expects to earn

**What's included**

| | Course | Live |
|---|---|---|
| 15 modules, 76 lessons, zero to operator | ✓ | ✓ |
| 25 strategy playbooks with maths and kill rules | ✓ | ✓ |
| Checklists and quizzes in every lesson | ✓ | ✓ |
| Due-diligence, pre-launch and bank-policy worksheets | ✓ | ✓ |
| Strategy, income and balance-sheet calculators | ✓ | ✓ |
| Analyst and operator capstones | ✓ | ✓ |
| Live group sessions | | ✓ |
| Capstone and portfolio reviews | | ✓ |
| Own-bank policy and income-engine reviews | | ✓ |
| **Price** | **$15,000 one-time** | **`<LIVE_PRICE>`** |

**Who it's for**
- Complete beginners who want to learn DeFi properly, from zero, with a process
- Traders and Grid Bot Builder customers ready to operate on-chain
- Holders of meaningful crypto who want income and liquidity from it without taking risks they don't understand

**Who it's not for**
- Anyone looking for guaranteed returns or signals to copy
- Anyone unwilling to self-custody or follow a written policy

**How to join:** Apply → short call → enrolment link. (Application link:
`<DEFI_APPLICATION_URL>`)

**FAQ**
- *I've never owned crypto. Is this for me?* Yes. Module 0 starts from buying your first crypto and setting up a wallet.
- *Do you manage my funds or need my keys?* Never. You keep custody. We will never ask for a seed phrase, private key or API key.
- *Will I make money / earn an income?* The program teaches you to build and run an income portfolio and to measure it honestly: expected income after expected losses, with a payout below that. It doesn't promise or project returns, and every strategy is taught alongside how it loses money.
- *What does "operate as your own bank" mean?* Running your crypto with the disciplines a bank uses: a balance sheet, custody controls, a credit policy, liquidity management and records. It's a method, not a licence or a financial service.
- *How does this relate to Grid Bot Builder?* Module 9 shows how on-chain liquidity and exchange grid bots do similar jobs, and how to run both in one portfolio.
- *Refunds?* `<REFUND_POLICY>`

**Footer disclaimer (put on the listing and at checkout):**
Educational content only. Not financial, tax or legal advice. Digital assets
are volatile and you can lose some or all of your capital. No results or
income are guaranteed.

---

## 4. Store setup checklist
- [ ] Product created in the Whop dashboard as **hidden**, named "On-Chain Operator Program"
- [ ] Logo icon, banner and 7 gallery images uploaded in the order above
- [ ] Copy pasted; `<LIVE_PRICE>`, `<REFUND_POLICY>`, `<DEFI_APPLICATION_URL>` filled
- [ ] Course experience added with 15 modules; module headers uploaded; lessons pasted with their diagrams
- [ ] Plans created via Zapier (course $15,000 one-time; live tier once priced), approved first
- [ ] Checkout tested end to end on a hidden plan
- [ ] Listing reviewed for any income or return claims before going public

---

# 5. Funnel changes (draft, not applied)

Proposed changes to the four live Zapier skills so they handle the DeFi
program alongside Grid Bot Builder. **Nothing has been changed in Zapier.**
Once you approve, the edits go into Zapier (`update_zapier_skill`) and are
mirrored into `.claude/skills/gbb-*`.

Product name: **On-Chain Operator Program**, course $15,000 one-time, sold through application → call → checkout (see `05-whop-setup.md`). This changes the emails below: hot/warm DeFi leads get the **application + call** link, not a direct checkout link. Placeholders still open: `<DEFI_LIVE_PRICE>`, `<DEFI_GBB_PRICE>`,
`<DEFI_CHECKOUT_URL>`, `<DEFI_PLAN_IDS>`, `<DEFI_ACCESS_URL>` (the program's Whop hub link), `<DEFI_APPLICATION_URL>` (Typeform application), `<DEFI_CALL_LINK>` (your `vip-defi-consult` Calendly link; verify the URL).

---

## 1. gbb new lead → handles DeFi interest

**Add fixed values**
- DeFi product: `On-Chain Operator Program`, `$15,000` one-time; checkout `<DEFI_CHECKOUT_URL>`.
- Mailchimp tags: `defi-lead`, `defi-nurture`.
- HubSpot deal name: `DEFI - <First Last>`.

**Add an interest field** to the form / intake: `interest = grid | defi | both`.

**Routing change (after scoring, step 3):**
| interest | Deal(s) created | Tags | Email |
|---|---|---|---|
| grid | `GBB - …` (unchanged) | `gbb-lead` (+ hot/nurture) | unchanged |
| defi | `DEFI - …`, amount `$15,000` | `defi-lead` (+ `defi-nurture` if cold) | DeFi email by tier (below) |
| both | GBB deal only; DeFi mentioned as next step | `gbb-lead`, `defi-lead` | GBB email + one line on DeFi |

Scoring stays the same. Capital and experience predict fit for both products.

**Draft emails (plain text, under 120 words, no profit promises)**

*DeFi — warm/hot*
> Hi {first},
> Thanks for your interest in On-Chain Operator Program. It's a step-by-step program for operating in DeFi safely: how to research a protocol, where yield actually comes from, and how to plan the exit before you enter.
> 15 modules and 76 lessons, from zero to running your own on-chain bank.
> It's application-only. Apply here: <DEFI_APPLICATION_URL>
> Qualified applicants book a call to see if it's the right fit: <DEFI_CALL_LINK>
> Stewart
> *Educational content, not financial advice.*

*DeFi — cold (nurture)*
> Hi {first},
> One rule before you put anything into DeFi: if you can't explain how you'd get out, don't get in.
> Over the next few emails I'll share the checklist we use before signing any transaction.
> If you want daily market intel in the meantime, Elite Intel Community has a 3-day free trial: https://elite-intel-community.whop.site/
> Stewart

---

## 2. gbb customer onboarding → DeFi branch + cross-sell

**When product = `On-Chain Operator Program`:**
1. HubSpot: lifecycle `customer`; deal `DEFI - …` → closedwon, amount = actual plan price.
2. Mailchimp: remove `defi-lead`, add `defi-customer`.
3. Gmail onboarding (draft below).
4. Sheets → Payments (product = DeFi) and ExcludeList.
5. Elite Intel Community invite, same rules as GBB (separate email, paid trial, never granted free).
6. If *not* a GBB customer: tag `gbb-crosssell-candidate` (no email yet; see the sequence below).

*DeFi onboarding email*
> Welcome to On-Chain Operator Program, {first}.
> Your access is live: <DEFI_ACCESS_URL> (log in with this email).
> Start with Module 1 — Foundations & Safety. Do the practical (3-wallet setup) before anything else.
> Two rules for the whole program:
> 1. Never share your seed phrase or private keys. We will never ask.
> 2. Run the before-signing checklist every time.
> Reply to this email if you get stuck.
> Stewart

**When product = Grid Bot Builder** (existing flow, plus one addition):
- Tag `defi-crosssell-candidate`. The cross-sell email goes **14 days after
  onboarding**, not in the welcome sequence, so they're set up and trading first.

*GBB → DeFi cross-sell (day 14)*
> Hi {first},
> By now your grid bots should be running. Here's where most of our builders go next: putting idle stablecoins and reserves to work on-chain, without taking on risks they don't understand.
> On-Chain Operator Program covers this, including a module on how a DeFi liquidity position is basically an on-chain grid bot, and when each one wins.
> It's application-only: <DEFI_APPLICATION_URL>
> Stewart

---

## 3. gbb ad performance → report DeFi

- Add `On-Chain Operator Program` to "products" with its plan IDs.
- Per campaign: DeFi sales (# and $), CAC-to-DeFi.
- New cross-sell metric: **GBB → DeFi attach rate** = GBB buyers who later buy DeFi ÷ GBB buyers ≥ 14 days old.
- Budget rule unchanged (it uses total net Whop revenue).

## 4. gbb pipeline check → DeFi deals

- Include deals starting `DEFI -` with the same stages.
- Revenue by product adds DeFi.
- Stale DeFi leads → offer `defi-nurture` tagging (same confirm rule).

---

## New Zapier skill (proposed): `defi-crosssell-sweep`
Weekly: find `defi-crosssell-candidate` contacts whose GBB onboarding is ≥ 14
days old and who haven't bought DeFi → show the list → on a yes, send the day-14
email and remove the tag. Same guardrails: no Slack/Discord/Skool, confirm
before sending, no profit promises.

---

# 6. Course content

Finished lessons in curriculum order. Lesson 8.3 (strategy mastery) appears before Module 9.

---

# Module 1 — Foundations & Safety

![Module 1 — Foundations & Safety](assets/modules/module-01.png)

*Outcome: set up and use a wallet safely, and know what can go irreversibly wrong before any capital moves.*
*Source: ATLAS "DeFi & On-Chain" ch. 1–5, 36. Educational content only. Not financial advice.*

The **before-signing checklist** is introduced in this module and used in every module after it:

- [ ] Chain confirmed
- [ ] Contract address verified from an authoritative source
- [ ] Token and amount double-checked
- [ ] Spender / allowance reviewed
- [ ] Slippage set deliberately
- [ ] Gas estimate reviewed
- [ ] Intended outcome stated in one sentence

---

## Lesson 1.1 — What DeFi is, and the risk-first mindset *(ch. 1)*

### Objective
Describe the DeFi stack and explain why every yield is payment for a risk.

### Explanation
DeFi replaces intermediaries (banks, brokers, exchanges) with **smart
contracts**: public programs on a blockchain that hold assets and follow fixed
rules. The stack, bottom to top:

1. **Blockchain**: records every balance and transaction (Ethereum, L2s, other chains).
2. **Smart contracts**: the protocol logic (a lending market, an exchange pool).
3. **Tokens**: the assets the contracts move.
4. **Wallets**: where *you* hold keys and sign actions.
5. **Interfaces**: websites that build transactions for you. They're a convenience, not the protocol itself.
6. **Data layers**: explorers and dashboards you use to verify what happened.

Three properties make DeFi powerful and dangerous:
- **Self-custody**: nobody can freeze your funds, and nobody can recover them either.
- **Composability**: protocols plug into each other. That makes products powerful, and a position can fail because of something it depends on.
- **Transparency**: you can verify everything on-chain. Transparent doesn't mean safe.

**Risk-first rule:** before comparing returns, list what could make you lose
money. A higher yield means you're being paid to carry more risk, whether or
not the website mentions it.

### Worked example
A pool advertises **12% APY on a stablecoin**. Before depositing, ask:
- Where does the 12% come from? Borrowers paying interest, trading fees, or a reward token?
- Which stablecoin, and what backs it? (Lesson 1.5)
- Which contracts hold the money, and who can upgrade them?
- Is there a bridge or oracle involved?
- How do I withdraw, and could withdrawals be blocked?

If you can't answer these, you don't know what the 12% is paying you for.

### Checklist
- [ ] I can name the six layers of the DeFi stack
- [ ] I can explain why self-custody cuts both ways
- [ ] Before any yield, I ask "what am I being paid to risk?"

### Quiz
<details><summary>1. Why can composability increase risk?</summary>A position inherits the failure risk of every protocol, asset, oracle and bridge it depends on.</details>
<details><summary>2. Is a website the same thing as the protocol?</summary>No. The interface only builds transactions. The contracts are the protocol, and interfaces can be faked or compromised.</details>
<details><summary>3. What is the risk-first mindset in one sentence?</summary>Identify what could make you lose money before you compare returns.</details>

---

## Lesson 1.2 — How a transaction actually happens *(ch. 2)*

### Objective
Follow a transaction from signature to finality, and estimate its cost.

### Explanation
**Lifecycle:** create → sign → broadcast → mempool (waiting) → included in a
block → confirmed → final.

- **Gas** is the unit of computation. Cost = `gas used × gas price`. On
  Ethereum the price has a *base fee* (burned) plus a *priority tip*
  (to get included sooner). Gas price is quoted in **gwei** (1 gwei = 0.000000001 ETH).
- **Nonce**: each account's transactions are numbered in order. A stuck
  low-nonce transaction blocks all later ones until it confirms or is
  **replaced** (same nonce, higher fee).
- **Failed transactions still cost gas.** The network did the computation even though the result was reverted.
- **Finality**: the point after which a transaction can't realistically be
  reversed. It differs by chain, and L2s have their own rules (Module 5).
- **Explorers** (e.g. Etherscan) show status, fee, sender, contract called, token transfers and logs.

### Worked example
A swap uses **150,000 gas** at **20 gwei**:
`150,000 × 20 = 3,000,000 gwei = 0.003 ETH`. At $3,000/ETH that's **$9**.
The same swap during congestion at 80 gwei costs **$36**. If you're compounding
$1.50 of rewards, the gas costs more than the rewards. That's why position
size matters on-chain.

### Checklist
- [ ] I check the fee estimate before signing
- [ ] I know how to find my transaction on an explorer
- [ ] I know a stuck transaction can be sped up or cancelled with the same nonce

### Quiz
<details><summary>1. Your transaction reverted. Did you pay?</summary>Yes, for the gas used up to the point of failure.</details>
<details><summary>2. 200,000 gas at 10 gwei with ETH at $2,500 costs?</summary>2,000,000 gwei = 0.002 ETH = $5.</details>
<details><summary>3. Why are your newer transactions all pending?</summary>An earlier nonce is stuck. Replace or speed it up, and the rest follow.</details>

---

## Lesson 1.3 — Wallets, keys, hardware & multisig *(ch. 3)*

### Objective
Set up a wallet structure where one mistake can't lose everything.

### Explanation
- **Private key**: the authority to sign. Whoever has it controls the funds.
- **Seed phrase**: 12–24 words that recreate your keys. **Never type it into
  a website, never photograph it, never share it. No legitimate support team
  will ever ask for it.**
- **Hardware wallet**: keeps keys on a separate device. Signing requires physical confirmation.
- **Multisig**: needs M of N signers (e.g. 2 of 3). Good for large or shared funds.
- **Smart wallets**: contract accounts that can add spending limits, recovery and batching.

**Compartmentalise:** separate wallets by job, so a compromise only reaches one of them.

### Worked example — the 3-wallet setup

![The 3-wallet setup](assets/diagrams/three-wallets.png)

| Wallet | Holds | Signs | Device |
|---|---|---|---|
| **Vault** | Long-term holdings | Almost never. No DeFi approvals | Hardware (or multisig) |
| **Operator** | Active DeFi positions | Known, verified protocols only | Hardware |
| **Burner** | Small amounts for new apps, mints, airdrops | Anything experimental | Hot wallet |

Move money *down* the chain (vault → operator → burner) only as needed, and
sweep profits back *up*. If the burner gets drained, you lose only the burner's balance.

### Checklist
- [ ] Seed phrase stored offline, in two separate physical places
- [ ] Vault wallet has never approved a DeFi contract
- [ ] Separate burner wallet for anything new
- [ ] I read every signing prompt on the hardware device screen, not just the website

### Quiz
<details><summary>1. A "support agent" in DMs needs your seed phrase to fix a stuck transaction. What do you do?</summary>Nothing. It's a scam, every time. Block and report.</details>
<details><summary>2. Why keep the vault wallet free of approvals?</summary>Approvals let contracts move your tokens. With none, a compromised protocol can't reach it.</details>
<details><summary>3. What does 2-of-3 multisig protect against?</summary>A single lost or compromised key. Two signers are still needed to move funds.</details>

---

## Lesson 1.4 — Tokens, approvals & allowances *(ch. 4)*

### Objective
Read an approval request and know what you're allowing.

### Explanation
- Most tokens on EVM chains are **ERC-20** (fungible). NFTs (ERC-721/1155)
  can also represent positions (e.g. concentrated LP).
- To let a protocol move your tokens you **approve** a **spender** for an
  **allowance**. The protocol then pulls tokens when you act.
- **Unlimited approvals** are convenient but let that contract move *all*
  of that token, now and in future. If the contract (or the approval) is
  exploited, the tokens can be taken.
- **Signature approvals (Permit / Permit2)** grant allowances with an
  off-chain signature, not a transaction. There's no gas, so they're easy to
  sign without noticing. Drainers abuse exactly this.
- **Wrapped / receipt tokens**: WETH, LP tokens and lending receipts represent a claim on something else.
- **Fake tokens**: anyone can create a token called "USDC". Only the **contract address** identifies it.

### Worked example — reading an approval
Wallet shows: *"Allow 0x3fC9…a1B2 to spend your USDC. Amount: Unlimited."*
1. Is `0x3fC9…a1B2` the protocol's official router? Check the docs or explorer.
2. Do I need unlimited? Edit it to the amount of this deposit.
3. Is this USDC the real contract?
4. After finishing, revoke with a revoke tool (e.g. revoke.cash) if I won't be back.

### Checklist
- [ ] Spender verified against official docs
- [ ] Allowance limited to what's needed
- [ ] Signature requests read as carefully as transactions
- [ ] Approvals reviewed and revoked monthly

### Quiz
<details><summary>1. Why is a gasless "Permit" signature dangerous?</summary>It can grant a token allowance without a transaction, so it's easy to sign without noticing. Drainers use it to take tokens.</details>
<details><summary>2. How do you know a token is the real one?</summary>By its contract address from an authoritative source, never by name or ticker.</details>
<details><summary>3. When should you revoke an approval?</summary>When you no longer use that protocol, or on a regular schedule.</details>

---

## Lesson 1.5 — Stablecoins and how they break *(ch. 5)*

### Objective
Classify a stablecoin by design and name what could break its peg.

### Explanation
| Type | Backing | Main risks |
|---|---|---|
| **Fiat-backed** | Cash/treasuries held by an issuer | Issuer, bank and custodian risk; freezes; redemption limited to approved parties |
| **Crypto-backed** | Over-collateralised on-chain crypto | Collateral crash, liquidations, oracle failure |
| **Synthetic / hedged** | Derivative positions (e.g. spot + short perp) | Funding turns negative, exchange/venue risk, model risk |
| **Algorithmic** | Mostly its own mechanism / sister token | Reflexive death spiral when confidence breaks |

**Peg mechanics:** if a stablecoin trades at $0.98 and can be redeemed for
$1.00, arbitrageurs buy and redeem it, pushing the price back up. The peg is
only as strong as **redemption access and reserve quality**.

History (research these as case studies):
- **May 2022**: TerraUSD (UST), an algorithmic design, lost its peg and collapsed toward zero.
- **March 2023**: USDC briefly traded well below $1 after part of its reserves were exposed to the failed Silicon Valley Bank, then recovered once reserves were confirmed.

### Worked example
A fiat-backed coin trades at **$0.97**. Redemption is **$1.00 minus a 0.1% fee**,
but only for verified institutional minters.
- A minter makes ~2.9% per coin by buying and redeeming, so arbitrage *should* restore the peg.
- You can't redeem, so you rely on minters acting and on the reserves being real.
- If markets doubt the reserves, minters may not step in, and the discount can grow.

### Checklist
- [ ] I know the type and backing of every stablecoin I hold
- [ ] I know who can redeem, and how
- [ ] I don't treat "different stablecoins" as diversified if they share issuers or collateral
- [ ] I have a depeg exit rule (e.g. sell or rotate below $0.99 for longer than X hours)

### Quiz
<details><summary>1. What keeps a fiat-backed stablecoin near $1?</summary>Redemption for $1 of reserves, plus arbitrageurs who can redeem.</details>
<details><summary>2. Why are algorithmic designs fragile?</summary>They rely on confidence and their own token. When demand falls, the mechanism can amplify the fall.</details>
<details><summary>3. Two stablecoins both backed by the same collateral. Diversified?</summary>No. They share the same failure point.</details>

---

## Lesson 1.6 — Scam defence *(ch. 36)*

### Objective
Recognise the common attacks before they cost you anything.

### Explanation
| Attack | How it works | Defence |
|---|---|---|
| **Phishing site** | Look-alike URL / sponsored search ad / fake app | Bookmarks only. Never click links from DMs or ads |
| **Wallet drainer** | You sign an approval, Permit or `setApprovalForAll` for an attacker | Read every prompt. Burner wallet for new sites |
| **Address poisoning** | Attacker sends $0 transfers from an address that looks like one you use, so it appears in your history | Never copy addresses from history. Use a saved address book and check the *full* address |
| **Fake token / airdrop** | Unknown tokens appear in your wallet with a "claim" link | Ignore them. Don't interact or try to sell |
| **Impersonation** | "Support", "admin" or "project team" DMs you | Real teams never DM first and never ask for seeds |
| **Too-good yields** | New protocol, huge APY, anonymous team, no audit | Due diligence (Module 6). Burner wallet and small size, or skip |

### Worked example — address poisoning
You regularly send to `0x7a3F…9c21`. Today your history shows a transfer from
`0x7a3F…9c21`, but the full address is `0x7a3F`**`e0b4…d18`**`9c21`: same
start and end, different middle. If you copy it from history you send your
funds to the attacker. **Always paste from your address book and check the
full address.**

### Checklist
- [ ] Protocol sites bookmarked; never reached through search ads or DMs
- [ ] Address book in use; full address checked before sending
- [ ] Unknown tokens ignored
- [ ] DMs from "support" treated as scams by default
- [ ] New sites only with the burner wallet

### Quiz
<details><summary>1. A new token worth "$5,000" appears in your wallet with a claim site. What do you do?</summary>Ignore it. It's bait, and interacting risks a drainer approval.</details>
<details><summary>2. How does address poisoning trick people?</summary>It puts a look-alike address in your history so you copy it by mistake.</details>
<details><summary>3. What's the single best habit against drainers?</summary>Reading every signature and approval prompt, and using a burner wallet for anything new.</details>

---

### Module 1 practical
1. Set up the 3-wallet structure (vault / operator / burner).
2. Send a small test transaction and trace it on an explorer: status, fee, nonce.
3. Approve a small, limited allowance on a reputable protocol, then revoke it.
4. Write your stablecoin list with type, backing, who can redeem, and your depeg exit rule.

---

# Module 2 — Trading On-Chain

![Module 2 — Trading On-Chain](assets/modules/module-02.png)

*Outcome: execute a swap or LP position deliberately, understanding price impact, fees, impermanent loss and MEV.*
*Source: ATLAS "DeFi & On-Chain" ch. 6–9, 35. Educational content only. Not financial advice. Figures illustrative.*


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

## Lesson 2.2 — AMM Mathematics (x · y = k)

*Module 2 · Trading On-Chain · Source: ATLAS ch. 7*
*Template every lesson follows: Objective → Explanation → Worked example → Checklist → Quiz.*

> Educational content only. Not financial advice. Examples are illustrative.

### Objective
By the end of this lesson you can calculate what a swap will actually pay out
in a constant-product pool, and explain why bigger trades get worse prices.

### Explanation
A constant-product AMM holds two tokens in a pool. It doesn't use an order
book. It keeps one rule: **reserves of token A × reserves of token B = k**, and
k must stay constant (ignoring fees) after every trade.

- **Pool price** is the ratio of reserves. 100 ETH and 300,000 USDC means 1 ETH ≈ 3,000 USDC.
- When you add ETH to the pool, the pool must *remove* enough USDC to keep x·y = k.
- The more of the pool you move, the further the price moves against you. That gap is **price impact**.
- **Arbitrageurs** then trade the pool back in line with other markets, and that changes what LPs hold. You'll see why that matters in Lesson 2.4.

![How a constant-product swap is priced](assets/diagrams/amm-swap-flow.png)

### Worked example

![The x·y=k curve](assets/charts/amm-curve.png)

Pool: **100 ETH** and **300,000 USDC**, so k = 30,000,000. Spot price = 3,000 USDC/ETH.

You swap in **10 ETH** (fees ignored):
1. x' = 100 + 10 = 110
2. y' = 30,000,000 ÷ 110 ≈ 272,727
3. You receive 300,000 − 272,727 ≈ **27,273 USDC**
4. Effective price ≈ 27,273 ÷ 10 = **2,727 USDC/ETH**, which is **~9.1% worse** than spot.

Now try **1 ETH**: x' = 101 → y' ≈ 297,030 → you receive ≈ 2,970 USDC, which is ~1% worse.
Ten times the size cost about nine times more in price impact. **Size relative to
pool depth is what matters, not the size of the trade in dollars.**

### Checklist before any swap
- [ ] Check the price impact the interface shows; if it isn't shown, work it out
- [ ] Compare with an aggregator quote
- [ ] Set slippage tolerance on purpose (too tight: the swap fails; too loose: you get a bad fill or a sandwich attack, see 2.5)
- [ ] Split large trades or use deeper pools
- [ ] Run the before-signing checklist (chain, contract, token, amount, spender)

### Quiz
<details><summary>1. A pool holds 50 ETH / 150,000 USDC. What is k and the spot price?</summary>
k = 7,500,000; spot = 3,000 USDC/ETH.</details>

<details><summary>2. Why does a 10 ETH swap get a worse average price than a 1 ETH swap in the same pool?</summary>
Each unit you add moves the reserve ratio further, so later units in the same trade are priced worse. Price impact grows with trade size relative to reserves.</details>

<details><summary>3. Who moves the pool price back in line after your trade, and why does that matter to LPs?</summary>
Arbitrageurs do. Their trades rebalance what the LP holds, which is where impermanent loss comes from (Lesson 2.4).</details>

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

![Impermanent loss vs holding](assets/charts/impermanent-loss.png)

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

### Module 2 practical
1. Quote the same swap on a single DEX and an aggregator. Record the net output after gas for a small and a large size.
2. Pick a real pool and calculate its full-range fee APR from 30-day volume and TVL.
3. Model an LP entry with `defi_calc.py`: IL at ±25% and ±50%, and the fee APR needed to break even over 90 days.
4. Turn on protected routing in your wallet or aggregator and set a default slippage you can justify.

---

# DeFi Strategy Mastery — How Strategies Make (and Lose) Money

*On-Chain Operator Program · Strategy module · Built on ATLAS "DeFi & On-Chain" ch. 7–18, 38–42 and the 16-framework Strategy Library, expanded to 25 strategies.*

> **Read this first.** This is educational material, not financial advice.
> No DeFi strategy guarantees profit. Every return in DeFi is payment for
> taking a risk. This module shows **where each strategy's return comes from,
> the maths to test it before you enter, how to run it, and exactly how it
> loses money**, so you only keep positions whose expected return still makes
> sense after costs and risk. All numbers below are illustrative. Use live
> rates from protocol dashboards and independent data (e.g. DefiLlama) when
> you model a real position.

Calculator for every formula here:
`python3 .claude/skills/defi-strategies/scripts/defi_calc.py <command> --help`

---

## Part 1 — Where profit actually comes from

There are only five sources of return in DeFi. Every strategy is a mix of them.

![Where DeFi returns come from](assets/diagrams/profit-sources.png)

| # | Source | You are paid for… | Example | Lasts? |
|---|---|---|---|---|
| 1 | **Service fees** | providing liquidity traders need | swap fees to LPs | As long as volume lasts |
| 2 | **Interest** | lending capital borrowers need | stablecoin supply APY | As long as borrow demand lasts |
| 3 | **Security rewards** | staking to secure a network | ETH staking yield | Structural, but changes over time |
| 4 | **Structural carry** | taking the other side of crowded positioning | perp funding, basis | Comes and goes with the market |
| 5 | **Incentives** | bringing capital to a protocol | token emissions, points, airdrops | Temporary, and often dilutive |

Price moves (beta) are not a strategy. If a position only made money because
ETH went up, it was a directional bet with extra steps. Strategies 1–4 can pay
in flat markets. Source 5 is only real once the tokens are sold.

### The one equation that matters

```
Net return = base yield (fees + interest + staking)
           + incentives (valued at the price you can actually sell at)
           − impermanent loss / inventory loss
           − borrow cost
           − gas + swap + bridge costs
           − protocol / vault fees
           − losses from risk events
           ± price change on assets held
```

A position is only worth running if **net return beats the simplest
alternative** (holding the assets, or plain stablecoin lending) **by enough to
pay for the extra risk**. Masters compare against a benchmark. Beginners
compare against zero.

### APR vs APY
APY assumes compounding. `APY = (1 + APR/n)^n − 1`. 10% APR compounded daily ≈
10.52% APY, **but only if compounding is free**. On-chain, each compound costs
gas. Compound only when `pending rewards ≥ ~10–20× the gas cost`, or use a vault
that batches it (and charges a fee for doing so).

---

## Part 2 — Strategy selector by market regime

This uses the same thinking as the Grid Bot module: **pick the market regime
first, then the strategy.**

| Regime | Strategies that tend to work | Avoid / reduce |
|---|---|---|
| **Sideways, low–moderate volatility** | Concentrated LP around the range · stable-stable LP · lending · grid bots (CEX) | Leverage loops with thin buffers |
| **Uptrend** | Hold + liquid staking · delta-neutral funding carry (longs usually pay) · conservative borrow against collateral | Narrow LP ranges (they sell your winners early) |
| **Downtrend** | Stablecoin lending · stable-stable LP · cash management | Leveraged loops · volatile/volatile LP · incentive farms paid in falling tokens |
| **High volatility / event risk** | Wider LP ranges or none · larger health-factor buffers · smaller size | New positions right before major news (FOMC, CPI), new or unaudited protocols |

---

## Part 3 — The strategy playbook

![The strategy library: 25 strategies in 6 levels](assets/diagrams/strategy-levels.png)

Each strategy card has the same sections:
**Profit engine · Key maths · Execute · Monitor · Exit/kill rules · How it loses · Size cap**.
Size caps are suggested maximums as a share of the DeFi portfolio. Tighten
them to fit your own risk budget.

### LEVEL 1 — CORE (start here)

#### 1. Stablecoin lending
- **Profit engine:** interest paid by borrowers (source 2).
- **Key maths:** `supply APY ≈ borrow APY × utilisation × (1 − reserve factor)`.
  Example: 8% borrow × 80% utilisation × 0.9 = **5.76%**.
- **Execute:** pick a stablecoin with a clear peg mechanism (Module 1.5) → pick a
  lending market that passed due diligence (`defi-due-diligence`) → check
  current utilisation and withdrawal liquidity → supply → record the receipt token.
- **Monitor:** utilisation (above ~90% = withdrawals may be stuck), stablecoin
  peg, governance changes, incidents.
- **Exit/kill:** peg below ~0.99 for a sustained period, utilisation pinned at
  100%, exploit news, or the rate falls below your benchmark.
- **How it loses:** stablecoin depeg, protocol exploit, bad debt, frozen withdrawals.
- **Size cap:** can be the largest bucket, but **split across ≥2 independent
  protocols and ≥2 stablecoin issuers**.

#### 2. Native / liquid staking (LSTs)
- **Profit engine:** network security rewards (source 3), minus the provider's fee.
- **Key maths:** `net yield = staking APR × (1 − provider fee)`. Your real
  return is still dominated by the asset's price, so this only improves on
  holding if you'd hold the asset anyway.
- **Execute:** choose the provider (validator spread, fee, track record,
  redemption path) → stake → confirm how the LST earns (rebasing, or an
  exchange rate that rises).
- **Monitor:** LST/underlying ratio on markets (discount), validator
  incidents/slashing, withdrawal queue length.
- **Exit/kill:** discount widens beyond your threshold, a slashing event,
  or the provider's governance or custody changes.
- **How it loses:** asset price falls (main risk), LST depeg, slashing,
  smart-contract risk.
- **Size cap:** "hold-anyway" capital only.

#### 3. Borrowing against collateral (liquidity without selling)

![The liquidation cascade](assets/diagrams/liquidation-cascade.png)

- **Profit engine:** none by itself. It's a tool. The gain comes from what
  the borrowed funds do, or from not triggering a sale.
- **Key maths:**
  - `Health factor (HF) = Σ(collateral value × liquidation threshold) ÷ debt`
  - `Liquidation price = debt ÷ (collateral qty × liquidation threshold)`
  - Example: 10 ETH at $3,000, LT 0.80, borrow $12,000 → HF = 2.0 → liquidation at **$1,500** (−50%).
- **Execute:** borrow only enough that liquidation is beyond a move you'd
  realistically expect to survive (**HF ≥ 2 for volatile collateral** is a
  sane starting rule) → write the defence plan before borrowing.
- **Monitor:** HF daily, borrow rate, oracle price.
- **Exit/kill:** HF < 1.5 → repay or add collateral. Don't wait for 1.1.
- **How it loses:** liquidation penalty (commonly 5–10%+ of the collateral
  seized), borrow rate spikes, oracle issues.
- **Size cap:** debt ≤ what you could repay from outside the position.

### LEVEL 2 — LIQUIDITY

#### 4. 50/50 AMM liquidity (full range)

![Impermanent loss vs holding](assets/charts/impermanent-loss.png)

- **Profit engine:** swap fees (source 1), sometimes plus incentives.
- **Key maths — impermanent loss (IL) vs just holding**, where `r` = price ratio change:
  `IL = 2√r ÷ (1 + r) − 1`

  | Price change | 1.25× | 1.5× | 2× | 3× | 4× | 5× |
  |---|---|---|---|---|---|---|
  | IL vs holding | −0.6% | −2.0% | −5.7% | −13.4% | −20.0% | −25.5% |

  (Same IL whether price goes up or down by the same ratio. 0.5× = 2×.)
- **Break-even rule:** `fees earned over the holding period ≥ IL`.
  Example: expect up to a 1.5× move within 90 days → IL ≈ 2.0% → you need fee
  APR ≥ **~8.2%** just to match holding.
- **Execute:** pick a pair you're happy to own either side of → check real
  fee APR over 30 days (not the peak day) → deposit → record entry prices.
- **Monitor:** fees accrued vs IL vs "just hold" benchmark, weekly.
- **Exit/kill:** fees stop covering IL, volume dies, or the pair enters a strong trend.
- **How it loses:** strong trends (you end up holding more of the losing asset), low volume, token risk.

#### 5. Concentrated liquidity (the on-chain grid bot)
- **Profit engine:** swap fees on a chosen range. It's economically very close
  to a grid bot: it sells as price rises through the range and buys as it
  falls (Module 9).
- **Key maths:** capital efficiency vs full range (price at the geometric
  middle of the range) ≈ `1 ÷ (1 − (P_low / P_high)^¼)`.
  A ±10% range (P_high/P_low ≈ 1.22) is ~**20×** as capital-efficient, so it
  earns ~20× the fees per dollar *while in range*. IL is also amplified by
  about the same factor, and **out of range earns 0% and leaves you holding
  100% of one asset.**
- **Execute:** set the range from structure and volatility, exactly like a
  grid range (`grid-bot-design`: regime → range → invalidation) → wider in
  high volatility → decide the rebalance rule *before* entry.
- **Monitor:** % of time in range, fees vs IL, gas cost of each rebalance.
- **Exit/kill:** range invalidated (price breaks structure) → don't chase
  every move. Rebalancing too often locks in losses and burns gas.
- **How it loses:** trending markets, over-rebalancing, gas on small positions.
- **Size cap:** active capital only. Needs weekly (or better) attention.

#### 6. Stable-stable LP
- **Profit engine:** swap fees between similarly priced assets. Very low IL *while the pegs hold*.
- **Execute:** only pair stables you'd accept holding 100% of (in a depeg the
  pool fills up with the weaker coin).
- **Kill:** either stable trades below ~0.99, or the pool balance goes heavily one-sided.
- **How it loses:** depeg (you end up holding the broken coin), contract risk.

### LEVEL 3 — YIELD

#### 7. Auto-compounding vaults
- **Profit engine:** the underlying strategy, plus compounding without you paying the gas.
- **Key maths:** `net APY = gross APY − performance fee share − management fee`.
  Compare against doing it yourself: vaults win on small positions (gas) and
  lose on large ones (fees).
- **Due diligence:** vault contract + **every** protocol it deposits into
  (the risks stack). Read withdrawal limits and fees.
- **How it loses:** any protocol in the chain fails, strategy change by the vault operator, withdrawal limits.

#### 8. Incentive farming
- **Profit engine:** token emissions (source 5) on top of a base yield.
- **The rule:** value rewards at the price you can **actually sell at after
  slippage**, and assume the token price falls while emissions continue.
  Harvest and sell on a schedule (e.g. weekly) unless you'd buy the token with cash.
- **Quick test:** remove the incentive APR. If the base yield alone doesn't
  justify the risk, you're being paid in a token that's likely to keep falling.
- **How it loses:** reward token price collapse, mercenary liquidity leaving,
  IL on the underlying LP.

#### 9. Airdrops and points
- **Profit engine:** possible future token distribution.
- **Key maths:** `EV = P(airdrop) × expected value to you − (gas + bridge + opportunity cost + risk)`.
- **Rule:** only farm with actions you'd do anyway, or with capital you've
  capped as speculative. Claim only from verified links (scam defence, Module 1.6).

### LEVEL 4 — ADVANCED (only after Levels 1–3 are routine)

#### 10. Leveraged lending loop

![Leveraged loop: net APY vs borrow rate](assets/charts/loop-spread.png)

- **Profit engine:** amplifies a *positive spread* between collateral yield and borrow cost.
- **Key maths:**
  - Leverage after n loops at LTV L: `(1 − L^(n+1)) ÷ (1 − L)`, max `1 ÷ (1 − L)` (L = 0.7 → 3.33×)
  - `Net APY on equity = collateral yield × Lev − borrow rate × (Lev − 1)`
  - Example: 3.5% collateral yield, 2.5% borrow, 3× → **5.5%**. If borrow rises
    to 4.5% → **1.5%**. If it rises to 5.25% → **0%**. The spread is everything.
- **Execute:** only loop assets that move closely together (e.g. an LST
  against its underlying, or stable against stable) → stay well below max
  leverage → set HF alerts.
- **Kill:** spread turns negative, HF < your floor, depeg of the collateral.
- **How it loses:** borrow rate spikes (they can happen quickly), liquidation
  cascades, depeg of correlated collateral, unwind costs.

#### 11. LST collateral loop
Strategy 10 using an LST as collateral against its own underlying asset.
Liquidation risk depends mainly on the **LST/underlying ratio and on how the
protocol's oracle prices it**, less on the asset's price. Check which oracle
the market uses before assuming "it can't be liquidated".

#### 12. Delta-neutral funding carry
- **Profit engine:** perpetual funding (source 4). In bullish markets longs
  usually pay shorts. Hold spot long + perp short at equal size, so price
  moves roughly cancel and you collect funding.
- **Key maths:** `funding APR ≈ rate per 8h × 3 × 365`. 0.01%/8h ≈ **10.95% APR on the hedged size**.
  Return on *total capital* is lower because capital sits in both legs:
  $10k spot + $10k margin (1× short) → ~5.5% on $20k; 2× short ($5k margin)
  → ~7.3% on $15k, but the short gets liquidated if price rises ~50%.
- **Execute:** open both legs at the same time, at the same size → keep a
  margin buffer → track funding every period.
- **Kill:** funding negative for a sustained period (you now pay), margin
  buffer thin, venue risk.
- **How it loses:** funding flips negative, short-leg liquidation in a squeeze,
  execution slippage/basis, exchange/venue failure (CEX or perp DEX).

#### 13. LP hedge
Concentrated or 50/50 LP plus a partial perp short to offset its directional
exposure. The hedge ratio changes as price moves (LP inventory changes), so it
needs rebalancing. It narrows the P&L range but adds funding + execution cost.
Only worth doing if fees exceed IL + hedge cost.

### LEVEL 5 — TREASURY & RESEARCH

#### 14. DeFi cash management
Build a ladder for idle stablecoins: instant-access tier (lending), core tier
(split across protocols and issuers), and a cap per protocol. Goal: earn a
reasonable return on cash **without any single failure costing more than
you've decided you can afford to lose**.

#### 15–16. On-chain accumulation screen / protocol growth screen
Research, not yield. Track users, fees/revenue, TVL quality, holder
concentration, exchange flows and unlocks to decide *what* to hold or provide
liquidity for. Never act on one metric (ATLAS ch. 27–34).

---

### LEVEL 6 — PROFESSIONAL (structured, fixed and hedged yield)

These are the strategies professional desks and treasuries use. Each one
swaps a risk you don't want for one you've chosen, so **name what you're
short before you enter.** Full lessons: Module 10 (Advanced Yield
Engineering), Module 11 (Hedging) and Module 12 (Own Bank).

#### 17. Fixed-rate yield with principal tokens (PT)

![PT price converges to 1.00 at maturity](assets/charts/pt-convergence.png)

- **Profit engine:** yield tokenization splits a yield-bearing asset into a
  **principal token (PT)**, which redeems 1:1 for the underlying at maturity,
  and a **yield token (YT)**, which collects all the variable yield until then.
  Buying PT at a discount locks in a fixed return (source 2/3, bought forward).
- **Key maths:** `fixed APY = (1 ÷ PT price)^(365 ÷ days) − 1`.
  PT at 0.96 with 180 days left → **8.63%** fixed if held to maturity.
  `defi_calc.py pt --price 0.96 --days 180`
- **Execute:** pick a PT on an underlying you'd hold anyway → check pool depth
  (for early exit) → buy → hold to maturity → redeem.
- **Kill:** underlying depeg or exploit. You're still exposed to the underlying asset; the rate is fixed, the asset risk isn't.
- **How it loses:** underlying fails; selling before maturity at a worse price; illiquid PT pools.

#### 18. Yield tokens (YT): buying variable yield
- **Profit engine:** YT collects all yield (and often points) on the underlying until maturity, then goes to zero.
- **Key maths:** a YT costs ~`1 − PT price` (0.04 above). It profits only if
  **realised variable yield plus points beats the implied rate (~8.6%)**.
- **Use:** a speculative, time-decaying position. Size it as speculation.
- **How it loses:** yields fall, points turn out worthless; the YT is worth zero at maturity by design.

#### 19. Cash-and-carry basis
- **Profit engine:** dated futures often trade above spot in bull markets.
  Buy spot, short the future at the same size, and the premium (basis) converges to zero at expiry (source 4).
- **Key maths:** `annualised basis = (future ÷ spot − 1) × 365 ÷ days`.
  Spot 3,000, 90-day future 3,060 → 2% → **8.11%** annualised.
  `defi_calc.py basis --spot 3000 --future 3060 --days 90`
- **Execute:** open both legs together → keep enough margin that the short survives a large rally → hold to expiry.
- **How it loses:** short-leg margin call in a squeeze, venue/counterparty failure, closing early at a wider basis.

#### 20. Covered calls and options vaults
- **Profit engine:** sell upside you're willing to give away. The option premium is paid to you (source 4: selling volatility).
- **Key maths:** ETH at 3,000, sell a 7-day 3,300 call for 0.4% →
  **20.9%** annualised *if* repeated at that premium (it won't be exactly).
  Max gain per week = 0.4% + 10% = 10.4%. Break-even price 2,988.
  `defi_calc.py covered-call --spot 3000 --strike 3300 --premium 0.4`
- **Execute:** only on assets you'd hold anyway → strikes above levels you'd happily sell at → roll weekly or monthly.
- **How it loses:** the asset falls (the premium is a small cushion); you miss big rallies; options-vault contract risk.

#### 21. Cash-secured puts: getting paid to wait for a lower entry
- **Profit engine:** sell a put at a price you'd buy at anyway, holding the cash to pay for it.
- **Key maths:** sell a 2,700 put for $12 with $2,700 of stablecoins reserved
  → **0.44%** for the week on the cash. If assigned, your effective entry is **$2,688**.
- **How it loses:** price falls far below the strike (you buy at 2,688 while the market is lower); you miss the move if price rips upward.

#### 22. Fixed-rate borrowing
- **Profit engine:** none by itself. It's insurance on your cost of credit (Module 12.3).
- **Worked comparison:** borrow $50,000 for a year. Fixed at 6% costs **$3,000**.
  Variable at 4% for 9 months, then spiking to 12% for 3 months, costs
  50,000 × (4% × 0.75 + 12% × 0.25) = **$3,000**. Same cost, but fixed let you plan.
  If the spike lasted longer, variable costs more; if rates stayed at 4%, fixed cost $1,000 more.
- **Use:** when the borrowing funds something with a fixed payoff, or when a rate spike would force a bad sale.

#### 23. Being the lender: curated lending vaults
- **Profit engine:** supply stablecoins to a vault whose curator spreads them
  across isolated lending markets (source 2). You're the bank's depositor
  *and* its credit committee.
- **Key maths:** judge risk-adjusted, not headline: 7% headline with an
  assumed 2%/yr chance of a loss event losing half → **6.0%** risk-adjusted.
  `defi_calc.py expected --yield-apy 7 --loss-prob 0.02 --lgd 0.5`
- **Due diligence:** which markets, which collateral, which oracles, what
  liquidation LTVs, the curator's record, and how fast you can withdraw.
- **How it loses:** bad debt in any one market, oracle failure, curator error, withdrawal queues in stress.

#### 24. Hedged restaking / points farming
- **Profit engine:** hold a liquid restaking token (staking yield + points)
  and short the underlying perp to remove price exposure. When funding is
  positive, the short *receives* funding too.
- **Key maths:** `net ≈ staking yield + funding received + points value − costs`.
  **Value the points at zero for planning.** Anything they pay is upside.
- **How it loses:** the restaking token depegs from the asset you hedged with
  (the hedge doesn't cover that), slashing, funding turns negative, short-leg liquidation.

#### 25. The yield-covered credit line
- **Profit engine:** borrow against yield-bearing collateral where the collateral's yield pays the interest.
- **Key maths:** $200,000 of an LST at 3.2% earns **$6,400/yr**. A $40,000
  stablecoin loan at 5% costs **$2,000/yr**, so yield covers interest 3.2×.
  LTV 20%, health factor 4.0 at an 0.8 liquidation threshold.
  `defi_calc.py bank --collateral 200000 --debt 40000 --borrow-apy 5`
- **Use:** access to liquidity without selling, as a bank client would (Module 12.3).
- **How it loses:** the collateral price falls (the LTV rises even if the
  interest is covered), the borrow rate spikes above the yield, the LST depegs.

---

## Part 4 — Execution system (what turns strategies into results)

### Position sizing rules (starting point, tighten as needed)
- Max **20–25%** of DeFi capital in any one protocol. Max **10%** in anything
  unaudited, new (< 6 months) or reliant on a single bridge.
- Max **~30–40%** on any one non-Ethereum chain / L2.
- Keep **10–20%** instantly liquid (not in any position) to defend debt and
  take opportunities.
- Leverage: total debt small enough that a −50% market day doesn't liquidate anything.

### Before every entry (5 gates)
1. **Due diligence** file complete (`defi-due-diligence`: 6-step loop).
2. **Profit engine named.** Which of the 5 sources pays you?
3. **Maths done.** Net return after costs beats the benchmark (use `defi_calc.py`).
4. **Kill rules written down.** Exact numbers: HF floor, peg level, spread, range break.
5. **Before-signing checklist** (chain, contract, token, amount, spender, slippage, gas).

### Journal (one row per position)
Protocol · chain · strategy # · entry date · amount · entry prices · profit
engine · expected net APY · benchmark · kill rules · approvals granted ·
weekly: fees/interest earned, IL, costs, net vs benchmark.

### Review rhythm
- **Daily:** health factors, pegs, LP ranges, incident feeds.
- **Weekly:** net P&L vs benchmark per position, harvest and sell incentive
  tokens, revoke unused approvals.
- **Monthly:** cut the bottom performer when judged against its risk, rebalance buckets,
  simplify anything you can't explain in one sentence.

### Take profits and keep them
- Sweep realised yield to stablecoins or cold storage on a schedule. Rewards
  sitting in a farm are still exposed to the farm's risks.
- Compound only what still passes the 5 gates. Compounding into a
  deteriorating position is how gains are given back.
- Track **net realised gains** after all costs. That's the only number that counts.

---

## Part 5 — Progression path

| Stage | Strategies | Graduate when… |
|---|---|---|
| 1. Foundation | #1 stable lending, #2 staking | You can do the full before-signing checklist without notes |
| 2. Liquidity | #4 50/50 LP, #6 stable LP | You've tracked LP vs hold for 30+ days |
| 3. Active | #5 concentrated LP, #7 vaults, #8 farming | You can say how much of a position's return is fees, IL and incentives |
| 4. Leverage | #3 borrowing, #10–11 loops | You've written and rehearsed a defence plan |
| 5. Carry & hedging | #12 funding carry, #13 LP hedge | You understand perp margin, funding and venue risk |
| 6. Operator | #14 treasury + #15–16 research | Your portfolio has caps, a journal, and a review you actually run |
| 7. Professional | #17–21 fixed, basis and options yield · #22–25 credit and hedged yield | You can state what every position is short, and your stress test survives a −50% day |

---

## Part 6 — Mastery quiz

<details><summary>1. A farm shows 60% APY: 5% fees, 55% token emissions. What's your first question?</summary>
What does the base 5% pay me for the risk, and at what price can I actually sell the reward token? Judge the farm on base yield plus rewards valued at a realistic, falling price.</details>

<details><summary>2. ETH doubles while you're in a 50/50 ETH/USDC pool. How did you do vs holding?</summary>
About 5.7% behind holding, before fees. Fees need to exceed that for LPing to have been worth it.</details>

<details><summary>3. A loop earns 3.5% on collateral and pays 2.5% to borrow at 3×. What borrow rate wipes out the return?</summary>
0 = 3.5×3 − b×2 → b = 5.25%.</details>

<details><summary>4. Funding is +0.01% per 8 hours. What is the APR on the hedged size, and why is your return on capital lower?</summary>
~10.95%. Capital sits in both the spot leg and the perp margin, so the return on total capital is roughly half to three-quarters of that, depending on the short's leverage.</details>

<details><summary>5. Your concentrated LP just went out of range after a breakout. What's the operator move?</summary>
Treat it as a range invalidation, just as with a grid bot: follow the pre-written rule (re-centre with a wider range, or exit). Don't chase every move with narrow rebalances.</details>

---

*Operating rule: if you can't name the profit engine and explain the unwind,
don't enter the position.*

---

# Module 9 — DeFi vs Grid Bots

![Module 9 — DeFi vs Grid Bots](assets/modules/module-09.png)

*Outcome: choose the right tool for the market, and run both as one system.*
*New content linking the On-Chain Operator Program to Grid Bot Builder. Educational only. Not financial advice. All figures illustrative.*

---

## Lesson 9.1 — Same idea, different machine

### Objective
Explain why a concentrated liquidity position and a grid bot are
economically close cousins, and where they differ.

### Explanation
Both strategies do the same basic thing inside a price range:
**sell as price rises, buy as price falls, and profit from price moving back and forth.**

| | Grid bot (e.g. Grid Bot Builder on an exchange) | Concentrated LP (on-chain AMM) |
|---|---|---|
| How it trades | Discrete orders at set levels | Continuous. Every trade in range moves your inventory |
| What it earns | Spread between grid levels, minus exchange fees | Share of the pool's swap fee on every trade in range |
| Who pays whom | You pay trading fees | Traders pay *you* fees |
| At the range low | Holds mostly/all the base asset | Holds 100% of the base asset |
| At the range high | Holds mostly/all quote (USDT/USDC) | Holds 100% of the quote asset |
| Outside the range | Stops trading, holding one side | Stops earning, holding one side |
| Custody | Exchange holds funds (you keep API control) | You hold keys, and the contract holds the position |
| Main extra risk | Exchange / counterparty | Smart contract, oracle, MEV, gas |
| Automation | Built into the tool | Manual, or a third-party manager (extra contract risk) |

### Worked example — same range, same inventory behaviour

![Grid bot vs concentrated LP](assets/diagrams/grid-vs-lp.png)

Range **$2,700–$3,300**, ETH at **$3,000**.

**Price falls to $2,700:**
- *Grid* (20 arithmetic levels, $30 apart): buys at 2,970, 2,940 … 2,700 → average buy ≈ **$2,835**.
- *Concentrated LP:* converts USDC to ETH continuously on the way down at the
  geometric average `√(2,700 × 3,000)` ≈ **$2,846**.

**Price rises to $3,300:**
- *Grid*: sells at 3,030 … 3,300 → average ≈ **$3,165**.
- *LP:* sells ETH at `√(3,000 × 3,300)` ≈ **$3,146**.

Almost the same inventory path. The real difference is **how money is made on
the way**: grid profit per completed level (after paying fees), versus LP fee
income on all trading volume in range (after impermanent loss).

### Checklist
- [ ] I can explain why both end up 100% in one asset at a range edge
- [ ] I know which one pays fees and which one earns them
- [ ] I treat a range break as an invalidation event in both

### Quiz
<details><summary>1. Price breaks below the range. What do the grid bot and the LP both hold?</summary>All, or nearly all, the base asset, bought on the way down. Both stop earning until price returns or you act.</details>
<details><summary>2. Who pays trading fees in each?</summary>The grid bot pays exchange fees. The LP earns fees from traders.</details>
<details><summary>3. Name one risk the LP has that the grid bot doesn't, and vice versa.</summary>LP: smart-contract/MEV/gas risk. Grid bot: exchange/counterparty risk.</details>

---

## Lesson 9.2 — When each one wins

### Objective
Pick grid bot, LP, both, or neither, for a given market and account.

### Explanation
| Factor | Favours grid bot | Favours on-chain LP |
|---|---|---|
| Position size | Small–medium (no gas per action) | Larger (gas becomes a smaller share of returns) |
| Pair | Major pairs listed on your exchange | Tokens only traded on-chain; pairs with deep pool volume |
| Fee economics | Low maker fees on your exchange | High-volume pools with a good fee tier (e.g. 0.05% / 0.3% / 1%) |
| Management | Want automation (Grid Bot Builder) | Happy to set ranges and rebalance by hand |
| Custody preference | Comfortable with exchange custody | Want self-custody |
| Counterparty view | Trust the exchange more than contracts | Trust audited contracts more than an exchange |
| Leverage wanted | Futures grid (advanced) | Not applicable (LP is unlevered unless you borrow) |

**Neither**, same as in the grid module: strong breakouts, parabolic moves,
major news, thin liquidity. Waiting is a position.

### Worked example — three traders
1. **$3k, trades BTC/ETH, wants automation** → grid bot. Gas would eat a small on-chain LP.
2. **$80k, holds ETH long-term, self-custody, checks weekly** → a wide-range
   ETH/USDC concentrated LP could earn fees on part of the stack. Size it as
   ETH they're willing to sell higher and USDC they're willing to spend lower.
3. **A token that's only liquid on a DEX** → only an LP is possible. Apply
   full due diligence (Module 6) and small size.

### Checklist
- [ ] I've matched the tool to position size, pair, custody and management time
- [ ] I've compared expected fee income to costs (gas or exchange fees)
- [ ] I've checked the regime before choosing either

### Quiz
<details><summary>1. Why does position size matter more on-chain?</summary>Gas is a roughly fixed cost per action, so it's a bigger percentage of a small position.</details>
<details><summary>2. When is an LP the only option?</summary>When the pair trades only on-chain.</details>
<details><summary>3. Market just broke out on huge news. Grid or LP?</summary>Neither, until a new range forms.</details>

---

## Lesson 9.3 — Building a combined system

### Objective
Design a portfolio that uses exchange grid bots and DeFi together without
doubling up on the same risk.

### Explanation
Each tool is good at a different job:
- **Grid bots** → capture oscillation in range-bound major pairs, fully automated.
- **DeFi lending / stable LP** → earn on idle stablecoins and reserves.
- **Staking / LSTs** → earn on assets you'd hold anyway.
- **Concentrated LP** → earn fees on-chain in ranges, for larger, self-custodied sizes.

**The trap: correlation.** An ETH grid bot + an ETH/USDC LP + an LST loop are
*three* bets on ETH staying in a range. If ETH breaks down, they all lose
together. Add up your exposure by **underlying asset and by range**, not by
number of positions.

### Worked example — an illustrative allocation framework
*Percentages are an example structure, not a recommendation. Set your own from your risk budget.*

| Bucket | Share | Tool | Job |
|---|---|---|---|
| Reserve | 15% | Stablecoin lending (split across 2 protocols) | Liquidity to defend positions and redeploy after range breaks |
| Core yield | 25% | Stable-stable LP / stable lending | Base return on cash |
| Hold-anyway assets | 25% | Staking / LSTs | Earn on long-term holdings |
| Range income | 30% | Grid bots on liquid majors (+ optional wide on-chain LP) | Capture oscillation |
| Speculative | ≤5% | Burner-wallet farms, airdrops, new protocols | Capped experiments |

Rules for this system:
1. **One range thesis per asset.** If a grid bot and an LP both run on ETH, their combined size must fit your ETH range-risk cap.
2. **Reserve funds the defence.** Range breaks and health-factor defence draw from reserve, never from other positions.
3. **Sweep profits up.** Realised grid profits and harvested yield go to reserve or vault on a schedule.
4. **Review together.** One weekly review across CEX and on-chain positions, using the same journal.

### Checklist
- [ ] Exposure added up by underlying asset, not by bot/position count
- [ ] Reserve sized and kept out of positions
- [ ] Profit sweep schedule set
- [ ] One journal covering bots and DeFi positions

### Quiz
<details><summary>1. ETH grid bot + ETH/USDC LP + ETH LST loop. How many independent bets?</summary>Essentially one: ETH staying in range or rising. They're correlated.</details>
<details><summary>2. What is the reserve for?</summary>Defending debt positions and redeploying after invalidations, without forced selling.</details>
<details><summary>3. Why sweep profits out of positions?</summary>Profits left in a position stay exposed to its risks. Sweeping locks them in.</details>

---

### Module 9 next step
- **Not a Grid Bot Builder customer yet?** Grid Bot Builder automates the "range
  income" bucket on your exchange: self-serve, delivered instantly. → Checkout link on the program page.
- **Want daily range and market intel?** Elite Intel Community: 3-day free trial → elite-intel-community.whop.site

---

# Module 10 — Advanced Yield Engineering

![Module 10 — Advanced Yield Engineering](assets/modules/module-10.png)

*Outcome: build fixed, hedged and structured yield, and know exactly what each position is short.*
*Stage 4 · Strategist. Prerequisites: Modules 1–9. Educational content only. Not financial advice. Figures are illustrative; use live rates.*

**The professional's rule for this module:** every structured position swaps
one risk for another. Before entering, write one sentence: *"This position
is short ___."* If you can't fill the blank, you're not ready to enter.

---

## Lesson 10.1 — Fixed-rate yield: principal and yield tokens (PT/YT)

### Objective
Lock a fixed return using principal tokens, and price a yield token against its implied rate.

### Explanation
**Yield tokenization** takes a yield-bearing asset (a staked asset, a lending
receipt, a stablecoin savings token) and splits it into two tokens that
mature on a set date:

- **PT (principal token):** redeems 1:1 for the underlying at maturity. It
  trades at a **discount** before then. Buy the discount, hold to maturity,
  and your return is fixed.
- **YT (yield token):** receives *all* the variable yield (and often points)
  the underlying earns until maturity, then is worth zero.

PT + YT = one unit of the underlying. The PT price implies a fixed rate; the
YT is a bet that realised yield beats it.

`fixed APY = (1 ÷ PT price)^(365 ÷ days) − 1`

![PT price converges to 1.00 at maturity](assets/charts/pt-convergence.png)

### Worked example
A stablecoin savings token has a PT maturing in **180 days**, priced at **0.96**.
- `defi_calc.py pt --price 0.96 --days 180` → **8.63%** fixed APY if held to maturity.
- $100,000 buys ~104,167 PT → redeems for ~104,167 of the underlying at maturity.
- The YT costs ~0.04 per unit. It only profits if the underlying's realised
  yield (plus any points) averages above ~8.6% for the 180 days.

**Near maturity, small discounts are big rates:** PT at 0.985 with 60 days left
→ **9.63%** APY. Check liquidity before chasing these; exiting early means
selling into the pool.

### What this position is short
PT: the underlying's credit/depeg risk, and liquidity if you exit early.
YT: falling yields, and time (it decays to zero).

### Checklist
- [ ] I'd hold the underlying asset anyway
- [ ] Maturity date matches when I'll need the money (Module 12.4 ladder)
- [ ] Pool depth checked for an early exit
- [ ] YT sized as speculation, not income

### Quiz
<details><summary>1. PT at 0.97, 120 days to maturity. Fixed APY?</summary>(1/0.97)^(365/120) − 1 ≈ 9.7%.</details>
<details><summary>2. Does buying PT remove the underlying's risk?</summary>No. It fixes the rate. If the underlying depegs or is exploited, the PT redeems into a damaged asset.</details>
<details><summary>3. What must happen for a YT to profit?</summary>Realised variable yield plus points must beat the implied rate priced into the PT.</details>

---

## Lesson 10.2 — Cash-and-carry basis trades

### Objective
Capture the premium of a dated future over spot without taking a view on price.

### Explanation
In rising markets, dated futures usually trade **above** spot. The gap (basis)
shrinks to zero at expiry because the future settles at spot.
**Buy spot + short the future at the same size** and you lock that gap,
whatever the price does, as long as both legs survive to expiry.

`annualised basis = (future ÷ spot − 1) × 365 ÷ days`

### Worked example
ETH spot **3,000**, 90-day future **3,060**.
- Basis = 2.0% → **8.11%** annualised (`defi_calc.py basis --spot 3000 --future 3060 --days 90`).
- At expiry, if ETH is 2,000: spot leg −1,000, short future +1,060 → +60 per ETH.
- At expiry, if ETH is 4,500: spot leg +1,500, short future −1,440 → +60 per ETH.
- **The catch:** before expiry, a rally to 4,500 means the short leg shows
  −1,440 per ETH. Without enough margin on the futures venue, it's closed out
  and you're left long spot at the top.

### What this position is short
Margin and venue risk: a squeeze on the short leg, or the venue failing.

### Checklist
- [ ] Both legs opened together, same size
- [ ] Futures margin survives at least a +100% move, or a rule to top up
- [ ] Venue risk sized (cap per venue)
- [ ] Plan to hold to expiry; early exit may be at a worse basis

### Quiz
<details><summary>1. Spot 2,000, 180-day future 2,080. Annualised basis?</summary>4% × 365/180 ≈ 8.1%.</details>
<details><summary>2. Why is the return "locked" at expiry?</summary>The future settles at spot, so the gain on one leg offsets the loss on the other, leaving the entry basis.</details>
<details><summary>3. What breaks the trade before expiry?</summary>A margin call or liquidation on the short future during a rally, or venue failure.</details>

---

## Lesson 10.3 — Delta-neutral funding carry, done properly

### Objective
Run a funding-carry position with proper sizing, venue limits and exit rules.

### Explanation
Perpetual futures pay **funding** between longs and shorts to keep the perp
near spot. In bullish markets longs usually pay shorts. Long spot + short
perp at the same size = no net price exposure, while collecting funding.

Professional rules:
1. **Measure funding over time, not today.** Use a 7- and 30-day average.
2. **Exit rule:** close when the 7-day average turns negative (you'd start paying).
3. **Margin buffer:** the short leg's leverage decides how big a rally it survives.
4. **Venue limits:** split across venues; cap each one.

### Worked example
Funding **+0.01% per 8h** ≈ **10.95% APR** on the hedged size.
| Short-leg leverage | Capital per $1 hedged | Return on capital | Short liquidates on a rally of roughly |
|---|---|---|---|
| 1× | $2.00 | ~5.5% | +100% |
| 2× | $1.50 | ~7.3% | +50% |
| 3× | $1.33 | ~8.2% | +33% |

`defi_calc.py carry --rate-8h 0.01 --short-lev 3`

Higher leverage improves return on capital a little and makes the position
much more fragile. Most operators stay at 1–2× and top up margin from reserve.

### What this position is short
Funding turning negative, short squeezes, and venue failure.

### Checklist
- [ ] 7- and 30-day funding averages checked
- [ ] Exit rule written (e.g. 7-day average < 0)
- [ ] Short-leg leverage ≤ 2×, top-up plan from reserve
- [ ] Per-venue cap set

### Quiz
<details><summary>1. Funding is +0.005%/8h. APR on hedged size?</summary>≈ 5.5%.</details>
<details><summary>2. Why not run the short at 5×?</summary>A ~20% rally would liquidate the short and leave you unhedged long.</details>
<details><summary>3. What's the exit signal?</summary>Average funding turning negative, meaning shorts start paying.</details>

---

## Lesson 10.4 — Options income: covered calls, cash-secured puts, options vaults

### Objective
Earn option premium on assets you'd hold or buy anyway, knowing exactly what you give up.

### Explanation
- **Covered call:** you hold the asset and sell someone the right to buy it
  from you at a higher **strike**. You keep the premium, and your upside is capped at the strike.
- **Cash-secured put:** you hold stablecoins and sell someone the right to sell
  you the asset at a lower strike. You keep the premium. If price falls below
  the strike, you buy at the strike.
- **The wheel:** sell puts until assigned → hold the asset → sell calls until
  called away → repeat.
- **Options vaults** automate this on-chain. They add contract risk and you
  don't choose the strikes.

### Worked example
ETH at **3,000**.
- **Covered call:** sell a 7-day **3,300** call for **0.4%** ($12).
  ≈ **20.9%** annualised *if* repeated at that premium, which it won't be exactly.
  Max gain for the week 10.4%. Break-even **2,988**.
  `defi_calc.py covered-call --spot 3000 --strike 3300 --premium 0.4`
- **Cash-secured put:** sell a 7-day **2,700** put for **$12** with $2,700 reserved
  → **0.44%** on the cash for the week. If assigned, effective entry **$2,688**.

### What this position is short
Covered call: upside above the strike, plus the full downside of the asset.
Cash-secured put: a crash through the strike.

### Checklist
- [ ] Only on assets I'd hold (calls) or buy at the strike (puts)
- [ ] Strike chosen from levels, not from the premium
- [ ] Annualised premium treated as "if repeated", never promised
- [ ] Vault due diligence done if automating

### Quiz
<details><summary>1. What do you give up by selling a covered call?</summary>Gains above the strike for that period.</details>
<details><summary>2. Put strike 2,700, premium $15. Effective entry if assigned?</summary>$2,685.</details>
<details><summary>3. Does premium protect you in a crash?</summary>Only by the size of the premium. The asset's downside remains.</details>

---

## Lesson 10.5 — Active concentrated-liquidity management

### Objective
Choose a range width and a rebalance rule that fee income can actually pay for.

### Explanation
Narrower ranges earn more fees per dollar *while in range* and go out of range sooner.

| Range around $3,000 | Capital efficiency vs full range |
|---|---|
| $2,400–$3,600 (±20%) | ~10.4× |
| $2,700–$3,300 (±10%) | ~20.4× |
| $2,850–$3,150 (±5%) | ~40.5× |

`defi_calc.py cl --low 2850 --high 3150`

Every rebalance costs gas and swap fees and **locks in** the impermanent loss
so far. Professionals set a rule before entering:
- **Width from volatility:** at least ~1.5× the typical weekly move.
- **Rebalance trigger:** out of range for 24h+, *and* the range thesis still holds.
- **Invalidation:** a structural break (as with a grid bot) means exit, not re-centre.
- **Budget:** rebalancing costs capped at a share of expected fees (e.g. ≤ 25%).

### Worked example
ETH typically moves ±7% a week. A ±5% range would be out of range most
weeks. The rule points to **±10–12%**: ~20× efficiency, and time in range to earn.

### What this position is short
Trending markets and volatility above what the range was sized for.

### Checklist
- [ ] Width ≥ 1.5× typical weekly move
- [ ] Rebalance trigger and invalidation written
- [ ] Rebalance cost budget set
- [ ] P&L tracked against holding (Lesson 2.4)

### Quiz
<details><summary>1. Why does a ±5% range earn ~2× the fees of ±10% while in range?</summary>The same capital is concentrated in half the price range, so it provides about twice the liquidity there.</details>
<details><summary>2. What does a rebalance lock in?</summary>The impermanent loss accrued so far, plus gas and swap costs.</details>
<details><summary>3. Price breaks structure and exits the range. Re-centre?</summary>No. That's an invalidation. Exit per plan.</details>

---

## Lesson 10.6 — Restaking and points: pricing speculative yield

### Objective
Value restaking and points programmes without letting unknown rewards drive position size.

### Explanation
Restaking reuses staked assets to secure more services, paying extra rewards
and often **points**: an off-chain score that may or may not become a token.
The risk stack grows at each layer: staking → liquid restaking token →
restaking protocol → each service it secures → slashing conditions.

Professional rules:
- **Plan with points at zero.** Base the decision on yield you can measure.
- **Treat points as an airdrop bet:** `EV = P(payout) × value − costs`.
- **Hedge price if you only want the yield:** short the underlying perp (strategy #24), knowing the hedge doesn't cover a depeg of the restaking token.
- **Cap it:** speculative bucket only (≤ 5–10% of DeFi capital).

### Worked example
$20,000 in a liquid restaking token: base staking yield ~3% ($600/yr).
Points: you estimate a 30% chance of a payout worth $1,500, costing $200 in
gas and bridging: `defi_calc.py airdrop --probability 0.3 --value 1500 --costs 200`
→ EV **$250**. Worth doing only if the position still makes sense at $600/yr
and the risk stack is acceptable.

### What this position is short
Slashing, depeg of the restaking token, and the chance that points never become anything.

### Checklist
- [ ] Decision still works with points valued at zero
- [ ] Full risk stack written, layer by layer
- [ ] Sized inside the speculative bucket
- [ ] Hedge (if any) and its gap understood

### Quiz
<details><summary>1. Why value points at zero?</summary>They're not guaranteed to become anything, so a decision that needs them is a speculation.</details>
<details><summary>2. What does a perp hedge on the underlying miss?</summary>The restaking token depegging from the underlying.</details>
<details><summary>3. Name three layers of the restaking risk stack.</summary>Any three: staking/validators, the liquid restaking token, the restaking protocol, each service secured, slashing conditions.</details>

---

### Module 10 practical
1. Price three live PTs with `defi_calc.py pt` and choose the one whose maturity fits your liquidity ladder.
2. Paper-trade a basis position: record entry basis, margin, and the rally it would survive.
3. Write the "this position is short ___" sentence for every strategy in this module.
4. Size a concentrated LP range from a real asset's weekly volatility and write its rebalance rule.

---

# Module 12 — Operate as Your Own Bank

![Module 12 — Operate as Your Own Bank](assets/modules/module-12.png)

*Outcome: run your crypto the way a bank runs its book: a balance sheet, a custody policy, a credit line, a liquidity ladder, a lending desk and records someone else could follow.*
*Stage 5 · Operator. Prerequisites: Modules 1–11. Educational content only. Not financial, tax or legal advice. Figures are illustrative.*

A bank does four things: it **keeps assets safe**, **lends**, **borrows**,
and **manages liquidity** so it can always meet what it owes. DeFi lets you
do all four yourself, with no one to call when something goes wrong. This
module turns that into written policy.

![Operate as your own bank](assets/diagrams/own-bank.png)

---

## Lesson 12.1 — Your balance sheet

### Objective
Build a personal on-chain balance sheet and read the three numbers that matter: equity, LTV and liquidity runway.

### Explanation
- **Assets:** everything you own, at market value: collateral, yield positions, reserves.
- **Liabilities:** everything you owe: loans, margin, any payables.
- **Equity** = assets − liabilities. This is what's actually yours.
- **LTV** = debt ÷ collateral. Your bank's leverage.
- **Liquidity runway** = liquid reserve ÷ monthly obligations (spending + interest).

Banks fail from **liquidity** (can't pay today) more often than from
**solvency** (owe more than they own). Track both.

### Worked example
$300,000 collateral, $60,000 debt at 5%, $40,000 stablecoin reserve, $5,000/month spending:

`defi_calc.py bank --collateral 300000 --debt 60000 --borrow-apy 5 --reserve 40000 --monthly-spend 5000`
- Equity **$280,000** · LTV **20%** · health factor **4.0**
- Obligations $5,250/month ($250 of it interest) → reserve covers **7.6 months**
- Policy checks: LTV ≤ 30% ✓ · HF ≥ 2 ✓ · reserve ≥ 6 months ✓

### Checklist
- [ ] Balance sheet updated weekly
- [ ] Equity, LTV and runway tracked over time
- [ ] Policy limits written (max LTV, min HF, min runway)

### Quiz
<details><summary>1. Assets $500k, debt $100k. Equity?</summary>$400k.</details>
<details><summary>2. Reserve $30k, obligations $6k/month. Runway?</summary>5 months, below a 6-month policy.</details>
<details><summary>3. Why track liquidity separately from equity?</summary>You can be solvent and still be forced to sell at the worst time if you can't meet obligations today.</details>

---

## Lesson 12.2 — Custody architecture: vault, multisig and spending policies

### Objective
Design custody so that no single lost device, stolen key or mistaken signature can drain the bank.

### Explanation
Scale Module 1's three wallets into a bank-grade setup:

| Tier | Holds | Control | Rules |
|---|---|---|---|
| **Vault** | Most of your equity | **Multisig**, e.g. 2-of-3 hardware keys in separate locations | No DeFi approvals. Moves only to the Operating tier, to allowlisted addresses |
| **Operating** | Active positions | Hardware wallet or a smart account with limits | Verified protocols only. Spending limit per day |
| **Hot** | Small float | Hot wallet | Anything new or experimental. Refilled on schedule |

Smart-account features to use where available:
- **Spending limits** per day/week
- **Allowlists** (it can only send to addresses you pre-approved)
- **Timelocks** on large moves (a delay you can cancel if it wasn't you)
- **Recovery** paths agreed and tested in advance

![Custody architecture](assets/diagrams/custody-architecture.png)

### Worked example
Vault: 2-of-3 multisig, with key A at home, key B in a safe-deposit box and
key C with a trusted person or a professional co-signer. Losing any one key
is survivable; stealing any one key is useless. **Test it:** move $10 through
every path once a quarter.

### Checklist
- [ ] Vault is multisig; keys in separate physical locations
- [ ] Operating tier has a daily limit
- [ ] Allowlist on vault outflows
- [ ] Quarterly recovery test done and logged

### Quiz
<details><summary>1. Why 2-of-3 rather than 1-of-1?</summary>One key can be lost or stolen without losing the funds or giving an attacker control.</details>
<details><summary>2. What does a timelock buy you?</summary>Time to notice and cancel an unauthorised large move.</details>
<details><summary>3. Why test recovery with a small amount?</summary>A recovery plan you've never run is an assumption. Testing proves every key and path works.</details>

---

## Lesson 12.3 — The credit line: borrowing like a bank client

### Objective
Use your assets as collateral for liquidity without selling, under a written credit policy.

### Explanation
Wealthy clients rarely sell appreciating assets to raise cash; they borrow
against them. DeFi money markets offer the same: deposit collateral, borrow
stablecoins, repay when it suits you, with no credit check. **The collateral
is liquidated if you breach the threshold**, and nobody calls first.

**A credit policy (write yours):**
- Max LTV **25–30%** on volatile collateral (liquidation is often near 80%+)
- Health factor floor **2.5**; act at **2.0**
- Prefer collateral whose **yield covers the interest** (strategy #25)
- Consider **fixed-rate** borrowing when a rate spike would force a sale (strategy #22)
- **Repayment source** named before borrowing (income, reserve, maturing PT)
- Tax treatment of borrowing varies by country: **check with a tax professional**

### Worked example
$200,000 of liquid-staked ETH earning 3.2% ($6,400/yr). Borrow **$40,000** stablecoins at 5% ($2,000/yr).
- Yield covers interest **3.2×**. LTV 20%. HF **4.0** at a 0.8 threshold.
- ETH would have to fall **~75%** before liquidation (HF falls in proportion to price).
- Defence plan: at HF 2.0, repay from reserve; at HF 1.7, sell part of the collateral deliberately rather than let a liquidator do it at a penalty.

### Checklist
- [ ] Credit policy written: max LTV, HF floor, action levels
- [ ] Repayment source named
- [ ] Alerts set at the action levels (Module 14.1)
- [ ] Fixed vs variable decision made on purpose

### Quiz
<details><summary>1. Why borrow against assets instead of selling them?</summary>You keep the asset and its upside (and in some jurisdictions avoid a taxable sale), at the cost of interest and liquidation risk.</details>
<details><summary>2. HF is 4.0. Roughly how far can collateral fall before liquidation?</summary>About 75%, since HF scales with collateral price (HF 1.0 at a quarter of the current price).</details>
<details><summary>3. What should happen at your action level?</summary>Repay or add collateral per the written plan. Sell deliberately before a liquidator does it at a penalty.</details>

---

## Lesson 12.4 — Treasury and the liquidity ladder

### Objective
Structure reserves so money is available when it's needed, earning a return at every tier.

### Explanation
Banks match the timing of assets to the timing of what they owe. Your ladder:

| Tier | Access | Holds | Size (example: $5,000/month spend) |
|---|---|---|---|
| **T0 Instant** | Seconds | Stablecoins in the operating wallet | 1 month: $5,000 |
| **T1 Same day** | Hours | Blue-chip stablecoin lending, split across 2 protocols | 5 months: $25,000 |
| **T2 Term** | Scheduled | PTs maturing on dates you'll need the money (Lesson 10.1) | Next 6–12 months of planned spending |
| **T3 Growth** | Days–weeks | Strategy positions, LPs, staking | The rest, within caps |

![The liquidity ladder](assets/diagrams/liquidity-ladder.png)

Refill downward on a schedule: T1 tops up T0 monthly; maturing PTs top up T1.
Never fund a T0 need by selling a T3 position in a bad market. That's what the
ladder exists to prevent.

### Worked example
T0 $5,000 + T1 $25,000 = **6 months** instantly available. T2 holds three PTs
maturing in 3, 6 and 9 months, each sized for 3 months of spending. A −50%
market day touches none of it.

### Checklist
- [ ] T0 + T1 ≥ 6 months of obligations
- [ ] T2 maturities matched to planned spending
- [ ] Monthly refill schedule set
- [ ] T3 never used for day-to-day needs

### Quiz
<details><summary>1. Why hold T0 in plain stablecoins earning little?</summary>Instant, certain access. It's the tier that pays today's bills without selling anything.</details>
<details><summary>2. What's T2 for?</summary>Known future spending, with maturities matched to when the money is needed and a fixed return locked in.</details>
<details><summary>3. What does the ladder prevent?</summary>Forced selling of growth positions at bad prices to meet short-term needs.</details>

---

## Lesson 12.5 — Being the lender: supplying, curating and pricing credit risk

### Objective
Act as the lending side of the bank: choose markets, price the risk, and know when to pull liquidity.

### Explanation
When you supply to a money market, you're the bank's depositor, and
effectively its credit desk. Your return:
`supply APY ≈ borrow APY × utilisation × (1 − reserve factor)`.

Modern designs split lending into **isolated markets** (one collateral, one
loan asset, one oracle, one liquidation LTV). **Curated vaults** spread
deposits across several of these; the curator decides the allocation.

What a lender must check:
- **Collateral quality and liquidation LTV:** the higher the LTV, the thinner the buffer before bad debt
- **Oracle:** what prices the collateral, and can it be manipulated? (Module 5.3)
- **Utilisation:** near 100% means you may not be able to withdraw
- **Curator:** track record, how allocations are changed, timelocks
- **Risk-adjusted return**, not headline

### Worked example
Vault A: 7% headline, exposure to newer collateral; you assume a 2%/yr chance of a loss event losing half the deposit → **6.0%** risk-adjusted.
Vault B: 4.5% headline, blue-chip collateral; 0.5%/yr, total loss assumed → **4.0%**.
`defi_calc.py expected --yield-apy 7 --loss-prob 0.02 --lgd 0.5`

A pays more after the haircut, *if* your loss estimates are honest. Split
between them, and cap A lower because its tail is fatter and less known.

### Checklist
- [ ] Every market's collateral, oracle and LTV listed
- [ ] Loss probability and loss-given-default written down (your assumptions)
- [ ] Utilisation alert (e.g. > 90%)
- [ ] Per-vault and per-curator caps

### Quiz
<details><summary>1. Borrow APY 10%, utilisation 70%, reserve factor 10%. Supply APY?</summary>6.3%.</details>
<details><summary>2. Why is utilisation at 100% a lender's problem?</summary>All liquidity is lent out, so withdrawals wait until borrowers repay or new deposits arrive.</details>
<details><summary>3. What's a curated vault's extra risk?</summary>The curator's allocation decisions and permissions, on top of each market's risk.</details>

---

## Lesson 12.6 — Books, records and succession

### Objective
Keep books a stranger could follow, and make sure your family could recover everything if you couldn't.

### Explanation
**Books** (update weekly from your journal, Module 8):
- Every position: protocol, chain, contract, amount, entry date and price, cost basis
- Every loan: collateral, debt, rate, HF, action levels
- Every approval granted, and when it was revoked
- Income received, by source and date
- Keep exportable records for tax. Rules differ by country, so **use a crypto-aware tax professional.**

**Succession:** self-custody means that if you're gone and nobody can sign,
the money is gone too.
- A **letter of instruction** that explains the setup (wallets, multisig, where
  the documents are, who to contact), **stored separately from any seed or key**
- Multisig with a trusted co-signer or professional service, so recovery doesn't depend on one person
- Legal documents (will, powers of attorney) that reference the digital assets: **use a lawyer**
- **Annual drill:** walk a trusted person through the letter without revealing secrets

### Worked example
A 2-of-3 vault: you hold two keys (home + safe-deposit box); a professional
co-signer holds the third under an agreed recovery process. Your letter of
instruction, stored with your will, explains how your executor works with
the co-signer. No single document contains enough to steal the funds.

### Checklist
- [ ] Books current within a week
- [ ] Tax records exportable; professional engaged
- [ ] Letter of instruction written and stored apart from keys
- [ ] Annual succession drill done

### Quiz
<details><summary>1. Why keep the letter of instruction apart from seeds and keys?</summary>So finding the letter isn't enough to steal the funds.</details>
<details><summary>2. What's the risk of single-key self-custody for your family?</summary>If you can't sign and no one else can, the assets are unrecoverable.</details>
<details><summary>3. What goes in the books for each loan?</summary>Collateral, debt, rate, health factor and your action levels.</details>

---

### Module 12 practical: your bank's founding documents
1. Balance sheet with equity, LTV and runway (`defi_calc.py bank`).
2. Custody policy: tiers, multisig setup, limits, allowlists, recovery test log.
3. Credit policy: max LTV, HF floor, action levels, repayment source.
4. Liquidity ladder: T0–T3 sizes and refill schedule.
5. Lending policy: markets, caps, risk assumptions.
6. Books template and letter of instruction (stored separately).

---

# Module 13 — The Income Engine

![Module 13 — The Income Engine](assets/modules/module-13.png)

*Outcome: design an income portfolio, measure expected income after expected losses, and set a payout you can sustain.*
*Stage 5 · Operator. Prerequisites: Modules 1–12. Educational content only. Not financial or tax advice. No income is guaranteed. Loss probabilities are your own assumptions; figures are illustrative.*

**The operator's income rule:** plan on **expected** income (yield minus
expected losses), pay out **less** than that, and never pay out of principal.

---

## Lesson 13.1 — Income sources ranked by durability

### Objective
Rank income sources by how long and how reliably they're likely to pay, not by their headline rate.

### Explanation
| Source | Typical driver | Durability | Variability |
|---|---|---|---|
| Blue-chip stablecoin lending | Borrower demand | High | Medium: moves with demand |
| Staking / LSTs | Network security rewards | High | Low–medium |
| Fixed-rate PTs to maturity | Locked at purchase | Fixed for the term | None until maturity |
| Curated lending vaults | Borrower demand in isolated markets | Medium | Medium |
| LP fees (major pairs) | Trading volume | Medium | High |
| Funding / basis carry | Market positioning | Low–medium | High: can turn negative |
| Options premium | Volatility | Medium | High |
| Incentives / points | Protocol budgets | Low | Very high |

A durable income engine is built mostly from the top of this table. The
bottom rows are **boosters** you size small and expect to switch off.

### Checklist
- [ ] Every income position tagged with its source and durability
- [ ] Core income from high-durability sources

### Quiz
<details><summary>1. Why is funding carry low durability?</summary>It depends on market positioning and can turn negative for long periods.</details>
<details><summary>2. Which source gives a known rate for a set term?</summary>Fixed-rate PTs held to maturity.</details>
<details><summary>3. How should incentive income be treated?</summary>As a temporary booster, sold on a schedule and not relied on.</details>

---

## Lesson 13.2 — Risk-adjusted yield: subtracting expected losses

### Objective
Convert every headline yield into an expected yield after the losses it statistically carries.

### Explanation
`risk-adjusted yield = headline − (annual loss probability × loss given default) − costs`

You don't know the true loss probability, so **write down an assumption and
be conservative.** Newer protocols, more dependencies and higher leverage
deserve higher numbers. The point isn't precision; it's making you compare
positions on the same footing.

### Worked example
| Position | Headline | Assumed loss prob. | LGD | Risk-adjusted |
|---|---|---|---|---|
| New protocol vault | 9.0% | 3%/yr | 100% | **6.0%** |
| Blue-chip lending | 4.5% | 0.5%/yr | 100% | **4.0%** |

`defi_calc.py expected --yield-apy 9 --loss-prob 0.03`

The 9% vault still wins on expectation, but by 2 points, not 4.5. Its bad
outcome is also far worse, so size it smaller (Lesson 13.3).

### Checklist
- [ ] Loss probability and LGD written for every position
- [ ] Decisions made on risk-adjusted, not headline

### Quiz
<details><summary>1. 12% headline, 5%/yr loss probability, 60% LGD. Risk-adjusted?</summary>12 − 3 = 9%.</details>
<details><summary>2. Why assume conservatively?</summary>Losses cluster in stress, when many positions fail together; optimistic assumptions overstate income.</details>
<details><summary>3. Two positions, same risk-adjusted yield. Which gets more capital?</summary>The one with the smaller and better-understood worst case.</details>

---

## Lesson 13.3 — Building the income portfolio

### Objective
Assemble an income portfolio and calculate its blended risk-adjusted yield and expected income.

### Explanation
Build in layers: **core** (high-durability, 60–80%), **term** (fixed PTs matched
to the liquidity ladder), **boosters** (carry, options, LP; small). Apply
Module 8's caps: per protocol, per chain, per stablecoin issuer.

### Worked example — $500,000 income portfolio
`defi_calc.py income --pos "Stable lending A:100000:5:0.005:1" --pos "Stable lending B:100000:4.5:0.005:1" --pos "LST staking:150000:3.2:0.01:0.5" --pos "PT fixed stable:100000:8:0.02:0.5" --pos "Funding carry:50000:9:0.05:0.3"`

| Position | Amount | Yield | Expected loss | Net | Income/yr |
|---|---|---|---|---|---|
| Stable lending A | 100,000 | 5.0% | 0.5% | 4.5% | 4,500 |
| Stable lending B | 100,000 | 4.5% | 0.5% | 4.0% | 4,000 |
| LST staking | 150,000 | 3.2% | 0.5% | 2.7% | 4,050 |
| PT fixed stable | 100,000 | 8.0% | 1.0% | 7.0% | 7,000 |
| Funding carry | 50,000 | 9.0% | 1.5% | 7.5% | 3,750 |
| **Total** | **500,000** | | | **4.66%** | **23,300** |

![From headline yield to sustainable payout](assets/charts/income-waterfall.png)

Note: the LST line is priced in ETH, so its dollar value, and therefore the
dollar income, moves with ETH. The rest is stablecoin-denominated.

### Checklist
- [ ] Core ≥ 60% from high-durability sources
- [ ] Caps respected per protocol, chain and issuer
- [ ] Blended risk-adjusted yield calculated

### Quiz
<details><summary>1. Which line contributes the most expected income, and why?</summary>PT fixed stable ($7,000): a high locked rate on a sizeable allocation, even after the haircut.</details>
<details><summary>2. Why is the carry line only $50,000?</summary>It's a low-durability booster with a higher assumed loss rate.</details>
<details><summary>3. What makes the LST income variable in dollars?</summary>It's denominated in ETH, so the dollar value moves with the ETH price.</details>

---

## Lesson 13.4 — The payout policy: how much you can take out

### Objective
Set a payout you can sustain through bad years, and the rules that change it.

### Explanation
- **Pay out a share of *expected* income, not headline** (e.g. 70%).
- **Retain the rest** as a loss buffer; it absorbs the losses you assumed in 13.2.
- **Pay from the T0/T1 ladder** (Module 12.4), refilled by income, so payouts never depend on selling anything that day.
- **Never pay from principal.** If income falls short, the payout falls.
- **Review quarterly:** if realised income is below expected for two quarters, cut the payout to 70% of the new realised level.

### Worked example
Expected income **$23,300/yr** × 70% = **$16,310/yr** paid out (**$1,359/month**).
**$6,990/yr** retained. If a position fails as assumed, the buffer absorbs it
and the payout continues.

### Checklist
- [ ] Payout ratio written (≤ 70–80% of expected income)
- [ ] Paid from the ladder, not from positions
- [ ] Quarterly review rule written
- [ ] "Never from principal" rule written

### Quiz
<details><summary>1. Expected income $40,000. Payout at 70%?</summary>$28,000/yr (~$2,333/month).</details>
<details><summary>2. What's the retained 30% for?</summary>Absorbing expected losses and bad years without cutting into principal.</details>
<details><summary>3. Realised income lags expected for two quarters. What happens?</summary>Cut the payout to the policy share of the new realised level.</details>

---

## Lesson 13.5 — Scaling, compounding and the annual review

### Objective
Grow the engine safely and review it like a bank's annual report.

### Explanation
**Compounding:** reinvesting the retained share grows principal, and income
with it. At a 4.66% risk-adjusted yield with 30% retained, principal grows
~**1.4%/yr** from retention alone. The payout grows at about the same rate:
$16,310 → ~$17,480 after five years (before any new capital).

**Scaling rules as the book grows:**
- Caps are **percentages**, so position sizes rise, and so does market impact.
  Check pool depth and exit liquidity at the new size.
- Add independent protocols and issuers before adding size to existing ones.
- More size means more value at stake in custody: revisit Module 12.2.

**Annual review (one page):**
1. Balance sheet: start vs end equity, LTV, runway
2. Income: expected vs realised, by source
3. Losses and near-misses: what happened, what changed
4. Payout: paid vs policy
5. Risk assumptions: update loss probabilities from the year's incidents
6. Custody and succession drill: done?

### Checklist
- [ ] Retained income reinvested per policy
- [ ] Exit liquidity checked at current size
- [ ] Annual review completed and filed with the books

### Quiz
<details><summary>1. Yield 5%, 40% retained. Growth from retention alone?</summary>~2% a year.</details>
<details><summary>2. Why check exit liquidity as the book grows?</summary>A position that was easy to exit at $50k may move the market at $500k.</details>
<details><summary>3. What should the annual review update?</summary>Loss-probability assumptions, from the year's incidents and near-misses.</details>

---

### Module 13 practical
1. Tag every position by source and durability (13.1).
2. Write loss assumptions and compute risk-adjusted yields (13.2).
3. Build your income portfolio with `defi_calc.py income` (13.3).
4. Write your payout policy (13.4) and first annual-review template (13.5).

---

# 7. Skills archive

Claude skills for building and running the Grid Bot Builder business and the
new DeFi program on Whop. Everything lives in `.claude/skills/`, so Claude Code
loads these skills automatically in any session opened on this repo.

## Start here

Ask Claude: *"Use whop-defi-program to plan the DeFi program."* That skill
walks through offer → curriculum → Whop setup → funnel → guardrails → launch,
and calls the others as needed.

## On-Chain Operator Program
Everything for the DeFi program is in one file: [`ON-CHAIN-OPERATOR-PROGRAM.md`](programs/defi-program/ON-CHAIN-OPERATOR-PROGRAM.md), also as [Word](programs/defi-program/On-Chain-Operator-Program.docx) and [PDF](programs/defi-program/On-Chain-Operator-Program.pdf).
To finish building it, paste [`programs/defi-program/BUILD-PROMPT.md`](programs/defi-program/BUILD-PROMPT.md) into Claude Code.

## Skills

### Your business skills (custom)
| Skill | What it does | Source |
|---|---|---|
| `whop-defi-program` | Master playbook: turn the 42-chapter DeFi module into a Whop product and wire it into the GBB funnel | New, built from Notion + Zapier |
| `defi-strategies` | 25 DeFi strategies in 6 levels (up to fixed-rate, basis, options, credit lines and hedged yield), plus `defi_calc.py` with 15 calculators including income portfolios and a personal balance sheet | Notion strategy library, expanded |
| `defi-due-diligence` | 6-step protocol risk loop, before-signing checklist, logs to Notion tracker | Notion: DeFi & On-Chain module |
| `grid-bot-design` | Regime/range/spacing/fees/risk method + `grid_calc.py` calculator, logs to Notion checklist | Notion: Grid Bot Builder module |
| `gbb-new-lead` | Score, tag and email new leads | Zapier (archive copy) |
| `gbb-customer-onboarding` | Post-purchase onboarding + Elite Intel upsell | Zapier (archive copy) |
| `gbb-ad-performance` | Weekly CAC / ROAS / budget report | Zapier (archive copy) |
| `gbb-pipeline-check` | Funnel stages, rates, stale leads | Zapier (archive copy) |

### Building blocks (from [anthropics/skills](https://github.com/anthropics/skills), Apache 2.0)
| Skill | Use it for |
|---|---|
| `mcp-builder` | Building an MCP server, e.g. to expose Grid Bot / DeFi tools to members' AI agents |
| `web-artifacts-builder` | Interactive tools, e.g. a DeFi Command Centre or grid simulator for the Whop app |
| `frontend-design` | Sales pages and course UI that don't look generic |
| `webapp-testing` | Playwright testing for anything you build |
| `skill-creator` | Writing, testing and improving new skills in this archive |

## Notes
- **Zapier is the source of truth** for the four `gbb-*` skills. This repo is
  public, so internal IDs (Mailchimp list, Whop business ID, plan IDs, owner
  email) are `<PLACEHOLDERS>`. To keep real values locally, put them in
  `config.local.md`, which git ignores.
- **Pricing conflict to resolve:** `gbb-ad-performance` still describes a
  "Grid Bot Starter" (A$47–97) and GBB at A$497. The newer skills say $997 and
  that there's no Starter tier.
- Provenance and licences: see `SOURCES.md`.

---

# 8. Build Prompt: On-Chain Operator Program

**Run it in:** Claude Code (claude.ai/code, the desktop app or the CLI) with
the GitHub repo `kyleashton88-cyber/claude` open on branch
`claude/grid-bot-builder-skills-bmrez2`. Connect **Notion** and **Zapier**,
and make sure **Whop is connected inside Zapier**. Claude Code loads the
skills in `.claude/skills/` automatically. Other AIs won't, and they can't
reach your Notion or Zapier, so use Claude Code.

Paste everything below the line as your first message.

---

You're building out my **On-Chain Operator Program**, a high-ticket DeFi
program that takes someone who knows nothing to complete mastery: every
professional strategy, a risk-adjusted income engine, and operating as their
own on-chain bank. It goes into my Whop store as a new product alongside
Grid Bot Builder. Work in this repo on branch
`claude/grid-bot-builder-skills-bmrez2`. Commit and push after each finished piece.

## Read first
1. `README.md` (skills archive) and `programs/defi-program/README.md` (build status)
2. `programs/defi-program/ON-CHAIN-OPERATOR-PROGRAM.md`: master file with decisions, curriculum, setup, funnel and finished lessons
3. `programs/defi-program/06-whop-store-listing.md`: logo system, store listing copy and image upload map
4. Skills: `whop-defi-program` (master workflow), `defi-strategies`, `defi-due-diligence`, `grid-bot-design`, `gbb-*`, `frontend-design`, `dataviz`
5. Notion: "ATLAS — The Universal Trading Library" → "DeFi & On-Chain (Complete Module)". This is the source for every lesson.

## Locked decisions (don't change them)
- Name: On-Chain Operator Program. Course tier $15,000 one-time. Live tier priced higher.
- Launch to everyone. Cold traffic goes application → call (vip-defi-consult Calendly) → checkout.
- **6 stages, 15 modules, 76 lessons**, Module 0 (Crypto From Zero) to Module 14 (Automation & Mastery). Structure in `01-offer-and-curriculum.md`. Every lesson follows: Objective → Explanation → Worked example → Checklist → 3-question quiz.
- **Depth standard:** match `lessons/module-10-…`, `module-12-…` and `module-13-…`. Advanced lessons state "what this position is short", show computed numbers, and give professional rules (sizing, exits, caps).

## Logo & brand (lead with it)
The logo is two interlocked chain rings inside a hexagonal block with corner
nodes (`logoMark()` in `export/build_images.js`). It leads every surface.
- Use the rendered files in `assets/brand/`: stacked icon, marks (dark and light transparent), horizontal lockups, favicon, brand guide.
- Every store image, module banner and document cover carries the logo. Document diagrams carry the small mark in the footer.
- Never recolour the rings, stretch the mark, or put the light version on dark.

## Imagery standard (every deliverable must meet it)
All images come from one generator, `programs/defi-program/export/build_images.js`,
so the brand stays consistent. Extend that file and don't hand-place one-off images.
- **Brand:** Inter typeface (bundled via `@fontsource`). Navy `#0B1F33`→`#12355B` gradient with a faint node-network motif for dark/store images. `#FCFCFB` surface for light document images. Teal `#2ee6a6` accent on dark only.
- **Charts:** follow the `dataviz` skill. Blue `#2a78d6` is the primary series, orange `#eb6834` the secondary (validated pair). One y-axis. Recessive grid. Direct labels on the empty side of the line, never overlapping. Every number must be computed, not typed.
- **Resolution:** document images at 2× (1800 px wide), store images at exact upload size (1024×1024, 1920×1080).
- **Every module** gets its banner (`assets/modules/module-NN.png`, already rendered for 0–14) at the top of its lesson file. **Every lesson** gets at least one diagram or chart where a picture explains the mechanism better than text (a flow, a curve, a comparison). Add new ones to the `ASSETS` list.
- **Review:** after rendering, open every new or changed image and check it by eye. Fix any label collision, overflow, clipped text or empty-looking layout before committing.
- Every image carries the footer "Educational content only · Not financial advice · No results are guaranteed" (the shells already do this).

## Work to do, in order
1. **Write the remaining 44 lessons** (32 of 76 are done: Modules 1, 2, 9, 10, 12, 13 and lesson 8.3), one file per module in `programs/defi-program/lessons/` (`module-NN-name.md`):
   - **Module 0** Crypto From Zero (5): absolute beginner, no jargon without a definition.
   - **Modules 3–7** (27) from the Notion ATLAS chapters listed in the curriculum.
   - **Lessons 8.1, 8.2, 8.4** (3) into `module-08-…` (8.3 is `03-defi-strategy-mastery.md`).
   - **Module 11** Hedging & Risk Engineering (5) and **Module 14** Automation & Mastery (4): original content at the depth of Modules 10/12/13.
   Check every number with `.claude/skills/defi-strategies/scripts/defi_calc.py` (15 calculators, including `pt`, `basis`, `covered-call`, `expected`, `income`, `bank`) or Python. Add a practical at the end of each module. Suggested new visuals: first-transaction walkthrough (M0), health-factor gauge (M3), APY decomposition bar (M4), bridge/oracle dependency map (M5), due-diligence scorecard (M6), exchange-flow and holder-metric examples (M7), portfolio risk buckets (M8), hedge payoff chart and stress-test table (M11), monitoring/alert flow (M14).
2. **Capstones**: the analyst capstone (due-diligence file, after Module 7) and the operator capstone (a complete personal bank: balance sheet, custody, credit, ladder, income portfolio, payout policy, stress test, incident plan). Write briefs and grading rubrics, each with a one-page visual overview.
3. **Live tier**: design what it includes (session cadence, capstone reviews, portfolio reviews, Q&A), then propose a price and wait for my approval. Update the "What's included" gallery image once it's priced.
4. **Application form** (questions + scoring that plugs into `gbb-new-lead` with interest = defi) and a **sales call script**.
5. **Sales page**: build it with the `frontend-design` skill using the store images, the copy in `06-whop-store-listing.md`, and the brand above.
6. **Add the product to my Whop store** per `05-whop-setup.md` and `06-whop-store-listing.md`. I create the hidden product in the dashboard and upload the images in the listed order, then give you the `prod_` ID. You create plans and checkout links through Zapier, but only after showing me the exact values.
7. **Funnel**: apply `04-funnel-changes.md` to my Zapier skills (`update_zapier_skill`) after I approve, and mirror the changes into `.claude/skills/gbb-*`.
8. **Rebuild everything and push**: `python3 programs/defi-program/build_master.py`, then `cd programs/defi-program/export && npm install && npm run build` (renders all images, then the Word and PDF copies). Open the PDF and spot-check pages that have images.

## Rules
- Educational only. No promised, projected or guaranteed returns or income anywhere: lessons, images, emails, sales page, store listing or call script. Always show how a strategy loses money next to how it earns. "Own bank" is a method, never presented as a licence or financial service. Tax and legal points always say to consult a professional.
- Never ask for seed phrases, private keys or exchange API keys.
- No Discord, Skool or Slack. Use only the Calendly links named in the skills.
- Ask me before anything outward-facing: creating or changing anything on Whop, sending emails, editing Zapier skills, changing prices.
- This repo is public. Never commit internal IDs (Mailchimp list, Whop business or plan IDs, private emails). Use `<PLACEHOLDERS>`.
- Still open, ask me: live-tier price, refund policy, Grid Bot Builder customer pricing, whether the "Grid Bot Starter" tier exists.

## Done when
- All 76 lessons and both capstones are written, number-checked and illustrated to the imagery standard, with the logo leading every surface.
- Live tier, application, call script and sales page are approved.
- The product is in my Whop store (hidden until I say launch) with icon, banner and gallery images, and its plans and checkout links exist.
- Funnel skills are updated in Zapier and the repo.
- The master file, Word and PDF are rebuilt and pushed.
