# Live Elite Intel picks screen (D and F)

Stewart approved tweaks D and F on 22 Nov 2026 at 6:10pm AEDT. The live implementation is `research/screen.py`. 8AM and 4PM Market Check runs must import it when choosing rotation picks and when wording the big-four lines. Do not hand-pick rotation coins, and do not copy an older work-*/write_*.py `PICKS = [...]` list without running this screen.

The older 58-line `select.py` copies (for example `2026-11-15-am/select.py`) and each `work-*/build.py` only score coins. They do not apply D or F. PR 10 (`https://github.com/kyleashton88-cyber/claude/pull/10`) holds an earlier unmerged A+D+E copy in `elite-intel/market-check/select.py` that is **not** what the AM/PM research runs call.

## Gates

- **D** — drop a rotation pick when `drift30 > 0.8` and `ADX14 > 40`, **or** when the last completed daily close is less than 8% above its example stop.
- **F** — when BTC's own `drift30 > 1.0` and `ADX14 > 35`, publish no rotation picks. Any big-four coin (BTC, ETH, SOL, XRP) whose latest completed daily close is below its example stop is labelled **"range not active"** instead of reprinting the old example range.

`drift30` and `ADX14` are the 30-day `win()` factors from the weekly review (close move over the 5th-to-95th close range, ADX on that same 30-bar window), not the high-low-range drift used in an earlier PR 10 draft.

Thresholds are named constants in `screen.py`. Existing informal 90-day filters (width, midline crosses, 90-day drift, volume) still apply before D and F.

## How an AM/PM run should call it

After `build.py` has `data.json` (and after 30-day `win()` factors are known for BTC and for each rotation candidate):

```python
from screen import evaluate_market, format_big_four_line, RANGE_NOT_ACTIVE, BIG_FOUR

out = evaluate_market(btc_drift30, btc_adx14, four_rows, rotation_rows)
PICKS = [p["coin"] for p in out["picks"]]
# For each item in out["four"], if status == RANGE_NOT_ACTIVE, use
# format_big_four_line(coin, price, status) in the post text. Do not
# publish the retired bottom/top/enter/stop as live example levels.
```

`run_current_screen.py` is a one-shot check against the latest `data.json` plus fresh Pionex dailies. Post text follows `../POST_TEMPLATE.md`. Education only. Not financial advice. Every level is an example.

Backups taken 22 Nov 2026 before this change:

- `POST_TEMPLATE.md.bak-2026-11-22-df`
- `research/work-2026-11-22-pm/build.py.bak-2026-11-22-df`
- `research/work-2026-11-22-pm/write_pm.py.bak-2026-11-22-df`
- `2026-11-15-am/select.py.bak-2026-11-22-df`

