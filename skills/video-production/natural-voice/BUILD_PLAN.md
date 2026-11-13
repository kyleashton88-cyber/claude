# Voice build plan

## Decision

One narration skill. Kokoro `af_heart` is the default, because every current master already uses it. Piper `lessac` is the second free voice, so a take can be compared without leaving the machine. Paid speech APIs are out.

## What shipped

- Moods: calm teacher, upbeat intro, serious risk warning, recap. Each is a words-per-minute target, a pause scale, a breath, and a small pitch and energy shift. Kokoro speed and Piper length scale both come from the words-per-minute number.
- Pauses follow the lesson narrator: longer after a question, a measured gap after a comma, exact silence from `<pause 400ms>` or `[[pause 0.4]]`, and a breath on a blank line.
- Emphasis: `*word*`, `<emph>`, `<slow>`, `<fast>`.
- Tickers and jargon in `voice/pronounce.py`. The caption keeps the written token.
- Word times by placing a same-engine rendering of each word inside the utterance. `words.json`, SRT, and VTT share those times. Median error on a reference clip is tested under 80 ms.
- Voice master at −14 LUFS / −1 dBTP, the same target as the mix.
- A fine-tune scaffold that checks consent and writes a dataset, and does not train.

## What is left

- Stewart listens to `test-outputs/moods/` and confirms or replaces the default.
- A custom voice still needs the speaker's own recordings and a filled consent file. Nothing here is trained.
- faster-whisper can be compared later. The shipped aligner does not depend on it, because the same engine that spoke the line can place each word.
