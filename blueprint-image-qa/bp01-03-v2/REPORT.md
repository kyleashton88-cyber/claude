# BP-01..BP-03 image QA v2 (strict first scoring)

Scored by Creative Studio, 14 Nov 2026 (WITA). Same strict method as bp04-11. Image scoring only: no verdict on the BP-01..03 videos.

**Scope:** image fields of course/scripts/bp-01..bp-03 @ d1f6 `fbb3f9c` (58 stills); files scored from cursor/blueprint-beginner-images `2f8bac1`.

**Result:** lesson stills 48 pass / 10 fail of 58. Stage 2 (34 shared/code-drawn assets): 8 pass / 26 fail. Whole list: 56 pass / 36 fail of 92. Remake queue: 11 (needs_mascot_ref: 0). Code fixes: 25 frames, see CODE_FIXES.md. (Updated 14 Nov after the BP-01/02 remake round below; first scoring was 37/21 stills, 45/47 overall.)

**Mismatches:** none. All 58 blobs are identical on d1f6 and beginner-images and match the v10 pass list's scored_blob. All 58 were 'pass' on v10; 21 are overturned here.

**Other finding:** the numbers files (d1f6) set the on-screen disclaimer to 'Educational content only. Not financial advice.', which is not the exact line (CODE_FIXES.md CF-1).

**Fix status:** every fail = `needs_remake`, prompt written (specs/remake/<lesson>__NNN.txt, copied to remake/), not regenerated. Old prompts moved to specs/remake/_superseded/: `bp-01-introduction__010.v1.txt`, `bp-02-what-you-need__004.v1.txt`, `bp-03-what-is-a-grid-bot__003.v1.txt`, `bp-03-what-is-a-grid-bot__010.v1.txt`.


## bp-01-introduction (Introduction): 18 total, 16 pass, 2 fail (after remake round 1; table below is the first scoring of the committed stills)

| File | Beat | Result | Reason | Fix status |
|---|---|---|---|---|
| 001.png | 1 Hook | FAIL | Clear sideways band, but the EXAMPLE stamp has a stray double-headed arrow pointing at the top line, and the zig-zag peaks stop short of the top line, so the price never visibly 'bounces' off it. Hard fail: artifact: stray double-headed arrow from the EXAMPLE stamp to the top dashed line. | needs remake, prompt `bp-01-introduction__001.txt` |
| 002.png | 2 Disclaimer | FAIL | Disclaimer card does not show the exact line 'Education only. Not financial advice.': it reads 'EDUCATION ONLY' plus tags 'Learning' / 'Not money advice'. Hard fail: disclaimer not exact. | needs remake, prompt `bp-01-introduction__002.txt` |
| 003.png | 3 Title card | PASS | Title card shows the lesson title (INTRODUCTION TO GRID BOTS) with a simple ladder: sells marked higher, buys lower, EXAMPLE stamp, one-line definition. Minor: the definition tag's arrow lands on an empty bottom line; last trough has no dot. | passed as is |
| 004.png | 4 The three parts | PASS | Three numbered cards (range / levels / stop) match the beat; plain labels. | passed as is |
| 005.png | 5 The range | PASS | Top and bottom lines with the range shaded between, EXAMPLE stamp; matches the beat. | passed as is |
| 006.png | 6 The levels | PASS | Ladder rungs = levels, waiting order tickets on rungs, EXAMPLE stamp; matches the beat. | passed as is |
| 007.png | 7 Buys and sells | FAIL | Diagram is right (sells above in mint, buys below in blue, price-now line), but the headline 'BUY LOW, SELL HIGH' is a profit slogan, not the beat ('buy orders below the mark, sell orders above it'). Fails the no-pitch rule. | needs remake, prompt `bp-01-introduction__007.txt` |
| 008.png | 8 The stop | PASS | Notebook with a written line + amber stop sign; 'Write it before you start' matches 'the stop is a sentence you write'. | passed as is |
| 009.png | 9 No order is sent | PASS | Crossed-out SEND button vs paper notebook; 'No order is sent' matches the beat. | passed as is |
| 010.png | 10 The map | FAIL | Course map path has 12 stones (pin stone + 11 ahead), so it contradicts both '10 lessons ahead' and the 11-lesson course. Hard fail: wrong number: 11 stones ahead of the 'You are here' stone but the label says '10 lessons ahead'. | needs remake, prompt `bp-01-introduction__010.txt` |
| 011.png | 11 When the drawing fails | PASS | Band, path leaves the top and keeps going, exit circled, EXAMPLE stamp; matches the beat. | passed as is |
| 012.png | 12 No result number | PASS | Crossed-out results board vs notebook; 'No results shown' matches 'no result number'. | passed as is |
| 013.png | 13 Eight ticks | PASS | Notebook band with 9 lines = 8 roughly even steps, EXAMPLE stamp; matches 'eight even ticks'. Minor: hand-drawn box is slightly skewed. | passed as is |
| 014.png | 14 The checklist is next | PASS | 1 paper checklist -> 2 laptop; matches 'checklist before screen'. | passed as is |
| 015.png | 15 Paper first | PASS | Glass fence around a practice laptop, 'Real market stays outside'; matches 'paper or demo account is a fence'. Minor: tiny unlabelled candle chart on the laptop trends upward. | passed as is |
| 016.png | 16 Your turn | FAIL | Content is right (Range / Levels / Stop on a notebook band), but the notebook base and pencil run to 37px from the bottom edge (under the 45px minimum). Hard fail: cramped margin: notebook base and pencil come within 37px of the bottom edge. | needs remake, prompt `bp-01-introduction__016.txt` |
| 017.png | 17 One sentence to keep | PASS | Range / Levels / Stop icons with 'Draw all three before any click'; matches the beat. | passed as is |
| 018.png | 18 Outro | FAIL | Outro names the next lesson only as 'WHAT YOU NEED' / 'what you need'; the next lesson's title is 'What you are going to need'. | needs remake, prompt `bp-01-introduction__018.txt` |

## bp-02-what-you-need (What you are going to need): 21 total, 21 pass, 0 fail (after remake round 1; table below is the first scoring of the committed stills)

| File | Beat | Result | Reason | Fix status |
|---|---|---|---|---|
| 001.png | 1 Hook | PASS | 1 notebook, 2 closed laptop; 'Paper before screen' matches 'you need a page before a screen'. | passed as is |
| 002.png | 2 Disclaimer | FAIL | Disclaimer card does not show the exact line 'Education only. Not financial advice.': it reads 'EDUCATION ONLY' plus 'For learning' / 'Not advice on what to buy'. Hard fail: disclaimer not exact. | needs remake, prompt `bp-02-what-you-need__002.txt` |
| 003.png | 3 Title card | FAIL | Title card headline is 'WHAT YOU WILL NEED', not the lesson title 'What you are going to need'; the desk slab runs to 24px from both side edges. Hard fail: cramped margin: the glass desk runs to 24px from the left and right edges. | needs remake, prompt `bp-02-what-you-need__003.txt` |
| 004.png | 4 Seven items | FAIL | Seven rows do not match the beat's seven lines (notebook, the three words, pair name, paper or demo, no secrets, a written stop, the word Example); 'EXAMPLE' appears as a stamp, a tag with an arrow to that stamp, and a checklist row. Hard fail: wrong count/content: rows are Notebook, Pair, Range, Levels, Stop, No secrets, EXAMPLE (missing 'paper or demo', three words split into two). | needs remake, prompt `bp-02-what-you-need__004.txt` |
| 005.png | 5 The three words | PASS | Range / Levels / Stop stacked blocks with plain definitions; matches the beat. | passed as is |
| 006.png | 6 Pair name | PASS | Two shapes joined by a slash: 'Thing you buy' / 'What you pay with' / 'Pair = the two together', EXAMPLE stamp. Minor: EXAMPLE stamp is amber, not cyan. | passed as is |
| 007.png | 7 Paper or demo | PASS | Sandbox practice laptop vs locked wallet in a glass box; matches 'paper or demo'. | passed as is |
| 008.png | 8 No secrets | PASS | Keys / Secret words / Passwords crossed off from a chat bubble, 'Never type them in a chat or form'; matches the beat. | passed as is |
| 009.png | 9 Written stop | PASS | Crossed-out tick vs written line; 'Just a tick: not enough' / 'Write a full sentence' matches the beat. | passed as is |
| 010.png | 10 The word Example | FAIL | Shows 'squiggle = EXAMPLE' rows, not a number or pair carrying the word Example, so a beginner cannot see what gets stamped; the left tag and pencil break the side margins. Hard fail: cramped margin: 'So nobody copies it as advice' tag sits ~43px from the left edge; pencil to 29px from the right edge. | needs remake, prompt `bp-02-what-you-need__010.txt` |
| 011.png | 11 Not on the list | PASS | Checklist with crossed-out target and gauge: 'Profit target: not here', 'Borrowed money: not here'; matches the beat. | passed as is |
| 012.png | 12 The form copies the page | PASS | Notebook page copied row-by-row into a form; matches 'the form copies the page'. | passed as is |
| 013.png | 13 You are early | PASS | One stone behind, 'You are here', 9 stones ahead = 11 lessons; matches 'you are early'. | passed as is |
| 014.png | 14 Empty pair | PASS | Form with the pair row empty and a pencil, 'Fill it later'; matches the beat. | passed as is |
| 015.png | 15 Common miss | PASS | Checklist path vs amber 'skip' path with X; matches the common miss. | passed as is |
| 016.png | 16 Your turn | FAIL | Seven tick boxes and right content, but the 'Copy the 7 lines' tag breaks the 45px right margin. Hard fail: cramped margin: 'Copy the 7 lines' tag ends ~43px from the right edge. | needs remake, prompt `bp-02-what-you-need__016.txt` |
| 017.png | 17 Your turn | PASS | Range / Levels / Stop drawn in a notebook; matches the beat. | passed as is |
| 018.png | 18 Your turn | FAIL | Pair circles and slash on a notebook, but an extra 'EXAMPLE' tag points at the EXAMPLE stamp (the word twice, the tag labels a label). | needs remake, prompt `bp-02-what-you-need__018.txt` |
| 019.png | 19 Recap | FAIL | Recap mislabels the range/levels/stop stack as 'Stop written down' and shows only four of the seven lines; does not show the recap the beat asks for (say the hook, name the diagram, name the line). | needs remake, prompt `bp-02-what-you-need__019.txt` |
| 020.png | 20 Finish the seven | PASS | Clipboard with 7 ticks + calendar 'Do it today'; matches 'complete the seven lines today'. | passed as is |
| 021.png | 21 Outro | PASS | Outro names the next lesson exactly: 'NEXT: WHAT IS A GRID BOT'. | passed as is |

## bp-03-what-is-a-grid-bot (What is a grid bot): 19 total, 11 pass, 8 fail

| File | Beat | Result | Reason | Fix status |
|---|---|---|---|---|
| 001.png | 1 Hook | FAIL | Crossed crystal ball is clear, but the 'orders waiting' board alternates mint and blue tickets (sell, buy, sell, buy), so it teaches the opposite of the course rule: sells sit above, buys below. | needs remake, prompt `bp-03-what-is-a-grid-bot__001.txt` |
| 002.png | 2 Disclaimer | FAIL | Disclaimer card does not show the exact line 'Education only. Not financial advice.': it reads 'EDUCATION ONLY' plus 'Learning' / 'Not advice'. Hard fail: disclaimer not exact. | needs remake, prompt `bp-03-what-is-a-grid-bot__002.txt` |
| 003.png | 3 Title card | FAIL | Title card shows 'WHAT IS A GRID BOT?', but a gear tagged 'Robot that places orders for you' frames the bot as a helper doing the work for you (product-pitch tone; contradicts beat 18 'not a person watching for you'), and its curved arrow lands in the empty gap between sell and buy rows. | needs remake, prompt `bp-03-what-is-a-grid-bot__003.txt` |
| 004.png | 4 Five labels | FAIL | Tags read Top / Bottom / Price steps / What you hold / Stop, but the narration teaches the five words upper, lower, levels, side, stop; 'Price steps' tag has three arrowheads and breaks the right margin. Hard fail: cramped margin: 'Price steps' tag ends 35px from the right edge. | needs remake, prompt `bp-03-what-is-a-grid-bot__004.txt` |
| 005.png | 5 Limit orders wait | PASS | Order ticket waits on a rung above the price line, 'Price has not reached it yet', EXAMPLE stamp; matches the beat. | passed as is |
| 006.png | 6 Price steps down | PASS | Price steps down through rungs and a buy ticket fills on the low rung, EXAMPLE stamp; matches the beat. | passed as is |
| 007.png | 7 Price steps up | PASS | Price steps up and a mint sell ticket fills on the high rung, EXAMPLE stamp; matches the beat. | passed as is |
| 008.png | 8 Inventory | FAIL | Two jars of coins: 'more of the coin' / 'more cash' with tautological 'What you hold = your holdings'; does not show uneven fills (balanced inside the band vs one heavy side after an exit); uses coins, which the brief bans. | needs remake, prompt `bp-03-what-is-a-grid-bot__008.txt` |
| 009.png | 9 The bot's job | PASS | Rungs with mint sells above and blue buys below, 'Bot's job: keep your orders waiting' / 'At the prices you wrote'; matches the clerical job in the beat. | passed as is |
| 010.png | 10 Say the five | FAIL | 'Say the five' frame labels Top / Price steps / Bottom / What you hold / Stop, not the five words the learner is told to say (upper, lower, levels, side, stop); no highlighted 'often skipped' tag. | needs remake, prompt `bp-03-what-is-a-grid-bot__010.txt` |
| 011.png | 11 Hypothetical path | PASS | 'This chart is made up', pretend path with fill dots, EXAMPLE stamp; matches 'hypothetical path'. | passed as is |
| 012.png | 12 Common miss | PASS | Orders filling on a band + crossed gauge 'Does not mean you earn'; matches the common miss. | passed as is |
| 013.png | 13 Not affiliated | PASS | Crossed handshake 'No partner company', shield 'We don't work for any exchange'; matches 'not affiliated'. | passed as is |
| 014.png | 14 One-breath definition | FAIL | Orders wait -> Inside your range -> Stop written -> Holdings change matches the one-breath definition, but the panel border breaks the 45px side margins. Hard fail: cramped margin: main panel border sits 40-41px from the left and right edges. | needs remake, prompt `bp-03-what-is-a-grid-bot__014.txt` |
| 015.png | 15 Paper check | PASS | Five blank tags around a box with the step-down arrow, 'Label the 5 words' / 'Draw one step down'; matches the paper check. | passed as is |
| 016.png | 16 Your turn | PASS | Five blank tags around a box, 'Fill in the 5 labels' / 'Say them out loud'; matches the beat. | passed as is |
| 017.png | 17 Your turn | PASS | Order waiting on a rung above the price, 'Price must reach it to fill'; matches the beat. | passed as is |
| 018.png | 18 What the bot is not | PASS | Not a signal / not a fund / not a person watching; matches the beat. | passed as is |
| 019.png | 19 Outro | FAIL | Outro says 'NEXT: MARKET SHAPES' and 'Next lesson: price shapes'; the next lesson is 'Market regimes' (two different wrong names on one frame). | needs remake, prompt `bp-03-what-is-a-grid-bot__019.txt` |

## Stage 2: the 34 non-script assets the masters use (shared stills, mascot, code-drawn frames)

Source: blueprint-smoke/BP01-03_IMAGE_USE.txt @fbb3f9c. **8 pass / 26 fail of 34.** ChatGPT assets 8/9 pass, code-drawn 0/25 pass. Whole list: 45 pass / 47 fail of 92.

- **Mascot:** confirmed approved. `course/images/mascot/blueprint-mascot.png` blob 5d421ae3 = the approved cut-out, identical on d1f6, beginner-images and PR #17 head.
- **Code-drawn frames** were scored from a fresh fbb3f9c render. The committed `blueprint-smoke/code-drawn` PNGs (61c4f97) are stale for 22 of 25. Every code-drawn fail is `code_fix_needed`; see CODE_FIXES.md.
- **ChatGPT fail:** analogy-fence. Remake prompt `blueprint-analogies__analogy-fence.txt`, queue row 22.


### bp-01-introduction: 14 total, 3 pass, 11 fail

| Asset | Kind | Result | Reason | Fix status |
|---|---|---|---|---|
| style-ref/01M6MSHVNHX3WQH81XS8KQK1HT.png | title-art | PASS | Used only as the GRID BOT BUILDER wordmark crop (WORD_BOX 260,52,760,176 via studio.py wordmark()); the crop is clean logo art with no other text. The full cover must never be shown: it carries 'BY STEWART CROWN', coin logos and price art (studio.py refuses an uncropped draw). | passed as is |
| mascot/blueprint-mascot.png | mascot | PASS | Approved mascot: blob 5d421ae3 equals the approved cut-out /workspace/image-gen-skills/character-sheet/blueprint-mascot.png, identical on d1f6, beginner-images and PR #17 head; matches mascot-sheet-v1 (white/silver body, gloss-black visor, blue eye bar, chest light and antenna ball). Clean alpha, no text. | passed as is |
| blueprint-analogies/analogy-ladder.png | analogy-still | PASS | 'A LADDER = YOUR STEPS': rung = one price step, gap = distance between steps; 1536x1024, margins 68-77px. In the frame the baked tags are re-covered at 28px by code. | passed as is |
| blueprint-analogies/analogy-fence.png | analogy-still | FAIL | Picture reads (top rail, bottom rail, price bouncing between), but the file is 1280x720 and is an older still with code-drawn PIL relabels (label.py), not a single 1536x1024 ChatGPT still. Hard fail: wrong size: 1280x720, not 1536x1024. | needs remake, prompt `blueprint-analogies__analogy-fence.txt` |
| chart/range-2023/hook | code-drawn-chart | FAIL | Footer reads 'Educational content only. Not financial advice.' Otherwise clear: real 90-day window, band 24,930 to 30,331, '16 Oct 28,519' (all match btc-usd-windows.json range_2023). Hard fail: disclaimer not exact. | code fix needed: CF-1 |
| chart/range-2023/a-ladder | code-drawn-chart | FAIL | Footer not exact. Otherwise fine: whole ladder still fitted, 28px tags, 'Not to scale: the chart has 7 levels', seven real levels 24,930 to 30,331. Hard fail: disclaimer not exact. | code fix needed: CF-1 |
| chart/range-2023/the-range | code-drawn-chart | FAIL | Footer not exact. Otherwise fine: real low 24,930 and high 30,331. Hard fail: disclaimer not exact. | code fix needed: CF-1 |
| chart/range-2023/the-levels | code-drawn-chart | FAIL | Footer not exact. Otherwise fine: seven levels, six gaps, 'one gap = about 900' (5,400.34 / 6 = 900.06). Hard fail: disclaimer not exact. | code fix needed: CF-1 |
| chart/range-2023/the-fence | code-drawn-chart | FAIL | Footer not exact. Otherwise fine: whole fence still fitted, connectors end on the rails. Hard fail: disclaimer not exact. | code fix needed: CF-1 |
| chart/range-2023/walk-the-summer | code-drawn-chart | FAIL | Footer not exact; the axis prints 30331/29431/... while the tag and every other frame print 30,331 style; the unwalked path is drawn so faint that the frame reads as an empty chart with one dot. Hard fail: disclaimer not exact; inconsistent figures: axis labels drawn without thousands separators (30331 ... 24930) beside the '19 Jul 29,914' tag. | code fix needed: CF-1, CF-2 |
| chart/breakout-2023/the-stop | code-drawn-chart | FAIL | Footer not exact. Otherwise fine: '23 Oct: leaves 30,331' (first close above, 33,086) and '14 Mar 71,397' match breakout_2023. Hard fail: disclaimer not exact. | code fix needed: CF-1 |
| title-card | title-card | FAIL | Footer not exact. Shows 'Lesson 01 / Introduction' (the lesson title), wordmark and the approved mascot. Hard fail: disclaimer not exact. | code fix needed: CF-1 |
| end-card | end-card | FAIL | Footer not exact. Names the next lesson: 'Lesson 2 / What you are going to need'. Hard fail: disclaimer not exact. | code fix needed: CF-1 |
| thumbnail | thumbnail | FAIL | Footer not exact. 'Your first range' with the real band chart and EXAMPLE pill. Hard fail: disclaimer not exact. | code fix needed: CF-1 |

### bp-02-what-you-need: 11 total, 3 pass, 8 fail

| Asset | Kind | Result | Reason | Fix status |
|---|---|---|---|---|
| style-ref/01M6MSHVNHX3WQH81XS8KQK1HT.png | title-art | PASS | Same wordmark crop as bp-01; clean. | passed as is |
| mascot/blueprint-mascot.png | mascot | PASS | Same approved mascot file as bp-01. | passed as is |
| blueprint-analogies/analogy-list.png | analogy-still | PASS | 'YOUR PLAN CHECKLIST' with Pair / Range / Gaps / Stop rows and plain tags; 1536x1024, margins 65-130px. In the bp-02 hook frame the tags are re-covered at 28px by code. | passed as is |
| chart/range-2023/hook | code-drawn-chart | FAIL | Footer not exact. Otherwise fine: list still fitted, its tags re-covered at 28px, Band 24,930 to 30,331 / Six gaps. About 900 / The close leaves 30,331. Hard fail: disclaimer not exact. | code fix needed: CF-1 |
| chart/range-2023/seven-lines | code-drawn-chart | FAIL | Footer not exact. Otherwise fine: the seven lines in order. Hard fail: disclaimer not exact. | code fix needed: CF-1 |
| chart/range-2023/the-three-words | code-drawn-chart | FAIL | Footer not exact. Otherwise fine: Range / Levels / Stop with real figures. Hard fail: disclaimer not exact. | code fix needed: CF-1 |
| chart/range-2023/no-secrets | code-drawn-chart | FAIL | Footer not exact. Otherwise fine: never vs allowed columns. Hard fail: disclaimer not exact. | code fix needed: CF-1 |
| chart/range-2023/copy-the-path | code-drawn-chart | FAIL | Same walk-chart problems as bp-01 walk-the-summer. Hard fail: disclaimer not exact; inconsistent figures: axis labels without thousands separators beside '19 Jul 29,914'. | code fix needed: CF-1, CF-2 |
| title-card | title-card | FAIL | Footer not exact. Shows 'Lesson 02 / What you are going to need' and the approved mascot. Hard fail: disclaimer not exact. | code fix needed: CF-1 |
| end-card | end-card | FAIL | Footer not exact. Names the next lesson: 'Lesson 3 / What is a grid bot'. Hard fail: disclaimer not exact. | code fix needed: CF-1 |
| thumbnail | thumbnail | FAIL | Footer not exact. Lesson title with the seven-line list. Hard fail: disclaimer not exact. | code fix needed: CF-1 |

### bp-03-what-is-a-grid-bot: 9 total, 2 pass, 7 fail

| Asset | Kind | Result | Reason | Fix status |
|---|---|---|---|---|
| style-ref/01M6MSHVNHX3WQH81XS8KQK1HT.png | title-art | PASS | Same wordmark crop as bp-01; clean. | passed as is |
| mascot/blueprint-mascot.png | mascot | PASS | Same approved mascot file as bp-01. | passed as is |
| chart/range-2023/hook | code-drawn-chart | FAIL | Footer not exact; ticket text too small. Counts are right (5 down-closes through 27,630: 17 Aug, 30 Aug + 3 in October). Hard fail: disclaimer not exact; illegible label: 'BUY 27,630' and '3 more in October' tickets are 22px at 1080p (28px minimum). | code fix needed: CF-1, CF-3 |
| chart/range-2023/limit-orders-wait | code-drawn-chart | FAIL | Footer not exact; 22px tickets; 'A cross is not a receipt' / 'That is not a receipt' is jargon a beginner cannot decode. The 10 crossings are right (5 down, 5 up), but only the 5 down-crosses are marked, so the frame shows 5 marks next to '10 times'. Hard fail: disclaimer not exact; illegible label: 22px tickets. | code fix needed: CF-1, CF-3, CF-4 |
| chart/range-2023/buys-and-sells | code-drawn-chart | FAIL | Footer not exact. Otherwise fine: sells above 27,630 in mint, buys below in blue. Hard fail: disclaimer not exact. | code fix needed: CF-1 |
| chart/range-2023/where-the-path-stood | code-drawn-chart | FAIL | Same walk-chart problems as bp-01 walk-the-summer. Hard fail: disclaimer not exact; inconsistent figures: axis labels without thousands separators beside '19 Jul 29,914'. | code fix needed: CF-1, CF-2 |
| title-card | title-card | FAIL | Footer not exact. Shows 'Lesson 03 / What is a grid bot' and the approved mascot. Hard fail: disclaimer not exact. | code fix needed: CF-1 |
| end-card | end-card | FAIL | Footer not exact. Names 'Lesson 4 / Market regimes' correctly, but the 'Break' mini chart ends only ~10px above the top line, so it reads as touching the band, not leaving it. Hard fail: disclaimer not exact. | code fix needed: CF-1, CF-5 |
| thumbnail | thumbnail | FAIL | Footer not exact. Lesson title with the band chart and 'BUY 27,630' level. Hard fail: disclaimer not exact. | code fix needed: CF-1 |


## Remake round 1: 13 BP-01/02 ChatGPT web renders (scored 14 Nov against the fbb3f9c narration and the current prompts)

Same strict standard: at least 4 in every category, no hard fails, margins of at least 45px measured on bright pixels (all 13 are 74px or more), spelling checked at zoom with no errors. None has an exchange name, entity branding, mascot, or bot sentence or product pitch. Both disclaimer cards say exactly "Education only. Not financial advice." The BP-01 outro names "What you are going to need" exactly.

| Still | File | Result | Reason | Status |
|---|---|---|---|---|
| bp-01-introduction 001 | `web1` | PASS | Two dashed lines with a zig-zag whose every peak touches the top line and every trough the bottom line, never leaving the band. "Top price", "Bottom price", "Price bouncing" each have one arrow with the tip on its target (3 of 3). EXAMPLE stamp inside the card (slightly tilted), no stray arrow. Plain headline PRICE OFTEN GOES SIDEWAYS matches the beat. | committed at course/images/bp-01-introduction/001.png, source chatgpt-web |
| bp-01-introduction 002 | `web1` | PASS | Disclaimer card reads exactly "Education only." / "Not financial advice." beside an open book with a check. No buy button, no extra words, 0 arrows. | committed at course/images/bp-01-introduction/002.png, source chatgpt-web |
| bp-01-introduction 007 | `web1` | FAIL | The three mint and three blue rungs sit side by side at one height, so each side reads as three orders at the same price, not a ladder of levels. The narration says four buys below and four sells above. The "Sell orders above" tip stops below and left of the first mint rung instead of touching the middle one, and the "Buy orders below" arrow has a kink. Hard fails: wrong picture: orders side by side at one price; arrow misses target. | stays in queue; prompt now v2 (v1 in _superseded/) |
| bp-01-introduction 010 | `web3` | PASS | 11 equal glass stones rising left to right; the first glows with a cyan pin. "You are here" tip on the pin, "10 lessons ahead" tip on the 11th stone (2 of 2). No numbers or icons on the stones. Matches "this introduction is only the first square". | committed at course/images/bp-01-introduction/010.png, source chatgpt-web |
| bp-01-introduction 016 | `web1` | FAIL | The rectangle has 4 inner lines where the prompt says 5. The "Levels" tip lands in the gap halfway between the 2nd and 3rd inner lines (measured 34px from each), touching no rung, so it doesn't show that the levels are the rungs. "Range" (top edge) and "Stop" (amber sign) are correct; "Point at each one" has no arrow, as specified. Hard fails: arrow misses target; wrong count. | stays in queue; prompt now v2 (v1 in _superseded/) |
| bp-01-introduction 018 | `web1` | PASS | Outro: headline NEXT: WHAT YOU ARE GOING TO NEED, tag "Next lesson: What you are going to need", which is the exact BP-02 title. Notebook card, then a thick arrow, then a clipboard with three empty boxes. "Bring your notes" tip on the notebook, next-lesson tip on the clipboard (2 of 2). | committed at course/images/bp-01-introduction/018.png, source chatgpt-web |
| bp-02-what-you-need 002 | `web1` | PASS | Disclaimer card reads exactly "Education only." / "Not financial advice." beside an open book with a check. Nothing else on the card, 0 arrows. | committed at course/images/bp-02-what-you-need/002.png, source chatgpt-web |
| bp-02-what-you-need 003 | `web1` | PASS | Title card shows the exact lesson title WHAT YOU ARE GOING TO NEED. Desk with notebook, pencil and a laptop showing only a shield with a check (no app screen). "Notebook", "Pencil", "Practice account" tips on target (3 of 3). Desk edges are about 112px from the frame edges (the prompt asks 120, the standard 45). | committed at course/images/bp-02-what-you-need/003.png, source chatgpt-web |
| bp-02-what-you-need 004 | `web3` | PASS | Clipboard with exactly 7 rows spelled as specified (Notebook, The three words, Pair name, Paper or demo, No secrets, Written stop, The word EXAMPLE); row 4 is highlighted; no ticks. "7 lines to check" tip on the clipboard edge at row 1 (1 of 1). Matches the beat's seven lines word for word. | committed at course/images/bp-02-what-you-need/004.png, source chatgpt-web |
| bp-02-what-you-need 010 | `web1` | PASS | Notebook rows: a sketched band, then a placeholder pair "___ / ___", each followed by an EXAMPLE stamp. "Stamp it EXAMPLE" tip on the first stamp (1 of 1); "So nobody copies it as advice" under the page with no arrow. Pencil fully in frame. | committed at course/images/bp-02-what-you-need/010.png, source chatgpt-web |
| bp-02-what-you-need 016 | `web1` | PASS | Notebook with exactly 7 tick-box rows; first box ticked with the pencil tip on it. "Tick each one" tip on the first box. "Copy the 7 lines" points at row 4, but its tip sits 16px above that line (measured): it clearly reads as row 4, so I scored it 4, not a miss. Tag is 230px inside the right edge. | committed at course/images/bp-02-what-you-need/016.png, source chatgpt-web |
| bp-02-what-you-need 018 | `web1` | PASS | Paper page with two empty circles joined by a slash and a blue EXAMPLE stamp under them; pencil beside it. "Thing you buy" tip on the left circle, "What you pay with" tip on the right circle (2 of 2). Matches the pair-name practice (two empty tags joined by a slash). | committed at course/images/bp-02-what-you-need/018.png, source chatgpt-web |
| bp-02-what-you-need 019 | `web1` | PASS | Recap: three cards (speech bubble, sketched band, written line with a check) with tags "1 Say the hook", "2 Name your drawing", "3 Name your line", 0 arrows. Matches "say the hook, name the diagram you drew, name the line you wrote". | committed at course/images/bp-02-what-you-need/019.png, source chatgpt-web |

Passes were saved to `out/course/images/<lesson>/NNN.png` (already 1536x1024, so no fill was needed) and committed at `course/images/<lesson>/NNN.png`. Their rows carry the scores, `pass: true`, `source: chatgpt-web`, `scored_blob` and `previous_committed_blob`. The two fails keep the old still and a `remake_review` block.

**Running counts (script stills):** BP-01 16/18, BP-02 21/21, BP-03 11/19. Whole 92-row list: 56/92.
