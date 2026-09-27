#!/usr/bin/env python3
"""Gold-standard script for Lesson 4.0, the Module 4 Mastery Starter
(target 11-14 minutes, following the "a bit longer" note for lessons from
here on). Yield: what every yield is actually payment for, the module's
five words (APY, emissions, staking, LST, RWA), and the mastery ladder,
reusing the module's own profit-sources.png diagram. Mirrors the Lesson
1.0/2.0/3.0 Mastery Starter pattern, written in one pass at the full
target length.

Writes video-scripts/gold/lesson-04-0.json (the generator skips lessons
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
sc("title", "Lesson four point zero. The Mastery Starter for Module Four: Yield. By the end, you'll know the five words this module runs on, and exactly how to tell when you've mastered it.",
   "Lesson 4.0. The Mastery Starter for Module 4: Yield. By the end, you'll know the five words this module runs on, and exactly how to tell when you've mastered it.",
   chapter="Intro", eyebrow="Lesson 4.0 · Mastery Starter", num="4.0", title="Yield", sub="Your map for Module 4, in pictures.")
sc("pillars", "Here's the plan. First, the sixty-second version: what every single yield you'll ever see is actually payment for. Second, the five words you'll need, each one drawn out on its own. Third, what to have ready before you start. Fourth, your first safe step: splitting one real, advertised A.P.Y. into its actual parts. And finally, the mastery ladder, so you know exactly what finishing this module looks like.",
   chapter="Intro", title="What this lesson covers",
   items=[{"icon": "coins", "title": "The 60-second version", "text": "Every yield is payment for a risk"}, {"icon": "book", "title": "Five words", "text": "Drawn out, not just defined"},
          {"icon": "clock", "title": "Before you start", "text": "Modules 0-3"}, {"icon": "target", "title": "The ladder", "text": "How you'll know you've mastered it"}])

# ---------------------------------------------------------------- the 60-second version
sc("statement", "Here's the whole module in one sentence. Every yield you'll ever come across is payment for something specific: staking pays you to help secure a network, lending pays you for taking on borrower demand, and farms often pay you in newly printed tokens, to attract deposits. This module teaches you to see exactly what any given yield is really paying for.",
   chapter="The 60-second version", kicker="The 60-second version", lines=["Every yield is payment for a risk.", "This module teaches you to see which one."], sub="Once you can name it, an APY stops being a mystery number.")
img(D + "profit-sources.png", "Where DeFi returns actually come from",
    "Here's the mechanism underneath every source of yield in this entire module. Real, organic yield comes from genuine economic activity: trading fees paid by real traders, interest paid by real borrowers, or a network paying real value for real security work. Subsidised yield, by contrast, comes from a protocol printing brand-new tokens and handing them out, specifically to attract deposits it wants right now. Both can show up as the exact same-looking A.P.Y. number on a dashboard.",
    chapter="The 60-second version")
sc("statement", "This distinction is the single most useful skill this entire module builds, so it's worth sitting with before moving on. Two protocols can advertise the exact same double-digit A.P.Y., and mean completely different things by it: one genuinely earned from real activity, durable for as long as that activity continues; the other manufactured from token emissions, and only as durable as the protocol's willingness, or ability, to keep printing.",
   chapter="The 60-second version", kicker="Why this distinction matters most", lines=["The same-looking APY number can mean two very different things.", "One is durable. The other lasts only as long as the printing does."], sub="This module teaches you to tell which one you're actually looking at.")
sc("title", "The same number, two very different sources.", chapter="The 60-second version", eyebrow="The 60-second version", num="2", title="A purely illustrative split",
   sub="Figures below are illustrative only, to show the shape of the idea.")
sc("stats", "Here's a purely illustrative example, just to make the shape of this concrete, not a claim about any specific real protocol. Imagine a headline A.P.Y. of thirty percent. Split honestly, that might actually be eight percent genuinely earned from real trading activity, and twenty-two percent paid out purely in emissions, newly printed tokens. Same headline number. Very different durability underneath it.",
   chapter="The 60-second version", title="A hypothetical 30% APY, split honestly (illustrative only)",
   stats=[["30%", "Headline APY shown on the dashboard"], ["8%", "Organic — real trading activity"], ["22%", "Emissions — newly printed tokens"]])
sc("statement", "Worth naming the actual habit this hypothetical builds, since you'll use it constantly from here on. Whenever a headline number looks unusually attractive compared to similar products elsewhere, that gap is almost always emissions, not some newly discovered source of free money. The honest question is never simply how big the number is; it's how much of it survives once the printing eventually slows down.",
   chapter="The 60-second version", kicker="The habit this builds", lines=["An unusually attractive number is almost always emissions.", "The question is how much survives once the printing slows."], sub="Not free money. A subsidy, with an expiry you can't see yet.")
sc("chart", "And here's the shape those two components tend to take over time, again purely illustrative, not a prediction about any real protocol. The organic portion tends to stay roughly flat, since it's tied to steady, ongoing activity. The emissions portion tends to decay, month after month, as more of the reward token gets printed, sold, and its price falls. Six months in, the headline number has usually fallen a long way, almost entirely because the emissions portion did.",
   chapter="The 60-second version", title="APY over time: organic vs emissions (illustrative)", kind="line",
   xlabels=["Mo 0", "Mo 1", "Mo 2", "Mo 3", "Mo 4", "Mo 5"], ymin=0, ymax=32,
   yticks=[[0, "0%"], [15, "15%"], [30, "30%"]],
   series=[{"values": [8, 8, 8, 8, 8, 8], "tone": "good", "label": "Organic"}, {"values": [22, 15, 10, 6, 4, 3], "tone": "bad", "label": "Emissions"}],
   marks=[{"i": 0, "text": "30% headline", "tone": "warn"}, {"i": 5, "text": "11% headline", "tone": "good", "below": True}])

# ---------------------------------------------------------------- words you'll need
sc("title", "Now, the five words you'll need.", chapter="Words you'll need", eyebrow="Words you'll need", num="5", title="Five words, drawn out",
   sub="APY · Emissions · Staking · LST · RWA")
sc("flow", "Word one: A.P.Y., annual percentage yield. Here's what actually goes into that single number. It starts with your base rate of return. It adds the effect of compounding, meaning reinvesting what you've already earned so far. And the result is a yearly rate that already assumes you keep reinvesting the whole way through, not just a simple, one-time percentage.",
   chapter="Words you'll need", title="What's actually inside an APY",
   nodes=[{"label": "A base rate of return", "sub": "The underlying, uncompounded yield", "icon": "chart"}, {"label": "+ Compounding", "sub": "Reinvesting what you've already earned", "icon": "coins"},
          {"label": "= APY", "sub": "A yearly rate that assumes full reinvestment", "icon": "check"}])
sc("statement", "Word two: emissions. New reward tokens, printed directly by a protocol, and handed out to whoever deposits, specifically to attract deposits it wants right now. Emissions aren't necessarily a red flag on their own; plenty of protocols use them deliberately, to bootstrap early liquidity. But they're a cost the protocol is choosing to pay, in its own token, and that token's price very often falls as more of it gets printed and sold.",
   chapter="Words you'll need", kicker="Word two: emissions", lines=["New tokens, printed and handed out to attract deposits.", "A real cost, paid in a token whose price often falls as it's printed."], sub="Not automatically bad. But always worth pricing honestly.")
sc("flow", "Word three: staking. Here's the actual sequence behind this one. You lock up tokens, specifically to help secure a network, most often a blockchain's own validator set. The network relies on that locked value to make attacking or corrupting it economically unattractive. And in exchange for taking on that role, and its risks, you're paid a yield, funded by the network itself.",
   chapter="Words you'll need", title="What staking actually does",
   nodes=[{"label": "Lock up tokens", "sub": "To help secure a network", "icon": "lock"}, {"label": "The network relies on that value", "sub": "Makes attacking it economically unattractive", "icon": "shield"},
          {"label": "You're paid for the role", "sub": "Yield funded by the network itself", "icon": "coins"}])
sc("statement", "Word four: L.S.T., a liquid staking token. When you stake through many modern platforms, instead of your original tokens simply disappearing into a locked, illiquid position, you receive an L.S.T. back: a separate token representing your staked position, which you can still trade, move, or use elsewhere in DeFi, all while your underlying stake keeps earning its own separate yield.",
   chapter="Words you'll need", kicker="Word four: LST", lines=["A token representing your staked position.", "Still tradeable and usable, while the underlying stake keeps earning."], sub="Liquidity and staking yield, at the same time, instead of choosing one.")
sc("statement", "Word five: R.W.A., a real-world asset. A token representing something that exists entirely outside crypto, most commonly a short-term government treasury bill, but sometimes real estate, private credit, or other traditional financial instruments. R.W.A. yield is attractive specifically because it's tied to real-world interest rates, largely independent of whatever's happening in crypto markets that particular week.",
   chapter="Words you'll need", kicker="Word five: RWA", lines=["A token representing something outside crypto entirely.", "Often a short-term treasury bill, tied to real-world rates."], sub="A yield source that mostly doesn't care what crypto is doing this week.")
sc("quiz", "Quick check. What does an L.S.T. actually let you do that plain staking, on its own, doesn't? [[pause 4]] The answer: it lets you keep trading, moving, or using your staked position elsewhere in DeFi, while the underlying stake keeps earning its own yield.",
   chapter="Words you'll need", n=1, of=3, q="What does an LST let you do that plain staking doesn't?",
   a="Trade, move, or use your staked position elsewhere in DeFi, while it keeps earning yield.")
sc("compare", "Here's L.S.T. and R.W.A. side by side, since they're easy to blur together, but come from genuinely different worlds. An L.S.T. represents a position staked inside crypto itself, earning yield the network pays for security. An R.W.A. represents something entirely outside crypto, most often earning yield tied to real-world interest rates. Both hand you a token you can trade or use elsewhere; what backs that token, and what risk it's actually exposed to, is completely different.",
   chapter="Words you'll need",
   left={"label": "LST", "tone": "good", "items": ["Represents a staked position, inside crypto", "Yield paid by the network, for security"]},
   right={"label": "RWA", "tone": "good", "items": ["Represents something outside crypto entirely", "Yield often tied to real-world interest rates"]})
sc("quiz", "Quick check. What's the actual difference between organic yield and emissions? [[pause 4]] The answer: organic yield comes from real economic activity, like trading fees or borrower interest. Emissions are new tokens a protocol prints and hands out, specifically to attract deposits.",
   chapter="Words you'll need", n=2, of=3, q="What's the difference between organic yield and emissions?",
   a="Organic yield comes from real activity (fees, interest); emissions are newly printed tokens handed out to attract deposits.")

# ---------------------------------------------------------------- before you start
sc("title", "Before you start.", chapter="Before you start", eyebrow="Before you start", num="1", title="What this module assumes you already have",
   sub="Modules zero through three.")
sc("steps", "Here's what this module assumes you're already comfortable with, before diving in. Everything from Module zero: wallets, networks, and gas. Module one's due-diligence habits, for checking any protocol before touching it. Module two's read on A.M.M.s, liquidity, and MEV. And Module three's lending and leverage concepts, since several yield sources in this module build directly on borrowing and collateral.",
   chapter="Before you start", title="What you should already have",
   steps=["Module 0: wallets, networks, gas", "Module 1: due-diligence habits", "Module 2: AMMs, liquidity, MEV", "Module 3: lending and leverage concepts"], result="If any of these feel shaky, that module is worth a quick revisit first")

# ---------------------------------------------------------------- your first safe step
sc("title", "Your first safe step.", chapter="Your first safe step", eyebrow="Your first safe step", num="1", title="Split one real APY into its parts",
   sub="Using the protocol's own dashboard. No new money required.")
sc("steps", "Here's exactly what to do, before this module goes any deeper into specific yield sources. Pick any protocol currently advertising a yield you've noticed. Open its own dashboard, and find the breakdown it actually publishes, most protocols do show this somewhere. Separate what it calls base yield from what it calls incentives or emissions. And write down, in your own words, what each part is actually payment for.",
   chapter="Your first safe step", title="Splitting a real APY",
   steps=["Pick a protocol advertising a yield you've noticed", "Open its dashboard and find the published breakdown", "Separate base yield from incentives/emissions", "Write down what each part is actually payment for"], result="No new money required. Just genuine, first-hand reading practice")
sc("statement", "Worth doing this exercise on a real number, not a hypothetical one, since the entire skill this module builds is reading real dashboards under real conditions. A yield that turns out to be almost entirely emissions isn't automatically a scam; it's simply telling you honestly what you'd actually be exposed to, and for how long that exposure is likely to last.",
   chapter="Your first safe step", kicker="Why a real number, not a hypothetical", lines=["The skill is reading real dashboards under real conditions.", "Mostly-emissions isn't automatically a scam — it's honest information."], sub="Read it. Don't just accept the headline number.")
sc("steps", "And here's what to do specifically if a protocol doesn't publish a clean breakdown at all, since not all of them do. Check the reward token's own emission schedule, most protocols document how many new tokens get released, and how often. Compare deposit growth against that emission schedule; deposits rising in step with new token releases is a strong signal you're looking at incentive-driven growth. And if you genuinely can't tell, treat the entire yield as if it were emissions, until you can.",
   chapter="Your first safe step", title="If the breakdown isn't published",
   steps=["Check the reward token's own emission schedule", "Compare deposit growth against that schedule", "Deposits tracking emissions = incentive-driven growth", "Can't tell? Treat the whole yield as emissions until you can"])

# ---------------------------------------------------------------- the mastery ladder
sc("title", "The mastery ladder.", chapter="The mastery ladder", eyebrow="The mastery ladder", num="1", title="Three levels, each building on the last",
   sub="Know exactly where you are, and what's next.")
sc("compare", "Here's the first two rungs on this module's ladder, side by side, so you can see exactly what separates them. At the beginner level, you can tell base yield apart from emissions on any given yield, the core skill this whole module starts with. At the practitioner level, you go further: comparing a managed vault against doing the same strategy yourself, and correctly pricing points programs or airdrop farming as the bets they actually are.",
   chapter="The mastery ladder",
   left={"label": "Beginner", "tone": "warn", "items": ["Tells base yield apart from emissions", "The core skill this module starts with"]},
   right={"label": "Practitioner", "tone": "good", "items": ["Compares vaults vs doing it yourself", "Prices points/airdrop farming as bets"]})
sc("flow", "Here's what the practitioner level actually looks like in practice, one level up from just telling base yield apart from emissions. First, you compare a managed vault's advertised yield against running that same underlying strategy yourself directly, factoring in the vault's own fee. Then, when a protocol offers points, or hints at a future airdrop, you price that specifically as a bet with real odds, not as guaranteed extra yield stacked on top.",
   chapter="The mastery ladder", title="Practitioner level, in practice",
   nodes=[{"label": "A managed vault's advertised yield", "sub": "Compared against doing it yourself", "icon": "chart"}, {"label": "− The vault's own fee", "sub": "What running it yourself would actually net", "icon": "coins"},
          {"label": "Points/airdrops priced as bets", "sub": "Real odds, not guaranteed extra yield", "icon": "target"}])
sc("statement", "And here's the top rung, master level, the one this module ultimately builds toward. At that level, you can construct yield deliberately from durable, well-understood sources: lending markets, staking, savings rates, and tokenised treasuries, choosing each source specifically because you understand exactly what risk it's paying you for, not just because the number looked attractive.",
   chapter="The mastery ladder", kicker="Master level", lines=["Builds yield from durable, well-understood sources.", "Chosen because you understand the risk, not just the number."], sub="Lending, staking, savings rates, tokenized treasuries.")
sc("statement", "Here's how you'll actually know you've mastered this entire module, in one sentence. You can look at any yield, anywhere, and name both its source and the specific risk being paid for, without needing to check a dashboard breakdown first, because you already recognise the pattern.",
   chapter="The mastery ladder", kicker="You've mastered this module when…", lines=["You can name the source and the risk behind any yield.", "In one sentence, without checking a breakdown first."], sub="That's the actual finish line for this module.")
sc("quiz", "Quick check. What does the master level of this module's ladder actually require? [[pause 4]] The answer: building yield deliberately from durable sources, like lending, staking, savings rates, and tokenised treasuries, chosen for their understood risk, not just their advertised number.",
   chapter="The mastery ladder", n=3, of=3, q="What does the master level of this module's ladder require?",
   a="Building yield from durable sources (lending, staking, savings rates, tokenized treasuries), chosen for their understood risk.")

# ---------------------------------------------------------------- recap
sc("bullets", "Let's recap. Every yield is payment for something specific, organic activity or printed emissions. The five words: A.P.Y., emissions, staking, L.S.T., and R.W.A. Your first safe step is splitting one real, advertised A.P.Y. into its actual parts, using the protocol's own numbers. And you'll know you've mastered this module when you can name the source and the risk behind any yield, in one sentence, on sight.",
   chapter="Recap", title="Recap", check=False,
   items=["Every yield is payment for something specific", "Five words: APY, emissions, staking, LST, RWA",
          "First step: split a real APY into base yield vs emissions", "Mastered when: name the source and risk behind any yield, on sight"])
sc("cta", "Pick one real, advertised A.P.Y. today, and split it into its actual parts using the protocol's own dashboard. Next up, Lesson four point one: yield farming, base yield versus emissions.",
   "Pick one real, advertised APY today, and split it into its actual parts using the protocol's own dashboard. Next up, Lesson 4.1: yield farming, base yield vs emissions.",
   chapter="Recap", button="Next: Lesson 4.1", sub="Yield farming: base yield vs emissions")

spec = {"id": "lesson-04-0", "title": "Lesson 4.0: Mastery Starter — Yield", "size": [1920, 1080], "group": "lessons", "maxMinutes": 25,
        "tag": "Lesson 4.0 · Mastery Starter", "gold": True, "music": True, "musicLevel": 0.14, "seed": 69,
        "use": "Lesson 4.0 page in the Whop course. Hand-written gold-standard Mastery Starter script for Module 4: the 60-second version, the module's five words, before-you-start, first safe step, and mastery ladder, as walk-throughs.",
        "thumbnail": {"title": "Yield: Mastery Starter", "subtitle": "Lesson 4.0"}, "scenes": S}
out = ROOT / "video-scripts" / "gold" / "lesson-04-0.json"
out.write_text(json.dumps(spec, indent=1, ensure_ascii=False))
words = sum(len(s["vo"].replace("[[pause 4]]", "").split()) for s in S)
print(f"{len(S)} scenes, {words} words, est {(words / 171 * 60 + len(S) * 1.3 + 4 * 3) / 60:.1f} min")
