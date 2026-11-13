# Quality gate

Result: **PASS**

Format: Short (`short`), 5s–60s.
Master: `test-outputs/demo/vertical.mp4`

Loudness fails the gate when it is outside the window. It is not only printed.
Target -14.0 LUFS ± 1.0, true peak at or below -1.0 dBTP.

This gate is the only duration rule. The older files now point here:

- course/skills/motion_picture/qa.py now points here and does not apply a 15-minute floor
- course/blueprint-rework/render_motion.py records length and does not exit on it

A Blueprint lesson of 6:15 is inside the 4–10 minute window.

| Check | Result | Detail |
|---|---|---|
| length | PASS | 5.0s is inside Short (5s–60s) |
| loudness | PASS | integrated -13.2 LUFS, target -14 ± 1 |
| true_peak | PASS | true peak -2.8 dBTP, limit -1 dBTP |
| frozen | PASS | longest static run 4.0s, limit 5s |
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
| figures | PASS | on-screen figures match the lesson, and each one is labelled EXAMPLE |

Every check passed.

This report does not publish the master.
