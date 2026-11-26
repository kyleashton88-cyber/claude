"""Fail a frame when a cyan label bar covers teaching, or a chip covers a header.

The bar used to be drawn after the card, at a fixed y of 520 or 620, with no
record of the prices and list rows already on the card. That is why it sat on
24,930, on axis labels, and on recap rows. The bar now lives in one lane under
the card. This check is what stops it moving back onto the card.
"""

from __future__ import annotations


def intersects(a: tuple[float, float, float, float], b: tuple[float, float, float, float]) -> bool:
    return a[0] < b[2] and a[2] > b[0] and a[1] < b[3] and a[3] > b[1]


def _center(box: tuple[float, float, float, float]) -> tuple[float, float]:
    return ((box[0] + box[2]) / 2, (box[1] + box[3]) / 2)


def _inside(outer: tuple[float, float, float, float], box: tuple[float, float, float, float]) -> bool:
    cx, cy = _center(box)
    return outer[0] <= cx <= outer[2] and outer[1] <= cy <= outer[3]


def _cyan(fill) -> bool:
    if not isinstance(fill, tuple) or len(fill) < 3:
        return False
    red, green, blue = fill[:3]
    return red < 40 and green > 160 and blue > 200


class LayoutLog:
    def __init__(self) -> None:
        self.texts: list[tuple[tuple[float, float, float, float], str]] = []
        self.bars: list[tuple[float, float, float, float]] = []
        self.chips: list[tuple[float, float, float, float]] = []
        self.diagrams: list[tuple[float, float, float, float]] = []

    def text(self, box: tuple[float, float, float, float], text: str, size: int = 32) -> None:
        self.texts.append((box, " ".join(text.split()), int(size)))

    def shape(self, box: tuple[float, float, float, float], fill, kind: str) -> None:
        x0, y0, x1, y1 = box
        width, height = abs(x1 - x0), abs(y1 - y0)
        ordered = (min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1))
        if _cyan(fill) and width >= 500 and 28 <= height <= 100:
            self.bars.append(ordered)

    def diagram(self, box: tuple[float, float, float, float]) -> None:
        x0, y0, x1, y1 = box
        ordered = (min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1))
        if ordered[2] - ordered[0] < 8 and ordered[3] - ordered[1] < 8:
            return
        self.diagrams.append(ordered)

    def problems(self) -> list[str]:
        found: list[str] = []
        for bar in self.bars:
            for box, text, _size in self.texts:
                if not text or _inside(bar, box):
                    continue
                if intersects(bar, box):
                    found.append(f"cyan bar covers text: {text[:80]}")
            for box in self.diagrams:
                # A line whose centre sits inside the bar is still covered.
                # The label may sit in the bar. The diagram may not.
                if intersects(bar, box):
                    found.append("cyan bar covers a diagram line")
                    break
        for box, text, size in self.texts:
            if len(text.strip()) >= 3 and size < 28:
                found.append(f"text under 28px: {text[:40]} at {size}px")
                return found
        for box, text, _size in self.texts:
            if text.upper() != "EXAMPLE":
                continue
            chip = (box[0] - 20, box[1] - 8, box[2] + 20, box[3] + 12)
            for other, other_text, _other_size in self.texts:
                if other_text.upper() == "EXAMPLE":
                    continue
                if intersects(chip, other):
                    found.append(f"EXAMPLE chip covers header: {other_text[:80]}")
        seen: dict[str, int] = {}
        for _box, text, _size in self.texts:
            key = text.strip().lower()
            if len(key) < 40 or key == "example":
                continue
            seen[key] = seen.get(key, 0) + 1
        for key, count in seen.items():
            if count > 1:
                found.append(f"sentence repeated {count} times: {key[:80]}")
        # Two different lines of teaching text must not sit on each other.
        for index, (box, text, _size) in enumerate(self.texts):
            if len(text) < 8:
                continue
            for other, other_text, _other_size in self.texts[index + 1:]:
                if len(other_text) < 8 or text == other_text:
                    continue
                if intersects(box, other):
                    found.append(f"text overlaps text: {text[:40]} / {other_text[:40]}")
                    return found
        return found


class TrackingDraw:
    """Records boxes, then draws. Unknown calls go straight to Pillow."""

    def __init__(self, inner, log: LayoutLog) -> None:
        self._inner = inner
        self._log = log

    def text(self, xy, text, font=None, fill=None, **kwargs):
        self._inner.text(xy, text, font=font, fill=fill, **kwargs)
        if not text:
            return
        x, y = xy
        if font is None:
            width, height = len(str(text)) * 8, 16
        else:
            width = int(font.getlength(str(text)))
            height = int(getattr(font, "size", 32))
        size = int(getattr(font, "size", 32) or 32)
        self._log.text((x, y, x + width, y + height), str(text), size)

    def rectangle(self, box, fill=None, outline=None, width=1):
        self._inner.rectangle(box, fill=fill, outline=outline, width=width)
        self._log.shape(tuple(box), fill, "rect")

    def rounded_rectangle(self, box, radius=0, fill=None, outline=None, width=1):
        self._inner.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)
        self._log.shape(tuple(box), fill, "round")

    def line(self, xy, fill=None, width=1):
        self._inner.line(xy, fill=fill, width=width)
        if not width or width <= 2 or not xy:
            return
        xs = [point[0] for point in xy]
        ys = [point[1] for point in xy]
        self._log.diagram((min(xs), min(ys), max(xs), max(ys)))

    def __getattr__(self, name):
        return getattr(self._inner, name)
