#!/usr/bin/env python3
"""Gold-standard script for Lesson 2.3, Providing liquidity (~8-10 min).

Source: lessons/module-02-trading-on-chain.md, "Lesson 2.3 -- Providing
liquidity". Teaches: what you actually receive when you LP, why your token
mix changes (you become the counterparty to every trade), the fee-APR
formula, why to use 30-day average volume, and the real worked example
($10M TVL, $2M 30-day avg daily volume, 0.3% fee tier -> ~21.9% fee APR).

Uses flow3d (see .claude/skills/webgl-motion-graphics/SKILL.md) once, with
layout="column" -- a vertical single-file stack, distinct from the row
chain, branch/merge fan, and cycle ellipse used in the last three lessons.
And chart3d once, for the fee-APR sensitivity (baseline vs. volume halving
vs. TVL doubling -- both cut it to the same 10.95%, a real derived
consequence of the same formula, not a fabricated data point). That's this
skill's "at most one or two" ceiling.

Writes video-scripts/gold/lesson-02-3.json.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
S = []


def sc(type_, vo, cap=None, **k):
    d = {"type": type_, **k, "vo": vo}
    if cap:
        d["cap"] = cap
    S.append(d)


# ---------------------------------------------------------------- intro
sc("title", "Lesson two point three. Providing liquidity. By the end, you'll be able to estimate an L.P. position's fee income from real pool data, before you ever deposit.",
   "Lesson 2.3. Providing liquidity. By the end, you'll be able to estimate an LP position's fee income from real pool data, before you ever deposit.",
   chapter="Intro", eyebrow="Lesson 2.3", num="2.3", title="Providing liquidity", sub="You don't just earn fees. You become the counterparty to every trade.")
sc("pillars", "Here's the plan. First, what you actually receive when you provide liquidity, and what changes underneath you while you hold it. Second, the fee A.P.R. formula, with a real worked example. And third, the checklist to run before you deposit into any pool.",
   chapter="Intro", title="What this lesson covers",
   items=[{"icon": "wallet", "title": "What you get", "text": "A share, and a new exposure"},
          {"icon": "chart", "title": "Fee APR", "text": "The formula, worked with real numbers"},
          {"icon": "check", "title": "Checklist", "text": "Run it before you deposit"}])
sc("statement", "Providing liquidity is not a savings account. You're not just earning a fee for sitting still. You're the counterparty to every single trade that happens in that pool, whether the price moves in your favor or not.",
   chapter="Why it matters", kicker="What LPing actually is", lines=["Not a savings account.", "You're the counterparty to every trade."], sub="Whether the price moves in your favor or not.")

# ---------------------------------------------------------------- what you get
sc("title", "What you actually get.", chapter="What you get", eyebrow="What you get", num="1", title="What you actually get", sub="A share of the pool. And a new exposure.")
sc("bullets", "When you L.P., you deposit both tokens, and you receive a share of the pool back, a fungible token for a full-range position, or an N.F.T. for a concentrated one. You earn your share of every swap fee that pool collects. In return, your token mix changes as traders move the price: you become the counterparty to every trade that goes through.",
   chapter="What you get", title="What you actually get",
   items=["Deposit both tokens, receive a share back (token, or NFT if concentrated)",
          "Earn your share of every swap fee the pool collects",
          "Your token mix changes as traders move the price"])
sc("flow3d", "Here's that exchange, start to finish. You deposit both tokens into the pool. The pool issues you a position, representing your exact share. From that point on, you earn a slice of every swap fee that passes through. And as traders push the price around, your own token mix shifts underneath you, automatically, to match the pool's new ratio.",
   "Here's that exchange, start to finish. You deposit both tokens into the pool. The pool issues you a position, representing your exact share. From that point on, you earn a slice of every swap fee that passes through. And as traders push the price around, your own token mix shifts underneath you, automatically, to match the pool's new ratio.",
   chapter="What you get", title="Providing liquidity, start to finish", seed=23,
   nodes=[{"id": "deposit", "label": "You deposit both tokens", "sub": "Into the pool", "icon": "wallet"},
          {"id": "position", "label": "Pool issues your position", "sub": "A token, or an NFT if concentrated", "icon": "layers"},
          {"id": "fees", "label": "You earn a fee slice", "sub": "On every swap that passes through", "icon": "coins"},
          {"id": "shift", "label": "Your mix shifts", "sub": "As traders move the price", "icon": "chart", "tone": "warn"}],
   edges=[{"from": "deposit", "to": "position"}, {"from": "position", "to": "fees"}, {"from": "fees", "to": "shift"}])
sc("quiz", "Quick check. What do you actually receive when you deposit into a pool? [[pause 4]] The answer: a share of the pool, a fungible token for a full-range position, or an N.F.T. representing a concentrated one.",
   n=1, of=3, q="What do you receive when you deposit into a pool?", a="A share of the pool: a token (full-range) or an NFT (concentrated).", chapter="What you get")

# ---------------------------------------------------------------- fee apr
sc("title", "The fee A.P.R. formula.", "The fee APR formula.", chapter="Fee APR", eyebrow="Fee APR", num="2", title="The fee APR formula", sub="One formula. Real numbers. No guessing.")
sc("bullets", "Here's the formula. Fee A.P.R. is approximately daily volume, times the fee tier, times your pool share, times three sixty five, divided by your deposit. For a full-range pool, your share is just your deposit divided by the pool's total value locked. That simplifies the formula to daily volume, times fee tier, times three sixty five, divided by T.V.L. And use a thirty day average volume, never today's. A single volatile day overstates your income, and that same volatile day is exactly when you take the most impermanent loss.",
   chapter="Fee APR", title="Fee APR ≈ daily volume × fee tier × 365 ÷ TVL",
   items=["Full formula: (volume × fee tier × your share × 365) ÷ your deposit",
          "Full-range simplifies to: daily volume × fee tier × 365 ÷ TVL",
          "Use a 30-day average volume — a spike day overstates income, and coincides with peak IL"])
sc("steps", "Work it through on a real pool. T.V.L. ten million dollars. Thirty day average daily volume, two million dollars. Fee tier, zero point three percent. Daily pool fees: two million times zero point zero zero three, six thousand dollars. Your ten thousand dollar deposit is zero point one percent of that T.V.L. Your share of today's fees: six dollars a day. Annualized, that's about twenty one point nine percent fee A.P.R., before impermanent loss and gas.",
   chapter="Fee APR", title="Worked example: $10,000 into a $10M pool",
   steps=["Pool: $10M TVL, 30-day avg daily volume $2M, fee tier 0.3%", "Daily pool fees: $2M × 0.003 = $6,000",
          "Your share: $10,000 ÷ $10M = 0.1%", "Your fees: $6,000 × 0.1% = $6/day"],
   result="≈21.9% fee APR — before impermanent loss and gas")
sc("chart3d", "Now watch what moves that number. Same pool, volume halves to one million a day: your fee A.P.R. halves too, to about ten point nine five percent. Or T.V.L. doubles to twenty million, with volume unchanged: your share shrinks, and your fee A.P.R. lands at exactly the same ten point nine five percent. Either one, on its own, cuts your fee income in half.",
   "Now watch what moves that number. Same pool, volume halves to $1M a day: your fee APR halves too, to about 10.95%. Or TVL doubles to $20M, with volume unchanged: your share shrinks, and your fee APR lands at exactly the same 10.95%. Either one, on its own, cuts your fee income in half.",
   chapter="Fee APR", kind="bars", title="What cuts your fee APR in half", sub="Same $10,000 position, one variable changes at a time", seed=223,
   bars=[{"label": "Baseline", "text": "$10M TVL, $2M volume", "value": 21.9, "show": "≈21.9%", "tone": "good"},
         {"label": "Volume halves", "text": "$10M TVL, $1M volume", "value": 10.95, "show": "≈10.95%", "tone": "warn"},
         {"label": "TVL doubles", "text": "$20M TVL, $2M volume", "value": 10.95, "show": "≈10.95%", "tone": "warn"}], max=21.9)
sc("quiz", "Quick check. A pool holds five million dollars T.V.L., one million a day in volume, a zero point zero five percent fee tier. What's the full-range fee A.P.R.? [[pause 4]] The answer: one million, times zero point zero zero zero five, times three sixty five, divided by five million, is three point six five percent.",
   n=2, of=3, q="Pool: $5M TVL, $1M daily volume, 0.05% fee. Full-range fee APR?", a="1,000,000 × 0.0005 × 365 ÷ 5,000,000 = 3.65%.", chapter="Fee APR")
sc("quiz", "Last check for this section. Why use a thirty day average volume instead of today's? [[pause 4]] The answer: a single volatile day overstates your fee income, and that same volatile day is exactly when you take the most impermanent loss.",
   n=3, of=3, q="Why use 30-day average volume instead of today's?", a="A single volatile day overstates income, and coincides with peak impermanent loss.", chapter="Fee APR")

# ---------------------------------------------------------------- pitfalls
sc("title", "Where L.P.s actually lose money.", "Where LPs actually lose money.", chapter="Where LPs lose money", eyebrow="Where LPs lose money", num="3", title="Where LPs actually lose money", sub="Four habits that quietly erase the fee income.")
sc("bullets", "Here's how people lose on this even after doing the math once. Chasing the single highest-A.P.R. pool listed anywhere, without checking whether that yield comes from real trading volume or from a temporary incentive that ends. Assuming fees always cover impermanent loss, they often don't, especially in a fast-moving market. Never recording entry prices, so there's no honest vs-hold comparison to catch a bad position. And panic-withdrawing after one rough day instead of following the exit rule written in advance.", check=False,
   chapter="Where LPs lose money", title="Where LPs actually lose money",
   items=["Chasing the highest listed APR without checking if it's real volume or a temporary incentive",
          "Assuming fees always cover impermanent loss (they often don't)",
          "Never recording entry prices, so there's no honest vs-hold comparison",
          "Panic-withdrawing after one rough day instead of following the written exit rule"])

# ---------------------------------------------------------------- checklist
sc("title", "Before you deposit.", chapter="Checklist", eyebrow="Checklist", num="4", title="Before you deposit", sub="Four checks, on any pool.")
sc("bullets", "Run this before you deposit into any pool. Calculate fee A.P.R. from thirty day volume, not today's. Confirm you'd genuinely be okay holding one hundred percent of either token, since that's the real downside case. Record your entry prices, so you have a real vs-hold benchmark later. And write your exit rule now: volume drops, a trend starts, or fees stop covering impermanent loss.",
   chapter="Checklist", title="Before you deposit",
   items=["Fee APR calculated from 30-day volume, not today's", "You're OK holding 100% of either token",
          "Entry prices recorded, for a real vs-hold benchmark", "Exit rule written: volume drops, trend starts, or fees stop covering IL"])

# ---------------------------------------------------------------- your turn
sc("statement", "Your turn, five to ten minutes. Pick a real pool. Pull its T.V.L. and thirty day average volume, and work out your fee A.P.R. for a deposit size you'd actually make, before you ever click confirm.",
   "Your turn, 5 to 10 minutes. Pick a real pool. Pull its TVL and 30-day average volume, and work out your fee APR for a deposit size you'd actually make, before you ever click confirm.",
   chapter="Your turn", kicker="Your turn", lines=["Pick a real pool.", "Work out your real fee APR."], sub="5 to 10 minutes, before you ever click confirm.")
sc("bullets", "To recap: providing liquidity means depositing both tokens and becoming the counterparty to every trade, not just collecting a fee. Fee A.P.R. is daily volume, times fee tier, times three sixty five, divided by T.V.L., always from a thirty day average. And either volume halving or T.V.L. doubling cuts your fee income in half.",
   "To recap: providing liquidity means depositing both tokens and becoming the counterparty to every trade, not just collecting a fee. Fee APR is daily volume, times fee tier, times 365, divided by TVL, always from a 30-day average. And either volume halving or TVL doubling cuts your fee income in half.",
   chapter="Recap", title="Three things to remember",
   items=["You're the counterparty to every trade, not just a fee collector", "Fee APR = daily volume × fee tier × 365 ÷ TVL, from a 30-day average",
          "Volume halving or TVL doubling both cut your fee income in half"])
sc("cta", "That's providing liquidity. Next up, lesson two point four: impermanent loss, and your L.P. position's true profit and loss against simply holding.",
   "That's providing liquidity. Next up, Lesson 2.4: impermanent loss, and your LP position's true profit and loss against simply holding.",
   chapter="Recap", button="Next: Lesson 2.4", sub="Impermanent loss & true LP P&L · Educational content only · Not financial advice")

video = {
    "id": "lesson-02-3",
    "title": "Lesson 2.3: Providing liquidity",
    "size": [1920, 1080],
    "group": "lessons",
    "maxMinutes": 25,
    "tag": "Lesson 2.3",
    "gold": True,
    "seed": 23,
    "use": "Lesson 2.3 page in the Whop course. Hand-written gold-standard script: what an LP position actually is, the fee-APR formula, why to use 30-day average volume, and the real $10M TVL / $2M volume / 0.3% fee worked example (~21.9% fee APR) with its sensitivity (volume halving or TVL doubling both cut it to ~10.95%). Facts last checked: 2026-09-26.",
    "thumbnail": {"title": "Fee APR, worked out", "subtitle": "Lesson 2.3"},
    "scenes": S,
}

out = ROOT / "video-scripts" / "gold" / "lesson-02-3.json"
out.write_text(json.dumps(video, indent=None))
print(f"wrote {out} ({len(S)} scenes)")
