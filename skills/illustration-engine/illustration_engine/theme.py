"""Style presets.

Sizes are authored at 1280×720 and scaled by canvas width / 1280.
House is the Blueprint still: 1536×1024. The same geometry also fits
1280×720 and 1920×1080.

`elite` uses the same geometry with a teal accent. It is provisional
until Stewart confirms it.
"""

from __future__ import annotations

from dataclasses import dataclass

BASE_W = 1280
CANVAS_SIZES = ((1536, 1024), (1280, 720), (1920, 1080))
PRESET_NAMES = ("house", "light", "contrast", "thumbnail", "elite")


@dataclass(frozen=True)
class Theme:
    name: str
    width: int
    height: int
    scale: float
    bg0: str
    bg_mid: str
    bg1: str
    ink: str
    muted: str
    accent: str
    accent_ink: str
    blue: str
    sell: str
    card: str
    card_line: str
    halo: str
    rim: str
    grid: str
    danger: str
    danger_ink: str
    chip: str
    chip_ink: str
    mascot: str
    mascot_shade: str
    visor: str
    eye: str
    headline: int
    label: int
    min_font: int
    headline_floor: int
    safe_top: int
    safe_bottom: int
    safe_x: int
    grid_pitch: int
    grid_alpha: float
    bokeh: bool
    vignette: str
    stroke: float
    arrow: float
    provisional: bool

    def s(self, px: float) -> float:
        """Scale a 1280-wide pixel value to this canvas."""
        return px * self.scale

    def glow_std(self) -> float:
        """Tight rim light. About 4 at 1536. A 10px blur read as a milky halo."""
        return 4 * self.width / 1536

    def wash_px(self) -> float:
        """Soft edge. About 6 at 1536, not a 32px flood."""
        return 6 * self.width / 1536


def _s(scale: float, px: float) -> int:
    return max(1, int(round(px * scale)))


def _theme(name: str, width: int, height: int, **colors) -> Theme:
    scale = width / BASE_W
    provisional = bool(colors.pop("provisional", False))
    return Theme(
        name=name,
        width=width,
        height=height,
        scale=scale,
        # 74px at 1280 is 89px at 1536. Roboto Condensed cap-height is 0.71em,
        # so that size paints a 63px cap, inside the 62-64px target.
        headline=_s(scale, 74),
        label=_s(scale, 34 * BASE_W / 1536),
        min_font=_s(scale, 24),
        headline_floor=_s(scale, 58),
        safe_top=_s(scale, 56),
        safe_bottom=_s(scale, 56),
        safe_x=_s(scale, 48),
        grid_pitch=_s(scale, 43),
        stroke=max(1.5, 2.0 * scale),
        arrow=max(2.0, 3.0 * scale),
        provisional=provisional,
        **colors,
    )


def _house_colors(**overrides) -> dict:
    colors = dict(
        bg0="#00081B",
        bg_mid="#000F2A",
        bg1="#000B21",
        ink="#F4F8FC",
        muted="#9AA8BC",
        accent="#00D4FF",
        accent_ink="#00D4FF",
        blue="#1E7BFF",
        sell="#4FD1A5",
        card="#060E1E",
        card_line="#3CC6FF",
        halo="#33E0FF",
        rim="#3CC6FF",
        grid="#0A1A38",
        danger="#FFB020",
        danger_ink="#FFB020",
        chip="#060E1E",
        chip_ink="#F4F8FC",
        mascot="#E8EEF7",
        mascot_shade="#B8C4D4",
        visor="#03080F",
        eye="#1EA8FF",
        grid_alpha=0.55,
        bokeh=True,
        vignette="#00040F",
    )
    colors.update(overrides)
    return colors


_PALETTES = {
    "house": ((1536, 1024), _house_colors()),
    "light": ((1536, 1024), _house_colors(
        bg0="#F4F7FB",
        bg_mid="#E7EEF6",
        bg1="#F7F9FC",
        ink="#0A1628",
        muted="#3E5168",
        accent="#0F6E8C",
        accent_ink="#083344",
        blue="#1E3A8A",
        sell="#0F766E",
        card="#FFFFFF",
        card_line="#0F6E8C",
        halo="#0F6E8C",
        rim="#083344",
        grid="#C5D4E4",
        danger="#9A3412",
        danger_ink="#9A3412",
        chip="#FFFFFF",
        chip_ink="#0A1628",
        mascot="#F8FAFC",
        mascot_shade="#94A3B8",
        visor="#0A1628",
        eye="#0F6E8C",
        grid_alpha=0.85,
        bokeh=False,
        vignette="#D5E0EC",
    )),
    "contrast": ((1536, 1024), _house_colors(
        bg0="#000000",
        bg_mid="#000000",
        bg1="#000000",
        ink="#FFFFFF",
        muted="#FFFFFF",
        accent="#FFE14A",
        accent_ink="#FFE14A",
        blue="#FFFFFF",
        sell="#B6FF4A",
        card="#000000",
        card_line="#FFE14A",
        halo="#FFE14A",
        rim="#FFE14A",
        grid="#3A3A3A",
        danger="#FFD000",
        danger_ink="#FFD000",
        chip="#000000",
        chip_ink="#FFFFFF",
        mascot="#FFFFFF",
        mascot_shade="#FFE14A",
        visor="#000000",
        eye="#FFE14A",
        grid_alpha=0.9,
        bokeh=False,
        vignette="#000000",
    )),
    "thumbnail": ((1080, 1080), _house_colors()),
    "elite": ((1536, 1024), _house_colors(
        bg0="#05080F",
        bg_mid="#08131F",
        bg1="#0B1424",
        accent="#14E0C8",
        accent_ink="#14E0C8",
        blue="#0FB5A5",
        card_line="#5DFFE8",
        halo="#5DFFE8",
        rim="#2EE6CF",
        grid="#0C2422",
        eye="#14E0C8",
        vignette="#02060C",
        provisional=True,
    )),
}


def get_theme(name: str | None = None, size: tuple[int, int] | None = None) -> Theme:
    key = name or _default
    if key not in _PALETTES:
        raise KeyError(f"unknown preset {key!r}; choose from {', '.join(PRESET_NAMES)}")
    default_size, colors = _PALETTES[key]
    width, height = (int(size[0]), int(size[1])) if size else default_size
    return _theme(key, width, height, **colors)


_default = "house"


def set_default(name: str) -> None:
    global _default
    if name not in _PALETTES:
        raise KeyError(name)
    _default = name


def get_default() -> str:
    return _default
