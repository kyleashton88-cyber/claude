"""Drawing surface shared by every visual type.

Text is real SVG text in the embedded fonts. Positions are recorded so QA
can check the safe area, overflow, size, and contrast without OCR.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from .clean import assert_drawable
from .fonts import advance, css_weight, family
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
    family: str
    bbox: tuple[float, float, float, float]

    def as_dict(self) -> dict:
        return {
            "role": self.role,
            "text": self.text,
            "size": self.size,
            "fill": self.fill,
            "bg": self.bg,
            "family": self.family,
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
        return advance(weight, text, size)

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
        face = family(weight)
        self.svg.text(
            content, x, y, size, fill, face,
            anchor=anchor, opacity=opacity, rotate=rotate, weight=css_weight(weight),
        )
        if role != "watermark":
            self.marks.append(Mark(role, content, size, fill, bg or self.theme.bg0, face, box))
        if role == "label" and content not in self.labels:
            self.labels.append(content)
        return box

    def backdrop(self) -> None:
        t = self.theme
        gid = self.svg.uid("bg")
        self.svg.linear_gradient(gid, [("0%", t.bg0), ("52%", t.bg_mid), ("100%", t.bg1)])
        self.svg.rect(0, 0, self.width, self.height, fill=f"url(#{gid})")
        if t.grid_alpha:
            step = max(8, t.grid_pitch)
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
            spots = ((0.86, 0.14, t.s(90)), (0.12, 0.88, t.s(70)))
            for fx, fy, radius in spots:
                self.svg.circle(self.width * fx, self.height * fy, radius, fill=t.accent, opacity=0.045)
        vig = self.svg.uid("vig")
        self.svg.radial_gradient(vig, t.bg0, t.vignette)
        self.svg.rect(0, 0, self.width, self.height, fill=f"url(#{vig})")

    def headline(self, text: str, keyword: str | None = None) -> None:
        t = self.theme
        words = [w for w in assert_drawable(text).upper().split() if w][:6]
        if not words:
            return
        size = t.headline

        def span(px: int) -> float:
            space = max(self.measure(" ", px, "condensed"), t.s(8))
            return sum(self.measure(word, px, "condensed") for word in words) + space * (len(words) - 1)

        while size > t.headline_floor and span(size) > self.width - t.safe_x * 2:
            size -= 2
        skip = {"THE", "A", "AN", "OF", "AND"}
        if keyword and keyword.upper() in words:
            key = keyword.upper()
        else:
            content = [w for w in words if w not in skip] or words
            if content[0] in {"NO", "NOT"} and len(content) > 1:
                key = content[1]
            else:
                key = content[0]
        baseline = t.safe_top + t.s(8) + size * CAP
        x = float(t.safe_x)
        space = max(self.measure(" ", size, "condensed"), t.s(8))
        bloom = self.svg.ensure_glow(t.glow_std())
        for word in words:
            weight_fill = t.accent_ink if word == key else t.ink
            self.svg.text(
                word, x, baseline, size, t.accent, family("condensed"),
                weight="700", opacity=0.9, filt=bloom,
            )
            self.text(word, x, baseline, size, weight_fill, weight="condensed", role="headline", bg=t.bg0)
            x += self.measure(word, size, "condensed") + space
        self.headline_text = " ".join(words)

    def content_rect(self) -> tuple[float, float, float, float]:
        t = self.theme
        top = t.safe_top + t.headline + t.s(36)
        left = float(t.safe_x)
        right = self.width - t.safe_x
        bottom = self.height - t.safe_bottom - 8
        avail_w = right - left
        avail_h = bottom - top
        # Wide enough for three cards of about 360px at 1536, short enough that
        # the bloom stays inside the 30-55% coverage band.
        width = min(avail_w, 3 * t.s(300) + 2 * t.s(28) + t.s(8))
        height = min(avail_h, t.s(433) + t.s(20))
        limit = 0.40 * self.width * self.height
        if width * height > limit and width > 0:
            height = min(height, limit / width)
            if width * height > limit:
                scale = (limit / (width * height)) ** 0.5
                width *= scale
                height *= scale
        left += (avail_w - width) / 2
        top += (avail_h - height) / 2
        return (left, top, width, height)

    def glass(self, x, y, w, h, rx=None) -> None:
        t = self.theme
        rx = t.s(22) if rx is None else rx
        bloom = self.svg.ensure_glow(t.glow_std())
        wash = t.wash_px()
        peak = self._peak(t.accent)
        fill_opacity = 0.94 if t.name == "light" else 0.9
        self.svg.rect(x, y, w, h, fill=t.card, stroke="none", sw=0, rx=rx, opacity=fill_opacity)
        # 32px soft inner wash at 1536, blurred, then a near-white peak with no hard 4px stroke.
        inner = 0.34 if t.name == "light" else (0.1 if t.name == "contrast" else 0.18)
        self.svg.rect(x, y, w, h, fill=t.accent, stroke="none", sw=0, rx=rx, opacity=inner)
        self.svg.rect(x, y, w, h, fill="none", stroke=t.accent, sw=wash, rx=rx, opacity=0.8, filt=bloom)
        self.svg.rect(x, y, w, h, fill="none", stroke=peak, sw=wash, rx=rx, opacity=0.55, filt=bloom)
        self.svg.rect(x, y, w, h, fill="none", stroke=peak, sw=max(1.6, t.s(1.7)), rx=rx, opacity=1)

    def chip(self, text: str, x: float, y: float, anchor: str = "middle") -> tuple[float, float, float, float]:
        t = self.theme
        words = [word for word in assert_drawable(text).split() if word][:3]
        label = " ".join(word[:1].upper() + word[1:].lower() for word in words)
        if not label:
            return (x, y, x, y)
        size = t.label
        width = self.measure(label, size, "bold")
        cap = size * CAP
        desc = size * DESC
        pad_x, pad_y = t.s(16), t.s(8)
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
        bloom = self.svg.ensure_glow(t.glow_std())
        peak = self._peak(t.accent)
        self.svg.rect(left, top, box_w, box_h, fill="none", stroke=t.accent, sw=t.s(12), rx=t.s(10), opacity=0.85, filt=bloom)
        self.svg.rect(left, top, box_w, box_h, fill=t.chip, stroke="none", sw=0, rx=t.s(10), opacity=0.92 if t.name != "light" else 0.96)
        self.svg.rect(left, top, box_w, box_h, fill="none", stroke=peak, sw=max(1.4, t.s(1.4)), rx=t.s(10), opacity=1)
        baseline = top + pad_y + cap
        self.text(label, left + box_w / 2, baseline, size, t.chip_ink, weight="bold", anchor="middle", role="label", bg=t.chip)
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
        self.glow_line(x1, y1, x2, y2, t.accent, sw=t.arrow)
        self.svg.circle(x2, y2, t.s(4.5), fill=t.accent)

    def arrow(self, x1, y1, x2, y2, color: str | None = None) -> None:
        color = color or self.theme.accent
        self.glow_line(x1, y1, x2, y2, color, sw=self.theme.arrow)
        angle = math.atan2(y2 - y1, x2 - x1)
        length = self.theme.s(14)
        spread = 0.42
        p1 = (x2 - length * math.cos(angle - spread), y2 - length * math.sin(angle - spread))
        p2 = (x2 - length * math.cos(angle + spread), y2 - length * math.sin(angle + spread))
        self.svg.polygon([(x2, y2), p1, p2], fill=color)

    def stamp_example(self) -> None:
        if self.example:
            return
        self.example = True
        t = self.theme
        size = t.label
        label = "EXAMPLE"
        width = self.measure(label, size, "bold")
        cap = size * CAP
        desc = size * DESC
        pad_x, pad_y = t.s(14), t.s(8)
        box_w = width + pad_x * 2
        box_h = cap + desc + pad_y * 2
        left = self.width - t.safe_x - box_w
        top = self.height - t.safe_bottom - box_h - t.s(12)
        bloom = self.svg.ensure_glow(t.glow_std())
        peak = self._peak(t.accent)
        self.svg.rect(left, top, box_w, box_h, fill="none", stroke=t.accent, sw=t.s(12), rx=t.s(8), opacity=0.85, filt=bloom)
        self.svg.rect(left, top, box_w, box_h, fill=t.chip, stroke="none", sw=0, rx=t.s(8), opacity=0.92)
        self.svg.rect(left, top, box_w, box_h, fill="none", stroke=peak, sw=max(1.4, t.s(1.4)), rx=t.s(8), opacity=1)
        baseline = top + pad_y + cap
        self.text(label, left + box_w / 2, baseline, size, t.accent_ink, weight="bold", anchor="middle", role="badge", bg=t.chip)

    def watermark(self, cx: float, cy: float) -> None:
        size = self.theme.s(78)
        self.svg.text(
            "EXAMPLE", cx, cy, size, self.theme.muted, family("condensed"),
            anchor="middle", opacity=0.16, rotate=-14, weight="700",
        )

    def _peak(self, color: str) -> str:
        if self.theme.name in {"light", "contrast"}:
            return self.theme.accent
        named = color.upper()
        if named == self.theme.danger.upper():
            return "#FFE7C2"
        if named == self.theme.sell.upper():
            return "#E7FFF6"
        if named == self.theme.blue.upper():
            return "#D9E8FF"
        return "#B8FFFF"

    def _blur(self) -> str:
        return self.svg.ensure_glow(self.theme.glow_std())

    def glow_line(self, x1, y1, x2, y2, color, sw=2.5, dash=None) -> None:
        filt = self._blur()
        wash = max(self.theme.wash_px(), sw)
        self.svg.line(x1, y1, x2, y2, color, sw=wash, dash=dash, opacity=0.85, filt=filt)
        self.svg.line(x1, y1, x2, y2, self._peak(color), sw=max(1.6, self.theme.s(1.6)), dash=dash, opacity=1)

    def glow_polyline(self, points, color, sw=3) -> None:
        filt = self._blur()
        wash = max(self.theme.wash_px() * 0.75, sw)
        self.svg.polyline(points, color, sw=wash, opacity=0.85, filt=filt)
        self.svg.polyline(points, self._peak(color), sw=max(1.6, self.theme.s(1.6)), opacity=1)

    def glow_rect(self, x, y, w, h, color, rx=4) -> None:
        filt = self._blur()
        self.svg.rect(x, y, w, h, fill=color, rx=rx, opacity=0.7, filt=filt)
        self.svg.rect(x, y, w, h, fill=color, stroke=self._peak(color), sw=max(1.5, self.theme.s(1.4)), rx=rx, opacity=1)

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
