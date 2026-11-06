# Elite motion

Code: `course/skills/elite_motion.py`. The renderer calls it for every Elite lesson.

- Every Elite beat is cut into pieces of at most 7.5 seconds (`segment_lengths`). Inside a piece the crop travels across one Lanczos scale, and the next piece starts from the opposite side. The picture is moving while the line is spoken, and a hold cannot run past 7.5 seconds. Labels are not scaled a second time.
- Beats with `example.kind` use the ChatGPT still at `course/images/examples/<kind>.png`. Those plates are real charts or everyday analogies. The renderer does not draw them. They wait for Creative Studio and are not marked pass.
- The previous masters stay in `course/masters/baseline/`. Do not delete them.

Blueprint lessons do not take this path.

Free tools only: Pillow and ffmpeg. Remotion and Manim are free software but are not installed. Do not add them, or any paid renderer, without Stewart's yes.
