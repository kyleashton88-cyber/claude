#!/usr/bin/env python3
"""Pass/fail a master against its format profile.

  python3 cli.py check master.mp4 --format short --captions master.vtt --out report-dir
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
VP = HERE.parent
if str(VP) not in sys.path:
    sys.path.insert(0, str(VP))
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from gate.evaluate import evaluate  # noqa: E402
from gate.profiles import PROFILES, get_profile  # noqa: E402
from gate.report import write_reports  # noqa: E402


def refuse_course(path: Path) -> None:
    if "course" in path.resolve().parts:
        raise SystemExit(f"refusing to write into course/: {path}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Pass/fail gate for a finished master")
    sub = parser.add_subparsers(dest="cmd", required=True)

    check = sub.add_parser("check", help="write report.json and report.md")
    check.add_argument("master", type=Path)
    check.add_argument("--format", required=True, help=", ".join(sorted(PROFILES)))
    check.add_argument("--captions", type=Path)
    check.add_argument("--transcript", type=Path)
    check.add_argument("--out", type=Path, required=True)
    check.add_argument("--max-hold", type=float, default=None)

    sub.add_parser("formats", help="list format profiles")

    args = parser.parse_args(argv)
    if args.cmd == "formats":
        for profile in PROFILES.values():
            print(
                f"{profile.name:14} {profile.label:18} "
                f"{profile.min_seconds:7.0f}s–{profile.max_seconds:7.0f}s  "
                f"{profile.width}x{profile.height}  hold {profile.max_hold_seconds:.0f}s"
            )
        return 0

    refuse_course(args.out)
    overrides = {}
    if args.max_hold is not None:
        overrides["max_hold_seconds"] = args.max_hold
    try:
        profile = get_profile(args.format, **overrides)
    except KeyError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    payload = evaluate(
        args.master,
        profile,
        captions=args.captions,
        transcript=args.transcript,
    )
    json_path, md_path = write_reports(payload, args.out)
    print(f"{payload['result'].upper()} {json_path}")
    print(md_path)
    return 0 if payload["result"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
