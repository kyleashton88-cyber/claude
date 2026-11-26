"""Draw the code beats for one lesson. ChatGPT beats get no file.

No film is rendered. There is no corner EXAMPLE chip. A figure is drawn
only when this beat names it. Every label is at least 28 px.
"""

from __future__ import annotations

import re
import shutil
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "course/visuals-25nov"
FONT = ROOT / "skills/video-production/fonts/inter/Inter-Bold.ttf"
FONT_REG = ROOT / "skills/video-production/fonts/inter/Inter-Regular.ttf"
GATE = ROOT / "skills/video-production/quality-gate"
sys.path.insert(0, str(GATE))
from gate.numbers import FIGURE, _GROUPED, _covered, _iter_dates, _norm, screen_figures  # noqa: E402

W, H = 1920, 1080
MARGIN = 96
NAVY = (7, 17, 31)
CYAN = (0, 229, 255)
WHITE = (255, 255, 255)
GLASS = (9, 22, 40)
MUTED = (154, 168, 188)


def face(size: int, regular: bool = False) -> ImageFont.FreeTypeFont:
    if size < 28:
        raise SystemExit(f"label under 28 px: {size}")
    return ImageFont.truetype(str(FONT_REG if regular else FONT), size)


def wrap(text: str, font: ImageFont.FreeTypeFont, width: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        trial = f"{current} {word}".strip()
        if current and font.getlength(trial) > width:
            lines.append(current)
            current = word
        else:
            current = trial
    if current:
        lines.append(current)
    return lines or [""]


def spellings(text: str) -> list[str]:
    """Figures this beat actually names, in the order they are spoken."""
    allowed = screen_figures(text)
    skip = [(match.start(), match.end()) for match in _iter_dates(text or "")]
    found: list[str] = []
    occupied = list(skip)
    for match in list(_GROUPED.finditer(text or "")) + list(FIGURE.finditer(text or "")):
        if _covered(occupied, match.start(), match.end()):
            continue
        raw = match.group(0).lstrip("$")
        occupied.append((match.start(), match.end()))
        if _norm(raw) not in allowed:
            continue
        if raw not in found:
            found.append(raw)
    return found


def background() -> Image.Image:
    image = Image.new("RGB", (W, H), NAVY)
    draw = ImageDraw.Draw(image)
    for x in range(0, W, 48):
        draw.line([(x, 0), (x, H)], fill=(12, 28, 46))
    for y in range(0, H, 48):
        draw.line([(0, y), (W, y)], fill=(12, 28, 46))
    return image


def footer(draw: ImageDraw.ImageDraw) -> None:
    draw.text((MARGIN, 992), "Education only. Not financial advice.", font=face(28, True), fill=MUTED)


def panel(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int]) -> None:
    draw.rounded_rectangle(box, 18, fill=GLASS, outline=CYAN, width=3)


def write_lines(draw: ImageDraw.ImageDraw, text: str, x: int, y: int, width: int, bottom: int, size: int = 32, fill=WHITE) -> int:
    font = face(size)
    lines = wrap(text, font, width)
    step = size + 8
    if y + len(lines) * step > bottom:
        font = face(28)
        lines = wrap(text, font, width)
        step = 36
    for line in lines:
        if y + step > bottom:
            break
        draw.text((x, y), line, font=font, fill=fill)
        y += step
    return y


def lockup(draw: ImageDraw.ImageDraw, x: int, y: int) -> None:
    import math
    points = []
    for index in range(6):
        angle = math.radians(-90 + index * 60)
        points.append((x + 54 * math.cos(angle), y + 54 * math.sin(angle)))
    draw.polygon(points, outline=CYAN)
    draw.text((x - 18, y - 22), "G", font=face(48), fill=CYAN)
    draw.text((x + 80, y - 36), "GRID BOT", font=face(42), fill=WHITE)
    draw.text((x + 80, y + 12), "BUILDER", font=face(42), fill=CYAN)


def rungs(draw: ImageDraw.ImageDraw, prices: list[str], box: tuple[int, int, int, int], source: str) -> None:
    x0, y0, x1, y1 = box
    show = prices[:8]
    if not show:
        return
    gap = (y1 - y0) / max(1, len(show))
    places = {}
    for index, price in enumerate(show):
        y = int(y0 + gap * index + gap / 2)
        places[price] = y
        draw.line([(x0, y), (x0 + 520, y)], fill=CYAN, width=4)
        label = f"Example {price}" if re.search(r"\bexample\b", source, re.I) or "marked Example" in source else price
        if "Example" not in label and re.search(r"\bexample\b", source, re.I) is None:
            # The lesson marks every figure Example. The word sits on the figure, not in a corner chip.
            label = f"Example {price}"
        draw.text((x0 + 544, y - 18), label, font=face(32), fill=WHITE)
    if "901" in source and "27,630" in places and "28,531" in places:
        mid = (places["27,630"] + places["28,531"]) // 2
        draw.text((x0 + 544, mid - 18), "Example 901", font=face(28), fill=CYAN)


def columns(draw: ImageDraw.ImageDraw, left: str, right: str, box: tuple[int, int, int, int]) -> None:
    x0, y0, x1, y1 = box
    mid = (x0 + x1) // 2
    draw.rounded_rectangle([x0, y0, mid - 16, y1], 16, outline=CYAN, width=3)
    draw.rounded_rectangle([mid + 16, y0, x1, y1], 16, outline=CYAN, width=3)
    write_lines(draw, left, x0 + 28, y0 + 28, mid - x0 - 72, y1 - 16)
    write_lines(draw, right, mid + 44, y0 + 28, x1 - mid - 72, y1 - 16)


def picture(draw: ImageDraw.ImageDraw, text: str, visual: str, box: tuple[int, int, int, int]) -> None:
    low = text.lower()
    prices = spellings(text)
    if "wrong beside right" in visual or ("wrong form" in low and "right form" in low):
        left = "wrong form" if "wrong form" in low else "seven"
        right = "right form" if "right form" in low else "six gaps"
        if "no logo" in low or "no balance" in low:
            left = left + ". No logo. No balance."
        columns(draw, left, right, box)
        return
    if prices and ("ladder" in visual or "chart" in visual or "Window" in visual):
        rungs(draw, prices, box, text)
        return
    if "cross" in low and "fill" in low:
        columns(draw, "cross", "fill", box)
        return
    if "limit order" in low and "market order" in low:
        columns(draw, "limit order", "market order", box)
        return
    if "buy" in low and "sell" in low and not prices:
        columns(draw, "buy", "sell", box)
        return
    if "range" in low and "trend" in low and "break" in low:
        columns(draw, "range", "trend", box)
        return
    if prices:
        rungs(draw, prices, box, text)
        return
    if "top" in low and "bottom" in low:
        x0, y0, x1, y1 = box
        draw.line([(x0, y0 + 36), (x1 - 200, y0 + 36)], fill=CYAN, width=6)
        draw.line([(x0, y1 - 48), (x1 - 200, y1 - 48)], fill=CYAN, width=6)
        draw.text((x1 - 180, y0 + 16), "top", font=face(32), fill=CYAN)
        draw.text((x1 - 180, y1 - 64), "bottom", font=face(32), fill=WHITE)


def paint(title: str, text: str, visual: str) -> Image.Image:
    image = background()
    draw = ImageDraw.Draw(image)
    write_lines(draw, title, MARGIN, 48, W - 2 * MARGIN, 130, size=36, fill=CYAN)
    card = (MARGIN, 150, W - MARGIN, 960)
    panel(draw, card)
    inner_w = W - 2 * MARGIN - 96
    if visual.startswith("code title"):
        write_lines(draw, text, MARGIN + 48, 360, inner_w, 900, size=48)
    elif visual.startswith("code end"):
        lockup(draw, 260, 340)
        write_lines(draw, text, MARGIN + 48, 480, inner_w, 900, size=36)
    elif visual.startswith("code disclaimer"):
        write_lines(draw, text, MARGIN + 48, 240, inner_w, 900, size=36)
    elif visual.startswith("code skip"):
        write_lines(draw, "Skipped on purpose. The spot page stands.", MARGIN + 48, 360, inner_w, 700, size=42)
        write_lines(draw, text, MARGIN + 48, 620, inner_w, 900, size=28)
    else:
        picture(draw, text, visual, (MARGIN + 48, 190, W - MARGIN - 48, 560))
        write_lines(draw, text, MARGIN + 48, 600, inner_w, 920, size=28)
    footer(draw)
    return image


def paint_hero(title: str, label: str) -> Image.Image:
    image = background()
    draw = ImageDraw.Draw(image)
    write_lines(draw, title, MARGIN, 48, W - 2 * MARGIN, 130, size=36, fill=CYAN)
    panel(draw, (MARGIN, 150, W - MARGIN, 960))
    prices = spellings(label)
    if prices:
        rungs(draw, prices, (MARGIN + 48, 190, W - MARGIN - 48, 520), label)
        top = 560
    else:
        picture(draw, label, label, (MARGIN + 48, 200, W - MARGIN - 48, 480))
        top = 520
    write_lines(draw, label, MARGIN + 48, top, W - 2 * MARGIN - 96, 760, size=28)
    if "four questions" in label:
        questions = (
            "What is a limit order? "
            "Which side of 27,630 is the buy side? "
            "How many gaps are there between seven levels? "
            "What is ten crosses of the middle?"
        )
        write_lines(draw, questions, MARGIN + 48, 760, W - 2 * MARGIN - 96, 920, size=32)
    footer(draw)
    return image


def parse_table(text: str, heading: str) -> list[list[str]]:
    rows = []
    capture = False
    for line in text.splitlines():
        if line.startswith(heading):
            capture = True
            continue
        if capture and line.startswith("## "):
            break
        if not capture or not line.startswith("| "):
            continue
        if line.startswith("| File") or line.startswith("| #") or line.startswith("|---"):
            continue
        parts = [part.strip() for part in line.strip().strip("|").split("|")]
        rows.append(parts)
    return rows


def paint_lesson(number: str) -> dict:
    folder = OUT / f"BP-{number}"
    manifest_path = folder / "MANIFEST.md"
    text = manifest_path.read_text(encoding="utf-8")
    title = text.split("Title: ", 1)[1].splitlines()[0].strip()
    stills = folder / "stills"
    heroes = folder / "heroes"
    if stills.exists():
        shutil.rmtree(stills)
    if heroes.exists():
        shutil.rmtree(heroes)
    stills.mkdir()
    heroes.mkdir()
    code = 0
    slots = []
    for parts in parse_table(text, "## Hero cards"):
        name = parts[0].strip("`")
        label = parts[1]
        paint_hero(title, label).save(heroes / Path(name).name, optimize=True)
    for parts in parse_table(text, "## Beats"):
        number_id = int(parts[0])
        sentence = parts[3]
        visual = parts[4]
        chatgpt = parts[6]
        if chatgpt == "yes":
            slots.append(number_id)
            continue
        paint(title, sentence, visual).save(stills / f"{number_id:03d}.png", optimize=True)
        code += 1
    note = "Code stills are `stills/NNN.png`, where NNN is the beat number. A ChatGPT beat has no PNG. That beat number is the open slot."
    if note not in text:
        text = text.replace(
            "There is no corner EXAMPLE chip and no untaught figure. A number is on screen only when this beat says it.\n",
            "There is no corner EXAMPLE chip and no untaught figure. A number is on screen only when this beat says it.\n\n" + note + "\n",
        )
        manifest_path.write_text(text, encoding="utf-8")
    return {"code": code, "slots": len(slots), "heroes": len(list(heroes.glob('*.png')))}


def main() -> None:
    number = sys.argv[1]
    print(paint_lesson(number))


if __name__ == "__main__":
    main()
