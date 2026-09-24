#!/usr/bin/env python3
"""Package everything Whop AI needs into one numbered, upload-ready zip.

Usage: python3 export/build_whop_bundle.py  ->  WHOP-AI-UPLOAD.zip
Text files are saved as .txt (the format AI uploaders accept most reliably).
Videos are not included: they go straight into the Whop course (see 00-START-HERE).
"""
import json
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "WHOP-AI-UPLOAD.zip"
STAGES = [("0-zero", [0]), ("1-foundations", [1, 2]), ("2-practitioner", [3, 4, 5]),
          ("3-analyst", [6, 7]), ("4-strategist", [8, 9, 10, 11]), ("5-operator", [12, 13, 14])]

prompt = (ROOT / "BUILD-PROMPT.md").read_text()
paste = prompt.split("\n---\n", 1)[1].strip()

FIRST = [
    ("01-offer-and-curriculum.txt", "01-offer-and-curriculum.md"),
    ("02-mastery-map.txt", "09-mastery-map.md"),
    ("03-video-production-plan.txt", "10-video-production-plan.md"),
    ("04-whop-store-listing.txt", "06-whop-store-listing.md"),
    ("05-operations-and-refund-policy.txt", "07-program-operations.md"),
    ("06-worksheets.txt", "08-worksheets.md"),
    ("07-vsl-and-intro-scripts.txt", "video/SCRIPTS.md"),
    ("08-GOLD-STANDARD-lesson-3-2-script.txt", "video-scripts/gold/lesson-03-2.json"),
    ("09-brand-guide.png", "assets/brand/brand-guide.png"),
    ("10-store-banner.png", "assets/store/banner-1920x1080.png"),
]

START = f"""ON-CHAIN OPERATOR PROGRAM: WHOP AI UPLOAD KIT
==============================================

STEP 1. Open Whop's AI.

STEP 2. Attach every file in the folder "1-ATTACH-FIRST" (10 files).

STEP 3. Open "2-PASTE-THIS-AS-YOUR-FIRST-MESSAGE.txt", copy ALL of it, and send it
        as your first message with those attachments.

STEP 4. The AI works in six passes, one stage at a time. When it asks for a section,
        attach the two files for that stage from "3-ATTACH-WHEN-ASKED", in order:
          stage 0 -> stage 1 -> stage 2 -> stage 3 -> stage 4 -> stage 5
        Each stage has:  section-N-...txt        (the lessons)
                         section-N-video-scripts.txt  (the lesson video scripts)

        If the AI limits attachments, send fewer at a time: the order still matters
        (01 -> 10), and the prompt tells it which file is which.

STEP 5. Save everything the AI gives back (new lesson files, rewritten video scripts,
        sales page, application form, marketing pack) and send it to Claude to put
        back into the program and re-render.

UPLOAD DIRECTLY TO YOUR WHOP COURSE (not to the AI)
- Videos: the "video" folder in the GitHub repo (programs/defi-program/video/):
    vsl-main.mp4 (listing video), vsl-short-vertical.mp4 (ads/Reels),
    welcome.mp4 (Start here), module-00-intro.mp4 ... module-14-intro.mp4 (top of each
    module), lesson-00-1.mp4, lesson-02-7.mp4, lesson-03-2.mp4 (their lesson pages).
    Thumbnails: video/thumbs/   Captions: video/captions/ (.vtt)
- Store images: assets/store/ (icon, banner, 7 gallery images, in the order in 04-whop-store-listing)
- PDFs: Day-1-Setup-Kit.pdf (Start here), On-Chain-Operator-Program.pdf (optional download)

Educational content only. Not financial advice. We never ask for seed phrases or keys.
"""


def section_scripts(mods):
    parts = []
    for m in mods:
        for folder in ("gold", "lessons"):
            for f in sorted((ROOT / "video-scripts" / folder).glob(f"lesson-{m:02d}-*.json"),
                            key=lambda p: int(p.stem.split("-")[-1])):
                parts.append(f"===== {f.name} ({'GOLD STANDARD, already finished' if folder == 'gold' else 'baseline: rewrite to the gold standard'}) =====\n"
                             + json.dumps(json.loads(f.read_text()), indent=1, ensure_ascii=False))
    return "\n\n".join(parts)


with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
    base = "WHOP-AI-UPLOAD/"
    z.writestr(base + "00-START-HERE.txt", START)
    names = "\n".join(f"- {n} = `{src}`" for n, src in FIRST)
    z.writestr(base + "2-PASTE-THIS-AS-YOUR-FIRST-MESSAGE.txt",
               "Attached files (the names below are how this prompt refers to them):\n" + names +
               "\n- section-N-....txt = `sections/section-N-....md`; section-N-video-scripts.txt = every lesson video script for that stage\n\n" + paste + "\n")
    for name, src in FIRST:
        z.write(ROOT / src, base + "1-ATTACH-FIRST/" + name)
    for stage, mods in STAGES:
        n = stage.split("-")[0]
        sec = next((ROOT / "sections").glob(f"section-{stage}.md"))
        z.write(sec, f"{base}3-ATTACH-WHEN-ASKED/stage-{n}/section-{stage}.txt")
        z.writestr(f"{base}3-ATTACH-WHEN-ASKED/stage-{n}/section-{n}-video-scripts.txt", section_scripts(mods))

print(f"wrote {OUT.relative_to(ROOT)} ({OUT.stat().st_size / 1e6:.1f} MB)")
