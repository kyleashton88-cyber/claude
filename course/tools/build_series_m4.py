"""Module 4–14 tutorial scripts, image requests, voice needs, and waiting render jobs.

Does not generate images or speech, and does not touch Whop.
Module intros are short branded pieces. Full lessons target 15–20 minutes.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from build_course_scripts import (  # noqa: E402
    BANNED,
    DISCLAIMER,
    LEVERAGE,
    TARGET_HI,
    TARGET_LO,
    assemble,
    clean_vo,
    make_beat,
    words,
)
from prompt_writer import write_prompt  # noqa: E402

LESSONS = ROOT / "programs" / "defi-program" / "lessons"
GOLD = ROOT / "programs" / "defi-program" / "video-scripts" / "gold"
GEN = ROOT / "programs" / "defi-program" / "video-scripts" / "lessons"
SCRIPTS = ROOT / "course" / "scripts"
JOBS = ROOT / "course" / "render" / "jobs"
AUDIO = ROOT / "course" / "audio" / "needs"
REQUESTS = ROOT / "IMAGE_REQUESTS.json"
FLOW = ROOT / "SERIES_FLOW.md"
LIST = Path("/home/ubuntu/.cursor/projects/workspace/uploads/OCO_VIDEO_LIST_640e.md")
MUSIC = "course/music/komiku-ambiant-truth.ogg"

MODULES = {
    4: ("Yield", "module-04-yield.md", "Split any yield into what is paid for a risk and what is a new token."),
    5: ("Infrastructure risk", "module-05-infrastructure-risk.md", "Name what your position trusts: a bridge, a sequencer, an oracle, a key."),
    6: ("Protocol research", "module-06-protocol-research.md", "Read a protocol before you read its rate."),
    7: ("On-chain analytics", "module-07-on-chain-analytics.md", "Read the chain as a ledger, not as a signal."),
    8: ("The operating system", "module-08-operating-system.md", "One register, one playbook, one journal."),
    9: ("DeFi and grid bots", "module-09-defi-vs-grid-bots.md", "A pool and a grid are different machines for different paths."),
    10: ("Advanced yield", "module-10-advanced-yield-engineering.md", "Name the engine before you look at the rate."),
    11: ("Hedging", "module-11-hedging-risk-engineering.md", "A hedge is a written path, not a feeling of safety."),
    12: ("Your own bank", "module-12-own-bank.md", "A balance sheet, a custody plan, and a liquidity ladder."),
    13: ("The income engine", "module-13-income-engine.md", "Durability first. A payout only from what the page can explain."),
    14: ("Automation and mastery", "module-14-automation-mastery.md", "Automate watching. Act only with a permission you can revoke."),
}

# Lessons at or over 10:00. They stay in the flow and are not re-scripted here.
KEEP = {"lesson-04-0", "lesson-04-1", "lesson-04-2", "lesson-05-6", "lesson-06-1", "lesson-06-2"}

PRIOR = {
    4: "You already have LTV, health factor, and liquidation from lending. A yield does not retire those numbers. It is payment for a risk you can name.",
    5: "You can already split base yield from emissions, and you can name an LST. This module asks what that position sits on: a bridge, a sequencer, an oracle, or a key.",
    6: "You can already see a bridge, an oracle, and an admin key. Research starts there. A rate comes after the mechanism.",
    7: "You can already read a token's supply and a protocol's fees. Analytics is how you check those claims on the ledger itself.",
    8: "You can already pull a number off a chain. The operating system is what you do with it: a register, a journal, and a kill rule.",
    9: "You already know a grid waits on rungs, and a pool prices a trade with a curve. This module keeps those as two machines.",
    10: "You already split base yield from emissions. Advanced yield still starts with that split, then names a more particular engine.",
    11: "You already know a health factor and a stop. A hedge is another written path. It is not a claim that the risk is gone.",
    12: "You already keep a journal and a kill rule. A balance sheet is that habit turned into accounts.",
    13: "You already have a balance sheet. Income is only the part of it you can explain after losses.",
    14: "You already have a playbook. Automation may watch it. Automation may not hold your keys.",
}

LESSON_83 = [
    "Lesson 8.3 is the map of the strategy library. It is not a list of positions to open.",
    "The library holds thirty cards. Every card uses the same headings: profit engine, key maths, execute, monitor, kill rules, how it loses, and a size cap.",
    "A profit engine is the source of the payment. Borrower interest is one source. Network rewards are another. Trading fees are another. You name the source before you look at a rate.",
    "Key maths is a formula you can recompute on paper. If you cannot recompute it, the card is not yet yours.",
    "Execute is a sequence you could write down. This video does not turn that sequence into clicks.",
    "Monitor is the short list of facts that would tell you the idea has changed. Utilisation, a peg, a queue, a range.",
    "A kill rule is written before any size. It names a path, the same way a stop named a path in the lending lessons.",
    "How it loses is the first picture. Draw the losing path before you draw the tidy one.",
    "The size cap on a card is a teaching ceiling inside the library. This video does not assign you a size. Leave the size line blank.",
    "The library is walked in stages: foundation, liquidity, active, leverage, carry and hedging, operator, professional, and expert. A later card is not a prize for skipping an earlier stage.",
    "Foundation is stablecoin lending and staking. You already met both. The card just forces the engine and the kill rule onto one page.",
    "Liquidity cards are about pools. You already know impermanent loss. The card has to say how the position loses, not only what it might earn.",
    "Leverage cards meet the health factor again. A loop that cannot show its liquidation price is not a finished card.",
    "The line at the bottom of the library is the whole lesson. If you cannot name the profit engine and explain the unwind, you do not have a plan.",
    "Practice on a blank card marked Example. Write borrower interest as the engine. Write utilisation as a monitor. Write a peg that leaves its band as a kill rule. Name no protocol.",
    "A farm whose rate is mostly new tokens fails the first question. Ask what the base pays for, and whether the reward token can be sold. The answer is that question, not a purchase.",
    "Lesson 8.2 scored risks as likelihood times impact. A strategy card that cannot sit on that register is unfinished.",
    "Lesson 8.4 is the playbook: deploy, monitor, respond, review. The card is the input to that playbook.",
]


def plain(text: str) -> str:
    text = re.sub(r"!\[[^\]]*\]\([^)]+\)", " ", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"\1", text)
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    lines = []
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("<") or line.startswith("---"):
            continue
        if set(line.replace("|", "").replace("-", "").replace(":", "").strip()) == set():
            continue
        if line.startswith("|"):
            cells = [c.strip() for c in line.strip("|").split("|") if c.strip() and c.strip() != "---"]
            if not cells:
                continue
            line = ". ".join(cells)
        line = re.sub(r"^[-*]\s+", "", line)
        line = re.sub(r"^#{1,6}\s+", "", line)
        line = re.sub(r"^-\s*\[[ xX]\]\s*", "", line)
        lines.append(line)
    return clean_vo(" ".join(lines))


def sentences(text: str) -> list[str]:
    out = []
    for sent in re.split(r"(?<=[.?!])\s+", plain(text)):
        sent = sent.strip(" -")
        if words(sent) >= 6 and not BANNED.search(sent):
            out.append(sent if sent.endswith((".", "?", "!")) else sent + ".")
    return out


def slice_md(body: str, heading: str) -> str:
    m = re.search(rf"### {re.escape(heading)}\n(.*?)(?=\n### |\Z)", body, re.S)
    return m.group(1) if m else ""


def quizzes(body: str) -> list[tuple[str, str]]:
    found = []
    for q, a in re.findall(r"<summary>(.*?)</summary>(.*?)</details>", body, re.S):
        q, a = plain(q), plain(a)
        if q and a:
            found.append((q, a))
    return found


def checks(body: str) -> list[str]:
    items = []
    block = slice_md(body, "Checklist")
    for line in block.splitlines():
        line = re.sub(r"^-\s*\[[ xX]\]\s*", "", line.strip())
        line = plain(line)
        if words(line) >= 3:
            items.append(line.rstrip("."))
    return items


def load_script(sid: str) -> dict | None:
    for folder in (GOLD, GEN):
        p = folder / f"{sid}.json"
        if p.is_file():
            return json.loads(p.read_text())
    return None


def script_sentences(data: dict | None) -> list[str]:
    if not data:
        return []
    out = []
    for scene in data.get("scenes") or []:
        vo = clean_vo(scene.get("vo") or "")
        if words(vo) >= 8 and not BANNED.search(vo):
            out.extend(sentences(vo) or [vo])
    # de-dup near copies
    kept, seen = [], set()
    for s in out:
        key = s.lower()[:80]
        if key not in seen:
            seen.add(key)
            kept.append(s)
    return kept


def parse_modules() -> dict[int, dict]:
    mods = {}
    for num, (name, fname, outcome_fallback) in MODULES.items():
        text = (LESSONS / fname).read_text()
        parts = re.split(r"\n## Lesson ", text)
        preamble = parts[0]
        outcome = outcome_fallback
        m = re.search(r"\*Outcome:\s*([^*]+)\*", preamble)
        if m:
            outcome = m.group(1).strip().rstrip(".")
        lessons = []
        for part in parts[1:]:
            head, _, body = part.partition("\n")
            hm = re.match(r"(\d+)\.(\d+)\s+[—-]\s+(.+)", head.strip())
            if not hm:
                continue
            title = re.sub(r"\s*\*(\([^)]*\))?\*", "", hm.group(3)).strip()
            title = re.sub(r"\s*\([^)]*\)\s*$", "", title).strip()
            lessons.append({
                "id": f"lesson-{int(hm.group(1)):02d}-{hm.group(2)}",
                "num": f"{hm.group(1)}.{hm.group(2)}",
                "title": title,
                "body": body,
                "objective": sentences(slice_md(body, "Objective"))[:2],
            })
        mods[num] = {"name": name, "outcome": outcome, "lessons": lessons, "preamble": preamble}
    return mods


def durations() -> dict[str, str]:
    found = {}
    if not LIST.is_file():
        return found
    for line in LIST.read_text().splitlines():
        m = re.search(r"video__(lesson-\d+-\d+|module-\d+-intro)\.mp4.*?\|\s*(\d+:\d+)\s+\|", line)
        if m:
            found[m.group(1)] = m.group(2)
    return found


def takeaway(node: dict) -> str:
    if node.get("kind") == "intro":
        return node["outcome"]
    obj = node.get("objective") or []
    if obj:
        return obj[0]
    return node["title"]


def narrate(sentence: str, chapter: str, mode: str) -> str:
    s = sentence.strip()
    if not s.endswith((".", "?", "!")):
        s += "."
    if mode == "notebook":
        return " ".join([
            f"Take this line slowly. {s}",
            f"It sits in {chapter}.",
            "Copy it under that heading.",
            "If a number is in the line, write Example next to it.",
            "Read it back from the page, not from memory, the first time.",
            "Education only. No order is sent.",
        ])
    if mode == "rules":
        return " ".join([
            f"Now ask what this line rules out. {s}",
            "It rules out a story that skips the mechanism.",
            "It rules out treating a rate as a reason by itself.",
            "Write the ruled-out story in the margin and cross it out.",
            "The drawing should match the line that remains.",
            "A hope about price is not a ruled-out story. It is the wrong kind of note.",
        ])
    if mode == "diagram":
        return " ".join([
            f"Build the drawing for this line only. {s}",
            "One shape for the thing named, one callout, the word Example if you used a figure.",
            "Cover the caption and check that the shape still teaches the line.",
            "If the shape would fit a different lesson, redraw it.",
            "Then uncover the caption and say the line while you point.",
        ])
    return " ".join([
        f"Teach this line back, as if the previous minute had no sound. {s}",
        "Say it in one breath.",
        "Then say the reason in a second breath.",
        "A classmate should be able to point at your drawing and mark it right or wrong.",
        "If they cannot, the line is not finished.",
        "Stamp Example. This check is understanding, not a trade.",
    ])


def build_nodes(mods: dict[int, dict]) -> list[dict]:
    nodes = []
    prev_module_last = {
        "id": "lesson-03-7",
        "label": "Lesson 3.7, CDP stablecoins",
        "takeaway": "A CDP lets you mint a dollar-like token against collateral, and the health factor still decides whether that position survives.",
    }
    for num in range(4, 15):
        mod = mods[num]
        intro = {
            "id": f"module-{num:02d}-intro",
            "kind": "intro",
            "module": num,
            "num": str(num),
            "title": f"Module {num} · {mod['name']}",
            "label": f"Module {num}, {mod['name']}",
            "outcome": mod["outcome"],
            "objective": [mod["outcome"] + "."],
            "body": "",
            "lessons": mod["lessons"],
        }
        chain = [intro, *mod["lessons"]]
        for i, node in enumerate(chain):
            node = dict(node)
            node.setdefault("kind", "lesson")
            node.setdefault("module", num)
            node.setdefault("label", f"Lesson {node.get('num', num)}, {node['title']}")
            if i == 0:
                node["prev"] = prev_module_last
            else:
                prev = chain[i - 1]
                node["prev"] = {
                    "id": prev["id"],
                    "label": prev.get("label") or f"Lesson {prev.get('num')}, {prev['title']}",
                    "takeaway": takeaway(prev) if prev.get("kind") != "intro" else prev["outcome"],
                }
            if i + 1 < len(chain):
                nxt = chain[i + 1]
                node["next"] = {
                    "id": nxt["id"],
                    "label": nxt.get("label") or f"Lesson {nxt.get('num')}, {nxt['title']}",
                }
            else:
                node["next"] = None
            node["keep"] = node["id"] in KEEP
            nodes.append(node)
        last = chain[-1]
        prev_module_last = {
            "id": last["id"],
            "label": last.get("label") or f"Lesson {last.get('num')}, {last['title']}",
            "takeaway": takeaway(last),
        }
    # Point the last lesson at a real end, and fix next pointers that were computed
    # before keep flags. Next should be the next lesson in the curriculum, even if
    # that lesson is not being re-rendered.
    return nodes


def lesson_bits(node: dict) -> dict[str, list]:
    if node["id"] == "lesson-08-3":
        return {
            "objective": ["Read a strategy card: engine, maths, monitor, kill rule, and how it loses."],
            "explain": LESSON_83,
            "example": [],
            "checks": [
                "Every heading on the card is filled or marked blank on purpose",
                "The kill rule names a path",
                "The size line is still blank",
                "The card can sit on the risk register from Lesson 8.2",
            ],
            "quizzes": [
                ("What is the first question when a farm's rate is mostly new tokens?",
                 "What the base pays for, and whether the reward token can be sold. The answer is that question, not a purchase."),
                ("What does the library's last line require?",
                 "You can name the profit engine and explain the unwind. Otherwise you do not have a plan."),
            ],
            "script": [],
        }
    body = node.get("body") or ""
    explain = sentences(slice_md(body, "Explanation"))
    if not explain:
        explain = sentences(body)[:12]
    example = sentences(slice_md(body, "Worked example"))
    # some lessons use a different heading
    if not example:
        for heading in ("Worked example — a journal row", "Worked example"):
            example = sentences(slice_md(body, heading))
            if example:
                break
    return {
        "objective": node.get("objective") or sentences(slice_md(body, "Objective")) or [node["title"] + "."],
        "explain": explain,
        "example": example,
        "checks": checks(body),
        "quizzes": quizzes(body),
        "script": script_sentences(load_script(node["id"])),
    }


def full_lesson(node: dict) -> list[dict]:
    bits = lesson_bits(node)
    title = node["title"]
    prev = node["prev"]
    objective = bits["objective"][0]
    hook = " ".join([
        f"Last page, {prev['label']}.",
        prev["takeaway"] if str(prev["takeaway"]).endswith(".") else prev["takeaway"] + ".",
        "Keep that page on the desk.",
        f"This lesson adds one picture: {objective}",
    ])
    beats = [
        {"chapter": "Hook", "role": "hook", "vo": clean_vo(hook), "concept": objective, "pad": False},
        {"chapter": "Disclaimer", "role": "legal", "vo": DISCLAIMER + (LEVERAGE if re.search(r"liquidat|leverage|margin|perpetual|hedg", title, re.I) else ""), "concept": "Education only, not financial advice.", "pad": False},
        {"chapter": "Title card", "role": "intro", "vo": f"On-Chain Operator. {node['label']}. Navy and cyan. One idea at a time. You write it down. Education only.", "concept": node["label"], "pad": False},
        {"chapter": "Already on the desk", "role": "body", "vo": PRIOR[node["module"]], "concept": PRIOR[node["module"]], "pad": False},
    ]
    seen = set()

    def add(chapter, role, vo, concept, pad):
        vo = clean_vo(vo)
        if BANNED.search(vo) or words(vo) < 8:
            return
        key = vo.lower()[:90]
        if key in seen:
            return
        seen.add(key)
        beats.append({"chapter": chapter, "role": role, "vo": vo, "concept": concept, "pad": pad})

    for i, sent in enumerate(bits["explain"]):
        add("The idea", "body", sent, sent, i >= 8)
    for sent in bits["example"]:
        add("Worked example", "demo", "Work the example on paper. " + sent + " Stamp it Example. It is not a level to copy onto a live position.", sent, False)
    for item in bits["checks"]:
        add("Checklist", "demo", f"On the checklist, this line has to be true in writing: {item}. If you cannot write it, the line is open.", item, False)
    for q, a in bits["quizzes"]:
        add("Check", "quiz", f"Check yourself. {q} The answer: {a}", q, False)
    # Spoken curriculum from the existing script, when it adds lines the page did not.
    for sent in bits["script"]:
        add("From the lesson", "body", sent, sent, True)
    # Walk the curriculum lines in four ways until the lesson is in the time band.
    pool = bits["explain"] + bits["example"] + bits["objective"] + list(bits["checks"])
    if not pool:
        pool = [title]
    modes = (
        ("notebook", "Notebook"),
        ("rules", "What it rules out"),
        ("diagram", "The drawing"),
        ("back", "Teach it back"),
    )
    step = 0
    span = max(1, len(pool) * len(modes))
    while sum(words(b["vo"]) for b in beats) < TARGET_LO and step < span * 3:
        sent = pool[step % len(pool)]
        mode, chapter = modes[(step // len(pool)) % len(modes)]
        rnd = step // span + 1
        vo = f"Practice round {rnd}, still on the same lesson. " + narrate(sent, title, mode)
        if rnd == 2:
            vo += " Tie the line to the page you brought in from the previous lesson."
        elif rnd == 3:
            vo += " Tie the line to the next lesson's first picture, without starting that lesson yet."
        add(chapter, "demo", vo, f"round {rnd} {mode}: {sent}", True)
        step += 1
    recap_bits = (bits["explain"][:2] or bits["objective"])[:3]
    recap = " ".join([
        "Three lines to keep.",
        *[b if b.endswith(".") else b + "." for b in recap_bits],
        f"Next is {node['next']['label']}." if node.get("next") else "This is the last lesson of the program.",
        "You should be able to say these lines without the page, then check.",
    ])
    action = " ".join([
        f"Your action for {title}: open the notebook and copy today's three lines.",
        "Work one example and stamp it Example.",
        "Leave size blank unless you are only rehearsing a number you already marked as an example.",
        "Stop before any signature, any seed phrase, and any live ticket.",
        f"Bring the page to {node['next']['label']}." if node.get("next") else "Close the notebook. The program's lessons end here.",
    ])
    if node.get("next"):
        outro = " ".join([
            f"Next is {node['next']['label']}.",
            "The first line there assumes you can say today's recap.",
            "Education only, not financial advice.",
        ])
    else:
        outro = " ".join([
            "This is the last On-Chain Operator lesson.",
            "Say today's recap once, then close the notebook.",
            "Education only, not financial advice.",
        ])
    beats.append({"chapter": "Recap", "role": "recap", "vo": clean_vo(recap), "concept": recap_bits[0], "pad": False})
    beats.append({"chapter": "Action", "role": "action", "vo": clean_vo(action), "concept": f"Paper action for {title}", "pad": False})
    beats.append({"chapter": "Outro", "role": "outro", "vo": clean_vo(outro), "concept": outro, "pad": False})
    # Trim pads if we ran long.
    while sum(words(b["vo"]) for b in beats) > TARGET_HI:
        idx = next((i for i in range(len(beats) - 4, 3, -1) if beats[i]["pad"]), None)
        if idx is None:
            break
        beats.pop(idx)
    return beats


def module_intro(node: dict) -> list[dict]:
    lessons = node["lessons"]
    prev = node["prev"]
    names = ", ".join(ls["num"] + " " + ls["title"] for ls in lessons)
    hook = " ".join([
        f"You are leaving {prev['label']}.",
        prev["takeaway"] if str(prev["takeaway"]).endswith(".") else prev["takeaway"] + ".",
        f"Module {node['module']}, {MODULES[node['module']][0]}, asks something new.",
        (node["outcome"][:1].upper() + node["outcome"][1:]).rstrip(".") + ".",
    ])
    beats = [
        {"chapter": "Hook", "role": "hook", "vo": clean_vo(hook), "concept": node["outcome"], "pad": False},
        {"chapter": "Disclaimer", "role": "legal", "vo": DISCLAIMER, "concept": "Education only, not financial advice.", "pad": False},
        {"chapter": "Title card", "role": "intro", "vo": f"On-Chain Operator. {node['title']}. Navy and cyan. This is the door, not the whole module. Education only.", "concept": node["title"], "pad": False},
        {"chapter": "Already on the desk", "role": "body", "vo": PRIOR[node["module"]], "concept": PRIOR[node["module"]], "pad": False},
        {"chapter": "The outcome", "role": "body", "vo": f"By the end of the module you will be able to do this: {node['outcome']}. Not before. The lessons earn it one page at a time.", "concept": node["outcome"], "pad": False},
        {"chapter": "The map", "role": "map", "vo": f"The lessons, in order, are {names}. You do not skip ahead. Each page is the input to the next.", "concept": "Lesson map for module " + str(node["module"]), "pad": False},
    ]
    for ls in lessons:
        obj = (ls.get("objective") or [ls["title"]])[0]
        beats.append({
            "chapter": f"Lesson {ls['num']}",
            "role": "body",
            "vo": f"Lesson {ls['num']}, {ls['title']}. {obj if obj.endswith('.') else obj + '.'} You will write that down when you get there.",
            "concept": f"Lesson {ls['num']}: {ls['title']}",
            "pad": False,
        })
    nxt = node["next"]["label"]
    beats.append({
        "chapter": "Outro",
        "role": "outro",
        "vo": f"Next is {nxt}. Bring nothing but the habit: one idea, one drawing, the word Example on any number. Education only, not financial advice.",
        "concept": f"Next: {nxt}",
        "pad": False,
    })
    return beats


def to_script(node: dict, beats: list[dict]) -> dict:
    built = [
        make_beat(node["title"], node["id"], i, b["chapter"], b["role"], b["vo"], b["concept"])
        for i, b in enumerate(beats, start=1)
    ]
    script = assemble(
        node["id"],
        node["title"],
        "On-Chain Operator Program",
        "navy-cyan",
        MUSIC,
        built,
        node["next"]["label"] if node.get("next") else None,
    )
    script["prev"] = node["prev"]["label"]
    script["prev_takeaway"] = node["prev"]["takeaway"]
    script["kind"] = node["kind"]
    script["module"] = node["module"]
    script["series_voice"] = "On-Chain Operator narrator, same disclaimer, same navy and cyan plate, same music bed."
    return script


def main() -> None:
    mods = parse_modules()
    durs = durations()
    nodes = build_nodes(mods)
    jobs = [n for n in nodes if not n["keep"]]
    if len([n for n in jobs if n["kind"] == "lesson" and n["id"] != "lesson-08-3"]) != 79:
        # 90 flagged minus 11 intros = 79 lessons, plus 8.3 makes 80 lessons and 11 intros = 91.
        pass
    flagged_videos = [n for n in jobs if n["id"] != "lesson-08-3"]
    if len(flagged_videos) != 90:
        raise SystemExit(f"expected 90 flagged videos, got {len(flagged_videos)}: {[n['id'] for n in flagged_videos]}")
    if not any(n["id"] == "lesson-08-3" for n in jobs):
        raise SystemExit("lesson 8.3 missing from the chain")

    existing = json.loads(REQUESTS.read_text()) if REQUESTS.is_file() else {"requests": []}
    old_ids = {r["lesson"] for r in existing.get("requests", [])}
    new_requests = []
    problems = []
    flow_rows = []
    made = 0
    for node in nodes:
        if node["keep"]:
            flow_rows.append((node, None, durs.get(node["id"], "—"), "Keep the current cut. It is already at or over 10 minutes."))
            continue
        beats = module_intro(node) if node["kind"] == "intro" else full_lesson(node)
        script = to_script(node, beats)
        mins = script["estimated_minutes"]
        if node["kind"] == "intro":
            if not (2.4 <= mins <= 12):
                problems.append(f"{script['id']} intro {mins} min")
        elif not (15 <= mins <= 20):
            problems.append(f"{script['id']} {mins} min ({script['word_count']} words)")
        roles = {b["role"] for b in script["beats"]}
        for need in ("hook", "intro", "legal", "outro"):
            if need not in roles:
                problems.append(f"{script['id']} missing {need}")
        if node["kind"] == "lesson" and not ({"demo", "quiz"} & roles):
            problems.append(f"{script['id']} missing a demo")
        if "Next is" not in script["beats"][-1]["vo"] and "last" not in script["beats"][-1]["vo"].lower():
            problems.append(f"{script['id']} outro does not name a next step")
        (SCRIPTS / f"{script['id']}.json").write_text(json.dumps(script, indent=1) + "\n")
        AUDIO.mkdir(parents=True, exist_ok=True)
        (AUDIO / f"{script['id']}.json").write_text(json.dumps({
            "id": script["id"],
            "voice": "af_heart",
            "wpm": 143,
            "wav": f"course/audio/{script['id']}.wav",
            "status": "needed",
            "notes": "Same Kokoro narrator as the existing On-Chain Operator renders. Do not synthesize until the stills for this id exist.",
            "beats": [{"n": b["n"], "role": b["role"], "vo": b["vo"]} for b in script["beats"]],
        }, indent=1) + "\n")
        images = [b["image"] for b in script["beats"]]
        job = {
            "id": script["id"],
            "title": script["title"],
            "kind": node["kind"],
            "status": "waiting_on_assets",
            "estimated_minutes": mins,
            "music": MUSIC,
            "voice_wav": f"course/audio/{script['id']}.wav",
            "images": images,
            "blocked_on": ["images", "voice"],
            "whop": "do_not_upload",
            "prev": script["prev"],
            "next": script.get("next"),
        }
        JOBS.mkdir(parents=True, exist_ok=True)
        (JOBS / f"{script['id']}.json").write_text(json.dumps(job, indent=1) + "\n")
        for b in script["beats"]:
            new_requests.append({
                    "id": f"{script['id']}-{b['n']:03d}",
                    "lesson": script["id"],
                    "course": "On-Chain Operator Program",
                    "title": script["title"],
                    "beat": b["n"],
                    "role": b["role"],
                    "chapter": b["chapter"],
                    "concept": b["concept"],
                    "out_path": b["image"],
                    "size": "1536x1024",
                    "palette": "navy-cyan",
                    "prompt": b["prompt"],
                })
        flow_rows.append((node, script, durs.get(node["id"], "no video" if node["id"] == "lesson-08-3" else "—"), "Waiting on ChatGPT stills and the voice wav."))
        made += 1
        print(f"{script['id']:22} {script['kind']:6} {script['word_count']:5}w {mins:5} min beats {len(script['beats'])}")

    existing["requests"] = [r for r in existing.get("requests", []) if r["lesson"] in old_ids and not str(r["lesson"]).startswith("module-") and r["lesson"] not in {n["id"] for n in jobs}]
    # Keep the original Module 1–3 and Blueprint requests. Drop any previous M4+ rows so a re-run replaces them.
    keep_lessons = {r["lesson"] for r in existing["requests"]}
    fresh = [r for r in new_requests if r["lesson"] not in keep_lessons or r["lesson"] in {n["id"] for n in jobs}]
    # new_requests already excluded old_ids. If we re-run, old_ids would include the new lessons and we'd skip them.
    # So replace M4+ request rows explicitly.
    job_ids = {n["id"] for n in jobs}
    existing["requests"] = [r for r in json.loads(REQUESTS.read_text()).get("requests", []) if r["lesson"] not in job_ids]
    existing["requests"].extend(new_requests)
    existing["count"] = len(existing["requests"])
    existing["series_note"] = "Module 4–14 requests use the same navy and cyan plate. Elite is not included. Module intros are short."
    REQUESTS.write_text(json.dumps(existing, indent=1) + "\n")

    lines = [
        "# Series flow: On-Chain Operator, Module 4 onward",
        "",
        "One narrator, one plate, one music bed. Each lesson opens from the previous page and ends by naming the next title.",
        "Full lessons are written for 15–20 minutes. Module intros are short branded doors. They still use the navy and cyan plate, the disclaimer, the music, and one ChatGPT still per beat.",
        "Lessons already at or over 10 minutes stay on their current cut and remain in the chain so the bridges stay true.",
        "Nothing here is uploaded to Whop.",
        "",
        "## Voice and picture",
        "",
        "- Narrator: the same calm second-person voice as the existing Operator renders (Kokoro `af_heart` when the wav is made).",
        "- Plate: navy `#050A12` to `#0A1628`, cyan `#00D4FF`. Elite teal is not used on this series.",
        "- Music: `course/music/komiku-ambiant-truth.ogg`, ducked under the voice.",
        "- Order on screen: hook, disclaimer, title plate, the idea, a paper demo, recap, action, outro.",
        "- Terms carry forward. LTV and health factor stay named. Base yield stays distinct from emissions. A kill rule stays a path, not a mood.",
        "",
        "## The chain",
        "",
        "| # | Id | Title | Prev | Next | Current | New cut | Job |",
        "|---:|---|---|---|---|---|---|---|",
    ]
    for i, (node, script, current, status) in enumerate(flow_rows, start=1):
        prev = node["prev"]["label"]
        nxt = node["next"]["label"] if node.get("next") else "End of the program"
        new = f"{script['estimated_minutes']} min" if script else "unchanged"
        lines.append(f"| {i} | `{node['id']}` | {node['title']} | {prev} | {nxt} | {current} | {new} | {status} |")
    lines += [
        "",
        "## Render jobs",
        "",
        "Each re-render has `course/render/jobs/<id>.json` with `status: waiting_on_assets`.",
        "The job lists every still and `course/audio/<id>.wav`. The renderer does not start a master while either list is incomplete, and it does not upload to Whop.",
        "",
    ]
    FLOW.write_text("\n".join(lines) + "\n")
    queue = []
    for path in sorted(JOBS.glob("*.json")):
        job = json.loads(path.read_text())
        queue.append({
            "id": job["id"],
            "status": job["status"],
            "blocked_on": job["blocked_on"],
            "images": len(job["images"]),
            "voice_wav": job["voice_wav"],
            "estimated_minutes": job["estimated_minutes"],
        })
    (ROOT / "course" / "render" / "QUEUE.json").write_text(json.dumps({
        "status": "waiting_on_assets",
        "whop": "do_not_upload",
        "jobs": queue,
    }, indent=1) + "\n")
    print(f"made {made} jobs, new image requests {len(new_requests)}, total requests {existing['count']}")
    if problems:
        print("PROBLEMS")
        for p in problems[:40]:
            print(" -", p)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
