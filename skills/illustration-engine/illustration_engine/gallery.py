"""Build the checked test gallery: three plates per type, every preset, one lesson."""

from __future__ import annotations

from pathlib import Path

from .batch import render_lesson, write_reports
from .contact import contact_sheet, side_by_side
from .render import RenderResult, render_spec
from .spec import Spec

# Three plates for every visual type. One of them is also rendered in every preset.
GALLERY: list[tuple[str, dict]] = [
    ("candle_anatomy", {"variant": "bull"}),
    ("candle_anatomy", {"variant": "bear"}),
    ("candle_anatomy", {"variant": "wick"}),
    ("candle_series", {"seed": 1, "count": 14}),
    ("candle_series", {"seed": 2, "count": 16}),
    ("candle_series", {"seed": 7, "count": 12}),
    ("candle_pattern", {"variant": "hammer"}),
    ("candle_pattern", {"variant": "doji"}),
    ("candle_pattern", {"variant": "engulfing"}),
    ("grid_ladder", {"low": 90, "high": 110, "grids": 10, "price": 100, "labels": ["BUY", "SELL", "PRICE"]}),
    ("grid_ladder", {"low": 80, "high": 120, "grids": 6, "price": 95, "labels": ["BUY", "SELL", "FILL"]}),
    ("grid_ladder", {"low": 40, "high": 70, "grids": 8, "price": 62, "labels": ["BUY", "SELL", "PRICE"]}),
    ("liquidation", {"entry": 100, "liquidation": 80, "price": 88, "leverage": 5}),
    ("liquidation", {"entry": 100, "liquidation": 92, "price": 98, "leverage": 10}),
    ("liquidation", {"entry": 50, "liquidation": 40, "price": 41, "leverage": 3}),
    ("price_range", {"variant": "inside", "headline": "THE RANGE", "labels": ["UPPER", "LOWER", "RANGE"]}),
    ("price_range", {"variant": "touch", "headline": "TAG SUPPORT", "labels": ["SUPPORT", "RANGE", "HOLD"]}),
    ("price_range", {"variant": "leave", "headline": "LEAVES THE BAND", "labels": ["UPPER", "LOWER", "OUT"]}),
    ("flowchart", {"headline": "THE PATH", "labels": ["RANGE", "LEVELS", "STOP"]}),
    ("flowchart", {"headline": "A REVIEW", "labels": ["LOOK", "NOTE", "DECIDE"]}),
    ("flowchart", {"headline": "PAPER FIRST", "labels": ["WRITE", "CHECK", "WAIT"]}),
    ("comparison", {"headline": "TWO WAYS", "labels": ["CLEAR", "MISS"], "variant": "shown"}),
    ("comparison", {"headline": "INSIDE OUTSIDE", "labels": ["INSIDE", "OUTSIDE"], "variant": "shown"}),
    ("comparison", {"headline": "NO RESULT", "labels": ["NUMBER", "SHAPE"], "variant": "plain"}),
    ("steps", {"headline": "THREE PARTS", "labels": ["RANGE", "LEVELS", "STOP"]}),
    ("steps", {"headline": "BEFORE A CLICK", "labels": ["WRITE", "CHECK", "WAIT"]}),
    ("steps", {"headline": "THE RECAP", "labels": ["RANGE", "LEVELS", "STOP"]}),
    ("analogy_fence", {"headline": "THE FENCE", "labels": ["INSIDE", "FENCE", "PRACTICE"]}),
    ("analogy_fence", {"headline": "STAY INSIDE", "labels": ["RAIL", "PATH", "INSIDE"]}),
    ("analogy_fence", {"headline": "PRACTICE FENCE", "labels": ["PRACTICE", "FENCE", "EDGE"]}),
    ("analogy_ladder", {"headline": "THE LADDER", "labels": ["RUNG", "LEVEL", "WAIT"], "highlight": 2}),
    ("analogy_ladder", {"headline": "NEXT RUNG", "labels": ["NEXT", "RUNG", "WAIT"], "highlight": 1}),
    ("analogy_ladder", {"headline": "EVEN RUNGS", "labels": ["EVEN", "RUNG", "GAP"], "highlight": 4}),
    ("analogy_buckets", {"variant": "apart", "headline": "TWO BUCKETS", "labels": ["APART", "LEFT", "RIGHT"]}),
    ("analogy_buckets", {"variant": "overlap", "headline": "OVERLAP", "labels": ["OVERLAP", "LEFT", "RIGHT"]}),
    ("analogy_buckets", {"variant": "empty", "headline": "ONE LIGHT", "labels": ["LIGHT", "FULL", "BUCKET"]}),
    ("checklist", {"headline": "ON PAPER", "labels": ["RANGE", "LEVELS", "STOP"], "highlight": 0}),
    ("checklist", {"headline": "THE LIST", "labels": ["WRITE", "CHECK", "WAIT"], "highlight": 1}),
    ("checklist", {"headline": "BEFORE SCREEN", "labels": ["PAPER", "PLAN", "PAUSE"], "highlight": 2}),
    ("mascot_scene", {"pose": "pointing", "headline": "LOOK HERE", "labels": ["POINT", "RANGE"]}),
    ("mascot_scene", {"pose": "thinking", "headline": "THINK FIRST", "labels": ["THINK", "CHECK"]}),
    ("mascot_scene", {"pose": "warning", "headline": "CHECK FIRST", "labels": ["WAIT", "CHECK"]}),
    ("mascot_scene", {"pose": "celebrating", "headline": "STEP DONE", "labels": ["DONE", "NEXT"]}),
    ("title_card", {"title": "INTRODUCTION", "labels": ["START", "HERE"]}),
    ("title_card", {"title": "THE RANGE", "labels": ["TOP", "BOTTOM"]}),
    ("title_card", {"title": "NEXT STEP", "labels": ["NEXT", "PAGE"]}),
    ("lesson_cover", {"title": "THE RANGE", "labels": ["LESSON", "START"]}),
    ("lesson_cover", {"title": "LEVELS", "labels": ["LESSON", "RUNGS"]}),
    ("lesson_cover", {"title": "A STOP", "labels": ["LESSON", "LINE"]}),
    ("section_divider", {"title": "NEXT", "labels": ["PART", "NEXT"]}),
    ("section_divider", {"title": "RANGE", "labels": ["PART", "RANGE"]}),
    ("section_divider", {"title": "PRACTICE", "labels": ["PART", "PAPER"]}),
]

PRESET_EXAMPLE = {
    "type": "grid_ladder",
    "params": {"low": 90, "high": 110, "grids": 10, "price": 100, "headline": "GRID LADDER", "labels": ["BUY", "SELL", "PRICE"]},
}


def repo_root() -> Path | None:
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "IMAGE_REQUESTS.json").is_file():
            return parent
    return None


def build_gallery(out_dir: Path, requests: Path | None = None, lesson: str = "bp-01-introduction",
                  originals: Path | None = None, strict: bool = True) -> None:
    out_dir = out_dir.resolve()
    if "course" in out_dir.parts:
        raise SystemExit("refusing to write the gallery into a course path")
    grouped: dict[str, list[tuple[dict, RenderResult]]] = {}
    flat: list[tuple[str, RenderResult]] = []
    sheet_items: list[tuple[Path, str]] = []
    for kind, params in GALLERY:
        grouped.setdefault(kind, [])
        index = len(grouped[kind]) + 1
        spec = Spec(type=kind, params=dict(params), preset="house", headline=params.get("headline"), labels=params.get("labels"))
        dest = out_dir / "types" / kind / f"{index:02d}.png"
        result = render_spec(spec, dest, preset="house", strict=strict)
        grouped[kind].append((params, result))
        flat.append((f"types/{kind}/{index:02d}.png", result))
        sheet_items.append((dest, f"{kind} {index}"))
        print(f"type {kind} {index}")
    preset_params = dict(PRESET_EXAMPLE["params"])
    for name in ("house", "light", "contrast", "thumbnail", "elite"):
        spec = Spec(type="grid_ladder", params=dict(preset_params), preset=name)
        dest = out_dir / "presets" / f"{name}.png"
        result = render_spec(spec, dest, preset=name, strict=strict)
        flat.append((f"presets/{name}.png", result))
        sheet_items.append((dest, f"preset {name}"))
        print(f"preset {name}")
    root = repo_root()
    request_path = requests or (root / "IMAGE_REQUESTS.json" if root else None)
    if request_path and request_path.is_file():
        lesson_dir = out_dir / "batch" / lesson
        render_lesson(request_path, lesson_dir, lesson=lesson, preset="house", strict=strict)
        for png in sorted(lesson_dir.glob("*.png")):
            sheet_items.append((png, f"{lesson} {png.stem}"))
        original_dir = originals or (root / "course" / "images" / lesson if root else None)
        if original_dir and original_dir.is_dir():
            for png in sorted(lesson_dir.glob("*.png")):
                source = original_dir / png.name
                if source.is_file():
                    side_by_side(source, png, out_dir / "compare" / png.name)
                    print(f"compare {png.name}")
    contact_sheet(sheet_items, out_dir / "contact-sheet.png", columns=4)
    write_reports(out_dir, flat)
    print(f"contact {out_dir / 'contact-sheet.png'}")
