# BP-02 What you need: film card text that must change on re-voice

Prepared 25 Nov 2026 (AEDT) for Stewart's round 2 (9:09am), item 5. Nothing was rendered, edited in the repo or sent.

- **Film checked:** `/workspace/bp02-render-c80ee62/master.mp4` (c80ee62, 11:04.2). Frames were pulled at every caption cue that says "close", plus spot checks at 1:55–5:40. The montages are in `_tools/ocr/bp02-m0*.jpg` and `bp02-x*.jpg`.
- **Code checked:** `studio.py` and `lesson_scripts.py` at c80ee62.
- **Copy it must match:** `BP-02-APPROVED.md`, which now has noun "close" as "closing price", R3 (M1 sentences dropped) and R5 ("public historical daily prices").
- **Timestamps** are film time (m:ss).

## A. Seen on screen in the c80ee62 film (confirmed from frames)

| # | Film time | Scene / card | Current card text | Change to | Where it is drawn (c80ee62) |
|---|---|---|---|---|---|
| 1 | 0:26 (26.6 s) | Risk card | "A daily close is the last price of that day." | "A daily closing price is the last price of that day." | studio.py `paint_stack` Risk branch, L2811 |
| 2 | 0:32 (31.8 s) | Risk card | "The prices are public historical daily closes, marked Example." | "The prices are public historical daily prices, marked Example." (R5. Not 'daily closing prices'.) | studio.py L2813 |
| 3 | 1:49–1:55 (109–115 s) | Seven items, glossary card | Title "A daily close"; line "A daily close is the last price of the day." | Title "A daily closing price"; line "A daily closing price is the last price of the day." | glossary card from the `bp02()` cue "a daily close" (lesson_scripts.py L609); the same words are in studio.py `paint_board` L1642–1643 |
| 4 | 2:56 (176 s) | No secrets panel | "Public close" (with "No balance") | "Public closing price" | studio.py `_paint_bp02_scene`, L2406 |
| 5 | 4:15 (255 s) | The pair panel | "Public daily closes" | "Public daily closing prices" | studio.py `_paint_bp02_scene`, L2437 |
| 6 | 12 caption cues (0:26 to 5:32) | Burned captions | for example "A public close is not your account.", "and the second close still outside." | These are regenerated from the new voice. Check that the pack says "closing price". | caption pack |

## B. In the c80ee62 source but not seen in the sampled frames (check before re-render)

| Source | Text | Change to |
|---|---|---|
| studio.py `paint_board` seven-lines rows and three-words cards (L1654, L1685) | "3. The pair: bitcoin, public daily closes." / STOP "Two daily closes outside." | "3. The pair: bitcoin, public daily closing prices." / "Two daily closing prices outside." |
| studio.py worked rows and say-the-page boards (L1722, L1732, L1752, L1770, L1773, L2058) | "Pair: bitcoin, public daily closes." / "Stop: two daily closes outside." / "Public daily close" / "Stop: two daily closes outside, then stop the bot." | "...public daily closing prices." / "Stop: two daily closing prices outside." / "Public daily closing price" / "Stop: two daily closing prices outside, then stop the bot." |
| studio.py `_paint_bp02_scene` stop text (L2471, L2472) | "If a daily close finishes outside the range" / "and the next daily close is still outside," | "If a daily closing price finishes outside the range" / "and the next daily closing price is still outside," |
| studio.py `_paint_journal` (L2217) | "Stop rule: two closes outside" | "Stop rule: two closing prices outside" |
| studio.py L1701 | "A public close is not your account." (No balance card) | "A public closing price is not your account." |

## C. Pipeline points that affect the re-voice (important)

- **Two BP-02 spoken sentences come from the pipeline, not the script.** studio.py `risk_lines` (L573) and the BP-02 override (L581–582) add the spoken lines at 0:26–0:32: "A daily close is the last price of that day." and "The prices are public historical daily closes, marked Example." The edit to `BP-02-APPROVED.md` alone will **not** change these in the voice. A re-voice needs studio.py L573 and L582 (and the cards at L2811–2813) changed to "A daily closing price is the last price of that day." and "The prices are public historical daily prices, marked Example." That is a repo change, so it was **not done**. It is flagged for Stewart and the developer.
- **Reveal timing** keyed on "daily close" (`_spoken(shot, local, "daily close")`, L1642) has to be rekeyed to "closing price" after the re-voice.
- **R3:** the dropped M1 sentences at L35 have no card. Nothing on screen changes.

## D. Count

- **5 card or text locations seen on screen** (A1–A5), plus the burned captions (A6).
- **5 source groups** (B) need checking.
- **2 pipeline-spoken sentences** (C) need a studio.py change before any re-voice.
- **Runtime after re-voice:** about 11:07.9 (11.13 min) at 163 wpm. That is the film plus 10 net words: 11 closing-price swaps, +11 −11 for M1 in and out, and −1 for R5. It does not include the pipeline sentences in C (+2 words if they are changed).
