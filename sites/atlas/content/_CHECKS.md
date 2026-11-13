# Atlas content checks

Script: `/tmp/atlas_check.py` (not part of the site). It scans `sites/atlas/content` for the acceptance rules: education-only wording, banned phrases, labelled numeric examples, no named exchange, Stewart not Kyle, Australian spelling, checklist name, official links only, legal banners and placeholders, and (when present) `glossary.json` shape.

Word counts below are body words after front matter.

## Batch 1 — legal pack — 2026-11-10

```
Root: /agent/repos/claude/sites/atlas/content
Files: 4
  - disclaimer.md (3216 bytes)
  - footer-line.md (467 bytes)
  - privacy.md (6471 bytes)
  - terms.md (5735 bytes)
--- notes ---
disclaimer.md: 499 words
footer-line.md: 40 words
privacy.md: 1049 words
terms.md: 920 words
--- problems ---
PASS: no problems
```

## Batch 1b — support email placeholder — 2026-11-10

`[CONTACT_EMAIL]` is now `[CONTACT_EMAIL: contact@stewartcrowncrypto.com, pending Stewart's confirmation]` in terms, privacy, disclaimer, and the footer line. Stewart has not confirmed the address.

```
disclaimer.md: 511 words
footer-line.md: 46 words
privacy.md: 1061 words
terms.md: 932 words
--- problems ---
PASS: no problems
```

## Batch 2 — glossary — 2026-11-10

435 terms in `glossary.json` (unique anchors, see_also all resolve). Includes the 36 grid-bot glossary terms and the DeFi / on-chain concepts. `glossary.md` is the readable form of the same rows.

```
Root: /agent/repos/claude/sites/atlas/content
Files: 7
  - _CHECKS.md (1504 bytes)
  - disclaimer.md (3344 bytes)
  - footer-line.md (531 bytes)
  - glossary.md (201072 bytes)
  - privacy.md (6599 bytes)
  - terms.md (5863 bytes)
  - glossary.json (236857 bytes)
--- notes ---
_CHECKS.md: 189 words
disclaimer.md: 511 words
footer-line.md: 46 words
glossary.md: 31086 words
privacy.md: 1061 words
terms.md: 932 words
glossary.json rows: 435
--- problems ---
PASS: no problems
```

## Batch 3 — market structure, technical analysis, risk — 2026-11-10

Formulas checked against the usual definitions: Wilder RSI, MACD as EMA(12) minus EMA(26) with a 9-period signal, population standard deviation for Bollinger Bands, true range and Wilder ATR, VWAP as price times volume over volume, expectancy as win fraction times average win minus loss fraction times average loss, and drawdown recovery as 1/(1-d)-1. Worked numbers are marked Hypothetical example.

```
market-structure.md: 1650 words
technical-analysis.md: 2338 words
risk-academy.md: 1732 words
glossary.json rows: 435
--- problems ---
PASS: no problems
```

## Batch 4 — exchanges, security, fundamentals, Solana, questions — 2026-11-10

AUSTRAC link used is the public Virtual Asset Service Provider Register (`online.apps.austrac.gov.au/vaspr`), which is the 2026 name for what had been discussed as the digital-currency-exchange register. Scamwatch and ReportCyber links are the official ones. Solana primer is about 150 words. Find-by-question has 62 question entries.

```
crypto-fundamentals.md: 1093 words
exchanges.md: 1100 words
find-by-question.md: 2756 words
security.md: 1109 words
solana-primer.md: 152 words
--- problems ---
PASS: no problems
```

## Batch 5 — chains, primers, futures, frameworks, journal, macro, tax, automation — 2026-11-10

Primers sit near 150 words. Strategies stay at framework level. Tax page links the ATO crypto guide, ASIC INFO 225, Moneysmart, and the AUSTRAC VASP register, and it does not apply those rules to a reader. Futures worked figures are marked Hypothetical example.

```
automation.md: 626 words
chains.md: 629 words
futures.md: 904 words
hbar-primer.md: 149 words
journal.md: 567 words
link-primer.md: 159 words
ltc-primer.md: 161 words
macro-etf-flows.md: 565 words
market-strategies.md: 737 words
psychology.md: 546 words
sui-primer.md: 157 words
tax-regulation-au.md: 601 words
xrp-primer.md: 164 words
glossary.json rows: 435
--- problems ---
PASS: no problems
```
