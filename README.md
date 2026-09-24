# Grid Bot Builder + DeFi Program — Skills Archive

Claude skills for building and running the Grid Bot Builder business and the
new DeFi program on Whop. Everything lives in `.claude/skills/`, so Claude Code
loads these skills automatically in any session opened on this repo.

## Start here

Ask Claude: *"Use whop-defi-program to plan the DeFi program."* That skill
walks through offer → curriculum → Whop setup → funnel → guardrails → launch,
and calls the others as needed.

## On-Chain Operator Program
Everything for the DeFi program is in one file: [`ON-CHAIN-OPERATOR-PROGRAM.md`](programs/defi-program/ON-CHAIN-OPERATOR-PROGRAM.md), also as [Word](programs/defi-program/On-Chain-Operator-Program.docx) and [PDF](programs/defi-program/On-Chain-Operator-Program.pdf).
All 107 lessons and 15 Mastery Starters are written (topic map: `programs/defi-program/09-mastery-map.md`); VSLs and module intro videos are in [`programs/defi-program/video/`](programs/defi-program/video/).
To finish and launch it, paste [`programs/defi-program/BUILD-PROMPT.md`](programs/defi-program/BUILD-PROMPT.md) into Whop's AI (Grok 4.6) with the files it lists, or run it in Claude Code.

## Skills

### Your business skills (custom)
| Skill | What it does | Source |
|---|---|---|
| `whop-defi-program` | Master playbook: turn the 42-chapter DeFi module into a Whop product and wire it into the GBB funnel | New, built from Notion + Zapier |
| `defi-strategies` | 30 DeFi strategies in 7 levels (up to fixed-rate, basis, options, credit lines, hedged yield, CDP minting, bribe markets, perp vaults, arbitrage and rates), plus `defi_calc.py` with 20 calculators including income portfolios and a personal balance sheet | Notion strategy library, expanded |
| `defi-due-diligence` | 6-step protocol risk loop, before-signing checklist, logs to Notion tracker | Notion: DeFi & On-Chain module |
| `grid-bot-design` | Regime/range/spacing/fees/risk method + `grid_calc.py` calculator, logs to Notion checklist | Notion: Grid Bot Builder module |
| `gbb-new-lead` | Score, tag and email new leads | Zapier (archive copy) |
| `gbb-customer-onboarding` | Post-purchase onboarding + Elite Intel upsell | Zapier (archive copy) |
| `gbb-ad-performance` | Weekly CAC / ROAS / budget report | Zapier (archive copy) |
| `gbb-pipeline-check` | Funnel stages, rates, stale leads | Zapier (archive copy) |

### Course video production

Start with `course-video-director`: it runs the others in order and holds the definition of done.

| Skill | What it does |
|---|---|
| `course-video-director` | End-to-end lesson video: teach plan, storyboard, flows, screen demos, script, practice, QA, render |
| `instructional-design` | Objectives, misconceptions and the understand, see it, do it, check, teach it back arc |
| `visual-storyboard` | What's on screen every 8 to 20 seconds, and when to cut away to a flow, image, screen or worked number |
| `animated-flows` | `flow` scenes: mechanisms that animate as they're narrated, plus a library of DeFi and grid bot flows |
| `screen-demo-cutaways` | `capture_demo.js`: real app screenshots with highlight and blur boxes, turned into `cutaway` scenes |
| `lesson-script-writing` | Gold-format script JSON, narration written for the ear, full scene reference |
| `practice-and-assessment` | Quizzes that test understanding, worked examples that fade into "your turn", implementation tasks |
| `video-qa-review` | `lint_video_script.py`, test renders, frame checks, facts, numbers and compliance |

### Building blocks (from [anthropics/skills](https://github.com/anthropics/skills), Apache 2.0)
| Skill | Use it for |
|---|---|
| `mcp-builder` | Building an MCP server, e.g. to expose Grid Bot / DeFi tools to members' AI agents |
| `web-artifacts-builder` | Interactive tools, e.g. a DeFi Command Centre or grid simulator for the Whop app |
| `frontend-design` | Sales pages and course UI that don't look generic |
| `webapp-testing` | Playwright testing for anything you build |
| `skill-creator` | Writing, testing and improving new skills in this archive |

## Notes
- **Zapier is the source of truth** for the four `gbb-*` skills. This repo is
  public, so internal IDs (Mailchimp list, Whop business ID, plan IDs, owner
  email) are `<PLACEHOLDERS>`. To keep real values locally, put them in
  `config.local.md`, which git ignores.
- **Pricing conflict to resolve:** `gbb-ad-performance` still describes a
  "Grid Bot Starter" (A$47–97) and GBB at A$497. The newer skills say $997 and
  that there's no Starter tier.
- Provenance and licences: see `SOURCES.md`.
