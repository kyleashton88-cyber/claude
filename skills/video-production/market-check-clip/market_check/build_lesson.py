"""Turn a Market Check markdown post into a pipeline lesson.yaml.

Sections stay short so a title card does not sit still for more than 8 seconds.
The whole narration is sized for the 60–90 second Market Check window.
"""

from __future__ import annotations

import re
from pathlib import Path

WPM = 148.0
PAD = 0.35 + 0.45
END_CARD = 3.2
SECTION_WORDS = 12


def _sentences(text: str) -> list[str]:
    parts = re.split(r"(?<=[.?!])\s+", re.sub(r"\s+", " ", text).strip())
    return [part.strip() for part in parts if part.strip()]


def parse_post(text: str) -> dict:
    title = "Market Check"
    body_lines: list[str] = []
    for line in text.splitlines():
        if line.startswith("# "):
            title = line[2:].strip()
            continue
        if line.startswith("#"):
            body_lines.append(line.lstrip("#").strip())
            continue
        body_lines.append(line)
    body = "\n".join(body_lines)
    spoken = " ".join(_sentences(body))
    if "not financial advice" not in spoken.lower():
        spoken += " This is education, not financial advice."
    return {"title": title, "spoken": spoken}


def _chunks(spoken: str, words_per: int = SECTION_WORDS) -> list[str]:
    words = spoken.split()
    if not words:
        return ["This is education, not financial advice."]
    return [" ".join(words[i:i + words_per]) for i in range(0, len(words), words_per)]


def estimate_seconds(chunks: list[str]) -> float:
    speech = sum(len(chunk.split()) for chunk in chunks) / WPM * 60.0
    return speech + len(chunks) * PAD + END_CARD


def lesson_from_post(text: str) -> dict:
    parsed = parse_post(text)
    chunks = _chunks(parsed["spoken"])
    sections = []
    for index, chunk in enumerate(chunks, start=1):
        chapter = "What changed" if index == 1 else "The check"
        sections.append({
            "id": f"b{index}",
            "chapter": chapter if index == 1 or index == len(chunks) else f"Beat {index}",
            "narration": chunk,
            "visual": {
                "kind": "title",
                "lines": [chunk.split()[0] if chunk.split() else "Check", "this week"],
                "sub": "EXAMPLE figures only" if "EXAMPLE" in chunk or "example" in chunk.lower() else "Education, not financial advice",
                "caption": "Education, not financial advice",
                "lower_third": {"kicker": "Market check", "line": "Not a call to trade"},
            },
        })
    return {
        "id": "market-check-demo",
        "title": parsed["title"],
        "format": "market-check",
        "engine": "kokoro",
        "mood": "calm-teacher",
        "sections": sections,
        "end_card": {
            "kicker": "Education only",
            "line": "Not financial advice. Figures marked EXAMPLE are illustrations.",
        },
    }


def write_lesson(post: Path, dest: Path) -> dict:
    import yaml
    data = lesson_from_post(post.read_text(encoding="utf-8"))
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True), encoding="utf-8")
    return data
