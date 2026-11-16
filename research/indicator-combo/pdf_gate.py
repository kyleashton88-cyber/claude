"""Refuse to build a guide PDF until every required out-of-sample cell clears 75%.

Stewart, 16 Nov 2026, 1:22pm WITA: do not generate or update
GridBot_Master_Strategy_Guide.pdf until both Arithmetic and Geometric
are at or above 75% per-deployment win rate on the untouched window
(16 May 2026 through 15 Nov 2026), on BTC, ETH, SOL and ZEC, with fees,
at every leverage that this study is required to test (1x, 2x, 3x and 5x),
on both 1h and 4h.

A cell with fewer than 20 deployments does not clear the gate, even if
its point estimate is above 75%. A missing cell does not clear the gate.

The results file is results/oos_gate.json. Exit code 0 means the PDF may
be built. Exit code 2 means it may not. This script does not write a PDF.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "results" / "oos_gate.json"

MODES = ("Arithmetic", "Geometric")
COINS = ("BTC-USDT", "ETH-USDT", "SOL-USDT", "ZEC-USDT")
TIMEFRAMES = ("1h", "4h")
LEVERAGES = (1, 2, 3, 5)
MIN_WIN = 0.75
MIN_N = 20
OOS_START = "2026-05-16"
OOS_END = "2026-11-15"

COIN_ALIAS = {
    "BTC": "BTC-USDT", "ETH": "ETH-USDT", "SOL": "SOL-USDT", "ZEC": "ZEC-USDT",
    "BTCUSDT": "BTC-USDT", "ETHUSDT": "ETH-USDT", "SOLUSDT": "SOL-USDT", "ZECUSDT": "ZEC-USDT",
}


def _coin(value):
    text = str(value).upper().replace("_", "-")
    return COIN_ALIAS.get(text, text)


def _num_leverage(value):
    if isinstance(value, str) and value.endswith("x"):
        value = value[:-1]
    return int(value)


def required_keys():
    keys = []
    for mode in MODES:
        for coin in COINS:
            for tf in TIMEFRAMES:
                for lev in LEVERAGES:
                    keys.append((mode, coin, tf, lev))
    return keys


def evaluate(payload):
    """Return a list of failure strings. An empty list means the gate is open."""
    failures = []
    if not isinstance(payload, dict):
        return ["results file must be a JSON object"]
    if payload.get("fees_included") is not True:
        failures.append("fees_included is not true")
    window = payload.get("window") or []
    if list(window) != [OOS_START, OOS_END]:
        failures.append(f"window must be {[OOS_START, OOS_END]}, got {window}")
    if payload.get("win_definition") not in (None, "per_deployment_net_of_fees"):
        failures.append("win_definition must be per_deployment_net_of_fees")
    found = {}
    for cell in payload.get("cells") or []:
        try:
            key = (
                cell["mode"],
                _coin(cell.get("coin") or cell.get("inst")),
                cell["tf"],
                _num_leverage(cell["leverage"]),
            )
        except (KeyError, TypeError, ValueError) as exc:
            failures.append(f"unreadable cell: {exc}")
            continue
        found[key] = cell
    for key in required_keys():
        cell = found.get(key)
        label = f"{key[0]} {key[1]} {key[2]} {key[3]}x"
        if cell is None:
            failures.append(f"missing {label}")
            continue
        if cell.get("fees_included", payload.get("fees_included")) is not True:
            failures.append(f"{label}: fees not included")
        n = cell.get("n")
        win = cell.get("win")
        if n is None or int(n) < MIN_N:
            failures.append(f"{label}: n={n} is below {MIN_N}")
            continue
        if win is None or float(win) < MIN_WIN:
            shown = "missing" if win is None else f"{float(win):.1%}"
            failures.append(f"{label}: win rate {shown} is below 75% (n={int(n)})")
    return failures


def assert_pdf_allowed(path=None):
    """Stop a PDF build. Raises SystemExit(2) unless every required cell passes."""
    path = Path(path) if path else RESULTS
    print("PDF gate: checking", path)
    if not path.exists():
        print("PDF gate CLOSED. No out-of-sample gate file yet.")
        print("A guide PDF is not built until Arithmetic and Geometric are")
        print("at or above 75% per deployment, net of fees, on BTC, ETH, SOL")
        print("and ZEC, at 1x, 2x, 3x and 5x, on 1h and 4h, for 16 May 2026")
        print("through 15 Nov 2026, with at least 20 deployments in every cell.")
        raise SystemExit(2)
    payload = json.loads(path.read_text())
    failures = evaluate(payload)
    if failures:
        print(f"PDF gate CLOSED. {len(failures)} cell(s) block the guide.")
        for line in failures[:40]:
            print(" -", line)
        if len(failures) > 40:
            print(f" - ... {len(failures) - 40} more")
        raise SystemExit(2)
    print("PDF gate open. Every required out-of-sample cell is at or above 75%.")
    return True


if __name__ == "__main__":
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else RESULTS
    try:
        assert_pdf_allowed(target)
    except SystemExit as exc:
        sys.exit(exc.code)
