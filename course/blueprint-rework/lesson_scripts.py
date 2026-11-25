"""Blueprint lessons built around one public Bitcoin path.

House example: daily closes from 19 July 2023 to 16 October 2023.
Low 24,930. High 30,331. Six gaps of about 900.
The path leaves that high on 23 October 2023.
A second window, March to June 2024, is the later page.
12–13 March 2020 is the crash used for liquidation, as a public price path only.
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PRICES = json.loads((ROOT / "course/data/public-prices/btc-usd-windows.json").read_text())
MONTHS = ["", "January", "February", "March", "April", "May", "June",
          "July", "August", "September", "October", "November", "December"]

SUMMER = "range_2023"
RALLY = "breakout_2023"
CRASH = "crash_2020"
LATER = "second_range_2024"
LOW, HIGH = 24930, 30331
LEVELS = [24930, 25830, 26730, 27630, 28531, 29431, 30331]


def pretty(iso: str) -> str:
    y, m, d = iso.split("-")
    return f"{int(d)} {MONTHS[int(m)]} {y}"


def _band_levels(lo: float, hi: float, gaps: int = 6) -> list[int]:
    """Equal gaps across one window's own high and low. Not the summer rungs."""
    lo_i, hi_i = int(round(lo)), int(round(hi))
    step = (hi_i - lo_i) / gaps
    levels = [int(round(lo_i + i * step)) for i in range(gaps + 1)]
    levels[0], levels[-1] = lo_i, hi_i
    return levels


def _window_levels(chart: str) -> list[int]:
    series = PRICES[chart]
    return _band_levels(min(row["low"] for row in series), max(row["high"] for row in series))


def _shot(**kwargs) -> dict:
    kwargs.setdefault("kind", "chart")
    kwargs.setdefault("chart", SUMMER)
    if "levels" not in kwargs:
        chart = kwargs.get("chart")
        if chart == SUMMER:
            kwargs["levels"] = LEVELS
        elif chart == LATER:
            kwargs["levels"] = _window_levels(LATER)
        else:
            # A later rally or the 2020 drop is not the summer grid.
            kwargs["levels"] = []
    kwargs.setdefault("chart_title", "19 July 2023 to 16 October 2023")
    kwargs.setdefault("reveal", 1.0)
    kwargs.setdefault("reveal_from", 0.0)
    return kwargs


def walk(chart: str, chapter: str, every: int, band: tuple[float, float] | None, title: str) -> list[dict]:
    """Move the playhead along the real closes and teach one fact at each stop."""
    series = PRICES[chart]
    idxs = list(range(0, len(series), every))
    if idxs[-1] != len(series) - 1:
        idxs.append(len(series) - 1)
    shots = []
    prev = 0.0
    for n, i in enumerate(idxs):
        row = series[i]
        reveal = i / (len(series) - 1)
        close = int(round(row["close"]))
        high = int(round(row["high"]))
        low = int(round(row["low"]))
        day_span = high - low
        levels = LEVELS if chart == SUMMER else (_window_levels(chart) if chart == LATER else [])
        bits = [
            f"On {pretty(row['date'])}, the public daily close was {close}.",
        ]
        if band:
            lo_i, hi_i = int(band[0]), int(band[1])
            if lo_i <= close <= hi_i:
                bits.append(f"The close is inside the band of {lo_i} to {hi_i}.")
            else:
                bits.append(
                    f"The close is outside the band of {lo_i} to {hi_i}. "
                    "A close outside, confirmed by the next close, is when the stop sentence applies."
                )
        if levels:
            nearest = min(levels, key=lambda lv: abs(lv - close))
            middle = levels[len(levels) // 2]
            gap = max(1, levels[1] - levels[0])
            side = "above" if close >= middle else "below"
            bits.append(f"The nearest example rung on this window is {nearest}. The close is {side} the middle line.")
            if day_span > gap:
                bits.append(
                    f"The day's own range was {day_span} dollars, wider than one gap on this window. "
                    "A single quiet day is not the whole band."
                )
            else:
                bits.append(
                    f"The day's own range was {day_span} dollars, inside one gap on this window. "
                    "The gap is a property of this window, not of this one day."
                )
        bits.append("Point at the playhead, say the close, and do not turn it into a result.")
        shots.append(_shot(
            kind="chart",
            chart=chart,
            chapter=chapter,
            chart_title=title,
            reveal_from=prev,
            reveal=max(reveal, prev + 0.01),
            vo=" ".join(bits),
            caption=f"{pretty(row['date'])}. Close {close:,}.",
            levels=levels,
            focus_price=(min(levels, key=lambda lv: abs(lv - close)) if levels else None),
            focus_label=(f"{min(levels, key=lambda lv: abs(lv - close)):,}" if levels else ""),
            pin_date=row["date"],
            pin_close=close,
        ))
        prev = reveal
    return shots


def legal(chapter: str = "Disclaimer") -> dict:
    return _shot(
        kind="legal",
        chapter=chapter,
        vo=(
            "Education only. Not financial advice. This is general information and doesn't consider your objectives, financial situation or needs. "
            "Crypto is high risk; you could lose all the money you put in. "
            "Past performance is not a reliable indicator of future results. "
            "The prices are public historical daily closes, marked Example. "
            "No order is sent from this lesson."
        ),
        caption="Education only. Not financial advice. Chart: historical BTC prices, EXAMPLE.",
        chart=SUMMER,
    )


def ident(number: str, title: str) -> dict:
    return _shot(
        kind="ident",
        chapter="GridBot Blueprint",
        vo=f"GridBot Blueprint, lesson {number}, {title}.",
        caption=f"Lesson {number}. {title}.",
    )


def outro(next_title: str | None, next_skill: str | None = None) -> dict:
    if next_title:
        skill = next_skill or f"use what {next_title} adds."
        vo = (
            f"Next lesson: {next_title}. Bring your notes: your band, your gaps and your stop rule. "
            "Keep the word Example on every practice figure. "
            f"Next lesson you will {skill}"
        )
        caption = next_title
    else:
        vo = (
            "This is the end of the Blueprint. Bring your notes: your band, your gaps and your stop rule. "
            "Keep the word Example on every practice figure. "
            "The spot page can stand on its own."
        )
        caption = "End of the Blueprint."
    return _shot(kind="outro", chapter="Next", vo=vo, caption=caption, reveal=1)


def stack(chapter: str, items: list[str], lead: str) -> list[dict]:
    lines = list(items)
    if lead:
        lines[0] = f"{lead} {items[0]}".strip()
    shots = []
    for i, line in enumerate(lines):
        # The card and the voice are the same sentence.
        shots.append(_shot(
            kind="stack",
            chapter=chapter,
            vo=line,
            caption=line,
            items=lines,
            index=i,
        ))
    return shots


def build(sid: str) -> list[dict]:
    if sid.startswith("el-"):
        raise SystemExit(f"refusing Elite id {sid}")
    shots = BUILDERS[sid]()
    if any(shot.get("canonical") for shot in shots):
        return shots
    if sid != "bp-01-introduction":
        path = Path(__file__).with_name("curriculum_expand.py")
        spec = importlib.util.spec_from_file_location("curriculum_expand", path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        shots = mod.insert(sid, shots)
    return shots


def bp01() -> list[dict]:
    """One flow. No second hook. No fence. Target about 12:30."""

    def gloss(chapter, vo, caption, term, defin, **extra):
        kind = extra.pop("kind", "stack")
        shot = _shot(kind=kind, chapter=chapter, vo=vo, caption=caption, items=[caption], index=0, **extra)
        shot["term_text"] = term
        shot["definition_text"] = defin
        return shot

    s = [ident("01", "Introduction")]
    s.append(gloss(
        "Hook",
        "By the end of this series you will understand what a grid bot does. It is a small program that places these orders for you. You will learn when it can capture bounces, and where it loses. You will know how to plan one, test it on paper, run it, check it, and change the capital you give to bots only under written risk rules. This is education, not a promise of results. "
        "Price often moves sideways, bouncing between the same top and bottom instead of leaving. A grid is a ladder of waiting orders, called limit orders, built for that bouncing. When price runs one way and stays there, the grid has nothing left to do. And if price falls through the bottom, coin means the crypto itself, and you are left holding the coin, and it is worth less.",
        "Plan, test, run, check, and change capital only under written rules.",
        "The promise",
        "Education about grids under written rules. Not a promise of results.",
    ))
    s += stack("Objectives", [
        "By the end you will know what a grid bot places.",
        "You will see that idea on one real path from 2023.",
        "You will be able to say the stop rule in one sentence.",
    ], "")
    s.append(gloss(
        "Example",
        "When a chart says Example, it means a real past price used as an example, not a forecast.",
        "Example: a real past price, not a forecast.",
        "Example",
        "A real past price used as an example, not a forecast.",
    ))
    s.append(gloss(
        "Crypto",
        "Crypto is a digital asset, such as bitcoin. You do not need to have bought any before this lesson.",
        "Crypto is a digital asset, such as bitcoin.",
        "Crypto",
        "A digital asset, such as bitcoin.",
    ))
    s.append(gloss(
        "Exchange",
        "An exchange is the website or app where you swap Australian dollars for crypto, and crypto back to dollars. This course does not name one, and it does not send an order.",
        "An exchange is where you swap dollars and crypto.",
        "Exchange",
        "The website or app where you swap Australian dollars for crypto and back.",
    ))
    s.append(gloss(
        "Cash and coin",
        "Cash is money you can spend. Here that means dollars, or a stablecoin, a crypto coin built to stay at one US dollar. We treat it like cash in this lesson, but it can drop below a dollar. Coin is the crypto, such as bitcoin.",
        "Cash is money you can spend. Coin is the crypto.",
        "Cash and coin",
        "A stablecoin, a crypto coin built to stay at one US dollar. We treat it like cash in this lesson, but it can drop below a dollar.",
    ))
    s.append(gloss(
        "Buy and sell",
        "An order is an instruction to buy or sell. A buy order swaps cash for coin. A sell order swaps coin back to cash, and you can only sell coin you already hold, on a spot account. A spot account is the normal account on an exchange. You own the coin you buy, and nothing is borrowed.",
        "Buy swaps cash for coin. Sell needs coin you already hold, on a spot account.",
        "Buy and sell",
        "A buy swaps cash for coin. A sell swaps coin for cash, and you can only sell coin you already hold, on a spot account.",
    ))
    s.append(gloss(
        "The idea",
        "A bot is software that places and refills orders for you. You start with some cash and some coin, so there is something to buy with and something to sell. A grid bot places waiting buy orders on lines below the current price and sell orders on lines above it, inside a top and a bottom you choose. The space between your top and your bottom is called the range. The sells need some coin, so a grid starts with part cash and part coin, and that is a description, not advice about what to hold.",
        "Buys below, sells above, inside a range you choose.",
        "Range",
        "The top and the bottom you choose. Also called the range.",
    ))
    s.append(gloss(
        "Limit order",
        "A limit order is an order that waits at a price you choose. It does not chase the price. Chasing the price would mean moving the order to follow wherever the price has gone.",
        "A limit order waits. It does not chase the price.",
        "Limit order",
        "An order that waits at a price you choose.",
    ))
    s.append(gloss(
        "Fill",
        "An order fills when the price reaches its line and the trade happens. Until then, the order is only waiting.",
        "A fill is the trade at the line.",
        "Fill",
        "The order's trade happens at its line.",
    ))
    s.append(_shot(
        kind="analogy", analogy="ladder", chapter="A ladder",
        reveal=1,
        levels=[LOW, HIGH],
        vo=(
            "Think of a ladder leaned on a wall. The rungs wait, and they do not chase you. "
            "A rung is one price where an order waits. The gap is the space between two rungs. "
            "The ladder is the analogy, and the chart beside it is the real past path."
        ),
        caption="The rungs wait. The chart is the real past path.",
        term_text="Rung",
        definition_text="A price where an order waits. The gap is the space between two rungs.",
    ))
    s.append(gloss(
        "The three parts",
        "The range is the top rung and the bottom rung. The levels are the rungs between them. The stop is the written rule for leaving.",
        "Range, levels, and stop.",
        "Range",
        "The top rung and the bottom rung of the range.",
    ))
    s.append(_shot(
        chapter="The range",
        reveal=1,
        focus_price=HIGH, focus_label="Top line",
        vo=(
            "The range is the top line and the bottom line, taken from the path. "
            "Hindsight: this range is drawn after the fact. "
            "The chart is bitcoin's real daily closing prices from 19 July to 16 October 2023. "
            "Every closing price in this window stayed between those two lines."
        ),
        caption="The top line and the bottom line, taken from the path. Bottom 24,930. Top 30,331.",
        levels=[LOW, HIGH],
        term_text="Range",
        definition_text="The top line and the bottom line, taken from the path.",
    ))
    s.append(_shot(
        chapter="The levels",
        reveal=1,
        vo=(
            "Six gaps of about 900 dollars each sit between the bottom line and the top line. "
            "Each gap is about 900 dollars: the top line minus the bottom line, divided by six. It is one step between lines, not the whole range. "
            "Seven lines make those six gaps. The levels are the prices on the rungs where limit orders wait."
        ),
        caption="Seven lines. Six gaps of about 900.",
        term_text="Gap",
        definition_text="The space between two lines. About 900 dollars in this example, which is the range divided by six.",
    ))
    s.append(gloss(
        "Buys and sells",
        "Buy orders wait on lines below the current price. Sell orders wait on lines above it. Each fill changes what you hold: a buy fill adds coin, and a sell fill adds cash. You choose the range, the gaps and the money. The bot places each order.",
        "Buys wait below. Sells wait above.",
        "Bot",
        "Software that places the orders for you, and refills one after a fill.",
    ))
    s.append(gloss(
        "Bot and you",
        "After a fill, the bot places the opposite order one rung up or down. A buy fill gets a sell one rung higher. A sell fill gets a buy one rung lower. You still write the stop, and you act when that rule is met. The bot does not decide the stop for you unless you turned that setting on, and you write which one before you start.",
        "You choose the rules. The bot places the orders.",
        "Bot and you",
        "You choose the range, the gaps, the money and the stop. The bot places and refills orders.",
        visual="BP01-V03",
    ))
    s.append(gloss(
        "How a grid can capture bounces",
        "Think of a market stall. The stallholder buys stock a little cheaper and sells it a little dearer, and pays a fee on every sale. Exchanges charge a small fee on each trade. A grid can do that while price bounces inside the range. A bounce means price moves down and back up, or up and back down, and stays inside. One buy at a lower line and the later sell of that same coin is one pair. On these daily closing prices, the July to October example window finished only three pairs, each a buy and a sell on lines next to each other. The sell line is higher, so the cash that comes back is more than the cash that left, before the fee. A fee is what the exchange charges when an order fills. The fees come out of what the pair makes. If the fees are larger than that, the pair keeps nothing. This is not a promise. The pair finishes only if price does bounce and both orders fill.",
        "A pair keeps the gap only after fees, and only on a bounce.",
        "Fee",
        "What the exchange charges when an order fills. It comes out of the gap.",
        visual="BP01-V04",
    ))
    s.append(_shot(
        chapter="One day",
        chart_title="One day inside the range",
        candle={"high": 30184, "low": 29794, "close": 29914, "date": "19 July 2023"},
        vo=(
            "The daily closing price is the last price of the day. Crypto trades all day, so the day is cut at a set time. "
            "This lesson uses the end of each UTC day, the world's standard clock, which is 11am Sydney time in daylight saving, 10am otherwise. "
            "This is a simple candle that shows the day's high, low and closing price. "
            "Traders call it a candle because the full version has a thick body and a thin wick, like a candle. Here we only need the high, the low and the closing price. "
            "This candle is 19 July 2023. The high, the low, and the closing price are labelled."
        ),
        caption="19 July 2023. Closing price 29,914. This lesson uses the end of each UTC day, the world's standard clock, which is 11am Sydney time in daylight saving, 10am otherwise.",
        term_text="Daily closing price",
        definition_text="The last price of the day. This lesson uses the end of each UTC day, the world's standard clock, which is 11am Sydney time in daylight saving, 10am otherwise.",
    ))
    s.append(_shot(
        chapter="The whole window",
        chart_title="19 July 2023 to 16 October 2023",
        reveal=1,
        vo=(
            "The example is Bitcoin's public daily price in US dollars. "
            "From 19 July 2023 to 16 October 2023, every one of those days closed inside the range. "
            "The closing price crossed the seven lines 28 times in that window. The count is an example, not a forecast. "
            "We do not need to read each day. The shape is the lesson, and it is marked Example. "
            "Worked check: 19 July 2023 to 16 October 2023. The low is the bottom line. The high is the top line. Nothing on this card is an order."
        ),
        caption="Every closing price stayed inside the range.",
        levels=[LOW, HIGH],
        term_text="Example",
        definition_text="A real past price used for practice. Not a live trade and not a forecast.",
    ))
    s.append(gloss(
        "Crossings",
        "Those 28 crossings, each time the price crosses a line, are not 28 results. A crossing only means the closing price moved from one side of a line to the other. A pair is finished only when a buy and its later sell have both filled, and only after the fee. The price can cross many lines and still leave you holding coin if it walks out through the bottom.",
        "A crossing is not a finished pair.",
        "Crossing",
        "The closing price moved from one side of a line to the other. It is not a finished pair and not a result.",
    ))
    s.append(gloss(
        "One pair",
        "You can buy part of a coin. Here we buy one hundredth of a bitcoin, 0.01. 900 dollars times 0.01 bitcoin is 9 dollars before fees. In this example a buy waiting at the lower of these two lines was reached on 17 August 2023, and the sell one line above was reached on 29 August 2023. The card shows the gap, then the two fees, then what is left. Each fee is 0.1 percent of the whole trade, not of the profit: about 27 cents on the 267 dollar buy and about 28 cents on the 276 dollar sell, about 54 cents together. That is about 8 dollars 46 after fees, for one small pair. It happens only if the price comes back up through the sell line. If the price leaves through the bottom, you still hold the coin, and the pair never finishes. This card is not money you made. Past results don't predict future results.",
        "About 27 cents and about 28 cents, about 54 cents together. About 8 dollars 46 after fees.",
        "Pair",
        "One buy and the later sell of the same coin. The trading pair, bitcoin and dollars, is a different word and comes in the next lesson.",
        visual="BP01-V05",
    ))
    s.append(gloss(
        "When price leaves the range",
        "Now watch what you hold when the price leaves the range and stays out. Above the range the sells have filled and you are holding cash, with nothing left to sell. Below the range the buys have filled and you are holding coin, with nothing left to buy. That is why the way down matters most: every buy fills, and you are left holding coin.",
        "Leave through the top: cash. Leave through the bottom: coin.",
        "Leave",
        "A closing price outside the range. Through the top you hold mostly cash. Through the bottom you hold mostly coin.",
    ))
    s.append(gloss(
        "The stop",
        "Here is that stop rule on the real path. It triggers if a daily closing price is outside the range, through the top or the bottom, and the next daily closing price is still outside. Then the idea is finished. You stop the bot, which cancels the waiting orders, and do what you wrote: keep the coin or swap to cash. A bot's automatic stop is a price that can fire during the day. This course uses the two daily closing prices, unless your written plan says you turned on a price stop. This is a teaching rule, not a recommendation. The stop is your written rule for when you stop the bot. On 23 October 2023 the closing price finished above the top line, and the next day was still above it.",
        "Two closing prices outside, top or bottom. Then stop the bot.",
        "Stop",
        "A written rule for what you do if price leaves the range and the next daily closing price is still outside.",
        visual="BP01-V06",
    ))
    s.append(gloss(
        "Downside",
        "Through the top, the sells have filled and you hold cash. Through the bottom, the buys have filled and you hold coin that you bought above where the price is now.",
        "Top: cash. Bottom: coin bought above the market.",
        "Downside",
        "A leave through the bottom leaves you holding coin. The loss can keep growing until the stop acts.",
    ))
    s.append(gloss(
        "Downside",
        "That loss can keep growing until the stop acts. You stop the bot either way, then you follow the written rule. The bot does not decide the stop unless you turned that setting on. EXAMPLE, made up: three buys fill on the way down. One hundredth of a bitcoin at 27,630 is 276 dollars 30. One hundredth at 26,730 is 267 dollars 30. One hundredth at 25,830 is 258 dollars 30. Together that is 801 dollars 90. Three buys of 0.01 is 0.03 bitcoin. At 24,000, that is 720 dollars. A little below the range, at a made-up price of 24,000, that coin is worth 720 dollars. You are down 81 dollars 90 before fees, and the loss keeps growing until your stop acts.",
        "EXAMPLE, made up. About 800 down to about 720.",
        "Downside example",
        "A made-up example. Three buys on the way down. Not a real fill.",
        visual="BP01-V08",
    ))
    s.append(gloss(
        "No promise of results",
        "A common mistake is thinking the bot predicts the price. It does not. It only waits. Another mistake is starting with no written stop. There is no promise of results in this lesson. Numbers marked Example are teaching numbers, not advice.",
        "No promise of results. The bot does not predict the price.",
        "No promise",
        "The pair card shows a teaching sum. It is not money you made and not a forecast.",
    ))
    s.append(gloss(
        "L-plates",
        "Paper or demo trading is like driving with learner plates, or training wheels: you practise with pretend money before anything is real. Lesson 7 shows you how.",
        "Learner plates, or training wheels. Pretend money first. Lesson 7 shows the practice.",
        "Learner plates",
        "Practice on paper or a demo before any real order. Learner plates, or training wheels.",
    ))
    s.append(gloss(
        "The map",
        "Steps one to six. This introduction is step one. Then what you need. Then exactly what a grid bot does, order by order. Then market regimes. Then choosing grid spacing and range. Then entry and exit rules. Steps seven to eleven. Then a paper test. Then weekly checks. Then common mistakes. Then scaling up under written rules. Then an optional wrap-up of the spot page, and what this course does not cover.",
        "Steps 1 to 6, each lesson named.",
        "The map",
        "The eleven lessons, ending in scaling under written rules and an optional wrap-up.",
        screen_lines=(
            ("1", "Introduction"),
            ("2", "Checklist"),
            ("3", "Definition"),
            ("4", "Market shape"),
            ("5", "Spacing"),
            ("6", "Entry and exit"),
        ),
    ))
    s.append(gloss(
        "The checklist is next",
        "The next lesson is a checklist you write on paper, before any screen.",
        "Next is a checklist on paper.",
        "Next",
        "A page of what you need, written before you open a screen.",
    ))
    s.append(gloss(
        "One sentence to keep",
        "In short: a grid waits, it buys lower and sells higher while price bounces, the fees come out of what the pair makes, and if a daily closing price leaves and stays out, you stop the bot and follow the rule you wrote.",
        "Wait, bounce, fees, and a written stop.",
        "One sentence",
        "Buys lower, sells higher, fees come out of what the pair makes, and the stop is yours to follow.",
    ))
    s += stack("Self-check", [
        "Check yourself. Why does a grid start with some coin as well as cash? Because the sell orders need coin you already hold.",
        "In the example pair, why is the net about 8 dollars 46 and not the full 9 dollars? The two fees come out first.",
        "Price closes above your top line, and the next day's closing price is still above it. What do you do, and who does it? You stop the bot and follow your written rule, by hand, unless you turned on the bot's stop setting.",
    ], "")
    s += stack("Your turn", [
        "Your turn. On paper, write the top and the bottom, one gap, and the stop rule.",
        "Say what you will do if a daily closing price leaves the range and the next closing price is still outside. Pause the video and write your answer before you go on.",
        "No real order is sent in this lesson. Paper practice comes in Lesson 7, and real money only after your written graduation rule. A graduation rule is the written test you pass on paper first. You draw the idea. If a screen appears later, it should be a copy of the page, and only on paper or demo.",
    ], "")
    s.append(gloss(
        "No secrets",
        "Bring a notebook, and no secrets: no seed phrase, private key or API secret. A seed phrase or private key is the master password to a crypto wallet. An API secret is a key that lets an app place trades on your account, and sometimes move money out of it. Never share a seed phrase, a private key or an API secret. Nobody from this course will ask for one.",
        "No seed phrase, private key, or API secret.",
        "Secrets",
        "A seed phrase or private key is the master password to a crypto wallet. An API secret is a key that lets an app place trades on your account, and sometimes move money out of it. Never share a seed phrase, a private key or an API secret. Nobody from this course will ask for one.",
    ))
    s.append(gloss(
        "The pair, next",
        "The pair, in the next lesson, is the two things you swap, like bitcoin and US dollars.",
        "Next, the pair: bitcoin and US dollars.",
        "Pair, next",
        "The two things you swap. Bitcoin and US dollars in this course.",
    ))
    s += stack("Recap", [
        "A grid bot places waiting buys below the current price and waiting sells above it, inside a range you choose.",
        "A finished pair buys lower and sells higher. The fees come out of what the pair makes. In the example that was about 8 dollars 46, and it is not a promise.",
        "Leave through the top and you hold mostly cash. Leave through the bottom and you hold mostly coin.",
        "If a daily closing price leaves the range and the next closing price is still outside, you stop the bot and follow the rule you wrote.",
    ], "")
    end = outro(
        "What you are going to need",
        "write the page of what you need, before any screen.",
    )
    end["vo"] = end["vo"].replace("band", "range")
    end["caption"] = end["caption"].replace("band", "range")
    s.append(end)
    return s

def _bp02_line(chapter: str, vo: str, **extra) -> dict:
    """One approved sentence or group. The card later shows this text in full."""
    first = vo.split(". ")[0].strip()
    if first and not first.endswith((".", "?", "!")):
        first += "."
    shot = _shot(chapter=chapter, vo=vo, caption=first, **extra)
    shot["term_text"] = chapter
    shot["definition_text"] = first
    return shot


def bp02() -> list[dict]:
    """Stewart, 23 Nov 11:04am AEDT: spoken changes B1–B5, T1–T3, L2, L3. Not L1."""
    s = [ident("02", "What you are going to need")]
    s.append(legal())
    s.append(_bp02_line(
        "Hook",
        "Crypto is a digital coin, such as bitcoin. "
        "A range is the top and the bottom, a gap is the space between two lines, "
        "and the step is how wide that gap is. "
        "A stop is the rule for what you will do if the price leaves the range. "
        "Like a packing list before a trip, your page comes before any screen.",
        kind="stack",
        v2_cards=[
            {"cue": "", "title": "Crypto", "lines": ["Crypto is a digital coin, such as bitcoin."]},
            {"cue": "a range", "title": "Range", "lines": ["A range is the top and the bottom."]},
            {"cue": "a gap", "kind": "scene", "scene": "gap", "title": "Gap"},
            {"cue": "the step", "kind": "scene", "scene": "step", "title": "Step"},
            {"cue": "a stop", "title": "Stop", "lines": ["A stop is the rule for what you will do if the price leaves the range."]},
            {"cue": "packing list", "kind": "scene", "scene": "packing", "title": "The page"},
        ],
    ))
    s += stack("Objectives", [
        "By the end you will fill in a seven-item checklist on paper.",
        "You will keep every secret off that page.",
        "You will mark the page Example so nobody can read it as an order.",
    ], "")
    for chapter, vo, cards in _BP02_BEATS:
        shot = _bp02_line(chapter, vo, kind="stack", v2_cards=cards)
        s.append(shot)
    s.append(_bp02_line(
        "Recap",
        "Recap: your page has seven items, each with a written fact, every figure marked Example, and no secrets on it.",
        kind="stack",
        v2_cards=[{"cue": "", "kind": "notebook", "shown": 7, "title": "Recap"}],
    ))
    end = outro("How a grid bot works, order by order", "see what the bot does, order by order.")
    end["vo"] = end["vo"].replace("your band,", "your range,", 1)
    s.append(end)
    return s


def _cards(*rows: tuple[str, str, bool]) -> list[dict]:
    """cue phrase, full lines joined by the caller, and whether the card needs an EXAMPLE chip."""
    cards = []
    for cue, text, example in rows:
        cards.append({"cue": cue, "title": "", "lines": [text], "example": example})
    if cards:
        cards[0]["cue"] = ""
    return cards


_BP02_BEATS: list[tuple[str, str, list]] = [
    (
        "Seven items",
        "The seven items are: a notebook, three words, range, levels and stop, the pair, "
        "paper or a demo account, no secrets, a written stop, and the word Example on every figure. "
        "Each item has a reason. The notebook is the plan you can check later. "
        "The three words stop you drawing a grid with no edges. "
        "The pair names what you buy and what you pay with. "
        "Paper or a demo is learner plates, or training wheels. "
        "No secrets keeps the keys off the page. The written stop is the action. "
        "Example marks a teaching number. "
        "For this course the pair is bitcoin priced in US dollars. "
        "A demo account uses pretend money. A daily closing price is the last price of the day. "
        "You are naming that public series, not choosing an app.",
        [
            {"cue": "", "kind": "notebook", "shown": 0, "title": "Seven items"},
            {"cue": "a notebook", "kind": "notebook", "shown": 1, "title": "Seven items"},
            {"cue": "three words", "kind": "notebook", "shown": 2, "title": "Seven items"},
            {"cue": "the pair", "kind": "notebook", "shown": 3, "title": "Seven items"},
            {"cue": "paper or", "kind": "notebook", "shown": 4, "title": "Seven items"},
            {"cue": "no secrets", "kind": "notebook", "shown": 5, "title": "Seven items"},
            {"cue": "a written", "kind": "notebook", "shown": 6, "title": "Seven items"},
            {"cue": "example on", "kind": "notebook", "shown": 7, "title": "Seven items"},
            {"cue": "the notebook is", "kind": "notebook", "shown": 7, "highlight": 0, "title": "Seven items"},
            {"cue": "three words stop", "kind": "notebook", "shown": 7, "highlight": 1, "title": "Seven items"},
            {"cue": "the pair names", "kind": "notebook", "shown": 7, "highlight": 2, "title": "Seven items"},
            {"cue": "learner plates", "kind": "notebook", "shown": 7, "highlight": 3, "title": "Seven items"},
            {"cue": "no secrets keeps", "kind": "notebook", "shown": 7, "highlight": 4, "title": "Seven items"},
            {"cue": "the written stop is", "kind": "notebook", "shown": 7, "highlight": 5, "title": "Seven items"},
            {"cue": "example marks", "kind": "notebook", "shown": 7, "highlight": 6, "title": "Seven items"},
            {"cue": "for this course", "title": "The pair", "lines": ["Bitcoin priced in US dollars.", "BTC/USD"], "example": True},
            {"cue": "uses pretend money", "title": "A demo account", "lines": ["Uses pretend money.", "BTC/USD"]},
            {"cue": "closing price", "title": "A daily closing price", "lines": ["A daily closing price is the last price of the day."]},
        ],
    ),
    (
        "The three words",
        "Three words, before any number. Range is the top line and the bottom line. "
        "An order is an instruction to buy or sell that can wait for a price. "
        "Levels are the price lines where orders wait, like the rungs of a ladder, and a gap is the space between two of them. "
        "A stop is the rule for what you will do if a daily closing price finishes outside the range and the next daily closing price is still outside. "
        "The figures from lesson 1 are on the card, marked Example. "
        "If you can only say one of the three words, the page is missing a part.",
        [
            {"cue": "", "kind": "chart", "stage": "range", "title": "Range"},
            {"cue": "an order", "title": "Order", "lines": ["An order is an instruction to buy or sell that can wait for a price."]},
            {"cue": "levels are", "kind": "chart", "stage": "levels", "title": "Levels"},
            {"cue": "a stop is", "kind": "chart", "stage": "stop", "title": "Stop"},
            {"cue": "the figures", "kind": "chart", "stage": "gaps", "title": "Lesson 1 figures"},
            {"cue": "missing a", "kind": "chart", "stage": "stop", "title": "All three"},
        ],
    ),
    (
        "No secrets",
        "A wallet is where your crypto is held. A seed phrase is the list of words that unlocks that wallet. "
        "A private key is a secret that can move your crypto. "
        "An API secret is a password that lets a program place orders on an account, and sometimes move money out of it. "
        "You never type a seed phrase, a private key, or an API secret onto this page. "
        "The chart has no balance on it. A public closing price is not your account. "
        "If a form asks for a secret, that form is not this lesson.",
        [
            {"cue": "", "title": "", "lines": ["A wallet is where your crypto is held. A seed phrase is the list of words that unlocks that wallet."]},
            {"cue": "a private key", "title": "", "lines": ["A private key is a secret that can move your crypto. An API secret is a password that lets a program place orders on an account, and sometimes move money out of it."]},
            {"cue": "you never", "kind": "scene", "scene": "secrets-off", "title": "No secrets"},
            {"cue": "no balance", "kind": "scene", "scene": "no-balance", "title": "No balance"},
            {"cue": "a form asks", "kind": "scene", "scene": "not-form", "title": "Not this lesson"},
        ],
    ),
    (
        "Copy the path",
        "You copy the range onto the page, not every day's prices. "
        "Copy the bottom line and the top line, with six gaps of about 900. "
        "Every closing price in that window stayed inside the range. Mark each figure Example.",
        [
            {"cue": "", "kind": "chart", "stage": "range", "title": "Copy the range"},
            {"cue": "copy the bottom", "kind": "chart", "stage": "gaps", "title": "Copy the range"},
            {"cue": "every closing", "kind": "chart", "stage": "page", "title": "Copy the range"},
        ],
    ),
    (
        "Worked check",
        "Worked check: pair, range, gaps, stop, and Example. "
        "If the stop line is only a tick with no sentence, the page fails the check. "
        "The rule has to say: if a daily closing price finishes outside the range and the next daily closing price is still outside, the example is over.",
        [
            {"cue": "", "kind": "chart", "stage": "check", "title": "Worked check"},
        ],
    ),
    (
        "The page",
        "A page is the notebook you can hold. "
        "An exchange is the app or website where people buy and sell crypto. The screen is the exchange. "
        "Lesson 1 ended by asking you to bring the page. This lesson is that page. "
        "Open the notebook before any screen.",
        [
            {"cue": "", "title": "", "lines": ["A page is the notebook you can hold."]},
            {"cue": "an exchange is", "title": "", "lines": ["An exchange is the app or website where people buy and sell crypto. The screen is the exchange."]},
            {"cue": "lesson 1 ended", "kind": "scene", "scene": "before-screen", "title": "The page"},
        ],
    ),
    (
        "The page",
        "Write today's date on the first line. Under it, write the word Example. "
        "Example means a real past price used for practice. It is not an order and not a forecast.",
        [
            {"cue": "", "kind": "scene", "scene": "date-line", "title": "The page"},
            {"cue": "example means", "title": "", "lines": ["Example means a real past price used for practice. It is not an order and not a forecast."]},
        ],
    ),
    (
        "The pair",
        "Write the pair first. The base is what you buy. The quote is what you pay with. "
        "For this course the prices are the July to October example window, the public bitcoin closing prices from 19 July to 16 October 2023, so you buy the base, bitcoin, with the quote, US dollars, and that row is labelled BTC/USD. "
        "Every other row depends on the pair. "
        "We price in US dollars. Your exchange may charge fees in Australian dollars, so keep each in its own column. "
        "If a fee sum is in Australian dollars, that sum goes on its own line, labelled BTC/AUD. "
        "Do not put a US dollar price and an Australian dollar fee on the same row.",
        [
            {"cue": "", "title": "", "lines": ["Write the pair first. The base is what you buy. The quote is what you pay with."]},
            {"cue": "for this course", "kind": "scene", "scene": "btc-usd", "title": "BTC/USD"},
            {"cue": "every other row", "kind": "scene", "scene": "btc-aud", "title": "BTC/AUD"},
            {"cue": "we price", "title": "Two columns", "lines": ["We price in US dollars. Your exchange may charge fees in Australian dollars, so keep each in its own column."]},
            {"cue": "do not put", "kind": "scene", "scene": "do-not-mix", "title": "Do not mix"},
        ],
    ),
    (
        "The range",
        "Range is the top line and the bottom line. In the July to October example window those lines are 24,930 and 30,331. Both figures are Example. "
        "Levels are the lines between them. Six gaps of about 900 dollars sit between the top and the bottom. "
        "Write the top and the bottom only after you have said what a range is. "
        "Then write one gap, and how you got it: the top minus the bottom, divided by the number of gaps.",
        [
            {"cue": "", "kind": "chart", "stage": "range", "title": "Range"},
            {"cue": "levels are", "kind": "chart", "stage": "levels", "title": "Levels"},
            {"cue": "write the top", "kind": "chart", "stage": "page", "title": "Range"},
        ],
    ),
    (
        "The stop",
        "The stop sentence has to say what you will do. "
        "A bot is a program that places and cancels the waiting orders for you. "
        "Two daily closing prices outside the range, through the top or the bottom, and the second closing price still outside. "
        "Then you stop the bot, which cancels the waiting orders, and you follow the rule you wrote. "
        "Write that stop in one sentence.",
        [
            {"cue": "", "kind": "scene", "scene": "stop-sentence", "title": "Stop"},
            {"cue": "a bot is", "kind": "scene", "scene": "bot", "title": "Bot"},
            {"cue": "two daily", "kind": "chart", "stage": "stop", "title": "Stop"},
            {"cue": "then you stop", "kind": "chart", "stage": "page", "title": "Stop"},
        ],
    ),
    (
        "Account in Australia",
        "A deposit is crypto or Australian dollars you send into an account at an exchange. "
        "An exchange in Australia asks who you are before you can deposit. "
        "That check is required by Australian anti-money laundering law, and the exchange runs it, not this course. "
        "You only upload identification inside the exchange's own app. "
        "This course does not name an exchange and does not show a balance. "
        "Any exchange offering crypto services in Australia must register with AUSTRAC, Australia's financial crime regulator, as a virtual asset service provider. "
        "AUSTRAC keeps a public register you can search. Check that register before you sign up. "
        "The register says the business is listed. It does not say your money is protected. "
        "Registration is not a safety guarantee. "
        "ASIC is Australia's financial services regulator. "
        "From April 2027, platforms that hold crypto for you need an ASIC licence, with a transition period to October 2027 for platforms already operating. "
        "Check ASIC for the current position. This lesson names only government bodies, never an exchange.",
        [
            {"cue": "", "kind": "safety", "step": 0, "mark": 0, "note": "Who you are, first", "title": "Account"},
            {"cue": "an exchange in", "kind": "safety", "step": 0, "mark": 1, "note": "The exchange asks who you are", "title": "Account"},
            {"cue": "that check is", "kind": "safety", "step": 0, "mark": 2, "note": "The exchange runs the check", "title": "Account"},
            {"cue": "you only upload", "kind": "safety", "step": 0, "mark": 3, "note": "Only in the exchange's own app", "title": "Account"},
            {"cue": "any exchange offering", "kind": "safety", "step": 1, "mark": 0, "note": "Look up the register", "title": "AUSTRAC"},
            {"cue": "austrac keeps", "kind": "safety", "step": 1, "mark": 1, "note": "Search the public register", "title": "AUSTRAC"},
            {"cue": "the register says", "kind": "safety", "step": 1, "mark": 2, "note": "Listed is not protection", "title": "AUSTRAC"},
            {"cue": "asic is", "kind": "safety", "step": 2, "mark": 3, "note": "Australia's financial services regulator.", "title": "ASIC"},
            {"cue": "from april", "kind": "safety", "step": 2, "mark": 1, "note": "ASIC licence from April 2027.", "title": "ASIC"},
            {"cue": "check asic", "kind": "safety", "step": 2, "mark": 0, "note": "Check the current position", "title": "ASIC"},
        ],
    ),
    (
        "Two-factor",
        "A second code, as well as your password, is two-factor authentication. "
        "Turn that on before any real dollars. Then look for a paper or demo mode. "
        "Paper uses pretend money. That practice is lesson 7.",
        [
            {"cue": "", "kind": "safety", "step": 3, "mark": 1, "note": "Turn on a second code", "title": "Two-factor"},
            {"cue": "then look", "kind": "safety", "step": 3, "mark": 2, "note": "Paper uses pretend money", "title": "Two-factor"},
        ],
    ),
    (
        "Fees",
        "A fill is when your waiting order actually trades. "
        "A maker fee is the charge when your order waits and someone else trades with it. "
        "A taker fee is the charge when your order fills straight away. "
        "A grid uses waiting orders, so read the maker fee first. "
        "Some bots also pay a taker fee when they first start. In this example both are 0.1 percent. "
        "On an example buy of 100 Australian dollars, 0.1 percent is 10 cents. "
        "The sell costs about 10 cents as well. "
        "The round trip is about 20 cents, which is 0.2 percent. "
        "This fee row is Australian dollars. It is not the July to October example window. "
        "If the gap is smaller than that 0.2 percent, each completed buy and sell costs more in fees than the gap is worth. "
        "To compare them, turn the gap into a percent by dividing it by the price. In the lesson 1 example, 900 divided by 27,630 is about 3.3 percent, well above 0.2 percent. "
        "Lesson 5 is where you test a gap against this fee. You do not pick a gap in this lesson.",
        [
            {"cue": "", "title": "", "lines": ["A fill is when your waiting order actually trades. A maker fee is the charge when your order waits and someone else trades with it. A taker fee is the charge when your order fills straight away."]},
            {"cue": "a grid uses", "kind": "fee", "stage": "maker", "title": "Fees"},
            {"cue": "100 australian", "kind": "fee", "stage": "buy", "title": "Fees"},
            {"cue": "the sell costs", "kind": "fee", "stage": "sell", "title": "Fees"},
            {"cue": "the round trip", "kind": "fee", "stage": "trip", "title": "Fees"},
            {"cue": "this fee row", "kind": "fee", "stage": "aud", "title": "Fees"},
            {"cue": "if the gap", "kind": "fee", "stage": "gap", "title": "Fees", "lines": ["900 divided by 27,630 is about 3.3 percent, well above 0.2 percent."]},
        ],
    ),
    (
        "Stablecoin",
        "A stablecoin is a coin built to stay worth about one US dollar. It can still lose that value. "
        "If your pair is priced in a stablecoin, every fill trades one coin for another, so every fill is a swap.",
        _cards(
            ("", "A stablecoin is a coin built to stay worth about one US dollar. It can still lose that value.", False),
            ("if your pair", "If your pair is priced in a stablecoin, every fill trades one coin for another, so every fill is a swap.", False),
        ),
    ),
    (
        "Journal",
        "A trading journal is a dated record of every bot: the plan, the changes, the fills, the fees, a review note of what happened, and whether you followed the rules. "
        "That note is not money you made. A stablecoin fill goes in the journal. "
        "The tax office treats a swap like a sale, so every swap goes in the journal. "
        "The journal is also the page you will open again in lesson 8 and lesson 10. "
        "For every transaction, including a buy, a sell, a swap, or a transfer, write the date and time, the amount, the value in Australian dollars at the time, the fee, which exchange or wallet, what it was for, and who the other side was. "
        "The columns are the date, the pair, the range, the gaps, the money in the bot, the stop rule, the fills, the fees, the Australian dollar value of each fill, a review note, and a yes or no for the rules. "
        "The Australian dollar value column is the one exception. It is for your tax records. "
        "Download your exchange's transaction history at least every three months. Keep those records for at least five years. "
        "This is general information, not tax advice. "
        "Leave two columns blank for now. One is for the fees. One is for whether you followed the rule. "
        "You fill those later. You do not fill them with a hope.",
        [
            {"cue": "", "kind": "journal", "cols": 4, "title": "Journal"},
            {"cue": "the tax office", "kind": "journal", "cols": 4, "mark": 0, "note": "A swap counts like a sale.", "title": "Journal"},
            {"cue": "for every transaction", "kind": "journal", "cols": 8, "mark": 1, "note": "Write the date and the fee.", "title": "Journal"},
            {"cue": "the columns are", "kind": "journal", "cols": 11, "title": "Journal"},
            {"cue": "the range", "kind": "journal", "cols": 11, "title": "Journal"},
            {"cue": "the money in", "kind": "journal", "cols": 11, "title": "Journal"},
            {"cue": "the stop rule", "kind": "journal", "cols": 11, "title": "Journal"},
            {"cue": "australian dollar", "kind": "journal", "cols": 11, "title": "Journal"},
            {"cue": "yes or no", "kind": "journal", "cols": 11, "title": "Journal"},
            {"cue": "australian dollar value", "occurrence": 2, "kind": "journal", "cols": 11, "mark": 2, "note": "That column is for tax records.", "title": "Journal"},
            {"cue": "download your", "kind": "journal", "cols": 11, "mark": 3, "note": "Download at least every three months. Keep for at least five years.", "title": "Export"},
            {"cue": "leave two", "kind": "journal", "cols": 11, "mark": 0, "note": "Fees and the rule: fill those later.", "title": "Later"},
        ],
    ),
    (
        "Scams",
        "Nobody from this course will ask for a seed phrase, a private key, or an API secret. "
        "If a message rushes you to send crypto, or asks for one of those, treat it as a scam. It is not this course.",
        [
            {"cue": "", "kind": "safety", "step": 4, "mark": 1, "note": "Nobody from this course will ask", "title": "Scams"},
            {"cue": "if a message", "kind": "safety", "step": 4, "mark": 2, "note": "A rush to send crypto is a scam", "title": "Scams"},
        ],
    ),
    (
        "Moneysmart",
        "ASIC's Moneysmart website is the public Australian guide for scam warnings. Check it yourself.",
        [
            {"cue": "", "kind": "safety", "step": 4, "mark": 0, "note": "ASIC's Moneysmart", "title": "Moneysmart"},
        ],
    ),
    (
        "Say the page",
        "Now cover the chart and say your page out loud: the pair, the range, the gaps and the stop rule. "
        "Name the pair, the range, the gaps, and the stop rule, then stop. "
        "If a word on it has not been defined, stop and define it before you go on. "
        "A secret is a seed phrase, a private key, or an API secret. None of those go on this page. "
        "You write Example on your own notebook so a practice sketch is never later mistaken for a live plan.",
        [
            {"cue": "", "kind": "scene", "scene": "say-page", "title": "Say the page"},
            {"cue": "name the pair", "kind": "scene", "scene": "name-four", "title": "Say the page"},
            {"cue": "if a word", "kind": "scene", "scene": "undefined", "title": "Say the page"},
            {"cue": "a secret is", "title": "", "lines": ["A secret is a seed phrase, a private key, or an API secret. None of those go on this page."]},
            {"cue": "you write example", "kind": "scene", "scene": "practice", "title": "Example"},
        ],
    ),
]



def signed_script(number: str, title: str, filename: str) -> list[dict]:
    """The spoken script Stewart signed on 24 Nov 2026, commit b958dff, plus the X6 title."""
    path = Path(__file__).resolve().parents[1] / "proposed-scripts-23nov" / filename
    spoken = path.read_text(encoding="utf-8").split("## Spoken script", 1)[1].strip()
    paragraphs = [part.strip() for part in spoken.split("\n\n") if part.strip()]
    shots = [ident(number, title)]
    for index, paragraph in enumerate(paragraphs):
        shots.append(_shot(
            kind="stack",
            chapter="Open" if index == 0 else "Lesson",
            vo=paragraph,
            caption=paragraph,
            canonical=True,
        ))
    return shots


def bp03() -> list[dict]:
    return signed_script("03", "How a grid bot works, order by order", "BP-03-PROPOSED.md")


def bp04() -> list[dict]:
    return signed_script("04", "Market regimes", "BP-04-PROPOSED.md")


def bp05() -> list[dict]:
    return signed_script("05", "Choosing grid spacing and range", "BP-05-PROPOSED.md")


def bp06() -> list[dict]:
    return signed_script("06", "Entry and exit rules", "BP-06-PROPOSED.md")


def bp07() -> list[dict]:
    return signed_script("07", "Spot paper trading", "BP-07-PROPOSED.md")


def bp08() -> list[dict]:
    return signed_script("08", "Managing and monitoring", "BP-08-PROPOSED.md")


def bp09() -> list[dict]:
    return signed_script("09", "Common mistakes", "BP-09-PROPOSED.md")


def bp10() -> list[dict]:
    return signed_script("10", "Scaling up on spot", "BP-10-PROPOSED.md")


def bp11() -> list[dict]:
    return signed_script("11", "Optional close: the spot page, and what this course does not cover", "BP-11-PROPOSED.md")


BUILDERS = {
    "bp-01-introduction": bp01,
    "bp-02-what-you-need": bp02,
    "bp-03-what-is-a-grid-bot": bp03,
    "bp-04-market-regimes": bp04,
    "bp-05-spacing-and-range": bp05,
    "bp-06-entry-and-exit": bp06,
    "bp-07-spot-paper-trading": bp07,
    "bp-08-managing-and-monitoring": bp08,
    "bp-09-common-mistakes": bp09,
    "bp-10-scaling-up": bp10,
    "bp-11-advanced-liquidation": bp11,
}


def attach_series(shots: list[dict]) -> list[dict]:
    for shot in shots:
        shot["series"] = PRICES.get(shot.get("chart") or "", [])
    return shots
