#!/usr/bin/env python3
"""In-house narration. Kokoro or Piper. No paid speech API.

  python3 cli.py say --engine kokoro --mood calm-teacher --text "A grid." --out out.wav
  python3 cli.py samples --out test-outputs/moods
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from voice.moods import MOODS  # noqa: E402
from voice.speak import Speaker, render_to_file  # noqa: E402

SCRIPT = """A grid places buy orders below the price and sell orders above it. When price crosses a line, that order fills.

The range is the band chosen before the start. Past that band, the grid has left its plan.

A liquidation line sits beyond the range. The gap is the *buffer*. If the buffer shrinks, the plan is under stress. <pause 400ms>

Count the fills. Read the buffer. Keep the picture."""


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Kokoro or Piper narration")
    sub = parser.add_subparsers(dest="cmd", required=True)
    say = sub.add_parser("say")
    say.add_argument("--engine", choices=("kokoro", "piper"), default="kokoro")
    say.add_argument("--mood", choices=tuple(MOODS), default="calm-teacher")
    say.add_argument("--text", required=True)
    say.add_argument("--out", type=Path, required=True)
    samples = sub.add_parser("samples")
    samples.add_argument("--out", type=Path, required=True)
    args = parser.parse_args(argv)
    if args.cmd == "say":
        speaker = Speaker(engine=args.engine, mood=args.mood)
        print(json.dumps(render_to_file(args.text, args.out, speaker), indent=2))
        return 0
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "script.txt").write_text(SCRIPT + "\n")
    report = []
    for engine in ("piper", "kokoro"):
        for name in MOODS:
            dest = args.out / f"{engine}-{name}.wav"
            print(f"rendering {dest.name}", flush=True)
            speaker = Speaker(engine=engine, mood=name)
            info = render_to_file(SCRIPT, dest, speaker)
            report.append({"file": dest.name, **info, "mood": name, "engine": engine})
    (args.out / "index.json").write_text(json.dumps(report, indent=2) + "\n")
    print(f"wrote {len(report)} takes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
