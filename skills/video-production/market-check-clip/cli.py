#!/usr/bin/env python3
"""Build a Market Check master and a vertical cut. Does not post."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path.insert(0, str(HERE))

from market_check.build_lesson import estimate_seconds, lesson_from_post, write_lesson  # noqa: E402


def refuse_course(path: Path) -> None:
    if "course" in path.resolve().parts:
        raise SystemExit(f"refusing to write into course/: {path}")


def main(argv: list[str] | None = None) -> int:
    import argparse
    parser = argparse.ArgumentParser(description="Market Check video from a post file")
    sub = parser.add_subparsers(dest="cmd", required=True)
    build = sub.add_parser("build")
    build.add_argument("post", type=Path)
    build.add_argument("--out", type=Path, required=True)
    vertical = sub.add_parser("vertical")
    vertical.add_argument("--master", type=Path, required=True)
    vertical.add_argument("--chapters", type=Path, required=True)
    vertical.add_argument("--vtt", type=Path, required=True)
    vertical.add_argument("--out", type=Path, required=True)
    args = parser.parse_args(argv)
    if args.cmd == "vertical":
        refuse_course(args.out)
        templates = REPO / "skills" / "video-production" / "templates" / "cli.py"
        proc = subprocess.run(
            [
                sys.executable, str(templates), "short",
                "--master", str(args.master),
                "--chapters", str(args.chapters),
                "--vtt", str(args.vtt),
                "--out", str(args.out),
            ],
            capture_output=True,
            text=True,
        )
        print(proc.stdout or proc.stderr)
        return proc.returncode
    refuse_course(args.out)
    out = args.out.resolve()
    lesson_path = out / "lesson.yaml"
    data = write_lesson(args.post, lesson_path)
    seconds = estimate_seconds([section["narration"] for section in data["sections"]])
    print(f"estimated {seconds:.1f}s")
    pipeline = REPO / "skills" / "production-pipeline"
    proc = subprocess.run(
        [sys.executable, "-m", "production_pipeline", "build", str(lesson_path), "--out", str(out)],
        cwd=str(pipeline),
    )
    return proc.returncode


if __name__ == "__main__":
    raise SystemExit(main())
