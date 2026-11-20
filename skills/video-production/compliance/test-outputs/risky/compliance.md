# Compliance

Status: **pending legal review**

This status stays on pending legal review until a person records approval in the review record.
Re-running the linter does not clear it.

Content: fail. Flags: 14.
Source: `samples/risky-script.txt`
Content hash: `50d067069580348597fd7e4cb524a93c1821f4fc8bc1fa63b840aca87ec48207`

| Line | Time | Kind | Text | Rewrite |
|---|---|---|---|---|
| 2 | 00:00:01.000 | hype | This strategy is guaranteed and risk-free, so you can't lose. | Say that the position can lose money. |
| 2 | 00:00:01.000 | hype | This strategy is guaranteed and risk-free, so you can't lose. | Say there is no guarantee, or describe the mechanism without a promise. |
| 2 | 00:00:01.000 | hype | This strategy is guaranteed and risk-free, so you can't lose. | Say you can lose some or all of the money. |
| 3 | 00:00:04.000 | hype | Trade like a pro. | Say "with a written plan". |
| 3 | 00:00:04.000 | hype | Proven 12% returns. | Say what was observed, and that it can fail. |
| 3 | 00:00:04.000 | hype | Proven 12% returns. | Drop the return claim. If the figure is a sketch, label it EXAMPLE and say it is not a forecast. |
| 3 | 00:00:04.000 | example-number | Proven 12% returns. | Label the figure EXAMPLE, for example "EXAMPLE: 12%". |
| 4 | 00:00:08.000 | personal-advice | You should buy this on Binance. | Describe the mechanism. Do not tell the viewer to buy, sell, or invest. |
| 4 | 00:00:08.000 | brand | You should buy this on Binance. | Remove the exchange or brand name. Describe the mechanism without naming a venue. |
| 4 | 00:00:08.000 | personal-advice | It is right for you. | Drop "right for you". The lesson is general. |
| 5 | 00:00:12.000 | example-number | The range is 90 to 110. | Label the figure EXAMPLE, for example "EXAMPLE: 90". |
| 8 | 00:00:01.000 | hype | Guaranteed profits | Say there is no guarantee, or describe the mechanism without a promise. |
| 2 | 00:00:01.000 | disclaimer | This strategy is guaranteed and risk-free, so you can't lose. Trade like a pro. Proven 12% returns. You should buy this on Binance. It is right for you. The range is 90 to 110. | Add a spoken line: "This is education, not financial advice." |
| 8 | 00:00:01.000 | disclaimer | Guaranteed profits | Put "Education, not financial advice." on screen as well as in the voice. |

A person records legal approval in the review record. This linter never writes that approval.

Nothing here publishes or sends mail.
