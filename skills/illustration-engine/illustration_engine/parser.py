"""Turn a sentence, or a JSON or YAML spec, into a Spec.

The rules are deterministic. An optional helper can draft the same JSON,
and this module is what accepts it. Nothing here draws pixels.
"""

from __future__ import annotations

import json
import re

import yaml

from .spec import TYPES, Spec

WORD_NUMBERS = {
    "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7,
    "eight": 8, "nine": 9, "ten": 10, "twelve": 12,
}

RANGE_RE = re.compile(
    r"range\s+(-?\d+(?:\.\d+)?)\s*(?:-|to|–)\s*(-?\d+(?:\.\d+)?)",
    re.I,
)
GRIDS_RE = re.compile(r"(\d+)\s+grids?", re.I)
PRICE_RE = re.compile(r"\b(?:price|mark|at)\s+(-?\d+(?:\.\d+)?)", re.I)
ENTRY_RE = re.compile(r"\bentry\s+(-?\d+(?:\.\d+)?)", re.I)
LIQ_RE = re.compile(r"\b(?:liquidation|liq)\s+(-?\d+(?:\.\d+)?)", re.I)
LEV_RE = re.compile(r"\bleverage\s+(\d+(?:\.\d+)?)", re.I)
SEED_RE = re.compile(r"\bseed\s+(\d+)", re.I)
LABEL_RE = re.compile(r"\blabels?\s+(.+)$", re.I)
HEAD_RE = re.compile(r'\bheadline\s+"([^"]+)"', re.I)


class ParseError(ValueError):
    pass


def parse_size(value) -> tuple[int, int] | None:
    if value is None:
        return None
    if isinstance(value, (list, tuple)) and len(value) == 2:
        return int(value[0]), int(value[1])
    text = str(value).lower().replace(" ", "")
    if "x" not in text:
        raise ParseError(f"size must look like 1536x1024, got {value!r}")
    w, h = text.split("x", 1)
    return int(w), int(h)


def _labels_from_clause(clause: str) -> list[str]:
    clause = RANGE_RE.sub(" ", clause)
    parts = re.split(r",| and ", clause, flags=re.I)
    out = []
    for part in parts:
        words = [w for w in re.findall(r"[A-Za-z][A-Za-z0-9]*", part)]
        if not words:
            continue
        label = " ".join(words[:3]).upper()
        if label and label not in out:
            out.append(label)
        if len(out) == 5:
            break
    return out


def _phrases_after_colon(concept: str) -> list[str]:
    if ":" not in concept:
        return []
    tail = concept.split(":", 1)[1]
    parts = re.split(r",| and ", tail, flags=re.I)
    stop = {"the", "a", "an", "of", "to", "before", "any", "you", "keep", "this"}
    out = []
    for part in parts:
        words = [w for w in re.findall(r"[A-Za-z]{3,}", part) if w.lower() not in stop]
        if not words:
            continue
        label = " ".join(words[:2]).upper()
        if label not in out:
            out.append(label)
        if len(out) == 4:
            break
    return out


def classify(concept: str, role: str = "", chapter: str = "") -> str:
    blob = f"{role} {chapter} {concept}".lower()
    role_l = role.lower()
    if role_l == "intro" or "title card" in blob:
        return "title_card"
    if "lesson cover" in blob or ("cover" in blob and "lesson" in blob):
        return "lesson_cover"
    if "section divider" in blob or role_l == "outro" or blob.strip().startswith("next lesson") or "next lesson" in blob[:80]:
        return "section_divider"
    if "fence" in blob:
        return "analogy_fence"
    if "bucket" in blob:
        return "analogy_buckets"
    if "checklist" in blob or "on paper" in blob:
        return "checklist"
    if "liquidat" in blob or "leverage" in blob or "danger zone" in blob:
        return "liquidation"
    if any(word in blob for word in ("doji", "hammer", "engulf")):
        return "candle_pattern"
    if "anatomy" in blob or "single candle" in blob:
        return "candle_anatomy"
    if "candle" in blob or "ohlc" in blob:
        return "candle_series"
    if "no order" in blob or "do not sell" in blob or "not a trading bot" in blob:
        return "mascot_scene"
    if "tick" in blob or "grid ladder" in blob or "grids" in blob or ("buy" in blob and "sell" in blob):
        return "grid_ladder"
    if "result number" in blob or "no result" in blob:
        return "comparison"
    if role_l == "map" or " is a map" in blob or "flowchart" in blob:
        return "flowchart"
    if "three parts" in blob or role_l in {"recap", "legal"}:
        return "steps"
    if "stop" in blob or "invalidat" in blob:
        return "price_range"
    if any(word in blob for word in ("range", "band", "sideways", "chop", "support", "resistance")):
        return "price_range"
    if "rung" in blob or "ladder" in blob:
        return "analogy_ladder"
    if any(word in blob for word in (" versus ", " vs ", "compared", "comparison")):
        return "comparison"
    if "cover" in blob and "lesson" in blob:
        return "lesson_cover"
    if "divider" in blob:
        return "section_divider"
    if "mascot" in blob or "robot" in blob:
        return "mascot_scene"
    if role_l in {"recap", "legal", "action"} or "three parts" in blob or "step" in blob:
        return "steps"
    return "steps"


def _headline(kind: str, concept: str, role: str, chapter: str, title: str) -> str:
    generic = {"hook", "body", "demo", "diagram", "disclaimer", "recap", "action", "intro", "outro", "map", "title card"}
    if role == "intro":
        return (title or "INTRODUCTION").upper()
    if role == "outro":
        return "NEXT"
    if role == "legal":
        return "EDUCATION ONLY"
    if chapter and chapter.lower() not in generic and len(chapter) <= 28:
        return chapter.upper()
    defaults = {
        "candle_anatomy": "CANDLE PARTS",
        "candle_series": "SIDEWAYS CANDLES",
        "candle_pattern": "ONE PATTERN",
        "grid_ladder": "GRID LADDER",
        "liquidation": "LIQUIDATION LINE",
        "price_range": "THE RANGE",
        "flowchart": "THE PATH",
        "comparison": "NO RESULT" if "result" in concept.lower() else "TWO WAYS",
        "steps": "THREE PARTS",
        "analogy_fence": "THE FENCE",
        "analogy_ladder": "THE LADDER",
        "analogy_buckets": "TWO BUCKETS",
        "checklist": "ON PAPER",
        "mascot_scene": "CHECK FIRST",
        "title_card": (title or "INTRODUCTION").upper(),
        "lesson_cover": (title or "LESSON").upper(),
        "section_divider": "NEXT",
    }
    return defaults.get(kind, "ONE IDEA")


def _params_for(kind: str, concept: str, role: str, chapter: str, title: str, beat: int) -> dict:
    low = concept.lower()
    params: dict = {"seed": beat, "concept": concept, "headline": _headline(kind, concept, role, chapter, title)}
    phrases = _phrases_after_colon(concept)
    if kind == "grid_ladder":
        params.update({"low": 90, "high": 110, "grids": 8, "price": 100, "labels": ["BUY", "SELL", "PRICE"]})
        for word, count in WORD_NUMBERS.items():
            if word in low:
                params["grids"] = count
        if "buy" in low and "sell" in low:
            params["labels"] = ["BUY", "SELL", "PRICE"]
    elif kind == "price_range":
        params["labels"] = ["UPPER", "LOWER", "RANGE"]
        if "stop" in low:
            params["stop"] = True
            params["variant"] = "stop"
            params["labels"] = ["UPPER", "LOWER", "STOP"]
        elif "leave" in low or "does not return" in low:
            params["variant"] = "leave"
            params["labels"] = ["UPPER", "LOWER", "OUT"]
        elif "sideways" in low or "chop" in low:
            params["labels"] = ["RANGE", "BAND"]
            params["headline"] = "SIDEWAYS BAND"
    elif kind == "liquidation":
        params.update({"entry": 100, "liquidation": 80, "price": 90, "leverage": 5, "labels": ["ENTRY", "DANGER", "LIQUIDATION"]})
    elif kind == "steps":
        if role == "legal":
            params["labels"] = ["LEARN", "NOTICE", "PAPER"]
        elif phrases:
            params["labels"] = phrases[:4]
        else:
            params["labels"] = ["RANGE", "LEVELS", "STOP"]
    elif kind == "checklist":
        params["labels"] = phrases[:4] or ["RANGE", "LEVELS", "STOP"]
        params["highlight"] = 0
    elif kind == "analogy_fence":
        params["labels"] = ["INSIDE", "FENCE", "PRACTICE"]
    elif kind == "analogy_ladder":
        params["labels"] = ["RUNG", "LEVEL", "WAIT"]
    elif kind == "analogy_buckets":
        params["labels"] = ["APART", "OVERLAP", "BUCKET"]
    elif kind == "flowchart":
        params["labels"] = ["START", "MIDDLE", "NEXT"]
    elif kind == "comparison":
        params["variant"] = "plain"
        params["labels"] = ["NUMBER", "SHAPE"]
        params["headline"] = "NO RESULT"
    elif kind == "mascot_scene":
        if "think" in low:
            pose = "thinking"
        elif "celebrat" in low:
            pose = "celebrating"
        elif "point" in low:
            pose = "pointing"
        else:
            pose = "warning"
        poses = {
            "pointing": ("LOOK HERE", ["POINT", "RANGE"]),
            "thinking": ("THINK FIRST", ["THINK", "CHECK"]),
            "warning": ("CHECK FIRST", ["WAIT", "CHECK"]),
            "celebrating": ("STEP DONE", ["DONE", "NEXT"]),
        }
        headline, pose_labels = poses[pose]
        params["pose"] = pose
        params["headline"] = headline
        params["labels"] = pose_labels
    elif kind == "title_card":
        params["title"] = title or "INTRODUCTION"
        params["labels"] = ["START", "HERE"]
    elif kind == "section_divider":
        params["title"] = "NEXT"
        params["labels"] = ["PART", "NEXT"]
    elif kind == "lesson_cover":
        params["title"] = title or "LESSON"
        params["labels"] = ["LESSON", "START"]
    if phrases and kind in {"steps", "checklist"}:
        params["labels"] = phrases[:4]
    return params


def spec_from_request(req: dict, *, fallback: bool = False, allow_generic: bool = False) -> Spec:
    from .policy import enforce_mode, screen

    concept, notes = screen(str(req.get("concept") or ""), allow_generic=allow_generic)
    role = str(req.get("role") or "")
    chapter = str(req.get("chapter") or "")
    title = str(req.get("title") or "")
    beat = int(req.get("beat") or 1)
    kind = classify(concept, role, chapter)
    params = _params_for(kind, concept, role, chapter, title, beat)
    file_name = None
    if req.get("out_path"):
        file_name = str(req["out_path"]).replace("\\", "/").split("/")[-1]
    elif req.get("file"):
        file_name = str(req["file"])
    if notes:
        params["replaced_names"] = len(notes)
    spec = Spec(
        type=kind,
        params=params,
        preset=str(req.get("palette") or "house") if str(req.get("palette") or "") in {"house", "light", "contrast", "thumbnail", "elite"} else "house",
        size=parse_size(req.get("size")) if req.get("size") else (1536, 1024),
        headline=params.get("headline"),
        labels=list(params.get("labels") or []),
        source_id=req.get("id"),
        file=file_name,
    )
    return enforce_mode(spec, fallback=fallback)


def spec_from_dict(data: dict) -> Spec:
    if not isinstance(data, dict):
        raise ParseError("a spec must be an object")
    kind = str(data.get("type") or "").strip()
    if kind not in TYPES:
        raise ParseError(f"unknown type {kind!r}")
    params = dict(data.get("params") or {})
    if data.get("headline") and "headline" not in params:
        params["headline"] = data["headline"]
    if data.get("labels") and "labels" not in params:
        params["labels"] = data["labels"]
    # Flatten common keys written beside type.
    for key in ("low", "high", "grids", "price", "entry", "liquidation", "leverage", "seed",
                "variant", "pose", "title", "stop", "count", "highlight"):
        if key in data and key not in params:
            params[key] = data[key]
    preset = str(data.get("preset") or "house")
    return Spec(
        type=kind,
        params=params,
        preset=preset,
        size=parse_size(data.get("size")) if data.get("size") else None,
        headline=params.get("headline"),
        labels=list(params.get("labels") or []) or None,
        source_id=data.get("source_id"),
        file=data.get("file"),
    )


def parse(source: str, *, fallback: bool = False, allow_generic: bool = False) -> Spec:
    """Parse a prompt. JSON and YAML win when the text is a spec; otherwise use the rules."""
    from .policy import enforce_mode, screen, screen_value

    text = (source or "").strip()
    if not text:
        raise ParseError("empty prompt")
    if text[0] == "{":
        try:
            loaded = json.loads(text)
        except json.JSONDecodeError as exc:
            raise ParseError(f"invalid JSON spec: {exc}") from exc
        loaded, notes = screen_value(loaded, allow_generic=allow_generic)
        spec = spec_from_dict(loaded)
        if notes:
            spec.params["replaced_names"] = len(notes)
        return enforce_mode(spec, fallback=fallback)
    if text.startswith("type:") or text.startswith("---"):
        try:
            loaded = yaml.safe_load(text)
        except yaml.YAMLError as exc:
            raise ParseError(f"invalid YAML spec: {exc}") from exc
        if isinstance(loaded, dict) and loaded.get("type"):
            loaded, notes = screen_value(loaded, allow_generic=allow_generic)
            spec = spec_from_dict(loaded)
            if notes:
                spec.params["replaced_names"] = len(notes)
            return enforce_mode(spec, fallback=fallback)
    text, notes = screen(text, allow_generic=allow_generic)
    spec = _parse_sentence(text)
    if notes:
        spec.params["replaced_names"] = len(notes)
    return enforce_mode(spec, fallback=fallback)


def _parse_sentence(text: str) -> Spec:
    headline = None
    head = HEAD_RE.search(text)
    if head:
        headline = head.group(1)
        text = HEAD_RE.sub(" ", text)
    labels = None
    label_match = LABEL_RE.search(text)
    if label_match:
        labels = _labels_from_clause(label_match.group(1))
        text = text[: label_match.start()]
    kind = classify(text)
    params: dict = {}
    if headline:
        params["headline"] = headline
    found = RANGE_RE.search(text)
    if found:
        params["low"] = float(found.group(1))
        params["high"] = float(found.group(2))
    grids = GRIDS_RE.search(text)
    if grids:
        params["grids"] = int(grids.group(1))
    price = PRICE_RE.search(text)
    if price:
        params["price"] = float(price.group(1))
    entry = ENTRY_RE.search(text)
    if entry:
        params["entry"] = float(entry.group(1))
    liq = LIQ_RE.search(text)
    if liq:
        params["liquidation"] = float(liq.group(1))
    lev = LEV_RE.search(text)
    if lev:
        params["leverage"] = float(lev.group(1))
    seed = SEED_RE.search(text)
    if seed:
        params["seed"] = int(seed.group(1))
    low = text.lower()
    if "hammer" in low:
        params["variant"] = "hammer"
    elif "doji" in low:
        params["variant"] = "doji"
    elif "engulf" in low:
        params["variant"] = "engulfing"
    elif "bear" in low:
        params["variant"] = "bear"
    elif "wick" in low:
        params["variant"] = "wick"
    if "pointing" in low:
        params["pose"] = "pointing"
    elif "thinking" in low:
        params["pose"] = "thinking"
    elif "celebrat" in low:
        params["pose"] = "celebrating"
    elif "warning" in low:
        params["pose"] = "warning"
    if "leave" in low or "does not return" in low:
        params["variant"] = params.get("variant") or "leave"
    if "stop" in low and kind == "price_range":
        params["stop"] = True
        params["variant"] = "stop"
    if labels:
        params["labels"] = labels
    # Fill the same defaults the lesson mapper uses, then let the sentence override.
    base = _params_for(kind, text, "", "", "", int(params.get("seed") or 1))
    base.update(params)
    if labels:
        base["labels"] = labels
    return Spec(type=kind, params=base, headline=base.get("headline"), labels=list(base.get("labels") or []) or None)
