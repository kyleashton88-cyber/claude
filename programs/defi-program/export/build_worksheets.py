#!/usr/bin/env python3
"""Build the downloadable worksheet workbook.

The module is an Excel workbook, not a web page. People open it in Excel,
Google Sheets, LibreOffice, or Numbers, type in the yellow cells, and the
green cells answer with the same formulas as defi_calc.py.

Usage (from programs/defi-program/export):
  python3 build_worksheets.py
Writes programs/defi-program/worksheets/On-Chain-Operator-Worksheets.xlsx
"""
from pathlib import Path

from openpyxl import Workbook
from openpyxl.comments import Comment
from openpyxl.formatting.rule import CellIsRule, FormulaRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Protection, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.worksheet.hyperlink import Hyperlink
from openpyxl.worksheet.page import PageMargins

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "worksheets" / "On-Chain-Operator-Worksheets.xlsx"

INK = "07111C"
TEAL = "0A5C48"
PAPER = "F3F6F8"
INPUT = "FFF6D8"
CALC = "E7F6F1"
WARN = "F8EFEA"
WHITE = "FFFFFF"
LINE = "C5D0DA"
MUTED = "3E4C59"
AMBER = "9A3412"

THIN = Border(
    left=Side(style="thin", color=LINE),
    right=Side(style="thin", color=LINE),
    top=Side(style="thin", color=LINE),
    bottom=Side(style="thin", color=LINE),
)
FONT = "Calibri"
SAFETY = (
    "Educational only. Not financial, tax, or legal advice. "
    "Never type a seed phrase, private key, API key, or password."
)


def font(size=11, bold=False, color=INK, italic=False):
    return Font(name=FONT, size=size, bold=bold, color=color, italic=italic)


def fill(hex_color):
    return PatternFill("solid", fgColor=hex_color)


def apply(cell, value=None, *, bold=False, size=11, color=INK, bg=None, align="left",
          fmt=None, locked=True, wrap=True, italic=False):
    if value is not None:
        cell.value = value
    cell.font = font(size, bold, color, italic)
    if bg:
        cell.fill = fill(bg)
    cell.alignment = Alignment(horizontal=align, vertical="center", wrap_text=wrap)
    cell.protection = Protection(locked=locked)
    if fmt:
        cell.number_format = fmt
    return cell


def banner(ws, title, lesson, note, cols):
    ws.sheet_view.showGridLines = False
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.page_setup.paperSize = ws.PAPERSIZE_TABLOID
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.page_margins = PageMargins(left=0.5, right=0.5, top=0.6, bottom=0.6, header=0.25, footer=0.25)
    ws.oddHeader.left.text = "On-Chain Operator Program"
    ws.oddFooter.left.text = SAFETY
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=cols)
    apply(ws.cell(1, 1), title, bold=True, size=18, color=WHITE, bg=INK, align="left")
    ws.row_dimensions[1].height = 28
    ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=cols)
    apply(ws.cell(2, 1), lesson, size=12, color=TEAL, bg=PAPER, italic=True)
    ws.row_dimensions[2].height = 18
    ws.merge_cells(start_row=3, start_column=1, end_row=3, end_column=cols)
    apply(ws.cell(3, 1), note, size=11, color=MUTED, bg=PAPER, wrap=True)
    ws.row_dimensions[3].height = 32
    ws.freeze_panes = "A5"
    ws.sheet_properties.tabColor = TEAL
    ws.oddHeader.center.text = title


def paint_header(ws, row, headers, bg=INK):
    for col, text in enumerate(headers, 1):
        cell = ws.cell(row, col, text)
        apply(cell, bold=True, size=11, color=WHITE, bg=bg, align="left")
        cell.border = THIN
    ws.row_dimensions[row].height = 22
    ws.auto_filter.ref = f"A{row}:{get_column_letter(len(headers))}{row + 1}"
    ws.freeze_panes = f"A{row + 1}"


def blank_rows(ws, start, count, cols, dropdowns=None):
    for r in range(start, start + count):
        for c in range(1, cols + 1):
            cell = ws.cell(r, c, None)
            apply(cell, locked=False, bg=WHITE)
            cell.border = THIN
        ws.row_dimensions[r].height = 18
    last = start + count - 1
    if dropdowns:
        for col, choices in dropdowns.items():
            letter = get_column_letter(col)
            dv = DataValidation(type="list", formula1='"' + ",".join(choices) + '"', allow_blank=True)
            dv.error = "Choose a value from the list."
            dv.errorTitle = "Use the list"
            dv.add(f"{letter}{start}:{letter}{last}")
            ws.add_data_validation(dv)
    widths_end = get_column_letter(cols)
    ws.auto_filter.ref = f"A{start - 1}:{widths_end}{last}"
    return last


def widths(ws, pairs):
    for letter, size in pairs.items():
        ws.column_dimensions[letter].width = size


_RATIO = {}


def ratio_rule(ws):
    dv = _RATIO.get(id(ws))
    if dv is None:
        dv = DataValidation(
            type="decimal", operator="between", formula1="0", formula2="1", allow_blank=True
        )
        dv.error = "Enter a number from 0 to 1. 0.80 means 80%."
        dv.errorTitle = "Use 0 to 1"
        ws.add_data_validation(dv)
        _RATIO[id(ws)] = dv
    return dv


def input_box(cell, value=None, fmt=None, hint=None):
    apply(cell, value, bg=INPUT, locked=False, fmt=fmt, align="right")
    cell.border = THIN
    if hint:
        cell.comment = Comment(hint, "On-Chain Operator Program", width=240, height=60)
        if "0 to 1" in hint.lower():
            ratio_rule(cell.parent).add(cell.coordinate)
    return cell


def calc_box(cell, formula, fmt=None):
    apply(cell, formula, bg=CALC, locked=True, fmt=fmt, align="right", bold=True)
    cell.border = THIN
    return cell


def label(cell, text, *, bold=False, color=INK):
    apply(cell, text, bold=bold, color=color, bg=WHITE, locked=True)
    return cell


def protect(ws):
    """Lock formula cells. Yellow inputs stay editable. No password.

    In the sheetProtection XML, 1 means the learner may do that action.
    """
    ws.protection.sheet = True
    ws.protection.selectLockedCells = True
    ws.protection.selectUnlockedCells = True
    ws.protection.insertRows = False
    ws.protection.insertColumns = False
    ws.protection.deleteRows = False
    ws.protection.deleteColumns = False
    ws.protection.formatCells = True
    ws.protection.autoFilter = True
    ws.protection.sort = True


def journal(wb, name, title, lesson, note, headers, rows=24, dropdowns=None, wide=None):
    ws = wb.create_sheet(name)
    banner(ws, title, lesson, note + "  " + SAFETY, len(headers))
    paint_header(ws, 4, headers)
    blank_rows(ws, 5, rows, len(headers), dropdowns)
    if wide:
        widths(ws, wide)
    else:
        for i in range(1, len(headers) + 1):
            ws.column_dimensions[get_column_letter(i)].width = 22
    ws.page_setup.orientation = "landscape"
    ws.print_title_rows = "1:4"
    ws.sheet_properties.tabColor = "14202B"
    protect(ws)
    return ws


CATALOG = []


def add_tool(ws, row, title, lesson, inputs, outputs):
    """inputs: (label, value, format, hint). outputs: (label, formula, format)."""
    CATALOG.append((title, row))
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=5)
    apply(ws.cell(row, 1), f"{title}   ·   {lesson}", bold=True, size=13, color=WHITE, bg=TEAL)
    ws.row_dimensions[row].height = 22
    row += 1
    n = max(len(inputs), len(outputs))
    for i in range(n):
        if i < len(inputs):
            lab, val, fmt, hint = inputs[i]
            label(ws.cell(row, 1), lab)
            input_box(ws.cell(row, 2), val, fmt, hint)
        if i < len(outputs):
            lab, formula, fmt = outputs[i]
            label(ws.cell(row, 4), lab, bold=True)
            calc_box(ws.cell(row, 5), formula, fmt)
        row += 1
    return row + 1


def build_start(wb):
    ws = wb.active
    ws.title = "Start"
    banner(
        ws,
        "On-Chain Operator worksheets",
        "Seventeen worksheets and the calculators they use",
        "Type in the yellow cells. Green cells are formulas, so leave them alone. "
        "Numbers already filled in on Tools are the lesson examples. They are for learning, not a forecast. "
        + SAFETY,
        4,
    )
    ws.row_dimensions[3].height = 48
    headers = ["Sheet", "Stage", "Lesson", "When you open it"]
    paint_header(ws, 5, headers)
    rows = [
        ("W1 Records", "0 · Zero", "0.3", "From the first action. One line each, and you keep the sheet."),
        ("W3 Due diligence", "3 · Analyst", "Module 6", "Before you use a protocol. Six checks, then a verdict."),
        ("W5 Portfolio", "4 · Strategist", "8.1", "When you set the buckets. Targets should add to 100%."),
        ("W4 Risk register", "4 · Strategist", "8.2", "When you score a risk. 20 or higher: do not hold it."),
        ("W2 Journal", "4 · Strategist", "8.4", "When a position is open. Thesis, kill rules, weekly result."),
        ("W12 Stress test", "4 · Strategist", "11.4", "Before you size the book up. Five named scenarios."),
        ("W13 Incident", "4 · Strategist", "11.5", "Before you need it. Channels and roles. No keys."),
        ("W6 Balance sheet", "5 · Operator", "12.1", "When you build the bank. Equity, LTV, health factor, runway."),
        ("W7 Custody", "5 · Operator", "12.2", "With the bank. Vault, operating wallet, hot float. No secrets."),
        ("W8 Credit policy", "5 · Operator", "12.3", "With the bank. The checks read the balance sheet."),
        ("W9 Liquidity", "5 · Operator", "12.4", "With the bank. Cash by how fast you can reach it."),
        ("W10 Lending", "5 · Operator", "12.5", "With the bank. Your assumed loss on each market."),
        ("W17 Letter", "5 · Operator", "12.6", "With the bank. Store it apart from any key."),
        ("W11 Income", "5 · Operator", "Module 13", "When you set a payout from expected income, not the headline."),
        ("W16 Annual review", "5 · Operator", "13.5", "Once a year. Equity, income, and whether the drill happened."),
        ("W14 Alerts", "5 · Operator", "14.1", "When you automate watching. A threshold and an action."),
        ("W15 Automation", "5 · Operator", "14.2", "When a bot can move funds. Write the cap and how you revoke it."),
        ("Tools", "Lessons 2–14", "Calculators", "Any time a lesson has a number. Yellow in, green answer."),
    ]
    for i, (sheet, stage, lesson, when) in enumerate(rows):
        r = 6 + i
        link = ws.cell(r, 1, sheet)
        apply(link, bold=True, color=TEAL, locked=True)
        link.hyperlink = Hyperlink(ref=f"A{r}", location=f"'{sheet}'!A1", tooltip=when)
        link.font = font(11, True, TEAL)
        apply(ws.cell(r, 2), stage, locked=True)
        apply(ws.cell(r, 3), lesson, locked=True)
        apply(ws.cell(r, 4), when, locked=True, wrap=True)
        for c in range(1, 5):
            ws.cell(r, c).border = THIN
            ws.cell(r, c).fill = fill(WHITE if i % 2 == 0 else PAPER)
        ws.row_dimensions[r].height = 22
    apply(ws.cell(26, 1), "How to open this file", bold=True, size=14, color=INK)
    notes = [
        "Excel, LibreOffice Calc, and Apple Numbers open the file directly.",
        "Google Sheets: File, Import, Upload, and choose this workbook.",
        "Yellow cells are yours. Green cells are the course formulas.",
        "The Tools sheet, the balance sheet, and the income sheet are prefilled with the lesson examples. Replace them with your own.",
        "Yellow cells are typed as the lesson writes them: 3.5 means 3.5%, and 0.80 means 80% where the label says 0 to 1.",
        "The health factor, the loop, the income payout, and the risk score update when you type. Print a sheet when you want paper. The formulas stay live in this file.",
        "Sheets are protected so a formula is not overwritten. There is no password. In Excel: Review, Unprotect Sheet.",
    ]
    for i, text in enumerate(notes):
        apply(ws.cell(27 + i, 1), text, locked=True, wrap=True)
        ws.merge_cells(start_row=27 + i, start_column=1, end_row=27 + i, end_column=4)
        ws.row_dimensions[27 + i].height = 20
    ws.auto_filter.ref = "A5:D23"
    widths(ws, {"A": 24, "B": 18, "C": 14, "D": 78})
    ws.freeze_panes = "A6"
    ws.page_setup.orientation = "landscape"
    ws.print_title_rows = "1:5"
    ws.sheet_properties.tabColor = INK
    protect(ws)


def build_tools(wb):
    CATALOG.clear()
    ws = wb.create_sheet("Tools", 1)
    banner(
        ws,
        "Calculators",
        "Lesson examples are already filled in. Change any yellow cell.",
        "Green answers use the course formulas. They are illustrations for learning, not a forecast and not a promise of a result. "
        + SAFETY,
        5,
    )
    ws.row_dimensions[3].height = 36
    apply(ws.cell(4, 1), "You type here", bold=True, color=INK, bg=INPUT, align="center")
    apply(ws.cell(4, 2), "Yellow input", color=MUTED, bg=INPUT)
    apply(ws.cell(4, 4), "The sheet answers", bold=True, color=TEAL, bg=CALC, align="center")
    apply(ws.cell(4, 5), "Green formula", color=TEAL, bg=CALC)
    widths(ws, {"A": 42, "B": 22, "C": 4, "D": 42, "E": 22})

    r = 6
    # Each block's first input is column B of (title_row + 1). Formulas use those addresses.
    # Health. Lesson 3.2: 10, 3000, 0.80, 12000 -> HF 2.00, liquidation 1500.
    b = r + 1
    r = add_tool(ws, r, "Health factor and liquidation price", "Lesson 3.2", [
        ("Collateral quantity", 10, "0.00", "How many units of collateral."),
        ("Collateral price", 3000, '"$"#,##0.00', "Price per unit."),
        ("Liquidation threshold (0 to 1)", 0.8, "0.00", "Use 0 to 1. 0.80 means 80%."),
        ("Debt", 12000, '"$"#,##0.00', "Amount borrowed."),
    ], [
        ("Collateral value", f"=B{b}*B{b+1}", '"$"#,##0.00'),
        ("LTV", f'=IF(B{b}*B{b+1}=0,"",B{b+3}/(B{b}*B{b+1}))', "0.0%"),
        ("Health factor", f'=IF(B{b+3}=0,"",B{b}*B{b+1}*B{b+2}/B{b+3})', "0.00"),
        ("Liquidation price", f'=IF(B{b}*B{b+2}=0,"",B{b+3}/(B{b}*B{b+2}))', '"$"#,##0.00'),
        ("Max debt for HF 2", f'=IF(B{b+2}=0,"",B{b}*B{b+1}*B{b+2}/2)', '"$"#,##0.00'),
        ("Check against 1.5", f'=IF(E{b+2}="","",IF(E{b+2}<1.5,"Below 1.5: repay or add collateral","At or above 1.5"))', None),
    ])

    # Loop. LTV 0.70, 3 loops, 3.5%, 2.5% -> 2.53x, net 5.03%, breakeven 5.78%.
    b = r + 1
    r = add_tool(ws, r, "Leveraged loop", "Lesson 3.4", [
        ("Borrow LTV (0 to 1)", 0.7, "0.00", "Use 0 to 1. Loan-to-value on each loop."),
        ("Loops", 3, "0", "How many times you borrow and deposit again."),
        ("Collateral APY", 3.5, '0.00"%"', "Yield on the collateral, in percentage points."),
        ("Borrow APY", 2.5, '0.00"%"', "Cost of the debt, in percentage points."),
    ], [
        ("Leverage", f'=IF(OR(B{b}<=0,B{b}>=1),"", (1-B{b}^(B{b+1}+1))/(1-B{b}))', '0.00"×"'),
        ("Net APY on equity", f'=IF(OR(B{b}<=0,B{b}>=1),"",B{b+2}*E{b}-B{b+3}*(E{b}-1))', '0.00"%"'),
        ("Breakeven borrow APY", f'=IF(OR(E{b}="",E{b}<=1),"",B{b+2}*E{b}/(E{b}-1))', '0.00"%"'),
        ("What the leverage did", f'=IF(E{b+1}="","",IF(E{b+1}<=B{b+2},"Adds nothing: the borrow rate is too high","Adds a spread over the unlevered yield"))', None),
    ])

    # IL at 2x is -5.72%.
    b = r + 1
    r = add_tool(ws, r, "Impermanent loss vs holding", "Lesson 2.4", [
        ("Price ratio (end ÷ start)", 2, "0.00", "2 means the price doubled. 0.5 means it halved."),
    ], [
        ("IL vs holding", f"=((2*SQRT(B{b})/(1+B{b}))-1)*100", '0.00"%"'),
    ])

    # LP breakeven: 2x over 90 days needs fee APR >= 23.19%.
    b = r + 1
    r = add_tool(ws, r, "LP fee breakeven", "Lesson 2.4", [
        ("Price ratio", 2, "0.00", "The move you want the fees to cover."),
        ("Days held", 90, "0", "How long the position is open."),
        ("Fee APR you expect", 20, '0.00"%"', "Optional. Leave blank to see only the fee rate required."),
    ], [
        ("IL over the period", f"=-( (2*SQRT(B{b})/(1+B{b}))-1 )*100", '0.00"%"'),
        ("Fee APR to match holding", f'=IF(B{b+1}=0,"",E{b}*365/B{b+1})', '0.00"%"'),
        ("Fees earned over the days", f'=IF(B{b+2}="","",B{b+2}*B{b+1}/365)', '0.00"%"'),
        ("Fees minus IL", f'=IF(B{b+2}="","",E{b+2}-E{b})', '0.00"%"'),
    ])

    # CL 1800-3000 ~ 8.3x
    b = r + 1
    r = add_tool(ws, r, "Concentrated liquidity efficiency", "Lesson 2.6", [
        ("Range low", 1800, '"$"#,##0.00', "Bottom of the range."),
        ("Range high", 3000, '"$"#,##0.00', "Top of the range."),
    ], [
        ("Geometric mid", f'=IF(OR(B{b}<=0,B{b+1}<=B{b}),"",SQRT(B{b}*B{b+1}))', '"$"#,##0.00'),
        ("Capital efficiency vs full range", f'=IF(OR(B{b}<=0,B{b+1}<=B{b}),"",1/(1-(B{b}/B{b+1})^0.25))', '0.0"×"'),
    ])

    # LVR vol 80 fee 12 -> 8.00% LVR, fees minus LVR +4.00
    b = r + 1
    r = add_tool(ws, r, "Loss versus rebalancing", "Lesson 2.7", [
        ("Volatility per year", 80, '0.00"%"', "Annualised volatility of the pair."),
        ("Fee APR", 12, '0.00"%"', "Fee APR you expect. Leave blank to see only LVR."),
    ], [
        ("LVR per year", f"=(B{b}/100)^2/8*100", '0.00"%"'),
        ("Fees minus LVR", f'=IF(B{b+1}="","",B{b+1}-E{b})', '0.00"%"'),
    ])

    # Supply 5% x 0.8 x 0.9 = 3.60%
    b = r + 1
    r = add_tool(ws, r, "Lending supply APY", "Lesson 4.2", [
        ("Borrow APY", 5, '0.00"%"', "What borrowers pay."),
        ("Utilisation (0 to 1)", 0.8, "0.00", "Use 0 to 1. Share of deposits that is lent out."),
        ("Reserve factor (0 to 1)", 0.1, "0.00", "Use 0 to 1. Share of interest the protocol keeps."),
    ], [
        ("Supply APY", f"=B{b}*B{b+1}*(1-B{b+2})", '0.00"%"'),
    ])

    # APY 12% n 365, position 10000, gas 2 -> 12.75% before gas, 5.45% after.
    b = r + 1
    r = add_tool(ws, r, "APR, APY, and gas", "Lesson 4.1", [
        ("APR", 12, '0.00"%"', "The stated rate, before compounding."),
        ("Compounds per year", 365, "0", "How often it compounds."),
        ("Position size", 10000, '"$"#,##0.00', "Optional. Used only for the gas drag."),
        ("Gas per compound", 2, '"$"#,##0.00', "Optional. What one compound costs."),
    ], [
        ("APY before gas", f'=IF(OR(B{b+1}<=0),"",( (1+B{b}/100/B{b+1})^B{b+1} - 1)*100)', '0.00"%"'),
        ("Gas drag", f'=IF(OR(B{b+2}="",B{b+2}=0,B{b+3}=""),"",B{b+3}*B{b+1}/B{b+2}*100)', '0.00"%"'),
        ("APY after gas", f'=IF(E{b+1}="","",E{b}-E{b+1})', '0.00"%"'),
    ])

    # Airdrop 0.3 * 1500 - 200 = 250
    b = r + 1
    r = add_tool(ws, r, "Airdrop expected value", "Lesson 4.6", [
        ("Probability (0 to 1)", 0.3, "0.00", "Use 0 to 1. Your estimate that it happens and you qualify."),
        ("Value if it happens", 1500, '"$"#,##0.00', "What you could sell it for, not the headline."),
        ("Costs", 200, '"$"#,##0.00', "Gas, bridges, and time you count as a cost."),
    ], [
        ("Expected value", f"=B{b}*B{b+1}-B{b+2}", '"$"#,##0.00'),
    ])

    # PT 0.95, 180 days -> 10.96%
    b = r + 1
    r = add_tool(ws, r, "Principal token fixed yield", "Lesson 10.1", [
        ("PT price (share of underlying)", 0.95, "0.00", "0.95 means you pay 0.95 for a claim on 1 at maturity."),
        ("Days to maturity", 180, "0", "Days left until redemption."),
    ], [
        ("Fixed APY if held", f'=IF(OR(B{b}<=0,B{b+1}=0),"",(B{b}^(-1))^(365/B{b+1})-1)', "0.00%"),
    ])

    # Basis 3000 / 3150 / 90 -> 5.00% and 20.28%
    b = r + 1
    r = add_tool(ws, r, "Cash-and-carry basis", "Lesson 10.3", [
        ("Spot price", 3000, '"$"#,##0.00', "Price of the asset today."),
        ("Futures price", 3150, '"$"#,##0.00', "Price of the dated future."),
        ("Days to expiry", 90, "0", "Days until the future expires."),
    ], [
        ("Basis", f'=IF(B{b}=0,"",B{b+1}/B{b}-1)', "0.00%"),
        ("Annualised, simple", f'=IF(B{b+2}=0,"",E{b}*365/B{b+2})', "0.00%"),
    ])

    # Covered call 3000, 3300, 1.5%, 7 days.
    b = r + 1
    r = add_tool(ws, r, "Covered call", "Lesson 10.4", [
        ("Spot price", 3000, '"$"#,##0.00', "Price of the asset you hold."),
        ("Strike", 3300, '"$"#,##0.00', "The cap you are willing to sell at."),
        ("Premium", 1.5, '0.00"%"', "Premium received, in percentage points of spot."),
        ("Days in the period", 7, "0", "Length of this option."),
    ], [
        ("Annualised if repeated", f'=IF(B{b+3}=0,"",B{b+2}*365/B{b+3})', '0.00"%"'),
        ("Max gain this period", f'=IF(B{b}=0,"",B{b+2}+(B{b+1}/B{b}-1)*100)', '0.00"%"'),
        ("Break-even price", f"=B{b}*(1-B{b+2}/100)", '"$"#,##0.00'),
    ])

    # Expected 12, 0.05, 0.6, 0.5 -> 8.50%
    b = r + 1
    r = add_tool(ws, r, "Risk-adjusted yield", "Lesson 13.2", [
        ("Headline yield", 12, '0.00"%"', "The advertised rate, in percentage points."),
        ("Loss probability (0 to 1)", 0.05, "0.00", "Use 0 to 1. Your assumed chance of a loss event this year."),
        ("Loss given default (0 to 1)", 0.6, "0.00", "Use 0 to 1. Share of the position lost if that event happens."),
        ("Other costs", 0.5, '0.00"%"', "Fees and gas, in percentage points."),
    ], [
        ("Expected loss", f"=B{b+1}*B{b+2}*100", '0.00"%"'),
        ("Risk-adjusted result", f"=B{b}-E{b}-B{b+3}", '0.00"%"'),
    ])

    # Income: 250000 at 5%, payout 0.7 -> 12500, 8750, 729.17, retain 3750.
    b = r + 1
    r = add_tool(ws, r, "Income and payout", "Module 13", [
        ("Position amount", 250000, '"$"#,##0.00', "Capital in the position."),
        ("Risk-adjusted yield", 5, '0.00"%"', "Yield after the expected-loss haircut."),
        ("Payout ratio (0 to 1)", 0.7, "0.00", "Use 0 to 1. Share of expected income you pay out."),
    ], [
        ("Expected income per year", f"=B{b}*B{b+1}/100", '"$"#,##0.00'),
        ("Payout per year", f"=E{b}*B{b+2}", '"$"#,##0.00'),
        ("Payout per month", f"=E{b+1}/12", '"$"#,##0.00'),
        ("Retained as a buffer", f"=E{b}-E{b+1}", '"$"#,##0.00'),
    ])

    # Bank. Lesson 12.1: 300000 collateral, 60000 debt at 5%, 40000 reserve, 5000 spend.
    b = r + 1
    r = add_tool(ws, r, "Balance sheet check", "Lesson 12.1", [
        ("Collateral", 300000, '"$"#,##0.00', "Collateral value."),
        ("Reserve", 40000, '"$"#,##0.00', "Cash you can reach quickly."),
        ("Other assets", 0, '"$"#,##0.00', "Anything else you count."),
        ("Debt", 60000, '"$"#,##0.00', "What you owe."),
        ("Borrow APY", 5, '0.00"%"', "Interest rate on the debt."),
        ("Monthly spending", 5000, '"$"#,##0.00', "Spending the reserve must also cover."),
        ("Liquidation threshold (0 to 1)", 0.8, "0.00", "Use 0 to 1. 0.80 means 80%."),
        ("Max LTV policy (0 to 1)", 0.3, "0.00", "Use 0 to 1. 0.30 means 30%."),
    ], [
        ("Equity", f"=B{b}+B{b+1}+B{b+2}-B{b+3}", '"$"#,##0.00'),
        ("LTV", f'=IF(B{b}=0,"",B{b+3}/B{b})', "0.0%"),
        ("Health factor", f'=IF(B{b+3}=0,"",B{b}*B{b+6}/B{b+3})', "0.00"),
        ("Reserve runway (months)", f'=IF((B{b+5}+B{b+3}*B{b+4}/100/12)=0,"",B{b+1}/(B{b+5}+B{b+3}*B{b+4}/100/12))', "0.0"),
        ("LTV within policy", f'=IF(E{b+1}="","",IF(E{b+1}<=B{b+7},"Yes","No"))', None),
        ("Health factor at least 2", f'=IF(E{b+2}="","",IF(E{b+2}>=2,"Yes","No"))', None),
        ("Reserve covers 6 months", f'=IF(E{b+3}="","",IF(E{b+3}>=6,"Yes","No"))', None),
    ])

    # Perp long 5x, 3000, mmr 0.5 -> 2415
    b = r + 1
    r = add_tool(ws, r, "Perp liquidation price", "Lesson 3.5", [
        ("Entry price", 3000, '"$"#,##0.00', "Price you entered at."),
        ("Leverage", 5, '0.0"×"', "Isolated leverage."),
        ("Side (1 long, -1 short)", 1, "0", "Type 1 for a long or -1 for a short."),
        ("Maintenance margin", 0.5, '0.00"%"', "Maintenance margin, in percentage points."),
    ], [
        ("Liquidation price", f'=IF(B{b+1}=0,"",B{b}*(1-B{b+2}*(1/B{b+1}-B{b+3}/100)))', '"$"#,##0.00'),
        ("Move to liquidation", f'=IF(B{b}=0,"",E{b}/B{b}-1)', "0.0%"),
    ])

    # TWR 4, -2, 3 -> 4.98%
    b = r + 1
    r = add_tool(ws, r, "Time-weighted return", "Lesson 8.5", [
        ("Period 1 return", 4, '0.00"%"', "First period, in percentage points. Negative is allowed."),
        ("Period 2 return", -2, '0.00"%"', "Second period."),
        ("Period 3 return", 3, '0.00"%"', "Third period. Leave later periods blank."),
        ("Period 4 return", None, '0.00"%"', "Optional."),
    ], [
        ("Time-weighted return", f'=(1+B{b}/100)*(1+B{b+1}/100)*(1+B{b+2}/100)*IF(B{b+3}="",1,1+B{b+3}/100)-1', "0.00%"),
    ])

    # CDP
    b = r + 1
    r = add_tool(ws, r, "CDP mint", "Lesson 3.7", [
        ("Collateral quantity", 10, "0.00", "Units of collateral."),
        ("Collateral price", 3000, '"$"#,##0.00', "Price per unit."),
        ("Stablecoins to mint", 10000, '"$"#,##0.00', "Amount you mint."),
        ("Minimum collateral ratio", 150, '0"%"', "150 means 150%."),
        ("Stability fee per year", 6, '0.00"%"', "Annual fee on the minted amount."),
    ], [
        ("Collateral value", f"=B{b}*B{b+1}", '"$"#,##0.00'),
        ("Maximum mint", f'=IF(B{b+3}=0,"",E{b}/(B{b+3}/100))', '"$"#,##0.00'),
        ("Collateral ratio", f'=IF(B{b+2}=0,"",E{b}/B{b+2})', "0%"),
        ("Liquidation price", f'=IF(B{b}=0,"",B{b+2}*(B{b+3}/100)/B{b})', '"$"#,##0.00'),
        ("Stability fee per year", f"=B{b+2}*B{b+4}/100", '"$"#,##0.00'),
    ])

    # Carry 0.01% / 8h, short 2x -> 10.95% APR, 7.30% on capital, +50% liquidation.
    b = r + 1
    r = add_tool(ws, r, "Funding carry", "Lesson 10.2", [
        ("Funding rate per 8 hours", 0.01, '0.00"%"', "The funding rate for one 8-hour period."),
        ("Short leverage", 2, '0.0"×"', "Leverage on the short leg."),
    ], [
        ("APR on the hedged size", f"=B{b}*3*365", '0.00"%"'),
        ("Return on total capital", f'=IF(B{b+1}=0,"",E{b}/(1+1/B{b+1}))', '0.00"%"'),
        ("Short liquidates near", f'=IF(B{b+1}=0,"",1/B{b+1})', "0%"),
    ])

    # VaR 100000, vol 70, z 1.65 -> about 6045.55
    b = r + 1
    add_tool(ws, r, "One-day value at risk", "Lesson 8.7", [
        ("Position", 100000, '"$"#,##0.00', "Size of the position."),
        ("Volatility per year", 70, '0.00"%"', "Annualised volatility."),
        ("Z score", 1.65, "0.00", "1.65 is about a 95% one-day estimate. 2.33 is about 99%."),
    ], [
        ("One-day VaR", f"=B{b+2}*(B{b+1}/100)/SQRT(365)*B{b}", '"$"#,##0.00'),
    ])

    ws.freeze_panes = "A5"
    ws.page_setup.orientation = "landscape"
    ws.print_title_rows = "1:4"
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.sheet_properties.tabColor = TEAL
    apply(ws.cell(4, 7), "Jump to a calculator", bold=True, size=12, color=WHITE, bg=INK, align="left")
    for i, (title, row) in enumerate(CATALOG):
        cell = ws.cell(5 + i, 7, title)
        apply(cell, bold=True, color=TEAL, locked=True)
        cell.hyperlink = Hyperlink(ref=f"G{5 + i}", location=f"'Tools'!A{row}", tooltip=title)
        cell.font = font(11, True, TEAL)
    ws.column_dimensions["G"].width = 38
    protect(ws)
    return ws


def build_w3(wb):
    ws = wb.create_sheet("W3 Due diligence")
    banner(ws, "W3 · Due-diligence file", "Module 6", "One protocol per copy of this sheet. " + SAFETY, 2)
    fields = [
        (5, "Protocol"),
        (6, "Chain"),
        (7, "TVL"),
        (8, "TVL source and date"),
        (9, "Risk rating (low, medium, high)"),
        (10, "Verdict (use, watch, pass)"),
        (12, "1 Mechanism"),
        (13, "2 Cash flow (organic vs subsidised)"),
        (14, "3 Dependencies"),
        (15, "4 Solvency"),
        (16, "5 Evidence (links)"),
        (17, "6 Exit"),
        (19, "Market cap"),
        (20, "Fully diluted value"),
        (21, "Unlocks in the next 12 months"),
        (22, "Value capture"),
        (24, "Voting concentration"),
        (25, "Timelock"),
        (27, "Holders"),
        (28, "Flows"),
        (29, "Activity"),
        (30, "Depth"),
        (31, "Derivatives"),
        (33, "Monitoring triggers"),
    ]
    for row, text in fields:
        label(ws.cell(row, 1), text, bold=True)
        input_box(ws.cell(row, 2), None)
        ws.row_dimensions[row].height = 22
    dv = DataValidation(type="list", formula1='"low,medium,high"', allow_blank=True)
    dv.add("B9")
    ws.add_data_validation(dv)
    dv2 = DataValidation(type="list", formula1='"use,watch,pass"', allow_blank=True)
    dv2.add("B10")
    ws.add_data_validation(dv2)
    widths(ws, {"A": 46, "B": 78})
    ws.freeze_panes = "A5"
    ws.sheet_properties.tabColor = "14202B"
    protect(ws)


def build_w4(wb):
    headers = ["Position", "Risk surface", "Description", "Likelihood 1–5", "Impact 1–5", "Score", "Response"]
    ws = journal(
        wb, "W4 Risk register", "W4 · Risk register", "Lesson 8.2",
        "Score is likelihood times impact. 15 or higher needs a mitigation or an exit. 20 or higher: do not hold it.",
        headers, rows=24,
        dropdowns={
            2: ["smart-contract", "economic", "oracle", "liquidity", "governance", "bridge/chain", "counterparty", "user-operation"],
        },
        wide={"A": 28, "B": 22, "C": 42, "D": 18, "E": 16, "F": 12, "G": 36},
    )
    whole = DataValidation(type="whole", operator="between", formula1="1", formula2="5", allow_blank=True)
    whole.error = "Enter a whole number from 1 to 5."
    whole.errorTitle = "Score from 1 to 5"
    whole.add("D5:E28")
    ws.add_data_validation(whole)
    for r in range(5, 29):
        calc_box(ws.cell(r, 6), f'=IF(OR(D{r}="",E{r}=""),"",D{r}*E{r})', "0")
    amber = PatternFill("solid", fgColor="F8EFEA")
    red = PatternFill("solid", fgColor="F4D6CC")
    ws.conditional_formatting.add("F5:F28", CellIsRule(operator="greaterThanOrEqual", formula=["20"], fill=red))
    ws.conditional_formatting.add("F5:F28", CellIsRule(operator="between", formula=["15", "19"], fill=amber))
    examples = [
        ("Example: looped ETH", "economic", "Borrow rate rises above the collateral yield. Replace this row.", 4, 5, "Do not hold it until the response is real."),
        ("Example: stablecoin pool", "smart-contract", "A bug drains the pool. Replace this row.", 3, 5, "Write the mitigation before you size it."),
    ]
    for i, (position, surface, desc, likelihood, impact, response) in enumerate(examples):
        r = 5 + i
        for col, value in enumerate((position, surface, desc, likelihood, impact, None, response), 1):
            if col == 6:
                continue
            ws.cell(r, col).value = value
    protect(ws)


def build_w5(wb):
    ws = wb.create_sheet("W5 Portfolio")
    banner(ws, "W5 · Portfolio plan", "Lesson 8.1",
           "Targets should add to 100%. Caps are the most you will put in one protocol, chain, issuer, or bridge. " + SAFETY, 5)
    headers = ["Bucket", "Target %", "Current %", "Holdings", "Caps (protocol / chain / issuer / bridge)"]
    paint_header(ws, 4, headers)
    blank_rows(ws, 5, 12, 5)
    for r in range(5, 17):
        ws.cell(r, 2).number_format = '0.0"%"'
        ws.cell(r, 3).number_format = '0.0"%"'
    label(ws.cell(18, 1), "Target total", bold=True)
    calc_box(ws.cell(18, 2), "=SUM(B5:B16)", '0.0"%"')
    label(ws.cell(19, 1), "Current total", bold=True)
    calc_box(ws.cell(19, 3), "=SUM(C5:C16)", '0.0"%"')
    label(ws.cell(20, 1), "Target check", bold=True)
    calc_box(ws.cell(20, 2), '=IF(COUNT(B5:B16)=0,"",IF(ABS(B18-100)<0.1,"Adds to 100%","Does not add to 100%"))')
    label(ws.cell(22, 1), "Rebalance rule", bold=True)
    input_box(ws.cell(22, 2))
    ws.merge_cells("B22:E22")
    widths(ws, {"A": 28, "B": 16, "C": 16, "D": 36, "E": 48})
    ws.sheet_properties.tabColor = "14202B"
    protect(ws)


def build_w6(wb):
    ws = wb.create_sheet("W6 Balance sheet")
    banner(ws, "W6 · Balance sheet", "Lesson 12.1",
           "The numbers already here are the lesson example: $300,000 collateral, $60,000 debt, $40,000 reserve. "
           "LTV, the health factor, and interest use loans plus margin. Yield positions sit in equity only. " + SAFETY, 2)
    rows = [
        (5, "Collateral", 300000, '"$"#,##0.00', "Lesson example. Market value of collateral."),
        (6, "Yield positions", 0, '"$"#,##0.00', None),
        (7, "Reserve (cash you can reach)", 40000, '"$"#,##0.00', "Cash you can use without selling a position."),
        (8, "Other assets", 0, '"$"#,##0.00', None),
        (10, "Loans", 60000, '"$"#,##0.00', "Lesson example."),
        (11, "Margin", 0, '"$"#,##0.00', None),
        (12, "Other liabilities", 0, '"$"#,##0.00', None),
        (14, "Liquidation threshold (0 to 1)", 0.8, "0.00", "Use 0 to 1. 0.80 means 80%."),
        (15, "Borrow APY", 5, '0.00"%"', "5 means 5%."),
        (16, "Monthly spending", 5000, '"$"#,##0.00', "Spending the reserve must also cover."),
    ]
    for row, text, value, fmt, hint in rows:
        label(ws.cell(row, 1), text, bold=True)
        input_box(ws.cell(row, 2), value, fmt, hint)
    label(ws.cell(18, 1), "Total assets", bold=True)
    calc_box(ws.cell(18, 2), "=B5+B6+B7+B8", '"$"#,##0.00')
    label(ws.cell(19, 1), "Total liabilities", bold=True)
    calc_box(ws.cell(19, 2), "=B10+B11+B12", '"$"#,##0.00')
    label(ws.cell(20, 1), "Equity", bold=True)
    calc_box(ws.cell(20, 2), "=B18-B19", '"$"#,##0.00')
    label(ws.cell(21, 1), "LTV (loans + margin ÷ collateral)", bold=True)
    calc_box(ws.cell(21, 2), '=IF(B5=0,"",(B10+B11)/B5)', "0.0%")
    label(ws.cell(22, 1), "Health factor on collateral", bold=True)
    calc_box(ws.cell(22, 2), '=IF(OR((B10+B11)=0,B14=""),"",B5*B14/(B10+B11))', "0.00")
    label(ws.cell(23, 1), "Monthly interest on loans and margin", bold=True)
    calc_box(ws.cell(23, 2), '=IF(B15="","",(B10+B11)*B15/100/12)', '"$"#,##0.00')
    label(ws.cell(24, 1), "Reserve runway (months)", bold=True)
    calc_box(ws.cell(24, 2), '=IF((B16+B23)=0,"",B7/(B16+B23))', "0.0")
    ws.row_dimensions[3].height = 48
    ws.conditional_formatting.add(
        "B22",
        FormulaRule(formula=["AND(ISNUMBER(B22),B22<1.5)"], fill=fill("F4D6CC")),
    )
    apply(
        ws.cell(26, 1),
        "Yield positions are inside equity. They are not treated as collateral on this sheet.",
        color=MUTED, italic=True, locked=True,
    )
    ws.merge_cells("A26:B26")
    widths(ws, {"A": 48, "B": 22})
    ws.freeze_panes = "A5"
    ws.sheet_properties.tabColor = "14202B"
    protect(ws)


def build_w7(wb):
    ws = wb.create_sheet("W7 Custody")
    banner(ws, "W7 · Custody policy", "Lesson 12.2",
           "Describe roles and wallet types. Do not write where a seed phrase is, and do not write the phrase. " + SAFETY, 2)
    fields = [
        (5, "Vault type (for example 2 of 3 multisig)"),
        (6, "Key holders, by role"),
        (7, "Allowlisted destinations, described generally"),
        (8, "Timelock"),
        (10, "Operating wallet type"),
        (11, "Daily limit"),
        (12, "Protocols the operating wallet may use"),
        (14, "Hot float size"),
        (15, "Refill schedule"),
    ]
    for row, text in fields:
        label(ws.cell(row, 1), text, bold=True)
        input_box(ws.cell(row, 2))
        ws.row_dimensions[row].height = 22
    paint_header(ws, 17, ["Date", "Recovery path tested (no secrets)", "Result"])
    blank_rows(ws, 18, 8, 3)
    widths(ws, {"A": 52, "B": 55, "C": 28})
    ws.freeze_panes = "A5"
    ws.sheet_properties.tabColor = "14202B"
    protect(ws)


def build_w8(wb):
    ws = wb.create_sheet("W8 Credit policy")
    banner(ws, "W8 · Credit policy", "Lesson 12.3",
           "The checks read the balance sheet on W6. Fill that sheet first. " + SAFETY, 2)
    fields = [
        (5, "Max LTV (0 to 1)", 0.3, "0.00", "Use 0 to 1. 0.30 means 30%, the lesson cap. Compared with W6 LTV."),
        (6, "Health-factor floor", 2, "0.00", "The lesson floor is 2."),
        (7, "Alert level 1", None, "0.00", None),
        (8, "Action at alert 1", None, None, None),
        (9, "Alert level 2", None, "0.00", None),
        (10, "Action at alert 2", None, None, None),
        (11, "Fixed or variable, and why", None, None, None),
        (12, "Repayment source", None, None, None),
        (13, "Collateral you allow", None, None, None),
    ]
    for row, text, value, fmt, hint in fields:
        label(ws.cell(row, 1), text, bold=True)
        input_box(ws.cell(row, 2), value, fmt, hint)
    label(ws.cell(15, 1), "W6 LTV is within this cap", bold=True)
    calc_box(ws.cell(15, 2), '=IF(OR(B5="",\'W6 Balance sheet\'!B21=""),"",IF(\'W6 Balance sheet\'!B21<=B5,"Yes","No"))')
    label(ws.cell(16, 1), "W6 health factor is at or above the floor", bold=True)
    calc_box(ws.cell(16, 2), '=IF(OR(B6="",\'W6 Balance sheet\'!B22=""),"",IF(\'W6 Balance sheet\'!B22>=B6,"Yes","No"))')
    widths(ws, {"A": 56, "B": 42})
    ws.freeze_panes = "A5"
    ws.sheet_properties.tabColor = "14202B"
    protect(ws)


def build_w9(wb):
    ws = wb.create_sheet("W9 Liquidity")
    banner(ws, "W9 · Liquidity ladder", "Lesson 12.4",
           "Target and current are in months of obligations. The gap is target minus current. " + SAFETY, 6)
    headers = ["Tier", "Access", "Holds", "Target (months)", "Current (months)", "Gap (above 0 is short)"]
    paint_header(ws, 4, headers)
    preset = [("T0", "Seconds"), ("T1", "Hours"), ("T2", "Scheduled"), ("T3", "Days–weeks")]
    for i, (tier, access) in enumerate(preset):
        r = 5 + i
        apply(ws.cell(r, 1), tier, bold=True, locked=True, bg=PAPER)
        ws.cell(r, 1).border = THIN
        apply(ws.cell(r, 2), access, locked=True, bg=PAPER)
        ws.cell(r, 2).border = THIN
        input_box(ws.cell(r, 3))
        input_box(ws.cell(r, 4), None, "0.0")
        input_box(ws.cell(r, 5), None, "0.0")
        calc_box(ws.cell(r, 6), f'=IF(OR(D{r}="",E{r}=""),"",D{r}-E{r})', "0.0")
    ws.conditional_formatting.add("F5:F8", CellIsRule(operator="greaterThan", formula=["0"], fill=fill(WARN)))
    label(ws.cell(10, 1), "Refill rule", bold=True)
    input_box(ws.cell(10, 3))
    ws.merge_cells("C10:F10")
    widths(ws, {"A": 14, "B": 18, "C": 36, "D": 20, "E": 20, "F": 24})
    ws.freeze_panes = "A5"
    ws.sheet_properties.tabColor = "14202B"
    protect(ws)


def build_w10(wb):
    headers = ["Market or vault", "Collateral", "Oracle", "Liquidation LTV (0–1)", "Curator", "Loss probability (0–1)", "LGD (0–1)", "Expected loss", "Cap"]
    ws = journal(
        wb, "W10 Lending", "W10 · Lending policy", "Lesson 12.5",
        "Expected loss is your assumed probability times the share you would lose. It is an assumption you type, not a forecast.",
        headers, rows=12,
        wide={"A": 28, "B": 22, "C": 22, "D": 18, "E": 18, "F": 24, "G": 14, "H": 16, "I": 14},
    )
    for r in range(5, 17):
        ws.cell(r, 4).number_format = "0.00"
        ws.cell(r, 6).number_format = "0.00"
        ws.cell(r, 7).number_format = "0.00"
        ws.cell(r, 9).number_format = '"$"#,##0'
        calc_box(ws.cell(r, 8), f'=IF(OR(F{r}="",G{r}=""),"",F{r}*G{r})', "0.0%")
    ratio_rule(ws).add("F5:G16")
    protect(ws)


def build_w11(wb):
    ws = wb.create_sheet("W11 Income")
    banner(ws, "W11 · Income portfolio and payout", "Module 13",
           "Rows already filled in are the Lesson 13.3 example ($500,000, five positions, 70% payout). Replace them with yours. "
           "Net yield is the headline minus probability times loss given default. " + SAFETY, 7)
    headers = ["Position", "Amount", "Yield %", "Loss probability (0–1)", "LGD (0–1)", "Net yield", "Income per year"]
    paint_header(ws, 4, headers)
    ws.row_dimensions[3].height = 48
    blank_rows(ws, 5, 10, 7)
    for r in range(5, 15):
        ws.cell(r, 2).number_format = '"$"#,##0.00'
        ws.cell(r, 3).number_format = '0.00"%"'
        ws.cell(r, 4).number_format = "0.00"
        ws.cell(r, 5).number_format = "0.00"
        calc_box(ws.cell(r, 6), f'=IF(C{r}="","",C{r}-D{r}*E{r}*100)', '0.00"%"')
        calc_box(ws.cell(r, 7), f'=IF(OR(B{r}="",F{r}=""),"",B{r}*F{r}/100)', '"$"#,##0.00')
    examples = [
        ("Stable lending A", 100000, 5, 0.005, 1),
        ("Stable lending B", 100000, 4.5, 0.005, 1),
        ("LST staking", 150000, 3.2, 0.01, 0.5),
        ("PT fixed stable", 100000, 8, 0.02, 0.5),
        ("Funding carry", 50000, 9, 0.05, 0.3),
    ]
    for i, values in enumerate(examples):
        r = 5 + i
        for col, value in enumerate(values, 1):
            ws.cell(r, col).value = value
    ws.cell(20, 2).value = 0.7
    label(ws.cell(16, 1), "Capital", bold=True)
    calc_box(ws.cell(16, 2), "=SUM(B5:B14)", '"$"#,##0.00')
    label(ws.cell(17, 1), "Expected income per year", bold=True)
    calc_box(ws.cell(17, 7), "=SUM(G5:G14)", '"$"#,##0.00')
    label(ws.cell(18, 1), "Blended risk-adjusted yield", bold=True)
    calc_box(ws.cell(18, 6), '=IF(B16=0,"",G17/B16*100)', '0.00"%"')
    label(ws.cell(20, 1), "Payout ratio (0 to 1)", bold=True)
    input_box(ws.cell(20, 2), None, "0.00", "Use 0 to 1. 0.70 means you pay out 70% of expected income.")
    ratio_rule(ws).add("D5:E14")
    label(ws.cell(21, 1), "Payout per year", bold=True)
    calc_box(ws.cell(21, 2), '=IF(B20="","",G17*B20)', '"$"#,##0.00')
    label(ws.cell(22, 1), "Payout per month", bold=True)
    calc_box(ws.cell(22, 2), '=IF(B21="","",B21/12)', '"$"#,##0.00')
    label(ws.cell(23, 1), "Retained as a buffer", bold=True)
    calc_box(ws.cell(23, 2), '=IF(B21="","",G17-B21)', '"$"#,##0.00')
    label(ws.cell(25, 1), "Review rule", bold=True)
    input_box(ws.cell(25, 2))
    ws.merge_cells("B25:G25")
    widths(ws, {"A": 32, "B": 18, "C": 14, "D": 26, "E": 14, "F": 16, "G": 20})
    ws.sheet_properties.tabColor = "14202B"
    protect(ws)


def build_w12(wb):
    ws = wb.create_sheet("W12 Stress test")
    banner(ws, "W12 · Stress test", "Lesson 11.4",
           "The five scenarios are the lesson's set. Fill the loss and the fix before you need them. " + SAFETY, 6)
    headers = ["Scenario", "Loss", "Liquidations?", "Liquidity OK?", "Payout OK?", "Fix"]
    paint_header(ws, 4, headers)
    scenarios = ["Crypto −50%", "Stablecoin −10%", "Borrow rate 20%", "Largest protocol hacked", "Main L2 halted 48h"]
    for i, name in enumerate(scenarios):
        r = 5 + i
        apply(ws.cell(r, 1), name, bold=True, locked=True, bg=PAPER)
        ws.cell(r, 1).border = THIN
        for c in range(2, 7):
            input_box(ws.cell(r, c))
        ws.cell(r, 2).number_format = '"$"#,##0'
    yn = DataValidation(type="list", formula1='"Yes,No"', allow_blank=True)
    yn.add("C5:E9")
    ws.add_data_validation(yn)
    label(ws.cell(11, 1), "Portfolio value, for an illustration", bold=True)
    input_box(ws.cell(11, 2), None, '"$"#,##0')
    label(ws.cell(12, 1), "Shock, in percentage points", bold=True)
    input_box(ws.cell(12, 2), None, '0.0"%"', "50 means a 50% move. An illustration, not a forecast.")
    label(ws.cell(13, 1), "Illustrative dollar loss", bold=True)
    calc_box(ws.cell(13, 2), '=IF(OR(B11="",B12=""),"",B11*B12/100)', '"$"#,##0')
    apply(ws.cell(14, 1), "Put that dollar figure in the Loss column as a starting point, then write the fix.", color=MUTED, italic=True, locked=True)
    ws.merge_cells("A14:F14")
    widths(ws, {"A": 42, "B": 18, "C": 16, "D": 16, "E": 16, "F": 42})
    ws.freeze_panes = "A5"
    ws.sheet_properties.tabColor = "14202B"
    protect(ws)


def build_w16(wb):
    ws = wb.create_sheet("W16 Annual review")
    banner(ws, "W16 · Annual review", "Lesson 13.5", SAFETY, 4)
    singles = [
        (5, "Equity at the start", '"$"#,##0.00'),
        (6, "Equity at the end", '"$"#,##0.00'),
        (8, "LTV at the review", '0.0"%"'),
        (9, "Runway at the review (months)", "0.0"),
        (10, "Payout paid", '"$"#,##0.00'),
        (11, "Payout the policy allowed", '"$"#,##0.00'),
    ]
    for row, text, fmt in singles:
        label(ws.cell(row, 1), text, bold=True)
        input_box(ws.cell(row, 2), None, fmt)
    label(ws.cell(7, 1), "Change in equity", bold=True)
    calc_box(ws.cell(7, 2), '=IF(OR(B5="",B6=""),"",B6-B5)', '"$"#,##0.00')
    label(ws.cell(12, 1), "Payout versus policy", bold=True)
    calc_box(ws.cell(12, 2), '=IF(OR(B10="",B11=""),"",B10-B11)', '"$"#,##0.00')
    paint_header(ws, 14, ["Source", "Income expected", "Income realised", "Gap"])
    blank_rows(ws, 15, 6, 4)
    for r in range(15, 21):
        ws.cell(r, 2).number_format = '"$"#,##0.00'
        ws.cell(r, 3).number_format = '"$"#,##0.00'
        calc_box(ws.cell(r, 4), f'=IF(OR(B{r}="",C{r}=""),"",C{r}-B{r})', '"$"#,##0.00')
    label(ws.cell(22, 1), "Losses and near-misses", bold=True)
    input_box(ws.cell(22, 2))
    ws.merge_cells("B22:D22")
    label(ws.cell(23, 1), "Updated loss assumptions", bold=True)
    input_box(ws.cell(23, 2))
    ws.merge_cells("B23:D23")
    label(ws.cell(24, 1), "Custody and succession drill done?", bold=True)
    input_box(ws.cell(24, 2))
    dv = DataValidation(type="list", formula1='"Yes,No"', allow_blank=True)
    dv.add("B24")
    ws.add_data_validation(dv)
    widths(ws, {"A": 42, "B": 22, "C": 22, "D": 18})
    ws.freeze_panes = "A5"
    ws.sheet_properties.tabColor = "14202B"
    protect(ws)


def build_w17(wb):
    ws = wb.create_sheet("W17 Letter")
    banner(
        ws,
        "W17 · Letter of instruction",
        "Lesson 12.6 · store this apart from any key",
        "Describe what exists and who has a role. Do not write a seed phrase, a private key, an API key, a password, or where a seed is hidden. " + SAFETY,
        2,
    )
    ws.row_dimensions[3].height = 48
    fields = [
        (5, "Wallet types that exist (hardware, multisig, hot). Not the keys."),
        (6, "Multisig shape (for example 2 of 3) and the roles, not the people\'s secrets."),
        (7, "Where the documents are (this file, the journal, the due-diligence notes)."),
        (8, "Co-signer or professional, by name and role."),
        (9, "How the executor should proceed, in order."),
        (10, "Who to call first."),
        (11, "What not to do."),
    ]
    for row, text in fields:
        label(ws.cell(row, 1), text, bold=True)
        input_box(ws.cell(row, 2))
        ws.row_dimensions[row].height = 36
    widths(ws, {"A": 72, "B": 55})
    ws.freeze_panes = "A5"
    ws.sheet_properties.tabColor = AMBER
    protect(ws)


def build():
    wb = Workbook()
    build_start(wb)
    build_tools(wb)
    w1 = journal(
        wb, "W1 Records", "W1 · Records sheet", "Lesson 0.3 · keep this",
        "One line per action. This is the record you keep.",
        ["Date", "Action", "Asset", "Amount", "Price (USD)", "Fee", "Network", "Tx link", "Notes"],
        rows=40,
        dropdowns={2: ["buy", "sell", "transfer", "swap", "fee", "income"]},
        wide={"A": 14, "B": 14, "C": 14, "D": 14, "E": 14, "F": 12, "G": 16, "H": 28, "I": 28},
    )
    for r in range(5, 45):
        w1.cell(r, 1).number_format = "yyyy-mm-dd"
        w1.cell(r, 4).number_format = "#,##0.00"
        w1.cell(r, 5).number_format = '"$"#,##0.00'
        w1.cell(r, 6).number_format = '"$"#,##0.00'
    label(w1.cell(46, 1), "Lines with a date", bold=True)
    calc_box(w1.cell(46, 2), "=COUNTA(A5:A44)", "0")
    label(w1.cell(47, 1), "Fees recorded", bold=True)
    calc_box(w1.cell(47, 2), "=SUM(F5:F44)", '"$"#,##0.00')
    journal(
        wb, "W2 Journal", "W2 · Position journal", "Lesson 8.4",
        "One row per position. Kill rules are numbers you will act on.",
        ["Position", "Protocol / chain", "Contracts", "Amount", "Entry date/price", "Profit engine", "Thesis", "Kill rules", "Approvals", "Weekly result"],
        rows=20,
        wide={"A": 22, "B": 22, "C": 22, "D": 14, "E": 20, "F": 20, "G": 28, "H": 28, "I": 22, "J": 22},
    )
    build_w3(wb)
    build_w4(wb)
    build_w5(wb)
    build_w6(wb)
    build_w7(wb)
    build_w8(wb)
    build_w9(wb)
    build_w10(wb)
    build_w11(wb)
    build_w12(wb)
    journal(
        wb, "W13 Incident", "W13 · Incident playbook", "Lesson 11.5",
        "Write the official channel you bookmarked, the containment step, and a role to contact. No keys.",
        ["Incident type", "Official channel (bookmarked)", "Containment steps", "Fresh-wallet procedure", "Who to contact (role)", "Journal note"],
        rows=10,
        wide={"A": 28, "B": 36, "C": 36, "D": 28, "E": 26, "F": 28},
    )
    journal(
        wb, "W14 Alerts", "W14 · Alert sheet", "Lesson 14.1",
        "A threshold without an action is not an alert.",
        ["Alert", "Threshold", "Tool", "Action"],
        rows=16,
        wide={"A": 32, "B": 22, "C": 22, "D": 42},
    )
    journal(
        wb, "W15 Automation", "W15 · Automation permissions", "Lesson 14.2",
        "Cap what a bot can move, and write how you revoke it.",
        ["Bot or automation", "Permission", "Contract", "Cap", "Expiry", "Revoke method"],
        rows=12,
        wide={"A": 28, "B": 28, "C": 28, "D": 16, "E": 16, "F": 28},
    )
    build_w16(wb)
    build_w17(wb)
    wb.properties.title = "On-Chain Operator Worksheets"
    wb.properties.subject = "Educational worksheets and calculators. Not financial advice."
    wb.properties.creator = "On-Chain Operator Program"
    wb.calculation.calcMode = "auto"
    wb.calculation.fullCalcOnLoad = True
    OUT.parent.mkdir(parents=True, exist_ok=True)
    wb.save(OUT)
    return OUT


if __name__ == "__main__":
    path = build()
    print(f"wrote {path} ({path.stat().st_size} bytes)")
