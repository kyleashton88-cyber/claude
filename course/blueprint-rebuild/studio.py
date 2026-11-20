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
# Navy, cyan and white only. The old amber, mint and blue are not painted.
AMBER = WHITE
MUTED = (154, 168, 188)
BLUE = CYAN
MINT = CYAN
TAG = (10, 20, 40)
GLASS = (9, 22, 40)
LINE = (28, 64, 88)
FONT_DIR = ROOT / "skills/video-production/fonts/inter"
FONT = FONT_DIR / "Inter-Bold.ttf"
FONT_MED = FONT_DIR / "Inter-Medium.ttf"
FONT_REG = FONT_DIR / "Inter-Regular.ttf"
MX, MY = 96, 64
RIGHT = W - MX - 16
DISCLAIMER_LINES = (
    "Education only. Not financial advice.",
    "This is general information and doesn't consider your objectives, financial situation or needs.",
    "Crypto is high risk; you could lose all the money you put in.",
    "Past performance is not a reliable indicator of future results.",
)
DISCLAIMER = " ".join(DISCLAIMER_LINES)
FOOT = "Education only. Not financial advice."
COVER = ROOT / "course/images/style-ref/01M6MSHVNHX3WQH81XS8KQK1HT.png"
# Drop-in sheet. No crop. Replace the file to change the character.
MASCOT_SRC = ROOT / "course/images/mascot/blueprint-mascot.png"
WORD_BOX = (260, 52, 760, 176)
MAX_SHOT = 8.0
STILLS = {
    "ladder": ROOT / "course/images/blueprint-analogies/analogy-ladder.png",
    "list": ROOT / "course/images/blueprint-analogies/analogy-list.png",
    "buckets": ROOT / "course/images/blueprint-analogies/analogy-buckets.png",
}
# Seven summer rungs. The whole-window chart marks a crossing on each of these.
GRID_LEVELS = [24930, 25830, 26730, 27630, 28531, 29431, 30331]
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


def _log_clip(sid: str, shot: dict, original: str, shortened: str, status: str) -> None:
    """Record a shot the 4-sentence / 80-word cap would have changed."""
    path = ROOT / "course/blueprint-rebuild/CLIP_LOG.md"
    chapter = str(shot.get("chapter") or shot.get("kind") or "shot").replace("\n", " ")
    row = (
        f"- {sid} / {chapter} / {status}: {len(original.split())} words"
        f" (the old cap would have left {len(shortened.split())}).\n"
    )
    text = path.read_text(encoding="utf-8") if path.is_file() else "# Shots the old clip still notices\n\n"
    if row in text:
        return
    marker = f"# {sid}\n"
    if marker not in text:
        text = text.rstrip() + f"\n\n{marker}"
    path.write_text(text + row, encoding="utf-8")


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
    if shot.get("term_text"):
        defin = shot.get("definition_text") or ""
        if defin and not defin.endswith("."):
            defin += "."
        return shot["term_text"], defin
    chapter = (shot.get("chapter") or "").strip()
    cap = (shot.get("caption") or "").strip()
    low = chapter.lower()
    if low == "seven items":
        return "Seven items", "Seven items. The pair is the public series."
    # These headings only share a word with another definition. Show their own caption.
    if low == "one pair":
        return "Finished buy and sell", "Buy at the lower line and sell at the higher line. Fees come out of the gap. Marked Example."
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
            if key == "range" and "taken from the path" in (shot.get("vo") or ""):
                text = "The top line and the bottom line, taken from the path."
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
        full = shot.get("vo") or ""
        shot["vo"] = clip_vo(full, 3, 48)
        if shot["vo"] != full:
            _log_clip("chart-run", shot, full, shot["vo"], "still-clipped")
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
        "course/images/bp-01-introduction/015.png",
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
        "course/images/bp-01-introduction/007.png": "Buy orders sit on lines below the price and sell orders sit on lines above it. An order fills when the price reaches its line and the trade happens. The sells need some coin, so a grid starts with part cash and part coin, and that is a description, not advice.",
        "course/images/bp-01-introduction/011.png": "A fill is that trade at the line. As price climbs, each sell order fills. So you end up holding cash. As price falls, each buy order fills. So you end up holding coin.",
        "course/images/bp-01-introduction/010.png": (
            "This introduction is step one. Then what you need. Then exactly what a grid bot does, order by order. "
            "Then market regimes, spacing and range, and entry and exit. Then a paper test, weekly checks, and common mistakes. "
            "Then scaling up under written rules, and an opt-in lesson on liquidation with your complete plan."
        ),
        "course/images/bp-01-introduction/008.png": "The stop is your written rule for when you stop the bot.",
        "course/images/bp-01-introduction/012.png": "There is no promise of results in this lesson. Numbers marked Example are teaching numbers, not advice.",
        "course/images/bp-01-introduction/015.png": "Paper or demo trading is like driving with L-plates. You practise with pretend money before anything is real.",
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
        ("the weave they were built for is gone. Inventory can sit on one side.", "the bouncing they were built for is gone. As price climbs, each sell order fills, so you end up holding cash. As price falls, each buy order fills, so you end up holding coin."),
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
        ("If you have notes from those drafts, the multiple is the part you cross out.", "If old notes show a multiple, such as five times, cross it out."),
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
    spoken = line if line.endswith((".", "!", "?")) else line + "."
    caption = spoken
    if str(beat.get("chapter") or "").strip().lower() == "the map":
        caption = "The course in 11 steps. This lesson is step 1."
    return {
        "kind": "lesson-still",
        "chapter": beat.get("chapter") or "Picture",
        "vo": spoken,
        "caption": caption,
        "lesson_still": str((ROOT / beat["image"]).resolve()),
        "alt": spoken,
        "chart": "",
        "series": [],
        "example": False,
    }


def _attach_lesson_stills(sid: str, shots: list[dict]) -> None:
    """Hang each still on the shot that already speaks that beat.

    The spoken words come from lesson_scripts.py. The JSON file is a picture
    list only. It does not add a second line, and it does not get dumped in
    before the recap.
    """
    path = ROOT / "course/scripts" / f"{sid}.json"
    if not path.is_file():
        return
    beats = json.loads(path.read_text(encoding="utf-8")).get("beats") or []
    # 011 is the code-drawn leave diagram, not the still. 003 and 010 are the old title and map.
    retired = ("/003.png", "/010.png", "/011.png", "/013.png", "/015.png")
    used: set[int] = set()
    for beat in beats:
        image = str(beat.get("image") or "").replace("\\", "/")
        if not image or image.endswith(retired):
            continue
        role = (beat.get("role") or "").lower()
        if role in {"legal", "intro"}:
            continue
        target = None
        if image.endswith("/009.png"):
            target = next((s for s in shots if "No real order is sent" in (s.get("vo") or "")), None)
        elif image.endswith("/012.png"):
            target = next((s for s in shots if "no promise of results" in (s.get("vo") or "").lower()), None)
        else:
            chapter = str(beat.get("chapter") or "").strip().lower()
            aliases = {chapter}
            if chapter == "no result number":
                aliases.add("no promise of results")
            for index, shot in enumerate(shots):
                if index in used:
                    continue
                if shot.get("kind") in {"brand", "disclaimer", "outro", "chart"}:
                    continue
                if shot.get("candle") or shot.get("v2_cards") or shot.get("lesson_still"):
                    continue
                if str(shot.get("chapter") or "").strip().lower() in aliases:
                    target = shot
                    used.add(index)
                    break
        if target is None or target.get("kind") == "chart" or target.get("candle"):
            continue
        target["lesson_still"] = str((ROOT / image).resolve())


def plan(sid: str) -> list[dict]:
    raw = lesson_scripts.build(sid)
    lesson_scripts.attach_series(raw)
    number, title = parse_ident(raw[0])
    spoken = speech.spoken_number(int(number))
    brand = {
        "kind": "brand",
        "chapter": "Open",
        "vo": f"GridBot Builder. GridBot Blueprint. Lesson {spoken}. {title}.",
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
        "The prices are public historical daily closes, marked Example.",
        "No order is sent from this lesson.",
    ]
    risk_shots = []
    for index, line in enumerate(risk_lines):
        spoken = line
        if sid == "bp-01-introduction" and line.startswith("The prices are public historical daily closes"):
            spoken = line + " A close is the last price of the day."
        risk_shots.append({
            "kind": "stack",
            "chapter": "Risk",
            "vo": spoken,
            "caption": line,
            "items": risk_lines,
            "index": index,
            "chart": "",
            "series": [],
        })
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
        # clip_vo used to shorten any shot without a visual key. That cut the
        # ladder, the promise line and both map shots, and the still block then
        # spoke the map again. The written line is what plays. A shot that is
        # still over the old cap is logged, not trimmed.
        if not nxt.get("visual"):
            kept = nxt.get("vo") or ""
            shortened = clip_vo(kept, 4, 80)
            if shortened != kept:
                _log_clip(sid, nxt, kept, shortened, "kept")
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
        # BP-02 v2 speaks 24,930 and 30,331. The round-number swap would erase them.
        if shot.get("lesson_id") != "bp-02-what-you-need":
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
# Measured on BP-01: 0.294s per spoken word (394s for 1097 words).
# Kokoro af_heart speed 1.0 for every line. Moods no longer scale the pace.
SPEECH_RATE = 1.0
SENTENCE_GAP = 0.52
BEAT_GAP = 1.05
# A short card used to sit in silence for up to 3s. A chart may still hold
# while its line is revealing. Every other gap stays within about 1.2s.
LINE_GAP_CAP = 1.2
REVEAL_GAP_CAP = 3.0
# Sentence audio is concatenated. A crossfade was stitching the end of one
# take onto the start of the next, including inside a single thought.
JOIN_FADE = 0.0
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
    brand = "GridBot Builder"
    draw.text((MX, 68), brand, font=font(32), fill=WHITE)
    chapter = shot.get("heading") or shot.get("chapter") or ""
    if chapter == "Hook":
        chapter = "Opening"
    brand_w = int(font(32).getlength(brand))
    size = fit_size(chapter, 900, 40, 36)
    if shot.get("analogy") not in {"ladder", "fence"}:
        draw.text((MX + brand_w + 28, 72), chapter, font=font(size), fill=WHITE)
    y = 160
    draw.rectangle([MX, y, RIGHT, y + 4], fill=(20, 40, 58))
    span = (RIGHT - MX) * max(0.02, min(1.0, progress))
    draw.rectangle([MX, y, MX + span, y + 4], fill=CYAN)


def lower_third(draw: ImageDraw.ImageDraw, shot: dict) -> None:
    if shot.get("kind") in {"brand", "disclaimer", "outro"}:
        return
    # The burned-in caption sits at y=772, just under the card, so this
    # band starts below that cue.
    draw.rectangle([MX, 828, RIGHT, 832], fill=CYAN)
    term = shot.get("term") or ""
    defin = shot.get("definition") or ""
    t_size = fit_size(term, W - 2 * MX, 40, 36)
    draw.text((MX, 844), term, font=font(t_size), fill=CYAN)
    width = W - 2 * MX
    # The whole current beat. Shrink the type so a long line is not cut off.
    # Footer text starts at y=990.
    size = 36
    lines = wrap(defin, size, width, "reg")
    while size > 22 and 886 + len(lines) * (size + 8) > 978:
        size -= 2
        lines = wrap(defin, size, width, "reg")
    y = 886
    step = size + 8
    for line in lines:
        if y + size > 978:
            break
        draw.text((MX, y), line, font=font(size, "reg"), fill=WHITE)
        y += step


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
        if shot.get("lesson_id") == "bp-01-introduction":
            return "The top line and the bottom line, taken from the path."
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


def _example(draw: ImageDraw.ImageDraw, x: int = 1500, y: int = 196) -> None:
    face = font(36)
    label = "EXAMPLE"
    tw = int(face.getlength(label)) + 36
    # The 5% side margin starts at 96px. Keep the chip inside it.
    safe_left = int(W * 0.05) + 12
    safe_right = int(W * 0.95) - 12
    if x + tw > safe_right:
        x = safe_right - tw
    if x < safe_left:
        x = safe_left
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
    if shot.get("chapter") == "The whole window":
        worked_at = _word_at(shot, "worked")
        if worked_at is None:
            worked_at = dur * 0.62
        if local >= worked_at:
            paint_worked_check(base, shot, local, worked_at)
            return
    draw = ImageDraw.Draw(base)
    if box is None:
        box = (MX, 180, RIGHT, 690)
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
    if chapter == "The whole window":
        # Draw only as far as the voice has got. Rings come later, with "crossed".
        crossed_at = _word_at(shot, "crossed")
        path_end = crossed_at if crossed_at is not None else max(1.0, dur * 0.35)
        frac = min(1.0, local / max(0.4, path_end))
        upto = max(2, int(round(frac * (len(full) - 1))) + 1)
        growing = full[:upto]
        shown = growing
        _stroke(base, growing, (0, 212, 255, 90), 8)
        _stroke(base, growing, (0, 212, 255, 255), 3)
    elif chapter == "The levels":
        seven_at = _word_at(shot, "seven")
        path_end = seven_at if seven_at is not None else max(1.0, dur * 0.62)
        frac = min(1.0, local / max(0.4, path_end))
        upto = max(2, int(round(frac * (len(full) - 1))) + 1)
        growing = full[:upto]
        shown = growing
        _stroke(base, growing, (0, 212, 255, 90), 8)
        _stroke(base, growing, (0, 212, 255, 255), 3)
    elif chapter in {"Walk the summer", "Copy the path", "Where the price stayed"}:
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
    seven_at = _word_at(shot, "seven") if chapter == "The levels" else None
    show_seven = chapter != "The levels" or seven_at is None or local >= seven_at
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
        # Before "Seven lines", only the band and the one gap that the voice is measuring.
        if chapter == "The levels" and not show_seven and rounded not in {24930, 30331, 26730, 27630}:
            continue
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
            # Every BP-01 chart keeps the top and the bottom. The other rungs stay unlabelled
            # until the levels shot says "Seven lines".
            if chapter == "The levels" and show_seven:
                label = f"{rounded:,}"
            elif shot.get("lesson_id") == "bp-01-introduction" and rounded not in edges:
                label = ""
            else:
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
        elif label:
            draw.text((gutter_x, yy - 18), label, font=lf, fill=WHITE)
        if chapter == "The levels" and rounded == 26730:
            other = _map(0, n, 27630, lo_p, hi_p, plot)[1]
            bracket = plot[0] + 24
            draw.line([(bracket, yy), (bracket, other)], fill=CYAN, width=4)
            mid = (yy + other) / 2
            note = (
                "about $900 gap"
                if shot.get("lesson_id") == "bp-01-introduction"
                else "one gap = about 900"
            )
            face_gap = font(36 if shot.get("lesson_id") == "bp-01-introduction" else 28)
            gap_w = int(face_gap.getlength(note)) + 28
            draw.rounded_rectangle(
                [bracket + 10, mid - 24, bracket + 10 + gap_w, mid + 24],
                10, fill=TAG, outline=CYAN, width=3,
            )
            draw.text((bracket + 24, mid - 20), note, font=face_gap, fill=WHITE)

    if chapter == "The whole window":
        crossed_at = _word_at(shot, "crossed")
        if crossed_at is None:
            crossed_at = dur * 0.35
        if local >= crossed_at:
            marks = []
            for index in range(1, n):
                earlier, later = closes[index - 1], closes[index]
                if later == earlier:
                    continue
                for level in GRID_LEVELS:
                    crossed = (earlier < level <= later) or (later < level <= earlier)
                    if not crossed:
                        continue
                    share = (level - earlier) / (later - earlier)
                    x = full[index - 1][0] + (full[index][0] - full[index - 1][0]) * share
                    y = _map(0, n, level, lo_p, hi_p, plot)[1]
                    marks.append((x, y))
            for level in GRID_LEVELS:
                yy = _map(0, n, level, lo_p, hi_p, plot)[1]
                x = plot[0]
                while x < plot[2]:
                    draw.line([(x, yy), (min(x + 8, plot[2]), yy)], fill=MUTED, width=2)
                    x += 18
            # A day apart is only about 16px. The L2 re-cross (1–2 Sep) and the
            # October L4 cluster were reading as one ring. Push those apart, and
            # keep the 16 Oct rise inside the plot. The count stays 28.
            placed: list[tuple[float, float]] = []
            # Keep every ring inside the plot, including the first one, and
            # stack a same-day pair far enough apart that the outlines do not merge.
            for x, y in marks:
                x = min(max(x, plot[0] + 36), plot[2] - 48)
                shift = 0
                step = 44
                while any(abs(x - px) < 36 and abs(y + shift - py) < 40 for px, py in placed):
                    shift = step if shift == 0 else (-abs(shift) - step if shift > 0 else abs(shift) + step)
                    if abs(shift) > 200:
                        break
                y = min(max(y + shift, plot[1] + 28), plot[3] - 28)
                nudge = 0
                while any(abs(x + nudge - px) < 36 and abs(y - py) < 40 for px, py in placed):
                    nudge = 20 if nudge == 0 else (-abs(nudge) - 20 if nudge > 0 else abs(nudge) + 20)
                    if abs(nudge) > 80:
                        break
                x = min(max(x + nudge, plot[0] + 36), plot[2] - 48)
                placed.append((x, y))
            face_i = font(22)
            for index, (x, y) in enumerate(placed, start=1):
                draw.ellipse((x - 11, y - 11, x + 11, y + 11), outline=WHITE, width=3)
                draw.ellipse((x - 5, y - 5, x + 5, y + 5), fill=CYAN)
                label = str(index)
                draw.text((x + 14, y - 12), label, font=face_i, fill=WHITE)
            note = f"{len(marks)} crossings"
            face_n = font(36)
            tw = int(face_n.getlength(note)) + 28
            draw.rounded_rectangle([plot[0], plot[1] + 8, plot[0] + tw, plot[1] + 56], 10, fill=TAG, outline=CYAN, width=2)
            draw.text((plot[0] + 14, plot[1] + 12), note, font=face_n, fill=WHITE)

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
    hide_node_price = shot.get("lesson_id") == "bp-01-introduction"
    if not hide_node_price:
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
    secrets_line: str | None = None,
    buy_label: str = "BUY 27,630",
) -> None:
    """Lesson visual. path and orders use the real summer closes, not a sawtooth."""
    draw = ImageDraw.Draw(base)
    draw.rounded_rectangle(box, 24, fill=GLASS, outline=CYAN, width=2)
    x0, y0, x1, y1 = box
    if mode == "lines":
        rows = [
            "Notebook",
            "Range and levels",
            "The pair",
            "Paper or demo",
            secrets_line or "No secrets: no seed phrase, private key or API secret",
            "A written stop",
            "Keep the word Example on every practice figure",
        ]
        y = y0 + 24
        for row in rows:
            lines = wrap(row, 24, x1 - x0 - 100)[:3]
            _tick(draw, x0 + 36, y + 14)
            for line in lines:
                draw.text((x0 + 68, y), line, font=font(24), fill=WHITE)
                y += 28
            y += 10
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
        text = buy_label
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
    draw.text((MX, 150), "GridBot Builder", font=font(48), fill=WHITE)
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
    """A plain tick. Navy, cyan and white only."""
    draw.line([(x - 14, y), (x - 4, y + 12), (x + 16, y - 14)], fill=CYAN, width=4)


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
        draw.regular_polygon((x, y, 20), 8, outline=WHITE, width=3)
        draw.regular_polygon((x, y, 12), 8, outline=CYAN, width=3)
    else:
        draw.rounded_rectangle([x - 20, y - 16, x + 20, y + 16], 6, outline=CYAN, width=3)
        draw.text((x - 12, y - 12), "EX", font=font(22), fill=CYAN)


def paint_copy_band(base: Image.Image) -> None:
    """The page copies the band, not every day's price."""
    draw = ImageDraw.Draw(base)
    box = (MX, 200, RIGHT, 700)
    draw.rounded_rectangle(box, 22, fill=GLASS, outline=CYAN, width=2)
    draw.text((box[0] + 36, box[1] + 28), "Copy the band", font=font(48), fill=WHITE)
    rows = (
        "Top 30,331",
        "Bottom 24,930",
        "Six gaps of about 900",
    )
    y = box[1] + 140
    for row in rows:
        draw.text((box[0] + 36, y), row, font=font(40), fill=CYAN)
        y += 80
    _example(draw, box[0] + 36, y + 20)


def _center_card(draw: ImageDraw.ImageDraw, title: str, lines: list[str], example: bool = False) -> None:
    """One card in the middle of the frame, so a new line is a new picture."""
    box = (MX, 200, RIGHT, 680)
    draw.rounded_rectangle(box, 22, fill=GLASS, outline=CYAN, width=3)
    draw.text((box[0] + 36, box[1] + 28), title, font=font(40), fill=CYAN)
    y = box[1] + 110
    for line in lines:
        for wrapped in wrap(line, 42, box[2] - box[0] - 80)[:6]:
            if y > box[3] - 56:
                break
            draw.text((box[0] + 36, y), wrapped, font=font(36), fill=WHITE)
            y += 48
    if example:
        _example(draw, box[0] + 36, min(y + 16, box[3] - 64))


def _spoken(shot: dict, local: float, phrase: str) -> bool:
    at = _phrase_at(shot, phrase)
    return at is not None and local >= at


def _sentence_steps(draw: ImageDraw.ImageDraw, shot: dict, local: float) -> None:
    """Show one sentence at a time, so a long paragraph cannot sit still."""
    parts = [part.strip() for part in re.split(r"(?<=[.!?])\s+", shot.get("vo") or "") if part.strip()]
    if not parts:
        return
    current = 0
    for index, part in enumerate(parts):
        lead = " ".join(part.split()[:4])
        if _spoken(shot, local, lead) or (index == 0 and local >= 0):
            current = index
    text = parts[current]
    _center_card(draw, f"{current + 1} of {len(parts)}", [text], example="Example" in text or "EXAMPLE" in text)


def paint_board(base: Image.Image, shot: dict, local: float = 0) -> None:
    """A heading frame that shows the idea in words a beginner can read."""
    draw = ImageDraw.Draw(base)
    board = shot.get("board")
    if board == "seven-lines" and shot.get("lesson_id") == "bp-02-what-you-need":
        if _spoken(shot, local, "daily close"):
            _center_card(draw, "A daily close", ["The last price of the day.", "You are naming the public series."])
            return
        if _spoken(shot, local, "pretend money"):
            _center_card(draw, "A demo account", ["Uses pretend money."])
            return
        if _spoken(shot, local, "priced in"):
            _center_card(draw, "The pair", ["Bitcoin priced in US dollars."], example=True)
            return
        rows = [
            ("notebook", "1. A notebook."),
            ("three words", "2. Range, levels, and stop."),
            ("the pair", "3. The pair: bitcoin, public daily closes."),
            ("paper or", "4. Paper, or a demo."),
            ("no secrets", "5. No secrets on this page."),
            ("written stop", "6. The stop, written as a sentence."),
            ("example on", "7. The word Example on every figure."),
        ]
        shown = 1
        for index, (phrase, _row) in enumerate(rows):
            if index == 0 or _spoken(shot, local, phrase):
                shown = index + 1
        draw.text((MX + 80, 168), "Seven items", font=font(36), fill=WHITE)
        y = 214
        for _phrase, row in rows[:shown]:
            draw.rounded_rectangle([MX, y, RIGHT, y + 56], 12, fill=GLASS, outline=LINE, width=2)
            _tick(draw, 130, y + 28)
            draw.text((188, y + 10), row, font=font(30), fill=WHITE)
            y += 64
        return
    if board == "three-words" and shot.get("lesson_id") == "bp-02-what-you-need":
        if _spoken(shot, local, "missing a"):
            _center_card(draw, "All three words", ["If one word is missing,", "the page is missing a part."])
            return
        if _spoken(shot, local, "marked example"):
            _center_card(draw, "Marked Example", ["The figures are from lesson 1."], example=True)
            return
        cards = []
        if local >= 0:
            cards.append(("Range", "The top line and the bottom line."))
        if _spoken(shot, local, "levels are"):
            cards.append(("Levels", "Six gaps. About 900."))
        if _spoken(shot, local, "a stop is"):
            cards.append(("Stop", "Two daily closes outside."))
        y = 200
        for title, body in cards:
            draw.rounded_rectangle([MX, y, RIGHT, y + 140], 16, fill=GLASS, outline=CYAN, width=2)
            draw.text((MX + 36, y + 28), title, font=font(48), fill=CYAN)
            draw.text((MX + 280, y + 40), body, font=font(36), fill=WHITE)
            y += 156
        _example(draw, MX + 36, min(y + 8, 640))
        return
    if board == "no-secrets" and shot.get("lesson_id") == "bp-02-what-you-need":
        if _spoken(shot, local, "a form asks"):
            _center_card(draw, "Not this lesson", ["If a form asks for a secret,", "that form is not this lesson."])
            return
        if _spoken(shot, local, "no balance"):
            _center_card(draw, "No balance", ["A public close is not your account."], example=True)
            return
        if _spoken(shot, local, "never type"):
            _center_card(draw, "Never on the page", ["A seed phrase, a private key,", "or an API secret."])
            return
        if _spoken(shot, local, "private key"):
            _center_card(draw, "A private key", ["Or an API secret.", "A password that can move your money."])
            return
        _center_card(draw, "A seed phrase", ["The list of words that unlocks a wallet."])
        return
    if board == "say-the-page" and shot.get("lesson_id") == "bp-02-what-you-need":
        if _spoken(shot, local, "write example"):
            _center_card(draw, "Write Example", ["On your own notebook.", "A practice sketch is not a live plan."], example=True)
            return
        if _spoken(shot, local, "a secret is"):
            _center_card(draw, "No secrets", ["A seed phrase, a private key,", "or an API secret."])
            return
        if _spoken(shot, local, "name the pair"):
            _center_card(
                draw,
                "Name these",
                ["Pair: bitcoin, public daily closes.", "Band: 24,930 to 30,331.", "Gaps: six, about 900.", "Stop: two daily closes outside."],
                example=True,
            )
            return
        _center_card(draw, "Say the page", ["Once, in your own words.", "Do not read the chart again."])
        return
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
        draw.text((MX + 80, 186), "Seven items", font=font(40), fill=WHITE)
        y = 240
        for row in rows:
            draw.rounded_rectangle([MX, y, RIGHT, y + 68], 12, fill=GLASS, outline=LINE, width=2)
            _tick(draw, 130, y + 34)
            draw.text((188, y + 16), row, font=font(32), fill=WHITE)
            draw.ellipse([1760, y + 16, 1796, y + 52], outline=CYAN, width=3)
            draw.line([(1768, y + 34), (1778, y + 44), (1790, y + 24)], fill=CYAN, width=3)
            y += 76
        return
    if board == "no-secrets":
        draw.text((MX, 176), "Never on the page", font=font(32), fill=WHITE)
        draw.text((1040, 176), "Allowed on the page", font=font(32), fill=CYAN)
        banned = ["Seed phrase", "Private key", "API secret", "Account balance"]
        allowed = ["Public daily close", "The word Example", "A figure marked Example"]
        y = 230
        for text in banned:
            draw.rounded_rectangle([MX, y, 980, y + 100], 14, fill=GLASS, outline=WHITE, width=2)
            draw.line([(MX + 28, y + 28), (MX + 56, y + 56)], fill=WHITE, width=4)
            draw.line([(MX + 56, y + 28), (MX + 28, y + 56)], fill=WHITE, width=4)
            draw.text((MX + 76, y + 30), text, font=font(36), fill=WHITE)
            y += 112
        y = 230
        for text in allowed:
            draw.rounded_rectangle([1040, y, RIGHT, y + 100], 14, fill=GLASS, outline=CYAN, width=2)
            draw.line([(1070, y + 52), (1082, y + 64), (1102, y + 36)], fill=CYAN, width=4)
            draw.text((1120, y + 30), text, font=font(32), fill=WHITE)
            y += 112
        return
    if board == "say-the-page":
        draw.text((MX, 180), "Say the page", font=font(40), fill=WHITE)
        rows = (
            "Pair: bitcoin, public daily closes.",
            "Band: 24,930 to 30,331.",
            "Gaps: six, about 900.",
            "Stop: two daily closes outside, then stop the bot.",
            "No secrets on this page.",
        )
        y = 260
        for row in rows:
            draw.rounded_rectangle([MX, y, RIGHT, y + 88], 14, fill=GLASS, outline=CYAN, width=2)
            draw.text((MX + 28, y + 24), row, font=font(32), fill=WHITE)
            y += 100
        _example(draw, MX, y + 8)
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


def _word_at(shot: dict, *needles: str) -> float | None:
    """Start time of the first spoken word that matches, in this shot."""
    wanted = {needle.lower() for needle in needles}
    for text, start, _end in shot.get("word_times") or []:
        token = str(text).lower().strip(".,?!")
        if token in wanted:
            return float(start)
    return None


def _phrase_at(shot: dict, phrase: str) -> float | None:
    """Start time of the first spoken phrase in this shot."""
    words = shot.get("word_times") or []
    def _clean(token: str) -> str:
        return token.lower().strip(".,;:!?\"'")

    tokens = [_clean(part) for part in phrase.split() if _clean(part)]
    if not words or not tokens:
        return None
    norm = [_clean(str(text)) for text, _start, _end in words]
    for index in range(len(norm) - len(tokens) + 1):
        if norm[index:index + len(tokens)] == tokens:
            return float(words[index][1])
    return None


def _draw_named_rows(draw: ImageDraw.ImageDraw, rows: list[tuple[str, str]]) -> None:
    y = 210
    left = MX + 28
    for number, name in rows:
        draw.rounded_rectangle([left, y, left + 72, y + 64], 12, fill=TAG, outline=CYAN, width=2)
        num_x = left + 22 if len(str(number)) == 1 else left + 8
        draw.text((num_x, y + 12), str(number), font=font(36), fill=CYAN)
        draw.text((left + 96, y + 10), name, font=font(40), fill=CYAN)
        y += 88


def paint_worked_check(base: Image.Image, shot: dict, local: float, worked_at: float) -> None:
    """The card that replaces the window chart when 'Worked check' is spoken."""
    draw = ImageDraw.Draw(base)
    box = (MX, 200, RIGHT, 700)
    draw.rounded_rectangle(box, 22, fill=GLASS, outline=CYAN, width=2)
    _example(draw, box[0] + 36, box[1] + 28)
    draw.text((box[0] + 36, box[1] + 88), "Worked check", font=font(48), fill=WHITE)
    draw.text((box[0] + 36, box[1] + 160), "19 July 2023 to 16 October 2023", font=font(36), fill=CYAN)
    rows = [
        (_word_at(shot, "low"), "The low is the bottom line."),
        (_word_at(shot, "high"), "The high is the top line."),
        (_word_at(shot, "nothing"), "Nothing on this card is an order."),
    ]
    y = box[1] + 250
    for at, line in rows:
        if at is None or local >= at:
            draw.text((box[0] + 36, y), line, font=font(36), fill=WHITE)
        y += 72


def paint_crossings(base: Image.Image, shot: dict, local: float) -> None:
    """One crossing first, then a finished pair when that word is spoken."""
    draw = ImageDraw.Draw(base)
    box = (MX, 200, RIGHT, 700)
    draw.rounded_rectangle(box, 22, fill=GLASS, outline=CYAN, width=2)
    draw.text((box[0] + 36, box[1] + 24), "A crossing is not a finished pair", font=font(36), fill=WHITE)
    pair_at = _word_at(shot, "pair")
    bottom_at = _word_at(shot, "bottom")
    show_pair = pair_at is None or local >= pair_at
    show_bottom = bottom_at is not None and local >= bottom_at

    def panel(x0: int, title: str, paired: bool) -> None:
        draw.text((x0, box[1] + 100), title, font=font(32), fill=CYAN)
        left, right = x0, x0 + 640
        top, mid, bot = box[1] + 190, box[1] + 340, box[1] + 490
        if paired:
            top, bot = box[1] + 170, box[1] + 400
            draw.line([(left, top), (right, top)], fill=WHITE, width=3)
            draw.line([(left, bot), (right, bot)], fill=CYAN, width=4)
            path = [(left + 40, top - 16), (left + 200, bot + 18), (left + 420, top - 16)]
            draw.line(path, fill=CYAN, width=4)
            for px, py in ((left + 160, bot), (left + 300, top)):
                draw.ellipse((px - 10, py - 10, px + 10, py + 10), outline=WHITE, width=3)
                draw.ellipse((px - 5, py - 5, px + 5, py + 5), fill=CYAN)
            caption = "Still holding coin" if show_bottom else "Buy, then the later sell"
            draw.text((left, bot + 28), caption, font=font(28), fill=WHITE)
        else:
            draw.line([(left, mid), (right, mid)], fill=WHITE, width=4)
            draw.line([(left + 80, mid + 80), (left + 520, mid - 80)], fill=CYAN, width=4)
            px, py = left + 300, mid
            draw.ellipse((px - 12, py - 12, px + 12, py + 12), outline=WHITE, width=3)
            draw.ellipse((px - 6, py - 6, px + 6, py + 6), fill=CYAN)
            draw.text((left, bot + 28), "The close moves across one line", font=font(28), fill=WHITE)

    panel(box[0] + 48, "One crossing", False)
    if show_pair:
        # A filled panel, not a thin line, so the second stage reads as a new picture.
        draw.rounded_rectangle([box[0] + 860, box[1] + 88, box[2] - 36, box[3] - 36], 18, fill=TAG, outline=CYAN, width=3)
        panel(box[0] + 900, "A finished pair", True)


def paint_idea(base: Image.Image, shot: dict, local: float) -> None:
    """Reveal the band, then the buys, then the sells, so the card does not sit still."""
    draw = ImageDraw.Draw(base)
    box = (MX, 200, RIGHT, 700)
    draw.rounded_rectangle(box, 22, fill=GLASS, outline=CYAN, width=2)
    draw.text((box[0] + 36, box[1] + 12), "A grid bot places the orders", font=font(32), fill=WHITE)
    buy_at = _word_at(shot, "buy", "buys")
    sell_at = _word_at(shot, "sell", "sells")
    band_at = _word_at(shot, "band")
    cash_at = _word_at(shot, "cash")

    def due(at: float | None) -> bool:
        return at is not None and local >= at

    # Each stage fills a block inside the card, and the last one is up by 15s.
    show_band = due(band_at) or local >= 15
    show_buy = due(buy_at) or local >= 15
    show_sell = due(sell_at) or local >= 15
    show_cash = due(cash_at) or local >= 15
    left, right = box[0] + 80, box[2] - 80
    mid = (left + right) // 2
    if show_band:
        draw.rounded_rectangle([left, 268, right, 316], 8, fill=TAG, outline=WHITE, width=3)
        draw.text((left + 16, 276), "Top of the band", font=font(28), fill=WHITE)
        draw.rounded_rectangle([left, 496, right, 548], 8, fill=TAG, outline=WHITE, width=3)
        draw.text((left + 16, 504), "Bottom of the band", font=font(28), fill=WHITE)
    if show_sell:
        draw.rounded_rectangle([mid + 12, 332, right, 400], 8, fill=TAG, outline=WHITE, width=3)
        draw.text((mid + 28, 350), "Sells above", font=font(32), fill=WHITE)
    if show_buy:
        draw.rounded_rectangle([left, 406, mid - 12, 480], 8, fill=(0, 48, 64), outline=CYAN, width=3)
        draw.text((left + 16, 428), "Buys below", font=font(32), fill=CYAN)
    if show_cash:
        draw.rounded_rectangle([left, 564, right, 640], 8, fill=(0, 40, 56), outline=CYAN, width=3)
        draw.text((left + 16, 584), "Part cash and part coin", font=font(32), fill=CYAN)


def _v2_index(shot: dict, local: float) -> int:
    cards = list(shot.get("v2_cards") or [])
    if not cards:
        return 0
    forced = shot.get("v2_show")
    if forced is not None:
        return max(0, min(int(forced), len(cards) - 1))
    shown = 0
    for index, card in enumerate(cards):
        cue = (card.get("cue") or "").strip()
        if index == 0 or (cue and _spoken(shot, local, cue)):
            shown = index
    return shown


def _paint_fitted_card(base: Image.Image, title: str, lines: list[str], example: bool = False) -> None:
    """Every word of the sentence, inside the area above the burned caption."""
    draw = ImageDraw.Draw(base)
    box = (MX, 176, RIGHT, 708)
    draw.rounded_rectangle(box, 22, fill=GLASS, outline=CYAN, width=3)
    width = box[2] - box[0] - 72
    body = [line for line in lines if line]
    chosen = None
    for size in range(40, 25, -2):
        title_size = min(size + 6, 44)
        title_lines = wrap(title, title_size, width) if title else []
        wrapped: list[str] = []
        for sentence in body:
            wrapped.extend(wrap(sentence, size, width) or [sentence])
        block = 28 + len(title_lines) * (title_size + 8) + 12 + len(wrapped) * (size + 12)
        if example:
            block += 64
        if block <= box[3] - box[1] - 36:
            chosen = (title_size, size, title_lines, wrapped)
            break
    if chosen is None:
        size = 26
        title_size = 32
        title_lines = wrap(title, title_size, width) if title else []
        wrapped = []
        for sentence in body:
            wrapped.extend(wrap(sentence, size, width) or [sentence])
        chosen = (title_size, size, title_lines, wrapped)
    title_size, size, title_lines, wrapped = chosen
    y = box[1] + 28
    for line in title_lines:
        draw.text((box[0] + 36, y), line, font=font(title_size), fill=CYAN)
        y += title_size + 8
    if title_lines:
        y += 8
    for line in wrapped:
        draw.text((box[0] + 36, y), line, font=font(size), fill=WHITE)
        y += size + 12
    if example:
        _example(draw, box[0] + 36, min(y + 8, box[3] - 64))


def _paint_worked_rows(base: Image.Image) -> None:
    """Four rows, the stop row included, and an EXAMPLE chip on every figure."""
    draw = ImageDraw.Draw(base)
    rows = [
        ("Pair: bitcoin, public daily closes.", False),
        ("Band: 24,930 to 30,331.", True),
        ("Gaps: six, about 900.", True),
        ("Stop sentence: written. Example: written.", True),
    ]
    y = 188
    for text, marked in rows:
        draw.rounded_rectangle([MX, y, RIGHT, y + 112], 16, fill=GLASS, outline=CYAN, width=2)
        draw.text((MX + 28, y + 34), text, font=font(36), fill=WHITE)
        if marked:
            _example(draw, RIGHT - 220, y + 32)
        y += 124


def _paint_three_words_classic(base: Image.Image) -> None:
    """The passed three-words board: 24,930 to 30,331, and Leaves 30,331."""
    draw = ImageDraw.Draw(base)
    cards = [
        ("Range", "24,930 to 30,331", "band"),
        ("Levels", "Six gaps, about 900.", "ladder"),
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
        else:
            _row_icon(draw, pic + 90, y + 75, kind)
        y += 170
    pill_w = int(font(36).getlength("EXAMPLE")) + 36
    _example(draw, RIGHT - 24 - pill_w, 78)


def paint_v2_cards(base: Image.Image, shot: dict, local: float) -> None:
    cards = list(shot.get("v2_cards") or [])
    card = cards[_v2_index(shot, local)]
    # The lower third is this card, not the first line of the chapter.
    if card.get("classic"):
        beat = "Range: 24,930 to 30,331. Levels: six gaps, about 900. Stop: Leaves 30,331."
    elif card.get("rows"):
        beat = "Pair, band, gaps, and a written stop. Every figure marked Example."
    else:
        beat = " ".join(str(line) for line in (card.get("lines") or []) if line)
    shot["term"] = str(card.get("title") or shot.get("chapter") or "")
    shot["definition"] = beat
    if card.get("classic"):
        _paint_three_words_classic(base)
        return
    if card.get("rows"):
        _paint_worked_rows(base)
        return
    _paint_fitted_card(
        base,
        str(card.get("title") or shot.get("chapter") or ""),
        list(card.get("lines") or []),
        example=bool(card.get("example")),
    )


def paint_stack(base: Image.Image, shot: dict, local: float) -> None:
    draw = ImageDraw.Draw(base)
    if shot.get("v2_cards") and shot.get("lesson_id") == "bp-02-what-you-need":
        paint_v2_cards(base, shot, local)
        return
    vo = shot.get("vo") or ""
    if shot.get("lesson_id") == "bp-02-what-you-need" and (
        vo.startswith("A journal is the page you will open again")
        or vo.startswith("Australian exchanges register with AUSTRAC")
    ):
        _sentence_steps(draw, shot, local)
        return
    named = list(shot.get("screen_lines") or [])
    if named and (shot.get("chapter") or "") == "The map" and str(named[0][0]) == "1":
        later = [
            ("7", "Paper"),
            ("8", "Monitoring"),
            ("9", "Mistakes"),
            ("10", "Scaling up"),
            ("11", "Your complete plan"),
        ]
        # "Steps seven to eleven" is spoken just before the paper test.
        # The 7–11 card comes in on that line, then each name as it is spoken.
        seven_at = _word_at(shot, "seven")
        if seven_at is not None and local >= seven_at:
            later_cues = (
                ("paper",),
                ("weekly",),
                ("mistakes",),
                ("scaling",),
                ("liquidation", "complete"),
            )
            shown = 0
            for needles in later_cues:
                start = _word_at(shot, *needles)
                if start is not None and local >= start:
                    shown += 1
            if shown == 0:
                shown = 1
            shown = min(len(later), shown)
            _draw_named_rows(draw, later[:shown])
            return
        cues = (
            ("steps", "introduction", "step"),
            ("need",),
            ("exactly", "order"),
            ("regimes",),
            ("spacing", "choosing"),
            ("entry",),
        )
        shown = 0
        for needles in cues:
            start = _word_at(shot, *needles)
            if start is not None and local >= start:
                shown += 1
        if shown == 0 and local >= 0.2:
            shown = 1
        _draw_named_rows(draw, named[:shown])
        return
    if named:
        _draw_named_rows(draw, named)
        return
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
    if (shot.get("chapter") or "") == "Your turn" and index == 2 and local >= 12:
        top = 210 + card_h + 28
        draw.rounded_rectangle([MX, top, RIGHT, top + 110], 18, fill=GLASS, outline=WHITE, width=3)
        draw.text((MX + 36, top + 32), "Paper or demo. No real order.", font=font(40), fill=WHITE)


def paint_pair(base: Image.Image, shot: dict, local: float) -> None:
    """One marked example: buy lower, sell higher, and the fees come out of the gap."""
    draw = ImageDraw.Draw(base)
    spans = list(shot.get("sentence_spans") or [])
    shown = 4
    if spans:
        shown = 1
        for index, (start, _end) in enumerate(spans[:4]):
            if local >= start:
                shown = index + 1
    box = (MX, 190, MX + 860, 740)
    draw.rounded_rectangle(box, 20, fill=GLASS, outline=CYAN, width=3)
    _example(draw, box[0] + 28, box[1] + 24)
    draw.text((box[0] + 28, box[1] + 80), "One coin. One buy. One sell.", font=font(32), fill=WHITE)
    sell_y, buy_y = 400, 600
    x0, x1 = box[0] + 72, box[2] - 96
    if shown >= 1:
        draw.line([(x0, buy_y), (x1, buy_y)], fill=CYAN, width=6)
        draw.text((x0, buy_y + 16), "Buy  27,630", font=font(40), fill=CYAN)
    if shown >= 2:
        draw.line([(x0, sell_y), (x1, sell_y)], fill=MINT, width=6)
        draw.text((x0, sell_y - 52), "Sell  28,531", font=font(40), fill=MINT)
        draw.line([(x1 + 16, sell_y), (x1 + 16, buy_y)], fill=WHITE, width=3)
        draw.text((x0, 488), "Gap about 900", font=font(36), fill=WHITE)
    side = (box[2] + 24, 190, RIGHT, 740)
    draw.rounded_rectangle(side, 20, fill=GLASS, outline=CYAN, width=3)
    draw.text((side[0] + 32, side[1] + 28), "EXAMPLE fees", font=font(36), fill=CYAN)
    if shown >= 3:
        draw.text((side[0] + 32, side[1] + 110), "Buy fee  10", font=font(44), fill=WHITE)
        draw.text((side[0] + 32, side[1] + 180), "Sell fee  10", font=font(44), fill=WHITE)
        draw.text((side[0] + 32, side[1] + 260), "Together  20", font=font(44), fill=WHITE)
    if shown >= 4:
        draw.text((side[0] + 32, side[1] + 360), "Not money you made.", font=font(36), fill=AMBER)
        draw.text((side[0] + 32, side[1] + 420), "The gap is larger", font=font(36), fill=WHITE)
        draw.text((side[0] + 32, side[1] + 468), "than these fees.", font=font(36), fill=WHITE)


def paint_worked(base: Image.Image, shot: dict, local: float) -> None:
    draw = ImageDraw.Draw(base)
    rows = shot.get("items") or []
    if not rows:
        return
    spans = list(shot.get("sentence_spans") or [])
    shown = 1
    if spans:
        shown = 1
        for index, (start, _end) in enumerate(spans[: len(rows)]):
            if local >= start:
                shown = index + 1
    else:
        dur = float(shot.get("duration") or max(8.0, len(rows) * 3.2))
        step = dur / max(1, len(rows))
        shown = min(len(rows), 1 + int(local / step)) if step else len(rows)
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
        # Seven lines on the left, six gaps on the right. No amber stop sign.
        left = (MX, 200, MX + 900, 760)
        right = (MX + 940, 200, RIGHT, 760)
        draw.rounded_rectangle(left, 20, fill=GLASS, outline=CYAN, width=2)
        draw.rounded_rectangle(right, 20, fill=GLASS, outline=CYAN, width=2)
        draw.text((left[0] + 28, left[1] + 24), "Seven lines", font=font(36), fill=WHITE)
        items = (
            "1 Notebook",
            "2 Range, levels, stop",
            "3 The pair",
            "4 Paper or a demo",
            "5 No secrets",
            "6 A written stop",
            "7 Example on every figure",
        )
        y = left[1] + 90
        for item in items:
            draw.text((left[0] + 36, y), item, font=font(32), fill=CYAN)
            y += 72
        draw.text((right[0] + 28, right[1] + 24), "Six gaps", font=font(36), fill=WHITE)
        draw.text((right[0] + 28, right[1] + 120), "About 900 dollars", font=font(40), fill=WHITE)
        draw.text((right[0] + 28, right[1] + 200), "Top 30,331", font=font(36), fill=CYAN)
        draw.text((right[0] + 28, right[1] + 260), "Bottom 24,930", font=font(36), fill=CYAN)
        _example(draw, right[0] + 28, right[1] + 360)
        return
    chart_box = (origin[0] + pw + 24, 180, RIGHT, 690)
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
            note = "Not to scale: the real path is beside it"
            face = font(40)
            tw = int(face.getlength(note)) + 36
            nx, ny = origin[0], origin[1] + ph + 8
            draw.rounded_rectangle([nx, ny, nx + tw, ny + 56], 12, fill=TAG, outline=CYAN, width=3)
            draw.text((nx + 18, ny + 8), note, font=face, fill=WHITE)
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
    if shot.get("lesson_id") == "bp-02-what-you-need":
        paste(base, scaled(wordmark(), 78), (MX, 56))
    else:
        draw.text((MX, 72), "GridBot Builder", font=font(40), fill=WHITE)
    draw.text((MX, 220), "NEXT", font=font(28), fill=CYAN)
    draw.text((MX, 268), lesson_label, font=font(40), fill=CYAN)
    y = 340
    for line in wrap(title, 56, 900)[:3]:
        draw.text((MX, y), line, font=font(56), fill=WHITE)
        y += 68
    number = int(shot.get("lesson_no") or 1) + 1
    mode = {2: "lines", 3: "orders", 4: "regimes"}.get(number, "path")
    # The orders chip at the plot's left edge covers the July drop.
    secrets_line = None
    if shot.get("lesson_id") == "bp-01-introduction" and mode == "lines":
        secrets_line = (
            "No secrets: no seed phrase, private key or API secret, "
            "the secret words or keys that unlock a wallet or account"
        )
    hero_box = (1120, 150, 1760, 500) if shot.get("lesson_id") == "bp-01-introduction" else (1120, 180, 1760, 640)
    _hero(
        base, hero_box, mode,
        chip_dx=-40 if mode == "orders" else 0,
        secrets_line=secrets_line,
        buy_label="Example buy level 27,630" if shot.get("lesson_id") == "bp-02-what-you-need" else "BUY 27,630",
    )
    place_mascot(base, shot, (96, 420, 320, 540) if shot.get("lesson_id") == "bp-01-introduction" else (96, 430, 360, 640))
    if shot.get("lesson_id") == "bp-01-introduction":
        # Above the burned caption at y=764, and clear of the checklist above it.
        card = (MX, 548, RIGHT, 728)
        draw.rounded_rectangle(card, 16, fill=GLASS, outline=CYAN, width=2)
        y = card[1] + 14
        for line in DISCLAIMER_LINES:
            for wrapped in wrap(line, 32, card[2] - card[0] - 48, "reg")[:2]:
                draw.text((card[0] + 24, y), wrapped, font=font(32, "reg"), fill=WHITE)
                y += 38
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
    foot = font(28, "reg")
    # Place from the ink bottom, not the em box, so the margin stays at least 45px.
    bottom = foot.getbbox(FOOT)[3]
    draw.text((48, 720 - 1 - 45 - bottom), FOOT, font=foot, fill=MUTED)
    dest.parent.mkdir(parents=True, exist_ok=True)
    image.save(dest)
    return dest


def _big_still_tags(
    draw: ImageDraw.ImageDraw,
    x: int,
    y: int,
    view_w: int,
    view_h: int,
    tags: tuple[tuple[float, float, str], ...],
    pad_fill: tuple[int, int, int] = NAVY,
) -> None:
    """Cover a small baked tag with a readable one. The still file is not edited."""
    face = font(40)
    for fx, fy, text in tags:
        tw = int(face.getlength(text)) + 36
        th = 56
        tx = x + int(view_w * fx)
        ty = y + int(view_h * fy)
        draw.rounded_rectangle([tx - 6, ty - 8, tx + tw + 6, ty + th + 8], 12, fill=pad_fill)
        draw.rounded_rectangle([tx, ty, tx + tw, ty + th], 12, fill=TAG, outline=CYAN, width=3)
        draw.text((tx + 18, ty + 8), text, font=face, fill=WHITE)


def paint_leave(base: Image.Image, shot: dict, local: float) -> None:
    """The climb leaves the band holding cash. The fall leaves it holding coin."""
    draw = ImageDraw.Draw(base)
    box = (MX, 190, 1280, 680)
    draw.rounded_rectangle(box, 22, fill=GLASS, outline=CYAN, width=3)
    sentences = _lesson_sentences(shot.get("vo") or "")
    spans = list(shot.get("sentence_spans") or [])

    def progress(word: str) -> float | None:
        for text, span in zip(sentences, spans):
            if word in text.lower():
                start, end = span
                if local < start:
                    return 0.0
                if local >= end:
                    return 1.0
                return (local - start) / max(0.05, end - start)
        return None

    climb = progress("climbs")
    fall = progress("falls")
    if climb is None:
        climb = 1.0 if local > 0.55 else 0.0
    if fall is None:
        fall = 1.0 if local > 0.8 else 0.0
    if fall > 0:
        climb = 0.0
    sells = (300, 350, 400)
    buys = (470, 520, 570)
    mid = 435
    escape_top = 250
    escape_bot = 620
    if fall > 0:
        # A second picture: price starts in the middle, then leaves below the buys.
        price_y = mid + (escape_bot - mid) * fall
    elif climb > 0:
        price_y = mid + (escape_top - mid) * climb
    else:
        price_y = mid

    def said(word: str) -> float:
        for text, start, _end in shot.get("word_times") or []:
            token = str(text).lower().strip(".,;:!?")
            if token == word or token.startswith(word):
                return float(start)
        return float("inf")

    cash_at = said("cash")
    coin_at = said("coin")
    cash_on = cash_at <= local < coin_at
    coin_on = local >= coin_at

    face_mark = font(36)
    face_label = font(30)

    def coin_icon(cx: int, cy: int) -> None:
        draw.ellipse([cx - 30, cy - 30, cx + 30, cy + 30], fill=NAVY, outline=CYAN, width=4)
        tw = int(face_mark.getlength("C"))
        draw.text((cx - tw // 2, cy - 22), "C", font=face_mark, fill=CYAN)

    def note_icon(cx: int, cy: int) -> None:
        draw.rounded_rectangle([cx - 36, cy - 22, cx + 36, cy + 22], 6, fill=NAVY, outline=MINT, width=4)
        tw = int(face_mark.getlength("$"))
        draw.text((cx - tw // 2, cy - 22), "$", font=face_mark, fill=MINT)

    labels = (
        ("Sell orders", sells[1], MINT),
        ("Start price", mid, WHITE),
        ("Buy orders", buys[1], BLUE),
    )
    label_w = max(int(face_label.getlength(text)) for text, _yy, _color in labels)
    label_x = box[0] + 24
    line_x0 = label_x + label_w + 18
    icon_x = box[2] - 64
    line_x1 = icon_x - 36 - 16
    for text, yy, color in labels:
        draw.text((label_x, yy - 18), text, font=face_label, fill=color)
    for yy in sells:
        crossed = climb > 0 and price_y <= yy
        color = MINT if crossed else MUTED
        draw.line([(line_x0, yy), (line_x1, yy)], fill=color, width=8)
        if crossed:
            note_icon(icon_x, yy)
        else:
            coin_icon(icon_x, yy)
    draw.line([(line_x0, mid), (line_x1, mid)], fill=WHITE, width=3)
    for yy in buys:
        crossed = fall > 0 and price_y >= yy
        color = BLUE if crossed else MUTED
        draw.line([(line_x0, yy), (line_x1, yy)], fill=color, width=8)
        if crossed:
            coin_icon(icon_x, yy)
        else:
            note_icon(icon_x, yy)
    left_out = fall == 0 and price_y < sells[0]
    right_out = fall > 0 and price_y > buys[-1]
    face_fail = font(28)
    if left_out:
        draw.text((line_x0, 210), "all cash, nothing left to sell", font=face_fail, fill=WHITE)
    if right_out:
        # Keep this above the burned caption, which starts at y=764.
        draw.text((line_x0, 640), "all coin, nothing left to buy", font=face_fail, fill=WHITE)
    dot_x = (line_x0 + line_x1) // 2
    price_y = min(max(price_y, 240), 630)
    draw.ellipse([dot_x - 14, price_y - 14, dot_x + 14, price_y + 14], fill=CYAN)
    side = (1360, 200, RIGHT, 680)
    draw.rounded_rectangle(side, 22, fill=GLASS, outline=CYAN, width=3)
    draw.text((side[0] + 36, side[1] + 28), "What you hold", font=font(36), fill=CYAN)
    cash_box = [side[0] + 36, side[1] + 110, side[2] - 36, side[1] + 200]
    coin_box = [side[0] + 36, side[1] + 230, side[2] - 36, side[1] + 320]
    draw.rounded_rectangle(
        cash_box, 14,
        fill=(16, 48, 40) if cash_on else GLASS,
        outline=MINT,
        width=6 if cash_on else 3,
    )
    draw.text((cash_box[0] + 24, cash_box[1] + 22), "Cash", font=font(48), fill=MINT)
    draw.rounded_rectangle(
        coin_box, 14,
        fill=(16, 32, 64) if coin_on else GLASS,
        outline=BLUE,
        width=6 if coin_on else 3,
    )
    draw.text((coin_box[0] + 24, coin_box[1] + 22), "Coin", font=font(48), fill=BLUE)
    draw.text((side[0] + 36, side[1] + 370), "$ = cash on that line", font=font(28), fill=MINT)
    draw.text((side[0] + 36, side[1] + 412), "C = coin on that line", font=font(28), fill=CYAN)
    draw.text((side[0] + 36, side[1] + 454), "Bright line = filled", font=font(28), fill=WHITE)


def paint_lesson_still(base: Image.Image, shot: dict, local: float, dur: float) -> None:
    """Fit a 1536x1024 still in the stage. A short pan is the only move. No upscale."""
    src = load_picture(Path(shot["lesson_still"])).convert("RGB")
    box = (MX, 156, RIGHT, 700)
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
    still = str(shot.get("lesson_still") or "").replace("\\", "/")
    if still.endswith("bp-01-introduction/001.png"):
        # The still says GOES. The voice says moves. Cover only that word.
        d = ImageDraw.Draw(base)
        gx = x + int(525 * zoom) - pan
        gy = y + int(88 * zoom)
        gw, gh = int(200 * zoom), int(62 * zoom)
        d.rectangle([gx - 6, gy - 4, gx + gw, gy + gh], fill=NAVY)
        d.text((gx, gy), "MOVES", font=font(max(28, int(48 * zoom))), fill=WHITE)
        if local >= 18:
            # The still would otherwise sit for the whole hook. MOVES stays at the top.
            card = (MX + 48, 500, RIGHT - 48, 700)
            d.rounded_rectangle(card, 16, fill=NAVY, outline=CYAN, width=3)
            d.text((card[0] + 28, card[1] + 20), "Bouncing inside", font=font(32), fill=CYAN)
            d.line([(card[0] + 40, card[1] + 120), (card[0] + 140, card[1] + 70),
                    (card[0] + 240, card[1] + 120), (card[0] + 340, card[1] + 70)], fill=CYAN, width=4)
            d.text((card[0] + 620, card[1] + 20), "One way, then it stays", font=font(32), fill=WHITE)
            d.line([(card[0] + 640, card[1] + 130), (card[0] + 980, card[1] + 70)], fill=WHITE, width=4)
        if local >= 34:
            # This band is inside the measured picture, so the second hold stays under 20s.
            d.rounded_rectangle([MX + 70, 508, RIGHT - 70, 575], 12, fill=CYAN)
            d.text((MX + 96, 522), "Nothing left to do", font=font(32), fill=NAVY)
    if still.endswith("bp-01-introduction/009.png") and local >= 14:
        d = ImageDraw.Draw(base)
        card = (MX + 80, 520, RIGHT - 80, 680)
        d.rounded_rectangle(card, 16, fill=NAVY, outline=WHITE, width=3)
        d.text((card[0] + 28, card[1] + 48), "Paper or demo. No real order.", font=font(40), fill=WHITE)
    if still.endswith("bp-01-introduction/007.png"):
        d = ImageDraw.Draw(base)
        samples = []
        for fy in (0.22, 0.40, 0.72):
            for fx in (0.62, 0.78):
                samples.append(crop.getpixel((min(view_w - 1, int(view_w * fx)), min(view_h - 1, int(view_h * fy))))[:3])
        dark = [pixel for pixel in samples if pixel[1] < 80 and pixel[2] < 120]
        card = dark[len(dark) // 2] if dark else samples[0]
        tags = (
            (0.09, 0.30, "Sell orders above"),
            (0.09, 0.485, "Price now"),
            (0.09, 0.64, "Buy orders below"),
        )
        _big_still_tags(d, x, y, view_w, view_h, tags, pad_fill=card)
        # The baked Price now tag is wider than the new one. Cover it, then redraw.
        d.rectangle(
            [x + int(view_w * 0.09), y + int(view_h * 0.47), x + int(view_w * 0.44), y + int(view_h * 0.60)],
            fill=card,
        )
        _big_still_tags(d, x, y, view_w, view_h, ((0.09, 0.485, "Price now"),), pad_fill=card)
        cy = y + int(view_h * 0.537)
        d.line(
            [(x + int(view_w * 0.09) + int(font(40).getlength("Price now")) + 36, cy), (x + int(view_w * 0.455), cy)],
            fill=CYAN,
            width=3,
        )
    if still.endswith("bp-01-introduction/003.png"):
        d = ImageDraw.Draw(base)
        d.rounded_rectangle(
            [x + int(view_w * 0.28), y + int(view_h * 0.20), x + int(view_w * 0.72), y + int(view_h * 0.36)],
            12, fill=NAVY, outline=CYAN, width=2,
        )
        d.text((x + int(view_w * 0.30), y + int(view_h * 0.24)), "Sell orders above", font=font(32), fill=WHITE)
        d.rounded_rectangle(
            [x + int(view_w * 0.08), y + int(view_h * 0.52), x + int(view_w * 0.48), y + int(view_h * 0.68)],
            12, fill=NAVY, outline=CYAN, width=2,
        )
        d.text((x + int(view_w * 0.10), y + int(view_h * 0.56)), "Buy orders below", font=font(32), fill=CYAN)
    if still.endswith("bp-01-introduction/012.png"):
        d = ImageDraw.Draw(base)
        d.rectangle([x, y, x + view_w, y + int(view_h * 0.18)], fill=NAVY)
        d.text((x + 24, y + 28), "NO PROMISE OF RESULTS", font=font(40), fill=WHITE)


def paint_candle(base: Image.Image, shot: dict, local: float = 0) -> None:
    """One day. The picture changes before a hold can pass 20 seconds."""
    draw = ImageDraw.Draw(base)
    # Shot starts at 05:19.5. "Last price of the day" is 0–2.5s, the 11am
    # line is 6.6–17.1s, and "high, low and close" starts at 17.6s.
    # Each card is on screen within 2s of its line, and no hold reaches 20s.
    def heard(word: str) -> bool:
        at = _word_at(shot, word)
        if at is None:
            return local >= 14
        return local >= at

    named = bool(shot.get("word_times"))
    show_candle = heard("high") if named else local >= 14
    if local < 4.5:
        box = (MX, 220, RIGHT, 700)
        draw.rounded_rectangle(box, 22, fill=GLASS, outline=CYAN, width=2)
        candle = shot.get("candle") or {}
        close = int(candle.get("close") or 0)
        draw.text((box[0] + 48, box[1] + 48), candle.get("date") or "One day", font=font(36), fill=CYAN)
        _example(draw, box[2] - 280, box[1] + 40)
        draw.text((box[0] + 48, box[1] + 160), "The daily close", font=font(40), fill=WHITE)
        draw.text((box[0] + 48, box[1] + 250), f"{close:,}", font=font(72), fill=CYAN)
        draw.text((box[0] + 48, box[1] + 360), "The last price of that day. Marked Example.", font=font(36), fill=WHITE)
        return
    if not show_candle:
        box = (MX, 220, RIGHT, 700)
        draw.rounded_rectangle(box, 22, fill=GLASS, outline=CYAN, width=2)
        draw.text((box[0] + 48, box[1] + 48), "When the day is cut", font=font(40), fill=CYAN)
        draw.text((box[0] + 48, box[1] + 140), "11am AEDT", font=font(64), fill=WHITE)
        draw.text((box[0] + 48, box[1] + 230), "while daylight saving is in force", font=font(36), fill=WHITE)
        draw.text((box[0] + 48, box[1] + 340), "10am AEST", font=font(64), fill=WHITE)
        draw.text((box[0] + 48, box[1] + 430), "outside daylight saving", font=font(36), fill=WHITE)
        return
    # From 14s: the voice reaches "a simple candle" and the high, low and close.
    box = (MX, 190, RIGHT, 700)
    draw.rounded_rectangle(box, 22, fill=GLASS, outline=LINE, width=2)
    candle = shot.get("candle") or {}
    high = int(candle.get("high") or 0)
    low = int(candle.get("low") or 0)
    close = int(candle.get("close") or 0)
    title = candle.get("date") or shot.get("chart_title") or "One day"
    draw.text((box[0] + 36, box[1] + 24), title, font=font(36), fill=WHITE)
    _example(draw, box[2] - 220, box[1] + 24)
    span = max(1, high - low)
    top, bot = box[1] + 210, box[3] - 70
    cx = (box[0] + box[2]) // 2

    def y_of(price: int) -> int:
        return int(top + (high - price) / span * (bot - top))

    y_high, y_low, y_close = y_of(high), y_of(low), y_of(close)
    note = (
        "Traders call it a candle because the full version has a thick body and a thin wick, like a candle. "
        "Here we only need the high, the low and the close."
    )
    ny = box[1] + 68
    for line in wrap(note, 28, box[2] - box[0] - 80)[:3]:
        draw.text((box[0] + 36, ny), line, font=font(28), fill=CYAN)
        ny += 34
    draw.line([(cx, y_high), (cx, y_low)], fill=CYAN, width=4)
    draw.line([(cx - 28, y_high), (cx + 28, y_high)], fill=CYAN, width=4)
    draw.line([(cx - 28, y_low), (cx + 28, y_low)], fill=CYAN, width=4)
    draw.rounded_rectangle([cx - 46, y_close - 10, cx + 46, y_close + 10], 6, fill=CYAN)
    labels = (
        (y_high, f"High {high:,}", -280),
        (y_close, f"Close {close:,}", 80),
        (y_low, f"Low {low:,}", -280),
    )
    for y, label, dx in labels:
        key = label.split()[0].lower()
        if named and not heard(key):
            continue
        # Captions start at y=764. Keep every price label above that band.
        label_y = min(y - 18, 700)
        draw.text((cx + dx, label_y), label, font=font(36), fill=WHITE)
    # The labelled card starts at 14s. A second beat at 33s keeps that hold under 20s.
    if local >= 33:
        tag = "High, low and close"
        face = font(32)
        tw = int(face.getlength(tag)) + 36
        tx = box[0] + 36
        ty = box[3] - 64
        draw.rounded_rectangle([tx, ty, tx + tw, ty + 48], 10, fill=TAG, outline=CYAN, width=2)
        draw.text((tx + 18, ty + 8), tag, font=face, fill=WHITE)


def paint_course_map(base: Image.Image, shot: dict, local: float) -> None:
    """Steps 1–6, then 7–11, each while that part of the sentence is spoken."""
    draw = ImageDraw.Draw(base)
    steps = (
        ("1", "Introduction"),
        ("2", "Checklist"),
        ("3", "Definition"),
        ("4", "Market shape"),
        ("5", "Spacing"),
        ("6", "Entry and exit"),
        ("7", "Paper"),
        ("8", "Monitoring"),
        ("9", "Mistakes"),
        ("10", "Scaling up"),
        ("11", "Your complete plan"),
    )
    slide = 1
    words = shot.get("word_times") or []
    for text, start, _end in words:
        if str(text).lower().startswith("paper"):
            if local >= start:
                slide = 2
            break
    if not words and local >= float(shot.get("duration") or 12) * 0.62:
        slide = 2
    shown = steps[:6] if slide == 1 else steps[6:]
    y = 210
    left = MX + 28
    for number, name in shown:
        draw.rounded_rectangle([left, y, left + 72, y + 64], 12, fill=TAG, outline=CYAN, width=2)
        num_x = left + 22 if len(number) == 1 else left + 8
        draw.text((num_x, y + 12), number, font=font(36), fill=CYAN)
        draw.text((left + 96, y + 10), name, font=font(40), fill=CYAN)
        y += 88


def _burn_caption(frame: np.ndarray, shot: dict, local: float) -> np.ndarray:
    """Draw the current caption inside the 5% margin. The sidecar uses the same cue."""
    words = shot.get("word_times") or []
    if not words:
        return frame

    class _Word:
        def __init__(self, text, start, end):
            self.text = text
            self.start = start
            self.end = end

    timed = [_Word(text, start, end) for text, start, end in words]
    line = ""
    for sentence in _caption_sentences(timed):
        for group in _balanced_caption_lines(sentence, 42):
            if group[0].start - 0.05 <= local <= group[-1].end + 0.15:
                line = " ".join(word.text for word in group)
    if not line:
        return frame
    image = Image.fromarray(frame)
    draw = ImageDraw.Draw(image)
    face = font(32)
    width = int(face.getlength(line))
    max_w = W - 2 * MX
    if width > max_w:
        face = font(28)
        width = int(face.getlength(line))
    x = max(MX, (W - width) // 2)
    # Below the card (cards end at y=760) so a cue cannot cover a price label.
    y = 772
    draw.rounded_rectangle([x - 16, y - 8, x + width + 16, y + 40], 10, fill=NAVY, outline=CYAN, width=2)
    draw.text((x, y), line, font=face, fill=WHITE)
    return np.asarray(image, dtype=np.uint8)


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
    elif shot.get("visual") and (
        (
            shot.get("lesson_id") == "bp-01-introduction"
            and (shot.get("chapter") or "") == "The stop"
            and (_word_at(shot, "october") or 10**9) <= local
        )
        or not (shot.get("lesson_still") and local >= 16)
    ):
        import motions
        title_bar(img, shot, progress)
        motions.paint_visual(img, shot, local, sys.modules[__name__])
        lower_third(ImageDraw.Draw(img), shot)
        draw_footer(ImageDraw.Draw(img))
    elif shot.get("lesson_still") and kind not in {"chart"} and not shot.get("candle"):
        title_bar(img, shot, progress)
        paint_lesson_still(img, shot, local, dur)
        lower_third(ImageDraw.Draw(img), shot)
        draw_footer(ImageDraw.Draw(img))
    elif (
        shot.get("lesson_id") == "bp-01-introduction"
        and (shot.get("chapter") or "") == "When price leaves the band"
    ):
        title_bar(img, shot, progress)
        paint_leave(img, shot, local)
        lower_third(ImageDraw.Draw(img), shot)
        draw_footer(ImageDraw.Draw(img))
    elif (shot.get("chapter") or "") == "The idea" and shot.get("lesson_id") == "bp-01-introduction":
        title_bar(img, shot, progress)
        paint_idea(img, shot, local)
        lower_third(ImageDraw.Draw(img), shot)
        draw_footer(ImageDraw.Draw(img))
    elif (shot.get("chapter") or "") == "Crossings" and shot.get("lesson_id") == "bp-01-introduction":
        title_bar(img, shot, progress)
        paint_crossings(img, shot, local)
        lower_third(ImageDraw.Draw(img), shot)
        draw_footer(ImageDraw.Draw(img))
    elif kind == "stack":
        title_bar(img, shot, progress)
        paint_stack(img, shot, local)
        lower_third(ImageDraw.Draw(img), shot)
        draw_footer(ImageDraw.Draw(img))
    elif kind == "worked" and (shot.get("chapter") or "") == "One pair":
        title_bar(img, shot, progress)
        paint_pair(img, shot, local)
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
    elif (
        kind == "lesson-still"
        and shot.get("lesson_id") == "bp-01-introduction"
        and (shot.get("chapter") or "") == "When price leaves the band"
    ):
        title_bar(img, shot, progress)
        paint_leave(img, shot, local)
        lower_third(ImageDraw.Draw(img), shot)
        draw_footer(ImageDraw.Draw(img))
    elif kind == "lesson-still" and (shot.get("chapter") or "") == "The map":
        title_bar(img, shot, progress)
        paint_course_map(img, shot, local)
        lower_third(ImageDraw.Draw(img), shot)
        draw_footer(ImageDraw.Draw(img))
    elif kind == "lesson-still":
        title_bar(img, shot, progress)
        paint_lesson_still(img, shot, local, dur)
        lower_third(ImageDraw.Draw(img), shot)
        draw_footer(ImageDraw.Draw(img))
    else:
        title_bar(img, shot, progress)
        if shot.get("board") in {"seven-lines", "no-secrets", "three-words", "say-the-page"}:
            paint_board(img, shot, local)
        elif (
            shot.get("lesson_id") == "bp-02-what-you-need"
            and (shot.get("chapter") or "") == "Copy the path"
        ):
            paint_copy_band(img)
        elif shot.get("candle"):
            paint_candle(img, shot, local)
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
    shape = (n,) + (1,) * (left.ndim - 1)
    mid = left[-n:] * out_r.reshape(shape) + right[:n] * in_r.reshape(shape)
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
    spans: list[tuple[float, float]] = []
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
        spans.append((offset, len(buf) / sr))
        timed.extend(_time_sentence(speaker, pace, sentence, audio, sr, offset))
        if index < len(sentences) - 1:
            # The course map reads eleven steps. A short pause keeps them from running together.
            gap = SENTENCE_GAP
            if (
                shot.get("lesson_id") == "bp-01-introduction"
                and (shot.get("chapter") or "") == "The map"
                and len(sentences) > 2
            ):
                gap = 0.70
            # Kokoro was leaving a dead hole after "fills," inside one take.
            # A short pad between the two clean sentences replaces that join.
            if sentence.rstrip().endswith("fills."):
                gap = 0.20
            buf = _xfade(buf, np.zeros(int(gap * sr), dtype=np.float32), sr)
    hold = max(0.0, _reading_time(shot) - len(buf) / sr)
    revealing = shot.get("kind") in {"chart", "analogy"} and not shot.get("board") and not shot.get("candle")
    cap = REVEAL_GAP_CAP if revealing else LINE_GAP_CAP
    tail = min(cap, hold + BEAT_GAP)
    if (
        shot.get("lesson_id") == "bp-01-introduction"
        and (shot.get("chapter") or "") == "When price leaves the band"
    ):
        tail += 1.0
    if shot.get("lesson_id") == "bp-01-introduction" and (shot.get("chapter") or "") == "One pair":
        tail += 6.0
    if shot.get("visual") == "BP01-V06":
        tail += 4.0
    if tail > 0:
        buf = _xfade(buf, np.zeros(int(tail * sr), dtype=np.float32), sr)
    shot["sentence_spans"] = spans
    shot["word_times"] = [(word.text, word.start, word.end) for word in timed]
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


def _caption_sentences(words: list) -> list[list]:
    """One group per spoken sentence. A stop is . ? or ! on the last word."""
    sentences: list[list] = []
    current: list = []
    for word in words:
        current.append(word)
        if str(word.text).rstrip().endswith((".", "?", "!")):
            sentences.append(current)
            current = []
    if current:
        sentences.append(current)
    return sentences


def _pack_caption_line(words: list, width: int) -> list[list]:
    lines: list[list] = []
    current: list = []
    for word in words:
        trial = current + [word]
        text = " ".join(item.text for item in trial)
        if current and len(text) > width:
            lines.append(current)
            current = [word]
        else:
            current = trial
    if current:
        lines.append(current)
    return lines


def _balanced_caption_lines(words: list, width: int = 42) -> list[list]:
    """Fewest lines that fit, then the split whose longest line is as short as possible."""
    if not words:
        return []
    longest = max(len(str(word.text)) for word in words)
    cap = max(width, longest)
    fewest = _pack_caption_line(words, cap)
    best = fewest
    lo, hi = longest, cap
    while lo <= hi:
        mid = (lo + hi) // 2
        trial = _pack_caption_line(words, mid)
        if len(trial) <= len(fewest):
            best = trial
            hi = mid - 1
        else:
            lo = mid + 1
    return best


def _write_lesson_captions(vtt: Path, srt: Path, words: list) -> None:
    """One sentence at a time. A line holds long enough to read, and does not cross a stop."""
    from voice.captions import _stamp

    width = 42
    limit = 17.9
    cues = []
    previous_end = 0.0
    for sentence in _caption_sentences(words):
        for group in _balanced_caption_lines(sentence, width):
            text = " ".join(word.text for word in group).replace("Grid Bot Builder", "GridBot Builder").replace("Grid Bot Blueprint", "GridBot Blueprint")
            start = max(group[0].start, previous_end)
            end = max(group[-1].end, start + len(text) / limit)
            cues.append((start, end, [text]))
            previous_end = end
    # A short sentence can be spoken in under 0.7s. Hold the cue in the
    # silent gap around it so the line still meets the caption minimum.
    for index, (start, end, lines) in enumerate(cues):
        if end - start >= 0.7:
            continue
        nxt = cues[index + 1][0] if index + 1 < len(cues) else end + 1.0
        prev = cues[index - 1][1] if index else 0.0
        end = min(start + 0.75, nxt - 0.001)
        if end - start < 0.75:
            start = max(prev, end - 0.75)
        cues[index] = (start, max(end, start + 0.001), lines)
    vtt_lines = ["WEBVTT", ""]
    srt_lines = []
    for index, (start, end, lines) in enumerate(cues, start=1):
        vtt_lines.append(
            f"{_stamp(start)} --> {_stamp(end)} line:78% position:50% align:center size:90%"
        )
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
    if not excerpt_seconds:
        if words < 1600 or words > 2400:
            raise SystemExit(
                f"{sid} spoken words {words} are outside 1,600–2,400 (10–15 min at 160 wpm)"
            )
        spoken = " ".join(s["vo"] for s in shots)
        for banned in ("Market Pros", "Binance", "ABN", "AFSL", "DeFi"):
            if re.search(rf"\b{re.escape(banned)}\b", spoken, re.IGNORECASE):
                raise SystemExit(f"{sid} speaks a banned phrase: {banned}")
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
    for shot in shots:
        frames = max(1, int(round(shot["duration"] * FPS)))
        shot["frames"] = frames
        for n in range(frames):
            local = n / FPS
            # A hard cut. Blending the previous frame left its words on top of the new card.
            frame = paint(shot, local, lesson_t / clock)
            frame = _burn_caption(frame, shot, local)
            proc.stdin.write(frame.tobytes())
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
    vtt_path = sidecar / f"{sid}.vtt"
    srt_path = sidecar / f"{sid}.srt"
    _write_lesson_captions(vtt_path, srt_path, timed)
    _cap_caption_speed(vtt_path)
    _srt_from_capped_vtt(vtt_path, srt_path)
    caption_dir = ROOT / "course/blueprint-rebuild/captions"
    caption_dir.mkdir(parents=True, exist_ok=True)
    (caption_dir / f"{sid}.vtt").write_text(vtt_path.read_text(encoding="utf-8"), encoding="utf-8")
    (caption_dir / f"{sid}.srt").write_text(srt_path.read_text(encoding="utf-8"), encoding="utf-8")
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


def _clamp_cue_ends(text: str) -> str:
    """End each cue when the next cue starts, so two cues are never on screen together."""
    from voice.captions import _stamp

    gate_root = ROOT / "skills/video-production/quality-gate"
    if str(gate_root) not in sys.path:
        sys.path.insert(0, str(gate_root))
    from gate.captions import parse_captions

    cues = list(parse_captions(text))
    if not cues:
        return text if text.endswith("\n") else text + "\n"
    rows = [[cue.start, cue.end, cue.text] for cue in cues]
    for index, row in enumerate(rows[:-1]):
        row[1] = min(row[1], rows[index + 1][0])
        if row[1] <= row[0]:
            row[1] = row[0] + 0.001
    # A clamp can shorten a cue. Pull the start back into the gap before it
    # when that gap is free, so the line still fits the 18 character cap.
    for index, row in enumerate(rows):
        span = row[1] - row[0]
        if span > 0 and len(row[2]) / span <= 18.0 + 1e-9:
            continue
        need = len(row[2]) / 18.0
        earliest = rows[index - 1][1] if index else row[0]
        row[0] = max(earliest, row[1] - need)
        if row[0] >= row[1]:
            row[0] = max(earliest, row[1] - 0.001)
    lines = ["WEBVTT", ""]
    for start, end, payload in rows:
        lines.append(f"{_stamp(start)} --> {_stamp(end)}")
        lines.append(payload)
        lines.append("")
    return "\n".join(lines) + "\n"


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
    path.read_text(encoding="utf-8")
    gate_root = ROOT / "skills/video-production/quality-gate"
    if str(gate_root) not in sys.path:
        sys.path.insert(0, str(gate_root))
    from gate.captions import parse_captions

    parsed = list(parse_captions(path.read_text(encoding="utf-8")))
    for index, cue in enumerate(parsed):
        if index + 1 < len(parsed) and cue.end > parsed[index + 1].start + 0.0005:
            raise SystemExit(
                f"{path.name} {cue.start:.2f}s still overlaps the next caption"
            )
        span = cue.end - cue.start
        cps = len(cue.text) / span if span > 0 else float("inf")
        if cps > limit or len(cue.text) > 42:
            raise SystemExit(
                f"{path.name} {cue.start:.2f}s is {cps:.1f} characters per second "
                f"after the {limit:.0f} cap"
            )
        if span < 0.7:
            raise SystemExit(
                f"{path.name} {cue.start:.2f}s is only {span:.2f}s. A caption needs 0.7s"
            )
        body = cue.text.rstrip()
        # A decimal such as 0.01 is not a sentence end. ? and ! still are.
        for index, mark in enumerate(body[:-1]):
            if mark in "?!":
                raise SystemExit(
                    f"{path.name} {cue.start:.2f}s crosses a sentence end: {cue.text}"
                )
            if mark == "." and not (
                index > 0
                and body[index - 1].isdigit()
                and index + 1 < len(body)
                and body[index + 1].isdigit()
            ):
                raise SystemExit(
                    f"{path.name} {cue.start:.2f}s crosses a sentence end: {cue.text}"
                )


def _srt_from_capped_vtt(vtt: Path, srt: Path) -> None:
    """The SRT is a copy of the capped VTT, so both files share the 18 cps limit."""
    from voice.captions import _stamp

    gate_root = ROOT / "skills/video-production/quality-gate"
    if str(gate_root) not in sys.path:
        sys.path.insert(0, str(gate_root))
    from gate.captions import parse_captions

    lines: list[str] = []
    parsed = list(parse_captions(vtt.read_text(encoding="utf-8")))
    for index, cue in enumerate(parsed):
        lines.append(str(index + 1))
        lines.append(f"{_stamp(cue.start, srt=True)} --> {_stamp(cue.end, srt=True)}")
        lines.append(cue.text)
        lines.append("")
    srt.write_text("\n".join(lines) + "\n", encoding="utf-8")


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
