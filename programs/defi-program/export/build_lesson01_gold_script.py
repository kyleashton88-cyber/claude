#!/usr/bin/env python3
"""Gold-standard script for Lesson 0.1, Money, ledgers and why blockchains exist
(about 12-14 minutes). Teaches every key idea from the lesson page with animated
flows and charts, and grounds it with three "illustrative" screen mockups (a block
explorer, a real Bitcoin/Ethereum timeline, a wallet's send screen) since this
environment cannot fetch live screenshots of exchanges or wallets and never logs
into an account or wallet to capture real UI itself.

Writes video-scripts/gold/lesson-00-1.json (the generator skips lessons with a
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

# ---------------------------------------------------------------- intro
sc("title", "Lesson zero point one. Money, ledgers and why blockchains exist. By the end, you'll be able to explain, in plain words, what a blockchain is, what a cryptocurrency is, and what DeFi means, well enough to teach someone else.",
   "Lesson 0.1. Money, ledgers and why blockchains exist. By the end, you'll be able to explain, in plain words, what a blockchain is, what a cryptocurrency is, and what DeFi means, well enough to teach someone else.",
   chapter="Intro", eyebrow="Lesson 0.1", num="0.1", title="Money, ledgers and why blockchains exist", sub="Every idea in this lesson, in pictures.")
sc("pillars", "Here's the plan. First, money as a record, and why a blockchain is a record nobody controls alone. Second, what Bitcoin and Ethereum actually are, with the real dates. Third, smart contracts, stablecoins and DeFi. And finally, a full worked example: Alice sends Bob zero point one E.T.H., step by step, on a real wallet screen.",
   "Here's the plan. First, money as a record, and why a blockchain is a record nobody controls alone. Second, what Bitcoin and Ethereum actually are, with the real dates. Third, smart contracts, stablecoins and DeFi. And finally, a full worked example: Alice sends Bob 0.1 ETH, step by step, on a real wallet screen.",
   chapter="Intro", title="What this lesson covers",
   items=[{"icon": "book", "title": "Money as a record", "text": "And why a blockchain is different"}, {"icon": "clock", "title": "BTC and ETH", "text": "The real history, in order"},
          {"icon": "code", "title": "Contracts, coins, DeFi", "text": "Three more words you'll need"}, {"icon": "swap", "title": "A worked example", "text": "Alice sends Bob 0.1 ETH"}])
sc("statement", "One honest note before we start. Some of the screens in this lesson are clearly labelled illustrative: accurate recreations of what you'll see, built so we can show you the idea, not a live capture of any one exchange or wallet, whose exact design changes over time anyway. When you get to Lesson zero point two, you'll be looking at the real thing, on your own screen.",
   "One honest note before we start. Some of the screens in this lesson are clearly labelled illustrative: accurate recreations of what you'll see, built so we can show you the idea, not a live capture of any one exchange or wallet, whose exact design changes over time anyway. When you get to Lesson 0.2, you'll be looking at the real thing, on your own screen.",
   chapter="Intro", kicker="A quick note", lines=["Mockups here are labelled", "“illustrative”, not live captures."], sub="You'll be on the real thing yourself from Lesson 0.2 onward.")

# ---------------------------------------------------------------- money is a record
sc("title", "Money is a record.", chapter="Money is a record", eyebrow="Money is a record", num="1", title="Money is a record",
   sub="Of who owns what.")
sc("statement", "Start here. Money is a record of who owns what. Your bank balance isn't a pile of cash sitting somewhere with your name on it. It's a line in your bank's private ledger, a record book, and you trust the bank to keep that line correct.",
   chapter="Money is a record", kicker="The first idea", lines=["Your balance isn't cash.", "It's a line in a ledger."], sub="A ledger is just a record book. You trust the bank to keep it correct.")
sc("flow", "Here's what happens when you pay someone through a bank. You tell the bank to move money. The bank checks your balance. It edits its private ledger: minus from you, plus to them. And it can, if it needs to, reverse that edit. A chargeback, a fraud reversal, a correction. The bank is the one party everyone trusts to keep, and if needed unwind, the record.",
   chapter="Money is a record", title="How a bank moves money",
   nodes=[{"label": "You instruct", "sub": "Pay someone", "icon": "bell"}, {"label": "Bank checks", "sub": "Your balance", "icon": "bank"},
          {"label": "Ledger edited", "sub": "Minus you, plus them", "icon": "doc"}, {"label": "Can reverse", "sub": "Chargebacks, corrections", "icon": "swap"}])
img(D + "ledgers-vs-blockchain.png", "A different kind of ledger",
    "A blockchain asks a different question. What if, instead of one company keeping the ledger, thousands of independent computers each kept an identical copy, and checked every new entry together? That's a blockchain: a shared ledger. New entries can't be quietly changed, because every other copy would disagree and reject it. The trade-off is real, and it's the whole reason this program starts with safety: there's no undo.",
    chapter="Money is a record")
img(D + "story-many-copies.png", "Why nobody can cheat",
    "Picture it concretely. One node tries to edit its copy to say it received extra coins. Every other node compares notes, sees the mismatch, and simply ignores the edited copy. To fake an entry, you'd have to control most of the network at once, which is enormously expensive by design. No single company decides what happened. And that's also why no one, not even the network itself, can undo a payment for you.",
    chapter="Money is a record", callouts=[{"x": 0.76, "y": 0.63, "text": "Rejected", "at": 1, "below": True}])
sc("stats", "One real number, so “thousands of computers” isn't just a phrase. Ethereum's ledger is checked by roughly one million independent validators worldwide, each one holding a copy and voting on what's true. That's not a company with a data centre. It's closer to a million strangers, on every continent, refusing to agree with a lie.",
   "One real number, so “thousands of computers” isn't just a phrase. Ethereum's ledger is checked by roughly 1 million independent validators worldwide, each one holding a copy and voting on what's true. That's not a company with a data centre. It's closer to a million strangers, on every continent, refusing to agree with a lie.",
   chapter="Money is a record", stats=[["≈ 1,000,000", "independent validators worldwide (illustrative)"]])
img(D + "story-chain-of-blocks.png", "Why it's called a chain",
    "New entries arrive in batches called blocks. Each block carries a seal, a fingerprint built from everything inside it plus the seal of the block before. That links the blocks into a chain. Change one old entry, and its seal changes, which breaks every seal after it. Every other copy notices immediately. That's why a blockchain's history can't be quietly rewritten, only added to.",
    chapter="Money is a record", zoom={"x": 0.3, "y": 0.55, "s": 1.3, "at": 2})
img(D + "story-block-explorer.png", "You can check it yourself",
    "And because it's public, anyone can check it. This is what a block explorer shows, an illustrative recreation of the kind of tool you'll actually use later in this program: a block number, how many transactions it holds, and each one's sender, receiver and amount. It can show you a transaction happened. It can never undo one.",
    chapter="Money is a record")

# ---------------------------------------------------------------- BTC and ETH
sc("title", "Bitcoin and Ethereum.", chapter="Bitcoin and Ethereum", eyebrow="Bitcoin and Ethereum", num="2", title="A cryptocurrency, defined",
   sub="With the real dates.")
sc("statement", "A cryptocurrency is simply a unit recorded on a blockchain. That's the whole definition. What makes Bitcoin and Ethereum different from each other is what each blockchain was built to do.",
   chapter="Bitcoin and Ethereum", kicker="The definition", lines=["A cryptocurrency is a unit", "recorded on a blockchain."], sub="What differs is what each blockchain was built to do.")
img(D + "story-btc-eth-timeline.png", "The real history",
    "Here's the real timeline, not a simplified version. In two thousand and eight, someone using the name Satoshi Nakamoto published the Bitcoin white paper: money with no bank in the middle. In two thousand and nine, the first block was mined, the first working blockchain, and the first cryptocurrency, B.T.C. In two thousand and fifteen, Ethereum launched: a blockchain that also runs small programs, not just payments. And through the twenty-twenties, DeFi grew up on top of that: lending, trading and stablecoins, run by those programs at real scale.",
    "Here's the real timeline, not a simplified version. In 2008, someone using the name Satoshi Nakamoto published the Bitcoin white paper: money with no bank in the middle. In 2009, the first block was mined, the first working blockchain, and the first cryptocurrency, BTC. In 2015, Ethereum launched: a blockchain that also runs small programs, not just payments. And through the 2020s, DeFi grew up on top of that: lending, trading and stablecoins, run by those programs at real scale.",
    chapter="Bitcoin and Ethereum")
sc("compare", "So, side by side. Bitcoin does one thing and does it well: it moves and stores value, with the deepest security and the longest track record of any blockchain. Ethereum does that too, but it also runs smart contracts, which is what makes lending apps, exchanges and stablecoins possible. Most of this program happens on Ethereum and the networks built around it, because that's where DeFi actually lives.",
   chapter="Bitcoin and Ethereum",
   left={"label": "Bitcoin (BTC)", "tone": "neutral", "items": ["Moves and stores value", "Deepest security, longest track record", "Doesn't run smart contracts"]},
   right={"label": "Ethereum (ETH)", "tone": "good", "items": ["Moves and stores value too", "Also runs smart contracts", "Where most of this program happens"]})
sc("stats", "One more real number, so “gas” isn't abstract later. Ethereum processes somewhere around one point two million transactions on an average day, each one checked by the network and added to a block. That volume is exactly why block space is scarce, and why, in Lesson zero point six, you'll learn that transaction fees rise and fall with demand.",
   "One more real number, so “gas” isn't abstract later. Ethereum processes somewhere around 1.2 million transactions on an average day, each one checked by the network and added to a block. That volume is exactly why block space is scarce, and why, in Lesson 0.6, you'll learn that transaction fees rise and fall with demand.",
   chapter="Bitcoin and Ethereum", stats=[["≈ 1.2M", "transactions on an average day (illustrative)"]])
sc("quiz", "Quick check. What's the one core difference between what Bitcoin does and what Ethereum does? [[pause 4]] The answer: Bitcoin moves and stores value. Ethereum does that too, but it also runs smart contracts, small programs that make DeFi possible.",
   chapter="Bitcoin and Ethereum", n=1, of=3, q="What's the one core difference between what Bitcoin does and what Ethereum does?",
   a="Bitcoin moves and stores value. Ethereum does that too, but also runs smart contracts, which is what makes DeFi possible.")

# ---------------------------------------------------------------- contracts, coins, DeFi
sc("title", "Contracts, coins and DeFi.", chapter="Contracts, coins and DeFi", eyebrow="Contracts, coins and DeFi", num="3", title="Three more words",
   sub="Smart contract · Stablecoin · DeFi")
img(D + "story-vending-machine.png", "A smart contract",
    "A smart contract is a program that lives on a blockchain and follows fixed rules. Picture a vending machine. You insert coins, the rules decide what happens, and you get the result instantly. There's no cashier: if you press the wrong button, nobody refunds you. A lending app's smart contract might say, in effect, “whoever deposits X gets Y back, plus interest,” and it will do exactly that, every time, for anyone.",
    chapter="Contracts, coins and DeFi")
img(D + "story-stablecoin-voucher.png", "A stablecoin",
    "A stablecoin is a token designed to stay worth about one dollar, like U.S.D.C. or U.S.D.T. Think of it as a digital dollar voucher: the issuer holds roughly a dollar in reserve for every token, and you can swap the token back for a dollar. You'll use stablecoins constantly in this program. But notice the word “designed”: a stablecoin is only as good as its reserves and its issuer, and it can still fail. You'll learn how to judge that in Lesson one point five.",
    "A stablecoin is a token designed to stay worth about one dollar, like USDC or USDT. Think of it as a digital dollar voucher: the issuer holds roughly a dollar in reserve for every token, and you can swap the token back for a dollar. You'll use stablecoins constantly in this program. But notice the word “designed”: a stablecoin is only as good as its reserves and its issuer, and it can still fail. You'll learn how to judge that in Lesson 1.5.",
    chapter="Contracts, coins and DeFi")
sc("flow", "Put those two ideas together and you get DeFi, decentralised finance: financial services, trading, lending, earning interest, run by smart contracts instead of banks. Take an ordinary trade. On a bank's system, it goes through the bank's own systems and staff before it settles in the bank's ledger.",
   chapter="Contracts, coins and DeFi", title="A trade, the bank way",
   nodes=[{"label": "You", "icon": "bell"}, {"label": "Bank's systems", "sub": "Staff, opening hours", "icon": "bank"}, {"label": "Settled", "sub": "In the bank's ledger", "icon": "check"}],
   layout="row")
sc("flow", "The same trade in DeFi skips all of that. It goes straight into a smart contract, and settles on the blockchain itself. No branch, no staff, no opening hours, just the contract and the ledger.",
   chapter="Contracts, coins and DeFi", title="The same trade, the DeFi way",
   nodes=[{"label": "You", "icon": "bell"}, {"label": "Smart contract", "sub": "No staff, no branch", "icon": "code"}, {"label": "Settled", "sub": "On the blockchain itself", "icon": "check"}],
   layout="row")
sc("compare", "So here's DeFi against traditional finance, directly. A bank has a branch, staff and opening hours, and it can reverse a mistaken payment. A DeFi smart contract has none of that: it's open all day, every day, needs no staff, and treats everyone identically. But it also can't make an exception for you. That's the deal.",
   chapter="Contracts, coins and DeFi",
   left={"label": "A bank", "tone": "neutral", "items": ["Branch, staff, opening hours", "Can reverse a mistaken payment", "Can make an exception"]},
   right={"label": "A DeFi smart contract", "tone": "good", "items": ["Open every hour, every day", "No staff, treats everyone the same", "Can never make an exception"]})
sc("stats", "And here's why DeFi doesn't need banking hours. A bank transfer can sit for a business day or more, waiting on staff and settlement windows. A new block on Ethereum settles roughly every twelve seconds, day or night, weekend or holiday. DeFi isn't faster because it's magic. It's faster because there's no one to wait on.",
   "And here's why DeFi doesn't need banking hours. A bank transfer can sit for a business day or more, waiting on staff and settlement windows. A new block on Ethereum settles roughly every 12 seconds, day or night, weekend or holiday. DeFi isn't faster because it's magic. It's faster because there's no one to wait on.",
   chapter="Contracts, coins and DeFi", stats=[["1 business day", "typical bank transfer (illustrative)"], ["12 sec", "typical block on Ethereum (illustrative)"]])
sc("statement", "Which brings us to the trade-off underneath everything in this module. No bank in the middle means nobody can freeze your money without your keys. It also means nobody can reverse your mistakes. That single sentence is why this program starts with safety, not strategy.",
   chapter="Contracts, coins and DeFi", kicker="The trade-off", lines=["Nobody can freeze it.", "Nobody can undo it, either."], sub="That single sentence is why this program starts with safety.")

# ---------------------------------------------------------------- worked example
sc("title", "Worked example.", chapter="Worked example", eyebrow="Worked example", num="4", title="Alice sends Bob 0.1 ETH",
   sub="Step by step, on a real wallet screen.")
img(D + "story-wallet-send.png", "What Alice sees",
    "Here's Alice's wallet, right before she sends. This is a labelled, illustrative recreation of a typical wallet screen, built to show the real fields you'll see, not a capture of any one product. She fills in Bob's address, an amount, zero point one E.T.H., and sees the network fee, the gas, that this transaction will cost. When she taps Sign and Send, she isn't sending a file. She's signing an instruction: “move zero point one E.T.H. from my address to Bob's.”",
    "Here's Alice's wallet, right before she sends. This is a labelled, illustrative recreation of a typical wallet screen, built to show the real fields you'll see, not a capture of any one product. She fills in Bob's address, an amount, 0.1 ETH, and sees the network fee, the gas, that this transaction will cost. When she taps Sign and Send, she isn't sending a file. She's signing an instruction: “move 0.1 ETH from my address to Bob's.”",
    chapter="Worked example")
sc("flow", "Now follow the instruction itself. Alice's wallet signs it with her private key, which proves it's really her without ever revealing the key. The network checks that she actually owns zero point one E.T.H. It's added to the next block. And every copy of the ledger updates at once. Bob now owns it. There is no undo button, anywhere in this chain.",
   "Now follow the instruction itself. Alice's wallet signs it with her private key, which proves it's really her without ever revealing the key. The network checks that she actually owns 0.1 ETH. It's added to the next block. And every copy of the ledger updates at once. Bob now owns it. There is no undo button, anywhere in this chain.",
   chapter="Worked example", title="What happens after she taps Send",
   nodes=[{"label": "Signed", "sub": "Her private key proves it", "icon": "key"}, {"label": "Checked", "sub": "She owns 0.1 ETH", "icon": "eye"},
          {"label": "Added to a block", "sub": "Sealed in", "icon": "layers"}, {"label": "Bob owns it", "sub": "Every copy updates", "icon": "check"}])
img(D + "story-block-explorer.png", "Now it's public",
    "And here's the same transaction, now that it's settled, on that illustrative block explorer again. Anyone, including Bob, including Alice, including a stranger, can look it up: from Alice's address, to Bob's, zero point one E.T.H., confirmed. Nothing about it is private, and nothing about it can be reversed.",
    "And here's the same transaction, now that it's settled, on that illustrative block explorer again. Anyone, including Bob, including Alice, including a stranger, can look it up: from Alice's address, to Bob's, 0.1 ETH, confirmed. Nothing about it is private, and nothing about it can be reversed.",
    chapter="Worked example")
sc("quiz", "Quick check. When Alice sends Bob crypto, what exactly does she sign? [[pause 4]] The answer: an instruction, something like “move zero point one E.T.H. from my address to Bob's.” She never sends a file, and she never reveals her private key.",
   "Quick check. When Alice sends Bob crypto, what exactly does she sign? [[pause 4]] The answer: an instruction, something like “move 0.1 ETH from my address to Bob's.” She never sends a file, and she never reveals her private key.",
   chapter="Worked example", n=2, of=3, q="When Alice sends Bob crypto, what exactly does she sign?",
   a="An instruction (“move 0.1 ETH from my address to Bob's”). Never a file, and never her private key.")

# ---------------------------------------------------------------- checklist and quiz
sc("bullets", "Here's your checklist. Do it now, for real. First, you can explain a blockchain as “a shared ledger nobody can quietly edit.” Second, you know the difference between B.T.C., E.T.H. and a stablecoin. And third, you understand that crypto transactions can't be reversed.",
   "Here's your checklist. Do it now, for real. First, you can explain a blockchain as “a shared ledger nobody can quietly edit.” Second, you know the difference between BTC, ETH and a stablecoin. And third, you understand that crypto transactions can't be reversed.",
   chapter="Checklist", title="Your checklist", numbered=True,
   items=["Explain a blockchain as “a shared ledger nobody can quietly edit”", "Know the difference: BTC, ETH and a stablecoin", "Understand: crypto transactions can't be reversed"])
sc("quiz", "Question one. Why can't someone quietly change an old blockchain entry? [[pause 4]] The answer: thousands of computers hold copies, and would reject any version that doesn't match.",
   chapter="Quiz", n=3, of=3, q="Why can't someone quietly change an old blockchain entry?",
   a="Thousands of computers hold copies, and would reject a version that doesn't match.")
sc("statement", "Two more from the checklist, quickly. What is a stablecoin designed to do? Stay worth about a dollar, or another currency, and it can still fail. And what does DeFi replace, and what do you give up? It replaces banks and brokers with smart contracts, and you give up anyone who can reverse a mistake or help you recover funds.",
   "Two more from the checklist, quickly. What is a stablecoin designed to do? Stay worth about $1, or another currency, and it can still fail. And what does DeFi replace, and what do you give up? It replaces banks and brokers with smart contracts, and you give up anyone who can reverse a mistake or help you recover funds.",
   chapter="Quiz", kicker="Two more, quickly", lines=["A stablecoin: stays near $1.", "DeFi: no one left to reverse a mistake."], sub="It can still fail · replaces banks and brokers with smart contracts")

# ---------------------------------------------------------------- recap
sc("bullets", "Let's recap. Money is a record of who owns what. A blockchain is a ledger that thousands of computers keep together, so no old entry can be quietly changed. Bitcoin, from two thousand and nine, moves and stores value. Ethereum, from two thousand and fifteen, does that and runs smart contracts. Stablecoins aim to hold a dollar. And DeFi is financial services run by those contracts, with the trade-off that nobody can reverse a mistake.",
   "Let's recap. Money is a record of who owns what. A blockchain is a ledger that thousands of computers keep together, so no old entry can be quietly changed. Bitcoin, from 2009, moves and stores value. Ethereum, from 2015, does that and runs smart contracts. Stablecoins aim to hold a dollar. And DeFi is financial services run by those contracts, with the trade-off that nobody can reverse a mistake.",
   chapter="Recap", title="Recap", check=False,
   items=["Money is a record of who owns what", "A blockchain: a ledger thousands of computers keep together", "Bitcoin (2009) moves value; Ethereum (2015) also runs contracts",
          "Stablecoins aim to hold $1; DeFi runs on contracts, with no undo"])
sc("cta", "Do the checklist now, before you move on. Next up, Lesson zero point two: Opening and securing an exchange account.",
   "Do the checklist now, before you move on. Next up, Lesson 0.2: Opening and securing an exchange account.",
   chapter="Recap", button="Next: Lesson 0.2", sub="Opening and securing an exchange account")

spec = {"id": "lesson-00-1", "title": "Lesson 0.1: Money, ledgers and why blockchains exist", "size": [1920, 1080], "group": "lessons", "maxMinutes": 25,
        "tag": "Lesson 0.1", "gold": True, "music": True, "musicLevel": 0.14, "seed": 41,
        "use": "Lesson 0.1 page in the Whop course. Hand-written gold-standard script: the real BTC/ETH timeline, animated flows and charts, and labelled-illustrative screen mockups.",
        "thumbnail": {"title": "Money, ledgers, blockchains", "subtitle": "Lesson 0.1"}, "scenes": S}
out = ROOT / "video-scripts" / "gold" / "lesson-00-1.json"
out.write_text(json.dumps(spec, indent=1, ensure_ascii=False))
words = sum(len(s["vo"].replace("[[pause 4]]", "").split()) for s in S)
print(f"{len(S)} scenes, {words} words, est {(words / 171 * 60 + len(S) * 1.3 + 4 * 3) / 60:.1f} min")
