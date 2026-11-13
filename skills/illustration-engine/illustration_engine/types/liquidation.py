"""Entry, liquidation line, and the danger band between them."""

from __future__ import annotations

from .common import fnum, labels_or, take_headline


def draw_liquidation(canvas, params: dict) -> None:
    take_headline(canvas, params, "LIQUIDATION LINE")
    entry = fnum(params, "entry", 100)
    liq = fnum(params, "liquidation", 80)
    mark = fnum(params, "price", (entry + liq) / 2)
    leverage = params.get("leverage", 5)
    x, y, w, h = canvas.content_rect()
    canvas.glass(x, y, w, h)
    left, right = x + 180, x + w - 160
    top, bottom = y + 48, y + h - 48
    lo = min(entry, liq, mark)
    hi = max(entry, liq, mark)
    span = hi - lo or 1
    lo -= span * 0.25
    hi += span * 0.25

    def y_of(value: float) -> float:
        return canvas.plot_y(value, lo, hi, top, bottom, pad=12)

    y_entry, y_liq, y_mark = y_of(entry), y_of(liq), y_of(mark)
    band_top, band_bot = min(y_entry, y_liq), max(y_entry, y_liq)
    canvas.svg.rect(left, band_top, right - left, band_bot - band_top, fill=canvas.theme.danger, opacity=0.28, rx=8)
    t = canvas.theme
    canvas.svg.line(left, y_entry, right, y_entry, t.accent, sw=2.5)
    canvas.svg.line(left, y_liq, right, y_liq, t.danger, sw=2.5, dash="8 6")
    canvas.svg.circle(left + (right - left) * 0.62, y_mark, 9, fill=t.ink)
    names = labels_or(params, ["ENTRY", "DANGER", "LIQUIDATION"])
    canvas.chip(names[0], x + 100, y_entry, anchor="end")
    canvas.leader(x + 108, y_entry, left, y_entry)
    if len(names) > 1:
        canvas.chip(names[1], (left + right) / 2, (band_top + band_bot) / 2)
    if len(names) > 2:
        canvas.chip(names[2], right + 24, y_liq, anchor="start")
        canvas.leader(right, y_liq, right + 16, y_liq)
    try:
        lev = int(float(leverage))
    except (TypeError, ValueError):
        lev = 5
    canvas.text(f"{lev}X", right - 8, top + 28, t.label, t.danger_ink, weight="bold", anchor="end", role="price", bg=t.card)
    canvas.watermark(x + w / 2, y + h / 2 + 20)
    canvas.stamp_example()
