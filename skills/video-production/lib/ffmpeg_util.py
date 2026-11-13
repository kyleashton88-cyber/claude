"""ffmpeg runners shared by grade, music, voice, and the demo."""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path


class FFmpegError(RuntimeError):
    pass


def ffmpeg_bin() -> str:
    found = shutil.which("ffmpeg")
    if not found:
        raise FFmpegError("ffmpeg is not on PATH")
    return found


def ffprobe_bin() -> str:
    found = shutil.which("ffprobe")
    if not found:
        raise FFmpegError("ffprobe is not on PATH")
    return found


def run(args: list[str], *, timeout: float | None = None) -> subprocess.CompletedProcess:
    proc = subprocess.run(
        args,
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    if proc.returncode != 0:
        tail = (proc.stderr or proc.stdout or "")[-4000:]
        raise FFmpegError(f"command failed ({proc.returncode}): {' '.join(args[:6])}\n{tail}")
    return proc


def probe(path: Path) -> dict:
    proc = run(
        [
            ffprobe_bin(),
            "-v",
            "error",
            "-show_entries",
            "format=duration,bit_rate:stream=index,codec_type,codec_name,width,height,avg_frame_rate,bit_rate,sample_rate,channels",
            "-of",
            "json",
            str(path),
        ]
    )
    return json.loads(proc.stdout)


def ebur128(path: Path) -> dict:
    """Integrated loudness and true peak from the ebur128 filter."""
    proc = subprocess.run(
        [
            ffmpeg_bin(),
            "-hide_banner",
            "-i",
            str(path),
            "-af",
            "ebur128=peak=true",
            "-f",
            "null",
            "-",
        ],
        capture_output=True,
        text=True,
    )
    text = proc.stderr or ""
    integrated = true_peak = None
    for line in text.splitlines():
        if "I:" in line and "LUFS" in line and "Threshold" not in line:
            try:
                integrated = float(line.split("I:")[1].split("LUFS")[0].strip())
            except ValueError:
                pass
        if "Peak:" in line and "dBFS" in line:
            try:
                true_peak = float(line.split("Peak:")[1].split("dBFS")[0].strip())
            except ValueError:
                pass
    if integrated is None:
        raise FFmpegError(f"ebur128 produced no integrated loudness for {path}\n{text[-1500:]}")
    return {"integrated_lufs": integrated, "true_peak_dbfs": true_peak}


def _loudnorm_json(stderr: str) -> dict:
    start = stderr.rfind("{")
    end = stderr.rfind("}")
    if start < 0 or end < start:
        raise FFmpegError(f"loudnorm did not return JSON\n{stderr[-1500:]}")
    return json.loads(stderr[start : end + 1])


def peak_normalize(src: Path, dest: Path, *, true_peak: float = -1.0) -> dict:
    """Peak-normalize a short effect. Integrated loudness is not meaningful under a few seconds."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    probe_run = subprocess.run(
        [ffmpeg_bin(), "-hide_banner", "-i", str(src), "-af", "volumedetect", "-f", "null", "-"],
        capture_output=True,
        text=True,
    )
    max_volume = None
    for line in (probe_run.stderr or "").splitlines():
        if "max_volume:" in line:
            try:
                max_volume = float(line.split("max_volume:")[1].split("dB")[0].strip())
            except ValueError:
                pass
    if max_volume is None:
        raise FFmpegError(f"volumedetect failed for {src}")
    gain = true_peak - max_volume
    run(
        [
            ffmpeg_bin(), "-y", "-hide_banner", "-i", str(src),
            "-af", f"volume={gain:.3f}dB,alimiter=limit={10 ** (true_peak / 20):.5f}",
            "-ar", "48000", "-ac", "2", "-c:a", "pcm_s16le", str(dest),
        ]
    )
    return {"mode": "peak", "max_volume_db": max_volume, "gain_db": round(gain, 3)}


def master_audio(src: Path, dest: Path, *, integrated: float = -14.0, true_peak: float = -1.0) -> dict:
    """Loudness-master a bed or a mix. Peak-normalize anything shorter than 3 seconds."""
    info = probe(src)
    duration = float(info["format"]["duration"])
    if duration < 3.0:
        return peak_normalize(src, dest, true_peak=true_peak)
    stats = loudnorm_wav(src, dest, integrated=integrated, true_peak=true_peak)
    stats["mode"] = "loudnorm"
    return stats


def loudnorm_wav(
    src: Path,
    dest: Path,
    *,
    integrated: float = -14.0,
    true_peak: float = -1.0,
    lra: float = 11.0,
) -> dict:
    """Two-pass EBU R128 loudness normalisation to a WAV master."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    measure = subprocess.run(
        [
            ffmpeg_bin(),
            "-hide_banner",
            "-y",
            "-i",
            str(src),
            "-af",
            f"loudnorm=I={integrated}:TP={true_peak}:LRA={lra}:print_format=json",
            "-f",
            "null",
            "-",
        ],
        capture_output=True,
        text=True,
    )
    stats = _loudnorm_json(measure.stderr or "")
    filt = (
        f"loudnorm=I={integrated}:TP={true_peak}:LRA={lra}:"
        f"measured_I={stats['input_i']}:measured_TP={stats['input_tp']}:"
        f"measured_LRA={stats['input_lra']}:measured_thresh={stats['input_thresh']}:"
        f"offset={stats['target_offset']}:linear=true:print_format=summary"
    )
    run(
        [
            ffmpeg_bin(),
            "-y",
            "-hide_banner",
            "-i",
            str(src),
            "-af",
            filt,
            "-ar",
            "48000",
            "-ac",
            "2",
            "-c:a",
            "pcm_s16le",
            str(dest),
        ]
    )
    return stats
