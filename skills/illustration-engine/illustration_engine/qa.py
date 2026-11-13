"""Automated checks, plus a beginner-check report a person can read."""

from __future__ import annotations

import io
from dataclasses import dataclass, field

from PIL import Image

from .theme import Theme


def relative_luminance(hex_color: str) -> float:
    hex_color = hex_color.lstrip("#")
    if len(hex_color) != 6:
        return 0.0
    channels = []
    for i in range(0, 6, 2):
        value = int(hex_color[i:i + 2], 16) / 255
        if value <= 0.04045:
            channels.append(value / 12.92)
        else:
            channels.append(((value + 0.055) / 1.055) ** 2.4)
    red, green, blue = channels
    return 0.2126 * red + 0.7152 * green + 0.0722 * blue


def contrast_ratio(foreground: str, background: str) -> float:
    lighter = max(relative_luminance(foreground), relative_luminance(background))
    darker = min(relative_luminance(foreground), relative_luminance(background))
    return (lighter + 0.05) / (darker + 0.05)


def _needs_ratio(size: int) -> float:
    return 3.0 if size >= 24 else 4.5


@dataclass
class QaReport:
    ok: bool
    checks: list[str] = field(default_factory=list)
    failures: list[str] = field(default_factory=list)

    def add(self, name: str, passed: bool, detail: str) -> None:
        line = f"{'pass' if passed else 'fail'}: {name} — {detail}"
        self.checks.append(line)
        if not passed:
            self.failures.append(line)
            self.ok = False


def check_pixels(png: bytes, theme: Theme) -> tuple[bool, str]:
    image = Image.open(io.BytesIO(png)).convert("RGB")
    if image.size != (theme.width, theme.height):
        return False, f"size {image.size[0]}x{image.size[1]}, expected {theme.width}x{theme.height}"
    small = image.resize((48, 32)).convert("L")
    values = list(small.get_flattened_data())
    lo, hi = min(values), max(values)
    mean = sum(values) / len(values)
    std = (sum((value - mean) ** 2 for value in values) / len(values)) ** 0.5
    if hi - lo < 24 or std < 6:
        return False, f"blank or near-blank output (spread {hi - lo:.0f}, std {std:.1f})"
    return True, f"{theme.width}x{theme.height}, spread {hi - lo:.0f}"


def check_scene(meta: dict, theme: Theme) -> QaReport:
    report = QaReport(ok=True)
    marks = meta.get("marks") or []
    labels = [mark for mark in marks if mark["role"] == "label"]
    safe_top = theme.safe_top
    safe_bottom = theme.height - theme.safe_bottom
    safe_left = 12
    safe_right = theme.width - 12
    overflow = 0
    outside = 0
    small = 0
    weak = 0
    for mark in marks:
        if mark["role"] == "watermark":
            continue
        x0, y0, x1, y1 = mark["bbox"]
        if x0 < -1 or y0 < -1 or x1 > theme.width + 1 or y1 > theme.height + 1:
            overflow += 1
        if mark["role"] in {"headline", "label", "price", "badge", "step"}:
            if y0 < safe_top - 1 or y1 > safe_bottom + 1 or x0 < safe_left or x1 > safe_right:
                outside += 1
        if mark["size"] < theme.min_font:
            small += 1
        ratio = contrast_ratio(mark["fill"], mark["bg"])
        if ratio < _needs_ratio(mark["size"]):
            weak += 1
    report.add("label overflow", overflow == 0, f"{overflow} marks outside the frame")
    report.add("safe margins", outside == 0, f"{outside} marks in the outer margin")
    report.add("minimum font size", small == 0, f"{small} marks under {theme.min_font}px")
    report.add("contrast", weak == 0, f"{weak} marks below the contrast floor")
    count = len({mark["text"] for mark in labels})
    report.add("label count", 2 <= count <= 5, f"{count} labels (want 2 to 5)")
    long = [mark["text"] for mark in labels if len(mark["text"].split()) > 3]
    report.add("plain labels", not long, "long labels: " + ", ".join(long) if long else "each label is at most three words")
    needs_example = any(
        mark["role"] == "price" or (mark["role"] == "label" and any(ch.isdigit() for ch in mark["text"]))
        for mark in marks
    )
    if needs_example:
        report.add("example stamp", bool(meta.get("example")), "a figure is on the plate" if meta.get("example") else "a figure is missing the EXAMPLE stamp")
    else:
        report.add("example stamp", True, "no figure on this plate")
    report.add("one idea", bool(meta.get("idea")), meta.get("idea") or "missing idea")
    banned = ("profit", "guaranteed", "win-rate", "win rate", "@", "http")
    dirty = []
    for mark in marks:
        low = mark["text"].lower()
        if any(word in low for word in banned):
            dirty.append(mark["text"])
    report.add("no claims or contact details", not dirty, ", ".join(dirty) if dirty else "clean")
    return report


def beginner_lines(name: str, meta: dict, report: QaReport) -> list[str]:
    labels = ", ".join(meta.get("labels") or []) or "(none)"
    verdict = "pass" if report.ok else "look again"
    lines = [
        f"### {name}",
        f"- Idea: {meta.get('idea') or 'unknown'}",
        f"- Headline: {meta.get('headline') or 'none'}",
        f"- Labels ({len(meta.get('labels') or [])}): {labels}",
        f"- Example stamp: {'yes' if meta.get('example') else 'no'}",
        f"- Automated: {verdict}",
    ]
    if report.failures:
        for failure in report.failures:
            lines.append(f"- {failure}")
    lines.append("- Human check: with the sound off, is this one idea, in plain words, and obvious to a beginner?")
    return lines


BEGINNER_INTRO = """# Beginner check

Read each plate with the sound off.

- One idea only.
- A short headline, then 2 to 5 plain labels.
- Arrows or leader lines point at the thing the label names.
- Any figure is stamped EXAMPLE.
- No venue name, no contact detail, no profit claim, no paragraph.
"""
