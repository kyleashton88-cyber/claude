# BP-01 to BP-03 image QA against the image quality standard

Standard: `skills/image-quality-standard/` on `cursor/illustration-engine-3a63` (f688829). Pass = every category at least 4 and no hard fail.
Scope: the 92 rows of `blueprint-smoke/BP01-03_IMAGE_USE.txt` on `cursor/blueprint-professional-rebuild-d1f6` (6940897). Every row is in `BP01-03_PASS_LIST.json` under its exact path string and lesson, in the `images` list that `course/blueprint-rebuild/image_gate.py` reads. Only `status: pass` rows have `pass: true`.

## Counts (against 92)

| Status | Rows |
|---|---|
| pass | 38 |
| fail | 12 |
| needs_render_to_score | 23 |
| pending (bp-03 stills not landed) | 19 |
| **total** | **92** |

The 38 passes are 16 bp-01 stills (001-003 and 005 refitted), 18 bp-02 stills, analogy-fence and the title art for each of the 3 lessons.
The 12 fails are bp-01 004 and 010, 3 bp-02 stills, analogy-ladder, analogy-list, the mascot for each of the 3 lessons, and the bp-01 title card and end card (smoke render).
Remake prompts are in `specs/remake/`: 7 for ChatGPT stills and 25 for code-drawn slots. The mascot has no prompt because it needs an approved character sheet.

## How it was scored

- Each image was viewed at full size, OCR'd with RapidOCR for spelling, and its labels were checked against `specs/prompts/<lesson>__NNN.txt`. It was then compared with `references/good` and `references/bad` (fetched from LFS).
- `check.py` ran on every file (`qa_sheets/check_results.json` on the box). Its `cramped` flag fires on almost every ChatGPT still because of the background grid in the 4% band, so margins were judged by eye. Its `off_brand_flag` also over-fires on glow, so brand was judged by eye too.
- Lesson stills and analogies were scored on the **a5b61b5** files (`cursor/blueprint-beginner-images`). `scored_blob` holds the git blob id.
- Code-drawn rows were scored from `blueprint-smoke/bp-01-excerpt.mp4`, which shows only the bp-01 title card and end card. Every other code-drawn row is `needs_render_to_score`. Those rows have `provisional_scores` taken from the committed 5d59cf0 masters (an older renderer), and all of them would fail.

## Important: path-only gate and stale blobs

At 6940897 the PR #17 branch still holds the **old** bp-01, bp-02, analogy and bp-03 PNGs at these same paths (for example, `bp-01-introduction/001.png` is blob 7c80c32 there but 49c480e on a5b61b5). `image_gate.py` matches rows by path and lesson only, so a pass here would also clear the old images. Merge a5b61b5 into the render branch, or make the gate check `scored_blob`, before trusting a pass. The old analogy blobs on that branch (RUNGS, RAILS, an unlabelled list) would all fail.

## Fails (contact sheet: `contact_sheet_fails.jpg`; it predates the refit, so 001-003 and 005 on it are the old padded versions)

| path | lesson | scores (cl/co/cr/br/le/ch/ac) | hard fails | remake prompt | notes |
|---|---|---|---|---|---|
| `course/images/fallback/el-06-circuit-breakers/28.png` | bp-01 | 4/3/3/4/5/1/5 | inconsistent mascot | — | Generated robot, not an approved character sheet: character scores 1 and is a hard fail under the standard. The knockout crop also leaves a visible darker box and cuts the feet flat. No remake prompt: blocked until Stewa |
| `course/images/blueprint-analogies/analogy-ladder.png` | bp-01 | 4/3/3/3/4/-/5 | off-brand colours | `specs/remake/blueprint-analogies__analogy-ladder.txt` | a5b61b5 version: earlier still with PIL relabel. Brown wooden ladder legs are off-palette; headline sits mid-right instead of top-left; gap bracket is a thin code-drawn line. The PR17 branch blob (f49d5b4) is the older R |
| `code-drawn/bp-01-introduction/title-card` | bp-01 | 4/3/3/4/4/1/5 | inconsistent mascot | `specs/remake/bp-01-introduction__title-card.txt` | Carries the generated el-06 robot (hard fail). Right two-thirds empty apart from the robot; plain Inter text stack, no composition. Wordmark itself fine. |
| `code-drawn/bp-01-introduction/end-card` | bp-01 | 3/2/2/4/2/-/4 | muddy or illegible label | `specs/remake/bp-01-introduction__end-card.txt` | Two footer lines are drawn on top of each other ("Education, not financial advice." over "Educational content only. Not financial advice."), which is illegible. An empty outlined box labelled "End screen" fills the right |
| `course/images/bp-01-introduction/004.png` | bp-01 | 5/4/4/3/5/-/5 | off-brand colours | `specs/remake/bp-01-introduction__004.txt` | Refit removed the padding bands (craft now 4). Still fails: the Stop icon is a red octagon; red is not in the palette and cropping cannot remove it. Remake prompt asks for an amber octagon. |
| `course/images/bp-01-introduction/010.png` | bp-01 | 4/4/4/5/5/-/2 | wrong number | `specs/remake/bp-01-introduction__010.txt` | "11 lessons ahead" is wrong: Blueprint has 11 lessons and this is lesson 1, so 10 lessons are ahead. The path also shows a tile count that does not match. Scored the a5b61b5 image; the PR17 branch (6940897) still holds t |
| `course/images/fallback/el-06-circuit-breakers/28.png` | bp-02 | 4/3/3/4/5/1/5 | inconsistent mascot | — | Generated robot, not an approved character sheet: character scores 1 and is a hard fail under the standard. The knockout crop also leaves a visible darker box and cuts the feet flat. No remake prompt: blocked until Stewa |
| `course/images/blueprint-analogies/analogy-list.png` | bp-02 | 4/3/4/4/4/-/3 | — | `specs/remake/blueprint-analogies__analogy-list.txt` | a5b61b5 version: no headline (prompt asks for "YOUR PLAN CHECKLIST"); labels do not match the prompt file ("Band" vs "Box: top and bottom"; "Gaps: space between steps" vs "Gaps: step size"). PR17 branch blob (34a2784) is |
| `course/images/bp-02-what-you-need/004.png` | bp-02 | 3/4/4/3/4/-/4 | off-brand colours | `specs/remake/bp-02-what-you-need__004.txt` | Amber used for non-warnings (gold coin, sand tray, EXAMPLE stamp); a coin icon is on the AVOID list; the seven rows are unexplained icons a beginner cannot name. Scored the a5b61b5 image; the PR17 branch (6940897) still  |
| `course/images/bp-02-what-you-need/011.png` | bp-02 | 4/4/4/4/5/-/3 | wrong number | `specs/remake/bp-02-what-you-need__011.txt` | Invented figure "x5" on the borrowed-money gauge: not in the prompt, not in the lesson, not stamped EXAMPLE. Scored the a5b61b5 image; the PR17 branch (6940897) still holds the OLD blob at this path. |
| `course/images/bp-02-what-you-need/017.png` | bp-02 | 3/4/4/4/5/-/3 | — | `specs/remake/bp-02-what-you-need__017.txt` | Range is drawn as a 3D cube, which contradicts every other range picture (a band with a top and bottom line). A beginner cannot read a cube as a price range. Scored the a5b61b5 image; the PR17 branch (6940897) still hold |
| `course/images/fallback/el-06-circuit-breakers/28.png` | bp-03 | 4/3/3/4/5/1/5 | inconsistent mascot | — | Generated robot, not an approved character sheet: character scores 1 and is a hard fail under the standard. The knockout crop also leaves a visible darker box and cuts the feet flat. No remake prompt: blocked until Stewa |

## Needs a render to score (provisional frames: `contact_sheet_code_drawn_provisional.jpg`)

| path | lesson | scores (cl/co/cr/br/le/ch/ac) | hard fails | remake prompt | notes |
|---|---|---|---|---|---|
| `code-drawn/bp-01-introduction/chart/range-2023/hook` | bp-01 | prov 2/2/2/3/4/-/4 | — | `specs/remake/bp-01-introduction__chart__range-2023__hook.txt` | No smoke render on 6940897 for this row. Provisional scores from the committed 5d59cf0 master frame (stale renderer): FAIL. Real 2023 price chart with 7 axis prices and a date range; a beginner cannot name one idea. Card |
| `code-drawn/bp-01-introduction/chart/range-2023/a-ladder` | bp-01 | prov 2/2/2/3/3/-/4 | — | `specs/remake/bp-01-introduction__chart__range-2023__a-ladder.txt` | No smoke render on 6940897 for this row. Provisional scores from the committed 5d59cf0 master frame (stale renderer): FAIL. Old PR17 analogy-ladder blob (RUNGS only) in left panel, real-price chart right; the ladder and  |
| `code-drawn/bp-01-introduction/chart/range-2023/the-range` | bp-01 | prov 2/2/2/3/4/-/4 | — | `specs/remake/bp-01-introduction__chart__range-2023__the-range.txt` | No smoke render on 6940897 for this row. Provisional scores from the committed 5d59cf0 master frame (stale renderer): FAIL. Same chart as hook; nothing marks the range idea except one amber rule. |
| `code-drawn/bp-01-introduction/chart/range-2023/the-levels` | bp-01 | prov 2/2/2/3/4/-/4 | — | `specs/remake/bp-01-introduction__chart__range-2023__the-levels.txt` | No smoke render on 6940897 for this row. Provisional scores from the committed 5d59cf0 master frame (stale renderer): FAIL. Same chart; levels are unlabelled dashed lines. |
| `code-drawn/bp-01-introduction/chart/range-2023/the-fence` | bp-01 | prov 2/2/2/3/3/-/4 | — | `specs/remake/bp-01-introduction__chart__range-2023__the-fence.txt` | No smoke render on 6940897 for this row. Provisional scores from the committed 5d59cf0 master frame (stale renderer): FAIL. Old RAILS-only fence blob in left panel; chart right; no link. |
| `code-drawn/bp-01-introduction/chart/range-2023/walk-the-summer` | bp-01 | prov 2/2/2/3/4/-/2 | — | `specs/remake/bp-01-introduction__chart__range-2023__walk-the-summer.txt` | No smoke render on 6940897 for this row. Provisional scores from the committed 5d59cf0 master frame (stale renderer): FAIL. Seven dated stops on the same chart. WRONG NUMBER on the first stop: tag "20 Jul 29,792" while t |
| `code-drawn/bp-01-introduction/chart/breakout-2023/the-stop` | bp-01 | prov 3/2/2/3/4/-/4 | — | `specs/remake/bp-01-introduction__chart__breakout-2023__the-stop.txt` | No smoke render on 6940897 for this row. Provisional scores from the committed 5d59cf0 master frame (stale renderer): FAIL. Oct 2023-Mar 2024 chart rising to 71,481; stop idea not marked. |
| `code-drawn/bp-01-introduction/thumbnail` | bp-01 | — | — | `specs/remake/bp-01-introduction__thumbnail.txt` | No thumbnail render exists for this lesson on 6940897 (the only thumbnail.png is the templates demo). Render it, then score. |
| `code-drawn/bp-02-what-you-need/chart/range-2023/hook` | bp-02 | prov 2/2/2/3/4/-/4 | — | `specs/remake/bp-02-what-you-need__chart__range-2023__hook.txt` | No smoke render on 6940897 for this row. Provisional scores from the committed 5d59cf0 master frame (stale renderer): FAIL. Real 2023 price chart with 7 axis prices and a date range; a beginner cannot name one idea. Card |
| `code-drawn/bp-02-what-you-need/chart/range-2023/seven-lines` | bp-02 | prov 1/2/2/4/4/-/3 | — | `specs/remake/bp-02-what-you-need__chart__range-2023__seven-lines.txt` | No smoke render on 6940897 for this row. Provisional scores from the committed 5d59cf0 master frame (stale renderer): FAIL. Shows the price chart only; no seven lines anywhere. Lower third "Seven lines. The pair is the p |
| `code-drawn/bp-02-what-you-need/chart/range-2023/the-three-words` | bp-02 | prov 1/2/2/3/4/-/3 | — | `specs/remake/bp-02-what-you-need__chart__range-2023__the-three-words.txt` | No smoke render on 6940897 for this row. Provisional scores from the committed 5d59cf0 master frame (stale renderer): FAIL. Chart only; range, levels and stop are not shown or labelled. |
| `code-drawn/bp-02-what-you-need/chart/range-2023/no-secrets` | bp-02 | prov 1/2/2/4/4/-/2 | — | `specs/remake/bp-02-what-you-need__chart__range-2023__no-secrets.txt` | No smoke render on 6940897 for this row. Provisional scores from the committed 5d59cf0 master frame (stale renderer): FAIL. Price chart with a "23 Aug 26,432" tag; nothing about secrets at all. |
| `code-drawn/bp-02-what-you-need/chart/range-2023/copy-the-path` | bp-02 | prov 2/2/2/3/4/-/2 | — | `specs/remake/bp-02-what-you-need__chart__range-2023__copy-the-path.txt` | No smoke render on 6940897 for this row. Provisional scores from the committed 5d59cf0 master frame (stale renderer): FAIL. Seven dated stops; WRONG NUMBER on first stop ("20 Jul 29,792" vs "19 July 2023. Close 29,914"). |
| `code-drawn/bp-02-what-you-need/title-card` | bp-02 | prov 4/3/3/4/4/1/5 | — | `specs/remake/bp-02-what-you-need__title-card.txt` | No smoke render for this lesson. 5d59cf0 master title card carries the generated robot (would hard-fail) — expect FAIL. |
| `code-drawn/bp-02-what-you-need/end-card` | bp-02 | prov 3/2/3/4/4/1/4 | — | `specs/remake/bp-02-what-you-need__end-card.txt` | No smoke render for this lesson. 5d59cf0 master end card carries the generated robot (hard fail); bp-01 smoke end card has overlapping footer text, likely the same here — expect FAIL. |
| `code-drawn/bp-02-what-you-need/thumbnail` | bp-02 | — | — | `specs/remake/bp-02-what-you-need__thumbnail.txt` | No thumbnail render exists for this lesson on 6940897 (the only thumbnail.png is the templates demo). Render it, then score. |
| `code-drawn/bp-03-what-is-a-grid-bot/chart/range-2023/hook` | bp-03 | prov 2/2/2/3/4/-/4 | — | `specs/remake/bp-03-what-is-a-grid-bot__chart__range-2023__hook.txt` | No smoke render on 6940897 for this row. Provisional scores from the committed 5d59cf0 master frame (stale renderer): FAIL. Real 2023 price chart with 7 axis prices and a date range; a beginner cannot name one idea. Card |
| `code-drawn/bp-03-what-is-a-grid-bot/chart/range-2023/limit-orders-wait` | bp-03 | prov 2/2/2/3/4/-/4 | — | `specs/remake/bp-03-what-is-a-grid-bot__chart__range-2023__limit-orders-wait.txt` | No smoke render on 6940897 for this row. Provisional scores from the committed 5d59cf0 master frame (stale renderer): FAIL. Chart only; no orders drawn. |
| `code-drawn/bp-03-what-is-a-grid-bot/chart/range-2023/buys-and-sells` | bp-03 | prov 1/2/2/3/4/-/3 | — | `specs/remake/bp-03-what-is-a-grid-bot__chart__range-2023__buys-and-sells.txt` | No smoke render on 6940897 for this row. Provisional scores from the committed 5d59cf0 master frame (stale renderer): FAIL. Chart only; no buys or sells drawn; one amber middle rule. |
| `code-drawn/bp-03-what-is-a-grid-bot/chart/range-2023/where-the-path-stood` | bp-03 | prov 2/2/2/3/4/-/2 | — | `specs/remake/bp-03-what-is-a-grid-bot__chart__range-2023__where-the-path-stood.txt` | No smoke render on 6940897 for this row. Provisional scores from the committed 5d59cf0 master frame (stale renderer): FAIL. Seven dated stops; WRONG NUMBER on first stop ("20 Jul 29,792" vs "19 July 2023. Close 29,914"). |
| `code-drawn/bp-03-what-is-a-grid-bot/title-card` | bp-03 | prov 4/3/3/4/4/1/5 | — | `specs/remake/bp-03-what-is-a-grid-bot__title-card.txt` | No smoke render for this lesson. 5d59cf0 master title card carries the generated robot (would hard-fail) — expect FAIL. |
| `code-drawn/bp-03-what-is-a-grid-bot/end-card` | bp-03 | prov 3/2/3/4/4/1/4 | — | `specs/remake/bp-03-what-is-a-grid-bot__end-card.txt` | No smoke render for this lesson. 5d59cf0 master end card carries the generated robot (hard fail); bp-01 smoke end card has overlapping footer text, likely the same here — expect FAIL. |
| `code-drawn/bp-03-what-is-a-grid-bot/thumbnail` | bp-03 | — | — | `specs/remake/bp-03-what-is-a-grid-bot__thumbnail.txt` | No thumbnail render exists for this lesson on 6940897 (the only thumbnail.png is the templates demo). Render it, then score. |

## Passed (as is or refit)

| path | lesson | scores (cl/co/cr/br/le/ch/ac) | hard fails | remake prompt | notes |
|---|---|---|---|---|---|
| `course/images/style-ref/01M6MSHVNHX3WQH81XS8KQK1HT.png` | bp-01 | 5/4/4/5/4/-/5 | — | — | Scored the wordmark crop as used. Full cover must never be shown: it has coin logos, profit-style claims ("Consistent returns") and the author name. At the 48px title-bar size the letter-spaced BUILDER line is near-illeg |
| `course/images/blueprint-analogies/analogy-fence.png` | bp-01 | 5/4/4/4/4/-/5 | — | — | a5b61b5 version (this is the ChatGPT style anchor). Zig-zag added by code but clean. Note: the PR17 branch blob (ce78c66) is the older RAILS-only version without the zig-zag or labels; that version would fail (clarity 2, |
| `course/images/bp-01-introduction/001.png` | bp-01 | 5/4/4/5/5/-/5 | — | — | Refit removed the blurred letterbox bands; no seam or smudge left, grid fades softly into the navy fill. Labels and margins unchanged and checked by eye. |
| `course/images/bp-01-introduction/002.png` | bp-01 | 5/4/4/5/5/-/5 | — | — | Refit removed the blurred letterbox bands; no seam or smudge left, grid fades softly into the navy fill. Labels and margins unchanged and checked by eye. |
| `course/images/bp-01-introduction/003.png` | bp-01 | 4/4/4/5/4/-/5 | — | — | Refit removed the blurred letterbox bands; no seam or smudge left, grid fades softly into the navy fill. Labels and margins unchanged and checked by eye. |
| `course/images/bp-01-introduction/005.png` | bp-01 | 5/4/4/5/5/-/5 | — | — | Refit removed the blurred letterbox bands; no seam or smudge left, grid fades softly into the navy fill. Labels and margins unchanged and checked by eye. |
| `course/images/bp-01-introduction/006.png` | bp-01 | 5/4/4/5/5/-/5 | — | — | Scored the a5b61b5 image; the PR17 branch (6940897) still holds the OLD blob at this path. |
| `course/images/bp-01-introduction/007.png` | bp-01 | 5/5/4/5/5/-/5 | — | — | Scored the a5b61b5 image; the PR17 branch (6940897) still holds the OLD blob at this path. |
| `course/images/bp-01-introduction/008.png` | bp-01 | 5/4/4/4/5/-/5 | — | — | Light paper notebook; acceptable. Scored the a5b61b5 image; the PR17 branch (6940897) still holds the OLD blob at this path. |
| `course/images/bp-01-introduction/009.png` | bp-01 | 5/4/4/5/5/-/4 | — | — | Extra word SEND on the crossed-out button; reads correctly. Scored the a5b61b5 image; the PR17 branch (6940897) still holds the OLD blob at this path. |
| `course/images/bp-01-introduction/011.png` | bp-01 | 5/4/4/5/5/-/5 | — | — | Scored the a5b61b5 image; the PR17 branch (6940897) still holds the OLD blob at this path. |
| `course/images/bp-01-introduction/012.png` | bp-01 | 4/4/4/5/5/-/5 | — | — | Scored the a5b61b5 image; the PR17 branch (6940897) still holds the OLD blob at this path. |
| `course/images/bp-01-introduction/013.png` | bp-01 | 4/4/4/4/5/-/5 | — | — | Counted 9 lines = 8 even steps; matches headline. Scored the a5b61b5 image; the PR17 branch (6940897) still holds the OLD blob at this path. |
| `course/images/bp-01-introduction/014.png` | bp-01 | 5/5/4/5/5/-/5 | — | — | Scored the a5b61b5 image; the PR17 branch (6940897) still holds the OLD blob at this path. |
| `course/images/bp-01-introduction/015.png` | bp-01 | 4/4/4/4/5/-/4 | — | — | Laptop shows a small candle chart (generic, no app or exchange); acceptable. Scored the a5b61b5 image; the PR17 branch (6940897) still holds the OLD blob at this path. |
| `course/images/bp-01-introduction/016.png` | bp-01 | 5/4/4/4/5/-/5 | — | — | Scored the a5b61b5 image; the PR17 branch (6940897) still holds the OLD blob at this path. |
| `course/images/bp-01-introduction/017.png` | bp-01 | 5/5/4/5/5/-/5 | — | — | Scored the a5b61b5 image; the PR17 branch (6940897) still holds the OLD blob at this path. |
| `course/images/bp-01-introduction/018.png` | bp-01 | 5/5/4/5/5/-/5 | — | — | Scored the a5b61b5 image; the PR17 branch (6940897) still holds the OLD blob at this path. |
| `course/images/style-ref/01M6MSHVNHX3WQH81XS8KQK1HT.png` | bp-02 | 5/4/4/5/4/-/5 | — | — | Scored the wordmark crop as used. Full cover must never be shown: it has coin logos, profit-style claims ("Consistent returns") and the author name. At the 48px title-bar size the letter-spaced BUILDER line is near-illeg |
| `course/images/bp-02-what-you-need/001.png` | bp-02 | 5/4/4/5/5/-/5 | — | — | Scored the a5b61b5 image; the PR17 branch (6940897) still holds the OLD blob at this path. |
| `course/images/bp-02-what-you-need/002.png` | bp-02 | 5/4/4/5/5/-/5 | — | — | Crossed-out BUY tag is extra text but clear. Scored the a5b61b5 image; the PR17 branch (6940897) still holds the OLD blob at this path. |
| `course/images/bp-02-what-you-need/003.png` | bp-02 | 5/4/4/5/5/-/5 | — | — | Glass table runs close to the left and right edges (object, not text); margins judged OK by eye. Scored the a5b61b5 image; the PR17 branch (6940897) still holds the OLD blob at this path. |
| `course/images/bp-02-what-you-need/005.png` | bp-02 | 5/4/4/5/5/-/5 | — | — | Scored the a5b61b5 image; the PR17 branch (6940897) still holds the OLD blob at this path. |
| `course/images/bp-02-what-you-need/006.png` | bp-02 | 5/4/4/4/5/-/5 | — | — | EXAMPLE stamp is amber (amber is reserved for warnings); minor, scored 4. Scored the a5b61b5 image; the PR17 branch (6940897) still holds the OLD blob at this path. |
| `course/images/bp-02-what-you-need/007.png` | bp-02 | 5/4/4/4/5/-/5 | — | — | Scored the a5b61b5 image; the PR17 branch (6940897) still holds the OLD blob at this path. |
| `course/images/bp-02-what-you-need/008.png` | bp-02 | 4/4/4/4/4/-/5 | — | — | Busy (five objects and four arrows) but readable. Scored the a5b61b5 image; the PR17 branch (6940897) still holds the OLD blob at this path. |
| `course/images/bp-02-what-you-need/009.png` | bp-02 | 5/4/4/5/5/-/5 | — | — | Scored the a5b61b5 image; the PR17 branch (6940897) still holds the OLD blob at this path. |
| `course/images/bp-02-what-you-need/010.png` | bp-02 | 4/4/4/5/5/-/4 | — | — | Numbers shown as squiggles; idea still clear. Scored the a5b61b5 image; the PR17 branch (6940897) still holds the OLD blob at this path. |
| `course/images/bp-02-what-you-need/012.png` | bp-02 | 5/4/4/5/5/-/5 | — | — | Scored the a5b61b5 image; the PR17 branch (6940897) still holds the OLD blob at this path. |
| `course/images/bp-02-what-you-need/013.png` | bp-02 | 5/4/4/5/5/-/5 | — | — | Pin on tile 2 of 11, correct for lesson 2. Scored the a5b61b5 image; the PR17 branch (6940897) still holds the OLD blob at this path. |
| `course/images/bp-02-what-you-need/014.png` | bp-02 | 5/4/4/5/5/-/5 | — | — | Scored the a5b61b5 image; the PR17 branch (6940897) still holds the OLD blob at this path. |
| `course/images/bp-02-what-you-need/015.png` | bp-02 | 5/4/4/5/5/-/5 | — | — | Scored the a5b61b5 image; the PR17 branch (6940897) still holds the OLD blob at this path. |
| `course/images/bp-02-what-you-need/016.png` | bp-02 | 5/4/4/4/5/-/5 | — | — | Seven boxes counted. Scored the a5b61b5 image; the PR17 branch (6940897) still holds the OLD blob at this path. |
| `course/images/bp-02-what-you-need/018.png` | bp-02 | 5/4/4/4/5/-/5 | — | — | Scored the a5b61b5 image; the PR17 branch (6940897) still holds the OLD blob at this path. |
| `course/images/bp-02-what-you-need/019.png` | bp-02 | 4/4/4/5/4/-/5 | — | — | Five objects for four labels; smallest labels near the limit. Scored the a5b61b5 image; the PR17 branch (6940897) still holds the OLD blob at this path. |
| `course/images/bp-02-what-you-need/020.png` | bp-02 | 5/5/4/5/5/-/5 | — | — | Seven ticks counted. Scored the a5b61b5 image; the PR17 branch (6940897) still holds the OLD blob at this path. |
| `course/images/bp-02-what-you-need/021.png` | bp-02 | 5/4/4/5/5/-/5 | — | — | Scored the a5b61b5 image; the PR17 branch (6940897) still holds the OLD blob at this path. |
| `course/images/style-ref/01M6MSHVNHX3WQH81XS8KQK1HT.png` | bp-03 | 5/4/4/5/4/-/5 | — | — | Scored the wordmark crop as used. Full cover must never be shown: it has coin logos, profit-style claims ("Consistent returns") and the author name. At the 48px title-bar size the letter-spaced BUILDER line is near-illeg |

## Pending

The 19 rows `course/images/bp-03-what-is-a-grid-bot/001-019.png` have not landed in `out/` yet. ChatGPT downloads are still sitting in `~/Downloads`, and one of them, "Neon Robot Order Ladder.png", contains a generated robot. That would be a hard fail under the character rule.

## Refit 13 Nov, 5:50pm WITA

bp-01 001-005 were re-made from `gen/bp-01-introduction/NNN/web.png` by `/workspace/blueprint-beginner/refit.py`. Each image was scaled to 1536x864 and centred on a solid navy fill matched to its edge, with a 32px feathered join and no blur. A centre crop to 3:2 would have cut 130px from each side, through labels and cards. Backups are `NNN.bak.png`. 001, 002, 003 and 005 now pass. 004 still fails because of its red stop sign.
