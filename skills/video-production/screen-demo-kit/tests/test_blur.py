"""Sensitive-pattern tests, plus one real blur of a synthetic still."""

from __future__ import annotations

import shutil
import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))

from screen_demo.blur import blur_image, pattern_hits, qa_image  # noqa: E402

FONT = HERE.parent / "templates" / "assets" / "fonts" / "Inter-Bold.ttf"


class PatternTests(unittest.TestCase):
    def test_patterns_name_the_four_kinds(self):
        text = (
            "Wallet 0x1111111111111111111111111111111111111111 "
            "Key sk-TESTKEYONLY000000 Balance $4200 Account 123456789012"
        )
        kinds = {kind for kind, _token in pattern_hits(text)}
        self.assertEqual(kinds, {"wallet", "api-key", "balance", "account"})

    def test_plain_lesson_text_is_quiet(self):
        self.assertEqual(pattern_hits("The buffer is the gap. EXAMPLE 90 and 110."), [])


class BlurTests(unittest.TestCase):
    def test_blur_clears_a_synthetic_screen(self):
        if shutil.which("tesseract") is None:
            self.skipTest("tesseract is not installed")
        folder = Path(tempfile.mkdtemp())
        try:
            image = Image.new("RGB", (1100, 420), (255, 255, 255))
            draw = ImageDraw.Draw(image)
            face = ImageFont.truetype(str(FONT), 32)
            draw.text((40, 40), "Wallet 0x1111111111111111111111111111111111111111", fill=(0, 0, 0), font=face)
            draw.text((40, 120), "Key sk-TESTKEYONLY000000", fill=(0, 0, 0), font=face)
            draw.text((40, 200), "Balance $4200", fill=(0, 0, 0), font=face)
            draw.text((40, 280), "Account 123456789012", fill=(0, 0, 0), font=face)
            raw = folder / "raw.png"
            image.save(raw)
            self.assertTrue(qa_image(raw))
            clean = folder / "clean.png"
            blur_image(raw, clean)
            self.assertEqual(qa_image(clean), [])
        finally:
            shutil.rmtree(folder)


if __name__ == "__main__":
    unittest.main()
