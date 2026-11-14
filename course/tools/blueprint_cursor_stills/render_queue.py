#!/usr/bin/env python3
"""Cursor stills for Blueprint BP-04 to BP-11. Status stays awaiting Creative Studio."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parent))
from render_bp01_007 import BLUE, CYAN, FONT_BOLD, FONT_SEMI, MINT, WHITE, px  # noqa: E402
from render_bp03_011_014 import (  # noqa: E402
    AMBER,
    arrow,
    assert_tip,
    draw_bokeh,
    draw_grid,
    finish,
    font,
    headline,
    hline,
    margins,
    new_canvas,
    paste_layer,
    rounded_glow,
    stamp,
    tag,
)

ROOT = Path(__file__).resolve().parents[3]
MANIFEST = ROOT / "course/images/FALLBACK_MANIFEST.json"


def canvas():
    img = new_canvas()
    draw_grid(img)
    draw_bokeh(img)
    return img


def card(img, box) -> None:
    rounded_glow(
        img,
        [px(v) for v in box],
        radius=px(24),
        fill=(7, 16, 34, 230),
        outline=CYAN + (255,),
        glow=(0, 170, 220, 90),
        width=px(4),
    )


def solid(img, pts, color=CYAN, width=6) -> None:
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.line([(px(x), px(y)) for x, y in pts], fill=color + (255,), width=px(width))
    paste_layer(img, layer)


def block(img, x, y, w, h, color) -> None:
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.rounded_rectangle([px(x), px(y), px(x + w), px(y + h)], radius=px(8), fill=color + (255,))
    paste_layer(img, layer)


def cross_mark(img, x, y, size=28, color=AMBER) -> None:
    solid(img, [(x - size, y - size), (x + size, y + size)], color, 6)
    solid(img, [(x - size, y + size), (x + size, y - size)], color, 6)


def head(img, text: str, cyan: str, y=100, size=46) -> None:
    face = font(FONT_BOLD, size)
    if cyan and cyan in text:
        i = text.index(cyan)
        parts = [(text[:i], WHITE), (cyan, CYAN), (text[i + len(cyan):], WHITE)]
    else:
        parts = [(text, WHITE)]
    headline(img, 100, y, parts, face)


def rows(img, lines: list[str], y0=250, size=36) -> None:
    face = font(FONT_SEMI, size)
    gap = 16
    h = 78 if size >= 34 else 68
    for i, line in enumerate(lines):
        top = y0 + i * (h + gap)
        tag(img, (120, top, 1416, top + h), [line], face)


def save(img, rel: str) -> Image.Image:
    final = finish(img)
    m = margins(final)
    if m[0] < 80 or m[1] < 80 or m[2] < 90 or m[3] < 90:
        raise SystemExit(f"margin {rel} {m}")
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    final.save(path, "PNG")
    print(rel, m)
    return final


def record(items: list[dict]) -> None:
    data = json.loads(MANIFEST.read_text())
    by_path = {row.get("path"): row for row in data["images"]}
    for item in items:
        rel = item["path"]
        digest = hashlib.md5((ROOT / rel).read_bytes()).hexdigest()
        row = by_path.get(rel)
        if row is None:
            row = {
                "id": item["lesson"] + "-" + Path(rel).stem,
                "lesson": item["lesson"],
                "shot": Path(rel).stem,
                "path": rel,
                "width": 1536,
                "height": 1024,
                "format": "png",
                "palette": "cyan",
                "style": "gbb-v3",
                "marker": "FALLBACK",
            }
            data["images"].append(row)
            by_path[rel] = row
        previous = row.get("md5")
        rebuilt = {}
        for key, value in row.items():
            if key in {"source", "shows", "alt"}:
                continue
            rebuilt[key] = value
            if key == "lesson":
                rebuilt["source"] = "cursor"
                rebuilt["shows"] = item["shows"]
                rebuilt["alt"] = item["alt"]
        rebuilt["status"] = "awaiting_qa"
        rebuilt["qa_reason"] = "Cursor redraw 14 Nov 2026. Awaiting Creative Studio. Not a pass."
        rebuilt["source_batch"] = item.get("batch", "cursor")
        rebuilt["previous_status"] = row.get("status", "pass")
        rebuilt["md5"] = digest
        rebuilt["previous_md5"] = previous
        row.clear()
        row.update(rebuilt)
    MANIFEST.write_text(json.dumps(data, indent=1) + "\n")


def bp04_006() -> None:
    img = canvas()
    head(img, "A CROSS IS NOT A FILL", "CROSS", size=48)
    card(img, (96, 300, 1440, 920))
    for y in (430, 590, 750):
        hline(img, 180, 1320, y, (120, 190, 210), 5)
    solid(img, [(220, 510), (420, 430), (640, 670), (860, 590), (1100, 750), (1280, 640)])
    # Ring on the top touch. Square where an order trades.
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    for rx, ry in ((420, 430), (567, 590), (860, 590)):
        d.ellipse([px(rx - 22), px(ry - 22), px(rx + 22), px(ry + 22)], outline=WHITE + (255,), width=px(7))
    d.rounded_rectangle([px(1100 - 16), px(750 - 16), px(1100 + 16), px(750 + 16)], radius=px(4), fill=WHITE + (255,))
    paste_layer(img, layer)
    face = font(FONT_SEMI, 32)
    tag(img, (150, 320, 620, 400), ["Cross: price touches a line"], face)
    tag(img, (860, 800, 1380, 880), ["Fill: an order trades"], face)
    arrow(img, (385, 400), (420, 412))
    arrow(img, (1100, 800), (1100, 758))
    stamp(img, 1260, 500)
    final = save(img, "course/images/bp-04-market-regimes/006.png")
    assert_tip(final, (420, 412), (420, 430), "cross")
    assert_tip(final, (1100, 758), (1100, 742), "fill")
    record([{
        "path": "course/images/bp-04-market-regimes/006.png",
        "lesson": "bp-04-market-regimes",
        "shows": "A made-up path touching rungs. A ring is a cross, where price only touches a line. A square is a fill, where an order trades.",
        "alt": "A ring means the price touched a line. A square means an order trades. A cross is not a fill.",
        "batch": "cursor-bp04",
    }])


def bp04_007() -> None:
    img = canvas()
    head(img, "TREND: KEEPS GOING ONE WAY", "ONE WAY", size=42)
    card(img, (96, 240, 1440, 900))
    pts = [(180, 780), (360, 660), (500, 730), (720, 540), (860, 610), (1100, 400), (1280, 470)]
    solid(img, pts, width=7)
    face = font(FONT_SEMI, 32)
    tag(img, (860, 250, 1340, 330), ["Higher highs"], face)
    tag(img, (140, 760, 560, 840), ["Small pullbacks"], face)
    arrow(img, (1100, 330), (1100, 402))
    arrow(img, (500, 760), (500, 728))
    stamp(img, 240, 300)
    final = save(img, "course/images/bp-04-market-regimes/007.png")
    assert_tip(final, (1100, 402), (1108, 405), "high")
    assert_tip(final, (500, 728), (508, 720), "dip")
    record([{
        "path": "course/images/bp-04-market-regimes/007.png",
        "lesson": "bp-04-market-regimes",
        "shows": "A path that keeps rising, with higher peaks and small dips between them.",
        "alt": "A trend keeps going one way, with higher highs and small pullbacks.",
        "batch": "cursor-bp04",
    }])


def bp04_011() -> None:
    img = canvas()
    head(img, "BAND TOO TIGHT FOR A NORMAL DAY", "TOO TIGHT", size=40)
    card(img, (120, 250, 700, 860))
    card(img, (760, 250, 1420, 860))
    hline(img, 200, 620, 480, CYAN, 6)
    hline(img, 200, 620, 560, CYAN, 6)
    # Normal move is much taller than that band.
    solid(img, [(900, 700), (1040, 340), (1180, 700)], width=7)
    face = font(FONT_SEMI, 34)
    tag(img, (180, 680, 640, 780), ["Your band"], face)
    tag(img, (860, 740, 1340, 830), ["Normal up-and-down"], face)
    arrow(img, (400, 680), (400, 559))
    arrow(img, (1040, 748), (1040, 348))
    stamp(img, 1260, 300)
    final = save(img, "course/images/bp-04-market-regimes/011.png")
    assert_tip(final, (400, 559), (450, 560), "band")
    assert_tip(final, (1040, 348), (1000, 420), "wave")
    record([{
        "path": "course/images/bp-04-market-regimes/011.png",
        "lesson": "bp-04-market-regimes",
        "shows": "A short band beside a much taller normal up-and-down move, so the band is too tight for a normal day.",
        "alt": "Your band is shorter than a normal day's up-and-down move, so the band is too tight.",
        "batch": "cursor-bp04",
    }])


def lesson_bp04() -> None:
    bp04_006()
    bp04_007()
    bp04_011()


def ladder(img, x, y0, gap, n, length=280) -> None:
    for i in range(n):
        hline(img, x, x + length, y0 + i * gap, CYAN, 5)


def bp05_015() -> None:
    img = canvas()
    head(img, "RECAP", "RECAP", size=52)
    card(img, (96, 220, 560, 900))
    ladder(img, 160, 280, 70, 7, 280)
    face = font(FONT_SEMI, 32)
    tag(img, (150, 780, 500, 860), ["7 lines, 6 gaps"], face)
    rows(img, ["Range first", "Count gaps, not lines", "Gap vs fee", "One change at a time"], y0=250, size=32)
    # rows() draws full width and would cover the ladder. Draw the phrases on the right instead.
    # The call above already painted full-width rows over the ladder. Redo is cleaner.
    final_unused = img
    del final_unused
    img = canvas()
    head(img, "RECAP", "RECAP", size=52)
    card(img, (100, 230, 520, 900))
    ladder(img, 160, 300, 62, 7, 260)
    tag(img, (140, 760, 480, 850), ["7 lines, 6 gaps"], font(FONT_SEMI, 32))
    phrases = ["Range first", "Count gaps, not lines", "Gap vs fee", "One change at a time"]
    face = font(FONT_SEMI, 32)
    for i, line in enumerate(phrases):
        top = 250 + i * 150
        tag(img, (580, top, 1420, top + 110), [line], face)
    stamp(img, 1200, 880)
    save(img, "course/images/bp-05-spacing-and-range/015.png")
    record([{
        "path": "course/images/bp-05-spacing-and-range/015.png",
        "lesson": "bp-05-spacing-and-range",
        "shows": "A recap beside the house example: 7 lines and 6 gaps. The four lines are range first, count gaps not lines, gap versus fee, and one change at a time.",
        "alt": "Recap: range first, count gaps not lines, check the gap against the fee, and change one thing at a time. The example has 7 lines and 6 gaps.",
        "batch": "cursor-bp05",
    }])


def lesson_bp05() -> None:
    bp05_015()


def leave_picture(img, box) -> None:
    x0, y0, x1, y1 = box
    card(img, box)
    top = y0 + 80
    bot = y0 + 200
    hline(img, x0 + 40, x1 - 40, top, CYAN, 5)
    hline(img, x0 + 40, x1 - 40, bot, CYAN, 5)
    solid(img, [
        (x0 + 70, (top + bot) // 2),
        (x0 + 160, top),
        (x0 + 250, bot),
        (x0 + 340, bot + 90),
        (x1 - 50, bot + 110),
    ])


def bp06() -> None:
    specs = [
        ("006", "FINISH RULE: PRICE LEAVES AND DOESN'T COME BACK", "DOESN'T COME BACK",
         "Price leaves the band and stays outside.",
         "The finish rule: price leaves the band and does not come back."),
        ("010", "INVALIDATION = WHERE YOUR IDEA IS PROVEN WRONG", "PROVEN WRONG",
         "The point where the idea you wrote is proven wrong.",
         "Invalidation means the point where your idea is proven wrong."),
        ("012", "COPY THE FINISH RULE FIRST", "FINISH RULE",
         "Write the finish rule before the start rule.",
         "Copy the finish rule first, before the start rule."),
        ("014", "WRITE BOTH RULES TODAY, FINISH FIRST", "FINISH FIRST",
         "Write the finish rule and the start rule today. Finish comes first.",
         "Write both rules today, and write the finish rule first."),
        ("019", "CAN A CLASSMATE POINT AT YOUR FINISH RULE?", "FINISH RULE",
         "The finish rule is clear enough for someone else to point at it.",
         "Can a classmate point at your finish rule?"),
    ]
    for num, title, cyan, shows, alt in specs:
        img = canvas()
        size = 36 if len(title) < 42 else 32
        head(img, title, cyan, size=size)
        if num in {"006", "010", "019"}:
            leave_picture(img, (160, 280, 1370, 860))
            face = font(FONT_SEMI, 32)
            if num == "006":
                tag(img, (220, 700, 720, 800), ["Price leaves"], face)
                tag(img, (780, 700, 1300, 800), ["Doesn't come back"], face)
                arrow(img, (470, 700), (410, 480))
                arrow(img, (1040, 700), (1000, 582))
            elif num == "010":
                tag(img, (360, 700, 1160, 800), ["Your idea is proven wrong"], face)
                arrow(img, (760, 700), (410, 480))
            else:
                tag(img, (300, 700, 1220, 800), ["Point at this leaving path"], face)
                arrow(img, (760, 700), (410, 480))
            stamp(img, 1240, 340)
        elif num == "012":
            face = font(FONT_SEMI, 34)
            tag(img, (160, 300, 1370, 460), ["1  Finish rule"], face)
            tag(img, (160, 520, 1370, 680), ["2  Start rule"], face)
            stamp(img, 1240, 760)
        else:
            face = font(FONT_SEMI, 34)
            tag(img, (160, 280, 760, 480), ["Finish rule", "Write this first"], face)
            tag(img, (800, 520, 1400, 720), ["Start rule", "Write this second"], face)
            arrow(img, (760, 380), (802, 562))
            stamp(img, 280, 760)
        rel = f"course/images/bp-06-entry-and-exit/{num}.png"
        final = save(img, rel)
        if num == "006":
            assert_tip(final, (410, 480), (410, 450), "leaves")
            assert_tip(final, (1000, 582), (1100, 584), "stays")
        record([{
            "path": rel,
            "lesson": "bp-06-entry-and-exit",
            "shows": shows,
            "alt": alt,
            "batch": "cursor-bp06",
        }])


def form_fields(img, x, y, w) -> None:
    face = font(FONT_SEMI, 34)
    labels = ["Pair", "Top", "Bottom", "Gap count", "Your two rules"]
    for i, line in enumerate(labels):
        top = y + i * 110
        tag(img, (x, top, x + w, top + 90), [line], face)


def bp07() -> None:
    img = canvas()
    head(img, "FIVE BOXES TO COPY", "FIVE", size=48)
    form_fields(img, 280, 240, 980)
    stamp(img, 1280, 200)
    save(img, "course/images/bp-07-spot-paper-trading/005.png")
    record([{
        "path": "course/images/bp-07-spot-paper-trading/005.png",
        "lesson": "bp-07-spot-paper-trading",
        "shows": "Five boxes to copy: pair, top, bottom, gap count, and your two rules. The word lines is not a field.",
        "alt": "Copy five fields: pair, top, bottom, gap count, and your two rules.",
        "batch": "cursor-bp07",
    }])
    img = canvas()
    head(img, "IF A LABEL DIFFERS, USE THESE", "THESE", size=42)
    form_fields(img, 280, 240, 980)
    stamp(img, 1280, 200)
    save(img, "course/images/bp-07-spot-paper-trading/019.png")
    record([{
        "path": "course/images/bp-07-spot-paper-trading/019.png",
        "lesson": "bp-07-spot-paper-trading",
        "shows": "If a screen label differs, use these five: pair, top, bottom, gap count, and your two rules.",
        "alt": "If a label on the screen differs, translate it to pair, top, bottom, gap count, and your two rules.",
        "batch": "cursor-bp07",
    }])


def lesson_bp05() -> None:
    bp05_015()


def center_lines(img, box, lines, face, fill=WHITE) -> None:
    draw = ImageDraw.Draw(img)
    left, top, right, bottom = [px(v) for v in box]
    heights = [font_box(face, line)[1] for line in lines]
    gap = px(8)
    block_h = sum(heights) + gap * (len(lines) - 1)
    ty = (top + bottom) // 2 - block_h // 2
    for line, h in zip(lines, heights):
        bb = face.getbbox(line)
        tw = bb[2] - bb[0]
        if tw > right - left - px(20):
            raise SystemExit(f"text overflow {line!r}")
        tx = left + (right - left - tw) // 2 - bb[0]
        draw.text((tx, ty - bb[1]), line, font=face, fill=fill)
        ty += h + gap


def font_box(face, line):
    bb = face.getbbox(line)
    return bb[2] - bb[0], bb[3] - bb[1]


def outline_box(img, box, width=8) -> None:
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.rounded_rectangle(
        [px(v) for v in box],
        radius=px(16),
        outline=CYAN + (255,),
        width=px(width),
    )
    paste_layer(img, layer)


def draw_lock(img, box) -> None:
    x0, y0, x1, y1 = box
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.rounded_rectangle(
        [px(x0), px(y0), px(x1), px(y1)],
        radius=px(22),
        fill=(7, 16, 34, 255),
        outline=CYAN + (255,),
        width=px(12),
    )
    inset = (x1 - x0) * 0.22
    # The arc's ends sit on the top stroke, so the shackle is part of the lock.
    mid = y0 + 8
    d.arc(
        [px(x0 + inset), px(mid - 180), px(x1 - inset), px(mid + 180)],
        180,
        360,
        fill=CYAN + (255,),
        width=px(14),
    )
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2 + 16
    d.ellipse(
        [px(cx - 16), px(cy - 22), px(cx + 16), px(cy + 10)],
        outline=CYAN + (255,),
        width=px(8),
    )
    d.rounded_rectangle(
        [px(cx - 7), px(cy - 2), px(cx + 7), px(cy + 36)],
        radius=px(4),
        fill=CYAN + (255,),
    )
    paste_layer(img, layer)


def bp02_008() -> None:
    img = canvas()
    head(img, "NEVER WRITE DOWN OR TYPE A SECRET", "SECRET", size=34)
    # One lock. The rule is the headline. The line under it names the three.
    draw_lock(img, (640, 400, 900, 700))
    face = font(FONT_SEMI, 32)
    tag(img, (300, 780, 1240, 880), ["Seed phrase, private key, API secret"], face)
    arrow(img, (770, 780), (770, 694))
    final = save(img, "course/images/bp-02-what-you-need/008.png")
    assert_tip(final, (770, 694), (770, 700), "lock")
    record([{
        "path": "course/images/bp-02-what-you-need/008.png",
        "lesson": "bp-02-what-you-need",
        "shows": "One lock. The rule is never write down or type a secret. A line names the seed phrase, the private key, and the API secret.",
        "alt": "Never write down or type a secret: a seed phrase, a private key, or an API secret.",
        "batch": "cursor-bp02-008",
    }])


def bp02_012() -> None:
    img = canvas()
    head(img, "THE FORM COPIES YOUR PAGE", "COPIES", size=44)
    card(img, (120, 280, 700, 780))
    card(img, (836, 280, 1416, 780))
    face = font(FONT_SEMI, 44)
    center_lines(img, (150, 360, 670, 700), ["1. Write it", "on paper"], face)
    center_lines(img, (866, 360, 1386, 700), ["2. Copy it into", "the form later"], face)
    # Right card left stroke is x=836. Tip sits 4px inside it.
    arrow(img, (700, 530), (840, 530))
    final = save(img, "course/images/bp-02-what-you-need/012.png")
    assert_tip(final, (840, 530), (836, 530), "form")
    record([{
        "path": "course/images/bp-02-what-you-need/012.png",
        "lesson": "bp-02-what-you-need",
        "shows": "Two plain cards and one arrow. Write it on paper, then copy it into the form later.",
        "alt": "Write it on paper first. Copy it into the form later.",
        "batch": "cursor-bp02-012",
    }])


def bp02_014() -> None:
    img = canvas()
    head(img, "AN EMPTY PAIR BLOCKS THE PAGE", "EMPTY", size=40)
    face = font(FONT_SEMI, 48)
    draw = ImageDraw.Draw(img)
    label = "Pair"
    bb = face.getbbox(label)
    draw.text((px(180), px(470) - bb[1]), label, font=face, fill=WHITE)
    # One blank row. Not a form.
    outline_box(img, (420, 420, 1320, 580), width=10)
    tag(img, (420, 680, 980, 800), ["Fill this in first"], font(FONT_SEMI, 40))
    # Blank row bottom stroke is y=580. Tip sits 4px inside it.
    arrow(img, (700, 680), (700, 576))
    stamp(img, 220, 860)
    final = save(img, "course/images/bp-02-what-you-need/014.png")
    assert_tip(final, (700, 576), (700, 580), "pair")
    record([{
        "path": "course/images/bp-02-what-you-need/014.png",
        "lesson": "bp-02-what-you-need",
        "shows": "One blank row labelled Pair. The arrow says to fill this in first.",
        "alt": "The pair row is blank. Fill this in first.",
        "batch": "cursor-bp02-014",
    }])


def bp03_009() -> None:
    img = canvas()
    head(img, "A FILL, THEN THE NEXT LINE", "NEXT LINE", size=42)
    ys = [360, 530, 700]
    for y in ys:
        hline(img, 160, 640, y, CYAN, 6)
    # A filled order on the middle line. A waiting order on the next line.
    block(img, 360, 490, 80, 80, CYAN)
    outline_box(img, (340, 660, 460, 740), width=8)
    face = font(FONT_SEMI, 40)
    center_lines(img, (720, 470, 1420, 590), ["An order fills"], face)
    center_lines(img, (720, 640, 1420, 800), ["A new order waits", "on the next line"], face)
    # Waiting box top stroke is y=660. Tip sits 4px inside it. One arrow, straight down.
    arrow(img, (400, 570), (400, 664))
    final = save(img, "course/images/bp-03-what-is-a-grid-bot/009.png")
    assert_tip(final, (400, 664), (400, 660), "next")
    record([{
        "path": "course/images/bp-03-what-is-a-grid-bot/009.png",
        "lesson": "bp-03-what-is-a-grid-bot",
        "shows": "One straight arrow. An order fills, then a new waiting order sits on the next line.",
        "alt": "An order fills, and a new order waits on the next line.",
        "batch": "cursor-bp03-009",
    }])


def beginner_six() -> None:
    bp02_008()
    bp02_012()
    bp02_014()
    bp03_009()
    from render_bp03_008_010 import OUT_008, render_008
    from render_bp03_011_014 import OUT_014, render_014

    render_008().save(OUT_008, "PNG")
    record([{
        "path": "course/images/bp-03-what-is-a-grid-bot/008.png",
        "lesson": "bp-03-what-is-a-grid-bot",
        "shows": "Two large boxes. Price bounces: coin and cash swap back and forth. Price leaves: mostly coin or mostly cash.",
        "alt": "When price bounces, coin and cash swap back and forth. When price leaves, you hold mostly coin or mostly cash.",
        "batch": "cursor-bp03-008",
    }])
    render_014().save(OUT_014, "PNG")
    record([{
        "path": "course/images/bp-03-what-is-a-grid-bot/014.png",
        "lesson": "bp-03-what-is-a-grid-bot",
        "shows": "Four large word labels: orders wait, inside your range, the stop is your rule if price leaves, and what you hold changes.",
        "alt": "Orders wait, inside your range, with a stop if price leaves, and what you hold changes.",
        "batch": "cursor-bp03-014",
    }])


def bp04_015() -> None:
    img = canvas()
    head(img, "SORT ONE CHART", "SORT", size=52)
    card(img, (160, 220, 1380, 920))
    # Handmade path: a sideways weave, no words on it.
    hline(img, 240, 700, 300, (90, 160, 190), 4)
    hline(img, 240, 700, 460, (90, 160, 190), 4)
    solid(img, [(260, 380), (360, 300), (460, 460), (560, 300), (660, 420)])
    # Three shape boxes. The first is ticked. Icons only, no extra words.
    boxes = [(760, 270, 940, 450), (980, 270, 1160, 450), (1200, 270, 1340, 450)]
    for i, (x0, y0, x1, y1) in enumerate(boxes):
        card(img, (x0, y0, x1, y1))
    # Icons: weave, staircase, drop.
    solid(img, [(790, 370), (840, 320), (890, 400), (920, 340)], width=4)
    solid(img, [(1010, 400), (1050, 330), (1090, 380), (1130, 320)], width=4)
    solid(img, [(1230, 320), (1270, 320), (1310, 410)], width=4)
    # Tick on the first box, drawn inside so it is not an arrow.
    solid(img, [(790, 400), (810, 420), (850, 360)], MINT, 5)
    face = font(FONT_SEMI, 32)
    tag(img, (170, 500, 520, 590), ["Pick one shape"], face)
    # Ticked box left stroke is x=780. Tip sits 2px inside that stroke.
    solid(img, [(762, 300), (762, 420)], CYAN, 10)
    arrow(img, (520, 545), (762, 360))
    # Blank reason line. The arrow is horizontal and overlaps its left end.
    hline(img, 620, 1280, 760, WHITE, 8)
    tag(img, (120, 715, 560, 805), ["Write one reason why"], face)
    arrow(img, (560, 760), (624, 760))
    stamp(img, 1240, 860)
    final = save(img, "course/images/bp-04-market-regimes/015.png")
    assert_tip(final, (762, 360), (766, 360), "shape")
    assert_tip(final, (624, 760), (630, 760), "reason")
    record([{
        "path": "course/images/bp-04-market-regimes/015.png",
        "lesson": "bp-04-market-regimes",
        "shows": "A handmade path, three shape boxes with the first one ticked, and a blank line for one reason.",
        "alt": "Sort one chart on paper: pick one shape, then write one reason why.",
        "batch": "cursor-bp04-015",
    }])


def bp05_006() -> None:
    img = canvas()
    head(img, "HALF THE GAP, DOUBLE THE GAPS", "DOUBLE THE GAPS", size=40)
    # Same band height. Halving the step doubles the gaps: 5 gaps become 10, so 6 lines become 11.
    card(img, (120, 280, 700, 700))
    card(img, (836, 280, 1416, 700))
    left_ys = [340 + i * 60 for i in range(6)]
    right_ys = [340 + i * 30 for i in range(11)]
    for y in left_ys:
        hline(img, 180, 640, y, CYAN, 5)
    for y in right_ys:
        hline(img, 896, 1356, y, CYAN, 5)
    # Dashed line joining the tops, with a dash at the left end.
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    x = 250
    while x < 820:
        d.line([(px(x), px(248)), (px(min(x + 28, 820)), px(248))], fill=WHITE + (255,), width=px(6))
        x += 48
    paste_layer(img, layer)
    face = font(FONT_SEMI, 30)
    tag(img, (120, 170, 470, 230), ["Same height"], face)
    arrow(img, (300, 230), (264, 248))
    tag(img, (836, 170, 1416, 250), ["Smaller gaps need more lines"], face)
    # Right box top stroke is y=280. Tip sits 2px inside it.
    arrow(img, (1120, 250), (1120, 284))
    # Counts match the lines actually drawn. The house recount is its own line.
    tag(img, (120, 720, 700, 800), ["6 lines, 5 gaps"], face)
    tag(img, (836, 720, 1416, 800), ["11 lines, 10 gaps"], face)
    tag(img, (140, 840, 1180, 920), ["9.5% range ÷ 0.25% step = 38 gaps, not 40"], face)
    stamp(img, 1320, 880)
    final = save(img, "course/images/bp-05-spacing-and-range/006.png")
    assert_tip(final, (264, 248), (270, 248), "height")
    assert_tip(final, (1120, 284), (1120, 280), "lines")
    if len(left_ys) != 6 or len(right_ys) != 11:
        raise SystemExit("line count")
    if abs((left_ys[-1] - left_ys[0]) - (right_ys[-1] - right_ys[0])) > 0.5:
        raise SystemExit("band height")
    record([{
        "path": "course/images/bp-05-spacing-and-range/006.png",
        "lesson": "bp-05-spacing-and-range",
        "shows": "Two boxes of the same height. The left is labelled 6 lines, 5 gaps. The right is labelled 11 lines, 10 gaps. A separate line gives the house recount: a 9.5% range divided by a 0.25% step is 38 gaps, not 40.",
        "alt": "Half the gap doubles the gaps. The left box is 6 lines and 5 gaps. The right box is 11 lines and 10 gaps. A 9.5% range divided by a 0.25% step is 38 gaps, not 40.",
        "batch": "cursor-bp05-006",
    }])


def plain(rel, lesson, title, cyan, lines, shows, alt, batch, size=34) -> None:
    img = canvas()
    head(img, title, cyan, size=40 if len(title) < 36 else 34)
    rows(img, lines, y0=240, size=size)
    stamp(img, 1320, 900)
    save(img, rel)
    record([{
        "path": rel,
        "lesson": lesson,
        "shows": shows,
        "alt": alt,
        "batch": batch,
    }])


def bp08() -> None:
    L = "bp-08-managing-and-monitoring"
    B = "cursor-bp08"
    base = "course/images/bp-08-managing-and-monitoring"
    plain(f"{base}/001.png", L, "A SHORT LIST, THEN YOU STOP", "SHORT LIST",
          ["Inside the band?", "Above or below the middle?", "Does your stop rule hold?", "Then you stop"],
          "Monitoring is a short list of three questions, then you stop.",
          "A short list you can finish: inside the band, above or below the middle, and whether your stop rule holds.", B)
    plain(f"{base}/004.png", L, "THREE QUESTIONS", "THREE",
          ["1  Inside the band?", "2  Above or below the middle?", "3  Does your stop rule hold?"],
          "The three questions are inside the band, above or below the middle, and whether the stop rule holds.",
          "Three questions: is the close inside the band, is it above or below the middle, and does your stop rule hold?", B)
    img = canvas()
    head(img, "THE CLOSE IS STILL INSIDE", "INSIDE")
    card(img, (200, 260, 1330, 860))
    hline(img, 280, 1240, 400, CYAN, 6)
    hline(img, 280, 1240, 680, CYAN, 6)
    solid(img, [(340, 540), (520, 420), (700, 640), (880, 460), (1060, 600), (1200, 500)])
    tag(img, (420, 740, 1100, 820), ["Still between top and bottom"], font(FONT_SEMI, 32))
    stamp(img, 1180, 320)
    save(img, f"{base}/005.png")
    record([{"path": f"{base}/005.png", "lesson": L, "shows": "A price path that stays between the top and bottom lines.", "alt": "Inside means the close is still between the top and the bottom.", "batch": B}])
    img = canvas()
    head(img, "ABOVE OR BELOW THE MIDDLE", "MIDDLE", size=40)
    card(img, (160, 230, 1380, 900))
    hline(img, 240, 1200, 540, WHITE, 8)
    block(img, 400, 370, 48, 48, CYAN)
    block(img, 756, 656, 48, 48, CYAN)
    tag(img, (220, 250, 560, 340), ["Above"], font(FONT_SEMI, 34))
    tag(img, (900, 780, 1300, 870), ["Below"], font(FONT_SEMI, 34))
    tag(img, (980, 390, 1320, 470), ["Middle 27630"], font(FONT_SEMI, 32))
    arrow(img, (420, 340), (424, 390))
    arrow(img, (1000, 780), (780, 680))
    arrow(img, (1100, 470), (1000, 540))
    stamp(img, 250, 820)
    final = save(img, f"{base}/006.png")
    assert_tip(final, (424, 390), (424, 410), "above")
    assert_tip(final, (780, 680), (780, 700), "below")
    assert_tip(final, (1000, 540), (1000, 542), "middle")
    record([{"path": f"{base}/006.png", "lesson": L, "shows": "The middle line is 27630. One close is above it and one close is below it.", "alt": "Above or below means which side of the middle line, 27630, the close is on.", "batch": B}])
    plain(f"{base}/007.png", L, "REREAD THE SAME SENTENCE", "SAME",
          ["Do not write a new sentence", "Read the finish rule again"],
          "The third check is rereading the finish sentence you already wrote.",
          "Reread the same finish sentence. Do not invent a new one while you look.", B)
    plain(f"{base}/008.png", L, "PICK A DAY TO REREAD", "A DAY",
          ["Choose one day", "Read the same three rows", "Then stop"],
          "A cadence is one day you choose to reread the same three rows.",
          "Pick a day, reread the same three rows, then stop.", B)
    plain(f"{base}/009.png", L, "DO NOT OPEN THESE", "NOT",
          ["Not a result chart", "Not a ranking", "Not a leverage control"],
          "The check does not open a result chart, a ranking, or a leverage control.",
          "Do not open a result chart, a ranking, or a leverage control.", B, size=36)
    img = canvas()
    head(img, "STARTS INSIDE, ENDS OUTSIDE", "OUTSIDE", size=40)
    card(img, (160, 250, 1360, 880))
    hline(img, 240, 1280, 400, CYAN, 5)
    hline(img, 240, 1280, 620, CYAN, 5)
    solid(img, [(280, 510), (460, 430), (700, 620), (1180, 760)])
    tag(img, (240, 660, 520, 740), ["Inside"], font(FONT_SEMI, 34))
    tag(img, (700, 800, 1100, 870), ["Outside"], font(FONT_SEMI, 34))
    arrow(img, (400, 660), (460, 430))
    arrow(img, (1000, 800), (1161, 754))
    stamp(img, 1240, 300)
    save(img, f"{base}/010.png")
    record([{"path": f"{base}/010.png", "lesson": L, "shows": "A path that starts inside the band and ends outside it.", "alt": "Run the check on a path that starts inside the band and ends outside it.", "batch": B}])
    plain(f"{base}/011.png", L, "AN ALERT IS ONLY A NUDGE", "NUDGE",
          ["It does not decide for you", "Come read the three rows"],
          "An alert is only a nudge to come read the same three rows.",
          "An alert only nudges you to come read the three rows.", B)
    plain(f"{base}/012.png", L, "DO NOT ADD A RESULT ROW", "NOT",
          ["Inside the band?", "Above or below the middle?", "Does your stop rule hold?", "No result row"],
          "The common miss is adding a result row. The card stays at three questions.",
          "Do not add a result row to the three questions.", B)
    plain(f"{base}/013.png", L, "THEN YOU STOP", "STOP",
          ["Answer the three questions", "Stop, or write an edit", "Do not keep watching"],
          "After the three answers you stop or you write an edit. You do not keep watching.",
          "After the check, stop or write an edit. Do not keep watching.", B)
    plain(f"{base}/014.png", L, "WRITE THE THREE ROWS", "THREE",
          ["Inside the band?", "Above or below the middle?", "Does your stop rule hold?"],
          "Build the three-row card on paper and run it once.",
          "Write the three questions on paper and run them once.", B)
    plain(f"{base}/015.png", L, "RECAP", "RECAP",
          ["Inside the band?", "Above or below the middle?", "Does the stop rule hold?", "A day you chose", "No result row", "Then stop"],
          "Recap of the check: inside, above or below, the rule, a chosen day, no result row, then stop.",
          "Recap: inside, above or below the middle, the stop rule, a day you chose, no result row, then stop.", B, size=30)
    plain(f"{base}/019.png", L, "POINT AT THE PAPER SCREEN", "PAPER",
          ["Same three rows", "On the paper, not a live order"],
          "If you finished the paper walk, point the three rows at that paper screen.",
          "Point the three rows at the paper screen. It is not a live order.", B)


def bp09() -> None:
    L = "bp-09-common-mistakes"
    B = "cursor-bp09"
    base = "course/images/bp-09-common-mistakes"
    plain(f"{base}/001.png", L, "MISTAKES ARE ON THE PAGE", "PAGE",
          ["Look at the page", "Not at the person"],
          "The mistakes in this lesson are on the page, not about the person.",
          "These mistakes are pages, not personalities.", B)
    plain(f"{base}/004.png", L, "A BLANK STOP WAS SKIPPED", "BLANK",
          ["The finish column is empty", "That means it was skipped"],
          "A blank stop means the finish column was skipped.",
          "A blank stop means the finish column was skipped.", B)
    plain(f"{base}/005.png", L, "THE BAND IS TOO SHORT", "TOO SHORT",
          ["Your band", "Shorter than a normal day's move"],
          "A tight band is shorter than the normal up-and-down of the path.",
          "The band is too short for a normal day's move.", B)
    plain(f"{base}/006.png", L, "DO NOT STOP THE COURSE HERE", "NOT",
          ["Scaling up is still ahead", "The liquidation lesson is still ahead"],
          "Ending at the mistakes page skips scaling and the opt-in liquidation lesson.",
          "Do not end the course on the mistakes page. Scaling and the liquidation lesson are still ahead.", B)
    img = canvas()
    head(img, "7 LINES = 6 GAPS", "6 GAPS", size=52)
    card(img, (360, 240, 1180, 900))
    ladder(img, 480, 300, 70, 7, 520)
    stamp(img, 1000, 320)
    save(img, f"{base}/007.png")
    record([{"path": f"{base}/007.png", "lesson": L, "shows": "Seven lines with six gaps between them. Counting the lines is not the same as counting the gaps.", "alt": "Seven lines make six gaps. Count the gaps, not the lines.", "batch": B}])
    plain(f"{base}/008.png", L, "A FILLED-IN SIZE IS NOT YOURS", "NOT YOURS",
          ["The form filled in a size", "That was not your choice"],
          "A size the form filled in for you is not your choice.",
          "A size the form filled in is not your choice.", B)
    plain(f"{base}/009.png", L, "NO PROMISE OF INCOME", "NO PROMISE",
          ["Do not promise income", "A result can fail"],
          "A promise of income, or a claim that a result cannot fail, does not belong on a teaching page.",
          "Do not promise income, and do not claim a result cannot fail.", B)
    img = canvas()
    head(img, "SEVEN LINES AND SIX GAPS", "SIX GAPS", size=42)
    card(img, (120, 240, 700, 900))
    ladder(img, 220, 320, 64, 7, 360)
    tag(img, (160, 790, 660, 870), ["7 lines, 6 gaps"], font(FONT_SEMI, 32))
    tag(img, (760, 360, 1400, 520), ["Blank stop"], font(FONT_SEMI, 36))
    tag(img, (760, 580, 1400, 740), ["That column was skipped"], font(FONT_SEMI, 32))
    stamp(img, 1240, 280)
    save(img, f"{base}/010.png")
    record([{"path": f"{base}/010.png", "lesson": L, "shows": "The house example has seven lines and six gaps, and a blank stop means the finish column was skipped.", "alt": "In the example there are seven lines and six gaps. A blank stop means the finish column was skipped.", "batch": B}])
    plain(f"{base}/011.png", L, "FIX ONE, THEN THE NEXT", "ONE",
          ["1  Fix one mistake", "2  Read the page again", "3  Fix the next one"],
          "Fix one miss, reread, then fix the next.",
          "Fix one mistake, read the page again, then fix the next.", B)
    plain(f"{base}/012.png", L, "THIS IS NOT A SCORE", "NOT",
          ["The audit finds mistakes", "It does not give you a grade"],
          "The audit does not produce a grade.",
          "Checking the page finds mistakes. It does not give you a score.", B)
    plain(f"{base}/013.png", L, "CROSS OUT A TIMES-NUMBER", "CROSS OUT",
          ["5x does not belong here", "This path is spot"],
          "A leverage multiple does not belong on the spot path.",
          "Cross out a times-number such as 5x. This path is spot.", B)
    plain(f"{base}/014.png", L, "CHECK YOUR OWN PAGE", "CHECK",
          ["Is the stop blank?", "Is the band too short?", "Is the word gaps missing?"],
          "Audit the notebook for a blank stop, a tight band, and a missing gaps word.",
          "Check your page for a blank stop, a band that is too short, and a missing gaps word.", B)
    plain(f"{base}/015.png", L, "RECAP", "RECAP",
          ["Blank stop", "Band too short", "Stopping the course early", "Counting lines, not gaps", "A size you did not choose", "A promise of income"],
          "Recap of the mistakes: blank stop, tight band, early ending, counting lines, a default size, and result words.",
          "Recap: blank stop, band too short, ending early, counting lines instead of gaps, a size you did not choose, and a promise of income.", B, size=30)
    plain(f"{base}/020.png", L, "KEEP THE MARKED PAGES", "KEEP",
          ["The marks stay on the page", "The marks are the lesson"],
          "Keep the marked-up pages. The marks are the lesson.",
          "Keep the marked pages. The marks are the lesson.", B)


def bp10() -> None:
    L = "bp-10-scaling-up"
    B = "cursor-bp10"
    base = "course/images/bp-10-scaling-up"
    plain(f"{base}/001.png", L, "A SECOND PAGE, NOT A BIGGER NUMBER", "SECOND PAGE",
          ["Page two is another written page", "It is not a bigger number"],
          "Scaling here means a second written page, not a bigger number.",
          "A second page, not a bigger number.", B)
    plain(f"{base}/004.png", L, "PAGE TWO REPEATS THE CHECKS", "CHECKS",
          ["Sort the shape", "Range", "Gaps", "Finish sentence", "Paper"],
          "The second page repeats the same checks: shape, range, gaps, finish sentence, and paper.",
          "Page two repeats the checks: the shape, the range, the gaps, the finish sentence, and paper.", B, size=32)
    plain(f"{base}/005.png", L, "TWO GRIDS CAN FIGHT", "FIGHT",
          ["Two grids, one coin", "They share what you hold"],
          "Two grids on one asset can fight if they share what you hold.",
          "Two grids on the same coin can fight if they share what you hold.", B)
    plain(f"{base}/006.png", L, "THE SAME SIZE IS ALLOWED", "SAME SIZE",
          ["You do not have to change the size", "That is a complete review"],
          "A review that keeps the size the same is a complete review.",
          "Keeping the same size is a complete review.", B)
    plain(f"{base}/008.png", L, "PAGE TWO: SAME PAIR, NEW BAND", "NEW BAND",
          ["Same pair", "Same spot", "Only the band changes"],
          "Page two keeps the same pair and spot, and changes only the band.",
          "Page two keeps the same pair and changes only the band.", B)
    plain(f"{base}/007.png", L, "CHANGE ONE THING", "ONE",
          ["Page one", "Page two changes one thing only"],
          "Change one thing between page one and page two.",
          "Change only one thing between page one and page two.", B)
    plain(f"{base}/009.png", L, "THIS IS NOT THE LAST LESSON", "NOT",
          ["Scaling is not the end", "One more lesson is optional"],
          "Scaling is not the end of the course.",
          "Scaling up is not the last lesson.", B)
    plain(f"{base}/010.png", L, "PAGE TWO IS STILL SPOT", "SPOT",
          ["You still hold the coin", "Not a contract"],
          "The second page is still spot. You hold the coin, not a contract.",
          "Page two is still spot. You hold the coin, not a contract.", B)
    plain(f"{base}/011.png", L, "NO MONEY AMOUNT ON THIS PAGE", "NO MONEY",
          ["The page does not say how much", "Leave that box empty"],
          "The page does not tell you how much money to assign.",
          "This page does not tell you how much money to use.", B)
    plain(f"{base}/012.png", L, "DO NOT DOUBLE THE COUNT", "NOT",
          ["The first page felt fine", "That is not a reason to double"],
          "The common miss is doubling a count because the first page felt fine.",
          "Do not double the count just because the first page felt fine.", B)
    plain(f"{base}/013.png", L, "THEY CAN FILL AT THE SAME TIME", "SAME TIME",
          ["Two pairs that move together", "Both can fill together"],
          "Two pairs that move together can fill the same way at the same time.",
          "Two pairs that move together can fill at the same time.", B)
    plain(f"{base}/014.png", L, "SAME CHECKS, OR NOT YET", "SAME CHECKS",
          ["Page two passes the same checks", "Or it does not exist yet"],
          "Page two passes the same checks, or it does not exist yet.",
          "Page two passes the same checks, or it does not exist yet.", B)
    plain(f"{base}/015.png", L, "RECAP", "RECAP",
          ["A second page", "The same checks", "They can share what you hold", "Change one thing", "Still spot", "No money amount"],
          "Recap: a second page, the same checks, shared holdings, one change, still spot, and no money amount.",
          "Recap: second page, same checks, shared holdings, one change, still spot, and no amount of money.", B, size=30)
    plain(f"{base}/020.png", L, "FILE BOTH ONLY IF BOTH PASSED", "BOTH",
          ["Page one passed", "Page two passed", "Then file them together"],
          "File page one and page two together only if both passed.",
          "File both pages together only if both passed.", B)


def bp11() -> None:
    L = "bp-11-advanced-liquidation"
    B = "cursor-bp11"
    base = "course/images/bp-11-advanced-liquidation"
    plain(f"{base}/001.png", L, "OPTIONAL. THE LOSS COMES FIRST", "LOSS",
          ["You can skip this lesson", "If you stay, draw the losing path first"],
          "This lesson is opt-in. The losing path comes first.",
          "This lesson is optional. If you stay, the losing path comes first.", B)
    plain(f"{base}/004.png", L, "THE SPOT PATH IS ALREADY DONE", "ALREADY DONE",
          ["The spot page stands on its own", "You do not need this lesson"],
          "The paper spot path is already complete without this lesson.",
          "The spot path is already complete without this lesson.", B)
    plain(f"{base}/005.png", L, "THE EXCHANGE CLOSES THE TRADE", "CLOSES",
          ["The margin no longer covers the loss", "The exchange closes the trade"],
          "Liquidation means the exchange closes the trade when the margin no longer covers the loss.",
          "Liquidation means the exchange closes the trade when the margin runs out.", B)
    plain(f"{base}/006.png", L, "PRICE LEAVES, THEN THE TRADE CLOSES", "THEN",
          ["1  Price leaves and does not come back", "2  The trade is closed"],
          "Draw the price leaving the band and not returning, then draw the trade closed.",
          "First the price leaves and does not come back. Then the trade is closed.", B)
    plain(f"{base}/007.png", L, "ISOLATED: THE LOSS STAYS IN ONE BOX", "ONE BOX",
          ["One box", "A loss in that box stays there"],
          "Isolated margin means the exchange looks only at what was assigned to that trade.",
          "Isolated means a loss in that one box stays in that box.", B)
    plain(f"{base}/008.png", L, "CROSS MARGIN CAN USE OTHER BALANCES", "OTHER BALANCES",
          ["The exchange may look past that box", "It may use other balances"],
          "Cross margin means the exchange may look at other balances in the same account.",
          "Cross margin means the exchange may use other balances in the account.", B)
    plain(f"{base}/009.png", L, "DO NOT WRITE A TIMES-NUMBER", "DO NOT",
          ["No 5x in the isolated box", "No 5x in the cross-margin box"],
          "Do not write a times-number in either box.",
          "Do not write a times-number in the isolated box or the cross-margin box.", B)
    plain(f"{base}/010.png", L, "FUNDING IS A SEPARATE PAYMENT", "SEPARATE",
          ["A payment between the two sides", "It is not the price path"],
          "A funding payment between sides is separate from the price path.",
          "Funding is a separate payment between the two sides, not the price path.", B)
    plain(f"{base}/011.png", L, "CROSS OUT 5x ON OLD NOTES", "CROSS OUT",
          ["Old notes may show 5x", "Cross that out"],
          "If old notes show a multiple like 5x, cross it out.",
          "If old notes show 5x, cross it out.", B)
    plain(f"{base}/012.png", L, "TWO WARNINGS", "TWO",
          ["This can be liquidated", "You can lose all you put in"],
          "Two warnings: the trade can be liquidated, and you can lose all the money you put in.",
          "Two warnings: this can be liquidated, and you can lose all the money you put in.", B, size=36)
    plain(f"{base}/013.png", L, "NOT A LIVE EXCHANGE SCREEN", "NOT",
          ["No login", "No live contract screen"],
          "The lesson does not walk a live contract screen.",
          "This is not a guide to a live exchange screen.", B)
    plain(f"{base}/014.png", L, "EXPLAIN IT WITHOUT A TIMES-NUMBER", "WITHOUT",
          ["Isolated: the loss stays in one box", "Cross margin: other balances can be used", "No times-number"],
          "The sentence to write: explain isolated and cross margin without a times-number, and draw the loss first.",
          "Explain isolated and cross margin without a times-number.", B, size=30)
    plain(f"{base}/015.png", L, "RECAP", "RECAP",
          ["Optional", "Loss first", "Isolated: one box", "Cross margin: other balances", "No times-number", "The spot page still stands"],
          "Recap: optional, loss first, isolated, cross margin, no times-number, and the spot page still stands.",
          "Recap: the lesson is optional, the loss comes first, isolated stays in one box, cross margin can use other balances, there is no times-number, and the spot page still stands.", B, size=28)
    plain(f"{base}/019.png", L, "SKIPPED ON PURPOSE", "SKIPPED",
          ["Write this on the spot notebook", "Skipped on purpose"],
          "If you skip this lesson, write Skipped on purpose on the spot notebook.",
          "If you skip this lesson, write Skipped on purpose on the spot notebook.", B)


LESSONS = {
    "bp02": bp02_014,
    "six": beginner_six,
    "bp04": lesson_bp04,
    "bp05": lesson_bp05,
    "bp06": bp06,
    "bp07": bp07,
    "bp08": bp08,
    "bp09": bp09,
    "bp10": bp10,
    "bp11": bp11,
}


if __name__ == "__main__":
    name = sys.argv[1] if len(sys.argv) > 1 else "bp04"
    LESSONS[name]()
