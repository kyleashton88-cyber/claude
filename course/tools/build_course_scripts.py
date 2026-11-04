"""Build 15–20 minute tutorial scripts and IMAGE_REQUESTS.json.

Images are not generated here. The orchestrator fills course/images from the requests.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from blueprint_curriculum import LESSONS  # noqa: E402
from prompt_writer import write_prompt  # noqa: E402

GOLD = ROOT / "programs" / "defi-program" / "video-scripts" / "gold"
OUT_SCRIPTS = ROOT / "course" / "scripts"
REQUESTS = ROOT / "IMAGE_REQUESTS.json"

WPM = 143  # measured on the current On-Chain Operator renders
TARGET_LO = 2350
TARGET_HI = 2550

DISCLAIMER = (
    "Education only, not financial advice. Crypto and DeFi carry significant risk, including total loss of capital. "
    "This is general information. It does not consider your objectives, financial situation, or needs. "
    "Past or example results do not indicate future results. Consider independent advice. "
    "We do not sell or run a trading bot."
)
LEVERAGE = (
    " Leverage magnifies losses. A leveraged position can be liquidated, and you can lose all the money you commit."
)

BANNED = re.compile(
    r"\b(guaranteed|risk-free|you will earn|will profit|you should buy|you should sell|passive income)\b",
    re.I,
)


def words(text: str) -> int:
    return len(re.findall(r"[A-Za-z0-9'%.]+", text or ""))


def clean_vo(text: str) -> str:
    text = re.sub(r"\[\[pause[^\]]*\]\]", "", text or "")
    text = re.sub(r"\bguaranteed\b", "certain", text, flags=re.I)
    text = re.sub(r"\brisk-free\b", "without a downside", text, flags=re.I)
    text = re.sub(r"\bfree money\b", "a gift", text, flags=re.I)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def cap_of(text: str, limit: int = 110) -> str:
    text = clean_vo(text)
    if len(text) <= limit:
        return text
    cut = text[:limit].rsplit(" ", 1)[0]
    return cut.rstrip(".,;") + "."


def blueprint_vo(fact: tuple) -> str:
    chapter, role, say, why, draw, paper, trap = fact
    return " ".join([
        say,
        why,
        f"On the diagram for this beat, look for {draw}.",
        "The shapes are the lesson. If a shape is only decoration, it does not belong on this frame.",
        paper,
        "Mark the page Example, so a later reader cannot mistake the sketch for a recommendation to trade an asset or these levels.",
        trap,
        f"Say the opening line once more, and point at the part that belongs to {chapter}.",
        "If you cannot point yet, do not move on. The point of the beat is the pointing.",
    ])


def your_turn(fact: tuple) -> str:
    chapter, _role, say, _why, draw, paper, _trap = fact
    return " ".join([
        f"Your turn, still inside {chapter}.",
        "Cover the notes and say this from memory: " + say,
        f"Then uncover the diagram and check that you can still see {draw}.",
        paper,
        "Write one check question a classmate could answer from the drawing alone, and write the answer under it.",
        "The answer has to name a shape on the page. An answer about what the market will do is the wrong kind of answer.",
        "This is practice on paper. No order is sent.",
    ])


def make_beat(lesson_title: str, slug: str, n: int, chapter: str, role: str, vo: str, concept: str,
              labels: list[str] | None = None) -> dict:
    image = f"course/images/{slug}/{n:03d}.png"
    prompt = write_prompt(concept, chapter, role, n, lesson_title, labels)
    if BANNED.search(vo):
        raise SystemExit(f"banned phrase in {slug} beat {n}: {vo[:180]}")
    return {
        "n": n,
        "chapter": chapter,
        "role": role,
        "vo": vo,
        "cap": cap_of(vo),
        "concept": concept,
        "image": image,
        "image_status": "needed",
        "prompt": prompt,
    }


def assemble(slug: str, title: str, course: str, palette: str, music: str, beats: list[dict],
             next_title: str | None) -> dict:
    # Renumber in order and rebuild prompts so beat numbers match.
    fixed = []
    for i, b in enumerate(beats, start=1):
        b = dict(b)
        b["n"] = i
        b["image"] = f"course/images/{slug}/{i:03d}.png"
        b["prompt"] = write_prompt(b["concept"], b["chapter"], b["role"], i, title)
        fixed.append(b)
    total_words = sum(words(b["vo"]) for b in fixed)
    minutes = total_words / WPM
    return {
        "id": slug,
        "title": title,
        "course": course,
        "palette": palette,
        "music": music,
        "next": next_title,
        "wpm_assumption": WPM,
        "word_count": total_words,
        "estimated_minutes": round(minutes, 2),
        "code_draws_visuals": False,
        "overlays_only": ["captions", "lower thirds", "intro title text", "disclaimer line", "Ken Burns"],
        "beats": fixed,
    }


def build_blueprint() -> list[dict]:
    music = "course/music/komiku-ambiant-obscur-technology.ogg"
    out = []
    for lesson in LESSONS:
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
            f"This is the Grid Bot Blueprint. The lesson is {lesson['title']}. "
            "Navy and cyan on the frame. Education only. You will write on paper before any screen."
        )
        intro = make_beat(lesson["title"], lesson["slug"], 0, "Title card", "intro", intro_vo, lesson["title"])
        built.insert(2, intro)
        # Practice beats until the lesson is long enough, never past the top of the band.
        for fact in facts:
            if fact[1] not in {"body", "diagram", "demo"}:
                continue
            if sum(words(b["vo"]) for b in built) >= TARGET_LO:
                break
            built.insert(-1, make_beat(
                lesson["title"], lesson["slug"], 0, "Your turn", "demo", your_turn(fact), "Practice: " + fact[2],
            ))
        if not any(b["role"] == "recap" for b in built):
            recap_vo = (
                f"Recap for {lesson['title']}. Say the hook in one line, name the diagram you drew, "
                "and name the line you wrote in the notebook. "
                "If one of those three is missing, the lesson is not finished. "
                "Stamp Example. Education only."
            )
            built.insert(-1, make_beat(
                lesson["title"], lesson["slug"], 0, "Recap", "recap", recap_vo, lesson["title"] + " recap",
            ))
        if lesson["next"]:
            outro_vo = (
                f"Next lesson: {lesson['next']}. Bring the page you just wrote. "
                "Leave every example marked Example. No order is sent between lessons."
            )
        else:
            outro_vo = (
                "This is the last Blueprint lesson. The spot path stands without this opt-in chapter. "
                "Keep the pages. No order is sent."
            )
        built.append(make_beat(
            lesson["title"], lesson["slug"], 0, "Outro", "outro", outro_vo,
            outro_vo,
        ))
        script = assemble(
            lesson["slug"], lesson["title"], "Grid Bot Blueprint", "navy-cyan", music, built, lesson["next"]
        )
        out.append(script)
    return out


def scene_bits(scene: dict) -> list[str]:
    bits = []
    for key in ("title", "q", "a", "sub", "kicker"):
        val = scene.get(key)
        if isinstance(val, str) and val.strip():
            bits.append(val.strip())
    for key in ("lines",):
        for line in scene.get(key) or []:
            if isinstance(line, str):
                bits.append(line)
    items = scene.get("items") or []
    for it in items:
        if isinstance(it, str):
            bits.append(it)
        elif isinstance(it, dict):
            chunk = " ".join(str(it[k]) for k in ("title", "text", "label") if it.get(k))
            if chunk:
                bits.append(chunk)
    for side in ("left", "right"):
        block = scene.get(side)
        if isinstance(block, dict):
            if block.get("label"):
                bits.append(str(block["label"]))
            for it in block.get("items") or []:
                if isinstance(it, str):
                    bits.append(it)
    steps = scene.get("steps") or []
    for st in steps:
        if isinstance(st, str):
            bits.append(st)
        elif isinstance(st, dict):
            chunk = " ".join(str(st[k]) for k in ("title", "text", "label") if st.get(k))
            if chunk:
                bits.append(chunk)
    # de-dup, keep order
    seen = set()
    out = []
    for b in bits:
        if b not in seen:
            seen.add(b)
            out.append(b)
    return out


def split_vo(text: str, size: int = 70) -> list[str]:
    text = clean_vo(text)
    sentences = re.split(r"(?<=[.?!])\s+", text)
    chunks, cur = [], ""
    for sent in sentences:
        if not sent:
            continue
        if words(cur) + words(sent) > size and cur:
            chunks.append(cur.strip())
            cur = sent
        else:
            cur = (cur + " " + sent).strip()
    if cur:
        chunks.append(cur.strip())
    return chunks or [text]


def teach_bit(title: str, bit: str, chapter: str) -> str:
    return " ".join([
        f"Let us slow this one down. The line from {title} is: {bit}.",
        "Draw it as its own shape, not as a bullet lost in a list.",
        f"The chapter is {chapter}. Write the line in the notebook, then write one reason in your own words.",
        "Use round example numbers only if the line already has numbers, and stamp the page Example.",
        "The reason has to match the line. A reason about what you hope the market will do does not count.",
        "Point at the shape and say the line once. If the point and the line disagree, fix the drawing.",
        "This is education. It is not an instruction to open, close, or size a position.",
    ])


def build_oco() -> list[dict]:
    ids = [f"lesson-01-{n}" for n in range(1, 10)]
    ids += [f"lesson-02-{n}" for n in range(0, 9)]
    ids += [f"lesson-03-{n}" for n in range(0, 6)]
    music = "course/music/komiku-ambiant-truth.ogg"
    scripts = []
    for sid in ids:
        gold = json.loads((GOLD / f"{sid}.json").read_text())
        title = gold["title"].split(":", 1)[-1].strip()
        beats_src: list[tuple[str, str, str, str]] = []
        # Collect original narration first.
        original_chunks: list[tuple[str, str, str]] = []
        for scene in gold["scenes"]:
            vo = clean_vo(scene.get("vo") or "")
            if not vo:
                continue
            chapter = scene.get("chapter") or scene.get("type") or "Lesson"
            role = {
                "title": "body",
                "quiz": "quiz",
                "cta": "action",
                "steps": "demo",
                "flow": "diagram",
                "chart": "diagram",
                "compare": "body",
                "image": "diagram",
            }.get(scene.get("type"), "body")
            for chunk in split_vo(vo):
                original_chunks.append((chapter, role, chunk))
        # Hook is the first chunk. Then we will add legal and intro around it in assemble step.
        for chapter, role, chunk in original_chunks:
            if not beats_src:
                beats_src.append((chapter, "hook", chunk, chunk))
            else:
                beats_src.append((chapter, role, chunk, chunk))
        # Paper teaching from on-screen bits, enough to reach the word target.
        extras = []
        for scene in gold["scenes"]:
            chapter = scene.get("chapter") or "Practice"
            for bit in scene_bits(scene):
                if words(bit) < 2:
                    continue
                extras.append((chapter, "demo", teach_bit(title, bit, chapter), bit))
        # Recap and action if the gold script is thin on them.
        chapters = []
        for scene in gold["scenes"]:
            ch = scene.get("chapter")
            if ch and ch not in chapters:
                chapters.append(ch)
        recap_lines = chapters[:3] or [title]
        recap = (
            "Recap, three lines. "
            + " ".join(f"Line: {line}." for line in recap_lines)
            + " Say them without looking, then check the page. "
            "Each line should point at a drawing, not at a hope about price. "
            "Education only, not financial advice."
        )
        action = (
            f"Your action for {title}: open the notebook, copy the three recap lines, and work one example you mark Example. "
            "Do the arithmetic on paper if the lesson had numbers. If it had a checklist, complete it in writing. "
            "Stop before any live signature, any seed phrase, and any size you were not already using as a hypothetical. "
            "Bring the page to the next lesson. No order is sent by this video."
        )
        required = [
            ("Recap", "recap", recap, "; ".join(recap_lines)),
            ("Action", "action", action, f"Paper action for {title}"),
        ]
        # Fill with paper beats, leaving room for the recap and the action.
        vo_words = sum(words(v) for *_, v, __ in beats_src)
        reserve = sum(words(item[2]) for item in required)
        for extra in extras:
            if vo_words + reserve >= TARGET_LO:
                break
            beats_src.append(extra)
            vo_words += words(extra[2])
        beats_src.extend(required)
        vo_words += reserve
        # Second pass: teach-back of each original chunk's first sentence, if still short.
        if vo_words < TARGET_LO:
            for chapter, role, chunk in original_chunks:
                if vo_words >= TARGET_LO:
                    break
                first = chunk.split(".")[0].strip()
                if words(first) < 4:
                    continue
                back = (
                    f"Teach this back. The claim was: {first}. "
                    f"In {chapter}, say what that claim rules out, in one sentence. "
                    "Then draw only the part the claim names. "
                    "A classmate should be able to grade the drawing without hearing you. "
                    "Stamp Example. This check is understanding, not a trade."
                )
                beats_src.append((chapter, "demo", back, first))
                vo_words += words(back)
        legal = DISCLAIMER
        if re.search(r"liquidat|leverage|margin|perpetual", title, re.I):
            legal += LEVERAGE
        # Insert legal and intro after hook.
        hook = beats_src[0]
        rest = beats_src[1:]
        intro_vo = (
            f"On-Chain Operator. {gold['title']}. "
            "The frame is navy and cyan. You will see one idea at a time, then write it down. "
            "Education only."
        )
        ordered = [
            hook,
            ("Disclaimer", "legal", legal, "Education only, not financial advice."),
            ("Title card", "intro", intro_vo, title),
            *rest,
        ]
        outro_vo = (
            "That is the end of this lesson. Keep the notebook page. "
            "The next lesson continues the same program. "
            "Reread the recap once before you close the page. Education only, not financial advice."
        )
        ordered.append(("Outro", "outro", outro_vo, "Lesson outro"))
        built = [
            make_beat(title, sid, i, ch, role, vo, concept)
            for i, (ch, role, vo, concept) in enumerate(ordered, start=1)
        ]
        # Trim from the end of the practice block if we overshot, but never trim hook, legal, intro, recap, action, outro.
        while sum(words(b["vo"]) for b in built) > TARGET_HI:
            idx = next((
                i for i in range(len(built) - 2, 2, -1)
                if built[i]["role"] == "demo" and built[i]["chapter"] not in {"Recap", "Action"}
            ), None)
            if idx is None:
                break
            built.pop(idx)
        script = assemble(sid, gold["title"], "On-Chain Operator Program", "navy-cyan", music, built, None)
        scripts.append(script)
    return scripts


def check(scripts: list[dict]) -> list[str]:
    problems = []
    prompts = []
    for s in scripts:
        mins = s["estimated_minutes"]
        if not (15 <= mins <= 20):
            problems.append(f"{s['id']} estimated {mins} min ({s['word_count']} words)")
        roles = {b["role"] for b in s["beats"]}
        for need in ("hook", "intro", "legal", "demo", "recap", "action", "outro"):
            if need not in roles and not (need == "demo" and "diagram" in roles):
                # demo may be satisfied by diagram + quiz practice
                if need == "demo" and ({"quiz", "diagram", "demo"} & roles):
                    continue
                problems.append(f"{s['id']} missing role {need}")
        images = [b["image"] for b in s["beats"]]
        if len(images) != len(set(images)):
            problems.append(f"{s['id']} reused an image path")
        for b in s["beats"]:
            prompts.append(b["prompt"])
            if "grey placeholder" in b["prompt"].lower() or len(b["prompt"]) < 200:
                problems.append(f"{s['id']} beat {b['n']} thin prompt")
            if BANNED.search(b["vo"]):
                problems.append(f"{s['id']} beat {b['n']} banned phrase")
    if len(prompts) != len(set(prompts)):
        problems.append("duplicate prompts across the course")
    return problems


def main() -> None:
    scripts = build_blueprint() + build_oco()
    problems = check(scripts)
    OUT_SCRIPTS.mkdir(parents=True, exist_ok=True)
    requests = []
    for s in scripts:
        path = OUT_SCRIPTS / f"{s['id']}.json"
        path.write_text(json.dumps(s, indent=1) + "\n")
        for b in s["beats"]:
            requests.append({
                "id": f"{s['id']}-{b['n']:03d}",
                "lesson": s["id"],
                "course": s["course"],
                "title": s["title"],
                "beat": b["n"],
                "role": b["role"],
                "chapter": b["chapter"],
                "concept": b["concept"],
                "out_path": b["image"],
                "size": "1536x1024",
                "palette": "navy-cyan",
                "prompt": b["prompt"],
            })
    payload = {
        "generator": "openai-image",
        "do_not_generate_in_this_repo_step": True,
        "palette": "navy and cyan for On-Chain Operator and Grid Bot Blueprint. Elite stays teal and is not in this file.",
        "notes": (
            "The orchestrator generates each PNG with ChatGPT (openai-image) and commits it at out_path. "
            "Do not draw the picture in code. After the files exist, run course/render/render_tutorial.py. "
            "No Whop upload."
        ),
        "count": len(requests),
        "requests": requests,
    }
    REQUESTS.write_text(json.dumps(payload, indent=1) + "\n")
    print(f"scripts {len(scripts)} requests {len(requests)}")
    for s in scripts:
        print(f"  {s['id']:28} {s['word_count']:5} words  {s['estimated_minutes']:5} min  beats {len(s['beats'])}")
    if problems:
        print("PROBLEMS")
        for p in problems:
            print(" -", p)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
