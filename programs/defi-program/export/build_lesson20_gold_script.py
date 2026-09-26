#!/usr/bin/env python3
"""Gold-standard script for Lesson 2.0, the Module 2 Mastery Starter (about
10-15 minutes). Trading On-Chain: executing a swap or LP position
deliberately, understanding price impact, fees, impermanent loss and MEV.
Teaches the module's five words (DEX, liquidity pool, price impact,
slippage, impermanent loss) and the mastery ladder with animated
flows/charts, reusing the module's own lesson diagrams (dex-vs-aggregator,
lp-position, mev-sandwich, order-types) wherever they already cover the
idea. Mirrors the Lesson 1.0 Mastery Starter pattern.

Writes video-scripts/gold/lesson-02-0.json (the generator skips lessons with
a gold script). Spoken text (vo) spells numbers for the voice; cap is the
written caption, same sentences."""
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
EX = "Illustrative categories, not measured data"

# ---------------------------------------------------------------- intro
sc("title", "Lesson two point zero. The Mastery Starter for Module Two: Trading On-Chain. By the end, you'll know the five words this module runs on, and exactly how to tell when you've mastered it.",
   "Lesson 2.0. The Mastery Starter for Module 2: Trading On-Chain. By the end, you'll know the five words this module runs on, and exactly how to tell when you've mastered it.",
   chapter="Intro", eyebrow="Lesson 2.0 · Mastery Starter", num="2.0", title="Trading On-Chain", sub="Your map for Module 2, in pictures.")
sc("pillars", "Here's the plan. First, the sixty-second version: what actually happens when you swap or provide liquidity on-chain. Second, the five words you'll need, each one drawn out. Third, what to have ready before you start. Fourth, your first safe step: comparing a real quote across two venues, without executing. And finally, the mastery ladder, so you know exactly what finishing this module looks like.",
   chapter="Intro", title="What this lesson covers",
   items=[{"icon": "swap", "title": "The 60-second version", "text": "What a swap or LP position actually does"}, {"icon": "book", "title": "Five words", "text": "Drawn out, not just defined"},
          {"icon": "clock", "title": "Before you start", "text": "A little ETH and USDC on a low-fee network"}, {"icon": "target", "title": "The ladder", "text": "How you'll know you've mastered it"}])

# ---------------------------------------------------------------- the 60-second version
sc("statement", "Here's the whole module in one sentence. A swap trades against a pool of tokens priced by a formula, not a person on the other side. Providing liquidity to that same pool earns you a share of trading fees, but it also changes what you actually hold. This module teaches you to do both deliberately, knowing the real cost before you commit.",
   chapter="The 60-second version", kicker="The 60-second version", lines=["A formula prices the trade.", "Know the real cost, before you commit."], sub="Trading and providing liquidity, deliberately.")
img(D + "amm-swap-flow.png", "What a swap actually is",
    "Here's what happens the moment you hit “swap.” You're not trading with another person. You're trading against a pool of two tokens, held by a smart contract, priced by a formula that shifts as the pool's balance shifts. Your trade itself moves that price, a little or a lot depending on size. That's the entire mechanism underneath every DEX trade in this module.",
    chapter="The 60-second version")
sc("statement", "And here's why this module exists at all, in one honest sentence. The quoted price on screen is never quite what you receive. Price impact, pool fees, slippage and gas all take a bite between the number you see and the number that actually lands in your wallet. Knowing exactly how much, before you trade, is the entire skill this module builds.",
   chapter="The 60-second version", kicker="Why this module exists", lines=["The quoted price isn't the received price.", "Knowing the gap, before you trade, is the skill."], sub="Four things take a bite: impact, fees, slippage, gas.")

# ---------------------------------------------------------------- words you'll need
sc("title", "Now, the five words you'll need.", chapter="Words you'll need", eyebrow="Words you'll need", num="5", title="Five words, drawn out",
   sub="DEX · Liquidity pool · Price impact · Slippage · Impermanent loss")
sc("flow", "Word one: DEX, a decentralised exchange. Here's what actually happens when you use one, from your wallet. You connect your wallet directly, no account or sign-up. You choose the two tokens you want to trade. The DEX quotes you a price, pulled from its pools in real time. And you sign one transaction, which settles instantly, on-chain, with no intermediary ever holding your funds.",
   chapter="Words you'll need", title="Using a DEX, from your wallet",
   nodes=[{"label": "Connect your wallet", "sub": "No account, no sign-up", "icon": "wallet"}, {"label": "Choose your tokens", "sub": "The pair you want to trade", "icon": "coins"},
          {"label": "Get a live quote", "sub": "Pulled from its pools in real time", "icon": "eye"}, {"label": "Sign, and it settles", "sub": "On-chain, no intermediary holds funds", "icon": "check"}])
img(D + "lp-position.png", "Word two: liquidity pool",
    "Word two: liquidity pool. A pot of two tokens that traders swap against, funded by people called liquidity providers, or LPs. Deposit both tokens in the pool's ratio, and you receive a share, and a cut of every trade's fee, proportional to your share. But your share of the pool can end up worth a different mix of tokens than what you put in. That's word five, coming up.",
    chapter="Words you'll need")
sc("flow", "Word three: price impact. Not a fee, a mechanical consequence of trade size against pool depth. A small trade against a deep pool barely moves the price at all. The same trade against a shallow pool moves it noticeably, because you're a bigger share of what's actually available. Bigger trade, or shallower pool, means more price impact, every time, by the formula itself, not by anyone's decision.",
   chapter="Words you'll need", title="What decides price impact",
   nodes=[{"label": "Trade size", "sub": "Bigger trades move price more", "icon": "chart"}, {"label": "Pool depth", "sub": "Shallower pools move more, for the same size", "icon": "layers"},
          {"label": "Price impact", "sub": "A mechanical result, not a fee", "icon": "alert"}])
sc("compare", "Word four: slippage, and it's easy to confuse with price impact, so here's the actual difference. Price impact is what your trade itself does to the pool's price, a real cost baked into the trade. Slippage tolerance is a setting you choose: the worst price you'll accept before your transaction simply reverts, protecting you from a price that moves between your quote and your confirmation.",
   chapter="Words you'll need",
   left={"label": "Price impact", "tone": "warn", "items": ["What your trade does to the pool's price", "A real cost, part of the trade itself"]},
   right={"label": "Slippage tolerance", "tone": "good", "items": ["A setting you choose in advance", "The worst price you'll accept before it reverts"]})
sc("stats", "One real, worked number for a liquidity pool, from later in this module. Put ten thousand dollars into a pool as a zero point one percent share, and a typical day might earn around six dollars in fees, which annualises to roughly twenty-two percent, before impermanent loss and gas. That's the number Lesson two point three teaches you to calculate for real, on any pool you're considering.",
   chapter="Words you'll need", stats=[["~22%", "illustrative annualised fee return on a $10,000 / 0.1% pool share, before IL and gas"]])
sc("quiz", "Quick check. What's the actual difference between price impact and slippage tolerance? [[pause 4]] The answer: price impact is what your trade does to the pool's price. Slippage tolerance is a setting you choose: the worst price you'll accept before the transaction reverts.",
   chapter="Words you'll need", n=1, of=4, q="What's the actual difference between price impact and slippage tolerance?",
   a="Price impact is a real cost from your trade; slippage tolerance is a setting protecting the worst price you'll accept.")
sc("chart", "Word five: impermanent loss, from Lesson two point four. Here's the honest shape of it. Hold both tokens yourself, and your value simply tracks the market. Provide the same two tokens as liquidity instead, and if their price ratio moves apart, your LP position ends up worth less than simply holding would have, even after counting the fees you earned. It's called “impermanent” because it only becomes permanent once you withdraw.",
   chapter="Words you'll need", kind="line", title="LP position vs simply holding, as prices diverge", sub=EX,
   series=[{"label": "Simply holding", "tone": "good", "values": [100, 108, 118, 132, 148]}, {"label": "LP position", "tone": "warn", "values": [100, 106, 112, 121, 131]}],
   xlabels=["Start", "", "", "", "Prices diverge"], marks=[{"i": 4, "text": "LP lags holding", "tone": "warn"}])

# ---------------------------------------------------------------- before you start
sc("title", "Before you start.", chapter="Before you start", eyebrow="Before you start", num="2", title="What Module 0 and 1 should have left you with",
   sub="Two things, ready before Lesson 2.1")
sc("bullets", "Two things, both already covered. First, Modules Zero and One done: a secured setup, and safe wallet habits already in place, since you'll be signing real swaps in this module. Second, a little E.T.H. for gas, and some U.S.D.C. to trade with, on a low-fee network. If either is missing, go back and finish those first. This module builds directly on those habits.",
   chapter="Before you start", title="Two things, ready to go", numbered=True,
   items=["Modules 0 & 1 done: secured setup, safe wallet habits", "A little ETH for gas and some USDC, on a low-fee network"])

# ---------------------------------------------------------------- your first safe step
sc("title", "Your first safe step.", chapter="Your first safe step", eyebrow="Your first safe step", num="1", title="Quote it. Don't execute yet.",
   sub="Compare two venues, with real numbers.")
sc("statement", "Your first step in this module doesn't touch a real trade at all. Quote a twenty-dollar swap on one DEX directly, and the same swap on an aggregator, which searches many pools for you. Compare what you'd actually receive after gas, on each. Don't execute either one. You're building the habit of comparing net received, before the habit of trading.",
   chapter="Your first safe step", kicker="Step one", lines=["Quote the same $20 swap,", "on a DEX, and on an aggregator."], sub="Compare net received after gas. Don't execute yet.")
img(D + "dex-vs-aggregator.png", "The worked example",
    "Here's exactly what you're comparing. A single DEX quotes you one price, direct from one pool. An aggregator searches many pools and venues, and may split your order across several routes to get a better net result. Neither is always better; it depends on the size of your trade and how liquidity is spread that day. The habit is checking both, every time, not assuming.",
    chapter="Your first safe step")
sc("compare", "One more routing trade-off worth knowing while you're comparing quotes. A single-pool route touches one contract, simple and predictable, but it might not be the cheapest path available. A multi-hop route, say, token A to B to C, can land a better price by spreading across pools, but it touches more contracts, meaning more that would need to behave correctly for your trade to succeed.",
   chapter="Your first safe step",
   left={"label": "A single-pool route", "tone": "good", "items": ["One contract, simple and predictable", "May not be the cheapest path"]},
   right={"label": "A multi-hop route", "tone": "warn", "items": ["Can land a better net price", "Touches more contracts along the way"]})
sc("quiz", "Quick check. Why compare a DEX quote against an aggregator quote before trading, instead of just picking one? [[pause 4]] The answer: an aggregator searches many pools and can split your order for a better net result, but it isn't always better, so checking both tells you what you'd actually receive.",
   chapter="Your first safe step", n=2, of=4, q="Why compare a DEX quote against an aggregator quote before trading, instead of just picking one?",
   a="Neither is always better; comparing both shows what you'd actually receive.")

# ---------------------------------------------------------------- mastery ladder
sc("title", "The mastery ladder.", chapter="The mastery ladder", eyebrow="The mastery ladder", num="3", title="Three rungs",
   sub="Beginner · Practitioner · Master")
sc("chart", "Here's how you'll measure your progress through Module Two. Beginner: makes small swaps with deliberate slippage settings and protected routing. Practitioner: calculates fee A.P.R. and impermanent loss, and actively tracks an LP position against simply holding. And Master: uses limit, T.W.A.P. and intent-based orders, and runs LP positions with written entry and exit rules.",
   chapter="The mastery ladder", kind="bars", title="The mastery ladder",
   bars=[{"label": "Beginner", "text": "Deliberate slippage, protected routing", "value": 1, "show": "Rung 1", "tone": "blue"},
         {"label": "Practitioner", "text": "Calculates fee APR and IL, tracks vs holding", "value": 2, "show": "Rung 2", "tone": "blue"},
         {"label": "Master", "text": "Limit/TWAP/intent orders, written LP rules", "value": 3, "show": "Rung 3", "tone": "good"}])
sc("bullets", "Here's the road ahead, lesson by lesson. Two point one, D.E.X.s, aggregators and routing. Two point two, A.M.M. mathematics. Two point three, providing liquidity. Two point four, impermanent loss and true L.P. profit and loss. Two point five, M.E.V. and protecting your trades. Two point six, advanced execution: limit, T.W.A.P. and intent orders. Two point seven, advanced A.M.M. design and L.V.R. And two point eight, the M.E.V. supply chain.",
   "Here's the road ahead, lesson by lesson. 2.1, DEXs, aggregators and routing. 2.2, AMM mathematics. 2.3, providing liquidity. 2.4, impermanent loss and true LP P&L. 2.5, MEV and protecting your trades. 2.6, advanced execution: limit, TWAP and intent orders. 2.7, advanced AMM design and LVR. And 2.8, the MEV supply chain.",
   chapter="The mastery ladder", title="The road ahead", numbered=True, compact=True,
   items=["2.1 · DEXs, aggregators & routing", "2.2 · AMM mathematics", "2.3 · Providing liquidity", "2.4 · Impermanent loss & true LP P&L",
          "2.5 · MEV and protecting your trades", "2.6 · Advanced execution: limit/TWAP/intent orders", "2.7 · Advanced AMM design & LVR", "2.8 · The MEV supply chain"])
img(D + "mev-sandwich.png", "One more preview",
    "One more preview, from Lesson two point five. Some of what looks like slippage is actually M.E.V., other traders exploiting the fact that your pending transaction is visible before it confirms. A “sandwich” attack buys just ahead of your trade and sells just after, pushing your price worse both ways. Protecting your trades rounds out this module for exactly that reason.",
    chapter="You've mastered it when…")
sc("statement", "You've mastered this module when you can quote a swap's real cost, and an L.P. position's real result against simply holding, before you ever commit either one. Not a big trade. A repeatable habit of knowing the number first.",
   chapter="You've mastered it when…", kicker="The top rung", lines=["Know the real cost,", "before you ever commit."], sub="Not a big trade. A repeatable habit of knowing the number first.")
sc("quiz", "One more. You provide liquidity to a pool, and the two tokens' prices drift apart over a month. Even after counting the fees you earned, what's this effect called? [[pause 4]] The answer: impermanent loss, how far your LP position lags simply holding the same two tokens, and it only becomes permanent once you withdraw.",
   chapter="You've mastered it when…", n=3, of=4, q="After providing liquidity, the two tokens' prices drift apart. Even after fees, what's this lag against simply holding called?",
   a="Impermanent loss — it only becomes permanent once you withdraw.")
sc("quiz", "Last check. What does mastering Module Two actually look like? [[pause 4]] The answer: quoting a swap's real cost, and an LP position's real result against holding, before you ever commit either one.",
   chapter="You've mastered it when…", n=4, of=4, q="What does mastering Module 2 actually look like?",
   a="Quoting a swap's real cost and an LP position's real result before you commit.")

# ---------------------------------------------------------------- recap
sc("bullets", "Let's recap the five words. DEX: you trade against a pool, no intermediary. Liquidity pool: deposit both tokens, earn a fee share, but your mix can change. Price impact: your own trade moving the price, mechanically. Slippage: the worst price you'll accept, your own setting. And impermanent loss: how far an LP position lags simply holding, once prices diverge.",
   chapter="Recap", title="Recap", check=False,
   items=["DEX: trade against a pool, no intermediary", "Liquidity pool: deposit both tokens; your mix can change",
          "Price impact: your own trade, moving the price", "Slippage: your own worst-acceptable-price setting", "Impermanent loss: how far an LP lags simply holding"])
sc("cta", "That's the Mastery Starter. You now have the whole module in your head: what a swap and an LP position actually do, the five words, your first safe step, and the ladder that tells you when you're done. Next up, Lesson two point one: DEXs, aggregators and routing.",
   "That's the Mastery Starter. You now have the whole module in your head: what a swap and an LP position actually do, the five words, your first safe step, and the ladder that tells you when you're done. Next up, Lesson 2.1: DEXs, aggregators and routing.",
   chapter="Recap", button="Next: Lesson 2.1", sub="DEXs, aggregators and routing")

spec = {"id": "lesson-02-0", "title": "Lesson 2.0: Mastery Starter", "size": [1920, 1080], "group": "lessons", "maxMinutes": 25, "tag": "Lesson 2.0",
        "gold": True, "music": True, "musicLevel": 0.14, "seed": 52,
        "use": "Lesson 2.0 page in the Whop course. Hand-written gold-standard script: the Module 2 Mastery Starter, taught with animated flows and charts.",
        "thumbnail": {"title": "Trading On-Chain", "subtitle": "Lesson 2.0 · Mastery Starter"}, "scenes": S}
out = ROOT / "video-scripts" / "gold" / "lesson-02-0.json"
out.write_text(json.dumps(spec, indent=1, ensure_ascii=False))
words = sum(len(s["vo"].replace("[[pause 4]]", "").split()) for s in S)
print(f"{len(S)} scenes, {words} words, est {(words / 171 * 60 + len(S) * 1.3 + 4 * 3) / 60:.1f} min")
