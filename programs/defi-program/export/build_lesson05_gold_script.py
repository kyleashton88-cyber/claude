#!/usr/bin/env python3
"""Gold-standard script for Lesson 0.5, Setting up your wallet and backing it
up (about 13-16 minutes). Promotes the old ~4-minute bullet-heavy script to
the gold standard: software vs hardware wallets, the five-step safe install,
the pre-printed-seed-phrase scam, and Sam's real worked example (Rabby,
restore test, same address) as a flow3d anchor.

Writes video-scripts/gold/lesson-00-5.json (the generator skips lessons with a
gold script). Every illustrative number is labelled as an example on screen
and in the narration. Spoken text (vo) spells numbers for the voice; cap is
the written caption, same sentences."""
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
sc("title", "Lesson zero point five. Setting up your wallet and backing it up. By the end, you'll install a wallet safely, back up the seed phrase correctly, and prove the backup actually works.",
   chapter="Why it matters", eyebrow="Lesson 0.5", num="0.5", title="Setting up your wallet and backing it up",
   sub="You do this once. Get it right once, and it holds for years.")
sc("statement", "Here's why this lesson gets its own dedicated time. Almost every story of someone losing everything traces back to this exact setup moment: a fake app, a backup that was never actually tested, a seed phrase typed into the wrong place. Slow down here, and you close off nearly all of it before you ever hold a real amount.",
   chapter="Why it matters", kicker="Why it matters", lines=["Most losses trace back here.", "To the setup moment, not later."], sub="Slow down now, and you close off nearly all of it before real money is involved.")
sc("pillars", "Here's the plan. First, software wallets versus hardware wallets. Second, the five-step safe install. Third, a scam you need to recognise on sight. Fourth, backing up correctly, and proving the backup actually works. And finally, Sam's real worked example, your checklist and a quiz.",
   chapter="Why it matters", title="What this lesson covers",
   items=[{"icon": "wallet", "title": "Software vs. hardware", "text": "Two kinds of wallet"}, {"icon": "check", "title": "The safe install", "text": "Five steps, in order"},
          {"icon": "alert", "title": "A scam to recognise", "text": "A pre-printed seed phrase"}, {"icon": "key", "title": "Backup and restore test", "text": "Prove it works before you fund it"}])

# ---------------------------------------------------------------- software vs hardware
sc("title", "Two kinds of wallet.", chapter="Two kinds of wallet", eyebrow="Two kinds of wallet", num="2", title="Software or hardware",
   sub="One is free and convenient. One adds a physical layer.")
sc("compare", "A software wallet, a browser extension or a phone app, like MetaMask or Rabby, is free and convenient. Your keys live on your computer or phone. A hardware wallet, a small physical device, like Ledger or Trezor, keeps your keys on the device itself, and every transaction must be approved right there, on its own screen. It's recommended once you're holding more than you'd be upset to lose.",
   chapter="Two kinds of wallet", title="Software wallet vs. hardware wallet",
   left={"label": "Software wallet", "tone": "neutral", "items": ["Browser extension or phone app", "Free, convenient", "Keys live on your computer or phone"]},
   right={"label": "Hardware wallet", "tone": "good", "items": ["A small physical device", "Every transaction approved on its screen", "Recommended once holdings grow"]})
sc("statement", "One rule that matters more than the brand you pick. Buy a hardware wallet only from the manufacturer's own official website, never second-hand, and never from a marketplace listing. A used or third-party device can arrive tampered with, in ways you'd never spot just by looking at it.",
   chapter="Two kinds of wallet", kicker="One rule that matters", lines=["Only from the manufacturer's site.", "Never second-hand."], sub="A tampered device can look completely normal from the outside.")
sc("flow", "Here's exactly why a hardware wallet protects you, even if the computer it's plugged into is already infected. Your computer prepares a transaction, but it can't sign it, only the device holds the key. The device shows you the real destination and amount, on its own trusted screen, one the malware can't touch. You check that screen, not your computer's. And you approve or reject right there, with a physical button.",
   chapter="Two kinds of wallet", title="Why a hardware wallet still protects you",
   nodes=[{"label": "Computer prepares a transaction", "sub": "Possibly infected, possibly not", "icon": "code"}, {"label": "Only the device can sign", "sub": "The key never leaves it", "icon": "key"},
          {"label": "Its own screen shows the truth", "sub": "Malware can't touch that screen", "icon": "eye"}, {"label": "You approve, on the device", "sub": "A physical button, not a click", "icon": "check"}])

# ---------------------------------------------------------------- safe install
sc("title", "The safe install.", chapter="The safe install", eyebrow="The safe install", num="5", title="Five steps, in order",
   sub="Get the app right before you get the words right.")
sc("flow", "Step one: get the wallet from its official website. Type the address yourself, or use the link on the official site, since fake wallet apps and sponsored search ads are a common way beginners get tricked from the very first click. Step two: create a brand new wallet, never one that came from someone else, or pre-printed in a box, a scam we'll walk through next.",
   chapter="The safe install", title="Steps one and two",
   nodes=[{"label": "Get it from the official site", "sub": "Type the address yourself", "icon": "check"}, {"label": "Create a brand new wallet", "sub": "Never one someone else gave you", "icon": "wallet"}])
sc("flow", "Step three: write the seed phrase on paper, or stamp it into metal, in order, spelled exactly. Step four: store it somewhere private, safe from fire and water, and for larger amounts, keep a second copy in a separate location. Step five: never store it in photos, email, notes apps, cloud drives, or password managers, no matter how convenient that feels in the moment.",
   chapter="The safe install", title="Steps three, four and five",
   nodes=[{"label": "Write it on paper or metal", "sub": "In order, spelled exactly", "icon": "doc"}, {"label": "Store it privately", "sub": "Safe from fire and water", "icon": "lock"},
          {"label": "Never store it digitally", "sub": "No photos, email, cloud, or password managers", "icon": "alert", "tone": "bad"}])
sc("flow", "Here's exactly why “just this once” with a cloud photo is so dangerous. You photograph the seed phrase, meaning to delete it later. It syncs automatically to every device tied to that account. That account gets phished, or its password gets reused and leaked elsewhere. And whoever gets in doesn't just see a photo, they see your entire wallet, instantly, with nothing left for you to do about it.",
   chapter="The safe install", title="Why \"just this once\" digitally is so dangerous",
   nodes=[{"label": "You photograph it", "sub": "Meaning to delete it later", "icon": "doc", "tone": "bad"}, {"label": "It syncs automatically", "sub": "To every linked device", "icon": "swap", "tone": "bad"},
          {"label": "That account gets breached", "sub": "Phished, or a reused password", "icon": "alert", "tone": "bad"}, {"label": "Your whole wallet is exposed", "sub": "Instantly, nothing left to do", "icon": "wallet", "tone": "bad"}],
   edges=[{"from": "0", "to": "1", "tone": "bad"}, {"from": "1", "to": "2", "tone": "bad"}, {"from": "2", "to": "3", "tone": "bad"}])
sc("compare", "One nuance on paper versus metal. Paper is free and fine for most people, but it can burn, soak through, or fade over years. Metal, a stamped plate, costs more, but survives a house fire or a flood that would destroy paper outright. Neither replaces having a second copy in a separate location; that habit matters more than which material you choose.",
   chapter="The safe install", title="Paper vs. metal",
   left={"label": "Paper", "tone": "neutral", "items": ["Free, fine for most people", "Can burn, soak through, or fade"]},
   right={"label": "Metal", "tone": "good", "items": ["Costs more", "Survives fire and flood"]})
sc("quiz", "Quick check. Why get the wallet app from the official website specifically, rather than the first search result? [[pause 4]] The answer: sponsored search ads and fake apps are a common scam. Typing the address yourself avoids that trap at the very first step.",
   chapter="The safe install", n=1, of=4, q="Why get the wallet app from the official website specifically?", a="Sponsored search ads and fake apps are a common scam. Typing the address yourself avoids it at the first step.")

# ---------------------------------------------------------------- the scam
sc("title", "A scam to recognise on sight.", chapter="A scam to recognise", eyebrow="A scam to recognise", num="1", title="A pre-printed seed phrase",
   sub="If the words are already there, walk away.")
sc("flow", "Here's exactly how this scam works. You buy what looks like a genuine hardware wallet, sometimes even from a real-looking store page. Inside the box is a card with twenty-four words already printed on it, presented as your seed phrase, ready to go. You fund the wallet, trusting those words. And the scammer, who wrote down that same seed phrase before ever selling you the box, drains it, often within minutes.",
   chapter="A scam to recognise", title="How the pre-printed scam works",
   nodes=[{"label": "You buy a device", "sub": "Sometimes a real-looking listing", "icon": "bank"}, {"label": "24 words, already printed", "sub": "Presented as your seed phrase", "icon": "doc", "tone": "bad"},
          {"label": "You fund the wallet", "sub": "Trusting those words", "icon": "coins", "tone": "bad"}, {"label": "The scammer already has it", "sub": "They wrote it down before selling it", "icon": "alert", "tone": "bad"}],
   edges=[{"from": "0", "to": "1", "tone": "bad"}, {"from": "1", "to": "2", "tone": "bad"}, {"from": "2", "to": "3", "tone": "bad"}])
sc("statement", "Here's the one fact that makes this scam avoidable every time. A genuine device generates your seed phrase itself, fresh, the first time you set it up, and shows it to you once, on its own screen. If words are already printed anywhere in the box, on a card, a sticker, a slip of paper, that box has been compromised. Don't use it. Return it, and buy again from the manufacturer directly.",
   chapter="A scam to recognise", kicker="The one fact that saves you", lines=["A real device generates it fresh.", "Never comes pre-printed."], sub="Words already in the box means the box has been compromised. Don't use it.")

# ---------------------------------------------------------------- backup and restore
sc("title", "Backing it up correctly.", chapter="Backup and restore test", eyebrow="Backup and restore test", num="1", title="On paper. Never digital.",
   sub="And then prove it, before you fund it.")
img(D + "seed-backup.png", "Seed phrase: do and don't",
    "Here's the do-and-don't in one picture. Do: paper or metal, private, safe from fire and water. Don't: photos, email, notes apps, cloud drives, password managers, anything connected to the internet, ever.",
    chapter="Backup and restore test")
sc("flow3d", "And here's the step almost every beginner skips: proving the backup actually works, before there's anything at risk. Remove the wallet, or use a second device. Choose restore, not create new. Restore with your written backup words, in order. And check that the exact same address appears. If it does, your backup is real. If it doesn't, you've just found a mistake while it cost you nothing.",
   chapter="Backup and restore test", title="Prove the backup works",
   nodes=[{"label": "Remove the wallet", "sub": "Or use a second device", "icon": "wallet"}, {"label": "Choose \"restore\"", "sub": "Not \"create new\"", "icon": "swap"},
          {"label": "Restore with backup words", "sub": "In order", "icon": "doc"}, {"label": "Same address appears?", "sub": "That's proof it's real", "icon": "check"}])
sc("bullets", "Here's what a restore test actually catches, that just glancing at your paper never would. A word written down slightly wrong. Two words swapped in order, easy to do without noticing. A word that's hard to read back later, your own handwriting working against you. Every one of these breaks the restore completely, and every one of them is invisible until you actually try it.",
   chapter="Backup and restore test", title="What a restore test actually catches",
   items=["A word written slightly wrong", "Two words swapped in order", "Handwriting that's hard to read back later"])
sc("quiz", "Quick check. Why do this restore test with nothing in the wallet yet? [[pause 4]] The answer: to prove your written backup is correct while nothing is actually at risk. If the backup is wrong, you find out for free.",
   chapter="Backup and restore test", n=2, of=4, q="Why do the restore test before depositing anything?", a="To prove your written backup is correct while nothing is at risk. If it's wrong, you find out for free.")
sc("statement", "And one reminder from earlier in this module, worth repeating here. Your seed phrase's words come from a standard list of two thousand and forty-eight, exactly like Lesson zero point zero covered. That's also why a restore test with even one wrong word fails completely: there's no “close enough” with a system built to be unguessable.",
   "And one reminder from earlier in this module, worth repeating here. Your seed phrase's words come from a standard list of 2,048, exactly like Lesson 0.0 covered. That's also why a restore test with even one wrong word fails completely: there's no \"close enough\" with a system built to be unguessable.",
   chapter="Backup and restore test", kicker="A reminder from Lesson 0.0", lines=["2,048 possible words.", "No \"close enough.\""], sub="The same unguessability that protects you also means one wrong word fails the whole restore.")
sc("statement", "One more question worth answering honestly, even though this program stops short of full estate planning: what happens to this backup if something happens to you? A written seed phrase that only you know the location of can be permanently lost to the people who'd need it. A brief, trusted note about where it lives, kept separately from the phrase itself, is worth more thought than most people give it. And none of this needs to happen in one rushed sitting either: installing, writing the backup, and the restore test can each take their own quiet ten minutes.",
   chapter="Backup and restore test", kicker="One honest question", lines=["What if something happens to you?", "A location note, kept separately, helps."], sub="None of this needs one rushed sitting. Three quiet, separate moments works just as well.")

# ---------------------------------------------------------------- worked example
sc("title", "Sam's worked example.", chapter="Sam's worked example", eyebrow="Sam's worked example", num="1", title="Install, write, restore, confirm",
   sub="Exactly what doing this looks like.")
sc("steps", "Here's exactly what Sam does. Installs Rabby, from its official site. Writes the twelve words onto the blank card that came in the hardware wallet box, since a genuine box's card always arrives blank. Removes the wallet from the computer, and restores it on a laptop instead, using only the written words. Sees the exact same address appear: zero x four b, dot dot dot, e one. And only then, with the restore already proven, sends any real money to it.",
   "Here's exactly what Sam does. Installs Rabby, from its official site. Writes the 12 words onto the blank card that came in the hardware wallet box, since a genuine box's card always arrives blank. Removes the wallet from the computer, and restores it on a laptop instead, using only the written words. Sees the exact same address appear: 0x4b...e1. And only then, with the restore already proven, sends any real money to it.",
   chapter="Sam's worked example", title="Sam's setup",
   steps=["Installs Rabby from its official site", "Writes the 12 words on the box's blank card", "Restores on a separate laptop", "Sees the same address: 0x4b...e1", "Only then sends real money"],
   result="Same address confirmed. The backup is proven, before a cent is at risk.")
sc("statement", "Notice the detail that made this safe: the card in Sam's box arrived blank. That's exactly what a genuine device does, it generates the words with you, it never hands them to you pre-written. That one blank card is the whole tell, and it's the same check worth making the moment any hardware wallet box is opened, regardless of the brand.",
   chapter="Sam's worked example", kicker="The tell", lines=["The card arrived blank.", "That's exactly what a real one does."], sub="A genuine device generates the words with you. It never hands them to you pre-written.")

# ---------------------------------------------------------------- checklist and quiz
sc("title", "Checklist and quiz.", chapter="Checklist and quiz", eyebrow="Checklist and quiz", num="4", title="Confirm you've got it",
   sub="Four boxes.")
sc("bullets", "Here's this lesson's checklist. Wallet installed from the official website. New seed phrase written on paper or metal, never digital. Restore test done, and the same address appeared. And a hardware wallet planned for larger amounts, bought directly from the maker.",
   chapter="Checklist and quiz", title="Before you move on", numbered=True,
   items=["Wallet installed from the official website", "New seed phrase, on paper or metal, never digital", "Restore test done: same address appeared", "Hardware wallet planned for larger amounts (from the maker)"])
sc("quiz", "Question three. A wallet box arrives with a card already showing twenty-four words. What do you do? [[pause 4]] The answer: don't use it. It's a scam. A genuine device generates your seed phrase itself, and never hands it to you pre-printed.",
   "Question three. A wallet box arrives with a card already showing 24 words. What do you do? [[pause 4]] The answer: don't use it. It's a scam. A genuine device generates your seed phrase itself, and never hands it to you pre-printed.",
   chapter="Checklist and quiz", n=3, of=4, q="A wallet box arrives with a card already showing 24 words. What do you do?", a="Don't use it. It's a scam. A genuine device generates your seed phrase itself, never pre-printed.")
sc("quiz", "Question four. Is a photo of your seed phrase, stored in your cloud drive, a safe backup? [[pause 4]] The answer: no. Anyone who gets into that account can take everything. Paper or metal, offline, is the only safe form.",
   chapter="Checklist and quiz", n=4, of=4, q="Is a cloud-drive photo of your seed phrase a safe backup?", a="No. Anyone who gets into that account can take everything. Paper or metal, offline, is the only safe form.")

# ---------------------------------------------------------------- recap
sc("flow", "Here's the whole lesson, recapped as one loop. Install from the official site. Write the seed phrase on paper or metal, never digitally. Prove the restore works, with nothing at risk. Only then, fund it. And for larger amounts, move to a hardware wallet, bought directly from the maker. Do those five things, and this lesson is done.",
   chapter="Recap and next", title="This lesson, recapped as one loop", layout="cycle",
   nodes=[{"label": "Install from the official site", "icon": "check"}, {"label": "Write it on paper or metal", "icon": "doc"}, {"label": "Prove the restore works", "icon": "swap"},
          {"label": "Only then fund it", "icon": "coins"}, {"label": "Hardware wallet for larger amounts", "icon": "lock"}])
sc("statement", "This is education, not financial advice. Set up your own wallet carefully and at your own pace, and nobody from this program will ever ask for your seed phrase, private keys or account access.",
   chapter="Recap and next", kicker="A reminder", lines=["Take your own pace here.", "We never ask for your keys."], sub="Not financial advice. This step is worth doing carefully.")
sc("cta", "That's setting up your wallet and backing it up. Install it safely, back it up on paper, and prove the restore before you trust it. Next up, Lesson zero point six: networks, gas, and your first transfer.",
   chapter="Recap and next", button="Next: Lesson 0.6", sub="Networks, gas and your first transfer")

spec = {"id": "lesson-00-5", "title": "Lesson 0.5: Setting up your wallet and backing it up", "size": [1920, 1080], "group": "lessons", "maxMinutes": 25, "tag": "Lesson 0.5",
        "gold": True, "seed": 45,
        "use": "Lesson 0.5 page in the Whop course. Gold-standard script: software vs hardware wallets, the five-step safe install, the pre-printed-seed-phrase scam, and Sam's worked example (Rabby, restore test, same address) as a flow3d anchor.",
        "thumbnail": {"title": "Setting up and backing up", "subtitle": "Lesson 0.5"}, "scenes": S}
out = ROOT / "video-scripts" / "gold" / "lesson-00-5.json"
out.write_text(json.dumps(spec, indent=1, ensure_ascii=False))
words = sum(len(s["vo"].replace("[[pause 4]]", "").split()) for s in S)
print(f"{len(S)} scenes, {words} words, est {(words / 171 * 60 + len(S) * 1.3 + 4 * 3) / 60:.1f} min")
