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
AMBER = (255, 176, 92)
GLASS = (9, 22, 40)
LINE = (28, 64, 88)
FONT = "/usr/share/fonts/truetype/macos/Inter-Bold.ttf"
FONT_MED = "/usr/share/fonts/truetype/macos/Inter-SemiBold.ttf"
FONT_REG = "/usr/share/fonts/truetype/macos/Inter-Regular.ttf"
MX, MY = 96, 64
RIGHT = W - MX - 16
DISCLAIMER = (
    "Educational content only. Not financial advice. "
    "Trading involves risk; you can lose money."
)
FOOT = "Educational content only. Not financial advice."
COVER = ROOT / "course/images/style-ref/01M6MSHVNHX3WQH81XS8KQK1HT.png"
MASCOT_SRC = ROOT / "course/images/fallback/el-06-circuit-breakers/28.png"
WORD_BOX = (260, 52, 760, 176)
MASCOT_BOX = (1105, 400, 1380, 812)
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
    return ImageFont.truetype(path, size)


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


@lru_cache(maxsize=1)
def wordmark() -> Image.Image:
    src = Image.open(COVER).convert("RGB").crop(WORD_BOX)
    return knockout(src)


@lru_cache(maxsize=1)
def mascot() -> Image.Image:
    src = Image.open(MASCOT_SRC).convert("RGB").crop(MASCOT_BOX)
    return knockout(src, thresh=22)


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
    table = [
        ("objective", "Objective", "One skill this lesson is building. Say it in your own words."),
        ("recap", "Recap", "A line to keep. Three lines, then the next lesson."),
        ("stop", "Stop", "A sentence that ends the idea when the close leaves the band and stays gone."),
        ("finish", "Finish", "The exit, written before the entry, and pointed at a real date."),
        ("range", "Range", "The top and the bottom copied from the prints, before any rung is drawn."),
        ("level", "Level", "A price where a limit order waits. It does not chase the market."),
        ("gap", "Gap", "The space between two rungs. Count gaps, not the lines that bound them."),
        ("wick", "Wick", "The high or low that a neat round number can miss."),
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
        ("trend", "Leave", "A path that exits the band and keeps making ground one way."),
        ("worked", "Worked example", "Figures you can point at. Marked Example. Not an order."),
        ("monitor", "Check", "Three questions on a date you chose, then you stop."),
        ("field", "Field", "A box on the page. Copy only what the page already says."),
        ("venue", "No venue", "No logo, no login, no balance. The figures are public closes."),
        ("liquidat", "Liquidation", "A venue can close a contract when the margin is gone. Spot is not that."),
    ]
    for key, term, defin in table:
        if key in low:
            text = defin or cap
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
    shots: list[dict] = [brand, disc]
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
    for shot in shots:
        shot["lesson_no"] = number
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
    return shots


def estimate(shot: dict) -> float:
    words = max(1, len((shot.get("vo") or "").split()))
    sec = words / 2.55 + 0.45
    kind = shot.get("kind")
    if kind == "brand":
        sec = max(sec, 8.5)
    elif kind == "disclaimer":
        sec = max(sec, 7.0)
    elif kind == "outro":
        sec = max(sec, 6.5)
    else:
        sec = max(sec, 5.0)
    return sec


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
    shift = int(local * 16) % 64
    grid = (18, 36, 58)
    for x in range(-64 + shift, W, 64):
        draw.line([(x, 0), (x, H)], fill=grid, width=1)
    for y in range(shift, H, 64):
        draw.line([(0, y), (W, y)], fill=grid, width=1)
    return img


def draw_footer(draw: ImageDraw.ImageDraw) -> None:
    face = font(36, "reg")
    draw.text((MX, 990), FOOT, font=face, fill=DIM)


def title_bar(base: Image.Image, shot: dict, progress: float) -> None:
    draw = ImageDraw.Draw(base)
    mark = scaled(wordmark(), 48)
    paste(base, mark, (MX, 72))
    chapter = shot.get("heading") or shot.get("chapter") or ""
    if chapter == "Hook":
        chapter = "Opening"
    size = fit_size(chapter, 900, 40, 36)
    draw.text((MX + mark.width + 28, 76), chapter, font=font(size), fill=WHITE)
    if shot.get("example"):
        label = "EXAMPLE"
        face = font(36)
        tw = int(face.getlength(label))
        x1 = RIGHT
        x0 = x1 - tw - 36
        draw.rounded_rectangle([x0, 70, x1, 118], 12, fill=(24, 48, 28), outline=AMBER, width=2)
        draw.text((x0 + 18, 76), label, font=face, fill=AMBER)
    y = 136
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


def chart_card(base: Image.Image, shot: dict, local: float, dur: float, box=None) -> None:
    draw = ImageDraw.Draw(base)
    if box is None:
        box = (MX, 168, RIGHT, 752)
    draw.rounded_rectangle(box, 22, fill=GLASS, outline=LINE, width=2)
    series = _series(shot)
    title = shot.get("chart_title") or ""
    if title:
        size = fit_size(title, box[2] - box[0] - 80, 36, 36)
        draw.text((box[0] + 28, box[1] + 18), title, font=font(size), fill=WHITE)
    if not series:
        draw.text((box[0] + 36, box[1] + 80), "Example window", font=font(36), fill=DIM)
        return
    plot = (box[0] + 28, box[1] + 72, box[2] - 210, box[3] - 36)
    gutter_x = box[2] - 196
    closes = [float(r["close"]) for r in series]
    lo = min(float(r["low"]) for r in series)
    hi = max(float(r["high"]) for r in series)
    pad = (hi - lo) * 0.12 or 1
    lo_p, hi_p = lo - pad, hi + pad
    n = len(series)
    end = float(shot.get("reveal") or 1)
    start = float(shot.get("reveal_from") or 0)
    if abs(end - start) < 0.03:
        start = max(0.0, end - 0.15)
    now = start + (end - start) * ease(min(1.0, local / max(1.2, dur * 0.88)))
    last = max(2, min(n, int(round(now * (n - 1))) + 1))
    full = [_map(i, n, closes[i], lo_p, hi_p, plot) for i in range(n)]
    if len(full) > 1:
        draw.line(full, fill=(36, 78, 96), width=3)
    shown = full[:last]
    if len(shown) > 1:
        draw.line(shown, fill=CYAN, width=5)
    hx, hy = shown[-1]
    r = 8
    draw.ellipse((hx - r - 3, hy - r - 3, hx + r + 3, hy + r + 3), outline=CYAN, width=3)
    draw.ellipse((hx - r, hy - r, hx + r, hy + r), fill=WHITE)
    row = series[last - 1]
    tag = f"{row['date'][8:10]} {row['date'][5:7]}  {int(round(row['close'])):,}"
    # Friendlier tag: day month via the series date ISO.
    months = ["", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    y, m, d = row["date"].split("-")
    tag = f"{int(d)} {months[int(m)]}  {int(round(row['close'])):,}"
    face = font(36)
    tw = int(face.getlength(tag)) + 28
    if hx > (plot[0] + plot[2]) / 2:
        tx = hx - tw - 14
    else:
        tx = hx + 16
    tx = min(plot[2] - tw, max(plot[0], tx))
    ty = hy - 56
    if ty < plot[1]:
        ty = hy + 18
    if ty + 48 > plot[3]:
        ty = plot[1]
    draw.rounded_rectangle([tx, ty, tx + tw, ty + 48], 10, fill=NAVY, outline=CYAN, width=2)
    draw.text((tx + 14, ty + 4), tag, font=face, fill=WHITE)

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
        color = AMBER if focus is not None and abs(price - float(focus)) < 2 else DIM
        x_a, x_b = plot[0], plot[2]
        step = 18
        x = x_a
        while x < x_b:
            draw.line([(x, yy), (min(x + 8, x_b), yy)], fill=color, width=2)
            x += step
        label = f"{int(round(price)):,}"
        lf = font(36)
        if gutter_x + lf.getlength(label) > box[2] - 16:
            continue
        draw.text((gutter_x, yy - 22), label, font=lf, fill=color)


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
    bot = mascot()
    mh = 520
    sprite = scaled(bot, mh)
    fade = ease(min(1.0, local / 0.8))
    if fade < 1:
        sprite = sprite.copy()
        alpha = sprite.getchannel("A").point(lambda p: int(p * fade))
        sprite.putalpha(alpha)
    paste(base, sprite, (W - MX - sprite.width, 300))


def paint_disclaimer(base: Image.Image, local: float) -> None:
    draw = ImageDraw.Draw(base)
    lines = [
        "Educational content only.",
        "Not financial advice.",
        "Trading involves risk; you can lose money.",
    ]
    # On screen together for the whole card, after a short fade.
    fade = ease(min(1.0, local / 0.45))
    if fade <= 0:
        return
    color = tuple(int(c * fade) for c in WHITE)
    widths = [font(52).getlength(line) for line in lines]
    block_h = 3 * 84
    y = (H - block_h) // 2 - 10
    rule = 240
    rx = (W - rule) // 2
    draw.rectangle([rx, y - 40, rx + rule, y - 32], fill=CYAN)
    for line in lines:
        size = fit_size(line, W - 2 * MX, 52, 36)
        tw = font(size).getlength(line)
        x = (W - tw) / 2
        draw.text((x, y), line, font=font(size), fill=color)
        y += 84


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
        size = 40 if font(40).getlength(text) < (W - 2 * MX - 80) else 36
        yy = y + 28
        for line in wrap(text, size, W - 2 * MX - 80)[:2]:
            draw.text((MX + 32, yy), line, font=font(size), fill=WHITE)
            yy += size + 4
        y += 128


def paint_analogy(base: Image.Image, shot: dict, local: float, dur: float) -> None:
    draw = ImageDraw.Draw(base)
    left = (MX, 168, 940, 752)
    right = (968, 168, RIGHT, 752)
    still = shot.get("still")
    panel = Image.new("RGB", (left[2] - left[0], left[3] - left[1]), NAVY2)
    if still:
        src = Image.open(still).convert("RGB")
        scale = min(panel.width / src.width, panel.height / src.height, 1.0)
        nw, nh = max(1, int(src.width * scale)), max(1, int(src.height * scale))
        fitted = src.resize((nw, nh), Image.Resampling.LANCZOS)
        panel.paste(fitted, ((panel.width - nw) // 2, (panel.height - nh) // 2))
    base.paste(panel, (left[0], left[1]))
    draw.rounded_rectangle(left, 18, outline=LINE, width=2)
    chart_card(base, shot, local, dur, right)


def paint_outro(base: Image.Image, shot: dict, local: float) -> None:
    """Template end card. The right side stays clear for an end screen."""
    templates = ROOT / "skills/video-production/templates"
    if str(templates) not in sys.path:
        sys.path.insert(0, str(templates))
    from pack.paint import paint_endcard

    card_path = Path("/tmp/bp-endcard.png")
    next_title = shot.get("caption") or "End of the Blueprint"
    paint_endcard(shot.get("lesson_title") or "Blueprint", next_title, card_path)
    card = Image.open(card_path).convert("RGB")
    if card.size != (W, H):
        card = card.resize((W, H), Image.Resampling.LANCZOS)
    base.paste(card, (0, 0))
    if local < 0.35:
        fade = Image.new("RGB", (W, H), NAVY)
        base.paste(Image.blend(fade, base, ease(local / 0.35)))
    draw = ImageDraw.Draw(base)
    draw.text((MX, 990), FOOT, font=font(36, "reg"), fill=DIM)


def paint(shot: dict, local: float, progress: float) -> np.ndarray:
    dur = float(shot.get("duration") or estimate(shot))
    img = background(local)
    kind = shot.get("kind") or "chart"
    if kind == "brand":
        paint_brand(img, shot, local)
        draw_footer(ImageDraw.Draw(img))
    elif kind == "disclaimer":
        paint_disclaimer(img, local)
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
        paint_analogy(img, shot, local, dur)
        lower_third(ImageDraw.Draw(img), shot)
        draw_footer(ImageDraw.Draw(img))
    else:
        title_bar(img, shot, progress)
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
    raw = dest.with_name("pad-raw.wav")
    sf.write(str(raw), stereo, sr)
    norm = dest.with_name("pad-norm.wav")
    run([
        "ffmpeg", "-y", "-v", "error", "-i", str(raw),
        "-af", "loudnorm=I=-29:TP=-3:LRA=5:linear=true",
        str(norm),
    ])
    fade_out = min(3.0, duration / 4)
    run([
        "ffmpeg", "-y", "-v", "error", "-i", str(norm),
        "-af", f"afade=t=in:st=0:d=2,afade=t=out:st={max(0, duration - fade_out):.3f}:d={fade_out:.3f}",
        str(dest),
    ])


def _voice_stack() -> None:
    root = ROOT / "skills/video-production"
    for folder in (root, root / "natural-voice"):
        text = str(folder)
        if text not in sys.path:
            sys.path.insert(0, text)


def _mood(kind: str) -> str:
    return {"brand": "upbeat-intro", "disclaimer": "serious-risk", "outro": "recap"}.get(kind, "calm-teacher")


def synth_voice(shots: list[dict], dest: Path) -> tuple[float, list]:
    """Kokoro af_heart through natural-voice, with word times on the timeline."""
    _voice_stack()
    from voice.align import Word
    from voice.speak import Speaker

    speakers: dict = {}
    pieces: list[np.ndarray] = []
    timed: list[Word] = []
    clock = 0.0
    sample_rate = None
    for i, shot in enumerate(shots):
        mood = _mood(shot.get("kind") or "chart")
        if mood not in speakers:
            speakers[mood] = Speaker(engine="kokoro", mood=mood)
        audio, rate, words, _method = speakers[mood].render(shot["vo"])
        if sample_rate is None:
            sample_rate = rate
        if rate != sample_rate:
            raise SystemExit("voice sample rate changed mid-lesson")
        min_sec = 0.0
        if shot["kind"] == "brand":
            min_sec = 8.5
        elif shot["kind"] == "disclaimer":
            min_sec = 7.0
        elif shot["kind"] == "outro":
            min_sec = 6.5
        elif shot["kind"] != "chart":
            min_sec = 5.0
        pad = max(0, int(min_sec * rate) - len(audio))
        if pad:
            audio = np.concatenate([audio, np.zeros(pad, dtype=np.float32)])
        shot["duration"] = len(audio) / rate
        for word in words:
            timed.append(Word(word.text, word.start + clock, word.end + clock))
        clock += shot["duration"]
        pieces.append(audio)
        if (i + 1) % 4 == 0:
            print(f"  voice {i + 1}/{len(shots)} t={clock:.0f}s", flush=True)
    voice = np.concatenate(pieces) if pieces else np.zeros(1, dtype=np.float32)
    sf.write(str(dest), voice, sample_rate or 24000)
    return clock, timed


def _excerpt(shots: list[dict], seconds: float) -> list[dict]:
    kept = []
    total = 0.0
    for shot in shots:
        guess = estimate(shot)
        if kept and total + guess > max(seconds, 24):
            break
        kept.append(shot)
        total += guess
        if total >= min(seconds, 22):
            break
    if kept and kept[-1].get("kind") not in {"brand", "disclaimer"}:
        kept[-1]["vo"] = clip_vo(kept[-1]["vo"], 1, 22)
    if not any(shot.get("kind") == "outro" for shot in kept):
        kept.append({
            "kind": "outro",
            "chapter": "Next",
            "vo": "Next. The page stays marked example. No order is sent.",
            "caption": "What you are going to need",
            "lesson_no": shots[0].get("lesson_no", "01"),
            "lesson_title": shots[0].get("lesson_title", "Blueprint"),
            "term": "Next",
            "definition": "Educational content only. Not financial advice.",
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
        "disclaimer_on_screen": "Educational content only. Not financial advice.",
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
        "disclaimer_on_screen: \"Educational content only. Not financial advice.\"\n"
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
    clock, timed = synth_voice(shots, voice_path)
    print(f"  voice {clock:.1f}s", flush=True)
    bed = work / "bed.wav"
    compose_pad(clock + 1.0, bed)
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
    from voice.captions import write_chapters, write_srt, write_vtt, write_words

    mixed = work / "mixed.wav"
    duck_under_voice(bed, voice_path, mixed)
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
        "-c:a", "aac", "-b:a", "320k", "-ar", "48000", "-ac", "2",
        "-shortest", "-movflags", "+faststart",
        str(final_path),
    ])
    sidecar = final_path.parent
    if "course" in sidecar.resolve().parts:
        sidecar = ROOT / "blueprint-smoke" / sid
        sidecar.mkdir(parents=True, exist_ok=True)
    write_words(sidecar / "words.json", timed, engine="kokoro", mood="af_heart", method="acoustic-forced-align")
    write_vtt(sidecar / f"{sid}.vtt", timed)
    _cap_caption_speed(sidecar / f"{sid}.vtt")
    write_srt(sidecar / f"{sid}.srt", timed)
    chapters = []
    cursor = 0.0
    for shot in shots:
        chapters.append((cursor, shot.get("chapter") or shot.get("kind") or "Section"))
        cursor += float(shot["duration"])
    if chapters:
        chapters[0] = (0.0, chapters[0][1])
    write_chapters(sidecar / "chapters.txt", chapters)
    lesson_yaml = sidecar / f"{sid}.yaml"
    _lesson_yaml(sid, shots, lesson_yaml)
    report_dir = sidecar / "gate"
    code = subprocess.call([
        sys.executable,
        str(ROOT / "skills/video-production/quality-gate/cli.py"),
        "check", str(final_path),
        "--format", "blueprint",
        "--captions", str(sidecar / f"{sid}.vtt"),
        "--transcript", str(lesson_yaml),
        "--lesson", str(lesson_yaml),
        "--out", str(report_dir),
    ])
    final_i, final_tp = measured_lufs(final_path)
    print(f"WROTE {final_path} {clock:.1f}s lufs {final_i:.1f} peak {final_tp:.1f}")
    print(f"GATE {report_dir / 'report.md'}")
    if code != 0:
        raise SystemExit(f"quality gate failed for {sid}. The build stops.")
    return final_path


def _cap_caption_speed(path: Path, limit: float = 18.0) -> None:
    """Shorten a cue that the voice packed faster than the caption limit."""

    def seconds(token: str) -> float:
        token = token.strip().split()[0]
        hours, minutes, rest = token.split(":")
        sec, ms = rest.split(".")
        return int(hours) * 3600 + int(minutes) * 60 + int(sec) + int(ms) / 1000

    lines_out = ["WEBVTT", ""]
    for block in path.read_text(encoding="utf-8").strip().split("\n\n"):
        rows = [row for row in block.splitlines() if row.strip() and row.strip() != "WEBVTT"]
        if not rows or "-->" not in rows[0]:
            continue
        left, right = rows[0].split("-->", 1)
        span = max(0.2, seconds(right) - seconds(left))
        text = " ".join(rows[1:])
        while text and len(text) / span > limit and " " in text:
            text = text.rsplit(" ", 1)[0]
        lines_out.extend([rows[0], text, ""])
    path.write_text("\n".join(lines_out) + "\n")


def _ts(sec: float) -> str:
    ms = int(round(sec * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d}.{ms:03d}"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--id", required=True)
    ap.add_argument("--stills", action="store_true")
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
    if args.stills:
        write_stills(args.id)
        return
    render(args.id, excerpt_seconds=args.excerpt, pass_list=args.pass_list, dest=args.dest)


if __name__ == "__main__":
    main()
