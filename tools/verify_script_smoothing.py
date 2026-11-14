#!/usr/bin/env python3
"""Check BP-04..BP-11 narration smoothing against the pre-edit scripts.

The baseline is commit fbb3f9c75981b80ac12ca1ba6b39f9d5bb676fed.
Narration (`vo`) is the only field that may change. For each beat the
checker requires:

- the same number tokens, including written-out numbers, with the same counts
- every original sentence that contains Example, not financial advice,
  do not operate, not affiliated, risk, or recommendation, byte for byte,
  except the two approved bot-line removals
- no bot sentence
- every field other than narration unchanged
"""

from __future__ import annotations

import argparse
import copy
import difflib
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
# Bot sentences only. "we do not operate" and a blanket "do not run" are not bans.
BOT_SENTENCE = re.compile(
    r"we do not run the bot|we don't run the bot|do not run the bot|don't run the bot|"
    r"run a trading bot|run the bot|sell or run|"
    r"do not run the card|don't run the card|"
    r"we do not sell|we don't sell|do not sell|don't sell|"
    r"market\s+pros|\bstewart\b|crown\s+crypto|\bABN\b|\bACN\b|\bAFSL\b",
    re.I,
)
PROTECTED = (
    "example",
    "not financial advice",
    "do not operate",
    "not affiliated",
    "risk",
    "recommendation",
)
APPROVED_REMOVALS = {
    "We do not run the bot that would confirm for you.",
    "Do not run the card on a live position as the homework.",
}
NOT_A_DEFINITION = APPROVED_REMOVALS | {
    "The lesson stops in front of that control.",
    "The homework is that card on the path you drew.",
}
SENTENCE_RE = re.compile(r".+?[.!?]+(?:\s+|$)", re.S)


def load_baseline(rel: str) -> dict:
    raw = subprocess.check_output(["git", "show", f"{BASE}:{rel}"], cwd=ROOT, text=True)
    return json.loads(raw)


def sentences(text: str) -> list[str]:
    parts = [match.group(0).strip() for match in SENTENCE_RE.finditer(text)]
    tail = SENTENCE_RE.sub("", text).strip()
    if tail:
        parts.append(tail)
    return parts


def number_tokens(text: str) -> Counter:
    found: Counter = Counter()
    found.update(f"num:{token}" for token in NUMBER_RE.findall(text))
    found.update(f"word:{token.casefold()}" for token in WORD_NUMBER_RE.findall(text))
    found.update(f"date:{token.casefold()}" for token in DATE_RE.findall(text))
    return found


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
    if len(original["beats"]) != len(revised["beats"]):
        return [f"{rel}: beat count changed"]

    original_structure = copy.deepcopy(original)
    revised_structure = copy.deepcopy(revised)
    for old_beat, new_beat in zip(original_structure["beats"], revised_structure["beats"]):
        old_beat.pop("vo", None)
        new_beat.pop("vo", None)
    if original_structure != revised_structure:
        errors.append(f"{rel}: a non-narration field changed")

    for old, new in zip(original["beats"], revised["beats"]):
        label = f"{rel} beat {old.get('n')}"
        if not isinstance(new.get("vo"), str) or not new["vo"].strip():
            errors.append(f"{label}: narration missing")
            continue
        if old.get("role") == "legal" and new.get("vo") != DISCLAIMER:
            errors.append(f"{label}: disclaimer is not byte-for-byte")
        old_numbers = number_tokens(old["vo"])
        new_numbers = number_tokens(new["vo"])
        if old_numbers != new_numbers:
            lost = old_numbers - new_numbers
            gained = new_numbers - old_numbers
            for token, count in sorted(lost.items()):
                errors.append(f"{label}: lost {count} x {token}")
            for token, count in sorted(gained.items()):
                errors.append(f"{label}: new count {count} x {token}")
        old_tickers = Counter(TICKER_RE.findall(old["vo"]))
        new_tickers = Counter(TICKER_RE.findall(new["vo"]))
        for token, count in sorted((old_tickers - new_tickers).items()):
            errors.append(f"{label}: lost ticker {token} x {count}")
        for token in sorted(new_tickers):
            if old_tickers[token] == 0:
                errors.append(f"{label}: new ticker {token}")
        for sentence in sentences(old["vo"]):
            folded = sentence.casefold()
            if sentence in APPROVED_REMOVALS:
                continue
            if any(trigger in folded for trigger in PROTECTED) and sentence not in new["vo"]:
                errors.append(f"{label}: protected line changed: {sentence}")

    banned = BOT_SENTENCE.search(path.read_text())
    if banned:
        errors.append(f"{rel}: bot sentence {banned.group(0)!r}")
    return errors


def added_definitions(original: dict, revised: dict) -> list[tuple[int, str]]:
    kept: list[tuple[int, str]] = []
    for old, new in zip(original["beats"], revised["beats"]):
        old_sentences = set(sentences(old["vo"]))
        for sentence in sentences(new["vo"]):
            if sentence in old_sentences or sentence in NOT_A_DEFINITION:
                continue
            kept.append((old["n"], sentence))
    return kept


def write_changes(dest: Path) -> None:
    lines = [
        "# BP-04 to BP-11 narration changes",
        "",
        "Spoken narration only. Beat order, captions, concepts, image paths, numbers, "
        "dates, tickers, and the disclaimer stay as written. The full Example risk "
        "sentence stays wherever the original had it. Unchanged beats are omitted. "
        "Legal beats are the disclaimer and are unchanged.",
        "",
        "## Kept plain-meaning definitions",
        "",
        "Each line below only restates the lesson or a basic dictionary meaning. "
        "Definitions that added a fact, a rule, or a recommendation were removed.",
        "",
    ]
    any_change = False
    any_definition = False
    for rel in SCRIPTS:
        if not (ROOT / rel).is_file():
            continue
        original = load_baseline(rel)
        revised = json.loads((ROOT / rel).read_text())
        kept = added_definitions(original, revised)
        if not kept:
            continue
        # Only list a lesson once its narration actually differs.
        if all(old["vo"] == new["vo"] for old, new in zip(original["beats"], revised["beats"])):
            continue
        any_definition = True
        lines.append(f"### {original['id']}")
        lines.append("")
        for number, sentence in kept:
            lines.append(f"- Beat {number}: {sentence}")
        lines.append("")
    if not any_definition:
        lines.append("None in the files changed so far.")
        lines.append("")
    for rel in SCRIPTS:
        if not (ROOT / rel).is_file():
            continue
        original = load_baseline(rel)
        revised = json.loads((ROOT / rel).read_text())
        changed = [
            (old, new)
            for old, new in zip(original["beats"], revised["beats"])
            if old["vo"] != new["vo"]
        ]
        if not changed:
            continue
        any_change = True
        lines.append(f"## {original['id']}")
        lines.append("")
        for old, new in changed:
            lines.append(f"### Beat {old['n']} ({old['role']}, {old['chapter']})")
            lines.append("")
            old_sentences = sentences(old["vo"])
            new_sentences = sentences(new["vo"])
            matcher = difflib.SequenceMatcher(a=old_sentences, b=new_sentences)
            change_number = 0
            for tag, i1, i2, j1, j2 in matcher.get_opcodes():
                if tag == "equal":
                    continue
                change_number += 1
                lines.append(f"Change {change_number}:")
                lines.append("")
                if tag in ("replace", "delete"):
                    for sentence in old_sentences[i1:i2]:
                        lines.append(f"- Before: {sentence}")
                if tag in ("replace", "insert"):
                    for sentence in new_sentences[j1:j2]:
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
    passed = 0
    for rel in SCRIPTS:
        lesson_errors = check(rel)
        if lesson_errors:
            errors.extend(lesson_errors)
            print(f"FAIL {rel}")
            for err in lesson_errors:
                print(f"- {err}")
        else:
            passed += 1
            print(f"PASS {rel}")
    if args.write_changes:
        destination = args.write_changes if args.write_changes.is_absolute() else ROOT / args.write_changes
        write_changes(destination)
    print(f"baseline {BASE}")
    print("JSON valid" if not any("invalid JSON" in err for err in errors) else "JSON invalid")
    print(f"lessons passed: {passed} of {len(SCRIPTS)}")
    if errors:
        print(f"FAIL {len(errors)} check(s)")
        return 1
    print("per-beat number and written-number counts match")
    print("protected lines match byte-for-byte")
    print("non-narration fields unchanged")
    print("bot sentences: 0")
    return 0


if __name__ == "__main__":
    sys.exit(main())
