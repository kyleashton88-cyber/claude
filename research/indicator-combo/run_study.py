"""In-sample search, then one out-of-sample report.

Rules locked before any out-of-sample number is computed:

- Win, cycle: a closed lot whose pnl is positive after fees and slippage.
- Win, deployment: a flat-to-flat episode whose combined pnl is positive after fees and slippage.
- The 75% target is judged on the out-of-sample deployment win rate. Cycle win rate is reported beside it.
- Tune only on BTC and ETH, 1h and 4h, from 2023-11-16 through 2026-05-15.
- Objective: mean deployment win rate across those four series. A variant needs at least 20 deployments in total. Ties within 0.02 go to the higher mean net return, then the smaller mean drawdown.
- Out-of-sample is 2026-05-16 through 2026-11-15, including the November 2026 sell-off. It is not used to pick a variant.
- Order size in the reported runs is 5% of marked equity per new order, still under the script's 1% hard-stop risk cap and 6-entry cap. Fixed quantity 1 on a 1,000,000 account is saved only as a sizing check, because that quantity is a different fraction of price on every coin.

Deep-search families, also scored only on the in-sample window:

- moving: the original range, rewritten every bar
- anchor: keep the range until a rebuild while flat
- anchor_drift: anchor, and no new buys when the picks-screen gate is on (drift30 > 0.8 and ADX > 40)
- anchor_vol: anchor, and no new buys when ATR/close is above its prior 180-bar 80th percentile
- per_level: anchored range, one lot per crossed level, exit at the next level instead of closing every lot

Walk-forward stays inside the in-sample window. Three test folds, each retuned on the bars before it.
"""
from __future__ import annotations

import json
from dataclasses import replace
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

from engine import (
    Params, align_funding, daily_drift_block, metrics, prepare, simulate, slice_idx, vol_hot_flag,
)

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
OUT = ROOT / "results"
OUT.mkdir(parents=True, exist_ok=True)

IS_START = datetime(2023, 11, 16, tzinfo=timezone.utc)
IS_END = datetime(2026, 5, 16, tzinfo=timezone.utc)
OOS_END = datetime(2026, 11, 16, tzinfo=timezone.utc)
FOLDS = [
    (datetime(2024, 11, 16, tzinfo=timezone.utc), datetime(2025, 5, 16, tzinfo=timezone.utc)),
    (datetime(2025, 5, 16, tzinfo=timezone.utc), datetime(2025, 11, 16, tzinfo=timezone.utc)),
    (datetime(2025, 11, 16, tzinfo=timezone.utc), datetime(2026, 5, 16, tzinfo=timezone.utc)),
]
TUNE = ["BTC-USDT", "ETH-USDT"]
ALL = ["BTC-USDT", "ETH-USDT", "SOL-USDT", "ZEC-USDT", "XRP-USDT", "LINK-USDT"]
TFS = ["1h", "4h"]


def ms(dt):
    return int(dt.timestamp() * 1000)


def load_symbol(inst, tf, tick):
    path = DATA / f"{inst.replace('-', '')}_{tf}.csv"
    df = pd.read_csv(path)
    t = df.t.to_numpy(np.int64)
    o = df.o.to_numpy(float)
    h = df.h.to_numpy(float)
    l = df.l.to_numpy(float)
    c = df.c.to_numpy(float)
    base = Params()
    ind = prepare(o, h, l, c, base)
    drift = daily_drift_block(t, h, l, c)
    hot = vol_hot_flag(h, l, c)
    fpath = DATA / f"{inst.replace('-', '')}_funding.csv"
    if fpath.exists():
        fund = pd.read_csv(fpath)
        funding = align_funding(t, fund.t.to_numpy(np.int64), fund.rate.to_numpy(float))
    else:
        funding = np.zeros(len(t))
    return {"t": t, "o": o, "h": h, "l": l, "c": c, "ind": ind, "drift": drift,
            "hot": hot, "funding": funding, "tick": tick, "inst": inst, "tf": tf}


def run(pack, i0, i1, p: Params, with_funding=False):
    sl = slice(i0, i1)
    ind = {
        "ema": pack["ind"]["ema"][sl],
        "atr": pack["ind"]["atr"][sl],
        "bb": tuple(a[sl] for a in pack["ind"]["bb"]),
        "adx": pack["ind"]["adx"][sl],
        "trend": pack["ind"]["trend"][sl],
    }
    fund = pack["funding"][sl] if with_funding else None
    res = simulate(
        pack["t"][sl], pack["o"][sl], pack["h"][sl], pack["l"][sl], pack["c"][sl],
        p, pack["tick"], prepared=ind, drift_block=pack["drift"][sl], vol_hot=pack["hot"][sl],
        funding=fund,
    )
    m = metrics(res, p.initial_capital)
    m["deployments_rows"] = res["deployments"]
    m["equity"] = res["equity"]
    m["t"] = pack["t"][sl]
    return m


def grid():
    rows = []
    for levels in (6, 8, 10):
        for adx in (20.0, 30.0):
            for stop in (0.75, 2.0):
                for method in ("ATR", "Bollinger Bands"):
                    for spacing in (1.25, 2.0):
                        rows.append(dict(levels=levels, adx_threshold=adx, stop_pct=stop,
                                         method=method, min_spacing_pct=spacing))
    return rows


def make_params(mode, spec, family="moving"):
    p = Params(
        mode=mode, initial_capital=10_000.0, notional_pct=0.05,
        levels=spec["levels"], adx_threshold=spec["adx_threshold"], stop_pct=spec["stop_pct"],
        method=spec["method"], min_spacing_pct=spec["min_spacing_pct"],
    )
    if family == "anchor":
        p.structure = "anchor"
    elif family == "anchor_drift":
        p.structure = "anchor"
        p.use_drift_gate = True
    elif family == "anchor_vol":
        p.structure = "anchor"
        p.use_vol_gate = True
    elif family == "per_level":
        p.structure = "per_level"
    elif family == "moving":
        p.structure = "moving"
    else:
        raise ValueError(family)
    return p


def better(a, b):
    """True if score a beats score b. None loses."""
    if a is None:
        return False
    if b is None:
        return True
    aw, an, ad = a
    bw, bn, bd = b
    if abs(aw - bw) > 0.02:
        return aw > bw
    if abs(an - bn) > 1e-9:
        return an > bn
    return ad > bd  # ad is negative drawdown, so larger is milder


DEFAULT_SPEC = {"levels": 8, "adx_threshold": 20.0, "stop_pct": 0.75, "method": "ATR", "min_spacing_pct": 1.25}


def score(ms, min_deps=20, min_series=None):
    if min_series is None:
        min_series = len(ms)
    deps = sum(m["deployments"] for m in ms)
    wins = [m["deployment_win_rate"] for m in ms if m["deployment_win_rate"] is not None]
    if deps < min_deps or len(wins) < min_series:
        return None
    return (
        float(np.mean(wins)),
        float(np.mean([m["net_return"] for m in ms])),
        float(-np.mean([m["max_dd"] for m in ms])),
    )


def eval_spec(books, mode, spec, family, i0_key, i1_key, coins):
    out = []
    p = make_params(mode, spec, family)
    for inst in coins:
        for tf in TFS:
            pack = books[(inst, tf)]
            m = run(pack, pack[i0_key], pack[i1_key], p)
            m.update({"inst": inst, "tf": tf, "mode": mode, "family": family, **spec})
            out.append(m)
    return out


def slim(m):
    keep = ["inst", "tf", "mode", "family", "levels", "adx_threshold", "stop_pct", "method",
            "min_spacing_pct", "net_return", "max_dd", "time_in_market", "cycle_win_rate",
            "deployment_win_rate", "cycles", "deployments", "stops", "blocked_entries",
            "blocked_then_stopped", "blocked_then_bounced", "blocked_stop_share", "end_equity",
            "open_qty"]
    return {k: m.get(k) for k in keep}


def choose(books, mode, specs, family, coins, i0_key="is0", i1_key="is1"):
    best = None
    best_spec = None
    log = []
    for n, spec in enumerate(specs, start=1):
        rows = eval_spec(books, mode, spec, family, i0_key, i1_key, coins)
        sc = score(rows)
        log.append({"n": n, "mode": mode, "family": family, "spec": spec, "score_win": None if sc is None else sc[0],
                    "score_net": None if sc is None else sc[1], "score_dd": None if sc is None else -sc[2],
                    "deployments": int(sum(r["deployments"] for r in rows))})
        if better(sc, best):
            best, best_spec = sc, spec
    if best_spec is None:
        best_spec = DEFAULT_SPEC
        if n % 8 == 0:
            print(f"  {mode} {family} {n}/{len(specs)} best={None if best is None else round(best[0], 3)}", flush=True)
    return best_spec, best, log


def regime_table(rows):
    buckets = {"adx_<20": [], "adx_20_30": [], "adx_>=30": []}
    for m in rows:
        for d in m["deployments_rows"]:
            adx = d.get("adx")
            if adx is None:
                continue
            key = "adx_<20" if adx < 20 else "adx_20_30" if adx < 30 else "adx_>=30"
            buckets[key].append(d["pnl"] > 0)
    out = {}
    for k, vals in buckets.items():
        out[k] = {"n": len(vals), "win_rate": (sum(vals) / len(vals)) if vals else None}
    return out


def scale_curve(returns, start=10_000.0):
    """Rule-based size on a sequence of account returns.

    m starts at 1. After three winning episodes and a drawdown under 8%, m steps
    to 1.25 and can reach 1.5. A drawdown past 15% cuts m to 0.5 until a new high.
    The return is scaled by m. This is a hypothetical replay, not a forecast.
    """
    equity = start
    peak = start
    m = 1.0
    wins = 0
    curve = [equity]
    mults = []
    for r in returns:
        if m >= 1.0 and wins >= 3 and peak > 0 and (peak - equity) / peak < 0.08:
            m = min(1.5, m + 0.25)
            wins = 0
        equity = equity * (1.0 + r * m)
        if equity > peak:
            peak = equity
            if m < 1.0:
                m = 1.0
        elif peak > 0 and (peak - equity) / peak > 0.15:
            m = 0.5
        wins = wins + 1 if r > 0 else 0
        curve.append(equity)
        mults.append(m)
    peak = curve[0]
    dd = 0.0
    for v in curve:
        peak = max(peak, v)
        if peak > 0:
            dd = max(dd, (peak - v) / peak)
    return np.array(curve), dd, mults


def monte_carlo(returns, n_paths=2000, seed=16):
    rng = np.random.default_rng(seed)
    returns = np.asarray(returns, dtype=float)
    if len(returns) == 0:
        return {}
    terminals = []
    dds = []
    # keep a few paths for the chart: median and a low path, chosen after the run
    saved = []
    for i in range(n_paths):
        sample = rng.choice(returns, size=len(returns), replace=True)
        curve, dd, _ = scale_curve(sample)
        terminals.append(curve[-1])
        dds.append(dd)
        if i < 400:
            saved.append(curve)
    terminals = np.sort(np.array(terminals))
    dds = np.sort(np.array(dds))
    order = np.argsort([c[-1] for c in saved])
    return {
        "paths": n_paths,
        "terminal_p05": float(terminals[int(0.05 * (len(terminals) - 1))]),
        "terminal_p50": float(np.median(terminals)),
        "terminal_p95": float(terminals[int(0.95 * (len(terminals) - 1))]),
        "maxdd_p50": float(np.median(dds)),
        "maxdd_p95": float(dds[int(0.95 * (len(dds) - 1))]),
        "median_curve": saved[order[len(order) // 2]].tolist() if saved else [],
        "low_curve": saved[order[max(0, int(0.05 * (len(order) - 1)))]].tolist() if saved else [],
    }


def main():
    manifest = json.loads((DATA / "manifest.json").read_text())
    books = {}
    for inst in ALL:
        tick = manifest["symbols"][inst]["tick"]
        for tf in TFS:
            print("load", inst, tf, flush=True)
            pack = load_symbol(inst, tf, tick)
            pack["is0"], pack["is1"] = slice_idx(pack["t"], ms(IS_START), ms(IS_END))
            pack["oos0"], pack["oos1"] = slice_idx(pack["t"], ms(IS_END), ms(OOS_END))
            books[(inst, tf)] = pack
            print("  bars", len(pack["t"]), "is", pack["is1"] - pack["is0"], "oos", pack["oos1"] - pack["oos0"],
                  "drift_on", int(pack["drift"].sum()), flush=True)

    specs = grid()
    print(f"setting variants per mode: {len(specs)}", flush=True)
    chosen = {}
    variant_log = []
    for mode in ("Arithmetic", "Geometric"):
        print("tune", mode, flush=True)
        spec, sc, log = choose(books, mode, specs, "moving", TUNE)
        for row in log:
            row["stage"] = "is_settings"
        variant_log.extend(log)
        chosen[mode] = {"spec": spec, "is_score": None if sc is None else {"win": sc[0], "net": sc[1], "neg_dd": sc[2]}}
        print(" chosen", mode, spec, chosen[mode]["is_score"], flush=True)

    families = ["moving", "anchor", "anchor_drift", "anchor_vol", "per_level"]
    deep = {}
    for mode in ("Arithmetic", "Geometric"):
        spec = chosen[mode]["spec"]
        best_f, best_sc = None, None
        print("deep", mode, flush=True)
        for fam in families:
            rows = eval_spec(books, mode, spec, fam, "is0", "is1", TUNE)
            sc = score(rows)
            variant_log.append({"stage": "is_deep", "mode": mode, "family": fam, "spec": spec,
                                "score_win": None if sc is None else sc[0],
                                "score_net": None if sc is None else sc[1],
                                "score_dd": None if sc is None else -sc[2],
                                "deployments": int(sum(r["deployments"] for r in rows)),
                                "n": 1})
            print(" ", fam, None if sc is None else round(sc[0], 3), flush=True)
            if better(sc, best_sc):
                best_f, best_sc = fam, sc
        deep[mode] = {"family": best_f, "is_score": None if best_sc is None else {"win": best_sc[0], "net": best_sc[1], "neg_dd": best_sc[2]}}

    # Walk-forward inside IS. Retune settings on the train window, then score families on the fold.
    wf_rows = []
    for fold_i, (a, b) in enumerate(FOLDS, start=1):
        print("walk-forward fold", fold_i, flush=True)
        for pack in books.values():
            pack["tr0"], pack["tr1"] = slice_idx(pack["t"], ms(IS_START), ms(a))
            pack["te0"], pack["te1"] = slice_idx(pack["t"], ms(a), ms(b))
        for mode in ("Arithmetic", "Geometric"):
            spec, sc, log = choose(books, mode, specs, "moving", TUNE, "tr0", "tr1")
            for row in log:
                row["stage"] = f"wf{fold_i}_train"
            variant_log.extend(log)
            for fam in families:
                test_rows = eval_spec(books, mode, spec if spec is not None else DEFAULT_SPEC, fam, "te0", "te1", TUNE)
                sc_te = score(test_rows, min_deps=8, min_series=2)
                wf_rows.append({"fold": fold_i, "test_start": a.date().isoformat(), "test_end": b.date().isoformat(),
                                "mode": mode, "family": fam, "spec": spec,
                                "win": None if sc_te is None else sc_te[0],
                                "net": None if sc_te is None else sc_te[1],
                                "max_dd": None if sc_te is None else -sc_te[2],
                                "deployments": int(sum(r["deployments"] for r in test_rows))})
            print("  fold", fold_i, mode, "train pick", spec, flush=True)

    # Lock is complete. Out-of-sample starts here.
    oos_rows = []
    is_rows = []
    equity_store = {}
    dep_store = {}
    for mode in ("Arithmetic", "Geometric"):
        spec = chosen[mode]["spec"]
        fam = deep[mode]["family"]
        for label, family in (("settings", "moving"), ("deep", fam)):
            p = make_params(mode, spec, family)
            for inst in ALL:
                for tf in TFS:
                    pack = books[(inst, tf)]
                    for split, i0, i1 in (("is", pack["is0"], pack["is1"]), ("oos", pack["oos0"], pack["oos1"])):
                        m = run(pack, i0, i1, p, with_funding=False)
                        m.update({"inst": inst, "tf": tf, "mode": mode, "family": family, "label": label,
                                  "split": split, **spec})
                        slim_m = slim(m)
                        slim_m["label"] = label
                        slim_m["split"] = split
                        (oos_rows if split == "oos" else is_rows).append(slim_m)
                        if split == "oos" and label == "deep" and inst in ("BTC-USDT", "ETH-USDT", "SOL-USDT", "ZEC-USDT"):
                            key = f"{mode}|{family}|{inst}|{tf}"
                            equity_store[key] = {"t": m["t"].tolist(), "equity": m["equity"].tolist()}
                            dep_store[key] = [{"t": d["t"], "pnl": d["pnl"], "eq0": d.get("eq0") or 0.0,
                                               "reason": d["reason"], "adx": d.get("adx"), "win": d["pnl"] > 0}
                                              for d in m["deployments_rows"]]
        # funding stress on the locked deep family, tune coins, OOS only, not used to choose
        for inst in TUNE:
            for tf in TFS:
                pack = books[(inst, tf)]
                m = run(pack, pack["oos0"], pack["oos1"], make_params(mode, spec, fam), with_funding=True)
                oos_rows.append({**slim(m), "inst": inst, "tf": tf, "mode": mode, "family": fam,
                                 "label": "deep_plus_funding", "split": "oos", **spec})

    # Fixed 1-unit sizing check on BTC 4h, in-sample only, original defaults. Not a candidate.
    qty_check = []
    for mode in ("Arithmetic", "Geometric"):
        p = Params(mode=mode, initial_capital=1_000_000.0, notional_pct=0.0)
        pack = books[("BTC-USDT", "4h")]
        m = run(pack, pack["is0"], pack["is1"], p)
        qty_check.append({**slim(m), "inst": "BTC-USDT", "tf": "4h", "mode": mode, "note": "script quantity 1 on 1,000,000"})

    # Regime on the in-sample tune coins for the locked deep family.
    regimes = {}
    for mode in ("Arithmetic", "Geometric"):
        rows = eval_spec(books, mode, chosen[mode]["spec"], deep[mode]["family"], "is0", "is1", TUNE)
        regimes[mode] = regime_table(rows)

    # Scaling on OOS 4h deployments for BTC ETH SOL ZEC, interleaved by time inside each sleeve.
    sleeves = {}
    combined_returns = []
    for mode in ("Arithmetic", "Geometric"):
        fam = deep[mode]["family"]
        sleeve_curves = []
        all_r = []
        for inst in ("BTC-USDT", "ETH-USDT", "SOL-USDT", "ZEC-USDT"):
            key = f"{mode}|{fam}|{inst}|4h"
            deps = dep_store.get(key, [])
            rets = []
            for d in deps:
                if d["eq0"]:
                    rets.append(d["pnl"] / d["eq0"])
            curve, dd, _ = scale_curve(rets, start=2_500.0)
            sleeves[f"{mode}|{inst}"] = {"n": len(rets), "max_dd": dd, "end": float(curve[-1]) if len(curve) else 2500.0,
                                        "curve": curve.tolist()}
            all_r.extend(rets)
            sleeve_curves.append(curve)
        # Book: sum of the four sleeve curves, padded with the last value.
        if sleeve_curves:
            length = max(len(c) for c in sleeve_curves)
            total = np.zeros(length)
            for c in sleeve_curves:
                padded = np.pad(c, (0, length - len(c)), mode="edge")
                total += padded
            peak = total[0]
            dd = 0.0
            for v in total:
                peak = max(peak, v)
                if peak > 0:
                    dd = max(dd, (peak - v) / peak)
            mc = monte_carlo(all_r)
            combined_returns.append({"mode": mode, "family": fam, "curve": total.tolist(), "max_dd": dd,
                                     "end": float(total[-1]), "monte_carlo": mc, "returns_used": len(all_r)})

    summary = {
        "disclaimer": "Hypothetical backtest, not a forecast. Past performance is not a reliable indicator of future results. Education only. Not financial advice.",
        "source_script": "indicators/tradingview/grid-bot-original.pine",
        "data": "OKX public spot candles and OKX swap funding history",
        "split": {"is": [IS_START.date().isoformat(), "2026-05-15"], "oos": ["2026-05-16", "2026-11-15"]},
        "costs": {"fee_per_side": 0.001, "slippage_per_side": 0.0005, "notional_pct": 0.05, "initial_capital": 10000},
        "variants_logged": len(variant_log),
        "setting_grid": len(specs),
        "chosen_settings": chosen,
        "deep": deep,
        "regimes_is": regimes,
        "qty_check_is": qty_check,
        "target": "75% out-of-sample deployment win rate. Reported honestly if missed.",
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, default=float))
    (OUT / "variants.json").write_text(json.dumps(variant_log, indent=2, default=float))
    (OUT / "walkforward.json").write_text(json.dumps(wf_rows, indent=2, default=float))
    (OUT / "is_results.json").write_text(json.dumps(is_rows, indent=2, default=float))
    (OUT / "oos_results.json").write_text(json.dumps(oos_rows, indent=2, default=float))
    (OUT / "equity_oos.json").write_text(json.dumps(equity_store))
    (OUT / "scaling.json").write_text(json.dumps({"sleeves": sleeves, "books": combined_returns}, default=float))
    print("variants", len(variant_log))
    print("wrote", OUT)


if __name__ == "__main__":
    main()
