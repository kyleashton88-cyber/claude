#!/usr/bin/env python3
"""DeFi strategy calculator: IL, LP break-even, concentrated-liquidity
efficiency, health factor / liquidation price, leverage loops, funding carry,
lending supply rate, APR->APY, airdrop EV, principal-token fixed yield,
cash-and-carry basis, covered calls, risk-adjusted yield, income portfolios,
a personal balance sheet, perp liquidation prices and time-weighted returns.

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


def cmd_pt(a):
    fixed = (1 / a.price) ** (365 / a.days) - 1
    simple = (1 / a.price - 1) * 365 / a.days
    print(f"PT at {a.price:g} of underlying, {a.days:g} days to maturity")
    print(f"Fixed APY if held to maturity: {fixed * 100:.2f}% (simple {simple * 100:.2f}%)")
    print(f"YT costs ~{1 - a.price:.4f} per unit: profits only if realised variable yield "
          f"(plus any points) beats ~{fixed * 100:.2f}% over the period")


def cmd_basis(a):
    b = a.future / a.spot - 1
    print(f"Basis {b * 100:.2f}% over {a.days:g} days -> {b * 365 / a.days * 100:.2f}% annualised (simple)")
    print("Locked only if both legs are held to expiry and margin is never called.")


def cmd_covered_call(a):
    cap = a.strike / a.spot - 1
    print(f"Premium {a.premium:g}% per {a.days:g}-day period "
          f"-> {a.premium * 365 / a.days:.1f}% annualised IF repeated at the same premium (it won't be exactly)")
    print(f"Max gain per period: {a.premium + cap * 100:.2f}% (upside capped at strike {a.strike:,.2f})")
    print(f"Break-even price: {a.spot * (1 - a.premium / 100):,.2f}; below that you lose like a holder, minus the premium")


def cmd_expected(a):
    haircut = a.loss_prob * a.lgd
    net = a.yield_apy - haircut * 100 - a.costs
    print(f"Headline {a.yield_apy:g}% - expected loss {haircut * 100:.2f}% "
          f"({a.loss_prob:g} x {a.lgd:g} LGD) - costs {a.costs:g}% = {net:.2f}% risk-adjusted")


def cmd_income(a):
    total = exp = 0.0
    print(f"{'position':<22}{'amount':>12}{'yield':>8}{'exp.loss':>10}{'net':>8}{'income/yr':>12}")
    for spec in a.pos:
        name, amt, y, p, lgd = spec.split(":")
        amt, y, p, lgd = float(amt), float(y), float(p), float(lgd)
        net = y - p * lgd * 100
        inc = amt * net / 100
        total += amt; exp += inc
        print(f"{name:<22}{amt:>12,.0f}{y:>7.2f}%{p * lgd * 100:>9.2f}%{net:>7.2f}%{inc:>12,.0f}")
    blended = exp / total * 100
    payout = exp * a.payout
    print(f"\nBlended risk-adjusted yield {blended:.2f}% on {total:,.0f}")
    print(f"Expected income {exp:,.0f}/yr -> pay out {a.payout:.0%} = {payout:,.0f}/yr "
          f"({payout / 12:,.0f}/month); retain {exp - payout:,.0f} as loss buffer")


def cmd_bank(a):
    coll = a.collateral
    ltv = a.debt / coll if coll else 0
    hf = coll * a.lt / a.debt if a.debt else float("inf")
    interest_m = a.debt * a.borrow_apy / 100 / 12
    obligations = a.monthly_spend + interest_m
    months = a.reserve / obligations if obligations else float("inf")
    equity = coll + a.reserve + a.other_assets - a.debt
    print(f"Assets: collateral {coll:,.0f} + reserve {a.reserve:,.0f} + other {a.other_assets:,.0f}")
    print(f"Liabilities: debt {a.debt:,.0f} at {a.borrow_apy:g}% ({interest_m:,.0f}/month interest)")
    print(f"Equity {equity:,.0f} | LTV {ltv * 100:.1f}% | health factor {hf:.2f}")
    print(f"Liquidity: reserve covers {months:.1f} months of obligations ({obligations:,.0f}/month)")
    for label, ok in (("LTV <= policy", ltv * 100 <= a.max_ltv), ("HF >= 2", hf >= 2), ("reserve >= 6 months", months >= 6)):
        print(f"  [{'PASS' if ok else 'FAIL'}] {label}")


def cmd_perp(a):
    move = 1 / a.leverage - a.mmr / 100
    liq = a.entry * (1 - move) if a.side == "long" else a.entry * (1 + move)
    print(f"{a.side} {a.leverage:g}x from {a.entry:,.2f}, maintenance margin {a.mmr:g}%")
    print(f"Approx. liquidation price {liq:,.2f} ({(liq / a.entry - 1) * 100:+.1f}%), before fees and funding")
    print(f"Margin per $1,000 of position: ${1000 / a.leverage:,.2f}")


def cmd_twr(a):
    growth = 1.0
    for r in a.period:
        growth *= 1 + r / 100
    print(f"Periods {a.period} -> time-weighted return {(growth - 1) * 100:.2f}%")
    if a.start is not None and a.end is not None and a.net_deposits is not None:
        simple = (a.end - a.start - a.net_deposits) / (a.start + a.net_deposits) * 100
        print(f"Simple gain on total capital in: {simple:.2f}% (deposits distort this; TWR measures skill)")


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

    s = sub.add_parser("pt", help="fixed yield from a principal token (yield tokenization)")
    s.add_argument("--price", type=float, required=True, help="PT price in units of the underlying, e.g. 0.96")
    s.add_argument("--days", type=float, required=True)
    s.set_defaults(fn=cmd_pt)

    s = sub.add_parser("basis", help="cash-and-carry basis")
    s.add_argument("--spot", type=float, required=True)
    s.add_argument("--future", type=float, required=True)
    s.add_argument("--days", type=float, required=True)
    s.set_defaults(fn=cmd_basis)

    s = sub.add_parser("covered-call", help="covered call / options vault economics")
    s.add_argument("--spot", type=float, required=True)
    s.add_argument("--strike", type=float, required=True)
    s.add_argument("--premium", type=float, required=True, help="premium per period, percent of spot")
    s.add_argument("--days", type=float, default=7)
    s.set_defaults(fn=cmd_covered_call)

    s = sub.add_parser("expected", help="risk-adjusted yield after expected losses")
    s.add_argument("--yield-apy", type=float, required=True)
    s.add_argument("--loss-prob", type=float, required=True, help="annual probability of a loss event, 0-1")
    s.add_argument("--lgd", type=float, default=1.0, help="loss given default, 0-1")
    s.add_argument("--costs", type=float, default=0.0, help="gas/fees as percent per year")
    s.set_defaults(fn=cmd_expected)

    s = sub.add_parser("income", help="income portfolio: risk-adjusted income and payout")
    s.add_argument("--pos", action="append", required=True, help="name:amount:yield%:loss_prob:lgd (repeat)")
    s.add_argument("--payout", type=float, default=0.7, help="share of expected income paid out, 0-1")
    s.set_defaults(fn=cmd_income)

    s = sub.add_parser("bank", help="personal balance sheet: LTV, health factor, liquidity runway")
    s.add_argument("--collateral", type=float, required=True)
    s.add_argument("--lt", type=float, default=0.8)
    s.add_argument("--debt", type=float, default=0.0)
    s.add_argument("--borrow-apy", type=float, default=0.0)
    s.add_argument("--reserve", type=float, default=0.0, help="liquid stablecoin reserve")
    s.add_argument("--other-assets", type=float, default=0.0)
    s.add_argument("--monthly-spend", type=float, default=0.0)
    s.add_argument("--max-ltv", type=float, default=30.0, help="policy max LTV, percent")
    s.set_defaults(fn=cmd_bank)

    s = sub.add_parser("perp", help="approximate liquidation price of an isolated perp position")
    s.add_argument("--entry", type=float, required=True)
    s.add_argument("--leverage", type=float, required=True)
    s.add_argument("--side", choices=["long", "short"], default="long")
    s.add_argument("--mmr", type=float, default=0.5, help="maintenance margin, percent")
    s.set_defaults(fn=cmd_perp)

    s = sub.add_parser("twr", help="time-weighted return across periods")
    s.add_argument("--period", type=float, action="append", required=True, help="return of each period, percent (repeat)")
    s.add_argument("--start", type=float)
    s.add_argument("--end", type=float)
    s.add_argument("--net-deposits", type=float)
    s.set_defaults(fn=cmd_twr)

    a = p.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
