# Atlas content checks

Script: `/tmp/atlas_check.py` (not part of the site). It scans `sites/atlas/content` for the acceptance rules: education-only wording, banned phrases, labelled numeric examples, no named exchange, Stewart not Kyle, Australian spelling, checklist name, official links only, legal banners and placeholders, and (when present) `glossary.json` shape.

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

Word counts are body words after front matter. Footer line is one public sentence plus the required draft banner and the four placeholders.
