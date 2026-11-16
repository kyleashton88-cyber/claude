"""Python port of the WaveTrend core of VuManChu Cipher B (public community imitation in /workspace/market-cipher/refs).
Signals: buy dot  = wt1 crosses over wt2 while wt2 <= osLevel ; sell dot = wt1 crosses under wt2 while wt2 >= obLevel.
Baseline strategy = the reference strategy file: long while wt1>wt2, short while wt1<wt2 (stop-and-reverse on every WT cross).
Optimised variant: enter on dots only, ATR TP/SL, optional max-hold, trend filters (EMA, 4h EMA200 side, ADX), weekday filter.
One position at a time; market fills at next open (+slip); TP/SL intrabar with TradingView's path rule; fee per side.
"""
import numpy as np, pandas as pd
from numba import njit
import ind, grid_sim as G

def wavetrend(D, chlen=9, avg=12, malen=3):
    src = (D.h + D.l + D.c) / 3
    esa = ind.ema(src, chlen); de = ind.ema(np.abs(src - esa), chlen)
    with np.errstate(invalid="ignore", divide="ignore"):
        ci = (src - esa) / (0.015 * de)
    wt1 = ind.ema(ci, avg); wt2 = ind.sma(wt1, malen)
    return wt1, wt2

@njit(cache=True)
def _sim(o, h, l, c, atr, longSig, shortSig, exitL, exitS, start, end, tpA, slA, maxHold, frac, fee, slip, init_cap, sar):
    cash = init_cap; pos = 0; q = 0.0; ep = 0.0; eb = 0; tpp = 0.0; slp = 0.0
    pend = 0; pendExit = False
    tp = np.zeros(100000); tr = np.zeros(100000); tk = np.zeros(100000, np.int64); nt = 0
    eq = np.zeros(end - start); hi = init_cap; ddm = 0.0
    for t in range(start, end):
        # open: queued exit then entry
        if pendExit and pos != 0:
            px = o[t] * (1 - slip) if pos > 0 else o[t] * (1 + slip)
            pnl = q * (px - ep) * pos - q * px * fee
            cash += pnl; tp[nt] = pnl; tr[nt] = (px / ep - 1) * pos; tk[nt] = 2; nt += 1; pos = 0
        pendExit = False
        if pend != 0 and pos == 0:
            px = o[t] * (1 + slip) if pend > 0 else o[t] * (1 - slip)
            q = cash * frac / px; ep = px; pos = pend; eb = t
            cash -= q * px * fee
            tpp = ep + pos * tpA * atr[t - 1] if tpA > 0 else 0.0
            slp = ep - pos * slA * atr[t - 1] if slA > 0 else 0.0
        pend = 0
        # intrabar TP/SL (orders active from fill bar: strategy.exit placed with entry)
        if pos != 0 and (tpA > 0 or slA > 0):
            upFirst = (h[t] - o[t]) < (o[t] - l[t])
            px = -1.0; kind = 0
            if pos > 0:
                hitT = tpA > 0 and h[t] >= tpp; hitS = slA > 0 and l[t] <= slp
                if tpA > 0 and o[t] >= tpp and t > eb: px = o[t]; kind = 1
                elif slA > 0 and o[t] <= slp and t > eb: px = o[t] * (1 - slip); kind = 0
                elif upFirst:
                    if hitT: px = tpp; kind = 1
                    elif hitS: px = slp * (1 - slip); kind = 0
                else:
                    if hitS: px = slp * (1 - slip); kind = 0
                    elif hitT: px = tpp; kind = 1
            else:
                hitT = tpA > 0 and l[t] <= tpp; hitS = slA > 0 and h[t] >= slp
                if tpA > 0 and o[t] <= tpp and t > eb: px = o[t]; kind = 1
                elif slA > 0 and o[t] >= slp and t > eb: px = o[t] * (1 + slip); kind = 0
                elif not upFirst:
                    if hitT: px = tpp; kind = 1
                    elif hitS: px = slp * (1 + slip); kind = 0
                else:
                    if hitS: px = slp * (1 + slip); kind = 0
                    elif hitT: px = tpp; kind = 1
            if px > 0:
                pnl = q * (px - ep) * pos - q * px * fee
                cash += pnl; tp[nt] = pnl; tr[nt] = (px / ep - 1) * pos; tk[nt] = kind; nt += 1; pos = 0
        # close
        equity = cash + (q * (c[t] - ep) * pos if pos != 0 else 0.0)
        eq[t - start] = equity
        if equity > hi: hi = equity
        d = (hi - equity) / hi
        if d > ddm: ddm = d
        if pos != 0:
            if (pos > 0 and exitL[t]) or (pos < 0 and exitS[t]) or (maxHold > 0 and t - eb + 1 >= maxHold):
                pendExit = True
                if sar:
                    if pos > 0 and shortSig[t]: pend = -1
                    if pos < 0 and longSig[t]: pend = 1
        else:
            if longSig[t]: pend = 1
            elif shortSig[t]: pend = -1
    return tp[:nt], tr[:nt], tk[:nt], eq, ddm

def run(D, p, start, end, fee=0.001, slip=0.0003, init_cap=10000.0):
    wt1, wt2 = D.get(("wt", p["chlen"], p["avg"]), lambda: wavetrend(D, p["chlen"], p["avg"]))
    prev1 = np.r_[np.nan, wt1[:-1]]; prev2 = np.r_[np.nan, wt2[:-1]]
    xUp = (wt1 > wt2) & (prev1 <= prev2); xDn = (wt1 < wt2) & (prev1 >= prev2)
    atr = D.get(("atr", 14), lambda: ind.atr(D.h, D.l, D.c, 14))
    if p["kind"] == "baseline":
        L = xUp.copy(); S = xDn.copy(); eL = xDn.copy(); eS = xUp.copy(); tpA = slA = 0.0; mh = 0; sar = True
    else:
        L = xUp & (wt2 <= -p["lvl"]); S = xDn & (wt2 >= p["lvl"])
        if p["trend"] == "ema":
            e = D.get(("ema", 200), lambda: ind.ema(D.c, 200)); L &= D.c > e; S &= D.c < e
        elif p["trend"] == "htf":
            up, dn = D.htf_side(200); L &= up; S &= dn
        if p["adxMax"] > 0:
            adx = D.get(("adx", 14), lambda: ind.dmi(D.h, D.l, D.c, 14, 14)[2]); L &= adx < p["adxMax"]; S &= adx < p["adxMax"]
        if p["side"] == "long": S[:] = False
        if p["side"] == "short": L[:] = False
        if p["wk"]: L &= D.wk; S &= D.wk
        if p["oppExit"]:
            eL = xDn & (wt2 >= p["lvl"]); eS = xUp & (wt2 <= -p["lvl"])
        else:
            eL = np.zeros(len(L), bool); eS = eL
        tpA, slA, mh, sar = p["tp"], p["sl"], p["hold"], False
    f = lambda x: np.nan_to_num(x).astype(np.bool_)
    r = _sim(D.o, D.h, D.l, D.c, np.nan_to_num(atr), f(L), f(S), f(eL), f(eS), start, end, tpA, slA, mh, p["frac"], fee, slip, init_cap, sar)
    return G.stats(*r, init_cap=init_cap)
