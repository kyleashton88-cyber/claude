#!/usr/bin/env python3
"""Gold-standard script for Lesson 1.0, the Module 1 Mastery Starter (about
13-16 minutes). Follows the lesson's own sections (the 60-second version,
words you'll need, the before-signing checklist introduced by this module,
before you start, your first safe step, the mastery ladder, mastered when)
and teaches each with a flow3d recreation of the module's own
simulate-before-sign diagram, a chart3d mastery-ladder anchor, a glossary
ticker, and two of the module's existing illustrative diagrams (anatomy of
an approval, and a real Permit-style phishing popup).

Writes video-scripts/gold/lesson-01-0.json (the generator skips lessons with
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


D = "assets/diagrams/"

# ---------------------------------------------------------------- why it matters
sc("title", "Lesson one point zero. The Mastery Starter for Module One, Foundations and Safety. In the next fifteen minutes, we'll map the whole module: the checklist you'll use from here on, the words you'll need, and exactly how you'll know you've mastered it.",
   "Lesson 1.0. The Mastery Starter for Module 1, Foundations and Safety. In the next 15 minutes, we'll map the whole module: the checklist you'll use from here on, the words you'll need, and exactly how you'll know you've mastered it.",
   chapter="Why it matters", eyebrow="Lesson 1.0 · Mastery Starter", num="1.0", title="Foundations & Safety", sub="Your map for Module 1, before any capital moves.")
sc("image", "This module's outcome, in one line: set up and use a wallet safely, and know what can go irreversibly wrong, before any capital moves.",
   "This module's outcome, in one line: set up and use a wallet safely, and know what can go irreversibly wrong, before any capital moves.",
   src="assets/modules/module-01.png", eyebrow="Module 1 · Foundations & Safety", wide=True, chapter="Why it matters")
sc("statement", "Here's the idea this entire module is built around. Most crypto losses aren't market losses at all. They're mistakes, and scams: a seed phrase typed into a fake site, an approval signed without reading it, a transfer sent on the wrong network. This module builds the specific habits that prevent every one of those.",
   chapter="Why it matters", kicker="Why it matters", lines=["Most losses aren't market losses.", "They're mistakes, and scams."], sub="This module builds the habits that prevent them.")
sc("pillars", "Here's the plan. First, the sixty-second version of the whole module. Second, the five words you'll need. Third, the before-signing checklist, a habit you'll use in every module from here on. And finally, what to have ready, your first safe step, and the mastery ladder.",
   "Here's the plan. First, the 60-second version of the whole module. Second, the five words you'll need. Third, the before-signing checklist, a habit you'll use in every module from here on. And finally, what to have ready, your first safe step, and the mastery ladder.",
   chapter="Why it matters", title="What this lesson covers",
   items=[{"icon": "clock", "title": "The 60-second version", "text": "Mistakes, not markets"}, {"icon": "book", "title": "Five words", "text": "Drawn out, not just defined"},
          {"icon": "check", "title": "The before-signing checklist", "text": "Used in every module after this"}, {"icon": "target", "title": "Ladder & first step", "text": "How you'll measure progress"}])

# ---------------------------------------------------------------- the 60-second version
sc("title", "The 60-second version.", chapter="The 60-second version", eyebrow="The 60-second version", num="60", title="Mistakes, not markets",
   sub="The whole module, in one distinction.")
sc("statement", "Here's the whole module in one sentence. A private key that only you hold, an approval you actually read before granting it, and a network you double-checked, prevent almost every loss that isn't simply the market moving. This module is entirely about building those three habits.",
   chapter="The 60-second version", kicker="The 60-second version", lines=["A key only you hold.", "An approval you actually read."], sub="Plus a checked network. That's almost the whole module.")
sc("compare", "It helps to separate two very different kinds of loss. A market loss is the price moving against you; if your thesis holds, it can recover over time. A mistake loss, a wrong network, an approval signed without reading, is usually final, with no recovery at all. This module is built entirely around preventing the second kind.",
   chapter="The 60-second version", title="Two very different kinds of loss",
   left={"label": "A market loss", "tone": "neutral", "items": ["The price moved against you", "Can recover, if the thesis holds"]},
   right={"label": "A mistake loss", "tone": "bad", "items": ["Wrong network, unread approval", "Usually final. No recovery"]})
sc("statement", "Put a number on it, purely as an illustration. Someone holding one thousand dollars of E.T.H. through a rough month might see it worth eight hundred, painful, but still theirs, still recoverable if the market turns. Someone who signs one unlimited approval on a malicious app can lose the entire one thousand, in a single transaction, with nothing left to recover at all.",
   "Put a number on it, purely as an illustration. Someone holding $1,000 of ETH through a rough month might see it worth $800, painful, but still theirs, still recoverable if the market turns. Someone who signs one unlimited approval on a malicious app can lose the entire $1,000, in a single transaction, with nothing left to recover at all.",
   chapter="The 60-second version", kicker="Illustrative, not a projection", lines=["$1,000 through a rough month: still $800, still yours.", "$1,000 to one bad approval: zero, instantly."], sub="Same starting amount. Completely different kind of loss.")

# ---------------------------------------------------------------- words you'll need
sc("title", "Words you'll need.", chapter="Words you'll need", eyebrow="Words you'll need", num="5", title="Five words for this module",
   sub="You'll meet each one properly, lesson by lesson.")
sc("ticker", "Five words for this module. A private key is the actual secret that signs your transactions. An approval is permission for an app to move one specific token. A multisig is a wallet that needs several separate keys to agree before it acts. Phishing is a fake site or message built specifically to steal from you. And a simulation is a preview of exactly what a transaction will change, before you ever sign it.",
   chapter="Words you'll need", title="Five words for this module",
   items=[{"label": "Private key", "value": "Signs your transactions"}, {"label": "Approval", "value": "Permission for one token"}, {"label": "Multisig", "value": "Needs several keys to act"},
          {"label": "Phishing", "value": "A fake site built to steal"}, {"label": "Simulation", "value": "Previews before you sign"}])
sc("statement", "You'll meet each of these properly, lesson by lesson. Multisig in Lesson one point three. Approvals in Lesson one point four. Phishing in Lesson one point six. And simulation in Lesson one point seven.",
   "You'll meet each of these properly, lesson by lesson. Multisig in Lesson 1.3. Approvals in Lesson 1.4. Phishing in Lesson 1.6. And simulation in Lesson 1.7.",
   chapter="Words you'll need", kicker="Coming up, in order", lines=["Each word gets its own lesson.", "Starting right after this one."], sub="1.3 multisig · 1.4 approvals · 1.6 phishing · 1.7 simulation")

# ---------------------------------------------------------------- the before-signing checklist
sc("title", "The checklist you'll use all module.", chapter="The before-signing checklist", eyebrow="The before-signing checklist", num="7", title="Seven checks, every time",
   sub="Introduced here. Used in every module after this one.")
sc("statement", "This module introduces one checklist you'll actually use for the rest of the entire program: the before-signing checklist. Seven quick checks, run every single time before you approve or sign anything. It takes a few seconds once it's a habit, and it catches almost everything this module warns about.",
   chapter="The before-signing checklist", kicker="One checklist, the whole program", lines=["Seven checks, every time you sign.", "It becomes a habit within days."], sub="It catches almost everything this module warns about.")
sc("steps", "The first four checks. One: chain confirmed, you know exactly which network you're on. Two: the contract address, verified from an authoritative source, never just a link in a message. Three: the token and the amount, double-checked, character by character. And four: the spender, meaning the allowance, reviewed: which app you're granting this permission to, and how much.",
   chapter="The before-signing checklist", title="Checks one through four", numbered=True,
   steps=["Chain confirmed", "Contract address verified from an authoritative source", "Token and amount double-checked", "Spender / allowance reviewed"],
   result="Four checks. About fifteen seconds, once it's a habit.")
sc("image", "Here's the anatomy of any approval, laid out. Which token the app may move. Which contract, the spender, can move it, always worth checking on a block explorer. And the amount: infinite, with no limit until revoked, or exact, covering only this one trade. Exact should be your default.",
   src=D + "approval-anatomy.png", eyebrow="Check four, in detail", wide=True, chapter="The before-signing checklist")
sc("steps", "The last three checks. Five: slippage, set deliberately, not left on whatever default you never looked at. Six: the gas estimate, reviewed, so nothing about the fee surprises you. And seven, the one people skip: state your intended outcome in one plain sentence, before you sign. If you can't state it simply, don't sign it yet.",
   chapter="The before-signing checklist", title="Checks five through seven", numbered=True,
   steps=["Slippage set deliberately", "Gas estimate reviewed", "Intended outcome stated in one sentence"],
   result="If you can't state it simply, don't sign it yet.")
sc("statement", "Notice why it's seven checks, not just one. Each check catches a different failure: the wrong chain, a spoofed address, a typo in the amount, an oversized allowance, careless slippage, a surprise fee, or simply not understanding what you're doing. No single check catches all of them, which is exactly why skipping even one reopens a specific door.",
   chapter="The before-signing checklist", kicker="Why seven, not one", lines=["Each check catches a different failure.", "Skipping even one reopens a specific door."], sub="No single check covers all seven failure modes.")
sc("image", "Here's exactly why checks two and four matter this much, a real pattern worth recognising. A popup claims to be 'verifying your wallet'. Look closer, and it's really a Permit-style signature, granting unlimited U.S.D.C. access to a spender you've never seen, for the next five years. No real verification ever needs a token approval. Reject it, close the tab, and check your existing approvals instead.",
   "Here's exactly why checks two and four matter this much, a real pattern worth recognising. A popup claims to be 'verifying your wallet'. Look closer, and it's really a Permit-style signature, granting unlimited USDC access to a spender you've never seen, for the next five years. No real verification ever needs a token approval. Reject it, close the tab, and check your existing approvals instead.",
   src=D + "story-permit-phishing.png", eyebrow="Why checks two and four exist", wide=True, chapter="The before-signing checklist")
sc("flow3d", "And here's the tool that makes check seven easy: simulation. Your wallet shows a preview of what it says will happen. A simulator runs that exact same call without actually sending it. It decodes exactly what's inside: the function, the token, the amount, the spender. And only if all three agree with what you intended do you sign; otherwise, you reject.",
   chapter="The before-signing checklist", title="Simulate before you sign",
   nodes=[{"label": "Wallet preview", "sub": "What the wallet says will happen", "icon": "eye"}, {"label": "Simulator", "sub": "Runs it, without sending", "icon": "search"},
          {"label": "Decoded calls", "sub": "Function, token, amount, spender", "icon": "code"}, {"label": "Sign, or reject", "sub": "Only if all three agree", "icon": "check"}])

# ---------------------------------------------------------------- before you start
sc("title", "Before you start.", chapter="Before you start", eyebrow="Before you start", num="2", title="Two things, first",
   sub="Both from Module 0.")
sc("bullets", "Before you start this module, two things should already be true. Module zero is done: you have a secured exchange account, and a wallet whose restore you've actually tested, not just set up. And you have a small amount sitting in that wallet already, on a low-fee network, ready to practise with.",
   "Before you start this module, two things should already be true. Module 0 is done: you have a secured exchange account, and a wallet whose restore you've actually tested, not just set up. And you have a small amount sitting in that wallet already, on a low-fee network, ready to practise with.",
   chapter="Before you start", title="Before you start", items=["Module 0 done: secured exchange, restore-tested wallet", "A small amount already in that wallet, on a low-fee network"])
sc("image", "One more mindset worth carrying over from Lesson zero point seven. Pilots train in a simulator before they ever fly a passenger: a test network, a short real hop, checking it did what was expected, then normal use. This module raises the stakes a little, multisig, hardware wallets, real approvals, so that exact discipline matters more here, not less.",
   "One more mindset worth carrying over from Lesson 0.7. Pilots train in a simulator before they ever fly a passenger: a test network, a short real hop, checking it did what was expected, then normal use. This module raises the stakes a little, multisig, hardware wallets, real approvals, so that exact discipline matters more here, not less.",
   src=D + "story-flight-simulator.png", eyebrow="Carried over from Lesson 0.7", wide=True, chapter="Before you start")

# ---------------------------------------------------------------- your first safe step
sc("title", "Your first safe step.", chapter="Your first safe step", eyebrow="Your first safe step", num="1", title="Five minutes, right now",
   sub="Before the rest of this module.")
sc("steps", "Here's your first safe step in this module, and it takes about five minutes. Open your wallet's approvals screen, or a dedicated revocation tool. List every single approval you've ever granted. And revoke any you don't currently use, closing off standing access you probably forgot existed.",
   chapter="Your first safe step", title="Your first safe step",
   steps=["Open your wallet's approvals screen, or a revocation tool", "List every approval you've ever granted", "Revoke any you don't currently use"],
   result="About five minutes. Standing access, closed off.")
sc("statement", "If this feels familiar, it should: it's the exact habit Lesson zero point seven ended on. The difference here is scope. Last time, it was one approval, right after using it. This time, it's everything you've ever granted, in a single pass.",
   "If this feels familiar, it should: it's the exact habit Lesson 0.7 ended on. The difference here is scope. Last time, it was one approval, right after using it. This time, it's everything you've ever granted, in a single pass.",
   chapter="Your first safe step", kicker="A familiar habit, wider scope", lines=["The exact habit Lesson 0.7 ended on.", "This time: everything, in one pass."], sub="Same habit. Wider scope.")

# ---------------------------------------------------------------- the mastery ladder
sc("title", "The mastery ladder.", chapter="The mastery ladder", eyebrow="The mastery ladder", num="3", title="Three rungs",
   sub="Beginner · Practitioner · Master")
sc("chart3d", "Here's how you'll measure your progress through this module. Three rungs. Beginner: a separate burner wallet, and reading every single prompt. Practitioner: running the before-signing checklist from memory, limited approvals as the default, and a hardware wallet in use. And Master: a multisig vault, simulation on every signature, private addresses, and a tested recovery process.",
   chapter="The mastery ladder", kind="bars", title="The mastery ladder",
   bars=[{"label": "Beginner", "text": "Burner wallet, reads every prompt", "value": 1, "show": "Rung 1"},
         {"label": "Practitioner", "text": "Checklist by memory, limited approvals, hardware wallet", "value": 2, "show": "Rung 2"},
         {"label": "Master", "text": "Multisig vault, simulation always, tested recovery", "value": 3, "show": "Rung 3", "tone": "good"}])
sc("statement", "Notice the top rung again asks for habits, not a balance. A multisig vault. Simulation, every time, with no exceptions. And a recovery process you've actually tested, not just assumed would work.",
   chapter="The mastery ladder", kicker="The top rung", lines=["Habits, not a balance.", "Simulation, every time. No exceptions."], sub="And a recovery process you've actually tested.")
sc("bullets", "Here's the first half of the road ahead. One point one, what DeFi is, and the risk-first mindset. One point two, how a transaction actually happens. One point three, wallets, keys, hardware and multisig. One point four, tokens, approvals and allowances. And one point five, stablecoins and how they break.",
   "Here's the first half of the road ahead. 1.1, what DeFi is, and the risk-first mindset. 1.2, how a transaction actually happens. 1.3, wallets, keys, hardware and multisig. 1.4, tokens, approvals and allowances. And 1.5, stablecoins and how they break.",
   chapter="The mastery ladder", title="The road ahead, part one", numbered=True, compact=True,
   items=["1.1 · What DeFi is, and the risk-first mindset", "1.2 · How a transaction actually happens", "1.3 · Wallets, keys, hardware & multisig",
          "1.4 · Tokens, approvals & allowances", "1.5 · Stablecoins and how they break"])
sc("bullets", "And the second half. One point six, scam defence. One point seven, reading signatures and simulating transactions. One point eight, privacy and physical security. And one point nine, smart accounts and account abstraction.",
   "And the second half. 1.6, scam defence. 1.7, reading signatures and simulating transactions. 1.8, privacy and physical security. And 1.9, smart accounts and account abstraction.",
   chapter="The mastery ladder", title="The road ahead, part two", numbered=True, compact=True,
   items=["1.6 · Scam defence", "1.7 · Reading signatures & simulating transactions", "1.8 · Privacy and physical security", "1.9 · Smart accounts & account abstraction"])
sc("flow", "And here's the whole module, recapped as one loop. Confirm the checklist before you ever sign. Limit every approval to what you actually need. Simulate first, whenever the tool is available. Revoke what you're not using, regularly. And as the amount grows, escalate to a multisig. Do those five things, and this module's whole job is done.",
   chapter="The mastery ladder", title="Module 1, recapped as one loop", layout="cycle",
   nodes=[{"label": "Confirm the checklist", "icon": "check"}, {"label": "Limit every approval", "icon": "lock"}, {"label": "Simulate first", "icon": "search"},
          {"label": "Revoke what's unused", "icon": "eye"}, {"label": "Escalate to multisig", "icon": "users"}])

# ---------------------------------------------------------------- checklist and quiz
sc("title", "Checklist and quiz.", chapter="Checklist and quiz", eyebrow="Checklist and quiz", num="5", title="Confirm you've got it",
   sub="Five quick questions.")
sc("quiz", "Question one. What actually signs a transaction, your seed phrase, or your private key? [[pause 4]] The answer: your private key. Your seed phrase is what generates, and can recreate, that private key.",
   chapter="Checklist and quiz", n=1, of=5, q="What actually signs a transaction: your seed phrase, or your private key?", a="Your private key. Your seed phrase is what generates and can recreate it.")
sc("quiz", "Question two. What does a multisig wallet require before it can act? [[pause 4]] The answer: several separate keys, agreeing together, not just one.",
   chapter="Checklist and quiz", n=2, of=5, q="What does a multisig wallet require to act?", a="Several separate keys agreeing together, not just one.")
sc("quiz", "Question three. What does a simulation actually show you? [[pause 4]] The answer: a preview of exactly what a transaction will change, before you ever sign it.",
   chapter="Checklist and quiz", n=3, of=5, q="What does a simulation show you?", a="A preview of exactly what a transaction will change, before you sign it.")
sc("quiz", "Question four. Why is an exact approval safer than an unlimited one? [[pause 4]] The answer: it caps exactly what an app can ever move, no matter what happens to that app later.",
   chapter="Checklist and quiz", n=4, of=5, q="Why is an exact approval safer than an unlimited one?", a="It caps what an app can ever move, no matter what happens to it later.")
sc("quiz", "Question five. What's the first safe step this module asks you to take? [[pause 4]] The answer: open your approvals, and revoke any you no longer use.",
   chapter="Checklist and quiz", n=5, of=5, q="What's the first safe step this module asks you to take?", a="Open your approvals and revoke any you no longer use.")

# ---------------------------------------------------------------- recap and next
sc("statement", "You've mastered this module when you can take a brand-new app from first visit to a limited, simulated, verified transaction. And revoke the approval afterward, without needing to look anything up.",
   chapter="Recap and next", kicker="You've mastered it when…", lines=["First visit to a verified transaction.", "And revoked afterward, without looking anything up."], sub="That's the whole finish line for this module.")
sc("statement", "This is education, not financial advice, and every dollar figure or hypothetical in this module is illustrative. Nobody from this program will ever ask for your seed phrase, private keys or account access.",
   chapter="Recap and next", kicker="A reminder", lines=["Every figure here is illustrative.", "We never ask for your keys."], sub="Not financial advice.")
sc("cta", "That's your Mastery Starter for Module one, Foundations and Safety: the before-signing checklist, five words, your first safe step, and the mastery ladder. Next, Lesson one point one: what DeFi actually is, and the risk-first mindset that runs through everything from here on.",
   chapter="Recap and next", button="Next: Lesson 1.1", sub="What DeFi is, and the risk-first mindset")

spec = {"id": "lesson-01-0", "title": "Lesson 1.0: Mastery Starter (Module 1: Foundations & Safety)", "size": [1920, 1080], "group": "lessons", "maxMinutes": 25, "tag": "Lesson 1.0",
        "gold": True, "seed": 100,
        "use": "Lesson 1.0 page in the Whop course. Module 1's Mastery Starter: the 60-second version, a 5-word glossary ticker, the before-signing checklist (introduced here, used every module after) with a flow3d simulate-before-sign anchor and 2 of the module's own illustrative diagrams, before-you-start, your first safe step, and a chart3d mastery-ladder anchor.",
        "thumbnail": {"title": "Foundations & Safety", "subtitle": "Lesson 1.0 · Mastery Starter"}, "scenes": S}
out = ROOT / "video-scripts" / "gold" / "lesson-01-0.json"
out.write_text(json.dumps(spec, indent=1, ensure_ascii=False))
words = sum(len(s["vo"].replace("[[pause 4]]", "").split()) for s in S)
print(f"{len(S)} scenes, {words} words, est {(words / 171 * 60 + len(S) * 1.3 + 5 * 3) / 60:.1f} min")
