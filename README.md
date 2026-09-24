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
To finish building it, paste [`programs/defi-program/BUILD-PROMPT.md`](programs/defi-program/BUILD-PROMPT.md) into Claude Code.

## Skills

### Your business skills (custom)
| Skill | What it does | Source |
|---|---|---|
| `whop-defi-program` | Master playbook: turn the 42-chapter DeFi module into a Whop product and wire it into the GBB funnel | New, built from Notion + Zapier |
| `defi-strategies` | 16 DeFi strategies: where each return comes from, the maths, execution, kill rules, plus the `defi_calc.py` calculator | Notion strategy library, expanded |
| `defi-due-diligence` | 6-step protocol risk loop, before-signing checklist, logs to Notion tracker | Notion: DeFi & On-Chain module |
| `grid-bot-design` | Regime/range/spacing/fees/risk method + `grid_calc.py` calculator, logs to Notion checklist | Notion: Grid Bot Builder module |
| `gbb-new-lead` | Score, tag and email new leads | Zapier (archive copy) |
| `gbb-customer-onboarding` | Post-purchase onboarding + Elite Intel upsell | Zapier (archive copy) |
| `gbb-ad-performance` | Weekly CAC / ROAS / budget report | Zapier (archive copy) |
| `gbb-pipeline-check` | Funnel stages, rates, stale leads | Zapier (archive copy) |

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
