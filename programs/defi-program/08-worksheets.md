# On-Chain Operator Program — Worksheets & Templates

Copy these into Notion, a spreadsheet or a document. Numbers come from
`defi_calc.py`. **Never write seed phrases, private keys or passwords in any
worksheet.**

---

## W1 · Records sheet (from Lesson 0.3, keep forever)
| Date | Action (buy/sell/transfer/swap/fee/income) | Asset | Amount | Price (USD) | Fee | Network | Tx link | Notes |
|---|---|---|---|---|---|---|---|---|

## W2 · Position journal (Lesson 8.4)
| Position | Protocol / chain | Contracts | Amount | Entry date/price | Profit engine | Thesis | Kill rules | Approvals | Weekly result |
|---|---|---|---|---|---|---|---|---|---|

## W3 · Due-diligence file (Module 6; mirrors the Notion tracker)
- Protocol · chain · TVL (source/date) · risk rating · verdict
- 1 Mechanism · 2 Cash flow (organic vs subsidised) · 3 Dependencies · 4 Solvency · 5 Evidence (links) · 6 Exit
- Tokenomics: market cap, FDV, 12-month unlocks, value capture
- Governance: voting concentration, timelock
- On-chain: holders, flows, activity, depth, derivatives
- Monitoring triggers

## W4 · Risk register (Lesson 8.2)
| Position | Risk surface | Description | Likelihood 1–5 | Impact 1–5 | Score | Response |
|---|---|---|---|---|---|---|

## W5 · Portfolio plan (Lesson 8.1)
| Bucket | Target % | Current % | Holdings | Caps (protocol / chain / issuer / bridge) |
|---|---|---|---|---|
Rebalance rule: ________

## W6 · Balance sheet (Lesson 12.1)
| Assets | Value | Liabilities | Value |
|---|---|---|---|
| Collateral | | Loans | |
| Yield positions | | Margin | |
| Reserve (T0+T1) | | | |
| **Total assets** | | **Total liabilities** | |
Equity = ____ · LTV = ____ · HF = ____ · Runway (months) = ____

## W7 · Custody policy (Lesson 12.2)
- Vault: type (multisig m-of-n) · key locations (general, not exact) · allowlisted destinations · timelock
- Operating: wallet type · daily limit · protocols allowed
- Hot: float size · refill schedule
- Recovery test log: date · path tested · result

## W8 · Credit policy (Lesson 12.3)
Max LTV __% · HF floor __ · alert levels __ / __ · actions at each level · fixed or variable (why) · repayment source · collateral allowed

## W9 · Liquidity ladder (Lesson 12.4)
| Tier | Access | Holds | Target (months of obligations) | Current | Refill rule |
|---|---|---|---|---|---|
| T0 | Seconds | | | | |
| T1 | Hours | | | | |
| T2 | Scheduled | | | | |
| T3 | Days–weeks | | | | |

## W10 · Lending policy (Lesson 12.5)
| Market/vault | Collateral | Oracle | Liquidation LTV | Curator | Loss prob. (assumed) | LGD | Cap |
|---|---|---|---|---|---|---|---|

## W11 · Income portfolio & payout policy (Module 13)
`defi_calc.py income --pos "name:amount:yield:loss_prob:lgd" ... --payout 0.7`
Blended risk-adjusted yield __% · expected income __/yr · payout ratio __% · monthly payout __ · review rule ________

## W12 · Stress test (Lesson 11.4)
| Scenario | Loss | Liquidations? | Liquidity OK? | Payout OK? | Fix |
|---|---|---|---|---|---|
| Crypto −50% | | | | | |
| Stablecoin −10% | | | | | |
| Borrow rate 20% | | | | | |
| Largest protocol hacked | | | | | |
| Main L2 halted 48h | | | | | |

## W13 · Incident playbook (Lesson 11.5)
Official channels per protocol (bookmarked) · containment steps per incident type · fresh-wallet procedure · who to contact · journal template

## W14 · Alert sheet (Lesson 14.1)
| Alert | Threshold | Tool | Action |
|---|---|---|---|

## W15 · Automation permissions (Lesson 14.2)
| Bot/automation | Permission | Contract | Cap | Expiry | Revoke method |
|---|---|---|---|---|---|

## W16 · Annual review (Lesson 13.5)
Equity start/end · LTV · runway · income expected vs realised by source · losses & near-misses · payout paid vs policy · updated loss assumptions · custody & succession drill done?

## W17 · Letter of instruction (Lesson 12.6), stored apart from any key
What exists (wallet types, multisig setup) · where documents are · who the co-signer/professional is · how the executor should proceed · **no seeds, no keys, no passwords**
