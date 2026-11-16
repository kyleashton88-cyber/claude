"""Pine-faithful indicator helpers (ta.rma / ta.ema / ta.atr / ta.dmi / ta.bb / ta.highest / ta.lowest)."""
import numpy as np, pandas as pd
from functools import lru_cache

def rma(x, n):
    x = np.asarray(x, float); out = np.full(len(x), np.nan)
    a = 1.0 / n; s = np.nan; buf = []
    for i, v in enumerate(x):
        if np.isnan(s):
            if not np.isnan(v):
                buf.append(v)
                if len(buf) == n: s = np.mean(buf); out[i] = s
        else:
            s = a * (v if not np.isnan(v) else 0) + (1 - a) * s; out[i] = s
    return out

def ema(x, n):
    x = np.asarray(x, float); out = np.full(len(x), np.nan)
    a = 2.0 / (n + 1); s = np.nan; buf = []
    for i, v in enumerate(x):
        if np.isnan(s):
            if not np.isnan(v):
                buf.append(v)
                if len(buf) == n: s = np.mean(buf); out[i] = s
        else:
            s = a * v + (1 - a) * s; out[i] = s
    return out

def tr(h, l, c):
    pc = np.r_[np.nan, c[:-1]]
    t = np.maximum(h - l, np.maximum(np.abs(h - pc), np.abs(l - pc)))
    t[0] = h[0] - l[0]
    return t

def atr(h, l, c, n): return rma(tr(h, l, c), n)

def dmi(h, l, c, n, sm):
    up = np.r_[np.nan, np.diff(h)]; dn = -np.r_[np.nan, np.diff(l)]
    pdm = np.where((up > dn) & (up > 0), up, 0.0); mdm = np.where((dn > up) & (dn > 0), dn, 0.0)
    pdm[0] = np.nan; mdm[0] = np.nan
    trr = rma(tr(h, l, c), n)
    p = pd.Series(100 * rma(pdm, n) / trr).ffill().values
    m = pd.Series(100 * rma(mdm, n) / trr).ffill().values
    s = p + m
    dx = np.abs(p - m) / np.where(s == 0, 1, s)
    return p, m, 100 * rma(dx, sm)

def sma(x, n): return pd.Series(x).rolling(n, min_periods=n).mean().values
def stdev(x, n): return pd.Series(x).rolling(n, min_periods=n).std(ddof=0).values
def highest(x, n): return pd.Series(x).rolling(n, min_periods=n).max().values
def lowest(x, n): return pd.Series(x).rolling(n, min_periods=n).min().values

def load(sym, tf):
    df = pd.read_csv(f"/workspace/tradingview/optimisation-2026-11-10/data/{sym}_{tf}.csv")
    return df
