#!/usr/bin/env python3
"""Rebuild every committed sample. Run from skills/video-production."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PY = sys.executable


def run(args: list[str]) -> None:
    print("+", " ".join(args), flush=True)
    subprocess.check_call(args, cwd=ROOT)


def main() -> int:
    run([PY, "-m", "unittest",
         "motion-graphics/tests/test_motion.py",
         "color-grade/tests/test_grade.py",
         "music-sound/tests/test_music.py",
         "natural-voice/tests/test_voice.py"])
    spec = ROOT / "motion-graphics" / "sequences" / "sample.json"
    print("+ spec >", spec, flush=True)
    spec.write_text(subprocess.check_output([PY, "motion-graphics/cli.py", "spec"], cwd=ROOT, text=True))
    run([PY, "motion-graphics/cli.py", "render", "--out", "motion-graphics/test-outputs/grid-sequence.mp4"])
    run([PY, "color-grade/cli.py", "demo", "--out", "color-grade/test-outputs"])
    voice = "natural-voice/test-outputs/piper-sample.wav"
    run([PY, "natural-voice/cli.py", "say", "--engine", "piper", "--voice", "lessac",
         "--text", "Price moves in candles. [[pause 0.4]] The figures are illustrative.",
         "--out", voice])
    run([PY, "music-sound/cli.py", "demo", "--out", "music-sound/test-outputs"])
    # A clearer duck: speech, a hole, speech, under a short bed.
    duck_voice = "music-sound/test-outputs/mix/voice-with-gap.wav"
    run([PY, "natural-voice/cli.py", "say", "--engine", "piper", "--voice", "lessac",
         "--text", "Buy orders sit below the price. [[pause 1.4]] Sell orders sit above it.",
         "--out", duck_voice])
    run([PY, "music-sound/cli.py", "bed", "--mood", "calm", "--key", "C", "--scale", "major",
         "--bpm", "72", "--seconds", "14", "--out", "music-sound/test-outputs/mix/bed-14s.wav"])
    run([PY, "music-sound/cli.py", "duck", "--music", "music-sound/test-outputs/mix/bed-14s.wav",
         "--voice", duck_voice, "--out", "music-sound/test-outputs/mix/ducked.wav"])
    run([PY, "demo/build_demo.py", "--out", "demo/test-outputs"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
