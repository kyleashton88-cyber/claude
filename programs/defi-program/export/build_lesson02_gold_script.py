#!/usr/bin/env python3
"""Gold-standard script for Lesson 0.2, Opening and securing an exchange account
(about 12-15 minutes). Promotes the old ~4-minute bullet-heavy script to the
gold standard: every multi-part idea (what to look for in an exchange, the six
security steps, Maria's worked example) becomes a walk-through scene instead of
a bullet list read straight through.

Writes video-scripts/gold/lesson-00-2.json (the generator skips lessons with a
gold script). Every illustrative number is labelled as an example on screen and
in the narration. Spoken text (vo) spells numbers for the voice; cap is the
written caption, same sentences."""
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
sc("title", "Lesson zero point two. Opening and securing an exchange account. By the end, you'll open an account on a reputable exchange, and lock it down before a single dollar goes in.",
   "Lesson 0.2. Opening and securing an exchange account. By the end, you'll open an account on a reputable exchange, and lock it down before a single dollar goes in.",
   chapter="Why it matters", eyebrow="Lesson 0.2", num="0.2", title="Opening and securing an exchange account",
   sub="Choose it well, then lock it down, before you deposit a cent.")
sc("statement", "Here's why this lesson comes before you buy anything. The single biggest reason a beginner's first crypto experience goes wrong isn't a bad trade. It's an account that was funded before it was secured: a weak password, no two-factor, a phone number that can be hijacked. Every step in this lesson closes one of those doors, in order, before money is ever at risk.",
   chapter="Why it matters", kicker="Why it matters", lines=["It's rarely a bad trade.", "It's an account secured too late."], sub="This lesson closes every door, in order, before money is ever at risk.")
sc("pillars", "Here's the plan. First, what an exchange actually is, and how to choose one. Second, the six-step lockdown that comes before any money goes in. Third, Maria's worked example, start to finish. And finally, your checklist and a quick quiz.",
   chapter="Why it matters", title="What this lesson covers",
   items=[{"icon": "bank", "title": "Choosing an exchange", "text": "What to look for, and why"}, {"icon": "lock", "title": "The lockdown", "text": "Six steps, before you deposit"},
          {"icon": "users", "title": "Maria's worked example", "text": "Twenty minutes, start to finish"}, {"icon": "check", "title": "Checklist and quiz", "text": "Confirm you've got it"}])
img(D + "exchange-lockdown.png", "Lock it down first",
    "Here's the idea in one picture. An exchange is your on-ramp from ordinary money into crypto. But before you send it a single dollar, you lock the account down. Order matters: account, then security, then money.",
    chapter="Why it matters")

# ---------------------------------------------------------------- choosing an exchange
sc("title", "Choosing an exchange.", chapter="Choosing an exchange", eyebrow="Choosing an exchange", num="1", title="What to look for",
   sub="Licensed, established, and it supports what you need.")
sc("statement", "First, what an exchange even is. It's a company that lets you swap ordinary money, dollars, pounds, euros, for crypto. It's your on-ramp, not your final destination.",
   chapter="Choosing an exchange", kicker="What it is", lines=["Your on-ramp,", "not your final destination."], sub="It swaps ordinary money for crypto. That's the whole job.")
sc("flow", "Here's the sign-up sequence you'll actually go through. You create the account with an email and a password. You verify that email address. You complete K.Y.C., uploading your I.D. and sometimes a proof of address. And once that's approved, the account is ready, but not yet secured. That's the part most beginners rush past, and it's the whole subject of the next chapter.",
   "Here's the sign-up sequence you'll actually go through. You create the account with an email and a password. You verify that email address. You complete KYC, uploading your ID and sometimes a proof of address. And once that's approved, the account is ready, but not yet secured. That's the part most beginners rush past, and it's the whole subject of the next chapter.",
   chapter="Choosing an exchange", title="The sign-up sequence",
   nodes=[{"label": "Create the account", "sub": "Email and a password", "icon": "doc"}, {"label": "Verify your email", "sub": "Click the confirmation link", "icon": "check"},
          {"label": "Complete KYC", "sub": "ID, sometimes proof of address", "icon": "users"}, {"label": "Account ready", "sub": "Not yet secured", "icon": "bank", "tone": "bad"}])
sc("pillars", "Choose one that's licensed or registered where you live, check your country's financial regulator. Large and long-established, with a good security record. And one that supports your bank's deposit method, plus the coins and networks you'll actually use, like E.T.H., U.S.D.C., and low-cost networks such as Arbitrum or Base. Well-known examples include Coinbase, Kraken, Binance, Bybit and O.K.X., but availability differs by country, so pick one that's legally available to you.",
   "Choose one that's licensed or registered where you live, check your country's financial regulator. Large and long-established, with a good security record. And one that supports your bank's deposit method, plus the coins and networks you'll actually use, like ETH, USDC, and low-cost networks such as Arbitrum or Base. Well-known examples include Coinbase, Kraken, Binance, Bybit and OKX, but availability differs by country, so pick one that's legally available to you.",
   chapter="Choosing an exchange", title="Three things to check",
   items=[{"icon": "check", "title": "Licensed where you live", "text": "Check your country's regulator"}, {"icon": "layers", "title": "Large and established", "text": "A good security record"},
          {"icon": "swap", "title": "Supports what you need", "text": "Your bank, plus ETH, USDC, low-cost networks"}])
sc("statement", "You'll also be asked for K.Y.C., know your customer: your ID, and sometimes proof of address. This is normal, and it's legally required for a regulated exchange. Treat a request for it as a good sign, not a red flag.",
   "You'll also be asked for KYC, know your customer: your ID, and sometimes proof of address. This is normal, and it's legally required for a regulated exchange. Treat a request for it as a good sign, not a red flag.",
   chapter="Choosing an exchange", kicker="KYC: know your customer", lines=["ID, sometimes proof of address.", "Normal, and legally required."], sub="A regulated exchange asking for this is a good sign, not a red flag.")
sc("compare", "So flip those three checks around, and you get the red flags. A reputable exchange is licensed, has a long track record, and asks for K.Y.C. A red-flag one is unregistered anywhere you can verify, brand new with no history, and skips identity checks entirely, which sounds convenient but is actually a warning sign, not a shortcut.",
   "So flip those three checks around, and you get the red flags. A reputable exchange is licensed, has a long track record, and asks for KYC. A red-flag one is unregistered anywhere you can verify, brand new with no history, and skips identity checks entirely, which sounds convenient but is actually a warning sign, not a shortcut.",
   chapter="Choosing an exchange", title="Reputable exchange vs. red flag",
   left={"label": "Red flags", "tone": "bad", "items": ["Unregistered, anywhere you can check", "Brand new, no track record", "Skips KYC entirely"]},
   right={"label": "Reputable", "tone": "good", "items": ["Licensed where you live", "Long, established track record", "Asks for KYC"]})
sc("statement", "One caution, though. Choosing a licensed, reputable exchange doesn't mean zero risk. Even large, well-known exchanges have had outages and security incidents. It means a far better starting point, and someone accountable if something goes wrong, not a guarantee that nothing ever will.",
   chapter="Choosing an exchange", kicker="One caution", lines=["\"Reputable\" isn't \"risk-free.\"", "It's a better starting point."], sub="Even large exchanges have had outages and incidents. This isn't a guarantee that nothing ever goes wrong.")
sc("steps", "One habit protects you before any of the lockdown steps even apply: making sure you're actually on the real site. Type the address yourself, or use a bookmark you saved the first time. Check the domain matches, letter for letter, not just something that looks close. Look for the padlock. And never log in by following a link from an email, a text, or a search ad, even if it looks exactly right.",
   chapter="Choosing an exchange", title="Before you type a password",
   steps=["Type the address yourself, or use a saved bookmark", "Check the domain matches, letter for letter", "Look for the padlock", "Never log in via a link from an email, text or ad"],
   result="A fake site can't steal what you never type into it.")

# ---------------------------------------------------------------- the lockdown
sc("title", "The six-step lockdown.", chapter="The lockdown", eyebrow="The lockdown", num="6", title="Before you deposit a cent",
   sub="Do all six. In this order.")
sc("flow", "Here's why the order matters, using the first step as the example. Skip securing your email, and this is the chain that can follow. Someone breaks into your email, often with a password leaked from another site entirely. They click forgot password on your exchange. The reset link lands in the email they now control. And they set a new exchange password, before you even notice. Lock the email first, and this whole chain breaks at step one.",
   chapter="The lockdown", title="Why order matters",
   nodes=[{"label": "Email compromised", "sub": "Often a reused, leaked password", "icon": "alert", "tone": "bad"}, {"label": "\"Forgot password\"", "sub": "On your exchange", "icon": "key", "tone": "bad"},
          {"label": "Reset link", "sub": "Arrives in that same email", "icon": "doc", "tone": "bad"}, {"label": "Exchange taken over", "sub": "Before you notice", "icon": "bank", "tone": "bad"}],
   edges=[{"from": "0", "to": "1", "tone": "bad"}, {"from": "1", "to": "2", "tone": "bad"}, {"from": "2", "to": "3", "tone": "bad"}])
sc("flow", "Here's the first half, the must-do basics. Step one, secure your email first, because whoever controls it can often reset your exchange account too. Step two, a unique, long password for the exchange itself, stored in a password manager. And step three, two-factor authentication with an authenticator app or a hardware security key, not text messages.",
   "Here's the first half, the must-do basics. Step one, secure your email first, because whoever controls it can often reset your exchange account too. Step two, a unique, long password for the exchange itself, stored in a password manager. And step three, two-factor authentication with an authenticator app or a hardware security key, not text messages.",
   chapter="The lockdown", title="The must-do basics",
   nodes=[{"label": "Secure your email first", "sub": "It can reset your exchange too", "icon": "key"}, {"label": "Unique, long password", "sub": "Stored in a password manager", "icon": "lock"},
          {"label": "2FA: app or hardware key", "sub": "Not text messages", "icon": "shield"}])
sc("compare", "Why not text messages? Because a criminal can talk your phone company into moving your number to their SIM card, a SIM swap, and your codes go straight to them. An authenticator app, or a hardware key, never leaves your possession.",
   "Why not text messages? Because a criminal can talk your phone company into moving your number to their SIM card, a SIM swap, and your codes go straight to them. An authenticator app, or a hardware key, never leaves your possession.",
   chapter="The lockdown", title="Text codes vs. an authenticator",
   left={"label": "SMS codes", "tone": "neutral", "items": ["Travel over your phone number", "A SIM swap sends them to a criminal"]},
   right={"label": "App or hardware key", "tone": "good", "items": ["Stays on a device you hold", "Can't be redirected by a phone company"]})
sc("flow", "Here's exactly how a SIM swap works, because the mechanism is what makes it dangerous. The attacker calls your phone company, posing as you, often using personal details found elsewhere. They convince the company to move your number onto a SIM card they control. Your phone loses signal, usually without much warning. And every text message, including your two-factor codes, now arrives on their phone instead of yours.",
   "Here's exactly how a SIM swap works, because the mechanism is what makes it dangerous. The attacker calls your phone company, posing as you, often using personal details found elsewhere. They convince the company to move your number onto a SIM card they control. Your phone loses signal, usually without much warning. And every text message, including your two-factor codes, now arrives on their phone instead of yours.",
   chapter="The lockdown", title="How a SIM swap actually works",
   nodes=[{"label": "Calls your phone company", "sub": "Posing as you", "icon": "alert", "tone": "bad"}, {"label": "Convinces them to move it", "sub": "Onto their own SIM", "icon": "swap", "tone": "bad"},
          {"label": "Your phone loses signal", "sub": "Often with little warning", "icon": "bell", "tone": "bad"}, {"label": "Your codes go to them", "sub": "Every text message, including 2FA", "icon": "key", "tone": "bad"}],
   edges=[{"from": "0", "to": "1", "tone": "bad"}, {"from": "1", "to": "2", "tone": "bad"}, {"from": "2", "to": "3", "tone": "bad"}])
sc("flow3d", "Here's the second half, the extra armour most beginners skip. Step four, save your two-factor backup codes offline, on paper, somewhere safe. Step five, turn on the anti-phishing code if it's offered, a word that appears in every genuine email the exchange sends you. And step six, turn on the withdrawal address allowlist if it's offered, so withdrawals can only ever go to addresses you've pre-approved.",
   "Here's the second half, the extra armour most beginners skip. Step four, save your two-factor backup codes offline, on paper, somewhere safe. Step five, turn on the anti-phishing code if it's offered, a word that appears in every genuine email the exchange sends you. And step six, turn on the withdrawal address allowlist if it's offered, so withdrawals can only ever go to addresses you've pre-approved.",
   chapter="The lockdown", title="The extra armour",
   nodes=[{"label": "Backup codes, offline", "sub": "On paper, somewhere safe", "icon": "doc"}, {"label": "Anti-phishing code", "sub": "A word only real emails carry", "icon": "eye"},
          {"label": "Withdrawal allowlist", "sub": "Only pre-approved addresses", "icon": "wallet"}])
sc("quiz", "Quick check. What does a withdrawal allowlist actually do? [[pause 4]] The answer: it restricts withdrawals so they can only go to addresses you've pre-approved, so even a hijacked account can't send funds somewhere new.",
   chapter="The lockdown", n=1, of=4, q="What does a withdrawal allowlist do?", a="It restricts withdrawals to addresses you've pre-approved in advance, even if the account is later hijacked.")

# ---------------------------------------------------------------- worked example
sc("title", "Maria's worked example.", chapter="Worked example", eyebrow="Worked example", num="20", title="Twenty minutes, start to finish",
   sub="Ten for KYC, ten for security.")
sc("chart", "Here's exactly where Maria's twenty minutes goes. Ten minutes on K.Y.C., signing up and verifying who she is. And ten more on security: a password manager, authenticator-app two-factor on both her email and the exchange, backup codes on paper, and an anti-phishing code. Security isn't the slow part. It's half the job, and it's the half most beginners skip.",
   "Here's exactly where Maria's twenty minutes goes. Ten minutes on KYC, signing up and verifying who she is. And ten more on security: a password manager, authenticator-app two-factor on both her email and the exchange, backup codes on paper, and an anti-phishing code. Security isn't the slow part. It's half the job, and it's the half most beginners skip.",
   chapter="Worked example", kind="donut", title="Maria's setup, twenty minutes", center="20 min", centerSub="example split",
   segs=[{"label": "KYC", "text": "Sign up, verify identity", "value": 10, "show": "10 min", "tone": "blue"},
         {"label": "Security", "text": "Password, 2FA, backup codes, code word", "value": 10, "show": "10 min", "tone": "good"}],
   note="Security is half the job, not an afterthought.")
sc("steps", "Now the whole thing, step by step. Maria signs up, and completes K.Y.C. in about ten minutes. She installs a password manager, and gives the exchange a unique password. She turns on authenticator-app two-factor, on both her email and the exchange. She writes her backup codes on paper, and stores them safely. And she sets an anti-phishing code: the word “blue-kettle.”",
   "Now the whole thing, step by step. Maria signs up, and completes KYC in about ten minutes. She installs a password manager, and gives the exchange a unique password. She turns on authenticator-app two-factor, on both her email and the exchange. She writes her backup codes on paper, and stores them safely. And she sets an anti-phishing code: the word \"blue-kettle.\"",
   chapter="Worked example", title="Maria's setup",
   steps=["Signs up, completes KYC (~10 min)", "Password manager + unique password", "Authenticator 2FA: email and exchange", "Backup codes written down, stored safely",
          "Sets an anti-phishing code: \"blue-kettle\"", "Turns on the withdrawal address allowlist"],
   result="Twenty minutes. All six steps done before a deposit.")
sc("flow", "Here's why that one word works so well. You choose it yourself, when you turn the feature on, and only you and the exchange ever know it. Every genuine email the exchange sends you includes it, somewhere in the text. An attacker writing a fake email has no way to know what word you picked. So a missing code isn't a minor detail. It's the whole tell.",
   chapter="Worked example", title="Why the anti-phishing code works",
   nodes=[{"label": "You choose a word", "sub": "Only you and the exchange know it", "icon": "key"}, {"label": "Every real email includes it", "sub": "Somewhere in the text", "icon": "doc"},
          {"label": "An attacker can't know it", "sub": "They never set it", "icon": "users", "tone": "bad"}, {"label": "Missing word = fake", "sub": "The whole tell", "icon": "alert"}])
sc("statement", "A few weeks later, an email arrives: “suspicious login, verify your account now.” It looks right. Same logo, same layout. But it doesn't say “blue-kettle” anywhere. Maria knows instantly it's fake, and deletes it without clicking a thing.",
   chapter="Worked example", kicker="Later, a test", lines=["No \"blue-kettle\" in the email.", "She knows it's fake."], sub="One missing word, and the whole attack fails.")
sc("statement", "One more thing, if you already opened an exchange account before this lesson. Everything here still applies to it. Go back now, and work through all six lockdown steps on that account, before you do anything else with it.",
   chapter="Worked example", kicker="Already have an account?", lines=["Everything here still applies.", "Go lock it down now."], sub="The six steps work just as well on an account you opened last year.")

# ---------------------------------------------------------------- checklist and quiz
sc("title", "Checklist and quiz.", chapter="Checklist and quiz", eyebrow="Checklist and quiz", num="6", title="Confirm you've got it",
   sub="Six boxes, before you deposit.")
sc("bullets", "Here's this lesson's checklist. Exchange chosen: legally available and reputable where you live. K.Y.C. complete. Email secured with its own strong password and two-factor. Exchange two-factor via an authenticator app or security key, never S.M.S. Backup codes stored offline. And the anti-phishing code and withdrawal allowlist switched on, if your exchange offers them.",
   "Here's this lesson's checklist. Exchange chosen: legally available and reputable where you live. KYC complete. Email secured with its own strong password and two-factor. Exchange two-factor via an authenticator app or security key, never SMS. Backup codes stored offline. And the anti-phishing code and withdrawal allowlist switched on, if your exchange offers them.",
   chapter="Checklist and quiz", title="Before you deposit", numbered=True, compact=True,
   items=["Exchange chosen: legal and reputable where you live", "KYC complete", "Email secured: own password + 2FA", "Exchange 2FA: app or key, never SMS",
          "Backup codes stored offline", "Anti-phishing code + withdrawal allowlist on"])
sc("quiz", "Question two. Why secure your email before the exchange? [[pause 4]] The answer: email is often how accounts get reset. Whoever controls your email can often take over the exchange account too.",
   chapter="Checklist and quiz", n=2, of=4, q="Why secure your email before the exchange?", a="Email is often how accounts get reset. Whoever controls it can often take over the exchange account too.")
sc("quiz", "Question three. Why avoid S.M.S. two-factor? [[pause 4]] The answer: attackers can hijack a phone number with a SIM swap, and receive your codes directly. An authenticator app or hardware key can't be redirected that way.",
   "Question three. Why avoid SMS two-factor? [[pause 4]] The answer: attackers can hijack a phone number with a SIM swap, and receive your codes directly. An authenticator app or hardware key can't be redirected that way.",
   chapter="Checklist and quiz", n=3, of=4, q="Why avoid SMS two-factor?", a="Attackers can hijack a phone number with a SIM swap and receive your codes directly. An app or hardware key can't be redirected that way.")
sc("quiz", "Question four. If a real email from your exchange always includes your anti-phishing code, and one arrives without it, what should you do? [[pause 4]] The answer: treat it as fake. Don't click any link in it, and delete it. The missing code is the tell.",
   chapter="Checklist and quiz", n=4, of=4, q="An email claiming to be from your exchange is missing your anti-phishing code. What should you do?", a="Treat it as fake. Don't click anything in it, and delete it — the missing code is the tell.")

# ---------------------------------------------------------------- recap
sc("flow", "Here's the whole lesson, recapped as one loop. You choose a licensed, established exchange. You verify you're really on its site. You complete K.Y.C. You work through all six lockdown steps. And only then do you deposit. Do those five things, in order, and this lesson is done.",
   "Here's the whole lesson, recapped as one loop. You choose a licensed, established exchange. You verify you're really on its site. You complete KYC. You work through all six lockdown steps. And only then do you deposit. Do those five things, in order, and this lesson is done.",
   chapter="Recap and next", title="This lesson, recapped as one loop", layout="cycle",
   nodes=[{"label": "Choose the exchange", "icon": "bank"}, {"label": "Verify the real site", "icon": "eye"}, {"label": "Complete KYC", "icon": "users"},
          {"label": "All six lockdown steps", "icon": "lock"}, {"label": "Then deposit", "icon": "check"}])
sc("bullets", "Let's recap. Choose an exchange that's licensed, established, and supports what you need. Complete K.Y.C., it's normal. Then lock down all six steps, before you deposit anything. Maria's twenty minutes shows exactly what that looks like in practice.",
   chapter="Recap and next", title="Recap", items=["Choose: licensed, established, supports your needs", "KYC is normal, and required", "Six lockdown steps, before you deposit", "Maria's 20 minutes: 10 KYC, 10 security"])
sc("statement", "This is education, not financial advice. Always verify you're on your exchange's real website before entering any password or code, and nobody from this program will ever ask for your seed phrase, private keys or account access.",
   chapter="Recap and next", kicker="A safety reminder", lines=["Verify the real website.", "We never ask for your keys."], sub="Not financial advice. Always double-check you're on the genuine site.")
sc("cta", "That's opening and securing an exchange account. Choose it well, lock it down, then deposit. Next up, Lesson zero point three: buying your first crypto without overpaying.",
   "That's opening and securing an exchange account. Choose it well, lock it down, then deposit. Next up, Lesson 0.3: buying your first crypto without overpaying.",
   chapter="Recap and next", button="Next: Lesson 0.3", sub="Buying your first crypto without overpaying")

spec = {"id": "lesson-00-2", "title": "Lesson 0.2: Opening and securing an exchange account", "size": [1920, 1080], "group": "lessons", "maxMinutes": 25, "tag": "Lesson 0.2",
        "gold": True, "seed": 42,
        "use": "Lesson 0.2 page in the Whop course. Gold-standard script: choosing and locking down an exchange, taught with a picture, a pillars walk-through, two flows for the six-step lockdown, a compare for SMS-vs-app, a donut and steps for Maria's worked example.",
        "thumbnail": {"title": "Securing an exchange account", "subtitle": "Lesson 0.2"}, "scenes": S}
out = ROOT / "video-scripts" / "gold" / "lesson-00-2.json"
out.write_text(json.dumps(spec, indent=1, ensure_ascii=False))
words = sum(len(s["vo"].replace("[[pause 4]]", "").split()) for s in S)
print(f"{len(S)} scenes, {words} words, est {(words / 171 * 60 + len(S) * 1.3 + 3 * 3) / 60:.1f} min")
