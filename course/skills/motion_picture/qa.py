"""Creative Studio checks for a finished lesson master. Read-only."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image

BRANDS = re.compile(
    r"bybit|binance|pionex|coinbase|okx|kucoin|kraken|bitget|market pros",
    re.I,
)


def _run(cmd: list[str]) -> str:
    return subprocess.check_output(cmd, stderr=subprocess.STDOUT, text=True, errors="replace")


def probe(path: Path) -> dict:
    import json
    text = _run([
        "ffprobe", "-v", "error", "-print_format", "json",
        "-show_entries", "format=duration:stream=codec_type,codec_name,width,height",
        str(path),
    ])
    data = json.loads(text)
    info = {"duration": data.get("format", {}).get("duration", "0")}
    for stream in data.get("streams", []):
        if stream.get("codec_type") == "video":
            info["width"] = str(stream.get("width"))
            info["height"] = str(stream.get("height"))
            info["codec_name"] = stream.get("codec_name")
    return info


def loudness(path: Path) -> str:
    log = _run(["ffmpeg", "-hide_banner", "-i", str(path), "-vn", "-af", "ebur128=peak=true", "-f", "null", "-"])
    keep = False
    lines = []
    for line in log.splitlines():
        if "Integrated loudness" in line:
            keep = True
        if keep:
            lines.append(line)
        if keep and "Peak:" in line:
            break
    return "\n".join(lines)


def motion_score(path: Path, a: float, b: float) -> float:
    work = Path("/tmp/bp-qa")
    work.mkdir(exist_ok=True)
    fa, fb = work / "a.jpg", work / "b.jpg"
    subprocess.check_call(["ffmpeg", "-y", "-v", "error", "-ss", str(a), "-i", str(path), "-frames:v", "1", str(fa)])
    subprocess.check_call(["ffmpeg", "-y", "-v", "error", "-ss", str(b), "-i", str(path), "-frames:v", "1", str(fb)])
    ia = np.asarray(Image.open(fa).resize((480, 270)), dtype=np.float32)
    ib = np.asarray(Image.open(fb).resize((480, 270)), dtype=np.float32)
    return float(np.mean(np.abs(ia - ib)))


def check(path: Path) -> list[str]:
    problems = []
    info = probe(path)
    dur = float(info.get("duration") or 0)
    if dur < 15 * 60:
        problems.append(f"duration {dur:.1f}s is under 15 minutes")
    if info.get("width") != "1920" or info.get("height") != "1080":
        problems.append(f"frame is {info.get('width')}x{info.get('height')}")
    if info.get("codec_name") not in {None, "h264"}:
        problems.append(f"video codec {info.get('codec_name')}")
    # Motion across the lesson. The open can be a title easing in.
    # A later second must show the path or the playhead actually moving.
    dur = float(info.get("duration") or 0)
    scores = [motion_score(path, t, t + 1) for t in (30, dur * 0.45, max(40, dur * 0.7))]
    if max(scores) < 1.2:
        problems.append(f"no clear motion in the body (scores {', '.join(f'{s:.2f}' for s in scores)})")
    # Brand scan on three frames via tesseract when it is installed.
    if subprocess.call(["bash", "-lc", "command -v tesseract"], stdout=subprocess.DEVNULL) == 0:
        for t in (12, dur * 0.5, max(1, dur - 8)):
            frame = Path(f"/tmp/bp-qa/f{int(t)}.png")
            subprocess.check_call([
                "ffmpeg", "-y", "-v", "error", "-ss", f"{t:.2f}", "-i", str(path), "-frames:v", "1", str(frame),
            ])
            text = _run(["tesseract", str(frame), "stdout", "--psm", "6"])
            if BRANDS.search(text):
                problems.append(f"brand text at {t:.0f}s: {BRANDS.search(text).group(0)}")
    return problems


def main() -> None:
    path = Path(sys.argv[1])
    problems = check(path)
    print(loudness(path))
    if problems:
        print("FAIL")
        for item in problems:
            print("-", item)
        raise SystemExit(1)
    print("PASS", path)


if __name__ == "__main__":
    main()
