"""Split IMAGE_REQUESTS.json into ChatGPT web prompt sheets of 20.

Order: Elite el-05 through el-11, then the rest of Elite, then Blueprint, then
On-Chain Operator. Each sheet lists the target path and the exact prompt.
Does not generate images and does not upload to Whop.

  python3 course/tools/export_web_batches.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from queue_order import ordered_requests

ROOT = Path(__file__).resolve().parents[2]
REQUESTS = ROOT / "IMAGE_REQUESTS.json"
OUT = ROOT / "course" / "image-batches"
SIZE = 20


def sheets(requests: list[dict], size: int = SIZE) -> list[list[dict]]:
    ordered = ordered_requests(requests)
    return [ordered[i:i + size] for i in range(0, len(ordered), size)]


def render_sheet(number: int, batch: list[dict], total: int) -> str:
    lines = [
        f"# Batch {number:03d} of {total:03d}",
        "",
        "ChatGPT web stills. Paste one prompt at a time. Save the PNG at the path under it. Do not draw a replacement in code. Elite stays teal. Blueprint and On-Chain Operator stay navy and cyan.",
        "",
    ]
    for item in batch:
        lines.extend([
            f"## {item['id']}",
            "",
            f"- Path: `{item['out_path']}`",
            f"- Lesson: `{item.get('lesson')}`",
            f"- Beat: {item.get('beat')}",
            f"- Palette: {item.get('palette')}",
            "",
            item["prompt"],
            "",
        ])
    return "\n".join(lines)


def main() -> None:
    payload = json.loads(REQUESTS.read_text())
    batches = sheets(payload["requests"])
    OUT.mkdir(parents=True, exist_ok=True)
    index = [
        "# ChatGPT web batches",
        "",
        "Order: Elite `el-05` through `el-11`, then `el-01` through `el-04`, then Blueprint, then On-Chain Operator.",
        f"Sheets: {len(batches)}. Prompts: {payload['count']}. Size: {SIZE}.",
        "",
    ]
    for i, batch in enumerate(batches, start=1):
        name = f"batch-{i:03d}.md"
        (OUT / name).write_text(render_sheet(i, batch, len(batches)))
        first = batch[0]["id"]
        last = batch[-1]["id"]
        index.append(f"- `{name}`: {first} → {last}")
    (OUT / "INDEX.md").write_text("\n".join(index) + "\n")
    print(f"sheets {len(batches)} prompts {payload['count']} dir {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
