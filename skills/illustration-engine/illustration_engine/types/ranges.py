"""Support, resistance, and a sideways path. One picture, one idea."""

from __future__ import annotations

from .common import labels_or, take_headline


def _path(canvas, left, right, upper, lower, kind: str) -> list[tuple[float, float]]:
    mid = (upper + lower) / 2
    span = (lower - upper) * 0.28
    points = []
    steps = 18
    for i in range(steps):
        t = i / (steps - 1)
        x = left + (right - left) * t
        wave = span if i % 2 == 0 else -span
        y = mid + wave * (0.35 + 0.65 * (0.5 - abs(t - 0.5)))
        if kind == "touch" and i == 11:
            y = lower - 4
        if kind == "leave" and t > 0.72:
            y = upper - (t - 0.72) * (lower - upper) * 1.6
        points.append((x, y))
    return points


def draw_range(canvas, params: dict) -> None:
    variant = params.get("variant", "inside")
    default = "THE RANGE"
    if variant == "leave" or params.get("stop"):
        default = "THE STOP" if params.get("stop") and variant != "leave" else "LEAVES THE BAND"
    take_headline(canvas, params, params.get("headline") or default)
    x, y, w, h = canvas.content_rect()
    canvas.glass(x, y, w, h)
    left, right = x + 70, x + w - 70
    upper = y + 78
    lower = y + h - 78
    t = canvas.theme
    if params.get("stop") or variant == "stop":
        stop_y = lower + 28
        if stop_y > y + h - 24:
            stop_y = lower
            lower -= 36
        canvas.glow_line(left, stop_y, right, stop_y, t.danger, sw=t.s(2.6), dash="9 7")
    canvas.glow_line(left, upper, right, upper, t.accent, sw=t.s(2.2), dash="6 6")
    canvas.glow_line(left, lower, right, lower, t.accent, sw=t.s(2.2), dash="6 6")
    kind = "leave" if variant == "leave" else ("touch" if variant == "touch" else "inside")
    pts = _path(canvas, left + 10, right - 10, upper, lower, kind)
    canvas.glow_polyline(pts, t.accent, sw=t.s(3))
    names = labels_or(params, ["UPPER", "LOWER", "RANGE"] if not params.get("stop") else ["UPPER", "LOWER", "STOP"])
    canvas.chip(names[0], right - 20, upper - 28, anchor="end")
    if len(names) > 1:
        canvas.chip(names[1], left + 20, lower + 32, anchor="start")
    if len(names) > 2:
        canvas.chip(names[2], left + w * 0.08, (upper + lower) / 2)
    canvas.watermark(x + w / 2, (upper + lower) / 2)
    canvas.stamp_example()
