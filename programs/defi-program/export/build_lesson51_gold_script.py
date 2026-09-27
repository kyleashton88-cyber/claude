#!/usr/bin/env python3
"""Gold-standard script for Lesson 5.1, Bridges and trust assumptions
(target 11-14 minutes, per the "a bit longer" note for lessons from here
on). Walks the three bridge types (canonical, lock-and-mint, liquidity
network), what actually decides a bridge's trust model, why bridges are
prime hack targets, and the source material's own worked example
(moving $50,000 to an L2: canonical for the bulk, a reputable fast bridge
for a small time-sensitive amount, send a test first, never leave large
balances as a wrapped asset from a weak bridge), as visual walk-throughs.
Written in one pass at the full target length (no separate expansion
round).

Writes video-scripts/gold/lesson-05-1.json (the generator skips lessons
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
sc("title", "Lesson five point one. Bridges, and trust assumptions. By the end, you'll be able to choose a bridge route by its actual trust model, and size your own exposure to it accordingly.",
   "Lesson 5.1. Bridges and trust assumptions. By the end, you'll be able to choose a bridge route by its actual trust model, and size your own exposure to it accordingly.",
   chapter="Intro", eyebrow="Lesson 5.1", num="5.1", title="Bridges & trust assumptions", sub="Never leave a large balance as a wrapped asset from a weak bridge.")
sc("pillars", "Here's the plan. The three genuinely different ways a bridge can actually move value between chains. What a trust model actually is, and exactly who gets to approve a transfer. Why bridges specifically end up as such frequent hack targets. And a full worked example, routing a real amount of money across a real bridge decision.",
   chapter="Intro", title="What this lesson covers",
   items=[{"icon": "chart", "title": "Three bridge types", "text": "Canonical, lock-and-mint, liquidity networks"}, {"icon": "shield", "title": "The trust model", "text": "Who's actually allowed to approve a transfer"},
          {"icon": "alert", "title": "Why bridges get hit", "text": "Large value, concentrated behind complex logic"}, {"icon": "target", "title": "Worked example", "text": "Routing $50,000 to an L2, correctly"}])

# ---------------------------------------------------------------- three bridge types
sc("title", "Three genuinely different ways to bridge.", chapter="Three bridge types", eyebrow="Three bridge types", num="3", title="Canonical · Lock-and-mint · Liquidity network",
   sub="Not interchangeable. Each makes a different trade-off.")
img(D + "bridge-trust.png", "How each bridge type actually works",
    "Here are all three ways value actually moves between chains. A canonical bridge is a chain's own official route, like a rollup's native bridge, usually carrying the strongest security available, sometimes at the cost of being slower. Lock-and-mint locks your asset on the source chain, and mints a wrapped copy on the destination chain, a copy that's only ever as good as whatever's actually backing that lock. And a liquidity network simply pays you out directly on the other side, fast, but specifically dependent on that network's own contracts and its own available liquidity.",
    chapter="Three bridge types")
sc("flow", "Here's the actual trade-off each of these three makes, side by side, since none of them is simply better than the others in every situation. Canonical: strongest security, sometimes slower. Lock-and-mint: fast, but the wrapped copy's real value depends entirely on the lock behind it holding. Liquidity network: fastest of all three, but you're now trusting that network's own contracts and its own liquidity being genuinely available when you need it.",
   chapter="Three bridge types", title="The trade-off each one makes",
   nodes=[{"label": "Canonical", "sub": "Strongest security, sometimes slower", "icon": "shield"}, {"label": "Lock-and-mint", "sub": "Fast; the wrapped copy is only as good as the lock", "icon": "coins"},
          {"label": "Liquidity network", "sub": "Fastest; trusting their contracts and liquidity", "icon": "chart"}])
sc("compare", "Here's a practical way to match these three types to what you're actually trying to do, rather than defaulting to whichever one loads first. Moving a genuinely large amount, with no particular urgency, is exactly the canonical route's own strength. Moving a small amount, where speed actually matters more than squeezing out the very last bit of security, is exactly where a fast liquidity network earns its keep instead.",
   chapter="Three bridge types",
   left={"label": "Large amount, no urgency", "tone": "good", "items": ["Exactly the canonical route's strength", "Worth the extra time for the extra security"]},
   right={"label": "Small amount, speed matters", "tone": "warn", "items": ["Where a fast liquidity network earns its keep", "The amount at risk is deliberately small"]})
sc("quiz", "Quick check. What actually backs a lock-and-mint wrapped token? [[pause 4]] The answer: the assets locked on the source chain, and the bridge's own security actually holding that lock.",
   chapter="Three bridge types", n=1, of=4, q="What backs a lock-and-mint wrapped token?",
   a="The locked assets on the source chain, and the bridge's security.")

# ---------------------------------------------------------------- the trust model
sc("title", "What a trust model actually is.", chapter="The trust model", eyebrow="The trust model", num="1", title="Who's actually allowed to approve a transfer",
   sub="Fewer, weaker signers. More risk. Every single time.")
sc("flow", "Here's exactly what decides a bridge's real trust model, the single most important question to ask about any bridge before using it. Who's actually allowed to approve a transfer moving through it: a multisig held by just a handful of keys, a broader validator set, a light client verifying the source chain directly, or genuine fraud or validity proofs. Fewer, weaker signers means more risk, in a direct, almost mechanical relationship.",
   chapter="The trust model", title="Who can approve a transfer",
   nodes=[{"label": "A multisig, a few keys", "sub": "Weakest: compromise a handful of keys, done", "icon": "alert"}, {"label": "A validator set", "sub": "Stronger: more independent parties to compromise", "icon": "shield"},
          {"label": "A light client", "sub": "Verifies the source chain directly, cryptographically", "icon": "eye"}, {"label": "Fraud or validity proofs", "sub": "Strongest: mathematically verified, not just trusted", "icon": "check"}])
sc("statement", "Worth being precise about why this specific question matters more than almost anything else about a bridge, including its own brand name or how long it's been operating. A bridge secured by a small multisig can be drained the moment enough of those keys are compromised, regardless of how much total value it's ever safely processed before that exact moment.",
   chapter="The trust model", kicker="Why this question matters most", lines=["A small multisig can be drained the moment enough keys are compromised.", "Regardless of how much it's safely processed before that exact moment."], sub="Past volume isn't safety. The trust model is what actually protects you.")
sc("steps", "Here's how to actually check a bridge's real trust model yourself, before ever routing meaningful value through it. Find its own documentation, specifically for how transfers actually get approved, not just its marketing description. Count how many signers, or validators, are genuinely required, and how independent they actually are from each other. And check whether it's ever published a real security audit covering that exact approval mechanism specifically.",
   chapter="The trust model", title="Checking a bridge's trust model yourself",
   steps=["Find its documentation on how transfers actually get approved", "Count how many signers are required, and how independent they are", "Check for a real audit covering that exact approval mechanism"])
sc("statement", "Worth making the multisig risk concrete, rather than leaving it abstract. If a bridge relies on a five-of-eight multisig, an attacker only needs to compromise five specific keys, out of eight, to move everything that bridge holds. That's a genuinely finite, achievable target, especially against keys held by individuals or small teams, not some enormous, near-impossible barrier.",
   chapter="The trust model", kicker="Making the multisig risk concrete", lines=["A 5-of-8 multisig: compromise 5 specific keys, move everything.", "A genuinely finite, achievable target, not an enormous barrier."], sub="Count the actual number. It's usually smaller than it sounds.")
sc("quiz", "Quick check. What's the actual relationship between the number of signers a bridge relies on, and its risk? [[pause 4]] The answer: fewer, weaker signers means more risk, directly, since compromising a smaller group is genuinely easier.",
   chapter="The trust model", n=2, of=4, q="What's the relationship between signer count and bridge risk?",
   a="Fewer, weaker signers means more risk.")

# ---------------------------------------------------------------- why bridges get hit
sc("title", "Why bridges are such frequent targets.", chapter="Why bridges get hit", eyebrow="Why bridges get hit", num="1", title="Large value, concentrated behind complex logic",
   sub="A single point where enormous value genuinely sits.")
sc("statement", "Worth being precise about the actual mechanism that makes bridges such attractive targets, since it isn't random or purely about weak code. Bridges hold large, concentrated pools of value, specifically because every single user crossing that bridge needs their assets to sit somewhere while the transfer completes. That concentration, combined with genuinely complex cross-chain logic, is exactly the combination an attacker is looking for: a lot to gain, in one place, through one mechanism.",
   chapter="Why bridges get hit", kicker="The actual mechanism", lines=["Large, concentrated value, held in one place, by design.", "Combined with genuinely complex cross-chain logic."], sub="A lot to gain, in one place, through one mechanism. That's the target.")
sc("statement", "Worth also naming why this pattern has repeated itself so often across DeFi's own history, rather than being an occasional accident. Complex cross-chain logic is genuinely hard to get perfectly right, and a single flaw anywhere in that logic can expose the entire pool at once, not just one user's individual funds. That's structurally different from a bug in an ordinary single-chain contract, which usually only exposes its own smaller pool.",
   chapter="Why bridges get hit", kicker="Why this pattern keeps repeating", lines=["Cross-chain logic is genuinely hard to get perfectly right.", "One flaw can expose the entire pool at once, not just one user."], sub="This is exactly why this module treats bridges as their own risk category.")

sc("quiz", "Quick check. Why are bridges such frequent hack targets, specifically? [[pause 4]] The answer: they concentrate large amounts of value behind genuinely complex, cross-chain logic, all in one place.",
   chapter="Why bridges get hit", n=3, of=4, q="Why are bridges frequent hack targets?",
   a="They concentrate large amounts of value behind complex, cross-chain logic.")

# ---------------------------------------------------------------- worked example
sc("title", "Worked example.", chapter="Worked example", eyebrow="Worked example", num="1", title="Routing $50,000 to a layer 2, correctly",
   sub="The source material's own scenario.")
sc("steps", "Here's exactly how to actually route this, step by step, applying everything from earlier in this lesson to a real amount. Use the canonical route for the bulk of the fifty thousand dollars, even if it's genuinely slower than the alternatives. Use a reputable, well-established fast bridge only for a small, specifically time-sensitive portion, if you actually need speed. And send a small test transaction first, on any route, before committing the full amount to it.",
   chapter="Worked example", title="Routing $50,000 to an L2",
   steps=["Canonical route for the bulk, even if slower", "A reputable fast bridge, only for a small, time-sensitive amount", "Send a test transaction first, on any route, before committing"], result="Never leave large balances as a wrapped asset from a weak bridge")
sc("compare", "Here's the actual reasoning behind splitting it this way, rather than simply picking whichever single route seems most convenient. The bulk of the value genuinely benefits from the canonical route's stronger security, since size is exactly what makes a position worth protecting most carefully. A small, urgent portion can reasonably accept a faster bridge's slightly different risk, specifically because the amount at stake, if something did go wrong, is deliberately kept small.",
   chapter="Worked example",
   left={"label": "The bulk ($50k, less urgent)", "tone": "good", "items": ["Canonical route, for its stronger security", "Size is exactly what's worth protecting most"]},
   right={"label": "A small, urgent portion", "tone": "warn", "items": ["A reputable fast bridge, accepted deliberately", "The amount at risk is kept deliberately small"]})
sc("statement", "Here's the one sentence this entire worked example exists to prove, worth holding onto more than the specific dollar figure involved. Never leave a large balance sitting as a wrapped asset from a weak bridge, for any longer than it genuinely has to, since that wrapped token's real value is only ever as good as the lock, or the trust model, actually standing behind it.",
   chapter="Worked example", kicker="The one sentence to keep", lines=["Never leave a large balance as a wrapped asset from a weak bridge.", "It's only ever as good as the lock or trust model behind it."], sub="Size and route deliberately. Don't just pick whatever's fastest.")
sc("quiz", "Quick check. For fifty thousand dollars, fast bridge, or canonical? [[pause 4]] The answer: canonical for the bulk of it; a fast bridge only for a small, genuinely urgent amount.",
   chapter="Worked example", n=4, of=4, q="Fast bridge or canonical for $50k?",
   a="Canonical for the bulk; fast only for small, urgent amounts.")

# ---------------------------------------------------------------- checklist and recap
sc("compare", "Here's why sending a small test transaction first is worth the extra few minutes it costs, on any bridge, even one you've used before. It catches a wrong destination address, an unexpected fee, or a genuinely broken route, all for the cost of a small amount, instead of discovering the exact same problem with your full balance already committed and in flight.",
   chapter="Checklist",
   left={"label": "Test transaction first", "tone": "good", "items": ["Catches problems for the cost of a small amount", "A few minutes, well spent"]},
   right={"label": "Full amount, no test", "tone": "bad", "items": ["Discovers the exact same problem too late", "With the full balance already in flight"]})
sc("steps", "Here's your checklist. Do it before bridging anything of real size. Write down the actual trust model of every bridge you use, explicitly, not just its name. Prefer the canonical route specifically for size, even when it's slower. And cap your own wrapped-asset exposure, deliberately, the same way you'd cap any other single point of failure.",
   chapter="Checklist", title="Your checklist",
   steps=["Trust model of every bridge I use written down", "Canonical route preferred for size", "Wrapped-asset exposure capped"])
sc("bullets", "Let's recap. Three bridge types: canonical, lock-and-mint, and liquidity network, each making a genuinely different trade-off. A bridge's trust model, who can actually approve a transfer, is the single most important question, and fewer, weaker signers always means more risk. Bridges are frequent targets specifically because they concentrate large value behind complex logic. And for real size, use the canonical route, keep fast bridges for small, urgent amounts, and never leave a large balance wrapped from a weak bridge.",
   chapter="Recap", title="Recap", check=False,
   items=["Three types: canonical, lock-and-mint, liquidity network", "Trust model = who can approve a transfer; fewer signers = more risk",
          "Bridges are targets: large value, concentrated behind complex logic", "For size: canonical route, small amounts on fast bridges, never leave wrapped and large"])
sc("statement", "Worth connecting this directly back to the dependency map from this module's own Mastery Starter. A bridge is exactly one specific link in that chain, and now you know exactly what to actually check on it: which of the three types it is, who's allowed to approve a transfer through it, and how much of your own balance you're willing to leave sitting on the wrapped side of it at any given moment.",
   chapter="Recap", kicker="Connecting back to the dependency map", lines=["A bridge is one specific link in that chain.", "Now you know exactly what to check on it."], sub="One link mapped. Several more links still to come in this module.")
sc("cta", "Write down every bridge's trust model, prefer canonical for size, and cap your wrapped-asset exposure. Next up, Lesson five point two: layer twos, sequencers, and withdrawal paths.",
   "Write down every bridge's trust model, prefer canonical for size, and cap your wrapped-asset exposure. Next up, Lesson 5.2: layer 2s, sequencers & withdrawal paths.",
   chapter="Recap", button="Next: Lesson 5.2", sub="Layer 2s, sequencers & withdrawal paths")

spec = {"id": "lesson-05-1", "title": "Lesson 5.1: Bridges & trust assumptions", "size": [1920, 1080], "group": "lessons", "maxMinutes": 25,
        "tag": "Lesson 5.1", "gold": True, "music": True, "musicLevel": 0.14, "seed": 79,
        "use": "Lesson 5.1 page in the Whop course. Hand-written gold-standard script: the three bridge types, what a trust model is and why fewer signers means more risk, why bridges get hit, and the source material's own $50,000-routing worked example, as walk-throughs.",
        "thumbnail": {"title": "Bridges & trust assumptions", "subtitle": "Lesson 5.1"}, "scenes": S}
out = ROOT / "video-scripts" / "gold" / "lesson-05-1.json"
out.write_text(json.dumps(spec, indent=1, ensure_ascii=False))
words = sum(len(s["vo"].replace("[[pause 4]]", "").split()) for s in S)
print(f"{len(S)} scenes, {words} words, est {(words / 171 * 60 + len(S) * 1.3 + 4 * 4) / 60:.1f} min")
