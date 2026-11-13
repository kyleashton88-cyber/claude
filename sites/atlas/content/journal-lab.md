---
title: Backtesting and journaling
slug: journal-lab
level: intermediate
category: research
related:
  - risk-academy
  - psychology
  - market-strategies
  - glossary
last_reviewed: 2026-11-10
status: draft
---

# Backtesting and journaling

A journal is the record of what you planned, what you did, and what happened. Without it, every review is memory, and memory edits itself in your favour. This page sets out a journal template, a review cadence, a way to label mistakes, and the metrics that turn a list of trades into something you can study. It is general information. The metrics describe a sample you already have. They do not forecast the next trade and they are not a promise about any future result. Consider your own circumstances.

Worked numbers below are invented. Each block is marked as a hypothetical example. The formulas for R, expectancy, and drawdown come from the [risk academy](risk-academy.md). The psychology tags come from the [psychology page](psychology.md). Short definitions are in the [glossary](glossary.md#journal).

## What a journal is for

A journal answers three questions over time:

1. **Did I follow my plan?** This is the process question, and you control it.
2. **What did the plan produce?** This is the outcome question, measured in R so trades of different sizes compare fairly.
3. **Where does the plan break?** This is the learning question. It needs enough trades to show a pattern rather than noise.

A journal kept only for winning trades answers none of them. Every trade goes in, including the ones you would rather forget, and the ones you planned but did not take.

## The template

The downloadable CSV on the Atlas site uses these columns. A spreadsheet with the same headings works as well. Keep one row per trade.

| Column | What goes in it |
|---|---|
| date_open | Date and time the position opened, with time zone |
| date_close | Date and time it closed |
| market | The asset and contract type, for example spot or perpetual |
| timeframe | The chart timeframe the setup was taken on |
| framework | The written framework, from [market strategies](market-strategies.md) or your own |
| direction | Long or short |
| entry | Average entry price |
| stop | Initial stop price, at entry |
| target | Planned target, if the framework has one |
| exit | Average exit price |
| size | Units or contracts |
| initial_risk | Cash at risk at entry, including your slippage allowance |
| fees | All fees and funding paid |
| result | Net result in cash, after fees |
| r_multiple | result divided by initial_risk |
| mae | Worst move against you while open, in R |
| mfe | Best move in your favour while open, in R |
| plan_followed | Yes or no |
| mistake_tags | Zero or more tags from the list below |
| emotion | One word, written before entry |
| screenshot | A link to the chart at entry and at exit |
| notes | One or two sentences, written within a day |

Two columns do most of the work. **initial_risk** fixes what 1 R meant for that trade, so a later stop change cannot quietly redefine it. **plan_followed** separates process from outcome. The [MAE](glossary.md#mae) and [MFE](glossary.md#mfe) columns show whether stops are too tight and targets too far, which a win or loss alone cannot show.

## Mistake tags

A tag names what went wrong in words you can count later. Keep the list short and fixed, so the same mistake always gets the same tag.

**Plan mistakes**
- `no-setup`: entered without a written framework condition.
- `no-stop`: no hard stop at entry.
- `oversize`: size larger than the position-sizing formula allowed.
- `heat`: total open risk above the limit.

**Execution mistakes**
- `chase`: entered after the planned level had passed.
- `early-exit`: closed before the stop or target without a rule that said so.
- `moved-stop`: stop moved in the direction of more risk.
- `slippage`: fill materially worse than planned, from market conditions rather than choice.

**State mistakes**
- `fomo`: entered from fear of missing the move.
- `revenge`: entered to recover a recent loss.
- `tilt`: one of your written tilt signs was present.
- `fatigue`: traded outside your planned hours or when tired.

**Missed and skipped**
- `missed`: a valid setup you did not take.
- `skipped-ok`: a setup you chose not to take for a written reason.

The tags come straight from the [psychology page](psychology.md). Counting them is the point. A review that says "I chased four times this month" is more useful than one that says "I should be more patient".

## The metrics

These are definitions. A metric on a small sample is a rough description, not a finding.

- **Win rate.** Winning trades divided by all closed trades. On its own it says nothing about whether the sample made or lost money. See [win rate](glossary.md#win-rate).
- **Average win and average loss, in R.** The typical size of each outcome.
- **[Payoff ratio](glossary.md#payoff-ratio).** Average win divided by average loss.
- **[Expectancy](risk-academy.md#expectancy).** The average R per trade in the sample: win fraction times average win, minus loss fraction times average loss.
- **Profit factor.** Total gains divided by total losses, both in cash or both in R. Above one means the gains in that sample were larger than the losses.
- **[Maximum drawdown](glossary.md#maximum-drawdown).** The deepest fall from an equity peak in the sample.
- **Plan-followed rate.** Trades with plan_followed set to yes, divided by all trades.
- **R by tag.** The total R of trades carrying each mistake tag.

Hypothetical example. A made-up journal has twenty closed trades. Eight are winners averaging +2.0 R. Twelve are losers averaging -1.0 R. The share of winners is 8 / 20, which is 40 percent. Payoff ratio is 2.0 / 1.0 = 2.0. Expectancy is (0.4 * 2.0) - (0.6 * 1.0) = 0.2 R per trade. Profit factor is (8 * 2.0) / (12 * 1.0) = 16 / 12 ≈ 1.33. Five of the losers carry the `chase` tag, for a total of -5 R, and the plan-followed rate is 14 / 20 = 70 percent. Illustrative example on hypothetical data. Not a recommendation to trade this asset or these levels.

The most useful line in that example is the last one. Five chased trades cost 5 R in a sample whose total was +4 R. Removing one repeated mistake would change the sample more than any new indicator. That is a description of invented trades, and the same question is worth asking of your own.

## Review cadence

A review is a set time to read the journal, not a reaction to the last trade.

**Daily, five minutes.** Fill in every row from today. Add the notes and screenshots while you still remember. Do not judge the framework.

**Weekly, thirty minutes.** Count the mistake tags. Read the plan_followed column. Pick one behaviour to change next week, and only one.

**Monthly, an hour.** Compute the metrics for the month and for the running total. Look at R by framework and by tag. Check whether MAE suggests stops are inside ordinary noise.

**Quarterly or per sample.** Decide in advance how many trades a framework needs before you judge it. When the sample reaches that number, compare its expectancy and drawdown with your written limits. Change the framework only then, and record the change, so the next sample is measured against the new version.

## Backtesting

A [backtest](glossary.md#backtest) applies a written rule to historical data to see what the rule would have done. It is a way of testing the rule, not the market.

**Write the rule completely first.** Entry, stop, target, size, fees, and slippage allowance. If any part is decided while looking at the chart, the test is contaminated.

**Use realistic costs.** Include fees for every fill, funding for any perpetual position, and a slippage allowance that is honest for the market's liquidity. A rule whose edge disappears after costs had no edge.

**Beware of look-ahead.** A rule cannot use a candle's close before that candle has closed, or an indicator value that changes once later data arrives.

**Beware of overfitting.** [Overfitting](glossary.md#overfitting) is tuning a rule until it fits past data closely. The more parameters you adjust, the better the past looks and the less the result means. Keep a portion of the data aside that you never tune on, and test the final rule on it once.

**Walk forward.** A [walk-forward test](glossary.md#walk-forward) tunes on one period, tests on the next, then rolls forward. It is slower and more honest than a single test on all the data.

**Replay and paper trading.** The Replay Lab on the Atlas site steps through historical candles one at a time so you can mark entries and stops without seeing what comes next. [Paper trading](glossary.md#paper-trading) runs the rule on live prices without money. A [forward test](glossary.md#forward-test) with small size comes after both. Each stage catches problems the previous one missed, and none of them is a promise about the next stage.

A backtest result describes how a rule behaved on a specific past. Markets change. A rule that suited one period may not suit another.

## Common mistakes

- Journalling only winning trades, or only trades that followed the plan.
- Changing the stop after entry and recomputing R from the new stop.
- Reviewing after every trade instead of on a schedule.
- Judging a framework after a handful of trades.
- Testing a rule on the same data used to design it.
- Ignoring fees and funding in either the journal or the backtest.

## Start small

The simplest useful journal is the template above, filled in honestly for every trade. The metrics follow from the rows. The most valuable column is often the one that says whether you followed your own plan.
