"""Original beds. No samples, no soundfont. Deterministic from key, mood, tempo, and length."""

from __future__ import annotations

import numpy as np
from scipy.signal import lfilter

SR = 48000

ROOTS = {
    "C": 60, "C#": 61, "Db": 61, "D": 62, "Eb": 63, "E": 64,
    "F": 65, "F#": 66, "Gb": 66, "G": 67, "Ab": 68, "A": 69,
    "Bb": 70, "B": 71,
}
SCALES = {
    "major": [0, 2, 4, 5, 7, 9, 11],
    "minor": [0, 2, 3, 5, 7, 8, 10],
}
PROGRESSIONS = {
    "calm": [1, 4, 6, 5],
    "focused": [1, 5, 6, 4],
    "hopeful": [1, 4, 5, 6],
}


def hz(midi: float) -> float:
    return 440.0 * 2.0 ** ((midi - 69.0) / 12.0)


def degree_midi(root: int, scale: list[int], degree: int, octave: int = 0) -> int:
    index = degree - 1
    return root + scale[index % 7] + 12 * (index // 7) + 12 * octave


def triad(root: int, scale: list[int], degree: int) -> list[int]:
    return [degree_midi(root, scale, degree + step) for step in (0, 2, 4)]


def lowpass(x: np.ndarray, cutoff: float, sr: int = SR) -> np.ndarray:
    a = float(np.exp(-2.0 * np.pi * cutoff / sr))
    return lfilter([1.0 - a], [1.0, -a], x).astype(np.float32)


def adsr(n: int, attack: int, decay: int, sustain: float, release: int) -> np.ndarray:
    env = np.zeros(n, dtype=np.float32)
    a = min(n, max(1, attack))
    env[:a] = np.linspace(0.0, 1.0, a, dtype=np.float32)
    d = min(max(0, n - a), max(1, decay))
    if d:
        env[a : a + d] = np.linspace(1.0, sustain, d, dtype=np.float32)
    rel_start = max(a + d, n - max(1, release))
    if rel_start < n:
        hold = rel_start
        if hold > a + d:
            env[a + d : hold] = sustain
        env[rel_start:] = np.linspace(env[rel_start - 1] if rel_start else sustain, 0.0, n - rel_start, dtype=np.float32)
    return env


def _place(buf: np.ndarray, start: int, audio: np.ndarray) -> None:
    if start >= len(buf) or start < 0:
        return
    end = min(len(buf), start + len(audio))
    buf[start:end] += audio[: end - start]


def _tone(freq: float, n: int, partials: tuple[tuple[float, float], ...]) -> np.ndarray:
    t = np.arange(n, dtype=np.float32) / SR
    y = np.zeros(n, dtype=np.float32)
    for harm, amp in partials:
        y += amp * np.sin(2.0 * np.pi * freq * harm * t).astype(np.float32)
    return y


def render_bed(
    *,
    mood: str = "calm",
    key: str = "C",
    scale: str = "major",
    bpm: float = 72.0,
    seconds: float = 60.0,
    seed: int = 7,
) -> tuple[np.ndarray, int]:
    if mood not in PROGRESSIONS:
        raise ValueError(f"unknown mood {mood}. choices: {', '.join(PROGRESSIONS)}")
    if key not in ROOTS:
        raise ValueError(f"unknown key {key}")
    if scale not in SCALES:
        raise ValueError(f"unknown scale {scale}")
    if not 40 <= bpm <= 140:
        raise ValueError("bpm must be between 40 and 140")
    if not 1 <= seconds <= 600:
        raise ValueError("seconds must be between 1 and 600")

    n = int(seconds * SR)
    left = np.zeros(n, dtype=np.float32)
    right = np.zeros(n, dtype=np.float32)
    root = ROOTS[key]
    steps = SCALES[scale]
    prog = PROGRESSIONS[mood]
    beat = 60.0 / bpm
    bar = beat * 4.0
    chord_len = bar * 4.0
    rng = np.random.default_rng(seed)

    chord_index = 0
    start_sec = 0.0
    while start_sec < seconds:
        degree = prog[chord_index % len(prog)]
        notes = triad(root, steps, degree)
        dur = int(min(chord_len + 0.6, seconds - start_sec + 0.6) * SR)
        dur = max(dur, int(0.2 * SR))
        pad = np.zeros(dur, dtype=np.float32)
        for i, midi in enumerate(notes):
            detune = 1.0 + (0.002 if i == 0 else -0.0015)
            voice = _tone(hz(midi - 12) * detune, dur, ((1.0, 0.55), (2.0, 0.18), (3.0, 0.05)))
            voice += _tone(hz(midi) * detune, dur, ((1.0, 0.22), (2.0, 0.06)))
            pad += voice
        pad *= adsr(dur, int(0.55 * SR), int(0.4 * SR), 0.72, int(0.7 * SR))
        pad = lowpass(pad, 900.0 if mood == "calm" else 1400.0)
        at = int(start_sec * SR)
        # A few milliseconds of width, not a hard pan.
        shift = int(0.011 * SR)
        _place(left, at, pad * 0.34)
        _place(right, at + shift, pad * 0.30)

        # Soft pluck on beat 1 of each bar, walking the triad.
        bars = 4
        for b in range(bars):
            when = start_sec + b * bar
            if when >= seconds:
                break
            midi = notes[b % 3] + 12
            pn = int(0.55 * SR)
            pluck = _tone(hz(midi), pn, ((1, 0.7), (2, 0.28), (3, 0.12), (5, 0.04)))
            pluck *= np.exp(-np.arange(pn) / (0.16 * SR)).astype(np.float32)
            pluck = lowpass(pluck, 2400.0)
            level = 0.16 if mood == "calm" else 0.20
            _place(left, int(when * SR), pluck * level)
            _place(right, int(when * SR) + 180, pluck * level * 0.85)
            # Bass on beats 1 and 3.
            for sub in (0.0, beat * 2):
                bass_at = when + sub
                if bass_at >= seconds:
                    continue
                bn = int(0.7 * SR)
                bass_midi = notes[0] - 12
                if sub > 0:
                    bass_midi = notes[0] - 12 + (7 if scale == "major" else 7)
                bass = _tone(hz(bass_midi), bn, ((1, 0.9), (2, 0.15)))
                bass *= np.exp(-np.arange(bn) / (0.28 * SR)).astype(np.float32)
                bass = lowpass(bass, 220.0)
                _place(left, int(bass_at * SR), bass * 0.22)
                _place(right, int(bass_at * SR), bass * 0.22)

        if mood != "calm":
            step = beat / 2.0
            ticks = int(chord_len / step)
            for k in range(ticks):
                when = start_sec + k * step
                if when >= seconds:
                    break
                tn = int(0.045 * SR)
                noise = rng.normal(0, 1, tn).astype(np.float32)
                tick = lowpass(noise, 6000.0) - lowpass(noise, 2500.0)
                tick *= np.exp(-np.arange(tn) / (0.012 * SR)).astype(np.float32)
                level = 0.035 if mood == "focused" else 0.05
                pan = 0.6 if k % 2 == 0 else 0.4
                _place(left, int(when * SR), tick * level * pan)
                _place(right, int(when * SR), tick * level * (1 - pan))

        chord_index += 1
        start_sec += chord_len

    # One-pass room. Short, quiet, so the bed stays out of the way of a voice.
    mix = np.column_stack([left, right])
    for delay, gain in ((int(0.037 * SR), 0.18), (int(0.059 * SR), 0.12), (int(0.083 * SR), 0.08)):
        wet = np.zeros_like(mix)
        wet[delay:] += mix[:-delay] * gain
        mix += lowpass(wet, 3500.0) if wet.ndim == 1 else np.column_stack(
            [lowpass(wet[:, 0], 3500.0), lowpass(wet[:, 1], 3500.0)]
        )

    fade_in = int(1.6 * SR)
    fade_out = int(2.4 * SR)
    env = np.ones(n, dtype=np.float32)
    env[:fade_in] = np.linspace(0.0, 1.0, fade_in, dtype=np.float32)
    env[-fade_out:] = np.linspace(1.0, 0.0, fade_out, dtype=np.float32)
    mix *= env[:, None]
    peak = float(np.max(np.abs(mix))) or 1.0
    mix *= min(1.0, 0.7 / peak)
    return mix.astype(np.float32), SR
