#!/usr/bin/env python3
"""Write one self-contained prompt for Whop AI: it fetches every file from GitHub,
reads it, builds the whole program on Whop, and ends with the wrap-up report.

Usage: python3 export/build_mega_prompt.py  ->  WHOP-AI-MEGA-PROMPT.txt (+ .md copy)
Only committed files are linked, so every link resolves once the branch is pushed.
"""
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPO, BRANCH = "kyleashton88-cyber/claude", "claude/grid-bot-builder-skills-bmrez2"
RAW = f"https://raw.githubusercontent.com/{REPO}/refs/heads/{BRANCH}/programs/defi-program/"
TREE = f"https://github.com/{REPO}/tree/{BRANCH}/programs/defi-program/"
ZIP = f"https://github.com/{REPO}/archive/refs/heads/{BRANCH}.zip"

tracked = set(subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True, check=True).stdout.split())


def link(rel, note=""):
    assert rel in tracked, f"not committed: {rel}"
    size = (ROOT / rel).stat().st_size
    human = f"{size / 1e6:.1f} MB" if size > 1e6 else f"{size / 1e3:.0f} KB"
    return f"- {RAW}{rel}  ({human}){f'  <- {note}' if note else ''}"


def group(title, rows):
    return f"### {title}\n" + "\n".join(rows) + "\n"


STAGES = [("0", "Zero", [0], "section-0-zero.md"), ("1", "Foundations", [1, 2], "section-1-foundations.md"),
          ("2", "Practitioner", [3, 4, 5], "section-2-practitioner.md"), ("3", "Analyst", [6, 7], "section-3-analyst.md"),
          ("4", "Strategist", [8, 9, 10, 11], "section-4-strategist.md"), ("5", "Operator", [12, 13, 14], "section-5-operator.md")]


def scripts_for(mods):
    out = []
    for m in mods:
        for folder in ("gold", "lessons"):
            fs = sorted((ROOT / "video-scripts" / folder).glob(f"lesson-{m:02d}-*.json"), key=lambda p: int(p.stem.split("-")[-1]))
            out += [link(str(f.relative_to(ROOT)), "GOLD STANDARD (finished)" if folder == "gold" else "") for f in fs]
    return out


brief = (ROOT / "BUILD-PROMPT.md").read_text().split("\n---\n", 1)[1].strip()

manifest = [
    group("A. Core documents: read every one in full before doing anything", [
        link("01-offer-and-curriculum.md", "decisions + full curriculum"),
        link("09-mastery-map.md", "every topic, where it's taught, at what level"),
        link("10-video-production-plan.md", "every course video, length and script file"),
        link("06-whop-store-listing.md", "listing copy, logo and image upload map"),
        link("07-program-operations.md", "capstones, application form, call script, emails, live tier, refund policy (section 9)"),
        link("08-worksheets.md", "17 worksheet templates"),
        link("05-whop-setup.md", "product, plans and course structure"),
        link("video/SCRIPTS.md", "VSL, welcome and module intro scripts with timings"),
        link("video-scripts/gold/lesson-03-2.json", "the GOLD-STANDARD lesson video script: the quality bar"),
        link("WHOP-UPLOAD-GUIDE.md", "the upload process, step by step"),
    ]),
    group("B. Brand and store images (upload to the product listing)", [
        link("assets/brand/brand-guide.png", "brand guide: colours, type, logo rules"),
        link("assets/store/icon-1024.png", "product icon"),
        link("assets/store/banner-1920x1080.png", "cover / hero banner"),
        *[link(f"assets/store/{f.name}", f"gallery {i + 1}") for i, f in enumerate(sorted((ROOT / "assets/store").glob("gallery-*.png")))],
    ]),
    group("C. Videos (upload into Whop; each has a thumbnail and captions below)", [
        link("video/vsl-main.mp4", "LISTING VIDEO + website hero (3:36)"),
        link("video/vsl-short-vertical.mp4", "ads, Reels, Shorts (9:16)"),
        link("video/welcome.mp4", "Start here chapter, first item"),
        *[link(f"video/module-{n:02d}-intro.mp4", f"top of Module {n}") for n in range(15)],
        *[link(f"video/{f.name}", f"Lesson {int(f.stem.split('-')[1])}.{f.stem.split('-')[2]} page") for f in sorted((ROOT / "video").glob("lesson-*.mp4"))],
        f"- Thumbnails (same name, .jpg): {TREE}video/thumbs",
        f"- Captions (same name, .vtt): {TREE}video/captions",
        f"- Chapter lists (same name, .txt): {TREE}video/chapters",
    ]),
    group("D. Sales website (build it on Whop with the main VSL embedded)", [
        link("website/index.html", "the finished page: exact design and copy"),
        link("website/media/vsl-main.mp4", "web-optimised VSL for the page"),
        link("website/media/vsl-poster.jpg", "VSL poster frame"),
        link("website/media/vsl-main.vtt", "VSL captions"),
        f"- All page images: {TREE}website/media",
        link("website/DEPLOY.md", "how the page is deployed"),
    ]),
    group("E. PDFs (downloads inside the course)", [
        link("Day-1-Setup-Kit.pdf", "Start here chapter"),
        link("On-Chain-Operator-Program.pdf", "optional full-course download"),
    ]),
]
stage_links = "\n".join(
    group(f"F{n}. Stage {n} · {name} (Modules {', '.join(map(str, mods))})",
          [link(f"sections/{sec}", "the lessons for this stage"), *scripts_for(mods)])
    for n, name, mods, sec in STAGES)

PROMPT = f"""# ON-CHAIN OPERATOR PROGRAM: COMPLETE BUILD ON WHOP (one prompt)

You are building and launching my **On-Chain Operator Program** on Whop, end to end. Everything you need is in a public
GitHub repository. Your job, in order: **collect** every file listed below, **read** it, **download** the media, **implement**
the whole program on Whop (product, listing, course, videos, website with the VSL embedded, application form, marketing),
and **end** with the wrap-up report in Phase 8.

## How to get the files
- Every link below is a direct download from GitHub's raw file server (public, no login). Open each one and read it in full.
  Text files (.md, .json, .html) are plain text; open them as text. Download images, videos and PDFs as files.
- If a link fails, retry it once. If you can't open links at all, say so immediately and I'll attach the files instead
  (they're packaged in `WHOP-AI-UPLOAD.zip`). **Never guess or invent the contents of a file you couldn't open.**
- Everything at once, as one zip: {ZIP} (unzip, then go to `programs/defi-program/`).
- Browse the folder: {TREE}

## How to work
- One phase per reply. At the end of each phase: what you did, the files you produced (complete, each under a heading with
  its file name), anything you couldn't verify, and "Ready for Phase N". Then wait for me to say **continue**.
- If a reply would be cut off, stop at a file boundary and say where you stopped; I'll say **continue**.
- Where you can act in Whop directly (create the product, plans, course, pages, uploads), do it and tell me what you did.
  Where you can't, give me exact values and click-by-click steps.

---

## THE FILES

{"".join(manifest)}
{stage_links}
---

## THE PHASES

**Phase 0 · Collect.** Open every file in sections A to E. Reply with an inventory: each file, opened yes/no, and one line on
what it contains. Confirm the decided facts (name, price, refund policy, rules) back to me in five bullet points. Don't start
building until I say continue.

**Phase 1 · Product and listing.** Create the product "On-Chain Operator Program". Upload the icon, banner and 7 gallery
images in the order in `06-whop-store-listing.md`. Set `video/vsl-main.mp4` as the listing video. Paste the listing copy,
the refund policy and the footer disclaimer. Create both plans: Course $15,000 one-time; Live on application.

**Phase 2 · Stage reviews and lesson videos (six replies: Stage 0, then 1, 2, 3, 4, 5).** For each stage, open its files in
section F, then do items 1 and 2 of the brief below: the mastery review (change list, then every changed module file in full)
and the lesson video scripts rewritten to the Lesson 3.2 gold standard (one JSON file per lesson, each at most 25 minutes).

**Phase 3 · Build the course.** Item 3 of the brief: 16 chapters (Start here + Modules 0-14), every lesson page with its text,
images and video, the drip rule, capstone pages. Place the media: `welcome.mp4` + `Day-1-Setup-Kit.pdf` in Start here;
`module-NN-intro.mp4` at the top of each module; `lesson-NN-M.mp4` on its lesson page, each with its thumbnail and captions.

**Phase 4 · Website with the VSL embedded.** Item 4 of the brief. Build the site on Whop from `website/index.html` (exact
design and copy) with `website/media/vsl-main.mp4` embedded as the hero video (poster `vsl-poster.jpg`, captions
`vsl-main.vtt`). If Whop can host the HTML directly, use it; otherwise rebuild it section by section and list what differs.

**Phase 5 · Application form.** Item 5 of the brief, and give me the form's link for the Apply buttons.

**Phase 6 · Marketing pack.** Item 6 of the brief.

**Phase 7 · Test.** Walk the buyer path: listing → VSL plays → website → Apply → application form → checkout (Course plan) →
refund policy visible at checkout → course opens on Start here with the welcome video → Module 0 intro video → Lesson 0.1 video.
Report anything that fails.

**Phase 8 · FINAL WRAP-UP (end the process here).**
1. Final checklist: everything left to launch, in order, with who does it (me or Whop) and where.
2. Delivery list: every file you produced in this conversation, with its file name and where it goes (repo folder or Whop page).
3. Compliance pass: confirm there are no promised, projected or guaranteed returns anywhere; the disclaimer is on the listing,
   checkout, website and every module; the refund policy is on the listing, checkout and application; nothing asks for seed
   phrases, keys or account access. List anything that fails.
4. Open items: anything you couldn't do or verify, and what you need from me.
End with a one-paragraph summary of what's built and the single next action for me.

---

## THE BRIEF (the decisions, brand, rules and work items; follow it exactly)

{brief}

---

Start now with **Phase 0 · Collect**.
"""

(ROOT / "WHOP-AI-MEGA-PROMPT.txt").write_text(PROMPT)
(ROOT / "WHOP-AI-MEGA-PROMPT.md").write_text(PROMPT)
print(f"wrote WHOP-AI-MEGA-PROMPT.txt ({len(PROMPT) / 1000:.0f}k characters, {PROMPT.count(RAW)} file links)")
