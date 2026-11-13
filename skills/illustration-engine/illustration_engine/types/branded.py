"""Title cards, lesson covers, and section dividers. No lockup, no byline."""

from __future__ import annotations

from .common import labels_or, take_headline
from .mascot import draw_mascot


def _title(params: dict, default: str) -> str:
    return str(params.get("title") or params.get("headline") or default)


def _subtitle(canvas, text: str, x: float, y: float) -> None:
    t = canvas.theme
    canvas.text(text, x, y, t.label, t.muted, weight="bold", role="subtitle", bg=t.bg0)


def draw_title(canvas, params: dict) -> None:
    title = _title(params, "INTRODUCTION")
    canvas.headline(title)
    names = labels_or(params, ["START", "HERE"])
    x, y, w, h = canvas.content_rect()
    t = canvas.theme
    _subtitle(canvas, str(params.get("subtitle") or "ONE IDEA"), x, y + t.s(28))
    canvas.glass(x, y + t.s(56), w * 0.62, h - t.s(70))
    top = y + h * 0.42
    bot = y + h * 0.72
    canvas.glow_line(x + t.s(36), top, x + w * 0.56, top, t.accent, sw=t.s(2.4), dash="7 7")
    canvas.glow_line(x + t.s(36), bot, x + w * 0.56, bot, t.accent, sw=t.s(2.4), dash="7 7")
    canvas.glow_polyline(
        [
            (x + t.s(48), (top + bot) / 2),
            (x + w * 0.18, top + t.s(16)),
            (x + w * 0.34, bot - t.s(16)),
            (x + w * 0.52, (top + bot) / 2),
        ],
        t.accent,
        sw=t.s(3),
    )
    canvas.chip(names[0], x + w * 0.72, y + h * 0.4)
    if len(names) > 1:
        canvas.chip(names[1], x + w * 0.72, y + h * 0.62)


def draw_cover(canvas, params: dict) -> None:
    title = _title(params, "THE RANGE")
    canvas.headline(title)
    names = labels_or(params, ["LESSON", "START"])
    x, y, w, h = canvas.content_rect()
    t = canvas.theme
    _subtitle(canvas, str(params.get("subtitle") or "A WORKED PICTURE"), x, y + t.s(8))
    card_w = w * 0.56
    canvas.glass(x, y + t.s(48), card_w, h - t.s(64))
    top = y + h * 0.38
    bot = y + h * 0.7
    canvas.glow_line(x + t.s(28), top, x + card_w - t.s(28), top, t.accent, sw=t.s(2.4), dash="7 7")
    canvas.glow_line(x + t.s(28), bot, x + card_w - t.s(28), bot, t.accent, sw=t.s(2.4), dash="7 7")
    canvas.glow_polyline(
        [
            (x + t.s(40), (top + bot) / 2 + t.s(8)),
            (x + card_w * 0.28, top + t.s(18)),
            (x + card_w * 0.55, bot - t.s(14)),
            (x + card_w - t.s(36), (top + bot) / 2),
        ],
        t.accent,
        sw=t.s(3.2),
    )
    canvas.chip(names[0], x + t.s(36), y + t.s(78), anchor="start")
    if len(names) > 1:
        canvas.chip(names[1], x + card_w - t.s(36), y + h - t.s(48), anchor="end")
    scale = min((h * 0.92) / 280, (w * 0.34) / 180)
    draw_mascot(canvas, x + w - 190 * scale, y + (h - 280 * scale) * 0.55, scale, "pointing")


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
    canvas.text(word, x + w / 2, y + h * 0.48, size, t.ink, weight="condensed", anchor="middle", role="headline", bg=t.bg0)
    canvas.svg.line(x + w * 0.3, y + h * 0.62, x + w * 0.7, y + h * 0.62, t.accent, sw=4)
    canvas.chip(names[0], x + w * 0.32, y + h * 0.74, anchor="middle")
    if len(names) > 1:
        canvas.chip(names[1], x + w * 0.68, y + h * 0.74, anchor="middle")
