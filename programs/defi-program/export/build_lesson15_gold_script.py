#!/usr/bin/env python3
"""Gold-standard script for Lesson 1.5, Stablecoins and how they break (about
12-15 minutes). Classifies stablecoins by design (fiat-backed, crypto-backed,
synthetic/hedged, algorithmic), walks the peg-arbitrage mechanism as an
animated flow, and covers two real, dated case studies as visual walk-throughs:
Terra's UST collapse (May 2022) and USDC's SVB-driven depeg and recovery
(March 2023, as a real-shaped line chart). Built to the "walk-through, not
narration" standard: almost every idea is a flow, steps, chart or callout
image, not a statement read over a static screen.

Writes video-scripts/gold/lesson-01-5.json (the generator skips lessons with a
gold script). Spoken text (vo) spells numbers for the voice; cap is the written
caption, same sentence count as vo."""
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
sc("title", "Lesson one point five. Stablecoins and how they break. By the end, you'll be able to classify any stablecoin by its design, and name exactly what could break its peg.",
   "Lesson 1.5. Stablecoins and how they break. By the end, you'll be able to classify any stablecoin by its design, and name exactly what could break its peg.",
   chapter="Intro", eyebrow="Lesson 1.5", num="1.5", title="Stablecoins and how they break", sub="Classify the design. Name what could break it.")
sc("pillars", "Here's the plan, and we'll walk through every part of it visually, not just talk about it. First, the four designs, side by side. Second, the arbitrage mechanism that holds a peg together, as a loop you'll watch run. Third, two real, dated collapses: Terra in twenty twenty-two, and U.S.D.C. in twenty twenty-three, each one walked through step by step. And finally, a full worked example with real percentages.",
   "Here's the plan, and we'll walk through every part of it visually, not just talk about it. First, the four designs, side by side. Second, the arbitrage mechanism that holds a peg together, as a loop you'll watch run. Third, two real, dated collapses: Terra in 2022, and USDC in 2023, each one walked through step by step. And finally, a full worked example with real percentages.",
   chapter="Intro", title="What this lesson covers",
   items=[{"icon": "layers", "title": "Four designs", "text": "Fiat, crypto, synthetic, algorithmic"}, {"icon": "swap", "title": "The peg mechanism", "text": "Watch the arbitrage loop run"},
          {"icon": "alert", "title": "Two real collapses", "text": "Terra 2022, USDC 2023"}, {"icon": "chart", "title": "A worked example", "text": "Real percentages, walked through"}])

# ---------------------------------------------------------------- four designs
sc("title", "Four designs.", chapter="Four designs", eyebrow="Four designs", num="4", title="Every stablecoin is one of these",
   sub="Fiat-backed · Crypto-backed · Synthetic/hedged · Algorithmic")
img(D + "stablecoin-designs.png", "Three of the four",
    "Three designs, and exactly how each one breaks. Fiat-backed: cash and treasuries held by an issuer, and it breaks if those reserves are frozen or turn out missing. Crypto-backed: over-collateralised with on-chain crypto, and it breaks if collateral falls faster than liquidations can catch up. Algorithmic: held up mostly by incentives and a sister token, and it breaks the moment confidence goes and the mechanism spirals against itself.",
    chapter="Four designs", callouts=[{"x": 0.2, "y": 0.68, "text": "Breaks: reserves frozen", "at": 1}, {"x": 0.55, "y": 0.68, "text": "Breaks: collateral crashes", "at": 3}, {"x": 0.83, "y": 0.68, "text": "Breaks: confidence spiral", "at": 5}])
sc("flow", "And the fourth design: synthetic, or hedged. This one holds a spot asset and a matching short position on a derivative, so the two move opposite each other and roughly cancel out. It breaks when funding on that short turns sharply negative for a sustained period, or when the exchange holding the position runs into trouble itself. Four designs, four different failure points, and none of them fail for the same reason.",
   chapter="Four designs", title="Synthetic / hedged: how it's built",
   nodes=[{"label": "Spot asset held", "sub": "Long exposure", "icon": "coins"}, {"label": "Matching short", "sub": "On a derivative", "icon": "chart"},
          {"label": "Roughly cancels out", "sub": "That's the peg", "icon": "check"}, {"label": "Breaks if…", "sub": "Funding flips, or the venue fails", "icon": "alert"}])
sc("stats", "One real number for scale, so this doesn't feel abstract. Stablecoins collectively represent well over a hundred billion dollars of value, moving through DeFi and exchanges every single day. That's the size of the thing whose design you're now able to classify, and whose failure points you can now name, before you deposit into any of it.",
   chapter="Four designs", stats=[["$150B+", "combined stablecoin value, roughly (outside research, illustrative)"]])
sc("quiz", "Quick check. Two stablecoins are both backed by the exact same collateral. Are they diversified, if you hold both? [[pause 4]] The answer: no. They share the same failure point, so a problem with that collateral hits both at once, not just one of them.",
   chapter="Four designs", n=1, of=3, q="Two stablecoins are both backed by the same collateral. Are they diversified if you hold both?",
   a="No. They share the same failure point — a problem with that collateral hits both at once.")

# ---------------------------------------------------------------- peg mechanics
sc("title", "The peg mechanism.", chapter="The peg mechanism", eyebrow="The peg mechanism", num="1", title="Watch it hold itself together",
   sub="Redemption access, plus arbitrage.")
sc("flow", "Here's the loop that holds a peg near one dollar, running in real time. The coin trades at ninety-eight cents on the open market, below its dollar target. An arbitrageur buys it cheap, at ninety-eight cents. They redeem it with the issuer, for a full dollar. And they pocket the two-cent difference, which pushes buying pressure back into the market and nudges the price back toward one dollar. That loop runs constantly, automatically, as long as redemption actually works.",
   chapter="The peg mechanism", title="The arbitrage loop, running", layout="cycle",
   nodes=[{"label": "Trades at $0.98", "sub": "Below the $1 target", "icon": "chart"}, {"label": "Bought cheap", "sub": "By an arbitrageur", "icon": "coins"},
          {"label": "Redeemed for $1.00", "sub": "With the issuer", "icon": "bank"}, {"label": "Price nudges up", "sub": "Toward $1 again", "icon": "check"}])
sc("flow", "Now run the exact same loop backwards, above one dollar, because the peg works in both directions. The coin trades at one dollar two, above target. An arbitrageur mints new coins from the issuer, paying one dollar each. They sell those new coins on the open market, at one dollar two. And that new supply pushes the price back down, toward one dollar again. Above or below target, the same arbitrage pressure pulls the price back to the peg.",
   chapter="The peg mechanism", title="The same loop, running above target", layout="cycle",
   nodes=[{"label": "Trades at $1.02", "sub": "Above the $1 target", "icon": "chart"}, {"label": "Minted at $1.00", "sub": "By an arbitrageur", "icon": "bank"},
          {"label": "Sold at $1.02", "sub": "On the open market", "icon": "coins"}, {"label": "Price nudges down", "sub": "Toward $1 again", "icon": "check"}])
sc("statement", "Read both loops again, and notice the one word that makes them work: redemption. The peg isn't magic, and it isn't really about the price chart at all. It's only as strong as redemption access and reserve quality. Break either one, and the loop simply stops running.",
   chapter="The peg mechanism", kicker="The one word that matters", lines=["Not the price chart.", "Redemption access and reserve quality."], sub="Break either one, and the loop stops running.")

# ---------------------------------------------------------------- case study: Terra
sc("title", "Case study: Terra, May 2022.", chapter="Case study: Terra (2022)", eyebrow="A real collapse", num="1", title="An algorithmic design, unwinding",
   sub="TerraUSD (UST) lost its peg and collapsed toward zero.")
sc("flow", "Here's how it actually unwound, step by step. U.S.T. depended on confidence in its sister token, Luna, to hold its peg, with no hard reserve behind it. Large withdrawals began, pushing U.S.T. below one dollar. The mechanism tried to defend the peg by minting huge amounts of Luna, which crashed Luna's own price. A falling Luna made the peg mechanism weaker, not stronger, which triggered still more withdrawals. And the two tokens spiralled down together, toward zero, in a matter of days.",
   chapter="Case study: Terra (2022)", title="How UST actually unwound",
   nodes=[{"label": "No hard reserve", "sub": "Depended on confidence in Luna", "icon": "alert"}, {"label": "Withdrawals begin", "sub": "UST slips below $1", "icon": "chart"},
          {"label": "Mechanism mints Luna", "sub": "To try to defend the peg", "icon": "coins"}, {"label": "Luna price crashes", "sub": "The defense weakens the peg further", "icon": "alert"},
          {"label": "Spiral to near zero", "sub": "In days, not months", "icon": "chart"}])
sc("stats", "Put a real number on how fast it happened. UST traded near one dollar for most of its history, and within roughly five days in May of twenty twenty-two, it and Luna together lost tens of billions of dollars of combined value. That's not a slow decline you'd have weeks to react to. It's the specific speed a reflexive spiral moves at, once it actually starts.",
   "Put a real number on how fast it happened. UST traded near $1 for most of its history, and within roughly five days in May 2022, it and Luna together lost tens of billions of dollars of combined value. That's not a slow decline you'd have weeks to react to. It's the specific speed a reflexive spiral moves at, once it actually starts.",
   chapter="Case study: Terra (2022)", stats=[["≈5 days", "from depeg to near-total collapse (May 2022)"]])
sc("statement", "This is what the checklist means by a reflexive death spiral. Each step made the next step worse, not better, and there was no outside reserve anywhere in the loop to stop it. That's the specific, structural weakness of an algorithmic design, not a one-off accident.",
   chapter="Case study: Terra (2022)", kicker="Why it's called reflexive", lines=["Each step made the next", "step worse, not better."], sub="No outside reserve anywhere in the loop to stop it.")

# ---------------------------------------------------------------- case study: USDC
sc("title", "Case study: USDC, March 2023.", chapter="Case study: USDC (2023)", eyebrow="A real collapse, and a recovery", num="2", title="A fiat-backed design, under real stress",
   sub="Briefly traded well below $1, then recovered.")
sc("chart", "Here's the shape of it, as it actually happened. Through most of March, U.S.D.C. held steady near one dollar. Then, on March eleventh, news broke that part of its reserves sat at Silicon Valley Bank, which had just failed. The price dropped sharply, down toward eighty-seven cents at its worst. Once regulators confirmed depositors, including Circle's reserves, would be made whole, the price recovered fully within about two days, back to one dollar.",
   "Here's the shape of it, as it actually happened. Through most of March, USDC held steady near one dollar. Then, on March 11th, news broke that part of its reserves sat at Silicon Valley Bank, which had just failed. The price dropped sharply, down toward $0.87 at its worst. Once regulators confirmed depositors, including Circle's reserves, would be made whole, the price recovered fully within about two days, back to $1.00.",
   chapter="Case study: USDC (2023)", kind="line", title="USDC's price, March 2023", sub="Shape is real; exact intraday values vary by source",
   series=[{"values": [1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 0.97, 0.87, 0.93, 0.99, 1.00, 1.00, 1.00, 1.00], "tone": "blue"}],
   xlabels=["Mar 1", "", "", "", "", "", "", "", "", "", "Mar 11", "", "", "Mar 13", "", "", "", "Mar 18"],
   yticks=[[0.87, "$0.87"], [1.00, "$1.00"]], ymin=0.83, ymax=1.03,
   marks=[{"i": 11, "text": "SVB news breaks: reserves exposed", "tone": "bad", "below": True}, {"i": 14, "text": "Depositors backstopped: peg restored", "tone": "good", "below": False}])
sc("flow", "Zoom into just the two recovery days, because that's where the real lesson sits. On March eleventh, the discount was near its worst, close to eighty-seven cents, and headlines were uncertain about the reserves. By March thirteenth, regulators had confirmed depositors would be made whole, redemption confidence returned, and the price closed the gap almost completely, back near one dollar. Two days, from worst point to fully recovered, once the actual question, “are the reserves real and reachable,” got a clear answer.",
   chapter="Case study: USDC (2023)", title="Two days, worst point to recovered",
   nodes=[{"label": "Mar 11: ≈$0.87", "sub": "Reserves' exposure unclear", "icon": "alert"}, {"label": "Regulators confirm", "sub": "Depositors made whole", "icon": "bank"},
          {"label": "Redemption confidence returns", "sub": "Minters act again", "icon": "check"}, {"label": "Mar 13: ≈$1.00", "sub": "Peg recovered", "icon": "swap"}])
sc("compare", "Compare the two collapses directly, because the contrast is the whole lesson. Terra had no outside reserve, so the spiral had nothing to stop it, and it never recovered. U.S.D.C. had real reserves, just temporarily hard to access, so once access was restored, the peg came straight back. Same word, “depeg,” two completely different outcomes, because the underlying design was different.",
   chapter="Case study: USDC (2023)",
   left={"label": "Terra (UST), 2022", "tone": "bad", "items": ["No outside reserve", "Nothing to stop the spiral", "Never recovered"]},
   right={"label": "USDC, 2023", "tone": "good", "items": ["Real reserves, temporarily hard to reach", "Access restored within days", "Peg fully recovered"]})
sc("quiz", "Quick check. What actually caused USDC's price to recover in March twenty twenty-three? [[pause 4]] The answer: confirmation that the reserves were real and depositors would be made whole, which restored confidence and let redemption function normally again. Not a change to how the coin itself works.",
   "Quick check. What actually caused USDC's price to recover in March 2023? [[pause 4]] The answer: confirmation that the reserves were real and depositors would be made whole, which restored confidence and let redemption function normally again. Not a change to how the coin itself works.",
   chapter="Case study: USDC (2023)", n=2, of=3, q="What actually caused USDC's price to recover in March 2023?",
   a="Confirmation the reserves were real and depositors would be made whole — redemption confidence returned. Nothing about the coin's design changed.")

# ---------------------------------------------------------------- worked example
sc("title", "Worked example.", chapter="Worked example", eyebrow="Worked example", num="2.9%", title="A fiat-backed coin trades at $0.97",
   sub="Redemption: $1.00 minus a 0.1% fee. Verified institutions only.")
sc("chart", "Here's the arbitrage math, worked in full. Buy the coin on the open market for ninety-seven cents. Redeem it with the issuer for a dollar, minus a zero point one percent fee, so about ninety-nine cents ninety. The margin: roughly two point nine percent per coin. On paper, that margin should pull minters in and push the price back to one dollar, exactly like the loop you watched earlier.",
   "Here's the arbitrage math, worked in full. Buy the coin on the open market for $0.97. Redeem it with the issuer for $1.00, minus a 0.1% fee, so about $0.999. The margin: roughly 2.9% per coin. On paper, that margin should pull minters in and push the price back to $1.00, exactly like the loop you watched earlier.",
   chapter="Worked example", kind="bars", title="The arbitrage math", sub="Illustrative figures from this worked example",
   bars=[{"label": "Buy price", "text": "On the open market", "value": 0.97, "show": "$0.97", "tone": "warn"}, {"label": "Redeem value", "text": "$1.00 minus 0.1% fee", "value": 0.999, "show": "≈$0.999", "tone": "good"}],
   note="≈2.9% margin per coin — enough to normally pull arbitrageurs in.")
sc("flow", "But notice exactly where you, personally, sit in this picture. You can't redeem directly, only verified institutional minters can. So you're not doing the arbitrage yourself. You're relying on minters acting, and on the reserves genuinely being real. If markets start doubting the reserves, minters may simply not step in, and the discount can grow instead of closing, no matter how attractive the math looks on paper.",
   chapter="Worked example", title="Where you actually sit in this loop",
   nodes=[{"label": "You hold the coin", "sub": "At $0.97", "icon": "wallet"}, {"label": "You can't redeem", "sub": "Only verified minters can", "icon": "alert"},
          {"label": "You rely on minters", "sub": "To act, and reserves to be real", "icon": "eye"}, {"label": "If doubted: discount grows", "sub": "The math alone doesn't fix it", "icon": "chart"}])
sc("steps", "So here's the same habit, as a decision walk-through you can actually run during a real depeg. First: check the type. Is it fiat, crypto, synthetic or algorithmic? Second: check redemption. Can you, or can only institutions, actually redeem right now? Third: check the news. Is this a reserve problem, or a market-wide panic with no reserve issue at all? And fourth: apply your exit rule, the one you set in advance, not one you invent under pressure.",
   chapter="Worked example", title="Reading a depeg, in the moment",
   steps=["Check the type: fiat, crypto, synthetic, algorithmic", "Check redemption: who can actually redeem, right now", "Check the news: reserve problem, or market panic", "Apply your exit rule, set in advance"], result="A decision made calmly, before the stress, not during it")
sc("statement", "One honest note to close the worked example on. None of this means avoid stablecoins entirely. They're genuinely useful, and you'll use them constantly through this program. It means treat “stable” as a description of intent, not a guarantee, and know which of the four designs you're actually holding before size or urgency ever makes that question hard to answer calmly.",
   chapter="Worked example", kicker="Not a reason to avoid them", lines=["“Stable” describes intent,", "not a guarantee."], sub="Know the design before size or urgency makes the question hard.")
sc("quiz", "Last check. What keeps a fiat-backed stablecoin trading near one dollar? [[pause 4]] The answer: redemption for a dollar of reserves, plus arbitrageurs who can actually access that redemption.",
   chapter="Worked example", n=3, of=3, q="What keeps a fiat-backed stablecoin trading near $1?",
   a="Redemption for $1 of reserves, plus arbitrageurs who can actually access that redemption.")

# ---------------------------------------------------------------- checklist and recap
sc("steps", "Here's your checklist, as a habit for every stablecoin you hold. Know the type and backing of each one. Know exactly who can redeem, and how. Don't count two stablecoins as diversified if they share issuers or collateral. And set a depeg exit rule in advance, for example: sell or rotate out if it's below ninety-nine cents for longer than a set number of hours.",
   "Here's your checklist, as a habit for every stablecoin you hold. Know the type and backing of each one. Know exactly who can redeem, and how. Don't count two stablecoins as diversified if they share issuers or collateral. And set a depeg exit rule in advance, for example: sell or rotate out if it's below $0.99 for longer than a set number of hours.",
   chapter="Checklist", title="Your checklist", steps=["Know the type and backing of each one", "Know who can redeem, and how", "Shared issuer/collateral isn't diversified", "Set a depeg exit rule in advance"], result="A rule set before the stress, not during it")
sc("bullets", "Let's recap. Four designs, four different failure points: fiat, crypto, synthetic, algorithmic. A peg holds because of an arbitrage loop, and that loop only runs while redemption and reserves both hold up. Terra had neither, and spiralled to zero. U.S.D.C. had both, and recovered in days. Know your stablecoin's design, and have your exit rule ready before you ever need it.",
   chapter="Recap", title="Recap", check=False,
   items=["Four designs: fiat, crypto, synthetic, algorithmic — four failure points", "A peg runs on an arbitrage loop; it needs redemption and real reserves",
          "Terra (2022): neither held, spiralled to zero. USDC (2023): both held, recovered.", "Know your stablecoin's design, and set your exit rule in advance"])
sc("cta", "Do the checklist now, before you move on. You now have the whole lesson in your head: the four designs, the arbitrage loop that holds a peg together, two real collapses that ended completely differently, and a decision walk-through for the next time a stablecoin wobbles. Next up, Lesson one point six: Scam defence.",
   "Do the checklist now, before you move on. You now have the whole lesson in your head: the four designs, the arbitrage loop that holds a peg together, two real collapses that ended completely differently, and a decision walk-through for the next time a stablecoin wobbles. Next up, Lesson 1.6: Scam defence.",
   chapter="Recap", button="Next: Lesson 1.6", sub="Scam defence")

spec = {"id": "lesson-01-5", "title": "Lesson 1.5: Stablecoins and how they break", "size": [1920, 1080], "group": "lessons", "maxMinutes": 25,
        "tag": "Lesson 1.5", "gold": True, "music": True, "musicLevel": 0.14, "seed": 47,
        "use": "Lesson 1.5 page in the Whop course. Hand-written gold-standard script: 4 designs, the peg-arbitrage loop, real Terra (2022) and USDC (2023) case studies, worked arbitrage math.",
        "thumbnail": {"title": "Stablecoins & how they break", "subtitle": "Lesson 1.5"}, "scenes": S}
out = ROOT / "video-scripts" / "gold" / "lesson-01-5.json"
out.write_text(json.dumps(spec, indent=1, ensure_ascii=False))
words = sum(len(s["vo"].replace("[[pause 4]]", "").split()) for s in S)
print(f"{len(S)} scenes, {words} words, est {(words / 171 * 60 + len(S) * 1.3 + 4 * 3) / 60:.1f} min")
