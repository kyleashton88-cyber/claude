"""Markup, pronunciation, alignment accuracy, and the ban on a paid speech engine."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from voice.align import align_templates
from voice.captions import caption_box, margin_ok, write_chapters
from voice.markup import parse_markup, written_text
from voice.pronounce import apply_pronunciation


class MarkupTests(unittest.TestCase):
    def test_pause_and_emphasis_do_not_change_the_written_line(self):
        text = "Read the *buffer*. <pause 400ms> Then stop."
        self.assertEqual(written_text(text), "Read the buffer. Then stop.")
        kinds = [span.kind for span in parse_markup(text)]
        self.assertIn("pause", kinds)
        self.assertTrue(any(span.emph for span in parse_markup(text)))

    def test_tickers_are_spoken_and_not_spelled_as_the_caption(self):
        self.assertIn("U S D T", apply_pronunciation("Hold USDT."))
        self.assertIn("dohj", apply_pronunciation("DOGE moved."))
        self.assertIn("sol", apply_pronunciation("SOL held."))


class AlignTests(unittest.TestCase):
    def test_word_error_against_a_reference_clip_is_under_80ms(self):
        sr = 22050
        words = ["Price", "moves", "in", "candles"]
        rng = np.random.default_rng(3)
        templates = []
        truth = []
        pieces = []
        clock = 0.0
        gap = 0.18
        for word in words:
            n = int((0.25 + 0.05 * len(word)) * sr)
            tone = (0.2 * np.sin(2 * np.pi * (180 + 40 * len(word)) * np.arange(n) / sr)).astype(np.float32)
            tone += 0.02 * rng.normal(0, 1, n).astype(np.float32)
            templates.append(tone)
            truth.append((clock, clock + n / sr))
            pieces.append(tone)
            pieces.append(np.zeros(int(gap * sr), dtype=np.float32))
            clock += n / sr + gap
        utterance = np.concatenate(pieces)
        placed = align_templates(utterance, sr, words, templates)
        errors = []
        for (start, end), word in zip(truth, placed):
            errors.append(abs(word.start - start))
            errors.append(abs(word.end - end))
        median = float(np.median(errors))
        self.assertLess(median, 0.080, f"median error {median:.3f}s")


class CaptionTests(unittest.TestCase):
    def test_burned_caption_stays_inside_five_percent(self):
        box = caption_box()
        self.assertTrue(margin_ok(box))

    def test_chapters_start_at_zero(self):
        path = Path("/tmp/chapters-test.txt")
        write_chapters(path, [(0.0, "Open"), (12.4, "The range")])
        text = path.read_text().splitlines()
        self.assertTrue(text[0].startswith("00:00"))
        self.assertIn("The range", text[1])


    def test_bundled_fonts_are_used_before_the_system_pack(self):
        from lib.fonts import font_file
        bold = font_file("Inter", "Bold")
        condensed = font_file("Roboto Condensed", "Bold")
        self.assertTrue(bold.is_file())
        self.assertIn("fonts/inter", str(bold))
        self.assertTrue(condensed.is_file())
    def test_paid_speech_name_is_gone_from_the_skill_source(self):
        root = Path(__file__).resolve().parents[1]
        banned = bytes.fromhex("656c6576656e6c616273").decode()
        for path in root.rglob("*"):
            if path.suffix not in {".py", ".md", ".txt", ".json"} or "test-outputs" in path.parts:
                continue
            if path.name == "test_voice.py":
                continue
            text = path.read_text(errors="ignore").lower()
            self.assertNotIn(banned, text, str(path))


if __name__ == "__main__":
    unittest.main()
