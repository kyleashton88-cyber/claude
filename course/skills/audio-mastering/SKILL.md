# Audio

Deprecated for new masters. The house mix is `skills/video-production/lib/mix.py`: voice at −14 LUFS and −1 dBTP, music 20 dB under the voice, then one sidechain. This note describes the older lesson renderer, which is still what a paused Blueprint render calls. Do not retune that renderer from this file.

Voice is Kokoro `af_heart` at speed 0.78, 24 kHz mono, from `course/tools/speak_lessons.py`. That pace sits under the 143-word picture clock so the outro is not cut.

The renderer masters the mix in ffmpeg:

- voice resampled to 48 kHz
- music at volume 0.22, looped, side-chain compressed under the voice
- loudnorm at integrated -16 LUFS, true peak -1.5 dB

Paid speech APIs are not used. A new voice vendor needs Stewart's yes.

Re-speak a lesson after its script changes. `speak_lessons.py` skips a wav that is already on disk, so a changed lesson has to be written on purpose.
