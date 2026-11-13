"""Piper, self-hosted. Stock checkpoints only. No cloning and no recordings."""

from __future__ import annotations

import os
import urllib.request
from pathlib import Path

import numpy as np

VOICES = {
    "lessac": (
        "https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/medium/en_US-lessac-medium.onnx",
    ),
}
CACHE = Path.home() / ".cache" / "piper-voices"


def model_path(voice: str = "lessac") -> Path:
    override = os.environ.get("PIPER_MODEL", "").strip()
    if override and voice == "lessac":
        return Path(override)
    if voice not in VOICES:
        raise KeyError(f"unknown Piper voice {voice}. bundled name: lessac")
    return CACHE / f"en_US-{voice}-medium.onnx"


def ensure_model(voice: str = "lessac") -> Path:
    path = model_path(voice)
    config = Path(str(path) + ".json")
    if path.is_file() and config.is_file():
        return path
    url = VOICES[voice][0]
    path.parent.mkdir(parents=True, exist_ok=True)
    urllib.request.urlretrieve(url, path)
    urllib.request.urlretrieve(url + ".json", config)
    return path


class PiperEngine:
    def __init__(self, voice: str = "lessac"):
        from piper import PiperVoice

        self.voice_name = voice
        self.model = ensure_model(voice)
        self.voice = PiperVoice.load(str(self.model))

    def say(self, text: str, length_scale: float, noise_scale: float = 0.45) -> tuple[np.ndarray, int]:
        from piper.config import SynthesisConfig

        config = SynthesisConfig(
            length_scale=length_scale,
            noise_scale=noise_scale,
            noise_w_scale=0.6,
        )
        parts = []
        rate = None
        for chunk in self.voice.synthesize(text, syn_config=config):
            parts.append(np.asarray(chunk.audio_float_array, dtype=np.float32))
            rate = chunk.sample_rate
        if not parts or rate is None:
            raise RuntimeError("Piper returned no audio")
        return np.concatenate(parts), rate
