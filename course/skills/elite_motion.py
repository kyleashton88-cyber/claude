"""Elite motion graphics. Free tools only: Pillow and ffmpeg.

One Lanczos scale, then a crop that drifts inside the spare margin, so labels
are not resampled on every frame. Example plates are drawn here from the
public index in real-market-charts/data. They use teal #14E0C8 on navy.
No exchange name, no logo, no dollar sign, no coin picture.
"""

from __future__ import annotations

import csv
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

DATA = Path(__file__).resolve().parent / "real-market-charts" / "data"
FONT = "/usr/share/fonts/truetype/macos/Inter-Bold.ttf"
NAVY = (5, 10, 18)
TEAL = (0x14, 0xE0, 0xC8)
WHITE = (255, 255, 255)
MUTED = (160, 196, 190)
W, H = 1536, 1024


def _font(size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT, size)


def _series(name: str) -> list[tuple[str, float]]:
    rows = []
    with (DATA / name).open() as handle:
        for row in csv.DictReader(handle):
            rows.append((row["date"], float(row["index"])))
    return rows


def _canvas() -> Image.Image:
    return Image.new("RGB", (W, H), NAVY)


def _stamp(draw: ImageDraw.ImageDraw, text: str, y: int = 900) -> None:
    font = _font(42)
    box = font.getbbox(text)
    x = (W - (box[2] - box[0])) // 2
    draw.text((x, y), text, font=font, fill=TEAL)


def _label(draw: ImageDraw.ImageDraw, text: str, xy: tuple[int, int], fill, size: int = 36) -> None:
    draw.text(xy, text, font=_font(size), fill=fill)


def _plot(draw: ImageDraw.ImageDraw, pts: list[tuple[float, float]], color, width: int, upto: int) -> None:
    if upto < 2:
        return
    show = pts[:upto]
    draw.line(show, fill=color, width=width, joint="curve")


def _norm(rows: list[tuple[str, float]], left: int, right: int, top: int, bottom: int):
    vals = [v for _, v in rows]
    lo, hi = min(vals), max(vals)
    span = max(hi - lo, 1e-6)
    pts = []
    n = max(len(rows) - 1, 1)
    for i, (_, v) in enumerate(rows):
        x = left + (right - left) * i / n
        y = bottom - (bottom - top) * (v - lo) / span
        pts.append((x, y))
    return pts


def _frame_path(i: int, n: int) -> Image.Image:
    rows = [r for r in _series("btc-index.csv") if "2021-11-08" <= r[0] <= "2022-11-21"]
    im = _canvas()
    draw = ImageDraw.Draw(im)
    _label(draw, "8 NOV 2021", (120, 200), WHITE, 40)
    _label(draw, "21 NOV 2022", (1120, 200), WHITE, 40)
    pts = _norm(rows, 140, 1380, 280, 820)
    upto = max(2, int(len(pts) * (i + 1) / n))
    _plot(draw, pts, TEAL, 6, upto)
    if upto > len(pts) * 0.85:
        _label(draw, "ABOUT 76 PERCENT LOWER", (140, 150), WHITE, 36)
    _stamp(draw, "EXAMPLE")
    return im


def _frame_two(i: int, n: int) -> Image.Image:
    btc = [r for r in _series("btc-index.csv") if "2021-11-08" <= r[0] <= "2022-11-21"]
    eth = [r for r in _series("eth-index.csv") if "2021-11-08" <= r[0] <= "2022-11-21"]
    im = _canvas()
    draw = ImageDraw.Draw(im)
    _label(draw, "BITCOIN", (140, 190), TEAL, 36)
    _label(draw, "ETHER", (420, 190), WHITE, 36)
    pb = _norm(btc, 140, 1380, 280, 800)
    pe = _norm(eth, 140, 1380, 280, 800)
    upto = max(2, int(len(pb) * (i + 1) / n))
    _plot(draw, pb, TEAL, 6, upto)
    _plot(draw, pe, WHITE, 4, upto)
    if upto > len(pb) * 0.85:
        _label(draw, "0.89    EXAMPLE    NOT RULE", (430, 840), TEAL, 36)
    else:
        _stamp(draw, "EXAMPLE")
    return im


def _frame_day(i: int, n: int) -> Image.Image:
    im = _canvas()
    draw = ImageDraw.Draw(im)
    _label(draw, "12 JUN 2022", (280, 240), WHITE, 40)
    _label(draw, "13 JUN 2022", (980, 240), WHITE, 40)
    # Two range bars. The second day is the wide one (about 21 percent).
    grow = (i + 1) / n
    h1 = int(180 * min(1, grow * 1.4))
    h2 = int(460 * grow)
    draw.rounded_rectangle((360, 700 - h1, 520, 700), radius=16, outline=TEAL, width=6)
    draw.rounded_rectangle((980, 700 - h2, 1140, 700), radius=16, outline=TEAL, width=6)
    if grow > 0.7:
        _label(draw, "16 PERCENT CLOSE", (560, 760), WHITE, 36)
    _stamp(draw, "EXAMPLE")
    return im


def _frame_analogy(words: tuple[str, str], i: int, n: int) -> Image.Image:
    im = _canvas()
    draw = ImageDraw.Draw(im)
    grow = (i + 1) / n
    # A simple object that completes as the sentence lands.
    if grow > 0.15:
        draw.rounded_rectangle((460, 300, 1070, 760), radius=28, outline=TEAL, width=6)
    if grow > 0.4:
        for k, y in enumerate((400, 500, 600)):
            draw.line((540, y, 980, y), fill=TEAL, width=4)
            if k == 1:
                break
    if grow > 0.7:
        draw.line((540, 600, 860, 600), fill=WHITE, width=6)
    font = _font(72)
    a, b = words
    draw.text((160, 180), a, font=font, fill=WHITE)
    box = font.getbbox(a)
    draw.text((180 + box[2] - box[0], 180), b, font=font, fill=TEAL)
    _stamp(draw, "EXAMPLE")
    return im


ANALOGY = {
    "analogy-map": ("PAPER", " MAP"),
    "analogy-list": ("PRE", " FLIGHT"),
    "analogy-shelf": ("ONE", " SHELF"),
    "analogy-breaker": ("HAND", " SWITCH"),
    "analogy-bridges": ("TWO", " BRIDGES"),
    "analogy-line": ("WHICH", " LINE"),
    "analogy-card": ("RECIPE", " CARD"),
}


def write_frames(kind: str, dest: Path, frames: int = 24) -> tuple[int, int]:
    """Write frame-000.png ... and return (fps, count)."""
    dest.mkdir(parents=True, exist_ok=True)
    for i in range(frames):
        if kind == "chart-path":
            im = _frame_path(i, frames)
        elif kind == "chart-two":
            im = _frame_two(i, frames)
        elif kind == "chart-day":
            im = _frame_day(i, frames)
        elif kind in ANALOGY:
            im = _frame_analogy(ANALOGY[kind], i, frames)
        else:
            raise ValueError(kind)
        im.save(dest / f"frame-{i:03d}.png")
    return 12, frames


def camera_and_callouts(callouts: bool = True) -> str:
    """Crop drift inside one Lanczos scale, plus a teal box that steps every 4 seconds.

    ffmpeg's `%` operator breaks the drawbox parser, so the step uses mod().
    Example plates skip the box so it does not cover the path being drawn.
    """
    parts = [
        "scale=2000:-2:flags=lanczos:in_color_matrix=bt709:out_color_matrix=bt709",
        "crop=1920:1080:"
        "x='(in_w-1920)/2+20*sin(2*PI*t/9)':"
        "y='(in_h-1080)/2+16*sin(2*PI*t/13)'",
        "format=yuv420p",
        "setparams=range=tv:color_primaries=bt709:color_trc=bt709:colorspace=bt709",
        "fade=t=in:st=0:d=0.35",
    ]
    if callouts:
        parts.append(
            "drawbox="
            "x='140+mod(floor(t/4)\\,3)*520':"
            "y='300+mod(floor(t/4)\\,2)*160':"
            "w=460:h=150:color=0x14E0C8:t=4"
        )
    return ",".join(parts)
