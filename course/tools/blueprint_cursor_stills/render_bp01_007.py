#!/usr/bin/env python3
"""Draw BP-01 beat 007: four sell rungs above the mark, four buy rungs below.

Arrow tips are placed on the rung stroke so no navy gap remains.
"""

from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "course/images/bp-01-introduction/007.png"

W, H = 1536, 1024
S = 2  # draw at 2x, then downscale

NAVY_TOP = (5, 10, 24)
NAVY_BOT = (8, 18, 40)
CYAN = (0, 212, 255)
BLUE = (30, 123, 255)
MINT = (79, 209, 165)
WHITE = (244, 248, 252)
INK = (8, 14, 28)

FONT_BOLD = "/usr/share/fonts/truetype/macos/Inter-Bold.ttf"
FONT_SEMI = "/usr/share/fonts/truetype/macos/Inter-SemiBold.ttf"


def px(n: float) -> int:
    return int(round(n * S))


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def new_canvas() -> Image.Image:
    img = Image.new("RGB", (px(W), px(H)), NAVY_TOP)
    draw = ImageDraw.Draw(img)
    for y in range(px(H)):
        t = y / px(H)
        # slight vignette toward the corners via a vertical ramp only
        draw.line([(0, y), (px(W), y)], fill=lerp(NAVY_TOP, NAVY_BOT, t * 0.85))
    return img


def draw_grid(base: Image.Image) -> None:
    overlay = Image.new("RGBA", base.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    step = px(56)
    color = (120, 170, 210, 18)
    for x in range(0, base.size[0], step):
        d.line([(x, 0), (x, base.size[1])], fill=color, width=S)
    for y in range(0, base.size[1], step):
        d.line([(0, y), (base.size[0], y)], fill=color, width=S)
    base.paste(Image.alpha_composite(base.convert("RGBA"), overlay).convert("RGB"))


def draw_bokeh(base: Image.Image) -> None:
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    spots = [
        (220, 180, 90, (0, 160, 220, 28)),
        (1280, 240, 120, (20, 80, 180, 26)),
        (1180, 820, 100, (0, 140, 200, 22)),
        (360, 860, 80, (30, 70, 160, 20)),
    ]
    for x, y, r, col in spots:
        d.ellipse([px(x - r), px(y - r), px(x + r), px(y + r)], fill=col)
    layer = layer.filter(ImageFilter.GaussianBlur(radius=px(18)))
    base.paste(Image.alpha_composite(base.convert("RGBA"), layer).convert("RGB"))


def rounded_glow(base: Image.Image, box, radius, fill, outline, glow, width) -> None:
    glow_layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow_layer)
    gd.rounded_rectangle(box, radius=radius, outline=glow, width=width + px(6))
    glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(radius=px(10)))
    body = Image.new("RGBA", base.size, (0, 0, 0, 0))
    bd = ImageDraw.Draw(body)
    bd.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)
    # soft inner top sheen
    x0, y0, x1, y1 = box
    sheen = Image.new("RGBA", base.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(sheen)
    sd.rounded_rectangle(
        [x0 + px(3), y0 + px(3), x1 - px(3), y0 + px(28)],
        radius=radius,
        fill=(180, 230, 255, 22),
    )
    composed = Image.alpha_composite(base.convert("RGBA"), glow_layer)
    composed = Image.alpha_composite(composed, body)
    composed = Image.alpha_composite(composed, sheen)
    base.paste(composed.convert("RGB"))


def line_glow(base: Image.Image, p0, p1, color, core, glow_rgba, width) -> None:
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.line([p0, p1], fill=glow_rgba, width=width + px(10))
    # round caps
    r = (width + px(10)) // 2
    for p in (p0, p1):
        d.ellipse([p[0] - r, p[1] - r, p[0] + r, p[1] + r], fill=glow_rgba)
    layer = layer.filter(ImageFilter.GaussianBlur(radius=px(4)))
    core_layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    cd = ImageDraw.Draw(core_layer)
    cd.line([p0, p1], fill=color + (255,), width=width)
    cr = width // 2
    for p in (p0, p1):
        cd.ellipse([p[0] - cr, p[1] - cr, p[0] + cr, p[1] + cr], fill=color + (255,))
    out = Image.alpha_composite(base.convert("RGBA"), layer)
    out = Image.alpha_composite(out, core_layer)
    base.paste(out.convert("RGB"))


def dashed_line(base: Image.Image, x0, x1, y, color, width, dash, gap) -> None:
    """Dashes begin at x0 so the left end is a solid dash the arrow can land on."""
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    x = x0
    while x < x1:
        end = min(x + dash, x1)
        d.line([(x, y), (end, y)], fill=color + (255,), width=width)
        r = max(1, width // 2)
        d.ellipse([x - r, y - r, x + r, y + r], fill=color + (255,))
        d.ellipse([end - r, y - r, end + r, y + r], fill=color + (255,))
        x = end + gap
    glow = layer.filter(ImageFilter.GaussianBlur(radius=px(3)))
    # recolor glow toward cyan-white
    out = Image.alpha_composite(base.convert("RGBA"), glow)
    out = Image.alpha_composite(out, layer)
    base.paste(out.convert("RGB"))


def dot(base: Image.Image, cx, cy, color) -> None:
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    r = px(11)
    d.ellipse([cx - r - px(4), cy - r - px(4), cx + r + px(4), cy + r + px(4)], fill=color + (90,))
    layer = layer.filter(ImageFilter.GaussianBlur(radius=px(3)))
    core = Image.new("RGBA", base.size, (0, 0, 0, 0))
    cd = ImageDraw.Draw(core)
    cd.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color + (255,))
    # lighter core so the dot reads as an order marker, not a second line
    ir = px(5)
    light = tuple(min(255, c + 50) for c in color)
    cd.ellipse([cx - ir, cy - ir, cx + ir, cy + ir], fill=light + (255,))
    out = Image.alpha_composite(base.convert("RGBA"), layer)
    out = Image.alpha_composite(out, core)
    base.paste(out.convert("RGB"))


def text_size(font: ImageFont.FreeTypeFont, text: str) -> tuple[int, int]:
    box = font.getbbox(text)
    return box[2] - box[0], box[3] - box[1]


def draw_tag(base: Image.Image, right: int, cy: int, text: str, font, width: int) -> tuple[int, int, int, int]:
    tw, th = text_size(font, text)
    pad_y = px(14)
    h = th + pad_y * 2
    left = right - width
    top = cy - h // 2
    bottom = top + h
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    radius = px(14)
    d.rounded_rectangle(
        [left, top, right, bottom],
        radius=radius,
        fill=(6, 14, 28, 235),
        outline=CYAN + (255,),
        width=px(3),
    )
    base.paste(Image.alpha_composite(base.convert("RGBA"), layer).convert("RGB"))
    draw = ImageDraw.Draw(base)
    # optically center using the font bbox
    box = font.getbbox(text)
    tx = left + (width - (box[2] - box[0])) // 2 - box[0]
    ty = cy - (box[1] + box[3]) // 2
    draw.text((tx, ty), text, font=font, fill=WHITE)
    return left, top, right, bottom


def h_arrow(base: Image.Image, x0: int, tip_x: int, y: int) -> None:
    """Horizontal cyan arrow. tip_x is inside the target stroke, not at its edge."""
    head = px(18)
    half = px(7)
    shaft_w = px(6)
    color = CYAN + (255,)
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    shaft_end = tip_x - head + px(8)
    d.rectangle(
        [x0, y - shaft_w // 2, shaft_end, y + shaft_w // 2],
        fill=color,
    )
    d.polygon(
        [(tip_x, y), (tip_x - head, y - half), (tip_x - head, y + half)],
        fill=color,
    )
    base.paste(Image.alpha_composite(base.convert("RGBA"), layer).convert("RGB"))


def draw_headline(base: Image.Image, x: int, y: int, font) -> None:
    parts = [
        ("BUY ORDERS ", WHITE),
        ("BELOW", CYAN),
        (", SELL ORDERS ", WHITE),
        ("ABOVE", CYAN),
    ]
    draw = ImageDraw.Draw(base)
    cursor = x
    for text, color in parts:
        draw.text((cursor, y), text, font=font, fill=color)
        cursor += font.getlength(text)


def draw_stamp(base: Image.Image, cx: int, cy: int, font) -> None:
    text = "EXAMPLE"
    tw, th = text_size(font, text)
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
    box = font.getbbox(text)
    tx = px(4) + pad_x - box[0]
    ty = px(4) + (h - (box[3] - box[1])) // 2 - box[1]
    d.text((tx, ty), text, font=font, fill=CYAN)
    tile = tile.rotate(8, expand=True, resample=Image.Resampling.BICUBIC)
    dest_x = cx - tile.size[0] // 2
    dest_y = cy - tile.size[1] // 2
    base.paste(Image.alpha_composite(base.convert("RGBA"), _paste_at(base.size, tile, dest_x, dest_y)).convert("RGB"))


def _paste_at(size, tile, x, y) -> Image.Image:
    layer = Image.new("RGBA", size, (0, 0, 0, 0))
    layer.paste(tile, (x, y), tile)
    return layer


def render() -> Image.Image:
    img = new_canvas()
    draw_grid(img)
    draw_bokeh(img)

    card = [px(108), px(206), px(1428), px(918)]
    rounded_glow(
        img,
        card,
        radius=px(28),
        fill=(7, 16, 34, 228),
        outline=CYAN + (255,),
        glow=(0, 180, 230, 110),
        width=px(4),
    )

    # Ladder geometry in final pixels, then scaled.
    rung_left, rung_right = 700, 1120
    gap = 68
    price_y = 548
    # index 0 is the top mint rung
    ys = [price_y + (i - 4) * gap for i in range(9)]
    # ys[0..3] mint, ys[4] price, ys[5..8] blue

    for i in range(4):
        y = ys[i]
        line_glow(
            img,
            (px(rung_left), px(y)),
            (px(rung_right), px(y)),
            MINT,
            core=MINT,
            glow_rgba=MINT + (120,),
            width=px(12),
        )
        dot(img, px((rung_left + rung_right) / 2), px(y), MINT)
    dashed_line(
        img,
        px(rung_left),
        px(rung_right),
        px(ys[4]),
        WHITE,
        width=px(10),
        dash=px(22),
        gap=px(14),
    )
    for i in range(4):
        y = ys[5 + i]
        line_glow(
            img,
            (px(rung_left), px(y)),
            (px(rung_right), px(y)),
            BLUE,
            core=BLUE,
            glow_rgba=BLUE + (130,),
            width=px(12),
        )
        dot(img, px((rung_left + rung_right) / 2), px(y), BLUE)

    label_font = ImageFont.truetype(FONT_SEMI, px(34))
    labels = [
        ("Sell orders above", ys[1]),  # second mint rung from the top
        ("Price now", ys[4]),
        ("Buy orders below", ys[6]),  # second blue rung from the top
    ]
    widest = max(text_size(label_font, t)[0] for t, _ in labels)
    tag_w = widest + px(36)
    # Tip sits 16px inside the stroke so the head overlaps the cap, not the empty ground.
    overlap = 16
    tip_x = px(rung_left + overlap)
    arrow_span = px(64)
    tag_right = tip_x - arrow_span
    for text, y in labels:
        draw_tag(img, tag_right, px(y), text, label_font, tag_w)
        # shaft starts 2px inside the tag border so it meets the border
        h_arrow(img, tag_right - px(2), tip_x, px(y))

    stamp_font = ImageFont.truetype(FONT_BOLD, px(28))
    draw_stamp(img, px(1268), px(840), stamp_font)

    head_font = ImageFont.truetype(FONT_BOLD, px(52))
    draw_headline(img, px(108), px(102), head_font)

    final = img.resize((W, H), Image.Resampling.LANCZOS)
    return final


def luminance(p) -> float:
    return 0.2126 * p[0] + 0.7152 * p[1] + 0.0722 * p[2]


def is_navy_gap(p) -> bool:
    """Dark background with no coloured stroke. Glow and strokes fail this test."""
    return luminance(p) < 26 and p[1] < 32 and p[2] < 48


def verify(im: Image.Image) -> None:
    if im.size != (W, H):
        raise SystemExit(f"size {im.size}")
    pxls = im.load()

    # Content margins. Ignore the faint grid (low luminance).
    min_x, min_y, max_x, max_y = W, H, 0, 0
    for y in range(H):
        for x in range(W):
            if luminance(pxls[x, y]) > 42:
                min_x = min(min_x, x)
                min_y = min(min_y, y)
                max_x = max(max_x, x)
                max_y = max(max_y, y)
    margins = (min_x, W - 1 - max_x, min_y, H - 1 - max_y)
    print("content margins L/R/T/B", margins)
    if min_x < 80 or (W - 1 - max_x) < 80 or min_y < 90 or (H - 1 - max_y) < 90:
        raise SystemExit(f"margin fail {margins}")

    # Expected geometry after downscale (integer round of the 2x coords).
    rung_left = 700
    gap = 68
    price_y = 548
    ys = [price_y + (i - 4) * gap for i in range(9)]
    tip_x = rung_left + 16
    targets = {
        "Sell orders above": ys[1],
        "Price now": ys[4],
        "Buy orders below": ys[6],
    }
    for name, y in targets.items():
        # The tip and the next 6px into the rung must not be navy.
        for x in range(tip_x - 1, tip_x + 8):
            p = pxls[x, y]
            if is_navy_gap(p):
                raise SystemExit(f"{name} navy gap at {(x, y)} rgb={p}")
        print(f"{name} tip rgb", [pxls[x, y][:3] for x in range(tip_x - 2, tip_x + 8)])

    # Sample the rung stroke left of the centre dot so the dot is not counted twice.
    sample_x = 760
    kinds = []
    for i, y in enumerate(ys):
        p = pxls[sample_x, y]
        if i < 4:
            kind = "mint"
            ok = p[1] > 160 and p[1] > p[2]
        elif i == 4:
            kind = "price"
            ok = p[0] > 200 and p[1] > 200 and p[2] > 200
        else:
            kind = "blue"
            ok = p[2] > 180 and p[2] > p[1]
        # The gap halfway to the next rung must be dark (a crossing is not a fill).
        if i < 8:
            gap_y = (y + ys[i + 1]) // 2
            gap = pxls[sample_x, gap_y]
            if luminance(gap) > 40:
                raise SystemExit(f"gap not empty at y={gap_y} rgb={gap}")
        kinds.append((kind, y, p, ok))
    print("rungs", kinds)
    if not all(ok for *_, ok in kinds):
        raise SystemExit("a rung is the wrong colour")
    print("verify ok")


def main() -> None:
    im = render()
    verify(im)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    im.save(OUT, "PNG")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
