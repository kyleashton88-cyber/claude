"""Grid-suitability screen. Universe: CoinGecko top coins by mkt cap, non-stable, listed on Bybit spot (CoinGecko tickers) and Pionex (Pionex API).
Daily candles: Pionex public klines (USDT pairs). Output: scores.csv, levels.json"""
import json, urllib.request, datetime as dt, numpy as np, pandas as pd
from pathlib import Path
from zoneinfo import ZoneInfo
def get(u): return json.load(urllib.request.urlopen(urllib.request.Request(u,headers={"User-Agent":"Mozilla/5.0"}),timeout=30))
STABLE={"USDT","USDC","DAI","USDE","FDUSD","TUSD","USDS","PYUSD","USD1","USDD","BUSD","RLUSD","USDTB","USDF","USDG","FRAX","GHO","EURC","USD0","BFUSD","SUSDS","SUSDE","XAUT","PAXG","USYC","BUIDL","USDX"}

# Review A, approved by Stewart 15 Nov 2026. Widths are the fractions win()
# already returns ((p95-p5)/mid), so 0.06 is 6%. Both cuts are strict.
SQUEEZE_WIDTH30_MIN = 0.06
SQUEEZE_WIDTH180_RATIO = 3

def is_squeeze(width30, width180, width30_min=None, width180_ratio=None):
    """True when the 30-day range is under the floor or under 1/ratio of the 180-day range."""
    if width30_min is None: width30_min = SQUEEZE_WIDTH30_MIN
    if width180_ratio is None: width180_ratio = SQUEEZE_WIDTH180_RATIO
    return bool(width30 < width30_min or width30 < width180 / width180_ratio)

# Review C. mid30 and long180 are the win() scores (the mid30 / long180 columns),
# not prices. Strict on all three. A hit zeros the 0.4 long-window weight and
# leaves the 0.5 mid weight and the liquidity term as they are — no renormalizing.
DRIFT30_GUARD_MIN = 0.8
ADX14_GUARD_MIN = 40
LONG_MID_GAP_MIN = 15
LONG_WINDOW_WEIGHT = 0.4

def long_window_weight(drift30, adx14, long180, mid30):
    if drift30 > DRIFT30_GUARD_MIN and adx14 > ADX14_GUARD_MIN and long180 > mid30 + LONG_MID_GAP_MIN:
        return 0.0
    return LONG_WINDOW_WEIGHT

def composite_score(mid, long, liq, long_weight=None):
    """Window blend: half the 30-day score, long_weight of the 180-day score, plus liquidity."""
    if long_weight is None: long_weight = LONG_WINDOW_WEIGHT
    return 0.5*mid + long_weight*long + 10*liq

# D and F, approved by Stewart 22 Nov 2026, 6:10pm AEDT.
# The cuts live in research/screen.py. drift30 is win() on the last 30 completed
# dailies: absolute close-to-close move divided by the 5th-to-95th close range.
# ADX14 is win()'s ADX on that same window. The older high-low drift is not used.
# long_window_weight is not applied. It stays so the original tests still describe it.
def _load_screen():
    import importlib.util
    path = Path(__file__).resolve().parent / "research" / "screen.py"
    spec = importlib.util.spec_from_file_location("elite_intel_market_screen", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

screen = _load_screen()
TREND_DRIFT30_MIN = screen.TREND_DRIFT30_MIN
TREND_ADX14_MIN = screen.TREND_ADX14_MIN
ROOM_ABOVE_STOP_MIN = screen.ROOM_ABOVE_STOP_MIN
trend_skip = screen.trend_skip
room_above_stop = screen.room_above_stop
room_skip = screen.room_skip
skip_reasons_from_facts = screen.skip_reasons_from_facts
BIG_FOUR = screen.BIG_FOUR
RANGE_NOT_ACTIVE = screen.RANGE_NOT_ACTIVE
EXAMPLE_LEVEL_BARS = 90
LEVELS_STATE_NAME = "levels_state.json"

def example_levels(d):
    """Example range. Same geometry as the original levels(), on a 90-day window.
    Editions publish this 90-day construction; it is what gets frozen."""
    w = d.tail(EXAMPLE_LEVEL_BARS)
    lo = float(np.percentile(w.low, 5)) * 0.99
    hi = float(np.percentile(w.high, 95)) * 1.01
    return _range_fields(lo, hi, float(w.close.iloc[-1]), stop=lo * 0.96)

def _range_fields(lo, hi, now, stop):
    w = (hi - lo) / lo
    r = hi - lo
    return dict(bottom=lo, top=hi, entry=(lo, lo + r / 3), optimal=lo + r * 0.12, exit=(hi - r / 3, hi), stop=stop,
                grids=int(np.clip(round(w * 100 / 0.8), 10, 60)), type="geometric" if w > 0.15 else "arithmetic",
                now=float(now), width=w)

def completed_daily(d):
    """Drop a forming UTC daily so the close, drift and ADX are completed bars."""
    if "date" not in getattr(d, "columns", []):
        return d
    today = dt.datetime.now(dt.timezone.utc).date()
    done = d[d.date.dt.date < today]
    if len(done) == 0:
        return d.reset_index(drop=True)
    return done.reset_index(drop=True)

def drift_adx30(d):
    """win() drift30 and ADX14 on the last 30 completed dailies."""
    window = completed_daily(d).tail(30)
    _score, _cross, _width, drift, adx14 = win(window)
    return drift, adx14

def skip_reasons(d):
    """D on a rotation candidate. Uses the fresh example stop (the stop we would publish today)."""
    levels = example_levels(d)
    done = completed_daily(d)
    drift, adx14 = drift_adx30(d)
    return skip_reasons_from_facts(drift, adx14, float(done.close.iloc[-1]), levels["stop"])

def empty_levels_state():
    return {"picks": {}}

def load_levels_state(path):
    path = Path(path)
    if not path.exists():
        return empty_levels_state()
    state = json.loads(path.read_text())
    state.setdefault("picks", {})
    return state

def save_levels_state(path, state):
    Path(path).write_text(json.dumps(state, indent=1) + "\n")

def _active_stint(state, coin):
    stints = state["picks"].get(coin, {})
    active = sorted((k, v) for k, v in stints.items() if v.get("active"))
    return active[-1] if active else None

def published_example_stop(state, coin, fresh):
    """Stop a reader would see: the frozen stop while that pick is live, else today's."""
    active = _active_stint(state, coin)
    if active:
        return active[1]["stop"]
    return fresh["stop"]

def present_big_four(coin, levels, last_close, stop):
    """F presentation. Below the example stop, do not reprint the old range."""
    if screen.is_range_not_active(last_close, stop):
        return {"coin": coin, "status": RANGE_NOT_ACTIVE, "now": float(last_close)}
    out = dict(levels)
    out["coin"] = coin
    out["status"] = "active"
    return out

def _fresh_key(stints, published_on):
    if published_on not in stints:
        return published_on
    n = 2
    while f"{published_on}#{n}" in stints:
        n += 1
    return f"{published_on}#{n}"

def apply_frozen(fresh, frozen):
    """Keep the first-published bottom, top and stop. Current price can move."""
    out = _range_fields(frozen["bottom"], frozen["top"], fresh["now"], stop=frozen["stop"])
    return out

def publish_levels(state, coin, fresh, published_on):
    """Freeze bottom, stop and range while the coin stays a live pick.
    A dropped coin that comes back is stored under the new date and gets fresh levels."""
    stints = state["picks"].setdefault(coin, {})
    active = _active_stint(state, coin)
    if active:
        out = apply_frozen(fresh, active[1])
    else:
        key = _fresh_key(stints, published_on)
        stints[key] = {"active": True, "bottom": fresh["bottom"], "top": fresh["top"], "stop": fresh["stop"]}
        out = dict(fresh)
    out["coin"] = coin
    return out

def mark_dropped(state, still_live):
    for coin, stints in state["picks"].items():
        if coin in still_live:
            continue
        for rec in stints.values():
            if rec.get("active"):
                rec["active"] = False

def kl(s,n=180):
    k=get(f"https://api.pionex.com/api/v1/market/klines?symbol={s}_USDT&interval=1D&limit={n}")["data"]["klines"]
    d=pd.DataFrame(k).astype({"open":float,"high":float,"low":float,"close":float,"volume":float})
    d["date"]=pd.to_datetime(d.time,unit="ms"); return d.sort_values("date").reset_index(drop=True)
def adx(d,n=14):
    d=d.reset_index(drop=True)
    h,l,c=d.high,d.low,d.close; up=h.diff(); dn=-l.diff()
    pdm=np.where((up>dn)&(up>0),up,0); ndm=np.where((dn>up)&(dn>0),dn,0)
    tr=pd.concat([h-l,(h-c.shift()).abs(),(l-c.shift()).abs()],axis=1).max(axis=1)
    atr=tr.ewm(alpha=1/n).mean(); pdi=100*pd.Series(pdm).ewm(alpha=1/n).mean()/atr; ndi=100*pd.Series(ndm).ewm(alpha=1/n).mean()/atr
    return float((100*(pdi-ndi).abs()/(pdi+ndi)).ewm(alpha=1/n).mean().iloc[-1])
def win(d):
    c=d.close; lo,hi=np.percentile(c,5),np.percentile(c,95); mid=(lo+hi)/2
    cross=int((np.sign(c-mid).diff().fillna(0)!=0).sum())
    width=(hi-lo)/mid; drift=abs(c.iloc[-1]-c.iloc[0])/(hi-lo)
    a=adx(d); wsc=max(0,1-abs(width-0.25)/0.25)   # sweet spot ~25% width
    s=min(cross/len(c)*4,1)*35 + max(0,1-a/40)*25 + max(0,1-drift)*25 + wsc*15
    return s,cross,width,drift,a
def main():
    mk=get("https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=80&page=1")
    by=set()
    for pg in range(1,4):
        by|={t["base"].upper() for t in get(f"https://api.coingecko.com/api/v3/exchanges/bybit_spot/tickers?page={pg}")["tickers"] if t["target"]=="USDT"}
    px={s["baseCurrency"] for s in get("https://api.pionex.com/api/v1/common/symbols")["data"]["symbols"] if s["quoteCurrency"]=="USDT" and s.get("enable") and s["type"]=="SPOT"}
    uni=[]
    for c in mk:
        s=c["symbol"].upper()
        if s in STABLE or "usd" in c["id"] or "wrapped" in c["id"] or "staked" in c["id"]: continue
        if s in by and s in px: uni.append((s,c["name"],c["market_cap"],c["total_volume"]))
        if len(uni)>=30: break
    rows=[]; data={}
    for s,name,mc,vol in uni:
        try: d=kl(s)
        except Exception as e: print("skip",s,e); continue
        if len(d)<120: continue
        data[s]=d; m=win(d.tail(30)); L=win(d)
        liq=min(np.log10(max(vol,1))/10,1)  # $10B/day = 1
        if is_squeeze(m[2], L[2]): continue
        reasons=skip_reasons(d)
        if reasons:
            print("skip", s + ":", "; ".join(reasons))
            continue
        score=composite_score(m[0], L[0], liq)
        rows.append(dict(coin=s,name=name,score=round(score,1),mid30=round(m[0],1),long180=round(L[0],1),cross30=m[1],width30=round(m[2],3),drift30=round(m[3],2),adx14=round(m[4],1),cross180=L[1],width180=round(L[2],3),vol24h_usd=int(vol)))
    df=pd.DataFrame(rows)
    if df.empty:
        df=pd.DataFrame(columns=["coin","name","score","mid30","long180","cross30","width30","drift30","adx14","cross180","width180","vol24h_usd"])
    else:
        df=df.sort_values("score",ascending=False)
    df.to_csv("scores.csv",index=False)
    asof=dt.datetime.now(ZoneInfo("Australia/Sydney"))
    published_on=asof.date().isoformat()
    state_path=Path(LEVELS_STATE_NAME)
    state=load_levels_state(state_path)
    four=[s for s in BIG_FOUR if s in data]
    rotation=[]
    for s in df.head(5).coin.tolist():
        drift, adx14 = drift_adx30(data[s])
        fresh = example_levels(data[s])
        done = completed_daily(data[s])
        rotation.append(dict(coin=s, drift30=drift, adx14=adx14, last_close=float(done.close.iloc[-1]), stop=fresh["stop"]))
    four_rows=[]
    for s in four:
        fresh = example_levels(data[s])
        done = completed_daily(data[s])
        last_close = float(done.close.iloc[-1])
        four_rows.append(dict(coin=s, last_close=last_close, stop=published_example_stop(state, s, fresh), now=last_close))
    if "BTC" in data:
        btc_drift, btc_adx = drift_adx30(data["BTC"])
    else:
        btc_drift, btc_adx = 0.0, 0.0
    screened = screen.evaluate_market(btc_drift, btc_adx, four_rows, rotation)
    if screened["regime"]:
        print(screened["regime_reason"])
    inactive={row["coin"] for row in screened["four"] if row["status"]==RANGE_NOT_ACTIVE}
    # A range that is not active is not reprinted, including via the rotation list.
    top=[p["coin"] for p in screened["picks"] if p["coin"] not in inactive]
    live=set(top)|{row["coin"] for row in screened["four"] if row["status"]!=RANGE_NOT_ACTIVE}
    mark_dropped(state, live)
    def levels(s):
        return publish_levels(state, s, example_levels(data[s]), published_on)
    picks=[levels(s) for s in top]
    four_levels=[]
    for row in screened["four"]:
        if row["status"]==RANGE_NOT_ACTIVE:
            four_levels.append(present_big_four(row["coin"], None, row["last_close"], row["stop"]))
        else:
            four_levels.append(present_big_four(row["coin"], levels(row["coin"]), row["last_close"], row["stop"]))
    save_levels_state(state_path, state)
    json.dump(dict(asof=asof.strftime("%-I:%M%p %-d %b %Y").lower().replace("am","am").replace("pm","pm"),source="Pionex public API (daily candles), CoinGecko (market cap, Bybit listings)",
      regime=screened["regime"], regime_reason=screened["regime_reason"],
      picks=picks,four=four_levels),open("levels.json","w"),indent=1,default=float)
    for s in set(top)|{"BTC","ETH","SOL","XRP"}:
        if s in data: data[s].to_csv(f"candles_{s}.csv",index=False)
    print(df.to_string(index=False)); print(asof)

if __name__=="__main__":
    main()
