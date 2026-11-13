"""What the engine will draw, and what it refuses.

A refused prompt stops. It is not redrawn as a generic plate.
"""

from __future__ import annotations

import re

from .spec import FALLBACK_TYPES, Spec

CONTACT = re.compile(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}|https?://|www\.", re.I)
PHOTO = re.compile(
    r"\b(photoreal(?:istic)?|photograph|photo of|portrait of|selfie|real person|real people)\b",
    re.I,
)
NAMED = re.compile(r"\b(stewart(?:\s+crown)?)\b", re.I)
EXCHANGE = re.compile(
    r"\b(pionex|binance|bybit|coinbase|okx|kraken|ftx|kucoin|gemini|bitfinex|"
    r"bitstamp|huobi|htx|deribit|chatgpt|openai|midjourney)\b",
    re.I,
)


class RefusedPrompt(RuntimeError):
    """The prompt is outside what this engine can truthfully draw."""


def _replace_exchange(text: str) -> tuple[str, list[str]]:
    found = []

    def swap(match: re.Match) -> str:
        found.append(match.group(0))
        return "exchange"

    return EXCHANGE.sub(swap, text), found


def screen(text: str, *, allow_generic: bool = False) -> tuple[str, list[str]]:
    """Return the text to draw, and any names that were rewritten on purpose."""
    raw = text or ""
    if CONTACT.search(raw):
        raise RefusedPrompt("refusing: contact details in the prompt")
    if PHOTO.search(raw) or NAMED.search(raw):
        raise RefusedPrompt(
            "refusing: this engine draws diagrams. "
            "It will not draw a photograph, a real person, or a named person."
        )
    names = EXCHANGE.findall(raw)
    if not names:
        return raw, []
    shown = ", ".join(sorted({name.upper() for name in names}))
    if not allow_generic:
        raise RefusedPrompt(
            f"refusing: exchange or brand name in the prompt: {shown}. "
            "Pass --allow-generic to draw the word exchange instead."
        )
    rewritten, found = _replace_exchange(raw)
    return rewritten, found


def screen_value(value, *, allow_generic: bool = False):
    notes: list[str] = []
    if isinstance(value, str):
        cleaned, found = screen(value, allow_generic=allow_generic)
        return cleaned, found
    if isinstance(value, list):
        out = []
        for item in value:
            cleaned, found = screen_value(item, allow_generic=allow_generic)
            notes.extend(found)
            out.append(cleaned)
        return out, notes
    if isinstance(value, dict):
        out = {}
        for key, item in value.items():
            cleaned, found = screen_value(item, allow_generic=allow_generic)
            notes.extend(found)
            out[key] = cleaned
        return out, notes
    return value, notes


def enforce_mode(spec: Spec, *, fallback: bool) -> Spec:
    if fallback and spec.type not in FALLBACK_TYPES:
        raise RefusedPrompt(
            f"refusing: {spec.type} is outside --fallback. "
            "That mode draws candles, grid ladders, liquidation, ranges, and beginner diagrams. "
            "Mascot, cover, and branded plates stay available without --fallback."
        )
    spec.params["mode"] = "fallback" if fallback else "normal"
    return spec
