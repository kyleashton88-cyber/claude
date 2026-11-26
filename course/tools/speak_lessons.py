"""Write course/audio/<id>.wav with Kokoro af_heart.

New narration goes through skills/video-production/natural-voice (Kokoro af_heart).
This script remains so an existing course render can still fill course/audio.

Skips a wav that is already at least 100 KB. One lesson at a time.
  python3 course/tools/speak_lessons.py
  python3 course/tools/speak_lessons.py --shard 0 --shards 2
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import soundfile as sf

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from queue_order import priority  # noqa: E402

ROOT = HERE.parents[1]
SCRIPTS = ROOT / "course" / "scripts"
AUDIO = ROOT / "course" / "audio"
VOICE = "af_heart"
SR = 24000
# af_heart at speed 1 is near 195 wpm. 0.78 lands just under the 143 wpm picture track
# so -shortest does not cut the outro.
SPEED = 0.78


def lesson_paths(shard: int, shards: int) -> list[Path]:
    paths = sorted(SCRIPTS.glob("*.json"), key=lambda p: (*priority(p.stem), p.stem))
    return [p for i, p in enumerate(paths) if i % shards == shard]


def already(path: Path) -> bool:
    return path.is_file() and path.stat().st_size >= 100_000


def speak(pipeline, script: dict, dest: Path) -> None:
    gap = np.zeros(int(0.35 * SR), dtype=np.float32)
    parts: list[np.ndarray] = []
    for beat in script["beats"]:
        chunks = []
        for _gs, _ps, audio in pipeline(beat["vo"], voice=VOICE, speed=SPEED):
            chunks.append(np.asarray(audio, dtype=np.float32))
        if chunks:
            parts.append(np.concatenate(chunks))
            parts.append(gap)
    if not parts:
        raise SystemExit(f"no audio for {script['id']}")
    dest.parent.mkdir(parents=True, exist_ok=True)
    sf.write(dest, np.concatenate(parts), SR)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--shard", type=int, default=0)
    parser.add_argument("--shards", type=int, default=1)
    parser.add_argument("--limit", type=int, default=0)
    args = parser.parse_args()
    from kokoro import KPipeline
    print(f"kokoro voice {VOICE} speed {SPEED} shard {args.shard}/{args.shards}", flush=True)
    pipeline = KPipeline(lang_code="a")
    done = 0
    paths = lesson_paths(args.shard, args.shards)
    if args.limit:
        paths = paths[: args.limit]
    for path in paths:
        script = json.loads(path.read_text())
        dest = AUDIO / f"{script['id']}.wav"
        if already(dest):
            print(f"skip {script['id']}", flush=True)
            continue
        speak(pipeline, script, dest)
        done += 1
        print(f"wrote {dest.relative_to(ROOT)} {dest.stat().st_size}", flush=True)
    print(f"shard {args.shard} wrote {done}", flush=True)


if __name__ == "__main__":
    main()
