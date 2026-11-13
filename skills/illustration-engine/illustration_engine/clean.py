"""Keep drawn text free of contact details and venue names."""

from __future__ import annotations

import re

EMAIL = re.compile(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}")
PHONE = re.compile(r"\b(?:\+?\d[\d\s().-]{7,}\d)\b")
URL = re.compile(r"https?://\S+|www\.\S+", re.I)
BANNED = re.compile(
    r"\b(binance|coinbase|bybit|okx|kraken|ftx|chatgpt|openai|midjourney|"
    r"gmail|protonmail)\b",
    re.I,
)


class UnsafeText(ValueError):
    pass


def scrub(text: str) -> str:
    """Drop contact details and venue names. Keep teaching words and figures."""
    cleaned = EMAIL.sub("", text or "")
    cleaned = URL.sub("", cleaned)
    cleaned = PHONE.sub("", cleaned)
    cleaned = BANNED.sub("", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned).strip(" -_,;:")
    return cleaned


def assert_drawable(text: str) -> str:
    """Return scrubbed text, and refuse leftovers that still look like contact data."""
    cleaned = scrub(text)
    if EMAIL.search(cleaned) or URL.search(cleaned):
        raise UnsafeText("refusing to draw contact details")
    return cleaned
