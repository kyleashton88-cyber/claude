#!/usr/bin/env python3
"""Gold-standard script for Lesson 4.7, Stablecoin savings rates and
yield-bearing stablecoins (target 11-14 minutes, per the "a bit longer"
note for lessons from here on). Walks the four genuinely different
sources of stablecoin yield (lending, protocol savings rates,
treasury-backed, synthetic/basis-backed), the different risk behind each,
and the source material's own worked example ($10,000 at 4.5% earns
~$450/yr if the rate holds; the real questions are where the 4.5% comes
from, what happens to it when funding goes negative, and who can actually
redeem for $1), as visual walk-throughs. Written in one pass at the full
target length (no separate expansion round).

Writes video-scripts/gold/lesson-04-7.json (the generator skips lessons
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
sc("title", "Lesson four point seven. Stablecoin savings rates, and yield-bearing stablecoins. By the end, you'll be able to tell apart four completely different ways a stablecoin can pay yield, and the specific risk behind each one.",
   "Lesson 4.7. Stablecoin savings rates and yield-bearing stablecoins. By the end, you'll be able to tell apart four completely different ways a stablecoin can pay yield, and the specific risk behind each one.",
   chapter="Intro", eyebrow="Lesson 4.7", num="4.7", title="Stablecoin savings rates & yield-bearing stablecoins", sub="Same 4 to 10% on dollars. Four completely different risks underneath.")
sc("pillars", "Here's the plan. The four genuinely different places yield on stablecoins can actually come from. The specific risk that rides along with each one. A full worked example, pricing a real, advertised rate against three real questions you should ask first. And a checklist for identifying, and diversifying across, these sources correctly.",
   chapter="Intro", title="What this lesson covers",
   items=[{"icon": "coins", "title": "Four yield sources", "text": "Lending, savings rates, treasury-backed, synthetic basis"}, {"icon": "alert", "title": "A different risk, each time", "text": "Same headline number, four different things that can go wrong"},
          {"icon": "chart", "title": "Worked example", "text": "$450/yr — if the rate holds. Three questions first"}, {"icon": "target", "title": "Real diversification", "text": "Different sources, not just different tickers"}])

# ---------------------------------------------------------------- four yield sources
sc("title", "Four genuinely different sources.", chapter="Four yield sources", eyebrow="Four yield sources", num="4", title="Same 4-10% on dollars, four different origins",
   sub="Lending · Savings rates · Treasury-backed · Synthetic basis")
img(D + "yield-bearing-stables.png", "Where stablecoin yield actually comes from",
    "Here are all four places yield on a dollar-pegged stablecoin can genuinely originate from. Lending, where you're lending stablecoins directly to borrowers, exactly the lending markets covered back in Module three. Savings rates, a set rate some stablecoin protocols pay directly to holders, funded by the protocol's own revenue. Treasury-backed, where the issuer holds real, short-term government debt, and passes on part of that interest. And synthetic, or basis-backed, where the yield comes from a hedged derivatives position, earning funding.",
    chapter="Four yield sources")
sc("flow", "Here's each of those four, paired directly with its own specific risk, since the risk is genuinely different every single time. Lending's risk is the protocol, the collateral backing it, and the oracles pricing that collateral. Savings rates carry the stablecoin's own design and governance risk, since governance is what actually sets that rate. Treasury-backed carries the issuer, the custodian holding those treasuries, and the redemption terms. And synthetic, basis-backed yield carries funding turning negative, and the exchange itself.",
   chapter="Four yield sources", title="Each source, its own risk",
   nodes=[{"label": "Lending", "sub": "The protocol, its collateral, and its oracles", "icon": "shield"}, {"label": "Savings rates", "sub": "The stablecoin's own design and governance", "icon": "chart"},
          {"label": "Treasury-backed", "sub": "The issuer, the custodian, the redemption terms", "icon": "coins"}, {"label": "Synthetic / basis-backed", "sub": "Negative funding, and the exchange itself", "icon": "alert"}])
sc("statement", "Worth being precise about the actual lesson this comparison proves, since it's easy to see one number and assume one risk. The exact same headline rate, somewhere between four and ten percent, can be sitting on top of four entirely different foundations, each one able to fail in a completely different way, for a completely different reason.",
   chapter="Four yield sources", kicker="The lesson this comparison proves", lines=["The same headline rate can sit on four different foundations.", "Each one fails in a completely different way, for a different reason."], sub="Never assume the risk just because you recognise the number.")
sc("steps", "Here's how to actually identify which of the four sources a specific stablecoin actually uses, rather than guessing from its marketing alone. Read its own documentation specifically for the words it uses to describe where the yield comes from, lending, a savings rate, treasuries, or a hedged position. Check whether it discloses what it's actually holding, or invested in, behind the token. And if none of that is genuinely disclosed anywhere, treat the yield source itself as unknown, and price that uncertainty as its own separate risk.",
   chapter="Four yield sources", title="Identifying the actual source",
   steps=["Read its documentation for how it describes the yield's origin", "Check whether it discloses what backs the token", "Undisclosed source? Price that uncertainty as its own risk"])
sc("compare", "Here's a rough, useful way to group these four, by how much their rate tends to actually move around. Lending and treasury-backed yields tend to move relatively slowly, tracking broader interest-rate conditions over time. Protocol savings rates and synthetic, funding-based yields can move considerably faster, since a governance vote or a sharp shift in market sentiment can change either one in a single day.",
   chapter="Four yield sources",
   left={"label": "Lending & treasury-backed", "tone": "good", "items": ["Tend to move slowly", "Track broader interest-rate conditions"]},
   right={"label": "Savings rates & synthetic/basis", "tone": "warn", "items": ["Can move considerably faster", "A vote or sentiment shift can change it in a day"]})
sc("quiz", "Quick check. Name the four sources of stablecoin yield. [[pause 4]] The answer: lending, protocol savings rates, treasury backing, and synthetic basis, or funding, positions.",
   chapter="Four yield sources", n=1, of=3, q="Name the four sources of stablecoin yield.",
   a="Lending, protocol savings rates, treasury backing, and synthetic basis/funding positions.")

# ---------------------------------------------------------------- a closer look at synthetic yield
sc("title", "A closer look at synthetic yield.", chapter="Synthetic yield", eyebrow="Synthetic yield", num="1", title="Why this one specifically can fall to zero",
   sub="The other three don't share this exact failure mode.")
sc("flow", "Here's exactly how a synthetic, basis-backed yield actually gets generated, since it's the least intuitive of the four. The protocol holds a spot position, long the underlying asset, and simultaneously holds a perpetual future, short, against that same asset. Those two positions largely cancel each other's price risk out. The yield itself comes specifically from funding payments, paid between longs and shorts on the perpetual, a mechanism covered back in Lesson three point five.",
   chapter="Synthetic yield", title="Spot long + perp short = funding income",
   nodes=[{"label": "Spot, long the asset", "sub": "The actual underlying position", "icon": "coins"}, {"label": "Perpetual, short the same asset", "sub": "Cancels most of the price risk", "icon": "shield"},
          {"label": "= Funding payments", "sub": "The actual source of the yield itself", "icon": "chart"}])
sc("statement", "Worth being precise about why this specific yield source can genuinely fall all the way to zero, unlike the other three. Funding isn't fixed; it moves with market sentiment, and can turn negative during a bear market, meaning shorts pay longs instead of the other way around. When that happens, this yield source doesn't just shrink, it can disappear, or even turn into an active cost, entirely independent of what the underlying asset's own price does.",
   chapter="Synthetic yield", kicker="Why this one can fall to zero", lines=["Funding moves with sentiment, and can turn negative in a bear market.", "The yield doesn't just shrink then. It can vanish, or turn into a cost."], sub="A risk none of the other three sources share in quite the same way.")
sc("statement", "Worth being precise about what the word hedged actually means here, since it's easy to hear it and assume the position is risk-free. Hedged specifically means the price risk of the underlying asset is largely cancelled out. It does not mean the exchange holding those positions can't fail, and it does not mean the funding payments themselves are guaranteed to stay positive. Hedged removes one specific risk. It doesn't remove risk itself.",
   chapter="Synthetic yield", kicker="What 'hedged' actually means", lines=["It cancels the underlying asset's price risk specifically.", "It doesn't remove exchange risk, or guarantee funding stays positive."], sub="Hedged removes one specific risk. Not risk itself.")
sc("quiz", "Quick check. Why can a basis-backed stablecoin's yield fall all the way to zero? [[pause 4]] The answer: funding can turn negative during a bear market, meaning shorts pay longs instead, removing the yield entirely.",
   chapter="Synthetic yield", n=2, of=3, q="Why can a basis-backed stablecoin's yield fall to zero?",
   a="Funding can turn negative in bear markets.")

# ---------------------------------------------------------------- worked example
sc("title", "Worked example.", chapter="Worked example", eyebrow="Worked example", num="1", title="$450 a year, if the rate holds",
   sub="The source material's own scenario, and its three real questions.")
sc("stats", "Here's the headline number first. Ten thousand dollars, deposited into a yield-bearing stablecoin paying four and a half percent, earns approximately four hundred fifty dollars a year. That's the easy part of the arithmetic. Everything that actually matters in this lesson comes right after it.",
   chapter="Worked example", title="$10,000 at 4.5% APY",
   stats=[["$10,000", "Deposited"], ["4.5%", "Advertised rate"], ["~$450/yr", "If the rate holds"]])
sc("steps", "Here are the three real questions to answer, before ever buying in, regardless of how attractive that four hundred fifty dollars looks. Where does the four and a half percent actually come from, which of the four sources from earlier in this lesson. What happens to that rate specifically in a bear market, if it's resting on synthetic funding. And can you genuinely redeem for one dollar, and specifically who is allowed to.",
   chapter="Worked example", title="The three real questions",
   steps=["Where does the 4.5% actually come from? (1 of the 4 sources)", "What happens to it in a bear market, if funding-based?", "Can you redeem for $1 — and who is actually allowed to?"], result="Answer all three before the $450 number means anything at all")
sc("compare", "Here's why that third question, about redemption, deserves just as much weight as the yield source itself. Some yield-bearing stablecoins let any holder redeem directly for a dollar, on demand. Others restrict redemption to specific, whitelisted institutional accounts only, leaving ordinary holders dependent entirely on secondary market liquidity to exit at all.",
   chapter="Worked example",
   left={"label": "Open redemption", "tone": "good", "items": ["Any holder can redeem for $1 directly", "Not dependent on market liquidity to exit"]},
   right={"label": "Restricted redemption", "tone": "warn", "items": ["Only whitelisted institutional accounts can", "Ordinary holders depend on market liquidity"]})
sc("stats", "Here's what's actually at stake in dollar terms, if this specific position turned out to be synthetic, basis-backed yield, and funding genuinely went negative for a stretch. The four hundred fifty dollars a year doesn't just shrink; in a genuinely negative funding environment, it can disappear entirely, or even flip into a real cost, on the exact same ten thousand dollars, with the underlying dollar peg itself potentially still holding throughout.",
   chapter="Worked example", title="If funding turns negative (illustrative)",
   stats=[["$450/yr", "The advertised, positive-funding number"], ["$0", "If funding goes flat"], ["Real cost", "If funding turns meaningfully negative"]])
sc("statement", "Here's the one sentence this entire worked example exists to prove, worth holding onto more than the specific four hundred fifty dollar figure. That number is only real for as long as the rate itself holds, and whether it holds depends entirely on the answers to those three questions, not on how attractive four and a half percent happens to sound on its own.",
   chapter="Worked example", kicker="The one sentence to keep", lines=["$450 is only real for as long as the rate holds.", "Whether it holds depends entirely on those three questions."], sub="The number means nothing until you've answered all three.")

# ---------------------------------------------------------------- checklist and recap
sc("compare", "Worth separating even those two steadier sources from each other, since grouping them together earlier was only about how much the rate itself tends to move, not about sharing the same risk. Lending's risk lives entirely on-chain: the protocol's own code, its collateral, and its oracles. Treasury-backed risk lives largely off-chain instead: the issuer's own solvency, the custodian actually holding those treasuries, and the real-world redemption terms behind them.",
   chapter="Checklist",
   left={"label": "Lending", "tone": "good", "items": ["Risk lives on-chain: protocol, collateral, oracles"]},
   right={"label": "Treasury-backed", "tone": "good", "items": ["Risk lives off-chain: issuer, custodian, redemption terms"]})
sc("steps", "Here's your checklist. Do it before holding any yield-bearing stablecoin. Identify its actual yield source: lending, a protocol savings rate, treasury backing, or synthetic basis. Know its redemption path, and specifically who's actually allowed to use it. And split your own holdings across genuinely different yield sources, not just across different-sounding tickers that all rest on the same underlying source.",
   chapter="Checklist", title="Your checklist",
   steps=["Yield source identified (lending, savings rate, treasuries or basis)", "Redemption path and who can redeem known", "Split across different yield sources, not just different tickers"])
sc("compare", "Here's exactly why that last point matters so much, using two yield-bearing stablecoins both backed by the same kind of basis trade, as a concrete example. They might carry different names, different branding, and different tickers entirely. But underneath, they share the exact same yield source, and the exact same failure mode: negative funding, in the exact same kind of bear market, at the exact same time.",
   chapter="Checklist",
   left={"label": "Looks diversified", "tone": "bad", "items": ["Two different tickers, two different names", "Both basis-backed, underneath"]},
   right={"label": "Isn't, really", "tone": "warn", "items": ["Same yield source, same failure mode", "Fails together, in the same bear market"]})
sc("quiz", "Quick check. Two yield-bearing stablecoins, both backed by basis trades. Are they actually diversified from each other? [[pause 4]] The answer: not really. They share the exact same yield source, and the exact same failure mode.",
   chapter="Checklist", n=3, of=3, q="Two yield-bearing stablecoins both backed by basis trades: diversified?",
   a="Not really. They share the same yield source and failure mode.")
sc("bullets", "Let's recap. Stablecoin yield comes from one of four places: lending, a protocol savings rate, treasury backing, or a synthetic basis position. Each source carries its own distinct risk, even at the exact same headline rate. Ask where the rate comes from, what happens to it in a bear market, and who can actually redeem, before the number means anything. And real diversification means different sources, never just different tickers.",
   chapter="Recap", title="Recap", check=False,
   items=["Stablecoin yield: lending, savings rate, treasury-backed, or synthetic basis", "Each source carries its own distinct risk, at the same headline rate",
          "Ask: where's it from, what happens in a bear market, who can redeem?", "Real diversification: different sources, never just different tickers"])
sc("cta", "Identify the actual yield source before buying, know the redemption path, and diversify across sources, not tickers. Next up, Lesson four point eight: tokenized treasuries and real-world assets.",
   "Identify the actual yield source before buying, know the redemption path, and diversify across sources, not tickers. Next up, Lesson 4.8: tokenized treasuries and real-world assets (RWAs).",
   chapter="Recap", button="Next: Lesson 4.8", sub="Tokenized treasuries and real-world assets (RWAs)")

spec = {"id": "lesson-04-7", "title": "Lesson 4.7: Stablecoin savings rates & yield-bearing stablecoins", "size": [1920, 1080], "group": "lessons", "maxMinutes": 25,
        "tag": "Lesson 4.7", "gold": True, "music": True, "musicLevel": 0.14, "seed": 76,
        "use": "Lesson 4.7 page in the Whop course. Hand-written gold-standard script: the four sources of stablecoin yield and their distinct risks, synthetic/basis yield explained, and the source material's own $450/yr-if-the-rate-holds worked example, as walk-throughs.",
        "thumbnail": {"title": "Yield-bearing stablecoins", "subtitle": "Lesson 4.7"}, "scenes": S}
out = ROOT / "video-scripts" / "gold" / "lesson-04-7.json"
out.write_text(json.dumps(spec, indent=1, ensure_ascii=False))
words = sum(len(s["vo"].replace("[[pause 4]]", "").split()) for s in S)
print(f"{len(S)} scenes, {words} words, est {(words / 171 * 60 + len(S) * 1.3 + 4 * 3) / 60:.1f} min")
