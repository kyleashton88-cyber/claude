"""Short synthetic masters for tests and demos. No paid voice, no image API."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

VP = Path(__file__).resolve().parents[2]
if str(VP) not in sys.path:
    sys.path.insert(0, str(VP))

from lib.ffmpeg_util import ffmpeg_bin  # noqa: E402

FONT = VP / "templates" / "assets" / "fonts" / "Inter-Bold.ttf"


def _frame(width: int, height: int, index: int, *, moving: bool, disclaimer: bool) -> bytes:
    from PIL import Image, ImageDraw, ImageFont

    image = Image.new("RGB", (width, height), (0, 8, 27))
    draw = ImageDraw.Draw(image)
    margin = max(8, int(width * 0.06))
    if moving:
        box = max(16, width // 14)
        travel = max(1, width - box - 2 * margin)
        x = margin + int((index * max(4, width / 80)) % travel)
        y = margin + height // 6
        draw.rectangle((x, y, x + box, y + box), fill=(0, 212, 255))
    if disclaimer:
        size = 42 if height >= 720 else 28 if height >= 300 else 16
        face = ImageFont.truetype(str(FONT), size)
        label = "Education not financial advice"
        while size > 12 and draw.textlength(label, font=face) > width - 2 * margin:
            size -= 2
            face = ImageFont.truetype(str(FONT), size)
        draw.text((margin, int(height * 0.72)), label, fill=(244, 248, 252), font=face)
    return image.tobytes()


def encode_clip(
    path: Path,
    *,
    width: int,
    height: int,
    seconds: float = 4.0,
    fps: int = 30,
    disclaimer: bool = True,
    moving: bool = True,
    loudnorm: bool = True,
    audio: str = "tone",
) -> Path:
    """H.264 + AAC clip. `audio` is `tone` or `silent`."""
    path.parent.mkdir(parents=True, exist_ok=True)
    count = max(1, int(round(seconds * fps)))
    if audio == "silent":
        audio_graph = f"anullsrc=r=48000:cl=stereo:d={seconds}"
        audio_filter: list[str] = []
    elif loudnorm:
        audio_graph = f"sine=frequency=220:sample_rate=48000:duration={seconds}"
        audio_filter = ["-af", "loudnorm=I=-14:TP=-2.0:LRA=11"]
    else:
        audio_graph = f"sine=frequency=220:sample_rate=48000:duration={seconds}"
        audio_filter = ["-af", "volume=8dB"]
    cmd = [
        ffmpeg_bin(),
        "-y",
        "-hide_banner",
        "-loglevel",
        "error",
        "-f",
        "rawvideo",
        "-pix_fmt",
        "rgb24",
        "-s",
        f"{width}x{height}",
        "-r",
        str(fps),
        "-i",
        "-",
        "-f",
        "lavfi",
        "-i",
        audio_graph,
        *audio_filter,
        "-shortest",
        "-c:v",
        "libx264",
        "-preset",
        "veryfast",
        "-crf",
        "28",
        "-pix_fmt",
        "yuv420p",
        "-r",
        str(fps),
        "-c:a",
        "aac",
        "-b:a",
        "160k",
        "-movflags",
        "+faststart",
        str(path),
    ]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    assert proc.stdin is not None
    for index in range(count):
        proc.stdin.write(_frame(width, height, index, moving=moving, disclaimer=disclaimer))
    proc.stdin.close()
    code = proc.wait()
    if code != 0:
        raise subprocess.CalledProcessError(code, cmd)
    return path


def encode_black_gap(path: Path, *, fps: int = 10) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        ffmpeg_bin(),
        "-y",
        "-hide_banner",
        "-loglevel",
        "error",
        "-f",
        "lavfi",
        "-i",
        f"color=c=0x00081B:s=160x90:d=0.4:r={fps}",
        "-f",
        "lavfi",
        "-i",
        f"color=c=black:s=160x90:d=0.8:r={fps}",
        "-f",
        "lavfi",
        "-i",
        f"color=c=0x00081B:s=160x90:d=0.4:r={fps}",
        "-filter_complex",
        "[0:v][1:v][2:v]concat=n=3:v=1:a=0",
        "-c:v",
        "libx264",
        "-pix_fmt",
        "yuv420p",
        str(path),
    ]
    subprocess.check_call(cmd)
    return path


def stamp(seconds: float) -> str:
    ms = int(round(seconds * 1000))
    hours, ms = divmod(ms, 3_600_000)
    minutes, ms = divmod(ms, 60_000)
    secs, ms = divmod(ms, 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}.{ms:03d}"


def write_pass_captions(path: Path, end: float = 3.6) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "WEBVTT\n\n"
        f"{stamp(0.3)} --> {stamp(end)}\n"
        "Education, not financial advice.\n",
        encoding="utf-8",
    )
    return path
