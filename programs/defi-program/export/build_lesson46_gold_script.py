#!/usr/bin/env python3
"""Gold-standard script for Lesson 4.6, Airdrops & points: opportunity
cost (target 11-14 minutes, per the "a bit longer" note for lessons from
here on). Walks how airdrops and points actually work (eligibility,
snapshots, sybil filters, nothing promised), the fake-claim-site scam
risk, and the source material's own worked example (EV = 0.3 x 1500 -
200 = $250, compared against $10,000 earning a risk-light 5%/$500 a
year elsewhere — the farm has to beat that plus its extra risk, and in
this exact scenario it doesn't), as visual walk-throughs. Written in one
pass at the full target length (no separate expansion round).

Writes video-scripts/gold/lesson-04-6.json (the generator skips lessons
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
sc("title", "Lesson four point six. Airdrops and points: opportunity cost. By the end, you'll be able to price farming for a future airdrop as exactly what it is: a bet, with real costs, not a guaranteed reward.",
   "Lesson 4.6. Airdrops & points: opportunity cost. By the end, you'll be able to price farming for a future airdrop as exactly what it is: a bet, with real costs, not a guaranteed reward.",
   chapter="Intro", eyebrow="Lesson 4.6", num="4.6", title="Airdrops & points: opportunity cost", sub="Nothing here is promised. Price it like the bet it actually is.")
sc("pillars", "Here's the plan. How airdrops and points actually work, and who decides who gets what. Why nothing here is ever promised, and the scam risk that follows directly from that fact. A full worked example, pricing a specific farm as an actual expected value. And a checklist for deciding whether farming for one is even worth your time and capital.",
   chapter="Intro", title="What this lesson covers",
   items=[{"icon": "coins", "title": "How it actually works", "text": "Points first, eligibility rules, snapshots, sybil filters"}, {"icon": "alert", "title": "Nothing is promised", "text": "And why that's exactly what scammers exploit"},
          {"icon": "chart", "title": "Worked example", "text": "Pricing a farm as a real expected value"}, {"icon": "target", "title": "Opportunity cost", "text": "Compared against what your capital could earn elsewhere"}])

# ---------------------------------------------------------------- how it actually works
sc("title", "How this actually works.", chapter="How it actually works", eyebrow="How it actually works", num="1", title="Points first, a token maybe later",
   sub="Eligibility rules, snapshots, and sybil filters decide who gets what.")
img(D + "points-opportunity-cost.png", "Points are a bet, not a receipt",
    "Here's the actual sequence most airdrops follow. A protocol wants to reward its earliest, genuine users, specifically with tokens, once it eventually launches one. Long before that token exists, it very often tracks your activity as points instead, a running, unofficial scoreboard. Eligibility rules, and a specific snapshot moment in time, decide who ultimately qualifies. And sybil filters are specifically designed to exclude anyone believed to have split into many wallets, purely to farm a larger share for themselves.",
    chapter="How it actually works")
sc("flow", "Here's that same sequence, laid out as the actual stages it moves through. You take real actions, using a protocol, genuinely or otherwise. The protocol tracks that activity, often as points, well before any token exists. At some undisclosed snapshot moment, eligibility gets locked in. Sybil filters then attempt to exclude wallets believed to be farming unfairly. And only after all of that does an actual token, if one ever comes at all, finally get distributed.",
   chapter="How it actually works", title="From activity to an actual token",
   nodes=[{"label": "You take real actions", "sub": "Using the protocol, genuinely or otherwise", "icon": "chart"}, {"label": "Tracked as points", "sub": "Long before any token exists", "icon": "coins"},
          {"label": "An undisclosed snapshot locks eligibility", "sub": "You don't know the moment until after it's passed", "icon": "eye"}, {"label": "Sybil filters, then maybe a token", "sub": "If one ever actually comes at all", "icon": "alert"}])
sc("statement", "Worth being precise about what a sybil filter is actually trying to catch, since it directly shapes how these programs get designed. It's specifically trying to exclude wallets believed to belong to one person splitting themselves into many, purely to claim a disproportionately larger share. That's exactly why protocols keep both their eligibility rules and their snapshot timing deliberately vague, right up until the moment they're finally revealed.",
   chapter="How it actually works", kicker="What a sybil filter is actually catching", lines=["Wallets believed to be one person, split into many.", "That's why rules and timing stay deliberately vague until revealed."], sub="The vagueness isn't an oversight. It's the design.")
sc("statement", "Worth being precise about why protocols actually run these programs at all, since it clarifies what they genuinely want from you. They're trying to reward genuine early users specifically, and distribute ownership more broadly, rather than concentrating a new token entirely among insiders and early investors. That underlying goal is exactly why sybil filters exist, and exactly why genuine, organic usage tends to be rewarded over obviously artificial, repetitive farming patterns.",
   chapter="How it actually works", kicker="Why protocols actually do this", lines=["To reward genuine early users and distribute ownership broadly.", "That goal is exactly why sybil filters exist."], sub="Genuine, organic usage tends to be rewarded over obviously artificial patterns.")
sc("quiz", "Quick check. What exactly is a sybil filter? [[pause 4]] The answer: rules that exclude wallets believed to belong to the same person, farming the same program many times over through multiple wallets.",
   chapter="How it actually works", n=1, of=3, q="What's a sybil filter?",
   a="Rules that exclude wallets believed to belong to the same person farming many times.")

# ---------------------------------------------------------------- nothing is promised
sc("title", "Nothing here is ever promised.", chapter="Nothing is promised", eyebrow="Nothing is promised", num="1", title="Points are a bet, never a receipt",
   sub="And that exact fact is what scammers exploit directly.")
sc("statement", "Worth being completely precise about this, since it's the single most important fact in this entire lesson. Points are not a promise of a future token. There is no contract, no guarantee, and no obligation on the protocol's part to ever distribute anything at all, no matter how many points you've accumulated, or how confident the community narrative around it happens to sound.",
   chapter="Nothing is promised", kicker="The single most important fact here", lines=["Points are not a promise of a future token.", "No contract. No guarantee. No obligation, however confident the narrative sounds."], sub="Treat every point balance as speculative, all the way to actual distribution.")
sc("flow", "Here's exactly why that uncertainty becomes the scammer's opening, since it's a direct consequence of nothing being promised or officially confirmed in advance. Real anticipation, and real uncertainty about timing, builds up around a genuinely large, unconfirmed airdrop. A fake claim site then appears, closely mimicking the real protocol, right at the exact moment people are anxiously watching for the real announcement. And anyone who connects their wallet, or signs what looks like a routine claim transaction, can lose everything in that wallet instantly.",
   chapter="Nothing is promised", title="Why fake claim sites specifically target this moment",
   nodes=[{"label": "Genuine uncertainty builds", "sub": "Around a large, unconfirmed airdrop", "icon": "chart"}, {"label": "A fake claim site appears", "sub": "Closely mimicking the real protocol", "icon": "alert"},
          {"label": "Right at peak anxious watching", "sub": "Exactly when people are least careful", "icon": "eye"}, {"label": "One signed transaction, wallet drained", "sub": "This exact scam is covered in Lesson 1.6", "icon": "target"}])
sc("statement", "Worth repeating the one rule that defeats this specific scam completely, since it's simple enough to actually follow every single time. Only ever claim from a link you've verified through the protocol's own official channel, directly, never from a link in a random message, a comment, or a search ad, no matter how urgent or time-limited it claims to be.",
   chapter="Nothing is promised", kicker="The one rule that defeats this scam", lines=["Only claim from a link verified through the official channel directly.", "Never from a message, comment, or search ad, however urgent it seems."], sub="Urgency is the tell. A real airdrop doesn't need you to rush.")
sc("quiz", "Quick check. Are points a promise of a future token? [[pause 4]] The answer: no. Never treat a points balance as a promise, a receipt, or a guarantee of anything.",
   chapter="Nothing is promised", n=2, of=3, q="Are points a promise of tokens?",
   a="No.")

# ---------------------------------------------------------------- worked example
sc("title", "Worked example.", chapter="Worked example", eyebrow="Worked example", num="1", title="Pricing a farm as an actual expected value",
   sub="The source material's own scenario.")
sc("steps", "Here's the expected-value formula first, using this program's own calculator. Probability of actually qualifying, times the airdrop's estimated value, minus your real costs of farming it, gas, time, and everything else you've spent. Plug in a thirty percent chance of qualifying, an estimated fifteen hundred dollar value, and two hundred dollars of real costs, and the expected value comes to exactly two hundred fifty dollars.",
   chapter="Worked example", title="defi_calc.py airdrop --probability 0.3 --value 1500 --costs 200",
   steps=["Probability (30%) × value ($1,500) = $450", "− $200 in real costs (gas, time, everything spent)", "Expected value = $250"], result="An actual number, not a hope")
sc("compare", "Now here's the actual comparison this expected value has to survive, against what that same capital could have earned somewhere else entirely. If the ten thousand dollars tied up farming this airdrop could instead have earned a risk-light five percent elsewhere, that's five hundred dollars a year, in an ordinary, well-understood position. The farm's two hundred fifty dollar expected value has to beat that five hundred dollars, plus compensate you for its own extra risk, or it's simply the worse choice.",
   chapter="Worked example",
   left={"label": "Farming the airdrop", "tone": "bad", "items": ["Expected value: $250", "Plus real uncertainty and extra risk"]},
   right={"label": "$10,000 at a risk-light 5%", "tone": "good", "items": ["$500/yr, in a well-understood position", "The bar the farm has to clear"]})
sc("title", "How much does the guess for probability matter?", chapter="Worked example", eyebrow="Worked example", num="2", title="The same $1,500 value and $200 costs, five different odds",
   sub="Probability is almost always the shakiest input in this formula.")
sc("chart", "Here's that same fifteen hundred dollar value and two hundred dollar cost, run across five different guesses for your actual probability of qualifying, since that number is almost always the shakiest input in this entire formula. At ten percent, the expected value is actually negative, fifty dollars, meaning the farm loses money on average. At twenty percent, it turns positive, at one hundred dollars. At the source material's own thirty percent, two hundred fifty. And at fifty percent, five hundred fifty.",
   chapter="Worked example", title="Expected value vs. probability of qualifying", kind="line",
   xlabels=["10%", "20%", "30%", "40%", "50%"], ymin=-100, ymax=600,
   yticks=[[0, "$0"], [250, "$250"], [500, "$500"]],
   series=[{"values": [-50, 100, 250, 400, 550], "tone": "warn", "label": "Expected value"}],
   marks=[{"i": 0, "text": "−$50 (loses money)", "tone": "bad"}, {"i": 2, "text": "$250 (the worked example)", "tone": "good"}])
sc("statement", "Notice what that negative value at ten percent actually tells you, since it's easy to only picture the optimistic end of this range. If your real odds of qualifying are genuinely that low, the honest expected value of farming is a loss, on average, even before comparing it against anything else you could have done with that same capital instead.",
   chapter="Worked example", kicker="What the negative end of the chart shows", lines=["At genuinely low odds, the expected value is a loss.", "Before even comparing it against any alternative at all."], sub="Get your own probability estimate honest before running the rest of the math.")
sc("steps", "Here's how to actually estimate your own probability of qualifying, rather than just guessing optimistically. Read the protocol's own stated eligibility criteria closely, and check your own activity honestly against it. Look at how similar, comparable protocols have handled past airdrops, for a realistic sense of typical qualifying rates. And when genuinely unsure, run the math at a deliberately conservative guess, not a hopeful one.",
   chapter="Worked example", title="Estimating your own probability",
   steps=["Read the protocol's stated eligibility criteria closely", "Check comparable protocols' past airdrops for typical rates", "When unsure, use a deliberately conservative guess"])
sc("statement", "Here's the one sentence this entire worked example exists to prove, worth holding onto more than the specific dollar figures involved. In this exact scenario, the farm's expected value doesn't even clear the safer alternative's return, before its extra risk is even accounted for at all, which means the honest answer here is that farming is the worse choice.",
   chapter="Worked example", kicker="The one sentence to keep", lines=["$250 doesn't clear $500, before extra risk is even counted.", "In this exact scenario, farming is the worse choice."], sub="Change the inputs, and the answer can change. Always run your own numbers.")
sc("quiz", "Quick check. What's the actual formula for an airdrop's expected value? [[pause 4]] The answer: probability of qualifying, times the airdrop's value, minus your real costs of farming it.",
   chapter="Worked example", n=3, of=3, q="What's the airdrop EV formula?",
   a="Probability × value − costs.")

# ---------------------------------------------------------------- checklist and recap
sc("compare", "Here's why the checklist's first item specifically distinguishes these two situations, since the real cost of farming differs enormously between them. Using a protocol you'd genuinely use anyway means the points are simply a bonus on top of activity you were already doing, at close to zero extra real cost. Taking on entirely new actions, purely to farm points, means every one of those costs, gas, time, and risk, is a real cost you're taking on solely for a speculative, unpromised outcome.",
   chapter="Checklist",
   left={"label": "Using a protocol you'd use anyway", "tone": "good", "items": ["Points are a bonus on existing activity", "Close to zero extra real cost"]},
   right={"label": "New actions purely to farm points", "tone": "warn", "items": ["Every cost is taken on solely for the bet", "Gas, time, and risk, all real"]})
sc("steps", "Here's your checklist. Do it before farming anything for points. Only take actions you'd genuinely take anyway, or set a strictly capped, specifically speculative budget for it, and nothing more. Compare its expected value against what that same capital could earn elsewhere, the way the worked example just did. And only ever claim through links you've verified from the protocol's own official channel.",
   chapter="Checklist", title="Your checklist",
   steps=["Only actions I'd take anyway, or a capped speculative budget", "Opportunity cost compared", "Claims only from verified official links"])
sc("bullets", "Let's recap. Airdrops reward early users, tracked first as points, decided by eligibility rules, a snapshot, and sybil filters. Nothing here is ever promised, which is exactly what fake claim sites exploit at the moment of peak anticipation. An airdrop farm has a real expected value, probability times value minus costs, and it has to beat what the same capital could earn safely elsewhere, plus its own extra risk. Price it as the bet it actually is.",
   chapter="Recap", title="Recap", check=False,
   items=["Airdrops: tracked as points first, decided by rules, snapshot, sybil filters", "Nothing is ever promised — fake claim sites exploit exactly that uncertainty",
          "Expected value: probability × value − costs", "It has to beat what the same capital earns safely elsewhere, plus its own risk"])
sc("cta", "Only farm what you'd do anyway, or a capped speculative budget, compare the opportunity cost honestly, and claim only from verified official links. Next up, Lesson four point seven: stablecoin savings rates and yield-bearing stablecoins.",
   "Only farm what you'd do anyway, or a capped speculative budget, compare the opportunity cost honestly, and claim only from verified official links. Next up, Lesson 4.7: stablecoin savings rates and yield-bearing stablecoins.",
   chapter="Recap", button="Next: Lesson 4.7", sub="Stablecoin savings rates and yield-bearing stablecoins")

spec = {"id": "lesson-04-6", "title": "Lesson 4.6: Airdrops & points, opportunity cost", "size": [1920, 1080], "group": "lessons", "maxMinutes": 25,
        "tag": "Lesson 4.6", "gold": True, "music": True, "musicLevel": 0.14, "seed": 75,
        "use": "Lesson 4.6 page in the Whop course. Hand-written gold-standard script: how airdrops/points work, why nothing is promised and the fake-claim-site risk, and the source material's own EV-vs-opportunity-cost worked example, as walk-throughs.",
        "thumbnail": {"title": "Airdrops & points", "subtitle": "Lesson 4.6"}, "scenes": S}
out = ROOT / "video-scripts" / "gold" / "lesson-04-6.json"
out.write_text(json.dumps(spec, indent=1, ensure_ascii=False))
words = sum(len(s["vo"].replace("[[pause 4]]", "").split()) for s in S)
print(f"{len(S)} scenes, {words} words, est {(words / 171 * 60 + len(S) * 1.3 + 4 * 3) / 60:.1f} min")
