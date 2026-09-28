#!/usr/bin/env python3
"""Gold-standard script for Lesson 0.6, Networks, gas and your first transfer
(about 13-16 minutes). Promotes the old ~4-minute bullet-heavy script to the
gold standard: networks and Layer 2s, the golden rule, the six-step transfer
process, and the lesson's own real fee comparison (Arbitrum cents vs Ethereum
dollars) as a chart3d anchor.

Writes video-scripts/gold/lesson-00-6.json (the generator skips lessons with a
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
EX = "Illustrative fees · check current network conditions"

# ---------------------------------------------------------------- intro
sc("title", "Lesson zero point six. Networks, gas, and your first transfer. By the end, you'll move crypto from the exchange to your own wallet safely, on the right network, starting with a test amount.",
   chapter="Why it matters", eyebrow="Lesson 0.6", num="0.6", title="Networks, gas and your first transfer",
   sub="One setting, one mistake, and funds can be gone for good.")
sc("statement", "Here's why this lesson is stricter than most. A wrong password can be reset. A wrong purchase can be sold back. But a transfer sent on the wrong network has no undo button, no support ticket that fixes it, and often no way to recover it at all. Everything in this lesson exists to make sure that specific mistake never happens to you.",
   chapter="Why it matters", kicker="Why it matters", lines=["Most mistakes have a fix.", "This one usually doesn't."], sub="Everything here exists to make sure it never happens to you.")
sc("pillars", "Here's the plan. First, networks, and why the same coin can live on several of them. Second, the golden rule that prevents the costly mistake. Third, the six-step transfer, done safely. And finally, a real worked example with real numbers, your checklist and a quiz.",
   chapter="Why it matters", title="What this lesson covers",
   items=[{"icon": "layers", "title": "Networks", "text": "The same coin, several chains"}, {"icon": "alert", "title": "The golden rule", "text": "The costly mistake to avoid"},
          {"icon": "check", "title": "The six-step transfer", "text": "Small test first, always"}, {"icon": "coins", "title": "A real worked example", "text": "What it actually costs"}])

# ---------------------------------------------------------------- networks
sc("title", "Networks.", chapter="Networks", eyebrow="Networks", num="4", title="The same coin, several chains",
   sub="Ethereum, and cheaper Layer 2s built around it.")
sc("statement", "Quick context on why several networks exist at all. Ethereum alone can only process so many transactions per second, and when demand outstrips that, fees rise sharply, exactly what Lesson zero point one's gas chart showed. Layer twos exist specifically to relieve that pressure, moving most activity off the busiest network while still settling back to it.",
   "Quick context on why several networks exist at all. Ethereum alone can only process so many transactions per second, and when demand outstrips that, fees rise sharply, exactly what Lesson 0.1's gas chart showed. Layer 2s exist specifically to relieve that pressure, moving most activity off the busiest network while still settling back to it.",
   chapter="Networks", kicker="Why several networks exist", lines=["Ethereum alone has a speed limit.", "Layer 2s relieve that pressure."], sub="Still settling back to Ethereum, just without competing for its busiest, priciest space.")
sc("compare", "The same token, U.S.D.C. for example, can exist on several different blockchains. Ethereum is the main one: the deepest security, the highest fees. Layer 2 networks, like Arbitrum, Base and Optimism, are built around Ethereum, inheriting much of its security, at a fraction of the cost.",
   "The same token, USDC for example, can exist on several different blockchains. Ethereum is the main one: the deepest security, the highest fees. Layer 2 networks, like Arbitrum, Base and Optimism, are built around Ethereum, inheriting much of its security, at a fraction of the cost.",
   chapter="Networks", title="Ethereum vs. Layer 2s",
   left={"label": "Ethereum (mainnet)", "tone": "neutral", "items": ["The deepest security", "The highest fees"]},
   right={"label": "Layer 2s (Arbitrum, Base, Optimism)", "tone": "good", "items": ["Built around Ethereum's security", "A fraction of the cost"]})
sc("statement", "Here's a detail worth knowing early. Your wallet address is usually the same across Ethereum and its Layer 2s, one address, several chains. But your balances are separate on each one. Switch networks inside your wallet to see what's actually there on each.",
   chapter="Networks", kicker="One address, separate balances", lines=["Same address, every network.", "Different balance on each."], sub="Switch networks in your wallet to see what's actually there.")
sc("flow", "And here's roughly why a Layer 2 can be so much cheaper while still being secure. It bundles up many transactions together, off the main Ethereum network, then posts a compact proof of all of them back to Ethereum itself. You still get Ethereum's security backing it up. You just aren't paying for space on the busiest, most expensive network for every single transaction.",
   chapter="Networks", title="Roughly, why a Layer 2 is cheaper",
   nodes=[{"label": "Bundles many transactions", "sub": "Off the main Ethereum network", "icon": "layers"}, {"label": "Posts a proof back to Ethereum", "sub": "A compact summary, not every detail", "icon": "check"},
          {"label": "Ethereum's security still backs it", "sub": "Without paying mainnet prices each time", "icon": "wallet"}])
sc("bullets", "One practical habit: always check which network you're actually on before you act, not after. Most wallets show a network name or logo near the top of the screen. Look at it before every withdrawal, every swap, every transfer, until it becomes automatic.",
   chapter="Networks", title="Check the network, every time", items=["Look at the network name or logo", "Do it before acting, not after", "Make it automatic, on every transaction"])

# ---------------------------------------------------------------- the golden rule
sc("title", "The golden rule.", chapter="The golden rule", eyebrow="The golden rule", num="1", title="The network must match",
   sub="On both ends. Every time.")
sc("statement", "Here it is, in one sentence, because this is the one rule this whole lesson protects. The network you withdraw on must match a network your wallet, or the receiving service, actually supports. Sending on the wrong network can mean the funds are simply lost.",
   chapter="The golden rule", kicker="The golden rule", lines=["The networks must match.", "On both ends, every time."], sub="Sending on the wrong network can mean the funds are simply lost.")
sc("flow", "Here's exactly how that mistake happens. You withdraw from the exchange, and pick a network without really checking it, maybe the default option. Your wallet, or the receiving service, doesn't actually support that network. The transaction still goes through, because the blockchain has no idea what you meant to do. And the funds land somewhere you can't see or reach, often gone for good.",
   chapter="The golden rule", title="How a wrong-network mistake happens",
   nodes=[{"label": "Pick a network without checking", "sub": "Often just the default option", "icon": "swap", "tone": "bad"}, {"label": "Your wallet doesn't support it", "sub": "But the exchange doesn't know that", "icon": "alert", "tone": "bad"},
          {"label": "It sends anyway", "sub": "The blockchain follows instructions exactly", "icon": "coins", "tone": "bad"}, {"label": "Funds land somewhere unreachable", "sub": "Often gone for good", "icon": "lock", "tone": "bad"}],
   edges=[{"from": "0", "to": "1", "tone": "bad"}, {"from": "1", "to": "2", "tone": "bad"}, {"from": "2", "to": "3", "tone": "bad"}])
sc("statement", "Notice there's no villain in that chain, no hacker, no phishing site. Just a dropdown menu, and a moment of not checking it. That's exactly why the fix isn't cleverness. It's a habit, the same small check, done the same way, every single time.",
   chapter="The golden rule", kicker="No villain required", lines=["No hacker. No phishing site.", "Just a dropdown, unchecked."], sub="The fix isn't cleverness. It's the same small check, every single time.")
sc("bullets", "Here are the shapes this mistake actually takes, so you recognise them by name. Withdrawing to an exchange deposit address on the wrong network, when the exchange only credits deposits on specific ones. Sending to a wallet that simply doesn't support the network you picked. And assuming an address looks the same everywhere, so it must work everywhere, which is exactly the assumption that catches people out.",
   chapter="The golden rule", title="The shapes this mistake takes",
   items=["Withdrawing to an exchange on the wrong network", "Sending to a wallet that doesn't support that network", "Assuming \"same address\" means \"works everywhere\""])
sc("quiz", "Quick check. You hold U.S.D.C. on Arbitrum, but zero E.T.H. there. Can you send the U.S.D.C.? [[pause 4]] The answer: no. You need a little E.T.H. on Arbitrum specifically to pay gas there. E.T.H. on Ethereum mainnet doesn't help.",
   "Quick check. You hold USDC on Arbitrum, but zero ETH there. Can you send the USDC? [[pause 4]] The answer: no. You need a little ETH on Arbitrum specifically to pay gas there. ETH on Ethereum mainnet doesn't help.",
   chapter="The golden rule", n=1, of=5, q="You have USDC on Arbitrum but zero ETH there. Can you send it?", a="No. You need a little ETH on Arbitrum specifically to pay gas. ETH on a different network doesn't help.")

# ---------------------------------------------------------------- the transfer
sc("title", "Your first transfer.", chapter="Your first transfer", eyebrow="Your first transfer", num="6", title="Six steps, in order",
   sub="A small test first. Always.")
img(D + "first-transfer.png", "Your first transfer",
    "Here's the whole transfer in one picture, before we walk through it step by step. Copy, choose, check, test, wait, then send the rest.",
    chapter="Your first transfer")
sc("flow", "Steps one and two. In your wallet, copy your address, using the copy button, never typing it by hand. On the exchange, choose withdraw, then the coin, then pick the network: for learning, a low-fee Layer 2 your wallet actually supports, like Arbitrum or Base.",
   chapter="Your first transfer", title="Steps one and two",
   nodes=[{"label": "Copy your address", "sub": "The copy button, never typed by hand", "icon": "wallet"}, {"label": "Withdraw, then pick the network", "sub": "A low-fee Layer 2 your wallet supports", "icon": "swap"}])
sc("steps", "Steps three and four, in full. Paste the address into the withdrawal field, never type it by hand. Check the first six characters match your wallet. Check the last six characters too. Better still, check the whole address, character by character, since a single wrong digit sends it somewhere else entirely. Then choose an amount for a small test first, something like ten dollars of E.T.H., before anything larger moves.",
   "Steps three and four, in full. Paste the address into the withdrawal field, never type it by hand. Check the first 6 characters match your wallet. Check the last 6 characters too. Better still, check the whole address, character by character, since a single wrong digit sends it somewhere else entirely. Then choose an amount for a small test first, something like $10 of ETH, before anything larger moves.",
   chapter="Your first transfer", title="Steps three and four, in full",
   steps=["Paste the address, never type it by hand", "Check the first 6 characters", "Check the last 6 characters (or all of it)", "Choose a small test amount, e.g. $10 of ETH"],
   result="One wrong digit sends it somewhere else entirely.")
sc("flow3d", "Steps five and six. Wait for the test to arrive, and confirm you see it in your wallet, on that exact network. Only then, send the rest. And add the address to the exchange's withdrawal allowlist, so future transfers to your own wallet are pre-approved.",
   chapter="Your first transfer", title="Steps five and six",
   nodes=[{"label": "Wait, confirm it arrived", "sub": "In your wallet, on that network", "icon": "check"}, {"label": "Send the rest", "sub": "Only once the test is confirmed", "icon": "coins"},
          {"label": "Add it to the allowlist", "sub": "Future transfers, pre-approved", "icon": "lock"}])
sc("bullets", "If the test doesn't show up within a few minutes, don't panic and don't send more. Check you're actually looking at the right network in your wallet, since it's easy to be watching the wrong one. Check the transaction on that network's block explorer, using the transaction I.D. from the exchange. And if the network is simply congested, a longer wait is often the whole answer.",
   "If the test doesn't show up within a few minutes, don't panic and don't send more. Check you're actually looking at the right network in your wallet, since it's easy to be watching the wrong one. Check the transaction on that network's block explorer, using the transaction ID from the exchange. And if the network is simply congested, a longer wait is often the whole answer.",
   chapter="Your first transfer", title="If the test doesn't show up",
   items=["Confirm you're viewing the right network", "Check the block explorer with the transaction ID", "A busy network may just need a longer wait"])
sc("statement", "How small should that test actually be? Small enough that losing it entirely wouldn't bother you, the same principle Lesson zero point zero used for a whole learning budget, just applied to one single transfer. Ten dollars is a reasonable starting point for most people; scale it to whatever number actually meets that bar for you.",
   "How small should that test actually be? Small enough that losing it entirely wouldn't bother you, the same principle Lesson 0.0 used for a whole learning budget, just applied to one single transfer. $10 is a reasonable starting point for most people; scale it to whatever number actually meets that bar for you.",
   chapter="Your first transfer", kicker="How small is small enough?", lines=["Small enough to not mind losing it.", "$10 is a reasonable start."], sub="The same principle as Lesson 0.0's learning budget, applied to one transfer.")
sc("quiz", "Quick check. Why send a small test amount before the rest? [[pause 4]] The answer: to confirm the address and the network are actually right, while only a small amount is at risk. If something's wrong, you find out cheaply.",
   chapter="Your first transfer", n=2, of=5, q="Why send a small test amount before the rest?", a="To confirm the address and network are right while only a small amount is at risk.")

# ---------------------------------------------------------------- worked example
sc("title", "A real worked example.", chapter="A real worked example", eyebrow="A real worked example", num="100", title="Withdrawing $100 of ETH",
   sub="To Arbitrum. Then using it.")
sc("stats", "Withdrawing one hundred dollars of E.T.H. to Arbitrum typically costs the exchange somewhere between ten cents and a dollar in withdrawal fees. Small, one-time, and worth it for what it unlocks.",
   "Withdrawing $100 of ETH to Arbitrum typically costs the exchange somewhere between $0.10 and $1 in withdrawal fees. Small, one-time, and worth it for what it unlocks.",
   chapter="A real worked example", stats=[["$0.10–$1", "typical Arbitrum withdrawal fee (example)"]], lastAccent=False)
sc("chart3d", "Here's what that unlocks. A swap on Arbitrum afterwards typically costs a few cents in gas. The same swap on Ethereum mainnet might cost a few dollars, more when the network is busy. That gap, cents against dollars, is exactly why beginners learn on Layer twos.",
   "Here's what that unlocks. A swap on Arbitrum afterwards typically costs a few cents in gas. The same swap on Ethereum mainnet might cost a few dollars, more when the network is busy. That gap, cents against dollars, is exactly why beginners learn on Layer 2s.",
   chapter="A real worked example", kind="bars", title="Cost of a swap: Arbitrum vs. Ethereum mainnet", sub=EX,
   bars=[{"label": "Arbitrum", "text": "A few cents", "value": 0.10, "show": "~$0.05", "tone": "good"},
         {"label": "Ethereum mainnet", "text": "A few dollars, more when busy", "value": 3.50, "show": "~$3.50", "tone": "bad"}])
sc("statement", "That's the whole reason this program starts you on a Layer 2. It's not because Ethereum mainnet is wrong. It's because learning costs real money there. Cents instead of dollars means you can make a mistake, or just try something twice, without it costing anything that matters.",
   chapter="A real worked example", kicker="Why start here", lines=["Not because mainnet is wrong.", "Because learning here is nearly free."], sub="Cents instead of dollars means a mistake, or a second try, costs nothing that matters.")
sc("compare", "That doesn't make Ethereum mainnet something to avoid forever. As your habits solidify and the amounts involved grow, some activity genuinely belongs there, for its deeper liquidity and its longer track record. Learn the habits small and cheap, first. Then decide where to apply them, deliberately, not by accident.",
   chapter="A real worked example", title="Layer 2 for learning, mainnet later",
   left={"label": "Now, while learning", "tone": "good", "items": ["Small amounts", "Cheap to make a mistake"]},
   right={"label": "Later, once habits are solid", "tone": "neutral", "items": ["Some activity genuinely belongs on mainnet", "Deeper liquidity, longer track record"]})

# ---------------------------------------------------------------- checklist and quiz
sc("title", "Checklist and quiz.", chapter="Checklist and quiz", eyebrow="Checklist and quiz", num="5", title="Confirm you've got it",
   sub="Five boxes.")
sc("bullets", "Here's this lesson's checklist. Network chosen on purpose, and supported by your wallet. Address pasted, first and last six characters checked. A test amount sent and received before the rest. A little E.T.H. held on that network for gas. And the address added to the exchange's withdrawal allowlist.",
   "Here's this lesson's checklist. Network chosen on purpose, and supported by your wallet. Address pasted, first and last 6 characters checked. A test amount sent and received before the rest. A little ETH held on that network for gas. And the address added to the exchange's withdrawal allowlist.",
   chapter="Checklist and quiz", title="Before you move on", numbered=True,
   items=["Network chosen on purpose, wallet-supported", "Address checked: first and last 6 characters", "Test amount sent and received before the rest", "A little ETH held on that network, for gas", "Address added to the exchange allowlist"])
sc("quiz", "Question three. What's the golden rule of withdrawals, in one sentence? [[pause 4]] The answer: the network you send on must be one the receiving wallet or service actually supports.",
   chapter="Checklist and quiz", n=3, of=5, q="What's the golden rule of withdrawals?", a="The network you send on must be one the receiving wallet or service actually supports.")
sc("quiz", "Question four. True or false: your wallet address changes when you switch from Ethereum to a Layer 2 like Arbitrum. [[pause 4]] The answer: false. The address usually stays the same. It's the balance on each network that's separate.",
   chapter="Checklist and quiz", n=4, of=5, q="True or false: your wallet address changes when you switch networks.", a="False. The address usually stays the same; it's the balance on each network that's separate.")
sc("quiz", "Question five. Your test transfer hasn't shown up after a few minutes. What's the first thing to check? [[pause 4]] The answer: that you're actually viewing the correct network in your wallet. It's easy to be watching the wrong one and assume the transfer is missing.",
   chapter="Checklist and quiz", n=5, of=5, q="Your test transfer hasn't arrived after a few minutes. What's the first thing to check?", a="That you're viewing the correct network in your wallet. It's easy to be watching the wrong one.")

# ---------------------------------------------------------------- recap
sc("flow", "Here's the whole lesson, recapped as one loop. Copy your address. Choose a network your wallet actually supports. Check the address, first and last characters. Send a small test first. Confirm it arrives. And only then, send the rest, and allowlist the address for next time. Do those six things, and this lesson is done.",
   chapter="Recap and next", title="This lesson, recapped as one loop", layout="cycle",
   nodes=[{"label": "Copy your address", "icon": "wallet"}, {"label": "Choose a supported network", "icon": "swap"}, {"label": "Check the address", "icon": "eye"},
          {"label": "Small test first", "icon": "coins"}, {"label": "Confirm, then send the rest", "icon": "check"}])
sc("statement", "This is education, not financial advice. Take your time on this lesson especially. It's the one with the least room for a casual mistake. And nobody from this program will ever ask for your seed phrase, private keys or account access.",
   chapter="Recap and next", kicker="A reminder", lines=["Take your time here especially.", "We never ask for your keys."], sub="Not financial advice. This lesson has the least room for a casual mistake.")
sc("cta", "That's networks, gas, and your first transfer. Copy, choose, check, test, confirm, then send the rest. Next up, Lesson zero point seven: your first DeFi steps, in practice mode first.",
   chapter="Recap and next", button="Next: Lesson 0.7", sub="Your first DeFi steps (practice mode first)")

spec = {"id": "lesson-00-6", "title": "Lesson 0.6: Networks, gas and your first transfer", "size": [1920, 1080], "group": "lessons", "maxMinutes": 25, "tag": "Lesson 0.6",
        "gold": True, "seed": 46,
        "use": "Lesson 0.6 page in the Whop course. Gold-standard script: networks and Layer 2s, the golden rule, the six-step transfer process, and the lesson's own real fee comparison (Arbitrum cents vs Ethereum mainnet dollars) as a chart3d anchor.",
        "thumbnail": {"title": "Networks, gas, first transfer", "subtitle": "Lesson 0.6"}, "scenes": S}
out = ROOT / "video-scripts" / "gold" / "lesson-00-6.json"
out.write_text(json.dumps(spec, indent=1, ensure_ascii=False))
words = sum(len(s["vo"].replace("[[pause 4]]", "").split()) for s in S)
print(f"{len(S)} scenes, {words} words, est {(words / 171 * 60 + len(S) * 1.3 + 4 * 3) / 60:.1f} min")
