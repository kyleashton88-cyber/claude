"""Blueprint lessons built around one public Bitcoin path.

House example: daily closes from 19 July 2023 to 16 October 2023.
Low 24,930. High 30,331. Six gaps of about 900.
The path leaves that high on 23 October 2023.
A second window, March to June 2024, is the later page.
12–13 March 2020 is the crash used for liquidation, as a public price path only.
"""

from __future__ import annotations

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


def _shot(**kwargs) -> dict:
    kwargs.setdefault("kind", "chart")
    kwargs.setdefault("chart", SUMMER)
    kwargs.setdefault("levels", LEVELS)
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
        nearest = min(LEVELS, key=lambda lv: abs(lv - close))
        side = "above" if close >= 27630 else "below"
        bits = [
            f"On {pretty(row['date'])}, the public daily close was {close}.",
            f"That day's low was {low} and the high was {high}.",
        ]
        if band:
            lo_i, hi_i = int(band[0]), int(band[1])
            if lo_i <= close <= hi_i:
                bits.append(f"The close is inside the band of {lo_i} to {hi_i}.")
            else:
                bits.append(
                    f"The close is outside the band of {lo_i} to {hi_i}. "
                    "The stop sentence is the line that applies."
                )
        bits.append(f"The nearest example rung is {nearest}. The close is {side} 27630.")
        if day_span > 900:
            bits.append(
                f"The day's own range was {day_span} dollars, wider than one example gap of about 900. "
                "A single quiet day is not the whole band."
            )
        else:
            bits.append(
                f"The day's own range was {day_span} dollars, inside one example gap of about 900. "
                "The gap is a property of the window, not of this one day."
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
            levels=LEVELS if chart in {SUMMER, RALLY, LATER} else [],
            focus_price=nearest,
            focus_label=f"{nearest:,}",
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
            "Education only, not financial advice. Crypto carries a risk of total loss. "
            "This is general information. It doesn't consider your objectives, financial situation or needs. "
            "The prices are public historical daily closes, marked Example. "
            "Past performance is not a reliable indicator of future results. "
            "No order is sent from this lesson."
        ),
        caption="Education only. Not financial advice. Chart: historical BTC prices, EXAMPLE.",
        chart=SUMMER,
    )


def ident(number: str, title: str) -> dict:
    return _shot(
        kind="ident",
        chapter="Grid Bot Blueprint",
        vo=f"Grid Bot Blueprint, lesson {number}, {title}.",
        caption=f"Lesson {number}. {title}.",
    )


def outro(next_title: str | None) -> dict:
    if next_title:
        vo = (
            f"Next lesson: {next_title}. Bring your notes: the top and bottom of the band, the gaps between the lines, and your stop rule. "
            "Leave every figure marked Example. No order is sent between lessons."
        )
        caption = next_title
    else:
        vo = (
            "This is the end of the Blueprint. The spot page can stand on its own. "
            "Leave every figure marked Example. No order is sent from this lesson."
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
    return BUILDERS[sid]()


def bp01() -> list[dict]:
    s = [ident("01", "Introduction")]
    s += stack("The idea", [
        "A grid bot places waiting buy orders on lines below the price and sell orders on lines above it, inside a top and a bottom you choose. The space between your top and your bottom is called the band.",
        "A limit order is an order that waits at a price you choose. It does not chase the price. Chasing the price would mean moving the order to follow wherever the price has gone.",
            "The sells above need some coin, so a grid starts with part cash and part coin, and that is a description, not advice about what to hold. Cash is money you can spend. Coin is the crypto.",
        "A stop is a rule you write down before you start, saying what you will do if the price leaves the band and does not come back.",
        "When a chart says Example, it means a real past price used as an example, not a forecast.",
    ], "")
    s += stack("Objectives", [
        "By the end you will know what a grid bot places.",
        "You will see that idea on one real path from 2023.",
        "You will be able to say the stop rule in one sentence.",
    ], "")
    s.append(legal())
    s.append(_shot(
        kind="analogy", analogy="ladder", chapter="A ladder",
        reveal=1,
        levels=[LOW, HIGH],
        vo=(
            "Think of a ladder leaned on a wall. The rungs wait, and they do not chase you. "
            "The ladder is the analogy, and the chart beside it is the real past path."
        ),
        caption="The rungs wait. The chart is the real past path.",
    ))
    s.append(_shot(
        chapter="The range",
        reveal=1,
        focus_price=HIGH, focus_label="High",
        vo=(
            "The range is the top line and the bottom line, taken from the path. "
            "Every close in this window stayed between those two lines."
        ),
        caption="The top line and the bottom line, taken from the path. Bottom 24,930. Top 30,331.",
        levels=[LOW, HIGH],
    ))
    s.append(_shot(
        chapter="The levels",
        reveal=1,
        vo=(
            "Six equal gaps of about 900 dollars sit between the bottom line and the top line. "
            "The about 900 dollar gap is the step from one line to the next, worked out as the top line minus the bottom line divided by the six gaps, not the whole band. "
            "Seven lines make those six gaps. A limit order waits on a level. It does not run after the price."
        ),
        caption="Seven lines. Six gaps of about 900.",
    ))
    s.append(_shot(
        kind="analogy", analogy="fence", chapter="The fence",
        reveal=1,
        vo=(
            "A fence has a top rail and a bottom rail. Inside them, the price can wander. "
            "On the chart those rails are 24930 and 30331."
        ),
        caption="Two rails: 24,930 and 30,331.",
    ))
    s.append(_shot(
        chapter="One day",
        chart_title="One day inside the band",
        candle={"high": 30184, "low": 29794, "close": 29914, "date": "19 July 2023"},
        vo=(
            "The daily close is the last price of the day. Crypto trades all day, so the day is cut at a set time. "
            "This is a simple candle that shows the day's high, low and close. "
            "This candle is 19 July 2023. The high, the low, and the close are labelled."
        ),
        caption="19 July 2023. Close 29,914. Low 29,794. High 30,184.",
    ))
    s.append(_shot(
        chapter="The whole window",
        chart_title="19 July 2023 to 16 October 2023",
        reveal=1,
        vo=(
            "The example is Bitcoin's public daily price in US dollars. "
            "From 19 July 2023 to 16 October 2023, every one of those days closed inside the band. "
            "We do not need to read each day. The shape is the lesson, and it is marked Example."
        ),
        caption="Every close stayed inside the band.",
        levels=[LOW, HIGH],
    ))
    s.append(_shot(
        chart=RALLY, chapter="The stop",
        chart_title="The price leaves the band",
        reveal_from=0, reveal=1,
        levels=LEVELS,
        focus_price=HIGH, focus_label="Left behind",
        vo=(
            "A stop is a rule you write down before you start, saying what you will do if the price leaves the band and does not come back. "
            "On 23 October 2023 the close finished above the top line. "
            "The price did not come back, so this example was finished."
        ),
        caption="23 October 2023. The close leaves 30,331.",
    ))
    s.append(_shot(
        kind="worked", chapter="Worked check",
        items=[
            "Window: 19 July 2023 to 16 October 2023.",
            "Six gaps: about 900 dollars.",
            "Low: 24,930.",
            "High: 30,331.",
        ],
        vo=(
            "Worked check: 19 July 2023 to 16 October 2023. "
            "Six equal gaps of about 900 dollars. "
            "The low is the bottom line. "
            "The high is the top line."
        ),
        caption="Six equal gaps of about 900 dollars.",
    ))
    s.append(_shot(
        kind="worked", chapter="Worked check",
        items=[
            "Stop: the close leaves the top line and does not come back.",
            "Nothing on this card is an order.",
        ],
        vo=(
            "The stop rule is: if the daily close leaves the top line and does not come back, the idea is finished. "
            "Nothing on this card is an order."
        ),
        caption="The stop rule finishes the idea. Nothing here is an order.",
    ))
    s += stack("Recap", [
        "A grid bot places waiting buys below the price and waiting sells above it.",
        "This 2023 path stayed between 24,930 and 30,331, with six gaps of about 900 between the lines.",
        "The stop rule says what you will do if the price leaves and does not come back.",
    ], "")
    s.append(outro("What you are going to need"))
    s[-1]["vo"] = (
        "Next lesson: What you are going to need. "
        "The pair is the two things you swap, like Bitcoin and US dollars. "
        "Bring your notes: the top and bottom of the band, the gaps between the lines, your stop rule, and no secrets. "
        "Leave every figure marked EXAMPLE, and no order is sent between lessons."
    )
    return s


def bp02() -> list[dict]:
    s = [ident("02", "What you are going to need")]
    s.append(_shot(
        kind="analogy", analogy="list", chapter="Hook",
        reveal=1,
        vo=(
            "Crypto is a digital coin, such as bitcoin, and a daily close is the last price of that day. "
            "A band, also called the range, is the top and the bottom, a gap is the space between two lines, and the step is how wide that gap is. "
            "A stop is the rule for what you will do if the price leaves the band. "
            "Like a packing list before a trip, your page comes before any screen."
        ),
        caption="Write the page before any screen.",
    ))
    s += stack("Objectives", [
        "By the end you will fill in a seven-item checklist on paper. An order is an instruction to buy or sell.",
        "You will keep every secret off that page.",
        "You will mark the page Example so nobody can read it as an order.",
    ], "")
    s.append(legal())
    s.append(_shot(
        chapter="Seven lines",
        board="seven-lines",
        reveal=1,
        vo=(
            "The seven items are: a notebook, the three words, range, levels and stop, which come next, the pair, "
            "paper or a demo account, no secrets, a written stop, and the word Example on every figure. "
            "A pair is what you buy and what you pay with. For this course the pair is bitcoin priced in US dollars. "
            "A demo account uses pretend money. "
            "A daily close is the last price of the day. You are naming that public series, not choosing an app."
        ),
        caption="Seven lines. The pair is the public series.",
    ))
    s.append(_shot(
        chapter="The three words",
        board="three-words",
        reveal=1,
        vo=(
            "Three words, before any number. Range is the top line and the bottom line. "
            "Levels are the price lines where orders wait, like the rungs of a ladder, and a gap is the space between two of them. "
            "A stop is the rule for what you will do if the price leaves the band and does not come back. "
            "The figures from lesson 1 are on the card, marked Example. If you can only say one of the three words, the page is missing a part."
        ),
        caption="Range, levels, stop. All three from the same window.",
    ))
    s.append(_shot(
        chapter="No secrets",
        board="no-secrets",
        reveal=1,
        vo=(
            "A seed phrase is the list of words that unlocks a crypto wallet. A private key or an API secret is a password that can move your money. "
            "You never type a seed phrase, a private key, or an API secret onto this page. "
            "The chart has no balance on it. A public close is not your account. "
            "If a form asks for a secret, that form is not this lesson."
        ),
        caption="No key. No balance. Public closes only.",
    ))
    s.append(_shot(
        chapter="Copy the path",
        reveal=1,
        vo=(
            "You copy the band onto the page, not every day's prices. "
            "Copy the bottom line and the top line, with six gaps of about 900. "
            "Every close in that window stayed inside the band. Mark each figure Example."
        ),
        caption="Copy the band. Every close stayed inside it.",
    ))
    s.append(_shot(
        kind="worked", chapter="Worked check",
        items=[
            "Pair: bitcoin, public daily closes.",
            "Band: 24,930 to 30,331.",
            "Gaps: six, about 900.",
            "Stop sentence: written. Example: written.",
        ],
        vo=(
            "Worked check: pair, band, gaps, stop, and Example. "
            "If the stop line is only a tick with no sentence, the page fails the check. "
            "The rule has to say: if the daily close goes above 30331 and does not come back, the example is over."
        ),
        caption="A tick with no sentence fails the check.",
    ))
    s.append(_shot(
        chapter="Say the page",
        reveal=1,
        vo=(
            "Say the page once, in your own words, and do not read the chart again. "
            "Name the pair, the band, the gaps, and the stop rule, then stop. "
            "A secret is a seed phrase, a private key, or an API secret. None of those go on this page. "
            "You write Example on your own notebook so a practice sketch is never later mistaken for a live plan."
        ),
        caption="Say the page once. No secrets. Example is not an order.",
    ))
    s += stack("Recap", [
        "The page comes before the screen.",
        "The figures are the bottom line, the top line, and six gaps.",
        "Secrets stay off the page. Example stays on it.",
    ], "")
    s.append(outro("What is a grid bot"))
    return s


def bp03() -> list[dict]:
    s = [ident("03", "What is a grid bot")]
    s.append(_shot(
        chapter="Hook", reveal=1,
        levels=[LOW, HIGH],
        vo=(
            "A grid bot places orders that wait inside a top and a bottom you already measured. "
            "A limit order is an order that waits at a price you choose. "
            "A market order does not wait. It buys or sells straight away, at the prices people are already offering."
        ),
        caption="Orders that wait inside a measured band.",
    ))
    s += stack("Objectives", [
        "By the end you will know what a grid bot is.",
        "You will know which side of the middle buys and which side sells.",
        "You will know why the price touching a line is not the same as making money.",
    ], "")
    s.append(legal())
    s.append(_shot(
        chapter="Limit orders wait", reveal=1, focus_price=27630, focus_label="27630",
        vo=(
            "A rung is one price line where an order waits. "
            "A ring on the chart means the price touched that rung. A white square means an order actually traded. "
            "The exchange is the app or website where people buy and sell crypto. "
            "The book is that exchange's list of everyone's waiting orders. "
            "A cross is the price line touching a rung. A fill is an order that actually trades."
        ),
        caption="A cross touches a rung. A fill is an order that trades.",
    ))
    s.append(_shot(
        chapter="Limit orders wait", reveal=1, focus_price=27630, focus_label="27630",
        vo=(
            "The daily close is the last price of each day. "
            "The middle rung on this chart is 27630, and the daily close crossed it ten times. "
            "These ten marks are crosses, not fills. They are marked Example, and they are not money you made."
        ),
        caption="The daily close crossed 27,630 ten times. Those marks are crosses, not fills.",
    ))
    s.append(_shot(
        chapter="Buys and sells", board="buys-sells", reveal=1, focus_price=27630, focus_label="Middle",
        vo=(
            "There are three buy rungs below the middle and three sell rungs above it. "
            "They sit about 900 apart. "
            "On 18 August 2023 the close was 26050, below the middle, so that day was on the buy side."
        ),
        caption="Three buy rungs below the middle. Three sell rungs above it.",
    ))
    s.append(_shot(
        chapter="Where the price stayed",
        reveal=1,
        levels=[LOW, HIGH, 27630],
        vo=(
            "From 19 July 2023 to 16 October 2023 the price stayed between 24930 and 30331. "
            "The daily close crossed the middle rung ten times. "
            "That is the path next to the band. It is marked Example, and it is not a forecast."
        ),
        caption="The price stayed between 24,930 and 30,331.",
    ))
    worked = (
        "Worked check. Three buy rungs sit below the middle and three sell rungs sit above it, about 900 apart. "
        "On 18 August 2023 the close was 26050, below the middle. "
        "The ten crosses are not a gain."
    )
    s.append(_shot(
        kind="worked", chapter="Worked check",
        items=[
            "Three buy rungs below the middle. Three sell rungs above it.",
            "The rungs are about 900 apart.",
            "18 August 2023: the close was 26,050, below the middle.",
            "The ten crosses are not a gain.",
        ],
        vo=worked,
        caption=worked,
    ))
    s.append(_shot(
        chapter="One step down, one step up",
        reveal=1,
        vo=(
            "Coin is the crypto. Cash is the money you can spend. "
            "Here is one step, slowly. Price falls through a buy rung, and the waiting buy can fill. "
            "You then hold a little more coin, and a sell can be written one rung higher. "
            "If price rises through that sell, it can fill, and you hold a little more cash. "
            "A cross is only the price touching the line. A fill is the order actually trading. "
            "This is how the picture works. It is not a promise that you make money."
        ),
        caption="A buy can fill on the way down. A sell can fill on the way up.",
    ))
    s.append(_shot(
        chart=RALLY, chapter="When the idea ends",
        chart_title="October 2023 to March 2024",
        reveal=1, levels=LEVELS, focus_price=HIGH, focus_label="Left behind",
        vo=(
            "This example ended in October 2023. "
            "On 23 October 2023 the daily close was 33086, above 30331. "
            "The price did not come back, so the waiting orders inside the old band no longer matched the path. "
            "A stop is your rule for what you will do if the price leaves the band. You write that rule before you start, so you already know the exit."
        ),
        caption="23 October 2023. Close 33,086. The old band was finished.",
    ))
    s.append(_shot(
        kind="stack", chapter="Your turn",
        vo="Your turn. Draw a top and a bottom. Put three buys below the middle and three sells above it. Write one stop sentence for when the price leaves.",
        caption="Your turn. Draw the band, the six gaps, and one stop sentence.",
        items=["Your turn. Draw a top and a bottom. Put three buys below the middle and three sells above it. Write one stop sentence for when the price leaves."],
        index=0,
    ))
    s += stack("Recap", [
        "A grid here means limit orders waiting inside the band you measured.",
        "Three buy rungs sit below the middle. Three sell rungs sit above it.",
        "When the price left the band in October, that picture no longer applied.",
    ], "")
    s.append(_shot(
        kind="outro",
        chapter="Next",
        vo=(
            "Next lesson: market regimes. "
            "A market regime is the kind of market you are in, for example sideways or trending. "
            "Bring the page with the band and the stop rule, and leave every figure marked Example. "
            "No order is sent between lessons."
        ),
        caption="Market regimes",
        reveal=1,
    ))
    return s


def bp04() -> list[dict]:
    s = [ident("04", "Market regimes")]
    s.append(_shot(
        chapter="Hook", chart=SUMMER, reveal=1,
        vo=(
            "A market regime is the kind of market you are in, for example sideways or trending. "
            "A trend is a price that leaves the band and keeps moving one way. "
            "You sort that shape before you talk about gaps. "
            "This lesson uses three public windows: the summer band, the rally that left it, "
            "and the March 2020 drop."
        ),
        caption="Sort the shape before the gaps.",
    ))
    s += stack("Objectives", [
        "By the end you will be able to call the summer window a range.",
            "You will call October 2023 to March 2024 a trend, not a range.",
        "You will call 12 to 13 March 2020 a break, and you will not draw a grid on those days.",
    ], "")
    s.append(legal())
    s.append(_shot(
        chapter="Range", chart=SUMMER, reveal=1,
        vo=(
            "A range, on this page, is a path that keeps returning inside the top line and the bottom line. "
            "From 19 July to 16 October 2023 every close stayed between those two lines, "
            "with the close swinging back through the middle line again and again. "
            "That is the kind of market a grid is built for."
        ),
        caption="Summer 2023: the path keeps returning.",
    ))
    s.append(_shot(
        chapter="Trend", chart=RALLY, chart_title="October 2023 to March 2024",
        reveal_from=0, reveal=1, levels=LEVELS, focus_price=HIGH, focus_label="Old high",
        vo=(
            "A trend on this page is a path that leaves and keeps making ground in one direction. "
            "After 23 October 2023 the close went from 33086 to 71397 by 14 March 2024. "
            "There were pauses. The old band did not contain them. "
            "A ladder drawn from the bottom line to the top line was finished when that trend held."
        ),
        caption="The trend ran from about 33,086 to about 71,397.",
    ))
    s.append(_shot(
        chapter="Break",
        candle={"high": 5838, "low": 4107, "close": 5564, "date": "13 March 2020"},
        vo=(
            "A break is a path that jumps out of the prices around it. "
            "This candle is 13 March 2020. The high, the low, and the close are labelled. "
            "From the close two days earlier, about 8 thousand, down to the low on this candle, is about 48 percent. "
            "You do not sort those days as a quiet range, and you do not lay a summer-style ladder across them."
        ),
        caption="13 March 2020. High 5,838. Low 4,107. Close 5,564.",
    ))
    s.append(_shot(
        chart=RALLY, chapter="After the leave",
        chart_title="After the summer band",
        reveal=1, levels=LEVELS, focus_price=HIGH, focus_label="Old high",
        vo=(
            "After 23 October 2023 the price stayed outside the old band. "
            "You can see that from the shape. You do not read every day. "
            "The old top line is behind the price. That shape is a trend, not a range."
        ),
        caption="The price left 30,331 and did not come back.",
    ))
    s.append(_shot(
        kind="worked", chapter="Worked sort",
        items=[
            "July to October 2023: range.",
            "23 October 2023 onward: trend.",
            "12 to 13 March 2020: break.",
        ],
        vo=(
            "Worked sort. Three labels, three windows, no score that tells you to trade. "
            "Range, trend, break. If you label the March 2020 drop a range, the sort is wrong."
        ),
        caption="Three windows. Three labels. No score.",
    ))
    s.append(_shot(
        chapter="How to sort",
        reveal=1,
        vo=(
            "Sort a window by the shape, not by a hope. "
            "If the price keeps returning inside a top and a bottom, call it a range. "
            "If it leaves and keeps going one way, call it a trend. "
            "If it jumps out of the prices around it, call it a break. "
            "A grid of waiting orders belongs to a range. It does not belong to a trend or a break. "
            "Name the shape before you draw any rungs. A range can hold a ladder. A trend and a break cannot. "
            "The three windows in this lesson are examples of those three shapes."
        ),
        caption="Range, trend, or break. A grid belongs to a range.",
    ))
    s += stack("Recap", [
        "The summer path returned inside 24930 and 30331.",
        "The autumn path trended away from 30331 and did not come back.",
        "March 2020 was a break. A ladder is the wrong picture for those days.",
    ], "")
    s.append(outro("Choosing grid spacing and range"))
    return s


def bp05() -> list[dict]:
    s = [ident("05", "Spacing and range")]
    s.append(_shot(
        chapter="Hook", reveal=1, focus_price=30000, focus_label="30000",
        vo=(
            "A band narrower than the real top line and bottom line is too tight, even when it looks neat. "
            "A round box would have missed days that went outside it."
        ),
        caption="A neat round box missed the real lines.",
    ))
    s += stack("Objectives", [
        "By the end you will count the gaps, not the lines that bound them.",
        "You will compare a gap of about 900 with an example cost of about 55.",
        "You will widen a band that the real top line already left.",
    ], "")
    s.append(legal())
    s.append(_shot(
        chapter="Gaps, not lines", reveal=1,
        vo=(
            "There are seven prices on the ladder and six gaps between them. "
            "Counting the lines and calling them gaps is the miss. "
            "The step is about 900 dollars. Near 27630, that step is about 3 percent. "
            "Say the example fee for one buy plus one sell is two tenths of one percent. On 27630 that is about 55 dollars. "
            "The gap is wider than that example cost. A gap thinner than the cost is the one you cross out."
        ),
        caption="Seven lines. Six gaps. About 900 dollars.",
    ))
    s.append(_shot(
        chapter="Real lines", reveal=1, focus_price=30000, focus_label="Too tight",
        vo=(
            "The range has to hold the real top line and bottom line, not only the closes you liked. "
            "If your top is a round number below the real top line, it doesn't match. "
            "Move the rail up to the top line, then recount the gaps. Do not change the step and the rail in one silent edit."
        ),
        caption="The top line is 30,331. A round top misses it.",
    ))
    s.append(_shot(
        chapter="Recount against the path",
        reveal=1,
        vo=(
            "Check the rails against the path once, not day by day. "
            "Every close from 19 July 2023 to 16 October 2023 stayed between 24930 and 30331. "
            "If your top is below the top line, move the rail, then count the gaps again."
        ),
        caption="Every close stayed between the bottom line and the top line.",
    ))
    s.append(_shot(
        kind="worked", chapter="Worked recount",
        items=[
            "Lines: 7. Gaps: 6.",
            "Step: about 900 dollars.",
            "Example cost: about 55 dollars.",
            "900 is wider than 55. The thin gap is the one you reject.",
        ],
        vo=(
            "Worked recount: seven lines, six gaps, about 900 against an example cost of about 55. "
            "Keep the wider one, and cross out a gap that cannot clear the cost. "
            "This is a recount of a public window, not a fee from an app."
        ),
        caption="900 against about 55. Example cost, not a venue fee.",
    ))
    s.append(_shot(
        chapter="Why the gap matters",
        reveal=1,
        vo=(
            "The rails come from the real recorded prices of that window. "
            "A gap is the space between two levels. This window has seven prices and six gaps. "
            "The step is about 900. An example cost of about 55 is much smaller, so this step can clear that cost. "
            "A gap thinner than the cost is the one you cross out. "
            "None of this is a fee from an app. It is a recount of a public window, marked Example. "
            "If you remember only one thing, remember to count the spaces between the lines, and to set the rails on the top line and the bottom line. "
            "Point at the top rail, the bottom rail, and one gap. Say the gap is about 900. Say the rails are 24930 and 30331. That is the recount. "
            "Then stop. You do not need a second pass through the days."
        ),
        caption="Use the real prices.",
    ))
    s += stack("Recap", [
        "Rails come from the real top line and the real bottom line.",
        "Count the gaps. Six, not seven.",
        "A gap that cannot clear the example cost is rejected.",
    ], "")
    s.append(outro("Entry and exit rules"))
    return s


def bp06() -> list[dict]:
    s = [ident("06", "Entry and exit rules")]
    s.append(_shot(
        chapter="Hook", chart=RALLY, chart_title="October 2023 to March 2024",
        caption="Write the exit first.",
        reveal=1, levels=LEVELS, focus_price=HIGH, focus_label="Exit",
        vo=(
            "Entry without an exit is a page that cannot finish. "
            "The exit is a path you can point at. On this chart it is already drawn. "
            "23 October 2023, close 33086, above the top line, and the path did not go back inside 30331."
        ),
    ))
    s += stack("Objectives", [
        "By the end you will write the finish rule before the start.",
        "You will point each sentence at a date on the chart.",
        "You will leave size off the page until both sentences exist.",
    ], "")
    s.append(legal())
    s.append(_shot(
        chapter="Finish first", chart=RALLY, chart_title="October 2023 to March 2024",
        reveal=1, levels=LEVELS, focus_price=HIGH, focus_label="Finish",
        vo=(
            "The finish rule is the stop rule from lesson 1: the condition that ends the idea. "
            "Size means how much money you would put in. "
            "Finish sentence: if the daily close leaves 30331 and does not return, the summer idea is over. "
            "The date you can point at is 23 October 2023. The close was 33086. "
            "Hoping the price keeps bouncing is not this rule. A feeling is not a date."
        ),
        caption="Finish: close leaves 30,331. Date: 23 October 2023.",
    ))
    s.append(_shot(
        chapter="Before", chart=SUMMER, reveal=1,
        vo=(
            "Before sentence: the path you are looking at is still the summer range, "
            "between 24930 and 30331, the way it was on 7 October 2023 when the close was 27969. "
            "You write this only after the finish sentence exists. "
            "Size is still blank. A blank size is allowed. A blank finish is not."
        ),
        caption="Before: 7 October 2023, close 27,969, still inside.",
    ))
    s.append(_shot(
        chart=RALLY, chapter="Point at the leave",
        chart_title="October 2023 to March 2024",
        reveal=1, levels=LEVELS, focus_price=HIGH, focus_label="Finish",
        vo=(
            "Point at 23 October 2023 and say the finish rule once. "
            "The close that day was 33086, above 30331, and the price did not come back. "
            "You do not need another day's prices to see that the rule was met."
        ),
        caption="23 October 2023. The finish rule was met.",
    ))
    s.append(_shot(
        kind="worked", chapter="Worked columns",
        items=[
            "Finish: leave 30,331, no return. 23 Oct 2023.",
            "Before: still inside. 7 Oct 2023, close 27,969.",
            "Size: blank on purpose.",
        ],
        vo=(
            "Worked columns. Read the finish sentence and point at October. "
            "Read the before sentence and point at 7 October. "
            "If a classmate cannot find the date from the sentence alone, rewrite the sentence."
        ),
        caption="Two sentences. Two dates. Size still blank.",
    ))
    s.append(_shot(
        chapter="Why the finish rule comes first",
        reveal=1,
        vo=(
            "Write the finish rule before you write the start. "
            "The finish rule here is: if the daily close leaves 30331 and does not come back, the idea is finished. "
            "You can point at 23 October 2023, when the close was 33086. "
            "The before sentence only says the path is still inside the band, the way it was on 7 October 2023. "
            "Size stays blank until both sentences point at a date. A blank size is allowed. A missing finish rule is not. "
            "Read the finish rule out loud and point at the date. Then read the before sentence and point at its date. "
            "If a classmate cannot find the date from the sentence alone, rewrite the sentence before you write anything else. "
            "A finish rule without a date is only a mood. This one has a date: 23 October 2023. "
            "A before sentence without a date is the same kind of miss. This one has 7 October 2023, a day still inside the band. "
            "Say both dates, point at both, and leave the size line empty."
        ),
        caption="Finish rule first. Then the before sentence. Size stays blank.",
    ))
    s.append(_shot(
        chapter="Point, then stop",
        chart=RALLY, chart_title="October 2023 to March 2024",
        reveal=1, levels=LEVELS, focus_price=HIGH,
        vo=(
            "Point at the chart and say the finish rule without looking at the page. "
            "If the daily close leaves 30331 and does not come back, this example is finished. "
            "The date is 23 October 2023. Then say the before sentence for a day still inside, 7 October 2023. "
            "If either date is missing, the page is not finished. Size is still not part of this lesson."
        ),
        caption="Say the finish rule, then the before sentence. Size stays off.",
    ))
    s += stack("Recap", [
        "The finish rule names 23 October 2023.",
        "The before sentence names a day still inside the band.",
        "Size waits until both sentences point at the chart.",
    ], "")
    s.append(outro("Spot paper trading"))
    return s


def bp07() -> list[dict]:
    s = [ident("07", "Spot paper trading")]
    s.append(_shot(
        kind="analogy", analogy="list", chapter="Hook", reveal=1,
        vo=(
            "This lesson walks fields on a paper or demo spot page, and it does not place an order. "
            "Think of the form as a copy of your notes. The chart is the source of the figures. "
            "If the form disagrees with 24930 and 30331, the form is wrong for this example."
        ),
        caption="The page wins. The form is a copy.",
    ))
    s += stack("Objectives", [
        "By the end you will copy only the pair, the band, the gap count, and the two sentences.",
        "You will treat a line count as the wrong way to say six gaps.",
        "You will leave without sending anything.",
    ], "")
    s.append(legal())
    s.append(_shot(
        chapter="Not a venue", reveal=1,
        vo=(
            "A venue is an app or a website where people buy and sell. "
            "A venue name may be printed on a real screen. This course is not affiliated with any venue, "
            "and the pictures do not show one. No logo, no login, no balance. "
            "You are copying a public window onto paper."
        ),
        caption="No venue name. No logo. No balance.",
    ))
    s.append(_shot(
        chapter="Fields", reveal=1,
        vo=(
            "The fields you may copy are the ones on the page. "
            "Pair: bitcoin, public daily closes. Upper: the top-line figure on your card. Lower: the bottom-line figure. Gaps: six. "
            "Finish sentence and before sentence, even if the form has no box for a sentence. "
            "You still read them before you stand up."
        ),
        caption="Upper 30,331. Lower 24,930. Gaps: six.",
    ))
    s.append(_shot(
        chapter="Spot, not a contract", reveal=0.5,
        vo=(
            "Spot means you buy the coin itself. A contract is a trade on the price, often with borrowed money. "
            "A multiple, like 5x, means borrowed size. "
            "Nothing in the summer window asks you to multiply your size. "
            "If a default size is already filled in, clear it. The page did not write that size."
        ),
        caption="Spot. Clear a size the page did not write.",
    ))
    s.append(_shot(
        chapter="Read the figures",
        reveal=1,
        vo=(
            "Read the page once: bitcoin, public daily closes, upper the top-line figure on your card, lower the bottom-line figure, six gaps. "
            "A daily close is the last price of the day. "
            "You point at those figures. You do not read every day, and you do not send an order."
        ),
        caption="Read the page once. Send nothing.",
    ))
    s.append(_shot(
        kind="worked", chapter="Worked check",
        items=[
            "Form says 7 grids. Page says 6 gaps.",
            "You recount. You do not accept the word grids.",
            "You leave. Nothing is sent.",
        ],
        vo=(
            "Worked check: the form says seven and your page says six gaps. "
            "Seven was the line count, and six is the gap count. "
            "You keep six, you close the page, and no order is sent."
        ),
        caption="Seven lines are not six gaps.",
    ))
    s.append(_shot(
        chapter="What you copy",
        reveal=1,
        vo=(
            "A venue is an app or a website where people buy and sell. This course is not affiliated with one, and the page has no logo and no balance. "
            "You copy five fields: pair, top, bottom, gap count, and your two sentences. The band is 24930 to 30331, and the gap count is six. "
            "If a form says seven grids, that counted lines. Your page counted gaps, and the answer is six. "
            "Spot means coins you hold. It is not a contract, and nothing here asks you to multiply your size. "
            "Then you close the page. No order is sent. "
            "A default size already filled in is not your page. Clear it. The summer example did not write a size. "
            "Read the two sentences aloud before you stand up, even if the form has no box for a sentence. "
            "If you cannot point at 24930 and 30331 on your page, you are not ready to close it."
        ),
        caption="Copy the page. Six gaps, not seven lines. Send nothing.",
    ))
    s += stack("Recap", [
        "Copy the summer figures, not a default.",
        "Turn a line count into a gap count before you accept it.",
        "Stop without sending.",
    ], "")
    s.append(outro("Managing and monitoring"))
    return s


def bp08() -> list[dict]:
    s = [ident("08", "Managing and monitoring")]
    s.append(_shot(
        chapter="Hook", reveal=0.55,
        caption="Three questions, then stop.",
        vo=(
            "Monitoring is three questions you can finish, not something you watch all day. "
            "Inside means the close is still between the top and the bottom. "
            "Which side means whether the close is above or below the middle line. "
            "We will ask the questions on 7 October 2023, then on 23 October 2023, so you can see the answers change."
        ),
    ))
    s += stack("Objectives", [
        "By the end you will answer three questions: inside, which side, and does the rule still hold.",
        "You will use 7 October and 23 October as the two checks.",
        "You will stop when the three answers are written.",
    ], "")
    s.append(legal())
    s.append(_shot(
        chapter="7 October", reveal=0.7, focus_price=27969, focus_label="27969",
        vo=(
            "7 October 2023. The public close was 27969. "
            "Inside the band? Yes. That close sits between 24930 and 30331. "
            "Which side of 27630? Above it, by a little. "
            "Does the finish sentence still hold? The path has not left 30331 yet, so the stop has not triggered. "
            "Three answers. Then you stop."
        ),
        caption="7 October 2023. Inside. Just above 27,630.",
    ))
    s.append(_shot(
        chart=RALLY, chapter="23 October", chart_title="The check after the leave",
        reveal=0.25, levels=LEVELS, focus_price=HIGH, focus_label="Left",
        vo=(
            "23 October 2023. The public close was 33086. "
            "Inside the summer band? No. "
            "Once the price has left the band, which side no longer matters. "
            "Does the finish sentence hold? Yes. The close left 30331. "
            "The action that follows is the sentence you already wrote, not a new hunt for a score."
        ),
        caption="23 October 2023. Outside. The stop sentence holds.",
    ))
    s.append(_shot(
        chapter="The same three questions",
        reveal=1,
        vo=(
            "You do not ask the three questions of every day in the window. "
            "Two dates are enough to see the change: one still inside, and one that has left. "
            "When the three answers are written, you stop."
        ),
        caption="Two dates. Then you stop.",
    ))
    s.append(_shot(
        kind="worked", chapter="Worked check",
        items=[
            "7 Oct: inside, above 27,630, stop not triggered.",
            "23 Oct: outside, stop triggered.",
            "No result row on either card.",
        ],
        vo=(
            "Worked check. Say the 7 October answers, then the 23 October answers. "
            "If you add a profit figure to either card, wipe it off. The card has three rows."
        ),
        caption="Two dates. Three rows. No result row.",
    ))
    s.append(_shot(
        chapter="What the three answers mean",
        reveal=1,
        vo=(
            "The first answer is inside or not. Inside means the close is still between 24930 and 30331. "
            "The second answer is which side of the middle the close is on. "
            "The third answer is whether your written rule still holds. "
            "On 7 October 2023 the close was 27969, still inside, and the rule had not been met. "
            "On 23 October 2023 the close was 33086, outside, and the rule had been met. "
            "You do not add a profit number to either card. When the three answers are written, you stop. "
            "The same three questions on any later day would be the same kind of check. You do not need a row for every day to understand the change. "
            "Write the three answers, close the card, and leave the chart. Monitoring is finished when the card is finished. "
            "A longer list of days would not teach a new idea. It would only repeat the same three questions."
        ),
        caption="Inside or not. Which side. Does the rule still hold. Then stop.",
    ))
    s.append(_shot(
        chapter="A check you can finish",
        reveal=1,
        vo=(
            "A check you cannot finish is not monitoring. It is just watching. "
            "These two dates are the whole practice: 7 October inside, 23 October outside. "
            "Write the three answers, and do not open a fourth row for a result. "
            "The rule you wrote before you started is the only action the second date can call for."
        ),
        caption="Two dates. Three answers. No result row.",
    ))
    s.append(_shot(
        kind="stack", chapter="Not our service",
        vo="We do not operate an alert service.",
        caption="We do not operate an alert service.",
        items=["We do not operate an alert service."],
        index=0,
    ))
    s += stack("Recap", [
        "Ask: inside or not, which side of the middle, and does the rule still hold.",
        "7 October was inside. 23 October was not.",
        "The check ends when the three answers are written.",
    ], "")
    s.append(outro("Common mistakes"))
    return s


def bp09() -> list[dict]:
    s = [ident("09", "Common mistakes")]
    s.append(_shot(
        chapter="Hook", reveal=1, focus_price=30000, focus_label="Miss",
        caption="Three mistakes you can point at.",
        vo=(
            "The mistakes in this lesson are pages, not personalities. "
            "A blank stop. A band tighter than the real top line. A line count used as a gap count. "
            "Each one can be pointed at on the summer chart."
        ),
    ))
    s += stack("Objectives", [
        "By the end you will find a missing stop, a band tighter than the real top line, and a line counted as a gap.",
        "You will fix one, reread, then fix the next.",
        "You will keep result language off the page.",
    ], "")
    s.append(legal())
    s.append(_shot(
        chapter="Blank stop", chart=RALLY, chart_title="October 2023 to March 2024",
        reveal=1, levels=LEVELS,
        vo=(
            "A blank stop means the finish column was skipped. "
            "Without a written rule for 23 October, every later copy of the summer band has no end. "
            "The fix is to write the sentence, not to add another chart tool."
        ),
        caption="No finish sentence, no end to the page.",
    ))
    s.append(_shot(
        chapter="Tight band", reveal=1, focus_price=30000, focus_label="Tight",
        vo=(
            "A tight band here is a round box. It looks tidy. "
            "The real top line sits above that box. "
            "The fix is to move the rail up to the top line, then recount six gaps. "
            "You do not fix the rail and the count in one scribble."
        ),
        caption="The round box missed the top line, 30,331.",
    ))
    s.append(_shot(
        chapter="Counting lines", reveal=1,
        vo=(
            "Seven prices are on the ladder. The gaps between them are six. "
            "Calling it a seven-grid because you counted seven lines is the same counting mistake from lesson 5. "
            "The fix is the recount you already did: six."
        ),
        caption="Seven marks. Six gaps.",
    ))
    s.append(_shot(
        chapter="Audit the path",
        reveal=1,
        vo=(
            "Ask one question of the whole window, not of every day: does the page match the path? "
            "The path stayed between 24930 and 30331 until the close left on 23 October 2023. "
            "If the page says something else, rewrite the page."
        ),
        caption="Does the page match the path? One question.",
    ))
    s.append(_shot(
        kind="worked", chapter="Worked audit",
        items=[
            "Pass one: write the 23 October stop.",
            "Pass two: move 30,000 up to 30,331.",
            "Do not grade the page. List the rewrites.",
        ],
        vo=(
            "Worked audit, two passes: first the missing stop rule, then the rail that ignored 30331. "
            "A result word does not belong on either pass."
        ),
        caption="One fix, then the next. No grade.",
    ))
    s.append(_shot(
        chapter="Fix one thing at a time",
        reveal=1,
        vo=(
            "Fix one miss, then read the page again, then fix the next. "
            "First write the stop rule for 23 October 2023, when the close left 30331 and did not come back. "
            "Then move a round top up to the real top line, because the path had already gone past the round number. "
            "Then recount. Seven marks on the ladder are six gaps, not seven. "
            "A result word does not belong on any of those passes. The page is an example, not a grade. "
            "After each fix, read the three words again: range, levels, and the stop rule. "
            "If one of them is still blank, that is the next fix. "
            "A tight band is one the real top line already left. A missing stop is a page that cannot finish. A line count is not a gap count. "
            "Fix those three, in that order, and the page matches the summer path."
        ),
        caption="One fix, then the next. No result word.",
    ))
    s.append(_shot(
        chapter="Read it back",
        reveal=1,
        vo=(
            "Read the corrected page back once. "
            "Range: the real bottom line to the real top line, past a round box. "
            "Levels: six gaps of about 900, not seven lines. "
            "Stop: the close leaves 30331 and does not come back, which this path did on 23 October 2023. "
            "If those three are on the page, the misses in this lesson are fixed."
        ),
        caption="Range, six gaps, and a stop rule. Then the misses are fixed.",
    ))
    s += stack("Recap", [
        "A missing finish rule is the first miss.",
        "A band tighter than the real top line is the second.",
        "A line count standing in for a gap count is the third.",
    ], "")
    s.append(outro("Scaling up on spot"))
    return s


def bp10() -> list[dict]:
    s = [ident("10", "Scaling up on spot")]
    s.append(_shot(
        kind="analogy", analogy="buckets", chapter="Hook",
        chart=LATER, chart_title="27 March 2024 to 24 June 2024",
        reveal=1, levels=[],
        vo=(
            "Scaling on this page means a second written page, not a bigger feeling. "
            "Page one is the summer of 2023, and page two is 27 March 2024 to 24 June 2024. Its band on the card runs from about 57 thousand to about 73 thousand. "
            "The checks stay the same, and the one change is the band."
        ),
        caption="Page two band: 56,555 to 72,715.",
    ))
    s += stack("Objectives", [
        "By the end you will open a second page only after the first page has a stop rule.",
        "You will change the band and nothing else.",
        "You will keep each page in its own bucket, meaning its own box with its own band and stop.",
    ], "")
    s.append(legal())
    s.append(_shot(
        chapter="Same checks", chart=LATER, chart_title="27 March 2024 to 24 June 2024",
        reveal_from=0, reveal=1, levels=[],
        vo=(
            "Page two still has to pass the sort, the rails, the gap count, and a finish sentence. "
            "The later window is not automatically a range just because you want a second page. "
            "Look at it. The band runs from about 57 thousand to about 73 thousand, and every close stayed inside it. "
            "That span is wider than the summer span. You measure it. You do not copy 900 dollars across."
        ),
        caption="Do not copy the 900 dollar step onto a new window.",
    ))
    s.append(_shot(
        chapter="One change", chart=LATER, chart_title="27 March 2024 to 24 June 2024",
        reveal=1, levels=[],
        vo=(
            "Between the pages you change one thing. Here, the band. "
            "The pair stays bitcoin, public daily closes. The product stays spot. "
            "A multiple means borrowed size, like 5x. It does not appear on page two because you are excited. "
            "If you cannot name the one change, page two is not ready."
        ),
        caption="One change: the band. Spot stays spot.",
    ))
    s.append(_shot(
        chart=LATER, chapter="Page two, measured once",
        chart_title="27 March 2024 to 24 June 2024",
        reveal=1, levels=[],
        vo=(
            "Measure page two once: a band from about 57 thousand to about 73 thousand. "
            "Do not read every day, and do not copy the summer step of about 900 onto this window. "
            "Each page stays in its own bucket, meaning its own box with its own band and stop."
        ),
        caption="Measure the band once: 56,555 to 72,715. Do not copy 900.",
    ))
    s.append(_shot(
        kind="worked", chapter="Worked pair",
        items=[
            "Page one: 24,930 to 30,331. Stop written.",
            "Page two: 56,555 to 72,715. Measured again.",
            "Buckets stay separate.",
        ],
        vo=(
            "Worked pair: say the summer band, say the later band, and say the one change. "
            "If both numbers moved and the product changed too, you changed more than one thing."
        ),
        caption="Two bands. One change. Two buckets.",
    ))
    s.append(_shot(
        chapter="What stays the same",
        reveal=1,
        vo=(
            "A second page is a new band, not a bigger feeling. "
            "Page one is the summer of 2023, from 24930 to 30331, with a stop rule already written. "
            "Page two is 27 March 2024 to 24 June 2024, from 56555 to 72715. "
            "You measure that band on its own. You do not paste the summer step of about 900 onto it. "
            "The pair stays bitcoin. Spot stays spot, which means coins you hold, not a contract. "
            "If you cannot name the one change, the band, page two is not ready. "
            "A bucket here means the page stays in its own box. Page two does not borrow page one's stop date or page one's step. "
            "You measure, you name the one change, and you stop. "
            "Page one keeps its own stop date, 23 October 2023. Page two needs its own finish rule, written for its own band, not borrowed. "
            "If both the band and the product changed, you changed more than one thing. "
            "Say page one's band, say page two's band, and say the one change out loud before you stop."
        ),
        caption="One change: the band. Spot stays coins you hold.",
    ))
    s.append(_shot(
        chapter="Two pages, said once",
        reveal=1,
        vo=(
            "Say both pages once. Page one is 24930 to 30331, with its stop already written. "
            "Page two is 56555 to 72715, measured on its own dates, 27 March 2024 to 24 June 2024. "
            "The product does not change. You still hold coins, not a contract. "
            "Two buckets stay two buckets. You do not pour one page into the other."
        ),
        caption="Two bands. One change. Two separate pages.",
    ))
    s.append(_shot(
        kind="stack", chapter="Not leverage",
        vo="Scaling by adding leverage is a different course of risk, and this page crosses that out.",
        caption="Scaling by adding leverage is a different course of risk, and this page crosses that out.",
        items=["Scaling by adding leverage is a different course of risk, and this page crosses that out."],
        index=0,
    ))
    s += stack("Recap", [
        "Page two uses the same checks as page one.",
        "The later window is 56,555 to 72,715, not a copy of 900.",
        "Spot stays spot. Size is still not a target.",
    ], "")
    s.append(outro("Advanced: liquidation scenarios"))
    return s


def bp11() -> list[dict]:
    s = [ident("11", "Liquidation, as a public path")]
    s.append(_shot(
        chapter="Hook",
        caption="13 March 2020. High 5,838. Low 4,107. Close 5,564.",
        candle={"high": 5838, "low": 4107, "close": 5564, "date": "13 March 2020"},
        vo=(
            "This lesson is opt-in. The spot page is already complete without it. "
            "The losing path comes first. This candle is 13 March 2020. The high, the low, and the close are labelled. "
            "A trade made with borrowed money can be closed by the venue when the money you put up is used up. A spot holding of coins is not that mechanism."
        ),
    ))
    s += stack("Objectives", [
        "By the end you will tell a spot holding apart from a forced close on a contract.",
        "You will describe isolated as one box, and cross as a reach into another box.",
        "You will skip the contract picture if you are staying on the summer spot page.",
    ], "")
    s.append(legal())
    s.append(_shot(
        chart=SUMMER, chapter="Spot is complete", reveal=1,
        vo=(
            "The summer page does not need this lesson. "
            "It has the bottom line, the top line, six gaps, and a stop on 23 October 2023. "
            "That page has no multiple on it. Leaving this lesson is a complete choice. "
            "Write Skipped on purpose if you stop here, and keep the spot page."
        ),
        caption="You can stop. The summer page already stands.",
    ))
    s.append(_shot(
        chart=CRASH, chapter="What the drop is", chart_title="The public drop",
        reveal=1, levels=[],
        vo=(
            "Margin is the money you put up to hold a trade made with borrowed money. "
            "A contract here is a trade on the price made with borrowed money. You never hold the coin. A position is that open trade. "
            "Liquidation, in plain words, means a venue closes a contract because the margin cannot carry it. "
            "The chart is not a venue screen. It is the public path those days followed. "
            "On this line of closes, 11 March closed at 7911 and 12 March closed at 4971. That is about 37 percent. "
            "Draw that drop before you draw any recovery. The day's extreme is on the candle, not on this line of closes."
        ),
        caption="Closes: 7,911 on 11 March to 4,971 on 12 March. About 37 percent.",
    ))
    s.append(_shot(
        kind="analogy", analogy="buckets", chart=CRASH, chart_title="Two boxes, one path",
        reveal=1, levels=[], chapter="Isolated and cross",
        vo=(
            "Isolated means one bucket, and a loss stays in that bucket. "
            "Cross means a line from that bucket into the next one. "
            "The buckets are not a balance. They only show whether a second box can be pulled in, and no multiple is written on either one."
        ),
        caption="One box, or a reach into the next. No multiple.",
    ))
    s.append(_shot(
        chart=CRASH, chapter="The drop, once",
        chart_title="February and March 2020",
        reveal=1, levels=[],
        vo=(
            "You already have the two prices that matter, and both are on the card, marked Example. "
            "You do not read every day of the drop. "
            "The summer spot page is a different picture, and this drop does not replace it."
        ),
        caption="Two prices. Then stop. The spot page still stands.",
    ))
    s.append(_shot(
        kind="worked", chapter="Worked path",
        items=[
            "11 March 2020 close: 7,911.",
            "12 March 2020 close: 4,971.",
            "Spot page: not this mechanism.",
            "If you stay on spot, write Skip.",
        ],
        vo=(
            "Worked path: say the 11 March close, then the 12 March close. "
            "A spot page does not get closed by that drop, and a contract might. "
            "Then choose. The summer page does not require the contract."
        ),
        caption="One close, then the next. Then choose spot or skip.",
    ))
    s.append(_shot(
        chapter="Spot or a contract",
        reveal=1,
        vo=(
            "Liquidation means an app closes a contract because the margin cannot carry it. "
            "A spot holding is coins you already hold. That drop does not close it for you. "
            "Isolated means one box: a loss stays in that box. Cross means a line from that box into the next one. "
            "The summer page, 24930 to 30331 with a stop on 23 October 2023, has no multiple on it. "
            "You can write Skip and keep that page. This lesson does not require a contract. "
            "Draw the losing path first. A recovery drawn before that drop would tell the story backwards. "
            "The summer spot page does not use this chart, and you can leave it closed."
        ),
        caption="Spot is coins you hold. A contract can be closed for you. You can skip.",
    ))
    s.append(_shot(
        kind="stack", chapter="Not a venue",
        vo="We do not operate a venue and we are not affiliated with one.",
        caption="We do not operate a venue and we are not affiliated with one.",
        items=["We do not operate a venue and we are not affiliated with one."],
        index=0,
    ))
    s += stack("Recap", [
        "The spot blueprint is complete without a contract.",
        "13 March 2020 shows a public drop, not a personal balance.",
        "Isolated stays in one box. Cross can reach. No multiple is written.",
    ], "")
    s.append(outro(None))
    return s


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
