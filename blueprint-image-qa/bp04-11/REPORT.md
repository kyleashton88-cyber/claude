# BP-04..BP-11 image QA, stage 1 (score only, nothing fixed)

Scored by Creative Studio, 14 Nov 2026 WITA. Standard: `skills/image-quality-standard` (7 categories, pass = every category >= 4 and no hard fail) plus Stewart's beginner-clear checks, applied strictly.

**Result (stage 1): 0 pass / 161 fail of 161. Current after BP-04 remake round 2 and the strict arrow re-check: 13/161 pass, BP-04 13/20.** No BP-04..BP-11 lesson is passing. Every image needs a remake.**

- Scope: every beat image in `course/scripts/bp-04..bp-11*.json` @ `cursor/blueprint-professional-rebuild-d1f6` fbb3f9c. `course/blueprint-rebuild/BP04-11_IMAGE_MANIFEST.json` was not on the branch yet (404), so scope comes from the scripts. Re-check against the manifest when it lands.
- Sources: all 161 files are byte-identical on both branches (d1f6 @ fbb3f9c and beginner-images @ adc3524). They are the old gbb-v3 fallback batch, which `FALLBACK_MANIFEST.json` lists as `pass`. That status is superseded.
- Size and file names: all 161 are 1536x1024 RGB at the path each beat expects. The images fail on content, not format.
- No mascot, no Market Pros, ABN, entity or exchange branding in any image. The headlines and labels have no misspellings, but several headlines run their words together.
- Do not use the existing BP-04..11 renders (`course/masters`, `masters-v2`, `masters-stills`, `render/passed`). They were built from these failing stills.

## Why the whole set fails

1. **Not beginner-clear.** Two-word code headlines (SAY SORT, COVER THREE, JUMPED BAR, PIN EDIT, IN/BASE/SAME, LID DOWN) over abstract chips, CPU tiles or empty glass cards. The beat's idea can't be read with the sound off.
2. **Title and disclaimer cards are empty glass rectangles** (8 title cards) or word chips ('EDUCATION / RISK / EXAMPLE'). None says 'Education only. Not financial advice.'
3. **Wrong labels or numbers:** bp-05 004 (badge says '19 GAPS' over 13 lines), bp-05 006 ('39' where the lesson says 38 gaps, not 40), bp-07 005/010/017/019 (LINES as a field, the exact confusion the lesson warns against), bp-09 006 ('LIQUID'), bp-11 012 ('TWO FLAGS' over three flags), bp-07 014 (reads as 'tick five, then press confirm').
4. **Artifacts:** smudged pseudo-text (bp-08 006, bp-09 008), dotted pseudo-text (bp-05 004), compositing patches or seams under the headline strip (bp-05 015, several bp-08).
5. **Tiny, illegible labels** (much of bp-09, bp-10 and bp-11), with focal subjects filling under 10% of the frame.
6. **Outro cards don't name the next lesson.**

Scores are listed as clarity / composition / craft / brand / legibility / character / label accuracy, with '-' meaning no character in the frame.

## bp-04-market-regimes: Market regimes (20 images, 0 pass, 20 fail)

1. `course/images/bp-04-market-regimes/001.png`: **FAIL** (2/3/3/4/4/-/2). Weave/Leave cards do not show the idea: the 'Weave' line barely crosses the rungs and the 'Leave' line flattens inside the ladder instead of leaving it; cryptic headline 'SAME LADDER'; charts carry no EXAMPLE stamp. *Fix status:* needs remake, prompt `specs/remake/bp-04-market-regimes__001.txt`.
2. `course/images/bp-04-market-regimes/002.png`: **FAIL** (3/3/4/4/2/-/3). Disclaimer reads 'STUDY ONLY / NOT ADVICE', not 'Education only. Not financial advice.'; generic document + magnifier icon. **Hard fail:** illegible label: 'NOT ADVICE' is tiny letter-spaced grey type. *Fix status:* needs remake, prompt `specs/remake/bp-04-market-regimes__002.txt`.
3. `course/images/bp-04-market-regimes/003.png`: **FAIL** (1/2/3/4/4/-/3). Title card is a glowing rectangle of blank bars with a 'LESSON' chip: no subject (rubric: a glowing rectangle is not a composition); no range/trend/break shapes. *Fix status:* needs remake, prompt `specs/remake/bp-04-market-regimes__003.txt`.
4. `course/images/bp-04-market-regimes/004.png`: **FAIL** (3/4/3/4/4/-/3). Closest to the beat, but the BREAK chart never visibly leaves the band (line exits flat at the top line); thin small labels; no EXAMPLE stamp on charts. *Fix status:* needs remake, prompt `specs/remake/bp-04-market-regimes__004.txt`.
5. `course/images/bp-04-market-regimes/005.png`: **FAIL** (2/3/3/4/3/-/2). Abstract 'SORT' glass slab and faint 'SPACING' chip on a wavy line: does not show sorting a price path; 'SPACING' chip is low-contrast. *Fix status:* needs remake, prompt `specs/remake/bp-04-market-regimes__005.txt`.
6. `course/images/bp-04-market-regimes/006.png`: **FAIL** (2/3/3/4/3/-/2). Rungs drawn as pill bars, one bump circled; floating 'RUNG' and 'EXAMPLE' tags with no arrows; does not show price crossing the same lines again and again; 'EXAMPLE' used as a side label, not a stamp. *Fix status:* needs remake, prompt `specs/remake/bp-04-market-regimes__006.txt`.
7. `course/images/bp-04-market-regimes/007.png`: **FAIL** (1/3/3/4/4/-/1). Grey staircase with a pile of glass cubes labelled 'PILE': no price path, no higher highs; does not teach 'trend'. *Fix status:* needs remake, prompt `specs/remake/bp-04-market-regimes__007.txt`.
8. `course/images/bp-04-market-regimes/008.png`: **FAIL** (3/3/3/4/4/-/2). Band with a line drifting to the band's lower edge labelled 'OUT' and a dashed 'STOP' line: price does not clearly leave and stay out; 'STOP' is new jargon; no EXAMPLE stamp. *Fix status:* needs remake, prompt `specs/remake/bp-04-market-regimes__008.txt`.
9. `course/images/bp-04-market-regimes/009.png`: **FAIL** (2/2/3/4/3/-/2). Mostly empty card with one flat line, a tiny 'RANGE' pill and an EXAMPLE stamp: no example path to read left to right. *Fix status:* needs remake, prompt `specs/remake/bp-04-market-regimes__009.txt`.
10. `course/images/bp-04-market-regimes/010.png`: **FAIL** (2/3/3/4/4/-/2). Text-only map RANGE->LADDER, TREND->PILE, BREAK->STOP: 'PILE'/'STOP' unexplained jargon, no picture, no decision shown. *Fix status:* needs remake, prompt `specs/remake/bp-04-market-regimes__010.txt`.
11. `course/images/bp-04-market-regimes/011.png`: **FAIL** (2/3/3/4/4/-/2). Big sine wave far outside a thin dashed band with 'BAND'/'WEAVE' bracket; headline 'TOO WIDE' contradicts the beat (ordinary day = the usual wiggle size); no EXAMPLE on chart. *Fix status:* needs remake, prompt `specs/remake/bp-04-market-regimes__011.txt`.
12. `course/images/bp-04-market-regimes/012.png`: **FAIL** (1/2/2/4/2/-/2). Stack of identical lines with one vertical tick: no calm path, no news spike, no thin-book idea; meaning unreadable with sound off. **Hard fail:** illegible label: 'JUMPED' tag is tiny. *Fix status:* needs remake, prompt `specs/remake/bp-04-market-regimes__012.txt`.
13. `course/images/bp-04-market-regimes/013.png`: **FAIL** (3/4/3/4/4/-/3). Ladder fits Range, crossed out on Trend/Break: but headline 'GRID FIRST' reads as an instruction when the beat says grid-first is the mistake; no wrong/right framing. *Fix status:* needs remake, prompt `specs/remake/bp-04-market-regimes__013.txt`.
14. `course/images/bp-04-market-regimes/014.png`: **FAIL** (2/3/3/4/4/-/2). Four floating chips (RANGE/TREND/BREAK/LADDER) with no picture or sequence: 'name it, then decide' not shown. *Fix status:* needs remake, prompt `specs/remake/bp-04-market-regimes__014.txt`.
15. `course/images/bp-04-market-regimes/015.png`: **FAIL** (2/3/3/4/3/-/2). CPU-style 'RANGE' chip and rubber stamp on a dotted wave: does not show sorting a sketched path into one of three boxes or writing a reason; small chip text. *Fix status:* needs remake, prompt `specs/remake/bp-04-market-regimes__015.txt`.
16. `course/images/bp-04-market-regimes/016.png`: **FAIL** (2/2/2/4/4/-/2). 'COVER THREE' cryptic; slanted panel cuts across the three mini charts; no EXAMPLE. **Hard fail:** artifact: stray dark vertical bars at left of the chart area and a skewed glass slab overlapping the charts. *Fix status:* needs remake, prompt `specs/remake/bp-04-market-regimes__016.txt`.
17. `course/images/bp-04-market-regimes/017.png`: **FAIL** (2/3/3/4/4/-/2). Left margin only 48px (headline/RANGE chip), under the 80px target. 'SAY SORT' cryptic; chips plus a locked 'SPACING' chip; no path. *Fix status:* needs remake, prompt `specs/remake/bp-04-market-regimes__017.txt`.
18. `course/images/bp-04-market-regimes/018.png`: **FAIL** (2/3/3/4/4/-/2). A single line with two dips numbered 1 and 2 and a 'TWICE' tag: no grid lines to cross, so the crossings are not shown. *Fix status:* needs remake, prompt `specs/remake/bp-04-market-regimes__018.txt`.
19. `course/images/bp-04-market-regimes/019.png`: **FAIL** (3/3/3/4/4/-/3). Dial with amber X and a Range/Trend/Break list where only Range has an amber dot: reads as 'Range is wrong' - confusing; no 'no go signal / you decide' message. *Fix status:* needs remake, prompt `specs/remake/bp-04-market-regimes__019.txt`.
20. `course/images/bp-04-market-regimes/020.png`: **FAIL** (3/3/4/4/4/-/3). Icons PAGE / GAPS / EXAMPLE stamp: next lesson ('Choosing grid spacing and range') not named; 'GAPS' unexplained. *Fix status:* needs remake, prompt `specs/remake/bp-04-market-regimes__020.txt`.

## bp-05-spacing-and-range: Choosing grid spacing and range (19 images, 0 pass, 19 fail)

1. `course/images/bp-05-spacing-and-range/001.png`: **FAIL** (2/3/3/4/4/-/2). Light streaks into a glowing 'EXIT' block: no band, no weave, no 'too tight' comparison; 'TIGHT BAND' headline alone does not teach the idea. *Fix status:* needs remake, prompt `specs/remake/bp-05-spacing-and-range__001.txt`.
2. `course/images/bp-05-spacing-and-range/002.png`: **FAIL** (3/3/4/4/4/-/3). Disclaimer reads 'READ ONLY / NOT ADVICE' with a book icon, not 'Education only. Not financial advice.'. *Fix status:* needs remake, prompt `specs/remake/bp-05-spacing-and-range__002.txt`.
3. `course/images/bp-05-spacing-and-range/003.png`: **FAIL** (1/2/3/4/4/-/3). Title card is an empty glass card with two bracket lines and a 'LESSON' chip: glowing rectangle, no subject. *Fix status:* needs remake, prompt `specs/remake/bp-05-spacing-and-range__003.txt`.
4. `course/images/bp-05-spacing-and-range/004.png`: **FAIL** (2/3/3/4/3/-/1). Lines are not labelled as orders, gaps are not marked, '20 order lines' is not shown. **Hard fail:** wrong number: badge says '19 GAPS' but only 13 lines (12 gaps) are drawn; artifact: rows of dotted pseudo-text along the lines. *Fix status:* needs remake, prompt `specs/remake/bp-05-spacing-and-range__004.txt`.
5. `course/images/bp-05-spacing-and-range/005.png`: **FAIL** (2/3/3/4/4/-/2). 'HALF SPAN' headline mislabels the beat (the span from 19 gaps x 0.5%); no 0.5% or 9.5% shown; 'SPAN' bracket and '19 GAPS' tag float between two lines with no ladder. *Fix status:* needs remake, prompt `specs/remake/bp-05-spacing-and-range__005.txt`.
6. `course/images/bp-05-spacing-and-range/006.png`: **FAIL** (2/3/3/4/4/-/1). 'NOT FORTY' on a stack of slabs: no before/after ladder, no labels, no EXAMPLE. **Hard fail:** wrong number: a crossed 40 beside a glowing unlabelled '39' reads as '39 gaps, not 40'; the lesson (beat 6) says 38 gaps, not 40 (39 is only right as a line count, and nothing says lines). *Fix status:* needs remake, prompt `specs/remake/bp-05-spacing-and-range__006.txt`.
7. `course/images/bp-05-spacing-and-range/007.png`: **FAIL** (3/3/3/4/3/-/3). Cyan 'RANGE' bracket beside faint grey ticks labelled 'SPACING' (low contrast): the idea 'range first, then spacing' is only implied. *Fix status:* needs remake, prompt `specs/remake/bp-05-spacing-and-range__007.txt`.
8. `course/images/bp-05-spacing-and-range/008.png`: **FAIL** (2/3/3/4/4/-/2). Two empty bars over blue bars labelled 'WIDE'/'THIN', one crossed: no cost-of-a-buy-and-sell shown against the gap; 'COST CHECK' not explained. *Fix status:* needs remake, prompt `specs/remake/bp-05-spacing-and-range__008.txt`.
9. `course/images/bp-05-spacing-and-range/009.png`: **FAIL** (3/3/3/4/4/-/2). Dense vs sparse ladder with 'CROWD'/'CLEAR'/'COST' tags: 'COST' tag points at nothing; cost check against gap size not shown. **Hard fail:** cramped margin: headline starts 40px from the left edge. *Fix status:* needs remake, prompt `specs/remake/bp-05-spacing-and-range__009.txt`.
10. `course/images/bp-05-spacing-and-range/010.png`: **FAIL** (3/4/3/4/4/-/3). Crossed '20 WRONG' vs '19 GAPS': numbers unlabelled as a sum ('20 x 0.5% = 10%' wrong vs '19 x 0.5% = 9.5%' right is the beat); no EXAMPLE. *Fix status:* needs remake, prompt `specs/remake/bp-05-spacing-and-range__010.txt`.
11. `course/images/bp-05-spacing-and-range/011.png`: **FAIL** (2/3/3/4/4/-/2). Dashed line with a tiny candle cluster and 'WICK'/'CLOSE' chips with no arrows: range needing room for wicks is not shown. *Fix status:* needs remake, prompt `specs/remake/bp-05-spacing-and-range__011.txt`.
12. `course/images/bp-05-spacing-and-range/012.png`: **FAIL** (3/4/4/4/4/-/3). Two knobs crossed 'BOTH' vs one knob 'ONE': knobs are not named (step, range), so 'one change at a time' is only half-readable. *Fix status:* needs remake, prompt `specs/remake/bp-05-spacing-and-range__012.txt`.
13. `course/images/bp-05-spacing-and-range/013.png`: **FAIL** (3/3/3/4/4/-/3). Three word chips 'PERCENT / GAPS / ORDERS' in an empty bar: not a written line, no example sentence; mostly empty frame. *Fix status:* needs remake, prompt `specs/remake/bp-05-spacing-and-range__013.txt`.
14. `course/images/bp-05-spacing-and-range/014.png`: **FAIL** (3/3/3/4/4/-/3). Small glass card listing BAND / GAPS / COST with an EXAMPLE stamp: list, not a picture of a quiet page with a band, gap count and cost check. *Fix status:* needs remake, prompt `specs/remake/bp-05-spacing-and-range__014.txt`.
15. `course/images/bp-05-spacing-and-range/015.png`: **FAIL** (2/3/3/4/4/-/2). Five chips 'RANGE / GAPS / 19 / COST / ONE': recap as bare words, no picture; '19' and 'ONE' meaningless without context. **Hard fail:** artifact: dark compositing patch visible behind the right of the headline. *Fix status:* needs remake, prompt `specs/remake/bp-05-spacing-and-range__015.txt`.
16. `course/images/bp-05-spacing-and-range/016.png`: **FAIL** (2/3/3/4/4/-/2). Card with a mini list icon, '19' and 'PRACTICE': 20 lines -> 19 gaps not shown. *Fix status:* needs remake, prompt `specs/remake/bp-05-spacing-and-range__016.txt`.
17. `course/images/bp-05-spacing-and-range/017.png`: **FAIL** (2/3/3/4/4/-/2). Bar with '19' and 'HALF' chips and a 'PRACTICE' tag: '19 gaps x 0.5% = 9.5%' not shown; 'HALF' ambiguous. *Fix status:* needs remake, prompt `specs/remake/bp-05-spacing-and-range__017.txt`.
18. `course/images/bp-05-spacing-and-range/018.png`: **FAIL** (2/3/3/4/4/-/2). Two blank glass tablets, one tagged 'BLANK': does not show 'recount on paper, not in a live ticket'. *Fix status:* needs remake, prompt `specs/remake/bp-05-spacing-and-range__018.txt`.
19. `course/images/bp-05-spacing-and-range/019.png`: **FAIL** (3/3/4/4/4/-/3). Glass page with a big EXAMPLE stamp and a 'NEXT' button: next lesson ('Entry and exit rules') not named. *Fix status:* needs remake, prompt `specs/remake/bp-05-spacing-and-range__019.txt`.

## bp-06-entry-and-exit: Entry and exit rules (20 images, 0 pass, 20 fail)

1. `course/images/bp-06-entry-and-exit/001.png`: **FAIL** (2/3/3/4/4/-/2). 'NO EXIT' over an ENTRY/EXIT card whose EXIT column is a block of blank lines covered by a stamp: 'entry without an exit cannot finish' is not shown (the exit column is full, not empty). *Fix status:* needs remake, prompt `specs/remake/bp-06-entry-and-exit__001.txt`.
2. `course/images/bp-06-entry-and-exit/002.png`: **FAIL** (3/3/3/4/4/-/3). Shield with 'EDUCATION' and a CPU chip reading 'RISK': chip icon is meaningless; does not read 'Education only. Not financial advice.'. *Fix status:* needs remake, prompt `specs/remake/bp-06-entry-and-exit__002.txt`.
3. `course/images/bp-06-entry-and-exit/003.png`: **FAIL** (2/2/3/4/4/-/3). Title card: an empty glass bar holding two buttons 'ENTRY' and 'EXIT' plus a stamp; no subject; headline drops 'Entry and'. *Fix status:* needs remake, prompt `specs/remake/bp-06-entry-and-exit__003.txt`.
4. `course/images/bp-06-entry-and-exit/004.png`: **FAIL** (3/3/3/4/4/-/3). Two empty columns 'BEFORE'/'FINISH' with a large stamp over the FINISH column: no example contents, stamp covers the column it should explain. *Fix status:* needs remake, prompt `specs/remake/bp-06-entry-and-exit__004.txt`.
5. `course/images/bp-06-entry-and-exit/005.png`: **FAIL** (3/4/3/4/4/-/3). 'START 2 / FINISH 1' cards: closest to the beat, but the dim '2' is low contrast and nothing shows a finish sentence being written. *Fix status:* needs remake, prompt `specs/remake/bp-06-entry-and-exit__005.txt`.
6. `course/images/bp-06-entry-and-exit/006.png`: **FAIL** (2/3/3/4/3/-/2). Three thin lines with one line drifting barely out at the right; an empty tag box next to 'EXAMPLE': price leaving the band is not visible; band not labelled. *Fix status:* needs remake, prompt `specs/remake/bp-06-entry-and-exit__006.txt`.
7. `course/images/bp-06-entry-and-exit/007.png`: **FAIL** (2/3/3/4/3/-/2). Three cyan bars in an ellipse with letter-spaced 'GAPS'/'COUNTS' captions: none of the three checks (range, gap clears cost, both columns) shown; headline word gap is tight ('THREECHECKS'). *Fix status:* needs remake, prompt `specs/remake/bp-06-entry-and-exit__007.txt`.
8. `course/images/bp-06-entry-and-exit/008.png`: **FAIL** (3/3/3/4/2/-/3). Band splitting into a path inside a big empty card: correct idea but unreadable at lesson size; no worked sentences. **Hard fail:** illegible label: 'BAND' and 'PATH' tags are tiny thin type. *Fix status:* needs remake, prompt `specs/remake/bp-06-entry-and-exit__008.txt`.
9. `course/images/bp-06-entry-and-exit/009.png`: **FAIL** (3/3/3/4/4/-/3). Crossed-out 'HOPE' cloud on a line: acceptable symbol but no entry/finish pairing; 'NOT HOPE' headline is unclear. *Fix status:* needs remake, prompt `specs/remake/bp-06-entry-and-exit__009.txt`.
10. `course/images/bp-06-entry-and-exit/010.png`: **FAIL** (2/3/3/4/4/-/2). Dashed arrow line through an 'INVALIDATION' chip: jargon chip with no picture of the finish path (price leaving the band). *Fix status:* needs remake, prompt `specs/remake/bp-06-entry-and-exit__010.txt`.
11. `course/images/bp-06-entry-and-exit/011.png`: **FAIL** (3/3/3/4/4/-/3). Crossed 'I WILL KNOW' over a small path arrow and 'PATH' tag: right idea, weakly drawn; 'WRITE PATH' headline unclear. *Fix status:* needs remake, prompt `specs/remake/bp-06-entry-and-exit__011.txt`.
12. `course/images/bp-06-entry-and-exit/012.png`: **FAIL** (2/3/3/4/4/-/2). Two chips 'FINISH 1' / 'START 2' floating on a dark frame with a stamp: no paper form or copying shown; mostly empty. *Fix status:* needs remake, prompt `specs/remake/bp-06-entry-and-exit__012.txt`.
13. `course/images/bp-06-entry-and-exit/013.png`: **FAIL** (3/3/3/4/4/-/3). Card 'SIZE -> LATER': readable but a word card, not a picture; fine-print 'SIZE' label is tiny. *Fix status:* needs remake, prompt `specs/remake/bp-06-entry-and-exit__013.txt`.
14. `course/images/bp-06-entry-and-exit/014.png`: **FAIL** (2/3/3/4/3/-/2). Open book with scribble-texture pages and an EXAMPLE stamp: no two sentences, no drawing; headline word gap tight ('BOTHPAGES'). *Fix status:* needs remake, prompt `specs/remake/bp-06-entry-and-exit__014.txt`.
15. `course/images/bp-06-entry-and-exit/015.png`: **FAIL** (2/3/3/4/4/-/2). Checklist of single words 'COLUMNS / FIRST / POINT / HOPE / LATER': recap words are cryptic out of context; 'HOPE' is ticked, which contradicts 'hope crossed out'. *Fix status:* needs remake, prompt `specs/remake/bp-06-entry-and-exit__015.txt`.
16. `course/images/bp-06-entry-and-exit/016.png`: **FAIL** (3/3/3/4/4/-/3). Notebook with 'BEFORE'/'FINISH' tags and empty boxes plus 'PRACTICE': ok idea, generic; tiny boxes; no example sentence. *Fix status:* needs remake, prompt `specs/remake/bp-06-entry-and-exit__016.txt`.
17. `course/images/bp-06-entry-and-exit/017.png`: **FAIL** (2/3/3/4/3/-/2). Four chips 'FINISH / START / PRACTICE / EXAMPLE': no picture; 'EXAMPLE' used as a chip; headline word gap tight ('ONEFIRST'). *Fix status:* needs remake, prompt `specs/remake/bp-06-entry-and-exit__017.txt`.
18. `course/images/bp-06-entry-and-exit/018.png`: **FAIL** (2/3/3/4/4/-/2). Path line with an empty price tag and 'PRACTICE'/'EXAMPLE' chips: band not drawn, 'leaves the band and does not return' not shown. *Fix status:* needs remake, prompt `specs/remake/bp-06-entry-and-exit__018.txt`.
19. `course/images/bp-06-entry-and-exit/019.png`: **FAIL** (3/3/3/4/4/-/3). 'PATH' vs dim 'MISS' lines in a card: audit question (can a classmate point at the finish path?) not shown; 'MISS' low contrast. *Fix status:* needs remake, prompt `specs/remake/bp-06-entry-and-exit__019.txt`.
20. `course/images/bp-06-entry-and-exit/020.png`: **FAIL** (2/3/3/4/4/-/2). Empty card with an arrow and stamp under 'NEXT CARD': next lesson ('Spot paper trading') not named. *Fix status:* needs remake, prompt `specs/remake/bp-06-entry-and-exit__020.txt`.

## bp-07-spot-paper-trading: Spot paper trading (20 images, 0 pass, 20 fail)

1. `course/images/bp-07-spot-paper-trading/001.png`: **FAIL** (3/3/3/4/4/-/3). Notebook -> blank form with a stamp: 'walk fields on a paper or demo screen, no order placed' only implied; 'PAPER SPOT' headline is jargon. *Fix status:* needs remake, prompt `specs/remake/bp-07-spot-paper-trading__001.txt`.
2. `course/images/bp-07-spot-paper-trading/002.png`: **FAIL** (2/3/3/4/4/-/2). Single bar reading 'EDUCATION, RISK, EXAMPLE': word list, not 'Education only. Not financial advice.'. *Fix status:* needs remake, prompt `specs/remake/bp-07-spot-paper-trading__002.txt`.
3. `course/images/bp-07-spot-paper-trading/003.png`: **FAIL** (2/2/3/4/4/-/3). Title card: an open book in a glass frame with a stamp; headline word order 'SPOT PAPER' differs from the title 'Spot paper trading'. *Fix status:* needs remake, prompt `specs/remake/bp-07-spot-paper-trading__003.txt`.
4. `course/images/bp-07-spot-paper-trading/004.png`: **FAIL** (1/3/3/4/4/-/1). 'BLANK MARK' with a blank glass key-cap: does not say or show 'not affiliated with any venue'; meaning unrecoverable. *Fix status:* needs remake, prompt `specs/remake/bp-07-spot-paper-trading__004.txt`.
5. `course/images/bp-07-spot-paper-trading/005.png`: **FAIL** (2/3/3/4/3/-/1). Tiny chip text inside a mostly empty card. **Hard fail:** wrong label: the five field chips read PAIR / UPPER / LOWER / GAPS / LINES; the lesson's five are pair, upper, lower, gap count and the two sentences (LINES is the exact confusion the lesson warns against). *Fix status:* needs remake, prompt `specs/remake/bp-07-spot-paper-trading__005.txt`.
6. `course/images/bp-07-spot-paper-trading/006.png`: **FAIL** (3/4/3/4/4/-/3). 'SPOT' tile vs crossed 'CONTRACT' tile: readable, but the X sits on top of the word, leverage is not mentioned, and the EXAMPLE stamp sits on a non-figure. *Fix status:* needs remake, prompt `specs/remake/bp-07-spot-paper-trading__006.txt`.
7. `course/images/bp-07-spot-paper-trading/007.png`: **FAIL** (3/4/3/4/4/-/3). Crossed key icon 'NO KEY': only covers API keys; seed phrase and password not shown; generic. *Fix status:* needs remake, prompt `specs/remake/bp-07-spot-paper-trading__007.txt`.
8. `course/images/bp-07-spot-paper-trading/008.png`: **FAIL** (2/3/3/4/4/-/2). Empty 'PAIR' field with a large stamp: no example pair written, nothing pointing from page to field. *Fix status:* needs remake, prompt `specs/remake/bp-07-spot-paper-trading__008.txt`.
9. `course/images/bp-07-spot-paper-trading/009.png`: **FAIL** (3/3/3/4/2/-/3). Two empty fields: no numbers read from the page. **Hard fail:** illegible label: 'UPPER'/'LOWER' field captions are tiny. *Fix status:* needs remake, prompt `specs/remake/bp-07-spot-paper-trading__009.txt`.
10. `course/images/bp-07-spot-paper-trading/010.png`: **FAIL** (2/3/3/4/3/-/1). Headline 'LINE COUNT' teaches the opposite of the beat. **Hard fail:** wrong label: cards 'GRIDS' and 'LINES' (and a blank third card) - the beat says walk the GAP count, not the line count. *Fix status:* needs remake, prompt `specs/remake/bp-07-spot-paper-trading__010.txt`.
11. `course/images/bp-07-spot-paper-trading/011.png`: **FAIL** (2/3/3/4/4/-/2). CPU-chip tile 'FINISH' beside an empty dashed box with an X: 'read your finish sentence before leaving' is not shown. *Fix status:* needs remake, prompt `specs/remake/bp-07-spot-paper-trading__011.txt`.
12. `course/images/bp-07-spot-paper-trading/012.png`: **FAIL** (1/3/3/4/4/-/1). Open blueprint book tagged 'THEIRS' under headline 'THEIRS': the 'default the form already filled' idea is not shown at all. *Fix status:* needs remake, prompt `specs/remake/bp-07-spot-paper-trading__012.txt`.
13. `course/images/bp-07-spot-paper-trading/013.png`: **FAIL** (3/3/3/4/4/-/3). CPU-style 'CONFIRM' chip wired to a 'STOP' tile: roughly the idea, but chip styling is confusing and 'STOP FIRST' is ambiguous. *Fix status:* needs remake, prompt `specs/remake/bp-07-spot-paper-trading__013.txt`.
14. `course/images/bp-07-spot-paper-trading/014.png`: **FAIL** (2/3/3/4/4/-/2). Five ticks leading into a 'CONFIRM' button: reads as 'tick five then press confirm', the opposite of 'stop before confirm'. *Fix status:* needs remake, prompt `specs/remake/bp-07-spot-paper-trading__014.txt`.
15. `course/images/bp-07-spot-paper-trading/015.png`: **FAIL** (2/3/3/4/4/-/2). Six word chips 'PAPER / PAGE / COUNT / DEFAULT / STOP / SECRET': cryptic recap; no picture. *Fix status:* needs remake, prompt `specs/remake/bp-07-spot-paper-trading__015.txt`.
16. `course/images/bp-07-spot-paper-trading/016.png`: **FAIL** (2/3/3/4/4/-/2). Card with chips 'PRACTICE' and 'NOT AFFILIATED': text card; CPU icon meaningless. *Fix status:* needs remake, prompt `specs/remake/bp-07-spot-paper-trading__016.txt`.
17. `course/images/bp-07-spot-paper-trading/017.png`: **FAIL** (2/3/3/4/3/-/1). Duplicate of 005 with a 'PRACTICE' chip. **Hard fail:** wrong label: field chips again read ...GAPS / LINES instead of gap count + the two sentences. *Fix status:* needs remake, prompt `specs/remake/bp-07-spot-paper-trading__017.txt`.
18. `course/images/bp-07-spot-paper-trading/018.png`: **FAIL** (3/3/3/4/4/-/3). 'SPOT' tile linked to crossed 'CONTRACT' and 'PRACTICE': near-duplicate of 006; leverage not mentioned. *Fix status:* needs remake, prompt `specs/remake/bp-07-spot-paper-trading__018.txt`.
19. `course/images/bp-07-spot-paper-trading/019.png`: **FAIL** (2/3/3/4/2/-/1). 'FIVE LINES' headline does not match the beat (if a label differs, translate it or stop). **Hard fail:** illegible label: tiny field labels; wrong label: list again includes LINES. *Fix status:* needs remake, prompt `specs/remake/bp-07-spot-paper-trading__019.txt`.
20. `course/images/bp-07-spot-paper-trading/020.png`: **FAIL** (2/3/3/4/4/-/2). Arrow into an empty card with a stamp: next lesson ('Managing and monitoring') not named. *Fix status:* needs remake, prompt `specs/remake/bp-07-spot-paper-trading__020.txt`.

## bp-08-managing-and-monitoring: Managing and monitoring (20 images, 0 pass, 20 fail)

1. `course/images/bp-08-managing-and-monitoring/001.png`: **FAIL** (3/3/3/4/4/-/3). Card listing INSIDE / SIDE / SENTENCE with a clock and stamp: closest to the beat, but 'SIDE' and 'SENTENCE' are unexplained single words; 'short list you can finish, not a vigil' only implied. *Fix status:* needs remake, prompt `specs/remake/bp-08-managing-and-monitoring__001.txt`.
2. `course/images/bp-08-managing-and-monitoring/002.png`: **FAIL** (2/2/3/4/3/-/2). Three small chips 'EDUCATION / RISK / EXAMPLE' in an empty frame: not 'Education only. Not financial advice.'; small text. *Fix status:* needs remake, prompt `specs/remake/bp-08-managing-and-monitoring__002.txt`.
3. `course/images/bp-08-managing-and-monitoring/003.png`: **FAIL** (1/2/3/4/3/-/3). Title card: empty glass card with one dash; headline 'MANAGINGMONITORING' drops 'and' and the words run together. *Fix status:* needs remake, prompt `specs/remake/bp-08-managing-and-monitoring__003.txt`.
4. `course/images/bp-08-managing-and-monitoring/004.png`: **FAIL** (3/3/3/4/3/-/3). Three-row card INSIDE / SIDE / SENTENCE with blank lines: the three questions are not written as questions; row labels small. *Fix status:* needs remake, prompt `specs/remake/bp-08-managing-and-monitoring__004.txt`.
5. `course/images/bp-08-managing-and-monitoring/005.png`: **FAIL** (2/3/3/4/3/-/2). 'INSIDE OUT' card with a line crossing it and tiny letter-spaced 'INSIDE'/'OUTSIDE': no band and no path, so 'still crosses the band' is not shown. *Fix status:* needs remake, prompt `specs/remake/bp-08-managing-and-monitoring__005.txt`.
6. `course/images/bp-08-managing-and-monitoring/006.png`: **FAIL** (1/3/2/4/2/-/1). 'WHICH SIDE' with a 'HEAVY' card: which asset you hold more of is not shown; headline words run together. **Hard fail:** artifact: smudged, half-erased pseudo-text above and below 'HEAVY' and 'EXAMPLE' in both cards. *Fix status:* needs remake, prompt `specs/remake/bp-08-managing-and-monitoring__006.txt`.
7. `course/images/bp-08-managing-and-monitoring/007.png`: **FAIL** (1/3/3/4/4/-/1). 'PIN / EDIT' tiles: the beat is 'reread the same finish sentence, don't invent one'; tiles do not show that. Visible seam under the composited headline strip. *Fix status:* needs remake, prompt `specs/remake/bp-08-managing-and-monitoring__007.txt`.
8. `course/images/bp-08-managing-and-monitoring/008.png`: **FAIL** (3/3/3/4/4/-/3). Calendar grid with one highlighted day and 'MONDAY'/'EXAMPLE' tags: readable, but tags float with no arrows and 'reread the same three rows' is not shown. *Fix status:* needs remake, prompt `specs/remake/bp-08-managing-and-monitoring__008.txt`.
9. `course/images/bp-08-managing-and-monitoring/009.png`: **FAIL** (2/2/3/4/3/-/2). Three tiny X boxes over 'NOT THIS': the three things not opened (result chart, ranking, leverage control) are not shown or named; seam under headline strip. *Fix status:* needs remake, prompt `specs/remake/bp-08-managing-and-monitoring__009.txt`.
10. `course/images/bp-08-managing-and-monitoring/010.png`: **FAIL** (1/3/3/4/4/-/1). Tile reading 'IN / BASE / SAME' under 'WORKED CHECK': cryptic; no path that starts inside and ends outside; seam under headline strip. *Fix status:* needs remake, prompt `specs/remake/bp-08-managing-and-monitoring__010.txt`.
11. `course/images/bp-08-managing-and-monitoring/011.png`: **FAIL** (3/3/3/4/4/-/3). Bell with an EXAMPLE card: an alert as a nudge to reread the three rows is not shown; tiny card text. *Fix status:* needs remake, prompt `specs/remake/bp-08-managing-and-monitoring__011.txt`.
12. `course/images/bp-08-managing-and-monitoring/012.png`: **FAIL** (3/4/3/4/4/-/3). Card INSIDE / SIDE / SENTENCE with a crossed 'EXTRA' fourth row: close; but the beat names a RESULT row, and the stamp overlaps the rows; headline words run together ('FOURTHROW'). *Fix status:* needs remake, prompt `specs/remake/bp-08-managing-and-monitoring__012.txt`.
13. `course/images/bp-08-managing-and-monitoring/013.png`: **FAIL** (2/3/3/4/3/-/2). 'DONE' tile with a pencil and tiny EXAMPLE: 'stop or write an edit, don't hover' not shown; seam under headline strip. *Fix status:* needs remake, prompt `specs/remake/bp-08-managing-and-monitoring__013.txt`.
14. `course/images/bp-08-managing-and-monitoring/014.png`: **FAIL** (1/3/3/4/4/-/1). Clipboard with 'EXAMPLE' under 'CLIPPED ON': does not show building a three-row card or running it on a drawn path. *Fix status:* needs remake, prompt `specs/remake/bp-08-managing-and-monitoring__014.txt`.
15. `course/images/bp-08-managing-and-monitoring/015.png`: **FAIL** (2/3/3/4/3/-/2). Six small chips INSIDE / SIDE / SENTENCE / CADENCE / NO RESULT / STOP: word list recap, small type; seam under headline strip. *Fix status:* needs remake, prompt `specs/remake/bp-08-managing-and-monitoring__015.txt`.
16. `course/images/bp-08-managing-and-monitoring/016.png`: **FAIL** (3/3/3/4/3/-/3). Card INSIDE / SIDE / SENTENCE with blank lines: duplicate of 004; small labels. *Fix status:* needs remake, prompt `specs/remake/bp-08-managing-and-monitoring__016.txt`.
17. `course/images/bp-08-managing-and-monitoring/017.png`: **FAIL** (3/3/3/4/3/-/3). Path leaving a two-line band with 'INSIDE'/'OUTSIDE': right idea, but the band is two unlabelled lines, 'INSIDE' sits above the band (outside it), seam under headline strip. *Fix status:* needs remake, prompt `specs/remake/bp-08-managing-and-monitoring__017.txt`.
18. `course/images/bp-08-managing-and-monitoring/018.png`: **FAIL** (2/3/3/4/4/-/2). 'HEAVY / LIGHT' boxes under 'HEAVY BOX': which asset you hold more of is not shown; jargon. *Fix status:* needs remake, prompt `specs/remake/bp-08-managing-and-monitoring__018.txt`.
19. `course/images/bp-08-managing-and-monitoring/019.png`: **FAIL** (2/3/3/4/4/-/2). 'DRAW / crossed LIVE / PAPER' icons under 'TWO SOURCES': the X sits on top of the word 'LIVE' (overlap); paper-screen idea unclear. *Fix status:* needs remake, prompt `specs/remake/bp-08-managing-and-monitoring__019.txt`.
20. `course/images/bp-08-managing-and-monitoring/020.png`: **FAIL** (3/3/3/4/4/-/3). Arrow to 'MISTAKES' tile: next lesson title should read 'Common mistakes'. *Fix status:* needs remake, prompt `specs/remake/bp-08-managing-and-monitoring__020.txt`.

## bp-09-common-mistakes: Common mistakes (21 images, 0 pass, 21 fail)

1. `course/images/bp-09-common-mistakes/001.png`: **FAIL** (2/2/3/4/2/-/2). 'THREE PAGES' headline; 'pages, not personalities' not shown; headline words run together. **Hard fail:** illegible label: 'BLANK / THIN / EARLY' sit on three tiny cards that fill under 5% of the frame. *Fix status:* needs remake, prompt `specs/remake/bp-09-common-mistakes__001.txt`.
2. `course/images/bp-09-common-mistakes/002.png`: **FAIL** (2/3/3/4/4/-/2). Three chips 'EDUCATION / RISK / EXAMPLE': not 'Education only. Not financial advice.'. *Fix status:* needs remake, prompt `specs/remake/bp-09-common-mistakes__002.txt`.
3. `course/images/bp-09-common-mistakes/003.png`: **FAIL** (1/2/3/4/4/-/3). Title card: empty glass card with one dash: glowing rectangle, no subject. *Fix status:* needs remake, prompt `specs/remake/bp-09-common-mistakes__003.txt`.
4. `course/images/bp-09-common-mistakes/004.png`: **FAIL** (2/3/3/4/3/-/2). Small card with an empty oval and a 'FIX' chip: a finish column left blank is not shown; tiny EXAMPLE. *Fix status:* needs remake, prompt `specs/remake/bp-09-common-mistakes__004.txt`.
5. `course/images/bp-09-common-mistakes/005.png`: **FAIL** (2/2/3/4/3/-/2). Tiny 'SHORT -> WIDEN -> WEAVE' net shape in the middle of an empty frame: band vs weave height not shown; small labels. *Fix status:* needs remake, prompt `specs/remake/bp-09-common-mistakes__005.txt`.
6. `course/images/bp-09-common-mistakes/006.png`: **FAIL** (2/2/3/4/3/-/1). Tiny crossed 'EARLY' node on a line to 'SCALE'/'LIQUID' chips: skipping the last two lessons is not readable; mostly empty frame. **Hard fail:** wrong label: 'LIQUID' is a truncated 'liquidation'. *Fix status:* needs remake, prompt `specs/remake/bp-09-common-mistakes__006.txt`.
7. `course/images/bp-09-common-mistakes/007.png`: **FAIL** (1/2/3/4/2/-/1). An oval of tick marks: 'counting lines as gaps' not shown at all. **Hard fail:** illegible label: tiny letter-spaced 'EXAMPLE' and unreadable tick marks. *Fix status:* needs remake, prompt `specs/remake/bp-09-common-mistakes__007.txt`.
8. `course/images/bp-09-common-mistakes/008.png`: **FAIL** (1/2/2/4/2/-/1). 'CLEAR SIZE' headline; 'a default size is the form's idea' not shown. **Hard fail:** artifact: smudged white blur inside the SIZE card where a value should be; illegible label: tiny 'SIZE', 'CLEARED', 'EXAMPLE'. *Fix status:* needs remake, prompt `specs/remake/bp-09-common-mistakes__008.txt`.
9. `course/images/bp-09-common-mistakes/009.png`: **FAIL** (3/2/3/4/3/-/3). Crossed 'GAIN / SURE / WIN' vs 'WAITS / FILLS / STOCK / LEAVES': chips are small in an empty frame; 'STOCK' is unexplained; promise-of-income idea only implied. *Fix status:* needs remake, prompt `specs/remake/bp-09-common-mistakes__009.txt`.
10. `course/images/bp-09-common-mistakes/010.png`: **FAIL** (2/3/3/4/4/-/1). Two circles 'BLANK' and 'GAPS': the worked audit page (blank stop, 10% span on 20 lines) is not shown; no numbers. *Fix status:* needs remake, prompt `specs/remake/bp-09-common-mistakes__010.txt`.
11. `course/images/bp-09-common-mistakes/011.png`: **FAIL** (2/3/3/4/3/-/2). Two cards with an 'O' and 'ONE'/'TWO': 'fix one, reread, fix the next' not shown; tiny captions. *Fix status:* needs remake, prompt `specs/remake/bp-09-common-mistakes__011.txt`.
12. `course/images/bp-09-common-mistakes/012.png`: **FAIL** (1/3/3/4/4/-/1). Card 'PAGE / LINE / STOP' under 'NOT SCORE': no relation to 'the audit does not produce a grade'. *Fix status:* needs remake, prompt `specs/remake/bp-09-common-mistakes__012.txt`.
13. `course/images/bp-09-common-mistakes/013.png`: **FAIL** (3/3/3/4/4/-/3). Glass card 'SPOT' with a crossed '2X': leverage-multiple idea roughly readable; headline 'NO TIMES' is unclear English. *Fix status:* needs remake, prompt `specs/remake/bp-09-common-mistakes__013.txt`.
14. `course/images/bp-09-common-mistakes/014.png`: **FAIL** (2/2/3/4/2/-/2). 'THREE LINES' card: blank stop / tight band / missing 'gaps' word are not named. **Hard fail:** illegible label: 'NONE' chip and three bullet lines are tiny. *Fix status:* needs remake, prompt `specs/remake/bp-09-common-mistakes__014.txt`.
15. `course/images/bp-09-common-mistakes/015.png`: **FAIL** (2/2/3/4/3/-/2). Six small chips BLANK / BAND / EARLY / LINES / SIZE / WORDS: cryptic recap, small type. *Fix status:* needs remake, prompt `specs/remake/bp-09-common-mistakes__015.txt`.
16. `course/images/bp-09-common-mistakes/016.png`: **FAIL** (1/3/3/4/2/-/1). 'COVER NOTES' with a half-white card: does not show 'a blank stop means the finish column was skipped'. **Hard fail:** illegible label: faint 'BLANK' text on a white card band. *Fix status:* needs remake, prompt `specs/remake/bp-09-common-mistakes__016.txt`.
17. `course/images/bp-09-common-mistakes/017.png`: **FAIL** (2/2/3/4/2/-/2). Two bracket shapes: weave not drawn, so 'band shorter than the weave' is not shown. **Hard fail:** illegible label: 'SHORT'/'TALL' captions are tiny. *Fix status:* needs remake, prompt `specs/remake/bp-09-common-mistakes__017.txt`.
18. `course/images/bp-09-common-mistakes/018.png`: **FAIL** (2/3/3/4/4/-/2). Crossed 'EARLY' -> 'MORE' with a stamp: skipping scaling and the opt-in liquidation lesson is not shown. *Fix status:* needs remake, prompt `specs/remake/bp-09-common-mistakes__018.txt`.
19. `course/images/bp-09-common-mistakes/019.png`: **FAIL** (2/2/3/4/2/-/1). A row of tick marks with one circled: lines vs gaps not labelled. **Hard fail:** illegible label: tiny 'ORDERS' and 'EXAMPLE'. *Fix status:* needs remake, prompt `specs/remake/bp-09-common-mistakes__019.txt`.
20. `course/images/bp-09-common-mistakes/020.png`: **FAIL** (3/3/3/4/3/-/3). 'KEPT' vs faded 'FADED' pages: idea readable; marked-up pages not shown; small captions. *Fix status:* needs remake, prompt `specs/remake/bp-09-common-mistakes__020.txt`.
21. `course/images/bp-09-common-mistakes/021.png`: **FAIL** (3/3/3/4/4/-/3). Arrow to 'SCALE' tile: next lesson title is 'Scaling up on spot'; 'SCALE' alone is vague. *Fix status:* needs remake, prompt `specs/remake/bp-09-common-mistakes__021.txt`.

## bp-10-scaling-up: Scaling up on spot (21 images, 0 pass, 21 fail)

1. `course/images/bp-10-scaling-up/001.png`: **FAIL** (3/2/3/4/2/-/3). Two small page outlines: 'a second written page, not a bigger number' only half shown; frame mostly empty. **Hard fail:** illegible label: tiny 'ONE'/'TWO' captions on small page outlines. *Fix status:* needs remake, prompt `specs/remake/bp-10-scaling-up__001.txt`.
2. `course/images/bp-10-scaling-up/002.png`: **FAIL** (2/3/3/4/4/-/2). Three hexagons 'EDUCATION / RISK / EXAMPLE': not 'Education only. Not financial advice.'. *Fix status:* needs remake, prompt `specs/remake/bp-10-scaling-up__002.txt`.
3. `course/images/bp-10-scaling-up/003.png`: **FAIL** (1/2/3/4/4/-/3). Title card: empty glass card with a faint dash; headline 'SCALING UP' drops 'on spot'. *Fix status:* needs remake, prompt `specs/remake/bp-10-scaling-up__003.txt`.
4. `course/images/bp-10-scaling-up/004.png`: **FAIL** (1/3/3/4/3/-/1). 'ONE GATE' with a tile 'DONE / OPEN / DONE': the beat says the second page repeats FIVE gates (regime sort, range, gaps, finish sentence, paper); headline contradicts it. *Fix status:* needs remake, prompt `specs/remake/bp-10-scaling-up__004.txt`.
5. `course/images/bp-10-scaling-up/005.png`: **FAIL** (3/4/3/3/4/-/3). Two overlapping cups 'LEFT/RIGHT' sharing a silver coin-like 'BOTH' token: nearest to the idea, but the silver coin reads as money (coins are banned) and inventory/fighting is not labelled. *Fix status:* needs remake, prompt `specs/remake/bp-10-scaling-up__005.txt`.
6. `course/images/bp-10-scaling-up/006.png`: **FAIL** (2/2/3/4/3/-/2). Word 'KEPT' between two lines with a tiny EXAMPLE: 'keeping the same size is a complete review' not shown. *Fix status:* needs remake, prompt `specs/remake/bp-10-scaling-up__006.txt`.
7. `course/images/bp-10-scaling-up/007.png`: **FAIL** (3/3/3/4/3/-/3). Two lists of four lines with one line tagged 'ONE': idea implied; pages not labelled page one / page two; tiny tag. *Fix status:* needs remake, prompt `specs/remake/bp-10-scaling-up__007.txt`.
8. `course/images/bp-10-scaling-up/008.png`: **FAIL** (2/3/3/4/3/-/2). Two cards 'A'/'B' over two cylinders: same band + different pair label not shown; no band drawn. *Fix status:* needs remake, prompt `specs/remake/bp-10-scaling-up__008.txt`.
9. `course/images/bp-10-scaling-up/009.png`: **FAIL** (2/3/3/4/3/-/2). 'SCALE -> OPTIONAL' chips under 'ONE MORE': 'scaling is not the end of the course' only implied; small chips. *Fix status:* needs remake, prompt `specs/remake/bp-10-scaling-up__009.txt`.
10. `course/images/bp-10-scaling-up/010.png`: **FAIL** (2/3/3/4/4/-/2). Card 'SPOT' with an X button under it: reads as 'no spot', the opposite of 'the second page is still spot'. *Fix status:* needs remake, prompt `specs/remake/bp-10-scaling-up__010.txt`.
11. `course/images/bp-10-scaling-up/011.png`: **FAIL** (2/2/3/4/2/-/2). 'LEFT OPEN': 'the page does not tell you how much money to assign' not shown. **Hard fail:** illegible label: tiny 'NOT THIS' in a near-empty card. *Fix status:* needs remake, prompt `specs/remake/bp-10-scaling-up__011.txt`.
12. `course/images/bp-10-scaling-up/012.png`: **FAIL** (2/2/3/4/3/-/2). 'TWO TWO' chips over a crossed 'FELT': doubling a count because it felt fine is not readable. *Fix status:* needs remake, prompt `specs/remake/bp-10-scaling-up__012.txt`.
13. `course/images/bp-10-scaling-up/013.png`: **FAIL** (2/3/3/4/4/-/2). Two identical dotted lines labelled 'SAME' under 'SAME PATH': correlated pairs filling at the same time not shown (no prices, no fills). *Fix status:* needs remake, prompt `specs/remake/bp-10-scaling-up__013.txt`.
14. `course/images/bp-10-scaling-up/014.png`: **FAIL** (3/3/3/4/4/-/4). Card reads 'PAGE TWO, SAME GATES, OR NONE.': text-only card (no picture), but accurate; still a word card, not a diagram. *Fix status:* needs remake, prompt `specs/remake/bp-10-scaling-up__014.txt`.
15. `course/images/bp-10-scaling-up/015.png`: **FAIL** (2/2/3/4/3/-/2). Six small hexagons PAGE / GATES / BUCKETS / CHANGE / SPOT / SIZE plus an 'OPTIONAL' arrow: cryptic recap, small type. *Fix status:* needs remake, prompt `specs/remake/bp-10-scaling-up__015.txt`.
16. `course/images/bp-10-scaling-up/016.png`: **FAIL** (1/3/3/4/4/-/1). Row DONE DONE OPEN DONE DONE under 'ONE OPEN': the five gates are not named; meaning unrecoverable. *Fix status:* needs remake, prompt `specs/remake/bp-10-scaling-up__016.txt`.
17. `course/images/bp-10-scaling-up/017.png`: **FAIL** (2/3/3/3/4/-/2). Two stacked cups with a 'BOTH' coin token: 'two grids on one asset can fight if they share inventory' not readable; coin-like token. *Fix status:* needs remake, prompt `specs/remake/bp-10-scaling-up__017.txt`.
18. `course/images/bp-10-scaling-up/018.png`: **FAIL** (1/2/3/4/2/-/1). 'SIZE KEPT': nothing shows a review keeping size the same. **Hard fail:** illegible label: tiny 'KEPT' in a tall empty card. *Fix status:* needs remake, prompt `specs/remake/bp-10-scaling-up__018.txt`.
19. `course/images/bp-10-scaling-up/019.png`: **FAIL** (2/3/3/4/3/-/2). Two cards with lines, one tagged 'ONE': duplicate of 007; headline 'ONE WORD' mislabels the beat (one change). *Fix status:* needs remake, prompt `specs/remake/bp-10-scaling-up__019.txt`.
20. `course/images/bp-10-scaling-up/020.png`: **FAIL** (3/3/3/4/3/-/3). Folders 'READY' and 'NOT READY': close to 'file both only if both passed', but it shows one ready and one not, the opposite of filing them together. *Fix status:* needs remake, prompt `specs/remake/bp-10-scaling-up__020.txt`.
21. `course/images/bp-10-scaling-up/021.png`: **FAIL** (2/2/3/4/3/-/2). Empty card with an arrow 'OPTIONAL' under 'CAN SKIP': next lesson ('Advanced: liquidation scenarios') not named. *Fix status:* needs remake, prompt `specs/remake/bp-10-scaling-up__021.txt`.

## bp-11-advanced-liquidation: Advanced: liquidation scenarios (20 images, 0 pass, 20 fail)

1. `course/images/bp-11-advanced-liquidation/001.png`: **FAIL** (2/3/3/4/3/-/2). 'OPT IN -> CLOSED' chips under 'LOSS FIRST': no losing path drawn; 'this lesson is opt-in, the losing path comes first' not readable; tiny EXAMPLE. *Fix status:* needs remake, prompt `specs/remake/bp-11-advanced-liquidation__001.txt`.
2. `course/images/bp-11-advanced-liquidation/002.png`: **FAIL** (2/3/3/4/3/-/2). Three small chips 'EDUCATION / RISK / EXAMPLE' in a diagonal: not 'Education only. Not financial advice.'. *Fix status:* needs remake, prompt `specs/remake/bp-11-advanced-liquidation__002.txt`.
3. `course/images/bp-11-advanced-liquidation/003.png`: **FAIL** (1/2/3/4/4/-/3). Title card: empty glass card with a dash and a dot; headline 'LIQUIDATION SCENES' misnames the lesson ('Advanced: liquidation scenarios'). *Fix status:* needs remake, prompt `specs/remake/bp-11-advanced-liquidation__003.txt`.
4. `course/images/bp-11-advanced-liquidation/004.png`: **FAIL** (2/3/3/4/3/-/2). Stack of pages 'SPOT' and a door 'SIDE' under 'SIDE DOOR': 'the spot path is already complete without this lesson' not readable. *Fix status:* needs remake, prompt `specs/remake/bp-11-advanced-liquidation__004.txt`.
5. `course/images/bp-11-advanced-liquidation/005.png`: **FAIL** (2/3/3/4/4/-/2). Closed box 'CLOSED' and open box 'MARGIN' under 'MARGIN GONE': liquidation (margin no longer covers the loss, position closed) is not shown; no loss, no price. *Fix status:* needs remake, prompt `specs/remake/bp-11-advanced-liquidation__005.txt`.
6. `course/images/bp-11-advanced-liquidation/006.png`: **FAIL** (1/2/3/4/2/-/1). Three tiny line-art panels (line, rectangle, X) under 'PATH ORDER': price leaving the band and the position closing are not drawn. **Hard fail:** illegible label: tiny '1'/'2' panel numbers. *Fix status:* needs remake, prompt `specs/remake/bp-11-advanced-liquidation__006.txt`.
7. `course/images/bp-11-advanced-liquidation/007.png`: **FAIL** (2/2/3/4/2/-/2). Dashed box around one of three squares: isolated margin readable only by an expert; frame mostly empty. **Hard fail:** illegible label: tiny 'ISOLATED' and 'ASSIGNED' captions. *Fix status:* needs remake, prompt `specs/remake/bp-11-advanced-liquidation__007.txt`.
8. `course/images/bp-11-advanced-liquidation/008.png`: **FAIL** (2/3/3/4/4/-/2). 'MARGIN -> PULL' boxes under 'CAN PULL': cross margin (venue may look at other balances in the account) not shown; no other balances drawn. *Fix status:* needs remake, prompt `specs/remake/bp-11-advanced-liquidation__008.txt`.
9. `course/images/bp-11-advanced-liquidation/009.png`: **FAIL** (2/3/3/4/4/-/2). Two 'no' symbols 'NONE / NONE' under 'NO TIMES': the two boxes (isolated, cross) are not named; 'NO TIMES' is unclear English for 'no leverage multiple'. *Fix status:* needs remake, prompt `specs/remake/bp-11-advanced-liquidation__009.txt`.
10. `course/images/bp-11-advanced-liquidation/010.png`: **FAIL** (1/3/3/4/2/-/1). Oval with a two-way arrow under 'NO RATE': a timed funding payment between sides is not shown. **Hard fail:** illegible label: tiny letter-spaced 'FUNDING'. *Fix status:* needs remake, prompt `specs/remake/bp-11-advanced-liquidation__010.txt`.
11. `course/images/bp-11-advanced-liquidation/011.png`: **FAIL** (1/3/3/4/4/-/1). Crossed symbol and a 'NONE' tile under 'OLD NOTES': deleted older drafts with leverage multiples are not shown. *Fix status:* needs remake, prompt `specs/remake/bp-11-advanced-liquidation__011.txt`.
12. `course/images/bp-11-advanced-liquidation/012.png`: **FAIL** (2/3/3/4/4/-/1). The two flags ('this can liquidate', 'you can lose all the money assigned') are not written. **Hard fail:** wrong count: headline 'TWO FLAGS' over three flags (LOSS / ALL / crossed GAIN). *Fix status:* needs remake, prompt `specs/remake/bp-11-advanced-liquidation__012.txt`.
13. `course/images/bp-11-advanced-liquidation/013.png`: **FAIL** (3/3/3/4/3/-/3). Crossed monitor 'NO SCREEN' under 'PAPER ONLY': close to 'not a venue guide / no live contract screen'; small caption. *Fix status:* needs remake, prompt `specs/remake/bp-11-advanced-liquidation__013.txt`.
14. `course/images/bp-11-advanced-liquidation/014.png`: **FAIL** (3/4/3/4/4/-/3). Checklist 'NO TIMES / LOSS FIRST' under 'TWO CHECKS': close to the sentence, but 'NO TIMES' is unclear English and 'explain isolated and cross' is missing. *Fix status:* needs remake, prompt `specs/remake/bp-11-advanced-liquidation__014.txt`.
15. `course/images/bp-11-advanced-liquidation/015.png`: **FAIL** (1/2/3/4/1/-/2). Recap unreadable at lesson size. **Hard fail:** illegible label: eight tiny chips (OPT / LOSS / FENCE / PULL / NONE / RATE / SPOT / LAST) across a thin strip. *Fix status:* needs remake, prompt `specs/remake/bp-11-advanced-liquidation__015.txt`.
16. `course/images/bp-11-advanced-liquidation/016.png`: **FAIL** (2/3/3/4/3/-/2). Book 'SPOT' and door 'SIDE' under 'BOOK DONE': near-duplicate of 004; 'spot path complete' only implied. *Fix status:* needs remake, prompt `specs/remake/bp-11-advanced-liquidation__016.txt`.
17. `course/images/bp-11-advanced-liquidation/017.png`: **FAIL** (2/3/3/4/3/-/2). Boxes 'CLOSED' lid and 'MARGIN' under 'LID DOWN': duplicate metaphor of 005; liquidation not shown. *Fix status:* needs remake, prompt `specs/remake/bp-11-advanced-liquidation__017.txt`.
18. `course/images/bp-11-advanced-liquidation/018.png`: **FAIL** (1/2/3/4/2/-/1). Duplicate of 006: band, price leaving it and position closed not drawn. **Hard fail:** illegible label: tiny '1'/'2' numbers in line-art panels. *Fix status:* needs remake, prompt `specs/remake/bp-11-advanced-liquidation__018.txt`.
19. `course/images/bp-11-advanced-liquidation/019.png`: **FAIL** (3/4/3/4/4/-/3). Card 'OPT IN' with a 'SKIPPED' stamp: close, but the instruction is to write 'Skipped on purpose' on the spot notebook; headline 'SKIPPED ON' is a truncated phrase. *Fix status:* needs remake, prompt `specs/remake/bp-11-advanced-liquidation__019.txt`.
20. `course/images/bp-11-advanced-liquidation/020.png`: **FAIL** (3/3/3/4/3/-/3). Three 'SPOT' dots and an 'OPT IN' tile under 'SPOT STANDS': readable-ish; last-lesson / keep-the-pages message missing; tiny dot labels. *Fix status:* needs remake, prompt `specs/remake/bp-11-advanced-liquidation__020.txt`.

## Next

- Remake queue: `blueprint-image-qa/bp04-11/REMAKE_QUEUE.json` (161 items, in lesson order). Prompts are in `specs/remake/<lesson>__<NNN>.txt` on the box, with a copy in `blueprint-image-qa/bp04-11/remake/`.
- Each prompt carries the 3:2 1536x1024 preamble, attaches `_anchors/anchor.png`, sets margins of at least 80px, spells out every label, pins each arrow to its target, and bans any robot or mascot (no BP-04..11 beat calls for the mascot). It stays exchange-neutral, stamps EXAMPLE on figures, and uses the lesson's real titles.
- Figures come only from the lesson scripts' own house example (bp-05: 20 lines, 19 gaps, 0.5%, 9.5%, 38 not 40; bp-09 beat 10). No BP-04..11 beat uses market data, so `btc-usd-windows.json` isn't needed.

## BP-04 remakes, round 1 (web1, scored against PR #17 6848d09)

The 10 ChatGPT web renders at `gen/bp-04-market-regimes/001..010/web1.png` are all 1536x1024 RGB. Each was scored against the 6848d09 narration and the prompt at this commit, using the same strict standard: at least 4 in every category, no hard fails, and margins of at least 45px measured on bright pixels. None has an exchange name, mascot or entity branding.

| Beat | Result | Reason |
|---|---|---|
| 001 | PASS | Same 5-line ladder on both cards: the weave crosses the rungs (check), the climb leaves the top (warning). Tags spelled right, EXAMPLE inside the card. Margins 81-177px. |
| 002 | FAIL (re-run anyway) | Made from the superseded prompt: "Learn the idea" / "Not financial advice" tags and a crossed BUY button, not the exact "Education only. Not financial advice." |
| 003 | FAIL | The trend line ends in a garbled cross/tick stub (AI artifact). The EXAMPLE stamp floats outside every card. Prompt is now v2. |
| 004 | PASS | Range, Trend and Break cards with correct tags and an EXAMPLE stamp in each card. Margins 55px or more. |
| 005 | FAIL | Step 2 ("Then set your steps") shows a price path breaking up out of the ladder, so it teaches a breakout, not setting steps. The bottom rung is slanted. Prompt is now v2. |
| 006 | FAIL | Crossings on the second line have no dot, which contradicts "Each dot = an order filling". The narration asks for three rungs and the image has five. Prompt is now v2. |
| 007 | PASS | Higher highs, small dips and the slope arrow each have one arrow, tips on target, 3 of 3. |
| 008 | PASS | "Your box" tip is on the top dashed line, the exit tip is on the amber ring, 2 of 2. Price leaves and stays out. |
| 009 | PASS | Dotted left-to-right arrow and an empty name tag, 2 of 2 tips on target. |
| 010 | FAIL | Shows a two-way choice, but the beat says copy three arrows (Ladder, Pile, Stop). The right tag sits 40px from the edge (needs 45). Prompt is rewritten as v2. |

The passes were saved to `out/course/images/bp-04-market-regimes/NNN.png` and committed at `course/images/bp-04-market-regimes/NNN.png`. They needed no navy fill because they were already 1536x1024. Their pass-list rows now carry the scores, `pass: true`, `source: chatgpt-web`, `scored_blob` and the previous blob. Fails keep the old committed still, carry a `remake_review` block, and stay in REMAKE_QUEUE (their target is now web2).

**BP-04 running count: 5/20 pass.** BP-04..11 total: 5/161.

## BP-04 remakes, round 2 (5 re-runs + 011..020 web1, scored against PR #17 6848d09)

All 15 files are 1536x1024 RGB from ChatGPT web, scored against the 6848d09 narration and the prompt at this commit with the same strict standard (at least 4 in every category, no hard fails, margins of at least 45px on bright pixels, text zoomed for spelling, arrow targets and counts checked). None has an exchange name, mascot, robot or entity branding. Margins are left/right/top/bottom in px.

| File | Result | Margins | Reason |
|---|---|---|---|
| gen/bp-04-market-regimes/002/web2.png | PASS | 75/78/74/236 | Disclaimer card on the current prompt: exactly "Education only." / "Not financial advice." in two large white lines, notebook with pencil and check on the left, no buy button or extra icons. Headline EDUCATION ONLY. 0 arrows. Matches 6848d09 beat 2. |
| gen/bp-04-market-regimes/003/web2.png | PASS | 70/69/111/238 | Title card MARKET REGIMES with three equal cards: zig-zag between two lines (Range), clean staircase ending inside its card with no stray stub (Trend), bounce then drop through the bottom line staying below (Break). Tags under each card, no arrows; EXAMPLE stamp inside the Break card. v1 artifact fixed. |
| gen/bp-04-market-regimes/005/web2.png | PASS | 69/72/104/166 | Step 1: magnifier over a zig-zag between two lines; cyan arrow to step 2: four parallel even cyan lines with a blue pencil drawing the fifth. No price path or breakout in step 2. Tags "1 Look at the shape" / "2 Then set your steps" spelled right; straight EXAMPLE stamp inside the step 1 card. v1 fault fixed. |
| gen/bp-04-market-regimes/006/web2.png | FAIL | 74/77/78/163 | Three rungs and four peaks, both arrow tips on dotted crossings, EXAMPLE inside the card, spelling right. But after the fourth peak the line comes down, crosses the middle rung with no dot and fades out in a stub below it, so one crossing is undotted (the exact fault the v2 prompt banned) and the path has no clean end. Hard fail: label/count mismatch: the last down-stroke crosses the middle rung with no dot, contradicting "Each dot = an order filling"; AI artifact: price line runs past its last dot and fades out in a stub below the middle rung. Next: web3.png on the v3 prompt (old prompt in specs/remake/_superseded/bp-04-market-regimes__006.v2.txt). |
| gen/bp-04-market-regimes/010/web2.png | PASS | 78/110/68/121 | Three chart cards (Range weave, Trend staircase, Break drop) with tags under each, three thick down arrows to Ladder, Pile (three plain glass discs) and Stop (amber line with a note card). EXAMPLE inside the Break card. Exactly three arrows; side margins 78/110px; tags well inside 100px. Matches 6848d09 beat 10 "three arrows from the three shapes to Ladder, Pile, and Stop". Small kink in the Range weave, not distracting. |
| gen/bp-04-market-regimes/011/web1.png | PASS | 71/114/78/182 | Glass chart with a small even wiggle and a bracket measuring its height; "Usual up-and-down size" arrow points at the bracket (tip about 12px right of the bracket spine, single unambiguous target); "Not a promise about tomorrow" in the card, no arrow; EXAMPLE stamp inside the card. Matches the current prompt and the "not a promise about tomorrow" line of 6848d09 beat 11. |
| gen/bp-04-market-regimes/012/web1.png | FAIL | 53/51/87/185 | Left card: calm wiggle, tall news bar beside a newspaper icon, amber warning, "News bar" tip on the bar. Right card: five rungs, two tickets far apart, price leaps across the empty rungs, amber warning, EXAMPLE stamp. But the "Thin book: few resting orders" arrow ends in the gap between the 2nd and 3rd rungs (about 15px above the 3rd), touching no rung, so it does not point at the empty rungs it names. Hard fail: label arrow misses its target: "Thin book: few resting orders" tip stops in the empty space between two rungs. Next: web2.png on the v2 prompt (old prompt in specs/remake/_superseded/bp-04-market-regimes__012.v1.txt). |
| gen/bp-04-market-regimes/013/web1.png | PASS | 62/62/123/182 | Two rows: "Wrong: grid first" with an amber X, ladder then chart; "Right: look at the shape first" with a check, chart then ladder. Small arrows show the order. Headline SHAPE FIRST, GRID SECOND. Matches the current prompt and 6848d09 beat 13 (the miss is grid first, regime second). |
| gen/bp-04-market-regimes/014/web1.png | PASS | 65/69/98/234 | Small chart in a card with a blank name tag beside it (the place to write the name), arrow to a ladder with a question mark. "Name the shape" tip on the name tag, "Then decide if a grid fits" tip on the ladder icon (2 of 2). Reads left to right: name it, then decide. |
| gen/bp-04-market-regimes/015/web1.png | PASS | 98/198/107/179 | Notebook page: sketched zig-zag between dashed lines, three tick boxes with tiny range/staircase/drop icons, the range box ticked by a pencil; "Pick one shape" tip on the ticked box; "Write one reason why" arrow points at the blank reason line (tip about 13px short, single unambiguous target); EXAMPLE stamp. Matches 6848d09 beat 15 (sort one path, write one reason). |
| gen/bp-04-market-regimes/016/web1.png | PASS | 101/237/95/147 | Frosted pale-blue notebook page with three pencil sketches: zig-zag in a box, staircase, line breaking out of the bottom of its box. "Range", "Trend", "Break" tips each on their sketch (3 of 3). Matches 6848d09 beat 16 (three panels labelled Range, Trend, Break). Paler page than the glass cards, still navy/cyan framed. |
| gen/bp-04-market-regimes/017/web1.png | PASS | 78/195/76/119 | Notebook page: (1) a circled chart sketch, (2) a sketched ladder of five lines, pencil below; tags "1 Name the shape" and "2 Then draw steps" under each, no arrows. Shape before steps is clear. Margins 76px or more. |
| gen/bp-04-market-regimes/018/web1.png | FAIL | 65/43/73/94 | Zig-zag across three lines with circles on most crossings, "Circle each crossing" tip on a circle, "More crossings = better fit" under the sketch, EXAMPLE stamp. But the line keeps climbing after its last circle and crosses the top line at the right with no circle, and the pencil sits off the page edge (not circling anything) with its eraser 43px from the right frame edge. Hard fail: label/count mismatch: the zig-zag crosses the top line at the right end with no circle, contradicting "Circle each crossing"; cramped margin: pencil eraser 43px from the right edge. Next: web2.png on the v2 prompt (old prompt in specs/remake/_superseded/bp-04-market-regimes__018.v1.txt). |
| gen/bp-04-market-regimes/019/web1.png | PASS | 59/54/74/112 | Traffic light with every lamp dark and an amber X over it, beside a notebook with a check. "No 'go' signal" tip on the light, "You decide on paper" tip on the notebook (2 of 2). Matches the prompt and the 6848d09 beat 19 idea (no score or signal that says go). |
| gen/bp-04-market-regimes/020/web1.png | PASS | 75/74/103/193 | Outro: finished notebook with a check, glowing arrow to a card with an evenly lined box and a ruler. "Bring your notes" tip on the notebook; "Next lesson: Choosing grid spacing and range" under the card, the exact next lesson title in 6848d09 beat 20. |

Arrow rule used: a tip that lands on its target, or points at a single unambiguous target with a small gap (011 bracket, 015 reason line, about 12-13px), scores 4 on label accuracy. A tip that ends in the gap between two rungs touches nothing and could mean either, so it fails (012, and bp-01 007).

Passes were saved to `out/course/images/bp-04-market-regimes/NNN.png` (already 1536x1024, no navy fill needed) and committed at `course/images/bp-04-market-regimes/NNN.png`; their rows carry `source: chatgpt-web`, scores, `scored_blob` and the previous blob, with the earlier web1 review kept in `previous_remake_reviews`. Fails keep the old committed still and stay in REMAKE_QUEUE: 006 -> web3 (v3 prompt), 012 -> web2 (v2), 018 -> web2 (v2). Old prompts are in `specs/remake/_superseded/` and `remake/_superseded/`.

**BP-04 running count: 17/20 pass. Not 100%: 006, 012 and 018 are left.** BP-04..11 total: 17/161. Queue: 144.

## Strict arrow re-check (14 Nov): a tip must touch its target

Stewart's rule for the perfect run is that every label arrow's point must touch the thing it names. A gap of a few pixels fails with "arrow tip stops short of target". This replaces the round-2 tolerance above (small gap allowed when the target is unambiguous). I zoomed (4-8x) into every label-arrow tip on all 17 passed BP-04 rows: 001-005, 010, 013 and 017 have no label arrows. The 010 column arrows and the 005/014/020 between-panel arrows are sequence connectors, not label arrows.

Flipped back to fail. The previous committed still is restored at `course/images/bp-04-market-regimes/NNN.png`, the `out/` file is removed (BP-04 convention: failing rows have no `out/` file), the passed render is kept in `remake_review` / `flipped_from_pass`, and the row is back in REMAKE_QUEUE on a v2 prompt that pins each tip (v1 moved to `_superseded/`):

| Row | Arrow that misses | Next |
|---|---|---|
| 007 | "Small dips" tip stops about 25px above the dip; "Keeps going one way" tip stops about 17px below the dashed slope arrow | web2, v2 |
| 009 | "Follow the line left to right" tip stops about 12px below the dotted arrow | web2, v2 |
| 011 | "Usual up-and-down size" tip stops about 12px right of the bracket | web2, v2 |
| 015 | "Write one reason why" tip stops about 13px short of (and above) the blank reason line | web2, v2 |

Checked and touching: 007 "Higher highs", 008 both, 009 "Give it one name", 014 both, 016 Range/Trend/Break, 019 both, 020 "Bring your notes".

**BP-04 running count: 13/20 pass. Not 100%. Left: 006 (web3, v3), 007, 009, 011, 012, 015, 018 (web2, v2).** BP-04..11 total: 13/161. Queue: 148.

---

## Run on top of 8f21533 — BP-04 010 flip + BP-05 web1 scoring

**BP-04 010 flipped to FAIL (panel-connector arrow rule).** The three column arrows (Range->Ladder, Trend->Pile, Break->Stop) stop 20-40px above their icons and float. Restored the original committed still (blob 100ad315); out/ copy absent; v3 prompt pins each arrowhead to touch its icon; queued at web3. **BP-04: 12/20 — NOT 100%.** Rows left: 006, 007, 009, 010, 011, 012, 015, 018.

### BP-05 spacing-and-range — web1 renders scored (14 pass / 5 fail)
PASS (placed, chatgpt-web): 001, 002, 003, 004, 007, 008, 009, 010, 011, 012, 013, 014, 017, 018.
- Number checks verified: 004 = 20 lines / 19 gaps (peak count 20); 010 = "20 lines x 0.5% = 10%" (wrong, X) vs "19 gaps x 0.5% = 9.5%" (right, check); 013/014/017/018 all show 19 gaps / 0.5% / 9.5% correctly. All arrow tips (incl. panel connectors) verified to touch.

FAIL (v2 prompt written, v1 superseded, queued at web2):
- **005** — misspelling "Eacn gap" (should be "Each gap"); 0.5%/9.5%/19 values were otherwise correct.
- **006** — unexplained big numerals "5" and "9" inside the boxes; 9 is not double 5, so it doesn't illustrate "DOUBLE THE LINES" (beginner-confusing). "Recount: 38 gaps, not 40" was correct.
- **015** — only FOUR recap chips; beat 15 calls for FIVE (missing the "19 gaps = 9.5%" house-example chip).
- **016** — only ~12 ladder lines, not the TWENTY lines / nineteen gaps the beat requires.
- **019** — next->card transition arrowhead stops ~25px short of the card (tip x=761, card border x=786); panel-connector fail. Outro text "Entry and exit rules" correct.

**BP-05: 14/19 — NOT 100%.** Rows left: 005, 006, 015, 016, 019.

---

## Run on top of 57e0aeb — 14 Nov 2026 (WITA): BP-04 remakes + BP-06 first scoring

Same perfect-run rules (every category at least 4/5, no hard fails; every arrow tip, including panel connectors, must visibly touch its target; doubt = fail). BP-04 renders used the prompts current when the batch started and were scored on merits. BP-06 is first scoring of the 20 web.png stills (beats inventoried from course/scripts/bp-06-entry-and-exit.json). Did not touch gen/bp-04-*/010, gen/bp-05-*, or gen/bp-07-*.

### BP-04 market-regimes remakes

| File | Result | Margins (l/r/t/b) | Reason |
|---|---|---|---|
| gen/bp-04-market-regimes/006/web3.png | FAIL | 79/80/79/161 | Crossing-count / stub faults from v2 look fixed, but "Each dot = an order filling" tip stops clearly short of the glowing dot. Next: web4.png on the v4 prompt. |
| gen/bp-04-market-regimes/007/web2.png | FAIL | 77/76/70/143 | "Higher highs" and "Small dips" appear to touch, but "Keeps going one way" tip has a visible sliver of navy under the dashed slope arrow. Next: web3.png on the v3 prompt. |
| gen/bp-04-market-regimes/009/web2.png | PASS | 80/82/117/154 | "Give it one name" tip on the empty tag-box edge; "Follow the line left to right" tip against the white dotted arrow. EXAMPLE present. Placed. |
| gen/bp-04-market-regimes/011/web2.png | FAIL | 84/89/99/189 | Teaching and EXAMPLE otherwise excellent, but "Usual up-and-down size" tip stops about 4-8px short of the bracket's top cap. Next: web3.png on the v3 prompt. |
| gen/bp-04-market-regimes/012/web2.png | PASS | 59/57/93/110 | "News bar" tip on the tall bar; "Thin book…" tip ON an empty rung (v1 gap-between-rungs fixed). EXAMPLE present. Placed. |
| gen/bp-04-market-regimes/015/web2.png | FAIL | 86/199/77/125 | "Pick one shape" touches the ticked box, but "Write one reason why" tip stops about 8-15px short of the blank pencil line. Next: web3.png on the v3 prompt. |
| gen/bp-04-market-regimes/018/web2.png | PASS | 92/130/90/152 | Every crossing circled; path starts and ends on the bottom line; pencil fully inside; "Circle each crossing" tip on a circle. Previous uncircled-right-crossing and 43px-pencil faults look fixed. Placed. |

010 was not in this batch and stays queued at web3 (another job is writing it).

**BP-04: 15/20 — NOT 100%.** Rows left: 006 (gen/bp-04-market-regimes/006/web4.png), 007 (gen/bp-04-market-regimes/007/web3.png), 011 (gen/bp-04-market-regimes/011/web3.png), 015 (gen/bp-04-market-regimes/015/web3.png), 010 (gen/bp-04-market-regimes/010/web3.png).

### BP-05 spacing-and-range — unchanged this run
**BP-05: 14/19 — NOT 100%.** Rows left: 005 (gen/bp-05-spacing-and-range/005/web2.png), 006 (gen/bp-05-spacing-and-range/006/web2.png), 015 (gen/bp-05-spacing-and-range/015/web2.png), 016 (gen/bp-05-spacing-and-range/016/web2.png), 019 (gen/bp-05-spacing-and-range/019/web2.png).

### BP-06 entry-and-exit — first scoring of web.png (20 beats)

PASS (placed, chatgpt-web): 001, 002, 003, 004, 005, 007, 008, 009, 011, 013, 015, 017.
FAIL (v2 prompt written, v1 superseded, queued at web2): 006, 010, 012, 014, 016, 018, 019, 020.

Per-image:
- **001 PASS** — doorway / X metaphor; "Way in" on the entrance-arrow shaft; "No way out…" on the amber X.
- **002 PASS** — exact disclaimer "Education only. Not financial advice."; headline EDUCATION ONLY.
- **003 PASS** — title ENTRY AND EXIT RULES; flag and stop; labels under, no arrows.
- **004 PASS** — two columns "Before I start" / "What ends it"; 0 arrows; no digits.
- **005 PASS** — stop column is 1 (pencil), start is 2; EXAMPLE present. Left-to-right shows 2 then 1, but the numbers make the order clear (clarity 4).
- **006 FAIL** — both "Price leaves the box" and "Still out at next check = stop" tips stop short of their targets. Path/EXAMPLE otherwise good.
- **007 PASS** — three checks; sideways, counts, and gap-bracket tips all touch. The "000" mark is a counter icon (prompt has no FIGURES/EXAMPLE line).
- **008 PASS** — "Read the rule" on the sentence line; "Point at the matching drawing" on the exit stroke at the box crossing.
- **009 PASS** — hope star with an X vs a written rule; 0 arrows.
- **010 FAIL** — "Finish path (invalidation)…" tip stops about 6-8px short of the dashed amber line. "Price leaves the box" touches.
- **011 PASS** — "I'LL JUST KNOW ISN'T A STOP" with space; feeling vs written rule; 0 arrows.
- **012 FAIL** — numbered scene connector 1 stops short of the stop row; connector 2 stops short of the start row; "2 Then start rule" tip stops short of the circled 2.
- **013 PASS** — amount box empty ("Not part of this lesson."); tip sits inside the dashed box (treated as touching the box).
- **014 FAIL** — cramped right margin 43px on the "Read them aloud" tag (x=1492). The three arrows themselves looked like they touched.
- **015 PASS** — four recap icons; EXAMPLE with the "1"; 0 arrows.
- **016 FAIL** — "Before I start" tip stops short of the flagpole (~8-15px). "What ends it" appears to touch the stop icon.
- **017 PASS** — "Write this side first" tip sits inside the highlighted right (stop-rule) column.
- **018 FAIL** — "Doesn't come back" tip stops about 4-8px short of the far right end of the line. "Price leaves" sits on the box-exit crossing.
- **019 FAIL** — cramped left margin 8px (left sleeve/cuff glow at x=8). Two outline hands are allowed by the prompt; not a character fail.
- **020 FAIL** — notebook-to-laptop panel-connector arrow floats well short of the laptop (large gap). "Bring your notes" touches the notebook. Outro title is exact: "Next lesson: Spot paper trading". Examples marked Example.

**BP-06: 12/20 — NOT 100%.** Rows left: 006 (gen/bp-06-entry-and-exit/006/web2.png), 010 (gen/bp-06-entry-and-exit/010/web2.png), 012 (gen/bp-06-entry-and-exit/012/web2.png), 014 (gen/bp-06-entry-and-exit/014/web2.png), 016 (gen/bp-06-entry-and-exit/016/web2.png), 018 (gen/bp-06-entry-and-exit/018/web2.png), 019 (gen/bp-06-entry-and-exit/019/web2.png), 020 (gen/bp-06-entry-and-exit/020/web2.png).

Updated ChatGPT queue (BP-04..11): 120 items.


---

## Run on top of 4bfe3e6 — 14 Nov 2026 (WITA): remake scoring for BP-04 010, BP-05 005/006/015/016/019, and first scoring of all 20 BP-07 stills

Same perfect-run rules (every category at least 4/5, no hard fails; every arrow tip, panel connectors included, must visibly touch its target; doubt = fail). These renders used the prompts current when the batch started and were scored on their own merits against the beat. Mismatch check: every image in this batch depicts its own prompt and beat (no tab-order swaps).

### BP-04 010 / BP-05 remakes

| File | Result | Margins (l/r/t/b) | Reason |
|---|---|---|---|
| gen/bp-04-market-regimes/010/web3.png | PASS | 80/98/78/97 | All three column arrows now touch (Range->Ladder on the top rung, Trend->Pile on the top disc, Break->Stop on the amber line). Headline spaced; EXAMPLE on the Break card. Placed at out/ and course/images/bp-04-market-regimes/010.png (`source: chatgpt-web`, scored_blob 9ad06527943e4ebb5169b1b44645beac82b2c98f). Removed from the queue. |
| gen/bp-05-spacing-and-range/005/web2.png | PASS | 82/82/81/170 | 'Each gap: 0.5%' spelled correctly (v1 was 'Eacn gap'). 19 bars; 0.5% / 9.5% / 19 correct; all three tips touch; EXAMPLE present. Placed (`scored_blob` ff2a27d9f6331b3b57fb421a56be3e9a69b5271e). Removed from the queue. |
| gen/bp-05-spacing-and-range/006/web2.png | FAIL | 80/58/73/77 | Left box has 6 interior lines, but the right box has 11, not the required 12 (double). Does not illustrate DOUBLE THE LINES. Both label arrows touch; unexplained 5/9 numerals are gone. Next: web3.png on the v3 prompt (v2 superseded). |
| gen/bp-05-spacing-and-range/015/web2.png | FAIL | 75/39/116/320 | All five recap chips are present, including the previously missing '19 gaps = 9.5%'. Hard fail: cramped right margin 39px on the 'One change at a time' tag (x=1496). Next: web3.png on the v3 prompt (v2 superseded). |
| gen/bp-05-spacing-and-range/016/web2.png | PASS | 76/70/70/93 | 20 dark lines and 19 green gap ticks. 'Count the lines' tip on the top line; 'Gaps = lines minus 1' tip on a green check. EXAMPLE present. Placed (`scored_blob` 616de7eae6a164f4f8c4c2b739e54979b7c913fd). Removed from the queue. |
| gen/bp-05-spacing-and-range/019/web2.png | FAIL | 85/95/97/213 | Outro title exact ('Next lesson: Entry and exit rules.'); 'Bring your notes' touches the notebook. But the scene-transition arrow still stops short of the glass card (visible gap). Next: web3.png on the v3 prompt (v2 superseded). |

### BP-07 first scoring (web.png; queue had listed web1.png)

- **001 PASS** — doorway-and-form walk-through, 5 empty rows, greyed locked confirm, EXAMPLE. Both tips touch (form top; confirm button).
- **002 PASS** — disclaimer exact: "Education only. Not financial advice." No arrows.
- **003 FAIL** — scene-transition arrow short of the form (clear navy gap); "Spot = you own what you buy" tip short of the notebook. "Paper = pretend money" touches the form. Next: web2/v2.
- **004 PASS** — blank logo plate and broken chain. "App name may show" on the plate; "Course is not linked to it" in the break of the chain.
- **005 FAIL** — five correct field labels and EXAMPLE, but all five label tips stop short of the form-row left ends (gap in the left padding). Next: web2/v2.
- **006 PASS** — Spot vs leverage/borrowing, check vs X, labels under, 0 arrows.
- **007 PASS** — API key / Seed phrase / Password each with an X; "Never paste them in a course field or chat." Tips land on the key, card, field, and input.
- **008 PASS** — "Read it from your notes" on the highlighted notebook pair line; "Pair box first" on the highlighted form pair row. EXAMPLE.
- **009 PASS** — "Top price" and "Bottom price" tips on the right ends of the two highlighted fields. EXAMPLE.
- **010 PASS** — "Number of gaps" tip in the green gap; "Not number of lines" tip on the amber X on a rung. EXAMPLE.
- **011 PASS** — "No box for it" tip inside the form (past the bottom border); "Read it out anyway" on the speech bubble.
- **012 PASS** — "Filled in by the app" tip on the pre-filled squiggle; "Not your choice: check it" under the form, no arrow.
- **013 PASS** — "The lesson stops here" on the amber stop-hand; "Confirm button" on the confirm bar.
- **014 PASS** — five cyan ticks, confirm greyed, EXAMPLE. Tips on a tick and on the confirm bar.
- **015 PASS** — exactly the four specified recap chips, 0 arrows. (VO lists six ideas; the remake prompt only asked for these four.)
- **016 PASS** — "Draw the broken link" tip in the break of the sketched chain; pencil inside the page.
- **017 PASS** — all five tips on the left ends of the five empty boxes. Pencil inside. No EXAMPLE required (no digits).
- **018 PASS** — "Own it: yes" / "Borrowed money: no," 0 arrows, pencil inside, no coins.
- **019 FAIL** — four scene-matching connectors short of the right form (visible gaps). Left form also shows 4 rows vs the right's 5, and the rows are not visibly in a different order. Next: web2/v2.
- **020 FAIL** — notebook-to-card panel-connector floats well short of the laptop/card (large gap); "Bring your notes" tip short of the notebook. Outro title exact: "Next lesson: Managing and monitoring." Next: web2/v2.

**BP-04: 16/20 — NOT 100%.** Rows left: 006 (gen/bp-04-market-regimes/006/web4.png), 007 (gen/bp-04-market-regimes/007/web3.png), 011 (gen/bp-04-market-regimes/011/web3.png), 015 (gen/bp-04-market-regimes/015/web3.png).
**BP-05: 16/19 — NOT 100%.** Rows left: 006 (gen/bp-05-spacing-and-range/006/web3.png), 015 (gen/bp-05-spacing-and-range/015/web3.png), 019 (gen/bp-05-spacing-and-range/019/web3.png).
**BP-06: 12/20 — NOT 100%.** Rows left: 006 (gen/bp-06-entry-and-exit/006/web2.png), 010 (gen/bp-06-entry-and-exit/010/web2.png), 012 (gen/bp-06-entry-and-exit/012/web2.png), 014 (gen/bp-06-entry-and-exit/014/web2.png), 016 (gen/bp-06-entry-and-exit/016/web2.png), 018 (gen/bp-06-entry-and-exit/018/web2.png), 019 (gen/bp-06-entry-and-exit/019/web2.png), 020 (gen/bp-06-entry-and-exit/020/web2.png).
**BP-07: 16/20 — NOT 100%.** Rows left: 003 (gen/bp-07-spot-paper-trading/003/web2.png), 005 (gen/bp-07-spot-paper-trading/005/web2.png), 019 (gen/bp-07-spot-paper-trading/019/web2.png), 020 (gen/bp-07-spot-paper-trading/020/web2.png).

Updated ChatGPT queue (BP-04..11): 101 items.


---

## Run on top of 0cc141a — 14 Nov 2026 (WITA): remake scoring for BP-04 006

Same perfect-run rules (every category at least 4/5, no hard fails; every arrow tip, panel connectors included, must visibly touch its target; doubt = fail). The render used the prompt current when the batch started and was scored on its own merits against the beat. Headline matches its job; no mismatch.

| File | Result | Margins (l/r/t/b) | Reason |
|---|---|---|---|
| gen/bp-04-market-regimes/006/web4.png | PASS | 78/77/81/153 | Three rungs; clean start and end; every crossing dotted. 'Each dot = an order filling' tip now lands on a glowing crossing-dot (the v3 miss). 'Price crosses the same lines again and again' tip sits on the middle rung. EXAMPLE present. Placed at out/ and course/images/bp-04-market-regimes/006.png (`source: chatgpt-web`, scored_blob a9936e9997ea49f1b9c7b63a43b8b9f376a1dd8d). Removed from the queue. |

**BP-04: 17/20 — NOT 100%.** Rows left: 007 (gen/bp-04-market-regimes/007/web3.png), 011 (gen/bp-04-market-regimes/011/web3.png), 015 (gen/bp-04-market-regimes/015/web3.png).
**BP-05: 16/19 — NOT 100%.** Rows left: 006 (gen/bp-05-spacing-and-range/006/web3.png), 015 (gen/bp-05-spacing-and-range/015/web3.png), 019 (gen/bp-05-spacing-and-range/019/web3.png).
**BP-06: 12/20 — NOT 100%.** Rows left: 006 (gen/bp-06-entry-and-exit/006/web2.png), 010 (gen/bp-06-entry-and-exit/010/web2.png), 012 (gen/bp-06-entry-and-exit/012/web2.png), 014 (gen/bp-06-entry-and-exit/014/web2.png), 016 (gen/bp-06-entry-and-exit/016/web2.png), 018 (gen/bp-06-entry-and-exit/018/web2.png), 019 (gen/bp-06-entry-and-exit/019/web2.png), 020 (gen/bp-06-entry-and-exit/020/web2.png).
**BP-07: 16/20 — NOT 100%.** Rows left: 003 (gen/bp-07-spot-paper-trading/003/web2.png), 005 (gen/bp-07-spot-paper-trading/005/web2.png), 019 (gen/bp-07-spot-paper-trading/019/web2.png), 020 (gen/bp-07-spot-paper-trading/020/web2.png).

Updated ChatGPT queue (BP-04..11): 100 items.

---

## Ledger update — 14 Nov 2026 (WITA): script rewrite b608319

Orchestrator ledger update against verifier report `/workspace/bp-script-check-0249f40/REPORT-b608319.md` and the rewrite at `b608319e26e72e0ef0957c7fc83ff5669ed1e8cc`. Placed files were left in `course/images`. No images were generated. Rows reopened or updated as not-current so nothing renders off the old stills. Exact replacement text is in each row's `fix_note`.

### Reopened / updated
- BP-04 006, 007, 011 (006 was a pass and is newly reopened; 007 and 011 were already fails and now carry the new narration text).
- BP-05 015 (already a fail; now carries the recap replacement text). 006 stays an existing fail (report: acceptable after the narration fix; nice to remake, not required). 019 stays an existing outro fail.
- BP-06 006, 010, 012, 014, 019 (already fails; now carry the new headlines). 016, 018, 020 stay as prior unlisted fails.
- BP-07 005, 019 (already fails; "LINES" as a field contradicts "gaps, not lines"). 003 and 020 stay as prior unlisted fails.
- BP-08..11: every still they **use** in the b608319 plan (14 per lesson) marked not-current for remake to the current beginner standard. Unused title-card / Your-turn / outro stills were already fails and stay in the denominator (not on the drop list).
- **BP-10 008 was not dropped** — it is still used in the plan. Remake it as "PAGE TWO: SAME PAIR, NEW BAND".

### Updated counts (dropped rows excluded; none dropped in this ledger)
- **BP-04: 16/20 — NOT 100%.**
- **BP-05: 16/19 — NOT 100%.**
- **BP-06: 12/20 — NOT 100%.**
- **BP-07: 16/20 — NOT 100%.**
- **BP-08: 0/20 — NOT 100%.**
- **BP-09: 0/21 — NOT 100%.**
- **BP-10: 0/21 — NOT 100%.**
- **BP-11: 0/20 — NOT 100%.**
- Queue (BP-04..11): 101 items. Script-rewrite stills are first, then remaining prior fails.

---

## Run on top of c3d1daa — 14 Nov 2026 (WITA): Cursor-agent remakes for BP-04 006, 007, 011

Authentic 1536×1024 files fetched via the GitHub Contents API (base64) and checked against git hash-object. 006 is identical at lesson commit cfa2179 and tip 3a1137a (`cursor1.png`). 007 and 011 were rescored from `8cb7a75539553b75b2ef45ab38ac217e5052039e` (`cursor2.png`), not the earlier cfa2179 files. Scored against 7a0430a / b608319 narration and REPORT-b608319 replacement text, on the same strict rubric (every category at least 4/5, no hard fails; every arrow tip must visibly touch its target; doubt = fail; margins at least 45px luma>110; EXAMPLE; approved mascot only; beginner standalone; no contradiction of earlier lessons on cross vs fill).

| File | Result | Margins (l/r/t/b) | Scores | Notes |
|---|---|---|---|---|
| gen/bp-04-market-regimes/006/cursor1.png | PASS | 96/96/111/104 | 5/5/5/5/5/—/5 | blob b8e740a5a84a9c6ef3345ce0123eb395c4f00b50. 'A CROSS IS NOT A FILL'; 'Cross: price touches a line' / 'Fill: an order trades'. Both tips touch. Teaches the required cross-vs-fill idea. |
| gen/bp-04-market-regimes/007/cursor2.png | PASS | 96/96/109/124 | 5/5/5/5/5/—/5 | blob 662f3d07bee08ddc2d495f3916beb6d304663baa @ 8cb7a75. 'TREND: KEEPS GOING ONE WAY'; 'Higher highs' / 'Small pullbacks'. Both tips sit on the path. |
| gen/bp-04-market-regimes/011/cursor2.png | PASS | 103/116/109/164 | 5/5/5/5/5/—/5 | blob b77ca17810991f7a7b6b70cfffeb8d8e341c4345 @ 8cb7a75. 'BAND TOO TIGHT FOR A NORMAL DAY'; 'Your band' / 'Normal up-and-down'. All contacts touch. |

### Updated counts
- **BP-04: 19/20 — not 100%.** Still queued: 015 (not in this Cursor batch).

---

## Cursor-agent remake for BP-05 015 (on top of the BP-04 commit)

Authentic 1536×1024 file from `29de59507d9c31a296671b026df83d3b4c080a0c` (identical at tip 3a1137a), blob `ea3082e7c76c8a10f3ff996a85149ebb6475b21c`.

| File | Result | Margins (l/r/t/b) | Scores | Notes |
|---|---|---|---|---|
| gen/bp-05-spacing-and-range/015/cursor1.png | PASS | 100/116/112/115 | 5/5/5/5/5/—/5 | 'RECAP' with the four required marks and a 7-line / 6-gap house example. |

### Updated counts
- **BP-05: 17/19 — not 100%.** Still queued: 006, 019 (not in this Cursor batch).

---

## Cursor-agent remakes for BP-06 006, 010, 012, 014, 019

006, 010, 012 and 019 from `cc73f31c02a4df10778a3565dc1373f976d1fcb8` (identical at tip 3a1137a). 014 rescored from `8cb7a75539553b75b2ef45ab38ac217e5052039e` (`cursor2.png`).

| File | Result | Margins (l/r/t/b) | Scores | Blob |
|---|---|---|---|---|
| gen/bp-06-entry-and-exit/006/cursor1.png | PASS | 102/166/107/164 | 5/5/5/5/5/—/5 | 70ef875cf1dfd6ba92b2ecfe9a7ab71b848bab3f |
| gen/bp-06-entry-and-exit/010/cursor1.png | PASS | 102/166/107/164 | 5/5/5/5/5/—/5 | cc7d4af5e7b588efbc460df174c5c341652e66f7 |
| gen/bp-06-entry-and-exit/012/cursor1.png | PASS | 102/166/108/235 | 5/5/5/5/5/—/5 | c2198d1b59768e10f9a59aa8048577b1b45f2146 |
| gen/bp-06-entry-and-exit/014/cursor2.png | PASS | 101/136/108/235 | 5/5/5/5/5/—/5 | bd6862e5adeb61215a9b515937d738569e3408be @ 8cb7a75 |
| gen/bp-06-entry-and-exit/019/cursor1.png | PASS | 101/166/107/164 | 5/5/5/5/5/—/5 | b95a3d59564d50bd90e1dc83a39d9ea7be49db2b |

All required headlines are exact; arrow tips touch. 

### Updated counts
- **BP-06: 17/20 — not 100%.** Other queued rows (not in this Cursor batch) remain.

---

## Cursor-agent remakes for BP-07 005 and 019

Both from `d62988f6c93856cadc5410b04219ec8b2382a6ca` (identical at tip 3a1137a).

| File | Result | Margins (l/r/t/b) | Scores | Blob |
|---|---|---|---|---|
| gen/bp-07-spot-paper-trading/005/cursor1.png | PASS | 103/176/111/254 | 5/5/5/5/5/—/5 | 3b621dcea5e76e897eab32ade7e36395d8968e18 |
| gen/bp-07-spot-paper-trading/019/cursor1.png | PASS | 103/176/109/254 | 5/5/5/5/5/—/5 | 0ba89c2a924230dd301cb007a3068ef05f7cd8f0 |

Five fields are Pair / Top / Bottom / Gap count / Your two rules. No 'LINES' field.

### Updated counts
- **BP-07: 18/20 — not 100%.** Other queued rows (not in this Cursor batch) remain.

---

## Cursor-agent remakes for bp-08-managing-and-monitoring used stills

Scored from `36ceecfef79bc2f7066f1d2fe5b96c73dacaa4d7` (010 from `8cb7a75539553b75b2ef45ab38ac217e5052039e`). All 14 used stills PASS, placed, source cursor.

| File | Result | Margins (l/r/t/b) | Scores | Blob |
|---|---|---|---|---|
| gen/bp-08-managing-and-monitoring/001/cursor1.png | PASS | 101/120/109/95 | 5/5/5/5/5/—/5 | `d8a2886cce33fa7aee0ea6b70e409c5e236420f1` |
| gen/bp-08-managing-and-monitoring/004/cursor1.png | PASS | 102/120/109/95 | 5/5/5/5/5/—/5 | `63e47dd3bb825f5eadd18f2c6fe542081f3a8d83` |
| gen/bp-08-managing-and-monitoring/005/cursor1.png | PASS | 102/206/111/164 | 5/5/5/5/5/—/5 | `51dfe88ce3c6e18bc05a8f9b0848900879d203f7` |
| gen/bp-08-managing-and-monitoring/006/cursor1.png | PASS | 101/156/109/124 | 5/5/5/5/5/—/5 | `79a45bf55552254af086005bf535a88cf1c0d2dc` |
| gen/bp-08-managing-and-monitoring/007/cursor1.png | PASS | 103/120/109/95 | 5/5/5/5/5/—/5 | `bf6cb9faf399916e13cb35a28b036772c6c15ec1` |
| gen/bp-08-managing-and-monitoring/008/cursor1.png | PASS | 103/120/109/95 | 5/5/5/5/5/—/5 | `768469a2f381791a548037054b63c72619697232` |
| gen/bp-08-managing-and-monitoring/009/cursor1.png | PASS | 103/120/109/95 | 5/5/5/5/5/—/5 | `a90f9745c04551c6beabbcc87781dc8b6b2f8c8a` |
| gen/bp-08-managing-and-monitoring/010/cursor2.png | PASS | 102/176/109/144 | 5/5/5/5/5/—/5 | `6057bfeea6ef20a6a38cc8b86963c8844ef400a1` |
| gen/bp-08-managing-and-monitoring/011/cursor1.png | PASS | 101/120/109/95 | 5/5/5/5/5/—/5 | `0b8cddc5dc8894ca127d784ffb4a5923e9eb8cf8` |
| gen/bp-08-managing-and-monitoring/012/cursor1.png | PASS | 103/120/109/95 | 5/5/5/5/5/—/5 | `67f3aeea0e847aca2005a4f33f9bcb465c69916a` |
| gen/bp-08-managing-and-monitoring/013/cursor1.png | PASS | 101/120/109/95 | 5/5/5/5/5/—/5 | `421f09975fddcd90c6fde3b003d4d8a5f357de08` |
| gen/bp-08-managing-and-monitoring/014/cursor1.png | PASS | 101/120/109/95 | 5/5/5/5/5/—/5 | `12bfe709501756bfdec796850bcce1d1a1b5842e` |
| gen/bp-08-managing-and-monitoring/015/cursor1.png | PASS | 103/120/110/95 | 5/5/5/5/5/—/5 | `567b3f1ff9303e5279a46902b67425ef87f4ee91` |
| gen/bp-08-managing-and-monitoring/019/cursor1.png | PASS | 103/120/109/95 | 5/5/5/5/5/—/5 | `b0b586c53a0d4170d48a89173c3e0f954ea95081` |

### Updated counts
- **BP-08: 14/20 — not 100%.** Unused title / your-turn / outro rows remain in the queue and were not in this Cursor batch.

---

## Cursor-agent remakes for bp-09-common-mistakes used stills

Scored from `c6cfb35131b48a7a4dd5f613dac374f76dc4c0d8` (identical at tip 3a1137a). All 14 used stills PASS, placed, source cursor.

| File | Result | Margins (l/r/t/b) | Scores | Blob |
|---|---|---|---|---|
| gen/bp-09-common-mistakes/001/cursor1.png | PASS | 103/120/109/95 | 5/5/5/5/5/—/5 | `f8573cb93bf837f4f608bb334413b2ac5120398a` |
| gen/bp-09-common-mistakes/004/cursor1.png | PASS | 101/120/109/95 | 5/5/5/5/5/—/5 | `6d621941449562781b4412646053ba08b26179dd` |
| gen/bp-09-common-mistakes/005/cursor1.png | PASS | 101/120/109/95 | 5/5/5/5/5/—/5 | `b862823eb7074e01e14057bd3bc2439829d6f98f` |
| gen/bp-09-common-mistakes/006/cursor1.png | PASS | 103/120/109/95 | 5/5/5/5/5/—/5 | `2684ad87c41e2ec293b112c3f5685d626c40d0c7` |
| gen/bp-09-common-mistakes/007/cursor1.png | PASS | 102/356/112/124 | 5/5/5/5/5/—/5 | `cdef486897d99dfd10cc571ac821f1d056cede88` |
| gen/bp-09-common-mistakes/008/cursor1.png | PASS | 101/120/109/95 | 5/5/5/5/5/—/5 | `ffb8b90408dde2a5a7f57c5b97fa6f6ba35d2354` |
| gen/bp-09-common-mistakes/009/cursor1.png | PASS | 103/120/109/95 | 5/5/5/5/5/—/5 | `d7fb787318ff1d5d2b1c643961cc37acac0d3d1c` |
| gen/bp-09-common-mistakes/010/cursor1.png | PASS | 102/136/109/124 | 5/5/5/5/5/—/5 | `d63e326f0ad9b750a2c24b756b0e2af600769031` |
| gen/bp-09-common-mistakes/011/cursor1.png | PASS | 103/120/110/95 | 5/5/5/5/5/—/5 | `9d130670c26dcef31593d7eb9809169502020c91` |
| gen/bp-09-common-mistakes/012/cursor1.png | PASS | 101/120/109/95 | 5/5/5/5/5/—/5 | `3856331becafbc1ff26427ae1ebae14a0f3363a9` |
| gen/bp-09-common-mistakes/013/cursor1.png | PASS | 102/120/109/95 | 5/5/5/5/5/—/5 | `266064d0266f6d3792524743138ea30cd036ad91` |
| gen/bp-09-common-mistakes/014/cursor1.png | PASS | 102/120/109/95 | 5/5/5/5/5/—/5 | `337ef77a55ad4f05f52d072e62812007a5b8072c` |
| gen/bp-09-common-mistakes/015/cursor1.png | PASS | 103/120/110/95 | 5/5/5/5/5/—/5 | `870f8e2e8a739e9a7ae8274b972d4db3a52decb2` |
| gen/bp-09-common-mistakes/020/cursor1.png | PASS | 103/120/109/95 | 5/5/5/5/5/—/5 | `ee64e0fd4eebfe819ef22e4e6792ce456067f5bd` |

### Updated counts
- **BP-09: 14/21 — not 100%.** Unused title / your-turn / outro rows remain in the queue and were not in this Cursor batch.

---

## Cursor-agent remakes for bp-10-scaling-up used stills

Scored from `2203da82b2cf2cc81d4ce06b45ecbe10c8587635` (identical at tip 3a1137a). All 14 used stills PASS, placed, source cursor.

| File | Result | Margins (l/r/t/b) | Scores | Blob |
|---|---|---|---|---|
| gen/bp-10-scaling-up/001/cursor1.png | PASS | 101/120/109/95 | 5/5/5/5/5/—/5 | `9fcfff72ad2ad1943156570b8d2698a8510a4861` |
| gen/bp-10-scaling-up/004/cursor1.png | PASS | 103/120/109/95 | 5/5/5/5/5/—/5 | `9edc11a9b20d811466e41cc16bdd431dc12b68e6` |
| gen/bp-10-scaling-up/005/cursor1.png | PASS | 101/120/109/95 | 5/5/5/5/5/—/5 | `0d69f63412478da17fad453f103f1199b1764e5e` |
| gen/bp-10-scaling-up/006/cursor1.png | PASS | 101/120/109/95 | 5/5/5/5/5/—/5 | `809d021a7a557bd28dbe7c5e4a473f66aa51dbf0` |
| gen/bp-10-scaling-up/007/cursor1.png | PASS | 102/120/109/95 | 5/5/5/5/5/—/5 | `5e478df7c903ad3fa85816bf2bc96ae5f5807e2b` |
| gen/bp-10-scaling-up/008/cursor1.png | PASS | 103/120/109/95 | 5/5/5/5/5/—/5 | `953eb68bad1091e72f4ad560978bd0c3ed560c6a` |
| gen/bp-10-scaling-up/009/cursor1.png | PASS | 101/120/109/95 | 5/5/5/5/5/—/5 | `a0ee852d00ed0d5ec6ed2add4f1b603a767c9b2e` |
| gen/bp-10-scaling-up/010/cursor1.png | PASS | 103/120/109/95 | 5/5/5/5/5/—/5 | `494d2d549571857d89a2b2b6098cc415384e39fa` |
| gen/bp-10-scaling-up/011/cursor1.png | PASS | 103/120/109/95 | 5/5/5/5/5/—/5 | `7068607b78a4a713eed4bf3f9fcd71a7565fbfe8` |
| gen/bp-10-scaling-up/012/cursor1.png | PASS | 103/120/109/95 | 5/5/5/5/5/—/5 | `45547a82833a9744c5f5672c6783a29ab803eb72` |
| gen/bp-10-scaling-up/013/cursor1.png | PASS | 101/120/109/95 | 5/5/5/5/5/—/5 | `3f8614e9d61467e62bf1ccf1283d5588920e59aa` |
| gen/bp-10-scaling-up/014/cursor1.png | PASS | 102/120/109/95 | 5/5/5/5/5/—/5 | `0e671249f5f93faeb8ad34a77f53d138af264b1c` |
| gen/bp-10-scaling-up/015/cursor1.png | PASS | 103/120/110/95 | 5/5/5/5/5/—/5 | `25c6357eaf918b048ec109a0487c83ce2eeb6f25` |
| gen/bp-10-scaling-up/020/cursor1.png | PASS | 103/120/109/95 | 5/5/5/5/5/—/5 | `8b58946bf76bedfda5c3fc3373733f1e4391672a` |

### Updated counts
- **BP-10: 14/21 — not 100%.** Unused title / your-turn / outro rows remain in the queue and were not in this Cursor batch.

---

## Cursor-agent remakes for bp-11-advanced-liquidation used stills

Scored from `3a1137a197ca9d295a229b829a46526637b49e86` (identical at tip 3a1137a). All 14 used stills PASS, placed, source cursor.

| File | Result | Margins (l/r/t/b) | Scores | Blob |
|---|---|---|---|---|
| gen/bp-11-advanced-liquidation/001/cursor1.png | PASS | 102/120/109/95 | 5/5/5/5/5/—/5 | `e3ce6f3b8f836afb488ba512fdea57d1c49a50be` |
| gen/bp-11-advanced-liquidation/004/cursor1.png | PASS | 101/120/109/95 | 5/5/5/5/5/—/5 | `d3a9442b2404141f0fcd21d3b4ca3cf0b00d6b47` |
| gen/bp-11-advanced-liquidation/005/cursor1.png | PASS | 101/120/109/95 | 5/5/5/5/5/—/5 | `840cfabd55be475780e53388458601068483a58f` |
| gen/bp-11-advanced-liquidation/006/cursor1.png | PASS | 103/120/109/95 | 5/5/5/5/5/—/5 | `1b6d814dc20a4f639831c1c007ce7bf3c16f2ba0` |
| gen/bp-11-advanced-liquidation/007/cursor1.png | PASS | 103/120/109/95 | 5/5/5/5/5/—/5 | `8fd6e21cbc474541ad86664e88ba828acefe99ae` |
| gen/bp-11-advanced-liquidation/008/cursor1.png | PASS | 102/120/109/95 | 5/5/5/5/5/—/5 | `ac5511a22a53231fec81860f0b493be6729186c1` |
| gen/bp-11-advanced-liquidation/009/cursor1.png | PASS | 103/120/109/95 | 5/5/5/5/5/—/5 | `80e1e0f6bc9e31b3127489f46f16a56baf5ed525` |
| gen/bp-11-advanced-liquidation/010/cursor1.png | PASS | 103/120/109/95 | 5/5/5/5/5/—/5 | `df536ec9158e70a6cde4c937b0223739aef4c726` |
| gen/bp-11-advanced-liquidation/011/cursor1.png | PASS | 102/120/109/95 | 5/5/5/5/5/—/5 | `f7a28dfe73eedb78719025791495e049a81c33af` |
| gen/bp-11-advanced-liquidation/012/cursor1.png | PASS | 102/120/109/95 | 5/5/5/5/5/—/5 | `ce65ee9940785297ec5395a6086c0345bc5ac309` |
| gen/bp-11-advanced-liquidation/013/cursor1.png | PASS | 103/120/109/95 | 5/5/5/5/5/—/5 | `d0af8eecd50f5a89cc174c92a45c0bbff48fe647` |
| gen/bp-11-advanced-liquidation/014/cursor1.png | PASS | 103/120/109/95 | 5/5/5/5/5/—/5 | `8b41a28cbbeef8cfc0e1df2e55719c848168a179` |
| gen/bp-11-advanced-liquidation/015/cursor1.png | PASS | 103/120/110/95 | 5/5/5/5/5/—/5 | `65ec7a0d3696d9143f06085706b39d458fb483c5` |
| gen/bp-11-advanced-liquidation/019/cursor1.png | PASS | 102/120/109/95 | 5/5/5/5/5/—/5 | `8e26bcccdd0883ac2194649a136568cc3e18daf4` |

### Updated counts
- **BP-11: 14/20 — not 100%.** Unused title / your-turn / outro rows remain in the queue and were not in this Cursor batch.

---

## Ledger update — 14 Nov 2026 (WITA): e03191f render plan unused drops
Re-ran `studio.plan(sid)` myself from `e03191f74c352b0fadf68a91dad11d86f5b89a3b` (d1f6) for BP-01 through BP-11. Nothing rendered, nothing pushed. Used = a `lesson-still` shot whose `lesson_still` is `course/images/<lesson>/NNN.png`. Confirmed against `/workspace/bp-script-check-0249f40/USED-STILLS-e03191f.md` and `planE.json`: the BP-04..11 used/unused sets and shot counts in that file match this run exactly. Orchestrator's claim that every lesson shows 14 stills is true for BP-03..11, but not for BP-01 (13 used) or BP-02 (15 used). The USED-STILLS table itself only lists BP-04..11.
Dropped every BP-04..11 still outside those used sets, including already-passing unused title / disclaimer / your-turn / outro rows on BP-04..07 (needed so each lesson denominator is the 14 used stills). Reason on each row: `not in e03191f render plan`. Placed files left in place. Excluded from denominators. BP-04 015 (Paper sort) and BP-05 006 (Half spacing) stay used and queued. Did not change BP-01..03 drops: the file does not clearly list those lessons' unused sets (it only notes that BP-02 014 is used again).

### Dropped (49 stills)
- **BP-04:** 002 (was_pass), 003 (was_pass), 016 (was_pass), 017 (was_pass), 018 (was_pass), 020 (was_pass)
- **BP-05:** 002 (was_pass), 003 (was_pass), 016 (was_pass), 017 (was_pass), 019 (was_fail)
- **BP-06:** 002 (was_pass), 003 (was_pass), 016 (was_fail), 017 (was_pass), 018 (was_fail), 020 (was_fail)
- **BP-07:** 002 (was_pass), 003 (was_fail), 016 (was_pass), 017 (was_pass), 018 (was_pass), 020 (was_fail)
- **BP-08:** 002 (was_fail), 003 (was_fail), 016 (was_fail), 017 (was_fail), 018 (was_fail), 020 (was_fail)
- **BP-09:** 002 (was_fail), 003 (was_fail), 016 (was_fail), 017 (was_fail), 018 (was_fail), 019 (was_fail), 021 (was_fail)
- **BP-10:** 002 (was_fail), 003 (was_fail), 016 (was_fail), 017 (was_fail), 018 (was_fail), 019 (was_fail), 021 (was_fail)
- **BP-11:** 002 (was_fail), 003 (was_fail), 016 (was_fail), 017 (was_fail), 018 (was_fail), 020 (was_fail)

### Used-still counts after the drop (denominators = e03191f used set)
| Lesson | Used stills | Pass | Fail | Remaining queued |
|---|---:|---:|---:|---|
| BP-04 | 14 | 13 | 1 | 015 Paper sort — 13/14, not 100% |
| BP-05 | 14 | 13 | 1 | 006 Half spacing — 13/14, not 100% |
| BP-06 | 14 | 14 | 0 | — — 14/14, 100% |
| BP-07 | 14 | 14 | 0 | — — 14/14, 100% |
| BP-08 | 14 | 14 | 0 | — — 14/14, 100% |
| BP-09 | 14 | 14 | 0 | — — 14/14, 100% |
| BP-10 | 14 | 14 | 0 | — — 14/14, 100% |
| BP-11 | 14 | 14 | 0 | — — 14/14, 100% |

Overall BP-04..11: **110/112** pass, 2 fail, 49 dropped (excluded).

Used stills that are not a current pass (only these two): BP-04 015 and BP-05 006. No other used still in BP-01..11 is short of a pass.

### BP-01..03 (no ledger change)
Verified with the same `studio.plan()` run. USED-STILLS-e03191f.md does not table these lessons, so existing drops were left as they are.
- **BP-01** used 13: 001, 004–012, 014, 015, 017. All 13 are current passes (13/13 on the used set). Ledger denominator is still 31/31 all-rows / 17/17 lesson-stills (unused 002, 003, 016, 018 remain as passes in the denominator; 013 is already dropped and is unused in this plan too).
- **BP-02** used 15: 001, 004–015, 019, 020, including 014 (Empty pair), which is a current pass. 15/15 on the used set. Ledger denominator is still 31/31 all-rows / 20/20 lesson-stills (unused 002, 003, 016, 017, 018 remain as passes; 021 is already dropped and is unused in this plan too).
- **BP-03** used 14: 001, 004–015, 018. All 14 are current passes (14/14 on the used set). Ledger denominator is still 28/28 all-rows / 19/19 lesson-stills (unused 002, 003, 016, 017, 019 remain as passes; no existing drops).
