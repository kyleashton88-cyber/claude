"""Cursor fallback stills, starting at the ChatGPT web pause.

The web run records its pause in course/images/batch-web/progress.json
(live copy: /workspace/course-images/batch-web/progress.json). This tool
reads that file and continues at the next beat that does not already have
a PNG from the web run.

Generated files are marked FALLBACK in course/images/FALLBACK_MANIFEST.json.
Creative Studio sets qa to "pass" or "fail". A master is not rendered from
a fallback still until qa is pass.

This tool does not call the OpenAI API. It does not upload to Whop.
Pixel generation is Cursor's fallback, invoked with --describe so each
prompt can be drawn and then recorded with --record.

  python3 course/tools/fallback_images.py
  python3 course/tools/fallback_images.py --describe --limit 20
  python3 course/tools/fallback_images.py --record el-05-portfolio-risk-001
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from queue_order import ordered_requests

ROOT = Path(__file__).resolve().parents[2]
REQUESTS = ROOT / "IMAGE_REQUESTS.json"
MANIFEST = ROOT / "course" / "images" / "FALLBACK_MANIFEST.json"
PROGRESS_REPO = ROOT / "course" / "images" / "batch-web" / "progress.json"
PROGRESS_BOX = Path("/workspace/course-images/batch-web/progress.json")


def load_progress() -> tuple[dict | None, Path | None]:
    """Prefer the live box file, then the committed repo copy."""
    for path in (PROGRESS_BOX, PROGRESS_REPO):
        if path.is_file():
            return json.loads(path.read_text()), path
    return None, None


def load_manifest() -> dict:
    if not MANIFEST.is_file():
        return {"images": {}}
    data = json.loads(MANIFEST.read_text())
    data.setdefault("images", {})
    return data


def save_manifest(data: dict) -> None:
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text(json.dumps(data, indent=1) + "\n")


def paused(progress: dict | None) -> bool:
    if not progress:
        return False
    status = str(progress.get("status") or progress.get("state") or "").lower()
    if progress.get("paused") is True or status in {"paused", "pause", "rate_limit", "limited"}:
        return True
    if progress.get("paused") is False or status in {"running", "active"}:
        return False
    return any(progress.get(key) for key in ("next_request_id", "last_request_id", "last_completed_id", "cursor", "next_index"))


def start_index(ordered: list[dict], progress: dict | None) -> int | None:
    if not paused(progress):
        return None
    assert progress is not None
    ids = [item["id"] for item in ordered]
    nxt = progress.get("next_request_id") or progress.get("cursor") or progress.get("next_id")
    if isinstance(nxt, str) and nxt in ids:
        return ids.index(nxt)
    last = progress.get("last_request_id") or progress.get("last_completed_id") or progress.get("last_id")
    if isinstance(last, str) and last in ids:
        return ids.index(last) + 1
    if isinstance(progress.get("next_index"), int):
        return max(0, progress["next_index"])
    return 0


def image_entry(manifest: dict, out_path: str) -> dict:
    images = manifest.get("images") or {}
    if isinstance(images, dict):
        return images.get(out_path) or {}
    for entry in images:
        if entry.get("path") == out_path or entry.get("out_path") == out_path:
            return entry
    return {}


def web_claimed(item: dict, manifest: dict) -> bool:
    path = ROOT / item["out_path"]
    if not path.is_file() or path.stat().st_size < 1000:
        return False
    entry = image_entry(manifest, item["out_path"])
    return not (entry and entry.get("marker") == "FALLBACK")


V2_FALLBACK_MATCH = "One small off-white rounded card"


def prompt_retired(text: str, manifest: dict | None = None) -> bool:
    """The v2 flat worksheet prompt is retired and must not be sent again."""
    if V2_FALLBACK_MATCH in (text or ""):
        return True
    retired = (manifest or {}).get("retired_prompts") or {}
    for entry in retired.values():
        if isinstance(entry, dict) and entry.get("status") == "retired":
            match = entry.get("match") or ""
            if match and match in (text or ""):
                return True
    return False


def needs_fallback(item: dict, manifest: dict, retry_failed: bool) -> bool:
    if prompt_retired(item.get("prompt") or "", manifest):
        return False
    if web_claimed(item, manifest):
        return False
    path = ROOT / item["out_path"]
    entry = image_entry(manifest, item["out_path"])
    if entry.get("prompt_status") == "retired" or entry.get("reusable") is False:
        return False
    exists = path.is_file() and path.stat().st_size >= 1000
    if not exists:
        return True
    qa = str((entry or {}).get("qa") or "pending").lower()
    return retry_failed and qa == "fail"


def queue(retry_failed: bool = False) -> tuple[list[dict], str]:
    payload = json.loads(REQUESTS.read_text())
    ordered = ordered_requests(payload["requests"])
    progress, path = load_progress()
    begin = start_index(ordered, progress)
    if begin is None:
        where = str(path) if path else "course/images/batch-web/progress.json"
        return [], f"no pause recorded ({where})"
    manifest = load_manifest()
    pending = []
    for item in ordered[begin:]:
        if needs_fallback(item, manifest, retry_failed):
            pending.append(item)
    return pending, f"pause {path} start {ordered[begin]['id'] if begin < len(ordered) else 'end'}"


def record(request_id: str) -> None:
    payload = json.loads(REQUESTS.read_text())
    item = next(row for row in payload["requests"] if row["id"] == request_id)
    data = load_manifest()
    if prompt_retired(item.get("prompt") or "", data):
        raise SystemExit(f"refusing {request_id}: v2 fallback prompt is retired")
    path = ROOT / item["out_path"]
    if not path.is_file() or path.stat().st_size < 1000:
        raise SystemExit(f"missing png for {request_id}: {item['out_path']}")
    if path.suffix.lower() != ".png":
        raise SystemExit(f"refusing {request_id}: stills are lossless PNG, never JPEG")
    previous = image_entry(data, item["out_path"])
    if previous.get("prompt_status") == "retired" or previous.get("reusable") is False:
        raise SystemExit(f"refusing {request_id}: this fallback prompt is retired")
    qa = previous.get("qa") or previous.get("status") or "pending"
    if str(qa).lower() in {"pass", "passed"}:
        print(f"keep pass {item['out_path']}")
        return
    entry = {
        "marker": "FALLBACK",
        "source": "cursor-fallback",
        "qa": "pending",
        "request_id": item["id"],
        "lesson": item["lesson"],
        "beat": item["beat"],
        "palette": item.get("palette"),
        "out_path": item["out_path"],
        "path": item["out_path"],
    }
    images = data.get("images")
    if isinstance(images, dict):
        images[item["out_path"]] = entry
    elif isinstance(images, list):
        images[:] = [row for row in images if row.get("path") != item["out_path"] and row.get("out_path") != item["out_path"]]
        images.append(entry)
    else:
        data["images"] = [entry]
    data["rule"] = (
        "Creative Studio sets qa to pass or fail. Masters stay unrendered until qa is pass. "
        "The v2 fallback prompt is retired and must not be reused."
    )
    save_manifest(data)
    print(f"recorded FALLBACK {item['out_path']}")


def self_test() -> None:
    ordered = [
        {"id": "el-05-portfolio-risk-001", "lesson": "el-05-portfolio-risk", "beat": 1, "out_path": "a"},
        {"id": "el-05-portfolio-risk-002", "lesson": "el-05-portfolio-risk", "beat": 2, "out_path": "b"},
        {"id": "bp-01-introduction-001", "lesson": "bp-01-introduction", "beat": 1, "out_path": "c"},
    ]
    assert start_index(ordered, None) is None
    assert start_index(ordered, {"paused": False}) is None
    assert start_index(ordered, {"paused": True, "next_request_id": "el-05-portfolio-risk-002"}) == 1
    assert start_index(ordered, {"status": "rate_limit", "last_request_id": "el-05-portfolio-risk-001"}) == 1
    assert ordered_requests.__doc__ is None or True
    from queue_order import ordered_requests as order
    ranked = order([
        {"id": "bp-01-introduction-001", "lesson": "bp-01-introduction", "beat": 1},
        {"id": "el-04-dynamic-spacing-002", "lesson": "el-04-dynamic-spacing", "beat": 2},
        {"id": "el-05-portfolio-risk-003", "lesson": "el-05-portfolio-risk", "beat": 3},
        {"id": "lesson-01-1-001", "lesson": "lesson-01-1", "beat": 1},
    ])
    assert [item["id"] for item in ranked] == [
        "el-05-portfolio-risk-003",
        "el-04-dynamic-spacing-002",
        "bp-01-introduction-001",
        "lesson-01-1-001",
    ]
    assert prompt_retired("card with One small off-white rounded card inside")
    assert not prompt_retired("glass card, teal glow, headline")
    assert needs_fallback(
        {"out_path": "course/images/x.png", "prompt": "One small off-white rounded card"},
        {"images": {}},
        False,
    ) is False


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--describe", action="store_true")
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--record")
    parser.add_argument("--retry-failed", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    self_test()
    if args.self_test:
        print("self-test ok")
        return
    if args.record:
        record(args.record)
        return
    pending, why = queue(args.retry_failed)
    print(why)
    print(f"unclaimed_from_pause {len(pending)}")
    shown = pending[: max(args.limit, 0)]
    if args.describe:
        for item in shown:
            print("---")
            print(item["id"])
            print(item["out_path"])
            print(item.get("palette"))
            print(item["prompt"])
    else:
        for item in shown:
            print(f"{item['id']} {item['out_path']} {item.get('palette')}")
    if not pending:
        raise SystemExit(0)


if __name__ == "__main__":
    main()
