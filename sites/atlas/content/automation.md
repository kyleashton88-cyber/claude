---
title: Trading automation
slug: automation
level: intermediate
category: automation
related:
  - market-strategies
  - security
  - risk-academy
  - journal-lab
last_reviewed: 2026-11-10
status: draft
---

# Trading automation

Automation means software places or manages orders for you under rules you wrote. It can follow a plan without hesitation, at any hour, and it can repeat a mistake just as faithfully. This page explains the common kinds of bots, how alerts and webhooks connect a chart to an order, how to set up API keys safely, and how to stop a bot when something goes wrong. It is general information. A bot does not make a strategy better. It executes the one it is given. Nothing here is a recommendation to run a bot or a promise about what one will do. Consider your own circumstances.

Worked numbers below are invented. Each block is marked as a hypothetical example. The grid bot has its own module on the Atlas site. Key safety basics are on the [security page](security.md#seed-phrases-and-keys). Short definitions are in the [glossary](glossary.md#trading-bot).

## What a bot actually does

Every trading bot does three things in a loop:

1. **Reads** data: prices, its own open orders, its balance.
2. **Decides** what to do, using rules written in advance.
3. **Acts** by sending orders to a venue through an API.

Each step can fail. The data can be late or wrong. The rule can meet a market it was never designed for. The order can be rejected, partly filled, or filled at a worse price. A well-built bot assumes all three will happen at some point and has a written response for each.

## Grid bots

A [grid](glossary.md#grid) places a ladder of buy and sell orders across a price range. As price moves up and down inside the range, orders fill and are replaced, and each completed buy-and-sell pair is a [grid cycle](glossary.md#grid-cycle). A grid is a form of the range framework on the [market strategies page](market-strategies.md#range-and-mean-reversion).

What a grid needs: a range you can defend, a step size that clears fees and slippage, and a plan for when price leaves the range. What a grid does when price leaves: above the range it holds only quote currency and stops cycling, and below the range it holds only the base asset, now worth less. Neither is a malfunction. Both are the design.

The grid module on the site goes much further, with spacing, sizing, and a simulator.

## DCA bots

A dollar-cost averaging bot buys a fixed amount at fixed intervals. The simple version is the same method described on the market strategies page, run on a schedule.

Some DCA bots add **safety orders**: extra buys at set steps below the first entry, each often larger than the last, to lower the average entry. They then sell the whole position at a set percentage above the average. This changes the shape of the risk:

- Each safety order adds size into a falling market.
- If the steps scale up, most of the capital is committed near the bottom of the ladder.
- If price keeps falling past the last safety order, the bot is holding its largest position at a loss, with nothing left to add.

Hypothetical example. A made-up DCA bot starts with a base order of 100 quote units and has four safety orders, each double the one before: 200, 400, 800, and 1,600. If all fill, the bot has committed 100 + 200 + 400 + 800 + 1,600 = 3,100 quote units. More than half of it, 1,600, is in the last order alone. A plan that sized the bot from the first order would have understated the real exposure by a factor of 31. Illustrative example on hypothetical data. Not a recommendation to trade this asset or these levels.

Size a DCA bot from the full ladder, not from the base order. Run that total through the [position-sizing formula](risk-academy.md#position-sizing) as if it were one position with one stop.

## Grid versus DCA

| | Grid | DCA with safety orders |
|---|---|---|
| Market it is built for | Sideways inside a range | A dip followed by a recovery |
| What it holds in a fall | More base asset, bought on the way down | A growing position, bought in larger steps |
| What it holds in a rise past the top | Quote currency, no longer cycling | Usually closed at its take-profit |
| Main risk | Price leaves the range and does not return | Price falls past the last safety order |
| What to set first | The range and the stop outside it | The total ladder size and a final stop |

Neither type has a stop by default on many platforms. Adding one is a choice you make in the settings, and it is the most important setting.

## Alerts and webhooks

Many people write their entry rules on a charting platform, such as TradingView, rather than inside a bot. The chain looks like this:

1. An **alert** fires when a condition on the chart is met, such as a close above a level.
2. The alert sends a **webhook**: an HTTP message to a web address you control or to a bot service.
3. The receiving service reads the message and sends an order through the venue's API.

Each link adds failure points:

- **Delay.** Alerts can arrive late, especially in busy markets. A rule that depends on a fast fill may not get one.
- **Repainting.** Some indicators change past values once more data arrives. An alert that fired on a value the chart later erased leaves an order with no visible reason.
- **Duplicate or missing messages.** A network retry can send the same alert twice. A dropped message sends nothing. The receiver should reject duplicates and log every message.
- **Exposed secrets.** A webhook message usually includes a passphrase or token. Anyone who sees it can place orders through your receiver. Keep it out of screenshots and shared chart layouts.

Test the full chain with tiny size or on a test environment before you rely on it. Then check the log against the venue's order history after every session for the first weeks.

## API keys

An [API key](glossary.md#api-key) lets software act on your account. Treat it like a password that can trade.

**Permissions.** Give the key only what the bot needs. A trading bot needs to read balances and place and cancel orders. It does not need permission to withdraw. Never enable withdrawal on a key used by a bot or a third-party service. The same rule is on the [security page](security.md#seed-phrases-and-keys).

**IP allow-listing.** Many venues let you restrict a key to specific IP addresses. A key that only works from your server is much less useful to someone who steals it.

**One key per bot.** Separate keys let you revoke one without stopping the others, and let you see which bot placed which order.

**Storage.** Keep keys in the bot's secure settings or a secrets manager, not in a chat, a spreadsheet, or a code repository. If a key is ever pasted somewhere public, revoke it at once and create a new one.

**Review.** Delete keys you no longer use. Check the list of active keys on your account on a schedule.

We never ask for seed phrases, passwords or withdrawal-enabled keys. A message that asks for one is not from Market Pros Proprietary Limited and not from Stewart.

## Kill switches

A kill switch is a written, tested way to stop a bot and flatten or freeze its positions quickly. Decide it before the bot runs.

Common kill-switch rules:

- **Loss limit.** Stop the bot if its equity falls a set amount from its starting value or from its peak.
- **Range break.** Stop a grid if price closes beyond the range by a set distance.
- **Error count.** Stop if the bot gets a set number of order rejections or data errors in a short window.
- **Stale data.** Stop if prices have not updated for longer than a set time.
- **Manual.** A single action, which you have practised, that cancels all orders and disables the key.

For each rule, write what "stop" means: cancel open orders only, or cancel and close positions at market. Closing at market in a fast market can fill badly. Leaving positions open after cancelling orders leaves them without the bot's management. Choose in advance.

## Monitoring

A bot that is not watched is not automated. It is abandoned. A simple monitoring routine:

- **Daily.** Compare the bot's reported position and balance with the venue's account page. Read the error log.
- **Weekly.** Compare fills with the plan: are fees and slippage what you assumed? Record results in R in the [journal](journal-lab.md).
- **After any outage or upgrade.** Venue, bot service, or your own server. Check that orders and positions match what the bot thinks they are.

Set notifications for fills, errors, and kill-switch triggers. A notification you ignore is the same as none, so keep the list short enough to read.

Hypothetical example. A made-up grid bot is set for a range of 90 to 110 with a kill switch at a close below 87. Price falls to 92 and the bot has bought at each level on the way down, as designed. Price then closes at 86.5. The kill switch fires, cancels the remaining orders, and closes the position. The journal row records the loss in R, the range, the trigger, and whether the fill matched the plan. Illustrative example on hypothetical data. Not a recommendation to trade this asset or these levels.

## Common mistakes

- Running a bot with no stop, because the platform's default had none.
- Sizing a DCA bot from the base order instead of the full ladder.
- Enabling withdrawal on an API key.
- Sharing a chart layout that contains a webhook passphrase.
- Never testing the kill switch until it is needed.
- Assuming a backtest of the rule also tested the bot, the alerts, and the venue's behaviour.
- Checking the bot only when it is doing well.

## Before you start

Write the strategy as a framework first, using the four parts on the [market strategies page](market-strategies.md). Test the rule on historical data and in replay, as on the [journal page](journal-lab.md#backtesting). Then test the bot itself with the smallest size the venue allows. Automation is the last step, after the plan and the test, not the first.
