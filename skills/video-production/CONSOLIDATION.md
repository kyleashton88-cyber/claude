# One video production set

New work starts at `skills/production-pipeline` and finishes at `skills/video-production/quality-gate`. Narration is `skills/video-production/natural-voice`. Kokoro `af_heart` is the default. The mix is `skills/video-production/lib/mix.py`: voice −14 LUFS / −1 dBTP, music 20 dB under that voice, then one sidechain. Duration is only `skills/video-production/quality-gate/gate/profiles.py`.

Paid speech APIs are not part of this set.

| Old entry | What happens now |
|---|---|
| `skills/production-pipeline` | The director. One `lesson.yaml` to a master. When the lesson sets `format`, the build runs the quality gate and stops on a fail. |
| `skills/video-production/natural-voice` | The narration skill. Kokoro `af_heart`, Piper `lessac` as the other free voice. |
| `skills/video-production/lib/mix.py` | The only loudness standard. |
| `skills/video-production/quality-gate` | The only video QA entry, including length and figure checks. |
| `skills/video-production/music-sound` | Beds and effects. Ducking calls `lib/mix.py`. The skill text uses −14, not −16. |
| `.claude/skills/course-video-director` | Deprecated as the entry point. The Operator gold steps in that file are still readable. |
| `studio.py` | Not in this branch. There is nothing to call. |
| `course/render/render_tutorial.py` | Still renders a stills lesson for the paused Blueprint rebuild. It does not judge duration. New lessons use the pipeline. |
| `course/skills/motion_picture/qa.py` | Deprecated. It no longer applies a 15-minute floor. The message points at the quality gate. |
| `course/blueprint-rework/render_motion.py` | Still renders. It records length and does not exit when a lesson is under 15 minutes. |
| `programs/defi-program/export/build_video.js` | Operator renderer, left as those masters were built. New lessons do not start here. |
| `course/tools/speak_lessons.py` | Still fills `course/audio` with Kokoro `af_heart` for an existing course render. New narration uses `natural-voice`. |
| `programs/defi-program/export/build_vo.py` | Still feeds `build_video.js`. New narration uses `natural-voice`. |
| `course/skills/audio-mastering` | Documents the older renderer mix. The house standard is `lib/mix.py`. |
| `.cursor/skills/illustration-qa` | Still a stills checklist. Its duration lines point at the quality-gate profiles. |
| `programs/defi-program/export/capture_demo.js` | Still captures shots. Blur and the secret check are `skills/video-production/screen-demo-kit`. |
| `skills/video-production/market-check-clip` | A Market Check post to a 60–90s 16:9 master and a vertical cut. |
| `skills/video-production/compliance` | Script linter. It does not sign off. A person records that in `review-record`. |
| `skills/video-production/scene-planner` | Shot list. The picture changes within 8 seconds. |
| `skills/video-production/review-record` | Append-only ledger. Nothing here publishes. |
| `skills/video-production/templates` | Format files, thumbnail, vertical cut, chapters, end card. |

A 6:15 Blueprint master is inside the Blueprint window (4–10 minutes). No other file may reject it for being under 15 minutes.
