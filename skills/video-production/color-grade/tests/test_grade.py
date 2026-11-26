"""Unit tests for the procedural LUTs. No video encode."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import numpy as np

from grade.lut import LOOKS, apply_look, generate_cube, parse_cube


class LutTests(unittest.TestCase):
    def test_cube_shape_and_bounds(self):
        for spec in LOOKS.values():
            text = generate_cube(spec, 17)
            size, table = parse_cube(text)
            self.assertEqual(size, 17)
            self.assertTrue(np.all(table >= 0.0))
            self.assertTrue(np.all(table <= 1.0))

    def test_gray_ramp_luma_rises(self):
        ramp = np.linspace(0.05, 0.95, 12).astype(np.float32)
        for spec in LOOKS.values():
            r, g, b = apply_look(ramp.copy(), ramp.copy(), ramp.copy(), spec)
            y = 0.2126 * r + 0.7152 * g + 0.0722 * b
            self.assertTrue(np.all(np.diff(y) > 0), spec["title"])

    def test_skin_hue_stays_put_under_the_warm_look(self):
        skin = np.array([0.84, 0.61, 0.49], dtype=np.float32)
        r, g, b = apply_look(skin[:1].copy(), skin[1:2].copy(), skin[2:3].copy(), LOOKS["warm-talking-head"])

        def hue(rr, gg, bb):
            mx = max(rr, gg, bb)
            mn = min(rr, gg, bb)
            df = mx - mn
            if mx == rr:
                h = ((gg - bb) / df) % 6
            elif mx == gg:
                h = (bb - rr) / df + 2
            else:
                h = (rr - gg) / df + 4
            return (h * 60) % 360

        before = hue(*skin.tolist())
        after = hue(float(r[0]), float(g[0]), float(b[0]))
        delta = min(abs(after - before), 360 - abs(after - before))
        self.assertLess(delta, 8.0, f"skin hue moved {delta:.2f} degrees")


if __name__ == "__main__":
    unittest.main()
