"""Watch stills and voice tracks, then render lessons whose assets are complete.

Does not generate pictures, does not draw diagrams, and does not upload to Whop.
ChatGPT stills land at the paths in IMAGE_REQUESTS.json. Voice lands at
course/audio/<id>.wav (see VOICE_REQUESTS.json when a wav is not in the tree).

  python3 course/tools/watch_assets.py
  python3 course/tools/watch_assets.py --render --batch 3
"""

from __future__ import annotations

import argparse
import contextlib
import io
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "course" / "render"))

from render_tutorial import accent_for, beat_seconds, check, missing_images  # noqa: E402

SCRIPTS = ROOT / "course" / "scripts"
AUDIO = ROOT / "course" / "audio"
MASTERS = ROOT / "course" / "masters"
QA_DIR = ROOT / "course" / "qa"
REQUESTS = ROOT / "IMAGE_REQUESTS.json"
STATUS_PATH = ROOT / "ASSET_STATUS.md"
VOICE_PATH = ROOT / "VOICE_REQUESTS.json"

# Elite stays teal and is not in IMAGE_REQUESTS.json. The image queue resumes
# at lesson 5. These ids have no long-form script in course/scripts yet.
ELITE = [
    ("el-05-portfolio-risk", "Portfolio risk controls"),
    ("el-06-circuit-breakers", "Circuit breakers done manually"),
    ("el-07-advanced-liquidation", "Advanced: liquidation scenarios"),
    ("el-08-size-on-a-schedule", "Size changes on a schedule"),
    ("el-09-multi-venue", "Multi-venue counterparty risk"),
    ("el-10-how-to-ask", "How to ask a general question"),
    ("el-11-paper-plan", "Paper plan instead of a 30-day deploy"),
    ("el-01-welcome", "Welcome and what Elite covers"),
    ("el-02-prerequisites", "Prerequisites check"),
    ("el-03-multi-layer", "Multi-layer grids as inventory buckets"),
    ("el-04-dynamic-spacing", "Dynamic spacing when volatility rises"),
]

ROLES = ("hook", "legal", "intro", "demo", "recap", "action", "outro")
INTRO_ROLES = ("hook", "legal", "intro", "outro")
NEEDS = ROOT / "course" / "audio" / "needs"
SPEECH_BANNED = re.compile(
    r"\b(guaranteed|risk-free|you will earn|will profit|passive income|promised income)\b",
    re.I,
)


def compress(nums: list[int]) -> str:
    if not nums:
        return "—"
    ordered = sorted(set(nums))
    ranges: list[str] = []
    start = prev = ordered[0]
    for n in ordered[1:]:
        if n == prev + 1:
            prev = n
            continue
        ranges.append(str(start) if start == prev else f"{start}-{prev}")
        start = prev = n
    ranges.append(str(start) if start == prev else f"{start}-{prev}")
    return ", ".join(ranges)


def priority(lesson_id: str) -> tuple:
    """el-05..el-11, then the rest of Elite, then Blueprint, then On-Chain Operator."""
    parts = lesson_id.split("-")
    if lesson_id.startswith("el-") and len(parts) > 1 and parts[1].isdigit():
        n = int(parts[1])
        band = 0 if 5 <= n <= 11 else 1
        return (band, n, lesson_id)
    if lesson_id.startswith("bp-"):
        return (2, 0, lesson_id)
    return (3, 0, lesson_id)


def speech_hit(text: str) -> str | None:
    cleaned = re.sub(
        r"\b(not|no|never|isn't|is not|aren't|without)\s+(a\s+)?guaranteed\b",
        "",
        text or "",
        flags=re.I,
    )
    match = SPEECH_BANNED.search(cleaned)
    return match.group(0) if match else None


def prompt_hits(prompt: str) -> list[str]:
    """Flags a Show sentence or a label that asks for a banned picture.

    The teaching line may name a seed phrase or a coin in order to say what not to
    draw. The shared ban sentence at the end of every prompt does not count.
    """
    show = ""
    match = re.search(r"Show (.+?)(?: The picture must|$)", prompt or "")
    if match:
        show = match.group(1)
    labels = ""
    match = re.search(r"Labels, spelled exactly: ([^.]+)", prompt or "")
    if match:
        labels = match.group(1)
    body = f"{show} {labels}"
    hits = []
    checks = (
        (r"grey placeholder", "asks for a grey placeholder"),
        (r"blank page", "asks for a blank page"),
        (r"\bcoins\b", "asks for coins"),
        (r"profit figure|\bP&L\b|show a profit", "asks for a profit figure"),
        (r"login screen|sign-in form|seed phrase|API key", "asks for a login or a secret"),
    )
    for pattern, label in checks:
        if re.search(pattern, body, re.I):
            hits.append(label)
    return hits


def is_intro(script: dict) -> bool:
    """Module doors are short on purpose. Full lessons stay in the 15–20 minute band."""
    return script.get("kind") == "intro" or str(script.get("id", "")).startswith("module-")


def script_qa(script: dict, seen_images: dict[str, str]) -> list[str]:
    problems: list[str] = []
    sid = script["id"]
    minutes = float(script.get("estimated_minutes") or 0)
    timeline = sum(beat_seconds(b) for b in script["beats"])
    if is_intro(script):
        if not (2 <= minutes <= 6):
            problems.append(f"module intro estimated length {minutes} min is outside 2–6")
        if not (90 <= timeline <= 420):
            problems.append(f"module intro picture timeline {timeline:.0f}s is outside 90–420")
        required = INTRO_ROLES
    else:
        if not (15 <= minutes <= 20):
            problems.append(f"estimated length {minutes} min is outside 15–20")
        if not (900 <= timeline <= 1200):
            problems.append(f"picture timeline {timeline:.0f}s is outside 900–1200")
        required = ROLES
    roles = {b["role"] for b in script["beats"]}
    missing_roles = [role for role in required if role not in roles]
    if missing_roles:
        problems.append("missing roles: " + ", ".join(missing_roles))
    if script["beats"][0]["role"] != "hook":
        problems.append("beat 1 is not the hook")
    if script["beats"][-1]["role"] != "outro":
        problems.append("last beat is not the outro")
    intro_at = next((b["n"] for b in script["beats"] if b["role"] == "intro"), None)
    hook_at = script["beats"][0]["n"]
    if intro_at is None or intro_at <= hook_at:
        problems.append("branded intro does not follow the hook")
    images = [b["image"] for b in script["beats"]]
    if len(images) != len(set(images)):
        problems.append("a beat reuses an image path inside the lesson")
    for path in images:
        if path in seen_images and seen_images[path] != sid:
            problems.append(f"{path} is also used by {seen_images[path]}")
        seen_images[path] = sid
    course = script.get("course") or ""
    palette = (script.get("palette") or "").lower()
    if "elite" in course.lower() and palette != "teal":
        problems.append("Elite palette is not teal")
    if course == "Grid Bot Blueprint" and palette != "navy-cyan":
        problems.append("Blueprint palette is not navy-cyan")
    if script.get("code_draws_visuals"):
        problems.append("script says code draws visuals")
    music = ROOT / script["music"]
    if not music.is_file():
        problems.append(f"music missing: {script['music']}")
    if sid == "bp-05-spacing-and-range":
        spoken = " ".join(b["vo"] for b in script["beats"])
        if "nineteen gaps" not in spoken.lower():
            problems.append("house example does not say nineteen gaps")
        if re.search(r"\btwenty gaps\b", spoken, re.I):
            problems.append("house example says twenty gaps")
    for beat in script["beats"]:
        prompt = beat.get("prompt") or ""
        cap = beat.get("cap") or ""
        if len(prompt) <= len(cap) or len(prompt) < 200:
            problems.append(f"beat {beat['n']} prompt is thinner than a caption")
        if "Show " not in prompt:
            problems.append(f"beat {beat['n']} prompt does not name shapes")
        for hit in prompt_hits(prompt):
            problems.append(f"beat {beat['n']} {hit}")
        said = speech_hit(beat.get("vo") or "")
        if said:
            problems.append(f"beat {beat['n']} spoken text contains '{said}'")
        expected = f"course/images/{sid}/{int(beat['n']):03d}.png"
        if beat.get("image") != expected:
            problems.append(f"beat {beat['n']} image path is {beat.get('image')}")
    return problems


def file_ready(path: Path) -> bool:
    return path.is_file() and path.stat().st_size >= 1000


def probe(path: Path) -> dict | None:
    if not path.is_file():
        return None
    raw = subprocess.check_output(
        [
            "ffprobe", "-v", "error",
            "-show_entries", "format=duration:stream=codec_type",
            "-of", "json", str(path),
        ],
        text=True,
    )
    data = json.loads(raw)
    streams = data.get("streams") or []
    return {
        "duration": float(data["format"]["duration"]),
        "has_audio": any(s.get("codec_type") == "audio" for s in streams),
        "has_video": any(s.get("codec_type") == "video" for s in streams),
    }


def render_qa(script: dict, info: dict | None, script_problems: list[str]) -> list[str]:
    if info is None:
        return ["no master at course/masters/"]
    problems = list(script_problems)
    duration = info["duration"]
    lo, hi = (90, 420) if is_intro(script) else (900, 1200)
    if not (lo <= duration <= hi):
        problems.append(f"ffprobe duration {duration:.0f}s is outside {lo}–{hi}")
    if not info["has_audio"]:
        problems.append("no audio stream, so the music bed is missing")
    if not info["has_video"]:
        problems.append("no video stream")
    if accent_for(script) == "0x00D4FF" and "elite" in (script.get("course") or "").lower():
        problems.append("Elite chapter colour was restyled to cyan")
    return problems


def lesson_status(missing: list[str], voice_ok: bool, master: Path, qa_passed: bool) -> str:
    if missing:
        return "waiting on images"
    if not voice_ok:
        return "waiting on voice"
    if master.is_file() and qa_passed:
        return "QA passed"
    if master.is_file():
        return "rendered"
    return "ready to render"


def load_scripts() -> list[dict]:
    out = []
    for path in sorted(SCRIPTS.glob("*.json")):
        out.append(json.loads(path.read_text()))
    return out


def voice_payload(scripts: list[dict]) -> dict:
    lessons = []
    referenced = []
    for script in scripts:
        needs = NEEDS / f"{script['id']}.json"
        if needs.is_file():
            referenced.append({
                "id": script["id"],
                "spec": f"course/audio/needs/{script['id']}.json",
                "wav": f"course/audio/{script['id']}.wav",
            })
            continue
        beats = []
        for beat in script["beats"]:
            beats.append({
                "n": beat["n"],
                "role": beat["role"],
                "chapter": beat["chapter"],
                "seconds": round(beat_seconds(beat), 2),
                "vo": beat["vo"],
            })
        lessons.append({
            "id": script["id"],
            "course": script["course"],
            "title": script["title"],
            "out_path": f"course/audio/{script['id']}.wav",
            "word_count": script["word_count"],
            "target_seconds": round(sum(b["seconds"] for b in beats), 2),
            "beats": beats,
        })
    return {
        "generator": "commit a wav per lesson; this file is the script, not audio",
        "voice_spec": {
            "engine": "Kokoro",
            "voice": "af_heart",
            "role": "Professional YouTube-tutorial narrator, the same voice as the existing On-Chain Operator renders",
            "language": "en-US",
            "delivery": "Calm, clear, adult, second person. One idea per sentence. Not a character and not a hype read.",
            "pace_wpm": 143,
            "format": "wav",
            "encoding": "pcm_s16le",
            "sample_rate_hz": 24000,
            "channels": 1,
            "pause_between_beats_seconds": 0.35,
            "music": "Do not mix music into the wav. course/render/render_tutorial.py ducks the licensed bed under this track.",
            "alignment": "Speak beats in order. Each beat's target length is beats[].seconds. The file should land within a few seconds of target_seconds so the outro is not clipped by -shortest.",
            "do_not_synthesize_before_stills": True,
        },
        "inline_count": len(lessons),
        "needs_count": len(referenced),
        "needs": referenced,
        "lessons": lessons,
    }


def write_note(script: dict, row: dict) -> None:
    QA_DIR.mkdir(parents=True, exist_ok=True)
    lines = [
        f"# QA: {script['id']}",
        "",
        f"- Course: {script['course']}",
        f"- Title: {script['title']}",
        f"- Status: {row['status']}",
        f"- Palette: {script.get('palette')} (chapter accent {accent_for(script)})",
        f"- Estimated speech: {script['estimated_minutes']} min, {script['word_count']} words at 143 wpm",
        f"- Picture timeline: {row['timeline_s']:.0f}s",
        f"- Images: {row['have']}/{row['beats']} at `course/images/{script['id']}/`",
        f"- Present beats: {row['present']}",
        f"- Missing beats: {row['missing']}",
        f"- Voice: {row['voice']}",
        f"- Master: {row['master']}",
        f"- Script checklist: {'pass' if not row['script_problems'] else 'fail'}",
        f"- Render checklist: {row['render_line']}",
        f"- Creative Studio: {row['studio']}",
        "",
        "## Script checklist",
        "",
    ]
    if row["script_problems"]:
        lines.extend(f"- {item}" for item in row["script_problems"])
    else:
        lines.append("- Duration, roles, unique stills, prompt shape, speech bans, and palette all pass.")
    lines.extend(["", "## Render checklist", ""])
    if row["render_problems"] == ["no master at course/masters/"]:
        lines.append("- Not rendered. The renderer refuses this lesson until every still exists and `course/audio/" + script["id"] + ".wav` is committed.")
    elif row["render_problems"]:
        lines.extend(f"- {item}" for item in row["render_problems"])
    else:
        lines.append("- Duration, soundtrack, hook-then-intro order, and outro all pass. Captions are an overlay on a still whose bottom fifth is left empty.")
    lines.extend(["", "## Blocker", ""])
    if row["status"] == "QA passed":
        lines.append("None in the automated checklist. Creative Studio still watches the master before it ships.")
    elif row["status"] == "waiting on images":
        lines.append("Waiting on ChatGPT stills. Code will not draw a replacement and will not reuse another beat.")
    elif row["status"] == "waiting on voice":
        lines.append("Stills are complete. Waiting on `course/audio/" + script["id"] + ".wav` from VOICE_REQUESTS.json.")
    elif row["status"] == "ready to render":
        lines.append("Stills and voice are both on disk. The next watcher batch can render this lesson.")
    else:
        lines.append("A master exists and the automated render checklist has not passed. See the render checklist above.")
    lines.append("")
    (QA_DIR / f"{script['id']}.md").write_text("\n".join(lines))


def write_status(rows: list[dict], elite_rows: list[dict], check_text: str, rendered_now: list[str]) -> None:
    counts: dict[str, int] = {}
    for row in rows:
        counts[row["status"]] = counts.get(row["status"], 0) + 1
    for row in elite_rows:
        counts[row["status"]] = counts.get(row["status"], 0) + 1
    images_have = sum(r["have"] for r in rows)
    images_need = sum(r["beats"] for r in rows)
    ready = [r for r in rows if r["status"] == "QA passed"]
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = [
        "# Asset status",
        "",
        f"Generated {stamp} by `course/tools/watch_assets.py`. This file does not upload anything to Whop.",
        "",
        "Pictures come only from ChatGPT, at the `out_path` values in `IMAGE_REQUESTS.json`. The watcher never draws a still. Elite stays teal and is not in that request file.",
        "",
        "## Counts",
        "",
        f"- Scripted lessons: {len(rows)}",
        f"- Elite lessons with no long-form script yet: {len(elite_rows)}",
        f"- Beats with a still: {images_have} of {images_need}",
        f"- Voice files on disk: {sum(1 for r in rows if r['voice_short'] == 'yes')} of {len(rows)}",
        f"- Waiting on images: {counts.get('waiting on images', 0)}",
        f"- Waiting on voice: {counts.get('waiting on voice', 0)}",
        f"- Ready to render: {counts.get('ready to render', 0)}",
        f"- Rendered: {counts.get('rendered', 0)}",
        f"- QA passed: {counts.get('QA passed', 0)}",
        f"- Rendered this run: {len(rendered_now)}",
        "",
        "## Ready for Creative Studio human QA",
        "",
    ]
    if ready:
        lines.append("These masters passed the automated checklist. A person still watches them before they ship.")
        lines.append("")
        for row in ready:
            lines.append(f"- `{row['id']}` — `course/masters/{row['id']}.mp4`")
    else:
        lines.append("None. A lesson is listed here only after its master exists and both the script checklist and the render checklist pass.")
    lines.extend([
        "",
        "## Scripted lessons",
        "",
        "| Lesson | Course | Status | Images | Voice | Master |",
        "|---|---|---|---:|---|---|",
    ])
    for row in sorted(rows, key=lambda r: priority(r["id"])):
        lines.append(
            f"| `{row['id']}` | {row['course']} | {row['status']} | {row['have']}/{row['beats']} | {row['voice_short']} | {row['master_short']} |"
        )
    lines.extend([
        "",
        "Beat coverage is in each lesson's note under `course/qa/`. Present and missing beat numbers are compressed there (for example `1-40`).",
        "",
        "## Elite queue",
        "",
        "Resume image generation at `el-05` and continue through `el-11` before `el-01` through `el-04`. These lessons have no 15–20 minute script in `course/scripts/`, so they have no beat stills to render. Do not reuse the short Elite stills from the previous cut, and do not restyle Elite to navy and cyan.",
        "",
        "| Lesson | Title | Status |",
        "|---|---|---|",
    ])
    for row in elite_rows:
        lines.append(f"| `{row['id']}` | {row['title']} | {row['status']} |")
    lines.extend([
        "",
        "## Voice",
        "",
        "No wav files are in `course/audio/`. The narrator is Kokoro `af_heart` at 143 words a minute, the same voice as the existing On-Chain Operator renders. Kokoro is not installed here, and ElevenLabs in this environment does not write `course/audio/<id>.wav`. Module 4–14 already has an exact read in `course/audio/needs/`. `VOICE_REQUESTS.json` holds the same voice spec plus the exact read for every lesson that does not have a needs file yet (Blueprint and Modules 1–3). Commit each wav, then rerun the watcher.",
        "",
        "## Image pipeline",
        "",
        "The `openai-image` MCP server is in an error state, so this run did not generate PNGs. Stewart's daily routine checks the ChatGPT limit and commits the files. When a lesson's folder is complete and its wav is present, render the next batch:",
        "",
        "```",
        "python3 course/tools/watch_assets.py --render --batch 3",
        "```",
        "",
        "Ready lessons render in this order: Elite `el-05` through `el-11`, then the earlier Elite lessons, then Blueprint, then On-Chain Operator. A lesson with a failed script checklist is left unrendered.",
        "",
        "## render_tutorial.py --check",
        "",
        "```",
        check_text.rstrip(),
        "```",
        "",
    ])
    STATUS_PATH.write_text("\n".join(lines))


def build_rows(scripts: list[dict]) -> tuple[list[dict], dict[str, dict]]:
    seen: dict[str, str] = {}
    rows = []
    by_id = {}
    for script in scripts:
        problems = script_qa(script, seen)
        missing = missing_images(script)
        have_nums = []
        miss_nums = []
        for beat in script["beats"]:
            path = ROOT / beat["image"]
            if file_ready(path):
                have_nums.append(int(beat["n"]))
            else:
                miss_nums.append(int(beat["n"]))
        voice = AUDIO / f"{script['id']}.wav"
        voice_ok = file_ready(voice)
        master = MASTERS / f"{script['id']}.mp4"
        info = probe(master)
        render_problems = render_qa(script, info, problems)
        qa_passed = info is not None and not render_problems
        status = lesson_status(missing, voice_ok, master, qa_passed)
        if problems and status == "QA passed":
            status = "rendered"
        timeline = sum(beat_seconds(b) for b in script["beats"])
        row = {
            "id": script["id"],
            "course": script["course"],
            "title": script["title"],
            "status": status,
            "beats": len(script["beats"]),
            "have": len(have_nums),
            "present": compress(have_nums),
            "missing": compress(miss_nums),
            "voice": f"`course/audio/{script['id']}.wav`" if voice_ok else "missing",
            "voice_short": "yes" if voice_ok else "no",
            "master": f"`course/masters/{script['id']}.mp4`" if master.is_file() else "not rendered",
            "master_short": "yes" if master.is_file() else "no",
            "script_problems": problems,
            "render_problems": render_problems,
            "render_line": "pass" if info is not None and not render_problems else ("not rendered" if info is None else "fail"),
            "studio": "ready for human QA" if qa_passed else "not ready",
            "timeline_s": timeline,
            "script_ok": not problems,
        }
        if problems and row["status"] == "QA passed":
            row["status"] = "rendered"
            row["studio"] = "not ready"
            row["render_line"] = "fail"
        rows.append(row)
        by_id[script["id"]] = row
    return rows, by_id


def elite_rows(script_ids: set[str]) -> list[dict]:
    rows = []
    for sid, title in ELITE:
        if sid in script_ids:
            continue
        rows.append({
            "id": sid,
            "title": title,
            "status": "waiting on images",
        })
    return rows


def render_ready(scripts: list[dict], by_id: dict[str, dict], batch: int) -> list[str]:
    ready = [
        s for s in scripts
        if by_id[s["id"]]["status"] == "ready to render" and by_id[s["id"]]["script_ok"]
    ]
    ready.sort(key=lambda s: priority(s["id"]))
    done = []
    for script in ready[:batch]:
        subprocess.check_call(
            [sys.executable, str(ROOT / "course" / "render" / "render_tutorial.py"), "--id", script["id"]],
            cwd=ROOT,
        )
        done.append(script["id"])
    return done


def self_test() -> None:
    assert compress([1, 2, 3, 5, 7, 8]) == "1-3, 5, 7-8"
    assert compress([]) == "—"
    assert accent_for({"course": "Grid Bot Elite", "palette": "teal"}) == "0x2EE6A6"
    assert accent_for({"course": "Grid Bot Blueprint", "palette": "navy-cyan"}) == "0x00D4FF"
    assert accent_for({"course": "On-Chain Operator Program", "palette": "navy-cyan"}) == "0x00D4FF"
    assert priority("el-05-portfolio-risk") < priority("el-11-paper-plan")
    assert priority("el-11-paper-plan") < priority("el-01-welcome")
    assert priority("el-04-dynamic-spacing") < priority("bp-01-introduction")
    assert priority("bp-11-advanced-liquidation") < priority("lesson-01-1")
    music = ROOT / "course" / "music" / "komiku-ambiant-truth.ogg"
    assert lesson_status(["missing.png"], False, music, False) == "waiting on images"
    assert lesson_status([], False, music, False) == "waiting on voice"
    assert lesson_status([], True, Path("/no/such/master.mp4"), False) == "ready to render"
    assert lesson_status([], True, music, False) == "rendered"
    assert lesson_status([], True, music, True) == "QA passed"
    assert speech_hit("This is not a guaranteed result.") is None
    assert speech_hit("Returns are guaranteed.") == "guaranteed"
    safe = (
        "Show a hardware key beside a crossed-out speech bubble. The picture must be understandable. "
        "Teaching line: You never type a seed phrase or an API key. Labels, spelled exactly: Key. "
        "No coins, banknotes, profit, P&L"
    )
    assert prompt_hits(safe) == []
    assert "coins" in prompt_hits("Show a pile of coins. The picture must. No coins, banknotes")[0]
    assert "blank page" in prompt_hits("Show a blank page. The picture must. No coins, banknotes")[0]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--render", action="store_true")
    parser.add_argument("--batch", type=int, default=3)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    self_test()
    if args.self_test:
        print("self-test ok")
        return
    scripts = load_scripts()
    rendered_now: list[str] = []
    if args.render:
        rows, by_id = build_rows(scripts)
        rendered_now = render_ready(scripts, by_id, max(args.batch, 0))
    rows, by_id = build_rows(scripts)
    for script in scripts:
        write_note(script, by_id[script["id"]])
    elite = elite_rows({s["id"] for s in scripts})
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        check()
    VOICE_PATH.write_text(json.dumps(voice_payload(scripts), indent=1, ensure_ascii=False) + "\n")
    write_status(rows, elite, buf.getvalue(), rendered_now)
    waiting_images = sum(1 for r in rows if r["status"] == "waiting on images")
    print(
        f"lessons {len(rows)} elite_unscripted {len(elite)} "
        f"waiting_on_images {waiting_images} rendered_now {len(rendered_now)} "
        f"status {STATUS_PATH.name} voice {VOICE_PATH.name}"
    )


if __name__ == "__main__":
    main()
