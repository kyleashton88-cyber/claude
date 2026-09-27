#!/usr/bin/env python3
"""Gold-standard script for Lesson 5.6, Beyond Ethereum: Solana, Bitcoin
and other ecosystems (target 11-14 minutes, per the "a bit longer" note
for lessons from here on). Walks Solana as a genuinely separate ecosystem
(own wallets, address format, gas token, SPL tokens), Bitcoin in DeFi via
wrapped tokens and each wrapper's own trust model, other ecosystems
(Cosmos/IBC, Move-based chains) and applying this module's own dependency
map to each, and the source material's own worked example (1 BTC to lend
on Ethereum: custodial wrapper, decentralised wrapper, or don't wrap at
all — write each option's trust model, cap wrapped BTC as bridge risk),
as visual walk-throughs. Written in one pass at the full target length
(no separate expansion round).

Writes video-scripts/gold/lesson-05-6.json (the generator skips lessons
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
sc("title", "Lesson five point six. Beyond Ethereum: Solana, Bitcoin, and other ecosystems. By the end, you'll be able to operate safely on non-E.V.M. chains, and understand exactly how Bitcoin actually gets used inside DeFi.",
   "Lesson 5.6. Beyond Ethereum: Solana, Bitcoin and other ecosystems. By the end, you'll be able to operate safely on non-EVM chains, and understand exactly how Bitcoin actually gets used inside DeFi.",
   chapter="Intro", eyebrow="Lesson 5.6", num="5.6", title="Beyond Ethereum: Solana, Bitcoin & other ecosystems", sub="Your Ethereum address simply doesn't work here. Not on any of these.")
sc("pillars", "Here's the plan. Solana, a genuinely separate ecosystem, with its own wallets, its own address format, and its own gas token entirely. Bitcoin in DeFi, and why it's almost always used as a wrapped token, with its own distinct trust model. Other ecosystems, and applying this module's own dependency map to every single one of them. And a full worked example, choosing how to actually lend one bitcoin on Ethereum.",
   chapter="Intro", title="What this lesson covers",
   items=[{"icon": "chart", "title": "Solana", "text": "Its own wallets, address format, and gas token"}, {"icon": "coins", "title": "Bitcoin in DeFi", "text": "Almost always wrapped, each wrapper its own trust model"},
          {"icon": "shield", "title": "Other ecosystems", "text": "Cosmos, Move-based chains — same dependency map applies"}, {"icon": "target", "title": "Worked example", "text": "Lending 1 BTC: three genuinely different options"}])

# ---------------------------------------------------------------- solana
sc("title", "Solana: a genuinely separate ecosystem.", chapter="Solana", eyebrow="Solana", num="1", title="Not an Ethereum variant. An entirely different chain.",
   sub="Your Ethereum address simply doesn't work here.")
img(D + "ecosystem-map.png", "How these ecosystems actually differ",
    "Here's exactly what makes Solana genuinely separate, not simply another Ethereum-compatible chain wearing a different name. It's a high-throughput chain with its own dedicated wallets, like Phantom or Solflare, its own distinct address format entirely, and very low fees, paid specifically in its own native token, SOL, not in Ethereum's own ETH. Its tokens follow their own separate standard, S.P.L., not Ethereum's familiar ERC-20.",
    chapter="Solana")
sc("compare", "Worth being precise about a distinction that trips people up constantly: not every chain outside Ethereum's own mainnet is actually non-E.V.M. Layer twos, like the rollups covered back in Lesson five point two, are still E.V.M.-compatible, meaning your same Ethereum address, and often your same wallet, genuinely works there directly. Solana specifically is different: a genuinely separate, non-E.V.M. architecture, needing its own dedicated wallet entirely.",
   chapter="Solana",
   left={"label": "EVM-compatible L2s", "tone": "good", "items": ["Same Ethereum address, same wallet, usually", "Different network, same address format"]},
   right={"label": "Solana (non-EVM)", "tone": "warn", "items": ["A genuinely separate architecture", "Needs its own dedicated wallet entirely"]})
sc("statement", "Worth being completely direct about the single most important consequence of all this. Your Ethereum address genuinely does not work on Solana, at all, under any circumstances. Sending assets between these two ecosystems specifically requires a bridge, or a centralised exchange, exactly the same category of infrastructure risk covered back in Lesson five point one, just connecting a different pair of chains this time.",
   chapter="Solana", kicker="The single most important consequence", lines=["Your Ethereum address doesn't work on Solana. At all.", "Moving between them needs a bridge, or an exchange."], sub="The same bridge trust-model questions from Lesson 5.1 apply here directly.")
sc("statement", "Worth also naming priority fees specifically, since they're a genuinely distinct Solana concept worth knowing before you transact there. During busy periods, you can pay an additional priority fee, on top of the base fee, specifically to have your transaction processed faster, ahead of others willing to pay less for that same priority.",
   chapter="Solana", kicker="Priority fees", lines=["An additional fee, on top of the base fee, during busy periods.", "Pays for faster processing, ahead of others paying less."], sub="A genuinely Solana-specific concept, worth knowing before you transact.")
sc("quiz", "Quick check. Does your Ethereum address actually work on Solana? [[pause 4]] The answer: no. It's a genuinely different ecosystem, with its own address format and its own dedicated wallets entirely.",
   chapter="Solana", n=1, of=3, q="Does your Ethereum address work on Solana?",
   a="No. It's a different ecosystem with its own address format and wallets.")

# ---------------------------------------------------------------- bitcoin in defi
sc("title", "Bitcoin in DeFi.", chapter="Bitcoin in DeFi", eyebrow="Bitcoin in DeFi", num="1", title="Almost always wrapped. Never natively running DeFi apps.",
   sub="Your \"BTC\" is only as good as whoever actually holds the real BTC.")
sc("flow", "Here's exactly why Bitcoin itself can't simply run a DeFi app directly, and what actually happens instead. Bitcoin's own base layer genuinely doesn't support the kind of smart-contract logic DeFi apps actually need. So B.T.C. gets used instead as a wrapped token, on other chains, backed specifically by a custodian, a group of signers, or a dedicated protocol, or alternatively used through a Bitcoin-specific layer two or sidechain built for exactly this purpose.",
   chapter="Bitcoin in DeFi", title="How BTC actually gets into DeFi",
   nodes=[{"label": "Bitcoin's base layer", "sub": "Doesn't support DeFi-style smart contracts", "icon": "shield"}, {"label": "So: a wrapped token elsewhere", "sub": "Backed by a custodian, signers, or a protocol", "icon": "coins"},
          {"label": "Or: a Bitcoin L2 / sidechain", "sub": "Built specifically for this purpose", "icon": "chart"}])
sc("statement", "Worth being completely precise about the single sentence this entire topic actually reduces to, since it directly echoes this module's own bridge lesson. Your wrapped B.T.C. is only ever as good as whoever actually holds the real Bitcoin backing it, and exactly how you'd genuinely redeem it back. That's the exact same trust-model question from Lesson five point one, just asked about a different specific asset this time.",
   chapter="Bitcoin in DeFi", kicker="The single sentence this reduces to", lines=["Your wrapped BTC is only as good as whoever holds the real BTC.", "The same trust-model question from Lesson 5.1, about a different asset."], sub="Every wrapper has its own trust model. Check it, the same way, every time.")
sc("compare", "Here's what those different backing arrangements actually look like, mechanically, since custodial and decentralised wrapping work in genuinely different ways. A custodial wrapper means one specific company holds the real Bitcoin directly, in its own custody, and mints the wrapped token against it. A decentralised wrapper instead means a broader group of signers, or a protocol's own mechanism, collectively holds and secures that same real Bitcoin.",
   chapter="Bitcoin in DeFi",
   left={"label": "Custodial wrapper", "tone": "warn", "items": ["One company holds the real BTC directly", "Mints the wrapped token against it"]},
   right={"label": "Decentralised wrapper", "tone": "good", "items": ["A broader signer set or protocol holds it", "Collectively secured, not one single party"]})
sc("quiz", "Quick check. What actually determines a wrapped B.T.C. token's real safety? [[pause 4]] The answer: who genuinely holds the real Bitcoin behind it, and exactly how it can actually be redeemed, its own trust model.",
   chapter="Bitcoin in DeFi", n=2, of=3, q="What determines a wrapped BTC token's safety?",
   a="Who holds the real BTC and how it can be redeemed: its trust model.")

# ---------------------------------------------------------------- other ecosystems
sc("title", "Other ecosystems, same dependency map.", chapter="Other ecosystems", eyebrow="Other ecosystems", num="1", title="Cosmos, Move-based chains, and beyond",
   sub="Every one of them gets the same treatment.")
sc("flow", "Here's exactly how to treat any other ecosystem you encounter, whether it's a Cosmos chain connected through I.B.C., a Move-based chain, or something else entirely you haven't seen before. Each one genuinely has its own wallets, its own fee structure, and its own bridges, exactly like Solana and Bitcoin do. And this module's own dependency map, from its very first lesson, applies to every single one of them, without exception.",
   chapter="Other ecosystems", title="Applying the same dependency map",
   nodes=[{"label": "Its own wallets", "sub": "Genuinely different from any you've used before", "icon": "shield"}, {"label": "Its own fee structure", "sub": "A different native gas token, every time", "icon": "coins"},
          {"label": "Its own bridges", "sub": "Each with its own trust model, to check", "icon": "alert"}, {"label": "Same dependency map, every time", "sub": "From this module's own Mastery Starter", "icon": "check"}])
sc("statement", "Worth naming I.B.C. specifically, since it's a genuinely different approach from the bridges covered back in Lesson five point one. I.B.C. lets Cosmos chains communicate through a shared, standardised protocol, rather than each pair of chains needing its own separate, custom bridge built between them. That's a meaningfully different trust model worth understanding on its own terms, not simply assuming it works exactly like the bridges from earlier in this module.",
   chapter="Other ecosystems", kicker="IBC, specifically", lines=["Cosmos chains communicate through a shared, standardised protocol.", "Not each pair needing its own custom bridge."], sub="A genuinely different model. Worth understanding on its own terms.")
sc("statement", "Worth being direct about the actual rules that stay identical, everywhere, regardless of which specific ecosystem you're actually operating in. Use the official wallet, from the official site, every single time. Send a small test transaction first. Confirm you're genuinely on the correct network. And hold that network's own gas token, on hand, before you actually need it.",
   chapter="Other ecosystems", kicker="What stays identical, everywhere", lines=["Official wallet, from the official site. Every time.", "Test transaction first. Correct network confirmed. Gas token on hand."], sub="These four rules don't change, no matter how unfamiliar the ecosystem looks.")
sc("steps", "Here's how to actually verify you're genuinely using the official wallet for a new ecosystem, rather than assuming a top search result is safe. Get the download link directly from the ecosystem's own official documentation or website, never from a search ad. Confirm the wallet's own publisher name matches what that documentation actually states. And send a small test transaction first, exactly like every other lesson in this module has already taught you.",
   chapter="Other ecosystems", title="Verifying the official wallet, for real",
   steps=["Get the link from the ecosystem's own official documentation", "Confirm the wallet publisher matches what that documentation states", "Send a small test transaction first, as always"])
sc("quiz", "Quick check. What's Solana's own native gas token specifically called? [[pause 4]] The answer: SOL.",
   chapter="Other ecosystems", n=3, of=3, q="What's Solana's gas token?",
   a="SOL.")

# ---------------------------------------------------------------- worked example
sc("title", "Worked example.", chapter="Worked example", eyebrow="Worked example", num="1", title="Lending 1 BTC on Ethereum",
   sub="The source material's own scenario.")
sc("compare", "Here's the actual choice, laid out fully, for genuinely lending one bitcoin on Ethereum. A custodial wrapper means trusting one specific company, directly, to actually hold the real B.T.C. behind your wrapped token. A decentralised wrapper instead means trusting a broader signer set, or a protocol's own mechanism, rather than one single company alone.",
   chapter="Worked example",
   left={"label": "Custodial wrapper", "tone": "warn", "items": ["Trust one specific company, directly", "Simpler; concentrated in one party"]},
   right={"label": "Decentralised wrapper", "tone": "good", "items": ["Trust a broader signer set, or a protocol", "Not concentrated in one single company"]})
sc("statement", "Worth naming the third option too, since it's the one most likely to be overlooked entirely. Not wrapping at all means simply keeping your Bitcoin as Bitcoin, forgoing the specific yield this lending opportunity offers, entirely. That's a genuinely legitimate choice, not a failure to act, specifically when neither wrapper's trust model actually satisfies you.",
   chapter="Worked example", kicker="The third option, easily overlooked", lines=["Not wrapping at all: keep it as Bitcoin, forgo the yield.", "A legitimate choice, when neither wrapper satisfies you."], sub="Declining is always on the table. It's not a failure to act.")
sc("steps", "Here's exactly what to actually do with these three options, rather than picking based on the advertised yield alone. Write down each option's own specific trust model, explicitly, in your own words. Cap whatever wrapped B.T.C. exposure you do decide to take, treating it as exactly the same bridge risk covered back in Lesson five point one. And only then compare the actual yield on offer against that fully-priced risk.",
   chapter="Worked example", title="What to actually do",
   steps=["Write down each option's trust model, explicitly", "Cap wrapped BTC exposure as bridge risk (Lesson 5.1)", "Only then compare the yield against that fully-priced risk"], result="The yield means nothing until the trust model is priced in first")

# ---------------------------------------------------------------- checklist and recap
sc("steps", "Here's your checklist. Do it for every non-E.V.M. chain you actually use. Keep a separate, official wallet for each one, specifically. Hold that chain's own gas token on hand, before you actually need it. And know your wrapped-B.T.C. trust model, precisely, and keep that exposure genuinely capped.",
   chapter="Checklist", title="Your checklist",
   steps=["Separate, official wallet for each non-EVM chain I use", "Gas token held on each chain", "Wrapped-BTC trust model known and capped"])
sc("bullets", "Let's recap. Solana is a genuinely separate ecosystem: its own wallets, address format, and gas token; your Ethereum address simply doesn't work there. Bitcoin gets used in DeFi almost entirely as a wrapped token, and that wrapper's real safety comes down to its own trust model, exactly like a bridge. Other ecosystems, Cosmos, Move-based chains, and beyond, all get this same module's own dependency map applied. And the same four rules hold everywhere: official wallet, test transaction, correct network, gas token ready.",
   chapter="Recap", title="Recap", check=False,
   items=["Solana: its own wallets, address format, gas token — a different chain entirely", "Bitcoin in DeFi: almost always wrapped — safety = the wrapper's trust model",
          "Other ecosystems get the same dependency map, every time", "Same four rules everywhere: official wallet, test transaction, correct network, gas ready"])
sc("statement", "Worth closing on the actual point this lesson proves, one more time, since it's easy to think of non-Ethereum chains as an entirely separate topic. Everything this module already taught you, the dependency map, bridge trust models, oracle risk, contract risk, doesn't reset at Ethereum's own edge. It's the same map, applied to unfamiliar territory, not a new set of rules to learn from scratch.",
   chapter="Recap", kicker="The actual point this lesson proves", lines=["This module's own map doesn't reset at Ethereum's edge.", "The same map, applied to unfamiliar territory."], sub="Not a new set of rules. The same rules, somewhere new.")
sc("cta", "Use a separate official wallet per chain, hold each chain's gas token, and know your wrapped-BTC trust model. Next up, Lesson five point seven: operating across chains, gas, routes, and chain abstraction.",
   "Use a separate official wallet per chain, hold each chain's gas token, and know your wrapped-BTC trust model. Next up, Lesson 5.7: operating across chains, gas, routes and chain abstraction.",
   chapter="Recap", button="Next: Lesson 5.7", sub="Operating across chains: gas, routes and chain abstraction")

spec = {"id": "lesson-05-6", "title": "Lesson 5.6: Beyond Ethereum — Solana, Bitcoin & other ecosystems", "size": [1920, 1080], "group": "lessons", "maxMinutes": 25,
        "tag": "Lesson 5.6", "gold": True, "music": True, "musicLevel": 0.14, "seed": 84,
        "use": "Lesson 5.6 page in the Whop course. Hand-written gold-standard script: Solana as a separate ecosystem, Bitcoin in DeFi via wrapped tokens and trust models, applying the dependency map to other ecosystems, and the source material's own 1-BTC-lending worked example, as walk-throughs.",
        "thumbnail": {"title": "Beyond Ethereum", "subtitle": "Lesson 5.6"}, "scenes": S}
out = ROOT / "video-scripts" / "gold" / "lesson-05-6.json"
out.write_text(json.dumps(spec, indent=1, ensure_ascii=False))
words = sum(len(s["vo"].replace("[[pause 4]]", "").split()) for s in S)
print(f"{len(S)} scenes, {words} words, est {(words / 171 * 60 + len(S) * 1.3 + 4 * 3) / 60:.1f} min")
