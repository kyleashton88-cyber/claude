#!/usr/bin/env python3
"""Gold-standard script for Lesson 1.2, How a transaction actually happens
(about 12-14 minutes). Follows a transaction from signature to finality, teaches
gas/gwei/base fee/priority tip, nonces and stuck transactions, and works the
real numbers: 150,000 gas at 20 gwei vs 80 gwei, and the quiz's 200,000 gas
at 10 gwei example, with animated flows and charts.

Writes video-scripts/gold/lesson-01-2.json (the generator skips lessons with a
gold script). Spoken text (vo) spells numbers for the voice; cap is the written
caption, same sentence count as vo."""
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
EX = "Illustrative example — real gas prices move constantly"

# ---------------------------------------------------------------- intro
sc("title", "Lesson one point two. How a transaction actually happens. By the end, you'll be able to follow a transaction from signature to finality, and estimate what it actually costs before you send it.",
   "Lesson 1.2. How a transaction actually happens. By the end, you'll be able to follow a transaction from signature to finality, and estimate what it actually costs before you send it.",
   chapter="Intro", eyebrow="Lesson 1.2", num="1.2", title="How a transaction actually happens", sub="Signature to finality, and what it really costs.")
sc("pillars", "Here's the plan. First, the full lifecycle, every stop a transaction makes between your signature and being irreversible. Second, gas: what it is, and the two parts of its price. Third, the nonce, and why one stuck transaction can jam every one behind it. And finally, the real math: what a swap actually costs, quiet versus congested.",
   chapter="Intro", title="What this lesson covers",
   items=[{"icon": "swap", "title": "The full lifecycle", "text": "Sign to finality, every stop"}, {"icon": "coins", "title": "Gas, explained", "text": "Base fee plus priority tip"},
          {"icon": "layers", "title": "The nonce", "text": "Why one stuck tx jams the rest"}, {"icon": "chart", "title": "The real math", "text": "What a swap actually costs"}])

# ---------------------------------------------------------------- lifecycle
sc("title", "The full lifecycle.", chapter="The full lifecycle", eyebrow="The full lifecycle", num="7", title="Seven stops, sign to finality",
   sub="Every transaction you'll ever send follows this.")
sc("flow", "Here's the complete path. You create the transaction, specifying what it does. You sign it with your private key. Your wallet broadcasts it to the network. It sits in the mempool, a public waiting room, visible to anyone. A validator includes it in a block. The network confirms that block. And after enough confirmations, it reaches finality: the point after which it can't realistically be reversed.",
   chapter="The full lifecycle", title="Create to finality, seven stops",
   nodes=[{"label": "Create", "sub": "You specify what it does", "icon": "doc"}, {"label": "Sign", "sub": "With your private key", "icon": "key"},
          {"label": "Broadcast", "sub": "To the network", "icon": "globe"}, {"label": "Mempool", "sub": "A public waiting room", "icon": "clock"},
          {"label": "In a block", "sub": "A validator includes it", "icon": "layers"}, {"label": "Confirmed", "sub": "The network agrees", "icon": "check"},
          {"label": "Final", "sub": "Can't realistically reverse", "icon": "shield"}])
img(D + "tx-lifecycle.png", "The short version",
    "Here's the short version, the one worth keeping in your head day to day: sign, mempool, block, finality. Gas is paid whether the transaction succeeds or fails, because the network still did the work of checking it. That single fact explains most of what's counterintuitive about how DeFi charges you.",
    chapter="The full lifecycle")
sc("statement", "One more distinction worth holding onto: “pending” and “confirmed” are not the same claim. Pending means the network has seen your transaction and it's waiting in the mempool. Confirmed means it made it into a block. Until it's confirmed, anyone watching the mempool, including a rival bidder, can technically see what you're about to do and try to act first. That's part of why priority tips exist.",
   chapter="The full lifecycle", kicker="Two different words", lines=["Pending: seen, waiting.", "Confirmed: in a block."], sub="A public mempool means others can see it before it confirms.")
sc("statement", "Notice the word “realistically” in finality. On most chains, a transaction can technically still be reorganised for a short window right after confirmation. Waiting for a few more confirmations, or for the finality rules of the specific chain and layer two you're using, which you'll cover in Module Five, is what makes “final” actually mean final.",
   chapter="The full lifecycle", kicker="A precise word", lines=["“Realistically” irreversible,", "not instantly irreversible."], sub="A few more confirmations is what makes “final” mean final.")

# ---------------------------------------------------------------- gas
sc("title", "Gas.", chapter="Gas", eyebrow="Gas", num="2", title="What you're actually paying for",
   sub="Gas used × gas price.")
sc("statement", "Gas is the unit of computation. Every operation a transaction performs, reading a balance, updating a balance, checking a signature, costs a fixed amount of gas. Your total cost is gas used, multiplied by gas price. Both numbers matter, and they move independently.",
   chapter="Gas", kicker="The formula", lines=["Cost = gas used", "× gas price."], sub="Gas used is the computation. Gas price is what you're willing to pay for it.")
sc("flow", "Gas price itself has two parts, on Ethereum. The base fee, set by the network based on how busy it is, and burned, destroyed, not paid to anyone. And the priority tip, an extra amount you add to get included sooner, which does go to the validator. Gas price is quoted in gwei: one gwei is one billionth of an E.T.H.",
   "Gas price itself has two parts, on Ethereum. The base fee, set by the network based on how busy it is, and burned, destroyed, not paid to anyone. And the priority tip, an extra amount you add to get included sooner, which does go to the validator. Gas price is quoted in gwei: one gwei is one billionth of an ETH.",
   chapter="Gas", title="Gas price: two parts",
   nodes=[{"label": "Base fee", "sub": "Set by network congestion. Burned.", "icon": "layers"}, {"label": "+ Priority tip", "sub": "Pays the validator, for speed", "icon": "coins"}, {"label": "= Gas price", "sub": "Quoted in gwei", "icon": "check"}])
sc("statement", "One real pattern worth knowing: priority tips spike hardest during sudden demand, a popular NFT mint, a hyped token launch, everyone racing for the same limited block space at once. That's a real, recurring phenomenon on Ethereum and similar chains, not a rare edge case. If you're not in a race for a scarce, time-limited slot, there's usually no reason to pay the premium everyone else is paying in that moment.",
   chapter="Gas", kicker="A real pattern", lines=["Mints and launches", "spike priority tips hardest."], sub="If you're not racing for a scarce slot, you don't need to pay that premium.")
sc("chart", "Gas price isn't fixed, it's an auction for block space, and it follows real patterns. Weekday business hours in the US and Europe tend to run busier, and so does any period right after major news or a popular new app launching. Quiet periods, like weekends and the middle of the night in those time zones, tend to run cheaper. None of this is guaranteed on any given day, but if a fee looks unusually high, waiting an hour is often free money.",
   "Gas price isn't fixed, it's an auction for block space, and it follows real patterns. Weekday business hours in the US and Europe tend to run busier, and so does any period right after major news or a popular new app launching. Quiet periods, like weekends and the middle of the night in those time zones, tend to run cheaper. None of this is guaranteed on any given day, but if a fee looks unusually high, waiting an hour is often free money.",
   chapter="Gas", kind="line", title="Gas price follows demand", sub="Illustrative pattern, not live data",
   series=[{"values": [22, 18, 15, 24, 31, 42, 38, 33, 40, 52, 60, 55, 46, 50, 44, 36, 28, 24], "tone": "blue"}],
   xlabels=["Mon", "", "Tue", "", "Wed", "", "Thu", "", "Fri", "", "", "Sat", "", "", "Sun", "", "", ""],
   yticks=[[15, "Quiet"], [40, "Typical"], [60, "Busy"]], ymin=10, ymax=65,
   marks=[{"i": 10, "text": "Weekday business hours: busier", "tone": "bad", "below": False}, {"i": 2, "text": "Off-hours: often cheaper", "tone": "good", "below": True}])
sc("quiz", "Quick check. Your transaction fails and reverts. Did you still pay for it? [[pause 4]] The answer: yes, for the gas used up to the point of failure. The network did the computation, even though the result didn't go through.",
   chapter="Gas", n=1, of=4, q="Your transaction fails and reverts. Did you still pay for it?",
   a="Yes, for the gas used up to the point of failure. The network did the computation, even though the result was reverted.")

# ---------------------------------------------------------------- nonce
sc("title", "The nonce.", chapter="The nonce", eyebrow="The nonce", num="1", title="Why one stuck transaction jams the rest",
   sub="Every account's transactions are numbered, in order.")
sc("statement", "Every account's transactions are numbered, in order, starting from zero. That number is the nonce. The network processes them strictly in sequence: it won't process nonce six until nonce five has confirmed, no matter how much you're willing to pay for six.",
   chapter="The nonce", kicker="The rule", lines=["Transactions confirm", "strictly in nonce order."], sub="Number six waits for number five, no matter the fee on six.")
sc("flow", "So here's what a stuck transaction actually does. You send transaction five with too low a fee, and it sits in the mempool, unconfirmed. You send transactions six and seven right after. They also sit and wait, even though they're perfectly valid, because five hasn't confirmed yet. The fix is to replace transaction five itself, same nonce, higher fee, which either confirms it or cancels it. Once five clears, six and seven follow immediately.",
   chapter="The nonce", title="One stuck nonce, three transactions waiting",
   nodes=[{"label": "Tx #5", "sub": "Low fee, stuck", "icon": "alert", "tone": "bad"}, {"label": "Tx #6", "sub": "Waiting behind it", "icon": "clock"},
          {"label": "Tx #7", "sub": "Also waiting", "icon": "clock"}, {"label": "Replace #5", "sub": "Same nonce, higher fee", "icon": "swap"}])
sc("compare", "When you replace a stuck transaction, you actually have two choices, both using the same nonce. Speed it up: keep the same instruction, just raise the fee, so it confirms as originally intended. Or cancel it: replace it with a zero-value transaction to yourself, at a higher fee, which uses up that nonce harmlessly and clears the jam without ever doing the original action.",
   chapter="The nonce",
   title="Speed up vs cancel a transaction", left={"label": "Speed up", "tone": "good", "items": ["Same instruction, higher fee", "Confirms as originally intended"]},
   right={"label": "Cancel", "tone": "neutral", "items": ["Zero-value tx to yourself, higher fee", "Clears the jam, does nothing else"]})
sc("quiz", "Quick check. All your newer transactions are stuck pending. What's the most likely cause? [[pause 4]] The answer: an earlier nonce is stuck. Replace it or speed it up, same nonce, higher fee, and everything behind it follows immediately.",
   chapter="The nonce", n=2, of=4, q="All your newer transactions are stuck pending. What's the most likely cause?",
   a="An earlier nonce is stuck. Replace or speed it up (same nonce, higher fee), and the rest follow.")

# ---------------------------------------------------------------- the real math
sc("title", "The real math.", chapter="The real math", eyebrow="The real math", num="$", title="What a swap actually costs",
   sub="150,000 gas, two very different gas prices.")
sc("chart", "Here's a real worked example. A swap uses one hundred fifty thousand gas. At twenty gwei, a quiet network, that's one hundred fifty thousand times twenty, three million gwei, which is zero point zero zero three E.T.H. At three thousand dollars an E.T.H., that's nine dollars. The same swap, during congestion, at eighty gwei, costs thirty-six dollars. Same swap. Same wallet. Four times the price, because the network got busy.",
   "Here's a real worked example. A swap uses 150,000 gas. At 20 gwei, a quiet network, that's 150,000 × 20 = 3,000,000 gwei, which is 0.003 ETH. At $3,000/ETH, that's $9. The same swap, during congestion, at 80 gwei, costs $36. Same swap. Same wallet. Four times the price, because the network got busy.",
   chapter="The real math", kind="bars", title="Same swap, quiet vs congested", sub=EX,
   bars=[{"label": "Quiet (20 gwei)", "text": "150,000 gas", "value": 9, "show": "$9", "tone": "good"}, {"label": "Congested (80 gwei)", "text": "Same 150,000 gas", "value": 36, "show": "$36", "tone": "bad"}],
   note="Same swap, same wallet. 4× the price, because the network got busy.")
sc("stats", "And here's the number that changes everything: the same swap, on a popular layer two instead of Ethereum's main chain. Layer twos batch many transactions together and settle them back to Ethereum as one group, which typically brings the cost down to somewhere around a cent or two, not dollars. That's an illustrative, rounded range, real costs vary by network and moment, but the direction is consistent and large. It's exactly why Module Zero has you practising on a low-fee network first.",
   "And here's the number that changes everything: the same swap, on a popular layer two instead of Ethereum's main chain. Layer 2s batch many transactions together and settle them back to Ethereum as one group, which typically brings the cost down to somewhere around a cent or two, not dollars. That's an illustrative, rounded range, real costs vary by network and moment, but the direction is consistent and large. It's exactly why Module 0 has you practising on a low-fee network first.",
   chapter="The real math", stats=[["$9", "same swap, Ethereum mainnet (quiet)"], ["≈ 1–2¢", "same kind of swap, a popular layer 2 (illustrative)"]])
sc("statement", "And here's why that number matters more than it looks. If you're compounding one dollar fifty of rewards, and gas costs nine dollars, the gas costs more than the rewards. That's not a rare edge case, it's the default at small position sizes. That's exactly why position size matters on-chain, and why this program keeps coming back to it.",
   "And here's why that number matters more than it looks. If you're compounding $1.50 of rewards, and gas costs $9, the gas costs more than the rewards. That's not a rare edge case, it's the default at small position sizes. That's exactly why position size matters on-chain, and why this program keeps coming back to it.",
   chapter="The real math", kicker="Why it matters", lines=["$1.50 of rewards.", "$9 of gas to claim them."], sub="Gas can cost more than the reward. Position size matters.")
img(D + "tx-lifecycle.png", "Reading it on an explorer",
    "One more real habit: checking a transaction on an explorer. It shows the status, the fee actually paid, the sender and receiver, which contract was called, and every token transfer and log the transaction produced. Get in the habit of checking your own transactions there. It's the fastest way to confirm a transaction did exactly what you expected, and nothing more.",
    chapter="The real math")
sc("quiz", "Last check, the numbers. Two hundred thousand gas at ten gwei, with E.T.H. at two thousand five hundred dollars. What does that cost? [[pause 4]] The answer: two hundred thousand times ten is two million gwei, which is zero point zero zero two E.T.H. At two thousand five hundred dollars an E.T.H., that's five dollars.",
   "Last check, the numbers. 200,000 gas at 10 gwei, with ETH at $2,500. What does that cost? [[pause 4]] The answer: 200,000 × 10 = 2,000,000 gwei = 0.002 ETH. At $2,500/ETH, that's $5.",
   chapter="The real math", n=3, of=4, q="200,000 gas at 10 gwei, with ETH at $2,500. What does that cost?",
   a="200,000 × 10 = 2,000,000 gwei = 0.002 ETH. At $2,500/ETH, that's $5.")
sc("quiz", "One more. You're about to sign a transaction, and the fee estimate looks unusually high. What should you do, in a single word? [[pause 4]] The answer: wait. Check the fee estimate before signing, every time, and if it's high, a quieter moment is often minutes away.",
   chapter="The real math", n=4, of=4, q="A fee estimate looks unusually high right before you sign. What should you do?",
   a="Wait, when you can. Check the fee estimate before signing every time — a quieter moment is often just minutes away.")

sc("steps", "Put it all together, and here's the habit for every transaction you'll ever sign. Check the fee estimate first. If it looks high and you're not racing anyone, wait. Sign only once the number makes sense for what you're doing. And afterward, confirm it on an explorer: status, fee paid, and exactly what it did. Four steps, every time, and gas surprises stop being surprises.",
   chapter="The real math", title="The habit, every transaction",
   steps=["Check the fee estimate first", "High, and no rush? Wait.", "Sign once the number makes sense", "Confirm it after, on an explorer"], result="Gas surprises stop being surprises")

# ---------------------------------------------------------------- checklist and recap
sc("bullets", "Here's your checklist. Do it now, for real. First, you check the fee estimate before signing. Second, you know how to find your transaction on an explorer. And third, you know a stuck transaction can be sped up or cancelled, with the same nonce and a higher fee.",
   chapter="Checklist", title="Your checklist", numbered=True,
   items=["Check the fee estimate before signing", "Know how to find your transaction on an explorer", "A stuck transaction: same nonce, higher fee, to speed up or cancel"])
sc("bullets", "Let's recap. Every transaction runs the same path: create, sign, broadcast, mempool, block, confirmed, final. Gas is computation, priced as base fee plus tip, in gwei, and it's paid whether or not the transaction succeeds. The nonce orders your transactions strictly, so one stuck transaction jams every one behind it. And the real cost of a swap can swing four times over, quiet versus congested, which is exactly why position size matters.",
   chapter="Recap", title="Recap", check=False,
   items=["Create → sign → broadcast → mempool → block → confirmed → final", "Gas = base fee + tip, in gwei; paid whether it succeeds or fails",
          "The nonce orders transactions strictly — one stuck tx jams the rest", "Gas can swing 4× with congestion; that's why position size matters"])
sc("cta", "Do the checklist now, before you move on. You now have the whole lesson in your head: the seven-stop lifecycle, what gas actually is, why the nonce orders everything strictly, how the real cost can swing four times over with congestion and drop by two orders of magnitude on a layer two, and how to estimate a real cost before you sign. Next up, Lesson one point three: Wallets, keys, hardware and multisig.",
   "Do the checklist now, before you move on. You now have the whole lesson in your head: the seven-stop lifecycle, what gas actually is, why the nonce orders everything strictly, how the real cost can swing 4x over with congestion and drop by two orders of magnitude on a layer 2, and how to estimate a real cost before you sign. Next up, Lesson 1.3: Wallets, keys, hardware and multisig.",
   chapter="Recap", button="Next: Lesson 1.3", sub="Wallets, keys, hardware & multisig")

spec = {"id": "lesson-01-2", "title": "Lesson 1.2: How a transaction actually happens", "size": [1920, 1080], "group": "lessons", "maxMinutes": 25,
        "tag": "Lesson 1.2", "gold": True, "music": True, "musicLevel": 0.14, "seed": 44,
        "use": "Lesson 1.2 page in the Whop course. Hand-written gold-standard script: the 7-stop lifecycle, gas/gwei/base fee/tip, nonces, and the real gas-cost worked math.",
        "thumbnail": {"title": "How a transaction happens", "subtitle": "Lesson 1.2"}, "scenes": S}
out = ROOT / "video-scripts" / "gold" / "lesson-01-2.json"
out.write_text(json.dumps(spec, indent=1, ensure_ascii=False))
words = sum(len(s["vo"].replace("[[pause 4]]", "").split()) for s in S)
print(f"{len(S)} scenes, {words} words, est {(words / 171 * 60 + len(S) * 1.3 + 4 * 4) / 60:.1f} min")
