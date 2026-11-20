"""Find sensitive text and cover it. A second read must come back clean."""

from __future__ import annotations

import re
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

PATTERNS = (
    ("api-key", re.compile(r"\bsk-[A-Za-z0-9]{8,}\b")),
    ("wallet", re.compile(r"\b0x[a-fA-F0-9]{40}\b")),
    ("balance", re.compile(r"\b[Bb]alance\b[:\s]*\$[\d,]+(?:\.\d+)?")),
    ("account", re.compile(r"\b[Aa]ccount\b[:\s#]*\d{6,}\b")),
)


@dataclass(frozen=True)
class Hit:
    kind: str
    text: str
    box: tuple[int, int, int, int]


def pattern_hits(text: str) -> list[tuple[str, str]]:
    found = []
    for kind, pattern in PATTERNS:
        for match in pattern.finditer(text or ""):
            found.append((kind, match.group(0)))
    return found


def _tesseract(image: Path) -> tuple[str, list[dict]]:
    if shutil.which("tesseract") is None:
        raise RuntimeError("tesseract is not installed. The sensitive-text check was not skipped.")
    proc = subprocess.run(
        ["tesseract", str(image), "stdout", "--psm", "6", "tsv"],
        capture_output=True,
        text=True,
        errors="replace",
    )
    if proc.returncode != 0:
        raise RuntimeError((proc.stderr or "tesseract failed")[-400:])
    lines = (proc.stdout or "").splitlines()
    if not lines:
        return "", []
    header = lines[0].split("\t")
    words = []
    try:
        i_text, i_left, i_top = header.index("text"), header.index("left"), header.index("top")
        i_width, i_height, i_conf = header.index("width"), header.index("height"), header.index("conf")
    except ValueError:
        return proc.stdout or "", []
    for line in lines[1:]:
        parts = line.split("\t")
        if len(parts) <= i_text or not parts[i_text].strip():
            continue
        try:
            conf = float(parts[i_conf])
        except ValueError:
            continue
        if conf < 40:
            continue
        words.append({
            "text": parts[i_text],
            "left": int(float(parts[i_left])),
            "top": int(float(parts[i_top])),
            "width": int(float(parts[i_width])),
            "height": int(float(parts[i_height])),
        })
    return " ".join(word["text"] for word in words), words


def _boxes_for(text: str, words: list[dict]) -> list[Hit]:
    hits = []
    # Walk a growing window of words so a wallet split across tokens still matches.
    for start in range(len(words)):
        blob = ""
        for end in range(start, min(len(words), start + 8)):
            blob = (blob + " " + words[end]["text"]).strip()
            for kind, token in pattern_hits(blob):
                left = min(words[i]["left"] for i in range(start, end + 1))
                top = min(words[i]["top"] for i in range(start, end + 1))
                right = max(words[i]["left"] + words[i]["width"] for i in range(start, end + 1))
                bottom = max(words[i]["top"] + words[i]["height"] for i in range(start, end + 1))
                hits.append(Hit(kind, token, (left, top, right - left, bottom - top)))
    # Dedup by box.
    unique = []
    seen = set()
    for hit in hits:
        if hit.box in seen:
            continue
        seen.add(hit.box)
        unique.append(hit)
    return unique


def pixelate(image: Image.Image, box: tuple[int, int, int, int]) -> None:
    x, y, w, h = box
    x, y = max(0, x), max(0, y)
    w, h = max(1, w), max(1, h)
    crop = image.crop((x, y, min(image.width, x + w), min(image.height, y + h)))
    small = crop.resize((max(1, crop.width // 12), max(1, crop.height // 12)), Image.Resampling.BILINEAR)
    block = small.resize(crop.size, Image.Resampling.NEAREST).filter(ImageFilter.GaussianBlur(radius=1.2))
    image.paste(block, (x, y))


def blur_image(src: Path, dest: Path, manual: list[tuple[int, int, int, int]] | None = None) -> list[Hit]:
    text, words = _tesseract(src)
    hits = _boxes_for(text, words)
    image = Image.open(src).convert("RGB")
    draw = ImageDraw.Draw(image)
    for hit in hits:
        x, y, w, h = hit.box
        pixelate(image, (x - 4, y - 4, w + 8, h + 8))
    for box in manual or []:
        pixelate(image, box)
        draw.rectangle((box[0], box[1], box[0] + box[2], box[1] + box[3]), outline=(0, 212, 255))
    dest.parent.mkdir(parents=True, exist_ok=True)
    image.save(dest)
    return hits


def qa_image(path: Path) -> list[str]:
    text, _words = _tesseract(path)
    return [f"{kind}: {token}" for kind, token in pattern_hits(text)]
