"""House frame size and palette, aligned with the lesson pictures.

Frames are drawn at final size. Nothing in these skills upscales a raster.
"""

from __future__ import annotations

from pathlib import Path

from lib.fonts import font_file

W, H = 1920, 1080
FPS = 30

INK = (11, 31, 51)
NAVY = (18, 53, 91)
BRAND = (31, 78, 121)
BLUE = (42, 120, 214)
BLUE_LT = (57, 135, 229)
ORANGE = (235, 104, 52)
AQUA = (27, 175, 122)
AQUA_LT = (46, 230, 166)
YELLOW = (237, 161, 0)
WHITE = (255, 255, 255)
TEXT = (244, 247, 250)
MUTED = (168, 188, 204)
LINE = (36, 72, 108)
RED = (226, 86, 78)
SKIN = (232, 190, 158)

DISCLAIMER = "Educational content only  ·  Not financial advice  ·  Figures are illustrative"

VP_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = VP_ROOT.parents[1]


def font_path(weight: str) -> str:
    family = {
        "bold": ("Inter", "Bold"),
        "regular": ("Inter", "Regular"),
        "medium": ("Inter", "Medium"),
        "mono": ("JetBrains Mono", "Regular"),
    }[weight]
    return str(font_file(*family))
