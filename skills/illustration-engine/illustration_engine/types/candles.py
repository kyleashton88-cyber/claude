"""Candle anatomy, a sideways series, and one pattern at a time."""

from __future__ import annotations

import random

from .common import labels_or, take_headline


def _candle(canvas, x, y_high, y_low, y_open, y_close, width):
    t = canvas.theme
    up = y_close <= y_open
    color = t.accent if up else t.blue
    canvas.glow_line(x, y_high, x, y_low, color, sw=max(3, width * 0.18))
    top = min(y_open, y_close)
    height = max(8, abs(y_close - y_open))
    canvas.glow_rect(x - width / 2, top, width, height, color, rx=4)


def _series(n: int, seed: int, start: float = 100.0) -> list[tuple[float, float, float, float]]:
    rng = random.Random(seed)
    price = start
    rows = []
    for _ in range(n):
        drift = (start - price) * 0.35
        move = drift + rng.uniform(-1.4, 1.4)
        opened = price
        closed = price + move
        wick = rng.uniform(0.3, 1.3)
        high = max(opened, closed) + wick
        low = min(opened, closed) - wick * rng.uniform(0.6, 1.0)
        rows.append((opened, high, low, closed))
        price = closed
    return rows


def _map(rows, top, bottom):
    highs = [row[1] for row in rows]
    lows = [row[2] for row in rows]
    lo, hi = min(lows), max(highs)
    pad = (hi - lo) * 0.08 or 1

    def y_of(value):
        return bottom - (value - (lo - pad)) / ((hi + pad) - (lo - pad)) * (bottom - top)

    return y_of


def draw_anatomy(canvas, params: dict) -> None:
    variant = params.get("variant", "bull")
    take_headline(canvas, params, "CANDLE PARTS")
    x, y, w, h = canvas.content_rect()
    canvas.glass(x, y, w, h)
    cx = x + w * 0.48
    top, bottom = y + 48, y + h - 48
    if variant == "bear":
        high, low, opened, closed = 80, 20, 70, 32
    elif variant == "wick":
        high, low, opened, closed = 90, 10, 58, 52
    else:
        high, low, opened, closed = 86, 18, 30, 74
    y_of = _map([(opened, high, low, closed)], top, bottom)
    _candle(canvas, cx, y_of(high), y_of(low), y_of(opened), y_of(closed), 54)
    names = labels_or(params, ["HIGH", "LOW", "BODY", "WICK"])
    canvas.leader(x + 120, y + 90, cx, y_of(high))
    canvas.chip(names[0], x + 120, y + 90)
    canvas.leader(x + 120, y + h - 90, cx, y_of(low))
    canvas.chip(names[1], x + 120, y + h - 90)
    body_mid = (y_of(opened) + y_of(closed)) / 2
    canvas.leader(x + w - 130, body_mid, cx + 30, body_mid)
    canvas.chip(names[2], x + w - 130, body_mid)
    if len(names) > 3:
        canvas.chip(names[3], x + w - 150, y + 110)
        canvas.leader(x + w - 150, y + 110, cx, (y_of(high) + min(y_of(opened), y_of(closed))) / 2)
    canvas.watermark(cx, (top + bottom) / 2)
    canvas.stamp_example()


def draw_series(canvas, params: dict) -> None:
    take_headline(canvas, params, "SIDEWAYS CANDLES")
    x, y, w, h = canvas.content_rect()
    canvas.glass(x, y, w, h)
    n = int(params.get("count") or 16)
    n = max(8, min(24, n))
    seed = int(params.get("seed") or 1)
    rows = _series(n, seed)
    left, right = x + 48, x + w - 48
    top, bottom = y + 56, y + h - 56
    y_of = _map(rows, top, bottom)
    slot = (right - left) / n
    body = min(28, slot * 0.55)
    for i, (opened, high, low, closed) in enumerate(rows):
        cx = left + slot * (i + 0.5)
        _candle(canvas, cx, y_of(high), y_of(low), y_of(opened), y_of(closed), body)
    names = labels_or(params, ["UP", "DOWN", "WICK"])
    canvas.chip(names[0], x + 120, y + 36)
    canvas.chip(names[1], x + w / 2, y + 36)
    if len(names) > 2:
        canvas.chip(names[2], x + w - 140, y + 36)
    canvas.watermark(x + w / 2, y + h / 2)
    canvas.stamp_example()


def draw_pattern(canvas, params: dict) -> None:
    variant = params.get("variant", "hammer")
    titles = {"hammer": "HAMMER", "doji": "DOJI", "engulfing": "ENGULFING"}
    take_headline(canvas, params, titles.get(variant, "PATTERN"))
    x, y, w, h = canvas.content_rect()
    canvas.glass(x, y, w, h)
    top, bottom = y + 70, y + h - 56
    mid = (top + bottom) / 2
    if variant == "doji":
        rows = [(50, 80, 20, 51)]
        names = labels_or(params, ["DOJI", "OPEN", "CLOSE"])
    elif variant == "engulfing":
        rows = [(60, 70, 40, 45), (48, 78, 36, 74)]
        names = labels_or(params, ["ENGULF", "FIRST", "SECOND"])
    else:
        rows = [(70, 78, 18, 74)]
        names = labels_or(params, ["HAMMER", "WICK", "BODY"])
    y_of = _map(rows, top, bottom)
    slot = (w * 0.5) / max(1, len(rows))
    origin = x + w * 0.42
    for i, (opened, high, low, closed) in enumerate(rows):
        cx = origin + slot * i
        _candle(canvas, cx, y_of(high), y_of(low), y_of(opened), y_of(closed), 48 if len(rows) == 1 else 36)
    canvas.chip(names[0], x + 140, mid - 40)
    if len(names) > 1:
        canvas.chip(names[1], x + 140, mid + 50)
    if len(names) > 2:
        canvas.chip(names[2], x + w - 160, mid)
    canvas.watermark(x + w / 2, mid)
    canvas.stamp_example()
