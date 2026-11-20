"""Moods for crypto education. Each one is a rate, a pause scale, and a small pitch shift.

Kokoro af_heart is the default because that is the voice on the existing masters.
Piper lessac is the other free voice in the side-by-side samples.
Measured bases: Kokoro speed 1.0 is about 197 words a minute. Piper lessac at
length_scale 1.0 is about 222 words a minute.
"""

from __future__ import annotations

KOKORO_BASE_WPM = 197.0
PIPER_BASE_WPM = 222.0

MOODS = {
    "calm-teacher": {
        "wpm": 148,
        "pause_scale": 1.0,
        "breath": 0.42,
        "pitch_semitones": 0.0,
        "energy": 1.0,
        "kokoro_voice": "af_heart",
        "piper_voice": "lessac",
    },
    "upbeat-intro": {
        "wpm": 176,
        "pause_scale": 0.7,
        "breath": 0.24,
        "pitch_semitones": 0.6,
        "energy": 1.06,
        "kokoro_voice": "af_heart",
        "piper_voice": "lessac",
    },
    "serious-risk": {
        "wpm": 126,
        "pause_scale": 1.28,
        "breath": 0.55,
        "pitch_semitones": -0.5,
        "energy": 0.94,
        "kokoro_voice": "af_heart",
        "piper_voice": "lessac",
    },
    "recap": {
        "wpm": 152,
        "pause_scale": 1.1,
        "breath": 0.48,
        "pitch_semitones": 0.0,
        "energy": 1.0,
        "kokoro_voice": "af_heart",
        "piper_voice": "lessac",
    },
}

DEFAULT_MOOD = "calm-teacher"
DEFAULT_ENGINE = "kokoro"


def mood(name: str) -> dict:
    if name not in MOODS:
        raise KeyError(f"unknown mood {name}. choices: {', '.join(MOODS)}")
    return MOODS[name]


def kokoro_speed(name: str, rate: float = 1.0) -> float:
    return max(0.5, min(1.6, mood(name)["wpm"] / KOKORO_BASE_WPM * rate))


def piper_length_scale(name: str, rate: float = 1.0) -> float:
    # length_scale above 1 is slower.
    return max(0.6, min(2.0, PIPER_BASE_WPM / (mood(name)["wpm"] * rate)))
