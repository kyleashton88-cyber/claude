import numpy as np, pandas as pd, cipher_sim as C, grid_sim as G, sys, random, multiprocessing as mp
TF = sys.argv[1]; N = int(sys.argv[2])
SYMS = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "ZECUSDT"]
SP = dict(chlen=[6, 9, 12], avg=[12, 21], lvl=[30.0, 40.0, 53.0, 60.0, 70.0], tp=[0.5, 0.75, 1.0, 1.5, 2.0, 3.0, 4.0],
          sl=[1.0, 1.5, 2.0, 3.0, 4.0, 6.0], hold=[0, 12, 24, 48, 96], trend=["none", "ema", "htf"], adxMax=[0.0, 20.0, 25.0, 35.0],
          side=["both", "long", "short"], wk=[False, True], oppExit=[False, True], frac=[0.5, 1.0])
DATA = {}
def init():
    for s in SYMS: DATA[s] = G.Data(s, TF)
def job(a):
    i, p = a; out = dict(idx=i, **{k: p[k] for k in SP if k in p})
    for s in SYMS:
        D = DATA[s]; n = len(D.c); sp = int(n * 0.7)
        for seg, (x, y) in [("IS", (1, sp)), ("OOS", (sp, n))]:
            r = C.run(D, p, x, y)
            for k in ["trades", "win", "ret", "dd", "pf", "avgWr", "avgLr"]: out[f"{seg}_{s[:3]}_{k}"] = r[k]
    return out
if __name__ == "__main__":
    rng = random.Random(11)
    confs = [(-1, dict(kind="baseline", chlen=9, avg=12, frac=1.0))]
    for i in range(N):
        p = {k: rng.choice(v) for k, v in SP.items()}; p["kind"] = "dots"; confs.append((i, p))
    with mp.Pool(8, initializer=init) as pool: res = pool.map(job, confs, chunksize=16)
    df = pd.DataFrame(res)
    for seg in ["IS", "OOS"]:
        for k in ["win", "ret", "trades", "dd", "pf"]:
            cols = [f"{seg}_{s[:3]}_{k}" for s in SYMS[:3]]
            df[f"{seg}min_{k}"] = df[cols].min(axis=1); df[f"{seg}max_{k}"] = df[cols].max(axis=1)
    df.to_csv(f"cipher_{TF}.csv", index=False)
    pd.set_option("display.width", 320); pd.set_option("display.max_columns", 80)
    print(df[df.idx == -1].filter(regex="IS_|OOS_").round(1).T.to_string())
    q = df[(df.ISmin_trades >= 30)]
    print("IS both:", ((q.ISmin_win >= 75) & (q.ISmin_ret >= 60)).sum(), "IS win75:", (q.ISmin_win >= 75).sum())
    show = ["idx","chlen","avg","lvl","tp","sl","hold","trend","adxMax","side","wk","oppExit","frac","ISmin_win","ISmin_ret","ISmax_dd","ISmin_trades","OOSmin_win","OOSmin_ret","OOSmax_ret","OOSmax_dd","OOSmin_trades","OOS_ZEC_ret"]
    q = q.assign(sc=q.ISmin_ret / q.ISmax_dd.clip(lower=5))
    print(q[q.ISmin_win >= 70].sort_values("sc", ascending=False)[show].head(25).round(1).to_string())
    print(q.sort_values("ISmin_ret", ascending=False)[show].head(15).round(1).to_string())
    print("OOS both (diagnostic only):", ((df.OOSmin_win >= 75) & (df.OOSmin_ret >= 60) & (df.OOSmin_trades >= 10)).sum())
