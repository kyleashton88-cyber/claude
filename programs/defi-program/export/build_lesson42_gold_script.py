#!/usr/bin/env python3
"""Gold-standard script for Lesson 4.2, Native staking (target 11-14
minutes, per the "a bit longer" note for lessons from here on). Walks what
staking rewards actually pay for, running a validator vs delegating,
slashing/unbonding/downtime risk, and the source material's own worked
example (staking ~3% on an asset that falls 30% is still a large loss:
1.03 x 0.70 - 1 ≈ -27.9%; stake what you'd hold anyway), as visual
walk-throughs. Written in one pass at the full target length (no separate
expansion round).

Writes video-scripts/gold/lesson-04-2.json (the generator skips lessons
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
sc("title", "Lesson four point two. Native staking. By the end, you'll understand exactly what staking rewards pay for, the real risks underneath them, and why staking is never a defence against a falling price.",
   "Lesson 4.2. Native staking. By the end, you'll understand exactly what staking rewards pay for, the real risks underneath them, and why staking is never a defence against a falling price.",
   chapter="Intro", eyebrow="Lesson 4.2", num="4.2", title="Native staking", sub="Stake what you'd hold anyway. Nothing more.")
sc("pillars", "Here's the plan. What staking rewards actually pay for, and the two ways you can participate. The real risks underneath a staking yield: slashing, unbonding, and validator downtime. A worked example showing exactly why staking is never protection against a falling price. And a checklist for choosing who to stake with, and how much.",
   chapter="Intro", title="What this lesson covers",
   items=[{"icon": "shield", "title": "What staking pays for", "text": "Securing the chain, run it yourself or delegate"}, {"icon": "alert", "title": "The real risks", "text": "Slashing, unbonding periods, validator downtime"},
          {"icon": "chart", "title": "Worked example", "text": "Why +3% staking doesn't save you from -30% price"}, {"icon": "target", "title": "Checklist", "text": "Choosing a validator, and how much to stake"}])

# ---------------------------------------------------------------- what staking pays for
sc("title", "What staking rewards actually pay for.", chapter="What staking pays for", eyebrow="What staking pays for", num="1", title="Securing the chain, not just holding a token",
   sub="Run a validator yourself, or delegate to one.")
img(D + "native-staking.png", "How native staking actually works",
    "Here's the mechanism underneath every proof-of-stake network. Stakers lock up the network's own asset, specifically to help secure the chain, by running software that proposes and validates new blocks. In return, the network pays stakers rewards, funded by a mix of new issuance and transaction fees. You can participate in exactly one of two ways: run a validator yourself, directly, or delegate your stake to someone else who already runs one.",
    chapter="What staking pays for")
sc("compare", "Here's the actual choice between those two ways to participate, side by side. Running your own validator means keeping the full reward for yourself, but it requires real technical setup, reliable uptime, and genuine ongoing responsibility. Delegating to someone else's validator is far simpler to start, but that validator takes a cut of the reward, and your outcome now depends partly on how well they run their own operation.",
   chapter="What staking pays for",
   left={"label": "Run your own validator", "tone": "good", "items": ["Keep the full reward", "Requires real setup, uptime, responsibility"]},
   right={"label": "Delegate to a validator", "tone": "warn", "items": ["Simple to start", "A fee is taken; depends on their operation"]})
sc("statement", "Worth being precise about why the network pays for this at all, since it's easy to just treat the yield as a given. Proof-of-stake networks need a large amount of value genuinely at risk, specifically to make attacking or corrupting the chain economically unattractive. Staking rewards are the network's direct payment for taking on that role, and the risk that comes with it, not a reward for simply holding the token.",
   chapter="What staking pays for", kicker="Why the network pays for this", lines=["It needs real value at risk, to deter attacks.", "The reward pays for taking on that role — not for holding."], sub="This is the actual source of every staking yield in this lesson.")
sc("compare", "Here's where that reward actually comes from, since the source matters for who ultimately bears its cost. Issuance means the network mints brand-new tokens specifically to pay stakers, which mildly dilutes everyone who isn't staking. Fees mean the reward comes from transaction fees actual users already paid, redistributed to whoever's securing the chain, with no dilution involved at all. Most networks blend both, in varying proportions.",
   chapter="What staking pays for",
   left={"label": "Issuance", "tone": "warn", "items": ["New tokens minted to pay stakers", "Mildly dilutes everyone not staking"]},
   right={"label": "Fees", "tone": "good", "items": ["Redistributed from fees users already paid", "No dilution involved"]})
sc("quiz", "Quick check. What do staking rewards actually pay for? [[pause 4]] The answer: securing the network, specifically by putting real value at risk to make attacking or corrupting the chain economically unattractive.",
   chapter="What staking pays for", n=1, of=3, q="What do staking rewards pay for?",
   a="Securing the network.")

# ---------------------------------------------------------------- the real risks
sc("title", "The real risks underneath the yield.", chapter="The real risks", eyebrow="The real risks", num="1", title="Slashing · Unbonding · Downtime",
   sub="None of these show up in the headline APY number.")
sc("flow", "Here's all three risks, and what each one actually does to you. Slashing is a direct penalty, on some networks, for validator misbehaviour, like double-signing or extended downtime, and it can cut directly into the staked principal itself, not just the reward. An unbonding period is a mandatory waiting time between requesting to withdraw and actually receiving your assets back, during which the market can move freely against you. And validator downtime simply means missed rewards, for however long that validator stays offline.",
   chapter="The real risks", title="Three risks, three different mechanisms",
   nodes=[{"label": "Slashing", "sub": "A direct penalty on some networks, for misbehaviour", "icon": "alert"}, {"label": "Unbonding period", "sub": "A mandatory wait before withdrawal completes", "icon": "clock"},
          {"label": "Validator downtime", "sub": "Missed rewards while the validator is offline", "icon": "chart"}])
sc("statement", "Worth being precise about the unbonding period specifically, since it's the risk most likely to catch someone off guard. It isn't a fee, and it isn't optional; it's simply time you cannot access your assets, whatever the market happens to do during that exact window. On some networks that's days; on others, considerably longer. Know the actual number before you stake, not after you try to withdraw.",
   chapter="The real risks", kicker="Why unbonding catches people off guard", lines=["Not a fee. Just time you can't access your assets.", "The market keeps moving, whether you can react or not."], sub="Know the actual number before you stake, not after you try to leave.")
sc("compare", "Here's why delegating specifically changes your exposure to these risks, compared with running a validator yourself. Delegating to a validator with a strong uptime record and no history of slashing meaningfully lowers your practical exposure to both of the first two risks. Delegating to an unproven or poorly run validator can expose you to the exact same slashing and downtime risk as running one badly yourself, without you having any direct control over the outcome.",
   chapter="The real risks",
   left={"label": "A proven, high-uptime validator", "tone": "good", "items": ["Lower practical slashing and downtime exposure", "A track record you can actually check"]},
   right={"label": "An unproven, poorly-run validator", "tone": "bad", "items": ["Same risk as running one badly yourself", "But with no direct control over the outcome"]})
sc("steps", "Here's how to actually plan around an unbonding period, rather than being caught by it. Know the exact number of days before you ever stake, not when you suddenly need the funds. Start the withdrawal well ahead of whenever you actually expect to need that liquidity, treating the unbonding period as a hard floor, not a rough guess. And never stake capital you might need on short notice, since no urgency on your end changes how long the network's own waiting period actually is.",
   chapter="The real risks", title="Planning around unbonding",
   steps=["Know the exact number of days before you stake", "Start withdrawal well ahead of when you'll need the funds", "Never stake capital you might need on short notice"])
sc("quiz", "Quick check. What exactly is unbonding? [[pause 4]] The answer: a mandatory waiting period, after requesting a withdrawal, before your unstaked assets actually become transferable again.",
   chapter="The real risks", n=2, of=3, q="What is unbonding?",
   a="A waiting period before unstaked assets become transferable.")

# ---------------------------------------------------------------- worked example
sc("title", "Worked example.", chapter="Worked example", eyebrow="Worked example", num="1", title="Why staking doesn't save you from a falling price",
   sub="The source material's own scenario.")
sc("steps", "Here's the scenario, step by step, using the source material's own realistic, illustrative numbers. You stake an asset, earning roughly three percent a year, paid in that same asset. Over that same year, the asset's own price falls thirty percent. Your staked balance is genuinely larger, by that three percent. But its dollar value has fallen anyway, because the price move overwhelms the staking yield entirely.",
   chapter="Worked example", title="The setup",
   steps=["Stake an asset, earning ~3% a year, in that same asset", "Over the year, the asset's own price falls 30%", "Your balance is 3% bigger, but worth far less in dollars"], result="A large loss, staking yield included")
sc("stats", "Here's the actual dollar math behind that, computed precisely. One point zero three, for the three percent staking gain, multiplied by zero point seven, for the thirty percent price drop, comes to zero point seven two one. That's a loss of about twenty-seven point nine percent, in dollar terms, despite every single staking reward being paid out exactly as promised.",
   chapter="Worked example", title="1.03 × 0.70 − 1 ≈ −27.9%",
   stats=[["+3%", "Staking yield, paid as promised"], ["−30%", "The asset's own price move"], ["−27.9%", "Your actual dollar result"]])
sc("statement", "Here's the one sentence this entire worked example exists to prove, worth holding onto more than any specific percentage. Staking adds a small, genuine yield on top of whatever the asset does anyway; it does not protect you from that asset's price falling. The three percent helped, technically, exactly as advertised. It simply wasn't remotely close to being enough.",
   chapter="Worked example", kicker="The one sentence to keep", lines=["Staking adds yield. It does not protect against price falls.", "The 3% helped. It just wasn't close to enough."], sub="This is true no matter which network, or how attractive the rate.")
sc("title", "The same 3%, across different price moves.", chapter="Worked example", eyebrow="Worked example", num="2", title="The staking yield barely moves the outcome",
   sub="A purely illustrative sensitivity, using that same +3%.")
sc("chart", "Here's that same three percent staking yield, applied across five different price scenarios, from a sharp fall to a solid gain, again purely illustrative. At a fifty percent price fall, you're down about forty-eight and a half percent, staking included. At the thirty percent fall from a moment ago, down twenty-seven point nine. At a ten percent fall, down about seven percent. With the price flat, you're simply up your three percent. And with a thirty percent gain, staking adds a little more on top, to about thirty-four percent.",
   chapter="Worked example", title="Dollar result: +3% staking, across price moves", kind="line",
   xlabels=["−50%", "−30%", "−10%", "0%", "+30%"], ymin=-55, ymax=40,
   yticks=[[-50, "−50%"], [0, "0%"], [30, "30%"]],
   series=[{"values": [-48.5, -27.9, -7.3, 3.0, 33.9], "tone": "warn", "label": "Dollar result"}],
   marks=[{"i": 0, "text": "−48.5%", "tone": "bad"}, {"i": 3, "text": "+3.0%", "tone": "good"}, {"i": 4, "text": "+33.9%", "tone": "good", "below": True}])
sc("statement", "Notice how little that three percent staking yield actually shifts any of these outcomes, compared to the price move itself. It nudges every single result by roughly three percentage points, in the same direction the price was already moving. It never once changes which direction the outcome goes. The price move decides that, on its own, every time.",
   chapter="Worked example", kicker="What the chart actually shows", lines=["The staking yield nudges every outcome by ~3 points.", "It never changes which direction the outcome goes."], sub="The price move decides that, on its own, every time.")
sc("compare", "Here's what this actually implies for deciding what to stake in the first place, since the math above applies to any asset, not just this one example. An asset you'd genuinely hold regardless of its price, for reasons entirely separate from the staking yield, is a reasonable candidate. An asset you're only holding because of the staking rate itself is exposed to exactly the loss the worked example just showed you, the instant that price falls.",
   chapter="Worked example",
   left={"label": "An asset you'd hold anyway", "tone": "good", "items": ["Staking is a genuine bonus on top", "The price risk was already yours regardless"]},
   right={"label": "An asset held only for the yield", "tone": "bad", "items": ["Exposed to the exact loss above", "The instant the price actually falls"]})
sc("quiz", "Quick check. Does staking protect you against the underlying asset's price falling? [[pause 4]] The answer: no. It adds a small yield on top; the asset's own price move still dominates your actual dollar result.",
   chapter="Worked example", n=3, of=3, q="Does staking protect against price falls?",
   a="No. It adds a small yield; price moves dominate.")

# ---------------------------------------------------------------- checklist and recap
sc("title", "Checking a validator, concretely.", chapter="Checklist", eyebrow="Checklist", num="1", title="What to actually look at",
   sub="Not just the advertised rate.")
sc("steps", "Here's exactly what to check on a validator or delegation provider, before staking anything with them. Its uptime percentage, over as long a track record as you can find, not just recent weeks. Whether it's ever been slashed, and if so, what actually happened. Its fee, and how that compares to similar providers. And how concentrated total stake already is with it, since heavy concentration in one provider is its own separate risk to the network.",
   chapter="Checklist", title="What to actually check",
   steps=["Uptime %, over as long a track record as you can find", "Any slashing history, and what actually happened", "Its fee, compared against similar providers", "How concentrated total stake already is with it"])
sc("steps", "Here's your checklist. Do it before staking anything. Choose your validator, or provider, based on its actual uptime record, its fee, how concentrated stake already is with it, and its track record, not just the advertised rate. Know the unbonding period, in actual days, before you commit. And stake only capital you'd genuinely hold anyway, regardless of the staking yield entirely.",
   chapter="Checklist", title="Your checklist",
   steps=["Validator/provider chosen on uptime, fee, concentration, record", "Unbonding period known, in actual days", "Only 'hold-anyway' capital staked"])
sc("bullets", "Let's recap. Staking rewards pay for securing the network, whether you run a validator yourself or delegate to one. The real risks are slashing, unbonding periods, and validator downtime, none of which show up in the headline rate. Staking adds a small yield on top of whatever the asset does anyway; it never protects against a falling price. And the rule that follows from all of it: stake what you'd hold anyway, nothing more.",
   chapter="Recap", title="Recap", check=False,
   items=["Staking rewards pay for securing the network", "Real risks: slashing, unbonding periods, validator downtime",
          "Staking adds yield — it never protects against a falling price", "Rule: stake what you'd hold anyway, nothing more"])
sc("cta", "Choose your validator on its record, not just its rate, know your unbonding period, and only stake what you'd hold anyway. Next up, Lesson four point three: liquid staking, and L.S.T.s.",
   "Choose your validator on its record, not just its rate, know your unbonding period, and only stake what you'd hold anyway. Next up, Lesson 4.3: liquid staking (LSTs).",
   chapter="Recap", button="Next: Lesson 4.3", sub="Liquid staking (LSTs)")

spec = {"id": "lesson-04-2", "title": "Lesson 4.2: Native staking", "size": [1920, 1080], "group": "lessons", "maxMinutes": 25,
        "tag": "Lesson 4.2", "gold": True, "music": True, "musicLevel": 0.14, "seed": 71,
        "use": "Lesson 4.2 page in the Whop course. Hand-written gold-standard script: what staking rewards pay for, running a validator vs delegating, slashing/unbonding/downtime risk, and the source material's own +3%/-30% worked example, as walk-throughs.",
        "thumbnail": {"title": "Native staking", "subtitle": "Lesson 4.2"}, "scenes": S}
out = ROOT / "video-scripts" / "gold" / "lesson-04-2.json"
out.write_text(json.dumps(spec, indent=1, ensure_ascii=False))
words = sum(len(s["vo"].replace("[[pause 4]]", "").split()) for s in S)
print(f"{len(S)} scenes, {words} words, est {(words / 171 * 60 + len(S) * 1.3 + 4 * 3) / 60:.1f} min")
