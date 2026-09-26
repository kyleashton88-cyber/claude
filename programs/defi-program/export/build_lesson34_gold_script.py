#!/usr/bin/env python3
"""Gold-standard script for Lesson 3.4, Borrowing strategies & looping
(target 10-20 minutes). Walks borrowing for liquidity without selling, the
looping mechanism, the leverage and net-APY-on-equity formulas, correlated
vs volatile loops, and the source material's own worked example (LTV 0.7,
3 loops, 3.5% collateral yield, 2.5% borrow: 2.53x leverage, 5.03% net on
equity, wiped out at 5.78% borrow), as visual walk-throughs. Built to the
walk-through-first standard: almost every idea is a flow, steps or callout
image, not a statement read over a static screen.

Writes video-scripts/gold/lesson-03-4.json (the generator skips lessons
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
CH = "assets/charts/"

# ---------------------------------------------------------------- intro
sc("title", "Lesson three point four. Borrowing strategies and looping. By the end, you'll use borrowing deliberately, and know exactly when looping adds real return, and when it just adds risk.",
   "Lesson 3.4. Borrowing strategies and looping. By the end, you'll use borrowing deliberately, and know exactly when looping adds real return, and when it just adds risk.",
   chapter="Intro", eyebrow="Lesson 3.4", num="3.4", title="Borrowing strategies & looping", sub="One number decides whether a loop is worth it.")
sc("pillars", "Here's the plan. Borrowing for liquidity, without ever selling what you hold. Looping, mechanically, and the leverage formula it actually produces. Correlated loops versus volatile ones, and why that distinction matters more than the leverage number itself. And a full worked example, with real numbers, showing exactly when a loop's return gets wiped out.",
   chapter="Intro", title="What this lesson covers",
   items=[{"icon": "coins", "title": "Liquidity without selling", "text": "Borrow against what you want to keep"}, {"icon": "layers", "title": "Looping", "text": "Deposit, borrow, re-deposit, repeat"},
          {"icon": "shield", "title": "Correlated vs volatile", "text": "Why the pairing matters most"}, {"icon": "target", "title": "Worked example", "text": "2.53× leverage, and when it breaks"}])

# ---------------------------------------------------------------- liquidity without selling
sc("title", "Liquidity without selling.", chapter="Liquidity without selling", eyebrow="Liquidity without selling", num="1", title="Borrow against what you want to keep",
   sub="A deliberate credit policy, not a reaction.")
sc("statement", "Here's the actual use case borrowing solves, worth naming plainly before looping at all. You hold an asset you want to keep, long-term, but you need cash now, for something else entirely. Instead of selling, and losing your position, and potentially triggering a taxable event, you borrow stablecoins against it, keep the asset locked as collateral, and repay later. Module twelve point three turns this exact habit into a real, written credit policy.",
   chapter="Liquidity without selling", kicker="The actual use case", lines=["Keep the asset. Borrow the cash instead.", "No sale. No lost position. Repay later."], sub="Module 12.3 turns this habit into a written credit policy.")
sc("compare", "Put a real example side by side with the alternative, to make “liquidity without selling” concrete. Sell ten thousand dollars of an asset for cash, and you've lost that entire position, permanently, plus potentially triggered a taxable event on any gain. Borrow five thousand dollars against that same ten thousand instead, and you keep the full position, still growing if the asset does, while the cash need is met either way.",
   chapter="Liquidity without selling",
   left={"label": "Sell $10,000 of the asset", "tone": "bad", "items": ["Lose the position, permanently", "Potentially, a taxable event"]},
   right={"label": "Borrow $5,000 against it instead", "tone": "good", "items": ["Keep the full position", "Cash need met, either way"]})
sc("quiz", "Quick check. What's the core benefit of borrowing stablecoins against an asset, instead of selling it? [[pause 4]] The answer: you get liquidity now, without losing your position in the asset, and without triggering a sale you didn't actually want to make.",
   chapter="Liquidity without selling", n=1, of=3, q="What's the core benefit of borrowing stablecoins against an asset, instead of selling it?",
   a="Liquidity now, without losing your position or triggering a sale.")

# ---------------------------------------------------------------- looping
sc("title", "Looping.", chapter="Looping", eyebrow="Looping", num="2", title="Deposit, borrow, re-deposit, repeat",
   sub="Multiplying exposure to the same asset.")
sc("flow", "Here's exactly what a loop does, mechanically, one full cycle at a time. Deposit an asset as collateral. Borrow against it, up to some chosen L.T.V. Use what you borrowed to buy more of the same asset. And re-deposit that, as more collateral, starting the exact same cycle again, one loop deeper each time.",
   chapter="Looping", title="One full loop, step by step",
   nodes=[{"label": "Deposit an asset", "sub": "As collateral", "icon": "coins"}, {"label": "Borrow against it", "sub": "Up to a chosen LTV", "icon": "chart"},
          {"label": "Buy more of the same asset", "sub": "With what you borrowed", "icon": "swap"}, {"label": "Re-deposit it", "sub": "Starting the cycle again, one loop deeper", "icon": "layers"}])
sc("statement", "Here's the formula that falls directly out of repeating that cycle, worth seeing in full before the worked example. After n loops at L.T.V. L, your leverage equals one minus L to the power of n plus one, all divided by one minus L. More loops push you closer and closer to a ceiling; at L.T.V. zero point seven five, that ceiling is exactly four times leverage, no matter how many additional loops you run.",
   chapter="Looping", kicker="The leverage formula", lines=["Leverage = (1 − Lⁿ⁺¹) ÷ (1 − L).", "More loops approach a ceiling — they never exceed it."], sub="At LTV 0.75, that ceiling is exactly 4×, however many loops you run.")
sc("chart", "Plot leverage against the number of loops, at an L.T.V. of zero point seven specifically, and you can watch that ceiling actually being approached. One loop: one point seven times. Three loops: two point five three times, exactly this lesson's worked example. Five loops: two point nine four times. And ten loops: three point two seven times, closing in on, but never quite reaching, the three point three three times ceiling.",
   "Plot leverage against the number of loops, at an LTV of 0.7 specifically, and you can watch that ceiling actually being approached. 1 loop: 1.7x. 3 loops: 2.53x, exactly this lesson's worked example. 5 loops: 2.94x. And 10 loops: 3.27x, closing in on, but never quite reaching, the 3.33x ceiling.",
   chapter="Looping", kind="line", title="Leverage vs number of loops, at LTV 0.7", sub="Approaching, never reaching, the 1 ÷ (1−LTV) ceiling",
   series=[{"values": [1.7, 2.19, 2.53, 2.94, 3.27], "tone": "good"}], xlabels=["1 loop", "2 loops", "3 loops", "5 loops", "10 loops"], yticks=[[1.7, "1.7×"], [3.27, "3.27×"]], ymin=0, ymax=3.6,
   marks=[{"i": 2, "text": "This lesson's worked example", "tone": "good", "below": False}])
sc("quiz", "Quick check. What's the maximum possible leverage from looping at an LTV of 0.75, however many loops you run? [[pause 4]] The answer: four times, exactly one divided by one minus zero point seven five, the ceiling the formula approaches as loops increase, but never exceeds.",
   chapter="Looping", n=2, of=3, q="What's the maximum possible leverage from looping at an LTV of 0.75, however many loops you run?",
   a="4×, the ceiling of 1 ÷ (1 − LTV).")

# ---------------------------------------------------------------- correlated vs volatile
sc("title", "Correlated vs volatile loops.", chapter="Correlated vs volatile", eyebrow="Correlated vs volatile", num="1", title="Why the pairing matters more than the leverage number",
   sub="Same multiple. Very different risk.")
sc("compare", "Here's the actual distinction that decides how dangerous any given loop really is, more than the leverage number alone ever does. A correlated loop, an L.S.T. against its own underlying asset, or one stablecoin against another, moves both sides together, almost in lockstep. A volatile-against-stable loop instead has collateral and debt that can move in completely opposite directions, which is exactly what actually threatens your health factor.",
   chapter="Correlated vs volatile",
   left={"label": "A correlated loop", "tone": "good", "items": ["LST vs its underlying, or stable vs stable", "Collateral and debt move together"]},
   right={"label": "A volatile-against-stable loop", "tone": "bad", "items": ["Collateral and debt can move opposite ways", "This is what actually threatens health factor"]})
sc("statement", "Worth naming concrete examples of each, so “correlated” isn't just an abstract label. A liquid-staking token looped against its own underlying, an L.S.T. of E.T.H. against E.T.H. itself, is a correlated loop; both sides track the same underlying price, closely. E.T.H. looped against U.S.D.C. debt is a volatile-against-stable loop; E.T.H.'s price can move sharply while the U.S.D.C. debt stays exactly flat.",
   chapter="Correlated vs volatile", kicker="Concrete examples of each", lines=["An LST vs its own ETH: correlated.", "ETH collateral, USDC debt: volatile-against-stable."], sub="Not an abstract label — a real difference in what can move.")
sc("statement", "Here's exactly why that correlation matters so directly to your safety, mechanically, not just intuitively. Health factor depends on your collateral's value relative to your debt. If both move together, in the same direction, by roughly the same amount, that ratio barely changes, even at high leverage. If they diverge instead, the exact same leverage multiple becomes dramatically more dangerous, far faster.",
   chapter="Correlated vs volatile", kicker="Why correlation protects health factor", lines=["Both move together: the ratio barely changes.", "They diverge: the same leverage becomes far more dangerous."], sub="Collateral and debt moving together, is the actual safety net.")

# ---------------------------------------------------------------- worked example
sc("title", "Worked example.", chapter="Worked example", eyebrow="Worked example", num="1", title="LTV 0.7, three loops, real numbers",
   sub="Matching this program's own calculator.")
img(CH + "loop-spread.png", "The spread is everything",
    "Here's the one relationship this entire lesson comes down to, visually. A leveraged loop's return depends entirely on the spread between what your collateral earns, and what your borrowed debt costs. Widen that spread, and leverage amplifies a genuinely good return. Narrow it, or let it flip negative, and the exact same leverage amplifies a loss just as fast.",
    chapter="Worked example")
sc("stats", "Here's the setup this entire worked example runs on. L.T.V. zero point seven, three loops, three point five percent collateral yield, two point five percent borrow rate. Run through this program's own calculator, and leverage comes out to two point five three times.",
   "Here's the setup this entire worked example runs on. LTV 0.7, 3 loops, 3.5% collateral yield, 2.5% borrow rate. Run through this program's own calculator, and leverage comes out to 2.53x.",
   chapter="Worked example", stats=[["2.53× leverage", "LTV 0.7, 3 loops, 3.5% yield, 2.5% borrow"]])
sc("steps", "Now the net A.P.Y. on equity, step by step, the formula that actually tells you whether this loop was worth doing. Collateral yield, times leverage: three point five percent, times two point five three, is eight point eight six percent. Borrow rate, times leverage minus one: two point five percent, times one point five three, is three point eight three percent. Subtract the second from the first, and net A.P.Y. on equity is five point zero three percent.",
   chapter="Worked example", title="Net APY on equity, step by step",
   steps=["Collateral yield × leverage: 3.5% × 2.53 = 8.86%", "Borrow rate × (leverage − 1): 2.5% × 1.53 = 3.83%", "Net APY on equity: 8.86% − 3.83% = 5.03%"], result="A real, positive return — at these specific rates")
sc("compare", "Now find the exact point where that positive return actually disappears, since rates don't stay fixed forever. At a two point five percent borrow rate, net A.P.Y. on equity is five point zero three percent, genuinely positive. Raise the borrow rate to five point seven eight percent, with nothing else changed, and that same loop's net return on equity hits exactly zero.",
   chapter="Worked example",
   left={"label": "Borrow rate: 2.5%", "tone": "good", "items": ["Net APY on equity: 5.03%", "The starting scenario"]},
   right={"label": "Borrow rate: 5.78%", "tone": "bad", "items": ["Net APY on equity: 0%", "Return, exactly wiped out"]})
sc("statement", "And here's exactly why that break-even number should worry you, not just interest you, given what Lesson three point one already showed. Borrow rates on a nearly-full pool can jump from around four percent to thirty-four percent, within hours, not months, exactly the kinked-curve mechanism from that same lesson. A loop that looks comfortably profitable today can be underwater by tomorrow morning, with nothing about your own position having changed at all.",
   chapter="Worked example", kicker="Why this break-even number should worry you", lines=["Borrow rates can jump from 4% to 34%, in hours.", "A profitable loop today can be underwater by morning."], sub="Nothing about your own position needs to change at all.")
sc("quiz", "Quick check. What single number actually decides whether a loop is worth doing, more than the leverage multiple itself? [[pause 4]] The answer: the spread between collateral yield and borrow rate. A wide, stable spread makes a loop worthwhile; a narrow or shrinking one erases the return.",
   chapter="Worked example", n=3, of=3, q="What single number actually decides whether a loop is worth doing, more than the leverage multiple itself?",
   a="The spread between collateral yield and borrow rate.")

# ---------------------------------------------------------------- checklist and recap
sc("steps", "Here's how to actually monitor an open loop, ongoing, not just at the moment you set it up. Check the current spread, collateral yield minus borrow rate, on a regular schedule, not only when something feels wrong. Watch for utilisation climbing on the borrow side specifically, since that's the exact signal from Lesson three point one that rates are about to move. And unwind, deliberately, the moment the spread turns negative, rather than waiting to see if it recovers.",
   chapter="Worked example", title="Monitoring an open loop, ongoing",
   steps=["Check the current spread, on a regular schedule", "Watch utilisation on the borrow side specifically", "Unwind deliberately, the moment the spread turns negative"], result="Don't wait to see if a negative spread recovers")
sc("steps", "Here's your checklist. Do it now, before opening any loop. Name your actual repayment source, before you ever borrow, not as an afterthought. Only loop correlated pairs, and stay below the mathematical maximum leverage for your L.T.V. And know your specific break-even borrow rate, with an alert actually set on it, not just calculated once and forgotten.",
   chapter="Checklist", title="Your checklist",
   steps=["Repayment source named, before borrowing", "Loops only on correlated pairs, below max leverage", "Break-even borrow rate known, and alerted"])
sc("statement", "One last honest connection before the recap, tying looping directly back to Lesson three point two. Every loop still carries a health factor, exactly like any other borrow, and the exact same liquidation mechanics from Lesson three point three still apply, on the full, leveraged position, not just the original deposit. Looping doesn't create a new category of risk. It multiplies the familiar one.",
   chapter="Recap", kicker="Looping doesn't create new risk", lines=["The same HF, the same liquidation mechanics.", "On the full leveraged position — not the original deposit."], sub="It multiplies the familiar risk. It doesn't replace it.")
sc("bullets", "Let's recap. Borrowing against an asset gets you liquidity without selling it, a deliberate credit policy, not a reaction. Looping multiplies exposure through repeated deposit-borrow cycles, approaching a leverage ceiling that never exceeds one over one minus L.T.V. Correlated pairs keep health factor stable even at high leverage; volatile-against-stable pairs don't. And the spread between collateral yield and borrow rate, not the leverage number alone, decides whether any given loop was actually worth doing.",
   chapter="Recap", title="Recap", check=False,
   items=["Borrowing: liquidity without selling, a deliberate policy", "Looping: leverage = (1 − Lⁿ⁺¹) ÷ (1 − L), a ceiling, never exceeded",
          "Correlated pairs keep HF stable at leverage; volatile-stable pairs don't", "The spread between yield and borrow rate decides if a loop is worth it"])
sc("cta", "Name your repayment source, loop only correlated pairs, and know your break-even borrow rate before you open anything. Next up, Lesson three point five: Perpetual futures and margin on-chain.",
   "Name your repayment source, loop only correlated pairs, and know your break-even borrow rate before you open anything. Next up, Lesson 3.5: Perpetual futures and margin on-chain.",
   chapter="Recap", button="Next: Lesson 3.5", sub="Perpetual futures and margin on-chain")

spec = {"id": "lesson-03-4", "title": "Lesson 3.4: Borrowing strategies & looping", "size": [1920, 1080], "group": "lessons", "maxMinutes": 25,
        "tag": "Lesson 3.4", "gold": True, "music": True, "musicLevel": 0.14, "seed": 65,
        "use": "Lesson 3.4 page in the Whop course. Hand-written gold-standard script: liquidity without selling, the looping mechanism and leverage formula, correlated vs volatile loops, and the source material's own 2.53x-leverage worked example, as walk-throughs.",
        "thumbnail": {"title": "Borrowing strategies & looping", "subtitle": "Lesson 3.4"}, "scenes": S}
out = ROOT / "video-scripts" / "gold" / "lesson-03-4.json"
out.write_text(json.dumps(spec, indent=1, ensure_ascii=False))
words = sum(len(s["vo"].replace("[[pause 4]]", "").split()) for s in S)
print(f"{len(S)} scenes, {words} words, est {(words / 171 * 60 + len(S) * 1.3 + 4 * 3) / 60:.1f} min")
