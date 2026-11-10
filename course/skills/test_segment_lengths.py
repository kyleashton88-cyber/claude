"""Holds must stay at or under 7.5 seconds, which is inside the 8 second QA limit."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import elite_motion


def test_short_beat_is_one_piece():
    assert elite_motion.segment_lengths(2.0) == [2.0]


def test_long_beat_has_no_piece_over_the_limit():
    for seconds in (3.17, 8.1, 15, 22.5, 45.31, 71.9, 120):
        parts = elite_motion.segment_lengths(seconds)
        assert parts, seconds
        assert abs(sum(parts) - seconds) < 1e-6
        assert max(parts) <= elite_motion.MAX_HOLD + 1e-6
        assert max(parts) < 3.17


def test_min_seconds_extends_a_short_line():
    assert elite_motion.segment_lengths(18.8)
    # Imported lazily so the renderer and the motion helper stay separate.
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "render"))
    from render_tutorial import beat_seconds
    got = beat_seconds({"role": "body", "vo": "One line.", "min_seconds": 18.8})
    assert got == 18.8


def test_example_stills_exist():
    for kind in (
        "chart-path", "chart-day", "chart-two",
        "analogy-map", "analogy-list", "analogy-shelf",
        "analogy-breaker", "analogy-bridges", "analogy-line", "analogy-card",
    ):
        path = elite_motion.example_png(kind)
        assert path.is_file(), path
        assert path.stat().st_size > 1000


if __name__ == "__main__":
    test_short_beat_is_one_piece()
    test_long_beat_has_no_piece_over_the_limit()
    test_min_seconds_extends_a_short_line()
    test_example_stills_exist()
    print("ok")
