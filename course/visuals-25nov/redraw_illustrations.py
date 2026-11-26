"""Redraw ChatGPT-yes stills so they meet the Creative Studio rules.

No mascot, no people, no red, no slogan chip, and no reprint of the spoken
sentence. A spoken count or sum is drawn as digits and marked EXAMPLE.
Margins stay at 96 px. Candles are not drawn.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

from PIL import Image, ImageDraw

import build_visuals as bv

OUT = Path(__file__).resolve().parent

ONES = {
    "zero": 0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6,
    "seven": 7, "eight": 8, "nine": 9, "ten": 10, "eleven": 11, "twelve": 12,
}
TENS = {
    "twenty": 20, "thirty": 30, "forty": 40, "fifty": 50, "sixty": 60,
    "seventy": 70, "eighty": 80, "ninety": 90,
}
WORDS = set(ONES) | set(TENS) | {"hundred", "thousand", "and", "a"}


def number_runs(text: str) -> list[int]:
    tokens = re.findall(r"[a-z0-9]+", text.lower().replace("-", " "))
    values: list[int] = []
    total = 0
    current = 0
    in_run = False

    def flush() -> None:
        nonlocal total, current, in_run
        if in_run:
            values.append(total + current)
        total = 0
        current = 0
        in_run = False

    for token in tokens:
        if token in ONES:
            current += ONES[token]
            in_run = True
        elif token in TENS:
            current += TENS[token]
            in_run = True
        elif token == "hundred" and in_run:
            current = max(current, 1) * 100
        elif token == "thousand" and in_run:
            current = max(current, 1) * 1000
            total += current
            current = 0
        elif token == "and" and in_run and (current >= 100 or total > 0):
            continue
        elif token == "a" and in_run:
            continue
        else:
            flush()
    flush()
    return values


def fmt(value: int) -> str:
    if value >= 1000:
        return f"{value:,}"
    return str(value)


def expression(text: str, values: list[int]) -> str:
    low = text.lower()
    if len(values) >= 3 and "minus" in low and values[0] - values[1] == values[2]:
        return f"{fmt(values[0])}  −  {fmt(values[1])}  =  {fmt(values[2])}"
    if len(values) >= 2 and "minus" in low:
        return f"{fmt(values[0])}  −  {fmt(values[1])}"
    if len(values) >= 2 and ("divided" in low or "split" in low):
        line = f"{fmt(values[0])}  ÷  {fmt(values[1])}"
        if len(values) >= 3:
            line += f"  =  about {fmt(values[2])}"
        return line
    if "not four and four" in low and 8 in values and 5 in values:
        return "8 near the top    5 near the bottom    not 4 and 4"
    if "seven" in low and "six" in low and ("gap" in low or "space" in low):
        return "7 lines    6 gaps"
    if "eight" in low and "five" in low and "top" in low:
        return "8 near the top    5 near the bottom"
    return ""


def concept(text: str) -> tuple[str, str]:
    low = text.lower()
    rules = [
        (("could lose", "past performance", "not a reliable"), ("Money put in can be lost", "risk")),
        (("not a promise", "not a forecast", "hindsight"), ("Not a promise", "hindsight")),
        (("not sorted",), ("Not sorted", "label")),
        (("do not send", "sends nothing", "nothing is sent", "no order"), ("Nothing is sent", "closed")),
        (("size", "blank"), ("Size stays blank", "blank")),
        (("finish", "before"), ("Finish, then the start", "order")),
        (("three question",), ("Three questions", "questions")),
        (("gap",), ("Count the gaps", "gap")),
        (("inside", "outside"), ("Inside or outside", "close")),
        (("daily closing", "last price", "utc"), ("End of the UTC day", "close")),
        (("borrow", "multiple", "contract"), ("Spot. Not borrowed.", "spot")),
        (("spot",), ("Spot. Coins you hold.", "spot")),
        (("second page", "page two", "two pages", "two boxes"), ("A second page", "pages")),
        (("stop",), ("The written stop", "stop")),
        (("fee",), ("The fee is a cost", "fee")),
        (("choosing those lines",), ("Choose the lines and the width", "gap")),
        (("as a percent",), ("The step as a percent", "gap")),
        (("where the page ends",), ("Where the page ends", "stop")),
        (("rule that ends",), ("Name the rule that ends it", "stop")),
        (("not to chase",), ("Point at it. Do not chase it.", "close")),
        (("throw the sentence",), ("Do not throw the sentence away", "stop")),
        (("cannot end",), ("A page with no exit", "blank")),
        (("third date",), ("No third date", "close")),
        (("eyes off",), ("Both dates, eyes off the chart", "close")),
        (("not affiliated",), ("Not affiliated with an exchange", "closed")),
        (("exchange is an app",), ("An exchange is where people trade", "closed")),
        (("does not match the page",), ("If it does not match, do not send", "closed")),
        (("does not teach", "does not recommend"), ("Not taught. Not recommended.", "spot")),
        (("quote is what you pay",), ("Bitcoin. Paid in US dollars.", "spot")),
        (("do not press that confirm", "confirm button"), ("Do not press confirm", "closed")),
        (("what do you send",), ("Send nothing", "closed")),
        (("point at on the notebook",), ("Only what you can point at", "paper")),
        (("sits on either line", "on either line"), ("On the line is still inside", "close")),
        (("already wrote",), ("The sentence already written", "stop")),
        (("alert service", "does not send one"), ("No alert is sent", "closed")),
        (("not a grade",), ("Not a grade", "hindsight")),
        (("and then what",), ("The action is already written", "stop")),
        (("habit for that page",), ("The habit ends", "stop")),
        (("not a grade of you",), ("A check, not a grade", "hindsight")),
        (("wrong page and a corrected",), ("Wrong page, then the fix", "pages")),
        (("not show what you made", "does not show what you made"), ("A public window. Not a score.", "hindsight")),
        (("keep the date",), ("Keep the date", "close")),
        (("fix them together",), ("One fix at a time", "order")),
        (("path is the judge",), ("The path is the judge", "close")),
        (("rounder than that path",), ("Rounder than the path is wrong", "close")),
        (("place to be written",), ("A place for the sentence", "paper")),
        (("buckets are mixed",), ("Keep the two pages apart", "pages")),
        (("next lesson closed",), ("This page can stand alone", "closed")),
        (("not money you made",), ("Not money you made", "hindsight")),
        (("sit in cash",), ("Cash, or the coin", "spot")),
        (("never share",), ("Never share the API secret", "closed")),
        (("example",), ("Example", "mark")),
        (("paper", "pretend"), ("Practice on paper", "paper")),
    ]
    best = None
    best_len = 0
    for keys, result in rules:
        for key in keys:
            if key in low and len(key) > best_len:
                best = result
                best_len = len(key)
    return best or ("This beat", "mark")


def paint(sentence: str) -> Image.Image:
    image = bv.background()
    draw = ImageDraw.Draw(image)
    # 96 px safe margin. Nothing is drawn outside it.
    left, top, right, bottom = 96, 96, bv.W - 96, bv.H - 96
    bv.panel(draw, (left, top, right, bottom))
    title, kind = concept(sentence)
    values = number_runs(sentence)
    expr = expression(sentence, values)
    draw.text((left + 48, top + 36), "EXAMPLE" if expr else title, font=bv.font(40), fill=bv.CYAN)
    y = top + 110
    if expr:
        draw.text((left + 48, y), expr, font=bv.font(48 if len(expr) > 24 else 64), fill=bv.WHITE)
        y += 100
        if title not in {"This beat", "Example"}:
            draw.text((left + 48, y), title, font=bv.font(36), fill=bv.WHITE)
            y += 64
    diagram(draw, kind, (left + 48, y + 16, right - 48, bottom - 48))
    return image


def diagram(draw: ImageDraw.ImageDraw, kind: str, box) -> None:
    x0, y0, x1, y1 = box
    if y1 - y0 < 80:
        return
    mid = (y0 + y1) // 2
    if kind == "gap":
        draw.line([(x0, y0 + 20), (x1, y0 + 20)], fill=bv.CYAN, width=6)
        draw.line([(x0, y1 - 20), (x1, y1 - 20)], fill=bv.CYAN, width=6)
        draw.text((x0, mid - 24), "Gap", font=bv.font(40), fill=bv.WHITE)
    elif kind == "close":
        draw.line([(x0, y0 + 30), (x1, y0 + 30)], fill=bv.CYAN, width=4)
        draw.line([(x0, y1 - 30), (x1, y1 - 30)], fill=bv.CYAN, width=4)
        draw.ellipse([x0 + 80, mid - 16, x0 + 112, mid + 16], fill=bv.WHITE)
        draw.text((x0 + 140, mid - 20), "UTC close", font=bv.font(32), fill=bv.WHITE)
    elif kind == "stop":
        draw.line([(x0, mid), (x1, mid)], fill=bv.CYAN, width=8)
        draw.text((x0, mid + 24), "Written before the start", font=bv.font(32), fill=bv.WHITE)
    elif kind == "pages":
        draw.rounded_rectangle([x0, y0, x0 + 360, y1], 16, outline=bv.CYAN, width=3)
        draw.rounded_rectangle([x0 + 420, y0, x0 + 780, y1], 16, outline=bv.WHITE, width=3)
        draw.text((x0 + 36, y0 + 24), "Page one", font=bv.font(32), fill=bv.CYAN)
        draw.text((x0 + 456, y0 + 24), "Page two", font=bv.font(32), fill=bv.WHITE)
    elif kind == "spot":
        draw.text((x0, y0), "Spot", font=bv.font(48), fill=bv.WHITE)
        draw.text((x0 + 420, y0), "Not borrowed", font=bv.font(40), fill=bv.CYAN)
    elif kind == "questions":
        for index, line in enumerate(("Inside or outside", "Which side", "Rule still in force")):
            draw.text((x0, y0 + index * 70), f"{index + 1}   {line}", font=bv.font(36), fill=bv.WHITE)
    elif kind == "blank":
        draw.text((x0, y0), "Size", font=bv.font(36), fill=bv.CYAN)
        draw.line([(x0, y0 + 70), (x0 + 480, y0 + 70)], fill=bv.WHITE, width=3)
        draw.text((x0, y0 + 90), "Left blank", font=bv.font(32), fill=bv.WHITE)
    elif kind == "closed":
        draw.rounded_rectangle([x0, y0, x0 + 520, y0 + 180], 16, outline=bv.CYAN, width=4)
        draw.text((x0 + 36, y0 + 60), "Not sent", font=bv.font(48), fill=bv.WHITE)
    elif kind == "risk":
        draw.line([(x0, y0 + 20), (x0 + 520, y1 - 10)], fill=bv.CYAN, width=6)
    elif kind == "hindsight":
        draw.text((x0, y0), "This window only", font=bv.font(40), fill=bv.WHITE)
    elif kind == "order":
        draw.text((x0, y0), "1  Finish", font=bv.font(40), fill=bv.WHITE)
        draw.text((x0, y0 + 70), "2  Before", font=bv.font(40), fill=bv.CYAN)
    elif kind == "fee":
        draw.text((x0, y0), "A cost on the trade", font=bv.font(40), fill=bv.WHITE)
    else:
        draw.rounded_rectangle([x0, y0, x0 + 280, y0 + 120], 12, outline=bv.CYAN, width=3)


def beats(number: str) -> list[tuple[str, str]]:
    text = (OUT / f"BP-{number}" / "MANIFEST.md").read_text(encoding="utf-8")
    rows = []
    for line in text.splitlines():
        parts = [part.strip() for part in line.strip().strip("|").split("|")]
        if len(parts) >= 9 and parts[0].isdigit() and parts[6] == "yes":
            rows.append((f"{int(parts[0]):03d}", parts[3]))
    return rows


def redraw(number: str) -> int:
    count = 0
    dest = OUT / f"BP-{number}" / "stills"
    for beat, sentence in beats(number):
        paint(sentence).save(dest / f"{beat}.png", optimize=True)
        count += 1
    return count


def main() -> None:
    for number in sys.argv[1:]:
        print(f"BP-{number} illustrations {redraw(number)}", flush=True)


if __name__ == "__main__":
    main()
