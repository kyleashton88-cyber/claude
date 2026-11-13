#!/usr/bin/env bash
# Voice and render dependencies. Idempotent. Does not train a voice and does not call a paid API.
set -euo pipefail
python3 -m pip install --user --break-system-packages --no-warn-script-location \
  piper-tts kokoro-onnx soundfile numpy scipy pillow pyyaml faster-whisper fonttools

CACHE="${KOKORO_DIR:-$HOME/.cache/kokoro}"
mkdir -p "$CACHE" "$HOME/.cache/piper-voices"
if [ ! -f "$CACHE/kokoro-v1.0.onnx" ]; then
  curl -fL --retry 3 -o "$CACHE/kokoro-v1.0.onnx" \
    "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx"
fi
if [ ! -f "$CACHE/voices-v1.0.bin" ]; then
  curl -fL --retry 3 -o "$CACHE/voices-v1.0.bin" \
    "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin"
fi
PIPER="$HOME/.cache/piper-voices/en_US-lessac-medium.onnx"
if [ ! -f "$PIPER" ]; then
  curl -fL --retry 3 -o "$PIPER" \
    "https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/medium/en_US-lessac-medium.onnx"
  curl -fL --retry 3 -o "${PIPER}.json" \
    "https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/medium/en_US-lessac-medium.onnx.json"
fi
command -v ffmpeg >/dev/null
echo "Voice setup complete. ffmpeg is on PATH. Models are in the home cache."
