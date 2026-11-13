import tempfile
import unittest
from pathlib import Path

from illustration_engine.qa import contrast_ratio
from illustration_engine.render import UnsafeOutput, render_prompt
from illustration_engine.theme import PRESETS


class ThemeTests(unittest.TestCase):
    def test_text_pairs_clear_the_floor(self):
        pairs = {
            "house": [("#FFFFFF", "#050A18"), ("#00D4FF", "#050A18"), ("#FFFFFF", "#0B1A30")],
            "light": [("#0A1628", "#F7F9FC"), ("#083344", "#F7F9FC"), ("#0A1628", "#FFFFFF")],
            "contrast": [("#FFFFFF", "#000000"), ("#FFE14A", "#000000")],
            "thumbnail": [("#FFFFFF", "#050A18"), ("#00D4FF", "#050A18")],
        }
        for name, items in pairs.items():
            self.assertIn(name, PRESETS)
            for fg, bg in items:
                self.assertGreaterEqual(contrast_ratio(fg, bg), 4.5, f"{name} {fg} on {bg}")


class RenderTests(unittest.TestCase):
    def test_house_grid_is_the_right_size(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "grid.png"
            result = render_prompt(
                "grid ladder, range 90-110, 10 grids, price 100, label buy and sell",
                dest,
                preset="house",
            )
            self.assertEqual(result.theme.width, 1536)
            self.assertEqual(result.theme.height, 1024)
            self.assertTrue(result.qa.ok, result.qa.failures)
            self.assertGreater(dest.stat().st_size, 1000)
            self.assertTrue(dest.with_suffix(".svg").is_file())
            self.assertIn("EXAMPLE", dest.with_suffix(".svg").read_text(encoding="utf-8"))

    def test_refuses_course_output(self):
        with self.assertRaises(UnsafeOutput):
            render_prompt("title card", Path("/tmp/course/images/x.png"), preset="house")

    def test_each_preset_renders(self):
        with tempfile.TemporaryDirectory() as tmp:
            for name in PRESETS:
                dest = Path(tmp) / f"{name}.png"
                result = render_prompt(
                    "grid ladder, range 90-110, 10 grids, price 100, label buy and sell",
                    dest,
                    preset=name,
                    strict=True,
                )
                self.assertTrue(result.qa.ok, f"{name}: {result.qa.failures}")


if __name__ == "__main__":
    unittest.main()
