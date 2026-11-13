---
name: review-record
description: Keep an append-only approval ledger for a master and build a review pack for a person. Use when QA and compliance reports exist and a legal reviewer or Stewart needs to record a decision. Publish stays false until QA passed, legal signed, and Stewart said yes.
---

# Review record

One folder per master. `ledger.jsonl` only grows. `ledger.md` grows with it. Do not edit a line that is already written, and do not delete the file to start again.

`publish_allowed` is computed. The CLI has no field for it, and an event that tries to set it is refused. Nothing in this skill uploads, publishes, or sends mail. Stewart's decision is recorded only after he has given it. The command does not email him.

## When publish is allowed

All of these, on the current hashes:

- The latest QA result is pass, for this master hash.
- The latest compliance content result is pass.
- A person has a legal event with their name, a date, and this content hash.
- The latest Stewart decision is yes, with a date.

A later QA fail closes it again. Content flags keep it closed even if someone has signed. A legal name of `cursor`, `agent`, or `auto` is refused.

## Commands

```bash
cd skills/video-production/review-record
python3 cli.py init --master clip.mp4 --id sample --format short --ledger ledger-dir
python3 cli.py qa --ledger ledger-dir --report report.json
python3 cli.py compliance --ledger ledger-dir --report compliance.json
python3 cli.py legal --ledger ledger-dir --name "Alex Counsel" --date 2026-11-13 --report compliance.json
python3 cli.py stewart --ledger ledger-dir --decision yes --date 2026-11-13
python3 cli.py status --ledger ledger-dir
python3 cli.py pack --ledger ledger-dir --out pack-dir --qa report.json --compliance compliance.json --transcript clip.vtt
```

The pack holds the master path, a contact sheet of frames, the QA report, the compliance report, and the transcript. It is for a person to read.

## Do not

- Publish from this folder.
- Email Stewart or anyone else.
- Rewrite history. Append a new event.
