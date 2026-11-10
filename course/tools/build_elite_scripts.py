"""Write the 11 Grid Bot Elite lessons and append teal prompts.

Does not rebuild Blueprint or On-Chain Operator. Does not upload to Whop.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from build_course_scripts import (  # noqa: E402
    DISCLAIMER,
    LEVERAGE,
    REQUESTS,
    ROOT,
    TARGET_HI,
    TARGET_LO,
    assemble,
    make_beat,
    words,
    your_turn,
)
from build_course_scripts import blueprint_vo  # noqa: E402
from elite_curriculum import LESSONS  # noqa: E402

MUSIC = "course/music/komiku-ambiant-truth.ogg"
NEEDS = ROOT / "course" / "audio" / "needs"


def build_one(lesson: dict) -> dict:
    legal = DISCLAIMER + (LEVERAGE if lesson.get("leverage") else "")
    facts = lesson["facts"]
    first = facts[0]
    built = []
    for fact in facts:
        vo = blueprint_vo(fact)
        if fact is first:
            built.append(make_beat(lesson["title"], lesson["slug"], 0, fact[0], fact[1], vo, fact[2]))
            built.append(make_beat(
                lesson["title"], lesson["slug"], 0, "Disclaimer", "legal", legal,
                "Education only, not financial advice.",
            ))
            continue
        built.append(make_beat(lesson["title"], lesson["slug"], 0, fact[0], fact[1], vo, fact[2]))
    intro_vo = (
        f"This is Grid Bot Elite. The lesson is {lesson['title']}. "
        "Teal on the frame. Not the Blueprint plate. Education only. "
        "You will write on paper before any screen."
    )
    intro = make_beat(lesson["title"], lesson["slug"], 0, "Title card", "intro", intro_vo, lesson["title"])
    built.insert(2, intro)
    teach = [fact for fact in facts if fact[1] in {"body", "diagram", "demo"}]
    guard = 0
    while teach and sum(words(b["vo"]) for b in built) < TARGET_LO and guard < 24:
        fact = teach[guard % len(teach)]
        built.insert(-1, make_beat(
            lesson["title"], lesson["slug"], 0, "Your turn", "demo", your_turn(fact), "Practice: " + fact[2],
        ))
        guard += 1
    while sum(words(b["vo"]) for b in built) > TARGET_HI:
        idx = next((
            i for i in range(len(built) - 2, 2, -1)
            if built[i]["role"] == "demo"
        ), None)
        if idx is None:
            break
        built.pop(idx)
    if lesson["next"]:
        outro_vo = (
            f"Next lesson: {lesson['next']}. Bring the page you just wrote. "
            "Leave every example marked Example. No order is sent between lessons."
        )
    else:
        outro_vo = (
            "This is the last Elite lesson. The assignment is the paper plan. "
            "Keep the pages. No order is sent."
        )
    built.append(make_beat(
        lesson["title"], lesson["slug"], 0, "Outro", "outro", outro_vo, outro_vo,
    ))
    return assemble(
        lesson["slug"], lesson["title"], "Grid Bot Elite", "teal", MUSIC, built, lesson["next"],
    )


def write_needs(script: dict) -> None:
    NEEDS.mkdir(parents=True, exist_ok=True)
    payload = {
        "id": script["id"],
        "voice": "af_heart",
        "wpm": 143,
        "wav": f"course/audio/{script['id']}.wav",
        "status": "needed",
        "notes": "Kokoro af_heart, the same narrator as the On-Chain Operator renders. Elite stays teal. Do not synthesize a different voice.",
        "beats": [
            {"n": b["n"], "role": b["role"], "vo": b["vo"]}
            for b in script["beats"]
        ],
    }
    (NEEDS / f"{script['id']}.json").write_text(json.dumps(payload, indent=1) + "\n")


def append_requests(scripts: list[dict]) -> None:
    payload = json.loads(REQUESTS.read_text())
    payload["palette"] = (
        "navy and cyan for On-Chain Operator and Grid Bot Blueprint. "
        "Grid Bot Elite requests in this file use palette teal and must not be recolored."
    )
    payload["notes"] = (
        "The orchestrator generates each PNG with ChatGPT and commits it at out_path. "
        "Elite prompts are teal. Do not draw the picture in code. "
        "After the files exist and any fallback stills are marked pass, run course/render/render_tutorial.py. "
        "No Whop upload."
    )
    existing = {item["id"] for item in payload["requests"]}
    added = 0
    for script in scripts:
        for beat in script["beats"]:
            rid = f"{script['id']}-{beat['n']:03d}"
            item = {
                "id": rid,
                "lesson": script["id"],
                "course": script["course"],
                "title": script["title"],
                "beat": beat["n"],
                "role": beat["role"],
                "chapter": beat["chapter"],
                "concept": beat["concept"],
                "out_path": beat["image"],
                "size": "1536x1024",
                "palette": "teal",
                "prompt": beat["prompt"],
            }
            if rid in existing:
                for i, old in enumerate(payload["requests"]):
                    if old["id"] == rid:
                        payload["requests"][i] = item
                        break
            else:
                payload["requests"].append(item)
                existing.add(rid)
                added += 1
    payload["count"] = len(payload["requests"])
    REQUESTS.write_text(json.dumps(payload, indent=1) + "\n")
    print(f"image requests added {added} total {payload['count']}")


def main() -> None:
    scripts = [build_one(lesson) for lesson in LESSONS]
    problems = []
    for script in scripts:
        if not (15 <= script["estimated_minutes"] <= 20):
            problems.append(f"{script['id']} {script['estimated_minutes']} min")
        roles = {b["role"] for b in script["beats"]}
        for need in ("hook", "legal", "intro", "demo", "recap", "action", "outro"):
            if need not in roles:
                problems.append(f"{script['id']} missing {need}")
        if script["palette"] != "teal":
            problems.append(f"{script['id']} palette")
        if "#00D4FF" in script["beats"][0]["prompt"].split("Do not recolor", 1)[0]:
            problems.append(f"{script['id']} hook prompt uses cyan before the ban line")
    out = ROOT / "course" / "scripts"
    for script in scripts:
        (out / f"{script['id']}.json").write_text(json.dumps(script, indent=1) + "\n")
        write_needs(script)
        print(f"  {script['id']:32} {script['word_count']:5} words  {script['estimated_minutes']:5} min  beats {len(script['beats'])}")
    append_requests(scripts)
    if problems:
        print("PROBLEMS")
        for item in problems:
            print(" -", item)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
