#!/usr/bin/env python3
"""Package everything for Whop: the Whop AI kit and the course media.

Usage:
  python3 export/build_whop_bundle.py            -> WHOP-AI-UPLOAD.zip (small; in the repo)
  python3 export/build_whop_bundle.py --media DIR -> DIR/WHOP-MEDIA-1-store-and-start-here.zip
                                                     DIR/WHOP-MEDIA-2-module-intros.zip
                                                     DIR/WHOP-MEDIA-3-lesson-videos.zip
Text files are .txt (the format AI uploaders accept most reliably). The media zips
hold the videos and images that go straight into Whop; they're too big for git.
"""
import json
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STAGES = [("0-zero", [0], "Zero"), ("1-foundations", [1, 2], "Foundations"), ("2-practitioner", [3, 4, 5], "Practitioner"),
          ("3-analyst", [6, 7], "Analyst"), ("4-strategist", [8, 9, 10, 11], "Strategist"), ("5-operator", [12, 13, 14], "Operator")]

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
    ("11-website-index.html.txt", "website/index.html"),
]


# ---------------------------------------------------------------- messages
def stage_message(i, stage, name):
    n = int(stage.split("-")[0])
    tail = f'"Ready for Stage {n + 1}"' if n < 5 else '"All six stages done"'
    cut = "\nIf your reply gets cut off, stop at a file boundary and I'll write 'continue'." if i == 0 else ""
    return f"""Here is Stage {n} ({name}). Attached: section-{stage}.txt (the lessons) and section-{n}-video-scripts.txt (the lesson video scripts).

For this stage, do item 1 and item 2 of the brief:
1. Mastery review: check coverage against the mastery map, make every Mastery Starter take a complete beginner to ready, check every fact and recompute every worked example, and bring every lesson to its level. Give me the change list, then every changed module file in full.
2. Video scripts: rewrite every lesson video script in this stage to the Lesson 3.2 gold standard and its target length (each at most 25 minutes), in the exact JSON schema, one file per lesson named video-scripts/gold/lesson-NN-M.json.

Finish with what changed, anything you couldn't verify, and {tail}.{cut}"""


MESSAGES = [
    ("03-after-stage-5-build-course.txt", """All six stages are reviewed. Now do item 3 of the brief: build the course in Whop.

Create (or give me exact values and click-by-click steps for) the product, both plans (Course $15,000 one-time; Live on application), the 14-day conditional refund policy text at checkout, the course with 16 chapters (Start here + Modules 0-14), every lesson page with its text, images and video slot, the Day-1 Setup Kit PDF on Start here, the capstone pages, and the drip rule (each stage unlocks when the previous stage's quizzes are passed).

Tell me exactly which video file goes on which page: listing = vsl-main.mp4, Start here = welcome.mp4, top of each module = module-NN-intro.mp4, lesson pages = lesson-NN-M.mp4."""),
    ("04-website.txt", """Now do item 4 of the brief: build the website on Whop with the main VSL embedded.

Use the attached finished page (11-website-index.html.txt) as the exact design and copy. The hero video is vsl-main.mp4 (web copy: website/media/vsl-main.mp4, poster website/media/vsl-poster.jpg). Also set vsl-main.mp4 as the product's listing video. Keep every section, the brand, the refund wording and the disclaimer. If Whop can host the HTML directly, use it; otherwise rebuild it section by section and list anything you couldn't reproduce."""),
    ("05-application-form.txt", """Now do item 5 of the brief: the application form. Give me the build-ready spec from operations kit section 4 (every question, field type, required flag, the scoring, and the acknowledgement that includes the 14-day conditional refund policy), and build it in Whop if you can. Give me the form's link so it can go on the Apply buttons."""),
    ("06-marketing-pack.txt", """Now do item 6 of the brief: the marketing pack. 20 ad hooks, 5 ad scripts (15-30 seconds) in the VSL style, a 5-email launch sequence, 10 organic post ideas, and 60-second and 15-second VSL cuts in the JSON scene schema. No return or income claims anywhere, no fake urgency."""),
    ("07-FINAL-wrap-up.txt", """Final step. Do item 7 of the brief and close out the build.

1. Final checklist: everything left to launch, in order, with who does it (me or Whop) and where.
2. Delivery list: every file you gave me in this conversation, with its file name and where it goes (repo folder or Whop page).
3. Compliance pass: confirm there are no promised, projected or guaranteed returns anywhere; the disclaimer is on the listing, checkout, website and every module; the refund policy is on the listing, checkout and application; and nothing asks for seed phrases, keys or account access. List anything that fails.
4. Open items: anything you couldn't do or verify, and what you need from me to finish it.

End with a one-paragraph summary of what's built and the single next action for me."""),
]

START = """ON-CHAIN OPERATOR PROGRAM: THE WHOLE WHOP PROCESS
===================================================

You have four downloads:
  WHOP-AI-UPLOAD.zip                      <- this kit (for Whop AI)
  WHOP-MEDIA-1-store-and-start-here.zip   <- store images, VSLs, welcome, PDFs, website
  WHOP-MEDIA-2-module-intros.zip          <- 15 module intro videos
  WHOP-MEDIA-3-lesson-videos.zip          <- finished lesson videos
Each media zip has a MEDIA-MAP.txt saying where every file goes.

-----------------------------------------------------------------
PART A. SET UP THE PRODUCT (about 15 minutes, in the Whop dashboard)
-----------------------------------------------------------------
A1. Create the product "On-Chain Operator Program".
A2. From WHOP-MEDIA-1 > 1-store: upload the icon, the banner and the 7 gallery images
    in the order in 04-whop-store-listing.txt.
A3. From WHOP-MEDIA-1 > 2-videos: upload vsl-main.mp4 as the listing video.

-----------------------------------------------------------------
PART B. RUN WHOP AI (copy and paste; one message at a time)
-----------------------------------------------------------------
B1. Open Whop's AI. Attach all 11 files in "1-ATTACH-FIRST".
B2. Paste ALL of "2-PASTE-THIS-AS-YOUR-FIRST-MESSAGE.txt" and send.
B3. Six stage passes. For each stage 0 -> 5, in order:
      - attach the two files in "3-ATTACH-WHEN-ASKED/stage-N/"
      - paste the matching message from "4-MESSAGES-IN-ORDER" (01-stage-0 ... 01-stage-5)
      - save everything it gives back (copy each file into a text file with the name it gives)
    If a reply is cut off, type: continue
B4. Then paste, one at a time, waiting for each reply:
      03-after-stage-5-build-course.txt   (builds the course in Whop)
      04-website.txt                      (builds the website with the VSL embedded)
      05-application-form.txt             (application form + its link)
      06-marketing-pack.txt               (ads, emails, posts, short VSL cuts)
B5. END THE PROCESS: paste 07-FINAL-wrap-up.txt. Whop AI finishes with the final
    launch checklist, the list of every file it delivered, a compliance check and
    anything still open.

-----------------------------------------------------------------
PART C. UPLOAD THE MEDIA INTO THE COURSE (Whop dashboard)
-----------------------------------------------------------------
C1. Start here chapter: welcome.mp4 + Day-1-Setup-Kit.pdf (WHOP-MEDIA-1).
C2. Top of each module: module-NN-intro.mp4 (WHOP-MEDIA-2).
C3. Lesson pages: lesson-NN-M.mp4 (WHOP-MEDIA-3). Every video has a thumbnail (thumbs/)
    and a captions file (captions/) with the same name.
C4. Website: the "4-website" folder in WHOP-MEDIA-1 (if Whop AI didn't host it, put the
    folder on any web host and link it from Whop).

-----------------------------------------------------------------
PART D. BRING IT BACK
-----------------------------------------------------------------
D1. Send Claude everything Whop AI produced (rewritten lessons, gold video scripts,
    website changes, the application form link, the marketing pack). Claude puts it into
    the program, renders every remaining lesson video (each at most 25 minutes) and puts
    the application link on the website's Apply buttons.

Educational content only. Not financial advice. Never share a seed phrase or keys.
"""


def section_scripts(mods):
    parts = []
    for m in mods:
        for folder in ("gold", "lessons"):
            for f in sorted((ROOT / "video-scripts" / folder).glob(f"lesson-{m:02d}-*.json"), key=lambda p: int(p.stem.split("-")[-1])):
                parts.append(f"===== {f.name} ({'GOLD STANDARD, already finished' if folder == 'gold' else 'baseline: rewrite to the gold standard'}) =====\n"
                             + json.dumps(json.loads(f.read_text()), indent=1, ensure_ascii=False))
    return "\n\n".join(parts)


def ai_kit():
    out = ROOT / "WHOP-AI-UPLOAD.zip"
    paste = (ROOT / "BUILD-PROMPT.md").read_text().split("\n---\n", 1)[1].strip()
    names = "\n".join(f"- {n} = `{src}`" for n, src in FIRST)
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        b = "WHOP-AI-UPLOAD/"
        z.writestr(b + "00-START-HERE.txt", START)
        z.writestr(b + "2-PASTE-THIS-AS-YOUR-FIRST-MESSAGE.txt",
                   "Attached files (the names below are how this prompt refers to them):\n" + names +
                   "\n- section-N-....txt = `sections/section-N-....md`; section-N-video-scripts.txt = every lesson video script for that stage\n\n"
                   "Work through the brief one item at a time and wait for my next message between items. Start by confirming "
                   "you've read the attached files, then ask me for Stage 0.\n\n" + paste + "\n")
        for name, src in FIRST:
            z.write(ROOT / src, b + "1-ATTACH-FIRST/" + name)
        for i, (stage, mods, name) in enumerate(STAGES):
            n = stage.split("-")[0]
            z.write(next((ROOT / "sections").glob(f"section-{stage}.md")), f"{b}3-ATTACH-WHEN-ASKED/stage-{n}/section-{stage}.txt")
            z.writestr(f"{b}3-ATTACH-WHEN-ASKED/stage-{n}/section-{n}-video-scripts.txt", section_scripts(mods))
            z.writestr(f"{b}4-MESSAGES-IN-ORDER/01-stage-{n}.txt", stage_message(i, stage, name) + "\n")
        for name, text in MESSAGES:
            z.writestr(f"{b}4-MESSAGES-IN-ORDER/{name}", text + "\n")
    print(f"wrote {out.relative_to(ROOT)} ({out.stat().st_size / 1e6:.1f} MB)")


# ---------------------------------------------------------------- media
def media(dest):
    dest = Path(dest)
    dest.mkdir(parents=True, exist_ok=True)
    V = ROOT / "video"

    def vid(z, folder, stem, where):
        z.write(V / f"{stem}.mp4", f"{folder}/{stem}.mp4", compress_type=zipfile.ZIP_STORED)
        for sub, ext in (("thumbs", "jpg"), ("captions", "vtt"), ("chapters", "txt")):
            f = V / sub / f"{stem}.{ext}"
            if f.exists():
                z.write(f, f"{folder}/{sub}/{stem}.{ext}")
        return f"{folder}/{stem}.mp4  ->  {where}"

    rows = []
    with zipfile.ZipFile(dest / "WHOP-MEDIA-1-store-and-start-here.zip", "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted((ROOT / "assets/store").glob("*.png")):
            z.write(f, f"1-store/{f.name}")
        rows.append("1-store/icon-1024.png  ->  product icon\n1-store/banner-1920x1080.png  ->  cover / hero banner\n"
                    "1-store/gallery-01 ... gallery-07  ->  gallery, in number order")
        rows.append(vid(z, "2-videos", "vsl-main", "product LISTING VIDEO (and the website hero)"))
        rows.append(vid(z, "2-videos", "vsl-short-vertical", "ads, Reels, Shorts, TikTok (9:16)"))
        rows.append(vid(z, "2-videos", "welcome", "Start here chapter, first item"))
        z.write(ROOT / "Day-1-Setup-Kit.pdf", "3-pdfs/Day-1-Setup-Kit.pdf")
        z.write(ROOT / "On-Chain-Operator-Program.pdf", "3-pdfs/On-Chain-Operator-Program.pdf")
        rows.append("3-pdfs/Day-1-Setup-Kit.pdf  ->  Start here chapter (download)\n3-pdfs/On-Chain-Operator-Program.pdf  ->  optional full-course download")
        for f in sorted((ROOT / "website").rglob("*")):
            if f.is_file():
                z.write(f, f"4-website/{f.relative_to(ROOT / 'website')}", compress_type=zipfile.ZIP_STORED if f.suffix == ".mp4" else zipfile.ZIP_DEFLATED)
        rows.append("4-website/  ->  the sales website with the VSL embedded (keep media/ next to index.html)")
        z.writestr("MEDIA-MAP.txt", "WHERE EVERY FILE GOES (part 1 of 3)\n\n" + "\n".join(rows) +
                   "\n\nEvery video has a thumbnail (thumbs/), captions (captions/, .vtt) and chapters (chapters/) with the same name.\n")
    rows = []
    with zipfile.ZipFile(dest / "WHOP-MEDIA-2-module-intros.zip", "w", zipfile.ZIP_DEFLATED) as z:
        for n in range(15):
            rows.append(vid(z, "module-intros", f"module-{n:02d}-intro", f"top of Module {n} (first item in its chapter)"))
        z.writestr("MEDIA-MAP.txt", "WHERE EVERY FILE GOES (part 2 of 3)\n\n" + "\n".join(rows) + "\n")
    rows = []
    with zipfile.ZipFile(dest / "WHOP-MEDIA-3-lesson-videos.zip", "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(V.glob("lesson-*.mp4")):
            a, b = f.stem.split("-")[1:]
            rows.append(vid(z, "lesson-videos", f.stem, f"Lesson {int(a)}.{b} page (Module {int(a)})"))
        z.writestr("MEDIA-MAP.txt", "WHERE EVERY FILE GOES (part 3 of 3)\n\n" + "\n".join(rows) +
                   "\n\nThe other lesson videos are scripted; they render after Whop AI's rewrite (00-START-HERE, part D).\n")
    for f in sorted(dest.glob("WHOP-MEDIA-*.zip")):
        print(f"wrote {f.name} ({f.stat().st_size / 1e6:.0f} MB)")


if __name__ == "__main__":
    ai_kit()
    if "--media" in sys.argv:
        media(sys.argv[sys.argv.index("--media") + 1])
