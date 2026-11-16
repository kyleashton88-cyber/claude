"""Second pass. Static range, screener gate, full bot budget.

Selection uses only bars before 16 May 2026, pooled across every coin.
The window 16 May 2026 through 15 Nov 2026 is evaluated after the lock.

Objective, pre-registered: deployment win rate, weighted by the number of
deployments. A candidate needs at least 80 deployments. Within 0.02 on the
win rate, the higher mean return on bot capital wins, then the smaller
average drawdown.

A deployment wins when its pnl on the 10,000 bot budget is above zero
after fees, slippage and any funding the candle window actually contains.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

from engine import align_funding, prepare
from screener import lag_one, map_to_lower, range_fit_mask, raw_metrics
from static_sim import StaticParams, simulate_static, wilson
from engine import Params, simulate as simulate_moving

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
OUT = ROOT / "results"
OUT.mkdir(exist_ok=True)

IS_START = datetime(2021, 1, 1, tzinfo=timezone.utc)
IS_END = datetime(2026, 5, 16, tzinfo=timezone.utc)
OOS_END = datetime(2026, 11, 16, tzinfo=timezone.utc)
COINS = ["BTC-USDT", "ETH-USDT", "SOL-USDT", "ZEC-USDT", "XRP-USDT", "LINK-USDT"]
TFS = ["1h", "4h"]
BAR_MS = {"1h": 3_600_000, "4h": 14_400_000}
BOT = 10_000.0


def ms(dt):
    return int(dt.timestamp() * 1000)


def slice_idx(t, start, end):
    i0 = int(np.searchsorted(t, start, side="left"))
    i1 = int(np.searchsorted(t, end, side="right"))
    # end is exclusive via the next window's start, so side left would drop a bar
    # sitting exactly on the boundary. IS_END is also OOS start, so use left for end.
    i1 = int(np.searchsorted(t, end, side="left"))
    return i0, i1


def load_pack(inst, tf, tick):
    df = pd.read_csv(DATA / f"{inst.replace('-', '')}_{tf}.csv")
    t = df.t.to_numpy(np.int64)
    o = df.o.to_numpy(float)
    h = df.h.to_numpy(float)
    l = df.l.to_numpy(float)
    c = df.c.to_numpy(float)
    v = df.vol.to_numpy(float)
    return {"t": t, "o": o, "h": h, "l": l, "c": c, "v": v, "tick": tick, "inst": inst, "tf": tf}


def weekday_mask(t, bar_ms):
    close_t = pd.to_datetime(t + bar_ms, unit="ms", utc=True).tz_convert("Australia/Sydney")
    return np.asarray(close_t.day_of_week < 5)


def resample_4h(pack):
    t, o, h, l, c, v = pack["t"], pack["o"], pack["h"], pack["l"], pack["c"], pack["v"]
    key = t // (4 * BAR_MS["1h"])
    rows = []
    start = 0
    for i in range(1, len(t) + 1):
        if i == len(t) or key[i] != key[start]:
            sl = slice(start, i)
            rows.append((int(t[start]), o[start], float(h[sl].max()), float(l[sl].min()), c[i - 1], float(v[sl].sum())))
            start = i
    arr = np.array(rows, dtype=float)
    return {"t": arr[:, 0].astype(np.int64), "o": arr[:, 1], "h": arr[:, 2], "l": arr[:, 3], "c": arr[:, 4], "v": arr[:, 5]}


def screener_allow(pack):
    """Neutral range-fit from the screener, lagged, plus a Sydney weekday."""
    if pack["tf"] == "4h":
        score, mode = raw_metrics(pack["h"], pack["l"], pack["c"], pack["v"], 4 * 3600)
        fit = range_fit_mask(lag_one(score), lag_one(mode))
    else:
        hi = resample_4h(pack)
        score, mode = raw_metrics(hi["h"], hi["l"], hi["c"], hi["v"], 4 * 3600)
        lagged_s = lag_one(score)
        lagged_m = lag_one(mode)
        fit_s = map_to_lower(hi["t"], 4 * BAR_MS["1h"], lagged_s, pack["t"])
        fit_m = map_to_lower(hi["t"], 4 * BAR_MS["1h"], lagged_m, pack["t"])
        fit = range_fit_mask(fit_s, fit_m)
    wk = weekday_mask(pack["t"], BAR_MS[pack["tf"]])
    return np.asarray(fit & wk)


def vol_hot(c, lookback=180, window=30):
    r = np.zeros(len(c))
    r[1:] = np.diff(np.log(np.maximum(c, 1e-12)))
    rv = pd.Series(r).rolling(window, min_periods=window).std().to_numpy()
    hot = np.zeros(len(c), dtype=bool)
    for i in range(lookback, len(c)):
        hist = rv[i - lookback:i]
        hist = hist[~np.isnan(hist)]
        if len(hist) < lookback // 2 or np.isnan(rv[i]):
            continue
        hot[i] = rv[i] > np.percentile(hist, 80)
    return hot


def btc_down_mask(btc_t, btc_c, t, bars_30d):
    """True on alt bars when BTC's trailing 30-day return is below -10%."""
    ret = np.full(len(btc_c), np.nan)
    if len(btc_c) > bars_30d:
        ret[bars_30d:] = btc_c[bars_30d:] / btc_c[:-bars_30d] - 1.0
    down = np.where(np.isnan(ret), False, ret < -0.10)
    idx = np.searchsorted(btc_t, t, side="right") - 1
    out = np.zeros(len(t), dtype=bool)
    ok = idx >= 0
    out[ok] = down[idx[ok]]
    return out


def max_dd(equity):
    peak = equity[0]
    dd = 0.0
    for v in equity:
        peak = max(peak, v)
        if peak > 0:
            dd = max(dd, (peak - v) / peak)
    return float(dd)


def run_one(pack, i0, i1, sp, allow):
    sl = slice(i0, i1)
    res = simulate_static(
        pack["t"][sl], pack["o"][sl], pack["h"][sl], pack["l"][sl], pack["c"][sl],
        sp, pack["tick"], allow[sl], funding=pack["funding"][sl], prepared=pack["prep_slice"](i0, i1),
    )
    deps = res["deployments"]
    cycles = res["cycles"]
    wins = sum(1 for d in deps if d["pnl"] > 0)
    n = len(deps)
    lo, hi = wilson(wins, n)
    stops = [d for d in deps if d["reason"] == "stop"]
    return {
        "deployments_rows": deps,
        "n": n,
        "wins": wins,
        "win": (wins / n) if n else None,
        "ci_lo": lo,
        "ci_hi": hi,
        "meaningful": n >= 20,
        "mean_ret": float(np.mean([d["ret"] for d in deps])) if n else None,
        "net_pnl": float(sum(d["pnl"] for d in deps)),
        "max_dd": max_dd(res["equity"]),
        "cycles": len(cycles),
        "cycle_win": (sum(1 for x in cycles if x["pnl"] > 0) / len(cycles)) if cycles else None,
        "stops": len(stops),
        "stop_mean_ret": float(np.mean([d["ret"] for d in stops])) if stops else None,
        "stop_pnl": float(sum(d["pnl"] for d in stops)) if stops else 0.0,
        "time_in_market": (sum(d["end"] - d["i"] for d in deps) / res["bars"]) if res["bars"] else 0.0,
        "open_pnl": res["open_pnl"],
        "equity": res["equity"],
        "t": pack["t"][sl],
    }


def specs():
    rows = []
    for levels in (6, 8, 10):
        for method in ("ATR", "Bollinger Bands"):
            for stop in (2.0, 5.0):
                for spacing in (1.25, 2.0):
                    rows.append(dict(levels=levels, method=method, stop_pct=stop, min_spacing_pct=spacing))
    return rows


def make(mode, spec, exit_mode="per_level"):
    return StaticParams(
        mode=mode, exit_mode=exit_mode, bot_capital=BOT,
        levels=spec["levels"], method=spec["method"], stop_pct=spec["stop_pct"],
        min_spacing_pct=spec["min_spacing_pct"],
    )


def pool(rows):
    deps = [d for r in rows for d in r["deployments_rows"]]
    n = len(deps)
    if n < 80:
        return None
    wins = sum(1 for d in deps if d["pnl"] > 0)
    return wins / n, float(np.mean([d["ret"] for d in deps])), -float(np.mean([r["max_dd"] for r in rows])), n


def better(a, b):
    if a is None:
        return False
    if b is None:
        return True
    if abs(a[0] - b[0]) > 0.02:
        return a[0] > b[0]
    if abs(a[1] - b[1]) > 1e-9:
        return a[1] > b[1]
    return a[2] > b[2]


def allow_for(pack, kind):
    base = pack["fit"]
    if kind == "none":
        base = np.ones(len(pack["t"]), dtype=bool) & pack["weekday"]
    elif kind == "vol":
        base = base & ~pack["vol_hot"]
    elif kind == "btc":
        if pack["inst"] == "BTC-USDT":
            pass
        else:
            base = base & ~pack["btc_down"]
    return base


def evaluate(books, mode, spec, exit_mode, kind, i0="is0", i1="is1"):
    sp = make(mode, spec, exit_mode)
    rows = []
    for inst in COINS:
        for tf in TFS:
            pack = books[(inst, tf)]
            allow = allow_for(pack, "fit" if kind == "fit" else kind)
            if kind == "fit":
                allow = pack["fit"]
            m = run_one(pack, pack[i0], pack[i1], sp, allow)
            m.update({"inst": inst, "tf": tf, "mode": mode, "exit": exit_mode, "gate": kind, **spec})
            rows.append(m)
    return rows


def slim(m):
    keep = ["inst", "tf", "mode", "exit", "gate", "levels", "method", "stop_pct", "min_spacing_pct",
            "n", "wins", "win", "ci_lo", "ci_hi", "meaningful", "mean_ret", "net_pnl", "max_dd",
            "cycles", "cycle_win", "stops", "stop_mean_ret", "stop_pnl", "time_in_market", "open_pnl"]
    return {k: m.get(k) for k in keep}


def _scale_curve(returns, start=10_000.0):
    equity = start
    peak = start
    frac = 0.25
    wins = 0
    curve = [equity]
    for r in returns:
        if frac >= 0.25 and wins >= 3 and peak > 0 and (peak - equity) / peak < 0.08:
            frac = min(0.50, frac + 0.10)
            wins = 0
        bot = equity * frac
        equity = equity + bot * float(r)
        if equity > peak:
            peak = equity
            if frac < 0.25:
                frac = 0.25
        elif peak > 0 and (peak - equity) / peak > 0.15:
            frac = max(0.10, frac / 2.0)
        wins = wins + 1 if r > 0 else 0
        curve.append(equity)
    peak = curve[0]
    dd = 0.0
    for v in curve:
        peak = max(peak, v)
        if peak > 0:
            dd = max(dd, (peak - v) / peak)
    return np.array(curve), float(dd)


def _monte(returns, n_paths=2000, seed=16):
    rng = np.random.default_rng(seed)
    if len(returns) == 0:
        return {"p05": 10000.0, "p50": 10000.0, "dd50": 0.0, "dd95": 0.0}
    terminals, dds = [], []
    for _ in range(n_paths):
        sample = rng.choice(returns, size=len(returns), replace=True)
        curve, dd = _scale_curve(sample)
        terminals.append(curve[-1])
        dds.append(dd)
    terminals = np.sort(np.array(terminals))
    dds = np.sort(np.array(dds))
    return {
        "p05": float(terminals[int(0.05 * (len(terminals) - 1))]),
        "p50": float(np.median(terminals)),
        "dd50": float(np.median(dds)),
        "dd95": float(dds[int(0.95 * (len(dds) - 1))]),
    }


def main():
    manifest = json.loads((DATA / "manifest.json").read_text())
    books = {}
    print("load", flush=True)
    raw = {}
    for inst in COINS:
        tick = manifest["symbols"][inst]["tick"]
        for tf in TFS:
            pack = load_pack(inst, tf, tick)
            fund_path = DATA / f"{inst.replace('-', '')}_funding.csv"
            fund = pd.read_csv(fund_path) if fund_path.exists() else pd.DataFrame({"t": [], "rate": []})
            pack["funding"] = align_funding(pack["t"], fund.t.to_numpy(np.int64) if len(fund) else np.array([], dtype=np.int64),
                                            fund.rate.to_numpy(float) if len(fund) else np.array([]))
            ep = Params()
            ind = prepare(pack["o"], pack["h"], pack["l"], pack["c"], ep)
            # prepare uses default lengths; static search does not change them
            def slicer(ind=ind):
                def cut(i0, i1):
                    sl = slice(i0, i1)
                    return {"ema": ind["ema"][sl], "atr": ind["atr"][sl],
                            "bb": tuple(a[sl] for a in ind["bb"]), "adx": ind["adx"][sl], "trend": ind["trend"][sl]}
                return cut
            pack["prep_slice"] = slicer()
            pack["is0"], pack["is1"] = slice_idx(pack["t"], ms(IS_START), ms(IS_END))
            pack["oos0"], pack["oos1"] = slice_idx(pack["t"], ms(IS_END), ms(OOS_END))
            pack["vol_hot"] = vol_hot(pack["c"])
            pack["weekday"] = weekday_mask(pack["t"], BAR_MS[tf])
            raw[(inst, tf)] = pack
            print(inst, tf, "bars", len(pack["t"]), "is", pack["is1"] - pack["is0"], "oos", pack["oos1"] - pack["oos0"], flush=True)
    print("screener", flush=True)
    for inst in COINS:
        for tf in TFS:
            pack = raw[(inst, tf)]
            pack["fit"] = screener_allow(pack) & pack["weekday"]
            print(" ", inst, tf, "fit bars", int(pack["fit"].sum()), flush=True)
    btc_1h = raw[("BTC-USDT", "1h")]
    btc_4h = raw[("BTC-USDT", "4h")]
    for inst in COINS:
        for tf in TFS:
            pack = raw[(inst, tf)]
            src = btc_1h if tf == "1h" else btc_4h
            bars = 24 * 30 if tf == "1h" else 6 * 30
            pack["btc_down"] = btc_down_mask(src["t"], src["c"], pack["t"], bars)
            books[(inst, tf)] = pack

    log = []
    chosen = {}
    grid = specs()
    print("settings", len(grid), "per mode", flush=True)
    for mode in ("Arithmetic", "Geometric"):
        best = None
        best_spec = grid[0]
        for n, spec in enumerate(grid, start=1):
            rows = evaluate(books, mode, spec, "per_level", "fit")
            sc = pool(rows)
            log.append({"stage": "is_settings", "mode": mode, "exit": "per_level", "gate": "fit", "spec": spec,
                        "win": None if sc is None else sc[0], "ret": None if sc is None else sc[1],
                        "dd": None if sc is None else -sc[2], "n": 0 if sc is None else sc[3]})
            if better(sc, best):
                best, best_spec = sc, spec
            if n % 4 == 0:
                print(f"  {mode} {n}/{len(grid)}", None if best is None else round(best[0], 3), flush=True)
        chosen[mode] = {"spec": best_spec, "is": None if best is None else {"win": best[0], "ret": best[1], "neg_dd": best[2], "n": best[3]}}
        print("locked settings", mode, best_spec, chosen[mode]["is"], flush=True)

    families = [
        ("per_level", "fit"),
        ("close_all", "fit"),
        ("trail", "fit"),
        ("above_avg", "fit"),
        ("per_level", "none"),
        ("per_level", "vol"),
        ("per_level", "btc"),
    ]
    family_choice = {}
    for mode in ("Arithmetic", "Geometric"):
        spec = chosen[mode]["spec"]
        best = None
        best_fam = ("per_level", "fit")
        print("families", mode, flush=True)
        for exit_mode, gate in families:
            rows = evaluate(books, mode, spec, exit_mode, gate)
            sc = pool(rows)
            log.append({"stage": "is_family", "mode": mode, "exit": exit_mode, "gate": gate, "spec": spec,
                        "win": None if sc is None else sc[0], "ret": None if sc is None else sc[1],
                        "dd": None if sc is None else -sc[2], "n": 0 if sc is None else sc[3]})
            print(" ", exit_mode, gate, None if sc is None else (round(sc[0], 3), round(sc[1], 4), sc[3]), flush=True)
            if better(sc, best):
                best, best_fam = sc, (exit_mode, gate)
        family_choice[mode] = {"exit": best_fam[0], "gate": best_fam[1],
                               "is": None if best is None else {"win": best[0], "ret": best[1], "neg_dd": best[2], "n": best[3]}}

    # Out of sample starts here. One locked system, plus the pre-registered
    # family list as a holdout table, plus the previous moving-band rule
    # re-run on the same 10,000 bot budget.
    oos_rows = []
    is_rows = []
    equity = {}
    scale_returns = []
    for mode in ("Arithmetic", "Geometric"):
        spec = chosen[mode]["spec"]
        exit_mode, gate = family_choice[mode]["exit"], family_choice[mode]["gate"]
        for split, a, b in (("is", "is0", "is1"), ("oos", "oos0", "oos1")):
            rows = evaluate(books, mode, spec, exit_mode, gate, a, b)
            for m in rows:
                rec = slim(m)
                rec["split"] = split
                rec["label"] = "locked"
                (oos_rows if split == "oos" else is_rows).append(rec)
                if split == "oos":
                    for d in m["deployments_rows"]:
                        scale_returns.append((d["t"], d["ret"]))
                    if m["inst"] in ("BTC-USDT", "ETH-USDT", "SOL-USDT", "ZEC-USDT") and m["tf"] == "4h":
                        equity[f"{mode}|{m['inst']}|4h"] = {"t": m["t"].tolist(), "equity": np.asarray(m["equity"]).tolist()}
        # holdout of the other families, not used to change the lock
        for exit_mode_h, gate_h in families:
            if (exit_mode_h, gate_h) == (exit_mode, gate):
                continue
            rows = evaluate(books, mode, spec, exit_mode_h, gate_h, "oos0", "oos1")
            sc = pool(rows)
            log.append({"stage": "oos_holdout_not_used", "mode": mode, "exit": exit_mode_h, "gate": gate_h,
                        "spec": spec, "win": None if sc is None else sc[0], "ret": None if sc is None else sc[1],
                        "dd": None if sc is None else -sc[2], "n": 0 if sc is None else sc[3]})

    # Previous rule, full bot budget: moving band, pass-1 settings, risk cap removed.
    before = []
    prev = dict(levels=6, adx_threshold=20.0, stop_pct=2.0, method="Bollinger Bands", min_spacing_pct=2.0)
    for mode in ("Arithmetic", "Geometric"):
        sp = Params(mode=mode, initial_capital=BOT, notional_pct=1.0 / 6.0, risk_pct=100.0,
                    max_entries=6, max_position=1e12, levels=6, adx_threshold=20.0, stop_pct=2.0,
                    method="Bollinger Bands", min_spacing_pct=2.0, structure="moving")
        for inst in COINS:
            for tf in TFS:
                pack = books[(inst, tf)]
                for split, i0, i1 in (("oos", pack["oos0"], pack["oos1"]),):
                    sl = slice(i0, i1)
                    ind = pack["prep_slice"](i0, i1)
                    res = simulate_moving(pack["t"][sl], pack["o"][sl], pack["h"][sl], pack["l"][sl], pack["c"][sl],
                                          sp, pack["tick"], prepared=ind, funding=pack["funding"][sl])
                    deps = res["deployments"]
                    # express pnl as a return on the 10,000 budget
                    for d in deps:
                        d["ret"] = d["pnl"] / BOT
                    wins = sum(1 for d in deps if d["pnl"] > 0)
                    n = len(deps)
                    lo, hi = wilson(wins, n)
                    stops = [d for d in deps if d["reason"] == "stop"]
                    before.append({
                        "inst": inst, "tf": tf, "mode": mode, "split": "oos", "label": "pass1_full_budget",
                        "n": n, "wins": wins, "win": (wins / n) if n else None, "ci_lo": lo, "ci_hi": hi,
                        "meaningful": n >= 20, "mean_ret": float(np.mean([d["ret"] for d in deps])) if n else None,
                        "net_pnl": float(sum(d["pnl"] for d in deps)), "max_dd": max_dd(res["equity"]),
                        "stops": len(stops),
                        "stop_mean_ret": float(np.mean([d["ret"] for d in stops])) if stops else None,
                        "cycle_win": None, "levels": 6, "method": "Bollinger Bands", "stop_pct": 2.0,
                        "min_spacing_pct": 2.0, "exit": "close_all", "gate": "original_pause",
                    })

    summary = {
        "disclaimer": "Hypothetical backtest, not a forecast. Past performance is not a reliable indicator of future results. Education only. Not financial advice.",
        "bot_capital": BOT,
        "sizing": "Fixed 10,000 bot budget. 100% is reserved for the buy levels below the launch price, equal notional, fees included. Return is pnl divided by 10,000.",
        "split": {"is": ["2021-01-01", "2026-05-15"], "oos": ["2026-05-16", "2026-11-15"]},
        "variants_logged": len(log),
        "setting_grid": len(grid),
        "chosen_settings": chosen,
        "family": family_choice,
        "pass1_settings": prev,
        "target": "75% out-of-sample deployment win rate on cells with at least 20 deployments. A smaller cell is not a result.",
    }
    (OUT / "pass2_summary.json").write_text(json.dumps(summary, indent=2, default=float))
    (OUT / "pass2_variants.json").write_text(json.dumps(log, indent=2, default=float))
    (OUT / "pass2_is.json").write_text(json.dumps(is_rows, indent=2, default=float))
    (OUT / "pass2_oos.json").write_text(json.dumps(oos_rows, indent=2, default=float))
    (OUT / "pass2_before.json").write_text(json.dumps(before, indent=2, default=float))
    (OUT / "pass2_equity.json").write_text(json.dumps(equity))
    scale_returns.sort()
    rets = np.array([r for _t, r in scale_returns], dtype=float)
    curve, dd = _scale_curve(rets)
    mc = _monte(rets)
    (OUT / "pass2_scale.json").write_text(json.dumps({
        "end": float(curve[-1]) if len(curve) else 10000.0,
        "max_dd": dd, "curve": curve.tolist(),
        "p05": mc["p05"], "p50": mc["p50"], "dd50": mc["dd50"], "dd95": mc["dd95"],
        "n": int(len(rets)),
    }))
    print("variants", len(log))
    print("wrote", OUT)


if __name__ == "__main__":
    main()
