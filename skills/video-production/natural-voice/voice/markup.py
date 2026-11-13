"""Pause markup, chunking, captions, and the character-cost estimate."""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass

PAUSE = re.compile(
    r"\[\[pause\s+([0-9]*\.?[0-9]+)\s*\]\]"
    r"|<break\s+time=[\"']([0-9]*\.?[0-9]+)(ms|s)[\"']\s*/?>",
    re.IGNORECASE,
)

# Credits per character. ElevenLabs bills from the account plan; these are the
# published relative weights so a run can be priced before it starts.
CREDIT_PER_CHARACTER = {
    "eleven_multilingual_v2": 1.0,
    "eleven_turbo_v2_5": 0.5,
    "eleven_flash_v2_5": 0.5,
}

STOCK_VOICES = {
    "rachel": "21m00Tcm4TlvDq8ikWAM",
    "drew": "29vD33N1CtxCmqQRPOHJ",
    "clyde": "2EiwWnXFnvU5JabPnv8n",
    "paul": "5Q0t7uMcjvnagumLfvZi",
    "domi": "AZnzlk1XvdvUeBnXmlld",
    "dave": "CYw3kZ02Hs0563khs1Fj",
    "fin": "D38z5RcWu1voky8WS1ja",
    "sarah": "EXAVITQu4vr4xnSDxMaL",
    "antoni": "ErXwobaYiN019PkySvjV",
    "thomas": "GBv7mTt0atIp3Br8iCZE",
    "charlie": "IKne3meq5aSn9XLyUdCD",
    "george": "JBFqnCBsd6RMkjVDRZzb",
    "callum": "N2lVS1w4EtoT3dr4eOWO",
    "harry": "SOYHLrjzK2X1ezoPC6cr",
    "liam": "TX3LPaxmHKxFdv7VOQHJ",
    "dorothy": "ThT5KcBeYPX3keUQqHPh",
    "josh": "TxGEqnHWrfWFTfGW9XjX",
    "arnold": "VR6AewLTigWG4xSOukaG",
    "charlotte": "XB0fDUnXU5powFXDhCwa",
    "alice": "Xb7hH8MSUJpSbSDYk0k2",
    "matilda": "XrExE9yKIg1WjnnlVkGX",
    "matthew": "Yko7PKHZNXotIFUBG7I9",
    "james": "ZQe5CZNOzWyzPSCn5a3c",
    "joseph": "Zlb1dXrM653N07WRdFW3",
    "jessica": "cgSgspJ2msm6clMCkdW9",
    "eric": "cjVigY5qzO86Huf0OWal",
    "michael": "flq6f7yk4E4fJM5XTYuZ",
    "ethan": "g5CIjZEefAph4nQFvHAz",
    "chris": "iP95p4xoKVk53GoZ742B",
    "brian": "nPczCjzI2devNBz1zQrb",
    "grace": "oWAxZDx7w5VEj9dCyTzz",
    "daniel": "onwK4e9ZLuTAKqWW03F9",
    "lily": "pFZP5JQG7iQjIQuC4Bku",
    "serena": "pMsXgVXv3BLzUgSXRplE",
    "adam": "pNInz6obpgDQGcFmaJgB",
    "nicole": "piTKgcLEGmPE4e6mEKli",
    "bill": "pqHfZKP75CvOlQylNhV4",
    "jessie": "t0jbNlBVZ17f02VDIeMI",
    "sam": "yoZ06aMxZJJ28mfd3POQ",
    "glinda": "z9fAnlkpzviPz146aGWa",
}


@dataclass
class Word:
    text: str
    start: float
    end: float

    def as_dict(self) -> dict:
        return {"text": self.text, "start": round(self.start, 3), "end": round(self.end, 3)}


def parse_segments(text: str) -> list[tuple[str, str | float]]:
    segments: list[tuple[str, str | float]] = []
    cursor = 0
    for match in PAUSE.finditer(text):
        before = text[cursor:match.start()].strip()
        if before:
            segments.append(("text", before))
        if match.group(1) is not None:
            seconds = float(match.group(1))
        else:
            seconds = float(match.group(2))
            if match.group(3).lower() == "ms":
                seconds /= 1000.0
        if seconds < 0 or seconds > 10:
            raise ValueError("a pause must be between 0 and 10 seconds")
        segments.append(("pause", seconds))
        cursor = match.end()
    tail = text[cursor:].strip()
    if tail:
        segments.append(("text", tail))
    return segments


def spoken_text(text: str) -> str:
    return " ".join(payload for kind, payload in parse_segments(text) if kind == "text")


def split_sentences(text: str) -> list[str]:
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [part.strip() for part in parts if part.strip()]


def chunk_text(text: str, limit: int = 420) -> list[str]:
    """Pack sentences into chunks short enough to keep prosody even."""
    if limit < 40:
        raise ValueError("chunk limit is too small")
    sentences = split_sentences(text)
    if not sentences:
        return []
    chunks: list[str] = []
    current = ""
    for sentence in sentences:
        if len(sentence) > limit:
            if current:
                chunks.append(current)
                current = ""
            words = sentence.split()
            line = ""
            for word in words:
                trial = (line + " " + word).strip()
                if len(trial) > limit and line:
                    chunks.append(line)
                    line = word
                else:
                    line = trial
            if line:
                current = line
            continue
        trial = (current + " " + sentence).strip()
        if current and len(trial) > limit:
            chunks.append(current)
            current = sentence
        else:
            current = trial
    if current:
        chunks.append(current)
    return chunks


def estimate(text: str, engine: str, model: str | None) -> dict:
    characters = len(spoken_text(text))
    if engine == "piper":
        credits = 0.0
        model_name = model or "piper-lessac-medium"
    elif engine == "elevenlabs":
        model_name = model or "eleven_multilingual_v2"
        if model_name not in CREDIT_PER_CHARACTER:
            raise ValueError(f"unknown ElevenLabs model {model_name}")
        credits = characters * CREDIT_PER_CHARACTER[model_name]
    else:
        raise ValueError("engine must be piper or elevenlabs")
    return {
        "engine": engine,
        "model": model_name,
        "characters": characters,
        "estimated_credits": round(credits, 2),
        "note": "ElevenLabs credits follow the account plan. Piper is local and costs nothing.",
    }


def cache_key(payload: dict) -> str:
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(raw.encode()).hexdigest()


def words_from_weights(words: list[str], weights: list[float], duration: float, offset: float) -> list[Word]:
    total = sum(weights) or 1.0
    t = offset
    out = []
    for word, weight in zip(words, weights):
        span = duration * weight / total
        out.append(Word(word, t, t + span))
        t += span
    if out:
        out[-1].end = offset + duration
    return out


def align_phonemes(sentence: str, phonemes: list[str], duration: float, offset: float) -> list[Word]:
    words = sentence.split()
    groups: list[list[str]] = []
    current: list[str] = []
    for phoneme in phonemes:
        if phoneme == " ":
            if current:
                groups.append(current)
                current = []
        else:
            current.append(phoneme)
    if current:
        groups.append(current)
    if len(groups) != len(words) or not words:
        weights = [max(1, len(word)) for word in words]
    else:
        weights = [max(1, sum(1 for phone in group if phone not in "ˈˌ")) for group in groups]
    return words_from_weights(words, weights, duration, offset)


def words_from_characters(characters: list[str], starts: list[float], ends: list[float], offset: float) -> list[Word]:
    words: list[Word] = []
    buf = ""
    start = None
    end = None
    for char, a, b in zip(characters, starts, ends):
        if char.isspace():
            if buf:
                words.append(Word(buf, offset + float(start), offset + float(end)))
                buf, start, end = "", None, None
            continue
        if start is None:
            start = a
        buf += char
        end = b
    if buf:
        words.append(Word(buf, offset + float(start), offset + float(end)))
    return words


def write_vtt(words: list[Word], path) -> None:
    """Group words into readable caption cues."""
    cues = []
    current: list[Word] = []
    for word in words:
        current.append(word)
        text = " ".join(item.text for item in current)
        if len(current) >= 8 or len(text) >= 42:
            cues.append(current)
            current = []
    if current:
        cues.append(current)
    lines = ["WEBVTT", ""]

    def stamp(seconds: float) -> str:
        ms = int(round(seconds * 1000))
        h, ms = divmod(ms, 3_600_000)
        m, ms = divmod(ms, 60_000)
        s, ms = divmod(ms, 1000)
        return f"{h:02d}:{m:02d}:{s:02d}.{ms:03d}"

    for cue in cues:
        lines.append(f"{stamp(cue[0].start)} --> {stamp(cue[-1].end)}")
        lines.append(" ".join(word.text for word in cue))
        lines.append("")
    path.write_text("\n".join(lines))
