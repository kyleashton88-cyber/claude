# Quality gate

Result: **FAIL**

Format: Blueprint lesson (`blueprint`), 240s–600s.
Master: `blueprint-smoke/bp-01-excerpt.mp4`

Loudness fails the gate when it is outside the window. It is not only printed.
Target -14.0 LUFS ± 1.0, true peak at or below -1.0 dBTP.

This gate is the only duration rule. The older files now point here:

- course/skills/motion_picture/qa.py now points here and does not apply a 15-minute floor
- course/blueprint-rework/render_motion.py records length and does not exit on it

A Blueprint lesson of 6:15 is inside the 4–10 minute window.

| Check | Result | Detail |
|---|---|---|
| length | FAIL | 25.2s is outside Blueprint lesson (240s–600s). Length follows the format profile. There is no 15-minute floor. |
| loudness | PASS | integrated -13.5 LUFS, target -14 ± 1 |
| true_peak | PASS | true peak -2.9 dBTP, limit -1 dBTP |
| frozen | PASS | longest static run 6.0s, limit 8s |
| black | PASS | no near-black run over 0.5s |
| silence | PASS | no silence of 2s or more |
| resolution | PASS | 1920x1080 |
| fps | PASS | 30.000 fps |
| codec | PASS | video h264, audio aac, yuv420p |
| captions | PASS | 6 cues, at most 42 characters and 20 per second |
| text_recognition | PASS | tesseract read the sampled frames |
| brands | PASS | no exchange or banned brand name |
| safe_margins | PASS | sampled words sit inside the 4% margin |
| disclaimer | PASS | found an education line that says not financial advice |
| figures | PASS | on-screen figures match the lesson, and each one is labelled EXAMPLE |

Failed: length

This report does not publish the master.
