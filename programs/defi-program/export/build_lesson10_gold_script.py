#!/usr/bin/env python3
"""Gold-standard script for Lesson 1.0, the Module 1 Mastery Starter (about 13-15 minutes).
Foundations & Safety: most crypto losses are mistakes and scams, not market moves. Teaches
the module's five words (private key, approval, multisig, phishing, simulation) and the
mastery ladder with animated flows/charts, reusing the module's own lesson diagrams
(approval-anatomy, scam-patterns, simulate-before-sign, privacy-physical, tx-lifecycle)
wherever they already cover the idea.

Writes video-scripts/gold/lesson-01-0.json (the generator skips lessons with a gold script).
Spoken text (vo) spells numbers for the voice; cap is the written caption, same sentences."""
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
EX = "Illustrative categories, not measured data"

# ---------------------------------------------------------------- intro
sc("title", "Lesson one point zero. The Mastery Starter for Module One: Foundations and Safety. By the end, you'll know the five words this module runs on, and exactly how to tell when you've mastered it.",
   "Lesson 1.0. The Mastery Starter for Module 1: Foundations and Safety. By the end, you'll know the five words this module runs on, and exactly how to tell when you've mastered it.",
   chapter="Intro", eyebrow="Lesson 1.0 · Mastery Starter", num="1.0", title="Foundations & Safety", sub="Your map for Module 1, in pictures.")
sc("pillars", "Here's the plan. First, the sixty-second version: why almost every loss in crypto is a mistake, not a market move. Second, the five words you'll need, each one drawn out. Third, what to have ready before you start. Fourth, your first safe step: auditing your approvals. And finally, the mastery ladder, so you know exactly what finishing this module looks like.",
   chapter="Intro", title="What this lesson covers",
   items=[{"icon": "alert", "title": "Why losses happen", "text": "Mistakes and scams, not markets"}, {"icon": "book", "title": "Five words", "text": "Drawn out, not just defined"},
          {"icon": "clock", "title": "Before you start", "text": "What Module 0 should've left you with"}, {"icon": "target", "title": "The ladder", "text": "How you'll know you've mastered it"}])

# ---------------------------------------------------------------- the 60-second version
sc("statement", "Here's the whole module in one sentence. Most crypto losses aren't market losses. They're mistakes and scams: a seed phrase typed into a fake site, an approval signed without reading, a transaction sent on the wrong network. This module builds the habits that prevent them.",
   chapter="The 60-second version", kicker="The 60-second version", lines=["Most losses aren't market losses.", "They're mistakes and scams."], sub="This module builds the habits that prevent them.")
sc("chart", "Here's roughly how beginner losses break down, as categories, not measured statistics. A leaked seed phrase or private key. A signed approval that let someone else move funds. A payment sent on the wrong network or to the wrong address. And outright phishing, a fake site or a fake support agent. Notice what's missing: “the market went down” isn't on this list. That's what this module is built to close.",
   chapter="The 60-second version", kind="donut", title="Where beginner losses usually come from", sub=EX, center="Not the market", centerSub="four preventable doors",
   segs=[{"label": "Leaked keys or seed", "text": "Typed in, photographed, shared", "value": 30, "show": "≈30%", "tone": "bad"},
         {"label": "Bad approvals", "text": "Signed without reading", "value": 25, "show": "≈25%", "tone": "warn"},
         {"label": "Wrong address/network", "text": "Sent to the wrong place", "value": 20, "show": "≈20%", "tone": "warn"},
         {"label": "Phishing", "text": "Fake sites, fake support", "value": 25, "show": "≈25%", "tone": "bad"}])

sc("statement", "This isn't a small problem. Multiple industry trackers have found that wallet-draining phishing scams are now one of the largest single categories of user-level crypto loss, year after year, bigger than exchange hacks. Not because the technology is weak. Because habits are the actual perimeter.",
   chapter="The 60-second version", kicker="Why this module exists", lines=["Wallet-draining scams:", "one of the biggest loss categories."], sub="Habits are the actual perimeter. Not the technology.")

# ---------------------------------------------------------------- words you'll need
sc("title", "Now, the five words you'll need.", chapter="Words you'll need", eyebrow="Words you'll need", num="5", title="Five words, drawn out",
   sub="Private key · Approval · Multisig · Phishing · Simulation")
sc("flow", "Word one: private key. The secret that signs transactions. You met this in Module Zero, but here's the operator version. A burner wallet is a wallet with only a small, disposable amount in it, used to try new apps first. Its private key can sign transactions, same as any wallet. The difference is what's at risk if it's ever compromised: a little, not everything.",
   chapter="Words you'll need", title="A burner wallet's key",
   nodes=[{"label": "Small amount", "sub": "Disposable, for trying new apps", "icon": "wallet"}, {"label": "Private key", "sub": "Signs transactions, same as any wallet", "icon": "key"},
          {"label": "Limited risk", "sub": "If compromised, you lose a little", "icon": "shield"}])
sc("stats", "One real-world number for the burner wallet. Most operators keep somewhere between twenty and a hundred dollars in a burner, enough to actually use a new app, small enough that losing it entirely wouldn't hurt. That's the number to aim for while you're still learning which apps you trust.",
   "One real-world number for the burner wallet. Most operators keep somewhere between $20 and $100 in a burner, enough to actually use a new app, small enough that losing it entirely wouldn't hurt. That's the number to aim for while you're still learning which apps you trust.",
   chapter="Words you'll need", stats=[["$20–$100", "a typical burner wallet balance (illustrative)"]])
img(D + "approval-anatomy.png", "Word two: approval",
    "Word two: approval. Permission for an app to move a token on your behalf. From Lesson one point four: an approval names a spender, a token, and an amount, and it keeps working every time after you sign it once. That's the trap. An approval outlives the trade it was signed for. Revoke the ones you no longer use.",
    chapter="Words you'll need")
sc("compare", "One habit that comes straight from that anatomy. Most apps default to asking for an unlimited approval, permission to move any amount, forever, because it means you won't be asked again next time. A safer habit, where your wallet allows it, is an exact approval: just enough for this one transaction. It costs you one extra click now and then. It also means a compromised app can only ever take what you approved.",
   chapter="Words you'll need",
   title="Unlimited vs exact approval", left={"label": "Unlimited approval", "tone": "bad", "items": ["The app's default, usually", "Never asks again", "A compromise can take everything approved"]},
   right={"label": "Exact approval", "tone": "good", "items": ["One extra click, sometimes", "Just enough for this transaction", "A compromise can only take that amount"]})
sc("flow", "Word three: multisig, short for multi-signature. A wallet that needs several separate keys to agree before it can act. Picture a vault with three locks, held by three different people, and any two of them are enough to open it. One compromised key isn't enough on its own. That's the whole idea: no single point of failure.",
   chapter="Words you'll need", title="A 2-of-3 multisig", layout="cycle",
   nodes=[{"label": "Key 1", "sub": "Held separately", "icon": "key"}, {"label": "Key 2", "sub": "Held separately", "icon": "key"}, {"label": "Key 3", "sub": "Held separately", "icon": "key"}])
sc("statement", "So with a two-of-three multisig, any two keys can move funds, but one stolen key, on its own, can do nothing. That's why serious amounts, later in this program, move into a multisig, not a single wallet.",
   chapter="Words you'll need", kicker="The point of a multisig", lines=["One stolen key,", "on its own, does nothing."], sub="Any 2 of 3 can act. No single point of failure.")
img(D + "scam-patterns.png", "Word four: phishing",
    "Word four: phishing. A fake site or message built to steal. From Lesson one point six: fake look-alike sites, drainers that get one signature to grant everything, fake support messages asking for your seed, and poisoned addresses slipped into your history hoping you'll copy the wrong one. The pattern is always pressure, plus a shortcut around your own checks.",
    chapter="Words you'll need")
img(D + "simulate-before-sign.png", "Word five: simulation",
    "Word five: simulation. A preview of what a transaction will actually change, before you sign it. From Lesson one point seven: a simulator shows you the real result, what leaves your wallet, what arrives, what approvals get granted, so you're never signing blind. If a wallet or tool can show you a simulation, use it, every time.",
    chapter="Words you'll need")
sc("compare", "And here's how to actually catch phishing in the moment. A fake site copies the real one closely, but the web address is slightly wrong, and you usually reached it through a search ad or a message, not a bookmark. A real site's address matches exactly, and you got there through your own bookmark or by typing it yourself. A padlock icon in the browser proves the connection is encrypted. It proves nothing about who's on the other end.",
   chapter="Words you'll need",
   title="Spotting a fake token", left={"label": "Likely fake", "tone": "bad", "items": ["Address is slightly off", "Reached via a search ad or message", "Padlock icon present (proves nothing here)"]},
   right={"label": "Likely real", "tone": "good", "items": ["Address matches exactly", "Reached via your own bookmark", "You typed it yourself, or confirmed it first"]})
sc("quiz", "Quick check. What's the core idea behind a multisig wallet? [[pause 4]] The answer: it needs several separate keys to agree before it can act, so one stolen key, on its own, can't move the funds.",
   chapter="Words you'll need", n=1, of=4, q="What's the core idea behind a multisig wallet?",
   a="It needs several separate keys to agree before it acts. One stolen key, on its own, can't move the funds.")

# ---------------------------------------------------------------- before you start
sc("title", "Before you start.", chapter="Before you start", eyebrow="Before you start", num="2", title="What Module 0 should have left you with",
   sub="Two things, ready before Lesson 1.1")
img(D + "tx-lifecycle.png", "A quick preview",
    "Here's a preview of Lesson one point two, because it matters for everything else in this module. Every transaction you'll ever sign follows this same life cycle: you sign it, the network checks it, it's added to a block, and it reaches finality. Every safety habit in this module, exact approvals, simulation, multisig, is really about controlling what happens at that first step: the sign.",
    chapter="Before you start")
sc("bullets", "Two things, both from Module Zero. First, Module Zero done: a secured exchange account, and a wallet whose restore you've tested. Second, a small amount already sitting in that wallet, on a low-fee network, ready to practise with. If either is missing, go back and finish Module Zero first. This module builds directly on those habits.",
   chapter="Before you start", title="Two things, ready to go", numbered=True,
   items=["Module 0 done: secured exchange, restore-tested wallet", "A small amount in your wallet, on a low-fee network"])

# ---------------------------------------------------------------- your first safe step
sc("title", "Your first safe step.", chapter="Your first safe step", eyebrow="Your first safe step", num="1", title="Audit your approvals",
   sub="Ten minutes, no new risk.")
sc("statement", "Your first step in this module doesn't touch a new app at all. Open your wallet's approvals screen, or a revoke tool, list every approval you've ever granted, and revoke any you don't currently use. It takes about ten minutes, and it closes the exact door word two warned you about.",
   chapter="Your first safe step", kicker="Step one", lines=["List every approval.", "Revoke what you don't use."], sub="About 10 minutes. It closes the door word two warned you about.")
sc("flow", "Here's the worked example. Open your wallet's approvals screen. Read down the list: which app, which token, how much it can move. For each one, ask: am I still using this? If yes, leave it. If no, revoke it, which costs a small network fee but permanently removes that permission. Ten minutes, and every unused door is closed.",
   chapter="Your first safe step", title="Auditing your approvals",
   nodes=[{"label": "Open approvals", "sub": "In your wallet or a revoke tool", "icon": "eye"}, {"label": "Read each one", "sub": "App, token, amount", "icon": "doc"},
          {"label": "Still using it?", "sub": "Decide, one by one", "icon": "search"}, {"label": "Revoke unused", "sub": "Small fee, permanent", "icon": "check"}])
sc("quiz", "Quick check. Why is an old, unused approval worth revoking, even if nothing's gone wrong yet? [[pause 4]] The answer: an approval outlives the trade it was signed for, and keeps working until you revoke it. If that app is ever compromised, an old approval is still a live door.",
   chapter="Your first safe step", n=2, of=4, q="Why is an old, unused approval worth revoking, even if nothing's gone wrong yet?",
   a="It outlives the trade it was signed for and keeps working until revoked. If that app is ever compromised, an old approval is still a live door.")

# ---------------------------------------------------------------- mastery ladder
sc("title", "The mastery ladder.", chapter="The mastery ladder", eyebrow="The mastery ladder", num="3", title="Three rungs",
   sub="Beginner · Practitioner · Master")
sc("chart", "Here's how you'll measure your progress through Module One. Beginner: uses a separate burner wallet, and reads every prompt before signing. Practitioner: runs the before-signing checklist from memory, keeps approvals limited, and uses a hardware wallet. And Master: a multisig vault, a simulation on every signature, private addresses, and a tested recovery plan.",
   chapter="The mastery ladder", kind="bars", title="The mastery ladder",
   bars=[{"label": "Beginner", "text": "Burner wallet, reads every prompt", "value": 1, "show": "Rung 1", "tone": "blue"},
         {"label": "Practitioner", "text": "Checklist from memory, hardware wallet", "value": 2, "show": "Rung 2", "tone": "blue"},
         {"label": "Master", "text": "Multisig, tested recovery", "value": 3, "show": "Rung 3", "tone": "good"}])
sc("bullets", "Here's the road ahead, lesson by lesson. One point one, what DeFi is, and the risk-first mindset. One point two, how a transaction actually happens. One point three, wallets, keys, hardware and multisig. One point four, tokens, approvals and allowances. One point five, stablecoins and how they break. One point six, scam defence. One point seven, reading signatures and simulating transactions. One point eight, privacy and physical security. And one point nine, smart accounts and account abstraction.",
   "Here's the road ahead, lesson by lesson. 1.1, what DeFi is, and the risk-first mindset. 1.2, how a transaction actually happens. 1.3, wallets, keys, hardware and multisig. 1.4, tokens, approvals and allowances. 1.5, stablecoins and how they break. 1.6, scam defence. 1.7, reading signatures and simulating transactions. 1.8, privacy and physical security. And 1.9, smart accounts and account abstraction.",
   chapter="The mastery ladder", title="The road ahead", numbered=True, compact=True,
   items=["1.1 · What DeFi is, and the risk-first mindset", "1.2 · How a transaction actually happens", "1.3 · Wallets, keys, hardware & multisig", "1.4 · Tokens, approvals & allowances",
          "1.5 · Stablecoins and how they break", "1.6 · Scam defence", "1.7 · Reading signatures, simulating transactions", "1.8 · Privacy and physical security", "1.9 · Smart accounts & account abstraction"])
img(D + "privacy-physical.png", "One more preview",
    "One more preview, from Lesson one point eight. Your wallet address isn't your identity, until you connect the two, by posting it publicly next to your name, or letting a delivery address and a crypto balance touch the same paper trail. Privacy and physical security round out this module for exactly that reason: the safest signature in the world doesn't help if someone knows which door to knock on.",
    chapter="You've mastered it when…")
sc("statement", "You've mastered this module when you can take a brand-new app from first visit, to a limited, simulated, verified transaction, and revoke that approval afterward. Not a big balance. A repeatable, careful process.",
   chapter="You've mastered it when…", kicker="The top rung", lines=["First visit to a new app,", "to a verified, revoked transaction."], sub="Not a big balance. A repeatable, careful process.")
sc("quiz", "One more. You get a message from “support,” claiming your wallet has a problem, with a link to fix it. The web address looks almost right, and there's a padlock icon. What should you do? [[pause 4]] The answer: don't click it. Nobody legitimate messages you first, the address is “almost right,” not right, and a padlock only means the connection is encrypted, not that the destination is real.",
   chapter="You've mastered it when…", n=3, of=4, q="A “support” message with an almost-right link and a padlock icon asks you to click. What should you do?",
   a="Don't click it. Nobody legitimate messages you first, “almost right” isn't right, and a padlock only proves encryption, not who's on the other end.")
sc("quiz", "Last check. What does mastering Module One actually look like? [[pause 4]] The answer: taking a new app from first visit to a limited, simulated, verified transaction, and revoking the approval afterward.",
   chapter="You've mastered it when…", n=4, of=4, q="What does mastering Module 1 actually look like?",
   a="Taking a new app from first visit to a limited, simulated, verified transaction, and revoking the approval afterward.")

# ---------------------------------------------------------------- recap
sc("bullets", "Let's recap the five words. Private key: the secret that signs, kept small in a burner wallet while you're learning. Approval: permission that outlives the trade, so revoke what you don't use. Multisig: several keys, no single point of failure. Phishing: pressure plus a shortcut around your checks. And simulation: never sign blind.",
   chapter="Recap", title="Recap", check=False,
   items=["Private key: the secret that signs; keep it small in a burner wallet", "Approval: outlives the trade; revoke what you don't use",
          "Multisig: several keys, no single point of failure", "Phishing: pressure plus a shortcut around your checks", "Simulation: never sign blind"])
sc("cta", "That's the Mastery Starter. You now have the whole module in your head: why losses happen, the five words, your first safe step, and the ladder that tells you when you're done. Next up, Lesson one point one: What DeFi is, and the risk-first mindset.",
   "That's the Mastery Starter. You now have the whole module in your head: why losses happen, the five words, your first safe step, and the ladder that tells you when you're done. Next up, Lesson 1.1: What DeFi is, and the risk-first mindset.",
   chapter="Recap", button="Next: Lesson 1.1", sub="What DeFi is, and the risk-first mindset")

spec = {"id": "lesson-01-0", "title": "Lesson 1.0: Mastery Starter", "size": [1920, 1080], "group": "lessons", "maxMinutes": 25, "tag": "Lesson 1.0",
        "gold": True, "music": True, "musicLevel": 0.14, "seed": 42,
        "use": "Lesson 1.0 page in the Whop course. Hand-written gold-standard script: the Module 1 Mastery Starter, taught with animated flows and charts.",
        "thumbnail": {"title": "Foundations & Safety", "subtitle": "Lesson 1.0 · Mastery Starter"}, "scenes": S}
out = ROOT / "video-scripts" / "gold" / "lesson-01-0.json"
out.write_text(json.dumps(spec, indent=1, ensure_ascii=False))
words = sum(len(s["vo"].replace("[[pause 4]]", "").split()) for s in S)
print(f"{len(S)} scenes, {words} words, est {(words / 171 * 60 + len(S) * 1.3 + 4 * 3) / 60:.1f} min")
