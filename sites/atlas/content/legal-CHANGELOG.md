DRAFT: legal wording needs Stewart's sign-off. Nothing here is committed, pushed, merged, published or deployed.

# Atlas legal pack: Legal Ops fixes applied (staged 10 Nov 2026)

- **Source review:** `/workspace/2m-plan/legal/ATLAS_LEGAL_PACK_REVIEW_2026-11-10.md` (Legal Ops).
- **Source drafts:** `kyleashton88-cyber/claude`, branch `cursor/atlas-library-buildout`, files `sites/atlas/content/{terms,privacy,disclaimer,footer-line}.md` and the `sites/atlas/*.html` pages, read on 10 Nov 2026.
- **Status:** staged on the box only, because Cursor usage is exhausted. Commit to the same branch when usage is back. Do not merge, deploy or publish.
- **Entity:** written as `Market Pros Proprietary Limited (ABN 19 679 270 387) [TO CONFIRM AGAINST ASIC]` at first mention, then `Market Pros Proprietary Limited`.
- **Email:** `contact@stewartcrowncrypto.com` is used throughout as Legal Ops wrote it. It is **still pending Stewart's confirmation** (domain owned by the business, mailbox exists and is monitored). Every file's DRAFT banner says so.
- **Placeholders left on purpose:** `[GOVERNING_LAW_STATE]`, `[POSTAL_ADDRESS]`, `[RETENTION_PERIODS: …]`, `[EFFECTIVE_DATE]`, `[HOST]`, `[PLATFORM]`, `[COUNTRY]`, `[PRIVACY_URL]`, `[CHECKLIST LINK]`, `[AFFILIATE_STATEMENT]`, `[FORM_ENDPOINT]`.

## Files staged

| File | What it is |
|---|---|
| `terms.md` | Terms of use, review fixes applied |
| `privacy.md` | Privacy policy, review fixes applied (still a BLOCKER until placeholders are real) |
| `disclaimer.md` | Disclaimer, review fixes applied |
| `footer-line.md` | F1 footer line, verbatim |
| `checklist-form-notice.md` | **New.** APP 5 notice, unticked opt-in, unsubscribe rules and reference markup for the checklist form (no such form exists in the build yet) |
| `sites/atlas/contact.html` | mailto swap, F1 footer, Disclaimer link |
| `sites/atlas/{about,academy,automation,community,crypto-fundamentals,defi-onchain,futures-leverage,index,journal-lab,learning-path,library,macro-lab}.html` | F1 footer line and Disclaimer link only (these are the 12 other pages with a Privacy/Terms legal footer) |
| `sites/atlas/{grid-bot,market-btc,market-eth,market-bnb,not-included}.html` | Follow-up edit: the same F1 footer block added (these pages had no legal footer before) |
| `CHANGELOG.md` | This file |

## Review item → file → change

### All files
| Item | File(s) | Change made |
|---|---|---|
| A1 | terms, privacy, disclaimer, footer-line, checklist-form-notice | Every `Market Pros Pty Ltd` and every "entity name to be confirmed" phrase was replaced. First mention reads `Market Pros Proprietary Limited (ABN 19 679 270 387) [TO CONFIRM AGAINST ASIC]`. |
| A2 | terms, privacy, disclaimer | `[ABN]` replaced with `19 679 270 387`, tagged TO CONFIRM AGAINST ASIC. |
| A3 | all | `[CONTACT_EMAIL: …]` replaced with `contact@stewartcrowncrypto.com`, flagged as pending Stewart's confirmation in the banner (and inline in terms and privacy). |
| A4 | terms, privacy, disclaimer | `[PRIVACY_CONTACT]` replaced with `contact@stewartcrowncrypto.com (subject line: Privacy)`. `[POSTAL_ADDRESS]` added in privacy.md only. |
| A5 | all | The old banner is **kept** (as instructed) but reworded without the em dash. Delete it on publish day. |

### terms.md
| Item | Change made |
|---|---|
| T1 | Intro sentence replaced verbatim ("By using the site you agree to these terms…signal service."). |
| T2 | "Until those placeholders are replaced…" deleted. |
| T3 | General-information / objectives-and-needs line replaced verbatim. |
| T4 | AFSL line replaced verbatim: "does not hold an Australian financial services licence or an Australian credit licence, and is not an authorised representative of a licensee." Section heading changed from "No licence is claimed" to "No licence is held" to match. |
| T5 | Licensed-adviser line replaced verbatim. |
| T7 | "or another reader's account" changed to "break or overload the site". |
| T8 | Third-party price-feed sentence added under "What Atlas is". |
| T10 | Liability exclusion narrowed to trading losses, verbatim. Follow-up edit: the cross-reference "Subject to the next paragraph" now reads "Subject to the Australian Consumer Law paragraph at the start of this Liability section", because the carve-out sits above it after T11. The drafting note about it was removed. |
| T11 | ACL carve-out replaced verbatim. The resupply-only cap was **deleted**, and the paragraph moved to the top of the Liability section. |
| T12 | Deemed acceptance ("If you keep using the site… you accept") deleted and replaced with the 30-day significant-change notice. |
| T13 | Governing-law clause replaced. `[STATE]` became `[GOVERNING_LAW_STATE]`. |
| T14 | New section "Where Atlas is offered" (UK clause) added before Contact, verbatim. |

### privacy.md
| Item | Change made |
|---|---|
| P1 | "It is written for readers, not as a substitute for legal advice…" deleted. |
| P2 | The APP-entity coverage hedge paragraph was deleted and replaced with "We handle personal information in line with the Australian Privacy Principles in the Privacy Act 1988 (Cth)." |
| P3 | "What may be collected, once Stewart confirms the live tools:" became "We collect:". |
| P4 | Host sentence replaced with `Our host, [HOST, e.g. Netlify/Vercel/Cloudflare], keeps these logs.` |
| P5 | The cookies bullet was replaced verbatim (no analytics/advertising cookies; Google Fonts, Binance's public data service and CoinGecko named as connections). The bullet label is now "Cookies and third-party connections". |
| P6 | Checklist bullet replaced verbatim (name, email, country; opt-in box; unsubscribe link; opt-outs within 5 business days). |
| P7 | "This draft does not start a mailing list" paragraph replaced verbatim (opt-in only, APP 7 and Spam Act 2003). |
| P8 | Overseas section replaced verbatim with the provider and country list. `[HOST]`, `[PLATFORM]` and the `[COUNTRY]` slots are left for Stewart. |
| P9 | Retention replaced with Legal Ops' wording. The bracketed periods are tagged `[RETENTION_PERIODS: 24 months suggested]` / `[RETENTION_PERIODS: 12 months suggested]`. |
| P10 | The breach-scheme hedge sentence deleted. |
| P11 | Access and correction now says: write to the email; response within 30 days; no charge. |
| P12 | Complaints section replaced verbatim: acknowledge within 7 days, respond within 30 days, OAIC path (www.oaic.gov.au, 1300 363 992) and `[POSTAL_ADDRESS]`. |
| P14 | "adults" became "adults (18+)". |
| (A4) | The Children section contact now uses the privacy email. |

### disclaimer.md
| Item | Change made |
|---|---|
| D1 | General-information line replaced verbatim (em dashes removed). |
| D2 | Licensed-adviser line replaced verbatim. |
| D3 | AFSL line replaced, then extended in a follow-up edit to match terms.md (T4) in full: "Market Pros Proprietary Limited does not hold an Australian financial services licence or an Australian credit licence, and is not an authorised representative of a licensee. It does not give personal advice, deal in financial products, operate a market or provide custody." Heading changed to "No licence is held". |
| D4 | "Only use money you can afford to lose" and the crypto regulatory-protection line added after the first Risk sentence. |
| D5 | "Past or example results don't indicate future results." added. |
| D7 | ACL line replaced verbatim. |

### footer-line.md and HTML footers
| Item | File(s) | Change made |
|---|---|---|
| F1 | footer-line.md | Whole line replaced verbatim. "Effective [date]" dropped. |
| F1 + footer note "add Disclaimer" | 18 staged HTML pages | Each `<nav class="legal">` was replaced with a `<p class="footer-legal-line">` holding the F1 text, followed by a legal nav in F1 order: Terms · Privacy · Disclaimer (`/disclaimer`) · `mailto:contact@stewartcrowncrypto.com`. An HTML DRAFT comment was added as line 1. |

### Checklist and contact
| Item | File | Change made |
|---|---|---|
| P13 | checklist-form-notice.md (new) | APP 5 notice verbatim. The opt-in checkbox is unticked by default, using the house wording from FORM_NOTICES_2026-10-26. The checklist must be sent whether or not the box is ticked. Unsubscribe rule included. Reference markup (no `checked` attribute) included. |
| Overall note | sites/atlas/contact.html | `mailto:support@example.com` replaced with `mailto:contact@stewartcrowncrypto.com`. |

## Left open for Stewart (review's "Stewart decides" list)
| # | Decision | Where it shows in the drafts | Review's reason |
|---|---|---|---|
| 1 | Entity name | `[TO CONFIRM AGAINST ASIC]` tags | Records say Market Pros Proprietary Limited, ABN 19 679 270 387, while the old drafts said Pty Ltd. The first mention must match ASIC exactly, so Stewart checks ASIC Connect / ABN Lookup. |
| 2 | Email | Banner in every file | contact@stewartcrowncrypto.com can only be used once Stewart confirms the domain is owned by the business and the mailbox exists and is monitored (never a personal Gmail). He also decides whether a privacy@ alias is wanted. |
| 3 | Postal address | `[POSTAL_ADDRESS]` (privacy.md) | Needed for the complaints path. A PO box is fine. |
| 4 | Governing-law state | `[GOVERNING_LAW_STATE]` (terms.md) | "Laws of Australia" is not a governing law; it needs a state. |
| 5 | Host and providers | `[HOST]`, `[PLATFORM]`, `[COUNTRY]` (privacy.md), plus a drafting note | APP 1.4(f)-(g) and APP 8 need the real overseas list. Stewart also decides whether to keep the Google Fonts and Binance/CoinGecko browser calls or to self-host or proxy them, which would remove those sentences. |
| 6 | Checklist funnel | P6, P7 and P13 applied as instructed, with drafting notes | These items apply only if the checklist form leads into the lead-magnet nurture emails. Per `lifecycle/lead-magnet-nurture.md` it does, but Stewart confirms. |
| 7 | Affiliate status | `[AFFILIATE_STATEMENT]` in terms (T9) and disclaimer (D6) | "Only if true", given the Pionex relationship. Stewart picks the no-payment line or the affiliate line. |
| 8 | UK / non-AU readers | T14 **applied** as instructed | The clause applies the standing UK exclusion, and the review says "Stewart confirms". Remove it if he doesn't approve. |
| 9 | Retention periods | `[RETENTION_PERIODS: …]` (privacy.md) | 24 and 12 months are Legal Ops' suggestions, not decisions. |
| 10 | Comments / community features | T6 **not applied**. Original paragraph kept with an inline OPEN note (terms.md) | The short "Third-party links are not endorsements." version applies only if there are no comments. If comments are planned, Legal Ops drafts a user-content clause first. |
| 11 | Effective date | `[EFFECTIVE_DATE]` on terms, privacy and disclaimer | Set on publish day, with the same date on all three. |
| 12 | Final sign-off | DRAFT banners | Each publish or deploy needs Stewart's own yes. |

## Not applied, ambiguous or needs a developer
1. **There is no checklist sign-up form in the build.** No `<form>` or email field exists in any `sites/atlas` page, so P13 is staged as a standalone file (`checklist-form-notice.md`) instead of being edited into a page.
2. **The legal pages aren't wired up (left alone as instructed).** `_redirects` sends `/privacy` and `/terms` to `/not-included.html`, and there is no `/disclaimer` route or page. The new footer links therefore point at pages that don't render yet. A developer needs to build the routes from the content md. `_redirects` was not changed or staged.
3. **Resolved in follow-up:** `grid-bot.html`, `market-btc.html`, `market-eth.html`, `market-bnb.html` and `not-included.html` had no legal footer. The same F1 block is now added inside each page's site footer (`<footer class="footer">` on grid-bot and not-included, `<footer class="market-footer">` on the market pages). The separate in-content `<footer>` on grid-bot (QA note and projections disclaimer) is unchanged.
4. **The /contact link was dropped from the 13 original legal footers** because F1 lists exactly Terms · Privacy · Disclaimer · email. A developer can re-add a Contact link if Stewart wants it.
5. **contact.html still carries its visible "Developer note: replace the placeholder email action before public deployment."** I left it in place because the email is still pending confirmation. Remove it once Stewart confirms.
6. **Resolved in follow-up:** the T10 cross-reference now points to the Australian Consumer Law paragraph above it. terms.md has no separate "Australian Consumer Law" heading (the carve-out is the first paragraph under "Liability"), so the reference names that paragraph and the Liability section.
7. **AFSL wording:** terms.md and disclaimer.md now use the same full sentence, including "is not an authorised representative of a licensee". footer-line.md and the HTML footer line stay exactly as Legal Ops' F1 ("does not hold an AFSL"), as instructed.
8. **Country slots for Binance's data service and CoinGecko** are left as `[COUNTRY]` because the review doesn't state them. They were not guessed.
9. **defi-onchain.html keeps its own footer tagline**, "Educational reference · Not financial advice". It is not in the review, so it was left unchanged; it sits alongside the F1 line.
10. **Note carried from the review:** the Privacy Act automated-decision duties (APP 1.7 to 1.9) start on 10 Dec 2026. The current build doesn't trigger them. Re-check if personalisation is added.

## Follow-up decisions (10 Nov 2026)
- **Exchange name:** kept in privacy.md only, for accurate disclosure (Orchestrator call; awaiting Stewart's sign-off). Longer-term fix: proxy or self-host the price feeds.
- **Redirects:** `/privacy`, `/terms` and `/disclaimer` routing left alone. `_redirects` is not staged or changed.
- **Source check:** the five newly staged pages were confirmed byte-identical (git blob SHA) to the current versions on `cursor/atlas-library-buildout` before editing.
- index.html hero: 'proven strategies' replaced with 'clear strategy frameworks' (banned word). 'LIVE · BINANCE' label left for the Cursor price-feed proxy fix.
