#!/usr/bin/env python3
"""Combine every On-Chain Operator Program file into one master document.

Run from anywhere: python3 programs/defi-program/build_master.py
Writes programs/defi-program/ON-CHAIN-OPERATOR-PROGRAM.md
"""
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
OUT = HERE / "ON-CHAIN-OPERATOR-PROGRAM.md"


def read(path):
    return (HERE / path).read_text().strip()


def module_02_with_sample():
    """Insert the sample lesson 2.2 between lessons 2.1 and 2.3."""
    mod = read("lessons/module-02-trading-on-chain.md")
    sample = read("02-sample-lesson-amm-math.md").replace("\n## ", "\n### ")
    sample = sample.replace("# Sample Lesson 2.2", "## Lesson 2.2", 1)
    mod = mod.replace("Lesson 2.2 (AMM mathematics) is in `../02-sample-lesson-amm-math.md`.\n", "")
    head, sep, tail = mod.partition("## Lesson 2.3")
    return f"{head}{sample}\n\n---\n\n{sep}{tail}"


def numbered(path, n, title):
    """Swap a source file's H1 for a numbered master-file heading."""
    return f"# {n}. {title}\n" + read(path).split("\n", 1)[1]


def lesson_files():
    """Module files in order; 2 gets the sample lesson, 8.3 comes from 03."""
    parts = []
    for f in sorted((HERE / "lessons").glob("module-*.md")):
        num = int(f.name.split("-")[1])
        if num == 9:
            parts.append(read("03-defi-strategy-mastery.md"))
        parts.append(module_02_with_sample() if num == 2 else f.read_text().strip())
    return [p.replace("](../assets/", "](assets/") for p in parts]


def main():
    sections = [
        f"# On-Chain Operator Program — Master File\n\n"
        f"![On-Chain Operator Program](assets/brand/logo-horizontal-light.png)\n\n"
        f"*Generated {date.today().isoformat()} from `programs/defi-program/`. "
        f"Don't edit this file directly: edit the source files and run "
        f"`python3 programs/defi-program/build_master.py`.*\n\n"
        "## Contents\n"
        "1. Build status\n2. Offer, decisions & curriculum\n3. Whop setup\n"
        "4. Whop store listing (logo, images, copy)\n5. Operations kit (capstones, application, call script, emails, live tier, terms)\n"
        "6. Worksheets & templates\n7. Funnel changes\n8. Video scripts (VSLs, welcome, module intros)\n"
        "9. Course content (all 79 lessons)\n10. Skills archive\n11. Build prompt (hand this to Grok or Claude Code)",
        "# 1. Build status\n\n" + read("README.md").split("\n", 1)[1],
        numbered("01-offer-and-curriculum.md", 2, "Offer, decisions & curriculum"),
        numbered("05-whop-setup.md", 3, "Whop setup"),
        numbered("06-whop-store-listing.md", 4, "Whop store listing"),
        numbered("07-program-operations.md", 5, "Operations kit"),
        numbered("08-worksheets.md", 6, "Worksheets & templates"),
        numbered("04-funnel-changes.md", 7, "Funnel changes (draft, not applied)"),
        *([numbered("video/SCRIPTS.md", 8, "Video scripts")] if (HERE / "video/SCRIPTS.md").exists() else []),
        "# 9. Course content\n\nFinished lessons in curriculum order. "
        "Lesson 8.3 (strategy mastery) appears before Module 9.",
        *lesson_files(),
        "# 10. Skills archive\n\n" + (ROOT / "README.md").read_text().split("\n", 1)[1].strip(),
        read("BUILD-PROMPT.md").replace("# Build Prompt", "# 11. Build Prompt", 1),
    ]
    OUT.write_text("\n\n---\n\n".join(sections) + "\n")
    print(f"Wrote {OUT.relative_to(ROOT)} ({OUT.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
