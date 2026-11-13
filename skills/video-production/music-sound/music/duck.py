"""Sidechain ducking. The ffmpeg path matches the lesson mix. The numpy path is the tested model."""

from __future__ import annotations

from pathlib import Path

import numpy as np

from lib.ffmpeg_util import ffmpeg_bin, loudnorm_wav, probe, run


def sidechain(
    music: np.ndarray,
    voice: np.ndarray,
    sr: int,
    *,
    threshold: float = 0.02,
    ratio: float = 6.0,
    attack: float = 0.02,
    release: float = 0.32,
) -> np.ndarray:
    """Lower `music` while `voice` is present. Length follows the music."""
    if music.ndim == 1:
        music = music[:, None]
    voice = np.asarray(voice, dtype=np.float32).reshape(-1)
    n = music.shape[0]
    if len(voice) < n:
        voice = np.pad(voice, (0, n - len(voice)))
    voice = voice[:n]
    win = max(1, int(0.012 * sr))
    kernel = np.ones(win, dtype=np.float32) / win
    power = np.convolve(voice.astype(np.float32) ** 2, kernel, mode="same")
    env = np.sqrt(np.maximum(power, 0.0))
    a_a = float(np.exp(-1.0 / max(1.0, attack * sr)))
    a_r = float(np.exp(-1.0 / max(1.0, release * sr)))
    smooth = np.empty(n, dtype=np.float32)
    acc = 0.0
    for i in range(n):
        coef = a_a if env[i] > acc else a_r
        acc = coef * acc + (1.0 - coef) * float(env[i])
        smooth[i] = acc
    gain = np.ones(n, dtype=np.float32)
    hot = smooth > threshold
    gain[hot] = (threshold + (smooth[hot] - threshold) / ratio) / np.maximum(smooth[hot], 1e-6)
    return (music.astype(np.float32) * gain[:, None]).astype(np.float32)


def ffmpeg_duck(music: Path, voice: Path, dest: Path, *, master: bool = True) -> Path:
    """Sidechain-compress the bed under the voice, then loudness-master the sum.

    The voice is padded to the bed so the sidechain releases and the bed
    returns after the last word. Without the pad, the sidechain ends when
    the voice ends and the tail of the bed is cut off.
    """
    dest.parent.mkdir(parents=True, exist_ok=True)
    music_seconds = float(probe(music)["format"]["duration"])
    mixed = dest if not master else dest.with_suffix(".pre-loudnorm.wav")
    run(
        [
            ffmpeg_bin(),
            "-y",
            "-hide_banner",
            "-i",
            str(music),
            "-i",
            str(voice),
            "-filter_complex",
            "[0:a]aresample=48000,aformat=channel_layouts=stereo[mus];"
            f"[1:a]aresample=48000,aformat=channel_layouts=stereo,apad=whole_dur={music_seconds:.3f},asplit=2[vo][key];"
            "[mus][key]sidechaincompress=threshold=0.02:ratio=8:attack=20:release=320:makeup=1[duck];"
            "[vo][duck]amix=inputs=2:duration=longest:normalize=0,alimiter=limit=0.89[a]",
            "-map",
            "[a]",
            "-ar",
            "48000",
            "-ac",
            "2",
            "-c:a",
            "pcm_s16le",
            str(mixed),
        ]
    )
    if master:
        loudnorm_wav(mixed, dest, integrated=-16.0, true_peak=-1.0)
        mixed.unlink(missing_ok=True)
    return dest
