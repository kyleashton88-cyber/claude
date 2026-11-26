"""Shot list tests."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))

from planner.plan import plan_path  # noqa: E402


class PlannerTests(unittest.TestCase):
    def test_picture_changes_within_eight_seconds(self):
        data = plan_path(HERE / "samples" / "lesson.yaml")
        self.assertGreaterEqual(data["shot_count"], 3)
        durations = [shot["duration"] for shot in data["shots"]]
        self.assertTrue(all(item <= 8.05 for item in durations))
        ladder = [shot for shot in data["shots"] if shot["beat"] == "ladder"]
        self.assertGreaterEqual(len(ladder), 3)
        self.assertEqual(ladder[0]["visual"], "grid ladder")
        self.assertEqual(ladder[0]["engine_type"], "grid_ladder")
        self.assertNotEqual(ladder[1]["visual"], ladder[0]["visual"])
        # Word timings set the clock. The second slice starts when the first would pass 8s.
        self.assertAlmostEqual(ladder[0]["start"], 0.0)
        self.assertAlmostEqual(ladder[0]["end"], 7.2)
        self.assertAlmostEqual(ladder[1]["start"], 7.2)
        self.assertLessEqual(ladder[1]["duration"], 8.0)

    def test_labels_are_short_and_alt_is_present(self):
        data = plan_path(HERE / "samples" / "lesson.yaml")
        for shot in data["shots"]:
            self.assertLessEqual(len(shot["labels"]), 4)
            for label in shot["labels"]:
                self.assertLessEqual(len(label.split()), 3)
            self.assertIn(shot["idea"], shot["alt"])
            self.assertNotIn(".", shot["idea"])

    def test_candle_visual(self):
        data = plan_path(HERE / "samples" / "lesson.yaml")
        first = data["shots"][0]
        self.assertEqual(first["visual"], "candle chart")
        self.assertEqual(first["engine_type"], "candle_series")
        self.assertEqual(first["duration"], 3.0)


if __name__ == "__main__":
    unittest.main()
