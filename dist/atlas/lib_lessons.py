"""Atlas lesson text. Plain sentences. Made-up numbers are marked as examples."""

LEVELS = [
    {
        "id": "beginner",
        "title": "Beginner",
        "blurb": "Start here if the words are new. You learn what a market is, how a candle is drawn, how an order waits or crosses, where coins can sit, and how a small risk limit becomes a size. Then you learn to name a trend, a swing, and a break.",
        "modules": [
            {
                "id": "foundations",
                "title": "Foundations",
                "blurb": "These five lessons are the floor. Later lessons use these words without stopping to redefine them.",
                "lessons": [
                    {
                        "id": "markets",
                        "title": "Markets",
                        "learn": "a market is where a buyer and a seller agree a price, and the printed price is that agreement.",
                        "paragraphs": [
                            "A market is a meeting place for orders. Someone wants to buy. Someone wants to sell. When they agree, a trade prints.",
                            "The printed price is not a vote about the future. It is the last agreement. The next agreement can be higher or lower.",
                            "Buyers and sellers can both be wrong about what they wanted a minute ago. The tape only shows the trades that happened.",
                            "You do not need a named venue to understand this. Any place that matches orders works the same way at this level.",
                            "Next you will see how one period of those trades is drawn as a candle.",
                        ],
                        "example": [
                            "A buyer is willing to pay 100.",
                            "A seller wants 110.",
                            "They meet in the middle and a trade prints at 105.",
                            "105 is the last price. It is not a promise that the next trade is 105.",
                        ],
                        "recap": [
                            "A trade is an agreement.",
                            "The last price is history, not a forecast.",
                            "The same idea fits any venue.",
                        ],
                        "images": ["atlas-foundations-01.png"],
                    },
                    {
                        "id": "candles",
                        "title": "Candles",
                        "learn": "a candle compresses one period into the open, the high, the low, and the close.",
                        "paragraphs": [
                            "Pick a clock. One minute, one hour, one day. A candle covers that clock and then the next candle starts.",
                            "The open is the first trade in the period. The close is the last trade. The high is the dearest trade. The low is the cheapest trade.",
                            "The body is the box from open to close. The wicks are the lines beyond the body. A wick shows that price visited a level and did not stay there by the close.",
                            "A wide body means the close is far from the open. A long wick means the extreme did not hold.",
                            "Colour is a convenience. The four prices are the fact. Next you will see how an order can wait at a price or cross the spread.",
                        ],
                        "example": [
                            "Open 100. High 108. Low 97. Close 104.",
                            "The body runs from 100 to 104. That is 4.",
                            "The upper wick runs from 104 to 108. The lower wick runs from 100 to 97.",
                            "Price traded at 108, but the period ended at 104.",
                        ],
                        "recap": [
                            "Four prices define the candle.",
                            "The body is open to close.",
                            "Wicks are visits that did not become the close.",
                        ],
                        "images": ["atlas-foundations-02.png", "atlas-foundations-03.png"],
                    },
                    {
                        "id": "order-types",
                        "title": "Order types",
                        "learn": "a limit order waits for your price, and a market order pays the price that is available now.",
                        "paragraphs": [
                            "An order book is a list. Bids are buys that are waiting. Asks are sells that are waiting. The best bid is the highest waiting buy. The best ask is the lowest waiting sell.",
                            "The spread is the gap between those two. Crossing the spread costs you that gap, plus any fee.",
                            "A limit order rests at the price you choose. It may not fill. A market order fills now against resting orders. You do not choose the exact print.",
                            "A stop is a trigger. When price reaches it, the stop becomes a market or a limit, depending on the rule you set. The name stop does not mean the loss is capped until you see the fill.",
                            "Next you will see the difference between coins you can move yourself and coins sitting at a venue.",
                        ],
                        "example": [
                            "Best bid 99. Best ask 101. The spread is 2.",
                            "A limit buy at 99 waits with the bid. It fills only if a seller comes down.",
                            "A market buy pays 101 now. The extra 2 is the cost of crossing, before fees.",
                        ],
                        "recap": [
                            "Limit waits. Market crosses.",
                            "The spread is a real cost.",
                            "A trigger is not the same thing as a fill.",
                        ],
                        "images": ["atlas-foundations-04.png"],
                    },
                    {
                        "id": "wallets",
                        "title": "Wallets and venues",
                        "learn": "coins you can move sit with your key, and coins at a venue sit with the venue until you withdraw.",
                        "paragraphs": [
                            "A wallet is a way to hold the secret that can move coins. The common secret is a word list. Anyone who has the words can move the coins. There is no ordinary reset.",
                            "A venue account is different. The venue's books say the balance is yours, but the keys are theirs until a withdrawal completes.",
                            "Both places can fail. You can lose a word list. A venue can freeze, halt withdrawals, or be wrong about a balance.",
                            "This directory does not name a venue and does not rank them. The question is only who can move the coins today.",
                            "Next you will turn a cash limit into a position size. That habit matters before any bot or any leverage.",
                        ],
                        "example": [
                            "You have 1000 coins in total in this example.",
                            "200 sit where you hold the word list.",
                            "800 sit in a venue balance.",
                            "You can move the 200 yourself. You can move the 800 only if the venue processes a withdrawal.",
                        ],
                        "recap": [
                            "The word list is the key.",
                            "A venue balance is a claim, not the same as a key in your hand.",
                            "Split the question: who can move the coins.",
                        ],
                        "images": ["atlas-foundations-05.png"],
                    },
                    {
                        "id": "risk-basics",
                        "title": "Risk basics",
                        "learn": "you choose the cash you can lose, then divide by the distance to the stop, and that quotient is the size.",
                        "paragraphs": [
                            "Risk here means the cash you are willing to lose if the idea is wrong. It is a number you write before the entry.",
                            "The stop is the price that means the idea is wrong. The distance is the gap from entry to that price.",
                            "Size is cash at risk divided by distance. A closer stop makes a larger size. A closer stop is not automatically safer.",
                            "Fees and slippage make the loss a bit larger than the cash you named. Later tools show that extra.",
                            "You now have the floor. The next module names the shape of the path: trend, swing, and break.",
                        ],
                        "example": [
                            "Account 10000. You risk 1 percent. That is 100 of cash.",
                            "Entry 100. Stop 95. Distance 5.",
                            "Size is 100 divided by 5, which is 20 units.",
                            "Notional is 20 times 100, which is 2000. That is the position, not the loss. The planned loss is still about 100, plus fees.",
                        ],
                        "recap": [
                            "Write the cash first.",
                            "Size equals cash divided by distance.",
                            "A tight stop increases size.",
                        ],
                        "images": ["atlas-foundations-06.png"],
                    },
                ],
            },
            {
                "id": "structure",
                "title": "Trading structure",
                "blurb": "Structure is a map of swings. You name the trend, the turning points, the floors and ceilings, and the two kinds of break.",
                "lessons": [
                    {
                        "id": "trend",
                        "title": "Trend",
                        "learn": "an uptrend is higher highs and higher lows, and a downtrend is the opposite, on a clock you name.",
                        "paragraphs": [
                            "A trend is a sequence, not a feeling. On an uptrend the lows keep stepping up. On a downtrend the highs keep stepping down.",
                            "Name the clock in the same breath. A rising hour can sit inside a falling day. Both descriptions can be true.",
                            "A trend does not have to be steep. It has to keep the sequence. When the sequence breaks, you stop calling it that trend.",
                            "Grid plans later in this directory prefer back and forth movement. A strong trend fights that plan. You need this lesson before that one.",
                        ],
                        "example": [
                            "On the daily clock the swing lows print at 90, then 100, then 110.",
                            "Each low is higher. That is an uptrend on the daily clock.",
                            "The same coin can still fall for three hours inside that day. The hour clock is a different sentence.",
                        ],
                        "recap": [
                            "Trend means a sequence of swings.",
                            "Always name the clock.",
                            "A break in the sequence ends that label.",
                        ],
                        "images": ["atlas-structure-01.png"],
                    },
                    {
                        "id": "swings",
                        "title": "Swing highs and lows",
                        "learn": "a swing high is a high with lower highs on both sides, and a swing low is a low with higher lows on both sides, under a rule you keep.",
                        "paragraphs": [
                            "You need a rule for how many bars sit on each side. Two bars, or five. Write it down and do not change it mid chart.",
                            "The swing is confirmed only after the later bars exist. You cannot know the high was a swing at the moment it prints.",
                            "Swings are the posts of the map. Trend, support, and breaks all hang off these posts.",
                        ],
                        "example": [
                            "A high prints at 120.",
                            "The bar on the left has a high of 110. The bar on the right has a high of 110.",
                            "Under a one-bar rule, 120 is a swing high.",
                            "If your rule needs five bars on each side, you wait until those bars exist.",
                        ],
                        "recap": [
                            "A swing is a turn under a written rule.",
                            "It is confirmed late, not in real time.",
                            "Keep the same rule on one map.",
                        ],
                        "images": ["atlas-structure-02.png"],
                    },
                    {
                        "id": "support-resistance",
                        "title": "Support and resistance",
                        "learn": "support is a price area where declines have stalled, and resistance is a price area where rallies have stalled.",
                        "paragraphs": [
                            "These are areas, not magic lines. A single print is weaker than several reactions in the same zone.",
                            "When price leaves a ceiling and later uses it as a floor, traders rename it. The rename is a description of later behaviour, not a duty the market owes you.",
                            "For a grid, these areas are how you sketch a box. The box is still a choice. It is not a forecast of the high and the low of the year.",
                        ],
                        "example": [
                            "Three declines stall near 100. You mark support around 100.",
                            "Two rallies stall near 130. You mark resistance around 130.",
                            "A plan that needs a range might use 100 and 130 as the first sketch, then add room for ordinary wicks.",
                        ],
                        "recap": [
                            "Support and resistance are reaction areas.",
                            "Several reactions matter more than one print.",
                            "They sketch a box. They do not guarantee it.",
                        ],
                        "images": ["atlas-structure-03.png"],
                    },
                    {
                        "id": "market-structure",
                        "title": "Market structure",
                        "learn": "market structure is the ordered list of swing highs and swing lows you are using on one clock.",
                        "paragraphs": [
                            "Write the last few swings in order. In an uptrend you expect a higher high, then a higher low, then another higher high.",
                            "The map is only as good as the swing rule. If you change the rule, you draw a different map. Say which rule you used.",
                            "Structure is the bridge into the next two lessons: a break that continues the sequence, and a break that opposes it.",
                        ],
                        "example": [
                            "Swing low 110, swing high 130, swing low 120, swing high 150.",
                            "110 to 120 is a higher low. 130 to 150 is a higher high.",
                            "On this clock the structure is still an uptrend.",
                        ],
                        "recap": [
                            "Structure is a list of swings.",
                            "The swing rule is part of the sentence.",
                            "The next lessons name the two kinds of break.",
                        ],
                        "images": ["atlas-structure-04.png"],
                    },
                    {
                        "id": "break-of-structure",
                        "title": "Break of structure",
                        "learn": "a break of structure is a close through the swing that would continue the sequence you already mapped.",
                        "paragraphs": [
                            "In an uptrend, a break of structure is a close through the latest higher high. The sequence is still up. It has extended.",
                            "Decide in advance whether a wick counts or only a close. Teachers differ. Your map cannot use both without saying so.",
                            "A break is a description. It is not an order to buy or sell.",
                        ],
                        "example": [
                            "The latest higher high is 130.",
                            "A later bar closes at 134.",
                            "If your rule uses closes, that is a break of structure in the direction of the uptrend.",
                            "A wick to 134 that closes back at 129 would not count under that same rule.",
                        ],
                        "recap": [
                            "Break of structure continues the sequence.",
                            "Write wick or close before you look.",
                            "The word is a description, not an instruction.",
                        ],
                        "images": ["atlas-structure-05.png"],
                    },
                    {
                        "id": "change-of-character",
                        "title": "Change of character",
                        "learn": "a change of character is a break against the sequence, such as losing the higher low an uptrend needed.",
                        "paragraphs": [
                            "In an uptrend the higher low is the post that must hold. A close through that low is against the sequence.",
                            "People abbreviate this idea as a change of character. The plain version is enough: the old pattern failed.",
                            "This is the point where a range plan and a trend plan part ways. A grid that assumed back and forth now needs the review rule you will write later.",
                            "The next level looks at liquidity and gaps. Those are extra marks on the same swings. You can skip ahead only if this page is already clear.",
                        ],
                        "example": [
                            "The uptrend's latest higher low is 110.",
                            "A later bar closes at 106.",
                            "Under a close rule, the higher low failed. The character of that uptrend has changed.",
                            "You do not invent a new trend until a new sequence of swings exists.",
                        ],
                        "recap": [
                            "Change of character breaks against the sequence.",
                            "The failed post is the higher low or the lower high.",
                            "Wait for a new sequence before you rename the trend.",
                        ],
                        "images": ["atlas-structure-06.png"],
                    },
                ],
            },
        ],
    },
    {
        "id": "intermediate",
        "title": "Intermediate",
        "blurb": "You already know swings. Here you add marks that some traders use around those swings, and then you learn how a grid bot repeats orders inside a box.",
        "modules": [
            {
                "id": "smart-money",
                "title": "Smart money concepts",
                "blurb": "These names describe pictures on a chart. They are not receipts from a bank, and they are not instructions.",
                "lessons": [
                    {
                        "id": "liquidity",
                        "title": "Liquidity",
                        "learn": "liquidity in this lesson means the cluster of stops and resting orders that often sit beyond an obvious high or low.",
                        "paragraphs": [
                            "Equal highs and equal lows are obvious. Stops are often parked just beyond them. Resting breakout orders sit there too.",
                            "A pool is a description of that cluster. You cannot see the stops. You can see the obvious level.",
                            "A sweep is a push through the level that then returns inside. You may call it a sweep only after the return. Before the return it is only a break.",
                            "Price can run those stops and keep going. The picture does not owe you a reversal.",
                        ],
                        "example": [
                            "Two highs sit at 130.",
                            "A later wick trades 133 and the bar closes back at 128.",
                            "After the close back inside, you can call 133 a sweep of the highs.",
                            "If the bar had closed at 133, you would not use the word sweep yet.",
                        ],
                        "recap": [
                            "Obvious highs and lows attract orders.",
                            "A sweep needs a return.",
                            "The mark is a hypothesis about the chart.",
                        ],
                        "images": ["atlas-smart-money-01.png", "atlas-smart-money-02.png"],
                    },
                    {
                        "id": "order-blocks",
                        "title": "Order blocks",
                        "learn": "an order block is a candle, or a small cluster, just before a strong move, which some methods mark in case price returns.",
                        "paragraphs": [
                            "The usual mark is the last opposite candle before the impulse. Down candle, then a strong rise. Or up candle, then a strong drop.",
                            "The zone is the body, or the whole candle, under a rule you write. When price later trades back into the zone, that return is called a mitigation. What happens after the return is a separate question.",
                            "Nothing on the chart proves a large trader placed an order there. You are marking a candle, not reading a private book.",
                        ],
                        "example": [
                            "A down candle runs from 102 to 98.",
                            "The next move rises to 120 without much overlap.",
                            "The marked zone is 98 to 102.",
                            "A later visit to 100 is a return into the zone. It is not yet a result.",
                        ],
                        "recap": [
                            "The mark is a candle before a strong move.",
                            "A return is visible. The outcome is not included in the word.",
                            "It is a chart hypothesis, not a receipt.",
                        ],
                        "images": ["atlas-smart-money-03.png"],
                    },
                    {
                        "id": "fair-value-gaps",
                        "title": "Fair value gaps",
                        "learn": "a fair value gap is a three-candle pattern where the wick of the first and the wick of the third do not overlap.",
                        "paragraphs": [
                            "Candle one, a fast middle candle, candle three. If candle three's wick does not reach candle one's wick, the space between them is the gap.",
                            "Some traders expect a later visit into that space. A visit is something you can check. It is not an unfilled order you can audit.",
                            "The gap is a location. It is not a reason, by itself, to place a trade.",
                        ],
                        "example": [
                            "Candle one high is 100.",
                            "The middle candle is large.",
                            "Candle three low is 106.",
                            "The wicks do not meet. The gap is 100 to 106, which is 6 wide.",
                        ],
                        "recap": [
                            "Three candles, and the outer wicks do not overlap.",
                            "The gap is the space between those wicks.",
                            "A later visit is a check, not a promise.",
                        ],
                        "images": ["atlas-smart-money-04.png"],
                    },
                    {
                        "id": "premium-discount",
                        "title": "Premium and discount",
                        "learn": "you split a swing from its low to its high, and the top half is premium while the bottom half is discount.",
                        "paragraphs": [
                            "Pick the swing yourself. Low to high. The midpoint splits it.",
                            "Discount does not mean the coin is cheap in a fundamental sense. It means price is in the lower half of the swing you chose.",
                            "Premium does not mean you must sell. It means price is in the upper half of that same swing.",
                            "A grid box can sit entirely in one half. Knowing which half only tells you where you are inside the swing.",
                        ],
                        "example": [
                            "Swing low 100. Swing high 140. The middle is 120.",
                            "Price at 110 is discount. It is 10 below the middle.",
                            "Price at 130 is premium. It is 10 above the middle.",
                            "Change the swing and the labels move. The words belong to the swing you named.",
                        ],
                        "recap": [
                            "Premium and discount need a swing you chose.",
                            "The middle is the divider.",
                            "The words are locations, not valuations.",
                        ],
                        "images": ["atlas-smart-money-05.png"],
                    },
                    {
                        "id": "inducement",
                        "title": "Inducement",
                        "learn": "inducement is a smaller obvious high or low that sits in front of a larger one, where early orders can gather.",
                        "paragraphs": [
                            "Traders mark a minor swing that is easy to see, just before a more important swing. The idea is that early stops collect at the minor one.",
                            "Like the other marks in this module, you are guessing where orders might sit. You cannot see them.",
                            "A grid range that ignores the larger swing can be built around the small one and then fail when price reaches the larger pool.",
                            "The next module leaves these marks and builds a grid from a box, a gap, and a fee.",
                        ],
                        "example": [
                            "The main high on the clock you care about is 140.",
                            "A smaller high sits at 125, in front of it.",
                            "Early buy stops might cluster above 125.",
                            "That is a hypothesis. A close through 125 does not require a stop at 140.",
                        ],
                        "recap": [
                            "Inducement is a smaller obvious swing in front of a larger one.",
                            "It is a guess about where orders sit.",
                            "The larger swing still matters.",
                        ],
                        "images": ["atlas-smart-money-06.png"],
                    },
                ],
            },
            {
                "id": "grid-bots",
                "title": "Grid bots",
                "blurb": "A grid bot repeats buys and sells inside a box you design. These seven lessons are the path: what it is, how a cycle works, how you set it up, how you choose the box and the count, how you limit the damage, how you watch it, and the mistakes that show up first.",
                "lessons": [
                    {
                        "id": "grid-what",
                        "title": "What a grid bot is",
                        "learn": "a grid bot places buys below the price and sells above it, on rungs you chose, and it does not predict the next candle.",
                        "paragraphs": [
                            "You choose an upper price and a lower price. Between them you place levels. Levels under the current price are buys. Levels above it are sells.",
                            "The bot follows that list. It does not decide that a coin is good. It does not read the news.",
                            "If price only goes one way, the bot mostly collects coins or cash. The ladder does not invent a new plan.",
                            "Think of it as a ladder in a room. The room is the box. Outside the room, the ladder is the wrong tool until you review it.",
                        ],
                        "example": [
                            "Price is 100.",
                            "Sells are written at 102 and 104.",
                            "Buys are written at 98 and 96.",
                            "Nothing has happened yet. These are instructions, not results.",
                        ],
                        "recap": [
                            "The bot repeats a ladder.",
                            "You choose the rungs.",
                            "It does not forecast.",
                        ],
                        "images": ["atlas-grid-bots-01.png"],
                    },
                    {
                        "id": "grid-how",
                        "title": "How a grid works",
                        "learn": "one cycle is a buy that fills and a later sell at the next rung, and the gap between them is the gross step.",
                        "paragraphs": [
                            "Price falls and a buy fills. Price rises and the paired sell fills. That round trip is one cycle.",
                            "The gross step is the sell price minus the buy price, before fees, spread, and slippage.",
                            "If price never crosses the next rung, the cycle does not finish. A quiet market can sit still. A market that leaves the box does not complete the old cycles.",
                            "The bot will keep the old instructions until you change them. Automation does not notice that your reason expired.",
                        ],
                        "example": [
                            "A buy fills at 98.",
                            "A sell fills at 100.",
                            "The gross gap is 2 per coin.",
                            "A round-trip fee larger than 2 would erase the gap. The next lessons put a fee next to the gap.",
                        ],
                        "recap": [
                            "A cycle needs a fill on the way down and a fill on the way up, or the reverse pair you defined.",
                            "Gross step is the gap before costs.",
                            "No cross means no finished cycle.",
                        ],
                        "images": ["atlas-grid-bots-02.png"],
                    },
                    {
                        "id": "grid-setup",
                        "title": "Setting one up",
                        "learn": "you write the upper price, the lower price, the number of gaps, the cash, the fee you assume, and the sentence that means the plan is over.",
                        "paragraphs": [
                            "Setting up is mostly writing. The bot cannot supply the box or the reason.",
                            "Start with a spot explanation. A futures grid uses the same ladder plus margin, funding, and liquidation. Those words have their own module. Do not add them until you can explain them.",
                            "The review rule is one sentence. A daily close outside the box is an example of a sentence. I will see is not a sentence.",
                            "Keep some cash out of the grid. A reserve is what you use if you must pay fees or meet a margin need. This page does not tell you how much.",
                        ],
                        "example": [
                            "Upper 110. Lower 90.",
                            "Ten gaps across that box.",
                            "Cash set aside for the grid: 1000. More cash stays outside it.",
                            "Review rule: a daily close outside 90 to 110 sends you back to the written plan.",
                        ],
                        "recap": [
                            "Write the box, the gaps, the cash, the fee, and the review rule.",
                            "Spot first.",
                            "A review rule is a sentence you can check.",
                        ],
                        "images": ["atlas-grid-bots-03.png"],
                    },
                    {
                        "id": "grid-range",
                        "title": "Range and grid count",
                        "learn": "the width of the box and the number of gaps set the step, and the step has to clear a round-trip fee.",
                        "paragraphs": [
                            "A tight box is crossed by ordinary noise. A very wide box spreads the same cash so thin that cycles are rare.",
                            "Arithmetic gaps keep the same price distance. Geometric gaps keep the same percentage, so the price distance grows as price rises.",
                            "More gaps inside a fixed box make a smaller step. If the step is smaller than the fee and the slippage you assume, extra trades repeat a loss.",
                            "Use the grid tool on the tools page to change the fee and watch the warning. The numbers there are the same kind of example as this lesson.",
                        ],
                        "example": [
                            "Lower 90. Upper 110. The box is 20 wide.",
                            "Ten gaps. Arithmetic step is 20 divided by 10, which is 2.",
                            "A fee of 10 basis points on each side is 0.10 percent each way. At a price of 100, the round trip is about 0.20 per unit.",
                            "Step 2 is larger than 0.20 in this example. Forty gaps in a box only 10 wide, from 100 to 110, would make a step of 0.25, which is close to a 0.20 fee.",
                        ],
                        "recap": [
                            "Width and count together set the step.",
                            "Arithmetic and geometric gaps are different shapes.",
                            "A step that does not clear the fee does not get fixed by more trades.",
                        ],
                        "images": ["atlas-grid-bots-04.png", "atlas-grid-bots-05.png", "atlas-grid-bots-06.png"],
                    },
                    {
                        "id": "grid-risk",
                        "title": "Grid risk",
                        "learn": "finished cycles and unsold coins are different results, and the account can be down while the cycle total is up.",
                        "paragraphs": [
                            "Grid profit usually counts finished round trips. Coins you bought and have not sold are inventory. Inventory can fall in price.",
                            "Several grids on the same coin are one bet that the coin stays in those boxes. They are not five independent ideas.",
                            "The cash you can lose if the review rule hits is the risk that matters. Use the position-size idea from the first module: cash divided by distance.",
                            "Leverage can turn a small trip outside the box into a margin problem. That is the next level, after this one is clear.",
                        ],
                        "example": [
                            "Ten finished cycles make a gross 20 in this example.",
                            "You still hold coins bought near 94. The price is now 80.",
                            "The unsold coins are a separate loss. They can be larger than the 20.",
                            "Reporting only the 20 would hide the account.",
                        ],
                        "recap": [
                            "Cycles and inventory are different lines.",
                            "Same coin, many grids, one bet.",
                            "Write the cash you can lose if the box fails.",
                        ],
                        "images": ["atlas-grid-bots-07.png"],
                    },
                    {
                        "id": "grid-monitor",
                        "title": "Monitoring and adjusting",
                        "learn": "you check whether the written reason is still true, and you do not drag the box every hour to chase the latest price.",
                        "paragraphs": [
                            "Look at three things. Is price still inside the box, under the rule you wrote. Does the step still clear the fees you are actually paying. Did a scheduled event make the old reason obsolete.",
                            "Adjusting means returning to the sentence you wrote. Moving the box so that price is always inside it deletes the review rule.",
                            "Keep a short record. The professional journaling lesson shows one way to turn a list of results into an expectancy. You can start with one line per day.",
                        ],
                        "example": [
                            "The box top is 110. The review rule uses a daily close.",
                            "Today closes at 112.",
                            "That close starts the review. It does not, by itself, tell you the next box.",
                            "If you silently move the top to 120, you no longer have the old plan to judge.",
                        ],
                        "recap": [
                            "Check the box, the fee, and the reason.",
                            "A close outside starts the written review.",
                            "Chasing price with a new box is a new plan.",
                        ],
                        "images": ["atlas-grid-bots-08.png"],
                    },
                    {
                        "id": "grid-mistakes",
                        "title": "Common grid mistakes",
                        "learn": "the usual errors are a fee larger than the step, a box that ignores the higher clock, leverage you cannot explain, and no sentence for failure.",
                        "paragraphs": [
                            "Too many levels are the first arithmetic error. The picture looks busy. The step is smaller than the cost.",
                            "The second error is calling a trend a range because you want fills. Check the higher clock from the structure module.",
                            "The third error is adding leverage so a small account can run a large ladder. If you cannot explain liquidation, stay with the spot story.",
                            "The fourth error is silence about failure. When the box is left behind, there is no rule, so the loss continues.",
                            "Sometimes the careful result is to wait. Waiting is a decision. The next level explains leverage on its own terms, not as a way to force a grid.",
                        ],
                        "example": [
                            "Box from 100 to 110. That is 10 wide.",
                            "Forty gaps. Step is 10 divided by 40, which is 0.25.",
                            "Round-trip fee at a price near 100 is 0.20 in the earlier example.",
                            "0.25 minus 0.20 leaves 0.05 before spread and slippage. The ladder is almost all cost.",
                        ],
                        "recap": [
                            "Count the step against the fee.",
                            "Match the box to the higher clock.",
                            "No review sentence means no real plan.",
                        ],
                        "images": ["atlas-grid-bots-09.png"],
                    },
                ],
            },
        ],
    },
    {
        "id": "advanced",
        "title": "Advanced",
        "blurb": "Leverage, futures, and options change the size of a loss and add new payments. Read them after the spot and grid lessons, not instead of them.",
        "modules": [
            {
                "id": "leverage",
                "title": "Leverage trading",
                "blurb": "Margin is the cash you post. Leverage is how large the position is compared with that cash. Liquidation is the price that ends the position for you.",
                "lessons": [
                    {
                        "id": "margin",
                        "title": "Margin",
                        "learn": "margin is the cash posted to support a position that is larger than that cash.",
                        "paragraphs": [
                            "Notional is price times size. Margin is the part you post. The rest is borrowed exposure.",
                            "Isolated margin is assigned to one position. If that position is closed out, the loss is meant to stop at that assignment. Cross margin shares a pool across positions. One loss can draw on the pool.",
                            "A venue can change margin rules. This page uses a plain example, not a live schedule.",
                        ],
                        "example": [
                            "You want exposure of 10000.",
                            "At 5 times, the margin is 10000 divided by 5, which is 2000.",
                            "The position is still 10000 of exposure. The cash posted is 2000.",
                        ],
                        "recap": [
                            "Margin is posted cash.",
                            "Notional can be larger than margin.",
                            "Isolated and cross share risk differently.",
                        ],
                        "images": ["atlas-leverage-01.png"],
                    },
                    {
                        "id": "leverage-multiples",
                        "title": "Leverage",
                        "learn": "leverage is notional divided by margin, and it scales both the gain and the loss on that margin.",
                        "paragraphs": [
                            "At 5 times, a 10 percent move in price is about a 50 percent move on the margin, before fees and funding.",
                            "The multiple does not make a setup more correct. It makes the same setup larger.",
                            "If you do not know the liquidation price, you do not yet know the leverage you are using.",
                        ],
                        "example": [
                            "Margin 2000. Notional 10000. That is 5 times.",
                            "Price falls 10 percent. The position loses about 1000.",
                            "1000 is half of the 2000 margin. The price move was 10 percent. The margin move was about 50 percent.",
                        ],
                        "recap": [
                            "Leverage scales the result on the margin.",
                            "It does not improve the idea.",
                            "Know the liquidation price before you care about the multiple.",
                        ],
                        "images": ["atlas-leverage-02.png"],
                    },
                    {
                        "id": "liquidation",
                        "title": "Liquidation",
                        "learn": "liquidation is the price where losses have used up the margin down to a maintenance level, and the position is closed.",
                        "paragraphs": [
                            "Maintenance margin is the minimum the venue wants left. This directory uses a simple model so you can see the arithmetic. A real schedule can be harsher, and fees make it worse.",
                            "For a long, the example price is entry times the quantity one minus one divided by leverage, plus the maintenance rate.",
                            "For a short, the example price is entry times the quantity one plus one divided by leverage, minus the maintenance rate.",
                            "The tools page runs this model from numbers you type. It is not a venue's ladder.",
                        ],
                        "example": [
                            "Entry 100. Leverage 10. Maintenance rate 0.5 percent, which is 0.005.",
                            "Long example: 100 times (1 minus 0.1 plus 0.005) equals 90.5.",
                            "A fall from 100 to 90.5 is 9.5 percent in price. At 10 times, that is enough to exhaust most of the margin in this model.",
                            "Short example at the same inputs: 100 times (1 plus 0.1 minus 0.005) equals 109.5.",
                        ],
                        "recap": [
                            "Liquidation closes the position for you.",
                            "The example formula is a teaching model.",
                            "Maintenance and fees move the real price.",
                        ],
                        "images": ["atlas-leverage-03.png"],
                    },
                    {
                        "id": "position-size",
                        "title": "Position sizing",
                        "learn": "you still divide cash at risk by the distance to the stop, and leverage does not replace that division.",
                        "paragraphs": [
                            "The beginner rule remains. Cash you can lose, divided by distance, is the size.",
                            "Leverage changes whether the account can hold that notional. It should not be the starting point.",
                            "If the notional divided by the account is larger than the leverage cap you set, the size does not fit the cap.",
                            "The tools page includes this calculator. Change the stop and watch the size move.",
                        ],
                        "example": [
                            "Account 10000. Risk 1 percent. Cash at risk 100.",
                            "Entry 100. Stop 95. Distance 5.",
                            "Size is 20. Notional is 2000.",
                            "2000 divided by 10000 is 0.20. You do not need 10 times leverage to hold this example. Wanting 10 times would be a different, larger plan.",
                        ],
                        "recap": [
                            "Size still comes from cash and distance.",
                            "Leverage is a constraint, not the goal.",
                            "Check notional against the account.",
                        ],
                        "images": ["atlas-leverage-04.png"],
                    },
                ],
            },
            {
                "id": "futures",
                "title": "Futures",
                "blurb": "A futures contract is an agreement on a later price. Perpetuals have no end date. Dated contracts do. Funding, direction, and hedges sit on top of that difference.",
                "lessons": [
                    {
                        "id": "perpetuals",
                        "title": "Perpetuals and dated contracts",
                        "learn": "a perpetual has no expiry, and a dated contract ends on a day you can name.",
                        "paragraphs": [
                            "Both are contracts. You do not hold the coin itself. You hold a claim whose value moves with price, plus the margin rules.",
                            "A dated contract stops on its end date. After that, the position is not the same agreement.",
                            "A perpetual does not end on a calendar day. It uses funding payments to keep its price near the spot market. The next lesson is that payment.",
                        ],
                        "example": [
                            "One contract in this example has no end date.",
                            "Another ends in 30 days.",
                            "The second one needs a plan for day 30. The first one needs a plan for funding instead.",
                        ],
                        "recap": [
                            "Perpetual means no expiry date.",
                            "Dated means a real end date.",
                            "You hold a contract, not the coins, unless you separately own coins.",
                        ],
                        "images": ["atlas-futures-01.png"],
                    },
                    {
                        "id": "funding",
                        "title": "Funding rates",
                        "learn": "funding is a periodic payment between longs and shorts on a perpetual, separate from your open and your close.",
                        "paragraphs": [
                            "In this directory's simple story, a positive rate means longs pay shorts. A negative rate means shorts pay longs. Live contracts can define the sign in their own documents. Read those before you rely on a sign.",
                            "The payment is rate times notional, usually several times a day. A small rate on a large notional is not small.",
                            "A grid that finishes many small cycles can still bleed if funding runs against the inventory the grid is holding.",
                        ],
                        "example": [
                            "Rate 0.01 percent for one interval. Notional 10000.",
                            "0.01 percent of 10000 is 1.",
                            "Three intervals in a day, if the rate stayed the same, would be 3.",
                            "This is an example rate, not a live reading.",
                        ],
                        "recap": [
                            "Funding is a payment between the two sides.",
                            "It is not your trading fee, and it is extra.",
                            "Small rates matter when the notional is large.",
                        ],
                        "images": ["atlas-futures-02.png"],
                    },
                    {
                        "id": "long-short",
                        "title": "Long and short",
                        "learn": "a long gains when price rises and loses when it falls, and a short does the opposite, before fees and funding.",
                        "paragraphs": [
                            "Long means you benefit from a higher price. Short means you benefit from a lower price.",
                            "Both can be leveraged. Both can be liquidated. The direction does not remove the margin rules.",
                            "A short can lose more than a beginner expects because price has no ceiling in the simple model. Write a stop anyway.",
                        ],
                        "example": [
                            "Entry 100. One unit.",
                            "Price goes to 110. The long is plus 10. The short is minus 10. Fees are not in those two numbers.",
                            "Price goes to 90. The long is minus 10. The short is plus 10. Again before fees and funding.",
                        ],
                        "recap": [
                            "Long and short are opposite price exposures.",
                            "Costs sit on top of that opposition.",
                            "A stop still belongs on both.",
                        ],
                        "images": ["atlas-futures-03.png"],
                    },
                    {
                        "id": "hedging",
                        "title": "Hedging",
                        "learn": "a hedge is a second position that offsets part of a move in something you already hold.",
                        "paragraphs": [
                            "If a grid has left you holding coins, a short contract can offset part of a further fall. It can also offset part of a rise. You give up some of the bounce.",
                            "The hedge has its own liquidation, fees, and funding. It is not free insurance.",
                            "Match the size on purpose. Hedging everything, or hedging a random fraction, are different plans.",
                        ],
                        "example": [
                            "You hold 2 coins. Price falls by 10. The coins lose 20.",
                            "You are also short 1 coin. That short gains about 10, before costs.",
                            "The net price result is about minus 10, not minus 20. The hedge did not erase the loss.",
                        ],
                        "recap": [
                            "A hedge offsets part of a move.",
                            "It also offsets part of the opposite move.",
                            "Costs and liquidation still apply to the hedge.",
                        ],
                        "images": ["atlas-futures-04.png"],
                    },
                ],
            },
            {
                "id": "derivatives",
                "title": "Derivatives",
                "blurb": "An option is a right you pay for. Calls and puts are the two directions. Greeks are names for how the price of that right changes. Basis is the gap between a futures price and spot.",
                "lessons": [
                    {
                        "id": "options-basics",
                        "title": "Options basics",
                        "learn": "you pay a premium for the right to buy or sell at a strike, and you can lose that premium.",
                        "paragraphs": [
                            "The premium is the price of the option. It is paid up front in this simple story.",
                            "The strike is the contract price inside the right. Expiry is the last moment the right exists.",
                            "You are not required to use the right. If you do nothing, the premium can expire worthless. That limited loss is the main difference from a futures position, which can keep losing past the cash you first noticed.",
                            "American or European exercise rules change when you may use the right. This page does not pick a venue's rule.",
                        ],
                        "example": [
                            "Premium 5. Strike 100.",
                            "You pay 5 now.",
                            "If the option expires with no value, the result is minus 5, plus any fees.",
                            "You do not have to add more cash just because the coin moved, in this simple bought-option story.",
                        ],
                        "recap": [
                            "Premium is what you pay for the right.",
                            "Strike and expiry define the right.",
                            "Doing nothing can lose the premium and no more, in the basic bought case.",
                        ],
                        "images": ["atlas-derivatives-01.png"],
                    },
                    {
                        "id": "calls-puts",
                        "title": "Calls and puts",
                        "learn": "a call is the right to buy at the strike, and a put is the right to sell at the strike.",
                        "paragraphs": [
                            "A call becomes valuable when price is above the strike by more than the remaining costs. At expiry, a common example value is the greater of zero and price minus strike.",
                            "A put becomes valuable when price is below the strike. At expiry, a common example value is the greater of zero and strike minus price.",
                            "Subtract the premium you paid to see a profit. A valuable option can still be a loss if the premium was larger than that value.",
                        ],
                        "example": [
                            "Strike 100. Premium 5. These numbers are an example.",
                            "Call at expiry, price 110. Value is about 10. Profit is about 10 minus 5, which is 5.",
                            "Call at expiry, price 100 or lower. Value is about 0. Result is about minus 5.",
                            "Put at expiry, price 90. Value is about 10. Profit is about 5. Put at 100 or higher. Result is about minus 5.",
                        ],
                        "recap": [
                            "Call benefits from a higher price.",
                            "Put benefits from a lower price.",
                            "Subtract the premium before you call it a profit.",
                        ],
                        "images": ["atlas-derivatives-02.png", "atlas-derivatives-03.png"],
                    },
                    {
                        "id": "greeks",
                        "title": "Greeks in plain words",
                        "learn": "delta, gamma, theta, and vega are names for how an option price responds to the coin, to the speed of that response, to time, and to volatility.",
                        "paragraphs": [
                            "Delta is how much the option price changes when the coin changes by 1. A delta of 0.50 means about half a point, in a small move.",
                            "Gamma is how fast delta itself changes as the coin moves. Near expiry, gamma can jump. The option can feel stable and then not.",
                            "Theta is the drift from time passing, often a loss for the buyer each day if nothing else changes. Vega is the response to volatility. Higher volatility often raises an option's premium, so a buyer can gain from that and a seller can lose.",
                            "These are sensitivities, not tips. They move together. Quoting one number and ignoring the others will mislead you.",
                        ],
                        "example": [
                            "Delta 0.50. The coin rises by 1. The option price rises by about 0.50, if the other inputs stay still.",
                            "Theta 0.20 a day. A quiet day can mark the option down by about 0.20.",
                            "Vega 0.10. If volatility rises by 1 point in the model's units, the option price rises by about 0.10.",
                            "Gamma is the reason tomorrow's delta may not be 0.50.",
                        ],
                        "recap": [
                            "Delta follows the coin.",
                            "Gamma changes delta.",
                            "Theta is time. Vega is volatility.",
                        ],
                        "images": ["atlas-derivatives-04.png"],
                    },
                    {
                        "id": "basis",
                        "title": "Basis",
                        "learn": "basis is the futures price minus the spot price, a gap you can measure today.",
                        "paragraphs": [
                            "If the futures price is above spot, the basis is positive. If it is below, the basis is negative.",
                            "Into a dated expiry, that gap tends to shrink because the contract and the spot market meet. A perpetual uses funding instead of a single expiry to pull the prices together. Neither path is a schedule you can treat as a profit.",
                            "Basis is a price difference. It is not a yield until you define both legs, the costs, and the exit.",
                        ],
                        "example": [
                            "Spot 100. Futures 103.",
                            "Basis is 103 minus 100, which is 3.",
                            "As a percent of spot, 3 divided by 100 is 3 percent.",
                            "That 3 can shrink, widen, or flip sign. The number is today's gap.",
                        ],
                        "recap": [
                            "Basis is futures minus spot.",
                            "Dated contracts and perpetuals close the gap differently.",
                            "A gap is not a profit by itself.",
                        ],
                        "images": ["atlas-derivatives-05.png"],
                    },
                ],
            },
        ],
    },
    {
        "id": "professional",
        "title": "Professional",
        "blurb": "The last module is about behaviour you can repeat: a written plan, a journal, a respect for losing streaks, a way to notice urges, and a system small enough to review.",
        "modules": [
            {
                "id": "professional",
                "title": "Professional practice",
                "blurb": "None of these lessons raise the odds of a single idea. They stop you from changing the idea in the middle of the result.",
                "lessons": [
                    {
                        "id": "trade-plans",
                        "title": "Trade plans",
                        "learn": "a plan names the entry, the stop, the cash at risk, and what would make the idea wrong, before you act.",
                        "paragraphs": [
                            "Four lines are enough to start. Where you enter. Where the idea is wrong. How much cash that wrongness may cost. What you will do if price never arrives.",
                            "A target can be a fourth price, but a target without a stop is not a plan. It is a wish.",
                            "If you cannot write the stop, you are not ready to write the size. Return to position sizing.",
                        ],
                        "example": [
                            "Entry 100. Stop 95. Distance 5.",
                            "Cash at risk 100. Size 20, from the usual division.",
                            "A target at 110 is 10 away, which is 2 times the distance. That is 2 R if the stop was the risk unit.",
                            "The target is a scenario. The stop is the rule.",
                        ],
                        "recap": [
                            "Write entry, invalidation, and cash before you act.",
                            "A target is optional. A stop is not.",
                            "If you change the stop later, write a new plan.",
                        ],
                        "images": ["atlas-professional-01.png"],
                    },
                    {
                        "id": "journaling",
                        "title": "Journaling",
                        "learn": "a journal records result in R so that different sizes can be compared, and expectancy is the average R in a sample.",
                        "paragraphs": [
                            "One R is the cash you planned to lose if the stop was hit. A result divided by that cash is the R multiple.",
                            "Expectancy is the win fraction times the average win, plus the loss fraction times the average loss. Losses are negative numbers, so the second term subtracts.",
                            "A short sample is noisy. Ten rows can teach the arithmetic. They cannot prove a method. You need more rows before you trust the average.",
                            "The tools page will average a column of R values you paste. It does not know whether you followed the plan.",
                        ],
                        "example": [
                            "Ten trades. Six wins. Four losses.",
                            "Average win 1.5 R. Average loss minus 1 R.",
                            "Expectancy is 0.6 times 1.5, plus 0.4 times minus 1.",
                            "That is 0.9 minus 0.4, which is 0.5 R per trade in this sample.",
                        ],
                        "recap": [
                            "Record R, not only cash.",
                            "Expectancy is an average of a sample.",
                            "A small sample is a lesson in arithmetic, not a verdict.",
                        ],
                        "images": ["atlas-professional-02.png"],
                    },
                    {
                        "id": "risk-of-ruin",
                        "title": "Risk of ruin",
                        "learn": "the percent you risk per idea decides how deep a losing streak cuts, even before you know the win rate.",
                        "paragraphs": [
                            "Ruin here means the account is too small to follow the plan. You do not need a total loss for the plan to be dead.",
                            "Losses compound. Ten losses at 10 percent do not remove 100 percent. They leave 0.9 to the power 10, which is about 0.35, so about 65 percent of the account is gone.",
                            "Ten losses at 1 percent leave 0.99 to the power 10, which is about 0.90. The same streak hurts much less.",
                            "This is why the first module started at 1 percent as an example, not as a rule for your life. The percent is the lever.",
                        ],
                        "example": [
                            "Start with 10000.",
                            "Ten losses of 10 percent leave about 3490.",
                            "Ten losses of 1 percent leave about 9044.",
                            "The streak length is the same. The percent is the difference.",
                        ],
                        "recap": [
                            "Streaks happen.",
                            "A larger percent makes the same streak deeper.",
                            "Compounding, not addition, is the right picture.",
                        ],
                        "images": ["atlas-professional-03.png"],
                    },
                    {
                        "id": "psychology",
                        "title": "Psychology",
                        "learn": "after a loss you will want to change size, and the want is not a new plan.",
                        "paragraphs": [
                            "Two losses in a row feel like a pattern. Often they are the sample being small. The urge is to win the money back by doubling.",
                            "Write the size rule where you can see it. When the urge appears, read the rule. If you still want to change it, change it tomorrow in writing, not in the middle of the urge.",
                            "A journal helps because the feeling and the R are on different lines. You can be uncomfortable and still have followed the plan.",
                            "None of this removes fear. It gives the fear a place that is not the order button.",
                        ],
                        "example": [
                            "The plan risks 1 percent.",
                            "Two losses happen. The urge says to risk 2 percent on the next idea so the loss comes back faster.",
                            "2 percent is a different plan. It also doubles the damage of a third loss.",
                            "The directory's answer is to keep 1 percent until you edit the written rule on purpose.",
                        ],
                        "recap": [
                            "The urge after a loss is predictable.",
                            "Doubling size is a new plan.",
                            "Edit rules in writing, away from the urge.",
                        ],
                        "images": ["atlas-professional-04.png"],
                    },
                    {
                        "id": "building-a-system",
                        "title": "Building a system",
                        "learn": "a small system is one market, one setup, one risk rule, and one day a week when you review the journal.",
                        "paragraphs": [
                            "More setups feel like progress. They also make the journal impossible to read. Start with one pattern you can describe to someone else.",
                            "One market means one clock and one instrument. Adding a second market is a second system, even if the sentence looks the same.",
                            "The review day is part of the system. Without it, the journal is a diary. With it, you can ask whether the expectancy is still the one you wrote down.",
                            "When you want a word, use the glossary. When you want the arithmetic, use the tools. When you are new again on a topic, go back to Start here.",
                        ],
                        "example": [
                            "Market: the coin you already studied, on the daily clock.",
                            "Setup: a range box only when the daily structure from the structure module is not a strong one-way trend.",
                            "Risk rule: 1 percent, size from cash divided by distance.",
                            "Review: one day each week, read the R column before you add a second setup.",
                        ],
                        "recap": [
                            "One market, one setup, one risk rule, one review.",
                            "A second market is a second system.",
                            "The glossary and the tools are there when the sentence needs a word or a number.",
                        ],
                        "images": ["atlas-professional-05.png"],
                    },
                ],
            },
        ],
    },
]


def flat_lessons():
    items = []
    for level in LEVELS:
        for module in level["modules"]:
            for lesson in module["lessons"]:
                items.append((level, module, lesson))
    return items


def lesson_index():
    return {lesson["id"]: (level, module, lesson) for level, module, lesson in flat_lessons()}
