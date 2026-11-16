"""Out-of-sample log for each pre-registered gate.

The gate list was fixed before this holdout. These rows are not used to
replace the walk-forward lock. 1x only, 4h, BTC ETH SOL ZEC.
"""
from __future__ import annotations

import json
from pathlib import Path

from run_round3 import OOS, REPORT, build_book, fetch_stable, pool_stats, run_book, spec_base

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "results"


def main():
    man = json.loads((ROOT / "data" / "manifest.json").read_text())
    stable_t, stable_chg = fetch_stable()
    rows = json.loads((OUT / "round3_variants.json").read_text())
    books = {}
    for inst in REPORT:
        books[inst] = build_book(inst, "4h", stable_t, stable_chg, man["symbols"][inst]["tick"])
    best = {}
    for row in rows:
        if row.get("stage") != "wf_select" or row.get("win") is None:
            continue
        if row.get("n", 0) < 40 or row.get("ret", -1) <= -0.005:
            continue
        key = (row["mode"], row["gate"])
        if key not in best or row["win"] > best[key]["win"]:
            best[key] = row
    report = []
    for (mode, gate), row in sorted(best.items()):
        spec = spec_base(mode, gate, row["range"], row["exit"])
        deps = []
        for inst in REPORT:
            deps.extend(run_book(books[inst], spec, OOS[0], OOS[1], 1.0))
        st = pool_stats(deps) or {"n": 0, "win": None, "ret": None}
        per = {}
        for inst in REPORT:
            sub = [d for d in deps if d["inst"] == inst]
            pst = pool_stats(sub) or {"n": 0, "win": None, "ret": None}
            per[inst] = {"n": pst["n"], "win": pst["win"], "ret": pst["ret"]}
        report.append({
            "mode": mode, "gate": gate, "range": row["range"], "exit": row["exit"],
            "wf_win": row["win"], "wf_n": row["n"], "wf_ret": row["ret"],
            "oos_n": st["n"], "oos_win": st["win"], "oos_ret": st["ret"], "by_coin": per,
        })
        print(mode[:4], gate, "oos", st["n"], None if st["win"] is None else round(st["win"], 3), flush=True)
    (OUT / "round3_indicator_oos.json").write_text(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
