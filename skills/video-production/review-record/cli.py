#!/usr/bin/env python3
"""Append-only review ledger and a review pack. Does not publish or email.

  python3 cli.py init --master clip.mp4 --id sample --format short --ledger out
  python3 cli.py qa --ledger out --report report.json
  python3 cli.py compliance --ledger out --report compliance.json
  python3 cli.py legal --ledger out --name "Alex Counsel" --date 2026-11-13 --report compliance.json
  python3 cli.py stewart --ledger out --decision yes --date 2026-11-13
  python3 cli.py status --ledger out
  python3 cli.py pack --ledger out --out pack-dir --qa report.json --compliance compliance.json --transcript t.vtt
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from record.ledger import Ledger, LedgerError  # noqa: E402
from record.pack import build_pack  # noqa: E402


def refuse_course(path: Path) -> None:
    if "course" in Path(path).resolve().parts:
        raise SystemExit(f"refusing to write into course/: {path}")


def _ledger(path: Path) -> Ledger:
    refuse_course(path)
    return Ledger(path)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Append-only approval ledger")
    sub = parser.add_subparsers(dest="cmd", required=True)

    init = sub.add_parser("init")
    init.add_argument("--master", type=Path, required=True)
    init.add_argument("--id", required=True)
    init.add_argument("--format", required=True)
    init.add_argument("--ledger", type=Path, required=True)

    qa = sub.add_parser("qa")
    qa.add_argument("--ledger", type=Path, required=True)
    qa.add_argument("--report", type=Path, required=True)

    comp = sub.add_parser("compliance")
    comp.add_argument("--ledger", type=Path, required=True)
    comp.add_argument("--report", type=Path, required=True)

    legal = sub.add_parser("legal")
    legal.add_argument("--ledger", type=Path, required=True)
    legal.add_argument("--name", required=True)
    legal.add_argument("--date", required=True)
    legal.add_argument("--report", type=Path, required=True)

    stewart = sub.add_parser("stewart")
    stewart.add_argument("--ledger", type=Path, required=True)
    stewart.add_argument("--decision", required=True, choices=("yes", "no"))
    stewart.add_argument("--date", required=True)

    status = sub.add_parser("status")
    status.add_argument("--ledger", type=Path, required=True)

    pack = sub.add_parser("pack")
    pack.add_argument("--ledger", type=Path, required=True)
    pack.add_argument("--out", type=Path, required=True)
    pack.add_argument("--qa", type=Path)
    pack.add_argument("--compliance", type=Path)
    pack.add_argument("--transcript", type=Path)

    args = parser.parse_args(argv)
    try:
        if args.cmd == "init":
            state = _ledger(args.ledger).init(master=args.master, master_id=args.id, fmt=args.format)
        elif args.cmd == "qa":
            _ledger(args.ledger).record_qa(args.report)
            state = _ledger(args.ledger).state()
        elif args.cmd == "compliance":
            _ledger(args.ledger).record_compliance(args.report)
            state = _ledger(args.ledger).state()
        elif args.cmd == "legal":
            _ledger(args.ledger).legal(name=args.name, day=args.date, report_path=args.report)
            state = _ledger(args.ledger).state()
        elif args.cmd == "stewart":
            _ledger(args.ledger).stewart(decision=args.decision, day=args.date)
            print("Recorded Stewart's decision. No message was sent.")
            state = _ledger(args.ledger).state()
        elif args.cmd == "status":
            state = _ledger(args.ledger).state()
        elif args.cmd == "pack":
            refuse_course(args.out)
            ledger = _ledger(args.ledger)
            state = ledger.state()
            master = Path(state["master"])
            build_pack(
                folder=args.out,
                master=master,
                qa_report=args.qa,
                compliance_report=args.compliance,
                transcript=args.transcript,
                state=state,
            )
            print(f"pack {args.out}")
        else:
            return 2
    except LedgerError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    print(json.dumps({"publish_allowed": state["publish_allowed"], "blocked_by": state["blocked_by"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
