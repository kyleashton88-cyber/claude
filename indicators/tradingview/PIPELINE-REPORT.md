# TradingView → Whop alert pipeline: how it works, gaps, and a repeatable process

Prepared for Stewart, 25 Oct 2026 (AEDT). Research only: nothing was deployed, edited, posted or sent.
Labels: **[Found]** = seen in code, sheet or files. **[Inferred]** = my reading, not confirmed. Secrets (WHOP_API_KEY, webhook secret) are not quoted here.

Sources read: `/workspace/tradingview/*` (grid-screener*.pine, grid-bot-improved*.pine, alert-logger-v6.gs / -v6-deploy.gs, CHANGES.md, independent-review.md, score.py, score-latest.json, run_v6_chart_offline.js, render_v6_sample.py, payload files), the Google Sheet "Alert Log" tab (read only), and a quick scan of /workspace and the bot store.
Not read (time): the Whop Elite Intel forum, Slack, Linear and Drive. Facts about the forum and the hourly relay come from the brief.

---

## 1. The current process, step by step

### 1.1 TradingView side
**A. Screener alert: `grid-screener-merged(-deploy).pine` ("Grid-Fit Screener", Pine v6)** [Found]
- 36 symbol inputs `s00..s35` (Bybit USDT perps: BTC … TAO). Each one goes through `request.security(sym, timeframe.period, f_metrics(), lookahead_off, ignore_invalid_symbol=true)`. Pine allows 40 request.security calls per script.
- `f_metrics()` returns the values of the **last closed bar** (`[1]`), so the output does not repaint.
- **Score formula** (0–100):
  `score = 100 × (0.25·sAdx + 0.15·sBbw + 0.15·sAtr + 0.15·sX + 0.30·sFit)`
  - `sAdx = clamp((adxMax·1.6 − ADX14) / (adxMax·0.8), 0, 1)`, with adxMax = 22. That gives 1 at ADX ≤ 17.6 and 0 at ADX ≥ 35.2.
  - `sBbw = f_band(BBwidth%, 2, 8)`, using BB(20, 2) width as a % of the basis.
  - `sAtr = f_band(ATR14/close·100, 0.4, 1.8)`.
  - `f_band(x, lo, hi)` = 1 inside [lo, hi]. Below the band it is `max(0, 2x/lo − 1)`, which is 0 at lo/2. Above it is `max(0, 1 − (x−hi)/hi)`, which is 0 at 2·hi.
  - `sX = min(1, crosses of close over EMA50 in the last 100 bars / 8)`.
  - `sFit` = share of the last 300 bars whose close stayed inside the Donchian(100) high/low from 100 bars earlier ("containment").
- **Exclusions:** a spike sets the score to −2. A spike is ATR14/SMA(ATR14,100) > 1.8 or bar range > 2.5×ATR within the last 7 bars (`spikeCool` 6 + 1). Coins with 24-bar SMA(close·volume) < 2,000,000 USDT, or with no data, score −1 (`f_push`).
- **Mode** `gm`: neutral if ADX < 22 and BBW < 8. Otherwise long if close > EMA200, else short.
- **Ranking:** `array.sort_indices(sc, descending)`. On `barstate.isconfirmed`, the script takes up to `maxAlert` = 10 symbols with score ≥ `minScore` = 60. If there is at least one, it sends a single `alert()` with `alert.freq_once_per_bar_close` and the payload
  `{secret, src:"screener", action:"screener", tf, ts:time_close, alert_id:"screener_<tf>_<bar time>", symbols:[{s,m,lo,hi,fit}…]}`.
  `lo`/`hi` are the Donchian(100) low and high.
- **Offline mirror `score.py`** [Found]: pulls OKX 1H candles for the same 36 coins and uses the same weights. It does **not** match the Pine formula exactly: sAdx = 1 − ADX/40, sX = crosses/10, containment uses a 200→100-bar-old window, f_band fades differently below lo, neutral is ADX < 20, there is no spike filter, and the min-score/top-10 filter is missing. Latest output (`score-latest.json`): ZEC 69, DOGE 67, SUI 66, UNI 64, ENA 62, all "short". Treat it as a rough cross-check only.

**B. Strategy alert: `grid-bot-improved-merged(-deploy).pine` (Grid Bot v2)** [Found]
- Sends events `grid_build | entry | exit | edge_exit | range_break` (and `paused`, which the logger posts) via `alert()` at bar close. Payload fields: `src:"gridv2"`, symbol, side, price, level, qty, stop, ts, alert_id. Parameters are listed in CHANGES.md §1.
- I did not find a file named exactly "Grid Screener DRAFT". **[Inferred]** It is the TradingView title for grid-screener-merged.

**C. Alert creation in TradingView**: **not done yet** (per the brief, and confirmed by the sheet, which holds no organic alerts).

### 1.2 Apps Script logger: `alert-logger-v6.gs` (deployed as Apps Script Version 5; v6.1 title and v6.2 chart changes are pending and not deployed)
1. `doPost(e)`: parses the JSON and compares `d.secret` with the `SECRET` constant. The secret is removed from the row and from forwarding. `alert_id` is either the payload value or `h_`+md5(body). Under a ScriptLock (8 s; returns `busy` on timeout) it runs `isDuplicate()` (CacheService 6 h, then a TextFinder search of the sheet). It then appends a row to **Alert Log** with status `queued` or `rejected`. If the secret is bad it returns `bad secret`. For a `grid_build` it calls `rememberRange()`. Finally it stores a `job_<id>` script property (because `PROCESS_INLINE = false`).
2. `processQueue()`: runs on a 1-minute time trigger set up by `installTriggers()`. It claims up to 8 `job_*` properties per run, with a 240 s budget, and requeues anything left over.
3. `processAlert()`:
   - `chartTarget()` picks the screener's **top result `symbols[0]`**, or the strategy symbol plus its range.
   - `renderChart()` → `fetchCandles()` (Bybit, falling back to OKX, 100 candles) → `quickChartPng()` (POST quickchart.io). On error it falls back to `chartsServicePng()` (line chart). `screenerLines_()`/`levelLines()` draw 8 grid levels, entry and stop.
   - `saveToDrive()` saves to the "Grid Bot Alert Charts" folder.
   - **Code reality:** the local v6 file still builds the image URL as `lh3.googleusercontent.com/d/<id>`. The Whop file-hosting fix from today is **not in any local .gs file**. **[Inferred]** It was applied through the Whop connector or by hand on individual posts. The deployed logger probably still embeds Drive lh3 URLs.
4. `deliverToEliteIntel()` checks, in order:
   - `ELITE_INTEL_ENABLED == 'true'`
   - action is in `POST_ACTIONS` = entry, range_break, paused, screener (exits and grid_build go to the sheet only)
   - `WHOP_API_KEY` property exists
   - inside a lock: `posted_<md5>` dedupe; `rl_sym_<SYMBOL or SCREENER_tf>` at 1 per hour; `rl_day_<Sydney date>` at 6 per day. The rate-limit slot is reserved *before* posting and is not released on failure.
   It then calls `buildPost()` (education text, "(example)" levels, `POST_FOOTER`) and `whop('post','/forum_posts', {experience_id: exp_BqdQtgX9CW2kDb, visibility: members_only})`.
5. `pinLatest_()`: PATCHes `is_pinned`. **This always fails** with "missing forum:post:create" on the logger key (sheet rows 9–10). The post itself still goes through.
6. `forward()`: off (`FORWARD_URL = ''`).
7. `writeCells()` writes status, chart_url, chart, chart_error, post_id and post_error.
8. Downstream (from the brief): an hourly Grok Bot routine relays new forum posts to the Elite Trading Floor chat.

### 1.3 What the Alert Log shows (10 rows, read 25 Oct) [Found]
- **Every row is a manual or test row.** There are 0 real TradingView alerts: 2 early ZEC entries, 2 TEST_ZEC rows, and 6 `screener_60_…` retests (`_retest1`, `_v5test`, …).
- Errors recorded:
  - "skipped: ELITE_INTEL_ENABLED is not true" ×2
  - "400 Attachments are not supported for Account API keys" ×2 (v2; fixed in v3)
  - "rate limit (1 per symbol per hour)" ×1
  - "pin failed … forum:post:create" ×2
- Successful posts: post_1CgM5KTqd8b681NxY89rWA, post_1CgM6zk9427tzj8Bfa7Ywt, post_1CgMDAxkcTKBBCZZLErsi6.
- `received_at` uses two formats: dd/mm/yyyy for the first 2 rows, ISO for the rest. **[Inferred]** The sheet's timezone may not be Sydney. Check it.

## 2. Backtesting / assessment methodology
- **For the screener score: none found.** Nothing tests whether a high grid-fit score is followed by range-bound behaviour. The weights (25/15/15/15/30) and the 60 cut-off are hand-picked. CHANGES.md correctly says the score is descriptive and not a probability.
- **For the strategy:** only strategy-tester *settings* were tightened (capital 10k, 5%/order, 0.055% fee, 2-tick slippage, next-bar fills). There is one chart image (`bt-zec-1h.png`, ZEC 1h). CHANGES.md §5 lists walk-forward, multi-coin, funding and paper-trading tests as **recommendations, not done**. `independent-review.md` is a code review, not a backtest. `creative-studio/.../source-strategy-backtest-review.md` covers a different strategy (the three-layer ATR grid from the course).
- **For the pipeline:** testing was manual (testPost / testChartOnly / retest rows). There is no automated test, no offline harness beyond `run_v6_chart_offline.js` (chart rendering only), and no reconciliation.

## 3. Gaps and single points of failure (highest risk first)
1. **The TradingView alerts don't exist yet.** Nothing fires. When they are created, each one is a snapshot: changing inputs means recreating it, alerts expire (up to 2 months on Essential/Plus), and TradingView pauses or stops alerts silently, including when the plan or 2FA changes. Nothing watches for this.
2. **TradingView does not retry webhooks.** If the call times out or the lock is busy (`busy`), the alert is lost. There is no external log to reconcile against apart from TradingView's own alert log.
3. **No heartbeat or dead-man check.** If no alert arrives for N hours, nobody can tell a quiet market (no coin ≥ 60) from a broken pipeline. Silence and failure look the same.
4. **Image hosting mismatch.** The deployed or local code still uses Drive lh3 URLs, while the fix was done elsewhere (Whop files). If Drive sharing or lh3 behaviour changes, posts go out with broken images. The deployed code is out of step with the local source and CHANGES.md.
5. **Single Apps Script project and owner account.** Quotas (UrlFetch, triggers), a lost authorisation, a deleted `processQueue` trigger, or an edited secret all stop everything. Version drift is already visible: Version 5 is deployed and v6.1/6.2 sit in files.
6. **Single Whop key with limited scope.** Pinning always fails. If the key is rotated or loses `forum_posts` scope, every post fails, and that only shows up in the sheet. Failed posts are **not retried**, and their rate-limit slot stays used.
7. **Rate limits can hide valid alerts.** The screener posts at most once per hour per timeframe and 6 per day across everything. On 1h that means most candles are logged but not posted. That is by design, but it is undocumented for members.
8. **Hourly relay to the Elite Trading Floor** is another unmonitored hop. It can lag by up to about 1 h, and it is unclear whether it dedupes.
9. **Data and scoring:** Bybit symbols in Pine vs Bybit/OKX in the logger vs OKX in score.py. `ignore_invalid_symbol` silently drops delisted coins. score.py differs from the Pine formula. The score has not been validated.
10. **Secret handling:** a single shared secret sits in the payload and in a .gs constant (local `*-deploy.gs` and `.webhook-secret` files). There is no rotation procedure.
11. **Sheet growth:** `isDuplicate` scans the whole column. **[Inferred]** It slows down after many thousands of rows, but that is fine at current volume.

## 4. Proposed repeatable process

### 4.1 Alert setup checklist (one-time, and again after any script change)
1. Deploy the logger version you intend to run. Write down the Apps Script version number and the md5 of the source in CHANGES.md. Confirm that `installTriggers()` created exactly one `processQueue` trigger.
2. Confirm the script properties exist: `WHOP_API_KEY` and `ELITE_INTEL_ENABLED` (keep it `false` until step 9). Don't paste the values anywhere.
3. TradingView (2FA on): add **Grid-Fit Screener** to a 1h chart and set the secret input. Then: Alert → condition "Any alert() function call" → Webhook URL = the `/exec` URL in `logger-url.txt`. Name it `GBB-SCREENER-1H vX`. Set expiry to the maximum and record the expiry date.
4. Strategy: chart BYBIT:ZECUSDT.P 1h → Grid Bot v2 → set the secret → "alert() function calls only" (not "order fills and alert()") → same webhook → name it `GBB-GRIDV2-ZEC-1H vX`.
5. Record both alerts (name, chart, timeframe, input snapshot, created date, expiry) in a new "Alert Registry" tab, or in CHANGES.md if the sheet should stay untouched.

### 4.2 Monitoring and health checks
- **Heartbeat** [proposed]: add a time-trigger function, or a Grok Bot routine, that alerts Stewart if **no row arrives within 3 h** during normal operation, or **no screener row arrives within 24 h**. For a stronger signal, make the screener send a small `action:"heartbeat"` every bar (sheet only, never posted).
- **Daily health digest** (09:00 AEDT): yesterday's rows by status, counts of `rejected` / `post_error` / `chart_error`, posts made against the cap, the latest post_id, and the queue length (`job_*` count).
- **Weekly:** check the TradingView alert list (active and expiry dates), confirm the Whop key works with a dry-run GET, renew alerts more than 7 days before expiry, and check that the 36 symbols are still listed.
- **Relay:** the routine should log each relayed post_id so you can see forum → chat lag.

### 4.3 Failure handling (runbook)
| Symptom | Action |
|---|---|
| No rows | Check that the TradingView alert is active and not expired, then its own log. Run `doGet` (the URL should return "ok"). Check the trigger. |
| `rejected` | Secret mismatch: re-enter it in the TradingView inputs, then recreate the alert. |
| `post_error` 4xx | Key or scope problem. Repost via the Whop connector after approval. Add a retry queue that releases the rate-limit slot after a failure [proposed]. |
| `chart_error` | Post text only (already the behaviour). Fix quickchart/candles later. |
| `pin failed` | Expected. Pin through the Whop connector, or grant the scope. |
| Queue backlog | Check Apps Script quotas and executions. |
Kill switch: set `ELITE_INTEL_ENABLED=false` (logging continues).

### 4.4 Test procedure before go-live
1. Run offline: `run_v6_chart_offline.js` / `render_v6_sample.py` on the payload files. Check the title, levels and footer visually.
2. Run the editor test with `ELITE_INTEL_ENABLED=false`: `testChartOnly()`, then `testPost()`. Expect a row with status `done` and the post skipped.
3. Webhook test: curl the `/exec` URL with a payload that uses a fresh `alert_id` and **a wrong secret**, and expect `rejected`. Then send the correct secret and expect `queued`, then `done` within 2 minutes. Send the same alert_id again and expect `duplicate`.
4. In TradingView, create the real alert, wait for one closed candle, and confirm the row.
5. Supervised post: switch on, take one post, and check it in Elite Intel (image renders, text, labels, footer). Check that the relay reaches the Trading Floor.
6. Watch for 48 h, then sign off in CHANGES.md.

### 4.5 Ownership [proposed]
- **Stewart:** TradingView account, creating and renewing alerts, the ELITE_INTEL switch, go-live sign-off.
- **Grok Bot:** logger code and versions, health digest, relay routine, runbook triage. It drafts fixes but deploys or posts only with approval.
- **Legal:** reviews any change to post text or footer.
- Single source of truth: CHANGES.md plus the alert registry.

### 4.6 Legal education-only guardrails (apply to every post and chart)
- Price levels in post text are labelled **"(example)"**. Keep `POST_FOOTER`: "Example only. General education, not financial advice." (v6 removes "example" from the image itself. Confirm with Legal that the post text label is enough.)
- No profit, return, win-rate or probability claims. The grid-fit score is "descriptive, history-based, not a forecast."
- No backtest numbers in member posts. If any ever appear, label them "historical simulation".
- No "buy/sell now" instructions. Use neutral wording ("a grid example could…").
- Visibility stays members_only, and posts go only to the Elite Intel experience (hardcoded).
