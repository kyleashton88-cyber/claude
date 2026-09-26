#!/usr/bin/env python3
"""Gold-standard script for Lesson 1.8, Privacy and physical security (target
10-20 minutes). Walks address-linking risk, name services, physical
("wrench attack") risk and multisig-as-coercion-defence, and home/device
hygiene as visual walk-throughs (flows, steps, compares), built to the
walk-through-first standard: almost every idea is a flow, steps or callout
image, not a statement read over a static screen.

Writes video-scripts/gold/lesson-01-8.json (the generator skips lessons with
a gold script). Spoken text (vo) spells numbers for the voice; cap is the
written caption, same sentence count as vo."""
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
sc("title", "Lesson one point eight. Privacy and physical security. By the end, you'll know how to keep your holdings private, and your household safe, as what you hold grows.",
   "Lesson 1.8. Privacy and physical security. By the end, you'll know how to keep your holdings private, and your household safe, as what you hold grows.",
   chapter="Intro", eyebrow="Lesson 1.8", num="1.8", title="Privacy and physical security", sub="Keep your holdings private. Keep your household safe.")
sc("pillars", "Here's the plan. Why blockchains being public matters more than people expect. How to actually link less, in practice. The physical risk that only shows up once holdings are large enough to be worth targeting. And the home and device habits that go with all of it.",
   chapter="Intro", title="What this lesson covers",
   items=[{"icon": "eye", "title": "Public by default", "text": "Anyone who links you, sees everything"}, {"icon": "link", "title": "Link less", "text": "Practical separation habits"},
          {"icon": "shield", "title": "Physical risk", "text": "When holdings become a target"}, {"icon": "lock", "title": "Home & devices", "text": "The habits that go with it"}])

# ---------------------------------------------------------------- public by default
sc("title", "Public by default.", chapter="Public by default", eyebrow="Public by default", num="1", title="Every blockchain is a public ledger",
   sub="Forever, not just for now.")
sc("flow", "Here's exactly what happens once one address gets linked to you, step by step. Someone connects your name to an address, maybe from a screenshot, a withdrawal, or a public post. From that moment, its full balance is visible to anyone who looks. So is its complete history: every deposit, every trade, every counterparty, going back to the very first transaction. And that visibility doesn't fade. It's permanent, and it covers every future transaction too, not just the past.",
   chapter="Public by default", title="What happens once an address is linked to you",
   nodes=[{"label": "Someone links your name to it", "sub": "A screenshot, a withdrawal, a post", "icon": "link"}, {"label": "Full balance visible", "sub": "To anyone who looks, from that moment", "icon": "eye"},
          {"label": "Complete history visible", "sub": "Every deposit, trade and counterparty", "icon": "search"}, {"label": "Permanent, and ongoing", "sub": "Covers every future transaction too", "icon": "alert"}])
sc("compare", "So here's the actual contrast worth holding in your head, day to day. A traditional bank balance is private by default; only you and the bank see it. A blockchain address is public by default; only the link between you and that address is ever hidden, and once that link is made, it can't be unmade.",
   chapter="Public by default",
   left={"label": "A bank balance", "tone": "good", "items": ["Private by default", "Only you and the bank see it"]},
   right={"label": "A blockchain address", "tone": "warn", "items": ["Public by default, forever", "Only the link to you is ever hidden — and can't be undone once made"]})
sc("steps", "Worth auditing your own exposure right now, before assuming you're fine. Search your own old posts and forum history for any address you've ever pasted. Check whether any address you use has an E.N.S.-style name pointing at it publicly. And check whether you've ever linked a wallet to a public profile, a Discord, or a leaderboard. Whatever turns up, you now know exactly what's already exposed, and can start a clean, separate address for anything that matters going forward.",
   chapter="Public by default", title="Audit your own exposure, right now",
   steps=["Search your own old posts for any pasted address", "Check for an ENS-style name pointing at your address", "Check for wallets linked to public profiles or leaderboards"], result="Now you know exactly what's already exposed")
sc("steps", "If your own audit just turned up an address you've already exposed, here's the actual fix, not just a worry. Treat that address as burned for privacy purposes, permanently; the link can't be undone. Move meaningful holdings to a fresh, never-shared address, using a method that doesn't itself create a new link. And simply stop using the old one for anything beyond what's already public.",
   chapter="Public by default", title="If you've already exposed one",
   steps=["Treat it as burned for privacy, permanently", "Move meaningful holdings to a fresh, unshared address", "Stop using the old one beyond what's already public"], result="The link can't be undone — but its impact can be contained")
sc("quiz", "Quick check. Once an address is linked to your identity, what can anyone see, and for how long? [[pause 4]] The answer: its full balance and complete history, permanently, including every future transaction from that address.",
   chapter="Public by default", n=1, of=3, q="Once an address is linked to your identity, what can anyone see, and for how long?",
   a="Its full balance and complete history, permanently.")

# ---------------------------------------------------------------- link less
sc("title", "Link less.", chapter="Link less", eyebrow="Link less", num="2", title="Practical habits that actually work",
   sub="Separation you set up once, and keep.")
sc("steps", "Here's what “link less” actually looks like as a habit, in order of impact. Never post an address, a balance, or a win publicly, screenshots included. Use one address for public activity, donations, NFTs, things you don't mind being seen, and a completely separate one for savings. Know that an exchange withdrawal links your verified identity to whichever address receives it, permanently. And think twice before using an ENS-style name service on your savings address specifically.",
   chapter="Link less", title="The link-less habit, in order of impact",
   steps=["Never post an address, balance or win publicly", "Public address for public activity; a separate one for savings", "An exchange withdrawal links your identity to that address", "Think twice before naming your savings address"], result="Separation you set up once, and just keep using")
sc("flow", "Here's exactly why an exchange withdrawal is the one people miss most often. You complete K.Y.C. on an exchange, which verifies your real identity. You withdraw to an address. That withdrawal is now a permanent record connecting your verified identity to that specific address, sitting on the exchange's books and, in principle, discoverable. From that point on, that address is not anonymous to anyone who could ever see that record.",
   chapter="Link less", title="Why an exchange withdrawal links you specifically",
   nodes=[{"label": "You complete KYC", "sub": "Verifies your real identity", "icon": "users"}, {"label": "You withdraw to an address", "sub": "A specific, chosen address", "icon": "wallet"},
          {"label": "Permanent record created", "sub": "Identity ↔ address, on the exchange's books", "icon": "link"}, {"label": "Not anonymous, from then on", "sub": "To anyone who could see that record", "icon": "alert"}])
sc("compare", "And here's exactly why a name service cuts the other way from what people expect. It exists to make an address memorable and easy to find, which is genuinely useful for a public-facing address. On a savings address specifically, that convenience becomes the problem: it makes the one address you most want private the easiest one for anyone to look up and associate with you.",
   chapter="Link less",
   left={"label": "A name on a public address", "tone": "good", "items": ["Convenient, easy to find", "Fine — it was never meant to be private"]},
   right={"label": "A name on your savings address", "tone": "bad", "items": ["Makes it the easiest address to look up", "Exactly the one you wanted private"]})
sc("flow", "Here's how a chain-analysis effort actually builds a full profile, since it's rarely one clue alone. It starts with an exchange withdrawal record, linking your verified identity to one address. From there, address reuse links that address to others you've used the same way. A public post, or an ENS name, adds a public label to the cluster. And the combination, not any single piece, produces a complete profile: identity, full balance, and behaviour, all tied together.",
   chapter="Link less", title="How a full profile actually gets built",
   nodes=[{"label": "Exchange withdrawal record", "sub": "Identity linked to one address", "icon": "link"}, {"label": "Address reuse", "sub": "Links that address to others", "icon": "search"},
          {"label": "A post or ENS name", "sub": "Adds a public label to the cluster", "icon": "globe"}, {"label": "Full profile", "sub": "Identity, balance and behaviour, combined", "icon": "eye"}])
sc("quiz", "Quick check. Why does an exchange withdrawal specifically link your identity to an address? [[pause 4]] The answer: because the exchange verified your identity through KYC, and its records connect that identity to whichever address you withdrew to.",
   chapter="Link less", n=2, of=3, q="Why does an exchange withdrawal specifically link your identity to an address?",
   a="The exchange's KYC records connect your identity to the address you withdrew to.")

# ---------------------------------------------------------------- physical risk
sc("title", "Physical risk.", chapter="Physical risk", eyebrow="Physical risk", num="3", title="When holdings become a target",
   sub="Sometimes called a “wrench attack.”")
sc("statement", "Here's the plain, uncomfortable version of this risk. Criminals have targeted people known, or believed, to hold significant crypto, specifically because a private key can move everything in minutes, with no bank to call and no transaction to reverse. This isn't a hypothetical for this lesson; it's documented, and it's exactly why the earlier habit of never posting your holdings matters as much as any technical safeguard.",
   chapter="Physical risk", kicker="Why this risk is different", lines=["A key can move everything,", "in minutes, with nothing to reverse."], sub="Low profile is the first defence — before any technical safeguard.")
sc("flow", "So here's how multisig actually defeats coercion specifically, step by step, since it's the one structural defence that works even under direct threat. Your funds require, say, two out of three keys to move, not one. Those keys are held in separate physical locations, ideally by separate trusted people. If someone coerces you specifically, you alone cannot produce the second key. And that means there is nothing a threat against you alone can actually unlock.",
   chapter="Physical risk", title="How multisig defeats coercion, specifically",
   nodes=[{"label": "Funds need 2-of-3 keys", "sub": "Not one, to move anything", "icon": "key"}, {"label": "Keys in separate locations", "sub": "Ideally, separate trusted people", "icon": "vault"},
          {"label": "You alone are coerced", "sub": "You cannot produce the second key", "icon": "alert"}, {"label": "Nothing to unlock", "sub": "A threat against you alone achieves nothing", "icon": "shield"}])
sc("compare", "Put a single key and multisig side by side, under exactly this threat, and the difference is total. A single key means one person, coerced once, can move everything, immediately, with no second step required. Two-of-three multisig means one person, even under direct threat, simply cannot move anything alone, no matter how much pressure is applied.",
   chapter="Physical risk",
   left={"label": "A single key", "tone": "bad", "items": ["One person, coerced once", "Can move everything, immediately"]},
   right={"label": "2-of-3 multisig", "tone": "good", "items": ["One person, even under direct threat", "Cannot move anything alone"]})
sc("stats", "One sobering, dated fact behind this chapter. Crypto-crime researchers and journalists have documented dozens of publicised physical robbery and coercion cases targeting known crypto holders across recent years, worldwide, not a handful. This is outside research, not this program's own data, but the pattern is consistent enough that low profile and multisig aren't optional extras for anyone holding a meaningful amount.",
   chapter="Physical risk", stats=[["Dozens+", "publicised physical crypto-coercion cases tracked in recent years (outside research)"]])
sc("compare", "Discretion doesn't mean total secrecy from everyone, so here's the honest line to draw. Worth telling: whoever holds one of your multisig keys, and, for real estate planning, a lawyer bound by confidentiality who knows a plan exists, not necessarily the amount. Not worth telling: casual acquaintances, coworkers, or anyone with no structural role in accessing or recovering it.",
   chapter="Physical risk",
   left={"label": "Worth telling", "tone": "good", "items": ["A multisig key-holder you trust", "A confidentiality-bound advisor, for estate planning"]},
   right={"label": "Not worth telling", "tone": "bad", "items": ["Casual acquaintances or coworkers", "Anyone with no structural role in access or recovery"]})
sc("quiz", "Quick check. Why does 2-of-3 multisig specifically protect against a coercion threat, where a single key doesn't? [[pause 4]] The answer: no single coerced person can produce the second key, so nobody can be forced, alone, to move everything.",
   chapter="Physical risk", n=3, of=3, q="Why does 2-of-3 multisig specifically protect against a coercion threat, where a single key doesn't?",
   a="No single coerced person can produce the second key needed.")

# ---------------------------------------------------------------- home and devices, worked example
sc("title", "Home and devices.", chapter="Home and devices", eyebrow="Home and devices", num="1", title="The habits that go with all of it",
   sub="Worked example: what Alex got wrong.")
sc("steps", "Here's the home and device side, as a straightforward habit list. Hardware wallets and backups stay physically out of sight, never displayed or left visible to visitors. Devices holding any wallet access stay encrypted, with a real passcode, not left unlocked. And holdings simply aren't discussed with people who have no need to know, including, quietly, most extended family and acquaintances.",
   chapter="Home and devices", title="The home and device checklist",
   steps=["Hardware wallets and backups: out of sight, always", "Devices encrypted, with a real passcode", "Holdings not discussed with people who don't need to know"], result="Ordinary discretion, kept up consistently")
sc("steps", "And before that first large deposit specifically, do these three things, in order. Set up a dedicated savings address, separate from anything you've ever used publicly. Leave it unnamed; no ENS, no label anywhere. And if you tell anyone at all that it exists, tell one trusted person, through a secure channel, not a casual conversation where others might overhear.",
   chapter="Home and devices", title="Before your first large deposit",
   steps=["A dedicated savings address, never used publicly", "Leave it unnamed — no ENS, no public label", "If you tell anyone, one trusted person, securely"], result="Set up once, before the balance exists to protect")
img(D + "story-social-leak.png", "What Alex got wrong, and the better version",
    "Alex posts a screenshot of a big win, with the address clearly visible in the corner. From that single post, anyone can now see Alex's full balance, and follow every future move that address makes, forever. A scammer or a thief now has a specific, verified target, not a guess. The better version: no screenshots, ever, a vault address that has never once been shared or posted, and a two-of-three multisig, so no single key holder, Alex included, can be coerced into draining it alone.",
    "Alex posts a screenshot of a big win, with the address clearly visible. From that single post, anyone can now see Alex's full balance, and follow every future move, forever. A scammer or thief now has a specific, verified target, not a guess. The better version: no screenshots ever, a vault address that has never been shared, and a 2-of-3 multisig, so no single key holder can be coerced into draining it alone.",
    chapter="Home and devices")

# ---------------------------------------------------------------- checklist and recap
sc("steps", "Here's your checklist. Do it now, for real. Your savings addresses have never been posted or linked publicly, anywhere. No holdings screenshots or wins go on social media, ever. Vault keys are held so that no single person can move everything alone. And backups are stored discreetly, somewhere nobody would think to look.",
   chapter="Checklist", title="Your checklist",
   steps=["Savings addresses never posted or linked publicly", "No holdings screenshots or wins on social media", "Vault keys held so no single person can move everything", "Backups stored discreetly, out of sight"])
sc("bullets", "Let's recap. Blockchains are public by default, permanently, and only the link to your identity is ever hidden. Linking less is a practical habit: separate addresses, care around exchange withdrawals, caution with name services on savings. Physical risk is real once holdings are worth targeting, and multisig is the structural defence that actually works under coercion. And ordinary discretion, at home and on your devices, is what keeps all of it holding together.",
   chapter="Recap", title="Recap", check=False,
   items=["Blockchains: public by default, permanently — only the link to you is hidden", "Link less: separate addresses, care with withdrawals and naming",
          "Physical risk: multisig is the defence that works under coercion", "Home & devices: ordinary discretion, kept up consistently"])
sc("cta", "Stay quiet about what you hold, separate your addresses by purpose, and structure real holdings so no single person, including you under threat, can move everything alone. Next up, Lesson one point nine: Smart accounts and account abstraction.",
   "Stay quiet about what you hold, separate your addresses by purpose, and structure real holdings so no single person, including you under threat, can move everything alone. Next up, Lesson 1.9: Smart accounts and account abstraction.",
   chapter="Recap", button="Next: Lesson 1.9", sub="Smart accounts and account abstraction")

spec = {"id": "lesson-01-8", "title": "Lesson 1.8: Privacy and physical security", "size": [1920, 1080], "group": "lessons", "maxMinutes": 25,
        "tag": "Lesson 1.8", "gold": True, "music": True, "musicLevel": 0.14, "seed": 50,
        "use": "Lesson 1.8 page in the Whop course. Hand-written gold-standard script: address-linking risk, link-less habits, physical/coercion risk and multisig defence, home/device hygiene, as walk-throughs.",
        "thumbnail": {"title": "Privacy & physical security", "subtitle": "Lesson 1.8"}, "scenes": S}
out = ROOT / "video-scripts" / "gold" / "lesson-01-8.json"
out.write_text(json.dumps(spec, indent=1, ensure_ascii=False))
words = sum(len(s["vo"].replace("[[pause 4]]", "").split()) for s in S)
print(f"{len(S)} scenes, {words} words, est {(words / 171 * 60 + len(S) * 1.3 + 4 * 3) / 60:.1f} min")
