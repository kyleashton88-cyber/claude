#!/usr/bin/env python3
"""Turn consented recordings into a Piper dataset. Does not train."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import wave
from pathlib import Path

PLACEHOLDERS = {"YOUR NAME", "YYYY-MM-DD", ""}


def consent_ok(path: Path) -> tuple[bool, str]:
    if not path.is_file():
        return False, "consent file is missing"
    text = path.read_text()
    if "I consent" not in text:
        return False, "consent statement must contain 'I consent'"
    name = ""
    for line in text.splitlines():
        if line.lower().startswith("name:"):
            name = line.split(":", 1)[1].strip()
    if name in PLACEHOLDERS:
        return False, "consent name is still the placeholder"
    return True, name


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--wavs", type=Path, required=True)
    parser.add_argument("--consent", type=Path, required=True)
    parser.add_argument("--script", type=Path, default=Path(__file__).with_name("recording_script.txt"))
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    ok, detail = consent_ok(args.consent)
    if not ok:
        raise SystemExit(detail)
    lines = [line.strip() for line in args.script.read_text().splitlines() if line.strip()]
    wavs = sorted(args.wavs.glob("*.wav"))
    if len(wavs) < len(lines):
        raise SystemExit(f"need at least {len(lines)} wavs, found {len(wavs)}")
    args.out.mkdir(parents=True, exist_ok=True)
    rows = []
    for index, (src, line) in enumerate(zip(wavs, lines), start=1):
        dest = args.out / f"line-{index:03d}.wav"
        subprocess.check_call(
            ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(src), "-ac", "1", "-ar", "22050", str(dest)]
        )
        with wave.open(str(dest)) as handle:
            if handle.getnchannels() != 1 or handle.getframerate() != 22050:
                raise SystemExit(f"{dest.name} was not resampled")
        rows.append(f"line-{index:03d}|{line}")
    (args.out / "metadata.csv").write_text("\n".join(rows) + "\n")
    shutil.copy(args.consent, args.out / "CONSENT.md")
    print(f"prepared {len(rows)} lines for {detail}. No training was started.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
