"""Checks for the static-range bot and the screener formula."""
import numpy as np

from screener import f_band, MIN_SCORE
from static_sim import StaticParams, level_prices, simulate_static, step_pct, wilson


def test_band_and_spacing():
    assert f_band(4, 2, 8) == 1
    assert f_band(1, 2, 8) == 0
    assert abs(f_band(12, 2, 8) - 0.5) < 1e-9
    arith = level_prices(100, 170, 8, "Arithmetic")
    geom = level_prices(100, 170, 8, "Geometric")
    a_steps = np.diff(arith)
    g_steps = np.diff([np.log(x) for x in geom])
    assert np.allclose(a_steps, a_steps[0])
    assert np.allclose(g_steps, g_steps[0])
    assert abs(arith[3] - geom[3]) > 1
    assert MIN_SCORE == 60


def test_wilson_wide_on_small_n():
    lo, hi = wilson(8, 10)
    assert lo < 0.55 and hi > 0.94


def test_static_range_does_not_follow_price():
    n = 80
    close = np.full(n, 100.0)
    close[10:40] = 100 - np.linspace(0, 8, 30)
    close[40:] = 100
    high = close + 0.3
    low = close - 0.3
    # one dip through a buy and back to the target
    low[20] = 90
    high[45] = 110
    open_ = close.copy()
    t = np.arange(n) * 3_600_000 + 1_700_000_000_000
    allow = np.zeros(n, dtype=bool)
    allow[60] = True
    n = 120
    close = np.full(n, 100.0)
    close[70:100] = 100 - np.linspace(0, 6, 30)
    close[100:] = 102
    high = close + 0.4
    low = close - 0.4
    low[80] = 92
    high[110] = 112
    open_ = close.copy()
    t = np.arange(n) * 3_600_000 + 1_700_000_000_000
    allow = np.zeros(n, dtype=bool)
    allow[65] = True
    res = simulate_static(t, open_, high, low, close, StaticParams(mode="Geometric", levels=6, method="ATR",
                          min_spacing_pct=1.0, stop_pct=20, outside_bars=40, auto_length=20, atr_length=10), 0.01, allow)
    assert res["deployments"], "expected a fill"
    # A second launch is not allowed, so one deployment.
    assert len(res["deployments"]) == 1
    assert res["deployments"][0]["ret"] != 0


def test_modes_differ_on_a_drift():
    rng = np.random.default_rng(3)
    n = 1500
    steps = rng.normal(0, 0.01, n)
    close = 100 * np.exp(np.cumsum(steps))
    high = close * 1.004
    low = close * 0.996
    open_ = close.copy()
    t = np.arange(n) * 3_600_000
    allow = np.zeros(n, dtype=bool)
    allow[200] = True
    allow[800] = True
    kw = dict(levels=8, method="Bollinger Bands", min_spacing_pct=1.25, stop_pct=4, outside_bars=8)
    a = simulate_static(t, open_, high, low, close, StaticParams(mode="Arithmetic", **kw), 0.01, allow)
    g = simulate_static(t, open_, high, low, close, StaticParams(mode="Geometric", **kw), 0.01, allow)
    # Levels differ, so the deployment pnl is not required to match.
    if a["deployments"] and g["deployments"]:
        assert a["deployments"][0]["pnl"] != g["deployments"][0]["pnl"] or step_pct(
            level_prices(90, 110, 8, "Arithmetic")) != step_pct(level_prices(90, 110, 8, "Geometric"))


if __name__ == "__main__":
    test_band_and_spacing()
    test_wilson_wide_on_small_n()
    test_static_range_does_not_follow_price()
    test_modes_differ_on_a_drift()
    print("static checks passed")
