# Changes, 16 November 2026

## Approved 16 Nov 2026, 9:14am WITA

Stewart approved all 55 wordings in `course/qa/FLAGS_FOR_STEWART.md` exactly as proposed. The four outcome lines are now the approved rewrites. The disclaimer is External Comms' canonical block, spoken in all 11. The PENDING STEWART markers are removed.

| ID | Now spoken |
|---|---|
| F-ALL-3 / S7a | No real order is sent in this lesson. Paper practice comes in Lesson 7, and real money only after your written graduation rule. |
| F-07-1 / S16 | On a paper or demo account, pressing start uses pretend money, and that is the practice. On a real account, you stop before confirm until your graduation rule passes. |
| F-08-1 / S17 | The fourth row is a review record, not a target: realised, unrealised, fees, and whether you followed the rules. |
| F-10-1 / S19 | Size comes from your caps, never from a target. |

The disclaimer now spoken in all 11 lessons is External Comms' canonical block, approved:

Education only. Not financial advice. This is general information and doesn't consider your objectives, financial situation or needs. Crypto is high risk; you could lose all the money you put in. Past performance is not a reliable indicator of future results.

## FLAG: both exits

| Old line | New line | Reason |
|---|---|---|
| It triggers when a daily close finishes outside the band and the next daily close is still outside. | It triggers when a daily close finishes outside the band, through the top or the bottom, and the next daily close is still outside. | FLAG F-ALL-7. The stop has to cover the downside as well as the 23 October rise. Two short shots then say you hold coin on the way down, and you stop the bot either way. |

## FLAG: facts, before the BP-01 render

Checked against `btc-usd-windows.json`. The 27,630 to 28,531 pair does not complete on the summer daily closes. The film uses the pair that does: buy at 26,730 reached on 17 August 2023, sell at 27,630 reached on 29 August 2023. Gross US$9.00, fees about US$0.54, net about US$8.46. The old card arithmetic of US$8.45 was the unfinished pair.

28 crossings still holds. The close-to-close drop from 11 to 12 March 2020 is −37.2% (7,911.43 to 4,970.79). The −48% figure is only the 13 March candle low against the 11 March close, and it is not spoken over a close-only line.

| Old line | New line | Reason |
|---|---|---|
| The price did not come back, so the waiting orders inside the old band no longer matched the path. | The next day's close was still above the top line, so the stop was confirmed then, not by looking back later. The rise sold every coin on the way up, so the grid sat in cash while the price rose. | FLAG. An upside leave is cash, not "holding inventory". The stop is the next close, not hindsight. BP-03 will need a re-render when its turn comes. |
| The rule has to say: if the daily close goes above 30331 and does not come back, the example is over. | The rule has to say: if a daily close finishes outside the band and the next daily close is still outside, the example is over. | FLAG. "Does not come back" cannot be known on the day you have to act. |
| Finish sentence: if the daily close leaves 30331 and does not return, the summer idea is over. | Finish sentence: if a daily close finishes outside the band and the next daily close is still outside, the summer idea is over. | FLAG. Same stop rule. |
| The finish rule here is: if the daily close leaves 30331 and does not come back, the idea is finished. | The finish rule here is: a daily close outside the band, confirmed by the next daily close still outside. | FLAG. Same stop rule. |
| If the daily close leaves 30331 and does not come back, this example is finished. | If a daily close finishes outside the band and the next daily close is still outside, this example is finished. | FLAG. Same stop rule. |
| Stop: the close leaves 30331 and does not come back, which this path did on 23 October 2023. | Stop: a close outside the band, confirmed by the next close, which this path met on 24 October 2023. | FLAG. The confirmation day is 24 October. |
| Seven was the line count, and six is the gap count. | On a Binance-style form, the grids field counts gaps, not lines. Seven grids would be seven gaps. | FLAG. BP-07. Grids means gaps. |
| If a form says seven grids, that counted lines. | If a form says seven grids, check the venue's help page. On a Binance-style form that means seven gaps, not seven lines. | FLAG. Same reason. |
| The daily close is at 11am Australian eastern daylight time, and at 10am outside daylight saving. | The daily close is at 11am Australian eastern daylight time while daylight saving is in force, and at 10am Australian eastern standard time otherwise. | FLAG. The glossary now names AEST. |

The chart walk no longer stamps the summer rungs onto the 2024 window or the 2020 drop. The 2024 window uses its own seven lines, from 56,555 to 72,715. After the October leave, the rally chart does not draw the summer grid. BP-08's week card, when its turn comes, uses about A$3.60 a pair and about −A$30 unrealised on the lesson 6 bot.

## FLAG: image sync, before the BP-01 render

| Old | New | Reason |
|---|---|---|
| BP-01 still 012 headline baked as NO PROFIT PROMISES | The film covers it and draws NO PROMISE OF RESULTS | FLAG. The old headline was the results slogan. |
| Course map labels: Scaling, Liquidation | Scaling up, Your complete plan | FLAG. The map has to name the lessons. Lesson 11's title card stays Advanced: liquidation scenarios. Your complete plan is the last step on the map, not a new title. |
| BP-04 regime word "range" on several existing lines | sideways market | FLAG. Already listed above. A regime is not the grid range. |

Mint, amber and electric blue were recoloured on the 42 KEEP stills named in the image-sync review. Sells that were mint are now white. Buys that were electric blue are now cyan. Amber marks are now white. Creative Studio still has to rescore them.

Retired and not shown: `analogy-fence.png`, the code-drawn fence chart, and BP-01 015. BP-02 and BP-11 fence phrases in the JSON were changed to L-plates and bucket.

28 crossings and the −37.2% close drop (7,911.43 on 11 March 2020 to 4,970.79 on 12 March 2020) were checked against `btc-usd-windows.json`.

Stale remake notes dropped: BP-03 009, 011 and 014 are already plain. BP-05 006 maths is already correct. The BP-09 005 wick note is stale. BP-08 015's NO RESULT chip is on the remake list. BP01-V07 is on the curriculum list. The cut list is `course/curriculum/CUTS.md`. No picture is planned to hold past 8 seconds.

## Source of truth

The film is spoken from `course/blueprint-rework/lesson_scripts.py`, expanded by `course/blueprint-rework/curriculum_expand.py`, and drawn by `course/blueprint-rebuild/studio.py`. That is the single source of truth for BP-01 to BP-11.

`course/scripts/bp-*.json` is not a second narration. The renderer uses it only to attach stills. Its legal lines, course name, fence phrases and prompt colours were aligned to this source so the two files no longer disagree. They are not rendered as their own film.

## FLAG: brand and tax, before the BP-01 render

| Old line | New line | Reason |
|---|---|---|
| Grid Bot Builder. Grid Bot Blueprint. Lesson one. Introduction. | GridBot Builder. GridBot Blueprint. Lesson one. Introduction. | FLAG. The ident showed the brand with a space. The locked spelling is GridBot Builder and GridBot Blueprint. |
| Education only. Not financial advice. This is general information and doesn't consider your objectives, financial situation or needs. Crypto is high risk. You could lose all the money you put in. | Education only. Not financial advice. This is general information and doesn't consider your objectives, financial situation or needs. Crypto is high risk; you could lose all the money you put in. Past performance is not a reliable indicator of future results. | FLAG. One disclaimer block, identical in all 11 lessons. The semicolon and the past-performance sentence are the canonical wording. |
| Risk card: Crypto carries a risk of total loss. | Removed as its own card. The same warning is inside the disclaimer: you could lose all the money you put in. | FLAG. It repeated the disclaimer. |
| Risk card: Past performance is not a reliable indicator of future results. | Removed as its own card. The same sentence is now the last line of the disclaimer. | FLAG. Same reason. |
| By the end of this series you will understand what a grid bot does, why it can earn when price bounces, and where it loses. You will know how to plan one, test it on paper, run it, check it, and grow the money you give to bots under written rules. | By the end of this series you will understand what a grid bot does, when it can capture bounces, and where it loses. You will know how to plan one, test it on paper, run it, check it, and change the capital you give to bots only under written risk rules. | FLAG. "Grow the money" could be heard as a results claim. |
| By the end you will be able to call the summer window a range. | By the end you will be able to call the summer window a sideways market. | FLAG. In BP-04, "range" is the regime. It was clashing with the grid range from BP-01. |
| You will call October 2023 to March 2024 a trend, not a range. | You will call October 2023 to March 2024 a trend, not a sideways market. | FLAG. Same reason. |
| That shape is a trend, not a range. | That shape is a trend, not a sideways market. | FLAG. Same reason. |
| Range, trend, break. If you label the March 2020 drop a range, the sort is wrong. | Sideways market, trend, break. If you label the March 2020 drop a sideways market, the sort is wrong. | FLAG. Same reason. |
| If the price keeps returning inside a top and a bottom, call it a range. | If the price keeps returning inside a top and a bottom, call it a sideways market. | FLAG. Same reason. |
| A grid of waiting orders belongs to a range. | A grid of waiting orders belongs to a sideways market. | FLAG. Same reason. |
| JSON, BP-02: look for a fence around a generic form labelled Paper. | L-plates on a generic form labelled Paper. | FLAG. The fence analogy is retired. Paper practice is L-plates. |
| JSON, BP-11: one fenced box, the fence labelled Isolated. | one bucket labelled Isolated. | FLAG. Isolated margin is a bucket, not a fence. |
| JSON, BP-11 recap: isolated fence. | isolated bucket. | FLAG. Same reason. |
| Still prompts: electric blue #1E5EFF. | cyan #00D4FF. | FLAG. Navy, cyan and white only. 219 prompt fields in the Blueprint JSON. |

Market Pros is not in the BP-07 legal line the renderer speaks, and it is not in `course/scripts/bp-07-spot-paper-trading.json`. The hard rule stays: the name is banned, and the test still fails the build if it appears.

The amber colour in `studio.py` is now white, and the mint and off-cyan blue are now cyan. No dark-green chip tuple remains in the current builder.

Tax lines added, not substituted for an old sentence: the BP-02 journal now asks for the date, the amount, the Australian-dollar value, the fee and where the fill happened. BP-08 says a coin-quoted pair makes every fill a swap, records are kept for five years, and this is not tax advice.


Lesson titles and lesson order are unchanged.

Additions are allowed. Every edit or removal of an existing script line is listed below so Stewart can flag it.

BP-08 and BP-10 reversals are approved. The old "no result row" and "size is not a target" lines are replaced by the approved wording. The added review and cap shots are part of the script.

## BP-01 existing lines

The lesson is still titled Introduction. The flow was expanded. These existing spoken lines were edited or removed.

| Old line | New line | Reason |
|---|---|---|
| A grid bot places waiting buy orders on lines below the price and sell orders on lines above it, inside a top and a bottom you choose. The space between your top and your bottom is called the band. | The same two sentences, followed by the existing coin sentence below. | Cash and coin are defined before this line is used. The band sentence itself is unchanged. |
| The sells above need some coin, so a grid starts with part cash and part coin, and that is a description, not advice about what to hold. Cash is money you can spend. Coin is the crypto. | Cash is money you can spend. Here that means dollars, or a coin that is meant to stay near one dollar. Coin is the crypto, such as bitcoin. Later: The sells need some coin, so a grid starts with part cash and part coin, and that is a description, not advice about what to hold. | The old sentence defined cash and coin after it had already used them. The definition now comes first. The "not advice" sentence is kept. |
| A stop is a rule you write down before you start, saying what you will do if the price leaves the band and does not come back. | A stop is a rule you write down before you start. It triggers when a daily close finishes outside the band and the next daily close is still outside. You stop the bot, which cancels the waiting orders, then you follow the rule you wrote: keep the coin, or swap it back to cash. Some bots have a stop setting that can do this. Otherwise you do it by hand, and you write which one before you start. | The old line named the rule and not the action, the trigger, or who does it. |
| When a chart says Example, it means a real past price used as an example, not a forecast. | Numbers marked Example are teaching numbers, not advice, and no order is sent. | The old instruction did not tell a beginner what to do with the word Example. |
| By the end you will know what a grid bot places. | Removed as its own card. The opening promise covers it: understand what a grid bot does, why it can earn when price bounces, and where it loses. | One opening, not a second list of aims in the middle of the lesson. |
| You will see that idea on one real path from 2023. | Removed as its own card. The 2023 path is still taught on the range, the candle and the whole window. | Same reason. The path was not removed. |
| You will be able to say the stop rule in one sentence. | Removed as its own card. The stop section and the recap say the rule, the trigger and who acts. | The old card promised the sentence before the sentence had been taught. |
| Think of a ladder leaned on a wall. The rungs wait, and they do not chase you. The ladder is the analogy, and the chart beside it is the real past path. | The same, plus: A rung is one price where an order waits. The gap is the space between two rungs. | The ladder caption is unchanged. The added sentence defines rung and gap at first use. |
| A fence has a top rail and a bottom rail. Inside them, the price can wander. On the chart those rails are 24930 and 30331. | Removed. | The fence analogy is retired. The range is the top and bottom rungs of the ladder. |
| The daily close is the last price of the day. Crypto trades all day, so the day is cut at a set time. | The same, plus: For these public prices the cut is 11 in the morning, Australian eastern daylight time. | The old line said "a set time" and did not say which time. |
| The example is Bitcoin's public daily price in US dollars. From 19 July 2023 to 16 October 2023, every one of those days closed inside the band. We do not need to read each day. The shape is the lesson, and it is marked Example. | The same, plus: The close crossed the seven lines 28 times in that window. The count is an example, not a forecast. | The count is true on the public closes (28 crossings) and stops a beginner treating every touch as a result. |
| A stop is a rule you write down before you start, saying what you will do if the price leaves the band and does not come back. On 23 October 2023 the close finished above the top line. The price did not come back, so this example was finished. | Kept inside the longer stop section, with the next day's close added: the next day was still above the top line, so this example was finished. | One close was not enough to teach "does not come back". 24 October 2023 is also above the top line. |
| Worked check: 19 July 2023 to 16 October 2023. Six equal gaps of about 900 dollars. The low is the bottom line. The high is the top line. | Removed as a separate card. The same facts remain on the range, the levels and the whole-window chart. | The card repeated numbers the charts had just shown. |
| The stop rule is: if the daily close leaves the top line and does not come back, the idea is finished. Nothing on this card is an order. | Removed as a separate card. The stop section says the trigger, the action and who does it, and says no order is sent. | The old card did not say what you do. |
| A grid bot places waiting buys below the price and waiting sells above it. | A grid bot places waiting buys below the price and waiting sells above it, inside a band you choose. | The band belongs in the recap sentence. |
| This 2023 path stayed between 24,930 and 30,331, with six gaps of about 900 between the lines. | A finished pair buys lower and sells higher. The fees come out of the gap. In the example that was about eight dollars fifty, and it is not a promise. | The old recap repeated the band and never said why a grid can earn. The band is still on the charts. |
| The stop rule says what you will do if the price leaves and does not come back. | If a daily close leaves the band and the next close is still outside, you stop the bot and follow the rule you wrote. | The old line did not say the trigger or that you stop the bot. |
| Leave every figure marked EXAMPLE, and no order is sent between lessons. | Numbers marked Example are teaching numbers, not advice, and no order is sent. | A beginner could not tell what "leave every figure marked" asked them to do. |
| Spoken still, beat 12: There is no result number in this lesson. A result number would pretend the example already happened. The example is a drawing of a mechanism. | There is no promise of results. The pair card is a teaching sum, marked Example. It is not money you made. | The lesson now shows one pair with fees, so "no result number" would contradict the card. The card is marked as teaching, not a result. |
| Spoken still, beat 15: A paper or demo account is practice with no real order. You can look at the fields. You still do not send an order in this course. | Removed from the film. Replaced by: Practice on paper, or on a demo, before any real money. Think of L-plates. | The still taught paper practice with the retired fence analogy. L-plates is the analogy for practice. |

Unchanged existing BP-01 lines, kept word for word:

- A limit order is an order that waits at a price you choose. It does not chase the price. Chasing the price would mean moving the order to follow wherever the price has gone.
- The range is the top line and the bottom line, taken from the path. Every close in this window stayed between those two lines.
- Six equal gaps of about 900 dollars sit between the bottom line and the top line. Each gap is about 900 dollars: the top line minus the bottom line, divided by six. It is one step between lines, not the whole band. Seven lines make those six gaps. A limit order waits on a level. It does not run after the price.
- The candle sentences about the body, the wick, the high, the low and the close, and the 19 July 2023 labels.
- The outro lines for the next lesson, the pair, the notebook, paper or demo, the stop rule, and no secrets, including the seed-phrase gloss.

## BP-02 to BP-11

No existing spoken line in these lessons was edited or removed.

Curriculum teaching was added before each outro. Lesson titles and order are the same.

BP-08, approved: a weekly review record (realised, unrealised, fees, rules followed). The "No result row" lines are replaced.

BP-10, approved: example sizing caps (20 percent of the account, 2.5 percent loss at the stop, on an example A$10,000 account). "Size is still not a target." is replaced by "Size comes from your caps, never from a target."

Nothing in BP-02 to BP-11 is final until Stewart says so and a full QA pass has run on the rendered lesson.

## Pictures

Passed BP-01 stills and the shared ladder, list, buckets and fence analogies were recoloured on 16 Nov 2026. Amber, mint, teal and off-cyan blue pixels were moved to white or cyan. Creative Studio still has to rescore them. The fence analogy is not used in the BP-01 film.

Files recoloured: `course/images/bp-01-introduction/001.png` through `018.png`, and `course/images/blueprint-analogies/analogy-ladder.png`, `analogy-list.png`, `analogy-buckets.png`, `analogy-fence.png`.

On-screen brand text is spelled GridBot Builder. The spoken open may still say it as three words. Captions spell it GridBot Builder.
