#!/usr/bin/env python3
"""Gold-standard script for Lesson 1.1, What DeFi is, and the risk-first mindset
(about 12-15 minutes). Replaces the pre-gold-pass-2 script from commit 6669bbe,
which predates the chart-variant/ticker/chart3d-line visual layer added in
1e2d691. Teaches the six-layer DeFi stack (a flow3d recreation of the module's
own defi-stack.png, plus a glossary ticker for all six layers), the three
properties that make DeFi powerful and dangerous, a chart3d anchor on how
composability stacks dependencies, the risk-first rule, and the "12% APY"
worked example.

Writes video-scripts/gold/lesson-01-1.json (the generator skips lessons with a
gold script). Every illustrative number is labelled as an example on screen
and in the narration. Spoken text (vo) spells numbers and abbreviations for
the voice; cap is the written caption, same sentences."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
S = []


def sc(type_, vo, cap=None, **k):
    d = {"type": type_, **k, "vo": vo}
    if cap:
        d["cap"] = cap
    S.append(d)


D = "assets/diagrams/"

# ---------------------------------------------------------------- why it matters
sc("title", "Lesson one point one. What DeFi is, and the risk-first mindset. By the end, you'll be able to describe the DeFi stack, and explain why every yield is payment for a risk, whether or not the website mentions it.",
   chapter="Why it matters", eyebrow="Lesson 1.1", num="1.1", title="What DeFi is, and the risk-first mindset", sub="Every yield is payment for a risk.")
sc("statement", "Here's the shift this lesson makes. DeFi replaces intermediaries, banks, brokers, exchanges, with smart contracts: public programs on a blockchain that hold assets and follow fixed rules. Nobody's judgment sits in the middle. That's exactly what makes it powerful, and exactly what makes it dangerous. That absence of a middleman means something very practical, too: there's no support line to call if a transaction does something you didn't intend, and no manager who can reverse it. Every protection you'd normally get from an institution has to come from your own habits instead, which is exactly why this module exists.",
   "Here's the shift this lesson makes. DeFi replaces intermediaries, banks, brokers, exchanges, with smart contracts: public programs on a blockchain that hold assets and follow fixed rules. Nobody's judgment sits in the middle. That's exactly what makes it powerful, and exactly what makes it dangerous. That absence of a middleman means something very practical, too: there's no support line to call if a transaction does something you didn't intend, and no manager who can reverse it. Every protection you'd normally get from an institution has to come from your own habits instead, which is exactly why this module exists.",
   chapter="Why it matters", kicker="Why it matters", lines=["Smart contracts replace intermediaries.", "No support line. No manager to call."], sub="Every protection now comes from your own habits.")
sc("pillars", "Here's the plan. First, the DeFi stack, six layers, bottom to top. Second, three properties that make it powerful and dangerous, at the same time. Third, the risk-first rule: name what you could lose before you compare returns. And finally, a real worked example, a pool advertising twelve percent, and the five questions it should raise.",
   "Here's the plan. First, the DeFi stack, six layers, bottom to top. Second, three properties that make it powerful and dangerous, at the same time. Third, the risk-first rule: name what you could lose before you compare returns. And finally, a real worked example, a pool advertising 12%, and the five questions it should raise.",
   chapter="Why it matters", title="What this lesson covers",
   items=[{"icon": "layers", "title": "The DeFi stack", "text": "Six layers, bottom to top"}, {"icon": "alert", "title": "Powerful and dangerous", "text": "Three properties, both at once"},
          {"icon": "target", "title": "The risk-first rule", "text": "Name the risk before the return"}, {"icon": "coins", "title": "A worked example", "text": "A 12% pool, five questions"}])

# ---------------------------------------------------------------- the defi stack
sc("title", "The DeFi stack.", chapter="The DeFi stack", eyebrow="The DeFi stack", num="6", title="Six layers, bottom to top",
   sub="Each one a different place things can go wrong.")
sc("flow3d", "Here's the stack, simplified to its core idea. The chain settles every transaction. Your wallet holds the keys and signs. The app is the smart contract itself, doing the swapping, lending or staking. And your position is what you actually hold, and what it risks. Every yield you'll ever see pays for something in this chain.",
   chapter="The DeFi stack", title="The DeFi stack, simplified",
   nodes=[{"label": "Chain", "sub": "Settles every transaction", "icon": "layers"}, {"label": "Wallet", "sub": "Holds your keys and signs", "icon": "wallet"},
          {"label": "App", "sub": "Smart contracts: swap, lend, stake", "icon": "grid"}, {"label": "Position", "sub": "What you hold, and what it risks", "icon": "target"}])
sc("ticker", "In full, it's six layers. The blockchain records every balance and transaction. Smart contracts are the protocol logic itself, a lending market, an exchange pool. Tokens are the assets those contracts move. Wallets are where you hold keys and sign actions. Interfaces are websites that build transactions for you, a convenience, not the protocol. And data layers, explorers and dashboards, let you verify what actually happened.",
   chapter="The DeFi stack", title="The six layers, in full",
   items=[{"label": "Blockchain", "value": "Records every transaction"}, {"label": "Smart contracts", "value": "The protocol logic itself"}, {"label": "Tokens", "value": "Assets the contracts move"},
          {"label": "Wallets", "value": "Where you hold your keys"}, {"label": "Interfaces", "value": "Build transactions for you"}, {"label": "Data layers", "value": "Verify what happened"}])
sc("bullets", "Here's why memorising six layers actually matters: each one is also a place something specific can go wrong. The chain can reorg, go down, or get congested. Contracts can contain bugs, or be upgraded in ways that don't favour you. Tokens can lose their peg. Wallets can be compromised or phished. Interfaces can be spoofed. And data layers can simply be misread, or wrong. Six layers, six distinct failure modes.",
   chapter="The DeFi stack", title="Six layers, six failure modes",
   items=["Chain: can reorg, stall, or get congested", "Contracts: can contain bugs, or be upgraded against you", "Tokens: can lose their peg", "Wallets: can be compromised or phished", "Interfaces: can be spoofed", "Data layers: can be misread, or simply wrong"])
sc("statement", "One layer deserves special attention: the interface. A website is not the protocol. It's a convenience that builds transactions for you, nothing more. Interfaces can be faked, compromised, or simply wrong, while the underlying contracts keep working exactly as written.",
   chapter="The DeFi stack", kicker="A website is not the protocol", lines=["An interface only builds transactions.", "It can be faked. The contracts still run."], sub="This exact distinction is one of this lesson's quiz questions.")

# ---------------------------------------------------------------- powerful and dangerous
sc("title", "Powerful and dangerous.", chapter="Powerful and dangerous", eyebrow="Powerful and dangerous", num="3", title="Three properties, both at once",
   sub="Self-custody · Composability · Transparency")
sc("compare", "Three properties define DeFi, and each one cuts both ways. Self-custody means nobody can freeze your funds; it also means nobody can recover them if something goes wrong. Composability means protocols plug into each other, making powerful products; it also means a position can fail because of something it merely depends on. And transparency means you can verify everything on-chain; it doesn't mean any of it is safe.",
   chapter="Powerful and dangerous", title="Self-custody, composability, transparency",
   left={"label": "The upside", "tone": "good", "items": ["Nobody can freeze your funds", "Protocols combine into powerful products", "Everything is verifiable, on-chain"]},
   right={"label": "The same property, reversed", "tone": "bad", "items": ["Nobody can recover them either", "A position inherits what it depends on", "Verifiable isn't the same as safe"]})
sc("statement", "You've already met self-custody in practice, back in Lesson zero point four. An exchange can freeze a withdrawal; a wallet only you control cannot be frozen by anyone else, for any reason. DeFi runs entirely on that second kind of custody, by design, not by accident.",
   "You've already met self-custody in practice, back in Lesson 0.4. An exchange can freeze a withdrawal; a wallet only you control cannot be frozen by anyone else, for any reason. DeFi runs entirely on that second kind of custody, by design, not by accident.",
   chapter="Powerful and dangerous", kicker="Not a new idea", lines=["Lesson 0.4's exchange-vs-wallet distinction.", "DeFi runs entirely on the wallet side."], sub="By design, not by accident.")
sc("flow", "Here's roughly how a composability failure actually cascades, so it isn't just an abstract word. A price oracle reports a manipulated, momentarily wrong price. A lending contract, built to trust that oracle completely, acts on it anyway. Positions get liquidated that never should have been. And the losses land on real depositors, who did nothing wrong except depend on that same oracle. Lesson five point three covers oracle manipulation properly.",
   "Here's roughly how a composability failure actually cascades, so it isn't just an abstract word. A price oracle reports a manipulated, momentarily wrong price. A lending contract, built to trust that oracle completely, acts on it anyway. Positions get liquidated that never should have been. And the losses land on real depositors, who did nothing wrong except depend on that same oracle. Lesson 5.3 covers oracle manipulation properly.",
   chapter="Powerful and dangerous", title="How a dependency failure cascades",
   nodes=[{"label": "An oracle reports a bad price", "sub": "Manipulated, even if briefly", "icon": "alert", "tone": "bad"}, {"label": "A lending contract trusts it anyway", "sub": "That's what it was built to do", "icon": "grid", "tone": "bad"},
          {"label": "Positions get wrongly liquidated", "sub": "Through no fault of their own", "icon": "coins", "tone": "bad"}, {"label": "Real depositors carry the loss", "sub": "For depending on that same oracle", "icon": "users", "tone": "bad"}],
   edges=[{"from": "0", "to": "1", "tone": "bad"}, {"from": "1", "to": "2", "tone": "bad"}, {"from": "2", "to": "3", "tone": "bad"}])
sc("statement", "This isn't a hypothetical pattern, either. Oracle manipulation causing incorrect liquidations is a well-documented category of real DeFi exploits, not a rare edge case. It's precisely why serious protocols spend so much engineering effort on oracle design, and why Lesson five point three treats it as a subject on its own.",
   "This isn't a hypothetical pattern, either. Oracle manipulation causing incorrect liquidations is a well-documented category of real DeFi exploits, not a rare edge case. It's precisely why serious protocols spend so much engineering effort on oracle design, and why Lesson 5.3 treats it as a subject on its own.",
   chapter="Powerful and dangerous", kicker="Not hypothetical", lines=["A well-documented category of real exploits.", "Not a rare edge case."], sub="Why serious protocols invest so heavily in oracle design.")
sc("chart3d", "Here's composability, made concrete, purely as an illustration of how dependencies stack. Simply holding a token depends on one thing: the chain itself. A basic lending deposit depends on three: the chain, the lending contract, and the price oracle it relies on. And a leveraged position across multiple protocols can depend on five or more: the chain, several contracts, an oracle, and often a bridge. More layers, more yield, usually more places for something to go wrong.",
   chapter="Powerful and dangerous", kind="bars", title="How many things a position depends on",
   sub="Illustrative examples, not a formula",
   bars=[{"label": "Holding a token", "text": "Just the chain itself", "value": 1, "show": "1 dependency"}, {"label": "A basic lending deposit", "text": "Chain, contract, oracle", "value": 3, "show": "3 dependencies"},
         {"label": "A leveraged, multi-protocol position", "text": "Chain, contracts, oracle, bridge", "value": 5, "show": "5+ dependencies", "tone": "bad"}])
sc("statement", "That's the real cost of composability: every extra layer you depend on is an extra way to lose money that has nothing to do with your own decisions. Transparency lets you see all of it, but seeing a risk and avoiding it are two very different things.",
   chapter="Powerful and dangerous", kicker="Seeing it isn't avoiding it", lines=["Every layer is an extra way to lose money.", "Transparency lets you see it. Not avoid it."], sub="That's exactly why the next rule exists.")

# ---------------------------------------------------------------- the risk-first rule
sc("title", "The risk-first rule.", chapter="The risk-first rule", eyebrow="The risk-first rule", num="1", title="Name the risk, before the return",
   sub="One sentence, before any deposit.")
sc("statement", "Here's the whole rule, in one sentence. Before comparing returns, list what could make you lose money. A higher yield means you're being paid to carry more risk, whether or not the website ever mentions it. If you can't name the risk, you haven't actually evaluated the return.",
   chapter="The risk-first rule", kicker="The risk-first rule", lines=["List what could make you lose money.", "Before you ever compare returns."], sub="A higher yield means more risk, mentioned or not.")
sc("compare", "Try it on a familiar shape of comparison. An ordinary savings product paying a modest rate is boring precisely because its risk is well understood and, in many places, insured. A DeFi pool paying several times that on the same kind of dollar carries no such insurance, and probably several dependencies from the stack you just saw. The extra yield isn't free. It's the price of everything this lesson just described.",
   chapter="The risk-first rule", title="A familiar comparison",
   left={"label": "A modest, insured rate", "tone": "neutral", "items": ["Well understood risk", "Boring, by design"]},
   right={"label": "Several times that, on the same dollar", "tone": "bad", "items": ["No such insurance", "Several dependencies from the stack"]})
sc("statement", "You'll apply this exact rule constantly from here on. Stablecoin risk gets its own lesson, one point five. Oracle risk gets its own lesson, five point three. Protocol due diligence gets an entire lesson, six point one. This single mental model, name the risk before the return, is what most of the rest of this program actually builds on.",
   "You'll apply this exact rule constantly from here on. Stablecoin risk gets its own lesson, 1.5. Oracle risk gets its own lesson, 5.3. Protocol due diligence gets an entire lesson, 6.1. This single mental model, name the risk before the return, is what most of the rest of this program actually builds on.",
   chapter="The risk-first rule", kicker="Where this rule shows up again", lines=["1.5 stablecoins · 5.3 oracles · 6.1 due diligence.", "Most of this program builds on this one rule."], sub="Name the risk before the return. That's the model.")

# ---------------------------------------------------------------- a worked example
sc("title", "A worked example.", chapter="A worked example", eyebrow="A worked example", num="12", title="A pool advertising 12%",
   sub="Five questions, before a single dollar moves.")
sc("steps", "Here's the worked example. A pool advertises twelve percent A.P.Y. on a stablecoin, purely as an illustration. Before depositing, ask five things. Where does the twelve percent actually come from: borrowers paying interest, trading fees, or a reward token? Which stablecoin is it, and what actually backs it, the subject of Lesson one point five? Which contracts hold the money, and who has the power to upgrade them? Is there a bridge or a price oracle quietly involved? And how do you withdraw, and could withdrawals ever be blocked?",
   "Here's the worked example. A pool advertises 12% APY on a stablecoin, purely as an illustration. Before depositing, ask five things. Where does the 12% actually come from: borrowers paying interest, trading fees, or a reward token? Which stablecoin is it, and what actually backs it, the subject of Lesson 1.5? Which contracts hold the money, and who has the power to upgrade them? Is there a bridge or a price oracle quietly involved? And how do you withdraw, and could withdrawals ever be blocked?",
   chapter="A worked example", title="Five questions, before you deposit",
   steps=["Where does the 12% actually come from?", "Which stablecoin, and what backs it?", "Which contracts hold the money, and who can upgrade them?", "Is a bridge or oracle involved?", "How do you withdraw, and could it be blocked?"],
   result="If you can't answer these, you don't know what the 12% is paying you for.")
sc("compare", "Here's the difference between an answer that actually tells you something, and one that doesn't. A real answer sounds specific: borrowers pay a base rate, the rest is a temporary reward token that will taper off on a known schedule. A red flag sounds like reassurance instead of information: just trust the protocol, it's always worked. Vague and permanent-sounding is exactly the shape a bad answer takes.",
   chapter="A worked example", title="A real answer, versus a red flag",
   left={"label": "A real answer", "tone": "good", "items": ["Specific: rates, sources, a schedule", "Checkable against the contracts"]},
   right={"label": "A red flag", "tone": "bad", "items": ["“Just trust the protocol”", "Vague, and permanent-sounding"]})
sc("statement", "Notice what this exercise actually is. It isn't cynicism about DeFi. It's the same due diligence a bank loan officer runs before approving a rate, just done by you, because here, nobody else is going to do it on your behalf.",
   chapter="A worked example", kicker="Not cynicism. Due diligence.", lines=["The same due diligence a loan officer runs.", "Except here, nobody does it for you."], sub="That's the trade self-custody makes.")

# ---------------------------------------------------------------- checklist and quiz
sc("title", "Checklist and quiz.", chapter="Checklist and quiz", eyebrow="Checklist and quiz", num="3", title="Confirm you've got it",
   sub="Three boxes, five questions.")
sc("bullets", "Here's this lesson's checklist. You can name the six layers of the DeFi stack, without looking them up. You can explain why self-custody cuts both ways, in one sentence. And before any yield, you ask yourself: what am I actually being paid to risk?",
   chapter="Checklist and quiz", title="Before you move on", numbered=True,
   items=["Can name the six layers of the DeFi stack", "Can explain why self-custody cuts both ways", "Before any yield: “what am I being paid to risk?”"])
sc("quiz", "Question one. Why can composability increase risk? [[pause 4]] The answer: a position inherits the failure risk of every protocol, asset, oracle and bridge it depends on, not just its own.",
   chapter="Checklist and quiz", n=1, of=5, q="Why can composability increase risk?", a="A position inherits the failure risk of everything it depends on.")
sc("quiz", "Question two. Is a website the same thing as the protocol? [[pause 4]] The answer: no. The interface only builds transactions. The contracts are the actual protocol, and interfaces can be faked or compromised.",
   chapter="Checklist and quiz", n=2, of=5, q="Is a website the same thing as the protocol?", a="No. The interface only builds transactions; the contracts are the protocol.")
sc("quiz", "Question three. What's the risk-first mindset, in one sentence? [[pause 4]] The answer: identify what could make you lose money, before you ever compare returns.",
   chapter="Checklist and quiz", n=3, of=5, q="What is the risk-first mindset, in one sentence?", a="Identify what could make you lose money before you compare returns.")
sc("quiz", "Question four. A pool offers a much higher yield than everywhere else. What should that immediately tell you? [[pause 4]] The answer: that you're being paid to carry more risk somewhere, whether or not it's obvious yet.",
   chapter="Checklist and quiz", n=4, of=5, q="A pool offers a much higher yield than everywhere else. What does that tell you?", a="You're being paid to carry more risk somewhere, whether it's obvious yet or not.")
sc("quiz", "Question five. What does self-custody take away, in exchange for nobody being able to freeze your funds? [[pause 4]] The answer: nobody can recover them for you either, if something goes wrong.",
   chapter="Checklist and quiz", n=5, of=5, q="What does self-custody take away, in exchange for nobody freezing your funds?", a="Nobody can recover them for you either, if something goes wrong.")

# ---------------------------------------------------------------- recap and next
sc("flow", "Here's the whole lesson, recapped as one loop. Know the stack, chain, wallet, app, position. Remember the interface isn't the protocol. Name what composability adds you depend on. Verify, don't just trust, because transparency isn't safety. And always ask what you're being paid to risk, before comparing any return.",
   chapter="Recap and next", title="This lesson, recapped as one loop", layout="cycle",
   nodes=[{"label": "Know the stack", "icon": "layers"}, {"label": "The interface isn't the protocol", "icon": "eye"}, {"label": "Name what you depend on", "icon": "grid"},
          {"label": "Verify, don't just trust", "icon": "search"}, {"label": "Ask what you're risking", "icon": "target"}])
sc("statement", "This is education, not financial advice, and every number in this lesson, the 12%, the dependency counts, is illustrative. No yield in DeFi is guaranteed, and none of it is risk-free; it's always payment for something.",
   chapter="Recap and next", kicker="A reminder", lines=["Every number here is illustrative.", "No yield is guaranteed. It's payment for something."], sub="Not financial advice.")
sc("cta", "That's what DeFi is, and the risk-first mindset: the six-layer stack, three properties that cut both ways, and naming your risk before your return. Next, Lesson one point two: how a transaction actually happens.",
   chapter="Recap and next", button="Next: Lesson 1.2", sub="How a transaction actually happens")

spec = {"id": "lesson-01-1", "title": "Lesson 1.1: What DeFi is, and the risk-first mindset", "size": [1920, 1080], "group": "lessons", "maxMinutes": 25, "tag": "Lesson 1.1",
        "gold": True, "seed": 111,
        "use": "Lesson 1.1 page in the Whop course. Gold-standard script: a flow3d recreation of the module's own defi-stack.png anchor, a 6-layer glossary ticker, a chart3d anchor on how composability stacks dependencies, the risk-first rule, and the 12% APY worked example.",
        "thumbnail": {"title": "What DeFi is, risk-first", "subtitle": "Lesson 1.1"}, "scenes": S}
out = ROOT / "video-scripts" / "gold" / "lesson-01-1.json"
out.write_text(json.dumps(spec, indent=1, ensure_ascii=False))
words = sum(len(s["vo"].replace("[[pause 4]]", "").split()) for s in S)
print(f"{len(S)} scenes, {words} words, est {(words / 171 * 60 + len(S) * 1.3 + 5 * 3) / 60:.1f} min")
