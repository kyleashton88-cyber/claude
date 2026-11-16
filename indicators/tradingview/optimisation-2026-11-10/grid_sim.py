"""Faithful Python port of grid-bot-improved-merged-deploy(-weekday).pine ("Crypto Grid Strategy v2").
Execution model mirrors TradingView's broker emulator with process_orders_on_close=false:
 - logic runs on bar close; strategy.entry / close_all fill at the NEXT bar open (+slippage)
 - strategy.exit limit/stop orders rest from the bar after they are placed; intrabar path = TV rule
   (open->nearer extreme->other extreme->close); gaps fill at the open
 - per-level legs L0..L(n-2) target i+1, S1..S(n-1) target i-1, stop beyond range +/- ATR*stopAtr
 - spike filter, circuit breaker (loss streak / DD pause), hard max-drawdown halt, gap/warm-up guards
Extra OPTIONAL filters (off in baseline): weekday-only entries (Sydney), HTF EMA side filter, TP edge toggles.
Costs: fee per side (default 0.10%), slippage on market & stop fills (default 0.03%).
"""
import numpy as np, pandas as pd
from numba import njit
import ind

@njit(cache=True)
def _sim(o, h, l, c, atr, adx, bbw, ema, hiC, loC, spike, gap, okdata, wk, htf_up, htf_dn,
         start, end, mode, n, minStep, geometric, qtyPct, maxOpen, stopAtr, tpEdge, cooldownN,
         adxMax, bbwMax, useRegime, useSpike, spikeCool, useCb, cbStreak, cbDd, cbPause, hardDd,
         fee, slip, useWk, sideFilt, init_cap, maxStopAtr):
    # mode 0 neutral 1 long 2 short
    NL = 40
    lev = np.zeros(NL)
    Lopen = np.zeros(NL, np.bool_); Lpx = np.zeros(NL); Lq = np.zeros(NL); Lbar = np.zeros(NL, np.int64)
    Sopen = np.zeros(NL, np.bool_); Spx = np.zeros(NL); Sq = np.zeros(NL); Sbar = np.zeros(NL, np.int64)
    Lpend = np.zeros(NL, np.bool_); Lpq = np.zeros(NL); Spend = np.zeros(NL, np.bool_); Spq = np.zeros(NL)
    Lstop = np.zeros(NL); Sstop = np.zeros(NL)
    cash = init_cap
    gridOn = False; gLo = 0.0; gHi = 0.0; cooldown = 0
    lastSpike = -100000
    lossStreak = 0; eqPeak = init_cap; pauseUntil = -1
    closeAllPend = False; halted = False; haltPend = False
    hardPeak = init_cap
    maxT = 200000
    tp = np.zeros(maxT); tret = np.zeros(maxT); tk = np.zeros(maxT, np.int64); nt = 0
    eq = np.zeros(end - start)
    ddMax = 0.0; eqHi = init_cap
    for t in range(start, end):
        closedPnls_n = 0
        # ---- A: open of bar t: queued market orders ----
        if closeAllPend or haltPend:
            for i in range(n):
                if Lopen[i]:
                    px = o[t] * (1 - slip)
                    pnl = Lq[i] * (px - Lpx[i]) - Lq[i] * px * fee
                    cash += Lq[i] * px - Lq[i] * px * fee
                    tp[nt] = pnl; tret[nt] = px / Lpx[i] - 1; tk[nt] = 2; nt += 1
                    lossStreak = lossStreak + 1 if pnl < 0 else 0
                    Lopen[i] = False
                if Sopen[i]:
                    px = o[t] * (1 + slip)
                    pnl = Sq[i] * (Spx[i] - px) - Sq[i] * px * fee
                    cash += Sq[i] * (Spx[i] - px) - Sq[i] * px * fee + Sq[i] * Spx[i]
                    tp[nt] = pnl; tret[nt] = Spx[i] / px - 1; tk[nt] = 2; nt += 1
                    lossStreak = lossStreak + 1 if pnl < 0 else 0
                    Sopen[i] = False
            if haltPend:
                halted = True; haltPend = False
            closeAllPend = False
        for i in range(n):
            if Lpend[i]:
                px = o[t] * (1 + slip)
                Lopen[i] = True; Lpx[i] = px; Lq[i] = Lpq[i]; Lbar[i] = t; Lpend[i] = False
                cash -= Lq[i] * px + Lq[i] * px * fee
            if Spend[i]:
                px = o[t] * (1 - slip)
                Sopen[i] = True; Spx[i] = px; Sq[i] = Spq[i]; Sbar[i] = t; Spend[i] = False
                cash -= Sq[i] * px + Sq[i] * px * fee   # margin 100%: reserve notional
        # ---- B: intrabar resting exits (placed at previous close) ----
        upFirst = (h[t] - o[t]) < (o[t] - l[t])
        for i in range(n):
            if Lopen[i] and Lbar[i] < t and i < n - 1:
                tgt = lev[i + 1]; st = Lstop[i]; px = -1.0; kind = 0
                if o[t] >= tgt:
                    px = o[t]; kind = 1
                elif o[t] <= st:
                    px = o[t] * (1 - slip); kind = 0
                elif upFirst:
                    if h[t] >= tgt: px = tgt; kind = 1
                    elif l[t] <= st: px = st * (1 - slip); kind = 0
                else:
                    if l[t] <= st: px = st * (1 - slip); kind = 0
                    elif h[t] >= tgt: px = tgt; kind = 1
                if px > 0:
                    pnl = Lq[i] * (px - Lpx[i]) - Lq[i] * px * fee
                    cash += Lq[i] * px - Lq[i] * px * fee
                    tp[nt] = pnl; tret[nt] = px / Lpx[i] - 1; tk[nt] = kind; nt += 1
                    lossStreak = lossStreak + 1 if pnl < 0 else 0
                    Lopen[i] = False
            if Sopen[i] and Sbar[i] < t and i > 0:
                tgt = lev[i - 1]; st = Sstop[i]; px = -1.0; kind = 0
                if o[t] <= tgt:
                    px = o[t]; kind = 1
                elif o[t] >= st:
                    px = o[t] * (1 + slip); kind = 0
                elif not upFirst:
                    if l[t] <= tgt: px = tgt; kind = 1
                    elif h[t] >= st: px = st * (1 + slip); kind = 0
                else:
                    if h[t] >= st: px = st * (1 + slip); kind = 0
                    elif l[t] <= tgt: px = tgt; kind = 1
                if px > 0:
                    pnl = Sq[i] * (Spx[i] - px) - Sq[i] * px * fee
                    cash += Sq[i] * Spx[i] + pnl
                    tp[nt] = pnl; tret[nt] = Spx[i] / px - 1; tk[nt] = kind; nt += 1
                    lossStreak = lossStreak + 1 if pnl < 0 else 0
                    Sopen[i] = False
        # ---- C: bar close ----
        posL = 0.0; posS = 0.0; ntr = 0; upnl = 0.0
        for i in range(n):
            if Lopen[i]:
                posL += Lq[i]; ntr += 1; upnl += Lq[i] * c[t]
            if Sopen[i]:
                posS += Sq[i]; ntr += 1; upnl += Sq[i] * Spx[i] + Sq[i] * (Spx[i] - c[t])
        equity = cash + upnl
        eq[t - start] = equity
        if equity > eqHi: eqHi = equity
        dd = (eqHi - equity) / eqHi
        if dd > ddMax: ddMax = dd
        if halted:
            continue
        # hard max drawdown
        if equity > hardPeak: hardPeak = equity
        if (hardPeak - equity) / hardPeak * 100 >= hardDd:
            haltPend = True
            continue
        if cooldown > 0: cooldown -= 1
        if spike[t]: lastSpike = t
        spikeBlock = useSpike and (spike[t] or t - lastSpike <= spikeCool)
        # circuit breaker
        if equity > eqPeak: eqPeak = equity
        ddp = (eqPeak - equity) / eqPeak * 100 if eqPeak > 0 else 0.0
        if useCb and t > pauseUntil and (lossStreak >= cbStreak or ddp >= cbDd):
            pauseUntil = t + cbPause; lossStreak = 0; eqPeak = equity
        cbPaused = useCb and t <= pauseUntil
        entryGate = (not spikeBlock) and (not cbPaused) and okdata[t] and (not gap[t]) and ((not useWk) or wk[t])
        ranging = adx[t] < adxMax and bbw[t] < bbwMax
        if mode == 0:
            regimeOk = (not useRegime) or ranging
        elif mode == 1:
            regimeOk = c[t] > ema[t] and ((not useRegime) or adx[t] < adxMax * 1.5)
        elif mode == 2:
            regimeOk = c[t] < ema[t] and ((not useRegime) or adx[t] < adxMax * 1.5)
        else:  # mode 3 "Auto": trend-aligned grid, side chosen by chart EMA + 4h EMA200
            regimeOk = ((c[t] > ema[t] and htf_up[t]) or (c[t] < ema[t] and htf_dn[t])) and ((not useRegime) or adx[t] < adxMax * 1.5)
        built = False
        if gridOn:
            brk = c[t] < gLo - atr[t] * stopAtr or c[t] > gHi + atr[t] * stopAtr
            if brk or ((not regimeOk) and ntr == 0):
                gridOn = False; cooldown = cooldownN
                if brk and ntr > 0:
                    closeAllPend = True
        if (not gridOn) and cooldown == 0 and entryGate and regimeOk and loC[t] > 0 and hiC[t] > loC[t] and c[t] > loC[t] and c[t] < hiC[t]:
            if geometric:
                stp = ((hiC[t] / loC[t]) ** (1.0 / (n - 1)) - 1.0) * 100
            else:
                stp = (hiC[t] - loC[t]) / (n - 1) / loC[t] * 100
            if stp >= minStep and (maxStopAtr <= 0 or (hiC[t]-loC[t]) <= maxStopAtr * atr[t]):
                gLo = loC[t]; gHi = hiC[t]
                for i in range(n):
                    fr = i / (n - 1.0)
                    lev[i] = gLo * (gHi / gLo) ** fr if geometric else gLo + (gHi - gLo) * fr
                gridOn = True; built = True
        if gridOn and not built and not closeAllPend:
            mid = (n - 1) / 2.0
            openCount = ntr
            for i in range(n):
                lv = lev[i]
                crossDn = c[t] < lv and c[t - 1] >= lv
                crossUp = c[t] > lv and c[t - 1] <= lv
                la = mode == 1 or (mode == 0 and i < mid) or (mode == 3 and c[t] > ema[t] and htf_up[t])
                sa = mode == 2 or (mode == 0 and i > mid) or (mode == 3 and c[t] < ema[t] and htf_dn[t])
                if sideFilt == 1:
                    la = la and htf_up[t]
                    sa = sa and htf_dn[t]
                if entryGate and crossDn and la and i < n - 1 and posS == 0 and openCount < maxOpen and not Lopen[i]:
                    q = equity * qtyPct / 100.0 / c[t]
                    if q * c[t] >= 5.0:
                        Lpend[i] = True; Lpq[i] = q; openCount += 1
                if entryGate and crossUp and sa and i > 0 and posL == 0 and openCount < maxOpen and not Sopen[i]:
                    q = equity * qtyPct / 100.0 / c[t]
                    if q * c[t] >= 5.0:
                        Spend[i] = True; Spq[i] = q; openCount += 1
        # exits placed this close (active from next bar); also for legs that fill next open -> placed next close
        if gridOn:
            for i in range(n):
                Lstop[i] = gLo - atr[t] * stopAtr
                Sstop[i] = gHi + atr[t] * stopAtr
        if tpEdge and gridOn and not built:
            if (posL > 0 and c[t] >= gHi) or (posS > 0 and c[t] <= gLo):
                closeAllPend = True
    return tp[:nt], tret[:nt], tk[:nt], eq, ddMax

class Data:
    def __init__(self, sym, tf):
        df = ind.load(sym, tf)
        self.sym, self.tf = sym, tf
        self.t = df.t.values
        self.o, self.h, self.l, self.c, self.v = [df[k].values.astype(float) for k in "ohlcv"]
        self.cache = {}
        # Sydney weekday of bar close
        tc = pd.to_datetime(self.t + (3600000 if tf == "1h" else 4 * 3600000) - 1, unit="ms", utc=True).tz_convert("Australia/Sydney")
        self.wk = np.asarray(tc.dayofweek < 5)
        h, l, c = self.h, self.l, self.c
        a14 = ind.atr(h, l, c, 14); base = ind.sma(a14, 100)
        with np.errstate(invalid="ignore", divide="ignore"):
            self.spike_base = (a14, base)
        self.spread = ind.sma((h - l) / c * 100, 24)
        pc = np.r_[np.nan, c[:-1]]
        self.gapv = np.abs(self.o / pc - 1) * 100
        # HTF (4h) EMA200 side filter from completed 4h bars, mapped to this tf
        self.htf = None

    def get(self, key, fn):
        if key not in self.cache: self.cache[key] = fn()
        return self.cache[key]

    def htf_side(self, emaLen=200):
        def f():
            d4 = ind.load(self.sym, "4h")
            e = ind.ema(d4.c.values, emaLen)
            close_t = d4.t.values + 4 * 3600000   # 4h bar close time
            s = pd.Series(np.sign(d4.c.values - e), index=close_t)
            bar_close = self.t + (3600000 if self.tf == "1h" else 4 * 3600000)
            idx = np.searchsorted(close_t, bar_close, side="right") - 1
            v = np.where(idx >= 0, s.values[np.clip(idx, 0, None)], 0)
            v = np.nan_to_num(v)
            return v > 0, v < 0
        return self.get(("htf", emaLen), f)

def run(D, p, start, end, fee=0.001, slip=0.0003, init_cap=10000.0):
    h, l, c, o = D.h, D.l, D.c, D.o
    atr = D.get(("atr", p["atrLen"]), lambda: ind.atr(h, l, c, p["atrLen"]))
    adx = D.get(("adx", p["adxLen"]), lambda: ind.dmi(h, l, c, p["adxLen"], p["adxLen"])[2])
    def bbwf():
        m = ind.sma(c, p["bbLen"]); s = ind.stdev(c, p["bbLen"])
        return (4 * s) / m * 100
    bbw = D.get(("bbw", p["bbLen"]), bbwf)
    ema = D.get(("ema", p["emaLen"]), lambda: ind.ema(c, p["emaLen"]))
    rl = p["rangeLen"]
    def rng():
        if p["rangeSrc"] == "Donchian":
            hi = ind.highest(h, rl); lo = ind.lowest(l, rl)
        elif p["rangeSrc"] == "ATR":
            e = ind.ema(c, rl); hi = e + atr * p["atrMult"]; lo = e - atr * p["atrMult"]
        else:
            s = pd.Series(c).rolling(rl)
            hi = s.quantile(p["pctHi"] / 100).values; lo = s.quantile(p["pctLo"] / 100).values
        return np.r_[np.nan, hi[:-1]], np.r_[np.nan, lo[:-1]]
    hiC, loC = D.get(("rng", p["rangeSrc"], rl, p.get("atrMult"), p.get("pctHi"), p.get("pctLo"), p["atrLen"]), rng)
    a14, base = D.spike_base
    with np.errstate(invalid="ignore"):
        spike = ((a14 / base) > p["spikeRatio"]) | ((h - l) > p["spikeRange"] * a14)
    spike = np.nan_to_num(spike).astype(np.bool_)
    warm = max(rl, p["emaLen"], 114, p["adxLen"] * 2, p["bbLen"]) + 1
    okdata = (np.arange(len(c)) >= warm) & ~np.isnan(base) & ~np.isnan(ema) & ~np.isnan(adx) & (np.nan_to_num(D.spread, nan=1e9) <= 3.0)
    gap = np.nan_to_num(D.gapv) >= 2.0
    up, dn = D.htf_side(p.get("htfEma", 200))
    f = lambda x: np.nan_to_num(np.asarray(x, float), nan=np.nan)
    r = _sim(o, h, l, c, np.nan_to_num(atr), np.nan_to_num(adx, nan=1e9), np.nan_to_num(bbw, nan=1e9), np.nan_to_num(ema),
             np.nan_to_num(hiC), np.nan_to_num(loC), spike, gap, okdata, D.wk, up, dn,
             start, end, {"Neutral": 0, "Long": 1, "Short": 2, "Auto": 3}[p["mode"]], p["gridCount"], p["minStep"], p["spacing"] == "Geometric",
             p["qtyPct"], p["maxOpen"], p["stopAtr"], p["tpEdge"], p["cooldown"], p["adxMax"], p["bbwMax"], p["useRegime"],
             p["useSpike"], p["spikeCool"], p["useCb"], p["cbStreak"], p["cbDd"], p["cbPause"], p["hardDd"],
             fee, slip, p.get("useWk", False), p.get("sideFilt", 0), init_cap, p.get("maxRangeAtr", 0.0))
    return stats(*r, init_cap=init_cap)

def stats(tp, tret, tk, eq, ddMax, init_cap=10000.0):
    n = len(tp); w = tp[tp > 0]; ls = tp[tp <= 0]
    gp, gl = w.sum(), -ls.sum()
    return dict(trades=n, win=(len(w) / n * 100 if n else np.nan), ret=(eq[-1] / init_cap - 1) * 100 if len(eq) else 0,
                dd=ddMax * 100, pf=(gp / gl if gl > 0 else np.inf if gp > 0 else np.nan),
                avgW=(w.mean() if len(w) else 0), avgL=(ls.mean() if len(ls) else 0), exp=(tp.mean() if n else 0),
                avgWr=(tret[tp > 0].mean() * 100 if len(w) else 0), avgLr=(tret[tp <= 0].mean() * 100 if len(ls) else 0),
                tpN=int((tk == 1).sum()), slN=int((tk == 0).sum()), mktN=int((tk == 2).sum()))

BASE = dict(mode="Neutral", rangeSrc="Donchian", rangeLen=100, atrMult=3.0, pctHi=90.0, pctLo=10.0, spacing="Geometric",
            gridCount=10, minStep=0.6, atrLen=14, useRegime=True, adxLen=14, adxMax=22.0, bbLen=20, bbwMax=8.0, emaLen=200,
            qtyPct=5.0, maxOpen=6, stopAtr=1.0, tpEdge=True, cooldown=12, useSpike=True, spikeRatio=1.8, spikeRange=2.5,
            spikeCool=6, useCb=True, cbStreak=4, cbDd=10.0, cbPause=24, hardDd=20.0, useWk=False, sideFilt=0)
