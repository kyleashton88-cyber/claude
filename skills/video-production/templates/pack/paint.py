"""House-style stills drawn with Pillow. No image API."""

from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
FONTS = ROOT / "assets" / "fonts"
ROBOTO = FONTS / "RobotoCondensed-Bold.ttf"
INTER = FONTS / "Inter-Bold.ttf"

CYAN = (0, 212, 255)
TEXT = (244, 248, 252)
NAVY_TOP = (0, 8, 27)
NAVY_MID = (0, 15, 42)
NAVY_BOTTOM = (0, 11, 33)


def gradient(width: int, height: int) -> Image.Image:
    stops = np.array([0.0, 0.55, 1.0], dtype=np.float32)
    colors = np.array([NAVY_TOP, NAVY_MID, NAVY_BOTTOM], dtype=np.float32)
    column = np.linspace(0, 1, height, dtype=np.float32)
    rgb = np.stack([np.interp(column, stops, colors[:, channel]) for channel in range(3)], axis=1)
    frame = np.repeat(rgb[:, None, :], width, axis=1)
    return Image.fromarray(frame.astype(np.uint8), "RGB")


def font(path: Path, size: int) -> ImageFont.FreeTypeFont:
    if not path.is_file():
        raise FileNotFoundError(f"missing font {path}")
    return ImageFont.truetype(str(path), size)


def wrap(draw: ImageDraw.ImageDraw, text: str, face: ImageFont.ImageFont, limit: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        trial = word if not current else f"{current} {word}"
        if draw.textlength(trial, font=face) <= limit:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines or [text]


def paint_thumbnail(title: str, label: str, dest: Path) -> Path:
    image = gradient(1280, 720)
    draw = ImageDraw.Draw(image)
    for x in range(0, 1280, 48):
        draw.line([(x, 0), (x, 720)], fill=(0, 28, 48))
    for y in range(0, 720, 48):
        draw.line([(0, y), (1280, y)], fill=(0, 28, 48))
    headline = font(ROBOTO, 84)
    label_font = font(INTER, 32)
    small = font(INTER, 22)
    lines = wrap(draw, title, headline, 1080)
    y = 150
    for line in lines[:3]:
        draw.text((80, y), line, fill=TEXT, font=headline)
        y += 96
    draw.rectangle((80, y + 8, 280, y + 16), fill=CYAN)
    draw.text((80, y + 36), label, fill=CYAN, font=label_font)
    draw.text((80, 640), "EXAMPLE  ·  Education, not financial advice.", fill=TEXT, font=small)
    dest.parent.mkdir(parents=True, exist_ok=True)
    image.save(dest)
    return dest


def paint_endcard(title: str, next_title: str, dest: Path) -> dict:
    """1920×1080 card. The right side stays clear for a YouTube end screen."""
    width, height = 1920, 1080
    image = gradient(width, height)
    draw = ImageDraw.Draw(image)
    headline = font(ROBOTO, 64)
    label_font = font(INTER, 28)
    small = font(INTER, 22)
    # Content lives in the left 58%. The end-screen slot is the right third.
    draw.text((96, 180), "NEXT", fill=CYAN, font=label_font)
    y = 240
    for line in wrap(draw, next_title, headline, 900):
        draw.text((96, y), line, fill=TEXT, font=headline)
        y += 78
    draw.text((96, y + 24), title, fill=CYAN, font=label_font)
    # The right third stays clear for a YouTube end screen. Nothing is drawn there:
    # an outlined box labelled "End screen" read as an empty placeholder.
    slot = {"x": 1180, "y": 220, "w": 620, "h": 620}
    draw.text((96, 980), "Educational content only. Not financial advice.", fill=TEXT, font=small)
    dest.parent.mkdir(parents=True, exist_ok=True)
    image.save(dest)
    return {
        "path": str(dest),
        "width": width,
        "height": height,
        "hold_seconds": 20,
        "end_screen_slot": slot,
        "next_title": next_title,
        "safe_content": {"x": 80, "y": 120, "w": 1040, "h": 820},
    }
