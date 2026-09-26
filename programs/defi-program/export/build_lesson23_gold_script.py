#!/usr/bin/env python3
"""Gold-standard script for Lesson 2.3, Providing liquidity (target 10-20
minutes). Walks what LPing actually does (depositing both tokens, becoming
the counterparty to every trade), the fee-APR formula and why 30-day volume
matters, and the source material's own worked example ($10M TVL pool, $2M
30-day volume, 0.3% fee, $10,000 deposit -> ~21.9% fee APR), as visual
walk-throughs. Built to the walk-through-first standard: almost every idea
is a flow, steps or callout image, not a statement read over a static
screen.

Writes video-scripts/gold/lesson-02-3.json (the generator skips lessons
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
sc("title", "Lesson two point three. Providing liquidity. By the end, you'll estimate an LP position's fee income from real pool data, before you ever deposit.",
   "Lesson 2.3. Providing liquidity. By the end, you'll estimate an LP position's fee income from real pool data, before you ever deposit.",
   chapter="Intro", eyebrow="Lesson 2.3", num="2.3", title="Providing liquidity", sub="Estimate the real income, before you deposit.")
sc("pillars", "Here's the plan. What providing liquidity actually does to your position, not just the fees it earns. The fee A.P.R. formula, spelled out piece by piece, and why thirty-day volume is the number to use. And a full worked example, with real numbers, showing exactly how a ten-thousand-dollar deposit turns into an actual daily and annual return.",
   chapter="Intro", title="What this lesson covers",
   items=[{"icon": "layers", "title": "What LPing actually does", "text": "You become the counterparty to every trade"}, {"icon": "chart", "title": "The fee APR formula", "text": "Piece by piece, and why 30-day volume"},
          {"icon": "target", "title": "Worked example", "text": "$10,000 into a real pool, real numbers"}, {"icon": "check", "title": "Your checklist", "text": "What to have decided before depositing"}])

# ---------------------------------------------------------------- what lping actually does
sc("title", "What LPing actually does.", chapter="What LPing actually does", eyebrow="What LPing actually does", num="1", title="You're not just earning fees",
   sub="You're taking the other side of every trade.")
img(D + "lp-position.png", "Depositing into a pool",
    "Here's the mechanics of becoming a liquidity provider. You deposit both tokens, in the pool's ratio, not just one. In return, you receive a share, a token, or an N.F.T. if it's a concentrated position, covered in Lesson two point seven. That share entitles you to your proportional cut of every swap fee the pool earns, for as long as you hold it.",
    chapter="What LPing actually does")
sc("statement", "Here's the part that's easy to skip past, and shouldn't be. When you provide liquidity, you're not a passive lender collecting interest. You become the counterparty to every single trade that goes through that pool. When a trader buys the token that's rising, they're buying it from the pool, meaning from you. That's exactly where impermanent loss, covered fully in Lesson two point four, actually comes from.",
   chapter="What LPing actually does", kicker="Not a passive lender", lines=["You're the counterparty,", "to every trade that goes through the pool."], sub="That's exactly where impermanent loss comes from.")
sc("compare", "Worth naming the two position types you'll actually choose between, even though this lesson focuses on the simpler one. A full-range position covers every possible price, simple to reason about, earning fees on the whole curve. A concentrated position, an NFT instead of a token, covers only a price band you choose, which can earn far more fee income inside that band, but earns nothing at all once price moves outside it.",
   chapter="What LPing actually does",
   left={"label": "Full-range position", "tone": "good", "items": ["Covers every possible price", "Simpler; earns fees across the whole curve"]},
   right={"label": "Concentrated position (an NFT)", "tone": "warn", "items": ["Covers only a price band you choose", "Can earn much more inside it; nothing outside it"]})
sc("flow", "Here's what actually happens when you eventually withdraw, since it's the moment your changed token mix becomes real. You redeem your share, your L.P. token or N.F.T., back to the pool. The pool returns whatever mix of the two tokens your share is currently worth, at today's ratio, not the ratio you originally deposited at. And you collect the accumulated fees your share has earned, on top of that mix.",
   chapter="What LPing actually does", title="What happens when you withdraw",
   nodes=[{"label": "You redeem your share", "sub": "Your LP token or NFT", "icon": "layers"}, {"label": "Pool returns today's mix", "sub": "At today's ratio, not your entry ratio", "icon": "swap"},
          {"label": "Plus accumulated fees", "sub": "Your share of everything earned", "icon": "coins"}, {"label": "That mix is now real", "sub": "Whatever it changed into, along the way", "icon": "check"}])
sc("compare", "One practical option worth knowing before you assume you always need both tokens ready. Some protocols accept a single-sided deposit, and swap half of it internally to build your pool position for you. The trade-off: that internal swap has its own price impact and fee, paid once, up front, versus depositing both tokens yourself, which needs no internal swap at all, but does need you to already hold the right ratio.",
   chapter="What LPing actually does",
   left={"label": "Depositing both tokens yourself", "tone": "good", "items": ["No internal swap needed", "You need the right ratio already"]},
   right={"label": "A single-sided deposit", "tone": "warn", "items": ["Convenient — no need to hold both first", "Pays a one-time swap cost and price impact"]})
sc("quiz", "Quick check. When you provide liquidity, what does becoming “the counterparty to every trade” actually mean for your position? [[pause 4]] The answer: as traders move the price, your token mix changes with it, since you're the one supplying whichever token they're buying, which is exactly where impermanent loss comes from.",
   chapter="What LPing actually does", n=1, of=3, q="When you provide liquidity, what does becoming “the counterparty to every trade” actually mean for your position?",
   a="Your token mix changes as traders move the price — you supply whichever token they're buying.")

# ---------------------------------------------------------------- the fee apr formula
sc("title", "The fee APR formula.", chapter="The fee APR formula", eyebrow="The fee APR formula", num="2", title="Four numbers, one estimate",
   sub="Daily volume, fee tier, your share, annualised.")
sc("flow", "Here's the formula, broken into the four numbers that actually build it. Daily trading volume through the pool. Multiplied by the pool's fee tier, the cut every trade pays. Multiplied by your share of the pool, your deposit divided by the pool's total value. And annualised, multiplied by three hundred sixty-five, to turn a daily number into the yearly rate everyone actually compares.",
   chapter="The fee APR formula", title="Fee APR, built from four numbers",
   nodes=[{"label": "Daily volume", "sub": "Trading through the pool", "icon": "swap"}, {"label": "× Fee tier", "sub": "The cut every trade pays", "icon": "coins"},
          {"label": "× Your share", "sub": "Your deposit ÷ pool's total value", "icon": "layers"}, {"label": "× 365", "sub": "Annualised, into a yearly rate", "icon": "chart"}])
sc("statement", "One simplification worth knowing, since it makes the mental math far easier for a full-range position specifically. Your share of a full-range pool is just your deposit divided by the pool's total value locked. Once you substitute that in, the whole formula collapses to one line: daily volume, times fee tier, times three hundred sixty-five, divided by T.V.L. Nothing about your specific deposit size needs to appear at all.",
   chapter="The fee APR formula", kicker="The full-range simplification", lines=["Daily volume × fee tier × 365, divided by TVL.", "Your deposit size drops out entirely."], sub="One line, for a full-range position.")
sc("compare", "And here's exactly why this lesson insists on thirty-day average volume, not today's number, since using the wrong one quietly wrecks the estimate. A single volatile day can spike volume far above normal, making the fee APR look unusually good, right when impermanent loss is also running at its worst. A thirty-day average smooths that out, giving you a number that actually represents a typical day, not the best one.",
   chapter="The fee APR formula",
   left={"label": "Today's volume", "tone": "bad", "items": ["A volatile day can spike it artificially", "Overstates income exactly when IL is worst"]},
   right={"label": "30-day average volume", "tone": "good", "items": ["Smooths out single-day spikes", "Represents a typical day, not the best one"]})
sc("stats", "One more real pair of numbers, at a completely different scale, so the formula feels usable on any pool, not just the worked example ahead. A five-million-dollar T.V.L. pool, one million dollars in thirty-day volume, a zero point zero five percent fee tier: one million times zero point zero zero zero five, times three hundred sixty-five, divided by five million, comes out to three point six five percent fee A.P.R.",
   "One more real pair of numbers, at a completely different scale. A $5M TVL pool, $1M in 30-day volume, a 0.05% fee tier: 1,000,000 × 0.0005 × 365 ÷ 5,000,000 comes out to 3.65% fee APR.",
   chapter="The fee APR formula", stats=[["3.65%", "$5M TVL, $1M/day volume, 0.05% fee tier"]])
sc("compare", "One nuance worth knowing before you assume a higher fee tier is always the better choice. A higher fee tier earns more per trade, but often attracts less volume, since traders and aggregators route toward the cheapest available price. A lower fee tier earns less per trade, but often wins far more volume. The fee A.P.R. formula is what actually tells you which one wins, not the fee tier number alone.",
   chapter="The fee APR formula",
   left={"label": "A higher fee tier", "tone": "warn", "items": ["Earns more, per trade", "Often attracts less volume"]},
   right={"label": "A lower fee tier", "tone": "warn", "items": ["Earns less, per trade", "Often wins far more volume"]})
sc("quiz", "Quick check. Why use a 30-day average volume instead of today's volume, when estimating fee APR? [[pause 4]] The answer: single-day spikes overstate fee income, and they happen on exactly the days you take the most impermanent loss, so the average gives a more honest number.",
   chapter="The fee APR formula", n=2, of=3, q="Why use a 30-day average volume instead of today's volume, when estimating fee APR?",
   a="Single-day spikes overstate income, and happen on the days IL is worst.")

# ---------------------------------------------------------------- worked example
sc("title", "Worked example.", chapter="Worked example", eyebrow="Worked example", num="1", title="$10,000 into a real pool",
   sub="Real numbers, from the source material.")
sc("stats", "Here's the pool this worked example runs on. Ten million dollars in total value locked. Two million dollars in thirty-day average daily volume. And a zero point three percent fee tier. Every number that follows comes directly out of these three starting figures.",
   "Here's the pool this worked example runs on. $10M in total value locked. $2M in 30-day average daily volume. And a 0.3% fee tier. Every number that follows comes directly out of these three starting figures.",
   chapter="Worked example", stats=[["$10M TVL", "$2M 30-day avg. daily volume, 0.3% fee tier"]])
sc("steps", "Now the arithmetic, step by step, exactly as the formula lays it out. Daily pool fees: two million dollars in volume, times zero point three percent, equals six thousand dollars, earned by the entire pool, that day. Your ten-thousand-dollar deposit is zero point one percent of the ten-million-dollar pool. Zero point one percent of six thousand dollars is six dollars a day, for you specifically.",
   chapter="Worked example", title="From pool fees to your daily income",
   steps=["Daily pool fees: $2M × 0.3% = $6,000", "Your share: $10,000 ÷ $10M TVL = 0.1%", "Your daily income: 0.1% × $6,000 = $6/day"], result="Annualised: ~21.9% fee APR, before IL and gas")
sc("compare", "Now see how sensitive that twenty-one point nine percent actually is, to the two things most likely to change after you deposit. If daily volume halves, your fee A.P.R. halves with it, straight line, since volume is a direct multiplier in the formula. And if a lot more T.V.L. joins the same pool, your share shrinks, at the same volume, so your fee income shrinks too, even though nothing about your own deposit changed.",
   chapter="Worked example",
   left={"label": "If volume halves", "tone": "warn", "items": ["Fee APR halves, directly", "Volume is a straight multiplier in the formula"]},
   right={"label": "If more TVL joins the pool", "tone": "warn", "items": ["Your share shrinks, at the same volume", "Fee income shrinks, even though your deposit didn't change"]})
sc("steps", "Here's exactly where to actually go find these three numbers yourself, on any pool you're considering, before you deposit a dollar. Open the pool on its own protocol's app or a pool-analytics site, not a general price chart. Read T.V.L. and the fee tier directly off the pool's own page. And pull thirty days of volume from that same analytics view, not just today's headline number.",
   chapter="Worked example", title="Finding these numbers yourself",
   steps=["Open the pool on its own app or an analytics site", "Read TVL and fee tier off the pool's own page", "Pull 30 days of volume, not just today's number"], result="Same three inputs, on any pool you're considering")
sc("quiz", "Quick check. In this worked example, what happens to your fee APR if the pool's TVL doubles, with volume unchanged? [[pause 4]] The answer: your share of the pool halves, and so does your fee income, at the same volume, since more deposits are now splitting the same trading fees.",
   chapter="Worked example", n=3, of=3, q="In this worked example, what happens to your fee APR if the pool's TVL doubles, with volume unchanged?",
   a="Your share halves, and so does your fee income, at the same volume.")
sc("statement", "One last honest number, before the checklist, since twenty-one point nine percent on its own can sound like the whole story. That figure is before impermanent loss and before gas, both real costs this same worked example is still ignoring. Lesson two point four takes this exact pool and shows what actually survives once both are counted properly.",
   chapter="Worked example", kicker="Before you get excited about 21.9%", lines=["Before impermanent loss.", "Before gas. Both still ahead."], sub="Lesson 2.4 shows what actually survives.")

# ---------------------------------------------------------------- checklist and recap
sc("steps", "Here's your checklist. Do it now, before any deposit. Your fee A.P.R. is calculated from thirty-day volume, not today's. You're genuinely comfortable ending up holding one hundred percent of either token, since that's a real possible outcome. Your entry prices are recorded, so you have an actual “versus holding” benchmark later. And your exit rule is written down now: volume drops, a clear trend starts, or fees simply stop covering impermanent loss.",
   chapter="Checklist", title="Your checklist, before any deposit",
   steps=["Fee APR calculated from 30-day volume, not today's", "Comfortable holding 100% of either token", "Entry prices recorded, for the “vs holding” benchmark", "Exit rule written: volume drops, trend starts, or fees stop covering IL"])
sc("bullets", "Let's recap. Providing liquidity means depositing both tokens and becoming the counterparty to every trade, not a passive lender. Fee A.P.R. is four numbers: daily volume, fee tier, your share, annualised, and for a full-range position it simplifies to one line. Use thirty-day volume, since single-day spikes overstate income exactly when impermanent loss is worst. And your fee A.P.R. is sensitive to both volume and T.V.L. changing after you've already deposited.",
   chapter="Recap", title="Recap", check=False,
   items=["LPing: you become the counterparty to every trade", "Fee APR: volume × fee tier × your share × 365",
          "Use 30-day volume — single-day spikes overstate income", "Sensitive to both volume and TVL, after you've deposited"])
sc("cta", "Calculate the real fee APR from thirty-day volume, before any deposit, not after. Next up, Lesson two point four: Impermanent loss and true LP profit and loss.",
   "Calculate the real fee APR from thirty-day volume, before any deposit, not after. Next up, Lesson 2.4: Impermanent loss and true LP P&L.",
   chapter="Recap", button="Next: Lesson 2.4", sub="Impermanent loss and true LP P&L")

spec = {"id": "lesson-02-3", "title": "Lesson 2.3: Providing liquidity", "size": [1920, 1080], "group": "lessons", "maxMinutes": 25,
        "tag": "Lesson 2.3", "gold": True, "music": True, "musicLevel": 0.14, "seed": 55,
        "use": "Lesson 2.3 page in the Whop course. Hand-written gold-standard script: what LPing actually does, the fee-APR formula and why 30-day volume, and the source material's own $10M TVL / $2M volume / 0.3% fee worked example, as walk-throughs.",
        "thumbnail": {"title": "Providing liquidity", "subtitle": "Lesson 2.3"}, "scenes": S}
out = ROOT / "video-scripts" / "gold" / "lesson-02-3.json"
out.write_text(json.dumps(spec, indent=1, ensure_ascii=False))
words = sum(len(s["vo"].replace("[[pause 4]]", "").split()) for s in S)
print(f"{len(S)} scenes, {words} words, est {(words / 171 * 60 + len(S) * 1.3 + 4 * 3) / 60:.1f} min")
