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

# Thousands groups (30,331) are one figure. A bare 30 is not that group.
_GROUPED = re.compile(r"\d{1,3}(?:,\d{3})+(?:\.\d+)?")
_PLAIN = re.compile(r"\d+(?:\.\d+)?")
FIGURE = re.compile(
    rf"\$[\d,]+(?:\.\d+)?|{_GROUPED.pattern}|\b{_PLAIN.pattern}\s*%|\b{_PLAIN.pattern}\b"
)
LABEL_OK = re.compile(r"\b(example|illustrative|illustration)\b", re.I)

_MONTH_FULL = {
    "january": "January",
    "february": "February",
    "march": "March",
    "april": "April",
    "may": "May",
    "june": "June",
    "july": "July",
    "august": "August",
    "september": "September",
    "october": "October",
    "november": "November",
    "december": "December",
}
_MONTH_ALIAS = {
    **{name.lower(): name for name in _MONTH_FULL.values()},
    "jan": "January",
    "feb": "February",
    "mar": "March",
    "apr": "April",
    "jun": "June",
    "jul": "July",
    "aug": "August",
    "sep": "September",
    "sept": "September",
    "oct": "October",
    "nov": "November",
    "dec": "December",
}
_MONTH_ALT = "|".join(sorted(_MONTH_ALIAS, key=len, reverse=True))
# A day that continues ",ddd" is the start of a thousands group, not a date.
_DATE = re.compile(
    rf"\b(?P<d1>\d{{1,2}})(?!,\d{{3}})\s+(?P<m1>{_MONTH_ALT})(?:\s+(?P<y1>\d{{4}}))?\b"
    rf"|\b(?P<m2>{_MONTH_ALT})\s+(?P<d2>\d{{1,2}})(?!,\d{{3}})(?:\s+(?P<y2>\d{{4}}))?\b",
    re.I,
)


def _norm(token: str) -> str:
    return token.replace("$", "").replace(",", "").replace("%", "").strip()


def _month_name(token: str) -> str:
    return _MONTH_ALIAS[token.lower()]


def _date_phrase(day: int, month: str, year: int | None) -> str:
    if year is None:
        return f"{day} {month}"
    return f"{day} {month} {year}"


def _parse_date(match: re.Match[str]) -> tuple[int, str, int | None]:
    if match.group("d1"):
        day = int(match.group("d1"))
        month = _month_name(match.group("m1"))
        year = int(match.group("y1")) if match.group("y1") else None
    else:
        day = int(match.group("d2"))
        month = _month_name(match.group("m2"))
        year = int(match.group("y2")) if match.group("y2") else None
    return day, month, year


def _iter_dates(text: str):
    """Date matches that do not overlap a thousands-grouped number.

    Grouped numbers are claimed first, so "Oct 28,519" is the price 28519
    and not the date 28 October.
    """
    grouped = [(match.start(), match.end()) for match in _GROUPED.finditer(text or "")]
    for match in _DATE.finditer(text or ""):
        if _covered(grouped, match.start(), match.end()):
            continue
        yield match


def find_dates(text: str) -> list[str]:
    """Dates in reading order. A day beside a month, with the year when it is written."""
    found: list[str] = []
    seen: set[str] = set()
    for match in _iter_dates(text or ""):
        phrase = _date_phrase(*_parse_date(match))
        if phrase not in seen:
            seen.add(phrase)
            found.append(phrase)
    return found


def _covered(spans: list[tuple[int, int]], start: int, end: int) -> bool:
    return any(start < stop and end > begin for begin, stop in spans)


def _figure_values(text: str, skip: list[tuple[int, int]]) -> set[str]:
    """Figures in text. Digits inside a date or a thousands group are not separate figures."""
    found: set[str] = set()
    occupied = list(skip)
    for match in _GROUPED.finditer(text or ""):
        if _covered(occupied, match.start(), match.end()):
            continue
        value = _norm(match.group(0))
        if value:
            found.add(value)
        occupied.append((match.start(), match.end()))
    for match in FIGURE.finditer(text or ""):
        if _covered(occupied, match.start(), match.end()):
            continue
        value = _norm(match.group(0))
        if not value or value in {".", ""}:
            continue
        if value.isdigit() and len(value) < 2:
            continue
        found.add(value)
    return found


def _date_known(seen: tuple[int, str, int | None], allowed: set[tuple[int, str, int | None]]) -> bool:
    day, month, year = seen
    if year is None:
        return any(item[0] == day and item[1] == month for item in allowed)
    return (day, month, year) in allowed


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
            date_spans = [(match.start(), match.end()) for match in _iter_dates(sentence)]
            for value in _figure_values(sentence, date_spans):
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


def lesson_date_keys(path: Path) -> set[tuple[int, str, int | None]]:
    data = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
    allowed: set[tuple[int, str, int | None]] = set()
    for item in data.get("dates") or []:
        for match in _DATE.finditer(str(item)):
            allowed.add(_parse_date(match))
    return allowed


def screen_figures(text: str) -> set[str]:
    spans = [(match.start(), match.end()) for match in _iter_dates(text or "")]
    return _figure_values(text or "", spans)


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
    allowed = lesson_date_keys(Path(lesson))
    unknown_dates = []
    for match in _iter_dates(screen_text or ""):
        parsed = _parse_date(match)
        if _date_known(parsed, allowed):
            continue
        phrase = _date_phrase(*parsed)
        if phrase not in unknown_dates:
            unknown_dates.append(phrase)
    if unknown_dates:
        problems.append("on-screen date not in the lesson: " + ", ".join(unknown_dates[:8]))
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
