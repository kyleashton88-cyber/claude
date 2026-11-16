"""Round 3. Walk-forward inside the in-sample window, then one out-of-sample pass.

Selection folds, both before 16 May 2026:
- 16 May 2023 to 15 May 2024
- 16 May 2024 to 15 May 2025

16 May 2025 to 15 May 2026 is a nested check. It is stored and not used to pick.
16 May 2026 to 15 Nov 2026 is the untouched out-of-sample window.

A deployment wins when its pnl is positive after taker fees and recorded funding.
The objective on the selection folds is that win rate, pooled across BTC, ETH,
SOL, XRP and LINK, on 1h and 4h. A candidate needs at least 40 deployments and
a mean return above -0.5% of margin. Within two percentage points of win rate,
the higher mean return is kept. ZEC is not in the selection folds: OKX spot
history for ZEC starts 24 Nov 2025, inside the nested check.

Leverage adjustments are chosen on the same selection folds at 3x, before the
out-of-sample window is opened. 1x, 2x, 3x and 5x are then all reported.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
import requests

from engine import align_funding
from round3 import (
    MMR, build_ranges, hysteresis, liq_price, map_daily_hyst, simulate,
    stable_mask, variance_ratio, wilson,
)
from screener import lag_one, raw_metrics

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
OUT = ROOT / "results"
OUT.mkdir(exist_ok=True)

SELECT = ["BTC-USDT", "ETH-USDT", "SOL-USDT", "XRP-USDT", "LINK-USDT"]
REPORT = ["BTC-USDT", "ETH-USDT", "SOL-USDT", "ZEC-USDT"]
TFS = ["1h", "4h"]
BAR_SEC = {"1h": 3600, "4h": 14400}
BAR_MS = {"1h": 3_600_000, "4h": 14_400_000}
SEL_FOLDS = [("2023-05-16", "2024-05-16"), ("2024-05-16", "2025-05-16")]
NEST = ("2025-05-16", "2026-05-16")
OOS = ("2026-05-16", "2026-11-16")


def ms(day):
    return int(datetime.strptime(day, "%Y-%m-%d").replace(tzinfo=timezone.utc).timestamp() * 1000)


def load_px(inst, tf):
    df = pd.read_csv(DATA / f"{inst.replace('-', '')}_{tf}.csv")
    return {k: df[k].to_numpy(float if k != "t" else np.int64) for k in ("t", "o", "h", "l", "c", "vol")}


def load_funding(inst, t):
    path = DATA / f"{inst.replace('-', '')}_funding.csv"
    if not path.exists():
        return np.zeros(len(t)), None, None
    fund = pd.read_csv(path)
    if len(fund) == 0:
        return np.zeros(len(t)), None, None
    ft = fund.t.to_numpy(np.int64)
    fr = fund.rate.to_numpy(float)
    return align_funding(t, ft, fr), int(ft.min()), int(ft.max())


def fetch_stable():
    path = DATA / "stablecoin_usd.csv"
    if path.exists() and path.stat().st_size > 1000:
        df = pd.read_csv(path)
        return df.t.to_numpy(np.int64), df.chg14.to_numpy(float)
    print("fetch stablecoin supply", flush=True)
    rows = requests.get("https://stablecoins.llama.fi/stablecoincharts/all", timeout=60).json()
    days, usd = [], []
    for row in rows:
        days.append(int(row["date"]))
        usd.append(float(row["totalCirculatingUSD"]["peggedUSD"]))
    days = np.array(days, dtype=np.int64)
    usd = np.array(usd)
    chg = np.full(len(usd), np.nan)
    chg[14:] = usd[14:] / usd[:-14] - 1.0
    pd.DataFrame({"t": days, "usd": usd, "chg14": chg}).to_csv(path, index=False)
    return days, chg


def weekday(t, bar_ms):
    idx = pd.to_datetime(t + bar_ms, unit="ms", utc=True).tz_convert("Australia/Sydney")
    return np.asarray(idx.day_of_week < 5)


def build_book(inst, tf, stable_t, stable_chg, manifest_tick):
    px = load_px(inst, tf)
    t, o, h, l, c, v = px["t"], px["o"], px["h"], px["l"], px["c"], px["vol"]
    ranges = build_ranges(h, l, c)
    from round3 import smooth_pair
    ranges["atr2s"] = smooth_pair(*ranges["atr2"])
    _p, _m, adx = __import__("engine", fromlist=["dmi"]).dmi(h, l, c, 14, 14)
    adx_s = __import__("engine", fromlist=["ema"]).ema(np.nan_to_num(adx, nan=0.0), 3)
    hyst = hysteresis(np.nan_to_num(adx_s, nan=99.0))
    hyst[:40] = False
    vr = variance_ratio(c)
    daily = map_daily_hyst(t, h, l, c)
    age_lo, age_hi = ranges["atr2"]
    from round3 import range_age
    age = range_age(c, age_lo, age_hi)
    score, mode = raw_metrics(h, l, c, v, BAR_SEC[tf])
    score_l, mode_l = lag_one(score), lag_one(mode)
    wk = weekday(t, BAR_MS[tf])
    stable = stable_mask(t, stable_t, stable_chg)
    quote = c * v
    bars24 = max(1, int(round(86400 / BAR_SEC[tf])))
    qv = pd.Series(quote).rolling(bars24, min_periods=max(1, bars24 // 2)).sum().to_numpy() / 24.0
    liquid = np.nan_to_num(qv, nan=0.0) >= 2_000_000.0
    gates = {
        "hyst": hyst & wk,
        "hyst_vr": hyst & wk & (vr < 0.90),
        "hyst_daily": hyst & wk & daily,
        "hyst_age": hyst & wk & (age >= 6) & (age <= 48),
        "hyst_stable": hyst & wk & stable,
        "score60": wk & (score_l >= 60) & (mode_l == 0),
        "score55": wk & (score_l >= 55),
        "hyst_liq": hyst & wk & liquid,
    }
    fund, f0, f1 = load_funding(inst, t)
    return {
        "inst": inst, "tf": tf, "t": t, "o": o, "h": h, "l": l, "c": c,
        "ranges": ranges, "gates": gates, "funding": fund,
        "fund_from": f0, "fund_to": f1, "tick": manifest_tick, "vr": vr, "hyst": hyst,
    }


def window(t, start, end):
    a = int(np.searchsorted(t, ms(start), side="left"))
    b = int(np.searchsorted(t, ms(end), side="left"))
    return max(0, a - 120), a, b


def spec_base(mode, gate, range_name, exit_name, **kw):
    exits = {
        "close": dict(exit="close_all", stop_pct=2.0, outside=3, max_bars=0),
        "time18": dict(exit="close_all", stop_pct=2.0, outside=3, max_bars=18),
        "time36": dict(exit="close_all", stop_pct=4.0, outside=6, max_bars=36),
        "tight": dict(exit="close_all", stop_pct=1.0, outside=3, max_bars=18),
        "partial": dict(exit="partial", stop_pct=2.0, outside=3, max_bars=24),
        "regime": dict(exit="regime", stop_pct=2.0, outside=3, max_bars=0),
    }
    body = dict(
        levels=8, mode=mode, tp_pct=2.0, leverage=1.0, margin=10_000.0,
        fee=0.001, slip=0.0005, min_step=0.005, buffer=False, bar_ms=None,
    )
    body.update(exits[exit_name])
    body.update(kw)
    body["_gate"] = gate
    body["_range"] = range_name
    body["_exit"] = exit_name
    return body


def run_book(book, spec, start, end, leverage=None):
    spec = dict(spec)
    if leverage is not None:
        spec["leverage"] = leverage
    t = book["t"]
    warm, a, b = window(t, start, end)
    if b - a < 30:
        return []
    sl = slice(warm, b)
    lo, hi = book["ranges"][spec["_range"]]
    allow = book["gates"][spec["_gate"]]
    regime = book["hyst"]
    spec["bar_ms"] = BAR_MS[book["tf"]]
    res = simulate(
        book["o"][sl], book["h"][sl], book["l"][sl], book["c"][sl], book["t"][sl],
        lo[sl], hi[sl], allow[sl], regime[sl], spec, book["tick"],
        funding=book["funding"][sl], mmr=MMR.get(book["inst"], 0.01),
        count_from=a - warm, count_to=b - warm,
    )
    for d in res["deployments"]:
        d["inst"] = book["inst"]
        d["tf"] = book["tf"]
        d["max_dd_path"] = res["max_dd"]
    return res["deployments"]


def pool_stats(deps):
    n = len(deps)
    if n == 0:
        return None
    wins = sum(1 for d in deps if d["pnl"] > 0)
    stops = [d for d in deps if d["reason"] == "stop"]
    liqs = [d for d in deps if d["reason"] == "liq"]
    return {
        "n": n, "wins": wins, "win": wins / n,
        "ret": float(np.mean([d["ret"] for d in deps])),
        "stops": len(stops),
        "stop_ret": float(np.mean([d["ret"] for d in stops])) if stops else None,
        "liqs": len(liqs),
        "dd": float(np.mean([d.get("max_dd_path") or 0 for d in deps])),
    }


def covers(deps):
    """BTC, ETH and SOL must actually trade on both timeframes in the selection folds."""
    counts = {}
    for d in deps:
        counts[(d["inst"], d["tf"])] = counts.get((d["inst"], d["tf"]), 0) + 1
    for inst in ("BTC-USDT", "ETH-USDT", "SOL-USDT"):
        for tf in ("1h", "4h"):
            if counts.get((inst, tf), 0) < 8:
                return False
    return True


def better(a, b):
    """a, b are pool stats or None. Eligible only if n>=40 and ret>-0.005."""
    def ok(s):
        return s is not None and s["n"] >= 40 and s["ret"] > -0.005
    if not ok(a):
        return False
    if not ok(b):
        return True
    if abs(a["win"] - b["win"]) > 0.02:
        return a["win"] > b["win"]
    if abs(a["ret"] - b["ret"]) > 1e-6:
        return a["ret"] > b["ret"]
    return a["liqs"] < b["liqs"]


def collect(books, spec, folds, coins, tfs, leverage=None):
    deps = []
    for inst in coins:
        for tf in tfs:
            book = books.get((inst, tf))
            if book is None:
                continue
            for start, end in folds:
                deps.extend(run_book(book, spec, start, end, leverage))
    return deps


def main():
    manifest = json.loads((DATA / "manifest.json").read_text())
    stable_t, stable_chg = fetch_stable()
    books = {}
    print("features", flush=True)
    for inst in SELECT + ["ZEC-USDT"]:
        tick = manifest["symbols"][inst]["tick"]
        for tf in TFS:
            print(" ", inst, tf, flush=True)
            books[(inst, tf)] = build_book(inst, tf, stable_t, stable_chg, tick)
            print("   bars", len(books[(inst, tf)]["t"]), "hyst", int(books[(inst, tf)]["hyst"].sum()), flush=True)

    ranges = ["atr2", "atr3", "atr_hold", "bb", "pct", "atr2s"]
    gates = ["hyst", "hyst_vr", "hyst_daily", "hyst_age", "hyst_stable", "score60", "score55", "hyst_liq"]
    exits = ["close", "time18", "time36", "tight", "partial", "regime"]
    log = []
    chosen = {}
    for mode in ("Arithmetic", "Geometric"):
        best = None
        best_spec = None
        fallback = None
        fallback_spec = None
        nvar = 0
        for rng in ranges:
            for gate in gates:
                for exit_name in exits:
                    nvar += 1
                    spec = spec_base(mode, gate, rng, exit_name)
                    deps = collect(books, spec, SEL_FOLDS, SELECT, TFS)
                    st = pool_stats(deps)
                    if st is not None and not covers(deps):
                        st = None
                    log.append({"stage": "wf_select", "mode": mode, "range": rng, "gate": gate, "exit": exit_name,
                                "levels": 8, **({} if st is None else {k: st[k] for k in ("n", "win", "ret", "stops", "liqs")})})
                    if st is not None and (fallback is None or st["win"] > fallback["win"]):
                        fallback, fallback_spec = st, spec
                    if better(st, best):
                        best, best_spec = st, spec
                    if nvar % 20 == 0:
                        print(mode, nvar, None if best is None else round(best["win"], 3), flush=True)
        if best_spec is None:
            best, best_spec = fallback, fallback_spec
            print(mode, "no candidate cleared the return floor; using the highest selection-fold win rate", flush=True)
        # refine levels and minimum step on the winner's range/gate/exit
        refine_best, refine_spec = best, best_spec
        for levels in (6, 8, 10, 12):
            for step in (0.005, 0.01, 0.02):
                spec = dict(best_spec)
                spec["levels"] = levels
                spec["min_step"] = step
                deps = collect(books, spec, SEL_FOLDS, SELECT, TFS)
                st = pool_stats(deps)
                if st is not None and not covers(deps):
                    st = None
                nvar += 1
                log.append({"stage": "wf_refine", "mode": mode, "levels": levels, "min_step": step,
                            "range": spec["_range"], "gate": spec["_gate"], "exit": spec["_exit"],
                            **({} if st is None else {k: st[k] for k in ("n", "win", "ret", "stops", "liqs")})})
                if better(st, refine_best):
                    refine_best, refine_spec = st, spec
        chosen[mode] = {"spec": {k: v for k, v in refine_spec.items() if not k.startswith("_") or True},
                        "wf": refine_best, "nvar_running": nvar}
        chosen[mode]["spec"] = refine_spec
        print("locked", mode, refine_spec["_range"], refine_spec["_gate"], refine_spec["_exit"],
              refine_spec["levels"], None if refine_best is None else round(refine_best["win"], 3), flush=True)

    # Coin offsets on selection folds. ZEC is excluded here.
    coin_spec = {mode: {} for mode in chosen}
    for mode, pack in chosen.items():
        base = pack["spec"]
        for inst in ("BTC-USDT", "ETH-USDT", "SOL-USDT"):
            best = pool_stats(collect(books, base, SEL_FOLDS, [inst], TFS))
            keep = base
            for levels in (6, 10):
                for stop in (1.0, 4.0):
                    spec = dict(base)
                    spec["levels"] = levels
                    spec["stop_pct"] = stop
                    st = pool_stats(collect(books, spec, SEL_FOLDS, [inst], TFS))
                    log.append({"stage": "wf_coin", "mode": mode, "inst": inst, "levels": levels, "stop_pct": stop,
                                **({} if st is None else {k: st[k] for k in ("n", "win", "ret")})})
                    if st and best and st["n"] >= 20 and st["win"] >= best["win"] + 0.03 and st["ret"] >= best["ret"] - 0.003:
                        if better(st, best) or st["win"] >= best["win"] + 0.03:
                            best, keep = st, spec
            coin_spec[mode][inst] = keep
            print("coin", mode, inst, keep.get("levels"), keep.get("stop_pct"),
                  None if best is None else round(best["win"], 3), flush=True)

    # Leverage adjustment at 3x on the selection folds, still before OOS.
    lev_choice = {}
    for mode, pack in chosen.items():
        base = pack["spec"]
        options = [("base", dict(base))]
        tight = dict(base)
        tight["stop_pct"] = 1.0
        options.append(("tighter_stop", tight))
        fewer = dict(base)
        fewer["levels"] = max(4, base["levels"] - 2)
        options.append(("fewer_levels", fewer))
        buf = dict(base)
        buf["buffer"] = True
        options.append(("liq_buffer", buf))
        best_name, best_spec, best_st = "base", base, None
        for name, spec in options:
            deps = collect(books, spec, SEL_FOLDS, SELECT, TFS, leverage=3.0)
            st = pool_stats(deps)
            log.append({"stage": "wf_leverage_3x", "mode": mode, "adjust": name,
                        **({} if st is None else {k: st[k] for k in ("n", "win", "ret", "stops", "liqs")})})
            # Prefer zero liquidations, then the usual objective.
            if st is None:
                continue
            if best_st is None or (st["liqs"] < best_st["liqs"] and st["win"] + 0.03 >= best_st["win"]) or better(st, best_st):
                if best_st is None or st["liqs"] < best_st["liqs"] or better(st, best_st):
                    best_name, best_spec, best_st = name, spec, st
        lev_choice[mode] = {"adjust": best_name, "spec": best_spec, "wf3x": best_st}
        print("lev", mode, best_name, None if best_st is None else (round(best_st["win"], 3), best_st["liqs"]), flush=True)

    # Nested fold, not used to change the lock. Recorded so the log shows it.
    for mode, pack in lev_choice.items():
        deps = collect(books, pack["spec"], [NEST], SELECT, TFS, leverage=1.0)
        st = pool_stats(deps)
        log.append({"stage": "nested_not_used", "mode": mode, **({} if st is None else st)})

    print("OOS", flush=True)
    cells = []
    oos_deps = {mode: [] for mode in lev_choice}
    for mode, pack in lev_choice.items():
        for inst in REPORT:
            spec = coin_spec[mode].get(inst, pack["spec"])
            # leverage adjustment applies on top of the coin spec's stop/levels if that was the base;
            # coin offsets keep their own stop and levels. Buffer flag comes from the leverage choice.
            spec = dict(spec)
            spec["buffer"] = pack["spec"].get("buffer", False)
            if pack["adjust"] == "tighter_stop" and inst not in coin_spec[mode]:
                spec["stop_pct"] = 1.0
            for tf in TFS:
                book = books[(inst, tf)]
                for lev in (1, 2, 3, 5):
                    deps = run_book(book, spec, OOS[0], OOS[1], leverage=lev)
                    st = pool_stats(deps) or {"n": 0, "wins": 0, "win": None, "ret": None, "stops": 0, "stop_ret": None, "liqs": 0, "dd": None}
                    lo, hi = wilson(st["wins"], st["n"])
                    # safe-leverage geometry on the median launch is reported from stop distance vs a representative entry
                    cells.append({
                        "mode": mode, "coin": inst, "tf": tf, "leverage": lev,
                        "win": st["win"], "n": st["n"], "wins": st["wins"],
                        "ci_lo": lo, "ci_hi": hi, "mean_ret": st["ret"], "max_dd": st["dd"],
                        "stops": st["stops"], "stop_mean_ret": st["stop_ret"], "liquidations": st["liqs"],
                        "fees_included": True,
                        "meaningful": st["n"] >= 20,
                    })
                    if lev == 1:
                        oos_deps[mode].extend(deps)
                    print(mode[:5], inst.split("-")[0], tf, f"{lev}x", st["n"], None if st["win"] is None else round(st["win"], 3), flush=True)

    # Safe leverage rule, applied to the OOS report, not used to change settings:
    # zero liquidations, and max drawdown on margin at or under 35%.
    # The 2x-stop-gap buffer is the launch filter when it was selected in-sample.
    safe = {}
    for mode in lev_choice:
        for inst in REPORT:
            safe_lev = None
            for lev in (1, 2, 3, 5):
                rows = [c for c in cells if c["mode"] == mode and c["coin"] == inst and c["leverage"] == lev]
                if not rows:
                    break
                if any((c["liquidations"] or 0) > 0 for c in rows):
                    break
                if any(c["max_dd"] is not None and c["max_dd"] > 0.35 for c in rows):
                    break
                safe_lev = lev
            safe[f"{mode}|{inst}"] = safe_lev

    # Scaling on 1x deployment returns of the locked rules, both modes pooled in time.
    rets = []
    for mode, deps in oos_deps.items():
        rets.extend((d["t"], d["ret"]) for d in deps)
    rets.sort()
    r = np.array([x[1] for x in rets], dtype=float)

    def scale_curve(sample):
        equity = 10_000.0
        peak = equity
        frac = 0.15
        wins = 0
        ruined = False
        curve = [equity]
        for ret in sample:
            if (not ruined) and wins >= 3 and peak > 0 and (peak - equity) / peak < 0.08 and frac < 0.30:
                frac = min(0.30, frac + 0.05)
                wins = 0
            margin_post = equity * frac
            equity = equity + margin_post * float(ret)
            if equity <= 2_000:
                ruined = True
                equity = max(equity, 0.0)
            peak = max(peak, equity)
            if peak > 0 and (peak - equity) / peak > 0.25:
                frac = max(0.05, frac / 2)
            wins = wins + 1 if ret > 0 else 0
            curve.append(equity)
        return np.array(curve), ruined

    terminals, ruins, dds = [], 0, []
    rng = np.random.default_rng(16)
    if len(r):
        base_curve, _ = scale_curve(r)
        for _i in range(2000):
            sample = rng.choice(r, size=len(r), replace=True)
            curve, ruined = scale_curve(sample)
            terminals.append(curve[-1])
            ruins += int(ruined)
            peak = np.maximum.accumulate(curve)
            dds.append(float(np.max((peak - curve) / np.maximum(peak, 1e-9))))
        terminals = np.sort(np.array(terminals))
        dds = np.sort(np.array(dds))
        scale = {
            "n": int(len(r)),
            "end": float(base_curve[-1]),
            "p05": float(terminals[int(0.05 * (len(terminals) - 1))]),
            "p50": float(np.median(terminals)),
            "ruin": ruins / 2000,
            "dd50": float(np.median(dds)),
            "dd95": float(dds[int(0.95 * (len(dds) - 1))]),
            "curve": base_curve.tolist(),
        }
    else:
        scale = {"n": 0, "end": 10000, "p05": 10000, "p50": 10000, "ruin": None, "dd50": None, "dd95": None, "curve": []}

    def public_spec(spec):
        return {k: (bool(v) if isinstance(v, (bool, np.bool_)) else v) for k, v in spec.items() if k != "bar_ms"}

    summary = {
        "selection": "walk-forward folds 2023-05-16..2024-05-16 and 2024-05-16..2025-05-16; nested 2025-05-16..2026-05-16 not used; OOS 2026-05-16..2026-11-15 not used",
        "variants": len(log),
        "chosen": {m: {"wf": chosen[m]["wf"], "spec": public_spec(chosen[m]["spec"])} for m in chosen},
        "coin_offsets": {m: {k: public_spec(v) for k, v in coin_spec[m].items()} for m in coin_spec},
        "leverage_adjustment": {m: {"adjust": lev_choice[m]["adjust"], "wf3x": lev_choice[m]["wf3x"]} for m in lev_choice},
        "safe_leverage": safe,
        "scale": {k: scale[k] for k in scale if k != "curve"},
        "funding_note": "OKX public funding history used where the file has prints, from about 10 Aug 2026. Earlier bars, including most of the in-sample window and the first part of the out-of-sample window, are charged zero. Binance futures funding was blocked from this environment.",
        "stablecoin": "DefiLlama stablecoins.llama.fi total circulating USD, 14-day change, lagged one day. History covers the in-sample window.",
        "margin": "Isolated. Maintenance rates: BTC 0.4%, ETH 0.5%, SOL 1%, ZEC 1% of notional. Teaching schedule, not a live table.",
    }
    (OUT / "round3_summary.json").write_text(json.dumps(summary, indent=2, default=float))
    (OUT / "round3_variants.json").write_text(json.dumps(log, default=float))
    (OUT / "round3_oos.json").write_text(json.dumps(cells, indent=2, default=float))
    (OUT / "round3_scale.json").write_text(json.dumps(scale))
    gate = {
        "fees_included": True,
        "window": ["2026-05-16", "2026-11-15"],
        "win_definition": "per_deployment_net_of_fees",
        "cells": [{k: c[k] for k in ("mode", "coin", "tf", "leverage", "win", "n", "fees_included")} for c in cells],
    }
    (OUT / "oos_gate.json").write_text(json.dumps(gate, indent=2))
    write_markdown(summary, cells, log, scale)
    write_charts(cells, scale)
    print("variants", len(log))
    print("gate file written; not opening it for selection and not building a PDF")


def write_markdown(summary, cells, log, scale):
    lines = [
        "# Round 3 holdout",
        "",
        "Education only. Not financial advice. Past performance is not a reliable indicator of future results.",
        "",
        "Leverage can liquidate a position before a stop fills. Isolated margin does not limit losses to the posted margin if a gap goes through the liquidation price in the same move; in this model a gap through liquidation wipes the posted margin.",
        "",
        f"Variants logged: {len(log)}. Selection did not use 16 May 2026 onward.",
        "",
        "## Locked from the walk-forward",
        "",
    ]
    for mode, pack in summary["chosen"].items():
        sp = pack["spec"]
        wf = pack["wf"] or {}
        lines.append(
            f"- {mode}: range `{sp.get('_range')}`, gate `{sp.get('_gate')}`, exit `{sp.get('_exit')}`, "
            f"levels {sp.get('levels')}, stop {sp.get('stop_pct')}%, min step {sp.get('min_step')}. "
            f"Selection-fold win rate {None if wf.get('win') is None else round(100*wf['win'], 1)}% "
            f"on n={wf.get('n')}, mean return {None if wf.get('ret') is None else round(100*wf['ret'], 2)}%."
        )
    lines += ["", "## Out of sample", "",
              "Win rate is per deployment, after fees and recorded funding. The interval is a 95% Wilson interval. n below 20 is not a result.",
              ""]
    lines.append("| Mode | Coin | TF | Lev | Win rate | 95% CI | n | Mean return | Max DD | Stops | Liq |")
    lines.append("|---|---|---|---|---|---|---|---|---|---|---|")
    for c in cells:
        ci = "—" if c["ci_lo"] is None else f"{100*c['ci_lo']:.1f}–{100*c['ci_hi']:.1f}%"
        win = "—" if c["win"] is None else f"{100*c['win']:.1f}%"
        flag = "" if c["meaningful"] else " not meaningful"
        ret = "—" if c["mean_ret"] is None else f"{100*c['mean_ret']:.2f}%"
        dd = "—" if c["max_dd"] is None else f"{100*c['max_dd']:.1f}%"
        lines.append(f"| {c['mode']} | {c['coin'].split('-')[0]} | {c['tf']} | {c['leverage']}x | {win}{flag} | {ci} | {c['n']} | {ret} | {dd} | {c['stops']} | {c['liquidations']} |")
    lines += ["", "## Max safe leverage", "",
              "Rule, applied after the fact to this holdout and not used to pick settings: zero liquidations on both timeframes, and max drawdown on margin at or under 35%. The highest leverage that still passes is the safe leverage. None means even 1x failed the rule.",
              ""]
    for k, v in summary["safe_leverage"].items():
        lines.append(f"- {k}: {v if v else 'none'}")
    lines += ["", "## Scaling", "",
              "Hypothetical. A 10,000 account posts 15% of equity as isolated margin per deployment at the locked leverage rule's returns from the 1x holdout path. This is not a forecast.",
              "",
              f"Terminal on the recorded path: {scale['end']:.0f}. Bootstrap median {scale['p50']:.0f}, 5th percentile {scale['p05']:.0f}, ruin rate {None if scale['ruin'] is None else round(100*scale['ruin'], 1)}% of 2,000 redraws. Ruin means equity at or under 2,000.",
              ""]
    lines.append(summary["funding_note"])
    lines.append(summary["stablecoin"])
    (ROOT / "ROUND3.md").write_text("\n".join(lines) + "\n")


def write_charts(cells, scale):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(10, 4.5))
    fig.patch.set_facecolor("#0A1628")
    ax.set_facecolor("#0E1C2F")
    coins = ["BTC-USDT", "ETH-USDT", "SOL-USDT", "ZEC-USDT"]
    x = np.arange(len(coins))
    for offset, mode, color in ((-0.15, "Arithmetic", "#00D4FF"), (0.15, "Geometric", "#7AA2FF")):
        vals = []
        for coin in coins:
            row = next((c for c in cells if c["mode"] == mode and c["coin"] == coin and c["tf"] == "4h" and c["leverage"] == 1), None)
            vals.append(0 if row is None or not row["meaningful"] or row["win"] is None else 100 * row["win"])
        ax.bar(x + offset, vals, width=0.3, color=color, label=mode)
    ax.axhline(75, color="#F5C16C", ls="--", lw=1, label="75% gate")
    ax.set_xticks(x)
    ax.set_xticklabels([c.split("-")[0] for c in coins], color="white")
    ax.tick_params(colors="white")
    ax.set_ylim(0, 100)
    ax.set_title("Out-of-sample 4h deployment win rate at 1x. Empty bar means n<20.", color="white", loc="left")
    ax.legend(facecolor="#0A1628", labelcolor="white")
    fig.text(0.01, 0.01, "Past performance is not a reliable indicator of future results.", color="#9FB3C8", fontsize=8)
    fig.tight_layout(rect=(0, 0.05, 1, 1))
    fig.savefig(ROOT / "charts" / "round3_win_4h.png", dpi=140)
    plt.close()
    if scale.get("curve"):
        fig, ax = plt.subplots(figsize=(10, 4))
        fig.patch.set_facecolor("#0A1628")
        ax.set_facecolor("#0E1C2F")
        ax.plot(scale["curve"], color="#00D4FF")
        ax.axhline(10000, color="#9FB3C8", lw=0.6)
        ax.tick_params(colors="white")
        ax.set_title("Hypothetical margin account on the 1x out-of-sample path", color="white", loc="left")
        fig.text(0.01, 0.01, "Past performance is not a reliable indicator of future results. Not a forecast.", color="#9FB3C8", fontsize=8)
        fig.tight_layout(rect=(0, 0.05, 1, 1))
        fig.savefig(ROOT / "charts" / "round3_scale.png", dpi=140)
        plt.close()


if __name__ == "__main__":
    main()
