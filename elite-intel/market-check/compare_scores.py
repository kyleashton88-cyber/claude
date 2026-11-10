"""Compare the production screen with review A (squeeze) and review C (long-window guard).

Reads the saved scores.csv files (and candle files, when present) and can fetch a
live Pionex/CoinGecko universe. Writes a markdown report. Does not change select.py.
"""
import argparse
import importlib.util
import math
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

# Halve the composite score instead of deleting the row. Comparison only.
SQUEEZE_PENALTY_MULTIPLIER = 0.5

HERE = Path(__file__).resolve().parent


def load_select():
    spec = importlib.util.spec_from_file_location("market_check_select_compare", HERE / "select.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def liq_of(vol):
    return min(math.log10(max(float(vol), 1.0)) / 10.0, 1.0)


def squeeze_reason(select, width30, width180):
    floor = width30 < select.SQUEEZE_WIDTH30_MIN
    relative = width30 < width180 / select.SQUEEZE_WIDTH180_RATIO
    if floor and relative:
        return "both cuts"
    if floor:
        return "width30<0.06"
    if relative:
        return "width30<width180/3"
    return ""


def base_score(mid, long, liq):
    return 0.5 * mid + 0.4 * long + 10 * liq


def prepare(select, frame):
    rows = []
    for old_rank, r in enumerate(frame.itertuples(index=False), start=1):
        liq = liq_of(r.vol24h_usd)
        reason = squeeze_reason(select, r.width30, r.width180)
        weight = select.long_window_weight(r.drift30, r.adx14, r.long180, r.mid30)
        guard = weight == 0.0
        published = float(r.score)
        if reason:
            new_score = None
            drop_score = None
            flag = "A drop (" + reason + ")"
        elif guard:
            new_score = round(select.composite_score(r.mid30, r.long180, liq, 0.0), 1)
            drop_score = published
            flag = "C weight 0"
        else:
            new_score = published
            drop_score = published
            flag = ""
        penalty = round(base_score(r.mid30, r.long180, liq) * SQUEEZE_PENALTY_MULTIPLIER, 1) if reason else published
        rows.append(dict(
            coin=r.coin, old_rank=old_rank, old_score=published, new_score=new_score,
            drop_score=drop_score, penalty_score=penalty, flag=flag, squeeze=bool(reason),
            guard=guard and not reason,
            width30=float(r.width30), width180=float(r.width180), drift30=float(r.drift30),
            adx14=float(r.adx14), mid30=float(r.mid30), long180=float(r.long180),
            vol24h_usd=int(r.vol24h_usd), liq=liq,
        ))
    _assign_ranks(rows, "new_score", "new_rank")
    _assign_ranks(rows, "drop_score", "drop_rank")
    _assign_ranks(rows, "penalty_score", "penalty_rank")
    return rows


def _assign_ranks(rows, score_key, rank_key):
    order = sorted((r for r in rows if r[score_key] is not None), key=lambda r: (-r[score_key], r["old_rank"]))
    for i, r in enumerate(order, start=1):
        r[rank_key] = i
    for r in rows:
        r.setdefault(rank_key, None)


def top_names(rows, rank_key, n=5):
    kept = [r for r in rows if r[rank_key] is not None]
    kept.sort(key=lambda r: r[rank_key])
    return [r["coin"] for r in kept[:n]]


def fmt_rank(rank):
    return "—" if rank is None else str(rank)


def fmt_score(score):
    return "—" if score is None else f"{score:.1f}"


def md_table(rows, columns):
    header = "| " + " | ".join(columns) + " |"
    rule = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for r in rows:
        body.append("| " + " | ".join(str(r[c]) for c in columns) + " |")
    return "\n".join([header, rule, *body])


def rank_rows(rows):
    view = []
    for r in rows:
        view.append(dict(
            coin=r["coin"],
            old_rank=r["old_rank"],
            old_score=f"{r['old_score']:.1f}",
            new_rank=fmt_rank(r["new_rank"]),
            new_score=fmt_score(r["new_score"]),
            flag=r["flag"] or "—",
            width30=f"{r['width30']:.3f}",
            width180=f"{r['width180']:.3f}",
            drift30=f"{r['drift30']:.2f}",
            adx14=f"{r['adx14']:.1f}",
            mid30=f"{r['mid30']:.1f}",
            long180=f"{r['long180']:.1f}",
        ))
    cols = ["old_rank", "coin", "old_score", "new_rank", "new_score", "flag",
            "width30", "width180", "drift30", "adx14", "mid30", "long180"]
    return md_table(view, cols)


def candle_check(select, folder, frame):
    notes = []
    by_coin = {r.coin: r for r in frame.itertuples(index=False)}
    for path in sorted(folder.glob("candles_*.csv")):
        coin = path.stem.replace("candles_", "")
        if coin not in by_coin:
            continue
        d = pd.read_csv(path)
        if "date" in d.columns:
            d["date"] = pd.to_datetime(d["date"])
            d = d.sort_values("date").reset_index(drop=True)
        m = select.win(d.tail(30))
        long = select.win(d)
        raw_squeeze = select.is_squeeze(m[2], long[2])
        raw_weight = select.long_window_weight(m[3], m[4], long[0], m[0])
        row = by_coin[coin]
        csv_squeeze = select.is_squeeze(row.width30, row.width180)
        csv_weight = select.long_window_weight(row.drift30, row.adx14, row.long180, row.mid30)
        same = raw_squeeze == csv_squeeze and (raw_weight == 0.0) == (csv_weight == 0.0)
        notes.append(dict(
            coin=coin, same="yes" if same else "NO",
            raw_w30=f"{m[2]:.4f}", csv_w30=f"{row.width30:.3f}",
            raw_w180=f"{long[2]:.4f}", csv_w180=f"{row.width180:.3f}",
            raw_A="drop" if raw_squeeze else "keep", csv_A="drop" if csv_squeeze else "keep",
            raw_C="zero" if raw_weight == 0.0 else "0.4",
            csv_C="zero" if csv_weight == 0.0 else "0.4",
        ))
    cols = ["coin", "same", "raw_w30", "csv_w30", "raw_w180", "csv_w180", "raw_A", "csv_A", "raw_C", "csv_C"]
    return md_table(notes, cols), notes


def sensitivity(select, frame):
    specs = []
    for floor in (0.05, 0.06, 0.07):
        specs.append((f"absolute only {floor:.0%}", floor, math.inf))
    for ratio in (2, 3, 4):
        specs.append((f"ratio only width180/{ratio}", 0.0, ratio))
    for floor in (0.05, 0.06, 0.07):
        for ratio in (2, 3, 4):
            specs.append((f"OR {floor:.0%} or width180/{ratio}", floor, ratio))
    out = []
    ordered = list(frame.itertuples(index=False))
    for label, floor, ratio in specs:
        dropped = []
        for r in ordered:
            if select.is_squeeze(r.width30, r.width180, floor, ratio):
                dropped.append(r.coin)
        kept = [r.coin for r in ordered if r.coin not in set(dropped)]
        watch = {c: ("drop" if c in dropped else "keep") for c in ("TRX", "XLM", "DOGE", "SHIB", "BTC", "ASTER")}
        out.append(dict(
            rule=label, n=len(dropped), top5=", ".join(kept[:5]),
            dropped=", ".join(dropped),
            TRX=watch["TRX"], XLM=watch["XLM"], DOGE=watch["DOGE"],
            SHIB=watch["SHIB"], BTC=watch["BTC"], ASTER=watch["ASTER"],
        ))
    cols = ["rule", "n", "top5", "TRX", "XLM", "DOGE", "SHIB", "BTC", "ASTER", "dropped"]
    return md_table(out, cols)


def penalty_summary(rows):
    lines = [
        f"- A-only hard drop top 5: {', '.join(top_names(rows, 'drop_rank'))}",
        f"- A-only 0.5× penalty top 5 (multiplier {SQUEEZE_PENALTY_MULTIPLIER}, C off): {', '.join(top_names(rows, 'penalty_rank'))}",
        f"- A hard-drop + C top 5: {', '.join(top_names(rows, 'new_rank'))}",
    ]
    for coin in ("TRX", "XLM", "DOGE", "SHIB", "BTC", "ETH", "SOL", "XRP", "WLD", "ASTER", "PEPE", "DOT", "KAS", "LTC", "HBAR"):
        hit = next((r for r in rows if r["coin"] == coin), None)
        if not hit:
            continue
        lines.append(
            f"- {coin}: old rank {hit['old_rank']} score {hit['old_score']:.1f}; "
            f"A-only drop rank {fmt_rank(hit['drop_rank'])}; "
            f"A-only 0.5× rank {hit['penalty_rank']} score {hit['penalty_score']:.1f}; "
            f"A+C rank {fmt_rank(hit['new_rank'])} score {fmt_score(hit['new_score'])}"
        )
    return "\n".join(lines)


def section_historical(select, title, csv_path, candle_dir):
    frame = pd.read_csv(csv_path)
    rows = prepare(select, frame)
    candles, notes = candle_check(select, Path(candle_dir), frame)
    disagree = [n["coin"] for n in notes if n["same"] != "yes"]
    text = [
        f"## {title}",
        "",
        "Baseline ranks and scores are the saved `scores.csv` (already sorted). "
        "A+C uses those published factor columns. A squeezed coin is removed. "
        "A guard hit recomputes `0.5*mid30 + 10*liq` from the published (rounded) factors "
        "and rounds to 0.1. Every other coin keeps its published score exactly.",
        "",
        f"Top 5 before: {', '.join(top_names(rows, 'old_rank'))}",
        "",
        f"Top 5 after A hard-drop + C: {', '.join(top_names(rows, 'new_rank'))}",
        "",
        rank_rows(rows),
        "",
        "### A only: hard drop vs 0.5× score penalty",
        "",
        "The penalty is not in `select.py`. It multiplies the rebuilt composite "
        f"(`0.5*mid30 + 0.4*long180 + 10*liq`) by {SQUEEZE_PENALTY_MULTIPLIER} when the "
        "provisional squeeze rule fires, and leaves every other published score unchanged. C is off.",
        "",
        penalty_summary(rows),
        "",
        "### Squeeze-rule sensitivity",
        "",
        "Counts use the rounded factor columns. `n` is how many of the 30 scored coins the rule removes. "
        "`top5` is who would lead if those coins were deleted and everyone else kept their published score.",
        "",
        sensitivity(select, frame),
        "",
        "### Candle recompute vs rounded factors",
        "",
        "Raw `win()` on the saved candle files, checked against the rounded columns. "
        + ("No A/C decision changed." if not disagree else "Decision mismatches: " + ", ".join(disagree) + "."),
        "",
        candles,
        "",
    ]
    return "\n".join(text), rows


def fetch_live(select):
    started = datetime.now(timezone.utc)
    mk = select.get("https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=80&page=1")
    by = set()
    for pg in range(1, 4):
        page = select.get(f"https://api.coingecko.com/api/v3/exchanges/bybit_spot/tickers?page={pg}")
        by |= {t["base"].upper() for t in page["tickers"] if t["target"] == "USDT"}
    symbols = select.get("https://api.pionex.com/api/v1/common/symbols")["data"]["symbols"]
    px = {s["baseCurrency"] for s in symbols if s["quoteCurrency"] == "USDT" and s.get("enable") and s["type"] == "SPOT"}
    uni = []
    for c in mk:
        s = c["symbol"].upper()
        if s in select.STABLE or "usd" in c["id"] or "wrapped" in c["id"] or "staked" in c["id"]:
            continue
        if s in by and s in px:
            uni.append((s, c["name"], c["total_volume"]))
        if len(uni) >= 30:
            break
    rows = []
    for s, name, vol in uni:
        try:
            d = select.kl(s)
        except Exception as exc:
            rows.append(dict(coin=s, error=str(exc)))
            continue
        if len(d) < 120:
            continue
        m = select.win(d.tail(30))
        long = select.win(d)
        liq = liq_of(vol)
        old = round(select.composite_score(m[0], long[0], liq, select.LONG_WINDOW_WEIGHT), 1)
        reason = squeeze_reason(select, m[2], long[2])
        weight = select.long_window_weight(m[3], m[4], long[0], m[0])
        if reason:
            new = None
            drop_score = None
            flag = "A drop (" + reason + ")"
            guard = False
        elif weight == 0.0:
            new = round(select.composite_score(m[0], long[0], liq, 0.0), 1)
            drop_score = old
            flag = "C weight 0"
            guard = True
        else:
            new = old
            drop_score = old
            flag = ""
            guard = False
        rows.append(dict(
            coin=s, name=name, old_score=old, new_score=new, drop_score=drop_score,
            flag=flag, squeeze=bool(reason), guard=guard,
            width30=m[2], width180=long[2], drift30=m[3], adx14=m[4], mid30=m[0], long180=long[0],
            vol24h_usd=int(vol), liq=liq, old_rank=0,
        ))
    scored = [r for r in rows if "old_score" in r]
    scored.sort(key=lambda r: -r["old_score"])
    for i, r in enumerate(scored, start=1):
        r["old_rank"] = i
    _assign_ranks(scored, "new_score", "new_rank")
    _assign_ranks(scored, "drop_score", "drop_rank")
    # penalty on the raw composite, A only
    for r in scored:
        raw = base_score(r["mid30"], r["long180"], r["liq"])
        r["penalty_score"] = round(raw * SQUEEZE_PENALTY_MULTIPLIER, 1) if r["squeeze"] else r["old_score"]
    _assign_ranks(scored, "penalty_score", "penalty_rank")
    fetched = datetime.now(timezone.utc)
    return scored, started, fetched


def section_live(rows, started, fetched):
    view = []
    for r in sorted(rows, key=lambda r: r["old_rank"]):
        view.append(dict(
            coin=r["coin"],
            old_rank=r["old_rank"],
            old_score=f"{r['old_score']:.1f}",
            new_rank=fmt_rank(r["new_rank"]),
            new_score=fmt_score(r["new_score"]),
            flag=r["flag"] or "—",
            width30=f"{r['width30']:.3f}",
            width180=f"{r['width180']:.3f}",
            drift30=f"{r['drift30']:.2f}",
            adx14=f"{r['adx14']:.1f}",
            mid30=f"{r['mid30']:.1f}",
            long180=f"{r['long180']:.1f}",
        ))
    cols = ["old_rank", "coin", "old_score", "new_rank", "new_score", "flag",
            "width30", "width180", "drift30", "adx14", "mid30", "long180"]
    text = [
        "## LIVE",
        "",
        f"Fetched {started.strftime('%Y-%m-%d %H:%M:%S')} UTC through {fetched.strftime('%Y-%m-%d %H:%M:%S')} UTC.",
        "Same universe rules as `select.py` (CoinGecko top, non-stable, Bybit USDT spot and Pionex USDT spot, cap 30). "
        "Daily candles are Pionex public 1D klines, limit 180. Factors below are raw `win()` values, "
        "rounded only for display; the drop and the guard use the raw values. "
        "Scores are rounded to 0.1 the way `select.py` writes `scores.csv`.",
        "",
        f"Top 5 before: {', '.join(top_names(rows, 'old_rank'))}",
        "",
        f"Top 5 after A hard-drop + C: {', '.join(top_names(rows, 'new_rank'))}",
        "",
        md_table(view, cols),
        "",
        "### A only on this live pull: hard drop vs 0.5× penalty",
        "",
        penalty_summary(rows),
        "",
    ]
    return "\n".join(text)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--bundle", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--live", action="store_true")
    args = parser.parse_args()
    select = load_select()
    bundle = args.bundle
    parts = []
    oct_md, _ = section_historical(
        select,
        "HISTORICAL — 24 Oct 2026 saved screen",
        bundle / "selection-2026-10-24" / "scores.csv",
        bundle / "selection-2026-10-24",
    )
    nov_md, _ = section_historical(
        select,
        "HISTORICAL — 1 Nov 2026 saved screen",
        bundle / "2026-11-01-am" / "screen" / "scores.csv",
        bundle / "2026-11-01-am" / "screen",
    )
    parts.append(oct_md)
    parts.append(nov_md)
    if args.live:
        try:
            rows, started, fetched = fetch_live(select)
            parts.append(section_live(rows, started, fetched))
        except Exception as exc:
            parts.append("## LIVE\n\nLive fetch failed: " + type(exc).__name__ + ": " + str(exc) + "\n")
    args.out.write_text("\n".join(parts))
    print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
