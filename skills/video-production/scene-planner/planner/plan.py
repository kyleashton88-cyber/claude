"""Turn a lesson script or lesson.yaml into a shot list."""

from __future__ import annotations

import json
import re
from pathlib import Path

import yaml

MAX_SHOT = 8.0
WORDS_PER_SECOND = 2.4

# Illustration-engine types, plus motion treatments when the plate is not a still.
VISUALS = (
    (r"liquidat", "liquidation warning", "liquidation"),
    (r"\bcandle", "candle chart", "candle_series"),
    (r"grid|ladder|\borders\b", "grid ladder", "grid_ladder"),
    (r"mascot|robot|visor", "mascot scene", "mascot_scene"),
    (r"\b(title|cover|brand|intro)\b", "branded scene", "title_card"),
    (r"analogy|fence|beginner|bucket|diagram", "beginner diagram", "analogy_fence"),
)
MOTION = ("motion graphic", "lower third", "kinetic type")


def load_beats(path: Path) -> tuple[dict, list[dict]]:
    raw = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".json":
        data = json.loads(raw)
    else:
        data = yaml.safe_load(raw) or {}
    if data.get("beats"):
        beats = data["beats"]
    elif data.get("scenes"):
        beats = [
            {
                "id": item.get("id") or f"s{index}",
                "chapter": item.get("chapter") or item.get("type") or "",
                "vo": item.get("vo") or "",
                "on_screen": item.get("on_screen") or item.get("cap") or item.get("caption") or "",
                "labels": item.get("labels"),
                "words": item.get("words"),
            }
            for index, item in enumerate(data["scenes"], start=1)
        ]
    elif data.get("shots"):
        beats = [
            {
                "id": item.get("id") or f"s{index}",
                "chapter": item.get("title") or item.get("kind") or "",
                "vo": item.get("vo") or "",
                "on_screen": item.get("caption") or item.get("on_screen") or "",
                "labels": item.get("labels"),
                "words": item.get("words"),
            }
            for index, item in enumerate(data["shots"], start=1)
        ]
    else:
        raise ValueError(f"no beats, scenes, or shots in {path}")
    return data, beats


def choose_visual(text: str, index: int) -> tuple[str, str | None]:
    for pattern, visual, engine in VISUALS:
        if re.search(pattern, text, re.I):
            return visual, engine
    return MOTION[index % len(MOTION)], None


def _clean_label(text: str) -> str:
    words = re.findall(r"[A-Za-z0-9']+", text)
    return " ".join(words[:3])


def labels_for(beat: dict, idea: str) -> list[str]:
    raw = beat.get("labels")
    if raw:
        labels = [_clean_label(str(item)) for item in raw]
    else:
        source = beat.get("on_screen") or idea
        chunks = re.split(r"[,.|/]| and ", source)
        labels = [_clean_label(chunk) for chunk in chunks]
    labels = [item for item in labels if item]
    if not labels:
        labels = [_clean_label(idea) or "One idea"]
    return labels[:4]


def idea_for(beat: dict) -> str:
    source = (beat.get("on_screen") or beat.get("vo") or beat.get("chapter") or "One idea").strip()
    sentence = re.split(r"[.?!]", source)[0].strip()
    words = sentence.split()
    return " ".join(words[:12])


def _segments(beat: dict) -> list[dict]:
    """Time slices of at most 8 seconds. Word timings win over a word-count estimate."""
    words = beat.get("words") or []
    if words:
        groups: list[list[dict]] = []
        bucket: list[dict] = []
        start = float(words[0].get("start", 0))
        for word in words:
            end = float(word.get("end", word.get("start", start)))
            if bucket and end - start > MAX_SHOT:
                groups.append(bucket)
                bucket = [word]
                start = float(word.get("start", end))
            else:
                bucket.append(word)
        if bucket:
            groups.append(bucket)
        slices = []
        for group in groups:
            begin = float(group[0].get("start", 0))
            finish = float(group[-1].get("end", begin))
            text = " ".join(str(word.get("text", "")) for word in group)
            slices.append({"start": begin, "end": max(finish, begin), "text": text})
        return slices
    vo = (beat.get("vo") or "").strip()
    tokens = vo.split() or ["Picture"]
    chunk = max(1, int(MAX_SHOT * WORDS_PER_SECOND))
    slices = []
    cursor = 0.0
    for offset in range(0, len(tokens), chunk):
        piece = tokens[offset:offset + chunk]
        duration = min(MAX_SHOT, max(1.0, len(piece) / WORDS_PER_SECOND))
        slices.append({"start": cursor, "end": cursor + duration, "text": " ".join(piece)})
        cursor += duration
    return slices


def alt_text(visual: str, idea: str, labels: list[str]) -> str:
    label_text = ", ".join(labels)
    return f"{visual[0].upper() + visual[1:]} of {idea}. Labels read: {label_text}."


def plan(data: dict, beats: list[dict]) -> dict:
    shots = []
    for beat_index, beat in enumerate(beats):
        idea = idea_for(beat)
        base_text = " ".join(
            [
                str(beat.get("chapter") or ""),
                str(beat.get("vo") or ""),
                str(beat.get("on_screen") or ""),
                idea,
            ]
        )
        visual, engine = choose_visual(base_text, beat_index)
        for slice_index, piece in enumerate(_segments(beat)):
            duration = round(piece["end"] - piece["start"], 3)
            if duration > MAX_SHOT + 0.05:
                raise RuntimeError(f"shot longer than {MAX_SHOT}s: {duration}")
            if slice_index == 0:
                shot_visual, shot_engine = visual, engine
            else:
                shot_visual, shot_engine = MOTION[(beat_index + slice_index) % len(MOTION)], None
            labels = labels_for(beat, idea)
            shot = {
                "id": f"{beat.get('id') or beat_index + 1}-{slice_index + 1}",
                "beat": beat.get("id") or str(beat_index + 1),
                "chapter": beat.get("chapter") or "",
                "start": round(piece["start"], 3),
                "end": round(piece["end"], 3),
                "duration": duration,
                "visual": shot_visual,
                "labels": labels,
                "idea": idea,
                "alt": alt_text(shot_visual, idea, labels),
                "vo": piece["text"],
            }
            if shot_engine:
                shot["engine_type"] = shot_engine
            shots.append(shot)
    return {
        "lesson": data.get("lesson") or data.get("id") or data.get("title") or "lesson",
        "title": data.get("title") or "",
        "max_shot_seconds": MAX_SHOT,
        "shot_count": len(shots),
        "shots": shots,
    }


def render_markdown(plan_data: dict) -> str:
    lines = [
        f"# Shot list: {plan_data['lesson']}",
        "",
        "The picture changes at least every 8 seconds. Each shot is one idea.",
        "",
        "| # | Time | Visual | Labels | Alt |",
        "|---|---|---|---|---|",
    ]
    for index, shot in enumerate(plan_data["shots"], start=1):
        labels = ", ".join(shot["labels"])
        lines.append(
            f"| {index} | {shot['start']:.1f}–{shot['end']:.1f}s | {shot['visual']} | {labels} | {shot['alt']} |"
        )
    lines.append("")
    return "\n".join(lines)


def plan_path(path: Path) -> dict:
    data, beats = load_beats(Path(path))
    return plan(data, beats)


def write_plan(plan_data: dict, dest: Path) -> tuple[Path, Path]:
    dest.mkdir(parents=True, exist_ok=True)
    yaml_path = dest / "shotlist.yaml"
    md_path = dest / "shotlist.md"
    yaml_path.write_text(yaml.safe_dump(plan_data, sort_keys=False, allow_unicode=True), encoding="utf-8")
    md_path.write_text(render_markdown(plan_data), encoding="utf-8")
    return yaml_path, md_path
