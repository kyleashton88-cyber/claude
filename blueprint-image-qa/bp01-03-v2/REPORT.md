# BP-01..BP-03 image QA v2 (strict first scoring)

Scored by Creative Studio, 14 Nov 2026 (WITA). Same strict method as bp04-11. Image scoring only: no verdict on the BP-01..03 videos.

**Scope:** image fields of course/scripts/bp-01..bp-03 @ d1f6 `fbb3f9c` (58 stills); files scored from cursor/blueprint-beginner-images `2f8bac1`.

**Result:** 37 pass / 21 fail of 58. Remake queue: 21 (needs_mascot_ref: 0).

**Mismatches:** none. All 58 blobs are identical on d1f6 and beginner-images and match the v10 pass list's scored_blob. All 58 were 'pass' on v10; 21 are overturned here.

**Out of scope / other findings:** 34 v10 rows (title art, mascot, analogy stills, code-drawn charts and cards) are not script image fields and were not re-scored. The numbers files (d1f6) set the on-screen disclaimer to 'Educational content only. Not financial advice.', which is not the exact line.

**Fix status:** every fail = `needs_remake`, prompt written (specs/remake/<lesson>__NNN.txt, copied to remake/), not regenerated. Old prompts moved to specs/remake/_superseded/: `bp-01-introduction__010.v1.txt`, `bp-02-what-you-need__004.v1.txt`, `bp-03-what-is-a-grid-bot__003.v1.txt`, `bp-03-what-is-a-grid-bot__010.v1.txt`.


## bp-01-introduction (Introduction): 18 total, 12 pass, 6 fail

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

## bp-02-what-you-need (What you are going to need): 21 total, 14 pass, 7 fail

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
