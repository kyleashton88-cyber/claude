"""A synthetic ungraded camera-style card, so the grade can be shown without a shoot."""

from __future__ import annotations

import subprocess
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from lib.brand import H, W
from lib.ffmpeg_util import ffmpeg_bin


from lib.fonts import font_file


def _font(size: int):
    from PIL import ImageFont
    return ImageFont.truetype(str(font_file("Inter", "Medium")), size)


def paint_card(t: float) -> Image.Image:
    img = Image.new("RGB", (W, H), (28, 24, 20))
    draw = ImageDraw.Draw(img)
    # Gray ramp. A grade should keep this neutral and ordered.
    for i in range(16):
        v = int(12 + i * 14)
        draw.rectangle([80 + i * 70, 120, 140 + i * 70, 280], fill=(v, v, v))
    # Skin-tone row. Protection should hold the hue.
    skins = [(214, 170, 140), (196, 142, 112), (168, 112, 86), (232, 196, 170), (140, 96, 74)]
    for i, color in enumerate(skins):
        draw.rounded_rectangle([80 + i * 220, 340, 270 + i * 220, 520], radius=16, fill=color)
    draw.text((80, 80), "Ungraded reference card", font=_font(36), fill=(230, 220, 200))
    # A small chart so the waveform has edges, drifting so the scope is not one line.
    drift = int(12 * np.sin(t * 1.4))
    for i, h in enumerate((180, 260, 140, 300, 220, 160)):
        x = 80 + i * 90
        draw.rectangle([x, 860 - h + drift, x + 50, 860], fill=(40, 110, 170))
    draw.rectangle([1280, 160, 1800, 860], fill=(48, 40, 32))
    draw.text((1320, 220), "Warm cast", font=_font(42), fill=(90, 60, 40))
    draw.text((1320, 290), "Dark exposure", font=_font(42), fill=(90, 60, 40))
    # Apply the fault: warm and dark. This is the "before".
    arr = np.asarray(img).astype(np.float32)
    arr *= np.array([1.18, 0.90, 0.68], dtype=np.float32)
    arr *= 0.62
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGB")


def write_card(dest: Path, seconds: float = 4.0, fps: int = 30) -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    frames = int(round(seconds * fps))
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
        f"{W}x{H}",
        "-r",
        str(fps),
        "-i",
        "-",
        "-c:v",
        "libx264",
        "-preset",
        "medium",
        "-crf",
        "18",
        "-pix_fmt",
        "yuv420p",
        "-color_range",
        "pc",
        "-color_primaries",
        "bt709",
        "-color_trc",
        "bt709",
        "-colorspace",
        "bt709",
        "-movflags",
        "+faststart",
        "-an",
        str(dest),
    ]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    assert proc.stdin is not None
    for i in range(frames):
        proc.stdin.write(paint_card(i / fps).tobytes())
    proc.stdin.close()
    err = proc.stderr.read().decode() if proc.stderr else ""
    if proc.wait() != 0:
        raise RuntimeError(err[-1500:])
    return dest
