"""Checks for the Blueprint path that do not encode a video."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "course/blueprint-rebuild"))
sys.path.insert(0, str(ROOT / "skills/video-production/quality-gate"))
sys.path.insert(0, str(ROOT / "skills/video-production"))
sys.path.insert(0, str(ROOT / "skills/video-production/natural-voice"))

import image_gate  # noqa: E402
import studio  # noqa: E402

lesson_scripts = studio.lesson_scripts
from gate.profiles import PROFILES, length_ok  # noqa: E402
from voice.align import Word  # noqa: E402
from voice.captions import cues, write_chapters, write_vtt  # noqa: E402
from voice.moods import MOODS  # noqa: E402

LEGAL = (
    "Education only, not financial advice. Crypto carries a risk of total loss. "
    "This is general information. It doesn't consider your objectives, financial situation or needs. "
    "The prices are public historical daily closes, marked Example. "
    "Past performance is not a reliable indicator of future results. "
    "No order is sent from this lesson."
)
DISCLAIMER = (
    "Education only. Not financial advice. "
    "This is general information and doesn't consider your objectives, financial situation or needs. "
    "Crypto is high risk. You could lose all the money you put in."
)


class PipelineTests(unittest.TestCase):
    def test_length_window_is_six_to_ten_minutes(self):
        profile = PROFILES["blueprint"]
        self.assertEqual(profile.min_seconds, 360)
        self.assertEqual(profile.max_seconds, 600)
        self.assertTrue(length_ok(6 * 60 + 15, profile))
        self.assertFalse(length_ok(5 * 60, profile))
        self.assertFalse(length_ok(11 * 60, profile))

    def test_fps_and_loudness_owner(self):
        self.assertEqual(studio.FPS, 30)
        self.assertEqual(PROFILES["blueprint"].fps, 30)
        source = Path(studio.__file__).read_text(encoding="utf-8")
        self.assertNotIn("loudnorm", source)
        self.assertIn("duck_under_voice", source)
        mix = (ROOT / "skills/video-production/lib/mix.py").read_text(encoding="utf-8")
        self.assertIn("VOICE_LUFS = -14.0", mix)

    def test_picture_changes_by_eight_seconds(self):
        import numpy as np

        audio = np.zeros(int(20 * 24000), dtype=np.float32)
        parts = studio._split_picture({"kind": "chart", "chapter": "Hook"}, audio, 24000)
        self.assertGreater(len(parts), 1)
        for part in parts:
            self.assertLessEqual(part["duration"], 8.0)

    def test_fonts_are_the_bundled_ofl_files(self):
        for path in (studio.FONT, studio.FONT_MED, studio.FONT_REG):
            self.assertTrue(path.is_file(), path)
            self.assertIn("skills/video-production/fonts/inter", str(path))

    def test_title_art_is_crop_only(self):
        mark = studio.wordmark()
        from PIL import Image

        full = Image.open(studio.COVER)
        self.assertLess(mark.size[0], full.size[0])
        self.assertLess(mark.size[1], full.size[1])
        with self.assertRaises(SystemExit):
            studio.load_picture(studio.COVER)

    def test_pinned_stop_matches_the_caption_row(self):
        shots = lesson_scripts.attach_series(lesson_scripts.walk(
            lesson_scripts.SUMMER, "Walk the summer", 4, (24930, 30331), "Closes inside the summer window"
        ))
        first = shots[0]
        self.assertEqual(first["pin_date"], "2023-07-19")
        self.assertEqual(first["pin_close"], 29914)
        self.assertIn("19 July 2023", first["caption"])
        self.assertIn("29,914", first["caption"])
        self.assertEqual(studio.playhead_index(first, 0.2, 6.0), 0)
        self.assertEqual(studio.playhead_index(first, 5.0, 6.0), 0)

    def test_six_gaps_between_seven_lines(self):
        levels = lesson_scripts.LEVELS
        self.assertEqual(len(levels), 7)
        gaps = [levels[i + 1] - levels[i] for i in range(len(levels) - 1)]
        self.assertEqual(len(gaps), 6)
        self.assertTrue(all(890 <= gap <= 910 for gap in gaps))
        self.assertIn("Six gaps", studio.chart_idea({"chapter": "The levels"}))
        self.assertNotIn("Seven gaps", studio.chart_idea({"chapter": "The levels"}))

    def test_disclaimer_and_legal_text(self):
        self.assertEqual(studio.DISCLAIMER, DISCLAIMER)
        self.assertEqual(" ".join(studio.DISCLAIMER_LINES), DISCLAIMER)
        legal = lesson_scripts.legal()
        self.assertEqual(legal["vo"], LEGAL)
        self.assertEqual(
            legal["caption"],
            "Education only. Not financial advice. Chart: historical BTC prices, EXAMPLE.",
        )
        self.assertNotIn("trading bot", legal["vo"].lower())
        self.assertNotIn("sell or run", legal["vo"].lower())

    def test_boards_name_their_headings(self):
        bp02 = lesson_scripts.build("bp-02-what-you-need")
        bp03 = lesson_scripts.build("bp-03-what-is-a-grid-bot")
        boards = {shot.get("chapter"): shot.get("board") for shot in bp02 + bp03}
        self.assertEqual(boards["Seven lines"], "seven-lines")
        self.assertEqual(boards["No secrets"], "no-secrets")
        self.assertEqual(boards["Buys and sells"], "buys-sells")

    def test_mascot_path_is_single_and_old_file_is_unused(self):
        self.assertTrue(str(studio.MASCOT_SRC).endswith("course/images/mascot/blueprint-mascot.png"))
        source = Path(studio.__file__).read_text(encoding="utf-8")
        self.assertNotIn("el-06-circuit-breakers/28.png", source)
        for sid in ("bp-01-introduction", "bp-02-what-you-need", "bp-03-what-is-a-grid-bot"):
            paths = [row["path"] for row in image_gate.images_for_lesson(sid)]
            self.assertIn(image_gate.MASCOT, paths)
            self.assertNotIn(image_gate.OLD_MASCOT, paths)

    def test_blob_mismatch_fails(self):
        cover = image_gate.COVER
        actual = image_gate.git_blob(cover)
        self.assertTrue(actual)
        self.assertIsNone(image_gate.blob_problem(cover, {"scored_blob": actual}))
        problem = image_gate.blob_problem(cover, {"scored_blob": "deadbeefdeadbeef"})
        self.assertIn("blob mismatch", problem or "")

    def test_captions_use_word_times_and_af_heart(self):
        for preset in MOODS.values():
            self.assertEqual(preset["kokoro_voice"], "af_heart")
        words = [Word("Education", 0.10, 0.55), Word("only", 0.55, 0.90)]
        grouped = cues(words)
        self.assertEqual(grouped[0][0].start, 0.10)
        folder = Path(tempfile.mkdtemp())
        vtt = folder / "cap.vtt"
        write_vtt(vtt, words)
        self.assertIn("00:00:00.100", vtt.read_text(encoding="utf-8"))
        chapters = folder / "chapters.txt"
        write_chapters(chapters, [(0.0, "Open"), (12.0, "Range")])
        self.assertTrue(chapters.read_text(encoding="utf-8").startswith("00:00 Open"))

    def test_old_mixer_cannot_encode(self):
        sys.path.insert(0, str(ROOT / "course/blueprint-rework"))
        import render_motion

        with self.assertRaises(SystemExit):
            render_motion.render("bp-01-introduction", False)

    def test_lesson_stills_are_attached(self):
        shots = studio.plan("bp-01-introduction")
        stills = [shot.get("lesson_still") or shot.get("still") for shot in shots]
        self.assertTrue(any(item and "bp-01-introduction" in item for item in stills))

    def test_customer_scripts_drop_the_bot_sentence(self):
        for name in (
            "bp-01-introduction.json",
            "bp-02-what-you-need.json",
            "bp-03-what-is-a-grid-bot.json",
        ):
            text = (ROOT / "course/scripts" / name).read_text(encoding="utf-8")
            self.assertNotIn("sell or run a trading bot", text)
            self.assertNotIn("Market Pros", text)
            data = json.loads(text)
            legal = next(beat for beat in data["beats"] if beat.get("role") == "legal")
            self.assertEqual(legal["vo"], LEGAL)


if __name__ == "__main__":
    unittest.main()
