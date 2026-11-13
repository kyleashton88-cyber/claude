"""Kokoro, self-hosted, Apache-2.0 weights. af_heart is the default.

The onnx build is the same one the lesson narrator uses. Models are downloaded
by setup.sh into ~/.cache/kokoro and are not committed.
"""

from __future__ import annotations

import os
from pathlib import Path

import numpy as np

DEFAULT_DIR = Path(os.environ.get("KOKORO_DIR", Path.home() / ".cache" / "kokoro"))


class KokoroEngine:
    def __init__(self, voice: str = "af_heart", model_dir: Path | None = None):
        from kokoro_onnx import Kokoro

        folder = model_dir or DEFAULT_DIR
        onnx = folder / "kokoro-v1.0.onnx"
        voices = folder / "voices-v1.0.bin"
        if not onnx.is_file() or not voices.is_file():
            raise FileNotFoundError(
                f"Kokoro files are not in {folder}. Run skills/video-production/natural-voice/setup.sh"
            )
        self.kokoro = Kokoro(str(onnx), str(voices))
        self.voice_name = voice
        self.lang = "en-gb" if voice.startswith("b") else "en-us"

    def say(self, text: str, speed: float) -> tuple[np.ndarray, int]:
        samples, rate = self.kokoro.create(text, voice=self.voice_name, speed=speed, lang=self.lang)
        return np.asarray(samples, dtype=np.float32), int(rate)
