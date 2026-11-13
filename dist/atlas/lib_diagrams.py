"""Labelled navy and cyan diagrams for Atlas. No custom fonts, no at-rules."""
from __future__ import annotations

import html


def esc(value: str) -> str:
    return html.escape(str(value), quote=True)


_SEQ = 0


class Svg:
    def __init__(self, alt: str) -> None:
        global _SEQ
        _SEQ += 1
        self.mid = f"ah{_SEQ}"
        self.alt = alt
        self.parts: list[str] = []
        self.parts.append(
            f'<svg viewBox="0 0 1600 900" role="img" aria-label="{esc(alt)}">'
        )
        self.parts.append("<title>" + esc(alt) + "</title>")
        self.parts.append('<rect width="1600" height="900" fill="#071422"/>')
        self.parts.append(
            f'<defs><marker id="{self.mid}" markerWidth="14" markerHeight="10" refX="12" refY="5" orient="auto">'
            '<polygon points="0 0, 14 5, 0 10" fill="#8fe7ff"/></marker></defs>'
        )

    def badge(self) -> None:
        self.parts.append('<rect x="1288" y="36" width="232" height="64" rx="12" fill="#ffe7a3"/>')
        self.text(1322, 80, "EXAMPLE", 36, "#1a1204", "700")

    def title(self, text: str) -> None:
        self.text(72, 86, text, 42, "#e8f4fc", "700")

    def text(self, x, y, text, size=48, fill="#e8f4fc", weight="650") -> None:
        self.parts.append(
            f'<text x="{x}" y="{y}" fill="{fill}" font-size="{size}" '
            f'font-family="Segoe UI, Helvetica, Arial, sans-serif" font-weight="{weight}">{esc(text)}</text>'
        )

    def line(self, x1, y1, x2, y2, color="#8fe7ff", width=6, arrow=False) -> None:
        marker = f' marker-end="url(#{self.mid})"' if arrow else ""
        self.parts.append(
            f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{width}"{marker}/>'
        )

    def rect(self, x, y, w, h, fill, stroke="#8fe7ff", sw=4, rx=16) -> None:
        self.parts.append(
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
        )

    def tag(self, x, y, text, size=40) -> None:
        w = int(len(text) * size * 0.62) + 40
        h = size + 28
        self.rect(x, y - h + 12, w, h, "#10283a", "#8fe7ff", 3, 12)
        self.text(x + 18, y, text, size, "#e8f4fc", "650")

    def candle(self, x, high, low, open_, close, width=48) -> None:
        up = close <= open_  # screen y: smaller y is higher price
        color = "#7dcea0" if close <= open_ else "#ffb4b4"
        # In this canvas, high/low/open/close are already screen y values.
        self.line(x, high, x, low, color, 8)
        top = min(open_, close)
        bot = max(open_, close)
        self.rect(x - width / 2, top, width, max(12, bot - top), color, color, 0, 4)

    def done(self) -> str:
        self.parts.append("</svg>")
        return "".join(self.parts)


def _flow(title, alt, boxes, arrows, tags, badge=True) -> str:
    s = Svg(alt)
    if badge:
        s.badge()
    s.title(title)
    for x, y, w, h, label in boxes:
        s.rect(x, y, w, h, "#10283a")
        s.text(x + 28, y + h / 2 + 12, label, 40)
    for x1, y1, x2, y2 in arrows:
        s.line(x1, y1, x2, y2, arrow=True)
    for x, y, label in tags:
        s.tag(x, y, label)
    return s.done()


def _candle_one() -> str:
    s = Svg("One candlestick. High 108, close 104, open 100, low 97.")
    s.badge()
    s.title("One candle shows four prices")
    s.candle(780, 180, 760, 560, 300)
    s.line(820, 180, 980, 180, arrow=True)
    s.tag(1000, 196, "High 108")
    s.line(820, 300, 980, 300, arrow=True)
    s.tag(1000, 316, "Close 104")
    s.line(700, 560, 520, 560, arrow=True)
    s.tag(180, 576, "Open 100")
    s.line(740, 760, 560, 760, arrow=True)
    s.tag(220, 776, "Low 97")
    return s.done()


def _two_candles() -> str:
    s = Svg("Two candles. The left has a wide body. The right has a long wick.")
    s.badge()
    s.title("Body and wick are different facts")
    s.candle(520, 220, 700, 280, 620, 70)
    s.candle(1040, 160, 760, 360, 420, 70)
    s.line(590, 450, 760, 450, arrow=True)
    s.tag(780, 466, "Wide body")
    s.line(1110, 200, 1240, 200, arrow=True)
    s.tag(1260, 216, "Long wick")
    return s.done()


def _levels(title, alt, rows, path=None, tags=None, badge=True, extra_paths=None) -> str:
    s = Svg(alt)
    if badge:
        s.badge()
    s.title(title)
    for y, label, color in rows:
        s.line(160, y, 1080, y, color, 6)
        s.tag(1120, y + 14, label)
    if path:
        d = "M " + " L ".join(f"{x} {y}" for x, y in path)
        s.parts.append(f'<path d="{d}" fill="none" stroke="#b6f3d4" stroke-width="8"/>')
    for extra, color in extra_paths or []:
        d = "M " + " L ".join(f"{x} {y}" for x, y in extra)
        s.parts.append(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="8"/>')
    for x, y, label in tags or []:
        s.tag(x, y, label)
    return s.done()


def _payoff(title, alt, points, tags) -> str:
    s = Svg(alt)
    s.badge()
    s.title(title)
    s.line(180, 760, 180, 180, "#8fb4cc", 4, arrow=True)
    s.line(180, 470, 1460, 470, "#8fb4cc", 4, arrow=True)
    s.text(80, 200, "Profit", 32, "#c5d7e6")
    s.text(1320, 520, "Price", 32, "#c5d7e6")
    d = "M " + " L ".join(f"{x} {y}" for x, y in points)
    s.parts.append(f'<path d="{d}" fill="none" stroke="#8fe7ff" stroke-width="8"/>')
    for x, y, label in tags:
        s.tag(x, y, label)
    return s.done()


def _bars(title, alt, bars) -> str:
    s = Svg(alt)
    s.badge()
    s.title(title)
    for x, h, label, value in bars:
        s.rect(x, 760 - h, 220, h, "#12344c", "#8fe7ff", 4, 8)
        s.text(x + 16, 800, label, 32)
        s.tag(x, 760 - h - 20, value)
    return s.done()


DIAGRAMS: dict[str, dict] = {}


def add(file, lesson, alt, prompt, svg) -> None:
    DIAGRAMS[file] = {
        "file": file,
        "lesson": lesson,
        "width": 1600,
        "height": 900,
        "alt": alt,
        "prompt": prompt,
        "svg": svg,
    }


def build() -> None:
    P = (
        "Flat educational diagram on a navy background (#071422) with cyan lines (#8fe7ff) and pale text. "
        "Amber rounded badge in the corner that reads EXAMPLE. No people, no faces, no logos, no brand names, "
        "no exchange names. One idea only. Short labels with arrows. "
    )
    add(
        "atlas-start-01.png",
        "start",
        "Four stages in a row: Beginner, Intermediate, Advanced, and Professional, with an arrow moving to the right.",
        P + "Four boxes in a row labelled Beginner, Intermediate, Advanced, Professional. A cyan arrow runs left to right. No numbers.",
        _flow(
            "Read in this order",
            "Four stages in a row: Beginner, Intermediate, Advanced, and Professional, with an arrow moving to the right.",
            [
                (70, 360, 300, 140, "Beginner"),
                (430, 360, 300, 140, "Intermediate"),
                (790, 360, 300, 140, "Advanced"),
                (1160, 360, 360, 140, "Professional"),
            ],
            [(370, 430, 430, 430), (730, 430, 790, 430), (1090, 430, 1160, 430)],
            [],
            badge=False,
        ),
    )
    add(
        "atlas-foundations-01.png",
        "markets",
        "Buyers on the left and sellers on the right meet at a price of 105.",
        P + "Left box Buyers, right box Sellers, middle label Price 105. Arrows from both boxes to the middle. Also label Buyer idea 100 and Seller idea 110.",
        _flow(
            "A trade is a meeting",
            "Buyers on the left and sellers on the right meet at a price of 105.",
            [(80, 340, 360, 180, "Buyers"), (1160, 340, 360, 180, "Sellers")],
            [(440, 400, 620, 430), (1160, 400, 980, 430)],
            [(80, 620, "Idea 100"), (620, 250, "Price 105"), (1160, 620, "Idea 110")],
        ),
    )
    add(
        "atlas-foundations-02.png",
        "candles",
        "One candlestick. High 108, close 104, open 100, low 97.",
        P + "A single cyan candlestick. Arrows label High 108, Close 104, Open 100, and Low 97.",
        _candle_one(),
    )
    add(
        "atlas-foundations-03.png",
        "candles",
        "Two candles. The left has a wide body. The right has a long wick.",
        P + "Two candlesticks. Arrow to the wide body labelled Wide body. Arrow to the long upper wick labelled Long wick.",
        _two_candles(),
    )
    add(
        "atlas-foundations-04.png",
        "order-types",
        "A small book. The ask is 101, the bid is 99, a limit rests at 99, and a market buy pays 101.",
        P + "Two horizontal prices, Ask 101 above Bid 99. An arrow up labelled Market buy. A resting box labelled Limit 99.",
        _levels(
            "Market crosses. Limit waits.",
            "A small book. The ask is 101, the bid is 99, a limit rests at 99, and a market buy pays 101.",
            [(320, "Ask 101", "#ffb4b4"), (560, "Bid 99", "#7dcea0")],
            tags=[(180, 250, "Market buy"), (180, 680, "Limit waits at 99")],
        ),
    )
    add(
        "atlas-foundations-05.png",
        "wallets",
        "Two balances. Your wallet holds 200 and the key. A venue balance holds 800 and the key stays there.",
        P + "Two stacks. Left label Your wallet 200 and You hold the key. Right label Venue balance 800. No logos.",
        _bars(
            "Where the coins sit",
            "Two balances. Your wallet holds 200 and the key. A venue balance holds 800 and the key stays there.",
            [(280, 220, "Your wallet", "200"), (860, 520, "Venue balance", "800")],
        ),
    )
    add(
        "atlas-foundations-06.png",
        "risk-basics",
        "An account bar of 10000 with a small slice of 100, which is 1 percent. The stop is 5 away, so the size is 20.",
        P + "A long bar labelled Account 10000, a small slice labelled 1 percent is 100, and a note Distance 5 gives size 20.",
        _flow(
            "Risk is a slice, then a size",
            "An account bar of 10000 with a small slice of 100, which is 1 percent. The stop is 5 away, so the size is 20.",
            [(80, 300, 1200, 120, "Account 10000"), (80, 300, 140, 120, "")],
            [],
            [(80, 520, "1 percent is 100"), (620, 520, "Distance 5"), (1040, 520, "Size 20")],
        ),
    )
    add(
        "atlas-structure-01.png",
        "trend",
        "A rising path with higher lows at 90, 100, and 110.",
        P + "A rising polyline. Three labels on the lows: Higher low 90, Higher low 100, Higher low 110.",
        _levels(
            "An uptrend makes higher lows",
            "A rising path with higher lows at 90, 100, and 110.",
            [],
            [(200, 700), (480, 560), (760, 620), (1040, 420), (1320, 480)],
            [(180, 760, "Low 90"), (500, 520, "Low 100"), (1000, 360, "Low 110")],
        ),
    )
    add(
        "atlas-structure-02.png",
        "swings",
        "A peak at 120 with 110 on both sides. That peak is a swing high.",
        P + "A peak. Label the top Swing high 120. Label both shoulders 110.",
        _levels(
            "A swing high has lower highs beside it",
            "A peak at 120 with 110 on both sides. That peak is a swing high.",
            [],
            [(200, 560), (520, 300), (860, 560), (1200, 500)],
            [(160, 640, "110"), (500, 250, "Swing high 120"), (860, 640, "110")],
        ),
    )
    add(
        "atlas-structure-03.png",
        "support-resistance",
        "A lower line at 100 called support and an upper line at 130 called resistance.",
        P + "Two horizontal lines. Lower label Support 100. Upper label Resistance 130. A small bounce off the lower line.",
        _levels(
            "Support holds. Resistance stalls.",
            "A lower line at 100 called support and an upper line at 130 called resistance.",
            [(260, "Resistance 130", "#ffb4b4"), (640, "Support 100", "#7dcea0")],
            [(200, 500), (480, 640), (700, 500), (980, 660), (1240, 480)],
        ),
    )
    add(
        "atlas-structure-04.png",
        "market-structure",
        "Higher highs and higher lows. Marks at 110, 130, 120, and 150.",
        P + "A rising swing path. Labels HL 110, HH 130, HL 120, HH 150.",
        _levels(
            "Structure is the sequence of swings",
            "Higher highs and higher lows. Marks at 110, 130, 120, and 150.",
            [],
            [(180, 640), (460, 360), (740, 520), (1100, 240)],
            [(140, 720, "HL 110"), (420, 310, "HH 130"), (700, 600, "HL 120"), (1080, 190, "HH 150")],
        ),
    )
    add(
        "atlas-structure-05.png",
        "break-of-structure",
        "A prior high at 130 and a later close at 134 beyond that high.",
        P + "A horizontal line Prior high 130. A candle close beyond it labelled Close 134. Arrow through the line.",
        _levels(
            "A break continues the sequence",
            "A prior high at 130 and a later close at 134 beyond that high.",
            [(400, "Prior high 130", "#ffb4b4")],
            [(200, 620), (520, 480), (900, 280)],
        ),
    )
    add(
        "atlas-structure-06.png",
        "change-of-character",
        "An uptrend higher low at 110, then a close at 106 under that low.",
        P + "Mark Higher low 110. Show a later close under it labelled Close 106.",
        _levels(
            "A break against the sequence",
            "An uptrend higher low at 110, then a close at 106 under that low.",
            [(420, "Higher low 110", "#7dcea0")],
            [(200, 300), (520, 420), (900, 680)],
        ),
    )
    add(
        "atlas-smart-money-01.png",
        "liquidity",
        "Two equal highs near 130, with a label that stops often sit just above them.",
        P + "Two peaks at the same height. Label Equal highs 130. Label Stops above.",
        _levels(
            "Liquidity sits where stops cluster",
            "Two equal highs near 130, with a label that stops often sit just above them.",
            [(300, "Equal highs 130", "#ffe7a3")],
            [(200, 560), (480, 300), (760, 520), (1040, 300), (1360, 560)],
        ),
    )
    add(
        "atlas-smart-money-02.png",
        "liquidity",
        "A wick pushes to 133 and the close returns to 128.",
        P + "A line at 130, a wick through it to 133, and a close back at 128. Labels Sweep 133 and Close back 128.",
        _levels(
            "A sweep is a push that comes back",
            "A wick pushes to 133 and the close returns to 128.",
            [(340, "Level 130", "#ffe7a3")],
            [(240, 560), (640, 180), (1040, 460)],
        ),
    )
    add(
        "atlas-smart-money-03.png",
        "order-blocks",
        "A small down candle from 102 to 98, then a rise to 120. The small candle is the marked zone.",
        P + "A small red candle, then a strong rise. Bracket the small candle and label Marked zone 98 to 102. Label Rise to 120.",
        _flow(
            "An order block is a marked candle",
            "A small down candle from 102 to 98, then a rise to 120. The small candle is the marked zone.",
            [(160, 420, 280, 200, "Zone 98-102"), (620, 240, 360, 160, "Rise to 120")],
            [(440, 500, 620, 340)],
            [(160, 700, "Marked zone"), (1040, 300, "Later price")],
        ),
    )
    add(
        "atlas-smart-money-04.png",
        "fair-value-gaps",
        "Three candles. Candle 1 high is 100. Candle 3 low is 106. The gap between them is the fair value gap.",
        P + "Three candlesticks. The middle one is large. Arrows label Candle 1 high 100, Candle 3 low 106, and Gap.",
        _flow(
            "A gap between wick and wick",
            "Three candles. Candle 1 high is 100. Candle 3 low is 106. The gap between them is the fair value gap.",
            [(140, 480, 280, 220, "High 100"), (660, 220, 280, 420, "Middle push"), (1120, 180, 300, 180, "Low 106")],
            [(420, 560, 660, 420)],
            [(140, 760, "Candle 1"), (1120, 420, "Gap of 6")],
        ),
    )
    add(
        "atlas-smart-money-05.png",
        "premium-discount",
        "A dealing range from 100 to 140. The middle is 120. 110 is discount. 130 is premium.",
        P + "A vertical range. Bottom 100, mid 120, top 140. Label Discount 110 below the mid and Premium 130 above the mid.",
        _levels(
            "Premium is the top half. Discount is the bottom half.",
            "A dealing range from 100 to 140. The middle is 120. 110 is discount. 130 is premium.",
            [(240, "Premium 130", "#ffb4b4"), (450, "Mid 120", "#ffe7a3"), (660, "Discount 110", "#7dcea0")],
        ),
    )
    add(
        "atlas-smart-money-06.png",
        "inducement",
        "A small high at 125 sits under a larger high at 140.",
        P + "Two peaks. The smaller one labelled Small high 125. The larger one labelled Main high 140.",
        _levels(
            "A small high can lure early buys",
            "A small high at 125 sits under a larger high at 140.",
            [(360, "Small high 125", "#ffe7a3"), (240, "Main high 140", "#ffb4b4")],
            [(200, 640), (520, 360), (820, 560), (1180, 240)],
        ),
    )
    add(
        "atlas-grid-bots-01.png",
        "grid-what",
        "A ladder. Sells sit above the price at 102 and 104. Buys sit below at 98 and 96. The price is 100.",
        P + "Horizontal rungs. Label Sell 104, Sell 102, Price 100, Buy 98, Buy 96.",
        _levels(
            "A grid is a ladder you write in advance",
            "A ladder. Sells sit above the price at 102 and 104. Buys sit below at 98 and 96. The price is 100.",
            [
                (200, "Sell 104", "#ffb4b4"),
                (320, "Sell 102", "#ffb4b4"),
                (460, "Price 100", "#ffe7a3"),
                (600, "Buy 98", "#7dcea0"),
                (720, "Buy 96", "#7dcea0"),
            ],
        ),
    )
    add(
        "atlas-grid-bots-02.png",
        "grid-how",
        "A buy fills at 98 and a later sell fills at 100. The gap is 2 before fees.",
        P + "Two prices, Buy 98 and Sell 100, with an arrow up between them labelled Gap 2.",
        _flow(
            "One cycle is a buy and a later sell",
            "A buy fills at 98 and a later sell fills at 100. The gap is 2 before fees.",
            [(160, 480, 360, 150, "Buy 98"), (900, 260, 360, 150, "Sell 100")],
            [(520, 540, 900, 340)],
            [(620, 620, "Gap 2 before fees")],
        ),
    )
    add(
        "atlas-grid-bots-03.png",
        "grid-setup",
        "Four setup facts: upper 110, lower 90, 10 gaps, and a review rule.",
        P + "Four boxes: Upper 110, Lower 90, Gaps 10, Review on a close outside.",
        _flow(
            "Write the rules before anything runs",
            "Four setup facts: upper 110, lower 90, 10 gaps, and a review rule.",
            [
                (60, 340, 330, 160, "Upper 110"),
                (430, 340, 330, 160, "Lower 90"),
                (800, 340, 330, 160, "Gaps 10"),
                (1170, 340, 360, 160, "Review rule"),
            ],
            [],
            [],
        ),
    )
    add(
        "atlas-grid-bots-04.png",
        "grid-range",
        "Three ranges. A tight box from 100 to 105, a middle box from 90 to 110, and a very wide box from 50 to 150.",
        P + "Three columns labelled Too tight, Room to repeat, and Too thin, with the ranges 100 to 105, 90 to 110, and 50 to 150.",
        _bars(
            "Width is a tradeoff",
            "Three ranges. A tight box from 100 to 105, a middle box from 90 to 110, and a very wide box from 50 to 150.",
            [(180, 140, "Too tight", "100-105"), (620, 320, "Has room", "90-110"), (1060, 520, "Very wide", "50-150")],
        ),
    )
    add(
        "atlas-grid-bots-05.png",
        "grid-range",
        "A step of 2 beside a round-trip fee of 0.20. The step is larger than the fee in this example.",
        P + "Two bars. Tall bar Step 2. Short bar Fee 0.20. Caption that the step clears the fee in this example.",
        _bars(
            "The step has to clear the fee",
            "A step of 2 beside a round-trip fee of 0.20. The step is larger than the fee in this example.",
            [(360, 480, "Step", "2"), (860, 80, "Round-trip fee", "0.20")],
        ),
    )
    add(
        "atlas-grid-bots-06.png",
        "grid-range",
        "Two ladders. The left has equal price gaps. The right has gaps that grow as price rises.",
        P + "Left ladder labelled Equal price gaps. Right ladder labelled Equal percent gaps, with spaces getting taller.",
        _flow(
            "Arithmetic gaps differ from geometric gaps",
            "Two ladders. The left has equal price gaps. The right has gaps that grow as price rises.",
            [(120, 240, 520, 460, "Equal price gaps"), (900, 240, 560, 460, "Equal percent gaps")],
            [],
            [(160, 760, "Same distance"), (940, 760, "Same percentage")],
        ),
    )
    add(
        "atlas-grid-bots-07.png",
        "grid-risk",
        "Finished cycles show plus 20. Unsold coins bought near 94 are now priced at 80.",
        P + "Two cards. Left: Cycle result plus 20. Right: Unsold coins from 94 to 80. An arrow noting they are separate.",
        _flow(
            "Cycle profit is not the whole account",
            "Finished cycles show plus 20. Unsold coins bought near 94 are now priced at 80.",
            [(120, 300, 520, 200, "Cycles plus 20"), (900, 300, 560, 200, "Coins 94 to 80")],
            [],
            [(360, 620, "Keep these apart")],
        ),
    )
    add(
        "atlas-grid-bots-08.png",
        "grid-monitor",
        "The box top is 110 and a later close is 112, which starts a review.",
        P + "Horizontal line Box top 110. A mark above it labelled Close 112 and Review.",
        _levels(
            "Outside the box, open the written rule",
            "The box top is 110 and a later close is 112, which starts a review.",
            [(480, "Box top 110", "#ffe7a3")],
            [(300, 620), (900, 280)],
        ),
    )
    add(
        "atlas-grid-bots-09.png",
        "grid-mistakes",
        "Forty gaps inside 100 to 110 make a step of 0.25, next to a fee of 0.20.",
        P + "Many thin rungs. Labels 40 gaps, Step 0.25, Fee 0.20.",
        _flow(
            "Too many rungs can leave nothing after fees",
            "Forty gaps inside 100 to 110 make a step of 0.25, next to a fee of 0.20.",
            [(140, 300, 360, 160, "40 gaps"), (580, 300, 360, 160, "Step 0.25"), (1040, 300, 400, 160, "Fee 0.20")],
            [(500, 380, 580, 380), (940, 380, 1040, 380)],
            [],
        ),
    )
    add(
        "atlas-leverage-01.png",
        "margin",
        "A notional of 10000 posted with 2000 of margin at 5 times.",
        P + "A large block Notional 10000 and a smaller block Margin 2000. Label 5 times.",
        _bars(
            "Margin is the cash you post",
            "A notional of 10000 posted with 2000 of margin at 5 times.",
            [(300, 520, "Notional", "10000"), (860, 160, "Margin", "2000")],
        ),
    )
    add(
        "atlas-leverage-02.png",
        "leverage-multiples",
        "The price falls 10 percent. On 5 times leverage the margin result is about minus 50 percent.",
        P + "Two arrows down. Short arrow Price minus 10. Long arrow Margin minus 50.",
        _flow(
            "Leverage scales the move",
            "The price falls 10 percent. On 5 times leverage the margin result is about minus 50 percent.",
            [(160, 280, 480, 160, "Price minus 10"), (860, 360, 560, 240, "Margin minus 50")],
            [(640, 360, 860, 460)],
            [],
        ),
    )
    add(
        "atlas-leverage-03.png",
        "liquidation",
        "Entry at 100 and an example long liquidation near 90.5 at 10 times with a 0.5 percent maintenance rate.",
        P + "Two horizontal lines. Entry 100 above. Example liquidation 90.5 below. Label 10 times and maintenance 0.5 percent.",
        _levels(
            "Liquidation is the price that ends the margin",
            "Entry at 100 and an example long liquidation near 90.5 at 10 times with a 0.5 percent maintenance rate.",
            [(300, "Entry 100", "#7dcea0"), (620, "Liquidation 90.5", "#ffb4b4")],
        ),
    )
    add(
        "atlas-leverage-04.png",
        "position-size",
        "Cash at risk 100 divided by a distance of 5 gives a size of 20.",
        P + "Three boxes in a chain: Cash at risk 100, Distance 5, Size 20. Arrows left to right.",
        _flow(
            "Size comes from cash and distance",
            "Cash at risk 100 divided by a distance of 5 gives a size of 20.",
            [(80, 360, 380, 160, "Risk 100"), (560, 360, 380, 160, "Distance 5"), (1080, 360, 400, 160, "Size 20")],
            [(460, 440, 560, 440), (940, 440, 1080, 440)],
            [],
        ),
    )
    add(
        "atlas-futures-01.png",
        "perpetuals",
        "Two contracts. One has no end date. The other ends in 30 days.",
        P + "Two cards. Left: No end date. Right: Ends in 30 days. No venue names.",
        _flow(
            "Perpetual and dated are different clocks",
            "Two contracts. One has no end date. The other ends in 30 days.",
            [(140, 320, 520, 200, "No end date"), (900, 320, 540, 200, "Ends in 30 days")],
            [],
            [(180, 620, "Perpetual"), (940, 620, "Dated")],
        ),
    )
    add(
        "atlas-futures-02.png",
        "funding",
        "A positive funding example of 0.01 percent. On 10000 of notional that is about 1, paid from longs to shorts in this example.",
        P + "An arrow from a Long box to a Short box. Labels Rate 0.01 percent and About 1 on 10000.",
        _flow(
            "Funding is a periodic payment",
            "A positive funding example of 0.01 percent. On 10000 of notional that is about 1, paid from longs to shorts in this example.",
            [(140, 340, 400, 160, "Longs"), (1040, 340, 400, 160, "Shorts")],
            [(540, 420, 1040, 420)],
            [(560, 250, "0.01 percent"), (560, 620, "About 1")],
        ),
    )
    add(
        "atlas-futures-03.png",
        "long-short",
        "Price rises by 10. The long result is plus 10 per unit. The short result is minus 10 per unit, before fees.",
        P + "An up arrow labelled Price plus 10. A card Long plus 10. A card Short minus 10.",
        _flow(
            "Long and short are opposite results",
            "Price rises by 10. The long result is plus 10 per unit. The short result is minus 10 per unit, before fees.",
            [(160, 300, 480, 160, "Long plus 10"), (920, 460, 500, 160, "Short minus 10")],
            [],
            [(620, 220, "Price plus 10")],
        ),
    )
    add(
        "atlas-futures-04.png",
        "hedging",
        "Two coins fall by 10 each, a loss of 20. A short of one coin gains about 10. The net loss is smaller.",
        P + "Card Coins lose 20. Card Short gains 10. Note that the hedge does not erase the whole loss.",
        _flow(
            "A hedge offsets part of a move",
            "Two coins fall by 10 each, a loss of 20. A short of one coin gains about 10. The net loss is smaller.",
            [(120, 300, 520, 180, "Coins lose 20"), (900, 300, 540, 180, "Short gains 10")],
            [],
            [(480, 600, "Net loss is smaller")],
        ),
    )
    add(
        "atlas-derivatives-01.png",
        "options-basics",
        "You pay a premium of 5 for a right. You do not have to use the right. The most you lose in this example is 5.",
        P + "A small stack labelled Premium 5 and a box labelled Right, not a duty.",
        _flow(
            "An option is a right you pay for",
            "You pay a premium of 5 for a right. You do not have to use the right. The most you lose in this example is 5.",
            [(160, 320, 480, 180, "Premium 5"), (900, 320, 520, 180, "A right")],
            [(640, 410, 900, 410)],
            [(480, 620, "Loss can stop at 5")],
        ),
    )
    add(
        "atlas-derivatives-02.png",
        "calls-puts",
        "A call with strike 100 and premium 5. At a price of 110 the example profit is 5.",
        P + "A call payoff line that is flat then rises after strike 100. Labels Strike 100, Premium 5, Profit 5 at price 110.",
        _payoff(
            "Call payoff, in this example",
            "A call with strike 100 and premium 5. At a price of 110 the example profit is 5.",
            [(200, 620), (700, 620), (1300, 220)],
            [(720, 700, "Strike 100"), (200, 560, "Premium 5"), (1100, 180, "Profit 5")],
        ),
    )
    add(
        "atlas-derivatives-03.png",
        "calls-puts",
        "A put with strike 100 and premium 5. At a price of 90 the example profit is 5.",
        P + "A put payoff line that falls as price rises, then goes flat after strike 100. Labels Strike 100, Premium 5, Profit 5 at price 90.",
        _payoff(
            "Put payoff, in this example",
            "A put with strike 100 and premium 5. At a price of 90 the example profit is 5.",
            [(200, 220), (800, 620), (1400, 620)],
            [(820, 700, "Strike 100"), (1040, 560, "Premium 5"), (220, 180, "Profit 5")],
        ),
    )
    add(
        "atlas-derivatives-04.png",
        "greeks",
        "Four plain meanings. Delta 0.50, gamma is the change in delta, theta 0.20 a day, vega 0.10.",
        P + "Four cards labelled Delta 0.50, Gamma, Theta 0.20, Vega 0.10. No formulas crowded on the picture.",
        _flow(
            "Greeks are sensitivities",
            "Four plain meanings. Delta 0.50, gamma is the change in delta, theta 0.20 a day, vega 0.10.",
            [
                (80, 280, 320, 180, "Delta 0.50"),
                (460, 280, 320, 180, "Gamma"),
                (840, 280, 320, 180, "Theta 0.20"),
                (1220, 280, 320, 180, "Vega 0.10"),
            ],
            [],
            [],
        ),
    )
    add(
        "atlas-derivatives-05.png",
        "basis",
        "Spot at 100 and a futures price at 103. The basis is 3.",
        P + "Two horizontal lines. Spot 100 and Futures 103. A bracket labelled Basis 3.",
        _levels(
            "Basis is futures minus spot",
            "Spot at 100 and a futures price at 103. The basis is 3.",
            [(360, "Futures 103", "#8fe7ff"), (520, "Spot 100", "#ffe7a3")],
        ),
    )
    add(
        "atlas-professional-01.png",
        "trade-plans",
        "A plan card with entry 100, stop 95, cash risk 100, and target 110.",
        P + "One card with four lines: Entry 100, Stop 95, Risk 100, Target 110.",
        _flow(
            "Write the plan before the click",
            "A plan card with entry 100, stop 95, cash risk 100, and target 110.",
            [(360, 240, 860, 420, "Entry 100")],
            [],
            [(420, 420, "Stop 95"), (820, 420, "Risk 100"), (420, 560, "Target 110")],
        ),
    )
    add(
        "atlas-professional-02.png",
        "journaling",
        "Ten example results. Six are wins. Expectancy in this sample is 0.5 R.",
        P + "A small table sketch. Label 6 wins of 10. Label Expectancy 0.5 R.",
        _flow(
            "A journal turns results into a sample",
            "Ten example results. Six are wins. Expectancy in this sample is 0.5 R.",
            [(160, 300, 560, 200, "6 wins of 10"), (860, 300, 560, 200, "Expectancy 0.5 R")],
            [(720, 400, 860, 400)],
            [],
        ),
    )
    add(
        "atlas-professional-03.png",
        "risk-of-ruin",
        "Ten losses at 1 percent leave about 90 percent of the account. Ten losses at 10 percent leave about 35 percent.",
        P + "Two falling paths. Gentle path labelled 1 percent risk. Steep path labelled 10 percent risk.",
        _levels(
            "Big risk makes a losing streak deeper",
            "Ten losses at 1 percent leave about 90 percent of the account. Ten losses at 10 percent leave about 35 percent.",
            [],
            [(200, 240), (700, 300), (1200, 360)],
            [(180, 200, "1 percent risk"), (160, 640, "10 percent risk")],
            extra_paths=[([(200, 260), (700, 520), (1200, 760)], "#ffb4b4")],
        ),
    )
    add(
        "atlas-professional-04.png",
        "psychology",
        "The written plan stays at 1 percent. The urge after two losses wants a bigger size. The urge is not a new plan.",
        P + "Two boxes. Plan stays 1 percent. Urge to double. A note that the urge is not a new plan.",
        _flow(
            "A feeling is not a new rule",
            "The written plan stays at 1 percent. The urge after two losses wants a bigger size. The urge is not a new plan.",
            [(120, 320, 560, 180, "Plan stays 1 percent"), (880, 320, 560, 180, "Urge to double")],
            [],
            [(460, 620, "Urge is not a plan")],
        ),
    )
    add(
        "atlas-professional-05.png",
        "building-a-system",
        "Four parts of a small system: one market, one setup, one risk rule, and one review day.",
        P + "Four boxes in a row labelled Market, Setup, Risk rule, Review day. Arrows between them.",
        _flow(
            "A system is four written lines",
            "Four parts of a small system: one market, one setup, one risk rule, and one review day.",
            [
                (60, 360, 320, 150, "Market"),
                (430, 360, 320, 150, "Setup"),
                (800, 360, 320, 150, "Risk rule"),
                (1170, 360, 360, 150, "Review day"),
            ],
            [(380, 435, 430, 435), (750, 435, 800, 435), (1120, 435, 1170, 435)],
            [],
            badge=False,
        ),
    )


build()
