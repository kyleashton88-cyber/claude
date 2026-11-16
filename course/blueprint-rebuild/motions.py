"""Code-drawn motion, card and screen visuals for BP-01 to BP-11.

Navy, cyan and white only. Every figure on these cards is an EXAMPLE.
"""

from __future__ import annotations

# Imported lazily from studio to avoid a cycle. studio calls paint_visual.


def visual_ids() -> list[str]:
    return list(SPECS)


SPECS: dict[str, dict] = {
    "BP01-V03": {
        "title": "You and the bot",
        "rows": [
            "YOU choose the band",
            "YOU choose the gaps",
            "YOU choose the money",
            "YOU write the stop",
            "YOU act on the stop",
            "THE BOT places each order",
            "THE BOT refills one rung away",
        ],
    },
    "BP01-V04": {
        "title": "One bounce = one pair",
        "rows": [
            "EXAMPLE. Buy 26,730",
            "EXAMPLE. Sell 27,630",
            "Pairs on these closes: 1, then 2, then 3",
            "Illustration, not the real order of fills",
            "Leaves the band: pairs stop",
        ],
    },
    "BP01-V05": {
        "title": "One pair, after fees",
        "rows": [
            "EXAMPLE. 17 Aug buy 0.01 BTC at 26,730 = US$267.30",
            "EXAMPLE. 29 Aug sell 0.01 BTC at 27,630 = US$276.30",
            "EXAMPLE. Gross US$9.00",
            "EXAMPLE. Fees 0.1% + 0.1% = US$0.54",
            "EXAMPLE. Net about US$8.46",
            "Only if price comes back up. Not a forecast.",
        ],
    },
    "BP01-V06": {
        "title": "The stop, plainly",
        "rows": [
            "EXAMPLE. 23 Oct close 33,086. Close 1 outside.",
            "EXAMPLE. 24 Oct close 33,902. Close 2 still outside.",
            "1. Stop the bot. Waiting orders are cancelled.",
            "2. Follow the rule: keep the coin, or swap back to cash.",
            "3. Who: the bot's stop setting, or you by hand.",
            "Daily close: 11am AEDT, or 10am outside daylight saving.",
        ],
    },
    "BP02-V01": {
        "title": "Account steps",
        "rows": [
            "1. ID check",
            "2. Check AUSTRAC registration",
            "3. Deposit A$",
            "4. Turn on 2FA",
            "No exchange name. No balance.",
        ],
    },
    "BP02-V03": {
        "title": "Fees: the round trip",
        "rows": [
            "EXAMPLE. A$100 buy x 0.1% = A$0.10",
            "EXAMPLE. A$100 sell x 0.1% = A$0.10",
            "EXAMPLE. Round trip about A$0.20, which is 0.2%",
            "A gap under 0.2% loses before price moves.",
        ],
    },
    "BP02-V05": {
        "title": "Page first, screen later",
        "rows": [
            "Your page is written first.",
            "The screen only copies the page.",
            "EXAMPLE pair on this card: BTC/USD. The A$ fee example is a different card.",
        ],
    },
    "BP03-V01": {
        "title": "The grid cycle",
        "rows": [
            "Buy fills, then a sell is placed one rung above.",
            "Sell fills, then a buy is placed one rung below.",
            "Completed pairs count only when both have filled.",
        ],
    },
    "BP03-V02": {
        "title": "Settings a bot asks for",
        "rows": [
            "Upper",
            "Lower",
            "Number of grids",
            "Amount",
            "Order size",
        ],
    },
    "BP03-V03": {
        "title": "Order size",
        "rows": [
            "EXAMPLE. A$600 across 6 orders",
            "EXAMPLE. A$100 per order",
        ],
    },
    "BP03-V04": {
        "title": "Inventory moves",
        "rows": [
            "Two buys fill: more coin, less cash.",
            "One sell fills: one completed pair.",
            "One coin parcel is still waiting for its sell.",
            "EXAMPLE. Not a profit.",
        ],
    },
    "BP04-V01": {
        "title": "How to sort a path",
        "rows": [
            "Count how often the close touches the band.",
            "Are the highs getting higher?",
            "Write one label and one reason.",
        ],
    },
    "BP04-V02": {
        "title": "What the grid does",
        "rows": [
            "Range: pairs can finish.",
            "Trend: you are left holding one side.",
            "Break: the stop is the rule.",
        ],
    },
    "BP04-V03": {
        "title": "Volatility and the gap",
        "rows": [
            "A wide day needs a gap that still clears the fees.",
            "EXAMPLE. Compare the day's move with the gap.",
        ],
    },
    "BP04-V04": {
        "title": "Three real windows",
        "rows": [
            "EXAMPLE. Summer 2023: a range.",
            "EXAMPLE. October 2023: a leave.",
            "EXAMPLE. March 2020: a break.",
        ],
    },
    "BP05-V01": {
        "title": "Two ways to space",
        "rows": [
            "Arithmetic = the same dollars.",
            "EXAMPLE. 100, 125, 150, 175, 200.",
            "Geometric = the same percent.",
            "EXAMPLE. 100, 118.9, 141.4, 168.2, 200.",
        ],
    },
    "BP05-V02": {
        "title": "Net per pair",
        "rows": [
            "EXAMPLE. 0.5% gap on A$100: +A$0.50, fees A$0.20, net +A$0.30. Passes.",
            "EXAMPLE. 0.15% gap: +A$0.15, fees A$0.20, net -A$0.05. Fails.",
        ],
    },
    "BP05-V03": {
        "title": "More lines or fewer",
        "rows": [
            "Many lines can mean more pairs. This summer window finished only three one-step pairs.",
            "Few lines: fewer, wider pairs.",
            "Both still pay the fee.",
        ],
    },
    "BP05-V04": {
        "title": "Leave room for the wicks",
        "rows": [
            "The band has to hold the real high and the real low.",
            "EXAMPLE. Summer band 24,930 to 30,331.",
        ],
    },
    "BP05-V05": {
        "title": "Order size and the minimum",
        "rows": [
            "EXAMPLE. A$2,000 across 20 orders = A$100.",
            "EXAMPLE. Exchange minimum A$10. This order clears it.",
        ],
    },
    "BP06-V01": {
        "title": "Trigger, then confirmation",
        "rows": [
            "Close 1 outside the band.",
            "Close 2 still outside.",
            "Then the written rule applies.",
        ],
    },
    "BP06-V03": {
        "title": "Up break and down break",
        "rows": [
            "Leave through the top: mostly cash.",
            "Leave through the bottom: mostly coin.",
            "The rule you wrote names the action.",
        ],
    },
    "BP06-V04": {
        "title": "Know your loss first",
        "rows": [
            "EXAMPLE. A$2,000 in the bot.",
            "EXAMPLE. Loss at the stop about A$249.",
            "You write that number before you start.",
        ],
    },
    "BP07-V01": {
        "title": "The form copies the page",
        "rows": [
            "The form calls it upper. Your page calls it the top.",
            "The form calls it lower. Your page calls it the bottom.",
            "Copy only what the page already says.",
        ],
    },
    "BP07-V04": {
        "title": "Two-week paper journal",
        "rows": [
            "EXAMPLE. 14 days.",
            "Every check written.",
            "Fees written. Rules followed: yes or no.",
        ],
    },
    "BP07-V05": {
        "title": "Graduation rule",
        "rows": [
            "EXAMPLE. At least 14 days.",
            "Every check on time. Journal complete. No rule broken.",
            "Then the smallest size your rule allows.",
        ],
    },
    "BP08-V02": {
        "title": "The review record",
        "rows": [
            "Realised. Unrealised. Fees.",
            "Rules followed: yes or no.",
            "A review record. Not a profit target.",
        ],
    },
    "BP08-V03": {
        "title": "Drawdown",
        "rows": [
            "Drawdown is the fall from a peak to a later low.",
            "EXAMPLE. You write the limit before you start.",
        ],
    },
    "BP08-V05": {
        "title": "Records for tax",
        "rows": [
            "A swap can be a CGT event.",
            "Keep the journal. This is general information.",
            "Check ATO guidance or a registered tax agent.",
        ],
    },
    "BP09-V01": {
        "title": "Grid in a trend",
        "rows": [
            "Price keeps leaving in one direction.",
            "Pairs stop finishing.",
            "You are left holding one side.",
        ],
    },
    "BP09-V02": {
        "title": "Gaps under the fees",
        "rows": [
            "EXAMPLE. Gap A$0.15. Fees A$0.20.",
            "The pair loses before price does anything.",
        ],
    },
    "BP09-V03": {
        "title": "Oversizing",
        "rows": [
            "EXAMPLE. A$10,000 account.",
            "60% in one bot. Loss at stop about A$750.",
            "That is 7.5% of the account, not the cap.",
        ],
    },
    "BP09-V04": {
        "title": "Do not chase the band",
        "rows": [
            "Moving the band to follow price is chasing.",
            "The rungs wait. You do not drag them.",
        ],
    },
    "BP10-V01": {
        "title": "What scaling means here",
        "rows": [
            "Scaling means growing the money given to bots.",
            "Step by step. Under written rules.",
            "Never a promise of results.",
        ],
    },
    "BP10-V02": {
        "title": "Two sizing caps",
        "rows": [
            "EXAMPLE. A$10,000 account.",
            "One bot at most 20% = A$2,000.",
            "Loss at stop at most 2.5% = A$250.",
            "EXAMPLE. A$2,000 bot, loss about A$249. Fits.",
        ],
    },
    "BP10-V04": {
        "title": "A step that fails the cap",
        "rows": [
            "EXAMPLE. Plus 25% makes a A$2,500 bot.",
            "That is 25% of a A$10,000 account, so the 20% share cap fails too.",
            "Loss at stop about A$311, which is 3.1%. The loss cap is 2.5%.",
            "The share cap binds first: wait until the account is about A$12,500.",
            "The rule decides, not the feeling.",
        ],
    },
    "BP10-V05": {
        "title": "Many bots, one risk cap",
        "rows": [
            "EXAMPLE. Total risk at most 6% = A$600.",
            "Correlated means they rise and fall together, so they count as one bucket.",
            "Two separate bots use about A$498, which stays under A$600.",
        ],
    },
    "BP10-V06": {
        "title": "When you scale down",
        "rows": [
            "EXAMPLE. Peak A$10,600 to A$9,540 is a 10% fall.",
            "At 10%, halve every bot.",
            "At 15%, stop the bots and return to paper.",
        ],
    },
    "BP10-V07": {
        "title": "The scaling ladder",
        "rows": [
            "Paper",
            "Small real bot",
            "Review passed",
            "One step up",
            "A second bot that does not move with the first",
            "A drawdown limit steps you back down",
        ],
    },
    "BP11-V01": {
        "title": "13 March 2020, closes only",
        "rows": [
            "EXAMPLE. Close 5,564.",
            "The high and the low are on the candle, not on a close line.",
            "A spot holding is not a liquidation.",
        ],
    },
    "BP11-V03": {
        "title": "Your complete plan",
        "rows": [
            "Band, gaps, stop, journal.",
            "Paper until the graduation rule passes.",
            "Weekly check. Scale only by the written caps.",
        ],
    },
    "BP11-V04": {
        "title": "Explain it back",
        "rows": [
            "What a grid does.",
            "Why a pair can keep the gap after fees.",
            "What you do when price leaves.",
            "How you would add money, and when you would not.",
        ],
    },
    "BP11-V05": {
        "title": "Blueprint complete",
        "rows": [
            "Paper until your graduation rule passes.",
            "Weekly check. Journal.",
            "Scale only by written rules.",
        ],
    },
}


def paint_visual(base, shot: dict, local: float, ui) -> None:
    spec = SPECS.get(shot.get("visual") or "")
    if spec is None:
        raise SystemExit(f"unknown visual {shot.get('visual')}")
    draw = ui.ImageDraw.Draw(base)
    rows = list(spec["rows"])
    spans = list(shot.get("sentence_spans") or [])
    shown = len(rows)
    if spans:
        shown = 1
        step = max(1, len(spans) / max(1, len(rows)))
        for index, (start, _end) in enumerate(spans):
            if local >= start:
                shown = min(len(rows), int(index / step) + 1)
    ui._example(draw, ui.RIGHT - 220, 188)
    y = 210
    for index, text in enumerate(rows[:shown]):
        draw.rounded_rectangle([ui.MX, y, ui.RIGHT, y + 78], 14, fill=ui.GLASS, outline=ui.CYAN, width=2)
        size = 36 if ui.font(36).getlength(text) < (ui.W - 2 * ui.MX - 80) else 28
        draw.text((ui.MX + 28, y + 18), text, font=ui.font(size), fill=ui.WHITE)
        y += 90
        if y > 760:
            break
