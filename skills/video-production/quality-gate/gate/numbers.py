"""Compare on-screen figures with the lesson file.

A figure is a dollar amount, a percent, or a number the lesson names.
On-screen text comes from captions and from OCR. A figure on screen that the
lesson does not name is a mismatch. A figure in the lesson without an EXAMPLE
or illustrative label is unlabeled.
"""

from __future__ import annotations

import re
from pathlib import Path

import yaml

FIGURE = re.compile(
    r"\$[\d,]+(?:\.\d+)?|\b\d+(?:\.\d+)?\s*%|\b\d+(?:\.\d+)?\b"
)
LABEL_OK = re.compile(r"\b(example|illustrative|illustration)\b", re.I)


def _norm(token: str) -> str:
    return token.replace("$", "").replace(",", "").replace("%", "").strip()


def _sentences(text: str) -> list[str]:
    return [part.strip() for part in re.split(r"(?<=[.?!])\s+|\n+", text) if part.strip()]


def lesson_figures(path: Path) -> tuple[set[str], list[str]]:
    """Return the set of named figures and unlabeled-figure messages."""
    data = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
    named: set[str] = set()
    unlabeled: list[str] = []
    blobs: list[str] = []

    def take(text: str) -> None:
        if not text:
            return
        blobs.append(text)
        for sentence in _sentences(text):
            for match in FIGURE.finditer(sentence):
                value = _norm(match.group(0))
                if not value or value in {".", ""}:
                    continue
                # Skip tiny counts that are not prices: single digits, and 1.
                if value.isdigit() and len(value) < 2:
                    continue
                named.add(value)
                if not LABEL_OK.search(sentence):
                    unlabeled.append(f"{value} in {sentence[:80]!r} has no EXAMPLE label")

    for key in ("disclaimer_spoken", "disclaimer_on_screen"):
        take(str(data.get(key) or ""))
    for beat in data.get("beats") or data.get("sections") or []:
        for key in ("vo", "narration", "on_screen", "cap", "caption", "sub"):
            take(str(beat.get(key) or ""))
        visual = beat.get("visual") or {}
        for key in ("caption", "sub", "title"):
            take(str(visual.get(key) or ""))
        for line in visual.get("lines") or []:
            take(str(line))
        for label in beat.get("labels") or []:
            take(str(label))
    for item in data.get("chart_labels") or []:
        take(f"EXAMPLE {item}")
    return named, unlabeled


def screen_figures(text: str) -> set[str]:
    found: set[str] = set()
    for match in FIGURE.finditer(text or ""):
        value = _norm(match.group(0))
        if value.isdigit() and len(value) < 2:
            continue
        if value:
            found.add(value)
    return found


def number_problems(screen_text: str, lesson: Path | None) -> list[str]:
    problems: list[str] = []
    seen = screen_figures(screen_text)
    if lesson is None or not Path(lesson).is_file():
        # Without a lesson, only unlabeled currency and percents in the captions can be judged.
        for sentence in _sentences(screen_text or ""):
            if "$" not in sentence and "%" not in sentence:
                continue
            if LABEL_OK.search(sentence):
                continue
            if FIGURE.search(sentence):
                problems.append(f"on-screen figure has no EXAMPLE label: {sentence[:80]!r}")
        return problems
    named, unlabeled = lesson_figures(Path(lesson))
    problems.extend(unlabeled[:8])
    extra = sorted(seen - named)
    # Axis ticks and OCR noise: only flag extras that are currency, percents, or declared-scale numbers.
    interesting = []
    for token in extra:
        raw = token
        if any(mark in screen_text for mark in (f"${raw}", f"{raw}%", f"{raw} %")):
            interesting.append(raw)
        elif raw in named:
            continue
        else:
            # A bare number on screen that the lesson never names.
            interesting.append(raw)
    if interesting:
        problems.append("on-screen figures not in the lesson: " + ", ".join(interesting[:12]))
    return problems
