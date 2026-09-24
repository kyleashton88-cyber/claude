---
name: gbb-pipeline-check
description: Grid Bot Builder funnel check — HubSpot deals by stage, bookings this week, show/close rates, stale leads for nurture, Whop revenue by product with per-campaign attribution. Use when the user asks how the pipeline or funnel is doing.
---

# GBB Pipeline Check (v3)

> **Archive copy.** The live version of this skill is the Zapier skill of the same name (run it with `get_zapier_skill`). This repo is public, so internal IDs are replaced with `<PLACEHOLDERS>` — resolve them from the Zapier copy or `config.local.md` (git-ignored). If the two copies disagree, Zapier wins.

## Fixed values
- HubSpot deals "GBB - <name>", stages Lead → Starter buyer → Call booked → Call done → Customer → Needs rebook → Lost; contact props lead_score, utm_campaign, utm_adset, utm_creative.
- Calendly (CalendlyCLIAPI) VIP bookings. Mailchimp list <MAILCHIMP_LIST_ID>, nurture tag `gbb-nurture`.
- Whop company <WHOP_BIZ_ID>; Stripe for history only.

## Actions
1. HubSpot deal search (dealstage, amount, createdate, closedate, utm_campaign), names starting "GBB -".
2. HubSpot contact search — leads/Starter buyers created > 3 days ago.
3. Calendly find_invitee_by_email per stale lead; count this week's bookings/cancels.
4. Whop entries + payments last 30 days — revenue by product and utm_campaign.
5. Optional on a clear yes: tag stale leads `gbb-nurture`.

## Output
Deals by stage (count + $); bookings/cancels this week; lead→booked, booked→showed, call→close, upgrade %; revenue 7/30 days by product; top 3 campaigns by GBB revenue; stale leads (first name + last initial, score, days). No emails in the summary.

## Constraints
Read-only unless nurture tagging is confirmed. No Slack.
