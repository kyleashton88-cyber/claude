"""Figures for Arty's four-week plan. Educational model only.

Live Pionex fees, spreads, maintenance margin, minimum size and the
liquidation prices on the preview override every planning assumption here.
The build inserts these strings into the PDF so the prose cannot drift.
"""

from __future__ import annotations

EQUITY = 500.0
DEPOSIT = 4_500.0
# Worked deposit case: trading result is zero, so equity becomes 5,000.
# If the screen shows a different equity, the plan says to recompute.
EQUITY_AFTER = EQUITY + DEPOSIT

MARGIN_PCT = 0.10
PHASE_PCT = 0.05
STOP_PCT = 0.08
TP_PCT = 0.048
WEEKLY_PCT = 0.03
WINDOW_PCT = 0.06
SOFT_PCT = 0.10
HARD_PCT = 0.15
RISK_CAP = 0.01

FEE_PER_SIDE = 0.0005  # 0.05% of the order, planning assumption
SPREAD = 0.0002  # 0.02% of price, planning assumption
MMR = 0.005  # 0.50% maintenance margin, planning assumption

EXAMPLE_MID = 3_000.0
EXAMPLE_HALF_WIDTH = 0.055  # 11% of mid, split either side
EXAMPLE_INTERVALS = 12
EXAMPLE_ATR = 60.0  # USDT, illustrative daily ATR(14)

LOWER = EXAMPLE_MID * (1 - EXAMPLE_HALF_WIDTH)  # 2,835
UPPER = EXAMPLE_MID * (1 + EXAMPLE_HALF_WIDTH)  # 3,165
SPAN = UPPER - LOWER  # 330
STEP = SPAN / EXAMPLE_INTERVALS  # 27.5


def money(value: float, digits: int = 2) -> str:
    return f"{value:,.{digits}f}"


def pct(fraction: float, digits: int = 2) -> str:
    return f"{fraction * 100:.{digits}f}%"


def liq_distance(leverage: float, mmr: float = MMR) -> float:
    """Adverse price fraction for a fully built isolated position."""
    return (1.0 / leverage) - mmr


def long_liq(entry: float, leverage: float, mmr: float = MMR) -> float:
    return entry * (1.0 - 1.0 / leverage + mmr)


def short_liq(entry: float, leverage: float, mmr: float = MMR) -> float:
    return entry * (1.0 + 1.0 / leverage - mmr)


def grid_step_percents(lower: float, upper: float, intervals: int) -> list[float]:
    step = (upper - lower) / intervals
    return [step / (lower + i * step) * 100 for i in range(intervals)]


def assert_plan() -> None:
    assert LOWER == 2_835
    assert UPPER == 3_165
    assert SPAN == 330
    assert STEP == 27.5

    margin = EQUITY * MARGIN_PCT
    stop = margin * STOP_PCT
    tp = margin * TP_PCT
    assert margin == 50
    assert stop == 4
    assert abs(tp - 2.4) < 1e-9
    assert abs(MARGIN_PCT * STOP_PCT - 0.008) < 1e-12
    assert MARGIN_PCT * STOP_PCT <= RISK_CAP
    assert abs(EQUITY * WEEKLY_PCT - 15) < 1e-9
    assert abs(EQUITY * WINDOW_PCT - 30) < 1e-9
    assert abs(EQUITY * SOFT_PCT - 50) < 1e-9
    assert abs(EQUITY * HARD_PCT - 75) < 1e-9
    assert 3 * stop == 12
    assert 4 * stop == 16
    assert 12 <= 15 < 16

    assert EQUITY_AFTER == 5_000
    assert EQUITY_AFTER * WEEKLY_PCT == 150
    assert EQUITY_AFTER * WINDOW_PCT == 300
    assert EQUITY_AFTER * SOFT_PCT == 500
    assert EQUITY_AFTER * HARD_PCT == 750
    assert EQUITY_AFTER * PHASE_PCT == 250
    assert EQUITY_AFTER * MARGIN_PCT == 500
    assert 250 * STOP_PCT == 20
    assert 500 * STOP_PCT == 40
    assert abs(20 / EQUITY_AFTER - 0.004) < 1e-12
    assert abs(40 / EQUITY_AFTER - 0.008) < 1e-12

    # A supposed exchange minimum that fails the 1% cap.
    assert abs(70 * STOP_PCT - 5.6) < 1e-9
    assert 5.6 > EQUITY * RISK_CAP

    assert abs(long_liq(EXAMPLE_MID, 3) - 2_015) < 1e-6
    assert abs(short_liq(EXAMPLE_MID, 3) - 3_985) < 1e-6
    assert abs(long_liq(EXAMPLE_MID, 5) - 2_415) < 1e-6
    assert abs(short_liq(EXAMPLE_MID, 5) - 3_585) < 1e-6
    assert abs(liq_distance(3) * 100 - (100 / 3 - 0.5)) < 1e-9
    assert abs(liq_distance(5) * 100 - 19.5) < 1e-9
    assert abs(EXAMPLE_MID * STOP_PCT / 3 - 80) < 1e-9
    assert abs(EXAMPLE_MID * STOP_PCT / 5 - 48) < 1e-9

    assert abs(LOWER * 0.97 - 2_749.95) < 1e-9
    assert abs(UPPER * 1.03 - 3_259.95) < 1e-9
    assert long_liq(EXAMPLE_MID, 3) <= LOWER * 0.97
    assert short_liq(EXAMPLE_MID, 3) >= UPPER * 1.03
    assert long_liq(EXAMPLE_MID, 5) <= LOWER * 0.97
    assert short_liq(EXAMPLE_MID, 5) >= UPPER * 1.03

    third = SPAN / 3
    assert third == 110
    assert LOWER + third == 2_945
    assert UPPER - third == 3_055

    steps = grid_step_percents(LOWER, UPPER, EXAMPLE_INTERVALS)
    worst = min(steps)
    # Smallest percent on an arithmetic grid is the top band.
    assert steps[-1] == worst
    assert abs(worst - (27.5 / 3_137.5 * 100)) < 1e-9

    round_trip = (2 * FEE_PER_SIDE + SPREAD) * 100  # 0.12
    assert abs(round_trip - 0.12) < 1e-12
    net = worst - round_trip
    assert net > 0.30
    assert worst > 0.50

    notional = margin * 3 / EXAMPLE_INTERVALS
    assert notional == 12.5
    gross_usd = notional * (worst / 100)
    cost_usd = notional * (2 * FEE_PER_SIDE + SPREAD)
    net_usd = gross_usd - cost_usd
    assert abs(cost_usd - 0.015) < 1e-12
    assert abs(gross_usd - 0.10956175298804781) < 1e-9
    assert abs(net_usd - 0.09456175298804781) < 1e-9

    # Example ATR filter: ETH floor 11% binds, and 11% is under the 8×ATR max.
    atr_pct = EXAMPLE_ATR / EXAMPLE_MID  # 0.02
    eth_min = max(0.11, 4 * atr_pct)
    width_max = 8 * atr_pct
    width = SPAN / EXAMPLE_MID
    assert abs(atr_pct - 0.02) < 1e-12
    assert eth_min == 0.11
    assert abs(width_max - 0.16) < 1e-12
    assert eth_min <= width <= width_max

    # Swing marks used by the range diagram.
    assert 2_865 - 0.5 * EXAMPLE_ATR == LOWER
    assert 3_135 + 0.5 * EXAMPLE_ATR == UPPER

    # Outer 10% of the example range, used by the volume close.
    assert LOWER + 0.1 * SPAN == 2_868
    assert UPPER - 0.1 * SPAN == 3_132

    # Deposit does not change a trading result of zero into a profit.
    assert (EQUITY_AFTER - (EQUITY + DEPOSIT)) == 0

    # Two full stops at the starter size.
    assert 2 * stop == 8
    assert abs(8 / EQUITY - 0.016) < 1e-12


def context() -> dict[str, str]:
    """Display strings. Run assert_plan() before trusting them."""
    assert_plan()
    margin = EQUITY * MARGIN_PCT
    stop = margin * STOP_PCT
    tp = margin * TP_PCT
    steps = grid_step_percents(LOWER, UPPER, EXAMPLE_INTERVALS)
    worst = min(steps) / 100
    round_trip = 2 * FEE_PER_SIDE + SPREAD
    net = worst - round_trip
    notional = margin * 3 / EXAMPLE_INTERVALS
    gross_usd = notional * worst
    cost_usd = notional * round_trip
    net_usd = gross_usd - cost_usd
    atr_pct = EXAMPLE_ATR / EXAMPLE_MID

    return {
        "equity": money(EQUITY),
        "deposit": money(DEPOSIT),
        "equity_after": money(EQUITY_AFTER),
        "margin": money(margin),
        "stop_usd": money(stop),
        "tp_usd": money(tp),
        "stop_share": pct(stop / EQUITY),
        "tp_share": pct(tp / EQUITY),
        "weekly": money(EQUITY * WEEKLY_PCT),
        "window": money(EQUITY * WINDOW_PCT),
        "soft": money(EQUITY * SOFT_PCT),
        "hard": money(EQUITY * HARD_PCT),
        "stops_three": money(3 * stop),
        "stops_four": money(4 * stop),
        "two_bots": money(2 * stop),
        "two_bots_share": pct(2 * stop / EQUITY),
        "risk_cap": money(EQUITY * RISK_CAP),
        "after_weekly": money(EQUITY_AFTER * WEEKLY_PCT),
        "after_window": money(EQUITY_AFTER * WINDOW_PCT),
        "after_soft": money(EQUITY_AFTER * SOFT_PCT),
        "after_hard": money(EQUITY_AFTER * HARD_PCT),
        "phase_margin": money(EQUITY_AFTER * PHASE_PCT),
        "phase_stop": money(EQUITY_AFTER * PHASE_PCT * STOP_PCT),
        "phase_share": pct(PHASE_PCT * STOP_PCT),
        "full_margin": money(EQUITY_AFTER * MARGIN_PCT),
        "full_stop": money(EQUITY_AFTER * MARGIN_PCT * STOP_PCT),
        "full_share": pct(MARGIN_PCT * STOP_PCT),
        "mid": money(EXAMPLE_MID, 0),
        "lower": money(LOWER, 0),
        "upper": money(UPPER, 0),
        "step": money(STEP),
        "span": money(SPAN, 0),
        "worst_gross": pct(worst, 3),
        "round_trip": pct(round_trip, 3),
        "net_step": pct(net, 3),
        "notional": money(notional),
        "gross_grid": f"{gross_usd:.4f}",
        "cost_grid": f"{cost_usd:.4f}",
        "net_grid": f"{net_usd:.4f}",
        "liq3_long": money(long_liq(EXAMPLE_MID, 3)),
        "liq3_short": money(short_liq(EXAMPLE_MID, 3)),
        "liq5_long": money(long_liq(EXAMPLE_MID, 5)),
        "liq5_short": money(short_liq(EXAMPLE_MID, 5)),
        "dist3": pct(liq_distance(3)),
        "dist5": pct(liq_distance(5)),
        "move3": pct(STOP_PCT / 3),
        "move5": pct(STOP_PCT / 5),
        "move3_usd": money(EXAMPLE_MID * STOP_PCT / 3, 0),
        "move5_usd": money(EXAMPLE_MID * STOP_PCT / 5, 0),
        "buf_low": money(LOWER * 0.97),
        "buf_high": money(UPPER * 1.03),
        "third_low": money(LOWER + SPAN / 3, 0),
        "third_high": money(UPPER - SPAN / 3, 0),
        "outer_low": money(LOWER + 0.1 * SPAN, 0),
        "outer_high": money(UPPER - 0.1 * SPAN, 0),
        "spread_px": money(EXAMPLE_MID * 0.0008),
        "depth": money(20 * notional),
        "fee_side": pct(FEE_PER_SIDE),
        "spread_assumed": pct(SPREAD),
        "mmr": pct(MMR),
        "half_range": pct(EXAMPLE_HALF_WIDTH),
        "half_usd": money(EXAMPLE_MID * EXAMPLE_HALF_WIDTH, 0),
        "atr": money(EXAMPLE_ATR, 0),
        "atr_pct": pct(atr_pct),
        "atr_4x": pct(4 * atr_pct),
        "atr_8x": pct(8 * atr_pct),
        "swing_low": "2,865",
        "swing_high": "3,135",
        "min_fail": money(70 * STOP_PCT),
        "min_example": "70.00",
    }


if __name__ == "__main__":
    data = context()
    for key in sorted(data):
        print(f"{key:16} {data[key]}")
