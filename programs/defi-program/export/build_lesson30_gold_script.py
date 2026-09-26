#!/usr/bin/env python3
"""Gold-standard script for Lesson 3.0, the Module 3 Mastery Starter (about
10-15 minutes). Lending & Leverage: lending markets, borrowing against
collateral, and the one hard rule (liquidation). Teaches the module's five
words (collateral, LTV, health factor, liquidation, utilisation) and the
mastery ladder with animated flows/charts, reusing the module's own lesson
diagrams (lending-pool-flow, liquidation-cascade, health-factor, loop-spread,
perp-anatomy, cdp-mint) wherever they already cover the idea. Mirrors the
Lesson 1.0 / 2.0 Mastery Starter pattern.

Writes video-scripts/gold/lesson-03-0.json (the generator skips lessons
with a gold script). Spoken text (vo) spells numbers for the voice; cap is
the written caption, same sentences."""
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
CH = "assets/charts/"

# ---------------------------------------------------------------- intro
sc("title", "Lesson three point zero. The Mastery Starter for Module Three: Lending and Leverage. By the end, you'll know the five words this module runs on, and exactly how to tell when you've mastered it.",
   "Lesson 3.0. The Mastery Starter for Module 3: Lending and Leverage. By the end, you'll know the five words this module runs on, and exactly how to tell when you've mastered it.",
   chapter="Intro", eyebrow="Lesson 3.0 · Mastery Starter", num="3.0", title="Lending & Leverage", sub="Your map for Module 3, in pictures.")
sc("pillars", "Here's the plan. First, the sixty-second version: how lending markets actually work, and the one hard rule borrowing comes with. Second, the five words you'll need, each one drawn out. Third, what to have ready before you start. Fourth, your first safe step: supplying a small amount, with no borrowing yet. And finally, the mastery ladder, so you know exactly what finishing this module looks like.",
   chapter="Intro", title="What this lesson covers",
   items=[{"icon": "coins", "title": "The 60-second version", "text": "Earn by lending, or borrow without selling"}, {"icon": "book", "title": "Five words", "text": "Drawn out, not just defined"},
          {"icon": "clock", "title": "Before you start", "text": "Modules 0-2, comfort using a DEX"}, {"icon": "target", "title": "The ladder", "text": "How you'll know you've mastered it"}])

# ---------------------------------------------------------------- the 60-second version
sc("statement", "Here's the whole module in one sentence. Lending markets let you earn interest by lending your assets out, or let you borrow against what you already own, without ever selling it. Borrowing comes with exactly one hard rule, worth knowing before anything else: if your collateral's value falls too far, it gets sold automatically, at a penalty, whether you're watching or not.",
   chapter="The 60-second version", kicker="The 60-second version", lines=["Earn by lending. Or borrow without selling.", "One hard rule: fall too far, and it's sold automatically."], sub="This module builds the habits that keep you clear of that line.")
img(D + "lending-pool-flow.png", "How a lending pool actually works",
    "Here's the mechanism underneath every lending market. Lenders deposit assets into a shared pool, and earn interest, paid by whoever borrows from that same pool. Borrowers lock up collateral, worth more than what they borrow, and can borrow against it without selling. The interest rate itself moves with how much of the pool is currently borrowed, which is exactly word five, coming up shortly.",
    chapter="The 60-second version")
sc("statement", "This isn't a small corner of DeFi. Lending markets are consistently among the largest categories of value locked in the entire industry, because the core trade, earning yield, or unlocking liquidity without selling, is useful in almost any market condition. That's also exactly why the one hard rule matters so much: a lot of real value sits directly on the other side of it.",
   chapter="The 60-second version", kicker="Why this module exists", lines=["One of DeFi's largest categories,", "by value locked, in almost any market."], sub="A lot of real value sits directly on the other side of the one hard rule.")

# ---------------------------------------------------------------- words you'll need
sc("title", "Now, the five words you'll need.", chapter="Words you'll need", eyebrow="Words you'll need", num="5", title="Five words, drawn out",
   sub="Collateral · LTV · Health factor · Liquidation · Utilisation")
sc("flow", "Word one: collateral. What you lock up in order to borrow. Here's the actual sequence. You deposit an asset you own, as collateral. The protocol values it, continuously, against the current market price. And it stays locked, entirely unavailable to you, for as long as your loan against it stays open.",
   chapter="Words you'll need", title="What happens to your collateral",
   nodes=[{"label": "You deposit an asset", "sub": "As collateral, to borrow against", "icon": "wallet"}, {"label": "Valued continuously", "sub": "Against the current market price", "icon": "chart"},
          {"label": "Stays locked", "sub": "Entirely unavailable, while the loan is open", "icon": "lock"}])
sc("statement", "Word two: L.T.V., loan-to-value. Your debt, divided by your collateral's value. It's the single number that tells you how borrowed you actually are, at any moment. A lower L.T.V. means more room before trouble; a higher one means less. Every other safety number in this module, including word three, is really just a different way of expressing this same relationship.",
   chapter="Words you'll need", kicker="Word two: LTV", lines=["Debt ÷ collateral value.", "How borrowed you actually are, right now."], sub="Every other safety number is a different view of this same relationship.")
img(CH + "health-factor.png", "Word three: health factor",
    "Word three: health factor. Your actual safety margin, expressed as a single number. Above one, your position is safe. At exactly one, it's at the liquidation line. Below one, liquidation can happen, automatically, without warning. Watch this chart as E.T.H.'s price moves: the health factor tracks it directly, since collateral value is what the whole number is built from.",
    chapter="Words you'll need")
img(D + "liquidation-cascade.png", "Word four: liquidation",
    "Word four: liquidation. The forced, automatic sale of your collateral, to repay your debt, once your health factor crosses below one. It isn't a warning, and it isn't negotiable; it's code, executing exactly as written, the moment the number crosses the line. And in a fast, falling market, one liquidation can trigger selling pressure that pushes prices further down, triggering more.",
    chapter="Words you'll need")
sc("stats", "One quick, concrete number, so L.T.V. isn't just a formula. Deposit one thousand dollars of collateral, borrow four hundred dollars against it, and your L.T.V. is exactly forty percent: four hundred divided by one thousand. Most protocols cap how high that ratio can go before your position becomes eligible for liquidation.",
   "One quick, concrete number, so LTV isn't just a formula. Deposit $1,000 of collateral, borrow $400 against it, and your LTV is exactly 40%: $400 ÷ $1,000. Most protocols cap how high that ratio can go before your position becomes eligible for liquidation.",
   chapter="Words you'll need", stats=[["40% LTV", "$400 borrowed against $1,000 collateral"]])
sc("quiz", "Quick check. What does a health factor below one actually mean, right now? [[pause 4]] The answer: liquidation can happen, automatically, without warning. It's not a soft warning zone; it's the line itself.",
   chapter="Words you'll need", n=1, of=4, q="What does a health factor below one actually mean, right now?",
   a="Liquidation can happen, automatically, without warning.")
sc("flow", "Word five: utilisation. How much of a lending pool's total deposits are currently borrowed out. Here's why it matters directly. Low utilisation means most of the pool sits idle, so rates stay low, for both sides. As utilisation climbs toward full, rates rise, often sharply, to pull in more lenders and push out some borrowers, keeping the pool solvent.",
   chapter="Words you'll need", title="Why utilisation drives rates",
   nodes=[{"label": "Low utilisation", "sub": "Most deposits sit idle", "icon": "coins"}, {"label": "Rates stay low", "sub": "For both lenders and borrowers", "icon": "chart"},
          {"label": "Utilisation climbs", "sub": "Toward the pool's full capacity", "icon": "alert"}, {"label": "Rates rise sharply", "sub": "Pulls in lenders, pushes out borrowers", "icon": "swap"}])

# ---------------------------------------------------------------- before you start
sc("title", "Before you start.", chapter="Before you start", eyebrow="Before you start", num="2", title="What Modules 0-2 should have left you with",
   sub="Two things, ready before Lesson 3.1")
sc("bullets", "Two things, both from earlier modules. First, Modules Zero through Two done: safe wallet habits, and comfort trading on-chain, since you'll be interacting with real lending contracts in this module. Second, comfort actually using a DEX on a low-fee network, since your first safe step needs no new skill beyond that. If either is missing, go back and finish those first.",
   chapter="Before you start", title="Two things, ready to go", numbered=True,
   items=["Modules 0-2 done: safe wallet habits, comfort trading on-chain", "Comfort using a DEX, on a low-fee network"])

# ---------------------------------------------------------------- your first safe step
sc("title", "Your first safe step.", chapter="Your first safe step", eyebrow="Your first safe step", num="1", title="Supply. Read. Withdraw.",
   sub="No borrowing yet.")
sc("statement", "Your first step in this module doesn't touch borrowing at all. Supply twenty dollars of U.S.D.C. to a blue-chip lending market. Read its utilisation, right there on the same screen. Then withdraw it. You're building the habit of reading a market's real state before you ever put real debt against it.",
   chapter="Your first safe step", kicker="Step one", lines=["Supply $20. Read utilisation.", "Withdraw. No borrowing yet."], sub="Reading the market's state, before you ever owe anything against it.")
sc("flow", "Here's the worked example. Open a blue-chip lending market's supply screen. Deposit twenty dollars of U.S.D.C. Read the pool's current utilisation and supply rate, right there. Then withdraw the same twenty dollars. Small, reversible, and it teaches you exactly where to look before Lesson three point one asks you to actually calculate anything.",
   chapter="Your first safe step", title="Supply, read, withdraw",
   nodes=[{"label": "Open the supply screen", "sub": "A blue-chip lending market", "icon": "eye"}, {"label": "Deposit $20 USDC", "sub": "Small, and fully reversible", "icon": "coins"},
          {"label": "Read utilisation and rate", "sub": "Right there, on the same screen", "icon": "chart"}, {"label": "Withdraw it", "sub": "No borrowing, this step", "icon": "check"}])
sc("stats", "One real number, so this module doesn't feel like a niche corner of DeFi. Lending protocols have consistently held tens of billions of dollars in total value locked, across major chains, year after year. This is outside research, not this program's own data, but it's exactly why the habits in this module, reading utilisation, respecting the health-factor line, matter at real scale.",
   "One real number, so this module doesn't feel like a niche corner of DeFi. Lending protocols have consistently held tens of billions of dollars in total value locked, across major chains, year after year. This is outside research, not this program's own data, but it's exactly why the habits in this module matter at real scale.",
   chapter="Your first safe step", stats=[["$10Bs+", "typical total value locked in lending protocols (outside research)"]])
sc("quiz", "Quick check. Why does the first safe step in this module involve no borrowing at all? [[pause 4]] The answer: it builds the habit of reading a lending market's real state, utilisation and rates, before you ever put real debt against it.",
   chapter="Your first safe step", n=2, of=4, q="Why does the first safe step in this module involve no borrowing at all?",
   a="It builds the habit of reading a market's state before you owe anything against it.")

# ---------------------------------------------------------------- mastery ladder
sc("title", "The mastery ladder.", chapter="The mastery ladder", eyebrow="The mastery ladder", num="3", title="Three rungs",
   sub="Beginner · Practitioner · Master")
sc("chart", "Here's how you'll measure your progress through Module Three. Beginner: supplies stablecoins, and reads utilisation and rates before acting. Practitioner: borrows with a health factor of two or higher, and keeps a written defence ladder ready. And Master: runs correlated loops and perpetual futures positions, with computed liquidation prices and break-even rates, known in advance.",
   chapter="The mastery ladder", kind="bars", title="The mastery ladder",
   bars=[{"label": "Beginner", "text": "Supplies stablecoins, reads utilisation", "value": 1, "show": "Rung 1", "tone": "blue"},
         {"label": "Practitioner", "text": "HF ≥ 2, a written defence ladder", "value": 2, "show": "Rung 2", "tone": "blue"},
         {"label": "Master", "text": "Loops & perps, computed in advance", "value": 3, "show": "Rung 3", "tone": "good"}])
sc("bullets", "Here's the road ahead, lesson by lesson. Three point one, how lending markets work. Three point two, health factor and liquidation. Three point three, leveraged loops. Three point four, perpetual futures. And three point five, C.D.P.s and minting your own dollars against collateral.",
   "Here's the road ahead, lesson by lesson. 3.1, how lending markets work. 3.2, health factor and liquidation. 3.3, leveraged loops. 3.4, perpetual futures. And 3.5, CDPs and minting your own dollars against collateral.",
   chapter="The mastery ladder", title="The road ahead", numbered=True, compact=True,
   items=["3.1 · How lending markets work", "3.2 · Health factor and liquidation", "3.3 · Leveraged loops: the spread is everything", "3.4 · Perpetual futures", "3.5 · CDPs: minting your own dollars"])
img(CH + "loop-spread.png", "One more preview",
    "One more preview, from Lesson three point three. A leveraged loop, supplying, borrowing, and re-supplying the same asset repeatedly, only works when the supply rate beats the borrow rate; that spread is everything. Get the spread wrong, and leverage amplifies a loss exactly as fast as it would have amplified a gain.",
    chapter="You've mastered it when…")
img(D + "cdp-mint.png", "And one more, from the far end of the module",
    "And one more preview, from Lesson three point five, the far end of this module. A C.D.P., a collateralised debt position, lets you mint your own stablecoin directly against locked collateral, rather than borrowing an existing one from a pool. Same core idea as everything else in this module, over-collateralise, respect the health-factor line, just with a different destination for what you borrow.",
    chapter="You've mastered it when…")
sc("statement", "You've mastered this module when you can open a borrow, monitor it, and unwind it, without ever approaching liquidation, and without needing to check on it anxiously. Not a large position. A repeatable, controlled process, with a defence plan written down before you need it.",
   chapter="You've mastered it when…", kicker="The top rung", lines=["Open, monitor, unwind.", "Without ever approaching liquidation."], sub="Not a large position. A repeatable, controlled process.")
sc("quiz", "One more. Your health factor is currently one point three, and falling steadily as the market moves against you. What's the actual state of your position? [[pause 4]] The answer: still above the liquidation line, but with shrinking room. This is exactly when a written defence ladder tells you what to do next, not the moment to decide under pressure.",
   chapter="You've mastered it when…", n=3, of=4, q="Your health factor is 1.3 and falling steadily. What's the actual state of your position?",
   a="Still above the liquidation line, but with shrinking room — exactly when a written defence plan matters.")
sc("quiz", "Last check. What does mastering Module Three actually look like? [[pause 4]] The answer: opening, monitoring and unwinding a borrow without ever approaching liquidation, a repeatable process, not a lucky outcome.",
   chapter="You've mastered it when…", n=4, of=4, q="What does mastering Module 3 actually look like?",
   a="Opening, monitoring and unwinding a borrow without ever approaching liquidation.")

# ---------------------------------------------------------------- recap
sc("statement", "One honest note before the recap, since leverage and perpetual futures sit at the top of this module's ladder for a reason. Everything in this module works both directions: the same borrowing mechanism that lets you unlock liquidity without selling can amplify a loss just as fast as a gain, once leverage is involved. Master the beginner and practitioner rungs first. There's no shortcut past them.",
   chapter="You've mastered it when…", kicker="Why the ladder has an order", lines=["Leverage amplifies both directions.", "Master beginner and practitioner first — no shortcut."], sub="The same mechanism, either way it moves.")
sc("bullets", "Let's recap the five words. Collateral: what you lock up, valued continuously. L.T.V.: debt over collateral value, how borrowed you are. Health factor: your safety margin; below one means liquidation. Liquidation: automatic, forced, no warning. And utilisation: how full a pool is, and exactly what drives its rates.",
   chapter="Recap", title="Recap", check=False,
   items=["Collateral: what you lock up, valued continuously", "LTV: debt ÷ collateral value — how borrowed you are",
          "Health factor: your safety margin; below 1 means liquidation", "Liquidation: automatic, forced, no warning", "Utilisation: how full a pool is; what drives its rates"])
sc("cta", "That's the Mastery Starter. You now have the whole module in your head: why lending markets exist, the five words, your first safe step, and the ladder that tells you when you're done. Next up, Lesson three point one: How lending markets work.",
   "That's the Mastery Starter. You now have the whole module in your head: why lending markets exist, the five words, your first safe step, and the ladder that tells you when you're done. Next up, Lesson 3.1: How lending markets work.",
   chapter="Recap", button="Next: Lesson 3.1", sub="How lending markets work")

spec = {"id": "lesson-03-0", "title": "Lesson 3.0: Mastery Starter", "size": [1920, 1080], "group": "lessons", "maxMinutes": 25, "tag": "Lesson 3.0",
        "gold": True, "music": True, "musicLevel": 0.14, "seed": 61,
        "use": "Lesson 3.0 page in the Whop course. Hand-written gold-standard script: the Module 3 Mastery Starter, taught with animated flows and charts.",
        "thumbnail": {"title": "Lending & Leverage", "subtitle": "Lesson 3.0 · Mastery Starter"}, "scenes": S}
out = ROOT / "video-scripts" / "gold" / "lesson-03-0.json"
out.write_text(json.dumps(spec, indent=1, ensure_ascii=False))
words = sum(len(s["vo"].replace("[[pause 4]]", "").split()) for s in S)
print(f"{len(S)} scenes, {words} words, est {(words / 171 * 60 + len(S) * 1.3 + 4 * 3) / 60:.1f} min")
