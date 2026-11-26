"""Template, thumbnail, short, chapter, and end-card tests."""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parents[1]
VP = HERE.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(VP))
sys.path.insert(0, str(VP / "quality-gate"))

from gate.synth import encode_clip  # noqa: E402
from pack.distribute import (  # noqa: E402
    chapter_lines,
    cut_short,
    load_lesson,
    make_thumbnail,
    parse_chapters,
    shift_vtt,
    write_description,
)
from pack.engine import engine_installed  # noqa: E402
from pack.paint import paint_endcard  # noqa: E402


class TemplateTests(unittest.TestCase):
    def test_six_formats_have_a_disclaimer_and_a_next_lesson(self):
        names = sorted(path.stem for path in (HERE / "formats").glob("*.yaml"))
        self.assertEqual(
            names,
            ["blueprint-lesson", "elite-lesson", "explainer", "interview", "market-check", "short"],
        )
        for name in names:
            lesson = load_lesson(HERE / "formats" / f"{name}.yaml")
            self.assertIn("not financial advice", lesson["disclaimer_spoken"].lower())
            self.assertIn("not financial advice", lesson["disclaimer_on_screen"].lower())
            self.assertTrue(lesson["next"]["title"])
            self.assertEqual(chapter_lines(lesson)[0][:4], "0:00")


class ThumbnailTests(unittest.TestCase):
    def test_fallback_is_1280_by_720_in_house_colors(self):
        folder = Path(tempfile.mkdtemp())
        try:
            dest = folder / "thumb.png"
            meta = make_thumbnail("A grid in one picture", "Four facts", dest, engine="pil")
            self.assertEqual(meta["renderer"], "pil-fallback")
            image = Image.open(dest)
            self.assertEqual(image.size, (1280, 720))
            corner = image.getpixel((4, 4))[:3]
            self.assertLess(sum(corner), 80)
            cyan = image.getpixel((90, 430))[:3]
            # The cyan rule sits under the headline. Search a band for #00D4FF.
            found = False
            for y in range(300, 620):
                pixel = image.getpixel((100, y))[:3]
                if pixel[2] > 200 and pixel[1] > 160 and pixel[0] < 40:
                    found = True
                    break
            self.assertTrue(found, cyan)
        finally:
            shutil.rmtree(folder)

    def test_auto_uses_the_engine_only_when_it_is_installed(self):
        # This branch does not vendor the engine. The fallback must run.
        self.assertFalse(engine_installed())
        folder = Path(tempfile.mkdtemp())
        try:
            meta = make_thumbnail("Range", "EXAMPLE", folder / "t.png", engine="auto")
            self.assertEqual(meta["renderer"], "pil-fallback")
        finally:
            shutil.rmtree(folder)


class ShortTests(unittest.TestCase):
    def test_chapter_shift_and_reframe(self):
        shifted = shift_vtt(
            "WEBVTT\n\n00:00:02.000 --> 00:00:03.500\nThe gap.\n",
            2.0,
            4.0,
        )
        self.assertIn("00:00:00.000 --> 00:00:01.500", shifted)
        chapters = parse_chapters("0:00 Open\n0:02 The idea\n")
        self.assertEqual(chapters[1]["title"], "The idea")
        folder = Path(tempfile.mkdtemp())
        try:
            master = encode_clip(
                folder / "wide.mp4",
                width=320,
                height=180,
                seconds=4,
                fps=10,
                disclaimer=True,
                moving=True,
                loudnorm=False,
            )
            chapter_file = folder / "chapters.txt"
            chapter_file.write_text("0:00 Open\n0:02 The idea\n", encoding="utf-8")
            vtt = folder / "in.vtt"
            vtt.write_text("WEBVTT\n\n00:00:02.100 --> 00:00:03.400\nEducation, not financial advice.\n", encoding="utf-8")
            meta = cut_short(master, chapter_file, folder / "short.mp4", vtt=vtt, chapter="The idea")
            self.assertLess(meta["duration"], 60)
            self.assertFalse(meta["publishes"])
            probe = subprocess.check_output(
                ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "csv=p=0", str(folder / "short.mp4")],
                text=True,
            )
            self.assertIn("1080,1920", probe.replace(" ", ""))
            captions = (folder / "short.vtt").read_text(encoding="utf-8")
            self.assertIn("00:00:00.", captions)
        finally:
            shutil.rmtree(folder)


class DescriptionTests(unittest.TestCase):
    def test_description_opens_with_the_disclaimer(self):
        folder = Path(tempfile.mkdtemp())
        try:
            lesson = load_lesson(HERE / "formats" / "blueprint-lesson.yaml")
            path = write_description(lesson, folder / "description.txt")
            text = path.read_text(encoding="utf-8")
            self.assertIn("education, not financial advice", text.lower())
            self.assertIn("0:00 The picture", text)
            self.assertIn("Where the range sits", text)
        finally:
            shutil.rmtree(folder)


class EndCardTests(unittest.TestCase):
    def test_end_card_keeps_a_slot_on_the_right(self):
        folder = Path(tempfile.mkdtemp())
        try:
            meta = paint_endcard("A grid in one picture", "Where the range sits", folder / "end.png")
            image = Image.open(folder / "end.png")
            self.assertEqual(image.size, (1920, 1080))
            self.assertEqual(meta["hold_seconds"], 20)
            slot = meta["end_screen_slot"]
            self.assertGreater(slot["x"], 1100)
            # The left side carries the next-lesson title, so it is not flat navy.
            left = image.getpixel((120, 280))[:3]
            self.assertGreater(sum(left), 200)
        finally:
            shutil.rmtree(folder)


if __name__ == "__main__":
    unittest.main()
