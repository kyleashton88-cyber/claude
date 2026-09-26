#!/usr/bin/env python3
"""Gold-standard script for Lesson 2.4, Impermanent loss & true LP P&L (~9-11 min).

Source: lessons/module-02-trading-on-chain.md, "Lesson 2.4 -- Impermanent
loss & true LP P&L". Teaches: the IL formula (IL = 2sqrt(r)/(1+r) - 1),
why it's only "impermanent" until you withdraw, full LP P&L vs. hold value,
and the real worked example (1 ETH + 3,000 USDC at $3,000, ETH rises to
$4,000: LP total $7,058 vs. $7,000 holding, so LPing itself only added $58,
not the headline +$1,058).

Uses flow3d (see .claude/skills/webgl-motion-graphics/SKILL.md) once, as a
manual-position diverge/converge diagram (start -> hold path / LP path ->
compare) -- the same proven manual-x/y technique as lesson-02-1's
branch/merge fan, just two paths instead of three. And chart3d once, for
the "+$1,058 vs. starting" vs. "+$58 vs. holding" comparison that is this
lesson's entire point. The IL-vs-ratio curve itself is a flat `chart`
line scene, not chart3d (which only supports bars/donut). That's this
skill's "at most one or two" WebGL-scene ceiling.

Writes video-scripts/gold/lesson-02-4.json.
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
sc("title", "Lesson two point four. Impermanent loss and true L.P. profit and loss. By the end, you'll be able to calculate an L.P. position's full profit and loss, and judge it against simply holding.",
   "Lesson 2.4. Impermanent loss & true LP P&L. By the end, you'll be able to calculate an LP position's full profit and loss, and judge it against simply holding.",
   chapter="Intro", eyebrow="Lesson 2.4", num="2.4", title="Impermanent loss & true LP P&L", sub="Your position can be 'up' and LPing can still have cost you money.")
sc("pillars", "Here's the plan. First, what impermanent loss actually is, and the formula behind it. Second, a real worked example, calculating the full P&L, not just the headline number. And third, the checklist to run so you always know if LPing actually worked.",
   chapter="Intro", title="What this lesson covers",
   items=[{"icon": "chart", "title": "Impermanent loss", "text": "What it is, and the formula"},
          {"icon": "cog", "title": "True P&L", "text": "The full calculation, worked with real numbers"},
          {"icon": "check", "title": "Checklist", "text": "Know if LPing actually worked"}])
sc("statement", "Your L.P. position can show a twenty percent gain, and LPing can still have cost you money. Until you compare against simply holding the same tokens, you genuinely don't know which one is true.",
   chapter="Why it matters", kicker="A number that can lie to you", lines=["Your position can be 'up' 20%.", "LPing can still have cost you money."], sub="You don't know which, until you compare against simply holding.")

# ---------------------------------------------------------------- what IL is
sc("title", "What impermanent loss is.", chapter="Impermanent loss", eyebrow="Impermanent loss", num="1", title="What impermanent loss is", sub="A gap with a formula, not a mystery.")
sc("bullets", "Impermanent loss is how far your L.P. position lags simply holding the same starting tokens, once their relative price changes. The formula: I.L. equals two times the square root of r, divided by one plus r, minus one, where r is the new price divided by your entry price. It's only impermanent if the price comes back. Withdraw after the move, and it's permanent, locked in the moment you exit.",
   chapter="Impermanent loss", title="The IL formula",
   items=["IL = 2√r ÷ (1 + r) − 1, where r = new price ÷ entry price", "Only \"impermanent\" if the price returns before you withdraw",
          "Withdraw after the move, and it's permanent, locked in at exit"])
sc("chart", "Here's that formula as a curve. At r equals one, price unchanged, I.L. is zero. Move the price either direction and I.L. grows, and it grows the same whether the price doubled or was cut in half, the formula doesn't care which way it moved. Double the price, and I.L. is about negative five point seven percent. Triple it, and it's already past negative thirteen percent.",
   "Here's that formula as a curve. At r = 1, price unchanged, IL is zero. Move the price either direction and IL grows, and it grows the same whether the price doubled or was cut in half — the formula doesn't care which way it moved. Double the price, and IL is about −5.7%. Triple it, and it's already past −13%.",
   chapter="Impermanent loss", kind="line", title="Impermanent loss vs. price ratio", sub="r = new price ÷ entry price — the curve is symmetric",
   series=[{"values": [-13.4, -5.7, -1.0, 0, -1.0, -5.7, -13.4], "tone": "bad", "label": "Impermanent loss %"}],
   xlabels=["r=3", "r=2", "r=1.33", "r=1", "r=0.75", "r=0.5", "r=0.33"], yticks=[[0, "0%"], [-7, "−7%"], [-14, "−14%"]],
   caption="Same IL whether price doubled or was cut in half — the formula is symmetric")
sc("quiz", "Quick check. E.T.H. doubles in price. What's the impermanent loss on a fifty-fifty pool? [[pause 4]] The answer: about negative five point seven percent, against simply holding.",
   n=1, of=3, q="ETH doubles. What is the impermanent loss on a 50/50 pool?", a="About −5.7% vs. holding.", chapter="Impermanent loss")

# ---------------------------------------------------------------- true p&l
sc("title", "The full P&L.", chapter="True P&L", eyebrow="True P&L", num="2", title="The full P&L", sub="Four numbers, one honest comparison.")
sc("statement", "Full L.P. profit and loss equals your L.P. value, plus fees earned, plus any incentives, minus gas. Compare that whole total against simply holding the same starting tokens, not against your original deposit. That second comparison is the only one that tells you whether LPing itself was worth it.",
   "Full LP profit and loss equals your LP value, plus fees earned, plus any incentives, minus gas. Compare that whole total against simply holding the same starting tokens, not against your original deposit. That second comparison is the only one that tells you whether LPing itself was worth it.",
   chapter="True P&L", kicker="The full formula", lines=["LP value + fees + incentives − gas,", "compared against holding."], sub="Not against your original deposit. That's the comparison that actually answers the question.")
sc("flow3d", "Walk through a real deposit. You put in one E.T.H. and three thousand U.S.D.C. at three thousand dollars an E.T.H., six thousand dollars total. From here, two paths. Holding, your tokens just sit there, unchanged. L.P.ing, the pool automatically rebalances your share as the price moves. Both paths land at the same finish line: a straight comparison of what each one was actually worth.",
   "Walk through a real deposit. You put in 1 ETH and 3,000 USDC at $3,000 an ETH, $6,000 total. From here, two paths. Holding, your tokens just sit there, unchanged. LPing, the pool automatically rebalances your share as the price moves. Both paths land at the same finish line: a straight comparison of what each one was actually worth.",
   chapter="True P&L", title="Two paths, one honest comparison", seed=24,
   nodes=[{"id": "start", "label": "Deposit $6,000", "sub": "1 ETH + 3,000 USDC at $3,000", "icon": "wallet", "x": 0.04, "y": 0.5},
          {"id": "hold", "label": "Hold path", "sub": "Tokens sit unchanged", "icon": "layers", "x": 0.5, "y": 0.12},
          {"id": "lp", "label": "LP path", "sub": "Pool auto-rebalances your share", "icon": "cog", "x": 0.5, "y": 0.88},
          {"id": "compare", "label": "Compare the two", "sub": "What each was actually worth", "icon": "chart", "x": 0.94, "y": 0.5}],
   edges=[{"from": "start", "to": "hold"}, {"from": "start", "to": "lp"}, {"from": "hold", "to": "compare"}, {"from": "lp", "to": "compare"}])
sc("steps", "Now the exact numbers. E.T.H. rises to four thousand dollars. The pool rebalances you to zero point eight six six E.T.H. and three thousand four hundred sixty four U.S.D.C. Your L.P. value: zero point eight six six times four thousand, plus three thousand four hundred sixty four, six thousand nine hundred twenty eight dollars. Holding instead would be worth four thousand plus three thousand, seven thousand dollars exactly. That's impermanent loss of seventy two dollars, about negative one point oh three percent. Add fees earned, one hundred fifty dollars, minus twenty dollars gas: your L.P. total is seven thousand fifty eight dollars.",
   chapter="True P&L", title="ETH: $3,000 → $4,000, worked in full",
   steps=["Pool rebalances you to: 0.866 ETH + 3,464 USDC", "LP value: 0.866 × $4,000 + $3,464 = $6,928",
          "Hold value: $4,000 + $3,000 = $7,000 → IL = −$72 (−1.03%)", "+ fees $150 − gas $20 = LP total $7,058"],
   result="LP total $7,058 vs. hold value $7,000 — LPing itself added $58")
sc("chart3d", "Here's the same result, framed two ways. Against your starting six thousand dollars, you're up one thousand fifty eight dollars, and that looks great. But almost all of that came from E.T.H. simply rising, not from LPing. Against holding, the honest comparison, you're up just fifty eight dollars. A master judges the position on the fifty eight, not the one thousand fifty eight.",
   "Here's the same result, framed two ways. Against your starting $6,000, you're up $1,058, and that looks great. But almost all of that came from ETH simply rising, not from LPing. Against holding, the honest comparison, you're up just $58. A master judges the position on the $58, not the $1,058.",
   chapter="True P&L", kind="bars", title="Two ways to frame the same result", sub="Same $7,058 LP total, two very different comparisons", seed=224,
   bars=[{"label": "vs. starting $6,000", "text": "Mostly ETH's price rising", "value": 1058, "show": "+$1,058", "tone": "warn"},
         {"label": "vs. holding $7,000", "text": "What LPing itself added", "value": 58, "show": "+$58", "tone": "good"}], max=1058)
sc("quiz", "Quick check. Your L.P. position is up twenty percent since deposit. Did LPing actually work? [[pause 4]] The answer: unknown, until you compare against simply holding. That twenty percent could be entirely the underlying price move.",
   n=2, of=3, q="Your LP is up 20% since deposit. Did LPing work?", a="Unknown until you compare with holding — the 20% could be all price.", chapter="True P&L")
sc("quiz", "Last check for this section. When does impermanent loss become permanent? [[pause 4]] The answer: the moment you withdraw while the price ratio is different from your entry.",
   n=3, of=3, q="When does impermanent loss become permanent?", a="When you withdraw while the price ratio differs from entry.", chapter="True P&L")

# ---------------------------------------------------------------- pitfalls
sc("title", "Where this judgment goes wrong.", chapter="Where this goes wrong", eyebrow="Where this goes wrong", num="3", title="Where this judgment goes wrong", sub="Four ways the number lies to you.")
sc("bullets", "Here's how people misjudge a position even after learning the formula. Watching the token count go up, and calling that a win, while ignoring what that same basket is actually worth in dollars. Forgetting incentive reward tokens entirely, extra emissions on top of swap fees, which change the real total either way. Comparing against the wrong hold baseline, today's price of just one token, instead of the actual basket you originally deposited. And ignoring the gas cost of frequent compounding, which quietly eats the very fees it's meant to reinvest.", check=False,
   chapter="Where this goes wrong", title="Where this judgment goes wrong",
   items=["Watching the token count rise, ignoring what that basket is actually worth",
          "Forgetting incentive reward tokens, on top of swap fees, in the total",
          "Comparing against the wrong hold baseline, not the actual deposited basket",
          "Ignoring the gas cost of frequent compounding, which eats the fees it reinvests"])

# ---------------------------------------------------------------- checklist
sc("title", "Before you judge a position.", chapter="Checklist", eyebrow="Checklist", num="4", title="Before you judge a position", sub="Three checks, run weekly.")
sc("bullets", "Run this on every open L.P. position, weekly. Track P&L against holding, not against your deposit. Record impermanent loss, fees, incentives and gas as separate line items, never blended into one number. And set an exit rule: if fees consistently fail to cover impermanent loss, that position is done. Two calculator commands do this math for you directly: I.L. by ratio, and L.P. break-even by ratio, days, and fee A.P.R.",
   chapter="Checklist", title="Before you judge a position",
   items=["Track P&L against holding, weekly, not against your deposit", "Record IL, fees, incentives and gas as separate line items",
          "Exit if fees consistently fail to cover impermanent loss"])

# ---------------------------------------------------------------- your turn
sc("statement", "Your turn, five to ten minutes. Pull up one open L.P. position, yours or a real one you can see the numbers for. Calculate its full P&L against holding, not against the deposit, and write down what LPing itself actually added.",
   "Your turn, 5 to 10 minutes. Pull up one open LP position, yours or a real one you can see the numbers for. Calculate its full P&L against holding, not against the deposit, and write down what LPing itself actually added.",
   chapter="Your turn", kicker="Your turn", lines=["Pick one open LP position.", "Calculate what LPing itself added."], sub="5 to 10 minutes, against holding, not against your deposit.")
sc("bullets", "To recap: impermanent loss is two times the square root of r, over one plus r, minus one, and it's only impermanent until you withdraw. Full L.P. P&L is your L.P. value, plus fees and incentives, minus gas. And the only honest comparison is against holding, not against your original deposit.",
   "To recap: impermanent loss is 2 times the square root of r, over 1 plus r, minus 1, and it's only impermanent until you withdraw. Full LP P&L is your LP value, plus fees and incentives, minus gas. And the only honest comparison is against holding, not against your original deposit.",
   chapter="Recap", title="Three things to remember",
   items=["IL = 2√r ÷ (1 + r) − 1 — impermanent only until you withdraw", "Full LP P&L = LP value + fees + incentives − gas",
          "Judge it against holding, never against your original deposit"])
sc("cta", "That's impermanent loss and true L.P. profit and loss. Next up, lesson two point five: M.E.V., and protecting your trades from it.",
   "That's impermanent loss and true LP profit and loss. Next up, Lesson 2.5: MEV, and protecting your trades from it.",
   chapter="Recap", button="Next: Lesson 2.5", sub="MEV and protecting your trades · Educational content only · Not financial advice")

video = {
    "id": "lesson-02-4",
    "title": "Lesson 2.4: Impermanent loss & true LP P&L",
    "size": [1920, 1080],
    "group": "lessons",
    "maxMinutes": 25,
    "tag": "Lesson 2.4",
    "gold": True,
    "seed": 24,
    "use": "Lesson 2.4 page in the Whop course. Hand-written gold-standard script: the IL formula (IL = 2sqrt(r)/(1+r) - 1), full LP P&L vs. hold value, and the real 1 ETH + 3,000 USDC worked example (ETH $3,000 -> $4,000: LP total $7,058 vs. $7,000 holding, so LPing itself added $58, not the headline +$1,058). Facts last checked: 2026-09-26.",
    "thumbnail": {"title": "+$58, not +$1,058", "subtitle": "Lesson 2.4"},
    "scenes": S,
}

out = ROOT / "video-scripts" / "gold" / "lesson-02-4.json"
out.write_text(json.dumps(video, indent=None))
print(f"wrote {out} ({len(S)} scenes)")
