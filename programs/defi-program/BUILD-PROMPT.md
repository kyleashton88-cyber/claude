# Build Prompt: On-Chain Operator Program

**Run it in:** Claude Code (claude.ai/code, the desktop app or the CLI) with
the GitHub repo `kyleashton88-cyber/claude` open on branch
`claude/grid-bot-builder-skills-bmrez2`. Connect **Notion** and **Zapier**,
and make sure **Whop is connected inside Zapier**. Claude Code loads the
skills in `.claude/skills/` automatically. Other AIs won't, and they can't
reach your Notion or Zapier, so use Claude Code.

Paste everything below the line as your first message.

---

You're building out my **On-Chain Operator Program**, a high-ticket DeFi
education product that goes into my Whop store as a new product alongside
Grid Bot Builder. Work in this repo on branch
`claude/grid-bot-builder-skills-bmrez2`. Commit and push after each finished piece.

## Read first
1. `README.md` (skills archive) and `programs/defi-program/README.md` (build status)
2. `programs/defi-program/ON-CHAIN-OPERATOR-PROGRAM.md`: master file with decisions, curriculum, setup, funnel and finished lessons
3. `programs/defi-program/06-whop-store-listing.md`: store listing copy and image upload map
4. Skills: `whop-defi-program` (master workflow), `defi-strategies`, `defi-due-diligence`, `grid-bot-design`, `gbb-*`, `frontend-design`, `dataviz`
5. Notion: "ATLAS — The Universal Trading Library" → "DeFi & On-Chain (Complete Module)". This is the source for every lesson.

## Locked decisions (don't change them)
- Name: On-Chain Operator Program. Course tier $15,000 one-time. Live tier priced higher.
- Launch to everyone. Cold traffic goes application → call (vip-defi-consult Calendly) → checkout.
- 9 modules, 45 lessons. Every lesson follows: Objective → Explanation → Worked example → Checklist → 3-question quiz.

## Imagery standard (every deliverable must meet it)
All images come from one generator, `programs/defi-program/export/build_images.js`,
so the brand stays consistent. Extend that file and don't hand-place one-off images.
- **Brand:** Inter typeface (bundled via `@fontsource`). Navy `#0B1F33`→`#12355B` gradient with a faint node-network motif for dark/store images. `#FCFCFB` surface for light document images. Teal `#2ee6a6` accent on dark only.
- **Charts:** follow the `dataviz` skill. Blue `#2a78d6` is the primary series, orange `#eb6834` the secondary (validated pair). One y-axis. Recessive grid. Direct labels on the empty side of the line, never overlapping. Every number must be computed, not typed.
- **Resolution:** document images at 2× (1800 px wide), store images at exact upload size (1024×1024, 1920×1080).
- **Every module** gets its banner (`assets/modules/module-0N.png`, already rendered for 1–9) at the top of its lesson file. **Every lesson** gets at least one diagram or chart where a picture explains the mechanism better than text (a flow, a curve, a comparison). Add new ones to the `ASSETS` list.
- **Review:** after rendering, open every new or changed image and check it by eye. Fix any label collision, overflow, clipped text or empty-looking layout before committing.
- Every image carries the footer "Educational content only · Not financial advice · No results are guaranteed" (the shells already do this).

## Work to do, in order
1. **Write the remaining 30 lessons**: Modules 3, 4, 5, 6, 7 and lessons 8.1, 8.2, 8.4, one file per module in `programs/defi-program/lessons/`, matching the style of `module-01-…` and `module-02-…`, with module banner + lesson imagery per the standard above. Check every number with `.claude/skills/defi-strategies/scripts/defi_calc.py` or Python. Add a practical at the end of each module. Suggested new visuals: health-factor gauge (M3), APY decomposition bar (M4), bridge/oracle dependency map (M5), due-diligence scorecard (M6), exchange-flow and holder-metric examples (M7), portfolio risk buckets (M8).
2. **Capstone brief and grading rubric** (due-diligence file + position plan with sizing, monitoring triggers and exact unwind), with a one-page visual overview.
3. **Live tier**: design what it includes (session cadence, capstone reviews, portfolio reviews, Q&A), then propose a price and wait for my approval. Update the "What's included" gallery image once it's priced.
4. **Application form** (questions + scoring that plugs into `gbb-new-lead` with interest = defi) and a **sales call script**.
5. **Sales page**: build it with the `frontend-design` skill using the store images, the copy in `06-whop-store-listing.md`, and the brand above.
6. **Add the product to my Whop store** per `05-whop-setup.md` and `06-whop-store-listing.md`. I create the hidden product in the dashboard and upload the images in the listed order, then give you the `prod_` ID. You create plans and checkout links through Zapier, but only after showing me the exact values.
7. **Funnel**: apply `04-funnel-changes.md` to my Zapier skills (`update_zapier_skill`) after I approve, and mirror the changes into `.claude/skills/gbb-*`.
8. **Rebuild everything and push**: `python3 programs/defi-program/build_master.py`, then `cd programs/defi-program/export && npm install && npm run build` (renders all images, then the Word and PDF copies). Open the PDF and spot-check pages that have images.

## Rules
- Educational only. No promised, projected or guaranteed returns anywhere: lessons, images, emails, sales page, store listing or call script. Always show how a strategy loses money next to how it earns.
- Never ask for seed phrases, private keys or exchange API keys.
- No Discord, Skool or Slack. Use only the Calendly links named in the skills.
- Ask me before anything outward-facing: creating or changing anything on Whop, sending emails, editing Zapier skills, changing prices.
- This repo is public. Never commit internal IDs (Mailchimp list, Whop business or plan IDs, private emails). Use `<PLACEHOLDERS>`.
- Still open, ask me: live-tier price, refund policy, Grid Bot Builder customer pricing, whether the "Grid Bot Starter" tier exists.

## Done when
- All 45 lessons and the capstone are written, number-checked and illustrated to the imagery standard.
- Live tier, application, call script and sales page are approved.
- The product is in my Whop store (hidden until I say launch) with icon, banner and gallery images, and its plans and checkout links exist.
- Funnel skills are updated in Zapier and the repo.
- The master file, Word and PDF are rebuilt and pushed.
