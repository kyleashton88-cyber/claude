"""Bespoke BP-05 stills. Each beat draws its own idea. Not a shared text card."""

from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image, ImageDraw

import build_visuals as bv
import redraw_illustrations as base

OUT = Path(__file__).resolve().parent
PAST = "Past performance is not a reliable indicator of future results."


def _canvas() -> tuple[Image.Image, ImageDraw.ImageDraw]:
    image = bv.background()
    draw = ImageDraw.Draw(image)
    bv.panel(draw, (96, 96, bv.W - 96, bv.H - 96))
    return image, draw


def _title(draw, text: str, y: int = 120) -> None:
    draw.text((140, y), text, font=bv.font(40), fill=bv.WHITE)


def _label(draw, xy, text: str, fill=bv.CYAN, size: int = 32) -> None:
    draw.text(xy, text, font=bv.font(size), fill=fill)


def _ladder(draw, x, y, n, gap_labels: bool) -> None:
    for i in range(n):
        yy = y + i * 56
        draw.line([(x, yy), (x + 520, yy)], fill=bv.CYAN, width=4)
        if gap_labels and i < n - 1:
            _label(draw, (x + 540, yy + 12), "gap", size=28)


def paint(beat: str, sentence: str) -> Image.Image:
    image, draw = _canvas()
    if beat == "003":
        _title(draw, "Money put in can be lost")
        draw.line([(180, 280), (900, 720)], fill=bv.CYAN, width=8)
        _label(draw, (140, 820), PAST, bv.WHITE, 28)
        return image
    if beat == "005":
        _title(draw, "Daily close, inside or outside")
        draw.line([(200, 360), (1500, 360)], fill=bv.CYAN, width=4)
        draw.line([(200, 640), (1500, 640)], fill=bv.CYAN, width=4)
        draw.ellipse([980, 470, 1020, 510], fill=bv.WHITE)
        _label(draw, (1060, 470), "Inside", bv.WHITE, 32)
        draw.ellipse([1280, 280, 1320, 320], outline=bv.WHITE, width=4)
        _label(draw, (1360, 280), "Outside", bv.WHITE, 32)
        _label(draw, (200, 760), "No order is sent from this lesson.", bv.WHITE, 32)
        return image
    if beat == "006":
        _title(draw, "Gap and step")
        draw.line([(240, 340), (1200, 340)], fill=bv.CYAN, width=6)
        draw.line([(240, 620), (1200, 620)], fill=bv.CYAN, width=6)
        draw.line([(1280, 340), (1280, 620)], fill=bv.WHITE, width=6)
        _label(draw, (300, 450), "Gap  =  the space", bv.WHITE, 40)
        _label(draw, (1320, 460), "Step  =  the width", bv.CYAN, 32)
        return image
    if beat == "008":
        _title(draw, "Choose the lines from the path")
        pts = [(200, 640), (480, 420), (760, 560), (1040, 300), (1400, 480)]
        draw.line(pts, fill=bv.WHITE, width=6)
        draw.line([(200, 300), (1500, 300)], fill=bv.CYAN, width=4)
        draw.line([(200, 700), (1500, 700)], fill=bv.CYAN, width=4)
        _label(draw, (1520, 280), "Top", size=32)
        _label(draw, (1520, 680), "Bottom", size=32)
        return image
    if beat == "009":
        _title(draw, "Nothing is sent")
        draw.rounded_rectangle([200, 280, 900, 760], 18, outline=bv.CYAN, width=4)
        _label(draw, (260, 360), "EXAMPLE", bv.CYAN, 48)
        _label(draw, (260, 460), "A teaching figure", bv.WHITE, 36)
        draw.line([(1100, 400), (1500, 640)], fill=bv.CYAN, width=8)
        _label(draw, (1100, 680), "No order", bv.WHITE, 36)
        return image
    if beat == "010":
        _title(draw, "Count the gaps")
        _ladder(draw, 240, 280, 7, True)
        _label(draw, (1100, 400), "Not the lines", bv.WHITE, 40)
        _label(draw, (1100, 480), "The spaces", bv.CYAN, 40)
        return image
    if beat == "013":
        _title(draw, "End of the UTC day")
        draw.line([(200, 520), (1600, 520)], fill=bv.CYAN, width=4)
        _label(draw, (200, 440), "00:00", bv.WHITE, 32)
        _label(draw, (1480, 440), "24:00", bv.WHITE, 32)
        draw.ellipse([1540, 496, 1588, 544], fill=bv.WHITE)
        _label(draw, (200, 640), "Last price of the day", bv.WHITE, 36)
        return image
    if beat == "018":
        _title(draw, "EXAMPLE  5,401")
        _ladder(draw, 200, 260, 7, False)
        _label(draw, (900, 360), "Seven prices", bv.WHITE, 40)
        _label(draw, (900, 440), "Six spaces", bv.CYAN, 40)
        return image
    if beat == "020":
        _title(draw, "Seven lines make six gaps")
        _ladder(draw, 220, 280, 7, True)
        _label(draw, (1000, 400), "Not seven gaps", bv.WHITE, 40)
        _label(draw, (1000, 480), "EXAMPLE  6", bv.CYAN, 48)
        return image
    if beat == "021":
        _title(draw, "A fee is a charge")
        draw.rounded_rectangle([200, 300, 820, 520], 16, outline=bv.CYAN, width=3)
        _label(draw, (240, 370), "Order trades", bv.WHITE, 36)
        draw.line([(860, 400), (1100, 400)], fill=bv.WHITE, width=6)
        draw.rounded_rectangle([1140, 320, 1680, 500], 16, outline=bv.CYAN, width=3)
        _label(draw, (1180, 380), "Charge", bv.CYAN, 40)
        _label(draw, (200, 640), "Not a shortcut from the middle line.", bv.WHITE, 32)
        return image
    if beat == "022":
        _title(draw, "Teaching cost, not an app fee")
        draw.rounded_rectangle([200, 320, 900, 700], 16, outline=bv.CYAN, width=4)
        _label(draw, (260, 400), "EXAMPLE", bv.CYAN, 40)
        _label(draw, (260, 480), "Cost already used", bv.WHITE, 36)
        _label(draw, (1040, 420), "Not copied from an app", bv.WHITE, 32)
        return image
    if beat == "035":
        _title(draw, "Move the top, then count again")
        draw.line([(200, 420), (1000, 420)], fill=bv.WHITE, width=3)
        draw.line([(200, 300), (1000, 300)], fill=bv.CYAN, width=6)
        _label(draw, (1040, 280), "Real high", size=32)
        _label(draw, (200, 700), "Then count the gaps again.", bv.WHITE, 32)
        return image
    if beat == "036":
        _title(draw, "Check top and bottom once")
        pts = [(220, 700), (500, 480), (780, 620), (1100, 300), (1460, 520)]
        draw.line(pts, fill=bv.WHITE, width=5)
        draw.line([(220, 280), (1500, 280)], fill=bv.CYAN, width=4)
        draw.line([(220, 760), (1500, 760)], fill=bv.CYAN, width=4)
        _label(draw, (200, 820), "Once. Not day by day.", bv.WHITE, 32)
        return image
    if beat == "038":
        _title(draw, "Top is too low")
        draw.line([(200, 480), (1100, 480)], fill=bv.WHITE, width=4)
        draw.line([(200, 320), (1100, 320)], fill=bv.CYAN, width=6)
        _label(draw, (1140, 300), "Move it up", bv.CYAN, 36)
        _label(draw, (200, 640), "Then count the gaps again.", bv.WHITE, 32)
        return image
    if beat == "039":
        _title(draw, "Two ways to space a ladder")
        _ladder(draw, 180, 300, 5, False)
        _label(draw, (180, 600), "Equal dollars", bv.WHITE, 32)
        x = 1000
        for i, gap in enumerate((40, 70, 50, 90)):
            yy = 300 + sum((40, 70, 50, 90)[:i])
            draw.line([(x, yy), (x + 420, yy)], fill=bv.CYAN, width=4)
        _label(draw, (1000, 640), "Equal percent", bv.CYAN, 32)
        return image
    if beat == "049":
        _title(draw, "Know which spacing you wrote")
        draw.rounded_rectangle([180, 300, 820, 700], 16, outline=bv.CYAN, width=3)
        _label(draw, (220, 400), "Dollars", bv.WHITE, 40)
        draw.rounded_rectangle([980, 300, 1620, 700], 16, outline=bv.WHITE, width=3)
        _label(draw, (1020, 400), "Percent", bv.CYAN, 40)
        _label(draw, (220, 760), "Not both on one page.", bv.WHITE, 32)
        return image
    if beat == "050":
        _title(draw, "The summer step as a percent")
        _label(draw, (200, 360), "EXAMPLE", bv.CYAN, 40)
        _label(draw, (200, 440), "Compare with the cost", bv.WHITE, 40)
        _label(draw, (200, 560), "Not a new plan", bv.WHITE, 32)
        return image
    if beat == "054":
        _title(draw, "A recount, not an app fee")
        draw.rounded_rectangle([200, 300, 1000, 720], 16, outline=bv.CYAN, width=4)
        _label(draw, (260, 380), "EXAMPLE", bv.CYAN, 48)
        _label(draw, (260, 480), "Public window", bv.WHITE, 36)
        _label(draw, (1100, 420), "Not a fee from an app", bv.WHITE, 32)
        return image
    if beat == "064":
        _title(draw, "Seven lines, not seven spaces")
        _ladder(draw, 200, 280, 7, False)
        _label(draw, (900, 360), "Lines named: 7", bv.WHITE, 36)
        _label(draw, (900, 440), "Spaces: 6", bv.CYAN, 40)
        return image
    if beat == "069":
        _title(draw, "Not money you made")
        draw.rounded_rectangle([200, 320, 900, 640], 16, outline=bv.CYAN, width=3)
        _label(draw, (260, 420), "Not an app fee", bv.WHITE, 36)
        _label(draw, (1000, 420), "Not a result", bv.CYAN, 36)
        return image
    if beat == "073":
        _title(draw, "Summer ladder: count the gaps")
        _ladder(draw, 200, 280, 7, True)
        _label(draw, (1000, 400), "Do not multiply", bv.WHITE, 36)
        return image
    if beat == "075":
        _title(draw, "How many gaps?")
        _ladder(draw, 200, 260, 7, True)
        _label(draw, (1000, 400), "EXAMPLE  6", bv.CYAN, 64)
        _label(draw, (1000, 500), "Between seven lines", bv.WHITE, 32)
        return image
    if beat == "082":
        _title(draw, "The gap is the space")
        draw.line([(200, 400), (1400, 400)], fill=bv.CYAN, width=6)
        draw.line([(200, 560), (1400, 560)], fill=bv.CYAN, width=6)
        _label(draw, (400, 450), "Space", bv.WHITE, 40)
        _label(draw, (200, 700), "Do not walk the days again.", bv.WHITE, 32)
        return image
    if beat == "085":
        _title(draw, "Write Example. Send nothing.")
        _label(draw, (200, 340), "EXAMPLE", bv.CYAN, 56)
        _label(draw, (200, 460), "A recount is not a live plan.", bv.WHITE, 36)
        draw.line([(1200, 360), (1600, 560)], fill=bv.CYAN, width=8)
        _label(draw, (1200, 600), "No order", bv.WHITE, 36)
        return image
    if beat == "086":
        _title(draw, "Recap")
        draw.line([(200, 320), (1100, 320)], fill=bv.CYAN, width=6)
        _label(draw, (1140, 300), "Real high", size=32)
        draw.line([(200, 640), (1100, 640)], fill=bv.CYAN, width=6)
        _label(draw, (1140, 620), "Real low", size=32)
        _label(draw, (200, 760), "Then count the gaps.", bv.WHITE, 36)
        return image
    if beat == "088":
        _title(draw, "EXAMPLE  equal dollars")
        _ladder(draw, 240, 300, 6, False)
        _label(draw, (1000, 400), "Equal dollars", bv.WHITE, 40)
        _label(draw, (1000, 480), "Not equal percent", bv.CYAN, 32)
        return image
    if beat == "090":
        _title(draw, "Finish rule first. Size stays blank.")
        draw.rounded_rectangle([200, 300, 1500, 760], 16, outline=bv.CYAN, width=3)
        _label(draw, (260, 360), "Finish rule", bv.WHITE, 36)
        _label(draw, (260, 460), "Written before the start", bv.CYAN, 32)
        draw.line([(260, 600), (900, 600)], fill=bv.WHITE, width=3)
        _label(draw, (260, 620), "Size  —  left blank", bv.WHITE, 32)
        return image
    _title(draw, sentence[:48])
    return image


def main() -> None:
    dest = OUT / "BP-05" / "stills"
    dest.mkdir(parents=True, exist_ok=True)
    for beat, sentence in base.beats("05"):
        paint(beat, sentence).save(dest / f"{beat}.png")
        print(beat, flush=True)


if __name__ == "__main__":
    sys.path.insert(0, str(OUT))
    main()
