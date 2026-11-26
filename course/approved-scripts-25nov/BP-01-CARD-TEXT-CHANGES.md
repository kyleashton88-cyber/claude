# BP-01 Introduction: film card text that must change on re-voice

Prepared 25 Nov 2026 (AEDT) for Stewart's round 2 (9:09am), item 5. Nothing was rendered, edited in the repo or sent.

- **Film checked:** `/workspace/bp01-render-c80ee62/master.mp4` (c80ee62, 14:40.6). Frames were pulled at every caption cue that says "close", plus spot checks at 9:50–12:00. The montages are in `_tools/ocr/bp01-m0*.jpg` and `bp01-x*.jpg`.
- **Code checked:** `course/blueprint-rebuild/studio.py` and `motions.py` at c80ee62 (`git show c80ee62:...`, copied to `/tmp/studio.py` and `/tmp/motions.py`).
- **Copy it must match:** `BP-01-APPROVED.md`, where every noun "close" is now "closing price".
- **Timestamps** are film time (m:ss).
- **Rule used:** "close" as a noun becomes "closing price". Verbs stay as they are (for example the self-check "Price closes above your top line").

## A. Seen on screen in the c80ee62 film (confirmed from frames)

| # | Film time | Scene / card | Current card text | Change to | Where it is drawn (c80ee62) |
|---|---|---|---|---|---|
| 1 | 6:00 (360 s) | One day, value card | "The daily close" over "29,914" | "The daily closing price" over "29,914" | studio.py `paint_candle`, L3572 |
| 2 | 6:19–6:35 (379–395 s) | One day, candle | "simplified: high, low, close" | "simplified: high, low, closing price" | studio.py L3605 |
| 3 | 6:19–6:35 | One day, candle | "The wick runs from the high to the low. The close is the last price." | "The wick runs from the high to the low. The closing price is the last price." | studio.py L3606 |
| 4 | 6:19–6:35 | One day, candle label | "Close 29,914" (the example asked about as 'daily close 29,914') | "Closing price 29,914" | studio.py L3610 `close_label` |
| 5 | 6:35 (395 s) | One day, tag chip | "High, low and close" | "High, low and closing price" | studio.py L3625 |
| 6 | 7:22 (442 s) | Crossings card | "The close moves across one line" | "The closing price moves across one line" | studio.py `paint_crossings`, L1947 |
| 7 | 9:11–9:50 (551–590 s) | The stop, stop-sign panel | "Two closes outside." | "Two closing prices outside." | motions.py `_paint_stop_card`, L456 |
| 8 | 9:44–9:50 (584–590 s) | The stop, chart pins | "Close 1" / "Close 2" | "Closing price 1" / "Closing price 2" (or, if the pins are too narrow, "Day 1 outside" / "Day 2 still outside"; Creative Studio to choose) | motions.py `_paint_stop_card` L463–464 and L525 (`f"Close {index + 1}"`) |
| 9 | 10:40 (640 s) | Downside, big type | "EXAMPLE two closes" | "EXAMPLE two closing prices" | studio.py `_open_build`, L3835 |
| 10 | 12:40, 13:01, 13:02, 14:20, 14:22 (760–862 s) | Self-check, Your turn, Recap: "Outside the range" sketch | "Next close still outside" | "Next closing price still outside" | studio.py `_paint_bp01_picture`, L2755 |
| 12 | 12:00–12:04 (720–724 s) | The map, roadmap node 11 (added Round 3, F2) | Node 11 label "Plan", lit when the voice says "opt-in"/"liquidation"; spoken line was "Then an opt-in lesson on liquidation and your complete plan." | Node 11 label "Wrap-up" (suggested; mirrors the new line "Then an optional wrap-up of the spot page, and what this course does not cover."). **Also rekey the reveal:** the cue needles are exact tokens ("opt-in", "opt", "liquidation"), and none matches "optional" or "wrap-up", so after re-voice node 11 would never light. Add "optional" / "wrap-up". | studio.py `_roadmap_nodes` L1853 (label); reveal cues L2859 (`_word_at` exact-token match) |
| 11 | 20 caption cues (3:59 to 14:22) | Burned captions | for example "Every close in this window", "The daily close is", "the next close is still outside." | These are regenerated from the new voice, so they need no hand edit. Check that the re-voice pack captions say "closing price". | caption pack / `captions.srt` |

## B. In the c80ee62 source but not seen in the sampled frames (check before re-render)

| Source | Text | Change to |
|---|---|---|
| motions.py `BP01-V06` "The stop, plainly" rows (L51, L52, L56) | "EXAMPLE. 23 Oct close 33,086. Close 1 outside." / "EXAMPLE. 24 Oct close 33,902. Close 2 still outside." / "Two daily closes. The second one still outside." | "EXAMPLE. 23 Oct closing price 33,086. Closing price 1 outside." / "EXAMPLE. 24 Oct closing price 33,902. Closing price 2 still outside." / "Two daily closing prices. The second one still outside." |
| lesson_scripts.py `bp01()` shot captions (L119, L368, L369, L383) | "{date}. Close {n}." / "19 July 2023. Close 29,914. ..." / term_text "Daily close" / "Every close stayed inside the range." | "{date}. Closing price {n}." / "19 July 2023. Closing price 29,914. ..." / "Daily closing price" / "Every closing price stayed inside the range." |
| studio.py roadmap labels L2848 and L3648; image alt text L371; lesson_scripts.py `bp01()` map caption L452 (added Round 3, F2) | "11, Your complete plan" / "...and an opt-in lesson on liquidation with your complete plan." / "The eleven lessons, ending in scaling under written rules and your complete plan." | "11, Optional wrap-up" / "...and an optional wrap-up of the spot page, and what this course does not cover." / "The eleven lessons, ending in scaling under written rules and an optional wrap-up." |
| studio.py shared glossary/key-stop text (L294, L309, L327) | "The figures are public closes." / "A public daily close on the path." / "Every close is an example. ..." | "...public closing prices." / "A public daily closing price on the path." / "Every closing price is an example. ..." |

## C. Pipeline points that affect the re-voice (for the developer; not edited)

- **Reveal timing keyed on the word "close".** The candle label (L3619 `heard("close")`) and similar `_spoken(..., "daily close")` cues fire when the voice reaches "close". After the re-voice the voice says "closing price", so check that each trigger still fires at the right moment, or rekey it to "closing price".
- **The opening risk line is spoken from the pipeline, not the script** (studio.py L579–580: "The prices are public historical prices at the end of each day, marked Example."). It has no "close", so no change is needed. Make sure the disclaimer is still added on re-voice (Legal G4).
- **Content gate D5** ("noun close marked from the vowel") should see no noun "close" in the BP-01 voice after re-voice. Every remaining "close" is a verb: "Price closes above your top line" and "every one of those days closed inside the range".

## D. Count

- **11 card or text locations seen on screen** (A1–A10, plus A12 added in Round 3), plus the burned captions (A11), which come from the voice.
- **4 source groups** (B) need checking (one added in Round 3).
- **Runtime after re-voice:** about 14:56.8 (14.95 min) at 163 wpm after Round 3 F2, under the 15.0 min ceiling by about 3 s. The card changes do not change the runtime.
