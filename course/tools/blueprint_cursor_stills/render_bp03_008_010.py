#!/usr/bin/env python3
"""BP-03 beats 008 and 010 with the beginner wording from the b608319 re-check.

008: what you hold changes. No "balanced".
010: Top, Bottom, Levels, What you hold, Stop. No Upper/Lower/Side, no skip line.
"""

from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parent))
from render_bp01_007 import BLUE, CYAN, FONT_BOLD, FONT_SEMI, MINT, WHITE, px  # noqa: E402
from render_bp03_011_014 import (  # noqa: E402
    AMBER,
    arrow,
    assert_tip,
    dashed_polyline,
    finish,
    font,
    headline,
    hline,
    margins,
    paste_layer,
    rounded_glow,
    stamp,
    tag,
    text_size,
    new_canvas,
    draw_bokeh,
    draw_grid,
)

ROOT = Path(__file__).resolve().parents[3]
OUT_008 = ROOT / "course/images/bp-03-what-is-a-grid-bot/008.png"
OUT_010 = ROOT / "course/images/bp-03-what-is-a-grid-bot/010.png"


def bars(base, x, y, w, h, color) -> None:
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.rounded_rectangle(
        [px(x), px(y), px(x + w), px(y + h)],
        radius=px(10),
        fill=color + (255,),
    )
    paste_layer(base, layer)


def center_lines(base, box, lines, face) -> None:
    draw = ImageDraw.Draw(base)
    left, top, right, bottom = [px(v) for v in box]
    heights = [text_size(face, line)[1] for line in lines]
    gap = px(6)
    block = sum(heights) + gap * (len(lines) - 1)
    ty = (top + bottom) // 2 - block // 2
    for line, h in zip(lines, heights):
        bb = face.getbbox(line)
        tw = bb[2] - bb[0]
        if tw > (right - left - px(24)):
            raise SystemExit(f"008 text overflow {line!r} {tw}")
        tx = left + (right - left - tw) // 2 - bb[0]
        draw.text((tx, ty - bb[1]), line, font=face, fill=WHITE)
        ty += h + gap


def render_008() -> Image.Image:
    img = new_canvas()
    draw_grid(img)
    draw_bokeh(img)
    # Full-width boxes so the two sentences can sit on two large lines.
    cards = [(120, 210, 1416, 530), (120, 570, 1416, 900)]
    for box in cards:
        rounded_glow(
            img,
            [px(v) for v in box],
            radius=px(26),
            fill=(7, 16, 34, 230),
            outline=CYAN + (255,),
            glow=(0, 180, 230, 100),
            width=px(4),
        )

    def band_and_path(x0, x1, top, bot, pts):
        hline(img, x0, x1, top, CYAN, 6)
        hline(img, x0, x1, bot, CYAN, 6)
        layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(layer)
        d.line([(px(x), px(y)) for x, y in pts], fill=CYAN + (255,), width=px(6))
        paste_layer(img, layer)

    # Left of each box: the picture. Right: the sentence, large.
    band_and_path(
        170,
        520,
        270,
        390,
        [(190, 330), (260, 270), (340, 390), (420, 270), (500, 330)],
    )
    bars(img, 190, 420, 140, 50, BLUE)
    bars(img, 360, 420, 140, 50, MINT)

    band_and_path(
        170,
        520,
        630,
        750,
        [(190, 690), (270, 630), (350, 750), (430, 660), (500, 820)],
    )
    bars(img, 190, 790, 120, 70, BLUE)
    bars(img, 360, 836, 120, 24, MINT)

    face = font(FONT_SEMI, 48)
    center_lines(
        img,
        (560, 250, 1360, 490),
        ["Price bounces: coin and cash", "swap back and forth"],
        face,
    )
    center_lines(
        img,
        (560, 610, 1360, 860),
        ["Price leaves: mostly coin", "or mostly cash"],
        face,
    )
    stamp(img, 1320, 160)
    headline(
        img,
        108,
        96,
        [("WHAT YOU ", WHITE), ("HOLD", CYAN), (" CHANGES", WHITE)],
        font(FONT_BOLD, 44),
    )
    final = finish(img)
    m = margins(final)
    print("008 margins", m)
    if m[0] < 80 or m[1] < 80 or m[2] < 90 or m[3] < 90:
        raise SystemExit(f"008 margin fail {m}")
    return final


def render_010() -> Image.Image:
    img = new_canvas()
    draw_grid(img)
    draw_bokeh(img)

    # The band. Top and bottom are the edges. Levels are the inner rungs.
    left, right, top, bot = 470, 980, 360, 700
    rounded_glow(
        img,
        [px(left), px(top), px(right), px(bot)],
        radius=px(18),
        fill=(7, 16, 34, 210),
        outline=CYAN + (255,),
        glow=(0, 160, 210, 80),
        width=px(4),
    )
    levels = [450, 540, 620]
    for y in levels:
        hline(img, left + 30, right - 30, y, (150, 210, 230), 6)
    # Thicker top and bottom so the arrow has a solid stroke.
    hline(img, left + 20, right - 20, top + 8, CYAN, 8)
    hline(img, left + 20, right - 20, bot - 8, CYAN, 8)

    # What you hold: one blue stack and one mint stack. Not coins.
    stack_x = 1140
    for i in range(3):
        bars(img, stack_x, 620 - i * 34, 64, 26, BLUE)
    for i in range(2):
        bars(img, 1240, 620 - i * 34, 64, 26, MINT)

    # Stop sits under the Stop label, not across the Bottom arrow.
    hline(img, 140, 420, 740, AMBER, 12)

    face = font(FONT_SEMI, 36)
    labels = {
        "Top": (620, 230, 860, 310),
        "Bottom": (620, 800, 860, 880),
        "Levels": (108, 500, 400, 580),
        "What you hold": (1040, 250, 1420, 340),
        "Stop": (108, 800, 360, 880),
    }
    # Measure and shrink boxes to the text so they stay large but not huge empty plates.
    placed = {}
    for name, (x0, y0, x1, y1) in labels.items():
        tw = text_size(face, name)[0] / 2 + 48
        th = 78
        if name == "Top":
            box = ((left + right) / 2 - tw / 2, 248, (left + right) / 2 + tw / 2, 248 + th)
        elif name == "Bottom":
            box = ((left + right) / 2 - tw / 2, 800, (left + right) / 2 + tw / 2, 800 + th)
        elif name == "Levels":
            box = (108, 512, 108 + tw, 512 + th)
        elif name == "What you hold":
            box = (1428 - tw, 268, 1428, 268 + th)
        else:
            box = (108, 800, 108 + tw, 800 + th)
        placed[name] = box
        tag(img, box, [name], face)

    tips = {
        "Top": ((left + right) / 2, top + 8),
        "Bottom": ((left + right) / 2, bot - 8),
        "Levels": (left + 40, levels[1]),
        "What you hold": (stack_x + 32, 620 - 34 + 8),
        "Stop": (280, 740),
    }
    starts = {
        "Top": ((placed["Top"][0] + placed["Top"][2]) / 2, placed["Top"][3]),
        "Bottom": ((placed["Bottom"][0] + placed["Bottom"][2]) / 2, placed["Bottom"][1]),
        "Levels": (placed["Levels"][2], (placed["Levels"][1] + placed["Levels"][3]) / 2),
        "What you hold": (placed["What you hold"][0], (placed["What you hold"][1] + placed["What you hold"][3]) / 2),
        "Stop": ((placed["Stop"][0] + placed["Stop"][2]) / 2, placed["Stop"][1]),
    }
    # Pull each tip a few pixels onto the stroke.
    tips["Top"] = (tips["Top"][0], tips["Top"][1] + 2)
    tips["Bottom"] = (tips["Bottom"][0], tips["Bottom"][1] - 2)
    tips["Levels"] = (tips["Levels"][0] + 6, tips["Levels"][1])
    tips["What you hold"] = (tips["What you hold"][0], tips["What you hold"][1] + 4)
    tips["Stop"] = (tips["Stop"][0], tips["Stop"][1] + 3)

    for name in tips:
        arrow(img, starts[name], tips[name])

    stamp(img, 1320, 820)
    headline(
        img,
        108,
        108,
        [("POINT AND SAY THE ", WHITE), ("FIVE", CYAN)],
        font(FONT_BOLD, 48),
    )
    final = finish(img)
    m = margins(final)
    print("010 margins", m)
    if m[0] < 80 or m[1] < 80 or m[2] < 90 or m[3] < 90:
        raise SystemExit(f"010 margin fail {m}")
    toward = {
        "Top": (tips["Top"][0], tips["Top"][1] + 10),
        "Bottom": (tips["Bottom"][0], tips["Bottom"][1] - 10),
        "Levels": (tips["Levels"][0] + 12, tips["Levels"][1]),
        "What you hold": (tips["What you hold"][0] + 10, tips["What you hold"][1]),
        "Stop": (tips["Stop"][0], tips["Stop"][1] + 6),
    }
    for name, tip in tips.items():
        assert_tip(final, (int(round(tip[0])), int(round(tip[1]))), toward[name], name)
    return final


def main() -> None:
    render_008().save(OUT_008, "PNG")
    render_010().save(OUT_010, "PNG")
    print("wrote", OUT_008)
    print("wrote", OUT_010)


if __name__ == "__main__":
    main()
