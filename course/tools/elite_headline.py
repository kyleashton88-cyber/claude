"""Place an Elite headline on the measured template.

Creative Studio, 6 Nov 2026: glyph top at y=110, capital height about 159,
and no diagram or label below y=870. The first word is white. The second
word is teal #14E0C8. Rows above the headline and below y=870 stay background.
"""

from __future__ import annotations

from PIL import Image, ImageDraw, ImageFilter, ImageFont

HEADLINE_TOP = 110
CAP_HEIGHT = 159
CONTENT_MAX_Y = 870
CONTENT_TOP = HEADLINE_TOP + CAP_HEIGHT + 24  # 293
FRAME = (1536, 1024)
TEAL = (0x14, 0xE0, 0xC8)
WHITE = (255, 255, 255)
LEFT = 72
FONT_PATH = "/usr/share/fonts/truetype/macos/Inter-Bold.ttf"

TEMPLATE = (
    "Elite headline template: one line, top-left, outside any card. "
    "Glyph top at y=110. Capital height about 159 pixels. "
    "First word white, second word teal #14E0C8. "
    "Rows 0 through 109 are background only. "
    "Diagrams, labels and every other mark end at or above y=870. "
    "Rows 871 through 1023 are background only."
)


def _font(size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_PATH, size)


def _cap_size(cap: int = CAP_HEIGHT - 4) -> int:
    lo, hi = 80, 420
    best = 210
    while lo <= hi:
        mid = (lo + hi) // 2
        box = _font(mid).getbbox("H")
        height = box[3] - box[1]
        best = mid
        if height == cap:
            return mid
        if height < cap:
            lo = mid + 1
        else:
            hi = mid - 1
    return best


def _word(text: str, fill: tuple[int, int, int]) -> Image.Image:
    size = _cap_size()
    font = _font(size)
    box = font.getbbox(text)
    layer = Image.new("RGBA", (box[2] - box[0] + 4, box[3] - box[1] + 4), (0, 0, 0, 0))
    ImageDraw.Draw(layer).text((-box[0], -box[1]), text, font=font, fill=fill + (255,))
    ink = layer.getbbox()
    return layer.crop(ink) if ink else layer


def _text_layer(first: str, second: str) -> Image.Image:
    """Transparent layer. Glyph top is row 0. A gap stays between the two words."""
    left = _word(first, WHITE)
    right = _word(second, TEAL)
    gap = 56
    max_w = FRAME[0] - LEFT - 48
    spare = max_w - gap
    if left.size[0] + right.size[0] > spare:
        scale = spare / (left.size[0] + right.size[0])
        left = left.resize((max(1, int(left.size[0] * scale)), left.size[1]), Image.Resampling.LANCZOS)
        right = right.resize((max(1, int(right.size[0] * scale)), right.size[1]), Image.Resampling.LANCZOS)
    layer = Image.new("RGBA", (left.size[0] + gap + right.size[0], max(left.size[1], right.size[1])), (0, 0, 0, 0))
    layer.alpha_composite(left, (0, 0))
    layer.alpha_composite(right, (left.size[0] + gap, 0))
    return layer


def measure(image: Image.Image) -> dict:
    """Ink bounds. A flat navy field is background, not a headline."""
    import numpy as np

    arr = np.asarray(image.convert("RGB"))
    lum = arr.mean(axis=2)
    samples = np.concatenate([
        lum[:24, :24].ravel(),
        lum[:24, -24:].ravel(),
        lum[-24:, :24].ravel(),
        lum[-24:, -24:].ravel(),
    ])
    corner = float(np.median(samples))
    red = arr[:, :, 0].astype(np.int16)
    green = arr[:, :, 1].astype(np.int16)
    hot = (lum > max(corner + 24, 46)) | ((green > red + 22) & (green > max(corner + 24, 48)) & (green > 55))
    counts = hot[:, ::2].sum(axis=1)
    ys = [int(y) for y, count in enumerate(counts) if count > 6]
    if not ys:
        return {"headline_top": None, "cap": None, "content_bottom": None}
    top = ys[0]
    end = top
    quiet = 0
    for y in range(top, min(arr.shape[0], top + 280)):
        if counts[y] > 6:
            end = y
            quiet = 0
        else:
            quiet += 1
            if quiet >= 8 and end > top + 20:
                break
    return {"headline_top": top, "cap": end - top + 1, "content_bottom": ys[-1]}


def _erase_top_block(image: Image.Image) -> Image.Image:
    """Remove the existing headline so the template line can replace it.

    Glyphs are near-white or saturated teal. Faint grid and card glow stay,
    and the block stops at the first quiet gap so a card underneath is kept.
    """
    import numpy as np

    rgb = image.convert("RGB")
    arr = np.asarray(rgb).copy()
    height, width = arr.shape[:2]
    lum = arr.mean(axis=2)
    red = arr[:, :, 0].astype(np.int16)
    green = arr[:, :, 1].astype(np.int16)
    blue = arr[:, :, 2].astype(np.int16)
    glyph = (lum > 70) | ((green > red + 28) & (green > 90) & (blue > 70))
    counts = glyph[:500].sum(axis=1)
    start = next((int(y) for y, count in enumerate(counts) if count > 12), None)
    # A diagram that starts below the headline zone is content, not a title.
    if start is None or start > 300:
        return rgb
    # A diagram is a wide bright band. A second headline line is narrower, so
    # it gets painted out with the first line instead of stopping the erase.
    diagram = None
    for y in range(start + 40, min(height - 1, 760)):
        xs = np.where(lum[y] > 45)[0]
        if len(xs) > 40 and int(xs[-1] - xs[0]) > 760:
            diagram = int(y)
            break
    y1 = max(0, start - 8)
    y2 = (diagram - 8) if diagram else min(height, start + 180)
    if y2 <= y1 + 10:
        return rgb
    # Left margin only. A full-width sample picks up chip glow and paints a bright band.
    above = arr[max(0, y1 - 24): y1, :48]
    below = arr[y2: min(height, y2 + 8), :48]
    top_colour = np.median(above.reshape(-1, 3), axis=0) if above.size else arr[0, 0]
    bottom_colour = np.median(below.reshape(-1, 3), axis=0) if below.size else top_colour
    span = max(1, y2 - y1 - 1)
    for i, y in enumerate(range(y1, y2)):
        blend = i / span
        arr[y] = (top_colour * (1 - blend) + bottom_colour * blend).astype(np.uint8)
    return Image.fromarray(arr)


def _fit_content(image: Image.Image) -> Image.Image:
    """Keep diagrams under the headline and at or above y=870."""
    rgb = image.convert("RGB")
    if rgb.size != FRAME:
        rgb = rgb.resize(FRAME, Image.Resampling.LANCZOS)
    pixels = rgb.load()
    width, height = rgb.size
    ys = []
    xs = []
    # Start above the content window so a diagram that collides with the
    # headline is moved down instead of being left underneath the type.
    for y in range(200, height):
        for x in range(0, width, 3):
            r, g, b = pixels[x, y]
            if r + g + b > 170 or (g > r + 24 and g > 80):
                ys.append(y)
                xs.append(x)
                break
    if not ys:
        return rgb
    top, bottom = ys[0], ys[-1]
    # A few pixels of glow above the window is not a collision.
    if top >= CONTENT_TOP - 16 and bottom <= CONTENT_MAX_Y:
        return rgb
    # Horizontal extent of the content, sampled.
    left, right = width, 0
    for y in range(top, bottom + 1, 4):
        for x in range(width):
            r, g, b = pixels[x, y]
            if r + g + b > 100 or (g > r + 16 and g > 34):
                left = min(left, x)
                break
        for x in range(width - 1, -1, -1):
            r, g, b = pixels[x, y]
            if r + g + b > 100 or (g > r + 16 and g > 34):
                right = max(right, x)
                break
    if right <= left:
        return rgb
    crop = rgb.crop((max(0, left - 8), top, min(width, right + 9), bottom + 1))
    max_w = width - 120
    max_h = CONTENT_MAX_Y - CONTENT_TOP
    scale = min(max_w / crop.size[0], max_h / crop.size[1], 1.0)
    fitted = crop.resize(
        (max(1, int(crop.size[0] * scale)), max(1, int(crop.size[1] * scale))),
        Image.Resampling.LANCZOS,
    )
    canvas = rgb.copy()
    # Clear the old content rows, keeping the background colour of the top margin.
    bg = canvas.getpixel((8, 8))
    paint = ImageDraw.Draw(canvas)
    paint.rectangle((0, CONTENT_TOP - 8, width, height), fill=bg)
    x = (width - fitted.size[0]) // 2
    canvas.paste(fitted, (x, CONTENT_TOP))
    return canvas


def apply_headline(image: Image.Image, first: str, second: str) -> Image.Image:
    """Return a 1536x1024 still with the template headline composited on."""
    plate = _erase_top_block(image)
    plate = _fit_content(plate)
    layer = _text_layer(first.upper(), second.upper())
    plate = plate.convert("RGBA")
    plate.alpha_composite(layer, (LEFT, HEADLINE_TOP))
    return plate.convert("RGB")
