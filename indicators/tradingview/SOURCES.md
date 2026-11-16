# TradingView sources

Copied from the shared store `/cursor/stores/bot/tradingview-src/` on 16 Nov 2026.

The strategy under test is `grid-bot-original.pine` (`Crypto Grid Bot Master Strategy & Alert System`, Pine v6). Arithmetic and Geometric are its two grid modes (`gridModeInput`). There is no separate on-chain indicator in this set.

Also stored here:

- v2 neutral scripts (`grid-bot-improved*.pine`), including `grid-bot-improved-merged-deploy-weekday.pine`
- grid screeners (`grid-screener*.pine`)
- `independent-review.md`, `CHANGES.md`, `PIPELINE-REPORT.md`
- `elite-mastery/` course drafts
- `optimisation-2026-11-10/` code, the small result tables, and the parameter JSON from the 10 Nov 2026 v2 study

Left in the store, not in git: that study's candle dumps and the multi-megabyte search logs (`data/`, `search_*.csv`, `cipher_1h.csv`, `cipher_4h.csv`, `oos_all_*.csv`). Those files are a prior v2 simulation on Binance candles. This study refetches public Bybit spot candles and ports `grid-bot-original.pine` on its own.
