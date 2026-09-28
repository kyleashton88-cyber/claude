#!/usr/bin/env python3
"""Gold-standard script for Lesson 1.4, Tokens, approvals & allowances
(about 12-15 minutes). Replaces the pre-gold-pass-2 script from commit
53ab047, which predates the chart-variant/ticker/chart3d-line visual layer
added in 1e2d691. Builds on the approval basics already covered in Lessons
0.7 and 1.0 with what's genuinely new here: token types as a glossary
ticker, a flow3d anchor on exactly why gasless Permit/Permit2 signatures
are dangerous, a chart3d anchor contrasting transaction-approval gas cost
against signature-approval's zero gas, fake-token verification, and the
source's own worked example reading a real approval prompt.

Writes video-scripts/gold/lesson-01-4.json (the generator skips lessons with
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


# ---------------------------------------------------------------- why it matters
sc("title", "Lesson one point four. Tokens, approvals and allowances. By the end, you'll be able to read an approval request and know exactly what you're allowing.",
   chapter="Why it matters", eyebrow="Lesson 1.4", num="1.4", title="Tokens, approvals & allowances", sub="Know exactly what you're allowing, every time.")
sc("statement", "You've already met approvals twice: the four actions in Lesson zero point seven, and the before-signing checklist in Lesson one point zero. This lesson goes one layer deeper, into what a token actually is, and the specific trick that makes some approvals invisible.",
   "You've already met approvals twice: the four actions in Lesson 0.7, and the before-signing checklist in Lesson 1.0. This lesson goes one layer deeper, into what a token actually is, and the specific trick that makes some approvals invisible.",
   chapter="Why it matters", kicker="Why it matters", lines=["You've met approvals twice already.", "This lesson goes one layer deeper."], sub="What a token is, and the trick that makes some approvals invisible.")
sc("pillars", "Here's the plan. First, what tokens actually are, fungible, non-fungible, and wrapped. Second, the specific danger of gasless signature approvals. Third, how to know a token is the real one. And finally, a real worked example reading an actual approval prompt.",
   chapter="Why it matters", title="What this lesson covers",
   items=[{"icon": "coins", "title": "What tokens actually are", "text": "Fungible, non-fungible, wrapped"}, {"icon": "alert", "title": "The invisible approval", "text": "Why gasless signatures are dangerous"},
          {"icon": "search", "title": "Real, or fake?", "text": "Verified by address, never by name"}, {"icon": "check", "title": "A worked example", "text": "Reading a real approval prompt"}])

# ---------------------------------------------------------------- what tokens are
sc("title", "What tokens actually are.", chapter="What tokens actually are", eyebrow="What tokens actually are", num="5", title="Five kinds of token",
   sub="Same underlying idea. Very different behaviour.")
sc("ticker", "Most tokens on Ethereum-compatible chains are E.R.C.-twenty, fungible, meaning any one is identical to any other, like U.S.D.C. or E.T.H. N.F.Ts, E.R.C.-seven twenty-one or eleven fifty-five, are non-fungible, each one unique, and can represent things like a concentrated liquidity position. Wrapped tokens, like W.E.T.H., represent a claim on something else, held elsewhere. L.P. tokens are a receipt for liquidity you've provided. And lending receipts represent a claim on whatever you deposited into a lending market.",
   "Most tokens on Ethereum-compatible chains are ERC-20, fungible, meaning any one is identical to any other, like USDC or ETH. NFTs, ERC-721 or 1155, are non-fungible, each one unique, and can represent things like a concentrated liquidity position. Wrapped tokens, like WETH, represent a claim on something else, held elsewhere. LP tokens are a receipt for liquidity you've provided. And lending receipts represent a claim on whatever you deposited into a lending market.",
   chapter="What tokens actually are", title="Five kinds of token",
   items=[{"label": "ERC-20", "value": "Fungible: USDC, ETH"}, {"label": "NFT (721/1155)", "value": "Unique, non-fungible"}, {"label": "Wrapped (WETH)", "value": "A claim on something else"},
          {"label": "LP token", "value": "A receipt for liquidity"}, {"label": "Lending receipt", "value": "A claim on your deposit"}])
sc("statement", "Notice what wrapped and receipt tokens have in common: they're all a claim, a piece of paper standing in for something held elsewhere, not the underlying asset itself. That distinction matters constantly from here on, especially once Module two covers liquidity positions in depth.",
   "Notice what wrapped and receipt tokens have in common: they're all a claim, a piece of paper standing in for something held elsewhere, not the underlying asset itself. That distinction matters constantly from here on, especially once Module 2 covers liquidity positions in depth.",
   chapter="What tokens actually are", kicker="A claim, not the asset itself", lines=["Wrapped and receipt tokens are a claim.", "Not the underlying asset itself."], sub="Module 2 covers liquidity positions built from exactly this.")
sc("statement", "Take W.E.T.H. as the clearest example. One W.E.T.H. is designed to always be redeemable for exactly one E.T.H., backed one-to-one inside the wrapping contract. The wrapping exists purely for compatibility, since some older token standards can't handle E.T.H. directly. Convenient, but it's still a separate contract you're now trusting, on top of the one you started with.",
   "Take WETH as the clearest example. One WETH is designed to always be redeemable for exactly one ETH, backed one-to-one inside the wrapping contract. The wrapping exists purely for compatibility, since some older token standards can't handle ETH directly. Convenient, but it's still a separate contract you're now trusting, on top of the one you started with.",
   chapter="What tokens actually are", kicker="WETH, specifically", lines=["Always redeemable for 1 ETH, 1:1.", "Convenient. But it's one more contract to trust."], sub="Wrapping exists purely for compatibility.")

# ---------------------------------------------------------------- the invisible approval
sc("title", "The invisible approval.", chapter="The invisible approval", eyebrow="The invisible approval", num="0", title="Zero gas. Zero friction.",
   sub="The exact trick that makes some approvals easy to miss.")
sc("statement", "Quick recap, since you've seen the basics twice already. To let a protocol move your tokens, you approve a spender for an allowance; the protocol then pulls tokens when you act. Unlimited approvals are convenient, but they let that contract move all of that token, now and at any point in the future.",
   chapter="The invisible approval", kicker="Quick recap", lines=["Approve a spender for an allowance.", "Unlimited: all of that token, forever."], sub="The part covered in Lessons 0.7 and 1.0.")
sc("statement", "Under the hood, this is just two function calls, written into the token's own standard. Approve, which you call, grants the allowance. Transfer-from, which the spender calls later, actually moves the tokens, using exactly the allowance you granted, no more.",
   chapter="The invisible approval", kicker="Under the hood: two function calls", lines=["Approve: you call it, grants the allowance.", "Transfer-from: the spender calls it, moves tokens."], sub="Using exactly the allowance granted. No more.")
sc("flow3d", "Here's what's genuinely new in this lesson: signature approvals, Permit and Permit2. Instead of an on-chain transaction, you sign an off-chain message. That message costs no gas at all. With no gas, and no separate confirmation screen slowing you down, it's remarkably easy to sign without really noticing. And once signed, the allowance it grants is exactly as real as any other.",
   chapter="The invisible approval", title="Why a Permit signature is different",
   nodes=[{"label": "You sign an off-chain message", "sub": "Not an on-chain transaction", "icon": "key"}, {"label": "It costs zero gas", "sub": "No fee, no separate confirmation friction", "icon": "coins"},
          {"label": "Easy to sign without noticing", "sub": "That's precisely what makes it risky", "icon": "alert"}, {"label": "The allowance it grants is just as real", "sub": "Drainers rely on exactly this gap", "icon": "lock"}])
sc("chart3d", "Here's that gap, made concrete. A normal on-chain approval costs real gas, a few dollars, a genuine transaction with its own confirmation screen. A Permit-style signature approval costs nothing at all, no fee, no separate friction to slow you down and make you think. That zero is exactly why drainers prefer this method.",
   chapter="The invisible approval", kind="bars", title="Transaction approval vs. signature approval",
   sub="Illustrative gas cost · a signature costs $0, by design",
   bars=[{"label": "On-chain approval", "text": "A real transaction, real friction", "value": 3, "show": "~$3 gas", "tone": "neutral"}, {"label": "Permit signature", "text": "Off-chain, no fee at all", "value": 0, "show": "$0", "tone": "bad"}])
sc("statement", "The defence is the same habit this whole module has been building. Read every prompt, transaction or signature, with equal care. A wallet that shows 'Signature Request' instead of 'Transaction' isn't asking for less trust. If anything, it deserves more.",
   chapter="The invisible approval", kicker="The defence is the same habit", lines=["Read a signature request as carefully as a transaction.", "Zero gas doesn't mean zero stakes."], sub="If anything, it deserves more attention, not less.")
sc("statement", "Here's a detail worth sitting with. An unlimited approval doesn't expire when you close the tab, or even when you forget about the app entirely. It sits there, live, for months or years, until you either revoke it or the contract uses it. Time doesn't make it safer. It just makes it easier to forget.",
   chapter="The invisible approval", kicker="It doesn't expire on its own", lines=["It sits there, live, for months or years.", "Time doesn't make it safer. It makes it easier to forget."], sub="Until you revoke it, or the contract uses it.")

# ---------------------------------------------------------------- real, or fake
sc("title", "Real, or fake?", chapter="Real, or fake", eyebrow="Real, or fake", num="1", title="One thing identifies a token",
   sub="Never its name. Never its ticker.")
sc("statement", "Here's a fact worth sitting with. Anyone, literally anyone, can create a token and name it 'U.S.D.C.', with the exact same ticker and logo. Only one thing actually identifies a token: its contract address, verified from an authoritative source, never typed from memory and never trusted just because the name matches.",
   "Here's a fact worth sitting with. Anyone, literally anyone, can create a token and name it 'USDC', with the exact same ticker and logo. Only one thing actually identifies a token: its contract address, verified from an authoritative source, never typed from memory and never trusted just because the name matches.",
   chapter="Real, or fake", kicker="Anyone can name a token anything", lines=["A fake can share the real name, ticker, logo.", "Only the contract address actually identifies it."], sub="Verified from an authoritative source. Never by name.")
sc("flow", "Here's how a fake-token scam actually plays out, so you recognise the shape of it. A token appears, using a familiar name, ticker and logo, often airdropped directly into wallets, uninvited. It shows up trading on a real-looking exchange listing, sometimes briefly on a real one. You approve or swap it, checking the name, not the underlying address. And the contract does whatever its creator actually wrote, which might be nothing like what a real token would do.",
   chapter="Real, or fake", title="How a fake-token scam plays out",
   nodes=[{"label": "A token appears, familiar name and logo", "sub": "Often airdropped, uninvited", "icon": "alert", "tone": "bad"}, {"label": "Trades on a real-looking listing", "sub": "Sometimes briefly on a real one too", "icon": "swap", "tone": "bad"},
          {"label": "You approve it, checking the name", "sub": "Not the underlying address", "icon": "eye", "tone": "bad"}, {"label": "The contract does whatever it was written to do", "sub": "Which may be nothing like the real thing", "icon": "coins", "tone": "bad"}],
   edges=[{"from": "0", "to": "1", "tone": "bad"}, {"from": "1", "to": "2", "tone": "bad"}, {"from": "2", "to": "3", "tone": "bad"}])
sc("statement", "Some fake tokens even have a real liquidity pool set up, letting them show an actual price and trade normally, right up until the moment the creator empties that pool entirely. A price chart existing doesn't make a token real; only the verified contract address does.",
   chapter="Real, or fake", kicker="A price chart isn't proof", lines=["A real pool can trade normally, for a while.", "Until the creator empties it entirely."], sub="Only the verified contract address is proof.")
sc("compare", "Here's the practical difference. A real U.S.D.C. approval shows a contract address matching the one published by the issuer, checkable on any block explorer. A fake shows a different address entirely, dressed up with an identical name and symbol, banking on you never checking the one field that actually matters.",
   "Here's the practical difference. A real USDC approval shows a contract address matching the one published by the issuer, checkable on any block explorer. A fake shows a different address entirely, dressed up with an identical name and symbol, banking on you never checking the one field that actually matters.",
   chapter="Real, or fake", title="A real token vs. a fake one",
   left={"label": "The real token", "tone": "good", "items": ["Contract address matches the issuer's", "Checkable on any block explorer"]},
   right={"label": "A fake token", "tone": "bad", "items": ["Identical name, symbol and logo", "A completely different contract address"]})
sc("statement", "N.F.T. approvals work a little differently, worth knowing separately. Instead of an amount, 'set approval for all' grants a spender control over every single N.F.T. you own in that entire collection, all at once, not just one. That's an even bigger blast radius than a typical token allowance, worth double-checking every time it appears.",
   "NFT approvals work a little differently, worth knowing separately. Instead of an amount, 'set approval for all' grants a spender control over every single NFT you own in that entire collection, all at once, not just one. That's an even bigger blast radius than a typical token allowance, worth double-checking every time it appears.",
   chapter="Real, or fake", kicker="NFT approvals: a bigger blast radius", lines=["“Set approval for all”: the whole collection.", "Not one NFT. Every one you own in it."], sub="Worth double-checking every time it appears.")
sc("statement", "Fake tokens and drainer scams both get a full lesson of their own soon, Lesson one point six, scam defence, in real depth. For now, contract-address verification and reading every prompt are enough to catch nearly all of it.",
   "Fake tokens and drainer scams both get a full lesson of their own soon, Lesson 1.6, scam defence, in real depth. For now, contract-address verification and reading every prompt are enough to catch nearly all of it.",
   chapter="Real, or fake", kicker="Coming back to this, properly", lines=["A full lesson soon: 1.6, scam defence.", "For now, address verification catches most of it."], sub="In real depth, coming up.")

# ---------------------------------------------------------------- a worked example
sc("title", "A worked example.", chapter="A worked example", eyebrow="A worked example", num="4", title="Reading a real approval",
   sub="Four checks, before you ever tap confirm.")
sc("steps", "Here's the prompt, word for word. 'Allow zero x three F C nine, dot dot dot, A one B two, to spend your U.S.D.C. Amount: Unlimited.' Four checks, in order. One: is that address actually the protocol's official router? Check the docs or an explorer, never assume. Two: do you actually need unlimited? Edit it down to the exact amount of this one deposit. Three: is this U.S.D.C. actually the real contract? And four: once you're finished with this app, revoke the approval with a tool like revoke dot cash, if you won't be back soon.",
   "Here's the prompt, word for word. 'Allow 0x3fC9…a1B2 to spend your USDC. Amount: Unlimited.' Four checks, in order. One: is that address actually the protocol's official router? Check the docs or an explorer, never assume. Two: do you actually need unlimited? Edit it down to the exact amount of this one deposit. Three: is this USDC actually the real contract? And four: once you're finished with this app, revoke the approval with a tool like revoke.cash, if you won't be back soon.",
   chapter="A worked example", title="Reading: “Allow 0x3fC9…a1B2 to spend USDC. Unlimited.”",
   steps=["Is this address the protocol's official router?", "Do you actually need unlimited? Edit it down.", "Is this USDC the real contract?", "Revoke it later, if you won't be back"],
   result="Four checks. About twenty seconds, once it's a habit.")
sc("statement", "Notice this is the exact same shape as the before-signing checklist from Lesson one point zero. It's just applied specifically to tokens now: confirm the spender, limit the amount, verify what you're actually approving, and clean up afterward.",
   "Notice this is the exact same shape as the before-signing checklist from Lesson 1.0. It's just applied specifically to tokens now: confirm the spender, limit the amount, verify what you're actually approving, and clean up afterward.",
   chapter="A worked example", kicker="The same checklist, applied here", lines=["Confirm the spender. Limit the amount.", "Verify it. Clean up afterward."], sub="Lesson 1.0's checklist, specifically for tokens.")
sc("statement", "This is the third time this program has walked through a revoke habit, after Lesson zero point seven and Lesson one point zero. That repetition is deliberate. It's one of the highest-value five-minute habits in this entire program, and the only one that actually undoes standing risk you've already taken on.",
   "This is the third time this program has walked through a revoke habit, after Lesson 0.7 and Lesson 1.0. That repetition is deliberate. It's one of the highest-value five-minute habits in this entire program, and the only one that actually undoes standing risk you've already taken on.",
   chapter="A worked example", kicker="The third time, deliberately", lines=["The third time this program covers revoking.", "The only habit that undoes risk already taken."], sub="After Lessons 0.7 and 1.0. Deliberately repeated.")

# ---------------------------------------------------------------- checklist and quiz
sc("title", "Checklist and quiz.", chapter="Checklist and quiz", eyebrow="Checklist and quiz", num="4", title="Confirm you've got it",
   sub="Four boxes, three questions.")
sc("statement", "One balancing note before the checklist. Unlimited approvals aren't purely a trap; they exist for real convenience, so you don't need to approve again for every single future interaction with a protocol you use constantly. The judgment call is deciding when that convenience is actually worth the exposure, and when it isn't.",
   chapter="Checklist and quiz", kicker="Not purely a trap", lines=["Unlimited exists for real convenience.", "The judgment call: when it's worth the exposure."], sub="Constant use might justify it. A one-off never does.")
sc("bullets", "Here's this lesson's checklist. The spender is verified against official docs, not assumed. The allowance is limited to what's actually needed. Signature requests are read as carefully as transactions. And approvals are reviewed and revoked on a regular schedule, not left to accumulate.",
   chapter="Checklist and quiz", title="Before you move on", numbered=True,
   items=["Spender verified against official docs", "Allowance limited to what's needed", "Signature requests read as carefully as transactions", "Approvals reviewed and revoked, monthly"])
sc("quiz", "Question one. Why is a gasless 'Permit' signature dangerous? [[pause 4]] The answer: it can grant a token allowance without a transaction, so it's easy to sign without noticing. Drainers use exactly this to take tokens.",
   chapter="Checklist and quiz", n=1, of=5, q="Why is a gasless “Permit” signature dangerous?", a="It can grant an allowance without a transaction, easy to sign without noticing.")
sc("quiz", "Question two. How do you actually know a token is the real one? [[pause 4]] The answer: by its contract address, from an authoritative source, never by its name or its ticker.",
   chapter="Checklist and quiz", n=2, of=5, q="How do you know a token is the real one?", a="By its contract address from an authoritative source, never by name or ticker.")
sc("quiz", "Question three. When should you revoke an approval? [[pause 4]] The answer: when you no longer use that protocol, or on a regular schedule either way.",
   chapter="Checklist and quiz", n=3, of=5, q="When should you revoke an approval?", a="When you no longer use that protocol, or on a regular schedule.")
sc("quiz", "Question four. True or false: an N.F.T. and a fungible token can both represent a DeFi position. [[pause 4]] The answer: true. A concentrated liquidity position, for instance, is commonly represented as an N.F.T., precisely because each one is unique.",
   "Question four. True or false: an NFT and a fungible token can both represent a DeFi position. [[pause 4]] The answer: true. A concentrated liquidity position, for instance, is commonly represented as an NFT, precisely because each one is unique.",
   chapter="Checklist and quiz", n=4, of=5, q="True or false: an NFT can represent a DeFi position.", a="True. A concentrated liquidity position is commonly an NFT.")
sc("quiz", "Question five. A wrapped token and a lending receipt both represent what? [[pause 4]] The answer: a claim on something else, held elsewhere, not the underlying asset itself.",
   chapter="Checklist and quiz", n=5, of=5, q="What do a wrapped token and a lending receipt both represent?", a="A claim on something held elsewhere, not the underlying asset itself.")

# ---------------------------------------------------------------- recap and next
sc("flow", "Here's the whole lesson, recapped as one loop. Know what kind of token you're holding. Verify the spender before approving. Limit the allowance to what you need. Read a signature request exactly as carefully as a transaction. Verify by contract address, never by name. And revoke on a schedule. Do those six things, and an approval can never quietly outlive its reason.",
   chapter="Recap and next", title="This lesson, recapped as one loop", layout="cycle",
   nodes=[{"label": "Know the token type", "icon": "coins"}, {"label": "Verify the spender", "icon": "search"}, {"label": "Limit the allowance", "icon": "lock"},
          {"label": "Read signatures as carefully", "icon": "eye"}, {"label": "Verify by address, not name", "icon": "check"}, {"label": "Revoke on a schedule", "icon": "clock"}])
sc("statement", "This is education, not financial advice, and every dollar figure and contract address in this lesson is illustrative. Nobody from this program will ever ask for your seed phrase, private keys or account access.",
   chapter="Recap and next", kicker="A reminder", lines=["Every figure and address here is illustrative.", "We never ask for your keys."], sub="Not financial advice.")
sc("cta", "That's tokens, approvals and allowances: what tokens actually are, why signature approvals are easy to miss, and how to verify what's real. Next, Lesson one point five: stablecoins and how they break.",
   chapter="Recap and next", button="Next: Lesson 1.5", sub="Stablecoins and how they break")

spec = {"id": "lesson-01-4", "title": "Lesson 1.4: Tokens, approvals & allowances", "size": [1920, 1080], "group": "lessons", "maxMinutes": 25, "tag": "Lesson 1.4",
        "gold": True, "seed": 114,
        "use": "Lesson 1.4 page in the Whop course. Gold-standard script: a 5-token-type glossary ticker, a flow3d anchor on exactly why gasless Permit/Permit2 signatures are dangerous, a chart3d anchor contrasting transaction-approval gas vs signature-approval's $0, a real-vs-fake-token compare, and the source's own worked example reading an approval prompt.",
        "thumbnail": {"title": "Tokens, approvals, allowances", "subtitle": "Lesson 1.4"}, "scenes": S}
out = ROOT / "video-scripts" / "gold" / "lesson-01-4.json"
out.write_text(json.dumps(spec, indent=1, ensure_ascii=False))
words = sum(len(s["vo"].replace("[[pause 4]]", "").split()) for s in S)
print(f"{len(S)} scenes, {words} words, est {(words / 171 * 60 + len(S) * 1.3 + 5 * 3) / 60:.1f} min")
