#!/usr/bin/env python3
"""Generate narration for every video scene with Kokoro TTS (offline).

Usage: python3 build_vo.py <scenes.json> <out_dir> [voice]
scenes.json: [{"id": "...", "vo": "..."}]. Writes <id>.wav and durations.json.

Needs: pip install kokoro-onnx soundfile, plus kokoro-v1.0.onnx and
voices-v1.0.bin (github.com/thewh1teagle/kokoro-onnx releases) in
KOKORO_DIR (default: ./tts next to this script).
"""
import json
import os
import sys

import soundfile as sf
from kokoro_onnx import Kokoro

scenes_path, out_dir = sys.argv[1], sys.argv[2]
voice = sys.argv[3] if len(sys.argv) > 3 else "af_heart"
model_dir = os.environ.get("KOKORO_DIR", os.path.join(os.path.dirname(__file__), "tts"))
kokoro = Kokoro(os.path.join(model_dir, "kokoro-v1.0.onnx"), os.path.join(model_dir, "voices-v1.0.bin"))
lang = "en-gb" if voice.startswith("b") else "en-us"

os.makedirs(out_dir, exist_ok=True)
durations = {}
for scene in json.load(open(scenes_path)):
    samples, rate = kokoro.create(scene["vo"], voice=voice, speed=0.97, lang=lang)
    sf.write(os.path.join(out_dir, f"{scene['id']}.wav"), samples, rate)
    durations[scene["id"]] = len(samples) / rate
json.dump(durations, open(os.path.join(out_dir, "durations.json"), "w"), indent=1)
print(f"{len(durations)} clips, {sum(durations.values()):.1f}s of narration ({voice})")
