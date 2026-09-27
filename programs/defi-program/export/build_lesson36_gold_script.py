#!/usr/bin/env python3
"""Gold-standard script for Lesson 3.6, Lending design deep dive: e-mode,
caps, auctions, soft liquidation, bad debt (target 10-20 minutes). Walks
e-mode and isolation mode, supply/borrow caps, the three liquidation
mechanisms, who absorbs bad debt, and the source material's own worked
example (a 90% LTV LST e-mode loop liquidated by a 6% oracle discount even
though ETH itself didn't move), as visual walk-throughs. Built to the
walk-through-first standard: almost every idea is a flow, steps or compare,
not a statement read over a static screen.

Writes video-scripts/gold/lesson-03-6.json (the generator skips lessons
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
sc("title", "Lesson three point six. Lending design deep dive: e-mode, caps, auctions, soft liquidation, and bad debt. By the end, you'll read a lending protocol's risk parameters the way a risk manager does, not just as a borrower.",
   "Lesson 3.6. Lending design deep dive: e-mode, caps, auctions, soft liquidation, and bad debt. By the end, you'll read a lending protocol's risk parameters the way a risk manager does, not just as a borrower.",
   chapter="Intro", eyebrow="Lesson 3.6", num="3.6", title="Lending design deep dive", sub="Read a lending protocol's risk parameters like a risk manager, not just a borrower.")
sc("pillars", "Here's the plan. Efficiency mode, and isolation mode, the two ways protocols let some collateral behave differently from the rest. Supply and borrow caps, the limits that protect against manipulation. The three different ways a protocol can actually liquidate you. And who pays when collateral ends up worth less than the debt it backs, plus a real worked example of e-mode failing.",
   chapter="Intro", title="What this lesson covers",
   items=[{"icon": "shield", "title": "E-mode & isolation mode", "text": "Higher LTVs for correlated assets, contained risk for new ones"},
          {"icon": "chart", "title": "Supply & borrow caps", "text": "Limits against manipulation and illiquid collateral"},
          {"icon": "target", "title": "Three liquidation mechanisms", "text": "Fixed bonus, Dutch auction, soft liquidation"},
          {"icon": "alert", "title": "Bad debt", "text": "Who actually pays when collateral falls short"}])

# ---------------------------------------------------------------- e-mode & isolation mode
sc("title", "Efficiency mode, and isolation mode.", chapter="E-mode & isolation mode", eyebrow="E-mode & isolation mode", num="1", title="Two opposite ways to treat collateral",
   sub="One raises your LTV. The other contains the damage.")
sc("flow", "Here's what efficiency mode, usually called e-mode, actually does. It's a special setting for collateral and debt that are expected to move together, like a staked E.T.H. token against E.T.H. itself, or one stablecoin against another. Because the protocol expects those two prices to stay close, it allows a much higher loan-to-value than it would for unrelated assets. That's genuinely useful for correlated loops. But it's dangerous specifically if that correlation breaks, meaning if the two assets ever trade apart from each other, even briefly.",
   chapter="E-mode & isolation mode", title="What e-mode actually does",
   nodes=[{"label": "Correlated assets", "sub": "An LST vs ETH, or stablecoin vs stablecoin", "icon": "chart"}, {"label": "Higher LTV allowed", "sub": "Because the two prices are expected to track", "icon": "shield"},
          {"label": "Great for correlated loops", "sub": "More capital efficiency, same underlying risk", "icon": "check"}, {"label": "Dangerous if correlation breaks", "sub": "A depeg, even briefly, changes everything", "icon": "alert"}])
sc("compare", "Isolation mode does something almost the opposite. Instead of raising what one asset can do, it contains what a risky one is allowed to do. A newer or less-proven collateral type gets isolated: it can only back a limited amount of borrowing, on its own, separate from the main pool. That way, if that specific asset fails badly, the damage stays contained to its own isolated market, instead of spreading into everything else the protocol holds.",
   chapter="E-mode & isolation mode",
   left={"label": "E-mode", "tone": "warn", "items": ["Raises LTV for correlated assets", "Risk: the correlation itself breaking"]},
   right={"label": "Isolation mode", "tone": "good", "items": ["Caps what new/risky collateral can borrow", "Contains a failure to its own market"]})
sc("quiz", "Quick check. What's e-mode actually for? [[pause 4]] The answer: allowing higher loan-to-value ratios specifically for correlated assets, like a staked E.T.H. token against E.T.H. itself.",
   chapter="E-mode & isolation mode", n=1, of=3, q="What's e-mode actually for?",
   a="Higher LTVs on correlated assets.")
sc("steps", "Here's how to actually check whether e-mode fits a position, before you rely on it. Confirm the two assets are genuinely expected to track, not just similarly named. Check what oracle prices each one, since that decides whether a brief panic reaches you. Ask what happens to your position specifically if that correlation gaps, even briefly. And only then decide whether the higher loan-to-value is worth that specific risk.",
   chapter="E-mode & isolation mode", title="Before you rely on an e-mode market",
   steps=["Confirm the two assets are genuinely expected to track", "Check what oracle prices each one", "Ask what happens if the correlation gaps, even briefly", "Only then decide if the higher LTV is worth it"])

sc("statement", "Worth being precise about what isolation mode actually contains, since it's a boundary around the asset, not a guarantee about it. An isolated market can still fail on its own terms, drop in value, get liquidated, even run into bad debt. What isolation mode prevents is that failure from being able to touch collateral in completely unrelated markets on the same protocol.",
   chapter="E-mode & isolation mode", kicker="What isolation actually contains", lines=["It's a boundary around the asset, not a guarantee about it.", "It stops a failure from touching unrelated markets."], sub="The asset can still fail. The failure just can't spread.")

# ---------------------------------------------------------------- caps
sc("title", "Supply and borrow caps.", chapter="Supply & borrow caps", eyebrow="Supply & borrow caps", num="1", title="Limits, not permissions",
   sub="Protecting against manipulation and illiquid collateral.")
sc("flow", "Here's what caps actually protect against, and why they exist even on well-established assets. A supply cap limits how much of a given asset can be deposited into the protocol as collateral, total. A borrow cap limits how much of an asset can be borrowed out, total. Both exist specifically to protect against price manipulation on thin markets, and against a situation where the protocol holds more of an illiquid asset than could actually be sold if it needed to be liquidated.",
   chapter="Supply & borrow caps", title="Why caps exist",
   nodes=[{"label": "Supply cap", "sub": "Limits total deposits of one asset", "icon": "chart"}, {"label": "Borrow cap", "sub": "Limits total borrowing of one asset", "icon": "shield"},
          {"label": "Protects against manipulation", "sub": "Especially on thin, low-liquidity markets", "icon": "eye"}, {"label": "Protects against illiquid collateral", "sub": "Can it actually be sold if liquidated?", "icon": "alert"}])
sc("statement", "Worth being precise about who actually sets these numbers, since it isn't automatic or purely algorithmic. Risk curators, or risk managers, set the specific loan-to-value ratios, liquidation thresholds, and caps for each market, based on that asset's own liquidity and volatility. Protocol governance then reviews and approves those parameters. Both roles matter: read the parameters, not just the protocol's name or reputation.",
   chapter="Supply & borrow caps", kicker="Who actually sets these numbers", lines=["Risk curators set LTVs, thresholds, and caps per market.", "Governance reviews and approves them."], sub="Read the parameters, not just the protocol's name.")

# ---------------------------------------------------------------- liquidation mechanisms
sc("title", "Three ways to get liquidated.", chapter="Three liquidation mechanisms", eyebrow="Three liquidation mechanisms", num="1", title="Fixed bonus, Dutch auction, or soft liquidation",
   sub="They differ in how much they cost you, and when they can fail.")
sc("compare", "Here's the first two, side by side, since they represent genuinely opposite trade-offs. A fixed bonus liquidation pays the liquidator a set extra amount, commonly around five percent of the collateral seized, as their incentive to act fast. It's simple and reliably fast, but that bonus is a fixed cost to you regardless of market conditions. A Dutch auction instead lets the price fall gradually until somebody actually buys, which can produce a better price in a calm market, but depends entirely on liquidator bots, called keepers, actually showing up to bid.",
   chapter="Three liquidation mechanisms",
   left={"label": "Fixed bonus", "tone": "warn", "items": ["A set bonus, often ~5%, to the liquidator", "Simple and fast; the bonus is a fixed cost"]},
   right={"label": "Dutch auction", "tone": "warn", "items": ["Price falls until someone buys", "Better price in calm markets; needs keepers to show up"]})
img(D + "liquidation-cascade.png", "The liquidation cascade",
    "And here's the third mechanism, soft liquidation, which works differently from both of the others. Instead of seizing your collateral all at once with a single penalty, it converts your collateral gradually, across a series of price bands as the price keeps falling. And critically, that conversion can actually reverse: if the price recovers before you're fully liquidated, some of that collateral converts back. Your losses come from the individual conversions along the way, not from one single, fixed penalty.",
    chapter="Three liquidation mechanisms")
sc("quiz", "Quick check. How does soft liquidation actually differ from a fixed-bonus liquidation? [[pause 4]] The answer: collateral is converted gradually across price bands, and can convert back if price recovers, instead of being seized all at once with a fixed penalty.",
   chapter="Three liquidation mechanisms", n=2, of=3, q="How does soft liquidation differ from a fixed-bonus liquidation?",
   a="Collateral converts gradually across price bands, and can convert back, instead of one seizure with a penalty.")

# ---------------------------------------------------------------- bad debt
sc("title", "Bad debt: who actually pays.", chapter="Bad debt", eyebrow="Bad debt", num="1", title="When collateral falls short of the debt it backs",
   sub="Somebody absorbs the gap. It's worth knowing who.")
sc("flow", "Here's what happens when liquidation genuinely can't keep up, and collateral ends up worth less than the debt it was backing. That shortfall is called bad debt, and it doesn't just vanish; somebody has to absorb it. Some protocols hold a reserve or an insurance fund specifically for this. Others have a staking safety module, where staked tokens can be slashed to cover the gap. And some protocols instead socialise the loss, spreading it pro rata across all of their lenders.",
   chapter="Bad debt", title="Where bad debt actually goes",
   nodes=[{"label": "Collateral < debt", "sub": "Liquidation didn't fully cover the loan", "icon": "alert"}, {"label": "A reserve or insurance fund", "sub": "Set aside specifically for this", "icon": "shield"},
          {"label": "A staking safety module", "sub": "Staked tokens can be slashed to cover it", "icon": "coins"}, {"label": "Or lenders, pro rata", "sub": "The loss is socialised across everyone lending", "icon": "chart"}])
sc("statement", "Worth being precise about why this question matters before you lend anywhere, not just after something goes wrong. Knowing who absorbs bad debt in a given protocol tells you what you're actually exposed to as a lender, even if you've never personally borrowed a dollar from it. A protocol with no reserve and no safety module is quietly asking its lenders to be that backstop.",
   chapter="Bad debt", kicker="Why this matters before you lend", lines=["It tells you what you're exposed to as a lender.", "No reserve, no safety module means lenders are the backstop."], sub="Check this before you lend, not after something breaks.")

# ---------------------------------------------------------------- worked example
sc("title", "Worked example.", chapter="Worked example", eyebrow="Worked example", num="1", title="An e-mode loop, liquidated without ETH moving",
   sub="The source material's own scenario.")
sc("steps", "Here's the scenario, step by step. An L.S.T., a liquid staking token, is looped against E.T.H. in e-mode, at ninety percent loan-to-value. It looks safe, because the L.S.T. and E.T.H. are expected to move together, almost in lockstep. Then, during a market panic, the L.S.T. trades at a six percent discount specifically on the oracle the protocol actually uses to price it. That discount alone is enough to push the position past its liquidation threshold.",
   chapter="Worked example", title="The setup",
   steps=["LST looped against ETH in e-mode, 90% LTV", "Looks safe: LST and ETH expected to move together", "A market panic hits; the LST trades at a 6% oracle discount", "That discount alone crosses the liquidation threshold"], result="Liquidated, even though ETH itself never moved")
sc("statement", "Here's the actual lesson this scenario proves, and it's worth sitting with. The position gets liquidated even though E.T.H.'s own price didn't move at all; only the LST's price, relative to E.T.H., on that specific oracle, moved. The correlation e-mode depends on isn't a law of physics. It's a market relationship that can gap, even briefly, and the oracle is what actually decides whether that gap reaches you.",
   chapter="Worked example", kicker="The lesson this scenario proves", lines=["Liquidated even though ETH itself never moved.", "The correlation e-mode depends on can gap, even briefly."], sub="The oracle decides whether that gap actually reaches you.")
sc("compare", "So the one thing worth checking before trusting any e-mode position is exactly which oracle prices your L.S.T., since the two options behave very differently under stress. A market-price oracle reflects whatever the L.S.T. is actually trading at on the open market right now, discount included. An exchange-rate oracle instead reflects the token's underlying redemption value, which doesn't move just because trading briefly panics.",
   chapter="Worked example",
   left={"label": "Market-price oracle", "tone": "bad", "items": ["Reflects live trading price, discount included", "Can trigger liquidation on a brief panic alone"]},
   right={"label": "Exchange-rate oracle", "tone": "good", "items": ["Reflects underlying redemption value", "Doesn't move just because trading panics"]})
sc("quiz", "Quick check. Who can end up paying for bad debt? [[pause 4]] The answer: a protocol's reserve or insurance fund, a staking safety module, or the protocol's own lenders, on a pro rata, socialised basis.",
   chapter="Worked example", n=3, of=3, q="Who can end up paying for bad debt?",
   a="Protocol reserves, a safety module, or lenders pro rata.")

# ---------------------------------------------------------------- checklist and recap
sc("steps", "Here's your checklist. Do it for every market you use, not just once. For each market: know its loan-to-value, its liquidation threshold, its liquidation mechanism and bonus, its caps, and specifically which oracle prices it. Know who actually absorbs bad debt in each protocol you lend to. And give every e-mode position of yours its own depeg scenario in your own stress test.",
   chapter="Checklist", title="Your checklist",
   steps=["For each market: LTV, liquidation threshold, bonus/mechanism, caps, oracle", "Know who absorbs bad debt in each protocol you lend to", "Give every e-mode position a depeg scenario in your stress test"])
sc("bullets", "Let's recap. E-mode raises LTV for correlated assets, but is exposed if that correlation breaks. Isolation mode contains a risky asset's failure to its own market. Caps protect against manipulation and illiquid collateral. Liquidation mechanisms differ: fixed bonus, Dutch auction, or soft liquidation with reversible bands. And bad debt has to go somewhere, a reserve, a safety module, or lenders themselves, so know which, before you lend.",
   chapter="Recap", title="Recap", check=False,
   items=["E-mode: higher LTV for correlated assets, exposed if correlation breaks", "Isolation mode: contains a risky asset's failure to its own market",
          "Caps guard against manipulation and illiquid collateral", "Liquidation: fixed bonus, Dutch auction, or reversible soft liquidation",
          "Bad debt goes somewhere: reserve, safety module, or lenders — know which"])
sc("cta", "Check the parameters, not just the protocol's name: LTV, threshold, mechanism, caps, oracle, and who absorbs bad debt. Next up, Lesson three point seven: C.D.P. stablecoins, minting your own dollars.",
   "Check the parameters, not just the protocol's name: LTV, threshold, mechanism, caps, oracle, and who absorbs bad debt. Next up, Lesson 3.7: CDP stablecoins, minting your own dollars.",
   chapter="Recap", button="Next: Lesson 3.7", sub="CDP stablecoins: minting your own dollars")

spec = {"id": "lesson-03-6", "title": "Lesson 3.6: Lending design deep dive", "size": [1920, 1080], "group": "lessons", "maxMinutes": 25,
        "tag": "Lesson 3.6", "gold": True, "music": True, "musicLevel": 0.14, "seed": 67,
        "use": "Lesson 3.6 page in the Whop course. Hand-written gold-standard script: e-mode, isolation mode, supply/borrow caps, the three liquidation mechanisms, bad debt, and the source material's own e-mode-LST-depeg worked example, as walk-throughs.",
        "thumbnail": {"title": "Lending design deep dive", "subtitle": "Lesson 3.6"}, "scenes": S}
out = ROOT / "video-scripts" / "gold" / "lesson-03-6.json"
out.write_text(json.dumps(spec, indent=1, ensure_ascii=False))
words = sum(len(s["vo"].replace("[[pause 4]]", "").split()) for s in S)
print(f"{len(S)} scenes, {words} words, est {(words / 171 * 60 + len(S) * 1.3 + 4 * 3) / 60:.1f} min")
