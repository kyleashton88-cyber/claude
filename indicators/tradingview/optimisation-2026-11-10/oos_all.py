# Diagnostic with HINDSIGHT: evaluate every sampled config on the OOS window to see whether 75%/60% exists at all.
import pandas as pd, numpy as np, grid_sim as G, sys, multiprocessing as mp
from search import SPACE
TF, f = sys.argv[1], sys.argv[2]
SY = ["BTCUSDT","ETHUSDT","SOLUSDT"]; DATA = {}
def init():
    for s in SY: DATA[s] = G.Data(s, TF)
def job(row):
    p = dict(G.BASE)
    for k in SPACE:
        v = row[k]; p[k] = v.item() if hasattr(v, "item") else v
    for k in ["useRegime","tpEdge","useSpike","useCb","useWk"]: p[k] = bool(p[k])
    for k in ["rangeLen","gridCount","maxOpen","cooldown","adxLen","bbLen","emaLen","sideFilt"]: p[k] = int(p[k])
    o = {"idx": row["idx"]}
    for s in SY:
        D = DATA[s]; N = len(D.c); r = G.run(D, p, int(N*.7), N)
        o[f"{s[:3]}_win"], o[f"{s[:3]}_ret"], o[f"{s[:3]}_dd"], o[f"{s[:3]}_n"] = r["win"], r["ret"], r["dd"], r["trades"]
    return o
if __name__ == "__main__":
    df = pd.read_csv(f)
    with mp.Pool(8, initializer=init) as pool: res = pool.map(job, [r for _, r in df.iterrows()], chunksize=32)
    o = pd.DataFrame(res); o.to_csv(f"oos_all_{TF}.csv", index=False)
    w = o[[f"{s[:3]}_win" for s in SY]]; r = o[[f"{s[:3]}_ret" for s in SY]]; n = o[[f"{s[:3]}_n" for s in SY]]
    print(TF, "configs:", len(o), " max single-symbol OOS ret:", r.max().round(1).to_dict())
    ok = (n >= 30).values
    print(" any symbol with win>=75 & ret>=60 & n>=30:", int(((w.values >= 75) & (r.values >= 60) & ok).any(axis=1).sum()))
    print(" all 3 symbols win>=75 & ret>=60:", int(((w.values >= 75) & (r.values >= 60)).all(axis=1).sum()))
    print(" best min-ret across 3 syms with min win>=75 (hindsight):", r[(w.min(axis=1) >= 75) & (n.min(axis=1) >= 10)].min(axis=1).max().round(1))
    print(" best single-symbol ret with win>=75 & n>=30:", np.nanmax(np.where((w.values >= 75) & ok, r.values, np.nan)).round(1))
