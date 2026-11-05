"""Beat-to-illustration prompts for ChatGPT images.

Code may later add captions, lower thirds, and Ken Burns motion.
The image itself has to teach the beat with the sound off.
"""

from __future__ import annotations

import re

STYLE = (
    "Flat educational vector illustration for a YouTube tutorial, 16:9, 1536x1024. "
    "Deep navy background from #050A12 to #0A1628, faint cyan grid, crisp cyan #00D4FF linework, "
    "electric blue #1E5EFF fills, off-white rounded panels, dark navy text on the panels. "
    "Calm and technical, like a worksheet, not a poster. "
    "The bottom fifth of the frame is empty dark navy so captions can sit there. "
    "At most four short English labels, one to three words each, spelled exactly as given. "
    "If a chart appears, stamp the word Example on it. "
    "No coins, banknotes, profit, P&L, trophies, rockets, brand logos, exchange names, "
    "logins, seed phrases, API keys, photoreal faces, or a chart that only goes up. "
    "A generic illustrated panel is fine. A real app screenshot is not."
)

LAYOUTS = (
    "One large diagram centered on an off-white panel, with thin cyan callout lines.",
    "Two panels side by side: the left panel is the idea done clearly, the right panel is the same idea done wrong and faded.",
    "Three numbered steps across the panel, left to right, each step a simple shape.",
    "An annotated chart scene: a sideways price path, horizontal levels, and two callouts.",
    "A step-by-step illustrated form, generic and unbranded, with one field highlighted in cyan.",
)

STYLE_TEAL = (
    "Flat educational vector illustration for a YouTube tutorial, 16:9, 1536x1024. "
    "Deep navy background from #050A12 to #0A1628, faint teal grid, crisp teal #2EE6A6 linework, "
    "medium blue #3E73B4 fills, off-white rounded panels, dark navy text on the panels. "
    "This is the Grid Bot Elite teal palette. Do not recolor the linework to cyan #00D4FF. "
    "Calm and technical, like a worksheet, not a poster. "
    "The bottom fifth of the frame is empty dark navy so captions can sit there. "
    "At most four short English labels, one to three words each, spelled exactly as given. "
    "If a chart appears, stamp the word Example on it. "
    "No coins, banknotes, profit, P&L, trophies, rockets, brand logos, exchange names, "
    "logins, seed phrases, API keys, photoreal faces, or a chart that only goes up. "
    "A generic illustrated panel is fine. A real app screenshot is not."
)

LAYOUTS_TEAL = (
    "One large diagram centered on an off-white panel, with thin teal callout lines.",
    "Two panels side by side: the left panel is the idea done clearly, the right panel is the same idea done wrong and faded.",
    "Three numbered steps across the panel, left to right, each step a simple shape.",
    "An annotated chart scene: a sideways price path, horizontal levels, and two callouts.",
    "A step-by-step illustrated form, generic and unbranded, with one field highlighted in teal.",
)


def _labels(concept: str, extra: list[str] | None = None) -> list[str]:
    found = re.findall(r"\b([A-Z][A-Za-z]{2,12}|LTV|HF|AMM|DEX|MEV|TWAP)\b", concept)
    labels: list[str] = []
    for word in (extra or []) + found:
        clean = re.sub(r"[^A-Za-z0-9 .+%-]", "", word).strip()
        if clean and clean not in labels and len(clean) <= 18:
            labels.append(clean)
        if len(labels) == 4:
            break
    return labels


def _scene(concept: str, chapter: str, role: str) -> str:
    c = concept.lower()
    parts: list[str] = []
    rules = (
        (("sideways", "chop", "weave", "rotat"),
         "a cyan price path weaving through six horizontal levels, inside a band on the left and stepping out through the lower line on the right"),
        (("range", "band", "upper", "lower"),
         "a price band drawn as two horizontal cyan lines labelled Upper and Lower, with the word Range on a small tag"),
        (("gap", "spacing", "order count", "nineteen"),
         "nineteen even gaps between twenty horizontal lines, the gaps marked, the lines only the edges of the gaps, a small note that counting lines is the miss"),
        (("stop", "invalidat", "leave"),
         "a dashed stop line below the band, and a price path that leaves the band and does not return"),
        (("limit order", "limit"),
         "markers waiting on horizontal levels, and a second faded arrow that wrongly cuts straight through the levels"),
        (("buy", "sell"),
         "buy markers on levels below a centre line and sell markers on levels above it"),
        (("regime", "trend", "breakout"),
         "three small charts in a row labelled Range, Trend, and Break, only the first one weaving inside a band"),
        (("fee", "round trip", "cost"),
         "one gap drawn wider than a two-way fee bar, and a second gap drawn thinner than that bar and crossed out"),
        (("liquidat", "margin", "leverage", "isolated", "cross"),
         "two columns labelled Isolated and Cross: the first box holds only its own inventory, the second box has a line reaching into a neighbouring box; a price path leaving the band"),
        (("health", "ltv", "collateral", "debt"),
         "a balance diagram: a collateral bar, a shorter debt bar, and a health marker that drops when the debt bar grows"),
        (("wallet", "key", "seed", "hardware"),
         "a hardware key beside a crossed-out speech bubble, showing a secret that is never typed into a page"),
        (("approval", "allowance", "token"),
         "a token moving only as far as a permission gate, with a second gate left wide open and marked as the miss"),
        (("stable",),
         "a peg line at a fixed height and a second path that slips off the peg, labelled as a break"),
        (("gas", "transaction", "mempool", "signature"),
         "a four-step path from a wallet, to a node, to a waiting pool, to a block, one step lit"),
        (("sopr", "spent output", "coins moved"),
         "a horizontal line labelled One, dots sitting above the line and dots sitting below it, stamped Example, with no currency symbols and no result number"),
        (("p&l",),
         "two bars labelled Pool and Hold, the pool bar shorter after a price move away from the start, both stamped Example, with no result number on either bar"),
        (("liquidity", "pool", "amm", "impermanent"),
         "a two-sided pool with an x times y curve, deposits as arrows in, and a price move that changes the mix of the two sides"),
        (("mev", "sandwich", "slippage"),
         "a trade arrow with a thin sandwich of two extra arrows around it, and a slippage band on the price"),
        (("oracle", "twap"),
         "a spot price spike beside a slower average line that barely moves"),
        (("bridge", "chain"),
         "two chains with a bridge between them and a trust mark on the bridge, not a guaranteed arrival"),
        (("utilis", "kink", "borrow", "lend", "supply"),
         "a kinked rate curve, gentle then steep, with utilisation marked before the kink and after it"),
        (("checklist", "paper", "notebook", "worksheet"),
         "an open notebook page with a short checklist, one row highlighted, next to the diagram it describes"),
        (("monitor", "cadence", "alert"),
         "a three-row review card: inside the band, inventory side, and the written stop, with a calendar chip"),
        (("mistake", "miss"),
         "a two-panel miss: a blank stop on the left, a clean written stop on the right"),
        (("scale", "bucket", "inventory bucket"),
         "two separate inventory buckets for two grids, with a warning when the buckets overlap on the same asset"),
        (("correlation", "drawdown ceiling", "per-coin"),
         "three checks on one card: a ceiling sentence, a per-coin cap, and two paths that travel together, stamped Example"),
        (("circuit", "band edge", "pause"),
         "a hand switch labelled Pause beside a band-edge mark, and a separate box labelled Venue close"),
        (("counterparty", "second venue"),
         "two venue boxes, the second one marked Halt, with separate inventory notes and no split ratio"),
        (("paper plan",),
         "an open notebook with five written rows: range, spacing, count, inventory, stop, and a line that says no deposit"),
    )
    for keys, picture in rules:
        if any(k in c for k in keys):
            parts.append(picture)
    if not parts:
        parts.append(
            "a labelled diagram whose shapes are the nouns in this exact line, not a generic document: "
            + concept.strip().rstrip(".")
        )
    if role in {"demo", "action"}:
        parts.append("a pencil completing the matching line on a notebook beside the diagram")
    if role == "hook":
        parts.append("the problem visible in the first glance, before any logo")
    if role == "recap":
        parts.append("three short recap rows, each row a tiny diagram plus a two-word label")
    if role == "outro":
        parts.append("a quiet next-step card with a single arrow to a blank next title, no price and no button that buys anything")
    chapter_bit = f"Chapter context: {chapter}." if chapter else ""
    return chapter_bit + " Show " + "; ".join(parts[:3]) + "."


def write_prompt(concept: str, chapter: str, role: str, beat_n: int, lesson_title: str,
                 labels: list[str] | None = None, palette: str = "navy-cyan") -> str:
    """One detailed prompt. The beat number is included so two similar beats cannot collapse."""
    labs = _labels(concept, labels)
    if role in {"demo", "diagram", "body"} and "Example" not in labs and any(
        k in concept.lower() for k in ("chart", "price", "band", "level", "gap", "ltv", "health")
    ):
        labs = (["Example"] + labs)[:4]
    label_line = "Labels, spelled exactly: " + ", ".join(labs) + "." if labs else "Use no words if a shape is clearer."
    teal = palette == "teal"
    layout = (LAYOUTS_TEAL if teal else LAYOUTS)[beat_n % 5]
    scene = _scene(concept, chapter, role)
    if teal:
        scene = scene.replace("cyan", "teal")
    style = STYLE_TEAL if teal else STYLE
    return (
        f"Lesson '{lesson_title}', beat {beat_n}, role {role}. {layout} {scene} "
        f"The picture must be understandable with the sound off. Teaching line: {concept.strip()} "
        f"{label_line} {style}"
    )
