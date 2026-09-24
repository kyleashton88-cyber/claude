#!/usr/bin/env python3
"""Turn every lesson (and Mastery Starter) into a narrated video script.

Reads lessons/module-*.md (+ the sample lesson 2.2 and strategy lesson 8.3),
writes one scene script per lesson to video-scripts/lessons/<id>.json in the
same schema build_video.js renders, and writes 10-video-production-plan.md.

Usage: python3 export/build_lesson_scripts.py
Render: cd export && node build_video.js lesson-01-3   (one)  |  node build_video.js lessons  (all)
"""
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUT = ROOT / "video-scripts" / "lessons"
GOLD = ROOT / "video-scripts" / "gold"   # hand-written scripts; the generator never touches these
WPM = 150            # narration pace (words per minute)
MAX_MIN = 25         # hard cap per video
NUM = "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen".split()

SAY = [  # written form -> spoken form (narration only; captions keep the written form)
    (r"\bAPY\b", "A.P.Y."), (r"\bAPR\b", "A.P.R."), (r"\bLTV\b", "L.T.V."), (r"\bHF\b", "health factor"),
    (r"\bLPs\b", "L.P.s"), (r"\bLP\b", "L.P."), (r"\bLSTs?\b", "liquid staking token"), (r"\bKYC\b", "K.Y.C."),
    (r"\b2FA\b", "two-factor"), (r"\bL2s\b", "layer twos"), (r"\bL2\b", "layer two"), (r"\bUSDC\b", "U.S.D.C."),
    (r"\bUSDT\b", "U.S.D.T."), (r"\bBTC\b", "bitcoin"), (r"\bDEXs\b", "decks"), (r"\bDEX\b", "decks"),
    (r"\bMEV\b", "M.E.V."), (r"\bTVL\b", "T.V.L."), (r"\bFDV\b", "F.D.V."), (r"\bTWAP\b", "T-wap"),
    (r"\bCDP\b", "C.D.P."), (r"\bPSM\b", "P.S.M."), (r"\bLVR\b", "L.V.R."), (r"\bVaR\b", "value at risk"),
    (r"\bTWR\b", "time-weighted return"), (r"\bRWAs?\b", "real-world asset"), (r"\bPT\b", "P.T."), (r"\bYT\b", "Y.T."),
    (r"\bMPC\b", "M.P.C."), (r"\bRPC\b", "R.P.C."), (r"\bOI\b", "open interest"), (r"\bIL\b", "impermanent loss"),
    (r"e\.g\.", "for example"), (r"i\.e\.", "that is"), (r"\bvs\.?\b", "versus"), (r"/yr\b", " a year"),
    (r"/month\b", " a month"), (r"/day\b", " a day"), ("→", " to "), ("×", " times "), ("≈", "about "),
    ("÷", " divided by "), ("–", " to "), ("≥", "at least "), ("≤", "at most "), ("−", "minus "), (r"(\w)\s*·\s*(\w)", r"\1 times \2"), ("·", ","), (r"(?<=\w)\s*=\s*(?=\w)", " equals "), (r"(?<=squared)\s*/\s*(?=\d)", " divided by "), (r"(?<=\))\s*/\s*(?=\d)", " divided by "), (r"(?<=\d)/(?=\d)", " to "), (" / ", " or "), ("≈", "comes to about "), ("σ", "sigma"),
    ("²", " squared"), ("√", "the square root of "), ("~", "about "), ("&", " and "),
]


def plain(md):
    """Markdown -> readable caption text."""
    t = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", md)
    t = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", t)
    t = re.sub(r"<[^>]+>", "", t)
    t = re.sub(r"`([^`]*)`", r"\1", t)
    t = t.replace("**", "").replace("*", "")
    t = re.sub(r"defi_calc\.py [^→;\n]*?→\s*", "the calculator gives ", t)
    t = re.sub(r"defi_calc\.py [^→;]*?(?=→|;|$)", "the calculator ", t, flags=re.M)
    t = re.sub(r"^\s*[-*]\s+(\[[ x]\]\s*)?", "", t, flags=re.M)
    return re.sub(r"\s+", " ", t).strip()


def spoken(md):
    t = plain(md)
    t = re.sub(r"defi_calc\.py [^.;]*", "the calculator", t)
    for a, b in SAY:
        t = re.sub(a, b, t) if a.startswith("\\") or a.startswith("(") or "\\" in a else t.replace(a, b)
    t = re.sub(r"(?<!\.)\.\.(?!\.)", ".", t)
    return re.sub(r"\s+", " ", t).strip()


def short(text, n=90):
    text = plain(text)
    m = re.match(r"(.+?)(?: — |: |(?<!e\.g)(?<!i\.e)\. )", text)
    head = m.group(1) if m and len(m.group(1)) <= n else text
    return head if len(head) <= n else head[: n - 1].rsplit(" ", 1)[0] + "…"


def blocks(section):
    """Split a lesson section into (heading, body) by ### headings."""
    parts = re.split(r"^### (.+)$", section, flags=re.M)
    out = [("_intro", parts[0])]
    out += [(parts[i].strip(), parts[i + 1]) for i in range(1, len(parts), 2)]
    return out


def bullet_items(body):
    items = re.findall(r"^\s*(?:[-*]|\d+\.)\s+(.+)$", body, flags=re.M)
    return [re.sub(r"^\[[ x]\]\s*", "", b.strip()) for b in items]


def table_rows(body):
    rows = [r for r in body.splitlines() if r.startswith("|") and not re.match(r"^\|[-\s|]+\|$", r)]
    return [[c.strip() for c in r.strip("|").split("|")] for r in rows[1:]]  # skip header


def images(body):
    return re.findall(r"!\[([^\]]*)\]\(([^)]+)\)", body)


MODULE_TITLES = {}
TRANSITIONS = ["First,", "Next,", "Then,", "Also,", "On top of that,", "And", "Plus,", "One more:"]


def say_num(lid):
    a, b = (int(x) for x in lid.split("."))
    return f"{NUM[a]} point {NUM[b] if b < 15 else b}"


def objective_of(body):
    m = re.search(r"^### (?:Objective|The 60-second version)\n(.+?)(?=\n###|\Z)", body, flags=re.M | re.S)
    return plain(m.group(1)) if m else ""


def thumb_title(title):
    t = re.split(r"[:—(]", plain(title))[0].strip()
    words = t.split()
    return " ".join(words[:5]) + ("…" if len(words) > 5 else "")


def quiz_scenes(text):
    qa = re.findall(r"<summary>(.*?)</summary>\s*(.*?)</details>", text, flags=re.S)
    out = []
    for i, (q, a) in enumerate(qa):
        q = re.sub(r"^\d+\.\s*", "", q.strip())
        word = NUM[i + 1] if i + 1 < len(NUM) else str(i + 1)
        out.append({"type": "quiz", "chapter": "Quiz", "n": i + 1, "of": len(qa), "q": plain(q), "a": plain(a),
                    "vo": f"Question {word}. {spoken(q)} [[pause 4]] The answer: {spoken(a)}",
                    "cap": f"Question {i + 1}. {plain(q)} The answer: {plain(a)}"})
    return out


LOWER_OK = set("a an the it its this that these those you your money each every no one there when if most some all any many what how why who once never always only in on at to for with by from after before most more less not keep use check set".split())


def lower_first(x):
    w = x.split(" ", 1)[0]
    return x[0].lower() + x[1:] if w.lower() in LOWER_OK and not w.isupper() else x


def recap_line(x):
    t = plain(x)
    parts = re.split(r" — |: |(?<!e\.g)(?<!i\.e)\. |; ", t)
    head = parts[0].strip().rstrip(".")
    if len(head) < 32 and len(parts) > 1:           # "Name: what it is" keeps its definition
        head = f"{head}: {parts[1].strip().rstrip('.')}"
    if len(head) > 100:
        cut = head[:100].rfind(",")
        head = head[:cut] if cut > 40 else head
    return head


def row_speech(r, say=True):
    f = spoken if say else plain
    if len(r) == 2:
        return f"{f(r[0])}: {lower_first(f(r[1]))}"
    return f(", ".join(r))


def taught_items(items, chapter, title, intro="", check=True, numbered=False):
    """Bullet scenes that narrate each item with a transition, so the highlight follows the voice."""
    scenes = []
    for i in range(0, len(items), 5):
        chunk = items[i:i + 5]
        vo, cap = [], []
        if i == 0 and intro:
            vo.append(spoken(intro)); cap.append(plain(intro))
        for j, x in enumerate(chunk):
            k = i + j
            lead = "" if not numbered and len(items) == 1 else (TRANSITIONS[min(k, len(TRANSITIONS) - 1)] if k < len(items) - 1 or k == 0 else "And finally,")
            sx, px = spoken(x), plain(x)
            vo.append(f"{lead} {lower_first(sx) if lead else sx}".strip() + ("" if sx.endswith((".", "?", "!")) else "."))
            cap.append(f"{lead} {lower_first(px) if lead else px}".strip() + ("" if px.endswith((".", "?", "!")) else "."))
        sc = {"type": "bullets", "chapter": chapter, "title": title if i == 0 else f"{title} (cont.)", "items": [short(x) for x in chunk],
              "vo": " ".join(vo), "cap": " ".join(cap)}
        if not check:
            sc["check"] = False
        if numbered:
            sc["numbered"] = True
        scenes.append(sc)
    return scenes


def scenes_for(lesson_id, title, body, module_num, next_lesson=None):
    starter = lesson_id.endswith(".0")
    objective = objective_of(body)
    mt = MODULE_TITLES.get(module_num, "")
    if starter:
        hook_vo = f"Mastery Starter {say_num(lesson_id)}. New to {spoken(mt)}? Start here. In about ten minutes, you'll go from zero to ready for this module."
        hook_cap = f"Mastery Starter {lesson_id}. New to {mt}? Start here. In about ten minutes, you'll go from zero to ready for this module."
    else:
        obj = objective.rstrip(".")
        hook_vo = f"Lesson {say_num(lesson_id)}. {spoken(title)}. " + (f"By the end of this lesson, you'll be able to {spoken(obj)[0].lower() + spoken(obj)[1:]}." if obj else "")
        hook_cap = f"Lesson {lesson_id}. {plain(title)}. " + (f"By the end of this lesson, you'll be able to {obj[0].lower() + obj[1:]}." if obj else "")
    scenes = [{"type": "title", "chapter": "Intro", "eyebrow": f"Module {module_num} · {mt}", "num": lesson_id,
               "title": "Mastery Starter" if starter else plain(title), "sub": objective[:200], "vo": hook_vo.strip(), "cap": hook_cap.strip()}]
    heads = [h.lower() for h, _ in blocks(body)]
    plan = [x for x, k in (("Key ideas", "explanation"), ("Worked example", "worked example"), ("Checklist", "checklist"), ("Quiz", "quiz")) if any(h.startswith(k) for h in heads)]
    PLAN_SAY = {"Key ideas": "the key ideas", "Worked example": "a worked example, step by step", "Checklist": "your checklist", "Quiz": "a three-question quiz"}
    plan_line = "Here's the plan. " + " ".join((f"{'Then' if i else 'First'}, {PLAN_SAY[x]}." if i < len(plan) - 1 else f"And finally, {PLAN_SAY[x]}.") for i, x in enumerate(plan))
    if len(plan) >= 3 and not starter:
        scenes.append({"type": "bullets", "chapter": "Plan", "title": "The plan", "numbered": True, "items": plan,
                       "vo": plan_line, "cap": plan_line})
    recap = []
    for head, text in blocks(body):
        h = head.lower()
        imgs = images(text)
        text_wo = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", text)
        text_wo = re.sub(r"```.*?```", "", text_wo, flags=re.S)
        text_wo = re.sub(r"^\s*---\s*$", "", text_wo, flags=re.M).strip()
        if h.startswith("you've mastered"):
            text_wo = "You've mastered this module when " + re.sub(r"^[.…\s]+", "", text_wo)
        chapter = {"explanation": "Key ideas", "checklist": "Checklist"}.get(h, "Worked example" if h.startswith("worked example") else plain(head)[:40])
        if head != "_intro" and plain(text_wo) and not h.startswith("quiz"):
            if h.startswith("objective"):
                pass  # already spoken in the hook
            elif h.startswith("the 60-second") or h.startswith("you've mastered") or h.startswith("your first safe step"):
                label = {"the 60-second version": "The 60-second version", "you've mastered this module when…": "You've mastered it when…",
                         "your first safe step": "Your first safe step"}.get(h, plain(head))
                items = bullet_items(text_wo)
                if items:
                    scenes += taught_items(items, label, label)
                else:
                    head_line = recap_line(text_wo)
                    rest = plain(text_wo)[len(head_line):].lstrip(" .:—;")
                    scenes.append({"type": "statement", "chapter": label, "kicker": label, "lines": [head_line + ("." if not rest else "")],
                                   "sub": rest[:260] or None,
                                   "vo": spoken(text_wo), "cap": plain(text_wo)})
            else:
                rows = table_rows(text_wo)
                items = bullet_items(text_wo)
                title_txt = {"explanation": "Key ideas", "checklist": "Checklist"}.get(h, "Worked example" if h.startswith("worked example") else plain(head)[:60])
                intro = plain("\n".join(l for l in text_wo.splitlines() if l.strip() and not l.startswith("|") and not re.match(r"^\s*(?:[-*]|\d+\.)\s", l)))
                if rows:
                    its = [short(" — ".join(r[:2]), 80) for r in rows]
                    for i in range(0, len(its), 6):
                        part = rows[i:i + 6]
                        scenes.append({"type": "bullets", "chapter": chapter, "title": title_txt, "items": its[i:i + 6], "compact": True,
                                       "vo": (spoken(intro) + " " if i == 0 and intro else "") + " ".join(row_speech(r).rstrip(".") + "." for r in part),
                                       "cap": (intro + " " if i == 0 and intro else "") + " ".join(row_speech(r, False).rstrip(".") + "." for r in part)})
                elif h.startswith("worked example") and items:
                    steps = [plain(x) for x in items if "defi_calc" not in x]
                    calc = any("defi_calc" in x for x in items)
                    for i in range(0, len(steps), 5):
                        chunk = steps[i:i + 5]
                        vo = ("Let's work an example, step by step. " + (spoken(intro) + " " if intro else "") if i == 0 else "")
                        vo += " ".join(spoken(x) + ("" if x.endswith(".") else ".") for x in chunk)
                        if calc and i + 5 >= len(steps):
                            vo += " You can check every number with the program's calculator."
                        scenes.append({"type": "steps", "chapter": "Worked example", "title": "Worked example" + (f": {short(intro, 50)}" if intro and i == 0 else ""),
                                       "steps": [short(x, 78) for x in chunk], "vo": vo.strip()})
                elif items:
                    if h == "explanation":
                        recap += items[:4]
                    scenes += taught_items(items, chapter, title_txt, intro=intro if h != "checklist" else "Here's your checklist. Do it now, for real.",
                                           numbered=h not in ("checklist",) and h != "explanation" and False)
                elif h.startswith("worked example"):
                    sents = [x for x in re.split(r"(?<=[.!?])\s+(?=[A-Z0-9$(])", plain(text_wo)) if x]
                    scenes.append({"type": "steps", "chapter": "Worked example", "title": "Worked example", "steps": [short(x, 78) for x in sents[:6]],
                                   "vo": "Let's work an example, step by step. " + spoken(text_wo), "cap": "Let's work an example, step by step. " + plain(text_wo)})
                else:
                    scenes.append({"type": "statement", "chapter": chapter, "kicker": title_txt, "lines": [short(text_wo, 60)],
                                   "sub": plain(text_wo)[:240] if len(plain(text_wo)) > 60 else None, "vo": spoken(text_wo), "cap": plain(text_wo)})
        for alt, src in imgs:
            src = src.replace("../assets/", "assets/")
            kind = "chart" if "/charts/" in src else "diagram"
            scenes.append({"type": "image", "chapter": chapter if head != "_intro" else "Key ideas", "src": src, "eyebrow": plain(alt)[:48] or kind.title(), "wide": True,
                           "vo": f"Let's look at the {kind}: {spoken(alt)}. Take a moment with it. It's everything we've just said, in one picture.",
                           "cap": f"Let's look at the {kind}: {plain(alt)}. Take a moment with it. It's everything we've just said, in one picture."})
        if h.startswith("quiz"):
            scenes += quiz_scenes(text)
    for sc in scenes:
        if sc.get("sub") is None:
            sc.pop("sub", None)
    if recap:
        its = [recap_line(x) for x in recap]
        scenes.append({"type": "bullets", "chapter": "Recap", "title": "Recap", "items": its,
                       "vo": "Let's recap. " + " ".join(spoken(x) + "." for x in its),
                       "cap": "Let's recap. " + " ".join(x + "." for x in its)})
    if next_lesson:
        nid, ntitle = next_lesson
        nxt_vo = f" Next up, lesson {say_num(nid)}: {spoken(ntitle)}."
        nxt_cap = f" Next up, Lesson {nid}: {plain(ntitle)}."
        button = f"Next: Lesson {nid}"
    else:
        nxt_vo = nxt_cap = ""
        button = "Do the checklist"
    scenes.append({"type": "cta", "chapter": "Recap" if recap else "Next", "button": button, "sub": "Do the checklist first · Educational content only · Not financial advice",
                   "vo": "Do the checklist now, before you move on." + nxt_vo, "cap": "Do the checklist now, before you move on." + nxt_cap})
    return scenes


def lesson_sections():
    """Yield (lesson_id, title, body, module_num) for every lesson in curriculum order."""
    sample = (ROOT / "02-sample-lesson-amm-math.md").read_text()
    for f in sorted((ROOT / "lessons").glob("module-*.md")):
        mod = int(re.search(r"module-(\d+)", f.name).group(1))
        text = f.read_text()
        parts = re.split(r"^## Lesson (\d+\.\d+) — (.+)$", text, flags=re.M)
        found = [(parts[i], parts[i + 1], parts[i + 2]) for i in range(1, len(parts), 3)]
        if mod == 2:
            body = sample.split("\n", 1)[1].replace("\n## ", "\n### ")
            found.append(("2.2", "AMM Mathematics (x · y = k)", body))
        for lid, title, body in sorted(found, key=lambda x: [int(p) for p in x[0].split(".")]):
            if lid == "8.3":
                continue  # strategy library: its own long-form series (see plan)
            body = body.split("\n### Module")[0]
            yield lid, re.sub(r"\s*\*\(.*?\)\*\s*$", "", title).strip(), body, mod


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    rows = []
    for f in sorted((ROOT / "lessons").glob("module-*.md")):
        n = int(re.search(r"module-(\d+)", f.name).group(1))
        MODULE_TITLES[n] = re.match(r"# Module \d+ — (.+)", f.read_text()).group(1).strip()
    lessons = list(lesson_sections())
    gold = {p.stem for p in GOLD.glob("*.json")}
    for i, (lid, title, body, mod) in enumerate(lessons):
        vid = f"lesson-{lid.split('.')[0].zfill(2)}-{lid.split('.')[1]}"
        nxt = (lessons[i + 1][0], lessons[i + 1][1]) if i + 1 < len(lessons) else None
        if lid == "8.2":
            nxt = ("8.3", "The strategy library")
        if vid in gold:  # hand-written gold-standard script wins; never overwrite it
            (OUT / f"{vid}.json").unlink(missing_ok=True)
            g = json.loads((GOLD / f"{vid}.json").read_text())
            words = sum(len(re.sub(r"\[\[pause [\d.]+\]\]", "", s["vo"]).split()) for s in g["scenes"])
            pauses = sum(float(x) for s in g["scenes"] for x in re.findall(r"\[\[pause ([\d.]+)\]\]", s["vo"]))
            rows.append((lid, title, len(g["scenes"]), words / WPM + (pauses + len(g["scenes"]) * 1.3) / 60, vid, "gold"))
            continue
        scenes = scenes_for(lid, title, body, mod, nxt)
        words = sum(len(re.sub(r"\[\[pause [\d.]+\]\]", "", s["vo"]).split()) for s in scenes)
        pauses = sum(float(x) for s in scenes for x in re.findall(r"\[\[pause ([\d.]+)\]\]", s["vo"]))
        est = words / WPM + (pauses + len(scenes) * 1.3) / 60  # narration + quiz pauses + scene padding
        spec = {"id": vid, "title": f"Lesson {lid}: {title}", "size": [1920, 1080], "group": "lessons", "tag": f"Lesson {lid}",
                "use": f"Lesson {lid} page in the Whop course.", "maxMinutes": MAX_MIN,
                "thumbnail": {"title": "Mastery Starter" if lid.endswith(".0") else thumb_title(title), "subtitle": f"Lesson {lid}" if not lid.endswith(".0") else f"Module {mod} · Start here"},
                "scenes": scenes}
        assert est <= MAX_MIN, f"{vid} estimated {est:.1f} min > {MAX_MIN}"
        (OUT / f"{vid}.json").write_text(json.dumps(spec, indent=1, ensure_ascii=False))
        rows.append((lid, title, len(scenes), est, vid, "auto"))
    # 8.3 strategy library as a series of long-form videos (one per level) is scripted by hand/AI; listed in the plan.
    total = sum(r[3] for r in rows)
    rendered = {p.stem for p in (ROOT / "video").glob("lesson-*.mp4")}
    md = [f"""# On-Chain Operator Program — Course Video Production Plan

*Generated by `export/build_lesson_scripts.py` from the lesson files. Edit lessons, then re-run.*

## The rule
**Every lesson and every Mastery Starter gets its own narrated video, each at most {MAX_MIN} minutes.**
Baseline scripts run about 3–7 minutes; rewritten gold scripts target 5–25 minutes. Nothing may exceed {MAX_MIN} minutes (split into Part 1 / Part 2 if it would).

## What exists
| Video type | Count | Where | Status |
|---|---|---|---|
| VSL (main ≈3.5 min + 40s vertical) | 2 | `video/vsl-*.mp4` | Rendered |
| Welcome | 1 | `video/welcome.mp4` | Rendered |
| Module intros | 15 | `video/module-NN-intro.mp4` | Rendered |
| **Lesson videos (incl. Mastery Starters)** | **{len(rows)}** | `video-scripts/lessons/*.json` + `video-scripts/gold/*.json` → `video/lesson-*.mp4` | Scripts ready (Lesson 3.2 gold standard); {len(rendered)} rendered |
| Strategy library series (8.3) | 7 (one per level) | to be scripted (see prompt) | To do |

Estimated total runtime of lesson videos from the baseline scripts: **{total / 60:.1f} hours**.

## The quality bar
`video-scripts/gold/lesson-03-2.json` (Lesson 3.2) is hand-written to the finished standard and rendered as
`video/lesson-03-2.mp4`. Every lesson video is rewritten to that standard (see `BUILD-PROMPT.md`, item 2) and
saved in `video-scripts/gold/`; the generator skips any lesson with a gold script.

## Video structure (every lesson)
1. Title card: lesson number, title, objective (chapter "Intro")
2. The plan: key ideas → worked example → checklist → quiz
3. Key ideas: one scene per group of points, each point narrated with a transition and highlighted as it's spoken
4. Every diagram and chart from the lesson, full-screen with a wipe reveal
5. Worked example as numbered steps, each revealed as it's spoken
6. Checklist read aloud
7. Quiz: question → 4-second thinking timer → answer
8. Recap, then "Next up: Lesson N.M"

Voice: Kokoro TTS (`af_heart`), sentence by sentence with measured pauses, mastered to −16 LUFS. Motion: captions
highlight word by word, living network background, progress bar and chapter tag. Each render also writes a
thumbnail (`video/thumbs/`), WebVTT captions (`video/captions/`) and a chapter list (`video/chapters/`).

## How to render
```
cd programs/defi-program/export
npm install
python3 build_lesson_scripts.py          # regenerate scripts from lessons
node build_video.js lesson-01-3          # one lesson
node build_video.js lessons              # all lessons (several hours of rendering)
```

## Every lesson video
| Lesson | Title | Scenes | Est. length | Script | Rendered |
|---|---|---|---|---|---|
"""]
    for lid, title, n, est, vid, kind in rows:
        folder = "gold" if kind == "gold" else "lessons"
        md.append(f"| {lid} | {title}{' **(gold standard)**' if kind == 'gold' else ''} | {n} | {est:.1f} min | `video-scripts/{folder}/{vid}.json` | {'✓' if vid in rendered else ''} |\n")
    (ROOT / "10-video-production-plan.md").write_text("".join(md))
    print(f"{len(rows)} lesson scripts, est. {total / 60:.1f} h total, longest {max(r[3] for r in rows):.1f} min")


if __name__ == "__main__":
    main()
