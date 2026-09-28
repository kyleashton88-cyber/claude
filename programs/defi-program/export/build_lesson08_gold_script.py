#!/usr/bin/env python3
"""Gold-standard script for Lesson 0.8, Your security baseline, and the
language of DeFi (about 13-16 minutes). Promotes the old ~6-minute
bullet-heavy script to the gold standard: the module's capstone. All 10
security rules grouped by theme, the full 18-word glossary read aloud via
four ticker scenes, an anatomy-of-a-scam flow3d anchor, an illustrative
"where beginner losses come from" chart3d donut anchor tying the whole
module together, and Jordan's real worked example spotting a DM scam.

Writes video-scripts/gold/lesson-00-8.json (the generator skips lessons with a
gold script). Every illustrative number is labelled as an example on screen
and in the narration. Spoken text (vo) spells numbers and abbreviations for
the voice; cap is the written caption, same sentences."""
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
sc("title", "Lesson zero point eight. Your security baseline, and the language of DeFi. By the end, you'll have ten rules that prevent most losses, and every word you'll need for the rest of this program.",
   chapter="Why it matters", eyebrow="Lesson 0.8", num="0.8", title="Your security baseline, and the language of DeFi",
   sub="The capstone of Module zero. Ten rules, and the words that follow.")
sc("statement", "Every lesson so far taught you one piece: exchanges, your own wallet, networks, your first DeFi steps. This lesson is the piece that ties all of them together, into ten rules you can actually remember, and a shared vocabulary for everything that comes next.",
   chapter="Why it matters", kicker="The capstone of Module zero", lines=["Every lesson taught you one piece.", "This one ties them together."], sub="Ten rules, and the vocabulary for everything that follows.")
sc("pillars", "Here's the plan. First, all ten rules, grouped into three themes you'll actually recall under pressure. Second, the full language of DeFi, eighteen words you'll meet constantly from here on. Third, how a real scam actually unfolds, and where beginner losses typically come from. And finally, a real worked example, your checklist and a quiz.",
   chapter="Why it matters", title="What this lesson covers",
   items=[{"icon": "shield", "title": "The ten rules", "text": "Grouped into three themes"}, {"icon": "book", "title": "The language of DeFi", "text": "Eighteen words, explained"},
          {"icon": "alert", "title": "Spotting it before it happens", "text": "How a scam actually unfolds"}, {"icon": "check", "title": "A real worked example", "text": "Applying the rules under pressure"}])

# ---------------------------------------------------------------- rules 1-4
sc("title", "Don't get scammed.", chapter="Don't get scammed", eyebrow="Don't get scammed", num="1", title="Rules one through four",
   sub="The four rules that stop the most common losses.")
sc("steps", "Rule one: never share your seed phrase. No real person or company will ever ask for it, not support, not this program, nobody. Rule two: bookmark the sites you actually use, and only ever reach them from that bookmark, never from an ad, a D.M. or an email link. Rule three: nobody legitimate D.M.s you first, offering help, an investment, or 'recovery' of lost funds. And rule four: guaranteed returns are a scam, always, with no exceptions.",
   "Rule one: never share your seed phrase. No real person or company will ever ask for it, not support, not this program, nobody. Rule two: bookmark the sites you actually use, and only ever reach them from that bookmark, never from an ad, a DM or an email link. Rule three: nobody legitimate DMs you first, offering help, an investment, or 'recovery' of lost funds. And rule four: guaranteed returns are a scam, always, with no exceptions.",
   chapter="Don't get scammed", title="Rules one through four", numbered=True,
   steps=["Never share your seed phrase", "Bookmark the sites you use; never follow ads, DMs or emails", "Nobody legitimate DMs you first", "Guaranteed returns are a scam, always"],
   result="Four rules. Zero exceptions to any of them.")
sc("statement", "Rule four deserves a moment on its own, because you'll hear it again and again in later modules. Real yield in DeFi moves with markets: it goes up, it goes down, and it's never locked in stone. Anyone promising a fixed, guaranteed number, especially a high one, isn't describing a real product. They're describing a scam.",
   chapter="Don't get scammed", kicker="Why rule four never has exceptions", lines=["Real yield moves with markets.", "A fixed, guaranteed number is not a real product."], sub="You'll see this idea again, properly, much later in the program.")

# ---------------------------------------------------------------- rules 5-7
sc("title", "Transaction habits.", chapter="Transaction habits", eyebrow="Transaction habits", num="2", title="Rules five through seven",
   sub="The habits that catch a mistake before it costs anything.")
sc("steps", "Rule five: read every wallet prompt before approving it, what it does, how much, and to whom, exactly the habit last lesson was built around. Rule six: test first, with a small amount, on anything new, a new app, a new network, a new kind of transaction. And rule seven: use a hardware wallet once the amount you're holding actually matters to you.",
   chapter="Transaction habits", title="Rules five through seven", numbered=True,
   steps=["Read every wallet prompt: what, how much, to whom", "Test first with a small amount on anything new", "Use a hardware wallet once the amount matters"],
   result="These three, together, catch almost every costly mistake.")
sc("statement", "Notice these three aren't new ideas. Rule five is Lesson zero point seven's whole point. Rule six is Lesson zero point six's small test transfer, applied everywhere. And rule seven is coming properly in Lesson one point three. This lesson isn't introducing new habits, it's just naming the ones you've already been building.",
   chapter="Transaction habits", kicker="Nothing new here, just named", lines=["You've already been building these.", "This lesson just gives them names."], sub="Lessons 0.6 and 0.7, generalised into permanent habits.")

# ---------------------------------------------------------------- rules 8-10
sc("title", "Everyday hygiene.", chapter="Everyday hygiene", eyebrow="Everyday hygiene", num="3", title="Rules eight through ten",
   sub="The quiet habits that hold up over years, not just one transaction.")
sc("steps", "Rule eight: keep your devices updated, and use a separate browser profile just for crypto, away from your everyday browsing. Rule nine: keep records of every buy, sell, transfer and fee, you'll thank yourself later, including at tax time. And rule ten, the one that catches almost everything else: if something feels urgent, stop. Scammers manufacture urgency on purpose. Real opportunities can always wait for you to check.",
   chapter="Everyday hygiene", title="Rules eight through ten", numbered=True,
   steps=["Keep devices updated; use a separate browser profile", "Keep records of every buy, sell, transfer and fee", "If something feels urgent, stop"],
   result="Rule ten alone catches almost every scam that reaches you.")
sc("statement", "If you remember only one rule under real pressure, make it rule ten. A wallet can't be 'suspended'. A giveaway doesn't expire in the next ten minutes. Urgency is not a feature of a real opportunity, it's a manufactured pressure tactic, and recognising it is usually enough on its own.",
   chapter="Everyday hygiene", kicker="If you remember only one", lines=["A wallet can't be “suspended”.", "Urgency is manufactured, on purpose."], sub="Recognising urgency is usually enough, by itself.")
sc("statement", "Rule nine deserves a moment too, because it doesn't pay off immediately. Good records mean you can reconcile a discrepancy in minutes, not days. They're the first thing a legitimate support process actually asks for. And in most places, they're exactly what's needed at tax time anyway, covered properly in Lesson twelve point seven. Build the habit before you have hundreds of transactions to reconstruct from memory.",
   "Rule nine deserves a moment too, because it doesn't pay off immediately. Good records mean you can reconcile a discrepancy in minutes, not days. They're the first thing a legitimate support process actually asks for. And in most places, they're exactly what's needed at tax time anyway, covered properly in Lesson 12.7. Build the habit before you have hundreds of transactions to reconstruct from memory.",
   chapter="Everyday hygiene", kicker="Why rule nine pays off later", lines=["It doesn't pay off immediately.", "Build it before you have hundreds to reconstruct."], sub="Lesson 12.7 covers tax and record-keeping properly.")

# ---------------------------------------------------------------- glossary
sc("title", "The language of DeFi.", chapter="The language of DeFi", eyebrow="The language of DeFi", num="18", title="Eighteen words, explained",
   sub="Words you'll meet constantly, starting next module.")
sc("ticker", "Four words about who holds what. Your address is your public account number on a blockchain. Your seed phrase is twelve to twenty-four words that recreate your wallet's keys, never shared with anyone, ever. Your private key is the actual secret that signs transactions; your seed phrase is what generates it. And custody just means who holds those keys: an exchange, that's custodial, or you, that's self-custody.",
   chapter="The language of DeFi", title="Who holds what",
   items=[{"label": "Address", "value": "Your account number"}, {"label": "Seed phrase", "value": "12–24 words, never shared"},
          {"label": "Private key", "value": "Signs your transactions"}, {"label": "Custody", "value": "An exchange, or you"}])
sc("ticker", "Five words about the network you're on. Gas is the fee a network charges for a transaction, paid in that network's own token. A network, or chain, is simply which blockchain you're using right now: Ethereum, Arbitrum, Base, and so on. A Layer two is a cheaper, faster network built on top of Ethereum. A token is a unit of value living on a blockchain, U.S.D.C. for example. And a stablecoin is a token deliberately designed to hold a steady value, usually one dollar.",
   "Five words about the network you're on. Gas is the fee a network charges for a transaction, paid in that network's own token. A network, or chain, is simply which blockchain you're using right now: Ethereum, Arbitrum, Base, and so on. A Layer 2 is a cheaper, faster network built on top of Ethereum. A token is a unit of value living on a blockchain, USDC for example. And a stablecoin is a token deliberately designed to hold a steady value, usually one dollar.",
   chapter="The language of DeFi", title="The network you're on",
   items=[{"label": "Gas", "value": "The network's fee"}, {"label": "Network / chain", "value": "Which blockchain you're on"},
          {"label": "Layer 2", "value": "Cheaper, built on Ethereum"}, {"label": "Token", "value": "A unit of value"}, {"label": "Stablecoin", "value": "Steady value, usually $1"}])
sc("ticker", "Four words about DeFi itself. A smart contract is a program on a blockchain that follows fixed rules, there's no negotiating with it. A D.E.X., a decentralised exchange, lets you swap tokens directly from your own wallet. An approval is permission for an app to move a specific token, the whole subject of last lesson. And a block explorer is a website that shows every transaction that's ever happened, in public.",
   "Four words about DeFi itself. A smart contract is a program on a blockchain that follows fixed rules, there's no negotiating with it. A DEX, a decentralised exchange, lets you swap tokens directly from your own wallet. An approval is permission for an app to move a specific token, the whole subject of last lesson. And a block explorer is a website that shows every transaction that's ever happened, in public.",
   chapter="The language of DeFi", title="DeFi mechanics",
   items=[{"label": "Smart contract", "value": "Code with fixed rules"}, {"label": "DEX", "value": "Swap from your wallet"},
          {"label": "Approval", "value": "Permission for one token"}, {"label": "Block explorer", "value": "Every transaction, visible"}])
sc("ticker", "And five more, about numbers and access. A testnet is a practice blockchain; a faucet is the site that hands you free test coins for it. A.P.Y. is annual percentage yield, your yearly return, including compounding. Liquidity is how easily something can be bought or sold without moving its price. K.Y.C. is the identity checks regulated exchanges require. And two-factor authentication, two-F.A., is a second proof of identity at login, beyond just your password.",
   "And five more, about numbers and access. A testnet is a practice blockchain; a faucet is the site that hands you free test coins for it. APY is annual percentage yield, your yearly return, including compounding. Liquidity is how easily something can be bought or sold without moving its price. KYC is the identity checks regulated exchanges require. And two-factor authentication, 2FA, is a second proof of identity at login, beyond just your password.",
   chapter="The language of DeFi", title="Numbers and access",
   items=[{"label": "Testnet / faucet", "value": "Free practice coins"}, {"label": "APY", "value": "Yearly return, compounded"}, {"label": "Liquidity", "value": "How easily it trades"},
          {"label": "KYC", "value": "ID checks, at exchanges"}, {"label": "2FA", "value": "A second login proof"}])
sc("statement", "That's all eighteen. You won't memorise them from one pass, and you don't need to. You'll meet every single one of these words again, in context, starting with the very next module.",
   chapter="The language of DeFi", kicker="You'll meet these again", lines=["You won't memorise them in one pass.", "You'll meet every one again, in context."], sub="Starting with the very next module.")

# ---------------------------------------------------------------- spotting it
sc("title", "Spotting it before it happens.", chapter="Spotting it before it happens", eyebrow="Spotting it before it happens", num="4", title="How a real scam unfolds",
   sub="The same shape, almost every time.")
sc("flow3d", "Here's the anatomy of a typical D.M. scam, almost always the same shape. It opens with a message claiming to be support, or a giveaway, or someone offering help. It adds urgency: act in the next ten minutes, or your wallet is 'suspended'. It dangles a fake guaranteed return, or free money, to override your caution, no real product works that way. And it ends with a request, dressed up as 'verification': your seed phrase, or an unlimited approval. Every single step in that chain breaks one of the rules you just learned.",
   chapter="Spotting it before it happens", title="Anatomy of a DM scam",
   nodes=[{"label": "“Support” or a giveaway messages you first", "sub": "Breaks rule three", "icon": "bell", "tone": "bad"},
          {"label": "Urgency: act now, or else", "sub": "Breaks rule ten", "icon": "alert", "tone": "bad"},
          {"label": "A fake guaranteed return, dangled", "sub": "Breaks rule four", "icon": "coins", "tone": "bad"},
          {"label": "Asks to “verify” your seed phrase", "sub": "Breaks rule one", "icon": "lock", "tone": "bad"}])
sc("chart3d", "And here's roughly where beginner losses actually come from, purely as an illustrative breakdown, to show why every lesson in this module earned its place. Seed-phrase phishing. Fake urgency and impersonated support. Unlimited approvals left open on an app you stopped using. And skipping the small test transfer on something new. Notice: rules one, ten, five and six, in that order.",
   chapter="Spotting it before it happens", kind="donut", title="Where beginner losses typically come from",
   sub="Illustrative breakdown, for discussion · not a real statistic",
   segs=[{"label": "Seed-phrase phishing", "value": 35, "text": "Rule one", "tone": "bad"}, {"label": "Urgency & fake support", "value": 30, "text": "Rule ten", "tone": "warn"},
         {"label": "Unlimited approvals left open", "value": 20, "text": "Rule five", "tone": "muted"}, {"label": "Skipped the small test first", "value": 15, "text": "Rule six"}])
sc("statement", "Notice that every slice of that chart already has its own dedicated defence, from a lesson you've already completed. Rule ten, stop when something feels urgent, would have caught almost all of it anyway, on its own, without you needing to identify which specific scam it was.",
   chapter="Spotting it before it happens", kicker="One rule, most of the protection", lines=["Every slice already has its defence.", "Rule ten alone would have caught most of it."], sub="You don't need to name the scam. You just need to stop.")
sc("statement", "One more thing worth knowing: every category on that chart gets a full lesson of its own, later in the program. Lesson one point six is entirely dedicated to scam defence, in real depth. For now, the ten rules you already have are enough to recognise all four of them the moment they show up.",
   "One more thing worth knowing: every category on that chart gets a full lesson of its own, later in the program. Lesson 1.6 is entirely dedicated to scam defence, in real depth. For now, the ten rules you already have are enough to recognise all four of them the moment they show up.",
   chapter="Spotting it before it happens", kicker="Coming back to this, properly", lines=["Every category gets its own lesson later.", "Lesson 1.6: scam defence, in depth."], sub="For now, the ten rules already cover all four.")

# ---------------------------------------------------------------- worked example
sc("title", "A real worked example.", chapter="A real worked example", eyebrow="A real worked example", num="60", title="Jordan's sixty-second check",
   sub="Two rules, applied in under a minute.")
sc("steps", "Jordan gets a D.M.: 'Your wallet has been flagged and will be suspended in one hour unless you verify it now.' It looks official, and it includes a link. Jordan doesn't click it. Rule three fires first: nobody legitimate D.M.s you first. Rule ten fires right behind it: the one-hour countdown is manufactured urgency, not a real deadline. Jordan opens their wallet directly, from a bookmark, not the link, and confirms nothing is wrong, wallets can't be 'suspended' in the first place. The message gets blocked and reported.",
   "Jordan gets a DM: 'Your wallet has been flagged and will be suspended in one hour unless you verify it now.' It looks official, and it includes a link. Jordan doesn't click it. Rule three fires first: nobody legitimate DMs you first. Rule ten fires right behind it: the one-hour countdown is manufactured urgency, not a real deadline. Jordan opens their wallet directly, from a bookmark, not the link, and confirms nothing is wrong, wallets can't be 'suspended' in the first place. The message gets blocked and reported.",
   chapter="A real worked example", title="What Jordan actually did",
   steps=["Received a DM: “verify now or your wallet is suspended”", "Rule three: nobody legitimate DMs you first", "Rule ten: the countdown is manufactured urgency", "Checked the wallet directly, from a bookmark, not the link", "Blocked and reported the message"],
   result="Total time: under a minute. Total funds at risk: zero.")
sc("statement", "Notice what made that safe wasn't cleverness, or spotting some sophisticated trick. It was two rules, recognised instantly, because Jordan already knew their names. That's the entire point of turning ten habits into ten memorable rules.",
   chapter="A real worked example", kicker="Recognised, not outsmarted", lines=["Two rules, recognised instantly.", "Because Jordan already knew their names."], sub="That's the whole point of naming the rules.")

# ---------------------------------------------------------------- checklist and quiz
sc("title", "Checklist and quiz.", chapter="Checklist and quiz", eyebrow="Checklist and quiz", num="5", title="Confirm you've got it",
   sub="Three boxes, and one milestone.")
sc("bullets", "Here's this lesson's checklist. You've read the ten rules, and can repeat them without looking. You've set up a separate browser profile for crypto. And you recognise every word in the glossary when you meet it again. Tick all three, and Module zero is genuinely complete.",
   chapter="Checklist and quiz", title="Before you move on", numbered=True,
   items=["Read the ten rules; can repeat them", "Separate browser profile set up for crypto", "Recognise every word in the glossary"])
sc("quiz", "Question one. Someone offers a 'guaranteed two percent a day'. What is it? [[pause 4]] The answer: a scam. Guaranteed returns simply don't exist; real yield moves with markets.",
   chapter="Checklist and quiz", n=1, of=5, q="Someone offers a “guaranteed 2% a day”. What is it?", a="A scam. Guaranteed returns don't exist.")
sc("quiz", "Question two. What's gas? [[pause 4]] The answer: the network fee for a transaction, paid in that network's own token.",
   chapter="Checklist and quiz", n=2, of=5, q="What's gas?", a="The network fee for a transaction, paid in the network's token.")
sc("quiz", "Question three. A message says your wallet will be 'suspended' unless you act in one hour. What do you do? [[pause 4]] The answer: stop. Urgency is a scam tactic. Wallets can't actually be suspended; check only through a bookmarked, official site.",
   chapter="Checklist and quiz", n=3, of=5, q="A message threatens your wallet will be “suspended” in 1 hour. What do you do?", a="Stop. Urgency is a scam tactic. Check only through bookmarked official sites.")
sc("quiz", "Question four. What's the difference between custodial and self-custody? [[pause 4]] The answer: custodial means an exchange holds your keys for you; self-custody means you hold them yourself, in your own wallet.",
   chapter="Checklist and quiz", n=4, of=5, q="What's the difference between custodial and self-custody?", a="Custodial: an exchange holds your keys. Self-custody: you hold them yourself.")
sc("quiz", "Question five. Which single rule would have caught almost every scam in this lesson's chart, on its own? [[pause 4]] The answer: rule ten. If something feels urgent, stop.",
   chapter="Checklist and quiz", n=5, of=5, q="Which single rule would have caught almost every scam in this lesson's chart, on its own?", a="Rule ten: if something feels urgent, stop.")

# ---------------------------------------------------------------- recap
sc("flow", "Here's the whole lesson, recapped as one loop. Protect: never share your seed phrase, and treat every guaranteed return as a scam. Verify: read every prompt, test small, and stop the moment something feels urgent. Maintain: keep devices updated and keep records, always. Do those three things, in that order, and you've built the security baseline this entire program is designed around.",
   chapter="Recap and next", title="This lesson, recapped as one loop", layout="cycle",
   nodes=[{"label": "Protect", "sub": "Never share your seed phrase", "icon": "lock"}, {"label": "Verify", "sub": "Read every prompt, test small, stop at urgency", "icon": "eye"}, {"label": "Maintain", "sub": "Devices updated, records kept", "icon": "shield"}])
sc("statement", "This is education, not financial advice, and every dollar figure and every chart in this lesson is illustrative. That said, this specific lesson matters more than most: nobody from this program, or any real one, will ever ask for your seed phrase, private keys or account access. Not once.",
   chapter="Recap and next", kicker="A reminder", lines=["Every figure here is illustrative.", "We never ask for your keys. Not once."], sub="Not financial advice. This one matters more than most.")
sc("cta", "That's your security baseline, and the language of DeFi, and with it, Module zero is complete. Next, Module one begins properly: what DeFi actually is, and the risk-first mindset that runs through everything from here on.",
   chapter="Recap and next", button="Next: Module 1", sub="What DeFi is, and the risk-first mindset")

spec = {"id": "lesson-00-8", "title": "Lesson 0.8: Your security baseline, and the language of DeFi", "size": [1920, 1080], "group": "lessons", "maxMinutes": 25, "tag": "Lesson 0.8",
        "gold": True, "seed": 48,
        "use": "Lesson 0.8 page in the Whop course. Gold-standard script: Module 0's capstone. The 10 rules grouped by theme, the full 18-word glossary across 4 ticker scenes, an anatomy-of-a-scam flow3d anchor, an illustrative where-losses-come-from chart3d donut anchor, and Jordan's real worked example.",
        "thumbnail": {"title": "Security baseline & glossary", "subtitle": "Lesson 0.8"}, "scenes": S}
out = ROOT / "video-scripts" / "gold" / "lesson-00-8.json"
out.write_text(json.dumps(spec, indent=1, ensure_ascii=False))
words = sum(len(s["vo"].replace("[[pause 4]]", "").split()) for s in S)
print(f"{len(S)} scenes, {words} words, est {(words / 171 * 60 + len(S) * 1.3 + 5 * 3) / 60:.1f} min")
