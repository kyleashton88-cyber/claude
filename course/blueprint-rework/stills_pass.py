"""Second pass: ChatGPT analogy stills, a tighter real-date walk, label skip.

Writes course/masters-stills/. Does not delete course/masters-v2/.
Refuses Elite ids. Does not merge anything.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "course/skills"))

STILLS = {
    "ladder": ROOT / "course/images/blueprint-analogies/analogy-ladder.png",
    "fence": ROOT / "course/images/blueprint-analogies/analogy-fence.png",
    "list": ROOT / "course/images/blueprint-analogies/analogy-list.png",
    "buckets": ROOT / "course/images/blueprint-analogies/analogy-buckets.png",
}
OUT = ROOT / "course/masters-stills"

# Fewer stops than the every-fourth-day walk. Every date is in the public series.
KEYS = {
    "range_2023": [
        "2023-07-19", "2023-07-29", "2023-08-08", "2023-08-18", "2023-08-28",
        "2023-09-07", "2023-09-17", "2023-09-27", "2023-10-07", "2023-10-16",
    ],
    "breakout_2023": [
        "2023-10-16", "2023-10-23", "2023-10-30", "2023-11-13", "2023-12-11",
        "2023-12-25", "2024-01-08", "2024-01-22", "2024-02-19", "2024-03-14",
    ],
    "crash_2020": [
        "2020-02-20", "2020-03-06", "2020-03-09", "2020-03-11",
        "2020-03-12", "2020-03-13", "2020-03-16", "2020-03-20",
    ],
    "second_range_2024": [
        "2024-03-27", "2024-04-06", "2024-04-16", "2024-04-26", "2024-05-06",
        "2024-05-16", "2024-05-26", "2024-06-05", "2024-06-15", "2024-06-24",
    ],
}

NOTES = [
    "Ask which rail is closer, the low or the high, and write that on the page.",
    "Ask whether this close is on the buy side or the sell side of 27630 in the example picture.",
    "Ask whether this day's own high-to-low range fits inside one gap of about 900 dollars.",
    "Ask whether the stop sentence would already have ended the summer idea by this date.",
]


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


ls = _load("lesson_scripts", ROOT / "course/blueprint-rework/lesson_scripts.py")
motion = _load("render_motion", ROOT / "course/blueprint-rework/render_motion.py")


def _row(chart: str, iso: str) -> dict | None:
    for row in ls.PRICES[chart]:
        if row["date"] == iso:
            return row
    return None


def _key_shots(chart: str, chapter: str, title: str) -> list[dict]:
    band = (24930, 30331) if chart != "crash_2020" else None
    if chart == "second_range_2024":
        band = (56555, 72715)
    shots = []
    prev_close = None
    prev_reveal = 0.0
    series = ls.PRICES[chart]
    for n, iso in enumerate(KEYS[chart]):
        row = _row(chart, iso)
        if row is None:
            continue
        idx = next(i for i, r in enumerate(series) if r["date"] == iso)
        reveal = idx / (len(series) - 1)
        close = int(round(row["close"]))
        high = int(round(row["high"]))
        low = int(round(row["low"]))
        nearest = min(ls.LEVELS, key=lambda lv: abs(lv - close))
        parts = [
            f"Stop on {ls.pretty(iso)}. The public daily close was {close}.",
            f"The low that day was {low} and the high was {high}.",
        ]
        if prev_close is not None:
            delta = close - prev_close
            way = "higher" if delta >= 0 else "lower"
            parts.append(f"Since the last stop, the close is {abs(delta)} dollars {way}.")
        if band and chart != "second_range_2024":
            if band[0] <= close <= band[1]:
                parts.append(
                    f"The close is still inside 24930 to 30331. "
                    f"It is {close - 24930} dollars above the low and {30331 - close} dollars under the high."
                )
            else:
                parts.append(
                    "The close is outside 24930 to 30331. "
                    "The summer idea is finished if your stop sentence says the path must return, and it has not."
                )
        elif chart == "second_range_2024":
            parts.append(
                f"This is page two's window, not the summer band. "
                f"The close is {close - 56555} dollars above 56555 and {72715 - close} dollars under 72715."
            )
        else:
            parts.append(
                f"This is the 2020 path. The nearest summer rung, {nearest}, is not a rung you lay across these days."
            )
        parts.append(NOTES[n % len(NOTES)])
        parts.append(
            f"The day's range, high minus low, is {high - low} dollars. "
            f"One example gap is about 900 dollars. "
            f"{'This day is wider than one gap.' if high - low > 900 else 'This day fits inside one gap.'} "
            "Marked Example. Not a fill. Not a forecast."
        )
        shots.append(ls._shot(
            kind="chart",
            chart=chart,
            chapter=chapter,
            chart_title=title,
            reveal_from=prev_reveal,
            reveal=max(reveal, prev_reveal + 0.01),
            vo=" ".join(parts),
            caption=f"{ls.pretty(iso)}. Close {close:,}.",
            levels=ls.LEVELS if chart != "crash_2020" else [],
            focus_price=nearest if chart != "crash_2020" else None,
            focus_label=f"{nearest:,}" if chart != "crash_2020" else "",
        ))
        shots.append(ls._shot(
            kind="chart",
            chart=chart,
            chapter=chapter,
            chart_title=title,
            reveal_from=reveal,
            reveal=max(reveal, prev_reveal + 0.01),
            vo=(
                f"Read {ls.pretty(iso)} back in one breath. Close {close}. "
                f"Low {low}. High {high}. Nearest rung {nearest}. "
                f"{NOTES[(n + 1) % len(NOTES)]} "
                "Then cover the caption and say the date before you move the playhead. "
                "The point of the stop is that you can find this day again on the public series."
            ),
            caption=f"Say it back. {ls.pretty(iso)}.",
            levels=ls.LEVELS if chart != "crash_2020" else [],
            focus_price=nearest if chart != "crash_2020" else None,
            focus_label=f"{nearest:,}" if chart != "crash_2020" else "",
        ))
        prev_close = close
        prev_reveal = reveal
    return shots


WALK = {
    "Walk the summer": ("range_2023", "Summer stops", "19 July 2023 to 16 October 2023"),
    "Copy the path": ("range_2023", "Page stops", "Figures you copy"),
    "Where the path stood": ("range_2023", "Path stops", "Where the close stood"),
    "Recount against the path": ("range_2023", "Recount stops", "Rails against the close"),
    "Read the figures aloud": ("range_2023", "Read the stops", "Read the real close"),
    "A cadence through the band": ("range_2023", "Check stops", "The three questions on a real day"),
    "Audit the path": ("range_2023", "Audit stops", "Does the page match this close?"),
    "The spot page beside it": ("range_2023", "Spot stops", "The spot page beside the crash"),
    "Walk the leave": ("breakout_2023", "Leave stops", "After 16 October 2023"),
    "Point at the leave": ("breakout_2023", "Finish stops", "The finish sentence on real closes"),
    "Walk page two": ("second_range_2024", "Page two stops", "27 March 2024 to 24 June 2024"),
    "Walk the drop": ("crash_2020", "Drop stops", "February and March 2020"),
}


def prepare(shots: list[dict]) -> list[dict]:
    out = []
    i = 0
    while i < len(shots):
        chapter = shots[i]["chapter"]
        if chapter in WALK:
            chart, new_chapter, title = WALK[chapter]
            while i < len(shots) and shots[i]["chapter"] == chapter:
                i += 1
            out.extend(_key_shots(chart, new_chapter, title))
            continue
        shot = shots[i]
        if shot.get("kind") == "analogy":
            shot["still"] = str(STILLS[shot.get("analogy") or "ladder"])
        out.append(shot)
        i += 1
    return out


def words_of(sid: str) -> int:
    shots = prepare(ls.build(sid))
    return sum(len(s["vo"].split()) for s in shots)


def main() -> None:
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--id", required=True)
    ap.add_argument("--count", action="store_true")
    args = ap.parse_args()
    if args.id.startswith("el-"):
        raise SystemExit("refusing Elite id")
    if args.count:
        print(args.id, words_of(args.id))
        return
    OUT.mkdir(parents=True, exist_ok=True)
    motion.render(args.id, proof=False, out_dir=OUT, prepare_shots=prepare)


if __name__ == "__main__":
    main()
