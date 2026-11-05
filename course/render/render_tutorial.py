"""Render a tutorial from ChatGPT stills plus overlays.

The pictures must already exist at each beat's image path. This file never
draws a diagram. It may add captions, a lower third, the disclaimer line,
a slow zoom, and the music bed.

  python3 course/render/render_tutorial.py --check
  python3 course/render/render_tutorial.py --id bp-01-introduction
  python3 course/render/render_tutorial.py --proof
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "course" / "scripts"
OUT = ROOT / "course" / "masters"
FONT = "/usr/share/fonts/truetype/macos/Inter-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/macos/Inter-Regular.ttf"
WPM = 143
DISCLAIMER = "Education only · Not financial advice · Examples do not indicate future results"


def scripts() -> list[Path]:
    return sorted(SCRIPTS.glob("*.json"))


def load(path: Path) -> dict:
    return json.loads(path.read_text())


def missing_images(script: dict) -> list[str]:
    bad = []
    for beat in script["beats"]:
        p = ROOT / beat["image"]
        if not p.is_file() or p.stat().st_size < 1000:
            bad.append(beat["image"])
    return bad


def check() -> int:
    total = 0
    blocked = 0
    voice_blocked = 0
    jobs = ROOT / "course" / "render" / "jobs"
    for path in scripts():
        script = load(path)
        bad = missing_images(script)
        voice = ROOT / "course" / "audio" / f"{script['id']}.wav"
        total += len(script["beats"])
        job = jobs / f"{script['id']}.json"
        waiting = job.is_file()
        if bad or (waiting and not voice.is_file()):
            blocked += 1
            if waiting and not voice.is_file():
                voice_blocked += 1
            print(
                f"BLOCKED {script['id']}: {len(bad)} of {len(script['beats'])} images missing, "
                f"voice {'missing' if not voice.is_file() else 'ready'}, est {script['estimated_minutes']} min"
            )
        else:
            print(f"READY   {script['id']}: {len(script['beats'])} images")
    print(f"beats {total} lessons_blocked {blocked} voice_blocked {voice_blocked}")
    return 2 if blocked else 0


def run(cmd: list[str]) -> None:
    subprocess.check_call(cmd)


def beat_seconds(beat: dict) -> float:
    words = len((beat.get("vo") or "").split())
    floor = {"intro": 5.5, "outro": 8.0, "legal": 12.0}.get(beat["role"], 6.0)
    return max(floor, words / WPM * 60)


def accent_for(script: dict) -> str:
    """Chapter colour. Elite stays teal. Blueprint and On-Chain Operator stay cyan."""
    course = (script.get("course") or "").lower()
    palette = (script.get("palette") or "").lower()
    if "elite" in course or palette == "teal":
        return "0x2EE6A6"
    return "0x00D4FF"


def render_script(script: dict) -> Path:
    bad = missing_images(script)
    if bad:
        raise SystemExit(f"{script['id']} missing {len(bad)} images. Refusing to reuse or to draw replacements.")
    accent = accent_for(script)
    work = ROOT / "course" / "render" / "work" / script["id"]
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)
    clips = []
    for beat in script["beats"]:
        secs = beat_seconds(beat)
        frames = int(round(secs * 30))
        clip = work / f"{beat['n']:03d}.mp4"
        cap = work / f"{beat['n']:03d}.txt"
        cap.write_text(beat["cap"])
        chapter = work / f"{beat['n']:03d}-ch.txt"
        chapter.write_text(f"{beat['chapter']}")
        foot = work / f"{beat['n']:03d}-foot.txt"
        foot.write_text(DISCLAIMER)
        vf = ",".join([
            "scale=1920:1080:force_original_aspect_ratio=increase",
            "crop=1920:1080",
            f"zoompan=z='min(1.0+0.04*on/{frames},1.05)':d={frames}:s=1920x1080:fps=30",
            f"drawtext=fontfile={FONT}:textfile={cap}:fontsize=36:fontcolor=white:box=1:boxcolor=0x050A12CC:boxborderw=16:x=(w-text_w)/2:y=h-160:line_spacing=8",
            f"drawtext=fontfile={FONT}:textfile={chapter}:fontsize=28:fontcolor={accent}:x=80:y=64",
            f"drawtext=fontfile={FONT_REG}:textfile={foot}:fontsize=22:fontcolor=0xD0D7E2:x=w-text_w-48:y=h-48",
        ])
        run([
            "ffmpeg", "-y", "-v", "error", "-loop", "1", "-i", str(ROOT / beat["image"]),
            "-vf", vf, "-frames:v", str(frames), "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30", str(clip),
        ])
        clips.append(clip)
    lst = work / "list.txt"
    lst.write_text("".join(f"file '{c}'\n" for c in clips))
    silent = work / "silent.mp4"
    run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(silent)])
    music = ROOT / script["music"]
    OUT.mkdir(parents=True, exist_ok=True)
    dest = OUT / f"{script['id']}.mp4"
    # Voice is not synthesized here. The bed plays under a silent picture track
    # only when --allow-silent is passed. The default render expects a voice wav
    # at course/audio/<id>.wav, ducked under the pictures.
    voice = ROOT / "course" / "audio" / f"{script['id']}.wav"
    if not voice.is_file():
        raise SystemExit(
            f"{script['id']} pictures are ready but course/audio/{script['id']}.wav is missing. "
            "Refusing a silent master."
        )
    run([
        "ffmpeg", "-y", "-v", "error", "-i", str(silent), "-i", str(voice), "-i", str(music),
        "-filter_complex",
        "[1:a]aresample=48000,apad,asplit=2[vo][key];"
        "[2:a]aresample=48000,volume=0.22,aloop=loop=-1:size=2e9[mus];"
        "[mus][key]sidechaincompress=threshold=0.03:ratio=8:attack=40:release=400[duck];"
        "[vo][duck]amix=inputs=2:normalize=0,loudnorm=I=-16:TP=-1.5:LRA=11[a]",
        "-map", "0:v", "-map", "[a]", "-shortest", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", str(dest),
    ])
    return dest


def proof() -> Path:
    """Six-second overlay proof on one existing ChatGPT still. Not a lesson master."""
    src = Path("/cursor/stores/bot/video-images/bp-01-introduction-hook.png")
    if not src.is_file():
        raise SystemExit(f"proof source missing: {src}")
    dest_dir = Path("/opt/cursor/artifacts")
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / "overlay-proof.mp4"
    music = ROOT / "course" / "music" / "komiku-ambiant-obscur-technology.ogg"
    cap = dest_dir / "overlay-proof-cap.txt"
    cap.write_text("Price often chops sideways.")
    chapter = dest_dir / "overlay-proof-ch.txt"
    chapter.write_text("HOOK")
    foot = dest_dir / "overlay-proof-foot.txt"
    foot.write_text(DISCLAIMER)
    vf = ",".join([
        "scale=1920:1080:force_original_aspect_ratio=increase",
        "crop=1920:1080",
        "zoompan=z='min(1.0+0.001*on,1.04)':d=180:s=1920x1080:fps=30",
        f"drawtext=fontfile={FONT}:textfile={cap}:fontsize=42:fontcolor=white:box=1:boxcolor=0x050A12CC:boxborderw=18:x=(w-text_w)/2:y=h-180",
        f"drawtext=fontfile={FONT}:textfile={chapter}:fontsize=28:fontcolor=0x00D4FF:x=80:y=64",
        f"drawtext=fontfile={FONT_REG}:textfile={foot}:fontsize=22:fontcolor=0xD0D7E2:x=w-text_w-48:y=h-48",
    ])
    run([
        "ffmpeg", "-y", "-v", "error", "-loop", "1", "-i", str(src), "-stream_loop", "-1", "-i", str(music),
        "-vf", vf, "-t", "6", "-map", "0:v", "-map", "1:a",
        "-af", "volume=0.35,afade=t=in:d=0.4,afade=t=out:st=5:d=1",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30", "-c:a", "aac", "-shortest", str(dest),
    ])
    return dest


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--id")
    ap.add_argument("--proof", action="store_true")
    args = ap.parse_args()
    if args.proof:
        print(proof())
        return
    # --check reports the whole course. --id renders that lesson alone, even
    # while other lessons are still missing stills. The lesson itself still
    # refuses to draw or to reuse a picture.
    if args.check or not args.id:
        code = check()
        if not args.id:
            raise SystemExit(code)
    if not args.id:
        return
    script = load(SCRIPTS / f"{args.id}.json")
    print(render_script(script))


if __name__ == "__main__":
    main()
