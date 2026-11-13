#!/usr/bin/env python3
"""Render a Blueprint lesson as a moving picture. Refuses Elite ids.

  python3 course/blueprint-rework/render_motion.py --id bp-01-introduction
  python3 course/blueprint-rework/render_motion.py --id bp-01-introduction --proof
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

import numpy as np
import soundfile as sf

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "course/skills"))

import importlib.util


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


lesson_scripts = _load("lesson_scripts", ROOT / "course/blueprint-rework/lesson_scripts.py")
draw = _load("draw", ROOT / "course/skills/motion_picture/draw.py")
audio = _load("audio", ROOT / "course/skills/motion_picture/audio.py")
speech = _load("speech", ROOT / "course/skills/motion_picture/speech.py")
SR = speech.SR
choose_speed = speech.choose_speed
synth = speech.synth
build_bed = audio.build_bed
mix = audio.mix

OUT = ROOT / "course" / "masters-v2"
CHANGELOG = ROOT / "course/blueprint-rework/CHANGELOG.md"
BANNED = ("bybit", "binance", "pionex", "coinbase", "okx", "kucoin", "kraken", "market pros")


def run(cmd: list[str]) -> None:
    subprocess.check_call(cmd)


def guard(text: str) -> None:
    low = text.lower()
    for word in BANNED:
        if word in low:
            raise SystemExit(f"brand in lesson text: {word}")


def fit_wav(wav: np.ndarray, frames: int) -> np.ndarray:
    target = int(frames / draw.FPS * SR)
    if len(wav) < target:
        wav = np.concatenate([wav, np.zeros(target - len(wav), dtype=np.float32)])
    return wav[:target]


def render(sid: str, proof: bool, out_dir: Path | None = None, prepare_shots=None) -> Path:
    if sid.startswith("el-"):
        raise SystemExit(f"refusing Elite id {sid}")
    shots = lesson_scripts.build(sid)
    if prepare_shots is not None:
        shots = prepare_shots(shots)
    if proof:
        shots = shots[:4]
    for shot in shots:
        guard(shot["vo"])
        guard(shot.get("caption") or "")
    words = sum(len(shot["vo"].split()) for shot in shots)
    speed = 1.05 if proof else choose_speed(words)
    print(f"{sid} shots {len(shots)} words {words} speed {speed:.2f}", flush=True)
    from kokoro import KPipeline
    pipe = KPipeline(lang_code="a", repo_id="hexgrad/Kokoro-82M")
    work = Path(f"/tmp/bp-motion/{sid}")
    if work.exists():
        for child in work.iterdir():
            if child.is_file():
                child.unlink()
    work.mkdir(parents=True, exist_ok=True)
    lesson_scripts.attach_series(shots)
    pieces = []
    clock = 0.0
    lifts = []
    for i, shot in enumerate(shots):
        wav = synth(pipe, shot["vo"], speed)
        min_sec = 0.0
        if shot["kind"] == "ident":
            min_sec = 6.5
        elif shot["kind"] == "outro" and i == len(shots) - 1:
            min_sec = len(wav) / SR + 1.5
        if min_sec and len(wav) < int(min_sec * SR):
            wav = np.concatenate([wav, np.zeros(int(min_sec * SR) - len(wav), dtype=np.float32)])
        frames = max(draw.FPS, int(round(len(wav) / SR * draw.FPS)))
        wav = fit_wav(wav, frames)
        shot["duration"] = frames / draw.FPS
        shot["frames"] = frames
        if shot["kind"] in {"ident", "outro"}:
            lifts.append((clock, clock + shot["duration"]))
        clock += shot["duration"]
        pieces.append(wav)
        if (i + 1) % 8 == 0:
            print(f"  voice {i + 1}/{len(shots)} t={clock:.0f}s", flush=True)
    voice = np.concatenate(pieces)
    voice_path = work / "voice.wav"
    sf.write(str(voice_path), voice, SR)
    silent = work / "silent.mp4"
    proc = subprocess.Popen(
        [
            "ffmpeg", "-y", "-v", "error",
            "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "1920x1080", "-r", str(draw.FPS),
            "-i", "-",
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", "-pix_fmt", "yuv420p",
            "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
            str(silent),
        ],
        stdin=subprocess.PIPE,
    )
    total_frames = sum(shot["frames"] for shot in shots)
    drawn = 0
    lesson_t = 0.0
    total_t = clock
    assert proc.stdin is not None
    for shot in shots:
        for n in range(shot["frames"]):
            local = n / draw.FPS
            frame = draw.paint(shot, local, lesson_t / total_t)
            proc.stdin.write(frame.tobytes())
            lesson_t += 1 / draw.FPS
            drawn += 1
            if drawn % (draw.FPS * 30) == 0:
                print(f"  frames {drawn}/{total_frames}", flush=True)
    proc.stdin.close()
    code = proc.wait()
    if code != 0:
        raise SystemExit(f"ffmpeg encode failed {code}")
    dest = (out_dir or OUT) / f"{sid}.mp4"
    if proof:
        dest = Path("/tmp/bp-motion-proof.mp4")
        # Proof keeps the picture and the voice so a frame can be checked.
    bed = work / "bed.wav"
    build_bed(clock, lifts, bed)
    mix(silent, voice_path, bed, dest)
    print(f"WROTE {dest} {clock:.1f}s words {words}", flush=True)
    # Duration is not judged here. The only rule is quality-gate profiles.py,
    # so a 6:15 Blueprint master is not rejected after a successful render.
    print(
        f"Length {clock:.1f}s is recorded, not failed. "
        "Judge it with skills/video-production/quality-gate --format blueprint.",
        flush=True,
    )
    return dest


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--id", required=True)
    ap.add_argument("--proof", action="store_true")
    args = ap.parse_args()
    render(args.id, args.proof)


if __name__ == "__main__":
    main()
