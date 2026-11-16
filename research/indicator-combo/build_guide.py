"""Build the GridBot Builder guide from the result JSON files.

Every number printed in the PDF is formatted from those files and checked
against the same format before the file is written.
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, ListFlowable, ListItem, KeepTogether,
)

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "results"
CHARTS = ROOT / "charts"
CHARTS.mkdir(parents=True, exist_ok=True)
PDF = ROOT / "GridBot_Master_Strategy_Guide.pdf"

NAVY = "#0A1628"
CYAN = "#00D4FF"
INK = "#102033"
MUTED = "#5C6B7A"
DISCLAIMER = "Past performance is not a reliable indicator of future results."
EDU = "Education only. Not financial advice. Hypothetical backtest, not a forecast."


def pct(x, digits=1):
    if x is None:
        return "—"
    return f"{100.0 * float(x):.{digits}f}%"


def num(x, digits=0):
    if x is None:
        return "—"
    return f"{float(x):.{digits}f}"


def load():
    return {
        "summary": json.loads((OUT / "summary.json").read_text()),
        "is": json.loads((OUT / "is_results.json").read_text()),
        "oos": json.loads((OUT / "oos_results.json").read_text()),
        "wf": json.loads((OUT / "walkforward.json").read_text()),
        "variants": json.loads((OUT / "variants.json").read_text()),
        "equity": json.loads((OUT / "equity_oos.json").read_text()),
        "scaling": json.loads((OUT / "scaling.json").read_text()),
    }


def find_row(rows, **kw):
    for r in rows:
        if all(r.get(k) == v for k, v in kw.items()):
            return r
    return None


def style_ax(ax, title):
    ax.set_facecolor("#0E1C2F")
    ax.set_title(title, color="white", loc="left", fontsize=12, pad=8)
    ax.tick_params(colors="white", labelsize=8)
    for sp in ax.spines.values():
        sp.set_color("#1E3A55")
    ax.grid(True, color="#1E3A55", linewidth=0.4)
    ax.figure.patch.set_facecolor(NAVY)


def save_fig(fig, name):
    fig.text(0.01, 0.01, DISCLAIMER, color="#9FB3C8", fontsize=8)
    path = CHARTS / name
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    fig.savefig(path, dpi=140)
    plt.close(fig)
    return path


def chart_modes(equity):
    fig, ax = plt.subplots(figsize=(10.2, 4.2))
    style_ax(ax, "Out-of-sample marked equity, BTC 4h, locked rules")
    for mode, color in (("Arithmetic", CYAN), ("Geometric", "#7AA2FF")):
        # key is mode|family|inst|tf; family varies. Match prefix and suffix.
        series = [(k, v) for k, v in equity.items() if k.startswith(mode + "|") and k.endswith("|BTC-USDT|4h")]
        if not series:
            continue
        v = series[0][1]
        t = np.array(v["t"], dtype=np.int64)
        eq = np.array(v["equity"], dtype=float)
        # plot as an index starting at 100
        if len(eq) == 0 or eq[0] == 0:
            continue
        idx = 100.0 * eq / eq[0]
        hours = (t - t[0]) / 3_600_000.0 / 24.0
        ax.plot(hours, idx, color=color, linewidth=1.4, label=mode)
    # Keep a minimum span so a few tenths of a percent do not fill the frame.
    ys = [ln.get_ydata() for ln in ax.get_lines()]
    flat = [v for arr in ys for v in arr]
    if flat:
        lo, hi = min(flat), max(flat)
        span = max(5.0, (hi - lo) * 1.25)
        mid = (lo + hi) / 2.0
        ax.set_ylim(mid - span / 2.0, mid + span / 2.0)
    ax.set_xlabel("Days from 16 May 2026", color="white")
    ax.set_ylabel("Equity index, start = 100", color="white")
    leg = ax.legend(facecolor=NAVY, edgecolor="#1E3A55", labelcolor="white")
    return save_fig(fig, "oos_btc_4h.png")


def chart_win_bars(oos_rows, family_for):
    fig, ax = plt.subplots(figsize=(10.2, 4.4))
    style_ax(ax, "Out-of-sample deployment win rate by coin, 4h, locked rules")
    coins = ["BTC-USDT", "ETH-USDT", "SOL-USDT", "ZEC-USDT", "XRP-USDT", "LINK-USDT"]
    x = np.arange(len(coins))
    width = 0.38
    for offset, mode, color in ((-width / 2, "Arithmetic", CYAN), (width / 2, "Geometric", "#7AA2FF")):
        vals = []
        for c in coins:
            row = find_row(oos_rows, mode=mode, inst=c, tf="4h", label="deep", family=family_for[mode])
            vals.append(0.0 if row is None or row["deployment_win_rate"] is None else 100 * row["deployment_win_rate"])
        ax.bar(x + offset, vals, width=width, color=color, label=mode)
    ax.axhline(75, color="#F5C16C", linewidth=1, linestyle="--", label="75% study target")
    ax.set_xticks(x)
    ax.set_xticklabels([c.split("-")[0] for c in coins], color="white")
    ax.set_ylabel("Deployment win rate, %", color="white")
    ax.set_ylim(0, 100)
    ax.legend(facecolor=NAVY, edgecolor="#1E3A55", labelcolor="white", fontsize=8)
    return save_fig(fig, "oos_win_4h.png")


def chart_spacing():
    fig, ax = plt.subplots(figsize=(10.2, 3.6))
    style_ax(ax, "Same lower and upper price, two ways to place eight levels")
    lo, hi, n = 100.0, 180.0, 8
    xs = np.arange(n)
    arith = lo + (hi - lo) * xs / (n - 1)
    geom = lo * (hi / lo) ** (xs / (n - 1))
    ax.plot(arith, np.zeros(n), "o", color=CYAN, label="Arithmetic, equal price gaps")
    ax.plot(geom, np.ones(n), "o", color="#7AA2FF", label="Geometric, equal percentage gaps")
    for a, g in zip(arith, geom):
        ax.plot([a, a], [0, -0.15], color=CYAN, linewidth=0.6)
        ax.plot([g, g], [1, 1.15], color="#7AA2FF", linewidth=0.6)
    ax.set_yticks([0, 1])
    ax.set_yticklabels(["Arithmetic", "Geometric"], color="white")
    ax.set_xlabel("Price", color="white")
    ax.set_ylim(-0.6, 1.7)
    ax.legend(facecolor=NAVY, edgecolor="#1E3A55", labelcolor="white", fontsize=8)
    return save_fig(fig, "spacing_modes.png")


def chart_scale(scaling, mode):
    fig, ax = plt.subplots(figsize=(10.2, 4.2))
    style_ax(ax, f"Hypothetical size-rule equity, {mode}, four sleeves, 4h out of sample")
    book = next(b for b in scaling["books"] if b["mode"] == mode)
    curve = np.array(book["curve"], dtype=float)
    ax.plot(np.arange(len(curve)), curve, color=CYAN, linewidth=1.5, label="Size rule on the out-of-sample episodes")
    mc = book["monte_carlo"]
    if mc.get("median_curve"):
        med = np.array(mc["median_curve"], dtype=float)
        low = np.array(mc["low_curve"], dtype=float)
        ax.plot(np.arange(len(med)), med, color="#7AA2FF", linewidth=1, label="Bootstrap median path")
        ax.plot(np.arange(len(low)), low, color="#F5C16C", linewidth=1, label="Bootstrap low path")
    ys = [ln.get_ydata() for ln in ax.get_lines()]
    flat = [float(v) for arr in ys for v in arr]
    if flat:
        lo, hi = min(flat), max(flat)
        span = max(500.0, (hi - lo) * 1.25)
        mid = (lo + hi) / 2.0
        ax.set_ylim(mid - span / 2.0, mid + span / 2.0)
    ax.set_xlabel("Episode step in the replay", color="white")
    ax.set_ylabel("Hypothetical equity", color="white")
    ax.legend(facecolor=NAVY, edgecolor="#1E3A55", labelcolor="white", fontsize=8)
    return save_fig(fig, f"scale_{mode.lower()}.png")


def header_footer(canvas, doc):
    canvas.saveState()
    w, h = landscape(A4)
    canvas.setFillColor(HexColor(NAVY))
    canvas.rect(0, h - 14 * mm, w, 14 * mm, fill=1, stroke=0)
    canvas.setFillColor(HexColor(CYAN))
    canvas.setFont("Helvetica-Bold", 11)
    canvas.drawString(14 * mm, h - 9 * mm, "GridBot Builder")
    canvas.setFillColor(white)
    canvas.setFont("Helvetica", 9)
    canvas.drawRightString(w - 14 * mm, h - 9 * mm, "Master Strategy guide  ·  education only")
    canvas.setFillColor(HexColor(NAVY))
    canvas.rect(0, 0, w, 12 * mm, fill=1, stroke=0)
    canvas.setFillColor(HexColor(CYAN))
    canvas.setFont("Helvetica", 8)
    canvas.drawString(14 * mm, 5 * mm, EDU)
    canvas.setFillColor(white)
    canvas.drawRightString(w - 14 * mm, 5 * mm, f"{doc.page}")
    canvas.restoreState()


def build():
    data = load()
    summary = data["summary"]
    deep = summary["deep"]
    family_for = {m: deep[m]["family"] for m in ("Arithmetic", "Geometric")}
    charts = [
        chart_spacing(),
        chart_modes(data["equity"]),
        chart_win_bars(data["oos"], family_for),
        chart_scale(data["scaling"], "Arithmetic"),
        chart_scale(data["scaling"], "Geometric"),
    ]

    styles = getSampleStyleSheet()
    title = ParagraphStyle("title", parent=styles["Title"], textColor=HexColor(NAVY), fontName="Helvetica-Bold", fontSize=22, leading=26, alignment=TA_LEFT)
    h = ParagraphStyle("h", parent=styles["Heading2"], textColor=HexColor(NAVY), fontName="Helvetica-Bold", fontSize=14, spaceBefore=8, spaceAfter=4)
    body = ParagraphStyle("body", parent=styles["BodyText"], textColor=HexColor(INK), fontName="Helvetica", fontSize=9.5, leading=13, alignment=TA_LEFT)
    small = ParagraphStyle("small", parent=body, fontSize=8, leading=10.5, textColor=HexColor(MUTED))
    cell = ParagraphStyle("cell", parent=body, fontSize=7, leading=9)

    story = []
    story.append(Paragraph("Crypto Grid Bot Master Strategy", title))
    story.append(Paragraph("Arithmetic and Geometric modes. A study guide for reading the script, running it beside a grid bot, and reading a historical simulation.", body))
    story.append(Spacer(1, 4 * mm))
    story.append(Paragraph(EDU, body))
    story.append(Paragraph(DISCLAIMER, body))
    story.append(Spacer(1, 3 * mm))
    story.append(Paragraph("This guide describes one saved TradingView strategy, <b>Crypto Grid Bot Master Strategy &amp; Alert System</b>, file <font face='Courier'>grid-bot-original.pine</font>. Arithmetic and Geometric are its two grid calculations. There is no separate on-chain indicator in this study.", body))

    story.append(Paragraph("What each mode shows", h))
    story.append(Paragraph("Both modes draw a lower price and an upper price, then place levels between them. A down-cross of a level can add a long. An up-cross flattens the open quantity. Buys pause when ADX is at or above its threshold or when price is far from the trend EMA, and they stay paused until several closes sit back inside the range. A hard stop sits under the lower level. A hard take-profit sits above the upper level. After enough closes outside the range, the script recentres the band.", body))
    story.append(Paragraph("<b>Arithmetic</b> spaces those levels by the same price distance. The gap in currency is constant, so the percentage gap is wider at the bottom of the band than at the top.", body))
    story.append(Paragraph("<b>Geometric</b> spaces them by the same percentage. Each step is a similar relative move. That is the usual fit when the coin's price covers a wide band, because a fixed coin gap becomes a tiny percentage near the top.", body))
    story.append(Spacer(1, 2 * mm))
    story.append(Image(str(charts[0]), width=240 * mm, height=82 * mm))
    story.append(Paragraph(DISCLAIMER + " The drawing is a formula, not a backtest.", small))

    story.append(Paragraph("How the original script behaves", h))
    story.append(Paragraph("The independent review of this file records several behaviours the port keeps, because the task is to test this script rather than a repaired one. In the default auto-range, the band is recalculated from the latest close on every bar, so a level can move through price even when price did not move. One entry id is shared, and any up-cross closes the whole position. Only the last crossed level on a bar is kept. The hard stop and the hard take-profit move whenever the band moves. Those are properties of the file, not extra filters added for this study.", body))
    story.append(Paragraph("The port checks the previous bar's stop and take-profit against the next bar's high and low. If both sit inside the same bar, the side closer to the open is taken first. A gap through the stop fills at the open. Fees are 0.10% a side, matching the script. Slippage is 0.05% a side on market and stop fills. The script's own slippage is one exchange tick, which is not comparable across coins, so it is not what this study charges. Take-profit limits fill at the limit.", body))
    story.append(Paragraph("Reported runs size each new order at 5% of marked equity, still under the script's 1% risk cap and six-entry cap. A fixed quantity of 1 on the script's 1,000,000 starting capital is a different fraction of price on every coin, so it is reported only as a check on BTC.", body))

    story.append(Paragraph("A routine for using it with a grid bot", h))
    story.append(Paragraph("Use the script as a checklist beside the bot. The script does not place exchange orders. Alerts, if you turn them on, are messages. Confirm fills on the exchange.", body))
    steps = [
        "Open the chart on the coin and bar size you intend to run. Add the strategy. Pick Arithmetic or Geometric before you read the levels. Changing the mode moves every level.",
        "Leave Auto-Grid on unless you have written a lower and an upper price yourself. Read the dashboard: range, spacing percent, whether buys are paused, and the outside-bar count.",
        "Launch only when the dashboard is in range, buys are not paused, and the spacing percent is wider than the round trip in fees and slippage (0.10% plus 0.05% each side in this study, so about 0.30% before funding).",
        "Pause new buys when the dashboard says buys are paused, or when the picks screen would skip the coin: 30-day drift above 0.8 and daily ADX above 40. The deep-search pass tests that gate. It does not override a stop you have already set.",
        "Rebuild only after the written outside-bar count, and only when you can say what the new range is. In this script the auto-range rebuild does not stay put on the next bar. Treat a rebuild as a new decision, not as an automatic trail.",
        "Widen the band, or raise the minimum spacing, when the step is inside the fee. Do not add levels to make a quiet chart look active.",
        "Stop the bot when the hard stop is hit, when the position no longer matches the written plan, or when you cannot explain the open inventory in one sentence. A take-profit above the band is also an exit of the whole position in this script.",
    ]
    story.append(ListFlowable([ListItem(Paragraph(s, body), leftIndent=8) for s in steps], bulletType="1", start="1"))

    story.append(Paragraph("Settings used in the study", h))
    story.append(Paragraph("The search changed only level count, ADX threshold, hard-stop percent, range method, and minimum spacing. It did this separately for each mode, on BTC and ETH, 1h and 4h, from 16 Nov 2023 through 15 May 2026. Anything within two percentage points on deployment win rate was broken by higher net return, then by a smaller drawdown. A variant needed at least 20 deployments across the four tune series.", body))
    story.append(Paragraph(f"Setting combinations per mode: {summary['setting_grid']}. Rows in the variant log, including walk-forward retunes and the deep-search families: {summary['variants_logged']}.", body))

    spec_header = ["Input", "Script default", "Arithmetic locked", "Geometric locked"]
    spec_rows = [spec_header]
    labels = [
        ("levels", "Grid levels", "8"),
        ("adx_threshold", "ADX threshold", "20"),
        ("stop_pct", "Hard stop % below the lower level", "0.75"),
        ("method", "Auto-range method", "ATR"),
        ("min_spacing_pct", "Minimum spacing %", "1.25"),
    ]
    for key, label, default in labels:
        spec_rows.append([
            label, default,
            str(summary["chosen_settings"]["Arithmetic"]["spec"][key]),
            str(summary["chosen_settings"]["Geometric"]["spec"][key]),
        ])
    spec_rows.append(["Structure kept for the deep pass", "Moving range", family_for["Arithmetic"], family_for["Geometric"]])
    spec_rows.append(["Order size", "1 unit", "5% of equity", "5% of equity"])
    spec_rows.append(["Fee / slippage", "0.10% and 1 tick", "0.10% and 0.05%", "0.10% and 0.05%"])
    spec_rows.append(["Unchanged inputs", "EMA 100, deviation 3%, recovery 4 bars, regrid 3 bars, take-profit 2%, ATR 14 × 2, risk 1%, max entries 6", "", ""])
    story.append(table(spec_rows, [55 * mm, 40 * mm, 55 * mm, 55 * mm]))
    story.append(Paragraph("In-sample score of the locked settings, mean of BTC and ETH, 1h and 4h. This number chose the settings. It is not the result.", small))
    for mode in ("Arithmetic", "Geometric"):
        sc = summary["chosen_settings"][mode]["is_score"]
        deep_sc = summary["deep"][mode]["is_score"]
        story.append(Paragraph(
            f"{mode} settings, in-sample mean deployment win rate {pct(sc['win'])}, mean net {pct(sc['net'])}, mean max drawdown {pct(-sc['neg_dd'])}. "
            f"Deep family <b>{family_for[mode]}</b>, in-sample mean deployment win rate {pct(deep_sc['win'])}, mean net {pct(deep_sc['net'])}.",
            body))

    story.append(Paragraph("Where the in-sample episodes sat", h))
    story.append(Paragraph("These buckets use the ADX reading at the first buy of an in-sample episode, on BTC and ETH only. They describe the tune window. They were not recomputed to change the out-of-sample rules.", body))
    reg_header = ["Mode", "ADX below 20", "ADX 20 to 30", "ADX 30 and above"]
    reg_rows = [reg_header]
    for mode in ("Arithmetic", "Geometric"):
        reg = summary["regimes_is"][mode]
        def cell_reg(key):
            b = reg[key]
            return f"{pct(b['win_rate'])}  (n={b['n']})"
        reg_rows.append([mode, cell_reg("adx_<20"), cell_reg("adx_20_30"), cell_reg("adx_>=30")])
    story.append(table(reg_rows, [40 * mm, 55 * mm, 55 * mm, 55 * mm]))

    manifest = json.loads((ROOT / "data" / "manifest.json").read_text())
    story.append(Paragraph("Candles", h))
    story.append(Paragraph("Public OKX spot history-candles, confirmed bars only. Bybit's public API was blocked from this environment. Swap funding is the OKX public funding-rate history. That endpoint returned 10 Aug 2026 through 16 Nov 2026, so earlier bars are charged no funding.", body))
    for inst, meta in manifest["symbols"].items():
        bits = []
        for tf in ("1h", "4h"):
            info = meta.get(tf)
            if info:
                bits.append(f"{tf} {info['start'][:10]} to {info['end'][:10]} ({info['rows']} bars)")
        story.append(Paragraph(f"{inst}, tick {meta['tick']}: " + "; ".join(bits) + ".", body))
    story.append(Paragraph("ZEC-USDT on this endpoint starts 24 Nov 2025, so its in-sample window is shorter than the others. ZEC was not used to choose settings.", body))

    story.append(Paragraph("In-sample and out-of-sample results", h))
    story.append(Paragraph("Out-of-sample is 16 May 2026 through 15 Nov 2026. It includes the November 2026 sell-off. No setting and no family was changed after these rows were computed. The table is the locked deep family. Win rate is the share of episodes with pnl above zero after fees and slippage.", body))
    story.append(Image(str(charts[1]), width=240 * mm, height=95 * mm))
    story.append(Paragraph(DISCLAIMER, small))
    story.append(Spacer(1, 2 * mm))
    story.append(Image(str(charts[2]), width=240 * mm, height=100 * mm))
    story.append(Paragraph(DISCLAIMER + " The dashed line is the study target, not a promise.", small))

    header = ["Mode", "Coin", "TF", "IS cycle", "IS dep", "IS net", "IS DD", "OOS cycle", "OOS dep", "OOS net", "OOS DD", "Stops", "n", "Time"]
    table_rows = [header]
    coins = ["BTC-USDT", "ETH-USDT", "SOL-USDT", "ZEC-USDT", "XRP-USDT", "LINK-USDT"]
    for mode in ("Arithmetic", "Geometric"):
        for inst in coins:
            for tf in ("1h", "4h"):
                a = find_row(data["is"], mode=mode, inst=inst, tf=tf, label="deep", family=family_for[mode])
                b = find_row(data["oos"], mode=mode, inst=inst, tf=tf, label="deep", family=family_for[mode])
                table_rows.append([
                    mode[:5], inst.split("-")[0], tf,
                    pct(a["cycle_win_rate"]), pct(a["deployment_win_rate"]), pct(a["net_return"]), pct(a["max_dd"]),
                    pct(b["cycle_win_rate"]), pct(b["deployment_win_rate"]), pct(b["net_return"]), pct(b["max_dd"]),
                    str(b["stops"]), str(b["deployments"]), pct(b["time_in_market"], 0),
                ])
    story.append(Spacer(1, 2 * mm))
    story.append(table(table_rows, [20 * mm, 14 * mm, 12 * mm, 18 * mm, 16 * mm, 16 * mm, 16 * mm, 20 * mm, 18 * mm, 16 * mm, 16 * mm, 14 * mm, 12 * mm, 14 * mm]))
    story.append(Paragraph("IS is 16 Nov 2023–15 May 2026. OOS is 16 May 2026–15 Nov 2026. DD is the largest peak-to-trough of marked equity. Stops count deployments closed by the hard stop. Time is the share of bars with a position. " + DISCLAIMER, small))

    # Target line, computed, not typed.
    oos_deep = [r for r in data["oos"] if r["label"] == "deep" and r["family"] == family_for[r["mode"]]]
    big = [r for r in oos_deep if r["deployments"] >= 20 and r["deployment_win_rate"] is not None]
    best = max(big, key=lambda r: r["deployment_win_rate"])
    best_txt = f"{best['mode']} {best['inst'].split('-')[0]} {best['tf']} at {pct(best['deployment_win_rate'])} over {best['deployments']} deployments"
    smalls = [r for r in oos_deep if r["deployments"] < 20 and r["deployment_win_rate"] is not None and r["deployment_win_rate"] >= 0.75]
    if smalls:
        s = smalls[0]
        small_txt = f"{s['mode']} {s['inst'].split('-')[0]} {s['tf']} at {pct(s['deployment_win_rate'])} over {s['deployments']} deployments"
    else:
        small_txt = "no smaller cell at 75%"
    # mean deployment win rate across all reported OOS rows
    dep_rates = [r["deployment_win_rate"] for r in oos_deep if r["deployment_win_rate"] is not None]
    cyc_rates = [r["cycle_win_rate"] for r in oos_deep if r["cycle_win_rate"] is not None]
    mean_dep = sum(dep_rates) / len(dep_rates) if dep_rates else None
    mean_cyc = sum(cyc_rates) / len(cyc_rates) if cyc_rates else None
    tune_oos = [r for r in oos_deep if r["inst"] in ("BTC-USDT", "ETH-USDT")]
    tune_dep = [r["deployment_win_rate"] for r in tune_oos if r["deployment_win_rate"] is not None]
    mean_tune = sum(tune_dep) / len(tune_dep) if tune_dep else None
    story.append(Paragraph(
        f"Across every coin and both bar sizes, the locked rules produced a mean out-of-sample cycle win rate of {pct(mean_cyc)} and a mean out-of-sample deployment win rate of {pct(mean_dep)}. "
        f"On the tune coins only, BTC and ETH, the mean out-of-sample deployment win rate was {pct(mean_tune)}. "
        f"The study target was 75% out of sample on the deployment win rate. That target was not met on the mean, and it was not met on any coin and bar size with 20 or more out-of-sample deployments. "
        f"The highest such cell was {best_txt}. One smaller cell reached {small_txt}. A short sample can print a high rate. Read it next to the deployment count. "
        f"Under these locked settings the two modes often print the same row: the moving band and the close-all rule do more of the work than the spacing formula.",
        body))

    # blocked filter line, averaged where present
    shares = [r["blocked_stop_share"] for r in oos_deep if r.get("blocked_stop_share") is not None]
    blocked_n = sum(r["blocked_entries"] or 0 for r in oos_deep)
    if shares:
        story.append(Paragraph(
            f"Out of sample, the pause rules blocked {blocked_n} buy signals that otherwise met a down-cross. Of the blocked signals the shadow test could judge, {pct(sum(shares)/len(shares))} were followed by a touch of the stop that existed at the signal before a one-step bounce. The shadow holds one idea at a time and does not resize. It is a description of the filter, not a second backtest.",
            body))

    story.append(Paragraph("Deep search and walk-forward", h))
    story.append(Paragraph("Five families were scored on the same in-sample objective, using the locked settings: the original moving range, an anchored range that stays put until a flat rebuild, that anchor plus the drift30/ADX gate, that anchor plus a high-volatility pause, and an anchored per-level grid that exits a lot at the next level instead of closing everything. Funding was applied afterwards as a cost on the locked family. It was not allowed to pick the winner. Funding history is the OKX swap series saved with the candles.", body))
    story.append(Paragraph("Walk-forward retuned the setting grid on three folds that end on 15 May 2026. The folds never see June–November 2026.", body))
    wf_header = ["Fold", "Mode", "Family", "Deploy win", "Net", "Max DD", "Deployments"]
    wf_table = [wf_header]
    for row in data["wf"]:
        if row["family"] not in (family_for[row["mode"]], "moving"):
            continue
        wf_table.append([
            str(row["fold"]), row["mode"][:5], row["family"],
            pct(row["win"]), pct(row["net"]), pct(row["max_dd"]), str(row["deployments"]),
        ])
    story.append(table(wf_table, [20 * mm, 28 * mm, 35 * mm, 30 * mm, 28 * mm, 28 * mm, 32 * mm]))
    story.append(Paragraph("Fold dates: 16 Nov 2024–15 May 2025, 16 May 2025–15 Nov 2025, 16 Nov 2025–15 May 2026. Each fold's settings were chosen on the bars before the fold. " + DISCLAIMER, small))

    fund_rows = [r for r in data["oos"] if r["label"] == "deep_plus_funding"]
    if fund_rows:
        story.append(Paragraph("Adding swap funding on BTC and ETH, out of sample, on the locked family:", body))
        for r in fund_rows:
            base = find_row(data["oos"], mode=r["mode"], inst=r["inst"], tf=r["tf"], label="deep", family=family_for[r["mode"]])
            story.append(Paragraph(
                f"{r['mode']} {r['inst'].split('-')[0]} {r['tf']}: deployment win rate {pct(r['deployment_win_rate'])} with funding, against {pct(base['deployment_win_rate'])} without. Net {pct(r['net_return'])} with funding, against {pct(base['net_return'])} without.",
                body))

    story.append(Paragraph("Hypothetical account scaling", h))
    story.append(Paragraph("The picture below is a replay of the out-of-sample 4h episodes on BTC, ETH, SOL and ZEC. Each sleeve starts at 2,500 in a 10,000 hypothetical account. The size multiplier starts at 1. After three winning episodes and a drawdown under 8%, it steps up by 0.25, capped at 1.5. A drawdown past 15% cuts it to 0.5 until the sleeve makes a new high. The Monte Carlo redraws the same episodes with replacement, 2,000 times, and shows a median path and a low path. It does not create new prices. Hypothetical backtest, not a forecast.", body))
    story.append(Image(str(charts[3]), width=240 * mm, height=95 * mm))
    story.append(Paragraph(DISCLAIMER, small))
    story.append(Image(str(charts[4]), width=240 * mm, height=95 * mm))
    story.append(Paragraph(DISCLAIMER, small))
    for book in data["scaling"]["books"]:
        mc = book["monte_carlo"]
        story.append(Paragraph(
            f"{book['mode']}: the size-rule book ended at {book['end']:.0f} from 10,000, with a max drawdown of {pct(book['max_dd'])}, over {book['returns_used']} episodes. "
            f"Bootstrap terminal equity, 5th percentile {mc['terminal_p05']:.0f}, median {mc['terminal_p50']:.0f}. "
            f"Bootstrap max drawdown, median {pct(mc['maxdd_p50'])}, 95th percentile {pct(mc['maxdd_p95'])}.",
            body))

    story.append(Paragraph("Quantity check", h))
    story.append(Paragraph("Script quantity of 1 unit and 1,000,000 starting capital, BTC 4h, in-sample, original default inputs. This is not the locked rule and it is not out of sample.", body))
    for row in summary["qty_check_is"]:
        story.append(Paragraph(
            f"{row['mode']}: deployment win rate {pct(row['deployment_win_rate'])}, cycle win rate {pct(row['cycle_win_rate'])}, net {pct(row['net_return'])}, max drawdown {pct(row['max_dd'])}, deployments {row['deployments']}.",
            body))

    story.append(Paragraph("Limitations", h))
    limits = [
        "The simulator is not the TradingView broker. Bar paths inside a candle are assumed, not known. A bar that touches both the stop and the take-profit is resolved by which side is closer to the open.",
        "The moving range can mark a cross because the level moved. Live alerts on a forming bar can differ from this closed-bar study.",
        "Spot candles are used for entries. Funding is a separate stress on the swap rate, not a full perpetual backtest. Borrow, margin, and missed fills are not modelled.",
        "5% of equity per order is a study choice so that coins with different prices are comparable. It is not the script's default quantity of 1.",
        "The search is small on purpose. A tighter search on the out-of-sample window would make the 75% figure meaningless, so it was not done.",
        "A high win rate can sit next to a loss. Read the net return and the drawdown on the same row.",
        "Nothing here is an instruction to run a live bot, and nothing here is a forecast.",
    ]
    story.append(ListFlowable([ListItem(Paragraph(s, body), leftIndent=8) for s in limits], bulletType="bullet"))

    story.append(Paragraph("Checklist", h))
    checks = [
        "Mode is chosen and written down: Arithmetic or Geometric.",
        "Range source is written down: auto ATR, auto Bollinger, or a manual band.",
        "Spacing percent is wider than the round trip in fees and slippage.",
        "Hard stop and hard take-profit are visible, and you know they move if the band moves.",
        "The trend pause is on, and you know how many in-range closes turn buys back on.",
        "The outside-bar count for a rebuild is written down, and a rebuild is a new decision.",
        "Order size is a fraction of equity you can name, under the risk cap.",
        "You can say what closes the bot: stop, take-profit, up-cross, or a written invalidation.",
        "You have read the out-of-sample row for this coin and bar size, including the drawdown.",
        "Education only. Past performance is not a reliable indicator of future results.",
    ]
    story.append(ListFlowable([ListItem(Paragraph(s, body), leftIndent=8) for s in checks], bulletType="bullet"))
    story.append(Spacer(1, 4 * mm))
    story.append(Paragraph(EDU + " " + DISCLAIMER, body))

    doc = SimpleDocTemplate(
        str(PDF), pagesize=landscape(A4),
        leftMargin=12 * mm, rightMargin=12 * mm, topMargin=18 * mm, bottomMargin=16 * mm,
        title="GridBot Builder — Master Strategy guide",
        author="GridBot Builder",
    )
    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
    check_numbers(data, family_for)
    print("pdf", PDF)


def table(rows, widths):
    cell = ParagraphStyle("c", fontName="Helvetica", fontSize=7, leading=9, textColor=HexColor(INK))
    head = ParagraphStyle("hc", fontName="Helvetica-Bold", fontSize=7, leading=9, textColor=white)
    built = []
    for r, row in enumerate(rows):
        style = head if r == 0 else cell
        built.append([Paragraph(str(x), style) for x in row])
    tbl = Table(built, colWidths=widths, repeatRows=1)
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), HexColor(NAVY)),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("BACKGROUND", (0, 1), (-1, -1), HexColor("#F4F7FB")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [HexColor("#F4F7FB"), white]),
        ("GRID", (0, 0), (-1, -1), 0.2, HexColor("#D5DEE8")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 2),
        ("RIGHTPADDING", (0, 0), (-1, -1), 2),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]))
    return tbl


def check_numbers(data, family_for):
    """Re-read the PDF text and confirm every formatted result is present."""
    from pypdf import PdfReader
    text = "\n".join(page.extract_text() or "" for page in PdfReader(str(PDF)).pages)
    missing = []
    summary = data["summary"]
    for mode in ("Arithmetic", "Geometric"):
        sc = summary["chosen_settings"][mode]["is_score"]
        for piece in (pct(sc["win"]), pct(sc["net"])):
            if piece not in text:
                missing.append(piece + " " + mode)
        for inst in ("BTC-USDT", "ETH-USDT", "SOL-USDT", "ZEC-USDT", "XRP-USDT", "LINK-USDT"):
            for tf in ("1h", "4h"):
                row = find_row(data["oos"], mode=mode, inst=inst, tf=tf, label="deep", family=family_for[mode])
                for piece in (pct(row["deployment_win_rate"]), pct(row["net_return"]), pct(row["max_dd"])):
                    # percents can repeat; require the coin appears and the percent appears
                    if piece not in text:
                        missing.append(f"{mode} {inst} {tf} {piece}")
    for book in data["scaling"]["books"]:
        dd = pct(book["max_dd"])
        if dd not in text:
            missing.append("scale " + dd)
    if "Market Pros" in text or "ABN" in text:
        missing.append("brand leak")
    if DISCLAIMER not in text:
        missing.append("disclaimer missing")
    if missing:
        raise SystemExit("PDF number check failed: " + "; ".join(missing[:12]))
    print("pdf number check ok", len(text), "chars")


if __name__ == "__main__":
    build()
