#!/usr/bin/env python3
"""Gold-standard script for Lesson 0.4, Exchange account vs your own wallet: who
holds the keys? (about 12-15 minutes). Promotes the old ~2-minute bullet-heavy
script to the gold standard: custodial vs self-custody as a full five-row
compare, addresses vs seed phrases, a flow3d anchor for what self-custody
actually does, and an illustrative worked scenario since this lesson's source
has no worked example of its own.

Writes video-scripts/gold/lesson-00-4.json (the generator skips lessons with a
gold script). Every illustrative scenario is labelled as an example on screen
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
sc("title", "Lesson zero point four. Exchange account versus your own wallet: who holds the keys? By the end, you'll understand custody, and decide what stays on the exchange and what moves to your own wallet.",
   chapter="Why it matters", eyebrow="Lesson 0.4", num="0.4", title="Exchange account vs. your own wallet",
   sub="Who holds the keys, and what that actually means.")
sc("statement", "There's a saying in crypto that sounds harsh the first time you hear it. Not your keys, not your coins. It means exactly what it says. If someone else holds the keys to your crypto, you don't control it, you're trusting them to give it back. This lesson is about understanding that trade-off, not fearing it.",
   chapter="Why it matters", kicker="A well-known saying", lines=["\"Not your keys,\"", "\"not your coins.\""], sub="If someone else holds the keys, you're trusting them to give your crypto back.")
sc("pillars", "Here's the plan. First, what it means to hold crypto on an exchange, custodial. Second, what it means to hold it yourself, self-custody. Third, the full comparison, five ways, side by side. And finally, an illustrative scenario, your checklist and a quiz.",
   chapter="Why it matters", title="What this lesson covers",
   items=[{"icon": "bank", "title": "On an exchange", "text": "Custodial: they hold the keys"}, {"icon": "wallet", "title": "In your own wallet", "text": "Self-custody: you hold the keys"},
          {"icon": "check", "title": "Five-way comparison", "text": "Side by side, honestly"}, {"icon": "users", "title": "A scenario, checklist, quiz", "text": "Make it concrete"}])
img(D + "custody-split.png", "Who holds the keys",
    "Here's the whole lesson in one picture. On the left, an exchange holding your keys for you. On the right, a wallet where you hold them yourself. Same crypto, two very different arrangements.",
    chapter="Why it matters")

# ---------------------------------------------------------------- custodial
sc("title", "On an exchange.", chapter="On an exchange", eyebrow="On an exchange", num="1", title="Custodial: they hold the keys",
   sub="Easy, recoverable, but not fully yours to control.")
sc("flow", "Here's how custody works when you leave crypto on an exchange. The exchange holds the actual keys. It owes you the balance you see in your account. If you forget your password, you can recover access with I.D., because the exchange is the one keeping the books. But if the exchange fails, freezes withdrawals, or is hacked, your money is at risk, because you never held the keys yourself.",
   "Here's how custody works when you leave crypto on an exchange. The exchange holds the actual keys. It owes you the balance you see in your account. If you forget your password, you can recover access with ID, because the exchange is the one keeping the books. But if the exchange fails, freezes withdrawals, or is hacked, your money is at risk, because you never held the keys yourself.",
   chapter="On an exchange", title="Custodial, step by step",
   nodes=[{"label": "Exchange holds the keys", "sub": "It owes you the balance", "icon": "bank"}, {"label": "Forgot your password?", "sub": "Recoverable with ID", "icon": "key"},
          {"label": "Exchange fails or is hacked", "sub": "Your money is at risk", "icon": "alert", "tone": "bad"}])

# ---------------------------------------------------------------- self-custody
sc("title", "In your own wallet.", chapter="Your own wallet", eyebrow="Your own wallet", num="2", title="Self-custody: you hold the keys",
   sub="Nobody can freeze it. Nobody can recover it for you, either.")
sc("statement", "In your own wallet, you hold the keys, the secret codes that control your crypto. Nobody can freeze it. But that cuts both ways: nobody can recover it for you either, if you lose those keys.",
   chapter="Your own wallet", kicker="The trade-off", lines=["Nobody can freeze it.", "Nobody can recover it for you."], sub="Full control, and full responsibility, in the same package.")
sc("flow3d", "And here's something worth being precise about. A wallet doesn't actually store your coins. The coins live on the blockchain, permanently. Your seed phrase creates your keys. Your keys prove you own an address, and let you sign transactions from it. The wallet app is just the interface. Lose the app, restore the seed phrase into any other one, and every key, every address, and every balance comes back exactly as it was.",
   chapter="Your own wallet", title="What a wallet actually holds",
   nodes=[{"label": "Seed phrase", "sub": "12 or 24 words", "icon": "doc"}, {"label": "Creates your keys", "sub": "The secret codes", "icon": "key"},
          {"label": "Proves you own an address", "sub": "And lets you sign from it", "icon": "wallet"}, {"label": "Coins stay on the blockchain", "sub": "The wallet is just the interface", "icon": "layers"}],
   edges=[{"from": "0", "to": "1", "label": "creates"}, {"from": "1", "to": "2", "label": "proves"}, {"from": "1", "to": "3"}])
sc("compare", "Which brings up two very different pieces of information. Your address is like an account number: safe to share, that's how people send you money. Your seed phrase is the master key to everything: never shared, never typed into a website, never photographed.",
   chapter="Your own wallet", title="Address vs. seed phrase",
   left={"label": "Your address", "tone": "good", "items": ["Safe to share, like an account number", "How people send you money"]},
   right={"label": "Your seed phrase", "tone": "bad", "items": ["Never shared, never typed into a site", "Never photographed"]})
sc("quiz", "Quick check. Is your crypto actually stored inside your wallet app? [[pause 4]] The answer: no. It's on the blockchain. The wallet just holds the keys that let you control it.",
   chapter="Your own wallet", n=1, of=4, q="Is your crypto stored inside your wallet app?", a="No. It's on the blockchain. The wallet holds the keys that let you control it.")
sc("compare", "Here's exactly why one side can recover a lost password and the other can't. On an exchange, forgetting your password isn't the end: you contact support, verify your identity with I.D., and they reset access, because they're the ones keeping the account records. In your own wallet, there's no support desk to contact. Nobody is keeping records on your behalf. Only your own seed phrase can rebuild those keys, which is exactly why losing it, with no backup, means the funds are gone for good.",
   "Here's exactly why one side can recover a lost password and the other can't. On an exchange, forgetting your password isn't the end: you contact support, verify your identity with ID, and they reset access, because they're the ones keeping the account records. In your own wallet, there's no support desk to contact. Nobody is keeping records on your behalf. Only your own seed phrase can rebuild those keys, which is exactly why losing it, with no backup, means the funds are gone for good.",
   chapter="Your own wallet", title="Why recovery works so differently",
   left={"label": "Exchange account", "tone": "neutral", "items": ["Contact support, verify with ID", "They reset it: they keep the records"]},
   right={"label": "Your own wallet", "tone": "bad", "items": ["No support desk to contact", "Only your seed phrase can rebuild it"]})
sc("pillars", "One more mental model, worth previewing here even though Module One goes much deeper on it. Custody isn't really all-or-nothing. Many people use a small, everyday wallet for spending and trying things, and a separate, more protected wallet, sometimes on a hardware device, for savings they don't touch often. Same principle as the exchange-versus-wallet split, applied one level deeper.",
   chapter="Your own wallet", title="A preview: tiers, not just two boxes",
   items=[{"icon": "wallet", "title": "An everyday wallet", "text": "Spending, trying things"}, {"icon": "lock", "title": "A protected wallet", "text": "Savings, touched rarely (more in Module 1)"}])

# ---------------------------------------------------------------- the comparison
sc("title", "Five ways, side by side.", chapter="Five-way comparison", eyebrow="Five-way comparison", num="5", title="The full comparison",
   sub="Neither side is simply \"better.\"")
sc("compare", "Who holds the keys? The exchange, or you. Can you recover access if you forget your password? Yes, with I.D., on an exchange. Only with your seed phrase, in your own wallet. Can your funds be frozen? Yes, on an exchange. No, in your own wallet. Can you use DeFi directly? Limited, on an exchange. Yes, in your own wallet. And what's your main risk? On an exchange, it's the company. In your own wallet, it's your own mistakes and scams.",
   "Who holds the keys? The exchange, or you. Can you recover access if you forget your password? Yes, with ID, on an exchange. Only with your seed phrase, in your own wallet. Can your funds be frozen? Yes, on an exchange. No, in your own wallet. Can you use DeFi directly? Limited, on an exchange. Yes, in your own wallet. And what's your main risk? On an exchange, it's the company. In your own wallet, it's your own mistakes and scams.",
   chapter="Five-way comparison", title="Exchange vs. your own wallet",
   left={"label": "Exchange", "tone": "neutral", "items": ["The exchange holds the keys", "Recoverable with ID", "Can be frozen", "DeFi access: limited", "Main risk: the company"]},
   right={"label": "Your wallet", "tone": "good", "items": ["You hold the keys", "Recoverable only with your seed phrase", "Cannot be frozen", "DeFi access: yes", "Main risk: your own mistakes and scams"]})
sc("statement", "Notice that last row especially. Self-custody doesn't remove risk, it relocates it, from a company you can't control to habits you can. That's not a downgrade. It's a different job, and this whole program is here to help you do that job well.",
   chapter="Five-way comparison", kicker="Risk doesn't disappear", lines=["It relocates.", "From a company, to your own habits."], sub="That's not a downgrade. It's a different job, and a learnable one.")
sc("statement", "And this isn't just a hypothetical concern. Crypto's history includes real exchanges that froze withdrawals during a crisis, or failed outright, sometimes for months, sometimes permanently. It also includes real people who lost everything to a mistake in their own wallet: a lost seed phrase, a phishing site. Both risks are real. This program spends real time on both.",
   chapter="Five-way comparison", kicker="Not just hypothetical", lines=["Exchanges have failed.", "Wallets have been mishandled."], sub="Both risks are real. This program spends real time on both.")
sc("bullets", "Why does an exchange freeze withdrawals in the first place? A few common reasons. A regulatory request, forcing a pause while something's investigated. Suspected fraud on an account, theirs or yours. Or a liquidity crunch, if too many people try to withdraw at once and the exchange can't meet every request instantly. None of these can happen to a wallet only you control, because there's no company in the loop to freeze anything.",
   chapter="Five-way comparison", title="Why an exchange freezes withdrawals",
   items=["A regulatory request", "Suspected fraud, on an account", "A liquidity crunch: too many withdrawals at once"])
sc("compare", "And here's why DeFi access is “limited” on an exchange specifically. An exchange only lets you do what its own interface offers: buy, sell, maybe a savings product it built itself. Your own wallet can connect directly to any smart contract on the blockchain, which is the entire rest of the program, from Module One onward.",
   chapter="Five-way comparison", title="Why DeFi access differs",
   left={"label": "Exchange", "tone": "neutral", "items": ["Only what its own interface offers", "Buy, sell, maybe its own savings product"]},
   right={"label": "Your wallet", "tone": "good", "items": ["Connects directly to any smart contract", "The rest of this program runs through this"]})
sc("pillars", "So, practically, what goes where? Keep on an exchange what you're actively trading, or a small amount you check often, since you'll want its convenience and its recoverability. Move to your own wallet what you're saving for the longer term, or what you need for DeFi, since that's where control actually matters.",
   chapter="Five-way comparison", title="Practically, what goes where",
   items=[{"icon": "bank", "title": "Keep on an exchange", "text": "Active trading, small amounts you check often"}, {"icon": "wallet", "title": "Move to your wallet", "text": "Longer-term savings, anything you'll use in DeFi"}])

# ---------------------------------------------------------------- scenario
sc("title", "An illustrative scenario.", chapter="An illustrative scenario", eyebrow="An illustrative scenario", num="2", title="One thousand dollars, split two ways",
   sub="A hypothetical, to make the trade-off concrete.")
sc("statement", "Numbers make trade-offs concrete in a way a rule never quite does. So before the checklist, here's one hypothetical scenario, walked all the way through, showing exactly what each side of the comparison table feels like when something actually goes wrong.",
   chapter="An illustrative scenario", kicker="Making it concrete", lines=["A rule is easy to nod along to.", "A scenario is harder to forget."], sub="One hypothetical, walked all the way through.")
sc("chart", "Here's a hypothetical, to make this concrete, not a real event or a prediction. Sam splits one thousand dollars: half stays on an exchange for easy trading, half moves to Sam's own wallet for DeFi and savings. One difficult week, the exchange pauses withdrawals while it investigates unusual activity. Sam's exchange half is temporarily stuck. Sam's wallet half is completely unaffected, and still fully usable, because nobody but Sam ever held those keys.",
   "Here's a hypothetical, to make this concrete, not a real event or a prediction. Sam splits $1,000: half stays on an exchange for easy trading, half moves to Sam's own wallet for DeFi and savings. One difficult week, the exchange pauses withdrawals while it investigates unusual activity. Sam's exchange half is temporarily stuck. Sam's wallet half is completely unaffected, and still fully usable, because nobody but Sam ever held those keys.",
   chapter="An illustrative scenario", kind="bars", variant="row", title="Sam's $1,000, during a bad week (hypothetical)", sub="Illustrative scenario, not a real event or a prediction",
   bars=[{"label": "On the exchange", "text": "Temporarily stuck, withdrawals paused", "value": 500, "show": "$500 stuck", "tone": "bad"},
         {"label": "In Sam's wallet", "text": "Fully usable the whole time", "value": 500, "show": "$500 usable", "tone": "good"}])
sc("statement", "Notice what this scenario isn't. It isn't a claim that exchanges are dangerous, or that self-custody is risk-free. It's a picture of what “not your keys, not your coins” actually looks like when it matters, and why many people choose to split, rather than put everything in one place.",
   chapter="An illustrative scenario", kicker="What this isn't", lines=["Not \"exchanges are dangerous.\"", "Not \"self-custody is risk-free.\""], sub="It's why many people choose to split, rather than put everything in one place.")
sc("steps", "Here's what actually moving funds from an exchange into your own wallet looks like, step by step. Copy your wallet's receive address. Paste it into the exchange's withdrawal field, and check it carefully. Confirm the network matches on both sides, sending on the wrong one is a real and costly mistake. Send a small test amount first. Confirm it arrives. And only then send the rest.",
   chapter="An illustrative scenario", title="Exchange to wallet, step by step",
   steps=["Copy your wallet's receive address", "Paste it into the exchange's withdrawal field", "Confirm the network matches, on both sides", "Send a small test amount first", "Confirm it arrives, then send the rest"],
   result="A small test first turns a possible disaster into a non-event.")

# ---------------------------------------------------------------- checklist and quiz
sc("title", "Checklist and quiz.", chapter="Checklist and quiz", eyebrow="Checklist and quiz", num="3", title="Confirm you've got it",
   sub="Three boxes.")
sc("bullets", "Here's this lesson's checklist. You can explain custodial versus self-custody in plain words. You know your seed phrase is the wallet, not just a backup of it. And you know an address is safe to share, while a seed phrase never, ever is.",
   chapter="Checklist and quiz", title="Confirm you've got it", numbered=True,
   items=["Can explain custodial vs. self-custody", "Know: the seed phrase is the wallet", "Know: address shareable, seed phrase never"])
sc("quiz", "Question two. What does “not your keys, not your coins” actually mean? [[pause 4]] The answer: if someone else holds the keys, you depend on them to give your crypto back. It's not automatically yours to move whenever you want.",
   chapter="Checklist and quiz", n=2, of=4, q="What does \"not your keys, not your coins\" mean?", a="If someone else holds the keys, you depend on them to give your crypto back.")
sc("quiz", "Question three. Which can you safely share: your address, or your seed phrase? [[pause 4]] The answer: your address. Never your seed phrase, to anyone, ever.",
   chapter="Checklist and quiz", n=3, of=4, q="Which can you safely share: your address or your seed phrase?", a="Your address. Never your seed phrase, to anyone, ever.")
sc("quiz", "Question four. Your funds are frozen by an exchange investigation. Is that possible in your own wallet too? [[pause 4]] The answer: no. Nobody but you holds the keys in your own wallet, so nobody but you can freeze it. The trade-off is that nobody but you can recover it, either.",
   chapter="Checklist and quiz", n=4, of=4, q="Can your own wallet be frozen the way an exchange account can?", a="No. Nobody but you holds the keys, so nobody but you can freeze it - or recover it, if you lose them.")

# ---------------------------------------------------------------- recap
sc("flow", "Here's the whole lesson, recapped as one loop. On an exchange, they hold the keys, easy, but recoverable and freezable by them. In your own wallet, you hold the keys, immune to freezing, but recoverable only by you. Compare the two, honestly, across all five dimensions. And decide what stays where, on purpose, not by accident.",
   chapter="Recap and next", title="This lesson, recapped as one loop", layout="cycle",
   nodes=[{"label": "Exchange: they hold the keys", "icon": "bank"}, {"label": "Easy, but freezable", "icon": "alert"}, {"label": "Wallet: you hold the keys", "icon": "wallet"},
          {"label": "Immune to freezing, yours to lose", "icon": "key"}, {"label": "Decide what stays where", "icon": "check"}])
sc("statement", "This is education, not financial advice. Where you hold your crypto is your decision to make. Base it on your own comfort with each trade-off. And nobody from this program will ever ask for your seed phrase, private keys or account access.",
   chapter="Recap and next", kicker="A reminder", lines=["Your decision, your trade-offs.", "We never ask for your keys."], sub="Not financial advice. Choose what fits your own comfort with each trade-off.")
sc("cta", "That's exchange versus your own wallet. Neither is simply better, they're different jobs, with different trade-offs. Next up, Lesson zero point five: setting up your wallet and backing it up.",
   chapter="Recap and next", button="Next: Lesson 0.5", sub="Setting up your wallet and backing it up")

spec = {"id": "lesson-00-4", "title": "Lesson 0.4: Exchange account vs your own wallet: who holds the keys?", "size": [1920, 1080], "group": "lessons", "maxMinutes": 25, "tag": "Lesson 0.4",
        "gold": True, "seed": 44,
        "use": "Lesson 0.4 page in the Whop course. Gold-standard script: custodial vs self-custody as a full five-row compare, a flow3d anchor for what a wallet actually holds, and an illustrative worked scenario since the source has no worked example of its own.",
        "thumbnail": {"title": "Who holds the keys?", "subtitle": "Lesson 0.4"}, "scenes": S}
out = ROOT / "video-scripts" / "gold" / "lesson-00-4.json"
out.write_text(json.dumps(spec, indent=1, ensure_ascii=False))
words = sum(len(s["vo"].replace("[[pause 4]]", "").split()) for s in S)
print(f"{len(S)} scenes, {words} words, est {(words / 171 * 60 + len(S) * 1.3 + 4 * 3) / 60:.1f} min")
