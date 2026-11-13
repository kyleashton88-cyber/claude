"""Open-licensed fonts embedded in every SVG.

Inter is shipped under the SIL Open Font License. The license text is
OFL.txt beside the font files. Documents drawn with the fonts are not
themselves under that license.
"""

from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path

from PIL import ImageFont

FONT_DIR = Path(__file__).resolve().parent / "assets" / "fonts"

FILES = {
    "regular": "Inter-Regular.ttf",
    "semi": "Inter-SemiBold.ttf",
    "bold": "Inter-Bold.ttf",
}

FAMILIES = {
    "regular": "Engine Regular",
    "semi": "Engine Semi",
    "bold": "Engine Bold",
}


def font_path(weight: str) -> Path:
    path = FONT_DIR / FILES[weight]
    if not path.is_file():
        raise FileNotFoundError(f"missing font file: {path.name}")
    return path


def family(weight: str) -> str:
    return FAMILIES[weight]


def css_for(svg_path: Path) -> str:
    """Font faces as relative URLs so a saved SVG still finds the files."""
    rules = []
    for weight, filename in FILES.items():
        target = FONT_DIR / filename
        href = Path(os.path.relpath(target, svg_path.parent)).as_posix()
        rules.append(
            "@font-face {"
            f' font-family: "{FAMILIES[weight]}";'
            f' src: url("{href}") format("truetype");'
            " font-weight: 400; font-style: normal; }"
        )
    return "\n".join(rules)


@lru_cache(maxsize=64)
def pil_font(weight: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(font_path(weight)), size)
