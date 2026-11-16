"""Curriculum additions for BP-02 to BP-11. Not rendered in this pass.

Each block is real teaching from course/curriculum/CURRICULUM.md.
BP-01 is written in lesson_scripts.bp01 and is not touched here.
"""

from __future__ import annotations

LEVELS = [24930, 25830, 26730, 27630, 28531, 29431, 30331]


def _shot(chapter: str, vo: str, visual: str | None = None) -> dict:
    shot = {
        "kind": "stack",
        "chapter": chapter,
        "vo": vo,
        "caption": vo if len(vo) < 90 else vo[:87].rsplit(" ", 1)[0] + ".",
        "items": [vo if len(vo) < 110 else vo[:107].rsplit(" ", 1)[0] + "."],
        "index": 0,
        "chart": "range_2023",
        "levels": LEVELS,
        "chart_title": "19 July 2023 to 16 October 2023",
        "reveal": 1.0,
        "reveal_from": 0.0,
    }
    if visual:
        shot["visual"] = visual
    return shot


def _block(chapter: str, lines: list[str], visual: str | None = None) -> list[dict]:
    shots = []
    for line in lines:
        shots.append(_shot(chapter, line, visual))
    return shots


EXTRA: dict[str, list[dict]] = {
    "bp-02-what-you-need": _block("Account in Australia", [
        "An exchange in Australia has to confirm who you are before you can deposit. That identity check is the first step, and it is the exchange's rule, not this course's.",
        "Australian exchanges register with AUSTRAC as virtual asset service providers. Check that register before you sign up. Registration is not a safety guarantee. ASIC licensing of exchanges starts on 9 April 2027. This lesson names the regulators only, never an exchange.",
        "Turn on a second code as well as your password. That second code is two-factor authentication. Then look for a paper or demo mode before any real dollars.",
    ]) + _block("Round trip", [
        "A pair such as BTC/AUD means you buy the base, bitcoin, with the quote, Australian dollars. A stablecoin is a coin designed to stay near one US dollar.",
        "A maker fee is the charge for an order that waits. A taker fee is the charge for an order that fills straight away. In this example both are 0.1 percent.",
        "On an example buy of 100 Australian dollars, 0.1 percent is 10 cents. The sell costs about 10 cents as well. The round trip is about 20 cents, which is 0.2 percent.",
        "Any gap smaller than that 0.2 percent loses money before the price does anything. Lesson 5 uses this as the test a gap has to pass.",
    ], "BP02-V03") + _block("Journal", [
        "A trading journal is a dated record of every bot: the plan, the changes, the fills, the fees, the result, and whether you followed the rules.",
        "The columns are the date, the pair, the band, the gaps, the money in the bot, the stop rule, the fills, the pairs, the fees, the result, and a yes or no for the rules.",
        "The summer band on the card is a bitcoin price in US dollars, so that example row is labelled BTC/USD. The fee example in Australian dollars is a separate row, labelled BTC/AUD. Do not mix the two currencies on one row.",
    ]) + _block("Scams", [
        "Nobody from this course will ask for a seed phrase, a private key, or an API secret. Those are the secret words or keys that unlock a wallet or account.",
        "If a message rushes you to send crypto, treat it as a scam. Moneysmart is the Australian guide for that warning. This is general information, not a product.",
    ]),
    "bp-03-what-is-a-grid-bot": _block("The grid cycle", [
        "A grid cycle is one fill and the order that follows it. When a buy fills, the bot places a sell one rung higher. When a sell fills, the bot places a buy one rung lower.",
        "A completed pair is one buy and its matching sell, both filled. The bot does that refill. You chose the band, the number of lines, and the amount.",
        "The number of grids is how many lines you set. The order size is your amount divided by the number of orders. In this example, 600 Australian dollars across 6 orders is 100 dollars each.",
    ], "BP03-V01") + _block("Inventory", [
        "Inventory is how much coin you hold against how much cash. After two buys you hold more coin. After the matching sell, one pair is complete and one coin parcel can still be waiting.",
        "A fill only swaps cash and coin. Whether you end up ahead depends on where the price goes next. That is not a promise that chopping earns.",
    ], "BP03-V04"),
    "bp-04-market-regimes": _block("Sorting a path", [
        "A regime is the shape of the path: a range, a trend, or a break. You sort it before you draw a grid, because a grid is built for a range.",
        "Count how often the close touches your band, and ask whether the highs are getting higher. Write one label and one reason. A feeling is not a label.",
        "In a range, pairs can finish. In a trend, you are left holding one side. In a break, the stop is the rule that applies.",
        "Near the top of the summer band the close came within one gap four times. Near the bottom it came within one gap three times. It is not four touches on each side. On the closes, the March drop is 11 to 12 March 2020, about 37 percent. The 13 March close was higher, so 12 to 13 March is not that break.",
    ], "BP04-V02"),
    "bp-05-spacing-and-range": _block("Spacing that clears the fee", [
        "Arithmetic spacing keeps the same number of dollars between lines. Geometric spacing keeps the same percent. Lesson 1 used equal dollar gaps. Both are ways to space, and neither is a recommendation.",
        "On an example of 100 Australian dollars, a gap of 0.5 percent is 50 cents. Take off the 20 cent round trip and 30 cents remain. That gap passes the fee test.",
        "A gap of 0.15 percent is 15 cents. The same 20 cent round trip is larger, so the pair loses 5 cents before the price moves. That gap fails.",
        "More lines mean more small pairs. Fewer lines mean fewer, wider pairs. Both still pay the fee on every fill.",
        "The band has to leave room for the real high and the real low, not only the closes. An order also has to clear the exchange minimum. In this example, 2,000 dollars across 20 orders is 100 dollars, above a 10 dollar minimum.",
    ], "BP05-V02"),
    "bp-06-entry-and-exit": _block("The loss you know first", [
        "The stop triggers on a daily close outside the band, confirmed by the next daily close still outside. One wick is not the trigger.",
        "You stop the bot, which cancels the waiting orders. Then you follow the written rule: keep the coin, or swap back to cash. You wrote which one before the entry.",
        "In this example the bot holds 2,000 Australian dollars, and the loss if the stop is met is about 249 dollars. You write that number before you start. It is the base of the sizing caps in lesson 10.",
        "Leave through the top and you hold mostly cash. Leave through the bottom and you hold mostly coin. The action is the sentence you already wrote.",
    ], "BP06-V04"),
    "bp-07-spot-paper-trading": _block("Paper before real money", [
        "A paper or demo run is the L-plate. You copy the page onto the form. Upper on the form is the top on your page. Lower is the bottom. You do not invent a new number on the screen.",
        "Record every check: the date, whether the close is inside, what you hold, and whether the stop rule still holds.",
        "Paper is practice. A real order spends money. You do not graduate because you feel ready.",
        "The example graduation rule is at least 14 days, every check done on time, the journal complete, and no rule broken. Then the smallest size your sizing rule allows, and not before.",
    ], "BP07-V05"),
    "bp-08-managing-and-monitoring": _block("The weekly review record", [
        "Once a week you write one row: what was realised, what is still unrealised, the fees, and whether you followed the rules. That row is a review record. It is not a profit target and not a forecast.",
        "Drawdown is the fall from a peak you already saw to a later low. You write the drawdown limit before you start, in the same way you wrote the stop.",
        "If the path has changed regime, or the stop has been met, you adjust or you stop. You do not drag the band to follow the price.",
        "A swap of crypto can be a capital gains event. Keep the journal. This is general information. Check ATO guidance or a registered tax agent.",
    ], "BP08-V02"),
    "bp-09-common-mistakes": _block("Four ways a plan breaks", [
        "A grid in a trend keeps one side filling and leaves you holding coin or cash. The pairs stop finishing. The stop you wrote is the exit, not a hope that the trend turns.",
        "A gap that is smaller than the round-trip fee loses before the price moves. In the example, a 15 cent gap against a 20 cent fee fails.",
        "Oversizing means one bot holds too much of the account. On an example account of 10,000 Australian dollars, 60 percent in one bot can lose about 750 dollars at the stop, which is 7.5 percent of the account.",
        "Revenge adding, or chasing the band, means moving the lines to follow the price. The rungs wait. You do not drag them.",
        "Two bots that move together are one risk, not two. Count them once when you look at the account.",
    ], "BP09-V03"),
    "bp-10-scaling-up": _block("Sizing caps", [
        "Scaling here means growing the money you give to bots, step by step, under written rules. It is never a promise of results.",
        "These are example caps on a 10,000 Australian dollar account, not a recommendation. One bot is at most 20 percent of the account, which is 2,000 dollars. The loss at the stop is at most 2.5 percent of the account, which is 250 dollars.",
        "The lesson 6 example, 2,000 dollars in the bot and about 249 dollars of loss at the stop, fits both caps. A feeling that you want more does not.",
        "You add money only after a review gate: enough time or enough pairs, every weekly check done, the rules followed, the journal complete, the regime still a range, and no drawdown limit hit.",
        "A step of 25 percent would make a 2,500 dollar bot. On a 10,000 dollar account that is 25 percent, so it breaks the 20 percent share cap as well as the loss cap. The loss at the stop would be about 311 dollars, or 3.1 percent. The share cap binds first, so you wait until the account is about 12,500 dollars, or you re-plan and test on paper. The rule decides.",
        "Correlated means the bots tend to rise and fall together, so they count as one bucket of risk, not two. Several bots share one risk cap. In this example the total loss at stop stays at or under 6 percent, which is 600 dollars. Two separate bots at about 249 dollars each use about 498 dollars, which is under the cap. Three full-size bots would not fit.",
        "If the account falls 10 percent from a peak, halve every bot. If it falls 15 percent, stop the bots and go back to paper until the review. A regime change, two band breaks in a month, a broken rule, or a late journal does the same.",
    ], "BP10-V02"),
    "bp-11-advanced-liquidation": _block("Your complete plan", [
        "This last part is opt-in. The spot plan is complete without borrowed money. A liquidation is a venue closing a borrowed position when the money you put up is used up. Coins you hold are not that mechanism.",
        "The 13 March 2020 candle is a public path of a violent day. Read the close on the close chart. The high and the low belong on the candle card only.",
        "We scale on spot only in this course. Borrowed size is a different risk, and the page crosses it out.",
        "Your complete plan is the band, the gaps, the stop, the journal, paper until the graduation rule passes, a weekly check, and new money only when the written caps and the review gate both pass.",
        "Explain it back. What a grid does. Why a pair can keep the gap after fees. What you do when price leaves. How you would add money, and when you would not.",
    ], "BP11-V03"),
}


WALK = {
    "bp-02-what-you-need": [
        "Open the notebook before any screen. Write today's date at the top and the word Example under it.",
        "Write the pair on the next line. If the prices are the summer bitcoin closes, write BTC/USD. If the fee sum is in Australian dollars, write BTC/AUD on its own line.",
        "Write the top and the bottom only after you have said what a range is. Then write one gap, and how you got it: the top minus the bottom, divided by the number of gaps.",
        "Write the stop in one sentence: two daily closes outside, then you stop the bot and follow the rule you already chose.",
        "Leave a blank column for fees and a blank column for whether you followed the rule. You fill those later. You do not fill them with a hope.",
        "Read the page aloud once. If a word on it has not been defined, stop and define it before you go on.",
    ],
    "bp-03-what-is-a-grid-bot": [
        "Draw seven lines. Mark the middle. Put buys on the lines below and sells on the lines above.",
        "Move a finger down two lines. Say: two buys can fill, so you hold more coin. Move it up one line. Say: one sell can fill, so one pair is complete and one coin parcel is still waiting.",
        "That finger path is an example. On the real summer closes the one-step pairs finished three times, and three parcels were still held at the end.",
        "Write the four settings under the drawing: top, bottom, number of lines, amount. Divide the amount by the number of orders and write the order size.",
        "Cross out any sentence that says the bot earns while price chops. Replace it with: a fill swaps cash and coin.",
        "Point at the stop and say who acts. You do, unless you have written that the bot's own stop setting is on.",
        "Close the page. The next lesson asks what shape of market this drawing is for.",
    ],
    "bp-04-market-regimes": [
        "Take the summer window first. Every close stayed inside. The close came near the top four times and near the bottom three times, counting within one gap. Label it a range, and write that reason.",
        "Take October 2023 to March 2024 next. The close left and kept going. Label it a trend. Higher closing peaks are the reason. Do not call the intraday wicks the reason while you are looking at a close line.",
        "Take March 2020 last. The drop on the closes is 11 to 12 March. Label it a break. 12 to 13 March rose, so it is not the label.",
        "A grid belongs on the range. It is the wrong tool for the trend and the break. Say that out loud before you draw any new lines.",
        "If you cannot decide, you are not ready to place lines. Write 'not sorted' and stop. A guess is not a regime.",
        "Put a date on the label. A label without a date cannot be checked next week.",
        "Next week you sort again. You do not keep last week's label because it was comforting.",
    ],
    "bp-05-spacing-and-range": [
        "The same market stall from lesson 1 applies here. The stall fee comes off every sale. If the gap is smaller than the two fees, the stall loses before the price moves.",
        "Write the round trip. Two times 0.1 percent is 0.2 percent. On 100 dollars that is 20 cents.",
        "Try a gap of 0.5 percent. The gross is 50 cents. After 20 cents of fees, 30 cents remain. Write 'passes'.",
        "Try a gap of 0.15 percent. The gross is 15 cents. After 20 cents of fees, you are down 5 cents. Write 'fails'.",
        "Choose equal dollars or equal percent and write which one. If you choose equal percent, the dollar gap is wider at the top than at the bottom.",
        "Count gaps, not lines. Twenty lines give nineteen gaps. Dividing the money by twenty orders is a different sum from dividing the band by nineteen.",
        "Put the high and the low on a candle, and widen the band if a real high or low sits outside. Then stop. Do not add another tool.",
    ],
    "bp-06-entry-and-exit": [
        "The stop covers a leave through the top and a leave through the bottom.",
        "Through the top you hold cash. Through the bottom you hold coin bought above the market, and the loss can keep growing until you act.",
        "Write the stop sentence at the top of the page, before any entry sentence.",
        "Use the two-close rule unless you have written that a bot setting will fire at a price during the day. Do not mix the two without saying which one is in force.",
        "Point the sentence at a real date. In the summer example the close left on 23 October 2023 and was still outside on 24 October.",
        "Under the sentence, write the loss if that rule is met. The example is about 249 Australian dollars on 2,000 dollars in the bot. Mark it Example.",
        "Write what you hold after a leave through the top, and after a leave through the bottom. Cash, or coin. Then write which one your rule keeps.",
        "Only then write the before sentence: the path is still inside, on a date you can point at.",
        "If the loss number is blank, the page is not finished. Sizing, the choice of how much, waits for lesson 10. Measuring the loss does not.",
    ],
    "bp-07-spot-paper-trading": [
        "Copy five fields and stop. Top. Bottom. Number of lines. Amount. The stop sentence. If the screen uses other names, write both names on the page so you do not mix them up.",
        "The lesson stops in front of the control that would send the order. Looking is allowed. Sending is not.",
        "For fourteen days, write one line a day. Date. Inside or not. What you hold. Whether the rule still holds.",
        "Do not write a pair count you did not count from closes. The long summer window finished three one-step pairs. A short paper run may finish none. None is a valid result.",
        "At day fourteen, read the graduation rule. Every line present. No rule broken. Journal complete. If one of those fails, you stay on paper.",
        "If all of them pass, the next size is the smallest size your written caps allow. You do not choose a size because the paper run felt good.",
        "File the paper page. Lesson 8 starts from it.",
    ],
    "bp-08-managing-and-monitoring": [
        "Remember the market stall. The closed sales are one line in the journal. They are not the whole result, and they are not a forecast. The fee still comes off each sale.",
        "On that day answer three questions and then close the chart. Inside or not. Which side of the middle. Does the written rule still hold.",
        "On the lesson 6 example bot, one finished pair nets about 3 dollars 60 after fees. Ten coins slipping by 3 dollars is about 30 dollars still unrealised. Write both as a review record, not a target.",
        "Write the drawdown from a peak you have already seen. If you have not written the limit for that fall, write the limit before you interpret the number.",
        "If the answers say the path has left and stayed out, you do the stop you wrote in lesson 6. You do not open a new band on the same afternoon.",
        "If the answers say you followed the rules, you write yes. If not, you write no, and you do not add money next week to make up for it.",
        "On a pair priced in another coin, such as a stablecoin, each buy and each sell swaps one crypto for another. The ATO lists swaps as disposals, which can be CGT events. Keep Australian-dollar records of every transaction for five years. This is general information, not tax advice. Check ATO guidance or a registered tax agent.",
    ],
    "bp-09-common-mistakes": [
        "A stop that only names the top misses the bottom. Through the bottom you hold coin, and the loss can keep growing.",
        "Read your page against four questions. Is the path still a sideways market? Does the gap clear the fee? Is one bot too large a share of the account? Did you move the lines to follow the price?",
        "A yes on the first question is the only one that supports keeping the grid. A trend or a break means the ladder was the wrong picture.",
        "A gap that fails the fee test cannot be saved by hoping for more fills. More fills would mean more fees.",
        "On the example 10,000 dollar account, 60 percent in one bot is the oversizing picture. About 750 dollars of loss is about 7.5 percent of the account. Write the cap from lesson 10 next to it.",
        "Moving the band after the price has left is chasing. A weekly check that the old rule still holds is not chasing. Say which one you did.",
        "If two bots move together, write them as one bucket before you tell yourself you are diversified.",
        "Fix the page, or stop the bot. Do not add a new indicator to hide the mistake.",
    ],
    "bp-10-scaling-up": [
        "Say the definition before any number. Scaling is growing the money you give to bots, step by step, under written rules. It is not a promise of results.",
        "On the example 10,000 dollar account the share cap is 2,000 dollars and the loss cap is 250 dollars. Both have to pass.",
        "A 2,500 dollar bot is 25 percent of that account, so it fails the share cap even before the loss of about 311 dollars fails the 2.5 percent cap.",
        "Twelve thousand five hundred dollars is the account size at which 2,500 dollars is 20 percent. Twelve thousand four hundred and forty would only clear the loss cap. The share cap binds first, so use twelve thousand five hundred.",
        "Two bots that do not move together can sit under the 600 dollar total. Three bots at the full loss of about 249 dollars each would be about 747 dollars, which is over 600. The picture keeps two.",
        "You step down by rule. Ten percent off a peak you have seen, you halve. Fifteen percent, you stop and return to paper.",
    ],
    "bp-11-advanced-liquidation": [
        "Keep the title card as Advanced: liquidation scenarios. The complete plan is the last chapter, not a new name for the lesson.",
        "Borrowed size can be closed by the venue when the money you put up is used up. Spot coins you hold are not closed that way. That is why this course scales on spot.",
        "Use one worked crash, on the closes: 11 March 2020 about 8 thousand, 12 March about 5 thousand, about 37 percent. The candle can show the high and the low. The close line does not pretend to be the low.",
        "Bring one plan to the last page. Summer band and three finished pairs, in US dollars, marked Example. Fee test, loss at stop, and caps, in Australian dollars, marked Example. Do not add those currencies on the same row.",
        "Say what you would do if two closes are outside. Stop the bot. Follow the written rule. Do not redraw the band the same day.",
        "Say what you would do before adding money. All six review checks, and both caps, and the total under 6 percent. If one fails, you do not add.",
        "If you cannot say those steps, the lesson to repeat is the one that teaches the missing step. The title of this lesson does not change.",
    ],
}


# Extra teaching so each unrendered lesson lands near 13 minutes at 161 words a minute.
# These are additions. They do not replace existing lines.
LENGTH = {
    "bp-02-what-you-need": [
        "Write the seven items as a list you can point at. A notebook. The three words, which are range, levels and stop. The pair. Paper or a demo. No secrets. A written stop. The word Example on every figure.",
        "Each item has a reason. The notebook is the plan you can check later. The three words stop you drawing a grid with no edges. The pair names what you buy and what you pay with. Paper or a demo is the L-plate. No secrets keeps the keys off the page. The written stop is the action. Example marks a teaching number.",
        "A maker fee is paid when your order waits and someone else trades with it. A taker fee is paid when your order fills straight away. A grid uses waiting orders, so the maker fee is the one to read first. The round trip is both sides.",
        "On the example of 100 Australian dollars at 0.1 percent each side, the buy costs 10 cents and the sell costs about 10 cents. Twenty cents is 0.2 percent. If the gap is smaller than that, the pair loses before the price moves. That is why lesson 5 tests the gap against the fee.",
        "The journal is the page you will open in lesson 8 and lesson 10. For every buy, sell or swap write the date and time, the amount, the value in Australian dollars at the time, the fee, which exchange or wallet, and what it was for. Export the history at least every three months. This is general information, not tax advice.",
        "If a message asks for a seed phrase, a private key, or an API secret, it is not this course. Those words unlock a wallet or an account. Moneysmart is the public Australian guide for scam warnings. Do not read a web address aloud. Check the register yourself.",
    ],
    "bp-03-what-is-a-grid-bot": [
        "Say the cycle in order. Price steps down and a buy fills. You hold more coin and less cash. The bot places a sell one rung higher. Price steps up and that sell fills. You hold less coin and more cash. The bot places a buy one rung lower. That is one completed pair.",
        "On the summer daily closes, that one-step cycle finished only three times. Three other buys were still waiting for their sell when the window ended. Three is the honest count. It is not a promise that the next window will do the same.",
        "The settings a bot asks for are the top, the bottom, how many lines, and how much money. The order size is the money divided by the number of orders. In the example, 600 Australian dollars across 6 orders is 100 dollars an order.",
        "You choose those settings. The bot only places and refills. It does not decide the stop unless you turned that setting on, and you write which one before you start.",
        "A fill is a swap, not a win. Cash becomes coin, or coin becomes cash. Whether you are ahead depends on the later sell, the fee, and whether the price comes back. Do not say the bot earns while the price chops. That sentence is a promise, and this course does not make it.",
    ],
    "bp-04-market-regimes": [
        "Sort the path before you draw the lines. A range keeps coming back inside the top and the bottom. A trend leaves and keeps making higher closing peaks, or lower ones. A break jumps away from the closes around it.",
        "On the summer window, closes came within one gap of the top four times and within one gap of the bottom three times. Say four and three. Do not say four touches on each side.",
        "The October 2023 to March 2024 window left the summer band and did not come back. That shape is a trend. The same leave is also the stop example from lesson 1. One path can be the end of a range and the start of a trend.",
        "On the closes, the sharp drop is 11 March 2020 to 12 March 2020, from about 8 thousand to about 5 thousand, about 37 percent. The 13 March close was higher than the 12 March close. Calling 12 to 13 March the break points at the wrong days.",
        "Write one label and one reason, then stop. If you cannot point at the dates, the label is a feeling. A grid is built for the range. It is the wrong picture for the trend and for the break.",
        "Look again each week. A range can become a trend. The old band does not move itself.",
    ],
    "bp-05-spacing-and-range": [
        "Two ways to space the lines. Arithmetic keeps the same number of dollars between them. Geometric keeps the same percent. The summer example used equal dollar gaps of about 900. Neither way is a recommendation.",
        "An example ladder from 100 to 200 in four steps is 100, 125, 150, 175 and 200 if the dollars are equal. The same ends with equal percent are about 100, 118.9, 141.4, 168.2 and 200. Count the gaps, not the lines. Four steps are four gaps.",
        "Test the gap against the fee. On 100 Australian dollars, a 0.5 percent gap is 50 cents. The round trip at 0.1 percent each side is 20 cents. Fifty minus 20 leaves 30 cents, so that gap passes. A 0.15 percent gap is 15 cents. Fifteen minus 20 is a loss of 5 cents, so that gap fails.",
        "More lines can mean more chances for a pair, and each pair is smaller. Fewer lines mean fewer pairs, and each gap is wider. The summer closes finished only three one-step pairs, so more lines do not mean many finished pairs.",
        "The band has to hold the real high and the real low of the window, not only the closes. Put those highs and lows on a candle card. Do not talk about a wick while a close-only line is on screen.",
        "Check the order size against the exchange minimum. In the example, 2,000 Australian dollars across 20 orders is 100 dollars an order. If the minimum were 10 dollars, that order would clear it. Twenty lines make nineteen gaps. Do not divide by the gaps and call it the same sum.",
    ],
    "bp-06-entry-and-exit": [
        "Write the finish before the start. The finish is the stop. In this course the example trigger is a daily close outside the band, and the next daily close still outside. One wick during the day is not the trigger.",
        "Then write what you will do. Stop the bot, so the waiting orders are cancelled. Then keep the coin, or swap it back to cash. You choose that sentence before you enter. Some bots have a price stop that can fire during the day. That is a different tool. If you use it, write that you use it. Otherwise you do the two-close rule by hand.",
        "Measure the loss before you start. In the example the bot is given 2,000 Australian dollars, and the loss if the stop is met is about 249 dollars. That number is what lesson 10 compares with the caps. This lesson does not choose the amount. It only measures the loss.",
        "Leave through the top and you are mostly in cash. Leave through the bottom and you are mostly in coin. The action is still the sentence you wrote. Do not invent a new one after the price has left.",
        "Say the finish sentence, point at the date, then say the before sentence. If either date is missing, the page is not ready.",
    ],
    "bp-07-spot-paper-trading": [
        "Paper or a demo is the L-plate. You practise the page before any real money. The form on the screen is a copy of the page. If the form says upper, your page says the top. If the form says lower, your page says the bottom. You do not type a new number because the box is empty.",
        "The lesson stops in front of the control that would send an order. You can look at the fields. You do not press send.",
        "Each check you write down has a date, whether the close is inside, what you hold, the fees if any, and whether the stop rule still holds. A two-week page is a practice of that habit. Do not invent a count of completed pairs. The summer window, which is ninety days, finished only three one-step pairs on the closes.",
        "The example graduation rule is at least fourteen days, every check done on the day you chose, the journal complete, and no rule broken. Then, and only then, the smallest size your sizing rule allows. Feeling ready is not the rule.",
    ],
    "bp-08-managing-and-monitoring": [
        "Once a week, three questions. Is the close still inside the band? Which side of the middle is it on? Does the written rule still hold? Two dates are enough to learn the habit: one inside, and one that has left. Then you stop. Watching all day does not change the path.",
        "The weekly row records what was realised, what is still unrealised, the fees, and whether you followed the rules. Drawdown is the fall from a peak you have already seen to a later low. Write the limit for that fall before you start.",
        "If the shape of the path has changed, or the stop has been met, you adjust or you stop. You do not drag the band so that it follows the price. Dragging the band is chasing.",
        "A grid can create many disposals. Each sell or swap can be a capital gains event. On a coin-quoted pair, each buy is a swap too. The journal is the record, in Australian dollars, kept for five years. This is general information, not tax advice. Check ATO guidance or a registered tax agent.",
    ],
    "bp-09-common-mistakes": [
        "Four mistakes show up again and again. A grid in a trend keeps filling one side, and the pairs stop finishing. A gap smaller than the round-trip fee loses before the price moves. One bot that is too large for the account turns a small loss into a large share of the account. Chasing the band means moving the lines after the price, which is not the same as a weekly check that the old rule still holds.",
        "On an example account of 10,000 Australian dollars, putting 60 percent in one bot can lose about 750 dollars at the stop. That is about 7.5 percent of the account. The caps in lesson 10 are there so that number is written first.",
        "Two bots that rise and fall together are one risk. Counting them as two makes the account look safer than it is.",
        "The summer leave was not a one-day surprise in the closes. The close left on 23 October 2023 and was still outside the next day. Give yourself the two closes. Do not call it a band that failed overnight if the chart does not say that.",
    ],
    "bp-10-scaling-up": [
        "Scaling means adding money, or a second bot, only after a written review. It does not mean a bigger feeling, and it does not mean borrowed money.",
        "Read the two caps before any step. On the example account of 10,000 Australian dollars, one bot is at most 20 percent, which is 2,000 dollars, and the loss at the stop is at most 2.5 percent, which is 250 dollars. The lesson 6 example, about 249 dollars of loss on 2,000 dollars, fits. A wish to add more does not.",
        "The review gate is six checks. Enough time or enough finished pairs. Every weekly check done. The rules followed. The journal complete. The path still a range. No drawdown limit hit. All six, or you do not add.",
        "If you add 25 percent to a 2,000 dollar bot you get 2,500 dollars. On a 10,000 dollar account that is 25 percent, so the share cap fails before you even look at the loss. The loss would be about 311 dollars, or 3.1 percent, which also fails the 2.5 percent cap. The share cap is the one that binds first. The account would need to be about 12,500 dollars before a 2,500 dollar bot is 20 percent. Until then, you wait or you re-plan on paper.",
        "Correlated means the prices tend to move the same way. Those bots are one bucket. You add their loss-at-stop figures together and count them once. Two bots that do not move together, at about 249 dollars of loss each, use about 498 dollars. The example cap is 600 dollars, which is 6 percent. Three full-size bots would go past that cap, so the picture stays at two.",
        "If the account falls 10 percent from a peak you have seen, halve every bot. If it falls 15 percent, stop them and go back to paper. A regime change, two leaves in a month, a broken rule, or a late journal is the same kind of step down.",
    ],
    "bp-11-advanced-liquidation": [
        "The title of this lesson stays Advanced: liquidation scenarios. Your complete plan is a chapter at the end. It is not a second title.",
        "This chapter is opt-in. The spot lessons stand without it. Liquidation is a venue closing a borrowed position when the money you put up is gone. Coins you already hold are not closed that way.",
        "On the closes, 11 March 2020 was about 8 thousand and 12 March was about 5 thousand. That is about a 37 percent fall. Read that on the close chart. The high and the low of the day belong on the candle card, not on the close line.",
        "The plan you can say back is one example, not a mix of currencies. The band, the gaps and the three finished pairs are the summer bitcoin prices in US dollars. The fee test, the loss at stop, and the caps are the Australian dollar examples, and you label them as dollars. You do not add a US dollar price to an Australian dollar row.",
        "Say the four questions. What a grid does. Why a finished pair can keep the gap only after fees, and only three times in that summer window. What you do when two daily closes are outside. When you would add money, and when you would step down. If you cannot answer one of them, that lesson is the one to watch again.",
    ],
}


def insert(sid: str, shots: list[dict]) -> list[dict]:
    """Add curriculum teaching. Existing lines are left as they are."""
    extra = [dict(shot) for shot in (EXTRA.get(sid) or [])]
    more = []
    for text in (LENGTH.get(sid) or []) + (WALK.get(sid) or []):
        parts = [part.strip() for part in text.split(". ") if part.strip()]
        for part in parts:
            if not part.endswith((".", "?", "!")):
                part += "."
            more.append(_shot("Added teaching", part))
    block = extra + more
    if not block:
        return shots
    at = next((i for i, shot in enumerate(shots) if shot.get("kind") == "outro"), len(shots))
    return shots[:at] + block + shots[at:]
