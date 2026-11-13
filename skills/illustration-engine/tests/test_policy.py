import json
import os
import tempfile
import unittest
from pathlib import Path

from illustration_engine.cli import main
from illustration_engine.parser import parse
from illustration_engine.policy import RefusedPrompt
from illustration_engine.render import read_manifest


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


if __name__ == "__main__":
    unittest.main()
