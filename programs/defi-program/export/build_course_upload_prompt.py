#!/usr/bin/env python3
"""Write the Whop AI prompt that fills every chapter of the course: each lesson page gets
its text, video (with thumbnail and captions) and images, in curriculum order.

Usage: python3 export/build_course_upload_prompt.py  ->  WHOP-COURSE-UPLOAD-PROMPT.txt
Every link points at a committed file on GitHub's raw server (public, no login).
"""
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPO, BRANCH = "kyleashton88-cyber/claude", "claude/grid-bot-builder-skills-bmrez2"
RAW = f"https://raw.githubusercontent.com/{REPO}/refs/heads/{BRANCH}/programs/defi-program/"
tracked = set(subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True, check=True).stdout.split())


def url(rel):
    assert rel in tracked, f"not committed: {rel}"
    return RAW + rel


def lessons_of(num):
    """[(lesson id, title, source file, images)] for a module, in order."""
    f = next((ROOT / "lessons").glob(f"module-{num:02d}-*.md"))
    text = f.read_text()
    parts = re.split(r"^## Lesson (\d+\.\d+) — (.+)$", text, flags=re.M)
    out = []
    for i in range(1, len(parts), 3):
        lid, title, body = parts[i], re.sub(r"\s*\*\(.*?\)\*\s*$", "", parts[i + 1]).strip(), parts[i + 2]
        src = f"lessons/{f.name}"
        if lid == "2.2":
            continue
        if lid == "8.3":
            src, body = "03-defi-strategy-mastery.md", (ROOT / "03-defi-strategy-mastery.md").read_text()
            title = "The strategy library (30 strategies in 7 levels)"
        imgs = [p.replace("../", "") for p in re.findall(r"!\[[^\]]*\]\(([^)]+)\)", body)]
        out.append((lid, "Mastery Starter" if lid.endswith(".0") else title, src, imgs))
    if num == 2:
        sample = (ROOT / "02-sample-lesson-amm-math.md").read_text()
        imgs = [p.replace("../", "") for p in re.findall(r"!\[[^\]]*\]\(([^)]+)\)", sample)]
        out.append(("2.2", "AMM mathematics (x · y = k)", "02-sample-lesson-amm-math.md", imgs))
    return sorted(out, key=lambda r: int(r[0].split(".")[1])), re.match(r"# Module \d+ — (.+)", text).group(1).strip()


def lesson_block(lid, title, src, imgs):
    a, b = lid.split(".")
    vid = f"lesson-{int(a):02d}-{b}"
    lines = [f"#### Lesson {lid} · {title}",
             f"- Text: {url(src)}  " + (f"(use the section headed \"Lesson {lid}\")" if src.startswith("lessons/") else "(the whole file is this lesson)")]
    if (ROOT / "video" / f"{vid}.mp4").exists():
        lines += [f"- Video: {url(f'video/{vid}.mp4')}",
                  f"- Thumbnail: {url(f'video/thumbs/{vid}.jpg')}",
                  f"- Captions: {url(f'video/captions/{vid}.vtt')}",
                  f"- Chapters (paste into the description): {url(f'video/chapters/{vid}.txt')}"]
    else:
        lines.append("- Video: none yet (leave the video slot empty)")
    seen = []
    for p in imgs:
        if p not in seen:
            seen.append(p)
    lines += [f"- Image: {url(p)}" for p in seen]
    return "\n".join(lines)


chapters = []
chapters.append("\n".join([
    "### Chapter: Start here",
    f"- Welcome video, full tour (10 min, first item): {url('video/welcome-long.mp4')}  (thumbnail {url('video/thumbs/welcome-long.jpg')}, captions {url('video/captions/welcome-long.vtt')}, chapters {url('video/chapters/welcome-long.txt')})",
    f"- How the program works, full walkthrough (23 min, second item): {url('video/how-the-program-works.mp4')}  (thumbnail {url('video/thumbs/how-the-program-works.jpg')}, captions {url('video/captions/how-the-program-works.vtt')}, chapters {url('video/chapters/how-the-program-works.txt')})",
    f"- Short welcome (1 min, optional third item): {url('video/welcome.mp4')}  (thumbnail {url('video/thumbs/welcome.jpg')}, captions {url('video/captions/welcome.vtt')})",
    f"- Day-1 Setup Kit (PDF download): {url('Day-1-Setup-Kit.pdf')}",
    f"- How to use the Day-1 Setup Kit (video, 10 min, directly under the kit): {url('video/day1-kit-guide.mp4')}  (thumbnail {url('video/thumbs/day1-kit-guide.jpg')}, captions {url('video/captions/day1-kit-guide.vtt')}, chapters {url('video/chapters/day1-kit-guide.txt')})",
    f"- Full course PDF (optional download): {url('On-Chain-Operator-Program.pdf')}",
    f"- Course Hub (optional offline companion; the file needs the repo's assets and video folders beside it): {url('course-hub/index.html')}",
    "- Text for this page: a short welcome, how every lesson works (watch → do the checklist → quiz), and the rule",
    "  \"Nobody from this program will ever ask for your seed phrase or keys.\"",
]))
n_lessons = n_videos = n_images = 0
for num in range(15):
    rows, mtitle = lessons_of(num)
    head = [f"### Chapter: Module {num} · {mtitle}",
            (f"- Module intro video (first item in the chapter; for Module 0 it's the long, story-led crypto-from-zero intro that ends by sending learners to Lesson 0.0): " if num == 0 else "- Module intro video (first item in the chapter): ") + f"{url(f'video/module-{num:02d}-intro.mp4')}  "
            f"(thumbnail {url(f'video/thumbs/module-{num:02d}-intro.jpg')}, captions {url(f'video/captions/module-{num:02d}-intro.vtt')}" + (f", chapters {url('video/chapters/module-00-intro.txt')}" if num == 0 else "") + ")",
            f"- Chapter cover image: {url(f'assets/modules/module-{num:02d}.png')}", ""]
    blocks = []
    for r in rows:
        blocks.append(lesson_block(*r))
        n_lessons += 1
        n_images += len(set(r[3]))
        a, b = r[0].split(".")
        n_videos += (ROOT / "video" / f"lesson-{int(a):02d}-{b}.mp4").exists()
    chapters.append("\n".join(head) + "\n" + "\n\n".join(blocks))

PROMPT = f"""# ON-CHAIN OPERATOR PROGRAM: FILL EVERY CHAPTER OF THE WHOP COURSE

You're adding the finished course content to my Whop course for the **On-Chain Operator Program**: every chapter,
every lesson page, with its text, its narrated video (thumbnail and captions) and its images. Everything is in a public
GitHub repository; every link below downloads directly, no login needed.

**Scope:** {n_lessons} lesson pages in 16 chapters (Start here + Modules 0-14), {n_videos} lesson videos, 15 module intro videos,
the welcome video and {n_images} lesson images.

## Rules
- **Only the course content.** Don't change the product, prices, plans, checkout, refund policy or store listing.
  Don't approve waitlist entries or applications. Don't publish or unhide anything unless I tell you to.
- **Use the files exactly as they are.** Don't rewrite lessons, re-cut videos or edit images. Never invent content for a
  file you couldn't open; tell me instead.
- **Keep the order** below: chapters in order, lessons in order inside each chapter (N.0 Mastery Starter first).
- **Compliance stays on every page:** "Educational content only. Not financial advice. No results are guaranteed."
  Nothing may promise or project returns, and nothing may ask for seed phrases, keys or account access.
- If Whop limits upload size or count, tell me the limit and continue with the next item; list what's left at the end.

## How to build each lesson page
1. Title: "Lesson N.M · <title>" (Mastery Starters: "N.0 · Mastery Starter").
2. Video at the top: upload the MP4, set the thumbnail, attach the captions (.vtt, English), and paste the chapter list
   (from the Chapters link) into the video description so learners can jump to sections.
3. Lesson text: open the Text link, take the section for that lesson, and paste it as the page body, keeping its
   headings (Objective, Explanation, Worked example, Checklist, Quiz). Keep the checklist as checkboxes if Whop supports
   them, and the quiz answers hidden or collapsed if it can.
4. Images: upload each Image and place it where its tag appears in the lesson text (the tag looks like
   `![Alt text](../assets/...png)`); use the alt text as the caption. If you can't place images inline, put them right
   under the Objective.
5. End every page with the disclaimer line above.

## How to work
- One chapter per reply: build it, then report what you created (every page and upload), what failed and why, and
  "Ready for the next chapter". Wait for me to say **continue**.
- If a reply would be cut off, stop at a lesson boundary, say where, and I'll say **continue**.
- If you can't create pages or upload files directly in Whop, give me exact click-by-click steps for each page with the
  links to use, and I'll do it.

## FINAL WRAP-UP (after the last chapter, end the process here)
1. Totals: chapters built, lesson pages built, videos uploaded, images uploaded, captions attached; anything missing,
   with the lesson id.
2. Spot-check: open Lesson 0.1, Lesson 3.2 and Lesson 14.6 as a member would and confirm video, captions, images, text,
   checklist, quiz and disclaimer all show.
3. Compliance pass: no return promises, the disclaimer on every page, nothing asking for keys or account access.
4. Open items and the single next action for me.

---

## THE CONTENT, CHAPTER BY CHAPTER

""" + "\n\n".join(chapters) + "\n\n---\n\nStart now with **Chapter: Start here**.\n"

(ROOT / "WHOP-COURSE-UPLOAD-PROMPT.txt").write_text(PROMPT)

# The same prompt split into one message per stage, for chats with a message-length limit.
head, body = PROMPT.split("## THE CONTENT, CHAPTER BY CHAPTER", 1)
by_title = {c.split("\n", 1)[0]: c for c in chapters}
STAGES = [("Start here + Stage 0 · Zero", ["Start here", 0]), ("Stage 1 · Foundations", [1, 2]), ("Stage 2 · Practitioner", [3, 4, 5]),
          ("Stage 3 · Analyst", [6, 7]), ("Stage 4 · Strategist", [8, 9, 10, 11]), ("Stage 5 · Operator", [12, 13, 14])]
parts = ROOT / "WHOP-COURSE-UPLOAD-PARTS"
parts.mkdir(exist_ok=True)
for i, (name, keys) in enumerate(STAGES, 1):
    chs = [c for c in chapters if any(c.startswith(f"### Chapter: {'Start here' if k == 'Start here' else f'Module {k} ·'}") for k in keys)]
    intro = (head + f"## THE CONTENT: PART 1 OF 6 ({name})\n\nThe rest arrives in parts 2 to 6, one message each. Build this part, then wait.\n\n") if i == 1 else \
        (f"# PART {i} OF 6: {name}\n\nSame task and rules as part 1. Build these chapters the same way, one chapter per reply, and wait for **continue** between them." +
         (" This is the last part: after it, do the FINAL WRAP-UP from part 1." if i == 6 else "") + "\n\n")
    (parts / f"part-{i}-of-6.txt").write_text(intro + "\n\n".join(chs) + "\n")
print("wrote WHOP-COURSE-UPLOAD-PARTS/part-1..6", [len((parts / f"part-{i}-of-6.txt").read_text()) // 1000 for i in range(1, 7)], "k chars")
print(f"wrote WHOP-COURSE-UPLOAD-PROMPT.txt ({len(PROMPT) / 1000:.0f}k chars): {n_lessons} lessons, {n_videos} lesson videos, {n_images} lesson images, {PROMPT.count(RAW)} links")
