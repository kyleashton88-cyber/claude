---
name: gbb-customer-onboarding
description: Onboard a Grid Bot Builder (or Elite) buyer after a Whop payment — HubSpot stage + ad attribution, Mailchimp tag swap, onboarding email, separate Elite Intel Community upsell invite, exclusion list, optional affiliate invite. Use when the user says "X just bought" or a Whop payment comes in.
---

# GBB Customer Onboarding (v5)

> **Archive copy.** The live version of this skill is the Zapier skill of the same name (run it with `get_zapier_skill`). This repo is public, so internal IDs are replaced with `<PLACEHOLDERS>` — resolve them from the Zapier copy or `config.local.md` (git-ignored). If the two copies disagree, Zapier wins.

## Fixed values
- Grid Bot Builder: self-serve no-code SaaS, instant delivery (NOT done-for-you, no 1:1 setup call). $997 (<GBB_PLAN_ONE_TIME>) or 3× $399 (<GBB_PLAN_3PAY>). 30-day money-back on the software.
- Grid Bot Elite: $2,497 (<ELITE_PLAN_ONE_TIME>) or 3× $999 (<ELITE_PLAN_3PAY>). Institutional-grade + live coaching + VIP chat.
- Client portal: https://grid-bot-builder.whop.site/account · Listing: https://whop.com/grid-bot-building-blueprint
- Elite Intel Community (founder Jessica Coady): https://elite-intel-community.whop.site/ — $67/mo, 3-day trial, code LAUNCH = $20 off. Upsell invite only; never grant access.
- Mailchimp list <MAILCHIMP_LIST_ID>: remove `gbb-lead`, add `gbb-customer`.
- HubSpot: lifecycle "customer", deal stage closedwon, amount = actual plan price (997, 1197 on 3-pay, 2497, 2997). Attribution: utm_campaign, utm_adset, utm_creative.
- Google Sheet "GBB Numbers": tabs Payments + ExcludeList.
- Pre-sale Calendly (vipbookings) is never sent to buyers. No Discord, no Skool, no Slack.

## Actions
1. WhopCLIAPI:find_member(email) / retrieve_payment(id) — confirm product, plan, amount, utm metadata.
2. HubSpot upsert_contact(lifecyclestage "customer") + update_crm_deal(closedwon, amount) — search first, never duplicate; write utm_* on contact.
3. Mailchimp tag swap.
4–5. Gmail welcome/onboarding: instant access + client portal + how to connect their exchange API key *inside the tool* (never shared with us) + setup docs / Mastery volumes.
6. Separate Gmail: Elite Intel Community invite (3-day trial, code LAUNCH), framed as optional upsell.
7. Sheets append → Payments (date, name, email, product, amount, campaign, adset, creative) and → ExcludeList.
8. Optional: WhopCLIAPI:create_affiliate(email). Builder affiliates via grid-bot-builder.whop.site/affiliate; Elite Intel Community affiliates earn 20% recurring.

## Runtime
Verify payment via Whop unless the user confirmed it. Show both emails for a one-word confirm unless told "send without asking". One-line result per step.

## Constraints
Never refund/cancel/modify memberships. Never ask for or store exchange API keys. Don't mark Customer without verified payment or explicit confirmation.
