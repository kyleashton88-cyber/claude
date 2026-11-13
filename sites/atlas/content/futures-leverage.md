---
title: Futures and leverage
slug: futures-leverage
level: intermediate
category: derivatives
related:
  - risk-academy
  - exchanges
  - automation
  - glossary
last_reviewed: 2026-11-10
status: draft
---

# Futures and leverage

A futures contract is an agreement whose value tracks an underlying asset. You can hold exposure to the price without holding the asset, and you can hold more exposure than the cash you post. That second feature is leverage. This page is general information about how the contracts work. It is not a recommendation to trade derivatives, it does not choose a leverage figure for you, and it is not personal advice. Leveraged products can lose more quickly than the same position held in spot. Consider your own circumstances.

Worked numbers below are invented so the arithmetic is visible. Each block is marked as a hypothetical example. Venues differ in contract specifications, so read the venue's own rules before you rely on a formula here. Position sizing and drawdown maths are on the [risk academy](risk-academy.md). Short definitions are in the [glossary](glossary.md#perpetual-future).

## Perpetuals and dated futures

A **dated future** has an [expiry](glossary.md#expiry). On that date it settles against a reference price, either in cash or by delivery of the asset. Before expiry its price can sit above or below spot. The gap is the [basis](glossary.md#basis).

A **perpetual future**, usually called a perp, has no expiry. To stop its price drifting far from spot forever, it uses a periodic payment between longs and shorts, the [funding rate](glossary.md#funding-rate), described below.

Contracts are also either **linear** or **inverse**. A [linear contract](glossary.md#linear-contract) is margined and settled in a quote currency, often a stablecoin, so profit and loss move in a straight line with price. An [inverse contract](glossary.md#inverse-contract) is margined in the coin itself. The coin you post as margin also falls when price falls, so a long loses on two fronts. Know which one you are looking at before you size anything.

## Notional, margin, and leverage

**Notional** is the full value of the position: contract size times price times quantity. **Margin** is the cash you post to hold it. **Leverage** is notional divided by the margin backing it.

```text
leverage = notional / margin
```

[Initial margin](glossary.md#initial-margin) is what you must post to open. [Maintenance margin](glossary.md#maintenance-margin) is the lower level you must keep to stay open. When equity in the position falls to maintenance, liquidation starts.

Leverage does not change how far price moves. It changes how much of your margin each move consumes. A one percent move in the underlying is roughly a ten percent move on margin at ten times leverage, before fees and funding.

Hypothetical example. A trader posts 500 quote units of margin and opens a long with a notional of 5000 quote units. Leverage is 5000 / 500 = 10. A 2 percent fall in price lowers the notional value by 100 quote units, which is 20 percent of the margin. Illustrative example on hypothetical data. Not a recommendation to trade this asset or these levels.

The useful habit is to size from risk first, using the [position-sizing formula](risk-academy.md#position-sizing), and then read the leverage that size implies. Choosing a leverage figure first and fitting the stop around it reverses the order.

## Mark price and last price

The [last price](glossary.md#last-price) is the most recent trade on that venue's contract. It can spike on one thin order. The [mark price](glossary.md#mark-price) is a smoothed reference that venues use to value positions and to trigger liquidations. It is usually built from an [index price](glossary.md#index-price) drawn from several spot sources, plus a basis or funding adjustment.

Because liquidations key off the mark, a wick on the last price does not always liquidate a position. The reverse also holds: a mark price can reach your liquidation level while the last price on your screen looks calmer. Read the venue's mark-price method, and set your stop on the price your venue uses for stops.

## Margin modes

**Isolated margin** ring-fences the margin for one position. If that position is liquidated, the loss is limited to the margin assigned to it, plus fees. Other balances are untouched.

**Cross margin** lets every position draw on the whole account balance. A losing position can survive longer because it borrows from the rest of the account. The cost is that one bad position can consume the balance meant for others. See [isolated margin](glossary.md#isolated-margin) and [cross margin](glossary.md#cross-margin).

Neither mode is safer in every case. Isolated margin makes each loss easier to see and cap. Cross margin can avoid an early liquidation and can also turn one mistake into an account-wide one. Write down which mode you are in before you open the position, because the default differs by venue.

## Liquidation

[Liquidation](glossary.md#liquidation) is the forced close of a position whose equity has fallen to maintenance margin. The venue closes it, usually at market, and may charge a liquidation fee. If the close fills worse than the bankruptcy price, an [insurance fund](glossary.md#insurance-fund) covers the gap. If that fund cannot, some venues use [auto-deleveraging](glossary.md#auto-deleveraging), which reduces profitable positions on the other side.

A simplified [liquidation price](glossary.md#liquidation-price) for an isolated linear long, ignoring fees and funding, is:

```text
liquidation price ≈ entry * (1 - 1/leverage + maintenance rate)
```

For a short, the signs flip:

```text
liquidation price ≈ entry * (1 + 1/leverage - maintenance rate)
```

The real level is closer to the entry than these forms suggest once fees, funding, and the venue's tiered maintenance rates are included. Use the venue's calculator for the live figure. Use the formula to understand why the distance shrinks as leverage rises.

Hypothetical example. An isolated linear long opens at 100 quote units with 10 times leverage and a maintenance rate of 0.5 percent. The approximate liquidation price is 100 * (1 - 0.1 + 0.005) = 90.5. A fall of about 9.5 percent from entry ends the position. At 20 times leverage the same formula gives 100 * (1 - 0.05 + 0.005) = 95.5, a fall of about 4.5 percent. Illustrative example on hypothetical data. Not a recommendation to trade this asset or these levels.

A liquidation price is not a stop. A stop is your invalidation, placed where the idea is wrong. If the liquidation price sits inside your stop, the venue will close you before your own plan does. The plan should place the stop well before liquidation, with room for slippage.

## Funding

The [funding rate](glossary.md#funding-rate) is a payment between longs and shorts on a perpetual, exchanged at a set [funding interval](glossary.md#funding-interval). Many venues use eight hours. Some use shorter intervals, and some change the interval in fast markets. When the perp trades above the index, funding is usually positive and longs pay shorts. When it trades below, shorts usually pay longs. The venue does not keep the payment. It passes between traders.

```text
funding payment ≈ position notional * funding rate
```

Funding is charged on notional, not on margin. At high leverage, a small rate is a large share of the margin over many intervals.

Hypothetical example. A long has a notional of 5000 quote units and the funding rate for one interval is 0.01 percent. The payment is 5000 * 0.0001 = 0.5 quote units. Across three intervals a day for thirty days, at the same rate, that is 45 quote units, which is 9 percent of a 500 quote unit margin. Illustrative example on hypothetical data. Not a recommendation to trade this asset or these levels.

Persistently high funding describes crowded positioning. It does not say when the crowd will leave. Read it as a cost and as context, not as a timing signal.

## Open interest

[Open interest](glossary.md#open-interest) is the number or value of contracts open at a moment. Each contract has a long and a short, so open interest counts positions, not one side's bet. Rising open interest means new positions are being opened. Falling open interest means positions are closing, by choice or by liquidation.

Open interest alongside price is context:

- Price and open interest rising together describe new exposure joining the move.
- Price falling sharply while open interest falls sharply often describes forced closing.
- Flat price with rising open interest describes positioning building without a move yet.

None of those lines tells you the next candle. Each describes the past interval on the venues that report it. Aggregated figures depend on which venues the data provider includes.

## Basis, contango, and backwardation

The basis is the futures price minus the spot price. When dated futures trade above spot, the curve is in [contango](glossary.md#contango). When they trade below, it is in [backwardation](glossary.md#backwardation). In traditional markets the gap often reflects interest rates and storage. In crypto it also reflects demand for leverage.

```text
annualised basis ≈ (futures - spot) / spot * (365 / days to expiry)
```

Hypothetical example. Spot is 100 and a future with 90 days to expiry is 101.5. The basis is 1.5, or 1.5 percent. Annualised, that is about 1.5 percent * 365 / 90 ≈ 6.1 percent. Illustrative example on hypothetical data. Not a recommendation to trade this asset or these levels.

A position that holds spot and shorts the future is called cash and carry. It is not without risk. It carries venue risk on both legs, margin calls on the short if price rises, funding or roll costs, and execution risk on entry and exit.

## Options, in brief

An option gives the holder the right, but not the obligation, to buy (a call) or sell (a put) at a set strike price before or at expiry. The buyer pays a premium. The buyer's loss is capped at the premium. The seller receives the premium and takes on the obligation, and a seller's loss can be large.

Option prices depend on the underlying price, the strike, time to expiry, interest rates, and the market's estimate of future volatility. That last input is called implied volatility, and it is not a forecast you can check in advance. Options are a separate module's worth of material. This section exists so the words are not new when you meet them. Atlas does not suggest any option position.

## Common mistakes

- Choosing leverage first and placing the stop wherever the leverage allows.
- Treating the liquidation price as a stop loss.
- Ignoring funding on a position held for weeks.
- Using cross margin without noticing that every balance in the account is now at risk.
- Comparing open interest across data sources that include different venues.
- Forgetting that an inverse contract's margin falls with the price.

## Where to practise

The leverage sandbox on the Atlas site lets you enter margin, leverage, and a maintenance rate to see the liquidation distance move. It runs on numbers you type. It is not a live account. Keep a record of any practice in the [journal](journal-lab.md), in R, so you can see what the plan did rather than what the leverage felt like.
