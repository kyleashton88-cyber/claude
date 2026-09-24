---
name: whop-defi-program
description: Plan, build and launch the DeFi education program as a Whop product alongside Grid Bot Builder and Elite Intel Community. Use when the user wants to design the DeFi program's offer, curriculum, Whop product/plans, onboarding funnel, marketing copy or launch checklist, or asks "what do I build next for the DeFi program". Chains the other skills in this repo (defi-due-diligence, grid-bot-design, gbb-* funnel skills, mcp-builder, frontend-design, web-artifacts-builder, webapp-testing).
---

# Whop DeFi Program Builder

Builds a complete DeFi program on Whop from the content already in the user's
Notion library (ATLAS — The Universal Trading Library → *DeFi & On-Chain
(Complete Module)*, 42 chapters) and plugs it into the existing Grid Bot
Builder sales machine.

## The existing product ladder (do not contradict)

| Product | Where | Price | Role |
|---|---|---|---|
| Elite Intel Community (founder Jessica Coady) | elite-intel-community.whop.site | $67/mo, 3-day trial, code LAUNCH = $20 off first month | Low-commitment recurring entry point / upsell. Never granted free. |
| Grid Bot Builder | grid-bot-builder.whop.site · whop.com/grid-bot-building-blueprint | $997 one-time or 3× $399; 30-day money-back on the software | Core self-serve no-code SaaS, delivered instantly. Not done-for-you. |
| Grid Bot Elite | same store | $2,497 one-time or 3× $999 | Institutional-grade + live coaching + VIP chat. |
| **DeFi Program (new)** | to be created on Whop | **TBD — ask the user** | This skill's job. |

Rules carried over from the live Zapier skills: no Discord, no Skool, no Slack
posts; no profit promises; never ask for or store exchange API keys or seed
phrases; only the `vipbookings` Calendly link is used for pre-sale calls.

> Note: the older *gbb ad performance* Zapier skill still mentions a
> "Grid Bot Starter" (A$47–97) and GBB at A$497, while the newer skills say
> $997 and "no invented Starter tier". Ask the user which is current before
> using either in DeFi program copy or pricing.

## Workflow

Work through these phases in order. At each phase, show the user the output and
get a yes before moving on — pricing, positioning and anything published to
Whop are the user's decisions.

### 1. Offer design
Ask (or propose, then confirm):
- Who is it for — existing GBB customers wanting on-chain yield, or new cold
  traffic? This decides whether it's an upsell (after GBB onboarding) or a new
  front-end.
- Format — course only, course + community chat, or course + live calls.
- Price model — one-time, payment plan, or monthly. Mirror the GBB pattern
  (one-time + 3-pay) unless the user says otherwise.
- The promise — must be about *skills and process* ("research any protocol with
  a 6-step risk loop"), never returns or APY.

### 2. Curriculum (from Notion)
**Current structure (source of truth):** `programs/defi-program/01-offer-and-curriculum.md`: 6 stages, 15 modules, 92 lessons + a Mastery Starter per module, from Crypto From Zero to Operate as Your Own Bank. The grouping below is the original ATLAS mapping for Modules 1–9.

Fetch the Notion page "DeFi & On-Chain (Complete Module)" and group the 42
chapters into Whop course modules. Default grouping:

1. **Foundations & Safety** — ch. 1–5, 36 (DeFi stack, transactions, wallets, token standards, stablecoins, scam defence)
2. **Trading on DEXs** — ch. 6–9, 35 (DEXs, AMM math, LPing, impermanent loss, MEV)
3. **Lending & Leverage** — ch. 10–13 (markets, LTV/health factor, liquidations, borrowing strategies)
4. **Yield** — ch. 14–18, 37 (farming, staking, liquid staking, restaking, vaults, airdrops)
5. **Infrastructure Risk** — ch. 19–23 (bridges, L2s, oracles, smart contracts, contract risk)
6. **Research** — ch. 24–34, 41 (due diligence, tokenomics, governance, on-chain analytics, research workflow)
7. **Operating System** — ch. 38–40, 42 (portfolio construction, risk framework, 16-strategy library, operating playbook)
8. **Bridge to Grid Bots** — tie-in lesson: when a CEX grid bot beats a DeFi LP position and vice-versa (use grid-bot-design + the LP benchmark concept). This is the natural cross-sell into GBB.

Each lesson: objective → explanation → worked example → checklist → 3 quiz
questions. Reuse the module's flashcards, mermaid diagrams, strategy table and
metrics table. Worksheets = the Notion "DeFi Protocol Due Diligence Tracker"
(see `defi-due-diligence` skill).

### 3. Whop setup
Use the Whop MCP / API (Zapier `WhopCLIAPI`, or Whop's official MCP server —
per Whop's docs there is a docs server and an API server; confirm the current
URL at docs.whop.com → Developer → AI and MCP before configuring).
- Create the product + plans (one-time + 3-pay, or recurring) — **only after
  the user approves the exact names and prices**.
- Add the course app with the modules above; attach worksheets as downloads
  or Notion links.
- Set checkout metadata to carry `utm_campaign`, `utm_adset`, `utm_creative`
  so `gbb-ad-performance` / `gbb-pipeline-check` can attribute DeFi sales too.
- Never refund, cancel or modify existing memberships from this skill.

If a custom Whop app is needed (e.g. an interactive DeFi Command Centre /
liquidation stress-tester), use `web-artifacts-builder` or `frontend-design`
to build it, `webapp-testing` to verify it, and `mcp-builder` if the user wants
an MCP server exposing their own tools to members' agents.

### 4. Funnel wiring (reuse the GBB machine)
Extend — don't duplicate — the existing Zapier skills:
- `gbb-new-lead`: add a `defi-lead` tag and a DeFi interest field to scoring.
- `gbb-customer-onboarding`: add a DeFi branch (Mailchimp tag `defi-customer`,
  HubSpot deal name `DEFI - <name>`, welcome + onboarding email pointing to the
  course).
- `gbb-ad-performance` / `gbb-pipeline-check`: add the DeFi product to revenue
  by product.
Propose the diffs to the user; the live versions are in Zapier, so edits must
be made there (`update_zapier_skill`) as well as mirrored in this repo.

### 5. Compliance & copy guardrails
Every sales page, email and lesson:
- Educational only; not financial advice; no guaranteed or projected returns.
- Headline APY is never shown without the risk that produces it.
- Operating rule from the module: *"If you cannot explain the unwind, you do
  not understand the position yet."*
- Customers keep custody of their own keys; the program never asks for seed
  phrases, private keys or API secrets.

### 6. Launch checklist
- [ ] Offer, price and plans approved by the user
- [ ] Whop product + plans live, checkout tested end to end
- [ ] All 8 course modules uploaded; quizzes and worksheets attached
- [ ] Onboarding email + Mailchimp tags + HubSpot pipeline stage configured
- [ ] Attribution metadata verified on a test purchase
- [ ] Sales page reviewed against the guardrails above
- [ ] Upsell/cross-sell paths set: DeFi ↔ GBB ↔ Elite Intel Community
