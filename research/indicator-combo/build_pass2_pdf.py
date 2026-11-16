"""Rebuild the guide from the second-pass result files.

Numbers are formatted from the JSON and then checked against the PDF text.
Cells with fewer than 20 deployments are marked not meaningful.
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from reportlab.lib.colors import HexColor, white
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, ListFlowable, ListItem

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "results"
CHARTS = ROOT / "charts"
CHARTS.mkdir(exist_ok=True)
PDF = ROOT / "GridBot_Master_Strategy_Guide.pdf"
NAVY = "#0A1628"
CYAN = "#00D4FF"
DISCLAIMER = "Past performance is not a reliable indicator of future results."
EDU = "Education only. Not financial advice. Hypothetical backtest, not a forecast."


def pct(x, d=1):
    if x is None:
        return "—"
    return f"{100.0 * float(x):.{d}f}%"


def load():
    return {
        "summary": json.loads((OUT / "pass2_summary.json").read_text()),
        "oos": json.loads((OUT / "pass2_oos.json").read_text()),
        "is_": json.loads((OUT / "pass2_is.json").read_text()),
        "before": json.loads((OUT / "pass2_before.json").read_text()),
        "variants": json.loads((OUT / "pass2_variants.json").read_text()),
        "equity": json.loads((OUT / "pass2_equity.json").read_text()),
    }


def find(rows, **kw):
    for r in rows:
        if all(r.get(k) == v for k, v in kw.items()):
            return r
    raise KeyError(kw)


def cell_win(r):
    n = 0 if r is None else r.get("n") or 0
    if r is None or r.get("win") is None or n < 20:
        return f"n={n} not meaningful"
    return f"{pct(r['win'])} ({pct(r['ci_lo'])}–{pct(r['ci_hi'])}) n={n}"


def style_ax(ax, title):
    ax.set_facecolor("#0E1C2F")
    ax.figure.patch.set_facecolor(NAVY)
    ax.set_title(title, color="white", loc="left", fontsize=11)
    ax.tick_params(colors="white", labelsize=8)
    for sp in ax.spines.values():
        sp.set_color("#1E3A55")
    ax.grid(True, color="#1E3A55", lw=0.4)


def save(fig, name):
    fig.text(0.01, 0.01, DISCLAIMER, color="#9FB3C8", fontsize=8)
    path = CHARTS / name
    fig.tight_layout(rect=(0, 0.05, 1, 1))
    fig.savefig(path, dpi=140)
    plt.close(fig)
    return path


def chart_equity(equity):
    fig, ax = plt.subplots(figsize=(10.2, 4.2))
    style_ax(ax, "Out-of-sample bot equity, BTC 4h, locked static rules, 10,000 budget")
    for mode, color in (("Arithmetic", CYAN), ("Geometric", "#7AA2FF")):
        key = f"{mode}|BTC-USDT|4h"
        if key not in equity:
            continue
        eq = np.array(equity[key]["equity"], dtype=float)
        ax.plot(np.arange(len(eq)), eq, color=color, lw=1.3, label=mode)
    ax.axhline(10000, color="#9FB3C8", lw=0.6)
    ax.set_ylabel("Bot equity", color="white")
    ax.set_xlabel("4h bars from 16 May 2026", color="white")
    ax.legend(facecolor=NAVY, edgecolor="#1E3A55", labelcolor="white")
    return save(fig, "pass2_btc_equity.png")


def chart_wins(oos):
    fig, ax = plt.subplots(figsize=(10.2, 4.4))
    style_ax(ax, "Out-of-sample deployment win rate, 4h, cells with n≥20 only")
    coins = ["BTC-USDT", "ETH-USDT", "SOL-USDT", "ZEC-USDT", "XRP-USDT", "LINK-USDT"]
    x = np.arange(len(coins))
    for offset, mode, color in ((-0.18, "Arithmetic", CYAN), (0.18, "Geometric", "#7AA2FF")):
        vals, yerr_lo, yerr_hi = [], [], []
        for c in coins:
            r = find(oos, mode=mode, inst=c, tf="4h", label="locked")
            if not r["meaningful"] or r["win"] is None:
                vals.append(0.0)
                yerr_lo.append(0.0)
                yerr_hi.append(0.0)
            else:
                vals.append(100 * r["win"])
                yerr_lo.append(100 * (r["win"] - (r["ci_lo"] or r["win"])))
                yerr_hi.append(100 * ((r["ci_hi"] or r["win"]) - r["win"]))
        ax.bar(x + offset, vals, width=0.36, color=color, label=mode,
               yerr=np.vstack([yerr_lo, yerr_hi]), ecolor="white", capsize=2)
    ax.axhline(75, color="#F5C16C", ls="--", lw=1, label="75% target")
    ax.text(0.0, -12, "Bars at zero are n<20 and are not a result.", color="#9FB3C8", fontsize=8)
    ax.set_xticks(x)
    ax.set_xticklabels([c.split("-")[0] for c in coins], color="white")
    ax.set_ylim(0, 100)
    ax.set_ylabel("Win rate, %", color="white")
    ax.legend(facecolor=NAVY, edgecolor="#1E3A55", labelcolor="white", fontsize=8)
    return save(fig, "pass2_win_4h.png")


def pooled(rows):
    # Recompute from cell wins and n so the headline matches the file.
    n = sum(r["n"] for r in rows)
    wins = sum(r["wins"] for r in rows)
    meaningful = [r for r in rows if r["meaningful"] and r["mean_ret"] is not None]
    # deployment-weighted return uses n * mean_ret
    num = sum(r["n"] * r["mean_ret"] for r in rows if r["mean_ret"] is not None and r["n"])
    den = sum(r["n"] for r in rows if r["mean_ret"] is not None and r["n"])
    return {
        "n": n,
        "win": (wins / n) if n else None,
        "ret": (num / den) if den else None,
        "meaningful_n": sum(r["n"] for r in meaningful),
    }


def header_footer(canvas, doc):
    canvas.saveState()
    w, h = landscape(A4)
    canvas.setFillColor(HexColor(NAVY))
    canvas.rect(0, h - 14 * mm, w, 14 * mm, fill=1, stroke=0)
    canvas.rect(0, 0, w, 12 * mm, fill=1, stroke=0)
    canvas.setFillColor(HexColor(CYAN))
    canvas.setFont("Helvetica-Bold", 11)
    canvas.drawString(14 * mm, h - 9 * mm, "GridBot Builder")
    canvas.setFillColor(white)
    canvas.setFont("Helvetica", 9)
    canvas.drawRightString(w - 14 * mm, h - 9 * mm, "Master Strategy guide  ·  education only")
    canvas.setFillColor(HexColor(CYAN))
    canvas.setFont("Helvetica", 8)
    canvas.drawString(14 * mm, 5 * mm, EDU)
    canvas.setFillColor(white)
    canvas.drawRightString(w - 14 * mm, 5 * mm, str(doc.page))
    canvas.restoreState()


def table(rows, widths):
    body = ParagraphStyle("b", fontName="Helvetica", fontSize=7, leading=9, textColor=HexColor("#102033"))
    head = ParagraphStyle("h", fontName="Helvetica-Bold", fontSize=7, leading=9, textColor=white)
    built = []
    for i, row in enumerate(rows):
        st = head if i == 0 else body
        built.append([Paragraph(str(x), st) for x in row])
    tbl = Table(built, colWidths=widths, repeatRows=1)
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), HexColor(NAVY)),
        ("BACKGROUND", (0, 1), (-1, -1), HexColor("#F4F7FB")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [HexColor("#F4F7FB"), white]),
        ("GRID", (0, 0), (-1, -1), 0.2, HexColor("#D5DEE8")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 2),
        ("RIGHTPADDING", (0, 0), (-1, -1), 2),
        ("TOPPADDING", (0, 0), (-1, -1), 1),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
    ]))
    return tbl


def build():
    from pdf_gate import assert_pdf_allowed
    assert_pdf_allowed()
    data = load()
    s = data["summary"]
    charts = [chart_equity(data["equity"]), chart_wins(data["oos"])]
    styles = getSampleStyleSheet()
    title = ParagraphStyle("title", parent=styles["Title"], textColor=HexColor(NAVY), fontName="Helvetica-Bold", fontSize=20, leading=24)
    h = ParagraphStyle("h2", parent=styles["Heading2"], textColor=HexColor(NAVY), fontName="Helvetica-Bold", fontSize=13, spaceBefore=6, spaceAfter=3)
    body = ParagraphStyle("body", parent=styles["BodyText"], textColor=HexColor("#102033"), fontName="Helvetica", fontSize=9, leading=12)
    small = ParagraphStyle("small", parent=body, fontSize=8, leading=10, textColor=HexColor("#5C6B7A"))
    story = []
    story.append(Paragraph("Crypto Grid Bot Master Strategy", title))
    story.append(Paragraph("Static range, Grid-Fit launch gate, and a full bot budget. Second study pass.", body))
    story.append(Paragraph(EDU + " " + DISCLAIMER, body))
    story.append(Paragraph("What this means for a bot", h))
    points = [
        "Set the range when you launch, and leave it there. Exchange grid bots (the usual spot and futures grids) use a fixed lower price and a fixed upper price. A band that jumps to every new close is not that bot. This pass freezes the ATR or Bollinger range on the launch bar.",
        "Do not launch just because a level was crossed. Launch when the Grid-Fit Screener, on the last closed 4h bar, scores at least 60 and calls the market neutral: ADX below 22 and Bollinger width below 8%, liquid, not in a spike cooldown, and not a Sydney weekend.",
        "Give the bot one budget, for example 10,000, and split all of it across the buy levels below the launch price. Judge the bot by the profit or loss of that budget when the bot stops, not by a 1% wiggle in a much larger account.",
        "A winning grid sell is a small cycle. The loss that matters is the stop, when the inventory is closed below the band. Read the stop-out column before you read the win rate.",
        "A cell with fewer than 20 deployments is not a result. The interval next to a win rate is a 95% Wilson interval. A wide interval means the sample cannot support the percentage.",
    ]
    story.append(ListFlowable([ListItem(Paragraph(p, body), leftIndent=6) for p in points], bulletType="bullet"))

    story.append(Paragraph("How the two modes differ once the range is fixed", h))
    story.append(Paragraph("Arithmetic puts equal price gaps between the frozen levels. Geometric puts equal percentage gaps. With a moving band the two often produced the same trades, because the band did the work. With a frozen band the gaps stay put, so the distance from a buy to its target is the spacing you chose.", body))
    story.append(Paragraph("The bot reserves the whole budget for the levels below the launch price, equal quote amount each, with room for the entry fee. A filled buy is sold at the next level up. Nothing is pre-bought for the levels above the launch price. A hard stop sits under the frozen lower level. A hard take-profit sits above the frozen upper level. Three closes outside the band close the bot, and the next launch is a new decision.", body))

    fam = s["family"]
    ch = s["chosen_settings"]
    story.append(Paragraph("Settings", h))
    story.append(Paragraph(
        f"The search had {s['setting_grid']} setting combinations per mode and {s['variants_logged']} logged rows, including the exit and gate families. "
        f"Coins were pooled. The tune window is 1 Jan 2021 through 15 May 2026 where the exchange history exists. ZEC on this OKX endpoint starts in November 2025. "
        f"16 May 2026 through 15 Nov 2026 was not used to pick a rule.", body))
    spec_rows = [["Input", "Arithmetic", "Geometric"]]
    for key, label in (("levels", "Levels"), ("method", "Range at launch"), ("min_spacing_pct", "Minimum spacing %"), ("stop_pct", "Stop % below the lower level")):
        spec_rows.append([label, str(ch["Arithmetic"]["spec"][key]), str(ch["Geometric"]["spec"][key])])
    spec_rows.append(["Exit", fam["Arithmetic"]["exit"], fam["Geometric"]["exit"]])
    spec_rows.append(["Launch gate", fam["Arithmetic"]["gate"], fam["Geometric"]["gate"]])
    story.append(table(spec_rows, [70 * mm, 70 * mm, 70 * mm]))
    for mode in ("Arithmetic", "Geometric"):
        sc = ch[mode]["is"]
        story.append(Paragraph(
            f"{mode} in-sample, the settings search, per-level exits and the screener gate: deployment win rate {pct(sc['win']) if sc else '—'}, "
            f"mean return on the 10,000 budget {pct(sc['ret']) if sc else '—'}, deployments {sc['n'] if sc else 0}. "
            f"The family lock then chose {fam[mode]['exit']} with gate {fam[mode]['gate']}: "
            f"in-sample win rate {pct(fam[mode]['is']['win']) if fam[mode]['is'] else '—'}, "
            f"mean return {pct(fam[mode]['is']['ret']) if fam[mode]['is'] else '—'}.",
            body))

    story.append(Paragraph("Before and after, out of sample", h))
    story.append(Paragraph(
        "Before is the previous locked rule: a band rewritten every bar, close-all on an up-cross, 6 levels, Bollinger, 2% spacing, 2% stop. It is re-run here on the same 10,000 budget with the 1% risk cap removed, so the size is comparable. After is the static-range rule locked above. Both are out of sample. A cell with n below 20 is marked not meaningful and is not a result.",
        body))
    story.append(Image(str(charts[1]), width=240 * mm, height=100 * mm))
    story.append(Paragraph(DISCLAIMER, small))
    header = ["Mode", "Coin", "TF", "Before win rate", "After win rate", "After return", "After DD", "Stops", "Stop loss"]
    rows = [header]
    coins = ["BTC-USDT", "ETH-USDT", "SOL-USDT", "ZEC-USDT", "XRP-USDT", "LINK-USDT"]
    for mode in ("Arithmetic", "Geometric"):
        for inst in coins:
            for tf in ("1h", "4h"):
                b = find(data["before"], mode=mode, inst=inst, tf=tf)
                a = find(data["oos"], mode=mode, inst=inst, tf=tf, label="locked")
                rows.append([
                    mode[:5], inst.split("-")[0], tf,
                    cell_win(b), cell_win(a), pct(a["mean_ret"]), pct(a["max_dd"]),
                    str(a["stops"]), pct(a["stop_mean_ret"]),
                ])
    story.append(table(rows, [22 * mm, 16 * mm, 12 * mm, 52 * mm, 52 * mm, 24 * mm, 20 * mm, 16 * mm, 22 * mm]))
    story.append(Paragraph("Win rates show a 95% Wilson interval. Return is the average deployment pnl divided by the 10,000 budget. Stop loss is the average return of the deployments that ended at the stop. " + DISCLAIMER, small))

    after = [r for r in data["oos"] if r["label"] == "locked"]
    before = data["before"]
    ap, bp = pooled([r for r in after if r["meaningful"]]), pooled([r for r in before if r["meaningful"]])
    meaningful = [r for r in after if r["meaningful"]]
    best = max(meaningful, key=lambda r: r["win"]) if meaningful else None
    story.append(Paragraph(
        f"Pooled out of sample, using only cells with at least 20 deployments: the previous moving-band rule won {pct(bp['win'])} of {bp['n']} deployments, "
        f"mean return {bp['ret']*100:.2f}% of the 10,000 budget. The locked static rule won {pct(ap['win'])} of {ap['n']} deployments, "
        f"mean return {ap['ret']*100:.2f}% of the budget. The win rate is higher. The return on bot capital is still about flat, and the 75% target was not met. "
        f"The guide keeps the static settings because that comparison was fixed before the out-of-sample window was opened. A higher win rate with a flat return is not a profit result.",
        body))
    if best:
        story.append(Paragraph(
            f"Among out-of-sample cells with at least 20 deployments, the highest deployment win rate is {best['mode']} {best['inst'].split('-')[0]} {best['tf']}: "
            f"{pct(best['win'])}, 95% interval {pct(best['ci_lo'])} to {pct(best['ci_hi'])}, n={best['n']}. "
            f"The 75% target is met only if the interval, not a small sample, sits at or above 75%. It does not, on this cell or on the pooled count.",
            body))
    else:
        story.append(Paragraph("No out-of-sample cell reached 20 deployments. There is no win-rate result to report.", body))
    story.append(Paragraph(
        "The 75% target is a deployment win rate, out of sample, on a sample large enough to read. A cycle win rate can look calmer because each grid sell is small. The stop closes the inventory. That cost is in the stop column.",
        body))

    story.append(Image(str(charts[0]), width=240 * mm, height=95 * mm))
    story.append(Paragraph(DISCLAIMER, small))

    story.append(Paragraph("Exits and extra data", h))
    story.append(Paragraph(
        "Close-all, per-level targets, a one-step trailing exit, and sells only above average cost were scored in sample on the locked spacing. So were a realised-volatility pause and a gate that skips alt launches when Bitcoin's trailing 30-day return is below -10%. "
        "Funding is charged when the public OKX history has a rate; that history starts in August 2026, so it cannot tune a funding gate. The holdout rows below were not used to change the lock.",
        body))
    hold = [r for r in data["variants"] if r.get("stage") == "oos_holdout_not_used"]
    hrows = [["Mode", "Exit", "Gate", "OOS win rate", "OOS mean return", "n"]]
    for r in hold:
        hrows.append([r["mode"][:5], r["exit"], r["gate"], pct(r["win"]), pct(r["ret"]), str(r["n"])])
    if len(hrows) > 1:
        story.append(table(hrows, [28 * mm, 32 * mm, 28 * mm, 36 * mm, 40 * mm, 24 * mm]))
    story.append(Paragraph("These rows are a holdout. They did not choose the settings. " + DISCLAIMER, small))

    # Stop cost on the locked OOS book
    stop_n = sum(r["stops"] for r in after)
    stop_pnl = sum(r["stop_pnl"] or 0 for r in after)
    story.append(Paragraph(
        f"Out of sample, the locked rules recorded {stop_n} stop-outs. Their combined pnl was {stop_pnl:.0f} on a sequence of separate 10,000 budgets "
        f"({pct(stop_pnl / (stop_n * 10000)) if stop_n else '—'} average per stop, when there was one). "
        f"A grid that wins its small sells and then stops out can still lose the deployment.",
        body))

    story.append(Paragraph("Scaling, on the bot budget", h))
    story.append(Paragraph(
        "Hypothetical account of 10,000. Each deployment uses 25% of the account as the bot budget, and the deployment's return on that budget is applied to the account. "
        "After three winning deployments and a drawdown under 8%, the fraction steps up by 0.10, capped at 0.50. A drawdown past 15% cuts the fraction in half until a new high. "
        "The bootstrap redraws the out-of-sample deployment returns 2,000 times. It does not create new prices. Hypothetical backtest, not a forecast.",
        body))
    scale = data.get("scale")
    # scale is attached by this builder if the runner stored it inside summary; compute here from oos rows' we don't have per-dep returns in slim.
    # The runner stores mean_ret. A proper curve needs the deployment list. Read pass2 if present.
    scale_path = OUT / "pass2_scale.json"
    if scale_path.exists():
        scale = json.loads(scale_path.read_text())
        fig, ax = plt.subplots(figsize=(10.2, 4.0))
        style_ax(ax, "Hypothetical account, size rule on out-of-sample bot returns")
        ax.plot(scale["curve"], color=CYAN, lw=1.4)
        ax.axhline(10000, color="#9FB3C8", lw=0.6)
        ax.set_ylabel("Account equity", color="white")
        ax.set_xlabel("Deployment step", color="white")
        scale["chart"] = str(save(fig, "pass2_scale.png"))
        story.append(Paragraph(
            f"Size-rule terminal equity {scale['end']:.0f} from 10,000, max drawdown {pct(scale['max_dd'])}. "
            f"Bootstrap terminal, 5th percentile {scale['p05']:.0f}, median {scale['p50']:.0f}. "
            f"Bootstrap max drawdown, median {pct(scale['dd50'])}, 95th percentile {pct(scale['dd95'])}.",
            body))
        if scale.get("chart"):
            story.append(Image(scale["chart"], width=240 * mm, height=90 * mm))
            story.append(Paragraph(DISCLAIMER, small))

    story.append(Paragraph("Limits", h))
    limits = [
        "The simulator is not an exchange matching engine. Limit fills assume the bar's high and low traded. A bar that touches both the stop and the take-profit is resolved by which side is closer to the open.",
        "The screener was written for 4h data and a 2,000,000 USDT per hour liquidity floor. Spot volume on OKX is the volume used here.",
        "Funding history from the public endpoint starts in August 2026. Earlier bars are charged nothing.",
        "ZEC history on this endpoint starts in November 2025. Its in-sample window is shorter.",
        "A win rate without the return on the bot budget, and without the stop-out cost, is an incomplete description.",
        "Nothing here is an instruction to run a live bot.",
    ]
    story.append(ListFlowable([ListItem(Paragraph(x, body), leftIndent=6) for x in limits], bulletType="bullet"))
    story.append(Paragraph("Checklist", h))
    checks = [
        "The range is written down at launch and is not rebuilt from the latest close.",
        "The screener score on the last closed 4h bar is at least 60, and the mode is neutral.",
        "The bot budget is a number you can point at, and every buy level's notional adds up to that budget.",
        "You know the stop price and what a stop does to the inventory.",
        "You will not treat a cell with fewer than 20 finished bots as evidence.",
        "Education only. Past performance is not a reliable indicator of future results.",
    ]
    story.append(ListFlowable([ListItem(Paragraph(x, body), leftIndent=6) for x in checks], bulletType="bullet"))

    doc = SimpleDocTemplate(str(PDF), pagesize=landscape(A4), leftMargin=12 * mm, rightMargin=12 * mm,
                            topMargin=18 * mm, bottomMargin=16 * mm, title="GridBot Builder — Master Strategy guide",
                            author="GridBot Builder")
    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
    check(data)
    print("pdf", PDF)


def check(data):
    from pypdf import PdfReader
    text = "\n".join((p.extract_text() or "") for p in PdfReader(str(PDF)).pages)
    missing = []
    if "Market Pros" in text or "ABN" in text:
        missing.append("brand")
    if DISCLAIMER not in text:
        missing.append("disclaimer")
    for mode in ("Arithmetic", "Geometric"):
        sc = data["summary"]["chosen_settings"][mode]["is"]
        if sc and pct(sc["win"]) not in text:
            missing.append(mode + " is win")
        for inst in ("BTC-USDT", "ETH-USDT", "SOL-USDT", "ZEC-USDT", "XRP-USDT", "LINK-USDT"):
            for tf in ("1h", "4h"):
                row = find(data["oos"], mode=mode, inst=inst, tf=tf, label="locked")
                if row["meaningful"] and pct(row["win"]) not in text:
                    missing.append(f"{mode} {inst} {tf}")
                if not row["meaningful"] and "not meaningful" not in text:
                    missing.append("flag")
    if missing:
        raise SystemExit("PDF check failed: " + ", ".join(missing[:12]))
    print("pdf check ok")


if __name__ == "__main__":
    build()
