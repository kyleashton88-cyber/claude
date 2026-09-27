#!/usr/bin/env python3
"""Gold-standard script for Lesson 3.7, CDP stablecoins: minting your own
dollars (target 10-20 minutes). Walks what a CDP actually is, the minimum
collateral ratio, how the peg holds (over-collateralisation, liquidations,
rates, PSM), how a CDP differs from borrowing from a lending pool, and the
source material's own worked example (10 ETH at $3,000, 150% minimum ratio,
minting $10,000 of $20,000 max: 300% ratio, liquidation at $1,500/-50%,
$600/yr stability fee), as visual walk-throughs. Built to the
walk-through-first standard: almost every idea is a flow, steps or compare,
not a statement read over a static screen. Written in one pass at the full
target length (no separate expansion round).

Writes video-scripts/gold/lesson-03-7.json (the generator skips lessons
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
sc("title", "Lesson three point seven. C.D.P. stablecoins: minting your own dollars. By the end, you'll be able to mint a stablecoin against your own collateral, the way your own bank would, and manage that position safely.",
   "Lesson 3.7. CDP stablecoins: minting your own dollars. By the end, you'll be able to mint a stablecoin against your own collateral, the way your own bank would, and manage that position safely.",
   chapter="Intro", eyebrow="Lesson 3.7", num="3.7", title="CDP stablecoins: minting your own dollars", sub="Treat the maximum mint as a cliff, not a target.")
sc("pillars", "Here's the plan. What a C.D.P. actually is, and what you owe back on it. The minimum collateral ratio, the line that decides liquidation. How the stablecoin's peg actually holds, through four different mechanisms working together. How this differs from simply borrowing from a lending pool. And a full worked example with real numbers, minting half of the available maximum.",
   chapter="Intro", title="What this lesson covers",
   items=[{"icon": "shield", "title": "What a CDP is", "text": "Lock collateral, mint a stablecoin, owe it back plus a fee"},
          {"icon": "chart", "title": "Minimum collateral ratio", "text": "The line that decides liquidation"},
          {"icon": "eye", "title": "How the peg holds", "text": "Over-collateralisation, liquidations, rates, and a PSM"},
          {"icon": "target", "title": "Worked example", "text": "10 ETH, $10,000 minted, 300% ratio"}])

# ---------------------------------------------------------------- what a cdp is
sc("title", "What a CDP actually is.", chapter="What a CDP is", eyebrow="What a CDP is", num="1", title="Minting, not borrowing someone else's deposit",
   sub="You create the stablecoin. You owe it back, plus a fee.")
img(D + "cdp-mint.png", "Minting your own dollars",
    "Here's a C.D.P., a collateralised debt position, in full. You lock collateral, an asset like E.T.H., into the position. Against that locked collateral, you mint a stablecoin, meaning the protocol creates new units of it, specifically for you, backed by what you locked. You owe that stablecoin back eventually, plus a stability fee, which is really just interest, charged on the amount you minted.",
    chapter="What a CDP is")
sc("flow", "Here's the full lifecycle, from opening the position to closing it. You lock collateral into the C.D.P. You mint stablecoins against it, up to some maximum the protocol allows. You use those stablecoins for whatever you actually need them for, while your collateral keeps earning nothing, or in some designs, still earning its own separate yield. And eventually, you repay the minted amount plus the accrued stability fee, to unlock your original collateral back.",
   chapter="What a CDP is", title="The full lifecycle",
   nodes=[{"label": "Lock collateral", "sub": "An asset like ETH, into the position", "icon": "shield"}, {"label": "Mint stablecoins", "sub": "New units, created against that collateral", "icon": "coins"},
          {"label": "Use the stablecoins", "sub": "For whatever you actually need", "icon": "chart"}, {"label": "Repay + fee, unlock", "sub": "Minted amount plus accrued stability fee", "icon": "check"}])
sc("quiz", "Quick check. What do you actually owe on a C.D.P.? [[pause 4]] The answer: the stablecoin you minted, plus the accrued stability fee, the interest charged on that minted amount.",
   chapter="What a CDP is", n=1, of=4, q="What do you owe on a CDP?",
   a="The minted stablecoin plus the accrued stability fee.")
sc("steps", "Here's what a C.D.P. is actually used for in practice, beyond just the mechanism itself. Getting liquidity without selling the underlying asset at all, keeping your original position fully intact. Funding a liquidity ladder, minting in stages as you need cash rather than all at once. Or building a yield-covered credit line, where yield from elsewhere covers the ongoing stability fee.",
   chapter="What a CDP is", title="What a CDP is actually used for",
   steps=["Liquidity without selling the underlying asset", "Funding a liquidity ladder, minted in stages", "A yield-covered credit line, funded by yield elsewhere"])

# ---------------------------------------------------------------- minimum collateral ratio
sc("title", "The minimum collateral ratio.", chapter="Minimum collateral ratio", eyebrow="Minimum collateral ratio", num="1", title="The line that decides liquidation",
   sub="Below it, the position is liquidated. No exceptions.")
sc("flow", "Here's what this ratio actually measures, and why it's the single number that matters most on any C.D.P. It's your collateral's current value, divided by how much stablecoin you've minted against it, expressed as a percentage. A common minimum might be one hundred fifty percent. As long as your ratio stays above that minimum, the position is safe. The moment it falls below, through a collateral price drop, the position gets liquidated, automatically, to protect the stablecoin's own backing.",
   chapter="Minimum collateral ratio", title="Collateral value ÷ minted debt",
   nodes=[{"label": "Collateral value", "sub": "Current market value of what's locked", "icon": "chart"}, {"label": "÷ Minted debt", "sub": "How much stablecoin you've minted", "icon": "coins"},
          {"label": "= Collateral ratio", "sub": "e.g. a 150% minimum, commonly", "icon": "shield"}, {"label": "Below minimum: liquidated", "sub": "Automatically, to protect the peg's backing", "icon": "alert"}])
sc("statement", "Worth being precise about the actual relationship this creates, between how much you mint and how much room you leave yourself. Minting the maximum the protocol allows puts you exactly at the minimum ratio, meaning any collateral price drop at all triggers liquidation immediately. Minting less than the maximum is what actually buys you room to survive a real price move.",
   chapter="Minimum collateral ratio", kicker="What minting the maximum actually means", lines=["It puts you exactly at the minimum ratio.", "Any price drop at all then triggers liquidation."], sub="Minting less than the max is what buys you room to survive a real move.")
sc("title", "How much you mint decides your cushion.", chapter="Minimum collateral ratio", eyebrow="Minimum collateral ratio", num="2", title="The same ten ETH, five different mint amounts",
   sub="The relationship isn't obvious until you actually see the curve.")
sc("chart", "Here's that exact relationship, plotted across five different mint amounts, all against the same ten E.T.H. of collateral at three thousand dollars. Minting five thousand dollars gives you a liquidation price of just seven hundred fifty dollars, a full seventy-five percent drop away. Minting ten thousand, the amount from our worked example, gives fifteen hundred dollars, fifty percent away. Minting eighteen thousand pushes it up to twenty-seven hundred dollars, only ten percent away. And minting the full twenty thousand dollar maximum pushes your liquidation price up to exactly three thousand dollars, the current price itself, with zero room left at all.",
   chapter="Minimum collateral ratio", title="Liquidation price vs. mint amount (10 ETH, $3,000 collateral)", kind="line",
   xlabels=["$5k", "$10k", "$15k", "$18k", "$20k"], ymin=0, ymax=3200,
   yticks=[[0, "$0"], [1500, "$1,500"], [3000, "$3,000"]],
   series=[{"values": [750, 1500, 2250, 2700, 3000], "tone": "bad", "label": "Liquidation price"}],
   marks=[{"i": 0, "text": "$750 (−75%)", "tone": "good"}, {"i": 1, "text": "$1,500 (−50%)", "tone": "warn"}, {"i": 4, "text": "$3,000 (0%)", "tone": "bad", "below": True}])
sc("statement", "Notice what happens right at the far end of that curve, at the full twenty thousand dollar maximum. The liquidation price doesn't just get close to the current price; it becomes the current price. There's no buffer left at all, no room for even the smallest, most ordinary market wobble. That's the cliff edge from a moment ago, expressed as an actual number instead of a description.",
   chapter="Minimum collateral ratio", kicker="What the far end of the curve actually shows", lines=["At the maximum, liquidation price equals the current price.", "Zero buffer left, for even the smallest ordinary wobble."], sub="The cliff edge, expressed as a number instead of a description.")
sc("quiz", "Quick check. On that same ten E.T.H. of collateral, roughly what's your liquidation price if you mint eighteen thousand dollars instead of ten thousand? [[pause 4]] The answer: about twenty-seven hundred dollars, only a ten percent drop away, since minting closer to the maximum leaves far less room.",
   chapter="Minimum collateral ratio", n=2, of=4, q="On 10 ETH collateral, roughly what's the liquidation price if you mint $18,000 instead of $10,000?",
   a="About $2,700, only a 10% drop away.")

# ---------------------------------------------------------------- how the peg holds
sc("title", "How the peg actually holds.", chapter="How the peg holds", eyebrow="How the peg holds", num="1", title="Four mechanisms, working together",
   sub="No single one of these does it alone.")
sc("flow", "Here's all four mechanisms that actually keep this stablecoin near one dollar, since no single one of them does it alone. Over-collateralisation means there's always more locked value backing the stablecoin than stablecoin in existence. Liquidations remove undercollateralised positions before they become a genuine shortfall. Interest rates, the stability fee, can be adjusted to change how attractive minting versus holding actually is. And a peg stability module lets holders swap the stablecoin one-to-one, minus a small fee, directly for other stablecoins.",
   chapter="How the peg holds", title="What keeps it near $1",
   nodes=[{"label": "Over-collateralisation", "sub": "More locked value than stablecoin in existence", "icon": "shield"}, {"label": "Liquidations", "sub": "Remove undercollateralised positions early", "icon": "alert"},
          {"label": "Stability fee (rates)", "sub": "Adjusted to shift minting vs holding demand", "icon": "chart"}, {"label": "Peg stability module", "sub": "1:1 swap with other stablecoins, minus a small fee", "icon": "coins"}])
sc("compare", "Here's the actual difference between a C.D.P. and simply borrowing from a lending pool, since they can look similar but work quite differently underneath. Borrowing from a pool means you're borrowing someone else's actual deposit, and the rate you pay is set by that pool's utilisation, how much of the pool is already lent out. A C.D.P. instead creates new money directly, and the rate you pay is set by protocol governance, not by any deposit or utilisation at all.",
   chapter="How the peg holds",
   left={"label": "Lending pool borrow", "tone": "good", "items": ["Borrows someone else's actual deposit", "Rate set by utilisation"]},
   right={"label": "CDP mint", "tone": "warn", "items": ["Creates new money directly", "Rate set by governance, not utilisation"]})
sc("statement", "Worth being precise about why that governance-set rate actually matters to you directly, not just as a design detail. Because it isn't tied to utilisation, it can move for reasons that have nothing to do with how much you're personally borrowing, purely as a peg-management decision. Always compare it against what a lending pool would currently charge for the same amount, before assuming the CDP is the cheaper choice.",
   chapter="How the peg holds", kicker="Why the governance-set rate matters", lines=["It can move for peg-management reasons, not your own usage.", "Always compare it against current lending-pool rates."], sub="Don't assume the CDP is cheaper. Check.")
sc("quiz", "Quick check. What does a peg stability module actually do? [[pause 4]] The answer: it swaps the stablecoin one-to-one, minus a small fee, with other stablecoins, directly supporting the peg.",
   chapter="How the peg holds", n=3, of=4, q="What does a PSM do?",
   a="Swaps the stablecoin 1:1 (minus a fee) with other stablecoins, supporting the peg.")

# ---------------------------------------------------------------- worked example
sc("title", "Worked example.", chapter="Worked example", eyebrow="Worked example", num="1", title="10 ETH, minting half the maximum",
   sub="Matching this program's own calculator.")
sc("steps", "Here's the setup, step by step. Ten E.T.H. at three thousand dollars each is thirty thousand dollars of collateral, total. At a one hundred fifty percent minimum ratio, the absolute maximum you could mint is thirty thousand divided by one point five: twenty thousand dollars. Instead of minting that maximum, mint just ten thousand dollars, half of what's available.",
   chapter="Worked example", title="The setup",
   steps=["10 ETH × $3,000 = $30,000 collateral", "Max mint at 150% minimum: $30,000 ÷ 1.5 = $20,000", "Mint $10,000 instead, half of the maximum"], result="A deliberately conservative starting ratio")
sc("compare", "Here's what that more conservative choice actually buys you, in real numbers, compared to minting the maximum. Minting the full twenty thousand puts you exactly at the one hundred fifty percent minimum, liquidated by any price drop at all. Minting ten thousand instead gives you a three hundred percent ratio, and pushes your actual liquidation price all the way down to fifteen hundred dollars, a fifty percent collateral price drop away.",
   chapter="Worked example",
   left={"label": "Mint the max: $20,000", "tone": "bad", "items": ["Ratio: exactly 150% — the minimum", "Liquidated by any price drop at all"]},
   right={"label": "Mint $10,000 instead", "tone": "good", "items": ["Ratio: 300%", "Liquidation at ~$1,500, a 50% drop away"]})
sc("stats", "And here's the ongoing cost of holding that more conservative position open, using this program's own calculator with a six percent annual stability fee. Ten thousand dollars minted, at six percent, comes to six hundred dollars a year in stability fee, the price of that extra safety margin.",
   chapter="Worked example", title="defi_calc.py cdp --qty 10 --price 3000 --mint 10000 --fee 6",
   stats=[["300%", "Collateral ratio"], ["$1,500", "Liquidation price (−50%)"], ["$600/yr", "Stability fee at 6%"]])
sc("statement", "Worth being precise about the actual lesson this comparison proves, since it's easy to treat the maximum mint as a target rather than a warning label. The protocol's maximum isn't a recommendation; it's simply the point at which any further minting would put you at immediate risk. Operators treat that maximum as a cliff edge to stay well back from, not a number to aim for.",
   chapter="Worked example", kicker="The lesson this comparison proves", lines=["The maximum isn't a recommendation. It's a cliff edge.", "Treat it as a line to stay back from, not a target."], sub="Operators mint well below the maximum, on purpose.")
sc("quiz", "Quick check. With forty thousand dollars of collateral, at a one hundred fifty percent minimum ratio, what's the maximum you could mint? [[pause 4]] The answer: about twenty-six thousand six hundred sixty-seven dollars, forty thousand divided by one point five.",
   chapter="Worked example", n=4, of=4, q="Collateral $40,000, 150% minimum ratio. Maximum mint?",
   a="About $26,667 ($40,000 ÷ 1.5).")

# ---------------------------------------------------------------- closing the position
sc("title", "Closing the position.", chapter="Closing the position", eyebrow="Closing the position", num="1", title="Repay the debt, unlock the collateral",
   sub="What you owe by then depends on how long you held it open.")
sc("steps", "Here's how you actually close a C.D.P., step by step, once you're ready to unwind it. Repay the stablecoin you originally minted. Repay the stability fee that's accrued since you opened it, which grows the longer the position stays open. Once both are repaid in full, your original collateral unlocks, and is returned to you directly.",
   chapter="Closing the position", title="Unwinding the position",
   steps=["Repay the stablecoin you minted", "Repay the stability fee accrued since opening", "Once both are repaid, collateral unlocks and returns to you"], result="Fully closed: no debt, no fee, collateral back")
sc("compare", "Here's why the moment you choose to close actually matters, not just the act of closing itself. If your collateral's price has risen since you opened the position, your ratio has already improved on its own, purely from that price move, before you've repaid anything. If it's fallen instead, your ratio has already worsened, and closing sooner, before the fee accrues further, becomes the safer choice.",
   chapter="Closing the position",
   left={"label": "Collateral price rose since opening", "tone": "good", "items": ["Your ratio improved on its own", "More room; less urgency to close"]},
   right={"label": "Collateral price fell since opening", "tone": "warn", "items": ["Your ratio worsened on its own", "Closing sooner limits further fee and risk"]})

# ---------------------------------------------------------------- checklist and recap
sc("steps", "Here's your checklist. Write it down before you mint anything. Set a collateral ratio target well above the minimum, something like two hundred fifty percent or higher, along with specific action levels below it. Compare the stability fee against what a lending pool would actually charge you to borrow the same amount. And understand the peg mechanism, the PSM and rate adjustments, plus your own exit plan if the stablecoin ever depegs.",
   chapter="Checklist", title="Your checklist",
   steps=["Collateral ratio target (e.g. ≥250%) and action levels written", "Stability fee compared against lending-pool borrow rates", "Peg mechanism understood, plus your exit plan if it depegs"])
sc("bullets", "Let's recap. A C.D.P. lets you mint a stablecoin against locked collateral; you owe it back plus a stability fee. The minimum collateral ratio is the line: below it, you're liquidated, automatically. The peg holds through four mechanisms together: over-collateralisation, liquidations, rates, and a PSM. A C.D.P. creates new money, unlike borrowing someone else's deposit from a pool. And the maximum mint is a cliff edge, not a target, worth staying well back from.",
   chapter="Recap", title="Recap", check=False,
   items=["A CDP: mint a stablecoin against locked collateral, owe it back plus a fee", "The minimum collateral ratio is the line: below it, automatic liquidation",
          "The peg holds through over-collateralisation, liquidations, rates, and a PSM", "A CDP creates new money — unlike borrowing someone else's deposit",
          "The maximum mint is a cliff edge, not a target"])
sc("cta", "Set your collateral ratio target well above the minimum, compare the stability fee to lending-pool rates, and know your exit if the peg breaks. That's the end of Module three. Next up, Module four.",
   "Set your collateral ratio target well above the minimum, compare the stability fee to lending-pool rates, and know your exit if the peg breaks. That's the end of Module 3. Next up, Module 4.",
   chapter="Recap", button="Next: Module 4", sub="Continuing the On-Chain Operator Program")

spec = {"id": "lesson-03-7", "title": "Lesson 3.7: CDP stablecoins, minting your own dollars", "size": [1920, 1080], "group": "lessons", "maxMinutes": 25,
        "tag": "Lesson 3.7", "gold": True, "music": True, "musicLevel": 0.14, "seed": 68,
        "use": "Lesson 3.7 page in the Whop course. Hand-written gold-standard script: what a CDP is, the minimum collateral ratio, how the peg holds, CDP vs lending-pool borrowing, and the source material's own 10-ETH/$10,000-mint worked example, as walk-throughs.",
        "thumbnail": {"title": "CDP stablecoins", "subtitle": "Lesson 3.7"}, "scenes": S}
out = ROOT / "video-scripts" / "gold" / "lesson-03-7.json"
out.write_text(json.dumps(spec, indent=1, ensure_ascii=False))
words = sum(len(s["vo"].replace("[[pause 4]]", "").split()) for s in S)
print(f"{len(S)} scenes, {words} words, est {(words / 171 * 60 + len(S) * 1.3 + 4 * 3) / 60:.1f} min")
