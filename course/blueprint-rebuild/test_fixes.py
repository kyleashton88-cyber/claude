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
from voice.captions import cues, fitted_cues, refit_vtt_text, write_chapters, write_vtt  # noqa: E402
from gate.captions import caption_problems, parse_captions  # noqa: E402
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

    def test_date_tag_stays_off_the_level_lines(self):
        shots = lesson_scripts.attach_series(lesson_scripts.walk(
            lesson_scripts.SUMMER, "Walk the summer", 4, (24930, 30331), "Closes inside the summer window"
        ))
        shot = shots[0]
        series = shot["series"]
        plot = (120, 200, 1500, 700)
        closes = [float(row["close"]) for row in series]
        lo = min(float(row["low"]) for row in series)
        hi = max(float(row["high"]) for row in series)
        pad = (hi - lo) * 0.12
        lo_p, hi_p = lo - pad, hi + pad
        n = len(series)
        full = [studio._map(i, n, closes[i], lo_p, hi_p, plot) for i in range(n)]
        hx, hy = full[0]
        level_ys = [studio._map(0, n, price, lo_p, hi_p, plot)[1] for price in (24930, 30331)]
        tx, ty = studio.place_date_tag(hx, hy, 280, 44, plot, level_ys, full)
        self.assertFalse(any(ty - 8 < level < ty + 44 + 8 for level in level_ys))
        self.assertLess(abs((ty + 22) - hy), 180)
        lane_ty = min(max(plot[1], hy - 22), plot[3] - 44)
        self.assertLess(abs((lane_ty + 22) - hy), 4)

    def test_end_card_names_the_next_lesson(self):
        kicker, label, cta = studio.next_lesson_label({
            "lesson_no": "01",
            "caption": "What you are going to need",
        })
        self.assertEqual((kicker, label, cta), ("NEXT", "Lesson 2", "Up next: Lesson 2"))
        mascot = studio.cleared_mascot({"lesson_id": "bp-01-introduction"})
        self.assertIsNotNone(mascot)
        self.assertEqual(mascot.size, (1024, 1024))

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

    def test_fast_cues_are_held_not_cut(self):
        """A 0.35s one-word cue used to survive the cap because the cap stopped at one word."""
        words = [
            Word("drawing.", 122.042, 122.092),
            Word("Seven", 122.092, 122.142),
            Word("days", 122.142, 122.192),
            Word("in", 122.192, 122.242),
            Word("this", 122.242, 122.292),
            Word("window", 122.292, 122.342),
            Word("wicked", 122.342, 122.392),
            Word("above", 122.392, 122.792),
            Word("tidy", 122.792, 123.192),
        ]
        # The spare time is on the earlier word, the way the aligner actually behaves.
        words = [Word("Round", 119.772, 122.042)] + words
        folder = Path(tempfile.mkdtemp())
        vtt = folder / "fast.vtt"
        write_vtt(vtt, words)
        text = vtt.read_text(encoding="utf-8")
        self.assertIn("drawing.", text)
        self.assertIn("wicked", text)
        self.assertIn("tidy", text)
        refit = refit_vtt_text(text)
        parsed = parse_captions(refit)
        spoken = " ".join(word.text for word in words)
        self.assertEqual(" ".join(cue.text for cue in parsed), spoken)
        problems = caption_problems(parsed, PROFILES["blueprint"])
        self.assertEqual(problems, [])
        for cue in parsed:
            cps = len(cue.text) / (cue.end - cue.start)
            self.assertLessEqual(cps, 18.0)
            self.assertLessEqual(len(cue.text), 42)

    def test_abutting_duplicate_token_is_one_caption_word(self):
        words = [Word("public", 1.0, 1.4), Word("public", 1.4, 1.7), Word("low", 1.9, 2.3)]
        text = " ".join(payload for _start, _end, payload in fitted_cues(words))
        self.assertEqual(text, "public low")

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
