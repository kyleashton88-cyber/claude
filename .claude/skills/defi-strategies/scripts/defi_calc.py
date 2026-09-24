#!/usr/bin/env python3
"""DeFi strategy calculator: IL, LP break-even, concentrated-liquidity
efficiency, health factor / liquidation price, leverage loops, funding carry,
lending supply rate, APR->APY and airdrop EV.

Educational modelling only. Rates are inputs you supply from live sources;
outputs are not forecasts.
"""
import argparse
import math


def il(r):
    """Impermanent loss of a 50/50 constant-product LP vs holding, as a fraction."""
    return 2 * math.sqrt(r) / (1 + r) - 1


def cmd_il(a):
    print(f"Price ratio {a.ratio:g}x -> IL vs holding {il(a.ratio) * 100:.2f}%")
    print("\nReference:")
    for r in (0.5, 0.75, 1.25, 1.5, 2, 3, 4, 5):
        print(f"  {r:>5g}x  {il(r) * 100:7.2f}%")


def cmd_lp_breakeven(a):
    loss = -il(a.ratio)
    need = loss * 365 / a.days
    print(f"{a.ratio:g}x move -> IL {loss * 100:.2f}%. Over {a.days:g} days you need "
          f"fee APR >= {need * 100:.2f}% just to match holding.")
    if a.fee_apr is not None:
        earned = a.fee_apr / 100 * a.days / 365
        print(f"At {a.fee_apr:g}% fee APR you'd earn {earned * 100:.2f}% -> "
              f"net vs holding {(earned - loss) * 100:+.2f}%")


def cmd_cl(a):
    if not 0 < a.low < a.high:
        raise SystemExit("need 0 < low < high")
    eff = 1 / (1 - (a.low / a.high) ** 0.25)
    mid = math.sqrt(a.low * a.high)
    print(f"Range {a.low:g}-{a.high:g} (geometric mid {mid:,.4f}, width x{a.high / a.low:.3f})")
    print(f"Capital efficiency vs full range ~{eff:.1f}x (fees and IL both scale by ~this while in range)")
    print("Out of range: 0% fees, position becomes 100% one asset.")


def cmd_health(a):
    coll = a.qty * a.price
    hf = coll * a.lt / a.debt
    liq = a.debt / (a.qty * a.lt)
    print(f"Collateral ${coll:,.2f}, debt ${a.debt:,.2f}, LTV {a.debt / coll * 100:.1f}%")
    print(f"Health factor {hf:.2f} | liquidation price {liq:,.4f} "
          f"({(liq / a.price - 1) * 100:+.1f}% from now)")
    for floor in (1.5, 2.0):
        max_debt = coll * a.lt / floor
        print(f"  Max debt for HF {floor}: ${max_debt:,.2f}")
    if hf < 1.5:
        print("WARN: HF below 1.5 - repay or add collateral.")


def cmd_loop(a):
    L = a.ltv
    if not 0 < L < 1:
        raise SystemExit("ltv must be between 0 and 1")
    lev = (1 - L ** (a.loops + 1)) / (1 - L)
    net = a.collateral_apy * lev - a.borrow_apy * (lev - 1)
    breakeven = a.collateral_apy * lev / (lev - 1) if lev > 1 else float("inf")
    print(f"LTV {L:g}, {a.loops} loops -> leverage {lev:.2f}x (max {1 / (1 - L):.2f}x)")
    print(f"Net APY on equity {net:.2f}% (unlevered {a.collateral_apy:.2f}%)")
    print(f"Borrow rate that wipes out the return: {breakeven:.2f}%")
    if net <= a.collateral_apy:
        print("WARN: leverage adds nothing (spread <= 0). Don't loop.")


def cmd_carry(a):
    apr = a.rate_8h * 3 * 365
    margin = 1 / a.short_lev
    capital = 1 + margin
    on_capital = apr / capital
    print(f"Funding {a.rate_8h:g}%/8h -> {apr:.2f}% APR on hedged size")
    print(f"Short at {a.short_lev:g}x: capital per $1 hedged = ${capital:.2f} -> "
          f"~{on_capital:.2f}% on total capital")
    print(f"Short leg liquidates on roughly a +{100 / a.short_lev:.0f}% move "
          f"(before maintenance margin) - keep a buffer.")


def cmd_supply(a):
    s = a.borrow_apy * a.utilisation * (1 - a.reserve_factor)
    print(f"Supply APY ~ {a.borrow_apy:g}% x {a.utilisation:g} x (1 - {a.reserve_factor:g}) = {s:.2f}%")


def cmd_apy(a):
    apy = (1 + a.apr / 100 / a.n) ** a.n - 1
    print(f"{a.apr:g}% APR compounded {a.n}x/yr -> {apy * 100:.2f}% APY (before gas)")
    if a.position and a.gas:
        per = a.position * a.apr / 100 / a.n
        print(f"Reward per compound ${per:,.2f} vs gas ${a.gas:,.2f} "
              f"-> {'OK' if per >= 10 * a.gas else 'compound less often'}")


def cmd_airdrop(a):
    ev = a.probability * a.value - a.costs
    print(f"EV = {a.probability:g} x ${a.value:,.2f} - ${a.costs:,.2f} = ${ev:,.2f}")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("il", help="impermanent loss for a price ratio")
    s.add_argument("--ratio", type=float, required=True, help="new price / entry price, e.g. 2")
    s.set_defaults(fn=cmd_il)

    s = sub.add_parser("lp-breakeven", help="fee APR needed to beat holding")
    s.add_argument("--ratio", type=float, required=True)
    s.add_argument("--days", type=float, required=True)
    s.add_argument("--fee-apr", type=float, help="actual fee APR, percent")
    s.set_defaults(fn=cmd_lp_breakeven)

    s = sub.add_parser("cl", help="concentrated liquidity efficiency for a range")
    s.add_argument("--low", type=float, required=True)
    s.add_argument("--high", type=float, required=True)
    s.set_defaults(fn=cmd_cl)

    s = sub.add_parser("health", help="health factor and liquidation price")
    s.add_argument("--qty", type=float, required=True, help="collateral units")
    s.add_argument("--price", type=float, required=True, help="collateral price")
    s.add_argument("--lt", type=float, required=True, help="liquidation threshold, e.g. 0.8")
    s.add_argument("--debt", type=float, required=True, help="debt value")
    s.set_defaults(fn=cmd_health)

    s = sub.add_parser("loop", help="leveraged lending loop")
    s.add_argument("--ltv", type=float, required=True, help="borrow LTV per loop, e.g. 0.7")
    s.add_argument("--loops", type=int, required=True)
    s.add_argument("--collateral-apy", type=float, required=True, help="percent")
    s.add_argument("--borrow-apy", type=float, required=True, help="percent")
    s.set_defaults(fn=cmd_loop)

    s = sub.add_parser("carry", help="delta-neutral funding carry")
    s.add_argument("--rate-8h", type=float, required=True, help="funding per 8h, percent, e.g. 0.01")
    s.add_argument("--short-lev", type=float, default=1.0, help="leverage on the short leg")
    s.set_defaults(fn=cmd_carry)

    s = sub.add_parser("supply", help="lending supply APY from borrow side")
    s.add_argument("--borrow-apy", type=float, required=True)
    s.add_argument("--utilisation", type=float, required=True, help="0-1")
    s.add_argument("--reserve-factor", type=float, default=0.1, help="0-1")
    s.set_defaults(fn=cmd_supply)

    s = sub.add_parser("apy", help="APR to APY and compounding vs gas")
    s.add_argument("--apr", type=float, required=True)
    s.add_argument("--n", type=int, default=365, help="compounds per year")
    s.add_argument("--position", type=float, help="position size, $")
    s.add_argument("--gas", type=float, help="gas per compound, $")
    s.set_defaults(fn=cmd_apy)

    s = sub.add_parser("airdrop", help="airdrop expected value")
    s.add_argument("--probability", type=float, required=True, help="0-1")
    s.add_argument("--value", type=float, required=True, help="expected $ if it happens")
    s.add_argument("--costs", type=float, required=True, help="gas + bridge + opportunity cost, $")
    s.set_defaults(fn=cmd_airdrop)

    a = p.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
