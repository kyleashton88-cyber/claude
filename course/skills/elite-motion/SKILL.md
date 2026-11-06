# Elite motion

Code: `course/skills/elite_motion.py`. The renderer calls it for every Elite lesson.

- The still or the example plate is scaled once with Lanczos.
- A crop then drifts a few pixels inside the spare margin. That is the camera move. Labels are not resampled on every frame, which keeps the no-degradation rule.
- A teal box steps every four seconds on ordinary beats, so the frame is not a static hold.
- Beats with `example.kind` play a 24-frame drawing (a path, two paths, a wide day, or an analogy card) and then hold the last frame for the rest of the narration.

Blueprint lessons do not take this path.

Free tools only: Pillow and ffmpeg. Remotion and Manim are free software but are not installed. Do not add them, or any paid renderer, without Stewart's yes.
