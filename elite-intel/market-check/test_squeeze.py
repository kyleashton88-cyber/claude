"""Boundary tests for the provisional squeeze hard-drop (review A only)."""
import importlib.util
import math
from pathlib import Path

# select.py shares its name with the stdlib select module, so load this file by path.
_path = Path(__file__).resolve().parent / "select.py"
_spec = importlib.util.spec_from_file_location("market_check_select", _path)
select = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(select)

SQUEEZE_WIDTH180_RATIO = select.SQUEEZE_WIDTH180_RATIO
SQUEEZE_WIDTH30_MIN = select.SQUEEZE_WIDTH30_MIN
composite_score = select.composite_score
is_squeeze = select.is_squeeze


def test_thresholds_are_the_named_constants():
    assert SQUEEZE_WIDTH30_MIN == 0.06
    assert SQUEEZE_WIDTH180_RATIO == 3


def test_width30_cut_is_strict_and_does_not_use_the_ratio():
    # width180/3 sits far below 6%, so only the absolute cut can fire.
    width180 = 0.06
    assert is_squeeze(0.06, width180) is False
    assert is_squeeze(math.nextafter(0.06, 0.0), width180) is True
    assert is_squeeze(math.nextafter(0.06, 1.0), width180) is False


def test_width_ratio_cut_is_strict_and_does_not_use_the_floor():
    width180 = 0.30
    third = width180 / SQUEEZE_WIDTH180_RATIO
    assert third > SQUEEZE_WIDTH30_MIN
    assert is_squeeze(third, width180) is False
    assert is_squeeze(math.nextafter(third, 0.0), width180) is True
    assert is_squeeze(math.nextafter(third, math.inf), width180) is False


def test_either_cut_drops_the_coin():
    assert is_squeeze(0.05, 0.05) is True  # under 6%; 0.05 is not under 0.05/3
    assert is_squeeze(0.10, 0.36) is True  # 0.10 < 0.12, and 0.10 is not under 6%
    assert is_squeeze(0.02, 0.30) is True  # both cuts
    assert is_squeeze(0.20, 0.30) is False


def test_trx_saved_widths_are_a_squeeze():
    # 24 Oct scores.csv: width30 0.024 (2.4%), width180 0.104 (10.4%).
    # The 1 Nov review describes that same coin as 2.4% over 30 days and ~9-10% over 90/180.
    assert is_squeeze(0.024, 0.104) is True
    assert 0.024 < SQUEEZE_WIDTH30_MIN
    assert 0.024 < 0.104 / SQUEEZE_WIDTH180_RATIO


def test_coin_outside_both_cuts_keeps_the_old_score():
    mid, long, liq = 56.8, 42.8, 0.55  # KAS-like factors; widths are not a squeeze
    assert is_squeeze(0.268, 0.487) is False
    assert composite_score(mid, long, liq) == 0.5 * mid + 0.4 * long + 10 * liq
