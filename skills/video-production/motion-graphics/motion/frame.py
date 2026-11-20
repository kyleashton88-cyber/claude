"""A 1920×1080 stage. Drawing commands are vector primitives, rasterized once at final size."""

from __future__ import annotations

from functools import lru_cache

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from lib.brand import AQUA, AQUA_LT, DISCLAIMER, H, MUTED, TEXT, W, font_path
from lib.easing import clamp

_WEIGHT = {"bold": "bold", "regular": "regular", "medium": "medium", "mono": "mono"}


@lru_cache(maxsize=64)
def font(size: int, weight: str = "regular") -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(font_path(_WEIGHT.get(weight, "regular")), size)


@lru_cache(maxsize=1)
def background() -> Image.Image:
    y = np.linspace(0.0, 1.0, H, dtype=np.float32)[:, None, None]
    x = np.linspace(0.0, 1.0, W, dtype=np.float32)[None, :, None]
    top = np.array([24, 58, 96], dtype=np.float32)
    bot = np.array([8, 20, 36], dtype=np.float32)
    col = bot * y + top * (1.0 - y)
    # A cool lift in the upper right, so the field is not a flat fill.
    lift = np.clip(1.0 - np.hypot(x - 0.92, (y - 0.08) * 1.4), 0, 1) ** 2
    col = col + lift * np.array([18, 36, 28], dtype=np.float32)
    rgb = np.clip(col, 0, 255).astype(np.uint8)
    img = Image.fromarray(rgb, "RGB")
    draw = ImageDraw.Draw(img)
    for gx in range(0, W, 48):
        draw.line([(gx, 0), (gx, H)], fill=(16, 40, 64), width=1)
    for gy in range(0, H, 48):
        draw.line([(0, gy), (W, gy)], fill=(16, 40, 64), width=1)
    return img


class Stage:
    def __init__(self, base: Image.Image, t: float, duration: float, global_t: float, total: float):
        self.im = base.copy()
        self.draw = ImageDraw.Draw(self.im)
        self.t = t
        self.duration = max(duration, 0.001)
        self.global_t = global_t
        self.total = max(total, 0.001)
        self.u = clamp(t / self.duration)

    def refresh(self) -> None:
        self.draw = ImageDraw.Draw(self.im)

    def paste(self, overlay: Image.Image, xy: tuple[int, int]) -> None:
        self.im.paste(overlay, xy, overlay)
        self.refresh()

    def panel(
        self,
        box: tuple[int, int, int, int],
        fill: tuple[int, int, int, int],
        radius: int = 18,
        outline: tuple[int, int, int, int] | None = None,
        width: int = 2,
    ) -> None:
        x0, y0, x1, y1 = [int(v) for v in box]
        w, h = max(1, x1 - x0), max(1, y1 - y0)
        ov = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        d = ImageDraw.Draw(ov)
        d.rounded_rectangle([0, 0, w - 1, h - 1], radius=radius, fill=fill, outline=outline, width=width)
        self.paste(ov, (x0, y0))

    def text(
        self,
        xy: tuple[float, float],
        text: str,
        size: int,
        fill: tuple[int, int, int] = TEXT,
        weight: str = "regular",
        anchor: str = "lt",
    ) -> None:
        self.draw.text(xy, text, font=font(size, weight), fill=fill, anchor=anchor)

    def width(self, text: str, size: int, weight: str = "regular") -> float:
        return font(size, weight).getlength(text)

    def line(self, a, b, fill, width: int = 2) -> None:
        self.draw.line([a, b], fill=fill, width=width)

    def finish(self, title: str | None, caption: str | None) -> None:
        p = clamp(self.global_t / self.total)
        self.draw.rectangle([0, 0, int(W * p), 6], fill=AQUA_LT)
        if title:
            self.text((72, 28), title, 32, TEXT, weight="bold")
            rule = self.width(title, 32, "bold")
            self.draw.rectangle([72, 74, 72 + int(min(rule, 280) * 0.45), 78], fill=AQUA)
        if caption:
            bar = Image.new("RGBA", (W, 84), (0, 0, 0, 0))
            d = ImageDraw.Draw(bar)
            d.rectangle([0, 0, W, 84], fill=(6, 16, 30, 228))
            d.rectangle([0, 0, 8, 84], fill=(*AQUA, 255))
            self.paste(bar, (0, 968))
            self.text((36, 1010), caption, 28, TEXT, weight="medium", anchor="lm")
        self.text((W - 64, 1056), DISCLAIMER, 16, MUTED, weight="regular", anchor="rm")
