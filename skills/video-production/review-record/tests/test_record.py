"""Ledger tests. Publish is computed, and the file only grows."""

from __future__ import annotations

import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
VP = HERE.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(VP / "quality-gate"))

from gate.synth import encode_clip  # noqa: E402
from record.ledger import Ledger, LedgerError, compute_state  # noqa: E402
from record.pack import build_pack  # noqa: E402


def _report(folder: Path, name: str, payload: dict) -> Path:
    path = folder / name
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


class LedgerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="review-"))
        self.master = encode_clip(
            self.tmp / "master.mp4",
            width=160,
            height=90,
            seconds=1.2,
            fps=10,
            moving=True,
            disclaimer=False,
            loudnorm=False,
        )
        self.ledger = Ledger(self.tmp / "ledger")

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def _pass_reports(self):
        qa = _report(self.tmp, "qa.json", {"result": "pass", "failed": []})
        compliance = _report(
            self.tmp,
            "compliance.json",
            {"content_result": "pass", "content_hash": "abc", "flag_count": 0, "status": "pending legal review"},
        )
        return qa, compliance

    def test_publish_requires_qa_legal_and_stewart(self):
        self.ledger.init(master=self.master, master_id="sample", fmt="short")
        self.assertFalse(self.ledger.state()["publish_allowed"])
        qa, compliance = self._pass_reports()
        self.ledger.record_qa(qa)
        self.ledger.record_compliance(compliance)
        self.assertEqual(self.ledger.state()["compliance_status"], "pending legal review")
        self.assertFalse(self.ledger.state()["publish_allowed"])
        self.ledger.legal(name="Alex Counsel", day="2026-11-13", report_path=compliance)
        self.ledger.stewart(decision="no", day="2026-11-13")
        self.assertFalse(self.ledger.state()["publish_allowed"])
        self.ledger.stewart(decision="yes", day="2026-11-13")
        state = self.ledger.state()
        self.assertTrue(state["publish_allowed"])
        self.assertEqual(state["legal_reviewer"], "Alex Counsel")
        self.assertEqual(state["stewart"], "yes")
        self.assertFalse(state["publishes"])

    def test_later_qa_fail_closes_publish(self):
        self.ledger.init(master=self.master, master_id="sample", fmt="short")
        qa, compliance = self._pass_reports()
        self.ledger.record_qa(qa)
        self.ledger.record_compliance(compliance)
        self.ledger.legal(name="Alex Counsel", day="2026-11-13", report_path=compliance)
        self.ledger.stewart(decision="yes", day="2026-11-13")
        self.assertTrue(self.ledger.state()["publish_allowed"])
        failed = _report(self.tmp, "qa-fail.json", {"result": "fail", "failed": ["loudness"]})
        self.ledger.record_qa(failed)
        self.assertFalse(self.ledger.state()["publish_allowed"])

    def test_append_only_and_no_direct_publish_flag(self):
        self.ledger.init(master=self.master, master_id="sample", fmt="short")
        first = self.ledger.jsonl.read_text(encoding="utf-8")
        with self.assertRaises(LedgerError):
            self.ledger.init(master=self.master, master_id="sample", fmt="short")
        self.assertEqual(self.ledger.jsonl.read_text(encoding="utf-8"), first)
        with self.assertRaises(LedgerError):
            self.ledger._append({"type": "note", "publish_allowed": True})
        with self.assertRaises(LedgerError):
            self.ledger.legal(name="cursor", day="2026-11-13", report_path=self._pass_reports()[1])
        qa, _compliance = self._pass_reports()
        self.ledger.record_qa(qa)
        lines = self.ledger.jsonl.read_text(encoding="utf-8").splitlines()
        self.assertEqual(json.loads(lines[0])["type"], "init")
        self.assertGreater(len(lines), 1)
        self.assertIn("Append-only", self.ledger.markdown.read_text(encoding="utf-8"))

    def test_content_flags_block_publish_even_after_signatures(self):
        self.ledger.init(master=self.master, master_id="sample", fmt="short")
        qa = _report(self.tmp, "qa.json", {"result": "pass", "failed": []})
        compliance = _report(
            self.tmp,
            "compliance.json",
            {"content_result": "fail", "content_hash": "abc", "flag_count": 2},
        )
        self.ledger.record_qa(qa)
        self.ledger.record_compliance(compliance)
        self.ledger.legal(name="Alex Counsel", day="2026-11-13", report_path=compliance)
        self.ledger.stewart(decision="yes", day="2026-11-13")
        state = self.ledger.state()
        self.assertEqual(state["legal_reviewer"], "Alex Counsel")
        self.assertFalse(state["publish_allowed"])

    def test_pack_writes_a_contact_sheet_and_does_not_publish(self):
        self.ledger.init(master=self.master, master_id="sample", fmt="short")
        qa, compliance = self._pass_reports()
        transcript = self.tmp / "transcript.vtt"
        transcript.write_text("WEBVTT\n\n00:00:00.000 --> 00:00:01.000\nEducation, not financial advice.\n", encoding="utf-8")
        pack = self.tmp / "pack"
        build_pack(
            folder=pack,
            master=self.master,
            qa_report=qa,
            compliance_report=compliance,
            transcript=transcript,
            state=self.ledger.state(),
        )
        self.assertTrue((pack / "contact-sheet.png").is_file())
        self.assertTrue((pack / "qa-report.json").is_file())
        self.assertTrue((pack / "compliance-report.json").is_file())
        self.assertTrue((pack / "transcript.vtt").is_file())
        self.assertIn("does not publish", (pack / "README.md").read_text(encoding="utf-8"))
        self.assertFalse(compute_state(self.ledger.events())["publish_allowed"])


if __name__ == "__main__":
    unittest.main()
