"""Beat plans for BP-03 to BP-11. No film is rendered.

Each paragraph is packed so no beat runs longer than 8 seconds at 163 words
a minute. That is the minimum picture count. Charts, ladders, forms and
lockups stay code. A beat with no figure, and that is not a title,
disclaimer or end card, is marked for a ChatGPT image. The 180 old
fallback stills are not reused.
"""

from __future__ import annotations

import json
import math
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
APPROVED = ROOT / "course/approved-scripts-25nov"
OUT = ROOT / "course/visuals-25nov"
WPM = 163
MAX_WORDS = max(8, int(7.8 * WPM / 60))

FLOORS = {
    "03": 112,
    "04": 94,
    "05": 87,
    "06": 92,
    "07": 90,
    "08": 94,
    "09": 89,
    "10": 91,
    "11": 103,
}

NEXT = {
    "03": "Market regimes",
    "04": "Choosing grid spacing and range",
    "05": "Entry and exit rules",
    "06": "Spot paper trading",
    "07": "Managing and monitoring",
    "08": "Common mistakes",
    "09": "Scaling up on spot",
    "10": "Optional wrap-up: the spot page, and what this course does not cover",
    "11": "End of the Blueprint. The spot page stands.",
}

NOTES = {
    "03": (
        "Self-check is four questions, and the answers stay off the card until the answer sentence. "
        "1. What is a limit order? 2. Which side of 27,630 is the buy side? "
        "3. How many gaps are there between seven levels? 4. What is ten crosses of the middle? "
        "The end lockup names the next lesson: Market regimes."
    ),
    "04": (
        "Two chart windows besides the summer range: crash_2020 (11–13 March 2020, including the 13 March candle) "
        "and the later path from 23 October 2023 (33,086) to 14 March 2024 (71,397). "
        "The header's seventh visual, a separate 13 March candle card, is not a seventh pass-list card. "
        "That candle is drawn on the March 2020 card, so the plan stays at the pass list's 6 cards."
    ),
    "05": (
        "The cost card prints the fee as 0.2673 + 0.2763 = 0.5436, not a rounded substitute. "
        "Both ladders are on the plan: 100, 125, 150, 175, 200 and 100, 118.9, 141.4, 168.2, 200. "
        "The fee paragraph is split into beats under 8 seconds. It does not sit on one card for 71 seconds."
    ),
    "06": (
        "The pass list has 4 cards. This plan adds two code cards, so the lesson has more than four heroes: "
        "the order of the lines (finish, then before, then a blank size) and, only after the word is spoken, "
        "the ceiling arithmetic (600 across 6 orders is 100). No card prints ceiling before that word."
    ),
    "07": (
        "The form is exchange-neutral: no logo, no login, no balance. "
        "The wrong form (seven grids, a size already typed, no sentence) sits beside the right form "
        "(six gaps, no size, two sentences)."
    ),
    "08": (
        "The stop card uses the three-question rule. It does not say two questions. "
        "Once the closing price is outside, which side is not asked, and then you close the page. "
        "The end lockup names the next lesson: Common mistakes."
    ),
    "09": (
        "Show the page being fixed: the blank stop filled, the round top corrected, the gap count changed from seven to six. "
        "No slogan chips. No label under 28 px."
    ),
    "10": (
        "Page two is second_range_2024, 56,555 to 72,715, 27 March 2024 to 24 June 2024. "
        "It is not the summer chart and it is not titled 19 July 2023 to 16 October 2023. No 2020 chart."
    ),
    "11": (
        "Do not use the old liquidation stills. The skip card says \"Skipped on purpose. The spot page stands.\" "
        "and does not define margin, liquidation, isolated, or cross. "
        "When the voice says 56,555 and 72,715, the picture is second_range_2024. No 2020 chart."
    ),
}

EXTRA_HEROES = {
    "06": [
        (
            "05.png",
            "Order of the lines: finish, then the before sentence, then the size line left blank. The word ceiling is not on this card.",
        ),
        (
            "06.png",
            "After the word ceiling has been spoken: a ceiling of 600 dollars across 6 orders is 100 dollars an order. Example only. Not a size for your account.",
        ),
    ],
    "08": [
        (
            "04.png",
            "A stop card on the three-question rule. Inside, which side, and whether the rule is still in force. Once the closing price is outside, which side is not asked, and then you close the page.",
        ),
    ],
}


def spoken_body(text: str) -> str:
    return text.split("## Spoken script", 1)[1].strip()


def paragraphs(body: str) -> list[str]:
    return [part.strip() for part in re.split(r"\n\s*\n", body) if part.strip()]


def sentences(paragraph: str) -> list[str]:
    parts = re.split(r"(?<=[.?!])\s+", paragraph.strip())
    return [part.strip() for part in parts if part.strip()]


def pack_paragraph(paragraph: str) -> list[str]:
    """The fewest beats that keep this paragraph from holding longer than 8 seconds."""
    words = paragraph.split()
    if not words:
        return []
    seconds = len(words) / WPM * 60
    count = max(1, math.ceil(seconds / 8))
    size = math.ceil(len(words) / count)
    while size / WPM * 60 > 8:
        count += 1
        size = math.ceil(len(words) / count)
    chunks = []
    for start in range(0, len(words), size):
        piece = words[start:start + size]
        if piece:
            chunks.append(" ".join(piece))
    return chunks


def figures(text: str) -> bool:
    return bool(re.search(r"\d", text))


def window_for(number: str, text: str) -> str:
    low = text.lower()
    if number in {"10", "11"} and ("56,555" in text or "72,715" in text or "16,160" in text):
        return "second_range_2024"
    if number in {"10", "11"} and any(token in text for token in ("7,911", "4,971", "5,838", "March 2020")):
        return "none — do not draw a 2020 chart"
    if number == "04" and any(token in text for token in ("7,911", "4,971", "5,838", "4,107", "5,564", "1,731", "March 2020")):
        return "crash_2020"
    if number == "04" and ("71,397" in text or "14 March 2024" in low):
        return "later path, 23 Oct 2023 to 14 Mar 2024"
    if figures(text):
        return "summer 2023, only the figures in this beat"
    return "none"


def kind_for(number: str, text: str, index: int, ceiling_spoken: bool) -> tuple[str, str, str]:
    """Return visual, source, chatgpt yes/no."""
    low = text.lower()
    if index == 0 or text.startswith("GridBot Builder"):
        return "code title card, signed heading", "code", "no"
    if text.startswith("Education only") or text.startswith("Not financial advice") or text.startswith("Past performance"):
        return "code disclaimer card", "code", "no"
    if text.startswith("Next lesson"):
        return f"code end lockup. Next lesson: {NEXT[number]}", "code", "no"
    if number == "07" and ("wrong form" in low or "right form" in low):
        return "code pair of forms, wrong beside right. No logo. No balance.", "code", "no"
    if number == "11" and ("skipped on purpose" in low or "does not cover" in low or "margin" in low):
        return "code skip card: Skipped on purpose. The spot page stands. No definition of margin, liquidation, isolated, or cross.", "code", "no"
    if number == "09" and any(phrase in low for phrase in ("blank stop", "round top", "counted as a gap", "common mistake")):
        return "code page being corrected. No slogan chip. Labels at 28 px or larger.", "code", "no"
    if number == "08" and "which side" in low and "no longer" in low:
        return "code three-question card. Which side is not asked once the closing price is outside.", "code", "no"
    if figures(text):
        return f"code chart or ladder. Window: {window_for(number, text)}.", "code", "no"
    if any(word in low for word in ("range", "trend", "break", "cross", "fill", "limit order", "market order")):
        return "code diagram of the words in this beat", "code", "no"
    return (
        "Illustration of this beat. Show the idea. Do not print the sentence as the picture. No slogan chip.",
        "ChatGPT",
        "yes",
    )


def heroes(number: str) -> list[tuple[str, str, str]]:
    listing = json.loads((APPROVED / f"BP-{number}-PASS-LIST-APPROVED.json").read_text())
    rows = []
    for image in listing["images"]:
        name = Path(image["path"]).name
        label = image["label"]
        if number == "08" and name == "04.png":
            label = EXTRA_HEROES["08"][0][1]
            rows.append((name, label, "pass list said two questions; the picture uses the three-question rule"))
            continue
        rows.append((name, label, "pass-list label, word for word"))
    for name, label in EXTRA_HEROES.get(number, []):
        if number == "08":
            continue
        rows.append((name, label, "added so this lesson has more than the pass-list card count"))
    return rows


def plan(number: str) -> dict:
    raw = (APPROVED / f"BP-{number}-APPROVED.md").read_text(encoding="utf-8")
    title = raw.splitlines()[0].lstrip("# ").strip()
    body = spoken_body(raw)
    rows = []
    clock = 0.0
    ceiling_spoken = False
    longest = 0.0
    for paragraph in paragraphs(body):
        for beat in pack_paragraph(paragraph):
            seconds = len(beat.split()) / WPM * 60
            longest = max(longest, seconds)
            visual, source, chatgpt = kind_for(number, beat, len(rows), ceiling_spoken)
            if "ceiling" in beat.lower():
                ceiling_spoken = True
            problems = []
            if seconds > 8:
                problems.append("hold over 8s")
            if number in {"10", "11"} and "2020" in window_for(number, beat):
                problems.append("2020 chart on a lesson that does not use it")
            rows.append({
                "n": len(rows) + 1,
                "start": clock,
                "seconds": seconds,
                "sentence": beat,
                "visual": visual,
                "window": window_for(number, beat),
                "chatgpt": chatgpt,
                "source": source,
                "gate": "pass" if not problems else "FAIL " + "; ".join(problems),
            })
            clock += seconds
    floor = FLOORS[number]
    lines = [
        f"# BP-{number} visual manifest",
        "",
        f"Title: {title}",
        "",
        f"Spoken words: {len(body.split())}. Pace: 163 words a minute. Runtime: {clock / 60:.2f} min.",
        "",
        "No film was rendered. This is the beat plan Creative Studio batches against.",
        f"Readiness floor: {floor} beats. This approved script needs {len(rows)} beats so no beat is longer than 8 seconds. Longest beat: {longest:.1f}s.",
        "",
        NOTES[number],
        "",
        "Do not reuse the 180 old fallback stills. They belong to the old scripts.",
        "A ChatGPT beat is an illustration. Charts, ladders, forms, disclaimer, title and the end lockup stay code.",
        "There is no corner EXAMPLE chip and no untaught figure. A number is on screen only when this beat says it.",
        "",
        f"Hero cards: {len(heroes(number))}. Beats: {len(rows)}. ChatGPT images needed: {sum(row['chatgpt'] == 'yes' for row in rows)}. Fallback images: 0.",
        "",
        "## Hero cards",
        "",
        "| File | Card text | Why this text | Source | ChatGPT |",
        "|---|---|---|---|---|",
    ]
    for name, label, why in heroes(number):
        lines.append(f"| `heroes/{name}` | {label.replace('|', '/')} | {why} | code | no |")
    lines.extend([
        "",
        "## Beats",
        "",
        "| # | Start | Seconds | Sentence | Visual | Chart window | ChatGPT image | Source | Gate |",
        "|---|---:|---:|---|---|---|---|---|---|",
    ])
    for row in rows:
        sentence = row["sentence"].replace("|", "/")
        lines.append(
            f"| {row['n']} | {row['start']:.1f} | {row['seconds']:.1f} | {sentence} | {row['visual']} | {row['window']} | {row['chatgpt']} | {row['source']} | {row['gate']} |"
        )
    chatgpt_rows = [str(row["n"]) for row in rows if row["chatgpt"] == "yes"]
    lines.extend([
        "",
        f"ChatGPT batch, beat numbers: {', '.join(chatgpt_rows) if chatgpt_rows else 'none'}.",
        "",
        "Creative Studio scores these before any render. Nothing here is marked pass.",
        "",
    ])
    path = OUT / f"BP-{number}" / "MANIFEST.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")
    return {
        "beats": len(rows),
        "floor": floor,
        "chatgpt": len(chatgpt_rows),
        "heroes": len(heroes(number)),
        "longest": round(longest, 2),
        "fails": sum(row["gate"] != "pass" for row in rows),
    }


def main() -> None:
    summary = {number: plan(number) for number in FLOORS}
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
