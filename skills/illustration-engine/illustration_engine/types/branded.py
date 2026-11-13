"""Title cards, lesson covers, and section dividers. No lockup, no byline."""

from __future__ import annotations

from .common import labels_or, take_headline
from .mascot import draw_mascot


def _title(params: dict, default: str) -> str:
    return str(params.get("title") or params.get("headline") or default)


def draw_title(canvas, params: dict) -> None:
    title = _title(params, "INTRODUCTION")
    canvas.headline(title)
    names = labels_or(params, ["START", "HERE"])
    x, y, w, h = canvas.content_rect()
    t = canvas.theme
    canvas.svg.line(x, y + h * 0.42, x + w * 0.42, y + h * 0.42, t.accent, sw=4)
    canvas.chip(names[0], x + 70, y + h * 0.58, anchor="start")
    if len(names) > 1:
        canvas.chip(names[1], x + 280, y + h * 0.58, anchor="start")


def draw_cover(canvas, params: dict) -> None:
    title = _title(params, "THE RANGE")
    canvas.headline(title)
    names = labels_or(params, ["LESSON", "START"])
    x, y, w, h = canvas.content_rect()
    t = canvas.theme
    canvas.svg.line(x, y + 20, x + min(420, w * 0.4), y + 20, t.accent, sw=4)
    canvas.chip(names[0], x + 80, y + 90, anchor="start")
    if len(names) > 1:
        canvas.chip(names[1], x + 80, y + 170, anchor="start")
    scale = min(1.25, (h - 20) / 280)
    draw_mascot(canvas, x + w - 220 * scale, y + h - 280 * scale, scale, "pointing")


def draw_divider(canvas, params: dict) -> None:
    title = _title(params, "NEXT")
    words = title.upper().split()
    word = words[-1] if words else "NEXT"
    # The divider is the one idea: a single large word, plus two short labels.
    canvas.headline(word if len(words) == 1 else title)
    names = labels_or(params, ["PART", "NEXT"])
    x, y, w, h = canvas.content_rect()
    t = canvas.theme
    size = min(160, int(w / max(4, len(word))))
    while size > t.min_font and canvas.measure(word, size, "bold") > w - 40:
        size -= 6
    canvas.text(word, x + w / 2, y + h * 0.48, size, t.ink, weight="bold", anchor="middle", role="headline", bg=t.bg0)
    canvas.svg.line(x + w * 0.3, y + h * 0.62, x + w * 0.7, y + h * 0.62, t.accent, sw=4)
    canvas.chip(names[0], x + w * 0.32, y + h * 0.74, anchor="middle")
    if len(names) > 1:
        canvas.chip(names[1], x + w * 0.68, y + h * 0.74, anchor="middle")
