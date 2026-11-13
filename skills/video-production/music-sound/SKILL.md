---
name: music-sound
description: Original music beds and sound design for teaching videos. Use when a lesson needs a calm instrumental bed at a set mood, key, BPM, and length, or whooshes, clicks, a riser, a UI tick, a short ident sting, and ducking under voice. The house mix is voice at -14 LUFS, the bed 20 dB under that, true peak -1 dBTP.
---

# Music and sound

Beds and effects are synthesized in numpy. There is no sample library and no soundfont, so there is nothing third-party to license inside the audio. See `LICENSES.md`.

The mix is `lib/mix.py` `duck_under_voice`. The bed is mastered to −14 LUFS, lowered 20 dB, then sidechain-ducked. The voice is already at −14 LUFS / −1 dBTP. The sum is peak-limited and not normalised again.

## When to use

- A lesson needs a bed that will not fight the voice.
- You need a short effect on a cut, a counter, or an ident.
- You want the bed at a specific key, BPM, and length.

## Moods, keys, tempo

| Mood | Progression | What you hear |
|---|---|---|
| `calm` | I–IV–vi–V | Pad, soft pluck, bass. No hats. |
| `focused` | I–V–vi–IV | The same family, plus a quiet tick. |
| `hopeful` | I–IV–V–vi | A little brighter, a slightly louder tick. |

Keys: `C C# Db D Eb E F F# Gb G Ab A Bb B`. Scales: `major`, `minor`. BPM 40–140. Length 1–600 seconds.

`calm` in a minor key uses the minor scale degrees on that same progression shape. The committed beds are calm C major at 72, focused A minor at 84, and hopeful F major at 76, each 60 seconds.

## Sound design

| File | What it is |
|---|---|
| `whoosh.wav` | A noise sweep, about 1.3 seconds. |
| `click.wav` | A soft two-tone click. |
| `riser.wav` | A two-second pitch rise. |
| `tick.wav` | A short UI tick. |
| `mark-sting.wav` | Four original notes (C E G C). Not a quotation of an existing ident. |

## Ducking and loudness

See `skills/video-production/lib/mix.py`. One function, one target.

Beds and mixes longer than three seconds are 48 kHz stereo. A standalone bed is mastered to −14 LUFS so the ducker can drop it 20 dB from a known level. An effect shorter than three seconds is peak-normalised to −1 dBTP.

## Run

```bash
cd skills/video-production/music-sound
python3 cli.py bed --mood calm --key C --scale major --bpm 72 --seconds 60 --out bed.wav
python3 cli.py sfx --out test-outputs/sfx
python3 cli.py duck --music bed.wav --voice voice.wav --out mix.wav
python3 cli.py demo --out test-outputs --voice path/to/voice.wav
```

## Settings

Beds and mixes longer than three seconds are written as 48 kHz stereo 16-bit WAV after two-pass loudnorm to −16 LUFS / −1 dBTP. An effect shorter than three seconds has no meaningful integrated loudness, so it is peak-normalised to −1 dBTP instead.
- Seed is fixed (`7` for beds, per-effect seeds for noise), so a re-run matches.
- Fade in 1.6 s, fade out 2.4 s, before the loudness pass.

## Failure modes

| What you see | Why | What to do |
|---|---|---|
| `unknown mood` / `unknown key` | The name is not in the tables. | Use a listed mood, key, and scale. |
| `bpm must be between 40 and 140` | Tempo is outside the range the arrangement is written for. | Pick a tempo inside the range. |
| Loudness is not −14 | The file skipped `master_audio`, or it is shorter than three seconds and was only peak-limited. | Re-run `cli.py bed` or `cli.py duck`. |
| Duck does nothing | The voice is silent, or it is far below the sidechain threshold. | Confirm the voice file has level. The numpy test uses a 0.4 tone against a 0.2 bed. |
| Bed feels busy under speech | Hats are on. | Use `calm`, which has no tick. |

## Test

```bash
python3 -m unittest tests/test_music.py
```

Committed samples: `test-outputs/beds/*.wav` (three 60 second beds), `test-outputs/sfx/*.wav`, and `test-outputs/mix/ducked.wav`.
