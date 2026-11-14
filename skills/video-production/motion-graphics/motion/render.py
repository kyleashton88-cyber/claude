"""Render a shot list to H.264. Frames are piped at final size. No upscale."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

from lib.brand import FPS, H, W
from lib.ffmpeg_util import FFmpegError, ffmpeg_bin
from motion.components import DRAW
from motion.frame import Stage, background

DEFAULT_STILL = "programs/defi-program/assets/diagrams/liquidity-ladder.png"


def sample_sequence(still: Path | None = None) -> dict:
    image = str(still or DEFAULT_STILL)
    return {
        "fps": FPS,
        "width": W,
        "height": H,
        "shots": [
            {
                "kind": "title",
                "seconds": 4.0,
                "lines": ["A grid,", "in one picture"],
                "sub": "Illustrative prices. Not a forecast.",
                "caption": "A worked picture of how a grid is drawn",
                "lower_third": {"kicker": "Worked picture", "line": "Orders, a range, a buffer"},
            },
            {
                "kind": "candles",
                "seconds": 6.0,
                "title": "Price, as candles",
                "caption": "Open, high, low, and close. Nothing else is hiding in the candle.",
            },
            {
                "kind": "ladder",
                "seconds": 8.0,
                "title": "Orders on a ladder",
                "caption": "Buys sit below the price. Sells sit above. A cross fills the order.",
            },
            {
                "kind": "risk",
                "seconds": 5.5,
                "title": "Range, and the line past it",
                "caption": "The buffer is the gap between price and the liquidation line.",
            },
            {
                "kind": "still",
                "seconds": 5.5,
                "title": "An existing plate, set in motion",
                "caption": "The diagram was already drawn. The camera, the card, and the figure move.",
                "image": image,
                "fills": 6,
                "lower_third": {"kicker": "Existing still", "line": "Moved in layers. Not regenerated."},
            },
        ],
    }


def load_sequence(path: Path) -> dict:
    data = json.loads(path.read_text())
    if "shots" not in data:
        raise ValueError(f"{path} has no shots")
    return data


def shot_duration(sequence: dict) -> float:
    return float(sum(float(s["seconds"]) for s in sequence["shots"]))


def _shot_at(sequence: dict, t: float) -> tuple[dict, float, float]:
    cursor = 0.0
    shots = sequence["shots"]
    for shot in shots:
        dur = float(shot["seconds"])
        if t < cursor + dur:
            return shot, t - cursor, cursor
        cursor += dur
    last = shots[-1]
    dur = float(last["seconds"])
    return last, dur, cursor - dur


def render_frame(sequence: dict, t: float, base) -> "Image.Image":
    from PIL import Image

    shot, local, _start = _shot_at(sequence, t)
    kind = shot["kind"]
    if kind not in DRAW:
        raise KeyError(f"unknown shot kind {kind}")
    total = shot_duration(sequence)
    stage = Stage(base, local, float(shot["seconds"]), t, total)
    DRAW[kind](stage, shot, local)
    # Title draws its own lower third. Other shots opt in.
    if kind != "title" and shot.get("lower_third") and kind != "still":
        from motion.components import draw_lower_third

        draw_lower_third(stage, shot["lower_third"], local)
    title = None if kind == "title" else shot.get("title")
    stage.finish(title=title, caption=shot.get("caption"))
    return stage.im


def render_sequence(
    sequence: dict,
    dest: Path,
    *,
    crf: int = 18,
    preset: str = "medium",
    fps: int | None = None,
) -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    fps = int(fps or sequence.get("fps") or FPS)
    if int(sequence.get("width") or W) != W or int(sequence.get("height") or H) != H:
        raise ValueError("sequences are drawn at 1920×1080 and are not scaled afterwards")
    total = shot_duration(sequence)
    frames = max(1, int(round(total * fps)))
    cmd = [
        ffmpeg_bin(),
        "-y",
        "-hide_banner",
        "-loglevel",
        "error",
        "-f",
        "rawvideo",
        "-pix_fmt",
        "rgb24",
        "-s",
        f"{W}x{H}",
        "-r",
        str(fps),
        "-i",
        "-",
        "-c:v",
        "libx264",
        "-preset",
        preset,
        "-crf",
        str(crf),
        "-pix_fmt",
        "yuv420p",
        "-color_primaries",
        "bt709",
        "-color_trc",
        "bt709",
        "-colorspace",
        "bt709",
        "-movflags",
        "+faststart",
        "-an",
        str(dest),
    ]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    assert proc.stdin is not None
    base = background()
    try:
        for i in range(frames):
            t = min(total - 1e-3, i / fps)
            im = render_frame(sequence, t, base)
            proc.stdin.write(im.tobytes())
        proc.stdin.close()
    except BrokenPipeError:
        err = proc.stderr.read().decode() if proc.stderr else ""
        raise FFmpegError(err[-2000:]) from None
    err = proc.stderr.read().decode() if proc.stderr else ""
    code = proc.wait()
    if code != 0:
        raise FFmpegError(err[-2000:])
    return dest
