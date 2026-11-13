import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from illustration_engine.cli import main
from illustration_engine.parser import parse
from illustration_engine.policy import RefusedPrompt
from illustration_engine.qa import headline_stem
from illustration_engine.render import PlateCollision, RasterFailed, rasterize, read_manifest


class RefusalTests(unittest.TestCase):
    def test_photoreal_named_person_is_refused(self):
        with self.assertRaises(RefusedPrompt):
            parse("photoreal photo of Stewart")

    def test_refused_prompt_writes_nothing(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "plate.png"
            code = main(["render", "photoreal photo of Stewart", "--preset", "house", "--out", str(dest)])
            self.assertEqual(code, 1)
            self.assertFalse(dest.exists())

    def test_exchange_name_is_refused(self):
        with self.assertRaises(RefusedPrompt) as caught:
            parse("grid ladder on PIONEX, range 90-110, 8 grids, price 100")
        self.assertIn("PIONEX", str(caught.exception))

    def test_allow_generic_rewrites_and_does_not_draw_the_name(self):
        spec = parse("grid ladder on Binance, range 90-110, 8 grids, price 100", allow_generic=True)
        blob = json.dumps(spec.as_dict()).lower()
        self.assertNotIn("binance", blob)
        self.assertIn("exchange", blob)
        self.assertEqual(spec.type, "grid_ladder")

    def test_fallback_blocks_mascot_and_allows_a_grid(self):
        with self.assertRaises(RefusedPrompt):
            parse("mascot pointing", fallback=True)
        spec = parse("grid ladder, range 90-110, 10 grids, price 100, label buy and sell", fallback=True)
        self.assertEqual(spec.type, "grid_ladder")

    def test_a_published_plate_is_in_the_manifest_once(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "grid.png"
            code = main([
                "render",
                "grid ladder, range 90-110, 10 grids, price 100, label buy and sell",
                "--preset", "house",
                "--out", str(dest),
            ])
            self.assertEqual(code, 0)
            self.assertTrue(dest.is_file())
            first = read_manifest(dest.parent)
            files = [row["file"] for row in first["images"]]
            self.assertEqual(files, ["grid.png"])
            self.assertEqual(first["source"], "illustration-engine")
            self.assertEqual(first["mode"], "normal")
            self.assertFalse(first["fallback_tier"])
            self.assertTrue(first["images"][0]["qa_ok"])
            self.assertTrue(first["images"][0]["checksum"])
            code = main([
                "render",
                "grid ladder, range 90-110, 10 grids, price 100, label buy and sell",
                "--preset", "house",
                "--out", str(dest),
            ])
            self.assertEqual(code, 0)
            second = read_manifest(dest.parent)
            self.assertEqual([row["file"] for row in second["images"]], ["grid.png"])
            row = second["images"][0]
            for key in (
                "job_id", "prompt_hash", "provider", "provider_version", "reason",
                "created_at", "updated_at", "qa_status", "reviewer", "sha256",
            ):
                self.assertTrue(row.get(key), key)
            self.assertEqual(row["provider"], "illustration-engine")
            self.assertEqual(row["qa_status"], "pass")
            self.assertEqual(row["reviewer"], "engine-preflight")
            self.assertEqual(len(row["sha256"]), 64)

    def test_fallback_refuses_a_scene_with_no_diagram(self):
        with self.assertRaises(RefusedPrompt):
            parse("a woman on a beach at sunset", fallback=True)
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "plate.png"
            code = main([
                "render", "a woman on a beach at sunset",
                "--fallback", "--preset", "house", "--out", str(dest),
            ])
            self.assertEqual(code, 1)
            self.assertFalse(dest.exists())
            self.assertFalse((dest.parent / "MANIFEST.json").exists())

    def test_duplicate_filenames_collide_before_drawing(self):
        from illustration_engine.batch import render_lesson

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "slots.yaml"
            source.write_text(
                "slots:\n"
                "  - file: same.png\n"
                "    prompt: grid ladder, range 90-110, 10 grids, price 100, label buy and sell\n"
                "  - file: same.png\n"
                "    prompt: candle anatomy, bull\n",
                encoding="utf-8",
            )
            with self.assertRaises(PlateCollision):
                render_lesson(source, root / "out")
            self.assertFalse((root / "out" / "same.png").exists())

    def test_unchanged_prompt_hash_skips_a_second_draw(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "grid.png"
            prompt = "grid ladder, range 90-110, 10 grids, price 100, label buy and sell"
            self.assertEqual(main(["render", prompt, "--preset", "house", "--out", str(dest)]), 0)
            first = read_manifest(dest.parent)["images"][0]["job_id"]
            self.assertEqual(main(["render", prompt, "--preset", "house", "--out", str(dest)]), 0)
            second = read_manifest(dest.parent)["images"][0]
            self.assertEqual(second["job_id"], first)
            self.assertEqual([row["file"] for row in read_manifest(dest.parent)["images"]], ["grid.png"])

    def test_plate_stem_does_not_borrow_the_font_probe(self):
        self.assertEqual(headline_stem(b"", []), 0.0)

    def test_a_failed_rerender_drops_the_manifest_entry(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "grid.png"
            prompt = "grid ladder, range 90-110, 10 grids, price 100, label buy and sell"
            self.assertEqual(main(["render", prompt, "--preset", "house", "--out", str(dest)]), 0)
            self.assertEqual(read_manifest(dest.parent)["images"][0]["file"], "grid.png")
            with patch("illustration_engine.render.check_pixels", return_value=(False, "forced failure")):
                code = main(["render", prompt + " again", "--preset", "house", "--out", str(dest)])
            self.assertEqual(code, 1)
            self.assertFalse(dest.exists())
            self.assertEqual(read_manifest(dest.parent).get("images"), [])
            self.assertEqual(read_manifest(dest.parent)["rejected"][0]["file"], "grid.png")
            self.assertEqual(read_manifest(dest.parent)["rejected"][0]["qa_status"], "fail")

    def test_rasterizer_logs_cairo_and_fails_when_both_miss(self):
        with tempfile.TemporaryDirectory() as tmp:
            svg = Path(tmp) / "x.svg"
            png = Path(tmp) / "x.png"
            svg.write_text('<svg xmlns="http://www.w3.org/2000/svg" width="8" height="8"/>', encoding="utf-8")
            with patch("illustration_engine.render.shutil.which", return_value=None):
                with self.assertLogs("illustration_engine", level="WARNING") as logs:
                    with patch("cairosvg.svg2png", side_effect=RuntimeError("cairo down")):
                        with self.assertRaises(RasterFailed):
                            rasterize(svg, png, 8, 8)
            self.assertTrue(any("not on PATH" in line for line in logs.output))


if __name__ == "__main__":
    unittest.main()
