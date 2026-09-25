#!/usr/bin/env python3
"""Crop each section of Day-1-Setup-Kit.pdf into assets/kit/*.png for the kit video.
Each section is found by its heading on whatever page it lands on, and ends at the
next heading on that page (or the page's content bottom)."""
from pathlib import Path
import pymupdf

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "kit"
OUT.mkdir(parents=True, exist_ok=True)
doc = pymupdf.open(ROOT / "Day-1-Setup-Kit.pdf")
MARKS = ["Part A", "Part B", "Part C", "Part D", "Part E", "Part F", "All ticked", "The 10 rules"]


def find(text, nth=-1):
    hits = sorted((i, r.y0) for i, pg in enumerate(doc) for r in pg.search_for(text))
    return hits[nth]  # last by page and position: headings come after any in-list mentions


def section(name, start, end=None, pad_end=0):
    page, y0 = find(start)
    ys = [y for m in MARKS for (p, y) in [find(m)] if p == page and y > y0 + 1]
    y1 = (find(end)[1] + pad_end) if end else (min(ys) - 6 if ys else doc[page].rect.height - 55)
    r = doc[page].rect
    text_bottom = max((b[3] for b in doc[page].get_text("blocks") if b[1] >= y0 - 2 and b[3] <= y1 + 1), default=y1)
    y1 = min(y1, text_bottom + 12)  # trim empty space below the section
    doc[page].get_pixmap(matrix=pymupdf.Matrix(3, 3), clip=pymupdf.Rect(40, y0 - 8, r.width - 40, y1)).save(OUT / f"{name}.png")
    print(f"wrote assets/kit/{name}.png (page {page + 1})")


doc[0].get_pixmap(matrix=pymupdf.Matrix(2, 2)).save(OUT / "cover.png"); print("wrote assets/kit/cover.png")
p, ya = find("Part A")
doc[p].get_pixmap(matrix=pymupdf.Matrix(3, 3), clip=pymupdf.Rect(40, 40, doc[p].rect.width - 40, ya - 8)).save(OUT / "intro.png"); print("wrote assets/kit/intro.png")
for n, m in zip(["part-a", "part-b", "part-c", "part-d", "part-e"], MARKS[:5]):
    section(n, m)
section("part-f", "Part F", "All ticked", pad_end=30)
section("rules", "The 10 rules")

# Wide, short crops read best on video: "What you need" alone, and the rules in two halves.
def band(name, start, end, start_nth=-1, pad_end=-6):
    page, y0 = find(start, start_nth)
    _, y1 = find(end)
    r = doc[page].rect
    doc[page].get_pixmap(matrix=pymupdf.Matrix(3, 3), clip=pymupdf.Rect(40, y0 - 8, r.width - 40, y1 + pad_end)).save(OUT / f"{name}.png")
    print(f"wrote assets/kit/{name}.png (page {page + 1})")


band("needs", "The checklist", "Part A")
p5, y6_ = find("Test first")
_, yr = find("The 10 rules")
line5_bottom = max(b[3] for b in doc[p5].get_text("blocks") if b[1] >= yr - 2 and b[3] <= y6_ + 1)
doc[p5].get_pixmap(matrix=pymupdf.Matrix(3, 3), clip=pymupdf.Rect(40, yr - 8, doc[p5].rect.width - 40, line5_bottom + 6)).save(OUT / "rules-1.png")
print(f"wrote assets/kit/rules-1.png (page {p5 + 1})")
p, y6 = find("Test first")
text_bottom = max(b[3] for b in doc[p].get_text("blocks") if b[1] >= y6 - 2 and b[3] < doc[p].rect.height - 60)
doc[p].get_pixmap(matrix=pymupdf.Matrix(3, 3), clip=pymupdf.Rect(40, y6 - 3, doc[p].rect.width - 40, text_bottom + 10)).save(OUT / "rules-2.png")
print(f"wrote assets/kit/rules-2.png (page {p + 1})")
