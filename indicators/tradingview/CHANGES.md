# Grid Bot – changes, webhook setup, coin coverage (Draft – not published)

Prepared for Stewart. Education-only material: everything here is about robustness and risk control. Backtest numbers are historical simulation, not a statement about future results.

Files:
- `grid-bot-improved.pine` – strategy (Pine v6), Neutral / Long / Short grid.
- `grid-screener.pine` – companion indicator ranking 36 coins by a history-based **grid-fit score**.
- `alert-logger.gs` – Google Apps Script webhook receiver that logs to the Google Sheet "Grid Bot Alert Log" (ID `1c-KueHCYrIEqemNCZMbIxg4b7letYsHlugKj8VnAn5c`).

## 1. What changed and why (strategy)

Problems in the original:
1. **Repainting / moving grid.** The range was recomputed from the live `close` every bar (and intrabar), so levels moved with price and a "crossing" could be manufactured by the grid moving, not price. Now the range is computed from the previous closed bar (`[1]`) and **frozen** when the grid is built; it is only rebuilt after invalidation.
2. **Unrealistic backtest.** `initial_capital = 1,000,000` with a fixed 1-unit order meant position size was meaningless; commission 0.1%; `process_orders_on_close = true` filled orders at the same close that generated the signal. Now: capital 10,000, 5% equity per grid order, commission 0.055% (Bybit taker), slippage 2 ticks, `process_orders_on_close = false` (fills next bar open), `calc_on_every_tick = false`, margin 100%.
3. **Grid logic bugs.** All grid buys shared one entry ID ("Grid Buy"), and any up-cross closed *everything* with `close_all`, so it was not a grid. Now each level has its own entry ID (`L3`, `S5`…) and its own exit at the adjacent level (limit) plus a hard stop beyond the range.
4. **Off-by-one.** Top line could never be sold to, bottom line never bought from — now explicit: longs only on levels 0..n-2 (target i+1), shorts only on 1..n-1 (target i-1).
5. **Pyramiding cap.** `pyramiding = 50` with an unreliable entry counter. Now pyramiding 20 and a per-bar counter enforces "Max open grid levels" even if several levels are crossed in one bar.
6. **ta.* in conditional branches** (v6 warning, inconsistent series). All indicator calls now run every bar.
7. **Integer division pitfall.** Level fraction uses `i / (n - 1.0)`.
8. **Fees vs grid step.** Grid is not built if step % < "Min step %" (default 0.6%), since a round trip costs ~0.11% + slippage.
9. **Hard stop/TP that ignored direction and regime.** Replaced with: range-break invalidation (close beyond edge ± 1 ATR → close all, cooldown 12 bars), resting stop orders for intrabar protection, optional flatten at opposite edge.
10. **alert() placeholders.** `{{ticker}}`/`{{close}}` are *not* expanded inside `alert()` messages; the script now uses `syminfo.ticker`/actual values there, and `{{ticker}}` only in order `alert_message`.
11. Removed `alertcondition()` (not usable in strategies for webhooks) and "net profit per grid" text.

New features: three modes; range method ATR / Donchian / Percentile; arithmetic/geometric spacing; grid count; regime filter (ADX < 22 and BB-width < 8% = ranging; Neutral only in ranging, Long only above EMA200, Short only below); max open levels; cooldown; status table.

### Default parameters (chosen for 1h crypto perps)
| Input | Default |
|---|---|
| Mode | Neutral |
| Range method / lookback | Donchian / 100 bars |
| Spacing / grid lines | Geometric / 10 |
| Min step % | 0.6 |
| ADX max / BB width max / Trend EMA | 22 / 8% / 200 |
| Equity % per order / max open levels | 5% / 6 (max ~30% equity deployed) |
| Range-break stop | 1.0 ATR beyond edge |
| Cooldown after invalidation | 12 bars |

## 2. Webhook alerts

Payload (strategy), one per event, sent at bar close:
```json
{"secret":"CHANGE_ME","src":"gridv2","action":"entry","mode":"neutral","symbol":"ZECUSDT.P","side":"buy","price":51.23,"level":3,"qty":9.7,"stop":47.8,"ts":1792818000000}
```
`action` ∈ `grid_build`, `entry`, `exit`, `edge_exit`, `range_break`. `ts` = bar close time in ms (UTC epoch).

Screener payload:
```json
{"secret":"CHANGE_ME","src":"screener","action":"screener","tf":"60","ts":1792818000000,"symbols":[{"s":"BYBIT:LTCUSDT.P","m":"neutral","lo":78.1,"hi":86.4,"fit":71}]}
```

### Create the strategy alert in TradingView
1. Open the chart (e.g. BYBIT:ZECUSDT.P, 1h), add the strategy, set inputs (change the secret).
2. Alert (clock icon) → **Condition**: "Crypto Grid Strategy v2…" → choose **"alert() function calls only"** (recommended: confirmed-bar signals only).  
   Alternative for bots that act on fills: **"Order fills only"** (uses each order's `alert_message`). Do not pick "Order fills and alert() function calls" with a bot, or you get duplicates.
3. **Message** box: leave as `{{strategy.order.alert_message}}` (for order fills) — for alert() calls the message comes from the script automatically.
4. **Frequency** is controlled by the script (`alert.freq_once_per_bar_close`).
5. **Notifications** tab → tick **Webhook URL** → paste the bot URL (Apps Script `/exec` URL, or the 3Commas/Pionex/Bybit-signal-bot URL). Requires 2FA on the TradingView account.
6. Expiration: Essential/Plus alerts last up to 2 months – renew them.
7. Changing inputs later requires deleting and recreating the alert (alerts snapshot the settings).

Screener: add `grid-screener.pine` on any 1h chart → Alert → Condition "Grid-Fit Screener" → "Any alert() function call" → webhook URL. One alert covers all 36 symbols.

Exchange formats: 3Commas, Pionex and Bybit signal bots each expect their own JSON fields (bot ID, pair, `email_token`, etc.). Either edit `f_json()` to match, or send to the Apps Script/your relay and translate there. Always validate `secret` server-side.

## 3. Coin coverage

Verified TradingView limits (pricing page, checked 24 Oct 2026): 
| Plan | Price alerts | Technical alerts | Watchlist alerts |
|---|---|---|---|
| Essential | 20 | 20 | 0 |
| Plus | 100 | 100 | 0 |
| Premium | 400 | 400 | 2 |
| Ultimate | 1,000 | 1,000 | 15 |
Strategy/indicator alerts count as *technical* alerts. Source: https://www.tradingview.com/pricing/ and https://www.tradingview.com/support/solutions/43000696403-alerts-separation-by-type/

Options:
- **One alert per chart (Essential):** up to 20 technical alerts → e.g. 1 screener alert + 19 strategy alerts on the coins the screener ranks highest. Rotate weekly.
- **Screener (any plan):** one alert scans 36 symbols (request.security limit is 40 per script; 36 + 1 for the chart symbol = 37). Use 2 copies with different symbol lists for ~72 coins (uses 2 alerts).
- **Watchlist alerts (Premium+):** create a watchlist, then Alert → condition = the strategy → apply to the watchlist; one alert runs on every symbol in it. Not available on Essential/Plus.

Default 36 symbols (Bybit USDT perps – check each still exists, `ignore_invalid_symbol` skips missing ones): BTC ETH SOL XRP DOGE ADA AVAX LINK DOT LTC BCH TRX TON SUI APT ARB OP NEAR ATOM FIL ETC XLM HBAR INJ SEI TIA AAVE UNI ICP ZEC ALGO WLD RENDER ENA ONDO TAO.

Grid-fit score (0–100, based on history only, not a probability): 25% low ADX, 15% BB width in 2–8% band, 15% ATR% in 0.4–1.8% band, 15% midline (EMA50) crossings over 100 bars, 30% historical containment = % of the last 300 bars whose close stayed inside the Donchian range known 100 bars earlier. Coins below the liquidity floor (24-bar avg quote volume < 2M USDT per bar) rank last. Mode suggestion: neutral if ranging, long above EMA200, short below.

## 4. Alert log sheet
https://docs.google.com/spreadsheets/d/1c-KueHCYrIEqemNCZMbIxg4b7letYsHlugKj8VnAn5c/edit — tabs "Alert Log" (headers = `HEADERS` in alert-logger.gs) and "Summary" (counts by action, rejected secrets, alerts by symbol). Deploy alert-logger.gs as a web app and use its `/exec` URL as the webhook URL.

## 5. Further recommendations
1. Paper-trade first (TradingView paper account or exchange testnet) for several weeks before any live bot.
2. Walk-forward test: optimise on one period, test on the next unseen period; repeat on BTC, ETH, SOL plus a few alts, on 15m/1h/4h.
3. Use Deep Backtesting (Premium+) or the bar magnifier (`use_bar_magnifier = true`, Premium+) for realistic intrabar fills of limits/stops.
4. Set commission to your actual fee tier (maker vs taker; 0.02% maker if grid orders are posted as limits on the exchange).
5. Model funding for perps: Strategy Tester ignores funding; holding grid legs through many 8h funding periods can be a material cost.
6. Stress-test the range-break stop: check the largest drawdown and the worst losing streak in the "List of trades", not only net result.
7. Keep max deployed equity (order % × max levels) and leverage low; consider isolated margin.
8. Match the payload to each bot's required format and verify one test alert end-to-end before enabling execution.
9. Re-check symbol lists and TradingView plan limits periodically; renew expiring alerts.
10. Log every alert (Apps Script sheet) and reconcile against exchange fills weekly.

## v6 – chart template restyle (2026-10-24)
- Chart image only (quickChartPng/levelLines); post text, POST_FOOTER and "(example)" labels unchanged.
- Navy background #121826, faint dashed grid, price axis on left, x labels "d MMM HH:mm" (Sydney).
- Removed the in-chart "Data: …" watermark; added bottom-left footer "data: <SRC> <SYMBOL> <tf> · times Sydney · not financial advice". No "example" anywhere on the image.
- Grid levels: thin dotted orange; labelled boxes rounded. Entry blue / stop red dashed / range orange / yellow alert dot kept.
- Sample: chart-template-v6-sample.png (render_v6_sample.py, live OKX ZEC-USDT-SWAP 1H).

## v6.1 – 24 Oct 2026
- chartTitle(): for screener alerts the title's style word now comes from the top pick's direction (`symbols[0].m`: short/long/neutral, the same field the post table uses for "Short grid"). Falls back to top-level `mode`, then the alert type ("screener"). Fixes titles reading "screener · screener". Nothing else changed.
- Applied to alert-logger-v6.gs and alert-logger-v6-deploy.gs. Not deployed.

## v6.2 – 24 Oct 2026
- Screener charts now match Stewart's mock: 8 thin dotted orange grid levels between range low/high (n from payload, default 8; step = (hi-lo)/(n+1)); blue "Entry <price>" (payload entry, else alert-bar close); red dashed "Stop <price>" (payload stop, else one grid step above the high for short, below the low for long/neutral). New helper screenerLines_(); levelLines(target, d, barClose); chartTarget passes n/entry/stop for screener.
- Layout: framed plot (box annotation), inset padding, y-axis grace 6%; label boxes left; title (v6.1) and footer unchanged. No "example" on the image. Yellow dot now sits on the alert bar's close.
- Applied to alert-logger-v6.gs and alert-logger-v6-deploy.gs. Not deployed. Rendered: zec-post-chart-v6b.png (live on post_1CgMDAxkcTKBBCZZLErsi6).

## v6.3 – 2026-10-24 – richer post text (buildPost only; chart code unchanged)
- Screener posts: score breakdown for the top pick (sideways 40% / volatility 30% / range-staying 30%, volume pass/fail; sub-scores shown only when the payload carries `sw`,`vl`,`rs`,`qv`, otherwise a note says they are not sent), grid step in price and % plus line count, example entry (alert-bar close) and example stop (one step beyond the edge), the same values as the chart, risk notes (thin-coin filter, circuit-breaker rule).
- Entry/range_break/paused posts: grid step line, risk notes (circuit-breaker status/rule, volume/thin status; uses optional `cb`,`qv`,`thin` when present).
- No backtest stats (education-only rule). Disclaimer kept. "1 coin" grammar fix.

## Screener v4h-1 – 4h data, 1h alerts (24 Oct 2026, draft, not published)
- New file `grid-screener-4h.pine` (from `grid-screener-merged.pine`; old files kept). Title unchanged ("Grid-Fit Screener – Draft").
- New input "Source timeframe" (default "240"). All 37 request.security calls (36 symbols + chart symbol) now use `srcTf` with `lookahead = barmerge.lookahead_on`; f_metrics() still returns only `[1]` values → every 1h bar sees the last COMPLETED 4h bar, no repaint. Score, ADX/BB/ATR, containment, midline crosses, spike filter, range lo/hi and mode are all 4h-based (lookbacks are now in 4h bars: range 100 = ~16.7 days, history 300 = 50 days).
- Liquidity: now "avg quote volume per hour over the last 24h" (sum of 6 4h bars / 24), so the 2M threshold means the same as before.
- Guard: runtime error if the chart timeframe is not lower than the source TF.
- Alert still `alert.freq_once_per_bar_close` on the 1h chart; `tf` stays "60", `alert_id` stays `screener_60_<bar time>`. New payload keys: `"tf4h":"240"`, `"src_tf":"240"`, `"src_bar_close":<ms close of the 4h bar used>`. Logger v6 ignores unknown keys (no logger change needed). Note: the logger still draws 1h candles for the chart while lo/hi come from the 4h range.
- Security calls: 37 / 40 (tuples, 10 values each).
- Python: `score_4h.py` (copy of score.py, unchanged original) with `--tf4h` flag → OKX 4H, completed bars only (confirm flag), writes score-latest-4h.json. `sim_4h_on_1h.py` replays the last 48 1h closes; output in `sim-4h-output.txt` (results changed 12 times, all on 4h-boundary closes).
