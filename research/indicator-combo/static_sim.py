"""Static-range grid, sized on a fixed bot budget.

The range and the level prices are computed once, from ATR or Bollinger at
the launch bar, and they do not move. The bot keeps them until the hard
stop, the hard take-profit, or N closes outside the band, then it may
launch again. That is the exchange pattern: a range is set when the bot
starts, not rewritten from every new close.

The whole bot budget is reserved for the buy levels that sit below the
launch price, equal quote notional each, scaled so the entry fees fit.
A filled buy targets the next level up. Nothing is sold below the price
that was paid, except a stop, a hard take-profit, or an outside-bar exit.
Those exits are the stop-out cost.

exit_mode:
- per_level: sell each lot at the next level
- close_all: the first target touch sells the whole inventory
- trail: after price has cleared the average cost, a one-step pullback sells the book
- above_avg: per-level sells only while the target is above the average cost
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from engine import Params, grid_price, prepare, raw_range


@dataclass
class StaticParams:
    mode: str = "Arithmetic"
    levels: int = 8
    method: str = "Bollinger Bands"
    min_spacing_pct: float = 2.0
    min_spacing_atr: float = 1.0
    stop_pct: float = 2.0
    tp_pct: float = 2.0
    outside_bars: int = 3
    exit_mode: str = "per_level"
    bot_capital: float = 10_000.0
    fee: float = 0.001
    slip: float = 0.0005
    auto_length: int = 50
    atr_length: int = 14
    atr_mult: float = 2.0
    bb_length: int = 20
    bb_mult: float = 2.0
    auto_max_dist: float = 25.0


def _engine_params(p: StaticParams) -> Params:
    return Params(
        mode=p.mode, levels=p.levels, method=p.method,
        min_spacing_pct=p.min_spacing_pct, min_spacing_atr=p.min_spacing_atr,
        stop_pct=p.stop_pct, tp_pct=p.tp_pct, regrid_bars=p.outside_bars,
        auto_length=p.auto_length, atr_length=p.atr_length, atr_mult=p.atr_mult,
        bb_length=p.bb_length, bb_mult=p.bb_mult, auto_max_dist=p.auto_max_dist,
    )


def level_prices(lower, upper, levels, mode):
    return [grid_price(i, lower, upper, levels, mode) for i in range(levels)]


def step_pct(prices):
    steps = [(b / a) - 1.0 for a, b in zip(prices, prices[1:]) if a > 0]
    if not steps:
        return 0.01
    return max(0.002, float(sum(steps) / len(steps)))


def simulate_static(t, o, h, l, c, p: StaticParams, mintick, allow, funding=None, prepared=None):
    n = len(c)
    ind = prepared if prepared is not None else prepare(o, h, l, c, _engine_params(p))
    ep = _engine_params(p)
    if funding is None:
        funding = np.zeros(n)
    if allow is None:
        allow = np.ones(n, dtype=bool)
    bb_mid, bb_up, bb_lo = ind["bb"]

    cash = p.bot_capital
    # lots: qty, limit or fill price, target, opened
    lots = []
    frozen = None
    equity = np.empty(n)
    deployments = []
    cycles = []
    offset = 0.0
    peak = None
    saw_fill = False

    def opened_lots():
        return [lot for lot in lots if lot[3]]

    def inventory():
        return sum(q for q, _e, _t, opened in lots if opened)

    def avg_cost():
        q = inventory()
        if q <= 0:
            return None
        return sum(qty * entry for qty, entry, _t, opened in lots if opened) / q

    def mark(px):
        return cash + inventory() * px * (1.0 - p.fee)

    def finish(reason, bar, px):
        nonlocal cash, lots, frozen, offset, peak, saw_fill
        held = opened_lots()
        for qty, entry, _tgt, _opened in held:
            fee = qty * px * p.fee
            entry_fee = qty * entry * p.fee
            pnl_lot = qty * (px - entry) - entry_fee - fee
            cycles.append({"bar": bar, "t": int(t[bar]), "pnl": pnl_lot, "reason": reason,
                           "entry": entry, "exit": px, "qty": qty})
            cash += qty * px - fee
        pnl = cash - p.bot_capital
        if frozen is not None and saw_fill:
            deployments.append({
                "t": int(t[frozen[6]]), "i": frozen[6], "end": bar, "pnl": pnl,
                "ret": pnl / p.bot_capital, "reason": reason,
            })
            offset += pnl
        cash = p.bot_capital
        lots = []
        frozen = None
        peak = None
        saw_fill = False

    for i in range(n):
        exited = False
        if inventory() and funding[i] != 0.0:
            cash -= inventory() * c[i] * funding[i]
        if frozen is not None:
            lo_f, hi_f, stop, tp, prices, outside, start_i = frozen
            stopped = l[i] <= stop
            tp_hit = h[i] >= tp
            if stopped or tp_hit:
                down_first = (o[i] - l[i]) <= (h[i] - o[i])
                if o[i] <= stop:
                    px, reason = o[i] * (1.0 - p.slip), "stop"
                elif o[i] >= tp and not stopped:
                    px, reason = o[i], "tp"
                elif stopped and tp_hit and down_first:
                    px, reason = stop * (1.0 - p.slip), "stop"
                elif stopped and tp_hit:
                    px, reason = tp, "tp"
                elif stopped:
                    px, reason = stop * (1.0 - p.slip), "stop"
                else:
                    px, reason = tp, "tp"
                finish(reason, i, px)
                exited = True
            else:
                # Buy limits. An unfilled lot's price is the limit.
                updated = []
                for qty, entry, target, opened in lots:
                    if opened or l[i] > entry:
                        updated.append((qty, entry, target, opened))
                        continue
                    fill = o[i] if o[i] < entry else entry
                    cost = qty * fill * (1.0 + p.fee)
                    if cost <= cash + 1e-6:
                        cash -= cost
                        updated.append((qty, fill, target, True))
                        saw_fill = True
                    else:
                        updated.append((qty, entry, target, False))
                lots = updated
                if p.exit_mode == "close_all":
                    touched = [target for qty, entry, target, opened in lots if opened and h[i] >= target]
                    if touched and inventory() > 0:
                        finish("sell", i, min(touched))
                        exited = True
                elif p.exit_mode == "trail":
                    avg = avg_cost()
                    if avg is not None and h[i] > avg:
                        peak = h[i] if peak is None else max(peak, h[i])
                    if peak is not None and avg is not None and inventory() > 0:
                        trail = peak * (1.0 - step_pct(prices))
                        if trail > avg and l[i] <= trail:
                            fill = o[i] * (1.0 - p.slip) if o[i] < trail else trail
                            finish("trail", i, fill)
                            exited = True
                else:
                    kept = []
                    avg = avg_cost()
                    for qty, entry, target, opened in lots:
                        sell = opened and h[i] >= target
                        if p.exit_mode == "above_avg":
                            sell = sell and avg is not None and target > avg
                        if sell:
                            fee = qty * target * p.fee
                            cash += qty * target - fee
                            entry_fee = qty * entry * p.fee
                            cycles.append({"bar": i, "t": int(t[i]), "pnl": qty * (target - entry) - entry_fee - fee,
                                           "reason": "sell", "entry": entry, "exit": target, "qty": qty})
                        else:
                            kept.append((qty, entry, target, opened))
                    lots = kept
                if not exited and frozen is not None:
                    outside = outside + 1 if (c[i] > hi_f or c[i] < lo_f) else 0
                    frozen = (lo_f, hi_f, stop, tp, prices, outside, start_i)
                    if outside >= p.outside_bars:
                        finish("outside", i, c[i] * (1.0 - p.slip))
                        exited = True
                    elif not lots or (not opened_lots() and not any(not lot[3] for lot in lots)):
                        finish("complete", i, c[i])
                        exited = True
        if exited:
            frozen = None
        if frozen is None and allow[i] and not exited and i > 0:
            lo, hi, _ceil = raw_range(c[i], ind["ema"][i], ind["atr"][i], bb_lo[i], bb_up[i], ep, mintick)
            if hi > lo > 0:
                prices = level_prices(lo, hi, p.levels, p.mode)
                below = [k for k in range(p.levels - 1) if prices[k] < c[i] - mintick]
                if len(below) >= 1:
                    notional = p.bot_capital / len(below) / (1.0 + p.fee)
                    lots = [(notional / prices[k], prices[k], prices[k + 1], False) for k in below]
                    stop = min(lo - mintick, lo * (1.0 - p.stop_pct / 100.0))
                    tp = max(hi + mintick, hi * (1.0 + p.tp_pct / 100.0))
                    frozen = (lo, hi, stop, tp, prices, 0, i)
                    cash = p.bot_capital
                    peak = None
        open_pnl = (mark(c[i]) - p.bot_capital) if frozen is not None else 0.0
        equity[i] = p.bot_capital + offset + open_pnl

    open_pnl = (mark(c[-1]) - p.bot_capital) if frozen is not None else 0.0
    return {"equity": equity, "deployments": deployments, "cycles": cycles, "open_pnl": open_pnl, "bars": n}


def wilson(wins, n, z=1.96):
    if n <= 0:
        return None, None
    p = wins / n
    den = 1.0 + z * z / n
    centre = (p + z * z / (2 * n)) / den
    margin = z * ((p * (1 - p) / n + z * z / (4 * n * n)) ** 0.5) / den
    return max(0.0, centre - margin), min(1.0, centre + margin)
