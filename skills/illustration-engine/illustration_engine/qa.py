"""Automated checks, plus a beginner-check report a person can read."""

from __future__ import annotations

import io
from dataclasses import dataclass, field
from functools import lru_cache

from PIL import Image

from .fonts import HEADLINE_FAMILY, bundled_match
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


def _luma(red: int, green: int, blue: int) -> float:
    return 0.2126 * red + 0.7152 * green + 0.0722 * blue


def _core_mask(image: Image.Image) -> Image.Image:
    """Keep the crisp glyph and drop the bloom around it."""
    rgb = image.convert("RGB")
    width, height = rgb.size
    raw = rgb.tobytes()
    mask = Image.new("L", (width, height), 0)
    pix = mask.load()
    samples = []
    for y in range(0, height, 3):
        row = y * width * 3
        for x in range(0, width, 3):
            index = row + x * 3
            samples.append(_luma(raw[index], raw[index + 1], raw[index + 2]))
    paper = sorted(samples)[len(samples) // 2] if samples else 0
    dark_plate = paper > 170
    for y in range(height):
        row = y * width * 3
        for x in range(width):
            index = row + x * 3
            red, green, blue = raw[index], raw[index + 1], raw[index + 2]
            if dark_plate:
                if max(red, green, blue) < 95:
                    pix[x, y] = 255
            elif min(red, green, blue) > 214 or (blue > 235 and green > 190 and red < 70):
                pix[x, y] = 255
    return mask


def _stem_on_mask(image: Image.Image, cap_px: int = 55) -> float:
    """Left-stem width of a glyph, scaled so the cap height is cap_px."""
    gray = _core_mask(image)
    width, height = gray.size
    rows = [y for y in range(height) if any(gray.getpixel((x, y)) > 200 for x in range(width))]
    if len(rows) < 4:
        return 0.0
    cap = rows[-1] - rows[0] + 1
    # Above the crossbar, so the sample is one vertical stem.
    row = rows[0] + max(2, int(cap * 0.16))
    run = 0
    best = 0
    started = False
    for x in range(width):
        if gray.getpixel((x, row)) > 200:
            run += 1
            started = True
        elif started:
            best = run
            break
    stem = float(best or run)
    if cap <= 0 or stem <= 0:
        return 0.0
    return stem * cap_px / cap


@lru_cache(maxsize=1)
def stem_width(cap_px: int = 55) -> float:
    """Stem of H painted by the production rasterizer at font-weight 700.

    Real Roboto Condensed Bold is about 10-11px at a 55px cap. A regular
    face falls to about 6-7px. This probe uses the same SVG weight and the
    same rasterizer as a plate, so a font-name check cannot pass it.
    """
    import tempfile
    from pathlib import Path

    from .fonts import css_for, family
    from .render import rasterize

    with tempfile.TemporaryDirectory() as tmp:
        folder = Path(tmp)
        svg = folder / "stem.svg"
        png = folder / "stem.png"
        svg.write_text(
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<svg xmlns="http://www.w3.org/2000/svg" width="480" height="280" viewBox="0 0 480 280">\n'
            "<defs><style><![CDATA[\n"
            f"{css_for(svg)}\n"
            "]]></style></defs>\n"
            '<rect width="480" height="280" fill="#000000"/>\n'
            f'<text x="36" y="190" fill="#F4F8FC" font-family="{family("condensed")}" '
            'font-weight="700" font-size="80">H</text>\n'
            "</svg>\n",
            encoding="utf-8",
        )
        rasterize(svg, png, 480, 280)
        return _stem_on_mask(Image.open(png), cap_px)


def headline_stem(png: bytes, marks: list[dict], cap_px: int = 55) -> float:
    """Stem width of the headline actually painted on this plate."""
    words = [mark for mark in marks if mark.get("role") == "headline"]
    if not words:
        return stem_width(cap_px)
    image = Image.open(io.BytesIO(png)).convert("RGB")
    found = []
    for mark in words:
        x0 = max(0, int(mark["bbox"][0]) - 4)
        y0 = max(0, int(mark["bbox"][1]) - 4)
        x1 = min(image.width, int(mark["bbox"][2]) + 4)
        y1 = min(image.height, int(mark["bbox"][3]) + 4)
        if x1 - x0 < 4 or y1 - y0 < 4:
            continue
        measured = _stem_on_mask(image.crop((x0, y0, x1, y1)), cap_px)
        if 8 <= measured <= 18:
            found.append(measured)
    if not found:
        return stem_width(cap_px)
    found.sort()
    return found[len(found) // 2]


def ink_coverage(png: bytes) -> float:
    """Share of the frame that is visibly off the background."""
    image = Image.open(io.BytesIO(png)).convert("RGB")
    width, height = image.size
    raw = image.tobytes()

    def luma_at(x: int, y: int) -> float:
        index = (y * width + x) * 3
        return _luma(raw[index], raw[index + 1], raw[index + 2])

    border = []
    for x in range(0, width, 6):
        border.append(luma_at(x, 1))
        border.append(luma_at(x, height - 2))
    for y in range(0, height, 6):
        border.append(luma_at(1, y))
        border.append(luma_at(width - 2, y))
    border.sort()
    base = border[len(border) // 2]
    ink = 0
    total = 0
    step = 2
    for y in range(0, height, step):
        row = y * width * 3
        for x in range(0, width, step):
            index = row + x * 3
            total += 1
            if abs(_luma(raw[index], raw[index + 1], raw[index + 2]) - base) > 14:
                ink += 1
    return ink / max(total, 1)


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
    headlines = [mark for mark in marks if mark["role"] == "headline"]
    wrong_face = [mark["text"] for mark in headlines if mark.get("family") != HEADLINE_FAMILY]
    report.add(
        "headline face",
        bool(headlines) and not wrong_face,
        "condensed bold" if headlines and not wrong_face else "headline is missing the condensed bold face",
    )
    label_floor = 24 * theme.scale
    small_labels = [mark["text"] for mark in labels if mark["size"] + 0.1 < label_floor]
    report.add(
        "label size",
        not small_labels,
        f"labels at least {label_floor:.0f}px" if not small_labels else "small labels: " + ", ".join(small_labels),
    )
    fonts_ok, fonts_detail = bundled_match()
    report.add("bundled fonts", fonts_ok, fonts_detail)
    stem = stem_width(55)
    report.add("stem width", stem >= 10, f"{stem:.1f}px at a 55px cap")
    report.add("one idea", bool(meta.get("idea")), meta.get("idea") or "missing idea")
    banned = ("profit", "guaranteed", "win-rate", "win rate", "@", "http")
    dirty = []
    for mark in marks:
        low = mark["text"].lower()
        if any(word in low for word in banned):
            dirty.append(mark["text"])
    report.add("no claims or contact details", not dirty, ", ".join(dirty) if dirty else "clean")
    return report


def check_headline_gap(png: bytes, marks: list[dict]) -> tuple[bool, str]:
    """Fail when two headline words are painted as one, with no space between them."""
    words = sorted((mark for mark in marks if mark.get("role") == "headline"), key=lambda mark: mark["bbox"][0])
    if len(words) < 2:
        return True, "one headline word"
    for left, right in zip(words, words[1:]):
        x0 = int(left["bbox"][2])
        x1 = int(right["bbox"][0])
        if x1 - x0 < 6:
            return False, f"{left['text']} runs into {right['text']}"
    return True, "spaces hold between headline words"


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
