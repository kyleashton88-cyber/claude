#!/usr/bin/env python3
"""Motion graphics CLI.

Examples
  python3 cli.py render --out test-outputs/grid-sequence.mp4
  python3 cli.py render --spec my-sequence.json --out out.mp4
  python3 cli.py frame --at 12.5 --out frame.png
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from motion.render import load_sequence, render_frame, render_sequence, sample_sequence, shot_duration  # noqa: E402
from motion.frame import background  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Code-drawn teaching motion graphics")
    sub = parser.add_subparsers(dest="cmd", required=True)

    render = sub.add_parser("render", help="Render a sequence to H.264")
    render.add_argument("--spec", type=Path, help="Sequence JSON. Default is the built-in sample.")
    render.add_argument("--out", type=Path, required=True)
    render.add_argument("--crf", type=int, default=18)
    render.add_argument("--preset", default="medium")

    frame = sub.add_parser("frame", help="Write one PNG frame")
    frame.add_argument("--spec", type=Path)
    frame.add_argument("--at", type=float, required=True)
    frame.add_argument("--out", type=Path, required=True)

    show = sub.add_parser("spec", help="Print the built-in sample sequence")

    args = parser.parse_args(argv)
    if args.cmd == "spec":
        print(json.dumps(sample_sequence(), indent=2))
        return 0
    sequence = load_sequence(args.spec) if args.spec else sample_sequence()
    if args.cmd == "frame":
        im = render_frame(sequence, args.at, background())
        args.out.parent.mkdir(parents=True, exist_ok=True)
        im.save(args.out)
        print(f"wrote {args.out} at t={args.at:.2f}s of {shot_duration(sequence):.2f}s")
        return 0
    render_sequence(sequence, args.out, crf=args.crf, preset=args.preset)
    print(f"wrote {args.out}  {shot_duration(sequence):.2f}s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
