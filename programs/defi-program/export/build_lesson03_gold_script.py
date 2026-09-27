#!/usr/bin/env python3
"""Gold-standard script for Lesson 0.3, Buying your first crypto without
overpaying (about 12-15 minutes). Promotes the old ~3-minute bullet-heavy
script to the gold standard: deposit methods, the spread mechanism, market vs
limit orders (with a real demo), why you need a little ETH even if you want
stablecoins, and the lesson's own $500 worked example as a chart3d anchor.

Writes video-scripts/gold/lesson-00-3.json (the generator skips lessons with a
gold script). Every illustrative number is labelled as an example on screen and
in the narration. Spoken text (vo) spells numbers for the voice; cap is the
written caption, same sentences."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
S = []


def sc(type_, vo, cap=None, **k):
    d = {"type": type_, **k, "vo": vo}
    if cap:
        d["cap"] = cap
    S.append(d)


def img(src, eyebrow, vo, cap=None, **k):
    sc("image", vo, cap, src=src, eyebrow=eyebrow, wide=True, **k)


D = "assets/diagrams/"
EX = "Illustrative fees · check your exchange's own fee page"

# ---------------------------------------------------------------- intro
sc("title", "Lesson zero point three. Buying your first crypto without overpaying. By the end, you'll fund your account and make a first purchase at a sensible cost.",
   chapter="Why it matters", eyebrow="Lesson 0.3", num="0.3", title="Buying your first crypto without overpaying",
   sub="Same coin, same exchange. The button you press changes what you pay.")
sc("statement", "Here's why this lesson earns its place. On the same exchange, buying the exact same coin, the button you press can change your cost by ten times over. Nobody warns you about this, because both buttons say “buy.” One of them is just quietly more expensive.",
   chapter="Why it matters", kicker="Why it matters", lines=["Same coin. Same exchange.", "A ten-times difference in cost."], sub="Both buttons say \"buy.\" One is quietly far more expensive.")
sc("pillars", "Here's the plan. First, how to get money onto the exchange. Second, why the instant-buy button often costs more, and the trading screen that usually costs less. Third, what to buy first for this program. And finally, a real worked example with real numbers, your checklist and a quiz.",
   chapter="Why it matters", title="What this lesson covers",
   items=[{"icon": "bank", "title": "Depositing", "text": "Bank transfer vs. card"}, {"icon": "swap", "title": "Buying without overpaying", "text": "Instant buy vs. the trading screen"},
          {"icon": "coins", "title": "What to buy first", "text": "A little ETH, some USDC"}, {"icon": "check", "title": "Worked example", "text": "A real $500 comparison"}])

# ---------------------------------------------------------------- depositing
sc("title", "Getting money in.", chapter="Depositing", eyebrow="Depositing", num="1", title="Bank transfer or card",
   sub="One is cheaper. One is faster.")
sc("compare", "First, deposit your money. A bank transfer is usually the cheapest way in, but it can take a day or more to arrive. A card is fast, often instant, but it usually carries a much higher fee for the convenience. Neither is wrong. Pick based on whether you need the money working today, or you're happy to plan a day ahead.",
   chapter="Depositing", title="Bank transfer vs. card",
   left={"label": "Bank transfer", "tone": "good", "items": ["Usually the cheapest way in", "Can take a day or more to arrive"]},
   right={"label": "Card", "tone": "warn", "items": ["Fast, often instant", "Usually a much higher fee"]})
sc("flow", "Here's the whole sequence, deposit to first buy. You deposit, by whichever method fits your timeline. You wait for funds to clear, instantly for a card, a day or more for a bank transfer. You choose your route to buy. And only then do you actually place the order. Skipping ahead doesn't save time, the funds simply aren't there yet.",
   chapter="Depositing", title="Deposit to first buy",
   nodes=[{"label": "Deposit", "sub": "Bank transfer or card", "icon": "bank"}, {"label": "Funds clear", "sub": "Instant, or a day or more", "icon": "check"},
          {"label": "Choose your route", "sub": "Instant buy, or the trading screen", "icon": "swap"}, {"label": "Place the order", "sub": "Only once funds have cleared", "icon": "coins"}])
sc("statement", "Why does a bank transfer take a day or more, when a card is instant? It's simply going through a slower system: your bank and the exchange's bank settle it between themselves, often only on business days, sometimes queued overnight. A card authorises instantly because the card network fronts the money and settles later, behind the scenes, which is exactly what you're paying its higher fee for.",
   chapter="Depositing", kicker="Why the delay", lines=["It's not the exchange being slow.", "It's the banking network settling."], sub="A card fronts the money instantly. That convenience is what its fee is for.")

# ---------------------------------------------------------------- the spread and order types
sc("title", "Buying without overpaying.", chapter="Buying without overpaying", eyebrow="Buying without overpaying", num="2", title="Instant buy vs. the trading screen",
   sub="Same coin. Two very different price tags.")
sc("flow", "Here's exactly how an instant-buy or convert button quietly costs you more. You tap buy. The exchange quotes you a price that's already marked up above the real market price, called the spread. It adds a convenience fee on top of that. And you receive your crypto, having paid both, without ever seeing them broken out.",
   chapter="Buying without overpaying", title="How the spread works",
   nodes=[{"label": "You tap buy", "sub": "The instant, easy button", "icon": "coins"}, {"label": "Price is marked up", "sub": "The spread, above the real price", "icon": "alert", "tone": "bad"},
          {"label": "A fee is added", "sub": "On top of the spread", "icon": "bank", "tone": "bad"}, {"label": "You receive crypto", "sub": "Having paid both, unbroken out", "icon": "wallet"}])
sc("compare", "The alternative is the trading screen, sometimes called “advanced” or “spot trading.” It uses an order book, and gives you two order types. A market order buys right now, at whatever the best available price is. A limit order buys only at your chosen price or better, and it often carries a lower “maker” fee for adding to the order book instead of taking from it.",
   chapter="Buying without overpaying", title="Market order vs. limit order",
   left={"label": "Market order", "tone": "neutral", "items": ["Buys right now", "At whatever price is available"]},
   right={"label": "Limit order", "tone": "good", "items": ["Buys at your price or better", "Often a lower \"maker\" fee"]})
sc("pillars", "So when do you actually reach for each one? Use a market order when speed matters more than the price, a small, one-off purchase, or a coin trading actively enough that the price barely moves. Use a limit order whenever the price matters more than speed, which for a first purchase is nearly always. You're not in a rush, so let the lower fee, and the better price, come to you.",
   chapter="Buying without overpaying", title="When to use each",
   items=[{"icon": "swap", "title": "Market order, when...", "text": "Speed matters more than price"}, {"icon": "check", "title": "Limit order, when...", "text": "Price matters more than speed (usually)"}])
sc("steps", "Here's placing a limit order, step by step. Open the trading or advanced screen, not the instant-buy button. Select limit order, not market order. Enter the price you're willing to pay. Enter the amount you want. Submit it. And then wait, because it only fills if the market reaches your price, and it might not fill at all.",
   chapter="Buying without overpaying", title="Placing a limit order",
   steps=["Open the trading / advanced screen", "Select \"limit\", not \"market\"", "Enter your price", "Enter the amount", "Submit, then wait for a fill"],
   result="It only fills at your price or better. It might not fill at all.")
sc("quiz", "Quick check. Which order type actually controls the price you pay: market, or limit? [[pause 4]] The answer: a limit order. A market order accepts whatever price is available right now.",
   chapter="Buying without overpaying", n=1, of=4, q="Which order type controls the price you pay: market or limit?", a="A limit order. A market order accepts whatever price is available right now.")
sc("statement", "One note of balance: instant buy isn't always the wrong choice. For a genuinely tiny amount, or when you'd rather spend thirty seconds than ten minutes, the extra cost can be worth the convenience. The point of this lesson isn't “never use it.” It's knowing the trade-off exists, so you're choosing it, not stumbling into it.",
   chapter="Buying without overpaying", kicker="A note of balance", lines=["Instant buy isn't always wrong.", "Just know the trade-off you're making."], sub="For a tiny amount, the convenience can be worth the cost. Choose it, don't stumble into it.")
sc("steps", "Whichever route you take, check your confirmation before you move on. It shows the price you actually paid, the fee charged, and the amount that landed in your account. Compare that amount against what you expected. If it's meaningfully different, that gap is exactly what a spread or a fee looks like in real life.",
   chapter="Buying without overpaying", title="Check the confirmation",
   steps=["Find the price you actually paid", "Find the fee that was charged", "Find the amount that landed", "Compare it to what you expected"],
   result="A meaningful gap is what a spread or fee looks like, in real life.")

# ---------------------------------------------------------------- what to buy first
sc("title", "What to buy first.", chapter="What to buy first", eyebrow="What to buy first", num="2", title="A little ETH, some USDC",
   sub="One pays the fees. One is for practice.")
sc("pillars", "For this program, buy two things. A little E.T.H., because you need it to pay network fees, called gas, on Ethereum and most of its low-cost networks. And some U.S.D.C., a dollar stablecoin, for practice with DeFi. Neither is a prediction about price. They're the two tools this program actually uses.",
   "For this program, buy two things. A little ETH, because you need it to pay network fees, called gas, on Ethereum and most of its low-cost networks. And some USDC, a dollar stablecoin, for practice with DeFi. Neither is a prediction about price. They're the two tools this program actually uses.",
   chapter="What to buy first", title="The two things you need",
   items=[{"icon": "coins", "title": "A little ETH", "text": "Pays gas on Ethereum and its networks"}, {"icon": "swap", "title": "Some USDC", "text": "A dollar stablecoin, for DeFi practice"}])
sc("compare", "Here's why the ETH part isn't optional, even if stablecoins are all you actually want. Hold only U.S.D.C., and try your first DeFi transaction, and it fails: there's nothing to pay the network fee with. Hold a little E.T.H. alongside it, and the same transaction just goes through.",
   "Here's why the ETH part isn't optional, even if stablecoins are all you actually want. Hold only USDC, and try your first DeFi transaction, and it fails: there's nothing to pay the network fee with. Hold a little ETH alongside it, and the same transaction just goes through.",
   chapter="What to buy first", title="Only USDC vs. USDC plus a little ETH",
   left={"label": "Only USDC", "tone": "bad", "items": ["Nothing to pay the network fee with", "Your first DeFi transaction fails"]},
   right={"label": "USDC + a little ETH", "tone": "good", "items": ["Gas is covered", "The same transaction just goes through"]})
sc("statement", "How much of each? There's no fixed rule, and it depends on your overall learning budget from Lesson zero point zero. A common approach is enough E.T.H. to cover several transactions' worth of gas, often just a few dollars, with the rest in U.S.D.C. for practice. You can always buy a little more of either, later, once you see how you're actually using it.",
   "How much of each? There's no fixed rule, and it depends on your overall learning budget from Lesson 0.0. A common approach is enough ETH to cover several transactions' worth of gas, often just a few dollars, with the rest in USDC for practice. You can always buy a little more of either, later, once you see how you're actually using it.",
   chapter="What to buy first", kicker="How much of each?", lines=["No fixed rule.", "Enough ETH for gas; the rest in USDC."], sub="Buy a little more of either later, once you see how you're actually using it.")

# ---------------------------------------------------------------- worked example
sc("title", "A real worked example.", chapter="Worked example", eyebrow="Worked example", num="500", title="Buying $500 of ETH",
   sub="Two routes. Same $500. Same coin.")
img(D + "first-buy-costs.png", "What a first buy actually costs",
    "Here's the shape of it, in one picture, before we run the numbers. Every purchase has a real cost hiding in it: the spread, the fee, or both. The route you choose decides how much of that cost you actually pay.",
    chapter="Worked example")
sc("chart3d", "Here are two real routes to the same five hundred dollars of E.T.H. Card plus instant buy: a typical cost of about three point nine nine percent, around nineteen dollars and ninety five cents in fees. Bank transfer plus a limit order: a typical cost of about zero point four percent, around two dollars in fees. Same coin, same exchange, about an eighteen dollar difference. Your own exchange's fee page has the exact numbers, but the shape of this gap is real.",
   "Here are two real routes to the same $500 of ETH. Card plus instant buy: a typical cost of about 3.99%, around $19.95 in fees. Bank transfer plus a limit order: a typical cost of about 0.4%, around $2 in fees. Same coin, same exchange, about an $18 difference. Your own exchange's fee page has the exact numbers, but the shape of this gap is real.",
   chapter="Worked example", kind="bars", title="Buying $500 of ETH: two routes", sub=EX,
   bars=[{"label": "Card + instant buy", "text": "About 3.99%", "value": 19.95, "show": "$19.95", "tone": "bad"},
         {"label": "Bank + limit order", "text": "About 0.4%", "value": 2.00, "show": "$2.00", "tone": "good"}])
sc("stats", "Put another way: about four hundred eighty dollars and five cents of ETH arrives the expensive way. About four hundred ninety eight dollars arrives the cheaper way. Same five hundred dollars in. A real difference in what actually shows up.",
   "Put another way: about $480.05 of ETH arrives the expensive way. About $498 arrives the cheaper way. Same $500 in. A real difference in what actually shows up.",
   chapter="Worked example", stats=[["$480.05", "arrives via card + instant buy (example)"], ["$498.00", "arrives via bank + limit order (example)"]], lastAccent=False)
sc("statement", "And that gap isn't a one-time cost. It repeats every single time you buy the expensive way. Learn the cheaper route once, on this first small purchase, and it can pay off on every purchase after it.",
   chapter="Worked example", kicker="It repeats", lines=["Not a one-time cost.", "It repeats every time you buy."], sub="Learn the cheaper route once, on a small purchase, and use it every time after.")
sc("stats", "And the percentages hold as the amount grows. Take that same roughly three point nine nine percent versus zero point four percent gap. Apply it to an illustrative five thousand dollar purchase instead of five hundred. It's about a hundred and ninety nine dollars against about twenty dollars. Same habit. A bigger number, later.",
   "And the percentages hold as the amount grows. The same roughly 3.99% versus 0.4% gap, applied to an illustrative $5,000 purchase instead of $500, is about $199 against about $20. Same habit. A bigger number, later.",
   chapter="Worked example", stats=[["~$199", "card + instant buy, on an illustrative $5,000 (example)"], ["~$20", "bank + limit order, on the same $5,000 (example)"]], lastAccent=False)

# ---------------------------------------------------------------- records and checklist
sc("title", "Keep a record.", chapter="Checklist and quiz", eyebrow="Checklist and quiz", num="4", title="Save it as you go",
   sub="Date, amount, price, fees.")
sc("bullets", "Save a record of every purchase, from day one: the date, the amount, the price, and the fees you paid. Most countries tax crypto gains, and this simple habit is what makes that straightforward later, instead of a scramble through months of exchange history.",
   chapter="Checklist and quiz", title="What to record, every time", items=["Date", "Amount", "Price", "Fees paid"])
sc("statement", "It's not only for tax season, either. That same record is the only honest way to know what you actually paid for something, months or years later, once memory has quietly rounded the number up or down. A spreadsheet, a notes app, even a photo of the confirmation screen all work. The habit matters more than the tool.",
   chapter="Checklist and quiz", kicker="Not just for tax season", lines=["It's how you know what you paid.", "Memory rounds numbers. Records don't."], sub="A spreadsheet, a notes app, even a photo of the confirmation - the habit matters more than the tool.")
sc("bullets", "Here's this lesson's checklist. Deposited by the cheapest method available to you. Bought a small amount of E.T.H., for gas, and U.S.D.C., for practice. Tried a limit order on the trading screen. And saved a record: date, amount, price and fees.",
   "Here's this lesson's checklist. Deposited by the cheapest method available to you. Bought a small amount of ETH, for gas, and USDC, for practice. Tried a limit order on the trading screen. And saved a record: date, amount, price and fees.",
   chapter="Checklist and quiz", title="Before you move on", numbered=True,
   items=["Deposited by the cheapest method available", "Bought a little ETH (gas) and some USDC (practice)", "Tried a limit order on the trading screen", "Saved a record: date, amount, price, fees"])
sc("quiz", "Question two. Why keep a little E.T.H. even if you mostly want stablecoins? [[pause 4]] The answer: you need E.T.H. to pay network fees, gas, on Ethereum and most of its low-cost networks. Without it, a transaction simply can't go through.",
   "Question two. Why keep a little ETH even if you mostly want stablecoins? [[pause 4]] The answer: you need ETH to pay network fees, gas, on Ethereum and most of its low-cost networks. Without it, a transaction simply can't go through.",
   chapter="Checklist and quiz", n=2, of=4, q="Why keep a little ETH even if you mostly want stablecoins?", a="You need ETH to pay network fees (gas) on Ethereum and most of its low-cost networks. Without it, a transaction can't go through.")
sc("quiz", "Question three. Why keep records from day one? [[pause 4]] The answer: most countries tax crypto gains, and a simple record of dates, amounts, prices and fees makes that straightforward, instead of a scramble later.",
   chapter="Checklist and quiz", n=3, of=4, q="Why keep records from day one?", a="Most countries tax crypto gains. Records of dates, amounts, prices and fees make that straightforward.")
sc("quiz", "Question four. True or false: the instant-buy button and the trading screen always cost roughly the same. [[pause 4]] The answer: false. This lesson's own worked example showed close to a ten-times difference, on the exact same coin, on the exact same exchange.",
   chapter="Checklist and quiz", n=4, of=4, q="True or false: instant-buy and the trading screen always cost roughly the same.", a="False. The worked example showed close to a 10x difference, on the same coin, on the same exchange.")

# ---------------------------------------------------------------- recap
sc("flow", "Here's the whole lesson, recapped as one loop. You deposit, by the cheapest method that works for you. You choose the trading screen over instant buy when you can. You place a limit order. You buy a little E.T.H. and some U.S.D.C. And you save the record. Do those five things, and this lesson is done.",
   chapter="Recap and next", title="This lesson, recapped as one loop", layout="cycle",
   nodes=[{"label": "Deposit, cheapest method", "icon": "bank"}, {"label": "Trading screen over instant buy", "icon": "swap"}, {"label": "Place a limit order", "icon": "check"},
          {"label": "A little ETH, some USDC", "icon": "coins"}, {"label": "Save the record", "icon": "doc"}])
sc("statement", "This is education, not financial advice. Fees, spreads and prices change constantly. Check your own exchange's fee page for the real numbers. And nobody from this program will ever ask for your seed phrase, private keys or account access.",
   chapter="Recap and next", kicker="A reminder", lines=["Check your exchange's real fee page.", "We never ask for your keys."], sub="Not financial advice. Fees and prices change; verify them yourself.")
sc("cta", "That's buying your first crypto without overpaying. Same coin, same exchange, a smarter button. Next up, Lesson zero point four: exchange account versus your own wallet, who holds the keys.",
   "That's buying your first crypto without overpaying. Same coin, same exchange, a smarter button. Next up, Lesson 0.4: exchange account versus your own wallet, who holds the keys.",
   chapter="Recap and next", button="Next: Lesson 0.4", sub="Exchange account vs. your own wallet: who holds the keys?")

spec = {"id": "lesson-00-3", "title": "Lesson 0.3: Buying your first crypto without overpaying", "size": [1920, 1080], "group": "lessons", "maxMinutes": 25, "tag": "Lesson 0.3",
        "gold": True, "seed": 43,
        "use": "Lesson 0.3 page in the Whop course. Gold-standard script: deposit methods, the spread mechanism, market vs limit orders with a real demo, why ETH is needed for gas, and the lesson's own $500 worked example as a chart3d anchor.",
        "thumbnail": {"title": "Buying without overpaying", "subtitle": "Lesson 0.3"}, "scenes": S}
out = ROOT / "video-scripts" / "gold" / "lesson-00-3.json"
out.write_text(json.dumps(spec, indent=1, ensure_ascii=False))
words = sum(len(s["vo"].replace("[[pause 4]]", "").split()) for s in S)
print(f"{len(S)} scenes, {words} words, est {(words / 171 * 60 + len(S) * 1.3 + 4 * 3) / 60:.1f} min")
