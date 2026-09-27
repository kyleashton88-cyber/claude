#!/usr/bin/env python3
"""Gold-standard script for Lesson 6.2, Tokenomics: supply, unlocks, FDV,
value capture (ch. 25). Target 10-13 minutes per the "a bit longer" note
active for lessons from here on. Walks circulating vs. max supply,
market cap vs. FDV, unlocks/vesting, emissions, and value capture as
dedicated scenes, then runs the source's own worked example (price $2,
circulating 100M, max 1B -> $200M market cap, $2B FDV, a 50M unlock
raising circulating supply 50%) as a chart and a flow, closing on
reading a real supply schedule end to end. Written in one pass at full
target length, reusing the module's token-supply-unlocks.png diagram.

Writes video-scripts/gold/lesson-06-2.json (the generator skips lessons
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
sc("title", "Lesson six point two. Tokenomics: supply, unlocks, F.D.V., and value capture. Today you'll learn to read a token's own supply schedule, and judge whether protocol success genuinely reaches the token itself.",
   "Lesson 6.2. Tokenomics: supply, unlocks, FDV, and value capture. Today you'll learn to read a token's own supply schedule, and judge whether protocol success genuinely reaches the token itself.",
   chapter="Intro", eyebrow="Lesson 6.2 · ch. 25", num="6.2", title="Tokenomics", sub="Supply, unlocks, FDV, and value capture.")
sc("statement", "Here's the objective, in one sentence. Read a token's supply schedule, and judge whether the protocol's own success actually reaches the token you'd be holding, rather than simply assuming it does because the protocol itself is doing well.",
   chapter="Intro", kicker="Objective", lines=["Read a token's own supply schedule.", "Judge whether protocol success actually reaches the token."], sub="A protocol can thrive while its token quietly doesn't.")
img(D + "token-supply-unlocks.png", "The four pieces this lesson covers",
    "Here's the full picture this lesson builds: circulating and max supply, market cap and F.D.V., the unlock and emissions schedule that grows supply over time, and value capture, whether protocol revenue actually reaches you.",
    chapter="Intro")
sc("flow", "Here's all four pieces, named individually, since each one answers a genuinely different question about the same token. Supply terms: how many tokens exist now, versus ever. Valuation terms: what the market actually says it's worth, at each of those two counts. Supply growth: how fast new tokens actually enter circulation. And value capture: whether the protocol's own success actually reaches you.",
   chapter="Intro", title="The four pieces, named individually",
   nodes=[{"label": "Supply terms", "sub": "Circulating vs. max supply", "icon": "layers"}, {"label": "Valuation terms", "sub": "Market cap vs. FDV", "icon": "scale"},
          {"label": "Supply growth", "sub": "Unlocks and emissions", "icon": "clock"}, {"label": "Value capture", "sub": "Does success reach you", "icon": "vault"}])

# ---------------------------------------------------------------- supply terms
sc("title", "Circulating supply vs. max supply.", chapter="Supply terms", eyebrow="Supply terms", num="1", title="How many tokens exist now, versus ever",
   sub="Two very different counts. Both worth knowing.")
sc("statement", "Circulating supply is the count that actually matters for trading right now: every token that's genuinely tradeable today, out in the open market. Max supply, sometimes called total supply, is every token that could ever genuinely exist, once every future unlock and emission has actually happened.",
   chapter="Supply terms", kicker="Two very different counts", lines=["Circulating supply: tokens genuinely tradeable right now.", "Max supply: every token that could ever exist, once fully released."], sub="A token can have a small circulating supply and a huge max supply.")
sc("statement", "Worth being direct about why that gap actually matters. If circulating supply is small relative to max supply, most of the token's eventual total hasn't reached the market yet, and it's going to, on some schedule you can actually go find and read.",
   chapter="Supply terms", kicker="Why the gap matters", lines=["A small circulating supply relative to max means most tokens are still coming.", "On a schedule you can actually go find and read."], sub="That future supply doesn't stay hidden. It has a release date.")

# ---------------------------------------------------------------- market cap vs FDV
sc("title", "Market cap vs. F.D.V.", chapter="Market cap vs FDV", eyebrow="Valuation terms", num="1", title="What the market says it's worth, at each count",
   sub="Fully diluted valuation: price × every token that will ever exist.")
sc("steps", "Two formulas, both built from the same token price, each answering a different question. Market cap: price, multiplied by circulating supply, the value of what's genuinely tradeable today. F.D.V., fully diluted valuation: price, multiplied by max supply, the value of everything that will ever exist, once fully released.",
   chapter="Market cap vs FDV", title="Two formulas, one price",
   steps=["Market cap = price × circulating supply", "FDV = price × max supply", "Same price. Two very different totals."], result="A large gap between the two is worth checking, not ignoring")
sc("stats", "Here's the source's own worked example. A token priced at two dollars, with a circulating supply of one hundred million: that's a market cap of two hundred million dollars. The same two-dollar price, applied to a max supply of one billion, gives an F.D.V. of two billion dollars, ten times larger than the market cap you'd actually be trading against today.",
   chapter="Market cap vs FDV", title="Worked example",
   stats=[["$200M", "Market cap (price $2 × 100M circulating)"], ["$2B", "FDV (price $2 × 1B max supply)"], ["10×", "The gap between them"]])
sc("statement", "Here's what that ten-times gap actually tells you: nine out of every ten tokens that will ever exist haven't reached the market yet. A low market cap sitting underneath a huge F.D.V. isn't automatically disqualifying, but it's a real, specific warning worth investigating, not a detail to skip past.",
   chapter="Market cap vs FDV", kicker="What the gap actually means", lines=["Nine of every ten eventual tokens haven't reached the market yet.", "Not automatically disqualifying. A real, specific warning worth investigating."], sub="A low market cap under a huge FDV is the pattern to notice.")
sc("quiz", "Quick check. A token trades at five dollars, with a circulating supply of twenty million, and a max supply of one hundred million. What's its F.D.V.? [[pause 4]] The answer: five hundred million dollars — five dollars, multiplied by the max supply of one hundred million.",
   chapter="Market cap vs FDV", n=1, of=3, q="Price $5, circulating 20M, max 100M. FDV?",
   a="$500M — $5 × 100M max supply.")

# ---------------------------------------------------------------- unlocks and vesting
sc("title", "Unlocks and vesting.", chapter="Unlocks and vesting", eyebrow="Supply growth, part 1", num="1", title="New supply released on a schedule",
   sub="Team and investor tokens, arriving on a real, checkable timeline.")
sc("statement", "Unlocks, also called vesting, are team and investor tokens released into circulation on a fixed schedule, agreed to well before launch. Every unlocked token becomes new supply that its recipient is genuinely free to sell, whether or not they actually choose to.",
   chapter="Unlocks and vesting", kicker="What an unlock actually is", lines=["Team and investor tokens, released on a fixed, pre-agreed schedule.", "Every unlocked token becomes new supply its recipient could sell."], sub="A real event, on a real date, worth checking before it happens.")
sc("chart", "Here's the source's own unlock example, made visual. Circulating supply starts at one hundred million tokens. One month later, a fifty-million-token unlock lands, and circulating supply jumps to one hundred fifty million: a fifty percent increase, in a single month.",
   chapter="Unlocks and vesting", title="A 50M unlock, one month later",
   kind="bars", bars=[{"label": "This month", "value": 100, "tone": "good"}, {"label": "Next month, after unlock", "value": 150, "tone": "warn"}],
   yticks=["0M", "50M", "100M", "150M"], ymax=150, marks=[{"i": 1, "text": "+50% in one month", "tone": "warn"}])
sc("statement", "Here's why that fifty-percent jump matters so much. Unless real demand for the token actually grows to match it, that much new sellable supply, arriving all at once, is genuine, heavy selling pressure on the price. This is exactly the kind of event worth knowing about in advance, not discovering after the price has already moved.",
   chapter="Unlocks and vesting", kicker="Why a large unlock matters", lines=["Unless demand grows to match it, that's real, heavy selling pressure.", "Worth knowing in advance, not discovering after the price has moved."], sub="The unlock date is public. Go find it before it happens.")
sc("compare", "Here's the actual fork in the road, once that fifty-million-token unlock genuinely lands. If real demand has grown enough to absorb it, price holds, and the extra supply simply gets absorbed by new buyers. If demand hasn't grown to match, recipients selling into a thin market can genuinely push price down, sometimes sharply, in a short window.",
   chapter="Unlocks and vesting",
   left={"label": "Demand grows to match", "tone": "good", "items": ["New supply gets absorbed by real buyers", "Price holds through the unlock"]},
   right={"label": "Demand doesn't grow", "tone": "warn", "items": ["Recipients selling into a thin market", "Price can drop sharply, in a short window"]})
sc("statement", "Worth knowing the actual shape most real vesting schedules take, since it changes how urgently a given unlock matters. Many token launches use a one-year cliff: genuinely zero tokens unlock for the first year, followed by linear monthly unlocks spread over the two or three years after that. A schedule still inside its cliff period carries a very different urgency than one already deep into linear unlocks.",
   chapter="Unlocks and vesting", kicker="What a real vesting schedule looks like", lines=["Many launches use a one-year cliff: zero unlocks for twelve months.", "Followed by linear monthly unlocks over the two or three years after that."], sub="Still inside the cliff? Different urgency than deep into linear unlocks.")

# ---------------------------------------------------------------- emissions
sc("title", "Emissions.", chapter="Emissions", eyebrow="Supply growth, part 2", num="2", title="Ongoing new tokens, handed out as rewards",
   sub="Different from an unlock: emissions are newly minted, not merely released.")
sc("statement", "Emissions are ongoing, newly minted tokens, handed out as rewards, most often to liquidity providers or stakers. Unlike an unlock, which releases tokens that already existed, an emission genuinely creates brand-new supply, diluting every existing holder a little, every single time it happens.",
   chapter="Emissions", kicker="How emissions differ from unlocks", lines=["An unlock releases tokens that already existed.", "An emission mints brand-new ones — diluting every holder, every time."], sub="This is exactly the same emissions this module's Lesson 6.1 warned about in cash-flow terms.")
sc("statement", "Worth connecting this directly back to last lesson's cash-flow step. If a protocol's own real revenue isn't growing fast enough to offset its ongoing emissions, the token supply keeps expanding faster than genuine demand for it, and price pressure is the structural result, not an accident.",
   chapter="Emissions", kicker="The connection to cash flow", lines=["If real revenue doesn't grow to offset emissions, supply outgrows demand.", "Price pressure becomes the structural result, not an accident."], sub="Step 2 of the research loop and this lesson are checking the same thing, from two angles.")

# ---------------------------------------------------------------- value capture
sc("title", "Value capture.", chapter="Value capture", eyebrow="The question that ties it together", num="1", title="Does protocol revenue actually reach the token",
   sub="And how, specifically, is that enforced.")
sc("compare", "Here's the real difference value capture actually makes, side by side. With genuine value capture, real, specific mechanisms send protocol revenue to holders: a direct fee share, or enforced token buybacks, written into the contracts themselves. Without it, all of that same revenue stays entirely with the team or the D.A.O. treasury, and holders benefit only indirectly, if at all.",
   chapter="Value capture",
   left={"label": "Has value capture", "tone": "good", "items": ["Fee share, or enforced buybacks", "Written into the contracts, not a promise"]},
   right={"label": "No value capture", "tone": "warn", "items": ["Revenue stays with the team or DAO treasury", "Holders benefit only indirectly, if at all"]})
sc("statement", "Here's the actual test worth applying, every single time. Don't just ask whether a protocol is profitable; ask specifically how that profit reaches you as a token holder, and whether that mechanism is genuinely enforced on-chain, or merely a stated intention the team could change later.",
   chapter="Value capture", kicker="The real test to apply", lines=["Ask specifically how profit reaches you, not just whether it exists.", "Enforced on-chain, or merely a stated intention that could change."], sub="\"None\" is a completely valid, honest answer here — as long as you write it down.")
sc("compare", "Here's a specific, real pattern worth being able to spot on sight: a low circulating market cap sitting under a genuinely huge F.D.V. On its own, that's not automatically disqualifying. But combined with heavy near-term unlocks and no real value-capture mechanism, it's a pattern that's shown up in plenty of real token launches, worth naming precisely rather than reacting to only vaguely.",
   chapter="Value capture",
   left={"label": "The red-flag combination", "tone": "warn", "items": ["Low market cap under a huge FDV", "Heavy near-term unlocks, no value capture"]},
   right={"label": "What it actually signals", "tone": "warn", "items": ["Most of the eventual supply is still coming", "And success wouldn't be enforced to reach you anyway"]})
sc("quiz", "Quick check. Why do unlocks matter for a token's price? [[pause 4]] The answer: they add real, sellable supply that recipients may choose to sell, whether or not they actually do.",
   chapter="Value capture", n=2, of=3, q="Why do unlocks matter?",
   a="They add supply that recipients may sell.")

# ---------------------------------------------------------------- reading it in practice
sc("title", "Reading a real supply schedule.", chapter="Reading it in practice", eyebrow="Putting it together", num="1", title="Five things to check, in order",
   sub="On any token, before you hold it.")
sc("steps", "Here's the actual sequence, run on any real token you're considering. Look up circulating and max supply. Calculate both market cap and F.D.V., and compare the gap between them. Find the next twelve months of scheduled unlocks. Check the current emissions rate, and whether real revenue is growing to offset it. And identify the value-capture mechanism, or honestly write down that there isn't one.",
   chapter="Reading it in practice", title="Five checks, run in order",
   steps=["Look up circulating and max supply", "Calculate market cap and FDV, compare the gap", "Find the next 12 months of scheduled unlocks", "Check the emissions rate against real revenue growth", "Identify the value-capture mechanism, or write \"none\""], result="Five checks. Every real token, every time.")
sc("statement", "This is exactly the same discipline last lesson's evidenced-not-assumed rule asked for, applied here to a token's own numbers instead of a protocol's dependencies. Every one of these five checks has a real, specific, findable answer. None of them are a matter of opinion.",
   chapter="Reading it in practice", kicker="The same discipline, applied to numbers", lines=["Every one of these five checks has a real, findable answer.", "None of them are a matter of opinion."], sub="If you can't find the answer, that's itself worth writing down.")
sc("bullets", "Three more questions worth asking directly, if a schedule genuinely isn't public. Is the full unlock schedule actually published anywhere, or only described in general terms. Has that schedule ever genuinely been changed after launch, and if so, in which direction. And is there any lockup-extension option that team or investor tokens could actually use to delay their own unlocks.",
   chapter="Reading it in practice", title="If the schedule isn't public", check=False,
   items=["Is the full schedule actually published, or only described vaguely", "Has it genuinely been changed after launch, and in which direction", "Any lockup-extension option team or investor tokens could use"])

# ---------------------------------------------------------------- checklist and quiz
sc("title", "Before you move on.", chapter="Checklist", eyebrow="Checklist", num="1", title="Three things to confirm",
   sub="From this lesson's own checklist.")
sc("bullets", "Confirm three things before calling this lesson done. Market cap has actually been compared against F.D.V., not just one of the two looked up in isolation. The next twelve months of unlocks have genuinely been listed out. And a value-capture mechanism has been identified, or honestly marked as none, rather than left unanswered.",
   chapter="Checklist", title="This lesson's checklist", check=True,
   items=["Market cap vs. FDV actually compared, not just one looked up", "Next 12 months of unlocks genuinely listed", "Value-capture mechanism identified — or honestly marked \"none\""])
sc("quiz", "One more. What is value capture, in one sentence? [[pause 4]] The answer: an enforceable way that a protocol's own success actually benefits the token itself.",
   chapter="Checklist", n=3, of=3, q="What is value capture?",
   a="An enforceable way protocol success benefits the token.")

# ---------------------------------------------------------------- recap
sc("bullets", "Let's recap this entire lesson. Circulating supply is what trades today; max supply is everything that will ever exist. Market cap and F.D.V. use that same price against those two very different counts, and a large gap between them is a real warning. Unlocks and emissions both grow supply, on a schedule you can actually go check. And value capture asks whether the protocol's own success genuinely reaches you, enforced, not merely promised.",
   chapter="Recap", title="Recap", check=False,
   items=["Circulating supply trades today; max supply is everything that will ever exist", "Market cap vs. FDV: same price, two counts — a large gap is a real warning",
          "Unlocks and emissions both grow supply, on a schedule you can check", "Value capture: does success genuinely reach you, enforced, not merely promised"])
sc("cta", "Pick one real token, and run all five checks on its own supply schedule today. Next up, Lesson six point three: governance and D.A.O.s.",
   "Pick one real token, and run all five checks on its own supply schedule today. Next up, Lesson 6.3: governance and DAOs.",
   chapter="Recap", button="Next: Lesson 6.3", sub="Governance & DAOs")

spec = {"id": "lesson-06-2", "title": "Lesson 6.2: Tokenomics — supply, unlocks, FDV, value capture", "size": [1920, 1080], "group": "lessons", "maxMinutes": 25,
        "tag": "Lesson 6.2 · Module 6", "gold": True, "music": True, "musicLevel": 0.14, "seed": 89,
        "use": "Lesson 6.2 page in the Whop course. Hand-written gold-standard script covering circulating/max supply, market cap vs FDV, unlocks/vesting, emissions, and value capture, using the source's own $2/100M/1B worked example as a chart and stats scene.",
        "thumbnail": {"title": "Tokenomics: supply, unlocks, FDV", "subtitle": "Lesson 6.2"}, "scenes": S}
out = ROOT / "video-scripts" / "gold" / "lesson-06-2.json"
out.write_text(json.dumps(spec, indent=1, ensure_ascii=False))
words = sum(len(s["vo"].replace("[[pause 4]]", "").split()) for s in S)
print(f"{len(S)} scenes, {words} words, est {(words / 171 * 60 + len(S) * 1.3 + 4 * 3) / 60:.1f} min")
