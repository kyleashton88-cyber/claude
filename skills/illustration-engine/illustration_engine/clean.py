"""Keep drawn text free of contact details and venue names."""

from __future__ import annotations

import re

from .policy import EXCHANGE, RefusedPrompt

EMAIL = re.compile(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}")
PHONE = re.compile(r"\b(?:\+?\d[\d\s().-]{7,}\d)\b")
URL = re.compile(r"https?://\S+|www\.\S+", re.I)


class UnsafeText(ValueError):
    pass


def assert_drawable(text: str) -> str:
    """Refuse contact details and venue names. Do not delete them quietly."""
    raw = text or ""
    if EMAIL.search(raw) or URL.search(raw) or PHONE.search(raw):
        raise UnsafeText("refusing to draw contact details")
    if EXCHANGE.search(raw):
        raise RefusedPrompt(
            "refusing: exchange or brand name reached the drawing step. "
            "It was not removed."
        )
    return raw
