"""Caption file checks: reading speed and line length."""

from __future__ import annotations

import re
from dataclasses import dataclass

from .profiles import Profile

_TS = re.compile(
    r"(?P<h>\d+):(?P<m>\d{2}):(?P<s>\d{2})[.,](?P<ms>\d{1,3})"
)


@dataclass(frozen=True)
class Cue:
    start: float
    end: float
    lines: tuple[str, ...]

    @property
    def text(self) -> str:
        return " ".join(line.strip() for line in self.lines if line.strip())


def _seconds(token: str) -> float:
    match = _TS.search(token.strip())
    if not match:
        raise ValueError(f"bad timestamp {token!r}")
    ms = match.group("ms").ljust(3, "0")
    return (
        int(match.group("h")) * 3600
        + int(match.group("m")) * 60
        + int(match.group("s"))
        + int(ms) / 1000
    )


def parse_captions(text: str) -> list[Cue]:
    """Parse WebVTT or SRT cues. Blank cues are dropped."""
    body = text.lstrip("\ufeff").replace("\r\n", "\n").replace("\r", "\n")
    if body.startswith("WEBVTT"):
        body = body.split("\n", 1)[1]
    blocks = re.split(r"\n\s*\n", body.strip())
    cues: list[Cue] = []
    for block in blocks:
        lines = [line for line in block.split("\n") if line.strip()]
        if lines and lines[0].strip().isdigit() and len(lines) > 1 and "-->" in lines[1]:
            lines = lines[1:]
        if not lines or "-->" not in lines[0]:
            continue
        left, right = lines[0].split("-->", 1)
        start = _seconds(left)
        end = _seconds(right.split()[0])
        payload = tuple(line.strip() for line in lines[1:] if line.strip())
        if payload:
            cues.append(Cue(start, end, payload))
    return cues


def caption_problems(cues: list[Cue], profile: Profile) -> list[str]:
    problems: list[str] = []
    if not cues:
        problems.append("caption file has no cues. Reading speed and line length were not skipped.")
        return problems
    for cue in cues:
        span = cue.end - cue.start
        stamp = f"{cue.start:.2f}-{cue.end:.2f}s"
        if span <= 0:
            problems.append(f"{stamp}: cue duration is not positive")
            continue
        if len(cue.lines) > profile.max_caption_lines:
            problems.append(
                f"{stamp}: {len(cue.lines)} lines, limit is {profile.max_caption_lines}"
            )
        for line in cue.lines:
            if len(line) > profile.max_caption_line:
                problems.append(
                    f"{stamp}: line is {len(line)} characters, limit is {profile.max_caption_line}"
                )
        cps = len(cue.text) / span
        if cps > profile.max_caption_cps:
            problems.append(
                f"{stamp}: {cps:.1f} characters per second, limit is {profile.max_caption_cps:.0f}"
            )
    return problems
