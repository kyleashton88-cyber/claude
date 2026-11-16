import requests, time, pandas as pd, sys, os
BASE="https://data-api.binance.vision/api/v3/klines"
def fetch(sym, iv, start_ms, end_ms):
    out=[]; s=start_ms
    while s<end_ms:
        r=requests.get(BASE,params=dict(symbol=sym,interval=iv,startTime=s,endTime=end_ms,limit=1000),timeout=30)
        r.raise_for_status(); d=r.json()
        if not d: break
        out+=d; s=d[-1][0]+1
        if len(d)<1000: break
    df=pd.DataFrame(out,columns="t o h l c v ct qv n tb tq x".split())[["t","o","h","l","c","v"]]
    df=df.astype(float); df["t"]=df["t"].astype("int64")
    return df.drop_duplicates("t")
start=int(pd.Timestamp("2023-08-01",tz="UTC").timestamp()*1000)
end=int(pd.Timestamp("2026-11-10",tz="UTC").timestamp()*1000)
for sym in ["BTCUSDT","ETHUSDT","SOLUSDT","ZECUSDT"]:
    for iv in ["1h","4h"]:
        df=fetch(sym,iv,start,end); df.to_csv(f"data/{sym}_{iv}.csv",index=False)
        print(sym,iv,len(df),pd.to_datetime(df.t.iloc[0],unit="ms"),pd.to_datetime(df.t.iloc[-1],unit="ms"))
