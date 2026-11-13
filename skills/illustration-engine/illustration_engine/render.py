"""Rasterise a spec. resvg is used when it runs, otherwise CairoSVG.

Cairo finds the bundled faces through a private fontconfig file.
resvg is given that same folder and told to skip system fonts.
"""

from __future__ import annotations

import hashlib
import json
import logging
import os
import shutil
import subprocess
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

from .fonts import FONT_DIR, css_for, install
from .parser import parse
from .policy import RefusedPrompt
from .qa import QaReport, check_headline_gap, check_pixels, check_scene, headline_stem, ink_coverage
from .spec import Spec
from .theme import Theme, get_theme
from .types import draw

log = logging.getLogger("illustration_engine")
ENGINE_PROVIDER = "illustration-engine"
ENGINE_VERSION = "1.0.0"
RASTER_TIMEOUT_SECONDS = 45


class UnsafeOutput(RuntimeError):
    pass


class RasterFailed(RuntimeError):
    """Neither resvg nor CairoSVG produced a PNG."""


class PlateCollision(RuntimeError):
    """Two slots in one job asked for the same filename."""


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
    job_id: str = ""
    prompt_hash: str = ""
    sha256: str = ""
    created_at: str = ""
    cached: bool = False


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
    resvg_error = "resvg is not on PATH"
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
            subprocess.run(cmd, check=True, capture_output=True, timeout=RASTER_TIMEOUT_SECONDS)
            return "resvg"
        except subprocess.TimeoutExpired as exc:
            resvg_error = f"resvg timed out after {RASTER_TIMEOUT_SECONDS}s"
            log.warning("%s for %s", resvg_error, svg_path.name)
            resvg_error = f"{resvg_error}: {exc}"
        except (OSError, subprocess.CalledProcessError) as exc:
            detail = exc.stderr.decode("utf-8", "replace").strip() if isinstance(exc, subprocess.CalledProcessError) and exc.stderr else str(exc)
            resvg_error = f"resvg failed: {detail or exc}"
            log.warning("%s for %s", resvg_error, svg_path.name)
    else:
        log.warning("resvg is not on PATH; trying CairoSVG for %s", svg_path.name)
    try:
        import cairosvg

        cairosvg.svg2png(
            url=str(svg_path),
            write_to=str(png_path),
            output_width=width,
            output_height=height,
        )
    except Exception as exc:
        raise RasterFailed(
            f"neither resvg nor CairoSVG could rasterize {svg_path.name}. {resvg_error}. CairoSVG: {exc}"
        ) from exc
    log.warning("rasterized %s with CairoSVG after resvg did not (%s)", svg_path.name, resvg_error)
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


def prompt_digest(spec: Spec, prompt: str | None = None) -> str:
    payload = prompt if prompt else json.dumps(spec.as_dict(), sort_keys=True, default=str)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def file_sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def entry_from_result(name: str, result: RenderResult) -> dict:
    lesson = (result.spec.params or {}).get("lesson")
    return {
        "file": name,
        "path": name,
        "job_id": result.job_id,
        "lesson": lesson,
        "prompt_hash": result.prompt_hash,
        "provider": ENGINE_PROVIDER,
        "provider_version": ENGINE_VERSION,
        "reason": f"{result.mode} {result.spec.type}",
        "created_at": result.created_at,
        "updated_at": _now(),
        "qa_status": "pass" if result.qa.ok else "fail",
        "qa_ok": result.qa.ok,
        "reviewer": "engine-preflight",
        "sha256": result.sha256,
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
        "qa": result.qa.checks,
        "mode": result.mode,
        "fallback_tier": result.mode == "fallback",
        "source": "illustration-engine",
    }


def drop_manifest_entry(directory: Path, filename: str, rejected: dict | None = None) -> None:
    """Remove a plate from the published list so a missing file is not still listed."""
    data = read_manifest(directory)
    data["images"] = [row for row in data.get("images") or [] if row.get("file") != filename]
    if rejected:
        prior = [row for row in data.get("rejected") or [] if row.get("file") != filename]
        prior.append(rejected)
        data["rejected"] = prior
    write_manifest_atomic(directory, data)


def lookup_cached(directory: Path, filename: str, digest: str) -> dict | None:
    if not (directory / filename).is_file():
        return None
    for row in read_manifest(directory).get("images") or []:
        if row.get("file") != filename or row.get("prompt_hash") != digest or not row.get("qa_ok"):
            continue
        payload = (directory / filename).read_bytes()
        if row.get("sha256") and row["sha256"] != file_sha256(payload):
            return None
        return row
    return None


def render_spec(spec: Spec, out: Path, preset: str | None = None, strict: bool = True,
                mode: str = "normal", prompt: str | None = None) -> RenderResult:
    out = assert_safe_output(out)
    if out.suffix.lower() != ".png":
        raise UnsafeOutput(f"refusing {out.name}: plates are PNG")
    digest = prompt_digest(spec, prompt)
    cached = lookup_cached(out.parent, out.name, digest)
    if cached:
        log.info("skip %s; prompt hash matches the plate on disk", out.name)
        theme = get_theme(preset or spec.preset, spec.size)
        png = out.read_bytes()
        return RenderResult(
            png=png,
            svg_path=out.with_suffix(".svg"),
            png_path=out,
            spec=spec,
            theme=theme,
            meta={"idea": cached.get("idea"), "labels": cached.get("labels") or [], "headline": ""},
            qa=QaReport(ok=True, checks=["pass: cache — prompt hash unchanged"]),
            checksum=cached.get("checksum") or hashlib.md5(png).hexdigest(),
            renderer=str(cached.get("renderer") or "cache"),
            alt=str(cached.get("alt") or ""),
            mode=mode,
            job_id=str(cached.get("job_id") or ""),
            prompt_hash=digest,
            sha256=str(cached.get("sha256") or file_sha256(png)),
            created_at=str(cached.get("created_at") or ""),
            cached=True,
        )
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
    cover = ink_coverage(png)
    # Fill percentage is recorded. It is not the quality bar. A milk halo used to
    # pass 30-55% while the plate still looked unfinished. See skills/image-quality-standard.
    scene.add(
        "ink coverage",
        True,
        f"{cover:.0%} of the frame. Recorded only. Craft is scored by skills/image-quality-standard.",
    )
    plate_stem = headline_stem(png, meta.get("marks") or [])
    scene.add(
        "plate stem",
        plate_stem >= 10,
        f"{plate_stem:.1f}px at a 55px cap. Font preflight only, not a craft score.",
    )
    md5 = hashlib.md5(png).hexdigest()
    sha = file_sha256(png)
    result = RenderResult(
        png=png,
        svg_path=out.with_suffix(".svg"),
        png_path=out,
        spec=spec,
        theme=theme,
        meta=meta,
        qa=scene,
        checksum=md5,
        renderer=renderer,
        alt=alt_text(spec, meta),
        mode=mode,
        failures=list(scene.failures),
        job_id=str(uuid.uuid4()),
        prompt_hash=digest,
        sha256=sha,
        created_at=_now(),
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
        drop_manifest_entry(out.parent, out.name, rejected={
            "file": out.name,
            "prompt_hash": digest,
            "qa_status": "fail",
            "reviewer": "engine-preflight",
            "sha256": sha,
            "updated_at": _now(),
            "reason": "QA failed; the previous good plate was removed",
            "kept": f".failed/{out.name}",
        })
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
    result = render_spec(spec, Path(out), preset=spec.preset, strict=strict, mode=mode, prompt=prompt)
    result.notes = notes
    return result
