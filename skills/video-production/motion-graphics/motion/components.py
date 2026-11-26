"""Reusable teaching components. Every shape is drawn in code.

Stills are accepted only as existing raster files, and only scaled down.
"""

from __future__ import annotations

import math
from functools import lru_cache
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

from lib.brand import (
    AQUA,
    AQUA_LT,
    BLUE,
    BLUE_LT,
    H,
    INK,
    MUTED,
    NAVY,
    ORANGE,
    RED,
    SKIN,
    TEXT,
    W,
    WHITE,
    YELLOW,
)
from lib.easing import clamp, ease_out, interval, lerp, smoothstep
from motion.frame import Stage, font

# Bottom of the liquidity-ladder plate carries a wordmark. The crop stays above it.
_STILL_FOOTER_CUT = 0.855


def _candles(n: int = 22, seed: int = 11) -> list[tuple[float, float, float, float]]:
    rng = np.random.default_rng(seed)
    price = 100.0
    rows = []
    for i in range(n):
        drift = 0.42 if i < 8 else (-0.28 if i < 14 else 0.22)
        o = price
        c = o + drift + float(rng.normal(0, 0.28))
        h = max(o, c) + abs(float(rng.normal(0.38, 0.08)))
        low = min(o, c) - abs(float(rng.normal(0.34, 0.08)))
        price = c
        rows.append((o, h, low, c))
    return rows


CANDLES = _candles()


def _waypoints() -> list[tuple[float, float]]:
    """Normalised time, illustrative price. Buys live below 118, sells above."""
    return [
        (0.00, 118.0),
        (0.16, 115.2),
        (0.34, 110.6),
        (0.48, 114.4),
        (0.62, 119.6),
        (0.78, 123.4),
        (0.90, 119.2),
        (1.00, 116.8),
    ]


def price_at(u: float) -> float:
    pts = _waypoints()
    u = clamp(u)
    for (t0, p0), (t1, p1) in zip(pts, pts[1:]):
        if u <= t1:
            span = max(1e-6, t1 - t0)
            return lerp(p0, p1, smoothstep((u - t0) / span))
    return pts[-1][1]


BUYS = (116.0, 114.0, 112.0, 110.0)
SELLS = (120.0, 122.0, 124.0)


def fills_at(u: float) -> dict[float, str]:
    """Orders that have already been crossed in the filling direction."""
    pts = _waypoints()
    done: dict[float, str] = {}
    samples = [(0.0, pts[0][1])]
    steps = 240
    for i in range(1, steps + 1):
        uu = i / steps
        if uu > u + 1e-9:
            break
        samples.append((uu, price_at(uu)))
    for (t0, p0), (t1, p1) in zip(samples, samples[1:]):
        for level in BUYS:
            if p0 > level >= p1 and level not in done:
                done[level] = "buy"
        for level in SELLS:
            if p0 < level <= p1 and level not in done:
                done[level] = "sell"
    return done


def draw_title(stage: Stage, shot: dict, t: float) -> None:
    lines = list(shot.get("lines") or ["A grid, in one picture"])
    sub = shot.get("sub") or "Illustrative prices. Not a forecast."
    block_h = 110 * len(lines)
    y0 = 340 - (block_h - 110) / 2
    for i, line in enumerate(lines):
        u = ease_out(interval(t, 0.12 + i * 0.16, 0.45))
        alpha_scale = u
        y = y0 + i * 108 + (1 - u) * 28
        # Draw via an overlay so the entrance can fade.
        tw = stage.width(line, 86, "bold")
        ov = Image.new("RGBA", (int(tw) + 8, 110), (0, 0, 0, 0))
        ImageDraw.Draw(ov).text((0, 0), line, font=font(86, "bold"), fill=(*TEXT, int(255 * alpha_scale)))
        stage.paste(ov, (int((W - tw) / 2), int(y)))
    rule_u = ease_out(interval(t, 0.55, 0.4))
    rw = int(220 * rule_u)
    cx = W // 2
    stage.draw.rectangle([cx - rw, int(y0 + block_h + 8), cx + rw, int(y0 + block_h + 12)], fill=AQUA_LT)
    sub_u = ease_out(interval(t, 0.7, 0.4))
    if sub_u > 0.02:
        ov = Image.new("RGBA", (W, 50), (0, 0, 0, 0))
        ImageDraw.Draw(ov).text(
            (W / 2, 24),
            sub,
            font=font(28, "medium"),
            fill=(*MUTED, int(255 * sub_u)),
            anchor="mm",
        )
        stage.paste(ov, (0, int(y0 + block_h + 36)))
    lower = shot.get("lower_third") or {"kicker": "Worked picture", "line": "How a grid is drawn"}
    draw_lower_third(stage, lower, t)


def draw_candles(stage: Stage, shot: dict, t: float) -> None:
    box = (120, 150, 1800, 900)
    stage.panel(box, (8, 22, 40, 230), radius=22, outline=(*BLUE, 90), width=2)
    rows = CANDLES
    reveal = smoothstep(interval(t, 0.15, stage.duration * 0.72))
    n = len(rows)
    shown = max(1, int(round(reveal * n)))
    highs = [r[1] for r in rows]
    lows = [r[2] for r in rows]
    lo, hi = min(lows) - 0.8, max(highs) + 0.8
    x0, y0, x1, y1 = 180, 210, 1680, 820
    slot = (x1 - x0) / n

    def py(price: float) -> float:
        return y1 - (y1 - y0) * ((price - lo) / (hi - lo))

    # Faint range the eye can use before the candles finish.
    for frac, label in ((0.25, ""), (0.5, ""), (0.75, "")):
        yy = y0 + (y1 - y0) * (1 - frac)
        stage.draw.line([(x0, yy), (x1, yy)], fill=(28, 58, 88), width=1)
    for i in range(shown):
        o, h, low, c = rows[i]
        local = 1.0 if i < shown - 1 else clamp((reveal * n) - (shown - 1))
        local = max(local, 0.15)
        cx = x0 + slot * i + slot * 0.5
        color = AQUA if c >= o else ORANGE
        wick_top = lerp(py(o), py(h), local)
        wick_bot = lerp(py(o), py(low), local)
        stage.draw.line([(cx, wick_top), (cx, wick_bot)], fill=color, width=2)
        body_top = py(max(o, lerp(o, c, local)))
        body_bot = py(min(o, lerp(o, c, local)))
        if body_bot - body_top < 8:
            mid = (body_top + body_bot) / 2
            body_top, body_bot = mid - 4, mid + 4
        bw = max(8, slot * 0.46)
        stage.draw.rounded_rectangle(
            [cx - bw / 2, body_top, cx + bw / 2, body_bot],
            radius=2,
            fill=color,
        )
    # Last price tag.
    last = rows[shown - 1]
    tag = f"{last[3]:.1f}"
    ty = py(last[3])
    stage.panel((x1 + 16, int(ty) - 18, x1 + 110, int(ty) + 18), (*NAVY, 240), radius=8)
    stage.text((x1 + 63, ty), tag, 20, TEXT, weight="mono", anchor="mm")
    stage.text((x0, 846), "Illustrative session  ·  each candle is open, high, low, close", 20, MUTED, weight="regular")
    # Legend
    stage.draw.rounded_rectangle([x0, 168, x0 + 18, 186], radius=3, fill=AQUA)
    stage.text((x0 + 26, 176), "Close above open", 18, MUTED, weight="medium", anchor="lm")
    stage.draw.rounded_rectangle([x0 + 230, 168, x0 + 248, 186], radius=3, fill=ORANGE)
    stage.text((x0 + 256, 176), "Close below open", 18, MUTED, weight="medium", anchor="lm")


def _price_y(price: float, top: int = 200, bot: int = 860) -> float:
    lo, hi = 106.0, 128.0
    return bot - (bot - top) * ((price - lo) / (hi - lo))


def draw_ladder(stage: Stage, shot: dict, t: float) -> None:
    u = clamp((t - 0.2) / max(0.2, stage.duration - 0.4))
    price = price_at(u)
    done = fills_at(u)
    box = (100, 140, 1820, 910)
    stage.panel(box, (8, 22, 40, 220), radius=22, outline=(*BLUE, 80), width=2)
    left, right = 430, 1480
    # Range band behind the ladder.
    y_hi = _price_y(124)
    y_lo = _price_y(110)
    band = Image.new("RGBA", (right - left, int(y_lo - y_hi)), (*BLUE, 36))
    stage.paste(band, (left, int(y_hi)))
    stage.text((left + 16, (y_hi + y_lo) / 2), "Range", 18, BLUE_LT, weight="medium", anchor="lm")

    def row(level: float, side: str) -> None:
        y = _price_y(level)
        filled = level in done
        color = AQUA if side == "buy" else BLUE_LT
        for x in range(left, right, 18):
            stage.draw.line([(x, y), (min(x + 8, right), y)], fill=(48, 86, 120), width=2)
        label = "BUY" if side == "buy" else "SELL"
        chip_w = 108
        if side == "buy":
            chip = (150, int(y) - 16, 150 + chip_w, int(y) + 16)
        else:
            chip = (right + 24, int(y) - 16, right + 24 + chip_w, int(y) + 16)
        fill = (*color, 230) if filled else (10, 28, 48, 220)
        outline = (*AQUA_LT, 255) if filled else (*color, 180)
        stage.panel(chip, fill, radius=8, outline=outline, width=2)
        stage.text(((chip[0] + chip[2]) / 2, y), "FILLED" if filled else label, 16, WHITE if filled else color, weight="bold", anchor="mm")
        stage.text((left - 18, y), f"{level:.0f}", 18, TEXT, weight="mono", anchor="rm")

    enter = smoothstep(interval(t, 0.05, 0.6))
    n_rows = int(round(enter * (len(BUYS) + len(SELLS))))
    ordered = [(lv, "sell") for lv in reversed(SELLS)] + [(lv, "buy") for lv in BUYS]
    for level, side in ordered[:n_rows]:
        row(level, side)

    # Price bead.
    y = _price_y(price)
    stage.draw.line([(left, y), (right, y)], fill=YELLOW, width=3)
    stage.draw.ellipse([right - 8, y - 10, right + 12, y + 10], fill=YELLOW)
    tag_w = 168
    stage.panel((right - tag_w - 18, int(y) - 46, right - 14, int(y) - 12), (20, 16, 8, 235), radius=8)
    stage.text((right - 18 - tag_w / 2, y - 29), f"Price  {price:.1f}", 18, YELLOW, weight="mono", anchor="mm")

    count = len(done)
    draw_counter(stage, count, len(BUYS) + len(SELLS), "orders filled", (128, 158), t)


def draw_risk(stage: Stage, shot: dict, t: float) -> None:
    """Price range plus a liquidation line and a shrinking buffer."""
    u = clamp((t - 0.15) / max(0.2, stage.duration - 0.3))
    # Price walks down toward the line so the buffer is the lesson.
    price = lerp(121.0, 109.4, smoothstep(u))
    range_hi, range_lo = 124.0, 112.0
    liq = 104.0
    box = (140, 160, 1780, 860)
    stage.panel(box, (8, 22, 40, 220), radius=22, outline=(*BLUE, 80), width=2)
    left, right = 260, 1500
    top, bot = 230, 800

    def py(p: float) -> float:
        return bot - (bot - top) * ((p - 100.0) / (30.0))

    y_hi, y_lo, y_liq, y_px = py(range_hi), py(range_lo), py(liq), py(price)
    band = Image.new("RGBA", (right - left, max(1, int(y_lo - y_hi))), (*AQUA, 40))
    stage.paste(band, (left, int(y_hi)))
    stage.draw.line([(left, y_hi), (right, y_hi)], fill=AQUA_LT, width=3)
    stage.draw.line([(left, y_lo), (right, y_lo)], fill=AQUA, width=3)
    stage.text((right + 16, y_hi), "Range high", 20, AQUA_LT, weight="medium", anchor="lm")
    stage.text((right + 16, y_lo), "Range low", 20, AQUA, weight="medium", anchor="lm")
    # Dashed liquidation line.
    pulse = 0.55 + 0.45 * (0.5 + 0.5 * math.sin(t * 5.0))
    dash_color = tuple(int(lerp(120, c, pulse)) for c in RED)
    for x in range(left, right, 22):
        stage.draw.line([(x, y_liq), (min(x + 12, right), y_liq)], fill=dash_color, width=3)
    stage.text((right + 16, y_liq), "Liquidation", 20, RED, weight="bold", anchor="lm")
    # Price.
    stage.draw.line([(left, y_px), (right, y_px)], fill=YELLOW, width=3)
    stage.draw.ellipse([left - 8, y_px - 8, left + 8, y_px + 8], fill=YELLOW)
    buffer = price - liq
    warn = buffer < 8
    draw_counter(stage, buffer, None, "buffer to the line", (128, 168), t, decimals=1, suffix="")
    if warn:
        a = int(180 + 60 * pulse)
        stage.panel((760, 250, 1160, 318), (*RED, a), radius=14)
        stage.text((960, 284), "Liquidation line", 26, WHITE, weight="bold", anchor="mm")
    # Arrow from price down to the line.
    draw_callout(
        stage,
        (left + 80, y_px + 10),
        (left + 80, y_liq - 8),
        "This gap is the buffer",
        t,
        delay=0.35,
    )


def draw_counter(
    stage: Stage,
    value: float,
    total: int | None,
    label: str,
    origin: tuple[int, int],
    t: float,
    decimals: int = 0,
    suffix: str = "",
) -> None:
    u = ease_out(interval(t, 0.2, 0.45))
    if decimals == 0:
        shown = f"{int(round(value))}"
    else:
        shown = f"{value:.{decimals}f}"
    if total is not None:
        shown = f"{shown}/{total}"
    shown += suffix
    x, y = origin
    pop = 0.92 + 0.08 * u
    stage.panel((x, y, x + 280, y + 108), (6, 18, 34, int(230 * u)), radius=16, outline=(*AQUA, 140), width=2)
    stage.text((x + 24, y + 18), label.upper(), 14, AQUA_LT, weight="bold")
    # Scale is faked by font size so we stay on the pixel grid.
    size = int(42 * pop)
    stage.text((x + 24, y + 78), shown, size, TEXT, weight="mono", anchor="ls")


def draw_callout(
    stage: Stage,
    start,
    end,
    label: str,
    t: float,
    delay: float = 0.2,
    label_at: tuple[int, int] | None = None,
) -> None:
    u = ease_out(interval(t, delay, 0.45))
    if u <= 0.01:
        return
    x = lerp(start[0], end[0], u)
    y = lerp(start[1], end[1], u)
    stage.draw.line([start, (x, y)], fill=YELLOW, width=3)
    if u > 0.85:
        ang = math.atan2(end[1] - start[1], end[0] - start[0])
        head = 14
        p1 = (end[0], end[1])
        p2 = (end[0] - head * math.cos(ang - 0.4), end[1] - head * math.sin(ang - 0.4))
        p3 = (end[0] - head * math.cos(ang + 0.4), end[1] - head * math.sin(ang + 0.4))
        stage.draw.polygon([p1, p2, p3], fill=YELLOW)
        tw = stage.width(label, 20, "bold")
        if label_at is None:
            lx, ly = int(end[0] + 16), int(end[1] - 36)
        else:
            lx, ly = label_at
        stage.panel((lx, ly, int(lx + tw + 28), ly + 36), (20, 16, 8, 230), radius=8)
        stage.text((lx + 14, ly + 18), label, 20, YELLOW, weight="bold", anchor="lm")


def draw_lower_third(stage: Stage, spec: dict, t: float) -> None:
    u = ease_out(interval(t, 0.25, 0.45))
    if u <= 0.01:
        return
    kicker = spec.get("kicker") or "Picture"
    line = spec.get("line") or ""
    width = int(max(520, stage.width(line, 28, "bold") + 48))
    x = int(lerp(-width - 20, 72, u))
    y = 860
    stage.panel((x, y, x + width, y + 84), (6, 18, 32, 235), radius=14, outline=(*AQUA, 160), width=2)
    stage.draw.rectangle([x, y, x + 8, y + 84], fill=AQUA_LT)
    stage.text((x + 24, y + 22), kicker.upper(), 14, AQUA_LT, weight="bold")
    stage.text((x + 24, y + 58), line, 26, TEXT, weight="bold", anchor="lm")


def draw_character(stage: Stage, origin: tuple[int, int], t: float, face: str = "right") -> None:
    """A geometric figure. Not a likeness of any person."""
    u = ease_out(interval(t, 0.1, 0.4))
    ox, oy = origin
    oy = int(oy + (1 - u) * 16)
    sign = 1 if face == "right" else -1
    stage.draw.ellipse([ox - 46, oy - 8, ox + 50, oy + 10], fill=(4, 12, 22))
    stage.draw.line([(ox - 14, oy - 70), (ox - 18, oy)], fill=NAVY, width=12)
    stage.draw.line([(ox + 14, oy - 70), (ox + 20, oy)], fill=NAVY, width=12)
    stage.draw.rounded_rectangle([ox - 34, oy - 168, ox + 34, oy - 64], radius=16, fill=NAVY)
    ax0, ax1 = ox + sign * 26, ox + sign * 34
    stage.draw.rectangle([min(ax0, ax1), oy - 168, max(ax0, ax1), oy - 96], fill=AQUA)
    stage.draw.ellipse([ox - 26, oy - 228, ox + 26, oy - 176], fill=SKIN)
    stage.draw.pieslice([ox - 26, oy - 230, ox + 26, oy - 176], 200, 340, fill=INK)
    ang = lerp(0.9, 0.15, ease_out(interval(t, 0.35, 0.55)))
    if face == "left":
        ang = math.pi - ang
    x0, y0 = ox + sign * 28, oy - 140
    x1 = x0 + math.cos(ang) * 78
    y1 = y0 + math.sin(ang) * 78
    stage.draw.line([(x0, y0), (x1, y1)], fill=SKIN, width=12)
    stage.draw.ellipse([x1 - 7, y1 - 7, x1 + 7, y1 + 7], fill=SKIN)


def _load_still(path: Path) -> Image.Image:
    if not path.is_file():
        raise FileNotFoundError(f"still not found: {path}")
    img = Image.open(path).convert("RGB")
    return img


@lru_cache(maxsize=4)
def _still(path: str) -> Image.Image:
    return _load_still(Path(path))


def ken_burns_frame(image: Image.Image, rect: tuple[float, float, float, float], size: tuple[int, int]) -> Image.Image:
    """Crop `rect` (x, y, w, h) in source pixels and scale to `size`.

    Refuses to scale up. The crop must already cover the destination.
    """
    x, y, w, h = rect
    dw, dh = size
    if w + 0.5 < dw or h + 0.5 < dh:
        raise ValueError(
            f"Ken Burns would upscale ({w:.0f}×{h:.0f} → {dw}×{dh}). "
            "Use a still that is already at least frame size."
        )
    x0 = int(math.floor(x))
    y0 = int(math.floor(y))
    x1 = int(math.ceil(x + w))
    y1 = int(math.ceil(y + h))
    x0 = max(0, min(x0, image.width - 1))
    y0 = max(0, min(y0, image.height - 1))
    x1 = max(x0 + 1, min(image.width, x1))
    y1 = max(y0 + 1, min(image.height, y1))
    crop = image.crop((x0, y0, x1, y1))
    return crop.resize(size, Image.Resampling.LANCZOS)


def _resolve_still(path: str) -> str:
    from lib.brand import REPO_ROOT

    candidate = Path(path)
    if candidate.is_file():
        return str(candidate)
    rooted = REPO_ROOT / candidate
    if rooted.is_file():
        return str(rooted)
    raise FileNotFoundError(f"still not found: {path}")


def still_crop(image: Image.Image, u: float) -> tuple[float, float, float, float]:
    """A slow push-in that stays above the plate's footer wordmark."""
    usable_bottom = image.height * _STILL_FOOTER_CUT
    aspect = 16 / 9
    h0 = min(usable_bottom - 8, image.width / aspect)
    h1 = max(720.0, h0 * 0.88)
    h = lerp(h0, h1, smoothstep(u))
    w = h * aspect
    max_x = max(0.0, image.width - w)
    x = lerp(40.0, min(max_x, 360.0), smoothstep(u))
    y = 0.0
    if y + h > usable_bottom:
        y = max(0.0, usable_bottom - h)
    if x + w > image.width:
        x = max(0.0, image.width - w)
    return x, y, w, h


def detail_crop(image: Image.Image, u: float) -> tuple[float, float, float, float]:
    """A tighter window anchored to the top-left of the same plate, so type is not sliced."""
    aspect = 16 / 9
    h = lerp(760.0, 600.0, smoothstep(u))
    w = h * aspect
    x = 0.0
    y = 0.0
    if w > image.width:
        w = float(image.width)
        h = w / aspect
    return x, y, w, h


def _rounded_photo(image: Image.Image, size: tuple[int, int], radius: int) -> Image.Image:
    w, h = size
    photo = image if image.size == size else image.resize(size, Image.Resampling.LANCZOS)
    out = Image.new("RGBA", size, (0, 0, 0, 0))
    mask = Image.new("L", size, 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, w - 1, h - 1], radius=radius, fill=255)
    out.paste(photo.convert("RGB"), (0, 0))
    out.putalpha(mask)
    return out


def draw_still(stage: Stage, shot: dict, t: float) -> None:
    path = shot.get("image")
    if not path:
        raise ValueError("still shot needs image")
    image = _still(_resolve_still(str(path)))
    u = clamp(t / stage.duration)
    # Back layer: the existing plate, inside a card, slow push-in.
    pw, ph = 1120, 630
    px, py = 72, 156
    plate = ken_burns_frame(image, still_crop(image, u * 0.55), (pw, ph))
    stage.paste(_rounded_photo(plate, (pw, ph), 18), (px, py))
    stage.panel((px, py, px + pw, py + ph), (0, 0, 0, 0), radius=18, outline=(*BLUE_LT, 180), width=3)
    # Near layer: a faster, tighter crop of the same file. It drifts more.
    dw, dh = 560, 315
    drift = int(lerp(0, -28, smoothstep(u)))
    dx, dy = 1260, 156 + drift
    detail = ken_burns_frame(image, detail_crop(image, u), (dw, dh))
    stage.paste(_rounded_photo(detail, (dw, dh), 16), (dx, dy))
    stage.panel((dx, dy, dx + dw, dy + dh), (0, 0, 0, 0), radius=16, outline=(*AQUA_LT, 220), width=3)
    stage.panel((dx, dy - 28, dx + 168, dy - 2), (*INK, 230), radius=6)
    stage.text((dx + 12, dy - 15), "NEAR LAYER", 14, AQUA_LT, weight="bold", anchor="lm")
    draw_callout(
        stage,
        (px + pw - 24, py + 48),
        (dx - 8, dy + 48),
        "Closer",
        t,
        delay=0.3,
        label_at=(1000, 108),
    )
    fills = int(round(lerp(0, float(shot.get("fills") or 6), ease_out(interval(t, 0.25, 0.7)))))
    draw_counter(stage, fills, None, "fills in the picture", (1260, 520 + drift // 2), t)
    draw_character(stage, (1688, 900), t, face="left")
    if shot.get("lower_third"):
        draw_lower_third(stage, shot["lower_third"], t)


DRAW = {
    "title": draw_title,
    "candles": draw_candles,
    "ladder": draw_ladder,
    "risk": draw_risk,
    "still": draw_still,
}
