# Quality gate

Result: **PASS**

Format: Blueprint lesson (`blueprint`), 360s minimum, no upper limit.
Master: `/agent/repos/claude/course/blueprint-rebuild/masters/bp-01-introduction.mp4`

Loudness fails the gate when it is outside the window. It is not only printed.
Target -14.0 LUFS ± 1.0, true peak at or below -1.0 dBTP.

This gate is the only duration rule. The older files now point here:

- course/skills/motion_picture/qa.py now points here and does not apply a 15-minute floor
- course/blueprint-rework/render_motion.py records length and does not exit on it

Blueprint lessons keep the 6-minute minimum. The 10-minute upper cap is removed.

| Check | Result | Detail |
|---|---|---|
| length | PASS | 406.9s is inside Blueprint lesson (360s minimum, no upper limit) |
| loudness | PASS | integrated -14.4 LUFS, target -14 ± 1 |
| true_peak | PASS | true peak -3.6 dBTP, limit -1 dBTP |
| frozen | PASS | longest static run 0.5s, limit 8s |
| black | PASS | no near-black run over 0.5s |
| silence | PASS | no silence of 2s or more |
| resolution | PASS | 1920x1080 |
| fps | PASS | 30.000 fps |
| codec | PASS | video h264, audio aac, yuv420p |
| captions | PASS | 221 cues, at most 42 characters and 20 per second |
| text_recognition | PASS | tesseract read the sampled frames |
| brands | PASS | no exchange or banned brand name |
| safe_margins | PASS | sampled words sit inside the 4% margin |
| disclaimer | PASS | found an education line that says not financial advice |
| figures | PASS | on-screen figures match the lesson, and each one is labelled EXAMPLE |

Every check passed.

This report does not publish the master.
