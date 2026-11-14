"""Forced alignment of a rendered line against the script.

The production path re-speaks each word with the same engine and finds that
word, left to right, in the utterance. That is offline and does not need a
second model. If faster-whisper is installed, `whisper_words` is also available
and the alignment report can compare the two.

Phoneme-weighted times remain the last fallback, used only when a word template
cannot be placed.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass
class Word:
    text: str
    start: float
    end: float

    def as_dict(self) -> dict:
        return {"text": self.text, "start": round(self.start, 3), "end": round(self.end, 3)}


def _trim(audio: np.ndarray, sr: int) -> np.ndarray:
    if len(audio) == 0:
        return audio
    thr = 10 ** (-40 / 20)
    idx = np.where(np.abs(audio) > thr)[0]
    if len(idx) == 0:
        return audio
    pad = int(0.02 * sr)
    return audio[max(0, int(idx[0]) - pad): min(len(audio), int(idx[-1]) + pad)].copy()


def find_span(haystack: np.ndarray, needle: np.ndarray, start: int, limit: int | None = None) -> tuple[int, int]:
    needle = _trim(np.asarray(needle, dtype=np.float32), 1)
    n = len(needle)
    ceiling = len(haystack) if limit is None else min(len(haystack), limit)
    if n < 8 or start >= ceiling:
        end = min(ceiling, start + max(n, 1))
        return start, max(start + 1, end)
    window = min(ceiling, start + n + max(n, 8000))
    seg = haystack[start:window].astype(np.float32)
    if len(seg) <= n:
        return start, max(start + 1, window)
    needle = needle - float(needle.mean())
    denom = float(np.sqrt(np.sum(needle ** 2))) + 1e-8
    size = 1
    while size < len(seg) + n:
        size *= 2
    corr = np.fft.irfft(np.fft.rfft(seg, size) * np.conj(np.fft.rfft(needle, size)), size)
    valid = len(seg) - n + 1
    corr = corr[:valid]
    energy = np.sqrt(np.convolve(seg ** 2, np.ones(n, dtype=np.float32), mode="valid")) + 1e-8
    score = corr / (energy * denom)
    idx = int(np.argmax(score))
    return start + idx, start + idx + n


def align_templates(
    utterance: np.ndarray,
    sample_rate: int,
    words: list[str],
    templates: list[np.ndarray],
) -> list[Word]:
    """Place each template inside the utterance, in order. Times are in seconds."""
    if len(words) != len(templates):
        raise ValueError("each written word needs one template")
    cursor = 0
    placed: list[Word] = []
    total = len(utterance)
    count = len(words)
    for index, (word, template) in enumerate(zip(words, templates)):
        reserve = int(0.05 * sample_rate) * (count - index - 1)
        limit = max(cursor + int(0.05 * sample_rate), total - reserve)
        start, end = find_span(utterance, template, cursor, limit)
        end = min(end, limit)
        if end <= start:
            end = min(total, start + int(0.08 * sample_rate))
        placed.append(Word(word, start / sample_rate, end / sample_rate))
        cursor = end
    if placed:
        placed[-1].end = max(placed[-1].end, placed[-1].start + 0.04)
        placed[-1].end = min(placed[-1].end, total / sample_rate)
    return placed


def phoneme_fallback(words: list[str], duration: float, offset: float = 0.0) -> list[Word]:
    weights = [max(1, len(word)) for word in words] or [1]
    total = sum(weights)
    t = offset
    out = []
    for word, weight in zip(words, weights):
        span = duration * weight / total
        out.append(Word(word, t, t + span))
        t += span
    if out:
        out[-1].end = offset + duration
    return out


def whisper_words(path: str, script: str) -> list[Word] | None:
    """Optional faster-whisper pass. Returns None when the package or model is absent."""
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        return None
    model = WhisperModel("tiny.en", device="cpu", compute_type="int8")
    segments, _info = model.transcribe(path, word_timestamps=True, language="en", initial_prompt=script)
    found: list[Word] = []
    for segment in segments:
        for word in segment.words or []:
            token = word.word.strip()
            if token:
                found.append(Word(token, float(word.start), float(word.end)))
    return found or None
