#!/usr/bin/env python3
"""One command from a lesson file to a mastered clip.

  python3 -m production_pipeline build examples/lesson.yaml --out test-outputs/demo

Stages, in order, are hooks another tool can replace:
narrate, align, illustrate, motion, grade, music, captions, endcard, loudness.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE.parents[1] / "video-production"))
sys.path.insert(0, str(HERE.parents[1] / "video-production" / "natural-voice"))
sys.path.insert(0, str(HERE.parents[1] / "video-production" / "motion-graphics"))
sys.path.insert(0, str(HERE.parents[1] / "video-production" / "color-grade"))
sys.path.insert(0, str(HERE.parents[1] / "video-production" / "music-sound"))

from production_pipeline.build import build  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Script to mastered teaching clip")
    sub = parser.add_subparsers(dest="cmd", required=True)
    run = sub.add_parser("build")
    run.add_argument("lesson", type=Path)
    run.add_argument("--out", type=Path, required=True)
    args = parser.parse_args(argv)
    report = build(args.lesson, args.out)
    print(report["master"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
