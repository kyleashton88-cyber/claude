#!/usr/bin/env python3
"""Blur a screen still and fail if sensitive text is still readable."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from screen_demo.blur import blur_image, qa_image  # noqa: E402


def _box(value: str) -> tuple[int, int, int, int]:
    parts = [int(part) for part in value.split(",")]
    if len(parts) != 4:
        raise argparse.ArgumentTypeError("box is x,y,w,h")
    return parts[0], parts[1], parts[2], parts[3]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Screen-demo blur and QA")
    sub = parser.add_subparsers(dest="cmd", required=True)
    blur = sub.add_parser("blur")
    blur.add_argument("--image", type=Path, required=True)
    blur.add_argument("--out", type=Path, required=True)
    blur.add_argument("--box", type=_box, action="append", default=[])
    check = sub.add_parser("qa")
    check.add_argument("--image", type=Path, required=True)
    args = parser.parse_args(argv)
    if "course" in Path(getattr(args, "out", args.image)).resolve().parts:
        print("refusing to write into course/", file=sys.stderr)
        return 2
    if args.cmd == "blur":
        hits = blur_image(args.image, args.out, args.box)
        print(f"blurred {len(hits)} detected regions into {args.out}")
        return 0
    problems = qa_image(args.image)
    if problems:
        print("FAIL")
        for item in problems:
            print("-", item)
        return 1
    print("PASS", args.image)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
