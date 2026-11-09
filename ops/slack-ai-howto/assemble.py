#!/usr/bin/env python3
"""Assemble the staff Slack AI how-to from stills + Clara's voiceover.

Inserts a short hold after each teaching beat so the click is readable, and
holds the recap card after the last line. Target length is about 3 minutes.
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
VO = ROOT / "audio" / "clara-vo.mp3"
SHOTS = ROOT / "shots"
OUT = ROOT / "out" / "how-to-use-ai-with-slack.mp4"
BUILD = ROOT / "build"
GAP = 3.2
TAIL = 11.0

# Spoken paragraphs, in order, mapped onto stills.
BEATS = [
    ("S01_title.png", "In the next three minutes, you'll ask our AI in Slack the right way — click by click."),
    ("S02_sidebar.png", "Open Slack on your computer. Look at the left sidebar. Under Channels, you'll see the rooms we use every day."),
    ("S03_channel.png", "For company-wide asks that several desks might see, open all-audience-asset-co. For a quick internal note, use staff-chat instead. Pick the channel that matches who needs to see the work."),
    ("S04_mention.png", "Click into the message box at the bottom. Type the at symbol. Choose the bot from the list — for routing work across desks, that is usually Orchestrator Bot. You can also mention ChatGPT or Creative Studio when the job is clearly theirs."),
    ("S05_draft.png", "Write one clear ask. Say what you need, who it is for, and the deadline. Attach a file or paste a link if it helps. Keep wording education-safe. Do not put client profit claims or unverified money numbers in the ask."),
    ("S06_sent.png", "When the draft looks right, press Send. Your ask appears in the channel so Stewart and the team can see it."),
    ("S07_thread.png", "Now click Reply in thread on that same message. Put every follow-up, file, and clarification inside the thread. Do not start a new top-level message for the same job — that splits context and slows everyone down."),
    ("S08_reply.png", "When the bot answers, read the reply in the thread. If something is missing or wrong, reply in that same thread with the correction. Stay in one thread until the job is done or handed off."),
    ("S08b_followup.png", "Here is a simple pattern you can copy. For who it is for, name Stewart or the desk. For by when, give a day and time. For what, state the outcome in one sentence. That format keeps Orchestrator and Creative Studio aligned. If the bot asks a clarifying question, answer in the thread. If the work needs Stewart's yes before publish or spend, say that clearly in the ask so nobody ships early."),
    ("S09_recap.png", "Quick recap. Open the right channel. At-mention the bot. Write one clear ask with a deadline. Keep follow-ups in the thread. Read the reply there. That is how we use AI with Slack at Market Pros."),
]


def words(text: str) -> int:
    return len(re.findall(r"[A-Za-z0-9']+", text))


def probe_duration(path: Path) -> float:
    out = subprocess.check_output(
        [
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "csv=p=0", str(path),
        ],
        text=True,
    ).strip()
    return float(out)


def silence_ends(path: Path) -> list[float]:
    log = subprocess.run(
        [
            "ffmpeg", "-i", str(path),
            "-af", "silencedetect=noise=-32dB:d=0.28",
            "-f", "null", "-",
        ],
        capture_output=True, text=True,
    ).stderr
    return [float(match) for match in re.findall(r"silence_end:\s*([0-9.]+)", log)]


def snap(target: float, ends: list[float], limit: float) -> float:
    window = [end for end in ends if target - 0.35 <= end <= target + 1.7 and end < limit - 0.2]
    if not window:
        return min(target, limit - 0.2)
    return min(window, key=lambda end: abs(end - target))


def timeline(duration: float, ends: list[float]) -> list[tuple[str, float, float, float]]:
    counts = [words(text) for _, text in BEATS]
    total = sum(counts)
    cursor = 0.0
    cuts = []
    consumed = 0
    for count in counts[:-1]:
        consumed += count
        raw = duration * consumed / total
        cut = snap(raw, ends, duration)
        cut = max(cut, cursor + 0.4)
        cuts.append(cut)
        cursor = cut
    edges = [0.0, *cuts, duration]
    rows = []
    for index, ((image, _text), start, end) in enumerate(zip(BEATS, edges, edges[1:])):
        hold = TAIL if index == len(BEATS) - 1 else GAP
        rows.append((image, start, end, hold))
    return rows


def build_audio(rows: list[tuple[str, float, float, float]], wav: Path) -> None:
    filters = []
    labels = []
    for index, (_image, start, end, hold) in enumerate(rows):
        filters.append(
            f"[0:a]atrim=start={start:.3f}:end={end:.3f},asetpts=PTS-STARTPTS[a{index}]"
        )
        filters.append(
            f"anullsrc=r=44100:cl=mono,atrim=0:{hold:.3f},asetpts=PTS-STARTPTS[s{index}]"
        )
        labels.append(f"[a{index}][s{index}]")
    filters.append(
        "".join(labels) + f"concat=n={len(rows) * 2}:v=0:a=1,loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000[outa]"
    )
    subprocess.check_call(
        [
            "ffmpeg", "-y", "-i", str(VO),
            "-filter_complex", ";".join(filters),
            "-map", "[outa]", "-c:a", "pcm_s16le", str(wav),
        ]
    )


def build_video(rows, wav: Path, mp4: Path) -> None:
    concat = BUILD / "slides.txt"
    lines = []
    for image, _start, end, hold in rows:
        span = (end - _start) + hold
        lines.append(f"file '{SHOTS / image}'")
        lines.append(f"duration {span:.3f}")
    lines.append(f"file '{SHOTS / rows[-1][0]}'")
    concat.write_text("\n".join(lines) + "\n")
    subprocess.check_call(
        [
            "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat),
            "-i", str(wav),
            "-vf", "scale=1920:1080,format=yuv420p",
            "-c:v", "libx264", "-tune", "stillimage", "-crf", "18", "-r", "30",
            "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart",
            str(mp4),
        ]
    )


def write_vtt(rows, path: Path) -> None:
    clock = 0.0
    cues = ["WEBVTT", ""]
    for index, ((_image, text), (_img, _start, end, hold)) in enumerate(zip(BEATS, rows), start=1):
        span = (end - _start) + (0 if index < len(rows) else 0)
        # Caption covers the spoken part only.
        spoken = end - _start
        start_at = clock
        end_at = clock + spoken
        cues.append(str(index))
        cues.append(f"{stamp(start_at)} --> {stamp(end_at)}")
        cues.append(text)
        cues.append("")
        clock += spoken + hold
    path.write_text("\n".join(cues))


def stamp(seconds: float) -> str:
    ms = int(round(seconds * 1000))
    hours, ms = divmod(ms, 3600000)
    minutes, ms = divmod(ms, 60000)
    secs, ms = divmod(ms, 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}.{ms:03d}"


def main() -> None:
    BUILD.mkdir(exist_ok=True)
    OUT.parent.mkdir(exist_ok=True)
    for image, _text in BEATS:
        if not (SHOTS / image).exists():
            raise SystemExit(f"missing still {image}")
    duration = probe_duration(VO)
    rows = timeline(duration, silence_ends(VO))
    wav = BUILD / "vo-with-holds.wav"
    build_audio(rows, wav)
    build_video(rows, wav, OUT)
    write_vtt(rows, OUT.with_suffix(".vtt"))
    wav.unlink(missing_ok=True)
    final = probe_duration(OUT)
    report = ROOT / "QA.md"
    report.write_text(
        "\n".join(
            [
                "# QA — How to use AI with the Slack channel",
                "",
                f"- File: `ops/slack-ai-howto/out/how-to-use-ai-with-slack.mp4`",
                f"- Measured length: {final:.2f}s ({final / 60:.2f} min)",
                f"- Voiceover source length: {duration:.2f}s",
                "- Frame size: 1920×1080",
                "- Voice: Clara, reused from `audio/clara-vo.mp3` (not regenerated)",
                "- Holds: 3.2s after each beat, 11s on the recap card after the last line",
                "- Loudness target: -16 LUFS integrated",
                "- No Slack message was posted",
                "",
                "## Stills",
                "",
                "S01 and S09 are the staged title and recap cards.",
                "S02–S08 and the follow-up still are rendered from the live thread text in #all-audience-asset-co (Jess’s task ask `1794230823.008249` and the Lea thread `1794230545.108409`).",
                "The workspace sign-in wall blocked a browser capture of audienceassetco.slack.com. See `capture-notes/signin-wall.png`. Email addresses from those threads are not shown.",
                "",
            ]
        )
    )
    print(f"duration {final:.2f}s -> {OUT}")


if __name__ == "__main__":
    main()
