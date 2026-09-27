#!/usr/bin/env python3
"""Gold-standard script for Lesson 4.4, Restaking & shared security
(target 11-14 minutes, per the "a bit longer" note for lessons from here
on). Walks what restaking actually reuses, the extra slashing/operator
risk layers it stacks on, correlated failure, and the source material's
own worked example (ETH -> staked -> LST -> liquid restaking token ->
restaking protocol -> 4 services = 6 layers, each able to fail; plan with
points valued at zero), as visual walk-throughs. Written in one pass at
the full target length (no separate expansion round).

Writes video-scripts/gold/lesson-04-4.json (the generator skips lessons
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
sc("title", "Lesson four point four. Restaking, and shared security. By the end, you'll be able to map every extra risk layer restaking adds, before ever accepting its extra yield in exchange.",
   "Lesson 4.4. Restaking & shared security. By the end, you'll be able to map every extra risk layer restaking adds, before ever accepting its extra yield in exchange.",
   chapter="Intro", eyebrow="Lesson 4.4", num="4.4", title="Restaking & shared security", sub="Plan with points valued at zero.")
sc("pillars", "Here's the plan. What restaking actually reuses, and why services are willing to pay extra for it. The two new risks this specifically adds: extra slashing conditions, and operator risk. Correlated failure, what happens when one collateral base secures many services at once. And a full worked example, stacking up the source material's own six-layer scenario.",
   chapter="Intro", title="What this lesson covers",
   items=[{"icon": "coins", "title": "What restaking reuses", "text": "The same staked assets, securing more than one thing"}, {"icon": "alert", "title": "Two new risks", "text": "Extra slashing conditions, plus operator risk"},
          {"icon": "chart", "title": "Correlated failure", "text": "One collateral base, many services, one failure point"}, {"icon": "target", "title": "Worked example", "text": "Six layers, stacked, each able to fail"}])

# ---------------------------------------------------------------- what restaking reuses
sc("title", "What restaking actually reuses.", chapter="What restaking reuses", eyebrow="What restaking reuses", num="1", title="The same staked assets, working twice",
   sub="Extra rewards, and often points, for taking on extra duty.")
img(D + "restaking-layers.png", "How restaking actually stacks",
    "Here's what restaking actually does with assets you've already staked. Instead of that stake securing only its original network, restaking reuses the exact same staked value to secure additional services on top of it, things like oracles, bridges, or other infrastructure that also need real economic security behind them. In exchange for taking on that extra duty, and its risk, you're paid extra rewards, and very often points, on top of your original staking yield.",
    chapter="What restaking reuses")
sc("statement", "Worth being precise about why these additional services are willing to pay for this at all, rather than simply building their own security from scratch. Bootstrapping genuine economic security from nothing is slow and expensive. Renting already-staked, already-trusted value is faster, and often cheaper, for the service. That's a completely reasonable trade for them to want to make. It doesn't automatically make it a good trade for you.",
   chapter="What restaking reuses", kicker="Why services pay for this", lines=["Renting already-trusted security is faster than building it.", "A reasonable trade for them. Not automatically one for you."], sub="The rest of this lesson is about pricing your side of that trade correctly.")
sc("compare", "Here's the actual trade-off, side by side, between leaving a stake exactly where it is versus restaking it further. Plain staking carries one network's own slashing and downtime risk, already covered back in Lesson four point two, and nothing more on top of that. Restaking adds every additional service's own slashing conditions and operator risk, stacked directly on top of that same original exposure, in exchange for the extra reward.",
   chapter="What restaking reuses",
   left={"label": "Plain staking", "tone": "good", "items": ["One network's own slashing and downtime risk", "Nothing stacked on top of that"]},
   right={"label": "Restaking", "tone": "warn", "items": ["Every additional service's risk, stacked on top", "In exchange for the extra reward"]})
sc("quiz", "Quick check. What does restaking actually add, in exchange for extra rewards? [[pause 4]] The answer: extra slashing conditions, and operator risk, on top of whatever risk your original stake already carried.",
   chapter="What restaking reuses", n=1, of=3, q="What does restaking add?",
   a="Extra rewards in exchange for extra slashing and operator risk.")

# ---------------------------------------------------------------- two new risks
sc("title", "Two new risks, stacked on top.", chapter="Two new risks", eyebrow="Two new risks", num="1", title="Slashing conditions · Operator risk",
   sub="Each additional service brings its own version of both.")
sc("flow", "Here's exactly what each of these two risks actually means, since they compound rather than simply repeat. Every additional service you help secure comes with its own slashing conditions, its own specific rules for what counts as misbehaviour, and its own specific penalty for it. And every service also depends on an operator, the entity actually running that service's infrastructure day to day, whose own competence and reliability becomes part of your risk too.",
   chapter="Two new risks", title="What each new service actually adds",
   nodes=[{"label": "New slashing conditions", "sub": "Its own rules, its own penalty, per service", "icon": "alert"}, {"label": "New operator risk", "sub": "Their competence and reliability, now yours too", "icon": "shield"},
          {"label": "Neither one repeats", "sub": "Each service adds its own separate exposure", "icon": "chart"}])
sc("statement", "Worth being precise about how these risks actually stack across multiple services, since it isn't simply additive in the way it might first appear. Securing four separate services doesn't just mean four separate, independent risks sitting side by side. It means four separate ways your one underlying stake can be slashed, any one of which alone is enough to cost you, regardless of how well the other three are performing.",
   chapter="Two new risks", kicker="How this actually stacks", lines=["Four services isn't four independent risks side by side.", "It's four separate ways your one stake can be slashed."], sub="Any single one going wrong is enough, whatever the other three do.")
sc("quiz", "Quick check. What are the two new risks restaking specifically stacks on top of ordinary staking? [[pause 4]] The answer: each service's own slashing conditions, and the operator risk of whoever actually runs that service.",
   chapter="Two new risks", n=2, of=3, q="What two risks does restaking add per service?",
   a="Each service's own slashing conditions, and its operator's risk.")

# ---------------------------------------------------------------- correlated failure
sc("title", "Correlated failure.", chapter="Correlated failure", eyebrow="Correlated failure", num="1", title="One collateral base, many services, one failure point",
   sub="They all lean on the same underlying stake.")
sc("flow", "Here's exactly why correlated failure is the real structural concern underneath all of this, not just a restatement of ordinary risk. One single collateral base ends up securing many different services simultaneously. That collateral base isn't duplicated for each service; it's the same underlying value, shared across every one of them. A serious failure in any single service can therefore reach back and hit that same shared collateral, and through it, every other service depending on it too.",
   chapter="Correlated failure", title="Why one failure can reach every service",
   nodes=[{"label": "One collateral base", "sub": "Shared, not duplicated, across services", "icon": "coins"}, {"label": "Secures many services at once", "sub": "All leaning on that same shared value", "icon": "chart"},
          {"label": "One service fails seriously", "sub": "The shared collateral is what gets hit", "icon": "alert"}, {"label": "Every other service feels it too", "sub": "Through that same shared collateral", "icon": "target"}])
sc("statement", "Worth being precise about what this actually means for how you should think about diversification here, since the usual instinct doesn't quite apply. Securing four services with the same underlying stake isn't the same kind of diversification as holding four unrelated assets. It's closer to four separate ways one single point can fail, all sharing the exact same foundation underneath them.",
   chapter="Correlated failure", kicker="Why this isn't ordinary diversification", lines=["Four services isn't like holding four unrelated assets.", "It's four ways one single foundation can fail."], sub="The usual diversification instinct doesn't quite apply here.")
sc("title", "Tracing one failure through the stack.", chapter="Correlated failure", eyebrow="Correlated failure", num="2", title="What happens when just one service trips",
   sub="A concrete walk-through of the mechanism above.")
sc("flow", "Here's that mechanism traced through concretely, one step at a time, for a single service out of several. One of the four services you're securing suffers a genuine slashing event, triggered entirely by its own conditions. That slashing draws directly against the shared collateral underneath it, the same collateral backing your other three services too. Your position across all four services is now thinner than it was, even though the other three services themselves did absolutely nothing wrong.",
   chapter="Correlated failure", title="One service's failure, traced through",
   nodes=[{"label": "One service is slashed", "sub": "Triggered entirely by its own conditions", "icon": "alert"}, {"label": "Draws against shared collateral", "sub": "The same collateral backing the other three", "icon": "coins"},
          {"label": "All four positions are now thinner", "sub": "Even though three of them did nothing wrong", "icon": "target"}])
sc("steps", "Here's how to actually read a service's slashing conditions yourself, before you ever secure it. Find its own published documentation specifically on what triggers a penalty, not just its advertised reward rate. Check whether the penalty is a small, capped amount, or can scale up to a much larger share of the stake. And check how the service's own operator has actually performed historically, since that track record is what you're really trusting.",
   chapter="Correlated failure", title="Reading a service's slashing conditions",
   steps=["Find its documentation on what actually triggers a penalty", "Check whether the penalty is capped, or can scale much higher", "Check that service's operator's actual historical track record"])

# ---------------------------------------------------------------- worked example
sc("title", "Worked example.", chapter="Worked example", eyebrow="Worked example", num="1", title="Six layers, stacked, for one position",
   sub="The source material's own scenario.")
sc("steps", "Here's the full stack, exactly as the source material lays it out, layer by layer, for a single restaking position. E.T.H., staked to become native staked E.T.H. That becomes an L.S.T., a liquid staking token. The L.S.T. is deposited into a restaking protocol, becoming a liquid restaking token. That restaking protocol then secures four separate services on top. Count them up, and that's six layers, total, each one of them independently able to fail.",
   chapter="Worked example", title="ETH → staked → LST → LRT → restaking protocol → 4 services",
   steps=["ETH → staked ETH → LST → liquid restaking token", "→ a restaking protocol → 4 separate services", "That's 6 layers, total, each independently able to fail"], result="Every extra layer of yield is also an extra layer of risk")
sc("statement", "Here's the one sentence this entire worked example exists to prove, worth holding onto more than the specific count of layers. The extra yield restaking offers has to genuinely pay for every single one of those six layers, not just the headline risk you happen to notice first. If it doesn't, you're not being paid enough for what you've actually taken on.",
   chapter="Worked example", kicker="The one sentence to keep", lines=["The extra yield has to pay for all six layers.", "Not just the one risk you happen to notice first."], sub="If it doesn't cover all six, you're underpaid for the real risk.")
sc("compare", "Here's specifically why points deserve their own separate treatment in this stack, rather than being counted as guaranteed extra yield. A stated A.P.Y. is a number the protocol is actually committing to, right now, however it ultimately gets funded. Points are, at best, a claim on some future, unconfirmed reward, of unknown size, that may or may not ever materialise into anything at all.",
   chapter="Worked example",
   left={"label": "Stated APY", "tone": "good", "items": ["A number the protocol commits to now", "However it ultimately gets funded"]},
   right={"label": "Points", "tone": "bad", "items": ["A claim on an unconfirmed future reward", "Unknown size; may never materialise"]})
sc("quiz", "Quick check. How should points be valued, specifically, when you're planning around a restaking position? [[pause 4]] The answer: at zero. Treat any actual payout as a pleasant surprise, never as part of the plan itself.",
   chapter="Worked example", n=3, of=3, q="How should points be valued when planning?",
   a="At zero.")

# ---------------------------------------------------------------- checklist and recap
sc("title", "What 'speculative bucket' actually means.", chapter="Checklist", eyebrow="Checklist", num="1", title="A specific test, not just a vague label",
   sub="Ask this before sizing any restaking position.")
sc("statement", "Worth being precise about what sizing something in your speculative bucket actually means, in practice, rather than treating it as a vague label. The real test is simple: could this entire position go to zero, all six layers at once, without changing a single one of your actual plans. If the honest answer is no, the position is currently sized too large for what it actually is.",
   chapter="Checklist", kicker="The actual test", lines=["Could this go to zero without changing your plans?", "If the honest answer is no, it's sized too large."], sub="This is the whole test. Apply it before sizing, not after.")
sc("steps", "Here's your checklist. Do it before restaking anything. Write down every single layer of your own stack, explicitly, the way the worked example just did. Read the actual slashing conditions of every service in that stack, not just the headline A.P.Y. it advertises. And size the entire position inside your speculative bucket specifically, never inside capital you're depending on.",
   chapter="Checklist", title="Your checklist",
   steps=["Every layer of the stack written down", "Slashing conditions of each service read", "Sized in the speculative bucket"])
sc("statement", "Here's the question this entire lesson reduces to, in the same spirit as the yield-farming question from earlier in this module. Would you take on six separate, stacked failure points, each capable of costing you on its own, for whatever this specific restaking position actually pays, once points are correctly valued at zero? If the honest answer is no, the extra yield isn't actually paying for what it's asking you to carry.",
   chapter="Recap", kicker="The question this reduces to", lines=["Six stacked failure points. Points valued at zero.", "Does the real yield actually pay for that?"], sub="If the honest answer is no, it isn't paying enough.")
sc("bullets", "Let's recap. Restaking reuses your already-staked assets to secure additional services, for extra rewards and often points. Each new service adds its own slashing conditions and its own operator risk, on top of what you already carried. One shared collateral base securing many services creates correlated failure, not ordinary diversification. And points get valued at zero when planning, since only the stated A.P.Y. is an actual commitment.",
   chapter="Recap", title="Recap", check=False,
   items=["Restaking reuses staked assets to secure more services, for extra reward", "Each service adds its own slashing conditions and operator risk",
          "One shared collateral base securing many services = correlated failure", "Points are valued at zero when planning — only the stated APY is a real commitment"])
sc("cta", "Write down every layer of your stack, read each service's slashing conditions, and size it in your speculative bucket, with points valued at zero. Next up, Lesson four point five: vaults and yield optimisers.",
   "Write down every layer of your stack, read each service's slashing conditions, and size it in your speculative bucket, with points valued at zero. Next up, Lesson 4.5: vaults and yield optimisers.",
   chapter="Recap", button="Next: Lesson 4.5", sub="Vaults & yield optimisers")

spec = {"id": "lesson-04-4", "title": "Lesson 4.4: Restaking & shared security", "size": [1920, 1080], "group": "lessons", "maxMinutes": 25,
        "tag": "Lesson 4.4", "gold": True, "music": True, "musicLevel": 0.14, "seed": 73,
        "use": "Lesson 4.4 page in the Whop course. Hand-written gold-standard script: what restaking reuses, slashing/operator risk per service, correlated failure, and the source material's own 6-layer worked example, as walk-throughs.",
        "thumbnail": {"title": "Restaking & shared security", "subtitle": "Lesson 4.4"}, "scenes": S}
out = ROOT / "video-scripts" / "gold" / "lesson-04-4.json"
out.write_text(json.dumps(spec, indent=1, ensure_ascii=False))
words = sum(len(s["vo"].replace("[[pause 4]]", "").split()) for s in S)
print(f"{len(S)} scenes, {words} words, est {(words / 171 * 60 + len(S) * 1.3 + 4 * 3) / 60:.1f} min")
