"""Frozen example levels: bottom, stop and range stay until a pick is dropped and re-added."""
import importlib.util
from pathlib import Path

_path = Path(__file__).resolve().parent / "select.py"
_spec = importlib.util.spec_from_file_location("market_check_select_freeze", _path)
select = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(select)


def _fresh(bottom, top, now):
    return select._range_fields(bottom, top, now, stop=bottom * 0.96)


def test_live_pick_keeps_bottom_stop_and_range():
    state = select.empty_levels_state()
    first = _fresh(1.0, 2.0, 1.4)
    published = select.publish_levels(state, "DOGE", first, "2026-11-08")
    assert published["bottom"] == 1.0
    assert published["top"] == 2.0
    assert published["stop"] == 1.0 * 0.96
    assert published["now"] == 1.4
    assert state["picks"]["DOGE"]["2026-11-08"]["active"] is True

    later = _fresh(1.5, 3.0, 1.9)
    again = select.publish_levels(state, "DOGE", later, "2026-11-15")
    assert again["bottom"] == 1.0
    assert again["top"] == 2.0
    assert again["stop"] == first["stop"]
    assert again["entry"][0] == 1.0
    assert again["exit"][1] == 2.0
    assert again["now"] == 1.9
    assert list(state["picks"]["DOGE"]) == ["2026-11-08"]


def test_drop_then_readd_gets_fresh_levels_under_a_new_date():
    state = select.empty_levels_state()
    select.publish_levels(state, "XLM", _fresh(0.15, 0.23, 0.17), "2026-11-08")
    select.mark_dropped(state, set())
    assert state["picks"]["XLM"]["2026-11-08"]["active"] is False

    fresh = _fresh(0.20, 0.30, 0.22)
    republished = select.publish_levels(state, "XLM", fresh, "2026-11-20")
    assert republished["bottom"] == 0.20
    assert republished["top"] == 0.30
    assert republished["stop"] == fresh["stop"]
    assert state["picks"]["XLM"]["2026-11-20"]["active"] is True
    assert state["picks"]["XLM"]["2026-11-08"]["active"] is False


def test_a_coin_that_stays_live_is_not_dropped():
    state = select.empty_levels_state()
    select.publish_levels(state, "BTC", _fresh(60_000, 80_000, 70_000), "2026-11-08")
    select.publish_levels(state, "SOL", _fresh(70, 120, 90), "2026-11-08")
    select.mark_dropped(state, {"BTC"})
    assert state["picks"]["BTC"]["2026-11-08"]["active"] is True
    assert state["picks"]["SOL"]["2026-11-08"]["active"] is False


def test_state_file_roundtrip(tmp_path):
    path = tmp_path / "levels_state.json"
    state = select.empty_levels_state()
    select.publish_levels(state, "ETH", _fresh(1800, 2700, 2200), "2026-11-08")
    select.save_levels_state(path, state)
    loaded = select.load_levels_state(path)
    assert loaded["picks"]["ETH"]["2026-11-08"]["bottom"] == 1800
    assert loaded["picks"]["ETH"]["2026-11-08"]["stop"] == 1800 * 0.96
    assert select.load_levels_state(tmp_path / "missing.json") == {"picks": {}}
