"""15 Nov trend and room-to-stop gate. The squeeze tests and the old long-window tests stay as they are."""
import importlib.util
import math
from pathlib import Path

import numpy as np
import pandas as pd

_path = Path(__file__).resolve().parent / "select.py"
_spec = importlib.util.spec_from_file_location("market_check_select_gate", _path)
select = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(select)


def test_gate_constants():
    assert select.TREND_DRIFT30_MIN == 0.8
    assert select.TREND_ADX14_MIN == 40
    assert select.ROOM_ABOVE_STOP_MIN == 0.08
    assert select.EXAMPLE_LEVEL_BARS == 90
    # One source of truth: the named cuts are the screen.py constants.
    assert select.TREND_DRIFT30_MIN is select.screen.TREND_DRIFT30_MIN
    assert select.TREND_ADX14_MIN is select.screen.TREND_ADX14_MIN
    assert select.ROOM_ABOVE_STOP_MIN is select.screen.ROOM_ABOVE_STOP_MIN
    assert select.trend_skip is select.screen.trend_skip
    assert select.room_skip is select.screen.room_skip
    assert select.skip_reasons_from_facts is select.screen.skip_reasons_from_facts


def test_trend_cut_is_strict_and_needs_both():
    adx_above = math.nextafter(40, math.inf)
    drift_above = math.nextafter(0.8, math.inf)
    assert select.trend_skip(0.8, adx_above) is False
    assert select.trend_skip(math.nextafter(0.8, 0.0), adx_above) is False
    assert select.trend_skip(drift_above, 40) is False
    assert select.trend_skip(drift_above, math.nextafter(40, 0.0)) is False
    assert select.trend_skip(drift_above, adx_above) is True
    assert select.trend_skip(0.97, 30) is False
    assert select.trend_skip(0.5, 55) is False


def test_room_cut_is_strict():
    stop = 100.0
    exact = stop * (1 + select.ROOM_ABOVE_STOP_MIN)
    assert select.room_above_stop(exact, stop) == select.ROOM_ABOVE_STOP_MIN
    assert select.room_skip(exact, stop) is False
    assert select.room_skip(math.nextafter(exact, 0.0), stop) is True
    assert select.room_skip(math.nextafter(exact, math.inf), stop) is False
    assert select.room_skip(stop, stop) is True  # price sitting on the stop
    assert select.room_skip(stop * 0.99, stop) is True


def test_either_reason_skips_and_both_are_logged():
    trend_only = select.skip_reasons_from_facts(0.91, 46.0, 120.0, 100.0)
    assert len(trend_only) == 1 and trend_only[0].startswith("trend:")
    room_only = select.skip_reasons_from_facts(0.2, 10.0, 105.0, 100.0)
    assert len(room_only) == 1 and room_only[0].startswith("room-to-stop:")
    both = select.skip_reasons_from_facts(0.91, 46.0, 105.0, 100.0)
    assert len(both) == 2
    assert select.skip_reasons_from_facts(0.8, 40.0, 108.0, 100.0) == []


def test_drift30_is_win_close_range_not_high_low():
    # Close moves 10. High-low span is 20, so the retired drift would be 0.5.
    # D uses win(): absolute close move / 5th-to-95th close range, plus that window's ADX.
    close = np.linspace(100.0, 110.0, 30)
    high = close + 5.0
    low = close - 5.0
    frame = pd.DataFrame({"open": close, "high": high, "low": low, "close": close})
    high_low = abs(float(close[-1]) - float(close[0])) / (float(high.max()) - float(low.min()))
    assert high_low == 0.5
    win_drift = select.win(frame)[3]
    assert win_drift != high_low
    drift, adx14 = select.drift_adx30(frame)
    assert drift == win_drift
    assert adx14 == select.win(frame)[4]
    assert not hasattr(select, "trend_drift30")


def test_range_not_active_does_not_reprint_the_range():
    levels = select._range_fields(100.0, 140.0, 90.0, stop=96.0)
    hidden = select.present_big_four("BTC", levels, 90.0, 96.0)
    assert hidden["status"] == "range not active"
    assert hidden["now"] == 90.0
    for key in ("bottom", "top", "entry", "exit", "stop", "optimal", "grids", "width"):
        assert key not in hidden
    shown = select.present_big_four("ETH", levels, 110.0, 96.0)
    assert shown["status"] == "active"
    assert shown["bottom"] == 100.0
    assert shown["top"] == 140.0
    assert shown["stop"] == 96.0


def test_regime_gate_is_the_screen_rule():
    assert select.screen.REGIME_DRIFT30_MIN == 1.0
    assert select.screen.REGIME_ADX14_MIN == 35
    out = select.screen.evaluate_market(
        1.35, 37.3,
        [{"coin": "BTC", "last_close": 90.0, "stop": 100.0}],
        [{"coin": "DOGE", "drift30": 0.2, "adx14": 10.0, "last_close": 120.0, "stop": 100.0}],
    )
    assert out["regime"] is True
    assert out["picks"] == []
    assert out["four"][0]["status"] == "range not active"
    assert select.screen.btc_regime_blocks_rotation(1.0, 37.3) is False
    assert select.screen.btc_regime_blocks_rotation(1.35, 35) is False


def test_example_stop_uses_the_90_day_window():
    old = pd.DataFrame({
        "open": np.full(60, 11.0), "high": np.full(60, 12.0),
        "low": np.full(60, 10.0), "close": np.full(60, 11.0),
    })
    new = pd.DataFrame({
        "open": np.full(30, 52.0), "high": np.full(30, 55.0),
        "low": np.full(30, 50.0), "close": np.full(30, 52.0),
    })
    frame = pd.concat([old, new], ignore_index=True)
    levels = select.example_levels(frame)
    window = frame.tail(select.EXAMPLE_LEVEL_BARS)
    bottom = float(np.percentile(window.low, 5)) * 0.99
    assert levels["bottom"] == bottom
    assert levels["stop"] == bottom * 0.96
    recent = float(np.percentile(frame.tail(30).low, 5)) * 0.99
    assert levels["bottom"] != recent
