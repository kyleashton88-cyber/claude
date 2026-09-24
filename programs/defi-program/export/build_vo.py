#!/usr/bin/env python3
"""Narration engine for every video: Kokoro TTS (offline), sentence by sentence.

Usage:
  python3 build_vo.py <scenes.json> <out_dir> [voice]     narration per scene
  python3 build_vo.py music <seconds> <out.wav> [seed]     ambient music bed

scenes.json: [{"id": "s01", "vo": "...", "speed": 0.96 (optional)}]
Writes <id>.wav per scene, durations.json {id: seconds} and timings.json
{id: {"dur": s, "sentences": [[start, end, text], ...]}} so captions and
on-screen reveals can follow the voice exactly.

How it sounds natural:
  * each sentence is synthesised on its own, so prosody resets like a speaker's;
  * model silence is trimmed and replaced by measured pauses (longer after a
    question, longest at "..." where the narrator deliberately waits);
  * abbreviations such as "A.P.Y." or "U.S.D.C." never end a sentence early;
  * a per-sentence cache means re-renders only synthesise changed lines.
Mastering (high-pass, de-ess, compression, loudness -16 LUFS) happens in
build_video.js when the scene clips are mixed.

Needs: pip install kokoro-onnx soundfile numpy, plus kokoro-v1.0.onnx and
voices-v1.0.bin (github.com/thewh1teagle/kokoro-onnx releases) in
KOKORO_DIR (default: ./tts next to this script).
"""
import hashlib
import json
import os
import re
import sys

import numpy as np
import soundfile as sf

RATE = 24000
PAUSE = {".": 0.30, "!": 0.30, "?": 0.42, ":": 0.26, ";": 0.24, "…": 0.70, "": 0.22}
HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, ".render", "tts-cache")

ABBR = re.compile(r"\b(?:[A-Za-z]\.){2,}[a-z]?")        # A.P.Y.  U.S.D.C.  L.P.s  e.g.
TITLES = re.compile(r"\b(Mr|Mrs|Ms|Dr|St|vs|etc|approx|no)\.", re.I)


def sentences(text):
    """Split narration into [(sentence, pause_after_seconds)].

    "[[pause 3]]" inserts an exact pause (e.g. thinking time in a quiz)."""
    out = []
    for i, piece in enumerate(re.split(r"\[\[pause ([\d.]+)\]\]", text)):
        if i % 2:
            if out:
                out[-1] = (out[-1][0], out[-1][1] + float(piece))
        else:
            out += _sentences(piece)
    return out


def _sentences(text):
    t = re.sub(r"\s+", " ", text.strip())
    t = t.replace("...", "…")
    guard = {}

    def protect(m):
        key = f"⁣{len(guard)}⁣"
        guard[key] = m.group(0)
        return key

    t = ABBR.sub(protect, t)
    t = TITLES.sub(protect, t)
    t = re.sub(r"(\d)\.(\d)", r"\1⁤\2", t)          # decimals: 2.0, 1.5
    parts = re.split(r"(?<=[.!?…])\s+|(?<=…)(?=\S)", t)
    out = []
    for p in parts:
        p = p.strip()
        if not p:
            continue
        for k, v in guard.items():
            p = p.replace(k, v)
        p = p.replace("⁤", ".")
        if p == "…":                                     # bare pause marker
            if out:
                out[-1] = (out[-1][0], out[-1][1] + PAUSE["…"])
            continue
        end = p[-1] if p[-1] in PAUSE else ""
        spoken = p.rstrip("…").strip() or p
        out.append((spoken, PAUSE[end]))
    # An abbreviation that ends a sentence ("... an A.P.Y. Operators start")
    # stays glued to the next one; Kokoro still breathes at the full stop.
    return out


def trim(samples, floor_db=-42.0, pad=0.035):
    """Cut leading/trailing silence, keeping a short natural tail."""
    if len(samples) == 0:
        return samples
    win = int(RATE * 0.01)
    n = len(samples) // win
    if n == 0:
        return samples
    frames = samples[: n * win].reshape(n, win)
    rms = np.sqrt((frames ** 2).mean(axis=1) + 1e-12)
    db = 20 * np.log10(rms / (np.abs(samples).max() + 1e-9))
    voiced = np.where(db > floor_db)[0]
    if len(voiced) == 0:
        return samples
    a = max(0, voiced[0] * win - int(pad * RATE))
    b = min(len(samples), (voiced[-1] + 1) * win + int(pad * 2 * RATE))
    out = samples[a:b].copy()
    fade = min(len(out) // 4, int(0.012 * RATE))        # click-free edges
    if fade > 0:
        out[:fade] *= np.linspace(0, 1, fade)
        out[-fade:] *= np.linspace(1, 0, fade)
    return out


class Voice:
    def __init__(self, voice):
        from kokoro_onnx import Kokoro
        d = os.environ.get("KOKORO_DIR", os.path.join(HERE, "tts"))
        self.k = Kokoro(os.path.join(d, "kokoro-v1.0.onnx"), os.path.join(d, "voices-v1.0.bin"))
        self.voice = voice
        self.lang = "en-gb" if voice.startswith("b") else "en-us"
        os.makedirs(CACHE, exist_ok=True)

    def say(self, text, speed):
        key = hashlib.sha1(f"{self.voice}|{speed}|{text}".encode()).hexdigest()[:20]
        path = os.path.join(CACHE, key + ".npy")
        if os.path.exists(path):
            return np.load(path)
        samples, rate = self.k.create(text, voice=self.voice, speed=speed, lang=self.lang)
        assert rate == RATE, rate
        samples = trim(np.asarray(samples, dtype=np.float32))
        np.save(path, samples)
        return samples


def narrate(scenes_path, out_dir, voice):
    v = Voice(voice)
    os.makedirs(out_dir, exist_ok=True)
    durations, timings = {}, {}
    for scene in json.load(open(scenes_path)):
        speed = scene.get("speed", 0.96)
        chunks, marks, t = [], [], 0.0
        sents = sentences(scene["vo"])
        for i, (s, pause) in enumerate(sents):
            audio = v.say(s, speed)
            d = len(audio) / RATE
            marks.append([round(t, 3), round(t + d, 3), s])
            chunks.append(audio)
            t += d
            if i < len(sents) - 1:
                chunks.append(np.zeros(int(pause * RATE), dtype=np.float32))
                t += pause
        audio = np.concatenate(chunks) if chunks else np.zeros(int(0.5 * RATE), dtype=np.float32)
        sf.write(os.path.join(out_dir, f"{scene['id']}.wav"), audio, RATE, subtype="PCM_16")
        durations[scene["id"]] = len(audio) / RATE
        timings[scene["id"]] = {"dur": len(audio) / RATE, "sentences": marks}
    json.dump(durations, open(os.path.join(out_dir, "durations.json"), "w"), indent=1)
    json.dump(timings, open(os.path.join(out_dir, "timings.json"), "w"), indent=1)
    print(f"{len(durations)} clips, {sum(durations.values()):.1f}s of narration ({voice})")


# ---------------------------------------------------------------- music bed
def music(seconds, out, seed=3):
    """Warm ambient pad (Am9 - Fmaj7 - C6/9 - G6sus), soft bells, room reverb.

    Deterministic, royalty-free by construction. Mixed low and ducked under the
    voice in build_video.js, so it supports rather than competes.
    """
    sr = 44100
    n = int(seconds * sr) + sr * 4
    rng = np.random.default_rng(seed)
    t = np.arange(n) / sr
    midi = lambda m: 440.0 * 2 ** ((m - 69) / 12)
    chords = [[45, 57, 60, 64, 67, 71], [41, 53, 57, 60, 64, 69], [48, 55, 60, 64, 69, 74], [43, 55, 60, 62, 67, 71]]
    bar = 8.0
    left = np.zeros(n)
    right = np.zeros(n)
    for ci in range(int(seconds / bar) + 2):
        notes = chords[ci % len(chords)]
        a, b = int(ci * bar * sr), min(n, int((ci + 1) * bar * sr + 3.5 * sr))
        if a >= n:
            break
        tt = t[a:b] - ci * bar
        env = np.minimum(1, tt / 2.8) * np.clip((bar + 3.5 - tt) / 3.5, 0, 1)
        env = env ** 1.6
        for j, m in enumerate(notes):
            f = midi(m)
            amp = (0.34 if j == 0 else 0.16) / (1 + 0.15 * j)
            for det, pan in ((-0.0035, 0.75), (0.0035, 0.25)):
                ph = rng.uniform(0, 2 * np.pi)
                tone = np.sin(2 * np.pi * f * (1 + det) * tt + ph)
                tone += 0.22 * np.sin(2 * np.pi * 2 * f * (1 + det) * tt + ph)
                tone *= 1 + 0.08 * np.sin(2 * np.pi * 0.21 * tt + j)     # slow breathing
                left[a:b] += amp * env * tone * pan
                right[a:b] += amp * env * tone * (1 - pan)
        # sparse bell notes from the chord, an octave up
        for k in range(3):
            st = a + int((1.4 + k * 2.6 + rng.uniform(0, 0.8)) * sr)
            if st >= n:
                continue
            f = midi(rng.choice(notes[2:]) + 12)
            L = min(n - st, int(4.0 * sr))
            bt = np.arange(L) / sr
            bell = np.sin(2 * np.pi * f * bt) + 0.35 * np.sin(2 * np.pi * 2.76 * f * bt) * np.exp(-bt * 3)
            bell *= np.exp(-bt * 1.25) * np.minimum(1, bt / 0.004) * 0.05
            p = rng.uniform(0.3, 0.7)
            left[st:st + L] += bell * p
            right[st:st + L] += bell * (1 - p)

    def spectral(x, fn):
        X = np.fft.rfft(x)
        f = np.fft.rfftfreq(len(x), 1 / sr)
        return np.fft.irfft(X * fn(f), len(x))

    lp = lambda f: 1 / np.sqrt(1 + (f / 2200) ** 4)        # soft low-pass
    hp = lambda f: 1 / np.sqrt(1 + (60 / np.maximum(f, 1)) ** 4)
    ir_len = int(2.6 * sr)
    ir_t = np.arange(ir_len) / sr
    stereo = []
    for ch in (left, right):
        ch = spectral(ch, lambda f: lp(f) * hp(f))
        ir = rng.standard_normal(ir_len) * np.exp(-ir_t * 2.4)
        ir[0] = 0
        L = len(ch) + ir_len
        wet = np.fft.irfft(np.fft.rfft(ch, L) * np.fft.rfft(ir, L), L)[: len(ch)]
        wet /= np.abs(wet).max() + 1e-9
        ch = ch / (np.abs(ch).max() + 1e-9)
        stereo.append(0.62 * ch + 0.38 * wet)
    y = np.stack(stereo, axis=1)[: int(seconds * sr)]
    fade_in, fade_out = int(1.5 * sr), int(3.0 * sr)
    y[:fade_in] *= np.linspace(0, 1, fade_in)[:, None]
    y[-fade_out:] *= np.linspace(1, 0, fade_out)[:, None]
    y *= 0.5 / (np.abs(y).max() + 1e-9)
    sf.write(out, y.astype(np.float32), sr, subtype="PCM_16")
    print(f"music bed {seconds:.1f}s -> {out}")


if __name__ == "__main__":
    if sys.argv[1] == "music":
        music(float(sys.argv[2]), sys.argv[3], int(sys.argv[4]) if len(sys.argv) > 4 else 3)
    else:
        narrate(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "af_heart")
