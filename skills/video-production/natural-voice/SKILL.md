---
name: natural-voice
description: In-house narration for teaching videos. Kokoro af_heart is the default, Piper lessac is the other free voice. Use for mood presets, ticker pronunciation, emphasis markup, forced word timings, and SRT or VTT captions. There is no paid speech API.
---

# Natural voice

One skill, two free engines, the same pauses, the same moods, and the same word times.

Kokoro `af_heart` is the default because that is the voice on the existing masters. Piper `lessac` is the side-by-side alternative. Both are self-hosted. Models download into the home cache and are not committed.

## Loudness

Voice tracks are mastered to **−14 LUFS** integrated and **−1 dBTP**. That is the single house target, shared with the music bed and the production pipeline. See `lib/mix.py` for the four older numbers this replaced.

## Moods

| Mood | Words per minute | What changes |
|---|---|---|
| `calm-teacher` | 148 | The default lesson voice. |
| `upbeat-intro` | 176 | Shorter pauses, a small pitch lift. |
| `serious-risk` | 126 | Longer pauses, a little lower. |
| `recap` | 152 | A slightly longer breath between sections. |

Kokoro speed and Piper `length_scale` are both derived from that words-per-minute target. Measured bases: Kokoro speed 1.0 is about 197 wpm. Piper lessac at `length_scale` 1.0 is about 222 wpm.

## Markup

```
A grid places *buy* orders below the price. <pause 400ms>
<slow>Read the buffer.</slow>
```

`*word*` and `<emph>` are a little faster, louder, and higher. `<slow>` and `<fast>` change the rate of that span. `[[pause 0.4]]` and `<pause 400ms>` are exact silence. A blank line is a breath, and the mood sets how long it is. Stops, questions, and commas take the pauses from the lesson narrator.

Tickers are in `voice/pronounce.py`. `USDT` is spoken as four letters. The caption still says `USDT`.

## Word times

`words.json` uses schema `video-production.words.v1`:

```json
{"schema": "video-production.words.v1", "engine": "kokoro", "mood": "calm-teacher", "method": "acoustic-forced-align", "words": [{"text": "A", "start": 0.0, "end": 0.12}]}
```

Each written word is spoken again with the same engine and found, left to right, in the utterance. If that placement fails, times fall back to phoneme weights. `.vtt` and `.srt` are written from the same words. A test checks median start and end error against a reference clip and requires it to be under 80 ms.

## Run

```bash
cd skills/video-production/natural-voice
python3 cli.py say --engine kokoro --mood calm-teacher --text "A grid places buy orders." --out out.wav
python3 cli.py samples --out test-outputs/moods
```

`samples` renders one script, about twenty-five seconds at the calm pace, in all four moods, once with Piper and once with Kokoro.

## A custom voice, later

`custom_voice/TRAINING.md` is the guide. `prepare_dataset.py` builds a Piper dataset and refuses to run without a filled consent file. It does not train. No one's voice is in this repo.

## Failure modes

| What you see | Why | What to do |
|---|---|---|
| `Kokoro files are not in` | The onnx pack was not downloaded. | Run `setup.sh`. |
| `engine must be kokoro or piper` | Another engine name was passed. | Stay on the two free engines. |
| `unknown mood` | The name is not in the table. | Use one of the four moods. |
| Alignment method says phoneme-weighted | A word template could not be placed. | Check the wav is not silent. The reference test still has to pass on a clean clip. |
| Consent is rejected | The name is still `YOUR NAME`, or the statement dropped "I consent". | Fill `CONSENT.md` with the speaker's own words before preparing a dataset. |
