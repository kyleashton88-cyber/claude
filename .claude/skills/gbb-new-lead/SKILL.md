---
name: gbb-new-lead
description: Process a new Grid Bot Builder lead — score and tier them, create/update the HubSpot contact + deal with ad attribution, tag in Mailchimp, and send the right email (hot → personal note, warm → standard, cold → nurture + Elite Intel Community mention). Use when the user shares a new lead, form response or "X is interested".
---

# GBB New Lead (v6)

> **Archive copy.** The live version of this skill is the Zapier skill of the same name (run it with `get_zapier_skill`). This repo is public, so internal IDs are replaced with `<PLACEHOLDERS>` — resolve them from the Zapier copy or `config.local.md` (git-ignored). If the two copies disagree, Zapier wins.

## Fixed values
- Grid Bot Builder: self-serve no-code SaaS, instant delivery. $997 one-time (<GBB_PLAN_ONE_TIME>) or 3× $399 (<GBB_PLAN_3PAY>). 30-day money-back on the software.
- Grid Bot Elite: $2,497 one-time (<ELITE_PLAN_ONE_TIME>) or 3× $999 (<ELITE_PLAN_3PAY>).
- Pre-sale free call (NOT post-purchase): https://calendly.com/stewartcrown/vipbookings — booking adds the invitee to Mailchimp with tag `call-booked` via the native Calendly↔Mailchimp integration. Anyone tagged `call-booked` must not receive `gbb-nurture`.
- Elite Intel Community: https://elite-intel-community.whop.site/ — $67/mo, 3-day trial, code LAUNCH = $20 off. Mention as an option only, never free/bundled.
- Mailchimp list <MAILCHIMP_LIST_ID>; tags `gbb-lead`, `gbb-hot`, `gbb-nurture`, `call-booked` (Calendly-applied).
- Whop company <WHOP_BIZ_ID>. Zapier apps: MailchimpCLIAPI, HubSpotCLIAPI, TypeformCLIAPI, WhopCLIAPI. Gmail from <OWNER_EMAIL>.
- Never use other Calendly links (vip-defi-consult, strategy-call, 30/45/90min-consult, 20-minute-power-session, freedom-call*, defi, communitycoaching, grid-bot-discovery-call).
- No Skool, no Discord, no Slack. Hot-lead alerts go by Gmail to the owner.

## Lead scoring
Capital 20k+ = 4, 5–20k = 3, 1–5k = 1, <1k = 0 · exchange Binance/Bybit/OKX = 2 · experience some = 1, advanced = 2.
Hot ≥ 6 · Warm 3–5 · Cold < 3.

## Actions
1. (Optional source) TypeformCLIAPI:lookup_responses(formId, since, complete "true", size "25").
2. WhopCLIAPI:find_member(email) — already bought Builder/Elite? Stop and route to `gbb-customer-onboarding`.
3. HubSpotCLIAPI:upsert_contact(email, firstname, lastname, lifecyclestage "lead", lead_score, gbb_source, utm_campaign, utm_adset, utm_creative).
4. HubSpotCLIAPI:dealCreate(dealname "GBB - <First Last>", amount "997", dealstage "Lead") — search first, never duplicate.
5. Check Mailchimp for `call-booked`. If present, skip `gbb-nurture` and call offers regardless of tier.
6. Otherwise memberCreate + subscriber_segment: `gbb-lead` always; `gbb-hot` for hot; `gbb-nurture` for cold only.
7. Gmail by tier: Hot → personal note + $997 checkout + optional free call; Warm → standard email + checkout + optional call; Cold → nurture content + one line on Elite Intel Community (3-day trial). Apply the call-booked skip rule.
8. Hot only: Gmail alert to owner "HOT lead: <name> · <exchange> · <capital>".

## Runtime
Collect name, email, exchange, capital, experience, utm fields; state score + tier. Run 2, then 5, then 3–4 always, 6–7 per call-booked check. Show emails for a one-word confirm unless told "send without asking". Report tier, HubSpot records, tags, email status.

## Constraints
Emails under 120 words, plain text, no profit promises. Never offer Elite Intel Community as free. Never send nurture or call offers to `call-booked` contacts.
