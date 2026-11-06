"""Shared still queue: Elite el-05..el-11, then the rest of Elite, then Blueprint, then On-Chain Operator."""

from __future__ import annotations


def priority(lesson_id: str) -> tuple:
    parts = lesson_id.split("-")
    if lesson_id.startswith("el-") and len(parts) > 1 and parts[1].isdigit():
        n = int(parts[1])
        band = 0 if 5 <= n <= 11 else 1
        return (band, n, lesson_id)
    if lesson_id.startswith("bp-"):
        return (2, 0, lesson_id)
    return (3, 0, lesson_id)


def ordered_requests(requests: list[dict]) -> list[dict]:
    return sorted(requests, key=lambda item: (*priority(str(item.get("lesson") or "")), int(item.get("beat") or 0), str(item.get("id") or "")))
