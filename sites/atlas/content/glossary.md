---
title: Glossary
slug: glossary
level: beginner
category: reference
related:
  - market-structure
  - technical-analysis
  - risk-academy
last_reviewed: 2026-11-10
status: draft
---

# Glossary

Atlas is one library for every market: a dictionary of crypto and trading ideas, written as general information. Each entry says what a term means, in plain English, so you can read a chart, a bot ticket, or a protocol page without guessing. Nothing here is personal advice, and nothing here is an instruction to acquire or dispose of an asset.

Stewart's grid-bot glossary is folded in under Grid trading, using the same meanings as that module: range, arithmetic and geometric spacing, realised and unrealised results, funding, and the rest. DeFi and on-chain ideas from the DeFi library are included as their own entries, including pools, health factor, impermanent loss, oracles, and the research metrics. Where a structure lesson and a DeFi lesson share a phrase, the entry says which meaning is which.

Levels mark how much context you need, not a rank of importance. Beginner entries are the words that unlock the rest. See also links jump to the anchor on this page.

## Categories

- [Grid trading](#grid) (25)
- [Market structure](#market-structure) (57)
- [Technical analysis](#technical-analysis) (56)
- [Risk](#risk) (26)
- [Derivatives and leverage](#derivatives) (31)
- [Venues, orders, and registration](#execution) (45)
- [Wallets and security](#security) (26)
- [Crypto fundamentals](#crypto) (71)
- [DeFi](#defi) (52)
- [On-chain data](#on-chain) (13)
- [Portfolio](#portfolio) (5)
- [Research, testing, and journaling](#research) (10)
- [Automation](#automation) (3)
- [Psychology](#psychology) (5)
- [Macro and cross-market context](#macro) (10)

This file defines 435 terms. The same rows live in `glossary.json` for the site to load.

## Grid trading

<a id="grid"></a>

### Arithmetic Grid

<a id="arithmetic-grid"></a>

*Grid levels spaced by an equal price distance.* Level: intermediate.

An arithmetic grid keeps the same price gap between levels, such as a fixed quote-currency step. The percentage gap gets smaller as price rises, because the same step is a smaller share of a higher price. It is the simpler spacing rule.

See also: [Geometric Grid](#geometric-grid), [Grid Spacing](#grid-spacing), [Grid Level](#grid-level).

### Capital Allocation

<a id="capital-allocation"></a>

*How much capital is assigned to a bot and its orders.* Level: beginner.

Capital allocation is the amount you set aside for a grid, a position, or a book of positions. It includes the size of each order and the reserve you are not willing to use. A larger allocation is a larger loss if the idea fails.

See also: [Position Sizing](#position-sizing), [Order Size](#order-size), [Risk Budget](#risk-budget).

### Fee Drag

<a id="fee-drag"></a>

*The share of each grid step consumed by fees and slippage.* Level: intermediate.

Fee drag is the cost that sits between the gross distance of a grid step and what is left after maker or taker fees and slippage. Dense grids feel this first. If the planned step does not clear those costs, more trades do not repair the design.

See also: [Maker Fee](#maker-fee), [Taker Fee](#taker-fee), [Grid Spacing](#grid-spacing).

### Floating P&L

<a id="floating-pnl"></a>

*Another name for open, unrealised profit and loss.* Level: beginner.

Floating profit and loss is the open result that has not been locked. Venues and bots often use it as a synonym for unrealised profit and loss. Treat the label as a mark, not as cash you can already count.

See also: [Unrealised P&L](#unrealised-pnl), [Mark Price](#mark-price), [Inventory](#inventory).

### Futures Grid

<a id="futures-grid"></a>

*A grid run with derivatives exposure, often with leverage.* Level: intermediate.

A futures grid uses perpetual or dated contracts, and it may use leverage, funding, and a liquidation price. The grid logic is similar to spot, and the risk model is not. Funding and margin need a review before launch and while it runs.

See also: [Spot Grid](#spot-grid), [Leverage](#leverage), [Funding Rate](#funding-rate).

### Geometric Grid

<a id="geometric-grid"></a>

*Grid levels spaced by an equal percentage distance.* Level: intermediate.

A geometric grid keeps the same percentage gap between levels. The price gap grows as price rises, which is useful when a wide range makes a percentage step more meaningful than a fixed step. It does not remove fees or inventory risk.

See also: [Arithmetic Grid](#arithmetic-grid), [Grid Spacing](#grid-spacing), [Volatility](#volatility).

### Grid

<a id="grid"></a>

*A set of predefined price levels with orders inside a range.* Level: beginner.

A grid is the ladder of price levels a bot uses between an upper and a lower boundary. Each level can hold an order, and a finished round trip between two levels is one cycle. The grid does not pick the range or the risk for you.

See also: [Range](#range), [Grid Level](#grid-level), [Grid Cycle](#grid-cycle).

### Grid Count

<a id="grid-count"></a>

*How many levels sit inside the range.* Level: intermediate.

Grid count is the number of order levels between the upper and lower price. Raising the count inside a fixed range makes each step smaller. A step that is smaller than fees and slippage can turn a busy bot into a losing one.

See also: [Grid Spacing](#grid-spacing), [Fee Drag](#fee-drag), [Grid Level](#grid-level).

### Grid Cycle

<a id="grid-cycle"></a>

*One completed round trip between two grid levels.* Level: beginner.

A grid cycle is a buy and a later sell, or a sell and a later buy, that closes one step of the ladder. The gross step minus fees and slippage is the cycle result. Counting cycles without subtracting costs overstates the bot.

See also: [Grid Profit](#grid-profit), [Grid Spacing](#grid-spacing), [Fee Drag](#fee-drag).

### Grid Level

<a id="grid-level"></a>

*One order line inside the range.* Level: beginner.

A grid level is a single price in the ladder where an order can sit. The distance to the next level is the spacing. More levels inside the same range means tighter spacing.

See also: [Grid](#grid), [Grid Spacing](#grid-spacing), [Grid Count](#grid-count).

### Grid Profit

<a id="grid-profit"></a>

*Realised result from completed buy and sell cycles.* Level: beginner.

Grid profit is the locked result of finished round trips, before you judge the open inventory. It can look positive while total profit and loss is negative, because coins still held can be marked below their cost. Read both numbers.

See also: [Realised P&L](#realised-pnl), [Unrealised P&L](#unrealised-pnl), [Grid Cycle](#grid-cycle).

### Grid Spacing

<a id="grid-spacing"></a>

*The price or percentage gap between two levels.* Level: intermediate.

Grid spacing is the distance from one level to the next, in price or in percent. It has to be wide enough that a finished cycle still clears fees and expected slippage. Tighter spacing means more trades and a smaller gross step.

See also: [Arithmetic Grid](#arithmetic-grid), [Geometric Grid](#geometric-grid), [Fee Drag](#fee-drag).

### Inventory

<a id="inventory"></a>

*The coins or contracts a grid still holds open.* Level: beginner.

Inventory is the position the bot has accumulated and not yet closed. In a spot grid that often means more of the base asset after a decline. Inventory can show an unrealised loss even when completed cycles show a grid profit.

See also: [Unrealised P&L](#unrealised-pnl), [Grid Profit](#grid-profit), [Base Asset](#base-asset).

### Long Grid

<a id="long-grid"></a>

*A grid configured with bullish directional exposure.* Level: intermediate.

A long grid is tilted so the inventory or the futures exposure benefits if price rises, while still using grid levels. The directional tilt is extra risk on top of ordinary grid inventory. It is a configuration, not a view that price will rise.

See also: [Neutral Grid](#neutral-grid), [Short Grid](#short-grid), [Long](#long).

### Lower Price

<a id="lower-price"></a>

*The bottom boundary of the grid.* Level: beginner.

The lower price is the lowest level in the planned range. Below it, the bot is outside the area you mapped. It is a design choice, not a forecast of the low.

See also: [Range](#range), [Upper Price](#upper-price), [Support](#support).

### Neutral Grid

<a id="neutral-grid"></a>

*A futures grid without a strong long or short bias.* Level: beginner.

A neutral grid is built for two-way trade inside a range, rather than for a strong directional view. It still holds inventory risk if price trends out of the range. Sideways conditions are the usual study case, not a requirement the market will obey.

See also: [Long Grid](#long-grid), [Short Grid](#short-grid), [Sideways Market](#sideways-market).

### Order Size

<a id="order-size"></a>

*How much each grid order is allowed to trade.* Level: beginner.

Order size is the quantity on one grid level. All the levels together, plus any inventory, are the capital the bot can use. A size that looks small on one line can be large once every line is filled.

See also: [Capital Allocation](#capital-allocation), [Grid Count](#grid-count), [Notional](#notional).

### Range

<a id="range"></a>

*The upper and lower prices where a grid is meant to work.* Level: beginner.

The range is the top and bottom price you set as the bot's working area. Orders are planned inside that band. If price leaves the band, the original range thesis is no longer the market you designed for.

See also: [Upper Price](#upper-price), [Lower Price](#lower-price), [Range Thesis](#range-thesis).

### Range Thesis

<a id="range-thesis"></a>

*The reason you believe price will stay inside the planned band.* Level: intermediate.

The range thesis is the written reason the upper and lower prices were chosen, such as repeated reactions and a volatility check. It is a hypothesis. If price lives outside the band, the hypothesis needs a review rather than a silent widening.

See also: [Range](#range), [Invalidation](#invalidation), [Support](#support).

### Realised P&L

<a id="realised-pnl"></a>

*Profit or loss already locked by completed trades.* Level: beginner.

Realised profit and loss is the result of trades that have closed. The cash or coin balance has already changed. It is not the same figure as the open, marked position.

See also: [Unrealised P&L](#unrealised-pnl), [Grid Profit](#grid-profit), [Floating P&L](#floating-pnl).

### Short Grid

<a id="short-grid"></a>

*A grid configured with bearish directional exposure.* Level: intermediate.

A short grid is tilted so the exposure benefits if price falls, while still using grid levels. The directional tilt can lose if price rises. It is a configuration, not a view that price will fall.

See also: [Neutral Grid](#neutral-grid), [Long Grid](#long-grid), [Short](#short).

### Spot Grid

<a id="spot-grid"></a>

*A grid that trades the cash market, without derivatives leverage.* Level: beginner.

A spot grid buys and sells the asset itself inside a range. You can be left holding inventory if price falls through the range, but there is no futures liquidation price from the grid itself. Fees and inventory still decide whether the cycles were worth running.

See also: [Futures Grid](#futures-grid), [Inventory](#inventory), [Grid](#grid).

### Trailing Grid

<a id="trailing-grid"></a>

*A grid whose range can move under written rules.* Level: advanced.

A trailing grid shifts its upper or lower boundary when price moves a set distance, according to rules you can read in advance. The trail can keep the bot near price, and it can also drag the range into a trend you did not map. Read the rule before you turn it on.

See also: [Range](#range), [Trailing Stop](#trailing-stop), [Grid](#grid).

### Unrealised P&L

<a id="unrealised-pnl"></a>

*Mark-to-market result on open inventory or positions.* Level: beginner.

Unrealised profit and loss is the paper result of what you still hold, using a current reference price. It changes every time that price changes. It becomes realised only when the position is closed.

See also: [Realised P&L](#realised-pnl), [Floating P&L](#floating-pnl), [Inventory](#inventory).

### Upper Price

<a id="upper-price"></a>

*The top boundary of the grid.* Level: beginner.

The upper price is the highest level in the planned range. Above it, a long-biased or neutral grid is outside the area you mapped. It is a design choice, not a forecast of the high.

See also: [Range](#range), [Lower Price](#lower-price), [Resistance](#resistance).

## Market structure

<a id="market-structure"></a>

### Bearish Candle

<a id="bearish-candle"></a>

*A candle that closed below its open.* Level: beginner.

A bearish candle closed lower than it opened. It shows the result of that period. A bearish candle inside an uptrend does not, by itself, end the uptrend.

See also: [Bullish Candle](#bullish-candle), [Body](#body), [Downtrend](#downtrend).

### Body

<a id="body"></a>

*The rectangle between a candle's open and close.* Level: beginner.

The body is the range between the open and the close. A large body means the period finished far from where it started. Colour conventions differ, so read the legend on the chart you are using.

See also: [Candlestick](#candlestick), [Bullish Candle](#bullish-candle), [Bearish Candle](#bearish-candle).

### Break of Structure

<a id="break-of-structure"></a>

*A break that continues the prevailing swing direction.* Level: intermediate.

A break of structure, often shortened to BOS, is a move beyond the most recent swing in the direction of the trend you are mapping. In an uptrend that is a break of the latest swing high. Teachers differ on wick versus close, so write the rule you use.

See also: [Change of Character](#change-of-character), [Swing High](#swing-high), [Trend](#trend).

### Breaker Block

<a id="breaker-block"></a>

*A failed order block that price has broken and may later retest.* Level: advanced.

A breaker is an order-block area that did not hold, so the level has swapped roles in that method's map. Traders study a later return to it. The name is a labelling rule, not evidence of a hidden order.

See also: [Order Block](#order-block), [Mitigation](#mitigation), [False Breakout](#false-breakout).

### Breakout

<a id="breakout"></a>

*Price moving beyond a range or a marked level.* Level: beginner.

A breakout is a move through a level or a range that had been containing price. Some breakouts continue and some fail and return. A grid that assumed the range would hold needs a review when price keeps trading outside it.

See also: [False Breakout](#false-breakout), [Range](#range), [Resistance](#resistance).

### Bullish Candle

<a id="bullish-candle"></a>

*A candle that closed above its open.* Level: beginner.

A bullish candle closed higher than it opened. It shows who won that period, not who will win the next one. A bullish candle inside a downtrend is still inside that downtrend until the swing sequence changes.

See also: [Bearish Candle](#bearish-candle), [Body](#body), [Uptrend](#uptrend).

### Buy-side Liquidity

<a id="buy-side-liquidity"></a>

*Resting buy orders, often stops, sitting above highs.* Level: advanced.

Buy-side liquidity is the cluster of buy stops and breakout orders inferred above prior highs. A sweep through those highs trades that cluster. The phrase names a location on the chart, and it does not tell you to buy.

See also: [Sell-side Liquidity](#sell-side-liquidity), [Liquidity Sweep](#liquidity-sweep), [Equal Highs](#equal-highs).

### Candlestick

<a id="candlestick"></a>

*A chart bar showing open, high, low, and close.* Level: beginner.

A candlestick draws one period's open, high, low, and close. The body is the open-to-close distance, and the wicks are the extremes beyond the body. It is a picture of that period, not a signal by itself.

See also: [Open](#open), [High](#high), [Body](#body).

### Change of Character

<a id="change-of-character"></a>

*A break against the prevailing swing direction.* Level: intermediate.

A change of character, often shortened to CHoCH, is a break of the swing that had been defending the trend, such as a loss of a higher low in an uptrend. It is a clue that the sequence may be changing. It is not an instruction to enter a trade.

See also: [Break of Structure](#break-of-structure), [Higher Low](#higher-low), [Market Structure](#market-structure).

### Close

<a id="close"></a>

*The last traded price of a candle's period.* Level: beginner.

The close is the last price recorded for that candle. Many structure rules use a close beyond a level rather than a wick, because a wick can poke through and return. Say which rule you are using.

See also: [Open](#open), [Candlestick](#candlestick), [Break of Structure](#break-of-structure).

### Compression

<a id="compression"></a>

*A tightening of range and volatility before a move.* Level: intermediate.

Compression is a squeeze in the recent high-low range, so candles overlap and bands narrow. Traders study it because a later expansion sometimes follows. Compression does not say the direction of that expansion.

See also: [Consolidation](#consolidation), [Bollinger Bands](#bollinger-bands), [Expansion](#expansion).

### Consolidation

<a id="consolidation"></a>

*A pause where price trades in a tighter band.* Level: beginner.

Consolidation is a period of narrower two-way trade after a move, or inside a larger range. It can precede another push or a failed break. The pause itself does not say which.

See also: [Sideways Market](#sideways-market), [Compression](#compression), [Breakout](#breakout).

### Correction

<a id="correction"></a>

*A move against the prevailing impulse.* Level: intermediate.

A correction, or pullback, retraces part of an impulse without necessarily ending the larger sequence. In an uptrend a correction is the dip that tries to hold a higher low. Depth alone does not name it a reversal.

See also: [Impulse](#impulse), [Higher Low](#higher-low), [Trend](#trend).

### Dealing Range

<a id="dealing-range"></a>

*The swing high-to-low range used to map premium and discount.* Level: intermediate.

A dealing range is the price distance between a swing high and a swing low that you have chosen as the current map. Premium, discount, and equilibrium are measured inside it. Pick a different swing and the map moves.

See also: [Equilibrium](#equilibrium), [Swing High](#swing-high), [Swing Low](#swing-low).

### Discount

<a id="discount"></a>

*The lower half of a dealing range in a structure map.* Level: advanced.

Discount is the lower portion of a range you have marked, often below the midpoint. The word here means a location inside a swing range. It does not mean the asset is cheap in any fundamental sense.

See also: [Premium](#premium), [Equilibrium](#equilibrium), [Dealing Range](#dealing-range).

### Displacement

<a id="displacement"></a>

*A fast, one-sided move away from a prior area.* Level: advanced.

Displacement is a decisive push that leaves prior price behind, often with large bodies and little overlap. Structure methods use it to mark where energy showed up. A large candle is not displacement unless it actually leaves the prior area.

See also: [Impulse](#impulse), [Order Block](#order-block), [Fair Value Gap](#fair-value-gap).

### Downtrend

<a id="downtrend"></a>

*A sequence of lower highs and lower lows.* Level: beginner.

A downtrend, on the timeframe you are mapping, keeps printing lower swing highs and lower swing lows. Rallies can be sharp and still leave the sequence intact. The sequence fails when a swing that should have capped price gives way.

See also: [Lower High](#lower-high), [Lower Low](#lower-low), [Trend](#trend).

### Equal Highs

<a id="equal-highs"></a>

*Two or more highs at nearly the same price.* Level: intermediate.

Equal highs are adjacent peaks that line up at almost the same price. Structure methods treat the area just above them as a likely stop cluster. Near equality is a judgement, so mark the prices you mean.

See also: [Equal Lows](#equal-lows), [Buy-side Liquidity](#buy-side-liquidity), [Swing High](#swing-high).

### Equal Lows

<a id="equal-lows"></a>

*Two or more lows at nearly the same price.* Level: intermediate.

Equal lows are adjacent troughs that line up at almost the same price. Structure methods treat the area just below them as a likely stop cluster. Mark the prices rather than relying on a glance.

See also: [Equal Highs](#equal-highs), [Sell-side Liquidity](#sell-side-liquidity), [Swing Low](#swing-low).

### Equilibrium

<a id="equilibrium"></a>

*The midpoint of a marked dealing range.* Level: intermediate.

Equilibrium is the halfway price between the swing high and the swing low you chose. It splits premium from discount in that simple map. A different pair of swings gives a different midpoint.

See also: [Premium](#premium), [Discount](#discount), [Dealing Range](#dealing-range).

### Expansion

<a id="expansion"></a>

*A widening of range after a quieter period.* Level: intermediate.

Expansion is a phase where candles and swings get larger after compression or a quiet range. It is a change in volatility as much as a change in direction. Name the direction separately from the fact that the range widened.

See also: [Compression](#compression), [Volatility](#volatility), [Impulse](#impulse).

### Fair Value Gap

<a id="fair-value-gap"></a>

*A three-candle imbalance where wicks do not overlap.* Level: advanced.

A fair value gap, often shortened to FVG, is a three-candle pattern where the middle candle leaves a price gap between the wick of the candle before it and the wick of the candle after it. Traders study whether later trade returns into that gap. A gap is a description of prints, not an unfilled order you can audit.

See also: [Order Block](#order-block), [Displacement](#displacement), [Candlestick](#candlestick).

### False Breakout

<a id="false-breakout"></a>

*A move beyond a level that fails and returns inside.* Level: intermediate.

A false breakout pokes through support, resistance, or a range and then comes back, so the break did not hold. You can only call it false after the return. Planning for the possibility is different from knowing it in advance.

See also: [Breakout](#breakout), [Liquidity Sweep](#liquidity-sweep), [Retest](#retest).

### High

<a id="high"></a>

*The highest traded price of a candle's period.* Level: beginner.

The high is the top price printed during that candle. A wick up to the high shows price traded there and did not close there. One high is not a swing high until you compare it with neighbouring candles.

See also: [Low](#low), [Wick](#wick), [Swing High](#swing-high).

### Higher High

<a id="higher-high"></a>

*A swing high above the previous swing high.* Level: beginner.

A higher high prints when a new swing peak exceeds the prior swing peak. Together with higher lows, it is the usual map of an uptrend. One higher high without the higher lows is an incomplete picture.

See also: [Higher Low](#higher-low), [Uptrend](#uptrend), [Swing High](#swing-high).

### Higher Low

<a id="higher-low"></a>

*A swing low above the previous swing low.* Level: beginner.

A higher low prints when a new swing trough holds above the prior swing trough. In an uptrend it is the pullback that did not break the sequence. A close through that low is often the change-of-character study point.

See also: [Higher High](#higher-high), [Change of Character](#change-of-character), [Swing Low](#swing-low).

### Impulse

<a id="impulse"></a>

*A strong push in the direction of the current sequence.* Level: intermediate.

An impulse is a relatively direct move that carries price to a new swing in the direction of the trend or the break. It is judged against the corrections around it. The word does not require a fixed indicator reading.

See also: [Correction](#correction), [Displacement](#displacement), [Break of Structure](#break-of-structure).

### Inducement

<a id="inducement"></a>

*A minor swing that may attract stops before a larger level is tested.* Level: advanced.

Inducement, in structure teaching, is a small obvious swing sitting in front of a larger pool of resting orders. The hypothesis is that price may trade that small swing before dealing with the larger one. It is a map of possible stops, not a schedule.

See also: [Liquidity Sweep](#liquidity-sweep), [Liquidity Pool](#liquidity-pool), [Swing Point](#swing-point).

### Liquidity Pool

<a id="liquidity-pool"></a>

*A cluster of resting orders, often beyond equal highs or lows.* Level: advanced.

In structure teaching, a liquidity pool is a place where stops and resting orders are likely to sit, such as above equal highs or below equal lows. The pool is inferred from the chart, not read from a private book. The same phrase in DeFi means a token pool, which is a different object.

See also: [Equal Highs](#equal-highs), [Liquidity Sweep](#liquidity-sweep), [Liquidity](#liquidity).

### Liquidity Sweep

<a id="liquidity-sweep"></a>

*A push beyond an obvious high or low that then reverses.* Level: advanced.

A liquidity sweep is a move through a prior high or low, where stops are often clustered, followed by a return back inside. The idea is that resting orders beyond the obvious level were traded. A sweep is a description after the fact, not a prediction that every poke will reverse.

See also: [Buy-side Liquidity](#buy-side-liquidity), [Sell-side Liquidity](#sell-side-liquidity), [Equal Highs](#equal-highs).

### Low

<a id="low"></a>

*The lowest traded price of a candle's period.* Level: beginner.

The low is the bottom price printed during that candle. A wick down to the low shows price traded there and did not close there. One low is not a swing low until you compare it with neighbouring candles.

See also: [High](#high), [Wick](#wick), [Swing Low](#swing-low).

### Lower High

<a id="lower-high"></a>

*A swing high below the previous swing high.* Level: beginner.

A lower high prints when a rally fails to exceed the prior swing peak. Together with lower lows, it is the usual map of a downtrend. It is a description of swings already printed.

See also: [Lower Low](#lower-low), [Downtrend](#downtrend), [Swing High](#swing-high).

### Lower Low

<a id="lower-low"></a>

*A swing low below the previous swing low.* Level: beginner.

A lower low prints when a new swing trough undercuts the prior swing trough. In a downtrend it continues the sequence. A later rally through the prior lower high is the usual place to study a change of character.

See also: [Lower High](#lower-high), [Break of Structure](#break-of-structure), [Swing Low](#swing-low).

### Market Regime

<a id="market-regime"></a>

*The broad behaviour of the market you are in, such as trend or range.* Level: intermediate.

A market regime is the working description of conditions, for example trending, ranging, or a high-volatility break. Tools that fit one regime often fit another badly. Naming the regime is a hypothesis you review when behaviour changes.

See also: [Trend](#trend), [Sideways Market](#sideways-market), [Volatility](#volatility).

### Market Structure

<a id="market-structure"></a>

*The map of swing highs and swing lows on a timeframe.* Level: beginner.

Market structure is the sequence of swing highs and swing lows you can point to on a chart. Trends, ranges, breaks of structure, and changes of character are all statements about that sequence. If you cannot mark the swings, you do not yet have a map.

See also: [Swing High](#swing-high), [Swing Low](#swing-low), [Trend](#trend).

### Market Structure Shift

<a id="market-structure-shift"></a>

*Another teaching label for a change of character on a chosen timeframe.* Level: advanced.

A market structure shift is a break against the prior swing sequence, the same family of idea as a change of character. Courses sometimes reserve the phrase for a shift on a lower timeframe inside a higher-timeframe idea. Ask which timeframe the speaker means.

See also: [Change of Character](#change-of-character), [Multi-timeframe Analysis](#multi-timeframe), [Break of Structure](#break-of-structure).

### Mean Reversion

<a id="mean-reversion"></a>

*A tendency for price to move back toward a central value.* Level: intermediate.

Mean reversion is the idea that price sometimes oscillates back toward an average or toward the middle of a range. It is a description of some markets some of the time. It is not a rule that every extension must snap back.

See also: [Sideways Market](#sideways-market), [Moving Average](#moving-average), [Neutral Grid](#neutral-grid).

### Mitigation

<a id="mitigation"></a>

*Price returning to an order block or a gap that was marked earlier.* Level: advanced.

Mitigation, in this teaching, is a later return into a previously marked order block or imbalance. The hypothesis is that the earlier area may be revisited. A return is something you can see, and what happens after it is not settled by the word.

See also: [Order Block](#order-block), [Fair Value Gap](#fair-value-gap), [Retest](#retest).

### Multi-timeframe Analysis

<a id="multi-timeframe"></a>

*Reading the same market on a higher and a lower timeframe together.* Level: intermediate.

Multi-timeframe analysis looks at a higher timeframe for the larger swing map and a lower timeframe for the detail of the current push. A setup that fights the higher-timeframe sequence needs a reason written down. Timeframes do not vote, and you still choose a plan.

See also: [Timeframe](#timeframe), [Market Structure](#market-structure), [Trend](#trend).

### Open

<a id="open"></a>

*The first traded price of a candle's period.* Level: beginner.

The open is the first price recorded for that candle. Compared with the close, it shows whether the period finished above or below where it started. The open depends on the session and the timeframe you chose.

See also: [Close](#close), [Candlestick](#candlestick), [Timeframe](#timeframe).

### Order Block

<a id="order-block"></a>

*A candle cluster at the origin of a strong move, studied as a reaction area.* Level: advanced.

An order block is a candle, or a small group of candles, at the start of a decisive move, which some structure methods mark as a place to study if price returns. The label is a hypothesis about where activity clustered. It does not mean you can see a resting order from a named institution.

See also: [Mitigation](#mitigation), [Displacement](#displacement), [Fair Value Gap](#fair-value-gap).

### Premium

<a id="premium"></a>

*The upper half of a dealing range in a structure map.* Level: advanced.

Premium is the upper portion of a range you have marked, often above the midpoint between a swing high and a swing low. Some methods prefer to study shorts in premium and longs in discount. That preference is a framework, not a law of the market.

See also: [Discount](#discount), [Equilibrium](#equilibrium), [Dealing Range](#dealing-range).

### Protected Swing

<a id="protected-swing"></a>

*The swing low or high that must hold for the current sequence to stay valid.* Level: advanced.

A protected swing is the higher low, or the lower high, that your written trend rule treats as the line in the sand. If price closes through it, the sequence you were mapping is no longer intact. The protection is a rule you chose, not a property of the candle.

See also: [Higher Low](#higher-low), [Invalidation](#invalidation), [Change of Character](#change-of-character).

### Range High

<a id="range-high"></a>

*The upper edge of a sideways band, as distinct from a grid's upper setting.* Level: beginner.

The range high is the top of a sideways market you have marked from the chart. A grid's upper price may be set near it, or inside it, or somewhere else. The chart level and the bot setting are two different decisions.

See also: [Range Low](#range-low), [Sideways Market](#sideways-market), [Upper Price](#upper-price).

### Range Low

<a id="range-low"></a>

*The lower edge of a sideways band, as distinct from a grid's lower setting.* Level: beginner.

The range low is the bottom of a sideways market you have marked from the chart. It can inform a grid's lower price. It does not set that price for you, and it can break.

See also: [Range High](#range-high), [Sideways Market](#sideways-market), [Lower Price](#lower-price).

### Rejection

<a id="rejection"></a>

*A wick or a quick return showing price did not stay beyond a level.* Level: beginner.

Rejection is the chart pattern of price trading through a level or an extreme and closing back away from it, often with a long wick. It shows that extreme did not hold for that candle. It does not settle the next candle.

See also: [Wick](#wick), [False Breakout](#false-breakout), [Pin Bar](#pin-bar).

### Retest

<a id="retest"></a>

*A later return to a level that price has broken or rejected.* Level: intermediate.

A retest is price coming back to a level after leaving it, such as a return to broken resistance. Some retests hold and some slice through. The return is the observation, and the outcome is not included in the definition.

See also: [Breakout](#breakout), [Support](#support), [Mitigation](#mitigation).

### Sell-side Liquidity

<a id="sell-side-liquidity"></a>

*Resting sell orders, often stops, sitting below lows.* Level: advanced.

Sell-side liquidity is the cluster of sell stops inferred below prior lows. A sweep through those lows trades that cluster. The phrase names a location, and it does not tell you to sell.

See also: [Buy-side Liquidity](#buy-side-liquidity), [Liquidity Sweep](#liquidity-sweep), [Equal Lows](#equal-lows).

### Sideways Market

<a id="sideways-market"></a>

*Price oscillating inside a band without a sustained trend.* Level: beginner.

A sideways market, or trading range, is two-way trade between a ceiling and a floor, without a sustained run of higher highs or lower lows. Grid lessons use this as the usual study case for a neutral grid. A range can end without warning you in advance.

See also: [Range](#range), [Mean Reversion](#mean-reversion), [Neutral Grid](#neutral-grid).

### Swing High

<a id="swing-high"></a>

*A high with lower highs on both sides.* Level: beginner.

A swing high is a local peak: a high that stands above the highs immediately to its left and right, using a rule you keep constant. Swing highs are the posts you use to map structure. Change the left-right rule and the map changes.

See also: [Swing Low](#swing-low), [Higher High](#higher-high), [Market Structure](#market-structure).

### Swing Low

<a id="swing-low"></a>

*A low with higher lows on both sides.* Level: beginner.

A swing low is a local trough: a low that stands below the lows immediately to its left and right. Swing lows are the other posts in a structure map. A single wick is not automatically a swing.

See also: [Swing High](#swing-high), [Higher Low](#higher-low), [Market Structure](#market-structure).

### Swing Point

<a id="swing-point"></a>

*Either a swing high or a swing low.* Level: beginner.

A swing point is a confirmed local extreme, high or low, under the left-and-right rule you use. Swing points are the only posts a structure map should need. If a method needs an unmarked point, write the extra rule down.

See also: [Swing High](#swing-high), [Swing Low](#swing-low), [Market Structure](#market-structure).

### Timeframe

<a id="timeframe"></a>

*The period each candle represents.* Level: beginner.

The timeframe is the length of one candle, such as one hour or one day. Structure on a small timeframe is nested inside structure on a larger one. Name the timeframe whenever you name a trend.

See also: [Multi-timeframe Analysis](#multi-timeframe), [Candlestick](#candlestick), [Trend](#trend).

### Trend

<a id="trend"></a>

*A persistent direction in swing structure.* Level: beginner.

A trend is a run of swings that keeps making progress in one direction, higher highs and higher lows, or lower highs and lower lows. It is observed on a chosen timeframe. A trend on one timeframe can be a pullback on a higher one.

See also: [Uptrend](#uptrend), [Downtrend](#downtrend), [Timeframe](#timeframe).

### Uptrend

<a id="uptrend"></a>

*A sequence of higher highs and higher lows.* Level: beginner.

An uptrend, on the timeframe you are mapping, keeps printing higher swing highs and higher swing lows. Pullbacks can be deep and still leave the sequence intact. The sequence fails when a swing that should have held gives way.

See also: [Higher High](#higher-high), [Higher Low](#higher-low), [Trend](#trend).

### Volatility

<a id="volatility"></a>

*How large and how fast price moves.* Level: beginner.

Volatility is the size and speed of price movement, not the direction. High volatility means wider swings. A grid studies it because spacing that is tight relative to the movement, or tight relative to fees, changes the economics of each cycle.

See also: [ATR](#atr), [Variance](#variance), [Grid Spacing](#grid-spacing).

### Wick

<a id="wick"></a>

*The thin line from the body to the high or the low.* Level: beginner.

A wick, or shadow, marks prices that traded during the candle beyond the open-to-close body. A long wick shows rejection of those prices only in the sense that the close did not stay there. Context from the surrounding swings still matters.

See also: [Body](#body), [High](#high), [Rejection](#rejection).

## Technical analysis

<a id="technical-analysis"></a>

### Anchored VWAP

<a id="anchored-vwap"></a>

*VWAP started from a candle you choose, rather than from the session open.* Level: advanced.

An anchored VWAP begins the volume-weighted sum at a swing, a break, or another candle you name, and runs forward from there. The anchor is a judgement. Two anchors produce two lines, so write down why you started where you did.

See also: [VWAP](#vwap), [Swing Point](#swing-point), [Volume](#volume).

### ATR

<a id="atr"></a>

*Average true range, a measure of recent movement size.* Level: intermediate.

Average true range smooths the true range, which is the widest of the bar's high minus low, and the gaps from the prior close to the high or the low. It describes how far price has been travelling. It does not say which way the next bar will go.

See also: [Volatility](#volatility), [True Range](#true-range), [Stop Distance](#stop-distance).

### Bollinger Bands

<a id="bollinger-bands"></a>

*A moving average with bands set a number of standard deviations away.* Level: intermediate.

Bollinger Bands draw a moving average and place an upper and a lower band a chosen number of standard deviations from it, commonly two. The bands widen when recent closes are more dispersed and narrow when they are quiet. A tag of the band is a location, not an automatic reversal.

See also: [Standard Deviation](#standard-deviation), [Simple Moving Average](#sma), [Compression](#compression).

### Channel

<a id="channel"></a>

*Two parallel lines containing a series of swings.* Level: intermediate.

A channel is a pair of parallel lines, one along highs and one along lows, so price has been rising or falling inside a lane. Touches alternate by construction if you drew it tightly. A break of the lane is the event, and the lane is not a container with a lock.

See also: [Trendline](#trendline), [Flag](#flag), [Trend](#trend).

### Chart Pattern

<a id="chart-pattern"></a>

*A named shape in price, such as a triangle or a double top.* Level: beginner.

A chart pattern is a geometric description of swings, such as a double top, a triangle, or a flag. The name helps you point at the shape. Measured outcomes in textbooks are historical descriptions, not a schedule for the current market.

See also: [Double Top](#double-top), [Triangle](#triangle), [Flag](#flag).

### Confluence

<a id="confluence"></a>

*Several independent observations lining up at the same area.* Level: intermediate.

Confluence is the overlap of separate pieces of evidence, such as a higher-timeframe swing, a level, and a volatility measure, in one price area. More overlapping labels are not more proof if they all come from the same candles. Independent means a different question, not a second colour on the same average.

See also: [Support](#support), [Multi-timeframe Analysis](#multi-timeframe), [Indicator](#indicator).

### Death Cross

<a id="death-cross"></a>

*A shorter average crossing below a longer average.* Level: beginner.

A death cross is a shorter moving average falling through a longer one. The name is dramatic and the content is a lagging cross. It describes the window behind you, and it does not schedule the next decline.

See also: [Golden Cross](#golden-cross), [Simple Moving Average](#sma), [Downtrend](#downtrend).

### Divergence

<a id="divergence"></a>

*Price and an oscillator making opposite swings.* Level: intermediate.

Regular divergence is a new price extreme that the oscillator does not match, such as a higher high in price with a lower high on RSI. It is a disagreement inside the lookback. It is not a timer for a reversal, and it can persist while the trend continues.

See also: [Hidden Divergence](#hidden-divergence), [RSI](#rsi), [MACD](#macd).

### Doji

<a id="doji"></a>

*A candle whose open and close are almost the same.* Level: beginner.

A doji has a very small body, so the period finished near where it started, often with wicks on one or both sides. It shows indecision in that period. A doji in the middle of a quiet range says less than a doji at a level you already marked.

See also: [Candlestick](#candlestick), [Body](#body), [Indecision](#indecision).

### Donchian Channel

<a id="donchian-channel"></a>

*The highest high and lowest low of the last N candles.* Level: intermediate.

A Donchian channel plots the highest high and the lowest low over a lookback, with the midpoint sometimes drawn between them. A push to the upper line is a push to the recent extreme, by definition. The channel restates the range, and it does not add new information beyond that.

See also: [High](#high), [Low](#low), [Breakout](#breakout).

### Double Bottom

<a id="double-bottom"></a>

*Two lows at a similar price with a peak between them.* Level: beginner.

A double bottom is two failed pushes to a similar low, separated by a bounce. The textbook pattern is complete only if price later breaks the peak between them. Two lows alone are equal lows.

See also: [Double Top](#double-top), [Equal Lows](#equal-lows), [Neckline](#neckline).

### Double Top

<a id="double-top"></a>

*Two highs at a similar price with a trough between them.* Level: beginner.

A double top is two failed pushes to a similar high, separated by a pullback. The pattern is complete, in the textbook sense, only if price later breaks the trough between them. Until that break, it is just two highs.

See also: [Double Bottom](#double-bottom), [Equal Highs](#equal-highs), [Neckline](#neckline).

### Engulfing Candle

<a id="engulfing"></a>

*A candle whose body fully covers the previous body.* Level: beginner.

A bullish engulfing candle has a body that covers the prior bearish body, and a bearish engulfing candle does the reverse. It shows a strong result for that one period relative to the one before. The pattern ignores the wicks unless your written rule includes them.

See also: [Body](#body), [Bullish Candle](#bullish-candle), [Bearish Candle](#bearish-candle).

### Exponential Moving Average

<a id="ema"></a>

*An average that weights recent closes more than older ones.* Level: intermediate.

An exponential moving average gives more weight to the newest close and keeps a fading memory of older closes. It responds faster than a simple average of the same length, and it still lags. The length is a setting, not a correct answer.

See also: [Simple Moving Average](#sma), [MACD](#macd), [Moving Average](#moving-average).

### Fibonacci Retracement

<a id="fibonacci-retracement"></a>

*Horizontal levels at fixed ratios of a prior swing.* Level: intermediate.

A Fibonacci retracement divides a swing you choose into ratios such as one half and the well-known nearby ratios derived from the Fibonacci sequence. The levels are arithmetic on that swing. They become useful only as places to compare with structure you can already see.

See also: [Swing Point](#swing-point), [Correction](#correction), [Confluence](#confluence).

### Flag

<a id="flag"></a>

*A small channel against the prior impulse.* Level: intermediate.

A flag is a short, tight consolidation that slopes against a sharp prior move. The textbook treats a break in the direction of that prior move as the pattern's completion. Many tight pauses are not flags, because the prior impulse was not there.

See also: [Impulse](#impulse), [Consolidation](#consolidation), [Chart Pattern](#chart-pattern).

### Golden Cross

<a id="golden-cross"></a>

*A shorter average crossing above a longer average.* Level: beginner.

A golden cross is a shorter moving average rising through a longer one, often taught with the fifty and the two-hundred on a daily chart. It describes a change in the averages. It is late by construction, because both averages are lagging.

See also: [Death Cross](#death-cross), [Simple Moving Average](#sma), [Lag](#lag).

### Hammer

<a id="hammer"></a>

*A small body with a long lower wick, after a decline.* Level: beginner.

A hammer has a small body near the top of the candle and a long lower wick, appearing after a downswing. It shows that the low was rejected inside that period. The same shape after an upswing is usually called a hanging man, and neither shape trades itself.

See also: [Pin Bar](#pin-bar), [Rejection](#rejection), [Wick](#wick).

### Head and Shoulders

<a id="head-and-shoulders"></a>

*A peak between two lower peaks, with a neckline through the troughs.* Level: intermediate.

A head and shoulders is a middle swing high above two lower swing highs, with a neckline along the intervening lows. The inverse form is a middle trough below two higher troughs. The shape is a description, and the neckline break is the event the textbook waits for.

See also: [Neckline](#neckline), [Double Top](#double-top), [Swing High](#swing-high).

### Hidden Divergence

<a id="hidden-divergence"></a>

*An oscillator extreme that disagrees with a pullback, studied inside a trend.* Level: advanced.

Hidden divergence is the case where price makes a higher low in an uptrend while the oscillator makes a lower low, or the mirror in a downtrend. Teachers study it as a trend-continuation clue. It is still only a disagreement between two plots.

See also: [Divergence](#divergence), [Correction](#correction), [RSI](#rsi).

### Indecision

<a id="indecision"></a>

*A candle or a cluster that does not close decisively either way.* Level: beginner.

Indecision is a small-body candle, such as a doji, or a cluster of overlapping candles, showing no clear winner for that window. It is a description of balance. Balance can break either way, so the word is not a setup.

See also: [Doji](#doji), [Consolidation](#consolidation), [Body](#body).

### Indicator

<a id="indicator"></a>

*A calculation on price, volume, or both, drawn to summarise the window.* Level: beginner.

An indicator is a formula applied to past prints, such as an average, RSI, or ATR. It cannot see more than the inputs you gave it. Use it to measure something you can name, and check the failure mode of that measure.

See also: [Oscillator](#oscillator), [Moving Average](#moving-average), [Confluence](#confluence).

### Inside Bar

<a id="inside-bar"></a>

*A candle whose high and low sit inside the previous candle.* Level: intermediate.

An inside bar has a lower high and a higher low than the candle before it, so its entire range is nested. It is a small compression on one timeframe. A break of the mother candle is the event people wait for, and it can fail.

See also: [Compression](#compression), [High](#high), [Low](#low).

### Keltner Channel

<a id="keltner-channel"></a>

*An average with bands set from ATR rather than standard deviation.* Level: advanced.

A Keltner channel places bands a multiple of ATR away from an exponential average. Compared with Bollinger Bands, the width follows true range rather than the standard deviation of closes. A close outside the band is a large move relative to that ATR setting.

See also: [ATR](#atr), [Bollinger Bands](#bollinger-bands), [Exponential Moving Average](#ema).

### Lag

<a id="lag"></a>

*The delay built into a calculation that uses past candles.* Level: intermediate.

Lag is the fact that an average or a similar smooth cannot turn until the candles inside it have turned. Faster settings reduce lag and increase whipsaw. You do not remove the trade-off by believing harder in the line.

See also: [Moving Average](#moving-average), [Exponential Moving Average](#ema), [Indicator](#indicator).

### MACD

<a id="macd"></a>

*The difference between a shorter and a longer exponential average.* Level: intermediate.

MACD subtracts a longer exponential moving average from a shorter one. Common study settings are twelve and twenty-six periods, with a nine-period average of the result as the signal line. The histogram is the gap between MACD and that signal, and crosses describe the averages, and they do not schedule the next price.

See also: [MACD Signal Line](#macd-signal), [MACD Histogram](#macd-histogram), [Exponential Moving Average](#ema).

### MACD Histogram

<a id="macd-histogram"></a>

*The gap between the MACD line and the signal line.* Level: intermediate.

The histogram plots MACD minus the signal line. Bars growing in one direction mean the gap is widening. Bars shrinking mean the gap is narrowing, which can happen while price is still moving the same way.

See also: [MACD](#macd), [MACD Signal Line](#macd-signal), [Momentum](#momentum).

### MACD Signal Line

<a id="macd-signal"></a>

*An exponential average of the MACD line.* Level: intermediate.

The signal line is a smoothed version of the MACD line, commonly nine periods. A cross of MACD through the signal says the shorter momentum of the averages has flipped relative to its own smooth. It is a description of two calculated lines.

See also: [MACD](#macd), [MACD Histogram](#macd-histogram), [Exponential Moving Average](#ema).

### Momentum

<a id="momentum"></a>

*The speed of a price change over a window.* Level: beginner.

Momentum is how far price has moved over a set number of candles, or an oscillator built to show that speed. Rising momentum means the recent push is larger than the one before it on that measure. Momentum can fade while price is still making new highs.

See also: [RSI](#rsi), [MACD](#macd), [Impulse](#impulse).

### Moving Average

<a id="moving-average"></a>

*A smoothed average of recent prices.* Level: beginner.

A moving average is the average of the last N closes, updated every candle. It lags price because it is built from candles already printed. Traders use it as a smoothing tool and as one input among others, not as a standalone command.

See also: [Simple Moving Average](#sma), [Exponential Moving Average](#ema), [Trend](#trend).

### Neckline

<a id="neckline"></a>

*The line drawn across the troughs or peaks of a reversal pattern.* Level: intermediate.

The neckline joins the reaction points of a head-and-shoulders or a double top or bottom. A close through it is the event those patterns treat as confirmation. Where you place the line changes the event, so mark the swings you used.

See also: [Head and Shoulders](#head-and-shoulders), [Double Top](#double-top), [Breakout](#breakout).

### On-balance Volume

<a id="obv"></a>

*A running total that adds volume on up closes and subtracts it on down closes.* Level: intermediate.

On-balance volume adds the period's volume when the close is up and subtracts it when the close is down. The level of the line matters less than whether it confirms or diverges from price. It inherits every flaw of the volume feed you use.

See also: [Volume](#volume), [Divergence](#divergence), [Close](#close).

### Oscillator

<a id="oscillator"></a>

*An indicator that swings inside a bounded or centred scale.* Level: beginner.

An oscillator, such as RSI or a stochastic, moves between bounds or around a centre line so you can compare readings across time. Boundedness is a feature of the formula. It is not a fence around future price.

See also: [RSI](#rsi), [Indicator](#indicator), [Overbought](#overbought).

### Overbought

<a id="overbought"></a>

*An oscillator reading in its upper zone.* Level: beginner.

Overbought means an oscillator such as RSI is in the high band of its own scale, often taught near seventy and above. The word means the lookback has been dominated by up closes. It does not mean the asset is expensive or that it must fall.

See also: [Oversold](#oversold), [RSI](#rsi), [Divergence](#divergence).

### Oversold

<a id="oversold"></a>

*An oscillator reading in its lower zone.* Level: beginner.

Oversold means an oscillator is in the low band of its own scale, often taught near thirty and below. The word means the lookback has been dominated by down closes. A market can stay there while the downtrend continues.

See also: [Overbought](#overbought), [RSI](#rsi), [Downtrend](#downtrend).

### Pin Bar

<a id="pin-bar"></a>

*A candle with a long wick and a small body at the other end.* Level: beginner.

A pin bar is a rejection candle: a long wick in one direction and a body closed near the opposite end. Traders study it at levels, not in the middle of nowhere. The wick shows where price traded and did not stay.

See also: [Hammer](#hammer), [Rejection](#rejection), [Wick](#wick).

### Pivot Point

<a id="pivot-point"></a>

*A reference price derived from the prior period's high, low, and close.* Level: intermediate.

A classic floor-trader pivot is a formula on the previous period's high, low, and close, with extra levels spaced from that pivot. It is a reference grid for the new period. It is not support merely because the formula printed a number.

See also: [High](#high), [Low](#low), [Support](#support).

### Point of Control

<a id="point-of-control"></a>

*The price with the most traded volume on a profile.* Level: advanced.

The point of control is the single price bin with the highest volume on the profile you built. It is a description of where trade concentrated in that window. A different window moves it.

See also: [Volume Profile](#volume-profile), [Value Area](#value-area), [VWAP](#vwap).

### Price Action

<a id="price-action"></a>

*Reading structure from candles and swings without requiring an indicator.* Level: beginner.

Price action is the practice of describing highs, lows, closes, and swings directly. Indicators can sit beside it, but they are not required to name a trend or a range. The standard is still a written rule, so two readers can agree on the same swing.

See also: [Candlestick](#candlestick), [Market Structure](#market-structure), [Swing Point](#swing-point).

### Relative Volume

<a id="relative-volume"></a>

*This candle's volume compared with its usual volume at that time.* Level: intermediate.

Relative volume divides current volume by a baseline, such as the average volume of the same hour over recent days. A high reading means this period is busier than that baseline. The baseline has to match the session or the comparison is noise.

See also: [Volume](#volume), [Timeframe](#timeframe), [VWAP](#vwap).

### Resistance

<a id="resistance"></a>

*An area where selling has repeatedly appeared.* Level: beginner.

Resistance is a price area where rallies have stalled often enough that traders mark it. It is a description of past reactions, not a ceiling that must hold. A break through it is information, not a promise of follow-through.

See also: [Support](#support), [Upper Price](#upper-price), [Breakout](#breakout).

### Round Number

<a id="round-number"></a>

*A psychologically obvious price such as a whole figure.* Level: beginner.

A round number is a clean price people can remember, where orders often cluster because humans and some bots use them. Clustering is a tendency, not a rule that the figure will hold. Treat it as a place to look, then check the actual reactions.

See also: [Support](#support), [Liquidity](#liquidity), [Limit Order](#limit-order).

### RSI

<a id="rsi"></a>

*A momentum oscillator that compares average up closes with average down closes.* Level: intermediate.

The relative strength index compares a smoothed average of up-close size with a smoothed average of down-close size over a lookback, using Wilder's smoothing. The scale runs from zero to one hundred. A high reading means up closes have dominated that window, which is not the same as saying price must reverse.

See also: [Overbought](#overbought), [Oversold](#oversold), [Divergence](#divergence).

### Simple Moving Average

<a id="sma"></a>

*An average that weights each of the last N closes equally.* Level: beginner.

A simple moving average adds the last N closes and divides by N. Every close in the window counts the same, and the oldest close drops off when a new one arrives. A short window hugs price more closely and whipsaws more often.

See also: [Exponential Moving Average](#ema), [Moving Average](#moving-average), [Lag](#lag).

### Standard Deviation

<a id="standard-deviation"></a>

*A measure of how far values sit from their average.* Level: intermediate.

Standard deviation summarises the scatter of a set of numbers around their mean. In bands and in risk, a larger standard deviation means the recent values have been more spread out. It is a statistic of the window you chose.

See also: [Variance](#variance), [Bollinger Bands](#bollinger-bands), [Volatility](#volatility).

### Stochastic

<a id="stochastic"></a>

*An oscillator that locates the close inside the recent high-low range.* Level: intermediate.

A stochastic compares the close with the high-low range of the last N candles, then smooths that result. A close near the top of the recent range reads high. Like RSI, a high reading is a description of the window, not an order to fade it.

See also: [Oscillator](#oscillator), [Overbought](#overbought), [RSI](#rsi).

### Support

<a id="support"></a>

*An area where buying has repeatedly appeared.* Level: beginner.

Support is a price area where declines have stalled often enough that traders mark it. It is a description of past reactions, not a floor that must hold. A break through it is information, not a broken law.

See also: [Resistance](#resistance), [Lower Price](#lower-price), [Retest](#retest).

### Support and Resistance

<a id="support-and-resistance"></a>

*The pair of ideas: areas where declines or rallies have stalled before.* Level: beginner.

Support and resistance are past reaction areas, floors and ceilings only in the sense that price has stalled there before. They can be levels, zones, or round numbers people watch. They fail often enough that a plan needs an invalidation, not only a line.

See also: [Support](#support), [Resistance](#resistance), [Retest](#retest).

### Trendline

<a id="trendline"></a>

*A straight line drawn across swing points in one direction.* Level: beginner.

A trendline connects two or more swing lows in an uptrend, or swing highs in a downtrend. A third touch makes the line more interesting and does not make it a wall. Redraw it when the swings you used are no longer the relevant ones.

See also: [Trend](#trend), [Swing Low](#swing-low), [Support](#support).

### Triangle

<a id="triangle"></a>

*Converging trendlines that compress recent swings.* Level: intermediate.

A triangle is two converging lines around recent highs and lows, so the range narrows. Ascending, descending, and symmetrical versions differ by which line is flat. A triangle does not contain the direction of the eventual break.

See also: [Compression](#compression), [Trendline](#trendline), [Chart Pattern](#chart-pattern).

### True Range

<a id="true-range"></a>

*The widest of the bar's range and the gaps from the prior close.* Level: intermediate.

True range is the greatest of high minus low, the absolute gap from high to the prior close, and the absolute gap from low to the prior close. It includes a gap that the high-low range would miss. ATR is a smooth of this number.

See also: [ATR](#atr), [High](#high), [Close](#close).

### Value Area

<a id="value-area"></a>

*The price band that contains a set share of profile volume.* Level: advanced.

The value area is the band around the point of control that contains a chosen share of the profile's volume, often taught as about seventy percent. It describes where most of the business occurred. It is not a forecast of where the next business must occur.

See also: [Volume Profile](#volume-profile), [Point of Control](#point-of-control), [Sideways Market](#sideways-market).

### Volume

<a id="volume"></a>

*How much traded during a period.* Level: beginner.

Volume is the amount traded in a candle, in coins or in contracts, depending on the feed. A price move on heavy volume had more participation than the same move on light volume. Crypto feeds can disagree because venues and the way they count differ.

See also: [On-balance Volume](#obv), [Relative Volume](#relative-volume), [VWAP](#vwap).

### Volume Profile

<a id="volume-profile"></a>

*A histogram of how much traded at each price.* Level: advanced.

Volume profile sums volume across prices rather than across time, over a window or a session you choose. Peaks are prices where more business was done. The picture is only as good as the feed and the window.

See also: [Point of Control](#point-of-control), [Value Area](#value-area), [Volume](#volume).

### VWAP

<a id="vwap"></a>

*The volume-weighted average price over a chosen session.* Level: intermediate.

VWAP adds up typical price times volume and divides by total volume for the session you set. It is the average price weighted by how much traded. A new session usually resets the sum, so the anchor of the session is part of the definition.

See also: [Volume](#volume), [Anchored VWAP](#anchored-vwap), [Moving Average](#moving-average).

### Whipsaw

<a id="whipsaw"></a>

*A signal that flips and then flips back, catching both sides.* Level: intermediate.

A whipsaw is a cross or a break that reverses quickly enough to lose on both the entry and the exit under the same rule. Faster indicator settings whipsaw more in ranges. The cure in a study is a regime filter or a slower rule, not a larger size.

See also: [Lag](#lag), [Sideways Market](#sideways-market), [False Breakout](#false-breakout).

## Risk

<a id="risk"></a>

### Account Risk

<a id="account-risk"></a>

*The fraction of equity you are willing to lose on one idea.* Level: beginner.

Account risk is the money, or the percentage of equity, you assign to one trade's stop being hit. Atlas lessons treat it as a ceiling you choose in advance. The right ceiling for a reader is not something a glossary can set.

See also: [Risk per Trade](#risk-per-trade), [Position Sizing](#position-sizing), [Equity Curve](#equity-curve).

### Compounding

<a id="compounding"></a>

*Leaving results in so later size is calculated on a larger base.* Level: intermediate.

Compounding means reinvesting a result so the next calculation uses a larger capital base. Later gains and later losses are both applied to that larger base. It is an arithmetic choice, not a promise that the base will grow.

See also: [Capital Allocation](#capital-allocation), [Equity Curve](#equity-curve), [Volatility Drag](#volatility-drag).

### Counterparty Risk

<a id="counterparty-risk"></a>

*The risk that the other side, or the venue holding the trade, fails.* Level: intermediate.

Counterparty risk is the chance that an exchange, a custodian, an issuer, or a protocol does not perform. On a centralised venue your position is a claim on that venue. On-chain, the counterparty may be a contract, and the failure mode is a bug or a governance action rather than a phone call.

See also: [Custody](#custody), [Centralised Exchange](#centralised-exchange), [Smart-contract Risk](#smart-contract-risk).

### Drawdown

<a id="drawdown"></a>

*A decline from a prior equity peak.* Level: beginner.

Drawdown is how far account equity has fallen from a previous high, usually stated as a fraction of that peak. It measures pain already experienced on the equity curve. It is not the same number as one trade's loss.

See also: [Maximum Drawdown](#maximum-drawdown), [Drawdown Recovery](#drawdown-recovery), [Equity Curve](#equity-curve).

### Drawdown Recovery

<a id="drawdown-recovery"></a>

*The rise required to regain a prior equity peak.* Level: advanced.

After equity falls by a fraction d of the peak, the rise needed on what remains is one divided by the quantity one minus d, minus one. Deeper drawdowns demand a much larger recovery than the decline itself. The formula is arithmetic, and it is not a forecast that the recovery will arrive.

See also: [Drawdown](#drawdown), [Maximum Drawdown](#maximum-drawdown), [Compounding](#compounding).

### Equity Curve

<a id="equity-curve"></a>

*A plot of account equity after each result.* Level: beginner.

The equity curve is the running total of the account, trade by trade or day by day. Peaks, drawdowns, and flat stretches are read from it. A smooth curve in a small sample is not evidence the next stretch will be smooth.

See also: [Drawdown](#drawdown), [Maximum Drawdown](#maximum-drawdown), [Journal](#journal).

### Expectancy

<a id="expectancy"></a>

*The average result per trade in a sample.* Level: intermediate.

Expectancy is the win rate times the average win, minus the loss rate times the average loss, in money or in R. It describes the sample you already recorded. A positive figure in a backtest is not a promise that the next sample matches it.

See also: [Win Rate](#win-rate), [Payoff Ratio](#payoff-ratio), [Backtest](#backtest).

### Hard Stop

<a id="hard-stop"></a>

*A stop order that sits in the market, not only in your notes.* Level: beginner.

A hard stop is a live order the venue can execute if price trades there, even if you are away. It can still slip. A stop that exists only as an intention is a different control, and the journal should say which one you used.

See also: [Stop Loss](#stop-loss), [Stop Order](#stop-order), [Slippage](#slippage).

### Invalidation

<a id="invalidation"></a>

*The condition that means the original idea no longer holds.* Level: beginner.

An invalidation is the event you named in advance as the reason to exit or to rebuild, such as a close beyond the range or a broken swing. It is part of the plan, not a feeling after the fact. Without it, a review has nothing to test.

See also: [Stop Loss](#stop-loss), [Range Thesis](#range-thesis), [Trading Plan](#trading-plan).

### Kelly Criterion

<a id="kelly-criterion"></a>

*A formula for a size that maximises growth under strong assumptions.* Level: advanced.

The Kelly fraction, in its simple form, uses a win rate and a payoff to suggest a stake that maximises long-run growth inside that model. The assumptions are strict, and estimated inputs are noisy. Full Kelly is a study topic, and it is not a size Atlas tells you to use.

See also: [Expectancy](#expectancy), [Position Sizing](#position-sizing), [Risk of Ruin](#risk-of-ruin).

### Maximum Drawdown

<a id="maximum-drawdown"></a>

*The deepest peak-to-trough decline in the sample.* Level: intermediate.

Maximum drawdown is the largest fall from an equity peak to a later trough, before a new peak. It is a historical fact about that sample. A live account can exceed it, which is why a risk plan does not treat the past worst as a cap.

See also: [Drawdown](#drawdown), [Drawdown Recovery](#drawdown-recovery), [Equity Curve](#equity-curve).

### Monte Carlo

<a id="monte-carlo"></a>

*Many reshuffles of a sample, used to see a spread of paths.* Level: advanced.

A Monte Carlo study reorders or resimulates a set of trade results many times and records the spread of equity paths. The output cannot be better than the trades you fed in. It shows path risk inside that sample, and it does not invent a new edge.

See also: [Equity Curve](#equity-curve), [Expectancy](#expectancy), [Sample Size](#sample-size).

### Payoff Ratio

<a id="payoff-ratio"></a>

*The average win divided by the average loss.* Level: intermediate.

The payoff ratio is how large the typical winner is compared with the typical loser in the sample. Together with the win rate it builds expectancy. Either number alone is an incomplete description.

See also: [Win Rate](#win-rate), [Expectancy](#expectancy), [R Multiple](#r-multiple).

### Position Sizing

<a id="position-sizing"></a>

*Choosing exposure so a loss stays inside a planned risk.* Level: beginner.

Position sizing is the decision of how large a position is, given the stop distance and the amount you are willing to lose if the stop is hit. Bigger size with the same stop means a bigger loss. The lesson is arithmetic, not a required size.

See also: [Risk per Trade](#risk-per-trade), [Stop Distance](#stop-distance), [Capital Allocation](#capital-allocation).

### R Multiple

<a id="r-multiple"></a>

*A result measured in units of the amount risked.* Level: intermediate.

One R is the amount you planned to lose if the stop was hit. A gain of twice that amount is plus two R, and a loss of the planned amount is minus one R. Stating results in R lets you compare trades that had different prices and different sizes.

See also: [Risk per Trade](#risk-per-trade), [Expectancy](#expectancy), [Stop Distance](#stop-distance).

### Risk Budget

<a id="risk-budget"></a>

*The total loss you will accept across open ideas at once.* Level: intermediate.

A risk budget caps the sum of risk-per-trade across everything that is open, so several small trades cannot silently become one large bet. Correlation matters, because positions that fall together are one risk wearing several names. The budget is a constraint, not a target to fill.

See also: [Portfolio Heat](#portfolio-heat), [Correlation](#correlation), [Risk per Trade](#risk-per-trade).

### Risk of Ruin

<a id="risk-of-ruin"></a>

*The chance a sequence of losses hits a ruin threshold, under stated assumptions.* Level: advanced.

Risk of ruin is the probability, inside a model, that equity falls to a level you have called ruin, given a win rate, a payoff, and a size. Change the assumptions and the probability changes. It is a stress question, not a prediction about your account.

See also: [Expectancy](#expectancy), [Position Sizing](#position-sizing), [Monte Carlo](#monte-carlo).

### Risk per Trade

<a id="risk-per-trade"></a>

*The cash amount lost if the stop fills at the planned price.* Level: beginner.

Risk per trade is position size times stop distance, plus a realistic allowance for fees and slippage. It is the number you compare with account risk. If the stop fills worse than planned, the realised loss is larger than this figure.

See also: [Position Sizing](#position-sizing), [Stop Distance](#stop-distance), [Slippage](#slippage).

### Risk-reward Ratio

<a id="risk-reward"></a>

*The planned gain compared with the planned loss.* Level: beginner.

Risk-reward compares the distance to the planned exit for a gain with the distance to the planned stop. A ratio is a statement about the plan, not about how often the gain will print. A flattering ratio with a tiny chance of being reached is still a plan you should be able to say out loud.

See also: [R Multiple](#r-multiple), [Take Profit](#take-profit), [Stop Loss](#stop-loss).

### Stop Distance

<a id="stop-distance"></a>

*How far the invalidation sits from the entry, in price.* Level: beginner.

Stop distance is the price gap between the entry and the stop. Position size falls as this gap rises, if the money you are willing to lose stays fixed. A stop placed so close that ordinary noise hits it is a different error from a stop placed so far that the loss is too large.

See also: [Position Sizing](#position-sizing), [ATR](#atr), [Stop Loss](#stop-loss).

### Stop Loss

<a id="stop-loss"></a>

*A predefined exit used to cap a loss or honour an invalidation.* Level: beginner.

A stop-loss is an order or a rule that exits when price reaches a level that means the idea is wrong, or when the loss has hit the planned amount. A stop can fill worse than its level in a fast market. It is a boundary, not a guarantee the loss stops there.

See also: [Stop Distance](#stop-distance), [Invalidation](#invalidation), [Slippage](#slippage).

### Time Stop

<a id="time-stop"></a>

*An exit that fires because too much time has passed.* Level: intermediate.

A time stop closes a trade, or forces a review, after a set number of candles if the idea has not worked. It treats a stale idea as a cost of attention and of risk budget. The clock is a rule you choose, not a property of the market.

See also: [Invalidation](#invalidation), [Trading Plan](#trading-plan), [Stop Loss](#stop-loss).

### Trailing Stop

<a id="trailing-stop"></a>

*A stop that moves in your favour under a written rule.* Level: intermediate.

A trailing stop ratchets toward price as the trade moves your way, by a fixed distance, an ATR multiple, or a swing rule. It can lock in an open gain, and it can exit a trend on ordinary noise if the trail is tight. The rule belongs in the plan before the trade.

See also: [Stop Loss](#stop-loss), [ATR](#atr), [Trailing Grid](#trailing-grid).

### Variance

<a id="variance"></a>

*The square of standard deviation, a raw measure of scatter.* Level: advanced.

Variance is the average squared distance of values from their mean. Standard deviation is its square root, which puts the unit back into price or return space. Both describe scatter in a sample, and neither forecasts the next print.

See also: [Standard Deviation](#standard-deviation), [Volatility](#volatility), [Monte Carlo](#monte-carlo).

### Volatility Drag

<a id="volatility-drag"></a>

*The damage variance does to a compounded path.* Level: advanced.

Volatility drag is the gap between the average of a series of returns and the compounded result, which variance pulls downward. A path that swings widely can compound to less than its average return suggests. This is arithmetic, not a reason to chase smoother marketing numbers.

See also: [Compounding](#compounding), [Variance](#variance), [Drawdown](#drawdown).

### Win Rate

<a id="win-rate"></a>

*The share of trades in a sample that finished positive.* Level: beginner.

Win rate is the count of winning trades divided by the count of all trades in the sample. A high win rate can still lose money if the losses are much larger than the wins. Quote it with the payoff ratio, or do not quote it as a summary.

See also: [Expectancy](#expectancy), [Payoff Ratio](#payoff-ratio), [Sample Size](#sample-size).

## Derivatives and leverage

<a id="derivatives"></a>

### Auto-deleveraging

<a id="auto-deleveraging"></a>

*A forced reduction of profitable positions when a venue cannot cover a deficit.* Level: advanced.

Auto-deleveraging closes or cuts opposing profitable positions when liquidation losses exceed the insurance waterfall. You can be taken out of a winning trade under the venue's ranking. Read that ranking before you treat a hedge as certain to stay open.

See also: [Insurance Fund](#insurance-fund), [Liquidation](#liquidation), [Hedge](#hedge).

### Backwardation

<a id="backwardation"></a>

*A futures curve where later expiries cost less than spot.* Level: advanced.

Backwardation means a longer-dated contract trades below spot. The curve can reflect demand to hold the spot asset or stress in the market. It is a description of the curve on that day.

See also: [Contango](#contango), [Basis](#basis), [Dated Future](#dated-future).

### Basis

<a id="basis"></a>

*The gap between a derivative's price and the spot reference.* Level: intermediate.

Basis is the futures or perpetual price minus the spot price, or the reverse, depending on the convention you state. A positive basis means the derivative trades above spot. Basis can come from funding, carry, and demand for leverage, and it can flip.

See also: [Contango](#contango), [Backwardation](#backwardation), [Funding Rate](#funding-rate).

### Contango

<a id="contango"></a>

*A futures curve where later expiries cost more than spot.* Level: advanced.

Contango means a longer-dated contract trades above the spot price, so the curve slopes upward. Holding that exposure through the roll has a cost if you buy high and the contract converges down. The slope is a price, not a view Atlas endorses.

See also: [Backwardation](#backwardation), [Basis](#basis), [Dated Future](#dated-future).

### Cross Margin

<a id="cross-margin"></a>

*One pool of collateral shared across positions.* Level: intermediate.

Cross margin lets open positions draw on the same collateral balance. A winner can support a loser, and a loser can consume collateral you thought was spare. Know which mode is selected before size is live.

See also: [Isolated Margin](#isolated-margin), [Margin](#margin), [Portfolio Heat](#portfolio-heat).

### Dated Future

<a id="dated-future"></a>

*A futures contract with a set expiry and settlement.* Level: intermediate.

A dated future expires on a known date, when it settles to a reference or delivers under its rules. The price converges toward that settlement as expiry nears. Rolling to a later contract replaces one basis with another.

See also: [Perpetual Future](#perpetual-future), [Expiry](#expiry), [Basis](#basis).

### Delta

<a id="delta"></a>

*How much a position's value moves when the underlying moves.* Level: advanced.

Delta is the change in a position for a small change in the underlying price. A plain long coin has a delta near one unit per unit. Options and liquidity-provider positions have deltas that change as price moves, so a hedge set once does not stay matched.

See also: [Delta-neutral](#delta-neutral), [Hedge](#hedge), [Exposure](#exposure).

### Delta-neutral

<a id="delta-neutral"></a>

*A book whose net delta is near zero.* Level: advanced.

A delta-neutral book is arranged so a small move in the underlying changes the book very little. Funding, basis, fees, and a delta that drifts can still produce a result. Neutral to price is not neutral to every other risk.

See also: [Delta](#delta), [Hedge](#hedge), [Funding Rate](#funding-rate).

### Expiry

<a id="expiry"></a>

*The moment a dated contract settles and ceases.* Level: beginner.

Expiry is the timestamp when a dated future or option reaches its end and settles under the contract rules. Positions still open are closed or delivered by that process. A grid or a hedge that depends on the contract needs a plan for that moment.

See also: [Dated Future](#dated-future), [Settlement](#settlement), [Basis](#basis).

### Funding Interval

<a id="funding-interval"></a>

*How often perpetual funding is exchanged.* Level: intermediate.

The funding interval is the schedule of funding payments, such as every eight hours on many venues, though the schedule is the venue's rule. A quoted funding rate is meaningless until you know the interval it belongs to. Check the current schedule rather than remembering an old one.

See also: [Funding Rate](#funding-rate), [Perpetual Future](#perpetual-future), [Futures Grid](#futures-grid).

### Funding Rate

<a id="funding-rate"></a>

*A periodic payment between long and short perpetual positions.* Level: intermediate.

The funding rate is a regular transfer between longs and shorts on a perpetual, designed to keep the contract near a spot reference. One side pays and the other receives. It is a carrying cost or credit, and it can flip.

See also: [Perpetual Future](#perpetual-future), [Funding Interval](#funding-interval), [Long](#long).

### Hedge

<a id="hedge"></a>

*A position taken to offset an existing exposure.* Level: intermediate.

A hedge reduces a risk you already have, such as a short derivative against coins you hold. The offset is only as good as the size, the timing, and the contract staying open. A hedge that is the wrong size is a new bet, not a cancellation.

See also: [Delta](#delta), [Exposure](#exposure), [Auto-deleveraging](#auto-deleveraging).

### Index Price

<a id="index-price"></a>

*A composite spot reference used to anchor a derivative.* Level: intermediate.

An index price blends prices from one or more spot sources under a published method. Perpetual funding and the mark often refer to it. If the sources are thin or the method is stale, the index can be a poor picture of where you can actually trade.

See also: [Mark Price](#mark-price), [Oracle](#oracle), [Funding Rate](#funding-rate).

### Initial Margin

<a id="initial-margin"></a>

*The collateral required to open a position.* Level: intermediate.

Initial margin is the minimum collateral a venue requires at entry, often a fraction of notional. A lower initial margin is higher leverage. Meeting the minimum is not the same as sizing the risk to your account rule.

See also: [Margin](#margin), [Leverage](#leverage), [Notional](#notional).

### Insurance Fund

<a id="insurance-fund"></a>

*A venue buffer that absorbs some losses beyond liquidated margin.* Level: advanced.

An insurance fund is capital a derivatives venue sets aside to cover losses when a liquidated account goes below zero. If the fund and the waterfall are not enough, some venues socialise the rest through auto-deleveraging. The fund is a design feature, not a promise your loss is capped.

See also: [Auto-deleveraging](#auto-deleveraging), [Liquidation](#liquidation), [Counterparty Risk](#counterparty-risk).

### Inverse Contract

<a id="inverse-contract"></a>

*A derivative margined in the base coin, with a nonlinear payoff.* Level: advanced.

An inverse contract is margined and settled in the coin itself, and the payoff in coin terms is not a straight line against price. The same price move means a different coin result at different prices. Read the contract sheet before you treat it as a simple short or long.

See also: [Linear Contract](#linear-contract), [Base Asset](#base-asset), [Notional](#notional).

### Isolated Margin

<a id="isolated-margin"></a>

*Margin assigned to one position, not to the whole account.* Level: intermediate.

Isolated margin limits the collateral a single position can consume to the amount you assigned to it. A liquidation then ends that position rather than pulling the rest of the wallet, under that venue's rules. The rest of the account is safer only if you truly did not assign it.

See also: [Cross Margin](#cross-margin), [Liquidation](#liquidation), [Margin](#margin).

### Leverage

<a id="leverage"></a>

*Borrowed exposure that magnifies both gains and losses.* Level: beginner.

Leverage lets a derivatives position control more exposure than the margin posted. It magnifies losses as well as gains, and it can bring a liquidation price closer to the market. It is not a way to make a weak idea safer.

See also: [Liquidation Price](#liquidation-price), [Margin](#margin), [Futures Grid](#futures-grid).

### Linear Contract

<a id="linear-contract"></a>

*A derivative margined and settled in the quote asset.* Level: advanced.

A linear contract measures profit in the quote asset, often a stablecoin, so a one-unit move has a stable quote value. Margin is posted in that quote. This is different from an inverse contract, where the margin coin's own price changes the result.

See also: [Inverse Contract](#inverse-contract), [Quote Asset](#quote-asset), [Perpetual Future](#perpetual-future).

### Liquidation

<a id="liquidation"></a>

*A forced close when collateral no longer covers the venue's rule.* Level: beginner.

Liquidation is the venue closing a leveraged position because margin has fallen through its threshold. The fill can be worse than the published liquidation price in a fast move. It is a mechanical event, not a judgement about the asset.

See also: [Liquidation Price](#liquidation-price), [Maintenance Margin](#maintenance-margin), [Insurance Fund](#insurance-fund).

### Liquidation Price

<a id="liquidation-price"></a>

*The price where margin may no longer support a leveraged position.* Level: beginner.

The liquidation price is the venue's estimate of where a leveraged position can be closed by force because margin is too thin. It moves if you add margin, change size, or if the mark price and fees change. It is a risk boundary, not a target.

See also: [Liquidation](#liquidation), [Leverage](#leverage), [Mark Price](#mark-price).

### Long

<a id="long"></a>

*Exposure that gains if the price rises.* Level: beginner.

A long position profits if the price of the asset rises and loses if it falls, before fees and funding. Owning the coin is a long. A perpetual can be a long as well, and the word describes the direction of the bet, not a recommendation to hold one.

See also: [Short](#short), [Exposure](#exposure), [Long Grid](#long-grid).

### Maintenance Margin

<a id="maintenance-margin"></a>

*The collateral floor below which a position can be liquidated.* Level: intermediate.

Maintenance margin is the level of collateral the venue requires you to keep. Fall below it, and liquidation rules can start. The published floor is the venue's rule, not a suggested operating point.

See also: [Margin Call](#margin-call), [Liquidation](#liquidation), [Margin](#margin).

### Margin

<a id="margin"></a>

*Collateral posted to support a derivatives position.* Level: beginner.

Margin is the balance the venue holds against your open contracts. Initial margin opens the position and maintenance margin is the floor below which the venue may liquidate. Margin is not a fee, and it is capital that can be lost.

See also: [Initial Margin](#initial-margin), [Maintenance Margin](#maintenance-margin), [Leverage](#leverage).

### Margin Call

<a id="margin-call"></a>

*A demand to add collateral or reduce the position.* Level: intermediate.

A margin call is the venue telling you that collateral is too low for the open risk. You add margin, cut size, or the venue may close the position under its rules. In many crypto venues the close happens automatically, with little or no call in the old sense.

See also: [Maintenance Margin](#maintenance-margin), [Liquidation](#liquidation), [Isolated Margin](#isolated-margin).

### Mark Price

<a id="mark-price"></a>

*The reference price a venue uses for unrealised results and liquidation.* Level: intermediate.

The mark price is a calculated reference, often from an index and sometimes smoothed, used to value positions and to test liquidation. It can differ from the last traded price. Know which price your stop and your liquidation actually watch.

See also: [Index Price](#index-price), [Last Price](#last-price), [Liquidation Price](#liquidation-price).

### Notional

<a id="notional"></a>

*The face value of a position, before considering margin.* Level: beginner.

Notional value is price times size, the full market value the position refers to. Margin is only the collateral posted. A small margin balance can sit under a large notional, which is what leverage means.

See also: [Leverage](#leverage), [Margin](#margin), [Exposure](#exposure).

### Open Interest

<a id="open-interest"></a>

*The stock of derivatives contracts still open.* Level: intermediate.

Open interest is the number, or the notional, of contracts that have been opened and not yet closed. It rises when new positions are created and falls when they are closed. It is a stock of exposure, not a forecast of direction.

See also: [Volume](#volume), [Liquidation](#liquidation), [Perpetual Future](#perpetual-future).

### Perpetual Future

<a id="perpetual-future"></a>

*A derivative with no expiry, kept near spot by funding.* Level: beginner.

A perpetual future has no settlement date. Funding payments between longs and shorts are the usual mechanism that tugs its price toward a spot index. You can hold it for a long time, and you pay or receive funding the whole time it is open.

See also: [Funding Rate](#funding-rate), [Dated Future](#dated-future), [Mark Price](#mark-price).

### Settlement

<a id="settlement"></a>

*The process that closes a contract at expiry or pays a difference.* Level: intermediate.

Settlement is how a derivative ends: cash difference against a reference, or delivery of the asset, under the contract. The reference price and the time are defined by the venue. Read them before you hold into the event.

See also: [Expiry](#expiry), [Index Price](#index-price), [Dated Future](#dated-future).

### Short

<a id="short"></a>

*Exposure that gains if the price falls.* Level: beginner.

A short position profits if the price falls and loses if it rises, before fees and funding. In derivatives it is a contract, not a borrowed coin you must find yourself, though the venue may be borrowing under the hood. Losses on a short are not capped by the price falling to zero in the way a long's price is.

See also: [Long](#long), [Exposure](#exposure), [Short Grid](#short-grid).

## Venues, orders, and registration

<a id="execution"></a>

### AML

<a id="aml"></a>

*Anti-money-laundering controls around the movement of value.* Level: beginner.

AML is the set of laws and internal controls aimed at spotting and reporting proceeds of crime. Businesses that exchange digital currency for fiat in Australia sit inside a registration and reporting framework run by AUSTRAC. Atlas describes the framework, and it does not tell a reader whether their own activity is caught.

See also: [KYC](#kyc), [AUSTRAC](#austrac), [Digital Currency Exchange](#digital-currency-exchange).

### Ask

<a id="ask"></a>

*A resting sell order at a stated price.* Level: beginner.

An ask, or offer, is a price and a size at which someone is willing to sell. The best ask is the lowest of those prices. Buying at the ask means you lift that sell interest.

See also: [Bid](#bid), [Spread](#spread), [Market Order](#market-order).

### AUSTRAC

<a id="austrac"></a>

*The Australian agency that registers digital currency exchange providers.* Level: beginner.

AUSTRAC is the Australian Transaction Reports and Analysis Centre. A business that exchanges digital currency for fiat, in the course of carrying on that business, generally has to register and meet reporting duties. The public register is the place to check a named business, and this sentence is general information, not a ruling on any reader.

See also: [Digital Currency Exchange](#digital-currency-exchange), [AML](#aml), [KYC](#kyc).

### Base Asset

<a id="base-asset"></a>

*The asset being priced, such as the coin in a pair.* Level: beginner.

The base asset is the coin or token the pair is quoting a price for. In a spot grid you can end up holding more of it after a fall. Know which asset you will actually be left with.

See also: [Quote Asset](#quote-asset), [Inventory](#inventory), [Spot Grid](#spot-grid).

### Best Bid and Offer

<a id="best-bid-and-offer"></a>

*The highest bid and the lowest ask, shown together.* Level: beginner.

The best bid and offer are the inside prices of the book. The gap between them is the spread. A quote you see is only as firm as the size sitting there.

See also: [Bid](#bid), [Ask](#ask), [Spread](#spread).

### Bid

<a id="bid"></a>

*A resting buy order at a stated price.* Level: beginner.

A bid is a price and a size at which someone is willing to buy. The best bid is the highest of those prices. Selling into the bid means you hit that buy interest and usually pay the taker schedule.

See also: [Ask](#ask), [Spread](#spread), [Limit Order](#limit-order).

### Centralised Exchange

<a id="centralised-exchange"></a>

*A venue that holds accounts and matches orders on its own books.* Level: beginner.

A centralised exchange is a company that custodies assets, runs an order book, and matches trades for account holders. You have counterparty risk on that company. Atlas explains the type of venue, and it does not name or rank individual venues.

See also: [Decentralised Exchange](#decentralised-exchange), [Custody](#custody), [Order Book](#order-book).

### Conditional Order

<a id="conditional-order"></a>

*An order that waits for a condition before it is sent.* Level: intermediate.

A conditional order, including many stops and triggers, is held until a price, a time, or another event occurs. Until then it may live on the venue's servers rather than in the public book. If those servers or the connection fail, the condition may not fire.

See also: [Trigger Price](#trigger-price), [Stop Order](#stop-order), [Hard Stop](#hard-stop).

### Decentralised Exchange

<a id="decentralised-exchange"></a>

*A venue where trades settle through contracts you sign yourself.* Level: beginner.

A decentralised exchange matches swaps with a pool or an on-chain book, and you keep the wallet that signs. There is no account in the usual sense, and there is smart-contract risk instead. Naming the category is not a recommendation to use any particular protocol.

See also: [Centralised Exchange](#centralised-exchange), [AMM](#amm), [Wallet](#wallet).

### Depth

<a id="depth"></a>

*How much size rests near the current price.* Level: beginner.

Depth is the quantity available at and near the best prices. A deep book can absorb a larger order with less price impact. A screenshot of depth is a moment, and it can vanish when you send the order.

See also: [Liquidity](#liquidity), [Order Book](#order-book), [Price Impact](#price-impact).

### Digital Currency Exchange

<a id="digital-currency-exchange"></a>

*A business that exchanges digital currency and fiat, in AUSTRAC's terms.* Level: beginner.

In Australian registration language, a digital currency exchange provider exchanges digital currency for money or the reverse. Registration is a record that the business enrolled. It is not a safety rating and not an endorsement of any venue, and atlas does not list venues.

See also: [AUSTRAC](#austrac), [Centralised Exchange](#centralised-exchange), [Fiat On-ramp](#fiat-on-ramp).

### Fiat On-ramp

<a id="fiat-on-ramp"></a>

*A path that turns government currency into crypto.* Level: beginner.

A fiat on-ramp is the service that converts dollars or another government currency into a cryptoasset, and an off-ramp does the reverse. The provider, the fees, and the registration status are facts to check at the source. A glossary does not choose a provider.

See also: [Digital Currency Exchange](#digital-currency-exchange), [Quote Asset](#quote-asset), [KYC](#kyc).

### Fill or Kill

<a id="fill-or-kill"></a>

*An instruction to fill the whole order immediately or cancel it.* Level: advanced.

Fill or kill demands a complete immediate fill. If the book cannot do the whole size at the conditions allowed, nothing trades. It is useful when a partial fill would leave a position you do not want.

See also: [Immediate or Cancel](#immediate-or-cancel), [Partial Fill](#partial-fill), [Time in Force](#time-in-force).

### Good till Cancelled

<a id="good-till-cancelled"></a>

*A resting order that stays until it fills or you cancel it.* Level: beginner.

Good till cancelled leaves a limit working across sessions until a fill or a cancel, subject to the venue's own expiry rules. Some venues quietly expire orders anyway. Check the order the next day rather than assuming it is still there.

See also: [Time in Force](#time-in-force), [Limit Order](#limit-order), [Partial Fill](#partial-fill).

### Iceberg Order

<a id="iceberg-order"></a>

*A large order that shows only a slice of its size.* Level: advanced.

An iceberg displays a small visible quantity and reloads as that slice fills, until the hidden total is done. The book you see understates that order's size. Not every venue offers the type, and the rules for reload differ.

See also: [Order Book](#order-book), [Depth](#depth), [Limit Order](#limit-order).

### Immediate or Cancel

<a id="immediate-or-cancel"></a>

*Fill what you can right now, and cancel the rest.* Level: advanced.

Immediate or cancel takes whatever quantity is available at the allowed prices and cancels the remainder. Unlike fill or kill, a partial fill is allowed. The unfilled part does not rest on the book.

See also: [Fill or Kill](#fill-or-kill), [Partial Fill](#partial-fill), [Market Order](#market-order).

### KYC

<a id="kyc"></a>

*Know-your-customer checks a venue uses to identify account holders.* Level: beginner.

KYC is the identity process a regulated business uses, such as collecting a name and evidence of identity, before it offers an account. Rules differ by country and by business. This is general information about the phrase, not advice on your own obligations.

See also: [AML](#aml), [AUSTRAC](#austrac), [Centralised Exchange](#centralised-exchange).

### Last Price

<a id="last-price"></a>

*The price of the most recent trade on that market.* Level: beginner.

The last price is simply the latest fill. It can jump on a small trade in a thin book. Do not assume the mark, the index, and the last price are the same number.

See also: [Mark Price](#mark-price), [Spread](#spread), [Slippage](#slippage).

### Limit Order

<a id="limit-order"></a>

*An order that trades only at your price or better.* Level: beginner.

A limit order states the worst price you will accept. It may rest on the book and add liquidity, or it may fill at once if the market is already through it. A limit that never trades has controlled the price and has not made the trade.

See also: [Market Order](#market-order), [Maker](#maker), [Post-only](#post-only).

### Liquidity

<a id="liquidity"></a>

*How easily size can trade without a large price move.* Level: beginner.

Liquidity is the ability to buy or sell a given size without moving the price much. Deep books and busy pools are more liquid. In structure lessons the same word also means the stops and resting orders that often sit beyond obvious highs and lows.

See also: [Depth](#depth), [Spread](#spread), [Liquidity Pool](#liquidity-pool).

### Lot Size

<a id="lot-size"></a>

*The smallest quantity step the venue allows.* Level: intermediate.

Lot size, or step size, is the minimum increment of quantity. A size that is not a multiple of the lot is rejected or trimmed. Check it when you translate a risk calculation into an order, because the rounded size changes the risk.

See also: [Tick Size](#tick-size), [Order Size](#order-size), [Position Sizing](#position-sizing).

### Maker

<a id="maker"></a>

*The side that adds a resting order to the book.* Level: beginner.

A maker posts liquidity that someone else can trade against. Maker fees, or rebates, apply when your order rests and is later hit. If your limit crosses the spread and fills at once, you were a taker, whatever you intended.

See also: [Taker](#taker), [Maker Fee](#maker-fee), [Post-only](#post-only).

### Maker Fee

<a id="maker-fee"></a>

*The fee for an order that adds to the book.* Level: beginner.

A maker fee is charged, or sometimes paid as a rebate, when your order rests on the book and adds liquidity. The schedule depends on the venue and your tier. A grid with many small cycles can give this fee a large share of the gross step.

See also: [Taker Fee](#taker-fee), [Maker](#maker), [Fee Drag](#fee-drag).

### Market Order

<a id="market-order"></a>

*An order that takes the best prices available now.* Level: beginner.

A market order buys or sells immediately against resting orders, walking the book if size requires it. You get speed and you give up price control. In a thin or fast market the fill can be far from the last price you saw.

See also: [Limit Order](#limit-order), [Slippage](#slippage), [Taker](#taker).

### Mid Price

<a id="mid-price"></a>

*The average of the best bid and the best ask.* Level: beginner.

The mid price sits halfway between the best bid and the best ask. It is a reference, not a price you can necessarily trade in size. Crossing the spread means paying the ask or selling the bid, not dealing at the mid.

See also: [Spread](#spread), [Bid](#bid), [Ask](#ask).

### One Cancels the Other

<a id="one-cancels-the-other"></a>

*Two orders linked so a fill on one cancels the other.* Level: intermediate.

One-cancels-the-other pairs two orders, often a take-profit and a stop, so that when one fills the other is pulled. If the link fails or one fills partially, you can be left with a live order you did not expect. Confirm the venue's behaviour with a small test in a safe setting.

See also: [Take Profit](#take-profit), [Stop Loss](#stop-loss), [Reduce-only](#reduce-only).

### Order

<a id="order"></a>

*An instruction to trade a size at rules you set.* Level: beginner.

An order is the message you send: side, size, price conditions, and time in force. It is not a trade until it matches. Review the pair, the side, and the size before you send it, because the venue will follow the message.

See also: [Trade](#trade), [Limit Order](#limit-order), [Market Order](#market-order).

### Order Book

<a id="order-book"></a>

*The list of resting bids and asks at each price.* Level: beginner.

An order book shows the buy orders and sell orders waiting at each price. A match happens when a new order crosses a resting one, or when two resting orders meet under the venue's rules. The visible book is not always the whole interest, because hidden size exists on some venues.

See also: [Bid](#bid), [Ask](#ask), [Depth](#depth).

### Partial Fill

<a id="partial-fill"></a>

*An order that trades some of its size and leaves the rest.* Level: beginner.

A partial fill means only part of the quantity was matched. The rest may rest, cancel, or fail, depending on time in force. Position size and risk should be computed from what actually filled, not from what you sent.

See also: [Order Size](#order-size), [Time in Force](#time-in-force), [Slippage](#slippage).

### Post-only

<a id="post-only"></a>

*A limit that cancels itself if it would take liquidity.* Level: intermediate.

A post-only order is allowed to rest as a maker and is rejected or repriced if it would match immediately. It is how a grid tries to stay on the maker schedule. If the market runs away, the order simply does not trade.

See also: [Maker](#maker), [Limit Order](#limit-order), [Maker Fee](#maker-fee).

### Price Impact

<a id="price-impact"></a>

*How far your own order moves the price.* Level: intermediate.

Price impact is the move caused by consuming depth, or by shifting a pool's reserves, as your size trades. It grows with size relative to available liquidity. A quote from a tiny test trade will not match the impact of a much larger one.

See also: [Slippage](#slippage), [Depth](#depth), [AMM](#amm).

### Quote Asset

<a id="quote-asset"></a>

*The asset used to price the base, often a stablecoin or a fiat unit.* Level: beginner.

The quote asset is the unit the price is expressed in. A grid spends and receives the quote as it buys and sells the base. If the quote itself can move or depeg, that is a separate risk from the chart.

See also: [Base Asset](#base-asset), [Stablecoin](#stablecoin), [Spread](#spread).

### Reduce-only

<a id="reduce-only"></a>

*An order that may only shrink an open position.* Level: intermediate.

A reduce-only order cannot flip you from long to short or increase size. Venues use it so a closing order does not accidentally open a new exposure. It limits the direction of the size change and does not promise that the order will fill.

See also: [Stop Loss](#stop-loss), [Take Profit](#take-profit), [Position Sizing](#position-sizing).

### Slippage

<a id="slippage"></a>

*The gap between the expected price and the fill.* Level: beginner.

Slippage is the difference between the price you thought you would trade and the price you actually received. It grows when you trade size into a thin book or a fast move. A backtest that ignores it overstates the historical result.

See also: [Price Impact](#price-impact), [Spread](#spread), [Market Order](#market-order).

### Slippage Tolerance

<a id="slippage-tolerance"></a>

*The largest price move you will still accept on a swap or an order.* Level: intermediate.

Slippage tolerance is the maximum worse price you allow before the trade should fail. Set tight, and a moving market cancels the attempt. Set loose, and a bad fill or a hostile ordering of transactions can stand, and the number is a limit, not a prediction of the fill.

See also: [Slippage](#slippage), [Price Impact](#price-impact), [Sandwich Attack](#sandwich-attack).

### Spread

<a id="spread"></a>

*The gap between the best bid and the best ask.* Level: beginner.

The spread is the best ask minus the best bid. A wide spread is a real cost of crossing the market, on top of fees. Thin books often show wider spreads.

See also: [Bid](#bid), [Ask](#ask), [Depth](#depth).

### Stop Order

<a id="stop-order"></a>

*An order that becomes active only after a trigger price prints.* Level: beginner.

A stop order waits until the trigger is touched, and then it becomes a market or a limit order, depending on the type. The trigger is not the fill. In a gap, the fill can be beyond the trigger.

See also: [Stop-limit Order](#stop-limit-order), [Trigger Price](#trigger-price), [Stop Loss](#stop-loss).

### Stop-limit Order

<a id="stop-limit-order"></a>

*A stop that, once triggered, rests as a limit rather than a market order.* Level: intermediate.

A stop-limit has a trigger and a limit price. After the trigger, it will only fill at the limit or better, so in a fast move it may not fill at all. Use it when a missed fill is more acceptable to the plan than an unbounded fill.

See also: [Stop Order](#stop-order), [Limit Order](#limit-order), [Slippage](#slippage).

### Take Profit

<a id="take-profit"></a>

*A predefined condition for closing a gain.* Level: beginner.

A take-profit is an order or a rule that closes a position once price reaches a level you chose in advance. It locks the result you planned. It does not mean the market will reach that level.

See also: [Stop Loss](#stop-loss), [Limit Order](#limit-order), [R Multiple](#r-multiple).

### Taker

<a id="taker"></a>

*The side that removes a resting order from the book.* Level: beginner.

A taker trades against liquidity that is already there. Market orders are takers, and so is a limit that is marketable on arrival. The taker fee schedule is the one that applies to that fill.

See also: [Maker](#maker), [Taker Fee](#taker-fee), [Market Order](#market-order).

### Taker Fee

<a id="taker-fee"></a>

*The fee for an order that removes liquidity from the book.* Level: beginner.

A taker fee is charged when your order matches immediately against resting orders. Market orders are takers, and so are marketable limit orders. Taker fees are usually higher than maker fees on the same schedule.

See also: [Maker Fee](#maker-fee), [Taker](#taker), [Market Order](#market-order).

### Tick Size

<a id="tick-size"></a>

*The smallest price increment the venue allows.* Level: intermediate.

Tick size is the minimum step between legal prices, such as one cent or a smaller unit on a low-priced pair. Orders between ticks are rejected or rounded under the venue's rule. A grid spaced more tightly than the tick cannot be built.

See also: [Lot Size](#lot-size), [Grid Spacing](#grid-spacing), [Limit Order](#limit-order).

### Time in Force

<a id="time-in-force"></a>

*The instruction for how long an order is allowed to work.* Level: intermediate.

Time in force covers rules such as good till cancelled, immediate or cancel, and fill or kill. It decides whether an unfilled order rests, dies at once, or dies at a time. The price and the size are not the whole order.

See also: [Good till Cancelled](#good-till-cancelled), [Immediate or Cancel](#immediate-or-cancel), [Fill or Kill](#fill-or-kill).

### Trade

<a id="trade"></a>

*A match between two orders that produces a fill.* Level: beginner.

A trade is the executed result, a price and a size, when orders match. One order can become several trades as it walks the book. The trade record, not the order ticket, is what the journal should score.

See also: [Order](#order), [Partial Fill](#partial-fill), [Journal](#journal).

### Trigger Price

<a id="trigger-price"></a>

*The price that activates a bot or a conditional order.* Level: beginner.

A trigger price is the condition that turns a plan on, such as starting a grid or firing a stop. Until it prints, the working orders may not exist. Set it from the plan, and check it before you leave the order live.

See also: [Stop Order](#stop-order), [Conditional Order](#conditional-order), [Invalidation](#invalidation).

## Wallets and security

<a id="security"></a>

### Address Poisoning

<a id="address-poisoning"></a>

*A look-alike address planted in your history so you copy the wrong one.* Level: intermediate.

Address poisoning sends a zero-value or dust transfer from an address that matches the start and end of one you use, so a hasty copy from the history grabs the attacker's address. Read the full string every time. Your history is not an address book.

See also: [Wallet Address](#wallet-address), [Dusting](#dusting), [Phishing](#phishing).

### Allowance

<a id="allowance"></a>

*The maximum a spender may transfer under an approval.* Level: intermediate.

The allowance is the cap on a token approval. A later transaction can spend up to that cap without asking you again. Check the current allowance in a block explorer when you want to know what an old contract can still move.

See also: [Token Approval](#token-approval), [Block Explorer](#block-explorer), [ERC-20](#erc-20).

### API Key

<a id="api-key"></a>

*A credential a program uses to talk to an account.* Level: intermediate.

An API key lets software read an account or place orders, depending on the permissions you tick. A withdrawal-enabled key can move funds, so a bot does not need that permission to place trades. Store keys as secrets, and delete keys you no longer use.

See also: [Trading Bot](#trading-bot), [Two-factor Authentication](#two-factor-authentication), [Withdrawal Whitelist](#withdrawal-whitelist).

### Cold Wallet

<a id="cold-wallet"></a>

*A wallet whose keys stay off the internet.* Level: beginner.

A cold wallet keeps the signing keys on a device or a medium that is not browsing the web. It reduces remote theft and does not protect you from a lost seed, a coerced signing, or a mistake when you move coins back online. The coldness is about the keys, not about the blockchain.

See also: [Hot Wallet](#hot-wallet), [Hardware Wallet](#hardware-wallet), [Seed Phrase](#seed-phrase).

### Custody

<a id="custody"></a>

*Who can actually move the assets.* Level: beginner.

Custody is control of the keys or the account that can transfer the asset. Leave coins on a venue and the venue has custody. Hold the keys yourself and you have self-custody, together with the duty not to lose them.

See also: [Self-custody](#self-custody), [Counterparty Risk](#counterparty-risk), [Private Key](#private-key).

### Dusting

<a id="dusting"></a>

*A tiny unwanted transfer used to mark or to bait an address.* Level: intermediate.

Dusting drops a very small amount of a token into many addresses. Sometimes it is tracking, and sometimes it is bait so you interact with a malicious contract to try to sell the dust. You can ignore tokens you do not recognise, and touching them is the risky step.

See also: [Address Poisoning](#address-poisoning), [Fake Token](#fake-token), [Wallet Address](#wallet-address).

### Fake Token

<a id="fake-token"></a>

*A contract that copies a name or a ticker without being the asset.* Level: beginner.

A fake token uses the same symbol or a similar name as a known asset, on a contract address that is not the real one. The ticker is not an identity. Confirm the contract address from a source you already trust, not from the token's own name.

See also: [Token](#token), [ERC-20](#erc-20), [Wallet Address](#wallet-address).

### Hardware Wallet

<a id="hardware-wallet"></a>

*A dedicated device that holds keys and signs on the device.* Level: beginner.

A hardware wallet keeps the private key inside a purpose-built device and asks you to confirm the transaction on its own screen. The computer can be infected and still not see the key, provided you read the device screen rather than the computer screen. Buy the device from a source you can verify, and never type the seed into the computer.

See also: [Seed Phrase](#seed-phrase), [Cold Wallet](#cold-wallet), [Signature](#signature).

### Hot Wallet

<a id="hot-wallet"></a>

*A wallet whose keys are on a machine connected to the internet.* Level: beginner.

A hot wallet can sign transactions from a phone or a browser, which makes it convenient and exposed. Use it for amounts you are prepared to have online. Long-term holdings belong on a colder setup if the plan says so.

See also: [Cold Wallet](#cold-wallet), [Private Key](#private-key), [Self-custody](#self-custody).

### Multisig

<a id="multisig"></a>

*A wallet that requires several keys to approve an action.* Level: intermediate.

A multisig requires M signatures out of N authorised keys before a transaction is valid. It reduces the damage from one lost or stolen key, and it creates a new problem if too many key-holders are unavailable or collude. The threshold and the list of holders are the whole design.

See also: [Private Key](#private-key), [Governance](#governance), [Custody](#custody).

### Phishing

<a id="phishing"></a>

*A fake message or site that imitates a real service to steal a secret or a signature.* Level: beginner.

Phishing copies a venue, a wallet, or a support agent and asks you to sign, to enter a seed, or to reset a password on a look-alike page. The tell is the request for a secret or an urgent signature. Check the address yourself, and do not use the link in the message.

See also: [Seed Phrase](#seed-phrase), [Wallet Drainer](#wallet-drainer), [Scamwatch](#scamwatch).

### Private Key

<a id="private-key"></a>

*The secret that authorises a signature.* Level: beginner.

A private key is the number that signs transactions for an address. Showing it, typing it into a website, or storing it in a chat is the same as handing over the coins. The public address can be shared, and the private key cannot.

See also: [Public Key](#public-key), [Seed Phrase](#seed-phrase), [Wallet Address](#wallet-address).

### Public Key

<a id="public-key"></a>

*The key that others can use to verify your signatures.* Level: beginner.

A public key is the counterpart of the private key, and an address is usually derived from it. Sharing the public key or the address is how people pay you, and it does not let them sign. Treat any request that blurs the two as hostile.

See also: [Private Key](#private-key), [Wallet Address](#wallet-address), [Signature](#signature).

### Recovery Scam

<a id="recovery-scam"></a>

*A second fraud that offers to retrieve funds already stolen.* Level: beginner.

A recovery scam contacts a victim and promises to get the lost coins back for an up-front fee or a signature. The money does not come back, and the new signature can take what remains. No legitimate recovery starts by asking for a seed phrase.

See also: [Phishing](#phishing), [Seed Phrase](#seed-phrase), [Scamwatch](#scamwatch).

### ReportCyber

<a id="reportcyber"></a>

*The Australian Cyber Security Centre's place to report cybercrime.* Level: beginner.

ReportCyber is the Australian government channel for reporting cybercrime, including stolen accounts and online fraud. Use Scamwatch for the scam report, and use ReportCyber when a crime has taken money or an account.

See also: [Scamwatch](#scamwatch), [Phishing](#phishing), [Wallet Drainer](#wallet-drainer).

### Rug Pull

<a id="rug-pull"></a>

*A project that removes liquidity or control and leaves holders stranded.* Level: beginner.

A rug pull is an exit by the people who control a token or a pool, such as draining the liquidity they added or minting a supply the buyers did not expect. Anonymous control of the pool and of the mint is the structural clue. A famous name on a website is not a control.

See also: [Liquidity Pool](#liquidity-pool), [Fake Token](#fake-token), [Smart-contract Risk](#smart-contract-risk).

### Scamwatch

<a id="scamwatch"></a>

*The ACCC site where Australians report scams.* Level: beginner.

Scamwatch, run by the Australian Competition and Consumer Commission, is where Australians can read about scam types and lodge a report. A report adds to the public warning record and does not itself return funds.

See also: [ReportCyber](#reportcyber), [Phishing](#phishing), [Recovery Scam](#recovery-scam).

### Seed Phrase

<a id="seed-phrase"></a>

*The recovery words that can recreate a wallet's keys.* Level: beginner.

A seed phrase is a list of words from which the private keys are derived. Anyone who has the words has the wallet. Atlas will never ask you for a seed phrase, a password, or a withdrawal-enabled key, and neither should a support message.

See also: [Private Key](#private-key), [Phishing](#phishing), [Hardware Wallet](#hardware-wallet).

### Self-custody

<a id="self-custody"></a>

*Holding the keys that can move your own assets.* Level: beginner.

Self-custody means you, not an account provider, control the private keys. There is no password reset if the seed is lost, and a transfer you sign is final in the ordinary case. The gain is that a venue failure does not, by itself, move those keys.

See also: [Seed Phrase](#seed-phrase), [Custody](#custody), [Hardware Wallet](#hardware-wallet).

### Signature

<a id="signature"></a>

*A cryptographic approval produced by a private key.* Level: beginner.

A signature proves that the holder of a private key agreed to a specific message or transaction. Some signatures move funds at once, and some grant permissions or sign in to a site. Read the human-readable content on a hardware screen before you approve, because the signature is consent.

See also: [Private Key](#private-key), [Wallet Drainer](#wallet-drainer), [Hardware Wallet](#hardware-wallet).

### SIM Swap

<a id="sim-swap"></a>

*A takeover of your phone number so text codes go to someone else.* Level: intermediate.

A SIM swap moves your mobile number onto an attacker's card, so text-message codes arrive there. Codes by text are a weak second factor for that reason. A hardware key or an app that is not the SMS inbox is a stronger second factor for account login.

See also: [Two-factor Authentication](#two-factor-authentication), [Phishing](#phishing), [API Key](#api-key).

### Token Approval

<a id="token-approval"></a>

*Permission for a contract to move your tokens up to an allowance.* Level: intermediate.

A token approval lets a spender contract transfer tokens from your address, up to the allowance you set. An unlimited allowance remains until you revoke it or the tokens are gone. Approve the amount the action needs, and review old spenders you no longer use.

See also: [Allowance](#allowance), [Wallet Drainer](#wallet-drainer), [ERC-20](#erc-20).

### Two-factor Authentication

<a id="two-factor-authentication"></a>

*A second check, beyond a password, before an account action.* Level: beginner.

Two-factor authentication asks for something in addition to the password, such as a time-based code or a hardware security key. It raises the cost of a stolen password. It does not help if you approve a prompt you did not start, or if the attacker already controls the device that receives the code.

See also: [SIM Swap](#sim-swap), [Phishing](#phishing), [API Key](#api-key).

### Wallet Address

<a id="wallet-address"></a>

*The destination identifier you can publish.* Level: beginner.

An address is the string that receives assets on a given network. The same-looking string on the wrong network is a different destination, and funds sent there may be unrecoverable. Check the full string, not the first and last characters, before you send.

See also: [Address Poisoning](#address-poisoning), [Network](#network), [Public Key](#public-key).

### Wallet Drainer

<a id="wallet-drainer"></a>

*A malicious page that asks you to sign a transaction which empties approved assets.* Level: intermediate.

A drainer presents a signature or a transaction that transfers tokens you have approved, often disguised as a claim or a mint. The wallet pop-up is the moment to read the spender, the token, and the amount. If the words on the screen are not the action you intended, reject it.

See also: [Token Approval](#token-approval), [Phishing](#phishing), [Signature](#signature).

### Withdrawal Whitelist

<a id="withdrawal-whitelist"></a>

*A list of the only addresses an account is allowed to withdraw to.* Level: intermediate.

A withdrawal whitelist, where a venue offers it, blocks withdrawals to any address you have not already approved. It slows a thief who has the login but not the whitelist change. Turn it on before you need it, and protect the change itself with a strong second factor.

See also: [API Key](#api-key), [Custody](#custody), [Two-factor Authentication](#two-factor-authentication).

## Crypto fundamentals

<a id="crypto"></a>

### Account Model

<a id="account-model"></a>

*A ledger that stores a balance and a nonce per address.* Level: intermediate.

An account-based chain, such as Ethereum, stores a balance against an address and uses a nonce to order that address's transactions. Contracts are accounts with code. The model makes token balances look like rows, which is a different shape from a UTXO set.

See also: [UTXO](#utxo), [Nonce](#nonce), [Ethereum](#ethereum).

### Bitcoin

<a id="bitcoin"></a>

*The first widely used public cryptocurrency, a proof-of-work ledger with a fixed supply cap.* Level: beginner.

Bitcoin is a public network that records transfers of BTC under proof of work, with a supply schedule that halves and a hard cap written into the protocol. Units are divisible down to the satoshi. This entry defines the system, and it is not a view on the price.

See also: [Proof of Work](#proof-of-work), [Halving](#halving), [Satoshi](#satoshi).

### Block

<a id="block"></a>

*A batch of transactions added to the chain together.* Level: beginner.

A block bundles transactions with a reference to the previous block and a proof that the consensus rule was met. Once later blocks build on it, changing it becomes harder. How many later blocks count as settled depends on the chain's finality rule.

See also: [Blockchain](#blockchain), [Confirmation](#confirmation), [Finality](#finality).

### Block Reward

<a id="block-reward"></a>

*The new coins plus fees paid to the producer of a valid block.* Level: beginner.

The block reward is the subsidy of new coins, where the protocol still issues them, together with the fees of the transactions included. It is how many proof-of-work and proof-of-stake systems pay for security. The schedule of the subsidy is a protocol rule you can read.

See also: [Halving](#halving), [Miner](#miner), [Emission](#emission).

### Block Time

<a id="block-time"></a>

*The target or typical gap between blocks.* Level: beginner.

Block time is how often a chain aims to produce a block, or how often it has actually done so. A shorter target is not the same thing as faster finality. Quote the finality rule beside the block time when you talk about settlement.

See also: [Block](#block), [Finality](#finality), [Throughput](#throughput).

### Blockchain

<a id="blockchain"></a>

*A shared ledger of transactions grouped into blocks.* Level: beginner.

A blockchain is a chain of blocks, each pointing at the one before it, so old records are hard to alter without redoing the later work. Participants agree on the next block through a consensus rule. The ledger can be public and still be wrong about the world outside it.

See also: [Block](#block), [Consensus](#consensus), [Transaction](#transaction).

### BNB

<a id="bnb"></a>

*The native coin of BNB Chain.* Level: beginner.

BNB is the coin used for fees and staking on BNB Chain, a smart-contract network. It is also used inside that wider ecosystem. This entry names the asset and the chain, and it does not name or rank a trading venue.

See also: [Coin](#coin), [Layer 1](#layer-1), [Gas](#gas).

### Bridge

<a id="bridge"></a>

*A system that moves assets or messages between chains.* Level: intermediate.

A bridge locks, burns, or escrows value on one chain and represents it on another, or it passes a message between chains. The trust sits in the verifiers, the multisig, or the proof system the bridge uses. Bridges have been a common point of large losses because they gather value at a seam.

See also: [Wrapped Asset](#wrapped-asset), [Layer 2](#layer-2), [Smart-contract Risk](#smart-contract-risk).

### Burn

<a id="burn"></a>

*A destruction of tokens so they cannot be spent.* Level: beginner.

A burn sends tokens to an address nobody can spend from, or reduces supply inside the contract, under a rule. It shrinks supply only if the tokens are truly unrecoverable. A burn paid for by emissions elsewhere can be a wash, so read both sides.

See also: [Tokenomics](#tokenomics), [Emission](#emission), [Max Supply](#max-supply).

### Chainlink

<a id="chainlink"></a>

*A project that runs oracle networks feeding data to smart contracts.* Level: intermediate.

Chainlink is an oracle network: node operators provide data, such as prices, that contracts can read. LINK is the token associated with that network. How a particular feed is sourced, aggregated, and updated is a property of that feed, not of the brand name alone.

See also: [Oracle](#oracle), [LINK](#link), [Smart Contract](#smart-contract).

### Circulating Supply

<a id="circulating-supply"></a>

*The coins data providers count as available in the market.* Level: intermediate.

Circulating supply is a published estimate of coins that are not locked, unissued, or otherwise excluded by that provider's method. Two sites can disagree. Market capitalisation uses this number, so a soft definition makes a soft capitalisation.

See also: [Max Supply](#max-supply), [Market Capitalisation](#market-capitalisation), [Tokenomics](#tokenomics).

### Coin

<a id="coin"></a>

*The native asset of a blockchain, used for fees and often for staking or mining.* Level: beginner.

A coin, in this library, means the native unit of a chain, such as bitcoin or ether. Tokens are issued on top of a chain by contracts. The usage is a teaching convention, and markets often use the words loosely.

See also: [Token](#token), [Bitcoin](#bitcoin), [Ethereum](#ethereum).

### Confirmation

<a id="confirmation"></a>

*A block built on top of the block that contains your transaction.* Level: beginner.

A confirmation is one block of depth after inclusion. More confirmations mean more work or more stake would have to be unwound to remove the transaction. How many you wait for is a risk choice that depends on the chain and the amount.

See also: [Finality](#finality), [Block](#block), [Reorg](#reorg).

### Consensus

<a id="consensus"></a>

*The rule by which nodes agree on the next block.* Level: beginner.

Consensus is the mechanism that lets independent nodes pick the same history. Proof of work and proof of stake are two families of rule, and they fail in different ways. Agreement among nodes is not the same thing as truth about an off-chain event.

See also: [Proof of Work](#proof-of-work), [Proof of Stake](#proof-of-stake), [Finality](#finality).

### Crypto-backed Stablecoin

<a id="crypto-backed-stablecoin"></a>

*A stablecoin supported by on-chain collateral, usually overcollateralised.* Level: intermediate.

A crypto-backed stablecoin locks other crypto as collateral and mints a token aimed at a reference value. Overcollateralisation is there because the collateral's price moves. If collateral falls faster than liquidations can clear, the design can be left with bad debt.

See also: [Stablecoin](#stablecoin), [Overcollateralisation](#overcollateralisation), [Liquidation](#liquidation).

### Data Availability

<a id="data-availability"></a>

*Whether the data needed to rebuild the chain's state is actually published.* Level: advanced.

Data availability is the question of whether block or rollup data was published so others can check the state. A proof without the underlying data can leave users unable to verify or to exit. The phrase is a security property, not a marketing label.

See also: [Rollup](#rollup), [Node](#node), [Finality](#finality).

### Depeg

<a id="depeg"></a>

*A stablecoin trading away from its reference value.* Level: intermediate.

A depeg is a persistent or sharp gap between a stablecoin's market price and the value it is meant to track. Causes include reserve fears, thin liquidity, oracle faults, and a run on redemptions. A depeg can be brief or it can be the failure of the design.

See also: [Stablecoin](#stablecoin), [Oracle](#oracle), [Liquidity](#liquidity).

### Emission

<a id="emission"></a>

*The ongoing issuance of new tokens.* Level: intermediate.

Emissions are new tokens paid out over time, as a block subsidy or as an incentive program. They dilute holders unless demand absorbs them. A high advertised rate that is mostly emissions is a distribution of new tokens, not evidence of fees.

See also: [Tokenomics](#tokenomics), [Block Reward](#block-reward), [Yield Farming](#yield-farming).

### EOA

<a id="eoa"></a>

*An externally owned account, controlled by a private key rather than by contract code.* Level: intermediate.

An externally owned account is an address whose actions come from a signature by a private key, as distinct from a contract account that runs code. Most ordinary wallets create EOAs. Losing the key means losing the account, because there is no code sitting behind it to recover you.

See also: [Wallet](#wallet), [Private Key](#private-key), [Multisig](#multisig).

### Ethereum

<a id="ethereum"></a>

*A public blockchain built to run general-purpose smart contracts.* Level: beginner.

Ethereum is a layer-1 network whose native coin, ether, pays for gas and is used in staking under its proof-of-stake design. Most of the DeFi vocabulary in this library grew up on its account model. The entry defines the network, and it is not a view on the price.

See also: [Smart Contract](#smart-contract), [Proof of Stake](#proof-of-stake), [Gas](#gas).

### Fiat-backed Stablecoin

<a id="fiat-backed-stablecoin"></a>

*A stablecoin that claims reserves of cash or cash-like assets.* Level: intermediate.

A fiat-backed stablecoin is issued by an entity that says it holds reserves and will redeem under its terms. The risks are the issuer, the reserve quality, the redemption rules, and the law around them. The word backed is a claim you verify from disclosures, not a synonym for safe.

See also: [Stablecoin](#stablecoin), [Depeg](#depeg), [Counterparty Risk](#counterparty-risk).

### Finality

<a id="finality"></a>

*The point after which a transaction is impractical or impossible to reverse under the rules.* Level: intermediate.

Finality is the chain's notion of settlement. Some designs offer probabilistic finality that strengthens as more blocks arrive, and some offer a deterministic checkpoint. A transfer that is final cannot be recalled by a support desk.

See also: [Confirmation](#confirmation), [Reorg](#reorg), [Transaction](#transaction).

### Fork

<a id="fork"></a>

*A split in the rules or in the chain history.* Level: intermediate.

A fork is a divergence. A soft or hard fork can be a deliberate upgrade, and a chain split can leave two histories if the network does not reunite. Coins on one side of a split are not the same asset as coins on the other.

See also: [Hard Fork](#hard-fork), [Blockchain](#blockchain), [Consensus](#consensus).

### Fully Diluted Valuation

<a id="fully-diluted-valuation"></a>

*Price multiplied by the full supply, including coins not yet circulating.* Level: intermediate.

Fully diluted valuation multiplies the current price by max supply, or by a total the provider treats as eventual supply. It imagines today's price still holds when locked coins exist in the market, which is an assumption, not a measurement. Use it beside circulating figures, not instead of a read of the unlocks.

See also: [Market Capitalisation](#market-capitalisation), [Max Supply](#max-supply), [Unlock](#unlock).

### Gas

<a id="gas"></a>

*The fee unit that pays for computation and storage on a chain.* Level: beginner.

Gas measures the work a transaction asks the network to do, and the fee is that work times a price. A complicated contract call costs more gas than a simple transfer. Setting the price too low can leave the transaction waiting, and a reverted call can still consume the fee.

See also: [Transaction](#transaction), [Gwei](#gwei), [Mempool](#mempool).

### Governance Token

<a id="governance-token"></a>

*A token that can vote on protocol parameters, under the protocol's rules.* Level: intermediate.

A governance token grants voting or delegation rights as the contracts define them. It may or may not receive fees. Holding it is not the same as controlling the protocol if a treasury, a multisig, or a low turnout decides outcomes.

See also: [Governance](#governance), [DAO](#dao), [Tokenomics](#tokenomics).

### Gwei

<a id="gwei"></a>

*A small unit of ether used to quote gas prices.* Level: beginner.

A gwei is one billionth of one ether, and gas prices on Ethereum-style chains are usually quoted in gwei. The unit is a denomination, like cents, not a separate asset. A high gwei price means the same transaction costs more of the native coin.

See also: [Gas](#gas), [Ethereum](#ethereum), [Transaction](#transaction).

### Halving

<a id="halving"></a>

*A scheduled cut in the new-coin subsidy on some proof-of-work chains.* Level: beginner.

A halving reduces the block subsidy by half at a block height written into the protocol, as on Bitcoin. It changes the rate of new supply. It does not, by itself, set a price, and the market can do anything around the event.

See also: [Block Reward](#block-reward), [Bitcoin](#bitcoin), [Circulating Supply](#circulating-supply).

### Hard Fork

<a id="hard-fork"></a>

*A rule change that nodes must adopt or they follow a different chain.* Level: intermediate.

A hard fork changes the rules so old software treats the new blocks as invalid. If part of the network refuses the change, two chains can persist. Holding coins through a contentious hard fork means learning which chain your wallet is following.

See also: [Fork](#fork), [Node](#node), [Consensus](#consensus).

### Hash

<a id="hash"></a>

*A fixed-length fingerprint of some data.* Level: beginner.

A hash function turns any input into a short fingerprint, so a tiny change in the input produces a completely different hash. Blocks and transactions are identified by hashes. You cannot rebuild the input from the hash, which is why it works as an identifier and not as a copy.

See also: [Block](#block), [Transaction](#transaction), [Proof of Work](#proof-of-work).

### Hashgraph

<a id="hashgraph"></a>

*A consensus structure that records who gossiped which event to whom.* Level: advanced.

Hashgraph is a data structure and consensus approach in which nodes gossip events and the history of that gossip yields an order. Hedera is the public network most readers meet it through. The definition is about ordering events, not about a price.

See also: [Hedera](#hedera), [Consensus](#consensus), [Finality](#finality).

### HBAR

<a id="hbar"></a>

*The native token of the Hedera network.* Level: beginner.

HBAR pays for transactions and is used in staking under Hedera's rules. The network entry describes the consensus design. This line only identifies the token, without a view on price.

See also: [Hedera](#hedera), [Token](#token), [Gas](#gas).

### Hedera

<a id="hedera"></a>

*A public network that orders transactions with hashgraph consensus.* Level: intermediate.

Hedera uses a hashgraph consensus design rather than a single chain of proof-of-work blocks, and it is governed by a council structure you can read about in its own documents. HBAR is the token used for fees and network services. This entry is a definition.

See also: [HBAR](#hbar), [Hashgraph](#hashgraph), [Consensus](#consensus).

### Layer 1

<a id="layer-1"></a>

*A base blockchain that settles its own consensus.* Level: beginner.

A layer 1 is a chain that finalises transactions under its own consensus, such as Bitcoin, Ethereum, or Solana. Other layers may post proofs or data to it. The base chain's fees, finality, and culture of upgrades are part of anything built above it.

See also: [Layer 2](#layer-2), [Blockchain](#blockchain), [Finality](#finality).

### Layer 2

<a id="layer-2"></a>

*A system that executes elsewhere and settles back to a layer 1.* Level: intermediate.

A layer 2 processes transactions outside the base chain and relies on that chain for settlement or data, according to its design. Rollups are the common family. A layer 2 inherits the base chain and adds its own sequencer, bridge, and proof assumptions.

See also: [Layer 1](#layer-1), [Rollup](#rollup), [Sequencer](#sequencer).

### LINK

<a id="link"></a>

*The token associated with the Chainlink oracle network.* Level: beginner.

LINK is the token used in the Chainlink ecosystem under that project's rules. The token's role in paying or staking node operators depends on the current design, which you should read at the source. This is a definition, not a view on the price.

See also: [Chainlink](#chainlink), [Oracle](#oracle), [Token](#token).

### Litecoin

<a id="litecoin"></a>

*An early proof-of-work blockchain derived from Bitcoin's design.* Level: beginner.

Litecoin is a proof-of-work chain that launched as a faster-block, different-hash variant of Bitcoin's approach, and LTC is its native coin. It is a payments-oriented public ledger with its own miners and its own supply schedule. This is a definition, not a view on the price.

See also: [Bitcoin](#bitcoin), [Proof of Work](#proof-of-work), [LTC](#ltc).

### LTC

<a id="ltc"></a>

*The native coin of Litecoin.* Level: beginner.

LTC is the unit transferred and mined on Litecoin. Fees and block rewards on that chain are denominated in it. The sentence identifies the ticker, and it does not discuss a price.

See also: [Litecoin](#litecoin), [Coin](#coin), [Block Reward](#block-reward).

### Market Capitalisation

<a id="market-capitalisation"></a>

*Price multiplied by circulating supply.* Level: beginner.

Market capitalisation is the current price times the circulating supply a provider publishes. It is not cash in a treasury, and it is not the cost of buying every coin, because price would move long before that. Compare methods before you compare numbers across sites.

See also: [Circulating Supply](#circulating-supply), [Fully Diluted Valuation](#fully-diluted-valuation), [Liquidity](#liquidity).

### Max Supply

<a id="max-supply"></a>

*The ceiling on issuance, if the protocol has one.* Level: beginner.

Max supply is the most that can exist under the current rules, such as Bitcoin's fixed cap. Some tokens have no cap, or a cap that governance can change. Read the rule, not the slogan on a homepage.

See also: [Circulating Supply](#circulating-supply), [Total Supply](#total-supply), [Halving](#halving).

### Mempool

<a id="mempool"></a>

*The waiting room of transactions a node has seen but not yet included.* Level: intermediate.

The mempool is a node's set of pending transactions. Different nodes can see different sets. Transactions sitting there can be reordered or replaced under the fee rules, which is one reason order is part of execution risk.

See also: [Transaction](#transaction), [Gas](#gas), [MEV](#mev).

### Miner

<a id="miner"></a>

*A participant who performs proof-of-work hashing to propose blocks.* Level: beginner.

A miner assembles transactions and searches for a valid proof-of-work hash. Successful miners receive the block reward and the fees under that chain's rules. Mining is a business with energy cost and variance, and it is not described here as an opportunity.

See also: [Proof of Work](#proof-of-work), [Block Reward](#block-reward), [Hash](#hash).

### Network

<a id="network"></a>

*The specific chain a transaction will be sent on.* Level: beginner.

The network, or chain, is the ledger your wallet is talking to. An address you use on one network is not automatically a safe destination on another, even when the string looks familiar. Confirm the network in the wallet before you sign.

See also: [Wallet Address](#wallet-address), [Blockchain](#blockchain), [Bridge](#bridge).

### Node

<a id="node"></a>

*A computer that keeps and checks the ledger.* Level: beginner.

A node stores blockchain data and checks that new blocks follow the rules. Some nodes produce blocks, and many only verify. A wallet that trusts someone else's node is trusting that operator's view of the chain.

See also: [Blockchain](#blockchain), [Validator](#validator), [Consensus](#consensus).

### Nonce

<a id="nonce"></a>

*A counter that orders transactions from one account.* Level: intermediate.

On account-based chains, the nonce is a sequence number so each transaction from an address is applied in order and cannot be replayed. A stuck nonce blocks later transactions until it is cleared. The word also means other one-time numbers in cryptography, so read which nonce is meant.

See also: [Transaction](#transaction), [Account Model](#account-model), [Gas](#gas).

### Optimistic Rollup

<a id="optimistic-rollup"></a>

*A rollup that assumes batches are valid unless someone challenges them.* Level: advanced.

An optimistic rollup posts batches and allows a dispute window in which a challenger can prove a batch wrong. Withdrawals through the official path wait out that window. A faster exit through a third party adds that party's risk.

See also: [Rollup](#rollup), [Bridge](#bridge), [Finality](#finality).

### Proof of Stake

<a id="proof-of-stake"></a>

*A consensus rule that puts staked coins at risk for proposing blocks.* Level: beginner.

Proof of stake selects validators who lock the native coin as collateral, and it can penalise some failures by slashing that stake. Ethereum and many newer chains use variants of this idea. The details of selection, rewards, and penalties are chain-specific.

See also: [Validator](#validator), [Staking](#staking), [Slashing](#slashing).

### Proof of Work

<a id="proof-of-work"></a>

*A consensus rule that spends computation to propose blocks.* Level: beginner.

Proof of work requires miners to find a hash below a target, which costs energy and equipment, so rewriting history means redoing that work. Bitcoin uses this family of rule. The cost makes casual rewriting expensive, and it does not make a transaction instantly final.

See also: [Miner](#miner), [Bitcoin](#bitcoin), [Hash](#hash).

### Reorg

<a id="reorg"></a>

*A replacement of recent blocks by a competing history.* Level: advanced.

A reorganisation happens when the canonical chain switches, so recent blocks that you saw are no longer in the history. Transactions in the dropped blocks may return to the mempool or disappear. Deeper confirmation is the ordinary defence against a shallow reorg.

See also: [Finality](#finality), [Confirmation](#confirmation), [Proof of Work](#proof-of-work).

### Rollup

<a id="rollup"></a>

*A layer 2 that posts transaction data or proofs to a base chain.* Level: intermediate.

A rollup executes transactions away from the layer 1 and publishes enough data or proof that the base chain can secure the result under that rollup's rules. Optimistic and validity-proof designs differ in how they catch a bad state. The rollup's bridge is part of the risk, not a footnote.

See also: [Optimistic Rollup](#optimistic-rollup), [ZK Rollup](#zk-rollup), [Layer 2](#layer-2).

### Satoshi

<a id="satoshi"></a>

*The smallest usual unit of bitcoin.* Level: beginner.

A satoshi is one one-hundred-millionth of a bitcoin. Prices and fees are sometimes quoted in satoshis so small amounts are readable. It is a unit of BTC, not a separate coin.

See also: [Bitcoin](#bitcoin), [Base Asset](#base-asset), [Transaction](#transaction).

### Sequencer

<a id="sequencer"></a>

*The component that orders transactions on many layer 2s.* Level: advanced.

A sequencer decides the order of transactions before they are settled to the base chain. A single sequencer can halt or censor for a time, even when the base chain is fine. Ask whether users can force a transaction through the base chain if the sequencer is down.

See also: [Layer 2](#layer-2), [Rollup](#rollup), [MEV](#mev).

### Smart Contract

<a id="smart-contract"></a>

*A program stored on a chain that runs when a transaction calls it.* Level: beginner.

A smart contract is code and stored state on a blockchain. It does what its code says when it is called, including things the author did not intend if the code is wrong. The word contract does not mean a court will read it as a legal agreement.

See also: [Smart-contract Risk](#smart-contract-risk), [Transaction](#transaction), [DeFi](#defi).

### Solana

<a id="solana"></a>

*A layer-1 blockchain that uses proof of stake and aims at high throughput.* Level: beginner.

Solana is a public layer 1 whose native coin is SOL, with a design focused on parallel execution and short block times. Fees, outages, and client diversity are part of studying any high-throughput chain. A fuller primer sits on the Solana page, and this line is only the definition.

See also: [Layer 1](#layer-1), [Proof of Stake](#proof-of-stake), [Throughput](#throughput).

### Stablecoin

<a id="stablecoin"></a>

*A token designed to track a reference value, often one unit of fiat.* Level: beginner.

A stablecoin aims to stay near a reference, commonly one US dollar, using reserves, collateral, or another mechanism. The peg can slip. Holding several stablecoins is not diversification if they share an issuer, a banking rail, or the same liquidity pool.

See also: [Depeg](#depeg), [Fiat-backed Stablecoin](#fiat-backed-stablecoin), [Quote Asset](#quote-asset).

### Sui

<a id="sui"></a>

*A layer-1 blockchain with an object-based data model.* Level: beginner.

Sui is a proof-of-stake layer 1 that records objects rather than only account balances, and SUI is its native token. The object model changes how assets and parallel execution are described. This entry is a definition for the primer, not a view on the price.

See also: [Layer 1](#layer-1), [Proof of Stake](#proof-of-stake), [SUI](#sui-token).

### SUI

<a id="sui-token"></a>

*The native token of the Sui network.* Level: beginner.

SUI is the coin used for fees and staking on Sui. The network entry describes the chain, and this entry names the unit. Nothing here is a view on the price or an instruction to hold the coin.

See also: [Sui](#sui), [Coin](#coin), [Gas](#gas).

### Throughput

<a id="throughput"></a>

*How many transactions a network processes in a given time.* Level: intermediate.

Throughput is a count of transactions per second or per block, under a stated definition. Chains count different things, and a simple transfer is not the same work as a heavy contract call. Compare figures only when the definition matches.

See also: [Solana](#solana), [Gas](#gas), [Block](#block).

### Token

<a id="token"></a>

*A unit issued by a contract on an existing chain.* Level: beginner.

A token is an asset accounted for by a smart contract, such as a fungible token on a public chain. It depends on that contract and that chain. The native coin that pays fees is a related but separate idea.

See also: [Coin](#coin), [ERC-20](#erc-20), [Fake Token](#fake-token).

### Tokenomics

<a id="tokenomics"></a>

*The supply, distribution, and value-capture rules of a token.* Level: intermediate.

Tokenomics covers who receives new tokens, what is locked, what the token is used for, and whether use of the protocol directs value to it by a rule you can point at. A story about future demand is not a mechanism. The mechanism is the part you can read in the contract or the monetary policy.

See also: [Emission](#emission), [Unlock](#unlock), [Governance Token](#governance-token).

### Total Supply

<a id="total-supply"></a>

*The coins created so far, including those still locked.* Level: intermediate.

Total supply counts coins that exist, whether or not they are circulating. Locked team allocations sit in total supply and not always in circulating supply. Unlock schedules tell you when the gap between the two can close.

See also: [Circulating Supply](#circulating-supply), [Unlock](#unlock), [Vesting](#vesting).

### Transaction

<a id="transaction"></a>

*A signed instruction that changes ledger state.* Level: beginner.

A transaction is a signed message that transfers value or calls a contract, and it is broadcast for inclusion in a block. A failed transaction can still cost a fee, because the network did the work of rejecting it. Until it is included and settled under the chain's rule, it is not final.

See also: [Signature](#signature), [Gas](#gas), [Mempool](#mempool).

### Unlock

<a id="unlock"></a>

*The moment previously locked tokens become transferable.* Level: intermediate.

An unlock is a date or a condition when vested tokens can move. A large unlock increases the supply that can be sold. It does not require that the holders sell, and it does not forbid it, and the calendar is the fact, and the reaction is not.

See also: [Vesting](#vesting), [Circulating Supply](#circulating-supply), [Tokenomics](#tokenomics).

### UTXO

<a id="utxo"></a>

*An unspent output, the unit Bitcoin-style chains track.* Level: intermediate.

A UTXO is a chunk of coins created by a previous transaction and not yet spent. A payment consumes some outputs and creates new ones. This model is different from an account balance, and many on-chain metrics such as SOPR are built on it.

See also: [Account Model](#account-model), [Bitcoin](#bitcoin), [SOPR](#sopr).

### Validator

<a id="validator"></a>

*A participant who proposes or attests to blocks under proof of stake.* Level: beginner.

A validator locks stake and takes part in proposing or voting on blocks, under the chain's rules. Poor uptime or certain rule breaches can cost rewards or principal where slashing exists. Delegating to a validator does not remove the validator's operational risk.

See also: [Proof of Stake](#proof-of-stake), [Delegation](#delegation), [Slashing](#slashing).

### Vesting

<a id="vesting"></a>

*A schedule that releases allocated tokens over time.* Level: intermediate.

Vesting is the rule that gives a team, an investor, or a treasury its tokens gradually rather than on day one. Cliffs, linear release, and who can change the schedule are the details that matter. A schedule that an admin key can rewrite is not the same object as a schedule baked into an immutable contract.

See also: [Unlock](#unlock), [Emission](#emission), [Governance](#governance).

### Wallet

<a id="wallet"></a>

*Software or hardware that holds keys and asks a network to accept transactions.* Level: beginner.

A wallet stores keys, shows balances by querying a node or an indexer, and builds the transactions you sign. It does not contain the coins. The coins are entries on the ledger, and the wallet is how you authorise changes to those entries.

See also: [Private Key](#private-key), [Self-custody](#self-custody), [Hot Wallet](#hot-wallet).

### Wrapped Asset

<a id="wrapped-asset"></a>

*A token that stands in for an asset on another chain or in another format.* Level: intermediate.

A wrapped asset is a claim, issued by a bridge or a custodian, that represents something held elsewhere. The wrapper can fail even when the underlying asset is fine. Know who or what holds the original, and how redemption works.

See also: [Bridge](#bridge), [Custody](#custody), [Token](#token).

### XRP

<a id="xrp"></a>

*The native token of the XRP Ledger.* Level: beginner.

XRP is the asset used to pay fees and to bridge payments on the XRP Ledger. The ledger is a public payment network with its own validator consensus, distinct from proof of work. This entry defines the asset, and it is not a comment on any court case and not a view on the price.

See also: [XRP Ledger](#xrp-ledger), [Token](#token), [Transaction](#transaction).

### XRP Ledger

<a id="xrp-ledger"></a>

*A public ledger designed for payments, with XRP as its native asset.* Level: intermediate.

The XRP Ledger settles transfers under a consensus protocol among validators, and it has built-in features such as a decentralised exchange order book at the protocol layer. Fees are paid by destroying a tiny amount of XRP. Study the current validator list and the fee rule at the source if you need more than this definition.

See also: [XRP](#xrp), [Consensus](#consensus), [Order Book](#order-book).

### ZK Rollup

<a id="zk-rollup"></a>

*A rollup that posts a validity proof of its state change.* Level: advanced.

A validity-proof rollup, often called a ZK rollup, attaches a cryptographic proof that the new state follows from the old one under its rules. There is no dispute window of the optimistic kind. The proof system, the prover, and the data you need to exit are still part of the design.

See also: [Rollup](#rollup), [Optimistic Rollup](#optimistic-rollup), [Finality](#finality).

## DeFi

<a id="defi"></a>

### Aggregator

<a id="aggregator"></a>

*A router that splits a swap across several pools or venues.* Level: intermediate.

An aggregator searches routes and can split one trade across pools to reduce price impact under its model. The route adds more contracts and more chances to fail. A quoted route is an estimate until the transaction lands.

See also: [AMM](#amm), [Price Impact](#price-impact), [Slippage Tolerance](#slippage-tolerance).

### Airdrop

<a id="airdrop"></a>

*A distribution of tokens to addresses that meet published conditions.* Level: intermediate.

An airdrop sends a new or existing token to wallets that did something the project counted, often based on a snapshot. The claim page is a favourite phishing surface. Verify the contract and the domain from a source you already had, and treat the token's future as unknown.

See also: [Phishing](#phishing), [Snapshot](#snapshot), [Points Programme](#points-programme).

### AMM

<a id="amm"></a>

*An automated market maker that quotes a price from a pool's reserves.* Level: beginner.

An automated market maker replaces the order book with a formula over tokens locked in a pool. Traders swap against the pool, and the formula moves the price. Liquidity providers take the other side of that inventory change.

See also: [Constant Product](#constant-product), [AMM Pool](#amm-pool), [Decentralised Exchange](#decentralised-exchange).

### AMM Pool

<a id="amm-pool"></a>

*The pair of token reserves that an automated market maker trades against.* Level: beginner.

An AMM pool is the contract that holds the reserves and executes the pricing formula. This is the DeFi object. In the structure lessons the phrase liquidity pool means a cluster of resting orders on a chart, which is a different thing.

See also: [AMM](#amm), [Liquidity Provider](#liquidity-provider), [Liquidity Pool](#liquidity-pool).

### APR

<a id="apr"></a>

*A quoted rate over a year, without assuming the rate is reinvested.* Level: beginner.

APR states a rate on a yearly basis without compounding that rate inside the quote. Variable protocol rates change, so today's APR is today's setting, not a year-long contract. Read whether the figure includes incentive tokens.

See also: [APY](#apy), [Utilisation](#utilisation), [Emission](#emission).

### APY

<a id="apy"></a>

*A quoted rate over a year that assumes the rate is compounded.* Level: beginner.

APY restates a rate as if it were reinvested through the year. It is a quoting convention. It is not a promise of what you will receive, because the rate, the token price, and your ability to exit can all change.

See also: [APR](#apr), [Compounding](#compounding), [Yield Farming](#yield-farming).

### Bad Debt

<a id="bad-debt"></a>

*Borrowing that is no longer covered by collateral the protocol can seize.* Level: advanced.

Bad debt appears when collateral falls through the debt faster than liquidations repay it, or when the collateral cannot be sold. Suppliers then hold a pool that is worth less than the books suggested. It is a solvency problem for the protocol, not a personal score.

See also: [Liquidation](#liquidation), [Overcollateralisation](#overcollateralisation), [Lending Market](#lending-market).

### Collateral

<a id="collateral"></a>

*Assets locked to secure a borrow.* Level: beginner.

Collateral is what the protocol can sell if the loan is no longer safe under its rules. A volatile collateral needs a larger buffer than a stable one, because the same price move consumes more of the cushion. The protocol's list of accepted collateral is a risk decision, not a convenience list.

See also: [Lending Market](#lending-market), [Loan-to-value](#loan-to-value), [Liquidation](#liquidation).

### Composability

<a id="composability"></a>

*The ability of protocols to call each other as building blocks.* Level: intermediate.

Composability means one contract can use another's tokens or functions without asking a gatekeeper. The same property stacks dependencies, so a failure in a token, an oracle, or a bridge is inherited by everything that sits on top. If you cannot list the stack, you cannot list the risks.

See also: [DeFi](#defi), [Smart Contract](#smart-contract), [Oracle](#oracle).

### Concentrated Liquidity

<a id="concentrated-liquidity"></a>

*Liquidity posted only inside a chosen price range.* Level: advanced.

Concentrated liquidity lets a provider put capital into a band instead of across every possible price. Inside the band the same capital supports more volume, and outside the band the position can sit entirely in one asset and stop earning swap fees. The band is a decision you have to tend.

See also: [Liquidity Provider](#liquidity-provider), [Range](#range), [Impermanent Loss](#impermanent-loss).

### Constant Product

<a id="constant-product"></a>

*A pool rule that keeps the product of the two reserves steady, before fees.* Level: intermediate.

A constant-product pool maintains the product of its two reserves, often written as x times y equals k, ignoring fees for the core idea. Selling one asset into the pool makes it scarcer and raises its price. The quoted price is the ratio of the reserves.

See also: [AMM](#amm), [AMM Pool](#amm-pool), [Price Impact](#price-impact).

### DAO

<a id="dao"></a>

*An organisation whose decisions are executed by token votes and contracts.* Level: intermediate.

A decentralised autonomous organisation holds assets and changes parameters through proposals and votes defined in its contracts. Turnout, delegation, and any remaining admin key decide how decentralised the practice really is. The label on the website is not the control structure.

See also: [Governance](#governance), [Governance Token](#governance-token), [Timelock](#timelock).

### DeFi

<a id="defi"></a>

*Financial protocols that run as smart contracts on public chains.* Level: beginner.

Decentralised finance is the set of lending, trading, and issuance programs that settle on a public ledger rather than on a firm's private books. You keep the keys, and you take smart-contract, oracle, and operational risk in exchange. The category name is not a quality rating.

See also: [Smart Contract](#smart-contract), [Wallet](#wallet), [Composability](#composability).

### Delegation

<a id="delegation"></a>

*Assigning your stake, or your votes, to someone who acts for you.* Level: intermediate.

Delegation lets a holder point stake at a validator, or voting power at a delegate, without running the operation. You still carry the validator's slashing and downtime where the protocol says so. Choosing a delegate is a risk decision about that operator.

See also: [Staking](#staking), [Validator](#validator), [Governance](#governance).

### ERC-20

<a id="erc-20"></a>

*The common standard for interchangeable tokens on Ethereum-style chains.* Level: beginner.

ERC-20 is an interface for a fungible token: transfer, balance, and approval functions that wallets expect. A token can implement the interface and still be malicious. The standard tells you how it talks, not whether the issuer is honest.

See also: [Token](#token), [Token Approval](#token-approval), [Fake Token](#fake-token).

### Flash Loan

<a id="flash-loan"></a>

*A loan that must be repaid inside the same transaction.* Level: advanced.

A flash loan is borrowed and repaid before the transaction ends, and the whole transaction reverts if repayment fails. It lets a sequence of actions run without starting capital. Weak contracts have been drained with that pattern, so this entry stops at the definition and does not describe an attack.

See also: [Lending Market](#lending-market), [Transaction](#transaction), [Smart-contract Risk](#smart-contract-risk).

### Governance

<a id="governance"></a>

*The process that changes a protocol's parameters or code.* Level: intermediate.

Governance is who may propose, who may vote, how long a change waits, and who can still act in an emergency. A timelock gives observers time to react. A multisig that can skip the vote is a different, faster power, and it belongs in the risk notes.

See also: [DAO](#dao), [Timelock](#timelock), [Multisig](#multisig).

### Health Factor

<a id="health-factor"></a>

*A protocol-specific score of how far a borrow sits from liquidation.* Level: intermediate.

Health factor is a single number some lending protocols publish to summarise collateral against the liquidation threshold. A higher score means more distance under that protocol's formula, and the formula is not the same everywhere. Treat the threshold as a cliff, not as a target to lean on.

See also: [Loan-to-value](#loan-to-value), [Liquidation Threshold](#liquidation-threshold), [Liquidation](#liquidation).

### Impermanent Loss

<a id="impermanent-loss"></a>

*How far a pool position lags simply holding the same coins.* Level: intermediate.

Impermanent loss is the gap between the value of a liquidity position and the value of having held the original coins, caused by a change in relative price. Fees can narrow the gap and do not erase it. Withdrawing turns today's mix into the result you actually keep.

See also: [Liquidity Provider](#liquidity-provider), [AMM](#amm), [Divergence](#divergence).

### Lending Market

<a id="lending-market"></a>

*A pool that accepts deposits and lends them against collateral.* Level: beginner.

A lending market lets suppliers deposit an asset and lets borrowers take it out after posting collateral the protocol accepts. Interest usually depends on how much of the pool is borrowed. You depend on the collateral rules, the oracle, and the contract.

See also: [Collateral](#collateral), [Utilisation](#utilisation), [Health Factor](#health-factor).

### Liquid Staking

<a id="liquid-staking"></a>

*Staking that gives you a token representing the staked position.* Level: intermediate.

Liquid staking deposits the native coin with a protocol and returns a liquid staking token you can transfer or use elsewhere. The underlying stays staked. You now have the staking risks plus the token's own contract and market price.

See also: [Liquid Staking Token](#liquid-staking-token), [Staking](#staking), [Depeg](#depeg).

### Liquid Staking Token

<a id="liquid-staking-token"></a>

*A token that tracks a claim on staked coins and their rewards.* Level: intermediate.

A liquid staking token represents a share of staked assets. Its price can drift from the value of the underlying if the market or the redemption path is stressed. Using it as collateral stacks that drift on top of ordinary liquidation risk.

See also: [Liquid Staking](#liquid-staking), [Wrapped Asset](#wrapped-asset), [Collateral](#collateral).

### Liquidation Threshold

<a id="liquidation-threshold"></a>

*The collateral ratio at which a position may be liquidated.* Level: intermediate.

The liquidation threshold is the protocol's line where some or all of the collateral becomes eligible for liquidation. Operating near it means a small oracle move can end the position. A buffer is part of the plan, because the line is the protocol's rule and not a suggestion.

See also: [Health Factor](#health-factor), [Liquidation](#liquidation), [Oracle](#oracle).

### Liquidity Provider

<a id="liquidity-provider"></a>

*Someone who deposits assets into a pool so others can swap.* Level: beginner.

A liquidity provider locks assets in a pool and receives a claim on the pool, plus a share of fees under the protocol's rules. The asset mix changes as traders swap. Fees are compensation for that inventory risk, not a separate salary.

See also: [AMM Pool](#amm-pool), [Impermanent Loss](#impermanent-loss), [Inventory](#inventory).

### Loan-to-value

<a id="loan-to-value"></a>

*Debt divided by the value of the collateral.* Level: intermediate.

Loan-to-value is the size of what you owe divided by the protocol's value of what you posted. A higher ratio is closer to the liquidation rule. The value in the denominator is only as good as the oracle that reports it.

See also: [Collateral](#collateral), [Health Factor](#health-factor), [Oracle](#oracle).

### MEV

<a id="mev"></a>

*Value captured by choosing the order or inclusion of transactions.* Level: advanced.

Maximal extractable value is profit available to whoever can order, insert, or censor transactions, for example by back-running a price gap between pools. Ordinary users feel it as a worse fill. Private routing and tighter slippage limits are the defences a reader actually controls.

See also: [Sandwich Attack](#sandwich-attack), [Mempool](#mempool), [Slippage Tolerance](#slippage-tolerance).

### NFT

<a id="nft"></a>

*A token that is unique or one of a distinct series.* Level: beginner.

A non-fungible token identifies a specific item, such as a position, a collectible, or a credential, rather than an interchangeable balance. Some liquidity positions are NFTs because each range is different. The token standard does not make the contents valuable.

See also: [ERC-20](#erc-20), [Token](#token), [Concentrated Liquidity](#concentrated-liquidity).

### Oracle

<a id="oracle"></a>

*A feed that brings an off-chain or cross-market fact into a contract.* Level: intermediate.

An oracle supplies a price or another fact that a contract cannot see by itself. Lending thresholds, liquidations, and some stablecoins depend on it. A stale, thin, or manipulated feed makes the contract act on the wrong world.

See also: [Chainlink](#chainlink), [TWAP](#twap), [Mark Price](#mark-price).

### Overcollateralisation

<a id="overcollateralisation"></a>

*Posting collateral worth more than the debt.* Level: intermediate.

Overcollateralisation means the protocol requires collateral value above the amount borrowed, so a price fall has room before liquidation. The buffer is only real if the collateral price and the oracle keep up. A design that looks overcollateralised on paper can still accrue bad debt in a gap.

See also: [Collateral](#collateral), [Bad Debt](#bad-debt), [Crypto-backed Stablecoin](#crypto-backed-stablecoin).

### Permissionless

<a id="permissionless"></a>

*A system anyone can use without an account-opening decision by a firm.* Level: beginner.

A permissionless protocol can be called by any wallet that pays the fee and follows the contract. Access is not the same as safety, and a front-end website can still block regions even when the contract does not. Jurisdiction and interface rules still apply to the person using it.

See also: [DeFi](#defi), [Smart Contract](#smart-contract), [KYC](#kyc).

### Points Programme

<a id="points-programme"></a>

*An off-chain or on-chain score that hints at a possible later reward.* Level: intermediate.

A points programme assigns a score for using a protocol and implies a future benefit without defining it. Points are not a token until a contract says they are. Spending fees to farm an undefined score is a cost you can measure against a reward you cannot yet.

See also: [Airdrop](#airdrop), [Yield Farming](#yield-farming), [Sybil](#sybil).

### Protocol Fee

<a id="protocol-fee"></a>

*A charge users pay for using a protocol.* Level: intermediate.

A protocol fee is what traders, borrowers, or other users pay, as written in the contracts. It is the raw takings before you ask who receives them. A fee that is then paid straight out as emissions is not the same as a fee that is kept.

See also: [Protocol Revenue](#protocol-revenue), [TVL](#tvl), [Yield Farming](#yield-farming).

### Protocol Revenue

<a id="protocol-revenue"></a>

*The portion of fees that the protocol, the treasury, or the token actually keeps.* Level: intermediate.

Protocol revenue is a defined share of fees after the method says what counts. Providers disagree on the definition, so name the source. Revenue is a flow, and a token does not receive it unless a rule you can point at directs it there.

See also: [Protocol Fee](#protocol-fee), [Tokenomics](#tokenomics), [TVL](#tvl).

### Proxy Contract

<a id="proxy-contract"></a>

*A contract address whose logic can be replaced by an upgrade.* Level: advanced.

A proxy keeps the user-facing address and the balances, and points at a separate implementation that an admin or a vote can change. Upgrades let bugs be fixed and let behaviour change after you have deposited. Know who can upgrade, and whether a timelock sits in front of them.

See also: [Smart Contract](#smart-contract), [Timelock](#timelock), [Governance](#governance).

### Rebasing Token

<a id="rebasing-token"></a>

*A token whose balance changes automatically under a protocol rule.* Level: advanced.

A rebasing token increases or decreases the balance in your wallet as the protocol distributes a change, rather than only moving the price. Accounting, taxes, and some contracts handle rebasing poorly. Read whether the reward is a rebase or a rising exchange rate before you integrate it.

See also: [Token](#token), [Receipt Token](#receipt-token), [Liquid Staking Token](#liquid-staking-token).

### Receipt Token

<a id="receipt-token"></a>

*A token that records your claim on a pool, a lend, or a vault.* Level: intermediate.

A receipt token, sometimes a share or a deposit token, is the accounting unit you receive when you deposit. Burning it is how you withdraw, under the protocol's rules. If the receipt is locked, paused, or mispriced, the deposit is not as liquid as the button suggested.

See also: [Vault](#vault), [Liquidity Provider](#liquidity-provider), [ERC-20](#erc-20).

### Reentrancy

<a id="reentrancy"></a>

*A bug where an outside call re-enters a contract before its books update.* Level: advanced.

Reentrancy happens when a contract calls out, and the callee calls back in, before balances have been updated. The impact can be a repeated withdrawal or broken accounting. This entry names the bug class only, and it does not include exploit steps.

See also: [Smart-contract Risk](#smart-contract-risk), [Smart Contract](#smart-contract), [Flash Loan](#flash-loan).

### Restaking

<a id="restaking"></a>

*Using staked assets as security for additional services.* Level: advanced.

Restaking takes coins that already secure a base chain and puts them to work securing other services, under extra slashing rules. Any extra reward is payment for those extra ways to lose the stake. One collateral base under many services can fail together.

See also: [Staking](#staking), [Slashing](#slashing), [Composability](#composability).

### Sandwich Attack

<a id="sandwich-attack"></a>

*A pair of trades wrapped around someone else's swap to harvest their price impact.* Level: advanced.

A sandwich places one trade before a victim's swap and another after it, so the victim trades at a worse price and the attacker keeps the difference. The impact grows with size and with loose slippage tolerance. This is a description of the harm, not a recipe.

See also: [MEV](#mev), [Slippage Tolerance](#slippage-tolerance), [Price Impact](#price-impact).

### Slashing

<a id="slashing"></a>

*A penalty that destroys part of a validator's stake.* Level: intermediate.

Slashing is a protocol penalty for defined misbehaviour, such as signing conflicting blocks, and on some networks for severe downtime. Delegators can lose alongside the validator. The conditions are in the chain's rules, and they are not the same on every proof-of-stake system.

See also: [Staking](#staking), [Validator](#validator), [Proof of Stake](#proof-of-stake).

### Smart-contract Risk

<a id="smart-contract-risk"></a>

*The chance that contract code or its economic design fails.* Level: intermediate.

Smart-contract risk covers bugs, unsafe permissions, upgrade surprises, and designs that behave badly when markets move. An audit reduces some uncertainty and does not erase it. If you cannot name the failure mode, you do not yet understand the position.

See also: [Smart Contract](#smart-contract), [Reentrancy](#reentrancy), [Proxy Contract](#proxy-contract).

### Snapshot

<a id="snapshot"></a>

*A recorded state of balances or actions at a chosen moment.* Level: intermediate.

A snapshot is a copy of who held what, or who had done what, at a block or a time. Airdrops and votes use snapshots so later transfers do not rewrite the record. The rules of what was counted matter more than the headline date.

See also: [Airdrop](#airdrop), [Governance](#governance), [Block](#block).

### Stable Swap

<a id="stable-swap"></a>

*A pool curve shaped for assets that should trade near one another.* Level: advanced.

A stable-swap curve flattens the price near one-to-one so similarly priced assets can trade with less slippage than a constant-product pool of the same size. The curve assumes the assets stay similar. A depeg breaks that assumption and the position can end up holding the weaker asset.

See also: [AMM](#amm), [Stablecoin](#stablecoin), [Depeg](#depeg).

### Staking

<a id="staking"></a>

*Locking the native coin so a validator can take part in consensus.* Level: beginner.

Staking posts the chain's coin under the protocol rules so a validator can propose or attest, and rewards follow those rules. Some networks slash stake for defined failures, and some impose an unbonding wait before you can transfer again. The reward is payment for that duty and that lockup, not a coupon detached from the coin's price.

See also: [Validator](#validator), [Slashing](#slashing), [Unbonding](#unbonding).

### Sybil

<a id="sybil"></a>

*Many addresses controlled by one actor to look like many users.* Level: advanced.

A Sybil strategy splits activity across addresses so a distribution or a vote treats one person as a crowd. Protocols try to filter clusters, and those filters can be wrong in both directions. Address count is not a count of people.

See also: [Airdrop](#airdrop), [Active Addresses](#active-addresses), [Wallet Address](#wallet-address).

### Timelock

<a id="timelock"></a>

*A required delay between approving a change and executing it.* Level: advanced.

A timelock queues a governance action so it cannot take effect until a waiting period ends. The delay is useful only if someone is watching and users can exit in time. A short delay, or a role that can bypass it, is a weaker control.

See also: [Governance](#governance), [DAO](#dao), [Proxy Contract](#proxy-contract).

### TVL

<a id="tvl"></a>

*Total value locked, the assets a method counts as deposited.* Level: beginner.

Total value locked is a provider's sum of assets sitting in a protocol, priced by that provider's method. Token prices move the number even when no one deposits or withdraws, and the same coins can be counted in more than one protocol. It is a size indicator, not a measure of safety or of revenue.

See also: [Protocol Revenue](#protocol-revenue), [Liquidity](#liquidity), [Oracle](#oracle).

### TWAP

<a id="twap"></a>

*A time-weighted average price over a window.* Level: advanced.

A time-weighted average price is the average of price over time, not weighted by volume, unless the implementation says otherwise. Oracles use it to blunt a one-block spike, and the cost is lag. A window that is slow to move is slow to tell the truth in a real crash as well.

See also: [Oracle](#oracle), [VWAP](#vwap), [Manipulation](#manipulation).

### Unbonding

<a id="unbonding"></a>

*The waiting period before staked coins can move again.* Level: intermediate.

Unbonding is the delay a protocol imposes between a request to leave staking and the coins becoming transferable. During the wait the coins may still be at risk and may not be available to sell or to post as collateral. The length of the wait is a parameter you read before you stake, not after you need the coins.

See also: [Staking](#staking), [Liquidity](#liquidity), [Validator](#validator).

### Utilisation

<a id="utilisation"></a>

*The share of a lending pool that is currently borrowed.* Level: intermediate.

Utilisation is borrowed amount divided by supplied amount. Many protocols raise the borrow rate sharply as utilisation gets high, so suppliers are paid to stay and borrowers are nudged to repay. High utilisation can also mean you cannot withdraw when you want to.

See also: [Lending Market](#lending-market), [APR](#apr), [Liquidity](#liquidity).

### Vault

<a id="vault"></a>

*A contract that pools deposits and runs a strategy for the depositors.* Level: intermediate.

A vault accepts deposits, issues shares, and deploys the assets according to a strategy, sometimes harvesting and reinvesting rewards. You take the vault's code risk and every protocol the strategy touches. The share price is a claim on the vault's assets, only as sound as that strategy.

See also: [Receipt Token](#receipt-token), [Yield Farming](#yield-farming), [Smart-contract Risk](#smart-contract-risk).

### Yield Farming

<a id="yield-farming"></a>

*Moving assets to collect fees and incentive tokens.* Level: intermediate.

Yield farming is the practice of depositing into pools or lenders to receive fees, interest, or extra tokens. Separate the part that comes from actual use of the protocol from the part that is new token emissions. Emissions can fall in price and can end on a date.

See also: [Emission](#emission), [APR](#apr), [Liquidity Provider](#liquidity-provider).

## On-chain data

<a id="on-chain"></a>

### Active Addresses

<a id="active-addresses"></a>

*How many addresses sent or received in a window.* Level: beginner.

Active addresses count addresses that appeared in transactions during the period. The count is not a count of people, because one person can use many addresses and a venue can batch many people into one. Bots and airdrop farming move the number.

See also: [Sybil](#sybil), [On-chain](#on-chain), [Throughput](#throughput).

### Block Explorer

<a id="block-explorer"></a>

*A website that reads a chain and shows transactions, addresses, and contracts.* Level: beginner.

A block explorer lets you inspect a transaction's status, the tokens moved, the logs, and the contract that was called. Use it to confirm what a wallet actually did, rather than what a front end claimed. Explorers can label addresses wrongly, so a label is a hint.

See also: [Transaction](#transaction), [Event Log](#event-log), [Allowance](#allowance).

### Event Log

<a id="event-log"></a>

*A structured note a contract emits while it executes.* Level: intermediate.

An event log is data a contract writes for observers, such as a token transfer, and explorers display those logs. A transfer you care about may be a log rather than a native-coin movement. Logs are only as honest as the contract that emitted them.

See also: [Block Explorer](#block-explorer), [Smart Contract](#smart-contract), [Transaction](#transaction).

### Exchange Netflow

<a id="exchange-netflow"></a>

*Coins sent to known venue addresses minus coins sent out, over a window.* Level: intermediate.

Exchange netflow subtracts outflows from inflows for addresses a data firm labels as venues. Labels can be wrong, and internal shuffles look like flow. A positive netflow is not proof that holders are selling, and it is a clue that needs a second source.

See also: [Whale](#whale), [On-chain](#on-chain), [Custody](#custody).

### HODL Waves

<a id="hodl-waves"></a>

*A chart of supply split by how long each coin has stayed unmoved.* Level: advanced.

HODL waves group supply into age bands based on when coins last moved, on a UTXO chain. Older bands growing means more supply has been idle. Idle is not the same as lost, and a move of old coins is activity, not automatically a sale on a venue.

See also: [Realised Cap](#realised-cap), [UTXO](#utxo), [Circulating Supply](#circulating-supply).

### Holder Concentration

<a id="holder-concentration"></a>

*How much of the supply sits in the largest addresses.* Level: intermediate.

Holder concentration is the share held by the top addresses after you try to separate contracts and venue wallets. High concentration means a few holders can move the market or the vote. The figure is only as good as the clustering behind it.

See also: [Whale](#whale), [Circulating Supply](#circulating-supply), [Governance](#governance).

### Manipulation

<a id="manipulation"></a>

*Trading or reporting that pushes a price or a metric away from an honest read.* Level: advanced.

Manipulation, in this library, means conduct that deliberately moves a printed price, an oracle, or a volume figure so other people rely on a distorted number. Thin books are easier to push. This entry names the risk, and it does not describe how to do it.

See also: [Oracle](#oracle), [TWAP](#twap), [Liquidity](#liquidity).

### MVRV

<a id="mvrv"></a>

*Market value divided by a realised-value measure of the same supply.* Level: advanced.

MVRV compares the market capitalisation with a realised capitalisation that prices coins near where they last moved, under a published method. Providers do not all compute it the same way. It is a lens on aggregate cost basis, not a signal to act.

See also: [Realised Cap](#realised-cap), [Market Capitalisation](#market-capitalisation), [SOPR](#sopr).

### Off-chain

<a id="off-chain"></a>

*Information or an agreement that is not settled on the public ledger.* Level: beginner.

Off-chain means the fact lives in a database, a legal agreement, or a conversation rather than in the block. Points, some order books, and reserve attestations are off-chain until a transaction records them. Treat off-chain claims as claims, and look for the attestation or the legal document.

See also: [On-chain](#on-chain), [Oracle](#oracle), [Points Programme](#points-programme).

### On-chain

<a id="on-chain"></a>

*Recorded on the public ledger and checkable by anyone running a node.* Level: beginner.

On-chain data is what the ledger itself stores: transactions, balances, and contract state. It shows movements. It does not, by itself, show who owns an address or why they moved funds.

See also: [Block Explorer](#block-explorer), [Transaction](#transaction), [Off-chain](#off-chain).

### Realised Cap

<a id="realised-cap"></a>

*A supply value that prices each coin near the price when it last moved.* Level: advanced.

Realised capitalisation adds up coins at the price associated with their last movement, instead of at today's price. It is an estimate of aggregate cost basis for a UTXO chain under that method. It is not the amount of cash investors have stored.

See also: [MVRV](#mvrv), [UTXO](#utxo), [Market Capitalisation](#market-capitalisation).

### SOPR

<a id="sopr"></a>

*Spent output profit ratio, a UTXO measure of whether moved coins are above their prior reference.* Level: advanced.

SOPR compares the value of coins when they are spent with the value when they last moved. A reading above one means that, in aggregate, those moved coins left a higher price than their prior reference. It describes coins that moved, not every holder, and it belongs to UTXO accounting.

See also: [UTXO](#utxo), [Realised Cap](#realised-cap), [MVRV](#mvrv).

### Whale

<a id="whale"></a>

*An address or a cluster that holds a large share of an asset.* Level: beginner.

A whale is a large holder, as a data firm defines large. One entity can use many addresses, and a labelled exchange wallet is not a person. Copying a whale's transfers ignores their hedges, their size, and their reasons.

See also: [Exchange Netflow](#exchange-netflow), [Holder Concentration](#holder-concentration), [On-chain](#on-chain).

## Portfolio

<a id="portfolio"></a>

### Concentration

<a id="concentration"></a>

*A large share of risk sitting in one asset, one venue, or one idea.* Level: beginner.

Concentration means one failure can do disproportionate damage, whether that is one coin, one protocol, or one correlated cluster. It is sometimes a deliberate choice. It should be a choice you can name, not an accident of adding similar positions.

See also: [Diversification](#diversification), [Exposure](#exposure), [Risk Budget](#risk-budget).

### Correlation

<a id="correlation"></a>

*How similarly two series move together.* Level: intermediate.

Correlation measures whether two prices, or two strategies, have tended to rise and fall at the same time. A high correlation means a loss in one often arrives with a loss in the other. Correlations change across regimes, so a long history average can hide the window that matters.

See also: [Diversification](#diversification), [Concentration](#concentration), [Market Regime](#market-regime).

### Diversification

<a id="diversification"></a>

*Spreading exposure across risks that do not all fail the same way.* Level: beginner.

Diversification is holding risks that are not the same bet in disguise. Several coins that all follow one market, or several grids on the same pair, are concentration. The test is what happens to the book in one bad day, not how many tickers are on the page.

See also: [Correlation](#correlation), [Concentration](#concentration), [Risk Budget](#risk-budget).

### Exposure

<a id="exposure"></a>

*How much of an asset or a factor the account actually holds.* Level: beginner.

Exposure is the economic bet, long or short, after you net related positions. Notional can overstate it when hedges offset, and it can understate it when leverage is hidden in a vault or a loop. Write the exposure in the asset you can lose.

See also: [Notional](#notional), [Hedge](#hedge), [Leverage](#leverage).

### Portfolio Heat

<a id="portfolio-heat"></a>

*The open risk currently in the account, added up.* Level: intermediate.

Portfolio heat is the sum of what you would lose if every open stop were hit, as a fraction of equity. It rises when you add positions and when stops are far. Check it before adding another idea, especially when the new idea moves with the ones you already have.

See also: [Risk Budget](#risk-budget), [Exposure](#exposure), [Correlation](#correlation).

## Research, testing, and journaling

<a id="research"></a>

### Backtest

<a id="backtest"></a>

*Running a written rule over past data to see what it would have done.* Level: intermediate.

A backtest applies rules you specified to historical prices and records the hypothetical results. It is only as honest as the fees, the slippage, and the fact that you did not reshape the rule after seeing the answer. Past paths are not a schedule for the future.

See also: [Overfitting](#overfitting), [Sample Size](#sample-size), [Forward Test](#forward-test).

### Forward Test

<a id="forward-test"></a>

*Running a frozen rule on data, or on paper, after the rule was locked.* Level: intermediate.

A forward test judges a rule on a period that was not used to design it. Paper trading is one way to do that. It still is not live trading, because fills and behaviour change when real size is on.

See also: [Backtest](#backtest), [Paper Trading](#paper-trading), [Sample Size](#sample-size).

### Journal

<a id="journal"></a>

*A record of what you did, why, and what the result was.* Level: beginner.

A journal stores the setup, the size, the stop, the result in R, and a note on whether you followed the plan. Without it, expectancy is a feeling. The point of the record is the review, not the decoration.

See also: [Trading Plan](#trading-plan), [Expectancy](#expectancy), [MAE](#mae).

### MAE

<a id="mae"></a>

*Maximum adverse excursion, the worst open loss during a trade.* Level: intermediate.

MAE is how far a trade moved against you before it closed, usually in R or in price. It shows whether your stop was inside the noise or far beyond where the trade actually went. Journal it so the stop rule can be reviewed against evidence.

See also: [MFE](#mfe), [Journal](#journal), [Stop Distance](#stop-distance).

### MFE

<a id="mfe"></a>

*Maximum favourable excursion, the best open gain during a trade.* Level: intermediate.

MFE is how far a trade moved in your favour before it closed. Compared with the result you actually kept, it shows what the management rule gave back. It is a review statistic, not a target to demand from the next trade.

See also: [MAE](#mae), [Journal](#journal), [Take Profit](#take-profit).

### Overfitting

<a id="overfitting"></a>

*A rule so tailored to past noise that it fails on new data.* Level: advanced.

Overfitting happens when you add parameters until the backtest looks excellent on the sample you tuned on. The fit describes that sample, including its accidents. A simpler rule that survives a forward test is stronger evidence than a busy rule that does not.

See also: [Backtest](#backtest), [Walk-forward](#walk-forward), [Sample Size](#sample-size).

### Paper Trading

<a id="paper-trading"></a>

*Following the plan with recorded hypothetical fills and no capital at risk.* Level: beginner.

Paper trading writes the orders down, or sends them to a simulator, without using funds. It practises the process and shows whether you can follow the rule. It does not reproduce slippage, emotion, or a full book of real fees.

See also: [Forward Test](#forward-test), [Trading Plan](#trading-plan), [Journal](#journal).

### Sample Size

<a id="sample-size"></a>

*How many observations sit behind a statistic.* Level: beginner.

Sample size is the count of trades, days, or events in the test. A win rate on a handful of trades swings wildly if you add or remove one result. Ask how many observations built the number before you treat it as stable.

See also: [Backtest](#backtest), [Expectancy](#expectancy), [Overfitting](#overfitting).

### Trading Plan

<a id="trading-plan"></a>

*A written set of conditions for entry, size, invalidation, and review.* Level: beginner.

A trading plan states what you would need to see, how large the position may be, where the idea is wrong, and when you will review. It is a document you can follow on a bad day. A plan that only describes the winning path is a wish.

See also: [Invalidation](#invalidation), [Position Sizing](#position-sizing), [Journal](#journal).

### Walk-forward

<a id="walk-forward"></a>

*A test that repeatedly tunes on one window and checks the next.* Level: advanced.

Walk-forward analysis chooses settings on a past window and then evaluates them on the following window, and it repeats that step through the history. It is a check on whether tuning was only memorising. It still uses history, so it is not a live result.

See also: [Overfitting](#overfitting), [Backtest](#backtest), [Forward Test](#forward-test).

## Automation

<a id="automation"></a>

### Alert

<a id="alert"></a>

*A message that fires when a price or a condition is met.* Level: beginner.

An alert tells you that a level or a rule has been touched so you can look. It is not an order unless you have separately built one. Alerts fail when the feed, the device, or the delivery channel fails, so a stop that matters belongs on the venue as well.

See also: [Trigger Price](#trigger-price), [Hard Stop](#hard-stop), [Automation](#automation).

### Automation

<a id="automation"></a>

*Letting software apply a rule you have already written.* Level: beginner.

Automation executes a defined rule, such as a grid or an alert, without you clicking each order. It removes hesitation and it also removes the pause in which you might have noticed a broken feed. The rule, the permissions, and the monitoring are the work.

See also: [Trading Bot](#trading-bot), [Alert](#alert), [Trading Plan](#trading-plan).

### Trading Bot

<a id="trading-bot"></a>

*Software that sends orders when written conditions are true.* Level: beginner.

A trading bot watches inputs and places the orders its code allows. It does the same wrong thing quickly if the rule or the key permissions are wrong. Give it no withdrawal permission, and keep a human review on the account.

See also: [API Key](#api-key), [Automation](#automation), [Grid](#grid).

## Psychology

<a id="psychology"></a>

### Confirmation Bias

<a id="confirmation-bias"></a>

*Noticing the evidence that agrees with the view you already hold.* Level: intermediate.

Confirmation bias is the habit of seeking charts and comments that support the idea you want, and of skipping the swing that contradicts it. A journal column for the case against the trade is a practical counter. The bias does not vanish because you have heard its name.

See also: [Trading Plan](#trading-plan), [Journal](#journal), [Process](#process).

### FOMO

<a id="fomo"></a>

*Fear of missing out, the urge to chase a move already underway.* Level: beginner.

FOMO is the pull to enter because price has already run and other people seem to be in. It skips the invalidation and the size rule. Naming it in the journal is more useful than pretending the chase was a setup.

See also: [Trading Plan](#trading-plan), [Revenge Trading](#revenge-trading), [Journal](#journal).

### Loss Aversion

<a id="loss-aversion"></a>

*Feeling a loss more strongly than a gain of the same size.* Level: intermediate.

Loss aversion is the tendency to hate a loss more than you enjoy an equal gain, which shows up as moving stops wider and cutting winners early. The R record makes the asymmetry visible. Awareness is not the same as a rule that blocks the click.

See also: [R Multiple](#r-multiple), [Stop Loss](#stop-loss), [Journal](#journal).

### Process

<a id="process"></a>

*The repeatable steps you follow, scored separately from the result.* Level: beginner.

Process is the checklist of plan, size, order type, and review, which you can mark as followed or not. A good process can lose on a single trade, and a broken process can win. Scoring only the profit teaches the wrong lesson.

See also: [Trading Plan](#trading-plan), [Journal](#journal), [Expectancy](#expectancy).

### Revenge Trading

<a id="revenge-trading"></a>

*A new trade taken to get back a loss, rather than because the plan allows it.* Level: beginner.

Revenge trading raises size or ignores the setup because the last result hurt. The market does not owe the loss back. A written cooldown after a loss is a process control, not a personality judgement.

See also: [FOMO](#fomo), [Trading Plan](#trading-plan), [Loss Aversion](#loss-aversion).

## Macro and cross-market context

<a id="macro"></a>

### Correlation Regime

<a id="correlation-regime"></a>

*A period in which assets move together more, or less, than usual.* Level: advanced.

A correlation regime is a stretch of time when the historical relationship between two markets is stable enough to describe. Stress often pushes correlations up. A hedge sized on a calm correlation can fail in the window you needed it.

See also: [Correlation](#correlation), [Hedge](#hedge), [Market Regime](#market-regime).

### CPI

<a id="cpi"></a>

*A consumer price index, a published measure of consumer inflation.* Level: beginner.

CPI is a statistical agency's index of consumer prices, and markets react to the print versus what was expected. The index is a measurement with a method, not a trade instruction. Know which country's index and which release you mean.

See also: [Interest Rate](#interest-rate), [Risk-on](#risk-on), [Macro](#macro).

### DXY

<a id="dxy"></a>

*A widely quoted index of the US dollar against a basket of currencies.* Level: intermediate.

DXY is an index of the dollar versus a set of other fiat currencies, with weights fixed by its publisher. A rising index means that basket is weaker against the dollar. Crypto's link to the index is a correlation you measure, not a mechanical rule.

See also: [Correlation](#correlation), [Risk-off](#risk-off), [Macro](#macro).

### ETF

<a id="etf"></a>

*An exchange-traded fund, a listed vehicle that holds a basket or a commodity-like asset.* Level: intermediate.

An ETF is a fund whose shares trade on a securities exchange, and some ETFs hold bitcoin or ether through a custodian. Creations and redemptions change the shares outstanding, which is why flow figures are studied. The fund is not the coin, and the custodian is a counterparty.

See also: [Custody](#custody), [Bitcoin](#bitcoin), [ETF Flow](#etf-flow).

### ETF Flow

<a id="etf-flow"></a>

*The net creation or redemption of shares in a crypto-linked fund.* Level: advanced.

ETF flow is the net amount of new shares created minus shares redeemed over a window, often restated in the underlying coin. A creation is demand for the share, which the fund structure may meet by buying the coin, depending on the product. Read the issuer's method before you treat a headline flow as spot buying.

See also: [ETF](#etf), [Bitcoin](#bitcoin), [Liquidity](#liquidity).

### Interest Rate

<a id="interest-rate"></a>

*The price of borrowing money, set in markets and influenced by policy.* Level: beginner.

An interest rate is what a borrower pays a lender for a period, in a given currency. Policy rates from central banks influence the curve, and crypto funding is a different rate with a different job. Do not treat a funding rate and a cash rate as the same object.

See also: [Yield Curve](#yield-curve), [Funding Rate](#funding-rate), [CPI](#cpi).

### Macro

<a id="macro"></a>

*The economy-wide backdrop: rates, inflation, growth, and the dollar.* Level: beginner.

Macro, in this library, means the cross-market context of policy rates, inflation prints, growth data, and the dollar. It sits behind risk appetite. It does not replace a read of the coin's own structure and liquidity.

See also: [CPI](#cpi), [Interest Rate](#interest-rate), [DXY](#dxy).

### Risk-off

<a id="risk-off"></a>

*A mood in which investors prefer safer holdings and sell riskier ones.* Level: beginner.

Risk-off describes a cross-market move toward cash and government bonds and away from assets seen as risky. Correlations that looked low in calm periods often rise on these days. A label is not a timing tool.

See also: [Risk-on](#risk-on), [Correlation](#correlation), [Drawdown](#drawdown).

### Risk-on

<a id="risk-on"></a>

*A mood in which investors prefer riskier assets.* Level: beginner.

Risk-on is a label for sessions when equities and other risky assets are bid together and safer holdings are sold. It is a description of cross-market behaviour, often after the fact. Crypto can join that move and can also ignore it.

See also: [Risk-off](#risk-off), [Correlation](#correlation), [CPI](#cpi).

### Yield Curve

<a id="yield-curve"></a>

*Interest rates plotted across different lending periods.* Level: intermediate.

The yield curve shows the rate for short periods beside the rate for long periods in one currency. A shift changes the discount people apply to future cash and the cost of funding. It is context for risk appetite, not a crypto entry signal.

See also: [Interest Rate](#interest-rate), [Risk-on](#risk-on), [Basis](#basis).
