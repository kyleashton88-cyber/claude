# BP-01 Introduction — spoken script

Source at commit `205aea3` on branch `cursor/blueprint-professional-rebuild-d1f6`: `course/blueprint-rework/lesson_scripts.py`, function `bp01()`. Approved spoken edits of 25 Nov 2026 applied in this copy: 8:57am AEDT ('closing price', legal M1) and 9:09am AEDT (legal R1 replaces M1), and 11:47am AEDT (F2 roadmap line). Not rendered; the c80ee62 mix still speaks the old text.

## GridBot Blueprint

GridBot Blueprint, lesson 01, Introduction.

## Hook

By the end of this series you will understand what a grid bot does. It is a small program that places these orders for you. You will learn when it can capture bounces, and where it loses. You will know how to plan one, test it on paper, run it, check it, and change the capital you give to bots only under written risk rules. This is education, not a promise of results. Price often moves sideways, bouncing between the same top and bottom instead of leaving. A grid is a ladder of waiting orders, called limit orders, built for that bouncing. When price runs one way and stays there, the grid has nothing left to do. And if price falls through the bottom, coin means the crypto itself, and you are left holding the coin, and it is worth less.

## Objectives

By the end you will know what a grid bot places.

You will see that idea on one real path from 2023.

You will be able to say the stop rule in one sentence.

## Example

When a chart says Example, it means a real past price used as an example, not a forecast.

## Crypto

Crypto is a digital asset, such as bitcoin. You do not need to have bought any before this lesson.

## Exchange

An exchange is the website or app where you swap Australian dollars for crypto, and crypto back to dollars. This course does not name one, and it does not send an order.

## Cash and coin

Cash is money you can spend. Here that means dollars, or a stablecoin, a crypto coin built to stay at one US dollar. We treat it like cash in this lesson, but it can drop below a dollar. Coin is the crypto, such as bitcoin.

## Buy and sell

An order is an instruction to buy or sell. A buy order swaps cash for coin. A sell order swaps coin back to cash, and you can only sell coin you already hold, on a spot account. A spot account is the normal account on an exchange. You own the coin you buy, and nothing is borrowed.

## The idea

A bot is software that places and refills orders for you. You start with some cash and some coin, so there is something to buy with and something to sell. A grid bot places waiting buy orders on lines below the current price and sell orders on lines above it, inside a top and a bottom you choose. The space between your top and your bottom is called the range. The sells need some coin, so a grid starts with part cash and part coin, and that is a description, not advice about what to hold.

## Limit order

A limit order is an order that waits at a price you choose. It does not chase the price. Chasing the price would mean moving the order to follow wherever the price has gone.

## Fill

An order fills when the price reaches its line and the trade happens. Until then, the order is only waiting.

## A ladder

Think of a ladder leaned on a wall. The rungs wait, and they do not chase you. A rung is one price where an order waits. The gap is the space between two rungs. The ladder is the analogy, and the chart beside it is the real past path.

## The three parts

The range is the top rung and the bottom rung. The levels are the rungs between them. The stop is the written rule for leaving.

## The range

The range is the top line and the bottom line, taken from the path. Hindsight: this range is drawn after the fact. The chart is bitcoin's real daily closing prices from 19 July to 16 October 2023. Every closing price in this window stayed between those two lines.

## The levels

Six gaps of about 900 dollars each sit between the bottom line and the top line. Each gap is about 900 dollars: the top line minus the bottom line, divided by six. It is one step between lines, not the whole range. Seven lines make those six gaps. The levels are the prices on the rungs where limit orders wait.

## Buys and sells

Buy orders wait on lines below the current price. Sell orders wait on lines above it. Each fill changes what you hold: a buy fill adds coin, and a sell fill adds cash. You choose the range, the gaps and the money. The bot places each order.

## Bot and you

After a fill, the bot places the opposite order one rung up or down. A buy fill gets a sell one rung higher. A sell fill gets a buy one rung lower. You still write the stop, and you act when that rule is met. The bot does not decide the stop for you unless you turned that setting on, and you write which one before you start.

## How a grid can capture bounces

Think of a market stall. The stallholder buys stock a little cheaper and sells it a little dearer, and pays a fee on every sale. Exchanges charge a small fee on each trade. A grid can do that while price bounces inside the range. A bounce means price moves down and back up, or up and back down, and stays inside. One buy at a lower line and the later sell of that same coin is one pair. On these daily closing prices, the July to October example window finished only three pairs, each a buy and a sell on lines next to each other. The sell line is higher, so the cash that comes back is more than the cash that left, before the fee. A fee is what the exchange charges when an order fills. The fees come out of what the pair makes. If the fees are larger than that, the pair keeps nothing. This is not a promise. The pair finishes only if price does bounce and both orders fill.

## One day

The daily closing price is the last price of the day. Crypto trades all day, so the day is cut at a set time. This lesson uses the end of each UTC day, the world's standard clock, which is 11am Sydney time in daylight saving, 10am otherwise. This is a simple candle that shows the day's high, low and closing price. Traders call it a candle because the full version has a thick body and a thin wick, like a candle. Here we only need the high, the low and the closing price. This candle is 19 July 2023. The high, the low, and the closing price are labelled.

## The whole window

The example is Bitcoin's public daily price in US dollars. From 19 July 2023 to 16 October 2023, every one of those days closed inside the range. The closing price crossed the seven lines 28 times in that window. The count is an example, not a forecast. We do not need to read each day. The shape is the lesson, and it is marked Example. Worked check: 19 July 2023 to 16 October 2023. The low is the bottom line. The high is the top line. Nothing on this card is an order.

## Crossings

Those 28 crossings, each time the price crosses a line, are not 28 results. A crossing only means the closing price moved from one side of a line to the other. A pair is finished only when a buy and its later sell have both filled, and only after the fee. The price can cross many lines and still leave you holding coin if it walks out through the bottom.

## One pair

You can buy part of a coin. Here we buy one hundredth of a bitcoin, 0.01. 900 dollars times 0.01 bitcoin is 9 dollars before fees. In this example a buy waiting at the lower of these two lines was reached on 17 August 2023, and the sell one line above was reached on 29 August 2023. The card shows the gap, then the two fees, then what is left. Each fee is 0.1 percent of the whole trade, not of the profit: about 27 cents on the 267 dollar buy and about 28 cents on the 276 dollar sell, about 54 cents together. That is about 8 dollars 46 after fees, for one small pair. It happens only if the price comes back up through the sell line. If the price leaves through the bottom, you still hold the coin, and the pair never finishes. This card is not money you made. Past results don't predict future results.

## When price leaves the range

Now watch what you hold when the price leaves the range and stays out. Above the range the sells have filled and you are holding cash, with nothing left to sell. Below the range the buys have filled and you are holding coin, with nothing left to buy. That is why the way down matters most: every buy fills, and you are left holding coin.

## The stop

Here is that stop rule on the real path. It triggers if a daily closing price is outside the range, through the top or the bottom, and the next daily closing price is still outside. Then the idea is finished. You stop the bot, which cancels the waiting orders, and do what you wrote: keep the coin or swap to cash. A bot's automatic stop is a price that can fire during the day. This course uses the two daily closing prices, unless your written plan says you turned on a price stop. This is a teaching rule, not a recommendation. The stop is your written rule for when you stop the bot. On 23 October 2023 the closing price finished above the top line, and the next day was still above it.

## Downside

Through the top, the sells have filled and you hold cash. Through the bottom, the buys have filled and you hold coin that you bought above where the price is now.

That loss can keep growing until the stop acts. You stop the bot either way, then you follow the written rule. The bot does not decide the stop unless you turned that setting on. EXAMPLE, made up: three buys fill on the way down. One hundredth of a bitcoin at 27,630 is 276 dollars 30. One hundredth at 26,730 is 267 dollars 30. One hundredth at 25,830 is 258 dollars 30. Together that is 801 dollars 90. Three buys of 0.01 is 0.03 bitcoin. At 24,000, that is 720 dollars. A little below the range, at a made-up price of 24,000, that coin is worth 720 dollars. You are down 81 dollars 90 before fees, and the loss keeps growing until your stop acts.

## No promise of results

A common mistake is thinking the bot predicts the price. It does not. It only waits. Another mistake is starting with no written stop. There is no promise of results in this lesson. Numbers marked Example are teaching numbers, not advice.

## L-plates

Paper or demo trading is like driving with learner plates, or training wheels: you practise with pretend money before anything is real. Lesson 7 shows you how.

## The map

Steps one to six. This introduction is step one. Then what you need. Then exactly what a grid bot does, order by order. Then market regimes. Then choosing grid spacing and range. Then entry and exit rules. Steps seven to eleven. Then a paper test. Then weekly checks. Then common mistakes. Then scaling up under written rules. Then an optional wrap-up of the spot page, and what this course does not cover.

## The checklist is next

The next lesson is a checklist you write on paper, before any screen.

## One sentence to keep

In short: a grid waits, it buys lower and sells higher while price bounces, the fees come out of what the pair makes, and if a daily closing price leaves and stays out, you stop the bot and follow the rule you wrote.

## Self-check

Check yourself. Why does a grid start with some coin as well as cash? Because the sell orders need coin you already hold.

In the example pair, why is the net about 8 dollars 46 and not the full 9 dollars? The two fees come out first.

Price closes above your top line, and the next day's closing price is still above it. What do you do, and who does it? You stop the bot and follow your written rule, by hand, unless you turned on the bot's stop setting.

## Your turn

Your turn. On paper, write the top and the bottom, one gap, and the stop rule.

Say what you will do if a daily closing price leaves the range and the next closing price is still outside. Pause the video and write your answer before you go on.

No real order is sent in this lesson. Paper practice comes in Lesson 7, and real money only after your written graduation rule. A graduation rule is the written test you pass on paper first. You draw the idea. If a screen appears later, it should be a copy of the page, and only on paper or demo.

## No secrets

Bring a notebook, and no secrets: no seed phrase, private key or API secret. A seed phrase or private key is the master password to a crypto wallet. An API secret is a key that lets an app place trades on your account, and sometimes move money out of it. Never share a seed phrase, a private key or an API secret. Nobody from this course will ask for one.

## The pair, next

The pair, in the next lesson, is the two things you swap, like bitcoin and US dollars.

## Recap

A grid bot places waiting buys below the current price and waiting sells above it, inside a range you choose.

A finished pair buys lower and sells higher. The fees come out of what the pair makes. In the example that was about 8 dollars 46, and it is not a promise.

Leave through the top and you hold mostly cash. Leave through the bottom and you hold mostly coin.

If a daily closing price leaves the range and the next closing price is still outside, you stop the bot and follow the rule you wrote.

## Next

Next lesson: What you are going to need. Bring your notes: your range, your gaps and your stop rule. Keep the word Example on every practice figure. Next lesson you will write the page of what you need, before any screen.
