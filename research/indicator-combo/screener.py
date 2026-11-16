"""Grid-Fit score from grid-screener-4h.pine and the weekday file.

The weights, bands, spike rule and the [1] lag match f_metrics().
A launch is allowed only when the lagged score is at least 60, the lagged
mode is neutral (ADX below 22 and Bollinger width below 8%), the lagged
quote-volume test passes, the bar is not in a spike cooldown, and the
execution bar closes on a Sydney weekday. That is the deployment gate.

On a 4h series the score is this series. On a 1h series the score is the
4h screener: the last completed 4h bar's f_metrics() value, which itself
returns the previous 4h bar's raw score.

Liquidity uses the 4h file's definition: average quote volume per hour
over the last 24 hours, minimum 2,000,000 USDT. Quote volume is close
times base volume, which is what OKX spot candles provide.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from engine import atr, bollinger, dmi, ema

RANGE_LEN = 100
HIST_LEN = 300
CROSS_LEN = 100
ADX_MAX = 22.0
BBW_LO = 2.0
BBW_HI = 8.0
ATR_LO = 0.4
ATR_HI = 1.8
MIN_QVOL = 2_000_000.0
MIN_SCORE = 60.0
SPIKE_RATIO = 1.8
SPIKE_RANGE = 2.5
SPIKE_COOL = 6


def f_band(x, lo, hi):
    if x is None or (isinstance(x, float) and np.isnan(x)):
        return 0.0
    if lo <= x <= hi:
        return 1.0
    if x < lo:
        return max(0.0, x / lo * 2.0 - 1.0) if lo else 0.0
    return max(0.0, 1.0 - (x - hi) / hi) if hi else 0.0


def _rolling_max(x, w):
    return pd.Series(x).rolling(w, min_periods=w).max().to_numpy()


def _rolling_min(x, w):
    return pd.Series(x).rolling(w, min_periods=w).min().to_numpy()


def raw_metrics(h, l, c, v, bar_seconds):
    """Score and mode on each bar, before the [1] lag and before liquidity."""
    n = len(c)
    _p, _m, adx = dmi(h, l, c, 14, 14)
    _mid, up, lo_bb = bollinger(c, 20, 2.0)
    mid = pd.Series(c).rolling(20, min_periods=20).mean().to_numpy()
    bbw = np.full(n, np.nan)
    ok = (mid != 0) & ~np.isnan(mid) & ~np.isnan(up)
    bbw[ok] = (up[ok] - lo_bb[ok]) / mid[ok] * 100.0
    a14 = atr(h, l, c, 14)
    with np.errstate(divide="ignore", invalid="ignore"):
        atr_p = np.where(c > 0, a14 / c * 100.0, np.nan)
    hi = _rolling_max(h, RANGE_LEN)
    lo = _rolling_min(l, RANGE_LEN)
    ema200 = ema(c, 200)
    ema50 = ema(c, 50)
    inside = np.zeros(n)
    for i in range(RANGE_LEN, n):
        href, lref = hi[i - RANGE_LEN], lo[i - RANGE_LEN]
        if np.isnan(href) or np.isnan(lref):
            continue
        inside[i] = 1.0 if (lref <= c[i] <= href) else 0.0
    fit = pd.Series(inside).rolling(HIST_LEN, min_periods=HIST_LEN).mean().to_numpy() * 100.0
    above = c > ema50
    cross = np.zeros(n)
    for i in range(1, n):
        if np.isnan(ema50[i]) or np.isnan(ema50[i - 1]):
            continue
        if above[i] != above[i - 1]:
            cross[i] = 1.0
    xs = pd.Series(cross).rolling(CROSS_LEN, min_periods=1).sum().to_numpy()
    bars24 = max(1, int(round(86400.0 / bar_seconds)))
    quote = c * v
    qv = pd.Series(quote).rolling(bars24, min_periods=bars24).sum().to_numpy() / 24.0
    a_base = pd.Series(a14).rolling(100, min_periods=100).mean().to_numpy()
    spike = np.zeros(n)
    for i in range(n):
        if np.isnan(a14[i]):
            continue
        ratio = a14[i] / a_base[i] if (not np.isnan(a_base[i]) and a_base[i] > 0) else 0.0
        wide = (h[i] - l[i]) > SPIKE_RANGE * a14[i]
        spike[i] = 1.0 if (ratio > SPIKE_RATIO or wide) else 0.0
    spiking = pd.Series(spike).rolling(SPIKE_COOL + 1, min_periods=1).max().to_numpy() > 0
    score = np.full(n, np.nan)
    mode = np.zeros(n)  # 0 neutral, 1 long, -1 short
    for i in range(n):
        if np.isnan(adx[i]) or np.isnan(fit[i]) or np.isnan(qv[i]):
            continue
        s_adx = min(1.0, max(0.0, (ADX_MAX * 1.6 - adx[i]) / (ADX_MAX * 0.8)))
        s_bbw = f_band(0.0 if np.isnan(bbw[i]) else bbw[i], BBW_LO, BBW_HI)
        s_atr = f_band(0.0 if np.isnan(atr_p[i]) else atr_p[i], ATR_LO, ATR_HI)
        s_x = min(1.0, xs[i] / 8.0)
        s_fit = 0.0 if np.isnan(fit[i]) else fit[i] / 100.0
        sc = 100.0 * (0.25 * s_adx + 0.15 * s_bbw + 0.15 * s_atr + 0.15 * s_x + 0.30 * s_fit)
        if spiking[i]:
            sc = -2.0
        if qv[i] < MIN_QVOL:
            sc = -1.0
        score[i] = sc
        if adx[i] < ADX_MAX and not np.isnan(bbw[i]) and bbw[i] < BBW_HI:
            mode[i] = 0.0
        elif not np.isnan(ema200[i]) and c[i] > ema200[i]:
            mode[i] = 1.0
        else:
            mode[i] = -1.0
    return score, mode


def lag_one(x):
    out = np.full(len(x), np.nan)
    out[1:] = x[:-1]
    return out


def map_to_lower(high_open, high_ms, values, low_open):
    """Last higher-timeframe bar whose close is at or before the lower bar's open."""
    closed = high_open + high_ms
    idx = np.searchsorted(closed, low_open, side="right") - 1
    out = np.full(len(low_open), np.nan)
    ok = idx >= 0
    out[ok] = values[idx[ok]]
    return out


def range_fit_mask(score_lagged, mode_lagged):
    """True when the screener would treat the market as a neutral range fit."""
    return (score_lagged >= MIN_SCORE) & (mode_lagged == 0.0)
