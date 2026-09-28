#!/usr/bin/env python3
"""Gold-standard script for Lesson 1.2, How a transaction actually happens
(about 12-15 minutes). Replaces the pre-gold-pass-2 script from commit
d35f1ac, which predates the chart-variant/ticker/chart3d-line visual layer
added in 1e2d691. Teaches the transaction lifecycle (a flow3d recreation of
the module's own tx-lifecycle.png), gas/gwei/nonce/finality as a glossary
ticker, the nonce-stuck mechanism, and the source's own $9-vs-$36 congestion
worked example as a chart3d anchor.

Writes video-scripts/gold/lesson-01-2.json (the generator skips lessons with
a gold script). Every illustrative number is labelled as an example on
screen and in the narration. Spoken text (vo) spells numbers and
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


EX = "Example gas price and ETH price · costs move with both"

# ---------------------------------------------------------------- why it matters
sc("title", "Lesson one point two. How a transaction actually happens. By the end, you'll be able to follow a transaction from signature to finality, and estimate what it actually costs.",
   chapter="Why it matters", eyebrow="Lesson 1.2", num="1.2", title="How a transaction actually happens", sub="From your signature to a point of no return.")
sc("statement", "Here's why this lesson earns its place early. Every single action in this entire program, every swap, every deposit, every approval, is a transaction. If you don't know what's happening between clicking sign and seeing it confirmed, every other lesson is asking you to trust a black box.",
   chapter="Why it matters", kicker="Why it matters", lines=["Every action in this program is a transaction.", "Not knowing the steps means trusting a black box."], sub="This lesson opens the box.")
sc("pillars", "Here's the plan. First, the full lifecycle, from signature to finality. Second, gas, gwei and nonce, the mechanics behind every fee. Third, a real worked example: the same swap, costing four times as much, just because the network got busy. And finally, your checklist and a quiz.",
   chapter="Why it matters", title="What this lesson covers",
   items=[{"icon": "key", "title": "The lifecycle", "text": "Signature to finality"}, {"icon": "cog", "title": "Gas, gwei, nonce", "text": "The mechanics behind every fee"},
          {"icon": "coins", "title": "A worked example", "text": "The same swap, 4x the cost"}, {"icon": "check", "title": "Checklist and quiz", "text": "Confirm you've got it"}])

# ---------------------------------------------------------------- the lifecycle
sc("title", "The lifecycle.", chapter="The lifecycle", eyebrow="The lifecycle", num="4", title="Sign to finality",
   sub="Four stages. Only the last one is irreversible.")
sc("flow3d", "Here's the journey. You sign the transaction in your wallet, which cryptographically proves it's really you. Your wallet then broadcasts it, sending that signed transaction out to the network's nodes, fast and automatic, but worth naming, since it's the exact moment it leaves your device. It sits in the mempool, a public waiting area every node can see, until a validator picks it up. A validator includes it in a block, and the network confirms that block happened. And eventually, it reaches finality: the point after which it can't realistically be reversed. Gas is paid whether it succeeds or fails.",
   chapter="The lifecycle", title="A transaction's life",
   nodes=[{"label": "Sign", "sub": "Your wallet signs it", "icon": "key"}, {"label": "Mempool", "sub": "Waiting, publicly visible", "icon": "clock"},
          {"label": "Block", "sub": "A validator includes it", "icon": "layers"}, {"label": "Finality", "sub": "Now irreversible", "icon": "check"}])
sc("statement", "Notice that middle stage. While a transaction sits in the mempool, it's genuinely public: anyone running specialised software can see it coming and act before it confirms. That single fact is the entire basis of Lesson two point five, protecting your trades from exactly that.",
   "Notice that middle stage. While a transaction sits in the mempool, it's genuinely public: anyone running specialised software can see it coming and act before it confirms. That single fact is the entire basis of Lesson 2.5, protecting your trades from exactly that.",
   chapter="The lifecycle", kicker="The mempool is public", lines=["Anyone can see a pending transaction.", "And act on it, before it confirms."], sub="The entire basis of Lesson 2.5.")
sc("statement", "And notice finality isn't a fixed universal number. It differs chain by chain, and Layer twos have their own rules entirely, the subject of Module five. In practice, 'confirmed' isn't a single instant either. Most wallets and exchanges wait for several blocks to pass before treating a transaction as safe, more for a large amount, fewer for a small one. That buffer exists because very early blocks can, rarely, get reorganised.",
   "And notice finality isn't a fixed universal number. It differs chain by chain, and Layer 2s have their own rules entirely, the subject of Module 5. In practice, 'confirmed' isn't a single instant either. Most wallets and exchanges wait for several blocks to pass before treating a transaction as safe, more for a large amount, fewer for a small one. That buffer exists because very early blocks can, rarely, get reorganised.",
   chapter="The lifecycle", kicker="Finality isn't universal", lines=["It differs, chain by chain.", "Waiting for several blocks is the practical version."], sub="More blocks for a larger amount. Fewer for a small one.")

# ---------------------------------------------------------------- gas, gwei and nonce
sc("title", "Gas, gwei and nonce.", chapter="Gas, gwei and nonce", eyebrow="Gas, gwei and nonce", num="5", title="The words behind every fee",
   sub="Five words, all doing real work.")
sc("ticker", "Gas is simply the unit of computation; cost equals gas used, multiplied by gas price. On Ethereum that price splits into a base fee, which is burned, and a priority tip, to get included sooner. Gas price is quoted in gwei, where one gwei equals one billionth of an E.T.H. Your nonce is your account's own transaction counter, in strict order. The mempool is where a transaction waits, publicly, before a block. And finality is the point after which it can't realistically be reversed.",
   "Gas is simply the unit of computation; cost equals gas used, multiplied by gas price. On Ethereum that price splits into a base fee, which is burned, and a priority tip, to get included sooner. Gas price is quoted in gwei, where one gwei equals one billionth of an ETH. Your nonce is your account's own transaction counter, in strict order. The mempool is where a transaction waits, publicly, before a block. And finality is the point after which it can't realistically be reversed.",
   chapter="Gas, gwei and nonce", title="Five words, all doing real work",
   items=[{"label": "Gas", "value": "Gas used × gas price"}, {"label": "Gwei", "value": "1 gwei = 0.000000001 ETH"}, {"label": "Nonce", "value": "Your account's tx counter"},
          {"label": "Mempool", "value": "Waiting, publicly visible"}, {"label": "Finality", "value": "The point of no return"}])
sc("statement", "One of these deserves special attention: the nonce. Transactions from one account must confirm strictly in order. So a single stuck transaction at a low nonce blocks every transaction you send after it, no matter how much gas those later ones offer. The fix is a replacement: same nonce, higher fee, sent again.",
   chapter="Gas, gwei and nonce", kicker="Why a stuck transaction blocks everything", lines=["One stuck nonce blocks every later one.", "The fix: same nonce, higher fee."], sub="Not a bug. It's how ordering is enforced.")
sc("flow", "Here's exactly how that gets unstuck, step by step. A low-nonce transaction gets stuck, its fee too low for current conditions. Every transaction you send after it queues up silently behind it, waiting. Nothing confirms, no matter how much you offer on the newer ones. And the fix is a replacement transaction: the identical nonce, a meaningfully higher fee, which releases the whole queue once it confirms.",
   chapter="Gas, gwei and nonce", title="Unsticking a stuck nonce",
   nodes=[{"label": "A low-nonce transaction gets stuck", "sub": "Its fee too low for current conditions", "icon": "alert"}, {"label": "Later transactions queue silently behind it", "sub": "No matter how much they offer"},
          {"label": "Nothing confirms, for any of them", "sub": "Ordering is enforced strictly", "icon": "clock"}, {"label": "Replace: same nonce, higher fee", "sub": "Releases the whole queue", "icon": "check"}])
sc("statement", "Here's how that actually plays out, purely as an illustration. Sam sends three transactions in quick succession: a swap, an approval, then another swap. The middle one, the approval, gets stuck with too low a fee. The third transaction, even though it's a completely different action, simply cannot confirm until that stuck approval does, because the network enforces the exact order Sam's account sent them in.",
   chapter="Gas, gwei and nonce", kicker="A stuck nonce, in practice", lines=["Three transactions, sent in order.", "The third waits on the stuck second, regardless."], sub="Illustrative example of how ordering actually bites.")
sc("statement", "Split the fee open, and it's really two pieces. The base fee is set by the network itself, and it's burned, destroyed, not paid to anyone. The priority tip is what you add on top, paid directly to whoever includes your transaction, to get it in sooner. Raise the tip, and you're not paying more for the same service, you're bidding to jump the queue.",
   chapter="Gas, gwei and nonce", kicker="What the fee is actually made of", lines=["Base fee: burned, not paid to anyone.", "Priority tip: a bid to jump the queue."], sub="Raising the tip doesn't buy more. It buys sooner.")
sc("compare", "Here's a detail that surprises almost everyone the first time. A transaction that reverts, fails, still costs gas. The network did the actual computation either way; it only refunds the gas it didn't need to spend. Success or failure changes the result. It doesn't change whether you paid.",
   chapter="Gas, gwei and nonce", title="Succeeds, or reverts: you still pay",
   left={"label": "Succeeds", "tone": "good", "items": ["The network did the work", "Gas is spent", "You get the intended result"]},
   right={"label": "Reverts", "tone": "bad", "items": ["The network did the work anyway", "Gas is still spent", "You get nothing for it"]})
sc("statement", "These five words aren't specific to this one lesson. Gas appears in literally every transaction from here on, in every module. Nonce issues show up any time you send several transactions in quick succession. And mempool visibility is the entire subject of protecting your trades, properly, in Lesson two point five. Learn them once, here, and you won't need to relearn them.",
   "These five words aren't specific to this one lesson. Gas appears in literally every transaction from here on, in every module. Nonce issues show up any time you send several transactions in quick succession. And mempool visibility is the entire subject of protecting your trades, properly, in Lesson 2.5. Learn them once, here, and you won't need to relearn them.",
   chapter="Gas, gwei and nonce", kicker="Where these words show up again", lines=["Gas: every transaction, every module.", "Mempool visibility: all of Lesson 2.5."], sub="Learn them once, here.")

# ---------------------------------------------------------------- a worked example
sc("title", "A worked example.", chapter="A worked example", eyebrow="A worked example", num="4", title="The same swap, 4 times the cost",
   sub="Nothing changed except how busy the network was.")
sc("steps", "Here's the maths, worked through in full. Start with a typical swap: about a hundred and fifty thousand gas. Multiply by the gas price, twenty gwei: a hundred and fifty thousand times twenty is three million gwei. Convert to E.T.H.: three million gwei is naught point naught naught three E.T.H. And convert to dollars, with E.T.H. at three thousand: that's nine dollars, for the whole swap.",
   "Here's the maths, worked through in full. Start with a typical swap: about 150,000 gas. Multiply by the gas price, 20 gwei: 150,000 × 20 is 3,000,000 gwei. Convert to ETH: 3,000,000 gwei is 0.003 ETH. And convert to dollars, with ETH at $3,000: that's $9, for the whole swap.",
   chapter="A worked example", title="The maths, step by step",
   steps=["150,000 gas (a typical swap)", "× 20 gwei = 3,000,000 gwei", "= 0.003 ETH", "× $3,000/ETH = $9 total"],
   result="$9, for a swap that felt instant.")
sc("chart3d", "Now here's the exact same swap, same hundred and fifty thousand gas, during network congestion, at eighty gwei instead of twenty. Four times the gas price. One hundred and fifty thousand times eighty is twelve million gwei, naught point naught one two E.T.H., thirty-six dollars. Nothing about your transaction changed. Only the network's mood did.",
   chapter="A worked example", kind="bars", title="The same swap: normal vs. congested",
   sub=EX,
   bars=[{"label": "Normal (20 gwei)", "text": "150,000 gas", "value": 9, "show": "$9", "tone": "good"}, {"label": "Congested (80 gwei)", "text": "Same 150,000 gas", "value": 36, "show": "$36", "tone": "bad"}])
sc("statement", "Now put that next to a small reward. If you're compounding, say, a dollar fifty of accumulated rewards, and it costs nine dollars, or thirty-six during congestion, just to claim them, the gas costs more than the reward itself. That's precisely why position size matters once you're operating on-chain.",
   chapter="A worked example", kicker="Why position size matters", lines=["Claiming $1.50 of rewards for $9 in gas.", "The fee can cost more than the reward."], sub="Position size isn't a detail. It's the whole economics.")
sc("compare", "Here's that same nine-dollar fee, against two very different position sizes, purely as an illustration. Against a ten-thousand-dollar position, nine dollars is under one tenth of one percent, barely noticeable. Against a ten-dollar position, that same nine dollars is ninety percent of the whole amount. The fee doesn't change. Only what it's a percentage of does.",
   chapter="A worked example", title="The same $9 fee, two position sizes",
   left={"label": "A $10,000 position", "tone": "good", "items": ["$9 gas ≈ 0.09%", "Barely noticeable"]},
   right={"label": "A $10 position", "tone": "bad", "items": ["$9 gas = 90%", "Nearly the whole amount"]})
sc("statement", "One more habit worth building here: an explorer, like Etherscan, shows you the status, fee, sender, contract called, and every token transfer for any transaction, yours or anyone else's. Lesson seven point two covers reading one properly; for now, know that it exists, and that it doesn't lie.",
   "One more habit worth building here: an explorer, like Etherscan, shows you the status, fee, sender, contract called, and every token transfer for any transaction, yours or anyone else's. Lesson 7.2 covers reading one properly; for now, know that it exists, and that it doesn't lie.",
   chapter="A worked example", kicker="Explorers don't lie", lines=["Status, fee, sender, every transfer.", "Yours, or anyone else's."], sub="Lesson 7.2 covers reading one properly.")
sc("steps", "Here's specifically what an explorer shows you, for any transaction. Its status: pending, success, or failed. The fee actually paid, to the cent. The sender, and which contract it called. And every single token transfer that happened inside it, in and out. All of it public, all of it checkable, whether it's your own transaction or someone else's.",
   chapter="A worked example", title="What an explorer actually shows you",
   steps=["Status: pending, success, or failed", "The fee actually paid, to the cent", "Sender, and the contract called", "Every token transfer, in and out"],
   result="All of it public. All of it checkable.")

# ---------------------------------------------------------------- checklist and quiz
sc("title", "Checklist and quiz.", chapter="Checklist and quiz", eyebrow="Checklist and quiz", num="3", title="Confirm you've got it",
   sub="Three boxes, three questions.")
sc("bullets", "Here's this lesson's checklist. You check the fee estimate before signing, every time. You know how to find your transaction on an explorer. And you know a stuck transaction can be sped up or cancelled, using the same nonce with a higher fee.",
   chapter="Checklist and quiz", title="Before you move on", numbered=True,
   items=["Check the fee estimate before signing", "Know how to find a transaction on an explorer", "Know a stuck transaction can be replaced: same nonce, higher fee"])
sc("quiz", "Question one. Your transaction reverted. Did you pay? [[pause 4]] The answer: yes. You pay for the gas used up to the point of failure; the network still did that computation.",
   chapter="Checklist and quiz", n=1, of=5, q="Your transaction reverted. Did you pay?", a="Yes, for the gas used up to the point of failure.")
sc("quiz", "Question two. Two hundred thousand gas, at ten gwei, with E.T.H. at twenty-five hundred dollars. What does it cost? [[pause 4]] The answer: two million gwei, naught point naught naught two E.T.H., which is five dollars.",
   "Question two. 200,000 gas, at 10 gwei, with ETH at $2,500. What does it cost? [[pause 4]] The answer: 2,000,000 gwei, 0.002 ETH, which is $5.",
   chapter="Checklist and quiz", n=2, of=5, q="200,000 gas at 10 gwei, ETH at $2,500. What's the cost?", a="2,000,000 gwei = 0.002 ETH = $5.")
sc("quiz", "Question three. Why are all your newer transactions stuck as pending? [[pause 4]] The answer: an earlier, lower nonce is stuck. Replace or speed it up, and every transaction behind it confirms.",
   chapter="Checklist and quiz", n=3, of=5, q="Why are your newer transactions all pending?", a="An earlier nonce is stuck. Replace or speed it up, and the rest follow.")
sc("quiz", "Question four. Does an unconfirmed transaction in the mempool stay private until it lands in a block? [[pause 4]] The answer: no. The mempool is public; anyone can see it waiting, and potentially act on it first.",
   chapter="Checklist and quiz", n=4, of=5, q="Does an unconfirmed transaction stay private until it's in a block?", a="No. The mempool is public; anyone can see it waiting.")
sc("quiz", "Question five. You're compounding one dollar fifty of rewards, and gas costs nine dollars. Should you claim now? [[pause 4]] The answer: probably not yet. The fee costs more than the reward; wait until the position, or the reward, has grown.",
   "Question five. You're compounding $1.50 of rewards, and gas costs $9. Should you claim now? [[pause 4]] The answer: probably not yet. The fee costs more than the reward; wait until the position, or the reward, has grown.",
   chapter="Checklist and quiz", n=5, of=5, q="You're compounding $1.50 of rewards and gas costs $9. Should you claim now?", a="Probably not yet. The fee costs more than the reward.")

# ---------------------------------------------------------------- recap and next
sc("flow", "Here's the whole lesson, recapped as one loop. Sign it. Watch it wait, publicly, in the mempool. See it included in a block. Confirm it's reached finality. Check the fee before any of that happens. And if it's stuck, replace the nonce with a higher fee. Do those things, and you'll never again wonder what's actually happening between clicking sign and seeing it done.",
   chapter="Recap and next", title="This lesson, recapped as one loop", layout="cycle",
   nodes=[{"label": "Check the fee first", "icon": "cog"}, {"label": "Sign", "icon": "key"}, {"label": "Wait, publicly, in the mempool", "icon": "clock"},
          {"label": "Included in a block", "icon": "layers"}, {"label": "Confirmed: finality", "icon": "check"}])
sc("statement", "This is education, not financial advice, and every dollar figure in this lesson, the gas prices, the E.T.H. price, is an illustrative example; real costs move with both, constantly. Nobody from this program will ever ask for your seed phrase, private keys or account access.",
   "This is education, not financial advice, and every dollar figure in this lesson, the gas prices, the ETH price, is an illustrative example; real costs move with both, constantly. Nobody from this program will ever ask for your seed phrase, private keys or account access.",
   chapter="Recap and next", kicker="A reminder", lines=["Every gas figure here is illustrative.", "Real costs move with both prices, constantly."], sub="Not financial advice.")
sc("cta", "That's how a transaction actually happens: sign, mempool, block, finality, and what it really costs along the way. Next, Lesson one point three: wallets, keys, hardware and multisig.",
   chapter="Recap and next", button="Next: Lesson 1.3", sub="Wallets, keys, hardware & multisig")

spec = {"id": "lesson-01-2", "title": "Lesson 1.2: How a transaction actually happens", "size": [1920, 1080], "group": "lessons", "maxMinutes": 25, "tag": "Lesson 1.2",
        "gold": True, "seed": 112,
        "use": "Lesson 1.2 page in the Whop course. Gold-standard script: a flow3d recreation of the module's own tx-lifecycle.png anchor, a 5-word glossary ticker (gas/gwei/nonce/mempool/finality), a stuck-nonce mechanism flow, a succeeds-vs-reverts compare, and the source's own $9-vs-$36 congestion worked example as a chart3d anchor.",
        "thumbnail": {"title": "How a transaction happens", "subtitle": "Lesson 1.2"}, "scenes": S}
out = ROOT / "video-scripts" / "gold" / "lesson-01-2.json"
out.write_text(json.dumps(spec, indent=1, ensure_ascii=False))
words = sum(len(s["vo"].replace("[[pause 4]]", "").split()) for s in S)
print(f"{len(S)} scenes, {words} words, est {(words / 171 * 60 + len(S) * 1.3 + 5 * 3) / 60:.1f} min")
