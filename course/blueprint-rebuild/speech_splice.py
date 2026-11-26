"""Replace coin, close, ASIC and API with tokens that measure as the target sounds.

Kokoro af_heart says the ɔɪ in "coin" as the vowel in "eye", and it says the
noun "close" with an unvoiced s. The written words stay as they are. The
audio of those words is replaced after the sentence is aligned.

"coin" comes from af_sky, the Kokoro voice whose isolated "coin" has the
join-vowel: F1 near 650 Hz and F2 near 1000 Hz, then F2 rises past 2000 Hz.
af_heart supplies the other tokens, so the rest of the line stays one voice.
"""

from __future__ import annotations

import re
from functools import lru_cache

import numpy as np

_COIN = re.compile(r"^coin$", re.I)
_CLOSE = re.compile(r"^close$", re.I)  # not closes, closed, closely
_ASIC = re.compile(r"^asic(?:'s)?$", re.I)
_API = re.compile(r"^api$", re.I)


def _bare(text: str) -> str:
    return text.strip(".,!?;:\"'").replace("'", "'")


def _kind(text: str) -> str | None:
    bare = _bare(text)
    if _COIN.match(bare):
        return "coin"
    if _CLOSE.match(bare):
        return "close"
    if _ASIC.match(bare):
        return "asic" if bare.lower() == "asic" else "asics"
    if _API.match(bare):
        return "api"
    return None


def _kokoro():
    from pathlib import Path
    from kokoro_onnx import Kokoro

    folder = Path.home() / ".cache" / "kokoro"
    return Kokoro(str(folder / "kokoro-v1.0.onnx"), str(folder / "voices-v1.0.bin"))


def _trim(audio: np.ndarray, sr: int) -> np.ndarray:
    thr = 10 ** (-38 / 20)
    idx = np.where(np.abs(audio) > thr)[0]
    if len(idx) == 0:
        return audio
    pad = int(0.02 * sr)
    start = max(0, int(idx[0]) - pad)
    end = min(len(audio), int(idx[-1]) + pad)
    return audio[start:end]


@lru_cache(maxsize=1)
def _engine():
    return _kokoro()


def _say(phonemes: str, voice: str) -> tuple[np.ndarray, int]:
    samples, rate = _engine().create(
        phonemes, voice=voice, speed=1.0, lang="en-us", is_phonemes=True,
    )
    audio = _trim(np.asarray(samples, dtype=np.float32), int(rate))
    return audio, int(rate)


def _token(kind: str) -> tuple[np.ndarray, int]:
    # af_sky is the voice whose "coin" actually glides from /ɔ/ to /ɪ/.
    # The other three stay on af_heart.
    spec = {
        "coin": ("kˈɔɪn", "af_sky"),
        "close": ("klˈoʊz", "af_heart"),
        "asic": ("ˈeɪsɪk", "af_heart"),
        "asics": ("ˈeɪsɪks", "af_heart"),
        "api": ("ˈeɪ. pˈiː. ˈaɪ.", "af_heart"),
    }[kind]
    return _say(*spec)


def _fit(token: np.ndarray, samples: int) -> np.ndarray:
    if samples < 8:
        return token[: max(8, samples)]
    if len(token) == samples:
        return token
    positions = np.linspace(0, len(token) - 1, samples)
    return np.interp(positions, np.arange(len(token)), token).astype(np.float32)


def _cross(audio: np.ndarray, start: int, end: int, token: np.ndarray, sr: int) -> None:
    fade = min(int(0.012 * sr), max(1, (end - start) // 8), len(token) // 8)
    if fade > 1 and start > 0:
        ramp = np.linspace(0, 1, fade, dtype=np.float32)
        token = token.copy()
        token[:fade] = token[:fade] * ramp + audio[start:start + fade] * (1 - ramp)
        token[-fade:] = token[-fade:] * ramp[::-1] + audio[end - fade:end] * ramp
    audio[start:end] = token


def splice_sentence(audio: np.ndarray, sr: int, words: list) -> tuple[np.ndarray, list]:
    """Drop the checked token onto each target word. Length can grow."""
    audio = np.asarray(audio, dtype=np.float32).copy()
    shift = 0.0
    for word in words:
        kind = _kind(word.text)
        word.start += shift
        word.end += shift
        if kind is None:
            continue
        token, token_sr = _token(kind)
        if token_sr != sr:
            raise SystemExit(f"splice token rate {token_sr} is not {sr}")
        start = int(round(word.start * sr))
        end = int(round(word.end * sr))
        start = max(0, min(start, len(audio) - 1))
        end = max(start + 8, min(end, len(audio)))
        slot = end - start
        # Keep the diphthong and the three letters from being crushed.
        target = slot
        natural = len(token)
        if natural > int(slot * 1.15):
            target = min(natural, int(0.95 * sr) if kind != "api" else int(1.15 * sr))
        fitted = _fit(token, target)
        slot_audio = audio[start:end]
        slot_rms = float(np.sqrt(np.mean(slot_audio**2)) + 1e-6)
        token_rms = float(np.sqrt(np.mean(fitted**2)) + 1e-6)
        gain = min(2.0, max(0.5, slot_rms / token_rms))
        fitted = (fitted * gain).astype(np.float32)
        if target == slot:
            _cross(audio, start, end, fitted, sr)
        else:
            _cross_insert = fitted
            fade = min(int(0.012 * sr), len(_cross_insert) // 8)
            if fade > 1 and start > 0:
                ramp = np.linspace(0, 1, fade, dtype=np.float32)
                _cross_insert = _cross_insert.copy()
                _cross_insert[:fade] = _cross_insert[:fade] * ramp + audio[start:start + fade] * (1 - ramp)
            audio = np.concatenate([audio[:start], _cross_insert, audio[end:]])
            grown = (target - slot) / sr
            word.end += grown
            shift += grown
    return audio, words


def _formants(audio: np.ndarray, sr: int) -> list[tuple[float, float, float]]:
    import parselmouth

    sound = parselmouth.Sound(np.asarray(audio, dtype=np.float64), sampling_frequency=sr)
    intensity = sound.to_intensity(minimum_pitch=60)
    form = sound.to_formant_burg(time_step=0.01, max_number_of_formants=5, maximum_formant=5500)
    points = []
    t = 0.02
    while t < sound.duration - 0.02:
        loud = intensity.get_value(t)
        f1 = form.get_value_at_time(1, t)
        f2 = form.get_value_at_time(2, t)
        if loud and loud == loud and loud > 55 and f1 and f1 == f1 and f2 and f2 == f2:
            if 200 < f1 < 1200 and 600 < f2 < 3200:
                points.append((t, float(f1), float(f2)))
        t += 0.01
    return points


def _coda(audio: np.ndarray, sr: int) -> tuple[float, float]:
    env = np.convolve(audio**2, np.ones(int(0.015 * sr)) / max(1, int(0.015 * sr)), mode="same")
    peak = float(env.max()) if len(env) else 0.0
    loud = np.where(env > peak * 0.2)[0] if peak else np.array([], dtype=int)
    if len(loud) < int(0.04 * sr):
        return 1.0, 0.0
    end = int(loud[-1])
    start = max(int(loud[0]), end - int(0.07 * sr))
    tail = audio[start:end]
    if len(tail) < 16:
        return 1.0, 0.0
    spec = np.abs(np.fft.rfft(tail * np.hanning(len(tail))))
    freqs = np.fft.rfftfreq(len(tail), 1 / sr)
    high = float(spec[freqs >= 4000].sum() / (spec.sum() + 1e-9))
    tail = tail - tail.mean()
    corr = np.correlate(tail, tail, mode="full")
    corr = corr[len(corr) // 2:]
    lags = range(int(sr / 300), int(sr / 80))
    voiced = float(np.max(corr[list(lags)]) / (corr[0] + 1e-9))
    return high, voiced


def _api_peaks(audio: np.ndarray, sr: int) -> int:
    hop = max(1, int(0.02 * sr))
    energy = np.array([
        float(np.sqrt(np.mean(audio[i:i + hop] ** 2)))
        for i in range(0, max(1, len(audio) - hop), hop)
    ])
    if len(energy) < 3:
        return 0
    thr = float(energy.max()) * 0.45
    peaks = 0
    last = -10
    for index, value in enumerate(energy):
        if value >= thr and index - last >= 3:
            peaks += 1
            last = index
    return peaks


def token_problems() -> list[str]:
    """The isolated tokens have to pass before any lesson is spoken."""
    problems = []
    coin, sr = _token("coin")
    points = _formants(coin, sr)
    if len(points) < 8:
        problems.append("coin token has no vowel")
    else:
        early = points[: max(3, len(points) // 3)]
        late = points[len(points) // 2:]
        f1 = float(np.median([p[1] for p in early]))
        f2 = float(np.median([p[2] for p in early]))
        glide = float(np.median([p[2] for p in late]))
        # /ɔɪ/ starts back and round, then the second vowel is front.
        if not (450 <= f1 <= 750 and 800 <= f2 <= 1400 and glide >= 1800):
            problems.append(f"coin token is not the join vowel: F1 {f1:.0f} F2 {f2:.0f} glide {glide:.0f}")
    close, sr = _token("close")
    high, voiced = _coda(close, sr)
    if not (high < 0.45 and voiced > 0.45):
        problems.append(f"close token coda is not a voiced z: high {high:.2f} voicing {voiced:.2f}")
    asic, sr = _token("asic")
    points = _formants(asic, sr)
    if len(points) < 4:
        problems.append("ASIC token has no vowel")
    else:
        early = points[: max(2, len(points) // 4)]
        f2 = float(np.median([p[2] for p in early]))
        # AY starts with a front vowel. The uh in "uh-sick" does not.
        if f2 < 1800:
            problems.append(f"ASIC token is not AY-sick: early F2 {f2:.0f}")
    api, sr = _token("api")
    if _api_peaks(api, sr) < 3:
        problems.append(f"API token does not have three letters: {_api_peaks(api, sr)} peaks")
    return problems


def master_problems(path, words: list) -> list[str]:
    """Measure the same words on the finished master. One decode, then slices."""
    import subprocess
    import tempfile
    import soundfile as sf

    problems = []
    with tempfile.NamedTemporaryFile(suffix=".wav") as handle:
        subprocess.check_call([
            "ffmpeg", "-y", "-v", "error", "-i", str(path),
            "-vn", "-ac", "1", "-ar", "24000", handle.name,
        ])
        film, rate = sf.read(handle.name)
    film = np.asarray(film, dtype=np.float32)
    targets = [(word, _kind(word.text)) for word in words if _kind(word.text)]
    for word, kind in targets:
        start = max(0, int(word.start * rate))
        end = min(len(film), int(word.end * rate))
        audio = film[start:end]
        if len(audio) < int(0.08 * rate):
            problems.append(f"{kind} at {word.start:.2f}s is too short to measure")
            continue
        if kind == "coin":
            points = _formants(audio, rate)
            if len(points) < 6:
                problems.append(f"coin at {word.start:.2f}s has no vowel")
                continue
            early = points[: max(3, len(points) // 3)]
            late = points[len(points) // 2:]
            f1 = float(np.median([p[1] for p in early]))
            f2 = float(np.median([p[2] for p in early]))
            glide = float(np.median([p[2] for p in late]))
            if not (400 <= f1 <= 800 and f2 <= 1650 and glide >= 1600 and glide > f2 + 400):
                problems.append(
                    f"coin at {word.start:.2f}s is not the join vowel: F1 {f1:.0f} F2 {f2:.0f} glide {glide:.0f}"
                )
        elif kind == "close":
            high, voiced = _coda(audio, rate)
            if not (high < 0.55 and voiced > 0.35):
                problems.append(
                    f"close at {word.start:.2f}s coda is not a voiced z: high {high:.2f} voicing {voiced:.2f}"
                )
        elif kind in {"asic", "asics"}:
            points = _formants(audio, rate)
            if len(points) < 4:
                problems.append(f"ASIC at {word.start:.2f}s has no vowel")
                continue
            early = points[: max(2, len(points) // 4)]
            f2 = float(np.median([p[2] for p in early]))
            if f2 < 1600:
                problems.append(f"ASIC at {word.start:.2f}s is not AY-sick: early F2 {f2:.0f}")
        elif kind == "api":
            peaks = _api_peaks(audio, rate)
            if peaks < 3:
                problems.append(f"API at {word.start:.2f}s has {peaks} bursts, not three letters")
    return problems
