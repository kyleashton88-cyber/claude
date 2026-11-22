"""Run gates D and F against the latest work data.json and (optionally) the
15–21 Nov weekly-review snapshot. Fetches Pionex dailies for 30-day win()
factors. Does not post or write an edition."""
from __future__ import annotations

import json
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from screen import (
    BIG_FOUR,
    RANGE_NOT_ACTIVE,
    evaluate_market,
    format_big_four_line,
    skip_reasons_from_facts,
)

ROOT = Path(__file__).resolve().parent
DEFAULT_DATA = ROOT / "work-2026-11-22-pm" / "data.json"
WEEK_PATH = ROOT / "week_2026_11_22.json"


def get(u):
    req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0 (compatible; EliteIntel/1.0)"})
    return json.load(urllib.request.urlopen(req, timeout=30))


def kl(s, n=180):
    k = get(f"https://api.pionex.com/api/v1/market/klines?symbol={s}_USDT&interval=1D&limit={n}")["data"]["klines"]
    d = pd.DataFrame(k).astype({"open": float, "high": float, "low": float, "close": float, "volume": float})
    d["date"] = pd.to_datetime(d.time, unit="ms")
    return d.sort_values("date").reset_index(drop=True)


def adx(d, n=14):
    d = d.reset_index(drop=True)
    h, l, c = d.high, d.low, d.close
    up = h.diff()
    dn = -l.diff()
    pdm = np.where((up > dn) & (up > 0), up, 0)
    ndm = np.where((dn > up) & (dn > 0), dn, 0)
    tr = pd.concat([h - l, (h - c.shift()).abs(), (l - c.shift()).abs()], axis=1).max(axis=1)
    atr = tr.ewm(alpha=1 / n).mean()
    pdi = 100 * pd.Series(pdm).ewm(alpha=1 / n).mean() / atr
    ndi = 100 * pd.Series(ndm).ewm(alpha=1 / n).mean() / atr
    return float((100 * (pdi - ndi).abs() / (pdi + ndi)).ewm(alpha=1 / n).mean().iloc[-1])


def win(d):
    c = d.close
    lo, hi = np.percentile(c, 5), np.percentile(c, 95)
    mid = (lo + hi) / 2
    cross = int((np.sign(c - mid).diff().fillna(0) != 0).sum())
    width = (hi - lo) / mid
    drift = abs(c.iloc[-1] - c.iloc[0]) / (hi - lo)
    a = adx(d)
    wsc = max(0, 1 - abs(width - 0.25) / 0.25)
    s = min(cross / len(c) * 4, 1) * 35 + max(0, 1 - a / 40) * 25 + max(0, 1 - drift) * 25 + wsc * 15
    return s, cross, width, drift, a


def completed(d):
    today = datetime.now(timezone.utc).date()
    return d[d.date.dt.date < today].reset_index(drop=True)


def factors(symbol):
    d = completed(kl(symbol))
    m = win(d.tail(30))
    return dict(last_date=str(d.date.iloc[-1].date()), last_close=float(d.close.iloc[-1]), drift30=m[3], adx14=m[4])


def run_current(data_path=DEFAULT_DATA):
    D = json.loads(Path(data_path).read_text())
    res = D["res"]
    print(f"# Current screen on {data_path}")
    print(f"# snapshot fetched {D.get('fetched')}")
    btc_f = factors("BTC")
    print(
        f"BTC 30-day win() through {btc_f['last_date']}: "
        f"drift30={btc_f['drift30']:.3f} ADX14={btc_f['adx14']:.1f} last_close={btc_f['last_close']}"
    )
    four_rows = []
    for coin in BIG_FOUR:
        r = res[coin]
        # Prefer the edition's lastclose/stop so the label matches what would have been published.
        four_rows.append({
            "coin": coin,
            "last_close": r["lastclose"],
            "stop": r["stop"],
            "now": r["now"],
            "bottom": r["bottom"],
        })
    rotation = []
    for coin, r in res.items():
        if coin in BIG_FOUR:
            continue
        try:
            f = factors(coin)
        except Exception as e:
            print(f"skip {coin}: {e}")
            continue
        rotation.append({
            "coin": coin,
            "drift30": f["drift30"],
            "adx14": f["adx14"],
            "last_close": r["lastclose"],
            "stop": r["stop"],
            "score": r.get("score"),
            "now": r["now"],
        })
    # Also re-evaluate four last_close vs stop using the edition snapshot.
    out = evaluate_market(btc_f["drift30"], btc_f["adx14"], four_rows, rotation)
    print("regime:", out["regime"], out["regime_reason"] or "")
    print("rotation picks:", [p["coin"] for p in out["picks"]] or "(none)")
    if out["skipped"]:
        print("skipped (up to 8):")
        for s in out["skipped"][:8]:
            print(f"  {s['coin']}: {'; '.join(s['reasons'])}")
        if len(out["skipped"]) > 8:
            print(f"  ... and {len(out['skipped'])-8} more")
    print("big four:")
    for row in out["four"]:
        pos = "below" if row["now"] < row["bottom"] else ("above" if row["now"] > row.get("top", row["bottom"]) else "inside")
        line = format_big_four_line(row["coin"], f"{row['now']:.6g}", row["status"], pos, f"{row['stop']:.6g}")
        print(f"  {row['coin']} last_close={row['last_close']:.6g} stop={row['stop']:.6g} status={row['status']}")
        print(f"    post: {line}")
    return out


def replay_week():
    week = json.loads(WEEK_PATH.read_text())
    print("\n# Replay 15–21 Nov week snapshot (week_2026_11_22.json)")
    btc = week["BTC"]
    four = [{"coin": c, "last_close": week[c]["c0"], "stop": week[c]["stop"], "now": week[c]["c0"]} for c in BIG_FOUR]
    # Rotation published 15 Nov am, plus BNB on 16 Nov pm.
    rotation = []
    for c in ("DOGE", "XLM", "SHIB", "ASTER", "BNB"):
        r = week[c]
        rotation.append({
            "coin": c, "drift30": r["drift30"], "adx14": r["adx14"],
            "last_close": r["c0"], "stop": r["stop"],
        })
    out = evaluate_market(btc["drift30"], btc["adx14"], four, rotation)
    print(f"15 Nov F regime: {out['regime']} ({btc['drift30']}/{btc['adx14']}) picks={ [p['coin'] for p in out['picks']] or '(none)' }")
    print("big four at week start (14 Nov close vs 15 Nov am stop):")
    for row in out["four"]:
        print(f"  {row['coin']} close={row['last_close']:.6g} stop={row['stop']:.6g} status={row['status']}")
    # D on BNB alone, as of its 16 Nov start, if F is ignored (already blocked by F on 15 Nov).
    bnb = week["BNB"]
    reasons = skip_reasons_from_facts(bnb["drift30"], bnb["adx14"], bnb["c0"], bnb["stop"])
    print(f"BNB 16 Nov pm D reasons (0.9% buffer, ADX 39.5): {reasons}")
    return out


if __name__ == "__main__":
    replay_week()
    print()
    run_current()

