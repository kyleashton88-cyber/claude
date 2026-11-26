#!/usr/bin/env python3
"""Color grade CLI.

  python3 cli.py luts --out luts
  python3 cli.py grade --in clip.mp4 --look clean-educational --out graded.mp4
  python3 cli.py demo --out test-outputs
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from grade.card import write_card  # noqa: E402
from grade.lut import LOOKS, write_looks  # noqa: E402
from grade.pipeline import (  # noqa: E402
    apply_grade,
    exposure_ev,
    match_to,
    sample_frames,
    signal_range,
    white_balance,
    write_scopes,
    write_split,
)
from lib.brand import H, W  # noqa: E402
from lib.ffmpeg_util import ffmpeg_bin, run  # noqa: E402


HERE = Path(__file__).resolve().parent
DEFAULT_LUTS = HERE / "luts"


def _variant(dest: Path) -> None:
    """A second ungraded card, cool and bright, used for the match test."""
    import subprocess

    import numpy as np
    from PIL import Image

    from grade.card import paint_card

    frames_n = 60
    cmd = [
        ffmpeg_bin(), "-y", "-hide_banner", "-loglevel", "error",
        "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", "30", "-i", "-",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p",
        "-color_range", "pc", "-movflags", "+faststart", "-an", str(dest),
    ]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    assert proc.stdin is not None
    for i in range(frames_n):
        base = np.asarray(paint_card(i / 30)).astype(np.float32)
        # paint_card already applied a warm-dark fault. Undo it, then apply a cool-bright fault.
        base = base / np.array([1.18, 0.90, 0.68]) / 0.62
        base *= np.array([0.82, 0.95, 1.20])
        base *= 1.35
        proc.stdin.write(np.clip(base, 0, 255).astype(np.uint8).tobytes())
    proc.stdin.close()
    err = proc.stderr.read().decode() if proc.stderr else ""
    if proc.wait() != 0:
        raise RuntimeError(err[-1500:])


def grade_one(src: Path, look: str, dest: Path, luts: Path, *, match: Path | None = None) -> dict:
    if look not in LOOKS:
        raise SystemExit(f"unknown look {look}. choices: {', '.join(LOOKS)}")
    lut = luts / f"{look}.cube"
    if not lut.is_file():
        write_looks(luts)
    frames = sample_frames(src)
    if match:
        gains, ev = match_to(frames, sample_frames(match))
        mode = "match"
    else:
        gains, ev = white_balance(frames), exposure_ev(frames)
        mode = "auto"
    apply_grade(src, dest, lut, gains, ev)
    return {
        "look": look,
        "mode": mode,
        "gains_rgb": [round(float(v), 4) for v in gains],
        "exposure_ev": round(float(ev), 4),
        "legal": {k: round(v, 2) for k, v in signal_range(dest).items()},
        "output": str(dest),
    }


def demo(out: Path) -> None:
    out.mkdir(parents=True, exist_ok=True)
    luts = DEFAULT_LUTS
    write_looks(luts)
    before = out / "ungraded.mp4"
    write_card(before)
    write_scopes(before, out / "scope-before-waveform.png", out / "scope-before-vectorscope.png")
    reports = []
    clean = out / "graded-clean-educational.mp4"
    for look in LOOKS:
        graded = out / f"graded-{look}.mp4"
        reports.append(grade_one(before, look, graded, luts))
        write_split(before, graded, out / f"split-{look}.mp4", look)
    write_scopes(clean, out / "scope-clean-waveform.png", out / "scope-clean-vectorscope.png")
    variant = out / "ungraded-cool.mp4"
    _variant(variant)
    matched = out / "matched-to-clean.mp4"
    reports.append(grade_one(variant, "clean-educational", matched, luts, match=clean))
    (out / "grade-report.json").write_text(json.dumps(reports, indent=2) + "\n")
    print(json.dumps(reports, indent=2))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="House color grade")
    sub = parser.add_subparsers(dest="cmd", required=True)
    luts = sub.add_parser("luts")
    luts.add_argument("--out", type=Path, default=DEFAULT_LUTS)
    luts.add_argument("--size", type=int, default=33)
    grade = sub.add_parser("grade")
    grade.add_argument("--in", dest="src", type=Path, required=True)
    grade.add_argument("--look", required=True)
    grade.add_argument("--out", type=Path, required=True)
    grade.add_argument("--luts", type=Path, default=DEFAULT_LUTS)
    grade.add_argument("--match", type=Path)
    sub.add_parser("demo").add_argument("--out", type=Path, required=True)
    args = parser.parse_args(argv)
    if args.cmd == "luts":
        for path in write_looks(args.out, args.size):
            print(path)
        return 0
    if args.cmd == "grade":
        print(json.dumps(grade_one(args.src, args.look, args.out, args.luts, match=args.match), indent=2))
        return 0
    demo(args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
