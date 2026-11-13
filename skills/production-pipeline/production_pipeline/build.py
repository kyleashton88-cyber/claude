"""Stage runners. Each one reads and writes the shared context dict."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np
import soundfile as sf
import yaml

from lib.ffmpeg_util import ebur128, ffmpeg_bin, run
from lib.fonts import font_file
from lib.mix import TRUE_PEAK_DBTP, VOICE_LUFS, duck_under_voice
from motion.render import render_sequence
from music.compose import render_bed
from voice.captions import caption_box, margin_ok, write_chapters, write_srt, write_vtt, write_words
from voice.speak import Speaker

STAGES = (
    "narrate",
    "align",
    "illustrate",
    "motion",
    "grade",
    "music",
    "captions",
    "endcard",
    "loudness",
)

LEAD = 0.35
TAIL = 0.45
END_CARD_SECONDS = 3.2


def _load(path: Path) -> dict:
    data = yaml.safe_load(path.read_text())
    if "sections" not in data:
        raise ValueError(f"{path} has no sections")
    return data


def narrate(ctx: dict) -> None:
    lesson = ctx["lesson"]
    speaker = Speaker(engine=lesson.get("engine", "piper"), mood=lesson.get("mood", "calm-teacher"))
    ctx["speaker"] = speaker
    pieces = []
    words = []
    shots = []
    chapters = []
    clock = 0.0
    sample_rate = None
    for section in lesson["sections"]:
        audio, rate, section_words, method = speaker.render(section["narration"])
        if sample_rate is None:
            sample_rate = rate
        spoken = len(audio) / rate
        seconds = round(LEAD + spoken + TAIL, 3)
        visual = dict(section.get("visual") or {"kind": "title"})
        visual["seconds"] = seconds
        visual.setdefault("title", section.get("chapter") or section["id"])
        visual.setdefault("caption", section.get("chapter") or "")
        shots.append(visual)
        chapters.append((clock, section.get("chapter") or section["id"]))
        pieces.append(np.zeros(int(LEAD * rate), dtype=np.float32))
        pieces.append(audio)
        pieces.append(np.zeros(int(round((seconds - LEAD - spoken) * rate)), dtype=np.float32))
        for word in section_words:
            words.append(type(word)(word.text, word.start + clock + LEAD, word.end + clock + LEAD))
        clock += seconds
        ctx["align_method"] = method
    ctx["sample_rate"] = sample_rate
    ctx["duration"] = clock
    ctx["words"] = words
    ctx["chapters"] = chapters
    ctx["shots"] = shots
    voice = ctx["work"] / "voice.wav"
    sf.write(str(voice), np.concatenate(pieces), sample_rate)
    ctx["voice"] = voice


def align(ctx: dict) -> None:
    # Narration already aligned each section. This stage publishes words.json.
    write_words(
        ctx["out"] / "words.json",
        ctx["words"],
        engine=ctx["speaker"].engine_name,
        mood=ctx["speaker"].mood_name,
        method=ctx.get("align_method", "acoustic-forced-align"),
    )


def illustrate(ctx: dict) -> None:
    prompts = []
    for section in ctx["lesson"]["sections"]:
        if section.get("illustration"):
            prompts.append({"id": section["id"], "prompt": section["illustration"]})
    note = ctx["out"] / "illustration.txt"
    if not prompts:
        note.write_text("No illustration prompts on this lesson.\n")
        ctx["illustration"] = "none"
        return
    spec = ctx["work"] / "illustrations.yaml"
    spec.write_text(yaml.safe_dump({"slots": prompts}))
    try:
        import illustration_engine  # noqa: F401
    except ImportError:
        note.write_text(
            "Illustration engine is not installed. Skipped.\n"
            "When PR #18 is on the machine: python3 -m illustration_engine batch "
            f"{spec} --preset house --out {ctx['out'] / 'plates'}\n"
        )
        ctx["illustration"] = "skipped"
        return
    dest = ctx["out"] / "plates"
    dest.mkdir(parents=True, exist_ok=True)
    subprocess.check_call(
        [sys.executable, "-m", "illustration_engine", "batch", str(spec), "--preset", "house", "--out", str(dest)]
    )
    note.write_text(f"Rendered plates in {dest}\n")
    ctx["illustration"] = "rendered"


def motion(ctx: dict) -> None:
    sequence = {"fps": 30, "width": 1920, "height": 1080, "shots": list(ctx["shots"])}
    # End card is its own shot so the picture closes on the disclaimer.
    sequence["shots"].append({
        "kind": "title",
        "seconds": END_CARD_SECONDS,
        "lines": [ctx["lesson"].get("end_card", {}).get("kicker", "Education only")],
        "sub": ctx["lesson"].get("end_card", {}).get("line", "Not financial advice. Figures are illustrative."),
        "caption": "Educational content only",
    })
    ctx["picture_seconds"] = ctx["duration"] + END_CARD_SECONDS
    picture = ctx["work"] / "picture.mp4"
    render_sequence(sequence, picture, crf=18, preset="veryfast")
    ctx["picture"] = picture


def grade(ctx: dict) -> None:
    from grade.lut import write_looks
    from grade.pipeline import apply_grade

    luts = Path(__file__).resolve().parents[2] / "video-production" / "color-grade" / "luts"
    if not (luts / "clean-educational.cube").is_file():
        write_looks(luts)
    graded = ctx["work"] / "graded.mp4"
    import numpy as np
    apply_grade(ctx["picture"], graded, luts / "clean-educational.cube", np.array([1.0, 1.0, 1.0]), 0.0)
    ctx["graded"] = graded


def music(ctx: dict) -> None:
    seconds = ctx["picture_seconds"] + 0.2
    audio, rate = render_bed(mood="calm", key="C", scale="major", bpm=72, seconds=seconds)
    bed = ctx["work"] / "bed.wav"
    sf.write(str(bed), audio, rate)
    # Pad the voice with silence through the end card so the bed can return.
    voice, sr = sf.read(str(ctx["voice"]), always_2d=False)
    need = int(ctx["picture_seconds"] * sr)
    if len(voice) < need:
        voice = np.pad(voice, (0, need - len(voice)))
    voiced = ctx["work"] / "voice-full.wav"
    sf.write(str(voiced), voice, sr)
    mix = ctx["work"] / "mix.wav"
    duck_under_voice(bed, voiced, mix)
    ctx["mix"] = mix


def captions(ctx: dict) -> None:
    write_vtt(ctx["out"] / "captions.vtt", ctx["words"])
    write_srt(ctx["out"] / "captions.srt", ctx["words"])
    write_chapters(ctx["out"] / "chapters.txt", ctx["chapters"])
    box = caption_box()
    ctx["caption_box"] = box
    ctx["caption_margin_ok"] = margin_ok(box)


def endcard(ctx: dict) -> None:
    # The end card is already the last motion shot. Record the line that was drawn.
    card = ctx["lesson"].get("end_card") or {}
    (ctx["out"] / "end-card.txt").write_text(
        (card.get("kicker") or "Education only") + "\n" + (card.get("line") or "") + "\n"
    )


def loudness(ctx: dict) -> None:
    final = ctx["out"] / "master.mp4"
    run([
        ffmpeg_bin(), "-y", "-hide_banner",
        "-i", str(ctx["graded"]), "-i", str(ctx["mix"]),
        "-map", "0:v:0", "-map", "1:a:0",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "320k", "-ar", "48000", "-ac", "2",
        "-shortest", "-movflags", "+faststart",
        str(final),
    ])
    meter = ebur128(final)
    report = {
        "master": str(final),
        "integrated_lufs": meter["integrated_lufs"],
        "true_peak_dbtp": meter["true_peak_dbfs"],
        "target_lufs": VOICE_LUFS,
        "target_true_peak": TRUE_PEAK_DBTP,
        "loudness_pass": abs(meter["integrated_lufs"] - VOICE_LUFS) <= 1.5 and (meter["true_peak_dbfs"] or -99) <= TRUE_PEAK_DBTP + 0.3,
        "caption_margin_pass": ctx["caption_margin_ok"],
        "illustration": ctx.get("illustration"),
        "align_method": ctx.get("align_method"),
        "font": str(font_file("Inter", "Bold")),
    }
    (ctx["out"] / "qa-report.json").write_text(json.dumps(report, indent=2) + "\n")
    ctx["report"] = report


RUNNERS = {
    "narrate": narrate,
    "align": align,
    "illustrate": illustrate,
    "motion": motion,
    "grade": grade,
    "music": music,
    "captions": captions,
    "endcard": endcard,
    "loudness": loudness,
}


def build(lesson_path: Path, out: Path, hooks: dict | None = None) -> dict:
    """Run every stage. `hooks[stage](ctx)` replaces that stage when present."""
    out.mkdir(parents=True, exist_ok=True)
    work = out / "_work"
    if work.exists():
        shutil.rmtree(work)
    work.mkdir()
    ctx = {"lesson": _load(lesson_path), "out": out, "work": work}
    for stage in STAGES:
        if hooks and stage in hooks:
            hooks[stage](ctx)
        else:
            RUNNERS[stage](ctx)
    return ctx["report"]
