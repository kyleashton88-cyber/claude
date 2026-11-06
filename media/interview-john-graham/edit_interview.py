#!/usr/bin/env python3
"""Edit the John and Graham interview for Jess (Market Pros).

Joins the lossless stream-copy segments, starts the cut in the silence after
the host has introduced John and Graham, and repairs John's microphone only.

John's track is dual-mono with Graham and the host, so he cannot be split by
channel. His mic is identified by a stable spectral signature measured on the
opening: a loud 110–180 Hz resonance and a speech band (500–2000 Hz) about
17 dB quieter than Graham. Graham and the host are left sample-for-sample
untouched outside short crossfades.

What was tried and not kept
- Single-channel WPE dereverb (nara_wpe) did not reduce the resonance or
  raise the speech band. The "room" on John is that resonance plus the
  missing presence, not a tail WPE can subtract.
- afftdn, anlmdn and arnndn did not move the speech-band spectrum. There is
  no discrete 50/60 Hz hum and the speech-band noise floor is already similar
  to Graham's once the level is matched, so a broadband denoiser is not applied.
- The source never hits full scale (peak about -2 dBFS, on the louder mics).
  A soft ceiling only stops the makeup gain from creating new clipping.

Video is stream-copied from the next keyframe. The short head before that
keyframe is re-encoded at CRF 8 (High profile 4:2:0, which cannot store a
mathematically lossless stream) so the trim is frame-accurate and the head
still concatenates with the bit-identical tail.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import wave
from pathlib import Path

import numpy as np
from scipy import signal

SR = 48000
# Silence between the host's handoff ("Awesome. John.") and John's first line
# ("Nice to meet you, Graham."). Energy of that word begins at 48.86 s.
CUT_S = 48.60
# First keyframe after the cut. Parts were stream-copied, so keyframes sit
# about 36 s apart: 0, 36.000, 60.040, ...
KEYFRAME_S = 60.040
FADE_S = 0.030


def run(cmd: list[str]) -> None:
    print("+", " ".join(cmd), flush=True)
    subprocess.check_call(cmd)


def concat_parts(parts: list[Path], dest: Path) -> None:
    lst = dest.with_suffix(".concat.txt")
    lst.write_text("".join(f"file '{p.resolve()}'\n" for p in parts))
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(dest)])


def read_mono_f64(path: Path) -> np.ndarray:
    """Decode audio to mono float64 in [-1, 1]. Stereo is averaged."""
    raw = path.with_suffix(".f64le")
    run(
        [
            "ffmpeg", "-y", "-i", str(path),
            "-vn", "-ac", "1", "-ar", str(SR),
            "-f", "f64le", "-c:a", "pcm_f64le",
            str(raw),
        ]
    )
    audio = np.fromfile(raw, dtype="<f8")
    if audio.size == 0:
        raise RuntimeError(f"no audio decoded from {path}")
    return audio


def write_wav(path: Path, audio: np.ndarray) -> None:
    pcm = np.clip(audio, -1.0, 1.0).astype("<f4")
    # Write float32 via ffmpeg from a raw pipe would add a process; use the
    # stdlib for int16 so the AAC encode has a plain PCM source.
    i16 = np.clip(np.round(audio * 32767.0), -32768, 32767).astype("<i2")
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(i16.tobytes())
    del pcm


def band_envelope(x: np.ndarray, lo: float, hi: float, hop: int, win: int) -> np.ndarray:
    sos = signal.butter(4, [lo, hi], btype="band", fs=SR, output="sos")
    y = signal.sosfiltfilt(sos, x)
    y2 = y * y
    c = np.cumsum(y2)
    idx = np.arange(0, len(x) - win, hop)
    e = c[idx + win] - c[idx]
    return np.sqrt(e / win + 1e-18)


def db(v: np.ndarray) -> np.ndarray:
    return 20.0 * np.log10(v + 1e-12)


def john_mask(x: np.ndarray) -> tuple[np.ndarray, list[tuple[float, float]]]:
    """Sample-rate mask that is 1 on John's mic and 0 on Graham and the host.

    Thresholds come from the opening, where the picture and the transcript
    say who is talking. John's 110–180 Hz band sits well above his own
    500–2000 Hz band, and that speech band never reaches Graham's or the
    host's. A frame has to stay boom-heavy for several hops before it can
    seed a turn, so a single plosive on the loud mics cannot open the mask.
    The seed then grows across his own pauses and stops at the other mic.
    """
    hop = int(0.020 * SR)
    win = int(0.040 * SR)
    boom = band_envelope(x, 110, 180, hop, win)
    pres = band_envelope(x, 500, 2000, hop, win)
    full = band_envelope(x, 80, 8000, hop, win)
    times = (np.arange(len(boom)) * hop + win / 2) / SR
    ratio = db(boom) - db(pres)
    full_db = db(full)
    pres_db = db(pres)
    boom_db = db(boom)

    # Loud, clear speech that is not boom-dominated. This is the barrier.
    other = (pres_db > -34.0) & (ratio < 8.0)
    raw_seed = (ratio > 12.0) & (pres_db < -40.0) & (boom_db > -48.0) & (full_db > -50.0) & ~other
    # Median of a binary run is 1 only when at least 3 of 5 frames are seeds.
    stable = signal.medfilt(raw_seed.astype(np.float64), kernel_size=5) >= 0.5

    mask_f = stable.copy()
    for _ in range(int(0.60 / 0.020)):
        neigh = np.zeros_like(mask_f)
        neigh[1:] = mask_f[:-1]
        neigh[:-1] |= mask_f[1:]
        new = neigh & ~other & ~mask_f & (full_db > -60.0)
        if not np.any(new):
            break
        mask_f |= new

    segs = _segments(times, mask_f)
    kept: list[tuple[float, float]] = []
    for a, b in segs:
        if (b - a) < 0.30:
            continue
        m = (times >= a) & (times <= b)
        # A real turn contains a sustained seed, not one spiked hop that grew.
        if float(np.sum(stable[m]) * 0.020) < 0.18:
            continue
        # Graham's mic stays clear in the speech band. A span whose middle is
        # that loud is his voice, even if the edges went boomy for a moment.
        if float(np.median(pres_db[m])) > -48.0:
            continue
        kept.append((a, b))

    merged: list[tuple[float, float]] = []
    for a, b in kept:
        if merged and a <= merged[-1][1] + 0.02:
            merged[-1] = (merged[-1][0], max(merged[-1][1], b))
        else:
            merged.append((a, b))

    sample_mask = np.zeros(len(x), dtype=np.float64)
    fade = int(FADE_S * SR)
    ramp = np.linspace(0.0, 1.0, fade, endpoint=False) if fade else np.array([])
    for a, b in merged:
        i0 = max(0, int(round(a * SR)))
        i1 = min(len(x), int(round(b * SR)))
        if i1 - i0 < 2 * fade + 8:
            continue
        sample_mask[i0:i1] = 1.0
        sample_mask[i0 : i0 + fade] = ramp
        sample_mask[i1 - fade : i1] = ramp[::-1]
    return sample_mask, merged


def _segments(times: np.ndarray, mask: np.ndarray) -> list[tuple[float, float]]:
    if not mask.any():
        return []
    d = np.diff(mask.astype(np.int8))
    starts = list(np.flatnonzero(d == 1) + 1)
    ends = list(np.flatnonzero(d == -1) + 1)
    if mask[0]:
        starts = [0] + starts
    if mask[-1]:
        ends = ends + [len(mask)]
    return [(float(times[s]), float(times[e - 1])) for s, e in zip(starts, ends)]


def bell(x: np.ndarray, f0: float, q: float, gain_db: float) -> np.ndarray:
    """Zero-phase peaking EQ. filtfilt applies the curve twice, so gain_db is half the audible amount."""
    A = 10 ** (gain_db / 40.0)
    w0 = 2 * np.pi * f0 / SR
    alpha = np.sin(w0) / (2 * q)
    b0 = 1 + alpha * A
    b1 = -2 * np.cos(w0)
    b2 = 1 - alpha * A
    a0 = 1 + alpha / A
    a1 = -2 * np.cos(w0)
    a2 = 1 - alpha / A
    b = np.array([b0, b1, b2]) / a0
    a = np.array([1.0, a1 / a0, a2 / a0])
    return signal.filtfilt(b, a, x)


def repair_john(x: np.ndarray) -> np.ndarray:
    """EQ used only under the John mask.

    Audible curve (filtfilt doubles the designed bell gains), measured on noise:
    steep high-pass through the 80–160 Hz resonance, presence back around
    500–1000 Hz, and a cut above 4 kHz so the makeup gain does not leave him
    brighter than Graham.
    """
    y = signal.sosfiltfilt(signal.butter(8, 185, btype="highpass", fs=SR, output="sos"), x)
    y = bell(y, 155, 0.8, -10)  # audible about -20 dB on the 125–160 Hz peak
    y = bell(y, 750, 0.9, 8)  # audible about +16 dB presence
    y = bell(y, 4200, 0.8, -8)  # audible about -16 dB, tames the lifted hiss
    y = signal.sosfiltfilt(signal.butter(4, 7000, btype="lowpass", fs=SR, output="sos"), y)
    return y


def speech_band(x: np.ndarray) -> np.ndarray:
    sos = signal.butter(4, [500, 1500], btype="band", fs=SR, output="sos")
    return signal.sosfiltfilt(sos, x)


def active_rms(band: np.ndarray, mask: np.ndarray, hop: int = 960) -> float:
    """RMS of 20 ms frames inside mask whose energy is in the top half of that mask."""
    n = len(band) // hop
    if n == 0:
        return 0.0
    frames = band[: n * hop].reshape(n, hop)
    m = mask[: n * hop].reshape(n, hop).mean(axis=1) > 0.6
    if m.sum() < 10:
        return 0.0
    e = np.sqrt(np.mean(frames[m] ** 2, axis=1) + 1e-18)
    thr = np.percentile(e, 50)
    keep = e[e >= thr]
    return float(np.sqrt(np.mean(keep**2)))


def soft_ceiling(x: np.ndarray, ceiling_db: float = -1.0) -> np.ndarray:
    """Smooth ceiling. Leaves everything under the threshold unchanged."""
    ceiling = 10 ** (ceiling_db / 20.0)
    thresh = ceiling * 0.85
    ax = np.abs(x)
    over = ax > thresh
    if not np.any(over):
        return x
    sign = np.sign(x)
    # Compress the overshoot into the remaining headroom.
    norm = np.clip((ax - thresh) / (1.0 - thresh), 0.0, 8.0)
    shaped = thresh + (ceiling - thresh) * np.tanh(norm)
    y = x.copy()
    y[over] = sign[over] * shaped[over]
    return y


def mix(original: np.ndarray, repaired: np.ndarray, mask: np.ndarray) -> tuple[np.ndarray, float]:
    band_o = speech_band(original)
    band_r = speech_band(repaired)
    john_rms = active_rms(band_r, mask)
    graham_rms = active_rms(band_o, 1.0 - mask)
    if john_rms <= 0 or graham_rms <= 0:
        raise RuntimeError(f"could not measure loudness john={john_rms} graham={graham_rms}")
    gain = graham_rms / john_rms
    # Sanity window around the measured ~17 dB. Outside this, the mask is wrong.
    gain_db = 20.0 * np.log10(gain)
    if not 8.0 <= gain_db <= 24.0:
        raise RuntimeError(f"John makeup gain {gain_db:.1f} dB is outside 8–24 dB; mask is suspect")
    lifted = soft_ceiling(repaired * gain, -1.0)
    # Graham and the host stay sample-identical wherever the mask is closed.
    mixed = original * (1.0 - mask) + lifted * mask
    return mixed, gain_db


def region_rms(x: np.ndarray, t0: float, t1: float) -> float:
    a = int(t0 * SR)
    b = int(t1 * SR)
    seg = x[a:b]
    hop = int(0.020 * SR)
    frames = seg[: len(seg) // hop * hop].reshape(-1, hop)
    e = np.sqrt(np.mean(frames**2, axis=1) + 1e-18)
    active = e > np.percentile(e, 55)
    return float(20.0 * np.log10(np.sqrt(np.mean(e[active] ** 2)) + 1e-12))


def build_video(full: Path, work: Path, audio_wav: Path, dest: Path) -> None:
    head = work / "video-head-lossless.mp4"
    tail = work / "video-tail-copy.mp4"
    joined = work / "video-joined.mp4"
    run(
        [
            "ffmpeg", "-y", "-i", str(full),
            "-ss", f"{CUT_S:.3f}", "-to", f"{KEYFRAME_S:.3f}",
            "-an",
            # High-profile 4:2:0 cannot be mathematically lossless. CRF 8 on
            # this already-small screen recording is past visually lossless,
            # and it matches the stream-copied tail so the files concatenate.
            "-c:v", "libx264", "-crf", "8", "-preset", "medium",
            "-pix_fmt", "yuv420p", "-profile:v", "high", "-level:v", "5.0",
            "-colorspace", "bt470bg", "-color_primaries", "bt470bg", "-color_trc", "bt709",
            "-video_track_timescale", "30000",
            str(head),
        ]
    )
    run(
        [
            "ffmpeg", "-y",
            "-ss", f"{KEYFRAME_S:.3f}", "-i", str(full),
            "-an", "-c", "copy",
            str(tail),
        ]
    )
    lst = work / "video-concat.txt"
    lst.write_text(f"file '{head.resolve()}'\nfile '{tail.resolve()}'\n")
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(joined)])
    # AAC at 256 kbps is transparent relative to the repaired PCM. -shortest
    # ends with the video; the source audio was already a fraction longer.
    run(
        [
            "ffmpeg", "-y",
            "-i", str(joined), "-i", str(audio_wav),
            "-map", "0:v:0", "-map", "1:a:0",
            "-c:v", "copy",
            "-c:a", "aac", "-b:a", "256k", "-ar", str(SR), "-ac", "2",
            "-shortest",
            "-movflags", "+faststart",
            str(dest),
        ]
    )


def probe(path: Path) -> dict:
    out = subprocess.check_output(
        [
            "ffprobe", "-v", "error",
            "-show_entries", "format=duration,size:stream=codec_name,width,height,sample_rate,channels,bit_rate,profile",
            "-of", "json", str(path),
        ]
    )
    return json.loads(out)


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--parts", nargs="+", type=Path, help="segment mp4s in order")
    p.add_argument("--input", type=Path, help="already-joined mp4")
    p.add_argument("--work", type=Path, default=Path("/tmp/interview-jg"))
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    if not args.parts and not args.input:
        p.error("pass --parts or --input")
    args.work.mkdir(parents=True, exist_ok=True)
    full = args.work / "interview-full.mp4"
    if args.parts:
        concat_parts(args.parts, full)
    else:
        full = args.input

    print("decoding audio", flush=True)
    audio = read_mono_f64(full)
    duration = len(audio) / SR
    print(f"source audio {duration:.3f}s peak {20*np.log10(np.max(np.abs(audio))+1e-12):.2f} dBFS", flush=True)

    print("finding John's mic", flush=True)
    mask, segs = john_mask(audio)
    covered = float(mask.sum() / SR)
    print(f"John mask {covered:.1f}s across {len(segs)} spans", flush=True)
    for a, b in segs:
        if b > 40 and a < 180 and (b - a) >= 0.4:
            print(f"  {a:7.2f}-{b:7.2f} ({b-a:.1f}s)")

    # Graham's question (about 92–108 s) must stay identical.
    g0, g1 = int(92.0 * SR), int(108.0 * SR)
    leaked = float(mask[g0:g1].mean())
    print(f"mask fraction inside Graham's question 92–108s: {leaked:.4f}")

    print("repairing John", flush=True)
    repaired = repair_john(audio)
    mixed, gain_db = mix(audio, repaired, mask)
    print(f"makeup gain {gain_db:.2f} dB")

    cut = int(round(CUT_S * SR))
    trimmed = mixed[cut:]
    wav_path = args.work / "interview-repaired.wav"
    write_wav(wav_path, trimmed)

    # Level check on the known opening turns, after the mix (still on the
    # untrimmed timeline, which shares samples with the file we export).
    metrics = {
        "cut_seconds": CUT_S,
        "keyframe_join_seconds": KEYFRAME_S,
        "source_duration_seconds": round(duration, 3),
        "john_mask_seconds": round(covered, 2),
        "john_spans": len(segs),
        "makeup_gain_db": round(gain_db, 2),
        "graham_question_mask_fraction": round(leaked, 4),
        "source_peak_dbfs": round(float(20 * np.log10(np.max(np.abs(audio)) + 1e-12)), 2),
        "repaired_peak_dbfs": round(float(20 * np.log10(np.max(np.abs(mixed)) + 1e-12)), 2),
        "clipped_samples": int(np.sum(np.abs(mixed) >= 0.999)),
        "john_hello_rms_db": round(region_rms(mixed, 48.9, 49.8), 2),
        "graham_hello_rms_db": round(region_rms(mixed, 51.15, 52.4), 2),
        "john_answer_rms_db": round(region_rms(mixed, 120.0, 160.0), 2),
        "graham_question_rms_db": round(region_rms(mixed, 94.0, 107.0), 2),
        "graham_question_max_abs_diff": round(float(np.max(np.abs(mixed[g0:g1] - audio[g0:g1]))), 6),
    }
    print(json.dumps(metrics, indent=2))

    print("muxing video", flush=True)
    build_video(full, args.work, wav_path, args.output)
    info = probe(args.output)
    metrics["output"] = info
    (args.work / "metrics.json").write_text(json.dumps(metrics, indent=2))
    print(json.dumps(info, indent=2))


if __name__ == "__main__":
    main()
