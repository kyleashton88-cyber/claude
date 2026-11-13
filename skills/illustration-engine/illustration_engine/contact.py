"""Contact sheets and side-by-side plates."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw

from .fonts import pil_font
from .render import assert_safe_output


def _caption(draw: ImageDraw.ImageDraw, text: str, box, fill=(232, 241, 247)) -> None:
    font = pil_font("semi", 18)
    draw.text((box[0] + 8, box[1] + 8), text, fill=fill, font=font)


def contact_sheet(items: list[tuple[Path, str]], dest: Path, columns: int = 4, thumb: int = 360) -> Path:
    dest = assert_safe_output(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    if not items:
        raise SystemExit("no images for the contact sheet")
    pad = 16
    caption_h = 36
    cell_w = thumb
    cell_h = int(thumb * 1024 / 1536) + caption_h
    rows = (len(items) + columns - 1) // columns
    sheet = Image.new("RGB", (columns * cell_w + pad * (columns + 1), rows * cell_h + pad * (rows + 1)), (5, 10, 18))
    draw = ImageDraw.Draw(sheet)
    for index, (path, caption) in enumerate(items):
        image = Image.open(path).convert("RGB")
        image.thumbnail((cell_w, cell_h - caption_h), Image.Resampling.LANCZOS)
        col, row = index % columns, index // columns
        x = pad + col * (cell_w + pad)
        y = pad + row * (cell_h + pad)
        sheet.paste(image, (x, y))
        _caption(draw, caption[:42], (x, y + image.height, x + cell_w, y + cell_h))
    sheet.save(dest, "PNG", optimize=True)
    return dest


def side_by_side(original: Path, rendered: Path, dest: Path) -> Path:
    dest = assert_safe_output(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    left = Image.open(original).convert("RGB")
    right = Image.open(rendered).convert("RGB")
    height = 512
    def fit(image: Image.Image) -> Image.Image:
        width = max(1, int(image.width * height / image.height))
        return image.resize((width, height), Image.Resampling.LANCZOS)
    left, right = fit(left), fit(right)
    gap = 20
    cap = 40
    sheet = Image.new("RGB", (left.width + right.width + gap, height + cap), (5, 10, 18))
    sheet.paste(left, (0, cap))
    sheet.paste(right, (left.width + gap, cap))
    draw = ImageDraw.Draw(sheet)
    font = pil_font("bold", 22)
    draw.text((16, 8), "Original still", fill=(0, 212, 255), font=font)
    draw.text((left.width + gap + 16, 8), "In-house render", fill=(255, 255, 255), font=font)
    sheet.save(dest, "PNG", optimize=True)
    return dest
