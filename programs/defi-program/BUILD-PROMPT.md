# Build Prompt: On-Chain Operator Program (for Grok 4.6 · medium)

## How to run it
1. Open a new Grok conversation (Grok 4.6, medium reasoning).
2. **Attach these files** from the GitHub repo `kyleashton88-cyber/claude`,
   branch `claude/grid-bot-builder-skills-bmrez2`, folder `programs/defi-program/`:
   - `ON-CHAIN-OPERATOR-PROGRAM.md` (the master file: everything in one document), or the PDF if Grok can't take large markdown
   - `07-program-operations.md` and `06-whop-store-listing.md` (also inside the master, but easier to edit on their own)
   - `assets/brand/brand-guide.png`, `assets/store/banner-1920x1080.png` (so Grok can see the brand)
   - `video/SCRIPTS.md` (VSL and video scripts)
3. Paste everything below the line as your first message.
4. When Grok returns edited files, put them back in the repo folder and rebuild:
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

The attached master file contains everything built so far: decisions,
curriculum (6 stages, 15 modules, **all 79 lessons written**), Whop setup,
store listing, operations kit, 17 worksheets, funnel changes, video scripts
and the brand system. Read it fully before doing anything.

## Locked decisions (don't change them)
- Name: **On-Chain Operator Program**. Tagline: **From zero to your own on-chain bank.**
- Course tier **$15,000 one-time**. Live tier priced higher (not yet set).
- Launch to everyone; cold traffic goes **application → call → checkout**.
- 6 stages · 15 modules (0–14) · 79 lessons · 25 strategy playbooks · 2 capstones.
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
2. **Quality pass on all 79 lessons.** Check facts are current (products, networks, mechanisms), recompute every worked example, make sure every term is defined, and that each lesson follows the template. Return a change list, then the corrected lesson files in full.
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
Decisions answered · lessons quality-checked · sales page, application form,
Whop setup steps, funnel skill text, marketing pack and extra video cuts
delivered · final checklist written.
