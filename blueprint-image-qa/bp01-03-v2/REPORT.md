# BP-01..BP-03 image QA v2 (strict first scoring)

Scored by Creative Studio, 14 Nov 2026 (WITA). Same strict method as bp04-11. Image scoring only: no verdict on the BP-01..03 videos.

**Scope:** image fields of course/scripts/bp-01..bp-03 @ d1f6 `fbb3f9c` (58 stills); files scored from cursor/blueprint-beginner-images `2f8bac1`.

**Result (current, 14 Nov after remake round 3 and the strict arrow re-check):** lesson stills 53 pass / 5 fail of 58. Shared + code-drawn: 33 pass / 1 fail of 34. Whole list: **86 pass / 6 fail of 92**. Remake queue: 5 (needs_mascot_ref: 0). Code fix needed: 1 frame (CF-7), plus CF-6 to apply with the new fence still. See CODE_FIXES.md. (History: first scoring 45/47; after round 1 56/36.)

**Mismatches:** none. All 58 blobs are identical on d1f6 and beginner-images and match the v10 pass list's scored_blob. All 58 were 'pass' on v10; 21 are overturned here.

**Other finding:** the numbers files (d1f6) set the on-screen disclaimer to 'Educational content only. Not financial advice.', which is not the exact line (CODE_FIXES.md CF-1).

**Fix status:** every fail = `needs_remake`, prompt written (specs/remake/<lesson>__NNN.txt, copied to remake/), not regenerated. Old prompts moved to specs/remake/_superseded/: `bp-01-introduction__010.v1.txt`, `bp-02-what-you-need__004.v1.txt`, `bp-03-what-is-a-grid-bot__003.v1.txt`, `bp-03-what-is-a-grid-bot__010.v1.txt`.


## bp-01-introduction (Introduction): 18 total, 15 pass, 3 fail (after round 3 + strict arrow re-check; table below is the first scoring of the committed stills)

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

## bp-02-what-you-need (What you are going to need): 21 total, 20 pass, 1 fail (after strict arrow re-check; table below is the first scoring of the committed stills)

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

## bp-03-what-is-a-grid-bot (What is a grid bot): 19 total, 18 pass, 1 fail (after remake round 2; table below is the first scoring of the committed stills)

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


### bp-01-introduction: 14 total, 14 pass, 0 fail (after round 2 + e0b84d5; table below is the first scoring)

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

### bp-02-what-you-need: 11 total, 11 pass, 0 fail (after e0b84d5; table below is the first scoring)

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

### bp-03-what-is-a-grid-bot: 9 total, 8 pass, 1 fail (after e0b84d5; table below is the first scoring)

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

## Remake round 2: 8 BP-03 ChatGPT web renders + analogy-fence (scored 14 Nov against the fbb3f9c narration and the current prompts)

Each file is 1536x1024. The margin is measured on bright pixels (at least 45px required).

| File | Result | Margins L/R/T/B | Reason | Status |
|---|---|---|---|---|
| gen/bp-03-what-is-a-grid-bot/001/web1.png | PASS | 80/107/71/172 | Crossed crystal ball (amber X) beside one card with a four-rung ladder: two mint tickets on the top two rungs, two blue on the bottom two, dashed price line between rung 2 and 3, so sells sit only above and buys only below. "Not a fortune teller" tip touches the top of the ball; "Orders waiting at set prices" tip touches the top mint ticket (2 of 2). EXAMPLE stamp inside the card. Headline A GRID BOT DOES NOT GUESS is plain and puts no thinking in the bot. Spelling clean. | placed at course/images/bp-03-what-is-a-grid-bot/001.png (blob 93dd60c4) |
| gen/bp-03-what-is-a-grid-bot/002/web1.png | PASS | 84/85/86/267 | Disclaimer card reads exactly "Education only." / "Not financial advice." in two large lines, open book with a check, nothing else on the card. Headline EDUCATION ONLY. Spelling clean. | placed at course/images/bp-03-what-is-a-grid-bot/002.png (blob 55ae0f32) |
| gen/bp-03-what-is-a-grid-bot/003/web1.png | PASS | 76/141/50/112 | Title card: headline WHAT IS A GRID BOT? matches the lesson title "What is a grid bot". Six-rung ladder: three mint tickets above the dashed line, three blue below. "Sell orders above" tip on the middle mint ticket, "Buy orders below" tip on the middle blue ticket (2 of 2); "Orders wait at prices you chose" has no arrow (sits along the bottom inside the card rather than under it, clear of the rails). EXAMPLE stamp inside the card. Headline top edge 50px (>=45). | placed at course/images/bp-03-what-is-a-grid-bot/003.png (blob 03d652a8) |
| gen/bp-03-what-is-a-grid-bot/004/web1.png | PASS | 70/83/87/160 | Box with a top edge, bottom edge and three inner lines; three-disc pile left; amber line under the box. All 5 arrows land: Upper on the middle of the top edge, Levels on the second inner line, Lower on the bottom edge (at its right-hand corner, hence 4), Side: what you hold on the disc pile, Stop on the amber line. Each tag touches the part it names, as the beat says. Spelling clean. | placed at course/images/bp-03-what-is-a-grid-bot/004.png (blob 30004d39) |
| gen/bp-03-what-is-a-grid-bot/008/web1.png | PASS | 79/79/81/158 | Left card: price weaves inside the band, blue and mint boxes the same height. Right card: price drops out through the bottom line and stays below; one tall blue box and a nearly empty mint box. Captions "Inside the band: balanced" and "Price left: one side piles up" with no arrows, as specified. EXAMPLE stamp inside the right card. No coins or currency. | placed at course/images/bp-03-what-is-a-grid-bot/008.png (blob cbaf79a4) |
| gen/bp-03-what-is-a-grid-bot/010/web1.png | FAIL | 0/110/136/60 | Five tiles spelled right, Levels highlighted, "The one people skip" arrow lands on the third tile. But the pencil runs off the frame at the bottom-left (0px margin, the prompt asks 80px for pencils) and its tip pokes into the "Upper" tile, with a thin glow streak rising from the tip into the letter p. The pencil does not lie under the row as asked. Hard fail: cramped margin: pencil runs off the left and bottom frame edges (0px); AI artifact: light streak from the pencil tip into the "Upper" tile. | stays in queue; v3 prompt `bp-03-what-is-a-grid-bot__010.txt` (v2 moved to `_superseded/`), target web3.png |
| gen/bp-03-what-is-a-grid-bot/014/web1.png | PASS | 48/49/126/252 | Four icons in one panel joined by three short arrows: two checked tickets, a zig-zag between dashed lines, an amber stop sign, blue and mint jars. Captions "Orders wait", "Inside your range", "Stop written", "Holdings change" match the one-breath definition. Panel glow sits 48px/49px from the left/right edges: inside the 45px standard but short of the prompt's 120px ask, hence composition 4. | placed at course/images/bp-03-what-is-a-grid-bot/014.png (blob 56cc2b82) |
| gen/bp-03-what-is-a-grid-bot/019/web1.png | PASS | 78/65/101/212 | Outro: headline NEXT: MARKET REGIMES and tag "Next lesson: Market regimes" name the next lesson's exact title. "Bring your notes" tip on the notebook, "Next lesson" tip on the right card (2 of 2). Three panels: sideways zig-zag between two lines, steady climb, bounce then break out above the top line and stay above. One thick arrow between the cards. | placed at course/images/bp-03-what-is-a-grid-bot/019.png (blob 44c3c90a) |
| gen/blueprint-analogies/analogy-fence/web1.png | PASS | 74/66/104/190 | Two posts, exactly two rails, cyan zig-zag whose every peak touches the underside of the top rail and every trough the top of the bottom rail, never crossing a rail. 3 of 3 arrows land: "Top rail = top price" on the top rail, "Bottom rail = bottom price" on the bottom rail, "Price bounces between" on the zig-zag midway. No digits, no mascot, no branding. Teaches on its own without code labels: yes. Posts have a wood-grain texture (craft 4). Label lettering is about 35px cap height (about 42px with descenders), short of the prompt's 52px: in the masters' 840x472 panel (scale 0.461) that is about 16px, below the 28px floor, so the CF-6 cover labels must stay and be retuned (text legibility 4). | placed at course/images/blueprint-analogies/analogy-fence.png (blob a8b3633d); CF-6 relabel still to apply in studio.py |

The 010 web1 is the first image of a 2-image ChatGPT series, and it was judged on its own. The web2.png in that folder was not scored.

## Code-drawn frames re-scored at PR #17 head e0b84d5 (CF-1..CF-5 applied)

These are the committed PNGs under blueprint-smoke/code-drawn/ at e0b84d5, and scored_blob is the committed blob. A scratch `--frames` export at e0b84d5 matches pixel for pixel, except the mascot box, which is gated on the pass list. Numbers were checked against course/data/public-prices/btc-usd-windows.json: band low 24,930.30, high 30,330.64, step 900.06; 19 Jul 29,913.92; 16 Oct 28,519.47; 23 Oct 33,086.23 (the first close above 30,331); 14 Mar 71,396.59; 27,630 crossed 10 times (5 down, 5 up).

| Frame | Result | Reason | Fix |
|---|---|---|---|
| bp-01-introduction/chart/range-2023/hook | PASS | Footer now exactly "Education only. Not financial advice." (CF-1). Real 90-day window 19 July to 16 October 2023, band 24,930 to 30,331 (min low 24,930.30, max high 30,330.64), "16 Oct 28,519" (close 28,519.47), all from btc-usd-windows.json range_2023. | none |
| bp-01-introduction/chart/range-2023/a-ladder | PASS | CF-1 footer exact. Ladder still fitted whole, 28px cover tags, "Not to scale: the chart has 7 levels", seven real levels 24,930 to 30,331 (step 900.06). | none |
| bp-01-introduction/chart/range-2023/the-range | PASS | CF-1 footer exact. Real low 24,930 and high 30,331, 16 Oct 28,519. | none |
| bp-01-introduction/chart/range-2023/the-levels | PASS | CF-1 footer exact. Seven lines 24,930 / 25,830 / 26,730 / 27,630 / 28,531 / 29,431 / 30,331, "one gap = about 900" (5,400.34 / 6 = 900.06). | none |
| bp-01-introduction/chart/range-2023/the-fence | PASS | CF-1 footer exact; connectors end on the rails. This frame still embeds the OLD 1280x720 fence still (the only one on d1f6 at e0b84d5) and its CF-6 cover boxes are still tuned to it, so it is correct as committed. CF-6 is NOT applied yet: once the new 1536x1024 fence still lands on d1f6, apply CF-6 and re-render and re-score this frame. | CF-6 (pending the new fence still) |
| bp-01-introduction/chart/range-2023/walk-the-summer | PASS | CF-1 footer exact. CF-2 verified: the axis now reads 30,331 / 29,431 / 28,531 / 27,630 / 26,730 / 25,830 / 24,930 with commas, and the unwalked path is drawn at alpha 150, width 2, so the whole summer path is visible. "19 Jul 29,914" = close 29,913.92. | none |
| bp-01-introduction/chart/breakout-2023/the-stop | PASS | CF-1 footer exact. "23 Oct: leaves 30,331" (first close above, 33,086.23) and "14 Mar 71,397" (close 71,396.59) match breakout_2023. | none |
| bp-01-introduction/title-card | PASS | CF-1 footer exact. "Lesson 01 / Introduction" = lesson title; wordmark; approved mascot (course/images/mascot/blueprint-mascot.png blob 5d421ae3, unchanged); band chart with EXAMPLE pill. | none |
| bp-01-introduction/end-card | PASS | CF-1 footer exact. Names the next lesson exactly: "Lesson 2 / What you are going to need"; approved mascot. | none |
| bp-01-introduction/thumbnail | PASS | CF-1 footer exact (paint.py thumbnail template). "Your first range" with the real band and EXAMPLE pill. | none |
| bp-02-what-you-need/chart/range-2023/hook | PASS | CF-1 footer exact. List still fitted, its tags re-covered at 28px; Band 24,930 to 30,331 / Six gaps. About 900. / The close leaves 30,331. with EXAMPLE. | none |
| bp-02-what-you-need/chart/range-2023/seven-lines | PASS | CF-1 footer exact. The seven lines in order, plain words. | none |
| bp-02-what-you-need/chart/range-2023/the-three-words | PASS | CF-1 footer exact. Range 24,930 to 30,331 / Levels six gaps about 900 / Stop leaves 30,331, EXAMPLE pill. | none |
| bp-02-what-you-need/chart/range-2023/no-secrets | PASS | CF-1 footer exact. Never (seed phrase, private key, API secret, account balance) vs allowed columns. | none |
| bp-02-what-you-need/chart/range-2023/copy-the-path | PASS | CF-1 footer exact. CF-2 verified: comma axis labels and the visible unwalked path; 19 Jul 29,914. | none |
| bp-02-what-you-need/title-card | PASS | CF-1 footer exact. "Lesson 02 / What you are going to need" = lesson title; approved mascot. | none |
| bp-02-what-you-need/end-card | PASS | CF-1 footer exact. Names the next lesson exactly: "Lesson 3 / What is a grid bot"; BUY 27,630 band chart with EXAMPLE; approved mascot. | none |
| bp-02-what-you-need/thumbnail | PASS | CF-1 footer exact. Lesson title with the seven-line list. | none |
| bp-03-what-is-a-grid-bot/chart/range-2023/hook | PASS | CF-1 footer exact. CF-3 verified: tickets drawn at 28px on 42px tags. Two BUY 27,630 tickets (17 Aug, 30 Aug) plus "3 more in October" with 3 dots = the 5 down-closes through 27,630 (17 Aug, 30 Aug, 2/5/9 Oct). Caption makes no count claim. | none |
| bp-03-what-is-a-grid-bot/chart/range-2023/limit-orders-wait | FAIL | CF-1 footer exact. CF-3 verified (28px tickets). CF-4 verified: subtitle "A buy order waits at 27,630. A cross is not a filled order." and caption "Daily closes crossed 27,630 10 times. A cross is not a filled order." No jargon left. Still failing on count: the caption (and VO) say 10 crosses, which is right (5 down: 17 Aug, 30 Aug, 2/5/9 Oct; 5 up: 29 Aug, 1/4/6/16 Oct), but the frame marks only the 5 down-crosses (2 BUY tickets + "3 more in October" dots). A beginner counts 5 marks next to "10 times". Stage 2 noted this but CODE_FIXES had no fix for it; now CF-7. | CF-7 |
| bp-03-what-is-a-grid-bot/chart/range-2023/buys-and-sells | PASS | CF-1 footer exact. 30,331/29,431/28,531 sell, 27,630 middle, 26,730/25,830/24,930 buy; sells above in mint, buys below in blue. | none |
| bp-03-what-is-a-grid-bot/chart/range-2023/where-the-path-stood | PASS | CF-1 footer exact. CF-2 verified: comma axis labels, visible unwalked path; 19 Jul 29,914. | none |
| bp-03-what-is-a-grid-bot/title-card | PASS | CF-1 footer exact. "Lesson 03 / What is a grid bot" = lesson title; approved mascot; BUY 27,630 band chart with EXAMPLE. | none |
| bp-03-what-is-a-grid-bot/end-card | PASS | CF-1 footer exact. Names "Lesson 4 / Market regimes" exactly. CF-5 verified: the Break panel path cuts through the top line and finishes about 80px above it, so it clearly leaves the band. | none |
| bp-03-what-is-a-grid-bot/thumbnail | PASS | CF-1 footer exact. "What is a grid bot" with the band chart and BUY 27,630 level. | none |

Disclaimer string sweep at e0b84d5: Blueprint code and yaml no longer contain "Educational content only" (studio.py, build_numbers.py, numbers/*.yaml, captions, lesson_scripts.py, pack/paint.py). It is still in two old committed smoke outputs, `blueprint-smoke/bp-01-introduction.yaml` and `bp-01-wrong-number.yaml`, which no frame reads, and in non-Blueprint files (brand.py, video-qa-review skill, production-pipeline, defi-program).

### Running counts after round 2 and e0b84d5

| Lesson | Script stills | Shared + code-drawn | All rows | Rows left |
|---|---|---|---|---|
| bp-01-introduction | 16/18 | 14/14 | 30/32 | 007.png and 016.png (ChatGPT, v2 prompts) |
| bp-02-what-you-need | 21/21 | 11/11 | 32/32 | none: 100% |
| bp-03-what-is-a-grid-bot | 18/19 | 8/9 | 26/28 | 010.png (ChatGPT, v3 prompt) and code-drawn chart/range-2023/limit-orders-wait (CF-7) |
| **All** | 55/58 | 33/34 | **88/92** | 4 |

## Remake round 3: bp-01 007 and 016 web2 (scored 14 Nov against the fbb3f9c narration and the v2 prompts)

| File | Result | Margins | Reason |
|---|---|---|---|
| gen/bp-01-introduction/007/web2.png | FAIL | 76/77/69/141 | Ladder is now right: four mint rungs above and four blue rungs below the dashed "Price now" line, evenly spaced, one dot each; headline and tags spelled right; EXAMPLE inside the card; 3 arrows. But the "Buy orders below" arrow ends in the empty gap between the 2nd and 3rd blue rungs (about 32px from each), touching no rung, while "Sell orders above" lands on its rung end. Same miss class as v1/016 v1. Hard fail: label arrow misses its target: "Buy orders below" tip stops in the empty gap between the 2nd and 3rd blue rungs. Next: web3.png on the v3 prompt (old prompt in specs/remake/_superseded/bp-01-introduction__007.v2.txt). |
| gen/bp-01-introduction/016/web2.png | PASS | 64/60/69/124 | Notebook rectangle has exactly 5 inner lines (7 counting top and bottom). "Range" tip on the middle of the top edge, "Levels" tip on the right end of the 3rd inner line, "Stop" tip on the amber STOP sign, "Point at each one" has no arrow (3 of 3). Pencil and notebook fully inside, bottom margin 124px. Matches fbb3f9c beat 16 (Range / Levels / Stop). |

016 was saved to `out/course/images/bp-01-introduction/016.png` and committed at `course/images/bp-01-introduction/016.png` (row: `source: chatgpt-web`, new `scored_blob`, web1 review kept in `previous_remake_reviews`). 007 keeps the old committed still and stays in the queue with target web3 on the v3 prompt (v2 moved to `specs/remake/_superseded/bp-01-introduction__007.v2.txt`).

### Running counts after round 3

| Lesson | Script stills | Shared + code-drawn | All rows | Rows left |
|---|---|---|---|---|
| bp-01-introduction | 17/18 | 14/14 | 31/32 | 007.png (ChatGPT, v3 prompt, web3) |
| bp-02-what-you-need | 21/21 | 11/11 | 32/32 | none: 100% |
| bp-03-what-is-a-grid-bot | 18/19 | 8/9 | 26/28 | 010.png (ChatGPT, v3 prompt, web3) and code-drawn chart/range-2023/limit-orders-wait (CF-7) |
| **All** | 56/58 | 33/34 | **89/92** | 3 |

## Strict arrow re-check (14 Nov): a tip must touch its target

Stewart's rule for the perfect run: every label arrow's point must touch the thing it names. A gap of a few pixels fails ("arrow tip stops short of target"). I zoomed (4-8x) into every label-arrow tip on every passed ChatGPT-web remake: bp-01 001/002/010/016/018, bp-02 002/003/004/010/016/018/019, bp-03 001/002/003/004/008/014/019 and analogy-fence. Rows whose prompt has 0 label arrows had nothing to check.

Flipped back to fail. The old committed still is restored at `course/images/` and `out/`, the passed render is kept in `remake_review` / `flipped_from_pass`, and the row is back in the queue on a new prompt that pins the tip:

| Row | Arrow that misses | Next |
|---|---|---|
| bp-01-introduction/001.png | "Price bouncing" tip stops about 9px short of the zig-zag line | web2, v2 prompt |
| bp-01-introduction/010.png | "You are here" tip stops about 6px above the location pin | web4, v3 prompt |
| bp-02-what-you-need/016.png | "Copy the 7 lines" tip ends in the gap above a row line, touching none (prompt: the fourth row line) | web2, v2 prompt |

Checked and touching: bp-01 001 Top/Bottom price, 010 "10 lessons ahead", 016 Range/Levels/Stop, 018 both; bp-02 003 all 3, 004, 010, 016 "Tick each one", 018 both circles; bp-03 001 both, 003 both, 004 all 5 (Stop tip enters the amber line's glow), 019 both; analogy-fence all 3 (the "Price bounces between" arrowhead overlaps the zig-zag stroke).

Not covered: arrows between two panels (sequence arrows such as notebook -> next card) connect panels and have no single target, so they are not treated as label arrows. Committed stills that passed at first scoring and were never remade, and the code-drawn frames, were outside this re-check.

### Running counts after the strict arrow re-check

| Lesson | Script stills | Shared + code-drawn | All rows | Rows left |
|---|---|---|---|---|
| bp-01-introduction | 15/18 | 14/14 | 29/32 | 001.png (web2, v2), 007.png (web3, v3), 010.png (web4, v3) |
| bp-02-what-you-need | 20/21 | 11/11 | 31/32 | 016.png (web2, v2) |
| bp-03-what-is-a-grid-bot | 18/19 | 8/9 | 26/28 | 010.png (web3, v3) and code-drawn chart/range-2023/limit-orders-wait (CF-7) |
| **All** | 53/58 | 33/34 | **86/92** | 6 |

---

## Update — code-drawn arrow sweep re-scored at 29b7444 (CF-6 + CF-7 landed on d1f6)

CF-6 and CF-7 landed on `cursor/blueprint-professional-rebuild-d1f6` at `29b74447505ee5f10e9fbd88ee912b0f98348edc`. Used `29b7444` as the code-drawn source for the whole arrow sweep. Of the 25 code-drawn frames, only the two CF frames changed blob vs e0b84d5; the other 23 are byte-identical, so their e0b84d5 scores stand (source tag updated to `code-drawn@29b7444`).

**the-fence** (bp-01) — re-scored at 29b7444, `scored_blob a18534c2`, source `code-drawn@29b7444`. CF-6 applied: re-rendered fence still with retuned labels. Arrow sweep (4–8x): "Top rail = top price" tip touches the top rail; "Price bounces between" tip touches a zigzag peak; "Bottom rail = bottom price" tip touches the bottom rail — no gaps. Disclaimer exact "Education only. Not financial advice." EXAMPLE present. Numbers match btc-usd-windows.json. 1920×1080 (normal for a code frame). **PASS.**

**limit-orders-wait** (bp-03) — re-scored at 29b7444, `scored_blob 0e4767e7`, source `code-drawn@29b7444`. CF-7 applied: frame now marks all 10 crosses (5 down + 5 up as rings), caption "10 crosses: 5 down, 5 up (rings)". Count now matches "Daily closes crossed 27,630 10 times". BUY-27,630 leader touches its ring; ring markers sit on the 27,630 line. Disclaimer exact. EXAMPLE present. **PASS — flipped from the e0b84d5 fail** (which failed on wrong count + no CF for it). No new CF item needed; CF-7 resolves it.

All 25 code-drawn frames now pass.

### d1f6 / beginner-images drift check (files at 29b7444 vs beginner-images pass-list blob)
5 rows differed; 2 are the CF frames resolved by this update (now scored at 29b7444). The remaining **3 genuine drifts** are BP-01 stills that the beginner-images pass list has flipped/replaced but d1f6 has not yet reconciled:

- `course/images/bp-01-introduction/001.png` — beginner-images `295ac01f` (old still restored after arrow-rule fail), d1f6@29b7444 `372a2558` (the arrow-failing remake). d1f6 still carries the remake this pass list rejected.
- `course/images/bp-01-introduction/010.png` — beginner-images `c2905476` (old still restored), d1f6@29b7444 `dc559613` (arrow-failing remake). Same situation.
- `course/images/bp-01-introduction/016.png` — beginner-images `d65e2d7e` (passing web2 remake, PASS), d1f6@29b7444 `330ae5ca` (different/older blob). d1f6 has not picked up the passing 016 remake.

Orchestrator should reconcile d1f6 to match the beginner-images pass list for these 3 rows.

### Counts after this update
- BP-01: **29/32** — NOT 100% (fail: 001, 007, 010)
- BP-02: **31/32** — NOT 100% (fail: 016)
- BP-03: **27/28** — NOT 100% (fail: 010)
- TOTAL: **87/92**

---

## Run on top of 8f21533 — close gaps + bp-03 010 v3

**bp-02 021 flipped to FAIL (panel-connector arrow rule).** Measured the next->grid transition arrow at full resolution: arrowhead tip x=745, grid-card left border x=761 -> 17px gap. Doubt=fail for a perfect run. Committed still unchanged (never remade); first remake prompt written (`specs/remake/bp-02-what-you-need__021.txt`) pinning the transition arrow and both label arrows to touch their targets; queued at web1.

**bp-03 010 web3 (v3) PASS.** Five word tiles spelled exactly Upper / Lower / Levels / Side / Stop (matches beat 10 "upper, lower, levels, side, stop"); third tile (Levels) highlighted; "The one people skip" arrow tip touches the top edge of the Levels tile (verified 4-8x). No digits, on-brand, pencil whole-in-frame with no glow streak. Placed; removed from queue. **This completes BP-03: 28/28 = 100%.**

### Updated counts (92-row list)
- **BP-01: 29/32 — NOT 100%.** Rows left: 001, 007, 010 (the three genuine d1f6/beginner-images drifts flagged for Orchestrator reconciliation + the tip-pinned remakes).
- **BP-02: 30/32 — NOT 100%.** Rows left: 016 (back to old still, queued), 021 (flipped this run).
- **BP-03: 28/28 — YES, 100%.**
- **92-row total: 87/92.**

---

## Run on top of 57e0aeb — 14 Nov 2026 (WITA): remake scoring for BP-01 001/007/010 and BP-02 016

Same perfect-run rules (every category at least 4/5, no hard fails; every arrow tip, panel connectors included, must visibly touch its target; doubt = fail). These renders used the prompts current when the batch started and were scored on their own merits against the beat.

| File | Result | Margins (l/r/t/b) | Reason |
|---|---|---|---|
| gen/bp-01-introduction/001/web2.png | FAIL | 78/80/86/162 | Teaching and EXAMPLE otherwise good, but "Top price" tip stops short of the top dashed line and "Price bouncing" tip stops short of the zig-zag (clear dark gaps). Next: web3.png on the v3 prompt (v2 moved to specs/remake/_superseded/bp-01-introduction__001.v2.txt). |
| gen/bp-01-introduction/007/web3.png | FAIL | 67/95/79/126 | Ladder is now right (4 mint above, 4 blue below, Buy aligned to the 2nd blue rung), but all 3 arrow tips stop short of their targets (sell ~8-9px, price-now ~11px, buy the same class). Next: web4.png on the v4 prompt (v3 superseded). |
| gen/bp-01-introduction/010/web4.png | PASS | 66/61/117/263 | 11 stones (pin + 10). "You are here" tip on the pin; "10 lessons ahead" tip on the last stone. Headline spaced; no EXAMPLE required. Placed at out/ and course/images/bp-01-introduction/010.png (`source: chatgpt-web`, scored_blob 4a3146c57f1ef4a8a2e624adb3f25af075d80155). Removed from the queue. |
| gen/bp-02-what-you-need/016/web2.png | FAIL | 81/58/77/99 | Seven boxes/lines are present, but "Tick each one" tip stops short of the checkbox and "Copy the 7 lines" tip ends in the paper margin / gap, touching no row line. Next: web3.png on the v3 prompt (v2 superseded). |

021 was not in this batch and stays queued at web1 (another job is writing it).

### Updated counts (92-row list)
- **BP-01: 30/32 — NOT 100%.** Rows left: 001 (web3, v3), 007 (web4, v4).
- **BP-02: 30/32 — NOT 100%.** Rows left: 016 (web3, v3), 021 (web1, untouched this run).
- **BP-03: 28/28 — YES, 100%.**
- **92-row total: 88/92.**
- ChatGPT queue (BP-01..03): 4 — bp-01-introduction/001 (gen/bp-01-introduction/001/web3.png), bp-01-introduction/007 (gen/bp-01-introduction/007/web4.png), bp-02-what-you-need/016 (gen/bp-02-what-you-need/016/web3.png), bp-02-what-you-need/021 (gen/bp-02-what-you-need/021/web1.png).


---

## Run on top of 4bfe3e6 — 14 Nov 2026 (WITA): remake scoring for BP-02 021

Same perfect-run rules (every category at least 4/5, no hard fails; every arrow tip, panel connectors included, must visibly touch its target; doubt = fail). These renders used the prompts current when the batch started and were scored on their own merits against the beat. Mismatch check: the image depicts its own prompt and beat (no tab-order swap).

| File | Result | Margins (l/r/t/b) | Reason |
|---|---|---|---|
| gen/bp-02-what-you-need/021/web1.png | FAIL | 79/90/88/183 | Headline and outro title are exact, and the two label arrows touch, but the scene-transition arrow still stops short of the grid card (visible navy gap, about 20-24px). Next: web2.png on the v3 prompt (v2 moved to specs/remake/_superseded/bp-02-what-you-need__021.v2.txt). |

001, 007 and 016 were not in this batch and stay queued.

### Updated counts (92-row list)
- **BP-01: 30/32 — NOT 100%.** Rows left: 001 (web3, v3), 007 (web4, v4).
- **BP-02: 30/32 — NOT 100%.** Rows left: 016 (web3, v3), 021 (web2, v3).
- **BP-03: 28/28 — YES, 100%.**
- **92-row total: 88/92.**
- ChatGPT queue (BP-01..03): 4 — bp-01-introduction/001 (gen/bp-01-introduction/001/web3.png), bp-01-introduction/007 (gen/bp-01-introduction/007/web4.png), bp-02-what-you-need/016 (gen/bp-02-what-you-need/016/web3.png), bp-02-what-you-need/021 (gen/bp-02-what-you-need/021/web2.png).


---

## Run on top of 0cc141a — 14 Nov 2026 (WITA): remake scoring for BP-01 001/007 and BP-02 016

Same perfect-run rules (every category at least 4/5, no hard fails; every arrow tip, panel connectors included, must visibly touch its target; doubt = fail). These renders used the prompts current when the batch started and were scored on their own merits against the beat. Headlines match their jobs; no mismatches.

| File | Result | Margins (l/r/t/b) | Reason |
|---|---|---|---|
| gen/bp-01-introduction/001/web3.png | PASS | 72/97/89/178 | All three tips now touch (Top price on the top dashed line, Bottom price on the bottom dashed line, Price bouncing on a rising zig-zag stroke). Peaks and troughs meet the dashed lines. Headline spaced; EXAMPLE present. Placed at out/ and course/images/bp-01-introduction/001.png (`source: chatgpt-web`, scored_blob 13c35d1ceb928a1ee7e4cf884583e1d45d91c480). Removed from the queue. |
| gen/bp-01-introduction/007/web4.png | FAIL | 79/94/69/137 | Ladder is correct (4 mint above, 4 blue below, one dot each; tags at the right heights). 'Price now' and 'Buy orders below' tips now touch. But 'Sell orders above' still stops short of the left end of the second mint rung (visible navy gap, about 4-8px). Next: web5.png on the v5 prompt (v4 moved to specs/remake/_superseded/bp-01-introduction__007.v4.txt). |
| gen/bp-02-what-you-need/016/web3.png | PASS | 68/53/67/114 | Seven boxes and seven lines; first box ticked; pencil on the page. 'Tick each one' tip on the first tick box; 'Copy the 7 lines' tip on the fourth row line. Headline spaced. Placed (`scored_blob` 7849a509812a57a068bf066370625c7d7ded397c). Removed from the queue. |

021 was not in this batch and stays queued at web2/v3.

### Updated counts (92-row list)
- **BP-01: 31/32 — NOT 100%.** Rows left: 007 (web5, v5).
- **BP-02: 31/32 — NOT 100%.** Rows left: 021 (web2, v3).
- **BP-03: 28/28 — YES, 100%.**
- **92-row total: 90/92.**
- ChatGPT queue (BP-01..03): 2 — bp-01-introduction/007 (gen/bp-01-introduction/007/web5.png), bp-02-what-you-need/021 (gen/bp-02-what-you-need/021/web2.png).


---

## Run on top of 9b79567 — 14 Nov 2026 (WITA): Cursor-agent still for BP-01 007, and BP-03 011/014 reopened

Image source is now the Cursor agent on `cursor/blueprint-cursor-images` in `kyleashton88-cyber/claude`, not ChatGPT. Fetched `course/images/bp-01-introduction/007.png` at commit `5988875b23967a21a821e038cd49c6ac384b580d` (git blob `59687210ee5623ec6584d56220dbef0aeeace311`), saved as `gen/bp-01-introduction/007/cursor1.png`. Real PNG, 1536x1024 RGB, 161477 bytes. Scored on the same strict rubric (every category at least 4/5, no hard fails; every arrow tip must visibly touch its target; doubt = fail; margins at least 45px luma>110).

| File | Result | Margins (l/r/t/b) | Reason |
|---|---|---|---|
| gen/bp-01-introduction/007/cursor1.png | PASS | 108/108/114/106 | All three tips touch: 'Sell orders above' on the left cap of the second mint rung, 'Price now' on the left end of the dashed price line, 'Buy orders below' on the left cap of the second blue rung. 4 mint rungs above and 4 blue below, one dot each. Headline 'BUY ORDERS BELOW, SELL ORDERS ABOVE' exact and spaced. EXAMPLE present. No mascot. GridBot Builder style. Beginner-clear against the beat (buy orders below the mark, sell orders above it). Placed at out/ and course/images/bp-01-introduction/007.png (`source: cursor`, scored_blob 59687210ee5623ec6584d56220dbef0aeeace311). Removed from the queue. |

BP-03 011 and 014 were reopened in the pass list (`status: reopened`, reason: beginner-watch failure, Cursor remake pending). Their placed files were left in place. They are added to the ChatGPT/Cursor remake queue as `cursor1.png` targets.

### Updated counts (92-row list)
- **BP-01: 32/32 — YES, 100%.**
- **BP-02: 31/32 — NOT 100%.** Rows left: 021 (web2, v3).
- **BP-03: 26/28 — NOT 100%.** Rows left: 011, 014 (reopened; Cursor remake pending).
- **92-row total: 89/92.**
- Queue (BP-01..03): 3 — bp-02-what-you-need/021 (gen/bp-02-what-you-need/021/web2.png), bp-03-what-is-a-grid-bot/011 (gen/bp-03-what-is-a-grid-bot/011/cursor1.png), bp-03-what-is-a-grid-bot/014 (gen/bp-03-what-is-a-grid-bot/014/cursor1.png).
