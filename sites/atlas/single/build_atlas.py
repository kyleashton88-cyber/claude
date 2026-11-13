#!/usr/bin/env python3
"""Run the course builder that writes dist/atlas/atlas.html."""
import runpy
from pathlib import Path

TARGET = Path(__file__).resolve().parents[3] / "dist" / "atlas" / "build_atlas.py"
runpy.run_path(str(TARGET), run_name="__main__")
