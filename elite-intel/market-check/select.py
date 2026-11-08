"""Grid-suitability screen. Universe: CoinGecko top coins by mkt cap, non-stable, listed on Bybit spot (CoinGecko tickers) and Pionex (Pionex API).
Daily candles: Pionex public klines (USDT pairs). Output: scores.csv, levels.json"""
import json, urllib.request, datetime as dt, numpy as np, pandas as pd
from zoneinfo import ZoneInfo
def get(u): return json.load(urllib.request.urlopen(urllib.request.Request(u,headers={"User-Agent":"Mozilla/5.0"}),timeout=30))
STABLE={"USDT","USDC","DAI","USDE","FDUSD","TUSD","USDS","PYUSD","USD1","USDD","BUSD","RLUSD","USDTB","USDF","USDG","FRAX","GHO","EURC","USD0","BFUSD","SUSDS","SUSDE","XAUT","PAXG","USYC","BUIDL","USDX"}
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
rows=[]; data={}
for s,name,mc,vol in uni:
    try: d=kl(s)
    except Exception as e: print("skip",s,e); continue
    if len(d)<120: continue
    data[s]=d; m=win(d.tail(30)); L=win(d)
    liq=min(np.log10(max(vol,1))/10,1)  # $10B/day = 1
    score=0.5*m[0]+0.4*L[0]+10*liq
    rows.append(dict(coin=s,name=name,score=round(score,1),mid30=round(m[0],1),long180=round(L[0],1),cross30=m[1],width30=round(m[2],3),drift30=round(m[3],2),adx14=round(m[4],1),cross180=L[1],width180=round(L[2],3),vol24h_usd=int(vol)))
df=pd.DataFrame(rows).sort_values("score",ascending=False); df.to_csv("scores.csv",index=False)
asof=dt.datetime.now(ZoneInfo("Australia/Sydney"))
def levels(s):
    d=data[s].tail(30); c=d.close   # example range from the mid-term (30-day) window
    lo=float(np.percentile(d.low,5))*0.99; hi=float(np.percentile(d.high,95))*1.01
    w=(hi-lo)/lo; geo=w>0.15; r=hi-lo
    return dict(coin=s,bottom=lo,top=hi,entry=(lo,lo+r/3),optimal=lo+r*0.12,exit=(hi-r/3,hi),stop=lo*0.96,
                grids=int(np.clip(round(w*100/0.8),10,60)),type="geometric" if geo else "arithmetic",now=float(c.iloc[-1]),width=w)
top=df.head(5).coin.tolist()
json.dump(dict(asof=asof.strftime("%-I:%M%p %-d %b %Y").lower().replace("am","am").replace("pm","pm"),source="Pionex public API (daily candles), CoinGecko (market cap, Bybit listings)",
  picks=[levels(s) for s in top],four=[levels(s) for s in ["BTC","ETH","SOL","XRP"] if s in data]),open("levels.json","w"),indent=1,default=float)
for s in set(top)|{"BTC","ETH","SOL","XRP"}:
    if s in data: data[s].to_csv(f"candles_{s}.csv",index=False)
print(df.to_string(index=False)); print(asof)
