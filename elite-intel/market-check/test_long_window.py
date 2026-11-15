"""Boundary tests for the long-window rescue guard (review C) and the A+C regression."""
import importlib.util
import math
from pathlib import Path

import numpy as np
import pandas as pd

_path = Path(__file__).resolve().parent / "select.py"
_spec = importlib.util.spec_from_file_location("market_check_select_c", _path)
select = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(select)

DRIFT30_GUARD_MIN = select.DRIFT30_GUARD_MIN
ADX14_GUARD_MIN = select.ADX14_GUARD_MIN
LONG_MID_GAP_MIN = select.LONG_MID_GAP_MIN
LONG_WINDOW_WEIGHT = select.LONG_WINDOW_WEIGHT
long_window_weight = select.long_window_weight
composite_score = select.composite_score
is_squeeze = select.is_squeeze
win = select.win


def _weight(drift, adx, long, mid):
    return long_window_weight(drift, adx, long, mid)


def test_guard_constants():
    assert DRIFT30_GUARD_MIN == 0.8
    assert ADX14_GUARD_MIN == 40
    assert LONG_MID_GAP_MIN == 15
    assert LONG_WINDOW_WEIGHT == 0.4


def test_each_guard_cut_is_strict():
    mid = 20.0
    long_above = mid + LONG_MID_GAP_MIN  # exactly +15 does not fire
    drift_above = math.nextafter(DRIFT30_GUARD_MIN, math.inf)
    adx_above = math.nextafter(ADX14_GUARD_MIN, math.inf)
    long_just_above = math.nextafter(long_above, math.inf)

    assert _weight(DRIFT30_GUARD_MIN, adx_above, long_just_above, mid) == 0.4
    assert _weight(math.nextafter(DRIFT30_GUARD_MIN, 0.0), adx_above, long_just_above, mid) == 0.4
    assert _weight(drift_above, adx_above, long_just_above, mid) == 0.0

    assert _weight(drift_above, ADX14_GUARD_MIN, long_just_above, mid) == 0.4
    assert _weight(drift_above, math.nextafter(ADX14_GUARD_MIN, 0.0), long_just_above, mid) == 0.4
    assert _weight(drift_above, adx_above, long_just_above, mid) == 0.0

    assert _weight(drift_above, adx_above, long_above, mid) == 0.4
    assert _weight(drift_above, adx_above, math.nextafter(long_above, 0.0), mid) == 0.4
    assert _weight(drift_above, adx_above, long_just_above, mid) == 0.0


def test_zero_weight_is_not_renormalized():
    mid, long, liq = 29.3, 53.5, 0.7
    score = composite_score(mid, long, liq, 0.0)
    kept = composite_score(mid, long, liq, 0.4)
    assert score == 0.5 * mid + 10 * liq
    assert kept == 0.5 * mid + 0.4 * long + 10 * liq
    assert score != 0.9 * mid + 10 * liq


def test_nov8_review_excludes_xlm_and_keeps_doge_and_shib():
    # Factors from the 8 Nov review table (win() as of 31 Oct).
    xlm = dict(drift=0.97, adx=46.9, long=53.5, mid=29.3)
    doge = dict(drift=0.92, adx=47.9, long=16.5, mid=29.4)
    shib = dict(drift=0.95, adx=54.2, long=28.3, mid=18.7)
    assert _weight(xlm["drift"], xlm["adx"], xlm["long"], xlm["mid"]) == 0.0
    assert _weight(doge["drift"], doge["adx"], doge["long"], doge["mid"]) == 0.4
    assert _weight(shib["drift"], shib["adx"], shib["long"], shib["mid"]) == 0.4

    liq = 0.75  # shared, so the window terms decide the order
    sx = composite_score(xlm["mid"], xlm["long"], liq, 0.0)
    sd = composite_score(doge["mid"], doge["long"], liq, 0.4)
    ss = composite_score(shib["mid"], shib["long"], liq, 0.4)
    assert sx < sd and sx < ss
    # Putting the discarded 0.4 onto the mid weight would leave XLM ahead of both.
    renorm = 0.9 * xlm["mid"] + 10 * liq
    assert renorm > sd and renorm > ss


def test_regression_coins_outside_a_and_c_match_the_old_formula():
    coins = [
        dict(width30=0.22, width180=0.40, drift30=0.50, adx14=20.0, mid=50.0, long=40.0, liq=0.70),
        # Exactly on the C cuts. Strict inequalities leave the old 0.4 weight in place.
        dict(width30=0.30, width180=0.45, drift30=0.8, adx14=40.0, mid=33.0, long=48.0, liq=0.20),
        # Gap of exactly 15, with drift and ADX already through their cuts.
        dict(width30=0.18, width180=0.40, drift30=0.95, adx14=55.0, mid=40.0, long=55.0, liq=0.50),
        # Just clear of the squeeze floor and the one-third ratio.
        dict(width30=0.06, width180=0.12, drift30=0.2, adx14=10.0, mid=22.0, long=22.0, liq=0.40),
    ]
    for c in coins:
        assert is_squeeze(c["width30"], c["width180"]) is False
        weight = _weight(c["drift30"], c["adx14"], c["long"], c["mid"])
        assert weight == 0.4
        legacy = 0.5 * c["mid"] + 0.4 * c["long"] + 10 * c["liq"]
        assert composite_score(c["mid"], c["long"], c["liq"], weight) == legacy


def test_regression_through_win_on_a_coin_that_trips_neither_rule():
    idx = np.arange(180)
    close = 100 + 12 * np.sin(2 * np.pi * idx / 18.0)
    frame = pd.DataFrame({"open": close, "high": close + 0.4, "low": close - 0.4, "close": close})
    m = win(frame.tail(30))
    long = win(frame)
    assert not is_squeeze(m[2], long[2])
    assert long_window_weight(m[3], m[4], long[0], m[0]) == LONG_WINDOW_WEIGHT
    liq = 0.42
    legacy = 0.5 * m[0] + 0.4 * long[0] + 10 * liq
    got = composite_score(m[0], long[0], liq, long_window_weight(m[3], m[4], long[0], m[0]))
    assert got == legacy
