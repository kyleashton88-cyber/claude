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
            f"Next lesson: {next_title}. Bring the page with the band, the gaps, and the stop sentence. "
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
    shots = []
    for i, item in enumerate(items):
        vo = lead + " " + item if i == 0 else item
        shots.append(_shot(
            kind="stack",
            chapter=chapter,
            vo=vo,
            caption=item,
            items=items,
            index=i,
        ))
    return shots


def build(sid: str) -> list[dict]:
    if sid.startswith("el-"):
        raise SystemExit(f"refusing Elite id {sid}")
    return BUILDERS[sid]()


def bp01() -> list[dict]:
    s = [ident("01", "Introduction")]
    s.append(_shot(
        chapter="Hook",
        reveal_from=0, reveal=1,
        vo=(
            "From 19 July 2023 to 16 October 2023, the public daily price of bitcoin stayed in a band. "
            "The lowest daily print was 24930. The highest was 30331. "
            "Ninety days, and the path kept returning into the middle. "
            "A grid is a ladder of limit orders built for a path that behaves like that. "
            "It has nothing to do once the path leaves and stays gone."
        ),
        caption="90 days between 24,930 and 30,331.",
        levels=[LOW, HIGH],
    ))
    s += stack("Objectives", [
        "Name the range, the levels, and the stop on this 2023 window.",
        "Point to a day whose close is still inside the band.",
        "Write the stop as the day the path leaves 30331 and does not return.",
    ], "By the end you will be able to do three things.")
    s.append(legal())
    s.append(_shot(
        kind="analogy", analogy="ladder", chapter="A ladder",
        reveal=1,
        vo=(
            "Think of a ladder leaned on a wall. The rungs do not chase you. They wait. "
            "On the right is the real path, not the ladder. The ladder is only the analogy. "
            "The rungs you are about to see are prices inside that summer band."
        ),
        caption="Analogy: rungs wait. The chart is the real path.",
    ))
    s.append(_shot(
        chapter="The range",
        reveal=1,
        focus_price=HIGH, focus_label="High",
        vo=(
            "The range is the top and the bottom you copy from the path, before you invent a rung. "
            "Here the public low is 24930 and the public high is 30331. "
            "Round numbers that ignore those prints are a different drawing. "
            "Seven days in this window wicked above 30000. One day wicked under 25000. "
            "A tidy 25000 to 30000 box would have been left behind on those days."
        ),
        caption="Use the real low and the real high.",
        levels=[LOW, HIGH],
    ))
    s.append(_shot(
        chapter="The levels",
        reveal=1,
        vo=(
            "Six equal gaps of about 900 dollars fit between those two prints. "
            "The rungs land near 25830, 26730, 27630, 28531, and 29431, with the ends at 24930 and 30331. "
            "A limit order sits on a rung. It does not run after the price. "
            "The daily close crossed 27630 ten times in this window. That is the path changing sides of one rung, "
            "not a promise that an order would have filled."
        ),
        caption="Six gaps of about 900. One rung was crossed 10 times.",
    ))
    s.append(_shot(
        kind="analogy", analogy="fence", chapter="The fence",
        reveal=1,
        vo=(
            "A fence has a top rail and a bottom rail. Inside it, the path can wander. "
            "The fence on the left is the analogy. The band on the right is 24930 to 30331. "
            "If you cannot point at both rails on the chart, the page is not ready."
        ),
        caption="Analogy: two rails. Chart: 24,930 and 30,331.",
    ))
    s += walk(SUMMER, "Walk the summer", 4, (LOW, HIGH), "Closes inside the summer window")
    s.append(_shot(
        chart=RALLY, chapter="The stop",
        chart_title="The leave: October 2023 into March 2024",
        reveal_from=0, reveal=1,
        levels=LEVELS,
        focus_price=HIGH, focus_label="Left behind",
        vo=(
            "The stop is a sentence about a path, not a mood. "
            "On 23 October 2023 the public daily close was 33086. That is above 30331. "
            "By 14 March 2024 the close was near 71397. The summer band was behind it. "
            "Write this: if the daily close leaves 30331 and does not return, the summer idea is finished. "
            "The chart now draws that leave. The old high stays on the screen as the rail that was crossed."
        ),
        caption="23 October 2023. The close leaves 30,331.",
    ))
    s.append(_shot(
        kind="worked", chapter="Worked check",
        items=[
            "Window: 19 July 2023 to 16 October 2023.",
            "Low 24,930. High 30,331.",
            "Six gaps. About 900 dollars each.",
            "Stop: close leaves 30,331 and does not return.",
        ],
        vo=(
            "Worked check, marked Example. The window is 19 July 2023 to 16 October 2023. "
            "Low 24930. High 30331. Six gaps of about 900. "
            "The stop sentence names 23 October 2023, when the close printed 33086. "
            "Nothing in that list is an order."
        ),
        caption="Example only. Low, high, six gaps, one stop.",
    ))
    s += stack("Recap", [
        "The range was the real low and the real high, 24930 and 30331.",
        "The levels were six gaps of about 900, and one rung was crossed ten times.",
        "The stop was the October leave, when 30331 stayed behind the path.",
    ], "Recap, in three lines.")
    s.append(outro("What you are going to need"))
    return s


def bp02() -> list[dict]:
    s = [ident("02", "What you are going to need")]
    s.append(_shot(
        kind="analogy", analogy="list", chapter="Hook",
        reveal=1,
        vo=(
            "A packing list is written before the trip, not during the scramble at the door. "
            "The list on the left is the analogy. The chart is the trip we already took in public prices. "
            "You need the page before you need a screen. People lose this lesson when they open a form "
            "and hope the summer band will type itself."
        ),
        caption="Write the page before any screen.",
    ))
    s += stack("Objectives", [
        "Fill seven lines from the summer window, on paper.",
        "Keep every secret off that page.",
        "Mark the page Example so it cannot be read as an order.",
    ], "By the end you will be able to do three things.")
    s.append(legal())
    s.append(_shot(
        chapter="Seven lines",
        board="seven-lines",
        reveal=1,
        vo=(
            "The seven lines are: notebook, the three words range levels and stop, the pair name, "
            "paper or demo, no secrets, a written stop, and the word Example on every figure. "
            "For this course the pair name is bitcoin versus the dollar, public daily closes. "
            "You are not choosing a venue. You are naming the series on the chart."
        ),
        caption="Seven lines. The pair is the public series.",
    ))
    s.append(_shot(
        chapter="The three words",
        board="three-words",
        reveal=1,
        vo=(
            "Carry the three words forward. Range: 24930 to 30331. "
            "Levels: six gaps of about 900. "
            "Stop: the close leaves 30331 and does not return, as it did on 23 October 2023. "
            "If you can only say one of them, the packing list is short a rail."
        ),
        caption="Range, levels, stop. All three from the same window.",
    ))
    s.append(_shot(
        chapter="No secrets",
        board="no-secrets",
        reveal=1,
        vo=(
            "You never type a seed phrase, a private key, or an A P I secret onto this page. "
            "The chart has no balance on it. A public close is not your account. "
            "If a form asks for a secret, that form is not this lesson."
        ),
        caption="No key. No balance. Public closes only.",
    ))
    s += walk(SUMMER, "Copy the path", 4, (LOW, HIGH), "One figure you are allowed to copy")
    s.append(_shot(
        kind="worked", chapter="Worked check",
        items=[
            "Pair: bitcoin, public daily closes.",
            "Band: 24,930 to 30,331.",
            "Gaps: six, about 900.",
            "Stop sentence: written. Example: written.",
        ],
        vo=(
            "Worked check. Read the seven ideas against the page. "
            "Pair, band, gaps, stop, Example. "
            "If the stop line is only a tick with no sentence, the page fails the check. "
            "The sentence has to name 30331 and a path that does not return."
        ),
        caption="A tick with no sentence fails the check.",
    ))
    s += stack("Recap", [
        "The page comes before the screen.",
        "The figures are the summer low, the summer high, and six gaps.",
        "Secrets stay off the page. Example stays on it.",
    ], "Recap.")
    s.append(outro("What is a grid bot"))
    return s


def bp03() -> list[dict]:
    s = [ident("03", "What is a grid bot")]
    s.append(_shot(
        chapter="Hook", reveal=1,
        levels=[LOW, HIGH],
        vo=(
            "A grid bot, in this lesson, is not a guess about next month. "
            "It is a set of limit orders waiting on rungs inside a band you already measured. "
            "The band is the summer of 2023. The path is already on the chart. "
            "We are naming the mechanism, not claiming a fill."
        ),
        caption="Waiting orders inside a band you measured.",
    ))
    s += stack("Objectives", [
        "Define a grid as limit orders waiting inside 24930 to 30331.",
        "Say which side of 27630 is the buy side in this picture.",
        "Refuse a sentence that calls the ten crosses a result.",
    ], "By the end you will be able to do three things.")
    s.append(legal())
    s.append(_shot(
        chapter="Limit orders wait", reveal=1, focus_price=27630, focus_label="27630",
        vo=(
            "A limit order waits at a price. A market order cuts through the book. They are different tools. "
            "On this chart the middle rung is 27630. The daily close crossed it ten times. "
            "Each cross is the path changing sides. It is not a receipt."
        ),
        caption="Daily closes crossed 27,630 10 times. A cross is not a filled order.",
    ))
    s.append(_shot(
        chapter="Buys and sells", board="buys-sells", reveal=1, focus_price=27630, focus_label="Middle",
        vo=(
            "One teaching picture places buy orders below the middle and sell orders above it. "
            "Below 27630: 26730, 25830, 24930. Above it: 28531, 29431, 30331. "
            "When the path stepped down toward 26050 on 18 August 2023, it was on the lower side of that picture. "
            "When it later printed 27969 on 7 October, it was back through the middle. "
            "If the path leaves, one side can be left holding inventory. The October leave did that to any band that ended at 30331."
        ),
        caption="Buys below 27,630. Sells above it. Example only.",
    ))
    s += walk(SUMMER, "Where the path stood", 4, (LOW, HIGH), "The path, not a forecast")
    s.append(_shot(
        kind="worked", chapter="Worked check",
        items=[
            "Middle rung: 27,630.",
            "18 August close: about 26,050. Lower side.",
            "7 October close: 27,969. Through the middle.",
            "Ten crosses are not a result.",
        ],
        vo=(
            "Worked check. Point at 27630. "
            "Say whether 26050 on 18 August is below it. It is. "
            "Say whether 27969 on 7 October is above it. It is. "
            "Then say the sentence you must not say: that the ten crosses were a gain. Do not say that. They were crosses."
        ),
        caption="Below, then above. Crosses are not a gain.",
    ))
    s += stack("Recap", [
        "A grid here means limit orders waiting inside the measured band.",
        "Buys sit below 27630 in the picture. Sells sit above it.",
        "The October leave left that picture behind.",
    ], "Recap.")
    s.append(outro("Market regimes"))
    return s


def bp04() -> list[dict]:
    s = [ident("04", "Market regimes")]
    s.append(_shot(
        chapter="Hook", chart=SUMMER, reveal=1,
        vo=(
            "The same ladder is a different idea when the path changes shape. "
            "You sort the shape before you talk about gaps. "
            "This lesson uses three public windows: the summer band, the rally that left it, "
            "and the March 2020 drop."
        ),
        caption="Sort the shape before the gaps.",
    ))
    s += stack("Objectives", [
        "Label the summer window as a range.",
        "Label October 2023 to March 2024 as a leave, not a range.",
        "Label 12 March 2020 as a break, and refuse a grid on that day.",
    ], "By the end you will be able to do three things.")
    s.append(legal())
    s.append(_shot(
        chapter="Range", chart=SUMMER, reveal=1,
        vo=(
            "A range, on this page, is a path that keeps returning inside a high and a low. "
            "From 19 July to 16 October 2023 the prints stayed between 24930 and 30331, "
            "with the close swinging back through 27630 again and again. "
            "That is the shape a ladder can even be about."
        ),
        caption="Summer 2023: the path keeps returning.",
    ))
    s.append(_shot(
        chapter="Trend", chart=RALLY, chart_title="October 2023 to March 2024",
        reveal_from=0, reveal=1, levels=LEVELS, focus_price=HIGH, focus_label="Old high",
        vo=(
            "A trend on this page is a path that leaves and keeps making ground in one direction. "
            "After 23 October 2023 the close went from 33086 to about 71397 by 14 March 2024. "
            "There were pauses. The old band did not contain them. "
            "A ladder drawn at 24930 to 30331 was finished when that leave held."
        ),
        caption="The leave ran from about 33,086 to about 71,397.",
    ))
    s.append(_shot(
        chapter="Break", chart=CRASH, chart_title="20 February 2020 to 23 March 2020",
        reveal_from=0, reveal=1, levels=[],
        vo=(
            "A break is a path that jumps out of the prices around it. "
            "On 11 March 2020 the public close was 7911. "
            "On 13 March the public daily low was 4107. "
            "That is a drop of about 48 percent from that close to that low. "
            "You do not sort those three days as a quiet range, and you do not lay a summer-style ladder across them."
        ),
        caption="13 March 2020. Low 4,107.",
    ))
    s += walk(RALLY, "Walk the leave", 8, (LOW, HIGH), "After the summer band")
    s.append(_shot(
        kind="worked", chapter="Worked sort",
        items=[
            "July to October 2023: range.",
            "23 October 2023 onward: leave.",
            "12 to 13 March 2020: break.",
        ],
        vo=(
            "Worked sort. Three labels, three windows, no score that says go. "
            "Range, leave, break. If you give the March 2020 low the label range, the sort is wrong."
        ),
        caption="Three windows. Three labels. No score.",
    ))
    s += stack("Recap", [
        "The summer path returned inside 24930 and 30331.",
        "The autumn path left 30331 and did not come back.",
        "March 2020 was a break. A ladder is the wrong picture for those days.",
    ], "Recap.")
    s.append(outro("Choosing grid spacing and range"))
    return s


def bp05() -> list[dict]:
    s = [ident("05", "Spacing and range")]
    s.append(_shot(
        chapter="Hook", reveal=1, focus_price=30000, focus_label="30000",
        vo=(
            "A band that ignores the real wick is too tight, even when it looks neat. "
            "A box from 25000 to 30000 would have missed seven days that wicked above 30000 "
            "in the summer window, and one day that wicked under 25000. "
            "The public high was 30331. The public low was 24930. Start there."
        ),
        caption="A neat 25,000 to 30,000 box missed real wicks.",
    ))
    s += stack("Objectives", [
        "Count gaps, not the lines that bound them, on this window.",
        "Compare a 900 dollar gap with a two-tenth of one percent cost.",
        "Widen a band that the real wick already left.",
    ], "By the end you will be able to do three things.")
    s.append(legal())
    s.append(_shot(
        chapter="Gaps, not lines", reveal=1,
        vo=(
            "The seven prices are 24930, 25830, 26730, 27630, 28531, 29431, and 30331. "
            "That is seven lines and six gaps. Counting the lines and calling them gaps is the miss. "
            "The step is about 900 dollars. On a middle near 27630, that step is about 3 percent. "
            "Two tenths of one percent of 27630 is about 55 dollars. "
            "The gap is wider than that example cost. A gap thinner than the cost is the one you cross out."
        ),
        caption="Seven lines. Six gaps. About 900 dollars.",
    ))
    s.append(_shot(
        chapter="Wicks", reveal=1, focus_price=30000, focus_label="Too tight",
        vo=(
            "The range has to hold the wicks you already have, not only the closes you liked. "
            "If your top is 30000 and the window printed 30331, the top is a story, not the data. "
            "Move the rail to the print, then recount the gaps. Do not change the step and the rail in one silent edit."
        ),
        caption="The high was 30,331. A 30,000 top is a story.",
    ))
    s += walk(SUMMER, "Recount against the path", 4, (LOW, HIGH), "Does the close fit the rails?")
    s.append(_shot(
        kind="worked", chapter="Worked recount",
        items=[
            "Lines: 7. Gaps: 6.",
            "Step: about 900 dollars.",
            "Example cost: about 55 dollars.",
            "900 is wider than 55. The thin gap is the one you reject.",
        ],
        vo=(
            "Worked recount. Say seven lines, six gaps. "
            "Say about 900 against about 55. "
            "Keep the wider one in the example. Cross the idea of a gap that cannot clear the cost. "
            "This is a recount of a public window, not a fee from a venue."
        ),
        caption="900 against about 55. Example cost, not a venue fee.",
    ))
    s += stack("Recap", [
        "Rails come from the prints: 24930 and 30331.",
        "Count the gaps. Six, not seven.",
        "A gap that cannot clear the example cost is rejected.",
    ], "Recap.")
    s.append(outro("Entry and exit rules"))
    return s


def bp06() -> list[dict]:
    s = [ident("06", "Entry and exit rules")]
    s.append(_shot(
        chapter="Hook", chart=RALLY, chart_title="The leave after the summer band",
        reveal=1, levels=LEVELS, focus_price=HIGH, focus_label="Exit",
        vo=(
            "Entry without an exit is a page that cannot finish. "
            "The exit is a path you can point at. On this chart it is already drawn. "
            "23 October 2023, close 33086, above the summer high, and the path did not go back inside 30331."
        ),
        caption="The exit is a path you can point at.",
    ))
    s += stack("Objectives", [
        "Write the finish sentence before the start sentence.",
        "Point each sentence at a date on the chart.",
        "Leave size off the page until both sentences exist.",
    ], "By the end you will be able to do three things.")
    s.append(legal())
    s.append(_shot(
        chapter="Finish first", chart=RALLY, reveal=1, levels=LEVELS, focus_price=HIGH, focus_label="Finish",
        vo=(
            "Finish sentence: if the daily close leaves 30331 and does not return, the summer idea is over. "
            "The date you can point at is 23 October 2023. The close was 33086. "
            "Hope that the weave continues is not this sentence. A feeling is not a date."
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
    s += walk(RALLY, "Point at the leave", 8, (LOW, HIGH), "Finish sentence, checked against closes")
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
    s += stack("Recap", [
        "The finish sentence names 23 October 2023.",
        "The before sentence names a day still inside the band.",
        "Size waits until both sentences point at the chart.",
    ], "Recap.")
    s.append(outro("Spot paper trading"))
    return s


def bp07() -> list[dict]:
    s = [ident("07", "Spot paper trading")]
    s.append(_shot(
        kind="analogy", analogy="list", chapter="Hook", reveal=1,
        vo=(
            "This lesson walks fields on a paper or demo spot page. It does not place an order. "
            "The list is the analogy of the form. The chart is the source of the figures. "
            "The page wins. If the form disagrees with 24930 and 30331, the form is wrong for this example."
        ),
        caption="The page wins. The form is a copy.",
    ))
    s += stack("Objectives", [
        "Copy only the pair, the band, the gap count, and the two sentences.",
        "Treat a line count as the wrong translation of six gaps.",
        "Leave without sending anything.",
    ], "By the end you will be able to do three things.")
    s.append(legal())
    s.append(_shot(
        chapter="Not a venue", reveal=1,
        vo=(
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
            "Pair: bitcoin, public daily closes. Upper: 30331. Lower: 24930. Gaps: six. "
            "Finish sentence and before sentence, even if the form has no box for a sentence. "
            "You still read them before you stand up."
        ),
        caption="Upper 30,331. Lower 24,930. Gaps: six.",
    ))
    s.append(_shot(
        chapter="Spot, not a contract", reveal=0.5,
        vo=(
            "The path is spot. A contract with a multiple is a different product. "
            "Nothing in the summer window asks you to multiply the position. "
            "If a default size is already filled in, clear it. The page did not write that size."
        ),
        caption="Spot. Clear a size the page did not write.",
    ))
    s += walk(SUMMER, "Read the figures aloud", 4, (LOW, HIGH), "Read, then point")
    s.append(_shot(
        kind="worked", chapter="Worked check",
        items=[
            "Form says 7 grids. Page says 6 gaps.",
            "You recount. You do not accept the word grids.",
            "You leave. Nothing is sent.",
        ],
        vo=(
            "Worked check. The form says seven and your page says six gaps. "
            "Seven was the line count. Six is the gap count. "
            "You keep six. You close the page. No order."
        ),
        caption="Seven lines are not six gaps.",
    ))
    s += stack("Recap", [
        "Copy the summer figures, not a default.",
        "Translate lines into gaps before you accept them.",
        "Stop without sending.",
    ], "Recap.")
    s.append(outro("Managing and monitoring"))
    return s


def bp08() -> list[dict]:
    s = [ident("08", "Managing and monitoring")]
    s.append(_shot(
        chapter="Hook", reveal=0.55,
        vo=(
            "Monitoring is a short list you can finish, not a vigil. "
            "Three questions, on a day you chose. "
            "We will run them on 7 October 2023, and then on 23 October 2023, so you can see the answers change."
        ),
        caption="Three questions. Two real dates.",
    ))
    s += stack("Objectives", [
        "Answer inside, which side, and does the sentence still hold.",
        "Use 7 October and 23 October as the two checks.",
        "Stop when the three answers are written. Do not open a result.",
    ], "By the end you will be able to do three things.")
    s.append(legal())
    s.append(_shot(
        chapter="7 October", reveal=0.7, focus_price=27969, focus_label="27969",
        vo=(
            "7 October 2023. The public close was 27969. "
            "Inside the band? Yes. 27969 sits between 24930 and 30331. "
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
            "Which side no longer matters in the old picture, because the picture was the band. "
            "Does the finish sentence hold? Yes. The close left 30331. "
            "The action that follows is the sentence you already wrote, not a new hunt for a score."
        ),
        caption="23 October 2023. Outside. The stop sentence holds.",
    ))
    s += walk(SUMMER, "A cadence through the band", 4, (LOW, HIGH), "Same three questions, another day")
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
    s += stack("Recap", [
        "Inside or not. Which side of 27630. Does the sentence hold.",
        "7 October was inside. 23 October was not.",
        "The check ends when the three answers are written.",
    ], "Recap.")
    s.append(outro("Common mistakes"))
    return s


def bp09() -> list[dict]:
    s = [ident("09", "Common mistakes")]
    s.append(_shot(
        chapter="Hook", reveal=1, focus_price=30000, focus_label="Miss",
        vo=(
            "The mistakes in this lesson are pages, not personalities. "
            "A blank stop. A band tighter than the wicks. A line count used as a gap count. "
            "Each one can be pointed at on the summer chart."
        ),
        caption="Three misses you can point at.",
    ))
    s += stack("Objectives", [
        "Find the blank stop, the tight band, and the line-count miss.",
        "Fix one of them, then reread, then fix the next.",
        "Keep result language off the page.",
    ], "By the end you will be able to do three things.")
    s.append(legal())
    s.append(_shot(
        chapter="Blank stop", chart=RALLY, reveal=1, levels=LEVELS,
        vo=(
            "A blank stop means the finish column was skipped. "
            "Without the sentence about 23 October, every later copy of the summer band has no end. "
            "The fix is to write the sentence, not to add a second indicator."
        ),
        caption="No finish sentence, no end to the page.",
    ))
    s.append(_shot(
        chapter="Tight band", reveal=1, focus_price=30000, focus_label="Tight",
        vo=(
            "A tight band here is 25000 to 30000. It looks round. "
            "The window's high was 30331 and seven days wicked over 30000. "
            "The fix is to move the rail to the print, then recount six gaps. "
            "You do not fix the rail and the count in one scribble."
        ),
        caption="Round numbers lost the wick at 30,331.",
    ))
    s.append(_shot(
        chapter="Counting lines", reveal=1,
        vo=(
            "Seven prices are on the ladder. The gaps between them are six. "
            "Calling it a seven-grid because you counted marks is the spacing miss, come back again. "
            "The fix is the recount you already did: six."
        ),
        caption="Seven marks. Six gaps.",
    ))
    s += walk(SUMMER, "Audit the path", 4, (LOW, HIGH), "One question: does the page match this close?")
    s.append(_shot(
        kind="worked", chapter="Worked audit",
        items=[
            "Pass one: write the 23 October stop.",
            "Pass two: move 30,000 up to 30,331.",
            "Do not grade the page. List the rewrites.",
        ],
        vo=(
            "Worked audit. Two passes. "
            "First the missing sentence. Then the rail that ignored 30331. "
            "A result word does not belong on either pass."
        ),
        caption="One fix, then the next. No grade.",
    ))
    s += stack("Recap", [
        "A blank finish column is the first miss.",
        "A band inside the real wicks is the second.",
        "A line count standing in for a gap count is the third.",
    ], "Recap.")
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
            "Two buckets. Page one is the summer of 2023. "
            "Page two is a later public window, 27 March 2024 to 24 June 2024, "
            "with a low of 56555 and a high of 72715. "
            "Same gates. One change: the band."
        ),
        caption="Page two: 56,555 to 72,715. One change.",
    ))
    s += stack("Objectives", [
        "Open page two only after page one has a stop sentence.",
        "Change the band and nothing else.",
        "Keep the two pages in separate buckets.",
    ], "By the end you will be able to do three things.")
    s.append(legal())
    s.append(_shot(
        chapter="Same gates", chart=LATER, chart_title="The later window",
        reveal_from=0, reveal=1, levels=[],
        vo=(
            "Page two still has to pass the sort, the rails, the gap count, and a finish sentence. "
            "The later window is not automatically a range just because you want a second page. "
            "Look at it. The low is 56555 and the high is 72715. "
            "That span is wider than the summer span. You measure it. You do not copy 900 dollars across."
        ),
        caption="Do not copy the 900 dollar step onto a new window.",
    ))
    s.append(_shot(
        chapter="One change", chart=LATER, reveal=1, levels=[],
        vo=(
            "Between the pages you change one thing. Here, the band. "
            "The pair stays bitcoin, public daily closes. The product stays spot. "
            "A multiple does not appear on page two because you are excited. "
            "If you cannot name the one change, page two is not ready."
        ),
        caption="One change: the band. Spot stays spot.",
    ))
    s += walk(LATER, "Walk page two", 4, (56555, 72715), "Later window, measured on its own")
    s.append(_shot(
        kind="worked", chapter="Worked pair",
        items=[
            "Page one: 24,930 to 30,331. Stop written.",
            "Page two: 56,555 to 72,715. Measured again.",
            "Buckets stay separate.",
        ],
        vo=(
            "Worked pair. Say the summer band. Say the later band. "
            "Say the one change. If both numbers moved and the product changed too, you changed more than one thing."
        ),
        caption="Two bands. One change. Two buckets.",
    ))
    s += stack("Recap", [
        "Page two uses the same gates as page one.",
        "The later window is 56555 to 72715, not a copy of 900.",
        "Spot stays spot. Size is still not a target.",
    ], "Recap.")
    s.append(outro("Advanced: liquidation scenarios"))
    return s


def bp11() -> list[dict]:
    s = [ident("11", "Liquidation, as a public path")]
    s.append(_shot(
        chart=CRASH, chapter="Hook", chart_title="February and March 2020",
        reveal_from=0, reveal=1, levels=[],
        vo=(
            "This lesson is opt-in. The spot page is already complete without it. "
            "The losing path comes first. On 13 March 2020 the public daily low was 4107. "
            "The close on 11 March had been 7911. "
            "A contract can be closed by the venue when the margin is gone. A spot holding of coins is not that mechanism."
        ),
        caption="13 March 2020. Public low 4,107.",
    ))
    s += stack("Objectives", [
        "Separate a spot holding from a forced close on a contract.",
        "Describe isolated as one box, and cross as a reach into another box.",
        "Skip the contract picture if you are staying on the summer spot page.",
    ], "By the end you will be able to do three things.")
    s.append(legal())
    s.append(_shot(
        chart=SUMMER, chapter="Spot is complete", reveal=1,
        vo=(
            "The summer page does not need this lesson. "
            "24930 to 30331, six gaps, a stop on 23 October 2023. "
            "That page has no multiple on it. Leaving this lesson is a complete choice. "
            "Write Skipped on purpose if you stop here, and keep the spot page."
        ),
        caption="You can stop. The summer page already stands.",
    ))
    s.append(_shot(
        chart=CRASH, chapter="What the drop is", chart_title="The public drop",
        reveal=1, levels=[],
        vo=(
            "Liquidation, in plain words, means a venue closes a contract because the margin cannot carry it. "
            "The chart is not a venue screen. It is the public path those days followed. "
            "From the 11 March close at 7911 to the 13 March low at 4107 is about 48 percent. "
            "Draw that drop before you draw any recovery. The low comes first in the story."
        ),
        caption="About 48 percent, from 7,911 to the low at 4,107.",
    ))
    s.append(_shot(
        kind="analogy", analogy="buckets", chart=CRASH, chart_title="Two boxes, one path",
        reveal=1, levels=[], chapter="Isolated and cross",
        vo=(
            "Isolated, in this analogy, means one bucket. A loss stays in that bucket. "
            "Cross means a line from that bucket into the next one. "
            "The chart on the right is still March 2020. The buckets are not a balance. "
            "They are the picture of whether a second box can be pulled in. "
            "No times-number is written on either bucket."
        ),
        caption="One box, or a reach into the next. No multiple.",
    ))
    s += walk(CRASH, "Walk the drop", 2, None, "February and March 2020")
    s += walk(SUMMER, "The spot page beside it", 6, (LOW, HIGH), "The spot page this crash does not replace")
    s.append(_shot(
        kind="worked", chapter="Worked path",
        items=[
            "11 March 2020 close: 7,911.",
            "13 March 2020 low: 4,107.",
            "Spot page: not this mechanism.",
            "If you stay on spot, write Skip.",
        ],
        vo=(
            "Worked path. Say the close, then the low. "
            "Say that a spot page does not get liquidated by that drop. "
            "Say that a contract might. Then choose. The summer page does not require the contract."
        ),
        caption="Close, then low. Then choose spot or skip.",
    ))
    s += stack("Recap", [
        "The spot blueprint is complete without a contract.",
        "13 March 2020 shows a public drop, not a personal balance.",
        "Isolated stays in one box. Cross can reach. No multiple is written.",
    ], "Recap.")
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
