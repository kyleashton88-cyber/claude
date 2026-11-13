"""Optional ElevenLabs Music and Sound Effects adapter.

Reads ELEVENLABS_API_KEY. If the key is absent, or the call fails, the caller
keeps the procedural render. This module never clones a voice and never
composes from an uploaded recording.
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from pathlib import Path

API = "https://api.elevenlabs.io"


class ElevenMusicError(RuntimeError):
    pass


def api_key() -> str | None:
    value = os.environ.get("ELEVENLABS_API_KEY", "").strip()
    return value or None


def _post(path: str, payload: dict, key: str, timeout: float = 120.0) -> bytes:
    if any(token in path for token in ("/voices/add", "/pvc", "clone")):
        raise ElevenMusicError("This adapter does not call cloning or voice-creation endpoints.")
    req = urllib.request.Request(
        API + path,
        data=json.dumps(payload).encode(),
        headers={
            "xi-api-key": key,
            "Content-Type": "application/json",
            "Accept": "audio/mpeg, application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as res:
            return res.read()
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", "replace")[:500]
        raise ElevenMusicError(f"ElevenLabs {exc.code} on {path}: {detail}") from exc


def compose_music(prompt: str, milliseconds: int, dest: Path, *, model: str = "music_v1") -> Path | None:
    """Return the written file, or None when no key is set."""
    key = api_key()
    if key is None:
        return None
    if not 3000 <= milliseconds <= 600000:
        raise ElevenMusicError("music_length_ms must be between 3000 and 600000")
    audio = _post(
        "/v1/music?output_format=mp3_44100_128",
        {
            "prompt": prompt,
            "music_length_ms": int(milliseconds),
            "model_id": model,
            "force_instrumental": True,
        },
        key,
    )
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(audio)
    return dest


def sound_effect(prompt: str, seconds: float, dest: Path) -> Path | None:
    key = api_key()
    if key is None:
        return None
    audio = _post(
        "/v1/sound-generation",
        {
            "text": prompt,
            "duration_seconds": float(seconds),
            "prompt_influence": 0.35,
        },
        key,
    )
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(audio)
    return dest
