#!/usr/bin/env python3
"""Lint the clean sample and the risky sample into test-outputs."""

from __future__ import annotations

import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))

from cli import main  # noqa: E402


def run(source: str, dest: str) -> None:
    os.chdir(HERE)
    code = main(["lint", source, "--out", str(Path("test-outputs") / dest)])
    if source.endswith("clean-lesson.yaml") and code != 0:
        raise SystemExit(code)
    if source.endswith("risky-script.txt") and code == 0:
        raise SystemExit("risky sample should flag")


if __name__ == "__main__":
    run("samples/clean-lesson.yaml", "clean")
    run("samples/risky-script.txt", "risky")
