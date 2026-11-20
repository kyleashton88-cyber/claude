"""Use the illustration engine when it is installed. Otherwise return None."""

from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]


def engine_root() -> Path | None:
    if importlib.util.find_spec("illustration_engine") is not None:
        return None
    candidate = REPO / "skills" / "illustration-engine"
    if (candidate / "illustration_engine" / "__main__.py").is_file():
        return candidate
    return None


def engine_installed() -> bool:
    if importlib.util.find_spec("illustration_engine") is not None:
        return True
    return engine_root() is not None


def render_cover(title: str, label: str, dest: Path) -> bool:
    """Draw one cover through the illustration engine. Never passes --llm."""
    if not engine_installed():
        return False
    prompt = json.dumps(
        {
            "type": "lesson_cover",
            "headline": title,
            "labels": [label, "EXAMPLE"],
        }
    )
    env = os.environ.copy()
    root = engine_root()
    if root is not None:
        env["PYTHONPATH"] = str(root) + os.pathsep + env.get("PYTHONPATH", "")
    dest.parent.mkdir(parents=True, exist_ok=True)
    proc = subprocess.run(
        [
            sys.executable,
            "-m",
            "illustration_engine",
            "render",
            prompt,
            "--preset",
            "thumbnail",
            "--size",
            "1280x720",
            "--out",
            str(dest),
        ],
        env=env,
        capture_output=True,
        text=True,
    )
    return proc.returncode == 0 and dest.is_file()
