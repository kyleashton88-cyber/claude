"""On-screen text: disclaimer, brands, and safe margins.

Brand and margin scans use tesseract. If it is missing, those checks fail.
They are never treated as a pass.
"""

from __future__ import annotations

import re
import shutil
import subprocess
from dataclasses import dataclass

from .profiles import Profile

# Exchange and channel names the old frame scan already refused.
BRANDS = re.compile(
    r"\b("
    r"bybit|binance|pionex|coinbase|okx|kucoin|kraken|bitget|"
    r"bitfinex|mexc|gemini|crypto\.com"
    r")\b|market\s+pros|\bgate\.io\b|\bhtx\b",
    re.I,
)

DISCLAIMER_NOTE = "Education, not financial advice."


def has_disclaimer(text: str) -> bool:
    low = text.lower()
    return "educat" in low and "not financial advice" in low


def find_brands(text: str) -> list[str]:
    return sorted({match.group(0).lower() for match in BRANDS.finditer(text)})


def tesseract_path() -> str | None:
    return shutil.which("tesseract")


@dataclass(frozen=True)
class WordBox:
    text: str
    left: int
    top: int
    width: int
    height: int
    conf: float


def parse_tsv(tsv: str) -> list[WordBox]:
    rows: list[WordBox] = []
    lines = tsv.splitlines()
    if not lines:
        return rows
    header = lines[0].split("\t")
    try:
        i_text = header.index("text")
        i_left = header.index("left")
        i_top = header.index("top")
        i_width = header.index("width")
        i_height = header.index("height")
        i_conf = header.index("conf")
    except ValueError:
        return rows
    for line in lines[1:]:
        parts = line.split("\t")
        if len(parts) <= i_text:
            continue
        text = parts[i_text].strip()
        if len(text) < 2:
            continue
        try:
            conf = float(parts[i_conf])
            box = WordBox(
                text=text,
                left=int(float(parts[i_left])),
                top=int(float(parts[i_top])),
                width=int(float(parts[i_width])),
                height=int(float(parts[i_height])),
                conf=conf,
            )
        except ValueError:
            continue
        if box.conf < 50 or box.width <= 0 or box.height <= 0:
            continue
        rows.append(box)
    return rows


def read_frame(image: str) -> tuple[str, list[WordBox]]:
    """OCR one image. Raises if tesseract is missing or the process fails."""
    binary = tesseract_path()
    if not binary:
        raise RuntimeError(
            "tesseract is not installed. Brand, exchange-name, and safe-margin "
            "checks cannot run. They are not skipped."
        )
    proc = subprocess.run(
        [binary, image, "stdout", "--psm", "6", "tsv"],
        capture_output=True,
        text=True,
        errors="replace",
    )
    if proc.returncode != 0:
        tail = (proc.stderr or proc.stdout or "")[-500:]
        raise RuntimeError(f"tesseract failed on {image}: {tail}")
    boxes = parse_tsv(proc.stdout or "")
    text = " ".join(box.text for box in boxes)
    return text, boxes


def margin_hits(boxes: list[WordBox], width: int, height: int, profile: Profile) -> list[str]:
    inset_x = width * profile.margin_frac
    inset_y = height * profile.margin_frac
    hits: list[str] = []
    for box in boxes:
        right = box.left + box.width
        bottom = box.top + box.height
        if (
            box.left < inset_x
            or box.top < inset_y
            or right > width - inset_x
            or bottom > height - inset_y
        ):
            hits.append(f"{box.text!r} at ({box.left},{box.top})")
    return hits
