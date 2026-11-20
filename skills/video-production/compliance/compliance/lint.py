"""Australian financial-content flags for a script or a transcript.

The linter suggests plain rewrites. It does not clear itself. Status stays
`pending legal review` until a person appends a legal event to the review record.
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

import yaml

HYPE = (
    (r"\brisk[\s-]*free\b", "risk-free", "Say that the position can lose money."),
    (r"\bguaranteed\b", "guaranteed", "Say there is no guarantee, or describe the mechanism without a promise."),
    (r"\bproven\b", "proven", "Say what was observed, and that it can fail."),
    (r"\blike a pro\b", "like a pro", "Say \"with a written plan\"."),
    (r"\bcan(?:not|'t) lose\b", "can't lose", "Say you can lose some or all of the money."),
    (
        r"\d+(?:\.\d+)?\s*(?:%|percent)\s*returns?\b",
        "% returns",
        "Drop the return claim. If the figure is a sketch, label it EXAMPLE and say it is not a forecast.",
    ),
    (
        r"\breturns?\s+of\s+\d+(?:\.\d+)?\s*(?:%|percent)\b",
        "% returns",
        "Drop the return claim. If the figure is a sketch, label it EXAMPLE and say it is not a forecast.",
    ),
)

ADVICE = (
    (
        r"\byou should (?:buy|sell|hold|invest|enter|exit|put)\b",
        "personal advice",
        "Describe the mechanism. Do not tell the viewer to buy, sell, or invest.",
    ),
    (
        r"\b(?:i|we) recommend\b",
        "personal advice",
        "A recommendation can be personal advice. Leave the decision with the viewer.",
    ),
    (r"\bright for you\b", "personal advice", "Drop \"right for you\". The lesson is general."),
    (r"\bsuitable for you\b", "personal advice", "Suitability is personal advice. Remove it."),
    (
        r"\bbased on your (?:situation|circumstances|needs|objectives|finances)\b",
        "personal advice",
        "Keep the lesson general. Do not tailor it to one person's situation.",
    ),
    (
        r"\byou need to (?:buy|sell|invest|deposit|open)\b",
        "personal advice",
        "Say what the tool does. Do not instruct the viewer to move money.",
    ),
    (r"\bmy advice is\b", "personal advice", "Say \"the lesson is\", not \"my advice is\"."),
)

BRANDS = re.compile(
    r"\b(bybit|binance|pionex|coinbase|okx|kucoin|kraken|bitget|bitfinex|mexc|gemini)\b"
    r"|market\s+pros|\bgate\.io\b|\bhtx\b|\bcrypto\.com\b",
    re.I,
)

NUMBER = re.compile(
    r"\$[\d,]+(?:\.\d+)?"
    r"|\b\d+(?:\.\d+)?\s*%|\b\d+(?:\.\d+)?\s*percent\b"
    r"|\b\d+(?:\.\d+)?\s*(?:grids?|levels?|x)\b"
    r"|\b\d{2,}(?:\.\d+)?\b",
    re.I,
)
NUMBER_CONTEXT = re.compile(
    r"\b(price|prices|range|level|levels|entry|liquidation|leverage|grid|grids|buffer|dollars|usd)\b",
    re.I,
)
EXAMPLE = re.compile(r"\b(example|illustrative|illustration)\b", re.I)
NEGATION = re.compile(
    r"\b(not|no|never|isn't|aren't|won't|without|cannot|can't|none)\b",
    re.I,
)
DISCLAIMER_SKIP = re.compile(
    r"not financial advice|does not consider your|general information|education only|educational content",
    re.I,
)


def has_disclaimer(text: str) -> bool:
    low = text.lower()
    return "educat" in low and "not financial advice" in low


def _sentences(text: str) -> list[str]:
    parts = re.split(r"(?<=[.?!])\s+|\n+", text.strip())
    return [part.strip() for part in parts if part.strip()]


def _negated(sentence: str, start: int) -> bool:
    window = sentence[max(0, start - 80):start]
    return NEGATION.search(window) is not None


def _line_of(raw: str, snippet: str) -> int:
    token = snippet.strip()[:80]
    if not token:
        return 1
    idx = raw.find(token)
    if idx < 0:
        return 1
    return raw.count("\n", 0, idx) + 1


def _stamp_from_words(words: list, snippet: str) -> str | None:
    if not words:
        return None
    first = snippet.split()[0].strip(".,") if snippet.split() else ""
    for word in words:
        text = str(word.get("text", "")).strip(".,")
        if text.lower() == first.lower() and "start" in word:
            return _format_seconds(float(word["start"]))
    if words and "start" in words[0]:
        return _format_seconds(float(words[0]["start"]))
    return None


def _format_seconds(seconds: float) -> str:
    ms = int(round(seconds * 1000))
    hours, ms = divmod(ms, 3_600_000)
    minutes, ms = divmod(ms, 60_000)
    secs, ms = divmod(ms, 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}.{ms:03d}"


def _parse_vtt_times(text: str) -> list[tuple[float, float, str]]:
    cues = []
    blocks = re.split(r"\n\s*\n", text.replace("\r\n", "\n"))
    stamp = re.compile(r"(\d+):(\d{2}):(\d{2})[.,](\d{1,3})")

    def secs(token: str) -> float | None:
        match = stamp.search(token)
        if not match:
            return None
        frac = match.group(4).ljust(3, "0")
        return int(match.group(1)) * 3600 + int(match.group(2)) * 60 + int(match.group(3)) + int(frac) / 1000

    for block in blocks:
        lines = [line for line in block.split("\n") if line.strip()]
        if not lines or "-->" not in lines[0]:
            continue
        left, right = lines[0].split("-->", 1)
        start, end = secs(left), secs(right)
        if start is None or end is None:
            continue
        cues.append((start, end, " ".join(lines[1:])))
    return cues


def _timestamp_for(raw: str, snippet: str, cues: list[tuple[float, float, str]]) -> str | None:
    inline = re.search(r"(\d{2}:\d{2}:\d{2}[.,]\d{1,3})", snippet)
    if inline:
        return inline.group(1).replace(",", ".")
    for start, _end, text in cues:
        if snippet[:40] and snippet[:40] in text:
            return _format_seconds(start)
    return None


def load_document(path: Path) -> dict:
    """Split a file into spoken lines and on-screen lines."""
    raw = path.read_text(encoding="utf-8")
    spoken: list[dict] = []
    screen: list[dict] = []
    cues = _parse_vtt_times(raw) if path.suffix.lower() in {".vtt", ".srt"} else []
    suffix = path.suffix.lower()
    if suffix in {".yaml", ".yml"}:
        data = yaml.safe_load(raw) or {}
        beats = data.get("beats") or data.get("scenes") or []
        clock = 0.0
        for beat in beats:
            vo = beat.get("vo") or ""
            cap = beat.get("on_screen") or beat.get("cap") or beat.get("caption") or ""
            words = beat.get("words") or []
            if words:
                stamp = _stamp_from_words(words, vo)
                clock = float(words[-1].get("end", clock))
            else:
                stamp = _format_seconds(clock)
                clock += max(1.0, len(vo.split()) / 2.4)
            if vo:
                spoken.append({"text": vo, "line": _line_of(raw, vo), "timestamp": stamp})
            if cap:
                screen.append({"text": cap, "line": _line_of(raw, cap), "timestamp": stamp})
            for label in beat.get("labels") or []:
                screen.append({"text": str(label), "line": _line_of(raw, str(label)), "timestamp": stamp})
        for key in ("disclaimer_spoken", "disclaimer"):
            if data.get(key):
                spoken.append(
                    {"text": str(data[key]), "line": _line_of(raw, str(data[key])), "timestamp": "00:00:00.000"}
                )
        if data.get("disclaimer_on_screen"):
            screen.append(
                {
                    "text": str(data["disclaimer_on_screen"]),
                    "line": _line_of(raw, str(data["disclaimer_on_screen"])),
                    "timestamp": "00:00:00.000",
                }
            )
    elif suffix == ".json":
        data = json.loads(raw)
        items = data.get("scenes") or data.get("shots") or data.get("beats") or []
        clock = 0.0
        for item in items:
            vo = item.get("vo") or ""
            cap = item.get("cap") or item.get("caption") or item.get("on_screen") or ""
            stamp = _format_seconds(clock)
            clock += max(1.0, len(vo.split()) / 2.4)
            if vo:
                spoken.append({"text": vo, "line": _line_of(raw, vo), "timestamp": stamp})
            if cap:
                screen.append({"text": cap, "line": _line_of(raw, cap), "timestamp": stamp})
    elif suffix in {".vtt", ".srt"}:
        for start, _end, text in cues:
            spoken.append({"text": text, "line": _line_of(raw, text), "timestamp": _format_seconds(start)})
            screen.append({"text": text, "line": _line_of(raw, text), "timestamp": _format_seconds(start)})
    else:
        mode = "spoken"
        for number, line in enumerate(raw.splitlines(), start=1):
            stripped = line.strip()
            low = stripped.lower()
            if low in {"## spoken", "# spoken", "[spoken]"}:
                mode = "spoken"
                continue
            if low in {"## on-screen", "## onscreen", "# on-screen", "[on-screen]", "[onscreen]"}:
                mode = "screen"
                continue
            if not stripped or stripped.startswith("#"):
                continue
            stamp_match = re.match(r"(?:\[(?:spoken|on-screen|onscreen)\s+)?(\d{2}:\d{2}:\d{2}[.,]\d{1,3})\]?\s+(.*)", stripped, re.I)
            if stamp_match:
                text = stamp_match.group(2)
                stamp = stamp_match.group(1).replace(",", ".")
            else:
                text = stripped
                stamp = None
            row = {"text": text, "line": number, "timestamp": stamp}
            if stripped.lower().startswith("[on-screen]") or stripped.lower().startswith("[onscreen]"):
                screen.append(row)
            elif mode == "screen":
                screen.append(row)
            else:
                spoken.append(row)
    return {"raw": raw, "spoken": spoken, "screen": screen, "cues": cues}


def _flag(kind: str, sentence: str, line: int, timestamp: str | None, term: str, suggestion: str) -> dict:
    return {
        "severity": "fail",
        "kind": kind,
        "term": term,
        "line": line,
        "timestamp": timestamp,
        "text": sentence[:240],
        "suggestion": suggestion,
    }


def lint_rows(rows: list[dict], cues: list[tuple[float, float, str]]) -> list[dict]:
    flags: list[dict] = []
    seen: set[tuple] = set()
    for row in rows:
        for sentence in _sentences(row["text"]):
            if DISCLAIMER_SKIP.search(sentence) and not re.search(r"\byou should (?:buy|sell|invest)\b", sentence, re.I):
                # The disclaimer names the viewer's situation in order to refuse it.
                advice_patterns = ()
            else:
                advice_patterns = ADVICE
            for pattern, term, suggestion in HYPE + advice_patterns:
                match = re.search(pattern, sentence, re.I)
                if not match or _negated(sentence, match.start()):
                    continue
                key = (term, row["line"], match.group(0).lower())
                if key in seen:
                    continue
                seen.add(key)
                stamp = row.get("timestamp") or _timestamp_for(sentence, sentence, cues)
                flags.append(_flag("hype" if (pattern, term, suggestion) in HYPE else "personal-advice", sentence, row["line"], stamp, term, suggestion))
            brand = BRANDS.search(sentence)
            if brand:
                key = ("brand", row["line"], brand.group(0).lower())
                if key not in seen:
                    seen.add(key)
                    flags.append(
                        _flag(
                            "brand",
                            sentence,
                            row["line"],
                            row.get("timestamp"),
                            brand.group(0),
                            "Remove the exchange or brand name. Describe the mechanism without naming a venue.",
                        )
                    )
            if NUMBER_CONTEXT.search(sentence) or "$" in sentence or "%" in sentence or re.search(r"\d+(?:\.\d+)?\s*(?:%|percent|grids?)", sentence, re.I):
                if EXAMPLE.search(sentence):
                    continue
                number = NUMBER.search(sentence)
                if number and not (number.group(0).isdigit() and not NUMBER_CONTEXT.search(sentence) and "$" not in sentence and "%" not in sentence):
                    key = ("number", row["line"], number.group(0))
                    if key not in seen:
                        seen.add(key)
                        flags.append(
                            _flag(
                                "example-number",
                                sentence,
                                row["line"],
                                row.get("timestamp"),
                                number.group(0),
                                f'Label the figure EXAMPLE, for example "EXAMPLE: {number.group(0)}".',
                            )
                        )
    return flags


def lint_document(doc: dict, *, source: str) -> dict:
    cues = doc.get("cues") or []
    flags = lint_rows(doc["spoken"] + doc["screen"], cues)
    spoken_text = " ".join(row["text"] for row in doc["spoken"])
    screen_text = " ".join(row["text"] for row in doc["screen"])
    if not has_disclaimer(spoken_text):
        flags.append(
            _flag(
                "disclaimer",
                spoken_text[:180] or "(no spoken text)",
                doc["spoken"][0]["line"] if doc["spoken"] else 1,
                doc["spoken"][0].get("timestamp") if doc["spoken"] else None,
                "spoken disclaimer",
                'Add a spoken line: "This is education, not financial advice."',
            )
        )
    if not has_disclaimer(screen_text):
        flags.append(
            _flag(
                "disclaimer",
                screen_text[:180] or "(no on-screen text)",
                doc["screen"][0]["line"] if doc["screen"] else 1,
                doc["screen"][0].get("timestamp") if doc["screen"] else None,
                "on-screen disclaimer",
                'Put "Education, not financial advice." on screen as well as in the voice.',
            )
        )
    content = "pass" if not flags else "fail"
    digest = hashlib.sha256(doc["raw"].encode("utf-8")).hexdigest()
    return {
        "tool": "compliance",
        "source": source,
        "status": "pending legal review",
        "auto_clear": False,
        "content_result": content,
        "content_hash": digest,
        "flag_count": len(flags),
        "flags": flags,
        "signoff": "A person records legal approval in the review record. This linter never writes that approval.",
        "publishes": False,
    }


def lint_path(path: Path) -> dict:
    document = load_document(Path(path))
    return lint_document(document, source=str(path))


def apply_ledger(report: dict, ledger: Path | None) -> dict:
    """Reflect a human legal event. Never invent one."""
    report = dict(report)
    report["legal_recorded"] = False
    if ledger is None or not Path(ledger).is_file():
        return report
    matched = False
    for line in Path(ledger).read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if event.get("type") != "legal":
            continue
        if event.get("content_hash") == report["content_hash"] and event.get("decision") == "approved":
            if event.get("name") and event.get("date"):
                matched = True
                report["legal_reviewer"] = event["name"]
                report["legal_date"] = event["date"]
    if matched and report["content_result"] == "pass":
        report["status"] = "legal signed"
        report["legal_recorded"] = True
    return report
