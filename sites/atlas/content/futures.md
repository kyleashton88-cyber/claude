---
title: Futures and leverage
slug: futures
level: intermediate
category: derivatives
related:
  - risk-academy
  - exchanges
  - glossary
last_reviewed: 2026-11-10
status: draft
---

# Futures and leverage

This page is general information about how perpetual and dated futures work, and about what leverage changes. It is not an instruction to open a position, and it does not name a venue. Order types live on the [exchanges page](exchanges.md). Sizing lives on the [risk page](risk-academy.md). Short definitions are in the [glossary](glossary.md#perpetual-future).

## What a futures contract is

A futures contract is an agreement whose value moves with an underlying price, settled in cash or by delivery under rules the venue publishes. You do not have to hold the coin to hold the exposure. You post **margin**, which is collateral, not a fee.

A **dated future** expires on a known timestamp and settles to a reference. As expiry nears, the contract price tends to converge toward that settlement. Rolling into a later contract replaces one basis with another.

A **perpetual future** has no expiry. **Funding** is the usual mechanism that tugs its price toward a spot index: a periodic payment between longs and shorts. One side pays and the other receives. The rate can flip. A quoted funding rate means little until you know the **funding interval**, because venues do not all use the same clock.

**Basis** is the gap between the derivative and the spot reference. State which way you subtract. A positive basis, derivative above spot, is not a view Atlas endorses. It is a price difference with a carrying cost.

## Leverage is a ratio, not a feature

Leverage is notional divided by the margin posted. Notional is price times size, the face value. Margin is the collateral the position can lose. A smaller margin against the same notional is higher leverage. It magnifies gains and losses, and it moves the liquidation price closer to the market.

Hypothetical example. A linear position with notional of 1000 quote units, posted with 100 quote units of margin, is ten times leverage, because 1000 divided by 100 is 10. A 10 percent adverse move in the underlying, with nothing else changing, wipes that 100 of margin. Illustrative example on hypothetical data. Not a recommendation to trade this asset or these levels.

The risk fraction that belongs in the account is still the cash you can lose, from the [position-sizing](risk-academy.md#position-sizing) formula. Meeting a venue's minimum margin is not that calculation.

## Margin modes and liquidation

**Initial margin** is what the venue requires to open. **Maintenance margin** is the floor below which liquidation can start. **Isolated margin** limits the collateral one position can consume to the amount you assigned. **Cross margin** lets positions share one pool, so a loser can draw on collateral you thought was spare.

**Liquidation** is a forced close when collateral no longer meets the venue's rule. The published liquidation price is an estimate. In a fast market the fill can be worse. An **insurance fund** is a buffer some venues keep for losses beyond a liquidated account. If that waterfall is not enough, **auto-deleveraging** can cut profitable positions on the other side, including a hedge you expected to stay open.

The price that matters is whichever price the venue uses for margin. **Mark price**, **index price**, and **last price** can differ. A stop watching the last trade, and a liquidation watching the mark, are two different triggers. Read which one your order uses.

**Open interest** is the stock of contracts still open. It rises when new positions are created and falls when they close. It is not a direction.

## Linear and inverse

A **linear** contract is margined and settled in the quote asset, often a stablecoin, so a one-unit price move has a stable quote value. An **inverse** contract is margined in the coin itself, and the coin result of a price move is not a straight line. Read the contract sheet before you treat the two as the same bet.

A **long** gains if the price rises and loses if it falls, before fees and funding. A **short** does the reverse. Losses on a short are not capped by the price falling toward zero in the way a long's price is. Neither word is an instruction.

## Funding is a cash flow to write down

On a perpetual, funding is a credit or a cost for as long as the position is open. A grid or a hedge that "collects funding" still has basis risk, liquidation risk, and the chance the rate flips. Delta-neutral, in the glossary sense, means a small price move changes the book very little. It does not mean the book is neutral to funding, fees, or a venue failure.

Hypothetical example. A made-up funding rate of 0.01 percent per interval, paid by longs to shorts, is 1 quote unit on 10000 quote units of notional for that interval only. The next interval can be zero or can reverse. Illustrative example on hypothetical data. Not a recommendation to trade this asset or these levels.

## What to write down before leverage is live

1. Notional, margin, and the leverage ratio those two imply.
2. Whether margin is isolated or cross.
3. Which price the liquidation and the stop actually watch.
4. The funding interval, and the cash effect at the current rate, labelled as today's reading.
5. The invalidation, in price or in a rule someone else could check.
6. What happens to the hedge if auto-deleveraging cuts one leg.

If one of those is missing, the missing piece is the plan. The [risk academy](risk-academy.md) is the arithmetic. This page is only the contract.
