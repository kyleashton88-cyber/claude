#!/usr/bin/env python3
"""Checks for the Kyle → Stuart replacer and the inventory split."""

import json
import unittest
from pathlib import Path

import apply_kyle_to_stuart as tool

HERE = Path(__file__).resolve().parent


class ReplaceTests(unittest.TestCase):
    def test_prose_forms(self):
        self.assertEqual(tool.replace_kyle("with Kyle for a decision"), "with Stuart for a decision")
        self.assertEqual(tool.replace_kyle("ready for Kyle's review"), "ready for Stuart's review")
        self.assertEqual(tool.replace_kyle("once Kyle’s decided"), "once Stuart’s decided")
        self.assertEqual(
            tool.replace_kyle("Decisions waiting on Stewart Crown (Kyle)"),
            "Decisions waiting on Stewart Crown (Stuart)",
        )
        self.assertEqual(tool.replace_kyle("Owner: Kyle/Stewart to decide"), "Owner: Stuart/Stewart to decide")

    def test_does_not_touch_stewart_or_account_paths(self):
        samples = [
            "Stewart Crown",
            "kyle-ashton/omni-brain",
            "origin.cursor.com/git/kyle-ashton/tmp.git",
            "kyleashton88@gmail.com",
        ]
        for sample in samples:
            self.assertEqual(tool.replace_kyle(sample), sample)

    def test_inventory_counts(self):
        groups = tool.classify(tool.load_inventory(HERE / "inventory.json"))
        self.assertEqual(len(groups["editable"]), 36)
        self.assertEqual(len(groups["leave"]), 5)
        self.assertEqual(len(groups["blocked"]), 14)
        self.assertTrue(all(row["author_id"] == tool.OWNER_ID for row in groups["editable"]))
        self.assertTrue(all(row["hit_kind"] == "account_path" for row in groups["leave"]))

    def test_editable_snippets_drop_kyle_and_keep_stewart(self):
        groups = tool.classify(tool.load_inventory(HERE / "inventory.json"))
        for row in groups["editable"]:
            before, after = tool.snippet_pair(row)
            self.assertIsNone(tool.KYLE_WORD.search(after), after)
            self.assertEqual(
                len(tool.STEWART_WORD.findall(before)),
                len(tool.STEWART_WORD.findall(after)),
            )
            if tool.KYLE_WORD.search(before):
                self.assertIn("Stuart", after)
            self.assertNotIn("Stewart's", after.replace("Stewart Crown", ""))


if __name__ == "__main__":
    unittest.main()
