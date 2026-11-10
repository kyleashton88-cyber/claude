"""Music bed, ducking, and loudness. The bed file is CC0."""

from __future__ import annotations

import subprocess
from pathlib import Path

import numpy as np
import soundfile as sf

ROOT = Path(__file__).resolve().parents[3]
MUSIC = ROOT / "course" / "music" / "komiku-ambiant-obscur-technology.ogg"


def run(cmd: list[str]) -> None:
    subprocess.check_call(cmd)


def build_bed(duration: float, lifts: list[tuple[float, float]], dest: Path) -> None:
    """Body gain 0.50 (about −26 LUFS from the −20 bed). Lifts are ident and outro."""
    raw = dest.parent / "music-src.wav"
    if not raw.is_file():
        run(["ffmpeg", "-y", "-v", "error", "-i", str(MUSIC), "-ac", "2", "-ar", "48000", str(raw)])
    music, sr = sf.read(str(raw), always_2d=True)
    if sr != 48000:
        raise SystemExit(f"unexpected music rate {sr}")
    need = int(duration * 48000) + 4800
    reps = int(np.ceil(need / len(music))) + 1
    loop = np.vstack([music] * reps)[:need]
    env = np.full(len(loop), 0.50, dtype=np.float32)
    ramp = int(0.35 * 48000)
    for start, end in lifts:
        a = int(start * 48000)
        b = min(len(env), int(end * 48000))
        if b <= a:
            continue
        env[a:b] = 1.29
        left = max(0, a - ramp)
        if a > left:
            env[left:a] = np.linspace(env[left], 1.29, a - left, dtype=np.float32)
        right = min(len(env), b + ramp)
        if right > b:
            env[b:right] = np.linspace(1.29, 0.50, right - b, dtype=np.float32)
    sf.write(str(dest), loop * env[:, None], 48000)


def mix(video: Path, voice: Path, bed: Path, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    run([
        "ffmpeg", "-y", "-v", "error",
        "-i", str(video), "-i", str(voice), "-i", str(bed),
        "-filter_complex",
        "[1:a]aresample=48000,aformat=channel_layouts=stereo,asplit=2[vo][key];"
        "[2:a]aresample=48000,aformat=channel_layouts=stereo[mus];"
        "[mus][key]sidechaincompress=threshold=0.02:ratio=8:attack=30:release=400:makeup=1[duck];"
        "[vo][duck]amix=inputs=2:duration=first:normalize=0,"
        "alimiter=limit=0.89,loudnorm=I=-16:TP=-1.5:LRA=11:linear=true[a]",
        "-map", "0:v", "-map", "[a]",
        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
        str(dest),
    ])
