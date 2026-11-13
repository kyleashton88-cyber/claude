---
name: compliance
description: Lint a lesson script or transcript for Australian financial-content risk before a person reviews it. Use when copy may promise returns, give personal advice, name an exchange, skip the disclaimer, or show a number without an EXAMPLE label. The result stays pending legal review until a person signs the review record.
---

# Compliance

A writing linter. It flags lines. It suggests a plain rewrite. It does not decide that the copy is lawful, and it does not clear itself.

Status stays **pending legal review** until a person records approval in `review-record`. Passing a clean script back through this command does not flip that status. There is no approve flag. `--approve` exits 2.

## What it flags

| Kind | Examples | Rewrite direction |
|---|---|---|
| Hype | guaranteed, risk-free, proven, like a pro, can't lose, 12% returns | Say the thing can lose money, or drop the claim. |
| Personal advice | you should buy, I recommend, right for you, suitable for you | Describe the mechanism. Leave the decision with the viewer. |
| Brand | Binance, Bybit, and the other venue names in the list | Name the mechanism, not the venue. |
| Example number | a price, a percent, or a grid count with no EXAMPLE or illustrative in the sentence | Put EXAMPLE on the figure. |
| Disclaimer | the spoken words or the on-screen words miss "education" and "not financial advice" | Add both. One of them is not enough. |

A negation counts. "Returns are not guaranteed" is not a hype flag. The disclaimer sentence is not personal advice.

## Run

```bash
cd skills/video-production/compliance
python3 cli.py lint samples/clean-lesson.yaml --out report-dir
```

The report is `compliance.json` and `compliance.md`. Each flag has a line, a timestamp when the file has one, the text, and a suggestion.

`--ledger path` only reads a review record. If that record has a legal event for this file's hash, the status line can show **legal signed**. The linter still does not write the event.

Exit 1 when there are content flags. Exit 0 when the copy is clean. A clean exit is not permission to publish. `publish_allowed` lives only in the review record.

## Do not

- Treat this as legal advice or as a sign-off.
- Email anyone, including Stewart.
- Write into `course/` or edit a live lesson in place.
