"""Elite Intel picks screen: gates D and F (Stewart approved 22 Nov 2026, 6:10pm AEDT).

D and F use the same 30-day win() factors as the weekly review
(research/week_2026_11_22.py): drift30 is the absolute close-to-close move
divided by the 5th-to-95th close range, and ADX14 is computed on that
same 30-bar window. That is what made BTC 1.35 / 37.3 on 15 Nov, and it
is what F needs — the high-low-range drift in PR 10 would have been
0.81 on that day and would not have tripped the 1.0 regime cut.

These functions are the live screen for 8AM/4PM Market Check runs.
Import them from this module; do not hand-pick rotation coins.
"""
from __future__ import annotations

# --- D: 30-day trend and floor-proximity gate (rotation picks only) ---
TREND_DRIFT30_MIN = 0.8
TREND_ADX14_MIN = 40
ROOM_ABOVE_STOP_MIN = 0.08

# --- F: market-regime gate and big-four "range not active" label ---
REGIME_DRIFT30_MIN = 1.0
REGIME_ADX14_MIN = 35
RANGE_NOT_ACTIVE = "range not active"
BIG_FOUR = ("BTC", "ETH", "SOL", "XRP")


def trend_skip(drift30, adx14):
    """D trend leg: drop when drift30 > 0.8 AND ADX14 > 40. Both cuts are strict."""
    return drift30 > TREND_DRIFT30_MIN and adx14 > TREND_ADX14_MIN


def room_above_stop(price, stop):
    if not stop or stop <= 0:
        return float("inf")
    return (price - stop) / stop


def room_skip(price, stop):
    """D floor leg: drop when price is less than 8% above the example stop."""
    return room_above_stop(price, stop) < ROOM_ABOVE_STOP_MIN


def skip_reasons_from_facts(drift30, adx14, price, stop):
    """D reasons to drop a rotation pick. Empty means this coin may stay (subject to F)."""
    reasons = []
    if trend_skip(drift30, adx14):
        reasons.append(
            f"trend: drift30 {drift30:.4f} > {TREND_DRIFT30_MIN} and ADX14 {adx14:.2f} > {TREND_ADX14_MIN}"
        )
    if room_skip(price, stop):
        room = room_above_stop(price, stop)
        reasons.append(
            f"room-to-stop: price {price:.6g} is {room:.2%} above stop {stop:.6g}, under {ROOM_ABOVE_STOP_MIN:.0%}"
        )
    return reasons


def btc_regime_blocks_rotation(drift30, adx14):
    """F regime gate: when BTC itself is trending, publish no rotation picks.

    True when BTC drift30 > 1.0 AND BTC ADX14 > 35. Both cuts are strict.
    """
    return drift30 > REGIME_DRIFT30_MIN and adx14 > REGIME_ADX14_MIN


def is_range_not_active(last_close, stop):
    """F presentation: a big-four example is not in play when the latest
    completed daily close is below its example stop."""
    return last_close < stop


def format_big_four_line(coin, price, status, range_position=None, invalidation=None):
    """Education-only one-liner for POST_TEMPLATE.md big-four bullets.

    When status is RANGE_NOT_ACTIVE, do not reprint the old example range.
    """
    if status == RANGE_NOT_ACTIVE:
        return (
            f"{coin} ${price}: range not active. The latest completed daily close "
            f"is below the example invalidation, so the previous example range is "
            f"not in play. Education only. Not financial advice."
        )
    pos = range_position or "relative to"
    inv = f"; example invalidation {invalidation}" if invalidation else ""
    return f"{coin} ${price}: {pos} its example range{inv}."


def evaluate_market(btc_drift30, btc_adx14, big_four, rotation):
    """Apply F then D and return the edition's rotation picks and big-four statuses.

    big_four / rotation: iterable of dicts with at least
      coin, last_close, stop, and (for rotation) drift30, adx14, plus any
      extra fields to pass through (score, now, ...).

    Returns a dict:
      regime: bool
      regime_reason: str | None
      picks: list of rotation dicts that cleared D (empty when regime is on)
      skipped: list of {coin, reasons, **row}
      four: list of rows with status 'range not active' or 'active'
    """
    regime = btc_regime_blocks_rotation(btc_drift30, btc_adx14)
    regime_reason = None
    if regime:
        regime_reason = (
            f"BTC trending: drift30 {btc_drift30:.4f} > {REGIME_DRIFT30_MIN} "
            f"and ADX14 {btc_adx14:.2f} > {REGIME_ADX14_MIN}; no rotation picks"
        )

    skipped = []
    kept = []
    if not regime:
        for row in rotation:
            reasons = skip_reasons_from_facts(
                row["drift30"], row["adx14"], row["last_close"], row["stop"]
            )
            if reasons:
                skipped.append({**row, "reasons": reasons})
            else:
                kept.append(dict(row))

    four = []
    for row in big_four:
        item = dict(row)
        if is_range_not_active(row["last_close"], row["stop"]):
            item["status"] = RANGE_NOT_ACTIVE
        else:
            item["status"] = "active"
        four.append(item)

    return {
        "regime": regime,
        "regime_reason": regime_reason,
        "picks": [] if regime else kept,
        "skipped": skipped if not regime else [{**row, "reasons": [regime_reason]} for row in rotation],
        "four": four,
    }

