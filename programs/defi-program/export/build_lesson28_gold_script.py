#!/usr/bin/env python3
"""Gold-standard script for Lesson 2.8, The MEV supply chain (target
10-20 minutes, expert). Walks the full path of a transaction (mempool/
private RPC, searchers/bundles, builders, relays/proposers via
proposer-builder separation), order-flow auctions and rebates, intent
systems, L2 sequencers, and the source material's own worked example
($100,000 swap: ~$1,000 leaked publicly vs no sandwich plus a possible
rebate through a protected RPC), as visual walk-throughs. Closes out
Module 2. Built to the walk-through-first standard: almost every idea is a
flow, steps or callout image, not a statement read over a static screen.

Writes video-scripts/gold/lesson-02-8.json (the generator skips lessons
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
sc("title", "Lesson two point eight. The MEV supply chain. By the end, you'll understand who sees, orders and profits from your transactions, and how to get some of that value back.",
   "Lesson 2.8. The MEV supply chain. By the end, you'll understand who sees, orders and profits from your transactions, and how to get some of that value back.",
   chapter="Intro", eyebrow="Lesson 2.8 · Expert", num="2.8", title="The MEV supply chain", sub="Same trade, very different outcome, decided by where you send it.")
sc("pillars", "Here's the plan. The full path your transaction actually takes, from your wallet to a confirmed block. Order-flow auctions and rebates, and how you can actually get some of that value back. What changes once you're on a layer two, with a single sequencer instead of this whole chain. And a full worked example, showing exactly how differently the same trade can end up.",
   chapter="Intro", title="What this lesson covers",
   items=[{"icon": "layers", "title": "The full path", "text": "Mempool, searchers, builders, proposers"}, {"icon": "coins", "title": "Rebates", "text": "Getting some of that value back"},
          {"icon": "cog", "title": "L2 sequencers", "text": "A single operator changes the dynamics"}, {"icon": "target", "title": "Worked example", "text": "$100,000, sent two different ways"}])

# ---------------------------------------------------------------- the full path
sc("title", "The full path.", chapter="The full path", eyebrow="The full path", num="1", title="Where your transaction actually goes",
   sub="Four stops, before it's ever confirmed.")
sc("flow", "Here's exactly where your transaction goes, step by step, from the moment you sign it. Your wallet sends it, either to the public mempool, visible to everyone, or to a private R.P.C., an M.E.V.-protection endpoint that keeps it hidden. Searchers scan constantly for opportunities, arbitrage, liquidations, backruns, sandwiches, and submit bundles competing to capture them. Builders assemble the most profitable possible block, from all the transactions and bundles available to them.",
   chapter="The full path", title="Steps one through three",
   nodes=[{"label": "Your wallet sends it", "sub": "Public mempool, or a private RPC", "icon": "wallet"}, {"label": "Searchers scan for it", "sub": "Arbitrage, liquidations, backruns, sandwiches", "icon": "eye"},
          {"label": "Submit competing bundles", "sub": "Each one trying to capture the opportunity", "icon": "layers"}, {"label": "Builders assemble a block", "sub": "The most profitable one they can build", "icon": "cog"}])
sc("flow", "And here's the fourth and final stop, before your transaction is actually confirmed. Relays pass completed blocks along to proposers, the validators who actually add a block to the chain. Those proposers simply pick whichever block pays them the most, a system called proposer-builder separation, run through infrastructure called M.E.V.-Boost. Your transaction, wherever it landed in that winning block, is now confirmed, for better or worse.",
   chapter="The full path", title="Step four: relays and proposers",
   nodes=[{"label": "Relays pass blocks along", "sub": "From builders, to proposers", "icon": "swap"}, {"label": "Proposers pick the highest payer", "sub": "Proposer-builder separation, via MEV-Boost", "icon": "coins"},
          {"label": "That block gets added", "sub": "To the chain, confirmed", "icon": "check"}, {"label": "Your transaction's fate", "sub": "Was decided several steps earlier", "icon": "alert"}])
img(D + "mev-supply-chain.png", "The whole chain, in one picture",
    "Here's the entire path, laid out as one picture, worth holding in your head as a single mental model. Your wallet, to the mempool or a private R.P.C. Searchers, submitting bundles. Builders, assembling blocks. Relays, passing them to proposers. Every one of those five stops is a separate party, each one capable of seeing, and acting on, your pending transaction before it confirms.",
    chapter="The full path")
sc("stats", "One real number, so this whole chain isn't abstract. Blockchain researchers have tracked hundreds of millions of dollars in total M.E.V. extracted across Ethereum in a single year, spread across arbitrage, liquidations and sandwich attacks combined. This is outside research, not this program's own data, but it's the actual scale of the supply chain this lesson just walked through.",
   chapter="The full path", stats=[["$100Ms+/yr", "total MEV extracted across Ethereum, tracked (outside research)"]])
sc("quiz", "Quick check. What do builders actually do, in this chain? [[pause 4]] The answer: they assemble the most profitable possible block, out of the available transactions and searcher bundles, to earn the right to have it chosen by a proposer.",
   chapter="The full path", n=1, of=3, q="What do builders actually do, in this chain?",
   a="Assemble the most profitable block from transactions and searcher bundles.")

# ---------------------------------------------------------------- rebates and intents
sc("title", "Getting value back.", chapter="Rebates", eyebrow="Rebates", num="2", title="Order-flow auctions and MEV rebates",
   sub="Some of that value can come back to you.")
sc("flow", "Here's how an M.E.V. rebate actually works, mechanically, since “getting value back” can sound abstract otherwise. Some private R.P.C.s and wallets let searchers bid directly for the right to backrun your transaction, the harmless kind of M.E.V., not a sandwich. The highest bidder wins that right. And a share of what they bid gets refunded straight back to you, the sender, simply for having routed through that R.P.C.",
   chapter="Rebates", title="How an MEV rebate actually works",
   nodes=[{"label": "Searchers bid to backrun you", "sub": "The harmless kind of MEV, not a sandwich", "icon": "coins"}, {"label": "Highest bidder wins the right", "sub": "An order-flow auction, run by the RPC", "icon": "target"},
          {"label": "A share gets refunded", "sub": "Back to you, the original sender", "icon": "check"}, {"label": "Just for routing through it", "sub": "No extra action required from you", "icon": "shield"}])
sc("statement", "Worth connecting this directly to Lesson two point six, since intent-based trading solves a related problem from a different angle. Intent systems move the entire competition to solvers, before your transaction even exists as a signed transaction at all, often with M.E.V. protection built into the system itself. A protected R.P.C. with rebates protects an existing transaction. An intent system changes how the trade happens in the first place.",
   chapter="Rebates", kicker="How this connects to Lesson 2.6", lines=["Intents move competition to solvers,", "before a signed transaction even exists."], sub="One protects an existing transaction. The other changes how the trade happens.")
sc("steps", "Here's how to actually check whether your own wallet already offers this, since it's often on by default without being named clearly. Open your wallet's network or R.P.C. settings directly. Look for a name like “protected,” “private,” or a specific R.P.C. provider known for M.E.V. protection. And check its own documentation specifically for whether it pays rebates, and how large a share it actually passes back to you.",
   chapter="Rebates", title="Checking your own wallet's RPC",
   steps=["Open your wallet's network / RPC settings", "Look for “protected,” “private,” or a known MEV-protection RPC", "Check its docs for rebates, and what share it pays back"], result="Often on by default — just not named clearly")
sc("compare", "Worth being honest about the actual size of a rebate, so expectations stay realistic. A rebate is a share of a backrun opportunity's value, not a share of your entire trade; it's typically a modest amount, not a meaningful yield on its own. The real value of routing correctly is avoiding the sandwich in the first place, from Lesson two point five. The rebate is a genuine bonus on top of that, not the main event.",
   chapter="Rebates",
   left={"label": "The main value: avoiding the sandwich", "tone": "good", "items": ["The bigger number, by far", "The Lesson 2.5 mechanism, prevented entirely"]},
   right={"label": "The rebate, on top", "tone": "good", "items": ["A share of a backrun opportunity", "A genuine bonus — not the main event"]})
sc("quiz", "Quick check. What is an MEV rebate, specifically? [[pause 4]] The answer: a refund of part of the value searchers bid to win the right to backrun your transaction, paid back to you for routing through a private RPC that offers it.",
   chapter="Rebates", n=2, of=3, q="What is an MEV rebate, specifically?",
   a="A refund of part of the value searchers extract from backrunning your transaction.")

# ---------------------------------------------------------------- l2 sequencers
sc("title", "L2 sequencers.", chapter="L2 sequencers", eyebrow="L2 sequencers", num="3", title="A single operator, ordering everything",
   sub="This whole chain, replaced with one decision-maker.")
sc("compare", "Here's the actual difference worth holding clearly, since an L2 changes almost everything from this lesson. Ethereum mainnet runs the full chain: searchers, builders, relays, proposers, each a separate, competing party. Most layer twos today instead run a single sequencer, one operator, ordering every transaction directly, commonly on a first-come-first-served or a priority-fee basis.",
   chapter="L2 sequencers",
   left={"label": "Ethereum mainnet", "tone": "warn", "items": ["The full chain: searchers, builders, relays, proposers", "Each one, a separate, competing party"]},
   right={"label": "Most L2s, today", "tone": "warn", "items": ["A single sequencer orders everything", "First-come-first-served, or priority fee"]})
sc("flow", "Worth knowing where this is actually heading, since “a single sequencer” isn't necessarily the permanent state of things. Today, most L2s run one operator, ordering everything. Several roadmaps now point toward shared or decentralised sequencing, spreading that same ordering power across multiple parties. And the actual M.E.V. dynamics on any given L2 will keep shifting as that rolls out, worth rechecking periodically, not assumed to be fixed.",
   chapter="L2 sequencers", title="Where sequencer design is actually heading",
   nodes=[{"label": "Today: a single sequencer", "sub": "One operator, ordering everything", "icon": "cog"}, {"label": "Roadmaps: shared / decentralised", "sub": "Spreading that power across parties", "icon": "layers"},
          {"label": "MEV dynamics will shift", "sub": "As that actually rolls out", "icon": "chart"}, {"label": "Worth rechecking", "sub": "Not assumed to be fixed, permanently", "icon": "eye"}])
sc("statement", "Worth being precise about what this actually means for you, practically, on any given L2. It's genuinely worth knowing that specific L2's own ordering rule, since it directly shapes what kind of M.E.V. is even possible there. A single, trusted sequencer removes the multi-party competition this lesson just walked through, but it doesn't automatically remove every form of M.E.V.; it just changes who's positioned to capture it.",
   chapter="L2 sequencers", kicker="What a single sequencer changes", lines=["Removes the multi-party competition.", "Doesn't remove MEV — changes who can capture it."], sub="Know that specific L2's own ordering rule.")

# ---------------------------------------------------------------- worked example
sc("title", "Worked example.", chapter="Worked example", eyebrow="Worked example", num="1", title="$100,000, sent two different ways",
   sub="Same trade. Very different outcome.")
sc("compare", "Here's the same one-hundred-thousand-dollar swap, sent two different ways, with one percent slippage tolerance either way. Sent publicly, to the open mempool: up to roughly one thousand dollars could leak straight to a sandwich bot, exactly the mechanism from Lesson two point five. Sent through a protected R.P.C. with rebates instead: no sandwich reaches it at all, since it was never visible to see.",
   chapter="Worked example",
   left={"label": "Sent publicly (mempool)", "tone": "bad", "items": ["Up to ~$1,000 could leak to a sandwich", "1% slippage, exactly the Lesson 2.5 mechanism"]},
   right={"label": "Sent via protected RPC", "tone": "good", "items": ["No sandwich — never visible to see", "Possibly, a rebate on top"]})
sc("statement", "And here's the part worth naming specifically, since the protected route isn't just “no loss,” it can be a genuine gain. If that same trade happens to create a backrun opportunity, say, an arbitrage between two pools it touches, you may actually receive a share of that value back, through the rebate mechanism from earlier in this lesson. Same trade. Same size. A meaningfully different financial outcome, decided entirely by where you sent it.",
   chapter="Worked example", kicker="Not just “no loss” — a possible gain", lines=["A backrun opportunity: you may get a share back.", "Same trade, same size, decided by where you sent it."], sub="That's the entire lesson, in one comparison.")
sc("quiz", "Quick check. Sending the exact same $100,000 swap through a protected RPC with rebates, instead of publicly, can result in what, beyond simply avoiding a sandwich? [[pause 4]] The answer: potentially receiving a share of a backrun opportunity's value back, as a rebate, turning a possible loss into a possible small gain.",
   chapter="Worked example", n=3, of=3, q="Sending the same $100,000 swap through a protected RPC, instead of publicly, can result in what, beyond just avoiding a sandwich?",
   a="Potentially receiving a rebate share of a backrun opportunity's value.")

# ---------------------------------------------------------------- checklist and recap
sc("steps", "Here's the actual decision, boiled down to when protection pays off most. It matters most on large trades, where a sandwich's absolute dollar take is largest. It matters most on volatile pairs, where backrun opportunities, and rebate value, show up most often. And it matters least on tiny, routine trades, where neither the risk nor the potential rebate is large enough to change much either way.",
   chapter="Worked example", title="When protection actually pays off most",
   steps=["Large trades: biggest absolute sandwich risk", "Volatile pairs: more backrun opportunity, more rebate value", "Tiny, routine trades: neither risk nor rebate is large"], result="Scale your attention to the trade's actual size")
sc("steps", "Here's your checklist. Do it now, before your next large trade. Large trades go through a protected R.P.C., an intent system, or an aggregator with M.E.V. protection built in, not the open mempool. You know specifically whether your own wallet's R.P.C. offers rebates. And you understand your own L2's sequencer ordering rules, since they're not the same everywhere.",
   chapter="Checklist", title="Your checklist",
   steps=["Large trades: protected RPC, intent system, or MEV-protected aggregator", "Know whether your wallet's RPC offers rebates", "Understand your L2's specific sequencer ordering rules"])
sc("statement", "One last thing worth naming, closing out this entire module. Every lesson in Module Two, price impact, slippage, impermanent loss, L.V.R., sandwich defence, order types, and this exact supply chain, is really one connected skill: knowing the real cost of a trade before you commit to it, from every direction it can come from.",
   chapter="Recap", kicker="Closing out Module 2", lines=["One connected skill, across every lesson.", "Knowing the real cost, before you commit."], sub="From every direction it can come from.")
sc("bullets", "Let's recap. Your transaction passes through the mempool or a private R.P.C., searchers, builders, and relays to proposers, before it's ever confirmed. Order-flow auctions can rebate you a share of the value a backrun opportunity creates, simply for routing correctly. Most L2s replace that whole chain with a single sequencer, which changes, but doesn't eliminate, M.E.V. dynamics. And the exact same trade, sent two different ways, can produce a meaningfully different financial outcome.",
   chapter="Recap", title="Recap", check=False,
   items=["The full path: mempool/private RPC → searchers → builders → relays/proposers", "Rebates: a share of backrun value, refunded for routing correctly",
          "L2 sequencers: change, don't eliminate, MEV dynamics", "The same trade, sent two ways, can produce very different outcomes"])
sc("cta", "Route large trades through protection, know your wallet's rebate policy, and know your L2's sequencer rules. That's Module Two, complete. Next up, Module Three: Lending and leverage.",
   "Route large trades through protection, know your wallet's rebate policy, and know your L2's sequencer rules. That's Module 2, complete. Next up, Module 3: Lending and leverage.",
   chapter="Recap", button="Next: Module 3", sub="Lending and leverage")

spec = {"id": "lesson-02-8", "title": "Lesson 2.8: The MEV supply chain", "size": [1920, 1080], "group": "lessons", "maxMinutes": 25,
        "tag": "Lesson 2.8", "gold": True, "music": True, "musicLevel": 0.14, "seed": 60,
        "use": "Lesson 2.8 page in the Whop course. Hand-written gold-standard script: the full transaction path (mempool/RPC, searchers, builders, relays/proposers), MEV rebates, L2 sequencers, and the source material's own $100,000 worked example, as walk-throughs. Closes Module 2.",
        "thumbnail": {"title": "The MEV supply chain", "subtitle": "Lesson 2.8 · Expert"}, "scenes": S}
out = ROOT / "video-scripts" / "gold" / "lesson-02-8.json"
out.write_text(json.dumps(spec, indent=1, ensure_ascii=False))
words = sum(len(s["vo"].replace("[[pause 4]]", "").split()) for s in S)
print(f"{len(S)} scenes, {words} words, est {(words / 171 * 60 + len(S) * 1.3 + 4 * 3) / 60:.1f} min")
