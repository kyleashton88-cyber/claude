import numpy as np, pandas as pd, grid_sim as G, sys, json, multiprocessing as mp, random
TF = sys.argv[1] if len(sys.argv) > 1 else "1h"
NCONF = int(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[2].isdigit() else 2000
SYMS = ["BTCUSDT", "ETHUSDT", "SOLUSDT"]
SPACE = dict(mode=["Neutral", "Long", "Short", "Auto", "Auto", "Auto"], rangeSrc=["Donchian", "ATR", "Percentile"],
             rangeLen=[50, 75, 100, 150, 200, 300], atrMult=[2.0, 3.0, 4.0, 6.0], pctHi=[85.0, 90.0, 95.0], pctLo=[5.0, 10.0, 15.0],
             spacing=["Geometric", "Arithmetic"], gridCount=[4, 6, 8, 10, 14, 20], minStep=[0.4, 0.6, 0.8, 1.0, 1.5, 2.0],
             adxMax=[16.0, 20.0, 22.0, 25.0, 30.0], bbwMax=[3.0, 5.0, 8.0, 12.0], useRegime=[True, True, False],
             qtyPct=[5.0, 10.0, 15.0, 20.0, 25.0, 33.0, 50.0], maxOpen=[2, 3, 4, 6, 10], stopAtr=[0.5, 1.0, 2.0, 3.0, 5.0, 8.0],
             tpEdge=[True, False], cooldown=[0, 6, 12, 24], useSpike=[True, False], useCb=[True, False],
             hardDd=[20.0, 30.0, 100.0], useWk=[False, True], sideFilt=[0, 1], emaLen=[100, 200], adxLen=[14], bbLen=[20])
DATA = {}
def init():
    for s in SYMS:
        D = G.Data(s, TF); DATA[s] = D
def sample(rng):
    p = dict(G.BASE)
    while True:
        for k, v in SPACE.items(): p[k] = rng.choice(v)
        if p["qtyPct"] * p["maxOpen"] <= 100.0: return p   # never more than 100% of equity deployed (no leverage)
def evalp(args):
    idx, p = args
    out = dict(idx=idx, **{k: p[k] for k in SPACE})
    for s in SYMS:
        D = DATA[s]; N = len(D.c); sp = int(N * 0.7)
        r = G.run(D, p, 1, sp)
        for k in ["trades", "win", "ret", "dd", "pf", "exp", "avgWr", "avgLr"]: out[f"{s[:3]}_{k}"] = r[k]
    return out
if __name__ == "__main__":
    rng = random.Random(int(sys.argv[3]) if len(sys.argv) > 3 else 42)
    confs = [(i, sample(rng)) for i in range(NCONF)]
    confs.insert(0, (-1, dict(G.BASE)))
    with mp.Pool(8, initializer=init) as pool:
        res = pool.map(evalp, confs, chunksize=8)
    df = pd.DataFrame(res); df.to_csv(f"search_{TF}_IS_{sys.argv[3] if len(sys.argv)>3 else 42}.csv", index=False)
    for k in ["win", "ret", "pf", "trades", "dd"]:
        cols = [f"{s[:3]}_{k}" for s in SYMS]
        df[f"min_{k}"] = df[cols].min(axis=1); df[f"max_{k}"] = df[cols].max(axis=1)
    pd.set_option("display.width", 300); pd.set_option("display.max_columns", 60)
    q = df[df.min_trades >= 30]
    print("configs with min_win>=75:", (q.min_win >= 75).sum(), " min_ret>=60 (IS 2.3y):", (q.min_ret >= 60).sum(),
          " both:", ((q.min_win >= 75) & (q.min_ret >= 60)).sum(), " min_pf>1:", (q.min_pf > 1).sum())
    show = ["idx","mode","rangeSrc","rangeLen","gridCount","minStep","stopAtr","qtyPct","maxOpen","tpEdge","useRegime","sideFilt","useWk","min_win","min_ret","max_dd","min_pf","min_trades"]
    print(q.sort_values("min_win", ascending=False)[show].head(15).to_string())
    print(q.sort_values("min_ret", ascending=False)[show].head(15).to_string())
    print(q[q.min_win >= 75].sort_values("min_ret", ascending=False)[show].head(15).to_string())
