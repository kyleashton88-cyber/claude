"""Picture and sound measurements for the gate."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import numpy as np

VP = Path(__file__).resolve().parents[2]
if str(VP) not in sys.path:
    sys.path.insert(0, str(VP))

from lib.ffmpeg_util import FFmpegError, ebur128, ffmpeg_bin, ffprobe_bin, run  # noqa: E402

from .profiles import LOUDNESS_TARGET, LOUDNESS_TOLERANCE, TRUE_PEAK_MAX, Profile


def media_info(path: Path) -> dict:
    proc = run(
        [
            ffprobe_bin(),
            "-v",
            "error",
            "-show_entries",
            "format=duration:stream=codec_type,codec_name,width,height,avg_frame_rate,pix_fmt",
            "-of",
            "json",
            str(path),
        ]
    )
    data = json.loads(proc.stdout)
    info = {
        "duration": float((data.get("format") or {}).get("duration") or 0),
        "video": None,
        "audio": None,
    }
    for stream in data.get("streams") or []:
        if stream.get("codec_type") == "video" and info["video"] is None:
            rate = str(stream.get("avg_frame_rate") or "0/1")
            num, den = rate.split("/")
            den_f = float(den) if den else 0.0
            fps = float(num) / den_f if den_f else 0.0
            info["video"] = {
                "codec": stream.get("codec_name"),
                "width": int(stream.get("width") or 0),
                "height": int(stream.get("height") or 0),
                "fps": fps,
                "pix_fmt": stream.get("pix_fmt"),
            }
        elif stream.get("codec_type") == "audio" and info["audio"] is None:
            info["audio"] = {"codec": stream.get("codec_name")}
    return info


def judge_loudness(integrated: float | None, true_peak: float | None) -> tuple[list[str], list[str]]:
    """Return (loudness problems, true-peak problems). Missing numbers fail."""
    loud: list[str] = []
    peak: list[str] = []
    if integrated is None:
        loud.append(
            f"integrated loudness was not measured. Target is {LOUDNESS_TARGET:.0f} LUFS "
            f"± {LOUDNESS_TOLERANCE:.0f}. This is a failure, not a note."
        )
    else:
        delta = integrated - LOUDNESS_TARGET
        if abs(delta) > LOUDNESS_TOLERANCE + 1e-6:
            loud.append(
                f"integrated loudness {integrated:.1f} LUFS is outside "
                f"{LOUDNESS_TARGET:.0f} ± {LOUDNESS_TOLERANCE:.0f}"
            )
    if true_peak is None:
        peak.append(
            f"true peak was not measured. Limit is {TRUE_PEAK_MAX:.0f} dBTP. This is a failure, not a note."
        )
    elif true_peak > TRUE_PEAK_MAX + 1e-6:
        peak.append(f"true peak {true_peak:.1f} dBTP is above {TRUE_PEAK_MAX:.0f} dBTP")
    return loud, peak


def measure_loudness(path: Path) -> tuple[float | None, float | None, str | None]:
    try:
        stats = ebur128(path)
    except FFmpegError as exc:
        return None, None, str(exc)
    return stats.get("integrated_lufs"), stats.get("true_peak_dbfs"), None


def gray_frames(path: Path, fps: int = 2) -> np.ndarray:
    raw = subprocess.check_output(
        [
            ffmpeg_bin(),
            "-v",
            "error",
            "-i",
            str(path),
            "-vf",
            f"fps={fps},scale=160:90",
            "-f",
            "rawvideo",
            "-pix_fmt",
            "gray",
            "-",
        ]
    )
    frame = 160 * 90
    count = len(raw) // frame
    if count == 0:
        return np.zeros((0, frame), dtype=np.uint8)
    trimmed = raw[: count * frame]
    return np.frombuffer(trimmed, dtype=np.uint8).reshape(count, frame)


def longest_static(frames: np.ndarray, fps: int = 2, mad_limit: float = 0.5) -> tuple[float, float]:
    """Longest run of near-identical frames, in seconds, and when it starts."""
    if len(frames) < 2:
        return 0.0, 0.0
    delta = np.abs(frames[1:].astype(np.int16) - frames[:-1].astype(np.int16)).mean(axis=1)
    worst = 1
    worst_at = 0
    run = 1
    for index, value in enumerate(delta, start=1):
        if value < mad_limit:
            run += 1
            if run > worst:
                worst = run
                worst_at = index - run + 1
        else:
            run = 1
    return worst / fps, worst_at / fps


def black_runs(frames: np.ndarray, fps: int = 2, luma_max: float = 4.0) -> list[tuple[float, float]]:
    """Runs of near-black frames. Navy #00081B sits above luma_max and is not black."""
    if len(frames) == 0:
        return []
    dark = frames.mean(axis=1) < luma_max
    runs: list[tuple[float, float]] = []
    start = None
    for index, flag in enumerate(dark):
        if flag and start is None:
            start = index
        elif not flag and start is not None:
            runs.append((start / fps, (index - start) / fps))
            start = None
    if start is not None:
        runs.append((start / fps, (len(dark) - start) / fps))
    return runs


def silent_gaps(path: Path, min_seconds: float) -> list[str]:
    """Silence at least min_seconds long. The detector threshold is the limit, so any hit fails."""
    proc = subprocess.run(
        [
            ffmpeg_bin(),
            "-hide_banner",
            "-i",
            str(path),
            "-af",
            f"silencedetect=n=-50dB:d={min_seconds}",
            "-f",
            "null",
            "-",
        ],
        capture_output=True,
        text=True,
    )
    text = proc.stderr or ""
    durations = [line.strip() for line in text.splitlines() if "silence_duration:" in line]
    if durations:
        return durations
    starts = [line.strip() for line in text.splitlines() if "silence_start:" in line]
    ends = [line for line in text.splitlines() if "silence_end:" in line]
    if len(starts) > len(ends):
        return starts[len(ends):]
    return []


def extract_png(path: Path, second: float, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    subprocess.check_call(
        [
            ffmpeg_bin(),
            "-y",
            "-v",
            "error",
            "-ss",
            f"{second:.3f}",
            "-i",
            str(path),
            "-frames:v",
            "1",
            str(dest),
        ]
    )


def sample_times(duration: float) -> list[float]:
    if duration <= 0.4:
        return [max(0.0, duration / 2)]
    raw = [0.4, duration * 0.3, duration * 0.55, duration * 0.8, max(0.3, duration - 0.35)]
    times: list[float] = []
    for item in raw:
        clipped = min(max(0.1, item), max(0.1, duration - 0.05))
        if not any(abs(clipped - seen) < 0.2 for seen in times):
            times.append(clipped)
    return times or [min(0.2, duration / 2)]


def technical_problems(info: dict, profile: Profile) -> dict[str, list[str]]:
    video = info.get("video") or {}
    audio = info.get("audio") or {}
    resolution: list[str] = []
    fps: list[str] = []
    codec: list[str] = []
    if not video:
        resolution.append("no video stream")
        fps.append("no video stream")
        codec.append("no video stream")
    else:
        if video["width"] != profile.width or video["height"] != profile.height:
            resolution.append(
                f"frame is {video['width']}x{video['height']}, {profile.label} expects {profile.width}x{profile.height}"
            )
        if abs(video["fps"] - profile.fps) > 0.05:
            fps.append(f"frame rate is {video['fps']:.3f}, expected {profile.fps:.0f}")
        if video.get("codec") != profile.video_codec:
            codec.append(f"video codec is {video.get('codec')}, expected {profile.video_codec}")
        if video.get("pix_fmt") not in {None, "yuv420p"}:
            codec.append(f"pixel format is {video.get('pix_fmt')}, expected yuv420p")
    if not audio:
        codec.append("no audio stream")
    elif audio.get("codec") != profile.audio_codec:
        codec.append(f"audio codec is {audio.get('codec')}, expected {profile.audio_codec}")
    return {"resolution": resolution, "fps": fps, "codec": codec}
