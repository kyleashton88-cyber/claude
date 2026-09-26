#!/usr/bin/env python3
"""Gold-standard script for Lesson 1.9, Smart accounts and account abstraction
(~14 minutes, expert lesson).

Source: lessons/module-01-foundations-safety.md, "Lesson 1.9 — Smart accounts and
account abstraction". Teaches: EOA vs. smart-account wallets, ERC-4337 (user
operations, bundlers, paymasters), the feature set (social recovery, spending
limits, session keys, batching, passkeys), EIP-7702 (part of the real 2025 Pectra
upgrade), and the new risks a smart account introduces.

Uses flow3d (see .claude/skills/webgl-motion-graphics/SKILL.md) for the ERC-4337
user-operation mechanism - the one genuinely novel mechanism worth visually
anchoring in 3D - and chart3d for the spending-limit tiers. That's this skill's
"at most one or two" ceiling; the social-recovery cycle stays a flat `flow`.

Writes video-scripts/gold/lesson-01-9.json.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
S = []


def sc(type_, vo, cap=None, **k):
    d = {"type": type_, **k, "vo": vo}
    if cap:
        d["cap"] = cap
    S.append(d)


# ---------------------------------------------------------------- intro
sc("title", "Lesson one point nine. Smart accounts and account abstraction. By the end, you'll know how a smart account actually works under the hood, and how to use its features, recovery, limits, passkeys, without opening up new risks.",
   "Lesson 1.9. Smart accounts and account abstraction. By the end, you'll know how a smart account actually works under the hood, and how to use its features, recovery, limits, passkeys, without opening up new risks.",
   chapter="Intro", eyebrow="Lesson 1.9", num="1.9", title="Smart accounts and account abstraction", sub="Your wallet, with programmable rules instead of one single key.")
sc("pillars", "Here's the plan. First, what actually changes when a wallet becomes a smart account, and the standard that makes it possible. Second, the features that standard unlocks, recovery, limits, passkeys. And third, the new risks those same features introduce, so you use them without a blind spot.",
   chapter="Intro", title="What this lesson covers",
   items=[{"icon": "wallet", "title": "What changes", "text": "E.O.A. vs. smart account"},
          {"icon": "cog", "title": "The features", "text": "Recovery, limits, passkeys"},
          {"icon": "shield", "title": "New risks", "text": "What you're now trusting instead"}])
sc("statement", "Every wallet so far in this program has had exactly one rule: whoever holds the private key can move the funds, full stop. A smart account changes that single rule into whatever rules you choose. That's a real upgrade in what's possible, and it's also a real expansion of what you have to understand.",
   chapter="Why it matters", kicker="What actually changes", lines=["One private key, one rule.", "Now: whatever rules you choose."], sub="More possible. Also more to understand.")

# ---------------------------------------------------------------- EOA vs smart account
sc("title", "Two kinds of wallet.", chapter="Two kinds of wallet", eyebrow="Two kinds of wallet", num="1", title="Two kinds of wallet", sub="One key, or programmable rules.")
sc("compare", "So, side by side. An E.O.A., an externally owned account, the wallet type you've used all module, is controlled by exactly one private key: that key signs, or nothing moves. A smart account is a contract wallet instead. Its rules, who can sign, how many signatures, what limits apply, are code you choose, not a fixed default.",
   "So, side by side. An EOA, an externally owned account, the wallet type you've used all module, is controlled by exactly one private key: that key signs, or nothing moves. A smart account is a contract wallet instead. Its rules, who can sign, how many signatures, what limits apply, are code you choose, not a fixed default.",
   chapter="Two kinds of wallet", title="EOA vs. smart account",
   left={"label": "EOA (what you've used so far)", "items": ["Controlled by exactly one private key", "That key signs, or nothing moves", "Rules are fixed, not chosen"]},
   right={"label": "Smart account", "tone": "good", "items": ["A contract wallet with rules you choose", "Multisig, limits, recovery, all optional", "Rules are code, not a fixed default"]})
sc("flow3d", "Here's the standard that makes this work without changing Ethereum itself: E.R.C. four three three seven, account abstraction. You sign an intent, called a user operation, instead of a normal transaction. A bundler, a specialised network participant, collects user operations and submits them on-chain. A paymaster can step in and pay the gas for you, in U.S.D.C., for instance, instead of the network's native token. And the entry point contract validates everything and finally executes your smart account's rules.",
   "Here's the standard that makes this work without changing Ethereum itself: ERC-4337, account abstraction. You sign an intent, called a user operation, instead of a normal transaction. A bundler, a specialised network participant, collects user operations and submits them on-chain. A paymaster can step in and pay the gas for you, in USDC, for instance, instead of the network's native token. And the entry point contract validates everything and finally executes your smart account's rules.",
   chapter="Two kinds of wallet", title="ERC-4337: how a user operation actually moves", seed=19,
   nodes=[{"id": "you", "label": "You sign", "sub": "A user operation, not a raw tx", "icon": "wallet"},
          {"id": "bundler", "label": "Bundler", "sub": "Collects and submits on-chain", "icon": "layers"},
          {"id": "paymaster", "label": "Paymaster", "sub": "Can pay gas for you, e.g. in USDC", "icon": "coins"},
          {"id": "entry", "label": "EntryPoint contract", "sub": "Validates, then executes", "icon": "check"}],
   edges=[{"from": "you", "to": "bundler", "label": "user operation"}, {"from": "bundler", "to": "paymaster", "label": "gas sponsorship"},
          {"from": "paymaster", "to": "entry", "label": "validated"}])
sc("quiz", "Quick check. What does a paymaster actually do? [[pause 4]] The answer: it pays gas on your behalf, which is what lets you pay network fees in a token like U.S.D.C. instead of the chain's native coin.",
   "Quick check. What does a paymaster actually do? [[pause 4]] The answer: it pays gas on your behalf, which is what lets you pay network fees in a token like USDC instead of the chain's native coin.",
   n=1, of=3, q="What does a paymaster do?", a="Pays gas on your behalf, e.g. letting you pay fees in USDC.", chapter="Two kinds of wallet")

# ---------------------------------------------------------------- features
sc("title", "What it unlocks.", chapter="What it unlocks", eyebrow="What it unlocks", num="2", title="What it unlocks", sub="Six features, one contract wallet.")
sc("bullets", "Once your wallet is a contract you control, all of this becomes possible in one account. Multisig, more than one key required. Social recovery, trusted guardians who can restore access. Spending limits, small moves need less. Session keys, a temporary key scoped to one app, which Lesson fourteen point two covers in full. Batching, approve and swap in a single step instead of two. And passkeys, logging in with your device's fingerprint or face instead of typing a seed phrase.",
   chapter="What it unlocks", title="Six features, one account",
   items=["Multisig: more than one key required to sign", "Social recovery: trusted guardians can restore access",
          "Spending limits: small moves need less", "Session keys: temporary, scoped to one app",
          "Batching: approve and swap in a single step", "Passkeys: your device's biometrics, not a typed phrase"])
sc("flow", "Walk through social recovery as it actually plays out. Normally, you just sign with your passkey, day to day. Say you lose your phone. Your guardians, people you chose in advance, can jointly request recovery. That request sits for a cancellable delay, say forty eight hours, before it takes effect. If that request is really you, you do nothing, and access is restored. If it isn't, if someone's trying to steal the account through your guardians, you cancel it in that window, and the attack fails.",
   chapter="What it unlocks", title="Social recovery, step by step",
   nodes=[{"id": "normal", "label": "Normal use", "sub": "Sign day to day with your passkey", "icon": "key"},
          {"id": "lost", "label": "Phone lost", "sub": "Guardians jointly request recovery", "icon": "bell"},
          {"id": "delay", "label": "48-hour delay", "sub": "Cancellable the whole time", "icon": "clock"},
          {"id": "restored", "label": "Access restored", "sub": "If you never cancelled it", "icon": "check"},
          {"id": "attack", "label": "Attacker tries the same path", "sub": "You cancel in the window", "icon": "bot", "tone": "bad"}],
   edges=[{"from": "normal", "to": "lost"}, {"from": "lost", "to": "delay"}, {"from": "delay", "to": "restored"},
          {"from": "delay", "to": "attack", "tone": "bad", "dashed": True}])
sc("quiz", "Quick check. What is social recovery, in one sentence? [[pause 4]] The answer: trusted guardians can restore access to your account, usually after a cancellable delay.",
   n=2, of=3, q="What is social recovery?", a="Trusted guardians can restore access to your account, usually after a delay.", chapter="What it unlocks")
sc("compare", "Two of those six are worth a closer look, because they change what you do day to day, not just what's possible in theory. Batching turns a two-step action, approve a token, then swap it, into one signature instead of two, which also means one less separate approval sitting around afterward. And a passkey is backed by your device's own secure hardware: nothing to type, and nothing a phishing site can trick you into pasting.",
   chapter="What it unlocks", title="Two features worth a closer look",
   left={"label": "Batching", "items": ["Approve, then swap: normally two signatures", "One user operation instead", "One less lingering approval afterward"]},
   right={"label": "Passkeys", "tone": "good", "items": ["Backed by your device's secure hardware", "Nothing to type, nothing to leak", "Can't be pasted into a phishing site by mistake"]})
sc("statement", "Session keys deserve one honest caveat here, and a full lesson later. A session key is a temporary key, scoped to one specific app, so you're not re-approving that app every single time. Scoped correctly, it's convenient. Scoped too broadly, it's a standing approval you forgot you granted. Lesson fourteen point two covers exactly how to scope one safely.",
   "Session keys deserve one honest caveat here, and a full lesson later. A session key is a temporary key, scoped to one specific app, so you're not re-approving that app every single time. Scoped correctly, it's convenient. Scoped too broadly, it's a standing approval you forgot you granted. Lesson 14.2 covers exactly how to scope one safely.",
   chapter="What it unlocks", kicker="One honest caveat", lines=["A session key, scoped correctly,", "is convenient. Scoped too broadly,"], sub="it's a standing approval you forgot you granted. Lesson 14.2 covers the scoping.")
sc("statement", "One more standard worth naming: E.I.P. seventy seven oh two, part of Ethereum's twenty twenty five Pectra upgrade. It lets an ordinary E.O.A. wallet temporarily, or permanently, delegate to smart-account code, gaining these features without ever moving to a new address. It's powerful. It's also exactly the phishing target Lesson one point seven warned you about: a malicious delegation looks, to an untrained eye, like any other signature request.",
   "One more standard worth naming: EIP-7702, part of Ethereum's 2025 Pectra upgrade. It lets an ordinary EOA wallet temporarily, or permanently, delegate to smart-account code, gaining these features without ever moving to a new address. It's powerful. It's also exactly the phishing target Lesson 1.7 warned you about: a malicious delegation looks, to an untrained eye, like any other signature request.",
   chapter="What it unlocks", kicker="EIP-7702", lines=["Your EOA can delegate to", "smart-account code, same address."], sub="Powerful — and the same phishing target Lesson 1.7 already warned you about.")

# ---------------------------------------------------------------- worked example
sc("title", "A worked setup.", chapter="Worked example", eyebrow="Worked example", num="3", title="A worked setup", sub="One operating wallet, three tiers of protection.")
sc("chart3d", "Here's a realistic shape for one operating wallet's limits. With just the passkey, day-to-day moves are capped around two thousand dollars a day. Above that, it requires both the passkey and a hardware key together, two of two, with no daily cap, because a bigger move now needs a second factor to approve it too.",
   "Here's a realistic shape for one operating wallet's limits. With just the passkey, day-to-day moves are capped around $2,000 a day. Above that, it requires both the passkey and a hardware key together, 2-of-2, with no daily cap, because a bigger move now needs a second factor to approve it too.",
   chapter="Worked example", kind="bars", title="One operating wallet's spending tiers", sub="Illustrative example, not a recommended limit", seed=319,
   bars=[{"label": "Passkey only", "text": "Day-to-day moves", "value": 2000, "show": "$2,000/day", "tone": "good"},
         {"label": "Passkey + hardware key", "text": "2-of-2, larger moves", "value": 20000, "show": "No fixed cap", "tone": "warn"}], max=20000)
sc("steps", "Put together, one real setup looks like this. Day to day: a passkey on your phone, capped at two thousand dollars a day. Larger moves: that same passkey, plus a separate hardware key, two of two required. Recovery: three guardians, two of three, with a forty eight hour delay you can always cancel. Lose your phone, guardians recover you. Phone stolen, the thief is capped at two thousand a day, and you have forty eight hours to cancel any recovery attempt you didn't start.",
   chapter="Worked example", title="One operating wallet, assembled",
   steps=["Day to day: passkey only, capped at $2,000/day", "Larger moves: passkey + hardware key, 2-of-2 required",
          "Recovery: 3 guardians, 2-of-3, 48-hour cancellable delay", "Phone stolen: thief capped at $2,000/day; you have 48h to cancel recovery"],
   result="Lose your phone, guardians recover you. Lose control of it, the caps hold the line.")

# ---------------------------------------------------------------- new risks
sc("title", "New risks.", chapter="New risks", eyebrow="New risks", num="4", title="New risks", sub="You're trusting code and people, not just a key anymore.")
sc("bullets", "Every feature above adds something new to verify, not just something new to enjoy. The account's contract code itself can have bugs, same as any smart contract. Module and plugin permissions deserve the same scrutiny as a token approval. Guardians can collude, if you chose them carelessly. And a smart account's address may simply not exist yet on every chain you use.", check=False,
   chapter="New risks", title="What you're now trusting",
   items=["The account's own contract code, like any smart contract, can have bugs", "Module and plugin permissions deserve the same scrutiny as an approval",
          "Guardians can collude, if chosen carelessly", "The address may not be deployed on every chain yet"])
sc("statement", "Guardian collusion is worth sitting with for a second. Three guardians who all live in the same house, or all work for the same company, aren't really three independent checks, they're one, wearing three hats. Choose guardians the same way you'd choose separated multisig key holders: people, or institutions, who genuinely couldn't coordinate even if they wanted to.",
   chapter="New risks", kicker="Guardians aren't automatically independent", lines=["Three guardians in one household", "are one check wearing three hats."], sub="Choose them the same way you'd separate multisig keys.")
sc("quiz", "Last check for this lesson. Why does it matter whether your smart account exists on the destination chain before you send to it? [[pause 4]] The answer: a smart-account address may not be deployed on every chain, so funds sent there can be hard, or impossible, to access.",
   n=3, of=3, q="Why check the smart account exists on the destination chain?", a="Smart-account addresses may not be deployed on every chain; funds sent there may be hard to access.", chapter="New risks")

# ---------------------------------------------------------------- your turn
sc("statement", "Your turn, five to fifteen minutes. List which of your wallets are E.O.A.s and which are already smart accounts. Choose guardians, on paper, so that no two of them could plausibly collude. And if you're moving to a smart account, confirm it's deployed, or deployable, on every chain you actually send to.",
   "Your turn, 5 to 15 minutes. List which of your wallets are EOAs and which are already smart accounts. Choose guardians, on paper, so that no two of them could plausibly collude. And if you're moving to a smart account, confirm it's deployed, or deployable, on every chain you actually send to.",
   chapter="Your turn", kicker="Your turn", lines=["List your wallets: EOA or smart.", "Choose guardians who couldn't collude."], sub="5 to 15 minutes, on paper, before you actually need any of it.")
sc("bullets", "To recap: a smart account turns one fixed rule, one key, into rules you choose, multisig, limits, recovery, passkeys, all through a standard called account abstraction. E.I.P. seventy seven oh two brings those same features to an ordinary wallet address. And every one of those features is also something new to verify, the code, the permissions, the guardians, the chain.",
   "To recap: a smart account turns one fixed rule, one key, into rules you choose, multisig, limits, recovery, passkeys, all through a standard called account abstraction. EIP-7702 brings those same features to an ordinary wallet address. And every one of those features is also something new to verify, the code, the permissions, the guardians, the chain.",
   chapter="Recap", title="Three things to remember",
   items=["A smart account trades one fixed key-rule for rules you choose", "EIP-7702 brings those features to an ordinary wallet address", "Every new feature is also something new to verify"])
sc("cta", "That's smart accounts and account abstraction, and the end of Module One. Next up, Module Two: Trading On-Chain, starting with how swaps, aggregators and routing actually work.",
   chapter="Recap", button="Continue to Module 2", sub="Trading On-Chain")

video = {
    "id": "lesson-01-9",
    "title": "Lesson 1.9: Smart accounts and account abstraction",
    "size": [1920, 1080],
    "group": "lessons",
    "maxMinutes": 25,
    "tag": "Lesson 1.9",
    "gold": True,
    "seed": 19,
    "use": "Lesson 1.9 page in the Whop course. Hand-written gold-standard script: EOA vs. smart account, ERC-4337 (user operations, bundlers, paymasters), social recovery, spending-limit tiers, EIP-7702 (2025 Pectra upgrade), and the new risks each feature introduces. Facts last checked: 2026-09-26.",
    "thumbnail": {"title": "Your wallet, upgraded", "subtitle": "Lesson 1.9"},
    "scenes": S,
}

out = ROOT / "video-scripts" / "gold" / "lesson-01-9.json"
out.write_text(json.dumps(video, indent=None))
print(f"wrote {out} ({len(S)} scenes)")
