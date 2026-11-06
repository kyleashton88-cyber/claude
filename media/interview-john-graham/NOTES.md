# John and Graham interview — edit notes

Cut and audio repair for Jess (Market Pros). Source is nine lossless
stream-copy segments of `video1834446502.mp4` (17:26.827, 1920×1080, 25 fps,
H.264 High / AAC-LC stereo). The two channels are the same signal
(correlation 1.0), so John cannot be split by pan.

Rebuild with:

```bash
python3 media/interview-john-graham/edit_interview.py \
  --parts interview_part00.mp4 ... interview_part08.mp4 \
  --output john-graham-interview.mp4
```

Needs `ffmpeg` on PATH, plus `numpy` and `scipy` (`requirements.txt`).

## Where the cut is

The host's introduction runs from 4.90 s ("I'm here today with beautiful
Graham and John") through "if you want to take it from there" (ends 44.98 s)
and the handoff "Awesome. John." (46.18–46.88 s). John is already on camera
by then. His first line, "Nice to meet you, Graham", has its first energy at
**48.86 s**.

The file starts at **48.600 s** (frame 1215, exactly 25 fps). That is 260 ms
of silence before the word, so the attack is not clipped and the open is not
a cold cut on a syllable. Graham's "Yeah, nice to meet you too, John" follows.
The host's scripted intro and the "Awesome. John." cue are the part that was
removed.

## What was wrong with John's audio

Measured on speech he is known to be saying (the long answer from about
109 s) against Graham's question just before it:

| | John, before | Graham |
|---|---:|---:|
| Speech-band level (500–1500 Hz) | about 17 dB quieter | reference |
| 125–160 Hz vs his own speech band | roughly +25 to +50 dB too hot | flat |
| 50/60 Hz hum line above the noise floor | none | none |
| Samples at full scale | none on his mic | none |

The boom at 125–160 Hz is a room or proximity resonance. It is what makes him
sound boxy and far away. His speech-band noise floor is already close to
Graham's once the level is matched, so the problem is not hiss and not a
discrete mains hum.

Tried and not used, because they did not move that spectrum:

- single-channel WPE dereverb (`nara_wpe`)
- `afftdn`, `anlmdn`, and `arnndn` (RNNoise)

## What the repair does

John is found by that resonance: a frame has to stay boom-heavy in the
110–180 Hz band, and quiet in the 500–2000 Hz band, for several hops before
it can open his mask. The mask then grows across his own pauses and stops
when Graham's or the host's mic is the loud, clear one. On the opening this
covers his hello and the screen-share line, and it leaves Graham's hello,
Graham's question (92–108 s, sample difference 0), and the host's lines
untouched.

Under the mask only, zero-phase EQ (so nothing shifts against the picture):

- High-pass, 8th order at 185 Hz, applied forward and back. Kills the
  resonance and the band where a hum would have been (about −85 dB at 80 Hz
  on a noise sweep).
- Peaking cut around 155 Hz and a presence lift around 750 Hz.
- A cut around 4.2 kHz and a low-pass at 7 kHz, so the makeup gain does not
  leave him brighter than Graham.

Then one makeup gain of **+12.7 dB**, set so his 500–1500 Hz speech matches
Graham's, and a soft ceiling at −1 dBFS on his signal only. After the mix:

- "Nice to meet you, Graham": John −16.2 dBFS, Graham's reply −15.3 dBFS.
- His later answer sits within a few dB of Graham's question. The full-band
  number is lower than the speech-band match because the boom that used to
  inflate his RMS is gone.
- 51 samples still reach 0 dBFS. They are AAC reconstruction peaks on the
  loud mics (the float decode of the source peaks at +0.97 dBFS) and they
  are outside John's mask, so they were not introduced by the makeup gain.

## Picture

Joined with `ffmpeg -f concat -c copy`. Keyframes in this recording are about
36 s apart, and the next one after the cut is **60.040 s**.

- 48.600–60.040 s (286 frames) is re-encoded H.264 High, 4:2:0, CRF 8.
  High profile cannot store a mathematically lossless 4:2:0 stream, and a
  4:4:4 lossless head would not concatenate with the rest. CRF 8 against the
  decoded source measures about 54–56 dB PSNR on checked frames.
- 60.040 s through the end (24,666 frames) is the original bitstream.
  A checked frame (source frame 1715, output frame 500) is byte-identical.

Output is 1920×1080, 25 fps, H.264 High + AAC-LC stereo 256 kbps, 24,952
frames. Duration **16:38.13** (998.13 s).
