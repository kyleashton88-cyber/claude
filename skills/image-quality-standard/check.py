#!/usr/bin/env python3
"""Technical measurements for the image quality standard.

This does not score appeal. Category scores are human_required.
Run: python3 skills/image-quality-standard/check.py <png or directory>
"""

from __future__ import annotations

import json
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

from PIL import Image

HOUSE = {
    "cyan": (0, 212, 255),
    "blue": (30, 123, 255),
    "mint": (79, 209, 165),
    "amber": (255, 176, 32),
    "white": (244, 248, 252),
    "navy": (0, 15, 42),
}


def _luma(red: int, green: int, blue: int) -> float:
    return 0.2126 * red + 0.7152 * green + 0.0722 * blue


def _chroma(red: int, green: int, blue: int) -> int:
    return max(red, green, blue) - min(red, green, blue)


def _near(color: tuple[int, int, int], target: tuple[int, int, int], tol: int = 48) -> bool:
    return sum(abs(a - b) for a, b in zip(color, target)) <= tol * 3


def measure(png: Path) -> dict:
    image = Image.open(png).convert("RGB")
    width, height = image.size
    raw = image.tobytes()
    margin = max(8, int(round(min(width, height) * 0.04)))
    edge = 0
    edge_total = 0
    ink = 0
    total = 0
    saturated = 0
    off_brand = 0
    step = 3
    for y in range(0, height, step):
        row = y * width * 3
        for x in range(0, width, step):
            index = row + x * 3
            red, green, blue = raw[index], raw[index + 1], raw[index + 2]
            total += 1
            bright = _luma(red, green, blue) > 28 or _chroma(red, green, blue) > 28
            if bright:
                ink += 1
            on_edge = x < margin or y < margin or x >= width - margin or y >= height - margin
            if on_edge:
                edge_total += 1
                if bright:
                    edge += 1
            if _chroma(red, green, blue) > 50 and _luma(red, green, blue) > 40:
                saturated += 1
                color = (red, green, blue)
                allowed = any(_near(color, HOUSE[name]) for name in ("cyan", "blue", "mint", "amber", "white"))
                if not allowed:
                    off_brand += 1
    svg = png.with_suffix(".svg")
    words = _svg_words(svg) if svg.is_file() else []
    spelling = {
        "status": "human_required",
        "reason": "No OCR binary is installed. Review these SVG words for misspellings.",
        "svg_words": words,
    }
    edge_ratio = edge / max(edge_total, 1)
    return {
        "file": str(png),
        "size": [width, height],
        "automated": {
            "contrast_proxy": "human_required on the rendered type; technical preflight lives in the engine",
            "margins": {
                "outer_band_px": margin,
                "bright_share_of_band": round(edge_ratio, 3),
                "cramped": edge_ratio > 0.08,
            },
            "fill": round(ink / max(total, 1), 3),
            "legibility": {
                "status": "human_required",
                "note": "Font size and weight are an engine preflight. Reading the plate is a human score.",
            },
            "palette": {
                "saturated_pixels": saturated,
                "off_brand_share": round(off_brand / max(saturated, 1), 3),
                "off_brand_flag": off_brand / max(saturated, 1) > 0.35 and saturated > 40,
            },
            "spelling": spelling,
        },
        "human_required": [
            "beginner_clarity",
            "composition_hierarchy",
            "craft_polish",
            "brand_fidelity",
            "text_legibility",
            "character_consistency",
            "label_accuracy",
        ],
        "pass": None,
        "note": "This report does not pass or fail the rubric. A human score under 4, or any hard fail, fails the plate.",
    }


def _svg_words(path: Path) -> list[str]:
    try:
        root = ET.parse(path).getroot()
    except ET.ParseError:
        return []
    words = []
    for node in root.iter():
        if node.tag.endswith("text") and node.text:
            words.extend(node.text.split())
    return words


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: python3 skills/image-quality-standard/check.py <png-or-directory>", file=sys.stderr)
        return 2
    target = Path(argv[1])
    paths = sorted(target.rglob("*.png")) if target.is_dir() else [target]
    paths = [path for path in paths if path.is_file() and ".partial" not in path.parts]
    reports = [measure(path) for path in paths]
    json.dump(reports if target.is_dir() else reports[0], sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
