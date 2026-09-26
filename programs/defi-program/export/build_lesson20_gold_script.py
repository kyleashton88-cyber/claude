#!/usr/bin/env python3
"""Gold-standard script for Lesson 2.0, Mastery Starter (Module 2: Trading On-Chain,
~12 minutes).

Source: lessons/module-02-trading-on-chain.md, "Lesson 2.0 — Mastery Starter".
Teaches: the 60-second version (a swap trades against a formula-priced pool; LPing
earns fees but changes what you hold), the five words the module needs (DEX,
liquidity pool, price impact, slippage, impermanent loss), a first safe step
(quote the same swap two ways before executing), and the mastery ladder.

Uses flow3d for how a swap actually routes through an aggregator to a pool - the
one genuine multi-step mechanism here - and chart3d for the mastery ladder, per
the webgl-motion-graphics skill's "1-2 scenes" guidance.

Writes video-scripts/gold/lesson-02-0.json.
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
sc("title", "Lesson two point oh. Mastery Starter. New to trading on-chain? Start here. In about ten minutes, you'll have the five words and the first move this whole module builds on.",
   "Lesson 2.0. Mastery Starter. New to trading on-chain? Start here. In about 10 minutes, you'll have the five words and the first move this whole module builds on.",
   chapter="Intro", eyebrow="Lesson 2.0", num="2.0", title="Mastery Starter", sub="Module 2: Trading On-Chain, from zero to ready.")
sc("pillars", "Here's the plan. First, the sixty second version of this whole module. Second, five words you'll hear constantly from here on. Third, one safe first move you can make today, without risking anything. And finally, the mastery ladder that shows where this module is taking you.",
   chapter="Intro", title="What this lesson covers",
   items=[{"icon": "swap", "title": "The 60-second version", "text": "What a swap and an LP position actually are"},
          {"icon": "book", "title": "Five words", "text": "You'll hear them constantly from here on"},
          {"icon": "compass", "title": "One safe first move", "text": "Nothing executed, nothing risked"}])

sc("statement", "Every swap you'll ever make on-chain moves a price that isn't set by any single seller. Trade blind to that, and the pool itself quietly charges you for the size of your own trade, before a single fee is even counted.",
   chapter="Why it matters", kicker="Why this module exists", lines=["No single seller sets the price.", "Trade blind, and the pool charges you."], sub="Before a single fee is even counted. That's what this module fixes.")

# ---------------------------------------------------------------- 60 second version
sc("title", "The 60-second version.", chapter="The 60-second version", eyebrow="The 60-second version", num="1", title="The 60-second version", sub="Two things happen on-chain when you trade.")
sc("statement", "Here it is, in full. A swap on a decentralised exchange trades against a pool of tokens, priced by a formula, not by a company's order book. Providing liquidity to that same pool earns you a share of its trading fees. But it also changes what you hold, compared to just holding the two tokens yourself. This module teaches you to do both, knowing the real cost going in.",
   chapter="The 60-second version", kicker="The whole module, in one breath", lines=["A swap trades against a formula.", "Providing liquidity earns fees —"], sub="but it also changes what you hold. This module teaches you the real cost of both.")
sc("flow3d", "Watch what actually happens when you tap “swap.” You submit the trade. An aggregator checks prices across many pools at once, not just one. It routes your trade to whichever pool, or split of pools, gives you the best price after fees. That pool's own formula sets the exact price as your trade executes. And you receive the output token, at whatever price the formula produced.",
   chapter="The 60-second version", title="What happens when you tap “swap”", seed=20,
   nodes=[{"id": "you", "label": "You submit the trade", "sub": "An amount, and a token pair", "icon": "wallet"},
          {"id": "agg", "label": "Aggregator checks prices", "sub": "Across many pools at once", "icon": "search"},
          {"id": "pool", "label": "Routed to the best pool(s)", "sub": "Best price after fees", "icon": "layers"},
          {"id": "out", "label": "You receive the output", "sub": "At the price the formula set", "icon": "check"}],
   edges=[{"from": "you", "to": "agg"}, {"from": "agg", "to": "pool", "label": "best route"}, {"from": "pool", "to": "out", "label": "executes"}])
sc("quiz", "Quick check. What does providing liquidity to a pool actually earn you? [[pause 4]] The answer: a share of that pool's trading fees, in exchange for changing what you hold compared to simply holding the two tokens yourself.",
   n=1, of=2, q="What does providing liquidity earn you, and what does it cost?", a="A share of the pool's trading fees, in exchange for changing what you hold vs. just holding the two tokens.", chapter="The 60-second version")

# ---------------------------------------------------------------- five words
sc("title", "Five words you'll need.", chapter="Five words", eyebrow="Five words", num="2", title="Five words you'll need", sub="Said constantly from here on. Worth locking in now.")
sc("compare", "The first two describe where a trade happens. A DEX, a decentralised exchange, is one you use straight from your own wallet, no account, no custody handed over. A liquidity pool is the pot of two tokens sitting inside it that your trade actually swaps against.",
   "The first two describe where a trade happens. A DEX, a decentralised exchange, is one you use straight from your own wallet, no account, no custody handed over. A liquidity pool is the pot of two tokens sitting inside it that your trade actually swaps against.",
   chapter="Five words", title="Where a trade happens",
   left={"label": "DEX", "items": ["A decentralised exchange", "Used straight from your own wallet", "No account, no custody handed over"]},
   right={"label": "Liquidity pool", "tone": "good", "items": ["The pot of two tokens inside it", "Your trade swaps against this pot", "Priced by a formula, not an order book"]})
sc("chart", "Put real numbers on price impact. In a typical pool, a tiny trade barely moves the price at all. Trade a size that's a meaningful slice of the pool, and the price you get worsens fast, well before any fee is even applied. That's why the same twenty dollar trade can cost noticeably more in a small pool than a deep one.",
   "Put real numbers on price impact. In a typical pool, a tiny trade barely moves the price at all. Trade a size that's a meaningful slice of the pool, and the price you get worsens fast, well before any fee is even applied. That's why the same $20 trade can cost noticeably more in a small pool than a deep one.",
   chapter="Five words", kind="line", title="Price impact grows with trade size", sub="Illustrative curve, not a live quote",
   series=[{"values": [0.1, 0.3, 0.8, 2.1, 5.4, 11.2], "tone": "bad", "label": "Price impact %"}],
   xlabels=["0.01%", "0.1%", "0.5%", "1%", "2%", "4%"], yticks=[[0, "0%"], [5, "5%"], [10, "10%"]],
   caption="X-axis: trade size as a share of the pool")
sc("compare", "The next two describe cost, and they're easy to confuse. Price impact is how much your own trade moves the price, purely because of its size relative to the pool. Slippage is the worst price you've told the app you'll accept, your safety limit. A big trade has real price impact whether you set slippage or not; slippage just stops it from executing far worse than you expected.",
   chapter="Five words", title="Price impact vs. slippage",
   left={"label": "Price impact", "items": ["How much YOUR trade moves the price", "Caused by trade size vs. pool size", "Happens whether you set a limit or not"]},
   right={"label": "Slippage", "tone": "good", "items": ["The worst price you'll accept", "A safety limit you set yourself", "Stops execution at a far worse price"]})
sc("statement", "The fifth word is the one that surprises people most. Impermanent loss is how far a liquidity position lags simply holding the same two tokens, once their prices move apart. It isn't a fee, and it isn't theft. It's the mathematical cost of the formula rebalancing your pool for you, automatically, every time the price moves.",
   chapter="Five words", kicker="The one that surprises people", lines=["Impermanent loss: how far an L.P.", "lags simply holding the same tokens."], sub="Not a fee. Not theft. The formula rebalancing your pool, automatically, as price moves.")
sc("chart", "Here's the shape of it. Deposit into a pool when both tokens are worth the same as just holding them. Let one token's price run up. Simply holding would have captured that whole move. The pool, instead, has been automatically selling the rising token into the falling one the entire way up, so the L.P. position lags. Fees earned can close that gap, or even close it entirely, but the gap itself is real, and it starts the moment prices move apart.",
   "Here's the shape of it. Deposit into a pool when both tokens are worth the same as just holding them. Let one token's price run up. Simply holding would have captured that whole move. The pool, instead, has been automatically selling the rising token into the falling one the entire way up, so the LP position lags. Fees earned can close that gap, or even close it entirely, but the gap itself is real, and it starts the moment prices move apart.",
   chapter="Five words", kind="line", title="Why an LP position lags simply holding", sub="Illustrative example, one token rising against the other",
   series=[{"values": [100, 100, 104, 112, 124, 140], "tone": "good", "label": "Simply holding"},
           {"values": [100, 100, 102, 106, 111, 118], "tone": "bad", "label": "LP position (before fees)"}],
   xlabels=["Deposit", "", "", "", "", "Now"], yticks=[[100, "100"], [120, "120"], [140, "140"]],
   caption="The gap is impermanent loss — fees earned can narrow or close it")
sc("quiz", "Quick check. What's the real difference between price impact and slippage? [[pause 4]] The answer: price impact is how much your trade moves the price, caused by its size; slippage is the worst price you've told the app you'll accept, a limit you set yourself.",
   n=2, of=2, q="What's the difference between price impact and slippage?", a="Price impact is how much your trade moves the price (caused by size); slippage is the worst price you'll accept (a limit you set).", chapter="Five words")

# ---------------------------------------------------------------- first safe step
sc("title", "Your first safe step.", chapter="Your first safe step", eyebrow="Your first safe step", num="3", title="Your first safe step", sub="Nothing executed. Nothing risked.")
sc("bullets", "Before you start this module for real, confirm two things. You've completed Modules zero and one. And you have a little E.T.H. for gas, plus some U.S.D.C., on a low-fee network, ready to go.",
   "Before you start this module for real, confirm two things. You've completed Modules 0 and 1. And you have a little ETH for gas, plus some USDC, on a low-fee network, ready to go.",
   chapter="Your first safe step", title="Before you start",
   items=["Modules 0 and 1 completed", "A little ETH for gas, and some USDC, on a low-fee network"])
sc("steps", "Here's the move itself. Pick a token pair you'd actually trade, say twenty dollars of it. Quote that exact trade on a single D.E.X. directly. Then quote the same trade on an aggregator instead. Compare what you'd actually receive after gas, on each. Don't execute either yet, just look at the difference the routing makes.",
   "Here's the move itself. Pick a token pair you'd actually trade, say $20 of it. Quote that exact trade on a single DEX directly. Then quote the same trade on an aggregator instead. Compare what you'd actually receive after gas, on each. Don't execute either yet, just look at the difference the routing makes.",
   chapter="Your first safe step", title="Quote it two ways",
   steps=["Pick a token pair, e.g. a $20 trade", "Quote it on a single DEX directly", "Quote the same trade on an aggregator", "Compare what you'd receive after gas — don't execute yet"],
   result="You've just seen what routing is worth, before risking a cent")
sc("quiz", "Quick check. Why quote the same trade both ways before executing either? [[pause 4]] The answer: routing through an aggregator can find a better price across several pools, and comparing first shows you exactly what that's worth, with nothing at risk.",
   n=1, of=1, q="Why quote a trade on both a DEX and an aggregator before executing?", a="An aggregator can route across several pools for a better price; comparing first shows what that's worth, with nothing at risk.", chapter="Your first safe step")

# ---------------------------------------------------------------- mastery ladder
sc("title", "The mastery ladder.", chapter="The mastery ladder", eyebrow="The mastery ladder", num="4", title="The mastery ladder", sub="Three rungs. Climb them in order.")
sc("chart3d", "Here's where this module takes you, as three rungs. Beginner: small swaps, deliberate slippage, protected routing. Practitioner: calculating fee A.P.R. and impermanent loss, tracking a position against simply holding. Master: running limit, T.W.A.P. and intent-based orders, with written rules for every L.P. position you open.",
   "Here's where this module takes you, as three rungs. Beginner: small swaps, deliberate slippage, protected routing. Practitioner: calculating fee APR and impermanent loss, tracking a position against simply holding. Master: running limit, TWAP and intent-based orders, with written rules for every LP position you open.",
   chapter="The mastery ladder", kind="bars", title="Three rungs, climbed in order", sub="Illustrative sequence, not a time estimate", seed=220,
   bars=[{"label": "Beginner", "text": "Small swaps, deliberate slippage", "value": 1, "show": "Rung 1", "tone": "muted"},
         {"label": "Practitioner", "text": "Fee APR and IL, tracked vs. holding", "value": 2, "show": "Rung 2", "tone": "warn"},
         {"label": "Master", "text": "Limit/TWAP/intent orders, written rules", "value": 3, "show": "Rung 3", "tone": "good"}], max=3)
sc("bullets", "Here's the road ahead, lesson by lesson. Two point one covers D.E.X.s, aggregators and routing in full. Two point three and two point four are providing liquidity, and the true P and L once impermanent loss is counted. Two point five is M.E.V., the value extracted from your trades if you don't protect them. And two point six through two point eight take you into limit orders, advanced A.M.M. design, and the M.E.V. supply chain end to end.",
   "Here's the road ahead, lesson by lesson. 2.1 covers DEXs, aggregators and routing in full. 2.3 and 2.4 are providing liquidity, and the true P&L once impermanent loss is counted. 2.5 is MEV, the value extracted from your trades if you don't protect them. And 2.6 through 2.8 take you into limit orders, advanced AMM design, and the MEV supply chain end to end.",
   chapter="The mastery ladder", title="The road ahead",
   items=["2.1: DEXs, aggregators & routing, in full", "2.3-2.4: Providing liquidity, and true P&L after IL",
          "2.5: MEV, and protecting your trades from it", "2.6-2.8: Limit/TWAP orders, advanced AMM design, the MEV supply chain"])
sc("statement", "You've mastered this module when you can predict a swap's real cost, and an L.P. position's likely result against simply holding, before you ever enter either one.",
   chapter="The mastery ladder", kicker="You've mastered this when…", lines=["…you can predict a swap's cost,", "and an LP's result vs. holding —"], sub="before you enter either one, not after.")

# ---------------------------------------------------------------- recap
sc("bullets", "To recap: a swap trades against a formula-priced pool, and providing liquidity earns fees but changes what you hold. Price impact and slippage are different things, and impermanent loss is the formula rebalancing you, not a fee. And your first move is simply to compare, quoted two ways, before you ever execute.",
   chapter="Recap", title="Three things to remember",
   items=["A swap trades against a formula-priced pool", "Price impact (size) and slippage (your limit) are different things", "Compare a quote two ways before you ever execute"])
sc("cta", "That's your Mastery Starter for Module Two. Next up, Lesson two point one: D.E.X.s, aggregators, and how routing actually decides your price.",
   "That's your Mastery Starter for Module Two. Next up, Lesson 2.1: DEXs, aggregators, and how routing actually decides your price.",
   chapter="Recap", button="Continue to Lesson 2.1", sub="DEXs, aggregators & routing")

video = {
    "id": "lesson-02-0",
    "title": "Lesson 2.0: Mastery Starter",
    "size": [1920, 1080],
    "group": "lessons",
    "maxMinutes": 25,
    "tag": "Lesson 2.0",
    "gold": True,
    "seed": 20,
    "use": "Lesson 2.0 page in the Whop course. Hand-written gold-standard script: the 60-second version, the swap-routing mechanism as a flow3d, the five key words (DEX, pool, price impact, slippage, IL), a risk-free first move, and the mastery ladder as a chart3d. Facts last checked: 2026-09-26.",
    "thumbnail": {"title": "Start trading on-chain", "subtitle": "Lesson 2.0"},
    "scenes": S,
}

out = ROOT / "video-scripts" / "gold" / "lesson-02-0.json"
out.write_text(json.dumps(video, indent=None))
print(f"wrote {out} ({len(S)} scenes)")
