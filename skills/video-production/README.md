# Video production

Teaching-video skills. Frames are drawn at 1920×1080. The house mix is one number: voice at **−14 LUFS** and **−1 dBTP**, the music bed **20 dB** under that voice, then a single sidechain in `lib/mix.py`.

Paid speech APIs are not used.

| Skill | What it does |
|---|---|
| [motion-graphics](motion-graphics/SKILL.md) | Code-drawn candlesticks, a filling order ladder, a range, a liquidation warning, callouts, lower-thirds, kinetic type, counters, a geometric figure, and Ken Burns on an existing still. |
| [color-grade](color-grade/SKILL.md) | ffmpeg grade and three procedural looks. |
| [music-sound](music-sound/SKILL.md) | Original beds and effects. Ducking goes through `lib/mix.py`. |
| [natural-voice](natural-voice/SKILL.md) | Kokoro `af_heart` and Piper `lessac`. Moods, ticker pronunciation, emphasis, forced word times, SRT and VTT. |

The script-to-master command is `skills/production-pipeline/`. Read `PIPELINE.md` for `lesson.yaml`, `words.json`, and the stage hooks.

Fonts live in `fonts/` (Inter and Roboto Condensed, both OFL). `lib/fonts.py` resolves them before any system path. `course/render/render_tutorial.py` uses that helper. There is no `studio.py` in this branch.

```bash
bash skills/video-production/natural-voice/setup.sh
cd skills/video-production/natural-voice && python3 cli.py samples --out test-outputs/moods
cd skills/production-pipeline && python3 -m production_pipeline build examples/lesson.yaml --out test-outputs/demo
```
