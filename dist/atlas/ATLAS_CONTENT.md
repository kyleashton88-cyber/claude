# Atlas

Atlas is a directory for learning how markets work, how to read structure, how grid bots behave, and how leverage and later contracts change the risk.

Educational content only, not financial advice.

If you are new, read Start here from the top. Each lesson says what you will learn, shows a labelled picture, walks through made-up numbers, and names the next lesson. The glossary is one plain line per word. The tools redo the arithmetic when you change a number.

## Start here

Follow the beginner lessons in order. Then open Intermediate.

1. Markets (Foundations). a market is where a buyer and a seller agree a price, and the printed price is that agreement.
2. Candles (Foundations). a candle compresses one period into the open, the high, the low, and the close.
3. Order types (Foundations). a limit order waits for your price, and a market order pays the price that is available now.
4. Wallets and venues (Foundations). coins you can move sit with your key, and coins at a venue sit with the venue until you withdraw.
5. Risk basics (Foundations). you choose the cash you can lose, then divide by the distance to the stop, and that quotient is the size.
6. Trend (Trading structure). an uptrend is higher highs and higher lows, and a downtrend is the opposite, on a clock you name.
7. Swing highs and lows (Trading structure). a swing high is a high with lower highs on both sides, and a swing low is a low with higher lows on both sides, under a rule you keep.
8. Support and resistance (Trading structure). support is a price area where declines have stalled, and resistance is a price area where rallies have stalled.
9. Market structure (Trading structure). market structure is the ordered list of swing highs and swing lows you are using on one clock.
10. Break of structure (Trading structure). a break of structure is a close through the swing that would continue the sequence you already mapped.
11. Change of character (Trading structure). a change of character is a break against the sequence, such as losing the higher low an uptrend needed.

## Beginner

Start here if the words are new. You learn what a market is, how a candle is drawn, how an order waits or crosses, where coins can sit, and how a small risk limit becomes a size. Then you learn to name a trend, a swing, and a break.

### Foundations

These five lessons are the floor. Later lessons use these words without stopping to redefine them.

#### Markets

What you'll learn: a market is where a buyer and a seller agree a price, and the printed price is that agreement.

A market is a meeting place for orders. Someone wants to buy. Someone wants to sell. When they agree, a trade prints.

The printed price is not a vote about the future. It is the last agreement. The next agreement can be higher or lower.

Buyers and sellers can both be wrong about what they wanted a minute ago. The tape only shows the trades that happened.

You do not need a named venue to understand this. Any place that matches orders works the same way at this level.

Next you will see how one period of those trades is drawn as a candle.

Example.

- A buyer is willing to pay 100.
- A seller wants 110.
- They meet in the middle and a trade prints at 105.
- 105 is the last price. It is not a promise that the next trade is 105.

Picture `atlas-foundations-01.png`. Buyers on the left and sellers on the right meet at a price of 105.

Recap.

- A trade is an agreement.
- The last price is history, not a forecast.
- The same idea fits any venue.

Next lesson: Candles.

#### Candles

What you'll learn: a candle compresses one period into the open, the high, the low, and the close.

Pick a clock. One minute, one hour, one day. A candle covers that clock and then the next candle starts.

The open is the first trade in the period. The close is the last trade. The high is the dearest trade. The low is the cheapest trade.

The body is the box from open to close. The wicks are the lines beyond the body. A wick shows that price visited a level and did not stay there by the close.

A wide body means the close is far from the open. A long wick means the extreme did not hold.

Colour is a convenience. The four prices are the fact. Next you will see how an order can wait at a price or cross the spread.

Example.

- Open 100. High 108. Low 97. Close 104.
- The body runs from 100 to 104. That is 4.
- The upper wick runs from 104 to 108. The lower wick runs from 100 to 97.
- Price traded at 108, but the period ended at 104.

Picture `atlas-foundations-02.png`. One candlestick. High 108, close 104, open 100, low 97.

Picture `atlas-foundations-03.png`. Two candles. The left has a wide body. The right has a long wick.

Recap.

- Four prices define the candle.
- The body is open to close.
- Wicks are visits that did not become the close.

Next lesson: Order types.

#### Order types

What you'll learn: a limit order waits for your price, and a market order pays the price that is available now.

An order book is a list. Bids are buys that are waiting. Asks are sells that are waiting. The best bid is the highest waiting buy. The best ask is the lowest waiting sell.

The spread is the gap between those two. Crossing the spread costs you that gap, plus any fee.

A limit order rests at the price you choose. It may not fill. A market order fills now against resting orders. You do not choose the exact print.

A stop is a trigger. When price reaches it, the stop becomes a market or a limit, depending on the rule you set. The name stop does not mean the loss is capped until you see the fill.

Next you will see the difference between coins you can move yourself and coins sitting at a venue.

Example.

- Best bid 99. Best ask 101. The spread is 2.
- A limit buy at 99 waits with the bid. It fills only if a seller comes down.
- A market buy pays 101 now. The extra 2 is the cost of crossing, before fees.

Picture `atlas-foundations-04.png`. A small book. The ask is 101, the bid is 99, a limit rests at 99, and a market buy pays 101.

Recap.

- Limit waits. Market crosses.
- The spread is a real cost.
- A trigger is not the same thing as a fill.

Next lesson: Wallets and venues.

#### Wallets and venues

What you'll learn: coins you can move sit with your key, and coins at a venue sit with the venue until you withdraw.

A wallet is a way to hold the secret that can move coins. The common secret is a word list. Anyone who has the words can move the coins. There is no ordinary reset.

A venue account is different. The venue's books say the balance is yours, but the keys are theirs until a withdrawal completes.

Both places can fail. You can lose a word list. A venue can freeze, halt withdrawals, or be wrong about a balance.

This directory does not name a venue and does not rank them. The question is only who can move the coins today.

Next you will turn a cash limit into a position size. That habit matters before any bot or any leverage.

Example.

- You have 1000 coins in total in this example.
- 200 sit where you hold the word list.
- 800 sit in a venue balance.
- You can move the 200 yourself. You can move the 800 only if the venue processes a withdrawal.

Picture `atlas-foundations-05.png`. Two balances. Your wallet holds 200 and the key. A venue balance holds 800 and the key stays there.

Recap.

- The word list is the key.
- A venue balance is a claim, not the same as a key in your hand.
- Split the question: who can move the coins.

Next lesson: Risk basics.

#### Risk basics

What you'll learn: you choose the cash you can lose, then divide by the distance to the stop, and that quotient is the size.

Risk here means the cash you are willing to lose if the idea is wrong. It is a number you write before the entry.

The stop is the price that means the idea is wrong. The distance is the gap from entry to that price.

Size is cash at risk divided by distance. A closer stop makes a larger size. A closer stop is not automatically safer.

Fees and slippage make the loss a bit larger than the cash you named. Later tools show that extra.

You now have the floor. The next module names the shape of the path: trend, swing, and break.

Example.

- Account 10000. You risk 1 percent. That is 100 of cash.
- Entry 100. Stop 95. Distance 5.
- Size is 100 divided by 5, which is 20 units.
- Notional is 20 times 100, which is 2000. That is the position, not the loss. The planned loss is still about 100, plus fees.

Picture `atlas-foundations-06.png`. An account bar of 10000 with a small slice of 100, which is 1 percent. The stop is 5 away, so the size is 20.

Recap.

- Write the cash first.
- Size equals cash divided by distance.
- A tight stop increases size.

Next lesson: Trend.

### Trading structure

Structure is a map of swings. You name the trend, the turning points, the floors and ceilings, and the two kinds of break.

#### Trend

What you'll learn: an uptrend is higher highs and higher lows, and a downtrend is the opposite, on a clock you name.

A trend is a sequence, not a feeling. On an uptrend the lows keep stepping up. On a downtrend the highs keep stepping down.

Name the clock in the same breath. A rising hour can sit inside a falling day. Both descriptions can be true.

A trend does not have to be steep. It has to keep the sequence. When the sequence breaks, you stop calling it that trend.

Grid plans later in this directory prefer back and forth movement. A strong trend fights that plan. You need this lesson before that one.

Example.

- On the daily clock the swing lows print at 90, then 100, then 110.
- Each low is higher. That is an uptrend on the daily clock.
- The same coin can still fall for three hours inside that day. The hour clock is a different sentence.

Picture `atlas-structure-01.png`. A rising path with higher lows at 90, 100, and 110.

Recap.

- Trend means a sequence of swings.
- Always name the clock.
- A break in the sequence ends that label.

Next lesson: Swing highs and lows.

#### Swing highs and lows

What you'll learn: a swing high is a high with lower highs on both sides, and a swing low is a low with higher lows on both sides, under a rule you keep.

You need a rule for how many bars sit on each side. Two bars, or five. Write it down and do not change it mid chart.

The swing is confirmed only after the later bars exist. You cannot know the high was a swing at the moment it prints.

Swings are the posts of the map. Trend, support, and breaks all hang off these posts.

Example.

- A high prints at 120.
- The bar on the left has a high of 110. The bar on the right has a high of 110.
- Under a one-bar rule, 120 is a swing high.
- If your rule needs five bars on each side, you wait until those bars exist.

Picture `atlas-structure-02.png`. A peak at 120 with 110 on both sides. That peak is a swing high.

Recap.

- A swing is a turn under a written rule.
- It is confirmed late, not in real time.
- Keep the same rule on one map.

Next lesson: Support and resistance.

#### Support and resistance

What you'll learn: support is a price area where declines have stalled, and resistance is a price area where rallies have stalled.

These are areas, not magic lines. A single print is weaker than several reactions in the same zone.

When price leaves a ceiling and later uses it as a floor, traders rename it. The rename is a description of later behaviour, not a duty the market owes you.

For a grid, these areas are how you sketch a box. The box is still a choice. It is not a forecast of the high and the low of the year.

Example.

- Three declines stall near 100. You mark support around 100.
- Two rallies stall near 130. You mark resistance around 130.
- A plan that needs a range might use 100 and 130 as the first sketch, then add room for ordinary wicks.

Picture `atlas-structure-03.png`. A lower line at 100 called support and an upper line at 130 called resistance.

Recap.

- Support and resistance are reaction areas.
- Several reactions matter more than one print.
- They sketch a box. They do not guarantee it.

Next lesson: Market structure.

#### Market structure

What you'll learn: market structure is the ordered list of swing highs and swing lows you are using on one clock.

Write the last few swings in order. In an uptrend you expect a higher high, then a higher low, then another higher high.

The map is only as good as the swing rule. If you change the rule, you draw a different map. Say which rule you used.

Structure is the bridge into the next two lessons: a break that continues the sequence, and a break that opposes it.

Example.

- Swing low 110, swing high 130, swing low 120, swing high 150.
- 110 to 120 is a higher low. 130 to 150 is a higher high.
- On this clock the structure is still an uptrend.

Picture `atlas-structure-04.png`. Higher highs and higher lows. Marks at 110, 130, 120, and 150.

Recap.

- Structure is a list of swings.
- The swing rule is part of the sentence.
- The next lessons name the two kinds of break.

Next lesson: Break of structure.

#### Break of structure

What you'll learn: a break of structure is a close through the swing that would continue the sequence you already mapped.

In an uptrend, a break of structure is a close through the latest higher high. The sequence is still up. It has extended.

Decide in advance whether a wick counts or only a close. Teachers differ. Your map cannot use both without saying so.

A break is a description. It is not an order to buy or sell.

Example.

- The latest higher high is 130.
- A later bar closes at 134.
- If your rule uses closes, that is a break of structure in the direction of the uptrend.
- A wick to 134 that closes back at 129 would not count under that same rule.

Picture `atlas-structure-05.png`. A prior high at 130 and a later close at 134 beyond that high.

Recap.

- Break of structure continues the sequence.
- Write wick or close before you look.
- The word is a description, not an instruction.

Next lesson: Change of character.

#### Change of character

What you'll learn: a change of character is a break against the sequence, such as losing the higher low an uptrend needed.

In an uptrend the higher low is the post that must hold. A close through that low is against the sequence.

People abbreviate this idea as a change of character. The plain version is enough: the old pattern failed.

This is the point where a range plan and a trend plan part ways. A grid that assumed back and forth now needs the review rule you will write later.

The next level looks at liquidity and gaps. Those are extra marks on the same swings. You can skip ahead only if this page is already clear.

Example.

- The uptrend's latest higher low is 110.
- A later bar closes at 106.
- Under a close rule, the higher low failed. The character of that uptrend has changed.
- You do not invent a new trend until a new sequence of swings exists.

Picture `atlas-structure-06.png`. An uptrend higher low at 110, then a close at 106 under that low.

Recap.

- Change of character breaks against the sequence.
- The failed post is the higher low or the lower high.
- Wait for a new sequence before you rename the trend.

Next lesson: Liquidity.

## Intermediate

You already know swings. Here you add marks that some traders use around those swings, and then you learn how a grid bot repeats orders inside a box.

### Smart money concepts

These names describe pictures on a chart. They are not receipts from a bank, and they are not instructions.

#### Liquidity

What you'll learn: liquidity in this lesson means the cluster of stops and resting orders that often sit beyond an obvious high or low.

Equal highs and equal lows are obvious. Stops are often parked just beyond them. Resting breakout orders sit there too.

A pool is a description of that cluster. You cannot see the stops. You can see the obvious level.

A sweep is a push through the level that then returns inside. You may call it a sweep only after the return. Before the return it is only a break.

Price can run those stops and keep going. The picture does not owe you a reversal.

Example.

- Two highs sit at 130.
- A later wick trades 133 and the bar closes back at 128.
- After the close back inside, you can call 133 a sweep of the highs.
- If the bar had closed at 133, you would not use the word sweep yet.

Picture `atlas-smart-money-01.png`. Two equal highs near 130, with a label that stops often sit just above them.

Picture `atlas-smart-money-02.png`. A wick pushes to 133 and the close returns to 128.

Recap.

- Obvious highs and lows attract orders.
- A sweep needs a return.
- The mark is a hypothesis about the chart.

Next lesson: Order blocks.

#### Order blocks

What you'll learn: an order block is a candle, or a small cluster, just before a strong move, which some methods mark in case price returns.

The usual mark is the last opposite candle before the impulse. Down candle, then a strong rise. Or up candle, then a strong drop.

The zone is the body, or the whole candle, under a rule you write. When price later trades back into the zone, that return is called a mitigation. What happens after the return is a separate question.

Nothing on the chart proves a large trader placed an order there. You are marking a candle, not reading a private book.

Example.

- A down candle runs from 102 to 98.
- The next move rises to 120 without much overlap.
- The marked zone is 98 to 102.
- A later visit to 100 is a return into the zone. It is not yet a result.

Picture `atlas-smart-money-03.png`. A small down candle from 102 to 98, then a rise to 120. The small candle is the marked zone.

Recap.

- The mark is a candle before a strong move.
- A return is visible. The outcome is not included in the word.
- It is a chart hypothesis, not a receipt.

Next lesson: Fair value gaps.

#### Fair value gaps

What you'll learn: a fair value gap is a three-candle pattern where the wick of the first and the wick of the third do not overlap.

Candle one, a fast middle candle, candle three. If candle three's wick does not reach candle one's wick, the space between them is the gap.

Some traders expect a later visit into that space. A visit is something you can check. It is not an unfilled order you can audit.

The gap is a location. It is not a reason, by itself, to place a trade.

Example.

- Candle one high is 100.
- The middle candle is large.
- Candle three low is 106.
- The wicks do not meet. The gap is 100 to 106, which is 6 wide.

Picture `atlas-smart-money-04.png`. Three candles. Candle 1 high is 100. Candle 3 low is 106. The gap between them is the fair value gap.

Recap.

- Three candles, and the outer wicks do not overlap.
- The gap is the space between those wicks.
- A later visit is a check, not a promise.

Next lesson: Premium and discount.

#### Premium and discount

What you'll learn: you split a swing from its low to its high, and the top half is premium while the bottom half is discount.

Pick the swing yourself. Low to high. The midpoint splits it.

Discount does not mean the coin is cheap in a fundamental sense. It means price is in the lower half of the swing you chose.

Premium does not mean you must sell. It means price is in the upper half of that same swing.

A grid box can sit entirely in one half. Knowing which half only tells you where you are inside the swing.

Example.

- Swing low 100. Swing high 140. The middle is 120.
- Price at 110 is discount. It is 10 below the middle.
- Price at 130 is premium. It is 10 above the middle.
- Change the swing and the labels move. The words belong to the swing you named.

Picture `atlas-smart-money-05.png`. A dealing range from 100 to 140. The middle is 120. 110 is discount. 130 is premium.

Recap.

- Premium and discount need a swing you chose.
- The middle is the divider.
- The words are locations, not valuations.

Next lesson: Inducement.

#### Inducement

What you'll learn: inducement is a smaller obvious high or low that sits in front of a larger one, where early orders can gather.

Traders mark a minor swing that is easy to see, just before a more important swing. The idea is that early stops collect at the minor one.

Like the other marks in this module, you are guessing where orders might sit. You cannot see them.

A grid range that ignores the larger swing can be built around the small one and then fail when price reaches the larger pool.

The next module leaves these marks and builds a grid from a box, a gap, and a fee.

Example.

- The main high on the clock you care about is 140.
- A smaller high sits at 125, in front of it.
- Early buy stops might cluster above 125.
- That is a hypothesis. A close through 125 does not require a stop at 140.

Picture `atlas-smart-money-06.png`. A small high at 125 sits under a larger high at 140.

Recap.

- Inducement is a smaller obvious swing in front of a larger one.
- It is a guess about where orders sit.
- The larger swing still matters.

Next lesson: What a grid bot is.

### Grid bots

A grid bot repeats buys and sells inside a box you design. These seven lessons are the path: what it is, how a cycle works, how you set it up, how you choose the box and the count, how you limit the damage, how you watch it, and the mistakes that show up first.

#### What a grid bot is

What you'll learn: a grid bot places buys below the price and sells above it, on rungs you chose, and it does not predict the next candle.

You choose an upper price and a lower price. Between them you place levels. Levels under the current price are buys. Levels above it are sells.

The bot follows that list. It does not decide that a coin is good. It does not read the news.

If price only goes one way, the bot mostly collects coins or cash. The ladder does not invent a new plan.

Think of it as a ladder in a room. The room is the box. Outside the room, the ladder is the wrong tool until you review it.

Example.

- Price is 100.
- Sells are written at 102 and 104.
- Buys are written at 98 and 96.
- Nothing has happened yet. These are instructions, not results.

Picture `atlas-grid-bots-01.png`. A ladder. Sells sit above the price at 102 and 104. Buys sit below at 98 and 96. The price is 100.

Recap.

- The bot repeats a ladder.
- You choose the rungs.
- It does not forecast.

Next lesson: How a grid works.

#### How a grid works

What you'll learn: one cycle is a buy that fills and a later sell at the next rung, and the gap between them is the gross step.

Price falls and a buy fills. Price rises and the paired sell fills. That round trip is one cycle.

The gross step is the sell price minus the buy price, before fees, spread, and slippage.

If price never crosses the next rung, the cycle does not finish. A quiet market can sit still. A market that leaves the box does not complete the old cycles.

The bot will keep the old instructions until you change them. Automation does not notice that your reason expired.

Example.

- A buy fills at 98.
- A sell fills at 100.
- The gross gap is 2 per coin.
- A round-trip fee larger than 2 would erase the gap. The next lessons put a fee next to the gap.

Picture `atlas-grid-bots-02.png`. A buy fills at 98 and a later sell fills at 100. The gap is 2 before fees.

Recap.

- A cycle needs a fill on the way down and a fill on the way up, or the reverse pair you defined.
- Gross step is the gap before costs.
- No cross means no finished cycle.

Next lesson: Setting one up.

#### Setting one up

What you'll learn: you write the upper price, the lower price, the number of gaps, the cash, the fee you assume, and the sentence that means the plan is over.

Setting up is mostly writing. The bot cannot supply the box or the reason.

Start with a spot explanation. A futures grid uses the same ladder plus margin, funding, and liquidation. Those words have their own module. Do not add them until you can explain them.

The review rule is one sentence. A daily close outside the box is an example of a sentence. I will see is not a sentence.

Keep some cash out of the grid. A reserve is what you use if you must pay fees or meet a margin need. This page does not tell you how much.

Example.

- Upper 110. Lower 90.
- Ten gaps across that box.
- Cash set aside for the grid: 1000. More cash stays outside it.
- Review rule: a daily close outside 90 to 110 sends you back to the written plan.

Picture `atlas-grid-bots-03.png`. Four setup facts: upper 110, lower 90, 10 gaps, and a review rule.

Recap.

- Write the box, the gaps, the cash, the fee, and the review rule.
- Spot first.
- A review rule is a sentence you can check.

Next lesson: Range and grid count.

#### Range and grid count

What you'll learn: the width of the box and the number of gaps set the step, and the step has to clear a round-trip fee.

A tight box is crossed by ordinary noise. A very wide box spreads the same cash so thin that cycles are rare.

Arithmetic gaps keep the same price distance. Geometric gaps keep the same percentage, so the price distance grows as price rises.

More gaps inside a fixed box make a smaller step. If the step is smaller than the fee and the slippage you assume, extra trades repeat a loss.

Use the grid tool on the tools page to change the fee and watch the warning. The numbers there are the same kind of example as this lesson.

Example.

- Lower 90. Upper 110. The box is 20 wide.
- Ten gaps. Arithmetic step is 20 divided by 10, which is 2.
- A fee of 10 basis points on each side is 0.10 percent each way. At a price of 100, the round trip is about 0.20 per unit.
- Step 2 is larger than 0.20 in this example. Forty gaps in a box only 10 wide, from 100 to 110, would make a step of 0.25, which is close to a 0.20 fee.

Picture `atlas-grid-bots-04.png`. Three ranges. A tight box from 100 to 105, a middle box from 90 to 110, and a very wide box from 50 to 150.

Picture `atlas-grid-bots-05.png`. A step of 2 beside a round-trip fee of 0.20. The step is larger than the fee in this example.

Picture `atlas-grid-bots-06.png`. Two ladders. The left has equal price gaps. The right has gaps that grow as price rises.

Recap.

- Width and count together set the step.
- Arithmetic and geometric gaps are different shapes.
- A step that does not clear the fee does not get fixed by more trades.

Next lesson: Grid risk.

#### Grid risk

What you'll learn: finished cycles and unsold coins are different results, and the account can be down while the cycle total is up.

Grid profit usually counts finished round trips. Coins you bought and have not sold are inventory. Inventory can fall in price.

Several grids on the same coin are one bet that the coin stays in those boxes. They are not five independent ideas.

The cash you can lose if the review rule hits is the risk that matters. Use the position-size idea from the first module: cash divided by distance.

Leverage can turn a small trip outside the box into a margin problem. That is the next level, after this one is clear.

Example.

- Ten finished cycles make a gross 20 in this example.
- You still hold coins bought near 94. The price is now 80.
- The unsold coins are a separate loss. They can be larger than the 20.
- Reporting only the 20 would hide the account.

Picture `atlas-grid-bots-07.png`. Finished cycles show plus 20. Unsold coins bought near 94 are now priced at 80.

Recap.

- Cycles and inventory are different lines.
- Same coin, many grids, one bet.
- Write the cash you can lose if the box fails.

Next lesson: Monitoring and adjusting.

#### Monitoring and adjusting

What you'll learn: you check whether the written reason is still true, and you do not drag the box every hour to chase the latest price.

Look at three things. Is price still inside the box, under the rule you wrote. Does the step still clear the fees you are actually paying. Did a scheduled event make the old reason obsolete.

Adjusting means returning to the sentence you wrote. Moving the box so that price is always inside it deletes the review rule.

Keep a short record. The professional journaling lesson shows one way to turn a list of results into an expectancy. You can start with one line per day.

Example.

- The box top is 110. The review rule uses a daily close.
- Today closes at 112.
- That close starts the review. It does not, by itself, tell you the next box.
- If you silently move the top to 120, you no longer have the old plan to judge.

Picture `atlas-grid-bots-08.png`. The box top is 110 and a later close is 112, which starts a review.

Recap.

- Check the box, the fee, and the reason.
- A close outside starts the written review.
- Chasing price with a new box is a new plan.

Next lesson: Common grid mistakes.

#### Common grid mistakes

What you'll learn: the usual errors are a fee larger than the step, a box that ignores the higher clock, leverage you cannot explain, and no sentence for failure.

Too many levels are the first arithmetic error. The picture looks busy. The step is smaller than the cost.

The second error is calling a trend a range because you want fills. Check the higher clock from the structure module.

The third error is adding leverage so a small account can run a large ladder. If you cannot explain liquidation, stay with the spot story.

The fourth error is silence about failure. When the box is left behind, there is no rule, so the loss continues.

Sometimes the careful result is to wait. Waiting is a decision. The next level explains leverage on its own terms, not as a way to force a grid.

Example.

- Box from 100 to 110. That is 10 wide.
- Forty gaps. Step is 10 divided by 40, which is 0.25.
- Round-trip fee at a price near 100 is 0.20 in the earlier example.
- 0.25 minus 0.20 leaves 0.05 before spread and slippage. The ladder is almost all cost.

Picture `atlas-grid-bots-09.png`. Forty gaps inside 100 to 110 make a step of 0.25, next to a fee of 0.20.

Recap.

- Count the step against the fee.
- Match the box to the higher clock.
- No review sentence means no real plan.

Next lesson: Margin.

## Advanced

Leverage, futures, and options change the size of a loss and add new payments. Read them after the spot and grid lessons, not instead of them.

### Leverage trading

Margin is the cash you post. Leverage is how large the position is compared with that cash. Liquidation is the price that ends the position for you.

#### Margin

What you'll learn: margin is the cash posted to support a position that is larger than that cash.

Notional is price times size. Margin is the part you post. The rest is borrowed exposure.

Isolated margin is assigned to one position. If that position is closed out, the loss is meant to stop at that assignment. Cross margin shares a pool across positions. One loss can draw on the pool.

A venue can change margin rules. This page uses a plain example, not a live schedule.

Example.

- You want exposure of 10000.
- At 5 times, the margin is 10000 divided by 5, which is 2000.
- The position is still 10000 of exposure. The cash posted is 2000.

Picture `atlas-leverage-01.png`. A notional of 10000 posted with 2000 of margin at 5 times.

Recap.

- Margin is posted cash.
- Notional can be larger than margin.
- Isolated and cross share risk differently.

Next lesson: Leverage.

#### Leverage

What you'll learn: leverage is notional divided by margin, and it scales both the gain and the loss on that margin.

At 5 times, a 10 percent move in price is about a 50 percent move on the margin, before fees and funding.

The multiple does not make a setup more correct. It makes the same setup larger.

If you do not know the liquidation price, you do not yet know the leverage you are using.

Example.

- Margin 2000. Notional 10000. That is 5 times.
- Price falls 10 percent. The position loses about 1000.
- 1000 is half of the 2000 margin. The price move was 10 percent. The margin move was about 50 percent.

Picture `atlas-leverage-02.png`. The price falls 10 percent. On 5 times leverage the margin result is about minus 50 percent.

Recap.

- Leverage scales the result on the margin.
- It does not improve the idea.
- Know the liquidation price before you care about the multiple.

Next lesson: Liquidation.

#### Liquidation

What you'll learn: liquidation is the price where losses have used up the margin down to a maintenance level, and the position is closed.

Maintenance margin is the minimum the venue wants left. This directory uses a simple model so you can see the arithmetic. A real schedule can be harsher, and fees make it worse.

For a long, the example price is entry times the quantity one minus one divided by leverage, plus the maintenance rate.

For a short, the example price is entry times the quantity one plus one divided by leverage, minus the maintenance rate.

The tools page runs this model from numbers you type. It is not a venue's ladder.

Example.

- Entry 100. Leverage 10. Maintenance rate 0.5 percent, which is 0.005.
- Long example: 100 times (1 minus 0.1 plus 0.005) equals 90.5.
- A fall from 100 to 90.5 is 9.5 percent in price. At 10 times, that is enough to exhaust most of the margin in this model.
- Short example at the same inputs: 100 times (1 plus 0.1 minus 0.005) equals 109.5.

Picture `atlas-leverage-03.png`. Entry at 100 and an example long liquidation near 90.5 at 10 times with a 0.5 percent maintenance rate.

Recap.

- Liquidation closes the position for you.
- The example formula is a teaching model.
- Maintenance and fees move the real price.

Next lesson: Position sizing.

#### Position sizing

What you'll learn: you still divide cash at risk by the distance to the stop, and leverage does not replace that division.

The beginner rule remains. Cash you can lose, divided by distance, is the size.

Leverage changes whether the account can hold that notional. It should not be the starting point.

If the notional divided by the account is larger than the leverage cap you set, the size does not fit the cap.

The tools page includes this calculator. Change the stop and watch the size move.

Example.

- Account 10000. Risk 1 percent. Cash at risk 100.
- Entry 100. Stop 95. Distance 5.
- Size is 20. Notional is 2000.
- 2000 divided by 10000 is 0.20. You do not need 10 times leverage to hold this example. Wanting 10 times would be a different, larger plan.

Picture `atlas-leverage-04.png`. Cash at risk 100 divided by a distance of 5 gives a size of 20.

Recap.

- Size still comes from cash and distance.
- Leverage is a constraint, not the goal.
- Check notional against the account.

Next lesson: Perpetuals and dated contracts.

### Futures

A futures contract is an agreement on a later price. Perpetuals have no end date. Dated contracts do. Funding, direction, and hedges sit on top of that difference.

#### Perpetuals and dated contracts

What you'll learn: a perpetual has no expiry, and a dated contract ends on a day you can name.

Both are contracts. You do not hold the coin itself. You hold a claim whose value moves with price, plus the margin rules.

A dated contract stops on its end date. After that, the position is not the same agreement.

A perpetual does not end on a calendar day. It uses funding payments to keep its price near the spot market. The next lesson is that payment.

Example.

- One contract in this example has no end date.
- Another ends in 30 days.
- The second one needs a plan for day 30. The first one needs a plan for funding instead.

Picture `atlas-futures-01.png`. Two contracts. One has no end date. The other ends in 30 days.

Recap.

- Perpetual means no expiry date.
- Dated means a real end date.
- You hold a contract, not the coins, unless you separately own coins.

Next lesson: Funding rates.

#### Funding rates

What you'll learn: funding is a periodic payment between longs and shorts on a perpetual, separate from your open and your close.

In this directory's simple story, a positive rate means longs pay shorts. A negative rate means shorts pay longs. Live contracts can define the sign in their own documents. Read those before you rely on a sign.

The payment is rate times notional, usually several times a day. A small rate on a large notional is not small.

A grid that finishes many small cycles can still bleed if funding runs against the inventory the grid is holding.

Example.

- Rate 0.01 percent for one interval. Notional 10000.
- 0.01 percent of 10000 is 1.
- Three intervals in a day, if the rate stayed the same, would be 3.
- This is an example rate, not a live reading.

Picture `atlas-futures-02.png`. A positive funding example of 0.01 percent. On 10000 of notional that is about 1, paid from longs to shorts in this example.

Recap.

- Funding is a payment between the two sides.
- It is not your trading fee, and it is extra.
- Small rates matter when the notional is large.

Next lesson: Long and short.

#### Long and short

What you'll learn: a long gains when price rises and loses when it falls, and a short does the opposite, before fees and funding.

Long means you benefit from a higher price. Short means you benefit from a lower price.

Both can be leveraged. Both can be liquidated. The direction does not remove the margin rules.

A short can lose more than a beginner expects because price has no ceiling in the simple model. Write a stop anyway.

Example.

- Entry 100. One unit.
- Price goes to 110. The long is plus 10. The short is minus 10. Fees are not in those two numbers.
- Price goes to 90. The long is minus 10. The short is plus 10. Again before fees and funding.

Picture `atlas-futures-03.png`. Price rises by 10. The long result is plus 10 per unit. The short result is minus 10 per unit, before fees.

Recap.

- Long and short are opposite price exposures.
- Costs sit on top of that opposition.
- A stop still belongs on both.

Next lesson: Hedging.

#### Hedging

What you'll learn: a hedge is a second position that offsets part of a move in something you already hold.

If a grid has left you holding coins, a short contract can offset part of a further fall. It can also offset part of a rise. You give up some of the bounce.

The hedge has its own liquidation, fees, and funding. It is not free insurance.

Match the size on purpose. Hedging everything, or hedging a random fraction, are different plans.

Example.

- You hold 2 coins. Price falls by 10. The coins lose 20.
- You are also short 1 coin. That short gains about 10, before costs.
- The net price result is about minus 10, not minus 20. The hedge did not erase the loss.

Picture `atlas-futures-04.png`. Two coins fall by 10 each, a loss of 20. A short of one coin gains about 10. The net loss is smaller.

Recap.

- A hedge offsets part of a move.
- It also offsets part of the opposite move.
- Costs and liquidation still apply to the hedge.

Next lesson: Options basics.

### Derivatives

An option is a right you pay for. Calls and puts are the two directions. Greeks are names for how the price of that right changes. Basis is the gap between a futures price and spot.

#### Options basics

What you'll learn: you pay a premium for the right to buy or sell at a strike, and you can lose that premium.

The premium is the price of the option. It is paid up front in this simple story.

The strike is the contract price inside the right. Expiry is the last moment the right exists.

You are not required to use the right. If you do nothing, the premium can expire worthless. That limited loss is the main difference from a futures position, which can keep losing past the cash you first noticed.

American or European exercise rules change when you may use the right. This page does not pick a venue's rule.

Example.

- Premium 5. Strike 100.
- You pay 5 now.
- If the option expires with no value, the result is minus 5, plus any fees.
- You do not have to add more cash just because the coin moved, in this simple bought-option story.

Picture `atlas-derivatives-01.png`. You pay a premium of 5 for a right. You do not have to use the right. The most you lose in this example is 5.

Recap.

- Premium is what you pay for the right.
- Strike and expiry define the right.
- Doing nothing can lose the premium and no more, in the basic bought case.

Next lesson: Calls and puts.

#### Calls and puts

What you'll learn: a call is the right to buy at the strike, and a put is the right to sell at the strike.

A call becomes valuable when price is above the strike by more than the remaining costs. At expiry, a common example value is the greater of zero and price minus strike.

A put becomes valuable when price is below the strike. At expiry, a common example value is the greater of zero and strike minus price.

Subtract the premium you paid to see a profit. A valuable option can still be a loss if the premium was larger than that value.

Example.

- Strike 100. Premium 5. These numbers are an example.
- Call at expiry, price 110. Value is about 10. Profit is about 10 minus 5, which is 5.
- Call at expiry, price 100 or lower. Value is about 0. Result is about minus 5.
- Put at expiry, price 90. Value is about 10. Profit is about 5. Put at 100 or higher. Result is about minus 5.

Picture `atlas-derivatives-02.png`. A call with strike 100 and premium 5. At a price of 110 the example profit is 5.

Picture `atlas-derivatives-03.png`. A put with strike 100 and premium 5. At a price of 90 the example profit is 5.

Recap.

- Call benefits from a higher price.
- Put benefits from a lower price.
- Subtract the premium before you call it a profit.

Next lesson: Greeks in plain words.

#### Greeks in plain words

What you'll learn: delta, gamma, theta, and vega are names for how an option price responds to the coin, to the speed of that response, to time, and to volatility.

Delta is how much the option price changes when the coin changes by 1. A delta of 0.50 means about half a point, in a small move.

Gamma is how fast delta itself changes as the coin moves. Near expiry, gamma can jump. The option can feel stable and then not.

Theta is the drift from time passing, often a loss for the buyer each day if nothing else changes. Vega is the response to volatility. Higher volatility often raises an option's premium, so a buyer can gain from that and a seller can lose.

These are sensitivities, not tips. They move together. Quoting one number and ignoring the others will mislead you.

Example.

- Delta 0.50. The coin rises by 1. The option price rises by about 0.50, if the other inputs stay still.
- Theta 0.20 a day. A quiet day can mark the option down by about 0.20.
- Vega 0.10. If volatility rises by 1 point in the model's units, the option price rises by about 0.10.
- Gamma is the reason tomorrow's delta may not be 0.50.

Picture `atlas-derivatives-04.png`. Four plain meanings. Delta 0.50, gamma is the change in delta, theta 0.20 a day, vega 0.10.

Recap.

- Delta follows the coin.
- Gamma changes delta.
- Theta is time. Vega is volatility.

Next lesson: Basis.

#### Basis

What you'll learn: basis is the futures price minus the spot price, a gap you can measure today.

If the futures price is above spot, the basis is positive. If it is below, the basis is negative.

Into a dated expiry, that gap tends to shrink because the contract and the spot market meet. A perpetual uses funding instead of a single expiry to pull the prices together. Neither path is a schedule you can treat as a profit.

Basis is a price difference. It is not a yield until you define both legs, the costs, and the exit.

Example.

- Spot 100. Futures 103.
- Basis is 103 minus 100, which is 3.
- As a percent of spot, 3 divided by 100 is 3 percent.
- That 3 can shrink, widen, or flip sign. The number is today's gap.

Picture `atlas-derivatives-05.png`. Spot at 100 and a futures price at 103. The basis is 3.

Recap.

- Basis is futures minus spot.
- Dated contracts and perpetuals close the gap differently.
- A gap is not a profit by itself.

Next lesson: Trade plans.

## Professional

The last module is about behaviour you can repeat: a written plan, a journal, a respect for losing streaks, a way to notice urges, and a system small enough to review.

### Professional practice

None of these lessons raise the odds of a single idea. They stop you from changing the idea in the middle of the result.

#### Trade plans

What you'll learn: a plan names the entry, the stop, the cash at risk, and what would make the idea wrong, before you act.

Four lines are enough to start. Where you enter. Where the idea is wrong. How much cash that wrongness may cost. What you will do if price never arrives.

A target can be a fourth price, but a target without a stop is not a plan. It is a wish.

If you cannot write the stop, you are not ready to write the size. Return to position sizing.

Example.

- Entry 100. Stop 95. Distance 5.
- Cash at risk 100. Size 20, from the usual division.
- A target at 110 is 10 away, which is 2 times the distance. That is 2 R if the stop was the risk unit.
- The target is a scenario. The stop is the rule.

Picture `atlas-professional-01.png`. A plan card with entry 100, stop 95, cash risk 100, and target 110.

Recap.

- Write entry, invalidation, and cash before you act.
- A target is optional. A stop is not.
- If you change the stop later, write a new plan.

Next lesson: Journaling.

#### Journaling

What you'll learn: a journal records result in R so that different sizes can be compared, and expectancy is the average R in a sample.

One R is the cash you planned to lose if the stop was hit. A result divided by that cash is the R multiple.

Expectancy is the win fraction times the average win, plus the loss fraction times the average loss. Losses are negative numbers, so the second term subtracts.

A short sample is noisy. Ten rows can teach the arithmetic. They cannot prove a method. You need more rows before you trust the average.

The tools page will average a column of R values you paste. It does not know whether you followed the plan.

Example.

- Ten trades. Six wins. Four losses.
- Average win 1.5 R. Average loss minus 1 R.
- Expectancy is 0.6 times 1.5, plus 0.4 times minus 1.
- That is 0.9 minus 0.4, which is 0.5 R per trade in this sample.

Picture `atlas-professional-02.png`. Ten example results. Six are wins. Expectancy in this sample is 0.5 R.

Recap.

- Record R, not only cash.
- Expectancy is an average of a sample.
- A small sample is a lesson in arithmetic, not a verdict.

Next lesson: Risk of ruin.

#### Risk of ruin

What you'll learn: the percent you risk per idea decides how deep a losing streak cuts, even before you know the win rate.

Ruin here means the account is too small to follow the plan. You do not need a total loss for the plan to be dead.

Losses compound. Ten losses at 10 percent do not remove 100 percent. They leave 0.9 to the power 10, which is about 0.35, so about 65 percent of the account is gone.

Ten losses at 1 percent leave 0.99 to the power 10, which is about 0.90. The same streak hurts much less.

This is why the first module started at 1 percent as an example, not as a rule for your life. The percent is the lever.

Example.

- Start with 10000.
- Ten losses of 10 percent leave about 3490.
- Ten losses of 1 percent leave about 9044.
- The streak length is the same. The percent is the difference.

Picture `atlas-professional-03.png`. Ten losses at 1 percent leave about 90 percent of the account. Ten losses at 10 percent leave about 35 percent.

Recap.

- Streaks happen.
- A larger percent makes the same streak deeper.
- Compounding, not addition, is the right picture.

Next lesson: Psychology.

#### Psychology

What you'll learn: after a loss you will want to change size, and the want is not a new plan.

Two losses in a row feel like a pattern. Often they are the sample being small. The urge is to win the money back by doubling.

Write the size rule where you can see it. When the urge appears, read the rule. If you still want to change it, change it tomorrow in writing, not in the middle of the urge.

A journal helps because the feeling and the R are on different lines. You can be uncomfortable and still have followed the plan.

None of this removes fear. It gives the fear a place that is not the order button.

Example.

- The plan risks 1 percent.
- Two losses happen. The urge says to risk 2 percent on the next idea so the loss comes back faster.
- 2 percent is a different plan. It also doubles the damage of a third loss.
- The directory's answer is to keep 1 percent until you edit the written rule on purpose.

Picture `atlas-professional-04.png`. The written plan stays at 1 percent. The urge after two losses wants a bigger size. The urge is not a new plan.

Recap.

- The urge after a loss is predictable.
- Doubling size is a new plan.
- Edit rules in writing, away from the urge.

Next lesson: Building a system.

#### Building a system

What you'll learn: a small system is one market, one setup, one risk rule, and one day a week when you review the journal.

More setups feel like progress. They also make the journal impossible to read. Start with one pattern you can describe to someone else.

One market means one clock and one instrument. Adding a second market is a second system, even if the sentence looks the same.

The review day is part of the system. Without it, the journal is a diary. With it, you can ask whether the expectancy is still the one you wrote down.

When you want a word, use the glossary. When you want the arithmetic, use the tools. When you are new again on a topic, go back to Start here.

Example.

- Market: the coin you already studied, on the daily clock.
- Setup: a range box only when the daily structure from the structure module is not a strong one-way trend.
- Risk rule: 1 percent, size from cash divided by distance.
- Review: one day each week, read the R column before you add a second setup.

Picture `atlas-professional-05.png`. Four parts of a small system: one market, one setup, one risk rule, and one review day.

Recap.

- One market, one setup, one risk rule, one review.
- A second market is a second system.
- The glossary and the tools are there when the sentence needs a word or a number.

Next: Glossary.

## Tools

Position size. Cash at risk divided by the distance from entry to stop. Lesson: Position sizing.

Liquidation price. A teaching model. Long result is entry times (1 minus 1 divided by leverage, plus the maintenance rate). Short result flips the middle sign. Lesson: Liquidation.

Grid profit per gap. Box width divided by the number of gaps, compared with a round-trip fee at the midpoint. Lesson: Range and grid count.

## Glossary

One plain line for each word, then the lesson that uses it.

### A

**Account Model.** A ledger that stores a balance and a nonce per address. Lesson: Markets.

**Account Risk.** The fraction of equity you are willing to lose on one idea. Lesson: Risk basics.

**Active Addresses.** How many addresses sent or received in a window. Lesson: Wallets and venues.

**Address Poisoning.** A look-alike address planted in your history so you copy the wrong one. Lesson: Wallets and venues.

**Aggregator.** A router that splits a swap across several pools or venues. Lesson: Wallets and venues.

**Airdrop.** A distribution of tokens to addresses that meet published conditions. Lesson: Wallets and venues.

**Alert.** A message that fires when a price or a condition is met. Lesson: How a grid works.

**Allowance.** The maximum a spender may transfer under an approval. Lesson: Wallets and venues.

**AML.** Anti-money-laundering controls around the movement of value. Lesson: Order types.

**AMM.** An automated market maker that quotes a price from a pool's reserves. Lesson: Wallets and venues.

**AMM Pool.** The pair of token reserves that an automated market maker trades against. Lesson: Wallets and venues.

**Anchored VWAP.** VWAP started from a candle you choose, rather than from the session open. Lesson: Support and resistance.

**API Key.** A credential a program uses to talk to an account. Lesson: Wallets and venues.

**APR.** A quoted rate over a year, without assuming the rate is reinvested. Lesson: Wallets and venues.

**APY.** A quoted rate over a year that assumes the rate is compounded. Lesson: Wallets and venues.

**Arithmetic Grid.** Grid levels spaced by an equal price distance. Lesson: Range and grid count.

**Ask.** A resting sell order at a stated price. Lesson: Order types.

**ATR.** Average true range, a measure of recent movement size. Lesson: Support and resistance.

**AUSTRAC.** The Australian agency that registers digital currency exchange providers. Lesson: Order types.

**Auto-deleveraging.** A forced reduction of profitable positions when a venue cannot cover a deficit. Lesson: Options basics.

**Automation.** Letting software apply a rule you have already written. Lesson: How a grid works.

### B

**Backtest.** Running a written rule over past data to see what it would have done. Lesson: Journaling.

**Backwardation.** A futures curve where later expiries cost less than spot. Lesson: Options basics.

**Bad Debt.** Borrowing that is no longer covered by collateral the protocol can seize. Lesson: Wallets and venues.

**Base Asset.** The asset being priced, such as the coin in a pair. Lesson: Order types.

**Basis.** The gap between a derivative's price and the spot reference. Lesson: Perpetuals and dated contracts.

**Bearish Candle.** A candle that closed below its open. Lesson: Market structure.

**Best Bid and Offer.** The highest bid and the lowest ask, shown together. Lesson: Order types.

**Bid.** A resting buy order at a stated price. Lesson: Order types.

**Bitcoin.** The first widely used public cryptocurrency, a proof-of-work ledger with a fixed supply cap. Lesson: Markets.

**Block.** A batch of transactions added to the chain together. Lesson: Markets.

**Block Explorer.** A website that reads a chain and shows transactions, addresses, and contracts. Lesson: Wallets and venues.

**Block Reward.** The new coins plus fees paid to the producer of a valid block. Lesson: Markets.

**Block Time.** The target or typical gap between blocks. Lesson: Markets.

**Blockchain.** A shared ledger of transactions grouped into blocks. Lesson: Markets.

**BNB.** The native coin of BNB Chain. Lesson: Markets.

**Body.** The rectangle between a candle's open and close. Lesson: Market structure.

**Bollinger Bands.** A moving average with bands set a number of standard deviations away. Lesson: Support and resistance.

**Break of Structure.** A break that continues the prevailing swing direction. Lesson: Market structure.

**Breaker Block.** A failed order block that price has broken and may later retest. Lesson: Market structure.

**Breakout.** Price moving beyond a range or a marked level. Lesson: Market structure.

**Bridge.** A system that moves assets or messages between chains. Lesson: Markets.

**Bullish Candle.** A candle that closed above its open. Lesson: Market structure.

**Burn.** A destruction of tokens so they cannot be spent. Lesson: Markets.

**Buy-side Liquidity.** Resting buy orders, often stops, sitting above highs. Lesson: Market structure.

### C

**Candlestick.** A chart bar showing open, high, low, and close. Lesson: Market structure.

**Capital Allocation.** How much capital is assigned to a bot and its orders. Lesson: What a grid bot is.

**Centralised Exchange.** A venue that holds accounts and matches orders on its own books. Lesson: Order types.

**Chainlink.** A project that runs oracle networks feeding data to smart contracts. Lesson: Markets.

**Change of Character.** A break against the prevailing swing direction. Lesson: Market structure.

**Channel.** Two parallel lines containing a series of swings. Lesson: Support and resistance.

**Chart Pattern.** A named shape in price, such as a triangle or a double top. Lesson: Support and resistance.

**Circulating Supply.** The coins data providers count as available in the market. Lesson: Markets.

**Close.** The last traded price of a candle's period. Lesson: Market structure.

**Coin.** The native asset of a blockchain, used for fees and often for staking or mining. Lesson: Markets.

**Cold Wallet.** A wallet whose keys stay off the internet. Lesson: Wallets and venues.

**Collateral.** Assets locked to secure a borrow. Lesson: Wallets and venues.

**Composability.** The ability of protocols to call each other as building blocks. Lesson: Wallets and venues.

**Compounding.** Leaving results in so later size is calculated on a larger base. Lesson: Risk basics.

**Compression.** A tightening of range and volatility before a move. Lesson: Market structure.

**Concentrated Liquidity.** Liquidity posted only inside a chosen price range. Lesson: Wallets and venues.

**Concentration.** A large share of risk sitting in one asset, one venue, or one idea. Lesson: Building a system.

**Conditional Order.** An order that waits for a condition before it is sent. Lesson: Order types.

**Confirmation.** A block built on top of the block that contains your transaction. Lesson: Markets.

**Confirmation Bias.** Noticing the evidence that agrees with the view you already hold. Lesson: Psychology.

**Confluence.** Several independent observations lining up at the same area. Lesson: Support and resistance.

**Consensus.** The rule by which nodes agree on the next block. Lesson: Markets.

**Consolidation.** A pause where price trades in a tighter band. Lesson: Market structure.

**Constant Product.** A pool rule that keeps the product of the two reserves steady, before fees. Lesson: Wallets and venues.

**Contango.** A futures curve where later expiries cost more than spot. Lesson: Options basics.

**Correction.** A move against the prevailing impulse. Lesson: Market structure.

**Correlation.** How similarly two series move together. Lesson: Building a system.

**Correlation Regime.** A period in which assets move together more, or less, than usual. Lesson: Markets.

**Counterparty Risk.** The risk that the other side, or the venue holding the trade, fails. Lesson: Risk basics.

**CPI.** A consumer price index, a published measure of consumer inflation. Lesson: Markets.

**Cross Margin.** One pool of collateral shared across positions. Lesson: Options basics.

**Crypto-backed Stablecoin.** A stablecoin supported by on-chain collateral, usually overcollateralised. Lesson: Markets.

**Custody.** Who can actually move the assets. Lesson: Wallets and venues.

### D

**DAO.** An organisation whose decisions are executed by token votes and contracts. Lesson: Wallets and venues.

**Data Availability.** Whether the data needed to rebuild the chain's state is actually published. Lesson: Markets.

**Dated Future.** A futures contract with a set expiry and settlement. Lesson: Options basics.

**Dealing Range.** The swing high-to-low range used to map premium and discount. Lesson: Market structure.

**Death Cross.** A shorter average crossing below a longer average. Lesson: Support and resistance.

**Decentralised Exchange.** A venue where trades settle through contracts you sign yourself. Lesson: Order types.

**DeFi.** Financial protocols that run as smart contracts on public chains. Lesson: Wallets and venues.

**Delegation.** Assigning your stake, or your votes, to someone who acts for you. Lesson: Wallets and venues.

**Delta.** How much a position's value moves when the underlying moves. Lesson: Greeks in plain words.

**Delta-neutral.** A book whose net delta is near zero. Lesson: Greeks in plain words.

**Depeg.** A stablecoin trading away from its reference value. Lesson: Markets.

**Depth.** How much size rests near the current price. Lesson: Order types.

**Digital Currency Exchange.** A business that exchanges digital currency and fiat, in AUSTRAC's terms. Lesson: Order types.

**Discount.** The lower half of a dealing range in a structure map. Lesson: Market structure.

**Displacement.** A fast, one-sided move away from a prior area. Lesson: Market structure.

**Divergence.** Price and an oscillator making opposite swings. Lesson: Support and resistance.

**Diversification.** Spreading exposure across risks that do not all fail the same way. Lesson: Building a system.

**Doji.** A candle whose open and close are almost the same. Lesson: Support and resistance.

**Donchian Channel.** The highest high and lowest low of the last N candles. Lesson: Support and resistance.

**Double Bottom.** Two lows at a similar price with a peak between them. Lesson: Support and resistance.

**Double Top.** Two highs at a similar price with a trough between them. Lesson: Support and resistance.

**Downtrend.** A sequence of lower highs and lower lows. Lesson: Market structure.

**Drawdown.** A decline from a prior equity peak. Lesson: Risk basics.

**Drawdown Recovery.** The rise required to regain a prior equity peak. Lesson: Risk basics.

**Dusting.** A tiny unwanted transfer used to mark or to bait an address. Lesson: Wallets and venues.

**DXY.** A widely quoted index of the US dollar against a basket of currencies. Lesson: Markets.

### E

**Emission.** The ongoing issuance of new tokens. Lesson: Markets.

**Engulfing Candle.** A candle whose body fully covers the previous body. Lesson: Support and resistance.

**EOA.** An externally owned account, controlled by a private key rather than by contract code. Lesson: Markets.

**Equal Highs.** Two or more highs at nearly the same price. Lesson: Market structure.

**Equal Lows.** Two or more lows at nearly the same price. Lesson: Market structure.

**Equilibrium.** The midpoint of a marked dealing range. Lesson: Market structure.

**Equity Curve.** A plot of account equity after each result. Lesson: Risk basics.

**ERC-20.** The common standard for interchangeable tokens on Ethereum-style chains. Lesson: Wallets and venues.

**ETF.** An exchange-traded fund, a listed vehicle that holds a basket or a commodity-like asset. Lesson: Markets.

**ETF Flow.** The net creation or redemption of shares in a crypto-linked fund. Lesson: Markets.

**Ethereum.** A public blockchain built to run general-purpose smart contracts. Lesson: Markets.

**Event Log.** A structured note a contract emits while it executes. Lesson: Wallets and venues.

**Exchange Netflow.** Coins sent to known venue addresses minus coins sent out, over a window. Lesson: Wallets and venues.

**Expansion.** A widening of range after a quieter period. Lesson: Market structure.

**Expectancy.** The average result per trade in a sample. Lesson: Journaling.

**Expiry.** The moment a dated contract settles and ceases. Lesson: Options basics.

**Exponential Moving Average.** An average that weights recent closes more than older ones. Lesson: Support and resistance.

**Exposure.** How much of an asset or a factor the account actually holds. Lesson: Building a system.

### F

**Fair Value Gap.** A three-candle imbalance where wicks do not overlap. Lesson: Market structure.

**Fake Token.** A contract that copies a name or a ticker without being the asset. Lesson: Wallets and venues.

**False Breakout.** A move beyond a level that fails and returns inside. Lesson: Market structure.

**Fee Drag.** The share of each grid step consumed by fees and slippage. Lesson: How a grid works.

**Fiat On-ramp.** A path that turns government currency into crypto. Lesson: Order types.

**Fiat-backed Stablecoin.** A stablecoin that claims reserves of cash or cash-like assets. Lesson: Markets.

**Fibonacci Retracement.** Horizontal levels at fixed ratios of a prior swing. Lesson: Support and resistance.

**Fill or Kill.** An instruction to fill the whole order immediately or cancel it. Lesson: Order types.

**Finality.** The point after which a transaction is impractical or impossible to reverse under the rules. Lesson: Markets.

**Flag.** A small channel against the prior impulse. Lesson: Support and resistance.

**Flash Loan.** A loan that must be repaid inside the same transaction. Lesson: Wallets and venues.

**Floating P&L.** Another name for open, unrealised profit and loss. Lesson: What a grid bot is.

**FOMO.** Fear of missing out, the urge to chase a move already underway. Lesson: Psychology.

**Fork.** A split in the rules or in the chain history. Lesson: Markets.

**Forward Test.** Running a frozen rule on data, or on paper, after the rule was locked. Lesson: Journaling.

**Fully Diluted Valuation.** Price multiplied by the full supply, including coins not yet circulating. Lesson: Markets.

**Funding Interval.** How often perpetual funding is exchanged. Lesson: Funding rates.

**Funding Rate.** A periodic payment between long and short perpetual positions. Lesson: Funding rates.

**Futures Grid.** A grid run with derivatives exposure, often with leverage. Lesson: What a grid bot is.

### G

**Gas.** The fee unit that pays for computation and storage on a chain. Lesson: Markets.

**Geometric Grid.** Grid levels spaced by an equal percentage distance. Lesson: Range and grid count.

**Golden Cross.** A shorter average crossing above a longer average. Lesson: Support and resistance.

**Good till Cancelled.** A resting order that stays until it fills or you cancel it. Lesson: Order types.

**Governance.** The process that changes a protocol's parameters or code. Lesson: Wallets and venues.

**Governance Token.** A token that can vote on protocol parameters, under the protocol's rules. Lesson: Markets.

**Grid.** A set of predefined price levels with orders inside a range. Lesson: What a grid bot is.

**Grid Count.** How many levels sit inside the range. Lesson: Range and grid count.

**Grid Cycle.** One completed round trip between two grid levels. Lesson: How a grid works.

**Grid Level.** One order line inside the range. Lesson: What a grid bot is.

**Grid Profit.** Realised result from completed buy and sell cycles. Lesson: How a grid works.

**Grid Spacing.** The price or percentage gap between two levels. Lesson: Range and grid count.

**Gwei.** A small unit of ether used to quote gas prices. Lesson: Markets.

### H

**Halving.** A scheduled cut in the new-coin subsidy on some proof-of-work chains. Lesson: Markets.

**Hammer.** A small body with a long lower wick, after a decline. Lesson: Support and resistance.

**Hard Fork.** A rule change that nodes must adopt or they follow a different chain. Lesson: Markets.

**Hard Stop.** A stop order that sits in the market, not only in your notes. Lesson: Risk basics.

**Hardware Wallet.** A dedicated device that holds keys and signs on the device. Lesson: Wallets and venues.

**Hash.** A fixed-length fingerprint of some data. Lesson: Markets.

**Hashgraph.** A consensus structure that records who gossiped which event to whom. Lesson: Markets.

**HBAR.** The native token of the Hedera network. Lesson: Markets.

**Head and Shoulders.** A peak between two lower peaks, with a neckline through the troughs. Lesson: Support and resistance.

**Health Factor.** A protocol-specific score of how far a borrow sits from liquidation. Lesson: Wallets and venues.

**Hedera.** A public network that orders transactions with hashgraph consensus. Lesson: Markets.

**Hedge.** A position taken to offset an existing exposure. Lesson: Options basics.

**Hidden Divergence.** An oscillator extreme that disagrees with a pullback, studied inside a trend. Lesson: Support and resistance.

**High.** The highest traded price of a candle's period. Lesson: Market structure.

**Higher High.** A swing high above the previous swing high. Lesson: Market structure.

**Higher Low.** A swing low above the previous swing low. Lesson: Market structure.

**HODL Waves.** A chart of supply split by how long each coin has stayed unmoved. Lesson: Wallets and venues.

**Holder Concentration.** How much of the supply sits in the largest addresses. Lesson: Wallets and venues.

**Hot Wallet.** A wallet whose keys are on a machine connected to the internet. Lesson: Wallets and venues.

### I

**Iceberg Order.** A large order that shows only a slice of its size. Lesson: Order types.

**Immediate or Cancel.** Fill what you can right now, and cancel the rest. Lesson: Order types.

**Impermanent Loss.** How far a pool position lags simply holding the same coins. Lesson: Wallets and venues.

**Impulse.** A strong push in the direction of the current sequence. Lesson: Market structure.

**Indecision.** A candle or a cluster that does not close decisively either way. Lesson: Support and resistance.

**Index Price.** A composite spot reference used to anchor a derivative. Lesson: Options basics.

**Indicator.** A calculation on price, volume, or both, drawn to summarise the window. Lesson: Support and resistance.

**Inducement.** A minor swing that may attract stops before a larger level is tested. Lesson: Market structure.

**Initial Margin.** The collateral required to open a position. Lesson: Options basics.

**Inside Bar.** A candle whose high and low sit inside the previous candle. Lesson: Support and resistance.

**Insurance Fund.** A venue buffer that absorbs some losses beyond liquidated margin. Lesson: Funding rates.

**Interest Rate.** The price of borrowing money, set in markets and influenced by policy. Lesson: Markets.

**Invalidation.** The condition that means the original idea no longer holds. Lesson: Risk basics.

**Inventory.** The coins or contracts a grid still holds open. Lesson: Grid risk.

**Inverse Contract.** A derivative margined in the base coin, with a nonlinear payoff. Lesson: Options basics.

**Isolated Margin.** Margin assigned to one position, not to the whole account. Lesson: Options basics.

### J

**Journal.** A record of what you did, why, and what the result was. Lesson: Journaling.

### K

**Kelly Criterion.** A formula for a size that maximises growth under strong assumptions. Lesson: Risk basics.

**Keltner Channel.** An average with bands set from ATR rather than standard deviation. Lesson: Support and resistance.

**KYC.** Know-your-customer checks a venue uses to identify account holders. Lesson: Order types.

### L

**Lag.** The delay built into a calculation that uses past candles. Lesson: Support and resistance.

**Last Price.** The price of the most recent trade on that market. Lesson: Order types.

**Layer 1.** A base blockchain that settles its own consensus. Lesson: Markets.

**Layer 2.** A system that executes elsewhere and settles back to a layer 1. Lesson: Markets.

**Lending Market.** A pool that accepts deposits and lends them against collateral. Lesson: Wallets and venues.

**Leverage.** Borrowed exposure that magnifies both gains and losses. Lesson: Options basics.

**Limit Order.** An order that trades only at your price or better. Lesson: Order types.

**Linear Contract.** A derivative margined and settled in the quote asset. Lesson: Options basics.

**LINK.** The token associated with the Chainlink oracle network. Lesson: Markets.

**Liquid Staking.** Staking that gives you a token representing the staked position. Lesson: Wallets and venues.

**Liquid Staking Token.** A token that tracks a claim on staked coins and their rewards. Lesson: Wallets and venues.

**Liquidation.** A forced close when collateral no longer covers the venue's rule. Lesson: Options basics.

**Liquidation Price.** The price where margin may no longer support a leveraged position. Lesson: Options basics.

**Liquidation Threshold.** The collateral ratio at which a position may be liquidated. Lesson: Wallets and venues.

**Liquidity.** How easily size can trade without a large price move. Lesson: Order types.

**Liquidity Pool.** A cluster of resting orders, often beyond equal highs or lows. Lesson: Market structure.

**Liquidity Provider.** Someone who deposits assets into a pool so others can swap. Lesson: Wallets and venues.

**Liquidity Sweep.** A push beyond an obvious high or low that then reverses. Lesson: Market structure.

**Litecoin.** An early proof-of-work blockchain derived from Bitcoin's design. Lesson: Markets.

**Loan-to-value.** Debt divided by the value of the collateral. Lesson: Wallets and venues.

**Long.** Exposure that gains if the price rises. Lesson: Options basics.

**Long Grid.** A grid configured with bullish directional exposure. Lesson: What a grid bot is.

**Loss Aversion.** Feeling a loss more strongly than a gain of the same size. Lesson: Psychology.

**Lot Size.** The smallest quantity step the venue allows. Lesson: Order types.

**Low.** The lowest traded price of a candle's period. Lesson: Market structure.

**Lower High.** A swing high below the previous swing high. Lesson: Market structure.

**Lower Low.** A swing low below the previous swing low. Lesson: Market structure.

**Lower Price.** The bottom boundary of the grid. Lesson: What a grid bot is.

**LTC.** The native coin of Litecoin. Lesson: Markets.

### M

**MACD.** The difference between a shorter and a longer exponential average. Lesson: Support and resistance.

**MACD Histogram.** The gap between the MACD line and the signal line. Lesson: Support and resistance.

**MACD Signal Line.** An exponential average of the MACD line. Lesson: Support and resistance.

**Macro.** The economy-wide backdrop: rates, inflation, growth, and the dollar. Lesson: Markets.

**MAE.** Maximum adverse excursion, the worst open loss during a trade. Lesson: Journaling.

**Maintenance Margin.** The collateral floor below which a position can be liquidated. Lesson: Options basics.

**Maker.** The side that adds a resting order to the book. Lesson: Order types.

**Maker Fee.** The fee for an order that adds to the book. Lesson: Order types.

**Manipulation.** Trading or reporting that pushes a price or a metric away from an honest read. Lesson: Wallets and venues.

**Margin.** Collateral posted to support a derivatives position. Lesson: Options basics.

**Margin Call.** A demand to add collateral or reduce the position. Lesson: Calls and puts.

**Mark Price.** The reference price a venue uses for unrealised results and liquidation. Lesson: Options basics.

**Market Capitalisation.** Price multiplied by circulating supply. Lesson: Markets.

**Market Order.** An order that takes the best prices available now. Lesson: Order types.

**Market Regime.** The broad behaviour of the market you are in, such as trend or range. Lesson: Market structure.

**Market Structure.** The map of swing highs and swing lows on a timeframe. Lesson: Market structure.

**Market Structure Shift.** Another teaching label for a change of character on a chosen timeframe. Lesson: Market structure.

**Max Supply.** The ceiling on issuance, if the protocol has one. Lesson: Markets.

**Maximum Drawdown.** The deepest peak-to-trough decline in the sample. Lesson: Risk basics.

**Mean Reversion.** A tendency for price to move back toward a central value. Lesson: Market structure.

**Mempool.** The waiting room of transactions a node has seen but not yet included. Lesson: Markets.

**MEV.** Value captured by choosing the order or inclusion of transactions. Lesson: Wallets and venues.

**MFE.** Maximum favourable excursion, the best open gain during a trade. Lesson: Journaling.

**Mid Price.** The average of the best bid and the best ask. Lesson: Order types.

**Miner.** A participant who performs proof-of-work hashing to propose blocks. Lesson: Markets.

**Mitigation.** Price returning to an order block or a gap that was marked earlier. Lesson: Market structure.

**Momentum.** The speed of a price change over a window. Lesson: Support and resistance.

**Monte Carlo.** Many reshuffles of a sample, used to see a spread of paths. Lesson: Risk basics.

**Moving Average.** A smoothed average of recent prices. Lesson: Support and resistance.

**Multi-timeframe Analysis.** Reading the same market on a higher and a lower timeframe together. Lesson: Market structure.

**Multisig.** A wallet that requires several keys to approve an action. Lesson: Wallets and venues.

**MVRV.** Market value divided by a realised-value measure of the same supply. Lesson: Wallets and venues.

### N

**Neckline.** The line drawn across the troughs or peaks of a reversal pattern. Lesson: Support and resistance.

**Network.** The specific chain a transaction will be sent on. Lesson: Markets.

**Neutral Grid.** A futures grid without a strong long or short bias. Lesson: What a grid bot is.

**NFT.** A token that is unique or one of a distinct series. Lesson: Wallets and venues.

**Node.** A computer that keeps and checks the ledger. Lesson: Markets.

**Nonce.** A counter that orders transactions from one account. Lesson: Markets.

**Notional.** The face value of a position, before considering margin. Lesson: Options basics.

### O

**Off-chain.** Information or an agreement that is not settled on the public ledger. Lesson: Wallets and venues.

**On-balance Volume.** A running total that adds volume on up closes and subtracts it on down closes. Lesson: Support and resistance.

**On-chain.** Recorded on the public ledger and checkable by anyone running a node. Lesson: Wallets and venues.

**One Cancels the Other.** Two orders linked so a fill on one cancels the other. Lesson: Order types.

**Open.** The first traded price of a candle's period. Lesson: Market structure.

**Open Interest.** The stock of derivatives contracts still open. Lesson: Options basics.

**Optimistic Rollup.** A rollup that assumes batches are valid unless someone challenges them. Lesson: Markets.

**Oracle.** A feed that brings an off-chain or cross-market fact into a contract. Lesson: Wallets and venues.

**Order.** An instruction to trade a size at rules you set. Lesson: Order types.

**Order Block.** A candle cluster at the origin of a strong move, studied as a reaction area. Lesson: Market structure.

**Order Book.** The list of resting bids and asks at each price. Lesson: Order types.

**Order Size.** How much each grid order is allowed to trade. Lesson: What a grid bot is.

**Oscillator.** An indicator that swings inside a bounded or centred scale. Lesson: Support and resistance.

**Overbought.** An oscillator reading in its upper zone. Lesson: Support and resistance.

**Overcollateralisation.** Posting collateral worth more than the debt. Lesson: Wallets and venues.

**Overfitting.** A rule so tailored to past noise that it fails on new data. Lesson: Journaling.

**Oversold.** An oscillator reading in its lower zone. Lesson: Support and resistance.

### P

**Paper Trading.** Following the plan with recorded hypothetical fills and no capital at risk. Lesson: Journaling.

**Partial Fill.** An order that trades some of its size and leaves the rest. Lesson: Order types.

**Payoff Ratio.** The average win divided by the average loss. Lesson: Risk basics.

**Permissionless.** A system anyone can use without an account-opening decision by a firm. Lesson: Wallets and venues.

**Perpetual Future.** A derivative with no expiry, kept near spot by funding. Lesson: Perpetuals and dated contracts.

**Phishing.** A fake message or site that imitates a real service to steal a secret or a signature. Lesson: Wallets and venues.

**Pin Bar.** A candle with a long wick and a small body at the other end. Lesson: Support and resistance.

**Pivot Point.** A reference price derived from the prior period's high, low, and close. Lesson: Support and resistance.

**Point of Control.** The price with the most traded volume on a profile. Lesson: Support and resistance.

**Points Programme.** An off-chain or on-chain score that hints at a possible later reward. Lesson: Wallets and venues.

**Portfolio Heat.** The open risk currently in the account, added up. Lesson: Building a system.

**Position Sizing.** Choosing exposure so a loss stays inside a planned risk. Lesson: Risk basics.

**Post-only.** A limit that cancels itself if it would take liquidity. Lesson: Order types.

**Premium.** The upper half of a dealing range in a structure map. Lesson: Market structure.

**Price Action.** Reading structure from candles and swings without requiring an indicator. Lesson: Support and resistance.

**Price Impact.** How far your own order moves the price. Lesson: Order types.

**Private Key.** The secret that authorises a signature. Lesson: Wallets and venues.

**Process.** The repeatable steps you follow, scored separately from the result. Lesson: Psychology.

**Proof of Stake.** A consensus rule that puts staked coins at risk for proposing blocks. Lesson: Markets.

**Proof of Work.** A consensus rule that spends computation to propose blocks. Lesson: Markets.

**Protected Swing.** The swing low or high that must hold for the current sequence to stay valid. Lesson: Market structure.

**Protocol Fee.** A charge users pay for using a protocol. Lesson: Wallets and venues.

**Protocol Revenue.** The portion of fees that the protocol, the treasury, or the token actually keeps. Lesson: Wallets and venues.

**Proxy Contract.** A contract address whose logic can be replaced by an upgrade. Lesson: Wallets and venues.

**Public Key.** The key that others can use to verify your signatures. Lesson: Wallets and venues.

### Q

**Quote Asset.** The asset used to price the base, often a stablecoin or a fiat unit. Lesson: Order types.

### R

**R Multiple.** A result measured in units of the amount risked. Lesson: Risk basics.

**Range.** The upper and lower prices where a grid is meant to work. Lesson: What a grid bot is.

**Range High.** The upper edge of a sideways band, as distinct from a grid's upper setting. Lesson: Market structure.

**Range Low.** The lower edge of a sideways band, as distinct from a grid's lower setting. Lesson: Market structure.

**Range Thesis.** The reason you believe price will stay inside the planned band. Lesson: What a grid bot is.

**Realised Cap.** A supply value that prices each coin near the price when it last moved. Lesson: Wallets and venues.

**Realised P&L.** Profit or loss already locked by completed trades. Lesson: What a grid bot is.

**Rebasing Token.** A token whose balance changes automatically under a protocol rule. Lesson: Wallets and venues.

**Receipt Token.** A token that records your claim on a pool, a lend, or a vault. Lesson: Wallets and venues.

**Recovery Scam.** A second fraud that offers to retrieve funds already stolen. Lesson: Wallets and venues.

**Reduce-only.** An order that may only shrink an open position. Lesson: Order types.

**Reentrancy.** A bug where an outside call re-enters a contract before its books update. Lesson: Wallets and venues.

**Rejection.** A wick or a quick return showing price did not stay beyond a level. Lesson: Market structure.

**Relative Volume.** This candle's volume compared with its usual volume at that time. Lesson: Support and resistance.

**Reorg.** A replacement of recent blocks by a competing history. Lesson: Markets.

**ReportCyber.** The Australian Cyber Security Centre's place to report cybercrime. Lesson: Wallets and venues.

**Resistance.** An area where selling has repeatedly appeared. Lesson: Support and resistance.

**Restaking.** Using staked assets as security for additional services. Lesson: Wallets and venues.

**Retest.** A later return to a level that price has broken or rejected. Lesson: Market structure.

**Revenge Trading.** A new trade taken to get back a loss, rather than because the plan allows it. Lesson: Psychology.

**Risk Budget.** The total loss you will accept across open ideas at once. Lesson: Risk basics.

**Risk of Ruin.** The chance a sequence of losses hits a ruin threshold, under stated assumptions. Lesson: Risk basics.

**Risk per Trade.** The cash amount lost if the stop fills at the planned price. Lesson: Risk basics.

**Risk-off.** A mood in which investors prefer safer holdings and sell riskier ones. Lesson: Markets.

**Risk-on.** A mood in which investors prefer riskier assets. Lesson: Markets.

**Risk-reward Ratio.** The planned gain compared with the planned loss. Lesson: Risk basics.

**Rollup.** A layer 2 that posts transaction data or proofs to a base chain. Lesson: Markets.

**Round Number.** A psychologically obvious price such as a whole figure. Lesson: Support and resistance.

**RSI.** A momentum oscillator that compares average up closes with average down closes. Lesson: Support and resistance.

**Rug Pull.** A project that removes liquidity or control and leaves holders stranded. Lesson: Wallets and venues.

### S

**Sample Size.** How many observations sit behind a statistic. Lesson: Journaling.

**Sandwich Attack.** A pair of trades wrapped around someone else's swap to harvest their price impact. Lesson: Wallets and venues.

**Satoshi.** The smallest usual unit of bitcoin. Lesson: Markets.

**Scamwatch.** The ACCC site where Australians report scams. Lesson: Wallets and venues.

**Seed Phrase.** The recovery words that can recreate a wallet's keys. Lesson: Wallets and venues.

**Self-custody.** Holding the keys that can move your own assets. Lesson: Wallets and venues.

**Sell-side Liquidity.** Resting sell orders, often stops, sitting below lows. Lesson: Market structure.

**Sequencer.** The component that orders transactions on many layer 2s. Lesson: Markets.

**Settlement.** The process that closes a contract at expiry or pays a difference. Lesson: Options basics.

**Short.** Exposure that gains if the price falls. Lesson: Options basics.

**Short Grid.** A grid configured with bearish directional exposure. Lesson: What a grid bot is.

**Sideways Market.** Price oscillating inside a band without a sustained trend. Lesson: Market structure.

**Signature.** A cryptographic approval produced by a private key. Lesson: Wallets and venues.

**SIM Swap.** A takeover of your phone number so text codes go to someone else. Lesson: Wallets and venues.

**Simple Moving Average.** An average that weights each of the last N closes equally. Lesson: Support and resistance.

**Slashing.** A penalty that destroys part of a validator's stake. Lesson: Wallets and venues.

**Slippage.** The gap between the expected price and the fill. Lesson: Order types.

**Slippage Tolerance.** The largest price move you will still accept on a swap or an order. Lesson: Order types.

**Smart Contract.** A program stored on a chain that runs when a transaction calls it. Lesson: Markets.

**Smart-contract Risk.** The chance that contract code or its economic design fails. Lesson: Wallets and venues.

**Snapshot.** A recorded state of balances or actions at a chosen moment. Lesson: Wallets and venues.

**Solana.** A layer-1 blockchain that uses proof of stake and aims at high throughput. Lesson: Markets.

**SOPR.** Spent output profit ratio, a UTXO measure of whether moved coins are above their prior reference. Lesson: Wallets and venues.

**Spot Grid.** A grid that trades the cash market, without derivatives leverage. Lesson: What a grid bot is.

**Spread.** The gap between the best bid and the best ask. Lesson: Order types.

**Stable Swap.** A pool curve shaped for assets that should trade near one another. Lesson: Wallets and venues.

**Stablecoin.** A token designed to track a reference value, often one unit of fiat. Lesson: Markets.

**Staking.** Locking the native coin so a validator can take part in consensus. Lesson: Wallets and venues.

**Standard Deviation.** A measure of how far values sit from their average. Lesson: Support and resistance.

**Stochastic.** An oscillator that locates the close inside the recent high-low range. Lesson: Support and resistance.

**Stop Distance.** How far the invalidation sits from the entry, in price. Lesson: Risk basics.

**Stop Loss.** A predefined exit used to cap a loss or honour an invalidation. Lesson: Risk basics.

**Stop Order.** An order that becomes active only after a trigger price prints. Lesson: Order types.

**Stop-limit Order.** A stop that, once triggered, rests as a limit rather than a market order. Lesson: Order types.

**Sui.** A layer-1 blockchain with an object-based data model. Lesson: Markets.

**SUI.** The native token of the Sui network. Lesson: Markets.

**Support.** An area where buying has repeatedly appeared. Lesson: Support and resistance.

**Support and Resistance.** The pair of ideas: areas where declines or rallies have stalled before. Lesson: Support and resistance.

**Swing High.** A high with lower highs on both sides. Lesson: Market structure.

**Swing Low.** A low with higher lows on both sides. Lesson: Market structure.

**Swing Point.** Either a swing high or a swing low. Lesson: Market structure.

**Sybil.** Many addresses controlled by one actor to look like many users. Lesson: Wallets and venues.

### T

**Take Profit.** A predefined condition for closing a gain. Lesson: Order types.

**Taker.** The side that removes a resting order from the book. Lesson: Order types.

**Taker Fee.** The fee for an order that removes liquidity from the book. Lesson: Order types.

**Throughput.** How many transactions a network processes in a given time. Lesson: Markets.

**Tick Size.** The smallest price increment the venue allows. Lesson: Order types.

**Time in Force.** The instruction for how long an order is allowed to work. Lesson: Order types.

**Time Stop.** An exit that fires because too much time has passed. Lesson: Risk basics.

**Timeframe.** The period each candle represents. Lesson: Market structure.

**Timelock.** A required delay between approving a change and executing it. Lesson: Wallets and venues.

**Token.** A unit issued by a contract on an existing chain. Lesson: Markets.

**Token Approval.** Permission for a contract to move your tokens up to an allowance. Lesson: Wallets and venues.

**Tokenomics.** The supply, distribution, and value-capture rules of a token. Lesson: Markets.

**Total Supply.** The coins created so far, including those still locked. Lesson: Markets.

**Trade.** A match between two orders that produces a fill. Lesson: Order types.

**Trading Bot.** Software that sends orders when written conditions are true. Lesson: How a grid works.

**Trading Plan.** A written set of conditions for entry, size, invalidation, and review. Lesson: Journaling.

**Trailing Grid.** A grid whose range can move under written rules. Lesson: What a grid bot is.

**Trailing Stop.** A stop that moves in your favour under a written rule. Lesson: Risk basics.

**Transaction.** A signed instruction that changes ledger state. Lesson: Markets.

**Trend.** A persistent direction in swing structure. Lesson: Market structure.

**Trendline.** A straight line drawn across swing points in one direction. Lesson: Support and resistance.

**Triangle.** Converging trendlines that compress recent swings. Lesson: Support and resistance.

**Trigger Price.** The price that activates a bot or a conditional order. Lesson: Order types.

**True Range.** The widest of the bar's range and the gaps from the prior close. Lesson: Support and resistance.

**TVL.** Total value locked, the assets a method counts as deposited. Lesson: Wallets and venues.

**TWAP.** A time-weighted average price over a window. Lesson: Wallets and venues.

**Two-factor Authentication.** A second check, beyond a password, before an account action. Lesson: Wallets and venues.

### U

**Unbonding.** The waiting period before staked coins can move again. Lesson: Wallets and venues.

**Unlock.** The moment previously locked tokens become transferable. Lesson: Markets.

**Unrealised P&L.** Mark-to-market result on open inventory or positions. Lesson: What a grid bot is.

**Upper Price.** The top boundary of the grid. Lesson: What a grid bot is.

**Uptrend.** A sequence of higher highs and higher lows. Lesson: Market structure.

**Utilisation.** The share of a lending pool that is currently borrowed. Lesson: Wallets and venues.

**UTXO.** An unspent output, the unit Bitcoin-style chains track. Lesson: Markets.

### V

**Validator.** A participant who proposes or attests to blocks under proof of stake. Lesson: Markets.

**Value Area.** The price band that contains a set share of profile volume. Lesson: Support and resistance.

**Variance.** The square of standard deviation, a raw measure of scatter. Lesson: Risk basics.

**Vault.** A contract that pools deposits and runs a strategy for the depositors. Lesson: Wallets and venues.

**Vesting.** A schedule that releases allocated tokens over time. Lesson: Markets.

**Volatility.** How large and how fast price moves. Lesson: Market structure.

**Volatility Drag.** The damage variance does to a compounded path. Lesson: Risk basics.

**Volume.** How much traded during a period. Lesson: Support and resistance.

**Volume Profile.** A histogram of how much traded at each price. Lesson: Support and resistance.

**VWAP.** The volume-weighted average price over a chosen session. Lesson: Support and resistance.

### W

**Walk-forward.** A test that repeatedly tunes on one window and checks the next. Lesson: Journaling.

**Wallet.** Software or hardware that holds keys and asks a network to accept transactions. Lesson: Markets.

**Wallet Address.** The destination identifier you can publish. Lesson: Wallets and venues.

**Wallet Drainer.** A malicious page that asks you to sign a transaction which empties approved assets. Lesson: Wallets and venues.

**Whale.** An address or a cluster that holds a large share of an asset. Lesson: Wallets and venues.

**Whipsaw.** A signal that flips and then flips back, catching both sides. Lesson: Support and resistance.

**Wick.** The thin line from the body to the high or the low. Lesson: Market structure.

**Win Rate.** The share of trades in a sample that finished positive. Lesson: Risk basics.

**Withdrawal Whitelist.** A list of the only addresses an account is allowed to withdraw to. Lesson: Wallets and venues.

**Wrapped Asset.** A token that stands in for an asset on another chain or in another format. Lesson: Markets.

### X

**XRP.** The native token of the XRP Ledger. Lesson: Markets.

**XRP Ledger.** A public ledger designed for payments, with XRP as its native asset. Lesson: Markets.

### Y

**Yield Curve.** Interest rates plotted across different lending periods. Lesson: Markets.

**Yield Farming.** Moving assets to collect fees and incentive tokens. Lesson: Wallets and venues.

### Z

**ZK Rollup.** A rollup that posts a validity proof of its state change. Lesson: Markets.
