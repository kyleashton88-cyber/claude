#!/usr/bin/env python3
"""Gold-standard script for Lesson 2.2, AMM mathematics (x*y=k) (target
10-20 minutes). Walks the constant-product formula, how price impact
actually emerges from it, arbitrage rebalancing, and the source material's
own worked example (100 ETH/300,000 USDC pool; 10 ETH swap vs 1 ETH swap),
as visual walk-throughs. Built to the walk-through-first standard: almost
every idea is a flow, steps or callout image, not a statement read over a
static screen.

Writes video-scripts/gold/lesson-02-2.json (the generator skips lessons with
a gold script). Spoken text (vo) spells numbers for the voice; cap is the
written caption, same sentence count as vo."""
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
sc("title", "Lesson two point two. AMM mathematics: x times y equals k. By the end, you'll calculate what a swap actually pays out in a constant-product pool, and explain why bigger trades get worse prices.",
   "Lesson 2.2. AMM mathematics: x times y equals k. By the end, you'll calculate what a swap actually pays out in a constant-product pool, and explain why bigger trades get worse prices.",
   chapter="Intro", eyebrow="Lesson 2.2", num="2.2", title="AMM mathematics: x × y = k", sub="One rule. Every price impact number falls out of it.")
sc("pillars", "Here's the plan. The one rule a constant-product pool actually keeps, and what it means for pricing. How price impact falls directly out of that rule, not from any separate fee. Who rebalances the pool after your trade, and why that matters later. And a full worked example, with real numbers, at two different trade sizes.",
   chapter="Intro", title="What this lesson covers",
   items=[{"icon": "cog", "title": "The one rule", "text": "Reserves × reserves = k, always"}, {"icon": "chart", "title": "Where price impact comes from", "text": "Directly out of the formula"},
          {"icon": "users", "title": "Arbitrageurs", "text": "Who rebalances the pool, and why it matters"}, {"icon": "target", "title": "Worked example", "text": "10 ETH vs 1 ETH, same pool"}])

# ---------------------------------------------------------------- the one rule
sc("title", "The one rule.", chapter="The one rule", eyebrow="The one rule", num="1", title="Reserves × reserves = k",
   sub="No order book. Just this, kept constant.")
sc("statement", "Here's the entire mechanism, in one sentence, before any numbers. A constant-product pool holds two tokens, and keeps one rule: the reserves of token A, multiplied by the reserves of token B, equals a constant, called k. No order book, no matching, just this one product, held constant, ignoring fees, after every single trade.",
   chapter="The one rule", kicker="The whole mechanism", lines=["Reserves A × reserves B = k.", "Held constant, after every trade."], sub="No order book. No matching. Just this.")
img(D + "amm-swap-flow.png", "What the pool's price actually is",
    "Here's what “pool price” means, concretely. It's simply the ratio of the two reserves. A hundred E.T.H. and three hundred thousand U.S.D.C. in the same pool means one E.T.H. is priced at roughly three thousand U.S.D.C., because that's the ratio those two reserve numbers make. Change either reserve, and that ratio, the price, changes with it.",
    chapter="The one rule")
sc("flow", "Here's what actually happens, mechanically, the instant you swap E.T.H. into that pool. You add E.T.H. to the pool's reserves. To keep x times y equal to that same constant k, the pool must remove U.S.D.C., automatically, by the formula alone, not by any decision. And what you receive is exactly however much U.S.D.C. the pool had to remove to keep the product constant.",
   chapter="The one rule", title="Add ETH in, USDC must come out",
   nodes=[{"label": "You add ETH", "sub": "To the pool's reserves", "icon": "coins"}, {"label": "x × y must stay = k", "sub": "The one rule, never broken", "icon": "cog"},
          {"label": "USDC must leave", "sub": "Automatically, by the formula alone", "icon": "swap"}, {"label": "That's what you receive", "sub": "Exactly enough to keep k constant", "icon": "check"}])
sc("flow", "Worth seeing the same rule run in the other direction, since it's perfectly symmetric. Swap U.S.D.C. into the pool instead, and E.T.H. is what has to leave, by the exact same formula, no exception for which token moves which way. Add U.S.D.C. to the pool's reserves. To keep x times y equal to k, the pool must remove E.T.H. And what you receive is exactly however much E.T.H. it had to remove.",
   chapter="The one rule", title="The same rule, running the other way",
   nodes=[{"label": "You add USDC", "sub": "To the pool's reserves", "icon": "coins"}, {"label": "x × y must stay = k", "sub": "The exact same rule, either direction", "icon": "cog"},
          {"label": "ETH must leave", "sub": "Automatically, by the formula", "icon": "swap"}, {"label": "That's what you receive", "sub": "No exception for which token moves", "icon": "check"}])
sc("quiz", "Quick check. A pool holds fifty E.T.H. and one hundred fifty thousand U.S.D.C. What's k, and what's the spot price? [[pause 4]] The answer: k is seven million five hundred thousand, from fifty times one hundred fifty thousand. Spot price is three thousand USDC per ETH, from the ratio of the two reserves.",
   chapter="The one rule", n=1, of=3, q="A pool holds 50 ETH and 150,000 USDC. What's k, and what's the spot price?",
   a="k = 7,500,000. Spot price = 3,000 USDC/ETH.")

# ---------------------------------------------------------------- where price impact comes from
sc("title", "Where price impact comes from.", chapter="Where price impact comes from", eyebrow="Where price impact comes from", num="2", title="Not a fee. The shape of the curve itself.",
   sub="The further you move it, the worse it gets.")
img(CH + "amm-curve.png", "The x × y = k curve",
    "Here's the actual shape underneath every constant-product trade. Plot the two reserves against each other, and every point that keeps x times y equal to k traces this curve. Your trade is a move along it: add to one axis, the other axis falls to compensate. And because the curve bends, moving further along it costs progressively more per unit, not a constant amount each time.",
    chapter="Where price impact comes from")
sc("statement", "This is the exact reason price impact isn't a fee anyone charges you. It's a direct, mechanical consequence of the curve's shape. The first unit of your trade moves the reserves a little. The last unit of the same trade moves them from an already-shifted starting point, which is why it's priced worse than the first unit, within the very same transaction.",
   chapter="Where price impact comes from", kicker="Why this isn't a fee", lines=["The curve's shape, not a charge.", "Later units, priced worse than earlier ones."], sub="Within the very same transaction.")
sc("steps", "Here's how to actually calculate price impact yourself, on any pool, using the exact same four moves as the worked example ahead. Read the pool's two current reserves. Add your trade size to the reserve you're putting in. Divide k, the original product, by that new reserve, to get the other side's new value. And compare what you'd receive against the pool's current spot price, to see the real percentage.",
   chapter="Where price impact comes from", title="Calculating it yourself, on any pool",
   steps=["Read the pool's two current reserves", "Add your trade size to the reserve you're putting in", "Divide k by that new reserve", "Compare the result to current spot price"], result="The exact same four moves as the worked example ahead")
sc("quiz", "Quick check. Why does a 10 ETH swap get a worse average price than a 1 ETH swap, in the exact same pool? [[pause 4]] The answer: each unit you add moves the reserve ratio further along the curve, so later units within the same trade are priced worse. Price impact grows with size relative to reserves.",
   chapter="Where price impact comes from", n=2, of=3, q="Why does a 10 ETH swap get a worse average price than a 1 ETH swap, in the exact same pool?",
   a="Each unit moves the ratio further along the curve; later units are priced worse.")

# ---------------------------------------------------------------- arbitrageurs
sc("title", "Arbitrageurs.", chapter="Arbitrageurs", eyebrow="Arbitrageurs", num="3", title="Who rebalances the pool, and why it matters",
   sub="A preview of Lesson 2.4.")
sc("flow", "Here's what happens right after your trade shifts the pool's ratio away from the wider market's price. An arbitrageur notices the pool is now priced differently from other venues. They trade against the pool, in whichever direction closes that gap. That trade pulls the pool's ratio back in line with the wider market. And it also changes exactly what the pool's liquidity providers now hold, which is where impermanent loss actually comes from.",
   chapter="Arbitrageurs", title="Why arbitrage changes what LPs hold",
   nodes=[{"label": "Your trade shifts the ratio", "sub": "Away from the wider market's price", "icon": "swap"}, {"label": "An arbitrageur notices", "sub": "The pool is now priced differently", "icon": "eye"},
          {"label": "They trade it back in line", "sub": "Closing the gap with other venues", "icon": "check"}, {"label": "LPs' holdings change", "sub": "This is where impermanent loss comes from", "icon": "alert"}])
sc("statement", "Worth being precise about why this matters beyond just this lesson. Arbitrage isn't a flaw in the system; it's what keeps a pool's price honest against the rest of the market. But every time it happens, the pool's liquidity providers end up holding a different mix of the two tokens than they started with. Lesson two point four picks this up directly, and shows exactly how to measure what that costs.",
   chapter="Arbitrageurs", kicker="Not a flaw — what keeps prices honest", lines=["Keeps the pool's price honest.", "But changes what LPs end up holding."], sub="Lesson 2.4 shows exactly how to measure that cost.")

# ---------------------------------------------------------------- worked example
sc("title", "Worked example.", chapter="Worked example", eyebrow="Worked example", num="1", title="100 ETH, 300,000 USDC — two trade sizes",
   sub="Real numbers, calculated live.")
sc("stats", "Here's the pool this entire example runs on. One hundred E.T.H., three hundred thousand U.S.D.C. Multiply those reserves and k is thirty million. Divide them and spot price is three thousand U.S.D.C. per E.T.H. Every number that follows falls directly out of these two starting reserves.",
   "Here's the pool this entire example runs on. 100 ETH, 300,000 USDC. Multiply those reserves and k is 30,000,000. Divide them and spot price is 3,000 USDC/ETH. Every number that follows falls directly out of these two starting reserves.",
   chapter="Worked example", stats=[["k = 30,000,000", "100 ETH × 300,000 USDC"], ["3,000 USDC/ETH", "spot price, from the same reserves"]])
sc("steps", "Now swap in ten E.T.H., fees ignored, and follow the arithmetic exactly. New E.T.H. reserve: one hundred plus ten, is one hundred ten. New U.S.D.C. reserve: thirty million divided by one hundred ten, is roughly two hundred seventy-two thousand seven hundred twenty-seven. You receive the difference: three hundred thousand minus that, roughly twenty-seven thousand two hundred seventy-three U.S.D.C.",
   chapter="Worked example", title="Swapping in 10 ETH, step by step",
   steps=["New ETH reserve: 100 + 10 = 110", "New USDC reserve: 30,000,000 ÷ 110 ≈ 272,727", "You receive: 300,000 − 272,727 ≈ 27,273 USDC"], result="Effective price: 27,273 ÷ 10 ≈ 2,727 USDC/ETH")
sc("stats", "Put that effective price next to spot, and here's the real cost of this trade. Twenty-seven hundred twenty-seven U.S.D.C. per E.T.H., against a spot price of three thousand. That's roughly nine point one percent worse than spot, entirely from this one trade's own size against this one pool's depth.",
   chapter="Worked example", stats=[["~9.1% worse", "10 ETH swap: 2,727 vs 3,000 USDC/ETH spot"]])
sc("compare", "Now the same pool, the same formula, a trade ten times smaller. One E.T.H. in: new reserve one hundred one, new U.S.D.C. reserve roughly two hundred ninety-seven thousand thirty, so you receive about two thousand nine hundred seventy, only around one percent worse than spot. Ten times the size cost roughly nine times more in price impact, not ten times, but close, and worth internalising either way.",
   chapter="Worked example",
   left={"label": "10 ETH swap", "tone": "warn", "items": ["Receive ~27,273 USDC", "~9.1% worse than spot"]},
   right={"label": "1 ETH swap, same pool", "tone": "good", "items": ["Receive ~2,970 USDC", "~1% worse than spot"]})
sc("stats", "Push it further still, same pool, same formula, to see how sharply this curves. Swap in fifty E.T.H., half the pool's original depth: new reserve one hundred fifty, new U.S.D.C. reserve exactly two hundred thousand, so you receive one hundred thousand U.S.D.C., at an effective price of two thousand per E.T.H. That's roughly thirty-three percent worse than spot, from a trade only five times larger than the first example.",
   "Push it further still, same pool, same formula, to see how sharply this curves. Swap in 50 ETH, half the pool's original depth: new reserve 150, new USDC reserve exactly 200,000, so you receive 100,000 USDC, at an effective price of 2,000 per ETH. That's roughly 33% worse than spot, from a trade only 5 times larger than the first example.",
   chapter="Worked example", stats=[["~33% worse", "50 ETH swap, same pool: 2,000 vs 3,000 USDC/ETH spot"]])
sc("chart", "Plot all three sizes together, and the shape of that earlier curve becomes obvious in the actual numbers. One E.T.H., about one percent worse. Ten E.T.H., about nine percent worse. Fifty E.T.H., about thirty-three percent worse. It isn't a straight line. Each step up in size costs a disproportionately bigger bite, exactly because you're moving further along a curve that bends, not a flat, constant rate.",
   chapter="Worked example", kind="line", title="Price impact, at three trade sizes", sub="Same pool, same formula — not a straight line",
   series=[{"values": [1, 9.1, 33], "tone": "bad"}], xlabels=["1 ETH", "10 ETH", "50 ETH"], yticks=[[1, "1%"], [33, "33%"]], ymin=0, ymax=38,
   marks=[{"i": 2, "text": "Disproportionately bigger, not linear", "tone": "bad", "below": False}])
sc("statement", "So here's the one sentence this entire worked example proves, worth remembering over any specific number. Size relative to pool depth is what actually matters, not the size of your trade in dollars alone. The same ten E.T.H. against a much deeper pool would barely move the price at all.",
   chapter="Worked example", kicker="The one sentence to keep", lines=["Size relative to pool depth.", "Not the size in dollars, alone."], sub="The same trade, against a deeper pool, barely moves the price.")
sc("quiz", "Quick check. Who actually moves the pool's price back in line with the wider market after a trade, and why does it matter to liquidity providers? [[pause 4]] The answer: arbitrageurs. Their trades rebalance the pool, which is exactly where impermanent loss comes from, since it changes what LPs end up holding.",
   chapter="Worked example", n=3, of=3, q="Who moves the pool's price back in line after a trade, and why does that matter to LPs?",
   a="Arbitrageurs — their rebalancing trades are where impermanent loss comes from.")

# ---------------------------------------------------------------- checklist and recap
sc("steps", "Here's your checklist, before any swap. Check the price impact the interface shows; if it isn't shown, work it out yourself, the same way this lesson just did. Compare with an aggregator quote. Set your slippage tolerance on purpose: too tight and the swap simply fails; too loose and you risk a bad fill or a sandwich attack, covered fully in Lesson two point five. Split large trades, or use deeper pools. And run the full before-signing checklist: chain, contract, token, amount, spender.",
   chapter="Checklist", title="Your checklist, before any swap",
   steps=["Check price impact shown, or work it out yourself", "Compare with an aggregator quote", "Slippage set on purpose — not too tight, not too loose", "Split large trades, or use deeper pools", "Full before-signing checklist: chain, contract, token, amount, spender"])
sc("bullets", "Let's recap. One rule: reserves times reserves equals k, held constant after every trade. Price impact isn't a fee; it's the direct, mechanical shape of that curve, worse for later units within the same trade. Arbitrageurs rebalance the pool back to the wider market, which is exactly where impermanent loss comes from. And size relative to pool depth is what actually decides your price, not the dollar size alone.",
   chapter="Recap", title="Recap", check=False,
   items=["x × y = k: the one rule, held constant every trade", "Price impact: the curve's shape, not a fee — worse for later units",
          "Arbitrageurs rebalance the pool; that's where impermanent loss comes from", "Size relative to pool depth is what decides your price"])
sc("cta", "Work out the price impact yourself, on any pool, before you trust the interface's number blindly. Next up, Lesson two point three: Providing liquidity.",
   "Work out the price impact yourself, on any pool, before you trust the interface's number blindly. Next up, Lesson 2.3: Providing liquidity.",
   chapter="Recap", button="Next: Lesson 2.3", sub="Providing liquidity")

spec = {"id": "lesson-02-2", "title": "Lesson 2.2: AMM mathematics (x·y=k)", "size": [1920, 1080], "group": "lessons", "maxMinutes": 25,
        "tag": "Lesson 2.2", "gold": True, "music": True, "musicLevel": 0.14, "seed": 54,
        "use": "Lesson 2.2 page in the Whop course. Hand-written gold-standard script: the constant-product formula, where price impact comes from, arbitrage rebalancing, and the source material's own 100 ETH/300,000 USDC worked example at two trade sizes, as walk-throughs.",
        "thumbnail": {"title": "AMM mathematics", "subtitle": "Lesson 2.2 · x·y=k"}, "scenes": S}
out = ROOT / "video-scripts" / "gold" / "lesson-02-2.json"
out.write_text(json.dumps(spec, indent=1, ensure_ascii=False))
words = sum(len(s["vo"].replace("[[pause 4]]", "").split()) for s in S)
print(f"{len(S)} scenes, {words} words, est {(words / 171 * 60 + len(S) * 1.3 + 4 * 3) / 60:.1f} min")
