---
title: Find by question
slug: find-by-question
level: beginner
category: reference
related:
  - glossary
  - market-structure
  - risk-academy
last_reviewed: 2026-11-10
status: draft
---

# Find by question

Ask the question you actually have. Each answer is general information, two to four sentences, and a link to the page that goes further. Nothing here tells you to acquire or dispose of an asset.

## Getting started

**I am new. Where do I start?**
Start with what a grid bot is, then how a cycle works. When a word is new, open the [glossary](glossary.md). When you need to see a range on a chart, read what a [candle](market-structure.md#candles) is, then what a [trend and a range](market-structure.md#trend-and-range) are.

**What is Atlas?**
Atlas is a directory for grid bots. It teaches what a grid bot is, how it works, how to set one up, how to choose a range, how to size risk, how to monitor a bot, and the mistakes that usually come first. It does not hold your funds and it does not place orders. The scope is in the [disclaimer](disclaimer.md).

**Is this personal advice?**
No. The library is general information and does not take your circumstances into account. If you need advice about you, ask someone who is allowed to give it. The [footer line](footer-line.md) says the same thing in one sentence.

**Who publishes the site?**
The draft legal pages name Market Pros Proprietary Limited, ABN 19 679 270 387, and contact@stewartcrowncrypto.com. Stewart has confirmed those three. The effective date is still [EFFECTIVE_DATE], and the checklist link is still [CHECKLIST LINK]. Read the [terms](terms.md) before you treat the pages as final.

## Grids

**What is a grid?**
A grid is a ladder of price levels inside a range you choose, with orders at those levels. A finished round trip is one cycle. The definition and the neighbouring words are under [Grid](glossary.md#grid).

**What is the range for?**
The range is the upper and lower price where the bot is meant to work. It is a design choice, not a forecast of the high or the low. See [Range](glossary.md#range) and the [range thesis](glossary.md#range-thesis).

**What happens if I add more grid levels?**
Inside a fixed range, more levels mean tighter spacing and a smaller gross step. If the step does not clear fees and slippage, more trades do not repair it. That trade-off is [grid count](glossary.md#grid-count) and [fee drag](glossary.md#fee-drag).

**What is the difference between an arithmetic and a geometric grid?**
Arithmetic spacing keeps an equal price gap. Geometric spacing keeps an equal percentage gap, so the price gap grows as price rises. Both are defined in the [glossary](glossary.md#arithmetic-grid).

**Why can grid profit be positive while the account is down?**
Grid profit counts finished cycles. Coins still held are an unrealised result, and that result can be a loss. Read [grid profit](glossary.md#grid-profit) beside [unrealised P&L](glossary.md#unrealised-pnl).

**What is a neutral grid?**
A neutral grid is built for two-way trade inside a range, without a strong long or short tilt. It still carries inventory risk if price leaves the range. See [neutral grid](glossary.md#neutral-grid) and [sideways markets](market-structure.md#trend-and-range).

**When should I review a running grid?**
Review it when price lives outside the band you planned, when funding or fees have changed the arithmetic, or when the reason you chose the range is no longer true. The condition you named in advance is the [invalidation](glossary.md#invalidation).

## Candles and structure

**What does a candlestick show?**
One period's open, high, low, and close. The body is open to close. The wicks are the extremes beyond the body. The walk-through is [Candles](market-structure.md#candles).

**What is a swing high?**
A high with lower highs on both sides, under a rule you keep constant. Swing highs and swing lows are the posts of a structure map. See [Swings](market-structure.md#swings).

**How do I tell a trend from a range?**
An uptrend prints higher highs and higher lows. A downtrend prints lower highs and lower lows. A range is two-way trade without that sequence. Name the timeframe in the same breath, as the [trend section](market-structure.md#trend-and-range) says.

**What is a break of structure?**
A break of structure continues the swing direction you were already mapping, such as a move through the latest higher high in an uptrend. It is a description, not an order. Read [BOS and CHoCH](market-structure.md#break-of-structure-and-change-of-character).

**What is a change of character?**
A change of character is a break against the sequence, such as losing the higher low an uptrend needed. Teachers differ on wick versus close, so write your rule down. The same section covers it.

**What is a liquidity sweep?**
A push through an obvious high or low, where stops often sit, that then returns inside. You can call it a sweep only after the return. The idea is in [Liquidity](market-structure.md#liquidity).

**What is an order block?**
A candle or a small cluster at the start of a strong move, which some methods mark in case price returns. It is a hypothesis about the chart, not a visible institutional order. See [order blocks and fair value gaps](market-structure.md#order-blocks-and-fair-value-gaps).

**What is a fair value gap?**
A three-candle pattern that leaves a price gap because the wicks on either side of the middle candle do not overlap. A later return into the gap is something you can check. It is not an unfilled order you can audit.

**How do timeframes fit together?**
Use a higher timeframe for the larger map and a lower timeframe for the current push. They are nested, not a vote. The routine is [multi-timeframe work](market-structure.md#multi-timeframe-work).

**What do premium and discount mean?**
They are the upper and lower halves of a swing range you chose, split at the midpoint. Discount does not mean the asset is cheap. See the [dealing range](market-structure.md#premium-discount-and-the-dealing-range).

## Indicators

**What is a moving average?**
An average of recent closes, updated every candle. A simple average weights them equally. An exponential average weights the newest close more. Both lag. Formulas are on the [technical analysis page](technical-analysis.md#simple-moving-average).

**How is RSI calculated?**
RSI compares a Wilder-smoothed average of up closes with the same kind of average of down closes. RS is one divided into the other, and RSI is 100 minus 100 divided by one plus RS. A high reading means up closes dominated the window. It does not mean price must reverse. See [RSI](technical-analysis.md#rsi).

**What is MACD?**
MACD is a shorter exponential average minus a longer one, commonly 12 and 26. A signal line is an average of that difference, commonly 9. The histogram is the gap between them. The formulas and the misreads are under [MACD](technical-analysis.md#macd).

**What is VWAP?**
VWAP divides the sum of price times volume by the sum of volume for a session you define. It is the average price weighted by how much traded. It resets when the session resets. See [VWAP](technical-analysis.md#vwap).

**What do Bollinger Bands measure?**
A moving average, with bands a number of standard deviations away, commonly 2, using the population standard deviation in the original construction. Wide bands mean recent closes were dispersed. A tag of the band is a location, not an automatic fade. See [Bollinger Bands](technical-analysis.md#bollinger-bands).

**What is ATR for?**
Average true range is a smoothed measure of how far price has been moving, including gaps from the prior close. It is a distance, not a direction. A stop scaled in ATR still has to be run through the position-size formula. See [ATR](technical-analysis.md#atr) and [stops](risk-academy.md#stops).

**What is divergence?**
Price and an oscillator making opposite swings, such as a higher high in price with a lower high on RSI. It is a disagreement inside the window, not a clock. Regular and hidden forms are under [divergence](technical-analysis.md#divergence).

**What counts as confluence?**
Several independent observations in the same area. Three moving averages of similar length are one question asked three times. A higher-timeframe swing and a separate volatility measure are closer to independent. See [confluence](technical-analysis.md#confluence).

**Do chart patterns set a destination?**
No. A double top, a triangle, or a flag is a name for a shape. The textbook event is usually a break of a boundary you marked in advance. Measured distances in old books are descriptions of samples, not a level the current market must reach. See [patterns](technical-analysis.md#patterns).

## Risk

**How do I turn a stop distance into a size?**
Divide the cash you are willing to lose by the price distance to the stop. A wider stop means fewer units. The formula, and a labelled hypothetical example, are in [position sizing](risk-academy.md#position-sizing).

**What is one R?**
One R is the cash you planned to lose if the stop was hit. A result divided by that cash is the R multiple. It lets you compare trades of different sizes. See [R multiples](risk-academy.md#r-multiples).

**What is expectancy?**
The average result per trade in a sample: the win fraction times the average win, minus the loss fraction times the average loss. It describes that sample. It does not forecast the next trade. See [expectancy](risk-academy.md#expectancy).

**Why is a high share of winners not enough?**
Because the losers can be larger than the winners. Quote the payoff ratio and the sample size beside the share of winners. The expectancy section shows a hypothetical sample where this is visible.

**How much must equity rise to recover a drawdown?**
If the decline as a fraction of the peak is d, the rise needed on what remains is 1 divided by (1 minus d), minus 1. A deeper hole needs a much larger repair. Worked figures are labelled on the [drawdown section](risk-academy.md#drawdown-and-the-recovery-fraction).

**What does a Monte Carlo study actually do?**
It reshuffles a sample of results many times so you can see how deep the path can get even when the ending average is unchanged. It cannot invent trades the sample does not contain. See [Monte Carlo](risk-academy.md#monte-carlo).

**What should be true before size is live?**
You can state the cash at risk, the stop distance, the heat of the whole book, and the invalidation someone else could check. The checklist is at the end of the [risk academy](risk-academy.md#a-pre-trade-check).

## Venues and orders

**What is the spread?**
The best ask minus the best bid. It is a real cost of crossing the market, on top of fees. Depth is how much size sits there. Both are in [exchanges](exchanges.md#the-order-book-the-spread-and-depth).

**What is the difference between a maker and a taker?**
A maker adds a resting order. A taker removes one. Market orders are takers. The fee schedule follows the role, and the names are under [maker and taker](exchanges.md#maker-and-taker).

**What is a stop-limit?**
A trigger that, once hit, rests as a limit rather than a market order. It can fail to fill in a fast move. Choose it only when a missed fill fits the plan better than an open-ended fill. The full list of order types is on the [exchanges page](exchanges.md#order-types).

**Does Atlas recommend an exchange?**
No. The library explains centralised and decentralised venues as types. It does not name or rank firms. Registration status is a separate question, answered from AUSTRAC's own register.

**What is AUSTRAC registration?**
AUSTRAC registers businesses that provide certain virtual-asset services in Australia. The public list is the Virtual Asset Service Provider Register, and a name on it is a legal status, not a safety rating. The explanation and the official link are in [registration](exchanges.md#registration-in-australia-as-general-information).

## Keys and scams

**What is a seed phrase?**
The word list that recreates a wallet's private keys. Anyone who has the words has the wallet. There is no ordinary reset. Read [seed phrases and keys](security.md#seed-phrases-and-keys).

**Will Atlas ever ask for my seed phrase?**
No. We never ask for seed phrases, passwords or withdrawal-enabled keys. A message that asks for any of those is not from Atlas, not from Market Pros Proprietary Limited, and not from Stewart. The [security page](security.md) repeats the rule because it matters.

**What is two-factor authentication?**
A second check beyond the password, such as an app code or a hardware key. Text-message codes are weaker because a SIM swap can move the number. It does not help if you approve a prompt you did not start.

**What is a wallet drainer?**
A page that asks you to sign something dressed as a claim or a mint, which actually moves tokens you approved. Read the spender and the amount on the device screen. Reject what you did not mean. More patterns are in the [scam list](security.md#a-short-encyclopedia-of-scams).

**What is address poisoning?**
A look-alike address planted in your history so you copy the wrong string. Read the full address every time. The history list is not an address book.

**Where do I report a scam in Australia?**
Scamwatch, run by the ACCC, takes scam reports: the official site is linked from the [security page](security.md#where-to-report). ReportCyber, through the Australian Cyber Security Centre, is the channel when a crime has taken an account or money. Reporting does not itself return the funds.

**Someone offered to recover my coins. What now?**
Treat that as a recovery scam. Do not pay, and do not sign. Report the approach. The encyclopedia entry is on the security page, next to the official links.

## Ledger and DeFi

**What is the difference between a coin and a token?**
In this library a coin is the native unit of a chain, used for fees. A token is issued by a contract on a chain. The split, and why it matters, is in [coins, tokens, and categories](crypto-fundamentals.md#coins-tokens-and-categories).

**What is finality?**
The point after which a transaction is impractical or impossible to reverse under the chain's rules. A final transfer cannot be recalled by support. See [transactions](crypto-fundamentals.md#transactions).

**What is gas?**
The fee unit that pays for computation. A complicated call costs more than a simple transfer, and a rejected call can still cost a fee. Networks and fees are in [crypto fundamentals](crypto-fundamentals.md#networks-fees-and-scaling).

**What is a stablecoin depeg?**
The market price leaving the reference value the token is built to track. Causes include reserves, liquidity, and oracle faults. Holding several stablecoins is not diversification if they share an issuer or a pool. See [stablecoin](glossary.md#stablecoin) and [depeg](glossary.md#depeg).

**What is impermanent loss?**
The gap between a liquidity position and simply having held the same coins, caused by a change in relative price. Fees can narrow it and do not erase it. See [impermanent loss](glossary.md#impermanent-loss).

**What is a health factor?**
A protocol-specific score of how far a collateralised borrow sits from liquidation. The formula is not the same on every lending market. Treat the liquidation line as a cliff. See [health factor](glossary.md#health-factor).

**Where does a durable DeFi fee come from?**
From use: trading fees, borrower interest, or another service someone paid for. Token emissions are a distribution of new tokens, not the same thing. Separate them before you compare headline rates. See [yield farming](glossary.md#yield-farming) and [protocol revenue](glossary.md#protocol-revenue).

**What is MEV?**
Value captured by ordering or inserting transactions, which ordinary users feel as a worse fill. The defences you control are trade size, slippage limits, and routing. The definition stops there on purpose. See [MEV](glossary.md#mev).

**What is Solana?**
A public layer-1 chain whose native coin is SOL, built around short block times and parallel execution. The short primer is [here](solana-primer.md). It is a definition, not a view on the price.

## Process

**What belongs in a journal?**
The setup, the size, the stop, the result in R, and whether you followed the plan. Without that record, expectancy is a feeling. See the [journal lab](journal-lab.md) and the glossary entry [journal](glossary.md#journal).

**What is overfitting?**
A rule tuned until it memorises one sample, including the accidents. A forward test on data you did not use for tuning is the basic check. See [overfitting](glossary.md#overfitting).

**What is the difference between hot and cold storage?**
Hot means the keys are on an online device. Cold means they are not. Cold reduces remote theft and does not forgive a lost seed. See [wallets](security.md#wallets).

**Can a calculator on Atlas tell me what to do?**
No. A calculator applies a formula to figures you type. Change an input and the answer changes. The output is an illustration of the arithmetic, which is the standard the [risk page](risk-academy.md) uses for every worked number.
