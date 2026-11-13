#!/usr/bin/env python3
"""Build dist/atlas/atlas.html — one offline file for the Atlas grid-bot directory."""
from __future__ import annotations

import base64
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]
SINGLE = Path(__file__).resolve().parent
CONTENT = ROOT / "content"
DIST = REPO / "dist" / "atlas"
TOKEN_RE = re.compile(r"\[[A-Z][^\]\n]{1,240}\]")

LINK_MAP = {
    "market-structure.md": "guides/market-structure",
    "technical-analysis.md": "guides/technical-analysis",
    "risk-academy.md": "guides/risk-academy",
    "crypto-fundamentals.md": "guides/crypto-fundamentals",
    "exchanges.md": "guides/exchanges",
    "security.md": "guides/security",
    "futures-leverage.md": "guides/futures-leverage",
    "automation.md": "guides/automation",
    "journal-lab.md": "guides/journal-lab",
    "macro-lab.md": "guides/macro-lab",
    "market-strategies.md": "guides/market-strategies",
    "psychology.md": "guides/psychology",
    "chains.md": "guides/chains",
    "tax-regulation.md": "guides/tax-regulation",
    "checklist-form-notice.md": "guides/checklist-form-notice",
    "find-by-question.md": "questions",
    "glossary.md": "glossary",
    "terms.md": "terms",
    "privacy.md": "privacy",
    "disclaimer.md": "disclaimer",
    "footer-line.md": "disclaimer/footer-line",
    "solana-primer.md": "markets/sol",
    "hbar-primer.md": "markets/hbar",
    "link-primer.md": "markets/link",
    "ltc-primer.md": "markets/ltc",
    "sui-primer.md": "markets/sui",
    "xrp-primer.md": "markets/xrp",
}

GUIDES = [
    ("crypto-fundamentals.md", "what the asset actually is, so a grid conversation starts from the coin and the fee, not from a chart pattern", "path/what", "step 1, what a grid bot is", "path/what", "What a grid bot is"),
    ("security.md", "how inventory and keys can be lost, because a grid holds coins while it waits", "path/setup", "step 3, setting one up", "path/setup", "Setting one up"),
    ("exchanges.md", "how a book, a spread, and an order type change the fill a grid bot actually gets", "path/setup", "step 3, setting one up", "path/how", "How it works"),
    ("automation.md", "what software can repeat for you, and which decisions it cannot make", "path/how", "step 2, how it works", "path/how", "How it works"),
    ("chains.md", "how network fees and wallets change a grid that settles on a chain", "path/setup", "step 3, setting one up", "path/setup", "Setting one up"),
    ("market-structure.md", "how to tell a range from a trend, which is the behaviour a grid is built for", "path/range", "step 4, choosing ranges and grids", "path/range", "Choosing ranges and grids"),
    ("technical-analysis.md", "how common chart tools describe past prices when you are drawing a grid's box", "path/range", "step 4, choosing ranges and grids", "path/range", "Choosing ranges and grids"),
    ("market-strategies.md", "how to write a framework, including a range plan, so a grid is a sentence and not a guess", "path/range", "step 4, choosing ranges and grids", "path/range", "Choosing ranges and grids"),
    ("futures-leverage.md", "how margin, funding, and liquidation change a grid that is not spot", "path/risk", "step 5, managing risk", "path/risk", "Managing risk"),
    ("risk-academy.md", "how size, R, and drawdown are calculated before a grid is allowed to run", "path/risk", "step 5, managing risk", "path/risk", "Managing risk"),
    ("psychology.md", "how to notice the urge to tighten a grid after a loss, and write it down instead of acting on it", "path/mistakes", "step 7, common mistakes", "path/mistakes", "Common mistakes"),
    ("journal-lab.md", "how to record finished cycles and unsold coins so a review is about the plan", "path/monitor", "step 6, monitoring and adjusting", "path/monitor", "Monitoring and adjusting"),
    ("macro-lab.md", "how a scheduled event can expire the reason you chose a range", "path/monitor", "step 6, monitoring and adjusting", "path/monitor", "Monitoring and adjusting"),
    ("tax-regulation.md", "why many grid fills create many records, as general information and not as tax advice", "path/monitor", "step 6, monitoring and adjusting", "path/monitor", "Monitoring and adjusting"),
    ("checklist-form-notice.md", "the wording for a future checklist sign-up, and which blanks Stewart still has to fill", "path/setup", "step 3, setting one up", "notes", "NOTES"),
]

PATH = [
    ("path/what", "What a grid bot is"),
    ("path/how", "How it works"),
    ("path/setup", "Setting one up"),
    ("path/range", "Choosing ranges and grids"),
    ("path/risk", "Managing risk"),
    ("path/monitor", "Monitoring and adjusting"),
    ("path/mistakes", "Common mistakes"),
]

FRAGMENTS = {
    "home": ("A directory for grid bots", "Atlas is one path for learning grid bots, and every guide, tool, and market study points back to a step on that path", "", "", "path/what", "What a grid bot is"),
    "path/what": ("What a grid bot is", "a grid bot is a ladder of buys and sells you design, not a machine that predicts the next candle", "path/what", "step 1 of the path", "path/how", "How it works"),
    "path/how": ("How it works", "how one cycle runs: a buy, a later sell, and a repeat only while price stays in the box", "path/how", "step 2 of the path", "path/setup", "Setting one up"),
    "path/setup": ("Setting one up", "which decisions you have to write down before a grid bot is allowed to repeat them", "path/setup", "step 3 of the path", "path/range", "Choosing ranges and grids"),
    "path/range": ("Choosing ranges and grids", "how to choose the box and the spacing so a gap can clear a fee in a hypothetical example", "path/range", "step 4 of the path", "path/risk", "Managing risk"),
    "path/risk": ("Managing risk", "how cash at risk and the distance to a stop set a size, and why that size is not a promise", "path/risk", "step 5 of the path", "path/monitor", "Monitoring and adjusting"),
    "path/monitor": ("Monitoring and adjusting", "what to check on a running grid, and how to separate finished cycles from unsold coins", "path/monitor", "step 6 of the path", "path/mistakes", "Common mistakes"),
    "path/mistakes": ("Common mistakes", "the configuration errors that show up first, and when the careful choice is to wait", "path/mistakes", "step 7 of the path", "directory", "The directory"),
    "tools": ("Tools", "how the spacing, the position size, and a journal average are calculated from figures you type", "path/risk", "step 5, managing risk", "path/risk", "Managing risk"),
    "about": ("About Atlas", "who publishes this directory, and that the file in front of you is the whole course", "path/what", "step 1, what a grid bot is", "path/what", "What a grid bot is"),
    "contact": ("Contact", "how to reach Stewart's company without sending a key or a seed phrase", "path/what", "step 1, what a grid bot is", "path/what", "What a grid bot is"),
}


def slugify(text: str) -> str:
    text = re.sub(r"<[^>]+>", "", text)
    text = text.lower().replace("&amp;", " and ")
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return text or "section"


def parse_front(text: str) -> tuple[dict, str]:
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    meta: dict = {"related": []}
    current = None
    for line in parts[1].splitlines():
        if re.match(r"^[A-Za-z0-9_-]+:", line):
            key, value = line.split(":", 1)
            current = key.strip()
            if current == "related":
                meta["related"] = []
            else:
                meta[current] = value.strip()
        elif current == "related" and line.strip().startswith("- "):
            meta["related"].append(line.strip()[2:].strip())
    return meta, parts[2].lstrip("\n")


def is_block(line: str) -> bool:
    return bool(
        re.match(r"^(#{1,3} |[-*] |\d+\. |>|\||```)", line)
    )


class Renderer:
    def __init__(self, page_id: str) -> None:
        self.page_id = page_id
        self.ids: dict[str, int] = {}

    def heading_id(self, text: str) -> str:
        base = slugify(text)
        n = self.ids.get(base, 0)
        self.ids[base] = n + 1
        return base if n == 0 else f"{base}-{n + 1}"

    def link(self, label: str, url: str) -> str:
        label_html = self.inline(label, links=False)
        external = url.startswith("http://") or url.startswith("https://")
        if url.startswith("mailto:"):
            return f'<a href="{html.escape(url, quote=True)}">{label_html}</a>'
        if external:
            return f'<a href="{html.escape(url, quote=True)}" rel="noopener noreferrer">{label_html}</a>'
        path, _, frag = url.partition("#")
        if path in LINK_MAP:
            dest = LINK_MAP[path]
            href = f"#/{dest}/{frag}" if frag else f"#/{dest}"
        elif not path and frag:
            href = f"#/{self.page_id}/{frag}"
        else:
            raise SystemExit(f"Unresolved link in {self.page_id}: {url}")
        return f'<a href="{href}">{label_html}</a>'

    def inline(self, text: str, links: bool = True) -> str:
        slots: list[str] = []

        def slot(piece: str) -> str:
            slots.append(piece)
            return f"@@SLOT{len(slots) - 1}@@"

        text = re.sub(r"`([^`]+)`", lambda m: slot("<code>" + html.escape(m.group(1)) + "</code>"), text)
        if links:
            text = re.sub(
                r"\[([^\]]+)\]\(([^)\s]+)\)",
                lambda m: slot(self.link(m.group(1), m.group(2))),
                text,
            )
        text = html.escape(text)
        text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
        text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", text)
        text = re.sub(r"@@SLOT(\d+)@@", lambda m: slots[int(m.group(1))], text)
        return text

    def table(self, rows: list[str]) -> str:
        parsed = []
        for row in rows:
            cells = [c.strip() for c in row.strip().strip("|").split("|")]
            if cells and all(re.fullmatch(r":?-{3,}:?", c.replace(" ", "")) for c in cells):
                continue
            parsed.append(cells)
        if not parsed:
            return ""
        head, body = parsed[0], parsed[1:]
        thead = "".join(f"<th>{self.inline(c)}</th>" for c in head)
        tbody = "".join(
            "<tr>" + "".join(f"<td>{self.inline(c)}</td>" for c in row) + "</tr>" for row in body
        )
        return f"<div class=\"table-scroll\"><table><thead><tr>{thead}</tr></thead><tbody>{tbody}</tbody></table></div>"

    def render(self, body: str) -> str:
        lines = body.replace("\r\n", "\n").split("\n")
        out: list[str] = []
        i = 0
        while i < len(lines):
            line = lines[i]
            if line.startswith("```"):
                buff = []
                i += 1
                while i < len(lines) and not lines[i].startswith("```"):
                    buff.append(lines[i])
                    i += 1
                i += 1
                out.append("<pre><code>" + html.escape("\n".join(buff)) + "</code></pre>")
                continue
            if not line.strip():
                i += 1
                continue
            if line.startswith("|"):
                rows = []
                while i < len(lines) and lines[i].startswith("|"):
                    rows.append(lines[i])
                    i += 1
                out.append(self.table(rows))
                continue
            if line.startswith(">"):
                buff = []
                while i < len(lines) and (lines[i].startswith(">") or (buff and lines[i].startswith("  "))):
                    buff.append(lines[i][1:].strip() if lines[i].startswith(">") else lines[i].strip())
                    i += 1
                out.append("<blockquote><p>" + self.inline(" ".join(buff)) + "</p></blockquote>")
                continue
            match = re.match(r"^(#{1,3}) ", line)
            if match:
                level = len(match.group(1))
                text = line[level + 1 :].strip()
                hid = self.heading_id(text)
                tag = "h2" if level == 1 else f"h{level}"
                if level == 1:
                    i += 1
                    continue
                out.append(f'<{tag} id="{hid}">{self.inline(text, links=False)}</{tag}>')
                i += 1
                continue
            if re.match(r"^[-*] ", line):
                items = []
                while i < len(lines) and re.match(r"^[-*] ", lines[i]):
                    items.append("<li>" + self.inline(lines[i][2:].strip()) + "</li>")
                    i += 1
                out.append("<ul>" + "".join(items) + "</ul>")
                continue
            if re.match(r"^\d+\. ", line):
                items = []
                while i < len(lines) and re.match(r"^\d+\. ", lines[i]):
                    items.append("<li>" + self.inline(re.sub(r"^\d+\. ", "", lines[i]).strip()) + "</li>")
                    i += 1
                out.append("<ol>" + "".join(items) + "</ol>")
                continue
            buff = [line.strip()]
            i += 1
            while i < len(lines) and lines[i].strip() and not is_block(lines[i]):
                buff.append(lines[i].strip())
                i += 1
            out.append("<p>" + self.inline(" ".join(buff)) + "</p>")
        return "\n".join(part for part in out if part)


def mark_placeholders(fragment: str) -> str:
    return TOKEN_RE.sub(lambda m: f'<mark class="placeholder">{m.group(0)}</mark>', fragment)


def peel_draft(fragment: str) -> tuple[str, str]:
    banner = []
    rest = fragment
    while True:
        match = re.match(r"\s*<p>(\[?DRAFT[\s\S]*?)</p>", rest)
        if not match:
            break
        banner.append("<p>" + match.group(1) + "</p>")
        rest = rest[match.end() :]
    return "".join(banner), rest


def plain(fragment: str) -> str:
    text = re.sub(r"<[^>]+>", " ", fragment)
    text = html.unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def page(pid, title, learn, fits_href, fits_label, nxt, nxt_label, body, banner=""):
    return {
        "id": pid,
        "title": title,
        "learn": learn,
        "fitsHref": fits_href,
        "fitsLabel": fits_label,
        "next": nxt,
        "nextLabel": nxt_label,
        "html": body,
        "banner": banner,
        "text": plain(body)[:4000],
    }


def index_list(items: list[tuple[str, str, str]]) -> str:
    lis = []
    for href, title, note in items:
        lis.append(
            f'<li><a href="#/{href}"><strong>{html.escape(title)}</strong><span>{html.escape(note)}</span></a></li>'
        )
    return '<ul class="index">' + "".join(lis) + "</ul>"


def load_fragments() -> dict[str, str]:
    raw = (SINGLE / "fragments.html").read_text(encoding="utf-8")
    found = dict(re.findall(r'<template id="([^"]+)">([\s\S]*?)</template>', raw))
    missing = [key for key in FRAGMENTS if key not in found]
    if missing:
        raise SystemExit(f"Missing fragments: {missing}")
    return found


def font_css() -> str:
    fonts = SINGLE / "fonts"
    latin = "U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD"

    def face(family: str, weight: str, filename: str) -> str:
        blob = base64.b64encode((fonts / filename).read_bytes()).decode("ascii")
        return (
            "@font-face{"
            f'font-family:"{family}";font-style:normal;font-weight:{weight};font-display:swap;'
            f'src:url(data:font/woff2;base64,{blob}) format("woff2");'
            f"unicode-range:{latin};"
            "}"
        )

    return "\n".join(
        [
            face("Inter", "400 700", "inter-400.woff2"),
            face("Space Grotesk", "500 700", "space-grotesk-500.woff2"),
            face("IBM Plex Mono", "400", "ibm-plex-mono-400.woff2"),
            face("IBM Plex Mono", "500", "ibm-plex-mono-500.woff2"),
            face("IBM Plex Mono", "600", "ibm-plex-mono-600.woff2"),
        ]
    )


def data_uri(path: Path, mime: str) -> str:
    return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode("ascii")


def load_markets(glossary_anchors: set[str]) -> dict:
    primers = {
        "sol": "solana-primer.md",
        "hbar": "hbar-primer.md",
        "link": "link-primer.md",
        "ltc": "ltc-primer.md",
        "sui": "sui-primer.md",
        "xrp": "xrp-primer.md",
    }
    samples = {"btc": "BTCUSDT", "eth": "ETHUSDT", "bnb": "BNBUSDT", "sol": "SOLUSDT"}
    names = {
        "btc": "Bitcoin",
        "eth": "Ethereum",
        "bnb": "BNB",
        "sol": "Solana",
        "link": "Chainlink",
        "sui": "Sui",
        "ltc": "Litecoin",
        "hbar": "Hedera",
        "xrp": "XRP",
    }
    markets = {}
    for mid, name in names.items():
        series = {}
        if mid in samples:
            for interval in ("1h", "4h", "1d"):
                payload = json.loads((ROOT / "data" / "samples" / f"{samples[mid]}-{interval}.json").read_text())
                series[interval] = [
                    {
                        "open": round(c["open"], 4),
                        "high": round(c["high"], 4),
                        "low": round(c["low"], 4),
                        "close": round(c["close"], 4),
                    }
                    for c in payload["candles"]
                ]
        primer_html = ""
        primer_text = ""
        if mid in primers:
            meta, body = parse_front((CONTENT / primers[mid]).read_text(encoding="utf-8"))
            renderer = Renderer(f"markets/{mid}")
            primer_html = renderer.render(body)
            primer_text = plain(primer_html)
            _ = meta
        blurb = (
            "Bundled study candles, not a live quote and not a historical claim. Ask whether price went back and forth inside a box."
            if series
            else "A short primer only. There is no candle sample for this asset in the file. Practise the range question on a charted market."
        )
        markets[mid] = {
            "name": name,
            "blurb": blurb,
            "learn": "how to ask whether this asset's study material looks like a range, which is the behaviour a grid is built for",
            "series": series,
            "primer": primer_html,
            "text": primer_text,
        }
    return markets


def related_html(slugs: list[str], pages: dict) -> str:
    items = []
    for slug in slugs:
        route = LINK_MAP.get(f"{slug}.md")
        if not route or route not in pages and not route.startswith("markets/") and route not in {"glossary", "questions", "terms", "privacy", "disclaimer"}:
            if route and (route in pages or route.startswith("markets/") or route in {"glossary", "questions", "terms", "privacy", "disclaimer", "disclaimer/footer-line"}):
                pass
            else:
                continue
        if not route:
            continue
        title = pages[route]["title"] if route in pages else slug.replace("-", " ")
        items.append(f'<li><a href="#/{route}">{html.escape(title)}</a></li>')
    if not items:
        return ""
    return '<nav class="related" aria-label="Related in the directory"><h2>Related in the directory</h2><ul>' + "".join(items) + "</ul></nav>"


def main() -> None:
    fragments = load_fragments()
    mascot = data_uri(ROOT / "assets" / "grid-bot-mascot.jpg", "image/jpeg")
    mascot_alt = data_uri(ROOT / "assets" / "grid-bot-mascot-alt.jpg", "image/jpeg")
    for key, body in list(fragments.items()):
        fragments[key] = body.replace("__MASCOT_ALT__", mascot_alt).replace("__MASCOT__", mascot)

    glossary = json.loads((ROOT / "data" / "glossary.json").read_text(encoding="utf-8"))
    anchors = {term["anchor"] for term in glossary}
    if len(glossary) != 435:
        raise SystemExit(f"Expected 435 glossary terms, found {len(glossary)}")
    for term in glossary:
        for ref in term.get("see_also") or []:
            if ref not in anchors:
                raise SystemExit(f"Glossary see_also missing: {ref}")

    pages: dict[str, dict] = {}
    for pid, (title, learn, fits, fits_label, nxt, nxt_label) in FRAGMENTS.items():
        pages[pid] = page(pid, title, learn, fits, fits_label, nxt, nxt_label, fragments[pid].strip())

    guide_rows = []
    for filename, learn, fits, fits_label, nxt, nxt_label in GUIDES:
        meta, body = parse_front((CONTENT / filename).read_text(encoding="utf-8"))
        pid = LINK_MAP[filename]
        renderer = Renderer(pid)
        rendered = renderer.render(body)
        banner, rendered = peel_draft(rendered)
        title = meta.get("title") or pid
        pages[pid] = page(pid, title, learn, fits, fits_label, nxt, nxt_label, rendered, banner)
        guide_rows.append((pid, title, learn))

    for filename, title, learn, fits, fits_label, nxt, nxt_label in [
        ("questions", "Questions", "the short answer to a grid-bot question, and which lesson goes further", "path/what", "step 1, what a grid bot is", "path/what", "What a grid bot is"),
    ]:
        pass
    meta, body = parse_front((CONTENT / "find-by-question.md").read_text(encoding="utf-8"))
    renderer = Renderer("questions")
    rendered = renderer.render(body)
    pages["questions"] = page(
        "questions",
        "Questions",
        "the short answer to a grid-bot question, and which lesson goes further",
        "path/what",
        "step 1, what a grid bot is",
        "path/what",
        "What a grid bot is",
        rendered,
    )

    for filename, pid, title, learn, nxt, nxt_label in [
        ("terms.md", "terms", "Terms of use", "the rules for using this directory, including that it is education and not personal advice", "privacy", "Privacy"),
        ("privacy.md", "privacy", "Privacy", "what this offline copy does and does not collect, and which contact details Stewart still has to fill", "disclaimer", "Disclaimer"),
        ("disclaimer.md", "disclaimer", "Disclaimer", "that the directory is general information, not a setting to copy and not a licence to advise you", "notes", "NOTES"),
    ]:
        meta, body = parse_front((CONTENT / filename).read_text(encoding="utf-8"))
        renderer = Renderer(pid)
        rendered = renderer.render(body)
        banner, rendered = peel_draft(rendered)
        pages[pid] = page(pid, meta.get("title") or title, learn, "path/what", "step 1, what a grid bot is", nxt, nxt_label, rendered, banner)

    footer_meta, footer_body = parse_front((CONTENT / "footer-line.md").read_text(encoding="utf-8"))
    footer_renderer = Renderer("disclaimer")
    footer_html = footer_renderer.render(footer_body)
    footer_banner, footer_html = peel_draft(footer_html)
    pages["disclaimer"]["html"] += f'<h2 id="footer-line">Footer line</h2>{footer_banner}{footer_html}'
    _ = footer_meta

    markets = load_markets(anchors)
    market_rows = [(f"markets/{mid}", item["name"], item["blurb"]) for mid, item in markets.items()]
    pages["markets"] = page(
        "markets",
        "Market studies",
        "how to look at a bundled sample, or a short primer, and ask whether price behaved like a range",
        "path/range",
        "step 4, choosing ranges and grids",
        "path/range",
        "Choosing ranges and grids",
        "<p>These pages are for practice, not for a signal. A sample is a saved series inside this file. A primer is a short description of the asset. Either way, the question you bring back to the path is the same: would a grid have had a range to work in, and what would have ended that idea?</p>"
        + index_list(market_rows),
    )
    pages["guides"] = page(
        "guides",
        "Guides",
        "where the longer lessons sit, and which step of the grid-bot path each one serves",
        "path/what",
        "step 1, what a grid bot is",
        "path/what",
        "What a grid bot is",
        "<p>Read a guide when the path uses a word you want more slowly. Then go back to the step named on that guide. The guides are not a second course.</p>"
        + index_list(guide_rows),
    )
    pages["glossary"] = page(
        "glossary",
        "Glossary",
        "the words you will meet while you set up, watch, and review a grid bot",
        "path/what",
        "step 1, what a grid bot is",
        "path/what",
        "What a grid bot is",
        "",
    )
    pages["search"] = page(
        "search",
        "Search",
        "how to find a grid-bot word or lesson that is already inside this file",
        "path/what",
        "step 1, what a grid bot is",
        "glossary",
        "Glossary",
        "",
    )
    pages["missing"] = page(
        "missing",
        "Pick a lesson",
        "how to get back onto the grid-bot path from an address this directory does not have",
        "path/what",
        "step 1, what a grid bot is",
        "path/what",
        "What a grid bot is",
        "",
    )

    # Related links once every target page exists.
    for filename, *_rest in GUIDES:
        pid = LINK_MAP[filename]
        meta, _body = parse_front((CONTENT / filename).read_text(encoding="utf-8"))
        pages[pid]["html"] += related_html(meta.get("related") or [], pages)

    path_rows = [(pid, label, FRAGMENTS[pid][1]) for pid, label in PATH]
    directory_body = (
        "<p>The path is the course. Everything else is a shelf that points back to a step.</p>"
        "<h2>The path</h2>"
        + index_list(path_rows)
        + "<h2>Shelves</h2>"
        + index_list(
            [
                ("glossary", "Glossary", "435 words, tied back to step 1"),
                ("guides", "Guides", "Longer lessons, each named to a step"),
                ("questions", "Questions", "A short answer and a link onward"),
                ("tools", "Tools", "Spacing, position size, and a journal average"),
                ("markets", "Market studies", "Samples and primers for the range question"),
                ("about", "About", "Who publishes Atlas"),
                ("contact", "Contact", "How to write to Market Pros"),
                ("terms", "Terms", "Draft rules of use"),
                ("privacy", "Privacy", "Draft notice, with blanks still open"),
                ("disclaimer", "Disclaimer", "Education, not personal advice"),
                ("notes", "NOTES", "The blanks Stewart still has to fill"),
            ]
        )
    )
    pages["directory"] = page(
        "directory",
        "The directory",
        "where every lesson sits, and which step of the grid-bot path it serves",
        "path/what",
        "step 1, what a grid bot is",
        "path/what",
        "What a grid bot is",
        directory_body,
    )

    # Placeholder pass and notes.
    found: dict[str, list[str]] = {}
    for pid, item in pages.items():
        item["html"] = mark_placeholders(item["html"])
        item["banner"] = mark_placeholders(item["banner"])
        for token in TOKEN_RE.findall(item["html"] + item["banner"]):
            found.setdefault(token, []).append(item["title"])
    notes_rows = []
    for token in sorted(found):
        where = ", ".join(sorted(set(found[token])))
        notes_rows.append(f"<li><mark class=\"placeholder\">{html.escape(token)}</mark> — {html.escape(where)}</li>")
    notes_html = """
<p>These blanks are still Stewart's. They are highlighted in amber wherever they appear. Do not invent a date, a postal address, a host, or a checklist URL to fill them.</p>
<h2>Named blanks</h2>
<ul>
<li><mark class="placeholder">[EFFECTIVE_DATE]</mark> on the terms, the privacy notice, and the disclaimer. Use the same date on all three when you publish.</li>
<li><mark class="placeholder">[POSTAL_ADDRESS]</mark> on the privacy notice, for the complaints path.</li>
<li><mark class="placeholder">[HOST]</mark> and the longer host example on the privacy notice. This file does not know where you will upload it.</li>
<li><mark class="placeholder">[PRIVACY_URL]</mark> in the checklist sign-up notice. Point it at the privacy page of the copy you actually publish.</li>
<li><mark class="placeholder">[CHECKLIST LINK]</mark> wherever The Grid Bot Starter Checklist is mentioned. The study checkboxes in this file are not that public file.</li>
</ul>
<h2>Every highlighted blank in this file</h2>
<ul>
""" + "".join(notes_rows) + """
</ul>
<h2>What this copy already changed</h2>
<p>The path, the home page, and the terms now describe Atlas as a directory for grid bots. This file embeds its fonts and its sample candles, so the privacy notice no longer says the browser calls a font host or a market-data service. The draft banners stay, because the wording still needs Stewart's sign-off. The footer records that Market Pros Proprietary Limited and ABN 19 679 270 387 were confirmed on 13 Nov 2026. The contact address written on the pages is contact@stewartcrowncrypto.com.</p>
<p>File size of this copy: __FILE_SIZE__ bytes.</p>
"""
    pages["notes"] = page(
        "notes",
        "NOTES",
        "which publisher blanks are still open, so you can find them without hunting",
        "path/setup",
        "step 3, setting one up",
        "path/what",
        "What a grid bot is",
        notes_html,
    )
    pages["notes"]["html"] = mark_placeholders(pages["notes"]["html"])

    # Link check.
    valid_pages = set(pages)
    hrefs = re.findall(r'href="#/([^"]+)"', "\n".join(item["html"] + item["banner"] for item in pages.values()))
    for href in hrefs:
        parts = href.split("/")
        if parts[0] == "markets" and len(parts) > 1 and parts[1] in markets:
            continue
        key = href
        if key in valid_pages:
            continue
        if len(parts) > 1 and "/".join(parts[:-1]) in valid_pages:
            parent = "/".join(parts[:-1])
            anchor = parts[-1]
            blob = pages[parent]["html"]
            if parent == "glossary":
                if anchor in anchors or anchor.startswith("letter-"):
                    continue
            if f'id="{anchor}"' in blob:
                continue
            raise SystemExit(f"Missing anchor #{anchor} on {parent} from href {href}")
        raise SystemExit(f"Broken directory link: #/{href}")

    payload = {
        "path": [{"id": pid, "label": label} for pid, label in PATH],
        "directory": [
            {"id": "directory", "label": "The directory"},
            {"id": "glossary", "label": "Glossary"},
            {"id": "guides", "label": "Guides"},
            {"id": "questions", "label": "Questions"},
            {"id": "tools", "label": "Tools"},
            {"id": "markets", "label": "Markets"},
            {"id": "notes", "label": "Notes"},
            {"id": "about", "label": "About"},
            {"id": "contact", "label": "Contact"},
        ],
        "pages": pages,
        "glossary": glossary,
        "markets": markets,
    }
    data_json = json.dumps(payload, ensure_ascii=True, separators=(",", ":")).replace("<", "\\u003c")
    css = font_css() + "\n" + (SINGLE / "shell.css").read_text(encoding="utf-8")
    js = (SINGLE / "shell.js").read_text(encoding="utf-8")
    icon = data_uri(ROOT / "favicon.svg", "image/svg+xml")
    document = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Atlas — a directory for grid bots</title>
<meta name="description" content="Atlas is Stewart Crown's directory for learning grid bots. One offline file: a seven-step path, a glossary, guides, calculators, and market studies.">
<link rel="icon" href="{icon}">
<style>
{css}
</style>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <div class="header-inner">
    <a class="brand" href="#/"><strong>ATLAS</strong><span>A directory for grid bots</span></a>
    <button class="menu-btn" id="menu-btn" type="button" aria-expanded="false" aria-controls="path-nav">Menu</button>
    <form class="search-form" id="search-form" role="search">
      <label class="visually-hidden" for="q">Search the directory</label>
      <input id="q" name="q" type="search" placeholder="Try range, fee, stop">
      <button type="submit">Search</button>
    </form>
  </div>
</header>
<div class="layout">
  <nav class="path-nav" id="path-nav" aria-label="Grid bot path and directory"></nav>
  <main id="main"></main>
</div>
<footer class="site-footer">
  <p>Atlas is a directory for grid bots, published by Market Pros Proprietary Limited (ABN 19 679 270 387). General information only, not financial product advice. It doesn't consider your objectives, financial situation or needs. Crypto and leveraged trading are high risk; you can lose all your money. Market Pros Proprietary Limited does not hold an AFSL.</p>
  <nav aria-label="Legal">
    <a href="#/terms">Terms</a>
    <a href="#/privacy">Privacy</a>
    <a href="#/disclaimer">Disclaimer</a>
    <a href="#/notes">NOTES</a>
    <a href="mailto:contact@stewartcrowncrypto.com">contact@stewartcrowncrypto.com</a>
  </nav>
  <p>Sample charts are bundled for study. This file does not need a network to open. Calculators use the numbers you type. They do not place orders.</p>
</footer>
<noscript class="noscript"><p>Atlas keeps every lesson in this file, and it uses JavaScript only to switch lessons and run the calculators. It does not need a network. Enable JavaScript to move through the path.</p></noscript>
<script>window.ATLAS={data_json};</script>
<script>
{js}
</script>
</body>
</html>
"""
    encoded = document.replace("__FILE_SIZE__", "00000000").encode("utf-8")
    size = len(encoded)
    document = document.replace("__FILE_SIZE__", f"{size:08d}")
    final = document.encode("utf-8")
    if len(final) != size:
        raise SystemExit(f"Size placeholder drifted: {len(final)} vs {size}")
    visible = "\n".join(
        item["html"] + item["banner"] + item["title"] + item["learn"] for item in pages.values()
    )
    visible += "\n".join(
        term["term"] + term["one_liner"] + term["explanation"] for term in glossary
    )
    visible += "\n".join(item["blurb"] + item["primer"] + item["name"] for item in markets.values())
    visible += (SINGLE / "shell.js").read_text(encoding="utf-8")
    visible = re.sub(r"data:[^\"'\s>]+", "", visible)
    lowered = visible.lower()
    for banned in (
        "lorem ipsum",
        "coming soon",
        "not in this build",
        "page was not included",
        "linked, and not included",
        "kyle",
    ):
        if banned in lowered:
            raise SystemExit(f"Banned phrase in output: {banned}")
    if re.search(r"\bTODO\b|\bFIXME\b", visible):
        raise SystemExit("TODO or FIXME left in the file")
    for name in ("Binance", "Coinbase", "Pionex", "Bybit", "KuCoin", "OKX", "Kraken", "CoinGecko"):
        if name.lower() in lowered:
            raise SystemExit(f"Exchange or data-vendor name in output: {name}")
    DIST.mkdir(parents=True, exist_ok=True)
    target = DIST / "atlas.html"
    target.write_bytes(final)
    print(f"Wrote {target} ({size} bytes, {size / 1024 / 1024:.2f} MiB)")
    print(f"Pages: {len(pages)} Glossary: {len(glossary)} Markets: {len(markets)}")
    print("Placeholders:")
    for token in sorted(found):
        print(" -", token)


if __name__ == "__main__":
    main()
