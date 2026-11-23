# Spoken changes, 23 Nov 2026

Stewart approved every recommended spoken change by voice at 11:04am AEDT. L1 is not applied. The licensing line stays date-neutral: "From April 2027".

| ID | Old | New | Why |
|---|---|---|---|
| B1 | The hook said "a daily close is the last price of that day" after the risk line had already said "daily closes". | The risk line now starts "A daily close is the last price of that day." The hook no longer repeats that sentence. | Define the term before the first use. |
| B2 | "the summer bitcoin closes", "the summer chart", "the summer bitcoin price". | "the July to October example window", defined once as the public bitcoin closes from 19 July to 16 October 2023. | One name, matching lesson 1. |
| B3 | "band", including "a band, also called the range". | "range" in the spoken lesson and on cards 02, 05, 72–78 and 83. | One word. |
| B4 | "Say the page once, in your own words, and do not read the chart again." | "Now cover the chart and say your page out loud: the pair, the range, the gaps and the stop rule." | The listener does the page, instead of being told not to read. |
| B5 | Two currency lines: do not put them on the same row, and do not mix the two currencies. | Kept "Do not put a US dollar price and an Australian dollar fee on the same row." | The second line repeated the first. |
| T1 | "Before you deposit, look the exchange up on AUSTRAC's public register." | Cut. The register is taught in the next sentence. | The early line repeated the later one. |
| T2 | "It is also the page you will open again in lesson 8 and lesson 10." | "The journal is also the page you will open again in lesson 8 and lesson 10." | The subject was missing. |
| T3 | The columns sentence ended, then the download line. | Added "The Australian dollar value column is the one exception. It is for your tax records." | Say what that column is for. |
| L2 | The journal said a stablecoin fill goes in it. | Added "The tax office treats a swap like a sale, so every swap goes in the journal." | A swap is a record, not only a fill. |
| L3 | "An API secret is a password that lets a program place orders on an account." | Added "and sometimes move money out of it." | The secret can do more than place orders. |
| L1 | Not applied. | The line stays "From April 2027, new licensing rules..." | Legal and tax do not agree on the calendar day. |

## BP-01 v14

| ID | Change |
|---|---|
| S1 | The disclaimer says "Crypto, a digital coin, is high risk". |
| S2 | The risk line says "prices at the end of each day" instead of "daily closes". |
| S3 | The hook says "coin means the crypto itself" and then "holding the coin". |
| S4 | Added "Exchanges charge a small fee on each trade." |
| S5 | "The exchange's day starts at 11am Sydney time in daylight saving, 10am otherwise." Later W5 changes starts to ends. |
| S6 | "28 crossings, each time the price crosses a line". |
| S7 | "learner plates, or training wheels". |
| S8 | "An API secret is a secret key that lets software control your account." |
| N1/F2 | The crypto line says "A digital asset, such as bitcoin." |
| F3 | "A dollar-pegged token, treated like cash in this lesson. The peg can break." |
| F4 | "you can only sell coin you already hold, on a spot account". |
| F5 | "Hindsight: this range is drawn after the fact." |
| 9:25 | The voice says "at 27,630", not "at the middle line". |

## Wording, 23 Nov 3:26pm AEDT

Stewart approved all eight spoken changes in his own words: "Approve all 8 wording changes." The lines below are the exact wording. Part A picture, timing, and pronunciation fixes are in the same source pass. BP-01 is the render. BP-02 is source only until he says go.

| ID | Exact spoken change |
|---|---|
| W1 | "band" is now "range" in the BP-01 voice, captions, cards, and the end checklist. |
| W2 | Added "A spot account is the normal account on an exchange. You own the coin you buy, and nothing is borrowed." |
| W3 | Added "A seed phrase or private key is the master password to a crypto wallet. An API secret is a key that lets an app place trades on your account." |
| W4 | Added "900 dollars times 0.01 bitcoin is 9 dollars before fees." and "Three buys of 0.01 is 0.03 bitcoin. At 24,000, that is 720 dollars." |
| W5 | "The exchange's day ends at 11am Sydney time in daylight saving, 10am otherwise." |
| W6 | Added "We price in US dollars. Your exchange may charge fees in Australian dollars, so keep each in its own column." |
| W7 | "A fill is when your waiting order actually trades." |
| W8 | "A stablecoin is a coin built to stay worth about one US dollar." |

## BP-01 spoken lines, 23 Nov 5:26pm AEDT

Stewart approved S1–S9. The lines below are his wording. Fix order #10 (picture and timing only) is in the same source. The film is rendered after this commit.

| ID | Exact spoken change |
|---|---|
| S1 | "Here that means dollars, or a stablecoin, a crypto coin built to stay at one US dollar. We treat it like cash in this lesson, but it can drop below a dollar." |
| S2 | "finished only three pairs, each a buy and a sell on lines next to each other." |
| S3 | Added "Each fee is 0.1 percent of the whole trade, not of the profit: about 27 cents on the 267 dollar buy and 28 cents on the 276 dollar sell, 54 cents together." |
| S4 | "not the full 9 dollars" and "The fees come out of what the pair makes. If the fees are larger than that, the pair keeps nothing." Recap lines use "what the pair makes". |
| S5 | "This lesson uses the end of each UTC day, the world's standard clock, which is 11am Sydney time in daylight saving, 10am otherwise." |
| S6 | The API secret line adds ", and sometimes move money out of it." |
| S7 | "what a grid bot does. It is a small program that places these orders for you. You will learn when it can capture bounces, and where it loses." |
| S8 | "below the current price" in the three buy-and-sell lines. |
| S9 | "the opposite order one rung up or down." |

## Spoken approvals, 24 Nov 7:02am AEDT

Stewart signed off the nine BP-03 to BP-11 scripts at commit `b958dff`. Those spoken scripts are now what `lesson_scripts.py` plays. `BP-11-ALT-long-warning.md` is not a lesson. X7 is declined: BP-01 still says "an opt-in lesson on liquidation and your complete plan."

| ID | Exact spoken change |
|---|---|
| X1 | BP-01 fee line: "about 27 cents on the 267 dollar buy and about 28 cents on the 276 dollar sell, about 54 cents together." The card keeps 0.2673 + 0.2763 = 0.5436. |
| X2 | BP-02: "three words, range, levels and stop". |
| X3 | BP-02, after the gap-and-fee sentence: "To compare them, turn the gap into a percent by dividing it by the price. In the lesson 1 example, 900 divided by 27,630 is about 3.3 percent, well above 0.2 percent." |
| X4 | BP-02: "If your pair is priced in a stablecoin, every fill trades one coin for another, so every fill is a swap." |
| X5 | BP-02: "From April 2027, platforms that hold crypto for you need an ASIC licence, with a transition period to October 2027 for platforms already operating. Check ASIC for the current position." |
| X6 | BP-03 is titled "How a grid bot works, order by order." The BP-02 end line and end card say "Next lesson: How a grid bot works, order by order." |

The stop card is still for the whole chapter. A GridBot Builder block moves in the lane under that card every 8 seconds, so the picture changes without covering the card.

## Fix order 13, pictures only

No spoken word changed. The stop card draws the notebook, the stop sign, and the real daily closes, including 33,086 and 33,902 when October is spoken. The sliding block is gone. The hold gate ignores the lane under the card, so a filler block cannot pass it. A cyan bar that crosses a diagram fails the layout gate.
