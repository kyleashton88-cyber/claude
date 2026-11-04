#!/usr/bin/env python3
"""Gold-standard script for Lesson 1.1, What DeFi is, and the risk-first mindset
(about 12-14 minutes). Teaches the six-layer DeFi stack, the three properties that
make DeFi powerful and dangerous (self-custody, composability, transparency), the
risk-first rule, and the "12% APY" worked example, with animated flows and charts.

Writes video-scripts/gold/lesson-01-1.json (the generator skips lessons with a gold
script). Spoken text (vo) spells numbers for the voice; cap is the written caption,
same sentence count as vo."""
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
sc("title", "Lesson one point one. What DeFi is, and the risk-first mindset. By the end, you'll be able to name every layer of the DeFi stack, and ask the one question that matters before any yield: what am I being paid to risk?",
   "Lesson 1.1. What DeFi is, and the risk-first mindset. By the end, you'll be able to name every layer of the DeFi stack, and ask the one question that matters before any yield: what am I being paid to risk?",
   chapter="Intro", eyebrow="Lesson 1.1", num="1.1", title="What DeFi is, and the risk-first mindset", sub="The stack, the trade-offs, and the one question before any yield.")
sc("pillars", "Here's the plan. First, what DeFi actually replaces, and the six layers underneath every app you'll ever use. Second, the three properties that make DeFi both powerful and dangerous. Third, the risk-first rule. And finally, a full worked example: a pool advertising twelve percent A.P.Y., and the five questions you ask before you believe it.",
   "Here's the plan. First, what DeFi actually replaces, and the six layers underneath every app you'll ever use. Second, the three properties that make DeFi both powerful and dangerous. Third, the risk-first rule. And finally, a full worked example: a pool advertising 12% APY, and the five questions you ask before you believe it.",
   chapter="Intro", title="What this lesson covers",
   items=[{"icon": "layers", "title": "The six-layer stack", "text": "What sits under every DeFi app"}, {"icon": "grid", "title": "Powerful & dangerous", "text": "Self-custody, composability, transparency"},
          {"icon": "target", "title": "Risk-first", "text": "List the risk before the return"}, {"icon": "search", "title": "A worked example", "text": "A 12% APY pool, checked properly"}])

# ---------------------------------------------------------------- the stack
sc("title", "The DeFi stack.", chapter="The DeFi stack", eyebrow="The DeFi stack", num="6", title="Six layers, bottom to top",
   sub="What DeFi actually replaces.")
sc("statement", "Start with what DeFi replaces. Banks, brokers and exchanges are intermediaries: companies that sit in the middle of a financial transaction. DeFi replaces them with smart contracts: public programs on a blockchain that hold assets and follow fixed rules, for everyone, the same way, every time.",
   chapter="The DeFi stack", kicker="What DeFi replaces", lines=["Banks, brokers, exchanges.", "With public, fixed-rule programs."], sub="Smart contracts hold assets and follow the same rules for everyone.")
sc("flow", "Here's the stack, bottom to top. The blockchain records every balance and transaction. Smart contracts are the protocol logic: a lending market, an exchange pool. Tokens are the assets those contracts move. Your wallet is where you hold the keys and sign actions. The interface is the website that builds transactions for you, a convenience, not the protocol itself. And data layers, explorers and dashboards, are how you verify what actually happened.",
   chapter="The DeFi stack", title="The DeFi stack, bottom to top",
   nodes=[{"label": "Blockchain", "sub": "Records every balance and transaction", "icon": "layers"}, {"label": "Smart contracts", "sub": "The protocol logic itself", "icon": "code"},
          {"label": "Tokens", "sub": "The assets the contracts move", "icon": "coins"}, {"label": "Wallet", "sub": "You hold the keys, you sign", "icon": "wallet"},
          {"label": "Interface", "sub": "Builds transactions for you", "icon": "globe"}, {"label": "Data layers", "sub": "Explorers, dashboards: verify it", "icon": "eye"}])
img(D + "tx-lifecycle.png", "A preview of the bottom layer",
    "A quick preview, because it matters for the whole stack above it. The blockchain layer isn't abstract: every action you take, in every layer above it, ultimately becomes a transaction that goes through this exact life cycle. You'll get the full picture in Lesson one point two. For now, just notice that “the blockchain records it” isn't a metaphor. It's the layer everything else sits on.",
    "A quick preview, because it matters for the whole stack above it. The blockchain layer isn't abstract: every action you take, in every layer above it, ultimately becomes a transaction that goes through this exact life cycle. You'll get the full picture in Lesson 1.2. For now, just notice that “the blockchain records it” isn't a metaphor. It's the layer everything else sits on.",
    chapter="The DeFi stack")
sc("statement", "Notice where the interface sits. It's a convenience, not the protocol. A website can go down, get hacked, or be faked entirely, and the underlying contracts keep running exactly as written. That's also why a fake website is such an effective scam: it looks identical, but it's not the layer that actually holds your money.",
   chapter="The DeFi stack", kicker="One layer to watch", lines=["The interface isn't the protocol.", "It's a convenience that can be faked."], sub="The contracts are what actually hold and move your money.")
sc("quiz", "Quick check. Is a DeFi website the same thing as the protocol it represents? [[pause 4]] The answer: no. The interface only builds transactions for you. The smart contracts are the protocol, and interfaces can be faked or compromised without touching the contracts at all.",
   chapter="The DeFi stack", n=1, of=4, q="Is a DeFi website the same thing as the protocol it represents?",
   a="No. The interface only builds transactions. The contracts are the protocol, and interfaces can be faked or compromised.")

# ---------------------------------------------------------------- powerful and dangerous
sc("title", "Powerful and dangerous.", chapter="Powerful and dangerous", eyebrow="Powerful and dangerous", num="3", title="Three properties, both ways",
   sub="Self-custody · Composability · Transparency")
sc("compare", "Property one: self-custody. In a bank, the bank can freeze your account, and the bank can also help you recover it if something goes wrong. In your own DeFi wallet, nobody can freeze your funds. Nobody can recover them for you either. It's the same trade-off from Module Zero, and it's worth repeating here because this whole module is built around it.",
   chapter="Powerful and dangerous",
   title="A bank account vs your own wallet", left={"label": "A bank account", "tone": "neutral", "items": ["The bank can freeze it", "The bank can help you recover it"]},
   right={"label": "Your own DeFi wallet", "tone": "good", "items": ["Nobody can freeze it", "Nobody can recover it for you, either"]})
sc("stats", "One sobering number on self-custody, from outside research, not this program. Blockchain-analytics researchers have estimated that somewhere around a fifth of all bitcoin ever mined sits in wallets that are effectively lost: forgotten passwords, discarded hard drives, seed phrases nobody can find anymore. Nobody can recover it. Nobody can freeze it either. Same coin, both directions, permanently.",
   "One sobering number on self-custody, from outside research, not this program. Blockchain-analytics researchers have estimated that somewhere around a fifth of all bitcoin ever mined sits in wallets that are effectively lost: forgotten passwords, discarded hard drives, seed phrases nobody can find anymore. Nobody can recover it. Nobody can freeze it either. Same coin, both directions, permanently.",
   chapter="Powerful and dangerous", stats=[["≈ 1 in 5", "bitcoin estimated permanently lost (outside research, illustrative)"]])
sc("flow", "Property two: composability. DeFi protocols plug into each other, like building blocks. A stablecoin can be deposited into a lending market. The interest-bearing receipt from that lending market can be deposited into a yield vault. That vault's shares can be used as collateral somewhere else. Composability is what makes DeFi powerful, letting small pieces combine into complex products. It's also why one position can fail because of something several layers away that it quietly depends on.",
   chapter="Powerful and dangerous", title="Composability: blocks plugged into blocks",
   nodes=[{"label": "Stablecoin", "sub": "Deposited into...", "icon": "coins"}, {"label": "Lending market", "sub": "Its receipt goes into...", "icon": "bank"},
          {"label": "Yield vault", "sub": "Its shares become...", "icon": "grid"}, {"label": "Collateral elsewhere", "sub": "One failure, several layers down, reaches here", "icon": "alert"}])
sc("statement", "Property three: transparency. Every DeFi transaction and every contract's code can be checked by anyone, for free, on a block explorer. That's genuinely powerful. But transparent doesn't mean safe. A contract can be fully visible and still contain a bug, an admin key that can change the rules, or economics that only work while a subsidy lasts. Transparency gives you the ability to check. It doesn't check for you.",
   chapter="Powerful and dangerous", kicker="Property three", lines=["Transparent doesn't mean safe.", "It means checkable."], sub="A visible contract can still have a bug, an admin key, or a subsidy that runs out.")
sc("statement", "Here's a real example of composability biting, not a hypothetical. In May of two thousand twenty-two, during the collapse of the Terra ecosystem, a liquid staking token called stETH briefly traded below the value of the ETH it represented, on the open market, even though it was still redeemable one-to-one over time. Protocols that had accepted stETH as collateral, several layers away from Terra itself, felt real stress from an event that, on the surface, had nothing to do with them.",
   chapter="Powerful and dangerous", kicker="A real example", lines=["May 2022: Terra's collapse", "stressed stETH markets, layers away."], sub="A position can feel an event it has no obvious connection to.")
sc("quiz", "Quick check. Why can composability increase risk, even in a position that looks simple on the surface? [[pause 4]] The answer: a position inherits the failure risk of every protocol, asset, oracle and bridge it depends on, even the ones you can't see from the front end.",
   chapter="Powerful and dangerous", n=2, of=4, q="Why can composability increase risk, even in a position that looks simple?",
   a="A position inherits the failure risk of every protocol, asset, oracle and bridge it depends on — even ones you can't see from the front end.")

# ---------------------------------------------------------------- risk-first rule
sc("title", "The risk-first rule.", chapter="The risk-first rule", eyebrow="The risk-first rule", num="1", title="One rule, before every yield",
   sub="List the risk before you compare the return.")
sc("statement", "Apply that rule to the stETH example from a moment ago. A risk-first operator, before ever depositing stETH as collateral anywhere, would have asked: what happens to this position if stETH trades below ETH on the open market, even briefly? That single question, asked in advance, is the entire difference between being surprised by an event and having already sized for it.",
   chapter="The risk-first rule", kicker="Applying it", lines=["“What if stETH trades below ETH?”", "Asked in advance, not after."], sub="The whole difference between surprised and already sized for it.")
sc("statement", "Here's the rule this whole program is built on. Before comparing returns, list what could make you lose money. A higher yield means you're being paid to carry more risk, whether or not the website mentions it. If you can't name the risk, you don't understand the yield, no matter how good the number looks.",
   chapter="The risk-first rule", kicker="The rule", lines=["List the risk", "before you compare the return."], sub="A higher yield means you're paid to carry more risk, named or not.")

sc("compare", "Here's the difference between the two mindsets, side by side. Return-first starts with the number, asks how to get more of it, and treats risk as a footnote to check later, if ever. Risk-first starts with what could go wrong, sizes the position around that answer, and only then looks at whether the remaining return is worth it. Same opportunity. Completely different order of operations.",
   chapter="The risk-first rule",
   title="Return-first vs risk-first", left={"label": "Return-first", "tone": "bad", "items": ["Starts with the number", "Risk is a footnote, checked later", "Sizes around the opportunity"]},
   right={"label": "Risk-first", "tone": "good", "items": ["Starts with what could go wrong", "Sizes the position around that", "Then checks if the return is worth it"]})
sc("flow", "Here's what asking the question actually looks like, step by step. You see a yield. You ask what could make it fail, before anything else. You name every risk you can find: contract, oracle, bridge, peg. You size the position so that if you're wrong, it doesn't matter much. And only then do you deposit, or decide not to.",
   chapter="The risk-first rule", title="The risk-first rule, as a habit",
   nodes=[{"label": "See a yield", "icon": "chart"}, {"label": "Ask what fails", "sub": "Before anything else", "icon": "search"}, {"label": "Name every risk", "sub": "Contract, oracle, bridge, peg", "icon": "alert"},
          {"label": "Size for being wrong", "sub": "So it doesn't matter much", "icon": "target"}, {"label": "Then decide", "sub": "Deposit, or don't", "icon": "check"}])

# ---------------------------------------------------------------- worked example
sc("title", "Worked example.", chapter="Worked example", eyebrow="Worked example", num="12%", title="A pool advertises 12% APY on a stablecoin",
   sub="Five questions, before you deposit a cent.")
img(D + "profit-sources.png", "Question one: where does it come from?",
    "Question one, and the most important: where does the twelve percent actually come from? Every DeFi return is a mix of five sources. Service fees, paid by traders. Interest, paid by borrowers. Security rewards, for staking. Structural carry, like funding and basis. And incentives: emissions or points, which are only real once you've sold them. If the answer is “incentives,” that twelve percent has an expiry date.",
    "Question one, and the most important: where does the 12% actually come from? Every DeFi return is a mix of five sources. Service fees, paid by traders. Interest, paid by borrowers. Security rewards, for staking. Structural carry, like funding and basis. And incentives: emissions or points, which are only real once you've sold them. If the answer is “incentives,” that 12% has an expiry date.",
    chapter="Worked example")
sc("chart", "So let's actually decompose an example twelve percent, the way an operator would. Say two percent comes from real trading fees. One percent from real borrower interest. And the remaining nine percent, the biggest slice by far, from a reward token being emitted to attract deposits. That nine percent only exists while the emissions keep flowing, and it's only real once you've sold the reward token for something else. The headline number and the durable number are two very different things.",
   "So let's actually decompose an example 12%, the way an operator would. Say 2% comes from real trading fees. 1% from real borrower interest. And the remaining 9%, the biggest slice by far, from a reward token being emitted to attract deposits. That 9% only exists while the emissions keep flowing, and it's only real once you've sold the reward token for something else. The headline number and the durable number are two very different things.",
   chapter="Worked example", kind="donut", title="Decomposing an example 12% APY", sub="Illustrative — every pool's mix is different", center="12%", centerSub="headline APY",
   segs=[{"label": "Trading fees", "text": "Real, durable", "value": 2, "show": "2%", "tone": "good"}, {"label": "Borrower interest", "text": "Real, durable", "value": 1, "show": "1%", "tone": "good"},
         {"label": "Reward-token emissions", "text": "Only real once sold; can stop anytime", "value": 9, "show": "9%", "tone": "bad"}],
   note="9 of the 12 points only exist while the emissions keep flowing.")
sc("bullets", "And four more questions, before you deposit. Which stablecoin, and what actually backs it? You'll learn to judge that properly in Lesson one point five. Which contracts hold the money, and who can upgrade them? Is there a bridge or an oracle involved, each one another thing that can fail? And how do you withdraw, and could withdrawals ever be blocked? If you can't answer these five questions, you don't know what the twelve percent is paying you for.",
   "And four more questions, before you deposit. Which stablecoin, and what actually backs it? You'll learn to judge that properly in Lesson 1.5. Which contracts hold the money, and who can upgrade them? Is there a bridge or an oracle involved, each one another thing that can fail? And how do you withdraw, and could withdrawals ever be blocked? If you can't answer these five questions, you don't know what the 12% is paying you for.",
   chapter="Worked example", title="Four more questions before you deposit", numbered=True,
   items=["Which stablecoin, and what backs it? (Lesson 1.5)", "Which contracts hold the money, and who can upgrade them?", "Is a bridge or an oracle involved?", "How do you withdraw — and could it be blocked?"])
sc("quiz", "One more. If nine of a pool's twelve percent A.P.Y. comes from a reward token being emitted, what should you assume about that nine percent? [[pause 4]] The answer: it's not durable. It only exists while the emissions continue, and it's only real once you've actually sold the reward token.",
   "One more. If 9 of a pool's 12% APY comes from a reward token being emitted, what should you assume about that 9%? [[pause 4]] The answer: it's not durable. It only exists while the emissions continue, and it's only real once you've actually sold the reward token.",
   chapter="Worked example", n=3, of=4, q="If 9 of a pool's 12% APY comes from emitted reward tokens, what should you assume about that 9%?",
   a="It's not durable — it only exists while emissions continue, and it's only real once you've sold the reward token.")
sc("quiz", "Last check. In one sentence, what is the risk-first mindset? [[pause 4]] The answer: identify what could make you lose money, before you compare returns.",
   chapter="Worked example", n=4, of=4, q="In one sentence, what is the risk-first mindset?",
   a="Identify what could make you lose money before you compare returns.")

# ---------------------------------------------------------------- checklist and recap
sc("bullets", "Here's your checklist. Do it now, for real. First, you can name the six layers of the DeFi stack. Second, you can explain why self-custody cuts both ways. And third, before any yield, you ask: what am I being paid to risk?",
   chapter="Checklist", title="Your checklist", numbered=True,
   items=["Name the six layers of the DeFi stack", "Explain why self-custody cuts both ways", "Before any yield: “what am I being paid to risk?”"])
sc("bullets", "Let's recap. DeFi replaces intermediaries with smart contracts, across six layers: blockchain, contracts, tokens, wallet, interface and data layers. Self-custody, composability and transparency make it both powerful and dangerous. And the risk-first rule: list what could make you lose money, before you ever compare returns.",
   chapter="Recap", title="Recap", check=False,
   items=["DeFi replaces intermediaries with smart contracts, six layers deep", "Self-custody, composability, transparency: powerful and dangerous",
          "Risk-first: list the risk before you compare the return"])
sc("cta", "Do the checklist now, before you move on. You now have the whole lesson in your head: the six-layer stack, the three properties that make DeFi powerful and dangerous, the risk-first rule, and how to actually decompose a headline yield. Next up, Lesson one point two: How a transaction actually happens.",
   "Do the checklist now, before you move on. You now have the whole lesson in your head: the six-layer stack, the three properties that make DeFi powerful and dangerous, the risk-first rule, and how to actually decompose a headline yield. Next up, Lesson 1.2: How a transaction actually happens.",
   chapter="Recap", button="Next: Lesson 1.2", sub="How a transaction actually happens")

spec = {"id": "lesson-01-1", "title": "Lesson 1.1: What DeFi is, and the risk-first mindset", "size": [1920, 1080], "group": "lessons", "maxMinutes": 25,
        "tag": "Lesson 1.1", "gold": True, "music": True, "musicLevel": 0.14, "seed": 43,
        "use": "Lesson 1.1 page in the Whop course. Hand-written gold-standard script: the six-layer DeFi stack, self-custody/composability/transparency, risk-first rule, worked APY example.",
        "thumbnail": {"title": "The risk-first mindset", "subtitle": "Lesson 1.1"}, "scenes": S}
out = ROOT / "video-scripts" / "gold" / "lesson-01-1.json"
out.write_text(json.dumps(spec, indent=1, ensure_ascii=False))
words = sum(len(s["vo"].replace("[[pause 4]]", "").split()) for s in S)
print(f"{len(S)} scenes, {words} words, est {(words / 171 * 60 + len(S) * 1.3 + 4 * 3) / 60:.1f} min")
