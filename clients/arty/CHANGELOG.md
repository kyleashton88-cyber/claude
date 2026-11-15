# Changelog

Compared with the five-page draft “ARTY Pionex Trade Plan, Capital-First Edition.”

## Removed

- The weekly account goal and the compounded markers (550.00, 605.00, 665.50, 732.05, and 5,232.05). They were being read as balances to hit. The deposit example no longer assumes they were hit.
- The dangling “Market reference” line and the claim that a snapshot ranked ETH first by volume. ETH/USDT for weeks 1 and 2 is now a process rule.
- The instruction to leave an extra 5–10% beyond the range “for stop/TP logic.” It conflicted with a close that is a percent of bot money.
- Any wording that a week should produce a result. A week with no bot, checks done, is a pass.

## Made specific

- Every percent now says what it is a percent of. Worked dollars are printed at 500.00 USDT and, separately, for an unchanged 500.00 plus a 4,500.00 deposit (equity 5,000.00).
- Position size is a formula: margin = baseline × 10% (or 5% when a phase-in or a halt says so). Planned stop = margin × 0.08, and that must be ≤ 1% of baseline. On 500.00 that is 50.00 in the bot and a 4.00 stop.
- The launch test adds week loss, 8% of every open bot, and 8% of the new bot. Three stops are 12.00 and fit under 15.00. A fourth planned stop is 16.00 and does not.
- A supposed exchange minimum of 70.00 fails, because 70.00 × 0.08 = 5.60, over the 5.00 cap. The real minimum is whatever the screen shows that day.
- Liquidation distance at 3× is 32.83% and at 5× is 19.50%, using a 0.50% maintenance assumption that must be replaced. Example prices at a fictional 3,000 are 2,015.00 / 3,985.00 at 3× and 2,415.00 / 3,585.00 at 5×. The buffer is 3% beyond the range. 5× needs six extra yeses and is not used in weeks 1–2.
- The range is built from swings plus half a daily ATR, then filtered by ATR multiples. The example (swings 2,865 and 3,135, ATR 60, bounds 2,835 and 3,165) is labelled fictional.
- Spacing must clear a live fee. The example round trip is 0.120%. The worst band of the example grid is 0.876% gross and 0.756% net. One 12.50 order keeps 0.0946 USDT after those example costs. That figure is a cost check, not a goal.
- Closes, pauses, the journal, the daily check, the weekly card, and the week-4 deposit each have a list someone else can mark yes or no.

## Kept

- Watchlist: ZEC, SOL, ETH, NEAR, DOGE, XRP, each against USDT. DODG is DOGE, and it must be confirmed on the screen.
- Starting account 500.00 USDT. Possible later deposit 4,500.00 USDT, only after the week-4 review, never into a bot that is down.
- Neutral futures grid, arithmetic, 10 to 12 intervals, 3× default, 5× only through a gate.
- The −8% and +4.8% closes, one bot in the first two weeks, two at most after that, and a weekly review with Stewart.
- Arty places every order. Stewart does not.

## Why the shape changed

The draft was five pages of principles with a few dollars attached. A first futures bot needs the dollars, the price tests, and the “do not launch” line on the same page as the button. The new plan is 15 A4 pages because each of those checks is written out once, with a picture where a picture is easier to check than a paragraph. Charts are plotted in code from `build/plan_math.py`, so a figure cannot drift away from the table underneath it.
