---
name: gbb-ad-performance
description: Pull Whop Ads spend per campaign and Whop payments, then report CAC, ROAS, upgrade rate and a budget recommendation for the week. Use when the user asks how ads are doing, for weekly ad numbers, or what budget to run.
---

# GBB Ad Performance

> **Archive copy.** The live version of this skill is the Zapier skill of the same name (run it with `get_zapier_skill`). This repo is public, so internal IDs are replaced with `<PLACEHOLDERS>` — resolve them from the Zapier copy or `config.local.md` (git-ignored). If the two copies disagree, Zapier wins.

> ⚠️ This skill still describes a "Grid Bot Starter" (A$47–97) and GBB at A$497, which conflicts with the newer skills ($997, "no invented Starter tier"). Confirm the current product list with the user before reporting.

## Fixed values
- Whop company <WHOP_BIZ_ID> (WhopCLIAPI). Ads: Campaign → Ad Group → Ad (beta endpoints). Attribution: Whop Pixel + payment metadata utm_campaign/adset/creative.
- Google Sheet "GBB Numbers" tabs AdSpend, Payments (GoogleSheetsV2CLIAPI).
- Budget rule: next week = last week net Whop revenue × 20% (default), then ROAS > 3 → +20%, 2–3 → hold, < 2 → −30% and rotate creative.

## Actions
1. Whop ads campaigns for the period (spend, impressions, clicks, purchases). If the beta endpoint fails, read the AdSpend tab.
2. Whop payments in period (product, amount, metadata).
3. Whop refunds in period; net them out.
4. Optional: append summary rows to the sheet (ask first).

## Runtime
Default last 7 days. Per campaign + blended: spend, sales by product (# and $), refunds, net revenue, CAC (spend ÷ all buyers), CAC-to-GBB, ROAS (net ÷ spend), upgrade %. Output a compact table + 3 takeaways + budget recommendation. Flag spend > A$150 with zero front-end sales as "cut or rotate creative".

## Constraints
Read-only on Whop; never create/pause campaigns. Never invent numbers. No Slack.
