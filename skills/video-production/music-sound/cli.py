#!/usr/bin/env python3
"""Music and sound-design CLI.

  python3 cli.py bed --mood calm --key C --scale major --bpm 72 --seconds 60 --out bed.wav
  python3 cli.py sfx --out test-outputs/sfx
  python3 cli.py duck --music bed.wav --voice voice.wav --out mix.wav
  python3 cli.py demo --out test-outputs
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import soundfile as sf

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib.ffmpeg_util import ebur128, master_audio  # noqa: E402
from music.compose import render_bed  # noqa: E402
from music.duck import ffmpeg_duck  # noqa: E402
from music.sfx import EFFECTS, render_effect  # noqa: E402


def _write(path: Path, audio: np.ndarray, sr: int) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = path.with_suffix(".raw.wav")
    sf.write(str(raw), audio, sr, subtype="PCM_16")
    master_audio(raw, path)
    raw.unlink(missing_ok=True)
    return path


def demo(out: Path, voice: Path | None) -> None:
    out.mkdir(parents=True, exist_ok=True)
    beds = [
        ("calm", "C", "major", 72),
        ("focused", "A", "minor", 84),
        ("hopeful", "F", "major", 76),
    ]
    written = []
    for mood, key, scale, bpm in beds:
        audio, sr = render_bed(mood=mood, key=key, scale=scale, bpm=bpm, seconds=60)
        dest = out / "beds" / f"{mood}-{key}-{scale}-{bpm}bpm.wav"
        _write(dest, audio, sr)
        meter = ebur128(dest)
        written.append({"file": str(dest), **{k: round(v, 2) if isinstance(v, float) else v for k, v in meter.items()}})
        print(f"bed {dest.name}  {meter['integrated_lufs']:.2f} LUFS")
    sfx_dir = out / "sfx"
    for name in EFFECTS:
        audio, sr = render_effect(name)
        dest = sfx_dir / f"{name}.wav"
        _write(dest, audio, sr)
        print(f"sfx {dest.name}")
    note = {"standard": "voice -14 LUFS, bed -20 dB under the voice, true peak -1 dBTP"}
    if voice and voice.is_file():
        bed = out / "beds" / "calm-C-major-72bpm.wav"
        mix = out / "mix" / "ducked.wav"
        ffmpeg_duck(bed, voice, mix)
        meter = ebur128(mix)
        note["duck"] = {"file": str(mix), "integrated_lufs": round(meter["integrated_lufs"], 2), "true_peak_dbfs": meter["true_peak_dbfs"]}
        print(f"mix {mix.name}  {meter['integrated_lufs']:.2f} LUFS")
    else:
        note["duck"] = "skipped, no voice file yet"
    (out / "music-report.json").write_text(json.dumps({"beds": written, **note}, indent=2) + "\n")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Original music beds and effects")
    sub = parser.add_subparsers(dest="cmd", required=True)
    bed = sub.add_parser("bed")
    bed.add_argument("--mood", default="calm")
    bed.add_argument("--key", default="C")
    bed.add_argument("--scale", default="major")
    bed.add_argument("--bpm", type=float, default=72)
    bed.add_argument("--seconds", type=float, default=60)
    bed.add_argument("--out", type=Path, required=True)
    sfx = sub.add_parser("sfx")
    sfx.add_argument("--name", default="all")
    sfx.add_argument("--out", type=Path, required=True)
    duck = sub.add_parser("duck")
    duck.add_argument("--music", type=Path, required=True)
    duck.add_argument("--voice", type=Path, required=True)
    duck.add_argument("--out", type=Path, required=True)
    show = sub.add_parser("demo")
    show.add_argument("--out", type=Path, required=True)
    show.add_argument("--voice", type=Path)
    args = parser.parse_args(argv)
    if args.cmd == "bed":
        audio, sr = render_bed(mood=args.mood, key=args.key, scale=args.scale, bpm=args.bpm, seconds=args.seconds)
        _write(args.out, audio, sr)
        print(args.out)
        return 0
    if args.cmd == "sfx":
        names = EFFECTS if args.name == "all" else (args.name,)
        args.out.mkdir(parents=True, exist_ok=True)
        for name in names:
            audio, sr = render_effect(name)
            dest = args.out / f"{name}.wav" if args.out.suffix != ".wav" else args.out
            _write(dest, audio, sr)
            print(dest)
        return 0
    if args.cmd == "duck":
        ffmpeg_duck(args.music, args.voice, args.out)
        print(args.out)
        return 0
    demo(args.out, args.voice)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
