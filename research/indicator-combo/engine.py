"""Faithful port of indicators/tradingview/grid-bot-original.pine.

The script is a Pine v6 strategy, "Crypto Grid Bot Master Strategy & Alert System".
Arithmetic and Geometric are gridModeInput. This module follows that file's
order of operations, including the behaviour the independent review calls out:

- In Auto mode the active range is rewritten from the current close on every bar.
- One entry id is used. Any up-cross flattens the whole position (close_all).
- The loop keeps only the last crossed level on the bar.
- Hard stop and hard take-profit are recomputed from the latest range.
- Buys pause when ADX or EMA deviation is extended, and stay paused until
  rangeRecoveryBars consecutive in-range bars.

Approximations (no TradingView runtime in this study):

- Fills use bar OHLC. Resting stop/limit orders from the previous close are
  tested on the next bar. If both stop and take-profit sit inside the bar,
  the side closer to the open is assumed to trade first. A gap through the
  stop fills at the open, then slippage.
- Commission is 0.10% per side, the script's commission_value. Slippage is
  0.05% per side on market and stop fills. The script's slippage=1 tick is
  not used: on BTC one OKX tick is 0.1 against a price near 60,000, which is
  not a realistic fill. Take-profit limits fill at the limit with no extra slip.
- syminfo.mintick is the OKX spot tick size stored with the candles.
- strategy.equity for the risk cap is cash plus the open quantity marked at
  the close, minus an estimated exit fee.
- Decisions on a bar see the position after any intrabar stop or take-profit.
  Close orders then run in the script's order: trend exit, buy, sell-all,
  stop close, take-profit close. close_all flattens lots opened earlier on
  that same close.
- Indicator warm-up follows Pine: EMA and Bollinger seed with an SMA, ATR and
  ADX use Wilder RMA. Values before the seed are treated as na, and nz()
  matches the script.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
import math

import numpy as np


@dataclass
class Params:
    mode: str = "Arithmetic"          # Arithmetic | Geometric
    levels: int = 8
    min_spacing_pct: float = 1.25
    min_spacing_atr: float = 1.0
    method: str = "ATR"               # ATR | Bollinger Bands
    auto_length: int = 50
    atr_length: int = 14
    atr_mult: float = 2.0
    bb_length: int = 20
    bb_mult: float = 2.0
    auto_max_dist: float = 25.0
    order_qty: float = 1.0
    risk_pct: float = 1.0
    max_position: float = 10.0
    max_entries: int = 6
    stop_pct: float = 0.75
    tp_pct: float = 2.0
    use_trend: bool = True
    adx_length: int = 14
    adx_smooth: int = 14
    adx_threshold: float = 20.0
    trend_ema: int = 100
    max_ma_dev: float = 3.0
    recovery_bars: int = 4
    regrid_bars: int = 3
    # structure: moving = original; anchor = range kept until a flat rebuild;
    # per_level = anchor plus one lot per crossed level, exit at the next level.
    structure: str = "moving"
    use_drift_gate: bool = False
    use_vol_gate: bool = False
    initial_capital: float = 1_000_000.0
    fee: float = 0.001
    slip: float = 0.0005
    # 0 keeps the script's fixed order_qty. A positive value sizes each new
    # order to that fraction of marked equity. The cross and exit rules do not change.
    notional_pct: float = 0.0


def ema(x: np.ndarray, length: int) -> np.ndarray:
    out = np.full(len(x), np.nan)
    if len(x) < length or length < 1:
        return out
    alpha = 2.0 / (length + 1.0)
    seed = float(np.mean(x[:length]))
    out[length - 1] = seed
    prev = seed
    for i in range(length, len(x)):
        prev = alpha * x[i] + (1.0 - alpha) * prev
        out[i] = prev
    return out


def rma(x: np.ndarray, length: int) -> np.ndarray:
    out = np.full(len(x), np.nan)
    if len(x) < length or length < 1:
        return out
    seed = float(np.mean(x[:length]))
    out[length - 1] = seed
    prev = seed
    inv = 1.0 / length
    for i in range(length, len(x)):
        prev = prev + inv * (x[i] - prev)
        out[i] = prev
    return out


def atr(h, l, c, length: int) -> np.ndarray:
    n = len(c)
    tr = np.empty(n)
    tr[0] = h[0] - l[0]
    prev = c[:-1]
    tr[1:] = np.maximum(h[1:] - l[1:], np.maximum(np.abs(h[1:] - prev), np.abs(l[1:] - prev)))
    return rma(tr, length)


def bollinger(c, length: int, mult: float):
    n = len(c)
    mid = np.full(n, np.nan)
    upper = np.full(n, np.nan)
    lower = np.full(n, np.nan)
    if n < length:
        return mid, upper, lower
    csum = np.cumsum(c)
    c2 = np.cumsum(c * c)
    for i in range(length - 1, n):
        a = 0 if i + 1 == length else csum[i - length]
        b = 0.0 if i + 1 == length else c2[i - length]
        s = csum[i] - a
        q = c2[i] - b
        mean = s / length
        var = max(0.0, q / length - mean * mean)
        sd = math.sqrt(var)
        mid[i] = mean
        upper[i] = mean + mult * sd
        lower[i] = mean - mult * sd
    return mid, upper, lower


def dmi(h, l, c, di_len: int, adx_len: int):
    n = len(c)
    plus_dm = np.zeros(n)
    minus_dm = np.zeros(n)
    tr = np.zeros(n)
    tr[0] = h[0] - l[0]
    for i in range(1, n):
        up = h[i] - h[i - 1]
        down = l[i - 1] - l[i]
        plus_dm[i] = up if up > down and up > 0 else 0.0
        minus_dm[i] = down if down > up and down > 0 else 0.0
        tr[i] = max(h[i] - l[i], abs(h[i] - c[i - 1]), abs(l[i] - c[i - 1]))
    str_ = rma(tr, di_len)
    sp = rma(plus_dm, di_len)
    sm = rma(minus_dm, di_len)
    plus = np.full(n, np.nan)
    minus = np.full(n, np.nan)
    dx = np.full(n, np.nan)
    for i in range(n):
        if np.isnan(str_[i]) or str_[i] == 0:
            continue
        plus[i] = 100.0 * sp[i] / str_[i]
        minus[i] = 100.0 * sm[i] / str_[i]
        den = plus[i] + minus[i]
        dx[i] = 0.0 if den == 0 else 100.0 * abs(plus[i] - minus[i]) / den
    # ADX is an RMA of DX. Pine's ta.dmi seeds once enough DX values exist.
    adx = np.full(n, np.nan)
    buf = []
    prev = None
    inv = 1.0 / adx_len
    for i in range(n):
        if np.isnan(dx[i]):
            continue
        if prev is None:
            buf.append(dx[i])
            if len(buf) == adx_len:
                prev = float(sum(buf) / adx_len)
                adx[i] = prev
            continue
        prev = prev + inv * (dx[i] - prev)
        adx[i] = prev
    return plus, minus, adx


def grid_price(index: int, lower: float, upper: float, levels: int, mode: str) -> float:
    frac = index / float(levels - 1)
    if mode == "Geometric":
        return lower * (upper / lower) ** frac
    return lower + (upper - lower) * frac


def raw_range(close, ema_basis, atr_v, bb_lo, bb_hi, p: Params, mintick: float):
    safe_basis = close if (ema_basis is None or math.isnan(ema_basis)) else ema_basis
    atr_use = 0.0 if (atr_v is None or math.isnan(atr_v)) else atr_v
    atr_lo = safe_basis - atr_use * p.atr_mult
    atr_hi = safe_basis + atr_use * p.atr_mult
    if p.method == "Bollinger Bands" and bb_lo is not None and not math.isnan(bb_lo):
        sel_lo, sel_hi = bb_lo, bb_hi
    else:
        sel_lo, sel_hi = atr_lo, atr_hi
    auto_lo_floor = max(mintick, close * (1.0 - p.auto_max_dist / 100.0))
    auto_hi_ceil = max(close + mintick, close * (1.0 + p.auto_max_dist / 100.0))
    auto_lo_cand = max(mintick, max(auto_lo_floor, sel_lo))
    safe_lo = min(max(mintick, close - mintick), auto_lo_cand)
    auto_hi_cand = max(safe_lo + mintick, sel_hi)
    safe_hi = max(close + mintick, min(auto_hi_ceil, auto_hi_cand))
    atr_spacing = (atr_use * p.min_spacing_atr / safe_lo * 100.0) if safe_lo > 0 else 0.0
    required = max(p.min_spacing_pct, atr_spacing)
    if p.mode == "Geometric":
        expanded = max(safe_hi, safe_lo * (1.0 + required / 100.0) ** (p.levels - 1))
    else:
        step = max(mintick, safe_lo * required / 100.0)
        expanded = max(safe_hi, safe_lo + step * (p.levels - 1))
    effective_hi = max(safe_lo + mintick, min(auto_hi_ceil, expanded))
    return safe_lo, effective_hi, auto_hi_ceil


def prepare(o, h, l, c, p: Params):
    return {
        "ema": ema(c, p.auto_length),
        "atr": atr(h, l, c, p.atr_length),
        "bb": bollinger(c, p.bb_length, p.bb_mult),
        "adx": dmi(h, l, c, p.adx_length, p.adx_smooth)[2],
        "trend": ema(c, p.trend_ema),
    }


def _nz(x, fallback=0.0):
    if x is None or (isinstance(x, float) and math.isnan(x)):
        return fallback
    return float(x)


def simulate(t, o, h, l, c, p: Params, mintick: float, prepared=None,
             drift_block=None, vol_hot=None, funding=None, detail=False):
    n = len(c)
    ind = prepared if prepared is not None else prepare(o, h, l, c, p)
    ema_a = ind["ema"]
    atr_a = ind["atr"]
    bb_mid, bb_up, bb_lo = ind["bb"]
    adx_a = ind["adx"]
    trend_a = ind["trend"]
    if drift_block is None:
        drift_block = np.zeros(n, dtype=bool)
    if vol_hot is None:
        vol_hot = np.zeros(n, dtype=bool)
    if funding is None:
        funding = np.zeros(n)

    cash = p.initial_capital
    # lots: qty, entry fill, entry fee, level index or -1
    lots = []
    active_lo = None
    active_hi = None
    prev_lo = None
    prev_hi = None
    prev_stop = None
    prev_tp = None
    prev_strong = False
    outside = 0
    prev_outside = 0
    buys_paused = False
    range_bound = 0
    equity = np.empty(n)
    in_mkt = 0
    cycles = []
    deployments = []
    dep_open = None
    shadow = None
    shadow_stop = 0
    shadow_win = 0
    shadow_open = 0
    blocked = 0
    trace = [] if detail else None

    def mark(px):
        qty = sum(lot[0] for lot in lots)
        exit_fee = qty * px * p.fee
        return cash + qty * px - exit_fee

    def flatten(px, reason, bar):
        nonlocal cash, dep_open
        if not lots:
            return
        pnl_sum = 0.0
        n_closed = len(lots)
        for qty, entry, entry_fee, level in lots:
            fee = qty * px * p.fee
            pnl = qty * (px - entry) - entry_fee - fee
            cash += qty * px - fee
            pnl_sum += pnl
            cycles.append({"bar": bar, "t": int(t[bar]), "pnl": pnl, "reason": reason,
                           "entry": entry, "exit": px, "qty": qty, "level": level})
        lots.clear()
        if dep_open is not None:
            deployments.append({
                "bar": bar, "t": int(t[bar]),
                "pnl": pnl_sum + dep_open.get("pnl", 0.0),
                "reason": reason,
                "lots": dep_open.get("lots", 0) + n_closed,
                "start": dep_open["start"],
                "i": dep_open.get("i"),
                "adx": dep_open.get("adx"),
                "dev": dep_open.get("dev"),
                "eq0": dep_open.get("eq0") or 0.0,
            })
            dep_open = None

    for i in range(n):
        # Funding on an open long: positive rate is a cost (OKX sign).
        if lots and funding[i] != 0.0:
            qty = sum(lot[0] for lot in lots)
            cash -= qty * c[i] * funding[i]

        # Resting hard stop / take-profit from the previous close.
        if lots and prev_stop is not None:
            stop_hit = l[i] <= prev_stop
            tp_hit = h[i] >= prev_tp
            fill = None
            reason = None
            if stop_hit or tp_hit:
                down_first = (o[i] - l[i]) <= (h[i] - o[i])
                if o[i] <= prev_stop:
                    fill, reason = o[i] * (1.0 - p.slip), "stop"
                elif o[i] >= prev_tp:
                    fill, reason = o[i], "tp"
                elif stop_hit and tp_hit:
                    if down_first:
                        fill, reason = prev_stop * (1.0 - p.slip), "stop"
                    else:
                        fill, reason = prev_tp, "tp"
                elif stop_hit:
                    fill, reason = prev_stop * (1.0 - p.slip), "stop"
                else:
                    fill, reason = prev_tp, "tp"
            if fill is not None:
                flatten(fill, reason, i)

        if shadow is not None:
            if l[i] <= shadow["stop"]:
                shadow_stop += 1
                shadow = None
            elif c[i] >= shadow["target"]:
                shadow_win += 1
                shadow = None
            else:
                shadow_open += 1

        lo_raw, hi_raw, _ceil = raw_range(
            c[i], ema_a[i], atr_a[i], bb_lo[i], bb_up[i], p, mintick
        )
        if active_lo is None or p.structure == "moving":
            active_lo, active_hi = lo_raw, hi_raw

        outside_now = c[i] > active_hi or c[i] < active_lo
        outside = outside + 1 if outside_now else 0
        rebalance = outside >= p.regrid_bars and prev_outside < p.regrid_bars
        if rebalance:
            if p.structure == "moving":
                width = max(active_hi - active_lo, mintick)
                cand_lo = max(mintick, c[i] - width * 0.5)
                cand_hi = max(cand_lo + mintick, c[i] + width * 0.5)
                active_lo, active_hi = cand_lo, cand_hi
            elif not lots:
                active_lo, active_hi = lo_raw, hi_raw
            outside = 0

        adx_v = _nz(adx_a[i], 0.0)
        tema = trend_a[i]
        if tema is None or (isinstance(tema, float) and math.isnan(tema)) or tema == 0:
            dev = 0.0
        else:
            dev = abs(c[i] / tema - 1.0) * 100.0
        strong = adx_v >= p.adx_threshold or dev >= p.max_ma_dev
        if strong:
            buys_paused = True
            range_bound = 0
        else:
            inside = active_lo <= c[i] <= active_hi
            range_bound = range_bound + 1 if inside else 0
            if buys_paused and range_bound >= p.recovery_bars:
                buys_paused = False
        trend_blocked = p.use_trend and (strong or buys_paused)
        gate_blocked = (p.use_drift_gate and bool(drift_block[i])) or (p.use_vol_gate and bool(vol_hot[i]))

        stop_level = min(active_lo - mintick, active_lo * (1.0 - p.stop_pct / 100.0))
        tp_level = max(active_hi + mintick, active_hi * (1.0 + p.tp_pct / 100.0))

        buy_triggered = False
        sell_triggered = False
        buy_level = None
        crossed = []
        if i > 0 and prev_lo is not None and prev_lo > 0 and active_lo > 0 and active_hi > active_lo:
            for gi in range(p.levels):
                cur = grid_price(gi, active_lo, active_hi, p.levels, p.mode)
                pri = grid_price(gi, prev_lo, prev_hi, p.levels, p.mode)
                down = c[i] < cur and c[i - 1] >= pri
                up = c[i] > cur and c[i - 1] <= pri
                if down and gi < p.levels - 1:
                    buy_triggered = True
                    buy_level = cur
                    crossed.append(("buy", gi, cur))
                if up and gi > 0:
                    sell_triggered = True
                    crossed.append(("sell", gi, cur))

        qty_now = sum(lot[0] for lot in lots)
        equity_now = mark(c[i])
        pref = p.order_qty
        if p.notional_pct > 0 and c[i] > 0:
            pref = max(equity_now, 0.0) * p.notional_pct / c[i]
        risk_capital = max(equity_now, 0.0) * p.risk_pct / 100.0
        risk_per = max(c[i] - stop_level, mintick)
        risk_qty = risk_capital / risk_per
        hard_cap = p.max_position if p.notional_pct <= 0 else pref * p.max_entries
        max_open = min(hard_cap, risk_qty)
        risk_cap = int(math.floor(max_open / pref)) if pref > 0 else 0
        allowed = min(p.max_entries, max(0, risk_cap))
        if p.notional_pct > 0:
            entry_count = len(lots)
        else:
            entry_count = int(math.floor(max(qty_now, 0.0) / pref + 1e-6)) if pref > 0 else 0
        remaining = max(0.0, max_open - max(qty_now, 0.0))
        buy_qty = min(pref, remaining)
        in_range = active_lo <= c[i] <= active_hi
        stop_cross = i > 0 and prev_stop is not None and c[i] <= stop_level and c[i - 1] > prev_stop
        tp_cross = i > 0 and prev_tp is not None and c[i] >= tp_level and c[i - 1] < prev_tp
        buy_ok = (buy_triggered and in_range and not trend_blocked and not gate_blocked
                  and not stop_cross and not tp_cross and entry_count < allowed and buy_qty > 0)
        trend_exit = p.use_trend and strong and not prev_strong and qty_now > 0

        if buy_triggered and in_range and (trend_blocked or gate_blocked) and not buy_ok:
            blocked += 1
            if shadow is None and i + 1 < n:
                step = 0.0
                if buy_level is not None and p.levels > 1 and active_hi > active_lo:
                    # one grid step above the crossed level, as a fraction of price
                    idx = 0
                    for gi in range(p.levels - 1):
                        if abs(grid_price(gi, active_lo, active_hi, p.levels, p.mode) - buy_level) < mintick * 2:
                            idx = gi
                            break
                    nxt = grid_price(idx + 1, active_lo, active_hi, p.levels, p.mode)
                    step = nxt
                else:
                    step = c[i] * (1.0 + p.min_spacing_pct / 100.0)
                shadow = {"stop": stop_level, "target": step if step > c[i] else c[i] * (1.0 + p.min_spacing_pct / 100.0)}

        action = ""
        if p.structure == "per_level":
            if trend_exit and lots:
                flatten(c[i] * (1.0 - p.slip), "trend", i)
                action = "trend"
            # open or close individual levels; last-cross overwrite is not used
            open_levels = {lot[3] for lot in lots}
            for side, gi, level in crossed:
                if side == "sell" and (gi - 1) in open_levels and lots:
                    # close the single lot bought at the level below
                    keep = []
                    for lot in lots:
                        if lot[3] == gi - 1:
                            qty, entry, entry_fee, level_i = lot
                            px = c[i] * (1.0 - p.slip)
                            fee = qty * px * p.fee
                            pnl = qty * (px - entry) - entry_fee - fee
                            cash += qty * px - fee
                            cycles.append({"bar": i, "t": int(t[i]), "pnl": pnl, "reason": "sell",
                                           "entry": entry, "exit": px, "qty": qty, "level": level_i})
                            if dep_open is not None:
                                dep_open["pnl"] = dep_open.get("pnl", 0.0) + pnl
                                dep_open["lots"] += 1
                            open_levels.discard(level_i)
                            action = "sell"
                        else:
                            keep.append(lot)
                    lots = keep
                    if not lots and dep_open is not None:
                        deployments.append({"bar": i, "t": int(t[i]), "pnl": dep_open.get("pnl", 0.0),
                                            "reason": "sell", "lots": dep_open["lots"], "start": dep_open["start"]})
                        dep_open = None
                if side == "buy":
                    qty_now = sum(lot[0] for lot in lots)
                    equity_now = mark(c[i])
                    pref_i = p.order_qty
                    if p.notional_pct > 0 and c[i] > 0:
                        pref_i = max(equity_now, 0.0) * p.notional_pct / c[i]
                    risk_capital = max(equity_now, 0.0) * p.risk_pct / 100.0
                    risk_per = max(c[i] - stop_level, mintick)
                    hard_cap = p.max_position if p.notional_pct <= 0 else pref_i * p.max_entries
                    max_open = min(hard_cap, risk_capital / risk_per)
                    risk_cap = int(math.floor(max_open / pref_i)) if pref_i > 0 else 0
                    allowed = min(p.max_entries, max(0, risk_cap))
                    entry_count = len(lots)
                    remaining = max(0.0, max_open - qty_now)
                    buy_qty = min(pref_i, remaining)
                    can = (in_range and not trend_blocked and not gate_blocked and not stop_cross
                           and not tp_cross and entry_count < allowed and buy_qty > 0 and gi not in open_levels)
                    if can:
                        px = c[i] * (1.0 + p.slip)
                        fee = buy_qty * px * p.fee
                        cash -= buy_qty * px + fee
                        lots.append((buy_qty, px, fee, gi))
                        open_levels.add(gi)
                if dep_open is None:
                    dep_open = {"start": int(t[i]), "i": i, "lots": 0, "pnl": 0.0, "adx": adx_v, "dev": dev, "eq0": equity_now}
                action = "buy"
            if lots and stop_cross:
                flatten(c[i] * (1.0 - p.slip), "stop", i)
                action = "stop"
            elif lots and tp_cross:
                flatten(tp_level, "tp", i)
                action = "tp"
        else:
            if trend_exit and lots:
                flatten(c[i] * (1.0 - p.slip), "trend", i)
                action = "trend"
            if buy_ok:
                px = c[i] * (1.0 + p.slip)
                fee = buy_qty * px * p.fee
                cash -= buy_qty * px + fee
                lots.append((buy_qty, px, fee, -1))
                if dep_open is None:
                    dep_open = {"start": int(t[i]), "i": i, "lots": 0, "pnl": 0.0, "adx": adx_v, "dev": dev, "eq0": equity_now}
                action = "buy"
            if sell_triggered and lots:
                flatten(c[i] * (1.0 - p.slip), "sell", i)
                action = "sell"
            if stop_cross and lots:
                flatten(c[i] * (1.0 - p.slip), "stop", i)
                action = "stop"
            if tp_cross and lots:
                flatten(tp_level, "tp", i)
                action = "tp"

        if lots:
            in_mkt += 1
        equity[i] = mark(c[i])
        prev_lo, prev_hi = active_lo, active_hi
        prev_stop, prev_tp = stop_level, tp_level
        prev_strong = strong
        prev_outside = outside
        if trace is not None and i < 400:
            trace.append({
                "i": i, "t": int(t[i]), "c": c[i], "lo": active_lo, "hi": active_hi,
                "adx": adx_v, "dev": dev, "paused": buys_paused, "strong": strong,
                "buy": buy_triggered, "sell": sell_triggered, "action": action,
                "pos": sum(lot[0] for lot in lots),
            })

    closed_deps = [d for d in deployments if d["reason"] != "mark"]
    return {
        "equity": equity,
        "cycles": cycles,
        "deployments": closed_deps,
        "bars_in_market": in_mkt,
        "bars": n,
        "blocked": blocked,
        "shadow_stop": shadow_stop,
        "shadow_win": shadow_win,
        "shadow_unresolved": 0 if shadow is None else 1,
        "trace": trace,
        "open_qty": sum(lot[0] for lot in lots),
    }


def metrics(result, initial: float):
    eq = result["equity"]
    peak = eq[0]
    max_dd = 0.0
    for v in eq:
        if v > peak:
            peak = v
        if peak > 0:
            max_dd = max(max_dd, (peak - v) / peak)
    cycles = result["cycles"]
    deps = result["deployments"]

    def rate(rows):
        if not rows:
            return None
        return sum(1 for r in rows if r["pnl"] > 0) / len(rows)

    net = float(eq[-1] / initial - 1.0) if initial else 0.0
    stops = sum(1 for d in deps if d["reason"] == "stop")
    blocked = result["blocked"]
    judged = result["shadow_stop"] + result["shadow_win"]
    return {
        "net_return": net,
        "max_dd": float(max_dd),
        "time_in_market": result["bars_in_market"] / result["bars"] if result["bars"] else 0.0,
        "cycle_win_rate": rate(cycles),
        "deployment_win_rate": rate(deps),
        "cycles": len(cycles),
        "deployments": len(deps),
        "stops": stops,
        "blocked_entries": blocked,
        "blocked_then_stopped": result["shadow_stop"],
        "blocked_then_bounced": result["shadow_win"],
        "blocked_stop_share": (result["shadow_stop"] / judged) if judged else None,
        "end_equity": float(eq[-1]),
        "open_qty": result["open_qty"],
    }


def slice_idx(t, start_ms, end_ms):
    """Half-open [start, end). End timestamps are not shared with the next window."""
    t = np.asarray(t)
    i0 = int(np.searchsorted(t, start_ms, side="left"))
    i1 = int(np.searchsorted(t, end_ms, side="left"))
    return i0, i1


def _select_adx(high, low, close, n=14):
    """ADX used by elite-intel/market-check/select.py: pandas ewm(alpha=1/n) on that window."""
    import pandas as pd
    h = pd.Series(np.asarray(high, dtype=float))
    l = pd.Series(np.asarray(low, dtype=float))
    c = pd.Series(np.asarray(close, dtype=float))
    up = h.diff()
    dn = -l.diff()
    pdm = np.where((up > dn) & (up > 0), up, 0.0)
    ndm = np.where((dn > up) & (dn > 0), dn, 0.0)
    tr = pd.concat([(h - l), (h - c.shift()).abs(), (l - c.shift()).abs()], axis=1).max(axis=1)
    alpha = 1.0 / n
    atr_ = tr.ewm(alpha=alpha).mean()
    pdi = 100.0 * pd.Series(pdm).ewm(alpha=alpha).mean() / atr_
    ndi = 100.0 * pd.Series(ndm).ewm(alpha=alpha).mean() / atr_
    dx = 100.0 * (pdi - ndi).abs() / (pdi + ndi)
    return float(dx.ewm(alpha=alpha).mean().iloc[-1])


def daily_drift_block(t, h, l, c, drift_min=0.8, adx_min=40.0):
    """Picks-screen gate from elite-intel/market-check/select.py trend_drift30 / trend_skip.

    On each completed UTC day, take the last 30 daily bars (tail(30)):
    drift30 = |last close - first close of that window| / (max high - min low).
    ADX is select.py's ewm ADX on those same 30 bars. Block when drift30 > 0.8
    and ADX > 40. The flag is applied to the following day's intraday bars.
    """
    day = t // 86_400_000
    days = []
    cur = None
    dh = dl = dc = None
    for i in range(len(t)):
        d = int(day[i])
        if cur is None:
            cur, dh, dl, dc = d, h[i], l[i], c[i]
        elif d != cur:
            days.append((cur, dh, dl, dc))
            cur, dh, dl, dc = d, h[i], l[i], c[i]
        else:
            dh = max(dh, h[i])
            dl = min(dl, l[i])
            dc = c[i]
    if cur is not None:
        days.append((cur, dh, dl, dc))
    block_day = {}
    if len(days) >= 30:
        dh = np.array([r[1] for r in days], dtype=float)
        dl = np.array([r[2] for r in days], dtype=float)
        dc = np.array([r[3] for r in days], dtype=float)
        for i in range(29, len(days)):
            hh, ll, cc = dh[i - 29:i + 1], dl[i - 29:i + 1], dc[i - 29:i + 1]
            span = float(hh.max() - ll.min())
            net = abs(float(cc[-1] - cc[0]))
            drift = (0.0 if net == 0 else float("inf")) if span == 0 else net / span
            adx_v = _select_adx(hh, ll, cc, 14)
            block_day[int(days[i][0])] = bool(drift > drift_min and adx_v > adx_min and not math.isnan(adx_v))
    out = np.zeros(len(t), dtype=bool)
    last = False
    prev_day = None
    for i in range(len(t)):
        d = int(day[i])
        if prev_day is None:
            prev_day = d
        elif d != prev_day:
            last = block_day.get(prev_day, False)
            prev_day = d
        out[i] = last
    return out


def vol_hot_flag(h, l, c, atr_len=14, lookback=180, pct=80.0):
    a = atr(h, l, c, atr_len)
    hot = np.zeros(len(c), dtype=bool)
    with np.errstate(divide="ignore", invalid="ignore"):
        ratio = np.where(c > 0, a / c, np.nan)
    for i in range(lookback, len(c)):
        window = ratio[i - lookback:i]
        window = window[~np.isnan(window)]
        if len(window) < lookback // 2 or np.isnan(ratio[i]):
            continue
        thr = float(np.percentile(window, pct))
        hot[i] = ratio[i] > thr
    return hot


def align_funding(bar_t, fund_t, fund_rate):
    """Sum funding rates whose timestamp falls in [bar, next bar)."""
    out = np.zeros(len(bar_t))
    if len(fund_t) == 0:
        return out
    idx = np.searchsorted(bar_t, fund_t, side="right") - 1
    for j, i in enumerate(idx):
        if 0 <= i < len(out):
            out[i] += fund_rate[j]
    return out


def params_public(p: Params):
    d = asdict(p)
    return d
