"""A review pack for a person. It does not upload or publish."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

VP = Path(__file__).resolve().parents[2]
if str(VP) not in sys.path:
    sys.path.insert(0, str(VP))

from lib.ffmpeg_util import ffmpeg_bin, probe  # noqa: E402

FONT = VP / "templates" / "assets" / "fonts" / "Inter-Bold.ttf"


def contact_sheet(master: Path, dest: Path, frames: int = 6) -> Path:
    info = probe(master)
    duration = float((info.get("format") or {}).get("duration") or 0)
    if duration <= 0:
        raise RuntimeError(f"no duration on {master}")
    work = dest.parent / "_frames"
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)
    times = [duration * (index + 0.5) / frames for index in range(frames)]
    images = []
    for index, second in enumerate(times):
        png = work / f"{index:02d}.png"
        subprocess.check_call(
            [
                ffmpeg_bin(),
                "-y",
                "-v",
                "error",
                "-ss",
                f"{min(second, max(0, duration - 0.05)):.3f}",
                "-i",
                str(master),
                "-frames:v",
                "1",
                str(png),
            ]
        )
        images.append(Image.open(png).convert("RGB"))
    thumb_w, thumb_h = 320, 180
    cols = 3
    rows = (len(images) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * thumb_w, rows * (thumb_h + 28)), (0, 8, 27))
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.truetype(str(FONT), 16) if FONT.is_file() else ImageFont.load_default()
    for index, image in enumerate(images):
        tile = image.resize((thumb_w, thumb_h))
        col, row = index % cols, index // cols
        x, y = col * thumb_w, row * (thumb_h + 28)
        sheet.paste(tile, (x, y))
        draw.text((x + 8, y + thumb_h + 4), f"{times[index]:.1f}s", fill=(244, 248, 252), font=font)
    dest.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(dest)
    shutil.rmtree(work)
    return dest


def build_pack(
    *,
    folder: Path,
    master: Path,
    qa_report: Path | None,
    compliance_report: Path | None,
    transcript: Path | None,
    state: dict,
) -> Path:
    folder.mkdir(parents=True, exist_ok=True)
    sheet = contact_sheet(master, folder / "contact-sheet.png")
    copied = {"contact_sheet": str(sheet), "master": str(master)}
    if qa_report and qa_report.is_file():
        target = folder / "qa-report.json"
        shutil.copyfile(qa_report, target)
        copied["qa_report"] = str(target)
    if compliance_report and compliance_report.is_file():
        target = folder / "compliance-report.json"
        shutil.copyfile(compliance_report, target)
        copied["compliance_report"] = str(target)
    if transcript and transcript.is_file():
        target = folder / f"transcript{transcript.suffix or '.txt'}"
        shutil.copyfile(transcript, target)
        copied["transcript"] = str(target)
    (folder / "state.json").write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# Review pack",
        "",
        "For a person to read. This folder does not publish, upload, or send mail.",
        "",
        f"Master: `{master}`",
        f"Publish allowed: **{str(state.get('publish_allowed')).lower()}**",
        "",
        "Contents:",
        "",
        f"- Contact sheet: `{sheet.name}`",
    ]
    for key in ("qa_report", "compliance_report", "transcript"):
        if key in copied:
            lines.append(f"- {key.replace('_', ' ')}: `{Path(copied[key]).name}`")
    if state.get("blocked_by"):
        lines.extend(["", "Still blocking publish:", ""])
        for reason in state["blocked_by"]:
            lines.append(f"- {reason}")
    lines.append("")
    (folder / "README.md").write_text("\n".join(lines), encoding="utf-8")
    return folder
