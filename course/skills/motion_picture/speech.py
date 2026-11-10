"""Local speech and the small pronunciation fixes Kokoro needs."""

from __future__ import annotations

import re

import numpy as np

SR = 24000
# Measured on this machine: Kokoro speed 1.0 is about 197 words per minute.
BASE_WPM = 197.0


def spoken_number(n: int) -> str:
    ones = [
        "zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine",
        "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen",
        "seventeen", "eighteen", "nineteen",
    ]
    tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]

    def under_100(v: int) -> str:
        if v < 20:
            return ones[v]
        t, r = divmod(v, 10)
        return tens[t] if r == 0 else f"{tens[t]} {ones[r]}"

    def under_1000(v: int) -> str:
        if v < 100:
            return under_100(v)
        h, r = divmod(v, 100)
        return ones[h] + " hundred" if r == 0 else f"{ones[h]} hundred {under_100(r)}"

    n = int(round(n))
    if n < 0:
        return "minus " + spoken_number(-n)
    if n < 1000:
        return under_1000(n)
    th, r = divmod(n, 1000)
    if r == 0:
        return under_1000(th) + " thousand"
    if r < 100:
        return under_1000(th) + " thousand and " + under_100(r)
    return under_1000(th) + " thousand " + under_1000(r)


def prepare(text: str) -> str:
    text = text.replace("BTC-USD", "bitcoin versus the dollar")
    text = text.replace("API", "A P I")
    text = re.sub(r"\$", "", text)
    # Bare prices like 24930 become words so the voice does not spell digits.
    def repl(match: re.Match) -> str:
        return spoken_number(int(match.group(0).replace(",", "")))

    text = re.sub(r"\b\d{1,3}(?:,\d{3})+\b|\b\d{4,6}\b", repl, text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def choose_speed(words: int) -> float:
    speed = words * 60 / (BASE_WPM * 980)
    return float(min(0.92, max(0.70, speed)))


def synth(pipe, text: str, speed: float) -> np.ndarray:
    chunks = []
    for _g, _p, audio in pipe(prepare(text), voice="af_heart", speed=speed):
        if audio is not None and len(audio):
            chunks.append(np.asarray(audio, dtype=np.float32))
    if not chunks:
        return np.zeros(int(0.4 * SR), dtype=np.float32)
    wav = np.concatenate(chunks)
    thr = 10 ** (-42 / 20)
    idx = np.where(np.abs(wav) > thr)[0]
    if len(idx):
        pad = int(0.05 * SR)
        wav = wav[max(0, int(idx[0]) - pad): min(len(wav), int(idx[-1]) + pad)]
    return wav
