#!/usr/bin/env python3
"""Gold-standard script for Lesson 5.7, Operating across chains: gas,
routes and chain abstraction (target 11-14 minutes, per the "a bit
longer" note for lessons from here on). Walks gas stranding, the four
route choices (canonical, fast bridge, exchange deposit-withdraw,
intent-based swaps), chain abstraction and its hidden dependency layers,
and the source material's own worked example ($30,000 USDC from Arbitrum
to Base: canonical via Ethereum, a fast bridge at $5-15/minutes, or an
exchange; send $50 first by the chosen route, keep ~$5 of ETH on Base for
gas, then send the rest), as visual walk-throughs. Written in one pass at
the full target length (no separate expansion round).

Writes video-scripts/gold/lesson-05-7.json (the generator skips lessons
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
sc("title", "Lesson five point seven. Operating across chains: gas, routes, and chain abstraction. By the end, you'll be able to move value between chains cheaply and safely, without ever getting stranded somewhere you can't afford to transact.",
   "Lesson 5.7. Operating across chains: gas, routes & chain abstraction. By the end, you'll be able to move value between chains cheaply and safely, without ever getting stranded somewhere you can't afford to transact.",
   chapter="Intro", eyebrow="Lesson 5.7", num="5.7", title="Operating across chains: gas, routes & chain abstraction", sub="Keep a small gas float on every chain you actually use.")
sc("pillars", "Here's the plan. Gas stranding, exactly what it is, and why it's a genuinely simple problem to avoid entirely. The four real route choices for moving value between chains, and how they actually differ. Chain abstraction, what it hides, and why every hidden layer is still a real dependency. And a full worked example, moving thirty thousand dollars, choosing the route deliberately.",
   chapter="Intro", title="What this lesson covers",
   items=[{"icon": "alert", "title": "Gas stranding", "text": "Tokens you genuinely can't move, for lack of gas"}, {"icon": "chart", "title": "Four route choices", "text": "Canonical, fast bridge, exchange, intent-based"},
          {"icon": "shield", "title": "Chain abstraction", "text": "Convenient, and every hidden layer is a real dependency"}, {"icon": "target", "title": "Worked example", "text": "$30,000, three real routes, one test transaction"}])

# ---------------------------------------------------------------- gas stranding
sc("title", "Gas stranding.", chapter="Gas stranding", eyebrow="Gas stranding", num="1", title="Tokens you genuinely can't move",
   sub="A simple problem, entirely avoidable, every single time.")
img(D + "cross-chain-gas.png", "Why a small gas float matters everywhere",
    "Here's exactly what gas stranding actually is, and why it happens more often than you'd expect. You hold real, valuable tokens on a chain, but you hold none of that specific chain's own native gas token. Without it, you genuinely cannot pay for a single transaction, meaning you can't move those tokens anywhere at all, no matter how much they're actually worth, until you somehow get that chain's gas token onto that same address.",
    chapter="Gas stranding")
sc("statement", "Worth being completely direct about the actual fix here, since it's genuinely simple, and entirely avoidable with almost no effort. Keep a small gas float, a modest amount of that chain's own native token, on every single chain you actually use, at all times, specifically before you ever need it, not after you've already discovered you're stuck.",
   chapter="Gas stranding", kicker="The actual fix", lines=["Keep a small gas float, on every chain you use.", "Before you need it. Not after you discover you're stuck."], sub="A genuinely simple habit that entirely prevents this specific problem.")
sc("steps", "Here's how to actually recover, if you've already discovered you're genuinely stranded, rather than just prevented it in advance. Send a small amount of that specific chain's gas token, from an exchange, or another wallet you own, directly to the stranded address. Some bridges and faucets can also deliver a small amount of gas token alongside an incoming transfer, specifically for this exact situation. And once you've recovered, immediately add that chain to your own ongoing gas-float habit.",
   chapter="Gas stranding", title="Recovering, if it's already happened",
   steps=["Send a small amount of that chain's gas token in directly", "Some bridges/faucets can deliver gas alongside an incoming transfer", "Once recovered, add that chain to your ongoing gas-float habit"])
sc("quiz", "Quick check. What exactly is gas stranding? [[pause 4]] The answer: having real tokens on a chain, but no gas token to actually pay for a transaction, meaning you genuinely can't move them.",
   chapter="Gas stranding", n=1, of=3, q="What is gas stranding?",
   a="Having tokens on a chain with no gas token to move them.")

# ---------------------------------------------------------------- four route choices
sc("title", "Four real route choices.", chapter="Four route choices", eyebrow="Four route choices", num="4", title="Canonical · Fast bridge · Exchange · Intent-based",
   sub="Genuinely different trade-offs. Choose deliberately, not by default.")
sc("flow", "Here's all four ways to actually move value between chains, and what each one genuinely trades off. A canonical bridge, from Lesson five point one, is the safest, sometimes slower option. A fast bridge, or liquidity network, is quicker, relying on that network's own liquidity. An exchange deposit-and-withdraw is often the simplest choice for genuinely large amounts, but makes you briefly custodial, trusting that exchange for the moment your funds actually sit there. And intent-based cross-chain swaps let specialised solvers deliver your funds on the destination chain directly, on your behalf.",
   chapter="Four route choices", title="What each route actually trades off",
   nodes=[{"label": "Canonical bridge", "sub": "Safest, sometimes slower (Lesson 5.1)", "icon": "shield"}, {"label": "Fast bridge / liquidity network", "sub": "Quicker; relies on that network's own liquidity", "icon": "chart"},
          {"label": "Exchange deposit-withdraw", "sub": "Simple for large amounts; briefly custodial", "icon": "coins"}, {"label": "Intent-based swaps", "sub": "Solvers deliver on the destination chain for you", "icon": "eye"}])
sc("statement", "Worth being precise about why an exchange specifically deserves its own separate mention here, since it's easy to overlook as a genuine route at all. For genuinely large amounts, it's often the simplest, most liquid option available. But for the specific window your funds sit on that exchange, you're trusting it directly, exactly the same custodial trust question covered back in earlier lessons, just for a shorter, deliberate stretch of time.",
   chapter="Four route choices", kicker="Why an exchange deserves its own mention", lines=["Often the simplest, most liquid option for large amounts.", "But briefly custodial, for however long your funds actually sit there."], sub="A real route. Also a real, if temporary, trust decision.")
sc("compare", "Here's a practical way to actually choose between these four, based specifically on size, echoing the same pattern from Lesson five point one's own bridge decision. A small, routine amount reasonably fits a fast bridge or an intent-based swap, where speed matters more than squeezing out the very last bit of security. A genuinely large amount deserves the canonical route, or a carefully-checked exchange, specifically because size is exactly what's worth protecting most carefully.",
   chapter="Four route choices",
   left={"label": "Small, routine amount", "tone": "good", "items": ["Fast bridge, or an intent-based swap", "Speed reasonably outweighs the marginal risk"]},
   right={"label": "Genuinely large amount", "tone": "warn", "items": ["Canonical route, or a carefully-checked exchange", "Size is exactly what's worth protecting most"]})
sc("quiz", "Quick check. What's the actual risk of chain abstraction, specifically? [[pause 4]] The answer: each layer it hides, smart accounts, paymasters, solvers, is still a real, additional dependency, even though it's now invisible to you.",
   chapter="Four route choices", n=2, of=3, q="Risk of chain abstraction?",
   a="Each hidden layer (smart accounts, paymasters, solvers) is an extra dependency.")

# ---------------------------------------------------------------- chain abstraction
sc("title", "Chain abstraction.", chapter="Chain abstraction", eyebrow="Chain abstraction", num="1", title="Convenient. And every hidden layer is still real.",
   sub="\"Pay gas in USDC.\" \"One balance across chains.\" Genuinely useful, genuinely a dependency.")
sc("flow", "Here's exactly what chain abstraction actually does, and the specific mechanisms doing the hiding underneath it. Wallets and apps increasingly hide which chain you're actually on entirely, letting you pay gas in a stablecoin instead of that chain's own native token, or presenting one single balance across several different chains at once. Underneath all of that, smart accounts, paymasters, and solvers are the actual mechanisms doing this work, quietly, on your behalf.",
   chapter="Chain abstraction", title="What's actually doing the hiding",
   nodes=[{"label": "Smart accounts", "sub": "Programmable accounts, replacing a plain wallet", "icon": "shield"}, {"label": "Paymasters", "sub": "Let you pay gas in a different token entirely", "icon": "coins"},
          {"label": "Solvers", "sub": "Execute the actual cross-chain move, on your behalf", "icon": "chart"}])
sc("statement", "Worth being precise about the actual question worth asking, before relying on any chain-abstracted app, rather than simply enjoying the convenience without a second thought. Ask specifically what's actually happening underneath that simplified interface, which of these mechanisms is involved, and whether you'd genuinely be comfortable with each one individually, on its own merits, if it weren't hidden from view at all.",
   chapter="Chain abstraction", kicker="The question worth asking first", lines=["What's actually happening underneath the simplified interface?", "Would you be comfortable with each mechanism, if it weren't hidden?"], sub="Convenience is fine. Just don't let it skip the question entirely.")
sc("statement", "Worth being completely direct about the one sentence this entire topic reduces to, since convenience and safety aren't automatically the same thing here. It's genuinely convenient, and every single layer that hides that complexity from you is also a real dependency, exactly like a bridge, an oracle, or an admin key, whether you can actually see it happening or not.",
   chapter="Chain abstraction", kicker="The one sentence this reduces to", lines=["Genuinely convenient. And every hidden layer is a real dependency.", "Exactly like a bridge, oracle, or admin key. Whether you can see it or not."], sub="This module's own dependency map still applies, even when the chain itself is hidden from view.")

# ---------------------------------------------------------------- worked example
sc("title", "Worked example.", chapter="Worked example", eyebrow="Worked example", num="1", title="$30,000 USDC, Arbitrum to Base",
   sub="The source material's own scenario.")
sc("compare", "Here's the actual choice, laid out fully, for genuinely moving thirty thousand dollars of U.S.D.C. from Arbitrum to Base. A canonical route, through Ethereum itself, takes two separate transactions, is genuinely slower, and costs more in gas. A reputable fast bridge instead costs somewhere between five and fifteen dollars, and takes just minutes.",
   chapter="Worked example",
   left={"label": "Canonical, via Ethereum", "tone": "good", "items": ["Two transactions, genuinely slower", "Higher gas; the safest available path"]},
   right={"label": "A reputable fast bridge", "tone": "warn", "items": ["$5-$15, and just minutes", "Relies on that bridge's own liquidity"]})
sc("statement", "Worth naming the third option too, an exchange, since it's a genuinely real choice for this exact amount. Withdraw directly on Base, specifically checking first that your exchange actually supports U.S.D.C. on both of those networks, before you ever deposit a single dollar into it.",
   chapter="Worked example", kicker="The third option: an exchange", lines=["Withdraw directly on Base.", "Check first that it supports USDC on both networks."], sub="A real, genuine option. Worth the same up-front check, every time.")
sc("steps", "Here's exactly how to actually execute this, step by step, regardless of which specific route you ultimately choose. Send fifty dollars first, by your chosen route, as a genuine test. Keep roughly five dollars of E.T.H. on Base specifically for gas, before you send anything else at all. And only then send the remaining balance, once that small test has actually confirmed successfully.",
   chapter="Worked example", title="Executing it, regardless of route",
   steps=["Send $50 first, by the chosen route, as a genuine test", "Keep ~$5 of ETH on Base for gas, before sending more", "Only then send the remaining balance"], result="A test amount, a gas float, then the rest. Every single time")
sc("quiz", "Quick check. What's genuinely the first step, on any new route, regardless of the amount involved? [[pause 4]] The answer: send a small test amount first, before committing the full balance to it.",
   chapter="Worked example", n=3, of=3, q="First step on any new route?",
   a="Send a small test amount.")

# ---------------------------------------------------------------- checklist and recap
sc("statement", "Worth being concrete about what recording the route actually looks like, in practice, rather than leaving it as a vague habit. A single line is genuinely enough: the date, the amount, the route you actually chose, and the fee and time it actually took. That real record is exactly what tells you, months later, which route genuinely worked well, and which one to actually avoid next time.",
   chapter="Checklist", kicker="What recording the route actually looks like", lines=["A single line: date, amount, route, fee, time.", "Tells you, months later, which route actually worked."], sub="A genuinely small habit, that pays off the next time you need to decide.")
sc("steps", "Here's your checklist. Do it before moving real value between chains. Keep a genuine gas float on every chain you actually use, at all times. Choose your route by its actual trust model and the amount involved, never just by whichever one looks fastest. And send a real test amount first, every time, recording the route you actually used in your own journal.",
   chapter="Checklist", title="Your checklist",
   steps=["Gas float on every chain I use", "Route chosen by trust model and size, not just speed", "Test amount first; route recorded"])
sc("bullets", "Let's recap. Gas stranding means holding tokens with no gas token to move them; a small float on every chain prevents it entirely. Four real routes exist: canonical, fast bridge, exchange, and intent-based, each with a genuinely different trade-off. Chain abstraction is genuinely convenient, but every layer it hides, smart accounts, paymasters, solvers, is still a real dependency. And on any real amount: a gas float first, a test transaction, then the rest, recorded in your own journal.",
   chapter="Recap", title="Recap", check=False,
   items=["Gas stranding: no gas token to move real tokens — a float prevents it", "Four routes: canonical, fast bridge, exchange, intent-based",
          "Chain abstraction is convenient; every hidden layer is still a real dependency", "Gas float, test transaction, then the rest — recorded, every time"])
sc("statement", "Worth closing on how directly this lesson actually builds on two others already covered in this module. The route choice here is the exact same trust-model question from Lesson five point one's bridges, and operating on a new chain safely is the exact same habit from Lesson five point six's ecosystems, now simply applied together, in the same real decision.",
   chapter="Recap", kicker="How this builds on two earlier lessons", lines=["The route choice: the same trust-model question as bridges.", "Operating safely: the same habit from other ecosystems, applied together."], sub="Not new rules. The same rules, now used together in one real decision.")
sc("cta", "Keep a gas float everywhere, choose your route deliberately, and always send a test amount first. Next up, Lesson five point eight: reading smart-contract code, enough to verify claims.",
   "Keep a gas float everywhere, choose your route deliberately, and always send a test amount first. Next up, Lesson 5.8: reading smart-contract code, enough to verify claims.",
   chapter="Recap", button="Next: Lesson 5.8", sub="Reading smart-contract code: enough to verify claims")

spec = {"id": "lesson-05-7", "title": "Lesson 5.7: Operating across chains — gas, routes & chain abstraction", "size": [1920, 1080], "group": "lessons", "maxMinutes": 25,
        "tag": "Lesson 5.7", "gold": True, "music": True, "musicLevel": 0.14, "seed": 85,
        "use": "Lesson 5.7 page in the Whop course. Hand-written gold-standard script: gas stranding, the four route choices, chain abstraction and its hidden dependencies, and the source material's own $30,000 Arbitrum-to-Base worked example, as walk-throughs.",
        "thumbnail": {"title": "Operating across chains", "subtitle": "Lesson 5.7"}, "scenes": S}
out = ROOT / "video-scripts" / "gold" / "lesson-05-7.json"
out.write_text(json.dumps(spec, indent=1, ensure_ascii=False))
words = sum(len(s["vo"].replace("[[pause 4]]", "").split()) for s in S)
print(f"{len(S)} scenes, {words} words, est {(words / 171 * 60 + len(S) * 1.3 + 4 * 3) / 60:.1f} min")
