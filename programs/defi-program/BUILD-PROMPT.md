# Build Prompt: On-Chain Operator Program (for Grok 4.6 · medium)

## How to run it
1. Open a new Grok conversation (Grok 4.6, medium reasoning).
2. **Attach the core files** from the GitHub repo `kyleashton88-cyber/claude`,
   branch `claude/grid-bot-builder-skills-bmrez2`, folder `programs/defi-program/`:
   - `01-offer-and-curriculum.md` (decisions + full curriculum)
   - `09-mastery-map.md` (every topic, where it's taught, at what level)
   - `06-whop-store-listing.md`, `07-program-operations.md`, `08-worksheets.md`
   - `assets/brand/brand-guide.png`, `assets/store/banner-1920x1080.png` (so Grok can see the brand)
   - `video/SCRIPTS.md` (VSL and video scripts)
3. Paste everything below the line as your first message.
4. **The course content is split into six section files** in `sections/`
   (one per stage). Attach **one section per pass** when Grok asks for it:
   `section-0-zero.md` → `section-1-foundations.md` → `section-2-practitioner.md`
   → `section-3-analyst.md` → `section-4-strategist.md` → `section-5-operator.md`.
   (The full single-file version is `ON-CHAIN-OPERATOR-PROGRAM.md` if your
   Grok plan handles very large files.)
5. When Grok returns edited files, put the **lesson files** back in `lessons/` (not the section files, which are generated) and rebuild:
   `python3 programs/defi-program/build_master.py && cd programs/defi-program/export && npm install && npm run build`
   (or ask Claude Code to do it).

Grok doesn't load the Claude skills in `.claude/skills/` and may not reach your
Notion, Zapier or Whop. Anything that needs those accounts comes back to you
as exact values and step-by-step clicks.

---

You're finishing and launching my **On-Chain Operator Program**: a high-ticket
DeFi education program on Whop that takes someone who knows nothing about crypto
to complete mastery: a safe setup, 25 professional strategies, a risk-adjusted
income engine, and operating as their own on-chain bank. It sits in my Whop
store alongside Grid Bot Builder ($997) and Elite Intel Community ($67/mo).

Everything is built: 6 stages, 15 modules, **92 lessons plus a Mastery
Starter (N.0) opening every module**, 25 strategy playbooks, 2 capstones, 17
worksheets, 17 calculators, a store listing, an operations kit, 18 videos
and a brand system. The attached core files describe it; the lessons come in
**six section files, one per stage, which I'll attach one at a time** when you
ask for them. Read the core files fully before doing anything.

## Locked decisions (don't change them)
- Name: **On-Chain Operator Program**. Tagline: **From zero to your own on-chain bank.**
- Course tier **$15,000 one-time**. Live tier priced higher (not yet set).
- Launch to everyone; cold traffic goes **application → call → checkout**.
- 6 stages · 15 modules (0–14) · 92 lessons + 15 Mastery Starters · 25 strategy playbooks · 2 capstones.
- **Every module opens with a Mastery Starter (N.0):** 60-second version, words you'll need, before you start, first safe step, beginner → practitioner → master ladder, and "you've mastered this module when…". Keep this structure in every module.
- Every lesson: Objective → Explanation → Worked example → Checklist → 3-question quiz, with at least one image.

## Brand (lead with the logo)
- Logo: two interlocked chain rings inside a hexagonal block with corner nodes. Colours: ink `#0B1F33`, navy `#12355B`, brand `#1F4E79`, teal `#2ee6a6` (on dark only), blue `#2a78d6`, orange `#eb6834`. Type: Inter; formulas in JetBrains Mono.
- Dark navy gradient with a faint node-network motif for marketing; `#FCFCFB` light surface for documents.
- Never recolour or stretch the logo. Every marketing asset carries the logo and the footer: "Educational content only · Not financial advice · No results are guaranteed".

## Non-negotiable rules
1. **No promised, projected or guaranteed returns or income** anywhere: lessons, ads, emails, sales page, call script, videos. Show how every strategy loses money next to how it earns. No fake scarcity or countdowns.
2. "Operate as your own bank" is a **method**, never presented as a licence or financial service.
3. Never ask for or accept seed phrases, private keys, exchange API keys or account access.
4. Beginner standard: define every term on first use; give do-it-now steps with a small test amount first; name products only as examples and tell learners to check availability and regulation where they live.
5. Every number must be computed, not typed. Show the calculation. If you can run code, check it; otherwise show the arithmetic.
6. Tax and legal points always say to consult a professional. Terms and disclaimers need a lawyer's review before launch: say so.
7. No Discord, Skool or Slack. Use only the Calendly links named in the master file.
8. The repo is public: never put internal IDs, plan IDs, list IDs or private emails in files. Use `<PLACEHOLDERS>`.
9. Ask me before anything outward-facing: publishing, emailing, changing prices or changing any live system.

## Work to do, in order
1. **Ask me the open decisions first** (one message, multiple choice where possible): live-tier price and exact inclusions · refund policy (options in the operations kit §9) · Grid Bot Builder customer pricing (if any) · whether a "Grid Bot Starter" tier exists · access duration (lifetime or 12 months).
2. **Section-by-section mastery review (six passes).** Ask me for one section file at a time, in order (0 → 5). For each section:
   - **Coverage:** check it against `09-mastery-map.md`; list any topic a complete DeFi mastery course needs that's missing or thin, and write it (as a new lesson or an addition), keeping the numbering scheme.
   - **Mastery Starter:** confirm each module's N.0 takes a complete beginner to ready: plain words, defined terms, a safe first step, and a clear mastery test. Improve it where it doesn't.
   - **Accuracy:** check facts are current (products, networks, mechanisms, dates); recompute every worked example; flag anything you can't verify.
   - **Depth:** every lesson reaches its stated level (B/P/M), follows the template, and has at least one image (propose new diagrams by name if needed).
   - **Output:** a change list, then each changed module file **in full** (`lessons/module-NN-name.md`), then an updated `09-mastery-map.md` if coverage changed. Wait for my "next" before the following section.
3. **Sales page:** a complete, responsive HTML page in the brand: hero with logo and the main VSL embed (`video/vsl-main.mp4`), the path (6 stages), curriculum, own-bank section, strategy library, what's included (Course vs Live), who it's for/not for, FAQ, application CTA, disclaimer footer. Single file, no external dependencies except Google Fonts (Inter).
4. **Application form:** build-ready spec (every question, field type, required flag, scoring) from operations kit §4, in Typeform- or Whop-form-ready format.
5. **Whop store setup:** exact values and click-by-click steps for me to create the hidden product, upload the logo/banner/7 gallery images in order (`06-whop-store-listing.md`), paste the copy, set up the course (15 chapters, lesson pages, videos, drip rules from §1), and create the plans once priced.
6. **Funnel:** rewrite my four Zapier skills (`gbb new lead`, `gbb customer onboarding`, `gbb ad performance`, `gbb pipeline check`) as full text, applying `04-funnel-changes.md` with the application-first path, for me to paste into Zapier.
7. **Marketing pack (compliant):** 20 ad hooks, 5 ad scripts (15–30s) matching the VSL's style, a 5-email launch sequence, and 10 organic post ideas, all with no return claims.
8. **Video:** using `video/SCRIPTS.md`, write alternate VSL cuts (a 60s version and a 15s version) and shot-by-shot notes so the same renderer or a video tool can produce them. If you have video/voice generation available, produce them in the brand and say which tool you used.
9. **Final checklist** of everything left for me to do, in order.

## Output format
- Deliver each item as complete files (markdown or HTML) with the file name as a heading, ready to drop into `programs/defi-program/`.
- Keep my existing file names; new files get the next number (`09-sales-page.html`, `10-application-form.md`, `11-marketing-pack.md`, …).
- After each item, list what changed and anything you couldn't verify.

## Done when
Decisions answered · all six sections reviewed for coverage, starters, accuracy and depth · sales page, application form,
Whop setup steps, funnel skill text, marketing pack and extra video cuts
delivered · final checklist written.
