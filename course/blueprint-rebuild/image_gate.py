#!/usr/bin/env python3
"""Refuse a Blueprint render unless every image it uses is on a pass list.

Creative Studio writes blueprint-image-qa/BP01-03_PASS_LIST.json with
path, lesson, and pass/fail. A missing row or a fail stops the build
before a frame is drawn. Code-drawn charts, the title card, the end
card, and the thumbnail are images too, listed as code-drawn/ paths.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_LIST = ROOT / "blueprint-image-qa" / "BP01-03_PASS_LIST.json"

COVER = "course/images/style-ref/01M6MSHVNHX3WQH81XS8KQK1HT.png"
MASCOT = "course/images/mascot/blueprint-mascot.png"
OLD_MASCOT = "course/images/fallback/el-06-circuit-breakers/28.png"
BRAND = [
    (COVER, "title-art"),
    (MASCOT, "mascot"),
]
ANALOGY = {
    "ladder": "course/images/blueprint-analogies/analogy-ladder.png",
    "fence": "course/images/blueprint-analogies/analogy-fence.png",
    "list": "course/images/blueprint-analogies/analogy-list.png",
    "buckets": "course/images/blueprint-analogies/analogy-buckets.png",
}


def _studio():
    path = ROOT / "course/blueprint-rebuild/studio.py"
    spec = importlib.util.spec_from_file_location("blueprint_studio", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _slug(text: str) -> str:
    keep = "".join(ch.lower() if ch.isalnum() else "-" for ch in text)
    return "-".join(part for part in keep.split("-") if part) or "shot"


def images_for_lesson(sid: str) -> list[dict]:
    """Every image the lesson render would use, in stable order."""
    studio = _studio()
    shots = studio.plan(sid)
    rows: list[dict] = []
    seen: set[str] = set()

    def add(path: str, kind: str) -> None:
        key = path.replace("\\", "/").lstrip("./")
        if key in seen:
            return
        seen.add(key)
        rows.append({"path": key, "lesson": sid, "kind": kind})

    for path, kind in BRAND:
        add(path, kind)
    for shot in shots:
        still = shot.get("still")
        if still:
            rel = str(Path(still).resolve().relative_to(ROOT)).replace("\\", "/")
            add(rel, "analogy-still")
        elif shot.get("analogy"):
            add(ANALOGY[shot["analogy"]], "analogy-still")
        if shot.get("kind") in {"chart", "analogy"}:
            chapter = _slug(str(shot.get("chapter") or "chart"))
            chart = _slug(str(shot.get("chart") or "chart"))
            add(f"code-drawn/{sid}/chart/{chart}/{chapter}", "code-drawn-chart")
    add(f"code-drawn/{sid}/title-card", "title-card")
    add(f"code-drawn/{sid}/end-card", "end-card")
    add(f"code-drawn/{sid}/thumbnail", "thumbnail")
    folder = ROOT / "course/images" / sid
    if folder.is_dir():
        for png in sorted(folder.glob("*.png")):
            add(str(png.relative_to(ROOT)).replace("\\", "/"), "lesson-still")
    return rows


def load_pass_list(path: Path) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, dict):
        rows = data.get("images") or data.get("items") or []
    else:
        rows = data
    if not isinstance(rows, list):
        raise SystemExit(f"pass list {path} is not a list of images")
    return rows


def _passed(row: dict) -> bool:
    if "pass" in row:
        value = row["pass"]
        if isinstance(value, str):
            return value.strip().lower() in {"pass", "passed", "true", "yes"}
        return bool(value)
    result = str(row.get("result") or row.get("status") or "").strip().lower()
    return result in {"pass", "passed"}


def _norm(path: str) -> str:
    return path.replace("\\", "/").lstrip("./")


def git_blob(rel: str) -> str | None:
    """Blob id of the file on disk. A different id is a different image."""
    path = ROOT / rel
    if not path.is_file():
        return None
    proc = subprocess.run(
        ["git", "hash-object", "--", str(path)],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        return None
    return proc.stdout.strip().lower()


def blob_problem(rel: str, row: dict) -> str | None:
    """A path match with a different scored_blob is a fail."""
    expected = str(row.get("scored_blob") or "").strip().lower()
    if not expected:
        return None
    actual = git_blob(rel)
    if actual is None:
        return f"scored_blob set but file missing: {rel}"
    if actual != expected and not actual.startswith(expected):
        return f"blob mismatch: {rel} is {actual} not scored_blob {expected}"
    return None


def problems_for(sid: str, pass_list: Path) -> list[str]:
    if not pass_list.is_file():
        return [f"pass list not found: {pass_list}"]
    rows = load_pass_list(pass_list)
    indexed: dict[tuple[str, str], dict] = {}
    for row in rows:
        path = _norm(str(row.get("path") or ""))
        lesson = str(row.get("lesson") or "")
        if path:
            indexed[(path, lesson)] = row
    problems = []
    for item in images_for_lesson(sid):
        path = item["path"]
        if path == OLD_MASCOT or path.endswith("el-06-circuit-breakers/28.png"):
            problems.append(f"old mascot is not allowed: {path}")
            continue
        if path == COVER and item["kind"] != "title-art":
            problems.append(f"title art may only be the wordmark crop: {path}")
            continue
        row = indexed.get((path, sid))
        if row is None:
            problems.append(f"missing from pass list: {path} ({item['kind']})")
            continue
        if not _passed(row):
            status = str(row.get("status") or "fail")
            problems.append(f"not a pass ({status}): {path} ({item['kind']})")
        found = blob_problem(path, row)
        if found:
            problems.append(found)
    return problems


def require(sid: str, pass_list: Path | None = None) -> None:
    path = pass_list or DEFAULT_LIST
    found = problems_for(sid, path)
    if found:
        lines = "\n".join(found)
        raise SystemExit(f"image quality gate failed for {sid}\n{lines}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Check a lesson against an image pass list")
    parser.add_argument("--id", required=True)
    parser.add_argument("--pass-list", type=Path, default=DEFAULT_LIST)
    parser.add_argument("--list", action="store_true", help="print the images this lesson uses")
    args = parser.parse_args()
    if args.list:
        for row in images_for_lesson(args.id):
            print(f"{row['lesson']}\t{row['kind']}\t{row['path']}")
        return
    require(args.id, args.pass_list)
    print(f"image gate pass {args.id}")


if __name__ == "__main__":
    main()
