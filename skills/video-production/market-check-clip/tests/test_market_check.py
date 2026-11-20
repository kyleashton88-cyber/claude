"""Parser tests. The rendered demo is separate and is not required here."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))

from market_check.build_lesson import estimate_seconds, lesson_from_post  # noqa: E402


class MarketCheckTests(unittest.TestCase):
    def test_sample_post_lands_in_the_window(self):
        text = (HERE / "fixtures" / "sample-post.md").read_text(encoding="utf-8")
        lesson = lesson_from_post(text)
        self.assertEqual(lesson["engine"], "kokoro")
        self.assertEqual(lesson["format"], "market-check")
        spoken = " ".join(section["narration"] for section in lesson["sections"]).lower()
        self.assertIn("not financial advice", spoken)
        self.assertIn("education", spoken)
        seconds = estimate_seconds([section["narration"] for section in lesson["sections"]])
        self.assertGreaterEqual(seconds, 60)
        self.assertLessEqual(seconds, 90)
        for section in lesson["sections"]:
            self.assertLessEqual(len(section["narration"].split()), 12)

    def test_missing_disclaimer_is_added(self):
        lesson = lesson_from_post("Price held a range. EXAMPLE 90 and 110.")
        spoken = " ".join(section["narration"] for section in lesson["sections"])
        self.assertIn("not financial advice", spoken.lower())
        self.assertIn("education", spoken.lower())


if __name__ == "__main__":
    unittest.main()
