# Build Prompt: On-Chain Operator Program

**Run it in:** Claude Code (claude.ai/code, the desktop app or the CLI) with
the GitHub repo `kyleashton88-cyber/claude` open. Connect **Notion** and
**Zapier**, and make sure **Whop is connected inside Zapier**. Claude Code
loads the skills in `.claude/skills/` automatically. Other AIs won't, and
they can't reach your Notion or Zapier, so use Claude Code.

Paste everything below the line as your first message.

---

You're building out my **On-Chain Operator Program**, a high-ticket DeFi
education product sold on Whop alongside my Grid Bot Builder business. Work
in this repo on branch `claude/grid-bot-builder-skills-bmrez2`. Commit and
push after each finished piece.

## Read first
1. `README.md` (skills archive) and `programs/defi-program/README.md` (build status)
2. `programs/defi-program/ON-CHAIN-OPERATOR-PROGRAM.md` (master file: decisions, curriculum, setup, funnel, finished lessons)
3. Skills: `whop-defi-program` (master workflow), `defi-strategies`, `defi-due-diligence`, `grid-bot-design`, `gbb-*`
4. Notion: "ATLAS — The Universal Trading Library" → "DeFi & On-Chain (Complete Module)". This is the source for every lesson.

## Locked decisions (don't change them)
- Name: On-Chain Operator Program. Course tier $15,000 one-time. Live tier priced higher.
- Launch to everyone. Cold traffic goes application → call (vip-defi-consult Calendly) → checkout.
- 9 modules, 45 lessons. Every lesson follows: Objective → Explanation → Worked example → Checklist → 3-question quiz.

## Work to do, in order
1. **Write the remaining 30 lessons**: Modules 3, 4, 5, 6, 7 and lessons 8.1, 8.2, 8.4, one file per module in `programs/defi-program/lessons/`, matching the style of `module-01-…` and `module-02-…`. Check every number in the worked examples with `.claude/skills/defi-strategies/scripts/defi_calc.py` or Python. Add a practical at the end of each module.
2. **Capstone brief and grading rubric** (due-diligence file + position plan with sizing, monitoring triggers and exact unwind).
3. **Live tier**: design what it includes (session cadence, capstone reviews, portfolio reviews, Q&A), then propose a price and wait for my approval.
4. **Application form** (questions + scoring that plugs into `gbb-new-lead` with interest = defi) and a **sales call script**.
5. **Sales page copy**: use the `frontend-design` skill if you build it as a page.
6. **Whop setup** per `05-whop-setup.md`: I create the product in the dashboard and give you the `prod_` ID. You create plans and checkout links through Zapier, but only after showing me the exact values.
7. **Funnel**: apply `04-funnel-changes.md` to my Zapier skills (`update_zapier_skill`) after I approve, and mirror the changes into `.claude/skills/gbb-*`.
8. Regenerate the master file with `python3 programs/defi-program/build_master.py` and push.

## Rules
- Educational only. No promised, projected or guaranteed returns anywhere: lessons, emails, sales page or call script. Always show how a strategy loses money next to how it earns.
- Never ask for seed phrases, private keys or exchange API keys.
- No Discord, Skool or Slack. Use only the Calendly links named in the skills.
- Ask me before anything outward-facing: creating or changing anything on Whop, sending emails, editing Zapier skills, changing prices.
- This repo is public. Never commit internal IDs (Mailchimp list, Whop business or plan IDs, private emails). Use `<PLACEHOLDERS>`.
- Still open, ask me: live-tier price, refund policy, Grid Bot Builder customer pricing, whether the "Grid Bot Starter" tier exists.

## Done when
All 45 lessons and the capstone are written and number-checked. Live tier,
application, call script and sales page are approved. Whop plans and
checkout links are live (hidden until I say launch). Funnel skills are
updated in Zapier and the repo. The master file is regenerated and pushed.
