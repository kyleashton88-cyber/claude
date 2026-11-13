"""Style presets. House matches the navy and cyan course stills."""

from __future__ import annotations

from dataclasses import dataclass, replace

PRESET_NAMES = ("house", "light", "contrast", "thumbnail")


@dataclass(frozen=True)
class Theme:
    name: str
    width: int
    height: int
    bg0: str
    bg1: str
    ink: str
    muted: str
    accent: str
    accent_ink: str
    blue: str
    card: str
    card_line: str
    grid: str
    danger: str
    danger_ink: str
    chip: str
    chip_ink: str
    mascot: str
    mascot_shade: str
    visor: str
    headline: int
    label: int
    min_font: int
    safe_top: int
    safe_bottom: int
    safe_x: int
    grid_alpha: float
    bokeh: bool
    stroke: float


def _house(**overrides) -> Theme:
    base = dict(
        name="house",
        width=1536,
        height=1024,
        bg0="#050A18",
        bg1="#0A1630",
        ink="#FFFFFF",
        muted="#8CA0C0",
        accent="#00D4FF",
        accent_ink="#00D4FF",
        blue="#1E5EFF",
        card="#0B1A30",
        card_line="#00D4FF",
        grid="#16345A",
        danger="#FFB020",
        danger_ink="#FFB020",
        chip="#0B1A30",
        chip_ink="#FFFFFF",
        mascot="#E8EEF5",
        mascot_shade="#8EA0B5",
        visor="#061018",
        headline=76,
        label=26,
        min_font=22,
        safe_top=80,
        safe_bottom=80,
        safe_x=72,
        grid_alpha=0.55,
        bokeh=True,
        stroke=2.0,
    )
    base.update(overrides)
    return Theme(**base)


PRESETS: dict[str, Theme] = {
    "house": _house(),
    "light": _house(
        name="light",
        bg0="#F7F9FC",
        bg1="#E6EEF6",
        ink="#0A1628",
        muted="#3E5168",
        accent="#0F6E8C",
        accent_ink="#083344",
        blue="#1E3A8A",
        card="#FFFFFF",
        card_line="#0F6E8C",
        grid="#C5D4E4",
        danger="#9A3412",
        danger_ink="#9A3412",
        chip="#FFFFFF",
        chip_ink="#0A1628",
        mascot="#F8FAFC",
        mascot_shade="#94A3B8",
        visor="#0A1628",
        grid_alpha=0.9,
        bokeh=False,
        stroke=2.25,
    ),
    "contrast": _house(
        name="contrast",
        bg0="#000000",
        bg1="#000000",
        ink="#FFFFFF",
        muted="#FFFFFF",
        accent="#FFE14A",
        accent_ink="#FFE14A",
        blue="#FFFFFF",
        card="#000000",
        card_line="#FFE14A",
        grid="#3A3A3A",
        danger="#FFD000",
        danger_ink="#FFD000",
        chip="#000000",
        chip_ink="#FFFFFF",
        mascot="#FFFFFF",
        mascot_shade="#FFE14A",
        visor="#000000",
        headline=80,
        label=30,
        min_font=26,
        safe_top=88,
        safe_bottom=88,
        grid_alpha=0.9,
        bokeh=False,
        stroke=3.25,
    ),
    "thumbnail": _house(
        name="thumbnail",
        width=1080,
        height=1080,
        headline=78,
        label=32,
        min_font=28,
        safe_top=72,
        safe_bottom=72,
        safe_x=64,
        grid_alpha=0.35,
        bokeh=True,
        stroke=2.5,
    ),
}

_default = "house"


def set_default(name: str) -> None:
    global _default
    if name not in PRESETS:
        raise KeyError(name)
    _default = name


def get_default() -> str:
    return _default


def get_theme(name: str | None = None, size: tuple[int, int] | None = None) -> Theme:
    key = name or _default
    if key not in PRESETS:
        raise KeyError(f"unknown preset {key!r}; choose from {', '.join(PRESET_NAMES)}")
    theme = PRESETS[key]
    if size:
        theme = replace(theme, width=int(size[0]), height=int(size[1]))
    return theme
