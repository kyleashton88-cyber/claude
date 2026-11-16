"""The PDF gate stays shut unless every required out-of-sample cell clears 75%."""
import json
from pathlib import Path

from pdf_gate import COINS, LEVERAGES, MODES, TIMEFRAMES, evaluate

ROOT = Path(__file__).resolve().parent


def _payload(win=0.80, n=40):
    cells = []
    for mode in MODES:
        for coin in COINS:
            for tf in TIMEFRAMES:
                for lev in LEVERAGES:
                    cells.append({
                        "mode": mode, "coin": coin, "tf": tf, "leverage": lev,
                        "win": win, "n": n, "fees_included": True,
                    })
    return {
        "fees_included": True,
        "window": ["2026-05-16", "2026-11-15"],
        "win_definition": "per_deployment_net_of_fees",
        "cells": cells,
    }


def test_full_grid_at_75_opens():
    assert evaluate(_payload(0.75, 20)) == []


def test_one_cell_under_75_closes():
    payload = _payload()
    payload["cells"][0]["win"] = 0.749
    failures = evaluate(payload)
    assert any("below 75%" in line for line in failures)


def test_small_n_closes_even_at_100():
    payload = _payload(1.0, 10)
    failures = evaluate(payload)
    assert failures
    assert all("below 20" in line for line in failures)


def test_missing_leverage_closes():
    payload = _payload()
    payload["cells"] = [c for c in payload["cells"] if not (c["leverage"] == 5 and c["mode"] == "Geometric")]
    failures = evaluate(payload)
    assert any("Geometric" in line and "5x" in line and "missing" in line for line in failures)


def test_builders_call_the_gate():
    for name in ("build_guide.py", "build_pass2_pdf.py"):
        text = (ROOT / name).read_text()
        assert "assert_pdf_allowed()" in text


if __name__ == "__main__":
    test_full_grid_at_75_opens()
    test_one_cell_under_75_closes()
    test_small_n_closes_even_at_100()
    test_missing_leverage_closes()
    test_builders_call_the_gate()
    print("pdf gate checks passed")
