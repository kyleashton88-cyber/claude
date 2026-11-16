import pandas as pd, numpy as np, grid_sim as G, robust as R, random, json, sys
from search import SPACE
SY = R.SY
cands = {
 "4h_plateau": ("4h", dict(mode="Auto", rangeSrc="Percentile", rangeLen=300, pctHi=90.0, pctLo=10.0, gridCount=10, minStep=1.5, stopAtr=3.0,
     qtyPct=5.0, maxOpen=6, sideFilt=1, emaLen=100, useRegime=True, adxMax=16.0, cooldown=24, tpEdge=True, useSpike=False, useCb=True, hardDd=20.0)),
 "4h_plateau_b": ("4h", dict(mode="Auto", rangeSrc="Percentile", rangeLen=200, pctHi=95.0, pctLo=5.0, gridCount=14, minStep=1.0, stopAtr=3.0,
     qtyPct=5.0, maxOpen=6, sideFilt=1, emaLen=100, useRegime=False, cooldown=12, tpEdge=True, useSpike=False, useCb=True, hardDd=20.0)),
 "1h_plateau": ("1h", dict(mode="Auto", rangeSrc="Percentile", rangeLen=150, gridCount=8, minStep=1.5, stopAtr=3.0, qtyPct=5.0, maxOpen=10,
     sideFilt=1, emaLen=200, useRegime=True, cooldown=24, hardDd=20.0)),
}
cands["4h_1130"] = ("4h", R.mk("4h", "oos_4h.csv", 1130))
out = {}
for name, (tf, upd) in cands.items():
    DS = {s: G.Data(s, tf) for s in SY}
    p = dict(G.BASE); p.update(upd)
    base = R.summ(R.ev(DS, p)); nohalt = R.summ(R.ev(DS, dict(p, hardDd=100.0, useCb=False)))
    rng = random.Random(5); nb = []
    for _ in range(40):
        q = dict(p)
        for key in rng.sample([k for k in SPACE if k not in ("adxLen", "bbLen")], 2):
            u = list(dict.fromkeys(SPACE[key]))
            if q[key] in u: q[key] = u[min(max(u.index(q[key]) + rng.choice([-1, 1]), 0), len(u) - 1)]
        if q["qtyPct"] * q["maxOpen"] > 100: continue
        nb.append(R.summ(R.ev(DS, q)))
    nb = pd.DataFrame(nb)
    out[name] = dict(base=base, nohalt=nohalt, nb_IS_pos=float((nb.IS_minret > 0).mean()), nb_OOS_pos=float((nb.OOS_minret > 0).mean()),
                     nb_OOS_win75=float((nb.OOS_minwin >= 75).mean()), nb_med_IS=float(nb.IS_minret.median()), nb_med_OOS=float(nb.OOS_minret.median()))
    print(name, json.dumps({k: (round(v, 2) if isinstance(v, float) else {a: round(b, 1) for a, b in v.items()}) for k, v in out[name].items()}))
    json.dump(p, open(f"params_{name}.json", "w"), indent=1, default=str)
