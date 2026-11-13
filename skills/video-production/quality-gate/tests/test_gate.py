"""Unit tests for the format-profile quality gate."""

from __future__ import annotations

import shutil
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
VP = HERE.parent
sys.path.insert(0, str(VP))
sys.path.insert(0, str(HERE))

from gate.captions import caption_problems, parse_captions  # noqa: E402
from gate.evaluate import evaluate  # noqa: E402
from gate.media import black_runs, gray_frames, judge_loudness, longest_static  # noqa: E402
from gate.profiles import PROFILES, get_profile, length_ok  # noqa: E402
from gate.synth import encode_black_gap, encode_clip, write_pass_captions  # noqa: E402
from gate.textscan import find_brands, has_disclaimer, tesseract_path  # noqa: E402


class ProfileTests(unittest.TestCase):
    def test_approved_bp01_length_fits_blueprint(self):
        """BP-01 is 6:15. The blueprint window is 4 to 10 minutes."""
        six_fifteen = 6 * 60 + 15
        self.assertTrue(length_ok(six_fifteen, PROFILES["blueprint"]))
        self.assertEqual(PROFILES["blueprint"].min_seconds, 4 * 60)
        self.assertLess(six_fifteen, 15 * 60)

    def test_short_is_under_one_minute(self):
        self.assertLess(PROFILES["short"].max_seconds, 60)
        self.assertEqual(PROFILES["short"].width, 1080)
        self.assertEqual(PROFILES["short"].height, 1920)

    def test_known_formats(self):
        for name in ("blueprint", "elite", "market-check", "explainer", "interview", "short"):
            self.assertEqual(get_profile(name).name, name)


class LoudnessTests(unittest.TestCase):
    def test_target_window_fails_closed(self):
        loud, peak = judge_loudness(-14.4, -1.6)
        self.assertEqual(loud, [])
        self.assertEqual(peak, [])
        loud, peak = judge_loudness(-16.2, -3.0)
        self.assertTrue(loud)
        self.assertEqual(peak, [])
        loud, peak = judge_loudness(-14.0, -0.2)
        self.assertEqual(loud, [])
        self.assertTrue(peak)
        loud, peak = judge_loudness(None, None)
        self.assertTrue(loud)
        self.assertTrue(peak)


class CaptionTests(unittest.TestCase):
    def test_line_length_and_speed(self):
        profile = PROFILES["short"]
        slow = parse_captions("WEBVTT\n\n00:00:00.000 --> 00:00:02.000\nFour facts.\n")
        self.assertEqual(caption_problems(slow, profile), [])
        fast = parse_captions(
            "WEBVTT\n\n00:00:00.000 --> 00:00:01.000\n"
            "1234567890123456789012345\n"
        )
        self.assertTrue(any("per second" in item for item in caption_problems(fast, profile)))
        long_line = parse_captions(
            "WEBVTT\n\n00:00:00.000 --> 00:00:04.000\n"
            "This caption line is deliberately longer than forty-two characters.\n"
        )
        self.assertTrue(any("characters" in item for item in caption_problems(long_line, profile)))


class TextTests(unittest.TestCase):
    def test_disclaimer_and_brands(self):
        self.assertTrue(has_disclaimer("This is education, not financial advice."))
        self.assertFalse(has_disclaimer("Watch the orders."))
        self.assertEqual(find_brands("The fill is on Binance today."), ["binance"])
        self.assertEqual(find_brands("A grid drawn as a picture."), [])


class PictureTests(unittest.TestCase):
    def test_static_and_black_runs(self):
        folder = Path(tempfile.mkdtemp(prefix="qg-pic-"))
        try:
            static = encode_clip(
                folder / "static.mp4",
                width=160,
                height=90,
                seconds=2,
                fps=10,
                moving=False,
                disclaimer=False,
                loudnorm=False,
            )
            frames = gray_frames(static, fps=2)
            hold, _at = longest_static(frames, fps=2)
            self.assertGreater(hold, 1.0)

            moving = encode_clip(
                folder / "move.mp4",
                width=160,
                height=90,
                seconds=2,
                fps=10,
                moving=True,
                disclaimer=False,
                loudnorm=False,
            )
            moving_frames = gray_frames(moving, fps=2)
            move_hold, _at = longest_static(moving_frames, fps=2)
            self.assertLess(move_hold, 1.0)

            gap = encode_black_gap(folder / "gap.mp4")
            dark = black_runs(gray_frames(gap, fps=4), fps=4)
            self.assertTrue(any(length >= 0.5 for _start, length in dark))
        finally:
            shutil.rmtree(folder)


class GateTests(unittest.TestCase):
    def test_small_master_passes_a_shrunk_short_profile(self):
        if tesseract_path() is None:
            self.skipTest("tesseract is not installed")
        folder = Path(tempfile.mkdtemp(prefix="qg-pass-"))
        try:
            master = encode_clip(
                folder / "master.mp4",
                width=640,
                height=360,
                seconds=4,
                disclaimer=True,
                moving=True,
                loudnorm=True,
            )
            captions = write_pass_captions(folder / "master.vtt", end=3.6)
            profile = get_profile(
                "short",
                min_seconds=1,
                max_seconds=30,
                width=640,
                height=360,
                max_hold_seconds=8,
            )
            payload = evaluate(master, profile, captions=captions)
            failed = payload["failed"]
            self.assertEqual(failed, [], payload)
            self.assertEqual(payload["result"], "pass")
            self.assertFalse(payload["publishes"])
        finally:
            shutil.rmtree(folder)

    def test_missing_tesseract_fails_the_gate(self):
        folder = Path(tempfile.mkdtemp(prefix="qg-ocr-"))
        try:
            master = encode_clip(
                folder / "master.mp4",
                width=160,
                height=90,
                seconds=2,
                fps=10,
                disclaimer=False,
                moving=True,
                loudnorm=False,
            )
            captions = write_pass_captions(folder / "c.vtt", end=1.5)
            profile = get_profile(
                "short",
                min_seconds=1,
                max_seconds=30,
                width=160,
                height=90,
                max_hold_seconds=8,
            )
            import sys as _sys

            evaluate_mod = _sys.modules["gate.evaluate"]
            original = evaluate_mod.tesseract_path
            evaluate_mod.tesseract_path = lambda: None
            try:
                payload = evaluate(master, profile, captions=captions)
            finally:
                evaluate_mod.tesseract_path = original
            self.assertEqual(payload["result"], "fail")
            self.assertIn("text_recognition", payload["failed"])
            self.assertIn("brands", payload["failed"])
            self.assertIn("safe_margins", payload["failed"])
            detail = next(item["detail"] for item in payload["checks"] if item["id"] == "brands")
            self.assertIn("not skipped", detail)
        finally:
            shutil.rmtree(folder)


if __name__ == "__main__":
    unittest.main()
