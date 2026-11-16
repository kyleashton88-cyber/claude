"""Round 3 simulator.

A deployment is one launch-to-flat episode. It wins when pnl is above zero
after taker fees and any funding that the public history actually contains.
The primary rate is that deployment win rate, not the rate of individual
grid sells.

Isolated margin. Notional = margin x leverage. Maintenance margin rate is a
small-tier teaching schedule (BTC 0.4%, ETH 0.5%, SOL and ZEC 1% of
notional), not a live exchange table. Liquidation is checked on 1h lows.
A stop that sits above the liquidation price is assumed to fill first when
the bar opens above the stop and trades down through it. A gap through the
liquidation price is a liquidation.
"""
from __future__ import annotations

import math

import numpy as np
import pandas as pd

from engine import atr, bollinger, dmi, ema, grid_price

MMR = {"BTC-USDT": 0.004, "ETH-USDT": 0.005, "SOL-USDT": 0.01, "ZEC-USDT": 0.01,
       "XRP-USDT": 0.01, "LINK-USDT": 0.01}


def liq_price(avg, qty, margin, cash_pnl, mmr):
    """Mark where isolated equity equals maintenance margin. Long only."""
    if qty <= 0 or avg <= 0:
        return 0.0
    # mark = (qty*avg - margin - cash_pnl) / (qty * (1 - mmr))
    num = qty * avg - margin - cash_pnl
    den = qty * (1.0 - mmr)
    if den <= 0:
        return 0.0
    return max(0.0, num / den)


def hysteresis(adx, enter=20.0, leave=32.0, hold=2):
    state = False
    streak = 0
    out = np.zeros(len(adx), dtype=bool)
    for i, a in enumerate(adx):
        if a is None or (isinstance(a, float) and math.isnan(a)):
            out[i] = state
            continue
        if not state:
            streak = streak + 1 if a < enter else 0
            if streak >= hold:
                state = True
                streak = 0
        elif a > leave:
            state = False
            streak = 0
        out[i] = state
    return out


def variance_ratio(close, q=8, window=64):
    logc = np.log(np.maximum(close, 1e-12))
    r1 = np.diff(logc, prepend=np.nan)
    rq = logc - pd.Series(logc).shift(q).to_numpy()
    v1 = pd.Series(r1).rolling(window, min_periods=window).var().to_numpy()
    vq = pd.Series(rq).rolling(window, min_periods=window).var().to_numpy()
    with np.errstate(divide="ignore", invalid="ignore"):
        vr = vq / (q * v1)
    return vr


def range_age(close, lower, upper):
    age = np.zeros(len(close), dtype=int)
    run = 0
    for i in range(len(close)):
        lo, hi = lower[i], upper[i]
        if math.isnan(lo) or math.isnan(hi) or not (lo <= close[i] <= hi):
            run = 0
        else:
            run += 1
        age[i] = run
    return age


def build_ranges(h, l, c):
    """Frozen-at-launch candidates. Each value is known on that bar; callers lag by 1."""
    a = atr(h, l, c, 14)
    basis = ema(c, 50)
    out = {}
    for name, mult in (("atr2", 2.0), ("atr3", 3.0), ("atr_hold", 2.3)):
        lo = basis - mult * a
        hi = basis + mult * a
        out[name] = (lo, hi)
    _m, up, lo = bollinger(c, 20, 2.0)
    out["bb"] = (lo, up)
    # 20th to 80th percentile of the last 80 closes
    s = pd.Series(c)
    out["pct"] = (s.rolling(80, min_periods=80).quantile(0.20).to_numpy(),
                  s.rolling(80, min_periods=80).quantile(0.80).to_numpy())
    return out


def smooth_pair(lo, hi, length=5):
    return ema(np.nan_to_num(lo, nan=np.nanmean(lo)), length), ema(np.nan_to_num(hi, nan=np.nanmean(hi)), length)


def prepare_features(h, l, c, v, bar_seconds, stable_t, stable_chg):
    a = atr(h, l, c, 14)
    _p, _m, adx = dmi(h, l, c, 14, 14)
    adx_s = ema(np.nan_to_num(adx, nan=0.0), 3)
    # restore nan warmup roughly: first 30 bars of ema(adx) are not meaningful
    adx_s = adx_s.copy()
    adx_s[:30] = np.nan
    hyst = hysteresis(np.nan_to_num(adx_s, nan=99.0), 20.0, 32.0, 2)
    vr = variance_ratio(c)
    ranges = build_ranges(h, l, c)
    ranges["atr2s"] = smooth_pair(*ranges["atr2"])
    quote = c * v
    bars24 = max(1, int(round(86400 / bar_seconds)))
    qv = pd.Series(quote).rolling(bars24, min_periods=bars24).sum().to_numpy() / 24.0
    liquid = qv >= 2_000_000.0
    # daily regime from these bars
    return {
        "atr": a, "adx": adx, "adx_s": adx_s, "hyst": hyst, "vr": vr,
        "ranges": ranges, "qv": qv, "liquid": liquid,
    }


def map_daily_hyst(t, h, l, c):
    day = t // 86_400_000
    rows = []
    s = 0
    for i in range(1, len(t) + 1):
        if i == len(t) or day[i] != day[s]:
            sl = slice(s, i)
            rows.append((int(day[s]), float(h[sl].max()), float(l[sl].min()), float(c[i - 1])))
            s = i
    if len(rows) < 40:
        return np.zeros(len(t), dtype=bool)
    dd = np.array([r[0] for r in rows])
    dh = np.array([r[1] for r in rows])
    dl = np.array([r[2] for r in rows])
    dc = np.array([r[3] for r in rows])
    _p, _m, adx = dmi(dh, dl, dc, 14, 14)
    hyst = hysteresis(np.nan_to_num(adx, nan=99.0), 22.0, 35.0, 1)
    # previous completed day
    flag = {int(dd[i]): bool(hyst[i - 1]) if i else False for i in range(len(dd))}
    out = np.zeros(len(t), dtype=bool)
    last = False
    prev = None
    for i in range(len(t)):
        d = int(day[i])
        if prev is None:
            prev = d
        elif d != prev:
            last = flag.get(prev, False)
            prev = d
        out[i] = last
    return out


def stable_mask(t, stable_t, stable_chg):
    """Previous day's 14-day stablecoin USD supply change is positive."""
    if stable_t is None or len(stable_t) == 0:
        return np.ones(len(t), dtype=bool)
    day = t // 86_400_000
    idx = np.searchsorted(stable_t, day, side="right") - 1
    out = np.zeros(len(t), dtype=bool)
    ok = idx >= 1
    # lag one day: use the change known at the previous day
    out[ok] = stable_chg[idx[ok] - 1] > 0
    return out


def simulate(o, h, l, c, t, lower, upper, allow, regime_on, spec, mintick,
             funding=None, mmr=0.005, count_from=0, count_to=None,
             t1=None, h1=None, l1=None, o1=None):
    """spec: levels, mode, stop_pct, tp_pct, outside, max_bars, exit, leverage, fee, slip, margin."""
    n = len(c)
    if count_to is None:
        count_to = n
    if funding is None:
        funding = np.zeros(n)
    lev = spec["leverage"]
    margin = spec["margin"]
    fee = spec["fee"]
    slip = spec["slip"]
    levels = spec["levels"]
    mode = spec["mode"]
    stop_pct = spec["stop_pct"]
    tp_pct = spec["tp_pct"]
    outside_n = spec["outside"]
    max_bars = spec["max_bars"]
    exit_mode = spec["exit"]  # close_all, partial, regime
    deps = []
    # position
    active = False
    qty = 0.0
    avg = 0.0
    cash_pnl = 0.0
    buys = []  # (price, qty, target, filled)
    lo_f = hi_f = stop = tp = 0.0
    start = 0
    outside = 0
    partial_done = False
    did_fill = False
    wallet_peak = margin
    wallet_dd = 0.0
    offset = 0.0

    def equity_at(mark):
        return margin + cash_pnl + qty * (mark - avg)

    def finish(reason, bar, px):
        nonlocal active, qty, avg, cash_pnl, offset, partial_done, outside, did_fill
        if qty > 0:
            px_use = px * (1.0 - slip) if reason in ("stop", "liq", "time", "regime", "outside") else px
            fee_c = qty * px_use * fee
            cash_pnl += qty * (px_use - avg) - fee_c
            qty = 0.0
        pnl = cash_pnl
        if start >= count_from and did_fill:
            deps.append({
                "i": start, "end": bar, "t": int(t[start]), "pnl": pnl,
                "ret": pnl / margin, "reason": reason, "leverage": lev,
            })
        offset += pnl
        active = False
        qty = 0.0
        avg = 0.0
        cash_pnl = 0.0
        buys.clear()
        partial_done = False
        did_fill = False
        outside = 0

    # 1h index
    use_1h = t1 is not None and len(t1) > 0 and lev >= 2.0
    bar_ms = int(spec.get("bar_ms") or (int(t[1] - t[0]) if n > 1 else 14_400_000))

    def adverse(so, sh, sl):
        nonlocal killed
        if qty <= 0:
            return
        liq = liq_price(avg, qty, margin, cash_pnl, mmr)
        if liq > 0 and so <= liq:
            finish("liq", i, so)
            killed = True
            return
        if liq > 0 and sl <= liq and not (stop > liq and so > stop):
            finish("liq", i, liq)
            killed = True
            return
        if sl <= stop:
            finish("stop", i, so if so < stop else stop)
            killed = True

    def targets(sh):
        nonlocal killed, qty, partial_done, cash_pnl
        if qty <= 0:
            return
        if exit_mode == "partial" and not partial_done:
            for b in buys:
                if b[3] and sh >= b[2]:
                    sell_q = qty * 0.5
                    px = b[2]
                    cash_pnl += sell_q * (px - avg) - sell_q * px * fee
                    qty -= sell_q
                    partial_done = True
                    break
        if exit_mode == "close_all":
            touched = [b[2] for b in buys if b[3] and sh >= b[2]]
            if touched:
                finish("sell", i, min(touched))
                killed = True
                return
        if sh >= tp:
            finish("tp", i, tp)
            killed = True

    def fill_buys(so, sl):
        nonlocal qty, avg, did_fill, cash_pnl
        for bi, b in enumerate(buys):
            if b[3] or sl > b[0]:
                continue
            fill = so if so < b[0] else b[0]
            if (qty + b[1]) * fill > margin * lev * 1.05:
                continue
            if qty == 0:
                avg = fill
                qty = b[1]
            else:
                avg = (avg * qty + fill * b[1]) / (qty + b[1])
                qty += b[1]
            cash_pnl -= b[1] * fill * fee
            buys[bi] = (b[0], b[1], b[2], True)
            did_fill = True

    for i in range(1, n):
        if active and funding[i] != 0.0 and qty > 0:
            cash_pnl -= qty * c[i] * funding[i]
        if active:
            if use_1h:
                a = int(np.searchsorted(t1, t[i], side="left"))
                b = int(np.searchsorted(t1, t[i] + bar_ms, side="left"))
                seq = [(o1[j], h1[j], l1[j]) for j in range(a, b) if 0 <= j < len(t1)]
                if not seq:
                    seq = [(o[i], h[i], l[i])]
            else:
                seq = [(o[i], h[i], l[i])]
            killed = False
            for so, sh, sl in seq:
                down_first = (so - sl) >= (sh - so)
                if down_first:
                    adverse(so, sh, sl)
                if not killed:
                    targets(sh)
                if not killed and not down_first:
                    adverse(so, sh, sl)
                if not killed:
                    fill_buys(so, sl)
                if killed or not active:
                    break
            if active and not killed:
                if c[i] > hi_f or c[i] < lo_f:
                    outside += 1
                else:
                    outside = 0
                if outside >= outside_n:
                    finish("outside", i, c[i])
                elif max_bars and (i - start) >= max_bars:
                    finish("time", i, c[i])
                elif exit_mode == "regime" and not regime_on[i]:
                    finish("regime", i, c[i])
                else:
                    eq = equity_at(c[i])
                    wallet_peak = max(wallet_peak, offset + eq)
                    if wallet_peak > 0:
                        wallet_dd = max(wallet_dd, (wallet_peak - (offset + eq)) / wallet_peak)
        if not active and allow[i - 1] and count_from <= i < count_to:
            lo = lower[i - 1]
            hi = upper[i - 1]
            if not (lo > 0 and hi > lo and c[i - 1] > lo):
                continue
            prices = [grid_price(k, lo, hi, levels, mode) for k in range(levels)]
            # enforce a minimum step of 0.6% by skipping a launch that is tighter
            steps = [(prices[k + 1] / prices[k] - 1) for k in range(levels - 1) if prices[k] > 0]
            if not steps or min(steps) < spec.get("min_step", 0.006):
                continue
            below = [k for k in range(levels - 1) if prices[k] < c[i - 1]]
            if not below:
                continue
            notional = margin * lev / len(below)
            buys = [(prices[k], notional / prices[k], prices[k + 1], False) for k in below]
            lo_f, hi_f = lo, hi
            stop = lo * (1.0 - stop_pct / 100.0)
            tp = hi * (1.0 + tp_pct / 100.0)
            # buffer filter: liq must sit at least 2 stop-gaps beyond the stop
            if spec.get("buffer"):
                est = liq_price(c[i - 1], (margin * lev) / c[i - 1], margin, 0.0, mmr)
                gap = lo - stop
                if est > stop - 2.0 * gap:
                    buys = []
                    continue
            active = True
            start = i
            qty = 0.0
            avg = 0.0
            cash_pnl = 0.0
            outside = 0
            partial_done = False
            did_fill = False
        eq_now = equity_at(c[i]) if active else margin
        wealth = offset + eq_now
        wallet_peak = max(wallet_peak, wealth)
        if wallet_peak > 0:
            wallet_dd = max(wallet_dd, (wallet_peak - wealth) / wallet_peak)
    return {"deployments": deps, "max_dd": wallet_dd}


def wilson(wins, n, z=1.96):
    if n <= 0:
        return None, None
    p = wins / n
    den = 1.0 + z * z / n
    centre = (p + z * z / (2.0 * n)) / den
    margin = z * math.sqrt(p * (1 - p) / n + z * z / (4.0 * n * n)) / den
    return max(0.0, centre - margin), min(1.0, centre + margin)
