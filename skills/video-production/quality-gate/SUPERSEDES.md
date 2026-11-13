# What this gate replaces

The 15-minute minimum is still in the tree. It is not the gate to use.

| File | What it still does | What to run instead |
|---|---|---|
| `course/skills/motion_picture/qa.py` | Fails a master under 15 minutes. Prints loudness and does not fail on it. Skips brand OCR when tesseract is missing. | `skills/video-production/quality-gate/cli.py check` |
| `course/blueprint-rework/render_motion.py` | Exits after a render when the lesson is under 15 minutes. | The same gate, with `--format blueprint`. |

There is no `course/tools/qa.py`. The check lives in `course/skills/motion_picture/qa.py`.

BP-01 at 6:15 fails that old floor and passes the Blueprint profile (4–10 minutes). Loudness on this gate is −14 LUFS ± 1 and true peak at or below −1 dBTP, and either miss is a fail.
