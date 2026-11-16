import numpy as np, pandas as pd, grid_sim as G, sys, multiprocessing as mp, random, json
from search import SPACE
TF = sys.argv[1]; f = sys.argv[2]
SYMS = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "ZECUSDT"]
DATA = {}
def init():
    for s in SYMS: DATA[s] = G.Data(s, TF)
def ev(p, seg):
    out = {}
    for s in SYMS:
        D = DATA[s]; N = len(D.c); sp = int(N * 0.7)
        a, b = (1, sp) if seg == "IS" else (sp, N)
        r = G.run(D, p, a, b)
        for k in ["trades", "win", "ret", "dd", "pf", "exp", "avgWr", "avgLr"]: out[f"{s[:3]}_{k}"] = r[k]
    return out
def neigh(p, rng, k=12):
    outs = []
    for _ in range(k):
        q = dict(p)
        for key in rng.sample(list(SPACE.keys()), 2):
            vals = SPACE[key]; uniq = list(dict.fromkeys(vals))
            if p[key] in uniq:
                i = uniq.index(p[key]); j = min(max(i + rng.choice([-1, 1]), 0), len(uniq) - 1); q[key] = uniq[j]
        if q["qtyPct"] * q["maxOpen"] > 100: continue
        outs.append(q)
    return outs
def job(row):
    p = dict(G.BASE); p.update({k: row[k] for k in SPACE})
    for k in ["rangeLen","gridCount","maxOpen","cooldown","adxLen","bbLen","emaLen","sideFilt"]: p[k] = int(p[k])
    for k in ["useRegime","tpEdge","useSpike","useCb","useWk"]: p[k] = bool(p[k])
    o = ev(p, "OOS"); o["idx"] = row["idx"]
    rng = random.Random(int(row["idx"]) + 1)
    nb = []
    for q in neigh(p, rng):
        r = ev(q, "IS"); nb.append(min(r[f"{s[:3]}_ret"] for s in SYMS[:3]))
    o["nbmed"] = float(np.median(nb)) if nb else np.nan
    o["nbpos"] = float(np.mean(np.array(nb) > 0)) if nb else np.nan
    return o
if __name__ == "__main__":
    df = pd.read_csv(f)
    for k in ["win","ret","pf","trades","dd"]:
        cols = [f"{s[:3]}_{k}" for s in SYMS[:3]]
        df[f"min_{k}"] = df[cols].min(axis=1); df[f"max_{k}"] = df[cols].max(axis=1)
    q = df[(df.min_trades >= 30) & (df.min_win >= 70) & (df.min_pf > 1.1)].copy()
    q["score"] = q.min_ret / q.max_dd.clip(lower=5)
    top = pd.concat([q.sort_values("score", ascending=False).head(40), q.sort_values("min_ret", ascending=False).head(20),
                     q.sort_values("min_win", ascending=False).head(20)]).drop_duplicates("idx")
    base = df[df.idx == -1]
    top = pd.concat([base, top])
    with mp.Pool(8, initializer=init) as pool:
        res = pool.map(job, [r for _, r in top.iterrows()])
    o = pd.DataFrame(res).add_prefix("O_").rename(columns={"O_idx": "idx"})
    m = top.merge(o, on="idx")
    for k in ["win","ret","pf","trades","dd"]:
        cols = [f"O_{s[:3]}_{k}" for s in SYMS[:3]]
        m[f"Omin_{k}"] = m[cols].min(axis=1); m[f"Omax_{k}"] = m[cols].max(axis=1); m[f"Osum_{k}"] = m[cols].sum(axis=1)
    m.to_csv(f"oos_{TF}.csv", index=False)
    pd.set_option("display.width", 320); pd.set_option("display.max_columns", 80)
    show = ["idx","mode","rangeSrc","rangeLen","gridCount","minStep","stopAtr","qtyPct","maxOpen","tpEdge","sideFilt","useWk","min_win","min_ret","max_dd","Omin_win","Omin_ret","Omax_ret","Omax_dd","Omin_pf","Osum_trades","O_ZEC_ret","O_ZEC_win","O_nbmed","O_nbpos"]
    show = [c for c in dict.fromkeys(show) if c in m]
    print(m.sort_values("Omin_ret", ascending=False)[show].head(30).round(1).to_string())
    print("OOS both targets met (all 3 syms):", ((m.Omin_win >= 75) & (m.Omin_ret >= 60)).sum(), "of", len(m))
