"""Beginner diagrams: flow, comparison, steps, and the three analogies."""

from __future__ import annotations

from .common import labels_or, take_headline


def _node(canvas, cx, cy, text, w=250, h=110) -> None:
    t = canvas.theme
    canvas.svg.rect(cx - w / 2, cy - h / 2, w, h, fill=t.card, stroke=t.card_line, sw=t.stroke, rx=22, opacity=0.94)
    canvas.text(text, cx, cy + t.label * 0.25, t.label, t.chip_ink, weight="bold", anchor="middle", role="label", bg=t.card)


def draw_flowchart(canvas, params: dict) -> None:
    take_headline(canvas, params, "THE PATH")
    names = labels_or(params, ["RANGE", "LEVELS", "STOP"])
    x, y, w, h = canvas.content_rect()
    cy = y + h * 0.48
    gap = w / (len(names) + 0.4)
    centers = [x + gap * (i + 0.7) for i in range(len(names))]
    for i, name in enumerate(names):
        if i:
            canvas.arrow(centers[i - 1] + 130, cy, centers[i] - 140, cy)
        _node(canvas, centers[i], cy, name)
    if params.get("example"):
        canvas.stamp_example()


def draw_comparison(canvas, params: dict) -> None:
    take_headline(canvas, params, params.get("headline") or "TWO WAYS")
    names = labels_or(params, ["CLEAR", "MISS"])
    x, y, w, h = canvas.content_rect()
    gap = 36
    box_w = (w - gap) / 2
    t = canvas.theme
    canvas.glass(x, y, box_w, h)
    with canvas.svg.group(opacity=0.45):
        canvas.glass(x + box_w + gap, y, box_w, h)
    canvas.text(names[0], x + box_w / 2, y + 70, t.headline - 20, t.accent_ink, weight="bold", anchor="middle", role="label", bg=t.card)
    if len(names) > 1:
        canvas.text(names[1], x + box_w + gap + box_w / 2, y + 70, t.headline - 20, t.muted, weight="bold", anchor="middle", role="label", bg=t.bg0)
    # Left: a clean band. Right: the same band with a slash, dimmed.
    def band(bx):
        top = y + h * 0.38
        bot = y + h * 0.72
        canvas.svg.line(bx + 40, top, bx + box_w - 40, top, t.accent, sw=2, dash="6 6")
        canvas.svg.line(bx + 40, bot, bx + box_w - 40, bot, t.accent, sw=2, dash="6 6")
        canvas.svg.polyline(
            [(bx + 50, (top + bot) / 2), (bx + box_w * 0.4, top + 20), (bx + box_w * 0.7, bot - 16), (bx + box_w - 50, (top + bot) / 2)],
            t.accent,
            sw=3,
        )

    band(x)
    with canvas.svg.group(opacity=0.55):
        band(x + box_w + gap)
        canvas.svg.line(x + box_w + gap + 50, y + h * 0.32, x + w - 50, y + h * 0.78, t.danger, sw=4)
    if params.get("variant") != "plain":
        canvas.stamp_example()
    if params.get("variant") == "plain":
        # No figures on this plate. The slash is the idea.
        canvas.example = False


def draw_steps(canvas, params: dict) -> None:
    take_headline(canvas, params, "THREE PARTS")
    names = labels_or(params, ["RANGE", "LEVELS", "STOP"])
    x, y, w, h = canvas.content_rect()
    t = canvas.theme
    cy = y + h * 0.55
    step_w = w / len(names)
    for i, name in enumerate(names):
        cx = x + step_w * (i + 0.5)
        if i:
            canvas.arrow(cx - step_w + 70, cy - 70, cx - 70, cy - 70)
        canvas.svg.circle(cx, cy - 70, 32, fill=t.card, stroke=t.accent, sw=t.stroke)
        canvas.text(str(i + 1), cx, cy - 70 + t.label * 0.28, t.label, t.accent_ink, weight="bold", anchor="middle", role="step", bg=t.card)
        canvas.text(name, cx, cy + 20, t.label, t.ink, weight="bold", anchor="middle", role="label", bg=t.bg0)


def draw_fence(canvas, params: dict) -> None:
    take_headline(canvas, params, "THE FENCE")
    names = labels_or(params, ["INSIDE", "FENCE", "PRACTICE"])
    x, y, w, h = canvas.content_rect()
    canvas.glass(x, y, w, h)
    left, right = x + 80, x + w - 80
    rail_top = y + 120
    rail_bot = y + h - 110
    t = canvas.theme
    posts = 6
    for i in range(posts):
        px = left + (right - left) * i / (posts - 1)
        canvas.svg.line(px, rail_top - 16, px, rail_bot + 16, t.accent, sw=4, opacity=0.85)
    canvas.svg.line(left, rail_top, right, rail_top, t.accent, sw=3)
    canvas.svg.line(left, rail_bot, right, rail_bot, t.accent, sw=3)
    mid = (rail_top + rail_bot) / 2
    canvas.svg.polyline(
        [
            (left + 30, mid),
            (left + w * 0.2, rail_top + 30),
            (left + w * 0.4, rail_bot - 30),
            (left + w * 0.62, mid - 10),
            (right - 40, mid + 16),
        ],
        t.ink,
        sw=3,
    )
    canvas.chip(names[0], (left + right) / 2, mid + 48)
    if len(names) > 1:
        canvas.chip(names[1], left + 40, rail_top - 36, anchor="start")
    if len(names) > 2:
        canvas.chip(names[2], right - 20, rail_bot + 40, anchor="end")
    canvas.stamp_example()


def draw_ladder(canvas, params: dict) -> None:
    take_headline(canvas, params, "THE LADDER")
    names = labels_or(params, ["RUNG", "LEVEL", "WAIT"])
    x, y, w, h = canvas.content_rect()
    canvas.glass(x, y, w, h)
    cx = x + w * 0.42
    top, bottom = y + 50, y + h - 50
    rail = 70
    t = canvas.theme
    canvas.glow_line(cx - rail, top, cx - rail, bottom, t.accent, sw=t.s(5))
    canvas.glow_line(cx + rail, top, cx + rail, bottom, t.accent, sw=t.s(5))
    rungs = 6
    highlight = int(params.get("highlight") or 3)
    highlight = max(0, min(rungs - 1, highlight))
    for i in range(rungs):
        gy = top + (bottom - top) * (i + 0.5) / rungs
        sw = t.s(5) if i == highlight else t.s(3.2)
        color = t.ink if i == highlight else t.accent
        canvas.glow_line(cx - rail, gy, cx + rail, gy, color, sw=sw)
        if i == highlight:
            canvas.leader(cx + rail + 10, gy, cx + 180, gy)
            canvas.chip(names[0], cx + 200, gy, anchor="start")
    if len(names) > 1:
        canvas.chip(names[1], x + 90, top + 10, anchor="start")
    if len(names) > 2:
        canvas.chip(names[2], x + w - 80, bottom - 10, anchor="end")
    canvas.stamp_example()


def _bucket(canvas, x, y, w, h, fill_to: float) -> None:
    t = canvas.theme
    rim = w * 0.08
    points = [(x + rim, y), (x + w - rim, y), (x + w, y + h), (x, y + h)]
    canvas.svg.polygon(points, fill=t.card, stroke=t.accent, sw=t.stroke, opacity=0.9)
    canvas.svg.ellipse(x + w / 2, y, w / 2 - rim, 14, fill="none", stroke=t.accent, sw=t.stroke)
    if fill_to > 0:
        inner_top = y + h * (1 - fill_to)
        canvas.svg.rect(x + 18, inner_top, w - 36, y + h - inner_top - 10, fill=t.accent, opacity=0.25, rx=6)


def draw_buckets(canvas, params: dict) -> None:
    take_headline(canvas, params, "TWO BUCKETS")
    names = labels_or(params, ["APART", "OVERLAP", "BUCKET"])
    variant = params.get("variant", "apart")
    x, y, w, h = canvas.content_rect()
    bw, bh = min(280, w * 0.28), h * 0.55
    yb = y + h * 0.22
    gap = w * 0.18
    left = x + w * 0.5 - gap / 2 - bw
    right = x + w * 0.5 + gap / 2
    if variant == "overlap":
        left = x + w * 0.5 - bw * 0.85
        right = x + w * 0.5 - bw * 0.15
    _bucket(canvas, left, yb, bw, bh, 0.55 if variant != "empty" else 0.15)
    _bucket(canvas, right, yb, bw, bh, 0.4 if variant != "empty" else 0.7)
    canvas.chip(names[0], left + bw / 2, yb + bh + 40)
    if len(names) > 1:
        canvas.chip(names[1], right + bw / 2, yb - 36)
    if len(names) > 2:
        canvas.chip(names[2], x + 80, y + 30, anchor="start")
    canvas.stamp_example()


def draw_checklist(canvas, params: dict) -> None:
    take_headline(canvas, params, "ON PAPER")
    names = labels_or(params, ["RANGE", "LEVELS", "STOP"])
    x, y, w, h = canvas.content_rect()
    canvas.glass(x + w * 0.18, y, w * 0.64, h)
    t = canvas.theme
    highlight = int(params.get("highlight") or 0)
    highlight = max(0, min(len(names) - 1, highlight))
    row_h = (h - 80) / len(names)
    for i, name in enumerate(names):
        cy = y + 50 + row_h * (i + 0.5)
        cx = x + w * 0.28
        color = t.accent if i == highlight else t.muted
        canvas.svg.circle(cx, cy, 16, fill="none", stroke=color, sw=2.5)
        if i == highlight:
            canvas.svg.polyline([(cx - 8, cy), (cx - 2, cy + 7), (cx + 9, cy - 8)], t.accent, sw=3)
        canvas.text(name, cx + 40, cy + t.label * 0.28, t.label, t.ink if i == highlight else t.muted, weight="bold", role="label", bg=t.card)
