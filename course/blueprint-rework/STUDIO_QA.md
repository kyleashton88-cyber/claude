# Ready for Creative Studio

Automated checks passed on every stills cut. This is not the Creative Studio sign-off.

Review `course/masters-stills/bp-01` through `bp-11`. The earlier motion cuts remain in `course/masters-v2/`. The original masters remain in `course/masters/`. Do not delete any of them.

Each stills file is 1920×1080 H.264, AAC 48 kHz stereo, about −16.2 LUFS, and at least 21 minutes. Analogy pictures are the ChatGPT fallback stills in `course/images/blueprint-analogies/` (ladder, fence, packing list, two buckets), navy and cyan, Lanczos-fit into the frame without upscaling. The price path is the public daily Bitcoin series in `course/data/public-prices/`. No venue name, logo, or balance is drawn.

Look for: label pile-up on the rally chart, a still that covers the chart, a caption that is not a full phrase, and any day whose spoken close does not match the playhead.

Motion pass: the picture is scaled to 2048 wide and cropped back to 1920×1080 with a slow Ken Burns drift (24 px over 5 s, 18 px over 7 s). The caption bar from the previous cut, including the cyan rule and the disclaimer, is laid on after the drift and does not move. Its left margin stays at 72 px. Audio is copied. `freezedetect=n=0.003:d=7.5` is the check that no frame holds for 8 seconds. A frame every 3 seconds is the check that no caption touches the frame edge. Lesson 07 is `bp-07-spot-paper-trading`, title Spot paper trading.

| Lesson | Holds over 8s before | After |
| --- | --- | --- |
| bp-01 | 5 | 0 |
| bp-02 | 4 | 0 |
| bp-03 | 3 | 0 |
| bp-04 | 3 | 0 |
| bp-05 | 4 | 0 |
| bp-06 | 1 | 0 |
| bp-07 | 5 | 0 |
| bp-08 | 3 | 0 |
| bp-09 | 2 | 0 |
| bp-10 | 4 | 0 |
| bp-11 | 6 | 0 |

Caption clips on a frame every 3 seconds, after the bar was pinned: bp-01 0, bp-02 0, bp-03 0, bp-04 0, bp-05 0, bp-06 0, bp-07 0, bp-08 0, bp-09 0, bp-10 0, bp-11 0. The drifting cut before this pin had 17, 17, 19, 28, 19, 24, 21, 18, 20, 15, and 28.
