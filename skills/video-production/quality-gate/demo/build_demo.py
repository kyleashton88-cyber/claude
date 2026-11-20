#!/usr/bin/env python3
"""Write a short master and its gate report. Synthetic picture, no paid API."""

from __future__ import annotations

import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))

from gate.profiles import PROFILES, length_ok  # noqa: E402
from gate.synth import encode_clip, write_pass_captions  # noqa: E402


def main() -> None:
    os.chdir(HERE)
    out = Path("test-outputs")
    out.mkdir(parents=True, exist_ok=True)
    master = encode_clip(
        out / "short-master.mp4",
        width=1080,
        height=1920,
        seconds=6,
        fps=30,
        disclaimer=True,
        moving=True,
        loudnorm=True,
    )
    captions = write_pass_captions(out / "short-master.vtt", end=5.4)
    from cli import main as cli_main

    code = cli_main(["check", str(master), "--format", "short", "--captions", str(captions), "--out", str(out / "pass")])
    twelve = 12 * 60
    note = out / "blueprint-length.md"
    note.write_text(
        "\n".join(
            [
                "# Blueprint length",
                "",
                f"12:00 ({twelve}s) is inside the Blueprint window "
                f"({PROFILES['blueprint'].min_seconds:.0f}s–{PROFILES['blueprint'].max_seconds:.0f}s): "
                f"{length_ok(twelve, PROFILES['blueprint'])}.",
                "",
                "The window is 10 to 15 minutes. A 6:15 cut is short of that window.",
                "The files that still apply an older floor are listed in SUPERSEDES.md. This gate does not.",
                "",
            ]
        ),
        encoding="utf-8",
    )
    if code != 0:
        raise SystemExit(code)


if __name__ == "__main__":
    main()
