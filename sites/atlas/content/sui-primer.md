---
title: Sui primer
slug: sui-primer
level: beginner
category: crypto
related:
  - crypto-fundamentals
  - chains
  - glossary
last_reviewed: 2026-11-10
status: draft
---

# Sui primer

Sui is a public layer-1 blockchain that uses proof of stake. Its native coin is SUI, which pays fees and is used in staking. The data model is object-based: assets are objects with owners and versions, rather than only balances on accounts. This page is general information. It is not a view on the price and not a recommendation to hold SUI.

That object model is why parallel execution is part of the design story. Two transactions that touch different objects need not wait for each other, under the protocol's rules. The details of finality, fees, and validator duties are chain-specific and belong in Sui's own documentation if you need to go past a primer. A transfer is still a signature. Seed-phrase rules on the [security page](security.md) apply on every chain. The directory line is on [chains](chains.md), and the glossary entries are [Sui](glossary.md#sui) and [SUI](glossary.md#sui-token).
