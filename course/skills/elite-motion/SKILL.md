# Elite motion

Code: `course/skills/elite_motion.py`. The renderer calls it for every Elite lesson.

- Every Elite beat is cut into pieces of at most 2.5 seconds (`segment_lengths`). The crop stays at the vertical centre and travels sideways, so it does not slide off the diagram into empty navy. A teal tick crosses the frame during the piece. The next piece starts from the opposite side. Labels are not scaled a second time.
- Beats with `example.kind` use the ChatGPT still at `course/images/examples/<kind>.png`. Those plates are real charts or everyday analogies. The renderer does not draw them. They wait for Creative Studio and are not marked pass.
- The previous masters stay in `course/masters/baseline/`. Do not delete them.

Blueprint lessons do not take this path.

Free tools only: Pillow and ffmpeg. Remotion and Manim are free software but are not installed. Do not add them, or any paid renderer, without Stewart's yes.
