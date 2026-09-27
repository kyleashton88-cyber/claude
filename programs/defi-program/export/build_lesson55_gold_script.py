#!/usr/bin/env python3
"""Gold-standard script for Lesson 5.5, Smart-contract risk & what audits
don't prove (target 11-14 minutes, per the "a bit longer" note for
lessons from here on). Walks the common failure types (logic bugs,
reentrancy, broken access control, economic exploits), what an audit
actually covers (scope, date, severity, fixed?), bug bounties, time and
value at risk as a real signal, and the source material's own worked
example (Protocol X: two audits, but last month's upgrade isn't in either
scope; a $50k bounty against $400M TVL; size down or wait), as visual
walk-throughs. Written in one pass at the full target length (no separate
expansion round).

Writes video-scripts/gold/lesson-05-5.json (the generator skips lessons
with a gold script). Spoken text (vo) spells numbers for the voice; cap is
the written caption, same sentence count as vo."""
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
sc("title", "Lesson five point five. Smart-contract risk, and what audits don't prove. By the end, you'll be able to weigh contract risk honestly, and read an audit for exactly what it actually covers, not what its own name implies.",
   "Lesson 5.5. Smart-contract risk & what audits don't prove. By the end, you'll be able to weigh contract risk honestly, and read an audit for exactly what it actually covers, not what its own name implies.",
   chapter="Intro", eyebrow="Lesson 5.5", num="5.5", title="Smart-contract risk & what audits don't prove", sub="An audit reviews specific code, at a specific time. Never more than that.")
sc("pillars", "Here's the plan. The four common failure types behind most real smart-contract losses. What an audit actually covers, and precisely what it doesn't. Bug bounties, and why their size matters relative to the value at stake. And a full worked example, reading a real protocol's real audit and bounty numbers together.",
   chapter="Intro", title="What this lesson covers",
   items=[{"icon": "alert", "title": "Four failure types", "text": "Logic bugs, reentrancy, access control, economic exploits"}, {"icon": "shield", "title": "What an audit covers", "text": "Scope, date, severity of findings, whether fixed"},
          {"icon": "coins", "title": "Bug bounties", "text": "Size matters, relative to the value they're protecting"}, {"icon": "target", "title": "Worked example", "text": "Two audits, one unaudited upgrade, a small bounty"}])

# ---------------------------------------------------------------- four failure types
sc("title", "The four common failure types.", chapter="Four failure types", eyebrow="Four failure types", num="4", title="Behind most real smart-contract losses",
   sub="Logic bugs · Reentrancy · Broken access control · Economic exploits")
img(D + "audit-coverage.png", "What an audit actually covers",
    "Here are the four failure types behind most real smart-contract losses. Logic bugs, straightforward mistakes in how the code is actually written. Reentrancy, where a contract gets called back into, before it's finished updating its own state, letting an attacker repeat an action it should only have allowed once. Broken access control, where a function that should be restricted simply isn't, properly. And economic exploits, where the code itself is technically correct, but the incentives, or the oracles, underneath it can be exploited anyway.",
    chapter="Four failure types")
sc("statement", "Worth naming the other two failure types specifically too, since reentrancy and economic exploits tend to get most of the attention. A logic bug is simply a straightforward mistake in the code itself, an off-by-one error, a wrong comparison, a case the developer genuinely didn't account for. Broken access control means a function that should have been restricted to specific callers simply wasn't, letting anyone call it directly.",
   chapter="Four failure types", kicker="The other two failure types", lines=["A logic bug: a straightforward mistake in the code itself.", "Broken access control: a restricted function that simply wasn't."], sub="Neither one is exotic. Both are genuinely common, and genuinely findable.")
sc("statement", "Worth being precise about that fourth category specifically, since it's the one most likely to be missed by a purely code-focused review. An economic exploit doesn't require finding any bug in the code at all; the code can execute exactly as written, every single time, and still be drained, because the underlying incentives or price feeds it depends on were exploitable from the start.",
   chapter="Four failure types", kicker="Why economic exploits get missed", lines=["No bug required. The code can run exactly as written.", "And still be drained, because the incentives underneath it were exploitable."], sub="This is exactly why Lesson 5.3's oracle risks matter here too.")
sc("quiz", "Quick check. What exactly is reentrancy? [[pause 4]] The answer: a contract being called back into before it's finished updating its own state, letting an attacker repeat an action it should only have allowed once.",
   chapter="Four failure types", n=1, of=3, q="What is reentrancy?",
   a="A contract being called back before it finishes updating its state, letting an attacker repeat actions.")

# ---------------------------------------------------------------- what an audit covers
sc("title", "What an audit actually covers.", chapter="What an audit covers", eyebrow="What an audit covers", num="1", title="Specific code, at a specific time",
   sub="Never more than that. Check scope, date, severity, and whether it was fixed.")
sc("flow", "Here's exactly what to check on any audit, before trusting its name alone. Its scope: specifically which contracts it actually reviewed, not just the protocol's name in general. Its date: specifically whether it happened before or after any later code changes. The severity of whatever it actually found. And whether those specific findings were genuinely fixed afterward, not simply noted and left as-is.",
   chapter="What an audit covers", title="What to actually check on any audit",
   nodes=[{"label": "Scope", "sub": "Which specific contracts it reviewed", "icon": "chart"}, {"label": "Date", "sub": "Before or after any later code changes?", "icon": "clock"},
          {"label": "Severity of findings", "sub": "What it actually found, and how serious", "icon": "alert"}, {"label": "Fixed?", "sub": "Genuinely resolved, or just noted?", "icon": "check"}])
sc("statement", "Worth being completely direct about the actual limit of what any audit can honestly claim, since the word itself tends to imply far more certainty than it should. An audit reviews specific code, at one specific point in time. It says nothing at all about code deployed afterward, and it can genuinely miss an economic exploit entirely, if that exploit never required a code-level bug to begin with.",
   chapter="What an audit covers", kicker="The actual limit of an audit", lines=["It reviews specific code, at one specific point in time.", "Nothing about later code. Can miss an economic exploit entirely."], sub="An audit is a real signal. It is not a guarantee, at any point after it happened.")
sc("quiz", "Quick check. What does an audit actually not prove? [[pause 4]] The answer: that the code, any later changes to it, or the economic design underneath it, is genuinely safe.",
   chapter="What an audit covers", n=2, of=3, q="What does an audit not prove?",
   a="That the code (or later changes, or economic design) is safe.")

# ---------------------------------------------------------------- bug bounties and time at risk
sc("title", "Bug bounties, and time at risk.", chapter="Bug bounties & time at risk", eyebrow="Bug bounties & time at risk", num="1", title="Two more real signals, beyond the audit itself",
   sub="Neither one is a substitute for the other.")
sc("statement", "Worth being precise about what a bug bounty actually does, and why its size relative to the protocol's own value matters so directly. It pays hackers to responsibly report a vulnerability, instead of quietly exploiting it themselves. A large, genuinely active bounty is a good sign specifically because it makes responsible disclosure the more financially attractive choice, compared with an exploit.",
   chapter="Bug bounties & time at risk", kicker="What a bug bounty actually does", lines=["Pays hackers to report responsibly, instead of exploiting quietly.", "A large one makes disclosure the more attractive choice."], sub="Its size only means something relative to what it's actually protecting.")
sc("title", "The same $50,000, at very different scales.", chapter="Bug bounties & time at risk", eyebrow="Bug bounties & time at risk", num="2", title="Why the ratio matters more than the raw number",
   sub="Purely illustrative, holding the bounty fixed at $50,000.")
sc("chart", "Here's that exact same fifty thousand dollar bounty, held fixed, but measured against six genuinely different total-value-locked scales, purely illustrative, to show why the ratio matters far more than the raw dollar figure. Against one million dollars of T.V.L., fifty thousand dollars is five percent, a genuinely strong incentive. Against one hundred million, it's down to zero point zero five percent. And against the source material's own four hundred million, just zero point zero one two five percent, vanishingly small.",
   chapter="Bug bounties & time at risk", title="$50,000 bounty, as a share of TVL (illustrative)", kind="line",
   xlabels=["$1M", "$10M", "$50M", "$100M", "$400M"], ymin=0, ymax=5.5,
   yticks=[[0, "0%"], [2.5, "2.5%"], [5, "5%"]],
   series=[{"values": [5, 0.5, 0.1, 0.05, 0.0125], "tone": "warn", "label": "Bounty as % of TVL"}],
   marks=[{"i": 0, "text": "5% — strong incentive", "tone": "good"}, {"i": 4, "text": "0.0125% — Protocol X's own case", "tone": "bad", "below": True}])
sc("statement", "Notice how quickly that ratio collapses, as the exact same bounty gets measured against genuinely larger protocols. A fifty thousand dollar bounty was never actually the fixed, meaningful number; it's only ever meaningful relative to what it's protecting, and it can look perfectly reasonable, or nearly irrelevant, depending entirely on that one ratio.",
   chapter="Bug bounties & time at risk", kicker="Why the ratio collapses so fast", lines=["The same bounty, measured against larger protocols, means less.", "It's only ever meaningful relative to what it's protecting."], sub="Always compute the ratio yourself. Never just read the headline number.")
sc("steps", "Here's how to actually check an audit's scope and date yourself, rather than trusting a badge or a headline claim. Open the audit report itself, and read its stated scope section directly, for the exact contract addresses covered. Compare that report's own date against the protocol's own deployment history, for the currently live contracts. And if the two don't line up, treat the gap between them as genuinely unaudited, full stop.",
   chapter="Bug bounties & time at risk", title="Checking scope and date yourself",
   steps=["Read the audit's stated scope for the exact contract addresses covered", "Compare its date against the protocol's own deployment history", "Any gap between them: treat as genuinely unaudited"])
sc("flow", "Here's why code that's safely held large value for a genuinely long time is itself a real, meaningful signal, separate from any audit. Every day that code sits there, holding real, significant value, is another day skilled, motivated attackers have genuinely had the opportunity to find a flaw in it, and haven't succeeded. That's not proof of safety either, but it's real, accumulated evidence, earned specifically by surviving real attempts.",
   chapter="Bug bounties & time at risk", title="Why time and value at risk matters",
   nodes=[{"label": "Real value, held for real time", "sub": "Every day is another day attackers had a real shot", "icon": "clock"}, {"label": "And they haven't succeeded", "sub": "Not proof. But real, accumulated evidence", "icon": "shield"}])

sc("statement", "Worth being direct about how these three signals actually combine, since none of them alone is genuinely sufficient on its own. A recent, well-scoped audit, a meaningfully sized bounty relative to T.V.L., and real time safely holding real value together, are what actually build honest confidence. Any one of the three, missing or weak, is a real gap worth pricing in directly, not explaining away.",
   chapter="Bug bounties & time at risk", kicker="How these three signals actually combine", lines=["None of the three alone is genuinely sufficient.", "A real gap in any one is worth pricing in, not explaining away."], sub="Audit. Bounty size. Time at risk. Check all three, together.")

# ---------------------------------------------------------------- worked example
sc("title", "Worked example.", chapter="Worked example", eyebrow="Worked example", num="1", title="Protocol X: two audits, one big gap",
   sub="The source material's own scenario.")
sc("steps", "Here's Protocol X, exactly as the source material lays it out. It has two audits on record. But its latest upgrade, deployed just last month, isn't actually covered in either audit's scope. Its bug bounty sits at fifty thousand dollars. Its total value locked sits at four hundred million dollars.",
   chapter="Worked example", title="Protocol X, as it actually stands",
   steps=["Two audits on record", "Latest upgrade (last month): not in either audit's scope", "Bug bounty: $50,000. TVL: $400,000,000"], result="The newest code is unaudited, and the bounty is small relative to the value")
sc("stats", "Here's what that bounty-to-value ratio actually looks like, precisely, once you compute it directly. Fifty thousand dollars, against four hundred million dollars, comes to just zero point zero one two five percent of total value locked, an extremely small incentive relative to what's genuinely at stake if a real flaw exists in that unaudited upgrade.",
   chapter="Worked example", title="$50,000 bounty vs. $400,000,000 TVL",
   stats=[["$50,000", "Bug bounty"], ["$400M", "Total value locked"], ["0.0125%", "Bounty, as a share of TVL"]])
sc("statement", "Here's the one sentence this entire worked example exists to prove, worth holding onto more than the specific numbers involved. The newest code, the part actually deployed most recently, is entirely unaudited, and the financial incentive to report a flaw in it responsibly is genuinely tiny, relative to what a successful exploit against four hundred million dollars could actually be worth.",
   chapter="Worked example", kicker="The one sentence to keep", lines=["The newest code is entirely unaudited.", "The incentive to report is tiny, relative to what an exploit could be worth."], sub="Size down, or wait for that specific upgrade to actually be reviewed.")
sc("statement", "Worth being concrete about what size down, or wait actually means here, rather than leaving it as an abstract recommendation. Size down means genuinely reducing the position specifically in that unaudited upgrade, to an amount you'd be fully fine losing outright. Wait means holding off entirely, until a real audit actually covers that exact code, rather than assuming the earlier two audits somehow still apply.",
   chapter="Worked example", kicker="What 'size down or wait' actually means", lines=["Size down: an amount you'd be fully fine losing outright.", "Wait: until a real audit covers that exact code, not the earlier ones."], sub="Neither option requires avoiding the protocol entirely. Both require being honest about the gap.")
sc("quiz", "Quick check. Why does it actually matter to check an audit's own date? [[pause 4]] The answer: any code changed after that audit happened was never reviewed by it at all.",
   chapter="Worked example", n=3, of=3, q="Why check audit dates?",
   a="Code changed after the audit wasn't reviewed.")

# ---------------------------------------------------------------- checklist and recap
sc("steps", "Here's your checklist. Do it before trusting any contract's own audit claims. Confirm the audit's scope genuinely matches the currently deployed code, and its date comes after the last real upgrade. Confirm any critical or high-severity findings were actually resolved, not just noted. And check the bug bounty's actual size, specifically relative to the protocol's own total value locked.",
   chapter="Checklist", title="Your checklist",
   steps=["Audit scope matches deployed code; date after last upgrade", "Critical/high findings resolved", "Bug bounty size relative to TVL checked"])
sc("bullets", "Let's recap. Four common failure types: logic bugs, reentrancy, broken access control, and economic exploits that need no code bug at all. An audit reviews specific code, at a specific time; check its scope, date, findings, and whether they were fixed. A bug bounty's size only matters relative to the value it's protecting. Time and value safely held is real evidence, though never proof. And Protocol X shows exactly why all of this matters together: two audits, but the newest code isn't in either one.",
   chapter="Recap", title="Recap", check=False,
   items=["Four failure types: logic bugs, reentrancy, access control, economic exploits", "An audit covers specific code, at a specific time — check scope, date, fixed?",
          "A bug bounty's size only matters relative to the value it protects", "Time and value safely held is real evidence, though never proof"])
sc("cta", "Check the audit's scope and date, confirm findings were fixed, and check the bounty relative to TVL. Next up, Lesson five point six: beyond Ethereum, Solana, Bitcoin, and other ecosystems.",
   "Check the audit's scope and date, confirm findings were fixed, and check the bounty relative to TVL. Next up, Lesson 5.6: beyond Ethereum — Solana, Bitcoin and other ecosystems.",
   chapter="Recap", button="Next: Lesson 5.6", sub="Beyond Ethereum: Solana, Bitcoin and other ecosystems")

spec = {"id": "lesson-05-5", "title": "Lesson 5.5: Smart-contract risk & what audits don't prove", "size": [1920, 1080], "group": "lessons", "maxMinutes": 25,
        "tag": "Lesson 5.5", "gold": True, "music": True, "musicLevel": 0.14, "seed": 83,
        "use": "Lesson 5.5 page in the Whop course. Hand-written gold-standard script: the four common failure types, what an audit actually covers, bug bounties and time-at-risk as signals, and the source material's own Protocol-X worked example, as walk-throughs.",
        "thumbnail": {"title": "Smart-contract risk & audits", "subtitle": "Lesson 5.5"}, "scenes": S}
out = ROOT / "video-scripts" / "gold" / "lesson-05-5.json"
out.write_text(json.dumps(spec, indent=1, ensure_ascii=False))
words = sum(len(s["vo"].replace("[[pause 4]]", "").split()) for s in S)
print(f"{len(S)} scenes, {words} words, est {(words / 171 * 60 + len(S) * 1.3 + 4 * 3) / 60:.1f} min")
