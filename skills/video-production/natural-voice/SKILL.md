---
name: natural-voice
description: One voice interface for teaching narration, voice=piper or voice=elevenlabs. Use when a lesson needs speech with pauses, long-script chunking, a character-cost estimate before any paid call, per-line caching, retries, loudness-normalised wav, and word timings for captions. Piper is the free local voice. ElevenLabs is stock voices only. Never clone a voice, never upload a recording of a person, and never call a voice-creation endpoint.
---

# Natural voice

`voice=piper` and `voice=elevenlabs` share one call: `Speaker(...).render(text)` then `render_to_file`. Both return a WAV at -16 LUFS / -1 dBTP, a WebVTT, and a JSON sidecar of word times.

## When to use

- A lesson needs narration and caption times.
- You want the free Piper voice, or a paid ElevenLabs stock voice, without two different caption pipelines.
- A script is long enough that one request would wander in pace. Chunking keeps one config on every piece.

## When not to use

- Anything that needs a clone, an instant voice, a professional voice clone, or `use_pvc_as_ivc`. Those words are refused.
- A voice that is not in the stock list, unless you pass a stock voice id from the account on purpose. The client still only calls text-to-speech.

## Shared text

Pauses, both of these, become exact silence. They are not sent to the engine (Piper would read `[[` as raw phonemes).

```
[[pause 0.4]]
<break time="400ms"/>
<break time="0.4s"/>
```

A pause must be between 0 and 10 seconds.

Spoken text is packed into chunks of at most 420 characters, on sentence boundaries, then on words. The same synthesis settings are used for every chunk. ElevenLabs also receives `previous_text` and `next_text` so the join stays in the same delivery. Piper has one `SynthesisConfig` for the whole script (`length_scale` 1.05, `noise_scale` 0.5, `noise_w_scale` 0.6).

## Engines

| Engine | Voice | Alignment | Cost |
|---|---|---|---|
| `piper` | `lessac` only, the stock `en_US-lessac-medium` model | Sentence edges are exact, because each sentence is its own audio chunk. Words inside a sentence are weighted by phoneme count. | 0 |
| `elevenlabs` | A name in `voice/markup.py` `STOCK_VOICES`, default `Brian` | Character times from `/with-timestamps`, grouped into words. | Estimated credits, printed first |

ElevenLabs models and the estimate used before a call:

| Model | Credits per character (estimate) |
|---|---|
| `eleven_multilingual_v2` (default) | 1 |
| `eleven_turbo_v2_5` | 0.5 |
| `eleven_flash_v2_5` | 0.5 |

The real bill follows the account plan. The estimate is there so a long script is priced before it runs.

## Run

```bash
cd skills/video-production/natural-voice
python3 cli.py estimate --engine elevenlabs --text "Hello there."
python3 cli.py say --engine piper --text 'Price moves. [[pause 0.4]] The figures are illustrative.' --out out.wav
python3 cli.py say --engine elevenlabs --voice Brian --text "Hello there." --yes --out out.wav
```

`--yes` is required for ElevenLabs. Without it the CLI prints the estimate and does not call the API. Piper does not need `--yes`.

Set `PIPER_MODEL` to point at a different local `.onnx`. The default is `~/.cache/piper-voices/en_US-lessac-medium.onnx`. If it is missing, the engine downloads the stock Lessac medium model and its JSON from the Piper voices release. The model is not committed.

Set `ELEVENLABS_API_KEY` for the paid path. This environment did not have the key, so the live sample was not rendered. The Piper sample in `test-outputs/` is the committed proof. The ElevenLabs path is covered by a mocked API test (retry, cache, alignment, clone refusal).

## Outputs

Next to the wav:

- `.vtt` — caption cues, about eight words or 42 characters.
- `.json` — the estimate, the alignment method, and every word with `start` and `end` in seconds.

Audio is 48 kHz stereo after the loudness pass, even though Piper speaks at 22050 mono. Duration is unchanged, so the word times still match.

Cache: `~/.cache/video-production/voice/<sha256>.wav` plus a JSON of the words. The key is the engine, the settings, the chunk text, and the previous/next chunk. A repeat does not call the engine again.

## Retries

ElevenLabs retries 429, 500, 502, 503, and 504, up to four attempts, waiting on `Retry-After` or else 1s, 2s, 4s. 401 and 403 are not retried.

## Failure modes

| What you see | Why | What to do |
|---|---|---|
| `ELEVENLABS_API_KEY is not set` | Paid engine, no key. | Export the key and pass `--yes`, or use `--engine piper`. |
| Dry run, no file | `--yes` was left off. | Read the estimate, then re-run with `--yes`. |
| `Voice cloning is disabled` | The voice, model, or settings contained clone / ivc / pvc. | Pick a stock name. Do not retry with a recording. |
| `unknown stock voice` | The name is not in `STOCK_VOICES`. | Use a listed name, or a stock voice id of 16+ letters. |
| `the installed Piper stock voice is lessac` | Another Piper voice was requested and is not installed. | Stay on `lessac`, or set `PIPER_MODEL` and extend the allow-list on purpose. |
| Piper download fails | The model host is blocked. | Copy the onnx and the `.onnx.json` to the cache path yourself. |
| Word times look even inside a sentence | Piper's Lessac model does not emit phoneme durations. Times are phoneme-weighted inside a sentence. Sentence edges and pauses are exact. | Use ElevenLabs when you need character-accurate times. The method string in the JSON says which one you got. |
| Loudness pass fails on a very short line | The meter needs a little audio. | Give the line a sentence, not a single syllable. |
| A chunk returns a different sample rate | Two engines or two models were mixed in one render. | One `Speaker` per file. |

## Test

```bash
python3 -m unittest tests/test_voice.py
```

Committed Piper proof: `test-outputs/piper-sample.wav`, `.vtt`, and `.json`.

The live ElevenLabs sample is the gap. Render it with the key:

```bash
ELEVENLABS_API_KEY=... python3 cli.py say --engine elevenlabs --voice Brian \
  --text 'Price moves in candles. [[pause 0.4]] The figures are illustrative.' \
  --yes --out test-outputs/elevenlabs-sample.wav
```
