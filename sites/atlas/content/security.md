---
title: Wallets, keys, and scams
slug: security
level: beginner
category: security
related:
  - exchanges
  - crypto-fundamentals
  - glossary
last_reviewed: 2026-11-10
status: draft
---

# Wallets, keys, and scams

We never ask for seed phrases, passwords or withdrawal-enabled keys.

This page is general information about how keys, wallets, and common scams work. It is not a recovery service, and it is not personal advice. If money has already moved, use the reporting links at the end. Do not pay a stranger who offers to get it back.

## Wallets

A wallet does not contain the coins. The coins are entries on a ledger. The wallet holds the keys that can authorise a change to those entries, and it shows balances by asking a node or an indexer.

A **hot wallet** keeps keys on a phone or a computer that is online. It is convenient for amounts you accept might be exposed. A **cold wallet** keeps keys off the internet. Cold storage reduces remote theft. It does not protect a lost seed, a coerced signature, or a mistake at the moment you move coins back online.

A **hardware wallet** is a dedicated device that signs on its own screen. Read that screen, not only the computer, because the computer can lie about what you are signing. Buy the device from a source you can verify. A pre-filled seed card in the box is a reason to stop.

An **externally owned account** is an address controlled by a private key. A **multisig** needs several keys, under a threshold, before a transaction is valid. Multisig reduces the damage from one lost key and creates a new problem if too many holders are missing or collude. The threshold and the list of holders are the design.

## Seed phrases and keys

A **seed phrase** is the word list from which the private keys are derived. Anyone with the words has the wallet. There is no ordinary password reset.

A **private key** is the secret that signs. A **public key**, and the **address** derived from it, can be shared so people can pay you. Sharing the address does not let them sign.

Write the seed down offline, in a form you can still read in ten years, and store the copies so that one fire or one theft does not take every copy. Do not type it into a website, a chat, a photo roll, or a cloud note. Do not read it aloud on a call.

**Two-factor authentication** adds a second check to an account login: an app code or a hardware key, not only a password. Text-message codes are weaker, because a SIM swap can move the number. A second factor does not help if you approve a prompt you did not start. Turn on a withdrawal whitelist, where the venue offers one, so a stolen login cannot send funds to a new address without a further change.

An **API key** lets software read an account or place orders. A bot that only needs to trade does not need permission to withdraw. Delete keys you no longer use. The automation page, when you reach it, repeats this rule.

## A short encyclopedia of scams

The pattern under every item is the same. Someone creates urgency, imitates a brand, and asks for a secret or a signature. The defence you control is to slow down and read the full request.

- **Phishing.** A message or a site copies a venue, a wallet, or a support agent. The link in the message is the trap. Type the address you already know, or use a bookmark you created yourself.
- **Wallet drainer.** A page asks you to sign a "claim" or a "mint" that actually transfers approved tokens. Read the spender, the token, and the amount on the wallet screen. Reject anything that is not the action you meant.
- **Fake token.** The ticker matches a known asset and the contract does not. Confirm the contract address from a source you already trusted.
- **Address poisoning.** A dust transfer arrives from an address that matches the start and end of one you use, so a hasty copy from history grabs the wrong string. Read the full address every time.
- **Unlimited approval.** You grant a contract an allowance with no practical cap. The allowance remains until you revoke it or the tokens are gone. Prefer a limited allowance, and review old spenders in a block explorer.
- **Rug pull.** The people who control a mint or a pool remove the liquidity or expand the supply. Anonymous control of the mint is the structural clue. A polished site is not a control.
- **Giveaway and impersonation.** A public figure, or a friend, appears to promise a doubled return if you send coins first. The account is copied. There is no double. Atlas will not run that kind of promotion.
- **Recovery scam.** After a loss, a new message offers to retrieve the funds for a fee or a signature. The funds do not come back, and the new signature can take what remains.
- **Pig-butchering romance or investment chat.** A long friendly conversation steers you to a fake dashboard that shows profits you cannot withdraw. The profit figure is a picture.
- **SIM swap.** Your phone number is moved so text codes go to someone else. Prefer an authenticator or a hardware key for accounts that can move money.
- **Dusting bait.** A tiny unknown token appears. Ignoring it is safer than interacting with its contract in the hope of selling it.
- **Fake support.** A reply asks you to install remote-access software or to "verify" a seed. Hang up. Real support for this library will not ask for that.

We never ask for seed phrases, passwords or withdrawal-enabled keys. A message that does is not from Market Pros Proprietary Limited and not from Stewart.

## Where to report

Reporting does not itself return funds. It is still worth doing, because it feeds the public record and, for cybercrime, a referral to police.

**Scamwatch**, run by the Australian Competition and Consumer Commission, is the place to read about scam types and to report a scam: [https://www.scamwatch.gov.au/](https://www.scamwatch.gov.au/).

**ReportCyber** is the Australian Cyber Security Centre's channel for reporting cybercrime, including stolen accounts and online fraud. Start from the ACSC report page, [https://www.cyber.gov.au/submit-a-report](https://www.cyber.gov.au/submit-a-report), which routes a cybercrime report into ReportCyber at [https://reportapp.cyber.gov.au/](https://reportapp.cyber.gov.au/). Use Scamwatch for the scam story. Use ReportCyber when a crime has taken an account or money through a computer or a network.

If you are unsure which form fits, submit the one that matches the harm you can describe, and do not send a seed phrase to either form or to anyone who contacts you afterwards offering help.
