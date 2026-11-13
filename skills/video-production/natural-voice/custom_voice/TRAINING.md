# Fine-tuning a house voice

This is tooling only. It does not train, and it does not contain anyone's recordings.

A custom voice is allowed only after a filled consent file sits next to the wavs.
Training on a teammate's voice, including Stewart's, waits for that person's own recording and their own signed consent. Do not start from a checkpoint with someone else's audio.

## What you record

Read `recording_script.txt` in a quiet room. One sentence a line, the same text, three takes if a line is messy. 22,050 Hz or 48,000 Hz mono wav, one file per line, named `line-001.wav` and so on. Twenty to forty minutes is enough for a Piper fine-tune from a checkpoint. More is better. Do not include music.

## Consent

Copy `CONSENT.md`, fill the name, the date, and the statement, and save it as `CONSENT.md` inside the dataset folder. `prepare_dataset.py` refuses to write a training set when that file is missing, when the name is still the placeholder, or when the statement does not contain the words "I consent".

## Prepare

```bash
python3 prepare_dataset.py --wavs /path/to/wavs --consent /path/to/wavs/CONSENT.md --out /path/to/dataset
```

The script checks consent, resamples to 22,050 Hz mono, and writes Piper's `metadata.csv` layout. It does not launch training.

## Train, later, on a machine you control

Piper fine-tunes from a published checkpoint (lessac medium is the usual start). The Piper training repo documents the command. This folder deliberately does not wrap that command, so a consent check cannot be skipped by a one-line train invocation here.

When a model exists, point the narrator at it with `PIPER_MODEL=/path/to/model.onnx`. The voice skill will use it for the `lessac` slot only if you also register the new name in `voice/piper_engine.py`. Until then the shipped voices stay the stock checkpoints.
