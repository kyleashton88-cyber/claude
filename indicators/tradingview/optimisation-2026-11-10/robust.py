import numpy as np, pandas as pd, grid_sim as G, sys, json
from search import SPACE
SY = ["BTCUSDT","ETHUSDT","SOLUSDT","ZECUSDT"]
def mk(tf, f, i):
    m = pd.read_csv(f); r = m[m.idx == i].iloc[0]; p = dict(G.BASE)
    for k in SPACE: p[k] = r[k].item() if hasattr(r[k], "item") else r[k]
    for k in ["useRegime","tpEdge","useSpike","useCb","useWk"]: p[k] = bool(p[k])
    for k in ["rangeLen","gridCount","maxOpen","cooldown","adxLen","bbLen","emaLen","sideFilt"]: p[k] = int(p[k])
    return p
def ev(DS, p, fee=0.001, slip=0.0003):
    o = {}
    for s, D in DS.items():
        N = len(D.c); sp = int(N * .7)
        for seg, (a, b) in [("IS", (1, sp)), ("OOS", (sp, N))]:
            r = G.run(D, p, a, b, fee, slip); o[(s, seg)] = r
    return o
def summ(o):
    g = lambda seg, k, f: f(o[(s, seg)][k] for s in SY[:3])
    return dict(IS_minwin=g("IS","win",min), IS_minret=g("IS","ret",min), IS_maxdd=g("IS","dd",max),
                OOS_minwin=g("OOS","win",min), OOS_minret=g("OOS","ret",min), OOS_maxret=g("OOS","ret",max), OOS_maxdd=g("OOS","dd",max),
                OOS_trades=g("OOS","trades",sum), ZEC_OOS_ret=o[("ZECUSDT","OOS")]["ret"])
if __name__ == "__main__":
    tf, f, i = sys.argv[1], sys.argv[2], int(sys.argv[3])
    DS = {s: G.Data(s, tf) for s in SY}
    p = mk(tf, f, i); rows = []
    rows.append(dict(param="(chosen)", value="", **summ(ev(DS, p))))
    for fee, slip in [(0.00055, 0.0001), (0.001, 0.001), (0.0015, 0.001)]:
        rows.append(dict(param="costs", value=f"fee{fee*100:.3f}%/slip{slip*100:.2f}%", **summ(ev(DS, p, fee, slip))))
    extra = dict(useCb=[True, False], hardDd=[20.0, 30.0, 100.0])
    for k, vals in {**SPACE, **extra}.items():
        for v in dict.fromkeys(vals):
            if v == p[k] or k in ("adxLen","bbLen"): continue
            q = dict(p); q[k] = v
            if q["qtyPct"] * q["maxOpen"] > 100: continue
            rows.append(dict(param=k, value=v, **summ(ev(DS, q))))
    df = pd.DataFrame(rows); df.to_csv(f"robust_{tf}_{i}.csv", index=False)
    pd.set_option("display.width", 250)
    print(df.round(1).to_string())
    pp = df[df.param.isin(list(SPACE))]
    print("one-step variants:", len(pp), " OOS minret>0:", (pp.OOS_minret > 0).mean().round(2), " OOS minwin>=75:", (pp.OOS_minwin >= 75).mean().round(2), " median OOS minret:", pp.OOS_minret.median().round(1))
    json.dump(p, open(f"params_{tf}_{i}.json", "w"), indent=1, default=str)
