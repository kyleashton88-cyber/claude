---
title: Chains and ecosystems
slug: chains
level: beginner
category: crypto
related:
  - crypto-fundamentals
  - solana-primer
  - security
  - glossary
last_reviewed: 2026-11-10
status: draft
---

# Chains and ecosystems

This page is a directory. Each card says what a network is, how it reaches agreement, what fees look like in broad terms, what people build on it, and which risks belong in any study of it. It is general information. It does not rank networks, it is not a view on any price, and it is not a recommendation to hold any coin or token. Consider your own circumstances.

Designs change through upgrades. Where a detail depends on a recent upgrade or a project's own documentation, read the project's current documents before you rely on it. The background words, such as consensus, finality, layer 1, and layer 2, are on [crypto fundamentals](crypto-fundamentals.md). Short definitions are in the [glossary](glossary.md#layer-1).

## How to read a card

Every card uses the same five questions.

1. **What it is.** The job the network was designed for, and its native coin.
2. **Consensus.** How nodes agree on the next state: [proof of work](glossary.md#proof-of-work), [proof of stake](glossary.md#proof-of-stake), or another rule.
3. **Fees.** Whether fees are usually small or large beside other networks, and what makes them rise. No card quotes a fee, because fees move with demand.
4. **What is built on it.** Categories of application, not named products.
5. **Risks to study.** The failure modes that belong to this design. Every network has them. A short list is not a clean bill of health.

A sixth question applies to all of them: who holds your keys. That answer is on the [security page](security.md), and it matters more than any line on these cards.

## Bitcoin

**What it is.** The first public blockchain, launched in 2009. Its native coin is BTC. The design aims at a scarce, censorship-resistant settlement asset rather than at general computation.

**Consensus.** Proof of work. Miners compete to find a valid block about every ten minutes on average. The block subsidy halves every 210,000 blocks, roughly every four years, toward a maximum supply of 21 million BTC. The most recent halving was in April 2024. The [halving](glossary.md#halving) entry explains the schedule.

**Fees.** Paid per unit of block space. They rise sharply when many transactions compete for the same block. A simple send costs less than a complex spending script.

**What is built on it.** Payments and long-term holding, payment channels that move small transfers off the base chain, and wrapped versions of BTC on other networks. Coins are tracked as unspent outputs, the [UTXO](glossary.md#utxo) model, rather than account balances.

**Risks to study.** Fee spikes, the long-run question of whether fees replace a shrinking subsidy, mining concentration in a few pools, and the custody risk of wrapped BTC held elsewhere. The [Bitcoin](glossary.md#bitcoin) entry has the one-line version.

## Ethereum

**What it is.** A general-purpose smart-contract chain launched in 2015. Its native coin is ETH, which pays gas. Most of the token standards and DeFi designs explained in the Atlas DeFi module started here.

**Consensus.** Proof of stake since the 2022 upgrade known as the Merge. Validators lock ETH and can be penalised, or slashed, for breaking the rules. Blocks reach a deterministic checkpoint, called finality, after a short delay.

**Fees.** Gas times a gas price. A base fee rises and falls with demand and is burned. Complex contract calls cost more than transfers. Much everyday activity has moved to layer 2s that settle back to Ethereum.

**What is built on it.** Tokens, stablecoins, lending markets, automated market makers, NFTs, governance systems, staking and restaking services, and the rollups listed below.

**Risks to study.** Smart-contract bugs in the applications, not only in the chain. Concentration of staked ETH in a few services. [MEV](glossary.md#mev), where block builders reorder transactions. Token approvals that outlive their purpose. The [Ethereum](glossary.md#ethereum) entry has the one-line version.

## Solana

**What it is.** A high-throughput layer-1 chain whose native coin is SOL. It aims at short block times and parallel execution.

**Consensus.** Proof of stake, with a clock-like ordering design that lets validators agree on sequence quickly.

**Fees.** Usually small beside a congested layer 1. Not zero. Priority fees rise in busy periods.

**What is built on it.** Payments, token launches, trading applications, and consumer apps that need many small transactions.

**Risks to study.** Past outages, the hardware needed to run a validator and what that does to concentration, and the speed at which new tokens appear, which suits scams as well as builders. The longer note is the [Solana primer](solana-primer.md).

## Layer 2s

A layer 2 executes transactions away from a base chain and posts data or proofs back to it. The idea is lower fees with security that leans on the base chain. The seam between the two is where the extra risks live. The [layer 2](glossary.md#layer-2) and [rollup](glossary.md#rollup) entries define the words.

- **Arbitrum.** An [optimistic rollup](glossary.md#optimistic-rollup) on Ethereum. Transactions are assumed valid unless someone proves fraud during a challenge window, which for a withdrawal to the base chain is about a week. Fast exits exist through third parties, at a cost and with their own risk.
- **Optimism.** An optimistic rollup on Ethereum and the origin of the OP Stack, a shared software kit that other rollups also run.
- **Base.** An optimistic rollup built on the OP Stack and operated by a large listed company. That operator runs the [sequencer](glossary.md#sequencer), which is a concentration to study.
- **zkSync.** A [zero-knowledge rollup](glossary.md#zk-rollup). It posts a validity proof that the new state follows the rules, so it does not need a fraud-challenge window.
- **Starknet.** A zero-knowledge rollup that uses STARK proofs and its own contract language, Cairo.

**Risks to study for all of them.** A single sequencer can pause or reorder transactions for a time. Upgrade keys can change the rules. Bridged tokens depend on the bridge contract. Withdrawal timing differs between designs. Read who controls upgrades before you treat a layer 2 as equal to its base chain.

## BNB Chain

**What it is.** An account-based smart-contract chain compatible with Ethereum tooling. Its native coin is BNB. It was launched by the group behind one of the largest centralised exchanges, which this library does not name.

**Consensus.** A proof-of-stake variant with a relatively small validator set, which is part of why fees and block times are low.

**Fees.** Usually small.

**What is built on it.** Copies and adaptations of Ethereum applications, token launches, and payments.

**Risks to study.** A small validator set is a concentration. The chain's close link to one company is a dependence. Copied contracts bring copied bugs. The [BNB](glossary.md#bnb) entry has the one-line version.

## Other networks

These cards are shorter. Each is a starting point, not a full study.

### XRP Ledger

A ledger running since 2012 with a fixed 100 billion XRP created at launch and fees that are burned. Validators agree through the XRP Ledger consensus protocol, and each server chooses the validators it trusts. Ledgers usually close in a few seconds. Study the role of the company that holds a large XRP balance, and how the default trust lists are formed. The longer note is the [XRP primer](xrp-primer.md).

### Cardano

A proof-of-stake chain whose consensus family is called Ouroboros. Its native coin is ADA. It uses an extended version of the unspent-output model, so contracts are written differently from account-based chains. Study how quickly applications have matured and how governance decisions are made.

### Avalanche

A network of chains with a shared primary network. The best-known part is an Ethereum-compatible chain where most applications run. Its native coin is AVAX. Projects can launch their own chains with their own validator rules. Study how security differs between the primary network and a project's own chain.

### TON

The Open Network, a proof-of-stake chain first designed by the team behind a large messaging app and later carried on by an independent community. Its native coin is TON. It splits work across many chains that can grow or shrink with load. Study the dependence on one messaging app for users, and the wallet and scam patterns that arrive through chat.

### Sui

A proof-of-stake layer 1 with contracts in Move and state stored as owned objects. Its native coin is SUI. The longer note is the [Sui primer](sui-primer.md).

### Chainlink

An oracle network rather than a chain. It carries outside data, such as reference prices, to contracts on many chains. Its token is LINK. Study how many applications rely on the same feeds. The longer note is the [Chainlink primer](link-primer.md).

### Hedera

A public ledger that uses hashgraph consensus rather than a chain of blocks, governed by a council of organisations. Its native coin is HBAR, with a fixed total supply. The longer note is the [Hedera primer](hbar-primer.md).

### Litecoin

A proof-of-work chain launched in 2011 from Bitcoin's code, with faster blocks, a different hashing function, and an 84 million coin maximum. The longer note is the [Litecoin primer](ltc-primer.md).

### Dogecoin

A proof-of-work chain launched in 2013, also using Scrypt, and often merge-mined with Litecoin. Its native coin is DOGE. Unlike Bitcoin and Litecoin it has no maximum supply: a fixed number of new coins is issued with each block. Study how a fixed issuance with no cap differs from a halving schedule, and how much of its price story is social rather than technical.

## Comparing networks without ranking them

Every design gives something up. A large, open validator set tends to be slower and costlier. A small set tends to be faster and more concentrated. A layer 2 gains cheap fees and adds a seam. A council can move quickly and asks you to trust the council. None of these choices is wrong on its own. The question is whether you know which one you are relying on.

When you meet a new network, write down four facts before anything else:

1. Who can produce blocks, and how many of them there are.
2. Who can change the rules, and how.
3. Where the coins you hold actually live: on this chain, on a bridge, or with a custodian.
4. What happened in the network's worst week so far.

If the project's own documents cannot answer those, that is a finding, not a gap to fill with hope.

## Using this directory

Each card links to a glossary entry or a primer. Market pages for some of these assets show educational price data, which may be delayed. A chart shows trading activity. It does not show the design questions on this page. Read the card, then the chart, and keep the two separate in your notes.
