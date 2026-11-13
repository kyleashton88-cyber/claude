---
title: Market strategies
slug: market-strategies
level: intermediate
category: strategy
related:
  - market-structure
  - technical-analysis
  - risk-academy
  - journal-lab
last_reviewed: 2026-11-10
status: draft
---

# Market strategies

A strategy, on this page, is a written framework: the conditions it needs, what would prove it wrong, how risk is set, and how you will review it. That is all it is. This page does not give signals, it does not say any framework works, and it does not compare their results, because no framework has a result until someone defines it precisely and tests it on their own data. It is general information, not personal advice. Consider your own circumstances.

Worked numbers below are invented so the logic is visible. Each block is marked as a hypothetical example. The words for swings and ranges are on [market structure](market-structure.md). The indicators are on [technical analysis](technical-analysis.md). Sizing is on the [risk academy](risk-academy.md). Short definitions are in the [glossary](glossary.md#trading-plan).

## The four parts of every framework

Each strategy below is described with the same four headings. If you cannot fill all four for your own version, you have an idea, not yet a framework.

1. **Conditions.** The market state the idea needs: a trend, a range, a level of volatility, a timeframe. Written so that someone else could check them on a chart.
2. **Invalidation.** The price, close, or time at which the idea is wrong. This is where the stop goes, or where the review starts.
3. **Risk.** How much is at risk per position and in total, using the [position-sizing formula](risk-academy.md#position-sizing).
4. **Review.** What you will record, how often you will look, and what sample size you need before you judge it.

The review part is what turns a story into something you can learn from. It also keeps you honest about how many trades a judgement needs. A few trades say very little.

## Trend following

**Idea.** Price that is already moving in one direction on a chosen timeframe is joined in that direction, with an exit when the trend structure breaks.

**Conditions.** A defined [trend](glossary.md#trend): for example higher highs and higher lows on the chosen timeframe, or price above a moving average that is itself rising. The definition must be written before you look at the chart you are trading.

**Invalidation.** A break of the most recent [swing low](glossary.md#swing-low) in an uptrend, or a close back through the moving average, depending on the rule you chose. Using both is fine as long as you decide in advance which one acts first.

**Risk.** Trend frameworks often accept a lower share of winning trades in exchange for occasional large moves. That shape means long runs of small losses are normal for the design. Size so that a long run does not breach your drawdown limit.

**Review.** Measure results in [R](risk-academy.md#r-multiples). Check whether losses cluster in ranging periods, because that is where trend rules usually struggle. The question for review is whether your rule spots ranges, not whether the last trade won.

## Swing trading

**Idea.** Hold a position across several candles to capture one leg of a larger structure, entering near a level and exiting at the next.

**Conditions.** A clear higher-timeframe direction, a pullback to a level you can name in advance (a prior swing, a [fair value gap](glossary.md#fair-value-gap), or a moving average), and a reaction at that level on the lower timeframe.

**Invalidation.** Beyond the swing point that formed the pullback. If that point breaks, the leg you expected has not formed.

**Risk.** The stop sits behind structure, so its distance varies trade to trade. Position size must vary with it. Holding overnight or over a weekend adds gap risk that a stop may not contain.

**Review.** Record the planned target and where price actually reached, as [maximum favourable excursion](glossary.md#mfe). Over a sample, that shows whether your targets are realistic for the timeframe.

Hypothetical example. On a made-up chart, the higher timeframe shows higher highs. Price pulls back to a prior swing high at 50, now acting as support, and prints a rejection candle. A swing framework would put the entry near 50.5, the invalidation below the pullback low at 48.5, and the first target at the prior high of 56. Risk is 2 per unit and the distance to target is 5.5, so the planned reward is 2.75 R. Illustrative example on hypothetical data. Not a recommendation to trade this asset or these levels.

## Breakout

**Idea.** When price leaves a well-defined range or pattern with strength, the framework joins the move out.

**Conditions.** A range or pattern you can draw before the break, a close beyond the boundary on the chosen timeframe, and, if your rule uses it, above-normal volume on the break.

**Invalidation.** A close back inside the range. A [false breakout](glossary.md#false-breakout) is the most common way this framework is wrong, and it should be written into the rule rather than treated as bad luck.

**Risk.** Entries near the boundary can suffer slippage when many orders arrive at once. Stops just inside the range are prone to being hit by retests. Some frameworks wait for a [retest](glossary.md#retest) of the boundary to reduce that, at the cost of missing moves that do not come back.

**Review.** Count how many breaks returned inside the range within a set number of candles. That share, on your market and timeframe, tells you more than any textbook pattern success figure.

## Range and mean reversion

**Idea.** In a market moving sideways between defined boundaries, sell near the top and buy near the bottom, expecting a return toward the middle.

**Conditions.** A [range](glossary.md#range) with at least two touches of each boundary, and evidence that the trend has paused, such as flat moving averages or a narrow band of [Bollinger Bands](technical-analysis.md#bollinger-bands). This is also the condition a grid bot needs, which is why grids are a form of this framework.

**Invalidation.** A close beyond the boundary. Range frameworks are wrong when a range becomes a trend, and that change is sudden.

**Risk.** Many small gains and occasional large losses is the typical shape, the reverse of trend following. One unstopped breakout can erase a long series of small cycles. A hard stop outside the range is not optional for this design.

**Review.** Record how long ranges lasted and how they ended. Track the share of trades closed by the range-break stop. If that share is high, the conditions rule is too loose.

## Dollar-cost averaging

**Idea.** Buy a fixed amount at fixed intervals regardless of price, so the average cost reflects many prices instead of one.

**Conditions.** A decision, made in advance and on research outside the chart, that you want exposure to that asset over a long period. Dollar-cost averaging is a method of entry, not a reason to own something.

**Invalidation.** The framework has no price stop by design. Its invalidation is a change in the reason you wanted the exposure, which should be written down at the start so you can tell when it changes.

**Risk.** Averaging smooths the entry price. It does not reduce the risk that the asset itself falls over the whole period. The total committed, not the size of one purchase, is the figure to compare with what you could afford to lose.

**Review.** Review on a schedule, perhaps quarterly, not after every price move. Check the original reason, fees paid, and whether the total exposure still matches your plan.

Hypothetical example. A plan buys 100 quote units of a made-up asset each month for four months at prices of 10, 8, 5, and 10. The units bought are 10, 12.5, 20, and 10, a total of 52.5 units for 400 quote units. The average cost is 400 / 52.5 ≈ 7.62 per unit, below the simple average price of 8.25, because more units were bought when the price was lower. Illustrative example on hypothetical data. Not a recommendation to trade this asset or these levels.

With a fixed amount per purchase, the average cost is never above the simple average of the purchase prices. That is arithmetic, not a gain. If the price had kept falling, the average cost would still be above the latest price. Averaging changes the entry. It does not choose the asset.

## Long-term holding

**Idea.** Hold an asset through volatility for years, based on a view of its long-run role, and trade it rarely.

**Conditions.** A written thesis about the asset that does not depend on short-term price: what it is for, why it would still matter in years, and what would change your mind.

**Invalidation.** Evidence against the thesis, not a price level. Examples include a design failure, a change in governance, a loss of the use case, or a custody problem you cannot fix.

**Risk.** Drawdowns in crypto assets have historically been deep and long, and a future one could be deeper. Past drawdowns are not a floor. Long-term holding also concentrates custody risk over years, so the [security page](security.md) matters more here than in any trading framework.

**Review.** Annual, against the written thesis. Rebalancing rules, if you use them, should be written before the drawdown, not during it.

## Spot versus futures

The same framework behaves differently in spot and in derivatives. In spot, the worst case is the loss of the amount bought. In futures, leverage brings [liquidation](glossary.md#liquidation), funding costs, and the gap between mark and last price. A framework that is reasonable in spot can fail in futures purely because the liquidation price sits inside the invalidation. Read [futures and leverage](futures-leverage.md) before you move any framework from one to the other.

## Choosing between frameworks

The market state usually decides which framework fits, not preference. A trending market suits trend and swing frameworks and punishes range rules. A ranging market suits range rules and punishes breakout entries. Many traders write one framework for each state and a rule for deciding which state is present. Others trade only one framework and stand aside when its conditions are absent. Standing aside is a valid output of a framework.

Write your own version of any framework here in the [journal](journal-lab.md), test it on historical data or by paper trading first, and judge it on a sample large enough to mean something. Nothing on this page is a substitute for that test.
