#!/usr/bin/env python3
"""Gold-standard script for Lesson 4.8, Tokenized treasuries and
real-world assets (RWAs) (target 11-14 minutes, per the "a bit longer"
note for lessons from here on). Completes Module 4. Walks what an RWA
token actually represents, who you're trusting (issuer, custodian,
redemption, transfer rules), access limits and composability, and the
source material's own worked example (4.0% short-term bills minus a
0.15% fee = ~3.85%), as visual walk-throughs. Written in one pass at the
full target length (no separate expansion round).

Writes video-scripts/gold/lesson-04-8.json (the generator skips lessons
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
sc("title", "Lesson four point eight. Tokenized treasuries, and real-world assets. By the end, you'll know exactly what you actually own, and specifically who you're trusting, before ever holding one of these tokens.",
   "Lesson 4.8. Tokenized treasuries and real-world assets (RWAs). By the end, you'll know exactly what you actually own, and specifically who you're trusting, before ever holding one of these tokens.",
   chapter="Intro", eyebrow="Lesson 4.8", num="4.8", title="Tokenized treasuries & real-world assets (RWAs)", sub="This completes Module 4: Yield.")
sc("pillars", "Here's the plan. What an R.W.A. token actually represents, off-chain. Exactly who you're trusting, across four separate parties. Access limits, and composability, the two practical constraints that decide how usable one actually is. And a full worked example, using the source material's own numbers for a tokenized treasury product.",
   chapter="Intro", title="What this lesson covers",
   items=[{"icon": "coins", "title": "What an RWA represents", "text": "Government bills, money-market funds, credit, property"}, {"icon": "shield", "title": "Who you're trusting", "text": "Issuer, custodian, redemption, transfer rules"},
          {"icon": "alert", "title": "Access limits", "text": "KYC, accreditation, country eligibility"}, {"icon": "target", "title": "Worked example", "text": "4.0% bills, a 0.15% fee, 3.85% net"}])

# ---------------------------------------------------------------- what an rwa represents
sc("title", "What an RWA actually represents.", chapter="What an RWA is", eyebrow="What an RWA is", num="1", title="A token, standing in for something off-chain",
   sub="Most commonly, short-term government bills.")
img(D + "rwa-trust.png", "What you're actually trusting",
    "Here's what a real-world asset token genuinely is: a token that represents an asset that exists entirely off-chain. Most commonly, that's short-term government bills, the single most common R.W.A. by far. But it can also be a money-market fund, private credit, commodities, or even property. The token itself is a claim, a representation. The actual asset it represents sits, and is managed, entirely outside the blockchain.",
    chapter="What an RWA is")
sc("statement", "Worth being precise about how a tokenized treasury product's yield typically works, since it's a genuinely simple, transparent relationship. It tracks the short-term government rate directly, minus the product's own management fee. There's no separate mechanism, no hidden formula, and importantly, none of the emissions or funding-rate risk that some of the other stablecoin yield sources from last lesson carry.",
   chapter="What an RWA is", kicker="How the yield actually works", lines=["Tracks the short-term government rate, minus a management fee.", "No emissions risk, no funding-rate risk, unlike some other sources."], sub="Simple and transparent. Its own risks live entirely elsewhere.")
sc("statement", "Worth connecting this directly back to the four stablecoin yield sources from last lesson, since a tokenized treasury is essentially that lesson's third source, treasury-backed, in its purest, most direct form. Its risk profile is genuinely different from the other three: no protocol code to worry about, no governance vote resetting a rate, and no funding payments that can silently turn negative.",
   chapter="What an RWA is", kicker="Connecting back to the four yield sources", lines=["This is essentially last lesson's 'treasury-backed' source, directly.", "No protocol code, no governance vote, no funding that can turn negative."], sub="A genuinely different risk profile from the other three sources.")
sc("quiz", "Quick check. What does a tokenized treasury product's yield actually track? [[pause 4]] The answer: short-term government rates, minus whatever fee the product itself charges.",
   chapter="What an RWA is", n=1, of=3, q="What does a tokenized treasury product's yield track?",
   a="Short-term government rates, minus the product's fees.")

# ---------------------------------------------------------------- who you're trusting
sc("title", "Who you're actually trusting.", chapter="Who you're trusting", eyebrow="Who you're trusting", num="4", title="Four separate parties, each one essential",
   sub="Issuer · Custodian · Redemption process · Transfer rules")
sc("flow", "Here's all four parties this actually runs through, since the token itself is only as good as every one of them. The issuer is the legal structure that actually created the token, and stands behind it. The custodian is who physically, or legally, holds the real off-chain assets backing it. The redemption process is how, and how quickly, you can actually convert the token back into real value. And transfer rules decide where, and to whom, the token is even allowed to move.",
   chapter="Who you're trusting", title="The four parties behind the token",
   nodes=[{"label": "The issuer", "sub": "The legal structure standing behind it", "icon": "shield"}, {"label": "The custodian", "sub": "Who actually holds the real assets", "icon": "coins"},
          {"label": "The redemption process", "sub": "How, and how quickly, you can convert back", "icon": "clock"}, {"label": "Transfer rules", "sub": "Where, and to whom, it's allowed to move", "icon": "alert"}])
sc("statement", "Worth being precise about why all four have to hold up, not just any one or two of them, for this to actually work the way you'd expect. A sound issuer with a weak custodian is still a real problem. A sound issuer and custodian with a redemption process that quietly stalls under stress is still a real problem. Each one is a genuinely separate point of trust, not a repeated version of the same risk.",
   chapter="Who you're trusting", kicker="Why all four have to hold up", lines=["A weak link at any one of the four is still a real problem.", "Each is a separate point of trust, not a repeated version of one risk."], sub="Check all four. Not just the one that's easiest to verify.")
sc("steps", "Here's how to actually verify these four parties yourself, rather than just taking a name on a website at face value. Find the issuer's actual legal structure and jurisdiction, documented, not just implied. Find independent evidence of what the custodian actually holds, ideally a real, regular attestation, not just a claim. And read the redemption terms directly, specifically for timing, minimums, and any conditions attached.",
   chapter="Who you're trusting", title="Verifying the four parties yourself",
   steps=["Find the issuer's legal structure and jurisdiction, documented", "Find independent attestation of what the custodian holds", "Read the redemption terms directly: timing, minimums, conditions"])
sc("quiz", "Quick check. Name two parties you're actually trusting with an R.W.A. token. [[pause 4]] The answer: any two of the issuer, the custodian, the redemption agent, or the token's administrators.",
   chapter="Who you're trusting", n=2, of=3, q="Name two parties you trust with an RWA token.",
   a="Any two: the issuer, the custodian, the redemption agent, the token's administrators.")

# ---------------------------------------------------------------- access limits and composability
sc("title", "Access limits, and composability.", chapter="Access limits & composability", eyebrow="Access limits & composability", num="1", title="The two practical constraints",
   sub="What decides who can hold it, and what you can actually do with it.")
sc("flow", "Here's exactly what these two constraints each actually decide. Access limits decide who's even allowed to hold the token in the first place, often restricted specifically to verified, K.Y.C.'d holders, or to accredited or qualified investors only, and not available at all in every country. Composability decides what you can actually do with it once you hold it: some R.W.A. tokens can be used freely as collateral elsewhere in DeFi, while others are restricted entirely to a specific allowlist of approved wallets.",
   chapter="Access limits & composability", title="What each constraint actually decides",
   nodes=[{"label": "Access limits", "sub": "Who's allowed to hold it: KYC, accreditation, country", "icon": "shield"}, {"label": "Composability", "sub": "What you can do with it: free collateral, or allowlisted only", "icon": "chart"}])
sc("statement", "Worth being completely direct about the actual rule here, since it's simple and non-negotiable. Check your own eligibility, in your own actual country, before ever touching one of these products. Never attempt to work around a restriction that specifically applies to you; that's a legal and structural risk entirely separate from anything about the underlying asset itself.",
   chapter="Access limits & composability", kicker="The non-negotiable rule", lines=["Check your own eligibility, in your own country, first.", "Never work around a restriction that applies to you."], sub="This risk has nothing to do with the underlying asset. It's entirely your own.")
sc("compare", "Here's what that composability difference actually looks like in practice, concretely, between two R.W.A. tokens that might otherwise look identical on paper. One with open composability can be deposited directly as collateral in an ordinary lending market, exactly like any other DeFi asset. One restricted to an allowlist can only move between pre-approved wallets, meaning it can't be used in most DeFi protocols at all, however attractive its own underlying yield happens to be.",
   chapter="Access limits & composability",
   left={"label": "Open composability", "tone": "good", "items": ["Usable as collateral in ordinary lending markets", "Behaves like any other DeFi asset"]},
   right={"label": "Allowlist-restricted", "tone": "warn", "items": ["Only moves between pre-approved wallets", "Can't be used in most DeFi protocols at all"]})
sc("quiz", "Quick check. Why does it actually matter to check an R.W.A. token's transfer restrictions? [[pause 4]] The answer: some R.W.A. tokens only move between allowlisted wallets, which directly limits your ability to exit, or to use it elsewhere in DeFi.",
   chapter="Access limits & composability", n=3, of=3, q="Why check transfer restrictions?",
   a="Some RWA tokens only move between allowlisted wallets, which limits exit and DeFi use.")

# ---------------------------------------------------------------- worked example
sc("title", "Worked example.", chapter="Worked example", eyebrow="Worked example", num="1", title="4.0% bills, a 0.15% fee",
   sub="The source material's own illustrative scenario.")
sc("steps", "Here's the calculation, exactly as the source material lays it out, illustratively. Short-term government bills are yielding four point zero percent. The tokenized product charges a zero point one five percent management fee on top of holding them for you. Subtract that fee from the underlying rate, and you'd earn approximately three point eight five percent, before any additional on-chain costs of your own.",
   chapter="Worked example", title="4.0% bills − 0.15% fee",
   steps=["Short-term government bills: 4.0%", "− 0.15% management fee", "≈ 3.85%, before your own on-chain costs"], result="A simple, transparent calculation — the hard part is the trust, not the math")
sc("statement", "Worth being precise about where this specific product could actually fit, using the own-bank ladder framework from Module twelve. It can genuinely suit the safer, near-term tiers of that ladder, but only, and specifically, if its redemption time actually matches when you'd genuinely need that money back. A product yielding an attractive rate is no use at all if your own redemption window doesn't line up with your own actual timeline.",
   chapter="Worked example", kicker="Where this actually fits your own plan", lines=["Can suit the safer, near-term tiers of your own ladder.", "Only if its redemption time matches when you'll actually need it."], sub="The rate doesn't matter if the timing doesn't line up.")
sc("compare", "Here's that exact same point, made concrete, comparing a redemption time that matches your own need against one that doesn't. A redemption window shorter than, or equal to, when you'll actually need the money keeps this product genuinely usable for that purpose. A redemption window longer than your own timeline means you could be forced to sell into a secondary market instead, at whatever price that happens to offer, right when you needed the cash.",
   chapter="Worked example",
   left={"label": "Redemption matches your timeline", "tone": "good", "items": ["Genuinely usable for that specific need", "You get the money when you actually need it"]},
   right={"label": "Redemption is slower than your timeline", "tone": "bad", "items": ["Forced to sell into a secondary market instead", "At whatever price it happens to offer, right then"]})

sc("compare", "Here's why this particular risk shape feels different from most of what this module has covered so far, worth naming explicitly before closing it out. A vault, a restaking stack, or a synthetic funding position all carry genuinely technical, on-chain risks, code, oracles, correlated failure, funding turning negative. An R.W.A. token's risk is almost entirely off-chain and legal instead: who the issuer and custodian actually are, and whether they do what they say.",
   chapter="Worked example",
   left={"label": "Vaults, restaking, synthetic yield", "tone": "warn", "items": ["Technical, on-chain risk", "Code, oracles, correlated failure, funding"]},
   right={"label": "RWA tokens", "tone": "warn", "items": ["Almost entirely off-chain, legal risk", "Who the issuer and custodian actually are"]})

# ---------------------------------------------------------------- checklist and recap
sc("steps", "Here's your checklist. Do it before holding any R.W.A. token. Confirm you're actually eligible in your own country, and that holding it is genuinely legal for you. Read the issuer, the custodian, and the redemption terms, all three, not just whichever one is easiest to find. Know its transfer restrictions and any minimum holding amounts. And size the entire position within caps, the exact same way you'd size any other single-issuer risk.",
   chapter="Checklist", title="Your checklist",
   steps=["Eligible in my country (and it's legal to hold)", "Issuer, custodian and redemption terms read", "Transfer restrictions and minimums known", "Sized within caps, like any other issuer risk"])
sc("title", "What this whole module actually built.", chapter="Recap", eyebrow="Module 4 complete", num="4", title="From farming to restaking to real-world assets",
   sub="One skill, applied across seven completely different yield sources.")
sc("bullets", "Here's the one skill this entire module has been building, across every lesson in it, from farming, through staking and restaking, to vaults, airdrops, stablecoins, and now real-world assets. Split any advertised yield into what it's genuinely earned from, and name the specific risk being paid for. That's the actual outcome this module set out to teach, back at its own Mastery Starter.",
   chapter="Recap", title="The one skill, across seven different sources", check=False,
   items=["Yield farming: base yield vs. printed emissions", "Staking and restaking: network security, stacked risk layers",
          "Vaults, airdrops, stablecoins, and now RWAs: same test, every time", "Split the source. Name the risk. That's the whole skill."])
sc("bullets", "Let's recap. An R.W.A. token represents an off-chain asset, most commonly short-term government bills. You're trusting four separate parties: the issuer, the custodian, the redemption process, and its transfer rules. Access limits and composability decide who can hold it, and what you can actually do with it. And the source material's own example shows the math is simple, four percent minus a small fee; the real work is verifying the trust behind it, and matching its redemption time to your own actual needs.",
   chapter="Recap", title="Recap", check=False,
   items=["An RWA token: a claim on an off-chain asset, most often government bills", "You trust four parties: issuer, custodian, redemption process, transfer rules",
          "Access limits and composability decide who can hold it, and what you can do with it", "The math is simple. The real work is verifying trust and matching redemption timing"])
sc("cta", "Confirm your own eligibility, read all three of issuer, custodian and redemption terms, and match redemption timing to your own needs. That's the end of Module four. Next up, Module five.",
   "Confirm your own eligibility, read all three of issuer, custodian and redemption terms, and match redemption timing to your own needs. That's the end of Module 4. Next up, Module 5.",
   chapter="Recap", button="Next: Module 5", sub="Continuing the On-Chain Operator Program")

spec = {"id": "lesson-04-8", "title": "Lesson 4.8: Tokenized treasuries & RWAs", "size": [1920, 1080], "group": "lessons", "maxMinutes": 25,
        "tag": "Lesson 4.8", "gold": True, "music": True, "musicLevel": 0.14, "seed": 77,
        "use": "Lesson 4.8 page in the Whop course. Hand-written gold-standard script: what an RWA token represents, the four parties you're trusting, access limits and composability, and the source material's own 4.0%-minus-0.15%-fee worked example, as walk-throughs. Completes Module 4.",
        "thumbnail": {"title": "Tokenized treasuries & RWAs", "subtitle": "Lesson 4.8"}, "scenes": S}
out = ROOT / "video-scripts" / "gold" / "lesson-04-8.json"
out.write_text(json.dumps(spec, indent=1, ensure_ascii=False))
words = sum(len(s["vo"].replace("[[pause 4]]", "").split()) for s in S)
print(f"{len(S)} scenes, {words} words, est {(words / 171 * 60 + len(S) * 1.3 + 4 * 3) / 60:.1f} min")
