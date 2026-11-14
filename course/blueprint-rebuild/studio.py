#!/usr/bin/env python3
"""Rebuild one Grid Bot Blueprint lesson as a 1080p teaching film.

Narration is natural-voice, Kokoro af_heart. The mix is lib/mix.py
(voice -14 LUFS / -1 dBTP, music 20 dB under, then one sidechain).
Word-timed captions, chapters, and the template end card are written
with the picture. The quality gate (format blueprint) runs last and a
fail stops the build. No image is drawn unless the pass list marks it
pass. No mail, no SMTP, no paid speech API.

  python3 course/blueprint-rebuild/studio.py --id bp-01-introduction
  python3 course/blueprint-rebuild/studio.py --id bp-01-introduction --excerpt 32 --pass-list fixture.json
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import subprocess
import sys
from functools import lru_cache
from pathlib import Path

import numpy as np
import soundfile as sf
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "course/skills"))

W, H = 1920, 1080
FPS = 30
NAVY = (7, 12, 22)
NAVY2 = (12, 22, 40)
CYAN = (0, 212, 255)
WHITE = (236, 241, 247)
DIM = (176, 196, 214)
AMBER = (255, 176, 32)
MUTED = (154, 168, 188)
BLUE = (30, 123, 255)
MINT = (79, 209, 165)
TAG = (10, 20, 40)
GLASS = (9, 22, 40)
LINE = (28, 64, 88)
FONT_DIR = ROOT / "skills/video-production/fonts/inter"
FONT = FONT_DIR / "Inter-Bold.ttf"
FONT_MED = FONT_DIR / "Inter-Medium.ttf"
FONT_REG = FONT_DIR / "Inter-Regular.ttf"
MX, MY = 96, 64
RIGHT = W - MX - 16
DISCLAIMER = (
    "Education only. Not financial advice. "
    "This is general information and doesn't consider your objectives, financial situation or needs. "
    "Crypto is high risk. You could lose all the money you put in."
)
DISCLAIMER_LINES = (
    "Education only. Not financial advice.",
    "This is general information and doesn't consider your objectives, financial situation or needs.",
    "Crypto is high risk. You could lose all the money you put in.",
)
FOOT = "Education only. Not financial advice."
COVER = ROOT / "course/images/style-ref/01M6MSHVNHX3WQH81XS8KQK1HT.png"
# Drop-in sheet. No crop. Replace the file to change the character.
MASCOT_SRC = ROOT / "course/images/mascot/blueprint-mascot.png"
WORD_BOX = (260, 52, 760, 176)
MAX_SHOT = 8.0
STILLS = {
    "ladder": ROOT / "course/images/blueprint-analogies/analogy-ladder.png",
    "fence": ROOT / "course/images/blueprint-analogies/analogy-fence.png",
    "list": ROOT / "course/images/blueprint-analogies/analogy-list.png",
    "buckets": ROOT / "course/images/blueprint-analogies/analogy-buckets.png",
}
BANNED = re.compile(
    r"market\s+pros|stewart|crown\s+crypto|consultants|\bABN\b|\bACN\b|\bAFSL\b|"
    r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}|"
    r"thanks for watching|see you|subscribe|cheers|yours sincerely",
    re.I,
)
OUT = ROOT / "course/blueprint-rebuild/masters"


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


lesson_scripts = _load("lesson_scripts", ROOT / "course/blueprint-rework/lesson_scripts.py")
speech = _load("speech", ROOT / "course/skills/motion_picture/speech.py")


@lru_cache(maxsize=32)
def font(size: int, weight: str = "bold") -> ImageFont.FreeTypeFont:
    path = {"bold": FONT, "semi": FONT_MED, "reg": FONT_REG}[weight]
    if not path.is_file():
        raise SystemExit(f"bundled OFL font missing: {path}")
    return ImageFont.truetype(str(path), size)


def wrap(text: str, size: int, width: int, weight: str = "bold") -> list[str]:
    face = font(size, weight)
    lines: list[str] = []
    cur = ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if face.getlength(trial) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit_size(text: str, width: int, start: int, floor: int = 36, weight: str = "bold") -> int:
    size = start
    while size > floor and font(size, weight).getlength(text) > width:
        size -= 2
    return size


def ease(t: float) -> float:
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)


def knockout(im: Image.Image, thresh: float = 28) -> Image.Image:
    """Clear background connected to the edges. Keep the visor, which is enclosed."""
    from collections import deque

    arr = np.asarray(im.convert("RGB"))
    h, w, _ = arr.shape
    dark = arr.max(axis=2) < thresh
    seen = np.zeros((h, w), dtype=bool)
    q: deque[tuple[int, int]] = deque()
    for x in range(w):
        q.append((0, x))
        q.append((h - 1, x))
    for y in range(h):
        q.append((y, 0))
        q.append((y, w - 1))
    while q:
        y, x = q.popleft()
        if y < 0 or x < 0 or y >= h or x >= w or seen[y, x] or not dark[y, x]:
            continue
        seen[y, x] = True
        q.append((y + 1, x))
        q.append((y - 1, x))
        q.append((y, x + 1))
        q.append((y, x - 1))
    alpha = np.where(seen, 0, 255).astype(np.uint8)
    return Image.fromarray(np.dstack([arr, alpha]), "RGBA")


def load_picture(path: Path) -> Image.Image:
    """Open a lesson picture. The title cover is never a full-frame image."""
    resolved = path.resolve()
    if resolved == COVER.resolve() or path.name == COVER.name:
        raise SystemExit(
            "title art may only be used as the wordmark crop. "
            "The full cover has coin logos, a profit claim, and a name."
        )
    return Image.open(resolved)


@lru_cache(maxsize=1)
def wordmark() -> Image.Image:
    """The only allowed use of the title cover: the GRID BOT BUILDER crop."""
    src = Image.open(COVER).convert("RGB")
    cropped = src.crop(WORD_BOX)
    if cropped.size == src.size or cropped.size[0] >= src.size[0] or cropped.size[1] >= src.size[1]:
        raise SystemExit("title art crop failed. Refusing to draw the full cover.")
    return knockout(cropped)


@lru_cache(maxsize=1)
def mascot() -> Image.Image | None:
    """The whole sheet, uncropped. None until Creative Studio drops the file."""
    if not MASCOT_SRC.is_file():
        return None
    return Image.open(MASCOT_SRC).convert("RGBA")


def scaled(im: Image.Image, height: int) -> Image.Image:
    ratio = height / im.height
    nw = max(1, int(im.width * ratio))
    return im.resize((nw, height), Image.Resampling.LANCZOS)


def paste(base: Image.Image, overlay: Image.Image, xy: tuple[int, int]) -> None:
    base.paste(overlay, xy, overlay)


def guard(text: str) -> None:
    if BANNED.search(text or ""):
        raise SystemExit(f"banned phrase in lesson text: {BANNED.search(text).group(0)}")


def clip_vo(vo: str, sentences: int, words: int) -> str:
    parts = re.split(r"(?<=[.!?])\s+", vo.strip())
    keep: list[str] = []
    count = 0
    for part in parts:
        if any(bad in part.lower() for bad in ("say it back", "say the opening", "point of the beat")):
            continue
        n = len(part.split())
        if keep and count + n > words:
            break
        keep.append(part)
        count += n
        if len(keep) >= sentences:
            break
    return " ".join(keep) if keep else vo.strip()


def parse_ident(shot: dict) -> tuple[str, str]:
    left, _, right = shot["caption"].partition(". ")
    num = left.replace("Lesson", "").strip()
    title = right.strip().rstrip(".")
    return num, title


def thirds(shot: dict) -> tuple[str, str]:
    chapter = (shot.get("chapter") or "").strip()
    cap = (shot.get("caption") or "").strip()
    low = chapter.lower()
    # These headings only share a word with another definition. Show their own caption.
    if low in {"finish the seven", "not on the list", "a check you can finish"}:
        text = cap if cap.endswith(".") else (cap + "." if cap else chapter + ".")
        return chapter, text
    table = [
        ("objective", "Objective", "One skill this lesson is building. Say it in your own words."),
        ("recap", "Recap", "A line to keep."),
        ("stop", "Stop", "A rule you write before you start: what you will do if the price leaves the band and does not come back."),
        ("finish", "Finish", "The exit, written before the entry, and pointed at a real date."),
        ("range", "Range", "The bottom line and the top line of the window."),
        ("level", "Level", "A price where a limit order waits. It does not chase the market."),
        ("gap", "Gap", "The space between two rungs. Count gaps, not the lines that bound them."),
        ("wick", "Wick", "The price poking past a line during the day but not closing there."),
        ("grid", "Grid", "Limit orders waiting inside a band you have already measured."),
        ("hook", "The idea", cap if cap.endswith(".") else (cap + "." if cap else "One picture, one point.")),
        ("ladder", "Rung", "A step that waits. The chart beside it is the real path."),
        ("fence", "Fence", "A top rail and a bottom rail. Inside them, the path can wander."),
        ("list", "Page", "The list you write before you open a screen."),
        ("bucket", "Bucket", "One page in its own box. A second page does not share the box."),
        ("isolated", "Isolated", "One box. A loss in that box stays in that box."),
        ("cross", "Cross", "A reach from one box into the next. No multiple is written."),
        ("spot", "Spot", "Coins you hold. This is not a contract and not a forced close."),
        ("secret", "Secret", "A seed, a key, or an A P I secret. None of those go on the page."),
        ("mistake", "Miss", "A blank stop, a band tighter than the wicks, or a line counted as a gap."),
        ("regime", "Regime", "The shape of the path: a range, a leave, or a break."),
        ("break", "Break", "A path that jumps out of the prices around it. Not a quiet range."),
        ("trend", "Trend", "A price that leaves the band and keeps moving one way."),
        ("worked", "Worked example", "Figures you can point at. Marked Example. Not an order."),
        ("monitor", "Check", "Three questions on a date you chose, then you stop."),
        ("field", "Field", "A box on the page. Copy only what the page already says."),
        ("venue", "No venue", "No logo, no login, no balance. The figures are public closes."),
        ("liquidat", "Liquidation", "A venue can close a contract when the margin is gone. Spot is not that."),
    ]
    for key, term, defin in table:
        if key in low:
            text = defin or cap
            if key == "secret" and re.search(r"\bAPI\b", shot.get("vo") or ""):
                text = "A seed, a key, or an API secret. None of those go on the page."
            if text and not text.endswith("."):
                text += "."
            return term, text
    if re.match(r"\d{1,2} \w+ \d{4}", cap):
        date, _, rest = cap.partition(". ")
        defin = rest if rest else "A public daily close on the path."
        if "example" not in defin.lower():
            defin = defin.rstrip(".") + ". Marked Example. Not a forecast."
        return date, defin
    defin = cap if cap.endswith(".") else (cap + "." if cap else "One point on this picture.")
    return (chapter or "Key point"), defin


def key_stops(run: list[dict]) -> list[dict]:
    n = len(run)
    k = 6 if n >= 6 else n
    idxs = sorted({int(round(i * (n - 1) / max(1, k - 1))) for i in range(k)})
    overview = dict(run[0])
    overview["reveal_from"] = 0.0
    overview["reveal"] = 1.0
    overview["vo"] = (
        "The public path draws across this window. "
        "We stop on a handful of days, not on every print. "
        "Every close is an example. It is not a fill, and it is not a forecast."
    )
    overview["caption"] = "The whole window stays on screen."
    overview["chapter"] = run[0]["chapter"]
    picked = []
    for i in idxs:
        shot = dict(run[i])
        shot["vo"] = clip_vo(shot["vo"], 3, 48)
        picked.append(shot)
    return [overview] + picked


def _beat_teaching(beat: dict) -> str | None:
    """The line spoken while a still is on screen. Picture descriptions are not spoken."""
    role = (beat.get("role") or "").lower()
    chapter = (beat.get("chapter") or "").strip().lower()
    concept = (beat.get("concept") or "").strip()
    image = (beat.get("image") or "").replace("\\", "/")
    if role in {"legal", "intro"} or chapter in {"title card", "outro", "disclaimer", "eight ticks"}:
        return None
    if concept.lower().startswith("practice:"):
        return None
    if image in {
        "course/images/bp-01-introduction/013.png",
        "course/images/bp-02-what-you-need/021.png",
    }:
        return None
    overrides = {
        "course/images/bp-03-what-is-a-grid-bot/001.png": "A grid bot doesn't predict the price. It waits.",
        "course/images/bp-03-what-is-a-grid-bot/003.png": "A grid bot is a tool that keeps buy orders below the price and sell orders above it.",
        "course/images/bp-03-what-is-a-grid-bot/009.png": "An order fills. A new order waits on the next line. That is the bot's job.",
        "course/images/bp-03-what-is-a-grid-bot/013.png": "This course is not connected to any exchange.",
        "course/images/bp-03-what-is-a-grid-bot/014.png": "Orders wait. Inside your range. Stop: your rule if price leaves. What you hold changes.",
        "course/images/bp-03-what-is-a-grid-bot/015.png": "Your turn: draw a band, label the five words, and draw one step down.",
        "course/images/bp-03-what-is-a-grid-bot/017.png": "Your turn: draw one buy order waiting below the price.",
        "course/images/bp-01-introduction/007.png": "Buy orders sit on lines below the price and sell orders sit on lines above it. The sells need some coin, so a grid starts with part cash and part coin. That is a description, not advice.",
        "course/images/bp-01-introduction/008.png": "Write your stop rule down before you start. On the card it says: Stop = when you quit.",
        "course/images/bp-03-what-is-a-grid-bot/004.png": "Five labels cover the picture: upper, lower, levels, side, and stop. On the card, Upper is the top edge, Lower is the bottom edge, Levels are the rungs, Side is what you hold, and Stop is your rule.",
        "course/images/bp-03-what-is-a-grid-bot/008.png": "What you hold changes. Price bounces: coin and cash swap back and forth. Price leaves: mostly coin or mostly cash.",
        "course/images/bp-03-what-is-a-grid-bot/010.png": "Point and say the five: Top, Bottom, Levels, What you hold, and Stop.",
        "course/images/bp-05-spacing-and-range/010.png": "Now a second, made-up example: twenty lines, with each gap half of one percent. Recount once from a wrong page: the wrong page says twenty times a half percent equals ten percent. Correct it in writing: nineteen times a half percent equals nine and a half percent.",
        "course/images/bp-05-spacing-and-range/015.png": "Recap: range first, count gaps not lines, check the gap against the fee, change one thing at a time.",
        "course/images/bp-06-entry-and-exit/010.png": "Traders call this an invalidation: the point where your idea is proven wrong.",
        "course/images/bp-09-common-mistakes/010.png": "In our example there are seven lines and six gaps.",
    }
    if image in overrides:
        return overrides[image]
    vo = (beat.get("vo") or "").strip()
    for marker in (
        "On the diagram for this beat",
        "Say the opening line",
        "Your turn, still inside",
        "Mark the page Example",
    ):
        if marker in vo:
            vo = vo.split(marker)[0].strip()
    swaps = (
        ("the size of weave you already drew", "the normal up-and-down you already measured"),
        ("a major news bar, or a thin book", "a big news event, or a market with few waiting orders"),
        ("A path into a major news bar, or a thin book,", "A path into a big news event, or a market with few waiting orders,"),
        ("the top is a story, not the data", "a 30000 top doesn't match the real high"),
        ("an ordinary weave you already drew", "a normal up-and-down move"),
        ("a live ticket", "a real order form"),
        ("not to add a second indicator", "not to add another chart tool"),
        ("A default size on a form is the form's idea.", "A size the form filled in for you is not your choice."),
        ("a grade you can trade", "a score"),
        ("Calling it a seven-grid because you counted marks is the spacing miss, come back again.", "Calling it a seven-grid because you counted seven lines is the same counting mistake from lesson 5."),
        ("Older drafts of this lesson that gave a leverage multiple, or a multiple of capital, are deleted.", ""),
        ("Venue screens move.", "Exchange screens change over time."),
        ("The list is the analogy of the form.", "Think of the form as a copy of your notes."),
        ("passes the same gates", "passes the same checks"),
        ("same gates", "same checks"),
        ("Side means which asset you hold more of after the example fills.", "Which side means whether the close is above or below the middle line."),
        ("Inside means the path you are looking at still crosses the band you drew.", "Inside means the close is still between the top and the bottom."),
        ("not a vigil", "not something you watch all day"),
        ("A vigil is watching with no end. A vigil pretends that watching harder changes the path.", "Watching all day does not change the path."),
        ("No exchange is a partner in this definition.", "This course is not connected to any exchange."),
        ("Inside the band, what you hold stays balanced: some of the coin and some cash.", "As orders fill, your mix of coin and cash changes."),
        ("upper, lower, levels, side, and stop", "top, bottom, levels, what you hold, and stop"),
        ("upper, lower, levels, side, stop", "top, bottom, levels, what you hold, and stop"),
        ("Upper and lower are the band. Levels are the rungs.", "The top and the bottom are the band. Levels are the rungs where orders wait."),
        ("Without a top and a bottom, a spacing percent is a number floating in the margin.", "Without a top and a bottom, you can't place the lines."),
        ("Price often chops sideways, weaving through the same band instead of leaving.", "Price often moves sideways, bouncing between the same top and bottom instead of leaving."),
        ("built for that weave", "built for that bouncing"),
        ("the weave they were built for is gone. Inventory can sit on one side.", "the bouncing they were built for is gone. Leave through the top and every sell has filled, so you hold mostly cash, and leave through the bottom and every buy has filled, so you hold mostly coin."),
        ("The weave is the job.", "Bouncing inside the band is what a grid is built for."),
        ("such as the base and the quote", "the coin you buy and the money you pay with"),
        ("The setup check has seven lines", "The setup check has seven items"),
        ("complete the seven lines on paper", "complete the seven items on paper"),
        ("That is the weave, told as inventory, not as a result.", "That change in what you hold is how a grid works, and it is not a profit."),
        ("They do not jump the queue.", "They wait their turn at that price."),
        ("hypothetical noise", "a made-up path"),
        ("the path leaves by construction", "a normal day will push the price out of it"),
        ("If your band is thinner than that drawn weave, a normal day will push the price out of it.", "If your band is narrower than that normal up-and-down, a normal day will push the price out of it."),
        ("Trend makes you draw the inventory pile before you go on.", "A trend means drawing what you'd end up holding."),
        ("a live chart's implication", "a live chart"),
        ("Twenty order lines make nineteen gaps.", "Now a second, made-up example: twenty lines, with each gap half of one percent. Twenty order lines make nineteen gaps."),
        ("the gap count is thirty-eight, not forty", "there are thirty-eight gaps, which is thirty-nine lines, not forty"),
        ("A wish that the weave continues", "A wish that the price keeps bouncing"),
        ("which side is the inventory, and does the finish sentence still match", "which side of the middle line the close is on, and does the finish sentence still match"),
        ("Inventory is what has piled up. ", ""),
        ("Row two names the side the exits would have piled.", "Row two says whether the close is above or below the middle line."),
        ("not to add a new indicator", "not to add another chart tool"),
        ("The span in the house example is nine and a half percent for nineteen gaps.", "In our example there are seven lines and six gaps."),
        ("If you have notes from those drafts, the multiple is the part you cross out.", "If old notes show a multiple like 5x, cross it out."),
        ("The flags are the lesson's voice. A flag that says opportunity is the wrong flag.", "These two warnings are the lesson's voice. A note that calls this an opportunity is the wrong note."),
        ("Two flags belong in the margin:", "Write two warnings beside your drawing:"),
        ("this can liquidate, and you can lose all the money assigned on the sketch.", "this can be liquidated, and you can lose all the money you put in."),
        ("The venue name is incidental. The field order is the lesson.", "The exchange name doesn't matter. Copying the right five fields does."),
        ("a little more of the base asset", "a little more coin"),
        ("Inventory of the base can fall, and the quote asset can rise, inside the example.", "You can hold less coin and more cash. This is only an example."),
        ("the top, the bottom, the price steps, what you hold, and a stop", "top, bottom, levels, what you hold, and stop"),
    )
    for old, new in swaps:
        vo = vo.replace(old, new)
    vo = re.sub(r"\s+", " ", vo).strip(" .")
    if not vo:
        vo = (beat.get("alt") or concept).strip()
    if not vo or vo.lower().startswith("practice:"):
        return None
    if vo.lower().startswith(("a notebook sketch", "a crystal ball", "a simple robot", "a robot putting", "two tokens joined")):
        return None
    parts = re.split(r"(?<=[.!?])\s+", vo)
    keep: list[str] = []
    words = 0
    for part in parts:
        part = part.strip()
        if not part:
            continue
        n = len(part.split())
        if keep and words + n > 80:
            break
        keep.append(part if part.endswith((".", "!", "?")) else part + ".")
        words += n
        if len(keep) >= 3:
            break
    return " ".join(keep).strip()


def _still_shot(beat: dict, line: str) -> dict:
    caption = line if line.endswith((".", "!", "?")) else line + "."
    return {
        "kind": "lesson-still",
        "chapter": beat.get("chapter") or "Picture",
        "vo": caption,
        "caption": caption,
        "lesson_still": str((ROOT / beat["image"]).resolve()),
        "alt": caption,
        "chart": "",
        "series": [],
        "example": False,
    }


def _attach_lesson_stills(sid: str, shots: list[dict]) -> None:
    """Put each still on the beat it illustrates, with a teaching line, not a picture description.

    Title cards, practice repeats, and the duplicate next-lesson card are not spoken.
    A code-drawn chart stays a chart. Its still is the next shot.
    """
    path = ROOT / "course/scripts" / f"{sid}.json"
    if not path.is_file():
        return
    beats = json.loads(path.read_text(encoding="utf-8")).get("beats") or []
    pending: list[tuple[dict, str]] = []
    for beat in beats:
        if not beat.get("image"):
            continue
        line = _beat_teaching(beat)
        if line:
            pending.append((beat, line))
    used: set[str] = set()
    i = 0
    while i < len(shots):
        chapter = str(shots[i].get("chapter") or "").strip().lower()
        kind = shots[i].get("kind")
        if kind in {"brand", "disclaimer", "outro"} or not chapter:
            i += 1
            continue
        match = next(
            (
                pair for pair in pending
                if pair[0]["image"] not in used
                and str(pair[0].get("chapter") or "").strip().lower() == chapter
            ),
            None,
        )
        if match is None:
            i += 1
            continue
        beat, line = match
        used.add(beat["image"])
        shots.insert(i + 1, _still_shot(beat, line))
        i += 2
    rest = [_still_shot(beat, line) for beat, line in pending if beat["image"] not in used]
    if not rest:
        return
    at = next(
        (i for i, shot in enumerate(shots) if str(shot.get("chapter") or "").strip().lower() == "recap"),
        next((i for i, shot in enumerate(shots) if shot.get("kind") == "outro"), len(shots)),
    )
    shots[at:at] = rest


def plan(sid: str) -> list[dict]:
    raw = lesson_scripts.build(sid)
    lesson_scripts.attach_series(raw)
    number, title = parse_ident(raw[0])
    spoken = speech.spoken_number(int(number))
    brand = {
        "kind": "brand",
        "chapter": "Open",
        "vo": f"Grid Bot Builder. Grid Bot Blueprint. Lesson {spoken}. {title}.",
        "caption": f"Lesson {number}. {title}.",
        "chart": "",
        "series": [],
    }
    disc = {
        "kind": "disclaimer",
        "chapter": "Disclaimer",
        "vo": DISCLAIMER,
        "caption": DISCLAIMER,
        "chart": "",
        "series": [],
    }
    risk_lines = [
        "Crypto carries a risk of total loss.",
        "The prices are public historical daily closes, marked Example.",
        "Past performance is not a reliable indicator of future results.",
    ]
    risk_shots = [
        {
            "kind": "stack",
            "chapter": "Risk",
            "vo": line,
            "caption": line,
            "items": risk_lines,
            "index": index,
            "chart": "",
            "series": [],
        }
        for index, line in enumerate(risk_lines)
    ]
    shots: list[dict] = [brand, disc, *risk_shots]
    seq = [s for s in raw if s.get("kind") not in {"ident", "legal"}]
    i = 0
    while i < len(seq):
        shot = seq[i]
        if shot.get("kind") == "chart":
            j = i + 1
            while (
                j < len(seq)
                and seq[j].get("kind") == "chart"
                and seq[j].get("chapter") == shot.get("chapter")
            ):
                j += 1
            run = seq[i:j]
            block = key_stops(run) if len(run) >= 6 else [dict(s) for s in run]
            shots.extend(block)
            i = j
            continue
        nxt = dict(shot)
        if nxt.get("kind") == "analogy":
            nxt["still"] = str(STILLS[nxt.get("analogy") or "ladder"])
        nxt["vo"] = clip_vo(nxt["vo"], 4, 80)
        shots.append(nxt)
        i += 1
    _attach_lesson_stills(sid, shots)
    for shot in shots:
        shot["lesson_no"] = number
        shot["lesson_id"] = sid
        shot["lesson_title"] = title
        shot["term"], shot["definition"] = thirds(shot)
        blob = " ".join(
            [
                shot.get("vo") or "",
                shot.get("caption") or "",
                shot.get("definition") or "",
                shot.get("chapter") or "",
                " ".join(shot.get("items") or []),
            ]
        )
        guard(blob)
        shot["example"] = bool(re.search(r"\d", blob))
        shot["vo"] = _speak_round(shot.get("vo") or "")
    return shots


def _speak_round(text: str) -> str:
    """Exact five-digit prices stay on the card. Speech uses the line or a round amount."""
    swaps = (
        ("24,930", "the bottom line"),
        ("24930", "the bottom line"),
        ("30,331", "the top line"),
        ("30331", "the top line"),
        ("27,630", "the middle line"),
        ("27630", "the middle line"),
        ("33,086", "about 33 thousand"),
        ("33086", "about 33 thousand"),
        ("29,914", "about 30 thousand"),
        ("29914", "about 30 thousand"),
        ("29,794", "about 30 thousand"),
        ("29794", "about 30 thousand"),
        ("30,184", "about 30 thousand"),
        ("30184", "about 30 thousand"),
        ("26,050", "about 26 thousand"),
        ("26050", "about 26 thousand"),
        ("27,969", "about 28 thousand"),
        ("27969", "about 28 thousand"),
        ("71,397", "about 71 thousand"),
        ("71397", "about 71 thousand"),
        ("56,555", "about 57 thousand"),
        ("56555", "about 57 thousand"),
        ("72,715", "about 73 thousand"),
        ("72715", "about 73 thousand"),
        ("30,000", "about 30 thousand"),
        ("30000", "about 30 thousand"),
        ("25,000", "about 25 thousand"),
        ("25000", "about 25 thousand"),
    )
    for old, new in swaps:
        text = text.replace(old, new)
    return text


# The old estimate used 2.55 words/second and said BP-01 was 7.2 minutes.
# Real Kokoro af_heart, with its sentence gaps, was 617.7s (101 words a minute).
# After the gap tighten, the same words are 0.584s each at speed 1.0.
# Kokoro af_heart speed 1.0 for every line. Moods no longer scale the pace.
SPEECH_RATE = 1.0
SENTENCE_GAP = 0.52
BEAT_GAP = 1.05
# A short card used to sit in silence for up to 3s. A chart may still hold
# while its line is revealing. Every other gap stays within about 1.2s.
LINE_GAP_CAP = 1.2
REVEAL_GAP_CAP = 3.0
JOIN_FADE = 0.030
SECONDS_PER_WORD = 610.085 / 1045


def estimate(shot: dict) -> float:
    """Rough length. The render go/no-go uses the real Kokoro file, not this."""
    words = max(1, len((shot.get("vo") or "").split()))
    return words * SECONDS_PER_WORD / max(SPEECH_RATE, 0.5)


def background(local: float) -> Image.Image:
    """A slow glow so a held card is not a frozen frame. Text is drawn after this."""
    yy = np.linspace(0, 1, H, dtype=np.float32)[:, None]
    xx = np.linspace(0, 1, W, dtype=np.float32)[None, :]
    cx = np.float32(0.32 + 0.22 * np.sin(local * 0.45))
    cy = np.float32(0.42 + 0.16 * np.cos(local * 0.37))
    glow = np.exp(-((xx - cx) ** 2 * 2.4 + (yy - cy) ** 2 * 3.0))
    base = np.empty((H, W, 3), np.float32)
    base[:] = NAVY
    base += glow[..., None] * np.array([14, 28, 48], np.float32)
    img = Image.fromarray(np.clip(base, 0, 255).astype(np.uint8), "RGB")
    draw = ImageDraw.Draw(img)
    shift = int(local * 40) % 64
    grid = (32, 64, 96)
    for x in range(-64 + shift, W, 64):
        draw.line([(x, 0), (x, H)], fill=grid, width=1)
    for y in range(shift, H, 64):
        draw.line([(0, y), (W, y)], fill=grid, width=1)
    return img


def draw_footer(draw: ImageDraw.ImageDraw) -> None:
    face = font(36, "reg")
    draw.text((MX, 990), FOOT, font=face, fill=MUTED)


def title_bar(base: Image.Image, shot: dict, progress: float) -> None:
    draw = ImageDraw.Draw(base)
    mark = scaled(wordmark(), 84)
    paste(base, mark, (MX, 64))
    chapter = shot.get("heading") or shot.get("chapter") or ""
    if chapter == "Hook":
        chapter = "Opening"
    size = fit_size(chapter, 900, 40, 36)
    if shot.get("analogy") not in {"ladder", "fence"}:
        draw.text((MX + mark.width + 28, 78), chapter, font=font(size), fill=WHITE)
    y = 160
    draw.rectangle([MX, y, RIGHT, y + 4], fill=(20, 40, 58))
    span = (RIGHT - MX) * max(0.02, min(1.0, progress))
    draw.rectangle([MX, y, MX + span, y + 4], fill=CYAN)


def lower_third(draw: ImageDraw.ImageDraw, shot: dict) -> None:
    if shot.get("kind") in {"brand", "disclaimer", "outro"}:
        return
    draw.rectangle([MX, 784, RIGHT, 788], fill=CYAN)
    term = shot.get("term") or ""
    defin = shot.get("definition") or ""
    t_size = fit_size(term, W - 2 * MX, 40, 36)
    draw.text((MX, 806), term, font=font(t_size), fill=CYAN)
    lines = wrap(defin, 36, W - 2 * MX, "reg")[:2]
    y = 858
    for line in lines:
        draw.text((MX, y), line, font=font(36, "reg"), fill=WHITE)
        y += 44


def _series(shot: dict) -> list[dict]:
    return shot.get("series") or []


def _map(i: int, n: int, price: float, lo: float, hi: float, box) -> tuple[float, float]:
    x0, y0, x1, y1 = box
    x = x0 + (x1 - x0) * (i / max(1, n - 1))
    span = max(1.0, hi - lo)
    y = y1 - (y1 - y0) * ((price - lo) / span)
    return x, y


def chart_idea(shot: dict) -> str:
    """One plain sentence so a chart frame says what its heading means."""
    board = shot.get("board") or ""
    chapter = shot.get("chapter") or ""
    if board == "buys-sells" or chapter == "Buys and sells":
        return "Three buy rungs below the middle. Three sell rungs above it."
    if chapter == "The levels":
        return "Seven lines. Six gaps. About 900 dollars."
    if chapter == "The range":
        return "The range is the real low and the real high."
    if chapter == "The stop":
        return "Stop: the close leaves 30,331 and does not return."
    if chapter == "Hook":
        if (shot.get("lesson_id") or "") == "bp-03-what-is-a-grid-bot":
            return "Orders that wait inside a measured band."
        caption = (shot.get("caption") or "").strip()
        return caption.rstrip(".") if caption else ""
    if chapter == "Limit orders wait":
        return "A cross touches a rung. A fill is an order that trades."
    return ""


def playhead_index(shot: dict, local: float, dur: float) -> int:
    """The day the date tag names. A pinned stop uses that row, not a neighbour."""
    series = _series(shot)
    n = len(series)
    if n == 0:
        return 0
    pin = shot.get("pin_date")
    if pin:
        matches = [i for i, row in enumerate(series) if row.get("date") == pin]
        if not matches:
            raise SystemExit(f"pinned date {pin} is not in this chart")
        idx = matches[0]
        close = int(round(float(series[idx]["close"])))
        wanted = shot.get("pin_close")
        if wanted is not None and int(wanted) != close:
            raise SystemExit(f"label close {wanted} does not match {pin} close {close}")
        return idx
    end = float(shot.get("reveal") or 1)
    start = float(shot.get("reveal_from") or 0)
    if abs(end - start) < 0.03:
        start = max(0.0, end - 0.15)
    now = start + (end - start) * ease(min(1.0, local / max(1.2, dur * 0.88)))
    last = max(1, min(n, int(round(now * (n - 1))) + 1))
    return last - 1


def _rect_hits_samples(rect: tuple[float, float, float, float], points: list[tuple[float, float]]) -> bool:
    x0, y0, x1, y1 = rect
    for index in range(len(points) - 1):
        ax, ay = points[index]
        bx, by = points[index + 1]
        length = max(1.0, ((bx - ax) ** 2 + (by - ay) ** 2) ** 0.5)
        steps = max(1, int(length / 6))
        for step in range(steps + 1):
            t = step / steps
            x = ax + (bx - ax) * t
            y = ay + (by - ay) * t
            if x0 <= x <= x1 and y0 <= y <= y1:
                return True
    return False


def place_date_tag(
    hx: float,
    hy: float,
    tw: int,
    th: int,
    plot: tuple[float, float, float, float],
    level_ys: list[float],
    polyline: list[tuple[float, float]],
) -> tuple[float, float]:
    """Park the date tag beside its close, clear of every level line and the path."""
    gap = 22
    radius = 12
    x0, y0, x1, y1 = plot

    def ok(tx: float, ty: float) -> bool:
        if tx < x0 or ty < y0 or tx + tw > x1 or ty + th > y1:
            return False
        if any(ty - 8 < level < ty + th + 8 for level in level_ys):
            return False
        rect = (tx - 4, ty - 4, tx + tw + 4, ty + th + 4)
        if _rect_hits_samples(rect, polyline):
            return False
        if tx - 6 <= hx <= tx + tw + 6 and ty - 6 <= hy <= ty + th + 6:
            return False
        return True

    shifts = [0]
    for step in range(8, 180, 8):
        shifts.extend((step, -step))
    for side in (1, -1):
        for dy in shifts:
            if side > 0:
                tx = hx + radius + gap
            else:
                tx = hx - radius - gap - tw
            ty = hy - th / 2 + dy
            if ok(tx, ty):
                return tx, ty
    ty = min(max(y0, hy + radius + 8), y1 - th)
    tx = min(max(x0, hx + radius + gap), x1 - tw)
    return tx, ty


def _blend(base: Image.Image, overlay: Image.Image) -> None:
    merged = Image.alpha_composite(base.convert("RGBA"), overlay).convert("RGB")
    base.paste(merged)


def _band(base: Image.Image, x0: float, x1: float, y_top: float, y_bot: float) -> None:
    overlay = Image.new("RGBA", base.size, (0, 0, 0, 0))
    ImageDraw.Draw(overlay).rectangle([x0, y_top, x1, y_bot], fill=(0, 212, 255, 20))
    _blend(base, overlay)


def _stroke(base: Image.Image, points: list[tuple[float, float]], color: tuple[int, int, int, int], width: int) -> None:
    if len(points) < 2:
        return
    overlay = Image.new("RGBA", base.size, (0, 0, 0, 0))
    ImageDraw.Draw(overlay).line(points, fill=color, width=width)
    _blend(base, overlay)


def _example(draw: ImageDraw.ImageDraw, x: int = 1640, y: int = 196) -> None:
    face = font(36)
    label = "EXAMPLE"
    tw = int(face.getlength(label)) + 36
    draw.rounded_rectangle([x, y, x + tw, y + 44], 22, fill=TAG, outline=CYAN, width=2)
    draw.text((x + 18, y + 2), label, font=face, fill=WHITE)


def _ticket(draw: ImageDraw.ImageDraw, x: float, y: float, outline: tuple[int, int, int], label: str = "") -> None:
    box = [x, y - 18, x + 64, y + 18]
    draw.rounded_rectangle(box, 8, fill=TAG, outline=outline, width=2)
    draw.ellipse([x + 8, y - 8, x + 24, y + 8], outline=outline, width=2)
    draw.line([(x + 16, y), (x + 16, y - 5)], fill=outline, width=2)
    if label:
        draw.text((x + 72, y - 14), label, font=font(28), fill=WHITE)


def chart_card(base: Image.Image, shot: dict, local: float, dur: float, box=None) -> None:
    draw = ImageDraw.Draw(base)
    if box is None:
        box = (MX, 180, RIGHT, 752)
    draw.rounded_rectangle(box, 22, fill=GLASS, outline=LINE, width=2)
    series = _series(shot)
    title = shot.get("chart_title") or ""
    idea = chart_idea(shot)
    if title:
        size = fit_size(title, box[2] - box[0] - 80, 32, 28)
        draw.text((box[0] + 28, box[1] + 16), title, font=font(size), fill=WHITE)
    chapter = shot.get("chapter") or ""
    idea_color = AMBER if chapter == "The stop" else WHITE
    if idea:
        draw.text((box[0] + 28, box[1] + 56), idea, font=font(36), fill=idea_color)
    if shot.get("example") or chapter:
        _example(draw)
    if not series:
        draw.text((box[0] + 36, box[1] + 96), "Example window", font=font(36), fill=MUTED)
        return
    plot_top = box[1] + (108 if idea else 72)
    months = ["", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    pinned = playhead_index(shot, local, dur)
    ymd = series[pinned]["date"].split("-")
    tag = f"{int(ymd[2])} {months[int(ymd[1])]}  {int(round(series[pinned]['close'])):,}"
    # Walk charts put the close in a small tag. 46px keeps a 9 from being read as a 0.
    tag_px = 46 if chapter in {"Walk the summer", "Copy the path", "Where the price stayed"} else 36
    face = font(tag_px)
    tw = int(face.getlength(tag)) + 28
    th = 64 if tag_px > 32 else 44
    plot = (box[0] + 28, plot_top, min(box[2] - 280, 1520), box[3] - 36)
    gutter_x = 1600
    closes = [float(r["close"]) for r in series]
    lo = min(float(r["low"]) for r in series)
    hi = max(float(r["high"]) for r in series)
    pad = (hi - lo) * 0.12 or 1
    lo_p, hi_p = lo - pad, hi + pad
    n = len(series)
    last = pinned + 1
    full = [_map(i, n, closes[i], lo_p, hi_p, plot) for i in range(n)]
    rails = [float(p) for p in (shot.get("levels") or [])]
    if rails:
        y_hi = _map(0, n, max(rails), lo_p, hi_p, plot)[1]
        y_lo = _map(0, n, min(rails), lo_p, hi_p, plot)[1]
        _band(base, plot[0], plot[2], min(y_hi, y_lo), max(y_hi, y_lo))
        draw = ImageDraw.Draw(base)
    shown = full[:last]
    if chapter in {"Walk the summer", "Copy the path", "Where the price stayed"}:
        rest = full[max(0, last - 1):]
        _stroke(base, rest, (0, 212, 255, 150), 2)
        _stroke(base, shown, (0, 212, 255, 90), 9)
        _stroke(base, shown, (0, 212, 255, 255), 3)
    else:
        _stroke(base, full, (0, 212, 255, 70), 1)
        _stroke(base, shown, (0, 212, 255, 80), 8)
        _stroke(base, shown, (0, 212, 255, 255), 3)
    draw = ImageDraw.Draw(base)
    hx, hy = shown[-1]
    dated = chapter in {"Walk the summer", "Copy the path", "Where the price stayed"}
    if dated:
        y_inner = _map(0, n, 29431, lo_p, hi_p, plot)[1]
        tx, ty = 150, max(hy + 18, y_inner + 14)
        hole = (tx - 6, ty - 6, tx + tw + 6, ty + th + 6)
    else:
        hole = None
    levels = [float(p) for p in (shot.get("levels") or [])]
    focus = shot.get("focus_price")
    prices = list(levels) if levels else []
    if not prices and focus:
        prices = [float(focus)]
    # Prefer the rails and the focus. Collision drops the rest.
    prefer = []
    if prices:
        prefer.append(min(prices))
        prefer.append(max(prices))
    if focus is not None:
        prefer.append(float(focus))
    order = prefer + [p for p in prices if p not in prefer]
    used: list[float] = []
    for price in order:
        _, yy = _map(0, n, price, lo_p, hi_p, plot)
        if any(abs(yy - u) < 46 for u in used):
            continue
        if yy < plot[1] + 8 or yy > plot[3] - 8:
            continue
        used.append(yy)
        rounded = int(round(price))
        edges = {24930, 30331}
        if chapter == "The range":
            color, width, label = CYAN, 3, ("Top" if rounded == 30331 else "Bottom") + f": {rounded:,}"
        elif chapter == "The levels":
            color, width = (CYAN, 3) if rounded in edges else (MUTED, 2)
            label = f"{rounded:,}"
        if chapter == "The stop" and abs(price - 30331) < 2:
            continue
        elif chapter in {"Walk the summer", "Copy the path", "Where the price stayed"}:
            color, width, label = MUTED, 2, f"{rounded:,}"
        elif shot.get("board") == "buys-sells":
            if price < 27629:
                color, label = BLUE, f"{rounded:,} buy"
            elif price > 27631:
                color, label = MINT, f"{rounded:,} sell"
            else:
                color, label = WHITE, f"{rounded:,} middle"
            width = 3 if abs(price - 27630) < 2 else 2
        elif chapter == "Limit orders wait" and abs(price - 27630) < 2:
            color, width, label = CYAN, 3, f"{rounded:,}"
        elif focus is not None and abs(price - float(focus)) < 2 and chapter == "The stop":
            color, width, label = AMBER, 3, f"{rounded:,}"
        else:
            color, width = (CYAN, 3) if rounded in edges else (MUTED, 2)
            label = f"{rounded:,}"
        step = 18
        x = plot[0]
        while x < plot[2]:
            x2 = min(x + 8, plot[2])
            if hole and hole[1] <= yy <= hole[3] and not (x2 < hole[0] or x > hole[2]):
                x += step
                continue
            draw.line([(x, yy), (x2, yy)], fill=color, width=width)
            x += step
        lf = font(36)
        if shot.get("board") == "buys-sells" and label.endswith(" middle"):
            # The full 36px tag ends past the 4% margin. Shifting it left makes
            # OCR read 27,630 as 927630, so the price stays put and the word shrinks.
            price = label[: -len(" middle")]
            draw.text((gutter_x, yy - 18), price, font=lf, fill=WHITE)
            role = font(28)
            role_x = gutter_x + lf.getlength(price) + 12
            draw.text((role_x, yy - 12), "middle", font=role, fill=WHITE)
        else:
            draw.text((gutter_x, yy - 18), label, font=lf, fill=WHITE)
        if chapter == "The levels" and rounded == 26730:
            other = _map(0, n, 27630, lo_p, hi_p, plot)[1]
            bracket = plot[0] + 24
            draw.line([(bracket, yy), (bracket, other)], fill=CYAN, width=2)
            mid = (yy + other) / 2
            note = "one gap = about 900"
            draw.rounded_rectangle([bracket + 10, mid - 18, bracket + 16 + font(28).getlength(note), mid + 18], 8, fill=TAG)
            draw.text((bracket + 16, mid - 16), note, font=font(28), fill=WHITE)

    if chapter == "Limit orders wait" or "waiting" in idea.lower():
        y_line = _map(0, n, 27630, lo_p, hi_p, plot)[1]
        if chapter == "Hook":
            x = plot[0]
            while x < plot[2]:
                draw.line([(x, y_line), (min(x + 8, plot[2]), y_line)], fill=CYAN, width=3)
                x += 18
            draw.text((gutter_x, y_line - 16), "27,630", font=font(28), fill=CYAN)
        # A buy is the day the close finishes below 27,630. The interpolated
        # point sits on the day before, which is the 29 Aug peak.
        downward = {
            "2023-08-17", "2023-08-30", "2023-10-02", "2023-10-05", "2023-10-09",
        }
        downs = [
            index for index in range(1, n)
            if series[index]["date"] in downward and closes[index - 1] > 27630 > closes[index]
        ]
        span = max(1, n - 1)

        def x_of(index: int) -> float:
            return plot[0] + (plot[2] - plot[0]) * (index / span)

        face_t = font(28)
        buy = "BUY 27,630"
        twid = int(face_t.getlength(buy)) + 16
        ticket_h = 42
        date_face = font(28)
        date_w = int(date_face.getlength(tag)) + 20
        date_h = 40
        date_x = hx - 24 - 11 - date_w
        date_y = hy - date_h / 2
        if date_x < plot[0]:
            date_x = min(hx + 24, plot[2] - date_w)
        date_y = min(max(plot[1], date_y), plot[3] - date_h)
        # 40px clear of the 16 Oct tag.
        clear = (date_x - 40, date_y - 40, date_x + date_w + 40, date_y + date_h + 40)

        def draw_ticket(label: str, left: float, top: float, target: tuple[float, float] | None) -> None:
            face = font(28)
            width = int(face.getlength(label)) + 16
            if target is not None:
                draw.line([(left + width, top + ticket_h), target], fill=CYAN, width=2)
            draw.rounded_rectangle([left, top, left + width, top + ticket_h], 8, fill=TAG, outline=CYAN, width=2)
            draw.text((left + 8, top + 6), label, font=face, fill=WHITE)

        if chapter == "Limit orders wait":
            # Rings mark crosses: the price line touched 27,630. A fill is a different mark.
            ups = [index for index in range(1, n) if closes[index - 1] < 27630 < closes[index]]
            for index in list(downs) + list(ups):
                cx = x_of(index)
                draw.ellipse((cx - 7, y_line - 7, cx + 7, y_line + 7), outline=WHITE, width=3)
            draw_ticket("Cross: price touched the rung", plot[0] + 16, plot[1] + 12, None)
            fill_label = "Fill: an order trades"
            fill_w = int(face_t.getlength(fill_label)) + 16
            fill_left = plot[2] - fill_w - 8
            fill_top = plot[3] - 16 - ticket_h
            draw.rectangle(
                (fill_left - 22, fill_top + 12, fill_left - 8, fill_top + 26),
                fill=WHITE,
            )
            draw_ticket(fill_label, fill_left, fill_top, None)
            count = f"{len(downs) + len(ups)} crosses: {len(downs)} down, {len(ups)} up"
            draw_ticket(count, plot[0] + 16, plot[3] - 16 - ticket_h, None)
        elif len(downs) >= 2:
            # 17 Aug: sit left of the drop so the path can meet the line.
            cx = x_of(downs[0])
            draw_ticket(buy, max(plot[0], cx - 28 - twid), y_line - 40 - ticket_h, (cx, y_line))
            # 30 Aug: the down-close itself, not the peak the day before.
            cx = x_of(downs[1])
            draw_ticket(buy, cx - twid / 2, y_line - 48 - ticket_h, (cx, y_line))
        if chapter != "Limit orders wait":
            october = downs[2:]
            for index in october:
                cx = x_of(index)
                draw.ellipse((cx - 5, y_line - 5, cx + 5, y_line + 5), fill=WHITE, outline=CYAN)
        else:
            october = []
        if october:
            more = "3 more in October"
            width = int(face_t.getlength(more)) + 16
            left = min(x_of(october[0]) - 12 - width, clear[0] - 8 - width)
            left = max(plot[0], left)
            top = y_line - 40 - ticket_h
            if top < clear[3] and left + width > clear[0]:
                top = clear[1] - 8 - ticket_h
            draw_ticket(more, left, top, None)

    if chapter == "The stop":
        for index, row in enumerate(series):
            if row.get("date") == "2023-10-23":
                mx, my = full[index]
                draw.ellipse((mx - 9, my - 9, mx + 9, my + 9), fill=AMBER)
                leave = "23 Oct: leaves 30,331"
                lf = font(28)
                lw = int(lf.getlength(leave)) + 24
                lx = min(mx + 16, plot[2] - lw)
                ly = my - 50
                draw.rounded_rectangle([lx, ly, lx + lw, ly + 40], 8, fill=TAG, outline=AMBER, width=2)
                draw.text((lx + 12, ly + 4), leave, font=lf, fill=WHITE)
                draw.line([(mx, my), (lx, ly + 20)], fill=AMBER, width=2)
                break

    if chapter == "The stop":
        yy = _map(0, n, 30331, lo_p, hi_p, plot)[1]
        x = plot[0]
        while x < plot[2]:
            draw.line([(x, yy), (min(x + 8, plot[2]), yy)], fill=AMBER, width=3)
            x += 18
        draw.text((gutter_x, yy - 34), "30,331", font=font(28), fill=AMBER)
    if not dated:
        face = font(28)
        tw = int(face.getlength(tag)) + 20
        th = 40
        # 24px between the tag and the dot's outer ring (radius 8, plus a 3px stroke).
        tx = hx - 24 - 11 - tw
        ty = hy - th / 2
        if tx < plot[0]:
            tx = min(hx + 24, plot[2] - tw)
        ty = min(max(plot[1], ty), plot[3] - th)
    r = 8
    draw.ellipse((hx - r - 3, hy - r - 3, hx + r + 3, hy + r + 3), outline=CYAN, width=3)
    draw.ellipse((hx - r, hy - r, hx + r, hy + r), fill=WHITE)
    anchor_x = tx if tx >= hx else tx + tw
    draw.line([(hx + (12 if tx >= hx else -12), hy), (anchor_x, ty + th / 2)], fill=CYAN, width=2)
    draw.rounded_rectangle([tx, ty, tx + tw, ty + th], 10, fill=TAG, outline=CYAN, width=2)
    draw.text((tx + 14, ty + 4), tag, font=face, fill=WHITE)
    # The ladder still has five rungs. Connectors would make them look like the seven levels.
    if shot.get("analogy") == "fence" and rails:
        marks = shot.get("rail_marks") or {}
        for price, key in ((max(rails), "top"), (min(rails), "bottom")):
            chart_y = _map(0, n, float(price), lo_p, hi_p, plot)[1]
            rail_y = marks.get(key, chart_y)
            draw.line([(marks.get("x", 900), rail_y), (plot[0], chart_y)], fill=CYAN, width=3)


def _hero(
    base: Image.Image,
    box: tuple[int, int, int, int],
    mode: str,
    chip_dx: int = 0,
    chip_x: int | None = None,
    chip_beside: bool = False,
) -> None:
    """Lesson visual. path and orders use the real summer closes, not a sawtooth."""
    draw = ImageDraw.Draw(base)
    draw.rounded_rectangle(box, 24, fill=GLASS, outline=CYAN, width=2)
    x0, y0, x1, y1 = box
    if mode == "lines":
        rows = ["Notebook", "Range and levels", "The pair", "Paper or demo", "No secrets", "A written stop", "Example on every figure"]
        if x1 - x0 < 520:
            rows[-1] = "EXAMPLE on figures"
        step = max(36, (y1 - y0 - 70) // len(rows))
        y = y0 + 28
        for row in rows:
            _tick(draw, x0 + 36, y + 16)
            draw.text((x0 + 68, y), row, font=font(28), fill=WHITE)
            y += step
        return
    if mode == "regimes":
        labels = ("Range", "Trend", "Break")
        gap = (x1 - x0 - 48) // 3
        for index, label in enumerate(labels):
            left = x0 + 24 + index * gap
            cell = (left, y0 + 70, left + gap - 16, y1 - 36)
            draw.rounded_rectangle(cell, 16, outline=CYAN, width=2)
            draw.text((left + 12, y0 + 80), label, font=font(28), fill=CYAN)
            px0, py0, px1, py1 = cell[0] + 16, cell[1] + 70, cell[2] - 16, cell[3] - 20
            if label == "Range":
                draw.line([(px0, py0 + 16), (px1, py0 + 16)], fill=CYAN, width=2)
                draw.line([(px0, py1 - 16), (px1, py1 - 16)], fill=CYAN, width=2)
                mid = (py0 + py1) / 2
                pts = [(px0 + (px1 - px0) * i / 6, mid + (12 if i % 2 else -12)) for i in range(7)]
                draw.line(pts, fill=CYAN, width=3)
            elif label == "Trend":
                span_x, span_y = px1 - px0, (py1 - 16) - (py0 + 16)
                knots = (0, 0.18, 0.34, 0.52, 0.68, 0.84, 1)
                rise = (0, 0.28, 0.16, 0.52, 0.38, 0.78, 1)
                pts = [(px0 + span_x * k, (py1 - 16) - span_y * r) for k, r in zip(knots, rise)]
                draw.line(pts, fill=CYAN, width=3)
            else:
                top = py0 + 90
                bot = py1 - 16
                draw.line([(px0, top), (px1, top)], fill=CYAN, width=2)
                draw.line([(px0, bot), (px1, bot)], fill=CYAN, width=2)
                span_x = px1 - px0
                mid = (top + bot) / 2
                pts = [
                    (px0, mid + 10),
                    (px0 + span_x * 0.28, mid - 8),
                    (px0 + span_x * 0.48, mid + 12),
                    (px0 + span_x * 0.62, top),
                    (px1, py0 + 6),
                ]
                draw.line(pts, fill=CYAN, width=3)
        return
    series = lesson_scripts.PRICES["range_2023"]
    plot = (x0 + 28, y0 + 78, x1 - 28, y1 - 64)
    closes = [float(row["close"]) for row in series]
    lo = min(float(row["low"]) for row in series)
    hi = max(float(row["high"]) for row in series)
    pad = (hi - lo) * 0.12 or 1
    lo_p, hi_p = lo - pad, hi + pad
    n = len(closes)
    points = [_map(i, n, closes[i], lo_p, hi_p, plot) for i in range(n)]
    y_top = _map(0, n, 30331, lo_p, hi_p, plot)[1]
    y_bot = _map(0, n, 24930, lo_p, hi_p, plot)[1]
    _band(base, plot[0], plot[2], y_top, y_bot)
    draw = ImageDraw.Draw(base)
    draw.line([(plot[0], y_top), (plot[2], y_top)], fill=CYAN, width=3)
    draw.line([(plot[0], y_bot), (plot[2], y_bot)], fill=CYAN, width=3)
    _stroke(base, points, (0, 212, 255, 80), 7)
    _stroke(base, points, (0, 212, 255, 255), 3)
    draw = ImageDraw.Draw(base)
    draw.text((plot[2] - 110, y_top - 32), "30,331", font=font(28), fill=CYAN)
    draw.text((plot[0], y_bot + 8), "24,930", font=font(28), fill=CYAN)
    _example(draw, x0 + 16, y0 + 16)
    if mode == "orders":
        y_line = _map(0, n, 27630, lo_p, hi_p, plot)[1]
        draw.line([(plot[0], y_line), (plot[2], y_line)], fill=CYAN, width=2)
        face = font(28)
        text = "BUY 27,630"
        tw = int(face.getlength(text)) + 24
        if chip_beside:
            # Left of the card, on the clear side of the line, so it misses the path.
            tx = min(560, x0 - 24 - tw)
            ty = y_line - 20
            draw.line([(tx + tw, ty + 20), (plot[0], y_line)], fill=CYAN, width=2)
        else:
            tx = plot[0] + 12 + chip_dx if chip_x is None else chip_x
            tx = min(max(tx, x0 + 12), x1 - 12 - tw)
            ty = y_line - 20
        draw.rounded_rectangle([tx, ty, tx + tw, ty + 40], 8, fill=TAG, outline=CYAN, width=2)
        draw.text((tx + 12, ty + 4), text, font=face, fill=WHITE)


def paint_brand(base: Image.Image, shot: dict, local: float) -> None:
    draw = ImageDraw.Draw(base)
    mark = scaled(wordmark(), 128)
    # Keep the lockup left of the mascot.
    paste(base, mark, (MX, 150))
    a = ease(min(1.0, max(0.0, local - 0.3) / 0.6))
    if a > 0:
        draw.text((MX, 310), "Blueprint", font=font(40), fill=CYAN)
    if local > 0.8:
        num = shot["lesson_no"]
        draw.text((MX, 390), f"Lesson {num}", font=font(72), fill=WHITE)
    if local > 1.2:
        lines = wrap(shot["lesson_title"], 56, 980)[:2]
        y = 490
        for line in lines:
            draw.text((MX, y), line, font=font(56), fill=WHITE)
            y += 70
    number = int(shot.get("lesson_no") or 1)
    _hero(base, (1040, 220, 1760, 820), {1: "path", 2: "lines", 3: "orders"}.get(number, "regimes"))
    place_mascot(base, shot, (96, 660, 520, 970))


def paint_disclaimer(base: Image.Image, shot: dict, local: float) -> None:
    draw = ImageDraw.Draw(base)
    if shot.get("disclaimer_part") == 2:
        draw.rounded_rectangle([MX, 150, RIGHT, 940], 20, outline=CYAN, width=4)
    if " ".join(DISCLAIMER_LINES) != DISCLAIMER:
        raise SystemExit("disclaimer lines do not match the spoken disclaimer")
    # On screen together for the whole card, after a short fade.
    fade = ease(min(1.0, local / 0.45))
    if fade <= 0:
        return
    color = tuple(int(c * fade) for c in WHITE)
    wrapped: list[str] = []
    for line in DISCLAIMER_LINES:
        wrapped.extend(wrap(line, 40, W - 2 * MX - 40) or [line])
    block_h = len(wrapped) * 58
    y = max(160, (H - block_h) // 2 - 20)
    rule = 240
    rx = (W - rule) // 2
    draw.rectangle([rx, y - 36, rx + rule, y - 28], fill=CYAN)
    for line in wrapped:
        tw = font(40).getlength(line)
        x = (W - tw) / 2
        draw.text((x, y), line, font=font(40), fill=color)
        y += 58


def _tick(draw: ImageDraw.ImageDraw, x: int, y: int) -> None:
    """A plain tick. The old checklist used letter marks such as B and EX."""
    draw.line([(x - 14, y), (x - 4, y + 12), (x + 16, y - 14)], fill=MINT, width=4)


def _row_icon(draw: ImageDraw.ImageDraw, x: int, y: int, kind: str) -> None:
    """40px-plus icons. Amber is only the stop sign."""
    if kind == "book":
        draw.rounded_rectangle([x - 18, y - 16, x + 18, y + 16], 3, outline=CYAN, width=3)
        draw.line([(x, y - 16), (x, y + 16)], fill=CYAN, width=3)
    elif kind == "ladder":
        draw.line([(x - 14, y - 20), (x - 14, y + 20)], fill=CYAN, width=3)
        draw.line([(x + 14, y - 20), (x + 14, y + 20)], fill=CYAN, width=3)
        for step in (-12, 0, 12):
            draw.line([(x - 14, y + step), (x + 14, y + step)], fill=CYAN, width=3)
    elif kind == "band":
        draw.line([(x - 18, y - 8), (x + 18, y - 8)], fill=CYAN, width=3)
        draw.line([(x - 18, y + 8), (x + 18, y + 8)], fill=CYAN, width=3)
    elif kind == "coin":
        draw.ellipse([x - 18, y - 18, x + 18, y + 18], outline=CYAN, width=3)
        draw.text((x - 8, y - 14), "B", font=font(28), fill=CYAN)
    elif kind == "paper":
        draw.rectangle([x - 14, y - 18, x + 14, y + 18], outline=CYAN, width=3)
        draw.line([(x - 8, y - 6), (x + 8, y - 6)], fill=CYAN, width=2)
        draw.line([(x - 8, y + 4), (x + 8, y + 4)], fill=CYAN, width=2)
    elif kind == "lock":
        draw.rounded_rectangle([x - 14, y - 2, x + 14, y + 18], 3, outline=CYAN, width=3)
        draw.arc([x - 10, y - 20, x + 10, y + 2], 180, 0, fill=CYAN, width=3)
    elif kind == "stop":
        draw.regular_polygon((x, y, 20), 8, outline=AMBER, width=3)
    else:
        draw.rounded_rectangle([x - 20, y - 16, x + 20, y + 16], 6, outline=CYAN, width=3)
        draw.text((x - 12, y - 12), "EX", font=font(22), fill=CYAN)


def paint_board(base: Image.Image, shot: dict) -> None:
    """A heading frame that shows the idea in words a beginner can read."""
    draw = ImageDraw.Draw(base)
    board = shot.get("board")
    if board == "seven-lines":
        rows = [
            "1. A notebook.",
            "2. Range, levels, and stop.",
            "3. The pair: bitcoin, public daily closes.",
            "4. Paper, or a demo.",
            "5. No secrets on this page.",
            "6. The stop, written as a sentence.",
            "7. The word Example on every figure.",
        ]
        draw.text((MX + 80, 186), "These are the seven lines on the page.", font=font(32), fill=WHITE)
        y = 240
        for row in rows:
            draw.rounded_rectangle([MX, y, RIGHT, y + 68], 12, fill=GLASS, outline=LINE, width=2)
            _tick(draw, 130, y + 34)
            draw.text((188, y + 16), row, font=font(32), fill=WHITE)
            draw.ellipse([1760, y + 16, 1796, y + 52], outline=MINT, width=3)
            draw.line([(1768, y + 34), (1778, y + 44), (1790, y + 24)], fill=MINT, width=3)
            y += 76
        return
    if board == "no-secrets":
        draw.text((MX, 176), "Never on the page", font=font(32), fill=AMBER)
        draw.text((1040, 176), "Allowed on the page", font=font(32), fill=MINT)
        banned = ["Seed phrase", "Private key", "API secret", "Account balance"]
        allowed = ["Public daily close", "The word Example", "A figure marked Example"]
        y = 230
        for text in banned:
            draw.rounded_rectangle([MX, y, 980, y + 100], 14, fill=GLASS, outline=AMBER, width=2)
            draw.line([(MX + 28, y + 28), (MX + 56, y + 56)], fill=AMBER, width=4)
            draw.line([(MX + 56, y + 28), (MX + 28, y + 56)], fill=AMBER, width=4)
            draw.text((MX + 76, y + 30), text, font=font(36), fill=WHITE)
            y += 112
        y = 230
        for text in allowed:
            draw.rounded_rectangle([1040, y, RIGHT, y + 100], 14, fill=GLASS, outline=MINT, width=2)
            draw.line([(1070, y + 52), (1082, y + 64), (1102, y + 36)], fill=MINT, width=4)
            draw.text((1120, y + 30), text, font=font(32), fill=WHITE)
            y += 112
        return
    if board == "three-words":
        cards = [
            ("Range", "24,930 to 30,331", "band"),
            ("Levels", "Six gaps. About 900.", "ladder"),
            ("Stop", "Leaves 30,331.", "stop"),
        ]
        y = 200
        for title, body, kind in cards:
            draw.rounded_rectangle([MX, y, RIGHT, y + 150], 16, fill=GLASS, outline=CYAN, width=2)
            _row_icon(draw, MX + 56, y + 75, kind)
            draw.text((MX + 110, y + 40), title, font=font(52), fill=CYAN)
            draw.text((MX + 420, y + 48), body, font=font(44), fill=WHITE)
            pic = 1540
            if kind == "band":
                draw.line([(pic, y + 52), (pic + 180, y + 52)], fill=CYAN, width=4)
                draw.line([(pic, y + 96), (pic + 180, y + 96)], fill=CYAN, width=4)
            elif kind == "ladder":
                _row_icon(draw, pic + 90, y + 75, "ladder")
            else:
                _row_icon(draw, pic + 90, y + 75, "stop")
            y += 170
        # Header, clear of the range lines. The pill used to sit on them.
        pill_w = int(font(36).getlength("EXAMPLE")) + 36
        _example(draw, RIGHT - 24 - pill_w, 78)
        return
    raise SystemExit(f"unknown board {board}")


def paint_stack(base: Image.Image, shot: dict, local: float) -> None:
    draw = ImageDraw.Draw(base)
    items = shot.get("items") or [shot.get("caption") or ""]
    index = int(shot.get("index") or 0)
    text = items[min(index, len(items) - 1)]
    lines = wrap(text, 44, W - 2 * MX - 96)[:3]
    card_h = 150 + len(lines) * 58
    draw.rounded_rectangle([MX, 210, RIGHT, 210 + card_h], 24, fill=GLASS, outline=CYAN, width=3)
    draw.text((MX + 36, 236), f"{index + 1} of {len(items)}", font=font(36), fill=CYAN)
    y = 300
    for line in lines:
        draw.text((MX + 36, y), line, font=font(44), fill=WHITE)
        y += 58


def paint_worked(base: Image.Image, shot: dict, local: float) -> None:
    draw = ImageDraw.Draw(base)
    rows = shot.get("items") or []
    if not rows:
        return
    shown = 1 + int(ease(min(1.0, local / max(0.8, len(rows) * 0.35))) * (len(rows) - 1))
    y = 190
    for text in rows[:shown]:
        draw.rounded_rectangle([MX, y, RIGHT, y + 110], 16, fill=GLASS, outline=CYAN, width=2)
        size = 48 if font(48).getlength(text) < (W - 2 * MX - 80) else 44
        yy = y + 28
        for line in wrap(text, size, W - 2 * MX - 80)[:2]:
            draw.text((MX + 32, yy), line, font=font(size), fill=WHITE)
            yy += size + 4
        y += 128


def _contain(src: Image.Image, pw: int, ph: int) -> tuple[Image.Image, int, int, float]:
    """Fit the whole still inside the panel. Nothing is cropped."""
    scale = min(pw / src.width, ph / src.height)
    nw, nh = max(1, int(src.width * scale)), max(1, int(src.height * scale))
    fitted = src.resize((nw, nh), Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", (pw, ph), NAVY2)
    ox, oy = (pw - nw) // 2, (ph - nh) // 2
    canvas.paste(fitted, (ox, oy))
    return canvas, ox, oy, scale


def _cover_label(draw: ImageDraw.ImageDraw, old: tuple[int, int, int, int], lines: list[str], bounds: tuple[int, int, int, int]) -> None:
    """28px tag that hides a baked-in label and stays inside the panel."""
    face = font(28)
    pad_x, line_h, pad_y = 14, 34, 10
    tw = max(int(face.getlength(line)) for line in lines) + pad_x * 2
    th = pad_y * 2 + line_h * len(lines)
    ox0, oy0, ox1, oy1 = old
    bx0, by0, bx1, by1 = bounds
    x0, y0 = ox0, oy0
    x1, y1 = max(ox1, ox0 + tw), max(oy1, oy0 + th)
    if x1 - x0 < tw:
        x1 = x0 + tw
    if y1 - y0 < th:
        y1 = y0 + th
    if x1 > bx1:
        x0 -= x1 - bx1
        x1 = bx1
    if x0 < bx0:
        x1 += bx0 - x0
        x0 = bx0
    if y1 > by1:
        y0 -= y1 - by1
        y1 = by1
    if y0 < by0:
        y1 += by0 - y0
        y0 = by0
    x0, y0 = min(x0, ox0), min(y0, oy0)
    x1, y1 = max(x1, ox1, x0 + tw), max(y1, oy1, y0 + th)
    draw.rounded_rectangle([x0, y0, x1, y1], 10, fill=TAG, outline=CYAN, width=2)
    y = y0 + (y1 - y0 - line_h * len(lines)) / 2
    for line in lines:
        draw.text((x0 + pad_x, y), line, font=face, fill=WHITE)
        y += line_h


def _retouch_analogy(draw: ImageDraw.ImageDraw, kind: str, origin: tuple[int, int]) -> None:
    """Replace baked tags that shrink below 28px. The still itself stays."""
    x, y = origin
    # Panel is 840 by 472, inset so labels stay off the rounded border.
    bounds = (x + 12, y + 12, x + 840 - 12, y + 472 - 12)
    if kind == "ladder":
        # Stop the rung label at the ladder's glow (screen x ~394).
        _cover_label(draw, (112, 400, 392, 444), ["Rung = one", "price step"], bounds)
        _cover_label(draw, (668, 440, 848, 506), ["Gap = the", "distance"], bounds)
        return
    if kind == "fence":
        # Tuned to the 1536x1024 fence still (contain scale 0.461, x offset 66).
        _cover_label(draw, (625, 316, 843, 368), ["Top rail = top price"], bounds)
        _cover_label(draw, (197, 568, 506, 622), ["Bottom rail", "= bottom price"], bounds)
        _cover_label(draw, (565, 568, 844, 622), ["Price bounces between"], bounds)
        return
    if kind == "list":
        # The passing checklist shrinks its own tags to ~17px. Cover them at 28px,
        # and stop before the binder rings (x ~400).
        edge = (104, 248, 400, 700)
        _cover_label(draw, (196, 360, 392, 404), ["Pair: what you trade"], edge)
        _cover_label(draw, (196, 428, 392, 488), ["Range: the band"], edge)
        _cover_label(draw, (196, 508, 380, 556), ["Gaps: step size"], edge)
        _cover_label(draw, (196, 572, 392, 620), ["Stop: when you quit"], edge)


def paint_analogy(base: Image.Image, shot: dict, local: float, dur: float) -> None:
    draw = ImageDraw.Draw(base)
    pw, ph = 840, 472
    origin = (MX, 230)
    kind = shot.get("analogy") or ""
    if kind == "list":
        still = shot.get("still")
        if still:
            panel, _ox, _oy, _scale = _contain(load_picture(Path(still)).convert("RGB"), pw, ph)
            base.paste(panel, origin)
            _retouch_analogy(draw, "list", origin)
        page = (origin[0] + pw + 24, 200, RIGHT, 760)
        draw.rounded_rectangle(page, 20, fill=GLASS, outline=CYAN, width=2)
        draw.text((page[0] + 28, page[1] + 28), "Write the page before any screen", font=font(32), fill=WHITE)
        rows = (("Band", "24,930 to 30,331"), ("Levels", "Six gaps. About 900."), ("Stop", "The close leaves 30,331."))
        y = page[1] + 110
        for name, value in rows:
            draw.text((page[0] + 36, y), name, font=font(36), fill=CYAN)
            draw.text((page[0] + 240, y), value, font=font(36), fill=WHITE)
            y += 80
        pill = font(36)
        pill_w = int(pill.getlength("EXAMPLE")) + 36
        _example(draw, page[2] - pill_w - 28, page[1] + 36)
        return
    chart_box = (origin[0] + pw + 24, 180, RIGHT, 752)
    still = shot.get("still")
    if still and kind in {"ladder", "fence"}:
        panel, ox, oy, scale = _contain(load_picture(Path(still)).convert("RGB"), pw, ph)
        base.paste(panel, origin)
        if kind == "fence":
            src_h = load_picture(Path(still)).size[1]
            rail_top = int(413 * src_h / 1024)
            rail_bot = int(611 * src_h / 1024)
            shot["rail_marks"] = {
                "top": origin[1] + oy + rail_top * scale,
                "bottom": origin[1] + oy + rail_bot * scale,
                "x": origin[0] + ox + panel.size[0] - ox - 36,
            }
            shot["rail_marks"]["x"] = origin[0] + pw - 28
        _retouch_analogy(draw, kind, origin)
        if kind == "ladder":
            note = "Not to scale: the chart has 7 levels"
            face = font(28)
            tw = int(face.getlength(note)) + 28
            nx, ny = origin[0], origin[1] + ph + 10
            draw.rounded_rectangle([nx, ny, nx + tw, ny + 44], 10, fill=TAG, outline=CYAN, width=2)
            draw.text((nx + 14, ny + 6), note, font=face, fill=WHITE)
    draw.rounded_rectangle([origin[0], origin[1], origin[0] + pw, origin[1] + ph], 18, outline=LINE, width=2)
    chart_card(base, shot, local, dur, chart_box)


def next_lesson_label(shot: dict) -> tuple[str, str, str]:
    """Kicker, lesson label, and call to action for the end card."""
    title = (shot.get("caption") or "End of the Blueprint").strip()
    if title.rstrip(".") == "End of the Blueprint":
        return "END", "The Blueprint", "That is the last lesson"
    number = int(shot.get("lesson_no") or 1) + 1
    return "NEXT", f"Lesson {number}", f"Up next: Lesson {number}"


def cleared_mascot(shot: dict) -> Image.Image | None:
    """The approved cut-out only, and only when its scored blob still matches."""
    if not MASCOT_SRC.is_file():
        return None
    lesson = str(shot.get("lesson_id") or "")
    if not lesson:
        return None
    here = str(ROOT / "course/blueprint-rebuild")
    if here not in sys.path:
        sys.path.insert(0, here)
    import image_gate

    if not image_gate.DEFAULT_LIST.is_file():
        return None
    rel = "course/images/mascot/blueprint-mascot.png"
    for row in image_gate.load_pass_list(image_gate.DEFAULT_LIST):
        path = image_gate._norm(str(row.get("path") or ""))
        if path != rel or str(row.get("lesson") or "") != lesson:
            continue
        if not image_gate._passed(row) or image_gate.blob_problem(rel, row):
            return None
        return Image.open(MASCOT_SRC).convert("RGBA")
    return None


def place_mascot(base: Image.Image, shot: dict, box: tuple[int, int, int, int]) -> None:
    """Fit the approved cut-out in a box. The sheet is never drawn."""
    src = cleared_mascot(shot)
    if src is None:
        return
    alpha = src.getchannel("A")
    bounds = alpha.getbbox()
    if not bounds:
        return
    cut = src.crop(bounds)
    x0, y0, x1, y1 = box
    scale = min((x1 - x0) / cut.width, (y1 - y0) / cut.height)
    nw, nh = max(1, int(cut.width * scale)), max(1, int(cut.height * scale))
    fitted = cut.resize((nw, nh), Image.Resampling.LANCZOS)
    paste(base, fitted, (x0 + (x1 - x0 - nw) // 2, y0 + (y1 - y0 - nh) // 2))


def paint_outro(base: Image.Image, shot: dict, local: float) -> None:
    """Wordmark, the next lesson, and a glass card. No subscribe line."""
    draw = ImageDraw.Draw(base)
    _kicker, lesson_label, cta = next_lesson_label(shot)
    title = (shot.get("caption") or "End of the Blueprint").strip().rstrip(".")
    mark = scaled(wordmark(), 110)
    paste(base, mark, (MX, 72))
    draw.text((MX, 220), "NEXT", font=font(28), fill=CYAN)
    draw.text((MX, 268), lesson_label, font=font(40), fill=CYAN)
    y = 340
    for line in wrap(title, 56, 900)[:3]:
        draw.text((MX, y), line, font=font(56), fill=WHITE)
        y += 68
    number = int(shot.get("lesson_no") or 1) + 1
    mode = {2: "lines", 3: "orders", 4: "regimes"}.get(number, "path")
    # The orders chip at the plot's left edge covers the July drop.
    _hero(base, (1120, 240, 1760, 800), mode, chip_dx=-40 if mode == "orders" else 0)
    place_mascot(base, shot, (96, 560, 560, 960))
    foot = font(36, "reg")
    fw = foot.getlength(FOOT)
    draw.text(((W - fw) / 2, 980), FOOT, font=foot, fill=MUTED)
    if local < 0.35:
        fade = Image.new("RGB", (W, H), NAVY)
        base.paste(Image.blend(fade, base, ease(local / 0.35)))


def paint_lesson_thumb(shot: dict, dest: Path) -> Path:
    """1280x720 thumbnail. One cyan keyword, a hero, and the course footer."""
    image = Image.new("RGB", (1280, 720), NAVY)
    draw = ImageDraw.Draw(image)
    for x in range(0, 1280, 48):
        draw.line([(x, 0), (x, 720)], fill=(18, 36, 58))
    for y in range(0, 720, 48):
        draw.line([(0, y), (1280, y)], fill=(18, 36, 58))
    number = int(shot.get("lesson_no") or 1)
    title = "Your first range" if number == 1 else (shot.get("lesson_title") or "Blueprint")
    keyword = {1: "range", 2: "need", 3: "grid"}.get(number, title.split()[-1])
    words = title.split()
    face = font(120)
    lines: list[list[str]] = []
    current: list[str] = []
    for word in words:
        trial = " ".join(current + [word])
        if current and face.getlength(trial) > 740:
            lines.append(current)
            current = [word]
        else:
            current.append(word)
    if current:
        lines.append(current)
    draw.text((48, 70), f"Blueprint · Lesson {number:02d}", font=font(32), fill=MUTED)
    y = 130
    for line in lines[:3]:
        x = 48
        for word in line:
            draw.text((x, y), word, font=face, fill=CYAN if word.lower() == keyword else WHITE)
            x += int(face.getlength(word + " "))
        y += 130
    # The thumbnail mascot was a speck between the headline and the footer.
    # The title and end cards already carry it.
    _hero(
        image,
        (820, 120, 1230, 560),
        {1: "path", 2: "lines", 3: "orders"}.get(number, "regimes"),
        chip_beside=(number == 3),
    )
    draw = ImageDraw.Draw(image)
    draw.text((48, 660), FOOT, font=font(28, "reg"), fill=MUTED)
    dest.parent.mkdir(parents=True, exist_ok=True)
    image.save(dest)
    return dest


def paint_lesson_still(base: Image.Image, shot: dict, local: float, dur: float) -> None:
    """Fit a 1536x1024 still in the stage. A short pan is the only move. No upscale."""
    src = load_picture(Path(shot["lesson_still"])).convert("RGB")
    box = (MX, 156, RIGHT, 760)
    pw, ph = box[2] - box[0], box[3] - box[1]
    scale = min(pw / src.width, ph / src.height, 1.0)
    zoom = scale * (0.94 + 0.06 * ease(min(1.0, local / max(dur, 0.1))))
    nw, nh = max(1, int(src.width * zoom)), max(1, int(src.height * zoom))
    fitted = src.resize((nw, nh), Image.Resampling.LANCZOS)
    view_w, view_h = min(pw, nw), min(ph, nh)
    max_x = max(0, nw - view_w)
    pan = int(max_x * ease(min(1.0, local / max(dur, 0.1))))
    crop = fitted.crop((pan, 0, pan + view_w, view_h))
    x = box[0] + (pw - view_w) // 2
    y = box[1] + (ph - view_h) // 2
    base.paste(crop, (x, y))


def paint_candle(base: Image.Image, shot: dict) -> None:
    """One day, large enough to see the high, the low, and the close."""
    draw = ImageDraw.Draw(base)
    box = (MX, 190, RIGHT, 760)
    draw.rounded_rectangle(box, 22, fill=GLASS, outline=LINE, width=2)
    candle = shot.get("candle") or {}
    high = int(candle.get("high") or 0)
    low = int(candle.get("low") or 0)
    close = int(candle.get("close") or 0)
    title = candle.get("date") or shot.get("chart_title") or "One day"
    draw.text((box[0] + 36, box[1] + 24), title, font=font(36), fill=WHITE)
    _example(draw, box[2] - 220, box[1] + 24)
    span = max(1, high - low)
    top, bot = box[1] + 140, box[3] - 80
    cx = (box[0] + box[2]) // 2

    def y_of(price: int) -> int:
        return int(top + (high - price) / span * (bot - top))

    y_high, y_low, y_close = y_of(high), y_of(low), y_of(close)
    draw.line([(cx, y_high), (cx, y_low)], fill=CYAN, width=6)
    body_top = min(y_close, y_close - 36)
    draw.rounded_rectangle([cx - 36, body_top, cx + 36, y_close + 8], 8, fill=CYAN)
    labels = (
        (y_high, f"High {high:,}", -280),
        (y_close, f"Close {close:,}", 80),
        (y_low, f"Low {low:,}", -280),
    )
    for y, label, dx in labels:
        draw.text((cx + dx, y - 18), label, font=font(36), fill=WHITE)


def paint_course_map(base: Image.Image) -> None:
    """Labelled steps, with a plain line under each lesson name."""
    draw = ImageDraw.Draw(base)
    steps = (
        ("1", "Introduction", "What a grid is"),
        ("2", "Checklist", "What you write before any screen"),
        ("3", "Definition", "Buys below the price, sells above it"),
        ("4", "Regimes", "Is the market trending or going sideways?"),
        ("5", "Spacing", "How far apart the lines are"),
        ("6", "Entry and exit", "Write the finish rule first"),
        ("7", "Paper", "Copy the page onto a practice form"),
        ("8", "Monitoring", "Three questions, then stop"),
        ("9", "Mistakes", "A blank stop, a tight band, a bad count"),
        ("10", "Scaling", "A second page in its own bucket"),
        ("11", "Liquidation", "When borrowed money forces your position closed"),
    )
    left = steps[:6]
    right = steps[6:]
    for column, x in ((left, MX), (right, 1000)):
        y = 196
        for number, name, gloss in column:
            draw.rounded_rectangle([x, y, x + 56, y + 48], 10, fill=TAG, outline=CYAN, width=2)
            num_x = x + 16 if len(number) == 1 else x + 6
            draw.text((num_x, y + 6), number, font=font(28), fill=CYAN)
            draw.text((x + 72, y - 2), name, font=font(32), fill=CYAN)
            draw.text((x + 72, y + 36), gloss, font=font(28), fill=WHITE)
            y += 92


def paint(shot: dict, local: float, progress: float) -> np.ndarray:
    dur = float(shot.get("duration") or estimate(shot))
    img = background(local)
    kind = shot.get("kind") or "chart"
    if kind == "brand":
        paint_brand(img, shot, local)
        draw_footer(ImageDraw.Draw(img))
    elif kind == "disclaimer":
        paint_disclaimer(img, shot, local)
    elif kind == "outro":
        paint_outro(img, shot, local)
    elif kind == "stack":
        title_bar(img, shot, progress)
        paint_stack(img, shot, local)
        lower_third(ImageDraw.Draw(img), shot)
        draw_footer(ImageDraw.Draw(img))
    elif kind == "worked":
        title_bar(img, shot, progress)
        paint_worked(img, shot, local)
        lower_third(ImageDraw.Draw(img), shot)
        draw_footer(ImageDraw.Draw(img))
    elif kind == "analogy":
        title_bar(img, shot, progress)
        if shot.get("lesson_still"):
            paint_lesson_still(img, shot, local, dur)
        else:
            paint_analogy(img, shot, local, dur)
        lower_third(ImageDraw.Draw(img), shot)
        draw_footer(ImageDraw.Draw(img))
    elif kind == "lesson-still" and (shot.get("chapter") or "") == "The map":
        title_bar(img, shot, progress)
        paint_course_map(img)
        lower_third(ImageDraw.Draw(img), shot)
        draw_footer(ImageDraw.Draw(img))
    elif kind == "lesson-still":
        title_bar(img, shot, progress)
        paint_lesson_still(img, shot, local, dur)
        lower_third(ImageDraw.Draw(img), shot)
        draw_footer(ImageDraw.Draw(img))
    else:
        title_bar(img, shot, progress)
        if shot.get("board") in {"seven-lines", "no-secrets", "three-words"}:
            paint_board(img, shot)
        elif shot.get("candle"):
            paint_candle(img, shot)
        else:
            chart_card(img, shot, local, dur)
        lower_third(ImageDraw.Draw(img), shot)
        draw_footer(ImageDraw.Draw(img))
    return np.asarray(img, dtype=np.uint8)


def margin_ink(frame: np.ndarray) -> tuple[int, int, int, int]:
    ink = frame.max(axis=2) > 70
    return (
        int(ink[:MY, :].sum()),
        int(ink[-48:, :].sum()),
        int(ink[:, :MX].sum()),
        int(ink[:, -MX:].sum()),
    )


def write_stills(sid: str) -> None:
    shots = plan(sid)
    dest = Path(f"/tmp/bp-proof/{sid}")
    dest.mkdir(parents=True, exist_ok=True)
    want = {"brand", "disclaimer", "chart", "stack", "analogy", "worked", "outro"}
    saved = 0
    for i, shot in enumerate(shots):
        kind = shot.get("kind") or "chart"
        if kind not in want and not (kind == "chart" and saved < 8):
            continue
        if kind in want:
            want.discard(kind)
        dur = estimate(shot)
        shot["duration"] = dur
        frame = paint(shot, dur * 0.82, (i + 1) / len(shots))
        path = dest / f"{i:02d}-{kind}.png"
        Image.fromarray(frame).save(path)
        print(kind, "margins", margin_ink(frame), path)
        saved += 1
        if not want and saved >= 8:
            break
    print(f"stills {saved} in {dest}")


def run(cmd: list[str]) -> None:
    subprocess.check_call(cmd)


def measured_lufs(path: Path) -> tuple[float, float]:
    proc = subprocess.run(
        ["ffmpeg", "-hide_banner", "-i", str(path), "-af", "ebur128=peak=true", "-f", "null", "-"],
        capture_output=True, text=True,
    )
    text = proc.stderr
    integ = re.findall(r"I:\s*(-?\d+\.?\d*)\s*LUFS", text)
    peak = re.findall(r"Peak:\s*(-?\d+\.?\d*)\s*dBFS", text)
    if not integ:
        raise SystemExit(f"no loudness for {path}\n{text[-500:]}")
    true_peak = float(peak[-1]) if peak else 0.0
    return float(integ[-1]), true_peak


def _lesson_bed(duration: float, dest: Path) -> None:
    """In-house calm bed. Synthesised in the repo, so there is nothing to license."""
    music = ROOT / "skills/video-production/music-sound"
    if str(music) not in sys.path:
        sys.path.insert(0, str(music))
    from music.compose import render_bed

    need = max(2.0, float(duration))
    if need <= 590:
        audio, sr = render_bed(mood="calm", key="C", scale="major", bpm=72, seconds=need)
    else:
        audio = None
        sr = 48000
        left = need
        while left > 1:
            take = min(480.0, left)
            piece, sr = render_bed(mood="calm", key="C", scale="major", bpm=72, seconds=take)
            audio = piece if audio is None else _xfade(audio, piece, sr, fade=1.0)
            left -= take
    sf.write(str(dest), audio, sr)


def compose_pad(duration: float, dest: Path) -> None:
    """Slow detuned pad. No melody, no rhythm, no bleeps. Original."""
    sr = 48000
    n = int((duration + 1.0) * sr)
    t = np.arange(n, dtype=np.float64) / sr
    left = np.zeros(n)
    right = np.zeros(n)
    partials = [(98.0, 0.20), (146.83, 0.11), (196.0, 0.07), (246.94, 0.035)]
    for freq, amp in partials:
        wobble = 0.9 + 0.1 * np.sin(2 * np.pi * 0.04 * t + freq)
        left += amp * wobble * np.sin(2 * np.pi * freq * t)
        right += amp * wobble * np.sin(2 * np.pi * freq * 1.002 * t + 0.6)
    rng = np.random.default_rng(7)
    white = rng.normal(0, 1, n)
    alpha = 0.015
    brown = np.empty(n)
    acc = 0.0
    for i, sample in enumerate(white):
        acc = (1 - alpha) * acc + alpha * sample
        brown[i] = acc
    brown *= 0.08 / (np.max(np.abs(brown)) + 1e-9)
    left += brown
    right += brown * 0.85
    peak = max(np.max(np.abs(left)), np.max(np.abs(right)), 1e-6)
    stereo = np.stack([left, right], axis=1).astype(np.float32) / peak * 0.4
    fade_in = min(len(stereo), int(2.0 * sr))
    fade_out = min(len(stereo), int(min(3.0, duration / 4) * sr))
    stereo[:fade_in] *= np.linspace(0, 1, fade_in, dtype=np.float32)[:, None]
    stereo[-fade_out:] *= np.linspace(1, 0, fade_out, dtype=np.float32)[:, None]
    # lib/mix.py is the only loudness pass. This file is not mastered here.
    sf.write(str(dest), stereo, sr)


def _voice_stack() -> None:
    root = ROOT / "skills/video-production"
    for folder in (root, root / "natural-voice"):
        text = str(folder)
        if text not in sys.path:
            sys.path.insert(0, text)


def _mood(kind: str) -> str:
    return {"brand": "upbeat-intro", "disclaimer": "serious-risk", "outro": "recap"}.get(kind, "calm-teacher")


def _tighten_narration(audio: np.ndarray, sr: int, words: list, gap: float = 0.35, tail: float = 0.45):
    """Shorten silence. Sentence gaps stay about 0.35s. A beat can end a little longer."""
    if len(audio) == 0:
        return audio, words
    thr = 10 ** (-42 / 20)
    hop = max(1, int(0.01 * sr))
    quiet = [float(np.max(np.abs(audio[i:i + hop]))) < thr for i in range(0, len(audio), hop)]
    keep = np.ones(len(audio), dtype=bool)
    i = 0
    while i < len(quiet):
        if not quiet[i]:
            i += 1
            continue
        j = i
        while j < len(quiet) and quiet[j]:
            j += 1
        start = i * hop
        end = min(len(audio), j * hop)
        dur = (end - start) / sr
        limit = tail if j >= len(quiet) else gap
        if dur > limit + 0.02:
            keep[start + int(limit * sr):end] = False
        i = j
    new_audio = audio[keep]
    mapping = np.cumsum(keep) - 1
    new_words = []
    last = len(audio) - 1
    for word in words:
        start = min(last, int(word.start * sr))
        end = min(last, max(start + 1, int(word.end * sr)))
        new_words.append(type(word)(
            word.text,
            float(mapping[start] / sr),
            float(max(mapping[end] / sr, mapping[start] / sr + 0.05)),
        ))
    return new_audio, new_words


def _lesson_sentences(text: str) -> list[str]:
    """Split on sentence stops. Commas stay inside the sentence."""
    cleaned = re.sub(r"\s+", " ", (text or "").strip())
    cleaned = re.sub(r"(\d)\.(\d)", r"\1<dot>\2", cleaned)
    parts = re.split(r"(?<=[.!?])\s+", cleaned)
    out = []
    for part in parts:
        part = part.replace("<dot>", ".").strip()
        if part:
            out.append(part)
    return out or ([cleaned] if cleaned else [])


def _reading_time(shot: dict) -> float:
    """At least 2s plus about 0.3s for each word of on-screen text."""
    blobs = [
        shot.get("caption") or "",
        shot.get("chapter") or "",
        " ".join(shot.get("items") or []),
    ]
    words = max((len(blob.split()) for blob in blobs), default=0)
    return 2.0 + 0.3 * words


def _xfade(left: np.ndarray, right: np.ndarray, sr: int, fade: float = JOIN_FADE) -> np.ndarray:
    n = min(int(fade * sr), len(left) // 2, len(right) // 2)
    if n < 2:
        return np.concatenate([left, right])
    out_r = np.linspace(1.0, 0.0, n, dtype=np.float32)
    in_r = np.linspace(0.0, 1.0, n, dtype=np.float32)
    mid = left[-n:] * out_r + right[:n] * in_r
    return np.concatenate([left[:-n], mid, right[n:]])


def _time_sentence(speaker, pace: float, text: str, audio: np.ndarray, sr: int, offset: float) -> list:
    """Align inside one sentence. Fall back to letter spacing if the aligner bunches words."""
    from voice.align import Word, align_templates

    tokens = text.split()
    if not tokens:
        return []
    templates = []
    for token in tokens:
        bare = token.strip(".,!?;:\"'") or token
        spoken, rate = speaker.say(bare, pace)
        if rate != sr:
            return _pace_words(text, audio, sr, offset)
        templates.append(np.asarray(spoken, dtype=np.float32))
    try:
        aligned = align_templates(audio, sr, tokens, templates)
    except Exception:
        aligned = None
    if aligned:
        bunched = sum(1 for word in aligned if word.end - word.start < 0.08)
        if bunched <= max(1, int(len(aligned) * 0.25)):
            return [Word(word.text, offset + word.start, offset + word.end) for word in aligned]
    return _pace_words(text, audio, sr, offset)


def _pace_words(text: str, audio: np.ndarray, sr: int, offset: float) -> list:
    """Place words across the sentence that was just spoken. No time-stretch."""
    from voice.align import Word

    tokens = text.split()
    if not tokens or len(audio) == 0:
        return []
    weights = [max(1, len(token.strip(".,!?;:\"'"))) for token in tokens]
    total = float(sum(weights))
    dur = len(audio) / sr
    cursor = 0.0
    placed = []
    for token, weight in zip(tokens, weights):
        span = dur * weight / total
        placed.append(Word(token, offset + cursor, offset + cursor + span))
        cursor += span
    if placed:
        last = placed[-1]
        placed[-1] = Word(last.text, last.start, offset + dur)
    return placed


def _narrate_shot(speaker, shot: dict) -> tuple[np.ndarray, int, list]:
    """One Kokoro speed for every sentence, then the pauses Stewart asked for."""
    from voice.moods import KOKORO_BASE_WPM, mood as mood_preset

    pace = KOKORO_BASE_WPM / mood_preset("calm-teacher")["wpm"]
    sentences = _lesson_sentences(shot.get("vo") or "")
    if not sentences:
        sr = 24000
        audio = np.zeros(int(BEAT_GAP * sr), dtype=np.float32)
        return audio, sr, []
    buf = None
    timed = []
    sr = None
    for index, sentence in enumerate(sentences):
        audio, rate = speaker.say(sentence, pace)
        audio = np.asarray(audio, dtype=np.float32)
        if sr is None:
            sr = rate
        elif rate != sr:
            raise SystemExit("voice sample rate changed mid-lesson")
        if buf is None:
            offset = 0.0
            buf = audio
        else:
            offset = max(0.0, len(buf) / sr - JOIN_FADE)
            buf = _xfade(buf, audio, sr)
        timed.extend(_time_sentence(speaker, pace, sentence, audio, sr, offset))
        if index < len(sentences) - 1:
            buf = _xfade(buf, np.zeros(int(SENTENCE_GAP * sr), dtype=np.float32), sr)
    hold = max(0.0, _reading_time(shot) - len(buf) / sr)
    revealing = shot.get("kind") in {"chart", "analogy"} and not shot.get("board") and not shot.get("candle")
    cap = REVEAL_GAP_CAP if revealing else LINE_GAP_CAP
    tail = min(cap, hold + BEAT_GAP)
    if tail > 0:
        buf = _xfade(buf, np.zeros(int(tail * sr), dtype=np.float32), sr)
    return buf, sr, timed


def synth_voice(shots: list[dict], dest: Path) -> tuple[float, list]:
    """Kokoro af_heart at natural speed 1.0, with the same pace on every beat."""
    _voice_stack()
    from voice.align import Word
    from voice.moods import kokoro_speed, mood as mood_preset
    from voice.speak import Speaker

    if mood_preset("calm-teacher").get("kokoro_voice") != "af_heart":
        raise SystemExit("Blueprint narration must be Kokoro af_heart")
    pace = 197.0 / mood_preset("calm-teacher")["wpm"]
    if abs(kokoro_speed("calm-teacher", pace) - 1.0) > 1e-6:
        raise SystemExit("natural pace did not land on Kokoro speed 1.0")
    speaker = Speaker(engine="kokoro", mood="calm-teacher")
    pieces: list[np.ndarray] = []
    timed: list[Word] = []
    expanded: list[dict] = []
    clock = 0.0
    sample_rate = None
    for i, shot in enumerate(shots):
        audio, rate, words = _narrate_shot(speaker, shot)
        if sample_rate is None:
            sample_rate = rate
        if rate != sample_rate:
            raise SystemExit("voice sample rate changed mid-lesson")
        for word in words:
            timed.append(Word(word.text, clock + word.start, clock + word.end))
        shot = dict(shot)
        shot["duration"] = len(audio) / rate
        shot["_audio"] = audio
        pieces.append(audio)
        expanded.append(shot)
        clock += shot["duration"]
        if (i + 1) % 4 == 0:
            print(f"  voice {i + 1}/{len(shots)} t={clock:.0f}s", flush=True)
    voice = np.concatenate(pieces) if pieces else np.zeros(1, dtype=np.float32)
    sf.write(str(dest), voice, sample_rate or 24000)
    return clock, timed, expanded


def _write_lesson_captions(vtt: Path, srt: Path, words: list) -> None:
    """Cues start on the spoken word. A short line holds into the pause, not early."""
    from voice.captions import _stamp

    groups: list[list] = []
    current: list = []
    for word in words:
        trial = current + [word]
        text = " ".join(item.text for item in trial)
        if current and len(text) > 42:
            groups.append(current)
            current = [word]
        else:
            current = trial
    if current:
        groups.append(current)
    cues = []
    for index, group in enumerate(groups):
        text = " ".join(word.text for word in group)
        start = group[0].start
        spoken = group[-1].end
        nxt = groups[index + 1][0].start if index + 1 < len(groups) else None
        end = max(spoken, start + len(text) / 18.0)
        # A cue may hold a fifth of a second into the next line so it stays readable.
        if nxt is not None:
            end = min(end, nxt + 0.20)
        cues.append((start, max(end, start + 0.2), [text]))
    vtt_lines = ["WEBVTT", ""]
    srt_lines = []
    for index, (start, end, lines) in enumerate(cues, start=1):
        vtt_lines.append(f"{_stamp(start)} --> {_stamp(end)}")
        vtt_lines.extend(lines)
        vtt_lines.append("")
        srt_lines.append(str(index))
        srt_lines.append(f"{_stamp(start, srt=True)} --> {_stamp(end, srt=True)}")
        srt_lines.extend(lines)
        srt_lines.append("")
    vtt.write_text("\n".join(vtt_lines) + "\n", encoding="utf-8")
    srt.write_text("\n".join(srt_lines) + "\n", encoding="utf-8")


def _wrap_caption(text: str) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        trial = f"{current} {word}".strip()
        if current and len(trial) > 42 and len(lines) < 1:
            lines.append(current)
            current = word
        else:
            current = trial
    if current:
        lines.append(current)
    if len(lines) > 2:
        lines = [" ".join(lines[:-1]), lines[-1]]
    return lines[:2]


def _split_picture(shot: dict, audio: np.ndarray, rate: int) -> list[dict]:
    """Cut a shot at 8 seconds and switch the picture. A glow is not the switch."""
    limit = max(1, int((MAX_SHOT - 0.05) * rate))
    parts = []
    offset = 0
    index = 0
    while offset < len(audio):
        chunk = audio[offset:offset + limit]
        nxt = dict(shot)
        nxt["duration"] = len(chunk) / rate
        nxt["_audio"] = chunk
        nxt["slice"] = index
        if index % 2 == 1:
            if nxt.get("lesson_still") and nxt.get("kind") != "lesson-still":
                nxt["kind"] = "lesson-still"
            elif nxt.get("kind") == "lesson-still":
                nxt["kind"] = "chart"
            elif nxt.get("kind") == "disclaimer":
                nxt["disclaimer_part"] = 2
            else:
                nxt["kind"] = "chart" if nxt.get("kind") != "chart" else "stack"
        parts.append(nxt)
        offset += limit
        index += 1
    return parts


def _excerpt(shots: list[dict], seconds: float) -> list[dict]:
    """Brand, the disclaimer card, two lesson stills, and the end card."""
    brand = next(shot for shot in shots if shot.get("kind") == "brand")
    disc = next(shot for shot in shots if shot.get("kind") == "disclaimer")
    stills = [shot for shot in shots if shot.get("lesson_still")][:2]
    if len(stills) < 2:
        raise SystemExit("excerpt needs two numbered lesson stills")
    for shot in stills:
        shot["kind"] = "lesson-still"
        line = (shot.get("alt") or shot.get("caption") or "Look at the picture.").strip()
        shot["vo"] = line.rstrip(".") + "."
        shot["caption"] = shot["vo"]
    kept = [brand, disc, stills[0], stills[1]]
    kept.append({
        "kind": "outro",
        "chapter": "Next",
        "vo": "Next. The page stays marked example. No order is sent.",
        "caption": "What you are going to need",
        "lesson_no": shots[0].get("lesson_no", "01"),
        "lesson_title": shots[0].get("lesson_title", "Blueprint"),
        "term": "Next",
        "definition": "Education only. Not financial advice.",
        "example": False,
        "series": [],
    })
    return kept


def _lesson_yaml(sid: str, shots: list[dict], dest: Path) -> None:
    """Figures in the yaml carry the word EXAMPLE, matching the on-screen badge."""
    beats = []
    for shot in shots:
        vo = shot.get("vo") or ""
        caption = shot.get("caption") or ""
        if re.search(r"\d", vo) and "example" not in vo.lower():
            vo = vo.rstrip(".") + ", marked EXAMPLE."
        if re.search(r"\d", caption) and "example" not in caption.lower():
            caption = caption.rstrip(".") + ", marked EXAMPLE."
        beats.append({
            "id": _slug(str(shot.get("chapter") or shot.get("kind"))),
            "chapter": shot.get("chapter") or shot.get("kind"),
            "vo": vo,
            "caption": caption,
        })
    payload = {
        "id": sid,
        "format": "blueprint",
        "disclaimer_spoken": DISCLAIMER,
        "disclaimer_on_screen": "Education only. Not financial advice.",
        "beats": beats,
        "chart_labels": sorted({
            token.replace(",", "")
            for shot in shots
            for token in re.findall(r"\d[\d,]*", f"{shot.get('caption') or ''} {shot.get('vo') or ''}")
            if len(token.replace(",", "")) >= 2
        }),
    }
    dest.write_text(
        "id: " + sid + "\n"
        "format: blueprint\n"
        "disclaimer_spoken: " + json_quote(DISCLAIMER) + "\n"
        "disclaimer_on_screen: \"Education only. Not financial advice.\"\n"
        "beats:\n" + "".join(
            "  - id: " + beat["id"] + "\n"
            "    chapter: " + json_quote(str(beat["chapter"])) + "\n"
            "    vo: " + json_quote(beat["vo"]) + "\n"
            "    caption: " + json_quote(beat["caption"]) + "\n"
            for beat in payload["beats"]
        )
        + "chart_labels:\n"
        + "".join(f"  - {json_quote(label)}\n" for label in payload["chart_labels"])
    )


def json_quote(text: str) -> str:
    return json.dumps(text, ensure_ascii=False)


def _slug(text: str) -> str:
    keep = "".join(ch.lower() if ch.isalnum() else "-" for ch in text)
    return "-".join(part for part in keep.split("-") if part) or "shot"


def render(
    sid: str,
    *,
    excerpt_seconds: float | None = None,
    pass_list: Path | None = None,
    dest: Path | None = None,
) -> Path:
    if sid.startswith("el-"):
        raise SystemExit("refusing Elite id")
    here = str(ROOT / "course/blueprint-rebuild")
    if here not in sys.path:
        sys.path.insert(0, here)
    import image_gate
    image_gate.require(sid, pass_list)
    shots = plan(sid)
    if excerpt_seconds:
        shots = _excerpt(shots, excerpt_seconds)
    words = sum(len(s["vo"].split()) for s in shots)
    print(f"{sid} shots {len(shots)} words {words}", flush=True)
    work = Path(f"/tmp/bp-rebuild/{sid}")
    if work.exists():
        for child in work.iterdir():
            if child.is_file():
                child.unlink()
    work.mkdir(parents=True, exist_ok=True)
    voice_path = work / "voice.wav"
    clock, timed, shots = synth_voice(shots, voice_path)
    print(f"  voice {clock:.1f}s", flush=True)
    bed = work / "bed.wav"
    _lesson_bed(clock + 1.2, bed)
    silent = work / "silent.mp4"
    proc = subprocess.Popen(
        [
            "ffmpeg", "-y", "-v", "error",
            "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "1920x1080", "-r", str(FPS),
            "-i", "-",
            "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p",
            "-profile:v", "high",
            "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
            str(silent),
        ],
        stdin=subprocess.PIPE,
    )
    assert proc.stdin is not None
    total = sum(int(round(s["duration"] * FPS)) for s in shots)
    drawn = 0
    lesson_t = 0.0
    prev = None
    fade_n = 8
    for shot in shots:
        frames = max(1, int(round(shot["duration"] * FPS)))
        shot["frames"] = frames
        for n in range(frames):
            local = n / FPS
            frame = paint(shot, local, lesson_t / clock)
            if prev is not None and n < fade_n:
                w = (n + 1) / fade_n
                frame = (prev * (1 - w) + frame * w).astype(np.uint8)
            proc.stdin.write(frame.tobytes())
            if n == frames - 1:
                prev = frame
            lesson_t += 1 / FPS
            drawn += 1
            if drawn % (FPS * 20) == 0:
                print(f"  frames {drawn}/{total}", flush=True)
    proc.stdin.close()
    if proc.wait() != 0:
        raise SystemExit("picture encode failed")
    _voice_stack()
    from lib.mix import duck_under_voice
    from voice.captions import write_chapters, write_words

    mixed = work / "mixed.wav"
    # Bed sits 20 dB under in the gaps. Gentle ducking holds it near 20 under the voice.
    duck_under_voice(
        bed, voice_path, mixed,
        bed_db=-20.0, attack_ms=150, release_ms=600, ratio=1.4, threshold=0.02,
    )
    final_path = dest or (OUT / f"{sid}.mp4")
    final_path.parent.mkdir(parents=True, exist_ok=True)
    preset = "veryfast" if excerpt_seconds else "medium"
    run([
        "ffmpeg", "-y", "-v", "error",
        "-i", str(silent), "-i", str(mixed),
        "-map", "0:v", "-map", "1:a",
        "-c:v", "libx264", "-preset", preset, "-crf", "17", "-profile:v", "high",
        "-pix_fmt", "yuv420p",
        "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
        # The native twoloop AAC coder wrote one sample to +1.9 dBFS in BP-03.
        # The WAV under it was already -2.9 dBTP. The fast coder keeps that peak.
        "-c:a", "aac", "-b:a", "320k", "-aac_coder", "fast", "-ar", "48000", "-ac", "2",
        "-shortest", "-movflags", "+faststart",
        str(final_path),
    ])
    sidecar = final_path.parent
    if "course" in sidecar.resolve().parts:
        sidecar = ROOT / "blueprint-smoke" / sid
        sidecar.mkdir(parents=True, exist_ok=True)
    write_words(sidecar / "words.json", timed, engine="kokoro", mood="af_heart", method="acoustic-forced-align")
    _write_lesson_captions(sidecar / f"{sid}.vtt", sidecar / f"{sid}.srt", timed)
    _cap_caption_speed(sidecar / f"{sid}.vtt")
    chapters = []
    cursor = 0.0
    for shot in shots:
        chapters.append((cursor, shot.get("chapter") or shot.get("kind") or "Section"))
        cursor += float(shot["duration"])
    if chapters:
        chapters[0] = (0.0, chapters[0][1])
    write_chapters(sidecar / "chapters.txt", chapters)
    numbers = ROOT / "course/blueprint-rebuild/numbers" / f"{sid}.yaml"
    if not numbers.is_file():
        raise SystemExit(f"numbers file missing: {numbers}. The gate will not check figures against the script echo.")
    templates = ROOT / "skills/video-production/templates"
    if str(templates) not in sys.path:
        sys.path.insert(0, str(templates))
    from pack.paint import paint_thumbnail
    paint_thumbnail(shots[0].get("lesson_title") or sid, "Blueprint", sidecar / "thumbnail.png")
    report_dir = sidecar / "gate"
    code = subprocess.call([
        sys.executable,
        str(ROOT / "skills/video-production/quality-gate/cli.py"),
        "check", str(final_path),
        "--format", "blueprint",
        "--captions", str(sidecar / f"{sid}.vtt"),
        "--transcript", str(numbers),
        "--lesson", str(numbers),
        "--out", str(report_dir),
    ])
    final_i, final_tp = measured_lufs(final_path)
    print(f"WROTE {final_path} {clock:.1f}s lufs {final_i:.1f} peak {final_tp:.1f}")
    print(f"GATE {report_dir / 'report.md'}")
    if code != 0:
        raise SystemExit(f"quality gate failed for {sid}. The build stops.")
    return final_path


def _cap_caption_speed(path: Path, limit: float = 18.0) -> None:
    """Hold every cue at or under the studio reading speed.

    The old cap deleted trailing words until one word remained, then stopped,
    because a single word has no space left to cut. The gate counts that
    leftover word (`len(cue text) / parsed span`), so a 0.35s cue stayed over
    the limit. This pass uses the gate's parser and lengthens or merges the
    cue. It does not delete words. Timestamp rounding is included, because the
    gate measures the milliseconds written in the file, not the float that
    was rounded away.
    """
    from voice.captions import refit_vtt_text

    path.write_text(refit_vtt_text(path.read_text(encoding="utf-8"), limit=limit), encoding="utf-8")
    gate_root = ROOT / "skills/video-production/quality-gate"
    if str(gate_root) not in sys.path:
        sys.path.insert(0, str(gate_root))
    from gate.captions import parse_captions

    for cue in parse_captions(path.read_text(encoding="utf-8")):
        span = cue.end - cue.start
        cps = len(cue.text) / span if span > 0 else float("inf")
        if cps > limit:
            raise SystemExit(
                f"{path.name} {cue.start:.2f}s is {cps:.1f} characters per second "
                f"after the {limit:.0f} cap"
            )


def _ts(sec: float) -> str:
    ms = int(round(sec * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d}.{ms:03d}"


def export_code_frames(dest_root: Path | None = None) -> list[Path]:
    """PNG stills only. No video, no audio, no lesson master."""
    dest_root = dest_root or (ROOT / "blueprint-smoke")
    lessons = (
        "bp-01-introduction",
        "bp-02-what-you-need",
        "bp-03-what-is-a-grid-bot",
    )
    templates = ROOT / "skills/video-production/templates"
    if str(templates) not in sys.path:
        sys.path.insert(0, str(templates))
    from pack.paint import paint_thumbnail

    saved: list[Path] = []
    for sid in lessons:
        planned = plan(sid)
        raw = lesson_scripts.attach_series(lesson_scripts.build(sid))
        number, title = parse_ident(raw[0])
        chosen: dict[str, dict] = {}
        for shot in raw:
            kind = shot.get("kind")
            if kind not in {"chart", "analogy"}:
                continue
            if kind == "analogy":
                shot["still"] = str(STILLS[shot.get("analogy") or "ladder"])
            shot["lesson_no"] = number
            shot["lesson_title"] = title
            shot["term"], shot["definition"] = thirds(shot)
            chart = _slug(str(shot.get("chart") or "chart"))
            chapter = _slug(str(shot.get("chapter") or "chart"))
            key = f"code-drawn/{sid}/chart/{chart}/{chapter}"
            prev = chosen.get(key)
            if prev is None or (shot.get("pin_date") and not prev.get("pin_date")):
                chosen[key] = shot
        for shot in planned:
            if shot.get("kind") == "brand":
                chosen[f"code-drawn/{sid}/title-card"] = shot
            elif shot.get("kind") == "outro":
                chosen[f"code-drawn/{sid}/end-card"] = shot
        for key, shot in chosen.items():
            dur = min(estimate(shot), MAX_SHOT - 0.05)
            frame_shot = dict(shot)
            frame_shot["duration"] = dur
            frame = paint(frame_shot, dur * 0.92, 0.45)
            path = dest_root / f"{key}.png"
            path.parent.mkdir(parents=True, exist_ok=True)
            Image.fromarray(frame).save(path)
            saved.append(path)
            print(path)
        thumb = dest_root / "code-drawn" / sid / "thumbnail.png"
        paint_lesson_thumb(planned[0], thumb)
        saved.append(thumb)
        print(thumb)
    return saved


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--id", default="")
    ap.add_argument("--stills", action="store_true")
    ap.add_argument("--frames", action="store_true", help="write code-drawn PNG stills and exit")
    ap.add_argument("--check-images", action="store_true")
    ap.add_argument("--excerpt", type=float, default=None, help="stop after about this many seconds")
    ap.add_argument("--pass-list", type=Path, default=None)
    ap.add_argument("--dest", type=Path, default=None)
    args = ap.parse_args()
    if args.check_images:
        import image_gate
        image_gate.require(args.id, args.pass_list)
        print(f"image gate pass {args.id}")
        return
    if args.frames:
        export_code_frames()
        return
    if not args.id:
        raise SystemExit("--id is required")
    if args.stills:
        write_stills(args.id)
        return
    render(args.id, excerpt_seconds=args.excerpt, pass_list=args.pass_list, dest=args.dest)


if __name__ == "__main__":
    main()
