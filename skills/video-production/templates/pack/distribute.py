"""Thumbnails, shorts, chapters, and the end card."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

import yaml

VP = Path(__file__).resolve().parents[2]
if str(VP) not in sys.path:
    sys.path.insert(0, str(VP))

from lib.ffmpeg_util import ffmpeg_bin, probe  # noqa: E402

from .engine import render_cover
from .paint import paint_endcard, paint_thumbnail

MAX_SHORT = 59.0


def make_thumbnail(title: str, label: str, dest: Path, engine: str = "auto") -> dict:
    if engine not in {"auto", "pil", "illustration"}:
        raise ValueError(f"unknown thumbnail engine {engine}")
    if engine in {"auto", "illustration"} and render_cover(title, label, dest):
        return {"renderer": "illustration-engine", "path": str(dest), "width": 1280, "height": 720}
    if engine == "illustration":
        raise RuntimeError("illustration engine is not installed, and this call asked for it")
    paint_thumbnail(title, label, dest)
    return {"renderer": "pil-fallback", "path": str(dest), "width": 1280, "height": 720}


def parse_chapters(text: str) -> list[dict]:
    rows = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        match = re.match(r"(?:(\d+):)?(\d+):(\d{2})\s+(.+)", stripped)
        if not match:
            continue
        hours = int(match.group(1) or 0)
        minutes = int(match.group(2))
        seconds = int(match.group(3))
        rows.append({"t": hours * 3600 + minutes * 60 + seconds, "title": match.group(4).strip()})
    if not rows:
        raise ValueError("no chapter markers")
    return rows


def chapter_windows(chapters: list[dict], duration: float) -> list[dict]:
    rows = []
    for index, chapter in enumerate(chapters):
        end = chapters[index + 1]["t"] if index + 1 < len(chapters) else duration
        rows.append({**chapter, "end": end, "duration": max(0.0, end - chapter["t"])})
    return rows


def pick_window(windows: list[dict], name: str | None) -> dict:
    if name:
        for window in windows:
            if window["title"].lower() == name.lower():
                return window
        raise ValueError(f"no chapter named {name!r}")
    fitting = [window for window in windows if 0 < window["duration"] <= MAX_SHORT]
    if fitting:
        return fitting[0]
    return windows[0]


def shift_vtt(text: str, start: float, end: float) -> str:
    stamp = re.compile(r"(\d+):(\d{2}):(\d{2})[.,](\d{1,3})")

    def seconds(token: str) -> float:
        match = stamp.search(token)
        if not match:
            raise ValueError(token)
        frac = match.group(4).ljust(3, "0")
        return int(match.group(1)) * 3600 + int(match.group(2)) * 60 + int(match.group(3)) + int(frac) / 1000

    def fmt(value: float) -> str:
        value = max(0.0, value)
        ms = int(round(value * 1000))
        hours, ms = divmod(ms, 3_600_000)
        minutes, ms = divmod(ms, 60_000)
        secs, ms = divmod(ms, 1000)
        return f"{hours:02d}:{minutes:02d}:{secs:02d}.{ms:03d}"

    blocks = re.split(r"\n\s*\n", text.replace("\r\n", "\n").strip())
    kept = ["WEBVTT", ""]
    for block in blocks:
        lines = [line for line in block.split("\n") if line.strip()]
        if not lines or "-->" not in lines[0]:
            continue
        left, right = lines[0].split("-->", 1)
        cue_start, cue_end = seconds(left), seconds(right.split()[0])
        if cue_end <= start or cue_start >= end:
            continue
        new_start = max(cue_start, start) - start
        new_end = min(cue_end, end) - start
        if new_end - new_start < 0.4:
            continue
        payload = "\n".join(lines[1:])
        kept.append(f"{fmt(new_start)} --> {fmt(new_end)}\n{payload}\n")
    return "\n".join(kept).rstrip() + "\n"


def cut_short(
    master: Path,
    chapters: Path,
    dest: Path,
    *,
    vtt: Path | None = None,
    chapter: str | None = None,
) -> dict:
    info = probe(master)
    duration = float((info.get("format") or {}).get("duration") or 0)
    windows = chapter_windows(parse_chapters(chapters.read_text(encoding="utf-8")), duration)
    window = pick_window(windows, chapter)
    length = min(MAX_SHORT, window["duration"])
    trimmed = window["duration"] > MAX_SHORT
    dest.parent.mkdir(parents=True, exist_ok=True)
    vtt_path = dest.with_suffix(".vtt")
    if vtt is not None:
        shifted = shift_vtt(vtt.read_text(encoding="utf-8"), window["t"], window["t"] + length)
        vtt_path.write_text(shifted, encoding="utf-8")
    crop = "crop=w='min(iw\\,ih*9/16)':h='min(ih\\,iw*16/9)':x='(iw-ow)/2':y='(ih-oh)/2',scale=1080:1920:flags=lanczos"
    if vtt is not None:
        escaped = str(vtt_path).replace("\\", "\\\\").replace(":", "\\:").replace("'", "\\'")
        crop = crop + f",subtitles='{escaped}'"
    cmd = [
        ffmpeg_bin(),
        "-y",
        "-hide_banner",
        "-loglevel",
        "error",
        "-ss",
        f"{window['t']:.3f}",
        "-t",
        f"{length:.3f}",
        "-i",
        str(master),
        "-vf",
        crop,
        "-c:v",
        "libx264",
        "-preset",
        "veryfast",
        "-crf",
        "28",
        "-pix_fmt",
        "yuv420p",
        "-c:a",
        "aac",
        "-b:a",
        "160k",
        "-movflags",
        "+faststart",
        str(dest),
    ]
    subprocess.check_call(cmd)
    return {
        "path": str(dest),
        "chapter": window["title"],
        "start": window["t"],
        "duration": length,
        "trimmed_to_fit": trimmed,
        "captions": str(vtt_path) if vtt is not None else None,
        "frame": "1080x1920",
        "publishes": False,
    }


def youtube_stamp(seconds: float) -> str:
    whole = int(seconds)
    hours, rem = divmod(whole, 3600)
    minutes, secs = divmod(rem, 60)
    if hours:
        return f"{hours}:{minutes:02d}:{secs:02d}"
    return f"{minutes}:{secs:02d}"


def load_lesson(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".json":
        return json.loads(text)
    return yaml.safe_load(text) or {}


def chapter_lines(lesson: dict) -> list[str]:
    chapters = list(lesson.get("chapters") or [])
    if not chapters:
        clock = 0.0
        for beat in lesson.get("beats") or []:
            chapters.append({"t": clock, "title": beat.get("chapter") or beat.get("id") or "Section"})
            words = beat.get("words") or []
            if words:
                clock = float(words[-1].get("end", clock))
            else:
                clock += max(1.0, len(str(beat.get("vo") or "").split()) / 2.4)
    if not chapters or float(chapters[0].get("t", 0)) != 0:
        chapters = [{"t": 0, "title": chapters[0]["title"] if chapters else "Start"}] + [
            row for row in chapters if float(row.get("t", 0)) != 0
        ]
    lines = []
    seen = set()
    for chapter in chapters:
        title = str(chapter.get("title") or "Section")
        if title in seen:
            continue
        seen.add(title)
        lines.append(f"{youtube_stamp(float(chapter.get('t', 0)))} {title}")
    return lines


def write_description(lesson: dict, dest: Path) -> Path:
    title = lesson.get("title") or lesson.get("lesson") or "Lesson"
    chapters = "\n".join(chapter_lines(lesson))
    next_title = (lesson.get("next") or {}).get("title")
    next_line = f"Next lesson: {next_title}." if next_title else ""
    body = (
        f"{title}\n\n"
        "This is education, not financial advice. It is general information. "
        "It does not consider your objectives, financial situation, or needs. "
        "Figures marked EXAMPLE are illustrations, not a forecast.\n\n"
        "Chapters\n"
        f"{chapters}\n\n"
        f"{next_line}\n"
        "The end card leaves the right side clear for the end screen.\n"
    )
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(body, encoding="utf-8")
    return dest
