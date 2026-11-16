# Independent Review: `grid-bot-original.pine` (Crypto Grid Bot Master Strategy & Alert System)

Prepared for Stewart Crown. **Education only.** This review covers code correctness, how realistic the backtest model is, and alert plumbing. It makes no claims about profit, win rate or probability. Backtest output is a simulation and does not predict live results.

Line numbers refer to the original file (355 lines). Each fix is labelled **FIX-xx** so it can be merged into `grid-bot-improved.pine`. All snippets target `//@version=6`.

---

## Summary of issues (severity: H = high, M = medium, L = low)

| ID | Sev | Lines | Issue |
|----|-----|-------|-------|
| R1 | H | 126-140, 110-111 | **The grid is not anchored.** In Auto mode (default) the `else` branch (138-140) rebuilds `activeLower/activeUpper` from the current `close` on every bar. Manual mode with 0 limits also re-centres on `close` every bar (110-111). Levels move with price, so "crossings" are mostly artefacts of the moving grid, and the rebuild at 152-160 is overwritten on the next bar (in Auto mode `rebuiltLower` is never used). |
| R2 | H | 200-205, 253 | **The stop and take-profit move with the grid.** Because of R1 the hard stop is recalculated below the latest close each bar. It keeps sliding down and can only be hit intrabar. `strategy.exit` (253) is re-issued with the new level every bar. |
| R3 | H | 220-236, 256-259 | **No per-level state.** One `Grid Buy` ID is used for every entry. Only the *last* crossed level in the loop is kept (233/236). A gap through N levels gives at most 1 buy. The same level can be bought again and again. Any up-cross of *any* level (even one never bought) triggers `close_all` (259), so the script is really "buy dips, dump everything" rather than a grid. |
| R4 | H | 229-230 | Crossing detection compares `close` with the current level and `close[1]` with the previous bar's level (`priorGridLevel`). When the grid shifts, a level can "cross" with no price movement. Bars where `low`/`high` touched a level but closed back are missed. |
| R5 | H | 91-92, 283-293 | **Placeholders inside `alert()` are not expanded.** `{{ticker}}`, `{{time}}`, `{{close}}` and `{{strategy.order.action}}` stay as literal text in `alert()` calls. They only work in alert-dialog messages and strategy order-fill `alert_message`. Use `syminfo.tickerid`, `time_close`, `close` and an explicit side instead. |
| R6 | H | 253-263 vs 266-280 | **Duplicate alert channels.** Every event sends both an order-fill `alert_message` and an `alert()` call. One TradingView alert set to "alert() function calls" plus order fills, or two alerts, will deliver the same event twice. Choose one channel. |
| R7 | M | 283-293 | `alertcondition()` has no effect in strategy scripts. It is dead code and may confuse users who expect it to show up in the alert dialog. |
| R8 | H | 90 | `bot_signal_id` = prefix+event+time+bar_index. It has no grid level index and no symbol or timeframe, so two levels on the same bar, or the same script on two charts, produce colliding IDs. There is also no per-level "already fired" state. |
| R9 | M | 80-82 | Grid prices are not rounded to `syminfo.mintick`. Orders and alerts carry unexecutable prices, and the arithmetic and geometric spacing drift from the exchange tick grid. |
| R10 | M | 212-217 | Quantity is not rounded to the exchange lot/step size, and there is no min-qty or min-notional check. `buyOrderQty` can be dust that the exchange rejects. |
| R11 | M | 214 | `currentEntryCount` = position/orderQty. This is wrong once quantities are risk-reduced (216). Count open trades or held levels instead. |
| R12 | M | 194-197 | The fee estimate is hardcoded at `0.001` and not linked to `commission_value`. It ignores slippage and perp funding, and uses `orderQtyInput` instead of the actual `buyOrderQty`. |
| R13 | M | 3-6 | `slippage = 1` tick is negligible on low-priced coins and unrealistic on illiquid ones. `initial_capital = 1,000,000` with `qty = 1` hides sizing problems. There is no `margin_long` setting for perp modelling. |
| R14 | M | 133 | `ta.rising()` is called inside a conditional branch, so its history is inconsistent (Pine warns about this). Compute it globally. |
| R15 | M | 184-187 | `math.log(activeUpper/activeLower)` and divisions are not guarded: you get na or div/0 when upper == lower or on early bars with na. `int(math.floor(na))` propagates. |
| R16 | M | 96-119 | No history guard. On a new listing, `ema/atr/bb/dmi` are na. `nz(...,0)` (100-101) collapses the ATR range to the close, and a grid is built on garbage that same bar. |
| R17 | M | 239-240 | `stopTriggered` needs a *cross* (`close[1] > stopLevel[1]`). If price gaps and stays below a moving stop (R2), the condition never becomes true while a position is still open. Use state (`position > 0 and low <= stop`) with a fire-once flag. |
| R18 | M | none | No liquidity filter: no volume/notional floor and no spread proxy. Thin coins produce fills in the backtest that would not happen live. |
| R19 | L | none | No weekend/session-gap handling. CME-style or exchange-maintenance gaps, or missing bars, can jump several levels; entries should be skipped or flagged on gap bars. |
| R20 | L | 63, 91 | The webhook secret is a plain input that is embedded in the payload and visible in alert logs. That is acceptable, but document it and never reuse an exchange API key here. |
| R21 | L | 151 | `rebalanceTriggered` uses `nz(outsideBars[1])`, but `outsideBars` is reset inside the same bar (161). That is fine, but in Auto mode the rebuild is discarded (R1). |
| R22 | L | 180, 255-257 | A trend exit and a buy on the same bar are only mutually exclusive while the trend filter is on. With the filter off, a trend exit cannot occur, but stop/TP plus a buy on the same bar can still race: 241 excludes them, but `sellTriggered` + `buyActionTriggered` on the same bar is possible. |
| R23 | L | none | Repainting: the logic uses the current bar's `close` with `barstate.isconfirmed` gating, which is fine. Do **not** add `request.security` without `lookahead_off` plus `[1]` offsets. Auto-grid levels drawn on the live bar move until it closes (R1). |

---

## Drop-in fixes (Pine v6)

### FIX-01: Strategy header (fees, slippage, margin) — replaces lines 3-6
```pine
strategy("Crypto Grid Bot Master Strategy & Alert System", overlay = true, pyramiding = 50,
     initial_capital = 10000, default_qty_type = strategy.fixed, default_qty_value = 1,
     commission_type = strategy.commission.percent, commission_value = 0.1, slippage = 2,
     margin_long = 100, margin_short = 100,
     process_orders_on_close = true, calc_on_every_tick = false,
     max_lines_count = 500, max_labels_count = 100)
```

### FIX-02: New inputs (exchange filters, costs, liquidity, history, gaps)
```pine
string GROUP_EXCH = "Exchange Filters & Costs"
string GROUP_LIQ  = "Liquidity & Data Quality"
lotStepInput        = input.float(0.0, "Lot / Qty Step (0 = none)", minval = 0.0, group = GROUP_EXCH)
minQtyInput         = input.float(0.0, "Min Order Qty", minval = 0.0, group = GROUP_EXCH)
minNotionalInput    = input.float(5.0, "Min Order Notional (quote)", minval = 0.0, group = GROUP_EXCH)
feePctInput         = input.float(0.1, "Fee % per side (match commission_value)", minval = 0.0, step = 0.01, group = GROUP_EXCH)
slipTicksInput      = input.int(2, "Slippage ticks per side (match slippage)", minval = 0, group = GROUP_EXCH)
fundingPct8hInput   = input.float(0.01, "Perp funding % per 8h (0 = spot)", step = 0.005, group = GROUP_EXCH)
expectedHoldHInput  = input.float(24.0, "Assumed hold time per grid (hours)", minval = 0.0, group = GROUP_EXCH)
liqLenInput         = input.int(20, "Liquidity lookback", minval = 1, group = GROUP_LIQ)
minQuoteVolInput    = input.float(250000.0, "Min avg quote volume per bar", minval = 0.0, group = GROUP_LIQ)
maxSpreadProxyInput = input.float(1.5, "Max avg (high-low)/close %", minval = 0.0, step = 0.1, group = GROUP_LIQ)
gapPctInput         = input.float(2.0, "Gap threshold % (open vs prior close)", minval = 0.0, step = 0.1, group = GROUP_LIQ)
```

### FIX-03: Rounding helpers (tick, lot, min notional) — add after line 82
```pine
f_tick(float p) => na(p) ? na : math.round_to_mintick(p)
f_lot(float q) => lotStepInput > 0.0 ? math.floor(q / lotStepInput + 1e-9) * lotStepInput : q
f_validQty(float q, float px) => q > 0.0 and q >= minQtyInput and q * px >= minNotionalInput
```
Replace `f_gridPrice` (80-82) so levels sit on the tick grid. Geometric spacing uses equal % steps and arithmetic uses equal price steps:
```pine
f_gridPrice(int _index, float _lower, float _upper, int _levels, string _mode) =>
    float fraction = _index / float(_levels - 1)
    float raw = _mode == "Geometric" and _lower > 0.0 ? _lower * math.pow(_upper / _lower, fraction) : _lower + (_upper - _lower) * fraction
    math.round_to_mintick(raw)
```

### FIX-04: History, liquidity, spread, gap guards (R16, R18, R19) — add after line 119
```pine
int warmupBars = math.max(autoLengthInput, atrLengthInput, bbLengthInput, trendMaLengthInput, adxLengthInput + adxSmoothingInput) + 1
bool enoughHistory = bar_index >= warmupBars and not na(atrValue) and not na(emaBasis) and not na(bbLower)
float avgQuoteVol = ta.sma(volume * close, liqLenInput)
float spreadProxy = ta.sma((high - low) / close * 100.0, liqLenInput)
bool liquidityOk = not na(avgQuoteVol) and avgQuoteVol >= minQuoteVolInput and nz(spreadProxy, 1e9) <= maxSpreadProxyInput
float barMs = timeframe.in_seconds() * 1000.0
bool timeGap = not na(time[1]) and (time - time[1]) > barMs * 1.5
bool priceGap = not na(close[1]) and math.abs(open / close[1] - 1.0) * 100.0 >= gapPctInput
bool gapBar = timeGap or priceGap
bool dataOk = enoughHistory and liquidityOk
```
Volume on some crypto feeds is base-asset volume, so `volume*close` gives quote notional. Confirm what your exchange feed reports.

### FIX-05: Anchored grid (R1, R2, R14, R21) — replaces lines 121-161
```pine
bool risingN = ta.rising(close, trendLengthInput)       // global call (R14)
var float activeLower = na
var float activeUpper = na
var int   gridEpoch   = 0                                // bumps on every rebuild; used in alert IDs
bool needInit = na(activeLower) and dataOk and barstate.isconfirmed
if needInit
    activeLower := f_tick(rawLower)
    activeUpper := f_tick(effectiveUpper)
    gridEpoch += 1
else if trailingGridInput and barstate.isconfirmed and not na(activeUpper) and close > activeUpper and risingN
    float upwardShift = close - activeUpper
    activeLower := f_tick(activeLower + upwardShift)
    activeUpper := f_tick(activeUpper + upwardShift)
    gridEpoch += 1
// Outside/rebuild accounting, unchanged in spirit but the rebuild now persists
float boundaryLowerBeforeRebuild = activeLower
float boundaryUpperBeforeRebuild = activeUpper
bool outsideRangeBeforeRebuild = not na(activeLower) and (close > activeUpper or close < activeLower)
var int outsideBars = 0
if barstate.isconfirmed
    outsideBars := outsideRangeBeforeRebuild ? outsideBars + 1 : 0
bool upperBreakout = barstate.isconfirmed and not na(activeUpper) and close > activeUpper and close[1] <= nz(activeUpper[1], activeUpper)
bool lowerBreakdown = barstate.isconfirmed and not na(activeLower) and close < activeLower and close[1] >= nz(activeLower[1], activeLower)
bool rebalanceTriggered = barstate.isconfirmed and dataOk and outsideBars >= regridBarsInput and strategy.position_size == 0.0
if rebalanceTriggered
    // auto mode: rebuild from fresh volatility range; manual mode: keep width, recentre
    float w = math.max(activeUpper - activeLower, syminfo.mintick * 2)
    activeLower := autoGridInput ? f_tick(rawLower) : f_tick(math.max(syminfo.mintick, close - w * 0.5))
    activeUpper := autoGridInput ? f_tick(effectiveUpper) : f_tick(activeLower + w)
    outsideBars := 0
    gridEpoch += 1
bool gridReady = not na(activeLower) and not na(activeUpper) and activeUpper > activeLower and activeLower > 0.0
```
The rebuild now happens only while flat. Rebuilding with open per-level positions would orphan them. If you want rebuilds while holding a position, close everything first and emit a REBUILD alert.

### FIX-06: Safe grid metrics (R15) — replaces lines 184-192
```pine
float rangeRatio = gridReady ? activeUpper / activeLower : na
float geometricFactor = gridReady ? math.pow(rangeRatio, 1.0 / (gridLevelsInput - 1)) : na
float arithmeticStep = gridReady ? (activeUpper - activeLower) / (gridLevelsInput - 1) : na
float spacingPercent = gridModeInput == "Geometric" ? (geometricFactor - 1.0) * 100.0 : arithmeticStep / activeLower * 100.0
float gridPosition = not gridReady ? na : gridModeInput == "Geometric" ? math.log(close / activeLower) / math.log(rangeRatio) : (close - activeLower) / (activeUpper - activeLower)
int activeIndex = na(gridPosition) ? 0 : math.max(0, math.min(gridLevelsInput - 1, int(math.floor(gridPosition * (gridLevelsInput - 1)))))
float activeLevel = gridReady ? f_gridPrice(activeIndex, activeLower, activeUpper, gridLevelsInput, gridModeInput) : na
```

### FIX-07: Cost model incl. slippage + funding (R12) — replaces lines 193-197
```pine
float nextLevel = gridReady and activeIndex < gridLevelsInput - 1 ? f_gridPrice(activeIndex + 1, activeLower, activeUpper, gridLevelsInput, gridModeInput) : activeLevel
float estimatedGridStep = nz(nextLevel - activeLevel)
float estQty = f_lot(orderQtyInput)
float feeCost   = (activeLevel + nextLevel) * estQty * feePctInput / 100.0
float slipCost  = 2.0 * slipTicksInput * syminfo.mintick * estQty
float fundCost  = activeLevel * estQty * fundingPct8hInput / 100.0 * (expectedHoldHInput / 8.0)
float grossProfitPerGrid = estimatedGridStep * estQty
float estimatedNetProfitPerGrid = grossProfitPerGrid - feeCost - slipCost - fundCost
float breakevenSpacingPct = 2.0 * feePctInput + 2.0 * slipTicksInput * syminfo.mintick / nz(activeLevel, close) * 100.0 + fundingPct8hInput * expectedHoldHInput / 8.0
bool spacingCoversCosts = nz(spacingPercent) > breakevenSpacingPct
```
This is an arithmetic cost estimate per grid round trip, shown for education. It is not a forecast. Funding can be negative or positive; the input models it as a cost.

### FIX-08: Qty rounding, min notional, entry count (R10, R11) — replaces lines 214-217
```pine
var array<bool>  levelHeld  = array.new_bool(MAX_GRID_LEVELS, false)
var array<float> levelQty   = array.new_float(MAX_GRID_LEVELS, 0.0)
int heldCount = 0
for i = 0 to MAX_GRID_LEVELS - 1
    if array.get(levelHeld, i)
        heldCount += 1
int currentEntryCount = heldCount
float remainingRiskQty = math.max(0.0, maxOpenGridQty - math.max(strategy.position_size, 0.0))
float buyOrderQty = f_lot(math.min(orderQtyInput, remainingRiskQty))
float buyOrderPercent = maxOpenGridQty > 0.0 ? buyOrderQty / maxOpenGridQty * 100.0 : 0.0
```

### FIX-09: Per-level grid engine with gap handling and fire-once state (R3, R4, R8, R22) — replaces lines 219-236 and 252-263
Level *i* (0..N-2) is a buy level, and its paired sell is level *i+1*. Each level can hold **at most one** open lot (`levelHeld`), so a gap that jumps several levels fills each crossed level **once**. Fills are recorded on confirmed bars only, so realtime ticks cannot mutate state: `var` state set under `barstate.isconfirmed` is committed once per bar.
```pine
var int alertSeq = 0
var array<int> levelLastAlertBar = array.new_int(MAX_GRID_LEVELS, -1)
int   buysThisBar  = 0
int   sellsThisBar = 0
bool  buyTriggered = false
bool  sellTriggered = false
float buyTriggerLevel = na
float sellTriggerLevel = na
bool canBuyBar = barstate.isconfirmed and gridReady and dataOk and not gapBar and rangeEligibleForBuy and not stopTriggered and not takeProfitTriggered
if barstate.isconfirmed and gridReady
    for i = 0 to MAX_GRID_LEVELS - 2
        if i < gridLevelsInput - 1
            float buyLvl  = f_gridPrice(i, activeLower, activeUpper, gridLevelsInput, gridModeInput)
            float sellLvl = f_gridPrice(i + 1, activeLower, activeUpper, gridLevelsInput, gridModeInput)
            bool held = array.get(levelHeld, i)
            // SELL first: a held lot whose paired level was touched this bar
            if held and high >= sellLvl
                float q = array.get(levelQty, i)
                strategy.close("GL" + str.tostring(i), qty = q, comment = "Grid Sell L" + str.tostring(i), alert_message = f_alertMessage2("SELL_LEVEL_TRIGGERED", i, sellLvl, "sell", q))
                array.set(levelHeld, i, false)
                array.set(levelQty, i, 0.0)
                sellsThisBar += 1
                sellTriggered := true
                sellTriggerLevel := sellLvl
            // BUY: touched from above (low reached level), price came from above, not already held
            else if not held and canBuyBar and low <= buyLvl and nz(close[1], close) > buyLvl and currentEntryCount + buysThisBar < allowedEntryCap and f_validQty(buyOrderQty, close)
                strategy.entry("GL" + str.tostring(i), strategy.long, qty = buyOrderQty, comment = "Grid Buy L" + str.tostring(i), alert_message = f_alertMessage2("BUY_LEVEL_TRIGGERED", i, buyLvl, "buy", buyOrderQty))
                array.set(levelHeld, i, true)
                array.set(levelQty, i, buyOrderQty)
                buysThisBar += 1
                buyTriggered := true
                buyTriggerLevel := buyLvl
bool buyActionTriggered = buysThisBar > 0
```
Notes:
* With `process_orders_on_close = true` the simulated fill is the bar **close** (+slippage), not the level. On a gap the fill can be far from the level. That is deliberately conservative and honest about gap risk. To simulate resting limit orders instead, use `strategy.entry(..., limit = buyLvl)` and move the `levelHeld` update to a fill check (`strategy.opentrades` delta).
* Sells are evaluated before buys, so a level is never bought and sold on the same bar.
* Remove `strategy.close_all` on generic up-crosses (original 258-259).

### FIX-10: Gap-safe, state-based hard stop / TP with fire-once (R2, R17) — replaces lines 239-240 and 252-263
```pine
var bool riskFired = false
bool inPos = strategy.position_size > 0.0
bool stopTriggered = barstate.isconfirmed and inPos and not riskFired and low <= stopLevel
bool takeProfitTriggered = barstate.isconfirmed and inPos and not riskFired and high >= takeProfitLevel and not stopTriggered
// Resting protective orders on every open lot (gap through stop fills at the open in the broker emulator)
if inPos
    for i = 0 to MAX_GRID_LEVELS - 1
        if array.get(levelHeld, i)
            strategy.exit("HR" + str.tostring(i), from_entry = "GL" + str.tostring(i), stop = stopLevel, limit = takeProfitLevel, alert_message = f_alertMessage2("HARD_RISK_EXIT", i, stopLevel, "close", array.get(levelQty, i)))
if (stopTriggered or takeProfitTriggered) and inPos
    strategy.close_all(comment = stopTriggered ? "Grid Stop" : "Grid Take Profit", alert_message = f_alertMessage2(stopTriggered ? "STOP_LOSS_HIT" : "TAKE_PROFIT_HIT", -1, stopTriggered ? stopLevel : takeProfitLevel, "close", strategy.position_size))
    riskFired := true
    for i = 0 to MAX_GRID_LEVELS - 1
        array.set(levelHeld, i, false)
        array.set(levelQty, i, 0.0)
if barstate.isconfirmed and not inPos
    riskFired := false
```
FIX-05 anchors `stopLevel`/`takeProfitLevel` to the anchored grid, so they no longer trail price. Note that `stopTriggered`/`takeProfitTriggered` are referenced by `canBuyBar` in FIX-09, so declare FIX-10's two `bool`s **before** FIX-09's loop.

### FIX-11: Alert payload without placeholders + unique, dedupe-friendly IDs (R5, R8, R20) — replaces `f_alertMessage` (84-93)
```pine
f_alertMessage2(string _event, int _level, float _price, string _side, float _qty) =>
    string lvl = _level >= 0 ? str.tostring(_level) : "NA"
    // Deterministic ID: same event on same bar/level/grid always produces the same ID -> receiver dedupes idempotently
    string sigId = alertPrefixInput + "_" + syminfo.tickerid + "_" + timeframe.period + "_" + str.tostring(time) + "_E" + str.tostring(gridEpoch) + "_L" + lvl + "_" + _event
    string px  = str.tostring(nz(_price), format.mintick)
    string qty = str.tostring(nz(_qty), "#.########")
    alertFormatInput == "JSON" ?
         "{\"secret\":\"" + webhookSecretInput + "\",\"source\":\"" + alertPrefixInput + "\",\"event\":\"" + _event + "\",\"bot_signal_id\":\"" + sigId + "\",\"ticker\":\"" + syminfo.tickerid + "\",\"tf\":\"" + timeframe.period + "\",\"bar_time\":" + str.tostring(time) + ",\"bar_close_time\":" + str.tostring(time_close) + ",\"grid_epoch\":" + str.tostring(gridEpoch) + ",\"grid_level\":\"" + lvl + "\",\"level_price\":\"" + px + "\",\"close\":\"" + str.tostring(close, format.mintick) + "\",\"side\":\"" + _side + "\",\"qty\":\"" + qty + "\",\"lower\":\"" + str.tostring(activeLower, format.mintick) + "\",\"upper\":\"" + str.tostring(activeUpper, format.mintick) + "\"}" :
         alertPrefixInput + "|event=" + _event + "|bot_signal_id=" + sigId + "|ticker=" + syminfo.tickerid + "|tf=" + timeframe.period + "|level=" + lvl + "|price=" + px + "|side=" + _side + "|qty=" + qty
```
Use `str.tostring(time)` (bar open, stable) rather than `timenow`. That way the ID is identical if TradingView ever re-sends the alert, and the receiver can safely drop repeats. `f_alertMessage2` reads `gridEpoch`/`activeLower`, which are globals, so define it after FIX-05 or pass them in as parameters.

### FIX-12: Single alert channel + per-bar/per-level fire-once (R6, R7) — replaces lines 265-293
Choose **one** channel:
* **Option A (recommended): order-fill alerts.** Keep the `alert_message` on every order (FIX-09/10). In TradingView create one alert: Condition = this strategy, "Order fills only". Message body = `{{strategy.order.alert_message}}`. Delete all `alert()` calls for order events.
* **Option B: `alert()` only.** Remove `alert_message` from orders and use the block below.

Either way, keep `alert()` for **non-order** events (boundary, rebuild) and remove all `alertcondition()` lines (283-293). They do nothing in strategies.
```pine
var int lastBoundaryAlertBar = -1
if alertsEnabledInput and barstate.isconfirmed and bar_index != lastBoundaryAlertBar
    if upperBreakout and enableBoundaryAlertInput
        alert(f_alertMessage2("UPPER_BOUNDARY_BREAKOUT", -1, boundaryUpperBeforeRebuild, "warning", 0.0), alert.freq_once_per_bar_close)
    if lowerBreakdown and enableBoundaryAlertInput
        alert(f_alertMessage2("LOWER_BOUNDARY_BREAKDOWN", -1, boundaryLowerBeforeRebuild, "warning", 0.0), alert.freq_once_per_bar_close)
    if rebalanceTriggered and enableRebalanceAlertInput
        alert(f_alertMessage2("GRID_RANGE_REBUILT", -1, close, "rebalance", 0.0), alert.freq_once_per_bar_close)
    if gapBar and inPos
        alert(f_alertMessage2("GAP_WARNING", -1, open, "warning", strategy.position_size), alert.freq_once_per_bar_close)
    lastBoundaryAlertBar := bar_index
```
Why these are not duplicated on realtime ticks: `alert.freq_once_per_bar_close` plus the `barstate.isconfirmed` gate run the block once per bar. `var` state changed on unconfirmed realtime ticks is rolled back by the runtime, and every state mutation here sits under `barstate.isconfirmed`. The `levelHeld` array prevents a level from re-firing until its paired sell resets it. The deterministic `bot_signal_id` lets the receiver drop anything that slips through (e.g. alert re-creation or a server retry).

### FIX-13: Dashboard additions (cost transparency)
```pine
// extra row: cost breakeven vs spacing (education display only)
table.cell(dashboardTable, 0, 9, "Spacing vs cost breakeven", text_color = dashboardTextColorInput, bgcolor = dashboardColorInput, text_size = size.tiny)
table.cell(dashboardTable, 1, 9, str.tostring(spacingPercent, "#.##") + "% / " + str.tostring(breakevenSpacingPct, "#.##") + "%", text_color = spacingCoversCosts ? supportColorInput : resistanceColorInput, bgcolor = dashboardColorInput, text_size = size.tiny)
table.cell(dashboardTable, 0, 10, "Data / Liquidity", text_color = dashboardTextColorInput, bgcolor = dashboardColorInput, text_size = size.tiny)
table.cell(dashboardTable, 1, 10, not enoughHistory ? "WARMUP" : not liquidityOk ? "THIN" : "OK", text_color = dataOk ? supportColorInput : resistanceColorInput, bgcolor = dashboardColorInput, text_size = size.tiny)
```
Size the table to 11 rows: `table.new(position.top_right, 2, 11, ...)`.

### FIX-14: Repainting checklist (R23)
* All state mutations and orders gated by `barstate.isconfirmed`. Already true for signals; FIX-05 extends it to the grid anchor.
* No `request.security` used. If one is added, use `request.security(sym, tf, expr[1], lookahead = barmerge.lookahead_on)` (the confirmed-HTF pattern).
* Grid lines are drawn from anchored `var` levels, so they no longer move on the live bar.
* Keep `calc_on_every_tick = false` and `calc_on_order_fills = false` (the defaults) to avoid backtest/realtime divergence.

---
*Education only. These changes make the model more conservative and transparent. They do not imply any expected return or likelihood of profit.*

---
## Merge status (added after `grid-bot-improved.pine` was marked final)

**Already covered by the improved draft:** R1/R2 (frozen grid, rebuilt only after invalidation), R3/R4 (one entry ID per level, exit at the adjacent level, `f_isOpen` blocks a second fill on the same level, so a gap fills each level once), R5 (no placeholders in `alert()`), R7 (alertcondition removed), R13 (capital, fees, slippage, margin, next-bar fills), R14 (no `ta.*` calls in branches), R15 (float division, range validity checks), R17 (resting stop beyond range plus range-break close), R22, R23.

**Added in `grid-bot-improved-merged.pine`:**
- [MERGE-A] Volatility spike filter: ATR(14)/SMA(ATR,100) > 1.8 or bar range > 2.5×ATR(14) blocks new entries and grid builds, with a 6-bar cooldown.
- [MERGE-B] Circuit breaker: counts consecutive losing closed trades with `strategy.closedtrades.profit()` and tracks equity drawdown from its peak. A streak of 4 or a drawdown of 10% pauses entries, builds and entry/build alerts for 24 bars and sends one `"action":"paused"` webhook (with `reason`). Also adds `strategy.risk.max_drawdown(20, strategy.percent_of_equity)` as a hard stop.
- [MERGE-C] Levels rounded to the tick size (R9). Quantity rounded to the lot step, with a min-notional check (R10). Warm-up guard (R16), liquidity floor and spread proxy (R18), and skipping entries on gap bars (R19). A funding input is included for reference (R12).
- [MERGE-D] Deterministic `alert_id` = `ticker_barOpenTime_action_level` in every payload (R8). Extra fields are ignored by `alert-logger.gs` and stored in `raw_json`.
- Status table rows and plotshapes for spike, data and pause states.
- `grid-screener-merged.pine`: coins that spiked within the cooldown get score -2 and are excluded from the alert and shown as "spike". An `alert_id` was added to the screener payload.

Kept on purpose during a pause: exit, range-break and edge-exit orders and alerts, so open risk can still be closed.
Not merged: FIX-09/10 (the draft's per-level engine already covers them) and FIX-11's full payload reshape (kept the logger-compatible schema).
