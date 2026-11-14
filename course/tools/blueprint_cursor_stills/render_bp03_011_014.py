#!/usr/bin/env python3
"""Redraw BP-03 beats 011 and 014.

011: a ring is a cross (price touched a rung). A square is a fill (an order trades).
014: the stop is a sentence for when the path leaves the band.
Arrow tips are placed on their targets.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

sys.path.insert(0, str(Path(__file__).resolve().parent))
from render_bp01_007 import (  # noqa: E402
    BLUE,
    CYAN,
    FONT_BOLD,
    FONT_SEMI,
    MINT,
    WHITE,
    S,
    W,
    H,
    draw_bokeh,
    draw_grid,
    new_canvas,
    px,
    rounded_glow,
    text_size,
)

AMBER = (255, 176, 32)
ROOT = Path(__file__).resolve().parents[3]
OUT_011 = ROOT / "course/images/bp-03-what-is-a-grid-bot/011.png"
OUT_014 = ROOT / "course/images/bp-03-what-is-a-grid-bot/014.png"


def paste_layer(base: Image.Image, layer: Image.Image) -> None:
    base.paste(Image.alpha_composite(base.convert("RGBA"), layer).convert("RGB"))


def font(path: str, size: float) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, px(size))


def headline(base: Image.Image, x: int, y: int, parts: list[tuple[str, tuple]], face) -> None:
    draw = ImageDraw.Draw(base)
    cursor = px(x)
    for text, color in parts:
        draw.text((cursor, px(y)), text, font=face, fill=color)
        cursor += int(face.getlength(text))


def tag(base: Image.Image, box, text_lines: list[str], face) -> None:
    left, top, right, bottom = [px(v) for v in box]
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.rounded_rectangle(
        [left, top, right, bottom],
        radius=px(14),
        fill=(6, 14, 28, 235),
        outline=CYAN + (255,),
        width=px(3),
    )
    paste_layer(base, layer)
    draw = ImageDraw.Draw(base)
    heights = [text_size(face, line)[1] for line in text_lines]
    gap = px(4)
    block = sum(heights) + gap * (len(text_lines) - 1)
    cy = (top + bottom) // 2
    ty = cy - block // 2
    for line, h in zip(text_lines, heights):
        box_px = face.getbbox(line)
        tw = box_px[2] - box_px[0]
        tx = left + (right - left - tw) // 2 - box_px[0]
        draw.text((tx, ty - box_px[1]), line, font=face, fill=WHITE)
        ty += h + gap


def arrow(base: Image.Image, start, tip) -> None:
    """Straight cyan arrow. tip is a point already on the target."""
    x0, y0 = px(start[0]), px(start[1])
    x1, y1 = px(tip[0]), px(tip[1])
    ang = math.atan2(y1 - y0, x1 - x0)
    ux, uy = math.cos(ang), math.sin(ang)
    vx, vy = -uy, ux
    head = px(18)
    half = px(7)
    shaft = px(5) / 2
    sx = x1 - ux * (head - px(7))
    sy = y1 - uy * (head - px(7))
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.polygon(
        [
            (x0 + vx * shaft, y0 + vy * shaft),
            (x0 - vx * shaft, y0 - vy * shaft),
            (sx - vx * shaft, sy - vy * shaft),
            (sx + vx * shaft, sy + vy * shaft),
        ],
        fill=CYAN + (255,),
    )
    d.polygon(
        [
            (x1, y1),
            (x1 - ux * head + vx * half, y1 - uy * head + vy * half),
            (x1 - ux * head - vx * half, y1 - uy * head - vy * half),
        ],
        fill=CYAN + (255,),
    )
    paste_layer(base, layer)


def hline(base: Image.Image, x0, x1, y, color, width) -> None:
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.line([(px(x0), px(y)), (px(x1), px(y))], fill=color + (255,), width=px(width))
    glow = layer.filter(ImageFilter.GaussianBlur(radius=px(3)))
    paste_layer(base, glow)
    paste_layer(base, layer)


def dashed_polyline(base: Image.Image, pts, color, width, dash, gap) -> None:
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    dist = 0.0
    draw_on = True
    remain = dash
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        seg = math.hypot(x1 - x0, y1 - y0)
        if seg == 0:
            continue
        ux, uy = (x1 - x0) / seg, (y1 - y0) / seg
        walked = 0.0
        while walked < seg:
            step = min(remain, seg - walked)
            a = (x0 + ux * walked, y0 + uy * walked)
            b = (x0 + ux * (walked + step), y0 + uy * (walked + step))
            if draw_on:
                d.line([(px(a[0]), px(a[1])), (px(b[0]), px(b[1]))], fill=color + (255,), width=px(width))
            walked += step
            remain -= step
            if remain <= 0.2:
                draw_on = not draw_on
                remain = dash if draw_on else gap
    glow = layer.filter(ImageFilter.GaussianBlur(radius=px(2)))
    paste_layer(base, glow)
    paste_layer(base, layer)


def ring(base: Image.Image, cx, cy, radius, stroke, color) -> None:
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.ellipse(
        [px(cx - radius), px(cy - radius), px(cx + radius), px(cy + radius)],
        outline=color + (255,),
        width=px(stroke),
    )
    glow = layer.filter(ImageFilter.GaussianBlur(radius=px(2)))
    paste_layer(base, glow)
    paste_layer(base, layer)


def square(base: Image.Image, cx, cy, half, fill) -> None:
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.rounded_rectangle(
        [px(cx - half), px(cy - half), px(cx + half), px(cy + half)],
        radius=px(4),
        fill=fill + (255,),
        outline=CYAN + (255,),
        width=px(3),
    )
    paste_layer(base, layer)


def stamp(base: Image.Image, cx, cy) -> None:
    face = font(FONT_BOLD, 26)
    text = "EXAMPLE"
    tw, th = text_size(face, text)
    pad_x, pad_y = px(16), px(10)
    w, h = tw + pad_x * 2, th + pad_y * 2
    tile = Image.new("RGBA", (w + px(8), h + px(8)), (0, 0, 0, 0))
    d = ImageDraw.Draw(tile)
    d.rounded_rectangle(
        [px(4), px(4), w + px(4), h + px(4)],
        radius=px(10),
        outline=CYAN + (255,),
        width=px(3),
    )
    box = face.getbbox(text)
    d.text(
        (px(4) + pad_x - box[0], px(4) + (h - (box[3] - box[1])) // 2 - box[1]),
        text,
        font=face,
        fill=CYAN,
    )
    tile = tile.rotate(8, expand=True, resample=Image.Resampling.BICUBIC)
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    layer.paste(tile, (px(cx) - tile.size[0] // 2, px(cy) - tile.size[1] // 2), tile)
    paste_layer(base, layer)


def crossings(pts, rung_ys) -> list[tuple[float, float]]:
    found = []
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        if y0 == y1:
            continue
        lo, hi = (y0, y1) if y0 < y1 else (y1, y0)
        for y in rung_ys:
            # Count a crossing when the segment reaches the rung, including an endpoint.
            if lo - 0.1 <= y <= hi + 0.1:
                t = (y - y0) / (y1 - y0)
                if -0.02 <= t <= 1.02:
                    x = x0 + t * (x1 - x0)
                    found.append((x, float(y)))
    # Drop duplicates where two segments meet on a rung.
    unique = []
    for x, y in found:
        if any(abs(x - ux) < 8 and abs(y - uy) < 8 for ux, uy in unique):
            continue
        unique.append((x, y))
    unique.sort(key=lambda p: p[0])
    return unique


def luminance(p) -> float:
    return 0.2126 * p[0] + 0.7152 * p[1] + 0.0722 * p[2]


def is_navy(p) -> bool:
    return luminance(p) < 28 and p[1] < 36 and p[2] < 55


def margins(im: Image.Image) -> tuple[int, int, int, int]:
    pxls = im.load()
    min_x, min_y, max_x, max_y = W, H, 0, 0
    for y in range(H):
        for x in range(W):
            if luminance(pxls[x, y]) > 46:
                min_x = min(min_x, x)
                min_y = min(min_y, y)
                max_x = max(max_x, x)
                max_y = max(max_y, y)
    return min_x, W - 1 - max_x, min_y, H - 1 - max_y


def assert_tip(im: Image.Image, tip, toward, name: str) -> None:
    """From the tip, the next pixels toward the target are not navy."""
    pxls = im.load()
    x, y = tip
    tx, ty = toward
    ang = math.atan2(ty - y, tx - x)
    ux, uy = math.cos(ang), math.sin(ang)
    # The tip and the next pixel toward the target must be the arrow or the mark.
    # A ring is hollow, so do not walk into its empty centre.
    seen = []
    for step in range(0, 3):
        sx = int(round(x + ux * step))
        sy = int(round(y + uy * step))
        p = pxls[sx, sy]
        seen.append(p)
        if is_navy(p):
            raise SystemExit(f"{name} navy at {(sx, sy)} rgb={p} path={seen}")
    print(name, "tip ok", seen)


def finish(img: Image.Image) -> Image.Image:
    return img.resize((W, H), Image.Resampling.LANCZOS)


def render_011() -> Image.Image:
    img = new_canvas()
    draw_grid(img)
    draw_bokeh(img)
    rounded_glow(
        img,
        [px(96), px(330), px(1440), px(918)],
        radius=px(28),
        fill=(7, 16, 34, 230),
        outline=CYAN + (255,),
        glow=(0, 180, 230, 110),
        width=px(4),
    )

    face = font(FONT_SEMI, 32)
    cross_lines = ["Cross: price touched a rung"]
    fill_lines = ["Fill: an order trades"]
    cross_w = text_size(face, cross_lines[0])[0] / S + 40
    fill_w = text_size(face, fill_lines[0])[0] / S + 40
    tag_h = 64
    tag_top = 214
    cross_box = (108, tag_top, 108 + cross_w, tag_top + tag_h)
    fill_box = (1428 - fill_w, tag_top, 1428, tag_top + tag_h)
    if fill_box[0] < cross_box[2] + 28:
        raise SystemExit("011 labels overlap")
    ring_x = (cross_box[0] + cross_box[2]) / 2
    fill_x = (fill_box[0] + fill_box[2]) / 2

    # Three rungs. The labelled ring sits under the cross tag. The square sits under the fill tag.
    # Other crossings stay off those two vertical arrows.
    rung_ys = [470, 620, 770]
    for y in rung_ys:
        hline(img, 160, 1340, y, (70, 150, 190), 4)
    mid_x = (ring_x + fill_x) / 2
    pts = [
        (170, 545),
        (ring_x, 470),
        (mid_x, 700),
        (fill_x, 770),
        (min(1340, fill_x + 120), 545),
    ]
    hits = crossings(pts, rung_ys)
    fill_at = min(hits, key=lambda p: abs(p[0] - fill_x) + abs(p[1] - 770))
    ring_target = min(hits, key=lambda p: abs(p[0] - ring_x) + abs(p[1] - 470))
    rings = [
        p
        for p in hits
        if not (abs(p[0] - fill_at[0]) < 12 and abs(p[1] - fill_at[1]) < 12)
    ]
    print("011 crossings", [(round(x), round(y)) for x, y in hits], "ring", ring_target, "fill", fill_at)
    # A vertical leader must not pass through a different mark.
    for x, y in hits:
        if abs(x - ring_x) < 24 and abs(y - ring_target[1]) > 12:
            raise SystemExit(f"cross arrow would hit another mark at {(x, y)}")
        if abs(x - fill_x) < 24 and abs(y - fill_at[1]) > 12:
            raise SystemExit(f"fill arrow would hit another mark at {(x, y)}")

    dashed_polyline(img, pts, CYAN, 6, 16, 12)
    for x, y in rings:
        ring(img, x, y, 20, 7, WHITE)
    square(img, fill_at[0], fill_at[1], 16, WHITE)

    tag(img, cross_box, cross_lines, face)
    tag(img, fill_box, fill_lines, face)

    # Straight down. The tip overlaps the mark.
    ring_tip = (ring_x, ring_target[1] - 15)
    square_tip = (fill_x, fill_at[1] - 8)
    arrow(img, (ring_x, cross_box[3]), ring_tip)
    arrow(img, (fill_x, fill_box[3]), square_tip)

    stamp(img, 1268, 860)
    headline(
        img,
        108,
        108,
        [("THIS CHART IS ", WHITE), ("MADE UP", CYAN)],
        font(FONT_BOLD, 52),
    )
    final = finish(img)
    m = margins(final)
    print("011 margins L/R/T/B", m)
    if m[0] < 80 or m[1] < 80 or m[2] < 90 or m[3] < 90:
        raise SystemExit(f"011 margin fail {m}")
    assert_tip(final, (int(round(ring_tip[0])), int(round(ring_tip[1]))), ring_target, "cross ring")
    assert_tip(final, (int(round(square_tip[0])), int(round(square_tip[1]))), fill_at, "fill square")
    return final


def render_014() -> Image.Image:
    img = new_canvas()
    draw_grid(img)
    draw_bokeh(img)
    face = font(FONT_SEMI, 44)
    labels = [
        "Orders wait",
        "Inside your range",
        "Stop: your rule if price leaves",
        "What you hold changes",
    ]
    tops = [210, 380, 550, 720]
    for text, top in zip(labels, tops):
        rounded_glow(
            img,
            [px(140), px(top), px(1396), px(top + 140)],
            radius=px(22),
            fill=(7, 16, 34, 230),
            outline=CYAN + (255,),
            glow=(0, 180, 230, 90),
            width=px(4),
        )
        tw = text_size(face, text)[0]
        if tw > px(1200):
            raise SystemExit(f"014 text overflow {text!r} {tw}")
        draw = ImageDraw.Draw(img)
        bb = face.getbbox(text)
        tx = px(768) - (bb[2] - bb[0]) // 2 - bb[0]
        ty = px(top + 70) - (bb[3] - bb[1]) // 2 - bb[1]
        draw.text((tx, ty), text, font=face, fill=WHITE)
    stamp(img, 1320, 150)
    headline(
        img,
        108,
        96,
        [("THE WHOLE IDEA IN ", WHITE), ("ONE", CYAN), (" BREATH", WHITE)],
        font(FONT_BOLD, 40),
    )
    final = finish(img)
    m = margins(final)
    print("014 margins L/R/T/B", m)
    if m[0] < 80 or m[1] < 80 or m[2] < 90 or m[3] < 90:
        raise SystemExit(f"014 margin fail {m}")
    return final


def main() -> None:
    im011 = render_011()
    im014 = render_014()
    im011.save(OUT_011, "PNG")
    im014.save(OUT_014, "PNG")
    print("wrote", OUT_011)
    print("wrote", OUT_014)


if __name__ == "__main__":
    main()
