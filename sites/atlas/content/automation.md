---
title: Automation
slug: automation
level: intermediate
category: automation
related:
  - security
  - exchanges
  - glossary
last_reviewed: 2026-11-10
status: draft
---

# Automation

Automation means software applies a rule you have already written. It removes the hesitation before a click, and it also removes the pause in which you might have noticed a broken feed or a wrong market. This page is general information. It is not a build guide for a bot that trades for you, and it does not name a venue or a product.

A grid bot is one example of a rule: levels, a range, a size, and an invalidation. The words are in the [glossary](glossary.md#trading-bot). The order types a bot can send are on the [exchanges page](exchanges.md#order-types).

## The rule comes first

Write the rule in sentences before it exists in code. Include:

- The market and the timeframe.
- The condition that arms an order, and the condition that must not.
- The size, from the cash-at-risk formula, not from a feeling.
- What the software is allowed to do if the feed is stale, the spread blows out, or the position is already at the heat limit.
- Who is alerted, and what a human does next.

If the sentence version is vague, the code version will be confidently vague. Software will do the wrong thing quickly and without boredom.

## Keys and permissions

An API key is a credential. Give it the smallest permission that the rule needs. A program that places orders does not need permission to withdraw. Store the key as a secret. Delete keys you no longer use. Do not paste a key into a chat, a screenshot, or a ticket.

We never ask for seed phrases, passwords or withdrawal-enabled keys. A bot does not need a seed phrase to send an order through an API that is already authorised to trade. A request for the seed is not part of automation. It is the moment to stop. The rest of that rule is on the [security page](security.md).

## Alerts are not orders

An alert tells you that a price or a condition printed, so you can look. It is not an order unless a separate instruction sends one. Alerts fail when the feed, the device, or the delivery channel fails. A stop that matters belongs on the venue as a hard stop, not only as a notification you might see.

## Monitoring

A live rule needs a check you can do when you are not excited. Useful checks are dull:

- Is the process running, and is the feed time moving?
- Are the open orders the orders the rule intended, on the right market?
- Is portfolio heat still inside the number you wrote down?
- Did a partial fill leave a residual order?
- Has funding, a fee tier, or a halt changed the arithmetic the rule assumed?

The [journal](journal.md) is where you record that the rule fired and whether you left it alone. Turning a bot off because one interval felt bad, without a written switch, is a second strategy hiding inside the first.

## Testing without capital

Paper trading and a forward test apply the frozen rule without funds, or with a simulator. They show whether the rule can be followed. They do not reproduce the slippage, the outage, or the feeling of a live loss. Treat a pretty paper curve as a rehearsal. The [glossary](glossary.md#paper-trading) says the same thing in fewer lines.

## When to pull the plug

Pull the plug when the invalidation prints, when you cannot explain the current orders, when the key permissions are wider than the rule, or when the feed and the venue disagree about the position. Those are operational stops. They are not a view on the next price. Restart only from the written rule, not from the hope that the next hour will repair the last one.
