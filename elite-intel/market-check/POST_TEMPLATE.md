# Elite Intel Market Check: post template (future posts only)
# v2 — 10 Nov 2026, Stewart-approved: lead with what changed, slim level lines, one funding line, no filename line, CPI/events only under Coming up.
# 22 Nov 2026, 6:10pm AEDT: Stewart approved screen tweaks D and F. See research/SCREEN.md and research/screen.py.

Target length is 300 to 400 words (hard ceiling 450). Fill every {placeholder}. Render the charts from the same snapshot the text quotes. Use one as-of time across the text and all 3 images.

---

**Market Check · {Day DD Mon} {AM/PM} · as of {h:mm am/pm} Sydney time**

G'day Elite crew,

**What changed since last check**
{Two to four sentences of factual changes only: price vs the example range, any level that broke or held, funding flip, ETF flow change, on-chain change. Name an exchange only if an event there directly affects a covered coin. Otherwise stay exchange-neutral.}

**Mood:** {One or two plain sentences. **Fear & Greed {value} ({label})**. Funding {mostly positive/negative/mixed}; see market.png. **ETF net flows {date}: BTC {±US$M}, ETH {±US$M}** (say plainly if this is not the previous US trading day). Describe only, no predictions.}

**Big four (example levels; full ranges on big-four.png)**
- BTC ${price}: {inside / above / below} its example range; example invalidation {unchanged / moved to ${stop}}.
- ETH ${price}: same one-line format.
- SOL ${price}: same one-line format.
- XRP ${price}: same one-line format.
- If a big-four coin's latest completed daily close is below its example invalidation, do not reprint the old example range. Write: "{COIN} ${price}: range not active. The latest completed daily close is below the example invalidation, so the previous example range is not in play." You may still give the live price. The label stays until price closes back inside or the levels are re-selected. Keep "example" wording. Education only. Not financial advice.

**Coins watched (example levels; full ranges on watched.png)**
- {COIN} ${price}: one line in the same format. If outside the range, add "this describes where price is, not a signal."
- {COIN}: one line.
- {COIN}: one line.
- If BTC itself is trending (30-day win() drift30 > 1.0 and ADX14 > 35), publish no rotation picks. Use the empty-state watched card and say no coin cleared the screen (market-regime gate F). The same empty-state applies when every candidate fails gate D (drift30 > 0.8 and ADX14 > 40, or less than about 8% above its example stop).

**On-chain:** {One or two sentences, only if something changed (e.g. watched cluster size, TVL). Otherwise "No notable on-chain change."}

**Coins screened:** {N} coins checked against {criteria, one line}. {Name any coin that moved onto or off the list, with one short reason.}

**News worth knowing**
- {New headline, one line, source}. Covered coins only; skip weakly related stories.
- {New headline, one line, source}.

**Coming up:** {Official scheduled events in Sydney time, one line, e.g. US CPI. Do not repeat these in News.}

New here? The pinned guide explains example ranges, example invalidation, funding, ETF flows and how to read these charts.

Stay disciplined and size sensibly.
Stewart

Example levels only. Education only. Not financial advice.

---

## Checklist before posting (draft stage)
- Word count 300–400 (max 450), excluding this checklist.
- "What changed" is the first section after the greeting.
- One as-of time. Text numbers match the image numbers.
- Bold only the as-of line, Fear & Greed and the ETF date/print, not every price.
- Funding is one sentence pointing to market.png; no per-coin funding list.
- No image filename line.
- Every level says "example". No profit, win-rate or income claims. No predictions.
- A big-four coin whose latest completed daily close is below its example invalidation is labelled "range not active"; the old example range is not reprinted as a live example.
- Rotation picks use the live screen in research/screen.py (gates D and F). Do not hand-pick coins that the screen dropped.
- No how-to steps or glossary. Those belong in the pinned guide.
- Exchange names only where a covered coin is directly affected.
- Scheduled events appear only under Coming up.

