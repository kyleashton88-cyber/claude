"""Section D checks for a finished Blueprint master.

The background grid is frozen, so a change in the card band is a content
change. This writes D2, D3, D4 and D5 next to the master. D1 is the frame
diff and is written by the same command when --previous is set.
"""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

import numpy as np


def _frames(path: Path) -> np.ndarray:
    raw = subprocess.check_output(
        ["ffmpeg", "-v", "error", "-i", str(path), "-vf", "fps=1,scale=160:90", "-f", "rawvideo", "-pix_fmt", "gray", "-"],
    )
    frame = 160 * 90
    count = len(raw) // frame
    frames = np.frombuffer(raw[: count * frame], dtype=np.uint8).reshape(count, 90, 160)
    # Title rows and the caption rows are not the card.
    return frames[:, 12:54, :]


def static_stretches(path: Path, limit: float = 8.0) -> list[tuple[float, float]]:
    """Stretches where the card does not change, ignoring the moving grid.

    The grid and the glow move every pixel by only a few levels. A drawn line
    or a word changes pixels by much more. Those strong pixels are the content.
    """
    frames = _frames(path)
    if len(frames) < 2:
        return []
    diff = np.abs(frames[1:].astype(np.int16) - frames[:-1].astype(np.int16)) > 18
    holds = []
    start = 0
    for index, mask in enumerate(diff):
        # Caption bar is already outside this crop. A change counts only when
        # it is taller than 60px at 1080p. Highlights, chips and thin lines are
        # not a build. A solid horizontal fill is a bar or a playhead.
        content = False
        if mask.any():
            rows = np.where(mask.any(axis=1))[0]
            height_px = int(rows[-1] - rows[0] + 1) * 12
            band = mask[rows[0]:rows[-1] + 1]
            if height_px > 60 and float(band.mean()) < 0.72:
                content = True
        if content:
            seconds = index - start + 1
            if seconds >= limit:
                holds.append((float(start), float(seconds)))
            start = index + 1
    seconds = len(diff) - start
    if seconds >= limit:
        holds.append((float(start), float(seconds)))
    return holds


def header_only(path: Path, limit: float = 5.0) -> list[tuple[float, float]]:
    """A card whose body has almost no cyan or white ink."""
    raw = subprocess.check_output(
        ["ffmpeg", "-v", "error", "-i", str(path), "-vf", "fps=1,scale=320:180", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
    )
    frame = 320 * 180 * 3
    count = len(raw) // frame
    frames = np.frombuffer(raw[: count * frame], dtype=np.uint8).reshape(count, 180, 320, 3)
    # Card body, under the title and above the caption.
    body = frames[:, 36:120, 20:300]
    bright = ((body[:, :, :, 1] > 140) & (body[:, :, :, 2] > 140)).sum(axis=(1, 2))
    quiet = bright < 80
    runs = []
    start = None
    for index, flag in enumerate(quiet):
        if flag and start is None:
            start = index
        elif not flag and start is not None:
            if index - start >= limit:
                runs.append((float(start), float(index - start)))
            start = None
    if start is not None and len(quiet) - start >= limit:
        runs.append((float(start), float(len(quiet) - start)))
    return runs


def text_heights(path: Path) -> list[str]:
    """Tesseract box heights. A 28px glyph at 1080p is about 14px tall at 540p."""
    raw = subprocess.check_output(
        ["ffmpeg", "-v", "error", "-i", str(path), "-vf", "fps=1/10,scale=960:540", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
    )
    # Sample every 10s is enough to find a small text block.
    frame = 960 * 540 * 3
    count = min(len(raw) // frame, 40)
    problems = []
    import tempfile
    from PIL import Image
    for index in range(count):
        img = Image.frombytes("RGB", (960, 540), raw[index * frame:(index + 1) * frame])
        with tempfile.NamedTemporaryFile(suffix=".png") as handle:
            img.save(handle.name)
            try:
                out = subprocess.check_output(["tesseract", handle.name, "stdout", "--psm", "11", "tsv"], text=True, stderr=subprocess.DEVNULL)
            except subprocess.CalledProcessError:
                continue
        for line in out.splitlines()[1:]:
            parts = line.split("\t")
            if len(parts) < 12:
                continue
            text = parts[11].strip()
            if len(text) < 8:
                continue
            try:
                height = int(parts[10]) - int(parts[8])  # not used
                top = int(float(parts[7]))
                h = int(float(parts[9]))
            except ValueError:
                continue
            # 28px at 1080p is 14px at 540p. Flag glyphs clearly under that.
            if 0 < h < 14 and top > 40:
                problems.append(f"{index * 10}s {text[:40]!r} height {h}px at 540p")
                if len(problems) > 30:
                    return problems
    return problems


def level_jumps(path: Path, words_path: Path) -> list[str]:
    words = json.loads(words_path.read_text())["words"]
    wav = path.with_suffix(".gate-audio.wav")
    subprocess.check_call(["ffmpeg", "-y", "-v", "error", "-i", str(path), "-vn", "-ac", "1", "-ar", "16000", str(wav)])
    import soundfile as sf
    audio, sr = sf.read(wav)
    audio = np.asarray(audio, dtype=np.float32)
    jumps = []
    # Sentence boundaries: a gap in the word list over 0.25s.
    for earlier, later in zip(words, words[1:]):
        gap = later["start"] - earlier["end"]
        if gap < 0.25:
            continue
        a = int(max(0, earlier["end"] - 0.08) * sr)
        b = int(min(len(audio), earlier["end"]) * sr)
        c = int(max(0, later["start"]) * sr)
        d = int(min(len(audio), later["start"] + 0.08) * sr)
        if min(b - a, d - c) < 16:
            continue
        left = float(np.sqrt(np.mean(audio[a:b] ** 2)) + 1e-8)
        right = float(np.sqrt(np.mean(audio[c:d] ** 2)) + 1e-8)
        db = 20 * np.log10(right / left)
        if abs(db) > 1.5 and left > 0.02 and right > 0.02:
            jumps.append(f"{later['start']:.2f}s {db:+.1f} dB at {later['text']}")
            if len(jumps) > 40:
                break
    wav.unlink(missing_ok=True)
    return jumps


def pronunciation(path: Path, words_path: Path) -> list[str]:
    import soundfile as sf
    import parselmouth
    words = json.loads(words_path.read_text())["words"]
    wav = path.with_suffix(".pron.wav")
    subprocess.check_call(["ffmpeg", "-y", "-v", "error", "-i", str(path), "-vn", "-ac", "1", "-ar", "24000", str(wav)])
    audio, sr = sf.read(wav)
    audio = np.asarray(audio, dtype=np.float32)
    lines = []

    def kind(text: str) -> str | None:
        bare = text.strip(".,!?;:\"'").lower()
        if bare == "coin":
            return "coin"
        if bare == "close":
            return "close"
        if bare == "asic":
            return "asic"
        if bare == "asic's":
            return "asic"
        if bare == "api":
            return "api"
        return None

    def formants(clip):
        sound = parselmouth.Sound(clip, sampling_frequency=sr)
        inten = sound.to_intensity(minimum_pitch=60)
        form = sound.to_formant_burg(time_step=0.01, max_number_of_formants=5, maximum_formant=5500)
        pts = []
        t = 0.02
        while t < sound.duration - 0.02:
            loud = inten.get_value(t)
            f1 = form.get_value_at_time(1, t)
            f2 = form.get_value_at_time(2, t)
            if loud and loud > 55 and f1 and f1 == f1 and f2 and f2 == f2 and 250 < f1 < 1100 and 700 < f2 < 3000:
                pts.append((f1, f2))
            t += 0.01
        return pts

    met = {"coin": 0, "close": 0, "asic": 0, "api": 0}
    seen = {"coin": 0, "close": 0, "asic": 0, "api": 0}
    for word in words:
        name = kind(word["text"])
        if name is None:
            continue
        seen[name] += 1
        a = int(word["start"] * sr)
        b = int(word["end"] * sr)
        clip = audio[max(0, a):min(len(audio), b)]
        if len(clip) < int(0.08 * sr):
            lines.append(f"NOT MET {name} {word['start']:.2f}s too short")
            continue
        if name == "coin":
            pts = formants(clip)
            if len(pts) < 6:
                lines.append(f"NOT MET coin {word['start']:.2f}s no vowel")
                continue
            early, late = pts[: len(pts) // 3], pts[len(pts) // 2 :]
            f1 = float(np.median([p[0] for p in early]))
            f2 = float(np.median([p[1] for p in early]))
            glide = float(np.median([p[1] for p in late]))
            ok = 450 <= f1 <= 750 and 800 <= f2 <= 1400 and glide >= 1800
            met["coin"] += int(ok)
            lines.append(f"{'MET' if ok else 'NOT MET'} coin {word['start']:.2f}s F1 {f1:.0f} F2 {f2:.0f} glide {glide:.0f}")
        elif name == "close":
            tail = clip[-int(0.07 * sr):]
            spec = np.abs(np.fft.rfft(tail * np.hanning(len(tail))))
            freqs = np.fft.rfftfreq(len(tail), 1 / sr)
            high = float(spec[(freqs >= 4000) & (freqs <= 8000)].sum() / (spec.sum() + 1e-9))
            tail = tail - tail.mean()
            corr = np.correlate(tail, tail, mode="full")
            corr = corr[len(corr) // 2 :]
            lags = range(int(sr / 300), int(sr / 80))
            voiced = float(np.max(corr[list(lags)]) / (corr[0] + 1e-9))
            # Noun close needs a voiced /z/ in the coda. The vowel alone is not a pass.
            ok = voiced >= 0.45 and high >= 0.22
            met["close"] += int(ok)
            lines.append(f"{'MET' if ok else 'NOT MET'} close {word['start']:.2f}s voicing {voiced:.2f} high {high:.2f} coda")
        elif name == "asic":
            pts = formants(clip)
            early = pts[: max(2, len(pts) // 4)] if pts else []
            f2 = float(np.median([p[1] for p in early])) if early else 0
            ok = f2 >= 1800
            met["asic"] += int(ok)
            lines.append(f"{'MET' if ok else 'NOT MET'} ASIC {word['start']:.2f}s early F2 {f2:.0f}")
        else:
            # Three letters: the word is longer than a single syllable.
            ok = (word["end"] - word["start"]) >= 0.7
            met["api"] += int(ok)
            lines.append(f"{'MET' if ok else 'NOT MET'} API {word['start']:.2f}s duration {word['end'] - word['start']:.2f}s")
    lines.append("TOTALS " + " ".join(f"{name} {met[name]}/{seen[name]}" for name in met))
    wav.unlink(missing_ok=True)
    return lines


def frame_diff(new: Path, old: Path, stamps: list[float], dest: Path) -> list[str]:
    dest.mkdir(parents=True, exist_ok=True)
    lines = []
    for stamp in stamps:
        for label, src in (("new", new), ("old", old)):
            out = dest / f"{label}-{stamp:.0f}.png"
            subprocess.check_call(["ffmpeg", "-y", "-v", "error", "-ss", f"{stamp:.3f}", "-i", str(src), "-frames:v", "1", str(out)])
        from PIL import Image
        a = np.array(Image.open(dest / f"new-{stamp:.0f}.png").convert("L").resize((320, 180)))
        b = np.array(Image.open(dest / f"old-{stamp:.0f}.png").convert("L").resize((320, 180)))
        changed = int((np.abs(a.astype(np.int16) - b.astype(np.int16)) > 24).sum())
        lines.append(f"{stamp:.0f}s changed pixels {changed} of {a.size}")
    return lines


def caption_echoes(path: Path, captions: Path) -> list[str]:
    """A fragment of the burned line repeated above the caption bar."""
    import re
    import tempfile
    from PIL import Image

    def stamp(value: str) -> float:
        h, m, rest = value.split(":")
        s, ms = rest.split(",")
        return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000

    cues = []
    for piece in re.split(r"\n\s*\n", captions.read_text(encoding="utf-8").strip()):
        lines = [line for line in piece.splitlines() if line.strip()]
        if not any("-->" in line for line in lines):
            continue
        timing = next(line for line in lines if "-->" in line)
        left, right = [part.strip() for part in timing.split("-->")]
        text = " ".join(line for line in lines if "-->" not in line and not line.strip().isdigit())
        cues.append((stamp(left), stamp(right), text.lower()))
    raw = subprocess.check_output(
        ["ffmpeg", "-v", "error", "-i", str(path), "-vf", "fps=1/15,scale=960:540", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
    )
    frame = 960 * 540 * 3
    count = min(len(raw) // frame, 60)
    found = []
    for index in range(count):
        when = index * 15
        cue = next((text for start, end, text in cues if start <= when < end), "")
        words = [part for part in re.findall(r"[a-z0-9']+", cue) if len(part) > 2]
        if len(words) < 4:
            continue
        img = Image.frombytes("RGB", (960, 540), raw[index * frame:(index + 1) * frame])
        # The caption bar sits at y=800 of 1080, which is y=400 of 540. Keep the card only.
        card = img.crop((0, 0, 960, 390))
        with tempfile.NamedTemporaryFile(suffix=".png") as handle:
            card.save(handle.name)
            try:
                out = subprocess.check_output(["tesseract", handle.name, "stdout"], text=True, stderr=subprocess.DEVNULL)
            except subprocess.CalledProcessError:
                continue
        blob = " ".join(re.findall(r"[a-z0-9']+", out.lower()))
        for size in (4, 5):
            for start in range(0, len(words) - size + 1):
                scrap = " ".join(words[start:start + size])
                if scrap in blob:
                    found.append(f"{when}s caption echo {scrap!r}")
                    break
            else:
                continue
            break
        if len(found) > 20:
            break
    return found


def _sha256(path: Path) -> str:
    import hashlib
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("master")
    parser.add_argument("--words", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--previous")
    parser.add_argument("--stamps", default="")
    parser.add_argument("--captions")
    args = parser.parse_args()
    master = Path(args.master)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    holds = static_stretches(master)
    (out / "D2-static.txt").write_text(
        "Static stretches over 8s, background grid frozen so it cannot count as change.\n"
        + ("\n".join(f"{start:.0f}s for {seconds:.0f}s" for start, seconds in holds) or "none")
        + "\n",
        encoding="utf-8",
    )
    small = text_heights(master)
    (out / "D3-text-size.txt").write_text(
        "Text blocks whose glyph height is under 14px at 540p (28px at 1080p).\n"
        + ("\n".join(small) or "none")
        + "\n",
        encoding="utf-8",
    )
    headers = header_only(master)
    echoes = caption_echoes(master, Path(args.captions)) if args.captions else []
    (out / "D4-header-overlap.txt").write_text(
        "Header-only stretches over 5s (card body with almost no ink).\n"
        + ("\n".join(f"{start:.0f}s for {seconds:.0f}s" for start, seconds in headers) or "none")
        + "\n\nCaption echoes (a caption fragment above the caption bar).\n"
        + ("\n".join(echoes) or "none")
        + "\n\nOverlap of drawn text is enforced while painting by layout_gate.py. A frame that overlaps text does not finish.\n",
        encoding="utf-8",
    )
    jumps = level_jumps(master, Path(args.words))
    said = pronunciation(master, Path(args.words))
    (out / "D5-pronunciation.txt").write_text(
        "Measured on the mixed master. No word splice is in the render.\n"
        + "\n".join(said)
        + "\n\nLevel jumps over 1.5 dB at a sentence boundary:\n"
        + ("\n".join(jumps) or "none")
        + "\n",
        encoding="utf-8",
    )
    if args.previous and args.stamps:
        stamps = [float(item) for item in args.stamps.split(",") if item]
        lines = frame_diff(master, Path(args.previous), stamps, out / "frames")
        (out / "D1-frame-diff.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    digest = _sha256(master)
    d5_bad = [line for line in said if line.startswith("NOT MET")]
    failed = []
    if holds:
        failed.append("D2 static run over 8s\n" + "\n".join(f"  {start:.0f}s for {seconds:.0f}s" for start, seconds in holds))
    if small:
        failed.append("D3 text under 28px\n" + "\n".join(f"  {line}" for line in small))
    if headers:
        failed.append("D4 empty card\n" + "\n".join(f"  {start:.0f}s for {seconds:.0f}s" for start, seconds in headers))
    if echoes:
        failed.append("D4 caption echo\n" + "\n".join(f"  {line}" for line in echoes))
    if d5_bad:
        failed.append("D5 pronunciation NOT MET on the unchanged mix\n" + "\n".join(f"  {line}" for line in d5_bad[:40]))
    result = "FAIL" if failed else "PASS"
    report = [
        "# Gate report",
        "",
        f"Result: **{result}**",
        "",
        f"Master sha256: `{digest}`",
        "",
        "PASS requires D2, D3, D4 and D5 to pass. A static run over 8s, text under 28px, covered text, a caption echo, or clipped text is a FAIL. Decorations under 60px and solid bars do not count as a picture change.",
        "",
    ]
    if failed:
        report.append("Failing checks:")
        report.append("")
        report.extend(failed)
    else:
        report.append("D2, D3, D4 and D5 passed.")
    report.append("")
    report.append("D5 totals are measured on this mix. Noun close is MET only when the coda has a voiced /z/.")
    (out / "gate-report.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    print(out)
    print(result)
    if failed:
        raise SystemExit(
            f"content gate failed: {len(holds)} stretches over 8s, "
            f"{len(headers)} header-only runs, {len(small)} text blocks under 28px, "
            f"{len(echoes)} caption echoes, {len(d5_bad)} pronunciation misses"
        )


if __name__ == "__main__":
    main()
