# Motion picture lessons

Draw a lesson as moving diagrams, not a stack of stills. Encode with ffmpeg. Narration is timed to the same shots.

## Pieces

| File | Role |
|---|---|
| `draw.py` | Frame painter. Navy and cyan, or navy and teal for a later Elite cut. Camera ease, wipe, playhead, callouts. |
| `speech.py` | Local Kokoro voice, pronunciation fixes, length of each shot. |
| `audio.py` | CC0 music bed, louder on the ident and the outro, sidechain under the voice, −16 LUFS. |
| `qa.py` | Duration, 1080p, loudness, motion, and a brand-name scan of sample frames. |

## Shot

A shot is one spoken idea. Fields that matter:

- `vo` — what is spoken.
- `caption` — the short line in the lower bar. A complete phrase.
- `kind` — `ident`, `chart`, `replay`, `analogy`, `stack`, `worked`, `legal`, `outro`.
- `chart` — a window name in `course/data/public-prices/btc-usd-windows.json`.
- `reveal` — how much of that path is drawn by the end of the shot (0 to 1).
- `levels` — horizontal prices to rule in.
- `analogy` — `ladder`, `fence`, `list`, or `buckets`.

The playhead sits on the revealed day. Levels draw in as `reveal` grows. The camera eases every shot, so the frame never freezes.

## Run

```bash
python3 course/blueprint-rework/render_motion.py --id bp-01-introduction
python3 course/skills/motion_picture/qa.py course/masters-v2/bp-01-introduction.mp4
```

Do not point this at an `el-` file from the Blueprint batch.
