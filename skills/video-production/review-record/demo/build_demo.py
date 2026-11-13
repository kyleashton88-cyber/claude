#!/usr/bin/env python3
"""A synthetic ledger. Stewart's yes here is a demo of the flag, not a real approval."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
VP = HERE.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(VP / "quality-gate"))

from gate.synth import encode_clip, write_pass_captions  # noqa: E402
from record.ledger import Ledger  # noqa: E402
from record.pack import build_pack  # noqa: E402


def main() -> None:
    os.chdir(HERE)
    out = Path("test-outputs")
    if (out / "ledger" / "ledger.jsonl").exists():
        raise SystemExit("ledger already exists; it is append-only. Remove test-outputs/ledger by hand if you mean to rebuild the demo.")
    out.mkdir(parents=True, exist_ok=True)
    master = encode_clip(
        out / "master.mp4",
        width=320,
        height=180,
        seconds=2,
        fps=15,
        disclaimer=True,
        moving=True,
        loudnorm=False,
    )
    transcript = write_pass_captions(out / "transcript.vtt", end=1.6)
    qa = out / "qa-report.json"
    qa.write_text(json.dumps({"result": "pass", "failed": [], "format": "short"}) + "\n", encoding="utf-8")
    compliance = out / "compliance-report.json"
    compliance.write_text(
        json.dumps(
            {
                "status": "pending legal review",
                "content_result": "pass",
                "content_hash": "demo-synthetic-script",
                "flag_count": 0,
            }
        )
        + "\n",
        encoding="utf-8",
    )
    ledger = Ledger(out / "ledger")
    ledger.init(master=master, master_id="synthetic-short", fmt="short")
    ledger.record_qa(qa)
    ledger.record_compliance(compliance)
    ledger.legal(name="Demo Counsel", day="2026-11-13", report_path=compliance)
    ledger.stewart(decision="yes", day="2026-11-13")
    state = ledger.state()
    (out / "state.json").write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
    build_pack(
        folder=out / "pack",
        master=master,
        qa_report=qa,
        compliance_report=compliance,
        transcript=transcript,
        state=state,
    )
    if not state["publish_allowed"]:
        raise SystemExit("demo ledger should compute publish_allowed true")
    note = out / "README.md"
    note.write_text(
        "\n".join(
            [
                "# Synthetic review demo",
                "",
                "The master is a generated clip. Demo Counsel and the Stewart yes are sample rows so the flag can be seen.",
                "They are not an approval of a real lesson, and no message was sent.",
                "",
                f"publish_allowed: {str(state['publish_allowed']).lower()}",
                "",
            ]
        ),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
