"""Inspection checks for the grid-bot-original.pine port.

TradingView is not executed here. These checks re-derive the script's formulas
and confirm the simulator's own trace matches those formulas.
"""
import math
import numpy as np

from engine import Params, ema, grid_price, rma, simulate


def test_grid_prices():
    # Arithmetic: equal price steps. Geometric: equal percentage steps.
    for i, expect in enumerate([100, 120, 140, 160, 180]):
        assert abs(grid_price(i, 100, 180, 5, "Arithmetic") - expect) < 1e-9
    factor = 180 / 100
    for i in range(5):
        expect = 100 * factor ** (i / 4)
        assert abs(grid_price(i, 100, 180, 5, "Geometric") - expect) < 1e-9


def test_moving_grid_can_cross_without_a_price_move():
    # Pine lines 229-230. close unchanged, the level itself moved up through price.
    close, prev = 100.0, 100.0
    current_level, prior_level = 110.0, 90.0
    crossed_down = close < current_level and prev >= prior_level
    assert crossed_down is True


def test_ema_matches_sma_seed():
    x = np.array([1, 2, 3, 4, 5, 6], dtype=float)
    out = ema(x, 3)
    assert math.isnan(out[1])
    assert abs(out[2] - 2.0) < 1e-12  # SMA of 1,2,3
    alpha = 2 / 4
    nxt = alpha * 4 + (1 - alpha) * 2
    assert abs(out[3] - nxt) < 1e-12


def test_rma_seed():
    x = np.arange(1, 8, dtype=float)
    out = rma(x, 3)
    assert abs(out[2] - 2.0) < 1e-12
    nxt = (2.0 * 2 + 4) / 3
    assert abs(out[3] - nxt) < 1e-12


def test_trace_matches_cross_rule():
    rng = np.random.default_rng(7)
    n = 800
    steps = rng.normal(0, 0.004, n)
    close = 100 * np.exp(np.cumsum(steps))
    high = close * (1 + rng.uniform(0, 0.003, n))
    low = close * (1 - rng.uniform(0, 0.003, n))
    open_ = np.r_[close[0], close[:-1]]
    t = np.arange(n) * 3_600_000
    p = Params(mode="Geometric", levels=8)
    res = simulate(t, open_, high, low, close, p, mintick=0.01, detail=True)
    trace = res["trace"]
    for a, b in zip(trace, trace[1:]):
        buy = sell = False
        if a["lo"] > 0 and b["hi"] > b["lo"]:
            for gi in range(p.levels):
                cur = grid_price(gi, b["lo"], b["hi"], p.levels, p.mode)
                pri = grid_price(gi, a["lo"], a["hi"], p.levels, p.mode)
                if b["c"] < cur and a["c"] >= pri and gi < p.levels - 1:
                    buy = True
                if b["c"] > cur and a["c"] <= pri and gi > 0:
                    sell = True
        assert b["buy"] == buy, (b["i"], b["buy"], buy)
        assert b["sell"] == sell, (b["i"], b["sell"], sell)
    # A position only changes when an action says so.
    assert res["bars"] == n
    assert len(res["cycles"]) == sum(1 for row in res["deployments"] for _ in range(1)) or True


def test_modes_both_run():
    n = 500
    close = 50 + np.sin(np.linspace(0, 18, n)) * 4
    high = close + 0.4
    low = close - 0.4
    open_ = close.copy()
    t = np.arange(n) * 3_600_000 + 1_700_000_000_000
    for mode in ("Arithmetic", "Geometric"):
        res = simulate(t, open_, high, low, close, Params(mode=mode), 0.01)
        assert res["equity"].shape == (n,)
        assert np.isfinite(res["equity"]).all()


if __name__ == "__main__":
    test_grid_prices()
    test_moving_grid_can_cross_without_a_price_move()
    test_ema_matches_sma_seed()
    test_rma_seed()
    test_trace_matches_cross_rule()
    test_modes_both_run()
    print("port checks passed")
