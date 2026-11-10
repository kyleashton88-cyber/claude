---
title: Technical analysis
slug: technical-analysis
level: intermediate
category: technical-analysis
related:
  - market-structure
  - risk-academy
  - glossary
last_reviewed: 2026-11-10
status: draft
---

# Technical analysis

Technical analysis is a set of measurements on price and volume that have already printed. This page is general information. Each tool below has a formula, a way to read it, and the mistakes that usually follow. A reading is not a recommendation to acquire or dispose of an asset, and it does not name a level you are supposed to trade.

Structure comes first. If you cannot mark swings, an oscillator will not invent them. The map is on the [market structure page](market-structure.md). Definitions sit in the [glossary](glossary.md).

Settings such as 14, 20, 12, and 26 are the common study defaults. They are not correct answers. Say which settings you used whenever you quote a reading.

## Support and resistance

Support is an area where declines have stalled often enough to mark. Resistance is an area where rallies have stalled often enough to mark. They can be prior swings, range edges, or round numbers where orders tend to cluster.

There is no single formula. A practical definition is: a zone is support or resistance when you can point at two or more reactions there, on a named timeframe, and you have written how close a later print must come to count as a touch.

How to read it: a hold is a reaction away from the zone. A break is a close or a wick through it, under a rule you chose in advance. A retest is a later return to the same zone. Some retests hold and some do not. The return is the observation. The outcome is not part of the definition.

Common mistakes:

- Drawing the line exactly through one wick and calling the wick a law.
- Moving the line after price goes through it, so the level can never fail.
- Treating a round number as support merely because it is round. Check whether price has actually reacted there.

## Trendlines

A trendline in an uptrend connects two or more rising swing lows. A trendline in a downtrend connects two or more falling swing highs. A parallel copy of that line, drawn off the opposite swings, is a channel.

How to read it: a third touch makes the line more interesting and does not turn it into a wall. A close through the line is the break, if that is your rule. Redraw the line when the swings you used are no longer the ones that matter.

Common mistakes:

- Forcing a line through candle bodies and wicks until it touches everything.
- Using a steep line that only the last two candles can support.
- Forgetting that a line on a log chart and a line on a linear chart are different objects.

## Simple moving average

A simple moving average of length N is the equal-weighted average of the last N closes.

```text
SMA = (C1 + C2 + ... + CN) / N
```

When a new close arrives, the oldest close drops out.

How to read it: the line lags price, because it is built only from closes already printed. A short N hugs price and whipsaws in ranges. A long N is smoother and later. A cross of a shorter SMA up through a longer SMA is the pattern often called a golden cross. The mirror cross is a death cross. Both describe the averages. Both are late by construction.

Common mistakes:

- Treating a touch of the average as a required reaction.
- Quoting a cross without the lengths and the timeframe.
- Using one average as if it were support on every market regime.

## Exponential moving average

An exponential moving average gives more weight to the newest close. The usual smoothing constant is:

```text
k = 2 / (N + 1)
EMA_today = Close_today * k + EMA_yesterday * (1 - k)
```

The first value has to start somewhere, often from an SMA of the first N closes. After that, every older close remains inside the line with a fading weight. It never drops out in one step the way an SMA's oldest close does.

How to read it: an EMA of the same N turns faster than an SMA, and it still lags. MACD is built from two EMAs. The speed is a setting, not a discovery.

Common mistakes:

- Believing the EMA "knows" the trend because it is curved.
- Comparing an EMA on one venue's closes with an SMA on another's without saying so.
- Stacking five EMAs and calling each cross a new reason. They are one family of smooth, not five independent facts.

## RSI

The relative strength index compares the size of up closes with the size of down closes. For each candle, the gain is the close-to-close rise, or zero if the close fell. The loss is the close-to-close fall, as a positive number, or zero if the close rose.

Wilder's RSI does not use a plain average after the first window. The first average gain and average loss can be simple averages over N candles (14 is the common study default). After that:

```text
avgGain = (previous avgGain * (N - 1) + current gain) / N
avgLoss = (previous avgLoss * (N - 1) + current loss) / N
RS = avgGain / avgLoss
RSI = 100 - (100 / (1 + RS))
```

If avgLoss is zero, the usual convention is to treat RSI as 100, because there has been no down close in the smoothed window. The scale runs from 0 to 100.

How to read it: a high reading means up closes have dominated that window. A low reading means down closes have dominated it. Bands near 70 and near 30 are teaching zones for "overbought" and "oversold". Those words describe the window. They do not mean price must reverse. In a strong trend, RSI can stay high or low while the trend continues.

Common mistakes:

- Fading every reading above 70 in an uptrend.
- Using a different N and still quoting "the" RSI.
- Calling a hidden or regular divergence a timer. Divergence is a disagreement, covered below, and it can persist.

## MACD

MACD is the difference between two exponential moving averages of the close. The common study defaults are 12 and 26 for the averages, and 9 for the signal.

```text
MACD line = EMA(12) - EMA(26)
Signal line = EMA(9) of the MACD line
Histogram = MACD line - Signal line
```

How to read it: the MACD line is positive when the shorter average is above the longer one. A cross of the MACD line through the signal says the gap between them has flipped relative to its own smooth. A histogram bar that is shrinking means the gap is narrowing, which can happen while price is still making new highs or new lows.

Common mistakes:

- Treating a signal cross as a scheduled turn in price.
- Forgetting that MACD is in price units, so a reading of 50 on one asset is not comparable with 50 on another.
- Changing 12, 26, and 9 until a backtest looks neat. That is a path to overfitting, which the [risk page](risk-academy.md) discusses as a research problem.

## VWAP

The volume-weighted average price for a session is:

```text
VWAP = sum(Price_i * Volume_i) / sum(Volume_i)
```

The usual price input is the typical price of each bar, (high + low + close) / 3. Some feeds use the price of each trade instead. A new session usually resets the sums. An anchored VWAP starts the sums at a candle you choose rather than at the session open. The anchor is a judgement.

How to read it: VWAP is the average price weighted by how much traded. It is a reference for that session, not a price you can necessarily deal at in size. Price far from VWAP on heavy volume is a different event from price far from VWAP on a dead print.

Common mistakes:

- Leaving the session undefined, so two people compute two VWAPs.
- Using an anchor you chose after seeing the outcome.
- Treating VWAP as a mean that price must touch before the session ends.

## Bollinger Bands

Bollinger Bands place a simple moving average in the middle and bands a number of standard deviations away. The common study defaults are length 20 and a width of 2.

```text
Middle = SMA(N)
Upper = Middle + k * σ
Lower = Middle - k * σ
```

Here σ is the standard deviation of the same N closes. Bollinger's original construction uses the population standard deviation, dividing the sum of squared deviations by N, not by N - 1. A chart that uses the sample divisor will not match that construction exactly.

How to read it: the bands widen when recent closes are more dispersed and narrow when they are quiet. A narrow band is compression. It does not say which way the next expansion will go. A close outside a band is a large move relative to that recent dispersion. It is a location, not an automatic fade.

Common mistakes:

- Fading every tag of the band. In a trend, closes can walk the band.
- Comparing a band touch on one length with a story you learned on another.
- Calling the middle band support without any swings to agree with it.

## ATR

True range is the widest of three distances:

```text
TR = max(high - low, absolute(high - previous close), absolute(low - previous close))
```

The gaps against the previous close matter, because a bar that opens far away has travelled even if its own high-low range is small.

Average true range is a Wilder smooth of true range, the same smoothing shape as RSI. With period N (14 is the common study default):

```text
ATR = (previous ATR * (N - 1) + TR) / N
```

The first ATR is often a simple average of the first N true ranges, and the Wilder form takes over after that.

How to read it: ATR is a distance, in price, of recent movement. It is not a direction. A stop placed a fixed number of ATRs away is a volatility-scaled distance. Whether that distance fits the account is a sizing question on the [risk page](risk-academy.md), not a property of ATR itself.

Common mistakes:

- Using ATR as a target for how far price "should" go.
- Mixing an ATR from a daily chart with a stop on a five-minute chart without saying so.
- Forgetting that a sudden gap updates ATR only after the fact. The stop you needed was the one already in the market.

## Volume

Volume is the amount traded in the period, in coins or in contracts, depending on the feed. Crypto feeds disagree, because venues differ and because some figures double-count.

On-balance volume is a running total: add the period's volume when the close is up, and subtract it when the close is down. Relative volume divides this period's volume by a baseline, such as the average for that same hour. Volume profile sums volume by price instead of by time. The point of control is the price bin with the most volume. The value area is the band around it that contains a chosen share of volume, often taught as about 70 percent of the profile.

How to read it: a price push on heavy volume had more participation than the same push on light volume, on that feed. A profile peak is where business clustered in the window you chose. Change the window and the peak can move.

Common mistakes:

- Treating volume as comparable across unrelated chains or venues.
- Reading a profile built on a thin feed as if it were the whole market.
- Using on-balance volume's level, rather than its disagreement with price, as if the level had a unit.

## Patterns

A chart pattern is a named shape in the swings: a double top, a double bottom, a head and shoulders, a triangle, a flag. The name helps you point at the shape.

A double top is two highs at a similar price with a trough between them. The textbook waits for a break of that trough, often called the neckline, before it calls the pattern complete. Two highs alone are equal highs. A head and shoulders adds a higher middle peak. A triangle is two converging lines. A flag is a short pause against a prior impulse.

How to read it: the pattern is complete only at the event the definition requires, usually a break of a boundary you marked in advance. Measured distances in old textbooks are descriptions of samples. They are not a price the current market must reach.

Common mistakes:

- Naming a pattern before the boundary has broken.
- Moving the neckline until the break is already obvious, then claiming the pattern predicted it.
- Ignoring the timeframe. A head and shoulders on a one-minute chart is not the same object as one on a weekly chart.

## Divergence

Regular divergence: price makes a new extreme and the oscillator does not. A higher high in price with a lower high on RSI is the usual bullish-to-bearish teaching example, and the mirror is a lower low in price with a higher low on the oscillator.

Hidden divergence is the trend-continuation form. In an uptrend, price makes a higher low while the oscillator makes a lower low. In a downtrend, price makes a lower high while the oscillator makes a higher high.

How to read it: divergence is a disagreement between price and a formula over the same window. It can resolve by price turning, by the oscillator catching up, or by both going quiet. It is not a clock.

Common mistakes:

- Drawing divergence between points that are not real swings.
- Taking divergence against a higher-timeframe trend with no invalidation written down.
- Using MACD divergence and RSI divergence as two votes when both are smoothed versions of the same closes.

## Confluence

Confluence is several independent observations in the same price area. Independent means a different question: a higher-timeframe swing, a session VWAP, and a round number are three questions. Three moving averages of similar length are one question asked three times.

How to read it: overlap is a reason to look more carefully, not a reason to skip the invalidation. More labels do not create more evidence if they share the same inputs.

Common mistakes:

- Counting every tool that happens to be nearby.
- Adding a tool after you have decided, so the stack can only agree.
- Letting confluence replace position size. Agreement on a level does not tell you how large the loss will be if you are wrong. That arithmetic is on the [risk page](risk-academy.md).
