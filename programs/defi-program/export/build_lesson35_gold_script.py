#!/usr/bin/env python3
"""Gold-standard script for Lesson 3.5, Perpetual futures and margin
on-chain (target 10-20 minutes). Walks what a perp actually is, isolated
vs cross margin, mark vs index price and funding, the liquidation formula,
and the source material's own worked example (long ETH from $3,000 at 5x,
0.5% maintenance margin: liquidation at ~$2,415, -19.5%; a 20x short
liquidated at ~$3,135, +4.5%), as visual walk-throughs. Built to the
walk-through-first standard: almost every idea is a flow, steps or callout
image, not a statement read over a static screen.

Writes video-scripts/gold/lesson-03-5.json (the generator skips lessons
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
sc("title", "Lesson three point five. Perpetual futures and margin on-chain. By the end, you'll understand perp positions well enough to use them for hedging and carry, and to see exactly why high leverage fails.",
   "Lesson 3.5. Perpetual futures and margin on-chain. By the end, you'll understand perp positions well enough to use them for hedging and carry, and to see exactly why high leverage fails.",
   chapter="Intro", eyebrow="Lesson 3.5", num="3.5", title="Perpetual futures and margin on-chain", sub="Leverage doesn't just magnify gains. It shrinks how wrong you're allowed to be.")
sc("pillars", "Here's the plan. What a perpetual future actually is, and the two margin modes you can choose between. Mark price, index price, and funding, the three mechanics that keep a perp tracking spot with no expiry. The liquidation formula, and what it actually does at high leverage. And a full worked example, with real numbers, showing exactly how little room high leverage leaves you.",
   chapter="Intro", title="What this lesson covers",
   items=[{"icon": "chart", "title": "What a perp is", "text": "No expiry, margin posted, leverage chosen"}, {"icon": "shield", "title": "Isolated vs cross margin", "text": "What's actually at risk, per position"},
          {"icon": "eye", "title": "Mark, index, funding", "text": "The three mechanics underneath"}, {"icon": "target", "title": "Worked example", "text": "5× vs 20×, real liquidation prices"}])

# ---------------------------------------------------------------- what a perp is
sc("title", "What a perp actually is.", chapter="What a perp is", eyebrow="What a perp is", num="1", title="Tracking price, with no expiry",
   sub="Margin posted. Leverage chosen.")
img(D + "perp-anatomy.png", "The anatomy of a perp position",
    "Here's a perpetual future, in full. It tracks an asset's price, with no expiry date, unlike a traditional futures contract that settles on a fixed day. You post margin, collateral backing the position, and choose leverage, a multiplier on your exposure relative to that margin. Higher leverage means more exposure, and controls, per dollar posted, but leaves proportionally less room before liquidation.",
    chapter="What a perp is")
sc("compare", "Here's the actual choice you make, before opening any perp position, between the two margin modes. Isolated margin risks only the margin you specifically put into that one position; a bad trade there can't touch the rest of your account. Cross margin instead backs every open position with your entire account balance, meaning one badly wrong trade can genuinely drain everything else you're holding open.",
   chapter="What a perp is",
   left={"label": "Isolated margin", "tone": "good", "items": ["Risks only that position's own margin", "A bad trade can't touch the rest of your account"]},
   right={"label": "Cross margin", "tone": "bad", "items": ["Your whole account backs every position", "One bad trade can drain the rest"]})
sc("quiz", "Quick check. What's the actual difference between isolated and cross margin? [[pause 4]] The answer: isolated margin risks only that specific position's own margin. Cross margin puts your whole account behind every open position at once.",
   chapter="What a perp is", n=1, of=3, q="What's the actual difference between isolated and cross margin?",
   a="Isolated risks only that position's margin; cross puts the whole account behind every position.")

# ---------------------------------------------------------------- mark, index, funding
sc("title", "Mark, index, and funding.", chapter="Mark, index, funding", eyebrow="Mark, index, funding", num="2", title="The three mechanics underneath",
   sub="What actually triggers liquidation, and what keeps price honest.")
sc("flow", "Here's what these three actually do, and why each one matters differently. Index price is the reference, pulled from spot markets elsewhere, what the asset is genuinely worth right now. Mark price is a smoothed version used specifically for liquidation decisions, designed to resist brief, manipulated price spikes. And funding is a periodic payment, usually every hour or every eight hours, between longs and shorts, that keeps the perp's price from drifting too far from index over time.",
   chapter="Mark, index, funding", title="What each one actually does",
   nodes=[{"label": "Index price", "sub": "The genuine spot reference", "icon": "eye"}, {"label": "Mark price", "sub": "Smoothed, used specifically for liquidation", "icon": "shield"},
          {"label": "Funding", "sub": "Paid between longs and shorts, periodically", "icon": "coins"}, {"label": "Keeps the perp honest", "sub": "Tracking spot, with no expiry needed", "icon": "check"}])
sc("statement", "Worth being precise about why liquidation uses mark price specifically, not index price directly, since it's an easy detail to overlook. A brief, thin-liquidity spike on one venue could otherwise trigger liquidations that shouldn't happen at all. Mark price smooths that out. But it also means your liquidation can technically trigger at a slightly different number than the headline spot price you're watching elsewhere.",
   chapter="Mark, index, funding", kicker="Why mark price, not index price", lines=["Resists a brief, thin-liquidity spike.", "But your liquidation trigger may differ slightly from headline spot."], sub="Watch your own mark price, not just a spot chart elsewhere.")
sc("quiz", "Quick check. Which price actually triggers your liquidation, mark or index? [[pause 4]] The answer: mark price, specifically because it's smoothed to resist brief, manipulated spikes that index price alone wouldn't filter out.",
   chapter="Mark, index, funding", n=2, of=3, q="Which price actually triggers your liquidation, mark or index?",
   a="The mark price.")

# ---------------------------------------------------------------- the liquidation formula
sc("title", "The liquidation formula.", chapter="The liquidation formula", eyebrow="The liquidation formula", num="1", title="How far you're allowed to be wrong",
   sub="Roughly: 1 ÷ leverage, minus maintenance margin.")
sc("flow", "Here's the formula, and exactly what it does to your room to be wrong as leverage climbs. Take one, divided by your leverage. Subtract your maintenance margin, the minimum buffer the exchange requires you to keep. The result is roughly how far, in percentage terms, the price can move against you before liquidation. Higher leverage shrinks that first term directly, which shrinks your entire allowed margin for error.",
   chapter="The liquidation formula", title="1 ÷ leverage, minus maintenance margin",
   nodes=[{"label": "1 ÷ leverage", "sub": "Shrinks directly as leverage climbs", "icon": "chart"}, {"label": "− Maintenance margin", "sub": "The exchange's required minimum buffer", "icon": "shield"},
          {"label": "= Room to be wrong", "sub": "Roughly, as a percentage move", "icon": "target"}, {"label": "Higher leverage: less room", "sub": "Directly, not just proportionally", "icon": "alert"}])
sc("statement", "Here's the one sentence this formula actually proves, worth holding onto more than any specific number in this lesson. Leverage doesn't just magnify your gains, the part everyone already expects. It shrinks how wrong you're allowed to be, mechanically, by the exact same multiple, whether you're thinking about that trade-off or not.",
   chapter="The liquidation formula", kicker="The one sentence to keep", lines=["Leverage doesn't just magnify gains.", "It shrinks how wrong you're allowed to be."], sub="By the exact same multiple, whether you're thinking about it or not.")

# ---------------------------------------------------------------- worked example
sc("title", "Worked example.", chapter="Worked example", eyebrow="Worked example", num="1", title="5× long vs 20× short, real numbers",
   sub="Matching this program's own calculator.")
sc("steps", "Here's the five-times long, step by step, starting from an E.T.H. entry of three thousand dollars, at zero point five percent maintenance margin. One divided by five is zero point two. Subtract zero point five percent maintenance margin: zero point one nine five, or nineteen point five percent. At three thousand dollars entry, that's a liquidation price of roughly two thousand four hundred fifteen dollars.",
   chapter="Worked example", title="5× long, from $3,000",
   steps=["1 ÷ 5 = 0.20 (20%)", "0.20 − 0.005 maintenance = 0.195 (19.5%)", "$3,000 × (1 − 0.195) ≈ $2,415"], result="Liquidated at ~$2,415, a 19.5% drop")
sc("compare", "Now the twenty-times short, the exact same entry price, and watch how dramatically less room remains. The five-times long survives roughly a nineteen-point-five-percent drop. The twenty-times short is liquidated by a price rise of only about four point five percent, a move E.T.H. can genuinely make within a single hour.",
   chapter="Worked example",
   left={"label": "5× long", "tone": "good", "items": ["Liquidated at ~$2,415", "A 19.5% drop — real room"]},
   right={"label": "20× short", "tone": "bad", "items": ["Liquidated at ~$3,135", "Just a 4.5% rise — an hour's move"]})
sc("statement", "Worth being precise about what that four point five percent actually represents, in real market terms, not just as an abstract number. E.T.H., and most volatile crypto assets, can genuinely move that much within a single hour, during ordinary volatility, without any unusual news or event at all. Twenty-times leverage isn't a bet on direction alone; it's a bet that nothing routine happens in the meantime.",
   chapter="Worked example", kicker="What 4.5% actually represents", lines=["A move ETH can make in one ordinary hour.", "Not just a bet on direction — a bet nothing routine happens."], sub="No unusual news required. Just an ordinary hour.")
sc("quiz", "Quick check. Roughly how far can a 10x long fall before liquidation, at a 0.5% maintenance margin? [[pause 4]] The answer: about nine point five percent. One divided by ten is ten percent, minus zero point five percent maintenance margin.",
   chapter="Worked example", n=3, of=3, q="Roughly how far can a 10x long fall before liquidation, at a 0.5% maintenance margin?",
   a="About 9.5% (1 ÷ 10 − 0.5%).")
sc("title", "The full curve.", chapter="Worked example", eyebrow="Worked example", num="2", title="Room to be wrong, across leverage",
   sub="Same 0.5% maintenance margin, six different multiples.")
sc("chart", "Here's that same formula, run across six different leverage multiples, all at the same zero point five percent maintenance margin, so you can see the actual shape of the curve, not just two points on it. At two times leverage, you can be wrong by roughly forty-nine and a half percent. At three times, thirty-two point eight percent. By ten times, you're down to nine and a half percent. And by fifty times, just one and a half percent, a move that can happen inside a single candle.",
   chapter="Worked example", title="Room to be wrong vs leverage (0.5% maintenance margin)", kind="line",
   xlabels=["2×", "3×", "5×", "10×", "20×", "50×"], ymin=0, ymax=55,
   yticks=[[0, "0%"], [25, "25%"], [50, "50%"]],
   series=[{"values": [49.5, 32.8, 19.5, 9.5, 4.5, 1.5], "tone": "bad", "label": "Room to be wrong"}],
   marks=[{"i": 0, "text": "49.5%", "tone": "good"}, {"i": 3, "text": "9.5%", "tone": "warn"}, {"i": 5, "text": "1.5%", "tone": "bad", "below": True}])
sc("statement", "Notice how the curve isn't a straight line down; it falls fastest exactly where most people first add leverage, between two times and ten times. Going from two times to five times costs you thirty percentage points of room. Going from twenty times to fifty times only costs another three. The most dangerous leverage decision is usually the early one, not the extreme one.",
   chapter="Worked example", kicker="Where the curve actually bites", lines=["2× to 5× costs 30 points of room.", "20× to 50× costs only 3 more."], sub="The early leverage decision is usually the dangerous one, not the extreme one.")
sc("stats", "Put another way. Doubling your leverage from two times to four times roughly halves your room to be wrong. Doubling it again, from four times to eight times, roughly halves it again. It's not a gentle slope; it's a halving, every time you double down.",
   chapter="Worked example", title="Every doubling of leverage roughly halves your room",
   stats=[["49.5%", "Room to be wrong, 2×"], ["24.5%", "Room to be wrong, 4×"], ["12.0%", "Room to be wrong, 8×"]])

# ---------------------------------------------------------------- checklist and recap
sc("title", "Before you open the position.", chapter="Checklist", eyebrow="Checklist", num="1", title="Check this first, not after",
   sub="One command, before you commit any margin.")
sc("steps", "Here's how you actually check your own liquidation price before opening anything, using this program's own calculator instead of guessing. You run defi_calc.py perp, passing your entry price, your chosen leverage, and your maintenance margin rate. It returns your exact liquidation price and the percentage move it represents. Compare that percentage against how far the asset has actually moved on an ordinary day, not just on a good one, before you decide the leverage is reasonable.",
   chapter="Checklist", title="Computing it yourself",
   steps=["Run: defi_calc.py perp --entry 3000 --leverage 5 --mmr 0.5", "Read the liquidation price and the % move it represents", "Compare that % against an ordinary day's real move", "Only then decide the leverage is reasonable"], result="Know the number before you commit any margin")
sc("compare", "Funding also matters more the longer you hold, so weigh it against your actual timeframe, not just the entry decision. A short hedge held for a few hours pays or receives only a few small funding settlements, a minor cost either way. The same position held open for months compounds every single settlement, and can quietly erode a position that looked fine on day one.",
   chapter="Checklist",
   left={"label": "Short holding period", "tone": "good", "items": ["A few funding settlements only", "A minor cost either way"]},
   right={"label": "Long holding period", "tone": "warn", "items": ["Every settlement compounds", "Can quietly erode a position that looked fine"]})
sc("steps", "Here's your full checklist. Do it now, before opening any perp position. Isolated margin, by default, every time, not cross margin. Liquidation price computed and known, before you open, not after. Leverage kept at two to three times, or less, for anything except a hedge you fully understand. And funding cost checked specifically for however long you actually plan to hold.",
   chapter="Checklist", title="Your checklist",
   steps=["Isolated margin by default", "Liquidation price computed before opening", "Leverage ≤ 2–3×, except for a fully understood hedge", "Funding cost checked for your holding period"])
sc("bullets", "Let's recap. A perp tracks price with no expiry; you post margin and choose leverage. Isolated margin risks only that position; cross margin risks your whole account. Mark price triggers liquidation specifically, smoothed against manipulation; funding keeps the perp tracking spot over time. And the liquidation formula proves the real lesson: leverage shrinks your room to be wrong, by the same multiple it magnifies your gains, whether you're accounting for that or not.",
   chapter="Recap", title="Recap", check=False,
   items=["A perp: no expiry, margin posted, leverage chosen", "Isolated margin: risks one position. Cross: risks the whole account",
          "Mark price triggers liquidation; funding keeps price tracking spot", "Leverage shrinks your room to be wrong, by the same multiple"])
sc("cta", "Default to isolated margin, compute your liquidation price before opening, and keep leverage low unless you fully understand the hedge. Next up, Lesson three point six: a deep dive into lending design, e-mode, caps, auctions, and bad debt.",
   "Default to isolated margin, compute your liquidation price before opening, and keep leverage low unless you fully understand the hedge. Next up, Lesson 3.6: lending design deep dive.",
   chapter="Recap", button="Next: Lesson 3.6", sub="Lending design deep dive: e-mode, caps, auctions, bad debt")

spec = {"id": "lesson-03-5", "title": "Lesson 3.5: Perpetual futures and margin on-chain", "size": [1920, 1080], "group": "lessons", "maxMinutes": 25,
        "tag": "Lesson 3.5", "gold": True, "music": True, "musicLevel": 0.14, "seed": 66,
        "use": "Lesson 3.5 page in the Whop course. Hand-written gold-standard script: what a perp is, isolated vs cross margin, mark/index/funding, the liquidation formula, and the source material's own 5x/20x worked example, as walk-throughs.",
        "thumbnail": {"title": "Perpetual futures & margin", "subtitle": "Lesson 3.5"}, "scenes": S}
out = ROOT / "video-scripts" / "gold" / "lesson-03-5.json"
out.write_text(json.dumps(spec, indent=1, ensure_ascii=False))
words = sum(len(s["vo"].replace("[[pause 4]]", "").split()) for s in S)
print(f"{len(S)} scenes, {words} words, est {(words / 171 * 60 + len(S) * 1.3 + 4 * 3) / 60:.1f} min")
