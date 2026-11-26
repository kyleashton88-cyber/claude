"""Compliance linter tests. Sign-off is never automatic."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))

from compliance.lint import lint_path  # noqa: E402

SAMPLES = HERE / "samples"
CLI = HERE / "cli.py"


class LintTests(unittest.TestCase):
    def test_clean_lesson_stays_pending(self):
        report = lint_path(SAMPLES / "clean-lesson.yaml")
        self.assertEqual(report["flags"], [])
        self.assertEqual(report["content_result"], "pass")
        self.assertEqual(report["status"], "pending legal review")
        self.assertFalse(report["auto_clear"])

    def test_risky_script_flags_line_time_and_rewrite(self):
        report = lint_path(SAMPLES / "risky-script.txt")
        kinds = {flag["kind"] for flag in report["flags"]}
        self.assertIn("hype", kinds)
        self.assertIn("personal-advice", kinds)
        self.assertIn("brand", kinds)
        self.assertIn("example-number", kinds)
        self.assertIn("disclaimer", kinds)
        for flag in report["flags"]:
            self.assertGreaterEqual(flag["line"], 1)
            self.assertTrue(flag["suggestion"])
        hype = next(flag for flag in report["flags"] if flag["term"] == "guaranteed")
        self.assertEqual(hype["timestamp"], "00:00:01.000")
        self.assertEqual(report["status"], "pending legal review")

    def test_negated_guarantee_is_quiet(self):
        folder = Path(tempfile.mkdtemp())
        path = folder / "note.txt"
        path.write_text(
            "## spoken\n"
            "Returns are not guaranteed. This is education, not financial advice.\n"
            "## on-screen\n"
            "Education, not financial advice. EXAMPLE only.\n",
            encoding="utf-8",
        )
        report = lint_path(path)
        self.assertFalse(any(flag["term"] == "guaranteed" for flag in report["flags"]))

    def test_approve_flag_is_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            proc = subprocess.run(
                [sys.executable, str(CLI), "lint", str(SAMPLES / "clean-lesson.yaml"), "--out", tmp, "--approve"],
                capture_output=True,
                text=True,
            )
        self.assertEqual(proc.returncode, 2)
        self.assertIn("never auto-clears", proc.stderr)

    def test_ledger_can_reflect_a_human_signature_only(self):
        report = lint_path(SAMPLES / "clean-lesson.yaml")
        ledger = Path(tempfile.mkdtemp()) / "ledger.jsonl"
        event = {
            "type": "legal",
            "decision": "approved",
            "name": "Alex Counsel",
            "date": "2026-11-13",
            "content_hash": report["content_hash"],
        }
        ledger.write_text(json.dumps(event) + "\n", encoding="utf-8")
        from compliance.lint import apply_ledger

        signed = apply_ledger(report, ledger)
        self.assertEqual(signed["status"], "legal signed")
        self.assertEqual(signed["legal_reviewer"], "Alex Counsel")
        unsigned = apply_ledger(report, None)
        self.assertEqual(unsigned["status"], "pending legal review")


if __name__ == "__main__":
    unittest.main()
