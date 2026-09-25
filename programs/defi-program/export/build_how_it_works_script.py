#!/usr/bin/env python3
"""Script for the long-form "How the program works" video (about 24 minutes).
Writes video-scripts/core/how-the-program-works.json. Spoken text (vo) spells numbers
and abbreviations for the voice; cap is the written caption with the same sentences."""
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


# ---------------------------------------------------------------- intro
sc("logo", "Welcome to the On-Chain Operator Program. This is the long version of how the program works. Over the next twenty-odd minutes, I'll take you inside all of it: why it exists, how it's built, every module in order, the tools you'll use, and how to get the most out of it. Get comfortable. This is the map for everything that follows.",
   "Welcome to the On-Chain Operator Program. This is the long version of how the program works. Over the next twenty-odd minutes, I'll take you inside all of it: why it exists, how it's built, every module in order, the tools you'll use, and how to get the most out of it. Get comfortable. This is the map for everything that follows.",
   chapter="Welcome", tagline="How the program works")
sc("pillars", "Here's the plan. First, why this program exists, and the mindset it teaches. Second, how it's built: stages, modules, lessons and starters. Third, a walk through all fifteen modules, with the pictures you'll see inside them. And fourth, your tools, your capstones, and how to succeed.",
   "Here's the plan. First, why this program exists, and the mindset it teaches. Second, how it's built: stages, modules, lessons and starters. Third, a walk through all 15 modules, with the pictures you'll see inside them. And fourth, your tools, your capstones, and how to succeed.",
   chapter="Welcome", title="What this video covers",
   items=[{"icon": "compass", "title": "Why", "text": "The problem and the mindset"}, {"icon": "layers", "title": "How it's built", "text": "Stages, modules, lessons, starters"},
          {"icon": "book", "title": "All 15 modules", "text": "With the pictures inside them"}, {"icon": "target", "title": "Tools & success", "text": "Calculators, capstones, habits"}])

# ---------------------------------------------------------------- why
sc("bullets", "Let's start with why this program exists. Most people get hurt in DeFi in the same four ways. Setup mistakes that can't be undone, like the wrong network, a leaked seed phrase, or one bad approval. Yields nobody can explain, until the subsidy stops. Borrowing with no buffer, so one sharp move liquidates the position. And no plan for the way out.",
   chapter="Why it exists", title="How people get hurt in DeFi", check=False,
   items=["Setup mistakes that can’t be undone", "Yields nobody can explain", "Borrowing with no buffer", "No plan for the way out"])
sc("statement", "And on-chain, there's no help desk. No chargebacks. No margin calls. No one to phone. The only protection you have is the process you follow before you act. That process is what this program teaches.",
   chapter="Why it exists", kicker="On-chain", lines=["There's no help desk."], sub="The only protection is the process you follow before you act.")
img("assets/diagrams/ledgers-vs-blockchain.png", "Why mistakes are final",
    "Here's why. A bank keeps a private ledger, and it can correct or reverse an entry. A blockchain is a shared ledger that thousands of computers keep identical copies of. That's what makes it trustworthy, and it's also why a mistake is final. You'll meet this idea in the very first lesson, because everything else builds on it.")

# ---------------------------------------------------------------- mindset
sc("strike", "Most people enter DeFi through a number. Twelve percent A.P.Y. Operators start with a different question. What am I being paid to risk?",
   "Most people enter DeFi through a number. 12% APY. Operators start with a different question. What am I being paid to risk?",
   chapter="The operator mindset", big="12% APY", after="What am I being paid to risk?")
sc("pillars", "The operator mindset comes down to three questions, asked before every position. What am I being paid to risk? How do I get out, and how fast? And how big should this be, so that if I'm wrong, it doesn't matter much? Every lesson in this program trains one of those three questions.",
   chapter="The operator mindset", title="Three questions before every position",
   items=[{"icon": "search", "title": "What's the risk?", "text": "What am I being paid to take on?"}, {"icon": "exit", "title": "What's the exit?", "text": "How do I get out, and how fast?"},
          {"icon": "target", "title": "How big?", "text": "Sized so being wrong doesn't matter much"}])
img("assets/diagrams/profit-sources.png", "Where returns come from",
    "Here's the first answer you'll learn. Every DeFi return comes from one of five places. Service fees, like swap fees paid to liquidity providers. Interest, paid by borrowers. Security rewards, for staking. Structural carry, like funding and basis. And incentives, which are only real once you've sold them. Price going up is not a strategy. If you can't name which of these five is paying you, you don't understand the position yet.")
img("assets/diagrams/defi-stack.png", "Every yield pays for a risk",
    "And here's the second. Every position sits on a stack. The chain that settles it. The wallet that signs it. The app that runs it. And the position itself. Each layer can fail, and every yield is a payment for taking on some of that risk. Your job is to name that risk before you deposit.")

# ---------------------------------------------------------------- structure
img("assets/diagrams/path-to-mastery.png", "Six stages, in order",
    "Now, how the program is built. It runs in six stages. Zero, you get set up safely. Foundations, you protect a wallet and learn to trade and provide liquidity. Practitioner, you borrow, earn yield and map infrastructure risk. Analyst, you research any protocol and read on-chain data. Strategist, thirty strategies, hedging and stress tests. And Operator, you run your own on-chain bank.",
    chapter="How it's built")
sc("stats", "In numbers: fifteen modules, a hundred and seven lessons, plus a Mastery Starter at the top of every module, and thirty strategy playbooks.",
   "In numbers: 15 modules, 107 lessons, plus a Mastery Starter at the top of every module, and 30 strategy playbooks.",
   chapter="How it's built", stats=[["15", "modules"], ["107", "lessons + 15 starters"], ["30", "strategy playbooks"]], lastAccent=False)
sc("statement", "The stages unlock in order. You move on by passing the previous stage's quizzes, not by the calendar. That's deliberate. It means nobody reaches leverage before they've mastered safety. Go at your own pace. There's no deadline, and you keep lifetime access.",
   chapter="How it's built", kicker="The drip rule", lines=["Each stage unlocks", "when you pass the last."], sub="Nobody reaches leverage before safety. No deadlines; lifetime access.")
sc("steps", "Every lesson has the same five parts, so you always know where you are. It starts with an objective: what you'll be able to do. Then an explanation, in plain words, with every term defined the first time it appears. Then a worked example, with every number calculated on screen. Then a checklist, which you do for real, with a small test amount. And finally, a three-question quiz.",
   chapter="How it's built", title="The anatomy of every lesson",
   steps=["Objective: what you'll be able to do", "Explanation: plain words, every term defined", "Worked example: every number calculated", "Checklist: done for real, small amounts", "Quiz: three questions before you move on"])
sc("bullets", "And every module opens with a Mastery Starter, so you can start any topic from zero. It has a sixty-second version of the whole module. The words you'll need. What to have in place before you start. One safe first step you can take today. A ladder from beginner, to practitioner, to master. And a clear test for when you've mastered the module.",
   "And every module opens with a Mastery Starter, so you can start any topic from zero. It has a 60-second version of the whole module. The words you'll need. What to have in place before you start. One safe first step you can take today. A ladder from beginner, to practitioner, to master. And a clear test for when you've mastered the module.",
   chapter="How it's built", title="Inside every Mastery Starter", numbered=True,
   items=["The 60-second version", "Words you’ll need", "Before you start", "Your first safe step", "The mastery ladder", "You’ve mastered it when…"])
sc("statement", "Most modules also have expert lessons, fifteen in all. They show how the machinery really works underneath: how automated market makers are designed, how lending protocols handle bad debt, how to read contract code, how to value a protocol. You don't need them to operate safely. They're there when you want to go deeper.",
   "Most modules also have expert lessons, 15 in all. They show how the machinery really works underneath: how automated market makers are designed, how lending protocols handle bad debt, how to read contract code, how to value a protocol. You don't need them to operate safely. They're there when you want to go deeper.",
   chapter="How it's built", kicker="Going deeper", lines=["15 expert lessons"], sub="How the machinery really works: AMM design, bad debt, contract code, protocol valuation.")

# ---------------------------------------------------------------- modules
MODS = [
 (0, "Crypto From Zero", [
   ("assets/diagrams/setup-roadmap.png", "Module zero assumes you've never owned crypto. Its seven steps take you from nothing to set up: secure your accounts, open and lock down an exchange, make a first small purchase, set up and back up a wallet, send a first transfer on the right network, practise on a test network, and finish with a security baseline. It all comes with a printable Day-One Setup Kit.",
    "Module 0 assumes you've never owned crypto. Its seven steps take you from nothing to set up: secure your accounts, open and lock down an exchange, make a first small purchase, set up and back up a wallet, send a first transfer on the right network, practise on a test network, and finish with a security baseline. It all comes with a printable Day-1 Setup Kit."),
   ("assets/diagrams/first-buy-costs.png", "Here's a Module zero example. The price on the chart isn't what you pay. You lose a little to the spread, a little to the trading fee, and a little more to the network when you withdraw. So you'll compare offers by what actually lands in your wallet.", "Here's a Module 0 example. The price on the chart isn't what you pay. You lose a little to the spread, a little to the trading fee, and a little more to the network when you withdraw. So you'll compare offers by what actually lands in your wallet."),
   ("assets/diagrams/custody-split.png", "One of the first ideas you'll meet is who holds the keys. On an exchange, the exchange holds them, which is fine for buying and cashing out. In your own wallet, you hold them, which is what you need for DeFi, and it means your backup is your responsibility. You'll test that backup by restoring it, before you ever rely on it.", None)]),
 (1, "Foundations & Safety", [
   ("assets/diagrams/tx-lifecycle.png", "Module one is foundations and safety. You'll learn what really happens when you press send: you sign, the transaction waits publicly in the mempool, a validator puts it in a block, and then it's final. You'll learn why gas is paid even when a transaction fails.", "Module 1 is foundations and safety. You'll learn what really happens when you press send: you sign, the transaction waits publicly in the mempool, a validator puts it in a block, and then it's final. You'll learn why gas is paid even when a transaction fails."),
   ("assets/diagrams/scam-patterns.png", "Then the attacks. Fake sites that look exactly like the real one. Drainers, where a single signature hands over everything. Fake support staff who ask for your seed phrase. And poisoned addresses planted in your history. You'll learn to recognise all four, and to simulate a transaction before you sign it, so you know exactly what it does.", None),
   ("assets/diagrams/approval-anatomy.png", "And you'll read every approval before you sign it: which token, which contract can spend it, and how much. An infinite approval stays open after the trade. An exact one covers only this trade. You'll default to exact, and revoke what you don't use.", None),
   ("assets/diagrams/stablecoin-designs.png", "You'll also learn how stablecoins are built, and how each design breaks. Fiat-backed coins depend on an issuer's reserves. Crypto-backed coins depend on collateral and liquidations. And algorithmic designs depend on confidence, which can vanish in days.", None)]),
 (2, "Trading On-Chain", [
   ("assets/charts/amm-curve.png", "Module two is trading on-chain. It starts with the maths behind every automated market maker. In this example, a pool holds a hundred E.T.H. and three hundred thousand dollars. Swapping in ten E.T.H. returns about twenty-seven thousand, two hundred and seventy-three dollars, not thirty thousand. That's price impact, and you'll learn to calculate it before you trade.",
    "Module 2 is trading on-chain. It starts with the maths behind every automated market maker. In this example, a pool holds 100 ETH and $300,000. Swapping in 10 ETH returns about $27,273, not $30,000. That's price impact, and you'll learn to calculate it before you trade."),
   ("assets/diagrams/lp-position.png", "Then providing liquidity. You deposit two assets, earn a share of every swap's fees, and your mix of assets shifts as prices move. Your real result is the fees you earned, minus the impermanent loss, compared with simply holding. You'll learn to measure that honestly, and when it's worth doing at all.", None),
   ("assets/charts/impermanent-loss.png", "Here's impermanent loss as a chart. If the price doubles, or halves, a fifty-fifty pool leaves you about five point seven percent behind simply holding. If it triples, thirteen point four percent. Your fees have to beat this line, or holding would have been better.", "Here's impermanent loss as a chart. If the price doubles, or halves, a 50/50 pool leaves you about 5.7% behind simply holding. If it triples, 13.4%. Your fees have to beat this line, or holding would have been better."),
   ("assets/diagrams/order-types.png", "And execution. Market orders, limit orders, orders split over time, and intent-based orders where solvers compete to fill you. Each one is safer in different situations, and you'll learn which to use when.", None)]),
 (3, "Lending & Leverage", [
   ("assets/diagrams/lending-pool-flow.png", "Module three is lending and leverage. You'll see how a lending pool works: suppliers deposit, borrowers post collateral and pay interest, and the rate rises with how much of the pool is borrowed. Near full utilisation, rates jump, and lenders may not be able to withdraw.", "Module 3 is lending and leverage. You'll see how a lending pool works: suppliers deposit, borrowers post collateral and pay interest, and the rate rises with how much of the pool is borrowed. Near full utilisation, rates jump, and lenders may not be able to withdraw."),
   ("assets/charts/health-factor.png", "The centre of this module is the health factor. Ten E.T.H. at three thousand dollars, with twelve thousand borrowed, gives a health factor of two, and liquidation at fifteen hundred dollars. Borrow sixteen thousand instead, and liquidation moves up to two thousand. You'll draw this line before every borrow, for the rest of your life.",
    "The centre of this module is the health factor. 10 ETH at $3,000, with $12,000 borrowed, gives a health factor of 2, and liquidation at $1,500. Borrow $16,000 instead, and liquidation moves up to $2,000. You'll draw this line before every borrow, for the rest of your life."),
   ("assets/diagrams/perp-anatomy.png", "You'll also learn perpetual futures: longs and shorts with no expiry, funding payments that keep them near the spot price, and liquidation. At twenty times leverage, a move of under five percent can wipe out the margin. That's why you'll use perps to hedge and to earn carry, not to gamble.", "You'll also learn perpetual futures: longs and shorts with no expiry, funding payments that keep them near the spot price, and liquidation. At 20× leverage, a move of under 5% can wipe out the margin. That's why you'll use perps to hedge and to earn carry, not to gamble."),
   ("assets/diagrams/liquidation-cascade.png", "And you'll learn why falls accelerate. Liquidations sell collateral into a falling market, which pushes prices lower, which triggers more liquidations. Your buffer is your time to react, and you'll write your defence plan before you borrow, not during the crash.", None)]),
 (4, "Yield", [
   ("assets/diagrams/base-vs-emissions.png", "Module four is yield. The core skill is splitting any A.P.Y. into what's organic and what's subsidised. Here, Pool A shows twenty percent, but sixteen of it is emissions. Pool B shows nine, and eight of it is real fees. You'll learn which part lasts, and which part disappears when the incentives stop.",
    "Module 4 is yield. The core skill is splitting any APY into what's organic and what's subsidised. Here, Pool A shows 20%, but 16 of it is emissions. Pool B shows 9, and 8 of it is real fees. You'll learn which part lasts, and which part disappears when the incentives stop."),
   ("assets/diagrams/lst-accrual.png", "Then staking. Native staking, liquid staking tokens that accrue rewards but can trade below the E.T.H. behind them, and restaking, which adds yield and adds new ways to be slashed.", "Then staking. Native staking, liquid staking tokens that accrue rewards but can trade below the ETH behind them, and restaking, which adds yield and adds new ways to be slashed."),
   ("assets/diagrams/rwa-trust.png", "And real-world assets. When you buy a tokenized treasury, you own a claim on an issuer, who promises redemption, through a custodian who holds the real asset. You'll learn to see every link in that chain before you trust it.", None)]),
 (5, "Infrastructure Risk", [
   ("assets/diagrams/bridge-trust.png", "Module five is infrastructure risk: everything a position depends on that isn't the position itself. Bridges first. Some depend on a small set of signers, some on the chains' own consensus, and some on at least one honest watcher. You'll size your exposure to the trust model.", "Module 5 is infrastructure risk: everything a position depends on that isn't the position itself. Bridges first. Some depend on a small set of signers, some on the chains' own consensus, and some on at least one honest watcher. You'll size your exposure to the trust model."),
   ("assets/diagrams/oracle-twap.png", "Then oracles, the price feeds that decide when positions get liquidated. A single spot price can be pushed around in a thin pool. A time-weighted average is harder to manipulate, but lags fast moves. You'll always ask which price secures your position.", None),
   ("assets/diagrams/proxy-admin-keys.png", "And the code itself. Many contracts can be upgraded after you deposit, by whoever holds the admin key. You'll learn to check the timelock and the admin before you put money in, and to read verified code well enough to check a claim.", None)]),
 (6, "Protocol Research", [
   ("assets/diagrams/research-loop.png", "Module six is protocol research. You'll learn a six-step loop you can run on anything. Mechanism: how it works. Cash flow: where the money comes from. Dependencies. Solvency. Evidence. And exit. You'll finish with a full due-diligence file on a real protocol.", "Module 6 is protocol research. You'll learn a six-step loop you can run on anything. Mechanism: how it works. Cash flow: where the money comes from. Dependencies. Solvency. Evidence. And exit. You'll finish with a full due-diligence file on a real protocol."),
   ("assets/diagrams/token-supply-unlocks.png", "You'll learn tokenomics: the difference between the supply trading today and the fully diluted value, how large unlocks add supply, and whether the protocol's success ever reaches the token at all.", None),
   ("assets/diagrams/failure-patterns.png", "And you'll study how DeFi failures happened, through real case studies. They rhyme. Manipulated oracles. Bad upgrades. Bank runs. And incentive programmes that end, taking the liquidity with them. Learn the patterns, and you'll spot them early.", None)]),
 (7, "On-Chain Analytics", [
   ("assets/diagrams/onchain-misreads.png", "Module seven is on-chain analytics, and it starts with humility. Volume can be faked. Addresses aren't people. And total value locked counts capital that's only there for the rewards. Every metric gets its caveat.", "Module 7 is on-chain analytics, and it starts with humility. Volume can be faked. Addresses aren't people. And total value locked counts capital that's only there for the rewards. Every metric gets its caveat."),
   ("assets/diagrams/explorer-anatomy.png", "You'll master the block explorer: the transaction hash, who signed and which contract was called, the event logs, and the internal calls that show what really happened. You won't need an app's interface to know what a transaction did.", None),
   ("assets/diagrams/pool-depth.png", "And you'll read markets. Here, a trade that's one percent of a pool's reserve moves the price about one percent. At ten percent, it moves it over nine. You'll check whether a pool can take your trade before you place it, and query the chain yourself when a dashboard isn't enough.",
    "And you'll read markets. Here, a trade that's 1% of a pool's reserve moves the price about 1%. At 10%, it moves it over 9. You'll check whether a pool can take your trade before you place it, and query the chain yourself when a dashboard isn't enough.")]),
 (8, "The DeFi Operating System", [
   ("assets/diagrams/risk-buckets.png", "Module eight turns knowledge into a system. You'll build a portfolio in buckets: a core of simple, well-tested positions, a satellite of strategies you've tested, and a small, capped speculative bucket. Each bucket, and each position inside it, has a written cap.", "Module 8 turns knowledge into a system. You'll build a portfolio in buckets: a core of simple, well-tested positions, a satellite of strategies you've tested, and a small, capped speculative bucket. Each bucket, and each position inside it, has a written cap."),
   ("assets/diagrams/risk-register.png", "You'll keep a risk register: every position, its risks, a score, and a written response. Then an operating playbook with the same four phases every time: deploy, monitor, respond, and review.", None),
   ("assets/charts/var-drawdown.png", "And you'll size positions from numbers, not feelings. This chart shows one-day value at risk for a hundred-thousand-dollar position. At seventy percent volatility, a bad day at the ninety-five percent level is about six thousand dollars. And because crypto has fatter tails than this model assumes, you'll treat it as a floor, not a ceiling.",
    "And you'll size positions from numbers, not feelings. This chart shows one-day value at risk for a $100,000 position. At 70% volatility, a bad day at the 95% level is about $6,040. And because crypto has fatter tails than this model assumes, you'll treat it as a floor, not a ceiling.")]),
 ("8.3", "The strategy library", [
   ("assets/diagrams/strategy-levels.png", "Inside Module eight is the strategy library: thirty strategies in seven levels. Core, like stablecoin lending and staking. Liquidity. Yield. Advanced, like leveraged loops and funding carry. Treasury and research. Professional, like fixed rates, basis and options. And Expert. Every strategy shows where its return comes from, the maths, the steps, the kill rules, and exactly how it loses money.", "Inside Module 8 is the strategy library: 30 strategies in 7 levels. Core, like stablecoin lending and staking. Liquidity. Yield. Advanced, like leveraged loops and funding carry. Treasury and research. Professional, like fixed rates, basis and options. And Expert. Every strategy shows where its return comes from, the maths, the steps, the kill rules, and exactly how it loses money."),
   ("assets/charts/loop-spread.png", "Here's an example from the library. A three-times loop on three and a half percent collateral yield. At a two and a half percent borrow rate, you net five and a half percent. Above three and a half percent borrow, leverage adds nothing. And at five and a quarter, the return is wiped out. The spread is everything, and you'll know the break-even before you start.",
    "Here's an example from the library. A 3× loop on 3.5% collateral yield. At a 2.5% borrow rate, you net 5.5%. Above 3.5% borrow, leverage adds nothing. And at 5.25%, the return is wiped out. The spread is everything, and you'll know the break-even before you start.")]),
 (9, "DeFi vs Grid Bots", [
   ("assets/diagrams/grid-vs-lp.png", "Module nine connects DeFi to grid bots. A concentrated liquidity position and a grid bot do almost the same job: both sell as the price rises and buy as it falls, inside a range. The difference is the risks: fees, custody, and what happens when the price leaves the range.", "Module 9 connects DeFi to grid bots. A concentrated liquidity position and a grid bot do almost the same job: both sell as the price rises and buy as it falls, inside a range. The difference is the risks: fees, custody, and what happens when the price leaves the range."),
   ("assets/diagrams/when-each-wins.png", "You'll learn when each one wins. In a range, both can work. In a strong trend, neither does well. And you'll build one system with two sleeves, an exchange grid sleeve and an on-chain sleeve, under a single risk cap.", None)]),
 (10, "Advanced Yield Engineering", [
   ("assets/charts/pt-convergence.png", "Module ten is advanced yield engineering. Fixed-rate yield first. A principal token bought at a discount converges to its full value at maturity, which locks in a fixed rate if you hold it to the end. You'll learn exactly what that fixed rate is short.", "Module 10 is advanced yield engineering. Fixed-rate yield first. A principal token bought at a discount converges to its full value at maturity, which locks in a fixed rate if you hold it to the end. You'll learn exactly what that fixed rate is short."),
   ("assets/diagrams/cash-and-carry.png", "Then basis and carry. Buy spot, short a dated future, and capture the gap between them, without a view on price. It works only if both legs are held to expiry and your margin is never called. You'll also learn funding carry, options income, and when you're really being paid to be the house.", None),
   ("assets/diagrams/covered-call-put.png", "And options income. A covered call earns a premium but caps your upside. A cash-secured put earns a premium, and may buy the asset for you after a fall. Every one of these strategies is taught with how it loses.", None)]),
 (11, "Hedging & Risk Engineering", [
   ("assets/diagrams/hedge-perp-option.png", "Module eleven is hedging and risk engineering. You'll hedge the risks you don't want, with a perpetual short, which costs funding, or a put option, which costs a premium upfront. You'll learn what on-chain cover actually pays, and what it excludes.", "Module 11 is hedging and risk engineering. You'll hedge the risks you don't want, with a perpetual short, which costs funding, or a put option, which costs a premium upfront. You'll learn what on-chain cover actually pays, and what it excludes."),
   ("assets/diagrams/liq-buffer-alerts.png", "You'll protect every borrow with three layers. A buffer, keeping the health factor well above one. Alerts that warn you long before trouble. And a repayment amount worked out in advance, with the funds ready.", None),
   ("assets/diagrams/stress-grid.png", "Then you'll stress-test the whole book. A thirty percent price fall. A stablecoin depeg. A protocol exploit. For each one, what breaks, and how you fix it now, before the market does it for you.", "Then you'll stress-test the whole book. A 30% price fall. A stablecoin depeg. A protocol exploit. For each one, what breaks, and how you fix it now, before the market does it for you."),
   ("assets/diagrams/incident-60min.png", "And you'll have an incident plan for the first sixty minutes of an exploit, a depeg, or a compromised wallet. Stop and sign nothing new. Size the exposure. Move keys and funds to safety. Then act on public facts only, and record everything.", "And you'll have an incident plan for the first 60 minutes of an exploit, a depeg, or a compromised wallet. Stop and sign nothing new. Size the exposure. Move keys and funds to safety. Then act on public facts only, and record everything.")]),
 (12, "Operate as Your Own Bank", [
   ("assets/diagrams/own-bank.png", "Module twelve is where you operate as your own bank. It's a method, not a licence. Four pillars: custody, a credit line, a lending desk and a treasury, standing on a base of books, records and succession, under one income policy.", "Module 12 is where you operate as your own bank. It's a method, not a licence. Four pillars: custody, a credit line, a lending desk and a treasury, standing on a base of books, records and succession, under one income policy."),
   ("assets/diagrams/personal-balance-sheet.png", "You'll build a real balance sheet. Assets at market value. Liabilities, like loans and accrued interest. And the numbers that matter: equity, loan-to-value, and how many months of runway your liquid assets cover.", None),
   ("assets/diagrams/custody-architecture.png", "You'll design custody in three tiers. A vault that needs more than one key. An operating wallet with limits. And a small hot float for anything new. No single lost phone, stolen key or bad signature can drain the bank.", None),
   ("assets/diagrams/liquidity-ladder.png", "And a liquidity ladder. Using an example of five thousand dollars a month of spending, one month sits instantly available, five more in blue-chip lending you can reach the same day, and the next six to twelve months in positions that mature when you'll need them. Everything else can grow. Add a written plan so your family could recover everything if you couldn't, and you're running a bank.", "And a liquidity ladder. Using an example of $5,000 a month of spending, one month sits instantly available, five more in blue-chip lending you can reach the same day, and the next 6 to 12 months in positions that mature when you'll need them. Everything else can grow. Add a written plan so your family could recover everything if you couldn't, and you're running a bank.")]),
 (13, "The Income Engine", [
   ("assets/diagrams/durability-rank.png", "Module thirteen is the income engine. You'll rank income by durability, not by headline yield. Staking rewards and lending interest at the durable end. Emissions and points at the fragile end.", "Module 13 is the income engine. You'll rank income by durability, not by headline yield. Staking rewards and lending interest at the durable end. Emissions and points at the fragile end."),
   ("assets/charts/expected-yield.png", "You'll subtract expected losses from every yield. An eighteen percent farm, with a ten percent yearly chance of losing sixty percent, has an expected yield of twelve. The forty percent farm barely beats it, with far more risk.", "You'll subtract expected losses from every yield. An 18% farm, with a 10% yearly chance of losing 60%, has an expected yield of 12. The 40% farm barely beats it, with far more risk."),
   ("assets/charts/income-waterfall.png", "And you'll set a payout policy. Start from the headline. Subtract expected losses. Keep part as a buffer. Only then decide what you may take out, and never from principal. This is an illustration, not a promise. No income is guaranteed, and the whole point is to live within what's real.", None)]),
 (14, "Automation & Mastery", [
   ("assets/diagrams/alert-stack.png", "Module fourteen is automation and mastery. You'll set up monitoring, so you hear about a problem before it costs money: positions, watchers that read the chain, and alerts that reach your phone.", "Module 14 is automation and mastery. You'll set up monitoring, so you hear about a problem before it costs money: positions, watchers that read the chain, and alerts that reach your phone."),
   ("assets/diagrams/least-permission-bot.png", "You'll automate with the least permission possible. A keeper that does one job, inside a box of limited functions and spending caps, that you can revoke at any time. And never, ever, a handed-over seed phrase.", None),
   ("assets/diagrams/capstone-pack.png", "And you'll finish with the operator capstone: your balance sheet, your policies, your monitors, and a stress test with every failure fixed. A document clear enough that a stranger could run your bank from it.", None)]),
]
import re
WHERE = {}
for f in sorted((ROOT / "lessons").glob("module-*.md")):
    for lid, body in re.findall(r"^## Lesson (\d+\.\d+) — .*?$(.*?)(?=^## Lesson |\Z)", f.read_text(), flags=re.M | re.S):
        for pth in re.findall(r"\(\.\./(assets/[^)]+)\)", body):
            WHERE.setdefault(pth, lid)
WHERE.setdefault("assets/charts/amm-curve.png", "2.2")
EXTRA = {"assets/diagrams/setup-roadmap.png": "The Day-1 Setup Kit", "assets/diagrams/own-bank.png": "Stage 5 · Operator"}
WHERE.setdefault("assets/diagrams/strategy-levels.png", "8.3")
WHERE.setdefault("assets/charts/loop-spread.png", "3.4")
for n, title, items in MODS:
    label = "The strategy library" if n == "8.3" else f"Module {n} · {title}"
    if n != "8.3":
        img(f"assets/modules/module-{n:02d}.png", f"Module {n}", None or f"Module {['zero','one','two','three','four','five','six','seven','eight','nine','ten','eleven','twelve','thirteen','fourteen'][n]}. {title.replace('&', 'and')}.",
            f"Module {n}. {title}.", chapter=label)
    for i, (src, vo, cap) in enumerate(items):
        eyebrow = f"From Lesson {WHERE[src]}" if src in WHERE else EXTRA.get(src, "Example")
        img(src, eyebrow, vo, cap, **({"chapter": label} if n == "8.3" and i == 0 else {}))

# ---------------------------------------------------------------- tools
sc("steps", "Now your tools. The program comes with calculators, so every number you act on is computed. Here's the health factor calculator on the example from Module three. Ten E.T.H. at three thousand dollars, a liquidation threshold of point eight, and twelve thousand dollars of debt. It returns a loan-to-value of forty percent, a health factor of two, and a liquidation price of fifteen hundred dollars. There are twenty calculators, from impermanent loss to income and value at risk.",
   "Now your tools. The program comes with calculators, so every number you act on is computed. Here's the health factor calculator on the example from Module 3. 10 ETH at $3,000, a liquidation threshold of 0.8, and $12,000 of debt. It returns a loan-to-value of 40%, a health factor of 2, and a liquidation price of $1,500. There are 20 calculators, from impermanent loss to income and value at risk.",
   chapter="Your tools", title="Example: the health factor calculator",
   steps=["Inputs: 10 ETH · $3,000 · LT 0.80 · debt $12,000", "LTV = 40%", "Health factor = 2.00", "Liquidation price = $1,500 (−50%)"], result="20 calculators in all")
sc("pillars", "You'll also have seventeen worksheets, for due diligence, pre-launch checks and your bank policies. The Course Hub, which puts every lesson, video, checklist and calculator in one place, with search and progress tracking. And a Day-One Setup Kit you can print.",
   "You'll also have 17 worksheets, for due diligence, pre-launch checks and your bank policies. The Course Hub, which puts every lesson, video, checklist and calculator in one place, with search and progress tracking. And a Day-1 Setup Kit you can print.",
   chapter="Your tools", title="Worksheets, hub and kit",
   items=[{"icon": "book", "title": "17 worksheets", "text": "Due diligence, pre-launch, bank policies"}, {"icon": "compass", "title": "Course Hub", "text": "Lessons, videos, checklists, calculators, progress"},
          {"icon": "check", "title": "Day-1 Setup Kit", "text": "A printable checklist for Module 0"}])
sc("compare", "There are two capstones. The analyst capstone, after Module seven, is a due-diligence file on a real protocol, ending in a verdict with size, conditions and exit. The operator capstone, at the end, is your personal bank. Each is marked against a written rubric, and passing earns a certificate. Certificates reflect course completion only, not a licence.",
   "There are two capstones. The analyst capstone, after Module 7, is a due-diligence file on a real protocol, ending in a verdict with size, conditions and exit. The operator capstone, at the end, is your personal bank. Each is marked against a written rubric, and passing earns a certificate. Certificates reflect course completion only, not a licence.",
   chapter="Capstones", title="Two capstones, two certificates",
   left={"label": "Analyst capstone", "tone": "neutral", "items": ["After Module 7", "Due-diligence file on a real protocol", "Verdict: size, conditions, exit"]},
   right={"label": "Operator capstone", "tone": "good", "items": ["At the end of Module 14", "Your personal bank, ten sections", "Stress-tested, with every failure fixed"]})

# ---------------------------------------------------------------- success
sc("bullets", "Finally, how to succeed. Do the stages in order. Do every checklist for real, with small amounts. Use the calculators instead of guessing. And write things down: your thesis, your exit, and your policies. The people who get the most from this program are the ones who do the work, not the ones who watch the most videos.",
   chapter="How to succeed", title="How to succeed", numbered=True,
   items=["Do the stages in order", "Do every checklist for real, small amounts", "Use the calculators, not guesses", "Write down the thesis, the exit, the policy"])
sc("quiz", "Let's check the most important idea in this video. Before any position, what's the first question an operator asks? [[pause 4]] The answer: what am I being paid to risk? Then how do I get out, and how big should this be?",
   chapter="How to succeed", n=1, of=1, q="Before any position, what’s the first question an operator asks?", a="What am I being paid to risk? Then: how do I get out, and how big should it be?")
sc("bullets", "And the rules that never change. Never share your seed phrase or keys. Nobody from this program will ever ask for them. Use only money you can afford to lose while you learn. And no one, including us, can promise you returns. What you get is a process.",
   chapter="How to succeed", title="Rules that never change", check=False,
   items=["Never share a seed phrase or keys", "Never use money you can’t afford to lose", "Never trust anyone who promises returns"])
sc("bullets", "So here's your first week. Open Module Zero and print the Day-One Setup Kit. Secure your email with a password manager and two-factor. Work through the kit in order, over a few days. And take each lesson's quiz before moving on. By the end of the week, you'll be set up safely, and ready for Module One.",
   "So here's your first week. Open Module 0 and print the Day-1 Setup Kit. Secure your email with a password manager and 2FA. Work through the kit in order, over a few days. And take each lesson's quiz before moving on. By the end of the week, you'll be set up safely, and ready for Module 1.",
   chapter="Your first week", title="Your first week", numbered=True,
   items=["Open Module 0, print the Day-1 Setup Kit", "Secure your email: password manager + 2FA", "Work through the kit, in order, over a few days", "Take each lesson’s quiz before moving on"])
sc("statement", "This is education, not financial advice, and no results are guaranteed. What you're getting is a process: one you can explain, position by position, for as long as you invest.",
   chapter="Begin", kicker="Educational content only", lines=["A process,", "not a prediction."], sub="Not financial advice. No results are guaranteed. You keep custody, always.")
sc("cta", "That's how the program works. Welcome aboard, operator. Open Module Zero, and let's begin.", "That's how the program works. Welcome aboard, operator. Open Module 0, and let's begin.",
   chapter="Begin", button="Open Module 0", sub="Educational content only · Not financial advice")

spec = {"id": "how-the-program-works", "title": "How the program works (long form)", "size": [1920, 1080], "music": True, "musicLevel": 0.18,
        "tag": "How it works", "seed": 23, "maxMinutes": 25,
        "thumbnail": {"title": "How the program works", "subtitle": "The full walkthrough"},
        "use": "Start here chapter: the in-depth walkthrough of the whole program, module by module.", "scenes": S}
out = ROOT / "video-scripts" / "core" / "how-the-program-works.json"
out.write_text(json.dumps(spec, indent=1, ensure_ascii=False))
words = sum(len(s["vo"].replace("[[pause 4]]", "").split()) for s in S)
print(f"{len(S)} scenes, {words} words, est {(words / 171 * 60 + len(S) * 1.3 + 4) / 60:.1f} min")
