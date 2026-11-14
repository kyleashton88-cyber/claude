"""Script markup: pauses, emphasis, and pace, plus the sentence pauses from the lesson narrator.

Written forms kept for captions:
  *word*  or  <emph>word</emph>   slightly faster, a little louder, a small pitch lift
  <slow>...</slow>                slower
  <fast>...</fast>                faster
  [[pause 0.4]]  <pause 400ms>  <pause 0.4s>
A blank line is a breath between sections. The mood sets how long that breath is.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

PAUSE = {".": 0.28, "!": 0.30, "?": 0.40, ":": 0.22, ";": 0.20, "…": 0.62, ",": 0.14, "": 0.16}
ABBR = re.compile(r"\b(?:[A-Za-z]\.){2,}[a-z]?")
TITLES = re.compile(r"\b(Mr|Mrs|Ms|Dr|St|vs|etc|approx|no)\.", re.I)

MARK = re.compile(
    r"\[\[pause\s+([0-9]*\.?[0-9]+)\s*\]\]"
    r"|<pause\s+([0-9]*\.?[0-9]+)\s*(ms|s)?\s*/?>"
    r"|<emph>(.*?)</emph>"
    r"|<slow>(.*?)</slow>"
    r"|<fast>(.*?)</fast>"
    r"|\*([^*]+)\*"
    r"|([^<*]+)",
    re.IGNORECASE | re.DOTALL,
)


@dataclass
class Span:
    kind: str  # speech or pause
    text: str = ""
    rate: float = 1.0
    emph: bool = False
    pause: float = 0.0


def _pause_seconds(amount: str, unit: str | None) -> float:
    value = float(amount)
    if unit and unit.lower() == "ms":
        value /= 1000.0
    if value < 0 or value > 10:
        raise ValueError("a pause must be between 0 and 10 seconds")
    return value


def parse_markup(text: str) -> list[Span]:
    spans: list[Span] = []
    for match in MARK.finditer(text):
        if match.group(1) is not None:
            spans.append(Span("pause", pause=float(match.group(1))))
        elif match.group(2) is not None:
            spans.append(Span("pause", pause=_pause_seconds(match.group(2), match.group(3))))
        elif match.group(4) is not None:
            spans.append(Span("speech", text=match.group(4), rate=0.94, emph=True))
        elif match.group(5) is not None:
            spans.append(Span("speech", text=match.group(5), rate=1.22))
        elif match.group(6) is not None:
            spans.append(Span("speech", text=match.group(6), rate=0.86))
        elif match.group(7) is not None:
            spans.append(Span("speech", text=match.group(7), rate=0.94, emph=True))
        elif match.group(8) and match.group(8).strip():
            spans.append(Span("speech", text=match.group(8)))
    return spans


def written_text(text: str) -> str:
    parts = []
    for span in parse_markup(text):
        if span.kind == "speech":
            parts.append(span.text)
    return re.sub(r"\s+", " ", "".join(parts)).strip()


def sentences(text: str) -> list[tuple[str, float]]:
    """Split narration the way the lesson voice does, keeping a pause after each stop."""
    out: list[tuple[str, float]] = []
    for span in parse_markup(text):
        if span.kind == "pause":
            if out:
                out[-1] = (out[-1][0], out[-1][1] + span.pause)
            else:
                out.append(("", span.pause))
            continue
        out.extend(_sentences(span.text))
    return [(text, pause) for text, pause in out if text or pause]


def _sentences(text: str) -> list[tuple[str, float]]:
    cleaned = re.sub(r"\s+", " ", text.strip()).replace("...", "…")
    guard: dict[str, str] = {}

    def protect(match: re.Match) -> str:
        key = f"⁣{len(guard)}⁣"
        guard[key] = match.group(0)
        return key

    cleaned = ABBR.sub(protect, cleaned)
    cleaned = TITLES.sub(protect, cleaned)
    cleaned = re.sub(r"(\d)\.(\d)", r"\1⁤\2", cleaned)
    parts = re.split(r"(?<=[.!?…,:])\s+|(?<=…)(?=\S)", cleaned)
    out: list[tuple[str, float]] = []
    for part in parts:
        part = part.strip()
        if not part:
            continue
        for key, value in guard.items():
            part = part.replace(key, value)
        part = part.replace("⁤", ".")
        if part == "…":
            if out:
                out[-1] = (out[-1][0], out[-1][1] + PAUSE["…"])
            continue
        end = part[-1] if part[-1] in PAUSE else ""
        spoken = part.rstrip("…").strip() or part
        out.append((spoken, PAUSE[end]))
    return out


def section_breaks(text: str) -> list[str]:
    """Blank lines split a script into sections. Each gap becomes a breath."""
    blocks = [block.strip() for block in re.split(r"\n\s*\n", text.strip()) if block.strip()]
    return blocks or [text.strip()]
