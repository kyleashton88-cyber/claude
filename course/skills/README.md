# Course skills

Elite and Blueprint each keep the tools that built their masters.

## Blueprint rework

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

## Elite

Shared tools for Grid Bot Elite and, later, Blueprint. The Blueprint agent
`bc-b0e396a6` was not available when this folder was added, so these files are
the starting set. Extend them. Do not fork a second copy.

Stewart asked for the Elite example stills to go through the ChatGPT image
path. Those ten plates are in `course/images/examples/` and are not marked pass.
ElevenLabs, HeyGen, and any other paid tool still need a separate yes.

| Skill | What it is |
|---|---|
| `instructional-design/SKILL.md` | How an Elite lesson teaches: objective, sequence, worked real example, recap |
| `elite-motion/SKILL.md` | Travelling crop on the ChatGPT stills, cut so no hold exceeds 7.5 seconds |
| `real-market-charts/SKILL.md` | Public price index, licence note, and the chart the plates draw |
| `audio-mastering/SKILL.md` | Kokoro voice and the music duck already in the renderer |
