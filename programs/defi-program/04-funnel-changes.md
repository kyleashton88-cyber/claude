# DeFi Program — Funnel Changes (DRAFT, not applied)

Proposed changes to the four live Zapier skills so they handle the DeFi
program alongside Grid Bot Builder. **Nothing has been changed in Zapier.**
Once you approve, the edits go into Zapier (`update_zapier_skill`) and are
mirrored into `.claude/skills/gbb-*`.

Product name: **On-Chain Operator Program**, course $15,000 one-time, sold through application → call → checkout (see `05-whop-setup.md`). This changes the emails below: hot/warm DeFi leads get the **application + call** link, not a direct checkout link. Live tier: price on application. Link placeholders (filled at setup): `<DEFI_CHECKOUT_URL>`, `<DEFI_PLAN_IDS>`, `<DEFI_ACCESS_URL>` (the program's Whop hub link), `<DEFI_APPLICATION_URL>` (Typeform application), `<DEFI_CALL_LINK>` (your `vip-defi-consult` Calendly link; verify the URL).

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
> 15 modules and 107 lessons, from zero to running your own on-chain bank.
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
