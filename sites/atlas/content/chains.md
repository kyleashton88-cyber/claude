---
title: Chain directory
slug: chains
level: beginner
category: crypto
related:
  - crypto-fundamentals
  - solana-primer
  - glossary
last_reviewed: 2026-11-10
status: draft
---

# Chain directory

This is a directory of the ledgers Atlas names elsewhere, so a reader can see what each one is for. It is general information. It is not a ranking, not a list of venues, and not a view on any price. How a ledger works in general is on [crypto fundamentals](crypto-fundamentals.md). One-line definitions are in the [glossary](glossary.md#blockchain).

A chain and a trading venue are different things. Registration of a business that exchanges or custodies assets is an AUSTRAC question, explained on the [exchanges page](exchanges.md#registration-in-australia-as-general-information). Being listed here does not mean a network is suitable for you.

## How an entry is written

Each note names the native coin, the consensus family, and where a longer primer lives if there is one. Operational questions that apply to all of them — the seed phrase, the network selected in the wallet, and finality — are on the [security page](security.md) and in [crypto fundamentals](crypto-fundamentals.md#transactions).

## Bitcoin

Bitcoin is a public proof-of-work ledger. BTC is the native coin, divisible to the satoshi, with a supply schedule that halves and a cap written into the protocol. Finality is probabilistic: more confirmations make a rewrite more expensive. The glossary entry is [Bitcoin](glossary.md#bitcoin).

## Ethereum

Ethereum is a public proof-of-stake ledger built to run smart contracts. Ether pays for gas and is used in staking. Much of the DeFi vocabulary in this library, including ERC-20 tokens and account-based nonces, grew up here. See [Ethereum](glossary.md#ethereum).

## BNB Chain

BNB Chain is a smart-contract network. BNB is its native coin, used for fees on that chain. This entry names the chain and the coin. It does not name or rank a trading venue. See [BNB](glossary.md#bnb).

## Solana

Solana is a proof-of-stake layer 1 aimed at short block times and parallel execution. SOL is the native coin. The short note is the [Solana primer](solana-primer.md).

## Sui

Sui is a proof-of-stake layer 1 that records objects rather than only account balances. SUI is the native coin used for fees and staking. The short note is the [Sui primer](sui-primer.md).

## Litecoin

Litecoin is an early proof-of-work chain that took Bitcoin's broad shape and changed the hashing algorithm and the target block interval. LTC is the native coin. The short note is the [Litecoin primer](ltc-primer.md).

## Hedera

Hedera orders transactions with hashgraph consensus rather than proof-of-work blocks, and it publishes a council model for governance. HBAR is the token used for fees and network services. The short note is the [Hedera primer](hbar-primer.md). Confirm the current council and fee rules in Hedera's own documents if you need more than this directory line.

## XRP Ledger

The XRP Ledger is a public payments ledger. XRP is the native asset used for fees. Consensus is among validators, not proof of work. The short note is the [XRP primer](xrp-primer.md).

## Layer 2s, as a category

A layer 2, often a rollup, executes away from a base chain and posts data or proofs back to it. Optimistic designs and validity-proof designs differ in how they catch a bad state. A sequencer and a bridge are part of that design. Atlas does not list individual rollups here, because a directory of brands would go stale and would start to look like a ranking. The mechanism is in [networks, fees, and scaling](crypto-fundamentals.md#networks-fees-and-scaling).

## What this directory will not do

It will not tell you which chain to use. It will not quote a fee as if it were stable, because fees move with demand. It will not treat a familiar address string as safe on a second network. Before a transfer, name the asset, the contract if it is a token, the chain, and who holds the keys.
