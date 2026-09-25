#!/usr/bin/env python3
"""Script for the long-form Module 0 intro (about 19 minutes): crypto from zero, told as a story.
A beginner, Sam, goes from "what even is crypto?" to set up safely, and every hard idea is
explained with an everyday picture (a shared notebook, a mailbox and key, a postage stamp,
a vending machine, a flight simulator). Ends by sending the viewer to Lesson 0.0.

Writes video-scripts/core/module-00-intro.json (it replaces the generated Module 0 intro).
Spoken text (vo) spells numbers and abbreviations for the voice; cap is the written caption
with the same sentences."""
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

# ---------------------------------------------------------------- cold open
sc("logo", "Welcome to Module Zero: Crypto From Zero. If you've never owned crypto, never opened a wallet, and you're not even sure what a blockchain is, you're in exactly the right place. This module was built for you.",
   "Welcome to Module 0: Crypto From Zero. If you've never owned crypto, never opened a wallet, and you're not even sure what a blockchain is, you're in exactly the right place. This module was built for you.",
   chapter="Welcome", tagline="Module 0 · Crypto From Zero")
sc("statement", "Over the next twenty minutes or so, I'm going to tell you a story. It's about someone called Sam. Sam is a lot like most people who join this program. Curious, a little nervous, and completely new.",
   "Over the next 20 minutes or so, I'm going to tell you a story. It's about someone called Sam. Sam is a lot like most people who join this program. Curious, a little nervous, and completely new.",
   chapter="Welcome", kicker="Meet Sam", lines=["Curious.", "A little nervous.", "Completely new."], sub="Sam's first week is the map for your first week.")
sc("bullets", "Sam had heard the words everywhere. Bitcoin, on the news. Wallets and seed phrases, from a friend at work. DeFi, in a video that promised the moon. And a story about someone who lost everything with one wrong click. It all sounded exciting, confusing and a bit dangerous, all at once.",
   chapter="Welcome", title="What Sam had heard", check=False,
   items=["Bitcoin, on the news", "Wallets and seed phrases, from a friend", "DeFi, in a video promising the moon", "Someone who lost everything in one click"])
sc("pillars", "So here's what this video will do. First, you'll understand what crypto actually is, using pictures from everyday life. Second, you'll see the tools Sam used, and why each one exists. Third, you'll learn the handful of mistakes that cause almost every beginner loss, and how to avoid them. And fourth, you'll see exactly how Module Zero walks you through all of it, one small step at a time.",
   "So here's what this video will do. First, you'll understand what crypto actually is, using pictures from everyday life. Second, you'll see the tools Sam used, and why each one exists. Third, you'll learn the handful of mistakes that cause almost every beginner loss, and how to avoid them. And fourth, you'll see exactly how Module 0 walks you through all of it, one small step at a time.",
   chapter="Welcome", title="What this video covers",
   items=[{"icon": "book", "title": "What crypto is", "text": "In everyday pictures"}, {"icon": "wallet", "title": "The tools", "text": "What each one is for"},
          {"icon": "shield", "title": "The mistakes", "text": "And how to avoid them"}, {"icon": "compass", "title": "The path", "text": "How Module 0 gets you set up"}])

# ---------------------------------------------------------------- chapter 1: money is a record
sc("title", "Chapter one. Money is a record.", "Chapter 1. Money is a record.",
   chapter="1 · Money is a record", eyebrow="Chapter 1", num="1", title="Money is a record", sub="Before crypto makes sense, money has to.")
sc("statement", "Sam's first surprise was this. Most of the money in your life isn't cash. It's a number in a list. When you get paid, no one carries notes to your bank. Someone changes a number in the bank's records, and that number is your money.",
   chapter="1 · Money is a record", kicker="The first surprise", lines=["Most money isn't cash.", "It's a number in a list."], sub="Your balance is an entry in your bank's records.")
sc("statement", "Picture a village with one notebook. Every time someone pays someone else, the village clerk writes it down. Ana paid Ben ten coins. Ben paid Cai five. Everyone trusts the notebook, because everyone trusts the clerk. That notebook has a name. It's called a ledger.",
   "Picture a village with one notebook. Every time someone pays someone else, the village clerk writes it down. Ana paid Ben 10 coins. Ben paid Cai 5. Everyone trusts the notebook, because everyone trusts the clerk. That notebook has a name. It's called a ledger.",
   chapter="1 · Money is a record", kicker="A story", lines=["One village.", "One notebook."], sub="The notebook of who paid whom is called a ledger.")
img(D + "story-bank-vs-you.png", "The clerk is your bank",
    "Your bank is that clerk. It keeps the record for you. It can reverse a payment if something goes wrong. It can help when you forget a password. But it can also freeze your account, and you have to trust it completely. Crypto changes who's in charge. In your own wallet, the network keeps the record, no one can reverse a payment, no one can reset your password, and no one can freeze it but you.",
    chapter="1 · Money is a record",
    zoom={"x": 0.75, "y": 0.6, "s": 1.3, "at": 6})
img(D + "ledgers-vs-blockchain.png", "From Lesson 0.1",
    "So what if the village didn't need a clerk at all? What if, instead of one notebook, every villager kept an identical copy, and they all checked each new entry together? That's the idea behind a blockchain. It's a shared ledger. Thousands of computers keep the same copy, and old entries can't be quietly changed. The trade-off is simple, and it matters: there's no undo.",
    chapter="1 · Money is a record", zoom={"x": 0.72, "y": 0.55, "s": 1.25, "at": 4})
img(D + "story-many-copies.png", "Thousands of copies",
    "Here's why nobody can cheat. Imagine someone edits their copy to say they received a hundred coins. Every other copy disagrees, so the network simply ignores the edited one. To fake a payment, you'd have to overpower most of the network at once, which is enormously expensive. No single company is in charge, and that's also why no one can undo a payment for you.",
    "Here's why nobody can cheat. Imagine someone edits their copy to say they received 100 coins. Every other copy disagrees, so the network simply ignores the edited one. To fake a payment, you'd have to overpower most of the network at once, which is enormously expensive. No single company is in charge, and that's also why no one can undo a payment for you.",
    chapter="1 · Money is a record", callouts=[{"x": 0.76, "y": 0.63, "text": "Ignored", "at": 1, "below": True}])
img(D + "story-chain-of-blocks.png", "Why it's called a chain",
    "And why the word chain? New entries are grouped into pages, called blocks. Each block carries a kind of seal, a fingerprint made from everything written on it, plus the seal of the page before. So the pages are linked. Change one old entry, and its seal changes, and every page after it stops matching. That's why history on a blockchain can't be quietly rewritten.",
    chapter="1 · Money is a record",
    zoom={"x": 0.3, "y": 0.55, "s": 1.4, "at": 2})
sc("compare", "So, in one picture. Bitcoin, launched in two thousand and nine, was the first blockchain: digital money with no bank in the middle. Ethereum, launched in two thousand and fifteen, went further. It lets people put small programs on the blockchain, which is what makes apps like lending and trading possible. Most of this program happens on Ethereum and the networks built around it.",
   "So, in one picture. Bitcoin, launched in 2009, was the first blockchain: digital money with no bank in the middle. Ethereum, launched in 2015, went further. It lets people put small programs on the blockchain, which is what makes apps like lending and trading possible. Most of this program happens on Ethereum and the networks built around it.",
   chapter="1 · Money is a record",
   left={"label": "Bitcoin (2009)", "tone": "neutral", "items": ["The first blockchain", "Digital money, no bank in the middle"]},
   right={"label": "Ethereum (2015)", "tone": "good", "items": ["Runs small programs", "Apps for lending and trading", "Where this program works"]})
img(D + "story-why-crypto.png", "Why people use it",
    "Sam asked the obvious question. Why would anyone want this? Four reasons. You can send money worldwide, to anyone, at any time, often in minutes. You can hold it yourself, with no bank needed. The money is programmable, so apps can lend, trade and pay automatically. And the rules are open: anyone can check the record. But notice the line at the bottom. The same things that make it powerful make mistakes permanent. That's why we start with safety.",
    chapter="1 · Money is a record")

# ---------------------------------------------------------------- chapter 2: the front door
sc("title", "Chapter two. The front door.", "Chapter 2. The front door.",
   chapter="2 · The front door", eyebrow="Chapter 2", num="2", title="The front door", sub="How Sam turned ordinary money into crypto, without overpaying.")
sc("statement", "Sam's first practical question was simple. How do I actually get some? The answer, for almost everyone, is an exchange. Think of it as a currency exchange desk at an airport. You hand over dollars, pounds or euros, and you get crypto back.",
   chapter="2 · The front door", kicker="The on-ramp", lines=["An exchange is", "the front door."], sub="Like a currency desk: ordinary money in, crypto out.")
img(D + "exchange-lockdown.png", "From Lesson 0.2",
    "Before Sam deposited a single dollar, they locked the door. First, the account: a unique email and a password manager. Second, two-factor authentication, using an authenticator app, not text messages, which can be hijacked. Third, a withdrawal whitelist, so money can only leave to addresses Sam has approved. And fourth, an anti-phishing code, a word that appears in every real email from the exchange. Fake emails won't have it.",
    chapter="2 · The front door", zoom={"x": 0.38, "y": 0.5, "s": 1.35, "at": 2})
img(D + "first-buy-costs.png", "From Lesson 0.3",
    "Then Sam made a small first buy, and learned the next lesson. The price on the chart is not what you get. There's the spread, the gap between the buying and selling price. There's a trading fee, sometimes hidden as a convenience fee. And there's a network cost when you move it out. What matters is what actually lands in your wallet. Compare offers by that, not by the headline price.",
    chapter="2 · The front door", zoom={"x": 0.88, "y": 0.5, "s": 1.35, "at": 5})
img(D + "story-stablecoin-voucher.png", "Meet the stablecoin",
    "Sam also met something called a stablecoin. Think of it as a digital dollar voucher. For each token, the issuer holds about a dollar in reserve, in cash and short-term government bonds. The token moves on the blockchain, any time of day, like any other crypto. And you can swap it back for a dollar. It's how people hold steady value on-chain. But it's only as good as the reserves and the issuer behind it. It can still fail, and you'll learn how to judge that later.",
    chapter="2 · The front door")
sc("bullets", "So Sam's first-buy plan was deliberately boring. A small learning amount, money they could afford to lose. A little E.T.H., the coin that pays fees on Ethereum. A little U.S.D.C., a widely used stablecoin. And the cheapest route, checked before clicking buy.",
   "So Sam's first-buy plan was deliberately boring. A small learning amount, money they could afford to lose. A little ETH, the coin that pays fees on Ethereum. A little USDC, a widely used stablecoin. And the cheapest route, checked before clicking buy.",
   chapter="2 · The front door", title="Sam's first buy", numbered=True,
   items=["A small learning amount", "A little ETH, for fees", "A little USDC, a stablecoin", "The cheapest route, checked first"])

# ---------------------------------------------------------------- chapter 3: keys
sc("title", "Chapter three. Who holds the keys?", "Chapter 3. Who holds the keys?",
   chapter="3 · Who holds the keys", eyebrow="Chapter 3", num="3", title="Who holds the keys?", sub="The single most important idea in crypto.")
img(D + "custody-split.png", "From Lesson 0.4",
    "Here's the idea that changed how Sam thought about all of it. When your crypto sits on an exchange, the exchange holds the keys. It's convenient for buying, selling and cashing out, but you're trusting a company, and companies can freeze accounts, get hacked, or go bust. In your own wallet, you hold the keys. Nobody can freeze it. But if you lose the keys, nobody can help you either.",
    chapter="3 · Who holds the keys", callouts=[{"x": 0.27, "y": 0.72, "text": "Trust a company", "at": 2}, {"x": 0.76, "y": 0.72, "text": "Trust yourself", "at": 3}])
img(D + "story-mailbox-and-key.png", "The mailbox and the key",
    "So what is a wallet, really? Picture a row of mailboxes. Your address is the slot on your mailbox. You can share it freely, and anyone can drop coins in. Your private key is the only key that opens the box. Whoever has it can empty the box, so you never share it. And your seed phrase is the master recipe: twelve or twenty-four words that can recreate every key you have. It's your backup if a phone is lost or broken.",
    "So what is a wallet, really? Picture a row of mailboxes. Your address is the slot on your mailbox. You can share it freely, and anyone can drop coins in. Your private key is the only key that opens the box. Whoever has it can empty the box, so you never share it. And your seed phrase is the master recipe: 12 or 24 words that can recreate every key you have. It's your backup if a phone is lost or broken.",
    chapter="3 · Who holds the keys")
sc("statement", "Here's a detail that surprises most beginners. Your coins aren't actually inside the wallet app. They live on the blockchain. The wallet just holds the keys that let you move them. That's why a seed phrase can restore everything on a brand new phone.",
   chapter="3 · Who holds the keys", kicker="A surprise", lines=["Your coins aren't in the app.", "They're on the blockchain."], sub="The wallet holds the keys. The seed phrase can rebuild the wallet anywhere.")
img(D + "story-seed-words.png", "What a seed phrase looks like",
    "This is what a seed phrase looks like. These are example words, never use them. The words come from a standard list of two thousand and forty-eight. Whoever has these words, in this order, controls every coin in the wallet. So they're written on paper or stamped in metal, and never typed, photographed, stored online or shared.",
    "This is what a seed phrase looks like. These are example words, never use them. The words come from a standard list of 2,048. Whoever has these words, in this order, controls every coin in the wallet. So they're written on paper or stamped in metal, and never typed, photographed, stored online or shared.",
    chapter="3 · Who holds the keys")
img(D + "seed-backup.png", "From Lesson 0.5",
    "Sam set up their wallet from the official website, wrote the words on paper, in order, and stored them somewhere private and safe from fire and water. Then Sam did the step most people skip. They tested a restore, before depositing anything, to prove the backup actually works. And they learned the don'ts: never type it into a website, never photograph it, never share it, and never use a phrase that came pre-printed or from someone else.",
    chapter="3 · Who holds the keys", zoom={"x": 0.27, "y": 0.62, "s": 1.4, "at": 1})
sc("statement", "And here's the rule that will protect you more than any other. No real support team, no exchange, no wallet company, and nobody from this program will ever ask for your seed phrase or keys. Anyone who asks is trying to rob you. Every time.",
   chapter="3 · Who holds the keys", kicker="The golden rule", lines=["Nobody legitimate", "ever asks for your seed phrase."], sub="Not support. Not an exchange. Not this program. Anyone who asks is a thief.")
sc("quiz", "Quick check. A friendly support agent messages Sam and asks for the seed phrase, to fix a problem. What should Sam do? [[pause 4]] The answer: never share it. Real support never asks. Close the chat and report it.",
   chapter="3 · Who holds the keys", n=1, of=3, q="A “support agent” asks Sam for the seed phrase to fix a problem. What should Sam do?",
   a="Never share it. Real support never asks. Close the chat and report it.")

# ---------------------------------------------------------------- chapter 4: roads and stamps
sc("title", "Chapter four. Roads and stamps.", "Chapter 4. Roads and stamps.",
   chapter="4 · Roads and stamps", eyebrow="Chapter 4", num="4", title="Roads and stamps", sub="Networks, gas, and Sam's first transfer.")
img(D + "story-networks-roads.png", "Networks are roads",
    "Now Sam wanted to move crypto from the exchange into their own wallet. That's when they met networks. Think of networks as separate roads. Ethereum is the original road: the most secure, but with higher fees. Layer twos are faster, cheaper roads built on top of Ethereum, and there are several of them. Your address can exist on many roads at once, but a parcel only travels on the road it was sent on. Send on a road your wallet doesn't support, and the money can be very hard, or impossible, to get back.",
    "Now Sam wanted to move crypto from the exchange into their own wallet. That's when they met networks. Think of networks as separate roads. Ethereum is the original road: the most secure, but with higher fees. Layer 2s are faster, cheaper roads built on top of Ethereum, and there are several of them. Your address can exist on many roads at once, but a parcel only travels on the road it was sent on. Send on a road your wallet doesn't support, and the money can be very hard, or impossible, to get back.",
    chapter="4 · Roads and stamps", callouts=[{"x": 0.78, "y": 0.66, "text": "Wrong road", "at": 5, "below": True}])
img(D + "story-gas-stamp.png", "Gas is a stamp",
    "Every trip on those roads needs a stamp. It's called gas. When you send a transaction, you pay a small fee in the network's own coin, which on Ethereum and most layer twos is E.T.H. The computers that run the network, called validators, check your transaction and add it to a block. When roads are busy, stamps cost more. And one detail catches people out: if a transaction fails, the stamp is usually still spent.",
    "Every trip on those roads needs a stamp. It's called gas. When you send a transaction, you pay a small fee in the network's own coin, which on Ethereum and most layer 2s is ETH. The computers that run the network, called validators, check your transaction and add it to a block. When roads are busy, stamps cost more. And one detail catches people out: if a transaction fails, the stamp is usually still spent.",
    chapter="4 · Roads and stamps")
sc("flow", "Here's what happened when Sam pressed send. Sam's wallet signed the transaction with their private key. It went out to the network, where validators checked it. It was sealed into a block. And a few moments later, it arrived at the address. Once it's in a block, it's final.",
   chapter="4 · Roads and stamps", title="What happens when you press send",
   nodes=[{"label": "Sign", "sub": "Your key approves it", "icon": "key"}, {"label": "Network", "sub": "Validators check it", "icon": "users"},
          {"label": "Block", "sub": "Sealed into the chain", "icon": "layers"}, {"label": "Arrives", "sub": "Final, no undo", "icon": "check"}])
img(D + "first-transfer.png", "From Lesson 0.6",
    "So Sam's first transfer followed five steps. Copy the address with the wallet's copy button, never type it. Choose a network your wallet supports. Check the first and last six characters, ideally all of them. Send a small test, about ten dollars, and wait until it arrives. Then send the rest, and add the address to your exchange's whitelist. It took ten extra minutes. Those ten minutes are the cheapest insurance in crypto.",
    "So Sam's first transfer followed five steps. Copy the address with the wallet's copy button, never type it. Choose a network your wallet supports. Check the first and last 6 characters, ideally all of them. Send a small test, about $10, and wait until it arrives. Then send the rest, and add the address to your exchange's whitelist. It took ten extra minutes. Those ten minutes are the cheapest insurance in crypto.",
    chapter="4 · Roads and stamps", zoom={"x": 0.69, "y": 0.5, "s": 1.35, "at": 4})
sc("quiz", "Quick check. Sam's exchange offers two networks for a withdrawal, and Sam's wallet supports only one of them. What should Sam do? [[pause 4]] The answer: choose the network the wallet supports, send a small test, and wait for it to arrive before sending the rest.",
   chapter="4 · Roads and stamps", n=2, of=3, q="The exchange offers two networks, and Sam's wallet supports only one. What should Sam do?",
   a="Pick the network the wallet supports, send a small test, wait for it to arrive, then send the rest.")

# ---------------------------------------------------------------- chapter 5: first DeFi steps
sc("title", "Chapter five. Machines with no cashier.", "Chapter 5. Machines with no cashier.",
   chapter="5 · First DeFi steps", eyebrow="Chapter 5", num="5", title="Machines with no cashier", sub="What DeFi is, and how Sam practised it safely.")
img(D + "story-vending-machine.png", "A smart contract",
    "Now for the part everyone talks about: DeFi, short for decentralised finance. At its heart is the smart contract, and the best picture for it is a vending machine. You insert coins. The rules, written in code, decide what happens. You get the result instantly. And there's no cashier. If you press the wrong button, there's no one to refund you. DeFi apps are simply collections of these machines, for swapping, lending and earning.",
    chapter="5 · First DeFi steps", zoom={"x": 0.86, "y": 0.5, "s": 1.35, "at": 5})
img(D + "story-flight-simulator.png", "Practise like a pilot",
    "So how do you learn to use machines that don't give refunds? The same way pilots learn to fly. Pilots train in a simulator before they carry passengers. In crypto, the simulator is a test network, where the coins are free and worth nothing, but the buttons are real. Then you do a short hop, with a tiny real amount. You check it did what you expected. And only then do you fly normally, with the same careful habits.",
    chapter="5 · First DeFi steps")
img(D + "practice-mode-first.png", "From Lesson 0.7",
    "Sam's first DeFi steps followed that exact path. Free test tokens on a test network first. Connecting the wallet only from a bookmarked site, never from a link in a message. Reading every request before signing: what it does, who it goes to, and how much. And only after the test worked, one tiny real swap.",
    chapter="5 · First DeFi steps", zoom={"x": 0.62, "y": 0.5, "s": 1.35, "at": 3})
sc("statement", "One idea from this chapter is worth holding on to. In DeFi, your wallet asks you to sign things. A signature is like a signed cheque with your name on it. Read what you're signing, every time. If you don't understand it, don't sign it.",
   chapter="5 · First DeFi steps", kicker="Signing", lines=["A signature is a signed cheque.", "Read it first."], sub="If you don't understand a request, don't sign it.")

# ---------------------------------------------------------------- chapter 6: what goes wrong
sc("title", "Chapter six. Where beginners get hurt.", "Chapter 6. Where beginners get hurt.",
   chapter="6 · Where beginners get hurt", eyebrow="Chapter 6", num="6", title="Where beginners get hurt", sub="And the habits that close each door.")
img(D + "story-what-can-go-wrong.png", "Four open doors",
    "Sam's friend, the one who lost everything with one wrong click, didn't do anything unusual. Almost every beginner loss starts with one of four things. A lost seed phrase, with no backup and no recovery. Coins sent on the wrong network. A fake website or a fake support agent who tricks you into signing. And rushing: urgency and fear of missing out beating good habits. Module Zero exists to close all four doors before you move real money.",
    "Sam's friend, the one who lost everything with one wrong click, didn't do anything unusual. Almost every beginner loss starts with one of four things. A lost seed phrase, with no backup and no recovery. Coins sent on the wrong network. A fake website or a fake support agent who tricks you into signing. And rushing: urgency and fear of missing out beating good habits. Module 0 exists to close all four doors before you move real money.",
    chapter="6 · Where beginners get hurt")
img(D + "scam-patterns.png", "Recognise the tricks",
    "Scams in crypto follow patterns, and once you've seen them, they're much easier to spot. Fake sites, with look-alike web addresses, often bought as sponsored search ads. Drainers: a single signature that quietly grants a stranger access to everything. Fake support, in direct messages you never asked for, asking for your seed phrase. And poisoned addresses: a look-alike address slipped into your history, hoping you'll copy it by mistake. The pattern is always the same. Pressure, and a shortcut around your own checks.",
    chapter="6 · Where beginners get hurt", zoom={"x": 0.37, "y": 0.5, "s": 1.35, "at": 2})
img(D + "security-baseline.png", "From Lesson 0.8",
    "So Sam finished the module with a security baseline, four habits that prevent most losses. A hardware wallet, once the amount matters, so the keys never touch the internet. Unique passwords in a password manager, and two-factor everywhere. Never sharing keys, with anyone, for any reason. And bookmarking the apps they use, never following links to wallets or DeFi apps.",
    chapter="6 · Where beginners get hurt")
sc("bullets", "And there are three rules that sit above everything else in this program. Only use money you can afford to lose while you learn. Never trust anyone who promises returns, including anyone who says they're from us. And slow is safe: there's no deadline in crypto that's worth a mistake you can't undo.",
   chapter="6 · Where beginners get hurt", title="Three rules above everything", check=False,
   items=["Only money you can afford to lose", "Never trust promised returns", "Slow is safe: no deadline is worth it"])
sc("quiz", "Last quick check. A message says a new token will double in an hour and asks Sam to connect their wallet through a link. What's the right move? [[pause 4]] The answer: ignore it. Urgency, a promised return and a link are three warning signs at once. Only use bookmarked sites.",
   chapter="6 · Where beginners get hurt", n=3, of=3, q="A message says a token will “double in an hour” and asks Sam to connect through a link. What's the right move?",
   a="Ignore it. Urgency, promised returns and a link are three warning signs. Only use bookmarked sites.")

# ---------------------------------------------------------------- chapter 7: your path
sc("title", "Chapter seven. Your path through Module Zero.", "Chapter 7. Your path through Module 0.",
   chapter="7 · Your path", eyebrow="Chapter 7", num="7", title="Your path through Module 0", sub="Nine short stops, from knowing nothing to set up safely.")
img(D + "story-module0-journey.png", "Nine stops",
    "Here's your journey, stop by stop. Zero point zero, the Mastery Starter, where you'll see what mastery of this module looks like. Zero point one, money, ledgers and why blockchains exist. Zero point two, opening and securing an exchange. Zero point three, your first buy without overpaying. Zero point four, who holds the keys. Zero point five, setting up and backing up your wallet. Zero point six, networks, gas and your first transfer. Zero point seven, your first DeFi steps, practice mode first. And zero point eight, your security baseline, and the language of DeFi.",
    "Here's your journey, stop by stop. 0.0, the Mastery Starter, where you'll see what mastery of this module looks like. 0.1, money, ledgers and why blockchains exist. 0.2, opening and securing an exchange. 0.3, your first buy without overpaying. 0.4, who holds the keys. 0.5, setting up and backing up your wallet. 0.6, networks, gas and your first transfer. 0.7, your first DeFi steps, practice mode first. And 0.8, your security baseline, and the language of DeFi.",
    chapter="7 · Your path", callouts=[{"x": 0.13, "y": 0.6, "text": "Start here", "at": 1, "below": True}])
img(D + "setup-roadmap.png", "Seven practical steps",
    "Underneath those lessons are seven practical steps, the same ones Sam took. Accounts. The exchange. A first buy. The wallet. A first transfer. Practice DeFi. And your security baseline. Do them in order, with a small learning amount. Allow two to three hours, spread over a few days. There's no rush.",
    "Underneath those lessons are seven practical steps, the same ones Sam took. Accounts. The exchange. A first buy. The wallet. A first transfer. Practice DeFi. And your security baseline. Do them in order, with a small learning amount. Allow 2 to 3 hours, spread over a few days. There's no rush.",
    chapter="7 · Your path")
img("assets/kit/cover.png", "Your checklist",
    "And you won't have to remember any of it. Everything is in the Day-One Setup Kit, a printable checklist in the Start here chapter. Tick each box as you go. When every box is ticked, you're set up safely.",
    "And you won't have to remember any of it. Everything is in the Day-1 Setup Kit, a printable checklist in the Start here chapter. Tick each box as you go. When every box is ticked, you're set up safely.",
    chapter="7 · Your path")
sc("bullets", "Here's how Sam's first week actually went. Day one: a password manager, a secured email, and two-factor authentication. Day two: the exchange account opened and locked down. Day three: a small first buy, and the wallet set up with the backup written on paper. Day four: a restore test, then the first transfer, test amount first. Day five: practice on a test network, one tiny real swap, and the security baseline. About half an hour a day. Nothing heroic.",
   "Here's how Sam's first week actually went. Day 1: a password manager, a secured email, and two-factor authentication. Day 2: the exchange account opened and locked down. Day 3: a small first buy, and the wallet set up with the backup written on paper. Day 4: a restore test, then the first transfer, test amount first. Day 5: practice on a test network, one tiny real swap, and the security baseline. About half an hour a day. Nothing heroic.",
   chapter="7 · Your path", title="Sam's first week", compact=True, check=False,
   items=["Day 1 · Password manager, secure email, 2FA", "Day 2 · Exchange opened and locked down", "Day 3 · Small first buy, wallet set up, backup on paper",
          "Day 4 · Restore test, then first transfer (test first)", "Day 5 · Test network, one tiny real swap, security baseline"])
sc("steps", "Every lesson works the same way. Watch the video. Read the lesson. Do the checklist, for real, with small amounts. Then take the short quiz before moving on. That rhythm is how you build habits, not just knowledge.",
   chapter="7 · Your path", title="How every lesson works",
   steps=["Watch the video", "Read the lesson", "Do the checklist, for real", "Take the quiz"], result="Habits, not just knowledge")

# ---------------------------------------------------------------- ending
sc("statement", "So how did Sam's story end? A week later, Sam had a secured exchange account, a wallet they controlled, a backup they'd tested, a first transfer that arrived safely, and a first practice DeFi transaction. Nothing lost. Nothing rushed. And for the first time, the words on the news actually made sense.",
   chapter="Welcome aboard", kicker="One week later", lines=["Set up safely.", "Nothing lost. Nothing rushed."], sub="Secured exchange · own wallet · tested backup · first transfer · first practice DeFi step")
sc("statement", "Sam didn't need to be technical, and neither do you. You just need to go in order, keep amounts small, and follow the checklist. This is education, not financial advice, and no results are guaranteed. What you'll get is a safe foundation, and a process you understand.",
   chapter="Welcome aboard", kicker="Educational content only", lines=["You don't need to be technical.", "You need to go in order."], sub="Not financial advice. No results are guaranteed. You keep custody, always.")
sc("cta", "That's the story of Module Zero. Now it's your turn. Welcome aboard, operator. Start now with Lesson zero point zero, the Mastery Starter for Module Zero: Crypto From Zero. And when you've finished Module Zero, Module One: Foundations and Safety is waiting for you.",
   "That's the story of Module 0. Now it's your turn. Welcome aboard, operator. Start now with Lesson 0.0, the Mastery Starter for Module 0: Crypto From Zero. And when you've finished Module 0, Module 1: Foundations & Safety is waiting for you.",
   chapter="Welcome aboard", button="Start Lesson 0.0 · Mastery Starter", sub="Module 0: Crypto From Zero · then Module 1: Foundations & Safety")

spec = {"id": "module-00-intro", "title": "Module 0 · Crypto From Zero (the story)", "size": [1920, 1080], "music": True, "musicLevel": 0.16,
        "tag": "Module 0", "seed": 31, "maxMinutes": 20,
        "thumbnail": {"title": "Crypto From Zero", "subtitle": "Module 0 · Start here"},
        "use": "Top of the Module 0 chapter: the long, story-led introduction to crypto for complete beginners. Ends by sending the viewer to Lesson 0.0.",
        "scenes": S}
out = ROOT / "video-scripts" / "core" / "module-00-intro.json"
out.write_text(json.dumps(spec, indent=1, ensure_ascii=False))
words = sum(len(s["vo"].replace("[[pause 4]]", "").split()) for s in S)
print(f"{len(S)} scenes, {words} words, est {(words / 171 * 60 + len(S) * 1.3 + 4 * 3) / 60:.1f} min")
