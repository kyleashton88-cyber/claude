#!/usr/bin/env python3
"""Gold-standard script for Lesson 2.5, MEV and protecting your trades (~8-10 min).

Source: lessons/module-02-trading-on-chain.md, "Lesson 2.5 -- MEV and
protecting your trades". Teaches: what MEV is, the sandwich-attack
mechanism, why your own slippage tolerance is the attacker's profit
ceiling, the real defences, and the worked example ($20,000 swap: 3%
slippage exposes ~$600, 0.5% exposes ~$100, a protected route isn't
visible in the public mempool at all).

Uses flow3d (see .claude/skills/webgl-motion-graphics/SKILL.md) once, for
the sandwich-attack sequence itself, styled with tone="bad" throughout
since this is the one mechanism in the course told from an attacker's
perspective -- a genuine tonal shift from every prior lesson's neutral
flows, not just a different topology. And chart3d once, for the
slippage-vs-exposure worked example. That's this skill's "at most one or
two" ceiling.

Writes video-scripts/gold/lesson-02-5.json.
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
sc("title", "Lesson two point five. M.E.V. and protecting your trades. By the end, you'll be able to set slippage and routing so your trades aren't easy targets.",
   "Lesson 2.5. MEV and protecting your trades. By the end, you'll be able to set slippage and routing so your trades aren't easy targets.",
   chapter="Intro", eyebrow="Lesson 2.5", num="2.5", title="MEV and protecting your trades", sub="One setting on your screen is also a profit ceiling for someone else.")
sc("pillars", "Here's the plan. First, what M.E.V. actually is, and the specific attack that targets your trades. Second, the real defences, with a worked example showing exactly what they're worth. And third, the checklist to run before any large swap.",
   chapter="Intro", title="What this lesson covers",
   items=[{"icon": "bot", "title": "The sandwich attack", "text": "How it actually works"},
          {"icon": "shield", "title": "Real defences", "text": "What they're worth, in dollars"},
          {"icon": "check", "title": "Checklist", "text": "Run it before any large swap"}])
sc("statement", "Your slippage tolerance is not just a safety setting. On a pending trade, it's also the profit ceiling for whoever is watching that trade in the mempool.",
   chapter="Why it matters", kicker="One number, two jobs", lines=["Your slippage tolerance.", "Also an attacker's profit ceiling."], sub="Set carelessly, it protects you and pays them at the same time.")

# ---------------------------------------------------------------- what MEV is
sc("title", "What M.E.V. actually is.", "What MEV actually is.", chapter="What MEV is", eyebrow="What MEV is", num="1", title="What MEV actually is", sub="Some of it is harmless. One kind targets you directly.")
sc("bullets", "M.E.V., maximal extractable value, is profit taken by whoever controls the order transactions land in inside a block. Some of it is harmless, arbitrage that simply realigns prices across venues. The kind that hurts you is a sandwich attack. A bot sees your pending swap, buys just before you, pushing the price up. It lets your trade execute at that worse price, then sells right after.",
   chapter="What MEV is", title="MEV, and the attack that targets you",
   items=["MEV: profit from controlling transaction order in a block", "Some MEV is harmless (arbitrage realigning prices)",
          "Sandwich attack: buys before you, lets you execute worse, sells after"])
sc("flow3d", "Watch a sandwich attack happen, step by step. A bot watches the public mempool and sees your pending swap before it's confirmed. It buys first, in front of you, pushing the price up. Your trade executes right after, at that now-worse price, exactly what your slippage tolerance allowed. And the bot sells immediately after you, pocketing the difference. Your slippage tolerance was its profit ceiling the entire time.",
   "Watch a sandwich attack happen, step by step. A bot watches the public mempool and sees your pending swap before it's confirmed. It buys first, in front of you, pushing the price up. Your trade executes right after, at that now-worse price, exactly what your slippage tolerance allowed. And the bot sells immediately after you, pocketing the difference. Your slippage tolerance was its profit ceiling the entire time.",
   chapter="What MEV is", title="A sandwich attack, step by step", seed=25,
   nodes=[{"id": "see", "label": "Bot sees your pending swap", "sub": "Watching the public mempool", "icon": "bot", "tone": "bad"},
          {"id": "front", "label": "Bot buys first", "sub": "Pushes the price up, in front of you", "icon": "chart", "tone": "bad"},
          {"id": "you", "label": "Your trade executes", "sub": "At the worse price your slippage allowed", "icon": "wallet", "tone": "bad"},
          {"id": "sell", "label": "Bot sells right after", "sub": "Pockets the difference", "icon": "coins", "tone": "bad"}],
   edges=[{"from": "see", "to": "front", "tone": "bad"}, {"from": "front", "to": "you", "tone": "bad"}, {"from": "you", "to": "sell", "tone": "bad"}])
sc("quiz", "Quick check. What actually limits how much a sandwich bot can take from your trade? [[pause 4]] The answer: your slippage tolerance, and the pool's depth.",
   n=1, of=3, q="What limits how much a sandwich bot can take?", a="Your slippage tolerance (and the pool's depth).", chapter="What MEV is")

# ---------------------------------------------------------------- defences
sc("title", "Real defences.", chapter="Defences", eyebrow="Defences", num="2", title="Real defences", sub="Four habits. What they're actually worth.")
sc("bullets", "Here are the real defences. Set a tight but realistic slippage, zero point one to zero point five percent for liquid majors, wider only when you understand exactly why. Use M.E.V.-protected or private transaction routing, many wallets and aggregators offer it. Split large trades instead of broadcasting one huge swap. And avoid thin pools entirely for size that matters.",
   chapter="Defences", title="Real defences",
   items=["Tight but realistic slippage: 0.1–0.5% for liquid majors", "MEV-protected or private transaction routing",
          "Split large trades instead of one broadcast swap", "Avoid thin pools for size that matters"])
sc("steps", "Here's exactly where those dollar figures come from. Swap size, twenty thousand dollars. At three percent slippage tolerance, the maximum value at risk is twenty thousand times zero point zero three, six hundred dollars. Tighten that to zero point five percent, and it's twenty thousand times zero point zero zero five, one hundred dollars. Your slippage percentage, times your trade size, is quite literally the sandwich's profit ceiling.",
   chapter="Defences", title="Where the exposure numbers come from",
   steps=["Swap size: $20,000", "At 3% slippage: $20,000 × 0.03 = $600 max at risk",
          "At 0.5% slippage: $20,000 × 0.005 = $100 max at risk"],
   result="Slippage % × trade size = the sandwich's profit ceiling")
sc("chart3d", "Put real numbers on it. Swapping twenty thousand dollars: at three percent slippage tolerance, a sandwich can take up to around six hundred dollars. Tighten that to zero point five percent, and its ceiling drops to around one hundred dollars. Route it privately or protected instead, and the transaction is never visible in the public mempool at all, so it can't be sandwiched from there.",
   "Swapping $20,000: at 3% slippage tolerance, a sandwich can take up to around $600. Tighten that to 0.5%, and its ceiling drops to around $100. Route it privately or protected instead, and the transaction is never visible in the public mempool at all, so it can't be sandwiched from there.",
   chapter="Defences", kind="bars", title="Swapping $20,000: sandwich exposure by defence", sub="What a sandwich bot could take, before its own costs", seed=225,
   bars=[{"label": "3% slippage", "text": "Wide open", "value": 600, "show": "~$600", "tone": "bad"},
         {"label": "0.5% slippage", "text": "Tightened", "value": 100, "show": "~$100", "tone": "warn"},
         {"label": "Protected route", "text": "Not in the public mempool", "value": 5, "show": "~$0", "tone": "good"}], max=600)
sc("quiz", "Quick check. Why not just set slippage as close to zero as possible? [[pause 4]] The answer: normal, ordinary price movement will make the transaction revert, and a failed transaction still costs you gas.",
   n=2, of=3, q="Why not set slippage near zero?", a="Normal price movement makes the transaction revert, and you still pay gas.", chapter="Defences")
sc("statement", "Too tight a tolerance, say zero point zero five percent on a volatile pair, just makes the transaction fail. And a failed transaction still costs gas, exactly what lesson one point two already warned you about.",
   "Too tight a tolerance, say 0.05% on a volatile pair, just makes the transaction fail. And a failed transaction still costs gas, exactly what Lesson 1.2 already warned you about.",
   chapter="Defences", kicker="Too tight has a real cost too", lines=["Too tight just fails the transaction.", "And failed transactions still cost gas."], sub="Exactly what Lesson 1.2 already warned you about.")
sc("quiz", "Last check for this section. Name two real M.E.V. defences. [[pause 4]] The answer: any two of these, tight slippage, private or protected routing, splitting large trades, or using deep pools.",
   n=3, of=3, q="Name two MEV defences.", a="Any two: tight slippage, private/protected routing, splitting trades, or using deep pools.", chapter="Defences")

# ---------------------------------------------------------------- pitfalls
sc("title", "Where this protection breaks down.", chapter="Where this breaks down", eyebrow="Where this breaks down", num="3", title="Where this protection breaks down", sub="Four habits that quietly undo it.")
sc("bullets", "Here's how people undo these defences without realizing it. Using the exact same slippage setting for every trade, regardless of how volatile or thin that specific pair actually is. Assuming an app's protected-routing feature is automatically on, when it often has to be switched on per transaction. Treating protected routing as total M.E.V. immunity, when other extraction methods beyond the classic sandwich can still exist. And ignoring pool depth entirely, watching only the slippage percentage, when a thin pool makes any slippage setting less protective.", check=False,
   chapter="Where this breaks down", title="Where this protection breaks down",
   items=["Using the same slippage setting for every pair, regardless of its volatility",
          "Assuming protected routing is on by default, when it's often per-transaction",
          "Treating protected routing as total MEV immunity", "Ignoring pool depth and watching only the slippage percentage"])

# ---------------------------------------------------------------- checklist
sc("title", "Before any large swap.", chapter="Checklist", eyebrow="Checklist", num="4", title="Before any large swap", sub="Three checks, every time.")
sc("bullets", "Run this before any large swap. Slippage set specifically for this pair and this size, never left sitting at a high default. Protected routing switched on for anything sizeable. And large orders either split, or routed through genuinely deep liquidity.",
   chapter="Checklist", title="Before any large swap",
   items=["Slippage set for this pair and size, never a high default", "Protected routing on for larger swaps",
          "Large orders split, or routed through deep liquidity"])

# ---------------------------------------------------------------- your turn
sc("statement", "Your turn, five minutes. Open your wallet or aggregator's slippage setting right now, and check what it's actually set to. If it's sitting at a high default, fix it before your next real trade.",
   "Your turn, 5 minutes. Open your wallet or aggregator's slippage setting right now, and check what it's actually set to. If it's sitting at a high default, fix it before your next real trade.",
   chapter="Your turn", kicker="Your turn", lines=["Check your slippage setting.", "Fix it if it's a high default."], sub="5 minutes, before your next real trade.")
sc("bullets", "To recap: M.E.V. is profit from controlling transaction order, and a sandwich attack specifically targets your pending trade, using your own slippage tolerance as its ceiling. Tight but realistic slippage, protected routing, and splitting large trades are real, measurable defences. And too tight a tolerance just fails the transaction, costing you gas for nothing.",
   "To recap: MEV is profit from controlling transaction order, and a sandwich attack specifically targets your pending trade, using your own slippage tolerance as its ceiling. Tight but realistic slippage, protected routing, and splitting large trades are real, measurable defences. And too tight a tolerance just fails the transaction, costing you gas for nothing.",
   chapter="Recap", title="Three things to remember",
   items=["A sandwich attack uses your own slippage tolerance as its profit ceiling", "Tight-but-realistic slippage and protected routing are real, measurable defences",
          "Too tight a tolerance just fails the transaction, costing gas for nothing"])
sc("cta", "That's M.E.V. and protecting your trades. Next up, lesson two point six: advanced execution, limit, T.W.A.P. and intent-based orders.",
   "That's MEV and protecting your trades. Next up, Lesson 2.6: advanced execution, limit, TWAP and intent-based orders.",
   chapter="Recap", button="Next: Lesson 2.6", sub="Advanced execution · Educational content only · Not financial advice")

video = {
    "id": "lesson-02-5",
    "title": "Lesson 2.5: MEV and protecting your trades",
    "size": [1920, 1080],
    "group": "lessons",
    "maxMinutes": 25,
    "tag": "Lesson 2.5",
    "gold": True,
    "seed": 25,
    "use": "Lesson 2.5 page in the Whop course. Hand-written gold-standard script: what MEV is, the sandwich-attack mechanism, why slippage tolerance is the attacker's profit ceiling, real defences, and the real $20,000 worked example (3% slippage exposes ~$600, 0.5% exposes ~$100, a protected route isn't visible in the public mempool at all). Facts last checked: 2026-09-26.",
    "thumbnail": {"title": "Your slippage is their ceiling", "subtitle": "Lesson 2.5"},
    "scenes": S,
}

out = ROOT / "video-scripts" / "gold" / "lesson-02-5.json"
out.write_text(json.dumps(video, indent=None))
print(f"wrote {out} ({len(S)} scenes)")
