#!/usr/bin/env python3
"""Gold-standard script for Lesson 6.1, Protocol due diligence (ch. 24).
Target 10-13 minutes per the "a bit longer" note active for lessons from
here on. Walks the six-step research loop from Lesson 6.0 in real depth,
one dedicated scene per step, then applies all six to the source's own
worked-example verdict (Protocol Y, lending, Arbitrum), breaks that
verdict into size/conditions/exit, and covers why the rating is the
worst risk found, never the average. Written in one pass at full target
length, reusing the module's research-loop.png and reaching back into
Module 5's own dependency map and audit-coverage.png for the
Dependencies and Evidence steps.

Writes video-scripts/gold/lesson-06-1.json (the generator skips lessons
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

# ---------------------------------------------------------------- intro
sc("title", "Lesson six point one. Protocol due diligence. Today you'll run the six-step research loop from Lesson six point zero in real depth, one step at a time, and land it on an actual written verdict.",
   "Lesson 6.1. Protocol due diligence. Today you'll run the six-step research loop from Lesson 6.0 in real depth, one step at a time, and land it on an actual written verdict.",
   chapter="Intro", eyebrow="Lesson 6.1 · ch. 24", num="6.1", title="Protocol due diligence", sub="One loop. Six steps. One written verdict.")
sc("statement", "Here's the objective for this lesson, in one sentence. Run the six-step research loop on a real protocol, and reach a written verdict: not a vague feeling about it, an actual verdict, with a size, conditions, and an exit written down.",
   chapter="Intro", kicker="Objective", lines=["Run the six-step loop on a real protocol.", "Reach a written verdict — not a vague feeling."], sub="This lesson is that loop, run for real, step by step.")
img(D + "research-loop.png", "The loop this lesson runs in full",
    "Here's the loop from last lesson again, since this entire video walks through it. Mechanism, cash flow, dependencies, solvency, evidence, and exit. Six questions, asked in order, every single time.",
    chapter="Intro")

# ---------------------------------------------------------------- step 1: mechanism
sc("title", "Step one: mechanism.", chapter="Step 1: Mechanism", eyebrow="Step 1 of 6", num="1", title="What the contracts actually do",
   sub="Users, assets, and incentives.")
sc("steps", "Mechanism means answering three concrete questions about a protocol's own contracts. Who actually uses this: lenders, borrowers, traders, liquidity providers. What assets actually move through it: which tokens, on which chain. And what incentive actually keeps people using it: real yield, token rewards, or something else entirely.",
   chapter="Step 1: Mechanism", title="Three questions for mechanism",
   steps=["Who uses it: lenders, borrowers, traders, LPs", "What assets move through it, and on which chain", "What incentive keeps people using it — real yield, or rewards"], result="A one-paragraph answer, not a marketing summary")
sc("statement", "Worth being direct here: mechanism is about what the contracts genuinely do, not what the website says they do. A protocol's own marketing page and its actual deployed contracts aren't always the same document, and this step is where you check.",
   chapter="Step 1: Mechanism", kicker="What mechanism actually checks", lines=["What the contracts genuinely do, not the marketing page.", "Those two aren't always the same document."], sub="This step is where you check the difference.")

# ---------------------------------------------------------------- step 2: cash flow
sc("title", "Step two: cash flow.", chapter="Step 2: Cash flow", eyebrow="Step 2 of 6", num="2", title="Real fees and interest vs. emissions",
   sub="Where the money genuinely comes from.")
sc("statement", "Cash flow means separating two very different sources of protocol income. Real revenue: actual fees and interest, paid by actual users, for an actual service. And emissions: newly minted tokens, handed out as rewards, that dilute existing holders whether or not the protocol itself is genuinely profitable.",
   chapter="Step 2: Cash flow", kicker="Two very different sources", lines=["Real revenue: fees and interest, paid by actual users.", "Emissions: new tokens handed out as rewards, whether or not it's profitable."], sub="A protocol can look busy while running entirely on the second one.")
sc("stats", "Here's why that distinction actually matters, using a purely illustrative example: Protocol Z. It pays out five hundred thousand dollars a month in reward emissions, but collects only eighty thousand dollars a month in real fees. That's real revenue covering just sixteen percent of what it pays out. With a seven-million-dollar rewards budget left in its treasury, that gap runs for roughly fourteen months before the rewards have to shrink, or stop.",
   chapter="Step 2: Cash flow", title="Real fees vs. emissions (illustrative)",
   stats=[["$80k/mo", "Real fees collected"], ["$500k/mo", "Emissions paid out"], ["~14 months", "Until the rewards budget runs dry"]])
sc("statement", "That's the actual risk emissions-funded activity carries. It's not that emissions are inherently bad; new protocols often need them to bootstrap real usage. It's that emissions are temporary by construction, and this step is where you check whether real revenue is growing to replace them before the budget actually runs out.",
   chapter="Step 2: Cash flow", kicker="The risk isn't emissions. It's relying on them", lines=["Emissions are temporary by construction.", "Check whether real revenue is growing to replace them in time."], sub="A protocol that never answers this question is worth watching closely.")

# ---------------------------------------------------------------- step 3: dependencies
sc("title", "Step three: dependencies.", chapter="Step 3: Dependencies", eyebrow="Step 3 of 6", num="3", title="Everything the protocol actually relies on",
   sub="This is Module 5's dependency map, applied directly.")
sc("bullets", "This step is exactly Module five's own dependency map, run against one specific protocol. Oracles: what feeds it prices, and how manipulable is that feed. Bridges: does it hold or move assets across chains, and under what trust model. Admin keys: who can upgrade it, and how fast. Stablecoins: which ones does it accept as collateral, and are they genuinely backed. And other protocols: what does it build on top of, that could itself fail.",
   chapter="Step 3: Dependencies", title="The five links, applied here", check=False,
   items=["Oracles — what feeds it prices, and how manipulable", "Bridges — trust model for any cross-chain assets", "Admin keys — who can upgrade it, and how fast", "Stablecoins accepted as collateral — genuinely backed?", "Other protocols it builds on — could their failure become yours"])
sc("statement", "If Module five's dependency map felt abstract at the time, this is exactly where it stops being abstract. Every one of those five links is a real, checkable fact about one specific protocol in front of you right now, not a general concept to remember.",
   chapter="Step 3: Dependencies", kicker="Why this step exists", lines=["Every link is a checkable fact about this one protocol.", "Not a general concept. A specific answer, right now."], sub="Module 5 built the map. This step is where you actually use it.")

# ---------------------------------------------------------------- step 4: solvency
sc("title", "Step four: solvency.", chapter="Step 4: Solvency", eyebrow="Step 4 of 6", num="4", title="Can it actually cover what it owes",
   sub="Collateral quality, liquidation design, and bad-debt paths.")
sc("steps", "Solvency means checking three things about how a protocol handles the money it currently holds. Collateral quality: is what's backing deposits genuinely liquid and independently priced, or thin and easily manipulated. Liquidation design: does it actually liquidate bad positions fast enough, before losses spread. And bad-debt paths: if a liquidation genuinely fails, who absorbs that loss — a reserve fund, or every depositor at once.",
   chapter="Step 4: Solvency", title="Three checks for solvency",
   steps=["Collateral quality — liquid and independently priced, or thin", "Liquidation design — fast enough before losses spread", "Bad-debt paths — a reserve fund, or every depositor at once"], result="A protocol with weak collateral can look fine right up until it isn't")
sc("statement", "Solvency problems are quiet almost right up until they aren't. A protocol can carry real, satisfied users for months on thin collateral and a slow liquidation design, and the failure, when it comes, tends to arrive all at once rather than gradually.",
   chapter="Step 4: Solvency", kicker="Why this step gets skipped", lines=["Solvency problems stay quiet almost until they aren't.", "The failure tends to arrive all at once, not gradually."], sub="That's exactly why this step can't wait for a visible warning sign.")

# ---------------------------------------------------------------- step 5: evidence
sc("title", "Step five: evidence.", chapter="Step 5: Evidence", eyebrow="Step 5 of 6", num="5", title="What real, verifiable data actually says",
   sub="Explorers, audits, governance, and independent data.")
img(D + "audit-coverage.png", "Evidence means checking real sources, not vibes",
    "This step means checking four kinds of real, verifiable sources. Explorers: the actual on-chain contracts and transaction history, not a claim about them. Audits: who reviewed the code, when, and whether every finding was actually fixed. Governance: the real proposal and vote history, not just the current parameters. And independent data: numbers from a source the protocol itself doesn't control.",
    chapter="Step 5: Evidence")
sc("statement", "Here's the actual standard this step holds you to: a claim only counts once you've genuinely traced it back to one of those four sources yourself. A protocol's own blog post, describing its own audit, is not the audit. Go find the actual report.",
   chapter="Step 5: Evidence", kicker="The evidence standard", lines=["A claim counts once you've traced it to the real source yourself.", "A protocol's own blog post describing its audit is not the audit."], sub="Go find the actual report. Every time.")

# ---------------------------------------------------------------- step 6: exit
sc("title", "Step six: exit.", chapter="Step 6: Exit", eyebrow="Step 6 of 6", num="6", title="Exactly how you'd get out",
   sub="Gas, slippage, and approvals to revoke.")
sc("steps", "Exit means writing down the actual unwind, before you ever need it, not while you're already trying to leave under pressure. The exact steps to withdraw or close the position. The realistic gas cost of doing it, at a normal network load. The likely slippage if you had to exit the full size at once. And every token approval you'd need to revoke afterward.",
   chapter="Step 6: Exit", title="What exit actually covers",
   steps=["The exact steps to withdraw or close the position", "Realistic gas cost, at normal network load", "Likely slippage exiting the full size at once", "Every token approval to revoke afterward"], result="Written down now, before you're already trying to leave")
sc("statement", "This is exactly the step this module's earlier lessons warned about skipping. An exit you've never actually mapped out is an exit you'll be improvising for the first time during whatever event made you want to leave in the first place, which is the worst possible moment to be improvising.",
   chapter="Step 6: Exit", kicker="Why exit comes last, but never gets skipped", lines=["An unmapped exit means improvising during the worst moment.", "Map it now, while nothing is actually forcing you to."], sub="Six steps in, and this is the one that's easiest to skip. Don't.")

# ---------------------------------------------------------------- logging discipline
sc("title", "Logging it: evidenced, not assumed.", chapter="Logging discipline", eyebrow="The tracker rule", num="1", title="One rule for every single box",
   sub="Tick a box only when the step is genuinely evidenced.")
sc("compare", "Here's the one rule that makes this loop actually worth running: log every step in your own due-diligence tracker, and tick a box only once it's genuinely evidenced, never merely assumed. An assumed box says you expect it's probably fine. An evidenced box says you actually checked, and here's the source.",
   chapter="Logging discipline",
   left={"label": "Assumed", "tone": "warn", "items": ["\"Probably fine\", based on reputation", "No source you could point to"]},
   right={"label": "Evidenced", "tone": "good", "items": ["You actually checked, and can name the source", "The box means something when it's ticked"]})
sc("statement", "This single rule is what separates real due diligence from simply feeling reassured. Six ticked boxes built on assumptions is a false sense of safety with a checklist attached. Six ticked boxes built on evidence is an actual verdict you can stand behind.",
   chapter="Logging discipline", kicker="Why the rule matters", lines=["Six assumed boxes: a false sense of safety with a checklist attached.", "Six evidenced boxes: an actual verdict you can stand behind."], sub="Same-looking tracker. Completely different amount of protection.")

# ---------------------------------------------------------------- worked example
sc("title", "The worked example, in full.", chapter="Worked example", eyebrow="Worked example", num="1", title="Protocol Y — lending, Arbitrum",
   sub="Every one of the six steps, mapped to one real verdict.")
sc("flow", "Here's how all six steps actually show up in one real verdict. Mechanism: Protocol Y, a lending market, on Arbitrum. Cash flow: fees are real, with two million dollars a year in genuine borrow demand. Dependencies: one collateral asset uses a thin-market oracle, a genuine risk. Governance found in dependencies: upgrades carry a twenty-four hour timelock, some real protection, but not a large one. Evidence: all four of that gathered and traced, not assumed. Exit: a stablecoins-only position keeps the exit simple.",
   chapter="Worked example", title="Six steps, one verdict",
   nodes=[{"label": "1. Mechanism", "sub": "Lending market, Arbitrum", "icon": "cog"}, {"label": "2. Cash flow", "sub": "Real: $2M/yr borrow demand", "icon": "coins"},
          {"label": "3. Dependencies", "sub": "One collateral: thin-market oracle", "icon": "link"}, {"label": "4. Solvency", "sub": "24-hour timelock on upgrades", "icon": "vault"},
          {"label": "5. Evidence", "sub": "Traced, not assumed", "icon": "eye"}, {"label": "6. Exit", "sub": "Stablecoins keep it simple", "icon": "exit"}])
sc("statement", "Read that whole verdict as one sentence, the way it actually gets written in the tracker. Protocol Y, lending, Arbitrum. Risk: medium. Fees are real, borrow demand two million dollars a year, but one collateral uses a thin-market oracle, and upgrades carry only a twenty-four hour timelock.",
   chapter="Worked example", kicker="The verdict, as written", lines=["\"Protocol Y (lending, Arbitrum). Risk: Medium.\"", "\"Fees are real ($2M/yr borrow demand), but one collateral uses a thin-market oracle, and upgrades have a 24h timelock.\""], sub="Six steps of real research, compressed into two honest sentences.")

# ---------------------------------------------------------------- worst risk, not average
sc("title", "Why the rating is the worst risk, not the average.", chapter="Worst risk, not average", eyebrow="A common mistake", num="1", title="One weak link outweighs five strong ones",
   sub="This is the single most common due-diligence mistake.")
sc("stats", "Here's the mistake, made concrete with a purely illustrative example. Say four of your five checks come back genuinely strong: real cash flow, solid governance, a clean audit, a mapped exit. Averaging those five checks might suggest the protocol is roughly eighty percent healthy. But the fifth check found a thin-market oracle, a genuine single point of failure. The real rating is medium-to-high risk, not eighty percent healthy, because that one failure point is enough to lose the position, regardless of how strong the other four are.",
   chapter="Worst risk, not average", title="4 strong checks, 1 weak one (illustrative)",
   stats=[["4 of 5", "Checks come back strong"], ["1 of 5", "Finds a real single point of failure"], ["Rating used", "The weak one — not the 80% average"]])
sc("statement", "Here's why that's the actual correct way to rate it, not just a conservative habit. A chain is exactly as strong as its weakest link, and a protocol's risk works the same way: it fails at its single worst dependency, not at some blended average of all its dependencies put together.",
   chapter="Worst risk, not average", kicker="Why worst risk, not average, is correct", lines=["A chain is exactly as strong as its weakest link.", "A protocol fails at its worst dependency, not a blended average."], sub="This is why Protocol Y above is rated Medium, driven entirely by the oracle.")

# ---------------------------------------------------------------- the verdict format
sc("title", "The verdict format, one more time.", chapter="The verdict format", eyebrow="Every verdict, every time", num="1", title="Size. Conditions. Exit.",
   sub="This is the actual finish line for every protocol you research.")
sc("steps", "Break Protocol Y's own verdict down into its three real components, since every single verdict this module asks for follows this exact same shape. Size: supply stablecoins only, meaning the riskiest collateral is avoided entirely. Conditions: cap it at ten percent of the whole DeFi book, a specific, decided-in-advance limit. And exit: alert on any queued upgrade, a concrete trigger, decided now, not improvised later.",
   chapter="The verdict format", title="Protocol Y's verdict, broken into three parts",
   steps=["Size / conditions: supply stablecoins only, capped at 10% of the DeFi book", "Exit trigger: alert on any queued upgrade", "Written down now — not improvised during a crisis"], result="Size, conditions, and exit. Every verdict, every time.")
sc("quiz", "Quick check. In the worked example, what specific exit trigger did the verdict actually set? [[pause 4]] The answer: alert on any queued upgrade.",
   chapter="The verdict format", n=1, of=3, q="What exit trigger did Protocol Y's verdict set?",
   a="Alert on any queued upgrade.")

# ---------------------------------------------------------------- checklist and quiz
sc("title", "Before you move on.", chapter="Checklist", eyebrow="Checklist", num="1", title="Three things to confirm",
   sub="From this lesson's own checklist.")
sc("bullets", "Confirm three things before calling this lesson done. All six steps written, with real sources for each one, not assumptions. The risk rating set to the single worst material risk found, never an average across all six steps. And the verdict itself states a size, real conditions, and an actual exit, every time.",
   chapter="Checklist", title="This lesson's checklist", check=True,
   items=["All six steps written, with sources for each one", "Risk rating = the worst material risk found, not an average", "Verdict states size, conditions, and an exit"])
sc("quiz", "Quick check. Why is the rating set to the worst risk found, rather than an average across all six steps? [[pause 4]] The answer: one real failure point is enough to lose the position, no matter how strong the other five checks are.",
   chapter="Checklist", n=2, of=3, q="Why is the rating the worst risk, not the average?",
   a="One failure point is enough to lose the position.")
sc("quiz", "One more. Which of the six steps exists specifically to prevent getting stuck in a position you can't leave? [[pause 4]] The answer: step six, exit.",
   chapter="Checklist", n=3, of=3, q="Which step prevents getting stuck?",
   a="Step 6: Exit.")

# ---------------------------------------------------------------- recap
sc("bullets", "Let's recap this entire lesson. The six-step loop, run in real depth: mechanism, cash flow, dependencies, solvency, evidence, exit. Log every step in your tracker, and tick a box only once it's genuinely evidenced, never merely assumed. Rate the risk at the single worst material finding, never an average. And every verdict ends the same way: a size, real conditions, and an actual exit, written down before you need it.",
   chapter="Recap", title="Recap", check=False,
   items=["Six steps, in real depth: mechanism, cash flow, dependencies, solvency, evidence, exit", "Tick a tracker box only when it's genuinely evidenced, never assumed",
          "Rate the worst material risk found — never an average", "Every verdict: size, conditions, and an exit, written down in advance"])
sc("cta", "Pick one real protocol, and write the full six-step verdict today, size, conditions, and exit included. Next up, Lesson six point two: tokenomics — supply, unlocks, and F.D.V.",
   "Pick one real protocol, and write the full six-step verdict today, size, conditions, and exit included. Next up, Lesson 6.2: tokenomics — supply, unlocks, and FDV.",
   chapter="Recap", button="Next: Lesson 6.2", sub="Tokenomics: supply, unlocks, FDV, value capture")

spec = {"id": "lesson-06-1", "title": "Lesson 6.1: Protocol due diligence", "size": [1920, 1080], "group": "lessons", "maxMinutes": 25,
        "tag": "Lesson 6.1 · Module 6", "gold": True, "music": True, "musicLevel": 0.14, "seed": 88,
        "use": "Lesson 6.1 page in the Whop course. Hand-written gold-standard script running the six-step research loop in depth, one step at a time, applied to the source's own Protocol Y worked-example verdict.",
        "thumbnail": {"title": "Protocol due diligence", "subtitle": "Lesson 6.1"}, "scenes": S}
out = ROOT / "video-scripts" / "gold" / "lesson-06-1.json"
out.write_text(json.dumps(spec, indent=1, ensure_ascii=False))
words = sum(len(s["vo"].replace("[[pause 4]]", "").split()) for s in S)
print(f"{len(S)} scenes, {words} words, est {(words / 171 * 60 + len(S) * 1.3 + 4 * 3) / 60:.1f} min")
