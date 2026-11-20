#!/usr/bin/env python3
"""Chain voice, a music bed, motion graphics, and the clean grade into one clip.

  python3 build_demo.py --out ../demo/test-outputs
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import soundfile as sf

VP = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(VP))
sys.path.insert(0, str(VP / "motion-graphics"))
sys.path.insert(0, str(VP / "natural-voice"))
sys.path.insert(0, str(VP / "color-grade"))
sys.path.insert(0, str(VP / "music-sound"))

from grade.lut import write_looks  # noqa: E402
from grade.pipeline import apply_grade  # noqa: E402
from lib.ffmpeg_util import ebur128, ffmpeg_bin, probe, run  # noqa: E402
from motion.render import render_sequence  # noqa: E402
from music.compose import render_bed  # noqa: E402
from music.duck import ffmpeg_duck  # noqa: E402
from voice.markup import Word, write_vtt  # noqa: E402
from voice.speak import Speaker  # noqa: E402

LEAD = 0.50
TAIL = 1.05
STILL = "programs/defi-program/assets/diagrams/liquidity-ladder.png"

SHOTS = [
    {
        "kind": "title",
        "lines": ["A grid,", "in one picture"],
        "sub": "Illustrative prices. Not a forecast.",
        "caption": "A worked picture. The prices are illustrative.",
        "lower_third": {"kicker": "Worked picture", "line": "Orders, a range, a buffer"},
        "vo": "Here is a grid, drawn as a picture. Nothing here is a forecast. The prices are illustrative. Watch the orders, then the buffer.",
    },
    {
        "kind": "candles",
        "title": "Price, as candles",
        "caption": "Open, high, low, and close. That is the whole candle.",
        "vo": "Each candle shows four facts. The open, the high, the low, and the close. That is the whole candle.",
    },
    {
        "kind": "ladder",
        "title": "Orders on a ladder",
        "caption": "Buys below. Sells above. A cross fills the order.",
        "vo": "Buy orders sit below the price. Sell orders sit above it. When the price crosses a line, that order fills. A fill is not a promise. It is the price touching a level that was already placed.",
    },
    {
        "kind": "risk",
        "title": "Range, and the line past it",
        "caption": "The buffer is the gap between price and the liquidation line.",
        "vo": "The shaded band is the range chosen before the start. The dashed line past it is liquidation. The gap between them is the buffer. When the buffer shrinks, the plan is under stress.",
    },
    {
        "kind": "still",
        "title": "An existing plate, set in motion",
        "caption": "Count the fills. Read the buffer. Keep the picture.",
        "image": STILL,
        "fills": 6,
        "lower_third": {"kicker": "Existing still", "line": "Moved in layers. Not regenerated."},
        "vo": "Count the fills. Read the buffer. Keep those two numbers, and let the rest of the noise go.",
    },
]


def build(out: Path) -> dict:
    out.mkdir(parents=True, exist_ok=True)
    work = out / "_work"
    work.mkdir(exist_ok=True)
    speaker = Speaker(engine="piper", voice="lessac", cache_dir=work / "voice-cache")
    rendered = []
    for shot in SHOTS:
        audio, rate, words, method = speaker.render(shot["vo"])
        rendered.append((shot, audio, rate, words, method))
    sample_rate = rendered[0][2]
    cursor = 0.0
    sequence_shots = []
    pieces = []
    captions: list[Word] = []
    for shot, audio, rate, words, _method in rendered:
        if rate != sample_rate:
            raise RuntimeError("voice sample rate changed between shots")
        spoken = len(audio) / rate
        seconds = round(LEAD + spoken + TAIL, 3)
        visual = {k: v for k, v in shot.items() if k != "vo"}
        visual["seconds"] = seconds
        sequence_shots.append(visual)
        pieces.append(np.zeros(int(LEAD * rate), dtype=np.float32))
        pieces.append(audio.astype(np.float32))
        pieces.append(np.zeros(int(round((seconds - LEAD - spoken) * rate)), dtype=np.float32))
        for word in words:
            captions.append(Word(word.text, word.start + cursor + LEAD, word.end + cursor + LEAD))
        cursor += seconds
    voice = np.concatenate(pieces)
    voice_wav = work / "voice.wav"
    sf.write(str(voice_wav), voice, sample_rate)
    sequence = {"fps": 30, "width": 1920, "height": 1080, "shots": sequence_shots}
    (out / "script.json").write_text(json.dumps({"shots": SHOTS, "lead": LEAD, "tail": TAIL}, indent=2) + "\n")
    picture = work / "picture.mp4"
    print(f"rendering picture, {cursor:.2f}s")
    render_sequence(sequence, picture, crf=16, preset="veryfast")
    bed_audio, bed_rate = render_bed(mood="calm", key="C", scale="major", bpm=72, seconds=cursor + 0.2)
    bed_wav = work / "bed.wav"
    sf.write(str(bed_wav), bed_audio, bed_rate)
    mix = work / "mix.wav"
    print("ducking and mastering")
    ffmpeg_duck(bed_wav, voice_wav, mix)
    luts = VP / "color-grade" / "luts"
    write_looks(luts)
    graded = work / "graded.mp4"
    print("grading")
    # Designed frames are already balanced. The look and the legal-range stage still run.
    # Auto exposure is for camera footage; applying it here would lift a navy field.
    apply_grade(picture, graded, luts / "clean-educational.cube", np.array([1.0, 1.0, 1.0]), 0.0)
    final = out / "grid-picture.mp4"
    run(
        [
            ffmpeg_bin(), "-y", "-hide_banner",
            "-i", str(graded), "-i", str(mix),
            "-map", "0:v:0", "-map", "1:a:0",
            "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
            "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", "-color_range", "tv",
            "-c:a", "aac", "-b:a", "320k", "-ar", "48000", "-ac", "2",
            "-movflags", "+faststart", "-shortest",
            str(final),
        ]
    )
    write_vtt(captions, out / "grid-picture.vtt")
    info = probe(final)
    meter = ebur128(final)
    report = {
        "file": str(final),
        "duration": float(info["format"]["duration"]),
        "loudness": meter,
        "streams": info["streams"],
        "alignment": rendered[0][4],
    }
    (out / "demo-report.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"duration": report["duration"], "lufs": meter["integrated_lufs"]}, indent=2))
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    build(args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
