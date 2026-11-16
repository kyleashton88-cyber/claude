# GridBot Blueprint: baseline of prior checks (what worked, what kept failing)

Prepared 16 Nov 2026 (WITA). Read-only review. No repo changes, no renders, no messages sent.

## Sources reviewed

- Local render packs:
  - `/workspace/bp01-render-962465c/`: BP-01 v8, 438.8 s. Includes COMPLETENESS (PASS), BEGINNER-WATCH (FAIL), gate-report, chapters and transcript.
  - `/workspace/bp01-render-632c776/`: BP-01 v7, 435.0 s. COMPLETENESS PASS, BEGINNER-WATCH "PASS with blocking notes".
  - Older BP-01 folders (`bp01-render-*`) and `bp02-render-8c65710`, `bp03-render-da9d22b`.
- `/workspace/bp-audit/BLUEPRINT_SIGNOFF_AUDIT.md` (15 Nov): 12-point audit of BP-01 to 11, including loudness measurements.
- `/workspace/bp-fixorder-51d8fcd/FIXES.md` (14 Nov): `studio.plan()` beginner-watch check for all 11 lessons, plus the BP-02 and BP-03 fresh beginner watches.
- Repo `kyleashton88-cyber/claude`, branch `cursor/blueprint-professional-rebuild-d1f6` at **962465c**. Read with git into `/workspace/bp-curriculum/src/`:
  - `course/scripts/bp-*.json`
  - `course/blueprint-rework/lesson_scripts.py` (the spoken plan) and `AUDIT.md`
  - `course/blueprint-rebuild/` (`studio.py`, `STATUS.md`, `BP-0x_REVIEW.md`, `BP04-11_SCRIPT_CHANGES.md`, `BP04-11_IMAGE_MANIFEST.json`, `numbers/*.yaml`)
  - `course/qa/bp-*.md`
  - `blueprint-image-qa/`, `blueprint-smoke/*/gate/`
  - `skills/video-production/*` (`CONSOLIDATION.md`, `quality-gate`, `screen-demo-kit`, `lib/mix.py`)
  - `course/images/STYLE_V3_GBB.md` and `FALLBACK_MANIFEST.json`
- Image scores: Creative Studio v2 pass lists on the images branch worktree `/workspace/blueprint-beginner/wt` (`cursor/blueprint-beginner-images` at 116f86b, **local only, unpushed**):
  - `blueprint-image-qa/bp01-03-v2/BP01-03_PASS_LIST.json` (90/90 rows PASS: 56 lesson stills plus 34 shared or code-drawn)
  - `blueprint-image-qa/bp04-11/BP04-11_PASS_LIST.json` (112/112 rows PASS, 14 per lesson; 49 practice-repeat beats dropped)

## Current state per lesson (runtime and script length)

| Lesson | Title (unchanged) | Current film | Spoken plan in `lesson_scripts.py` | Planning JSON (`course/scripts`) |
|---|---|---|---|---|
| BP-01 | Introduction | **7:19** (438.8 s, v8 962465c, 1,181 spoken words) | 23 shots | 18 beats, 2,415 planning words |
| BP-02 | What you are going to need | **7:23** (443.2 s, older render 8c65710) | 16 shots, about 860 words | 21 beats |
| BP-03 | What is a grid bot | **6:30** (390.3 s, older render da9d22b) | 18 shots, about 940 words | 19 beats |
| BP-04 | Market regimes | not rendered; **est. 6:00–7:00** | 16 shots, about 850 words | 20 beats |
| BP-05 | Choosing grid spacing and range | not rendered; **est. 5:30–6:30** | 15 shots, about 790 words | 19 beats |
| BP-06 | Entry and exit rules | not rendered; **est. 6:00–7:00** | 16 shots, about 840 words | 20 beats |
| BP-07 | Spot paper trading | not rendered; **est. 6:00–7:00** | 16 shots, about 810 words | 20 beats |
| BP-08 | Managing and monitoring | not rendered; **est. 6:00–7:00** | 17 shots, about 850 words | 20 beats |
| BP-09 | Common mistakes | not rendered; **est. 6:00–7:00** | 17 shots, about 840 words | 21 beats |
| BP-10 | Scaling up on spot | not rendered; **est. 6:30–7:30** | 17 shots, about 940 words | 21 beats |
| BP-11 | Advanced: liquidation scenarios | not rendered; **est. 6:00–7:00** | 17 shots, about 910 words | 20 beats |

How the estimates were made: word counts include repeated stack items. The BP-01 measured rate is about 161 spoken words a minute, including holds, at Kokoro af_heart 1.0. Planned lessons are in line with BP-02 and BP-03, which rendered at 6:30–7:23 from similar plans.

**Rule of thumb for the additions:** 1 minute of added teaching is about 160 words of narration plus its visual.

The planning JSON estimates of about 17 minutes are **not** real runtimes. `studio.py` shortens the lines and speaks them at 1.0.

## What passed and worked well (KEEP and reuse)

### Explanations that landed

Evidence comes from the completeness checks and the beginner watches.

- **"Rungs wait, they don't chase."** The limit order explained through the ladder ("A limit order is an order that waits at a price you choose. It does not chase the price.") is clear in BP-01 v7/v8 and BP-03.
- **The house example is accurate and verified twice.** It is the BTC/USD summer 2023 window: 19 Jul to 16 Oct 2023, band 24,930 to 30,331, six equal gaps of about 900, seven lines.
  - The arithmetic is shown: (30,331 − 24,930) / 6 = 900.17.
  - The stop example is the 23 Oct 2023 close of 33,086 above the top line. The 24 Oct close of 33,901.53 was still above it, which confirms the "did not come back" example.
- **The candle card** (19 Jul 2023: High 30,184, Low 29,794, Close 29,914) is correct and spoken correctly.
- **"Fills" is defined at first use:** "An order fills when the price reaches its line and the trade happens."
- **The leave-the-band explanation works.** Leave through the top and you hold mostly cash. Leave through the bottom and you hold mostly coin. The 51d8fcd check passed it, and it is the clearest consequence teaching in the course.
- **The seed-phrase gloss** ("the secret words or keys that unlock a wallet or account") fixed the v7 blocker.
- **Disclaimer wording** is the Australian general-advice form: "general information… doesn't consider your objectives, financial situation or needs", "Crypto is high risk… could lose all the money", and "Past performance is not a reliable indicator…". It is spoken and on screen, and every watch passed it.
- **Five-digit prices are not spoken.** `_speak_round()` turns them into "the top line" or "about N thousand", and the exact figures stay on cards. This fixed the BP-03 complaint about spoken number strings.
- **The BP-03 mechanics click.** The fresh watch said: "Main idea clear 1:59, mechanics click 2:51."
- **The BP-02 page-before-screen idea** was clear at 0:58.

### Analogies

- **Ladder** (`blueprint-analogies/analogy-ladder.png`, PASS): rung = one price level, gap = the space between rungs. This is the strongest analogy, and the course keeps it as the core one.
- **Checklist** (`blueprint-analogies/analogy-list.png`, PASS): "Your plan checklist" with Pair / Range / Gaps / Stop rows. Keep it.
- **Buckets** (BP-10 005, BP-11 007/008, PASS): separate money per grid, and isolated vs cross margin. Keep it.
- **Fence** (`analogy-fence.png`, BP-01 015 "paper or demo is a fence around practice", the BP-01 "The fence" chapter at 2:39, and the BP-11 recap "isolated fence"). It passed image QA, but the beginner watch flagged that it is reused for two different ideas. **RETIRE** it under Stewart's rule (see CURRICULUM.md analogy set).

### Visuals and pacing

- **Branded intro**: Grid Bot Builder wordmark, visor mascot, "Blueprint / Lesson NN / Title". It passed in BP-01, 02 and 03.
- **Branded outro**: "NEXT / Lesson N / title" card with the mascot, the spoken checklist and the disclaimer footer. It passed in BP-01, 02 and 03.
- **Code-drawn charts** (`studio.py`, PASS on the v2 list): range-2023 hook, a-ladder, the-range, the-levels, walk-the-summer, breakout-2023 the-stop, BP-02 seven-lines, three-words, no-secrets, copy-the-path, BP-03 limit-orders-wait (10 crosses marked), buys-and-sells and where-the-path-stood.
- **Leave-the-band motion** (`paint_leave`): $ / C key, climb, then all cash, fall, then all coin, with a hold of at least 1 s. It passed every check and is the model for the new MOTION visuals.
- **Lower-third term with a plain definition**, plus the EXAMPLE pill on every figure.
- **Worked check card.** The old review called it "the clearest card in the film".
- **Captions:** sidecar VTT, at most 42 characters, at most 18 characters per second, no overlaps. They passed in BP-01 to 03.
- **Pacing:** the picture changes inside 8 seconds and there is no frozen frame (gate PASS).

### Audio (consistent across the renders)

| Lesson | Gate on master | Independent measure on review copy | Silence |
|---|---|---|---|
| BP-01 | −14.4 LUFS, −3.6 dBTP | −14.4 LUFS, −2.5 dBFS true peak | none ≥ 0.5 s at −50 dB |
| BP-02 | −14.4 LUFS, −3.6 dBTP | −14.5 LUFS | none ≥ 0.5 s at −50 dB |
| BP-03 | −14.4 LUFS, −3.5 dBTP | −14.5 LUFS | none ≥ 0.5 s at −50 dB |

- Background music: an in-house calm bed (72 bpm, C major), ducked 20 dB under the voice. It passed in all three lessons.

### Passed stills by lesson (Creative Studio v2 lists, 14 Nov)

These are the KEEP candidates. Before any render, `image_gate.py` must confirm the blob at each path equals the scored blob. Two cautions:
- The 15 Nov audit found the committed 13 Nov list stale against current blobs.
- The v2 lists are held locally by Creative Studio (commits 2639ad5 and 116f86b, unpushed).

| Lesson | PASS stills (ids are `course/images/<lesson>/NNN.png`) | Not on the pass list |
|---|---|---|
| BP-01 | 001–012, 014–018 (17) | 013 (dropped) |
| BP-02 | 001–020 (20) | 021 outro (**known FAIL**, connector arrow 17 px short) |
| BP-03 | 001–019 (19) | none |
| BP-04 | 001, 004–015, 019 (14) | 002, 003, 016–018, 020 |
| BP-05 | 001, 004–015, 018 (14) | 002, 003, 016, 017, 019 (**019 known FAIL**) |
| BP-06 | 001, 004–015, 019 (14) | 002, 003, 016–018, 020 |
| BP-07 | 001, 004–015, 019 (14) | 002, 003, 016–018, 020 |
| BP-08 | 001, 004–015, 019 (14) | 002, 003, 016–018, 020 |
| BP-09 | 001, 004–015, 020 (14) | 002, 003, 016–019 |
| BP-10 | 001, 004–015, 020 (14) | 002, 003, 016–019 |
| BP-11 | 001, 004–015, 019 (14) | 002, 003, 016–018, 020 |

- Shared PASS assets: the wordmark crop (`style-ref/01M6MSHVNHX3WQH81XS8KQK1HT.png`), the mascot (`mascot/blueprint-mascot.png`) and the ladder and list analogies.
- **Title, disclaimer and outro cards are code-drawn** for BP-01 to 03 (PASS), so the missing 002, 003 and 020 stills in BP-04 to 11 should also be code-drawn, not generated.

## What failed repeatedly (design these out)

1. **It never taught why a grid earns.** It never showed one buy-low, sell-high pair on a bounce with fees. This was blocking in the BP-01 v8 watch. The "BUY LOW, SELL HIGH" still (BP-01 007) failed image QA as a profit slogan. The mechanism has to be taught with EXAMPLE numbers, fees and the catch, never as a slogan headline.
2. **The stop action was undefined.** What do you actually do, how long counts as "does not come back", and what does the bot do versus what do you do? This was blocking in v8. In BP-03, the stop was used before it was explained.
3. **Orders were not grounded.** Buy = swap cash for coin, sell = swap coin for cash, and selling needs coin first. Blocking in v8.
4. **The structure jumped around.** BP-01 v8 runs a second "Hook" block at 4:21, after the worked check. Those are the planning-JSON beats appended after the `lesson_scripts` flow, so the film re-teaches the three parts, buys and sells, and the map. BP-02 and BP-03 have the same two-source stacking.
5. **Terms were used before they were defined.** Examples: crypto, daily close, band, range, gap, step, order, fills, rung, coin vs cash, regime, profit target, leverage, seed phrase. This came up in the BP-01 v7, BP-02 and BP-03 watches and is the most frequent single complaint.
6. **High, low or wick was spoken over close-only line charts.** BP-02 #15, BP-04 #13 (13 Mar 2020 low 4,107 is not on the close line), BP-05 #5/#11/#13/#16, BP-06 #5, BP-09 #12, BP-10 #5/#10/#13 and BP-11 #5/#12/#16 (51d8fcd).
7. **Cryptic titles and slides:**
   - "When the drawing fails" (two watches in a row)
   - "Your page comes first / form only copies it"
   - "Empty Pair" form
   - icon strings ("One-breath definition")
   - chain and circle icons on order lines
   - "Leave every figure marked EXAMPLE" (unclear instruction to the learner)
8. **Number lists were too fast or repeated.** Dates and prices were recited twice (BP-02 3:08 and 3:43), and BP-10 #16 had too many numbers. Swaps also broke the grammar: "about about" (BP-04), "On a middle near the middle line" (BP-05), "the middle line, the middle line" (BP-08), and sentences starting in lower case (BP-08 #10, BP-11 #10).
9. **Stack items were repeated.** The recap and objectives stacks speak each line two or three times (seen in BP-02 and BP-11 `lesson_scripts` output). The old "say it back" loops held one chart for about 15 minutes.
10. **Stills had arrow tips short of their targets.** This is the most common Creative Studio fail reason (BP-02 021, BP-05 019, BP-06 016/018/020, BP-07 003/020). Other fails: wrong title text ("MANAGINGMONITORING"), a disclaimer not matching the exact sentence, and "LIQUIDATION SCENES".
11. **The palette breaks the navy and cyan rule.** `studio.py` defines AMBER (stop, "all coin", warning X), MINT (sell lines, key and end-card ticks) and BLUE (buy lines). `STYLE_V3_GBB.md` lets stills use mint for sells and amber for warnings. There is no colour lint.
12. **Length was too short against Stewart's ask.** Every film is 6:30–7:23, and the planning JSON estimates (about 17 min) are misleading.
13. **Stale status docs mislead reviewers.** `STATUS.md` (6:15/4:43/5:02, −16 LUFS) and `course/qa/bp-*.md` ("waiting on images") are out of date, and the BP-01_REVIEW checklist still says −16 LUFS.
14. **Content gaps no lesson fills:**
    - a worked fee calculation per round trip
    - per-bot money sizing
    - what you record in a journal
    - drawdown
    - how to grow or shrink capital under rules
    - Australian specifics (daily close time in AEDT, tax records)
    - BP-10 says outright: "The page does not tell you how much money to assign."

## Where the standard tools live, and whether they are consistent

| Tool | Where in the repo (d1f6 @ 962465c) | Consistent across lessons? |
|---|---|---|
| **Single builder** | `course/blueprint-rebuild/studio.py`. It reads `course/blueprint-rework/lesson_scripts.py` (spoken plan) plus `course/scripts/bp-*.json` (beats and stills) plus `course/blueprint-rebuild/numbers/<lesson>.yaml` | **No.** BP-01 to 03 were built with `studio.py`, but BP-02 and BP-03 at older commits. BP-04 to 11 have never been built and have **no numbers YAML**, so `studio.py` would stop. `skills/video-production/CONSOLIDATION.md` wrongly says "studio.py: not in this branch" and names `skills/production-pipeline` as the director. Other renderers still exist (`course/render/render_tutorial.py`, `course/blueprint-rework/render_motion.py`). **Decision:** `studio.py` is the one builder for all 11, and CONSOLIDATION.md needs correcting. |
| **Loudness standard** | `skills/video-production/lib/mix.py`: voice −14 LUFS, −1 dBTP, music 20 dB under, one sidechain. `studio.py` header says it uses this mix. | **Yes in practice.** BP-01 to 03 all measured −14.4/−14.5 LUFS. Stale docs still say −16: `course/skills/audio-mastering` and the `BP-01_REVIEW.md` checklist. |
| **Quality gate** | `skills/video-production/quality-gate` (`cli.py check … --format blueprint`). Length comes from `gate/profiles.py` (`blueprint`: min 360 s, **no max**). Image gate: `course/blueprint-rebuild/image_gate.py` | **Partly.** BP-01 to 03 passed, and BP-04 to 11 have never run it. Gaps against the new standard: 4% safe margin (not 5%), no 10–15 minute window, no colour lint, no teal check. The gate SKILL.md and CONSOLIDATION.md still say "4–10 min", which conflicts with `profiles.py`. The image gate's default pass list (`blueprint-image-qa/BP01-03_PASS_LIST.json`) is stale, and BP-04 to 11 need the v2 list wired in. |
| **Screen-demo kit** | `skills/video-production/screen-demo-kit` (`cli.py blur` / `cli.py qa`; it fails if an API-key shape, 0x address, balance or account number is still readable). Capture is in `programs/defi-program/export/capture_demo.js` | **Not used by any Blueprint lesson.** `studio.py` never calls it. BP-07's "walk the fields" uses generated stills of imaginary forms. Any new exchange or bot walkthrough (BP-02, BP-03, BP-05, BP-07, BP-08) must be captured through this kit. |
| **Narration** | `studio.py` exits unless Kokoro `af_heart` at speed 1.0 | **Yes.** All three renders. |
| **Captions** | sidecar VTT from `studio.py` into `blueprint-smoke/<lesson>/` | Yes for BP-01 to 03. Not burned in, so the 5% caption margin depends on the player (see the rubric). |

Recommended tool changes (proposals only, nothing changed in the repo):
- Set the `blueprint` profile to 600–900 s.
- Move the safe-margin OCR to 5%.
- Add a palette lint: navy, cyan and white only, failing on teal, mint or amber.
- Wire the screen-demo kit QA into `studio.py` for any `kind: screen` shot.
- Add numbers YAML for BP-04 to 11.
- Make `studio.py` build from **one** script source per lesson, so the duplicate-hook stacking cannot recur.

## Final team QA plan (after each lesson passes its own render and check)

Each lesson still goes one at a time: script, stills, render, quality gate, accuracy verifier, then a fresh blind first-timer watch. When the **full set of 11** has passed, these teammate bots review it in parallel. Each scores against the CURRICULUM.md rubric. Legal Ops is excluded.

| Teammate | Reviews for | Pass bar |
|---|---|---|
| **Creative Studio** (3cfc1bae-…) | Visuals and brand: navy and cyan only (no teal, mint or amber unless Stewart approves), titles in frame, 5% margins, every still on a current PASS blob, unique lesson illustration, intro and outro consistent, GridBot Builder only | All 11 at least 4 in every image category, no hard fail |
| **YouTube & Shorts Producer** | Pacing and retention: hook in the first 20 s, a picture change at least every 8 s, no dead stretches, chapter markers, 10–15 minute runtime, end screen to the next lesson | No segment flagged as a drop-off risk without a fix |
| **Content Marketing** | Message clarity: one idea per segment, the same analogy set everywhere, plain-English terms, the series promise stated the same way in every lesson, no profit framing | Every lesson's one-line objective can be said back from the recap |
| **Customer Success** | Beginner usefulness: could a real new member do the "what you do next" step after each lesson? Are the questions members already ask (fees, how much money, what to do when price breaks out, tax records) answered? | Zero "I still don't know what to do" items |
| **Organic Growth** | Titles, thumbnails and chapter names: searchable, accurate, not clickbait, consistent numbering | Titles approved for upload copy |
| **Crypto Research** (ed24c7f7-…) | Market mechanics and number accuracy: worked examples, fee maths, regime calls on the historical windows, drawdown and sizing arithmetic | Every EXAMPLE number re-computed and matching |
| **Fresh blind first-timer watch** (new executor per lesson, never reused) | The master criterion: can a total beginner explain the lesson back, and how does it move them toward running and scaling a grid bot under written rules? | Rubric PASS (CURRICULUM.md §4) |

Coordination and verification stay with Grok Bot. Results are reported to Stewart for his yes, and nothing goes live without it.
