"""Repo-bundled fonts, then the usual system paths.

Inter is SIL Open Font License. Roboto Condensed is SIL Open Font License
(the files and OFL.txt are from the Google Fonts `ofl/robotocondensed` tree).
Callers should use `font_file` so a machine without the macOS font pack still renders.
"""

from __future__ import annotations

from pathlib import Path

LIB_DIR = Path(__file__).resolve().parent
VP_ROOT = LIB_DIR.parent
FONT_ROOT = VP_ROOT / "fonts"

# Bundled first, then the paths this repo used to hardcode.
CANDIDATES = {
    ("Inter", "Regular"): [
        FONT_ROOT / "inter" / "Inter-Regular.ttf",
        Path("/usr/share/fonts/truetype/macos/Inter-Regular.ttf"),
        Path("/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"),
        Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
    ],
    ("Inter", "Medium"): [
        FONT_ROOT / "inter" / "Inter-Medium.ttf",
        Path("/usr/share/fonts/truetype/macos/Inter-Medium.ttf"),
        Path("/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"),
        Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
    ],
    ("Inter", "Bold"): [
        FONT_ROOT / "inter" / "Inter-Bold.ttf",
        Path("/usr/share/fonts/truetype/macos/Inter-Bold.ttf"),
        Path("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"),
        Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"),
    ],
    ("Roboto Condensed", "Regular"): [
        FONT_ROOT / "roboto-condensed" / "RobotoCondensed-Regular.ttf",
        Path("/usr/share/fonts/truetype/roboto/unhinted/RobotoCondensed-Regular.ttf"),
    ],
    ("Roboto Condensed", "Bold"): [
        FONT_ROOT / "roboto-condensed" / "RobotoCondensed-Bold.ttf",
        Path("/usr/share/fonts/truetype/roboto/unhinted/RobotoCondensed-Bold.ttf"),
    ],
    ("JetBrains Mono", "Regular"): [
        Path("/usr/share/fonts/truetype/macos/JetBrainsMono-Regular.ttf"),
        Path("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"),
    ],
}


def font_file(family: str, weight: str = "Regular") -> Path:
    """Resolve a face. Bundled files win over `/usr/share/fonts/...`."""
    key = (family, weight)
    if key not in CANDIDATES:
        raise KeyError(f"no font candidates for {family} {weight}")
    for path in CANDIDATES[key]:
        if path.is_file():
            return path
    raise FileNotFoundError(f"{family} {weight} is not bundled and not on this machine")
