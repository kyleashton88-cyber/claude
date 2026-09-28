#!/usr/bin/env python3
"""Gold-standard script for Lesson 1.5, Stablecoins and how they break (about
12-15 minutes). Replaces the pre-gold-pass-2 script from commit bf85b68,
which predates the chart-variant/ticker/chart3d-line visual layer added in
1e2d691. Teaches the four stablecoin designs as a glossary ticker, a flow3d
recreation of the module's own stablecoin-designs.png (extended to all four
types), peg mechanics with a chart3d anchor on the source's own arbitrage
maths, two real historical case studies (UST May 2022, USDC March 2023),
and the source's own $0.97 worked example.

Writes video-scripts/gold/lesson-01-5.json (the generator skips lessons with
a gold script). Every illustrative number is labelled as an example on
screen and in the narration; real historical figures are stated as
approximate and clearly dated. Spoken text (vo) spells numbers and
abbreviations for the voice; cap is the written caption, same sentences."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
S = []


def sc(type_, vo, cap=None, **k):
    d = {"type": type_, **k, "vo": vo}
    if cap:
        d["cap"] = cap
    S.append(d)


# ---------------------------------------------------------------- why it matters
sc("title", "Lesson one point five. Stablecoins and how they break. By the end, you'll be able to classify a stablecoin by its design, and name exactly what could break its peg.",
   chapter="Why it matters", eyebrow="Lesson 1.5", num="1.5", title="Stablecoins and how they break", sub="“Stable” describes an intention, not a guarantee.")
sc("statement", "Here's the assumption this lesson challenges. 'Stablecoin' sounds like a single, simple thing: a dollar, on-chain. It isn't. Four genuinely different designs all get called stablecoins, and they can fail in four genuinely different ways. Which one you're holding matters enormously.",
   chapter="Why it matters", kicker="Why it matters", lines=["“Stablecoin” sounds like one simple thing.", "Four different designs. Four different ways to break."], sub="Which one you're holding matters enormously.")
sc("pillars", "Here's the plan. First, the four designs, and what backs each one. Second, peg mechanics, what actually keeps the price at one dollar. Third, two real historical case studies, one that recovered and one that didn't. And finally, a real worked example with real arbitrage maths.",
   chapter="Why it matters", title="What this lesson covers",
   items=[{"icon": "layers", "title": "Four designs", "text": "What actually backs each one"}, {"icon": "target", "title": "Peg mechanics", "text": "What keeps the price at $1"},
          {"icon": "book", "title": "Two real case studies", "text": "One recovered. One didn't."}, {"icon": "coins", "title": "A worked example", "text": "Real arbitrage maths"}])

# ---------------------------------------------------------------- four designs
sc("title", "Four designs.", chapter="Four designs", eyebrow="Four designs", num="4", title="Same label. Four different machines.",
   sub="Backed very differently. Breaks very differently.")
sc("flow3d", "Here are all four, side by side. Fiat-backed: cash and treasuries held by an issuer; it breaks if reserves are frozen or simply missing. Crypto-backed: over-collateralised with on-chain crypto; it breaks if that collateral crashes faster than liquidations can keep up. Synthetic, or hedged: built from derivative positions, like spot held against a short perpetual; it breaks if funding turns negative or the venue itself fails. And algorithmic: held up mostly by incentives and a sister token; it breaks when confidence goes, and the mechanism amplifies the fall instead of stopping it.",
   chapter="Four designs", title="Four stablecoin designs",
   nodes=[{"label": "Fiat-backed", "sub": "Cash & treasuries. Breaks: reserves frozen", "icon": "bank"}, {"label": "Crypto-backed", "sub": "Over-collateralised. Breaks: collateral crash", "icon": "layers"},
          {"label": "Synthetic / hedged", "sub": "Spot + short perp. Breaks: funding, venue risk", "icon": "swap"}, {"label": "Algorithmic", "sub": "Incentives & a sister token. Breaks: confidence", "icon": "alert"}])
sc("ticker", "In one line each. Fiat-backed: cash and treasuries, at an issuer you have to trust. Crypto-backed: over-collateralised, exposed to a collateral crash. Synthetic or hedged: a derivative position, exposed to funding and venue risk. And algorithmic: incentives and a sister token, exposed to confidence itself.",
   chapter="Four designs", title="Backing, and the main risk",
   items=[{"label": "Fiat-backed", "value": "Issuer & custodian risk"}, {"label": "Crypto-backed", "value": "Collateral crash, liquidations"}, {"label": "Synthetic / hedged", "value": "Funding, venue risk"},
          {"label": "Algorithmic", "value": "Confidence, reflexively"}])
sc("statement", "Take the synthetic design a little further, since it's the least obvious of the four. Hold spot E.T.H., and simultaneously short an E.T.H. perpetual future of equal size. If E.T.H. rises, the spot gains and the short loses, and the reverse if it falls; the two roughly cancel, leaving a dollar-stable position funded by whatever the perpetual's funding rate pays. When funding turns negative for long enough, that cost erodes the peg instead of supporting it.",
   "Take the synthetic design a little further, since it's the least obvious of the four. Hold spot ETH, and simultaneously short an ETH perpetual future of equal size. If ETH rises, the spot gains and the short loses, and the reverse if it falls; the two roughly cancel, leaving a dollar-stable position funded by whatever the perpetual's funding rate pays. When funding turns negative for long enough, that cost erodes the peg instead of supporting it.",
   chapter="Four designs", kicker="Synthetic, in a little more depth", lines=["Spot ETH, plus a short perp of equal size.", "Funded by the funding rate. Erodes it if negative."], sub="The least obvious of the four designs.")
sc("statement", "You've already used a fiat-backed design without necessarily naming it: the U.S.D.C. from your very first buy, back in Lesson zero point three. Everything in this lesson has been running underneath that same coin the whole time.",
   "You've already used a fiat-backed design without necessarily naming it: the USDC from your very first buy, back in Lesson 0.3. Everything in this lesson has been running underneath that same coin the whole time.",
   chapter="Four designs", kicker="You've already held one of these", lines=["USDC, from your very first buy.", "Lesson 0.3. Fiat-backed, the whole time."], sub="Everything here has been running underneath it.")
sc("compare", "Not every crypto-backed or synthetic design carries equal risk, either. A coin over-collateralised at three times its value can absorb a far larger crash than one collateralised at just one point two times. Module three covers exactly this ratio, and the liquidations it triggers, in full.",
   "Not every crypto-backed or synthetic design carries equal risk, either. A coin over-collateralised at three times its value can absorb a far larger crash than one collateralised at just one point two times. Module 3 covers exactly this ratio, and the liquidations it triggers, in full.",
   chapter="Four designs", title="The collateral ratio is the risk dial",
   left={"label": "3x over-collateralised", "tone": "good", "items": ["Absorbs a much larger crash", "More buffer before liquidation"]},
   right={"label": "1.2x over-collateralised", "tone": "bad", "items": ["Absorbs far less of a crash", "Liquidates much sooner"]})
sc("statement", "Notice the pattern in how each one fails. Fiat-backed fails through a person or institution. Crypto-backed fails through a market crash. Synthetic fails through a funding rate or a venue. Algorithmic fails through belief itself, which is exactly why it can go to zero fastest of all four.",
   chapter="Four designs", kicker="The pattern in how each fails", lines=["Fiat, crypto, synthetic: external failures.", "Algorithmic: belief itself. Which is why it's fastest."], sub="Same label, completely different failure points.")

# ---------------------------------------------------------------- peg mechanics
sc("title", "Peg mechanics.", chapter="Peg mechanics", eyebrow="Peg mechanics", num="1", title="What actually holds $1 in place",
   sub="Redemption access, and reserve quality. That's it.")
sc("statement", "Here's the whole mechanism, in one sentence. If a stablecoin trades at ninety-eight cents and can be redeemed for one dollar, arbitrageurs buy it cheap and redeem it at face value, pushing the price back up as they do. The peg is only ever as strong as two things: redemption access, and reserve quality.",
   chapter="Peg mechanics", kicker="The whole mechanism", lines=["Trades at $0.98, redeems for $1.00.", "Arbitrage buys it back up to $1."], sub="Only as strong as redemption access and reserve quality.")
sc("chart3d", "Here's that arbitrage, with the source's own real numbers. A coin trades at ninety-seven cents. Redemption pays one dollar, minus a naught point one percent fee, so ninety-nine point nine cents. Buy at ninety-seven, redeem for ninety-nine point nine. A minter earns roughly two point nine cents per coin, about two point nine percent, for doing the one thing that pushes the price back toward a dollar.",
   chapter="Peg mechanics", kind="bars", title="The arbitrage that repairs a $0.97 peg",
   sub="From the source's own worked example",
   bars=[{"label": "Buy on the open market", "text": "The discounted price", "value": 0.97, "show": "$0.97", "tone": "bad"}, {"label": "Redeem from the issuer", "text": "$1.00 minus a 0.1% fee", "value": 0.999, "show": "$0.999", "tone": "good"}])
sc("statement", "The same mechanism works in reverse, too. Say a fiat-backed coin trades above one dollar, at one dollar and two cents. An authorised minter can create new coins for one dollar and sell them at that premium, pushing the price back down. The peg is defended from both sides, by exactly the same profit motive.",
   chapter="Peg mechanics", kicker="Defended from both sides", lines=["Above $1: mint new coins, sell at the premium.", "The same profit motive, working in reverse."], sub="Defended from both sides, by the same incentive.")
sc("statement", "That naught point one percent redemption fee isn't arbitrary, either. It compensates the issuer for the operational cost of redeeming. It's small enough that arbitrage still works, but large enough to discourage redeeming and re-minting for no real reason at all.",
   chapter="Peg mechanics", kicker="Why the fee exists", lines=["Small enough that arbitrage still works.", "Large enough to discourage pointless redemptions."], sub="Not arbitrary. A deliberately small friction.")
sc("steps", "Here's how to actually check a stablecoin's backing yourself. Find the issuer's own attestation or reserve report, usually published regularly. Check who actually audits it, and how often, monthly is meaningfully better than never. Check exactly which assets back it, cash and short-term treasuries are very different from long-dated bonds or other crypto entirely. And check whether it's ever been tested by a real stress event, the way U.S.D.C. was in March twenty twenty-three.",
   "Here's how to actually check a stablecoin's backing yourself. Find the issuer's own attestation or reserve report, usually published regularly. Check who actually audits it, and how often, monthly is meaningfully better than never. Check exactly which assets back it, cash and short-term treasuries are very different from long-dated bonds or other crypto entirely. And check whether it's ever been tested by a real stress event, the way USDC was in March 2023.",
   chapter="Peg mechanics", title="Checking backing yourself",
   steps=["Find the issuer's own attestation or reserve report", "Check who audits it, and how often", "Check exactly which assets back it", "Check if it's ever survived a real stress event"],
   result="Four checks. Available for any stablecoin you hold.")
sc("statement", "But notice every word doing real work in that sentence. Only verified institutional minters can actually redeem, not you. And the whole mechanism assumes minters act, and that the reserves are genuinely real. Doubt either one, and the discount can simply grow instead of closing.",
   chapter="Peg mechanics", kicker="The mechanism has conditions", lines=["Only verified minters can redeem, not you.", "It assumes minters act, and reserves are real."], sub="Doubt either, and the discount can grow instead.")

# ---------------------------------------------------------------- two real case studies
sc("title", "Two real case studies.", chapter="Two real case studies", eyebrow="Two real case studies", num="2", title="One recovered. One didn't.",
   sub="Real events. Worth knowing by name.")
sc("flow", "First, the one that didn't recover. In May twenty twenty-two, TerraUSD, an algorithmic design, started slipping below its dollar peg. Confidence wavered, and holders began redeeming for its sister token instead. That sister token flooded the market, crashing its own price. And the falling price fed straight back into more panic selling, a genuine death spiral that took the whole design toward zero within days.",
   chapter="Two real case studies", title="May 2022: TerraUSD's collapse",
   nodes=[{"label": "TerraUSD slips below its peg", "sub": "Confidence starts to waver", "icon": "alert", "tone": "bad"}, {"label": "Holders redeem for the sister token", "sub": "Its supply floods the market", "icon": "swap", "tone": "bad"},
          {"label": "The sister token's price crashes", "sub": "Which feeds straight back into more panic", "icon": "coins", "tone": "bad"}, {"label": "A death spiral toward zero", "sub": "Within days, not months", "icon": "lock", "tone": "bad"}],
   edges=[{"from": "0", "to": "1", "tone": "bad"}, {"from": "1", "to": "2", "tone": "bad"}, {"from": "2", "to": "3", "tone": "bad"}])
sc("compare", "Now, the one that recovered. In March twenty twenty-three, U.S.D.C. briefly traded as low as around eighty-seven cents, after part of its reserves turned out to be exposed to the failed Silicon Valley Bank. But the reserves themselves were real. Once that was confirmed, and depositors were made whole, U.S.D.C. recovered fully to one dollar within days.",
   "Now, the one that recovered. In March 2023, USDC briefly traded as low as around $0.87, after part of its reserves turned out to be exposed to the failed Silicon Valley Bank. But the reserves themselves were real. Once that was confirmed, and depositors were made whole, USDC recovered fully to $1 within days.",
   chapter="Two real case studies", title="March 2023: USDC's brief depeg",
   left={"label": "TerraUSD, May 2022", "tone": "bad", "items": ["Algorithmic: backed by confidence", "Confidence broke. Never recovered"]},
   right={"label": "USDC, March 2023", "tone": "good", "items": ["Fiat-backed: real reserves", "Reserves confirmed. Recovered in days"]})
sc("statement", "The difference wasn't luck. One design's backing was, in the end, a belief. The other's backing was, in the end, real. That's the entire lesson of this section, in two real events instead of one abstract rule.",
   chapter="Two real case studies", kicker="Not luck. Backing.", lines=["One was backed by belief.", "One was backed by something real."], sub="Two real events, not one abstract rule.")

# ---------------------------------------------------------------- a worked example
sc("title", "A worked example.", chapter="A worked example", eyebrow="A worked example", num="97", title="A fiat-backed coin at $0.97",
   sub="Should you expect the peg to hold?")
sc("steps", "Here's the scenario. A fiat-backed coin trades at ninety-seven cents. Redemption pays one dollar, minus a naught point one percent fee, but only for verified institutional minters. A minter earns roughly two point nine percent per coin by buying and redeeming, so arbitrage should restore the peg. You, personally, can't redeem, so you're relying on minters actually acting, and on the reserves being real. If the market doubts those reserves, minters may simply not step in, and the discount can grow instead.",
   "Here's the scenario. A fiat-backed coin trades at $0.97. Redemption pays $1.00, minus a 0.1% fee, but only for verified institutional minters. A minter earns roughly 2.9% per coin by buying and redeeming, so arbitrage should restore the peg. You, personally, can't redeem, so you're relying on minters actually acting, and on the reserves being real. If the market doubts those reserves, minters may simply not step in, and the discount can grow instead.",
   chapter="A worked example", title="Should the peg hold, at $0.97?",
   steps=["Minters earn ~2.9% per coin, buying and redeeming", "You personally can't redeem; only verified minters can", "It relies on minters acting, and reserves being real", "If reserves are doubted, minters may not step in"],
   result="The peg should hold, on paper. “Should” is doing real work in that sentence.")
sc("statement", "Notice this is exactly the risk-first mindset from Lesson one point one, applied to a specific two-point-nine percent discount. Before assuming arbitrage saves you, name what has to be true for it to actually happen.",
   "Notice this is exactly the risk-first mindset from Lesson 1.1, applied to a specific 2.9% discount. Before assuming arbitrage saves you, name what has to be true for it to actually happen.",
   chapter="A worked example", kicker="The risk-first mindset, applied", lines=["Lesson 1.1's rule, applied to one discount.", "Name what has to be true, before trusting it."], sub="“Should” is not the same as “will”.")
sc("statement", "Notice why the phrase 'verified institutional minters' matters so much here. Most fiat-backed stablecoins restrict direct redemption to large, vetted counterparties, not everyday users like you. That's not a flaw, it's how the issuer manages compliance and operational load, but it does mean your own ability to close this gap is indirect, not direct.",
   chapter="A worked example", kicker="Why “institutional” matters", lines=["Direct redemption: large, vetted counterparties only.", "Your ability to close the gap is indirect."], sub="Not a flaw. But not something you control directly.")

# ---------------------------------------------------------------- checklist and quiz
sc("title", "Checklist and quiz.", chapter="Checklist and quiz", eyebrow="Checklist and quiz", num="4", title="Confirm you've got it",
   sub="Four boxes, three questions.")
sc("statement", "Everything Lesson one point four taught about verifying a token by its contract address applies doubly here. A fake token calling itself a well-known stablecoin's name is one of the single most common scams in this entire space.",
   "Everything Lesson 1.4 taught about verifying a token by its contract address applies doubly here. A fake token calling itself a well-known stablecoin's name is one of the single most common scams in this entire space.",
   chapter="Checklist and quiz", kicker="Lesson 1.4 applies doubly here", lines=["Verify by contract address. Doubly, for stablecoins.", "A fake “USDC” is one of the most common scams."], sub="The same habit, applied to the token you trust most.")
sc("bullets", "Here's this lesson's checklist. You know the type and backing of every stablecoin you hold. You know exactly who can redeem it, and how. You don't treat different stablecoins as diversified if they share the same issuer or collateral. And you have an actual depeg exit rule, written down before you need it.",
   chapter="Checklist and quiz", title="Before you move on", numbered=True,
   items=["Know the type and backing of every stablecoin held", "Know who can redeem it, and how", "Don't count shared-issuer coins as diversified", "Have a written depeg exit rule, in advance"])
sc("quiz", "Question one. What actually keeps a fiat-backed stablecoin near one dollar? [[pause 4]] The answer: redemption for one dollar of real reserves, plus arbitrageurs who are able to redeem it.",
   chapter="Checklist and quiz", n=1, of=5, q="What keeps a fiat-backed stablecoin near $1?", a="Redemption for $1 of reserves, plus arbitrageurs who can redeem.")
sc("quiz", "Question two. Why are algorithmic designs specifically fragile? [[pause 4]] The answer: they rely on confidence and their own sister token. When demand falls, the mechanism itself can amplify the fall instead of stopping it.",
   chapter="Checklist and quiz", n=2, of=5, q="Why are algorithmic designs fragile?", a="They rely on confidence and their own token; falling demand can amplify the fall.")
sc("quiz", "Question three. Two stablecoins, both backed by the exact same collateral. Are you diversified? [[pause 4]] The answer: no. They share the exact same failure point; if it fails, both fail together.",
   chapter="Checklist and quiz", n=3, of=5, q="Two stablecoins backed by the same collateral. Diversified?", a="No. They share the same failure point.")
sc("quiz", "Question four. What actually made U.S.D.C. recover in March twenty twenty-three, while TerraUSD never did in May twenty twenty-two? [[pause 4]] The answer: real, confirmable reserves. U.S.D.C.'s backing was real; TerraUSD's was ultimately just confidence.",
   "Question four. What actually made USDC recover in March 2023, while TerraUSD never did in May 2022? [[pause 4]] The answer: real, confirmable reserves. USDC's backing was real; TerraUSD's was ultimately just confidence.",
   chapter="Checklist and quiz", n=4, of=5, q="Why did USDC recover in 2023 while TerraUSD never did in 2022?", a="USDC's backing was real reserves. TerraUSD's was ultimately just confidence.")
sc("quiz", "Question five. In the worked example, why can't you personally arbitrage the ninety-seven-cent discount? [[pause 4]] The answer: only verified institutional minters can redeem directly with the issuer; you have to rely on them acting instead.",
   "Question five. In the worked example, why can't you personally arbitrage the $0.97 discount? [[pause 4]] The answer: only verified institutional minters can redeem directly with the issuer; you have to rely on them acting instead.",
   chapter="Checklist and quiz", n=5, of=5, q="Why can't you personally arbitrage a $0.97 stablecoin discount?", a="Only verified institutional minters can redeem directly with the issuer.")

# ---------------------------------------------------------------- recap and next
sc("flow", "Here's the whole lesson, recapped as one loop. Know the design: fiat, crypto, synthetic or algorithmic. Know exactly who can redeem, and how. Watch redemption access and reserve quality, since that's the whole peg. Never count shared-collateral coins as diversified. And keep a written depeg exit rule, ready before you ever need it.",
   chapter="Recap and next", title="This lesson, recapped as one loop", layout="cycle",
   nodes=[{"label": "Know the design", "icon": "layers"}, {"label": "Know who can redeem", "icon": "key"}, {"label": "Watch access & reserves", "icon": "eye"},
          {"label": "Shared collateral isn't diversified", "icon": "alert"}, {"label": "Have a written exit rule", "icon": "check"}])
sc("statement", "This is education, not financial advice. The historical events in this lesson, TerraUSD in May twenty twenty-two and U.S.D.C. in March twenty twenty-three, are real and worth researching further; every other number is illustrative.",
   "This is education, not financial advice. The historical events in this lesson, TerraUSD in May 2022 and USDC in March 2023, are real and worth researching further; every other number is illustrative.",
   chapter="Recap and next", kicker="A reminder", lines=["The two historical events here are real.", "Every other figure is illustrative."], sub="Not financial advice. Worth researching further.")
sc("cta", "That's stablecoins and how they break: four designs, peg mechanics, two real events, and a real worked example. Next, Lesson one point six: scam defence.",
   chapter="Recap and next", button="Next: Lesson 1.6", sub="Scam defence")

spec = {"id": "lesson-01-5", "title": "Lesson 1.5: Stablecoins and how they break", "size": [1920, 1080], "group": "lessons", "maxMinutes": 25, "tag": "Lesson 1.5",
        "gold": True, "seed": 115,
        "use": "Lesson 1.5 page in the Whop course. Gold-standard script: a flow3d recreation of the module's own stablecoin-designs.png (extended to all 4 types) anchor, a backing/risk glossary ticker, a chart3d anchor on the source's own $0.97 arbitrage maths, two real historical case studies (UST May 2022, USDC March 2023), and the source's worked example.",
        "thumbnail": {"title": "Stablecoins & how they break", "subtitle": "Lesson 1.5"}, "scenes": S}
out = ROOT / "video-scripts" / "gold" / "lesson-01-5.json"
out.write_text(json.dumps(spec, indent=1, ensure_ascii=False))
words = sum(len(s["vo"].replace("[[pause 4]]", "").split()) for s in S)
print(f"{len(S)} scenes, {words} words, est {(words / 171 * 60 + len(S) * 1.3 + 5 * 3) / 60:.1f} min")
