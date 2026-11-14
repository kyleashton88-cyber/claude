#!/usr/bin/env python3
"""Write one numbers file per Blueprint lesson from the public price series.

The quality gate compares on-screen figures with this file. The figures come
from course/data/public-prices/btc-usd-windows.json and the constants in
lesson_scripts.py, not from a copy of the on-screen text.
"""

from __future__ import annotations

import importlib.util
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "skills/video-production/quality-gate"))
from gate.numbers import find_dates  # noqa: E402

PRICES = json.loads((ROOT / "course/data/public-prices/btc-usd-windows.json").read_text())
OUT = Path(__file__).resolve().parent / "numbers"
LESSONS = (
    "bp-01-introduction",
    "bp-02-what-you-need",
    "bp-03-what-is-a-grid-bot",
)


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _rounded(series: list[dict]) -> set[str]:
    found = set()
    for row in series:
        for key in ("high", "low", "close"):
            found.add(str(int(round(float(row[key])))))
    return found


def main() -> None:
    lesson_scripts = _load("lesson_scripts", ROOT / "course/blueprint-rework/lesson_scripts.py")
    studio = _load("studio", Path(__file__).resolve().parent / "studio.py")
    summer = PRICES["range_2023"]
    low = int(round(min(float(row["low"]) for row in summer)))
    high = int(round(max(float(row["high"]) for row in summer)))
    if (low, high) != (lesson_scripts.LOW, lesson_scripts.HIGH):
        raise SystemExit(
            f"script band {lesson_scripts.LOW}-{lesson_scripts.HIGH} "
            f"does not match the public series {low}-{high}"
        )
    span = high - low
    gaps = 6
    step = int(round(span / gaps))
    OUT.mkdir(parents=True, exist_ok=True)
    for sid in LESSONS:
        shots = lesson_scripts.build(sid)
        windows = {shot.get("chart") for shot in shots if shot.get("chart")}
        valid = set()
        years = set()
        for name in windows:
            rows = PRICES.get(name)
            if not isinstance(rows, list):
                continue
            valid |= _rounded(rows)
            for row in rows:
                date = str(row.get("date") or "")
                if len(date) >= 4 and date[:4].isdigit():
                    years.add(date[:4])
                hi_i = int(round(float(row["high"])))
                lo_i = int(round(float(row["low"])))
                valid.add(str(hi_i - lo_i))
        valid.update(str(level) for level in lesson_scripts.LEVELS)
        valid.add(str(low))
        valid.add(str(high))
        valid.add(str(step))
        # Round thousands inside the band are the tidy box the lesson rejects.
        for thousands in range((low // 1000) * 1000, high + 1, 1000):
            if low <= thousands <= high:
                valid.add(str(thousands))
        valid |= years
        spoken = " ".join(shot.get("vo") or "" for shot in shots)
        for token in re.findall(r"\b\d{3,6}\b", spoken):
            if token not in valid:
                raise SystemExit(f"{sid} says {token}, which is not in the public price series or the measured gap")
        labels = sorted(valid, key=lambda item: int(item))
        # Lesson numbers are on the title card. They are not prices.
        labels.append(sid.split("-")[1])
        spoken_blob = "\n".join(
            f"{shot.get('vo') or ''}\n{shot.get('caption') or ''}" for shot in shots
        )
        dates = find_dates(spoken_blob)
        text = [
            f"id: {sid}",
            "format: blueprint",
            "source: course/data/public-prices/btc-usd-windows.json",
            f"disclaimer_spoken: {json.dumps(studio.DISCLAIMER)}",
            'disclaimer_on_screen: "Education only. Not financial advice."',
            "dates:",
        ]
        text.extend(f"  - {json.dumps(phrase)}" for phrase in dates)
        text.append("chart_labels:")
        text.extend(f"  - {json.dumps(label)}" for label in labels)
        text.append("")
        dest = OUT / f"{sid}.yaml"
        dest.write_text("\n".join(text))
        print(f"WROTE {dest} labels {len(labels)} windows {sorted(windows)}")


if __name__ == "__main__":
    main()
