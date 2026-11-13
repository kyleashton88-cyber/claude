"""ElevenLabs stock-voice TTS. Cloning endpoints are not implemented and are refused."""

from __future__ import annotations

import base64
import io
import json
import os
import time
import urllib.error
import urllib.request
from pathlib import Path

import numpy as np
import soundfile as sf

from voice.markup import CREDIT_PER_CHARACTER, STOCK_VOICES, Word, words_from_characters

API = "https://api.elevenlabs.io"
BLOCKED = ("clone", "instant-voice", "ivc", "pvc", "use_pvc", "voices/add")


class VoiceError(RuntimeError):
    pass


def assert_stock(voice: str, model: str, extra: dict | None = None) -> str:
    blob = " ".join([voice, model, json.dumps(extra or {})]).lower()
    for token in BLOCKED:
        if token in blob:
            raise VoiceError("Voice cloning is disabled. Use a stock voice name or a stock voice id.")
    if model not in CREDIT_PER_CHARACTER:
        raise VoiceError(f"model {model} is not in the stock model list")
    key = voice.strip()
    if key.lower() in STOCK_VOICES:
        return STOCK_VOICES[key.lower()]
    if len(key) >= 16 and key.replace("-", "").isalnum():
        return key
    known = ", ".join(sorted(STOCK_VOICES))
    raise VoiceError(f"unknown stock voice {voice!r}. Choose one of: {known}")


def _decode(raw: bytes) -> tuple[np.ndarray, int]:
    if raw[:4] == b"RIFF":
        audio, sample_rate = sf.read(io.BytesIO(raw), dtype="float32", always_2d=False)
        return np.asarray(audio, dtype=np.float32), int(sample_rate)
    tmp = Path("/tmp") / "el-voice-decode.mp3"
    tmp.write_bytes(raw)
    wav = tmp.with_suffix(".wav")
    import subprocess

    subprocess.run(
        ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(tmp), "-ac", "1", str(wav)],
        check=True,
    )
    audio, sample_rate = sf.read(str(wav), dtype="float32", always_2d=False)
    return np.asarray(audio, dtype=np.float32), int(sample_rate)


class ElevenLabsEngine:
    def __init__(
        self,
        voice: str = "Brian",
        model: str = "eleven_multilingual_v2",
        *,
        stability: float = 0.45,
        similarity_boost: float = 0.75,
        style: float = 0.0,
        seed: int = 42,
        opener=None,
        sleep=None,
    ):
        self.voice_id = assert_stock(voice, model)
        self.voice_name = voice
        self.model = model
        self.stability = stability
        self.similarity_boost = similarity_boost
        self.style = style
        self.seed = seed
        self.opener = opener or urllib.request.urlopen
        self.sleep = sleep or time.sleep
        self.settings = {
            "voice": voice,
            "voice_id": self.voice_id,
            "model": model,
            "stability": stability,
            "similarity_boost": similarity_boost,
            "style": style,
            "seed": seed,
        }

    def synthesize(self, text: str, previous: str = "", following: str = "") -> tuple[np.ndarray, int, list[Word], str]:
        key = os.environ.get("ELEVENLABS_API_KEY", "").strip()
        if not key and self.opener is urllib.request.urlopen:
            raise VoiceError("ELEVENLABS_API_KEY is not set. Use --engine piper, or export the key and pass --yes.")
        payload = {
            "text": text,
            "model_id": self.model,
            "voice_settings": {
                "stability": self.stability,
                "similarity_boost": self.similarity_boost,
                "style": self.style,
                "use_speaker_boost": True,
            },
            "seed": self.seed,
            "apply_text_normalization": "auto",
        }
        if previous:
            payload["previous_text"] = previous
        if following:
            payload["next_text"] = following
        url = f"{API}/v1/text-to-speech/{self.voice_id}/with-timestamps?output_format=mp3_44100_128"
        body = self._request(url, payload, key or "test")
        raw = base64.b64decode(body["audio_base64"])
        audio, sample_rate = _decode(raw)
        if audio.ndim > 1:
            audio = audio.mean(axis=1)
        alignment = body.get("alignment") or {}
        chars = alignment.get("characters") or []
        starts = alignment.get("character_start_times_seconds") or []
        ends = alignment.get("character_end_times_seconds") or []
        if chars and len(chars) == len(starts) == len(ends):
            words = words_from_characters(chars, starts, ends, 0.0)
            method = "elevenlabs character alignment"
        else:
            from voice.markup import align_phonemes

            words = align_phonemes(text, [], len(audio) / sample_rate, 0.0)
            method = "character alignment missing; weights used"
        return audio.astype(np.float32), sample_rate, words, method

    def _request(self, url: str, payload: dict, key: str) -> dict:
        delay = 1.0
        last = None
        for attempt in range(4):
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode(),
                headers={"xi-api-key": key, "Content-Type": "application/json", "Accept": "application/json"},
                method="POST",
            )
            try:
                with self.opener(req, timeout=90) as res:
                    return json.loads(res.read().decode())
            except urllib.error.HTTPError as exc:
                last = exc
                detail = exc.read().decode("utf-8", "replace")[:400]
                if exc.code in (429, 500, 502, 503, 504) and attempt < 3:
                    retry_after = exc.headers.get("Retry-After") if exc.headers else None
                    wait = float(retry_after) if retry_after else delay
                    self.sleep(wait)
                    delay *= 2
                    continue
                if exc.code in (401, 403):
                    raise VoiceError("ElevenLabs rejected the API key. Reconnect it and try again.") from exc
                raise VoiceError(f"ElevenLabs {exc.code}: {detail}") from exc
        raise VoiceError("ElevenLabs did not answer after retries") from last
