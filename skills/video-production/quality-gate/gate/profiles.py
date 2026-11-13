"""Length and frame rules per format.

The old 15-minute floor rejected the approved Blueprint lesson BP-01 (6:15).
Length now comes from the profile for the format.
"""

from __future__ import annotations

from dataclasses import dataclass, replace


@dataclass(frozen=True)
class Profile:
    name: str
    label: str
    min_seconds: float
    max_seconds: float
    width: int
    height: int
    fps: float = 30.0
    max_hold_seconds: float = 8.0
    max_black_seconds: float = 0.5
    max_silence_seconds: float = 2.0
    max_caption_cps: float = 20.0
    max_caption_line: int = 42
    max_caption_lines: int = 2
    margin_frac: float = 0.04
    video_codec: str = "h264"
    audio_codec: str = "aac"


PROFILES: dict[str, Profile] = {
    "blueprint": Profile(
        "blueprint",
        "Blueprint lesson",
        min_seconds=4 * 60,
        max_seconds=10 * 60,
        width=1920,
        height=1080,
    ),
    "elite": Profile(
        "elite",
        "Elite lesson",
        min_seconds=8 * 60,
        max_seconds=20 * 60,
        width=1920,
        height=1080,
    ),
    "market-check": Profile(
        "market-check",
        "Market Check",
        min_seconds=2 * 60,
        max_seconds=8 * 60,
        width=1920,
        height=1080,
    ),
    "explainer": Profile(
        "explainer",
        "Explainer",
        min_seconds=3 * 60,
        max_seconds=8 * 60,
        width=1920,
        height=1080,
    ),
    "interview": Profile(
        "interview",
        "Interview",
        min_seconds=8 * 60,
        max_seconds=25 * 60,
        width=1920,
        height=1080,
        max_hold_seconds=12.0,
    ),
    "short": Profile(
        "short",
        "Short",
        min_seconds=5.0,
        max_seconds=59.999,
        width=1080,
        height=1920,
        max_hold_seconds=5.0,
    ),
}

ALIASES = {
    "blueprint-lesson": "blueprint",
    "elite-lesson": "elite",
    "market_check": "market-check",
    "marketcheck": "market-check",
    "shorts": "short",
    "reel": "short",
    "reels": "short",
}


def get_profile(name: str, **overrides) -> Profile:
    key = ALIASES.get(name.strip().lower(), name.strip().lower())
    if key not in PROFILES:
        known = ", ".join(sorted(PROFILES))
        raise KeyError(f"unknown format {name!r}. Known formats: {known}")
    profile = PROFILES[key]
    if overrides:
        profile = replace(profile, **overrides)
    return profile


def length_ok(duration: float, profile: Profile) -> bool:
    return profile.min_seconds <= duration <= profile.max_seconds


# YouTube integrated-loudness target. The older music bed still aims at -16.
LOUDNESS_TARGET = -14.0
LOUDNESS_TOLERANCE = 1.0
TRUE_PEAK_MAX = -1.0
