#!/usr/bin/env python3
"""Render P0 ATLAS pages from sites/atlas/content and patch the existing shell."""
from __future__ import annotations

import hashlib
import html
import json
import math
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content"
DATA = ROOT / "data"

WARNING = (
    '<p class="atlas-general-warning">General information only, published by Market Pros Pty Ltd '
    "([ABN — placeholder]). Not personal financial advice. Consider your own circumstances. "
    'Contact <a href="mailto:contact@stewartcrowncrypto.com">contact@stewartcrowncrypto.com</a> '
    "(pending Stewart's confirmation). Examples are hypothetical unless a public data feed is named. "
    "Past prices do not indicate future results.</p>"
)

HEADER = r'''<a class="skip-link" href="#main-content">Skip to main content</a>
<header class="atlas-unified-header" data-atlas-header>
  <div class="atlas-unified-header__inner">
    <a class="atlas-unified-brand" href="/" aria-label="ATLAS home">
      <span class="atlas-unified-brand__mark">ATLAS</span>
      <span class="atlas-unified-brand__descriptor">The Universal Trading Library</span>
    </a>
    <button class="atlas-mobile-toggle" type="button" aria-label="Open navigation" aria-expanded="false" aria-controls="primary-navigation" data-nav-toggle>☰</button>
    <nav class="atlas-unified-nav" id="primary-navigation" aria-label="Primary navigation" data-primary-nav>
      <ul class="atlas-unified-nav-list">
        <li class="atlas-unified-nav-item">
          <button class="atlas-unified-trigger" type="button" aria-haspopup="true" aria-expanded="false" aria-controls="markets-menu">Markets</button>
          <div class="atlas-unified-dropdown" id="markets-menu" hidden>
            <a href="/#live-markets">Market Overview</a><a href="/markets/btc">Bitcoin</a><a href="/markets/eth">Ethereum</a><a href="/markets/sol">Solana</a><a href="/markets/bnb">BNB</a><a href="/exchanges">Exchanges</a>
          </div>
        </li>
        <li class="atlas-unified-nav-item">
          <button class="atlas-unified-trigger" type="button" aria-haspopup="true" aria-expanded="false" aria-controls="academy-menu">Academy</button>
          <div class="atlas-unified-dropdown" id="academy-menu" hidden>
            <a href="/academy">Academy Overview</a><a href="/academy/beginner">Crypto Fundamentals</a><a href="/market-structure">Market Structure</a><a href="/technical-analysis">Technical Analysis</a><a href="/risk-academy">Risk Academy</a><a href="/futures-leverage">Futures &amp; Leverage</a>
          </div>
        </li>
        <li class="atlas-unified-nav-item">
          <button class="atlas-unified-trigger" type="button" aria-haspopup="true" aria-expanded="false" aria-controls="tools-menu">Tools</button>
          <div class="atlas-unified-dropdown" id="tools-menu" hidden>
            <a href="/tools">All Tools</a><a href="/tools/grid-bot">Grid Calculator</a><a href="/journal-lab">Journal Analyser</a><a href="/tools/risk-calc">Risk / Position Size</a><a href="/tools/replay-lab">Replay Lab</a><a href="/macro-lab">Macro &amp; Intermarket</a>
          </div>
        </li>
        <li class="atlas-unified-nav-item">
          <button class="atlas-unified-trigger" type="button" aria-haspopup="true" aria-expanded="false" aria-controls="library-menu">Library</button>
          <div class="atlas-unified-dropdown" id="library-menu" hidden>
            <a href="/library">Library Overview</a><a href="/library#by-topic">A–Z</a><a href="/library#by-level">By level</a><a href="/library#by-question">By question</a><a href="/glossary">Glossary</a>
          </div>
        </li>
        <li><a href="/glossary">Glossary</a></li>
        <li><a href="/learning-path">Learning Path</a></li>
        <li><a href="/community">Community</a></li>
      </ul>
      <div class="atlas-unified-actions">
        <div class="atlas-global-progress" aria-label="Learning progress"><span>Progress</span><strong data-global-progress>0%</strong></div>
        <form class="atlas-header-search" action="/search" method="get" role="search">
          <label class="visually-hidden" for="atlasHeaderSearch">Search the library</label>
          <input id="atlasHeaderSearch" name="q" type="search" placeholder="Search" autocomplete="off" data-atlas-search-input>
        </form>
        <a class="atlas-search-button" href="/search" aria-label="Search ATLAS">⌕</a>
        <a class="atlas-start-learning" href="/learning-path">Start Learning</a>
      </div>
    </nav>
  </div>
</header>'''

# slugified heading -> section id, plus extra alias ids
ANCHOR = {
    "market-structure.md": {
        "candles": ("candles", []),
        "swings": ("swings", []),
        "trend-and-range": ("trend", ["ranges"]),
        "break-of-structure-and-change-of-character": ("bos-choch", []),
        "liquidity": ("liquidity", []),
        "order-blocks-and-fair-value-gaps": ("order-blocks", ["fvg"]),
        "multi-timeframe-work": ("multi-timeframe", []),
    },
    "technical-analysis.md": {
        "support-and-resistance": ("support-resistance", []),
        "trendlines": ("trendlines", []),
        "simple-moving-average": ("ema-sma", []),
        "rsi": ("rsi", []),
        "macd": ("macd", []),
        "vwap": ("vwap", []),
        "bollinger-bands": ("bollinger", []),
        "atr": ("atr", []),
        "volume": ("volume", []),
        "patterns": ("patterns", []),
        "divergence": ("divergence", []),
        "confluence": ("confluence", []),
    },
    "risk-academy.md": {
        "position-sizing": ("position-sizing", []),
        "r-multiples": ("r-multiple", []),
        "stops": ("stop-placement", []),
        "expectancy": ("expectancy", []),
        "drawdown-and-the-recovery-fraction": ("drawdown", []),
        "monte-carlo": ("monte-carlo", []),
        "a-pre-trade-check": ("pre-trade", ["correlation", "leverage-risk"]),
    },
    "exchanges.md": {
        "centralised-and-decentralised-venues": ("cex", ["dex"]),
        "the-order-book-the-spread-and-depth": ("order-book", ["spread-depth"]),
        "maker-and-taker": ("maker-taker", []),
        "order-types": ("order-types", []),
        "registration-in-australia-as-general-information": ("kyc-au", ["proof-of-reserves", "withdrawals"]),
    },
    "security.md": {
        "wallets": ("wallet-types", ["hardware"]),
        "seed-phrases-and-keys": ("seed-phrase", ["2fa", "exchange-account"]),
        "a-short-encyclopedia-of-scams": ("scams", ["approvals"]),
        "where-to-report": ("report-au", []),
    },
    "crypto-fundamentals.md": {
        "a-shared-ledger": ("what-is-blockchain", ["blocks"]),
        "transactions": ("transactions", ["mempool"]),
        "consensus": ("consensus", ["pow-pos"]),
        "coins-tokens-and-categories": ("coins-vs-tokens", ["token-categories", "market-cap"]),
        "networks-fees-and-scaling": ("networks", []),
        "what-the-chart-does-not-show": ("liquidity", ["halving"]),
    },
}

MD_PAGE = {
    "market-structure.md": ("/market-structure", "Academy 02 · 07 · 08", "market-structure.html"),
    "technical-analysis.md": ("/technical-analysis", "Academy 03 · 06", "technical-analysis.html"),
    "risk-academy.md": ("/risk-academy", "Academy 04", "risk-academy.html"),
    "exchanges.md": ("/exchanges", "Venues and orders", "exchanges.html"),
    "security.md": ("/security", "Wallets and scams", "security.html"),
    "crypto-fundamentals.md": ("/crypto-fundamentals", "Academy 13", "crypto-fundamentals.html"),
    "terms.md": ("/terms", "Legal · draft", "terms.html"),
    "privacy.md": ("/privacy", "Legal · draft", "privacy.html"),
    "disclaimer.md": ("/disclaimer", "Legal · draft", "disclaimer.html"),
}


def slug(text: str) -> str:
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", text.lower())).strip("-")


def inline(text: str) -> str:
    safe = html.escape(text.strip())
    safe = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", safe)
    safe = re.sub(r"`([^`]+)`", r"<code>\1</code>", safe)
    def link(match: re.Match) -> str:
        label, href = match.group(1), match.group(2)
        if href.startswith("http"):
            return f'<a href="{href}">{label}</a>'
        href = re.sub(r"\.md(?=#|$)", "", href)
        if not href.startswith("/"):
            href = "/" + href
        return f'<a href="{href}">{label}</a>'
    safe = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", link, safe)
    safe = safe.replace("[ABN]", "[ABN — placeholder]")
    safe = safe.replace("[EFFECTIVE_DATE]", "[effective date — placeholder]")
    safe = safe.replace("[PRIVACY_CONTACT]", "contact@stewartcrowncrypto.com (pending Stewart's confirmation)")
    safe = re.sub(
        r"\[CONTACT_EMAIL:[^\]]+\]",
        '<a href="mailto:contact@stewartcrowncrypto.com">contact@stewartcrowncrypto.com</a> (pending Stewart\'s confirmation)',
        safe,
    )
    return safe


def render_markdown(name: str, body: str) -> tuple[str, list[tuple[str, str]]]:
    rules = ANCHOR.get(name, {})
    lines = body.splitlines()
    out: list[str] = []
    toc: list[tuple[str, str]] = []
    i = 0
    section = False

    def close() -> None:
        nonlocal section
        if section:
            out.append("</section>")
            section = False

    while i < len(lines):
        line = lines[i]
        if line.startswith("```"):
            buf = []
            i += 1
            while i < len(lines) and not lines[i].startswith("```"):
                buf.append(lines[i])
                i += 1
            i += 1
            out.append("<pre>" + html.escape("\n".join(buf)) + "</pre>")
            continue
        if line.startswith("# "):
            i += 1
            continue
        if line.startswith("## "):
            close()
            title = line[3:].strip()
            key = slug(title)
            sec_id, aliases = rules.get(key, (key, []))
            toc.append((sec_id, title))
            alias = "".join(f'<span id="{html.escape(a)}"></span>' for a in aliases)
            out.append(f'<section class="section" id="{html.escape(sec_id)}">{alias}<h2>{inline(title)}</h2>')
            section = True
            i += 1
            continue
        if line.startswith("### "):
            out.append(f"<h3>{inline(line[4:].strip())}</h3>")
            i += 1
            continue
        if line.startswith("- "):
            items = []
            while i < len(lines) and lines[i].startswith("- "):
                items.append("<li>" + inline(lines[i][2:]) + "</li>")
                i += 1
            out.append("<ul>" + "".join(items) + "</ul>")
            continue
        if re.match(r"\d+\. ", line):
            items = []
            while i < len(lines) and re.match(r"\d+\. ", lines[i]):
                items.append("<li>" + inline(re.sub(r"^\d+\. ", "", lines[i])) + "</li>")
                i += 1
            out.append("<ol>" + "".join(items) + "</ol>")
            continue
        if not line.strip():
            i += 1
            continue
        if line.startswith("DRAFT"):
            out.append(f'<p class="draft-banner">{inline(line)}</p>')
            i += 1
            continue
        buf = [line.strip()]
        i += 1
        while i < len(lines) and lines[i].strip() and not lines[i].startswith(("#", "- ", "```")) and not re.match(r"\d+\. ", lines[i]):
            buf.append(lines[i].strip())
            i += 1
        text = " ".join(buf)
        if text.lower().startswith("hypothetical example"):
            out.append(f'<p class="atlas-note">{inline(text)}</p>')
        else:
            out.append("<p>" + inline(text) + "</p>")
    close()
    return "\n".join(out), toc


def split_front(text: str) -> tuple[str, str]:
    if not text.startswith("---"):
        return "", text
    end = text.find("\n---", 3)
    return text[:end], text[end + 4 :].lstrip("\n")


def lede_of(body: str) -> str:
    for line in body.splitlines():
        if line.startswith("#") or not line.strip() or line.startswith("DRAFT") or line.startswith("**"):
            continue
        return re.sub(r"\[(.+?)\]\([^)]+\)", r"\1", line.strip())
    return ""


def page(title: str, description: str, kicker: str, lede: str, body: str, toc: list[tuple[str, str]], scripts: list[str], crumb_label: str) -> str:
    toc_html = "".join(f'<a href="#{html.escape(i)}">{html.escape(t)}</a>' for i, t in toc)
    lesson = (
        f'<div class="atlas-lesson"><nav class="atlas-toc" aria-label="On this page"><p>On this page</p>{toc_html}</nav><div class="atlas-lesson__body">{body}</div></div>'
        if toc else body
    )
    script_tags = "\n".join(f'<script src="{html.escape(src)}"></script>' for src in scripts)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<link rel="icon" href="/favicon.svg" type="image/svg+xml"/>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>{html.escape(title)} — ATLAS</title>
<meta name="description" content="{html.escape(description)}"/>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin=""/>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&amp;family=Inter:wght@400;500;600;700&amp;family=Space+Grotesk:wght@500;600;700&amp;display=swap" rel="stylesheet"/>
<link href="/assets/site.css" rel="stylesheet"/>
<link rel="stylesheet" href="/assets/atlas-production.css"/>
<link rel="stylesheet" href="/assets/atlas-completed.css"/>
<link rel="stylesheet" href="/assets/atlas-layout-hardening.css"/>
<link rel="stylesheet" href="/assets/atlas-deep-layout-fixes.css"/>
<link rel="stylesheet" href="/assets/atlas-quality-fixes.css"/>
<link rel="stylesheet" href="/assets/atlas-library.css"/>
</head>
<body class="atlas-unified">
{HEADER}
<div class="unified-breadcrumb no-print"><a href="/">ATLAS</a><span>›</span><strong>{html.escape(crumb_label)}</strong></div>
<main id="main-content">
<section class="pagehero"><div class="kicker">{html.escape(kicker)}</div><h1 id="page-title">{html.escape(title)}</h1><p>{html.escape(lede)}</p></section>
{lesson}
</main>
<footer class="footer"><div><b>ATLAS — The Universal Trading Library</b><br/>One library. Every market. A smarter you.</div>
<nav><a href="/library">Library</a><a href="/glossary">Glossary</a><a href="/tools">Tools</a><a href="/academy">Academy</a></nav>
<nav aria-label="Legal" class="legal"><a href="/privacy">Privacy</a><a href="/terms">Terms</a><a href="/disclaimer">Disclaimer</a><a href="/contact">Contact</a></nav>
{WARNING}</footer>
<button aria-label="Back to top" class="backtop" type="button">↑</button>
<script src="/assets/atlas-config.js"></script>
<script src="/assets/site.js"></script>
{script_tags}
</body>
</html>
"""


def placeholder(src: str, caption: str) -> str:
    return (
        f'<figure class="atlas-ph" data-asset="{html.escape(src)}" data-alt="{html.escape(caption)}">'
        f'<div class="atlas-ph__box" role="img" aria-label="Image placeholder. Creative Studio has not landed {html.escape(src)}.">'
        f"<strong>Image placeholder</strong><span>{html.escape(src)}</span>"
        f"<span>Awaiting Creative Studio. This build does not invent the still.</span></div>"
        f"<figcaption>{html.escape(caption)}</figcaption></figure>"
    )


CHART = (
    '<div data-atlas-chart data-symbol="BTCUSDT" data-tf="1h" data-overlays="ema20,sma50,bb20,vwap" '
    'data-pane="rsi" data-controls></div>'
)
CHART_SWINGS = (
    '<div data-atlas-chart data-symbol="BTCUSDT" data-tf="1h" data-overlays="ema20" data-pane="" data-markers="swings" data-controls></div>'
)
ORDERBOOK = '''<div class="card" data-orderbook>
<label>Symbol <select data-book-symbol><option>BTCUSDT</option><option>ETHUSDT</option><option>SOLUSDT</option></select></label>
<p>Spread <strong data-book-spread>—</strong></p>
<p data-book-status role="status">Loading public depth…</p>
<div class="book"><div><h3>Bids</h3><ol data-book-bids></ol></div><div><h3>Asks</h3><ol data-book-asks></ol></div></div>
</div>'''
PATTERNS = '''<svg class="atlas-svg" viewBox="0 0 720 180" role="img" aria-label="Schematic shapes: head and shoulders, double top, triangle, flag. Not forecasts.">
<text x="16" y="24" fill="#ffd06f" font-size="13">Schematic shapes. Not forecasts.</text>
<g fill="none" stroke="#52e4ff" stroke-width="2">
<polyline points="20,120 60,70 90,110 140,40 190,110 230,80 280,130"/>
<polyline points="320,110 370,50 430,100 490,48 540,120"/>
<polyline points="20,160 70,100 120,130 180,90 240,140"/>
</g></svg>'''


def inject(html_text: str, sec_id: str, extra: str) -> str:
    needle = f'id="{sec_id}"'
    idx = html_text.find(needle)
    if idx < 0:
        return html_text + extra
    close = html_text.find("</section>", idx)
    if close < 0:
        return html_text + extra
    return html_text[:close] + extra + html_text[close:]


def render_lessons() -> None:
    scripts = {
        "market-structure.html": ["/assets/vendor/lightweight-charts.standalone.production.js", "/assets/atlas-livechart.js"],
        "technical-analysis.html": ["/assets/vendor/lightweight-charts.standalone.production.js", "/assets/atlas-livechart.js"],
        "risk-academy.html": ["/assets/atlas-riskcharts.js"],
        "exchanges.html": ["/assets/atlas-orderbook.js"],
    }
    heroes = {
        "market-structure.html": "/assets/img/market-structure/hero.webp",
        "technical-analysis.html": "/assets/img/technical-analysis/hero.webp",
        "risk-academy.html": "/assets/img/risk-academy/hero.webp",
        "exchanges.html": "/assets/img/exchanges/hero.webp",
        "security.html": "/assets/img/security/hero.webp",
        "crypto-fundamentals.html": "/assets/img/crypto-fundamentals/hero.webp",
    }
    for name, (path, kicker, filename) in MD_PAGE.items():
        raw = (CONTENT / name).read_text()
        _front, body = split_front(raw)
        rendered, toc = render_markdown(name, body)
        if filename in heroes:
            rendered = placeholder(heroes[filename], "Hero still. Caption stays in the page.") + rendered
        if filename == "market-structure.html":
            rendered = inject(rendered, "swings", CHART_SWINGS)
            rendered = inject(rendered, "candles", '<svg class="atlas-svg" viewBox="0 0 320 140" role="img" aria-label="Annotated candle. High, close, open, and low."><line x1="70" y1="16" x2="70" y2="120" stroke="#55e7c1"/><rect x="54" y="40" width="32" height="48" fill="#55e7c1"/><text x="100" y="24" fill="#9fdfff" font-size="14">High</text><text x="100" y="70" fill="#edf8ff" font-size="14">Open / close</text><text x="100" y="124" fill="#ffb4bc" font-size="14">Low</text></svg>')
        if filename == "technical-analysis.html":
            rendered = inject(rendered, "ema-sma", '<div id="indicators"></div>' + CHART)
            rendered = inject(rendered, "patterns", PATTERNS)
        if filename == "risk-academy.html":
            rendered = inject(rendered, "drawdown", '<div data-drawdown-curve></div>')
            rendered = inject(rendered, "monte-carlo", '<div data-monte-carlo></div>')
        if filename == "exchanges.html":
            rendered = inject(rendered, "order-book", ORDERBOOK)
        title = re.search(r"^title:\s*(.+)$", _front, re.M)
        title_s = title.group(1).strip() if title else filename
        lede = lede_of(body)
        (ROOT / filename).write_text(page(title_s, lede[:180], kicker, lede[:280], rendered, toc, scripts.get(filename, []), title_s))
        print("page", filename)


def tools_pages() -> None:
    tools_body = """
<section class="section" id="index"><h2>The bench</h2>
<ul>
<li><a href="/tools/risk-calc">Risk and position size</a>. Account, risk percent, entry, stop, fees, and slippage. Spot and futures. Hypothetical output.</li>
<li><a href="/tools/grid-bot">Grid command centre</a>. The grid module's calculators.</li>
<li><a href="/journal-lab">Journal analyser</a>. Paste R results and read that paste.</li>
<li><a href="/technical-analysis#indicators">Indicator playground</a>. EMA, SMA, Bollinger, VWAP, RSI, MACD, ATR, and volume.</li>
<li><a href="/exchanges#order-book">Order book</a>. Public depth and a spread.</li>
<li><a href="/risk-academy#drawdown">Drawdown and Monte Carlo</a>. The recovery identity and a labelled reshuffle.</li>
<li><a href="/futures-leverage">Leverage sandbox</a>. How leverage changes notional. Not a liquidation engine.</li>
</ul>
<p>Replay Lab is still not in this build.</p>
</section>"""
    (ROOT / "tools.html").write_text(page(
        "Tools", "Index of ATLAS calculators and labs.", "Tools",
        "Tools make a number visible. They do not choose a trade.",
        placeholder("/assets/img/tools/hero.webp", "Tools index hero.") + tools_body,
        [("index", "The bench")], [], "Tools",
    ))
    calc = '''<section class="section" id="calculator"><h2>Calculator</h2>
<p>Size is the cash at risk divided by the distance from entry to stop. Fees and slippage are basis points on the notional, in and out. The futures cap is compared with notional divided by the account. A venue's margin ladder is not in this form.</p>
<form class="card atlas-calc" data-risk-calc>
<div class="fields">
<label>Mode <select name="mode"><option value="spot">Spot</option><option value="futures">Futures</option></select></label>
<label>Account <input name="account" type="number" min="0" step="1" value="10000"></label>
<label>Risk percent <input name="riskPct" type="number" min="0" step="0.1" value="1"></label>
<label>Entry <input name="entry" type="number" min="0" step="0.01" value="100"></label>
<label>Stop <input name="stop" type="number" min="0" step="0.01" value="95"></label>
<label>Leverage cap <input name="leverage" type="number" min="1" step="0.5" value="3"></label>
<label>Fee, basis points <input name="feeBps" type="number" min="0" step="0.1" value="10"></label>
<label>Slippage, basis points <input name="slipBps" type="number" min="0" step="0.1" value="5"></label>
</div>
<div class="score-grid">
<div class="score"><span>Size</span><b id="riskQty">—</b></div>
<div class="score"><span>Notional</span><b id="riskNotional">—</b></div>
<div class="score"><span>Cash at the stop</span><b id="riskCash">—</b></div>
<div class="score"><span>Stop distance</span><b id="riskDistance">—</b></div>
<div class="score"><span>Fee plus slippage</span><b id="riskFriction">—</b></div>
<div class="score"><span>Cash if stopped, with friction</span><b id="riskLoss">—</b></div>
<div class="score"><span>Implied leverage</span><b id="riskImplied">—</b></div>
</div>
<p id="riskWarning" class="atlas-note" role="status"></p>
</form>
<p class="atlas-note">Hypothetical example. The defaults are a 10,000 account, 1 percent risk, entry 100, stop 95. They are not a trade.</p>
</section>'''
    (ROOT / "risk-calc.html").write_text(page(
        "Risk and position-size calculator",
        "Turn an account, a risk percent, an entry, and a stop into a size.",
        "Tools",
        "The size is the cash you are willing to lose, divided by the distance to the stop.",
        calc, [("calculator", "Calculator")], ["/assets/atlas-risk.js"], "Risk calculator",
    ))


def glossary_and_search() -> None:
    (DATA).mkdir(exist_ok=True)
    raw = json.loads((CONTENT / "glossary.json").read_text())
    (DATA / "glossary.json").write_text(json.dumps(raw))
    body = placeholder("/assets/img/glossary/hero.webp", "Glossary hero.") + '''
<section class="section" id="glossary-top"><h2>Browse</h2>
<div data-atlas-glossary>
<div class="atlas-filters">
<label>Filter <input data-glossary-q type="search" placeholder="Type a term" aria-label="Filter terms"></label>
<label>Topic <select data-glossary-cat><option value="">All topics</option></select></label>
<label>Level <select data-glossary-level><option value="">All levels</option></select></label>
<span data-glossary-count></span>
</div>
<div class="atlas-letters"><button type="button" class="atlas-letter is-on" data-letter="all">All</button></div>
<div data-atlas-chart id="glossaryChart" hidden data-symbol="BTCUSDT" data-tf="1h" data-overlays="ema20" data-pane="rsi"></div>
<div data-glossary-list></div>
</div></section>'''
    (ROOT / "glossary.html").write_text(page(
        "Glossary", "A to Z of the crypto and trading terms used in ATLAS.", "Dictionary",
        "One library needs one dictionary. Filter by letter, topic, or level.",
        body, [("glossary-top", "Browse")],
        ["/assets/vendor/lightweight-charts.standalone.production.js", "/assets/atlas-livechart.js", "/assets/atlas-glossary.js"],
        "Glossary",
    ))
    search = '''<section class="section" id="results"><h2>Find a page or a term</h2>
<div data-atlas-search-page>
<form class="atlas-filters" action="/search" method="get" role="search">
<label>Search <input data-search-q name="q" type="search" placeholder="Try a term or a module"></label>
</form>
<p data-search-meta role="status">Loading the index…</p>
<div data-search-results></div>
</div></section>'''
    (ROOT / "search.html").write_text(page(
        "Search", "Search ATLAS pages, anchors, and glossary terms.", "Library",
        "Search runs in your browser. The slash key focuses the header box.",
        search, [("results", "Results")],
        ["/assets/vendor/fuse.min.js", "/assets/atlas-search.js"],
        "Search",
    ))


def questions() -> list[dict]:
    text = (CONTENT / "find-by-question.md").read_text()
    _f, body = split_front(text)
    parts = re.split(r"\n\*\*(.+?)\*\*\n", body)
    out = []
    i = 1
    while i + 1 < len(parts):
        q = parts[i].strip()
        block = parts[i + 1]
        i += 2
        links = re.findall(r"\[([^\]]+)\]\(([^)]+)\)", block)
        href = "/library"
        if links:
            target = links[0][1]
            target = re.sub(r"\.md(?=#|$)", "", target)
            href = target if target.startswith("/") else "/" + target
            # remap long CM anchors to the ids we actually emit
            href = href.replace("#trend-and-range", "#trend")
            href = href.replace("#break-of-structure-and-change-of-character", "#bos-choch")
            href = href.replace("#order-blocks-and-fair-value-gaps", "#order-blocks")
            href = href.replace("#multi-timeframe-work", "#multi-timeframe")
        out.append({"q": q, "href": href})
    return out


def library_page(qs: list[dict]) -> None:
    items = [
        ("Grid Bot Builder", "/grid-bot", "1", "Intermediate", "Range, spacing, maths, risk, and the command centre."),
        ("Market Structure", "/market-structure", "2", "Beginner", "Candles, swings, trend, range, breaks, and liquidity."),
        ("Technical Analysis", "/technical-analysis", "3", "Intermediate", "Support, averages, RSI, MACD, VWAP, bands, ATR, volume, and patterns."),
        ("Risk Academy", "/risk-academy", "4", "Intermediate", "Size, R, stops, expectancy, drawdown, and a reshuffle."),
        ("DeFi and on-chain", "/defi-onchain", "14", "Advanced", "Wallets, pools, lending, bridges, and on-chain research."),
        ("Crypto fundamentals", "/crypto-fundamentals", "13", "Beginner", "Ledgers, consensus, coins and tokens, fees, and what a chart hides."),
        ("Exchanges and orders", "/exchanges", "", "Beginner", "Books, spread, order types, and Australian registration as general information."),
        ("Wallets and scams", "/security", "", "Beginner", "Keys, seed phrases, and the common cons."),
        ("Futures and leverage", "/futures-leverage", "9", "Intermediate", "The existing leverage sandbox. The longer derivatives lesson is still to expand."),
        ("Journal", "/journal-lab", "11", "Intermediate", "Paste R results. The longer journal lesson is still to expand."),
        ("Automation", "/automation", "15", "Intermediate", "A short module. The longer automation lesson is still to expand."),
        ("Macro", "/macro-lab", "17", "Advanced", "A short module. The longer macro lesson is still to expand."),
        ("Glossary", "/glossary", "", "Beginner", "435 terms, A to Z."),
        ("Tools", "/tools", "", "Beginner", "Calculators and labs that are in this build."),
        ("Learning path", "/learning-path", "", "Beginner", "A route through the library."),
        ("Academy", "/academy", "", "Beginner", "The 18-module map."),
        ("Bitcoin", "/markets/btc", "", "Beginner", "Educational chart. Data may be delayed."),
        ("Ethereum", "/markets/eth", "", "Beginner", "Educational chart. Data may be delayed."),
        ("BNB", "/markets/bnb", "", "Beginner", "Educational chart. Data may be delayed."),
        ("Solana", "/markets/sol", "", "Beginner", "Educational chart plus a short primer."),
    ]
    cards = []
    for title, href, academy, level, summary in items:
        label = f"Academy {academy}" if academy else "Library"
        cards.append(f'<a class="card" href="{href}"><span class="num">{html.escape(label)}</span> <span class="status">LIVE</span><h3>{html.escape(title)}</h3><p>{html.escape(summary)}</p></a>')
    by_level = []
    for level in ("Beginner", "Intermediate", "Advanced"):
        group = [c for c, item in zip(cards, items) if item[3] == level]
        by_level.append(f"<h3>{level}</h3><div class=\"grid3\">{''.join(group)}</div>")
    qhtml = "".join(f'<a href="{html.escape(q["href"])}">{html.escape(q["q"])}</a>' for q in qs)
    manifest = {
        "items": [
            {"title": t, "path": h, "academy": a, "level": lv, "status": "live", "summary": s}
            for t, h, a, lv, s in items
        ],
        "questions": qs,
    }
    (DATA / "library-manifest.json").write_text(json.dumps(manifest, indent=2))
    body = f'''<section class="section" id="by-topic"><h2>By topic</h2><div class="library-views"><a class="btn" href="#by-topic">A–Z</a><a class="btn" href="#by-level">By level</a><a class="btn" href="#by-question">By question</a></div><p>Built from <code>data/library-manifest.json</code>. A live badge means the page exists. Academy numbers follow the 18-module scheme. Pages still to expand are labelled in the summary.</p><div class="grid3">{"".join(cards)}</div></section>
<section class="section" id="by-level"><h2>By level</h2>{"".join(by_level)}</section>
<section class="section" id="by-question"><h2>By question</h2><div class="q-list">{qhtml}</div></section>'''
    (ROOT / "library.html").write_text(page(
        "Library", "The ATLAS directory by topic, level, and question.", "One library",
        "Every page in this build, plus the questions Content Marketing wrote.",
        body, [("by-topic", "By topic"), ("by-level", "By level"), ("by-question", "By question")],
        [], "Library",
    ))
    print("questions", len(qs))


def samples() -> None:
    folder = DATA / "samples"
    folder.mkdir(parents=True, exist_ok=True)
    bases = {"BTCUSDT": 42000, "ETHUSDT": 2200, "BNBUSDT": 310, "SOLUSDT": 98}
    for symbol, base in bases.items():
        for interval, step in (("1h", 3600), ("4h", 14400), ("1d", 86400)):
            seed = int(hashlib.sha256(f"{symbol}-{interval}".encode()).hexdigest()[:8], 16) or 1
            x = seed
            price = base
            candles = []
            for i in range(240):
                x = (1103515245 * x + 12345) & 0x7FFFFFFF
                rnd = x / 0x7FFFFFFF
                o = price
                c = max(1e-8, o * (1 + math.sin(i / 18) * 0.004 + (rnd - 0.48) * 0.02))
                h = max(o, c) * (1 + rnd * 0.006)
                low = min(o, c) * (1 - rnd * 0.006)
                candles.append({"time": 1704067200 + i * step, "open": round(o, 6), "high": round(h, 6), "low": round(low, 6), "close": round(c, 6), "volume": round(500 + rnd * 4000, 3)})
                price = c
            (folder / f"{symbol}-{interval}.json").write_text(json.dumps({
                "symbol": symbol, "interval": interval, "label": "Educational sample",
                "note": "Bundled study series. Not a historical claim and not a live quote.",
                "candles": candles,
            }))


def market_sol() -> None:
    text = (ROOT / "market-btc.html").read_text()
    primer_md = split_front((CONTENT / "solana-primer.md").read_text())[1]
    primer_html, _toc = render_markdown("solana-primer.md", primer_md)
    text = text.replace("Bitcoin Market", "Solana Market")
    text = text.replace("Live Bitcoin market chart", "Live Solana market chart")
    text = text.replace('data-symbol="BTCUSDT"', 'data-symbol="SOLUSDT"')
    text = text.replace('data-coin="Bitcoin"', 'data-coin="Solana"')
    text = text.replace('data-cgid="bitcoin"', 'data-cgid="solana"')
    text = text.replace(">Bitcoin <", ">Solana <")
    text = text.replace("BTC / USDT", "SOL / USDT")
    text = text.replace("LIVE MARKETS / BTC", "LIVE MARKETS / SOL")
    text = text.replace('aria-label="Bitcoin candlestick chart"', 'aria-label="Solana candlestick chart"')
    text = text.replace("</main>", f'<section class="market-integrated"><article class="market-panel">{primer_html}</article></section></main>', 1)
    (ROOT / "market-sol.html").write_text(text)


def patch_file(path: Path, index: int) -> None:
    text = path.read_text()
    original = text
    if "atlas-library.css" not in text and "</head>" in text:
        text = text.replace("</head>", '<link rel="stylesheet" href="/assets/atlas-library.css"/>\n</head>', 1)
    if "/assets/atlas-config.js" not in text and "</body>" in text:
        text = text.replace("</body>", '<script src="/assets/atlas-config.js"></script>\n</body>', 1)
    text = text.replace(
        "https://unpkg.com/lightweight-charts@4.2.3/dist/lightweight-charts.standalone.production.js",
        "/assets/vendor/lightweight-charts.standalone.production.js",
    )
    text = text.replace("proven strategies", "structured strategy frameworks")
    if "data-atlas-search-input" not in text:
        form = (
            f'<form class="atlas-header-search" action="/search" method="get" role="search">'
            f'<label class="visually-hidden" for="atlasHeaderSearch{index}">Search the library</label>'
            f'<input id="atlasHeaderSearch{index}" name="q" type="search" placeholder="Search" autocomplete="off" data-atlas-search-input></form>'
        )
        needle = '<a class="atlas-search-button" href="/search"'
        if needle in text:
            text = text.replace(needle, form + needle, 1)
        needle = '<a class="atlas-search" href="/search"'
        if needle in text and "data-atlas-search-input" not in text:
            text = text.replace(needle, form + needle, 1)
    if "atlas-general-warning" not in text and "</footer>" in text:
        text = text.replace("</footer>", WARNING + "</footer>", 1)
    if 'href="/disclaimer"' not in text and 'href="/terms"' in text:
        text = text.replace('href="/terms">Terms</a>', 'href="/terms">Terms</a><a href="/disclaimer">Disclaimer</a>', 1)
    if path.name == "library.html":
        return
    if text != original:
        path.write_text(text)


def patch_shell(path: Path) -> None:
    text = path.read_text()
    built = [
        "/markets/sol", "/market-sol",
        "/academy/ta", "/academy/structure", "/academy/risk",
        "/academy/02-technical-analysis", "/academy/03-market-structure", "/academy/04-risk-management",
        "/technical-analysis", "/market-structure", "/risk-academy",
        "/tools", "/tools/risk-calc", "/search", "/privacy", "/terms",
    ]
    for key in built:
        text = re.sub(rf'\n    "{re.escape(key)}": "[^"]*",?', "", text)
    if "data-atlas-search-input" not in text:
        text = text.replace(
            '  var notice = document.getElementById("notice-current");',
            '''  document.querySelectorAll("[data-atlas-email]").forEach(function (el) {
    var email = window.ATLAS_SUPPORT_EMAIL || "";
    if (!email || el.tagName !== "A") return;
    el.href = "mailto:" + email;
    var slot = el.querySelector("[data-atlas-email-text]");
    if (slot) slot.textContent = email;
  });
  document.addEventListener("keydown", function (e) {
    if (e.key !== "/" || e.ctrlKey || e.metaKey || e.altKey) return;
    var tag = e.target && e.target.tagName ? e.target.tagName.toLowerCase() : "";
    if (tag === "input" || tag === "textarea" || tag === "select" || (e.target && e.target.isContentEditable)) return;
    var input = document.querySelector("[data-atlas-search-input]");
    if (!input) return;
    var nav = document.querySelector("[data-primary-nav], [data-grid-primary-nav]");
    if (nav && window.matchMedia("(max-width: 980px)").matches) nav.classList.add("is-open");
    e.preventDefault();
    input.focus();
  });
  var notice = document.getElementById("notice-current");''',
        )
    path.write_text(text)


def patch_index_and_contact() -> None:
    index = (ROOT / "index.html").read_text()
    old_btn = '<button aria-controls="introModal" aria-haspopup="dialog" class="btn secondary" id="introOpen" type="button">▶ Watch Introduction · 2 min</button>'
    new_btn = '''<button aria-controls="introModal" aria-haspopup="dialog" class="btn secondary" id="introOpen" type="button" hidden>Watch introduction</button>
<div class="intro-inline" id="introInline"><p><strong>A short orientation.</strong> The video file is not on this site yet.</p><ul>
<li>ATLAS is one library for every market you study.</li>
<li>Lessons move from what something is, to how to see it, to how to practise it.</li>
<li>Charts here are for study. They are not orders.</li>
<li>Worked numbers are hypothetical unless a public data feed is named.</li>
<li>Stewart's line for the library: one library, every market, a smarter you.</li>
</ul></div>'''
    if old_btn not in index:
        raise SystemExit("intro button missing")
    index = index.replace(old_btn, new_btn)
    index = index.replace(
        '<video id="introVideo" controls playsinline preload="metadata" aria-label="ATLAS two-minute introduction"></video>',
        '<video id="introVideo" data-src="" controls playsinline preload="none" aria-label="ATLAS introduction"></video>',
    )
    index = index.replace(
        '<div class="intro-copy"><strong>Welcome to ATLAS.</strong><p></p></div>',
        '<div class="intro-copy"><strong>Welcome to ATLAS.</strong><ul><li>One library, every market.</li><li>Learn the mechanism before the tool.</li><li>Charts are for study, not tickets.</li><li>Examples are hypothetical unless a feed is named.</li><li>A smarter you is the aim. A promised result is not.</li></ul></div>',
    )
    old_js = "let lastFocus=null;const source=video?.querySelector('source');if(source?.getAttribute('src'))videoWrap?.classList.add('has-source');"
    new_js = """let lastFocus=null;const inline=document.getElementById('introInline');
 const configured=(video?.getAttribute('data-src')||video?.getAttribute('src')||video?.querySelector('source')?.getAttribute('src')||'').trim();
 if(configured){if(!video.getAttribute('src'))video.src=configured;videoWrap?.classList.add('has-source');open.hidden=false;if(inline)inline.hidden=true;}
 else{open.hidden=true;if(inline)inline.hidden=false;}"""
    if old_js not in index:
        raise SystemExit("intro script missing")
    index = index.replace(old_js, new_js)
    (ROOT / "index.html").write_text(index)

    contact = (ROOT / "contact.html").read_text()
    contact = contact.replace("mailto:support@example.com", "mailto:contact@stewartcrowncrypto.com")
    contact = contact.replace("support@example.com", "contact@stewartcrowncrypto.com")
    contact = contact.replace(
        "<strong>Developer note:</strong> replace the placeholder email action before public deployment.",
        "The address is <span data-atlas-email-text>contact@stewartcrowncrypto.com</span>. It is pending Stewart's confirmation and is set in ATLAS_SUPPORT_EMAIL.",
    )
    contact = contact.replace(
        '<a class="btn primary" href="mailto:contact@stewartcrowncrypto.com">Email ATLAS Support →</a>',
        '<a class="btn primary" data-atlas-email href="mailto:contact@stewartcrowncrypto.com">Email <span data-atlas-email-text>contact@stewartcrowncrypto.com</span></a>',
    )
    (ROOT / "contact.html").write_text(contact)


def redirects_and_notice() -> None:
    text = (ROOT / "_redirects").read_text()
    swaps = {
        "/markets/sol": "/market-sol.html",
        "/academy/ta": "/technical-analysis.html",
        "/academy/structure": "/market-structure.html",
        "/academy/risk": "/risk-academy.html",
        "/tools": "/tools.html",
        "/tools/risk-calc": "/risk-calc.html",
        "/search": "/search.html",
        "/privacy": "/privacy.html",
        "/terms": "/terms.html",
        "/academy/02-technical-analysis": "/technical-analysis.html",
        "/academy/03-market-structure": "/market-structure.html",
        "/academy/04-risk-management": "/risk-academy.html",
        "/market-sol": "/market-sol.html",
        "/market-structure": "/market-structure.html",
        "/risk-academy": "/risk-academy.html",
        "/technical-analysis": "/technical-analysis.html",
    }
    for src, dest in swaps.items():
        pattern = re.compile(rf"^{re.escape(src)}\s+/not-included\.html\s+200\s*$", re.M)
        if not pattern.search(text):
            raise SystemExit("redirect missing: " + src)
        text = pattern.sub(f"{src:<28} {dest:<26} 200", text, count=1)
    if "/glossary " not in text:
        text += "\n/glossary                    /glossary.html             200\n/disclaimer                  /disclaimer.html           200\n/exchanges                   /exchanges.html            200\n/security                    /security.html             200\n"
    (ROOT / "_redirects").write_text(text)
    notice = (ROOT / "not-included.html").read_text()
    for path in [
        "/markets/sol", "/academy/ta", "/technical-analysis", "/academy/structure", "/market-structure",
        "/academy/risk", "/risk-academy", "/tools", "/tools/risk-calc", "/search", "/privacy", "/terms",
    ]:
        notice = re.sub(rf"<li><code>{re.escape(path)}</code><span>[^<]*</span></li>\n?", "", notice)
    (ROOT / "not-included.html").write_text(notice)


def search_index() -> None:
    entries = []
    for path in ROOT.rglob("*.html"):
        if "content" in path.parts:
            continue
        raw = path.read_text(errors="ignore")
        rel = path.relative_to(ROOT).as_posix()
        url = "/" + rel[:-5]
        if url.endswith("/index"):
            url = "/"
        title = re.search(r"<title>([^<]*)</title>", raw)
        title_s = re.sub(r"\s+—\s+ATLAS.*", "", title.group(1)).strip() if title else rel
        visible = re.sub(r"<script[\s\S]*?</script>", " ", raw)
        visible = re.sub(r"<style[\s\S]*?</style>", " ", visible)
        visible = re.sub(r"<[^>]+>", " ", visible)
        visible = re.sub(r"\s+", " ", visible).strip()
        entries.append({"title": title_s, "url": url, "kind": "page", "text": visible[:400]})
        for match in re.finditer(r'<h2[^>]*\sid="([^"]+)"[^>]*>([\s\S]*?)</h2>', raw):
            label = re.sub(r"<[^>]+>", "", match.group(2))
            label = re.sub(r"\s+", " ", label).strip()
            entries.append({"title": label or match.group(1), "url": url + "#" + match.group(1), "kind": "anchor", "text": label})
    for term in json.loads((DATA / "glossary.json").read_text()):
        entries.append({
            "title": term["term"],
            "url": "/glossary#" + term["anchor"],
            "kind": "term",
            "text": term["one_liner"] + " " + term["explanation"],
        })
    (DATA / "search-index.json").write_text(json.dumps({"count": len(entries), "entries": entries}))
    print("search", len(entries))


def main() -> None:
    render_lessons()
    tools_pages()
    glossary_and_search()
    library_page(questions())
    samples()
    market_sol()
    html_files = [p for p in ROOT.rglob("*.html") if "content" not in p.parts]
    for i, path in enumerate(html_files):
        if path.name == "library.html":
            continue
        patch_file(path, i)
    patch_index_and_contact()
    patch_shell(ROOT / "assets" / "site.js")
    patch_shell(ROOT / "assets" / "atlas-shell.js")
    redirects_and_notice()
    search_index()
    print("p0 build done")


if __name__ == "__main__":
    main()
