---
title: Market structure
slug: market-structure
level: beginner
category: market-structure
related:
  - technical-analysis
  - risk-academy
  - glossary
last_reviewed: 2026-11-10
status: draft
---

# Market structure

Market structure is the map of swing highs and swing lows on a timeframe you name. This page is general information. It shows how to read candles, trends, ranges, breaks, and liquidity. It is not an instruction to enter a trade, and it does not set a price to aim at.

The same words appear in the [glossary](glossary.md#market-structure). Use this page when you want the sequence, and the glossary when you want one definition.

## Candles

A candlestick is one period. It has four prints:

- **Open** is the first price of the period.
- **High** is the highest price traded.
- **Low** is the lowest price traded.
- **Close** is the last price of the period.

The **body** is the distance from open to close. A candle that closes above its open is bullish. A candle that closes below its open is bearish. The **wick** (or shadow) is the line from the body out to the high or the low. A long wick means price traded there and did not finish there.

Colour is a convention of the chart, not a fact of the market. Read the legend.

How to read a single candle:

- A large body means the period finished far from where it started.
- A small body means the open and the close were close together.
- A wick through a level, with the close back inside, is a rejection of that extreme for that one candle only.

Common mistakes:

- Treating one candle as a complete story. The swings around it decide whether it mattered.
- Calling every wick a reversal. A wick is a print inside one period.
- Forgetting the timeframe. A large candle on a one-minute chart can be noise on a daily chart.

## Swings

A **swing high** is a high with lower highs on both sides, under a left-and-right rule you keep constant. A **swing low** is a low with higher lows on both sides, under the same kind of rule. Those two posts are the structure. If you change how many candles must sit on each side, you change the map, so write the rule down.

A single wick is not automatically a swing. It becomes a swing only when the candles after it confirm that the extreme held, under your rule.

## Trend and range

On the timeframe you are mapping:

- An **uptrend** is a sequence of higher highs and higher lows.
- A **downtrend** is a sequence of lower highs and lower lows.
- A **sideways market**, or trading range, is two-way trade between a ceiling and a floor, without that sustained sequence.

A trend on a small timeframe can be a pullback inside a larger timeframe's range, or the other way around. Name the timeframe in the same sentence as the trend.

A range is the usual study case for a neutral grid, because the bot is built to buy and sell inside a band. The range is a hypothesis. Price does not owe you the band.

How to tell them apart in practice:

1. Mark the last few swing highs and swing lows.
2. Ask whether each new swing continued the sequence or broke it.
3. If you cannot mark the swings, you do not yet have a regime. Do not borrow a name from a headline.

Common mistakes:

- Calling a market a trend because the last candle was large.
- Drawing a range so wide that almost any path fits inside it.
- Switching the definition after the fact so the label still matches what happened.

## Break of structure and change of character

A **break of structure** (BOS) continues the swing direction you were already mapping. In an uptrend, that is a move beyond the most recent swing high. In a downtrend, it is a move beyond the most recent swing low.

A **change of character** (CHoCH), sometimes called a market structure shift, is a break *against* that sequence. In an uptrend, the usual study point is a loss of the higher low that the trend needed. In a downtrend, it is a rally through the lower high that had been capping price.

Teachers disagree on whether a wick is enough or whether the candle must close through the swing. Pick one rule and keep it. A wick rule will mark more breaks, including more failures. A close rule will mark fewer, later.

A BOS or a CHoCH is a description of swings that have printed. It is not an order to take a position. The invalidation of the map is the swing your rule said must hold. If that swing fails, the map is the thing that changed.

Common mistakes:

- Labelling every small dip a change of character while the higher-timeframe sequence is intact.
- Using a wick on one timeframe and a close on another without saying so.
- Treating the break as a forecast of how far price will travel afterwards.

## Liquidity

**Liquidity**, in the execution sense, is how much you can trade without moving the price much. **Liquidity**, in the structure sense, is the cluster of stops and resting orders that often sit beyond obvious highs and lows. This page uses the second sense. The [glossary entry](glossary.md#liquidity) records both.

A **liquidity pool** on a chart is an inferred cluster, often just beyond **equal highs** or **equal lows**. You infer it because many people put stops there. You cannot see the private book. **Buy-side liquidity** is the cluster inferred above highs. **Sell-side liquidity** is the cluster inferred below lows. The words name a location. They do not tell you to buy or to sell.

A **liquidity sweep** is a push through that location which then returns back inside. You can call it a sweep only after the return. Planning for the possibility is different from knowing it in advance.

**Inducement**, in this teaching, is a minor obvious swing sitting in front of a larger pool. The hypothesis is that price may trade the small swing before the larger one. It is a map of possible stops, not a timetable.

Common mistakes:

- Drawing pools on every high until the word means nothing.
- Assuming a sweep must reverse. Some pushes through a high simply become the new trend.
- Confusing this chart idea with an AMM pool, which is a contract holding token reserves. The [AMM pool entry](glossary.md#amm-pool) is the other object.

## Order blocks and fair value gaps

An **order block** is a candle, or a small group of candles, at the origin of a strong move, which some methods mark as a place to study if price later returns. The label is a hypothesis about where trading clustered on the chart. It is not evidence that you can see a resting order from a named institution.

**Displacement** is the decisive push that leaves the prior area, often with large bodies and little overlap. Without displacement, a candle is just a candle. **Mitigation** is a later return into the marked area. The return is visible. What price does after the return is not included in the word.

A **breaker** is an order-block area that failed and, in that method, swaps roles on a later retest. It is a labelling rule.

A **fair value gap** (FVG) is a three-candle pattern. The wick of the candle before the middle candle and the wick of the candle after it do not overlap, so a price gap is left beside the middle candle. Traders study whether later trade returns into that gap. A gap is a description of prints. It is not an unfilled order you can audit on a venue.

Common mistakes:

- Marking every candle that touches a move as an order block.
- Treating a gap fill as required. Many gaps are never fully traded again.
- Stacking three names (block, gap, sweep) on the same candles and calling the pile confluence. Confluence needs independent questions, which the [technical analysis page](technical-analysis.md#confluence) covers.

## Premium, discount, and the dealing range

Pick a swing high and a swing low. That distance is the **dealing range**. The midpoint is **equilibrium**. Above it is **premium**. Below it is **discount**.

Some frameworks prefer to study rallies into premium and dips into discount, relative to the trend they have mapped. That is a location filter. Discount does not mean the asset is cheap in any fundamental sense. A different pair of swings produces a different midpoint.

## Multi-timeframe work

Use a higher timeframe for the larger swing map and a lower timeframe for the detail of the current push.

A practical order:

1. Mark the higher-timeframe trend or range, and the swing that would invalidate it.
2. Drop one or two steps to see how the current push is built: impulse, correction, sweep, or compression.
3. Write whether the lower-timeframe idea agrees with the higher-timeframe sequence or fights it. A fight is allowed only if the plan says why.
4. Do not average the timeframes into a vote. They are nested maps, not ballots.

Common mistakes:

- Letting a one-minute change of character cancel a daily uptrend without saying you have changed maps.
- Hunting a lower-timeframe entry in the middle of a higher-timeframe range and calling it a trend trade.
- Changing timeframe after a loss until a picture appears that excuses the loss.

## A small routine

Before you describe a market, you should be able to answer, in this order:

1. Which timeframe is the map?
2. What are the last swing high and swing low?
3. Is the sequence an uptrend, a downtrend, or a range?
4. What print would be a break of structure, and what print would be a change of character?
5. Where are the obvious equal highs or equal lows, if any?
6. What does the next higher timeframe say about the same swings?

If one of those answers is missing, the next step is to mark the chart, not to add an indicator. Indicators are on the [technical analysis page](technical-analysis.md). The size of any position you might later take is on the [risk page](risk-academy.md).
