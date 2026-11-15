# Arty — four-week Pionex operating plan

Educational operating plan for Arty. Prepared for review with Stewart.
It is not financial advice.

## Build

From the repository root:

```bash
python3 clients/arty/build/build.py
```

That command:

1. Checks every worked figure in `build/plan_math.py`.
2. Draws the charts in `build/charts.py` (matplotlib only).
3. Fills `build/template.html` and prints `Arty_Trade_Plan_v2.pdf`.

Needs Python 3.11+, the packages in `build/requirements.txt`, and Google Chrome.
Headless Chrome on this machine writes the PDF and then may keep running; the
build treats a finished file after 25 seconds as success.

Fonts in `build/fonts/` are Atkinson Hyperlegible (Braille Institute) and
Newsreader (Production Type), both under the SIL Open Font License. The license
text is next to the files.

## What else is here

| File | Role |
| --- | --- |
| `Arty_Trade_Plan_v2.pdf` | The plan. A4, 15 pages. |
| `REVIEW.md` | Gap review of the previous draft, and the fix for each gap. |
| `CHANGELOG.md` | What changed, and why. |
| `SELF_CHECK.md` | Layout, arithmetic, coverage, and wording checks. |

Example prices in the plan are constructed for the arithmetic. They are not
quotes and not results. Live Pionex fees, minimums, funding, and liquidation
prices override the planning assumptions.
