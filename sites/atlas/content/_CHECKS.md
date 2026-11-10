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
