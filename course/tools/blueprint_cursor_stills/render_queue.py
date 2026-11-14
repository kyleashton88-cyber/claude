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
    arrow(img, (1100, 330), (1100, 400))
    arrow(img, (500, 760), (500, 730))
    stamp(img, 240, 300)
    final = save(img, "course/images/bp-04-market-regimes/007.png")
    assert_tip(final, (1100, 400), (1160, 430), "high")
    assert_tip(final, (500, 730), (560, 680), "dip")
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
    arrow(img, (400, 680), (400, 560))
    arrow(img, (1040, 748), (1040, 348))
    stamp(img, 1260, 300)
    final = save(img, "course/images/bp-04-market-regimes/011.png")
    assert_tip(final, (400, 560), (400, 556), "band")
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
            arrow(img, (760, 380), (800, 560))
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


LESSONS = {
    "bp04": lesson_bp04,
    "bp05": lesson_bp05,
    "bp06": bp06,
    "bp07": bp07,
}


if __name__ == "__main__":
    name = sys.argv[1] if len(sys.argv) > 1 else "bp04"
    LESSONS[name]()
