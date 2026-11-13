"""Rasterise a spec. resvg is used when it is on PATH, otherwise CairoSVG."""

from __future__ import annotations

import hashlib
import shutil
import subprocess
from dataclasses import dataclass, field
from pathlib import Path

from .fonts import css_for
from .parser import parse
from .qa import QaReport, check_pixels, check_scene
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
    failures: list[str] = field(default_factory=list)


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
    resvg = shutil.which("resvg")
    if resvg:
        subprocess.run(
            [resvg, "--width", str(width), "--height", str(height), str(svg_path), str(png_path)],
            check=True,
        )
        return "resvg"
    import cairosvg

    cairosvg.svg2png(
        url=str(svg_path),
        write_to=str(png_path),
        output_width=width,
        output_height=height,
    )
    return "cairosvg"


def render_spec(spec: Spec, out: Path, preset: str | None = None, strict: bool = True) -> RenderResult:
    out = assert_safe_output(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    theme = get_theme(preset or spec.preset, spec.size)
    canvas = build_canvas(spec, theme)
    svg_path = out.with_suffix(".svg")
    svg_path.write_text(canvas.svg.tostring(css_for(svg_path)), encoding="utf-8")
    renderer = rasterize(svg_path, out, theme.width, theme.height)
    png = out.read_bytes()
    meta = canvas.meta()
    scene = check_scene(meta, theme)
    pixels_ok, pixel_detail = check_pixels(png, theme)
    scene.add("frame", pixels_ok, pixel_detail)
    if strict and not scene.ok:
        raise RuntimeError("QA failed for " + out.name + "\n" + "\n".join(scene.failures))
    digest = hashlib.md5(png).hexdigest()
    return RenderResult(
        png=png,
        svg_path=svg_path,
        png_path=out,
        spec=spec,
        theme=theme,
        meta=meta,
        qa=scene,
        checksum=digest,
        renderer=renderer,
        alt=alt_text(spec, meta),
        failures=list(scene.failures),
    )


def render_prompt(prompt: str, out: Path, preset: str = "house", size: str | None = None,
                  seed: int | None = None, use_llm: bool = False, strict: bool = True) -> RenderResult:
    if use_llm:
        from .llm import spec_from_llm

        spec = spec_from_llm(prompt)
    else:
        spec = parse(prompt)
    spec.preset = preset or spec.preset
    if size:
        from .parser import parse_size

        spec.size = parse_size(size)
    if seed is not None:
        spec.params["seed"] = seed
    return render_spec(spec, Path(out), preset=spec.preset, strict=strict)
