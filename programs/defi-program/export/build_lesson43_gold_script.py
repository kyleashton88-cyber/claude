#!/usr/bin/env python3
"""Gold-standard script for Lesson 4.3, Liquid staking (LSTs) (target
11-14 minutes, per the "a bit longer" note for lessons from here on).
Walks what an LST actually represents, the two accrual methods (rebasing
vs a rising exchange rate), how an LST can trade at a discount under
stress, and the source material's own worked example (an exchange-rate
LST goes from 1.000 to 1.030 over a year, +3%; in a panic it trades at a
2% discount to that redemption value — patient holders who can wait for
the queue recover the full 1.03, forced sellers take the discount), as
visual walk-throughs. Written in one pass at the full target length (no
separate expansion round).

Writes video-scripts/gold/lesson-04-3.json (the generator skips lessons
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
sc("title", "Lesson four point three. Liquid staking, and L.S.T.s. By the end, you'll know exactly how these tokens accrue value, and how they can trade at a discount, before you ever use one as collateral.",
   "Lesson 4.3. Liquid staking (LSTs). By the end, you'll know exactly how these tokens accrue value, and how they can trade at a discount, before you ever use one as collateral.",
   chapter="Intro", eyebrow="Lesson 4.3", num="4.3", title="Liquid staking (LSTs)", sub="Never borrow so close to the limit that a discount liquidates you.")
sc("pillars", "Here's the plan. What an L.S.T. actually represents, and the two different ways it can pass staking rewards on to you. How a discount can appear under stress, and exactly who it actually hurts. A full worked example, using the source material's own accrual and discount numbers. And a checklist for using L.S.T.s safely, especially as collateral.",
   chapter="Intro", title="What this lesson covers",
   items=[{"icon": "coins", "title": "What an LST is", "text": "Staked assets plus rewards, tradeable and usable as collateral"}, {"icon": "chart", "title": "Two accrual methods", "text": "Rebasing balances, or a rising exchange rate"},
          {"icon": "alert", "title": "The discount", "text": "Market price falling below redemption value, under stress"}, {"icon": "target", "title": "Worked example", "text": "+3% a year, then a 2% panic discount"}])

# ---------------------------------------------------------------- what an lst is
sc("title", "What an LST actually represents.", chapter="What an LST is", eyebrow="What an LST is", num="1", title="Staked assets, plus rewards, still usable",
   sub="Trade it, or use it as collateral, without unstaking first.")
img(D + "lst-accrual.png", "How an LST actually accrues value",
    "Here's exactly what you're holding when you hold a liquid staking token. It represents your original staked assets, plus every reward that's accrued on them since, bundled into a single token you can still trade, transfer, or use as collateral elsewhere in DeFi, all without ever unstaking your underlying position. That's the entire point of the design: keeping your capital liquid and useful, while it keeps earning staking rewards in the background.",
    chapter="What an LST is")
sc("flow", "Here's the two different ways an L.S.T. can actually pass those accrued rewards on to you, since protocols genuinely differ on this. A rebasing L.S.T. grows your token balance directly, over time, so you hold more tokens tomorrow than you do today, each still worth about the same. An exchange-rate L.S.T. instead keeps your token balance fixed, but each token becomes redeemable for a growing amount of the underlying asset, as rewards accrue underneath it.",
   chapter="What an LST is", title="Two ways rewards get passed on",
   nodes=[{"label": "Rebasing", "sub": "Your token balance itself grows over time", "icon": "chart"}, {"label": "Exchange rate", "sub": "Balance fixed; each token redeems for more", "icon": "coins"},
          {"label": "Same underlying reward", "sub": "Just represented two different ways", "icon": "check"}])
sc("statement", "Worth being precise about why this distinction actually matters in practice, beyond just being a technical detail. A rebasing token can complicate certain integrations, since some contracts don't expect a balance to change on its own without a transfer. An exchange-rate token avoids that specific problem, which is part of why it's become the more common design, but it does mean the token's price, not your balance, is what carries the growing value.",
   chapter="What an LST is", kicker="Why the distinction matters", lines=["Rebasing can complicate contracts expecting a fixed balance.", "Exchange-rate avoids that, but the price carries the growth instead."], sub="Know which kind you're holding before integrating it anywhere.")
sc("title", "That 3% a year, compounded.", chapter="What an LST is", eyebrow="What an LST is", num="2", title="An exchange rate rising, year after year",
   sub="The same rate as the worked example, extended out.")
sc("chart", "Here's that same three percent annual rate, extended out across five years, so you can see what genuine compounding actually does to the redemption value. Starting at one point zero zero zero, year one closes at one point zero three. By year three, one point zero nine three. By year five, one point one five nine, meaning each token then redeems for nearly sixteen percent more of the underlying than it started with, entirely from staking rewards compounding on themselves.",
   chapter="What an LST is", title="Redemption value over time, at 3%/year (compounding)", kind="line",
   xlabels=["Yr 0", "Yr 1", "Yr 2", "Yr 3", "Yr 4", "Yr 5"], ymin=0.95, ymax=1.20,
   yticks=[[1.0, "1.000"], [1.1, "1.100"]],
   series=[{"values": [1.0, 1.03, 1.061, 1.093, 1.126, 1.159], "tone": "good", "label": "Redemption value"}],
   marks=[{"i": 1, "text": "1.030 (the worked example)", "tone": "good"}, {"i": 5, "text": "1.159", "tone": "good", "below": True}])
sc("quiz", "Quick check. What are the two ways an L.S.T. can pass rewards on to you? [[pause 4]] The answer: rebasing, where your token balance itself grows, or a rising exchange rate, where each token redeems for more of the underlying.",
   chapter="What an LST is", n=1, of=3, q="Two ways LSTs pass on rewards?",
   a="Rebasing balances, or a rising exchange rate.")

# ---------------------------------------------------------------- the discount
sc("title", "How a discount actually appears.", chapter="The discount", eyebrow="The discount", num="1", title="Market price, below redemption value",
   sub="A gap that only shows up under real stress.")
sc("flow", "Here's exactly how this gap opens up, since an L.S.T.'s market price and its redemption value aren't actually the same thing, mechanically. Redemption value is what the L.S.T. is genuinely worth, based on its accrued rewards, if you're willing to wait through the protocol's own unstaking queue to claim it. Market price is simply whatever someone else will pay for it, right now, on the open market. In calm conditions, arbitrage keeps these two numbers close together. Under real stress, that arbitrage can break down, and a gap opens.",
   chapter="The discount", title="Why market price and redemption value can split",
   nodes=[{"label": "Redemption value", "sub": "What it's worth, if you wait through the queue", "icon": "shield"}, {"label": "Market price", "sub": "Whatever someone else pays for it, right now", "icon": "chart"},
          {"label": "Calm markets: arbitrage keeps them close", "sub": "Usually a tiny, unremarkable gap", "icon": "check"}, {"label": "Real stress: the gap can open wide", "sub": "Arbitrage can't always keep up", "icon": "alert"}])
sc("statement", "Worth being precise about who actually has the power to close this gap, and who doesn't. Anyone willing, and able, to simply wait through the redemption queue can eventually claim the full redemption value, regardless of whatever the market price does in the meantime. The discount only becomes a real, permanent loss for whoever is forced to sell into the market immediately, unable to wait that queue out.",
   chapter="The discount", kicker="Who can actually close the gap", lines=["Anyone who can wait out the queue gets full redemption value.", "The discount only becomes real for forced sellers."], sub="Patience, where you have it, is worth its full value here.")
sc("compare", "Here's a distinction worth keeping clear, since an L.S.T. discount and a genuine protocol failure can look similar from a chart alone, but mean completely different things. A discount is a temporary market gap, fully backed the entire time, and fully recoverable simply by waiting out the queue. A genuine depeg, from an actual protocol failure, means the backing itself is impaired, and waiting doesn't necessarily fix anything at all.",
   chapter="The discount",
   left={"label": "An LST discount", "tone": "good", "items": ["Fully backed the entire time", "Recoverable by waiting out the queue"]},
   right={"label": "A genuine depeg (protocol failure)", "tone": "bad", "items": ["The backing itself is impaired", "Waiting doesn't necessarily fix it"]})
sc("quiz", "Quick check. What exactly is an L.S.T. discount? [[pause 4]] The answer: its market price falling below what it would actually redeem for, through the protocol's own unstaking queue.",
   chapter="The discount", n=2, of=3, q="What is an LST discount?",
   a="Its market price falling below its redemption value.")

# ---------------------------------------------------------------- worked example
sc("title", "Worked example.", chapter="Worked example", eyebrow="Worked example", num="1", title="A year of accrual, then a panic",
   sub="The source material's own scenario.")
sc("steps", "Here's the accrual side first, over an ordinary year, with no panic involved at all. An exchange-rate L.S.T. starts the year redeemable for one point zero zero zero of the underlying asset, per token. Over that year, staking rewards accrue underneath it. By year's end, it's redeemable for one point zero three zero, a genuine three percent gain, entirely from staking rewards.",
   chapter="Worked example", title="A year of ordinary accrual",
   steps=["Starts the year at 1.000 of the underlying, per token", "Staking rewards accrue underneath it, all year", "Ends the year at 1.030 — a genuine +3% gain"], result="Nothing unusual here. Just staking, working as intended")
sc("compare", "Now here's what happens when a panic hits, right at that same one point zero three zero redemption value, and the market and redemption value split apart. Patient holders, willing to enter the protocol's own redemption queue and simply wait, still recover the full one point zero three zero they're genuinely owed. Forced sellers, who need to exit immediately on the open market, instead sell at a two percent discount to that same redemption value.",
   chapter="Worked example",
   left={"label": "Patient holders (redemption queue)", "tone": "good", "items": ["Wait out the queue", "Recover the full 1.030 they're owed"]},
   right={"label": "Forced sellers (open market)", "tone": "bad", "items": ["Sell immediately, at market price", "Take a 2% discount to redemption value"]})
sc("statement", "Here's the one sentence this entire worked example exists to prove, worth holding onto more than the specific percentages involved. The exact same token, worth the exact same one point zero three zero underneath, delivers two completely different outcomes, purely based on whether its holder could afford to wait. That gap is never about the asset's real value; it's entirely about who was forced to sell, and when.",
   chapter="Worked example", kicker="The one sentence to keep", lines=["Same token. Same real value underneath.", "Two different outcomes, purely based on who could afford to wait."], sub="The gap is about who was forced to sell, never about real value.")
sc("quiz", "Quick check. Who's actually hurt most by an L.S.T. discount? [[pause 4]] The answer: forced sellers, who can't wait out the redemption queue, and leveraged holders who get liquidated directly into that discount.",
   chapter="Worked example", n=3, of=3, q="Who is hurt most by a discount?",
   a="Forced sellers and leveraged holders who get liquidated.")

# ---------------------------------------------------------------- the leverage trap
sc("title", "The leverage trap.", chapter="Worked example", eyebrow="Worked example", num="2", title="Why this hits collateral positions hardest",
   sub="A discount that would otherwise cost you nothing can force a sale.")
sc("flow", "Here's exactly how this discount turns into forced liquidation, specifically for anyone using an L.S.T. as collateral, close to their limit. A protocol's own oracle reads the L.S.T.'s current market price, discount included, not its underlying redemption value. If that discounted price crosses your collateral's own liquidation threshold, you're liquidated immediately, at exactly the wrong moment, even though the asset itself never actually lost any real value at all.",
   chapter="Worked example", title="How a discount becomes a forced sale",
   nodes=[{"label": "Oracle reads market price", "sub": "Discount included, not redemption value", "icon": "eye"}, {"label": "Price crosses your liquidation threshold", "sub": "Purely from the temporary discount", "icon": "alert"},
          {"label": "Liquidated immediately", "sub": "At exactly the wrong moment", "icon": "target"}, {"label": "The asset itself never lost real value", "sub": "You were never actually insolvent", "icon": "shield"}])
sc("compare", "Here's that exact same two percent discount, applied to two different borrowers against the same L.S.T. collateral, to make the rule concrete rather than abstract. A borrower with real room to spare simply absorbs that two percent inside their existing buffer, and nothing happens at all. A borrower already sitting right at their limit gets liquidated by that same two percent, purely because they left themselves no buffer for it in the first place.",
   chapter="Worked example",
   left={"label": "Real room to spare", "tone": "good", "items": ["The 2% discount fits inside the buffer", "Nothing happens"]},
   right={"label": "Already sitting at the limit", "tone": "bad", "items": ["The same 2% triggers liquidation", "Purely for lack of buffer"]})
sc("statement", "Here's the actual rule this entire chain of reasoning leads to, and it's worth remembering on its own, independent of everything else in this lesson. Never borrow so close to your limit that an L.S.T. discount alone, entirely temporary and entirely disconnected from the asset's real value, could be the thing that liquidates you.",
   chapter="Worked example", kicker="The rule this leads to", lines=["Never borrow so close to the limit that a discount liquidates you.", "A temporary discount, disconnected from real value, shouldn't end your position."], sub="This is the single most important sentence in this entire lesson.")

# ---------------------------------------------------------------- checklist and recap
sc("title", "Checking the queue yourself.", chapter="Checklist", eyebrow="Checklist", num="1", title="Before you rely on being able to wait",
   sub="A patient holder still needs to know how long that patience actually takes.")
sc("steps", "Here's how to actually check a redemption queue before you rely on being able to wait it out. Check the protocol's own documentation or dashboard for its current stated unbonding or redemption time. Check whether that time is fixed, or can extend under heavy demand, since a rush of withdrawals can lengthen it. And size your own discount tolerance around that real number, not around an assumption that you can always exit whenever you'd like.",
   chapter="Checklist", title="Checking the redemption queue",
   steps=["Check the protocol's current stated redemption time", "Check whether it's fixed or can extend under heavy demand", "Size your discount tolerance around that real number"])
sc("steps", "Here's your checklist. Do it before using any L.S.T., especially as collateral. Know its accrual method, rebasing or exchange rate, since that changes how it behaves in other contracts. Know its redemption path, and specifically how long that queue actually runs. And set a discount alert for yourself, if you're using it as collateral, so a widening gap never catches you by surprise.",
   chapter="Checklist", title="Your checklist",
   steps=["Accrual method known (rebase vs exchange rate)", "Redemption path and queue length known", "Discount alert set if used as collateral"])
sc("bullets", "Let's recap. An L.S.T. represents staked assets plus accrued rewards, still tradeable and usable as collateral. It accrues value either by rebasing your balance, or through a rising exchange rate. Under real stress, it can trade at a discount to its redemption value, a gap that only becomes a real loss for forced sellers. And the rule that follows from all of it: never borrow so close to the limit that a temporary discount alone can liquidate you.",
   chapter="Recap", title="Recap", check=False,
   items=["An LST: staked assets plus rewards, tradeable and usable as collateral", "Accrues via rebasing balances, or a rising exchange rate",
          "Under stress, it can trade at a discount — a real loss only for forced sellers", "Rule: never borrow so close to the limit that a discount liquidates you"])
sc("cta", "Know your LST's accrual method and redemption queue, and never borrow so close to the limit that a discount alone can liquidate you. Next up, Lesson four point four: restaking and shared security.",
   "Know your LST's accrual method and redemption queue, and never borrow so close to the limit that a discount alone can liquidate you. Next up, Lesson 4.4: restaking and shared security.",
   chapter="Recap", button="Next: Lesson 4.4", sub="Restaking & shared security")

spec = {"id": "lesson-04-3", "title": "Lesson 4.3: Liquid staking (LSTs)", "size": [1920, 1080], "group": "lessons", "maxMinutes": 25,
        "tag": "Lesson 4.3", "gold": True, "music": True, "musicLevel": 0.14, "seed": 72,
        "use": "Lesson 4.3 page in the Whop course. Hand-written gold-standard script: what an LST is, rebasing vs exchange-rate accrual, how a discount appears and who it hurts, and the source material's own +3%/2%-discount worked example, as walk-throughs.",
        "thumbnail": {"title": "Liquid staking (LSTs)", "subtitle": "Lesson 4.3"}, "scenes": S}
out = ROOT / "video-scripts" / "gold" / "lesson-04-3.json"
out.write_text(json.dumps(spec, indent=1, ensure_ascii=False))
words = sum(len(s["vo"].replace("[[pause 4]]", "").split()) for s in S)
print(f"{len(S)} scenes, {words} words, est {(words / 171 * 60 + len(S) * 1.3 + 4 * 3) / 60:.1f} min")
