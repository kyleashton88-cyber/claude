"""Bundled fonts, loaded by name for Cairo and by file for resvg.

CairoSVG asks fontconfig for the family on each text node and ignores
@font-face file URLs. A private fontconfig file points only at this
folder, so "Roboto Condensed" and "Inter" resolve to the files shipped
here. resvg, when it is present, is given the same folder and told to
skip system fonts.

Inter is SIL Open Font License (OFL.txt). Roboto Condensed Bold is
Apache 2.0 (LICENSE-Roboto.txt).
"""

from __future__ import annotations

import os
import subprocess
from functools import lru_cache
from pathlib import Path
from urllib.request import pathname2url

from PIL import ImageFont

FONT_DIR = Path(__file__).resolve().parent / "assets" / "fonts"
CONF_PATH = Path("/tmp/illustration-engine-fonts.conf")
CACHE_DIR = Path("/tmp/illustration-engine-fontconfig")

FILES = {
    "regular": "Inter-Regular.ttf",
    "semi": "Inter-SemiBold.ttf",
    "bold": "Inter-Bold.ttf",
    "condensed": "RobotoCondensed-Bold.ttf",
}

# Real family names from the font files. Cairo matches these.
FAMILIES = {
    "regular": "Inter",
    "semi": "Inter",
    "bold": "Inter",
    "condensed": "Roboto Condensed",
}

HEADLINE_FAMILY = FAMILIES["condensed"]
LABEL_FAMILY = FAMILIES["bold"]


def font_path(weight: str) -> Path:
    path = FONT_DIR / FILES[weight]
    if not path.is_file():
        raise FileNotFoundError(f"missing bundled font: {path.name}")
    return path


def family(weight: str) -> str:
    return FAMILIES[weight]


def css_weight(weight: str) -> str:
    """Numeric weight. 700 is the bundled Bold file. 400 is Regular."""
    if weight in {"bold", "condensed"}:
        return "700"
    if weight == "semi":
        return "600"
    return "400"


def file_uri(path: Path) -> str:
    return "file://" + pathname2url(str(path.resolve()))


def install() -> Path:
    """Point fontconfig at the bundled files and nothing else."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    conf = (
        '<?xml version="1.0"?>\n'
        '<!DOCTYPE fontconfig SYSTEM "fonts.dtd">\n'
        "<fontconfig>\n"
        f"  <dir>{FONT_DIR}</dir>\n"
        f"  <cachedir>{CACHE_DIR}</cachedir>\n"
        "</fontconfig>\n"
    )
    CONF_PATH.write_text(conf, encoding="utf-8")
    os.environ["FONTCONFIG_FILE"] = str(CONF_PATH)
    return CONF_PATH


def css_for(svg_path: Path) -> str:
    """@font-face rules with absolute file URLs for resvg and other readers."""
    del svg_path
    rules = []
    for weight, filename in FILES.items():
        target = FONT_DIR / filename
        rules.append(
            "@font-face {"
            f' font-family: "{FAMILIES[weight]}";'
            f' src: url("{file_uri(target)}") format("truetype");'
            f" font-weight: {css_weight(weight)}; font-style: normal; }}"
        )
    return "\n".join(rules)


def bundled_match() -> tuple[bool, str]:
    """Fail unless fontconfig resolves the two faces to the bundled files."""
    install()
    checks = (
        ("Roboto Condensed:weight=bold", font_path("condensed")),
        ("Inter:weight=bold", font_path("bold")),
    )
    lines = []
    ok = True
    for pattern, expected in checks:
        found = subprocess.run(
            ["fc-match", "-f", "%{file}", pattern],
            check=False,
            capture_output=True,
            text=True,
            env=os.environ.copy(),
        ).stdout.strip()
        match = Path(found).resolve() == expected.resolve() if found else False
        ok = ok and match
        lines.append(f"{pattern} -> {found or 'none'}")
    return ok, "; ".join(lines)


def advance(weight: str, text: str, size: int) -> float:
    """Advance width of the bundled file. There is no width multiplier."""
    return float(pil_font(weight, int(size)).getlength(text))


@lru_cache(maxsize=64)
def pil_font(weight: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(font_path(weight)), size)


install()
