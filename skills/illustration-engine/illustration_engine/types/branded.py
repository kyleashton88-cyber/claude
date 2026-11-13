"""Title cards, lesson covers, and section dividers. No lockup, no byline."""

from __future__ import annotations

from .common import labels_or, take_headline
from ..fonts import family


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
    canvas.glass(x, y + t.s(48), w, h - t.s(56))
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
    canvas.glass(x, y + t.s(8), w, h - t.s(16))
    _subtitle(canvas, str(params.get("subtitle") or "A WORKED PICTURE"), x + t.s(28), y + t.s(52))
    card_right = x + w * 0.62
    top = y + h * 0.28
    bot = y + h * 0.78
    canvas.glow_line(x + t.s(36), top, card_right - t.s(24), top, t.accent, sw=t.s(2.6), dash="8 7")
    canvas.glow_line(x + t.s(36), bot, card_right - t.s(24), bot, t.accent, sw=t.s(2.6), dash="8 7")
    canvas.glow_polyline(
        [
            (x + t.s(48), (top + bot) / 2 + t.s(10)),
            (x + w * 0.16, top + t.s(22)),
            (x + w * 0.32, bot - t.s(18)),
            (x + w * 0.48, (top + bot) / 2 - t.s(6)),
            (card_right - t.s(36), (top + bot) / 2 + t.s(8)),
        ],
        t.accent,
        sw=t.s(3.4),
    )
    canvas.svg.line(x + t.s(18), y + t.s(28), x + t.s(18), y + h - t.s(36), t.accent, sw=t.s(3), opacity=0.7)
    canvas.svg.line(x + w - t.s(18), y + t.s(28), x + w - t.s(18), y + h - t.s(36), t.rim, sw=t.s(3), opacity=0.45)
    canvas.chip(names[0], x + t.s(48), top - t.s(28), anchor="start")
    if len(names) > 1:
        canvas.chip(names[1], x + t.s(48), bot + t.s(36), anchor="start")
    canvas.character = "withheld"
    canvas.svg.comment("character: withheld; cover does not invent a mascot")


def draw_divider(canvas, params: dict) -> None:
    title = _title(params, "NEXT")
    words = title.upper().split()
    word = words[-1] if words else "NEXT"
    # The divider is the one idea: a single large word, plus two short labels.
    canvas.headline(word if len(words) == 1 else title)
    names = labels_or(params, ["PART", "NEXT"])
    x, y, w, h = canvas.content_rect()
    t = canvas.theme
    canvas.glass(x + w * 0.08, y, w * 0.84, h * 0.86)
    size = min(int(t.s(150)), int(w / max(4, len(word))))
    bloom = canvas.svg.ensure_glow(t.glow_std())
    while size > t.min_font and canvas.measure(word, size, "condensed") > w - 40:
        size -= 6
    canvas.svg.text(word, x + w / 2, y + h * 0.48, size, t.accent, family("condensed"), anchor="middle", weight="700", opacity=0.9, filt=bloom)
    canvas.text(word, x + w / 2, y + h * 0.48, size, t.ink, weight="condensed", anchor="middle", role="headline", bg=t.bg0)
    canvas.glow_line(x + w * 0.22, y + h * 0.62, x + w * 0.78, y + h * 0.62, t.accent, sw=t.s(3))
    canvas.chip(names[0], x + w * 0.32, y + h * 0.74, anchor="middle")
    if len(names) > 1:
        canvas.chip(names[1], x + w * 0.68, y + h * 0.74, anchor="middle")
