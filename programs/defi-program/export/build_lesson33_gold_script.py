#!/usr/bin/env python3
"""Gold-standard script for Lesson 3.3, Liquidations and cascades (target
10-20 minutes). Walks exactly what a liquidator does, how cascades form,
and the source material's own worked example continuing Lesson 3.2's
position (10 ETH, $12,000 debt; ETH falls to $1,490: a liquidator repays
$6,000, seizes $6,300 of ETH, a $300 bonus lost to you), plus the written
defence ladder (HF 2.0 alert, 1.7 repay/add, 1.5 sell yourself, never wait
for 1.1), as visual walk-throughs. Built to the walk-through-first
standard: almost every idea is a flow, steps or callout image, not a
statement read over a static screen.

Writes video-scripts/gold/lesson-03-3.json (the generator skips lessons
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
sc("title", "Lesson three point three. Liquidations and cascades. By the end, you'll know exactly what a liquidation costs you, and how to avoid ever reaching one.",
   "Lesson 3.3. Liquidations and cascades. By the end, you'll know exactly what a liquidation costs you, and how to avoid ever reaching one.",
   chapter="Intro", eyebrow="Lesson 3.3", num="3.3", title="Liquidations and cascades", sub="Never wait for 1.1.")
sc("pillars", "Here's the plan. Exactly what a liquidator does, mechanically, the moment your health factor crosses below one. How a single liquidation can actually trigger a cascade of more. A full worked example, continuing directly from Lesson three point two's own position. And the written defence ladder that keeps you from ever needing to find out what any of this actually costs.",
   chapter="Intro", title="What this lesson covers",
   items=[{"icon": "alert", "title": "What a liquidator does", "text": "Repays debt, seizes collateral, plus a bonus"}, {"icon": "chart", "title": "Cascades", "text": "How one liquidation can trigger more"},
          {"icon": "target", "title": "Worked example", "text": "Continuing Lesson 3.2's own position"}, {"icon": "shield", "title": "The defence ladder", "text": "Written, with exact HF levels"}])

# ---------------------------------------------------------------- what a liquidator does
sc("title", "What a liquidator actually does.", chapter="What a liquidator does", eyebrow="What a liquidator does", num="1", title="The moment health factor crosses below one",
   sub="Usually a bot. Always mechanical.")
img(D + "liquidation-cascade.png", "The mechanism, step by step",
    "Here's exactly what happens, the instant your health factor drops below one. A liquidator, almost always a bot watching for exactly this, repays part of your debt, up to a limit called the close factor, often fifty percent. In exchange, it seizes collateral worth that same repaid amount, plus a bonus, the liquidation penalty, often five to ten percent. That bonus is the liquidator's profit, and it comes directly out of what would otherwise have been your collateral.",
    chapter="What a liquidator does")
sc("flow", "Here's that same sequence, broken into its four actual steps, since “liquidator” can sound abstract until you see the mechanics. Your health factor crosses below one. A bot notices, essentially instantly; this is automated, competitive, and fast. It repays up to the close factor of your debt. And it seizes collateral worth that repayment, plus the bonus, leaving you with less collateral and less debt, but a real loss on the bonus itself.",
   chapter="What a liquidator does", title="The four actual steps",
   nodes=[{"label": "HF crosses below 1", "sub": "The trigger, automatic", "icon": "alert"}, {"label": "A bot notices, instantly", "sub": "Automated and competitive", "icon": "eye"},
          {"label": "Repays up to the close factor", "sub": "Often 50% of your debt", "icon": "coins"}, {"label": "Seizes collateral + bonus", "sub": "The penalty: often 5–10%", "icon": "alert"}])
sc("stats", "One real number, so this isn't a rare edge case. Blockchain analytics have tracked billions of dollars in total liquidations across major lending protocols, cumulatively, since DeFi lending began. This is outside research, not this program's own data, but it's exactly why this lesson's defence ladder is worth writing down now, not after your first close call.",
   chapter="What a liquidator does", stats=[["$Bs+", "total DeFi liquidations, tracked cumulatively (outside research)"]])
sc("quiz", "Quick check. What does a liquidator actually receive, in exchange for repaying part of your debt? [[pause 4]] The answer: collateral equal to the debt it repaid, plus a bonus, the liquidation penalty, often five to ten percent, which is a real loss to you.",
   chapter="What a liquidator does", n=1, of=3, q="What does a liquidator actually receive, in exchange for repaying part of your debt?",
   a="Collateral equal to the debt repaid, plus a bonus (the liquidation penalty).")

# ---------------------------------------------------------------- cascades
sc("title", "Cascades.", chapter="Cascades", eyebrow="Cascades", num="2", title="How one liquidation can trigger more",
   sub="Selling into an already-falling market.")
sc("flow", "Here's exactly how a cascade actually forms, step by step, since it's the mechanism that turns an isolated event into a market-wide one. A liquidation sells seized collateral, immediately, into the open market. That sale itself pushes the price down further, the same price-impact mechanism from Module two. That further price drop pushes other, separate positions below their own health-factor line. And those get liquidated too, selling more collateral, into an already-falling price.",
   chapter="Cascades", title="How one liquidation becomes many",
   nodes=[{"label": "A liquidation sells collateral", "sub": "Into the open market, immediately", "icon": "swap"}, {"label": "That sale pushes price down further", "sub": "The same price-impact mechanism, from Module 2", "icon": "chart"},
          {"label": "Other positions cross below HF 1", "sub": "Pushed there by the falling price", "icon": "alert"}, {"label": "Those get liquidated too", "sub": "Selling more, into an already-falling price", "icon": "layers"}])
sc("statement", "Worth being precise about why this matters even if your own position feels perfectly safe. A cascade isn't really about any single borrower's mistake; it's a mechanical feedback loop, forced selling causing more forced selling, that can move a market meaningfully in a short window. It's exactly why a comfortable buffer matters most during genuinely volatile periods, not just on an average day.",
   chapter="Cascades", kicker="Why this matters even when you feel safe", lines=["A mechanical feedback loop.", "Forced selling, causing more forced selling."], sub="Exactly why a buffer matters most in genuinely volatile periods.")
sc("statement", "Worth naming, plainly, that cascades aren't a theoretical risk this lesson invented. DeFi lending markets have genuinely experienced sharp, fast periods of concentrated liquidations during major market drops, with total liquidation volume spiking well above a typical day's level in a matter of hours. This is outside research, illustrative of the pattern, not a specific claim about any one event, but the pattern itself is well documented.",
   chapter="Cascades", kicker="Not a theoretical risk", lines=["Genuinely happened, during major market drops.", "Liquidation volume spiking, well above typical, in hours."], sub="The pattern is well documented, even where specific events vary.")
sc("quiz", "Quick check. What's the actual mechanism that turns one liquidation into a cascade of more? [[pause 4]] The answer: liquidations sell collateral into the market, pushing the price down, which pushes other, separate positions below their own health-factor line, triggering further liquidations.",
   chapter="Cascades", n=2, of=3, q="What's the actual mechanism that turns one liquidation into a cascade of more?",
   a="Liquidations sell collateral, pushing prices down, which pushes more positions below HF 1.")

# ---------------------------------------------------------------- worked example
sc("title", "Worked example.", chapter="Worked example", eyebrow="Worked example", num="1", title="Continuing Lesson 3.2's own position",
   sub="10 ETH, $12,000 debt, HF 2.0. Now watch it fall.")
sc("stats", "Here's the exact position this worked example continues from Lesson three point two. Ten E.T.H., thirty thousand dollars of collateral, twelve thousand dollars of debt, a health factor of two. Now E.T.H. falls to one thousand four hundred ninety dollars, just under the fifteen-hundred-dollar liquidation price. Health factor is now just under one.",
   "Here's the exact position this worked example continues from Lesson 3.2. 10 ETH, $30,000 of collateral, $12,000 of debt, a health factor of 2. Now ETH falls to $1,490, just under the $1,500 liquidation price. Health factor is now just under 1.",
   chapter="Worked example", stats=[["ETH: $1,490", "just under the $1,500 liquidation price from Lesson 3.2"]])
sc("steps", "Now watch exactly what the liquidator does, in this specific case, step by step. It repays six thousand dollars, fifty percent of your twelve-thousand-dollar debt, the close factor. It seizes collateral worth six thousand dollars, times one point zero five, the five-percent bonus, which is six thousand three hundred dollars. At one thousand four hundred ninety dollars per E.T.H., that's roughly four point two two eight E.T.H., seized from your position.",
   chapter="Worked example", title="What the liquidator actually does, here",
   steps=["Repays $6,000 (50% close factor)", "Seizes $6,000 × 1.05 = $6,300 of collateral", "At $1,490/ETH: ≈ 4.228 ETH seized"], result="The $300 bonus: a pure loss to you, on top of selling near the low")
sc("statement", "Worth being precise about what that three hundred dollars actually represents, since it's easy to gloss past as a small number. It's not a fee for a service you needed. It's value that leaves your position specifically because you didn't act first, on top of having your collateral sold, involuntarily, near the low of that exact price move. The bonus is the entire reason self-deleveraging beats being liquidated.",
   chapter="Worked example", kicker="What the $300 actually represents", lines=["Not a fee for a service you needed.", "Value lost, specifically because you didn't act first."], sub="The entire reason self-deleveraging beats being liquidated.")
sc("statement", "Worth naming what's actually left of your position after this specific liquidation, since fifty percent repaid isn't the whole story. Your debt drops from twelve thousand to six thousand dollars. Your collateral drops by that roughly four point two two eight E.T.H. seized. If price keeps falling from here, health factor can cross below one again, and the exact same process can repeat, on what's left.",
   chapter="Worked example", kicker="What's actually left, afterward", lines=["Debt: $12,000 → $6,000.", "If price keeps falling, the same process can repeat."], sub="One liquidation doesn't guarantee it's the only one.")
sc("quiz", "Quick check. Why is choosing to sell some of your own collateral yourself, before liquidation, better than letting it happen automatically? [[pause 4]] The answer: you avoid the liquidation penalty entirely, and you choose the size and timing yourself, instead of a bot forcing both on you.",
   chapter="Worked example", n=3, of=3, q="Why is choosing to sell some of your own collateral yourself, before liquidation, better than letting it happen automatically?",
   a="You avoid the penalty, and choose the size and timing yourself.")

# ---------------------------------------------------------------- the defence ladder
sc("title", "The defence ladder.", chapter="The defence ladder", eyebrow="The defence ladder", num="1", title="Written down, with exact HF levels",
   sub="Never wait for 1.1.")
sc("steps", "Here's the actual ladder, with exact health-factor levels, written down before you ever need it, not decided under pressure. At health factor two point zero: an alert fires, nothing else yet. At one point seven: repay from a reserve you've already set aside, or add more collateral. At one point five: sell part of your collateral yourself, deliberately, on your own terms. And never, under any circumstance, wait until one point one to start acting.",
   chapter="The defence ladder", title="The ladder, with exact levels",
   steps=["HF 2.0 → an alert fires", "HF 1.7 → repay from reserve, or add collateral", "HF 1.5 → sell part of your collateral, yourself", "Never wait for 1.1"], result="Written down in advance, not decided under pressure")
sc("flow", "Here's what actually setting up that health-factor-two alert looks like, in practice, from the ladder's very first rung. Open your protocol's own notification settings, or a third-party monitoring tool, covered fully in Module fourteen point one. Set a trigger at your own chosen health-factor level. Point it at a channel you'll actually see quickly, not one you check once a week. And test it once, deliberately, so you know it actually works before you need it to.",
   chapter="The defence ladder", title="Setting up the HF 2.0 alert, in practice",
   nodes=[{"label": "Open notification settings", "sub": "Your protocol, or a monitoring tool", "icon": "cog"}, {"label": "Set a trigger at HF 2.0", "sub": "Your own chosen level", "icon": "target"},
          {"label": "Point it at a fast channel", "sub": "Not one you check weekly", "icon": "eye"}, {"label": "Test it once", "sub": "Before you actually need it", "icon": "check"}])
sc("statement", "Worth being precise about what “repay from reserve” at HF 1.7 actually buys you, versus waiting. Repaying debt directly raises health factor immediately, by the same formula from Lesson three point two, without touching your collateral at all. Adding collateral instead raises it too, but ties up more capital. Either move, taken at 1.7, costs nothing beyond the capital itself. The same move, forced at 1.1, costs the liquidation penalty on top.",
   chapter="The defence ladder", kicker="What acting early actually buys you", lines=["Repay, or add collateral — either raises HF.", "At 1.7: costs only the capital. At 1.1: costs the penalty too."], sub="Same move. Radically different cost, depending on when.")
sc("compare", "Put the two paths side by side, at the exact same starting point, since the entire lesson comes down to this choice. Wait, and a bot decides the size, the timing, and takes a bonus on top, at whatever price the market happens to be at that moment. Act at one point five, and you choose the size, the timing, and keep the full value of what you sell, no penalty attached.",
   chapter="The defence ladder",
   left={"label": "Wait for liquidation", "tone": "bad", "items": ["A bot decides size and timing", "Pays a bonus, on top of a forced sale"]},
   right={"label": "Act at HF 1.5, yourself", "tone": "good", "items": ["You decide size and timing", "Keep full value — no penalty"]})

# ---------------------------------------------------------------- checklist and recap
sc("steps", "Here's your checklist. Do it now, before you ever need it. Your defence ladder is written, with exact health-factor levels, not vague intentions. A reserve is actually set aside to repay from, covered fully in Module twelve point four. And you know your collateral's specific price oracle, covered in Module five point three, since that's what actually decides when liquidation triggers.",
   chapter="Checklist", title="Your checklist",
   steps=["Defence ladder written, with exact HF levels", "Reserve set aside to repay from", "Your collateral's specific price oracle, known"])
sc("statement", "One last honest connection before the recap, since this ladder is only as good as the reserve behind it. Rung two of the ladder, repay from reserve, assumes that reserve genuinely exists, already funded, before health factor ever gets there. A defence ladder with an empty reserve rung is really just a two-step ladder, with a gap exactly where you need it most.",
   chapter="Recap", kicker="The ladder needs a funded reserve", lines=["An empty reserve rung is really a gap.", "Exactly where the ladder needs to hold most."], sub="Module 12.4 covers setting that reserve aside properly.")
sc("bullets", "Let's recap. A liquidator repays part of your debt, up to the close factor, and seizes that value in collateral, plus a bonus, a real loss to you. Cascades form because liquidations sell into the market, pushing prices down, triggering more liquidations. In the worked example, a fall to fourteen ninety cost three hundred dollars in bonus alone, on top of an involuntary sale near the low. And the defence ladder, written with exact HF levels, is what keeps you from ever finding any of that out the hard way.",
   chapter="Recap", title="Recap", check=False,
   items=["A liquidator: repays debt, seizes collateral + a bonus", "Cascades: forced selling pushes prices down, triggering more",
          "The worked example: a $300 bonus lost, on top of a forced sale near the low", "The defence ladder: written, with exact HF levels, in advance"])
sc("cta", "Write your defence ladder now, with exact health-factor levels, before you ever need it under pressure. Next up, Lesson three point four: Borrowing strategies and looping.",
   "Write your defence ladder now, with exact health-factor levels, before you ever need it under pressure. Next up, Lesson 3.4: Borrowing strategies and looping.",
   chapter="Recap", button="Next: Lesson 3.4", sub="Borrowing strategies and looping")

spec = {"id": "lesson-03-3", "title": "Lesson 3.3: Liquidations and cascades", "size": [1920, 1080], "group": "lessons", "maxMinutes": 25,
        "tag": "Lesson 3.3", "gold": True, "music": True, "musicLevel": 0.14, "seed": 64,
        "use": "Lesson 3.3 page in the Whop course. Hand-written gold-standard script: what a liquidator does, how cascades form, and the source material's own worked example continuing Lesson 3.2's position, plus the written defence ladder, as walk-throughs.",
        "thumbnail": {"title": "Liquidations and cascades", "subtitle": "Lesson 3.3"}, "scenes": S}
out = ROOT / "video-scripts" / "gold" / "lesson-03-3.json"
out.write_text(json.dumps(spec, indent=1, ensure_ascii=False))
words = sum(len(s["vo"].replace("[[pause 4]]", "").split()) for s in S)
print(f"{len(S)} scenes, {words} words, est {(words / 171 * 60 + len(S) * 1.3 + 4 * 3) / 60:.1f} min")
