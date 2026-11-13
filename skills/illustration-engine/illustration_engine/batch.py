"""Render every slot in a lesson file. Writes only under the output directory."""

from __future__ import annotations

import json
from pathlib import Path

import yaml

from .parser import parse, spec_from_request
from .qa import BEGINNER_INTRO, beginner_lines
from .render import RenderResult, assert_safe_output, entry_from_result, render_spec, write_manifest_atomic, empty_manifest
from .spec import Spec


def load_slots(source: Path, lesson: str | None = None, *, fallback: bool = False,
               allow_generic: bool = False) -> list[Spec]:
    text = source.read_text(encoding="utf-8")
    if source.suffix.lower() in {".yaml", ".yml"}:
        data = yaml.safe_load(text)
        return _slots_from_yaml(data, fallback=fallback, allow_generic=allow_generic)
    data = json.loads(text)
    requests = data["requests"] if isinstance(data, dict) and "requests" in data else data
    if lesson:
        requests = [row for row in requests if row.get("lesson") == lesson]
    if not requests:
        raise SystemExit(f"no slots found in {source}" + (f" for {lesson}" if lesson else ""))
    specs = []
    for row in requests:
        if row.get("prompt") and not row.get("concept"):
            spec = parse(str(row["prompt"]), fallback=fallback, allow_generic=allow_generic)
            spec.file = row.get("file") or f"{len(specs) + 1:03d}.png"
            spec.source_id = row.get("id")
            if row.get("size"):
                from .parser import parse_size
                spec.size = parse_size(row["size"])
            specs.append(spec)
        else:
            specs.append(spec_from_request(row, fallback=fallback, allow_generic=allow_generic))
    return specs


def _slots_from_yaml(data: dict, *, fallback: bool = False, allow_generic: bool = False) -> list[Spec]:
    if not isinstance(data, dict) or "slots" not in data:
        raise SystemExit("a lesson YAML needs a slots list")
    preset = data.get("preset") or "house"
    size = data.get("size")
    specs = []
    for index, slot in enumerate(data["slots"], start=1):
        if slot.get("spec"):
            spec = parse(json.dumps(slot["spec"]) if isinstance(slot["spec"], dict) else str(slot["spec"]),
                         fallback=fallback, allow_generic=allow_generic)
        elif slot.get("prompt"):
            spec = parse(str(slot["prompt"]), fallback=fallback, allow_generic=allow_generic)
        else:
            raise SystemExit(f"slot {index} needs prompt or spec")
        spec.file = slot.get("file") or f"{index:03d}.png"
        spec.preset = slot.get("preset") or preset
        if slot.get("size") or size:
            from .parser import parse_size
            spec.size = parse_size(slot.get("size") or size)
        specs.append(spec)
    return specs


def write_reports(out_dir: Path, results: list[tuple[str, RenderResult]], mode: str = "normal") -> None:
    seen: dict[str, dict] = {}
    beginner = [BEGINNER_INTRO, ""]
    qa_lines = ["# QA", ""]
    alt_lines = []
    for name, result in results:
        seen[name] = entry_from_result(name, result)
        qa_lines.append(f"## {name}")
        qa_lines.extend(f"- {line}" for line in result.qa.checks)
        qa_lines.append("")
        beginner.extend(beginner_lines(name, result.meta, result.qa))
        beginner.append("")
        alt_lines.append(name)
        alt_lines.append(result.alt)
        alt_lines.append("")
    manifest = empty_manifest(mode)
    manifest["images"] = list(seen.values())
    write_manifest_atomic(out_dir, manifest)
    (out_dir / "QA.md").write_text("\n".join(qa_lines), encoding="utf-8")
    (out_dir / "BEGINNER.md").write_text("\n".join(beginner), encoding="utf-8")
    (out_dir / "ALT.txt").write_text("\n".join(alt_lines), encoding="utf-8")


def render_lesson(source: Path, out_dir: Path, lesson: str | None = None, preset: str = "house",
                  strict: bool = True, fallback: bool = False, allow_generic: bool = False) -> list[RenderResult]:
    out_dir = assert_safe_output(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    mode = "fallback" if fallback else "normal"
    specs = load_slots(source, lesson, fallback=fallback, allow_generic=allow_generic)
    results: list[tuple[str, RenderResult]] = []
    rendered: list[RenderResult] = []
    for index, spec in enumerate(specs, start=1):
        name = spec.file or f"{index:03d}.png"
        if not name.endswith(".png"):
            name += ".png"
        spec.preset = preset or spec.preset
        result = render_spec(spec, out_dir / name, preset=spec.preset, strict=strict, mode=mode)
        results.append((name, result))
        rendered.append(result)
        print(f"rendered {name} {result.theme.width}x{result.theme.height} {result.spec.type}")
    write_reports(out_dir, results, mode=mode)
    return rendered
