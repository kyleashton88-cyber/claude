---
title: Crypto fundamentals
slug: crypto-fundamentals
level: beginner
category: crypto
related:
  - security
  - exchanges
  - glossary
last_reviewed: 2026-11-10
status: draft
---

# Crypto fundamentals

This page is general information about how a public ledger works, and about the risks that sit underneath a chart. It matches the short module already on the Atlas site: liquidity, custody, token categories, networks, stablecoins, and scams. It is not a recommendation to hold any asset. Definitions in brief are in the [glossary](glossary.md#blockchain). Keys and scams are on the [security page](security.md).

## A shared ledger

A blockchain is a list of blocks. Each block points at the one before it by a **hash**, a fingerprint of the data. Change one old transaction and its hash changes, so every later block would have to be rebuilt. Participants agree on the next block through a **consensus** rule. Agreement among nodes is not the same thing as truth about the world outside the chain. An oracle, a headline, or a reserve attestation can still be wrong.

A **node** stores the ledger and checks that new blocks follow the rules. Some nodes produce blocks. Many only verify. A wallet that trusts someone else's node is trusting that operator's picture of the chain.

## Transactions

A transaction is a signed instruction: move value, or call a contract. The life of one transaction is create, sign, broadcast, wait in a mempool, get included in a block, then gather confirmations or finality.

**Finality** is the point after which reversing the transaction is impractical or impossible under the rules. Some chains offer probabilistic finality that strengthens as more blocks are built on top. Some offer a deterministic checkpoint. A transfer that is final cannot be recalled by a support desk.

A failed transaction can still cost a fee. The network did the work of rejecting it. On account-based chains a **nonce** orders an address's transactions so they cannot be replayed. A stuck nonce blocks the ones behind it.

## Keys, briefly

The private key signs. The address receives. The seed phrase recreates the keys. That is the whole custody model of self-custody, and the whole reason a seed does not belong in a message. The longer version is on the [security page](security.md). Leaving coins on a venue is the other model: the venue holds the keys, and you hold a claim on the venue.

## Consensus

**Proof of work** spends computation. Miners search for a hash below a target. Rewriting recent history means redoing that work. Bitcoin uses this family of rule. Finality is probabilistic: more confirmations make a rewrite more expensive. They do not make the newest block instantly irreversible.

**Proof of stake** locks the native coin. Validators propose or attest, and some designs slash stake for defined failures. Ethereum and many newer chains use variants. Rewards, penalties, and unbonding delays are chain-specific. Staking is a duty with a lockup, not a coupon detached from the coin's price.

A **reorg** is a switch of the recent canonical chain. Transactions in the dropped blocks may return to the mempool. Waiting for more confirmations is the ordinary defence against a shallow reorg. A **hard fork** is a rule change that old software will not accept. If the network splits, coins on one side are not the same asset as coins on the other.

## Coins, tokens, and categories

A **coin**, in this library, is the native unit of a chain, used for fees and often for mining or staking. A **token** is issued by a contract on top of a chain. The chain can halt or fork, and the token's contract can be wrong, even when the idea on the website is simple.

Categories behave differently because their designs differ:

- **Payment coins** are built to be transferred. Throughput, fees, and finality are the operational questions.
- **Smart-contract platforms** sell blockspace for programs. The native coin pays for gas, and the programs carry their own bugs.
- **Governance tokens** may vote on parameters. Holding one is not control if a treasury, a multisig, or a low turnout decides the outcome.
- **Stablecoins** aim at a reference value. The design is either a claim on an issuer's reserves, collateral locked on-chain, or another mechanism. A depeg is the reference and the market price coming apart.
- **Utility and receipt tokens** record a right inside one protocol: a pool share, a deposit, a staked claim. The right is only as good as that protocol.

**Wrapped assets** represent something held elsewhere. The wrapper can fail while the underlying asset is fine.

Supply words are easy to mix. **Circulating supply** is a provider's estimate of what is in the market. **Total supply** includes coins that exist but are locked. **Max supply** is a ceiling, if the rules have one and if those rules cannot be changed. **Market capitalisation** is price times circulating supply. It is not cash in a treasury, and it is not the cost of buying every coin. **Fully diluted valuation** multiplies price by a full supply, imagining today's price still holds when locked coins can move. That is an assumption.

## Networks, fees, and scaling

The **network** is which ledger you are talking to. An address you use on one network is not automatically a safe destination on another. Confirm the network in the wallet before you sign.

**Gas** measures work. The fee is that work times a price. Congestion raises the price of the same transfer. A complicated contract call costs more than a simple send.

A **layer 1** settles under its own consensus. A **layer 2**, often a rollup, executes elsewhere and posts data or proofs back to a base chain. An optimistic rollup allows a dispute window. A validity-proof rollup attaches a proof instead. A **sequencer** orders layer-2 transactions and can halt or censor for a time even when the base chain is fine. A **bridge** moves assets or messages across that seam. Bridges gather value and have been a common point of large losses. The seam is part of the risk, not a footnote.

## What the chart does not show

Market liquidity is depth and spread. A thin book turns a small order into a large price move. Custody decides who can move the coins. Token category decides which failure matters: an issuer, a contract, a vote, or a peg. Network choice decides the fee, the finality, and whether a transfer is even on the ledger you think it is. Stablecoins are useful settlement units and they carry issuer, collateral, and depeg risk. Scams and bad signatures matter because a blockchain transfer is often irreversible.

If you remember one operating rule, make it this: name the asset, the contract, the chain, and who holds the keys, before you talk about the price.
