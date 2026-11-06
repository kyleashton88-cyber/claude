"""Flag a master whose picture stays identical for more than 8 seconds.

Samples 2 frames a second at 160x90. A cut to a new crop changes the sample,
so a legal 7.5 second piece stays under the limit.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def longest_hold(path: Path, fps: int = 2) -> tuple[float, float]:
    width, height = 160, 90
    raw = subprocess.check_output([
        "ffmpeg", "-v", "error", "-i", str(path),
        "-vf", f"fps={fps},scale={width}:{height}",
        "-f", "rawvideo", "-pix_fmt", "gray", "-",
    ])
    frame = width * height
    count = len(raw) // frame
    previous = None
    run = 0
    worst = 0
    worst_at = 0.0
    for index in range(count):
        buf = raw[index * frame:(index + 1) * frame]
        if previous is not None and buf == previous:
            run += 1
        else:
            if run > worst:
                worst = run
                worst_at = (index - run) / fps
            run = 1
        previous = buf
    if run > worst:
        worst = run
        worst_at = (count - run) / fps
    return worst / fps, worst_at


def main() -> None:
    path = Path(sys.argv[1])
    limit = float(sys.argv[2]) if len(sys.argv) > 2 else 8.0
    seconds, at = longest_hold(path)
    print(f"{path.name} longest hold {seconds:.2f}s at {at:.1f}s")
    if seconds > limit:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
