"""Caption files. words.json is the schema the rest of the pipeline reads."""

from __future__ import annotations

import json
from pathlib import Path

from voice.align import Word

SCHEMA = "video-production.words.v1"
# Studio cap. The blueprint gate allows 20; cues are built to this stricter figure
# and then re-measured with the gate's own timestamp parse.
DISPLAY_CPS = 18.0


def words_payload(words: list[Word], *, engine: str, mood: str, method: str) -> dict:
    return {
        "schema": SCHEMA,
        "engine": engine,
        "mood": mood,
        "method": method,
        "words": [word.as_dict() for word in words],
    }


def write_words(path: Path, words: list[Word], *, engine: str, mood: str, method: str) -> None:
    path.write_text(json.dumps(words_payload(words, engine=engine, mood=mood, method=method), indent=2) + "\n")


def _stamp(seconds: float, srt: bool = False) -> str:
    ms = max(0, int(round(seconds * 1000)))
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    sep = "," if srt else "."
    return f"{h:02d}:{m:02d}:{s:02d}{sep}{ms:03d}"


def cues(words: list[Word], max_words: int = 8, max_chars: int = 42) -> list[list[Word]]:
    groups: list[list[Word]] = []
    current: list[Word] = []
    for word in words:
        trial = current + [word]
        text = " ".join(item.text for item in trial)
        if current and (len(trial) > max_words or len(text) > max_chars):
            groups.append(current)
            current = [word]
        else:
            current = trial
    if current:
        groups.append(current)
    return groups


def _cue_end(cue: list[Word], following: float | None) -> float:
    """Hold a cue long enough to read, without running into the next cue."""
    start = cue[0].start
    end = cue[-1].end
    text = " ".join(word.text for word in cue)
    need = len(text) / DISPLAY_CPS
    if end - start < need:
        end = start + need
    if following is not None:
        end = min(end, max(following, start + 0.2))
    return max(end, start + 0.2)


def collapse_repeated_tokens(words: list[Word]) -> list[Word]:
    """Drop a second copy of a token that abuts the first.

    Picture cuts used to emit the same aligned word twice, back to back.
    The narration said it once. A real repeat, with a gap, stays.
    """
    kept: list[Word] = []
    for word in words:
        if kept and kept[-1].text == word.text and word.start <= kept[-1].end + 0.03:
            prev = kept[-1]
            kept[-1] = Word(prev.text, prev.start, max(prev.end, word.end))
            continue
        kept.append(Word(word.text, word.start, word.end))
    return kept


def readable_word_times(words: list[Word], limit: float = DISPLAY_CPS) -> list[Word]:
    """Give every word enough display time, using slack from earlier words.

    Alignment sometimes parks a long word on several seconds and then stacks
    the rest of the sentence into 50ms slots. Those slots cannot be read.
    Pull the stacked words back into the spare time. Do not move the first
    word earlier than it was spoken, and do not let windows overlap.
    """
    if not words:
        return []
    timed = [Word(word.text, word.start, max(word.end, word.start + 0.05)) for word in words]
    anchor = timed[0].start
    for _ in range(len(timed) + 2):
        changed = False
        for index in range(len(timed) - 1, -1, -1):
            word = timed[index]
            need = (len(word.text) + 1) / limit
            if word.end - word.start + 1e-9 >= need:
                continue
            timed[index] = Word(word.text, word.end - need, word.end)
            changed = True
            if index and timed[index - 1].end > timed[index].start:
                prev = timed[index - 1]
                timed[index - 1] = Word(prev.text, prev.start, timed[index].start)
        if timed[0].start < anchor:
            shift = anchor - timed[0].start
            timed = [Word(word.text, word.start + shift, word.end + shift) for word in timed]
            changed = True
        for index in range(len(timed) - 1):
            if timed[index].end <= timed[index + 1].start + 1e-9:
                continue
            nxt = timed[index + 1]
            start = timed[index].end
            need = (len(nxt.text) + 1) / limit
            end = max(nxt.end, start + need)
            timed[index + 1] = Word(nxt.text, start, end)
            changed = True
        if not changed:
            break
    return timed


def _rounded(seconds: float) -> float:
    """Match the gate: timestamps are whole milliseconds, then parsed back."""
    return max(0, int(round(seconds * 1000))) / 1000.0


def fitted_cues(words: list[Word], limit: float = DISPLAY_CPS) -> list[tuple[float, float, str]]:
    """Cues that keep every word and stay at or under `limit` characters per second.

    The speed uses the millisecond timestamps the caption file will actually
    store, which is the span the quality gate measures.
    """
    paced = readable_word_times(collapse_repeated_tokens(words), limit)
    grouped = cues(paced)
    rows: list[list] = []
    for group in grouped:
        rows.append([
            group[0].start,
            group[-1].end,
            " ".join(word.text for word in group),
        ])
    for index, row in enumerate(rows[:-1]):
        row[1] = max(row[1], rows[index + 1][0])
    _hold_for_speed(rows, limit)
    return [(float(row[0]), float(row[1]), str(row[2])) for row in rows]


def _hold_for_speed(rows: list[list], limit: float) -> None:
    """Lengthen a fast cue without delaying the words after it."""
    for _ in range(len(rows) * 4 + 8):
        moved = False
        for index, row in enumerate(rows):
            start = _rounded(row[0])
            end = _rounded(row[1])
            if end <= start:
                end = start + 0.001
            span = end - start
            if span > 0 and len(row[2]) / span <= limit + 1e-9:
                row[0], row[1] = start, end
                continue
            need = len(row[2]) / limit
            new_end = start + need + 0.002
            if index + 1 < len(rows):
                new_end = min(new_end, rows[index + 1][0] + 0.20)
            if new_end > end + 0.0005:
                row[0], row[1] = start, new_end
                moved = True
                break
            if index + 1 < len(rows):
                nxt = rows[index + 1]
                row[2] = f"{row[2]} {nxt[2]}".strip()
                row[1] = max(new_end, nxt[1])
                del rows[index + 1]
                moved = True
                break
            row[0], row[1] = start, new_end
            moved = True
            break
        if not moved:
            return
    raise RuntimeError("caption cues could not be held under the reading-speed cap")


def render_vtt(words: list[Word], limit: float = DISPLAY_CPS) -> str:
    lines = ["WEBVTT", ""]
    for start, end, text in fitted_cues(words, limit):
        lines.append(f"{_stamp(start)} --> {_stamp(end)}")
        lines.append(text)
        lines.append("")
    return "\n".join(lines) + "\n"


def render_srt(words: list[Word], limit: float = DISPLAY_CPS) -> str:
    lines: list[str] = []
    for index, (start, end, text) in enumerate(fitted_cues(words, limit), start=1):
        lines.append(str(index))
        lines.append(f"{_stamp(start, srt=True)} --> {_stamp(end, srt=True)}")
        lines.append(text)
        lines.append("")
    return "\n".join(lines) + "\n"


def write_vtt(path: Path, words: list[Word]) -> None:
    path.write_text(render_vtt(words), encoding="utf-8")


def write_srt(path: Path, words: list[Word]) -> None:
    path.write_text(render_srt(words), encoding="utf-8")


def refit_vtt_text(text: str, limit: float = DISPLAY_CPS) -> str:
    """Lengthen or merge cues that are still over the cap. Do not delete words.

    Measurement uses the quality gate's parser, so a millisecond-rounded span
    cannot slip past this cap and then fail the gate.
    """
    import sys

    gate_root = Path(__file__).resolve().parents[2] / "quality-gate"
    if str(gate_root) not in sys.path:
        sys.path.insert(0, str(gate_root))
    from gate.captions import parse_captions

    parsed = parse_captions(text)
    if not parsed:
        return text if text.endswith("\n") else text + "\n"
    rows = [[cue.start, cue.end, cue.text] for cue in parsed]
    _hold_for_speed(rows, limit)
    # A cue that is still one fast word, hard against the next cue, joins that neighbour.
    merged: list[list] = []
    for row in rows:
        if not merged:
            merged.append(row)
            continue
        start = _rounded(merged[-1][0])
        end = _rounded(row[0])
        span = end - start
        combined = f"{merged[-1][2]} {row[2]}".strip()
        own_span = _rounded(merged[-1][1]) - start
        if own_span > 0 and len(merged[-1][2]) / own_span <= limit + 1e-9 and len(merged[-1][2]) <= 42:
            merged.append(row)
            continue
        if len(combined) <= 42 and span > 0:
            merged[-1][1] = max(merged[-1][1], row[1])
            merged[-1][2] = combined
        else:
            merged.append(row)
    _hold_for_speed(merged, limit)
    lines = ["WEBVTT", ""]
    for start, end, payload in merged:
        wrapped = _wrap_lines(payload)
        # One line of at most 42 characters per cue. Joining the wrapped
        # lines used to push a single caption line past the gate.
        groups = [[line] for line in wrapped] or [[payload]]
        weights = [max(1, sum(len(line) for line in group)) for group in groups]
        total = float(sum(weights))
        cursor = start
        span = max(0.0, end - start)
        for index, group in enumerate(groups):
            if index == len(groups) - 1:
                stop = end
            else:
                stop = cursor + span * weights[index] / total
            lines.append(f"{_stamp(cursor)} --> {_stamp(stop)}")
            lines.extend(group)
            lines.append("")
            cursor = stop
    return "\n".join(lines) + "\n"


def _wrap_lines(text: str, width: int = 42) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        trial = f"{current} {word}".strip()
        if current and len(trial) > width:
            lines.append(current)
            current = word
        else:
            current = trial
    if current:
        lines.append(current)
    return lines or [text]


def write_chapters(path: Path, sections: list[tuple[float, str]]) -> None:
    """YouTube chapter file. The first mark is always 0:00."""
    lines = []
    for start, title in sections:
        whole = int(start)
        h, rem = divmod(whole, 3600)
        m, s = divmod(rem, 60)
        stamp = f"{h:02d}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"
        lines.append(f"{stamp} {title}")
    path.write_text("\n".join(lines) + "\n")


def caption_box(frame_w: int = 1920, frame_h: int = 1080, font_px: int = 42, lines: int = 2) -> dict:
    """Where a burned caption sits. The box must stay inside a 5% margin."""
    margin_x = int(round(frame_w * 0.05))
    margin_y = int(round(frame_h * 0.05))
    box_h = font_px * lines + 28
    top = frame_h - margin_y - box_h
    return {
        "x": margin_x,
        "y": top,
        "w": frame_w - 2 * margin_x,
        "h": box_h,
        "margin_x": margin_x,
        "margin_y": margin_y,
    }


def margin_ok(box: dict, frame_w: int = 1920, frame_h: int = 1080) -> bool:
    return (
        box["x"] >= int(frame_w * 0.05) - 1
        and box["y"] >= int(frame_h * 0.05) - 1
        and box["x"] + box["w"] <= frame_w - int(frame_w * 0.05) + 1
        and box["y"] + box["h"] <= frame_h - int(frame_h * 0.05) + 1
    )
