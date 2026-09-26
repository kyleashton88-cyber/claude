#!/usr/bin/env python3
"""Gold-standard script for Lesson 2.1, DEXs, aggregators & routing (~9-11 minutes).

Source: lessons/module-02-trading-on-chain.md, "Lesson 2.1 -- DEXs, aggregators
& routing". Teaches: AMM DEX vs. on-chain order book vs. aggregator, price
impact, slippage tolerance, routing, the net-output formula, and the real
worked example (20 ETH sale: aggregator wins by ~$308; 0.5 ETH sale: direct
pool wins because gas eats the improvement).

Uses flow3d (see .claude/skills/webgl-motion-graphics/SKILL.md) once, for the
aggregator's split-and-recombine routing -- a genuine branch/merge topology
(manual node x/y instead of the linear chain used in lesson-01-9 and
lesson-02-0's flow3d scenes, so this lesson reads as visually distinct) -- and
chart3d once, for the 20 ETH worked example's net-output comparison. That's
this skill's "at most one or two" ceiling; the 0.5 ETH counter-example stays a
flat `steps` scene.

Writes video-scripts/gold/lesson-02-1.json.
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
sc("title", "Lesson two point one. decks, aggregators and routing. By the end, you'll be able to choose where to swap by comparing the net amount you actually receive, not the quoted price.",
   "Lesson 2.1. DEXs, aggregators & routing. By the end, you'll be able to choose where to swap by comparing the net amount you actually receive, not the quoted price.",
   chapter="Intro", eyebrow="Lesson 2.1", num="2.1", title="DEXs, aggregators & routing", sub="The quoted price is not what lands in your wallet. The net amount is.")
sc("pillars", "Here's the plan. First, the three places a swap can actually happen, and what an aggregator does differently. Second, a real worked example showing exactly when routing wins, and when it quietly loses to gas. And third, a checklist to run before you click swap, every time.",
   chapter="Intro", title="What this lesson covers",
   items=[{"icon": "layers", "title": "Three ways to swap", "text": "AMM, order book, aggregator"},
          {"icon": "chart", "title": "Worked example", "text": "When routing wins, when it loses"},
          {"icon": "check", "title": "Checklist", "text": "Run it before every swap"}])
sc("statement", "Every swap you make shows you a quoted price first. That number is not what lands in your wallet. What you actually get equals the quoted output, minus price impact, minus pool fees, minus gas. Chase the quote, and you can end up worse off than the option that looked less impressive on screen.",
   chapter="Why it matters", kicker="What actually matters", lines=["The quote isn't what you get.", "The net amount is."], sub="Quoted output − price impact − pool fees − gas = what actually lands.")

# ---------------------------------------------------------------- three ways to swap
sc("title", "Three ways to swap.", chapter="Three ways to swap", eyebrow="Three ways to swap", num="1", title="Three ways to swap", sub="Same goal, three different mechanisms.")
sc("bullets", "So, three venues, side by side. An A.M.M. deck, an automated market maker, means you trade against a liquidity pool, priced by a formula, which lesson two point two covers in full. An on-chain order book means your order is matched by price and time against other orders, fully or partly on-chain. And an aggregator doesn't hold liquidity itself, it searches many pools and venues at once, and may split your order across several routes to get a better result.",
   chapter="Three ways to swap", title="Three ways to swap",
   items=["AMM DEX: trade against a liquidity pool, priced by a formula (Lesson 2.2)",
          "On-chain order book: orders matched by price and time, on-chain",
          "Aggregator: searches many pools and venues, may split your order across routes"])
sc("flow3d", "Here's what an aggregator actually does with your order. You submit one swap. The aggregator scans prices across every pool and venue it knows about. Rather than sending your whole order to one pool, it can split it: part to pool A, part to pool B, part to pool C. Each one absorbs less of the trade, so each one moves its own price less. Those three fills recombine into one net output back to you.",
   "Here's what an aggregator actually does with your order. You submit one swap. The aggregator scans prices across every pool and venue it knows about. Rather than sending your whole order to one pool, it can split it: part to pool A, part to pool B, part to pool C. Each one absorbs less of the trade, so each one moves its own price less. Those three fills recombine into one net output back to you.",
   chapter="Three ways to swap", title="How an aggregator splits and recombines an order", seed=21,
   nodes=[{"id": "you", "label": "You submit", "sub": "One swap order", "icon": "wallet", "x": 0.03, "y": 0.5},
          {"id": "agg", "label": "Aggregator", "sub": "Scans every pool and venue", "icon": "search", "x": 0.27, "y": 0.5},
          {"id": "poolA", "label": "Pool A", "sub": "Takes part of the order", "icon": "layers", "x": 0.56, "y": 0.02},
          {"id": "poolB", "label": "Pool B", "sub": "Takes part of the order", "icon": "layers", "x": 0.66, "y": 0.5},
          {"id": "poolC", "label": "Pool C", "sub": "Takes part of the order", "icon": "layers", "x": 0.56, "y": 0.98},
          {"id": "out", "label": "Net output", "sub": "Recombined, back to you", "icon": "check", "x": 0.95, "y": 0.5}],
   edges=[{"from": "you", "to": "agg", "label": "one order"},
          {"from": "agg", "to": "poolA"}, {"from": "agg", "to": "poolB"}, {"from": "agg", "to": "poolC"},
          {"from": "poolA", "to": "out"}, {"from": "poolB", "to": "out"}, {"from": "poolC", "to": "out"}])
sc("quiz", "Quick check. Why can an aggregator often give a better price than sending your whole order to one pool? [[pause 4]] The answer: it can split an order across several pools, so each pool absorbs less, and each one's price moves less.",
   n=1, of=3, q="Why can an aggregator give a better price?", a="It can split an order across pools, so each pool's price moves less.", chapter="Three ways to swap")

# ---------------------------------------------------------------- what moves the number
sc("title", "What moves the number.", chapter="What moves the number", eyebrow="What moves the number", num="2", title="What moves the number", sub="Two forces decide whether routing is worth it.")
sc("bullets", "Two things decide whether splitting actually helps. Price impact is how much your own trade moves the price, and it grows with your size relative to the pool's depth. Slippage tolerance is the worst price you'll accept before your transaction reverts instead of executing. And routing itself just means the path your order takes, sometimes multiple hops, A to B to C, which can reach a better price but touches more contracts along the way.",
   chapter="What moves the number", title="Two forces, plus the path itself",
   items=["Price impact: how much your trade moves the price; grows with size vs. pool depth",
          "Slippage tolerance: the worst price you'll accept before the transaction reverts",
          "Routing: multi-hop paths (A → B → C) can price better but touch more contracts"])
sc("compare", "Here's the pattern that actually decides the winner. On a small trade, your price impact is already tiny at a single pool, so an aggregator's improvement is a few dollars, easily eaten by its extra gas. On a large trade, your price impact at a single pool is real money. Splitting it across several pools, each moving less, saves real money too, comfortably past the extra gas it costs.",
   chapter="What moves the number", title="Small trade vs. large trade",
   left={"label": "Small trade", "items": ["Price impact already tiny at one pool", "Aggregator's edge: a few dollars", "Extra gas can erase it entirely"]},
   right={"label": "Large trade", "tone": "good", "items": ["Price impact at one pool is real money", "Splitting it saves real money too", "Savings comfortably outweigh the extra gas"]})
sc("quiz", "Quick check. What actually drives price impact? [[pause 4]] The answer: your trade size, relative to the pool's liquidity depth.",
   n=2, of=3, q="What drives price impact?", a="Trade size relative to pool liquidity.", chapter="What moves the number")
sc("statement", "Big trades benefit from routing. Small trades mostly lose to gas. That single line is the whole lesson, if you remember nothing else from it.",
   "Big trades benefit from routing. Small trades mostly lose to gas. That single line is the whole lesson, if you remember nothing else from it.",
   chapter="What moves the number", kicker="The one line to remember", lines=["Big trades benefit from routing.", "Small trades mostly lose to gas."], sub="Everything below is that idea, with real numbers.")

# ---------------------------------------------------------------- worked example
sc("title", "A worked example.", chapter="Worked example", eyebrow="Worked example", num="3", title="A worked example", sub="Same trade, two venues, two very different outcomes.")
sc("chart3d", "Selling twenty E.T.H. A single pool, direct, quotes fifty nine thousand one hundred U.S.D.C., costs about eight dollars in gas, netting fifty nine thousand and ninety two. An aggregator, splitting across three pools, quotes fifty nine thousand four hundred twenty, costs about twenty dollars in gas, netting fifty nine thousand four hundred. The aggregator wins here by about three hundred and eight dollars.",
   "Selling 20 ETH. A single pool, direct, quotes 59,100 USDC, costs about $8 in gas, netting 59,092. An aggregator, splitting across three pools, quotes 59,420, costs about $20 in gas, netting 59,400. The aggregator wins here by about $308.",
   chapter="Worked example", kind="bars", title="Selling 20 ETH: net output by venue", sub="Aggregator wins by ~$308 at this size", seed=221,
   bars=[{"label": "Single pool, direct", "text": "$8 gas", "value": 59092, "show": "$59,092 net", "tone": "neutral"},
         {"label": "Aggregator, split × 3", "text": "$20 gas", "value": 59400, "show": "$59,400 net", "tone": "good"}], max=59400)
sc("steps", "Now the same comparison at a much smaller size: selling zero point five E.T.H. The aggregator's quote is three dollars better than the direct pool's. But its route costs twelve dollars more in gas. Net, the aggregator is nine dollars worse off. At this size, the direct pool wins.",
   chapter="Worked example", title="Selling 0.5 ETH: the same comparison, small size",
   steps=["Direct pool: quoted output, baseline", "Aggregator: quote is $3 better", "Aggregator: route costs $12 more in gas", "Net: aggregator is $9 worse off at this size"],
   result="Direct pool wins here. The aggregator's edge didn't cover its own gas.")
sc("quiz", "Last check for this section. When does the best-looking quote actually lose? [[pause 4]] The answer: when the extra gas its route costs is more than the price improvement it offers, which is common on small trades.",
   n=3, of=3, q="When does the best quote lose?", a="When the extra gas costs more than the price improvement — common on small trades.", chapter="Worked example")

# ---------------------------------------------------------------- pitfalls
sc("title", "Where this goes wrong.", chapter="Where this goes wrong", eyebrow="Where this goes wrong", num="5", title="Where this goes wrong", sub="Four habits that quietly cost you money.")
sc("bullets", "Here's how people actually lose money on this, even once they know the theory. Comparing quoted prices instead of net output, so a worse deal looks better on screen. Assuming a route through more contracts is automatically riskier, when a well-established aggregator routing through audited major pools is often fine. Setting slippage tolerance far too high just to make a transaction go through, which opens the door to a much worse fill. And routing a small trade through several hops anyway, out of habit, when a single pool would have kept more of it.", check=False,
   chapter="Where this goes wrong", title="Where this goes wrong",
   items=["Comparing quoted price instead of net output", "Assuming more contracts always means more risk, even for audited major pools",
          "Setting slippage tolerance too high just to force a transaction through", "Routing a small trade through several hops out of habit"])

# ---------------------------------------------------------------- checklist
sc("title", "Before you click swap.", chapter="Checklist", eyebrow="Checklist", num="6", title="Before you click swap", sub="Four checks, every single time.")
sc("bullets", "Run this before every swap, not just the large ones. Compare net output after gas, never the headline quoted price. Check that the price impact shown is acceptable for this size. Confirm the route uses reputable pools and tokens you've actually verified. And set your slippage tolerance on purpose, which lesson two point five covers in depth.",
   chapter="Checklist", title="Your checklist",
   items=["Compare net output after gas, not the headline price", "Price impact shown is acceptable for this size",
          "Route uses reputable pools and tokens you've verified", "Slippage tolerance set on purpose (see Lesson 2.5)"])

# ---------------------------------------------------------------- your turn
sc("statement", "Your turn, five to ten minutes. Pull up a swap you're actually considering. Get a direct-pool quote and an aggregator quote for the same size. Work out the net output for each, quote minus price impact minus fees minus gas. Then pick whichever number is actually bigger, not whichever quote looked better on screen.",
   "Your turn, 5 to 10 minutes. Pull up a swap you're actually considering. Get a direct-pool quote and an aggregator quote for the same size. Work out the net output for each, quote minus price impact minus fees minus gas. Then pick whichever number is actually bigger, not whichever quote looked better on screen.",
   chapter="Your turn", kicker="Your turn", lines=["Get both quotes.", "Compare net output, not the quote."], sub="5 to 10 minutes, before your next real swap.")
sc("bullets", "To recap: an A.M.M. prices against a pool, an order book matches orders, and an aggregator can split across both to chase a better net result. Price impact and slippage tolerance are the two forces that decide whether splitting is worth it. And the rule of thumb holds: big trades benefit from routing, small trades mostly lose to gas.",
   "To recap: an AMM prices against a pool, an order book matches orders, and an aggregator can split across both to chase a better net result. Price impact and slippage tolerance are the two forces that decide whether splitting is worth it. And the rule of thumb holds: big trades benefit from routing, small trades mostly lose to gas.",
   chapter="Recap", title="Three things to remember",
   items=["An aggregator can split your order across pools to chase a better net result",
          "Price impact and slippage tolerance decide whether splitting is worth it",
          "Big trades benefit from routing; small trades mostly lose to gas"])
sc("cta", "That's decks, aggregators and routing. Next up, lesson two point two: A.M.M. mathematics, the formula behind every pool you just saw, x times y equals k.",
   "That's DEXs, aggregators and routing. Next up, Lesson 2.2: AMM mathematics, the formula behind every pool you just saw, x · y = k.",
   chapter="Recap", button="Next: Lesson 2.2", sub="AMM mathematics (x · y = k) · Educational content only · Not financial advice")

video = {
    "id": "lesson-02-1",
    "title": "Lesson 2.1: DEXs, aggregators & routing",
    "size": [1920, 1080],
    "group": "lessons",
    "maxMinutes": 25,
    "tag": "Lesson 2.1",
    "gold": True,
    "seed": 21,
    "use": "Lesson 2.1 page in the Whop course. Hand-written gold-standard script: AMM DEX vs. on-chain order book vs. aggregator, price impact, slippage tolerance, routing, the net-output formula, and the real 20 ETH / 0.5 ETH worked examples. Facts last checked: 2026-09-26.",
    "thumbnail": {"title": "Net output, not the quote", "subtitle": "Lesson 2.1"},
    "scenes": S,
}

out = ROOT / "video-scripts" / "gold" / "lesson-02-1.json"
out.write_text(json.dumps(video, indent=None))
print(f"wrote {out} ({len(S)} scenes)")
