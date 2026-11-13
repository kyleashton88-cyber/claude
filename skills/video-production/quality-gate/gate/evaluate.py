"""Run every check and build the report payload."""

from __future__ import annotations

import tempfile
from pathlib import Path

from .captions import caption_problems, parse_captions
from .media import (
    black_runs,
    extract_png,
    gray_frames,
    judge_loudness,
    longest_static,
    measure_loudness,
    media_info,
    sample_times,
    silent_gaps,
    technical_problems,
)
from .profiles import LOUDNESS_TARGET, LOUDNESS_TOLERANCE, TRUE_PEAK_MAX, Profile, length_ok
from .textscan import find_brands, has_disclaimer, margin_hits, read_frame, tesseract_path

SUPERSEDES = (
    "course/skills/motion_picture/qa.py (15-minute minimum, loudness printed and not failed)",
    "course/blueprint-rework/render_motion.py (exit when a lesson is under 15 minutes)",
)


def _check(name: str, problems: list[str], *, ok_detail: str) -> dict:
    if problems:
        return {"id": name, "result": "fail", "detail": " ".join(problems)}
    return {"id": name, "result": "pass", "detail": ok_detail}


def evaluate(
    master: Path,
    profile: Profile,
    *,
    captions: Path | None = None,
    transcript: Path | None = None,
) -> dict:
    master = Path(master)
    checks: list[dict] = []
    if not master.is_file():
        checks.append({"id": "master", "result": "fail", "detail": f"master not found: {master}"})
        return _payload(master, profile, checks)

    info = media_info(master)
    duration = float(info["duration"])
    if length_ok(duration, profile):
        length_detail = (
            f"{duration:.1f}s is inside {profile.label} "
            f"({profile.min_seconds:.0f}s–{profile.max_seconds:.0f}s)"
        )
        length_problems: list[str] = []
    else:
        length_detail = ""
        length_problems = [
            f"{duration:.1f}s is outside {profile.label} "
            f"({profile.min_seconds:.0f}s–{profile.max_seconds:.0f}s). "
            "Length follows the format profile. There is no 15-minute floor."
        ]
    checks.append(_check("length", length_problems, ok_detail=length_detail))

    integrated, true_peak, loud_error = measure_loudness(master)
    if loud_error:
        loud_problems = [loud_error]
        peak_problems = ["true peak was not measured because the loudness meter failed"]
    else:
        loud_problems, peak_problems = judge_loudness(integrated, true_peak)
    loud_ok = (
        f"integrated {integrated:.1f} LUFS, target {LOUDNESS_TARGET:.0f} ± {LOUDNESS_TOLERANCE:.0f}"
        if integrated is not None and not loud_problems
        else ""
    )
    peak_ok = (
        f"true peak {true_peak:.1f} dBTP, limit {TRUE_PEAK_MAX:.0f} dBTP"
        if true_peak is not None and not peak_problems
        else ""
    )
    checks.append(_check("loudness", loud_problems, ok_detail=loud_ok))
    checks.append(_check("true_peak", peak_problems, ok_detail=peak_ok))

    frames = gray_frames(master, fps=2)
    hold, hold_at = longest_static(frames, fps=2)
    if hold > profile.max_hold_seconds + 1e-6:
        freeze = [f"static frames run {hold:.1f}s from {hold_at:.1f}s, limit {profile.max_hold_seconds:.0f}s"]
        freeze_ok = ""
    else:
        freeze = []
        freeze_ok = f"longest static run {hold:.1f}s, limit {profile.max_hold_seconds:.0f}s"
    checks.append(_check("frozen", freeze, ok_detail=freeze_ok))

    dark = [run for run in black_runs(frames, fps=2) if run[1] > profile.max_black_seconds]
    if dark:
        bits = [f"{length:.1f}s from {start:.1f}s" for start, length in dark]
        black_problems = [f"near-black gap {', '.join(bits)}, limit {profile.max_black_seconds:.1f}s"]
        black_ok = ""
    else:
        black_problems = []
        black_ok = f"no near-black run over {profile.max_black_seconds:.1f}s"
    checks.append(_check("black", black_problems, ok_detail=black_ok))

    gaps = silent_gaps(master, profile.max_silence_seconds) if info.get("audio") else ["no audio stream"]
    if gaps:
        silence_problems = [
            f"silence at least {profile.max_silence_seconds:.0f}s: " + " | ".join(gaps[:4])
        ]
        silence_ok = ""
    else:
        silence_problems = []
        silence_ok = f"no silence of {profile.max_silence_seconds:.0f}s or more"
    checks.append(_check("silence", silence_problems, ok_detail=silence_ok))

    tech = technical_problems(info, profile)
    video = info.get("video") or {}
    checks.append(
        _check(
            "resolution",
            tech["resolution"],
            ok_detail=f"{video.get('width')}x{video.get('height')}",
        )
    )
    checks.append(
        _check(
            "fps",
            tech["fps"],
            ok_detail=f"{video.get('fps', 0):.3f} fps",
        )
    )
    audio_codec = (info.get("audio") or {}).get("codec")
    checks.append(
        _check(
            "codec",
            tech["codec"],
            ok_detail=f"video {video.get('codec')}, audio {audio_codec}, {video.get('pix_fmt')}",
        )
    )

    caption_text = ""
    if captions is None or not Path(captions).is_file():
        checks.append(
            {
                "id": "captions",
                "result": "fail",
                "detail": "no caption file. Reading speed and line length were not skipped.",
            }
        )
    else:
        raw = Path(captions).read_text(encoding="utf-8")
        try:
            cues = parse_captions(raw)
        except ValueError as exc:
            cues = []
            problems = [str(exc)]
        else:
            problems = caption_problems(cues, profile)
        caption_text = raw
        checks.append(
            _check(
                "captions",
                problems,
                ok_detail=(
                    f"{len(cues)} cues, at most {profile.max_caption_line} characters "
                    f"and {profile.max_caption_cps:.0f} per second"
                ),
            )
        )

    transcript_text = ""
    if transcript is not None and Path(transcript).is_file():
        transcript_text = Path(transcript).read_text(encoding="utf-8")

    ocr_text = ""
    margin_problems: list[str] = []
    ocr_error = None
    if tesseract_path() is None:
        ocr_error = (
            "tesseract is not installed. Brand, exchange-name, and safe-margin checks "
            "cannot run. They are not skipped."
        )
    else:
        with tempfile.TemporaryDirectory(prefix="quality-gate-") as tmp:
            folder = Path(tmp)
            for second in sample_times(duration):
                png = folder / f"f{int(second * 1000):07d}.png"
                extract_png(master, second, png)
                try:
                    text, boxes = read_frame(str(png))
                except RuntimeError as exc:
                    ocr_error = str(exc)
                    break
                ocr_text += "\n" + text
                width = video.get("width") or 0
                height = video.get("height") or 0
                hits = margin_hits(boxes, width, height, profile) if width and height else []
                if hits:
                    margin_problems.append(f"at {second:.1f}s: " + ", ".join(hits[:6]))

    if ocr_error:
        checks.append({"id": "text_recognition", "result": "fail", "detail": ocr_error})
        checks.append({"id": "brands", "result": "fail", "detail": ocr_error})
        checks.append({"id": "safe_margins", "result": "fail", "detail": ocr_error})
    else:
        checks.append(
            {
                "id": "text_recognition",
                "result": "pass",
                "detail": "tesseract read the sampled frames",
            }
        )
        blob = "\n".join([caption_text, transcript_text, ocr_text])
        brands = find_brands(blob)
        if brands:
            checks.append(
                {
                    "id": "brands",
                    "result": "fail",
                    "detail": "brand or exchange name: " + ", ".join(brands),
                }
            )
        else:
            checks.append({"id": "brands", "result": "pass", "detail": "no exchange or banned brand name"})
        checks.append(
            _check(
                "safe_margins",
                margin_problems,
                ok_detail=f"sampled words sit inside the {profile.margin_frac:.0%} margin",
            )
        )

    disclaimer_blob = "\n".join([caption_text, transcript_text, ocr_text])
    if has_disclaimer(disclaimer_blob):
        checks.append(
            {
                "id": "disclaimer",
                "result": "pass",
                "detail": "found an education line that says not financial advice",
            }
        )
    else:
        checks.append(
            {
                "id": "disclaimer",
                "result": "fail",
                "detail": "disclaimer not found in captions, transcript, or on-screen text. Expected education plus 'not financial advice'.",
            }
        )
    return _payload(master, profile, checks)


def _payload(master: Path, profile: Profile, checks: list[dict]) -> dict:
    failed = [item["id"] for item in checks if item["result"] != "pass"]
    return {
        "tool": "quality-gate",
        "result": "fail" if failed else "pass",
        "master": str(master),
        "format": profile.name,
        "format_label": profile.label,
        "length_window_seconds": [profile.min_seconds, profile.max_seconds],
        "loudness_target_lufs": LOUDNESS_TARGET,
        "loudness_tolerance_lu": LOUDNESS_TOLERANCE,
        "true_peak_max_dbtp": TRUE_PEAK_MAX,
        "failed": failed,
        "checks": checks,
        "supersedes": list(SUPERSEDES),
        "publishes": False,
    }
