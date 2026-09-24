# On-Chain Operator Program — Complete Mastery Map

![The path to mastery](assets/diagrams/path-to-mastery.png)

This is the full syllabus by **topic**: every subject a complete DeFi mastery
course needs, where it's taught, and at what level. Use it to check coverage,
find a topic quickly, or plan a learner's path.

**Levels:** **B** = Beginner (Mastery Starter or foundation lesson) ·
**P** = Practitioner (can do it safely) · **M** = Master (can design, size,
hedge and teach it).

---

## How mastery works in every module

Every module follows the same path, so a complete beginner can start anywhere:

1. **Mastery Starter (N.0):** 60-second plain-English version, key words, prerequisites, a first safe step, and the module's own beginner → practitioner → master ladder.
2. **Lessons (N.1…):** Objective → Explanation → Worked example → Checklist → 3-question quiz, each with at least one image.
3. **Module practical:** do it for real, with small amounts.
4. **Mastered when…:** each starter states the test (e.g. "you can open, monitor and unwind a borrow without approaching liquidation").
5. **Capstones:** analyst (after Module 7), operator (Module 14), graded against rubrics (`07-program-operations.md`).

---

## Topic map by domain

### 1. Money, blockchains and the basics
| Topic | Where | Level |
|---|---|---|
| What money, ledgers and blockchains are | 0.0, 0.1 | B |
| BTC, ETH, stablecoins, smart contracts, DeFi | 0.1, 1.1 | B |
| The DeFi stack and risk-first mindset | 1.1 | B |
| Transactions, gas, nonces, finality | 1.2 | B |
| Glossary of core terms | 0.8, every N.0 | B |

### 2. Accounts, custody and security
| Topic | Where | Level |
|---|---|---|
| Exchange accounts, KYC, 2FA, allowlists | 0.2 | B |
| Custodial vs self-custody | 0.4 | B |
| Wallet setup, seed backup, restore test | 0.5 | B |
| Keys, hardware wallets, multisig, smart wallets | 1.3 | B–P |
| Approvals, allowances, Permit signatures | 1.4 | B–P |
| Scam defence: phishing, drainers, address poisoning | 1.6, 0.8 | B |
| Reading signatures, simulation, blind signing, account delegation | 1.7 | P |
| Privacy and physical security | 1.8 | P |
| Bank-grade custody architecture, limits, allowlists, timelocks | 12.2 | M |
| Multisig signing procedures and change control | 14.3 | M |
| Incident response and fresh-wallet procedure | 11.5 | M |

### 3. Trading and execution
| Topic | Where | Level |
|---|---|---|
| Buying first crypto; market vs limit orders; fees | 0.3 | B |
| DEXs, aggregators, routing | 2.1 | B |
| AMM mathematics (x·y=k), price impact | 2.2 | P |
| MEV and trade protection | 2.5 | P |
| Limit, TWAP and intent-based orders | 2.6 | P–M |

### 4. Liquidity providing
| Topic | Where | Level |
|---|---|---|
| Providing liquidity and fee APR | 2.3 | B–P |
| Impermanent loss and true LP P&L | 2.4 | P |
| Concentrated liquidity and range management | Strategy #5, 10.5 | M |
| LP vs grid bot | 9.1–9.3 | P–M |

### 5. Lending, borrowing and leverage
| Topic | Where | Level |
|---|---|---|
| Money markets, utilisation, rate curves | 3.1 | B–P |
| LTV, liquidation threshold, health factor | 3.2 | P |
| Liquidations and cascades | 3.3 | P |
| Borrowing strategies and looping | 3.4 | P–M |
| Credit lines and credit policy | 12.3 | M |
| Being the lender: curated vaults, credit risk | 12.5 | M |

### 6. Derivatives
| Topic | Where | Level |
|---|---|---|
| Perpetual futures, margin, liquidation price | 3.5 | P |
| Funding, open interest, positioning data | 7.8 | P |
| Basis (cash-and-carry) | 10.2 | M |
| Delta-neutral funding carry | 10.3 | M |
| Options: covered calls, cash-secured puts, vaults | 10.4 | M |
| Hedging with perps and options | 11.1 | M |

### 7. Yield
| Topic | Where | Level |
|---|---|---|
| Where returns come from (5 sources) | 8.3 Part 1, 4.0 | B |
| Farming: base yield vs emissions | 4.1 | B–P |
| Staking and liquid staking | 4.2, 4.3 | B–P |
| Restaking and points | 4.4, 10.6 | P–M |
| Vaults and optimisers | 4.5 | P |
| Airdrops as expected-value bets | 4.6 | P |
| Fixed-rate yield (PT/YT) | 10.1 | M |

### 8. Stablecoins, cash and real-world assets
| Topic | Where | Level |
|---|---|---|
| Stablecoin designs and depegs | 1.5 | B |
| Savings rates and yield-bearing stablecoins | 4.7 | P |
| Tokenized treasuries and RWAs | 4.8 | P |
| DeFi cash management and the liquidity ladder | Strategy #14, 12.4 | M |

### 9. Infrastructure and multi-chain
| Topic | Where | Level |
|---|---|---|
| Networks and first transfers | 0.6 | B |
| Bridges and trust models | 5.1 | P |
| Layer 2s, sequencers, withdrawals | 5.2 | P |
| Oracles and manipulation | 5.3 | P |
| Smart contracts, proxies, admin keys, timelocks | 5.4 | P |
| Contract risk and reading audits | 5.5 | P–M |
| Solana, Bitcoin in DeFi, other ecosystems | 5.6 | P |
| Cross-chain gas, routes, chain abstraction | 5.7 | P–M |

### 10. Research and analytics
| Topic | Where | Level |
|---|---|---|
| Protocol due diligence (6-step loop) | 6.1 | P |
| Tokenomics, FDV, unlocks, value capture | 6.2 | P |
| Governance and DAOs | 6.3 | P |
| Research workflow and theses | 6.4 | P–M |
| Failure case studies and patterns | 6.5 | P–M |
| On-chain data, explorers, flows, whales | 7.1–7.4 | P |
| Holder/supply metrics, network activity, DEX analytics | 7.5–7.7 | P–M |

### 11. Strategy, portfolio and performance
| Topic | Where | Level |
|---|---|---|
| Portfolio buckets and caps | 8.1 | P |
| Risk register | 8.2 | P |
| 25-strategy library (6 levels) | 8.3 | P–M |
| Operating playbook: deploy, monitor, respond, review | 8.4 | P |
| Performance measurement: TWR, benchmarks, attribution | 8.5 | M |
| Psychology and discipline | 8.6 | P–M |
| Stress testing | 11.4 | M |
| Protection: cover, liquidation automation | 11.2, 11.3 | M |

### 12. Operating as your own bank
| Topic | Where | Level |
|---|---|---|
| Balance sheet, equity, LTV, runway | 12.1 | M |
| Custody, credit, ladder and lending policies | 12.2–12.5 | M |
| Books, records and succession | 12.6 | M |
| Tax, regulation and compliance awareness | 12.7 | P–M |

### 13. Income
| Topic | Where | Level |
|---|---|---|
| Income sources by durability | 13.1 | P |
| Risk-adjusted yield | 13.2 | P–M |
| Building the income portfolio | 13.3 | M |
| Payout policy | 13.4 | M |
| Scaling, compounding, annual review | 13.5 | M |

### 14. Automation and tools
| Topic | Where | Level |
|---|---|---|
| Monitoring and alerts | 14.1 | P–M |
| Automation with scoped permissions | 14.2 | M |
| Building read-only tools, APIs, RPC | 14.5 | M |
| Operator capstone and certification | 14.4 | M |

---

## Coverage check

Every domain has a **Beginner** entry point (a Mastery Starter or foundation
lesson), **Practitioner** lessons with safe hands-on practice, and **Master**
lessons that design, size and hedge. The totals:

- **15 Mastery Starters** (one per module)
- **92 lessons** across 14 domains
- **278 quiz questions**, **25 strategy playbooks**, **17 worksheets**, **17 calculators**
- **2 capstones** and **3 certification levels**

---

## Section plan (for building and reviewing in parts)

The program is split into six section files, one per stage, in `sections/`,
regenerated by `build_master.py`. Each can be reviewed or handed to an AI on its own:

| Section file | Stage | Modules | Lessons (+ starters) |
|---|---|---|---|
| `sections/section-0-zero.md` | 0 · Zero | 0 | 8 (+1) |
| `sections/section-1-foundations.md` | 1 · Foundations | 1–2 | 14 (+2) |
| `sections/section-2-practitioner.md` | 2 · Practitioner | 3–5 | 20 (+3) |
| `sections/section-3-analyst.md` | 3 · Analyst | 6–7 | 13 (+2) |
| `sections/section-4-strategist.md` | 4 · Strategist | 8–11 | 20 (+4) |
| `sections/section-5-operator.md` | 5 · Operator | 12–14 | 17 (+3) |
