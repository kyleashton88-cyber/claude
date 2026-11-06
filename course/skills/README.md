# Course skills built for the Blueprint rework

These are free and local. Elite lessons can import them later. This rework does not render Elite files.

| Tool | What it is |
|---|---|
| `instructional_design/GUIDE.md` | Objective, sequence, worked example, recap. Every concept needs a real anchor. |
| `motion_picture/` | Motion-graphics engine: animated public-price charts, analogies, callouts, camera ease, wipes, narration sync, music ducking, loudness, and a QA check. |
| `course/data/public-prices/` | Recreated public Bitcoin daily windows. See `SOURCE.md`. |

## What was not acquired

- HeyGen, and any hosted avatar. Not used.
- Paid image APIs and paid stock libraries. Not used. The ChatGPT web image batch is a stills path. These lessons do not use it, because a still cannot move with the sentence. If that web path is paused, the documented fallback is `course/tools/fallback_images.py`, and Creative Studio still has to mark a still pass before a master may use it.
- Remotion (open source, needs a Node project) and Manim (open source). Not installed. The motion engine here is the local replacement: vector frames piped to ffmpeg. It is free.

## No-degradation

Frames are drawn at 1920×1080. Nothing is upscaled. The encode is H.264, CRF 16, BT.709. Labels are drawn at final size, not scaled up afterwards.
