"""Draw one 1920x1080 teaching frame. Native size. No upscale."""

from __future__ import annotations

import math
from functools import lru_cache

import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H = 1920, 1080
FPS = 30
NAVY = (5, 10, 18)
CYAN = (0, 212, 255)
BLUE = (30, 94, 255)
WHITE = (236, 241, 247)
DIM = (156, 180, 198)
AMBER = (255, 154, 72)
GLASS = (9, 24, 42)
FONT = "/usr/share/fonts/truetype/macos/Inter-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/macos/Inter-Regular.ttf"
DISCLAIMER = "Education only · Not financial advice · Examples do not indicate future results"

PALETTES = {
    "navy-cyan": {"accent": CYAN, "blue": BLUE},
    "navy-teal": {"accent": (20, 224, 200), "blue": (14, 140, 128)},
}


def ease(t: float) -> float:
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)


@lru_cache(maxsize=4)
def _font(size: int, bold: bool) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT if bold else FONT_REG, size)


def _wrap(text: str, size: int, width: int) -> list[str]:
    font = _font(size, True)
    lines: list[str] = []
    cur = ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if font.getlength(trial) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines[:3]


def _series(shot: dict) -> list[dict]:
    return shot.get("series") or []


def _prices(series: list[dict]) -> list[float]:
    return [float(row["close"]) for row in series]


def chart_box(local: float, dur: float) -> tuple[int, int, int, int]:
    """Slow push-in plus a breath, so the card never sits still."""
    z = 0.94 + 0.06 * ease(min(1.0, local / max(dur, 0.1))) + 0.01 * math.sin(local * 1.3)
    cx, cy = 960, 470
    x0, y0, x1, y1 = 140, 128, 1780, 820
    def sc(v, c):
        return int(c + (v - c) * z)
    return sc(x0, cx), sc(y0, cy), sc(x1, cx), sc(y1, cy)


def _map(i: int, n: int, price: float, lo: float, hi: float, box) -> tuple[float, float]:
    x0, y0, x1, y1 = box
    x = x0 + 90 + (x1 - x0 - 160) * (i / max(1, n - 1))
    span = max(1.0, hi - lo)
    y = y1 - 70 - (y1 - y0 - 130) * ((price - lo) / span)
    return x, y


def _path(series, reveal: float, box) -> list[tuple[float, float]]:
    if not series:
        return []
    n = len(series)
    last = max(1, min(n, int(round(reveal * (n - 1))) + 1))
    closes = _prices(series)
    lo = min(float(r["low"]) for r in series)
    hi = max(float(r["high"]) for r in series)
    pad = (hi - lo) * 0.08
    pts = [_map(i, n, closes[i], lo - pad, hi + pad, box) for i in range(last)]
    return pts


def _label_ok(used_y: list[float], series, price: float, box) -> bool:
    lo = min(float(r["low"]) for r in series)
    hi = max(float(r["high"]) for r in series)
    pad = (hi - lo) * 0.08
    y = _map(0, len(series), price, lo - pad, hi + pad, box)[1]
    return all(abs(y - prev) > 28 for prev in used_y)


def _rule(draw: ImageDraw.ImageDraw, series, price: float, box, accent, label: str) -> float:
    if not series:
        return
    lo = min(float(r["low"]) for r in series)
    hi = max(float(r["high"]) for r in series)
    pad = (hi - lo) * 0.08
    n = len(series)
    a = _map(0, n, price, lo - pad, hi + pad, box)
    b = _map(n - 1, n, price, lo - pad, hi + pad, box)
    for x in range(int(a[0]), int(b[0]), 16):
        draw.line([(x, a[1]), (min(x + 8, b[0]), a[1])], fill=accent, width=2)
    if label:
        font = _font(20, True)
        tw = font.getlength(label)
        draw.text((b[0] - tw, a[1] - 26), label, font=font, fill=accent)
    return a[1]


def paint(shot: dict, local: float, lesson_p: float, palette: str = "navy-cyan") -> np.ndarray:
    accent = PALETTES[palette]["accent"]
    blue = PALETTES[palette]["blue"]
    img = Image.new("RGB", (W, H), NAVY)
    draw = ImageDraw.Draw(img)
    # Drifting grid. One new position every frame.
    shift = int(local * 18 + lesson_p * 200) % 48
    for x in range(-48 + shift, W, 48):
        draw.line([(x, 0), (x, H)], fill=(12, 28, 46), width=1)
    for y in range(shift, H, 48):
        draw.line([(0, y), (W, y)], fill=(12, 28, 46), width=1)
    # Lesson progress. It moves for the whole running time.
    draw.rectangle([0, 0, int(W * lesson_p), 6], fill=accent)
    draw.text((72, 28), shot.get("chapter") or "", font=_font(26, True), fill=accent)

    kind = shot.get("kind") or "chart"
    dur = float(shot.get("duration") or 4)
    if kind == "ident":
        _ident(draw, shot, local, accent, blue)
    elif kind == "stack":
        _stack(draw, shot, local, accent)
    elif kind == "analogy":
        _analogy(draw, shot, local, dur, accent)
    elif kind == "legal":
        _legal(draw, local, accent)
    elif kind == "outro":
        _outro(draw, shot, local, accent, blue)
    elif kind == "worked":
        _worked(draw, shot, local, accent)
    else:
        _chart(draw, shot, local, dur, accent)

    # Sweep on the way in. A hard cut never sits on the boundary.
    if local < 0.28:
        x = int((local / 0.28) * W)
        draw.rectangle([x - 10, 0, x + 2, H], fill=accent)

    draw.rectangle([0, 868, W, H], fill=NAVY)
    draw.rectangle([0, 868, W, 874], fill=accent)
    lines = _wrap(shot.get("caption") or "", 32, 1700)
    y = 900
    for line in lines:
        draw.text((72, y), line, font=_font(32, True), fill=WHITE)
        y += 40
    draw.text((72, 1032), DISCLAIMER, font=_font(20, False), fill=DIM)
    return np.asarray(img, dtype=np.uint8)


def _ident(draw, shot, local, accent, blue) -> None:
    p = ease(min(1.0, local / 1.1))
    draw.text((160, 280), "GRID BOT", font=_font(92, True), fill=accent)
    if local > 0.35:
        draw.text((160, 390), "BLUEPRINT", font=_font(92, True), fill=WHITE)
    line = int(720 * p)
    draw.rectangle([160, 510, 160 + line, 518], fill=accent)
    if local > 0.7:
        draw.text((160, 560), shot.get("caption") or "", font=_font(40, True), fill=DIM)


def _stack(draw, shot, local, accent) -> None:
    items = shot.get("items") or [shot.get("caption") or ""]
    index = int(shot.get("index") or 0)
    y = 180
    for i, text in enumerate(items[: index + 1]):
        arrive = 1.0 if i < index else ease(min(1.0, local / 0.45))
        x = 180 + int((1 - arrive) * 70)
        outline = accent if i == index else (30, 60, 80)
        draw.rounded_rectangle([x, y, 1700, y + 120], 18, fill=GLASS, outline=outline, width=3)
        draw.text((x + 28, y + 24), f"{i + 1}", font=_font(28, True), fill=accent)
        for j, line in enumerate(_wrap(text, 30, 1300)):
            draw.text((x + 90, y + 28 + j * 36), line, font=_font(30, True), fill=WHITE)
        y += 150


def _legal(draw, local, accent) -> None:
    lines = [
        "Education only. Not financial advice.",
        "The path on screen is a public daily series, marked Example.",
        "No order is sent from this lesson.",
    ]
    y = 240
    for i, line in enumerate(lines):
        if local > i * 0.35:
            draw.text((180, y), line, font=_font(40, True), fill=WHITE if i == 0 else DIM)
            y += 90
    draw.rectangle([180, 560, 180 + int(400 * ease(min(1, local / 1.2))), 568], fill=accent)


def _outro(draw, shot, local, accent, blue) -> None:
    p = ease(min(1.0, local / 0.8))
    draw.text((160, 300), "NEXT", font=_font(80, True), fill=accent)
    if local > 0.25:
        for j, line in enumerate(_wrap(shot.get("caption") or "", 48, 1500)):
            draw.text((160, 420 + j * 64), line, font=_font(48, True), fill=WHITE)
    draw.rectangle([160, 620, 160 + int(640 * p), 628], fill=blue)


def _worked(draw, shot, local, accent) -> None:
    draw.text((160, 180), "WORKED EXAMPLE", font=_font(28, True), fill=accent)
    rows = shot.get("items") or []
    y = 260
    shown = 1 + int(ease(min(1.0, local / 0.9)) * max(0, len(rows) - 1))
    for i, text in enumerate(rows[:shown]):
        draw.rounded_rectangle([160, y, 1680, y + 100], 16, fill=GLASS, outline=accent, width=2)
        draw.text((190, y + 28), text, font=_font(32, True), fill=WHITE)
        y += 120


def _analogy(draw, shot, local, dur, accent) -> None:
    name = shot.get("analogy") or "ladder"
    box = (140, 150, 980, 820)
    draw.rounded_rectangle(box, 24, fill=GLASS, outline=accent, width=2)
    draw.text((170, 175), "ANALOGY", font=_font(22, True), fill=accent)
    t = ease(min(1.0, local / 0.8))
    if name == "fence":
        _fence(draw, t, accent)
    elif name == "list":
        _list(draw, t, accent)
    elif name == "buckets":
        _buckets(draw, t, accent)
    else:
        _ladder(draw, t, accent)
    # The real path stays beside the analogy.
    mini = dict(shot)
    mini_box_shot = shot
    _chart(draw, mini_box_shot, local, dur, accent, box=(1020, 150, 1800, 820))


def _ladder(draw, t, accent) -> None:
    draw.line([(360, 260), (360, 760)], fill=WHITE, width=8)
    draw.line([(560, 260), (560, 760)], fill=WHITE, width=8)
    rungs = int(1 + t * 5)
    for i in range(rungs):
        y = 320 + i * 70
        draw.line([(360, y), (560, y)], fill=accent, width=6)
    draw.text((620, 500), "Rungs wait.", font=_font(28, True), fill=DIM)


def _fence(draw, t, accent) -> None:
    draw.line([(300, 280), (300, 760)], fill=WHITE, width=8)
    draw.line([(700, 280), (700, 760)], fill=WHITE, width=8)
    if t > 0.3:
        draw.line([(300, 360), (700, 360)], fill=accent, width=6)
    if t > 0.6:
        draw.line([(300, 680), (700, 680)], fill=accent, width=6)
    draw.text((320, 500), "Top and bottom.", font=_font(28, True), fill=DIM)


def _list(draw, t, accent) -> None:
    labels = ["Pair", "Band", "Gaps", "Stop"]
    n = 1 + int(t * 3)
    y = 280
    for i in range(n):
        draw.rounded_rectangle([240, y, 860, y + 80], 12, outline=accent, width=2)
        draw.text((270, y + 22), labels[i], font=_font(28, True), fill=WHITE)
        y += 100


def _buckets(draw, t, accent) -> None:
    draw.rounded_rectangle([260, 340, 460, 720], 20, outline=WHITE, width=4)
    draw.text((300, 500), "One", font=_font(28, True), fill=DIM)
    if t > 0.45:
        draw.rounded_rectangle([560, 340, 760, 720], 20, outline=accent, width=4)
        draw.text((590, 500), "Two", font=_font(28, True), fill=accent)


def _chart(draw, shot, local, dur, accent, box=None) -> None:
    series = _series(shot)
    if box is None:
        box = chart_box(local, dur)
    draw.rounded_rectangle(box, 22, fill=GLASS, outline=(20, 50, 70), width=2)
    if not series:
        draw.text((box[0] + 40, box[1] + 40), "Example", font=_font(28, True), fill=DIM)
        return
    reveal = float(shot.get("reveal") or 1)
    # Draw the path on during this shot, ending at the shot's reveal.
    start = float(shot.get("reveal_from") or 0)
    now = start + (reveal - start) * ease(min(1.0, local / max(0.6, dur * 0.55)))
    pts = _path(series, now, box)
    if len(pts) > 1:
        draw.line(pts, fill=accent, width=4)
        # The playhead stays on the latest close. A second dot keeps walking
        # the path so the frame cannot freeze while the sentence continues.
        hx, hy = pts[-1]
        r = 8 + 2 * math.sin(local * 6)
        draw.ellipse((hx - r, hy - r, hx + r, hy + r), fill=WHITE)
        scan = pts[int((local * 0.35) * (len(pts) - 1)) % len(pts)]
        draw.ellipse((scan[0] - 5, scan[1] - 5, scan[0] + 5, scan[1] + 5), fill=AMBER)
        # Callout travels with the playhead.
        row_i = max(0, min(len(series) - 1, int(now * (len(series) - 1))))
        row = series[row_i]
        tag = f"{row['date']}  {int(round(row['close'])):,}"
        tw = int(_font(22, True).getlength(tag)) + 24
        tx = min(box[2] - tw - 16, max(box[0] + 16, hx + 16))
        ty = max(box[1] + 16, hy - 48)
        draw.rounded_rectangle([tx, ty, tx + tw, ty + 36], 8, fill=NAVY, outline=accent, width=2)
        draw.text((tx + 12, ty + 6), tag, font=_font(22, True), fill=WHITE)
    # Label the rails and the rung being spoken. Skip a label that would
    # sit on top of one already drawn (the rally scale compresses the old band).
    if now > 0.15:
        levels = [float(p) for p in (shot.get("levels") or [])]
        named = []
        if levels:
            named.extend([min(levels), max(levels)])
        focus = shot.get("focus_price")
        if focus is not None:
            named.append(float(focus))
        used_y: list[float] = []
        for price in levels:
            show = any(abs(price - n) < 2 for n in named)
            label = f"{int(round(price)):,}" if show else ""
            y = _rule(draw, series, price, box, DIM, label if _label_ok(used_y, series, price, box) else "")
            if label and y is not None:
                used_y.append(y)
    focus = shot.get("focus_price")
    if focus and now > 0.4:
        _rule(
            draw, series, float(focus), box, AMBER,
            shot.get("focus_label") or f"{int(round(float(focus))):,}",
        )
    draw.text((box[0] + 24, box[3] - 42), "EXAMPLE  ·  public daily closes", font=_font(18, True), fill=DIM)
    title = shot.get("chart_title") or ""
    if title:
        draw.text((box[0] + 24, box[1] + 16), title, font=_font(22, True), fill=WHITE)
