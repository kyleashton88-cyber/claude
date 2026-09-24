# DeFi Program: build files

**Everything in one file:** `ON-CHAIN-OPERATOR-PROGRAM.md`, also as `On-Chain-Operator-Program.docx` (Word) and `On-Chain-Operator-Program.pdf`.
Rebuild: `python3 programs/defi-program/build_master.py`, then `cd programs/defi-program/export && npm install && npm run build`.
**To finish the build with AI:** paste `BUILD-PROMPT.md` into Claude Code.

| File | Phase | Status |
|---|---|---|
| `01-offer-and-curriculum.md` | 1–2 Offer + curriculum | Decisions locked; curriculum expanded to 6 stages · 15 modules · 79 lessons |
| `02-sample-lesson-amm-math.md` | Lesson 2.2 | Written |
| `03-defi-strategy-mastery.md` | Lesson 8.3 (strategy library) | Written |
| `04-funnel-changes.md` | 4 Funnel wiring | Draft, not applied to Zapier |
| `05-whop-setup.md` | 3 Whop setup | Decisions locked; waiting on Whop reconnect + product ID |
| `06-whop-store-listing.md` | Store product listing: copy + image upload map | Ready to paste (3 placeholders) |
| `assets/` | 53 images: logo system (8), store icon + banner + 7 gallery (9), 15 module banners, 16 diagrams, 5 charts | Rendered by `export/build_images.js` |
| `Day-1-Setup-Kit.pdf` | Printable beginner setup checklist (generated from Module 0) | Built by `npm run build` |
| `lessons/module-00-crypto-from-zero.md` | Module 0 (8) + Day-1 Setup Kit | Written |
| `lessons/module-01-foundations-safety.md` | Module 1 (6) | Written |
| `lessons/module-02-trading-on-chain.md` | Module 2 (4 + sample 2.2) | Written |
| `lessons/module-09-defi-vs-grid-bots.md` | Module 9 (3) | Written |
| `lessons/module-10-advanced-yield-engineering.md` | Module 10 (6) | Written |
| `lessons/module-12-own-bank.md` | Module 12 (6) | Written |
| `lessons/module-13-income-engine.md` | Module 13 (5) | Written |


Lessons written: 40 of 79 (Modules 0, 1, 2, 9, 10, 12, 13 + lesson 8.3).
Still to write (39): Modules 3–7 · lessons 8.1, 8.2, 8.4 · Module 11 · Module 14.
Phase 3: blocked until Whop is reconnected in Zapier and the product is created in the Whop dashboard (see `05-whop-setup.md`).
