#!/usr/bin/env python3
"""Insert lesson images into lessons/module-*.md, right after each lesson's Objective
paragraph (Mastery Starters: after the intro line). Idempotent: never adds a file twice.

Usage: python3 export/wire_lesson_images.py <create.json>   (list of [lesson, path, alt])
Reused images are skipped when the lesson already has any image; new images are skipped
only when the lesson already shows that exact file.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REUSE = [("0.5", "diagrams/seed-backup.png", "Backing up a seed phrase"), ("0.6", "diagrams/first-transfer.png", "Your first transfer"),
         ("1.3", "diagrams/three-wallets.png", "The 3-wallet setup"), ("1.9", "diagrams/three-wallets.png", "The 3-wallet setup"),
         ("2.4", "charts/impermanent-loss.png", "Impermanent loss vs simply holding"), ("2.7", "charts/lvr.png", "Loss-versus-rebalancing"),
         ("2.8", "diagrams/mev-supply-chain.png", "The MEV supply chain"), ("3.3", "diagrams/liquidation-cascade.png", "The liquidation cascade"),
         ("3.6", "diagrams/liquidation-cascade.png", "The liquidation cascade"), ("3.4", "charts/loop-spread.png", "Leveraged loop: the spread is everything"),
         ("6.1", "diagrams/research-loop.png", "The 6-step research loop"), ("9.1", "diagrams/grid-vs-lp.png", "Grid bot vs concentrated LP"),
         ("10.1", "charts/pt-convergence.png", "PT price converging to par"), ("10.8", "charts/pt-convergence.png", "PT price converging to par"),
         ("12.2", "diagrams/custody-architecture.png", "Custody architecture"), ("12.8", "diagrams/custody-architecture.png", "Custody architecture"),
         ("12.4", "diagrams/liquidity-ladder.png", "The liquidity ladder"), ("13.3", "charts/income-waterfall.png", "From headline yield to a sustainable payout")]


def module_files():
    return {int(re.match(r"module-(\d+)", f.name).group(1)): f for f in (ROOT / "lessons").glob("module-*.md")}


def insert(text, lid, tag, path, reuse):
    m = re.search(rf"^## Lesson {re.escape(lid)} — .*$", text, flags=re.M)
    if not m:
        return text, "lesson not found"
    end = text.find("\n## ", m.end())
    end = len(text) if end < 0 else end
    sec = text[m.end():end]
    if f"(../assets/{path})" in sec:
        return text, "already there"
    if reuse and "![" in sec:
        return text, "skipped (has an image)"
    obj = re.search(r"^### Objective\n", sec, flags=re.M)
    if obj:  # after the objective paragraph
        para_end = re.search(r"\n\s*\n|\n(?=### )", sec[obj.end():])
        at = obj.end() + (para_end.start() if para_end else len(sec) - obj.end())
    else:    # Mastery Starter: before the first ### section
        first = re.search(r"^### ", sec, flags=re.M)
        at = first.start() - 1 if first else len(sec)
    new = sec[:at].rstrip("\n") + f"\n\n{tag}\n\n" + sec[at:].lstrip("\n")
    return text[:m.end()] + new + text[end:], "wired"


def main():
    files = module_files()
    rows = []
    jobs = [(l, p, a, True) for l, p, a in REUSE]
    for n, f in sorted(files.items()):
        title = re.match(r"# Module \d+ — (.+)", f.read_text()).group(1).strip()
        jobs.append((f"{n}.0", f"modules/module-{n:02d}.png", f"Module {n} — {title}", True))
    jobs += [(l, p, a, False) for l, p, a in json.loads(Path(sys.argv[1]).read_text())]
    for lid, path, alt, reuse in sorted(jobs, key=lambda j: [int(x) for x in j[0].split(".")]):
        f = files[int(lid.split(".")[0])]
        text, status = insert(f.read_text(), lid, f"![{alt}](../assets/{path})", path, reuse)
        f.write_text(text)
        rows.append((lid, f"assets/{path}", status, "new" if not reuse else "reuse"))
    print("| Lesson | File | Type | Wired |\n|---|---|---|---|")
    for lid, p, st, kind in rows:
        print(f"| {lid} | `{p}` | {kind} | {'yes' if st in ('wired', 'already there') else 'no'} ({st}) |")


if __name__ == "__main__":
    main()
