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
            "YOU choose the range",
            "YOU choose the gaps",
            "YOU choose the money",
            "YOU write the stop",
            "YOU act on the stop",
            "THE BOT places each order",
            "THE BOT refills one rung up or down",
        ],
    },
    "BP01-V04": {
        "title": "One bounce = one pair",
        "rows": [
            "EXAMPLE. Buy 0.01 bitcoin at 26,730",
            "EXAMPLE. Sell 27,630",
            "Example order",
            "Leaves the range: pairs stop",
        ],
    },
    "BP01-V05": {
        "title": "One pair, after fees",
        "rows": [
            "EXAMPLE. 17 Aug buy 0.01 bitcoin at 26,730 = US$267.30",
            "EXAMPLE. 29 Aug sell 0.01 bitcoin at 27,630 = US$276.30",
            "EXAMPLE. Before fees US$9.00",
            "EXAMPLE. Fees 0.1% + 0.1% = US$0.54",
            "EXAMPLE. After fees, net about US$8.46 (8.4564)",
            "Only if price comes back up. Not a forecast.",
        ],
    },
    "BP01-V06": {
        "title": "The stop, plainly",
        "rows": [
            "EXAMPLE. 23 Oct closing price 33,086. Closing price 1 outside.",
            "EXAMPLE. 24 Oct closing price 33,902. Closing price 2 still outside.",
            "1. Stop the bot. Waiting orders are cancelled.",
            "2. Follow the rule: keep the coin, or swap back to cash.",
            "3. Who: the bot's stop setting, or you by hand.",
            "Two daily closing prices. The second one still outside.",
        ],
    },
    "BP01-V08": {
        "title": "EXAMPLE, made up",
        "rows": [
            "EXAMPLE, made up. Not a real fill.",
            "EXAMPLE. 0.01 bitcoin at 27,630 = US$276.30",
            "EXAMPLE. 0.01 bitcoin at 26,730 = US$267.30",
            "EXAMPLE. 0.01 bitcoin at 25,830 = US$258.30",
            "EXAMPLE. Together US$801.90",
            "EXAMPLE. Made-up price 24,000: worth US$720",
            "EXAMPLE. Down US$81.90 before fees.",
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


def _paint_stall(draw, ui, shot: dict, local: float) -> None:
    """The stall, built in steps, and kept above the lane."""
    box = (ui.MX, 188, ui.RIGHT, ui.CARD_BOTTOM)
    draw.rounded_rectangle(box, 22, fill=ui.GLASS, outline=ui.CYAN, width=2)
    draw.text((box[0] + 36, box[1] + 20), "A market stall", font=ui.font(40), fill=ui.WHITE)
    left, right = box[0] + 280, box[2] - 280
    if local >= 1.5:
        draw.polygon(
            [(left, 360), (left + 70, 280), (right - 70, 280), (right, 360)],
            outline=ui.CYAN,
        )
    if local >= 3.0:
        draw.line([(left, 360), (right, 360)], fill=ui.CYAN, width=4)
        draw.rounded_rectangle([left + 36, 400, right - 36, 490], 10, outline=ui.CYAN, width=3)
    if local >= 4.5:
        draw.line([(left + 100, 490), (left + 100, 520)], fill=ui.CYAN, width=4)
        draw.line([(right - 100, 490), (right - 100, 520)], fill=ui.CYAN, width=4)
    words = shot.get("word_times") or []
    heard = sum(1 for _text, start, _end in words if float(start) <= local)
    frac = heard / max(1, len(words)) if words else 0
    notes = (
        (0.15, "Buys a little cheaper"),
        (0.35, "Sells a little dearer"),
        (0.55, "The stall waits for price"),
        (0.75, "Each rung is one order"),
    )
    y = 540
    due = [line for need, line in notes if frac >= need]
    draw.text((box[0] + 36, 500), "Example amount, explained shortly", font=ui.font(28), fill=ui.CYAN)
    for index, line in enumerate(due):
        latest = index == len(due) - 1
        draw.rounded_rectangle(
            [box[0] + 36, y, box[0] + 720, y + 40], 8,
            fill=ui.CYAN if latest else ui.GLASS, outline=ui.CYAN, width=2,
        )
        draw.text((box[0] + 52, y + 6), line, font=ui.font(28), fill=ui.NAVY if latest else ui.WHITE)
        y += 48


def _summer_closes(ui) -> tuple[list[dict], list[dict]]:
    import json

    data = json.loads((ui.ROOT / "course/data/public-prices/btc-usd-windows.json").read_text())
    inside = list(data["range_2023"])
    outside = [row for row in data["breakout_2023"] if row["date"] in {"2023-10-23", "2023-10-24"}]
    return inside, outside


def _paint_stop_card(draw, shot: dict, local: float, ui) -> None:
    """Notebook, a stop sign, and the real daily closes, a new stretch every 6 seconds."""
    import math

    box = (ui.MX, 176, ui.RIGHT, ui.CARD_BOTTOM)
    draw.rounded_rectangle(box, 18, fill=ui.GLASS, outline=ui.CYAN, width=3)
    draw.text((box[0] + 28, box[1] + 12), "WRITE YOUR STOP DOWN", font=ui.font(32), fill=ui.CYAN)
    # A stop sign, not a notepad sketch. The chart carries Close 1 and Close 2.
    cx, cy, radius = box[0] + 180, box[1] + 170, 78
    points = []
    for index in range(8):
        angle = math.radians(-90 + index * 45 + 22.5)
        points.append((cx + radius * math.cos(angle), cy + radius * math.sin(angle)))
    draw.polygon(points, fill=ui.CYAN)
    draw.line(points + [points[0]], fill=ui.CYAN, width=4)
    draw.text((cx - 36, cy - 16), "STOP", font=ui.font(28), fill=ui.NAVY)
    draw.text((box[0] + 28, box[1] + 268), "Two closing prices outside.", font=ui.font(28), fill=ui.WHITE)
    draw.text((box[0] + 28, box[1] + 308), "Then the stop acts.", font=ui.font(28), fill=ui.CYAN)
    steps = (
        "Write the stop",
        "Before you start",
        "Two closing prices",
        "Still outside",
        "Closing price 1",
        "Closing price 2",
        "You act",
        "The rule holds",
    )
    words = shot.get("word_times") or []
    heard = sum(1 for _text, start, _end in words if float(start) <= local)
    frac = heard / max(1, len(words)) if words else 0
    count = max(1, min(len(steps), int(frac * len(steps)) + 1))
    sy = box[1] + 360
    for line in steps[:count]:
        if sy + 48 > box[3] - 16:
            break
        draw.rounded_rectangle([box[0] + 28, sy, box[0] + 560, sy + 48], 8, fill=ui.CYAN)
        draw.text((box[0] + 40, sy + 10), line, font=ui.font(28), fill=ui.NAVY)
        sy += 56
    inside, outside = _summer_closes(ui)
    october_at = ui._word_at(shot, "october")
    show_out = october_at is not None and local >= october_at
    plot = (box[0] + 620, box[1] + 64, box[2] - 28, box[3] - 28)
    draw.rounded_rectangle(plot, 10, outline=ui.CYAN, width=2)
    lo, hi = 24000, 35000

    def y_of(price: float) -> int:
        span = hi - lo
        return int(plot[3] - 16 - (price - lo) / span * (plot[3] - plot[1] - 32))

    top_y, bot_y = y_of(30331), y_of(24930)
    draw.line([(plot[0] + 12, top_y), (plot[2] - 12, top_y)], fill=ui.CYAN, width=3)
    draw.line([(plot[0] + 12, bot_y), (plot[2] - 12, bot_y)], fill=ui.CYAN, width=3)
    draw.text((plot[2] - 140, top_y - 32), "30,331", font=ui.font(28), fill=ui.CYAN)
    draw.text((plot[2] - 140, bot_y + 8), "24,930", font=ui.font(28), fill=ui.CYAN)
    ui._example(draw, plot[2] - 200, plot[1] + 8)
    # The path grows with the words, not on a clock. No playhead bar.
    words = shot.get("word_times") or []
    heard = sum(1 for _text, start, _end in words if float(start) <= local)
    frac = heard / max(1, len(words)) if words else min(1.0, local / 8.0)
    shown_n = min(len(inside), max(8, int(frac * len(inside))))
    closes = list(inside[:shown_n]) + (list(outside) if show_out else [])
    if len(closes) >= 2:
        step = (plot[2] - plot[0] - 36) / max(1, len(inside) + 2 - 1)
        pts = []
        for index, row in enumerate(closes):
            pts.append((plot[0] + 18 + step * index, y_of(float(row["close"]))))
        draw.line(pts, fill=ui.WHITE, width=5)
        for index, (x, y) in enumerate(pts):
            radius_dot = 8 if show_out and index >= len(pts) - 2 else 4
            draw.ellipse([x - radius_dot, y - radius_dot, x + radius_dot, y + radius_dot], fill=ui.WHITE)
        last = closes[-1]
        months = ["", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        label = f"{int(last['date'][8:10])} {months[int(last['date'][5:7])]}  {round(float(last['close'])):,}"
        if show_out:
            label = "23 Oct 33,086    24 Oct 33,902"
        face = ui.font(28)
        pill_w = min(int(face.getlength(label)) + 28, plot[2] - plot[0] - 16)
        px = plot[0] + 12
        py = plot[1] + 8
        draw.rounded_rectangle([px, py, px + pill_w, py + 36], 8, fill=ui.CYAN)
        draw.text((px + 12, py + 6), label, font=face, fill=ui.NAVY)
        if show_out and len(pts) >= 2:
            # Arrows sit beside the dots, not on them. Labels stay off the 24,930 line.
            for index, (x, y) in enumerate(pts[-2:]):
                label = f"Closing price {index + 1}"
                draw.line([(x - 70, y - 36), (x - 18, y - 8)], fill=ui.CYAN, width=4)
                draw.text((x - 168, y - 52), label, font=ui.font(28), fill=ui.WHITE)


def paint_visual(base, shot: dict, local: float, ui) -> None:
    spec = SPECS.get(shot.get("visual") or "")
    if spec is None:
        raise SystemExit(f"unknown visual {shot.get('visual')}")
    draw = ui.ImageDraw.Draw(base)
    if spec.get("title") == "You and the bot" and shot.get("lesson_id") == "bp-01-introduction":
        # The three choose rows were spoken in the previous shot. They are on
        # this card from the first frame, then the stop rows join the voice.
        labels = [
            (None, "YOU choose the range"),
            (None, "YOU choose the gaps and the money"),
            (None, "THE BOT places each order"),
            ("write the stop", "YOU write the stop"),
            ("you act", "YOU act on the stop"),
            ("one rung", "THE BOT refills one rung up or down"),
            ("does not", "The bot does not decide the stop. You do."),
        ]
        y = 188
        for phrase, label in labels:
            at = ui._phrase_at(shot, phrase) if phrase else 0
            if phrase and (at is None or local < at):
                continue
            draw.rounded_rectangle([ui.MX, y, ui.RIGHT, y + 64], 12, outline=ui.CYAN, width=2)
            draw.text((ui.MX + 28, y + 14), label, font=ui.font(32), fill=ui.WHITE)
            y += 72
        return
    if (shot.get("chapter") or "") == "The stop" and shot.get("lesson_id") == "bp-01-introduction":
        _paint_stop_card(draw, shot, local, ui)
        return
    # The pair rows finish in the top of the card. The bottom-leave line is later.
    if (shot.get("chapter") or "") == "One pair" and shot.get("lesson_id") == "bp-01-introduction":
        bottom_at = ui._word_at(shot, "bottom")
        if bottom_at is not None and local >= bottom_at:
            box = (ui.MX, 200, ui.RIGHT, 700)
            draw.rounded_rectangle(box, 22, fill=ui.GLASS, outline=ui.CYAN, width=3)
            ui._example(draw, box[0] + 36, box[1] + 28)
            left, right = box[0] + 80, box[0] + 980
            draw.line([(left, 340), (right, 340)], fill=ui.CYAN, width=4)
            draw.line([(left, 520), (right, 520)], fill=ui.CYAN, width=4)
            draw.text((right + 16, 324), "Top", font=ui.font(28), fill=ui.CYAN)
            draw.text((right + 16, 504), "Bottom", font=ui.font(28), fill=ui.CYAN)
            draw.line([(left + 40, 420), (left + 220, 480), (left + 400, 560), (left + 560, 640)], fill=ui.WHITE, width=5)
            draw.line([(left + 520, 600), (left + 560, 640), (left + 500, 640)], fill=ui.WHITE, width=5)
            draw.text((left, 250), "Price leaves through the bottom", font=ui.font(36), fill=ui.WHITE)
            if local >= (ui._word_at(shot, "money") or bottom_at):
                draw.text((left, 660), "You still hold the coin. The pair is not finished.", font=ui.font(28), fill=ui.CYAN)
            return
    rows = list(spec["rows"])
    chapter = shot.get("chapter") or ""
    if chapter == "The stop" and shot.get("lesson_id") == "bp-01-introduction":
        october_at = ui._word_at(shot, "october")
        if october_at is None or local < october_at:
            rows = [row for row in rows if "Oct" not in row and "33," not in row]
    if chapter == "How a grid can capture bounces":
        buy_at = ui._phrase_at(shot, "one buy")
        if buy_at is None or local < buy_at:
            _paint_stall(draw, ui, shot, local)
            fee_at = ui._phrase_at(shot, "exchanges charge")
            if fee_at is not None and local >= fee_at:
                # In the lane under the stall, not across the drawing.
                lane = ui.MOTION_LANE
                draw.text((lane[0] + 16, lane[1] + 14), "A fee on each trade", font=ui.font(28), fill=ui.WHITE)
            return
        sell_at = ui._phrase_at(shot, "later sell")
        if sell_at is None or local < sell_at:
            rows = [row for row in rows if "27,630" not in row]
    spans = list(shot.get("sentence_spans") or [])
    shown = len(rows)
    paced = shot.get("lesson_id") == "bp-01-introduction" and chapter == "One pair"
    if spans:
        shown = 1
        step = max(1, len(spans) / max(1, len(rows)))
        for index, (start, _end) in enumerate(spans):
            if local >= start:
                shown = min(len(rows), int(index / step) + 1)
    if paced:
        # Buy row when 17 August is spoken, sell row when 29 August is spoken.
        gates = [
            ui._phrase_at(shot, "17 august"),
            ui._phrase_at(shot, "29 august"),
            ui._phrase_at(shot, "the card shows"),
            ui._phrase_at(shot, "two fees"),
            ui._phrase_at(shot, "that is about"),
        ]
        shown = 0
        for at in gates:
            if at is not None and local >= at:
                shown += 1
            else:
                break
        shown = min(shown, len(rows))
    if chapter == "One pair" and shot.get("lesson_id") == "bp-01-introduction":
        net_at = ui._phrase_at(shot, "that is about")
        if net_at is not None and local >= net_at:
            for index, text in enumerate(rows):
                if text.startswith("EXAMPLE. After fees"):
                    shown = max(shown, index + 1)
    downside_at = None
    if chapter == "Downside" and shot.get("lesson_id") == "bp-01-introduction":
        downside_at = [
            None,
            ui._phrase_at(shot, "276"),
            ui._phrase_at(shot, "26,730"),
            ui._phrase_at(shot, "25,830"),
            ui._phrase_at(shot, "801"),
            ui._phrase_at(shot, "24,000"),
            ui._phrase_at(shot, "81"),
        ]
    y = 286 if chapter == "One pair" and shot.get("lesson_id") == "bp-01-introduction" else 220
    step = 64 if chapter == "One pair" and shot.get("lesson_id") == "bp-01-introduction" else (72 if len(rows) > 6 else 86)
    row_h = 56 if chapter == "One pair" and shot.get("lesson_id") == "bp-01-introduction" else (62 if len(rows) > 6 else 74)
    accent = int(local // 8) % max(1, shown) if paced or chapter == "The stop" else -1
    made_at = ui._phrase_at(shot, "made up") if chapter == "Downside" else None
    if chapter == "Downside" and shot.get("lesson_id") == "bp-01-introduction":
        # One table. Rows appear with the voice. No second diagram.
        table = [
            ("Buy 1", "0.01 at 27,630 = 276.30", ui._phrase_at(shot, "276")),
            ("Buy 2", "0.01 at 26,730 = 267.30", ui._phrase_at(shot, "26,730")),
            ("Buy 3", "0.01 at 25,830 = 258.30", ui._phrase_at(shot, "25,830")),
            ("Total", "801.90", ui._phrase_at(shot, "801")),
            ("At 24,000", "worth 720", ui._phrase_at(shot, "720")),
            ("Down", "81.90", ui._phrase_at(shot, "81")),
        ]
        ui._example(draw, ui.RIGHT - 280, 168)
        draw.text((ui.MX + 28, 188), "Three buys on the way down", font=ui.font(32), fill=ui.WHITE)
        down_at = ui._phrase_at(shot, "you are down")
        # Before the buys, a falling price and a stop. Not a reprint of the caption.
        first_buy = ui._phrase_at(shot, "276")
        if first_buy is None or local < first_buy:
            words = shot.get("word_times") or []
            heard = sum(1 for _text, start, _end in words if float(start) <= local)
            steps = min(5, max(1, 1 + heard // 6))
            left, right = ui.MX + 80, ui.RIGHT - 80
            top, bot = 280, 620
            draw.line([(left, top), (right, top)], fill=ui.CYAN, width=3)
            draw.text((left, top - 36), "Top of the range", font=ui.font(28), fill=ui.CYAN)
            draw.line([(left, bot), (right, bot)], fill=ui.WHITE, width=4)
            draw.text((left, bot + 8), "Stop", font=ui.font(32), fill=ui.WHITE)
            pts = []
            for index in range(steps):
                px = left + 40 + (right - left - 80) * index / 4
                py = top + 30 + (bot - top - 50) * index / 4
                pts.append((px, py))
            if len(pts) >= 2:
                draw.line(pts, fill=ui.WHITE, width=4)
            if pts:
                px, py = pts[-1]
                draw.ellipse([px - 8, py - 8, px + 8, py + 8], fill=ui.CYAN)
            return
        y = 240
        latest = None
        for name, value, at in table:
            if name == "Down":
                at = down_at or at
            if at is not None and local >= at:
                latest = name
        for name, value, at in table:
            if name == "Down":
                at = down_at or at
            if at is None or local < at:
                break
            hot = name == latest
            draw.rounded_rectangle(
                [ui.MX, y, ui.RIGHT, y + 56], 12,
                fill=ui.CYAN if hot else ui.GLASS, outline=ui.CYAN, width=2,
            )
            ink = ui.NAVY if hot else ui.CYAN
            draw.text((ui.MX + 28, y + 12), name, font=ui.font(32), fill=ink)
            draw.text((ui.MX + 280, y + 12), "EXAMPLE  " + value, font=ui.font(32), fill=ui.NAVY if hot else ui.WHITE)
            y += 64
        if local >= (ui._phrase_at(shot, "0.03") or 10**9):
            draw.text((ui.MX + 28, y + 8), "0.03 BTC × $24,000 = $720", font=ui.font(32), fill=ui.CYAN)
        return
    visible = [text for text in rows[:shown] if not (chapter == "Downside" and text.startswith("EXAMPLE, made up") and (made_at is None or local < made_at))]
    if any(ch.isdigit() for text in visible for ch in text):
        ui._example(draw, ui.RIGHT - 280, 168)
    start_row = 0
    one_pair = chapter == "One pair" and shot.get("lesson_id") == "bp-01-introduction"
    formula_on = False
    fee_line_on = False
    if one_pair:
        gross_at = ui._phrase_at(shot, "900 dollars")
        fee_spoken = ui._phrase_at(shot, "two fees") or ui._phrase_at(shot, "the card shows")
        formula_on = gross_at is not None and local >= gross_at
        fee_line_on = fee_spoken is not None and local >= fee_spoken
        if shown == 0 and not formula_on:
            draw.rounded_rectangle([ui.MX, 220, ui.RIGHT, 420], 16, outline=ui.CYAN, width=3)
            draw.text((ui.MX + 36, 250), "Buy lower", font=ui.font(40), fill=ui.CYAN)
            draw.text((ui.MX + 36, 320), "Sell higher. One pair.", font=ui.font(40), fill=ui.WHITE)
            return
        extras = (1 if formula_on else 0) + (1 if fee_line_on else 0)
        start_row = max(0, shown - max(1, 4 - extras))
        ui._example(draw, ui.RIGHT - 280, 168)
    for index, text in enumerate(rows[:shown]):
        if index < start_row:
            continue
        if chapter == "Downside" and text.startswith("EXAMPLE, made up") and (made_at is None or local < made_at):
            y += step
            continue
        if downside_at is not None and index > 0:
            at = downside_at[index] if index < len(downside_at) else None
            if at is None or local < at:
                break
        outline = ui.WHITE if index == accent else ui.CYAN
        draw.rounded_rectangle(
            [ui.MX, y, ui.RIGHT, y + row_h], 14, fill=ui.GLASS, outline=outline, width=4 if index == accent else 2,
        )
        size = 32 if ui.font(32).getlength(text) < (ui.W - 2 * ui.MX - 80) else 28
        draw.text((ui.MX + 28, y + 14), text, font=ui.font(size), fill=ui.WHITE)
        y += step
        if y > 700:
            break
    if y + 84 < 620 and shot.get("lesson_id") in {"bp-01-introduction", "bp-02-what-you-need"}:
        steps = (
            "EXAMPLE 24,930", "EXAMPLE 26,730", "EXAMPLE 27,630", "EXAMPLE 28,531",
            "EXAMPLE 30,331", "EXAMPLE gap 900", "EXAMPLE 0.01", "EXAMPLE fee 0.1%",
        )
        words = shot.get("word_times") or []
        heard = sum(1 for _text, start, _end in words if float(start) <= local)
        label = steps[(heard // 5) % len(steps)]
        draw.text((ui.MX + 36, y + 8), label, font=ui.font(72), fill=ui.WHITE)
    if chapter == "How a grid can capture bounces" and any("26,730" in text for text in rows[:shown]):
        draw.text((ui.MX + 28, 620), "26,730 = 24,930 + 900 + 900", font=ui.font(28), fill=ui.CYAN)
    if one_pair:
        # At most four lines, counting the formula and the fee basis.
        if formula_on:
            draw.rounded_rectangle([ui.MX, 188, ui.RIGHT, 236], 10, fill=ui.GLASS, outline=ui.CYAN, width=2)
            draw.text((ui.MX + 24, 198), "gap × coin size = gross:  $900 × 0.01 = $9.00", font=ui.font(32), fill=ui.WHITE)
        if fee_line_on:
            draw.text(
                (ui.MX + 24, 560),
                "0.1% of $267.30 = $0.2673; 0.1% of $276.30 = $0.2763; total $0.5436 ≈ $0.54",
                font=ui.font(28),
                fill=ui.CYAN,
            )
        return
