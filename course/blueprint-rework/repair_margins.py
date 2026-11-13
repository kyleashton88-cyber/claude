"""Pin Blueprint titles and captions inside a 5% safe margin.

The stills masters scale the frame and crop it with a slow drift. The section
title is part of that picture, so it slides off the top and the left. The
caption bar was copied back at a fixed 72 px, which is inside the frame and
outside the 5% margin (96 px across, 54 px down).

This pass keeps the chart motion, pulls bright chart ink back inside the
margin, redraws the section title in one place, and moves the caption and the
disclaimer in from the edges. The voice is copied through a limiter so the
true peak sits at or under -1.5 dBTP. Integrated loudness is already about
-16 LUFS.

Refuses Elite ids.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
import types
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
if "soundfile" not in sys.modules:
    sys.modules["soundfile"] = types.ModuleType("soundfile")
sys.path.insert(0, str(ROOT / "course" / "blueprint-rework"))

import lesson_scripts  # noqa: E402
import stills_pass  # noqa: E402

W, H = 1920, 1080
FPS = 30
SAFE_X = 96   # 5% of 1920
SAFE_Y = 54   # 5% of 1080
SAFE_R = W - SAFE_X
SAFE_B = H - SAFE_Y
NAVY = np.array([5, 10, 18], dtype=np.uint8)
CYAN = (0, 212, 255)
FONT = "/usr/share/fonts/truetype/macos/Inter-Bold.ttf"
TITLE_SIZE = 26
TITLE_X = 100
TITLE_Y = 60
HEADER_Y = 80
HEADER_X = 820
CHART_TOP = 96
CHART_BOT = 860
CAPTION_BAND = (888, 990)
DISCLAIMER_BAND = (990, 1040)


def chapters_for(sid: str) -> list[str]:
    if sid.startswith("el-"):
        raise SystemExit(f"refusing Elite id {sid}")
    shots = stills_pass.prepare(lesson_scripts.build(sid))
    return [shot.get("chapter") or "" for shot in shots]


def _ink_bbox(arr: np.ndarray) -> tuple[int, int, int, int] | None:
    ink = arr[:, :, 2].astype(np.int16) > 80
    ys, xs = np.where(ink)
    if len(xs) == 0:
        return None
    return int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())


def render_title(text: str) -> np.ndarray:
    """Cyan title on navy, cropped to the ink with a 2 px pad."""
    font = ImageFont.truetype(FONT, TITLE_SIZE)
    canvas = Image.new("RGB", (1600, 80), tuple(int(v) for v in NAVY))
    draw = ImageDraw.Draw(canvas)
    draw.text((4, 4), text, font=font, fill=CYAN)
    arr = np.asarray(canvas, dtype=np.uint8)
    box = _ink_bbox(arr)
    if box is None:
        raise SystemExit(f"title rendered with no ink: {text}")
    x0, y0, x1, y1 = box
    sprite = arr[max(0, y0 - 2): y1 + 3, max(0, x0 - 2): x1 + 3]
    if TITLE_X + sprite.shape[1] > SAFE_R or TITLE_Y + sprite.shape[0] > CHART_TOP:
        raise SystemExit(f"title does not fit in the safe header: {text} {sprite.shape}")
    return sprite


def title_sprites(names: list[str]) -> list[np.ndarray]:
    cache: dict[str, np.ndarray] = {}
    out = []
    for name in names:
        if name not in cache:
            cache[name] = render_title(name)
        out.append(cache[name])
    return out


def _cyan_mask(region: np.ndarray) -> np.ndarray:
    r = region[:, :, 0].astype(np.int16)
    g = region[:, :, 1].astype(np.int16)
    b = region[:, :, 2].astype(np.int16)
    return (b > 140) & (g > 110) & (r < 120) & ((b - r) > 40)


def _dilate(mask: np.ndarray, times: int = 2) -> np.ndarray:
    out = mask.copy()
    for _ in range(times):
        grown = out.copy()
        grown[1:] |= out[:-1]
        grown[:-1] |= out[1:]
        grown[:, 1:] |= out[:, :-1]
        grown[:, :-1] |= out[:, 1:]
        out = grown
    return out


def erase_drifting_title(frame: np.ndarray) -> None:
    """Remove the section title the crop has been sliding around.

    A vertical wipe is a tall cyan stroke. Those columns stay.
    """
    region = frame[:HEADER_Y, :HEADER_X]
    cyan = _cyan_mask(region)
    below = frame[HEADER_Y: HEADER_Y + 90, :HEADER_X]
    tall = _cyan_mask(below).sum(axis=0) > 24
    cyan[:, tall] = False
    region[_dilate(cyan)] = NAVY


def paste_title(frame: np.ndarray, sprite: np.ndarray) -> None:
    sh, sw = sprite.shape[:2]
    y, x = TITLE_Y, TITLE_X
    dest = frame[y: y + sh, x: x + sw]
    ink = sprite[:, :, 2].astype(np.int16) > 40
    dest[ink] = sprite[ink]


def draw_progress(frame: np.ndarray, progress: float) -> None:
    """Inset meter. The old one rode the drift and touched the frame edge."""
    frame[:8, :] = NAVY
    span = SAFE_R - SAFE_X
    width = max(0, min(span, int(round(progress * span))))
    if width:
        frame[1:5, SAFE_X: SAFE_X + width] = np.array(CYAN, dtype=np.uint8)


def _shift_rect(frame: np.ndarray, y0: int, y1: int, x0: int, x1: int, dx: int, dy: int) -> None:
    """Slide a navy rectangle. Overlap is safe because the source is copied first."""
    src = frame[y0:y1, x0:x1].copy()
    frame[y0:y1, x0:x1] = NAVY
    frame[y0 + dy: y1 + dy, x0 + dx: x1 + dx] = src


def place_footer(frame: np.ndarray) -> None:
    """Move the pinned caption and disclaimer into the safe margin.

    The stills pass left both at x=73. The disclaimer also sits at y=1055,
    25 px from the bottom. The words are the original pixels, only moved.
    """
    # Caption ink is y=906..937, x=73..1248 on every lesson from this renderer.
    _shift_rect(frame, 896, 960, 60, 1500, 28, 0)
    # Disclaimer ink is y=1037..1055. Land the bottom at 1023 (57 px of margin).
    _shift_rect(frame, 1028, 1064, 60, 900, 28, -32)


def clamp_chart(frame: np.ndarray) -> tuple[int, int]:
    """Shift the picture so chart ink stays inside the margin.

    The caption bar is not part of the drift, so it is not moved here.
    """
    sub = frame[CHART_TOP:CHART_BOT:4, ::4]
    bright = sub.max(axis=2) > 80
    cols = bright.any(axis=0)
    rows = bright.any(axis=1)
    if not cols.any():
        return 0, 0
    left = int(np.argmax(cols)) * 4
    right = int(len(cols) - 1 - np.argmax(cols[::-1])) * 4 + 3
    top = int(np.argmax(rows)) * 4 + CHART_TOP
    bottom = int(len(rows) - 1 - np.argmax(rows[::-1])) * 4 + CHART_TOP
    dx = 0
    if left < SAFE_X:
        dx = SAFE_X - left
    if right + dx > SAFE_R:
        dx -= (right + dx) - SAFE_R
    dy = 0
    if top < CHART_TOP:
        dy = CHART_TOP - top
    if bottom + dy > CHART_BOT - 8:
        dy -= (bottom + dy) - (CHART_BOT - 8)
    if dx:
        _roll_x(frame, dx)
    if dy:
        _roll_y_picture(frame, dy)
    return dx, dy


def _roll_x(frame: np.ndarray, dx: int) -> None:
    picture = frame[:CHART_BOT]
    out = np.empty_like(picture)
    if dx > 0:
        out[:, dx:] = picture[:, :-dx]
        out[:, :dx] = NAVY
    elif dx < 0:
        shift = -dx
        out[:, :-shift] = picture[:, shift:]
        out[:, -shift:] = NAVY
    else:
        return
    frame[:CHART_BOT] = out


def _roll_y_picture(frame: np.ndarray, dy: int) -> None:
    picture = frame[:CHART_BOT]
    out = np.empty_like(picture)
    if dy > 0:
        out[dy:] = picture[:-dy]
        out[:dy] = NAVY
    elif dy < 0:
        shift = -dy
        out[:-shift] = picture[shift:]
        out[-shift:] = NAVY
    else:
        return
    frame[:CHART_BOT] = out


def repair_frame(frame: np.ndarray, sprite: np.ndarray, progress: float) -> np.ndarray:
    clamp_chart(frame)
    erase_drifting_title(frame)
    paste_title(frame, sprite)
    draw_progress(frame, progress)
    place_footer(frame)
    return frame


def detect_shots(path: Path, expected: int) -> list[int]:
    """Return the frame index where each shot's caption first appears."""
    cmd = [
        "ffmpeg", "-nostdin", "-v", "error", "-i", str(path),
        "-vf", "fps=4,crop=1320:48:80:900",
        "-f", "rawvideo", "-pix_fmt", "rgb24", "-",
    ]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    assert proc.stdout is not None
    cw, ch = 1320, 48
    prev = None
    starts = [0]
    n = 0
    while True:
        buf = proc.stdout.read(cw * ch * 3)
        if len(buf) < cw * ch * 3:
            break
        band = np.frombuffer(buf, dtype=np.uint8).reshape(ch, cw, 3)
        small = band[::2, ::4].mean(axis=2) > 100
        if prev is not None:
            changed = int(np.count_nonzero(small != prev))
            if changed > 40 and (n * FPS // 4) - starts[-1] > FPS:
                starts.append(n * FPS // 4)
        prev = small
        n += 1
    proc.wait()
    if len(starts) != expected:
        raise SystemExit(
            f"{path.name}: found {len(starts)} caption changes, script has {expected} shots"
        )
    return starts


def shot_at(starts: list[int], frame_index: int) -> int:
    lo, hi = 0, len(starts) - 1
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if starts[mid] <= frame_index:
            lo = mid
        else:
            hi = mid - 1
    return lo


def text_outside(frame: np.ndarray) -> list[str]:
    """Titles and captions whose ink crosses the safe margin. Ignores the meter."""
    problems = []
    title = frame[8:HEADER_Y, :HEADER_X]
    cyan = _cyan_mask(title)
    # The shot wipe is a full-height cyan stroke. It is not the section title.
    cyan[:, cyan.sum(axis=0) > 36] = False
    ys, xs = np.where(cyan)
    if len(xs):
        if int(xs.min()) < SAFE_X or int(ys.min()) + 8 < SAFE_Y:
            problems.append(f"title ink x={int(xs.min())} y={int(ys.min()) + 8}")
        if int(xs.max()) > SAFE_R:
            problems.append(f"title right {int(xs.max())}")
    for name, (y0, y1) in (("caption", CAPTION_BAND), ("disclaimer", DISCLAIMER_BAND)):
        band = frame[y0:y1]
        luma = band.astype(np.int16).mean(axis=2)
        ys, xs = np.where(luma > 40)
        if len(xs) == 0:
            problems.append(f"{name} missing")
            continue
        if int(xs.min()) < SAFE_X or int(xs.max()) > SAFE_R:
            problems.append(f"{name} x={int(xs.min())}..{int(xs.max())}")
        if y0 + int(ys.max()) > SAFE_B or y0 + int(ys.min()) < SAFE_Y:
            problems.append(f"{name} y={y0 + int(ys.min())}..{y0 + int(ys.max())}")
    return problems


def encode(src: Path, dest: Path, sprites: list[np.ndarray], starts: list[int]) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    probe = subprocess.check_output([
        "ffprobe", "-v", "error", "-select_streams", "v:0",
        "-show_entries", "stream=nb_frames", "-of", "csv=p=0", str(src),
    ], text=True).strip()
    total = int(probe)
    log_path = dest.with_suffix(".ffmpeg.log")
    err = open(log_path, "w")
    decode = subprocess.Popen(
        [
            "ffmpeg", "-nostdin", "-v", "error", "-i", str(src),
            "-f", "rawvideo", "-pix_fmt", "rgb24", "-",
        ],
        stdout=subprocess.PIPE,
        stderr=err,
    )
    enc = subprocess.Popen(
        [
            "ffmpeg", "-y", "-nostdin", "-v", "error",
            "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
            "-i", str(src),
            "-map", "0:v", "-map", "1:a",
            "-af", "alimiter=limit=0.841:attack=5:release=80:level=false",
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", "-pix_fmt", "yuv420p",
            "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
            "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
            "-movflags", "+faststart",
            str(dest),
        ],
        stdin=subprocess.PIPE,
        stderr=err,
    )
    assert decode.stdout is not None and enc.stdin is not None
    frame_bytes = W * H * 3
    n = 0
    checked = 0
    try:
        while True:
            buf = decode.stdout.read(frame_bytes)
            if len(buf) < frame_bytes:
                break
            frame = np.frombuffer(buf, dtype=np.uint8).reshape(H, W, 3).copy()
            shot = shot_at(starts, n)
            progress = min(1.0, n / max(1, total - 1))
            repair_frame(frame, sprites[shot], progress)
            if n % (FPS * 20) == 0:
                bad = text_outside(frame)
                checked += 1
                if bad:
                    raise SystemExit(f"{src.name} t={n / FPS:.1f}s still outside margin: {bad}")
            enc.stdin.write(frame.tobytes())
            n += 1
            if n % (FPS * 60) == 0:
                print(f"  {src.stem} {n / FPS:.0f}s", flush=True)
    finally:
        try:
            enc.stdin.close()
        except BrokenPipeError:
            pass
        if decode.poll() is None:
            decode.kill()
        code = enc.wait()
        decode.wait()
        err.close()
    if code != 0:
        raise SystemExit(f"encode failed {code} for {src.name}")
    print(f"WROTE {dest} frames {n} spot-checks {checked}", flush=True)


def repair_one(sid: str, src: Path, dest: Path) -> None:
    names = chapters_for(sid)
    sprites = title_sprites(names)
    print(f"{sid} detecting {len(names)} shots", flush=True)
    starts = detect_shots(src, len(names))
    encode(src, dest, sprites, starts)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--id", required=True)
    ap.add_argument("--src", type=Path)
    ap.add_argument("--dest", type=Path)
    args = ap.parse_args()
    src = args.src or (ROOT / "course" / "masters-stills" / f"{args.id}.mp4")
    dest = args.dest or src
    repair_one(args.id, src, dest)


if __name__ == "__main__":
    main()
