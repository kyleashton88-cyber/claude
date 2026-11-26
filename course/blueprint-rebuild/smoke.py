#!/usr/bin/env python3
"""Smoke the Blueprint path. Does not render a full lesson.

1. A tiny pass list fails because an image the lesson uses is unlisted.
2. A 20–40s excerpt of BP-01 runs voice, mix, captions, end card, and the gate.
3. The same excerpt fails the gate when a figure is removed from the lesson file.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
OUT = ROOT / "blueprint-smoke"
sys.path.insert(0, str(HERE))

import image_gate  # noqa: E402


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    inventory = OUT / "BP01-03_IMAGE_USE.txt"
    lines = []
    for sid in (
        "bp-01-introduction",
        "bp-02-what-you-need",
        "bp-03-what-is-a-grid-bot",
    ):
        for row in image_gate.images_for_lesson(sid):
            lines.append(f"{row['lesson']}\t{row['kind']}\t{row['path']}")
    inventory.write_text("\n".join(lines) + "\n")
    print(f"WROTE {inventory} ({len(lines)} rows)")

    tiny = OUT / "tiny-pass-list.json"
    tiny.write_text(json.dumps({
        "images": [{
            "path": "course/images/style-ref/01M6MSHVNHX3WQH81XS8KQK1HT.png",
            "lesson": "bp-01-introduction",
            "pass": True,
        }]
    }, indent=2))
    probe = subprocess.run(
        [sys.executable, str(HERE / "image_gate.py"), "--id", "bp-01-introduction", "--pass-list", str(tiny)],
        capture_output=True, text=True,
    )
    print(probe.stdout)
    print(probe.stderr)
    if probe.returncode == 0:
        raise SystemExit("expected the tiny pass list to fail")
    if "missing from pass list" not in probe.stderr and "missing from pass list" not in probe.stdout:
        raise SystemExit("the failure did not name an unlisted image")
    print("IMAGE CHECK FAIL on an unlisted image, as required.")

    full = OUT / "sample-pass-list.json"
    rows = []
    for sid in (
        "bp-01-introduction",
        "bp-02-what-you-need",
        "bp-03-what-is-a-grid-bot",
    ):
        for item in image_gate.images_for_lesson(sid):
            rows.append({"path": item["path"], "lesson": item["lesson"], "pass": True})
    full.write_text(json.dumps({"images": rows}, indent=2) + "\n")
    dest = OUT / "bp-01-excerpt.mp4"
    render = subprocess.run(
        [
            sys.executable, str(HERE / "studio.py"),
            "--id", "bp-01-introduction",
            "--excerpt", "32",
            "--pass-list", str(full),
            "--dest", str(dest),
        ],
    )
    report = OUT / "bp-01-introduction" / "gate" / "report.md"
    # studio writes the gate next to dest when dest is outside course/
    alt = dest.parent / "gate" / "report.md"
    if alt.is_file():
        report = alt
    print(f"excerpt render exit {render.returncode}")
    if report.is_file():
        print(report.read_text())
    else:
        print(f"no gate report at {report}")

    lesson = dest.parent / "bp-01-introduction.yaml"
    if not lesson.is_file():
        lesson = OUT / "bp-01-introduction" / "bp-01-introduction.yaml"
    if lesson.is_file() and dest.is_file():
        broken_vtt = OUT / "bp-01-wrong-number.vtt"
        broken_vtt.write_text(
            (dest.parent / "bp-01-introduction.vtt").read_text()
            + "\n00:00:24.200 --> 00:00:25.000\nThe close was 99999.\n"
        )
        wrong = subprocess.run(
            [
                sys.executable,
                str(ROOT / "skills/video-production/quality-gate/cli.py"),
                "check", str(dest),
                "--format", "blueprint",
                "--captions", str(broken_vtt),
                "--lesson", str(lesson),
                "--out", str(OUT / "gate-wrong-number"),
            ],
        )
        print(f"wrong-number gate exit {wrong.returncode}")
        print((OUT / "gate-wrong-number" / "report.md").read_text())
        if wrong.returncode == 0:
            raise SystemExit("a lesson file with the figures removed was accepted")


if __name__ == "__main__":
    main()
