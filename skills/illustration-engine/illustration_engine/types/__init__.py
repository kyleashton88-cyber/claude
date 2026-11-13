"""Visual-type registry. Each drawer paints one idea."""

from __future__ import annotations

from .branded import draw_cover, draw_divider, draw_title
from .candles import draw_anatomy, draw_pattern, draw_series
from .diagrams import draw_buckets, draw_checklist, draw_comparison, draw_fence, draw_flowchart, draw_ladder, draw_steps
from .grid import draw_grid
from .liquidation import draw_liquidation
from .mascot import draw_mascot_scene
from .ranges import draw_range

IDEAS = {
    "candle_anatomy": "One candle, with the body and the wick called out.",
    "candle_series": "A sideways run of candles, marked as an example.",
    "candle_pattern": "One named candle pattern, shown on its own.",
    "grid_ladder": "Buy orders wait below the mark and sell orders wait above it.",
    "liquidation": "A danger band between the entry and the liquidation line.",
    "price_range": "A top and a bottom, with price moving inside the band.",
    "flowchart": "A short path of steps, read from left to right.",
    "comparison": "Two ways to see the same idea, side by side.",
    "steps": "A few numbered steps for one idea.",
    "analogy_fence": "A fence around practice: stay inside the rails.",
    "analogy_ladder": "Rungs are levels that wait. One rung is the next step.",
    "analogy_buckets": "Two separate buckets. Overlap is the thing to notice.",
    "checklist": "A short paper checklist, one row highlighted.",
    "mascot_scene": "The grid bot mascot in one pose, beside one prop.",
    "title_card": "A title card for the lesson, with no extra lockup.",
    "lesson_cover": "A lesson cover: a title and the mascot.",
    "section_divider": "A section divider with one word.",
}

DRAWERS = {
    "candle_anatomy": draw_anatomy,
    "candle_series": draw_series,
    "candle_pattern": draw_pattern,
    "grid_ladder": draw_grid,
    "liquidation": draw_liquidation,
    "price_range": draw_range,
    "flowchart": draw_flowchart,
    "comparison": draw_comparison,
    "steps": draw_steps,
    "analogy_fence": draw_fence,
    "analogy_ladder": draw_ladder,
    "analogy_buckets": draw_buckets,
    "checklist": draw_checklist,
    "mascot_scene": draw_mascot_scene,
    "title_card": draw_title,
    "lesson_cover": draw_cover,
    "section_divider": draw_divider,
}


def draw(canvas, spec) -> None:
    kind = spec.type
    if kind not in DRAWERS:
        raise KeyError(kind)
    canvas.idea = IDEAS[kind]
    DRAWERS[kind](canvas, spec.params or {})
