# Production pipeline

One command builds a lesson. Another agent owns quality-gate, compliance, scene-planner, review-record, and templates. Those packages are not here. The hooks below are how they attach.

```bash
cd skills/production-pipeline
python3 -m production_pipeline build examples/lesson.yaml --out test-outputs/demo
```

## Loudness, one standard

| Piece | Target |
|---|---|
| Voice master | −14 LUFS integrated, −1 dBTP |
| Music bed before the mix | mastered to −14 LUFS, then lowered **20 dB** |
| Ducking | one function, `lib/mix.py` `duck_under_voice` |
| Final mix | the sum of that voice and that ducked bed, peak-limited to −1 dBTP, not loudness-normalised a second time |

Four older values this replaced:

1. Voice master at −16 LUFS.
2. Music bed master at −16 LUFS, with no separate under-voice offset.
3. Ducked mix mastered again at −16 LUFS, which lifted the bed.
4. The lesson renderer's −1.5 dBTP ceiling and a fixed music volume of 0.22.

## lesson.yaml

```yaml
id: grid-picture
title: A grid, in one picture
engine: piper          # piper or kokoro
mood: calm-teacher     # calm-teacher, upbeat-intro, serious-risk, recap
sections:
  - id: orders
    chapter: Orders    # YouTube chapter title. First chapter is 0:00.
    narration: >
      A grid places buy orders below the price.
    visual:            # a motion-graphics shot
      kind: ladder
      title: Orders on a ladder
      caption: Buys below. Sells above.
    illustration: "grid ladder, range 90 to 110, price 100"
end_card:
  kicker: Education only
  line: Not financial advice. Figures are illustrative.
```

`illustration` is optional. When the illustration engine from PR #18 is importable, the stage runs `python3 -m illustration_engine batch <generated.yaml> --preset house --out plates`. When it is not installed, the stage writes `illustration.txt` and continues. This pipeline does not copy that engine.

## words.json

Written by the align stage. Schema `video-production.words.v1`.

```json
{
  "schema": "video-production.words.v1",
  "engine": "piper",
  "mood": "calm-teacher",
  "method": "acoustic-forced-align",
  "words": [{"text": "A", "start": 0.35, "end": 0.48}]
}
```

Times are seconds on the finished timeline, including the short lead before each section. SRT and VTT are the same words. `chapters.txt` is the YouTube chapter list.

## Stage hooks

`build(lesson, out, hooks)` runs this order:

`narrate`, `align`, `illustrate`, `motion`, `grade`, `music`, `captions`, `endcard`, `loudness`

Pass `hooks={"grade": my_grade}` to replace a stage. The hook receives the context dict and may read or replace what the default stage would have written.

| Key | After the default stage |
|---|---|
| `lesson` | The parsed yaml. |
| `speaker` | The Kokoro or Piper speaker. |
| `words` | `Word` objects. Also `out/words.json`. |
| `chapters` | `(start_seconds, title)` pairs. |
| `shots` | Motion-graphics shot dicts. |
| `voice` | Path of the section voice wav, before the end-card pad. |
| `picture` | Ungraded motion mp4, including the end card. |
| `graded` | Clean-educational grade of a designed picture (exposure left at 0). |
| `mix` | Ducked mix wav. |
| `caption_box` | Burn rectangle. `caption_margin_ok` is true when it sits inside a 5% margin. |
| `report` | `qa-report.json`. |

The end card is the last motion shot, not a second video. Its line comes from `end_card` in the yaml.

## Outputs

`master.mp4`, `words.json`, `captions.srt`, `captions.vtt`, `chapters.txt`, `end-card.txt`, `illustration.txt`, `qa-report.json`.
