"""Download public OKX spot candles and swap funding.

Source: https://www.okx.com/api/v5/market/history-candles
        https://www.okx.com/api/v5/public/instruments
        https://www.okx.com/api/v5/public/funding-rate-history

Bybit's public API returned a CloudFront country block from this environment,
so OKX is the public source. The last incomplete candle (confirm=0) is dropped.
"""
import json
import time
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import requests

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
DATA.mkdir(parents=True, exist_ok=True)

SYMBOLS = ["BTC-USDT", "ETH-USDT", "SOL-USDT", "ZEC-USDT", "XRP-USDT", "LINK-USDT"]
BARS = {"1h": "1H", "4h": "4H"}
START = datetime(2021, 1, 1, tzinfo=timezone.utc)
END = datetime(2026, 11, 16, tzinfo=timezone.utc)
BASE = "https://www.okx.com"


def get(path, params):
    for attempt in range(6):
        r = requests.get(BASE + path, params=params, timeout=40)
        if r.status_code == 429:
            time.sleep(1.5 + attempt)
            continue
        r.raise_for_status()
        body = r.json()
        if body.get("code") not in ("0", 0, None):
            raise RuntimeError(f"{path} {body.get('code')} {body.get('msg')}")
        return body["data"]
    raise RuntimeError(f"rate limited: {path}")


def fetch_candles(inst, bar):
    start_ms = int(START.timestamp() * 1000)
    end_ms = int(END.timestamp() * 1000)
    rows = []
    after = None
    while True:
        params = {"instId": inst, "bar": bar, "limit": "100"}
        if after is not None:
            params["after"] = str(after)
        page = get("/api/v5/market/history-candles", params)
        if not page:
            break
        rows.extend(page)
        oldest = int(page[-1][0])
        if oldest <= start_ms or len(page) < 100:
            break
        after = oldest
        time.sleep(0.08)
    # newest-first from the API
    df = pd.DataFrame(rows, columns=["t", "o", "h", "l", "c", "vol", "vol_ccy", "vol_quote", "confirm"])
    df = df.astype({"t": "int64", "o": float, "h": float, "l": float, "c": float, "vol": float, "confirm": "int64"})
    df = df[(df.t >= start_ms) & (df.t <= end_ms) & (df.confirm == 1)]
    df = df.drop_duplicates("t").sort_values("t")
    return df[["t", "o", "h", "l", "c", "vol"]]


def fetch_tick(inst):
    rows = get("/api/v5/public/instruments", {"instType": "SPOT", "instId": inst})
    row = rows[0]
    return {"inst": inst, "tick": float(row["tickSz"]), "lot": float(row["lotSz"]), "min_sz": float(row["minSz"])}


def fetch_funding(inst):
    swap = inst.replace("-USDT", "-USDT-SWAP")
    start_ms = int(START.timestamp() * 1000)
    rows = []
    after = None
    while True:
        params = {"instId": swap, "limit": "100"}
        if after is not None:
            params["after"] = str(after)
        page = get("/api/v5/public/funding-rate-history", params)
        if not page:
            break
        rows.extend(page)
        oldest = int(page[-1]["fundingTime"])
        if oldest <= start_ms or len(page) < 100:
            break
        after = oldest
        time.sleep(0.08)
    if not rows:
        return pd.DataFrame(columns=["t", "rate"])
    df = pd.DataFrame(rows)
    df["t"] = df["fundingTime"].astype("int64")
    df["rate"] = df["realizedRate"].astype(float)
    df = df[df.t >= start_ms].drop_duplicates("t").sort_values("t")
    return df[["t", "rate"]]


def main():
    manifest = {"source": "OKX public REST", "fetched_utc": datetime.now(timezone.utc).isoformat(), "symbols": {}}
    for inst in SYMBOLS:
        meta = fetch_tick(inst)
        manifest["symbols"][inst] = meta
        for name, bar in BARS.items():
            df = fetch_candles(inst, bar)
            path = DATA / f"{inst.replace('-', '')}_{name}.csv"
            df.to_csv(path, index=False)
            t0 = datetime.fromtimestamp(int(df.t.iloc[0]) / 1000, timezone.utc)
            t1 = datetime.fromtimestamp(int(df.t.iloc[-1]) / 1000, timezone.utc)
            meta[name] = {"rows": int(len(df)), "start": t0.isoformat(), "end": t1.isoformat(), "file": path.name}
            print(inst, name, len(df), t0, t1, flush=True)
        fund = fetch_funding(inst)
        fpath = DATA / f"{inst.replace('-', '')}_funding.csv"
        fund.to_csv(fpath, index=False)
        meta["funding_rows"] = int(len(fund))
        print(inst, "funding", len(fund), flush=True)
    (DATA / "manifest.json").write_text(json.dumps(manifest, indent=2))
    print("manifest", DATA / "manifest.json")


if __name__ == "__main__":
    main()
