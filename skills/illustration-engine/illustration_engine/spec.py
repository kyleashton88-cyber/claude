"""A visual spec is the only thing the renderer accepts.

Pixels are produced later, from this object, by the local drawing code.
"""

from __future__ import annotations

from dataclasses import dataclass, field


TYPES = (
    "candle_anatomy",
    "candle_series",
    "candle_pattern",
    "grid_ladder",
    "liquidation",
    "price_range",
    "flowchart",
    "comparison",
    "steps",
    "analogy_fence",
    "analogy_ladder",
    "analogy_buckets",
    "checklist",
    "mascot_scene",
    "title_card",
    "lesson_cover",
    "section_divider",
)


@dataclass
class Spec:
    type: str
    params: dict = field(default_factory=dict)
    preset: str = "house"
    size: tuple[int, int] | None = None
    headline: str | None = None
    labels: list[str] | None = None
    source_id: str | None = None
    file: str | None = None

    def as_dict(self) -> dict:
        data = {
            "type": self.type,
            "preset": self.preset,
            "params": self.params,
        }
        if self.size:
            data["size"] = f"{self.size[0]}x{self.size[1]}"
        if self.headline:
            data["headline"] = self.headline
        if self.labels:
            data["labels"] = list(self.labels)
        if self.source_id:
            data["source_id"] = self.source_id
        if self.file:
            data["file"] = self.file
        return data
