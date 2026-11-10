---
title: Risk academy
slug: risk-academy
level: intermediate
category: risk
related:
  - market-structure
  - technical-analysis
  - glossary
last_reviewed: 2026-11-10
status: draft
---

# Risk academy

Risk is the amount you can lose if the idea is wrong, sized before you act. This page is general information. The formulas describe arithmetic. They do not choose a size for you, they do not promise a result, and they are not personal advice. Consider your own circumstances.

Worked numbers below are invented so the arithmetic is visible. Each block is marked as a hypothetical example. None of them is a record of a live account.

The map of swings is on the [market structure page](market-structure.md). The measurements on price are on the [technical analysis page](technical-analysis.md). Short definitions are in the [glossary](glossary.md#drawdown).

## Position sizing

Decide the cash you are willing to lose if the stop is hit. That is the risk per trade. Then divide by the stop distance, in price per unit.

```text
cash at risk = equity * risk fraction
units = cash at risk / stop distance
```

Stop distance is the gap between the entry and the invalidation, in price. A wider stop means fewer units for the same cash at risk. Fees and slippage make the real loss larger than this figure if the fill is worse than the stop price, so the cash at risk in the formula should already include an allowance you believe is realistic.

The risk fraction is a ceiling you choose. This page cannot set it. A smaller fraction survives a longer run of losses and grows more slowly when the sample is favourable. Both halves of that sentence matter.

Hypothetical example. Equity is 10000 quote units. The plan risks 1 percent of equity, so cash at risk is 100 quote units. The invalidation is 2 quote units away from the entry. Units = 100 / 2 = 50. Illustrative example on hypothetical data. Not a recommendation to trade this asset or these levels.

Common mistakes:

- Sizing from a feeling about the asset, then placing the stop wherever that size happens to fit.
- Ignoring the gap between the stop trigger and the fill.
- Adding several positions that fall together, so the account risk is the sum, not the single-line figure. That sum is portfolio heat.

## R multiples

One R is the cash you planned to lose if the stop was hit. A result stated in R is the money gained or lost, divided by that initial risk.

```text
R multiple = result / initial risk
```

A gain of twice the planned risk is +2 R. A loss of the planned risk is -1 R. Stating results in R lets you compare trades with different prices and different sizes. It does not make a losing trade into a winning process.

Hypothetical example. Initial risk is 100 quote units. The closed result is a gain of 180 quote units. The R multiple is 180 / 100 = 1.8 R. A second trade loses the full 100, which is -1 R. Illustrative example on hypothetical data. Not a recommendation to trade this asset or these levels.

Common mistakes:

- Moving the stop wider and still calling the original risk "one R". The R has changed.
- Counting a paper gain as R before the position is closed.
- Comparing R across a strategy that sometimes has no stop. If the loss was not defined, the multiple is not defined.

## Stops

A stop is the invalidation made executable: a price, a close, or a time at which the idea is wrong or the loss has reached the plan.

- A **hard stop** is an order resting at the venue.
- A **trailing stop** moves in your favour under a rule written beforehand, such as a fixed distance or a multiple of ATR.
- A **time stop** forces a review or an exit after a set number of candles if nothing has happened.

ATR, from the technical page, can scale a distance to recent movement. It does not know your account. A 2 ATR stop on a huge account and a 2 ATR stop on a small account are the same distance and a different fraction of equity. Run the position-size formula after you pick the distance.

A stop can fill worse than its price in a fast market or a gap. The formula's cash at risk is a plan, not a promise that the venue will complete the order at that print.

Common mistakes:

- Putting the stop inside ordinary noise so the idea is never allowed to work, then widening it only after you are in.
- Using a mental stop and calling it equivalent to a hard stop. They fail in different ways.
- Trailing so tightly that ordinary candles knock out a position the plan still called valid.

## Expectancy

Expectancy is the average result per trade in a sample you already have. With the average loss written as a positive number:

```text
expectancy = (win fraction * average win) - (loss fraction * average loss)
```

The win fraction and the loss fraction are shares of the sample, and they add to one if every trade is either a win or a loss. In R units, use the average win and the average loss in R. A positive expectancy means the average of that sample was a gain. It is a description of those trades. It is not a forecast of the next trade, and it is not a promise about a future return.

The payoff ratio is the average win divided by the average loss. Either figure alone is incomplete. A high share of winners still loses money if the losers are large enough. A low share of winners can still show a positive average if the winners are large enough. Quote them together, and quote the sample size.

Hypothetical example. In a made-up sample of ten closed trades, four are winners and six are losers. The average winner is 2 R and the average loser is 1 R. Expectancy = (0.4 * 2) - (0.6 * 1) = 0.2 R per trade. That sentence describes these ten invented results and no other account. Illustrative example on hypothetical data. Not a recommendation to trade this asset or these levels.

Common mistakes:

- Publishing the share of winners and hiding the size of the losers.
- Computing expectancy on open trades, marked at a favourable moment.
- Reshaping the rule after seeing the sample, then treating the new average as if it had been specified in advance. That is overfitting.

## Drawdown and the recovery fraction

Drawdown is the fall from an equity peak to a later trough, divided by the peak.

```text
d = (peak - trough) / peak
```

Maximum drawdown is the deepest such fall in the sample. It is a fact about that path. A later path can be worse.

The rise required to regain the peak, as a fraction of the equity you have left, is:

```text
recovery = 1 / (1 - d) - 1
```

If d is one half, 1 - d is one half, and the recovery fraction is 1 / (1/2) - 1 = 1. The remaining equity must double. A deeper d demands a much larger rise than the decline itself, because you are compounding off a smaller base. The formula is arithmetic. It does not say the rise will happen.

Hypothetical example. A peak of 1000 quote units falls to 800. Then d = (1000 - 800) / 1000 = 0.2. Recovery = 1 / (1 - 0.2) - 1 = 0.25. The 800 must rise by a quarter of itself, which is 200, to see 1000 again. Illustrative example on hypothetical data. Not a recommendation to trade this asset or these levels.

Hypothetical example. The same peak falls to 500, so d = 0.5. Recovery = 1 / (1 - 0.5) - 1 = 1. The remaining 500 must double. The decline was one half of the peak. The repair, measured on what is left, is the whole of what is left. Illustrative example on hypothetical data. Not a recommendation to trade this asset or these levels.

Common mistakes:

- Comparing a decline of one tenth with a later rise of one tenth and calling the account restored. One tenth of the smaller number does not refill the peak. Use the formula.
- Quoting a maximum drawdown from a short, smooth sample as if it were a cap.
- Adding leverage so the same price path produces a deeper d. The recovery fraction then belongs to the leveraged equity, not to the unlevered story.

## Monte Carlo

A Monte Carlo study takes a sample of trade results and builds many alternate paths. The usual simple version reshuffles the same results into a new order, thousands of times, and records the equity curve of each order. You then look at the spread: how deep the drawdowns were across paths, and how often a path touched a ruin level you defined.

What it can show: path risk inside that sample. Two traders with the same trades in a different order live through different drawdowns. The average expectancy can match while the worst path does not.

What it cannot show: a result the sample does not contain. If the historical trades had no fee, the reshuffle has no fee. If you tuned the rule on the same trades, the reshuffle repeats the tuning. New regimes, broken feeds, and a size that moves the market are not created by shuffling.

Hypothetical example. Five invented R results, -1, -1, +2, -1, +3, have the same average in every order. One order might take both losses first. Another might take the gains first. The ending sum of this list is the same. The deepest drop along the way is not. Illustrative example on hypothetical data. Not a recommendation to trade this asset or these levels.

A practical study also states the ruin line in advance, for example equity down by a fraction you refuse to cross, and counts the share of reshuffled paths that touch it. That share is a property of the model and the sample. Change the size per trade and the share changes, which is the point of doing the exercise before size is live.

Common mistakes:

- Running the shuffle on a handful of trades and treating the pretty middle path as evidence.
- Replacing losers with a hoped-for average before the shuffle, which hides the tail.
- Confusing a Monte Carlo fan with a forecast of the next month.

## A pre-trade check

Before size is live, write four numbers and one sentence:

1. Cash at risk if the stop fills at the planned price, including a slippage allowance.
2. Stop distance, and the units that distance implies.
3. Portfolio heat if this idea is added to what is already open.
4. The invalidation, in a form someone else could check on a chart.
5. One sentence on why this idea is not the same bet as the positions you already hold.

If you cannot fill those in, the missing piece is the plan, not another indicator. The record of what you then do belongs in a journal, so expectancy is computed on trades you actually took.
