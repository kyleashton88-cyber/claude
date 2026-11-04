#!/usr/bin/env python3
"""Gold-standard script for Lesson 2.5, MEV and protecting your trades
(target 10-20 minutes). Walks what MEV actually is, the sandwich attack
mechanism, the real defences, and the source material's own worked example
($20,000 swap: 3% slippage exposes ~$600, 0.5% exposes ~$100, a private
route removes the exposure entirely), as visual walk-throughs. Built to the
walk-through-first standard: almost every idea is a flow, steps or callout
image, not a statement read over a static screen.

Writes video-scripts/gold/lesson-02-5.json (the generator skips lessons
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

# ---------------------------------------------------------------- intro
sc("title", "Lesson two point five. MEV and protecting your trades. By the end, you'll set slippage and routing so your trades aren't easy targets.",
   "Lesson 2.5. MEV and protecting your trades. By the end, you'll set slippage and routing so your trades aren't easy targets.",
   chapter="Intro", eyebrow="Lesson 2.5", num="2.5", title="MEV and protecting your trades", sub="Your slippage setting is a bot's profit ceiling.")
sc("pillars", "Here's the plan. What M.E.V. actually is, and which kind of it actually hurts you. The sandwich attack, mechanically, step by step. The real defences that work, and why. And a full worked example, with real numbers, showing exactly what your own slippage setting exposes you to.",
   chapter="Intro", title="What this lesson covers",
   items=[{"icon": "eye", "title": "What MEV actually is", "text": "Profit from ordering transactions in a block"}, {"icon": "alert", "title": "The sandwich attack", "text": "Step by step, mechanically"},
          {"icon": "shield", "title": "The real defences", "text": "Slippage, routing, splitting, pool depth"}, {"icon": "target", "title": "Worked example", "text": "$20,000, at different slippage settings"}])

# ---------------------------------------------------------------- what mev actually is
sc("title", "What MEV actually is.", chapter="What MEV actually is", eyebrow="What MEV actually is", num="1", title="Profit from ordering transactions",
   sub="Some of it's harmless. Some of it targets you.")
sc("statement", "Here's the precise definition, worth getting right before anything else. M.E.V., maximal extractable value, is profit taken by whoever decides the order transactions land in, inside a block. Some M.E.V. is genuinely harmless, arbitrage that simply realigns a pool's price with the wider market, the exact mechanism from Lesson two point two. The kind that actually hurts you is different, and it specifically targets your own pending trade.",
   chapter="What MEV actually is", kicker="Some MEV is harmless", lines=["Profit from ordering transactions.", "Arbitrage realigns prices. This lesson is about the kind that targets you."], sub="Specifically, your own pending trade.")
sc("stats", "One real, dated number, so this isn't an abstract worry. Blockchain researchers have tracked hundreds of millions of dollars extracted from traders through sandwich attacks and similar MEV, across multiple years of on-chain activity. This is outside research, not this program's own data, but it's exactly why the defences in this lesson are worth setting up before your next large trade, not after a bad one.",
   chapter="What MEV actually is", stats=[["$100Ms+", "extracted via sandwich/MEV attacks, tracked across years (outside research)"]])
sc("compare", "Put the two kinds of M.E.V. side by side, since telling them apart is the whole point of this chapter. Arbitrage M.E.V. reacts to a price that's already out of line, and its actual effect is to correct it, closer to the wider market. Sandwich M.E.V. creates the bad price itself, purely to profit from your specific trade, and leaves nothing corrected once it's done.",
   chapter="What MEV actually is",
   title="Arbitrage vs sandwich MEV", left={"label": "Arbitrage MEV", "tone": "good", "items": ["Reacts to a price already out of line", "Corrects it, closer to the wider market"]},
   right={"label": "Sandwich MEV", "tone": "bad", "items": ["Creates the bad price itself", "Profits from your trade; corrects nothing"]})
sc("quiz", "Quick check. Is all MEV harmful to you as a trader? [[pause 4]] The answer: no. Arbitrage that realigns a pool's price with the wider market is a harmless form of MEV. This lesson is about the specific kind that targets your own pending trade.",
   chapter="What MEV actually is", n=1, of=3, q="Is all MEV harmful to you as a trader?",
   a="No — arbitrage MEV is harmless. This lesson is about the kind that targets your trade.")

# ---------------------------------------------------------------- the sandwich attack
sc("title", "The sandwich attack.", chapter="The sandwich attack", eyebrow="The sandwich attack", num="2", title="Your slippage setting is its profit ceiling",
   sub="Step by step, mechanically.")
img(D + "mev-sandwich.png", "How a sandwich actually works",
    "Here's exactly how a sandwich attack unfolds, in order. A bot watches the public mempool, and sees your pending swap before it confirms. It buys the same token, just ahead of you, pushing the price up. Your trade then executes, at that now-worse price. And the bot immediately sells, just after you, capturing the gap it created. Your trade is the bread. The bot's two trades are the filling.",
    chapter="The sandwich attack")
sc("flow", "Here's why your own slippage tolerance is exactly what caps how much a sandwich can actually take from you, mechanically. Your slippage setting defines the single worst price you'll accept before the transaction simply reverts. A sandwich bot can only push the price as far as that ceiling allows, since pushing further would just cause your trade to fail entirely, earning it nothing. Your own setting is, literally, its profit ceiling.",
   chapter="The sandwich attack", title="Why your slippage setting is the ceiling",
   nodes=[{"label": "You set a slippage tolerance", "sub": "The worst price you'll accept", "icon": "eye"}, {"label": "Bot pushes price toward it", "sub": "But no further, or you'd revert", "icon": "alert"},
          {"label": "Your trade executes there", "sub": "At the worst price your setting allows", "icon": "swap"}, {"label": "That gap is the bot's profit", "sub": "Capped by your own setting", "icon": "coins"}])
sc("steps", "Here's how to actually check, after the fact, whether a past trade of yours was sandwiched. Pull up your transaction on a block explorer. Look at the two transactions immediately before and after yours, in the same block. If the same address bought the identical token right before you, and sold it right after, that's the signature of a sandwich, not a coincidence.",
   chapter="The sandwich attack", title="Checking a past trade for a sandwich",
   steps=["Pull up your transaction on a block explorer", "Look at the two transactions immediately around it", "Same address, buying before and selling after: that's a sandwich"], result="A pattern, not a coincidence, once you know what to look for")
sc("quiz", "Quick check. What specifically limits how much a sandwich bot can extract from your trade? [[pause 4]] The answer: your own slippage tolerance, and the pool's depth. The bot can't push the price further than your setting allows, or your transaction simply reverts.",
   chapter="The sandwich attack", n=2, of=3, q="What specifically limits how much a sandwich bot can extract from your trade?",
   a="Your slippage tolerance, and the pool's depth.")

# ---------------------------------------------------------------- the real defences
sc("title", "The real defences.", chapter="The real defences", eyebrow="The real defences", num="3", title="What actually works, and why",
   sub="Four defences, each closing a different door.")
sc("steps", "Here are the four defences that actually work, in the order most worth setting up. Tight but realistic slippage, something like zero point one to zero point five percent for liquid major pairs, looser only when you specifically understand why. M.E.V.-protected or private transaction routing, offered by many wallets and aggregators directly. Split large trades, so no single trade is a big enough target. And avoid broadcasting huge swaps into thin, illiquid pairs.",
   chapter="The real defences", title="The four defences, in order",
   steps=["Tight, realistic slippage (~0.1–0.5% for liquid majors)", "MEV-protected / private transaction routing", "Split large trades into smaller ones", "Avoid huge swaps in thin, illiquid pairs"], result="Each closes a different door a sandwich bot needs")
sc("flow", "Zoom into the private-routing defence specifically, since it works completely differently from tightening slippage. A normal transaction sits visibly in the public mempool, where any bot can see it before it confirms. A private or protected route instead sends your transaction directly, never appearing in that public mempool at all. With nothing to see, there's simply nothing for a sandwich bot to react to.",
   chapter="The real defences", title="Why private routing works differently",
   nodes=[{"label": "Normal transaction", "sub": "Visible in the public mempool", "icon": "eye"}, {"label": "A bot can see it, pending", "sub": "Before it ever confirms", "icon": "alert"},
          {"label": "Private route instead", "sub": "Sent directly, never public", "icon": "lock"}, {"label": "Nothing to react to", "sub": "No sandwich is possible from there", "icon": "shield"}])
sc("steps", "Here's what turning on protected routing actually looks like, in practice, since it's simpler than it sounds. Check whether your wallet or aggregator offers a “private,” “protected,” or “M.E.V.-secure” routing option directly in its settings. Switch it on, ideally as your default for anything above a small size. And confirm the transaction still lands normally; a private route changes where it's broadcast, not whether it eventually confirms.",
   chapter="The real defences", title="Turning on protected routing",
   steps=["Check your wallet/aggregator for a “protected” or “private” option", "Switch it on, as your default above a small size", "Confirm it still lands normally — just broadcast differently"], result="Simpler than it sounds; most major wallets offer this")
sc("compare", "Worth being precise about the one mistake this lesson keeps circling back to, since it's the opposite failure to a sandwich. Slippage set too loose leaves room for a sandwich to profit inside it. Slippage set too tight, near zero, on a genuinely volatile pair, just makes ordinary price movement cause your transaction to fail outright, and a failed transaction still costs you the gas, from Lesson one point two.",
   chapter="The real defences",
   title="Slippage: too loose vs too tight", left={"label": "Too loose", "tone": "bad", "items": ["Leaves room for a sandwich to profit", "The exact exposure this lesson measures"]},
   right={"label": "Too tight", "tone": "bad", "items": ["Ordinary price movement causes it to fail", "A failed transaction still costs gas"]})

# ---------------------------------------------------------------- worked example
sc("title", "Worked example.", chapter="Worked example", eyebrow="Worked example", num="1", title="Swapping $20,000, three ways",
   sub="Real numbers, from the source material.")
sc("stats", "Here's the exposure, at a slippage tolerance of three percent, on a twenty-thousand-dollar swap. Up to roughly six hundred dollars, is the most a sandwich could take, before its own costs, since three percent of twenty thousand is exactly six hundred.",
   "Here's the exposure, at a slippage tolerance of three percent, on a $20,000 swap. Up to roughly $600 is the most a sandwich could take, before its own costs, since 3% of $20,000 is exactly $600.",
   chapter="Worked example", stats=[["~$600 exposed", "3% slippage tolerance, on a $20,000 swap"]])
sc("compare", "Now tighten that same swap to zero point five percent slippage, and see how directly the exposure shrinks with it. At three percent, up to roughly six hundred dollars is exposed. At zero point five percent, that drops to roughly one hundred dollars, a six-fold reduction, from tightening one single setting, on the exact same trade.",
   chapter="Worked example",
   title="3% vs 0.5% slippage tolerance", left={"label": "3% slippage tolerance", "tone": "bad", "items": ["Up to ~$600 exposed", "1.5% of the full $20,000 trade"]},
   right={"label": "0.5% slippage tolerance", "tone": "good", "items": ["Up to ~$100 exposed", "A 6× reduction, same trade"]})
sc("chart", "Plot exposure against slippage tolerance across a wider range, and the relationship is exactly as direct as it looks. Three percent slippage exposes roughly six hundred dollars. One percent exposes roughly two hundred. Zero point five percent, one hundred. And zero point one percent, roughly twenty dollars, though at that tightness, ordinary price movement starts making the trade fail outright, exactly the trade-off from a moment ago.",
   chapter="Worked example", kind="line", title="Exposure vs slippage tolerance, on a $20,000 swap", sub="Illustrative — roughly linear with your setting",
   series=[{"values": [600, 200, 100, 20], "tone": "bad"}], xlabels=["3%", "1%", "0.5%", "0.1%"], yticks=[[20, "$20"], [600, "$600"]], ymin=0, ymax=650,
   marks=[{"i": 3, "text": "This tight: risk of failed tx instead", "tone": "warn", "below": False}])
sc("statement", "And here's the third option, which isn't a tighter number at all, but a different mechanism entirely. Route that same twenty-thousand-dollar swap through a private or protected transaction path, and it's never visible in the public mempool in the first place. Not a smaller exposure. Effectively no exposure to a sandwich, from that route, at all.",
   chapter="Worked example", kicker="The third option, not a smaller number", lines=["Private routing: never visible.", "Not smaller exposure — no exposure, from that route."], sub="A different mechanism, not a tighter setting.")
sc("quiz", "Quick check. Why does setting slippage tolerance near zero on a genuinely volatile pair actually backfire? [[pause 4]] The answer: ordinary price movement makes the transaction revert, and a failed transaction still costs you gas, so you've paid without the trade even happening.",
   chapter="Worked example", n=3, of=3, q="Why does setting slippage tolerance near zero on a genuinely volatile pair actually backfire?",
   a="Ordinary price movement makes it revert, and you still pay gas on the failure.")

# ---------------------------------------------------------------- checklist and recap
sc("compare", "One last reason splitting large trades specifically works, worth naming before the checklist. A sandwich bot pays its own gas, twice, to set up and close its attack, so it needs enough expected profit to justify that cost. A large trade, sandwiched once, can easily clear that bar. That same total value, split into several smaller trades, may simply not be worth attacking, individually, at all.",
   chapter="Checklist",
   title="One large trade vs several smaller", left={"label": "One large trade", "tone": "bad", "items": ["Clears the bot's own gas cost easily", "A worthwhile target, on its own"]},
   right={"label": "Split into smaller trades", "tone": "good", "items": ["Each one, individually, may not be worth it", "The bot's gas cost has to be justified each time"]})
sc("steps", "Here's your checklist. Do it now, on every trade of real size. Slippage is set specifically for this pair and this size, never left on whatever high default the interface picked. Protected or private routing is switched on for larger swaps. And large orders are split, or routed through genuinely deep liquidity, not broadcast as one big, visible target.",
   chapter="Checklist", title="Your checklist",
   steps=["Slippage set for this pair and size, not a high default", "Protected routing on for larger swaps", "Large orders split, or routed through deep liquidity"])
sc("bullets", "Let's recap. M.E.V. is profit from ordering transactions in a block; arbitrage is harmless, sandwiching your own pending trade isn't. A sandwich bot's profit is capped by your own slippage tolerance, mechanically. Tight, realistic slippage, protected routing, splitting large trades and avoiding thin pools are the four defences that actually work. And private routing removes your exposure entirely, rather than just shrinking it.",
   chapter="Recap", title="Recap", check=False,
   items=["MEV: profit from ordering transactions — arbitrage is harmless", "A sandwich's profit is capped by your own slippage setting",
          "Four defences: tight slippage, protected routing, splitting, deep pools", "Private routing removes exposure entirely, not just shrinks it"])
sc("statement", "One last honest note, before you go set these up. None of these four defences make you invisible or untouchable; they raise the cost and shrink the payoff of attacking you, which is what actually changes a bot's decision to bother. Layered together, tight slippage, protected routing, splitting, deep pools, they cover almost every realistic case this lesson describes.",
   chapter="Recap", kicker="What these defences actually do", lines=["Not invisible. Not untouchable.", "Raise the cost, shrink the payoff — layered together."], sub="That's what changes a bot's decision to bother at all.")
sc("cta", "Set slippage for this specific pair and size, and switch on protected routing before your next large swap. Next up, Lesson two point six: Advanced execution, limit, T.W.A.P. and intent-based orders.",
   "Set slippage for this specific pair and size, and switch on protected routing before your next large swap. Next up, Lesson 2.6: Advanced execution, limit, TWAP and intent-based orders.",
   chapter="Recap", button="Next: Lesson 2.6", sub="Advanced execution: limit, TWAP and intent-based orders")

spec = {"id": "lesson-02-5", "title": "Lesson 2.5: MEV and protecting your trades", "size": [1920, 1080], "group": "lessons", "maxMinutes": 25,
        "tag": "Lesson 2.5", "gold": True, "music": True, "musicLevel": 0.14, "seed": 57,
        "use": "Lesson 2.5 page in the Whop course. Hand-written gold-standard script: what MEV actually is, the sandwich-attack mechanism, the real defences, and the source material's own $20,000 worked example at different slippage settings, as walk-throughs.",
        "thumbnail": {"title": "MEV & protecting your trades", "subtitle": "Lesson 2.5"}, "scenes": S}
out = ROOT / "video-scripts" / "gold" / "lesson-02-5.json"
out.write_text(json.dumps(spec, indent=1, ensure_ascii=False))
words = sum(len(s["vo"].replace("[[pause 4]]", "").split()) for s in S)
print(f"{len(S)} scenes, {words} words, est {(words / 171 * 60 + len(S) * 1.3 + 4 * 3) / 60:.1f} min")
