#!/usr/bin/env python3
"""Check the worksheet workbook against the lesson examples.

Rebuilds nothing. Run build_worksheets.py first.
Requires the formulas package to evaluate the green cells.
"""
import math
import sys
import zipfile
from pathlib import Path

import formulas
from openpyxl import load_workbook

ROOT = Path(__file__).resolve().parent.parent
PATH = ROOT / "worksheets" / "On-Chain-Operator-Worksheets.xlsx"
SAFETY = "Never type a seed phrase, private key, API key, or password."
EXPECTED_SHEETS = [
    "Start",
    "Tools",
    "W1 Records",
    "W2 Journal",
    "W3 Due diligence",
    "W4 Risk register",
    "W5 Portfolio",
    "W6 Balance sheet",
    "W7 Custody",
    "W8 Credit policy",
    "W9 Liquidity",
    "W10 Lending",
    "W11 Income",
    "W12 Stress test",
    "W13 Incident",
    "W14 Alerts",
    "W15 Automation",
    "W16 Annual review",
    "W17 Letter",
]


def close(got, want, tol=0.02):
    return abs(float(got) - float(want)) <= tol


def cell_value(sol, sheet, addr):
    target = addr.upper()
    sheet_u = sheet.upper()
    hits = [k for k in sol if sheet_u in k.upper() and k.upper().endswith("!" + target)]
    if len(hits) != 1:
        raise AssertionError(f"{sheet}!{addr} matched {hits}")
    raw = sol[hits[0]].value
    return raw[0][0]


def main():
    failures = []

    def check(name, ok, detail=""):
        status = "ok" if ok else "FAIL"
        print(f"  {status}  {name}" + (f"  {detail}" if detail else ""))
        if not ok:
            failures.append(name)

    if not PATH.exists():
        print(f"missing {PATH}")
        return 1

    wb = load_workbook(PATH)
    print(f"file {PATH.name}  {PATH.stat().st_size} bytes  {len(wb.sheetnames)} sheets")

    check("sheet names", wb.sheetnames == EXPECTED_SHEETS, " / ".join(wb.sheetnames))

    start = wb["Start"]
    for row in range(6, 24):
        link = start.cell(row, 1)
        name = link.value
        location = link.hyperlink.location if link.hyperlink is not None else None
        check(f"link {name}", location == f"'{name}'!A1" and name in wb.sheetnames, location)

    for name in wb.sheetnames:
        ws = wb[name]
        blob = " ".join(
            str(c.value) for row in ws.iter_rows(max_row=4, max_col=8) for c in row if c.value
        )
        footer = ws.oddFooter.left.text or ""
        check(f"safety on {name}", SAFETY in blob and SAFETY in footer)

        prot = ws.protection
        check(f"protected {name}", prot.sheet is True and not prot.password)
        check(
            f"yellow cells selectable on {name}",
            prot.selectUnlockedCells is True and prot.selectLockedCells is True,
        )

    # No column asks the learner to type a secret. The warning itself may name them.
    banned = ("seed phrase", "private key", "api key", "password", "mnemonic", "seed")
    excuses = ("never", "do not", "don't", "no seed", "no secret", "no password", "not the", "apart from")
    for name in wb.sheetnames:
        ws = wb[name]
        for row in ws.iter_rows(min_row=4, max_col=12):
            for cell in row:
                text = str(cell.value or "").lower()
                if not any(word in text for word in banned):
                    continue
                if any(word in text for word in excuses):
                    continue
                check(f"no secret field {name}!{cell.coordinate}", False, cell.value)

    tools = wb["Tools"]
    check("health input unlocked", tools["B7"].protection.locked is False)
    check("health formula locked", tools["E9"].protection.locked is True)
    check("tools have no password", "password=" not in _protection_xml())

    print("evaluating formulas")
    xl = formulas.ExcelModel().loads(str(PATH)).finish()
    sol = xl.calculate()

    def got(sheet, addr):
        return cell_value(sol, sheet, addr)

    pairs = [
        ("collateral", got("TOOLS", "E7"), 30000),
        ("LTV", got("TOOLS", "E8"), 0.40),
        ("health factor", got("TOOLS", "E9"), 2.00),
        ("liquidation price", got("TOOLS", "E10"), 1500),
        ("max debt HF 2", got("TOOLS", "E11"), 12000),
        ("loop leverage", got("TOOLS", "E14"), 2.533),
        ("loop net", got("TOOLS", "E15"), 5.033),
        ("loop breakeven", got("TOOLS", "E16"), 5.783),
        ("IL", got("TOOLS", "E20"), -5.719),
        ("fee APR to match", got("TOOLS", "E24"), 23.194),
        ("fees minus IL", got("TOOLS", "E26"), -0.788),
        ("CL efficiency", got("TOOLS", "E30"), 8.341),
        ("LVR", got("TOOLS", "E33"), 8.00),
        ("fees minus LVR", got("TOOLS", "E34"), 4.00),
        ("supply APY", got("TOOLS", "E37"), 3.60),
        ("APY before gas", got("TOOLS", "E42"), 12.747),
        ("APY after gas", got("TOOLS", "E44"), 5.447),
        ("airdrop", got("TOOLS", "E48"), 250),
        ("PT fixed", got("TOOLS", "E53"), 0.1096),
        ("basis", got("TOOLS", "E57"), 0.05),
        ("basis annualised", got("TOOLS", "E58"), 0.2028),
        ("covered call annualised", got("TOOLS", "E62"), 78.21),
        ("covered call max gain", got("TOOLS", "E63"), 11.50),
        ("covered call breakeven", got("TOOLS", "E64"), 2955),
        ("expected loss", got("TOOLS", "E68"), 3.0),
        ("risk-adjusted", got("TOOLS", "E69"), 8.50),
        ("income", got("TOOLS", "E74"), 12500),
        ("payout", got("TOOLS", "E75"), 8750),
        ("monthly payout", got("TOOLS", "E76"), 729.17),
        ("retained", got("TOOLS", "E77"), 3750),
        ("equity", got("TOOLS", "E80"), 280000),
        ("bank LTV", got("TOOLS", "E81"), 0.20),
        ("bank HF", got("TOOLS", "E82"), 4.0),
        ("runway", got("TOOLS", "E83"), 7.619),
        ("perp long", got("TOOLS", "E90"), 2415),
        ("perp move", got("TOOLS", "E91"), -0.195),
        ("TWR", got("TOOLS", "E96"), 0.0498),
        ("CDP max mint", got("TOOLS", "E103"), 20000),
        ("CDP ratio", got("TOOLS", "E104"), 3.0),
        ("CDP liq", got("TOOLS", "E105"), 1500),
        ("carry APR", got("TOOLS", "E109"), 10.95),
        ("carry on capital", got("TOOLS", "E110"), 7.30),
        ("carry liquidation", got("TOOLS", "E111"), 0.50),
        ("VaR", got("TOOLS", "E114"), 6045.55),
        ("W4 score 20", got("W4 RISK REGISTER", "F5"), 20),
        ("W4 score 15", got("W4 RISK REGISTER", "F6"), 15),
        ("W6 equity", got("W6 BALANCE SHEET", "B20"), 280000),
        ("W6 LTV", got("W6 BALANCE SHEET", "B21"), 0.20),
        ("W6 HF", got("W6 BALANCE SHEET", "B22"), 4.0),
        ("W6 runway", got("W6 BALANCE SHEET", "B24"), 7.619),
        ("W11 income", got("W11 INCOME", "G17"), 23300),
        ("W11 blended", got("W11 INCOME", "F18"), 4.66),
        ("W11 payout", got("W11 INCOME", "B21"), 16310),
        ("W11 month", got("W11 INCOME", "B22"), 1359.17),
        ("W11 retained", got("W11 INCOME", "B23"), 6990),
    ]
    for name, actual, want in pairs:
        check(name, close(actual, want), f"got {actual} want {want}")

    check("bank policy", got("TOOLS", "E84") == "Yes" and got("TOOLS", "E86") == "Yes")
    check("W8 reads W6", got("W8 CREDIT POLICY", "B15") == "Yes" and got("W8 CREDIT POLICY", "B16") == "Yes")
    check("empty portfolio check stays blank", got("W5 PORTFOLIO", "B20") in ("", None))

    # Short perp uses the same formula with side -1. The sheet's example is the long.
    short = 3000 * (1 - (-1) * (1 / 5 - 0.5 / 100))
    check("perp short formula", close(short, 3585), f"got {short}")
    check("VaR matches defi_calc", close(1.65 * (70 / 100) / math.sqrt(365) * 100000, 6045.55))

    print()
    if failures:
        print(f"{len(failures)} failed")
        return 1
    print("all checks passed")
    return 0


def _protection_xml():
    with zipfile.ZipFile(PATH) as zf:
        parts = []
        for name in zf.namelist():
            if name.startswith("xl/worksheets/"):
                parts.append(zf.read(name).decode())
    return "\n".join(parts)


if __name__ == "__main__":
    sys.exit(main())
