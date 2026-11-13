"""Piper stock voice. No cloning, no custom recordings."""

from __future__ import annotations

import os
import urllib.request
from pathlib import Path

import numpy as np

from voice.markup import Word, align_phonemes, split_sentences

ONNX = "https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/medium/en_US-lessac-medium.onnx"
JSON = ONNX + ".json"
DEFAULT_MODEL = Path.home() / ".cache" / "piper-voices" / "en_US-lessac-medium.onnx"


def model_path() -> Path:
    override = os.environ.get("PIPER_MODEL", "").strip()
    return Path(override) if override else DEFAULT_MODEL


def ensure_model(path: Path | None = None) -> Path:
    path = path or model_path()
    config = Path(str(path) + ".json")
    if path.is_file() and config.is_file():
        return path
    path.parent.mkdir(parents=True, exist_ok=True)
    urllib.request.urlretrieve(ONNX, path)
    urllib.request.urlretrieve(JSON, config)
    return path


class PiperEngine:
    def __init__(self, model: Path | None = None, length_scale: float = 1.05, noise_scale: float = 0.5, noise_w_scale: float = 0.6):
        from piper import PiperVoice
        from piper.config import SynthesisConfig

        self.model = ensure_model(model)
        self.voice = PiperVoice.load(str(self.model))
        # One config for every chunk, so a long script does not drift in pace.
        self.config = SynthesisConfig(
            length_scale=length_scale,
            noise_scale=noise_scale,
            noise_w_scale=noise_w_scale,
        )
        self.settings = {
            "voice": "lessac",
            "length_scale": length_scale,
            "noise_scale": noise_scale,
            "noise_w_scale": noise_w_scale,
            "model": self.model.name,
        }

    def synthesize(self, text: str) -> tuple[np.ndarray, int, list[Word], str]:
        chunks = list(self.voice.synthesize(text, syn_config=self.config, include_alignments=True))
        if not chunks:
            raise RuntimeError("Piper returned no audio")
        sentences = split_sentences(text)
        phonemes = self.voice.phonemize(text)
        sample_rate = chunks[0].sample_rate
        if len(chunks) == len(sentences) == len(phonemes):
            audio_parts = []
            words: list[Word] = []
            offset = 0.0
            for sentence, chunk, phones in zip(sentences, chunks, phonemes):
                audio = np.asarray(chunk.audio_float_array, dtype=np.float32)
                duration = len(audio) / sample_rate
                words.extend(align_phonemes(sentence, list(phones), duration, offset))
                audio_parts.append(audio)
                offset += duration
            method = "sentence-exact, phoneme-weighted inside the sentence"
            return np.concatenate(audio_parts), sample_rate, words, method
        audio = np.concatenate([np.asarray(chunk.audio_float_array, dtype=np.float32) for chunk in chunks])
        words = align_phonemes(text, [phone for sentence in phonemes for phone in sentence], len(audio) / sample_rate, 0.0)
        return audio, sample_rate, words, "phoneme-weighted across the chunk"
