"""Redraw the code beats and hero cards for one lesson.

Illustration PNGs are left in place. A figure is drawn only when that beat
or the approved card text says it, and it is marked Example. Labels are
28 px or larger. There is no corner chip and no balance.
"""

from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image, ImageDraw

import build_visuals as bv

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "course/visuals-25nov"


def wrap_draw(draw, text, box, fill=bv.WHITE, sizes=(40, 36, 32, 28)) -> None:
    x0, y0, x1, y1 = box
    width = x1 - x0
    chosen = None
    for size in sizes:
        face = bv.font(size)
        lines = bv.wrap(text, face, width)
        step = size + 12
        if y0 + len(lines) * step <= y1:
            chosen = (face, lines, step)
            break
    if chosen is None:
        face = bv.font(28)
        lines = bv.wrap(text, face, width)
        step = 40
        chosen = (face, lines, step)
    face, lines, step = chosen
    y = y0
    for line in lines:
        if y + step > y1:
            break
        draw.text((x0, y), line, font=face, fill=fill)
        y += step


def ladder(draw, prices: list[str], box) -> None:
    x0, y0, x1, y1 = box
    show = []
    for price in prices:
        if price not in show:
            show.append(price)
    show = show[:8]
    if not show:
        return
    gap = (y1 - y0) / len(show)
    for index, price in enumerate(show):
        y = int(y0 + gap * index + gap / 2)
        draw.line([(x0, y), (x0 + 720, y)], fill=bv.CYAN, width=6)
        draw.text((x0 + 748, y - 18), f"Example {price}", font=bv.font(32), fill=bv.WHITE)


def frame(title: str) -> tuple[Image.Image, ImageDraw.ImageDraw]:
    image = bv.background()
    draw = ImageDraw.Draw(image)
    draw.text((bv.MARGIN, 48), title, font=bv.font(36), fill=bv.CYAN)
    bv.panel(draw, (bv.MARGIN, 120, bv.W - bv.MARGIN, 960))
    bv.footer(draw)
    return image, draw


def paint_hero(title: str, label: str) -> Image.Image:
    image, draw = frame(title)
    prices = bv.price_tokens(label)
    top = 168
    if "0.2673" in label and "0.2763" in label and "0.5436" in label:
        draw.text((bv.MARGIN + 48, 170), "Example  0.2673 + 0.2763 = 0.5436", font=bv.font(40), fill=bv.WHITE)
        top = 250
    elif 0 < len(prices) <= 6:
        ladder(draw, prices, (bv.MARGIN + 48, 180, bv.W - bv.MARGIN - 48, 180 + 70 * len(prices)))
        top = 200 + 70 * len(prices)
    wrap_draw(draw, label, (bv.MARGIN + 48, top, bv.W - bv.MARGIN - 48, 920))
    return image


def paint_beat(title: str, sentence: str, visual: str) -> Image.Image:
    image, draw = frame(title)
    low = visual.lower()
    inner = (bv.MARGIN + 48, 180, bv.W - bv.MARGIN - 48, 900)
    if "title card" in low:
        wrap_draw(draw, sentence, (bv.MARGIN + 80, 360, bv.W - bv.MARGIN - 80, 860), sizes=(64, 48, 40, 36))
        return image
    if "disclaimer" in low:
        draw.text((bv.MARGIN + 48, 180), "Education only.", font=bv.font(48), fill=bv.CYAN)
        wrap_draw(draw, sentence, (bv.MARGIN + 48, 280, bv.W - bv.MARGIN - 48, 900), sizes=(36, 32, 28))
        return image
    if "end lockup" in low:
        bv.lockup(draw, 280, 340)
        next_name = visual.split("Next lesson:", 1)[-1].strip() if "Next lesson:" in visual else ""
        draw.text((bv.MARGIN + 48, 480), "Next lesson", font=bv.font(32), fill=bv.CYAN)
        wrap_draw(draw, next_name, (bv.MARGIN + 48, 540, bv.W - bv.MARGIN - 48, 860), sizes=(48, 40, 36))
        return image
    if "skip card" in low:
        draw.text((bv.MARGIN + 80, 360), "Skipped on purpose.", font=bv.font(56), fill=bv.WHITE)
        draw.text((bv.MARGIN + 80, 460), "The spot page stands.", font=bv.font(48), fill=bv.CYAN)
        return image
    if "three-question" in low:
        draw.text((bv.MARGIN + 48, 180), "Three questions", font=bv.font(48), fill=bv.CYAN)
        lines = [
            "1  Inside, or outside?",
            "2  Which side? Not asked once it is outside.",
            "3  Is the written rule still in force?",
        ]
        y = 320
        for line in lines:
            draw.text((bv.MARGIN + 48, y), line, font=bv.font(36), fill=bv.WHITE)
            y += 80
        return image
    if "pair of forms" in low:
        mid = bv.W // 2
        draw.rounded_rectangle([bv.MARGIN + 48, 200, mid - 24, 860], 16, outline=bv.CYAN, width=3)
        draw.rounded_rectangle([mid + 24, 200, bv.W - bv.MARGIN - 48, 860], 16, outline=bv.CYAN, width=3)
        draw.text((bv.MARGIN + 80, 230), "Wrong", font=bv.font(40), fill=bv.CYAN)
        draw.text((mid + 56, 230), "Right", font=bv.font(40), fill=bv.WHITE)
        for index, name in enumerate(("Pair", "Range", "Stop")):
            y = 360 + index * 140
            draw.text((bv.MARGIN + 80, y), name, font=bv.font(32), fill=bv.WHITE)
            draw.line([(bv.MARGIN + 80, y + 56), (mid - 64, y + 56)], fill=bv.CYAN, width=3)
            draw.text((mid + 56, y), name, font=bv.font(32), fill=bv.WHITE)
            draw.line([(mid + 56, y + 56), (bv.W - bv.MARGIN - 88, y + 56)], fill=bv.CYAN, width=3)
        return image
    if "page being corrected" in low:
        draw.rounded_rectangle([bv.MARGIN + 180, 200, bv.W - bv.MARGIN - 180, 820], 16, outline=bv.CYAN, width=3)
        draw.text((bv.MARGIN + 230, 260), "This page", font=bv.font(48), fill=bv.WHITE)
        draw.text((bv.MARGIN + 230, 360), "is being fixed.", font=bv.font(48), fill=bv.CYAN)
        draw.line([(bv.MARGIN + 230, 500), (bv.W - bv.MARGIN - 260, 500)], fill=bv.CYAN, width=4)
        draw.text((bv.MARGIN + 230, 560), "One change, then check it.", font=bv.font(36), fill=bv.WHITE)
        return image
    prices = bv.price_tokens(sentence)
    if "0.2673" in sentence and "0.2763" in sentence and "0.5436" in sentence:
        draw.text((bv.MARGIN + 48, 220), "Example", font=bv.font(32), fill=bv.CYAN)
        draw.text((bv.MARGIN + 48, 300), "0.2673 + 0.2763 = 0.5436", font=bv.font(48), fill=bv.WHITE)
        return image
    if prices and ("chart" in low or "ladder" in low or "diagram" in low):
        window = visual.split("Window:", 1)[-1].strip(" .") if "Window:" in visual else ""
        if window:
            draw.text((bv.MARGIN + 48, 160), window[:48], font=bv.font(28), fill=bv.CYAN)
        ladder(draw, prices, (bv.MARGIN + 48, 230, bv.W - bv.MARGIN - 48, 880))
        return image
    # A diagram of the idea, not a reprint of the spoken line.
    if any(word in sentence.lower() for word in ("gap", "step", "space")):
        draw.line([(bv.MARGIN + 120, 340), (bv.W - bv.MARGIN - 120, 340)], fill=bv.CYAN, width=6)
        draw.line([(bv.MARGIN + 120, 560), (bv.W - bv.MARGIN - 120, 560)], fill=bv.CYAN, width=6)
        draw.text((bv.MARGIN + 120, 420), "Gap", font=bv.font(48), fill=bv.WHITE)
        return image
    if "buy" in sentence.lower() and "sell" in sentence.lower():
        bv.draw_columns(draw, "Buy", "Sell", inner)
        return image
    if "stop" in sentence.lower():
        draw.text((bv.MARGIN + 80, 300), "Stop", font=bv.font(64), fill=bv.WHITE)
        draw.line([(bv.MARGIN + 80, 420), (bv.W - bv.MARGIN - 80, 420)], fill=bv.CYAN, width=8)
        draw.text((bv.MARGIN + 80, 460), "The written rule", font=bv.font(36), fill=bv.CYAN)
        return image
    if "range" in sentence.lower() or "top" in sentence.lower() or "bottom" in sentence.lower():
        draw.line([(bv.MARGIN + 120, 280), (bv.W - bv.MARGIN - 120, 280)], fill=bv.CYAN, width=6)
        draw.text((bv.MARGIN + 120, 200), "Top line", font=bv.font(36), fill=bv.CYAN)
        draw.line([(bv.MARGIN + 120, 700), (bv.W - bv.MARGIN - 120, 700)], fill=bv.WHITE, width=6)
        draw.text((bv.MARGIN + 120, 730), "Bottom line", font=bv.font(36), fill=bv.WHITE)
        return image
    draw.rounded_rectangle([bv.MARGIN + 160, 300, bv.W - bv.MARGIN - 160, 640], 18, outline=bv.CYAN, width=4)
    words = [word for word in sentence.split() if word[:1].isupper()][:3]
    label = " ".join(words) if words else "This beat"
    wrap_draw(draw, label, (bv.MARGIN + 200, 400, bv.W - bv.MARGIN - 200, 600), sizes=(48, 40, 36, 32))
    return image


def beats(manifest: str) -> list[tuple[str, str, str, str]]:
    rows = []
    for line in manifest.splitlines():
        parts = [part.strip() for part in line.strip().strip("|").split("|")]
        if len(parts) < 9 or not parts[0].isdigit():
            continue
        rows.append((f"{int(parts[0]):03d}", parts[3], parts[4], parts[6]))
    return rows


def heroes(manifest: str) -> list[tuple[str, str]]:
    rows = []
    for line in manifest.splitlines():
        parts = [part.strip() for part in line.strip().strip("|").split("|")]
        if len(parts) < 3 or not parts[0].startswith("`heroes/"):
            continue
        name = parts[0].strip("`")
        rows.append((name, parts[1]))
    return rows


def paint_lesson(number: str) -> tuple[int, int]:
    lesson = OUT / f"BP-{number}"
    manifest = (lesson / "MANIFEST.md").read_text(encoding="utf-8")
    title = ""
    for line in manifest.splitlines():
        if line.startswith("Title:"):
            title = line.split(":", 1)[1].strip()
            break
    code = 0
    for beat, sentence, visual, chatgpt in beats(manifest):
        if chatgpt == "yes":
            continue
        image = paint_beat(title, sentence, visual)
        image.save(lesson / "stills" / f"{beat}.png", optimize=True)
        code += 1
    hero_count = 0
    for name, label in heroes(manifest):
        paint_hero(title, label).save(lesson / name, optimize=True)
        hero_count += 1
    return code, hero_count


def main() -> None:
    numbers = sys.argv[1:] or [f"{n:02d}" for n in range(3, 12)]
    for number in numbers:
        code, hero_count = paint_lesson(number)
        print(f"BP-{number} code {code} heroes {hero_count}", flush=True)


if __name__ == "__main__":
    main()
