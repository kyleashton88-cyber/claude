"""Caption files. words.json is the schema the rest of the pipeline reads."""

from __future__ import annotations

import json
from pathlib import Path

from voice.align import Word

SCHEMA = "video-production.words.v1"


def words_payload(words: list[Word], *, engine: str, mood: str, method: str) -> dict:
    return {
        "schema": SCHEMA,
        "engine": engine,
        "mood": mood,
        "method": method,
        "words": [word.as_dict() for word in words],
    }


def write_words(path: Path, words: list[Word], *, engine: str, mood: str, method: str) -> None:
    path.write_text(json.dumps(words_payload(words, engine=engine, mood=mood, method=method), indent=2) + "\n")


def _stamp(seconds: float, srt: bool = False) -> str:
    ms = max(0, int(round(seconds * 1000)))
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    sep = "," if srt else "."
    return f"{h:02d}:{m:02d}:{s:02d}{sep}{ms:03d}"


def cues(words: list[Word], max_words: int = 8, max_chars: int = 42) -> list[list[Word]]:
    groups: list[list[Word]] = []
    current: list[Word] = []
    for word in words:
        trial = current + [word]
        text = " ".join(item.text for item in trial)
        if current and (len(trial) > max_words or len(text) > max_chars):
            groups.append(current)
            current = [word]
        else:
            current = trial
    if current:
        groups.append(current)
    return groups


def _cue_end(cue: list[Word], following: float | None) -> float:
    """Give a readable hold when alignment crushed several words into a few frames."""
    start = cue[0].start
    end = cue[-1].end
    text = " ".join(word.text for word in cue)
    need = max(0.8, len(text) / 17.0)
    if end - start < need:
        end = start + need
    if following is not None:
        end = min(end, following)
    return max(end, start + 0.2)


def write_vtt(path: Path, words: list[Word]) -> None:
    lines = ["WEBVTT", ""]
    grouped = cues(words)
    for index, cue in enumerate(grouped):
        following = grouped[index + 1][0].start if index + 1 < len(grouped) else None
        lines.append(f"{_stamp(cue[0].start)} --> {_stamp(_cue_end(cue, following))}")
        lines.append(" ".join(word.text for word in cue))
        lines.append("")
    path.write_text("\n".join(lines))


def write_srt(path: Path, words: list[Word]) -> None:
    lines = []
    grouped = cues(words)
    for index, cue in enumerate(grouped, start=1):
        following = grouped[index][0].start if index < len(grouped) else None
        lines.append(str(index))
        lines.append(f"{_stamp(cue[0].start, srt=True)} --> {_stamp(_cue_end(cue, following), srt=True)}")
        lines.append(" ".join(word.text for word in cue))
        lines.append("")
    path.write_text("\n".join(lines))


def write_chapters(path: Path, sections: list[tuple[float, str]]) -> None:
    """YouTube chapter file. The first mark is always 0:00."""
    lines = []
    for start, title in sections:
        whole = int(start)
        h, rem = divmod(whole, 3600)
        m, s = divmod(rem, 60)
        stamp = f"{h:02d}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"
        lines.append(f"{stamp} {title}")
    path.write_text("\n".join(lines) + "\n")


def caption_box(frame_w: int = 1920, frame_h: int = 1080, font_px: int = 42, lines: int = 2) -> dict:
    """Where a burned caption sits. The box must stay inside a 5% margin."""
    margin_x = int(round(frame_w * 0.05))
    margin_y = int(round(frame_h * 0.05))
    box_h = font_px * lines + 28
    top = frame_h - margin_y - box_h
    return {
        "x": margin_x,
        "y": top,
        "w": frame_w - 2 * margin_x,
        "h": box_h,
        "margin_x": margin_x,
        "margin_y": margin_y,
    }


def margin_ok(box: dict, frame_w: int = 1920, frame_h: int = 1080) -> bool:
    return (
        box["x"] >= int(frame_w * 0.05) - 1
        and box["y"] >= int(frame_h * 0.05) - 1
        and box["x"] + box["w"] <= frame_w - int(frame_w * 0.05) + 1
        and box["y"] + box["h"] <= frame_h - int(frame_h * 0.05) + 1
    )
