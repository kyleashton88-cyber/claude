#!/usr/bin/env python3
"""Audit the eleven Grid Bot Blueprint masters (bp-01 .. bp-11).

Measures container timing, loudness, silence, scene holds, script-vs-picture
sync, burned-in text collisions, truncated captions, and exchange names on
screen. Writes a JSON sidecar next to this file. Elite lessons are not read.
"""

from __future__ import annotations

import json
import re
import subprocess
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MASTERS = ROOT / "course" / "masters"
SCRIPTS = ROOT / "course" / "scripts"
FRAMES = Path("/tmp/bp-audit/frames")
WPM = 143
BRANDS = re.compile(
    r"\b(bybit|binance|pionex|coinbase|okx|okex|kucoin|kraken|bitget|huobi|htx|"
    r"mexc|deribit|blofin|bingx|tradingview|metatrader|bitfinex|lbank|gate\.?io|"
    r"crypto\.com|whitebit|3commas|bitsgap|cryptohopper)\b",
    re.I,
)
DANGLING = re.compile(
    r"\b(a|an|the|of|and|or|to|in|on|for|with|from|that|this|is|are|if|but|then|as|at|by|into)\.?$",
    re.I,
)
POINTING = "The point of the beat is the pointing."


def run(cmd: list[str]) -> str:
    return subprocess.check_output(cmd, stderr=subprocess.STDOUT, text=True, errors="replace")


def beat_frames(beat: dict) -> int:
    words = len((beat.get("vo") or "").split())
    floor = {"intro": 5.5, "outro": 8.0, "legal": 12.0}.get(beat["role"], 6.0)
    secs = max(floor, words / WPM * 60)
    return int(round(secs * 30))


def ffprobe(path: Path) -> dict:
    raw = run([
        "ffprobe", "-v", "error", "-show_entries",
        "format=duration,bit_rate,format_name:stream=index,codec_type,codec_name,width,height,avg_frame_rate,sample_rate,channels,bit_rate,duration,start_time,pix_fmt,color_space,profile",
        "-of", "json", str(path),
    ])
    return json.loads(raw)


def audio_report(path: Path) -> dict:
    log = run([
        "ffmpeg", "-hide_banner", "-i", str(path), "-vn",
        "-af", "silencedetect=noise=-36dB:d=0.45,ebur128=peak=true",
        "-f", "null", "-",
    ])
    silences = []
    starts = [float(x) for x in re.findall(r"silence_start: ([0-9.]+)", log)]
    ends = re.findall(r"silence_end: ([0-9.]+) \| silence_duration: ([0-9.]+)", log)
    for i, (end, dur) in enumerate(ends):
        start = starts[i] if i < len(starts) else float(end) - float(dur)
        silences.append({"start": round(start, 3), "end": round(float(end), 3), "duration": round(float(dur), 3)})
    if len(starts) > len(ends):
        silences.append({"start": round(starts[-1], 3), "end": None, "duration": None, "open": True})

    def grab(label: str) -> str | None:
        m = re.search(rf"{label}:\s+(-?[0-9.]+)", log)
        return m.group(1) if m else None

    vol = run(["ffmpeg", "-hide_banner", "-i", str(path), "-vn", "-af", "volumedetect", "-f", "null", "-"])
    max_vol = re.search(r"max_volume: (-?[0-9.inf]+) dB", vol)
    mean_vol = re.search(r"mean_volume: (-?[0-9.]+) dB", vol)
    return {
        "integrated_lufs": float(grab("I") or "nan"),
        "lra": grab("LRA"),
        "threshold_lufs": grab("Threshold"),
        "true_peak_dbfs": grab("Peak"),
        "max_volume_db": max_vol.group(1) if max_vol else None,
        "mean_volume_db": float(mean_vol.group(1)) if mean_vol else None,
        "silences": silences,
    }


def scene_times(path: Path) -> list[float]:
    log = run([
        "ffmpeg", "-hide_banner", "-i", str(path),
        "-vf", "select='gt(scene,0.12)',showinfo",
        "-fps_mode", "vfr", "-f", "null", "-",
    ])
    return [round(float(x), 3) for x in re.findall(r"pts_time:([0-9.]+)", log)]


def ocr_image(path: Path) -> str:
    try:
        return run(["tesseract", str(path), "stdout", "--psm", "6"]).strip()
    except subprocess.CalledProcessError as exc:
        return exc.output or ""


def file_md5(path: Path) -> str:
    h = hashlib.md5()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def ts(seconds: float) -> str:
    seconds = max(0.0, seconds)
    m, s = divmod(int(round(seconds)), 60)
    h, m = divmod(m, 60)
    if h:
        return f"{h}:{m:02d}:{s:02d}"
    return f"{m}:{s:02d}"


def audit_one(script_path: Path) -> dict:
    script = json.loads(script_path.read_text())
    sid = script["id"]
    master = MASTERS / f"{sid}.mp4"
    probe = ffprobe(master)
    fmt = probe["format"]
    streams = probe["streams"]
    video = next(s for s in streams if s["codec_type"] == "video")
    audio = next(s for s in streams if s["codec_type"] == "audio")
    duration = float(fmt["duration"])
    audio_rep = audio_report(master)
    cuts = scene_times(master)
    boundaries = [0.0] + cuts
    # Drop a cut that is only the last frame jitter.
    if boundaries and duration - boundaries[-1] < 0.2:
        boundaries = boundaries[:-1]

    expected = []
    t = 0.0
    for beat in script["beats"]:
        frames = beat_frames(beat)
        secs = frames / 30
        expected.append({"n": beat["n"], "start": round(t, 3), "duration": round(secs, 3), "frames": frames})
        t += secs
    expected_total = round(t, 3)

    sections = []
    frame_dir = FRAMES / sid
    frame_dir.mkdir(parents=True, exist_ok=True)
    for i, beat in enumerate(script["beats"]):
        start = boundaries[i] if i < len(boundaries) else None
        end = boundaries[i + 1] if i + 1 < len(boundaries) else duration
        if start is None:
            hold = None
            offset = None
        else:
            hold = round(end - start, 3)
            offset = round(start - expected[i]["start"], 3)
        cap = beat["cap"].strip()
        vo = beat["vo"]
        cap_problem = None
        if not cap.endswith((".", "?", "!")) or DANGLING.search(cap):
            cap_problem = "caption is cut mid-sentence"
        elif cap.endswith(".") and not vo.startswith(cap[:-1]) and cap not in vo:
            cap_problem = "caption does not match the spoken line"
        look = re.search(r"look for ([^.]+)", vo)
        sections.append({
            "n": beat["n"],
            "chapter": beat["chapter"],
            "role": beat["role"],
            "start": start,
            "end": round(end, 3) if start is not None else None,
            "hold": hold,
            "script_start": expected[i]["start"],
            "script_duration": expected[i]["duration"],
            "sync_offset": offset,
            "cap": cap,
            "cap_problem": cap_problem,
            "sentences": vo.count(".") + vo.count("?"),
            "pointing_tail": POINTING in vo,
            "look_for": look.group(1).strip() if look else None,
            "image": beat["image"],
        })

    # Sample one frame per section and OCR the title band and the caption band.
    for sec in sections:
        if sec["start"] is None:
            continue
        stamp = sec["start"] + min(0.4, (sec["hold"] or 1) / 2)
        top = frame_dir / f"{sec['n']:02d}-top.png"
        bot = frame_dir / f"{sec['n']:02d}-bot.png"
        run([
            "ffmpeg", "-y", "-v", "error", "-ss", f"{stamp:.3f}", "-i", str(master),
            "-frames:v", "1", "-vf", "crop=960:180:40:40", str(top),
        ])
        run([
            "ffmpeg", "-y", "-v", "error", "-ss", f"{stamp:.3f}", "-i", str(master),
            "-frames:v", "1", "-vf", "crop=1920:200:0:880", str(bot),
        ])
        top_text = ocr_image(top)
        bot_text = ocr_image(bot)
        sec["ocr_top"] = " ".join(top_text.split())
        sec["ocr_caption"] = " ".join(bot_text.split())
        brands = sorted(set(m.group(0) for m in BRANDS.finditer(top_text + "\n" + bot_text)))
        sec["brands_on_frame"] = brands
        # Chapter label sits in the title band when both the chapter and another word are present.
        chapter_hit = beat_chapter_hit(sec["chapter"], top_text)
        sec["chapter_overlaps_title"] = chapter_hit

    image_hashes = {}
    image_ocr = {}
    dupes = []
    for beat in script["beats"]:
        img = ROOT / beat["image"]
        digest = file_md5(img) if img.is_file() else "missing"
        if digest in image_hashes and digest != "missing":
            dupes.append({"n": beat["n"], "same_as": image_hashes[digest], "image": beat["image"]})
        else:
            image_hashes[digest] = beat["n"]
        if img.is_file() and digest not in image_ocr:
            image_ocr[digest] = " ".join(ocr_image(img).split())
        text = image_ocr.get(digest, "")
        brands = sorted(set(m.group(0) for m in BRANDS.finditer(text)))
        for sec in sections:
            if sec["n"] == beat["n"]:
                sec["image_ocr"] = text[:400]
                sec["brands_on_still"] = brands
                sec["image_missing"] = digest == "missing"

    roles = [b["role"] for b in script["beats"]]
    chapters = [b["chapter"].lower() for b in script["beats"]]
    return {
        "id": sid,
        "title": script["title"],
        "next": script.get("next"),
        "music": script.get("music"),
        "duration": round(duration, 3),
        "duration_ts": ts(duration),
        "expected_duration": expected_total,
        "timeline_delta": round(duration - expected_total, 3),
        "video": {
            "codec": video.get("codec_name"),
            "profile": video.get("profile"),
            "width": video.get("width"),
            "height": video.get("height"),
            "fps": video.get("avg_frame_rate"),
            "pix_fmt": video.get("pix_fmt"),
            "color_space": video.get("color_space"),
            "start_time": video.get("start_time"),
            "duration": video.get("duration"),
        },
        "audio": {
            "codec": audio.get("codec_name"),
            "sample_rate": audio.get("sample_rate"),
            "channels": audio.get("channels"),
            "bit_rate": audio.get("bit_rate"),
            "start_time": audio.get("start_time"),
            "duration": audio.get("duration"),
            **{k: audio_rep[k] for k in ("integrated_lufs", "lra", "threshold_lufs", "true_peak_dbfs", "max_volume_db", "mean_volume_db")},
        },
        "silences": audio_rep["silences"],
        "cuts": cuts,
        "section_count": len(sections),
        "cut_count": len(cuts),
        "roles": roles,
        "has_hook": "hook" in roles,
        "has_intro_role": "intro" in roles,
        "has_outro_role": "outro" in roles,
        "has_recap_role": "recap" in roles,
        "has_objective_chapter": any("objective" in c or "you will be able" in c or "by the end" in c for c in chapters),
        "duplicate_stills": dupes,
        "sections": sections,
    }


def beat_chapter_hit(chapter: str, ocr: str) -> bool:
    """True when the burned-in chapter word is in the title band.

    The title band should be the illustration. A chapter label there means the
    lower third was drawn on top of the artwork.
    """
    token = chapter.split()[0]
    if len(token) < 3:
        token = chapter
    return token.lower() in ocr.lower()


def main() -> None:
    out = []
    for path in sorted(SCRIPTS.glob("bp-*.json")):
        print(f"AUDIT {path.stem}", flush=True)
        out.append(audit_one(path))
    dest = Path(__file__).resolve().parent / "audit-data.json"
    dest.write_text(json.dumps(out, indent=2))
    print(f"wrote {dest}")


if __name__ == "__main__":
    main()
