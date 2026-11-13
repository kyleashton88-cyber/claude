"""One interface for Piper and ElevenLabs."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import soundfile as sf

from lib.ffmpeg_util import loudnorm_wav
from voice.markup import Word, cache_key, chunk_text, estimate, parse_segments, write_vtt


def _fade(audio: np.ndarray, sample_rate: int, ms: float = 6.0) -> np.ndarray:
    n = min(len(audio) // 4, int(sample_rate * ms / 1000))
    if n < 2:
        return audio
    ramp = np.linspace(0.0, 1.0, n, dtype=np.float32)
    audio = audio.copy()
    audio[:n] *= ramp
    audio[-n:] *= ramp[::-1]
    return audio


def _load_cached(path: Path) -> tuple[np.ndarray, int, list[Word], str] | None:
    meta_path = path.with_suffix(".json")
    if not path.is_file() or not meta_path.is_file():
        return None
    meta = json.loads(meta_path.read_text())
    audio, sample_rate = sf.read(str(path), dtype="float32", always_2d=False)
    words = [Word(item["text"], item["start"], item["end"]) for item in meta["words"]]
    return np.asarray(audio, dtype=np.float32), int(sample_rate), words, meta.get("method", "cache")


def _store_cache(path: Path, audio: np.ndarray, sample_rate: int, words: list[Word], method: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    sf.write(str(path), audio, sample_rate)
    path.with_suffix(".json").write_text(
        json.dumps({"method": method, "words": [word.as_dict() for word in words]}, indent=2)
    )


class Speaker:
    def __init__(self, engine: str = "piper", voice: str = "lessac", model: str | None = None, cache_dir: Path | None = None, **kwargs):
        self.engine_name = engine
        self.cache_dir = cache_dir
        if engine == "piper":
            from voice.piper_engine import PiperEngine

            if voice not in ("lessac", "en_US-lessac-medium"):
                raise ValueError("the installed Piper stock voice is lessac. ElevenLabs stock names need --engine elevenlabs.")
            self.engine = PiperEngine(**{k: v for k, v in kwargs.items() if k in ("length_scale", "noise_scale", "noise_w_scale", "model")})
            self.model = self.engine.settings["model"]
            self.voice = "lessac"
        elif engine == "elevenlabs":
            from voice.elevenlabs import ElevenLabsEngine

            self.model = model or "eleven_multilingual_v2"
            self.voice = voice or "Brian"
            self.engine = ElevenLabsEngine(voice=self.voice, model=self.model, **kwargs)
        else:
            raise ValueError("engine must be piper or elevenlabs")

    def quote(self, text: str) -> dict:
        return estimate(text, self.engine_name, self.model if self.engine_name == "elevenlabs" else None)

    def synthesize_chunk(self, text: str, previous: str = "", following: str = "") -> tuple[np.ndarray, int, list[Word], str]:
        settings = self.engine.settings
        key = cache_key({"engine": self.engine_name, "settings": settings, "text": text, "previous": previous, "following": following})
        if self.cache_dir:
            cached = _load_cached(self.cache_dir / f"{key}.wav")
            if cached:
                return cached
        if self.engine_name == "piper":
            audio, sample_rate, words, method = self.engine.synthesize(text)
        else:
            audio, sample_rate, words, method = self.engine.synthesize(text, previous, following)
        if self.cache_dir:
            _store_cache(self.cache_dir / f"{key}.wav", audio, sample_rate, words, method)
        return audio, sample_rate, words, method

    def render(self, text: str) -> tuple[np.ndarray, int, list[Word], str]:
        events: list[tuple] = []
        sample_rate = None
        method = ""
        for kind, payload in parse_segments(text):
            if kind == "pause":
                events.append(("pause", float(payload)))
                continue
            chunks = chunk_text(str(payload))
            for index, chunk in enumerate(chunks):
                previous = chunks[index - 1] if index else ""
                following = chunks[index + 1] if index + 1 < len(chunks) else ""
                audio, rate, chunk_words, method = self.synthesize_chunk(chunk, previous, following)
                if sample_rate is None:
                    sample_rate = rate
                if rate != sample_rate:
                    raise RuntimeError("a chunk came back at a different sample rate")
                events.append(("audio", _fade(np.asarray(audio, dtype=np.float32).reshape(-1), rate), chunk_words))
        if sample_rate is None:
            raise ValueError("nothing to speak")
        pieces: list[np.ndarray] = []
        words: list[Word] = []
        clock = 0.0
        for event in events:
            if event[0] == "pause":
                pieces.append(np.zeros(int(event[1] * sample_rate), dtype=np.float32))
                clock += event[1]
            else:
                audio, chunk_words = event[1], event[2]
                for word in chunk_words:
                    words.append(Word(word.text, word.start + clock, word.end + clock))
                pieces.append(audio)
                clock += len(audio) / sample_rate
        return np.concatenate(pieces), sample_rate, words, method


def render_to_file(text: str, dest: Path, speaker: Speaker) -> dict:
    quote = speaker.quote(text)
    audio, sample_rate, words, method = speaker.render(text)
    dest.parent.mkdir(parents=True, exist_ok=True)
    raw = dest.with_suffix(".raw.wav")
    sf.write(str(raw), audio, sample_rate)
    loudnorm_wav(raw, dest, integrated=-16.0, true_peak=-1.0)
    raw.unlink(missing_ok=True)
    vtt = dest.with_suffix(".vtt")
    write_vtt(words, vtt)
    sidecar = dest.with_suffix(".json")
    payload = {
        "estimate": quote,
        "alignment": method,
        "words": [word.as_dict() for word in words],
        "wav": dest.name,
        "vtt": vtt.name,
    }
    sidecar.write_text(json.dumps(payload, indent=2) + "\n")
    return payload
