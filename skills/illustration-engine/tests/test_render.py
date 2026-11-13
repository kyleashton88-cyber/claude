import tempfile
import unittest
from pathlib import Path

from illustration_engine.qa import contrast_ratio
from illustration_engine.render import UnsafeOutput, render_prompt
from illustration_engine.theme import PRESET_NAMES, get_theme


class ThemeTests(unittest.TestCase):
    def test_text_pairs_clear_the_floor(self):
        pairs = {
            "house": [("#F4F8FC", "#00081B"), ("#00D4FF", "#00081B"), ("#F4F8FC", "#060E1E")],
            "light": [("#0A1628", "#F4F7FB"), ("#083344", "#F7F9FC"), ("#0A1628", "#FFFFFF")],
            "contrast": [("#FFFFFF", "#000000"), ("#FFE14A", "#000000")],
            "thumbnail": [("#F4F8FC", "#00081B"), ("#00D4FF", "#00081B")],
            "elite": [("#F4F8FC", "#05080F"), ("#14E0C8", "#05080F"), ("#4FD1A5", "#05080F")],
        }
        for name, items in pairs.items():
            self.assertIn(name, PRESET_NAMES)
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
            self.assertTrue(all(mark["family"] == "Roboto Condensed" for mark in result.meta["marks"] if mark["role"] == "headline"))
            floor = 24 * result.theme.scale
            labels = [mark for mark in result.meta["marks"] if mark["role"] == "label"]
            self.assertTrue(labels)
            self.assertTrue(all(mark["size"] + 0.1 >= floor for mark in labels))
            svg = dest.with_suffix(".svg").read_text(encoding="utf-8")
            self.assertIn('font-weight: 700', svg)
            self.assertIn('font-weight="700"', svg)
            self.assertNotIn("1.18", svg)
            self.assertIn("stdDeviation=\"10\"", svg)
            stem = next(line for line in result.qa.checks if "stem width" in line)
            self.assertTrue(stem.startswith("pass"), stem)

    def test_canvas_sizes_scale_type(self):
        from illustration_engine.theme import get_theme
        for width, height, headline, label in (
            (1280, 720, 74, 28),
            (1536, 1024, 89, 34),
            (1920, 1080, 111, 42),
        ):
            theme = get_theme("house", (width, height))
            self.assertEqual((theme.width, theme.height), (width, height))
            self.assertEqual(theme.headline, headline)
            self.assertEqual(theme.label, label)
            self.assertGreaterEqual(theme.label, round(24 * width / 1280))

    def test_refuses_course_output(self):
        with self.assertRaises(UnsafeOutput):
            render_prompt("title card", Path("/tmp/course/images/x.png"), preset="house")

    def test_each_preset_renders(self):
        with tempfile.TemporaryDirectory() as tmp:
            for name in PRESET_NAMES:
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
