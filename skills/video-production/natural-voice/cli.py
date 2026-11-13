#!/usr/bin/env python3
"""Natural voice CLI. Piper is local. ElevenLabs is stock voices only.

  python3 cli.py estimate --engine elevenlabs --text "Hello there."
  python3 cli.py say --engine piper --text "Hello there." --out out.wav
  python3 cli.py say --engine elevenlabs --voice Brian --text "Hello." --yes --out out.wav
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from voice.markup import estimate  # noqa: E402
from voice.speak import Speaker, render_to_file  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Piper or ElevenLabs stock voice")
    sub = parser.add_subparsers(dest="cmd", required=True)
    est = sub.add_parser("estimate")
    est.add_argument("--engine", choices=("piper", "elevenlabs"), required=True)
    est.add_argument("--model", default=None)
    est.add_argument("--text", required=True)
    say = sub.add_parser("say")
    say.add_argument("--engine", choices=("piper", "elevenlabs"), default="piper")
    say.add_argument("--voice", default=None)
    say.add_argument("--model", default=None)
    say.add_argument("--text", required=True)
    say.add_argument("--out", type=Path, required=True)
    say.add_argument("--yes", action="store_true", help="Required before an ElevenLabs call, after the estimate is printed.")
    say.add_argument("--cache", type=Path, default=Path.home() / ".cache" / "video-production" / "voice")
    args = parser.parse_args(argv)
    if args.cmd == "estimate":
        print(json.dumps(estimate(args.text, args.engine, args.model), indent=2))
        return 0
    voice = args.voice or ("lessac" if args.engine == "piper" else "Brian")
    quote = estimate(args.text, args.engine, args.model)
    print(json.dumps(quote, indent=2))
    if args.engine == "elevenlabs" and not args.yes:
        print("Dry run. Re-run with --yes to spend the estimated credits.")
        return 0
    speaker = Speaker(engine=args.engine, voice=voice, model=args.model, cache_dir=args.cache)
    payload = render_to_file(args.text, args.out, speaker)
    print(json.dumps({"wav": str(args.out), "alignment": payload["alignment"], "words": len(payload["words"])}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
