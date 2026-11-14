#!/usr/bin/env python3
"""A fake screen with a wallet and a key, then the blurred still."""

from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))

from screen_demo.blur import blur_image, qa_image  # noqa: E402

FONT = HERE.parent / "templates" / "assets" / "fonts" / "Inter-Bold.ttf"


def main() -> None:
    out = HERE / "test-outputs"
    out.mkdir(parents=True, exist_ok=True)
    image = Image.new("RGB", (960, 540), (0, 8, 27))
    draw = ImageDraw.Draw(image)
    face = ImageFont.truetype(str(FONT), 28)
    draw.text((48, 60), "Practice screen", fill=(244, 248, 252), font=face)
    draw.text((48, 140), "Wallet 0x1111111111111111111111111111111111111111", fill=(244, 248, 252), font=face)
    draw.text((48, 200), "Key sk-TESTKEYONLY000000", fill=(244, 248, 252), font=face)
    draw.text((48, 260), "Balance $4200", fill=(244, 248, 252), font=face)
    draw.text((48, 320), "Account 123456789012", fill=(244, 248, 252), font=face)
    raw = out / "before.png"
    image.save(raw)
    blurred = out / "after.png"
    blur_image(raw, blurred)
    problems = qa_image(blurred)
    (out / "qa.txt").write_text("PASS\n" if not problems else "FAIL\n" + "\n".join(problems) + "\n", encoding="utf-8")
    if problems:
        raise SystemExit("blur left a readable secret: " + "; ".join(problems))


if __name__ == "__main__":
    main()
