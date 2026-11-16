# Elite Troubleshooting: Multi-Exchange and Multi-Layer Problems

> Education only, not financial advice.

**Fills gap:** troubleshooting at Elite level. Suggested place: Capital Scaling Strategies, after "Multi-Exchange Deployment".

## Balances don't add up across exchanges
- Pull each exchange's own statement. Don't rely on a dashboard alone.
- Check for funds sitting in funding wallets, sub-accounts or open orders.
- Check transfers in transit and the network used.

## A layer behaves differently on two exchanges
- Fees, minimum order size and tick size differ by venue. The same settings won't fill the same way.
- Liquidation rules and margin tiers differ too. Recheck liquidation distance per venue.

## Circuit breaker didn't fire
- Most exchange bots only support simple triggers (price-based stop or take-profit). Portfolio-level rules usually need you, an alert, or your own tool.
- Set price alerts on TradingView as a backup.
- Test triggers on a small bot first.

## API or connection issues (third-party tools)
- Use API keys with trading only. Never enable withdrawals.
- Restrict keys by IP if the exchange allows it.
- Rotate keys if you suspect a leak, and remove keys for tools you no longer use.

## Larger size, worse fills
- At larger size, each level can move the order book. Check depth on the pair, or split across venues.

## Platform risk signals
- Withdrawal delays, sudden rule changes, or public reports of problems. Reduce exposure on that venue first and ask questions later.

## When to ask the Elite Trading Floor
Post: exchange, layer, pair, settings, screenshot (no personal info), and what you tried.
