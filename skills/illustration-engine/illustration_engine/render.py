"""Rasterise a spec. resvg is used when it runs, otherwise CairoSVG.

Cairo finds the bundled faces through a private fontconfig file.
resvg is given that same folder and told to skip system fonts.
"""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
from dataclasses import dataclass, field
from pathlib import Path

from .fonts import FONT_DIR, css_for, install
from .parser import parse
from .policy import RefusedPrompt
from .qa import QaReport, check_headline_gap, check_pixels, check_scene
from .spec import Spec
from .theme import Theme, get_theme
from .types import draw

class UnsafeOutput(RuntimeError):
    pass


@dataclass
class RenderResult:
    png: bytes
    svg_path: Path | None
    png_path: Path | None
    spec: Spec
    theme: Theme
    meta: dict
    qa: QaReport
    checksum: str
    renderer: str
    alt: str
    mode: str = "normal"
    failures: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)


def assert_safe_output(path: Path) -> Path:
    resolved = path.expanduser().resolve()
    if "course" in resolved.parts:
        raise UnsafeOutput(f"refusing to write inside a course path: {resolved}")
    return resolved


def alt_text(spec: Spec, meta: dict) -> str:
    concept = str((spec.params or {}).get("concept") or "").strip()
    if concept and "@" not in concept and "http" not in concept.lower():
        sentence = concept.rstrip(".")
        if len(sentence) > 180:
            sentence = sentence[:177].rstrip() + "..."
        return sentence + "."
    idea = meta.get("idea") or "A teaching diagram."
    labels = meta.get("labels") or []
    if labels:
        return f"{idea} Labels: {', '.join(labels)}."
    return idea


def build_canvas(spec: Spec, theme: Theme):
    from .canvas import Canvas

    canvas = Canvas(theme)
    canvas.backdrop()
    draw(canvas, spec)
    return canvas


def rasterize(svg_path: Path, png_path: Path, width: int, height: int) -> str:
    install()
    resvg = shutil.which("resvg")
    if resvg:
        cmd = [
            resvg,
            "--use-fonts-dir", str(FONT_DIR),
            "--skip-system-fonts",
            "--width", str(width),
            "--height", str(height),
            str(svg_path),
            str(png_path),
        ]
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            return "resvg"
        except (OSError, subprocess.CalledProcessError):
            pass
    import cairosvg

    cairosvg.svg2png(
        url=str(svg_path),
        write_to=str(png_path),
        output_width=width,
        output_height=height,
    )
    return "cairosvg"


def _replace(src: Path, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    os.replace(src, dest)


def manifest_path(directory: Path) -> Path:
    return directory / "MANIFEST.json"


def empty_manifest(mode: str) -> dict:
    return {
        "source": "illustration-engine",
        "mode": mode,
        "fallback_tier": mode == "fallback",
        "rule": (
            "In-house illustration engine. These files are not course stills. "
            "The engine does not write into course/. A router may copy an approved "
            "fallback plate into course/images/_fallback_quarantine/."
        ),
        "images": [],
    }


def read_manifest(directory: Path) -> dict:
    path = manifest_path(directory)
    if not path.is_file():
        return empty_manifest("normal")
    data = json.loads(path.read_text(encoding="utf-8"))
    data.setdefault("images", [])
    data.setdefault("source", "illustration-engine")
    return data


def write_manifest_atomic(directory: Path, data: dict) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    path = manifest_path(directory)
    tmp = directory / ".MANIFEST.json.partial"
    tmp.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    os.replace(tmp, path)


def upsert_manifest(directory: Path, entry: dict, mode: str) -> None:
    data = read_manifest(directory)
    data["source"] = "illustration-engine"
    data["mode"] = mode
    data["fallback_tier"] = mode == "fallback"
    images = [row for row in data.get("images") or [] if row.get("file") != entry["file"]]
    images.append(entry)
    data["images"] = images
    write_manifest_atomic(directory, data)


def entry_from_result(name: str, result: RenderResult) -> dict:
    return {
        "file": name,
        "path": name,
        "preset": result.theme.name,
        "width": result.theme.width,
        "height": result.theme.height,
        "checksum": result.checksum,
        "md5": result.checksum,
        "renderer": result.renderer,
        "alt": result.alt,
        "spec": result.spec.as_dict(),
        "idea": result.meta.get("idea"),
        "labels": result.meta.get("labels"),
        "example": result.meta.get("example"),
        "qa_ok": result.qa.ok,
        "qa": result.qa.checks,
        "mode": result.mode,
        "fallback_tier": result.mode == "fallback",
        "source": "illustration-engine",
    }


def render_spec(spec: Spec, out: Path, preset: str | None = None, strict: bool = True,
                mode: str = "normal") -> RenderResult:
    out = assert_safe_output(out)
    if out.suffix.lower() != ".png":
        raise UnsafeOutput(f"refusing {out.name}: plates are PNG")
    theme = get_theme(preset or spec.preset, spec.size)
    canvas = build_canvas(spec, theme)
    partial = out.parent / ".partial"
    partial.mkdir(parents=True, exist_ok=True)
    svg_tmp = partial / f"{out.stem}.svg"
    png_tmp = partial / out.name
    svg_tmp.write_text(canvas.svg.tostring(css_for(svg_tmp)), encoding="utf-8")
    renderer = rasterize(svg_tmp, png_tmp, theme.width, theme.height)
    png = png_tmp.read_bytes()
    meta = canvas.meta()
    scene = check_scene(meta, theme)
    pixels_ok, pixel_detail = check_pixels(png, theme)
    scene.add("frame", pixels_ok, pixel_detail)
    gap_ok, gap_detail = check_headline_gap(png, meta.get("marks") or [])
    scene.add("word spacing", gap_ok, gap_detail)
    digest = hashlib.md5(png).hexdigest()
    result = RenderResult(
        png=png,
        svg_path=out.with_suffix(".svg"),
        png_path=out,
        spec=spec,
        theme=theme,
        meta=meta,
        qa=scene,
        checksum=digest,
        renderer=renderer,
        alt=alt_text(spec, meta),
        mode=mode,
        failures=list(scene.failures),
    )
    if not scene.ok:
        failed = out.parent / ".failed"
        failed.mkdir(parents=True, exist_ok=True)
        _replace(png_tmp, failed / out.name)
        _replace(svg_tmp, failed / f"{out.stem}.svg")
        if out.exists():
            out.unlink()
        svg_final = out.with_suffix(".svg")
        if svg_final.exists():
            svg_final.unlink()
        if strict:
            raise RuntimeError("QA failed for " + out.name + "\n" + "\n".join(scene.failures))
        return result
    # Manifest lists the plate before the final name appears, so a published file has an entry.
    upsert_manifest(out.parent, entry_from_result(out.name, result), mode)
    _replace(png_tmp, out)
    _replace(svg_tmp, out.with_suffix(".svg"))
    return result


def render_prompt(prompt: str, out: Path, preset: str = "house", size: str | None = None,
                  seed: int | None = None, use_llm: bool = False, strict: bool = True,
                  fallback: bool = False, allow_generic: bool = False) -> RenderResult:
    mode = "fallback" if fallback else "normal"
    if use_llm:
        from .llm import spec_from_llm

        spec = spec_from_llm(prompt)
        from .policy import enforce_mode, screen_value
        screened, notes = screen_value(spec.as_dict(), allow_generic=allow_generic)
        from .parser import spec_from_dict
        spec = enforce_mode(spec_from_dict(screened), fallback=fallback)
    else:
        spec = parse(prompt, fallback=fallback, allow_generic=allow_generic)
        notes = ["exchange"] if spec.params.get("replaced_names") else []
    spec.preset = preset or spec.preset
    if size:
        from .parser import parse_size

        spec.size = parse_size(size)
    if seed is not None:
        spec.params["seed"] = seed
    result = render_spec(spec, Path(out), preset=spec.preset, strict=strict, mode=mode)
    result.notes = notes
    return result
