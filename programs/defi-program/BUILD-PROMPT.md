# Build Prompt: On-Chain Operator Program (for Whop AI · Grok 4.6)

## How to run it
1. Open **Whop's AI** (it runs on Grok 4.6).
2. **Attach the core files** from the GitHub repo `kyleashton88-cyber/claude`,
   branch `claude/grid-bot-builder-skills-bmrez2`, folder `programs/defi-program/`:
   - `01-offer-and-curriculum.md` (decisions + full curriculum)
   - `09-mastery-map.md` (every topic, where it's taught, at what level)
   - `10-video-production-plan.md` (every course video, with length and script file)
   - `06-whop-store-listing.md`, `07-program-operations.md` (includes the refund policy), `08-worksheets.md`
   - `assets/brand/brand-guide.png`, `assets/store/banner-1920x1080.png` (so the AI can see the brand)
   - `video/SCRIPTS.md` (VSL and intro scripts) and one example lesson script: `video-scripts/lessons/lesson-00-1.json`
3. Paste everything below the line as your first message.
4. **The lessons come in six section files** in `sections/`, one per stage. Attach one
   section per pass when the AI asks: `section-0-zero.md` → `section-1-foundations.md` →
   `section-2-practitioner.md` → `section-3-analyst.md` → `section-4-strategist.md` →
   `section-5-operator.md`. The matching lesson video scripts are in
   `video-scripts/lessons/` (attach the ones for that section).
5. Put what the AI returns back into the repo: lesson files in `lessons/`, video scripts in
   `video-scripts/lessons/`, new files next to the others. Then rebuild and render:
   `python3 programs/defi-program/build_master.py && cd programs/defi-program/export && npm install && npm run build && node build_video.js lessons`

---

You're finishing and launching my **On-Chain Operator Program** on Whop: a DeFi education
program that takes someone who knows nothing about crypto to complete mastery: a safe setup,
30 professional strategies, a risk-adjusted income engine, and operating as their own on-chain
bank. It sits in my Whop store alongside Grid Bot Builder ($997) and Elite Intel Community ($67/mo).

Everything is built: 6 stages, 15 modules, **107 lessons (15 of them expert-level) plus a
Mastery Starter (N.0) opening every module**, 30 strategy playbooks in 7 levels, 2 capstones,
17 worksheets, 20 calculators, a store listing, an operations kit with the refund policy,
55 images, 18 finished videos (VSLs, welcome, module intros) and **121 lesson video scripts**.
The lessons come in six section files, which I'll attach one at a time when you ask. Read the
core files fully before doing anything.

## Decided (don't ask about these, don't change them)
- Name: **On-Chain Operator Program**. Tagline: **From zero to your own on-chain bank.**
- Course tier **$15,000 one-time**. **Live tier: price on application**, set on the sales call. Lifetime access.
- **Refund policy: 14-day conditional refund** (full text in `07-program-operations.md` §9): a full refund within 14 days if ≤ 10% of lessons are completed (10 of 107), no capstone has been submitted and no live session or review has been used. Duplicate purchases and access problems not fixed within 7 days are always refunded. No refunds based on investment results. Chargebacks end access. Show it on the listing, at checkout and in the application acknowledgement.
- Launch to everyone; cold traffic goes **application → call → checkout**.
- 6 stages · 15 modules (0–14) · 107 lessons + 15 Mastery Starters · 30 strategy playbooks · 2 capstones.
- **Every module opens with a Mastery Starter (N.0):** 60-second version, words you'll need, before you start, first safe step, beginner → practitioner → master ladder, "you've mastered this module when…". Keep this in every module.
- Every lesson: Objective → Explanation → Worked example → Checklist → 3-question quiz, with at least one image.

## Brand (lead with the logo)
- Logo: two interlocked chain rings inside a hexagonal block with corner nodes. Colours: ink `#0B1F33`, navy `#12355B`, brand `#1F4E79`, teal `#2ee6a6` (on dark only), blue `#2a78d6`, orange `#eb6834`. Type: Inter; formulas in JetBrains Mono.
- Dark navy gradient with a faint node-network motif for marketing and video; `#FCFCFB` light surface for documents and diagrams.
- Never recolour or stretch the logo. Every marketing asset and video carries the logo and the footer "Educational content only · Not financial advice · No results are guaranteed".

## Rules
1. **No promised, projected or guaranteed returns or income** anywhere: lessons, videos, ads, emails, sales page, call script. Show how every strategy loses money next to how it earns. No fake scarcity or countdowns.
2. "Operate as your own bank" is a **method**, never presented as a licence or financial service.
3. Never ask for or accept seed phrases, private keys, exchange API keys or account access.
4. Beginner standard: define every term on first use; do-it-now steps with a small test amount first; name products only as examples and tell learners to check availability where they live.
5. Every number is computed, not typed. Show the calculation.
6. In lessons, tax and legal points tell learners to consult a professional.
7. No Discord, Skool or Slack. Use only the Calendly links named in the files.
8. Never put internal IDs, plan IDs, list IDs or private emails in files. Use `<PLACEHOLDERS>`.

## Work to do, in order

### 1. Section-by-section mastery review (six passes, 0 → 5)
Ask me for one section at a time. For each section:
- **Coverage:** check it against `09-mastery-map.md`; write any missing or thin topic a complete DeFi mastery course needs (new lesson or addition, keeping the numbering).
- **Mastery Starter:** make sure each N.0 takes a complete beginner to ready.
- **Accuracy:** check facts are current (products, networks, mechanisms, dates); recompute every worked example; flag anything you can't verify.
- **Depth:** every lesson reaches its level (B/P/M), follows the template, and has at least one image.
- **Output:** change list, then each changed module file in full (`lessons/module-NN-name.md`), and an updated `09-mastery-map.md` if coverage changed.

### 2. Course video production: every lesson, maximum 25 minutes each
Do this in the same six passes, right after each section's review.
- **One video per lesson and per Mastery Starter** (121 videos: all lessons except 8.3), plus the **strategy library (8.3) as a 7-video series**, one per level.
- **Length:** each video at most **25 minutes**. Targets: Mastery Starters 5–10 min; lessons 8–20 min; expert lessons and the 8.3 level videos up to 25 min. If a lesson needs more, split it into Part 1 and Part 2, each ≤ 25 min.
- **Teach, don't read:** the baseline scripts in `video-scripts/lessons/` read the lesson text (3–5 min each). Rewrite each into a full teaching script: explain the idea in plain words, walk through the worked example step by step with the numbers on screen, show every diagram and say what to look at, add a real-world scenario, read the checklist, and do the quiz as question → pause → answer. Use the lesson file as the source of truth; don't add claims that aren't in it.
- **Structure (every video):** title card (module banner + lesson number/title) → objective → teaching segments (one idea per scene) → diagrams/charts → worked example → common mistakes → checklist → quiz → outro ("Do the checklist before moving on"). Add chapter timestamps.
- **Visuals:** use the existing images in `assets/` (module banners, diagrams, charts). Where a new visual would teach better, describe it precisely (title, what it shows, data) and name the file `assets/diagrams/<name>.png` or `assets/charts/<name>.png` so it can be added to the renderer.
- **Captions and brand:** burned-in captions, logo, footer disclaimer, the brand colours above.
- **Thumbnail:** for each video, a thumbnail title (≤ 5 words) and subtitle in the brand style.
- **Format:** deliver each video as a JSON file in exactly this schema (the renderer turns it into an MP4 with narration and captions), named `video-scripts/lessons/lesson-NN-M.json`:
```json
{"id": "lesson-03-2", "title": "Lesson 3.2: LTV, liquidation threshold & health factor", "size": [1920, 1080],
 "group": "lessons", "maxMinutes": 25, "use": "Lesson 3.2 page in the Whop course.",
 "chapters": [["0:00", "Objective"], ["1:10", "Health factor explained"]],
 "thumbnail": {"title": "Never get liquidated", "subtitle": "Lesson 3.2"},
 "scenes": [
  {"type": "image", "src": "assets/modules/module-03.png", "eyebrow": "Lesson 3.2", "vo": "Spoken narration…", "cap": "Written caption…"},
  {"type": "statement", "lines": ["Objective"], "sub": "On-screen text", "vo": "…", "cap": "…"},
  {"type": "bullets", "title": "Key ideas", "items": ["Short point", "Short point"], "vo": "…", "cap": "…"},
  {"type": "statement", "lines": ["Quiz", "Question?"], "sub": "Answer: …", "subAt": 0.62, "vo": "Question? … Pause and think. … The answer: …", "cap": "…"},
  {"type": "cta", "button": "Do the checklist", "sub": "Educational content only · Not financial advice", "vo": "…", "cap": "…"}
 ]}
```
  Scene types: `image`, `statement`, `bullets`, `stats`, `strike`, `logo`, `cta`. `vo` is what the narrator says (spell out abbreviations and numbers the way they should be spoken, e.g. "A.P.Y.", "health factor"); `cap` is the on-screen caption in normal written form. About 150 spoken words per minute, so a 15-minute video is about 2,200 words of `vo`.
- **If you can generate video directly** (voice and visuals) in Whop, also produce the finished videos in this brand and structure, each ≤ 25 minutes, and tell me which tool you used.

### 3. Build the course in Whop
Create (or give me exact values and steps for) the product, both plans (Course $15,000 one-time; Live on application), the refund policy text at checkout, the course with 15 chapters (Start here + Modules 0–14), every lesson page (lesson text, images, its video), the Day-1 Setup Kit PDF, capstone pages, and the drip rule (each stage unlocks when the previous stage's quizzes are passed). Upload the logo, banner and 7 gallery images in the order in `06-whop-store-listing.md`, and the main VSL as the listing video.

### 4. Sales page
A complete, responsive HTML page in the brand: hero with logo and the main VSL (`video/vsl-main.mp4`), the path (6 stages), curriculum, expert lessons, own-bank section, strategy library, what's included (Course vs Live), who it's for/not for, FAQ (including the refund policy), application CTA, disclaimer footer. One file, Google Fonts (Inter) only.

### 5. Application form
Build-ready spec from operations kit §4 (questions, field types, required flags, scoring, and the acknowledgement that includes the refund policy).

### 6. Marketing pack
20 ad hooks, 5 ad scripts (15–30s) in the VSL style, a 5-email launch sequence, 10 organic post ideas, and 60s + 15s VSL cuts in the JSON scene schema above. All with no return claims.

### 7. Final checklist
Everything left to launch, in order.

## Output format
- Deliver complete files, each under a heading with its file name, ready to drop into `programs/defi-program/`.
- Keep existing file names; new files get the next number (`11-sales-page.html`, `12-application-form.md`, `13-marketing-pack.md`, …).
- After each item, list what changed and anything you couldn't verify.

## Done when
All six sections reviewed · 121 lesson videos + the 7-part strategy series scripted (or produced), each ≤ 25 minutes ·
course built in Whop with the refund policy · sales page, application form and marketing pack delivered ·
final checklist written.
