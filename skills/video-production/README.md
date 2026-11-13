# Video production

Four skills for teaching videos, plus one clip that runs them in order. They follow the lesson renderer: frames at 1920×1080, no upscale, voice timed to the picture, the bed ducked under the voice, and the mix mastered to −16 LUFS.

Nothing here publishes, uploads, or emails. Sample lines do not name a company, and they do not carry an address or a number for one.

| Skill | What it does |
|---|---|
| [motion-graphics](motion-graphics/SKILL.md) | Code-drawn candlesticks, a filling order ladder, a range, a liquidation warning, callouts, lower-thirds, kinetic type, counters, a geometric figure, and Ken Burns / parallax on a still that already exists. |
| [color-grade](color-grade/SKILL.md) | ffmpeg grade, procedural `.cube` looks, white balance, exposure, skin-tone protection, legal range, clip matching, waveform and vectorscope. |
| [music-sound](music-sound/SKILL.md) | Original beds at a mood, key, BPM, and length. Whoosh, click, riser, tick, ident sting. Sidechain duck. −16 LUFS / −1 dBTP. Optional ElevenLabs Music, off unless a key is set. |
| [natural-voice](natural-voice/SKILL.md) | `voice=piper` or `voice=elevenlabs`. Pauses, chunking, a cost estimate before a paid call, cache, retries, loudness, word-level captions. Stock voices only. No cloning. |

Shared code is in `lib/` (palette, ffmpeg, loudness, easing). Install with `pip install -r requirements.txt`. ffmpeg must be on `PATH`.

Rebuild every sample:

```bash
cd skills/video-production
python3 render_samples.py
```

The end-to-end clip is `demo/build_demo.py`. It speaks the picture with Piper, lays a calm bed under it and ducks, draws the five motion shots to the length of the voice, grades with `clean-educational` plus legal range, and writes 1080p H.264 CRF 18 with AAC requested at 320 kbps. The committed clip is 45.1 seconds. Integrated loudness is −15.9 LUFS, true peak −3.3 dBTP. The native AAC encoder averages about 308 kbps on this material.

Designed frames skip auto exposure. Auto exposure is for camera footage, and it is what the color-grade samples demonstrate. A navy title card is already where it should be.

## Samples

Large media is Git LFS. A file's bytes are at:

`https://media.githubusercontent.com/media/kyleashton88-cyber/claude/cursor/video-production-skills-001b/<path>`

| Path | What it proves |
|---|---|
| `skills/video-production/motion-graphics/test-outputs/grid-sequence.mp4` | 29s reel of the motion components. |
| `skills/video-production/color-grade/test-outputs/` | Ungraded card, three looks, three split screens, a matched clip, waveform and vectorscope PNGs, `grade-report.json`. |
| `skills/video-production/music-sound/test-outputs/beds/` | Three 60s beds. |
| `skills/video-production/music-sound/test-outputs/sfx/` | The effect pack. |
| `skills/video-production/music-sound/test-outputs/mix/ducked.wav` | Bed ducked under a voice with a gap in the middle. |
| `skills/video-production/natural-voice/test-outputs/piper-sample.wav` | Piper, with a pause, plus `.vtt` and `.json` word times. |
| `skills/video-production/demo/test-outputs/grid-picture.mp4` | The chained clip, with `grid-picture.vtt`. |

## Gap

`ELEVENLABS_API_KEY` was not set here. The ElevenLabs voice path is implemented and unit-tested against a mock (retry, cache, character alignment, clone refusal). It has no committed live sample. The music adapter returns no file when the key is missing and keeps the procedural bed. Render a live voice sample with the command in `natural-voice/SKILL.md` once the key is available.
