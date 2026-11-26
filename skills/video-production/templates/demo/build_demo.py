#!/usr/bin/env python3
"""Thumbnail, end card, description, and a vertical cut. No image API."""

from __future__ import annotations

import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
VP = HERE.parent
sys.path.insert(0, str(HERE))

from cli import main  # noqa: E402

sys.path.insert(0, str(VP / "quality-gate"))
from gate.synth import encode_clip, write_pass_captions  # noqa: E402


def main_demo() -> None:
    os.chdir(HERE)
    out = Path("test-outputs")
    out.mkdir(parents=True, exist_ok=True)
    wide = encode_clip(
        out / "wide-master.mp4",
        width=640,
        height=360,
        seconds=4,
        fps=30,
        disclaimer=True,
        moving=True,
        loudnorm=False,
    )
    chapters = out / "chapters.txt"
    chapters.write_text("0:00 Open\n0:02 The idea\n", encoding="utf-8")
    vtt = write_pass_captions(out / "wide-master.vtt", end=3.5)
    code = main(
        [
            "short",
            "--master",
            str(wide),
            "--chapters",
            str(chapters),
            "--vtt",
            str(vtt),
            "--chapter",
            "The idea",
            "--out",
            str(out / "short.mp4"),
        ]
    )
    if code != 0:
        raise SystemExit(code)
    if main(["thumbnail", "--title", "A grid in one picture", "--label", "Four facts", "--engine", "pil", "--out", str(out / "thumbnail.png")]) != 0:
        raise SystemExit(1)
    if main(["endcard", "--title", "A grid in one picture", "--next", "Where the range sits", "--out", str(out / "endcard.png")]) != 0:
        raise SystemExit(1)
    if main(["chapters", "--lesson", "formats/blueprint-lesson.yaml", "--out", str(out / "description.txt")]) != 0:
        raise SystemExit(1)


if __name__ == "__main__":
    main_demo()
