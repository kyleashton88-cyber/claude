"""Write report.json and report.md."""

from __future__ import annotations

import json
from pathlib import Path


def write_reports(payload: dict, dest: Path) -> tuple[Path, Path]:
    dest.mkdir(parents=True, exist_ok=True)
    json_path = dest / "report.json"
    md_path = dest / "report.md"
    json_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    md_path.write_text(render_markdown(payload), encoding="utf-8")
    return json_path, md_path


def render_markdown(payload: dict) -> str:
    window = payload.get("length_window_seconds") or [0, 0]

    def _seconds(value: float) -> str:
        if abs(value - round(value)) < 0.001:
            return f"{value:.0f}s"
        return f"{value:.2f}s"

    lines = [
        "# Quality gate",
        "",
        f"Result: **{payload['result'].upper()}**",
        "",
        f"Format: {payload.get('format_label')} (`{payload.get('format')}`), "
        f"{_seconds(window[0])}–{_seconds(window[1])}.",
        f"Master: `{payload.get('master')}`",
        "",
        "Loudness fails the gate when it is outside the window. It is not only printed.",
        f"Target {payload.get('loudness_target_lufs')} LUFS ± {payload.get('loudness_tolerance_lu')}, "
        f"true peak at or below {payload.get('true_peak_max_dbtp')} dBTP.",
        "",
        "This gate supersedes the 15-minute minimum. Those older files stay where they are:",
        "",
    ]
    for item in payload.get("supersedes") or []:
        lines.append(f"- {item}")
    lines.extend(
        [
            "",
            "A Blueprint lesson of 6:15 is inside the 4–10 minute window.",
            "",
            "| Check | Result | Detail |",
            "|---|---|---|",
        ]
    )
    for check in payload.get("checks") or []:
        detail = (check.get("detail") or "").replace("|", "/")
        lines.append(f"| {check['id']} | {check['result'].upper()} | {detail} |")
    if payload.get("failed"):
        lines.extend(["", "Failed: " + ", ".join(payload["failed"]), ""])
    else:
        lines.extend(["", "Every check passed.", ""])
    lines.append("This report does not publish the master.")
    lines.append("")
    return "\n".join(lines)
