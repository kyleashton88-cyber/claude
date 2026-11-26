#!/usr/bin/env python3
"""Plan the sample lesson into test-outputs."""

from __future__ import annotations

import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))

from cli import main  # noqa: E402

if __name__ == "__main__":
    os.chdir(HERE)
    raise SystemExit(main(["plan", "samples/lesson.yaml", "--out", "test-outputs"]))
