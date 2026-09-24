#!/usr/bin/env python3
"""Grid bot planner: levels, capital per grid and fee-adjusted step size.

Educational modelling only. Check live exchange tick size, minimum order
size, fees, spread and funding before using any configuration.
"""
import argparse


def levels(lower, upper, grids, mode):
    if mode == "arithmetic":
        step = (upper - lower) / grids
        return [lower + i * step for i in range(grids + 1)]
    ratio = (upper / lower) ** (1 / grids)
    return [lower * ratio**i for i in range(grids + 1)]


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--lower", type=float, required=True)
    p.add_argument("--upper", type=float, required=True)
    p.add_argument("--grids", type=int, required=True, help="number of intervals")
    p.add_argument("--capital", type=float, required=True)
    p.add_argument("--mode", choices=["arithmetic", "geometric"], default="arithmetic")
    p.add_argument("--fee", type=float, default=0.1, help="fee per side, percent")
    p.add_argument("--slippage", type=float, default=0.0, help="round-trip slippage, percent")
    p.add_argument("--funding", type=float, default=0.0, help="funding cost per cycle, percent (futures)")
    a = p.parse_args()

    if not 0 < a.lower < a.upper or a.grids < 1 or a.capital <= 0:
        p.error("need 0 < lower < upper, grids >= 1, capital > 0")

    lv = levels(a.lower, a.upper, a.grids, a.mode)
    cost = 2 * a.fee + a.slippage + a.funding
    steps = [(lv[i + 1] - lv[i]) / lv[i] * 100 for i in range(a.grids)]
    worst, best = min(steps), max(steps)

    print(f"Range {a.lower:,.4f} – {a.upper:,.4f} "
          f"(width {a.upper - a.lower:,.4f}, {(a.upper / a.lower - 1) * 100:.2f}%)")
    print(f"Mode {a.mode}, {a.grids} grids, capital per grid {a.capital / a.grids:,.2f}")
    print(f"Gross step {worst:.3f}%–{best:.3f}% | round-trip cost {cost:.3f}% "
          f"| net step {worst - cost:.3f}%–{best - cost:.3f}%")
    print("\nLevels:")
    for i, price in enumerate(lv):
        print(f"  {i:>3}  {price:,.4f}")

    net = worst - cost
    if net <= 0:
        print("\nFAIL: smallest step does not cover fees/slippage. Widen spacing or cut grid count.")
    elif net < cost:
        print("\nWARN: net step is thinner than round-trip cost; fee sensitivity is high.")
    else:
        print("\nOK: every step clears estimated costs. Still confirm regime, range and invalidation.")


if __name__ == "__main__":
    main()
