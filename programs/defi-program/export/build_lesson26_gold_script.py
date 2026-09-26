#!/usr/bin/env python3
"""Gold-standard script for Lesson 2.6, Advanced execution: limit, TWAP and
intent-based orders (target 10-20 minutes). Walks on-chain limit orders,
TWAP orders, intent-based/RFQ trading, their trade-offs, and the source
material's own worked example ($50,000 ETH buy: single trade ~1.5%/~$750
impact vs a 10x$5,000 TWAP vs an intent order sourcing multiple venues), as
visual walk-throughs. Built to the walk-through-first standard: almost
every idea is a flow, steps or callout image, not a statement read over a
static screen.

Writes video-scripts/gold/lesson-02-6.json (the generator skips lessons
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
sc("title", "Lesson two point six. Advanced execution: limit, T.W.A.P. and intent-based orders. By the end, you'll use order types that give you better prices and protection than a plain swap.",
   "Lesson 2.6. Advanced execution: limit, TWAP and intent-based orders. By the end, you'll use order types that give you better prices and protection than a plain swap.",
   chapter="Intro", eyebrow="Lesson 2.6", num="2.6", title="Advanced execution", sub="Better than a plain swap, for the right trade.")
sc("pillars", "Here's the plan. On-chain limit orders, and the one real risk they carry. T.W.A.P. orders, and exactly why slicing a trade reduces its impact. Intent-based trading, and who actually fills your order. And a full worked example, comparing all three, on the exact same fifty-thousand-dollar trade.",
   chapter="Intro", title="What this lesson covers",
   items=[{"icon": "target", "title": "Limit orders", "text": "Fills only at your price, or not at all"}, {"icon": "clock", "title": "TWAP orders", "text": "Sliced over time, to reduce impact"},
          {"icon": "users", "title": "Intent-based / RFQ", "text": "Solvers compete to fill your order"}, {"icon": "chart", "title": "Worked example", "text": "$50,000, compared three ways"}])

# ---------------------------------------------------------------- on-chain limit orders
sc("title", "On-chain limit orders.", chapter="On-chain limit orders", eyebrow="On-chain limit orders", num="1", title="Fills at your price, or not at all",
   sub="Usually gasless, until it fills.")
sc("flow", "Here's exactly how an on-chain limit order works, step by step. You sign an order off-chain, something like “sell one E.T.H. at three thousand three hundred or better.” That order sits, waiting, usually costing no gas at all while it waits. It fills only once the market actually reaches your price. And if the market never gets there, it simply never fills, at no cost to you either way.",
   chapter="On-chain limit orders", title="How a limit order actually works",
   nodes=[{"label": "You sign an order off-chain", "sub": "“sell 1 ETH at 3,300 or better”", "icon": "eye"}, {"label": "It waits, usually gasless", "sub": "No cost while it's unfilled", "icon": "clock"},
          {"label": "Fills only at your price", "sub": "Or better", "icon": "check"}, {"label": "Never reached? Never fills", "sub": "No cost, either way", "icon": "alert"}])
sc("statement", "Here's the one real risk worth naming plainly, since a limit order isn't a strictly better version of a swap. If the price never reaches your chosen level, your order simply never fills, and you may miss a move you actually wanted to be part of. It's not a downside cost. It's an opportunity you didn't take, which is its own kind of cost.",
   chapter="On-chain limit orders", kicker="The one real risk", lines=["It may never fill.", "Not a cost — a missed opportunity, its own kind of cost."], sub="Set it, knowing that trade-off going in.")
sc("compare", "Worth being clear about when each one actually fits, since neither is universally better. A limit order fits when you're patient, and have a specific price in mind you'd genuinely be happy with, with no urgency to act right now. A plain swap fits when you need the trade to happen now, at whatever the current price actually is, urgency outweighing getting a specific number.",
   chapter="On-chain limit orders",
   left={"label": "A limit order fits when…", "tone": "good", "items": ["You're patient, no urgency", "You have a specific acceptable price in mind"]},
   right={"label": "A plain swap fits when…", "tone": "good", "items": ["You need it to happen now", "Urgency outweighs getting a specific number"]})
sc("quiz", "Quick check. What's the actual risk of placing an on-chain limit order? [[pause 4]] The answer: it may simply never fill, if the market never reaches your chosen price, which can mean missing a move you wanted to be part of.",
   chapter="On-chain limit orders", n=1, of=3, q="What's the actual risk of placing an on-chain limit order?",
   a="It may never fill, if the market never reaches your price.")

# ---------------------------------------------------------------- twap orders
sc("title", "TWAP orders.", chapter="TWAP orders", eyebrow="TWAP orders", num="2", title="Splitting one trade into many, over time",
   sub="Less impact per slice, from Lesson 2.2's own curve.")
sc("flow", "Here's exactly what a T.W.A.P. order does, mechanically. Take one large trade, and split it into many equal, smaller slices. Execute those slices spread out over a set period of time, not all at once. Each slice, being far smaller, sits much further back on the price-impact curve from Lesson two point two, so it moves the price far less individually. And the total impact, summed across every slice, comes out lower than one trade of the full size.",
   chapter="TWAP orders", title="How a TWAP order actually works",
   nodes=[{"label": "One large trade", "sub": "Split into many equal slices", "icon": "layers"}, {"label": "Executed over time", "sub": "Spread out, not all at once", "icon": "clock"},
          {"label": "Each slice: less impact", "sub": "Further back on the same curve", "icon": "chart"}, {"label": "Lower total impact", "sub": "Summed across every slice", "icon": "check"}])
sc("statement", "Here's the trade-off a T.W.A.P. order actually carries, worth naming honestly. It takes real time to execute, by design, since that's exactly what reduces the impact. And during that window, the price can simply move against you, for reasons that have nothing to do with your own trade at all. Less impact from your own size. Real exposure to the market moving, meanwhile.",
   chapter="TWAP orders", kicker="The trade-off, honestly", lines=["Takes real time, by design.", "The price can move against you, meanwhile."], sub="Less impact from your size. Real exposure to the market, meanwhile.")
sc("steps", "Here's what actually setting one up looks like, in practice, on a wallet or aggregator that offers it. Choose your total trade size, and how many slices to split it into. Choose the time window it executes across, balancing less impact against more market exposure. And let it run; most implementations execute the remaining slices automatically, without a separate signature each time.",
   chapter="TWAP orders", title="Setting up a TWAP order, in practice",
   steps=["Choose total size, and number of slices", "Choose the time window, balancing impact vs exposure", "Let it run — most execute automatically"], result="No separate signature needed per slice, on most implementations")
sc("quiz", "Quick check. Why does splitting a large trade into a TWAP actually reduce total price impact? [[pause 4]] The answer: smaller slices sit further back on the price-impact curve, so each one moves the price less individually, even though the same total size eventually goes through.",
   chapter="TWAP orders", n=2, of=3, q="Why does splitting a large trade into a TWAP actually reduce total price impact?",
   a="Smaller slices cause less price impact each, on the same curve.")

# ---------------------------------------------------------------- intent-based / rfq
sc("title", "Intent-based trading.", chapter="Intent-based / RFQ", eyebrow="Intent-based / RFQ", num="3", title="You state what you want. Solvers compete to fill it.",
   sub="Often with MEV protection built in.")
img(D + "order-types.png", "How an intent-based order actually works",
    "Here's the actual mechanism behind intent-based, or R.F.Q., trading. You state your intent plainly: “one hundred thousand U.S.D.C. into E.T.H., at least this much back.” Competing solvers, or market makers, see that intent and compete to fill it, sourcing liquidity from wherever they can find it, often across several venues at once. You get the best fill any solver was willing to offer, frequently with M.E.V. protection built in, and no gas paid on a failed attempt.",
    chapter="Intent-based / RFQ")
sc("compare", "Worth naming the one real trade-off intent-based trading carries, since “solvers compete” can sound like a free upgrade. Your actual fill quality depends entirely on how many solvers are actively competing for your specific order, and how well that particular protocol's solver system is designed. A thin solver market, or a poorly designed one, can leave you with a fill no better than a plain swap.",
   chapter="Intent-based / RFQ",
   left={"label": "A healthy solver market", "tone": "good", "items": ["Many solvers, actively competing", "Genuinely better fills, often MEV-protected"]},
   right={"label": "A thin solver market", "tone": "warn", "items": ["Few solvers, or a weak design", "May fill no better than a plain swap"]})
sc("stats", "One real number, so intent-based trading doesn't feel like a niche experiment. Industry trackers have recorded intent-based and R.F.Q.-style trading growing to a meaningful share of total on-chain swap volume in recent years, across multiple chains. This is outside research, not this program's own data, but it's real, current infrastructure, worth actually comparing, not skipping past.",
   chapter="Intent-based / RFQ", stats=[["Growing share", "of on-chain swap volume now runs through intent/RFQ systems (outside research)"]])
sc("quiz", "Quick check. Who actually fills an intent-based order, and what do they compete on? [[pause 4]] The answer: competing solvers or market makers, who compete to offer you the best fill for what you stated you wanted, often sourcing liquidity from several venues at once.",
   chapter="Intent-based / RFQ", n=3, of=3, q="Who actually fills an intent-based order, and what do they compete on?",
   a="Competing solvers or market makers, competing to offer the best fill.")

# ---------------------------------------------------------------- worked example
sc("title", "Worked example.", chapter="Worked example", eyebrow="Worked example", num="1", title="Buying $50,000 of ETH, three ways",
   sub="Real numbers, from the source material.")
sc("stats", "Here's the baseline this entire comparison starts from. A single fifty-thousand-dollar trade, in this specific pool, carries roughly one point five percent price impact, which is about seven hundred fifty dollars, straight out of the same formula from Lesson two point two.",
   "Here's the baseline this entire comparison starts from. A single $50,000 trade, in this specific pool, carries roughly 1.5% price impact, which is about $750, straight out of the same formula from Lesson 2.2.",
   chapter="Worked example", stats=[["~1.5% / ~$750", "a single $50,000 trade, straight impact"]])
sc("flow", "Now the T.W.A.P. alternative, on the exact same fifty thousand dollars. Split it into ten slices, of five thousand dollars each. Execute those ten slices spread across one hour. Each slice, being a tenth of the size, carries far less impact individually. And the total impact across all ten slices comes out well below the seven hundred fifty dollars a single trade would have cost, as long as the price doesn't trend against you during that hour.",
   chapter="Worked example", title="The TWAP alternative: 10 × $5,000",
   nodes=[{"label": "Split into 10 × $5,000", "sub": "Same total, ten equal slices", "icon": "layers"}, {"label": "Spread across one hour", "sub": "Not all at once", "icon": "clock"},
          {"label": "Each slice: far less impact", "sub": "A tenth of the size, on the same curve", "icon": "chart"}, {"label": "Total: well below $750", "sub": "As long as price doesn't trend against you", "icon": "check"}])
sc("statement", "And the third option, on that same fifty thousand dollars, works completely differently again. An intent-based order may beat both of the other two, by sourcing liquidity from several venues at once, through competing solvers, rather than working against a single pool's depth at all. The only way to actually know, on any given day, is to compare all three quotes side by side, not assume one always wins.",
   chapter="Worked example", kicker="The intent-based option", lines=["May beat both, sourcing several venues at once.", "The only way to know: compare all three quotes."], sub="Don't assume one always wins — compare, every time.")
sc("compare", "Put all three side by side, for this exact fifty-thousand-dollar trade, and here's the actual decision. A single swap: instant, but the full seven hundred fifty dollars of impact, all at once. A T.W.A.P.: less impact, but real time exposure to the price moving during that hour. An intent order: potentially the best of all three, but only as good as that protocol's actual solver competition, that day.",
   chapter="Worked example",
   left={"label": "Single swap", "tone": "warn", "items": ["Instant", "Full ~$750 impact, all at once"]},
   right={"label": "TWAP, or intent order", "tone": "good", "items": ["Less impact, or a competed-for fill", "Real time exposure, or solver-dependent quality"]})

# ---------------------------------------------------------------- checklist and recap
sc("steps", "Here's how to actually get all three quotes yourself, before committing to any of them. Get a standard swap quote, direct or through an aggregator, as your baseline. Check whether that same venue or wallet offers a T.W.A.P. option, and get its estimated total impact. And check whether an intent-based venue is available for this pair, and get its quote too, before picking whichever nets the most.",
   chapter="Worked example", title="Getting all three quotes yourself",
   steps=["A standard swap quote, as your baseline", "A TWAP option's estimated total impact, if offered", "An intent-based quote, if available for this pair"], result="Pick whichever nets the most — don't default to one")
sc("steps", "Here's your checklist. Do it now, on every large trade. Compare a plain swap, a T.W.A.P., and an intent-based quote, side by side, before choosing. Any limit order you place has an expiry you've actually chosen, not left indefinite. And you know, specifically, which order types you're using include M.E.V. protection, and which don't.",
   chapter="Checklist", title="Your checklist",
   steps=["Compare a plain swap, a TWAP, and an intent quote", "Limit orders: an expiry you've chosen", "Know which order types include MEV protection"])
sc("statement", "One last honest point, before the recap, since these three tools can sound like they replace everything earlier in this module. They don't replace slippage discipline, checking price impact, or protected routing from Lesson two point five. They sit on top of those habits, giving you more ways to execute a trade well, not a reason to skip the checks that still apply to every single one of them.",
   chapter="Recap", kicker="What these tools don't replace", lines=["Not a replacement for the earlier habits.", "More ways to execute well — the checks still apply."], sub="Slippage discipline and protected routing, on every one of them.")
sc("bullets", "Let's recap. On-chain limit orders fill only at your price, usually gasless while waiting, but may simply never fill. T.W.A.P. orders slice a large trade over time, reducing impact per slice, at the cost of real time exposure to the market moving. Intent-based trading lets competing solvers fill your order, often with M.E.V. protection, but only as good as that protocol's actual solver competition. And for any trade of real size, comparing all three is the actual habit, not picking one by default.",
   chapter="Recap", title="Recap", check=False,
   items=["Limit orders: fill at your price, or never — usually gasless", "TWAP: slices over time, less impact, real time exposure",
          "Intent/RFQ: solvers compete, often MEV-protected", "For real size: compare all three, don't default to one"])
sc("cta", "Compare a plain swap, a TWAP, and an intent quote, before your next large trade. Next up, Lesson two point seven: Advanced AMM design and LVR.",
   "Compare a plain swap, a TWAP, and an intent quote, before your next large trade. Next up, Lesson 2.7: Advanced AMM design and LVR.",
   chapter="Recap", button="Next: Lesson 2.7", sub="Advanced AMM design and LVR")

spec = {"id": "lesson-02-6", "title": "Lesson 2.6: Advanced execution (limit, TWAP, intent-based orders)", "size": [1920, 1080], "group": "lessons", "maxMinutes": 25,
        "tag": "Lesson 2.6", "gold": True, "music": True, "musicLevel": 0.14, "seed": 58,
        "use": "Lesson 2.6 page in the Whop course. Hand-written gold-standard script: on-chain limit orders, TWAP orders, intent-based/RFQ trading, and the source material's own $50,000 worked example comparing all three, as walk-throughs.",
        "thumbnail": {"title": "Advanced execution", "subtitle": "Lesson 2.6 · Limit, TWAP, intent"}, "scenes": S}
out = ROOT / "video-scripts" / "gold" / "lesson-02-6.json"
out.write_text(json.dumps(spec, indent=1, ensure_ascii=False))
words = sum(len(s["vo"].replace("[[pause 4]]", "").split()) for s in S)
print(f"{len(S)} scenes, {words} words, est {(words / 171 * 60 + len(S) * 1.3 + 4 * 3) / 60:.1f} min")
