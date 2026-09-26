#!/usr/bin/env python3
"""Gold-standard script for Lesson 2.2, AMM mathematics (x . y = k) (~9-11 min).

Source: 02-sample-lesson-amm-math.md, "Sample Lesson 2.2 -- AMM Mathematics
(x . y = k)". Teaches: the constant-product rule, pool price as a reserve
ratio, price impact, arbitrage rebalancing, and the real worked examples (a
100 ETH / 300,000 USDC pool; a 10 ETH swap nets ~9.1% worse than spot, a 1
ETH swap ~1% worse).

Uses flow3d (see .claude/skills/webgl-motion-graphics/SKILL.md) once, with
layout="cycle" instead of the linear chain or branch/merge fan used in the
last two lessons -- a genuine fit here, since "swap moves the price ->
arbitrageurs trade it back in line -> pool is rebalanced" is a real repeating
cycle, not a one-way pipeline. And chart3d once, for the 1 ETH vs. 10 ETH
price-impact comparison. That's this skill's "at most one or two" ceiling.

Writes video-scripts/gold/lesson-02-2.json.
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
sc("title", "Lesson two point two. A.M.M. mathematics, x times y equals k. By the end, you'll be able to calculate what a swap actually pays out in a constant-product pool, and explain why bigger trades get worse prices.",
   "Lesson 2.2. AMM mathematics (x · y = k). By the end, you'll be able to calculate what a swap actually pays out in a constant-product pool, and explain why bigger trades get worse prices.",
   chapter="Intro", eyebrow="Lesson 2.2", num="2.2", title="AMM mathematics (x · y = k)", sub="One rule prices every trade in the pool. Here's exactly how.")
sc("pillars", "Here's the plan. First, the one rule that prices every trade in a constant-product pool. Second, a real worked example, with the exact numbers a swap pays out. And third, the checklist you run before any swap that touches one of these pools.",
   chapter="Intro", title="What this lesson covers",
   items=[{"icon": "cog", "title": "The one rule", "text": "x · y = k, and what it forces"},
          {"icon": "chart", "title": "Worked example", "text": "The exact payout, step by step"},
          {"icon": "check", "title": "Checklist", "text": "Run it before any swap"}])
sc("statement", "You already know bigger trades get worse prices. This lesson is where that stops being a feeling and becomes a number you can calculate yourself, before you ever sign the transaction.",
   chapter="Why it matters", kicker="Where this stops being a guess", lines=["Bigger trades get worse prices.", "Now you can calculate exactly how much."], sub="From a felt sense to an exact number, before you sign anything.")

# ---------------------------------------------------------------- the rule
sc("title", "The one rule.", chapter="The one rule", eyebrow="The one rule", num="1", title="The one rule", sub="No order book. Just an equation.")
sc("bullets", "A constant-product A.M.M. holds two tokens in a pool, no order book at all. It keeps exactly one rule: reserves of token A, times reserves of token B, equals k. And k has to stay constant, ignoring fees, after every single trade. Pool price is just the ratio of those two reserves: a hundred E.T.H. and three hundred thousand U.S.D.C. means one E.T.H. is worth about three thousand U.S.D.C.",
   chapter="The one rule", title="The constant-product rule",
   items=["Reserves of token A × reserves of token B = k, always", "k stays constant (ignoring fees) after every trade",
          "Pool price is just the ratio of the two reserves"])
sc("flow3d", "Here's that rule playing out as an actual trade happens. You swap E.T.H. into the pool. The pool has to remove enough U.S.D.C. to keep x times y equal to k, no exceptions. That shift moves the price against the next trader; the further you moved the pool, the bigger that price impact. Arbitrageurs then trade the pool back in line with every other market. And that rebalancing is exactly what changes what an L.P. holds, which lesson two point four covers in full.",
   "Here's that rule playing out as an actual trade happens. You swap ETH into the pool. The pool has to remove enough USDC to keep x times y equal to k, no exceptions. That shift moves the price against the next trader; the further you moved the pool, the bigger that price impact. Arbitrageurs then trade the pool back in line with every other market. And that rebalancing is exactly what changes what an LP holds, which Lesson 2.4 covers in full.",
   chapter="The one rule", title="One trade, all the way around", seed=22, layout="cycle",
   nodes=[{"id": "swap", "label": "You swap ETH in", "sub": "Adding to one side of the pool", "icon": "wallet"},
          {"id": "rule", "label": "x · y = k enforced", "sub": "The pool removes USDC to match", "icon": "cog"},
          {"id": "impact", "label": "Price moves", "sub": "Against the next trader", "icon": "chart", "tone": "warn"},
          {"id": "arb", "label": "Arbitrageurs trade it back", "sub": "Back in line with other markets", "icon": "search"},
          {"id": "lp", "label": "LP holdings shift", "sub": "What rebalancing actually changes", "icon": "layers"}],
   edges=[{"from": "swap", "to": "rule"}, {"from": "rule", "to": "impact"}, {"from": "impact", "to": "arb"},
          {"from": "arb", "to": "lp"}, {"from": "lp", "to": "swap", "dashed": True}])
sc("quiz", "Quick check. A pool holds fifty E.T.H. and one hundred fifty thousand U.S.D.C. What's k, and what's the spot price? [[pause 4]] The answer: k is seven point five million, and spot price is three thousand U.S.D.C. per E.T.H.",
   n=1, of=3, q="Pool: 50 ETH / 150,000 USDC. What is k and the spot price?", a="k = 7,500,000; spot = 3,000 USDC/ETH.", chapter="The one rule")

# ---------------------------------------------------------------- worked example
sc("title", "A worked swap.", chapter="Worked example", eyebrow="Worked example", num="2", title="A worked swap", sub="Same pool, two trade sizes, two very different outcomes.")
sc("steps", "Start with a pool holding one hundred E.T.H. and three hundred thousand U.S.D.C., so k is thirty million, and spot price is three thousand U.S.D.C. per E.T.H. Swap in ten E.T.H., fees ignored. New E.T.H. side: one hundred plus ten, one hundred ten. New U.S.D.C. side: thirty million divided by one hundred ten, about two hundred seventy two thousand seven hundred twenty seven. You receive the difference: three hundred thousand minus that, about twenty seven thousand two hundred seventy three U.S.D.C. Your effective price: about two thousand seven hundred twenty seven per E.T.H., roughly nine point one percent worse than spot.",
   chapter="Worked example", title="Swapping in 10 ETH",
   steps=["Pool: 100 ETH / 300,000 USDC, so k = 30,000,000", "New ETH side: 100 + 10 = 110",
          "New USDC side: 30,000,000 ÷ 110 ≈ 272,727", "You receive: 300,000 − 272,727 ≈ 27,273 USDC"],
   result="Effective price ≈ $2,727/ETH — about 9.1% worse than the $3,000 spot price")
sc("chart3d", "Now try the same pool at three sizes. One E.T.H.: new E.T.H. side one hundred one, you'd receive about two thousand nine hundred seventy U.S.D.C., only around one percent worse than spot. Ten E.T.H., the trade you just worked through, about nine point one percent worse. And fifty E.T.H.: new E.T.H. side one hundred fifty, you'd receive about one hundred thousand U.S.D.C., roughly thirty three percent worse than spot. Ten times the size cost about nine times more impact. Five times that again cost more than triple again. Size relative to the pool's depth is what matters, not the size of the trade in dollars.",
   "Now try the same pool at three sizes. 1 ETH: new ETH side 101, you'd receive about 2,970 USDC, only around 1% worse than spot. 10 ETH, the trade you just worked through, about 9.1% worse. And 50 ETH: new ETH side 150, you'd receive about 100,000 USDC, roughly 33% worse than spot. Ten times the size cost about nine times more impact. Five times that again cost more than triple again. Size relative to the pool's depth is what matters, not the size of the trade in dollars.",
   chapter="Worked example", kind="bars", title="Price impact grows faster than trade size", sub="Same 100 ETH / 300,000 USDC pool, three sizes", seed=222,
   bars=[{"label": "1 ETH swap", "text": "≈2,970 USDC received", "value": 1, "show": "≈1%", "tone": "good"},
         {"label": "10 ETH swap", "text": "≈27,273 USDC received", "value": 9.1, "show": "≈9.1%", "tone": "warn"},
         {"label": "50 ETH swap", "text": "≈100,000 USDC received", "value": 33.3, "show": "≈33%", "tone": "bad"}], max=33.3)
sc("quiz", "Quick check. Why does a ten E.T.H. swap get a worse average price than a one E.T.H. swap, in that same pool? [[pause 4]] The answer: each unit you add moves the reserve ratio further, so later units in the same trade are priced worse. Price impact grows with trade size relative to reserves.",
   n=2, of=3, q="Why does a 10 ETH swap get a worse average price than a 1 ETH swap?", a="Each unit moves the reserve ratio further; price impact grows with size relative to reserves.", chapter="Worked example")
sc("statement", "Size relative to pool depth is what matters. Not the size of the trade in dollars.",
   "Size relative to pool depth is what matters. Not the size of the trade in dollars.",
   chapter="Worked example", kicker="The one line to remember", lines=["Size relative to pool depth", "is what matters."], sub="Not the size of the trade in dollars.")
sc("quiz", "Last check for this section. Who actually moves the pool price back in line after your trade, and why does that matter to L.P.s? [[pause 4]] The answer: arbitrageurs do. Their trades rebalance what the L.P. holds, which is exactly where impermanent loss comes from, covered fully in Lesson two point four.",
   n=3, of=3, q="Who rebalances the pool price after a trade, and why does it matter to LPs?", a="Arbitrageurs; their trades rebalance what the LP holds, which is where impermanent loss comes from (Lesson 2.4).", chapter="Worked example")

# ---------------------------------------------------------------- pitfalls
sc("title", "Where this trips people up.", chapter="Where this trips people up", eyebrow="Where this trips people up", num="3", title="Where this trips people up", sub="Four habits worth breaking.")
sc("bullets", "Here's how people get this wrong even once they know the formula. Assuming price impact scales in proportion to size, it doesn't, it gets worse than proportionally, as you just saw. Reading the pool's spot price and assuming that's what they'll receive, it's only the starting point, not the fill. Ignoring that fees also sit in the pool and shift the real math slightly. And skipping the aggregator comparison because the math felt done once k was calculated, when a split across pools can still beat a single constant-product pool outright.", check=False,
   chapter="Where this trips people up", title="Where this trips people up",
   items=["Assuming price impact scales in proportion to size (it gets worse than proportional)",
          "Reading spot price and assuming that's the fill you'll actually receive",
          "Ignoring that trading fees also sit in the pool and shift the real math",
          "Skipping the aggregator comparison once k is calculated (Lesson 2.1)"])

# ---------------------------------------------------------------- checklist
sc("title", "Before any swap.", chapter="Checklist", eyebrow="Checklist", num="4", title="Before any swap", sub="Five checks, every single time.")
sc("bullets", "Run this before any swap on one of these pools. Check the price impact the interface shows; if it isn't shown, work it out yourself. Compare with an aggregator quote. Set your slippage tolerance on purpose, too tight and the swap fails, too loose and you risk a bad fill or a sandwich attack, which lesson two point five covers in full. Split large trades, or use deeper pools. And run the before-signing checklist: chain, contract, token, amount, spender.",
   chapter="Checklist", title="Before any swap",
   items=["Check the price impact shown; work it out yourself if it isn't", "Compare with an aggregator quote",
          "Set slippage tolerance on purpose (too tight fails; too loose risks a sandwich, see 2.5)",
          "Split large trades, or use deeper pools", "Run the before-signing checklist: chain, contract, token, amount, spender"])

# ---------------------------------------------------------------- your turn
sc("statement", "Your turn, five to ten minutes. Pick any constant-product pool you can see the reserves for. Calculate k, and work out what a trade of a size you'd actually make would net you, before you ever open the swap screen.",
   "Your turn, 5 to 10 minutes. Pick any constant-product pool you can see the reserves for. Calculate k, and work out what a trade of a size you'd actually make would net you, before you ever open the swap screen.",
   chapter="Your turn", kicker="Your turn", lines=["Pick a real pool.", "Calculate k, then your real net."], sub="5 to 10 minutes, with a calculator, before your next swap.")
sc("bullets", "To recap: a constant-product pool keeps reserves of token A times reserves of token B equal to k, always. Price impact grows with your trade size relative to the pool's depth, not the size of the trade in dollars. And arbitrageurs rebalance the pool after every trade, which is exactly where impermanent loss for L.P.s comes from.",
   "To recap: a constant-product pool keeps reserves of token A times reserves of token B equal to k, always. Price impact grows with your trade size relative to the pool's depth, not the size of the trade in dollars. And arbitrageurs rebalance the pool after every trade, which is exactly where impermanent loss for LPs comes from.",
   chapter="Recap", title="Three things to remember",
   items=["Reserves of token A × reserves of token B = k, always", "Price impact grows with size relative to pool depth, not dollars",
          "Arbitrageurs rebalance the pool — that's where impermanent loss comes from"])
sc("cta", "That's A.M.M. mathematics. Next up, lesson two point three: providing liquidity, and estimating what an L.P. position actually earns.",
   "That's AMM mathematics. Next up, Lesson 2.3: providing liquidity, and estimating what an LP position actually earns.",
   chapter="Recap", button="Next: Lesson 2.3", sub="Providing liquidity · Educational content only · Not financial advice")

video = {
    "id": "lesson-02-2",
    "title": "Lesson 2.2: AMM mathematics (x · y = k)",
    "size": [1920, 1080],
    "group": "lessons",
    "maxMinutes": 25,
    "tag": "Lesson 2.2",
    "gold": True,
    "seed": 22,
    "use": "Lesson 2.2 page in the Whop course. Hand-written gold-standard script: the constant-product rule, pool price as a reserve ratio, price impact, arbitrage rebalancing, and the real 100 ETH/300,000 USDC pool worked examples (10 ETH swap ~9.1% worse than spot, 1 ETH swap ~1% worse). Facts last checked: 2026-09-26.",
    "thumbnail": {"title": "x · y = k, worked out", "subtitle": "Lesson 2.2"},
    "scenes": S,
}

out = ROOT / "video-scripts" / "gold" / "lesson-02-2.json"
out.write_text(json.dumps(video, indent=None))
print(f"wrote {out} ({len(S)} scenes)")
