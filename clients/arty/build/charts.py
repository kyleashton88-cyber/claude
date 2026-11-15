"""Plot every figure in Arty's plan. No external image generator.

Prices, candles and the wavy path are constructed here. They are teaching
drawings, not market data and not results.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager
from matplotlib.patches import FancyBboxPatch, Rectangle

from plan_math import (
    EXAMPLE_ATR,
    EXAMPLE_INTERVALS,
    EXAMPLE_MID,
    FEE_PER_SIDE,
    LOWER,
    MMR,
    SPAN,
    SPREAD,
    STEP,
    UPPER,
    EQUITY,
    EQUITY_AFTER,
    STOP_PCT,
    liq_distance,
    long_liq,
    short_liq,
)

ROOT = Path(__file__).resolve().parent
FONT = ROOT / "fonts" / "AtkinsonHyperlegible-Regular.ttf"
FONT_BOLD = ROOT / "fonts" / "AtkinsonHyperlegible-Bold.ttf"
CHARTS = ROOT / "charts"

INK = "#172033"
STEEL = "#1E3A5F"
STEEL_SOFT = "#3E6D99"
PALE = "#E7EEF3"
PAPER = "#F7F9FA"
SIGNAL = "#F0B429"
BURGUNDY = "#8E2F3A"
PINE = "#1E6B45"
LINE = "#C5D0D8"
MUTED = "#4E5E70"

# Content width of an A4 page with 14mm side margins, in inches.
WIDTH = 7.16


def _fonts() -> None:
    font_manager.fontManager.addfont(str(FONT))
    font_manager.fontManager.addfont(str(FONT_BOLD))
    plt.rcParams["font.family"] = "Atkinson Hyperlegible"
    plt.rcParams["axes.unicode_minus"] = False


def _badge(ax, text: str = "Example") -> None:
    ax.text(
        0.985,
        0.97,
        text,
        transform=ax.transAxes,
        ha="right",
        va="top",
        fontsize=8,
        color=INK,
        bbox={"boxstyle": "square,pad=0.28", "fc": SIGNAL, "ec": "none"},
        zorder=5,
    )


def _finish(fig, ax, title: str, xlabel: str, ylabel: str) -> None:
    ax.set_title(title, loc="left", color=STEEL, fontsize=12, pad=10, fontweight="bold")
    ax.set_xlabel(xlabel, color=INK, fontsize=9)
    ax.set_ylabel(ylabel, color=INK, fontsize=9)
    fig.tight_layout()


def _save(fig, name: str) -> Path:
    CHARTS.mkdir(parents=True, exist_ok=True)
    path = CHARTS / name
    fig.savefig(path, dpi=160, facecolor=fig.get_facecolor())
    plt.close(fig)
    return path


def _ax(fig, *args):
    ax = fig.add_subplot(*args)
    ax.set_facecolor(PAPER)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color("#8AA0B4")
    ax.tick_params(colors=INK, labelsize=8, length=3)
    ax.grid(axis="y", color="#E1E7EC", linewidth=0.7, zorder=0)
    return ax


def price_chart(cover: bool = False) -> Path:
    """Fictional path inside an example range, plus a full-scale liquidation strip."""
    x = np.arange(0, 72)
    price = EXAMPLE_MID + 78 * np.sin(x / 5.5) + 26 * np.sin(x / 2.15 + 0.4)
    # Keep the drawing inside the range so it cannot be read as a breakout result.
    price = np.clip(price, LOWER + 18, UPPER - 18)

    if cover:
        fig, ax = plt.subplots(figsize=(6.7, 2.85))
        fig.patch.set_facecolor("#FFFFFF")
        ax.set_facecolor("#FFFFFF")
    else:
        fig = plt.figure(figsize=(WIDTH, 5.15))
        fig.patch.set_facecolor("#FFFFFF")
        grid = fig.add_gridspec(2, 1, height_ratios=[3.15, 1.15], hspace=0.38)
        ax = fig.add_subplot(grid[0])
        ax2 = fig.add_subplot(grid[1])
        ax2.set_facecolor(PAPER)

    levels = [LOWER + i * STEP for i in range(EXAMPLE_INTERVALS + 1)]
    ax.axhspan(LOWER, UPPER, color="#E5F0F4", zorder=0)
    ax.axhspan(2945, 3055, color="#D5E4C8", alpha=0.55, zorder=0)
    for level in levels:
        ax.axhline(level, color=STEEL_SOFT, linewidth=0.6, alpha=0.85, zorder=1)
    ax.axhline(LOWER, color=STEEL, linewidth=1.3, zorder=2)
    ax.axhline(UPPER, color=STEEL, linewidth=1.3, zorder=2)
    ax.plot(x, price, color=INK, linewidth=1.35, zorder=3)
    launch_at = int(np.argmin(np.abs(price - EXAMPLE_MID)))
    ax.scatter([launch_at], [price[launch_at]], s=36, color=SIGNAL, zorder=4, edgecolors=INK, linewidths=0.4)

    if cover:
        ax.set_xlim(-1, 72)
        ax.set_ylim(LOWER - 25, UPPER + 25)
        ax.set_yticks([LOWER, EXAMPLE_MID, UPPER])
        ax.set_yticklabels(["2,835", "3,000", "3,165"])
        ax.set_xticks([])
        ax.tick_params(colors=INK, labelsize=8, length=0)
        for side in ("top", "right"):
            ax.spines[side].set_visible(False)
        ax.spines["left"].set_color("#8AA0B4")
        ax.spines["bottom"].set_color("#8AA0B4")
        ax.set_title("Example range, fictional prices", loc="left", color=STEEL, fontsize=11, pad=6)
        ax.text(0.99, 0.08, "Example", transform=ax.transAxes, ha="right", va="bottom", fontsize=8,
                color=INK, bbox={"boxstyle": "square,pad=0.25", "fc": SIGNAL, "ec": "none"})
        fig.tight_layout(pad=0.35)
        return _save(fig, "cover_range.png")

    ax.annotate(
        "Example launch dot.\nMiddle third only.",
        xy=(launch_at, price[launch_at]),
        xytext=(max(2, launch_at - 22), 2862),
        fontsize=7.5,
        color=INK,
        arrowprops={"arrowstyle": "-", "color": INK, "lw": 0.6},
        ha="left",
    )
    ax.text(
        2,
        3238,
        "A 4H close above 3,165 ends the bot. This path stays inside on purpose.",
        fontsize=7.5,
        color=BURGUNDY,
        ha="left",
    )
    ax.set_xlim(-1, 73)
    ax.set_ylim(2780, 3285)
    ax.set_yticks([2835, 2945, 3000, 3055, 3165])
    ax.set_xticks([0, 24, 48, 71])
    ax.set_xticklabels(["1", "25", "49", "72"])
    _badge(ax)
    ax.set_title(
        "Example grid: 12 arithmetic intervals on a fictional path",
        loc="left",
        color=STEEL,
        fontsize=12,
        pad=8,
    )
    ax.set_ylabel("Example price, USDT", color=INK, fontsize=9)
    ax.set_xlabel("Example bar number, not a date", color=INK, fontsize=9)
    ax.tick_params(colors=INK, labelsize=8)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.spines["left"].set_color("#8AA0B4")
    ax.spines["bottom"].set_color("#8AA0B4")

    # Full scale so liquidation is visible, not cropped off a zoomed chart.
    ax2.set_xlim(1700, 4400)
    ax2.set_ylim(0, 1)
    ax2.set_yticks([])
    ax2.axvspan(LOWER, UPPER, color="#E5F0F4", zorder=0)
    ax2.plot([LOWER, UPPER], [0.55, 0.55], color=STEEL, linewidth=8, solid_capstyle="butt", zorder=2)
    ax2.text((LOWER + UPPER) / 2, 0.70, "Grid range\n2,835 to 3,165", ha="center", va="bottom", fontsize=7, color=STEEL)
    marks = (
        (long_liq(EXAMPLE_MID, 3), "3× long  2,015", BURGUNDY, 0.34, "top"),
        (long_liq(EXAMPLE_MID, 5), "5× long  2,415", "#A35B2B", 0.72, "bottom"),
        (short_liq(EXAMPLE_MID, 5), "5× short  3,585", "#A35B2B", 0.72, "bottom"),
        (short_liq(EXAMPLE_MID, 3), "3× short  3,985", BURGUNDY, 0.34, "top"),
    )
    for price_mark, label, color, text_y, valign in marks:
        ax2.plot([price_mark, price_mark], [0.42, 0.66], color=color, linewidth=1.2, zorder=3)
        ax2.text(price_mark, text_y, label, ha="center", va=valign, fontsize=7, color=color)
    ax2.set_xticks([2000, 3000, 4000])
    ax2.set_xlabel("Example price, USDT. Maintenance assumption 0.50%. Not a live quote.", color=INK, fontsize=9)
    ax2.set_title(
        "Same example, zoomed out: liquidation sits outside the range",
        loc="left",
        color=STEEL,
        fontsize=11,
        pad=6,
    )
    ax2.tick_params(colors=INK, labelsize=8)
    for side in ("top", "right", "left"):
        ax2.spines[side].set_visible(False)
    ax2.spines["bottom"].set_color("#8AA0B4")
    fig.subplots_adjust(hspace=0.55, left=0.10, right=0.98, top=0.90, bottom=0.10)
    return _save(fig, "price_grid.png")


def sizing_chart() -> Path:
    fig = plt.figure(figsize=(WIDTH, 3.35))
    fig.patch.set_facecolor("#FFFFFF")
    left = fig.add_subplot(1, 2, 1)
    right = fig.add_subplot(1, 2, 2)
    for ax in (left, right):
        ax.set_facecolor(PAPER)
        for side in ("top", "right"):
            ax.spines[side].set_visible(False)
        ax.spines["left"].set_color("#8AA0B4")
        ax.spines["bottom"].set_color("#8AA0B4")
        ax.tick_params(colors=INK, labelsize=8)
        ax.grid(axis="x", color="#E1E7EC", linewidth=0.7)

    labels = ["Money in the bot (10%)", "If the −8% close fills", "If the +4.8% close fills"]
    values = [50, 4, 2.4]
    colors = [STEEL_SOFT, BURGUNDY, PINE]
    y = np.arange(len(labels))[::-1]
    left.barh(y, values, color=colors, height=0.55, zorder=2)
    for yi, value in zip(y, values):
        left.text(value + 1.6, yi, f"{value:,.2f} USDT", va="center", fontsize=8, color=INK)
    left.set_yticks(y)
    left.set_yticklabels(labels, fontsize=8)
    left.set_xlim(0, 78)
    left.set_xlabel("USDT, from a 500.00 account", color=INK, fontsize=9)
    left.set_title("Where a stopped bot sits", loc="left", color=STEEL, fontsize=11, pad=8)
    _badge(left)

    labels2 = ["Phase-in stop\n(5% of 5,000)", "Later stop\n(10% of 5,000)", "Week limit\nat 5,000", "Hard halt\nat 5,000"]
    values2 = [20, 40, 150, 750]
    colors2 = [BURGUNDY, BURGUNDY, SIGNAL, BURGUNDY]
    y2 = np.arange(len(labels2))[::-1]
    right.barh(y2, values2, color=colors2, height=0.62, zorder=2)
    for yi, value in zip(y2, values2):
        right.text(value + 12, yi, f"{value:,.2f}", va="center", fontsize=8, color=INK)
    right.set_yticks(y2)
    right.set_yticklabels(labels2, fontsize=8)
    right.set_xlim(0, 980)
    right.set_xlabel("USDT. Example only, not a forecast.", color=INK, fontsize=9)
    right.set_title("Deposit case, result still zero", loc="left", color=STEEL, fontsize=11, pad=8)
    fig.tight_layout()
    return _save(fig, "sizing.png")


def leverage_chart() -> Path:
    levers = [2, 3, 4, 5, 10]
    dist = [liq_distance(lev) * 100 for lev in levers]
    fig, ax = plt.subplots(figsize=(WIDTH, 3.25))
    fig.patch.set_facecolor("#FFFFFF")
    ax.set_facecolor(PAPER)
    colors = []
    for lev in levers:
        if lev == 3:
            colors.append(STEEL)
        elif lev == 5:
            colors.append("#A35B2B")
        elif lev == 10:
            colors.append("#C5CDD4")
        else:
            colors.append(STEEL_SOFT)
    bars = ax.bar([str(lev) + "×" for lev in levers], dist, color=colors, width=0.72, zorder=2)
    for bar, value in zip(bars, dist):
        ax.text(bar.get_x() + bar.get_width() / 2, value + 0.8, f"{value:.2f}%", ha="center", fontsize=8, color=INK)
    ax.axhline(5.5, color=PINE, linewidth=1, linestyle=(0, (3, 2)))
    ax.set_ylim(0, 58)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.spines["left"].set_color("#8AA0B4")
    ax.spines["bottom"].set_color("#8AA0B4")
    ax.tick_params(colors=INK, labelsize=8)
    ax.grid(axis="y", color="#E1E7EC", linewidth=0.7)
    ax.set_title(
        "How far a fully built position can move before liquidation",
        loc="left",
        color=STEEL,
        fontsize=12,
        pad=8,
    )
    ax.set_xlabel(
        "Leverage. 4× shows the shape only. 10× is not used.\nDashed line: half of the 11% example range (5.50%).",
        color=INK,
        fontsize=9,
    )
    ax.set_ylabel("Adverse distance, percent of price", color=INK, fontsize=9)
    _badge(ax, "Example, 0.50% maintenance")
    fig.tight_layout()
    return _save(fig, "leverage.png")


def limits_chart() -> Path:
    labels = ["Week\n−3%", "Four-week window\n−6%", "Soft halt\n−10%", "Hard halt\n−15%"]
    at_500 = [15, 30, 50, 75]
    at_5000 = [150, 300, 500, 750]
    y = np.arange(len(labels))
    fig, ax = plt.subplots(figsize=(WIDTH, 3.15))
    fig.patch.set_facecolor("#FFFFFF")
    ax.set_facecolor(PAPER)
    h = 0.36
    ax.barh(y + h / 2, at_500, height=h, color=STEEL, label="Baseline 500.00 USDT", zorder=2)
    ax.barh(y - h / 2, at_5000, height=h, color=SIGNAL, label="Example after a 4,500.00 deposit, result unchanged", zorder=2)
    for yi, a, b in zip(y, at_500, at_5000):
        ax.text(
            a + 6,
            yi + h / 2,
            f"{a:.2f}",
            va="center",
            fontsize=7.5,
            color=INK,
            bbox={"fc": "white", "ec": "none", "pad": 0.15},
            zorder=3,
        )
        ax.text(b + 8, yi - h / 2, f"{b:.2f}", va="center", fontsize=7.5, color=INK, zorder=3)
    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=8)
    ax.set_xlabel("Loss that triggers the rung, USDT", color=INK, fontsize=9)
    ax.set_xlim(0, 980)
    ax.legend(frameon=False, fontsize=8, loc="upper center", bbox_to_anchor=(0.42, -0.22), ncol=2)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.spines["left"].set_color("#8AA0B4")
    ax.spines["bottom"].set_color("#8AA0B4")
    ax.tick_params(colors=INK, labelsize=8)
    ax.grid(axis="x", color="#E1E7EC", linewidth=0.7)
    ax.set_title("Circuit-breaker ladder, in USDT", loc="left", color=STEEL, fontsize=12, pad=8)
    fig.subplots_adjust(left=0.16, right=0.98, top=0.86, bottom=0.28)
    return _save(fig, "limits.png")


def fee_chart() -> Path:
    gross = np.linspace(0.15, 1.40, 200)
    # USDT left on a 12.50 order after the planning-assumption round trip.
    cost = (2 * FEE_PER_SIDE + SPREAD) * 100
    net_pct = gross - cost
    net_usd = 12.50 * net_pct / 100
    fig, ax = plt.subplots(figsize=(WIDTH, 3.35))
    fig.patch.set_facecolor("#FFFFFF")
    ax.set_facecolor(PAPER)
    ax.axvspan(0.15, 0.50, color="#F6E4E2", zorder=0)
    ax.plot(gross, net_usd, color=STEEL, linewidth=2, zorder=2)
    ax.axhline(0, color=BURGUNDY, linewidth=0.8)
    ax.axvline(0.876494, color=SIGNAL, linewidth=1.3)
    worst_net = 12.50 * (0.876494023904 - cost) / 100
    ax.scatter([0.876494], [worst_net], color=SIGNAL, s=28, zorder=3, edgecolors=INK, linewidths=0.4)
    ax.annotate(
        "Example top band, 0.876% gross",
        xy=(0.876, worst_net),
        xytext=(0.52, 0.128),
        fontsize=7.5,
        color=INK,
        arrowprops={"arrowstyle": "-", "color": INK, "lw": 0.6},
    )
    ax.text(0.20, 0.105, "Fails the\n0.50% floor", color=BURGUNDY, fontsize=7.5)
    ax.set_xlim(0.15, 1.45)
    ax.set_ylim(-0.015, 0.195)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.spines["left"].set_color("#8AA0B4")
    ax.spines["bottom"].set_color("#8AA0B4")
    ax.tick_params(colors=INK, labelsize=8)
    ax.grid(color="#E1E7EC", linewidth=0.7)
    ax.set_title(
        "What one completed grid keeps after example fees",
        loc="left",
        color=STEEL,
        fontsize=12,
        pad=8,
    )
    ax.set_xlabel("Gross spacing, percent of the band's lower price", color=INK, fontsize=9)
    ax.set_ylabel("USDT left on a 12.50 order", color=INK, fontsize=9)
    _badge(ax, "Example fees 0.12% round trip")
    fig.tight_layout()
    return _save(fig, "fees.png")


def range_schematic() -> Path:
    """Synthetic daily candles with the swing, ATR buffer and middle third."""
    rng = np.random.default_rng(11)
    closes = []
    price = 3000.0
    for i in range(18):
        price += float(rng.normal(0, 18))
        price = min(3105, max(2895, price))
        closes.append(price)
    # Force a visible swing low and swing high inside the series.
    closes[3] = 2878
    closes[11] = 3122
    closes[16] = 2994

    fig, ax = plt.subplots(figsize=(WIDTH, 3.45))
    fig.patch.set_facecolor("#FFFFFF")
    ax.set_facecolor(PAPER)
    ax.axhspan(LOWER, UPPER, color="#E5F0F4", zorder=0)
    ax.axhspan(2945, 3055, color="#D5E4C8", alpha=0.5, zorder=0)
    ax.axhline(2865, color=STEEL_SOFT, linewidth=0.8, linestyle=(0, (2, 2)))
    ax.axhline(3135, color=STEEL_SOFT, linewidth=0.8, linestyle=(0, (2, 2)))
    ax.axhline(LOWER, color=STEEL, linewidth=1.2)
    ax.axhline(UPPER, color=STEEL, linewidth=1.2)
    for i, close in enumerate(closes):
        high = close + float(rng.uniform(8, 22))
        low = close - float(rng.uniform(8, 22))
        if i == 3:
            low, high, close = 2865, 2925, 2878
        if i == 11:
            low, high, close = 3060, 3135, 3122
        open_ = closes[i - 1] if i else 3000
        color = PINE if close >= open_ else BURGUNDY
        ax.plot([i, i], [low, high], color=color, linewidth=1)
        body_low = min(open_, close)
        ax.add_patch(
            Rectangle((i - 0.28, body_low), 0.56, abs(close - open_) or 2, facecolor=color, edgecolor=color, zorder=3)
        )
    ax.set_xlim(-0.8, 18.6)
    ax.set_ylim(2760, 3240)
    ax.set_xticks([0, 3, 11, 17])
    ax.set_xticklabels(["Day 1", "Swing low", "Swing high", "Day 18"])
    ax.set_ylabel("Example price, USDT", color=INK, fontsize=9)
    ax.set_xlabel("Example daily candles, not a real month", color=INK, fontsize=9)
    ax.text(17.4, 2865, "Swing 2,865", ha="right", va="bottom", fontsize=7, color=STEEL)
    ax.text(17.4, LOWER - 8, "Lower 2,835  (−0.5 ATR)", ha="right", va="top", fontsize=7, color=STEEL)
    ax.text(17.4, 3135, "Swing 3,135", ha="right", va="bottom", fontsize=7, color=STEEL)
    ax.text(0.2, 3188, "Upper 3,165  (+0.5 ATR of 60)", fontsize=7, color=STEEL)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.spines["left"].set_color("#8AA0B4")
    ax.spines["bottom"].set_color("#8AA0B4")
    ax.tick_params(colors=INK, labelsize=8)
    ax.set_title(
        "How the example range is built from swings plus half an ATR",
        loc="left",
        color=STEEL,
        fontsize=12,
        pad=8,
    )
    _badge(ax)
    fig.tight_layout()
    return _save(fig, "range_build.png")


def _box(ax, x, y, w, h, text, face, edge=INK, size=7.4):
    patch = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle="square,pad=0",
        facecolor=face,
        edgecolor=edge,
        linewidth=0.8,
    )
    ax.add_patch(patch)
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=size, color=INK, wrap=True)


def launch_flow() -> Path:
    fig, ax = plt.subplots(figsize=(WIDTH, 2.95))
    fig.patch.set_facecolor("#FFFFFF")
    ax.set_xlim(0, 160)
    ax.set_ylim(0, 48)
    ax.axis("off")
    fig.suptitle(
        "Pre-launch gate. Any no means no bot.",
        x=0.012,
        ha="left",
        color=STEEL,
        fontsize=12,
        fontweight="bold",
    )
    labels = ["Pair and\ncount", "Halt and\nsize", "Range", "Fees and\nbook", "Liquidation\nbuffer", "Journal\nfilled"]
    xs = [1, 23, 45, 67, 89, 111]
    for i, (x, text) in enumerate(zip(xs, labels)):
        _box(ax, x, 26, 18, 14, text, "#E7EEF3", STEEL, 7)
        ax.annotate(
            "",
            xy=(x + 9, 14.3),
            xytext=(x + 9, 25.4),
            arrowprops={"arrowstyle": "-|>", "color": BURGUNDY, "lw": 0.7},
        )
        if i < len(xs) - 1:
            ax.annotate(
                "",
                xy=(xs[i + 1] - 0.3, 33),
                xytext=(x + 18.3, 33),
                arrowprops={"arrowstyle": "-|>", "color": STEEL, "lw": 0.8},
            )
            ax.text((x + 18.3 + xs[i + 1]) / 2, 35.2, "yes", ha="center", fontsize=6.5, color=PINE)
    _box(
        ax,
        1,
        2,
        129,
        12,
        "No on any box: do not launch. Log the failed check number.",
        "#F6E4E2",
        BURGUNDY,
        7.6,
    )
    _box(ax, 138, 26, 20, 14, "Launch", "#D5E4C8", PINE, 8.5)
    ax.annotate(
        "",
        xy=(137.6, 33),
        xytext=(129.4, 33),
        arrowprops={"arrowstyle": "-|>", "color": PINE, "lw": 0.8},
    )
    ax.text(133.4, 35.2, "yes", ha="center", fontsize=6.5, color=PINE)
    fig.tight_layout(rect=(0, 0, 1, 0.90))
    return _save(fig, "launch_flow.png")


def pause_tree() -> Path:
    fig, ax = plt.subplots(figsize=(WIDTH, 4.35))
    fig.patch.set_facecolor("#FFFFFF")
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 108)
    ax.axis("off")
    fig.suptitle(
        "When an open bot is closed. Check from the top.",
        x=0.012,
        ha="left",
        color=STEEL,
        fontsize=12,
        fontweight="bold",
    )
    _box(ax, 16, 96, 36, 8, "A bot is open", "#E7EEF3", STEEL, 8)
    rows = [
        "A listed event is inside the next 2 hours",
        "A 4H candle closed outside the range",
        "One 1H or 4H candle moved 8% or more",
        "Funding paid clears the funding rule",
        "1H ATR is over 2.5%, or one 1H range is over 3%",
        "Page stuck 15 minutes, or an exchange outage",
        "7 days with under 3 round trips, or 14 days open",
    ]
    top = 84
    for i, text in enumerate(rows):
        y = top - i * 10
        _box(ax, 3, y, 64, 8, text, "#FFFFFF", "#8AA0B4", 7)
        ax.annotate(
            "",
            xy=(78, y + 4),
            xytext=(67.2, y + 4),
            arrowprops={"arrowstyle": "-|>", "color": BURGUNDY, "lw": 0.7},
        )
    _box(ax, 78, 24, 20, 68, "Yes\n\nClose\nthe bot", "#F6E4E2", BURGUNDY, 8)
    _box(
        ax,
        3,
        2,
        95,
        10,
        "If every row is no: do not edit the bot. The daily check still happens.",
        "#D5E4C8",
        PINE,
        7.4,
    )
    fig.tight_layout(rect=(0, 0, 1, 0.93))
    return _save(fig, "pause_tree.png")


def roadmap() -> Path:
    fig, ax = plt.subplots(figsize=(WIDTH, 2.55))
    fig.patch.set_facecolor("#FFFFFF")
    ax.set_xlim(0, 4)
    ax.set_ylim(0, 1)
    ax.axis("off")
    blocks = [
        (0, STEEL, "Week 1", "ETH/USDT only\nOne bot\nDaily check, 7 days"),
        (1, "#2C5282", "Week 2", "Same pair\nWrite the live\nfee and spread"),
        (2, "#3E6D99", "Week 3", "A second pair\nonly if the card\nsays yes"),
        (3, "#8A6A2F", "Week 4", "Review first\nDeposit is a\nseparate decision"),
    ]
    for i, (x, color, title, body) in enumerate(blocks):
        ax.add_patch(Rectangle((x + 0.06, 0.18), 0.88, 0.74, facecolor=color, edgecolor="none"))
        ax.text(x + 0.5, 0.78, title, ha="center", va="center", color="white", fontsize=10)
        ax.text(x + 0.5, 0.46, body, ha="center", va="center", color="white", fontsize=7.4)
        if i < 3:
            ax.annotate("", xy=(x + 1.05, 0.55), xytext=(x + 0.96, 0.55),
                        arrowprops={"arrowstyle": "-|>", "color": INK, "lw": 0.8})
    ax.set_title("Four weeks. Process only. No balance to aim at.", loc="left", color=STEEL, fontsize=12, pad=6)
    fig.tight_layout()
    return _save(fig, "roadmap.png")


def build_all() -> list[Path]:
    _fonts()
    # Silence the unused import if a helper is not called.
    _ = (EXAMPLE_ATR, SPAN)
    return [
        price_chart(cover=True),
        price_chart(cover=False),
        sizing_chart(),
        leverage_chart(),
        limits_chart(),
        fee_chart(),
        range_schematic(),
        launch_flow(),
        pause_tree(),
        roadmap(),
    ]


if __name__ == "__main__":
    for path in build_all():
        print(path)
