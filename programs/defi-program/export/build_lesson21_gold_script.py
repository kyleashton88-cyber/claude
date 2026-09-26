#!/usr/bin/env python3
"""Gold-standard script for Lesson 2.1, DEXs, aggregators & routing (target
10-20 minutes). Walks AMM DEXs vs on-chain order books, aggregators and
multi-hop routing, and the real formula for what you actually receive, as
visual walk-throughs, ending on the source material's own worked example
(20 ETH via direct pool vs aggregator; 0.5 ETH where the direct pool wins).
Built to the walk-through-first standard: almost every idea is a flow, steps
or callout image, not a statement read over a static screen.

Writes video-scripts/gold/lesson-02-1.json (the generator skips lessons with
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

# ---------------------------------------------------------------- intro
sc("title", "Lesson two point one. DEXs, aggregators and routing. By the end, you'll choose where to swap by comparing what you'd actually receive, not the price quoted on screen.",
   "Lesson 2.1. DEXs, aggregators and routing. By the end, you'll choose where to swap by comparing what you'd actually receive, not the price quoted on screen.",
   chapter="Intro", eyebrow="Lesson 2.1", num="2.1", title="DEXs, aggregators and routing", sub="Compare net received. Not the quote.")
sc("pillars", "Here's the plan. The two ways a DEX can actually price your trade. What an aggregator does differently, and why routing across pools can help. The real formula for what you actually receive, once every cost is counted. And a full worked example, with real numbers, showing exactly when each approach wins.",
   chapter="Intro", title="What this lesson covers",
   items=[{"icon": "swap", "title": "How a DEX prices a trade", "text": "AMM pools vs on-chain order books"}, {"icon": "layers", "title": "Aggregators & routing", "text": "Splitting an order across pools"},
          {"icon": "chart", "title": "The real formula", "text": "Quote minus impact, fees and gas"}, {"icon": "target", "title": "Worked example", "text": "Real numbers, both directions"}])

# ---------------------------------------------------------------- how a dex prices a trade
sc("title", "Two ways to price a trade.", chapter="Two ways to price a trade", eyebrow="Two ways to price a trade", num="1", title="AMM pools vs on-chain order books",
   sub="Same goal, two different mechanisms.")
sc("flow", "First mechanism: the A.M.M. DEX, the one most people mean by “DEX.” You trade against a pool of two tokens, held by a smart contract. A formula, covered fully in Lesson two point two, sets the price from the pool's current balance. Your trade itself shifts that balance, which is exactly what moves the price. There's no order book, and no waiting for a matching counterparty.",
   chapter="Two ways to price a trade", title="How an AMM DEX prices your trade",
   nodes=[{"label": "A pool of two tokens", "sub": "Held by a smart contract", "icon": "layers"}, {"label": "A formula sets the price", "sub": "From the pool's current balance", "icon": "cog"},
          {"label": "Your trade shifts the balance", "sub": "Which is what moves the price", "icon": "swap"}, {"label": "No counterparty needed", "sub": "No order book, no waiting", "icon": "check"}])
sc("compare", "Second mechanism: the on-chain order book, less common but worth knowing by name. Here's the actual contrast. An A.M.M. pool always has a price, set by a formula, and always has some liquidity available, even if a large trade moves it a lot. An order book needs an actual matching order at your price, fully or partly on-chain, or your trade simply doesn't fill.",
   chapter="Two ways to price a trade",
   title="AMM pool vs order book", left={"label": "AMM pool", "tone": "good", "items": ["Price set by a formula, always available", "Large trades move the price, but still fill"]},
   right={"label": "On-chain order book", "tone": "warn", "items": ["Needs a matching order, at your price", "No match at your price: it doesn't fill"]})
sc("flow", "Worth seeing an on-chain order book as its own walk-through, since “needs a match” undersells how it actually works. You place an order, at a specific price you choose. It sits on the book, waiting, visible to everyone, fully or partly on-chain depending on the venue. Another trader's order arrives that matches your price. And the trade settles, for exactly your chosen price, no impact from pool depth at all.",
   chapter="Two ways to price a trade", title="How an on-chain order book actually fills",
   nodes=[{"label": "You place an order", "sub": "At a specific price you choose", "icon": "eye"}, {"label": "It waits on the book", "sub": "Visible to everyone", "icon": "clock"},
          {"label": "A matching order arrives", "sub": "At your chosen price", "icon": "swap"}, {"label": "Settles at your price", "sub": "No pool-depth impact at all", "icon": "check"}])
sc("stats", "One real number, so this isn't a niche corner of crypto. Industry trackers have recorded decentralised exchanges collectively processing tens of billions of dollars in trading volume in a typical month, across chains. This is outside research, not this program's own data, but it's why getting this one habit right, comparing net received, matters at real scale, not just for your own trades.",
   chapter="Two ways to price a trade", stats=[["$10Bs+/mo", "typical DEX trading volume, across chains (outside research)"]])
sc("quiz", "Quick check. What actually moves the price in an AMM pool? [[pause 4]] The answer: your own trade does, by shifting the pool's balance of the two tokens, which is what the pricing formula reacts to.",
   chapter="Two ways to price a trade", n=1, of=3, q="What actually moves the price in an AMM pool?",
   a="Your own trade, by shifting the pool's token balance.")

# ---------------------------------------------------------------- aggregators and routing
sc("title", "Aggregators and routing.", chapter="Aggregators & routing", eyebrow="Aggregators & routing", num="2", title="Searching, and splitting, for a better result",
   sub="Not always better. Worth checking, every time.")
img(D + "dex-vs-aggregator.png", "What an aggregator actually does",
    "An aggregator searches many pools and venues for your trade, not just one. And critically, it may split your order across several routes at once, sending part of it through one pool and part through another, so no single pool absorbs the full price impact alone. That splitting is exactly how it can land a better net price than any single pool could offer on its own.",
    chapter="Aggregators & routing")
sc("flow", "Here's what “routing” actually means, step by step, since “multi-hop” sounds abstract until you see it. A direct route goes straight from token A to token B, through one pool. A multi-hop route instead goes A to B to C, through two or more pools in sequence. That extra hop can land a meaningfully better price. It also means more contracts your trade depends on behaving correctly, one after another.",
   chapter="Aggregators & routing", title="A direct route, vs a multi-hop route",
   nodes=[{"label": "Token A", "sub": "Where your trade starts", "icon": "coins"}, {"label": "Through pool 1", "sub": "Direct: straight to token B", "icon": "swap"},
          {"label": "Optionally, pool 2", "sub": "Multi-hop: via an intermediate token", "icon": "layers"}, {"label": "Token B (or C)", "sub": "More hops, more contracts depended on", "icon": "check"}])
sc("statement", "Worth being precise about what routing does and doesn't guarantee, before the worked example. It can land a better price, by spreading your trade or finding a cheaper path. It cannot make a trade free, and it cannot remove price impact entirely, only reduce how much of it lands on any one pool. Gas for those extra hops is real, and it comes out of the same net result you're comparing.",
   chapter="Aggregators & routing", kicker="What routing doesn't guarantee", lines=["Not free. Not impact-free.", "Just spread across more, and often cheaper, pools."], sub="The extra gas is real, and comes out of the same net result.")
sc("steps", "Before trusting any aggregator with real size, here's what's actually worth checking. Confirm it's a reputable, widely used aggregator, not an unfamiliar interface someone linked you. Check that its fee, if any, is disclosed plainly, not hidden inside a worse quote. And read the route it's proposing, at least the token list, before you sign, the same habit as reading any other prompt.",
   chapter="Aggregators & routing", title="Before trusting an aggregator with real size",
   steps=["Reputable, widely used — not an unfamiliar link", "Any fee disclosed plainly, not hidden in the quote", "Read the proposed route before you sign"], result="Same habit as reading any other prompt")
sc("compare", "One more honest trade-off worth naming, since aggregators aren't purely an upgrade. A direct DEX trade touches one contract, so there's exactly one thing that needs to behave correctly. An aggregator route touches its own routing contract, plus every pool along the path, which is more surface area, even though each individual contract is typically well-audited on a reputable aggregator.",
   chapter="Aggregators & routing",
   title="A direct trade vs an aggregator route", left={"label": "A direct DEX trade", "tone": "good", "items": ["One contract, exactly", "Less surface area, simpler to reason about"]},
   right={"label": "An aggregator route", "tone": "warn", "items": ["The router, plus every pool along the path", "More surface area, even if each is well-audited"]})
sc("quiz", "Quick check. Why can splitting an order across several pools actually improve the price you get? [[pause 4]] The answer: no single pool absorbs the full trade, so no single pool's price moves as far, which is exactly what price impact is driven by.",
   chapter="Aggregators & routing", n=2, of=3, q="Why can splitting an order across several pools actually improve the price you get?",
   a="No single pool absorbs the full trade, so no single pool's price moves as far.")

# ---------------------------------------------------------------- the real formula
sc("title", "The real formula.", chapter="The real formula", eyebrow="The real formula", num="3", title="What you actually receive",
   sub="Four things subtract from the number on screen.")
sc("flow", "Here's the formula, spelled out as four steps, not just a line of text. Start with the quoted output, the headline number the interface shows you. Subtract price impact, your own trade moving the pool's price against you. Subtract pool fees, paid to whoever provided that liquidity. And subtract gas, the network fee for executing the transaction at all. What's left is what actually lands in your wallet.",
   chapter="The real formula", title="Quoted output, minus everything real",
   nodes=[{"label": "Quoted output", "sub": "The headline number shown", "icon": "eye"}, {"label": "− Price impact", "sub": "Your own trade, moving the price", "icon": "alert"},
          {"label": "− Pool fees", "sub": "Paid to liquidity providers", "icon": "coins"}, {"label": "− Gas", "sub": "The network fee to execute at all", "icon": "cog"}])
sc("compare", "Put real numbers on how pool depth changes the same trade, since “relative to pool depth” is easy to nod along to and hard to picture. The same ten-thousand-dollar trade against a deep, million-dollar-plus pool might move the price by a few hundredths of a percent, barely measurable. Against a shallow, ten-thousand-dollar pool, that same trade is now a huge share of what's available, and price impact can run into double digits.",
   chapter="The real formula",
   title="A deep pool vs a shallow pool", left={"label": "$10K trade, a deep pool", "tone": "good", "items": ["Millions in the pool", "Price impact: a few hundredths of a percent"]},
   right={"label": "$10K trade, a shallow pool", "tone": "bad", "items": ["Only tens of thousands in the pool", "Price impact: can run into double digits"]})
sc("steps", "Turn that formula into an actual pre-trade habit, every time you swap. Check the price impact shown, and ask whether it's acceptable for a trade this size. Confirm the route uses pools and tokens you've actually verified, not an unfamiliar token that appeared in a route. And set your slippage tolerance on purpose, covered fully in Lesson two point five, not left on whatever default the interface picked.",
   chapter="The real formula", title="The pre-trade habit",
   steps=["Check price impact: acceptable for this size?", "Route uses pools and tokens you've verified", "Slippage tolerance set on purpose, not left default"], result="Compare net output after gas, not the headline price")

# ---------------------------------------------------------------- worked example
sc("title", "Worked example.", chapter="Worked example", eyebrow="Worked example", num="1", title="Selling 20 ETH, two ways",
   sub="Real numbers, from the source material.")
sc("stats", "Here's the real comparison, selling twenty E.T.H. A single pool, direct, quotes fifty-nine thousand one hundred U.S.D.C., costs eight dollars in gas, netting fifty-nine thousand ninety-two. An aggregator, splitting across three pools, quotes fifty-nine thousand four hundred and twenty, costs twenty dollars in gas, netting fifty-nine thousand four hundred. The aggregator wins, by roughly three hundred and eight dollars, even after its higher gas cost.",
   "Here's the real comparison, selling 20 ETH. A single pool, direct, quotes 59,100 USDC, costs $8 in gas, netting 59,092. An aggregator, splitting across 3 pools, quotes 59,420, costs $20 in gas, netting 59,400. The aggregator wins, by roughly $308, even after its higher gas cost.",
   chapter="Worked example", stats=[["$59,092", "Direct pool, net after $8 gas"], ["$59,400", "Aggregator (3 pools), net after $20 gas"]])
sc("compare", "Now the same comparison, at a much smaller size, since the answer actually flips. Selling zero point five E.T.H., the aggregator quotes three dollars better than the direct pool. But it also costs twelve dollars more in gas. Net, the direct pool wins by nine dollars. Big trades benefit from routing. Small trades mostly lose to the extra gas.",
   chapter="Worked example",
   title="Selling 20 ETH vs 0.5 ETH", left={"label": "Selling 20 ETH", "tone": "good", "items": ["Aggregator nets ~$308 more", "The extra gas is worth it, at this size"]},
   right={"label": "Selling 0.5 ETH", "tone": "warn", "items": ["Aggregator quotes $3 better, costs $12 more gas", "Direct pool wins, net, by $9"]})
sc("steps", "Here's how to actually run this comparison yourself, on any trade, before you commit. Get a quote from a single DEX, direct. Get a quote from an aggregator, for the exact same pair and size. Subtract each route's own gas estimate from its quoted output. And take whichever net number is higher, not whichever quote looked better on its own.",
   chapter="Worked example", title="Running the comparison yourself",
   steps=["Quote a single DEX, direct", "Quote an aggregator, same pair and size", "Subtract each route's own gas estimate", "Take the higher net — not the better-looking quote"], result="Two minutes, before every trade that's worth comparing")
sc("quiz", "Quick check. Why does the direct pool win on the small 0.5 ETH trade, when the aggregator quoted a better price? [[pause 4]] The answer: the aggregator's extra gas cost, twelve dollars, was larger than its three-dollar price improvement, so net, the direct pool came out ahead.",
   chapter="Worked example", n=3, of=3, q="Why does the direct pool win on the small 0.5 ETH trade, when the aggregator quoted a better price?",
   a="Its extra gas cost more than its price improvement, so net, the direct pool won.")

# ---------------------------------------------------------------- checklist and recap
sc("steps", "Here's your checklist. Do it now, for real, on every swap. You compare net output after gas, not the headline quoted price. Price impact shown is acceptable for the size you're trading. Your route uses reputable pools and tokens you've actually verified. And your slippage tolerance is set on purpose, covered fully in Lesson two point five.",
   chapter="Checklist", title="Your checklist",
   steps=["Compare net output after gas, not the headline price", "Price impact shown is acceptable for this size", "Route uses reputable, verified pools and tokens", "Slippage set on purpose, not left on default"])
sc("statement", "One last thing worth naming before the recap, since it sets up everything through the rest of this module. Every number in this lesson, price impact, the formula, the worked example, comes out of the same underlying pricing formula a pool actually runs. Lesson two point two opens that formula up directly, so you can calculate these numbers yourself, not just recognise them on screen.",
   chapter="Recap", kicker="Where this leads next", lines=["One formula, underneath everything here.", "Lesson 2.2 opens it up directly."], sub="So you can calculate these numbers yourself.")
sc("bullets", "Let's recap. An A.M.M. pool always has a price, set by a formula; an order book needs an actual match. An aggregator can land a better price by splitting your order across pools, at the cost of more gas for the extra hops. The real formula is quoted output, minus price impact, minus fees, minus gas. And the size of your trade decides which approach wins: big trades benefit from routing, small trades mostly lose to gas.",
   chapter="Recap", title="Recap", check=False,
   items=["AMM pool: always has a price. Order book: needs a match", "Aggregators: better price, at the cost of more gas for extra hops",
          "The real formula: quote minus impact, fees and gas", "Big trades benefit from routing; small trades mostly lose to gas"])
sc("cta", "Compare net received, not the quote, on every single swap. Next up, Lesson two point two: AMM mathematics.",
   "Compare net received, not the quote, on every single swap. Next up, Lesson 2.2: AMM mathematics.",
   chapter="Recap", button="Next: Lesson 2.2", sub="AMM mathematics")

spec = {"id": "lesson-02-1", "title": "Lesson 2.1: DEXs, aggregators & routing", "size": [1920, 1080], "group": "lessons", "maxMinutes": 25,
        "tag": "Lesson 2.1", "gold": True, "music": True, "musicLevel": 0.14, "seed": 53,
        "use": "Lesson 2.1 page in the Whop course. Hand-written gold-standard script: AMM vs order book, aggregators/routing, the real net-received formula, and the source material's own 20 ETH / 0.5 ETH worked example, as walk-throughs.",
        "thumbnail": {"title": "DEXs, aggregators, routing", "subtitle": "Lesson 2.1"}, "scenes": S}
out = ROOT / "video-scripts" / "gold" / "lesson-02-1.json"
out.write_text(json.dumps(spec, indent=1, ensure_ascii=False))
words = sum(len(s["vo"].replace("[[pause 4]]", "").split()) for s in S)
print(f"{len(S)} scenes, {words} words, est {(words / 171 * 60 + len(S) * 1.3 + 4 * 3) / 60:.1f} min")
