"""Short original effects. No sampled libraries."""

from __future__ import annotations

import numpy as np

from music.compose import SR, _tone, hz, lowpass

EFFECTS = ("whoosh", "click", "riser", "tick", "mark-sting")


def whoosh() -> np.ndarray:
    n = int(1.25 * SR)
    rng = np.random.default_rng(11)
    noise = rng.normal(0.0, 1.0, n).astype(np.float32)
    y = np.empty(n, dtype=np.float32)
    acc = 0.0
    for i in range(n):
        u = i / n
        cutoff = 180.0 + 5200.0 * (u ** 1.35)
        a = float(np.exp(-2.0 * np.pi * cutoff / SR))
        acc = a * acc + (1.0 - a) * float(noise[i])
        y[i] = acc * np.sin(np.pi * u) ** 1.15
    stereo = np.column_stack([y, np.roll(y, int(0.008 * SR))])
    return _peak(stereo * 0.55)


def click() -> np.ndarray:
    n = int(0.09 * SR)
    t = np.arange(n, dtype=np.float32) / SR
    body = np.sin(2 * np.pi * 740 * t) * np.exp(-t / 0.018)
    tick = np.sin(2 * np.pi * 1860 * t) * np.exp(-t / 0.008)
    y = (0.35 * body + 0.2 * tick).astype(np.float32)
    return _peak(np.column_stack([y, y]))


def riser() -> np.ndarray:
    n = int(2.1 * SR)
    t = np.arange(n, dtype=np.float32) / SR
    freq = 160.0 * (2.0 ** (2.3 * t / t[-1]))
    phase = np.cumsum(2 * np.pi * freq / SR).astype(np.float32)
    tone = np.sin(phase)
    rng = np.random.default_rng(19)
    noise = lowpass(rng.normal(0, 1, n).astype(np.float32), 5000.0)
    u = t / t[-1]
    y = (0.45 * tone + 0.25 * noise) * (u ** 1.6)
    y = y.astype(np.float32)
    return _peak(np.column_stack([y, np.roll(y, 200)]))


def tick() -> np.ndarray:
    n = int(0.05 * SR)
    t = np.arange(n, dtype=np.float32) / SR
    y = (np.sin(2 * np.pi * 2450 * t) * np.exp(-t / 0.007)).astype(np.float32)
    return _peak(np.column_stack([y, y]) * 0.8)


def mark_sting() -> np.ndarray:
    """Four original notes. Not a quotation of an existing ident."""
    notes = [(60, 0.00), (64, 0.18), (67, 0.36), (72, 0.56)]
    total = int(2.6 * SR)
    buf = np.zeros(total, dtype=np.float32)
    for midi, at in notes:
        n = int(1.7 * SR)
        bell = _tone(hz(midi + 12), n, ((1, 0.55), (2.01, 0.22), (3.0, 0.10), (4.2, 0.04)))
        bell *= np.exp(-np.arange(n) / (0.42 * SR)).astype(np.float32)
        start = int(at * SR)
        end = min(total, start + n)
        buf[start:end] += bell[: end - start]
    buf = lowpass(buf, 4200.0)
    fade = np.linspace(1.0, 0.0, int(0.5 * SR), dtype=np.float32)
    buf[-len(fade) :] *= fade
    return _peak(np.column_stack([buf, np.roll(buf, 240)]) * 0.9)


def render_effect(name: str) -> tuple[np.ndarray, int]:
    table = {
        "whoosh": whoosh,
        "click": click,
        "riser": riser,
        "tick": tick,
        "mark-sting": mark_sting,
    }
    if name not in table:
        raise ValueError(f"unknown effect {name}. choices: {', '.join(table)}")
    return table[name](), SR


def _peak(audio: np.ndarray, ceiling: float = 0.7) -> np.ndarray:
    peak = float(np.max(np.abs(audio))) or 1.0
    return (audio * min(1.0, ceiling / peak)).astype(np.float32)
