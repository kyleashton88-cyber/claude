"""Shared helpers for the drawers."""

from __future__ import annotations


def take_headline(canvas, params: dict, default: str) -> None:
    canvas.headline(str(params.get("headline") or default))


def sentence_case(text: str) -> str:
    words = [word for word in str(text).replace("_", " ").split() if word][:3]
    return " ".join(word[:1].upper() + word[1:].lower() for word in words)


def labels_or(params: dict, defaults: list[str]) -> list[str]:
    raw = params.get("labels") or defaults
    out: list[str] = []
    for item in list(raw) + list(defaults):
        label = sentence_case(item)
        if label and label not in out:
            out.append(label)
        if len(out) == 5:
            break
    while len(out) < 2 and defaults:
        label = sentence_case(defaults[len(out) % len(defaults)])
        if label not in out:
            out.append(label)
        else:
            break
    return out[:5]


def fnum(params: dict, key: str, default: float) -> float:
    try:
        return float(params.get(key, default))
    except (TypeError, ValueError):
        return float(default)


def inum(params: dict, key: str, default: int) -> int:
    try:
        return int(params.get(key, default))
    except (TypeError, ValueError):
        return int(default)
