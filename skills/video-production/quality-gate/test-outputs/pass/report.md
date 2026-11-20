# Quality gate

Result: **PASS**

Format: Short (`short`), 5s–60s.
Master: `test-outputs/short-master.mp4`

Loudness fails the gate when it is outside the window. It is not only printed.
Target -14.0 LUFS ± 1.0, true peak at or below -1.0 dBTP.

This gate supersedes the 15-minute minimum. Those older files stay where they are:

- course/skills/motion_picture/qa.py (15-minute minimum, loudness printed and not failed)
- course/blueprint-rework/render_motion.py (exit when a lesson is under 15 minutes)

A Blueprint lesson of 6:15 is inside the 4–10 minute window.

| Check | Result | Detail |
|---|---|---|
| length | PASS | 6.0s is inside Short (5s–60s) |
| loudness | PASS | integrated -14.0 LUFS, target -14 ± 1 |
| true_peak | PASS | true peak -7.6 dBTP, limit -1 dBTP |
| frozen | PASS | longest static run 0.5s, limit 5s |
| black | PASS | no near-black run over 0.5s |
| silence | PASS | no silence of 2s or more |
| resolution | PASS | 1080x1920 |
| fps | PASS | 30.000 fps |
| codec | PASS | video h264, audio aac, yuv420p |
| captions | PASS | 1 cues, at most 42 characters and 20 per second |
| text_recognition | PASS | tesseract read the sampled frames |
| brands | PASS | no exchange or banned brand name |
| safe_margins | PASS | sampled words sit inside the 4% margin |
| disclaimer | PASS | found an education line that says not financial advice |

Every check passed.

This report does not publish the master.
