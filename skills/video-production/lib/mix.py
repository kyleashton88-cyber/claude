"""One mix for every teaching video.

Voice is mastered to -14 LUFS integrated and -1 dBTP.
The bed is mastered to that same loudness, then lowered 20 dB so it sits
under the voice, then sidechain-ducked while the voice is present.
The sum is only peak-limited. It is not loudness-normalised again, because
a second pass would lift the bed back up.

Four values this replaces:
1. Voice master at -16 LUFS (`natural-voice` `render_to_file`).
2. Music bed master at -16 LUFS (`music-sound` CLI).
3. Ducked-mix master at -16 LUFS (`ffmpeg_duck`).
4. The lesson renderer's -1.5 dBTP ceiling and a fixed music volume of 0.22
   (`course/skills/motion_picture/audio.py`, not edited here).
"""

from __future__ import annotations

from pathlib import Path

import numpy as np

from lib.ffmpeg_util import ffmpeg_bin, loudnorm_wav, probe, run

VOICE_LUFS = -14.0
TRUE_PEAK_DBTP = -1.0
BED_UNDER_VOICE_DB = -20.0


def duck_under_voice(music: Path, voice: Path, dest: Path) -> Path:
    """Place `music` about 20 dB under `voice`, then duck it while the voice speaks."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    work = dest.parent / "_duck"
    work.mkdir(parents=True, exist_ok=True)
    voice_m = work / "voice.wav"
    bed_m = work / "bed.wav"
    loudnorm_wav(voice, voice_m, integrated=VOICE_LUFS, true_peak=TRUE_PEAK_DBTP)
    loudnorm_wav(music, bed_m, integrated=VOICE_LUFS, true_peak=TRUE_PEAK_DBTP)
    seconds = float(probe(bed_m)["format"]["duration"])
    limit = 10 ** (TRUE_PEAK_DBTP / 20.0)
    run(
        [
            ffmpeg_bin(), "-y", "-hide_banner",
            "-i", str(bed_m), "-i", str(voice_m),
            "-filter_complex",
            f"[0:a]volume={BED_UNDER_VOICE_DB}dB,aresample=48000,aformat=channel_layouts=stereo[mus];"
            f"[1:a]aresample=48000,aformat=channel_layouts=stereo,apad=whole_dur={seconds:.3f},asplit=2[vo][key];"
            "[mus][key]sidechaincompress=threshold=0.015:ratio=10:attack=20:release=320:makeup=1[duck];"
            f"[vo][duck]amix=inputs=2:duration=longest:normalize=0,alimiter=limit={limit:.5f}[a]",
            "-map", "[a]",
            "-ar", "48000", "-ac", "2", "-c:a", "pcm_s16le",
            str(dest),
        ]
    )
    return dest


def sidechain_gain(
    music: np.ndarray,
    voice: np.ndarray,
    sr: int,
    *,
    threshold: float = 0.02,
    ratio: float = 10.0,
    attack: float = 0.02,
    release: float = 0.32,
) -> np.ndarray:
    """The gain law the ffmpeg sidechain is aimed at. Used by the unit test."""
    if music.ndim == 1:
        music = music[:, None]
    voice = np.asarray(voice, dtype=np.float32).reshape(-1)
    n = music.shape[0]
    if len(voice) < n:
        voice = np.pad(voice, (0, n - len(voice)))
    voice = voice[:n]
    win = max(1, int(0.012 * sr))
    power = np.convolve(voice.astype(np.float32) ** 2, np.ones(win, dtype=np.float32) / win, mode="same")
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
