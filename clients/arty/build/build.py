#!/usr/bin/env python3
"""Build Arty_Trade_Plan_v2.pdf from the template and the chart scripts.

Run from anywhere:
    python3 clients/arty/build/build.py
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pypdfium2 as pdfium
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parent
OUT_DIR = ROOT.parent
PDF_PATH = OUT_DIR / "Arty_Trade_Plan_v2.pdf"
HTML_PATH = ROOT / "plan.html"
PAGE_DIR = ROOT / "page_png"

DISCLAIMER = (
    "Educational information only. This is not financial advice and not a "
    "guarantee of any result. Crypto and leveraged futures carry high risk, "
    "including the loss of the entire amount. Past figures and the example "
    "figures in this plan are not indicative of future results. The reader is "
    "responsible for their own decisions. Pionex is not affiliated with this "
    "plan. Verify every setting against Pionex’s current screens, fees, "
    "funding and product rules before any order."
)

FOOTER = (
    "Educational information only, not financial advice. Leveraged crypto "
    "futures can cause a total loss. Example figures are not indicative of "
    "future results. You are responsible for your decisions. Pionex is not "
    "affiliated. Verify this plan against Pionex’s current settings."
)

# Phrases that must not appear, even in the negative, outside the disclaimer.
BANNED_BODY = (
    "Market Pros",
    "passive income",
    "will make",
    "10% weekly",
    "10 percent a week",
    "per week growth",
    "growth marker",
    "$550",
    "550.00",
    "605.00",
    "665.50",
    "732.05",
    "5,232",
    "5232",
)


def fill_template() -> str:
    sys.path.insert(0, str(ROOT))
    import charts
    import plan_math

    charts.build_all()
    values = plan_math.context()
    values["disclaimer"] = DISCLAIMER
    values["footer"] = FOOTER
    html = (ROOT / "template.html").read_text(encoding="utf-8")
    for key, value in values.items():
        html = html.replace(f"[[{key}]]", value)
    if "[[" in html:
        missing = sorted({chunk.split("]]", 1)[0] for chunk in html.split("[[")[1:]})
        raise SystemExit(f"Unfilled tokens: {missing}")
    return html


def assert_copy(html: str) -> None:
    if html.count(DISCLAIMER) < 3:
        raise SystemExit("Disclaimer must appear on the cover, in the how-to page, and on the sign-off page.")
    if html.count(FOOTER) < 14:
        raise SystemExit("Footer disclaimer missing from an interior page.")
    body = html.replace(DISCLAIMER, "")
    for phrase in BANNED_BODY:
        if phrase.lower() in body.lower():
            raise SystemExit(f"Banned phrase in the plan body: {phrase}")
    if "Market Pros" in html:
        raise SystemExit("Company name found.")


def write_pdf(html: str) -> None:
    HTML_PATH.write_text(html, encoding="utf-8")
    cmd = [
        "google-chrome",
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--disable-dev-shm-usage",
        "--user-data-dir=/tmp/arty-chrome-pdf",
        "--no-pdf-header-footer",
        "--virtual-time-budget=15000",
        "--timeout=20000",
        f"--print-to-pdf={PDF_PATH}",
        HTML_PATH.as_uri(),
    ]
    # Headless Chrome writes the PDF, then often keeps running on this host.
    # A timeout after the file exists is a finished print, not a failed one.
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=25)
    except subprocess.TimeoutExpired:
        if not PDF_PATH.exists() or PDF_PATH.stat().st_size < 10_000:
            raise SystemExit("Chrome did not write a PDF before the timeout.")


def audit_pdf() -> int:
    reader = PdfReader(str(PDF_PATH))
    pages = len(reader.pages)
    if not 10 <= pages <= 16:
        raise SystemExit(f"Page count {pages} is outside 10–16.")
    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    if "Educational information only" not in text:
        raise SystemExit("Disclaimer text missing from the PDF.")
    if "Pionex is not affiliated" not in text:
        raise SystemExit("Affiliation line missing from the PDF.")
    for phrase in ("Market Pros", "passive income", "will make", "10% weekly", "732.05", "5,232"):
        if phrase.lower() in text.lower():
            raise SystemExit(f"Banned phrase in the PDF: {phrase}")
    required = (
        "2,015.00",
        "2,415.00",
        "32.83%",
        "19.50%",
        "2.67%",
        "1.60%",
        "2,835",
        "3,165",
        "0.876%",
        "0.0946",
        "DOGE",
        "isolated",
        "14 days",
        "[[",
    )
    for token in required:
        if token not in text and token != "[[":
            raise SystemExit(f"Expected figure missing from the PDF text: {token}")
        if token == "[[" and token in text:
            raise SystemExit("Unfilled token survived into the PDF.")
    return pages


def render_pages() -> None:
    PAGE_DIR.mkdir(parents=True, exist_ok=True)
    pdf = pdfium.PdfDocument(str(PDF_PATH))
    scale = 140 / 72
    for index in range(len(pdf)):
        bitmap = pdf[index].render(scale=scale)
        image = bitmap.to_pil()
        image.save(PAGE_DIR / f"page-{index + 1:02d}.png")
    pdf.close()


def main() -> None:
    html = fill_template()
    assert_copy(html)
    write_pdf(html)
    pages = audit_pdf()
    render_pages()
    print(f"Wrote {PDF_PATH} ({pages} pages)")
    print(f"Page images in {PAGE_DIR}")


if __name__ == "__main__":
    main()
