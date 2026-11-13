"""A vector grid-bot mascot drawn in code.

The face is one visor bar. There is no mouth, no smile, and no celebrating pose.
The chest mark is a geometric badge, not a wordmark.
"""

from __future__ import annotations

from .common import labels_or, take_headline


def _badge(canvas, cx, cy, s, accent) -> None:
    """A geometric G, drawn as a path so it is not a text label."""
    r = 11 * s
    d = (
        f"M {cx + r * 0.35:.1f} {cy - r * 0.75:.1f} "
        f"A {r:.1f} {r:.1f} 0 1 0 {cx + r * 0.45:.1f} {cy + r * 0.55:.1f} "
        f"L {cx - r * 0.15:.1f} {cy + r * 0.55:.1f} "
        f"L {cx - r * 0.15:.1f} {cy + r * 0.05:.1f} "
        f"L {cx + r * 0.7:.1f} {cy + r * 0.05:.1f}"
    )
    canvas.svg.path(d, fill="none", stroke=accent, sw=max(2, 3 * s))


def draw_mascot(canvas, x: float, y: float, scale: float, pose: str) -> None:
    """Draw the figure. (x, y) is the top-left of the unscaled 180 by 280 box."""
    t = canvas.theme
    s = scale
    with canvas.svg.group(transform=f"translate({x:.1f} {y:.1f}) scale({s})"):
        canvas.svg.ellipse(90, 268, 62, 10, fill=t.accent, opacity=0.16)
        canvas.svg.rect(62, 214, 22, 52, fill=t.mascot, stroke=t.mascot_shade, sw=2, rx=8)
        canvas.svg.rect(96, 214, 22, 52, fill=t.mascot_shade, stroke=t.mascot_shade, sw=2, rx=8)
        canvas.svg.rect(40, 112, 100, 112, fill=t.mascot, stroke=t.rim, sw=2.5, rx=32)
        canvas.svg.rect(92, 118, 44, 98, fill=t.mascot_shade, rx=18, opacity=0.55)
        canvas.svg.circle(90, 168, 22, fill=t.visor, stroke=t.eye, sw=2)
        _badge(canvas, 90, 168, 1, t.eye)
        canvas.svg.rect(28, 8, 124, 112, fill=t.mascot, stroke=t.rim, sw=3, rx=56)
        canvas.svg.path("M 46 36 A 58 52 0 0 1 132 22", fill="none", stroke="#F4F8FC", sw=3, opacity=0.7)
        canvas.svg.rect(50, 46, 80, 36, fill=t.visor, rx=14)
        # One visor bar. Not two dots, and not a smile.
        canvas.svg.rect(58, 60, 64, 7, fill=t.eye, rx=2)
        # Arms sit in front of the body. Local coordinates, before the group scale.
        if pose == "pointing":
            canvas.svg.line(40, 150, 16, 168, t.mascot_shade, sw=14)
            canvas.svg.line(140, 146, 210, 132, t.mascot, sw=14)
            canvas.svg.circle(214, 130, 8, fill=t.mascot, stroke=t.accent, sw=2)
        elif pose == "thinking":
            canvas.svg.line(140, 150, 168, 176, t.mascot_shade, sw=14)
            canvas.svg.line(40, 146, 28, 78, t.mascot, sw=14)
            canvas.svg.circle(26, 70, 8, fill=t.mascot, stroke=t.accent, sw=2)
        else:
            # warning: one arm up, holding a small triangle sign
            canvas.svg.line(40, 150, 12, 176, t.mascot_shade, sw=14)
            canvas.svg.line(140, 140, 168, 70, t.mascot, sw=14)
            canvas.svg.polygon([(196, 36), (176, 76), (216, 76)], fill=t.danger, stroke=t.ink, sw=2)


def draw_mascot_scene(canvas, params: dict) -> None:
    pose = str(params.get("pose") or params.get("variant") or "pointing")
    if pose == "celebrating":
        pose = "pointing"
    if pose not in {"pointing", "thinking", "warning"}:
        pose = "pointing"
    titles = {
        "pointing": "LOOK HERE",
        "thinking": "THINK FIRST",
        "warning": "CHECK FIRST",
    }
    take_headline(canvas, params, titles[pose])
    defaults = {
        "pointing": ["POINT", "RANGE"],
        "thinking": ["THINK", "CHECK"],
        "warning": ["WAIT", "CHECK"],
    }
    names = labels_or(params, defaults[pose])
    x, y, w, h = canvas.content_rect()
    canvas.glass(x, y, w, h)
    t = canvas.theme
    card_x = x + w * 0.40
    card_w = w * 0.56
    if pose == "pointing":
        top = y + h * 0.38
        bot = y + h * 0.68
        canvas.svg.line(card_x + 40, top, card_x + card_w - 40, top, t.accent, sw=2, dash="6 6")
        canvas.svg.line(card_x + 40, bot, card_x + card_w - 40, bot, t.accent, sw=2, dash="6 6")
        canvas.svg.polyline(
            [(card_x + 50, (top + bot) / 2), (card_x + 140, top + 16), (card_x + 230, bot - 12), (card_x + card_w - 50, (top + bot) / 2)],
            t.accent,
            sw=3,
        )
    elif pose == "thinking":
        for i in range(3):
            yy = y + 90 + i * 70
            canvas.svg.circle(card_x + 50, yy, 10, fill="none", stroke=t.accent, sw=2)
            canvas.svg.line(card_x + 80, yy, card_x + card_w - 50, yy, t.muted, sw=2)
    elif pose == "warning":
        canvas.svg.rect(card_x + 40, y + h * 0.42, card_w - 80, h * 0.28, fill=t.danger, opacity=0.2, rx=12)
        canvas.svg.line(card_x + 40, y + h * 0.42, card_x + card_w - 40, y + h * 0.42, t.danger, sw=3)
    else:
        canvas.svg.polyline(
            [(card_x + 70, y + h * 0.62), (card_x + 100, y + h * 0.48), (card_x + 140, y + h * 0.66)],
            t.accent,
            sw=6,
        )
    canvas.chip(names[0], card_x + card_w * 0.3, y + 70)
    if len(names) > 1:
        canvas.chip(names[1], card_x + card_w * 0.72, y + h - 50)
    scale = min((h * 0.88) / 280, (w * 0.38) / 180)
    draw_mascot(canvas, x + t.s(12), y + h - 280 * scale - t.s(8), scale, pose)
    if pose == "warning":
        canvas.stamp_example()
