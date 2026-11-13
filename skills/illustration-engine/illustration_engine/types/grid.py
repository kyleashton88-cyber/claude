"""A grid ladder: even rungs, buys below the mark, sells above."""

from __future__ import annotations

from .common import fnum, inum, labels_or, take_headline


def draw_grid(canvas, params: dict) -> None:
    take_headline(canvas, params, "GRID LADDER")
    low = fnum(params, "low", fnum(params, "range_low", 90))
    high = fnum(params, "high", fnum(params, "range_high", 110))
    if low > high:
        low, high = high, low
    if high == low:
        high = low + 1
    gaps = max(2, min(16, inum(params, "grids", 10)))
    price = fnum(params, "price", (low + high) / 2)
    x, y, w, h = canvas.content_rect()
    canvas.glass(x, y, w, h)
    left, right = x + 150, x + w - 120
    top, bottom = y + 64, y + h - 48
    lines = gaps + 1
    ys = []
    for i in range(lines):
        value = low + (high - low) * i / gaps
        ys.append(canvas.plot_y(value, low, high, top, bottom, pad=16))
    t = canvas.theme
    for gy in ys:
        canvas.glow_line(left, gy, right, gy, t.accent, sw=t.s(1.7))
    price_y = canvas.plot_y(min(high, max(low, price)), low, high, top, bottom, pad=16)
    canvas.glow_line(left - 16, price_y, right + 16, price_y, t.blue, sw=t.s(2.8))
    buy_at = None
    sell_at = None
    fills = set(params.get("fills") or [])
    buy_x = left + 70
    sell_x = right - 70
    for i, gy in enumerate(ys):
        value = low + (high - low) * i / gaps
        if value < price - (high - low) / gaps * 0.15:
            canvas.svg.polygon(
                [(buy_x, gy - 11), (buy_x - 9, gy + 7), (buy_x + 9, gy + 7)],
                fill=t.blue,
            )
            buy_at = (buy_x, gy)
            if i in fills:
                canvas.svg.circle(buy_x, gy, 16, fill="none", stroke=t.ink, sw=2)
        elif value > price + (high - low) / gaps * 0.15:
            canvas.svg.polygon(
                [(sell_x, gy + 11), (sell_x - 9, gy - 7), (sell_x + 9, gy - 7)],
                fill=t.sell,
            )
            sell_at = (sell_x, gy)
            if i in fills:
                canvas.svg.circle(sell_x, gy, 16, fill="none", stroke=t.ink, sw=2)
    names = labels_or(params, ["BUY", "SELL", "PRICE"])
    if "PRICE" not in names and len(names) < 5:
        names.append("PRICE")
    if buy_at and not fills:
        canvas.svg.circle(buy_at[0], buy_at[1], 16, fill="none", stroke=t.ink, sw=2)
    if buy_at:
        canvas.leader(buy_at[0] - 28, buy_at[1], buy_at[0] - 12, buy_at[1])
        canvas.chip(names[0], buy_at[0] - 36, buy_at[1], anchor="end")
    else:
        canvas.chip(names[0], x + 90, y + h * 0.7)
    if sell_at and len(names) > 1:
        canvas.leader(sell_at[0] + 16, sell_at[1], sell_at[0] + 28, sell_at[1])
        canvas.chip(names[1], sell_at[0] + 36, sell_at[1], anchor="start")
    elif len(names) > 1:
        canvas.chip(names[1], right - 40, y + 80)
    if len(names) > 2:
        canvas.chip(names[2], right - 10, price_y - 28, anchor="end")
    # Plain figures on the axis, inside the card. The stamp says they are an example.
    low_label = str(int(low)) if low == int(low) else f"{low:g}"
    high_label = str(int(high)) if high == int(high) else f"{high:g}"
    canvas.text(low_label, x + 28, ys[0] + 6, t.min_font, t.muted, weight="semi", role="price", bg=t.card)
    canvas.text(high_label, x + 28, ys[-1] + 6, t.min_font, t.muted, weight="semi", role="price", bg=t.card)
    canvas.watermark(x + w / 2, y + h / 2)
    canvas.stamp_example()
