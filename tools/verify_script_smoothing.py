#!/usr/bin/env python3
"""Check BP-04..BP-11 narration smoothing against the pre-edit scripts.

The baseline is commit fbb3f9c75981b80ac12ca1ba6b39f9d5bb676fed, the scripts
before this pass. The checker requires:

- valid JSON
- the same beats, in the same order, with image, caption, concept, and chapter
  left untouched
- every number, written number, date, and ticker token from the original
  narration still present (counts may only stay or grow)
- the legal disclaimer byte-for-byte
- none of the banned brand, entity, or bot-operation strings
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "fbb3f9c75981b80ac12ca1ba6b39f9d5bb676fed"
SCRIPTS = [
    "course/scripts/bp-04-market-regimes.json",
    "course/scripts/bp-05-spacing-and-range.json",
    "course/scripts/bp-06-entry-and-exit.json",
    "course/scripts/bp-07-spot-paper-trading.json",
    "course/scripts/bp-08-managing-and-monitoring.json",
    "course/scripts/bp-09-common-mistakes.json",
    "course/scripts/bp-10-scaling-up.json",
    "course/scripts/bp-11-advanced-liquidation.json",
]
DISCLAIMER = (
    "Education only, not financial advice. Crypto carries a risk of total loss. "
    "This is general information. It doesn't consider your objectives, financial "
    "situation or needs. The prices are public historical daily closes, marked "
    "Example. Past performance is not a reliable indicator of future results. "
    "No order is sent from this lesson."
)
NUMBER_RE = re.compile(r"\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+\.\d+|\d+")
DATE_RE = re.compile(
    r"\b\d{1,2}\s+(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|"
    r"Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:t(?:ember)?)?|Oct(?:ober)?|"
    r"Nov(?:ember)?|Dec(?:ember)?)(?:\s+\d{4})?\b"
    r"|\b(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|"
    r"Jul(?:y)?|Aug(?:ust)?|Sep(?:t(?:ember)?)?|Oct(?:ober)?|Nov(?:ember)?|"
    r"Dec(?:ember)?)\s+\d{1,2}(?:,?\s+\d{4})?\b",
    re.I,
)
TICKER_RE = re.compile(r"\b[A-Z]{2,6}(?:[-/][A-Z]{2,6})?\b")
WORD_NUMBER_RE = re.compile(
    r"\b(?:zero|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|"
    r"thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|"
    r"thirty|forty|fifty|sixty|seventy|eighty|ninety|hundred|thousand|half|"
    r"quarter|first|second|third|twice)(?:-[a-z]+)?\b",
    re.I,
)
BANNED = re.compile(
    r"market\s+pros|\bstewart\b|crown\s+crypto|\bconsultants\b|\bABN\b|\bACN\b|"
    r"\bAFSL\b|do not run|don't run|do not sell|don't sell|sell or run|"
    r"run the bot|run a trading bot|we do not run|we don't run|we do not sell|"
    r"we don't sell|we do not operate|we don't operate",
    re.I,
)
SENTENCE_RE = re.compile(r".+?[.!?]+(?:\s+|$)", re.S)


def load_baseline(rel: str) -> dict:
    raw = subprocess.check_output(
        ["git", "show", f"{BASE}:{rel}"], cwd=ROOT, text=True
    )
    return json.loads(raw)


def narrate(data: dict) -> str:
    return "\n".join(beat["vo"] for beat in data["beats"])


def tokens(text: str) -> Counter:
    found: Counter = Counter()
    found.update(f"num:{m}" for m in NUMBER_RE.findall(text))
    found.update(f"date:{m.casefold()}" for m in DATE_RE.findall(text))
    found.update(f"ticker:{m}" for m in TICKER_RE.findall(text))
    found.update(f"word:{m.casefold()}" for m in WORD_NUMBER_RE.findall(text))
    return found


def sentences(text: str) -> list[str]:
    parts = [m.group(0).strip() for m in SENTENCE_RE.finditer(text)]
    tail = SENTENCE_RE.sub("", text).strip()
    if tail:
        parts.append(tail)
    return parts


def check(rel: str) -> list[str]:
    path = ROOT / rel
    errors: list[str] = []
    try:
        revised = json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        return [f"{rel}: invalid JSON ({exc})"]
    try:
        original = load_baseline(rel)
    except (subprocess.CalledProcessError, json.JSONDecodeError) as exc:
        return [f"{rel}: could not read baseline ({exc})"]

    if not isinstance(revised.get("beats"), list):
        return [f"{rel}: beats is not a list"]
    if [b.get("n") for b in original["beats"]] != [b.get("n") for b in revised["beats"]]:
        errors.append(f"{rel}: beat order changed")
    if len(original["beats"]) != len(revised["beats"]):
        errors.append(f"{rel}: beat count changed")
        return errors

    for old, new in zip(original["beats"], revised["beats"]):
        for key in ("n", "role", "chapter", "cap", "concept", "image", "image_status", "prompt"):
            if old.get(key) != new.get(key):
                errors.append(f"{rel} beat {old.get('n')}: {key} changed")
        if not isinstance(new.get("vo"), str) or not new["vo"].strip():
            errors.append(f"{rel} beat {old.get('n')}: narration missing")
        if old.get("role") == "legal" and new.get("vo") != old.get("vo"):
            errors.append(f"{rel} beat {old.get('n')}: disclaimer narration changed")
        if new.get("role") == "legal" and new.get("vo") != DISCLAIMER:
            errors.append(f"{rel} beat {old.get('n')}: disclaimer is not the required text")

    original_tokens = tokens(narrate(original))
    revised_tokens = tokens(narrate(revised))
    missing = original_tokens - revised_tokens
    for token, count in sorted(missing.items()):
        errors.append(f"{rel}: lost {count} x {token}")
    for token in sorted(revised_tokens):
        if token.startswith("word:"):
            continue
        if original_tokens[token] == 0:
            errors.append(f"{rel}: new {token}")

    banned = BANNED.search(path.read_text())
    if banned:
        errors.append(f"{rel}: banned string {banned.group(0)!r}")
    return errors


def write_changes(dest: Path) -> None:
    lines = [
        "# BP-04 to BP-11 narration changes",
        "",
        "Spoken narration only. Beat order, captions, concepts, image paths, numbers, "
        "dates, tickers, and the disclaimer stay as written. Unchanged beats are omitted. "
        "Legal beats are the disclaimer and are unchanged.",
        "",
    ]
    any_change = False
    for rel in SCRIPTS:
        original = load_baseline(rel)
        revised = json.loads((ROOT / rel).read_text())
        changed = []
        for old, new in zip(original["beats"], revised["beats"]):
            if old["vo"] == new["vo"]:
                continue
            changed.append((old, new))
        if not changed:
            continue
        any_change = True
        lines.append(f"## {original['id']}")
        lines.append("")
        for old, new in changed:
            lines.append(
                f"### Beat {old['n']} ({old['role']}, {old['chapter']})"
            )
            lines.append("")
            old_s = sentences(old["vo"])
            new_s = sentences(new["vo"])
            if old_s == new_s:
                lines.append("Before:")
                lines.append("")
                lines.append(f"> {old['vo']}")
                lines.append("")
                lines.append("After:")
                lines.append("")
                lines.append(f"> {new['vo']}")
                lines.append("")
                continue
            # Pair sentences with a diff so each changed line is visible.
            import difflib

            matcher = difflib.SequenceMatcher(a=old_s, b=new_s)
            n = 0
            for tag, i1, i2, j1, j2 in matcher.get_opcodes():
                if tag == "equal":
                    continue
                n += 1
                lines.append(f"Change {n}:")
                lines.append("")
                if tag in ("replace", "delete"):
                    for sentence in old_s[i1:i2]:
                        lines.append(f"- Before: {sentence}")
                if tag in ("replace", "insert"):
                    for sentence in new_s[j1:j2]:
                        lines.append(f"- After: {sentence}")
                lines.append("")
        lines.append("")
    if not any_change:
        lines.append("No narration lines differ from the baseline yet.")
        lines.append("")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text("\n".join(lines).rstrip() + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--write-changes",
        type=Path,
        help="Also write the before/after markdown to this path.",
    )
    args = parser.parse_args()
    errors: list[str] = []
    for rel in SCRIPTS:
        errors.extend(check(rel))
    if args.write_changes:
        write_changes(args.write_changes if args.write_changes.is_absolute() else ROOT / args.write_changes)
    if errors:
        print(f"FAIL {len(errors)} check(s)")
        for err in errors:
            print(f"- {err}")
        return 1
    print(f"PASS {len(SCRIPTS)} lessons")
    print(f"baseline {BASE}")
    print("JSON valid")
    print("number, date, and ticker tokens preserved")
    print("disclaimers match byte-for-byte")
    print("banned strings: 0")
    return 0


if __name__ == "__main__":
    sys.exit(main())
