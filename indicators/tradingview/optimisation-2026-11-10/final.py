import pandas as pd, numpy as np, grid_sim as G, cipher_sim as C, json, robust as R
SY = ["BTCUSDT","ETHUSDT","SOLUSDT","ZECUSDT"]
sets = {"Baseline (live v2 settings) 1h": ("1h", dict(G.BASE)),
        "Baseline (live v2 settings) 4h": ("4h", dict(G.BASE)),
        "Recommended v3 (4h, Auto)": ("4h", json.load(open("params_4h_1130.json"))),
        "Alt: max OOS growth w/ win>=75 (1h, fragile)": ("1h", json.load(open("params_1h_4194.json")))}
rows = []; split_dates = {}
for name, (tf, p) in sets.items():
    for k in ["rangeLen","gridCount","maxOpen","cooldown","adxLen","bbLen","emaLen","sideFilt","cbStreak","cbPause","spikeCool","atrLen"]:
        p[k] = int(p[k])
    for k in ["useRegime","tpEdge","useSpike","useCb","useWk"]:
        p[k] = p[k] if isinstance(p[k], bool) else str(p[k]) == "True"
    for s in SY:
        D = G.Data(s, tf); N = len(D.c); sp = int(N * .7)
        split_dates[tf] = (str(pd.to_datetime(D.t[1], unit="ms").date()), str(pd.to_datetime(D.t[sp], unit="ms").date()), str(pd.to_datetime(D.t[-1], unit="ms").date()))
        for seg, (a, b) in [("IS", (1, sp)), ("OOS", (sp, N))]:
            for cost, (fee, slip) in {"0.10%+0.03%": (0.001, 0.0003)}.items():
                r = G.run(D, p, a, b, fee, slip); r.update(set=name, sym=s, seg=seg); rows.append(r)
        if name.startswith("Baseline (live v2 settings) 1h"):
            r = G.run(D, p, 1, N, 0.00055, 0.0); r.update(set=name + " @script costs 0.055%", sym=s, seg="FULL"); rows.append(r)
# Cipher B baseline
for tf in ["1h", "4h"]:
    for s in SY:
        D = G.Data(s, tf); N = len(D.c); sp = int(N * .7)
        for seg, (a, b) in [("IS", (1, sp)), ("OOS", (sp, N))]:
            r = C.run(D, dict(kind="baseline", chlen=9, avg=12, frac=1.0), a, b); r.update(set=f"Cipher B ref strategy (WT cross SAR) {tf}", sym=s, seg=seg); rows.append(r)
df = pd.DataFrame(rows)
df.to_csv("final_results.csv", index=False)
json.dump(split_dates, open("split_dates.json", "w"))
pd.set_option("display.width", 250)
print(split_dates)
print(df[["set","sym","seg","trades","win","ret","dd","pf","avgWr","avgLr","avgW","avgL","exp","tpN","slN","mktN"]].round(2).to_string())
