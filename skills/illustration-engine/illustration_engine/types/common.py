"""Shared helpers for the drawers."""

from __future__ import annotations


def take_headline(canvas, params: dict, default: str) -> None:
    canvas.headline(str(params.get("headline") or default))


def labels_or(params: dict, defaults: list[str]) -> list[str]:
    raw = params.get("labels") or defaults
    out: list[str] = []
    for item in raw:
        words = str(item).upper().split()[:3]
        if not words:
            continue
        label = " ".join(words)
        if label not in out:
            out.append(label)
        if len(out) == 5:
            break
    if len(out) < 2:
        for item in defaults:
            if item not in out:
                out.append(item)
            if len(out) == 2:
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
