"""Drawing surface shared by every visual type.

Text is real SVG text in the embedded fonts. Positions are recorded so QA
can check the safe area, overflow, size, and contrast without OCR.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from .clean import assert_drawable
from .fonts import family, pil_font
from .svg import Svg
from .theme import Theme

CAP = 0.72
DESC = 0.20


@dataclass
class Mark:
    role: str
    text: str
    size: int
    fill: str
    bg: str
    bbox: tuple[float, float, float, float]

    def as_dict(self) -> dict:
        return {
            "role": self.role,
            "text": self.text,
            "size": self.size,
            "fill": self.fill,
            "bg": self.bg,
            "bbox": [round(v, 1) for v in self.bbox],
        }


class Canvas:
    def __init__(self, theme: Theme):
        self.theme = theme
        self.svg = Svg(theme.width, theme.height)
        self.marks: list[Mark] = []
        self.labels: list[str] = []
        self.idea = ""
        self.example = False
        self.headline_text = ""

    @property
    def width(self) -> int:
        return self.theme.width

    @property
    def height(self) -> int:
        return self.theme.height

    def measure(self, text: str, size: int, weight: str = "semi") -> float:
        return float(pil_font(weight, size).getlength(text))

    def ink_box(self, text: str, x: float, y: float, size: int, anchor: str, weight: str) -> tuple[float, float, float, float]:
        width = self.measure(text, size, weight)
        if anchor == "middle":
            left = x - width / 2
        elif anchor == "end":
            left = x - width
        else:
            left = x
        top = y - size * CAP
        return (left, top, left + width, y + size * DESC)

    def text(self, content: str, x: float, y: float, size: int, fill: str, *,
             weight: str = "semi", anchor: str = "start", role: str = "label",
             bg: str | None = None, opacity: float = 1, rotate: float | None = None) -> tuple[float, float, float, float]:
        content = assert_drawable(content)
        if not content:
            return (x, y, x, y)
        box = self.ink_box(content, x, y, size, anchor, weight)
        self.svg.text(content, x, y, size, fill, family(weight), anchor=anchor, opacity=opacity, rotate=rotate)
        if role != "watermark":
            self.marks.append(Mark(role, content, size, fill, bg or self.theme.bg0, box))
        if role == "label" and content not in self.labels:
            self.labels.append(content)
        return box

    def backdrop(self) -> None:
        t = self.theme
        gid = self.svg.uid("bg")
        self.svg.linear_gradient(gid, t.bg0, t.bg1)
        self.svg.rect(0, 0, self.width, self.height, fill=f"url(#{gid})")
        if t.grid_alpha:
            step = 64
            with self.svg.group(opacity=t.grid_alpha):
                x = 0
                while x <= self.width:
                    self.svg.line(x, 0, x, self.height, t.grid, sw=1)
                    x += step
                y = 0
                while y <= self.height:
                    self.svg.line(0, y, self.width, y, t.grid, sw=1)
                    y += step
        if t.bokeh:
            spots = (
                (0.12, 0.18, 150),
                (0.88, 0.16, 180),
                (0.82, 0.84, 160),
                (0.16, 0.82, 120),
            )
            for fx, fy, radius in spots:
                self.svg.circle(self.width * fx, self.height * fy, radius, fill=t.accent, opacity=0.07)

    def headline(self, text: str, keyword: str | None = None) -> None:
        t = self.theme
        words = [w for w in assert_drawable(text).upper().split() if w][:6]
        if not words:
            return
        size = t.headline
        while size > t.min_font and self.measure(" ".join(words), size, "bold") > self.width - t.safe_x * 2:
            size -= 4
        skip = {"THE", "A", "AN", "OF", "AND"}
        if keyword and keyword.upper() in words:
            key = keyword.upper()
        else:
            content = [w for w in words if w not in skip] or words
            if content[0] in {"NO", "NOT"} and len(content) > 1:
                key = content[1]
            else:
                key = content[0]
        baseline = t.safe_top + 8 + size * CAP
        x = float(t.safe_x)
        for word in words:
            weight_fill = t.accent_ink if word == key else t.ink
            chunk = word + " "
            self.text(word, x, baseline, size, weight_fill, weight="bold", role="headline", bg=t.bg0)
            x += self.measure(chunk, size, "bold")
        self.headline_text = " ".join(words)

    def content_rect(self) -> tuple[float, float, float, float]:
        t = self.theme
        top = t.safe_top + t.headline + 52
        left = float(t.safe_x)
        right = self.width - t.safe_x
        bottom = self.height - t.safe_bottom - 8
        return (left, top, right - left, bottom - top)

    def glass(self, x, y, w, h, rx=28) -> None:
        t = self.theme
        self.svg.rect(x - 6, y - 6, w + 12, h + 12, fill="none", stroke=t.accent, sw=t.stroke * 4, rx=rx + 4, stroke_opacity=0.16)
        opacity = 0.94 if t.name == "light" else 0.82
        self.svg.rect(x, y, w, h, fill=t.card, stroke=t.card_line, sw=t.stroke, rx=rx, opacity=opacity)
        self.svg.line(x + rx, y + 1.5, x + w - rx, y + 1.5, "#FFFFFF", sw=1.25, opacity=0.18 if t.name != "light" else 0.7)

    def chip(self, text: str, x: float, y: float, anchor: str = "middle") -> tuple[float, float, float, float]:
        t = self.theme
        label = " ".join(assert_drawable(text).upper().split()[:3])
        if not label:
            return (x, y, x, y)
        size = t.label
        width = self.measure(label, size, "semi")
        cap = size * CAP
        desc = size * DESC
        pad_x, pad_y = 16, 9
        box_w = width + pad_x * 2
        box_h = cap + desc + pad_y * 2
        if anchor == "middle":
            left = x - box_w / 2
        elif anchor == "end":
            left = x - box_w
        else:
            left = x
        top = y - box_h / 2
        left, top = self._nudge(left, top, box_w, box_h)
        self.svg.rect(left, top, box_w, box_h, fill=t.chip, stroke=t.accent, sw=1.75, rx=10, opacity=0.96)
        baseline = top + pad_y + cap
        self.text(label, left + box_w / 2, baseline, size, t.chip_ink, weight="semi", anchor="middle", role="label", bg=t.chip)
        return (left, top, left + box_w, top + box_h)

    def _nudge(self, left: float, top: float, w: float, h: float) -> tuple[float, float]:
        t = self.theme
        min_x = 16
        max_x = self.width - 16 - w
        min_y = t.safe_top + 4
        max_y = self.height - t.safe_bottom - 4 - h
        return (min(max(left, min_x), max_x), min(max(top, min_y), max_y))

    def leader(self, x1, y1, x2, y2) -> None:
        t = self.theme
        self.svg.line(x1, y1, x2, y2, t.accent, sw=1.6)
        self.svg.circle(x2, y2, 4.5, fill=t.accent)

    def arrow(self, x1, y1, x2, y2, color: str | None = None) -> None:
        color = color or self.theme.accent
        self.svg.line(x1, y1, x2, y2, color, sw=self.theme.stroke + 0.5)
        angle = math.atan2(y2 - y1, x2 - x1)
        length = 14
        spread = 0.42
        p1 = (x2 - length * math.cos(angle - spread), y2 - length * math.sin(angle - spread))
        p2 = (x2 - length * math.cos(angle + spread), y2 - length * math.sin(angle + spread))
        self.svg.polygon([(x2, y2), p1, p2], fill=color)

    def stamp_example(self) -> None:
        if self.example:
            return
        self.example = True
        t = self.theme
        size = max(t.min_font, 22)
        label = "EXAMPLE"
        width = self.measure(label, size, "bold")
        cap = size * CAP
        desc = size * DESC
        pad_x, pad_y = 14, 8
        box_w = width + pad_x * 2
        box_h = cap + desc + pad_y * 2
        left = self.width - t.safe_x - box_w
        top = self.height - t.safe_bottom - box_h - 16
        self.svg.rect(left, top, box_w, box_h, fill=t.chip, stroke=t.accent, sw=2, rx=8, opacity=0.98)
        baseline = top + pad_y + cap
        self.text(label, left + box_w / 2, baseline, size, t.accent_ink, weight="bold", anchor="middle", role="badge", bg=t.chip)

    def watermark(self, cx: float, cy: float) -> None:
        size = 96 if self.width >= 1400 else 72
        self.svg.text("EXAMPLE", cx, cy, size, self.theme.muted, family("bold"), anchor="middle", opacity=0.16, rotate=-14)

    def plot_y(self, value: float, lo: float, hi: float, top: float, bottom: float, pad: float = 28) -> float:
        span = hi - lo
        if span == 0:
            span = 1
        t = (value - lo) / span
        t = min(1.0, max(0.0, t))
        return bottom - pad - t * (bottom - top - 2 * pad)

    def meta(self) -> dict:
        return {
            "idea": self.idea,
            "headline": self.headline_text,
            "labels": list(self.labels),
            "example": self.example,
            "marks": [mark.as_dict() for mark in self.marks],
        }
