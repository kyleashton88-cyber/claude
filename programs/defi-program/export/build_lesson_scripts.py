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
    ("÷", " divided by "), ("≥", "at least "), ("≤", "at most "), ("−", "minus "), ("·", ","), ("σ", "sigma"),
    ("²", " squared"), ("√", "the square root of "), ("~", "about "), ("&", " and "),
]


def plain(md):
    """Markdown -> readable caption text."""
    t = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", md)
    t = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", t)
    t = re.sub(r"<[^>]+>", "", t)
    t = re.sub(r"`([^`]*)`", r"\1", t)
    t = t.replace("**", "").replace("*", "")
    t = re.sub(r"defi_calc\.py [^→;]*?(?=→|;|$)", "the calculator ", t, flags=re.M)
    t = re.sub(r"^\s*[-*]\s+(\[[ x]\]\s*)?", "", t, flags=re.M)
    return re.sub(r"\s+", " ", t).strip()


def spoken(md):
    t = plain(md)
    t = re.sub(r"defi_calc\.py [^.;]*", "the calculator", t)
    for a, b in SAY:
        t = re.sub(a, b, t) if a.startswith("\\") or a.startswith("(") or "\\" in a else t.replace(a, b)
    return re.sub(r"\s+", " ", t).strip()


def short(text, n=90):
    text = plain(text)
    m = re.match(r"(.+?)(?: — |: )", text)
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


def scenes_for(lesson_id, title, body, module_num):
    n = int(lesson_id.split(".")[0])
    spoken_id = f"{NUM[n]} point {NUM[int(lesson_id.split('.')[1])]}" if int(lesson_id.split(".")[1]) < 15 else lesson_id
    scenes = [{"type": "image", "src": f"assets/modules/module-{module_num:02d}.png", "eyebrow": f"Lesson {lesson_id}",
               "vo": f"Lesson {spoken_id}. {spoken(title)}.", "cap": f"Lesson {lesson_id}. {plain(title)}."}]
    for head, text in blocks(body):
        h = head.lower()
        imgs = images(text)
        for alt, src in imgs:
            src = src.replace("../assets/", "assets/")
            scenes.append({"type": "image", "src": src, "eyebrow": plain(alt)[:40] or "Diagram",
                           "vo": f"Here's the picture: {spoken(alt)}.", "cap": f"{plain(alt)}."})
        text_wo = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", text)
        text_wo = re.sub(r"```.*?```", "", text_wo, flags=re.S)
        if head == "_intro" or not plain(text_wo):
            continue
        if h.startswith("quiz"):
            for q, a in re.findall(r"<summary>(.*?)</summary>\s*(.*?)</details>", text, flags=re.S):
                q = re.sub(r"^\d+\.\s*", "", q.strip())
                scenes.append({"type": "statement", "lines": ["Quiz", plain(q)], "sub": "Answer: " + plain(a), "subAt": 0.62,
                               "vo": f"{spoken(q)} ... Pause and think. ... The answer: {spoken(a)}",
                               "cap": f"{plain(q)} Pause and think. The answer: {plain(a)}"})
            continue
        if h.startswith("objective") or h.startswith("the 60-second") or h.startswith("you've mastered") or h.startswith("your first safe step"):
            label = {"objective": "Objective", "the 60-second version": "The 60-second version",
                     "you've mastered this module when…": "You've mastered it when…", "your first safe step": "Your first safe step"}.get(h, head)
            scenes.append({"type": "statement", "lines": [label], "sub": plain(text_wo)[:260],
                           "vo": spoken(text_wo), "cap": plain(text_wo)})
            continue
        rows = table_rows(text_wo)
        items = bullet_items(text_wo)
        title_txt = {"explanation": "Key ideas", "checklist": "Checklist", "worked example": "Worked example"}.get(h, plain(head)[:60])
        if rows:
            its = [short(" — ".join(r[:2]), 80) for r in rows]
            vo = " ".join(spoken(", ".join(r)) + "." for r in rows)
            for i in range(0, len(its), 6):
                scenes.append({"type": "bullets", "title": title_txt, "items": its[i:i + 6], "compact": True,
                               "vo": vo if i == 0 else "…", "cap": plain(" ".join(", ".join(r) for r in rows[i:i + 6]))})
            rest = "\n".join(l for l in text_wo.splitlines() if not l.startswith("|"))
            if plain(rest):
                scenes.append({"type": "statement", "lines": [title_txt], "sub": plain(rest)[:260], "vo": spoken(rest), "cap": plain(rest)})
            continue
        if items:
            intro = plain("\n".join(l for l in text_wo.splitlines() if l.strip() and not re.match(r"^\s*(?:[-*]|\d+\.)\s", l)))
            vo_prefix = "Your checklist. " if h == "checklist" else (spoken(intro) + " " if intro else "")
            for i in range(0, len(items), 5):
                chunk = items[i:i + 5]
                scenes.append({"type": "bullets", "title": title_txt, "items": [short(x) for x in chunk],
                               "vo": (vo_prefix if i == 0 else "") + " ".join(spoken(x) for x in chunk),
                               "cap": plain(" ".join(chunk))})
            continue
        scenes.append({"type": "statement", "lines": [title_txt], "sub": plain(text_wo)[:260],
                       "vo": spoken(text_wo), "cap": plain(text_wo)})
    # drop "…" placeholder narration from split tables (merge into previous scene)
    for s in scenes:
        if s.get("vo") == "…":
            s["vo"] = "Continuing."
    scenes.append({"type": "cta", "button": "Do the checklist", "sub": "Educational content only · Not financial advice",
                   "vo": "Now do the checklist before moving on. See you in the next lesson.", "cap": "Now do the checklist before moving on."})
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
            body = sample.split("\n", 1)[1]
            found.append(("2.2", "AMM Mathematics (x · y = k)", body))
        for lid, title, body in sorted(found, key=lambda x: [int(p) for p in x[0].split(".")]):
            if lid == "8.3":
                continue  # strategy library: its own long-form series (see plan)
            body = body.split("\n### Module")[0]
            yield lid, re.sub(r"\s*\*\(.*?\)\*\s*$", "", title).strip(), body, mod


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    rows = []
    for lid, title, body, mod in lesson_sections():
        scenes = scenes_for(lid, title, body, mod)
        words = sum(len(s["vo"].split()) for s in scenes)
        est = words / WPM + len(scenes) * 1.05 / 60  # narration + scene padding
        vid = f"lesson-{lid.split('.')[0].zfill(2)}-{lid.split('.')[1]}"
        spec = {"id": vid, "title": f"Lesson {lid}: {title}", "size": [1920, 1080], "group": "lessons",
                "use": f"Lesson {lid} page in the Whop course.", "maxMinutes": MAX_MIN, "scenes": scenes}
        assert est <= MAX_MIN, f"{vid} estimated {est:.1f} min > {MAX_MIN}"
        (OUT / f"{vid}.json").write_text(json.dumps(spec, indent=1, ensure_ascii=False))
        rows.append((lid, title, len(scenes), est, vid))
    # 8.3 strategy library as a series of long-form videos (one per level) is scripted by hand/AI; listed in the plan.
    total = sum(r[3] for r in rows)
    rendered = {p.stem for p in (ROOT / "video").glob("lesson-*.mp4")}
    md = [f"""# On-Chain Operator Program — Course Video Production Plan

*Generated by `export/build_lesson_scripts.py` from the lesson files. Edit lessons, then re-run.*

## The rule
**Every lesson and every Mastery Starter gets its own narrated video, each at most {MAX_MIN} minutes.**
Typical length is 3–12 minutes; nothing may exceed {MAX_MIN} minutes (split into Part 1 / Part 2 if it would).

## What exists
| Video type | Count | Where | Status |
|---|---|---|---|
| VSL (main + vertical) | 2 | `video/vsl-*.mp4` | Rendered |
| Welcome | 1 | `video/welcome.mp4` | Rendered |
| Module intros | 15 | `video/module-NN-intro.mp4` | Rendered |
| **Lesson videos (incl. Mastery Starters)** | **{len(rows)}** | `video-scripts/lessons/*.json` → `video/lesson-*.mp4` | Scripts ready; {len(rendered)} rendered as samples |
| Strategy library series (8.3) | 7 (one per level) | to be scripted (see prompt) | To do |

Estimated total runtime of lesson videos from the baseline scripts: **{total / 60:.1f} hours**.

## Video structure (every lesson)
1. Title card: module banner + "Lesson N.M" + title
2. Objective (or, for Mastery Starters, the 60-second version)
3. Key ideas: one scene per group of points, narrated in full
4. Every diagram and chart from the lesson, shown full-screen and explained
5. Worked example, step by step, with the numbers on screen
6. Checklist read aloud
7. Quiz: question → pause → answer
8. Outro: "Do the checklist before moving on"

Brand: the same dark navy system, logo, captions burned in (most people watch muted),
disclaimer footer. Narration: Kokoro TTS (`af_heart`) by default; swap for a human or other AI voice
by replacing the audio track or changing `VOICE`.

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
    for lid, title, n, est, vid in rows:
        md.append(f"| {lid} | {title} | {n} | {est:.1f} min | `video-scripts/lessons/{vid}.json` | {'✓' if vid in rendered else ''} |\n")
    (ROOT / "10-video-production-plan.md").write_text("".join(md))
    print(f"{len(rows)} lesson scripts, est. {total / 60:.1f} h total, longest {max(r[3] for r in rows):.1f} min")


if __name__ == "__main__":
    main()
