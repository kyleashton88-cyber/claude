"""Append-only JSONL ledger and a markdown twin.

`publish_allowed` is computed. A caller cannot write it in.
"""

from __future__ import annotations

import hashlib
import json
from datetime import date
from pathlib import Path

BLOCKED_NAMES = {"auto", "agent", "cursor", "system", "bot", "claude"}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


class LedgerError(RuntimeError):
    pass


class Ledger:
    def __init__(self, folder: Path):
        self.folder = Path(folder)
        self.jsonl = self.folder / "ledger.jsonl"
        self.markdown = self.folder / "ledger.md"

    def exists(self) -> bool:
        return self.jsonl.is_file()

    def events(self) -> list[dict]:
        if not self.jsonl.is_file():
            return []
        rows = []
        for line in self.jsonl.read_text(encoding="utf-8").splitlines():
            if line.strip():
                rows.append(json.loads(line))
        return rows

    def init(self, *, master: Path, master_id: str, fmt: str) -> dict:
        if self.exists():
            raise LedgerError(f"ledger already exists at {self.jsonl}. It is append-only.")
        self.folder.mkdir(parents=True, exist_ok=False)
        master = Path(master)
        if not master.is_file():
            raise LedgerError(f"master not found: {master}")
        event = {
            "type": "init",
            "id": master_id,
            "format": fmt,
            "master": str(master),
            "master_hash": sha256_file(master),
        }
        self._append(event)
        return self.state()

    def _append(self, event: dict) -> dict:
        if "publish_allowed" in event:
            raise LedgerError("publish_allowed is computed. It cannot be written into the ledger.")
        if not self.jsonl.is_file() and event.get("type") != "init":
            raise LedgerError("ledger has not been initialised")
        event = dict(event)
        prior = self.events()
        event["seq"] = len(prior) + 1
        line = json.dumps(event, ensure_ascii=True)
        with self.jsonl.open("a", encoding="utf-8") as handle:
            handle.write(line + "\n")
        self._append_md(event)
        return event

    def _append_md(self, event: dict) -> None:
        if event["seq"] == 1:
            self.markdown.write_text(
                "# Review record\n\n"
                "Append-only. Do not edit lines already written.\n"
                "`publish_allowed` is computed from the ledger. Nothing here publishes.\n\n",
                encoding="utf-8",
            )
        state = compute_state(self.events())
        with self.markdown.open("a", encoding="utf-8") as handle:
            handle.write(f"## {event['seq']}. {event['type']}\n\n")
            handle.write("```json\n")
            handle.write(json.dumps(event, indent=2))
            handle.write("\n```\n\n")
            handle.write(
                f"After this event, publish allowed is **{str(state['publish_allowed']).lower()}**.\n\n"
            )

    def record_qa(self, report_path: Path) -> dict:
        report = json.loads(Path(report_path).read_text(encoding="utf-8"))
        result = report.get("result")
        if result not in {"pass", "fail"}:
            raise LedgerError("QA report needs result pass or fail")
        state = self.state()
        return self._append(
            {
                "type": "qa",
                "result": result,
                "master_hash": state["master_hash"],
                "report": str(report_path),
                "report_hash": sha256_file(Path(report_path)),
                "failed": report.get("failed") or [],
            }
        )

    def record_compliance(self, report_path: Path) -> dict:
        report = json.loads(Path(report_path).read_text(encoding="utf-8"))
        content = report.get("content_result")
        if content not in {"pass", "fail"}:
            raise LedgerError("compliance report needs content_result pass or fail")
        return self._append(
            {
                "type": "compliance",
                "status": "pending legal review",
                "content_result": content,
                "content_hash": report.get("content_hash"),
                "flag_count": report.get("flag_count"),
                "report": str(report_path),
                "report_hash": sha256_file(Path(report_path)),
            }
        )

    def legal(self, *, name: str, day: str, report_path: Path) -> dict:
        cleaned = name.strip()
        if not cleaned or cleaned.lower() in BLOCKED_NAMES:
            raise LedgerError("legal sign-off needs a person's name")
        _parse_day(day)
        report = json.loads(Path(report_path).read_text(encoding="utf-8"))
        if not report.get("content_hash"):
            raise LedgerError("compliance report has no content hash")
        return self._append(
            {
                "type": "legal",
                "decision": "approved",
                "name": cleaned,
                "date": day,
                "content_hash": report["content_hash"],
                "content_result": report.get("content_result"),
            }
        )

    def stewart(self, *, decision: str, day: str) -> dict:
        if decision not in {"yes", "no"}:
            raise LedgerError("Stewart's decision is yes or no")
        _parse_day(day)
        return self._append(
            {
                "type": "stewart",
                "decision": decision,
                "name": "Stewart Crown",
                "date": day,
                "notified": False,
            }
        )

    def state(self) -> dict:
        return compute_state(self.events())


def _parse_day(value: str) -> date:
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise LedgerError(f"date must be YYYY-MM-DD, got {value!r}") from exc


def compute_state(events: list[dict]) -> dict:
    init = next((event for event in events if event["type"] == "init"), None)
    qa = _latest(events, "qa")
    compliance = _latest(events, "compliance")
    legal = _latest(events, "legal")
    stewart = _latest(events, "stewart")
    master_hash = init["master_hash"] if init else None
    content_hash = compliance.get("content_hash") if compliance else None
    qa_ok = bool(
        qa
        and qa.get("result") == "pass"
        and qa.get("master_hash") == master_hash
    )
    content_ok = bool(compliance and compliance.get("content_result") == "pass")
    legal_signed = bool(
        legal
        and legal.get("decision") == "approved"
        and legal.get("name")
        and legal.get("date")
        and legal.get("content_hash")
        and legal.get("content_hash") == content_hash
    )
    legal_ok = legal_signed and content_ok
    stewart_ok = bool(stewart and stewart.get("decision") == "yes" and stewart.get("date"))
    reasons = []
    if not qa_ok:
        reasons.append("QA has not passed for this master hash")
    if not content_ok:
        reasons.append("compliance content has flags or has not been recorded")
    if not legal_signed:
        reasons.append("legal review is not signed for this content hash")
    if not stewart_ok:
        reasons.append("Stewart has not approved")
    if compliance is None:
        compliance_status = None
    elif legal_signed:
        compliance_status = "legal signed"
    else:
        compliance_status = "pending legal review"
    return {
        "id": init.get("id") if init else None,
        "format": init.get("format") if init else None,
        "master": init.get("master") if init else None,
        "master_hash": master_hash,
        "qa_result": qa.get("result") if qa else None,
        "compliance_status": compliance_status,
        "compliance_result": compliance.get("content_result") if compliance else None,
        "content_hash": content_hash,
        "legal_reviewer": legal.get("name") if legal_signed else None,
        "legal_date": legal.get("date") if legal_signed else None,
        "stewart": stewart.get("decision") if stewart else None,
        "stewart_date": stewart.get("date") if stewart else None,
        "publish_allowed": bool(qa_ok and legal_ok and stewart_ok),
        "blocked_by": reasons,
        "publishes": False,
    }


def _latest(events: list[dict], kind: str) -> dict | None:
    found = [event for event in events if event.get("type") == kind]
    return found[-1] if found else None
