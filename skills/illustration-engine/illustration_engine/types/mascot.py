"""Place an approved character sheet. Never invent one.

The generated robot (stacked rectangles, a visor pill, stick arms) is withdrawn.
A pose PNG in assets/character/poses/ is placed in a locked box. If that file
is missing, the plate is the diagram alone and the SVG says the character
was withheld.
"""

from __future__ import annotations

import base64
from pathlib import Path

from .common import labels_or, take_headline

POSES = {
    "pointing": "point",
    "point": "point",
    "thinking": "think",
    "think": "think",
    "warning": "warn",
    "warn": "warn",
    "explain": "explain",
    "thumbs": "thumbs",
    "thumbs-up": "thumbs",
}

POSE_DIR = Path(__file__).resolve().parent.parent / "assets" / "character" / "poses"


def pose_file(pose: str) -> Path | None:
    key = POSES.get(pose, "")
    if not key:
        return None
    candidate = POSE_DIR / f"{key}.png"
    if candidate.is_file() and candidate.stat().st_size > 64:
        return candidate
    return None


def place_character(canvas, pose: str, x: float, y: float, height: float) -> bool:
    """Place the approved pose. Returns False when no sheet has been supplied."""
    path = pose_file(pose)
    if path is None:
        canvas.character = "withheld"
        canvas.svg.comment("character: withheld; no approved sheet")
        return False
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    # Width follows the file. Height is the locked token.
    try:
        from PIL import Image

        with Image.open(path) as image:
            aspect = image.width / max(image.height, 1)
    except OSError:
        aspect = 0.62
    width = height * aspect
    canvas.svg.image_data(encoded, "image/png", x, y, width, height)
    canvas.character = f"placed:{POSES.get(pose, pose)}"
    canvas.svg.comment(f"character: {canvas.character}")
    return True


def _diagram(canvas, x, y, w, h, pose: str) -> None:
    t = canvas.theme
    top = y + h * 0.34
    bot = y + h * 0.68
    canvas.glow_line(x + t.s(28), top, x + w - t.s(28), top, t.accent, sw=t.s(2), dash="7 7")
    canvas.glow_line(x + t.s(28), bot, x + w - t.s(28), bot, t.accent, sw=t.s(2), dash="7 7")
    canvas.glow_polyline(
        [
            (x + t.s(48), (top + bot) / 2),
            (x + w * 0.28, top + t.s(16)),
            (x + w * 0.48, bot - t.s(14)),
            (x + w - t.s(48), (top + bot) / 2),
        ],
        t.accent,
        sw=t.s(2.6),
    )
    if pose == "warning":
        canvas.glow_line(x + t.s(36), bot + t.s(36), x + w - t.s(36), bot + t.s(36), t.danger, sw=t.s(2.4))


def draw_mascot_scene(canvas, params: dict) -> None:
    pose = str(params.get("pose") or params.get("variant") or "pointing")
    if pose == "celebrating":
        pose = "pointing"
    if pose not in {"pointing", "thinking", "warning", "explain", "thumbs", "thumbs-up"}:
        pose = "pointing"
    titles = {
        "pointing": "LOOK HERE",
        "thinking": "THINK FIRST",
        "warning": "CHECK FIRST",
        "explain": "ONE IDEA",
        "thumbs": "STEP DONE",
        "thumbs-up": "STEP DONE",
    }
    take_headline(canvas, params, titles.get(pose, "LOOK HERE"))
    defaults = {
        "pointing": ["POINT", "RANGE"],
        "thinking": ["THINK", "CHECK"],
        "warning": ["WAIT", "CHECK"],
        "explain": ["IDEA", "NEXT"],
        "thumbs": ["DONE", "NEXT"],
        "thumbs-up": ["DONE", "NEXT"],
    }
    names = labels_or(params, defaults.get(pose, ["POINT", "RANGE"]))
    x, y, w, h = canvas.content_rect()
    t = canvas.theme
    height = t.s(433)
    placed = place_character(canvas, pose, x, y + h - height, height)
    diagram_x = x + (height * 0.7 if placed else 0)
    diagram_w = w - (height * 0.7 if placed else 0)
    _diagram(canvas, diagram_x, y, diagram_w, h, pose)
    canvas.chip(names[0], diagram_x + diagram_w * 0.28, y + t.s(36))
    if len(names) > 1:
        canvas.chip(names[1], diagram_x + diagram_w * 0.72, y + h - t.s(28))
    if pose == "warning":
        canvas.stamp_example()
