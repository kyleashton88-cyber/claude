"""Small easing helpers. All curves clamp to 0..1."""

from __future__ import annotations


def clamp(t: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return lo if t < lo else hi if t > hi else t


def lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t


def smoothstep(t: float) -> float:
    t = clamp(t)
    return t * t * (3.0 - 2.0 * t)


def ease_out(t: float) -> float:
    t = clamp(t)
    return 1.0 - (1.0 - t) ** 3


def ease_in_out(t: float) -> float:
    t = clamp(t)
    return 2 * t * t if t < 0.5 else 1 - ((-2 * t + 2) ** 2) / 2


def interval(t: float, start: float, length: float) -> float:
    """Progress of a local animation that begins at `start` seconds."""
    if length <= 0:
        return 1.0
    return clamp((t - start) / length)
