"""Ticker and jargon said the way a teacher says them.

The written word stays in the captions. Only the audio uses the spoken form.
A one-token replacement that becomes several spoken words is timed as one caption word.
"""

from __future__ import annotations

import re

# Longer keys first so "USDT" is not partly eaten by a shorter token.
SPOKEN = {
    "USDT": "U S D T",
    "USDC": "U S D C",
    "DOGE": "dohj coin",
    "HODL": "hoddle",
    "DeFi": "dee fye",
    "DEFI": "dee fye",
    "APY": "A P Y",
    "APR": "A P R",
    "TVL": "T V L",
    "KYC": "K Y C",
    "ATH": "all time high",
    "ATL": "all time low",
    "PnL": "P and L",
    "PNL": "P and L",
    "BTC": "bitcoin",
    "ETH": "eeth",
    "SOL": "sol",
    "LP": "L P",
    "API": "A P I",
}


def apply_pronunciation(text: str) -> str:
    def repl(match: re.Match) -> str:
        word = match.group(0)
        return SPOKEN.get(word, word)

    keys = sorted(SPOKEN, key=len, reverse=True)
    pattern = r"\b(?:" + "|".join(re.escape(key) for key in keys) + r")\b"
    return re.sub(pattern, repl, text)


def spoken_tokens(written: str) -> list[str]:
    """Spoken pieces for one written word. Used to group alignment back."""
    said = apply_pronunciation(written)
    return said.split()
