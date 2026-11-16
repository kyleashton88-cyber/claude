import numpy as np, pandas as pd, grid_sim as G, json
rows = []
for tf in ["1h", "4h"]:
    for sym in ["BTCUSDT", "ETHUSDT", "SOLUSDT", "ZECUSDT"]:
        D = G.Data(sym, tf); N = len(D.c); split = int(N * 0.7)
        for name, (s, e) in {"full": (1, N), "IS": (1, split), "OOS": (split, N)}.items():
            r = G.run(D, G.BASE, s, e); r.update(sym=sym, tf=tf, seg=name); rows.append(r)
df = pd.DataFrame(rows)
pd.set_option("display.width", 250)
print(df[["tf","sym","seg","trades","win","ret","dd","pf","avgWr","avgLr","exp","tpN","slN","mktN"]].round(2).to_string())
df.to_csv("baseline.csv", index=False)
