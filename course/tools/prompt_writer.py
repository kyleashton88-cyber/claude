"""Beat-to-illustration prompts for ChatGPT images.

Code may later add captions, lower thirds, and Ken Burns motion.
The image itself has to teach the beat with the sound off.
"""

from __future__ import annotations

import re

STYLE = (
    "Premium course still, 16:9, 1536x1024. "
    "Near-black navy background, faint cyan grid, glowing cyan glass cards with rim light and depth. "
    "Not flat, not matte grey, not an off-white paper card. "
    "The top 80 pixels and the bottom 80 pixels are empty background only. "
    "At most four short English labels, one to three words each, spelled exactly as given. "
    "If a chart appears, it moves sideways and is stamped Example. "
    "No coins other than BTC, ETH and USDT, no banknotes, no profit, no trophies, no rockets, "
    "no brand logos, no exchange names, no logins, no seed phrases, no API keys, no photoreal faces. "
    "A generic glass panel is fine. A real app screenshot is not."
)

LAYOUTS = (
    "One large diagram centered on a glowing glass card, with thin cyan callout lines.",
    "Two panels side by side: the left panel is the idea done clearly, the right panel is the same idea done wrong and faded.",
    "Three numbered steps across the panel, left to right, each step a simple shape.",
    "An annotated chart scene: a sideways price path, horizontal levels, and two callouts.",
    "A step-by-step illustrated form, generic and unbranded, with one field highlighted in cyan.",
)

STYLE_TEAL = (
    "Premium Grid Bot Elite still, 16:9, 1536x1024. "
    "Near-black navy with teal glow, faint teal grid, frosted teal glass cards and rim light. "
    "Not flat navy, not matte grey, not an off-white paper card. Never recolor the glow to cyan #00D4FF. "
    "The top 80 pixels and the bottom 80 pixels are empty background only. "
    "At most four short English labels, one to three words each, spelled exactly as given. "
    "If a chart appears, it moves sideways and is stamped Example. "
    "Coins are BTC, ETH and USDT only. No banknotes, no profit, no trophies, no rockets, "
    "no brand logos, no exchange names, no logins, no seed phrases, no API keys, no photoreal faces. "
    "A glass panel is fine. A real app screenshot is not."
)

# Creative Studio v3b, 5 Nov 2026. These rules apply to every still.
HARD_RULES = (
    "Hard rules: no text beyond the named headline and labels. "
    "No branding, no byline, no 'BY STEWART CROWN', no course headers, no logos, "
    "no extra sub-labels, no sentences. "
    "Charts go sideways or are left out. No rising charts or arrows, and no $ axes or $ text. "
    "Coins are BTC, ETH and USDT only, at most 3 per vault. No gold coins. "
    "Coin rims are plain, with no text. "
    "Never duplicate a coin type where the beat says single, lone or independent. "
    "The background is one seamless pass. No paper blocks. "
    "Nothing in the top 80px or the bottom 80px. "
    "Elite uses teal glass cards and glow only, never flat navy or matte grey. "
    "From el-08 onward, match course/images/_anchors/elite-teal-anchor.png, the passed el-08 shot 28: "
    "deep navy, electric teal wireframe glass, faint grid and bokeh. "
    "No flat off-white card, no soft mint wash, and no grey-blue fog. "
    "Blueprint and On-Chain Operator use the same glass and glow in cyan. "
    "If a robot appears, it has straight visor-bar eyes and no smile, matching the passed el-06 shot 28. "
    "A toggle is OFF, knob left and track unlit, unless the label says otherwise. "
    "The picture must match its labels. "
    "A variant must differ from its sibling on the named axis. "
    "That difference is stated first, for example 'DIFFERENT FROM the centred sibling: subject at 80% scale, left of centre' "
    "or 'all except the key element dimmed to 25%'. Do not redraw the sibling. "
    "Image quality must not degrade at any stage: no compression artifacts, no loss of detail, "
    "no colour shift, no softening of labels or text; full resolution preserved from generation "
    "through to the final 1080p video frame."
)

# Stated first so a variant cannot collapse into a copy of its sibling.
VARIANTS = (
    "VARIANT, base: hero centred.",
    "DIFFERENT FROM the centred sibling: subject at 80% scale, left of centre, with a glow trail to the right.",
    "DIFFERENT FROM the centred sibling: all except the key element dimmed to 25%.",
    "DIFFERENT FROM the centred sibling: the key element is a glowing wireframe, not a solid render.",
    "DIFFERENT FROM the centred sibling: hero at 60% scale with deep fog and bokeh.",
    "DIFFERENT FROM the centred sibling: a faint empty glass card on the left and the hero card on the right.",
)

LAYOUTS_TEAL = (
    "One large diagram centered on a glowing teal glass card, with thin teal callout lines.",
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
    variant = VARIANTS[beat_n % len(VARIANTS)]
    scene = _scene(concept, chapter, role)
    if teal:
        scene = scene.replace("cyan", "teal")
    style = STYLE_TEAL if teal else STYLE
    return (
        f"{variant} Lesson '{lesson_title}', beat {beat_n}, role {role}. {layout} {scene} "
        f"The picture must be understandable with the sound off. Teaching line: {concept.strip()} "
        f"{label_line} {style} {HARD_RULES}"
    )
