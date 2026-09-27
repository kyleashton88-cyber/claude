#!/usr/bin/env python3
"""Gold-standard script for Lesson 6.0, the Module 6 Mastery Starter
(target 11-14 minutes, per the "a bit longer" note for lessons from here
on). Protocol Research: the six-step research loop a professional runs
every single time (what it does, where its money comes from, what it
depends on, whether it's solvent, what the evidence says, how to get
out). Teaches the module's five words (due diligence, TVL, FDV,
governance, thesis) and the mastery ladder with animated flows, reusing
the module's own research-loop.png and module-06.png diagrams. Mirrors
the Lesson 1.0-5.0 Mastery Starter pattern, written in one pass at the
full target length, with a wider icon vocabulary per the standing note.

Writes video-scripts/gold/lesson-06-0.json (the generator skips lessons
with a gold script). Spoken text (vo) spells numbers for the voice; cap is
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
M = "assets/modules/"

# ---------------------------------------------------------------- intro
sc("title", "Lesson six point zero. The Mastery Starter for Module Six: Protocol Research. By the end, you'll know the five words this module runs on, and exactly how to tell when you've mastered it.",
   "Lesson 6.0. The Mastery Starter for Module 6: Protocol Research. By the end, you'll know the five words this module runs on, and exactly how to tell when you've mastered it.",
   chapter="Intro", eyebrow="Lesson 6.0 · Mastery Starter", num="6.0", title="Protocol Research", sub="Your map for Module 6, in pictures.")
sc("pillars", "Here's the plan. First, the sixty-second version: the same six-step loop a professional actually runs, every single time, before ever trusting a protocol with money. Second, the five words you'll need, each one drawn out. Third, what to have ready before you start. Fourth, your first safe step: running that six-step loop on one real protocol today. And finally, the mastery ladder, so you know exactly what finishing this module looks like.",
   chapter="Intro", title="What this lesson covers",
   items=[{"icon": "search", "title": "The 60-second version", "text": "The same six-step loop, every single time"}, {"icon": "book", "title": "Five words", "text": "Drawn out, not just defined"},
          {"icon": "clock", "title": "Before you start", "text": "Modules 0-5"}, {"icon": "target", "title": "The ladder", "text": "How you'll know you've mastered it"}])

# ---------------------------------------------------------------- the 60-second version
sc("statement", "Here's the whole module in one sentence. Before trusting any protocol with real money, a professional researches it the same exact way, every single time: what it actually does, where its money genuinely comes from, what it actually depends on, whether it's genuinely solvent, what the real evidence actually says, and precisely how you'd get out. This module teaches you that same repeatable loop.",
   chapter="The 60-second version", kicker="The 60-second version", lines=["The same six-step loop, run every single time.", "Not a different process for every new protocol."], sub="This module teaches you that one loop, run consistently.")
img(D + "research-loop.png", "The six-step research loop",
    "Here's that loop, laid out in full, the exact same six steps this entire module builds on. Mechanism: what it actually does, and how. Cash flow: where its money genuinely comes from. Dependencies: everything it actually relies on, from Module five's own dependency map. Solvency: whether it can genuinely cover what it owes. Evidence: what real, verifiable data actually says. And exit: precisely how, and how fast, you could genuinely get out.",
    chapter="The 60-second version")
sc("flow", "Here's all six steps, named individually, since each one asks a genuinely different question you'll come back to throughout this module. Mechanism: what does it actually do. Cash flow: where does its money genuinely come from. Dependencies: what does it actually rely on. Solvency: can it genuinely cover what it owes. Evidence: what does real, verifiable data actually say. And exit: how, and how fast, could you actually get out.",
   chapter="The 60-second version", title="The six steps, named individually",
   nodes=[{"label": "1. Mechanism", "sub": "What does it actually do", "icon": "cog"}, {"label": "2. Cash flow", "sub": "Where does its money come from", "icon": "coins"},
          {"label": "3. Dependencies", "sub": "What does it actually rely on", "icon": "layers"}, {"label": "4. Solvency", "sub": "Can it cover what it owes", "icon": "scale"},
          {"label": "5. Evidence", "sub": "What does real data actually say", "icon": "search"}, {"label": "6. Exit", "sub": "How, and how fast, could you leave", "icon": "exit"}])
sc("statement", "Worth being direct about why running this exact same loop, every time, actually matters, rather than improvising a fresh process for each new protocol. Consistency is what actually lets you compare one protocol against another honestly, and it's what stops you from skipping the one specific step that happens to feel unnecessary for whatever protocol currently has your attention.",
   chapter="The 60-second version", kicker="Why the same loop, every time", lines=["Consistency lets you compare protocols honestly.", "It stops you skipping the one step that feels unnecessary this time."], sub="The loop doesn't change. Only the protocol you're pointing it at does.")

# ---------------------------------------------------------------- words you'll need
sc("title", "Now, the five words you'll need.", chapter="Words you'll need", eyebrow="Words you'll need", num="5", title="Five words, drawn out",
   sub="Due diligence · TVL · FDV · Governance · Thesis")
sc("flow", "Word one: due diligence. Structured research, run before you ever invest, not after. Here's the actual sequence it follows. You define the specific questions worth answering, using the six-step loop. You gather real, verifiable evidence for each one. And you reach an actual verdict, with a size, conditions, and an exit, rather than simply a vague overall feeling about the protocol.",
   chapter="Words you'll need", title="What due diligence actually is",
   nodes=[{"label": "Define the questions", "sub": "Using the six-step loop", "icon": "search"}, {"label": "Gather real evidence", "sub": "For each specific question", "icon": "doc"},
          {"label": "Reach an actual verdict", "sub": "Size, conditions, and an exit", "icon": "scale"}])
sc("statement", "Word two: T.V.L., total value locked. The total value currently deposited in a protocol. It's a genuinely useful signal of real, current usage, but it's not, on its own, any kind of safety guarantee; a protocol can hold enormous T.V.L. and still fail, exactly the way this module's earlier lessons on infrastructure risk already covered.",
   chapter="Words you'll need", kicker="Word two: TVL", lines=["Total value currently deposited in a protocol.", "A real usage signal. Never a safety guarantee on its own."], sub="High TVL tells you it's used. It doesn't tell you it's safe.")
sc("statement", "Word three: F.D.V., fully diluted valuation. Token price, multiplied by the maximum supply that could ever genuinely exist. It's worth comparing directly against a protocol's own actual, current market cap, since a large gap between the two tells you a great deal about how much future dilution current holders are actually exposed to.",
   chapter="Words you'll need", kicker="Word three: FDV", lines=["Token price × maximum possible supply.", "Compare it against current market cap for the real dilution picture."], sub="A large gap here is a real signal, worth checking every time.")
sc("stats", "Here's why checking F.D.V. against current market cap actually matters, using a purely illustrative example. A token might show a current market cap of one hundred million dollars, genuinely tradeable today, but an F.D.V. of one billion, ten times larger, once every token that could ever exist is actually counted. That gap is real future dilution, worth knowing before you buy, not after.",
   chapter="Words you'll need", title="Market cap vs. FDV (illustrative)",
   stats=[["$100M", "Current market cap"], ["$1B", "Fully diluted valuation"], ["10×", "The real dilution gap"]])
sc("quiz", "Quick check. What does F.D.V. actually measure? [[pause 4]] The answer: token price, multiplied by the maximum supply that could ever genuinely exist.",
   chapter="Words you'll need", n=1, of=2, q="What does FDV measure?",
   a="Token price × maximum supply.")
sc("statement", "Word four: governance. How a protocol's own token holders actually vote on real changes: upgrades, parameters, treasury spending, all of it. Worth checking specifically how concentrated that voting power actually is, since governance controlled by a genuinely small handful of large holders behaves very differently from governance spread broadly across many.",
   chapter="Words you'll need", kicker="Word four: governance", lines=["How token holders actually vote on real changes.", "Check how concentrated that voting power genuinely is."], sub="Concentrated governance is a real, checkable risk, not an abstraction.")
sc("statement", "Word five: thesis. What genuinely has to be true, specifically, for a position to actually work out the way you expect. Writing it down explicitly is what lets you actually notice, later, the exact moment that thesis breaks, rather than simply continuing to hold out of habit, or hope, once the real conditions have already changed.",
   chapter="Words you'll need", kicker="Word five: thesis", lines=["What has to be true for the position to work.", "Writing it down lets you notice the moment it breaks."], sub="A thesis without an invalidation condition isn't really a thesis at all.")
sc("quiz", "Quick check. What's the actual purpose of writing down your thesis explicitly? [[pause 4]] The answer: it lets you genuinely notice the moment it breaks, rather than continuing to hold purely out of habit or hope.",
   chapter="Words you'll need", n=2, of=2, q="What's the purpose of writing down your thesis?",
   a="It lets you notice the moment it breaks, rather than holding out of habit.")

# ---------------------------------------------------------------- before you start
sc("title", "Before you start.", chapter="Before you start", eyebrow="Before you start", num="1", title="What this module assumes you already have",
   sub="Modules zero through five.")
sc("steps", "Here's what this module assumes you're already comfortable with, before diving in. Everything from Module zero through two: wallets, networks, swaps, and liquidity. Modules three and four: lending, leverage, and where yield genuinely comes from. And Module five, in full: the complete dependency map, since dependencies are exactly step three of this module's own six-step loop.",
   chapter="Before you start", title="What you should already have",
   steps=["Modules 0-2: wallets, networks, swaps, liquidity", "Modules 3-4: lending, leverage, yield sources", "Module 5, in full: the complete dependency map"], result="Dependencies is step 3 of this module's own loop — Module 5 feeds directly into it")

# ---------------------------------------------------------------- your first safe step
sc("title", "Your first safe step.", chapter="Your first safe step", eyebrow="Your first safe step", num="1", title="Run the loop on one real protocol",
   sub="Today. Even a one-sentence answer per step is enough to start.")
sc("steps", "Here's exactly what to do, before this module goes any deeper into each individual step. Pick any protocol you've genuinely heard of, one you're at least somewhat familiar with. Write exactly one sentence for each of the six steps: mechanism, cash flow, dependencies, solvency, evidence, and exit. And if you genuinely don't know the answer for one, write don't know yet, honestly, rather than guessing.",
   chapter="Your first safe step", title="Running the loop for the first time",
   steps=["Pick a protocol you've genuinely heard of", "Write one sentence per step: mechanism, cash flow, dependencies, solvency, evidence, exit", "Don't know one? Write \"don't know yet\", honestly"], result="A real first pass. Not a perfect one, a real one")
sc("statement", "Worth being direct about why don't know yet is a genuinely acceptable, even valuable, answer here, rather than something to avoid writing down. It tells you exactly where your own research actually has to go next, specifically. A confident guess, dressed up as a real answer, is far more dangerous than an honestly incomplete one.",
   chapter="Your first safe step", kicker="Why \"don't know yet\" is a real answer", lines=["It tells you exactly where your research has to go next.", "A confident guess is far more dangerous than an honest gap."], sub="Honesty here is the actual skill this first step is building.")

# ---------------------------------------------------------------- the mastery ladder
sc("title", "The mastery ladder.", chapter="The mastery ladder", eyebrow="The mastery ladder", num="1", title="Three levels, each building on the last",
   sub="Know exactly where you are, and what's next.")
sc("compare", "Here's the first two rungs on this module's ladder, side by side. At the beginner level, you can complete the full six-step loop, with real sources backing each step. At the practitioner level, you go further: genuinely reading tokenomics and governance directly, and writing an actual thesis that includes its own specific invalidation condition.",
   chapter="The mastery ladder",
   left={"label": "Beginner", "tone": "warn", "items": ["Completes the six-step loop, with sources", "The full loop, done honestly"]},
   right={"label": "Practitioner", "tone": "good", "items": ["Reads tokenomics and governance directly", "Writes a thesis with its own invalidation condition"]})
sc("flow", "Here's what practitioner-level tokenomics and governance reading actually looks like, concretely. Check how concentrated token holdings genuinely are, among the largest wallets. Check exactly how much voting power that same concentration actually translates into. And write your thesis with a specific, real invalidation condition attached, not simply a general, vague sense of optimism about the protocol.",
   chapter="The mastery ladder", title="Practitioner level, in practice",
   nodes=[{"label": "Check holder concentration", "sub": "Among the largest wallets", "icon": "users"}, {"label": "Check voting-power concentration", "sub": "How much that translates into control", "icon": "scale"},
          {"label": "Write a thesis with real invalidation", "sub": "Not just general optimism", "icon": "doc"}])
sc("statement", "And here's the top rung, master level, the one this module ultimately builds toward. At that level, you can genuinely spot failure patterns early, often before they're obvious to everyone else, and write verdicts other people can actually act on directly, not just your own private notes.",
   chapter="The mastery ladder", kicker="Master level", lines=["Spots failure patterns early, before they're obvious.", "Writes verdicts other people can actually act on."], sub="Not just your own notes. A verdict someone else could use.")
sc("statement", "Here's how you'll actually know you've mastered this entire module, in one sentence. Your due-diligence file ends in a real verdict, specifically with a size, real conditions, and an actual exit, every single time, not simply a vague, unresolved impression of the protocol.",
   chapter="The mastery ladder", kicker="You've mastered this module when…", lines=["Your file ends in a verdict: size, conditions, exit.", "Every time. Not a vague, unresolved impression."], sub="That's the actual finish line for this module.")

# ---------------------------------------------------------------- recap
sc("title", "What a real verdict actually looks like.", chapter="The mastery ladder", eyebrow="The mastery ladder", num="2", title="Size, conditions, and an exit, made concrete",
   sub="Not a feeling. An actual, written decision.")
sc("steps", "Here's what a real verdict genuinely looks like, in practice, not as an abstract requirement. A size: a specific, capped dollar amount, decided in advance, not an open-ended one. Conditions: the specific facts that currently make this position acceptable, written down explicitly. And an exit: the exact condition that would actually make you leave, decided now, before you're emotionally attached to the outcome.",
   chapter="The mastery ladder", title="Size, conditions, exit — an example shape",
   steps=["Size: a specific, capped amount, decided in advance", "Conditions: the specific facts that currently make it acceptable", "Exit: the exact condition that would make you leave, decided now"])
sc("bullets", "Let's recap. The six-step loop: mechanism, cash flow, dependencies, solvency, evidence, exit, run the same way every single time. The five words: due diligence, T.V.L., F.D.V., governance, and thesis. Your first safe step is running that loop, in one sentence per step, on one real protocol today. And you'll know you've mastered this module when your file ends in a real verdict, with a size, conditions, and an exit.",
   chapter="Recap", title="Recap", check=False,
   items=["The six-step loop: mechanism, cash flow, dependencies, solvency, evidence, exit", "Five words: due diligence, TVL, FDV, governance, thesis",
          "First step: one sentence per step, on one real protocol, today", "Mastered when: your file ends in a verdict — size, conditions, exit"])
sc("cta", "Pick one real protocol today, and write one honest sentence for each of the six steps. Next up, Lesson six point one: protocol due diligence.",
   "Pick one real protocol today, and write one honest sentence for each of the six steps. Next up, Lesson 6.1: protocol due diligence.",
   chapter="Recap", button="Next: Lesson 6.1", sub="Protocol due diligence")

spec = {"id": "lesson-06-0", "title": "Lesson 6.0: Mastery Starter — Protocol Research", "size": [1920, 1080], "group": "lessons", "maxMinutes": 25,
        "tag": "Lesson 6.0 · Mastery Starter", "gold": True, "music": True, "musicLevel": 0.14, "seed": 87,
        "use": "Lesson 6.0 page in the Whop course. Hand-written gold-standard Mastery Starter script for Module 6: the 60-second version, the module's five words, before-you-start, first safe step, and mastery ladder, as walk-throughs.",
        "thumbnail": {"title": "Protocol Research: Mastery Starter", "subtitle": "Lesson 6.0"}, "scenes": S}
out = ROOT / "video-scripts" / "gold" / "lesson-06-0.json"
out.write_text(json.dumps(spec, indent=1, ensure_ascii=False))
words = sum(len(s["vo"].replace("[[pause 4]]", "").split()) for s in S)
print(f"{len(S)} scenes, {words} words, est {(words / 171 * 60 + len(S) * 1.3 + 4 * 2) / 60:.1f} min")
