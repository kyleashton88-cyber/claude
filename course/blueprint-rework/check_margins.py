"""Sample a repaired master and report title or caption ink outside the 5% margin."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import repair_margins as rm


def check(path: Path, step: float = 3.0) -> int:
    cmd = [
        "ffmpeg", "-nostdin", "-v", "error", "-i", str(path),
        "-vf", f"fps=1/{step:.3f}",
        "-f", "rawvideo", "-pix_fmt", "rgb24", "-",
    ]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    assert proc.stdout is not None
    frame_bytes = rm.W * rm.H * 3
    n = 0
    bad = 0
    while True:
        buf = proc.stdout.read(frame_bytes)
        if len(buf) < frame_bytes:
            break
        frame = np.frombuffer(buf, dtype=np.uint8).reshape(rm.H, rm.W, 3)
        problems = rm.text_outside(frame)
        if problems:
            bad += 1
            if bad <= 8:
                print(f"  t={n * step:.0f}s {problems}")
        n += 1
    proc.wait()
    print(f"{path.name} samples {n} outside {bad}")
    return bad


if __name__ == "__main__":
    failed = 0
    for arg in sys.argv[1:]:
        failed += check(Path(arg))
    raise SystemExit(1 if failed else 0)
