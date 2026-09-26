#!/usr/bin/env python3
"""Gold-standard script for Lesson 2.7, Advanced AMM design and LVR (target
10-20 minutes, expert). Walks the major AMM designs (constant product,
StableSwap, weighted pools, concentrated liquidity, hooks) and
loss-versus-rebalancing (LVR), ending on the source material's own worked
example (ETH/USDC full-range pool, 80% volatility: LVR ~8.0%/yr, +4%/yr net
of 12% fee APR; 110% volatility flips it to a loss), as visual
walk-throughs. Built to the walk-through-first standard: almost every idea
is a flow, steps or callout image, not a statement read over a static
screen.

Writes video-scripts/gold/lesson-02-7.json (the generator skips lessons
with a gold script). Spoken text (vo) spells numbers for the voice; cap is
the written caption, same sentence count as vo."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
S = []


def sc(type_, vo, cap=None, **k):
    d = {"type": type_, **k, "vo": vo}
    if cap:
        d["cap"] = cap
    S.append(d)


def img(src, eyebrow, vo, cap=None, **k):
    sc("image", vo, cap, src=src, eyebrow=eyebrow, wide=True, **k)


D = "assets/diagrams/"
CH = "assets/charts/"

# ---------------------------------------------------------------- intro
sc("title", "Lesson two point seven. Advanced AMM design and LVR. By the end, you'll know the major AMM designs, and measure an LP's real cost with loss-versus-rebalancing.",
   "Lesson 2.7. Advanced AMM design and LVR. By the end, you'll know the major AMM designs, and measure an LP's real cost with loss-versus-rebalancing.",
   chapter="Intro", eyebrow="Lesson 2.7 · Expert", num="2.7", title="Advanced AMM design and LVR", sub="Fees have to beat LVR. Not just impermanent loss.")
sc("pillars", "Here's the plan. The major A.M.M. designs, and which pair each one actually fits. Loss-versus-rebalancing, L.V.R., the more complete measure of what an L.P. actually loses to arbitrage. A full worked example, with real numbers, showing exactly when fees beat L.V.R., and when they don't. And what changes once volatility rises.",
   chapter="Intro", title="What this lesson covers",
   items=[{"icon": "layers", "title": "AMM designs", "text": "Constant product, StableSwap, weighted, concentrated"}, {"icon": "chart", "title": "LVR", "text": "The more complete measure than IL alone"},
          {"icon": "target", "title": "Worked example", "text": "80% volatility, then 110%"}, {"icon": "alert", "title": "Hooks", "text": "New designs, new contract risk"}])

# ---------------------------------------------------------------- amm designs
sc("title", "The major AMM designs.", chapter="AMM designs", eyebrow="AMM designs", num="1", title="Which pair each one actually fits",
   sub="Not one design for every pool.")
sc("compare", "Start with the two ends of the spectrum, since they solve genuinely different problems. Constant product, x times y equals k, from Lesson two point two, works for any pair at all, spreading liquidity evenly across every possible price. StableSwap is built specifically for assets that should trade near one-to-one, stablecoins, or a liquid-staking token against E.T.H., blending a flat, low-slippage curve near the peg with constant-product safety further away from it.",
   chapter="AMM designs",
   left={"label": "Constant product (x·y=k)", "tone": "good", "items": ["Works for any pair, at all", "Spreads liquidity evenly across every price"]},
   right={"label": "StableSwap", "tone": "good", "items": ["Built for near-1:1 pairs specifically", "Flat near the peg; constant-product safety away from it"]})
sc("flow", "Here's exactly how StableSwap achieves that low slippage near the peg, mechanically. Near the peg, the curve behaves almost flat, like a constant-sum pool, meaning trades near one-to-one barely move the price at all. Further from the peg, it blends toward constant-product behaviour instead, for safety. And an amplification parameter tunes exactly how wide that flat, low-slippage zone actually is.",
   chapter="AMM designs", title="How StableSwap blends two curves",
   nodes=[{"label": "Near the peg", "sub": "Almost flat, like constant-sum", "icon": "chart"}, {"label": "Further from the peg", "sub": "Blends toward constant-product", "icon": "swap"},
          {"label": "Amplification parameter", "sub": "Tunes how wide the flat zone is", "icon": "cog"}, {"label": "Low slippage, where it matters", "sub": "Exactly where these pairs actually trade", "icon": "check"}])
sc("statement", "Two more designs worth knowing by name, each solving a specific, different problem. Weighted pools hold more than two tokens, or uneven weights like eighty-twenty, and an eighty-twenty pool specifically carries less impermanent loss on its eighty-percent token. Concentrated liquidity lets you place a position only within a price range you choose, tracking the square root of price internally, covered in more depth as your positions get more advanced.",
   chapter="AMM designs", kicker="Two more, by name", lines=["Weighted pools: uneven splits, like 80/20.", "Concentrated liquidity: a chosen price range, not the whole curve."], sub="Each one solves a specific, different problem.")
sc("flow", "Zoom into concentrated liquidity specifically, since “a chosen price range” is easy to nod along to without seeing the mechanism. You choose a price range, called a tick range, rather than the entire possible curve. Your capital only becomes active liquidity while price sits inside that range. Inside it, you earn a far larger share of fees per dollar deposited, since your capital isn't spread thin across prices that never trade. And if price moves outside your range entirely, your position earns nothing until it moves back in, or you adjust it.",
   chapter="AMM designs", title="How a concentrated position actually works",
   nodes=[{"label": "Choose a tick range", "sub": "Not the entire possible curve", "icon": "target"}, {"label": "Active only inside it", "sub": "While price sits in your chosen range", "icon": "check"},
          {"label": "Far more fees per dollar", "sub": "Capital isn't spread thin, elsewhere", "icon": "coins"}, {"label": "Outside the range: nothing", "sub": "Until price returns, or you adjust it", "icon": "alert"}])
sc("quiz", "Quick check. Why is StableSwap specifically built for near-1:1 pairs, rather than any pair? [[pause 4]] The answer: it blends a flat, low-slippage curve near the peg with constant-product safety further away, giving very low slippage exactly where these pairs actually trade.",
   chapter="AMM designs", n=1, of=3, q="Why is StableSwap specifically built for near-1:1 pairs, rather than any pair?",
   a="It gives very low slippage near the peg, where these pairs trade.")

# ---------------------------------------------------------------- lvr
sc("title", "Loss-versus-rebalancing.", chapter="LVR", eyebrow="Loss-versus-rebalancing", num="2", title="A more complete measure than IL alone",
   sub="What LPs actually lose to arbitrage.")
sc("statement", "Here's precisely what L.V.R. measures, and why it's more complete than impermanent loss on its own. A pool's price only updates when an arbitrageur actually trades against it, after the real price has already moved elsewhere, the exact mechanism from Lesson two point two. L.V.R. measures what that lag costs L.P.s, compared against a portfolio that rebalances continuously, at the real market price, the instant it moves.",
   chapter="LVR", kicker="What LVR actually measures", lines=["What LPs lose to that lag.", "Versus a portfolio that rebalances instantly, at the real price."], sub="A more complete measure than a single impermanent-loss snapshot.")
sc("flow", "Here's the formula itself, for a full-range constant-product pool specifically. Take sigma, the token's annual volatility. Square it. Divide by eight. That gives L.V.R., as a percentage of pool value, per year. And the rule that actually matters in practice: your fees have to beat this number, not just beat impermanent loss on its own.",
   chapter="LVR", title="The LVR formula, for a full-range pool",
   nodes=[{"label": "σ = annual volatility", "sub": "The one input the formula needs", "icon": "chart"}, {"label": "σ² ÷ 8", "sub": "Squared, divided by eight", "icon": "cog"},
          {"label": "= LVR, per year", "sub": "As a percentage of pool value", "icon": "alert"}, {"label": "Fees must beat this", "sub": "Not just beat impermanent loss alone", "icon": "shield"}])
img(CH + "lvr.png", "LVR rises with volatility, not linearly",
    "Here's the actual shape of that relationship. Because volatility is squared in the formula, L.V.R. doesn't rise in a straight line as volatility increases; it rises faster and faster, the same bending-curve pattern from the price-impact formula in Lesson two point two, just applied to volatility instead of trade size now.",
    chapter="LVR")
sc("compare", "Worth reconciling this with Lesson two point five directly, since it can sound contradictory otherwise. Arbitrage M.E.V. is harmless to the market as a whole; it's exactly what keeps a pool's price honest against everywhere else. L.V.R. is the same arbitrage, viewed specifically from the L.P.'s side of the trade; harmless to the system, and a real, measurable cost to whoever was supplying that liquidity.",
   chapter="LVR",
   left={"label": "From the market's view", "tone": "good", "items": ["Arbitrage MEV: harmless", "Keeps the pool's price honest"]},
   right={"label": "From the LP's view", "tone": "warn", "items": ["The same arbitrage: LVR", "A real, measurable cost to the LP"]})
sc("quiz", "Quick check. What does LVR actually measure, that a simple impermanent-loss snapshot doesn't fully capture? [[pause 4]] The answer: what LPs lose to arbitrageurs specifically because the pool's price lags the real market, compared against a portfolio that rebalances continuously at the real price.",
   chapter="LVR", n=2, of=3, q="What does LVR actually measure, that a simple impermanent-loss snapshot doesn't fully capture?",
   a="What LPs lose to arbitrageurs because the pool's price lags the market.")
sc("compare", "One practical consequence worth naming before the worked example: concentrated liquidity and weighted pools both carry a form of L.V.R. too, not just full-range constant-product pools. The exact formula changes shape for each design, but the underlying cause is identical: price lags the market until an arbitrageur closes the gap, at the LP's expense. Full-range is simply the case with the cleanest, most citable formula.",
   chapter="LVR",
   left={"label": "Full-range constant product", "tone": "good", "items": ["The formula this lesson uses: σ² ÷ 8", "The cleanest, most citable case"]},
   right={"label": "Concentrated / weighted pools", "tone": "warn", "items": ["Same underlying cause, different formula shape", "Still a real cost, still worth measuring"]})

# ---------------------------------------------------------------- worked example
sc("title", "Worked example.", chapter="Worked example", eyebrow="Worked example", num="1", title="ETH/USDC, at two volatility levels",
   sub="Real numbers, calculated from the formula.")
sc("steps", "Here's the arithmetic, at eighty percent annual E.T.H. volatility, step by step. Square sigma: zero point eight squared is zero point six four. Divide by eight: zero point six four divided by eight is zero point zero eight, or eight percent. That's your L.V.R., as a share of pool value, every year, before any fees are even counted.",
   chapter="Worked example", title="LVR at 80% annual volatility",
   steps=["σ = 0.80 (80% annual volatility)", "σ² = 0.64", "σ² ÷ 8 = 0.08"], result="LVR ≈ 8.0% of pool value, per year")
sc("compare", "Now bring fees into it, at a twelve percent fee A.P.R. on this same pool. Fees: twelve percent a year. L.V.R.: eight percent a year. The difference, roughly four percent a year, is what L.P.s actually keep, before gas, at this specific volatility level. Not the fee A.P.R. alone. The fee A.P.R., minus L.V.R.",
   chapter="Worked example",
   left={"label": "Fee APR", "tone": "good", "items": ["12% per year"]},
   right={"label": "Minus LVR (8%)", "tone": "warn", "items": ["Net: ~+4%/yr, before gas", "Not the 12% alone"]})
sc("stats", "Now raise volatility to one hundred ten percent, the same pair, a more turbulent year, and watch what the squared relationship does to this exact same math. One point one squared is one point two one. Divided by eight, that's roughly fifteen percent L.V.R. a year, nearly double the previous figure, from a volatility increase of only about thirty-eight percent.",
   "Now raise volatility to 110%, the same pair, a more turbulent year, and watch what the squared relationship does to this exact same math. 1.1 squared is 1.21. Divided by 8, that's roughly 15% LVR a year, nearly double the previous figure, from a volatility increase of only about 38%.",
   chapter="Worked example", stats=[["~15%/yr", "LVR at 110% volatility — nearly double, from ~38% more volatility"]])
sc("statement", "And here's exactly what that does to the same twelve percent fee A.P.R. that was profitable a moment ago. Twelve percent in fees, minus roughly fifteen percent in L.V.R., comes out negative, around minus three percent a year. The same fee income that comfortably beat L.V.R. at eighty percent volatility now loses money outright, at one hundred ten percent, with nothing about the fees themselves having changed.",
   chapter="Worked example", kicker="The same fees, now losing money", lines=["12% fees − ~15% LVR ≈ −3%/yr.", "Nothing about the fees changed. The volatility did."], sub="Higher-volatility pairs need much higher fee tiers to compensate.")
sc("steps", "Here's how to actually run this comparison yourself, on any pool, using this program's own calculator tool, rather than doing the arithmetic by hand each time. Estimate the token's annual volatility, from its own recent price history. Feed that volatility, and the pool's advertised fee A.P.R., into the calculator directly. And only proceed if fee A.P.R. genuinely clears L.V.R., with real room to spare, not just barely.",
   chapter="Worked example", title="Running this yourself, with the calculator",
   steps=["Estimate the token's annual volatility", "Feed volatility and fee APR into the calculator", "Proceed only if fee APR clears LVR, with room to spare"], result="Not just barely — volatility itself isn't constant")
sc("quiz", "Quick check. Volatility is sixty percent a year, on a full-range pool. What's the approximate LVR? [[pause 4]] The answer: about four point five percent a year. Zero point six squared is zero point three six, divided by eight is zero point zero four five.",
   chapter="Worked example", n=3, of=3, q="Volatility is 60%/yr on a full-range pool. What's the approximate LVR?",
   a="About 4.5%/yr (0.6² ÷ 8 = 0.045).")

# ---------------------------------------------------------------- hooks and checklist
sc("title", "Hooks, and new contract risk.", chapter="Hooks", eyebrow="Hooks", num="1", title="Newer designs, new things to check",
   sub="Custom code, at the moment of every swap.")
sc("statement", "Worth knowing this one newer category by name, since it changes what due diligence on a pool actually means. Hooks let a pool run custom code at the exact moment of every swap: dynamic fees, built-in limit orders, live oracle feeds, whatever the pool's designer wrote. Each hook is its own additional smart contract, carrying its own additional risk, on top of the AMM design underneath it.",
   chapter="Hooks", kicker="Custom code, at every swap", lines=["Dynamic fees, limit orders, oracles — built in.", "Each hook: its own contract, its own additional risk."], sub="Review a hook the same way you'd review any other contract.")
sc("steps", "Here's your checklist. Do it now, before choosing a pool type or depositing into one. Choose pool type by the actual pair: StableSwap for pegged pairs, weighted or concentrated liquidity otherwise. Compare fee A.P.R. against L.V.R. specifically, not just impermanent loss on its own. And review any hook contract the exact same way you'd review any other contract, since it carries the exact same kind of risk.",
   chapter="Hooks", title="Your checklist",
   steps=["Pool type by pair: StableSwap pegged, weighted/CL otherwise", "Compare fee APR against LVR, not just IL", "Review hook contracts like any other contract"])

# ---------------------------------------------------------------- recap
sc("statement", "One last honest framing, before the recap, since “expert” shouldn't mean “ignore this.” Nothing here changes what you learned about impermanent loss in Lesson two point four; L.V.R. simply gives you the sharper, more complete lens for judging whether a specific pool's fees genuinely compensate for the risk you're taking on, especially as volatility climbs.",
   chapter="Recap", kicker="What this adds, not replaces", lines=["Doesn't replace Lesson 2.4's IL.", "A sharper lens, especially as volatility climbs."], sub="Judging whether fees genuinely compensate for the risk.")
sc("bullets", "Let's recap. Constant product fits any pair; StableSwap fits near-1:1 pairs specifically, with much lower slippage there. Weighted pools handle uneven splits; concentrated liquidity focuses a position into a chosen range. L.V.R. equals volatility squared, divided by eight, for a full-range pool, and it's the more complete measure of what arbitrage actually costs L.P.s. And because volatility is squared, L.V.R. rises far faster than volatility itself, which is exactly why higher-volatility pairs need much higher fee tiers to stay profitable.",
   chapter="Recap", title="Recap", check=False,
   items=["Constant product: any pair. StableSwap: near-1:1, much lower slippage", "Weighted pools: uneven splits. Concentrated liquidity: a chosen range",
          "LVR = σ² ÷ 8, for a full-range pool — more complete than IL alone", "LVR rises faster than volatility itself — fees must beat it, not just IL"])
sc("cta", "Compare fee APR against LVR, not just impermanent loss, before trusting any pool's advertised yield. Next up, Lesson two point eight: The MEV supply chain.",
   "Compare fee APR against LVR, not just impermanent loss, before trusting any pool's advertised yield. Next up, Lesson 2.8: The MEV supply chain.",
   chapter="Recap", button="Next: Lesson 2.8", sub="The MEV supply chain")

spec = {"id": "lesson-02-7", "title": "Lesson 2.7: Advanced AMM design and LVR", "size": [1920, 1080], "group": "lessons", "maxMinutes": 25,
        "tag": "Lesson 2.7", "gold": True, "music": True, "musicLevel": 0.14, "seed": 59,
        "use": "Lesson 2.7 page in the Whop course. Hand-written gold-standard script: the major AMM designs, the LVR formula, hooks/new contract risk, and the source material's own 80%-vs-110%-volatility worked example, as walk-throughs.",
        "thumbnail": {"title": "Advanced AMM design & LVR", "subtitle": "Lesson 2.7 · Expert"}, "scenes": S}
out = ROOT / "video-scripts" / "gold" / "lesson-02-7.json"
out.write_text(json.dumps(spec, indent=1, ensure_ascii=False))
words = sum(len(s["vo"].replace("[[pause 4]]", "").split()) for s in S)
print(f"{len(S)} scenes, {words} words, est {(words / 171 * 60 + len(S) * 1.3 + 4 * 3) / 60:.1f} min")
