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


def test_drift30_is_net_move_over_high_low_range():
    # Close moves 10. High-low range is 20. drift30 = 0.5.
    # The win() drift uses the close percentile range and is a different number.
    close = np.linspace(100.0, 110.0, 30)
    high = close + 5.0
    low = close - 5.0
    # First bar low is 95, last bar high is 115, but the running band is 10 wide
    # only if each bar's high/low stay next to its close. Span is max high - min low
    # = 115 - 95 = 20. Net move = 10. drift = 0.5.
    frame = pd.DataFrame({"open": close, "high": high, "low": low, "close": close})
    assert select.trend_drift30(frame) == 0.5
    win_drift = select.win(frame)[3]
    assert win_drift != select.trend_drift30(frame)


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
