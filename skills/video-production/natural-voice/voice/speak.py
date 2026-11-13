"""Kokoro or Piper, one call. Paid speech APIs are not part of this skill."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import soundfile as sf

from lib.ffmpeg_util import loudnorm_wav
from lib.mix import VOICE_LUFS, TRUE_PEAK_DBTP
from voice.align import Word, align_templates, phoneme_fallback
from voice.captions import write_srt, write_vtt, write_words
from voice.markup import _sentences, parse_markup, section_breaks, written_text
from voice.moods import DEFAULT_ENGINE, DEFAULT_MOOD, kokoro_speed, mood as mood_preset, piper_length_scale
from voice.pronounce import apply_pronunciation

CACHE = Path.home() / ".cache" / "video-production" / "voice"


def _trim(audio: np.ndarray, sr: int) -> np.ndarray:
    if len(audio) == 0:
        return audio
    thr = 10 ** (-42 / 20)
    idx = np.where(np.abs(audio) > thr)[0]
    if len(idx) == 0:
        return audio
    pad = int(0.03 * sr)
    out = audio[max(0, int(idx[0]) - pad): min(len(audio), int(idx[-1]) + pad)].copy()
    fade = min(len(out) // 4, int(0.01 * sr))
    if fade > 1:
        out[:fade] *= np.linspace(0, 1, fade, dtype=np.float32)
        out[-fade:] *= np.linspace(1, 0, fade, dtype=np.float32)
    return out


def _pitch(audio: np.ndarray, semitones: float) -> np.ndarray:
    if abs(semitones) < 0.05 or len(audio) < 8:
        return audio
    factor = 2 ** (semitones / 12.0)
    stretched = np.interp(np.linspace(0, len(audio) - 1, int(len(audio) / factor)), np.arange(len(audio)), audio)
    return np.interp(np.linspace(0, len(stretched) - 1, len(audio)), np.arange(len(stretched)), stretched).astype(np.float32)


class Speaker:
    def __init__(self, engine: str = DEFAULT_ENGINE, mood: str = DEFAULT_MOOD, cache: bool = True):
        if engine not in ("kokoro", "piper"):
            raise ValueError("engine must be kokoro or piper. There is no paid speech engine.")
        self.engine_name = engine
        self.mood_name = mood
        self.preset = mood_preset(mood)
        self.cache = cache
        if engine == "kokoro":
            from voice.kokoro_engine import KokoroEngine
            self.engine = KokoroEngine(voice=self.preset["kokoro_voice"])
        else:
            from voice.piper_engine import PiperEngine
            self.engine = PiperEngine(voice=self.preset["piper_voice"])

    def _cache_key(self, text: str, rate: float) -> str:
        blob = json.dumps({"e": self.engine_name, "m": self.mood_name, "r": round(rate, 3), "t": text}, sort_keys=True)
        return hashlib.sha256(blob.encode()).hexdigest()[:24]

    def say(self, text: str, rate: float = 1.0) -> tuple[np.ndarray, int]:
        spoken = apply_pronunciation(text)
        key = self._cache_key(spoken, rate)
        path = CACHE / f"{key}.npy"
        meta = CACHE / f"{key}.json"
        if self.cache and path.is_file() and meta.is_file():
            info = json.loads(meta.read_text())
            return np.load(path), int(info["sr"])
        if self.engine_name == "kokoro":
            audio, sr = self.engine.say(spoken, kokoro_speed(self.mood_name, rate))
        else:
            audio, sr = self.engine.say(spoken, piper_length_scale(self.mood_name, rate))
        audio = _trim(audio, sr)
        audio = _pitch(audio, self.preset["pitch_semitones"] + (0.4 if rate < 1 else 0.0))
        audio = (audio * self.preset["energy"]).astype(np.float32)
        if self.cache:
            CACHE.mkdir(parents=True, exist_ok=True)
            np.save(path, audio)
            meta.write_text(json.dumps({"sr": sr}))
        return audio, sr

    def render(self, text: str) -> tuple[np.ndarray, int, list[Word], str]:
        pieces: list[np.ndarray] = []
        sample_rate = None
        blocks = section_breaks(text)
        for index, block in enumerate(blocks):
            for span in parse_markup(block):
                if span.kind == "pause":
                    if sample_rate is None:
                        continue
                    pieces.append(np.zeros(int(span.pause * self.preset["pause_scale"] * sample_rate), dtype=np.float32))
                    continue
                lines = _sentences(span.text)
                for line_index, (line, pause) in enumerate(lines):
                    if not line or not line.strip(".,!?;:…"):
                        if sample_rate:
                            pieces.append(np.zeros(int(max(pause, 0.12) * sample_rate), dtype=np.float32))
                        continue
                    audio, rate = self.say(line, span.rate)
                    if sample_rate is None:
                        sample_rate = rate
                    if rate != sample_rate:
                        raise RuntimeError("a line came back at a different sample rate")
                    pieces.append(audio)
                    gap = pause * self.preset["pause_scale"]
                    if line_index < len(lines) - 1 or span.kind == "speech":
                        pieces.append(np.zeros(int(gap * sample_rate), dtype=np.float32))
            if index < len(blocks) - 1 and sample_rate:
                pieces.append(np.zeros(int(self.preset["breath"] * sample_rate), dtype=np.float32))
        if not pieces or sample_rate is None:
            raise ValueError("nothing to speak")
        utterance = np.concatenate(pieces)
        words = written_text(text).split()
        templates = []
        for word in words:
            template, rate = self.say(word.strip(".,!?;:"), 1.0)
            if rate != sample_rate:
                raise RuntimeError("template sample rate changed")
            templates.append(template)
        try:
            aligned = align_templates(utterance, sample_rate, words, templates)
            method = "acoustic-forced-align"
        except Exception:
            aligned = phoneme_fallback(words, len(utterance) / sample_rate)
            method = "phoneme-weighted-fallback"
        return utterance, sample_rate, aligned, method


def render_to_file(text: str, dest: Path, speaker: Speaker) -> dict:
    audio, sample_rate, words, method = speaker.render(text)
    dest.parent.mkdir(parents=True, exist_ok=True)
    raw = dest.with_suffix(".raw.wav")
    sf.write(str(raw), audio, sample_rate)
    loudnorm_wav(raw, dest, integrated=VOICE_LUFS, true_peak=TRUE_PEAK_DBTP)
    raw.unlink(missing_ok=True)
    write_words(dest.with_suffix(".words.json"), words, engine=speaker.engine_name, mood=speaker.mood_name, method=method)
    write_vtt(dest.with_suffix(".vtt"), words)
    write_srt(dest.with_suffix(".srt"), words)
    # Loudnorm keeps duration, so the word times still match the mastered file.
    return {"method": method, "words": len(words), "wav": str(dest)}
