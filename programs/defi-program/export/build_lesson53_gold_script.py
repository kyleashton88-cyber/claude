#!/usr/bin/env python3
"""Gold-standard script for Lesson 5.3, Oracles, TWAPs & manipulation
(target 11-14 minutes, per the "a bit longer" note for lessons from here
on). Walks why contracts need oracles, push vs pull oracles, what a TWAP
actually trades off, oracle failure modes, and the source material's own
worked example (a 30-minute TWAP with the market down 10% in 5 minutes:
screen shows -10%, the oracle shows maybe -2%, and you can't rely on the
lag lasting — it catches up; conversely a thin-market token can be pushed
up and borrowed against), as visual walk-throughs. Written in one pass at
the full target length (no separate expansion round).

Writes video-scripts/gold/lesson-05-3.json (the generator skips lessons
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
sc("title", "Lesson five point three. Oracles, T.W.A.P.s, and manipulation. By the end, you'll know exactly which price feed actually secures each of your positions, and precisely how each one can fail.",
   "Lesson 5.3. Oracles, TWAPs & manipulation. By the end, you'll know exactly which price feed actually secures each of your positions, and precisely how each one can fail.",
   chapter="Intro", eyebrow="Lesson 5.3", num="5.3", title="Oracles, TWAPs & manipulation", sub="The oracle price liquidates you. Not the price on your screen.")
sc("pillars", "Here's the plan. Push versus pull oracles, the two genuinely different ways a price actually gets into a contract. What a T.W.A.P. actually trades off, and exactly why it lags. The specific ways an oracle can fail: stale prices, thin-market manipulation, and misconfiguration. And a full worked example, using the source material's own thirty-minute T.W.A.P. scenario.",
   chapter="Intro", title="What this lesson covers",
   items=[{"icon": "chart", "title": "Push vs. pull", "text": "Two genuinely different ways a price gets in"}, {"icon": "clock", "title": "The TWAP trade-off", "text": "Harder to manipulate, but it lags fast moves"},
          {"icon": "alert", "title": "Three failure modes", "text": "Stale prices, thin-market manipulation, misconfiguration"}, {"icon": "target", "title": "Worked example", "text": "Screen: -10%. Oracle: maybe -2%. Why that gap matters"}])

# ---------------------------------------------------------------- push vs pull oracles
sc("title", "Why contracts need an oracle at all.", chapter="Push vs pull oracles", eyebrow="Push vs pull oracles", num="1", title="Push vs. pull, two genuinely different ways in",
   sub="Your liquidation runs on the oracle price. Never the price on your screen.")
img(D + "oracle-twap.png", "How a price actually gets into a contract",
    "Here's the one fact this entire lesson builds from. A smart contract genuinely cannot see market prices on its own; an oracle is what brings that price in from the outside. And critically, a lending market liquidates you based specifically on that oracle's own price, not whatever number happens to be showing on your own screen, or on any exchange you personally happen to be watching at that exact moment.",
    chapter="Push vs pull oracles")
sc("compare", "Here's the actual difference between the two ways that price gets delivered. A push oracle has a network updating prices on its own schedule, or specifically whenever price moves past a set deviation threshold, whichever comes first. A pull oracle instead fetches, and cryptographically verifies, a price only at the exact moment a transaction actually needs it, rather than continuously updating in the background.",
   chapter="Push vs pull oracles",
   left={"label": "Push oracles", "tone": "good", "items": ["Updates on a schedule, or past a deviation threshold", "Continuously running in the background"]},
   right={"label": "Pull oracles", "tone": "good", "items": ["Fetched and verified only when a transaction needs it", "No continuous background updates"]})
sc("quiz", "Quick check. Which price actually triggers a DeFi liquidation? [[pause 4]] The answer: the oracle price the protocol itself uses, never the price you happen to be watching on your own screen.",
   chapter="Push vs pull oracles", n=1, of=3, q="Which price triggers a DeFi liquidation?",
   a="The oracle price used by the protocol.")

# ---------------------------------------------------------------- the twap trade-off
sc("title", "What a TWAP actually trades off.", chapter="The TWAP trade-off", eyebrow="The TWAP trade-off", num="1", title="Harder to manipulate. But it lags.",
   sub="Time-weighted average price, smoothed on purpose.")
sc("flow", "Here's exactly what a T.W.A.P., a time-weighted average price, is actually doing, and why it's deliberately built this way. Instead of reading one single, instantaneous price, it averages price out across a real window of time, say thirty minutes. That averaging is precisely what makes it genuinely harder to manipulate with one quick, isolated trade. But that exact same averaging is also what makes it lag behind a real, fast market move, on purpose.",
   chapter="The TWAP trade-off", title="Why a TWAP is built this way",
   nodes=[{"label": "Averages price over a real window", "sub": "Say, thirty minutes, not one instant", "icon": "clock"}, {"label": "Harder to manipulate", "sub": "One quick, isolated trade barely moves the average", "icon": "shield"},
          {"label": "But it lags real, fast moves", "sub": "By design. That's the actual trade-off", "icon": "alert"}])
sc("statement", "Worth being precise about why this specific trade-off exists at all, rather than simply reading the current spot price directly. A spot price can be manipulated in a single block, by one large, isolated trade, especially in a thin market. A T.W.A.P. makes that same manipulation require sustaining an artificial price across the entire averaging window, which is genuinely far more expensive to actually pull off.",
   chapter="The TWAP trade-off", kicker="Why this trade-off exists", lines=["A spot price can be manipulated in a single block.", "A TWAP requires sustaining that manipulation across the whole window."], sub="Harder to manipulate is the whole point. The lag is the cost of that.")
sc("quiz", "Quick check. What's the actual trade-off of using a T.W.A.P.? [[pause 4]] The answer: it's genuinely harder to manipulate than a spot price, but it lags behind fast, real market moves, by design.",
   chapter="The TWAP trade-off", n=2, of=3, q="What's the trade-off of a TWAP?",
   a="Harder to manipulate, but it lags fast moves.")

# ---------------------------------------------------------------- three failure modes
sc("title", "Three ways an oracle can fail.", chapter="Three failure modes", eyebrow="Three failure modes", num="3", title="Stale prices · Thin-market manipulation · Misconfiguration",
   sub="Each one is a genuinely different mechanism.")
sc("flow", "Here's each of these three, and exactly how each one actually happens. Stale prices happen specifically during an outage, when the feed simply stops updating, but the last known price is still what the contract keeps using. Thin-market manipulation happens when an attacker moves a low-liquidity asset's price artificially, specifically because it doesn't take much capital to move a thin market meaningfully. And misconfigured feeds happen when a protocol simply points at the wrong oracle, or the wrong specific parameters, entirely by human error.",
   chapter="Three failure modes", title="How each failure actually happens",
   nodes=[{"label": "Stale prices", "sub": "An outage stops updates; the last price keeps being used", "icon": "clock"}, {"label": "Thin-market manipulation", "sub": "Low liquidity means less capital needed to move it", "icon": "alert"},
          {"label": "Misconfigured feeds", "sub": "Pointed at the wrong oracle, or wrong parameters", "icon": "target"}])
sc("statement", "Worth being precise about why thin-market manipulation specifically threatens lenders, not just the manipulator themselves. An attacker can artificially push up a thinly traded token's price, deposit it as collateral at that inflated price, and borrow far more than the token is actually, genuinely worth, leaving the lending protocol holding collateral worth a fraction of the debt it's meant to cover.",
   chapter="Three failure modes", kicker="Why this specifically threatens lenders", lines=["Push the price up, deposit as collateral, borrow against the inflated value.", "The protocol is left holding collateral worth a fraction of the debt."], sub="This is exactly why thin-market collateral gets treated so cautiously.")
sc("statement", "Worth being precise about the actual danger inside a stale price specifically, since it's the quietest of these three failures, right up until it isn't. During an outage, the contract keeps using the last price it ever received, treating it as current, with no warning built in that anything's actually wrong. A real market move happening during exactly that outage simply isn't reflected anywhere, until the feed eventually recovers.",
   chapter="Three failure modes", kicker="The quiet danger in a stale price", lines=["The contract keeps using the last price, with no warning.", "A real move during the outage isn't reflected anywhere, until it recovers."], sub="The quietest of the three failures, right up until it isn't.")
sc("quiz", "Quick check. Why is thin-market collateral specifically dangerous for lenders? [[pause 4]] The answer: its price can be artificially manipulated, letting someone borrow far more against it than it's actually, genuinely worth.",
   chapter="Three failure modes", n=3, of=3, q="Why is thin-market collateral dangerous for lenders?",
   a="Its price can be manipulated to borrow more than it's really worth.")

# ---------------------------------------------------------------- worked example
sc("title", "Worked example.", chapter="Worked example", eyebrow="Worked example", num="1", title="Screen: -10%. Oracle: maybe -2%.",
   sub="The source material's own scenario.")
sc("steps", "Here's the scenario, exactly as the source material lays it out. Your collateral is priced by a thirty-minute T.W.A.P. The market itself drops ten percent, in just five minutes, a genuinely fast move. Your own screen shows that full ten percent drop, immediately. The oracle, still averaging across its thirty-minute window, might show something closer to just two percent, at that same exact moment.",
   chapter="Worked example", title="The setup",
   steps=["Collateral priced by a 30-minute TWAP", "Market drops 10% in 5 minutes", "Your screen: -10%, immediately", "The oracle, mid-average: maybe -2%, at that same moment"], result="A real, temporary gap between what you see and what actually triggers liquidation")
sc("statement", "Worth being precise about the actual trap hiding inside this exact gap, since it cuts in both directions at once. You might genuinely feel liquidated, watching that ten percent drop on your own screen, when the oracle hasn't caught up yet, and you technically aren't. But you also can't rely on that same lag lasting: the T.W.A.P. keeps averaging, and it does eventually catch up to the real move, whether you've prepared for that or not.",
   chapter="Worked example", kicker="The trap hiding inside the gap", lines=["You might feel liquidated when you technically aren't yet.", "But the lag doesn't last. The TWAP catches up, whether you're ready or not."], sub="Neither side of this gap is a safe place to plan around.")
sc("title", "Watching the oracle actually catch up.", chapter="Worked example", eyebrow="Worked example", num="2", title="The same drop, over the full 30-minute window",
   sub="A simplified, illustrative model of how a rolling TWAP converges.")
sc("chart", "Here's what that catch-up actually looks like, plotted across the full thirty-minute window, in a simplified, illustrative model of how a rolling average genuinely converges. Right after the drop, at five minutes, the oracle's showing roughly negative two percent, matching the source material's own figure closely. By fifteen minutes, about negative five. And by the full thirty minutes, it's essentially caught all the way up to the real negative ten percent move.",
   chapter="Worked example", title="TWAP catch-up after a step change (illustrative)", kind="line",
   xlabels=["5 min", "10 min", "15 min", "20 min", "25 min", "30 min"], ymin=-11, ymax=1,
   yticks=[[0, "0%"], [-5, "−5%"], [-10, "−10%"]],
   series=[{"values": [-1.67, -3.33, -5, -6.67, -8.33, -10], "tone": "warn", "label": "Oracle (TWAP)"}],
   marks=[{"i": 0, "text": "≈ −2% (matches the worked example)", "tone": "good"}, {"i": 5, "text": "−10%, fully caught up", "tone": "bad", "below": True}])
sc("statement", "Notice that the oracle line never stops moving toward the real price; it just takes real time to get there. That's the entire lag, laid out visually: not a permanent gap, and not a loophole, just a delay that closes steadily, the whole way from the moment the real move happened.",
   chapter="Worked example", kicker="What the chart actually shows", lines=["The oracle line never stops moving toward the real price.", "Not a permanent gap. A delay that closes steadily."], sub="Plan for where that line is headed, not just where it is right now.")
sc("steps", "Here's how to actually find this out for a protocol you use, rather than assuming. Check its documentation specifically for which oracle it uses, and whether that oracle is push or pull. Find the actual TWAP window length, if one is used, in real minutes. And check whether that window is published clearly, or whether you'd have to dig through the contract itself to find it.",
   chapter="Worked example", title="Finding your own protocol's actual setup",
   steps=["Check documentation for which oracle, push or pull", "Find the actual TWAP window length, in real minutes", "Published clearly, or buried in the contract itself?"])
sc("compare", "Here's the exact same lag mechanism, but working in the opposite direction, against a thinly traded collateral token instead. An attacker pushes that token's price up artificially, on a thin market. If the protocol's oracle hasn't caught up yet, or if its window is short enough to reflect that push quickly, the attacker can deposit at the inflated price and borrow well beyond what the token is actually worth.",
   chapter="Worked example",
   left={"label": "You, holding real collateral", "tone": "warn", "items": ["The lag can make you feel liquidated early", "But it also doesn't protect you once it catches up"]},
   right={"label": "An attacker, thin-market collateral", "tone": "bad", "items": ["Pushes the price up artificially", "Borrows against the inflated value before it corrects"]})
sc("statement", "Here's the one sentence this entire worked example exists to prove, worth holding onto more than the specific ten-percent and two-percent figures. Size your own buffers for the oracle's catch-up, never for the lag lasting forever, since a T.W.A.P. smooths manipulation, it doesn't erase the real move underneath it.",
   chapter="Worked example", kicker="The one sentence to keep", lines=["Size your buffers for the catch-up, never for the lag lasting.", "A TWAP smooths manipulation. It doesn't erase the real move."], sub="The lag is temporary, by design. Plan as if it will close.")

# ---------------------------------------------------------------- checklist and recap
sc("steps", "Here's your checklist. Do it for every collateral type you actually use. Know the oracle type and its actual source, for each one, not just that an oracle exists at all. Avoid, or deliberately cap, thin-market collateral specifically. And size your own buffers assuming the oracle genuinely catches up, never assuming its lag will simply protect you indefinitely.",
   chapter="Checklist", title="Your checklist",
   steps=["Oracle type and source known for each collateral", "Thin-market collateral avoided or capped", "Buffers sized for oracle catch-up"])
sc("bullets", "Let's recap. A contract can't see market prices; an oracle brings them in, and it's the oracle price, not your screen, that actually triggers liquidation. Push oracles update on a schedule or threshold; pull oracles fetch and verify on demand. A T.W.A.P. is harder to manipulate, but lags fast moves, on purpose. Oracles fail through stale prices, thin-market manipulation, and misconfiguration. And the real rule: size your buffers for the catch-up, never for the lag lasting.",
   chapter="Recap", title="Recap", check=False,
   items=["The oracle price triggers liquidation — never the price on your screen", "Push: scheduled/threshold updates. Pull: fetched on demand",
          "A TWAP is harder to manipulate, but lags fast moves by design", "Size buffers for the oracle's catch-up, never for the lag lasting"])
sc("statement", "Worth connecting this back to the dependency map from this module's own Mastery Starter, one more time. The oracle pricing your collateral is another specific link in that same chain, and now you know exactly what to check on it: push or pull, its TWAP window if it has one, and how thin the market behind whatever it's pricing actually is.",
   chapter="Recap", kicker="Connecting back to the dependency map", lines=["The oracle is another specific link in that same chain.", "Now you know exactly what to check on it."], sub="Three links mapped so far. More still to come in this module.")
sc("cta", "Know each collateral's oracle type and source, cap thin-market exposure, and size buffers for the catch-up, not the lag. Next up, Lesson five point four: smart contracts, state, proxies, and admin keys.",
   "Know each collateral's oracle type and source, cap thin-market exposure, and size buffers for the catch-up, not the lag. Next up, Lesson 5.4: smart contracts, state, proxies, admin keys.",
   chapter="Recap", button="Next: Lesson 5.4", sub="Smart contracts: state, proxies, admin keys")

spec = {"id": "lesson-05-3", "title": "Lesson 5.3: Oracles, TWAPs & manipulation", "size": [1920, 1080], "group": "lessons", "maxMinutes": 25,
        "tag": "Lesson 5.3", "gold": True, "music": True, "musicLevel": 0.14, "seed": 81,
        "use": "Lesson 5.3 page in the Whop course. Hand-written gold-standard script: push vs pull oracles, what a TWAP trades off, the three oracle failure modes, and the source material's own 30-minute-TWAP worked example, as walk-throughs.",
        "thumbnail": {"title": "Oracles, TWAPs & manipulation", "subtitle": "Lesson 5.3"}, "scenes": S}
out = ROOT / "video-scripts" / "gold" / "lesson-05-3.json"
out.write_text(json.dumps(spec, indent=1, ensure_ascii=False))
words = sum(len(s["vo"].replace("[[pause 4]]", "").split()) for s in S)
print(f"{len(S)} scenes, {words} words, est {(words / 171 * 60 + len(S) * 1.3 + 4 * 3) / 60:.1f} min")
