#!/usr/bin/env python3
"""Lint a script or transcript. Does not sign off and does not publish.

  python3 cli.py lint samples/clean-lesson.yaml --out report-dir
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from compliance.lint import apply_ledger, lint_path  # noqa: E402


def refuse_course(path: Path) -> None:
    if "course" in path.resolve().parts:
        raise SystemExit(f"refusing to write into course/: {path}")


def render_markdown(report: dict) -> str:
    lines = [
        "# Compliance",
        "",
        f"Status: **{report['status']}**",
        "",
        "This status stays on pending legal review until a person records approval in the review record.",
        "Re-running the linter does not clear it.",
        "",
        f"Content: {report['content_result']}. Flags: {report['flag_count']}.",
        f"Source: `{report['source']}`",
        f"Content hash: `{report['content_hash']}`",
        "",
    ]
    if not report["flags"]:
        lines.append("No content flags.")
    else:
        lines.extend(["| Line | Time | Kind | Text | Rewrite |", "|---|---|---|---|---|"])
        for flag in report["flags"]:
            text = flag["text"].replace("|", "/").replace("\n", " ")
            suggestion = flag["suggestion"].replace("|", "/")
            lines.append(
                f"| {flag['line']} | {flag.get('timestamp') or ''} | {flag['kind']} | {text} | {suggestion} |"
            )
    lines.extend(["", report["signoff"], "", "Nothing here publishes or sends mail.", ""])
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Lint a script for financial-content risk")
    sub = parser.add_subparsers(dest="cmd", required=True)
    lint = sub.add_parser("lint")
    lint.add_argument("source", type=Path)
    lint.add_argument("--out", type=Path, required=True)
    lint.add_argument("--ledger", type=Path, help="read a review record, never write one")
    lint.add_argument("--approve", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args(argv)
    if getattr(args, "approve", False):
        print(
            "refusing to approve. Legal sign-off is a person writing the review record. This linter never auto-clears.",
            file=sys.stderr,
        )
        return 2
    refuse_course(args.out)
    report = apply_ledger(lint_path(args.source), args.ledger)
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "compliance.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    (args.out / "compliance.md").write_text(render_markdown(report), encoding="utf-8")
    print(f"{report['status']}  content {report['content_result']}  {args.out / 'compliance.json'}")
    return 0 if report["content_result"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
