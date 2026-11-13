#!/usr/bin/env python3
"""Build a shot list from a lesson script or lesson.yaml.

  python3 cli.py plan samples/lesson.yaml --out out-dir
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from planner.plan import plan_path, write_plan  # noqa: E402


def refuse_course(path: Path) -> None:
    if "course" in path.resolve().parts:
        raise SystemExit(f"refusing to write into course/: {path}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Plan shots so the picture changes within 8 seconds")
    sub = parser.add_subparsers(dest="cmd", required=True)
    plan = sub.add_parser("plan")
    plan.add_argument("source", type=Path)
    plan.add_argument("--out", type=Path, required=True)
    args = parser.parse_args(argv)
    refuse_course(args.out)
    data = plan_path(args.source)
    yaml_path, md_path = write_plan(data, args.out)
    print(f"{data['shot_count']} shots  {yaml_path}")
    print(md_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
