---
title: Exchanges and orders
slug: exchanges
level: beginner
category: execution
related:
  - security
  - crypto-fundamentals
  - glossary
last_reviewed: 2026-11-10
status: draft
---

# Exchanges and orders

This page is general information about how venues and orders work. It does not name a venue, it does not rank venues, and it is not a recommendation to open an account or to trade. Consider your own circumstances. Short definitions live in the [glossary](glossary.md#order-book).

## Centralised and decentralised venues

A **centralised exchange** is a company that holds customer accounts, custodies assets, and matches orders on its own systems. Your balance there is a claim on that company. If the company fails, freezes withdrawals, or is compromised, the claim can fail even though the blockchain itself is fine.

A **decentralised exchange** settles through contracts you sign from your own wallet. There is no account in the ordinary sense. The risks move: smart-contract bugs, a bad route, a thin pool, and a signature you did not intend. Keeping the keys does not remove those risks.

Neither structure is "the safe one". One concentrates custody in a firm. The other concentrates responsibility in the signature and the contract. Atlas explains the types. It does not send you to a named venue.

## The order book, the spread, and depth

An **order book** is the list of resting bids and asks. A **bid** is a price someone will pay. An **ask** is a price someone will sell at. The **spread** is the best ask minus the best bid. The **mid** is halfway between them, and it is a reference, not a price you can assume you will receive in size.

**Depth** is how much size sits at and near those prices. A market order walks that depth. The further it walks, the worse the average fill. That gap is **price impact**. A screenshot of depth is a moment. The size can disappear when your order arrives.

## Maker and taker

A **maker** adds a resting order that someone else later trades against. A **taker** removes a resting order. Market orders are takers. A limit that is already marketable when it arrives is also a taker, whatever you hoped.

Venues publish a fee schedule for each role. The schedule depends on the venue and often on a volume tier. A grid that fires many small cycles can hand a large share of each step to fees. Compare the planned step with the fee and with a realistic slippage allowance before you call the step viable. That comparison is arithmetic, not a promise that the cycles will occur.

## Order types

These are the common instructions. Names differ slightly by venue. Read the venue's own specification before you rely on a label.

- **Market.** Take the best prices available now. You get speed. You give up a ceiling on the fill.
- **Limit.** Trade only at your price or better. The order may rest, or it may fill at once if the book is already through it. A limit that never trades has protected the price and has not made the trade.
- **Stop.** Wait until a trigger prints, then become a market order or a limit order, depending on the variant. The trigger is not the fill.
- **Stop-limit.** After the trigger, rest as a limit. In a fast move it can fail to fill. Use it only when a missed fill is more acceptable to the plan than an open-ended fill.
- **Trailing stop.** The trigger ratchets as price moves in your favour, by a distance or a rule you set. A tight trail exits on ordinary noise.
- **Post-only.** Rest as a maker, or cancel if the order would take liquidity. It is how a grid tries to stay on the maker schedule.
- **Reduce-only.** May only shrink an open position. It does not promise a fill. It only blocks an accidental increase.
- **Iceberg.** Shows a slice and reloads until a hidden total is done, on venues that offer it. The visible book then understates that order.
- **Fill or kill.** Fill the entire size immediately or cancel the whole order.
- **Immediate or cancel.** Fill what you can immediately and cancel the rest. A partial fill is allowed.
- **Good till cancelled.** Rest until a fill or a cancel, subject to the venue's own expiry. Some venues expire orders anyway. Check the next day.
- **One cancels the other.** Two linked orders, often a take-profit and a stop. A fill on one cancels the other. Confirm what a partial fill does. The link is only as good as the venue's implementation.
- **Conditional.** Held until a price, a time, or another event. It may live on the venue's servers rather than in the public book. If that path fails, the condition may not fire.

**Time in force** is the family name for fill-or-kill, immediate-or-cancel, and good-till-cancelled. **Tick size** is the smallest price step. **Lot size** is the smallest quantity step. A grid spaced inside the tick, or a size that is not a multiple of the lot, cannot be built as drawn.

## Registration in Australia, as general information

AUSTRAC, the Australian Transaction Reports and Analysis Centre, supervises businesses that provide certain services with virtual assets. For years those businesses were discussed as digital currency exchange providers. AUSTRAC's public material in 2026 uses the name **virtual asset service provider** (VASP) for the wider set of services, including exchanging virtual assets for money, exchanging virtual assets for other virtual assets, safekeeping, and passing on transfer instructions.

AUSTRAC states that a business must be registered before it provides those services in Australia, and that providing them without registration is an offence. Registration is a legal status. It is not a safety rating, not a promise about solvency, and not an endorsement of any firm. A name on the register means the business is on the register. It does not mean the business is suitable for you.

The public search is AUSTRAC's Virtual Asset Service Provider Register: [https://online.apps.austrac.gov.au/vaspr](https://online.apps.austrac.gov.au/vaspr). AUSTRAC's own overview of who is likely to be a VASP is here: [https://www.austrac.gov.au/industry-and-business/your-industry/virtual-asset-service-providers/virtual-asset-service-providers-overview](https://www.austrac.gov.au/industry-and-business/your-industry/virtual-asset-service-providers/virtual-asset-service-providers-overview).

This paragraph is general information about that framework. It is not advice about whether any reader's own activity must be registered. Atlas is an education library. It does not exchange assets, hold customer funds, or pass on transfer instructions, and it does not claim to be registered as a VASP.

Know-your-customer checks and anti-money-laundering controls are the ordinary companions of a registered account. They identify the customer and create reporting duties for the business. They are not a product feature to shop for, and this page does not tell you how to avoid them.
