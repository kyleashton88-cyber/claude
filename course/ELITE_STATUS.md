# Elite status

Branch `cursor/course-video-qa-fix-7f90`. Audit date 6 November 2026. PR #6 stays open and unmerged. No HeyGen.

This file is the read of where Elite stood, then the list of changes made after Creative Studio failed el-07 and el-09 and Stewart asked for real examples worked through the teaching.

## Where Elite is

All 11 lessons have a script, a full set of passed stills, a fresh voice track, and a new 1080p master of at least 15 minutes. Creative Studio's earlier video QA passed 9 of 11 and failed el-07 and el-09 because the voice and the caption named Bybit and Pionex. Those lines are gone. The new masters speak a generic US-persons line, teach through a public price path and a set of analogies, and move on screen. Creative Studio has not QA'd this new cut.

## Per lesson, this cut

Voice times are the re-speak. Master times are the re-encode. Every master is 1920×1080, h264 and aac.

Wired stills are the pictures the script points at. Every wired still is in `FALLBACK_MANIFEST.json` with status pass, palette teal, and the no-degradation clause. Each file on disk is a 1536×1024 PNG. Manifest rows above the beat count are older v3 stills that are not on the long script.

| Lesson | Beats | Wired stills | Passed | Voice | Master |
|---|---:|---:|---:|---|---|
| el-01 Welcome | 20 | 20 local | 20 | 16.46 min | 16.81 min |
| el-02 Prerequisites | 22 | 22 local | 22 | 17.35 min | 17.33 min |
| el-03 Multi-layer | 22 | 22 local | 22 | 16.97 min | 17.16 min |
| el-04 Dynamic spacing | 20 | 20 local | 20 | 17.34 min | 17.09 min |
| el-05 Portfolio risk | 21 | 17 local, 4 v3 | 21 | 17.11 min | 17.08 min |
| el-06 Circuit breakers | 21 | 12 local, 9 v3 | 21 | 16.40 min | 16.82 min |
| el-07 Liquidation | 22 | 13 local, 9 v3 | 22 | 18.90 min | 18.05 min |
| el-08 Size on a schedule | 21 | 10 local, 11 v3 | 21 | 16.52 min | 16.69 min |
| el-09 Multi-venue | 22 | 22 local | 22 | 17.24 min | 17.40 min |
| el-10 How to ask | 22 | 11 local, 11 v3 | 22 | 17.06 min | 17.11 min |
| el-11 Paper plan | 21 | 10 local, 11 v3 | 21 | 17.30 min | 16.92 min |

Masters are 1920×1080, h264 and aac, under `course/masters/`. Voice is 24 kHz mono. Music is `course/music/komiku-ambiant-truth.ogg`, ducked under the voice and loudnormed to about -16 LUFS.

One manifest row has no no-degradation clause: `el-05-portfolio-risk-11` at `course/images/fallback/el-05-portfolio-risk/11.png`. It is not wired to a long-script beat. The other 312 Elite rows are teal and carry the clause. None of the 313 Elite rows is a fail.

## Creative Studio on disk

`course/images/fallback-qa/` holds the 5 November still reviews (`2026-11-05_1055`, `v3a`, `v3b`, `v3c`). Those rounds failed many early plates. The manifest later marks the Elite v3 set pass (133 rows dated 5 November, plus one ChatGPT-web row). The 6 November re-QA is stored only as `qa_reason` on the manifest, not as a JSON file on disk:

- 89 passes at `077197f`
- 23 passes at `4e32c28` (rqa2)
- 12 passes at `1976166` (rqa3). el-07 beat 7 failed in that round for naming exchanges and was redrawn with generic VENUE chips
- 55 passes at `105e4b8` (rqa4)

Video QA after the masters: 9 of 11 passed. el-07 around 05:06 and el-09 around 04:52 named Bybit and Pionex in the voice and the caption. The plates behind those lines do not print the names. el-07 beats 14 and 18 use older v3 plates (a falling chart, and an isolated-versus-cross diagram). Those plates do not print an exchange name either.

## What changed

Exchange names were removed from every Elite script field. The spoken line is now: "United States: some venues' futures products are not available to US persons." A search of `course/scripts/el-*.json` for Bybit, Pionex, Binance, OKX, KuCoin, Bitget, Coinbase, and Kraken returns nothing. Captions that had been cut off at "Bybit" were rebuilt from the new line. The four practice captions in el-07 beats 14 and 18 and el-09 beats 14 and 18 were in that set.

Each lesson's key beats now teach through one real example. The picture is drawn at render time, in teal, and animated across about two seconds, then held. The passed still remains the file the script points at. Chart and analogy beats play the drawn plate instead, so the example is what the learner sees while the line is spoken.

| Lesson | Example on screen |
|---|---|
| el-01 | Paper map. Elite is the map you finish before a trip. |
| el-02 | Pre-flight list. You can say the first grid in one line before a second grid. |
| el-03 | One shelf. Two labels fighting over one box. |
| el-04 | 12 and 13 June 2022. The second day is the wide bar. The close was 16 percent under the day before. |
| el-05 | Bitcoin and ether, November 2021 to November 2022, rebased. Daily moves lined up near 0.89. That figure is an example, not a rule, and so is the old 0.8 tag. |
| el-06 | A switch you flip by hand. US share trading paused on 9, 12, 16 and 18 March 2020. |
| el-07 | The public path from 8 November 2021 to 21 November 2022, about 76 percent lower, stamped Example. The June day keeps the deleted multiple struck. The US-persons line names no venue. |
| el-08 | The same path. November 2022 was a lower close, not a receipt. |
| el-09 | Two bridges. A second venue is a second way to be stuck, not a discount. The US-persons line names no venue. |
| el-10 | Which line the stop is on. The question does not hand over a balance. |
| el-11 | A recipe card before you cook. The assignment is the page, not a deposit. |

The index behind the charts is `course/skills/real-market-charts/data/`. It is rebased to 100 on the 8 November 2021 close. Dollar prices and the data vendor's name are not drawn. Source note is in that folder's `SOURCE.md`.

New shared skills, because `bc-b0e396a6` was not available to copy from:

- `course/skills/instructional-design/SKILL.md`
- `course/skills/elite-motion/SKILL.md` and `course/skills/elite_motion.py`
- `course/skills/real-market-charts/SKILL.md`
- `course/skills/audio-mastering/SKILL.md`

The renderer now uses that motion code for Elite only. Blueprint stays a still hold. The camera is a crop inside one Lanczos scale, so labels are not resampled on every frame.

Not bought, and not run: ChatGPT image generation, ElevenLabs, HeyGen, Remotion, and Manim. Those last two are free software and are not installed. Stewart's yes comes before any of them.

## Done

- Exchange names removed from Elite script voice, captions, concepts, and prompts.
- Real examples written into the key beats and drawn as teal plates while those lines play.
- All 11 lessons re-spoken with Kokoro and re-encoded at 1920×1080. Every new master is at least 16.69 minutes.
- Motion path added for Elite. Blueprint renders are unchanged.

## In progress

Nothing is rendering. The re-speak and the re-encode of all 11 lessons have finished.

## Blocked

- Creative Studio has not QA'd this cut. The drawn plates and the new masters are waiting on that review. Do not treat them as passed.
- PR #6 is not merged, on purpose. Masters are ordinary git files and several are over GitHub's 50 MB hint.
- No paid art was commissioned, so the new plates are drawings of public data and analogies, not photographs.

## Next

- Send the new masters to Creative Studio for video QA. The lines that used to name Bybit and Pionex are now "United States: some venues' futures products are not available to US persons."
- Leave PR #6 unmerged until Stewart says otherwise.
