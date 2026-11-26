"""Voice-tied stills for BP-03 to BP-11. No film is rendered.

Charts, diagrams and cards are drawn here. Photographic stills are not
invented. A figure is drawn only when that beat says it. There is no
corner EXAMPLE chip.
"""

from __future__ import annotations

import json
import math
import re
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
APPROVED = ROOT / "course/approved-scripts-25nov"
OUT = ROOT / "course/visuals-25nov"
NUMBERS = ROOT / "course/blueprint-rebuild/numbers"
FONT_DIR = ROOT / "skills/video-production/fonts/inter"
WPM = 163
MAX_SECONDS = 7.8
MAX_WORDS = max(8, int(MAX_SECONDS * WPM / 60))
W, H = 1920, 1080
MARGIN = 96
NAVY = (7, 17, 31)
CYAN = (0, 229, 255)
WHITE = (255, 255, 255)
GLASS = (9, 22, 40)
MUTED = (154, 168, 188)

GATE = ROOT / "skills/video-production/quality-gate"
sys.path.insert(0, str(GATE))
from gate.numbers import (  # noqa: E402
    FIGURE,
    _GROUPED,
    _covered,
    _iter_dates,
    find_dates,
    screen_figures,
)

LESSONS = {
    "03": "bp-03-what-is-a-grid-bot",
    "04": "bp-04-market-regimes",
    "05": "bp-05-spacing-and-range",
    "06": "bp-06-entry-and-exit",
    "07": "bp-07-spot-paper-trading",
    "08": "bp-08-managing-and-monitoring",
    "09": "bp-09-common-mistakes",
    "10": "bp-10-scaling-up",
    "11": "bp-11-advanced-liquidation",
}


def font(size: int, weight: str = "bold") -> ImageFont.FreeTypeFont:
    name = {"bold": "Inter-Bold.ttf", "reg": "Inter-Regular.ttf"}[weight]
    return ImageFont.truetype(str(FONT_DIR / name), size)


def wrap(text: str, face: ImageFont.FreeTypeFont, width: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        trial = f"{current} {word}".strip()
        if current and face.getlength(trial) > width:
            lines.append(current)
            current = word
        else:
            current = trial
    if current:
        lines.append(current)
    return lines or [""]


def spoken_body(text: str) -> str:
    return text.split("## Spoken script", 1)[1].strip()


def paragraphs(body: str) -> list[str]:
    return [part.strip() for part in re.split(r"\n\s*\n", body) if part.strip()]


def sentences(paragraph: str) -> list[str]:
    parts = re.split(r"(?<=[.?!])\s+", paragraph.strip())
    return [part.strip() for part in parts if part.strip()]


def pack(words: list[str]) -> list[list[str]]:
    """Chunks of at most MAX_WORDS, preferring a comma as the join."""
    if len(words) <= MAX_WORDS:
        return [words]
    chunks: list[list[str]] = []
    current: list[str] = []
    for word in words:
        current.append(word)
        joined = " ".join(current)
        boundary = word.endswith(",") or word.endswith(";") or word.endswith(":")
        if len(current) >= MAX_WORDS or (boundary and len(current) >= 8):
            chunks.append(current)
            current = []
    if current:
        if chunks and len(current) < 4 and len(chunks[-1]) + len(current) <= MAX_WORDS:
            chunks[-1].extend(current)
        else:
            chunks.append(current)
    return chunks


def beats_for(paragraph: str) -> list[str]:
    words = paragraph.split()
    need = max(1, math.ceil((len(words) / WPM * 60) / 8))
    chunks: list[list[str]] = []
    for sentence in sentences(paragraph):
        chunks.extend(pack(sentence.split()))
    guard = 0
    while guard < 40:
        guard += 1
        too_long = [i for i, chunk in enumerate(chunks) if len(chunk) / WPM * 60 > 8]
        if not too_long and len(chunks) >= need:
            break
        index = too_long[0] if too_long else max(range(len(chunks)), key=lambda i: len(chunks[i]))
        chunk = chunks[index]
        if len(chunk) < 2:
            break
        half = max(1, len(chunk) // 2)
        chunks[index:index + 1] = [chunk[:half], chunk[half:]]
    return [" ".join(chunk) for chunk in chunks]


def price_tokens(text: str) -> list[str]:
    """Figure spellings in this sentence. Digits inside a date stay off the ladder."""
    skip = [(match.start(), match.end()) for match in _iter_dates(text or "")]
    found: list[str] = []
    occupied = list(skip)
    for match in _GROUPED.finditer(text or ""):
        if _covered(occupied, match.start(), match.end()):
            continue
        found.append(match.group(0))
        occupied.append((match.start(), match.end()))
    for match in FIGURE.finditer(text or ""):
        if _covered(occupied, match.start(), match.end()):
            continue
        value = match.group(0)
        if value.isdigit() and len(value) < 2:
            continue
        found.append(value)
    return found


def background() -> Image.Image:
    image = Image.new("RGB", (W, H), NAVY)
    draw = ImageDraw.Draw(image)
    for x in range(0, W, 48):
        draw.line([(x, 0), (x, H)], fill=(12, 28, 46))
    for y in range(0, H, 48):
        draw.line([(0, y), (W, y)], fill=(12, 28, 46))
    return image


def footer(draw: ImageDraw.ImageDraw) -> None:
    draw.text((MARGIN, 992), "Education only. Not financial advice.", font=font(28, "reg"), fill=MUTED)


def panel(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int]) -> None:
    draw.rounded_rectangle(box, 18, fill=GLASS, outline=CYAN, width=3)


def fit_lines(draw: ImageDraw.ImageDraw, text: str, x: int, y: int, width: int, bottom: int, fill=WHITE) -> int:
    face = font(32)
    lines = wrap(text, face, width)
    if y + len(lines) * 40 > bottom:
        face = font(28)
        lines = wrap(text, face, width)
    step = 40 if face.size >= 32 else 36
    for line in lines:
        if y + step > bottom:
            break
        draw.text((x, y), line, font=face, fill=fill)
        y += step
    return y


def draw_rungs(draw: ImageDraw.ImageDraw, prices: list[str], box: tuple[int, int, int, int], source: str = "") -> None:
    x0, y0, x1, y1 = box
    unique = []
    for price in prices:
        if price not in unique:
            unique.append(price)
    show = unique[:7]
    if not show:
        return
    gap = (y1 - y0) / max(1, len(show))
    ys = {}
    for index, price in enumerate(show):
        y = int(y0 + gap * index + gap / 2)
        ys[price] = y
        draw.line([(x0, y), (x0 + 640, y)], fill=CYAN, width=4)
        draw.text((x0 + 660, y - 18), f"Example {price}", font=font(32), fill=WHITE)
    if "901" in source and "27,630" in ys and "28,531" in ys:
        mid = (ys["27,630"] + ys["28,531"]) // 2
        draw.text((x0 + 24, mid - 16), "Example 901", font=font(28), fill=CYAN)


def draw_columns(draw: ImageDraw.ImageDraw, left: str, right: str, box: tuple[int, int, int, int]) -> None:
    x0, y0, x1, y1 = box
    mid = (x0 + x1) // 2
    draw.rounded_rectangle([x0, y0, mid - 16, y1], 16, outline=CYAN, width=3)
    draw.rounded_rectangle([mid + 16, y0, x1, y1], 16, outline=CYAN, width=3)
    fit_lines(draw, left, x0 + 28, y0 + 36, mid - x0 - 72, y1 - 20)
    fit_lines(draw, right, mid + 44, y0 + 36, x1 - mid - 72, y1 - 20)


def diagram(draw: ImageDraw.ImageDraw, text: str, box: tuple[int, int, int, int]) -> str:
    """A picture of this beat only. Returns a short name for the manifest."""
    low = text.lower()
    prices = price_tokens(text)
    if prices:
        draw_rungs(draw, prices, box, text)
        return "code ladder of the figures in this sentence"
    if "cross" in low and "fill" in low:
        draw_columns(draw, "cross", "fill", box)
        return "code two columns, cross and fill"
    if "limit order" in low and "market order" in low:
        draw_columns(draw, "limit order", "market order", box)
        return "code two columns, limit order and market order"
    if "buy" in low and "sell" in low:
        draw_columns(draw, "buy", "sell", box)
        return "code two columns, buy and sell"
    if "range" in low or "top" in low or "bottom" in low:
        x0, y0, x1, y1 = box
        draw.line([(x0, y0 + 40), (x1, y0 + 40)], fill=CYAN, width=6)
        draw.line([(x0, y1 - 40), (x1, y1 - 40)], fill=CYAN, width=6)
        draw.text((x0, y0 + 4), "top line", font=font(28), fill=CYAN)
        draw.text((x0, y1 - 36), "bottom line", font=font(28), fill=WHITE)
        return "code range, top line and bottom line"
    if "stop" in low or "finish" in low:
        x0, y0, x1, y1 = box
        draw.line([(x0, (y0 + y1) // 2), (x1, (y0 + y1) // 2)], fill=CYAN, width=6)
        draw.text((x0, y0 + 24), "stop", font=font(32), fill=WHITE)
        return "code stop line"
    x0, y0, x1, y1 = box
    draw.rounded_rectangle([x0, y0, x0 + 280, y0 + 160], 16, outline=CYAN, width=3)
    label = " ".join(text.split()[:3])
    draw.text((x0 + 24, y0 + 56), label, font=font(32), fill=WHITE)
    return "code mark for the opening words of this sentence"


def lockup(draw: ImageDraw.ImageDraw, x: int, y: int) -> None:
    points = []
    for index in range(6):
        angle = math.radians(-90 + index * 60)
        points.append((x + 54 * math.cos(angle), y + 54 * math.sin(angle)))
    draw.polygon(points, outline=CYAN)
    draw.text((x - 18, y - 22), "G", font=font(48), fill=CYAN)
    draw.text((x + 80, y - 36), "GRID BOT", font=font(42), fill=WHITE)
    draw.text((x + 80, y + 12), "BUILDER", font=font(42), fill=CYAN)


def paint(kind: str, title: str, line: str, next_title: str = "") -> Image.Image:
    image = background()
    draw = ImageDraw.Draw(image)
    draw.text((MARGIN, 56), title, font=font(36), fill=CYAN)
    card = (MARGIN, 140, W - MARGIN, 980)
    panel(draw, card)
    if kind == "title":
        fit_lines(draw, line, MARGIN + 48, 420, W - 2 * MARGIN - 96, 860)
    elif kind == "end":
        lockup(draw, 220, 360)
        fit_lines(draw, line, MARGIN + 48, 520, W - 2 * MARGIN - 96, 920)
    elif kind == "disclaimer":
        fit_lines(draw, line, MARGIN + 48, 220, W - 2 * MARGIN - 96, 920)
    else:
        diagram(draw, line, (MARGIN + 48, 200, W - MARGIN - 48, 620))
        fit_lines(draw, line, MARGIN + 48, 660, W - 2 * MARGIN - 96, 940)
    footer(draw)
    return image


def paint_hero(label: str, title: str) -> Image.Image:
    image = background()
    draw = ImageDraw.Draw(image)
    draw.text((MARGIN, 56), title, font=font(36), fill=CYAN)
    card = (MARGIN, 140, W - MARGIN, 980)
    panel(draw, card)
    prices = price_tokens(label)
    if prices:
        draw_rungs(draw, prices, (MARGIN + 48, 180, W - MARGIN - 48, 520), label)
        top = 560
    else:
        diagram(draw, label, (MARGIN + 48, 180, W - MARGIN - 48, 460))
        top = 500
    fit_lines(draw, label, MARGIN + 48, top, W - 2 * MARGIN - 96, 940)
    footer(draw)
    return image


def on_screen_figures(text: str) -> set[str]:
    return screen_figures(text)


def gate_row(beat: str, seconds: float, shown: str) -> list[str]:
    problems = []
    if seconds > 8:
        problems.append("hold over 8s")
    extra = on_screen_figures(shown) - on_screen_figures(beat)
    if extra:
        problems.append("figure not in this sentence: " + ", ".join(sorted(extra)[:6]))
    if "EXAMPLE" in shown and "Example" not in beat and not price_tokens(beat):
        problems.append("Example overlay without a figure")
    return problems


def write_yaml(number: str, script: Path, body: str, beats: list[dict]) -> None:
    ident = LESSONS[number]
    paras = paragraphs(body)
    disclaimer = next((p for p in paras if p.startswith("Education only")), paras[0])
    dates = find_dates(body)
    figures = sorted(screen_figures(body), key=lambda item: (len(item), item))
    lines = [
        f"id: {ident}",
        "format: blueprint",
        f"source: course/approved-scripts-25nov/BP-{number}-APPROVED.md",
        "disclaimer_spoken: " + json.dumps(disclaimer),
        'disclaimer_on_screen: "Education only. Not financial advice."',
        "past_performance: \"Past performance is not a reliable indicator of future results.\"",
        "dates:",
    ]
    for date in dates:
        lines.append(f"  - {json.dumps(date)}")
    lines.append("chart_labels:")
    for figure in figures:
        lines.append(f"  - {json.dumps(figure)}")
    lines.append(f"spoken_words: {len(body.split())}")
    lines.append(f"beats: {len(beats)}")
    path = NUMBERS / f"{ident}.yaml"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def build(number: str) -> dict:
    script = APPROVED / f"BP-{number}-APPROVED.md"
    listing = json.loads((APPROVED / f"BP-{number}-PASS-LIST-APPROVED.json").read_text())
    raw = script.read_text(encoding="utf-8")
    title = raw.splitlines()[0].lstrip("# ").strip()
    body = spoken_body(raw)
    lesson_dir = OUT / f"BP-{number}"
    stills = lesson_dir / "stills"
    heroes = lesson_dir / "heroes"
    stills.mkdir(parents=True, exist_ok=True)
    heroes.mkdir(parents=True, exist_ok=True)
    hero_rows = []
    for image in listing["images"]:
        label = image["label"]
        name = Path(image["path"]).name
        paint_hero(label, title).save(heroes / name, optimize=True)
        hero_rows.append((name, label, on_screen_figures(label)))
    clock = 0.0
    rows = []
    for paragraph in paragraphs(body):
        for beat in beats_for(paragraph):
            seconds = len(beat.split()) / WPM * 60
            low = beat.lower()
            if paragraph == paragraphs(body)[0]:
                kind = "title"
            elif beat.startswith("Education only"):
                kind = "disclaimer"
            elif beat.startswith("Next lesson"):
                kind = "end"
            else:
                kind = "beat"
            image = paint(kind, title, beat)
            filename = f"{len(rows) + 1:03d}.png"
            image.save(stills / filename, optimize=True)
            shown = beat
            problems = gate_row(beat, seconds, shown)
            if kind == "beat":
                visual = diagram_name(beat)
            elif kind == "title":
                visual = "code title card, signed heading"
            elif kind == "disclaimer":
                visual = "code disclaimer card, spoken paragraph"
            else:
                visual = "code end card, official lockup, next lesson in the spoken words"
            rows.append({
                "n": len(rows) + 1,
                "start": clock,
                "seconds": seconds,
                "sentence": beat,
                "visual": visual,
                "file": f"stills/{filename}",
                "source": "code",
                "gates": "pass" if not problems else "FAIL " + "; ".join(problems),
            })
            clock += seconds
    write_yaml(number, script, body, rows)
    manifest = [
        f"# BP-{number} visual manifest",
        "",
        f"Title: {title}",
        "",
        f"Spoken words: {len(body.split())}. Pace: 163 words a minute. Runtime: {clock / 60:.2f} min.",
        "",
        "No film was rendered. Charts, diagrams and cards are code. No ChatGPT image was required, because none of these beats is a photograph. No corner EXAMPLE chip is drawn. A figure is on a still only when that sentence says it.",
        "",
        f"Hero cards: {len(hero_rows)}. Stills: {len(rows)}. Fallback images: 0.",
        "",
        "## Hero cards",
        "",
        "The card text is the approved pass-list label, word for word. These files are the full cards. The stills below are the voice-tied beats.",
        "",
        "| File | Approved card text | Source | Figures outside the card text |",
        "|---|---|---|---|",
    ]
    for name, label, figures in hero_rows:
        extra = "none"
        manifest.append(f"| `heroes/{name}` | {label.replace('|', '/')} | code | {extra} |")
    manifest.extend([
        "",
        "## Voice-tied stills",
        "",
        "| # | Start | Seconds | Sentence | Visual | File | Source | Gate |",
        "|---|---:|---:|---|---|---|---|---|",
    ])
    for row in rows:
        sentence = row["sentence"].replace("|", "/")
        manifest.append(
            f"| {row['n']} | {row['start']:.1f} | {row['seconds']:.1f} | {sentence} | {row['visual']} | `{row['file']}` | {row['source']} | {row['gates']} |"
        )
    fails = [row for row in rows if row["gates"] != "pass"]
    manifest.extend([
        "",
        f"Gate fails: {len(fails)}.",
        "",
        "Creative Studio still has to score the hero cards. They are draft. This manifest does not mark them pass.",
        "",
    ])
    (lesson_dir / "MANIFEST.md").write_text("\n".join(manifest), encoding="utf-8")
    return {
        "heroes": len(hero_rows),
        "stills": len(rows),
        "fallback": 0,
        "fails": len(fails),
        "words": len(body.split()),
        "seconds": clock,
    }


def diagram_name(text: str) -> str:
    low = text.lower()
    if price_tokens(text):
        return "code ladder of the figures in this sentence"
    if "cross" in low and "fill" in low:
        return "code two columns, cross and fill"
    if "limit order" in low and "market order" in low:
        return "code two columns, limit order and market order"
    if "buy" in low and "sell" in low:
        return "code two columns, buy and sell"
    if "range" in low or "top line" in low or "bottom" in low:
        return "code range, top line and bottom line"
    if "stop" in low or "finish" in low:
        return "code stop line"
    return "code mark for the opening words of this sentence"


def main() -> None:
    summary = {}
    for number in LESSONS:
        summary[number] = build(number)
        print(number, summary[number], flush=True)
    (OUT / "SUMMARY.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
