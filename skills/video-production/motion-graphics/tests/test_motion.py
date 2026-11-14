"""Fast checks for the motion components. The sample movie is produced by cli.py render."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from PIL import Image

from motion.components import fills_at, ken_burns_frame, price_at
from motion.render import sample_sequence, shot_duration


class MotionTests(unittest.TestCase):
    def test_sample_is_a_short_teaching_reel(self):
        sequence = sample_sequence()
        self.assertGreaterEqual(shot_duration(sequence), 20)
        self.assertLessEqual(shot_duration(sequence), 30)
        self.assertEqual(
            [shot["kind"] for shot in sequence["shots"]],
            ["title", "candles", "ladder", "risk", "still"],
        )

    def test_orders_fill_as_price_crosses(self):
        early = fills_at(0.05)
        later = fills_at(0.95)
        self.assertLess(len(early), len(later))
        self.assertGreater(len(later), 0)
        self.assertGreater(price_at(0.0), 110)

    def test_ken_burns_refuses_to_upscale(self):
        tiny = Image.new("RGB", (320, 180), (10, 20, 30))
        with self.assertRaises(ValueError):
            ken_burns_frame(tiny, (0, 0, 320, 180), (1920, 1080))

    def test_sample_copy_has_no_contact_details(self):
        blob = str(sample_sequence()).lower()
        for token in ("@", ".com", " ltd", "llc", "inc."):
            self.assertNotIn(token, blob)


if __name__ == "__main__":
    unittest.main()
