# Audio

Voice is Kokoro `af_heart` at speed 0.78, 24 kHz mono, from `course/tools/speak_lessons.py`. That pace sits under the 143-word picture clock so the outro is not cut.

The renderer masters the mix in ffmpeg:

- voice resampled to 48 kHz
- music at volume 0.22, looped, side-chain compressed under the voice
- loudnorm at integrated -16 LUFS, true peak -1.5 dB

No ElevenLabs and no HeyGen. A new voice vendor needs Stewart's yes.

Re-speak a lesson after its script changes. `speak_lessons.py` skips a wav that is already on disk, so a changed lesson has to be written on purpose.
