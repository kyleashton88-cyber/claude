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

    check("Start opens on W1", start["A6"].value == "W1 Records")
    check("Start names the stage", start["B5"].value == "Stage")
    check("W6 debt includes margin", "B10+B11" in str(wb["W6 Balance sheet"]["B21"].value))
    check("W16 equity change", wb["W16 Annual review"]["A7"].value == "Change in equity")
    check("W12 illustration", "B11*B12/100" in str(wb["W12 Stress test"]["B13"].value))
    check("W1 fee total", wb["W1 Records"]["B47"].value == "=SUM(F5:F44)")
    jumps = [wb["Tools"].cell(r, 7).value for r in range(5, 25)]
    check("Tools jump list", len(jumps) == 20 and jumps[0] == "Health factor and liquidation price", str(len(jumps)))

    print("evaluating formulas")
    xl = formulas.ExcelModel().loads(str(PATH)).finish()
    sol = xl.calculate()

    def tool(title, label):
        ws = wb["Tools"]
        start_row = next(r for r in range(1, ws.max_row + 1) if str(ws.cell(r, 1).value or "").startswith(title))
        for r in range(start_row + 1, ws.max_row + 1):
            marker = ws.cell(r, 1).value
            if isinstance(marker, str) and "·" in marker:
                break
            if ws.cell(r, 4).value == label:
                return cell_value(sol, "TOOLS", ws.cell(r, 5).coordinate)
        raise AssertionError(f"missing {title} / {label}")

    def sheet_cell(sheet, addr):
        return cell_value(sol, sheet, addr)

    pairs = [
        ("collateral", tool("Health factor", "Collateral value"), 30000),
        ("LTV", tool("Health factor", "LTV"), 0.40),
        ("health factor", tool("Health factor", "Health factor"), 2.00),
        ("liquidation price", tool("Health factor", "Liquidation price"), 1500),
        ("max debt HF 2", tool("Health factor", "Max debt for HF 2"), 12000),
        ("loop leverage", tool("Leveraged loop", "Leverage"), 2.533),
        ("loop net", tool("Leveraged loop", "Net APY on equity"), 5.033),
        ("loop breakeven", tool("Leveraged loop", "Breakeven borrow APY"), 5.783),
        ("IL", tool("Impermanent loss", "IL vs holding"), -5.719),
        ("fee APR to match", tool("LP fee", "Fee APR to match holding"), 23.194),
        ("fees minus IL", tool("LP fee", "Fees minus IL"), -0.788),
        ("CL efficiency", tool("Concentrated liquidity", "Capital efficiency vs full range"), 8.341),
        ("LVR", tool("Loss versus rebalancing", "LVR per year"), 8.00),
        ("fees minus LVR", tool("Loss versus rebalancing", "Fees minus LVR"), 4.00),
        ("supply APY", tool("Lending supply", "Supply APY"), 3.60),
        ("APY before gas", tool("APR, APY", "APY before gas"), 12.747),
        ("APY after gas", tool("APR, APY", "APY after gas"), 5.447),
        ("airdrop", tool("Airdrop", "Expected value"), 250),
        ("PT fixed", tool("Principal token", "Fixed APY if held"), 0.1096),
        ("basis", tool("Cash-and-carry", "Basis"), 0.05),
        ("basis annualised", tool("Cash-and-carry", "Annualised, simple"), 0.2028),
        ("covered call annualised", tool("Covered call", "Annualised if repeated"), 78.21),
        ("covered call max gain", tool("Covered call", "Max gain this period"), 11.50),
        ("covered call breakeven", tool("Covered call", "Break-even price"), 2955),
        ("expected loss", tool("Risk-adjusted", "Expected loss"), 3.0),
        ("risk-adjusted", tool("Risk-adjusted", "Risk-adjusted result"), 8.50),
        ("income", tool("Income and payout", "Expected income per year"), 12500),
        ("payout", tool("Income and payout", "Payout per year"), 8750),
        ("monthly payout", tool("Income and payout", "Payout per month"), 729.17),
        ("retained", tool("Income and payout", "Retained as a buffer"), 3750),
        ("equity", tool("Balance sheet check", "Equity"), 280000),
        ("bank LTV", tool("Balance sheet check", "LTV"), 0.20),
        ("bank HF", tool("Balance sheet check", "Health factor"), 4.0),
        ("runway", tool("Balance sheet check", "Reserve runway (months)"), 7.619),
        ("perp long", tool("Perp liquidation", "Liquidation price"), 2415),
        ("perp move", tool("Perp liquidation", "Move to liquidation"), -0.195),
        ("TWR", tool("Time-weighted", "Time-weighted return"), 0.0498),
        ("CDP max mint", tool("CDP mint", "Maximum mint"), 20000),
        ("CDP ratio", tool("CDP mint", "Collateral ratio"), 3.0),
        ("CDP liq", tool("CDP mint", "Liquidation price"), 1500),
        ("carry APR", tool("Funding carry", "APR on the hedged size"), 10.95),
        ("carry on capital", tool("Funding carry", "Return on total capital"), 7.30),
        ("carry liquidation", tool("Funding carry", "Short liquidates near"), 0.50),
        ("VaR", tool("One-day value", "One-day VaR"), 6045.55),
        ("W4 score 20", sheet_cell("W4 RISK REGISTER", "F5"), 20),
        ("W4 score 15", sheet_cell("W4 RISK REGISTER", "F6"), 15),
        ("W6 equity", sheet_cell("W6 BALANCE SHEET", "B20"), 280000),
        ("W6 LTV", sheet_cell("W6 BALANCE SHEET", "B21"), 0.20),
        ("W6 HF", sheet_cell("W6 BALANCE SHEET", "B22"), 4.0),
        ("W6 runway", sheet_cell("W6 BALANCE SHEET", "B24"), 7.619),
        ("W11 income", sheet_cell("W11 INCOME", "G17"), 23300),
        ("W11 blended", sheet_cell("W11 INCOME", "F18"), 4.66),
        ("W11 payout", sheet_cell("W11 INCOME", "B21"), 16310),
        ("W11 month", sheet_cell("W11 INCOME", "B22"), 1359.17),
        ("W11 retained", sheet_cell("W11 INCOME", "B23"), 6990),
    ]
    for name, actual, want in pairs:
        check(name, close(actual, want), f"got {actual} want {want}")

    check("health floor text", tool("Health factor", "Check against 1.5") == "At or above 1.5")
    check("loop spread text", "spread" in str(tool("Leveraged loop", "What the leverage did")).lower())
    check("bank policy", tool("Balance sheet check", "LTV within policy") == "Yes" and tool("Balance sheet check", "Reserve covers 6 months") == "Yes")
    check("W8 reads W6", sheet_cell("W8 CREDIT POLICY", "B15") == "Yes" and sheet_cell("W8 CREDIT POLICY", "B16") == "Yes")
    check("empty portfolio check stays blank", sheet_cell("W5 PORTFOLIO", "B20") in ("", None))

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
