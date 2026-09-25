#!/usr/bin/env python3
"""Script for "How to use your Day-1 Setup Kit" (7-10 minutes).
Writes video-scripts/core/day1-kit-guide.json. The kit's own sections (assets/kit/,
cropped from the PDF by build_kit_crops.py) are shown next to the lesson diagrams."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
S = []


def sc(type_, vo, cap=None, **k):
    S.append({"type": type_, **k, "vo": vo, **({"cap": cap} if cap else {})})


def img(src, eyebrow, vo, cap=None, **k):
    sc("image", vo, cap, src=src, eyebrow=eyebrow, wide=True, **k)


sc("logo", "Welcome. In this video, I'll show you exactly how to use your Day-One Setup Kit. It's the checklist that takes you from knowing nothing about crypto to set up safely, and ready for Module One. We'll go through it part by part, with what to do, why it matters, and the mistakes to avoid.",
   "Welcome. In this video, I'll show you exactly how to use your Day-1 Setup Kit. It's the checklist that takes you from knowing nothing about crypto to set up safely, and ready for Module 1. We'll go through it part by part, with what to do, why it matters, and the mistakes to avoid.",
   chapter="Intro", tagline="How to use your Day-1 Setup Kit")
img("assets/kit/cover.png", "The Day-1 Setup Kit", "Here's the kit. It's a short printable P.D.F., four pages, in the Start here section of the course. It holds a setup roadmap, a checklist in six parts, ten rules to keep forever, and two reference diagrams. Download it, and if you can, print it. Ticking boxes on paper, with a pen, is part of the point.",
    "Here's the kit. It's a short printable PDF, four pages, in the Start here section of the course. It holds a setup roadmap, a checklist in six parts, ten rules to keep forever, and two reference diagrams. Download it, and if you can, print it. Ticking boxes on paper, with a pen, is part of the point.",
    chapter="What it is")
img("assets/kit/needs.png", "What you need", "Before you start, gather what you'll need. Photo I.D. for the exchange's identity checks. A bank account. A smartphone for an authenticator app. A computer with an up-to-date browser. Pen and paper, or a metal backup plate, for your seed phrase. And, optionally, a hardware wallet bought directly from the maker. Plan on two to three hours in total, spread over a few days, because identity checks and bank deposits can take time.",
    "Before you start, gather what you'll need. Photo ID for the exchange's identity checks. A bank account. A smartphone for an authenticator app. A computer with an up-to-date browser. Pen and paper, or a metal backup plate, for your seed phrase. And, optionally, a hardware wallet bought directly from the maker. Plan on 2 to 3 hours in total, spread over a few days, because identity checks and bank deposits can take time.",
    chapter="What it is")
sc("pillars", "Four ground rules for using the kit. Go in order, because every part depends on the one before. Use a small learning amount only, money you could lose without it hurting. Tick each box only when it's truly done, not when you've read it. And write things down as you go, because your records sheet starts here.",
   chapter="How to use it", title="Four ground rules",
   items=[{"icon": "compass", "title": "In order", "text": "Each part depends on the one before"}, {"icon": "coins", "title": "Small amount", "text": "Money you could lose without it hurting"},
          {"icon": "check", "title": "Tick when done", "text": "Not when you've read it"}, {"icon": "book", "title": "Write it down", "text": "Your records sheet starts here"}])
img("assets/diagrams/setup-roadmap.png", "Your setup roadmap", "Here's the whole journey on one page. Accounts. Exchange. First buy. Wallet. First transfer. Practice DeFi. And a security baseline. The checklist follows exactly this order, in six parts, A to F. Let's go through each one.",
    "Here's the whole journey on one page. Accounts. Exchange. First buy. Wallet. First transfer. Practice DeFi. And a security baseline. The checklist follows exactly this order, in six parts, A to F. Let's go through each one.",
    chapter="How to use it")

# Part A
img("assets/kit/part-a.png", "Part A · Accounts · about 45 min", "Part A is accounts, and it takes about forty-five minutes. Start with a password manager, and write its master password down somewhere safe. Secure your email with a unique password and an authenticator app, because your email is the key to every other account. Then choose an exchange that's legally available where you live and has a solid reputation, open your account, and complete the identity checks.",
    "Part A is accounts, and it takes about 45 minutes. Start with a password manager, and write its master password down somewhere safe. Secure your email with a unique password and an authenticator app, because your email is the key to every other account. Then choose an exchange that's legally available where you live and has a solid reputation, open your account, and complete the identity checks.",
    chapter="Part A · Accounts")
img("assets/diagrams/exchange-lockdown.png", "Lock the exchange down first", "Before you deposit a cent, lock the exchange down. Turn on two-factor with an authenticator app or a security key, not text messages, which can be hijacked. Store the backup codes offline. Switch on the anti-phishing code, so every real email from the exchange shows your secret word. And switch on the withdrawal allowlist, so money can only ever leave to addresses you've approved.",
    chapter="Part A · Accounts")
# Part B
img("assets/kit/part-b.png", "Part B · First purchase · about 20 min", "Part B is your first purchase, about twenty minutes. Deposit a small learning amount, using the cheapest method your exchange offers. Buy a little E.T.H., which you'll need to pay network fees, and some U.S.D.C., a dollar stablecoin you'll practise with. Then try one limit order, so you learn to set your own price instead of taking whatever the market gives you.",
    "Part B is your first purchase, about 20 minutes. Deposit a small learning amount, using the cheapest method your exchange offers. Buy a little ETH, which you'll need to pay network fees, and some USDC, a dollar stablecoin you'll practise with. Then try one limit order, so you learn to set your own price instead of taking whatever the market gives you.",
    chapter="Part B · First purchase")
img("assets/diagrams/first-buy-costs.png", "Why the cheapest route matters", "Here's why the method matters. The price on the chart is not what you pay. You lose a little to the spread, a little to the trading fee, and a little more to the network when you withdraw. Compare what actually lands in your wallet, not the headline price.",
    chapter="Part B · First purchase")
sc("steps", "The last box in Part B is your records sheet, and it's simpler than it sounds. One row for every action. The date. What you did. The amount. The price. And the fees. Here's an example row for a small E.T.H. purchase. Keep it from day one, and tax time, and your own reviews, become easy.",
   "The last box in Part B is your records sheet, and it's simpler than it sounds. One row for every action. The date. What you did. The amount. The price. And the fees. Here's an example row for a small ETH purchase. Keep it from day one, and tax time, and your own reviews, become easy.",
   chapter="Part B · First purchase", title="Your records sheet: one row per action",
   steps=["Date · Action · Amount · Price · Fees", "Example: 25 Sep · Buy · 0.01 ETH · $3,000 · $0.50", "Example: 25 Sep · Withdraw · 0.01 ETH · — · network fee"],
   result="Start it today; update it every time")
# Part C
img("assets/kit/part-c.png", "Part C · Your wallet · about 30 min", "Part C is your wallet, about thirty minutes. Install it only from the official website, ideally in a separate browser profile that you use just for crypto. When it shows you a new seed phrase, write it down, on paper or metal, in order. Never type it into a computer, never photograph it, and never store it in the cloud.",
    "Part C is your wallet, about 30 minutes. Install it only from the official website, ideally in a separate browser profile that you use just for crypto. When it shows you a new seed phrase, write it down, on paper or metal, in order. Never type it into a computer, never photograph it, and never store it in the cloud.",
    chapter="Part C · Your wallet")
img("assets/diagrams/seed-backup.png", "Seed phrase: do and don't", "The seed phrase is your wallet. Anyone who has it owns your funds, and if you lose it, nobody can recover them for you. Here are the do's and don'ts. Write it on paper or stamp it in metal, in order, keep it private and safe from fire and water, and keep a second copy elsewhere once the amount grows. Never photograph it or keep it in notes, email or the cloud, never share it, and never use a phrase that came pre-printed or from someone else.",
    "The seed phrase is your wallet. Anyone who has it owns your funds, and if you lose it, nobody can recover them for you. Here are the dos and don'ts. Write it on paper or stamp it in metal, in order, keep it private and safe from fire and water, and keep a second copy elsewhere once the amount grows. Never photograph it or keep it in notes, email or the cloud, never share it, and never use a phrase that came pre-printed or from someone else.",
    chapter="Part C · Your wallet")
sc("steps", "Then do the restore test. It's the most skipped box in the kit, and the most important. Before you put money in, note your wallet address. Remove the wallet from the app. Restore it from your written seed phrase. Then check that the same address appears. If it does, your backup works. If it doesn't, you found out while the wallet was empty. Finally, save the wallet's address, the address only, never the seed, in your password manager.",
   chapter="Part C · Your wallet", title="The restore test",
   steps=["Note your wallet address", "Remove the wallet from the app", "Restore it from your written seed phrase", "Check: the same address appears"],
   result="Backup proven, before any real money goes in")
# Part D
img("assets/kit/part-d.png", "Part D · First transfer · about 20 min", "Part D is your first transfer, about twenty minutes. Choose a low-fee network that both your exchange and your wallet support. Then send a small test first, for example ten dollars of E.T.H., and wait until it arrives. Only then send the rest of your learning funds, and add your wallet's address to the exchange allowlist. Finally, find the transfer on a block explorer, so you can see it for yourself.",
    "Part D is your first transfer, about 20 minutes. Choose a low-fee network that both your exchange and your wallet support. Then send a small test first, for example $10 of ETH, and wait until it arrives. Only then send the rest of your learning funds, and add your wallet's address to the exchange allowlist. Finally, find the transfer on a block explorer, so you can see it for yourself.",
    chapter="Part D · First transfer")
img("assets/diagrams/first-transfer.png", "Your first transfer", "Here's the transfer step by step. The network you choose at the exchange must match the network your wallet is on. Copy the address with the wallet's copy button, never type it, and check at least the first and last six characters. Send the small test. Wait until it arrives. Then send the rest, and keep a little E.T.H. on that network for gas. The test costs one extra small fee, and it protects you from the most common, and most permanent, beginner mistake.",
    "Here's the transfer step by step. The network you choose at the exchange must match the network your wallet is on. Copy the address with the wallet's copy button, never type it, and check at least the first and last six characters. Send the small test. Wait until it arrives. Then send the rest, and keep a little ETH on that network for gas. The test costs one extra small fee, and it protects you from the most common, and most permanent, beginner mistake.",
    chapter="Part D · First transfer")
# Part E
img("assets/kit/part-e.png", "Part E · Practice DeFi · about 30 min", "Part E is practice, about thirty minutes. Add the Sepolia test network to your wallet, and get free test E.T.H. from a faucet. Make one practice transaction there, where nothing real is at stake. Then make one tiny real swap on a low-fee network, with a limited approval. And afterwards, revoke that approval.",
    "Part E is practice, about 30 minutes. Add the Sepolia test network to your wallet, and get free test ETH from a faucet. Make one practice transaction there, where nothing real is at stake. Then make one tiny real swap on a low-fee network, with a limited approval. And afterwards, revoke that approval.",
    chapter="Part E · Practice DeFi")
img("assets/diagrams/practice-mode-first.png", "Practice mode first", "The order is the lesson. Test network first, with free test tokens. Connect only from a bookmarked site. Read what the wallet asks you to sign: what, to whom, how much. And the tiny real amount comes last, only after the test works.",
    chapter="Part E · Practice DeFi")
img("assets/diagrams/approval-anatomy.png", "Why you revoke the approval", "Here's why the last box matters. When an app asks to move your tokens, it's asking for an approval, and an approval stays open after the trade is done. Give an exact amount, not unlimited, and revoke it afterwards. You'll learn to read approvals properly in Module One, but this habit starts today.",
    "Here's why the last box matters. When an app asks to move your tokens, it's asking for an approval, and an approval stays open after the trade is done. Give an exact amount, not unlimited, and revoke it afterwards. You'll learn to read approvals properly in Module 1, but this habit starts today.",
    chapter="Part E · Practice DeFi", callouts=[{"x": 0.83, "y": 0.45, "text": "Exact, not infinite", "at": 2}])
# Part F
img("assets/kit/part-f.png", "Part F · Security baseline · about 15 min", "Part F is your security baseline, about fifteen minutes. Read the ten rules, and make sure you understand each one. Bookmark the sites you use, and never reach them from ads or messages. Order a hardware wallet from the maker, for when the amount starts to matter. And bring your records sheet up to date.",
    "Part F is your security baseline, about 15 minutes. Read the ten rules, and make sure you understand each one. Bookmark the sites you use, and never reach them from ads or messages. Order a hardware wallet from the maker, for when the amount starts to matter. And bring your records sheet up to date.",
    chapter="Part F · Security baseline")
img("assets/kit/rules-1.png", "The 10 rules · 1 to 5", "Here are the ten rules, the part of the kit you'll keep forever. One. Never share your seed phrase; no real person or company will ever ask for it. Two. Bookmark the sites you use, and never reach them from ads, messages or emails. Three. Nobody legitimate messages you first offering help, investments or recovery. Four. Guaranteed returns are a scam, always. Five. Read every wallet prompt before approving: what, how much, and to whom.",
    chapter="Part F · Security baseline")
img("assets/kit/rules-2.png", "The 10 rules · 6 to 10", "Six. Test first, with a small amount, on anything new. Seven. Use a hardware wallet once the amount matters to you. Eight. Keep your devices updated, and use a separate browser profile for crypto. Nine. Keep records of every buy, sell, transfer and fee. And ten. If something feels urgent, stop. Scammers create urgency. Real opportunities wait.",
    chapter="Part F · Security baseline")
img("assets/diagrams/scam-patterns.png", "What the rules protect you from", "These rules exist because the same attacks happen every day. Fake websites that look exactly like the real one. Drainers that empty a wallet with a single signature. Fake support staff who ask for your seed phrase. And poisoned addresses planted in your history. The ten rules close every one of these doors.",
    chapter="Part F · Security baseline")

# mistakes, help, quiz, finish
sc("bullets", "Here are the mistakes we see most often. Skipping the restore test. Choosing text-message two-factor because it's easier. Sending on the wrong network, or skipping the test transfer. Storing the seed phrase in a notes app or a photo. And rushing to finish in one sitting. Take the few days. It's worth it.",
   chapter="Common mistakes", title="The mistakes to avoid", check=False,
   items=["Skipping the restore test", "Text-message 2FA instead of an app", "Wrong network, or no test transfer", "Seed phrase in a notes app or photo", "Rushing it in one sitting"])
sc("bullets", "If you get stuck. Identity checks and bank deposits can take a day or two; that's normal, so move on to reading and come back. If a transfer hasn't arrived, find it on the block explorer before doing anything else. And if anyone messages you offering to help, that's a scammer. Our support will never message you first, and never asks for your seed phrase.",
   chapter="If you get stuck", title="If you get stuck", numbered=True,
   items=["ID checks or deposits slow? Normal: wait a day", "Transfer missing? Look it up on the explorer first", "Someone offers help in a DM? It's a scam"])
sc("quiz", "Let's check two things. Question one. Why do you send a small test before the full transfer? [[pause 4]] The answer: to prove the network and address are right, while a mistake would only cost the test amount.",
   chapter="Quiz", n=1, of=2, q="Why send a small test before the full transfer?", a="To prove the network and address are right, while a mistake costs only the test amount.")
sc("quiz", "Question two. When is Part C really done? [[pause 4]] The answer: when the restore test has passed, and the same address appears, not just when the seed phrase is written down.",
   chapter="Quiz", n=2, of=2, q="When is Part C really done?", a="When the restore test has passed and the same address appears, not just when the seed is written down.")
sc("statement", "When every box is ticked, you're done. Your accounts are secured, your wallet is backed up and proven, you've made a real transfer and a real swap, and you have a security baseline you'll keep for life. You're ready for Module One: Foundations and Safety.",
   "When every box is ticked, you're done. Your accounts are secured, your wallet is backed up and proven, you've made a real transfer and a real swap, and you have a security baseline you'll keep for life. You're ready for Module 1: Foundations and Safety.",
   chapter="Finish", kicker="All ticked?", lines=["You're ready", "for Module 1."], sub="Secured, backed up, tested, and set for life.")
sc("cta", "Download the kit, print it, and start with Part A today. Take your time. I'll see you in Module One.", "Download the kit, print it, and start with Part A today. Take your time. I'll see you in Module 1.",
   chapter="Finish", button="Open the Day-1 Setup Kit", sub="Educational content only · Not financial advice")

spec = {"id": "day1-kit-guide", "title": "How to use your Day-1 Setup Kit", "size": [1920, 1080], "music": True, "musicLevel": 0.16,
        "tag": "Day-1 Setup Kit", "seed": 24, "maxMinutes": 12,
        "thumbnail": {"title": "Your Day-1 Setup Kit", "subtitle": "Start here"},
        "use": "Start here chapter and Module 0: a walkthrough of the Day-1 Setup Kit, part by part.", "scenes": S}
out = ROOT / "video-scripts" / "core" / "day1-kit-guide.json"
out.write_text(json.dumps(spec, indent=1, ensure_ascii=False))
words = sum(len(s["vo"].replace("[[pause 4]]", "").split()) for s in S)
print(f"{len(S)} scenes, {words} words, est {(words / 171 * 60 + len(S) * 1.3 + 8) / 60:.1f} min")
